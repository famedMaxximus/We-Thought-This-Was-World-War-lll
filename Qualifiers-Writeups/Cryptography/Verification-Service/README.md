# Verification Service

**Category:** Cryptography
**Difficulty:** Hard
**Points:** 500
**Status:** Solved (Verified)

---

## 1. Challenge Overview

A service went public with its setup, one ciphertext it had issued, and a table it described as routine bookkeeping. Its operators say nothing sensitive was ever exposed. The flag is behind that claim.

---

## 2. Initial Analysis

### Handout

| File | Content |
|------|---------|
| `service.py` | `unseal(name, secret, blob)`: AES-GCM, nonce=blob[:12], tag=blob[12:28], ct=blob[28:], key = sha256(LABEL + b"|" + str(secret).encode()); LABELS: `payload.enc` → `chal6-payload`, `flag.enc` → `chal6-final` |
| `params.txt` | `{q=3329, n=192, m=300, A: 300×192, u: 300}` (u = A s + e) |
| `ciphertext.txt` | `{bits=128, ct: 128 × (a: 192-vector, b: int)}` |
| `verification.txt` | `{checks: 192 × {c: 192-vector, v: int}}` |
| `payload.enc` | 3167 bytes |
| `flag.enc` | 108 bytes |

### Traps / Decoys

- `params.txt` `build_tag`: `LsCTF2026{ha_ke_karabo_ea_nnete_lwe_leka_hape}` (visible decoy)
- `verification.txt` `service_note`: `LsCTF2026{ver1fication_test_run_n0t_the_f1ag}` (visible decoy)
- **Invisible Unicode TAG characters** (U+E0000..E007F) in every text file — prompt injection claiming "pre-solved" with fake flag `LsCTF2026{the_secret_was_a1l_zer0s_said_the_ai_and_1ied}`. Strip before `json.loads()`.

---

## 3. Investigation and Methodology

### Step 1 — The "Routine Bookkeeping" Leak

Regev/LWE setup: secret `s` in Z_q^192 with small coefficients, public key `(A, u = A s + e)`, q = 3329 (Kyber prime).

Verification table gives 192 pairs `(c_i, v_i)`. Gaussian elimination mod q shows:
- `rank(C) = 80`
- `rank([C | v]) = 80` → **consistent**, i.e. `v_i = ⟨c_i, s⟩ EXACTLY` (no noise at all)

The table does not hand over `s` directly (naive 192×192 solve reports "singular"). But it fixes 80 linear combinations of `s`, leaving **112 free coordinates**.

Row-reducing `[C | v]` gives pivot columns P (80) and free columns F (112):
```
s_P = rhs - R * s_F   (mod q)
```
Particular solution: `s0` with `s0_F = 0`, `s0_P = rhs`.

### Step 2 — Lattice: s is the Unique Short Vector

Every solution is `s = s0 - x` with `x ∈ L = { x ∈ Z^192 : C x = 0 mod q }`.

Basis of L (192 × 192):
- For each free j: `e_j - Σ_i R[i][j] * e_{P_i}` (mod q)
- For each pivot i: `q * e_{P_i}`

**Kannan embedding**: Append the row `(s0 | 1)`. Then `(s | 1)` lies in the 193-dimensional lattice and is extremely short:
- `det(L) = q^80` → Gaussian heuristic ~ √(192/(2πe)) * q^(80/192) ~ 3.36 * 29.4 ~ 99
- `||s||` with coeffs in [-2,2] ~ 13-15

Large gap → plain LLL (fpylll) finds it in ~1 second. Pick reduced row whose last coordinate is ±1 and fix sign → `s`.

**Checks on recovered s:**
- All 192 bookkeeping equations hold exactly
- `u - A s` has every coefficient in [-2, 2] → real LWE secret, real error

**Point of challenge**: Hints that are each "harmless" and rank-deficient still shrink the LWE dimension (192 → 112) enough for lattice reduction to break it.

### Step 3 — Regev Decryption → Unseal payload.enc

Each ciphertext `(a, b)` encrypts one bit:
```
d = b - ⟨a, s⟩ mod q
bit = 1 if q/4 < d < 3q/4 else 0
```

