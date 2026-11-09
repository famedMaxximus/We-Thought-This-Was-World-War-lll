# Jeopardy — Strategy & Cheatsheet Index

> Finals jeopardy = the classic board you already crushed in quals. Flag format is almost
> certainly `LsCTF2026{...}`. This folder is your fast-reference so you solve on muscle memory.

## 1. Scoring strategy (how to win, not just solve)

- **Blood is temporary, points are forever** — but first-blood bonuses exist on some boards.
  Grab easy challenges fast to bank points and bonuses; don't open a 500pt rev while 50pt webs sit.
- **Sweep by value, then by your strengths.** Open every challenge's description first (2 min),
  tag each `easy / medium / hard / mine`, then attack easy+yours in parallel across the team.
- **Dynamic scoring:** if points decay as more teams solve, the *hard* challenges few can solve
  are worth the most late-game. Early: farm easy. Late: your edge is the unpopular hard ones.
- **Divide by category.** Assign each person their strongest 2 categories; don't dogpile.
- **Time-box 15 min.** No real progress → write a note, move on, return later. (Master prompt §8.)
- **Submit immediately**, keep a shared `flags.txt`, never sit on an unsubmitted flag.

## 2. First moves on ANY challenge

```bash
file suspicious_file          # what IS it, really
strings -n 8 file | less      # cheap wins hide here
binwalk file                  # embedded/nested files
xxd file | head               # magic bytes, structure
```
Then pick the matching cheatsheet below.

## 3. Cheatsheet index (in ./cheatsheets/)

| File | Covers |
|------|--------|
| `web.md` | SQLi, XSS, SSTI, LFI/RFI, SSRF, JWT, IDOR, deserialization, cookies, upload RCE. |
| `crypto.md` | RSA attacks, AES modes, XOR, classical, hashes, PRNG, encodings, sage/sympy snippets. |
| `forensics-stego.md` | pcap, disk/memory, file carving, images, audio, EXIF, LSB, archives, office docs. |
| `rev-pwn.md` | Ghidra/gdb workflow, common rev patterns, ret2win/ROP/ret2libc, format string, fmt pwntools template. |
| `osint-misc-network.md` | OSINT method, geolocation, metadata, misc/esoteric, encodings, QR, network/protocols. |

## 4. Helper scripts (in ./scripts/)

| Script | Use |
|--------|-----|
| `triage.sh <file>` | Kitchen-sink first-look: file/strings/binwalk/exif/entropy + category hints. |
| `pwn_template.py` | pwntools skeleton: local/remote switch, libc, ROP helpers, ready to fill. |
| `crypto_helpers.py` | RSA (factor/common-modulus/low-e/Wiener), XOR, base-N, hash-id helpers. |

## 5. Flag hygiene

- Confirm the exact format at kickoff; set it everywhere: `grep -ao 'LsCTF2026{[^}]*}'`.
- Watch for **rot/encoded flags**: a near-miss string may need `base64 -d`, `rev`, `rot13`.
- Submit exactly as recovered — case and punctuation matter.

## 6. Must-have tools (pre-install OFFLINE)

```
# general
file binwalk foremost exiftool steghide zsteg xxd hexedit sqlmap
# crypto
python3-pip  (pip: pycryptodome sympy gmpy2 requests pwntools)  sage (if space)
# rev/pwn
ghidra gdb (pwndbg/gef) radare2 pwntools ltrace strace one_gadget ropper checksec
# forensics/net
wireshark tshark volatility3 testdisk photorec stegsolve (jar) john hashcat
```
See each cheatsheet for exact invocations.
