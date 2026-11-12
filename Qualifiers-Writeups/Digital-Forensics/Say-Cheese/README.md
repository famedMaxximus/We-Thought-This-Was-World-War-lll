# Say Cheese

**Category:** Digital Forensics
**Difficulty:** Hard
**Points:** 500
**Status:** Unsolved (No verified flag)

---

## 1. Challenge Overview

A staff access badge was served off the portal CDN over HTTP. The image came through, but it is not quite right. Mission: recover the badge image and read what is printed on it.

---

## 2. Initial Analysis

### Handout (`say-cheese_capture.zip` → `say-cheese_capture.pcap`)

PCAP capture of HTTP traffic containing a badge image.

### Objectives

1. Carve the image out of the capture
2. Read what is printed on the badge
3. Submit the recovered flag (format: `LsCTF2026{...}`)

---

## 3. Investigation and Methodology

### Wireshark Analysis

1. Open `say-cheese_capture.pcap` in Wireshark
2. Follow HTTP streams
3. Look for image data (JPEG/PNG signatures) in HTTP responses
4. Export the image (File → Export Objects → HTTP)

### Image Analysis

The recovered image may have steganography or visual artifacts. Examine:
- Visual inspection (zoom, enhance)
- Steganography tools (`zsteg`, `steghide`, `exiftool`)
- LSB analysis
- Color channel separation

---

## 4. Current Status

**Unsolved.** The PCAP has not been fully analyzed in this repository. HTTP objects extracted include: `gen_204`, `ncsi.txt`, `favicon.ico`, `badge.png`, but the flag has not been recovered.

---

## 5. Flag

**None recovered** — Challenge remains unsolved.

---

## 6. Evidence and References

- `evidence/say-cheese_capture.pcap` — Network capture
- `evidence/analysis/http_objects/` — HTTP objects (gen_204, ncsi.txt, favicon.ico, badge.png)
- `evidence/analysis/swirl_zoom.png` — Enhanced analysis image

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

