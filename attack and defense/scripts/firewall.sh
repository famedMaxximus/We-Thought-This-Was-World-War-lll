#!/usr/bin/env bash
# firewall.sh — SLA-safe iptables baseline for an A&D vulnbox.
# Philosophy: LOG everything, keep game service ports OPEN (checker must reach them),
# rate-limit floods, block the random junk. Never blanket-drop inbound to a game port.
#
#   sudo bash firewall.sh "22 80 8080 5000 3306"   # <-- list YOUR service ports
#
# Pass the ports your services listen on (from `ss -tulpn`). SSH (22) is kept open.
# Watch hits:  dmesg -w | grep AD-     (or tail /var/log/kern.log)
set -euo pipefail
PORTS="${1:-22 80 443 8080 5000}"
echo "[fw] opening + logging ports: $PORTS"

ipt=iptables
$ipt -F; $ipt -X 2>/dev/null || true

# Default: allow loopback + established, drop the rest inbound (but we open svc ports below).
$ipt -P INPUT DROP
$ipt -P FORWARD DROP
$ipt -P OUTPUT ACCEPT
$ipt -A INPUT -i lo -j ACCEPT
$ipt -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
$ipt -A INPUT -p icmp --icmp-type echo-request -m limit --limit 5/s -j ACCEPT

# Keep SSH reachable for YOU (optionally restrict --source to your laptop IP).
$ipt -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m limit --limit 10/min -j ACCEPT

# Game service ports: OPEN but logged + flood-limited so SLA checker always gets in.
for p in $PORTS; do
  [ "$p" = "22" ] && continue
  # log a sample of new connections (so you can see who attacks you)
  $ipt -A INPUT -p tcp --dport "$p" -m conntrack --ctstate NEW \
       -m limit --limit 2/sec -j LOG --log-prefix "AD-SVC:$p " --log-level 6
  # rate-limit per-source to blunt floods without blocking the checker
  $ipt -A INPUT -p tcp --dport "$p" -m conntrack --ctstate NEW \
       -m hashlimit --hashlimit-above 50/sec --hashlimit-burst 100 \
       --hashlimit-mode srcip --hashlimit-name "fl$p" \
       -j LOG --log-prefix "AD-FLOOD:$p " --log-level 4
  $ipt -A INPUT -p tcp --dport "$p" -m conntrack --ctstate NEW \
       -m hashlimit --hashlimit-above 80/sec --hashlimit-burst 160 \
       --hashlimit-mode srcip --hashlimit-name "fl${p}d" -j DROP
  $ipt -A INPUT -p tcp --dport "$p" -j ACCEPT
done

# Everything else inbound: log a trickle, then drop.
$ipt -A INPUT -m limit --limit 1/sec -j LOG --log-prefix "AD-DROP " --log-level 4

echo "[fw] active. Rules:"
$ipt -L INPUT -n --line-numbers | sed 's/^/  /'
echo "[fw] Watch attacks:  sudo dmesg -w | grep -E 'AD-SVC|AD-FLOOD'"
echo "[fw] Reset if it breaks SLA:  sudo iptables -P INPUT ACCEPT; sudo iptables -F"
