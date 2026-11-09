#!/usr/bin/env bash
# harden.sh — first-5-minutes defensive hardening for your A&D vulnbox.
# RUN AS ROOT, ON YOUR OWN BOX ONLY, AFTER you have taken a backup.
# It is intentionally conservative: it does NOT stop game services (SLA!).
#
#   sudo bash harden.sh            # interactive-ish, prints what it does
#
set -uo pipefail
say(){ printf '\n\033[1;36m[harden]\033[0m %s\n' "$*"; }

# 0. SAFETY: back up before anything --------------------------------------
TS=$(date +%s)
say "Backing up service dirs to /root/ORIGINAL_${TS}.tar.gz ..."
tar czf "/root/ORIGINAL_${TS}.tar.gz" /srv /opt /var/www /home /etc/passwd /etc/shadow 2>/dev/null \
  && echo "  backup ok" || echo "  (some paths missing, continuing)"

# 1. Inventory ------------------------------------------------------------
say "Listening services (port -> process):"
ss -tulpn 2>/dev/null | sed 's/^/  /'
say "Docker (if any):"
command -v docker >/dev/null && docker ps --format '  {{.Names}}  {{.Ports}}  {{.Image}}' || echo "  no docker"
say "Shell users (watch for attacker-added accounts):"
awk -F: '$7 ~ /sh$/ {print "  "$1" ("$7")"}' /etc/passwd
say "Recently changed files (last 2h, service dirs):"
find /srv /opt /var/www /home -newermt '-2 hours' -type f 2>/dev/null | grep -vE '/\.git/' | sed 's/^/  /' | head -40

# 2. Rotate YOUR password (the organizer default is shared with everyone) --
say "Rotate your login password NOW (shared defaults = instant compromise)."
read -rp "  Set a new password for current user '$(whoami)'? [y/N] " a
[[ "${a,,}" == y ]] && passwd

# 3. SSH hardening (keep your own access!) ---------------------------------
if [ -f /etc/ssh/sshd_config ]; then
  say "Hardening sshd (PermitRootLogin, keep current sessions alive)..."
  cp /etc/ssh/sshd_config "/root/sshd_config.bak.${TS}"
  sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config
  # Only disable password auth if an authorized_keys exists (else you lock yourself out):
  if [ -s "$HOME/.ssh/authorized_keys" ]; then
    sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
    echo "  password auth disabled (you have a key)"
  else
    echo "  !! no authorized_keys found — leaving password auth ON so you don't lock out"
  fi
  systemctl reload ssh 2>/dev/null || systemctl reload sshd 2>/dev/null || service ssh reload 2>/dev/null
fi

# 4. Kill web debug modes (RCE + source leak) -----------------------------
say "Scanning for debug flags to disable (review before trusting)..."
grep -rilE 'debug\s*=\s*true|DEBUG\s*=\s*True|display_errors\s*=\s*On|FLASK_ENV=development' \
  /srv /opt /var/www 2>/dev/null | sed 's/^/  CHECK: /' | head -30
echo "  -> manually flip these off in source; a blind sed can break SLA."

# 5. Hunt obvious backdoors -----------------------------------------------
say "Searching for webshell / backdoor signatures (review each hit):"
grep -rilE '(eval|assert|system|exec|passthru|shell_exec)\s*\(\s*\$_(POST|GET|REQUEST)' \
  /srv /opt /var/www 2>/dev/null | sed 's/^/  SHELL?: /'
grep -rilE 'bash -i|/dev/tcp/|nc .*-e|pty.spawn' \
  /srv /opt /var/www 2>/dev/null | sed 's/^/  REVSHELL?: /'
find /srv /opt /var/www -type f -perm -0002 2>/dev/null | sed 's/^/  WORLD-WRITABLE: /' | head -20

# 6. Cron / persistence check ---------------------------------------------
say "Cron entries (look for planted persistence):"
for u in $(cut -f1 -d: /etc/passwd); do
  c=$(crontab -l -u "$u" 2>/dev/null) && [ -n "$c" ] && echo "  [$u]" && echo "$c" | sed 's/^/    /'
done
ls -la /etc/cron.* 2>/dev/null | sed 's/^/  /' | head -30

say "DONE. Next: firewall.sh, then service_monitor.py snapshot, then patch & keep SLA green."
