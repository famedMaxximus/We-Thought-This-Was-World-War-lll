#!/usr/bin/env python3
"""Who's the Gateway — LsCTF2026 solver.
Finds the ARP spoofer and decodes the credential exposed by the redirect.
Usage: python3 solve.py whos-the-gateway_capture.pcap
"""
import base64, subprocess, sys, collections

pcap = sys.argv[1] if len(sys.argv) > 1 else "whos-the-gateway_capture.pcap"

def tshark(args):
    return subprocess.run(["tshark", "-r", pcap] + args,
                          capture_output=True, text=True).stdout

# 1) ARP anomaly: which IP is claimed by more than one MAC?
rows = tshark(["-Y", "arp.opcode==2", "-T", "fields",
               "-e", "arp.src.proto_ipv4", "-e", "arp.src.hw_mac"]).split("\n")
claims = collections.defaultdict(collections.Counter)
for r in rows:
    if "\t" in r:
        ip, mac = r.split("\t")
        claims[ip][mac] += 1
print("[*] ARP replies per IP:")
for ip, macs in claims.items():
    for mac, n in macs.most_common():
        tag = "  <-- SPOOFER" if len(macs) > 1 and n == max(macs.values()) else ""
        print(f"    {ip:16} {mac}  x{n}{tag}")

# 2) credential exposed via HTTP Basic auth
auth = tshark(["-Y", "http.authorization", "-T", "fields",
               "-e", "http.authorization"]).strip().split()[-1]
cred = base64.b64decode(auth).decode()
user, hexpart = cred.split(":", 1)
flag = bytes.fromhex(hexpart).decode()
print(f"\n[*] Basic auth user: {user}")
print(f"[+] FLAG: {flag}")
