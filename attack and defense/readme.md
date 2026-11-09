# Attack & Defense — Battle Plan

> **Scope:** Everything here is for the **sanctioned Lesotho Cybersecurity Hackathon finals** only.
> You act **only** against the CTF-provided targets (your own box + the other teams' vulnbox
> IPs the gameserver gives you). Never touch anything outside the scoreboard's declared range.

## 0. What Attack & Defense actually is

Every team gets an **identical "vulnbox"** running several vulnerable services. A central
**gameserver** does two things on a fixed tick (usually every 1–5 min):

1. **Plants flags** into every team's services (SLA checker also confirms the service still works).
2. **Lets you submit flags** you stole from *other* teams' services.

You score by:
- **Attack points** — submitting valid, fresh flags stolen from opponents.
- **Defense points** — keeping your own flags from being stolen (patching the bug).
- **SLA/uptime points** — keeping your services *functional* (a patch that breaks the service loses SLA — this is the #1 rookie mistake).

**The golden rule: a patched-but-broken service scores worse than an unpatched working one.**
Patch minimally, keep the service passing the checker.

## 1. Roles (assign BEFORE the match)

With a team of 3–5, split like this and don't let everyone dogpile one service:

| Role | Owner | Job |
|------|-------|-----|
| **Captain / Scorekeeper** | 1 person | Watches scoreboard, calls targets, runs flag submitter, time-boxes everyone. |
| **Defense lead** | 1 person | Runs `harden.sh` + `firewall.sh` in first 5 min, backs up all services, monitors diffs. |
| **Attack lead(s)** | 1–2 | Find the bug in ONE service each, weaponize, feed exploit to `exploit_runner.py`. |
| **Traffic/IR** | 1 (can be shared) | Runs `tcpdump`, watches for incoming exploits, steals opponents' exploits from PCAP. |

Everyone shares findings in one channel/notes file. **One service = one attack owner** to avoid duplicate work.

## 2. First 15 minutes (do these IN ORDER, don't skip)

```
T+0   Get your vulnbox IP, SSH creds, scoreboard URL, flag format, team IP range, tick length.
T+1   Defense lead: snapshot EVERYTHING first (see §3). Do NOT edit before you back up.
T+3   Everyone: enumerate services  ->  ss -tlnp ; docker ps ; ls /srv /opt /home
T+5   Defense lead: run harden.sh (rotate creds, kill default passwords) + firewall.sh (log all).
T+7   Attack leads: pull one service's source each into the attack/ repo, start reading for bugs.
T+8   Traffic/IR: start tcpdump -> rolling PCAPs (see §4). This is how you steal others' 0days.
T+10  Captain: confirm flag format + regex, test ONE manual flag submit so the pipeline works.
T+12  Keep SLA green: never hard-down a service. Verify checker still passes after every change.
T+15  First exploits should be in testing against your OWN box before firing at opponents.
```

## 3. Golden backup rule (do this before touching anything)

```bash
# On the vulnbox, immediately:
sudo tar czf /root/ORIGINAL_$(date +%s).tar.gz /srv /opt /var/www /home 2>/dev/null
# If services are dockerized, also:
docker ps -q | xargs -I{} docker commit {} backup/{}:original
# Pull a copy OFF the box to your laptop too, in case the box is reset:
#   scp -r user@VULNBOX:/srv ./vulnbox_backup/
```
If a patch breaks a service, you restore in seconds instead of panicking.

## 4. Steal exploits from traffic (free attack points)

Other teams will attack you. Their exploits hit your box in the clear. Capture and replay them.

```bash
# Rolling capture, 5-min files, so disk never fills:
sudo tcpdump -i any -w /root/cap/ad_%Y%m%d_%H%M%S.pcap -G 300 -z gzip
```
Then run `scripts/pcap_steal.py` to pull out flag-shaped strings and the requests that produced
them. If you see a request pattern that returns a flag, you just got a free exploit — point it at
everyone with `exploit_runner.py`. (See `attack_script.md` §5.)

## 5. The two loops you run all match

**Defense loop (every tick):** diff services vs backup (`service_monitor.py`) → investigate any
change you didn't make → re-check SLA green → look for new flags being stolen.

**Attack loop (every tick):** for each working exploit, run `exploit_runner.py` against all live
team IPs → auto-submit harvested flags → watch which targets stopped yielding (they patched) →
move to next service.

## 6. Files in this folder

| File | What it is |
|------|-----------|
| `readme.md` | This battle plan. |
| `defense.md` | Full hardening + patching + monitoring playbook. |
| `attack_script.md` | Full exploitation + flag-farming playbook. |
| `scripts/harden.sh` | First-5-min hardening (creds, SSH, disable debug). |
| `scripts/firewall.sh` | iptables baseline with logging + per-service rate limits. |
| `scripts/service_monitor.py` | Snapshots & diffs service files, alerts on tampering/webshells. |
| `scripts/exploit_runner.py` | Runs your exploit vs all teams each tick, auto-submits flags. |
| `scripts/pcap_steal.py` | Pulls flags + attacker requests out of captured traffic. |
| `scripts/flag_proxy.py` | Logging reverse proxy; optional outbound-flag blocking (defense). |
| `scripts/requirements.txt` | pip deps for the Python tools. |

## 7. Pre-match checklist (print this)

- [ ] Laptop: python3, pip, nmap, tcpdump, netcat, curl, git, tmux, gdb/pwndbg, wireshark/tshark
- [ ] `pip install -r scripts/requirements.txt` done & tested OFFLINE before the venue
- [ ] SSH key + known-good creds to your vulnbox saved
- [ ] Scoreboard URL + submission API + API token field names known
- [ ] Flag regex confirmed (edit it into `exploit_runner.py` and `pcap_steal.py`)
- [ ] Team IP range / target list format known
- [ ] tmux layout rehearsed (one window per role)
- [ ] Everyone has run `harden.sh`/`firewall.sh` on a throwaway box once already
- [ ] Shared notes doc open; roles assigned; tick length written on the whiteboard
