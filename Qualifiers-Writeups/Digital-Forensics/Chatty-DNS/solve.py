#!/usr/bin/env python3
"""Solver for "Chatty DNS" (LsCTF2026) — DNS exfiltration.

The suspicious lookups are subdomains of report.telemetry-sync.net of the form
    <index>.<base32-chunk>.report.telemetry-sync.net
Ordering by <index>, concatenating the base32 chunks, base32-decoding, then
base64-decoding recovers the flag.

Reads the chunks straight from the pcap via tshark (no manual copy/paste).
"""
import base64, subprocess, re, shutil, tempfile, os

PCAP = "chatty-dns_capture.pcap"
DOMAIN = "telemetry-sync.net"

# tshark drops privileges to a helper that may not be able to read files under
# arbitrary paths, so run it against a world-readable temp copy.
tmp = os.path.join(tempfile.gettempdir(), "chatty-dns_capture.pcap")
shutil.copy(PCAP, tmp)
os.chmod(tmp, 0o644)

out = subprocess.check_output(
    ["tshark", "-r", tmp,
     "-Y", f'dns.flags.response==0 && dns.qry.name contains "{DOMAIN}"',
     "-T", "fields", "-e", "dns.qry.name"],
    text=True,
)

# {index: chunk}, de-duplicated (DNS retransmits)
pieces = {}
for name in out.split():
    m = re.match(r"(\d+)\.([a-z0-9]+)\.report\." + re.escape(DOMAIN), name)
    if m:
        pieces[int(m.group(1))] = m.group(2)

b32 = "".join(pieces[i] for i in sorted(pieces)).upper()
b32 += "=" * ((-len(b32)) % 8)
inner = base64.b32decode(b32)          # -> a base64 string
flag = base64.b64decode(inner).decode()
print("FLAG:", flag)
