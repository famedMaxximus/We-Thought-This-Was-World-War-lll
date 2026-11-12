# Operation Quthing Storm

**Category:** ICS / OT Security (SDR signal analysis + firmware forensics)
**Difficulty:** Hard
**Points:** 4450
**Status:** Partial (drone Q1–Q4 accepted; remaining answers and firmware flags recovered, submission status not recorded for most)

---

## 1. Challenge Overview

**Scenario:** It is 07 December 2024, 23:15 in Maseru. The phones at CSIRT Lesotho start ringing. Metolong Dam (water for 400,000+ people) reports anomalous readings: Spillway Gate 7 open, safety interlock bypassed, PLC unresponsive, backup generator tripped, logs wiped remotely. By midnight, the water level is dropping — not a failure, an attack.

At 01:30, a burned USB drive is left at the CSIRT front desk containing `wh097_firmware.bin` from the Metolong Dam Water Control System (LesothoTech Industrial, model MTD-WCS-042). A note: *"Lesson delivered. Start learning."*

Attacker: **Wh097**. Intelligence points to Quthing (southern Lesotho, Maluti mountains).

A second module ("Operation Fly Maloti"): at 22:41 UTC on 07 Dec 2024, MOUNTAIN-3 captured a 433.925 MHz UAV telemetry downlink from operator Wh097. The signal changes character at ~T+19 s. Task: demodulate, decode the protocol, reconstruct the flight, recover all data.

**Job:** Find everything.

---

## 2. Initial Analysis

### Files

| File | Description |
|------|-------------|
| `wh097_drone_capture.zip` → `wh097_drone_capture.wav` | 60,000,058 bytes. WAV header 58 bytes, format 3 (IEEE float32), 2 channels (L = I, R = Q), 250,000 Hz, 30.0 s |
| `wh097_firmware.zip` → `wh097_firmware.bin` | 9,250 bytes, uImage with fake CRCs (DEADBEEF/CAFEF00D) |

### Firmware layout

The 64-byte uImage header says gzip/8192 B, but the payload is **not** real gzip.
The real data is embedded zlib (`78 da`) streams: the big one at file offset
**672** (24,301 bytes) is the packed rootfs (banner, passwd, shadow, cron,
`system.conf`, logs, …); a directory index stream sits at offset **7782**.

```python
zlib.decompressobj().decompress(fw[672:])
```

Rootfs contents named in the index include `/etc/init.d/S99backdoor`,
`/etc/banner`, `/etc/passwd`, `/etc/shadow`, `/etc/cron.d`,
`/opt/ics_controller/{config/system.conf,logs/modbus.log,payloads/modbus_write.py}`,
`/home/wh097/{.bash_history,.ssh/authorized_keys}`,
`/tmp/.wh097_cache/.session_token`, `/tmp/.metolong/.coordinates`,
`/usr/share/.quthing/manifesto.txt`, `/var/log/auth.log`.

---

## 3. Investigation and Methodology

### Drone capture — modulation and timing (numpy on raw IQ at offset 58)

1. **Amplitude envelope:** noise floor ~0.1, bursts ~0.5–0.7. Inside a burst,
   amplitude std/mean is only ~0.14 → constant carrier, no on/off keying → rules
   out OOK/ASK.
2. **Instantaneous frequency** inside bursts (`angle(s[n]*conj(s[n-1]))*fs/2π`)
   is bimodal: two tones at ~+41.5 kHz and ~+57.5 kHz → **2-FSK**, shift ~16 kHz
   (deviation ±8 kHz), centred ~+49.5 kHz. Sharp transitions, no Gaussian
   smoothing → plain FSK, not GFSK.
3. **Bursts:** 32 bursts from ~2.0 s to ~27.8 s, each ~25–170 ms.
4. **Symbol timing:** 51.98 samples/symbol across all 32 bursts
   (range 51.95–52.00) → 250000/52 = 4807.7 → **4800 baud**. Each burst starts
   with an alternating `1010…` preamble.

### Demodulation and framing (`scripts/demod.py`, `scripts/dec.py`)

