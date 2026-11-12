# Mohale Sensor Traces

**Category:** Cryptography / Hardware Security
**Difficulty:** Hard
**Points:** Unknown
**Status:** Solved (Both flags verified)

---

## 1. Challenge Overview

Side-channel analysis challenge. The handout contains AES plaintext/ciphertext pairs and power traces for two different firmware builds. The bootloader has 2,500 traces with 96 samples each; the field firmware has 60,000 traces with 98 samples each.

---

## 2. Initial Analysis

### Handout (`Mohale Sensor Traces handout.zip` → `extracted/handout/`)

| File | Content |
|------|---------|
| `boot_traces.npy` | 2,500 × 96 power traces (bootloader) |
| `boot_pt.npy` | 2,500 plaintexts (bootloader) |
| `fw_pt.npy` | 60,000 plaintexts (firmware) |
| `flag1.enc` | Flag 1 encrypted |
| `flag2.enc` | Flag 2 encrypted |

---

## 3. Investigation and Methodology

### Flag 1 — Bootloader (1st-Order CPA)

For each byte position and candidate key byte `k`, predict:
```
HW(SBOX[plaintext_byte XOR k])
```
Compute Pearson correlation with every trace sample. The strongest absolute correlation selects the byte. Repeating for all 16 positions recovers:

```
e403a16c08b08d0cf1a3276f050d0768
```

The key reproduces the supplied AES ciphertexts. Decrypt `flag1.enc` using:
```
SHA-256("mohale-flag1|" + lowercase_hex(boot_key))
```

### Flag 2 — Firmware (2nd-Order CPA with Timing Shift)

The firmware uses **Boolean masking**, so useful leakage is in products of centered sample pairs.

For each pair `(i, j)`, form:
```
(trace[i] - mean[i]) * (trace[j] - mean[j])
```
Normalize it, and correlate against the same S-box Hamming-weight predictions. Retain signed correlations.

There is also a **timing shift over three sample positions**. For each nominal pair, combine the correlations for `(i,j)`, `(i+1,j+1)`, and `(i+2,j+2)` before taking an absolute value. Using this three-position sum recovers the complete key:

```
a8ddd0d11c6c7a9fe18c4db74de5d6ee
```

That key reproduces the firmware ciphertexts, and authenticated AES-GCM decryption succeeds with:
```
SHA-256("mohale-flag2|" + lowercase_hex(firmware_key))
```

---

## 4. Vulnerability / Technical Discovery

| Target | Protection | Attack |
|--------|------------|--------|
| Bootloader | None (raw AES) | 1st-order CPA (Hamming weight of S-box output) |
| Firmware | Boolean masking | 2nd-order CPA (product of centered pairs) + timing shift compensation |

**Key insight**: Masking moves leakage to 2nd order (products of shares). The timing shift (jitter) spreads the leakage across adjacent samples, requiring the 3-position sum to capture the full signal.

---

## 5. Exploitation / Solution

```bash
# Bootloader CPA (verifies both keys)
python3 solve.py --challenge mohale

# Full firmware 2nd-order CPA (memory intensive ~1.5 GB)
python3 solve.py --challenge mohale --recover-firmware
```

### Complete Solver Flow (`solve.py`)

1. Load `boot_traces.npy`, `boot_pt.npy`
2. For each of 16 key bytes:
   - For each candidate `k` in 0..255:
     - Compute predicted HW(SBOX[pt ⊕ k]) for all traces
     - Correlate with each sample point
     - Select `k` with max absolute correlation
3. Verify boot key against known plaintext/ciphertext pairs
4. Derive Flag 1 key: `SHA-256("mohale-flag1|" + boot_key_hex)`
5. Decrypt `flag1.enc` (AES-GCM)
6. For firmware (with `--recover-firmware`):
   - Load `fw_pt.npy`, compute centered traces
   - For each byte position, evaluate all sample pairs `(i,j)` with 3-position sum
   - Select key byte with max correlation
7. Verify firmware key against known pairs
8. Derive Flag 2 key: `SHA-256("mohale-flag2|" + firmware_key_hex)`
9. Decrypt `flag2.enc` (AES-GCM)

---

## 6. Flags

### Flag 1 (VERIFIED)
```
LsCTF2026{b00tl04d3r_k3y_l34k3d_thr0ugh_th3_p0w3r_l1n3}
```

### Flag 2 (VERIFIED)
```
LsCTF2026{m4sk1ng_0nly_d3l4ys_th3_4tt4ck_t0_s3c0nd_0rd3r}
```

Both authenticated via AES-GCM tag checks.

---

## 7. Lessons Learned

1. **1st-order CPA breaks unmasked AES** — Hamming weight of S-box output correlates with power consumption.
2. **Boolean masking raises attack order** — 1st-order CPA fails; must use 2nd-order (products of centered samples).
3. **Timing jitter spreads leakage** — The 3-sample shift requires combining adjacent pair correlations to recover full signal.
3. **Correlation sign matters** — For 2nd-order CPA, retain signed correlations before combining/absolute.
4. **Authenticated decryption confirms keys** — AES-GCM tag verification on both flags proves key correctness.

---

## 8. Tools Used

- Python 3: `numpy` (trace loading, correlation), `pycryptodome` (AES-GCM), `hashlib`
- `solve.py` — Packaged solver (bootloader CPA by default; firmware with flag)
- Memory: ~1.5 GB for full firmware recovery

---

## 9. Evidence and References

- `evidence/extracted/handout/boot_traces.npy` — Bootloader traces
- `evidence/extracted/handout/boot_pt.npy` — Bootloader plaintexts
- `evidence/extracted/handout/fw_pt.npy` — Firmware plaintexts
- `evidence/extracted/handout/flag1.enc` / `flag2.enc` — Encrypted flags
- `solve.py` — Complete solver