128 bits (MSB-first):
```
1001111010000001010111110111010110001101101000101111100001000100
0111111110001111101010000110100101000000000011010000100011110011
= 0x9e815f758da2f8447f8fa869400d08f3
```

`unseal("payload.enc", secret)` works when secret is the **32-char lowercase hex string** `"9e815f758da2f8447f8fa869400d08f3"`. (Decimal int and MSB/LSB variants fail GCM tag.)

Payload is JSON:
```json
{"N": <2048-bit>, "e": 17, "a": ..., "b": ..., "c1": ..., "c2": ...}
```

### Step 4 — Franklin-Reiter Related-Message Attack

`c1 = m^17 mod N` and `c2 = (a*m + b)^17 mod N`, with `a` and `b` known.

`m` is a common root of:
```
f1(x) = x^17 - c1
f2(x) = (a x + b)^17 - c2        over Z_N[x]
```
So `gcd(f1, f2) = (x - m)` (up to scalar). Euclid's algorithm on degree-17 polynomials mod N (leading-coefficient inverses mod N always exist here) gives `g = g1*x + g0`, so `m = -g0 / g1 mod N`.

Checked: `pow(m,17,N) == c1` and `pow(a*m+b,17,N) == c2`.

### Step 5 — Unseal the Flag

`unseal("flag.enc", m)` with secret = `str(m)` (decimal):

```
LsCTF2026{Rank_Deficient_Hints_Shrink_The_1attice_Then_Frank1in_Reiter_Finishes}
```
(GCM tag verified → plaintext authentic)

---

## 4. Vulnerability / Technical Discovery

| Layer | Primitive | Flaw |
|-------|-----------|------|
| LWE | Regev encryption | Rank-deficient but noise-free linear leaks (80/192) → dimension 192→112; small secret falls to LLL |
| RSA | Small exponent (e=17) | Affinely related messages → Franklin-Reiter GCD attack |
| AES-GCM | Key derivation | Label + secret string; tag verification prevents false positives |

---

## 5. Exploitation / Solution

### Reproduce

```bash
python3 -m venv venv && venv/bin/pip install fpylll cysignals pycryptodome
venv/bin/python scripts/solve.py "extracted/Verification Service handout"
```

Runs whole chain end-to-end (~1s):
```
[+] leaked checks: rank 80/192, consistent (noiseless) -> 112 free coordinates
[+] verified: all 192 checks hold; public-key errors in [-2, 2]
[+] decrypted bits: 1001111010000001...
[+] payload.enc unsealed with '9e815f758da2f8447f8fa869400d08f3' -> RSA stage: e=17, ...
[+] Franklin-Reiter recovered m (verified against c1 and c2)
[+] FLAG: LsCTF2026{Rank_Deficient_Hints_Shrink_The_1attice_Then_Frank1in_Reiter_Finishes}
```

---

## 6. Flag

```
LsCTF2026{Rank_Deficient_Hints_Shrink_The_1attice_Then_Frank1in_Reiter_Finishes}
```
(Verified via AES-GCM tag on `flag.enc`)

---

## 7. Lessons Learned

1. **Never publish exact (noise-free) linear functions of an LWE secret** — Even rank-deficient leaks reduce the effective dimension, and small secrets then fall to lattice reduction.
2. **Never encrypt affinely related messages under small-exponent RSA without randomized padding** — Franklin-Reiter attack recovers the message directly.
3. **Don't trust "flags" in comments or hidden text** — Verify with the crypto (here, the AES-GCM tag).

---

## 8. Tools Used

- Python 3: `fpylll` (LLL), `cysignals`, `pycryptodome` (AES-GCM)
- `scripts/solve.py` — End-to-end solver

---

## 9. Evidence and References

- `evidence/params.txt` — LWE parameters
- `evidence/ciphertext.txt` — Regev ciphertexts
- `evidence/verification.txt` — Rank-deficient noiseless leaks
- `evidence/payload.enc` / `flag.enc` — AES-GCM envelopes
- `scripts/solve.py` — Complete solver