- Burst detect: |IQ| smoothed (25 taps) > 0.3.
- FM discriminator, smoothed 15 taps, sliced at 49.5 kHz (high tone = 1).
- Clock 51.98 samples/symbol, phase from the first transition, sample at symbol centre.
- Frame: preamble `0xAA ×4`, sync `0x7E 0x5A`, then `[type][seq][len][payload][1-byte checksum]`, MSB first.
- Types: `01` heartbeat/ID, `02` GPS, `03` STATUS text, `04` PARAM, `05` COMMAND, `06` short (battery/RSSI?).

Full decode of all 32 bursts is in `evidence/decoded_frames.md`.

---

## 4. Vulnerability / Technical Discovery

- **Cleartext UAV telemetry** — flags, operator e-mail and callsign broadcast unencrypted on 433.925 MHz.
- **"Encryption" with a repeating key from public data** — the CRYPT_IV parameter is XORed with the drone ID prefix.
- **Unauthenticated command channel** — an unknown `cmd_id 0xC2C2` with a `DEADBEEF` token was accepted, followed by a forced GOTO.
- **Firmware secrets** — hardcoded credentials, a backdoor telnet account, persistence via cron and init scripts, and base64-"hidden" payloads.

---

## 5. Exploitation / Solution

### Drone capture questions

| Q | Pts | Question | Answer | Status |
|---|-----|----------|--------|--------|
| 1 | 50 | Modulation scheme | `2-FSK` | ✅ Accepted (`"FSK (binary 2-FSK)."` was rejected — the grader wants the exact short token) |
| 2 | 100 | Carrier offset from DC (SDR tuned to 433.875 MHz), kHz | `50` | ✅ Accepted |
| 3 | 100 | Real transmitter frequency, MHz | `433.925` | ✅ Accepted |
| 4 | 100 | Baud rate | `4800` | ✅ Accepted |
| 5 | 100 | Flag in first STATUS message (~T+2.8 s) | `LsCTF2026{f1rst_s1gn4l_d3c0d3d_quth1ng_433MHz}` | Recovered; acceptance not recorded |
| 6 | 100 | Drone ID in HEARTBEAT (T+2.0 s) | `QTH-UAV-007` | Recovered; acceptance not recorded |
| 7 | 100 | HEARTBEAT "reserved" field at offset 17 | `LsCTF2026{h34rtb34t_f13ld_17_expos3s_0p3r4t0r}` | Recovered; acceptance not recorded |
| 8 | 100 | Extra data on final GPS waypoint (T+16.0 s) | `LsCTF2026{GPS_w4yp01nt_0v3r_m3t0l0ng_c4tchm3nt}` | Recovered; acceptance not recorded |
| 9 | 100 | XOR-encrypted CRYPT_IV PARAM (T+11.0 s) | `LsCTF2026{XOR_w1th_dr0n3_1D_pr3f1x_QTH_d4sh}` | Recovered; acceptance not recorded |
| 10 | 100 | Unrecognised COMMAND (T+19.0 s), `command,LsCTF{}` | `0xC2C2,LsCTF2026{c0mm4nd_1nj3ct10n_0v3r_th3_4ir_wh097}` | Recovered; acceptance not recorded |

**Q2/Q3:** 433.925 − 433.875 = +0.050 MHz = 50 kHz. Measured tone medians
(~41.6 / ~57.0 kHz, midpoint ~49.3 kHz) agree within estimation error.

**Q5** — frame at 2.800 s:
```
7e 5a 03 02 5c "BOOT OK | MISSION: SURVEY_METOLONG_DAM |
FLAG=LsCTF2026{f1rst_s1gn4l_d3c0d3d_quth1ng_433MHz}" 60
```

**Q6/Q7** — HEARTBEAT at 2.000 s (type 01, seq 01, len 0x3F = 63):
```
off 0-11  : "QTH-UAV-007\0"   drone ID (null-terminated)
off 12-15 : "v2.1"            firmware version
off 16    : 0x05              status/mode byte
off 17-62 : "LsCTF2026{h34rtb34t_f13ld_17_expos3s_0p3r4t0r}"   <- "reserved" field
trailer   : 0xED
```
The callsign is confirmed by the 3.5 s STATUS frame:
`OPERATOR: wh097@protonmail.com | CALLSIGN: QTH-UAV-007`.

