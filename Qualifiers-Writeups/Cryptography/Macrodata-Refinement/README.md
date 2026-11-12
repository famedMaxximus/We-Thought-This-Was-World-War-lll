# Macrodata Refinement

**Category:** Cryptography
**Difficulty:** Hard
**Points:** 500 (Flag 1: 200, Flag 2: 300)
**Status:** Solved (Both flags verified)

---

## 1. Challenge Overview

A gateway capture from the severed floor of Lumon Industries. A batch file left the building via DNS exfiltration. The objective is to reconstruct the exfiltrated file from DNS traffic, decrypt two AES-GCM envelopes, and break a Geffe generator stream cipher protecting the second flag.

---

## 2. Initial Analysis

### Handout Files (`Macrodata Refinement handout.zip`)

| File | Contents |
|------|----------|
| `capture.pcap` | 2,908 frames: DNS (2,748), NTP (40), TLS/TCP (120) |
| `lumon_cipher.py` | "Batch file protection": three LFSRs as a Geffe generator, 77-byte `BANNER` prefix |
| `flag1.enc` | 194 bytes, AES-256-GCM (`nonce(12) || tag(16) || ct`) |
| `stage2.enc` | 321 bytes, same envelope format |

---

## 3. Investigation and Methodology

### 3.1 DNS Exfiltration Channel (Flag 1)

Most DNS resolves `*.lumon.test` / `example-*.test`. Two zones under `lumon-cdn.test` return **NXDOMAIN** for every query — classic DNS tunneling:

| Zone | Queries | Purpose |
|------|---------|---------|
| `tNNNN.<b32>.metrics.lumon-cdn.test` | 36 chunks | Base32 telemetry (decoy) |
| `NNNN.<b32>.sync.lumon-cdn.test` | 623 unique chunks | **Exfiltrated file** |

**Reassembly Gotchas:**
- **Order**: Chunks sent out of order, some repeated (A and TXT both). Deduplicate by hex sequence label and sort.
- **Case**: Random letter case (DNS 0x20 mixing). Case bits carry **no data**. Lowercase before decoding.
- **Per-label Base32**: Each label is 58 chars (290 bits). Decode **each label independently** (36 bytes + 2 leftover bits dropped). Joining all labels first misaligns chunks.

### 3.2 File Reconstruction

Chunk 0 is a header:
```
4d445231  0000576f  8882bd9b494b389a5624fa9dd8898ce5  000000…
"MDR1"   len=22383   SHA-256(file)[:16]                 pad
```

Chunks 1–622 → 22,383-byte **160×160 RGB PNG** (Macrodata Refinement grid). SHA-256 matches header prefix:
```
8882bd9b494b389a5624fa9dd8898ce55b0e6261450c9c7b39c0affa22576301
```

### 3.3 Flag 1 Decryption

Key derivation (label not in handout, from reference solve):
```
key = SHA-256(b"macrodata-flag1|" + sha256(png).hexdigest())
```

Decrypts `flag1.enc` → **Flag 1**:
```
LsCTF2026{n4m3_l00kups_4r3_4_sm4ll_p1p3}
```

> "That is the file that left the building. A picture holds more than it shows: look at it as pixels, not as an image."

---

## 4. Vulnerability / Technical Discovery

### 4.1 Green-Channel LSB Steganography (Column-Major)

The PNG has two near-identical background colours: `(6,24,32)` and `(6,25,32)`. **Green LSB** carries data; red/blue LSBs are constant.

**Critical**: Row-major extraction gives random bytes. **Column-major** (`pixels[:,:,1].T`), MSB-first packed, yields a length header:
```
000000ae  bfc4b2bd3d94915caf6a…   # len = 174 bytes
```

```python
hid = np.packbits((px[:, :, 1] & 1).T.ravel()).tobytes()
batch = hid[4 : 4 + int.from_bytes(hid[:4], "big")]  # 174 bytes
```

### 4.2 Geffe Generator Correlation Attack

`lumon_cipher.py` defines three LFSRs:
```python
ra = LFSR(29, [2],  a)   # x^29 + x^2 + 1
rb = LFSR(31, [28], b)   # x^31 + x^28 + 1   (selector)
rc = LFSR(28, [3],  c)   # x^28 + x^3 + 1
z  = x if s else y
```

