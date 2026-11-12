#!/usr/bin/env python3
"""Museum Piece — LsCTF2026. Pull the token from the cleartext Telnet session and restore it."""
import base64, subprocess, sys, re
pcap = sys.argv[1] if len(sys.argv) > 1 else "museum-piece_capture.pcap"
# find the telnet stream and follow it
streams = subprocess.run(["tshark","-r",pcap,"-Y","telnet","-T","fields","-e","tcp.stream"],
                         capture_output=True,text=True).stdout.split()
s = sorted(set(streams))[0]
sess = subprocess.run(["tshark","-r",pcap,"-q","-z",f"follow,tcp,ascii,{s}"],
                      capture_output=True,text=True).stdout
# the token line is the base64-looking string after the "stored backwards" comment
m = re.search(r"backwards on purpose\s*\n([A-Za-z0-9+/=]+)", sess)
token = m.group(1)
print("captured (backwards):", token)
flag = base64.b64decode(token[::-1] + "===").decode()
print("FLAG:", flag)