**Q8** — GPS (type 02) payload, big-endian: int32 lat ×1e-7, int32 lon ×1e-7,
int32 alt (mm), 6 bytes speed/heading/fix, 8 bytes zero padding (len 0x1A). The
16.0 s frame has len 0x41 and carries the flag instead of the padding.

Flight path:
```
 4.0 s  -30.4012, 27.7108  182 m   start, Quthing district
 6.5 s  -30.1845, 27.7521  195 m
 9.0 s  -29.9230, 27.8013  205 m
12.0 s  -29.6712, 27.8634  215 m
16.0 s  -29.3189, 27.9643  208 m   final waypoint, Metolong catchment (+flag)
--- after T+19 s (command injection) ---
18.5 s  -29.3189, 27.9643  208 m   hovering
22.5 s  -29.3189, 27.9643  190 m
25.5 s  -29.5200, 27.8800  175 m   emergency RTL, heading south
Injected GOTO target (21.0 s): -29.2541, 27.5102 ALT 50
```

**Q9** — PARAM frame at 11.0 s: `"CRYPT_IV"` + 45-byte ciphertext.
Known plaintext: `ciphertext XOR "LsCTF2026{" = "QTH-QTH-QT"` → repeating
4-byte key `QTH-` (the drone ID prefix). `plaintext[i] = c[i] ^ "QTH-"[i % 4]`.

**Q10** — COMMAND at 19.0 s:
```
7e 5a 05 16 3f | c2 c2 | 01 00 | de ad be ef | 00 00 00 01 | 00 00 00 00 |
"LsCTF2026{c0mm4nd_1nj3ct10n_0v3r_th3_4ir_wh097}" | 18
```
The drone's 20.5 s STATUS confirms it: `[ALERT] UNEXPECTED COMMAND RECEIVED | CMD_ID=0xC2C2`.
The 21.0 s COMMAND carries `GOTO:-29.2541,27.5102 ALT:50 FORCE`. This is the
T+19 s "change in character" from the brief.

**Extra — FINAL_TX (27.0 s STATUS frame):**
```
FINAL_TX | THNDVEYyMDI2e2w0c3RfdHJhbnNtMXNzMTBuX1FUSF9VQVZfMDA3X3MxbDNuYzNkfQ== | LINK_LOST
base64 -d -> LsCTF2026{l4st_transm1ss10n_QTH_UAV_007_s1l3nc3d}
```
Recovered from the capture; no question for it is recorded and its submission status is unknown.

### Firmware questions

**/etc/shadow SHA-512 crack (150 pts).** Accounts `wh097` and `backdoor` share one hash:
```
wh097:$6$6Skn1aQzTGK2N0Ne$z.yf3YoP5Z7NWEyMyOgIh/6ltykdNw/QAFvZ8.UgB3VX9e17P/oMC18R.P45FZR9x8e9PYCcgCbfPLWr9Ca9V.:19742:0:99999:7:::
```
The candidate came from `system.conf`; `john --wordlist=cand.txt --format=crypt hash.txt` → **`Quthing@2024`**.

**"The same password appears somewhere else in the config. Where, and in what field?"**
In `/opt/ics_controller/config/system.conf`, section `[backdoor]`, field **`telnet_pass`**:
```
[backdoor]
# DO NOT REMOVE - engineering access
telnet_user = backdoor
telnet_pass = Quthing@2024
```

**Hidden `/tmp` base64 JSON token.** Decodes to:
```json
{"type":"session","attacker":"wh097","flag":"LsCTF2026{h1dd3n_d0tf1l3s_4r3_n3v3r_s4f3_1n_quth1ng}","target":"Metolong Dam","status":"compromised","timestamp":"2024-12-07T23:47:12Z"}
```

### Flags in the firmware rootfs