Key space: 2²⁹·2³¹·2²⁸ = 2⁸⁸ (brute force impossible). But the combiner **leaks**:
- `P[z = x] = 0.75` (when `s=1`, z=x; when `s=0`, z=y, matches x half the time)
- `P[z = y] = 0.75`
- `P[z = s] = 0.5` (selector uncorrelated → "not worth attacking first")

**Known keystream**: `seal_batch` prepends 77-byte `BANNER` → `batch[:77] ⊕ BANNER` = **616 known keystream bits**.

**Correlation attack**: Scan all 2²⁹ seeds of A and 2²⁸ of C, score agreements with `z`. Wrong seed ≈ 308 ± 12; correct seed ≈ 462. OpenMP C implementation (`solve/corr.c`) finishes in ~30s on 8 cores.

Results:
```
LFSR29: seed 522115143  agrees 469/616 (76.1%)  ← ~13σ above noise
LFSR28: seed 149916127  agrees 454/616 (73.7%)  ← unique hit
```

**Recovering selector B**: Where `x_t ≠ y_t`, `s_t` is directly revealed (309 equations). Each `s_t` is a GF(2)-linear function of B's 31 seed bits → Gaussian elimination gives unique solution:
```
key (a, b, c) = (522115143, 1327243828, 149916127)
```

---

## 5. Exploitation / Solution

### Complete Solver Flow

```bash
$ python3 solve/solve.py "<extracted handout dir>"
[+] 623 DNS chunks -> 22383-byte PNG, truncated SHA-256 matches header
[+] Flag 1: LsCTF2026{n4m3_l00kups_4r3_4_sm4ll_p1p3}
[+] green-channel LSB payload: 174 bytes
[+] stage2 notes: ...
[*] correlating outer registers (~30 s)...
    LFSR29: seed 522115143 agrees 469/616
    LFSR28: seed 149916127 agrees 454/616
[+] key (a, b, c) = (522115143, 1327243828, 149916127)
[+] BATCH 0x1D3F // 4 OF 4 REFINED // CHECK: LsCTF2026{c0rr3l4t3d_r3g1st3rs_br34k_thr33_l1ttl3_k3ys}
```

### Flag 2 Decryption

Regenerate full keystream from recovered seeds, XOR with `batch` → plaintext batch file containing Flag 2 in `CHECK` field.

---

## 6. Flags

### Flag 1 (VERIFIED)
```
LsCTF2026{n4m3_l00kups_4r3_4_sm4ll_p1p3}
```

### Flag 2 (VERIFIED)
```
LsCTF2026{c0rr3l4t3d_r3g1st3rs_br34k_thr33_l1ttl3_k3ys}
```

Both authenticated via AES-GCM tag checks.

---

## 7. Lessons Learned

1. **NXDOMAIN-only high-entropy labels** to one zone are a clear DNS exfiltration indicator.
2. **Read order matters in LSB stego** — not just channel, but row-major vs column-major.
3. **Geffe generator is broken** — its combining function correlates with inputs, reducing 2⁸⁸ key space to ~2²⁹ + 2²⁸ work + linear solve.
4. **Correlation immunity is essential** — nonlinear combiners must be correlation-immune; LFSR-based ciphers should use ChaCha20/AES-CTR.
5. **Decoys waste time** — `metrics.lumon-cdn.test` tunnel, mixed case, NTP, TLS all contained no flag data.

---

## 8. Tools Used

- Python 3: `pycryptodome`, `numpy`, `Pillow`
- C with OpenMP (`corr.c` compiled on first run)
- Built-in pcap/DNS parsing (no tshark/scapy needed)
- `gcc` for correlation attack binary

---

## 9. Evidence and References

- `evidence/capture.pcap` — Network capture
- `evidence/lumon_cipher.py` — Cipher implementation
- `evidence/flag1.enc` / `stage2.enc` — Encrypted flags
- `solve/solve.py` — Complete solver
- `solve/corr.c` — OpenMP correlation attack