#!/usr/bin/env python3
"""The Rushed Login - pull the HTTP Basic Authorization header out of the pcap
and peel both base64 layers. Needs tshark.
Usage: python3 solve.py [rushed-login_capture.pcap]"""
import base64, subprocess, sys

pcap = sys.argv[1] if len(sys.argv) > 1 else "rushed-login_capture.pcap"
out = subprocess.run(["tshark", "-r", pcap, "-Y", "http.authorization",
                      "-T", "fields", "-e", "http.authorization"],
                     capture_output=True, text=True, check=True).stdout.split()
blob = out[out.index("Basic") + 1]
user, pw = base64.b64decode(blob).decode().split(":", 1)
print("[*] user:", user)
print("FLAG:", base64.b64decode(pw + "=" * (-len(pw) % 4)).decode())
