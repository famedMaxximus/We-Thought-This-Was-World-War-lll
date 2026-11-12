# Seven Locks, One Lie

**Category:** Cryptography
**Difficulty:** Medium
**Points:** 300
**Status:** Solved (Verified)

---

## 1. Challenge Overview

A FastAPI service exposing an evidence explorer. Seven cryptographic "locks" are chained: each recovered 32-byte secret `Kᵢ` is the `X-Lock-Key` header for the next evidence record. The final archive key = `HKDF-SHA256(K1‖K2‖…‖K7)`, used to AES-GCM-decrypt the flag capsule (`GET /api/archive`). Each lock has one textbook flaw — "seven guarantees, one lie" (per lock, and literally in lock 6).

---

## 2. Initial Analysis

### Service Endpoints

- Evidence records accessed via `X-Lock-Key` headers
- Each lock's flaw yields a 32-byte secret
- Final archive at `GET /api/archive`

---

## 3. Investigation and Methodology

### Lock 1 — RSA Common Modulus / Bézout

Same modulus `n`, same message, two coprime exponents (65537, 17).
With `a·e1 + b·e2 = 1`: `m = c1^a · c2^b mod n`.
→ **K1** = low 32 bytes of m.

### Lock 2 — AES-GCM Nonce Reuse (Keystream Reuse)

Two records share a nonce.
`keystream = known_ct ⊕ known_pt`
`target_pt = target_ct ⊕ keystream`
Plaintext: `DTX-RECORD|2026|RECOVERY-KEY|<K2>`
→ **K2**

### Lock 3 — Predictable LCG

Modulus published, multiplier/increment unknown.
From consecutive outputs:
`a = (x3−x2)/(x2−x1) mod m`, `c = x2 − a·x1`.
(Recovered a=48271, c=12345.)
Predict next output, `mask = SHA256(decimal(next))`, `K3 = ct ⊕ mask`.
→ **K3**

### Lock 4 — ECDSA Nonce Reuse (secp256r1)

Both signatures share `r` ⇒ same nonce `k`.
`k = (z1−z2)/(s1−s2)`, `d = (s1·k − z1)/r mod n`; verified `d·G == pubkey`.
`K4 = SHA256(d_be32 ‖ "|DTX-K4")`.
→ **K4**

### Lock 5 — SHA-256 Length-Extension Forgery

`tag = SHA256(secret‖message)`, secret = 16 bytes.
Append `&scope=recovery` with glue padding and extend the hash state from the published tag (custom SHA-256 with settable IV).
`POST /api/integrity/check` (keyed by K4) returns **K5**.

### Lock 6 — Shamir with One Corrupted Share (The Literal "Lie")

3-of-5 over the 2⁵²¹−1 prime, one share forged.
Interpolate `f(0)` over all 10 triples; the correct secret is the majority (appeared 4×; the 6 bad triples scatter).
→ **K6**

### Lock 7 — AES-CBC Padding Oracle

`POST /api/recovery/check` (keyed by K6) distinguishes valid vs invalid PKCS#7 padding (and padding lives in the last block, independent of IV).
Standard byte-by-byte CBC padding-oracle, forging the preceding block.
Plaintext: `DTX-RECOVERY:<K7>`
→ **K7**

### Final Archive

`GET /api/archive` returns salt/nonce/ciphertext+tag.
`key = HKDF-SHA256(IKM = K1‖K2‖…‖K7, salt, info="Daltrixx-Seven-Locks-v1")`
AES-256-GCM decrypt → flag.

---

## 4. Vulnerability / Technical Discovery

| Lock | Primitive | Flaw |
|------|-----------|------|
| 1 | RSA | Common modulus, coprime exponents → Bézout |
| 2 | AES-GCM | Nonce reuse → keystream reuse |
| 3 | LCG | Predictable from 3 outputs → linear recurrence |
| 4 | ECDSA | Nonce reuse → private key recovery |
| 5 | SHA-256 | Length extension (secret prefix) |
| 6 | Shamir | One corrupted share → majority vote on f(0) |
| 7 | AES-CBC | Padding oracle → byte-by-byte decryption |

---

## 5. Exploitation / Solution

Each lock solved sequentially. The service is a FastAPI application; requests made with appropriate `X-Lock-Key` headers.

### Recovered Secrets (hex)

- K1  `38a7ea4dfa3293978b647248a5762045c73a51ad7a195da2688e76b15c2a2044`
- K2  `78034e1e08e84ecfa7bf78974fd5092819d7dc9fe802016eed12f40aaa822ac1`
- K3  `de460309d9fb430400a32937b9bb23e60ca4b0b1930c9e46784b80d46cc48508`
- K4  `36ac73ceab78dd420cff24a1aa9409dc38796cf7127b3c99a62a9bf4b89c17fb`
- K5  `6c6aa7c224e340a0d944b3d6f84b5ae9bc2c503d2683985bdcebdc82e7aed504`
- K6  `5555e758f96c65ec355474423c2f43064657131eda31001d4bbae12f6873e00b`
- K7  `84d1a75c0bc0736ae112635a8f364c1127...` (from `DTX-RECOVERY:<hex>` via CBC padding oracle)

### Final Decryption

```python
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

ikm = bytes.fromhex(K1 + K2 + K3 + K4 + K5 + K6 + K7)
hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=salt, info=b"Daltrixx-Seven-Locks-v1")
key = hkdf.derive(ikm)
# AES-256-GCM decrypt archive ciphertext
```

---

## 6. Flag

```
LsCTF2026{m4!Qv8#kR2$nL7&xP9}
```
(Verified via AES-GCM tag authentication on archive)

---

## 7. Lessons Learned

1. **RSA common modulus** — Never reuse modulus across different exponents for the same message.
2. **AES-GCM nonce reuse** — Catastrophic; reusing a nonce with the same key leaks the keystream.
3. **LCGs are not cryptographically secure** — Three outputs suffice to recover parameters.
4. **ECDSA nonce reuse** — Same as RSA common modulus: reusing `k` exposes the private key immediately.
5. **SHA-256 length extension** — Use HMAC or SHA-3 for secret-prefix MACs.
6. **Shamir secret sharing** — A single corrupted share in a threshold scheme can be detected by majority interpolation.
7. **CBC padding oracle** — Any padding validation difference is an oracle; use encrypt-then-MAC or AEAD.

---

## 8. Tools Used

- Python 3: `cryptography`, `requests`, `sage`/`sympy` for ECDSA math
- Custom scripts for each lock
- FastAPI service interaction via HTTP

---

## 9. Evidence and References

- `evidence/lock1_data.json` — RSA parameters and ciphertexts
- `evidence/lock2_data.json` — AES-GCM nonce reuse records
- `evidence/lock3_data.json` — LCG outputs
- `evidence/lock4_data.json` — ECDSA signatures
- `evidence/lock5_data.json` — SHA-256 tag and message
- `evidence/lock6_data.json` — Shamir shares
- `evidence/lock7_data.json` — CBC padding oracle endpoint
- `evidence/archive_response.json` — Final archive ciphertext