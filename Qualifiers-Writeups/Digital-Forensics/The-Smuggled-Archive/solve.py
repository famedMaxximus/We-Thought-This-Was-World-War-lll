#!/usr/bin/env python3
"""The Smuggled Archive - carve export.zip out of the pcap and decode the token.

The 481-byte zip rides in a single HTTP response segment (GET /backup/export.zip,
10.7.7.30 -> 10.7.7.80), so it can be carved straight from the raw capture bytes:
local-file-header magic PK\\x03\\x04 up to the end-of-central-directory record (+22 bytes).
"""
import base64, io, sys, zipfile

data = open(sys.argv[1] if len(sys.argv) > 1 else "smuggled-archive_capture.pcap", "rb").read()
start = data.index(b"PK\x03\x04")
eocd = data.index(b"PK\x05\x06", start)
blob = data[start:eocd + 22]
with zipfile.ZipFile(io.BytesIO(blob)) as z:
    print("[*] archive members:", z.namelist())
    rec = z.read("recovery.dat").strip()
print("[*] recovery.dat:", rec.decode())
print("[+] flag:", base64.b64decode(rec).decode()[::-1])
