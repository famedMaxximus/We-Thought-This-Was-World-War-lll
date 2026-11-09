#!/usr/bin/env python3
"""
flag_proxy.py — a logging reverse proxy you drop IN FRONT of a game service.

Two uses:
  1. DEFENSE VISIBILITY (safe): log every request+response so you see exploits live.
  2. LAST-DITCH EGRESS FILTER (risky for SLA): optionally redact/deny responses that
     contain OTHER teams' flag patterns leaving your box. Test against the checker first —
     if the checker's own planted flag gets blocked you lose SLA. Use --block only if the
     service is already being farmed and you can't patch in time.

Run it on a spare port and point the game port at it (or vice-versa via iptables REDIRECT).

  # observe only:
  ./flag_proxy.py --listen 0.0.0.0:9080 --upstream 127.0.0.1:8080

  # observe + block outbound flags (CAREFUL):
  ./flag_proxy.py --listen 0.0.0.0:9080 --upstream 127.0.0.1:8080 \
       --block --flag 'LsCTF2026\\{[^}]+\\}'

Pure stdlib; handles raw TCP (works for HTTP and most line protocols).
"""
import argparse, re, socket, sys, threading, time

def pipe(src, dst, tag, flag_re, block, logf):
    """Copy src->dst, logging and optionally redacting flag matches."""
    src.settimeout(300)
    try:
        while True:
            data = src.recv(65536)
            if not data:
                break
            if flag_re:
                hits = flag_re.findall(data)
                if hits:
                    ts = time.strftime("%H:%M:%S")
                    msg = f"[{ts}] {tag} FLAG-IN-STREAM x{len(hits)}: {hits[:3]}"
                    print(msg); logf and logf.write(msg + "\n") and logf.flush()
                    if block and tag == "<-upstream":   # only redact RESPONSES leaving us
                        data = flag_re.sub(b"[REDACTED]", data)
            dst.sendall(data)
    except Exception:
        pass
    finally:
        for s in (src, dst):
            try: s.shutdown(socket.SHUT_RDWR)
            except Exception: pass

def handle(client, up_host, up_port, flag_re, block, logf):
    try:
        upstream = socket.create_connection((up_host, up_port), timeout=10)
    except Exception as e:
        print(f"[!] upstream {up_host}:{up_port} unreachable: {e}")
        client.close(); return
    threading.Thread(target=pipe, args=(client, upstream, "client->", flag_re, block, logf), daemon=True).start()
    threading.Thread(target=pipe, args=(upstream, client, "<-upstream", flag_re, block, logf), daemon=True).start()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--listen", required=True, help="host:port to listen on")
    ap.add_argument("--upstream", required=True, help="host:port of the real service")
    ap.add_argument("--flag", help="flag regex to watch (and redact with --block)")
    ap.add_argument("--block", action="store_true", help="redact flags in RESPONSES (SLA risk!)")
    ap.add_argument("--log", help="append log to this file")
    args = ap.parse_args()
    lh, lp = args.listen.split(":"); uh, up = args.upstream.split(":")
    flag_re = re.compile(args.flag.encode()) if args.flag else None
    logf = open(args.log, "a") if args.log else None
    if args.block and not flag_re:
        sys.exit("--block needs --flag")

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((lh, int(lp))); srv.listen(128)
    print(f"[proxy] {args.listen} -> {args.upstream}  "
          f"{'BLOCKING flags' if args.block else 'observe-only'}")
    while True:
        client, addr = srv.accept()
        threading.Thread(target=handle,
                         args=(client, uh, int(up), flag_re, args.block, logf),
                         daemon=True).start()

if __name__ == "__main__":
    main()
