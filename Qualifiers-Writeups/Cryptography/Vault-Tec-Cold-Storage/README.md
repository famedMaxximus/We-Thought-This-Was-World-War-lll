# Vault-Tec Cold Storage

**Category:** Cryptography
**Difficulty:** Hard
**Points:** Unknown
**Status:** Partially Solved (Flag 2 verified, Flag 1 unverified)

---

## 1. Challenge Overview

A memory dump from a Vault-Tec system contains TLS traffic and RSA key material. The challenge involves recovering a partial RSA prime using Coppersmith's method, decrypting a TLS ClientKeyExchange, and deriving AES-GCM keys to decrypt Flag 2. Flag 1 remains unresolved.

---

## 2. Initial Analysis

### Handout (`Vault-Tec Cold Storage handout.zip`)

- Memory dump with `VTKEYC01` records
- TLS traffic capture
- `flag1.enc` and `flag.enc` (Flag 2)

---

## 3. Investigation and Methodology (Flag 2 — VERIFIED)

### 3.1 Carving `VTKEYC01` Records

From memory dump, carve records beginning with `VTKEYC01`. Useful record at byte offset 122945.

16-byte header after magic parses as little-endian `<HIHHHI`:
- Version: 1
- Identifier
- 128-byte modulus
- 3-byte exponent (65537)
- 64-byte prime field
- 272 known bits

The prime field retains the **high 272 bits of a 512-bit RSA prime**, with the low 240 bits zeroed.

### 3.2 Coppersmith Partial Factorization

Write the prime as `P = P0 + x`, where `0 ≤ x < 2²⁴⁰`. Since `P` divides the 1024-bit public modulus `N`, this is a partial-factor Coppersmith problem.

Construct 20-dimensional lattice with `m = t = 10`:
```
N^(m-i) * (P0 + x)^i       for i = 0 .. m-1
x^j * (P0 + x)^m          for j = 0 .. t-1
```

Scale coefficient column `j` by `(2^240)^j`, apply LLL, remove scaling, factor short polynomials. A linear root gives the missing low bits.

**Recovered factor (512-bit prime):**
```
11504922306534769629256793619865808381216610146944323478042368877785440554830304507620748418474269744713805112531778117712916587805998795736838958354679731
```

Verified: divides `N` and matches surviving prime bits.

### 3.3 RSA Private Exponent & TLS Decryption

Derive RSA private exponent `d`. TLS ClientKeyExchange contains a 128-byte RSA ciphertext. Private decryption produces valid PKCS#1 v1.5 padding and a 48-byte premaster secret beginning with TLS version `03 03`.

Negotiated suite: `TLS_RSA_WITH_AES_128_GCM_SHA256` (`0x009c`).

Use TLS 1.2 SHA-256 PRF to derive master secret from client/server randoms, then expand client/server AES keys and four-byte fixed IVs.

Server's application-data record authenticates at sequence number 1. Its plaintext is a Vault-Tec response containing **Flag 2**.

---

## 4. Vulnerability / Technical Discovery

| Component | Flaw |
|-----------|------|
| RSA key storage | Partial prime (high 272 bits) leaked in memory dump |
| TLS_RSA key exchange | No forward secrecy — compromise of RSA key decrypts all past sessions |
| Coppersmith attack | 272/512 = 53% of prime known → sufficient for lattice attack |

---

## 5. Exploitation / Solution

### Reproduce (Flag 2)

```bash
python3 solve.py --challenge vault_partial
```

Does: prime recovery via Coppersmith/LLL → RSA key derivation → TLS 1.2 PRF → AES-GCM decryption of server application data.

**Does not claim to decrypt `flag1.enc`.**

---

## 6. Flags

### Flag 2 (VERIFIED)
```
LsCTF2026{st4t1c_rsa_k3y_3xch4ng3_h4s_n0_f0rw4rd_s3cr3cy}
```

### Flag 1 (UNVERIFIED)
Not recovered. The writeup explicitly covers Flag 2 only.

---

## 7. Lessons Learned

1. **Partial key exposure is fatal** — 272 bits of a 512-bit RSA prime enables Coppersmith factorization.
2. **Static RSA key exchange has no forward secrecy** — Once the private key is recovered, all recorded TLS sessions can be decrypted.
3. **TLS 1.2 PRF with fixed IVs** — The 4-byte fixed IVs (from RFC) + sequence number construct the nonce for AES-GCM.
4. **Memory forensics + crypto** — Carving key material from memory dumps is a realistic attack vector.

---

## 8. Tools Used

- Python 3: `pycryptodome`, `fpylll` (LLL), `cysignals`
- `volatility` or custom carving for `VTKEYC01` records
- TLS 1.2 PRF implementation (RFC 5246)

---

## 9. Evidence and References

- `evidence/Vault-Tec Cold Storage handout.zip` — Original handout
- `evidence/VTKEYC01_record.bin` — Carved key record
- `solve.py` — Complete solver for Flag 2
- `results/prime_recovery.log` — LLL output showing recovered factor