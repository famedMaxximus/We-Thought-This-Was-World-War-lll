# Forensics & Stego Cheatsheet

## Always start here
```bash
file X ; xxd X | head ; strings -n 6 X | grep -i -E 'flag|LsCTF|pass|key'
binwalk X            # embedded files?   binwalk -e X  to extract
foremost -i X -o out ; photorec X        # carve deleted/embedded files
exiftool X           # metadata/comments (flags hide in Comment/Artist/GPS)
```

## File signatures / repair
- Fix broken magic bytes: PNG `89 50 4E 47`, JPG `FF D8 FF`, PDF `%PDF`, ZIP `50 4B 03 04`,
  GIF `47 49 46 38`, ELF `7F 45 4C 46`. Edit with `hexedit`/`xxd`.
- PNG: check width/height in IHDR (image cropped to hide data → edit height). `pngcheck -v X`.
- Wrong extension? Trust `file`, rename.

## Images / stego
```bash
steghide extract -sf X.jpg            # (asks passphrase; try empty, strings from challenge)
zsteg X.png                           # LSB / BMP/PNG stego, try zsteg -a
stegsolve (java jar)                  # browse bit planes, XOR, channel combos
exiftool X                            # comments, thumbnails (exiftool -b -ThumbnailImage)
# LSB manual: extract least-significant bit of each channel, reassemble bytes
outguess -r X.jpg out.txt             # another jpg stego tool
```
Try passwords from the challenge text/filename with steghide. Check for appended data after
image EOF (`binwalk`, or look past `FF D9` in jpg / `IEND` in png).

## Audio
- Spectrogram often hides text: Audacity / Sonic Visualiser → spectrogram view.
- DTMF tones → decode dial tones. Morse in a tone → decode. SSTV → `qsstv`.
- `sox X.wav -n stat` ; check stereo channel diff; LSB in WAV samples.

## Archives / passwords
```bash
unzip -l X.zip ; 7z l X.7z
zip2john X.zip > h ; john h --wordlist=rockyou.txt      # cracked pw
# known-plaintext ZIP (ZipCrypto): bkcrack  (if you know a contained file's bytes)
for pw in $(cat rockyou.txt); do unzip -P "$pw" X.zip 2>/dev/null && break; done
```

## PCAP / network forensics
```bash
tshark -r X.pcap -q -z io,phs            # protocol hierarchy — what's in it
tshark -r X.pcap -Y http.request -T fields -e http.host -e http.request.uri
tshark -r X.pcap --export-objects http,out/    # dump transferred files
# Wireshark: Follow TCP/HTTP Stream; File>Export Objects; search packet bytes for 'flag'
strings X.pcap | grep -i flag
# USB keyboard HID: extract usb.capdata, map HID codes -> keystrokes (known script)
# DNS exfil: concat subdomain labels, base32/hex decode
```

## Disk / memory
```bash
# disk image:
mmls X.img ; fls -r X.img ; icat X.img INODE     (sleuthkit) ; autopsy for GUI
testdisk / photorec for recovery ; mount -o ro,loop X.img /mnt
# memory (volatility3):
vol -f mem.raw windows.info
vol -f mem.raw windows.pslist | grep -i notepad
vol -f mem.raw windows.cmdline ; windows.filescan ; windows.dumpfiles --virtaddr ADDR
vol -f mem.raw windows.hashdump    (then crack)
```

## Office / PDF / misc docs
```bash
oletools: olevba doc.docm            # macros (often the payload/flag)
pdf: pdf-parser.py , pdfdetach , strings; hidden layers/objects/JS
qpdf --decrypt in.pdf out.pdf        # remove owner password
# git repo given? git log --all ; git show each commit ; check deleted files & stash
```

## Mental checklist
- [ ] `file` + `strings` + `exiftool` + `binwalk`
- [ ] Appended data after EOF?  Nested archives?
- [ ] Image: LSB (zsteg), steghide (try pws), bit planes (stegsolve), cropped height
- [ ] Audio: spectrogram, morse, DTMF
- [ ] PCAP: export objects, follow streams, odd protocols/DNS/USB
- [ ] Archive: crack with john; ZipCrypto → bkcrack
