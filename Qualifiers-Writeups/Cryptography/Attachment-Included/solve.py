#!/usr/bin/env python3
"""Attachment Included - reassemble the SMTP session, parse the MIME message,
decode the base64 attachment, then base64-decode its contents. Needs tshark.
Usage: python3 solve.py [attachment-included_capture.pcap]"""
import base64, email, subprocess, sys

pcap = sys.argv[1] if len(sys.argv) > 1 else "attachment-included_capture.pcap"
run = lambda *a: subprocess.run(["tshark", "-r", pcap, *a], capture_output=True,
                                text=True, check=True).stdout
stream = run("-Y", "smtp", "-T", "fields", "-e", "tcp.stream").split()[0]
payload = run("-Y", f"tcp.stream=={stream} && tcp.dstport==25 && tcp.len>0",
              "-T", "fields", "-e", "tcp.payload").split()
raw = b"".join(bytes.fromhex(p.replace(":", "")) for p in payload)
msg = email.message_from_bytes(raw.split(b"DATA\r\n", 1)[1])
for part in msg.walk():
    if part.get_content_disposition() == "attachment":
        inner = part.get_payload(decode=True)          # MIME base64 layer
        print("[*]", part.get_filename(), "->", inner.decode())
        print(base64.b64decode(inner).decode())         # second base64 layer
