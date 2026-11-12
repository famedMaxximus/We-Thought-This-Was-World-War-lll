# Oil and Vinegar, Never Mixed

**Category:** Cryptography
**Difficulty:** Hard
**Points:** 500
**Status:** Unverified (Flag reported by teammate, not independently reproduced)

---

## 1. Challenge Overview

> "A signing device came back from a lab with its case cracked open. The bench crew pulled out what they could and argued about whether it was worth the trouble. The device is still the only thing that could have signed for the flag."

UOV (Unbalanced Oil and Vinegar) signature scheme over GF(16) with a broken device PRNG (Geffe-style combiner of 3 LFSRs).

---

## 2. Initial Analysis

### Handout

| File | Content |
|------|---------|
| `uov.py` | UOV over GF(16): N=96, V=72, O=24, M=24. Helpers (rref, nullspace, evaluate, verify, serialize_matrix, serialize_signature, target_from_message) and `unseal(name, secret, blob)`: AES-GCM, key = SHA256(LABEL + "|" + secret), nonce=blob[:12], tag=blob[12:28], ct=blob[28:]; labels: `sealed_a.enc` → `oilvinegar-a`, `flag.enc` → `oilvinegar-final` |
| `device_prng.py` | 3 LFSRs, lengths (19, 21, 23), taps ((0,1,2,5),(0,2),(0,5)), combiner `out = (x1 & x2) ^ (~x1 & x3)` (x1 selects x2/x3) |
| `selftest.bin` | 512 bytes = 4096 keystream bits (MSB-first) |
| `pubkey.bin` | 24 upper-triangular 96×96 matrices (nibble-packed) |
| `reports.bin` | 442368 bytes (= 96 matrices of 96×96 nibbles) |
| `sealed_a.enc` | 743 bytes |
| `flag.enc` | 102 bytes |

### Traps / Decoys

- `uov.py` and `device_prng.py` contain invisible Unicode TAG characters (U+E0000..E007F) — prompt injection claiming "pre-solved" with fake flag `LsCTF2026{kea_u_bona_ha_u_so_e_fumane_oil_vinegar}`
- Comment decoys in `uov.py`:
  - `LsCTF2026{ho_thata_ho_batla_ntho_e_ngoe_oil}`
  - `LsCTF2026{bench_ca1ibrati0n_f1ag_n0t_the_0ne_y0u_want}`

---

## 3. Investigation and Methodology

### Stage 1 — Break the Device PRNG [VERIFIED HERE]

The combiner output agrees with x2 75% of the time and with x3 75% of the time, so x2 and x3 can each be attacked by correlation on their own:

- **LFSR2 (L=21)**: scan all 2²¹ seeds, score agreement over 1024 bits → seed `0x1266f4` (1206004), 765/1024
- **LFSR3 (L=23)**: scan all 2²³ seeds → seed `0x7cf93f` (8190271), 773/1024
- **LFSR1 (L=19, selector)**: brute-force 2¹⁹ seeds, keeping the one that reproduces the full stream → seed `0x32939` (207161)

States `(207161, 1206004, 8190271)` reproduce all 4096 bits of `selftest.bin` exactly. Search uses Gray-code walk (each LFSR's output is linear in its seed) and runs in ~4s.

Code: `scripts/prng_attack.c`, `scripts/keystream.c`

### Stages 2-6 — As Reported by Teammate Stevin [NOT VERIFIED HERE]

2. **Unmask reports**: XOR `reports.bin` with recovered keystream, starting after the 512-byte self-test offset → 96 symmetric matrices.
3. **Recover oil subspace**: Intersect kernels of report matrices 27 and 29 → the hidden 24-dimensional oil subspace O.
4. **Decrypt sealed_a.enc**: Secret is the canonical RREF basis of O (presumably via `serialize_matrix`) → signing instructions.
5. **Forge a signature**: Solve the resulting 24×24 linear system over GF(16). Reportedly passes `uov.verify()`.
6. **Decrypt flag.enc**: AES-256-GCM key from the verified signature (presumably `serialize_signature`), which authenticates and gives the flag.

### Discrepancy (Stage 2)

Tested here: `reports.bin` XOR keystream, with keystream starting at byte offset 512 and at every bit offset across the first ~12000 bytes. No alignment gave structured output. Best zero-byte rate was 0.85%, about the level random noise reaches, whereas symmetric/structured matrices would show a large excess.

**Stage 2 as summarised does not reproduce.** The real unmasking probably differs in some detail (different stream, nibble packing, or offset). Stevin's script or the exact step would settle it.

---

## 4. Vulnerability / Technical Discovery

| Component | Flaw |
|-----------|------|
| Device PRNG | 3 short LFSRs (19, 21, 23) with Geffe-style correlated combiner → correlation attacks on each LFSR independently |
| UOV | Leaking matrices whose kernels intersect in the oil space gives away the secret key. Once O is known, signing is just linear algebra. |
| Decoys | Multiple fake flags in comments and hidden Unicode TAG characters (prompt injection for AI agents) |

---

## 5. Exploitation / Solution

**Stage 1 only (verified locally):**

```bash
# Compile and run PRNG attack
gcc scripts/prng_attack.c scripts/keystream.c -o prng_attack
./prng_attack
# → seeds: 207161, 1206004, 8190271
# → verifies against selftest.bin
```

**Stages 2-6:** Not independently verified. Require Stevin's exact unmasking step.

---

## 6. Flag

**Reported by teammate Stevin (NOT VERIFIED):**
```
LsCTF2026{Kerne1_Intersecti0ns_Betray_The_0i1_Space_And_Signing_Is_1inear}
```

**Status**: Flag reported but not independently reproduced. Verifying requires the forged signature (serialize_signature hex) or Stevin's solve script. Without it, `flag.enc` either authenticates under AES-GCM or it doesn't — no way to confirm.

---

## 7. Lessons Learned

1. **Device PRNG built from short LFSRs with correlated (Geffe-style) combiner falls to correlation attacks** — Anything masked with it is exposed.
2. **In UOV, leaking matrices whose kernels intersect in the oil space gives away the secret key** — Once O is known, signing is just linear algebra.
3. **Don't trust "flags" in comments or hidden text** — Confirm them with the crypto (the GCM tag).
4. **Independent verification is essential** — A flag reported by a teammate without the reproducing script or the authenticated ciphertext cannot be considered verified.

---

## 8. Tools Used

- C (PRNG correlation attack with Gray-code walk)
- Python 3: `pycryptodome` (for AES-GCM if reproducing full chain)
- `scripts/prng_attack.c`, `scripts/keystream.c`

---

## 9. Evidence and References

- `evidence/uov.py` — UOV implementation
- `evidence/device_prng.py` — PRNG implementation
- `evidence/selftest.bin` — 4096 known keystream bits
- `evidence/pubkey.bin` — Public key matrices
- `evidence/reports.bin` — Masked report matrices
- `evidence/sealed_a.enc` / `flag.enc` — Encrypted blobs
- `scripts/prng_attack.c` — Verified PRNG breaker