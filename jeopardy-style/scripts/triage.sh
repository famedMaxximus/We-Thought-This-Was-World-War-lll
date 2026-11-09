#!/usr/bin/env bash
# triage.sh — kitchen-sink first look at any challenge file. Runs the cheap wins
# automatically and prints category hints so you know which cheatsheet to open.
#
#   ./triage.sh suspicious_file          # (optionally set FLAG=regex)
#
FLAG="${FLAG:-LsCTF2026\{[^}]{1,128}\}}"
F="${1:?usage: triage.sh <file>}"
have(){ command -v "$1" >/dev/null 2>&1; }
hdr(){ printf '\n\033[1;36m==== %s ====\033[0m\n' "$*"; }

hdr "file type";            file "$F"
hdr "size / hexdump head";  ls -l "$F"; xxd "$F" | head -6
hdr "flag-ish strings";     strings -n 6 "$F" | grep -aoE "$FLAG" | sort -u | head
hdr "interesting strings";  strings -n 6 "$F" | grep -aiE 'flag|pass|secret|key|LsCTF|BEGIN|http' | head -30

if have exiftool; then hdr "exiftool (metadata)"; exiftool "$F" | grep -viE '^(ExifTool|File (Perm|Inode|Block))'; fi
if have binwalk;  then hdr "binwalk (embedded)";  binwalk "$F" | head -40; fi

hdr "entropy hint"
python3 - "$F" <<'PY' 2>/dev/null
import sys,math,collections
d=open(sys.argv[1],'rb').read() or b'\0'
c=collections.Counter(d); n=len(d)
H=-sum(v/n*math.log2(v/n) for v in c.values())
print(f"  Shannon entropy: {H:.2f}/8   "+(
  "-> looks ENCRYPTED/COMPRESSED/packed" if H>7.5 else
  "-> looks like text/structured data" if H<5 else "-> mixed"))
PY

# category hint
hdr "category hint"
T=$(file -b "$F")
case "$T" in
  *ELF*)            echo "  -> REVERSE/PWN: open cheatsheets/rev-pwn.md (checksec, ghidra, gdb)";;
  *PNG*|*JPEG*|*GIF*|*bitmap*) echo "  -> STEGO: cheatsheets/forensics-stego.md (zsteg/steghide/stegsolve/exiftool)";;
  *pcap*|*capture*) echo "  -> NETWORK FORENSICS: tshark/wireshark (forensics-stego.md pcap section)";;
  *Zip*|*7-zip*|*gzip*|*tar*|*RAR*) echo "  -> ARCHIVE: unzip/7z; crack with zip2john (forensics-stego.md)";;
  *PDF*)            echo "  -> DOC FORENSICS: pdf-parser/pdfdetach/qpdf (forensics-stego.md)";;
  *ASCII*|*text*|*Unicode*) echo "  -> CRYPTO/ENCODING or MISC: crypto.md / osint-misc-network.md (try CyberChef Magic)";;
  *data*)           echo "  -> UNKNOWN: fix magic bytes? carve with binwalk -e / foremost. Maybe crypto blob.";;
  *)                echo "  -> inspect manually; see jeopardy-style/readme.md";;
esac
echo
echo "next: binwalk -e '$F'   |   foremost -i '$F' -o carve/   |   open the matching cheatsheet"
