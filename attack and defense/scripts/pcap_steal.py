#!/usr/bin/env python3
"""
pcap_steal.py — mine captured traffic for (a) leaked flags and (b) the attacker
requests that leaked them. Incoming exploits against you are free exploits for you.

Prefers tshark (install wireshark/tshark). Falls back to a raw byte scan of the
pcap if tshark is missing (less precise but still finds flag strings + nearby URIs).

Usage:
  ./pcap_steal.py cap.pcap                 # list flags + the HTTP requests near them
  ./pcap_steal.py cap.pcap --flag 'LsCTF2026\\{[^}]+\\}'
  ./pcap_steal.py 'cap/*.pcap.gz'          # globs ok (quote them)

Capture with:  sudo tcpdump -i any -w cap/ad_%Y%m%d_%H%M%S.pcap -G 300 -z gzip
"""
import argparse, glob, gzip, re, shutil, subprocess, sys, collections

DEFAULT_FLAG = r'LsCTF2026\{[^}]{1,128}\}'   # finals format (override with --flag)

def tshark_available():
    return shutil.which("tshark") is not None

def via_tshark(path, flag_re):
    """Pull HTTP requests + responses, correlate flags to the request that caused them."""
    # request lines
    reqs = subprocess.run(
        ["tshark", "-r", path, "-Y", "http.request", "-T", "fields",
         "-e", "ip.dst", "-e", "tcp.stream", "-e", "http.request.method",
         "-e", "http.host", "-e", "http.request.uri"],
        capture_output=True, text=True).stdout
    stream_req = {}
    for line in reqs.splitlines():
        f = line.split('\t')
        if len(f) >= 5:
            dst, stream, method, host, uri = f[:5]
            stream_req[stream] = f"{method} http://{host}{uri}  (to {dst})"
    # response bodies / full data per stream
    resp = subprocess.run(
        ["tshark", "-r", path, "-Y", "http.response || http", "-T", "fields",
         "-e", "tcp.stream", "-e", "http.file_data"],
        capture_output=True, text=True).stdout
    rx = re.compile(flag_re)
    found = collections.defaultdict(set)   # stream -> flags
    for line in resp.splitlines():
        f = line.split('\t')
        if len(f) >= 2:
            stream, body = f[0], f[1]
            for m in rx.findall(body):
                found[stream].add(m)
    if not found:
        print("[tshark] no flags in HTTP bodies; trying raw scan too...")
        via_raw(path, flag_re)
        return
    print(f"=== {path}: flags correlated to the request that leaked them ===")
    for stream, flags in found.items():
        print(f"\n[stream {stream}] REQUEST: {stream_req.get(stream, '??? (non-HTTP or missing)')}")
        for fl in sorted(flags):
            print(f"    FLAG: {fl}")
    print("\n>>> Replay the REQUEST above against every target to farm this bug.")

def _read_bytes(path):
    op = gzip.open if path.endswith(".gz") else open
    with op(path, "rb") as f:
        return f.read()

def via_raw(path, flag_re):
    data = _read_bytes(path)
    rx = re.compile(flag_re.encode())
    uri = re.compile(rb'(GET|POST|PUT|DELETE)\s+(\S+)\s+HTTP')
    flags = sorted(set(m.decode('latin1') for m in rx.findall(data)))
    uris  = sorted(set(f"{m[0].decode()} {m[1].decode('latin1')}" for m in uri.findall(data)))
    print(f"=== {path} (raw scan) ===")
    print(f"[flags] {len(flags)} unique:")
    for fl in flags: print("   ", fl)
    if flags:
        print(f"[requests seen in capture — look for the one near a flag]:")
        for u in uris[:60]: print("   ", u)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pcap", help="pcap file or glob")
    ap.add_argument("--flag", default=DEFAULT_FLAG, help="flag regex")
    args = ap.parse_args()
    paths = glob.glob(args.pcap) or [args.pcap]
    for p in paths:
        if tshark_available() and not p.endswith(".gz"):
            via_tshark(p, args.flag)
        else:
            if p.endswith(".gz"):
                print(f"[i] {p} gzipped — raw scan (gunzip for tshark correlation)")
            via_raw(p, args.flag)

if __name__ == "__main__":
    main()
