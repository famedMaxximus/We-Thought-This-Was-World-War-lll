# Oil and Vinegar, Never Mixed

**Category:** Cryptography
**Difficulty:** Hard
**Points:** 500
**Status:** Solved (Verified)

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

### Stage 1 — Break the Device PRNG

The combiner output agrees with x2 75% of the time and with x3 75% of the time, so x2 and x3 can each be attacked by correlation on their own:

- **LFSR2 (L=21)**: scan all 2²¹ seeds, score agreement over 1024 bits → seed `0x1266f4` (1206004), 765/1024
- **LFSR3 (L=23)**: scan all 2²³ seeds → seed `0x7cf93f` (8190271), 773/1024
- **LFSR1 (L=19, selector)**: brute-force 2¹⁹ seeds, keeping the one that reproduces the full stream → seed `0x32939` (207161)

States `(207161, 1206004, 8190271)` reproduce all 4096 bits of `selftest.bin` exactly. `geffe.c` does the brute force (~73 s); a Gray-code walk (each LFSR's output is linear in its seed) brings it down to a few seconds.

### Stage 2 — Unmask the reports

`reports.bin` XOR keystream, with the keystream taken **after** the 512-byte self-test prefix (i.e. bytes `512 … 512+len(reports)` of the same stream), gives 96 **symmetric** 96×96 matrices — the device leaked its masked internal forms. `solve.py` asserts that the first 512 keystream bytes equal `selftest.bin` before using the rest.

> An earlier attempt recorded in this repository could not reproduce this step and listed it as a discrepancy. The full solver below does reproduce it from the original handout files.

### Stage 3 — Recover the oil space

O = ker(M27) ∩ ker(M29) = nullspace([M27; M29]) — exactly 24-dimensional, and every public form P_i vanishes on it (checked). "Oil hides where every public form vanishes together."

### Stage 4 — Unseal `sealed_a.enc`

secret = `serialize_matrix(RREF(O))` (canonical basis). This yields the message ("release 3 of 3 from the cold wallet to the bearer") and the vinegar vector v (96 field elements) to sign with.

### Stage 5 — Forge the signature

With O known, signing is linear: for s = v + o, o ∈ O,
P_i(v+o) = P_i(v) + vᵀ M_i o (since P_i(o) = 0, M_i = P_i + P_iᵀ).
Solve the 24×24 system vᵀ M_i o = target_i − P_i(v) over GF(16) for o ∈ O. The resulting s passes `uov.verify()`.

### Stage 6 — Unseal `flag.enc`

secret = `serialize_signature(s)` → the flag (AES-256-GCM, tag checked).

---

## 4. Vulnerability / Technical Discovery

| Component | Flaw |
|-----------|------|
| Device PRNG | 3 short LFSRs (19, 21, 23) with a Geffe correlated combiner → correlation attacks on each LFSR independently |
| UOV | Leaking matrices whose kernels intersect in the oil space gives away the secret key. Once O is known, signing is just linear algebra. |
| Decoys | Multiple fake flags in comments and hidden Unicode TAG characters (prompt injection for AI agents) |

---

## 5. Exploitation / Solution

```bash
cd "Oil and Vinegar, Never Mixed handout"   # uov.py, device_prng.py, *.bin, *.enc
python3 /path/to/solve.py
```

Output (reproduced from the original handout):

```
[*] LFSR states: (207161, 1206004, 8190271)
[*] oil space recovered (dim 24, verified)
[*] forged signature verifies
[+] FLAG: LsCTF2026{Kerne1_Intersecti0ns_Betray_The_0i1_Space_And_Signing_Is_1inear}
```

To recover the LFSR states from scratch instead of using the hard-coded ones: `gcc -O2 geffe.c -o geffe && ./geffe selftest.bin`.

---

## 6. Flag

```
LsCTF2026{Kerne1_Intersecti0ns_Betray_The_0i1_Space_And_Signing_Is_1inear}
```

**Verified:** the forged signature passes `uov.verify()`, and `flag.enc` decrypts under AES-256-GCM *authenticated* decryption (the tag check proves the key is correct).

---

## 7. Lessons Learned

1. **A device PRNG built from short LFSRs with a correlated (Geffe) combiner falls to correlation attacks** — anything masked with it is exposed.
2. **In UOV, leaking matrices whose kernels intersect in the oil space gives away the secret key** — once O is known, signing is just linear algebra.
3. **Don't trust "flags" in comments or hidden text** — confirm them with the crypto (the GCM tag).
4. **Get offsets exactly right** — the unmasking only works with the keystream continued past the 512-byte self-test.

---

## 8. Tools Used

- C (`geffe.c`, LFSR state brute force)
- Python 3 + NumPy, `pycryptodome` (AES-GCM via the handout's `uov.unseal`)

---

## 9. Evidence and References

- `solve.py` — full reproducible solver (run inside the handout dir; ~2 s)
- `geffe.c` — brute-force recovery of the 3 LFSR states from `selftest.bin`
- `evidence/README.md` — handout file list
