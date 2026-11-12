# The Rushed Login

**Category:** Digital Forensics / Network (HTTP Basic Auth)
**Status:** Solved (Verified)
**Flag:** `LsCTF2026{r3ad_th3_str3am_g3t_th3_cr3ds}` ✅ VERIFIED

---

## 1. Challenge Overview

> Maluti Microfinance runs its internal admin panel over plain HTTP "because it
> is only on the LAN". An administrator signed in first thing this morning, and
> the session was captured on the access switch.
>
> **Mission:** Read the login and recover the administrator's password.

---

## 2. Initial Analysis

### Handout (`rushed-login_capture.zip` → `rushed-login_capture.pcap`)

A standard Ethernet packet capture. List every HTTP request:

```
$ tshark -r rushed-login_capture.pcap -Y 'http.request' \
         -T fields -e frame.number -e http.request.method -e http.host -e http.request.uri
40   GET  www.microsoft.com        /generate_204
183  GET  www.ecocash.co.ls        /ncsi.txt
210  GET  www.google.com           /favicon.ico
215  GET  vodacom.co.ls            /gen_204
232  GET  intranet.maluti.local    /admin/dashboard   <-- the target
269  GET  outlook.office365.com     /generate_204
...
```

Most of the traffic is OS/browser connectivity-check noise (`generate_204`, `ncsi.txt`, favicons). The only request to the internal admin panel is frame **232**: `GET /admin/dashboard` on `intranet.maluti.local`.

---

## 3. Investigation and Methodology

### Find the request that carries the login

There is **no POST** in the capture. The admin panel doesn't use a login form. It uses **HTTP Basic Authentication**, where the browser sends the credentials in an `Authorization` header:

```
$ tshark -r rushed-login_capture.pcap -Y 'http.authorization' \
         -T fields -e frame.number -e http.host -e http.request.uri -e http.authorization
232  intranet.maluti.local  /admin/dashboard  Basic d2ViYWRtaW46VEhORFZFWXlNREkyZTNJ...
```

Frame 232, source `10.20.5.37` → `10.20.5.10:80`, carries the login.

### Pull the credentials out of the session

```
Authorization: Basic d2ViYWRtaW46VEhORFZFWXlNREkyZTNJellXUmZkR2d6WDNOMGNqTmhiVjluTTNSZmRHZ3pYMk55TTJSemZR
```

---

## 4. Vulnerability / Technical Discovery

HTTP Basic Auth is **not encryption**. The header is `base64("user:password")`, sent over plain HTTP. The password itself is a second base64 layer.

---

## 5. Exploitation / Solution

```
$ echo d2ViYWRtaW46VEhORFZFWXlNREkyZTNJel... | base64 -d
webadmin:THNDVEYyMDI2e3IzYWRfdGgzX3N0cjNhbV9nM3RfdGgzX2NyM2RzfQ
```

Username: `webadmin`
Password (still encoded): `THNDVEYyMDI2e3IzYWRfdGgzX3N0cjNhbV9nM3RfdGgzX2NyM2RzfQ`

The prefix `THNDVEYy...` decodes to `LsCTF2026...`:

```
$ echo THNDVEYyMDI2e3IzYWRfdGgzX3N0cjNhbV9nM3RfdGgzX2NyM2RzfQ | base64 -d
LsCTF2026{r3ad_th3_str3am_g3t_th3_cr3ds}
```

Both layers, end to end:

```
$ echo d2ViYWRtaW46VEhORFZFWXlNREkyZTNJellXUmZkR2d6WDNOMGNqTmhiVjluTTNSZmRHZ3pYMk55TTJSemZR \
    | base64 -d | cut -d: -f2 | base64 -d
LsCTF2026{r3ad_th3_str3am_g3t_th3_cr3ds}
```

`solve.py` does the same from the pcap:

```
$ python3 solve.py rushed-login_capture.pcap
[*] user: webadmin
FLAG: LsCTF2026{r3ad_th3_str3am_g3t_th3_cr3ds}
```

---

## 6. Flag

```
LsCTF2026{r3ad_th3_str3am_g3t_th3_cr3ds}
```
(Verified: `solve.py` reproduces it from the original pcap)

---

## 7. Lessons Learned

1. **HTTP Basic Auth over plain HTTP has no confidentiality.** The credentials travel in reversible base64, readable by anyone who can sniff the LAN (here, a mirror/SPAN port on the access switch).
2. **"It's only on the LAN" is not a security control.**
3. **Use HTTPS**, and prefer auth schemes that don't replay a reusable secret on every request.

---

## 8. Tools Used

- `tshark` (HTTP request and header extraction)
- `base64`
- Python 3: `base64`, `subprocess`

---

## 9. Evidence and References

- `solve.py` — Extracts the `Authorization` header and decodes both layers
- `evidence/README.md` — Original handout file list
