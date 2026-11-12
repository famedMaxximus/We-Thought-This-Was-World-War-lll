# NOTES

```
OPERATION FLY MALOTI - WORKING NOTES
=====================================
3rd annual cybersecurity hackathon, Lesotho
Scenario: 07 Dec 2024, 22:41 UTC. MOUNTAIN-3 captured a 433.925 MHz UAV
telemetry downlink (operator Wh097). Signal changes character at ~T+19 s.
Task: demodulate, decode protocol, reconstruct flight, recover all data.

FILES
-----
- wh097_drone_capture.zip -> wh097_drone_capture.wav (60,000,058 bytes)
    WAV header 58 bytes, format 3 (IEEE float32), 2 channels, 250,000 Hz.
    L = I, R = Q. 30.0 s total.
- wh097_firmware.zip -> wh097_firmware.bin (9,250 bytes) - NOT YET ANALYZED

=====================================================================
QUESTION 1 (50 pts)
Open the WAV in URH (Complex float32, 250000 S/s). What modulation scheme?
ANSWER: 2-FSK   <-- ACCEPTED (exact string "2-FSK")
---------------------------------------------------------------------
Method (Python/numpy, reading IQ from offset 58 as interleaved float32):
1. Amplitude envelope: noise floor ~0.1, bursts ~0.5-0.7. Inside a burst
   amplitude std/mean is only ~0.14 = constant carrier, no on/off keying
   -> rules out OOK/ASK.
2. Instantaneous frequency inside bursts (angle(s[n]*conj(s[n-1]))*fs/2pi)
   is bimodal: two tones at ~ +41.5 kHz and ~ +57.5 kHz from center.
   -> 2-FSK, shift ~16 kHz (deviation ~ +/-8 kHz), centered ~ +49.5 kHz.
3. Burst timing: 32 bursts from ~2.0 s to ~27.8 s, each ~25-170 ms
   (6,241 to 42,434 samples). Burst start times (s):
   2.0 2.8 3.5 4.0 5.0 5.5 6.0 6.5 7.5 8.0 9.0 10.0 10.5 11.0 12.0 13.5
   14.0 16.0 17.0 17.5 18.5 19.0 20.5 21.0 21.5 22.5 24.0 24.5 25.5 26.0
   27.0 27.8
4. Symbol timing: ~52 samples/symbol -> 250000/52 = ~4808 baud (~4800 bd).
   Each burst starts with an alternating 1010... preamble.
   Frequency transitions are sharp (a few samples), with no visible Gaussian
   smoothing, so it looks like plain FSK, not GFSK.
SUBMISSION LOG:
   "FSK (binary 2-FSK)."  -> REJECTED (probably the format, not the answer)
   "2-FSK"                -> ACCEPTED
   Lesson: the grader wants an exact short token. Submit just the value.
URH tip: Interpretation tab -> Autodetect, or set Modulation = FSK manually;
the center will sit near +49.5 kHz because of the frequency offset.

=====================================================================
QUESTION 2 (100 pts)
SDR tuned to 433.875 MHz. Carrier offset from DC in the recording (kHz)?
ANSWER: 50   <-- ACCEPTED
---------------------------------------------------------------------
- Theory: 433.925 MHz (signal) - 433.875 MHz (tuned) = 0.050 MHz = +50 kHz.
- Measured: FSK tones at ~+41.5 kHz and ~+57.5 kHz, midpoint ~+49.5 kHz.
  A burst FFT peak sat at ~+41.5 kHz, which is one tone, not the carrier.
  Measurement agrees with theory to within estimation error.

=====================================================================
QUESTION 3 (100 pts)
Actual real-world frequency of the drone's transmitter in MHz?
ANSWER: 433.925   <-- ACCEPTED
---------------------------------------------------------------------
- Tuned 433.875 MHz + offset 0.050 MHz (Q2) = 433.925 MHz.
- Matches the brief ("narrowband signal appears on 433.925 MHz").
- Measured tone medians across all bursts: low ~41.6 kHz, high ~57.0 kHz,
  midpoint ~49.3 kHz -> 433.9243 MHz. That is the nominal 50 kHz within
  noise/estimation error (the noise bias pulls the medians inward).

=====================================================================
QUESTION 4 (100 pts)
Measure the baud rate by counting samples per symbol transition.
ANSWER: 4800   <-- ACCEPTED
---------------------------------------------------------------------
- FM-demodulated each burst (instantaneous freq), smoothed (9 taps),
  sliced at 49.5 kHz, found transitions, divided run lengths by nearest
  whole number of symbols.
- Result across all 32 bursts: 51.98 samples/symbol (range 51.95-52.00).
- 250000 / 52 = 4807.7 baud. Nearest standard rate = 4800 baud.
  (A transmitter generating exactly 52 samples/symbol is effectively 4800 bd.)
- Preamble at burst start = alternating 1010... with ~52-sample runs.

=====================================================================
QUESTION 5 (100 pts)
First STATUS message at ~T+2.8 s contains a plain-ASCII flag. What is it?
ANSWER: LsCTF2026{f1rst_s1gn4l_d3c0d3d_quth1ng_433MHz}
---------------------------------------------------------------------
Demod method (scripts/demod.py, scripts/dec.py):
- Burst detect: |IQ| smoothed (25 taps) > 0.3.
- FM discriminator: angle(s[n]*conj(s[n-1]))*fs/2pi, smoothed 15 taps,
  sliced at 49.5 kHz (high tone = 1, low tone = 0).
- Clock: 51.98 samples/symbol, phase from the first transition, sample at
  the symbol centre.
- Frame: preamble 0xAA x4, sync 0x7E 0x5A, then bytes (MSB first).
  Full decode of all 32 bursts -> decoded_frames.txt
Frame at 2.800 s:
  7e 5a 03 02 5c "BOOT OK | MISSION: SURVEY_METOLONG_DAM |
  FLAG=LsCTF2026{f1rst_s1gn4l_d3c0d3d_quth1ng_433MHz}" 60
Provisional frame layout: [7E 5A sync][type][seq][len][payload][1-byte CRC?]
  type 01 = heartbeat/ID, 02 = GPS/telemetry (binary), 03 = STATUS text,
  04 = param, 05 = COMMAND (appears at T+19 s = the "change in character"),
  06 = short (battery/RSSI?)

OTHER ITEMS SEEN IN THE DECODE (for later questions, not yet submitted):
- 2.000 s type 01: QTH-UAV-007, fw v2.1,
  LsCTF2026{h34rtb34t_f13ld_17_expos3s_0p3r4t0r}
- 3.500 s: OPERATOR: wh097@protonmail.com | CALLSIGN: QTH-UAV-007
- 11.000 s type 04: CRYPT_IV + 50-ish bytes of binary (encrypted? key may be in firmware)
- 16.000 s type 02: LsCTF2026{GPS_w4yp01nt_0v3r_m3t0l0ng_c4tchm3nt}
- 19.000 s type 05 CMD 0xC2C2, deadbeef:
  LsCTF2026{c0mm4nd_1nj3ct10n_0v3r_th3_4ir_wh097}
- 21.000 s type 05: GOTO:-29.2541,27.5102 ALT:50 FORCE
- 27.000 s FINAL_TX base64:
  THNDVEYyMDI2e2w0c3RfdHJhbnNtMXNzMTBuX1FUSF9VQVZfMDA3X3MxbDNuYzNkfQ==

=====================================================================
QUESTION 6 (100 pts)
HEARTBEAT frame at T+2.0 s contains the drone's ID string. What is it?
ANSWER: QTH-UAV-007   (fallback: the flag in the same frame,
        LsCTF2026{h34rtb34t_f13ld_17_expos3s_0p3r4t0r})
---------------------------------------------------------------------
Frame at 2.000 s (type 01 = HEARTBEAT, seq 01, len 0x3F = 63):
  7e 5a 01 01 3f | 51 54 48 2d 55 41 56 2d 30 30 37 00 = "QTH-UAV-007\0"
  | 76 32 2e 31 = "v2.1" | 05 | "LsCTF2026{h34rtb34t_f13ld_17_expos3s_0p3r4t0r}" | ed
- ID is null-terminated, followed by firmware version v2.1.
- QTH = Quthing (operator's district). The callsign also appears in the
  3.5 s STATUS frame: "CALLSIGN: QTH-UAV-007".

=====================================================================
QUESTION 7 (100 pts)
HEARTBEAT payload byte offset 17 ("reserved" in spec). Parse it. Flag?
ANSWER: LsCTF2026{h34rtb34t_f13ld_17_expos3s_0p3r4t0r}
---------------------------------------------------------------------
HEARTBEAT payload (63 bytes, after 7e 5a | 01 01 3f):
  off 0-11  : "QTH-UAV-007\0"   drone ID (null-terminated)
  off 12-15 : "v2.1"            firmware version
  off 16    : 0x05              status/mode byte
  off 17-62 : "LsCTF2026{h34rtb34t_f13ld_17_expos3s_0p3r4t0r}" (46 bytes)
              <- the "reserved" field ("f13ld_17" in the flag confirms it)
  trailer   : 0xED (checksum, outside the payload)

=====================================================================
QUESTION 8 (100 pts)
Five GPS frames trace a flight path; final waypoint at T+16.0 s has extra
data appended after the standard GPS fields. Flag?
ANSWER: LsCTF2026{GPS_w4yp01nt_0v3r_m3t0l0ng_c4tchm3nt}
---------------------------------------------------------------------
GPS frame (type 02) payload, big-endian:
  off 0-3  int32 lat  x1e-7 deg
  off 4-7  int32 lon  x1e-7 deg
  off 8-11 int32 alt  mm
  off 12-17 6 bytes: u16 speed?, u16 heading?, 0x0309 (fix/sats?)
  off 18-25 8 x 0x00 padding (normal frames, len 0x1A = 26)
The 16.0 s frame has len 0x41 = 65; the flag starts at off 18 instead of the padding.

Flight path (time, seq, lat, lon, alt):
  4.0  #4   -30.4012, 27.7108  182 m   <- start, Quthing district
  6.5  #5   -30.1845, 27.7521  195 m
  9.0  #6   -29.9230, 27.8013  205 m
 12.0  #7   -29.6712, 27.8634  215 m
 16.0  #8   -29.3189, 27.9643  208 m   <- final waypoint, Metolong catchment (+flag)
 --- after T+19 s (post command injection) ---
 18.5  #21  -29.3189, 27.9643  208 m   hovering (speed field 0x0032)
 22.5  #26  -29.3189, 27.9643  190 m
 25.5  #29  -29.5200, 27.8800  175 m   emergency RTL, heading back south
Injected GOTO target (21.0 s): -29.2541, 27.5102 ALT 50

=====================================================================
QUESTION 9 (100 pts)
PARAM frame at T+11.0 s: CRYPT_IV, XOR-encrypted, key derivable from the
drone's own transmissions. Decrypt. Flag?
ANSWER: LsCTF2026{XOR_w1th_dr0n3_1D_pr3f1x_QTH_d4sh}
---------------------------------------------------------------------
PARAM frame (type 04) payload = ASCII param name + value.
  11.0 s: 7e 5a 04 0e 35 | "CRYPT_IV" | 45-byte ciphertext | a4
  ciphertext: 1d270b791766781f672f1062030b3f1c253c17492364261e0e650c72
              21267b4b602c177c051c17496527205005
Known-plaintext attack: ciphertext XOR "LsCTF2026{" = "QTH-QTH-QT"
  -> repeating 4-byte key "QTH-" (the drone ID prefix from QTH-UAV-007).
Decrypt: plaintext[i] = c[i] ^ "QTH-"[i % 4]
  -> LsCTF2026{XOR_w1th_dr0n3_1D_pr3f1x_QTH_d4sh}  (+1 trailing junk byte)
Other PARAM frames: 5.5 s "MAX_SPEE.." / 8.0 s "RTL_ALT_.." (short numeric values)

=====================================================================
QUESTION 10 (100 pts)
COMMAND frame at T+19.0 s with unrecognised cmd_id: cmd_id in hex + flag.
Format: command,LsCTF{}
ANSWER: 0xC2C2,LsCTF2026{c0mm4nd_1nj3ct10n_0v3r_th3_4ir_wh097}
   (fallbacks: C2C2,LsCTF2026{...}  /  0xc2c2,LsCTF2026{...})
---------------------------------------------------------------------
19.0 s frame: 7e 5a 05 16 3f | c2 c2 | 01 00 | de ad be ef | 00 00 00 01 |
              00 00 00 00 | "LsCTF2026{c0mm4nd_1nj3ct10n_0v3r_th3_4ir_wh097}" | 18
COMMAND (type 05) payload layout (provisional):
  off 0-1  cmd_id   0xC2C2 (unrecognised; "C2" = command & control)
  off 2-3  0x0100   flags/version?
  off 4-7  0xDEADBEEF auth token/magic
  off 8-11 counter  (1 here, 2 in the 21.0 s frame)
  off 12-15 0
  off 16+  extra bytes: flag (19.0 s) / "GOTO:-29.2541,27.5102 ALT:50 FORCE" (21.0 s)
The drone's 20.5 s STATUS confirms it: "[ALERT] UNEXPECTED COMMAND RECEIVED | CMD_ID=0xC2C2"
This is the T+19 s "change in character" from the brief.

=====================================================================

=====================================================================
QUESTION (150 pts) - /etc/shadow SHA-512 crack
The attacker's account has a SHA-512 hash in /etc/shadow. Crack it.
ANSWER (password): Quthing@2024
---------------------------------------------------------------------
Source: wh097_firmware.bin (uImage; fake CRCs DEADBEEF/CAFEF00D).
  - uImage header 64B says gzip/8192B but payload is NOT real gzip.
  - Real data = embedded zlib (78 da) streams. Big one at file offset
    672 -> 24,301 bytes = packed rootfs (banner, passwd, shadow, cron,
    system.conf, logs, etc.). Dir index stream at offset 7782.
  - Extract: python zlib.decompressobj().decompress(bin[672:])
/etc/shadow (two accounts share ONE hash - the attacker wh097 / backdoor):
  wh097:$6$6Skn1aQzTGK2N0Ne$z.yf3YoP5Z7NWEyMyOgIh/6ltykdNw/QAFvZ8.UgB3VX9e17P/oMC18R.P45FZR9x8e9PYCcgCbfPLWr9Ca9V.:19742:0:99999:7:::
  backdoor:$6$6Skn1aQzTGK2N0Ne$...(same)...:19742:0:99999:7:::
Crack: hint came from recovered etc/system.conf -> [backdoor] telnet_pass = Quthing@2024
  john --wordlist=cand.txt --format=crypt hash.txt  ->  wh097:Quthing@2024
Bonus flags recovered from the rootfs blob along the way:
  LsCTF2026{b4nn3r_gr4bb1ng_101_wh097}          (banner)
  LsCTF2026{y0u_f0und_th3_gh0st_0f_quth1ng}     (passwd GECOS, user wh097)
  LsCTF2026{ssh_k3y_t0_th3_k1ngd0m_0f_quth1ng}  (authorized_keys comment)
  LsCTF2026{m0dbus_cl34rt3xt_k1lls_1nfr4structur3_wh097} (modbus.log)
  LsCTF2026{str1ngs_r3v34l_c2_b34c0n_wh097_0wns_d4m}     (beacon binary)
  LsCTF2026{wh097_th3_m4lut1_gh0st_l3s0th0_r1s3s}        (note)
  LsCTF2026{4uth_l0gs_c4tch_3v3n_gh0sts_wh097_0192}      (auth log)
```
