# Operation Quthing Storm

**Category:** ICS / OT Security
**Difficulty:** Hard
**Points:** 4450
**Status:** Partial (Some questions answered, firmware analyzed)

---

## 1. Challenge Overview

**Scenario:** It is 07 December 2024, 23:15 in Maseru. The phones at CSIRT Lesotho start ringing. Metolong Dam (water for 400,000+ people) reports anomalous readings: Spillway Gate 7 open, safety interlock bypassed, PLC unresponsive, backup generator tripped, logs wiped remotely. By midnight, water level dropping — not a failure, an attack.

At 01:30, a burned USB drive is left at CSIRT front desk containing `wh097_firmware.bin` from the Metolong Dam Water Control System (LesothoTech Industrial, model MTD-WCS-042). A note: *"Lesson delivered. Start learning."*

Attacker: **Wh097**. Intelligence points to Quthing (southern Lesotho, Maluti mountains). Remote, off-grid. He left breadcrumbs — either to be caught or to be understood.

**Job:** Find everything.

---

## 2. Initial Analysis

### Files

| File | Description |
|------|-------------|
| `wh097_firmware.bin` | Firmware binary from MTD-WCS-042 |
| `wh097_drone_capture.zip` | Drone capture (PCAP) |
| `wh097_firmware.bin.extracted/` | Binwalk extraction of firmware |

### Firmware Extraction (Binwalk)

The firmware is a SquashFS filesystem. Extracted to `_wh097_firmware.bin.extracted/squashfs-root/`.

Key artifacts found:
- `/etc/init.d/S99backdoor` — Backdoor init script
- `/etc/banner` — Banner with flag: `LsCTF2026{b4nn3r_gr4bb1ng_101_wh097}`
- `/etc/shadow` — Password hashes
- `/etc/passwd` — User `wh097` with flag in GECOS: `LsCTF2026{y0u_f0und_th3_gh0st_0f_quth1ng}` (VERIFIED)
- `/usr/share/.quthing/manifesto.txt` — Attacker manifesto
- `/opt/ics_controller/logs/` — Modbus logs, exfil data
- `/opt/ics_controller/config/system.conf` — Controller config
- `/opt/ics_controller/payloads/modbus_write.py` — Modbus payload script
- `/tmp/.wh097_cache/.session_token` — Session token
- `/tmp/.metolong/.coordinates` — Coordinates
- `/home/wh097/.bash_history` — Command history
- `/home/wh097/.ssh/authorized_keys` — SSH keys

---

## 3. Investigation and Methodology

### Question 6 (200 pts)

> The same password appears somewhere else in the config. Where, and in what field?

**Status:** Not yet answered in this repository.

### Question 16 (200 pts)

> There are hidden directories in `/tmp`. One contains a base64 encoded JSON token. Decode it. What flag is inside the JSON?

**Status:** Not yet answered in this repository. The hidden directories `/tmp/.wh097_cache/` and `/tmp/.metolong/` are known; `.session_token` and `.coordinates` need base64 decoding and JSON parsing.

---

## 4. Flags Found (Partial)

### From `/etc/banner`
```
LsCTF2026{b4nn3r_gr4bb1ng_101_wh097}
```

### From `/etc/passwd` (wh097 user GECOS field)
```
LsCTF2026{y0u_f0und_th3_gh0st_0f_quth1ng}
```

### From `/usr/share/.quthing/manifesto.txt`
Likely contains additional flags/intel.

### From `/tmp/.wh097_cache/.session_token` (base64 JSON)
Pending decode.

### From `/tmp/.metolong/.coordinates` (base64 JSON)
Pending decode.

---

## 5. Current Status

**Partial.** Firmware fully extracted and key files identified. Two flags recovered from static files. Remaining questions require deeper analysis of:
- Modbus traffic (`modbus.log`, `modbus_write.py`)
- Drone capture (`wh097_drone_capture.zip`)
- Password cracking (`/etc/shadow`)
- Session token / coordinates decoding

---

## 6. Evidence and References

- `evidence/wh097_firmware.bin` — Original firmware
- `evidence/wh097_drone_capture.zip` — Drone PCAP
- `evidence/squashfs-root/` — Extracted filesystem
- `evidence/squashfs-root/etc/banner` — Banner flag
- `evidence/squashfs-root/etc/passwd` — Passwd flag
- `evidence/squashfs-root/etc/shadow` — Shadow file
- `evidence/squashfs-root/usr/share/.quthing/manifesto.txt` — Manifesto
- `evidence/squashfs-root/opt/ics_controller/` — ICS controller files
- `evidence/squashfs-root/tmp/.wh097_cache/.session_token` — Session token
- `evidence/squashfs-root/tmp/.metolong/.coordinates` — Coordinates

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

