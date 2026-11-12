# Museum Piece

**Category:** Digital Forensics / Network (Telnet)
**Status:** Solved (Verified)
**Flag:** `LsCTF2026{telnet_museum_p13c3}` ✅ VERIFIED

---

## 1. Challenge Overview

> The core router is still administered over **Telnet** in 2026. A maintenance
> session was captured while an operator was working on it.
>
> **Mission:** Read the session and recover the token the operator pulled up,
> then restore it to its original value.

---

## 2. Initial Analysis

### Handout (`museum-piece_capture.zip` → `museum-piece_capture.pcap`)

```
$ tshark -r museum-piece_capture.pcap -q -z io,phs
  ... tcp ... tls ... http ... telnet frames:10 ... dns ... ntp ...
```

There is a **Telnet** conversation. Telnet is plaintext, so the whole session is readable.

---

## 3. Investigation and Methodology

### Follow the Telnet session

```
$ tshark -r museum-piece_capture.pcap -Y telnet -T fields -e tcp.stream | sort -u
13
$ tshark -r museum-piece_capture.pcap -q -z follow,tcp,ascii,13
Node 0: 10.30.0.55:51234
Node 1: 10.30.0.1:23

MikroTik RouterOS 6.48
core-rtr login: admin
Password: Str0ngR0uterP@ss
[admin@core-rtr] > cat /tmp/token.txt
# stored backwards on purpose
9NzYzEDcf1WdlNXdt9Fdl5GblR3e2IDMyYEVDNHT
[admin@core-rtr] > /quit
```

The operator logs into a MikroTik core router (`admin` / `Str0ngR0uterP@ss`) and prints `/tmp/token.txt`. The file says the token is **stored backwards on purpose**:

```
9NzYzEDcf1WdlNXdt9Fdl5GblR3e2IDMyYEVDNHT
```

---

## 4. Vulnerability / Technical Discovery

| Component | Flaw |
|-----------|------|
| Router management | Telnet: credentials and session output in cleartext |
| Token storage | Reversed string + Base64, obfuscation only |

---

## 5. Exploitation / Solution

Reverse the string, then Base64-decode it:

```
$ python3 -c "import base64;print(base64.b64decode('9NzYzEDcf1WdlNXdt9Fdl5GblR3e2IDMyYEVDNHT'[::-1]))"
reversed = THNDVEYyMDI2e3RlbG5ldF9tdXNldW1fcDEzYzN9
b64      = LsCTF2026{telnet_museum_p13c3}
```

`solve.py` does the same straight from the pcap:

```
$ python3 solve.py museum-piece_capture.pcap
FLAG: LsCTF2026{telnet_museum_p13c3}
```

---

## 6. Flag

```
LsCTF2026{telnet_museum_p13c3}
```
(Verified: `solve.py` reproduces it from the original pcap)

---

## 7. Lessons Learned

1. **Telnet sends everything in cleartext.** One capture gives away the router login *and* the token.
2. **"Stored backwards" plus Base64 is not encryption.** Reverse, decode, done.
3. **Use SSH** for device administration.

---

## 8. Tools Used

- `tshark` (protocol hierarchy, TCP stream follow)
- Python 3: `base64`

---

## 9. Evidence and References

- `solve.py` — Finds the Telnet stream, extracts the token, reverses and decodes it
- `evidence/README.md` — Original handout file list

> Note: on the solving host, `tshark` drops privileges and could not read files under the home directory. Run the solver against a copy of the pcap in a world-readable path (e.g. `/tmp`) if you get a permission error.
