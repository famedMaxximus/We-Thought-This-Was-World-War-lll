#!/usr/bin/env python3
"""Old Habits - carve the FTP passive-data transfer (site_backup.gz.b64) from the
pcap, base64-decode, gunzip. Needs tshark.
Usage: python3 solve.py [old-habits_capture.pcap]"""
import base64, gzip, subprocess, sys

pcap = sys.argv[1] if len(sys.argv) > 1 else "old-habits_capture.pcap"
run = lambda *a: subprocess.run(["tshark", "-r", pcap, *a], capture_output=True,
                                text=True, check=True).stdout
for line in run("-Y", "ftp", "-T", "fields", "-e", "ftp.request.command",
                "-e", "ftp.request.arg").splitlines():
    if line.split("\t")[0] in ("USER", "PASS", "RETR"):
        print("[*]", line.replace("\t", " "))
stream = run("-Y", "ftp-data", "-T", "fields", "-e", "tcp.stream").split()[0]
payload = run("-Y", f"tcp.stream=={stream} && tcp.len>0", "-T", "fields",
              "-e", "tcp.payload").split()
data = b"".join(bytes.fromhex(p.replace(":", "")) for p in payload)
print(gzip.decompress(base64.b64decode(data)).decode())
