# Everything, Almost

**Category:** Cryptography
**Difficulty:** Hard
**Points:** Unknown
**Status:** Solved (Both flags verified)

---

## 1. Challenge Overview

An NTRU-like cryptosystem over the negacyclic ring `Z_3329[x] / (x^256 + 1)` with `p = 3` and ternary private polynomials. The leak supplies 240 coefficients of `f`, leaving 16 unknown values in `{-1, 0, 1}`.

---

## 2. Initial Analysis

### Public Key

```
h = 3 * g * f^(-1) mod 3329
```

### Leak

240 coefficients of `f` known, 16 unknown in `{-1, 0, 1}`. The correct completion satisfies `f * h mod 3329` in `{0, 3, 3326}` coefficient by coefficient.

---

## 3. Investigation and Methodology

### Meet-in-the-Middle on Unknown Coefficients

Split the 16 unknowns into two groups of eight. Enumerate the `3^8 = 6561` assignments in each group and compute their contributions to the first two coefficients of `f * h`.

Hash one side by those two modular values. For each assignment on the other side, try the nine possible target pairs from `{-3, 0, 3}^2`, then check every coefficient of each matched candidate.

This recovers a full valid private polynomial `f` without enumerating all `3^16` completions.

### Flag 1

Authenticated AES-GCM decryption of `flag1.enc` with:
```
SHA-256("everything-flag1|" + comma_separated_signed_coefficients(f))
```

### Recover `g`

Center `f * h` modulo 3329 and divide by three to recover ternary `g`.

### Stage 3 / Flag 2

Decrypt `stage3.enc` using same serialization with prefix `everything-stage3|`. Its notes confirm the NTRU decryption steps:

```
a = center_3329(f * e)
m = center_3(f^(-1) * a mod 3)
```

All products use `x^256 = -1`. Compute the inverse of `f` modulo three and recover the ternary message polynomial `m`.

Finally decrypt `flag.enc` with:
```
SHA-256("everything-final|" + comma_separated_signed_coefficients(m))
```

Both flag envelopes and the intermediate note authenticate successfully.

---

## 4. Vulnerability / Technical Discovery

| Component | Flaw |
|-----------|------|
| Partial key leak | 240/256 coefficients of `f` leaked → only 16 unknown ternary coefficients |
| Meet-in-the-middle | 16 unknowns split into 2×8 → `3^8 + 3^8` work instead of `3^16` |
| NTRU structure | `f * h = 3g` reveals `g` once `f` is known; decryption is standard NTRU |

---

## 5. Exploitation / Solution

```bash
python3 solve.py --challenge everything
```

Reproduces: `f` recovery → Flag 1 → `g` recovery → `stage3.enc` note → `m` recovery → Flag 2.

---

## 6. Flags

### Flag 1 (VERIFIED)
```
LsCTF2026{m1ss1ng_c03ff1c13nts_4r3_just_4_cvp}
```

### Flag 2 (VERIFIED)
```
LsCTF2026{4lm0st_3v3ryth1ng_1s_3n0ugh}
```

Both authenticated via AES-GCM tag checks.

---

## 7. Lessons Learned

1. **Partial key exposure in structured lattices** — Even a small number of unknown coefficients (16) in a ternary polynomial can be recovered via meet-in-the-middle when the public key provides verification equations.
2. **NTRU decryption is standard** — Once `f` and `g` are known, decryption follows the textbook algorithm.
3. **Authenticated decryption at every stage** — Each envelope (flag1, stage3, flag) has an AES-GCM tag, confirming correctness at each step.
4. **Negacyclic ring arithmetic** — `x^256 = -1` (mod `x^256 + 1`) is the defining relation; all polynomial products respect this.

---

## 8. Tools Used

- Python 3: `pycryptodome` (AES-GCM), `hashlib`
- Polynomial arithmetic over `Z_3329[x] / (x^256 + 1)` and `Z_3[x] / (x^256 + 1)`
- `solve.py` — Packaged solver

---

## 9. Evidence and References

- `evidence/handout/` — Public key, leak, encrypted flags
- `solve.py` — Complete solver with meet-in-the-middle and NTRU decryption