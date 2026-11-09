# OSINT, Misc & Network Cheatsheet

# ──────────────── OSINT ────────────────
> Only public, challenge-relevant info. Corroborate; distinguish evidence from assumption.

## Method
1. Extract every identifier from the prompt/image: username, handle, email, name, place, device.
2. **Username pivot** across platforms: `sherlock <user>`, whatsmyname.app, namechk.
3. **Image geolocation**: landmarks, signs/language, road markings, vegetation, sun angle,
   license plates, architecture. Reverse image: Google Lens, Yandex (best for faces/places),
   TinEye. Check EXIF GPS first (`exiftool`).
4. **Metadata**: `exiftool` on any file; document authors, software, timestamps, GPS.
5. **People/handles**: social profiles, old posts, GitHub (commits, emails: `.patch` on a commit),
   Gravatar, data-breach checks (haveibeenpwned for context only).
6. **Places**: Google Maps/Street View, OpenStreetMap, Wikimapia; match the photo to a spot.
7. **Domains/infra**: `whois`, `dig`, crt.sh (subdomains via certs), Wayback Machine
   (web.archive.org — deleted pages!), Shodan/Censys for a given IP.
8. **Time**: shadow direction + date → suncalc.org for location/time reasoning.

## Handy
```bash
exiftool img.jpg
whois example.com ; dig +short example.com ANY ; dig TXT example.com
curl -s 'https://crt.sh/?q=%25.example.com&output=json' | jq -r '.[].name_value' | sort -u
# wayback:
curl -s 'http://web.archive.org/cdx/search/cdx?url=example.com*&output=text&fl=original' | sort -u
```
Google dorks: `site: inurl: intitle: filetype: "exact"` ; `github.com` + the handle.

# ──────────────── MISC / ESOTERIC ────────────────

## Encoding zoo (CyberChef "Magic" nails most)
- base64/32/85/58, hex, binary, octal, decimal, URL, HTML entities.
- **Esolangs**: Brainfuck (`+-><[].,`), Ook!, Malbolge, Whitespace (only space/tab/newline!),
  Piet (image), JSFuck (`[]()!+`). Run with online interpreters.
- Morse (`.-`), Bacon (AAAAB), tap code, Polybius, T9/phone keypad, semaphore, braille.
- **QR / barcodes**: `zbarimg img.png` ; broken QR → repair finder patterns, or `qrazybox`.
- Emoji/zero-width steg: zero-width chars (U+200B/C/D) hide data → `strings` won't show; use a
  zero-width decoder. Unicode confusables / tags (U+E00xx).

## Programming / jail / misc
- **Pyjail**: escape `eval`/restricted globals: `().__class__.__base__.__subclasses__()` →
  find `os`/`subprocess`; `breakpoint()`; `__import__('os').system('sh')`; builtins via
  `().__class__.__mro__`. Bypass char filters with getattr/chr/octal/unicode.
- **Bash jail**: `${PATH:0:1}` for `/`, wildcards, `$IFS` for spaces, `printf`, brace expansion.
- **Regex / math / "guess the number" services**: just script the interaction with pwntools/requests.
- Game/logic challenges: automate the protocol; read responses, respond programmatically.

# ──────────────── NETWORK / PROTOCOLS ────────────────

## Service interaction
```bash
nc host port                     # raw; read the banner, talk the protocol
ncat --ssl host port             # TLS service
curl -v ... ; openssl s_client -connect host:443   # inspect certs (flag in CN/SAN sometimes)
nmap -sV -sC -p- host            # (only authorized targets)
```

## Protocol analysis (see also forensics-stego pcap section)
- Weird custom TCP protocol → reverse the message format, script client with `pwntools` `remote()`.
- **DNS**: exfil in subdomain labels (join + base32/hex decode); TXT records; DNS tunneling.
- **ICMP**: data in ping payloads (`tshark -r x -Y icmp -T fields -e data`).
- **HTTP/2, MQTT, modbus, SMB, FTP, SNMP** — Wireshark dissects; follow streams; export objects.
- TLS with given key → Wireshark: set (Pre)-Master-Secret log / RSA key to decrypt.

## Scripting a service (template)
```python
from pwn import remote
r = remote('host', 1337)
print(r.recvline())
r.sendline(b'answer')
print(r.recvall(timeout=2))
```
