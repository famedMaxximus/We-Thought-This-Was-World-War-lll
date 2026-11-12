# Enkapune 2 – The Cleanup Assignment

**Category:** Cryptography
**Difficulty:** Easy
**Points:** 100
**Status:** Solved (Verified)

---

## 1. Challenge Overview

RSA + XOR challenge. The handout contains multiple files with fake flags and a Wiener's attack on RSA with a large public exponent.

---

## 2. Initial Analysis

### Files (`enkapune-sacco-challenge-2.zip`)

| File | Content |
|------|---------|
| `.ledger_shadow` | `pad_hex=...` (616 bytes) |
| `ear_tags/Tag-{A,B,C,D}_checksum.dat` | 512 bits of hex each |
| `guarantor_walk.txt` | Order: `C A D B` |
| `pasture_map.png` | PNG header + IEND + text between `--ENK-DESK-CIPHER--` and `--END--` |

---

## 3. Investigation and Methodology

### 3.1 Fake Flags (Decoys)

Every file has a fake flag in comments:
- `sh0rt_3_is_n0t_alw4ys_th3_w4y`
- `n0t_th3_dr0ught_l0an_st4mp`
- `w13n3r_w4s_t00_0bvi0us`
- `f4k3_m0dulus_try_f4ct0rdb`
- Plus Base32 "bait" strings

Two are useful hints: *"short 3 is not always the way"* (e is not small) and *"Wiener"*

### 3.2 Ciphertext

`pasture_map.png` is a PNG header, an `IEND` chunk, and then text between `--ENK-DESK-CIPHER--` and `--END--`. That text is the **2048-bit RSA ciphertext `c` in hex**.

### 3.3 Modulus

Joining the four tag values in the order from `guarantor_walk.txt` (C, A, D, B) gives the **2048-bit modulus `N`**.

### 3.4 Public Exponent

`pad_hex` is 616 bytes = length of a 2048-bit number in decimal. It is XOR-encrypted with a repeating 8-byte key. Requiring every decoded byte to be an ASCII digit narrows each key byte to two choices; the key is `encapune`. The decoded decimal number is the public exponent `e`.

### 3.5 Wiener's Attack

`e` is about as large as `N`, so the private exponent `d` is probably small.

Continued-fraction expansion of `e/N` gives:
```
d = 1172615391623919965125441
m = pow(c, d, N)  →  LsCTF2026{rsa_encryption_IS_Me@nt_k33p_everything_S@f3}
```

---

## 4. Vulnerability / Technical Discovery

| Component | Flaw |
|-----------|------|
| RSA | Public exponent `e` ≈ `N` → small private exponent `d` → Wiener's attack (continued fractions) |
| XOR encryption | Repeating 8-byte key `encapune`; ASCII digit constraint reduces key space to 2⁸ = 256 |

---

## 5. Exploitation / Solution

### Solve Script

```python
import re
from gmpy2 import mpz, powmod, is_square

pad = bytes.fromhex(re.search(r'pad_hex=(\w+)', open('.ledger_shadow').read()).group(1))
c = int(re.search(rb'CIPHER--\n(\w+)', open('pasture_map.png', 'rb').read()).group(1), 16)
tag = {t: re.search(r'checksum_hex=(\w+)', open(f'ear_tags/Tag-{t}_checksum.dat').read()).group(1) for t in 'ABCD'}

N = mpz(int(''.join(tag[t] for t in 'CADB'), 16))
key = b'encapune'
e = mpz(int(bytes(b ^ key[i % 8] for i, b in enumerate(pad))))

def cf(a, b):
    while b:
        q = a // b
        yield q
        a, b = b, a - b * q

def wiener(e, n):
    h0, h1, k0, k1 = 0, 1, 1, 0
    for q in cf(e, n):
        h0, h1 = h1, q * h1 + h0
        k0, k1 = k1, q * k1 + k0
        k, d = h1, k1
        if k == 0 or (e * d - 1) % k:
            continue
        phi = (e * d - 1) // k
        s = n - phi + 1
        D = s * s - 4 * n
        if D >= 0 and is_square(D):
            return d

d = wiener(e, N)
m = int(powmod(c, d, N))
print(m.to_bytes((m.bit_length() + 7) // 8, 'big').decode())
```

---

## 6. Flag

```
LsCTF2026{rsa_encryption_IS_Me@nt_k33p_everything_S@f3}
```
(Verified by successful RSA decryption)

---

## 7. Lessons Learned

1. **Wiener's attack** — When `e` is large (≈ N), `d` is small. Continued fractions of `e/N` recover `d` efficiently.
2. **Repeating-key XOR with constraints** — If plaintext is known to be ASCII digits, each key byte has only 2 possibilities (digit ⊕ ciphertext_byte). Brute-forcing 2⁸ = 256 keys is trivial.
3. **Fake flags as hints** — Decoy flags often contain hints about the solution method ("short 3 is not always the way" → e not small; "Wiener" → Wiener's attack).
4. **File carving** — The ciphertext was hidden in a PNG after the IEND chunk.

---

## 8. Tools Used

- Python 3 with `gmpy2` (for large integer arithmetic and `is_square`)
- `re` for parsing
- File carving (manual or scripted)

---

## 9. Evidence and References

- `evidence/.ledger_shadow` — XOR-encrypted public exponent
- `evidence/pasture_map.png` — PNG with ciphertext after IEND
- `evidence/ear_tags/` — Modulus fragments
- `evidence/guarantor_walk.txt` — Fragment order