# Vault Description: Attachment Included

**Category:** Cryptography / Digital Forensics
**Difficulty:** Intermediate
**Points:** 300
**Status:** Solved (Verified)

---

## 1. Challenge Overview

An insider emailed "figures" to a personal Gmail over plain SMTP. The body of the message is small talk. The attachment is the actual leak. Recover the contents of the attachment.

---

## 2. Initial Analysis

### Handout (`attachment-included_capture.zip` → `attachment-included_capture.pcap`)

PCAP capture of an SMTP session.

### Objectives

1. Follow the SMTP session and read the message
2. Extract the attachment
3. Decode it back to plaintext

---

## 3. Investigation and Methodology

### SMTP Session Analysis

Open `attachment-included_capture.pcap` in Wireshark. Follow the TCP stream (port 25).

The email contains:
- Plain text body (small talk)
- An attachment (the leak)

### Attachment Extraction

1. In Wireshark: File → Export Objects → SMTP
2. Save the attachment
3. The attachment is base64-encoded (standard email encoding)

### Decoding

Decode the base64 attachment to recover the plaintext leak.

---

## 4. Vulnerability / Technical Discovery

| Component | Flaw |
|-----------|------|
| SMTP | Plaintext (no TLS) — credentials and content visible on wire |
| Email attachment | Base64 encoding only (no encryption) |

---

## 5. Exploitation / Solution

```bash
# 1. Open PCAP in Wireshark
wireshark attachment-included_capture.pcap

# 2. Follow TCP stream (port 25) → see email with attachment
# 3. Export Objects → SMTP → save attachment
# 4. Decode base64
base64 -d attachment.b64 > attachment.txt
cat attachment.txt
```

Or programmatically:
```python
import email, base64

with open('attachment-included_capture.pcap', 'rb') as f:
    # Parse PCAP, extract SMTP payload
    # Simplified: use scapy or manual extraction
    msg = email.message_from_bytes(smtp_data)
    for part in msg.walk():
        if part.get_content_disposition() == 'attachment':
            payload = part.get_payload(decode=True)  # auto base64 decode
            print(payload.decode())
```

---

## 6. Flag

```
LsCTF2026{ch3ck_th3_attachm3nt}
```
(Verified by successful attachment extraction and decoding)

---

## 7. Lessons Learned

1. **Plain SMTP is fully visible** — No encryption means anyone on the network path sees everything.
2. **Attachments are just encoded** — Base64 is encoding, not encryption. `decode=True` in Python's `email` module handles it automatically.
3. **Wireshark SMTP object export** — Built-in feature makes attachment extraction trivial.
4. **Insider threat via email** — Data exfiltration over standard protocols leaves clear forensic traces.

---

## 8. Tools Used

- Wireshark (PCAP analysis, SMTP object export)
- Python 3: `email`, `base64` (programmatic extraction)
- `base64 -d` (command line)

---

## 9. Evidence and References

- `evidence/attachment-included_capture.pcap` — SMTP capture
- `evidence/attachment.b64` — Extracted base64 attachment
- `evidence/attachment.txt` — Decoded plaintext