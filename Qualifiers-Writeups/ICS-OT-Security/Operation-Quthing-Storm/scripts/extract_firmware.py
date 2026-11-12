#!/usr/bin/env python3
"""Unpack wh097_firmware.bin and list every flag-shaped / base64 string in the rootfs blob.

The uImage header (64 B, fake CRCs DEADBEEF/CAFEF00D) claims gzip, but the payload
is raw zlib streams: the packed rootfs at offset 672, a directory index at 7782.
Usage: python3 extract_firmware.py wh097_firmware.bin
"""
import base64, re, sys, zlib

fw = open(sys.argv[1], "rb").read()
rootfs = zlib.decompressobj().decompress(fw[672:])
index = zlib.decompressobj().decompress(fw[7782:])
open("rootfs.raw", "wb").write(rootfs)
print(f"rootfs {len(rootfs)} bytes, index {len(index)} bytes")

flags = set(re.findall(rb"LsCTF2026\{[^}]*\}", rootfs))
for b64 in re.findall(rb"[A-Za-z0-9+/]{40,}={0,2}", rootfs):
    try:
        flags.update(re.findall(rb"LsCTF2026\{[^}]*\}", base64.b64decode(b64)))
    except Exception:
        pass
for f in sorted(flags):
    print(f.decode())