Reproduced with `scripts/extract_firmware.py` (unpacks the zlib rootfs, greps
flags, and decodes embedded base64):

| Flag | Location |
|------|----------|
| `LsCTF2026{b4nn3r_gr4bb1ng_101_wh097}` | `/etc/banner` |
| `LsCTF2026{y0u_f0und_th3_gh0st_0f_quth1ng}` | `/etc/passwd` GECOS of `wh097` |
| `LsCTF2026{ssh_k3y_t0_th3_k1ngd0m_0f_quth1ng}` | `authorized_keys` comment |
| `LsCTF2026{c3rt1f1c4t3s_d0nt_l13_1f_y0u_kn0w_wh3r3_t0_l00k}` | certificate CN (`metolong_ctrl.crt`) |
| `LsCTF2026{h4rdc0d3d_k3ys_s1nk_sh1ps_4nd_d4ms}` | `system.conf` `api_key` |
| `LsCTF2026{m0dbus_cl34rt3xt_k1lls_1nfr4structur3_wh097}` | `modbus.log` |
| `LsCTF2026{pyth0n_plus_m0dbus_3quals_0wn3d_d4m}` | `modbus_write.py` comment (`EXFIL_KEY`) |
| `LsCTF2026{GPS_tr41l_l34ds_t0_quth1ng_28S_27E}` | `.coordinates` note |
| `LsCTF2026{h1dd3n_d0tf1l3s_4r3_n3v3r_s4f3_1n_quth1ng}` | base64 JSON session token in `/tmp` |
| `LsCTF2026{cront4b_1s_w31rd_w1ld_wh397_p0wer}` | base64 in `/etc/cron.d` "watchdog" job |
| `LsCTF2026{1n1t_d_p3rs1st3nc3_w1ns_4g41n_wh097}` | base64 `_x` in `S99backdoor` |
| `LsCTF2026{bash_h1st0ry_n3v3r_l13s_wh097_l3ft_pr00f}` | base64 in `.bash_history` |
| `LsCTF2026{str1ngs_r3v34l_c2_b34c0n_wh097_0wns_d4m}` | beacon binary strings |
| `LsCTF2026{wh097_th3_m4lut1_gh0st_l3s0th0_r1s3s}` | attacker note |
| `LsCTF2026{4uth_l0gs_c4tch_3v3n_gh0sts_wh097_0192}` | `auth.log` |

---

## 6. Flag

Accepted answers: Q1 `2-FSK`, Q2 `50`, Q3 `433.925`, Q4 `4800`.

Previously marked verified in this repository: `LsCTF2026{b4nn3r_gr4bb1ng_101_wh097}`,
`LsCTF2026{y0u_f0und_th3_gh0st_0f_quth1ng}`.

All other flags above are reproduced from the handout files (capture decode or
firmware rootfs), but whether each was submitted and accepted was not recorded.

---

## 7. Lessons Learned

1. **Graders want exact tokens** — `2-FSK` was accepted where a descriptive answer was rejected.
2. **Measure, then check against theory** — tuned frequency + offset gave the carrier exactly; measured tones confirmed it.
3. **Known-plaintext breaks repeating-key XOR** — the flag prefix `LsCTF2026{` revealed the key `QTH-`.
4. **Don't trust firmware headers** — the uImage claimed gzip; the data was raw zlib at other offsets.
5. **Credential reuse** — the shadow password was sitting in plaintext in `system.conf`.

---

## 8. Tools Used

- Python 3 + NumPy (IQ envelope, FM discriminator, burst detection, clock recovery)
- URH (optional cross-check: Complex float32, 250000 S/s)
- `zlib`, `base64`, `strings`
- John the Ripper (`--format=crypt`)

---

## 9. Evidence and References

- `scripts/demod.py` — burst detection + FSK demodulation of the WAV
- `scripts/dec.py` — frame sync and byte decoding
- `scripts/an*.py` — exploratory envelope / frequency / timing analysis
- `scripts/extract_firmware.py` — rootfs extraction and flag listing
- `evidence/decoded_frames.md` — all 32 decoded frames
- `evidence/NOTES.md` — original working notes with submission log
