# Phone Home

**Category:** Digital Forensics
**Difficulty:** Hard
**Points:** 500
**Status:** Unsolved (No verified flag)

---

## 1. Challenge Overview

An endpoint resolved a domain none of the tooling recognises, then POSTed a lump of "telemetry" to it. It has the shape of a malware beacon calling home. Mission: identify the command-and-control destination, reconstruct the data the beacon sent.

---

## 2. Initial Analysis

### Handout (`phone-home_capture.zip` → `phone-home_capture.pcap`)

PCAP capture of C2 beacon traffic.

### Objectives

1. Identify the command-and-control destination
2. Reconstruct the data the beacon sent
3. Submit the recovered value as the flag (format: `LsCTF2026{...}`)

---

## 3. Investigation and Methodology

### Wireshark Analysis

1. Open `phone-home_capture.pcap` in Wireshark
2. Look for DNS queries to unknown domains
3. Follow HTTP/HTTPS POST requests to suspicious domains
4. Analyze the POST body (telemetry data)

### Beacon Analysis

The telemetry data is likely encoded/encrypted. Common techniques:
- Base64 encoding
- XOR encryption
- Custom encoding
- AES encryption with embedded key

---

## 4. Current Status

**Unsolved.** The PCAP has not been fully analyzed in this repository.

---

## 5. Flag

**None recovered** — Challenge remains unsolved.

---

## 6. Evidence and References

- `evidence/phone-home_capture.pcap` — Network capture
- `evidence/extracted/phone-home_capture.pcap` — Extracted capture

---

## 4. Vulnerability / Technical Discovery

*Challenge not yet solved. Analysis pending.*

## 5. Exploitation / Solution

*Challenge not yet solved. Analysis pending.*

## 6. Flag

**Status: Unsolved** — No flag recovered yet.

## 7. Lessons Learned

*To be completed upon solving.*

## 8. Tools Used

*To be completed upon solving.*

## 9. Evidence and References

*To be completed upon solving.*

