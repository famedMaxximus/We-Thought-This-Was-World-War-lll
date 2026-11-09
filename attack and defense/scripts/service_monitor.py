#!/usr/bin/env python3
"""
service_monitor.py — Defense: snapshot service files and alert on tampering.

First run:  stores a hash snapshot of every file under the watched dirs.
Later runs: reports files ADDED / MODIFIED / DELETED since the snapshot, and
greps new/modified files for webshell & backdoor signatures.

Usage:
  ./service_monitor.py snapshot /srv /var/www /opt      # baseline (after YOUR patches)
  ./service_monitor.py check    /srv /var/www /opt      # one check
  ./service_monitor.py watch    /srv /var/www /opt      # loop every 20s

Re-run `snapshot` yourself after every legit patch so your own edits don't alarm.
"""
import hashlib, json, os, re, sys, time

STATE = os.path.join(os.path.dirname(__file__), ".monitor_state.json")
SKIP_DIRS = {'.git', '__pycache__', 'node_modules', '.cache'}
# Signatures of planted webshells / backdoors:
SIGS = [
    rb'eval\s*\(\s*(base64_decode|gzinflate|\$_(POST|GET|REQUEST))',
    rb'(system|exec|passthru|shell_exec|popen|proc_open)\s*\(\s*\$_(POST|GET|REQUEST)',
    rb'assert\s*\(\s*\$_(POST|GET|REQUEST)',
    rb'os\.(system|popen)\s*\(.*request',
    rb'subprocess\.(call|Popen|run)\(.*request',
    rb'__import__\(["\']os["\']\)',
    rb'pickle\.loads',
    rb'\b(nc|ncat|netcat)\b.*-e',
    rb'/bin/(ba)?sh.*-i',
    rb'bash\s+-i\s+>&\s*/dev/tcp',
]
SIGS = [re.compile(s, re.I) for s in SIGS]

def walk(dirs):
    for d in dirs:
        for root, subdirs, files in os.walk(d):
            subdirs[:] = [s for s in subdirs if s not in SKIP_DIRS]
            for fn in files:
                yield os.path.join(root, fn)

def digest(path):
    try:
        h = hashlib.sha256()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(65536), b''):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

def scan_sigs(path):
    hits = []
    try:
        with open(path, 'rb') as f:
            data = f.read(512 * 1024)
        for rx in SIGS:
            if rx.search(data):
                hits.append(rx.pattern.decode('latin1'))
    except Exception:
        pass
    return hits

def snapshot(dirs):
    snap = {p: digest(p) for p in walk(dirs)}
    json.dump({"dirs": dirs, "files": snap, "ts": time.time()}, open(STATE, 'w'))
    print(f"[snapshot] {len(snap)} files baselined under {dirs}")

def check(dirs):
    try:
        old = json.load(open(STATE))["files"]
    except FileNotFoundError:
        print("[!] no snapshot — run `snapshot` first"); return False
    cur = {p: digest(p) for p in walk(dirs)}
    added    = [p for p in cur if p not in old]
    deleted  = [p for p in old if p not in cur]
    modified = [p for p in cur if p in old and cur[p] != old[p]]
    alarm = False
    for label, items in (("ADDED", added), ("MODIFIED", modified), ("DELETED", deleted)):
        for p in items:
            msg = f"[{label}] {p}"
            if label != "DELETED":
                hits = scan_sigs(p)
                if hits:
                    msg += f"   <<< WEBSHELL/BACKDOOR SIG: {hits}"
                    alarm = True
            print(msg)
    if not (added or deleted or modified):
        print("[ok] no changes since snapshot")
    return alarm

def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    mode, dirs = sys.argv[1], sys.argv[2:]
    if mode == "snapshot":
        snapshot(dirs)
    elif mode == "check":
        check(dirs)
    elif mode == "watch":
        print("[watch] Ctrl-C to stop")
        while True:
            print("---", time.strftime("%H:%M:%S"))
            check(dirs)
            time.sleep(20)
    else:
        print(__doc__)

if __name__ == "__main__":
    main()
