# Defense Playbook

> Goal: keep your flags un-stealable **and** your services SLA-green. Patch the bug, not the feature.

## 1. Order of operations (never deviate)

1. **Back up first** (see `readme.md` §3). No edits before a backup exists.
2. **Enumerate** every listening service and what runs it.
3. **Harden the box** (creds, SSH, debug flags) — `harden.sh`.
4. **Firewall + logging** — `firewall.sh`. Default to logging, not blocking, so SLA survives.
5. **Read the source** of each service; find & minimally patch bugs.
6. **Monitor** continuously — `service_monitor.py` + traffic.
7. **Verify SLA after every single change.**

## 2. Enumerate the box

```bash
ss -tulpn                      # every listening port + the process
ps auxf                        # process tree, spot weird children of web servers
docker ps ; docker compose ls  # containerized services
ls -la /srv /opt /var/www /home/*/   # where services usually live
crontab -l ; ls /etc/cron.*    # persistence / planted backdoors
find / -newermt '-2 hours' -type f 2>/dev/null | grep -vE '/proc|/sys'  # recently changed
cat /etc/passwd | grep -E 'sh$'    # shell users (spot attacker-added accounts)
```
Map **port → process → source directory → language** for every service. Write it down.

## 3. Credential & access hardening (`harden.sh` covers most)

- **Rotate every password** the organizers shipped (DB, admin panels, service accounts). Teams
  share the same default creds — if you don't change yours, anyone logs in.
- **SSH:** disable password auth if you have keys; change known default passwords otherwise.
- **Kill debug modes:** Flask `debug=True`, Django `DEBUG=True`, PHP `display_errors`, Node dev
  mode, Werkzeug console — these leak source/flags and give RCE.
- **Remove obvious backdoors:** search services for `eval(`, `exec(`, `system(`, `shell_exec(`,
  `os.popen`, base64-decoded blobs, odd `/upload` dirs, files with 777 perms.
- **DB:** bind to localhost only unless the service genuinely needs remote; drop default users.

## 4. Firewall strategy (SLA-safe)

**Do NOT blanket-block.** The checker must reach your services or you lose SLA.
- Allow: scoreboard/checker source (if known), established connections, loopback, your SSH.
- Allow each **game service port** (checker needs it) but **log** it and rate-limit abusive floods.
- Block: everything else inbound, and egress to places a service should never talk to.
- Consider **egress filtering on flag format** as a last-ditch (see `flag_proxy.py`) — stops flags
  leaving in HTTP responses. Risky for SLA; test first.

`firewall.sh` sets a logging-first baseline. Watch `dmesg`/`/var/log/kern.log` for the `AD-DROP`/
`AD-SVC` tags to see who's hitting you.

## 5. Patching common bug classes (minimal, SLA-preserving)

| Bug class | Tell-tale in source | Minimal patch |
|-----------|--------------------|---------------|
| **Path traversal** | `open(base + user_input)`, `../` reaches files | `os.path.realpath` + assert it stays under base dir; reject `..`. |
| **SQL injection** | string-concatenated queries | switch to parameterized query; or whitelist/escape the one param. |
| **Command injection** | `os.system(f"...{x}")`, `shell_exec` | `shlex.quote`, or `subprocess` with arg list + `shell=False`; whitelist. |
| **Auth bypass** | `==` on secrets, type juggling (`==` vs `===`), missing check | `hmac.compare_digest`; add the missing authz check. |
| **Insecure deserialization** | `pickle.loads`, `yaml.load`, PHP `unserialize` | `yaml.safe_load`, reject untrusted pickle, signed payloads only. |
| **SSTI** | user input into `render_template_string`/Jinja | render with context vars, never format user data into the template. |
| **Weak crypto / hardcoded key** | static key, ECB, predictable IV | rotate key to a per-box random one *if the checker allows* (careful: shared keys may be checker-required — test!). |
| **File upload RCE** | uploads servable + executable | force content-type, strip extensions, store outside web root, `chmod -x`. |
| **IDOR** | object id from user, no owner check | add ownership/authz check on the id. |
| **Debug/info leak** | stack traces, `/debug`, `.git/` exposed | disable debug, block the path, remove `.git`. |

**After each patch:** run the service's own checker action manually (login, fetch, store/retrieve a
test "flag") to confirm it still behaves. Then diff-watch for re-exploitation.

## 6. Detecting active exploitation

- `service_monitor.py` snapshots every service dir and **alerts on any file change** you didn't
  make (webshells, modified handlers, new routes) and greps for webshell signatures.
- Tail service logs for anomalies: bursts of 500s, `../`, `UNION SELECT`, `/bin/sh`, long base64.
- Watch `tcpdump` (via `pcap_steal.py`) — **incoming** exploits are also **free exploits for you**.
  When you see a request that pulls a flag out of your box, replay it at everyone.

## 7. "Keep SLA green" discipline

- Never stop/restart a service without confirming it comes back.
- If a patch is risky, deploy behind `flag_proxy.py` (log + optional filter) first, observe, then
  bake the fix into source.
- Keep a `restore.sh` one-liner ready: `tar xzf /root/ORIGINAL_*.tar.gz -C /` then restart.
- If you break it and can't fix fast → **restore the backup immediately**, SLA beats a perfect patch.

## 8. Defense checklist per service

- [ ] Source pulled into repo + read
- [ ] Backup taken
- [ ] Default creds rotated
- [ ] Debug/verbose off
- [ ] Known bug(s) patched minimally
- [ ] SLA action re-tested and green
- [ ] Monitor watching the dir
- [ ] Logs being captured
