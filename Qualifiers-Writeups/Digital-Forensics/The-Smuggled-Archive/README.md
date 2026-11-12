# The Smuggled Archive

**Category:** Digital Forensics
**Difficulty:** Hard
**Points:** 500
**Status:** Unsolved (No verified flag)

---

## 1. Challenge Overview

An operator pulled a zip of "staff export" off an internal box over HTTP. It was not supposed to leave the building. Mission: recover the archive from the capture and find the token inside it.

---

## 2. Initial Analysis

### Handout (`smuggled-archive_capture.zip` → `smuggled-archive_capture.pcap`)

PCAP capture of HTTP traffic containing an exfiltrated ZIP archive.

### Objectives

1. Carve the exfiltrated archive from HTTP traffic
2. Extract the ZIP
3. Find the file that matters
4. Submit the recovered flag (format: `LsCTF2026{...}`)

---

## 3. Investigation and Methodology

### Wireshark Analysis

1. Open `smuggled-archive_capture.pcap` in Wireshark
2. Follow HTTP streams
3. Look for ZIP file signatures (`PK\x03\x04`) in HTTP responses
4. Export the ZIP file (File → Export Objects → HTTP)

### Archive Extraction

Once carved, extract the ZIP and examine contents for the flag.

---

## 4. Current Status

**Unsolved.** The PCAP has not been fully analyzed in this repository. The challenge requires carving a ZIP from HTTP traffic and extracting the flag.

---

## 5. Flag

**None recovered** — Challenge remains unsolved.

---

## 6. Evidence and References

- `evidence/smuggled-archive_capture.pcap` — Network capture
- `evidence/analysis/zipout/` — Extracted ZIP contents (recovery.dat, staff.csv, README.txt)
- `evidence/analysis/httpobj/` — HTTP objects

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

