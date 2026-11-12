# The Smuggled Archive

**Category:** Digital Forensics / Network (HTTP file carving)
**Difficulty:** Hard
**Points:** 500
**Status:** Solved (Verified)
**Flag:** `LsCTF2026{z1pp3d_but_n0t_h1dd3n}` ✅ VERIFIED

---

## 1. Challenge Overview

An operator pulled a zip of "staff export" off an internal box over HTTP. It was not supposed to leave the building. Mission: recover the archive from the capture and find the token inside it.

---

## 2. Initial Analysis

### Handout (`smuggled-archive_capture.zip` → `smuggled-archive_capture.pcap`)

The capture is mostly noise: a lot of TLS on port 443 and many tiny HTTP connectivity checks (`/ncsi.txt`, `/gen_204`, `/generate_204`, `/favicon.ico`), each with a 2-byte body.

### Objectives

1. Carve the exfiltrated archive from HTTP traffic
2. Extract the ZIP
3. Find the file that matters
4. Recover the flag (format: `LsCTF2026{...}`)

---

## 3. Investigation and Methodology

### Find the transfer

Listing the HTTP requests turns up one that doesn't fit. It is also the only one whose server is on the internal network:

```
tshark -r smuggled-archive_capture.pcap -Y http.request \
  -T fields -e ip.src -e ip.dst -e http.request.method -e http.request.uri
...
10.7.7.30   10.7.7.80   GET   /backup/export.zip
```

### Extract the archive

In Wireshark use **File → Export Objects → HTTP** and save `export.zip`. With tshark:

```
tshark -r smuggled-archive_capture.pcap --export-objects http,out/
```

`export.zip` is 481 bytes, has no password, and holds:

| File | Contents |
|---|---|
| `README.txt` | "Exfiltrated staff export. The token lives in recovery.dat (not here)." |
| `staff.csv` | Decoy: two staff rows (M. Letsie / Finance, T. Nkoe / Security) |
| `recovery.dat` | `fW4zZGQxaF90MG5fdHViX2QzcHAxens2MjAyRlRDc0w=` |

---

## 4. Vulnerability / Technical Discovery

| Component | Flaw |
|-----------|------|
| Transfer | Plain HTTP: the whole file can be rebuilt from a capture |
| Archive | No password / encryption |
| Token | Base64 of the reversed flag, encoding only |

---

## 5. Exploitation / Solution

`recovery.dat` is Base64. Decoding it gives `}n3dd1h_t0n_tub_d3pp1z{6202FTCsL`, the flag written backwards. Reversing it gives the flag:

```
echo fW4zZGQxaF90MG5fdHViX2QzcHAxens2MjAyRlRDc0w= | base64 -d | rev
LsCTF2026{z1pp3d_but_n0t_h1dd3n}
```

`solve.py` uses only the Python standard library. The whole zip sits in one TCP segment, so the script cuts it straight out of the raw pcap: from the `PK\x03\x04` local-file header to the end-of-central-directory record (`PK\x05\x06`) plus 22 bytes. It then opens the zip in memory and decodes `recovery.dat`.

```
$ python3 solve.py
[*] archive members: ['README.txt', 'staff.csv', 'recovery.dat']
[*] recovery.dat: fW4zZGQxaF90MG5fdHViX2QzcHAxens2MjAyRlRDc0w=
[+] flag: LsCTF2026{z1pp3d_but_n0t_h1dd3n}
```

---

## 6. Flag

```
LsCTF2026{z1pp3d_but_n0t_h1dd3n}
```
(Verified: `solve.py` reproduces it from the original pcap)

---

## 7. Lessons Learned

1. **Anything sent over plain HTTP can be rebuilt in full** from a packet capture.
2. **"Export Objects" turns a pcap into files in one click.**
3. **Base64 plus string reversal is encoding, not protection.**
4. **Read the decoy notes.** `README.txt` points straight at `recovery.dat`; `staff.csv` is filler.

---

## 8. Tools Used

- Wireshark / `tshark` (HTTP request listing, Export Objects)
- `base64`, `rev`
- Python 3 stdlib: `zipfile`, `io`, `base64`

---

## 9. Evidence and References

- `solve.py` — Carves `export.zip` from the raw pcap and decodes the token
- `evidence/README.md` — Original handout file list and carved archive members
