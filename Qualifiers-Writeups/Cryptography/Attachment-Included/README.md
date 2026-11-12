# Attachment Included

**Category:** Cryptography / Digital Forensics (SMTP / email)
**Difficulty:** Intermediate
**Points:** 300
**Status:** Solved (Verified)
**Flag:** `LsCTF2026{ch3ck_th3_attachm3nt}` ✅ VERIFIED

---

## 1. Challenge Overview

An insider emailed "figures" to a personal Gmail over plain SMTP. The body of the message is small talk. The attachment is the actual leak. Follow the SMTP session, extract the attachment, and decode it.

---

## 2. Initial Analysis

### Handout (`attachment-included_capture.zip` → `attachment-included_capture.pcap`)

```
$ tshark -r attachment-included_capture.pcap -q -z io,phs
... smtp (13 frames) ... imf (1 frame) ...
```

Plain **SMTP** (port 25, cleartext). One mail session carries the leak.

### Objectives

1. Follow the SMTP session and read the message
2. Extract the attachment
3. Decode it back to plaintext

---

## 3. Investigation and Methodology

### Follow the SMTP session

```
$ tshark -r attachment-included_capture.pcap -Y smtp -T fields -e tcp.stream   # -> stream 16
$ tshark -r attachment-included_capture.pcap -q -z follow,tcp,ascii,16
```

The session (sender `10.5.9.23` → mail server `196.30.20.9:25`):

```
EHLO wks-fin-07
MAIL FROM:<t.mokoena@maluti.co.ls>
RCPT TO:<personal.backup@gmail.com>
DATA
From: t.mokoena@maluti.co.ls
To: personal.backup@gmail.com
Subject: figures
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="==_Maluti_7731_=="

--==_Maluti_7731_==
Content-Type: text/plain

As promised. Everything is in the attached file.          <-- small talk

--==_Maluti_7731_==
Content-Type: text/plain; name="codes.txt"
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename="codes.txt"

WVdOalpYTnpJR052WkdVNklFeHpRMVJHTWpBeU5udGphRE5qYTE5MGFETmZZWFIwWVdOb2JU
TnVkSDA9

--==_Maluti_7731_==--
.
QUIT
```

A `multipart/mixed` MIME message: the body is harmless small talk, and the payload is the base64 attachment `codes.txt`.

In Wireshark the same attachment can be saved via **File → Export Objects → IMF**.

---

## 4. Vulnerability / Technical Discovery

| Component | Flaw |
|-----------|------|
| SMTP | Plaintext (no TLS): headers, body and attachments visible on the wire |
| Email attachment | MIME base64 transport encoding, then a second base64 layer; no encryption |

---

## 5. Exploitation / Solution

The attachment is MIME base64 (`Content-Transfer-Encoding: base64`). Decoding it once yields **another** base64 string, which decodes to the plaintext:

```
$ echo 'WVdOalpYTnpJR052WkdVNklFeHpRMVJHTWpBeU5udGphRE5qYTE5MGFETmZZWFIwWVdOb2JUTnVkSDA9' | base64 -d
YWNjZXNzIGNvZGU6IExzQ1RGMjAyNntjaDNja190aDNfYXR0YWNobTNudH0=

$ echo 'YWNjZXNzIGNvZGU6IExzQ1RGMjAyNntjaDNja190aDNfYXR0YWNobTNudH0=' | base64 -d
access code: LsCTF2026{ch3ck_th3_attachm3nt}
```

`solve.py` reassembles the client side of the SMTP stream, parses it with Python's `email` module and decodes both layers:

```
$ python3 solve.py attachment-included_capture.pcap
[*] codes.txt -> YWNjZXNzIGNvZGU6IExzQ1RGMjAyNntjaDNja190aDNfYXR0YWNobTNudH0=
access code: LsCTF2026{ch3ck_th3_attachm3nt}
```

---

## 6. Flag

```
LsCTF2026{ch3ck_th3_attachm3nt}
```
(Verified: `solve.py` reproduces it from the original pcap)

---

## 7. Lessons Learned

1. **SMTP without TLS sends everything in the clear.** Anyone capturing the session reads the attachment.
2. **MIME base64 is a transport encoding, not encryption.** Here it took two decodes.
3. **The innocuous body is misdirection.** The leak was in the file.
4. **Defences:** enforce STARTTLS / submission over TLS, and use DLP to flag attachments leaving for personal webmail.

---

## 8. Tools Used

- Wireshark / `tshark` (SMTP stream follow, IMF export)
- `base64 -d`
- Python 3: `email`, `base64`, `subprocess`

---

## 9. Evidence and References

- `solve.py` — Extracts the SMTP message from the pcap and decodes the attachment
- `evidence/README.md` — Original handout file list and recovered attachment
