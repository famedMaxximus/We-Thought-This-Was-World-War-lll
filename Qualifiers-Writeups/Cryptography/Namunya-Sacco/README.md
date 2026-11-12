# Namunya Sacco

**Category:** Cryptography
**Difficulty:** Easy
**Points:** 100
**Status:** Solved (Verified)

---

## 1. Challenge Overview

You're covering Namunya Sacco on the night desk. Incident INC-40117 attaches last night's export. The day shift needs a token believed to sit inside that log. You have the tooling that produced the dump; not the key that sealed it.

---

## 2. Initial Analysis

### Handout (`namunya sacco.zip`)

| File | Content |
|------|---------|
| `chall.py` | The encryptor (from-scratch AES-128-CBC with custom S-box) |
| `output.txt` | `iv`, `check = sha256(flag)`, ~3.4 KB `ct` |

### Encryption Scheme

- Custom AES-128 in CBC mode with PKCS#7 padding
- Key and IV are random
- Plaintext structure:
  ```
  HEADER = b"NAMUNYA//SECLOG\n"   # exactly one 16-byte block
  pt = pkcs7(HEADER + message_with_flag)
  ```

- Round structure, key schedule, ShiftRows, MixColumns are standard
- **S-box is custom** (not AES's inversion in GF(2⁸))

---

## 3. Investigation and Methodology

### 3.1 S-box Analysis

AES's security comes from the S-box's non-linearity (inversion in GF(2⁸)). This custom S-box was tested:

```python
all(S[a ^ b] == S[a] ^ S[b] ^ S[0] for a in range(256) for b in range(256))  # True
```

**The S-box is affine over GF(2).**

### 3.2 Full Cipher Collapse

With an affine S-box, every step (SubBytes, ShiftRows, MixColumns, AddRoundKey, key schedule) is affine over GF(2). The entire block cipher collapses to:

```
E_k(x) = L · x  ⊕  C_k
```

Where `L` is a fixed 128×128 bit matrix (independent of key), and only `C_k` depends on the key.

---

## 4. Vulnerability / Technical Discovery

**All of AES's security comes from the non-linear S-box.** Swapping in an affine S-box reduces the cipher to a matrix multiply plus a key-dependent constant. One known plaintext block then decrypts everything — **no key recovery needed**.

---

## 5. Exploitation / Solution

### Attack Steps

1. **Recover `L`**: Encrypt with all-zero key: `L·eⱼ = E_0(eⱼ) ⊕ E_0(0)` for each of 128 unit vectors `eⱼ`.

2. **Cancel the key using known header**: CBC's first block encrypts `x₀ = HEADER ⊕ IV` (both known). With `c₀ = E_k(x₀)`, any block satisfies:
   `E_k(x) ⊕ c₀ = L·(x ⊕ x₀)`, so `x = L⁻¹(c ⊕ c₀) ⊕ x₀`.

3. **Undo CBC**: `Pᵢ = x_i ⊕ C_{i-1}` (using IV for first block), then strip padding.

4. **Compute `L⁻¹`** via Gaussian elimination over GF(2) (128 basis vectors packed as Python ints).

### Solver (`solve.py`)

```bash
cd handout && python3 ../solve.py .
```

Imports the challenge's own `encrypt_block`, builds `L` from it, decrypts every block, prints the log, and checks each candidate against the SHA-256.

---

## 6. Flag

The decrypted log contains multiple flag-shaped strings (decoys):

| Entry | String | Why Wrong |
|-------|--------|-----------|
| [2] | `LsCTF2026{w3lc0me_t0_m4th_1n_s3cur1ty}` | `m4th` |
| [4] | `LsCTF2026{w3lc0me_t0_math_1n_s3cur1ty}` (VERIFIED) | wrong year (2025) |
| [6] | `LsCTF2026{w3lcome_t0_math_1n_s3cur1ty}` | `o` instead of `0` |
| **[7]** | **`LsCTF2026{w3lc0me_t0_math_1n_s3cur1ty}`** | **matches `check`** |
| [8] | `flag{linear_algebra_is_not_a_security_model}` | wrong format (hint) |
| [9] | `LsCTF2026{n1c3_try_but_n0t_th1s_0n3}` | base64 decoy |
| [10] | `lsctf2026{…}` | lowercase prefix |
| [11] | `picoCTF{…}` | wrong format |
| [12] | `LsCTF2026{w3lc0me_t0_math_1n_s3cur1ty!}` | trailing `!` |

`output.txt` includes `check = sha256(flag)`. Solver hashes every `LsCTF2026{…}` candidate and keeps only the match:
```
FLAG LsCTF2026{w3lc0me_t0_math_1n_s3cur1ty} check ok
```

**Verified Flag:**
```
LsCTF2026{w3lc0me_t0_math_1n_s3cur1ty}
```

---

## 7. Lessons Learned

1. **AES security = S-box non-linearity** — The entire cipher's security rests on the S-box being non-linear (inversion in GF(2⁸)). An affine S-box collapses AES to a linear map.
2. **One known plaintext block breaks affine ciphers** — With `HEADER` known and fixed, the key-dependent constant cancels out.
3. **Custom crypto is fragile** — Small deviations from standard primitives (like a custom S-box) can catastrophically break security.
4. **Always verify against provided checksums** — The `check = sha256(flag)` in `output.txt` definitively identifies the real flag among decoys.

---

## 8. Tools Used

- Python 3 (stdlib only — Gaussian elimination over GF(2) with packed ints)
- `chall.py` (imported for `encrypt_block`)

---

## 9. Evidence and References

- `evidence/chall.py` — Encryptor source
- `evidence/output.txt` — IV, SHA-256 check, ciphertext
- `solve.py` — Complete solver