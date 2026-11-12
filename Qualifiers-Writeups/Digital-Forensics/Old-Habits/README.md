# Old Habits

**Category:** Digital Forensics / Network (FTP)
**Status:** Solved (Verified)
**Flag:** `LsCTF2026{ftp_st1ll_l3aks_1n_2026}` ✅ VERIFIED

---

## 1. Challenge Overview

> An FTP server that was supposed to be decommissioned is still answering.
> Someone logged in and pulled a backup file down off it.
>
> **Mission:** Recover the file that was downloaded and read what is inside.

---

## 2. Initial Analysis

### Handout (`old-habits_capture.zip` → `old-habits_capture.pcap`)

```
$ tshark -r old-habits_capture.pcap -q -z io,phs
... tcp ... ftp (13 frames) ... ftp-data (1 frame) ...
```

The protocol hierarchy shows **FTP** control traffic plus a single **ftp-data** transfer. FTP is plaintext, so both the login and the file cross the wire in the clear ("old habits").

---

## 3. Investigation and Methodology

### Confirm which login succeeded

Dump the FTP control channel:

```
$ tshark -r old-habits_capture.pcap -Y ftp \
         -T fields -e frame.number -e ip.src -e ftp.request.command \
         -e ftp.request.arg -e ftp.response.code -e ftp.response.arg
142  172.16.8.20                       220  (vsFTPd 3.0.3)
150  172.16.8.133  USER  backup
156  172.16.8.20                       331  Please specify the password.
169  172.16.8.133  PASS  Autumn2026!
185  172.16.8.20                       230  Login successful.      <-- success
211  172.16.8.133  TYPE  I                                        (binary)
226  172.16.8.133  PASV
241  172.16.8.20                       227  Entering Passive Mode (172,16,8,20,195,80).
256  172.16.8.133  RETR  site_backup.gz.b64                       <-- the download
261  172.16.8.20                       150  Opening BINARY mode data connection...
263  172.16.8.133  QUIT
```

- Server: `vsFTPd 3.0.3` at `172.16.8.20`; client `172.16.8.133`.
- The successful login (response **230**) is `backup` / `Autumn2026!`.
- Transfer mode is **binary** (`TYPE I`); passive data port = `195*256 + 80 = 50000`.
- The file pulled is **`site_backup.gz.b64`** via `RETR`.

### Locate the file transfer

The passive data connection is the lone `ftp-data` frame (TCP stream 19):

```
$ tshark -r old-habits_capture.pcap -Y ftp-data \
         -T fields -e frame.number -e ip.src -e ip.dst -e tcp.stream
283  172.16.8.20  172.16.8.133  19
```

Server → client on port 50000, as the PASV reply advertised.

---

## 4. Vulnerability / Technical Discovery

FTP authenticates and transfers in cleartext. The downloaded file is wrapped in gzip and then base64, which is encoding, not protection.

---

## 5. Exploitation / Solution

Follow the data stream and pull out the server's payload:

```
$ tshark -r old-habits_capture.pcap -q -z follow,tcp,raw,19
...
H4sIALYezmoC/0tKTM4uLVDITczLTEstLuEqAhL5RakK2amVVgo+xc4hbkYG...
```

The filename `.gz.b64` means a gzip that was then base64-encoded. The payload begins `H4sI`, which is base64 for the gzip magic `1f 8b 08`. Two decodes recover the original:

```
$ base64 -d site_backup.gz.b64 > site_backup.gz
$ file site_backup.gz
site_backup.gz: gzip compressed data, max compression, original size 64

$ gunzip -c site_backup.gz
backup manifest
restore key: LsCTF2026{ftp_st1ll_l3aks_1n_2026}
```

`solve.py` does the whole chain from the pcap:

```
$ python3 solve.py old-habits_capture.pcap
[*] USER backup
[*] PASS Autumn2026!
[*] RETR site_backup.gz.b64
backup manifest
restore key: LsCTF2026{ftp_st1ll_l3aks_1n_2026}
```

---

## 6. Flag

```
LsCTF2026{ftp_st1ll_l3aks_1n_2026}
```
(Verified: `solve.py` reproduces it from the original pcap)

---

## 7. Lessons Learned

1. **FTP leaks everything.** A single SPAN/mirror capture gives an attacker the working credentials (`backup:Autumn2026!`) and the full file.
2. **`.b64` / `.gz` wrapping is encoding.** It comes off with two standard commands.
3. **Decommission legacy FTP for real**, or replace it with FTPS/SFTP.

---

## 8. Tools Used

- `tshark` (FTP control parsing, stream follow)
- `base64`, `gunzip`
- Python 3: `base64`, `gzip`, `subprocess`

---

## 9. Evidence and References

- `solve.py` — Prints the FTP login and RETR, carves the ftp-data payload, decodes it
- `evidence/README.md` — Original handout file list and intermediate artifacts
