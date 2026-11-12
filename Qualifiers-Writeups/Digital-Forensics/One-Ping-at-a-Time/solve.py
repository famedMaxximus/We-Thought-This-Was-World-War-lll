#!/usr/bin/env python3
"""Solver for "One Ping at a Time" (LsCTF2026) — ICMP covert channel.

A ping sweep across 10.13.37.0/24 is cover traffic (32-byte payloads, varying
idents). One host, 10.13.37.7, is pinged with a fixed ident 16962 (0x4242) and
tiny 2-byte payloads, sequence-numbered. Ordering those payloads by icmp.seq and
concatenating gives an ASCII-hex string -> un-hex -> base64 -> the flag.
"""
import base64, subprocess, shutil, tempfile, os

PCAP = "one-ping-at-a-time_capture.pcap"
# tshark's privilege-drop helper may not read arbitrary paths; use a temp copy.
tmp = os.path.join(tempfile.gettempdir(), "one-ping.pcap")
shutil.copy(PCAP, tmp); os.chmod(tmp, 0o644)

out = subprocess.check_output(
    ["tshark", "-r", tmp,
     "-Y", "icmp.type==8 && icmp.ident==16962",
     "-T", "fields", "-e", "icmp.seq", "-e", "data.data"],
    text=True,
)

pairs = []
for line in out.splitlines():
    f = line.split()
    if len(f) >= 2:
        pairs.append((int(f[0]), bytes.fromhex(f[1].replace(":", ""))))
pairs.sort()

hex_ascii = b"".join(b for _, b in pairs).decode()   # the 2-byte payloads spell ASCII hex
b64 = bytes.fromhex(hex_ascii).decode()              # -> base64 text
flag = base64.b64decode(b64).decode()
print("FLAG:", flag)
