# The Secret Between the Lines

**Category:** Cryptography
**Difficulty:** Medium
**Points:** Unknown
**Status:** Unsolved (No verified flag)

---

## 1. Challenge Overview

A vault recovery drill produced two batches of custody records. Each batch was created from a polynomial of degree at most seven over the same prime field. The custodians report that no more than five records in either batch were altered during transfer. The second batch was generated after a maintenance operation that changed the recovery polynomial by an unknown polynomial of degree at most three.

The vault's original master secret is the constant coefficient of the first batch (amber). Its SHA-256 commitment is provided to verify recovery.

---

## 2. Initial Analysis

### Handout (`records.json`)

Contains:
- Field modulus (prime)
- Two batches of records (amber and another)
- Nonce, ciphertext, tag, commitment
- All integers as decimal strings

### Archive Specification

```
key = SHA256(secret.to_bytes(16, "big"))
keystream = SHAKE256(b"SBL-stream-v1" + key + nonce), length of ciphertext
plaintext = ciphertext XOR keystream
tag = HMAC-SHA256(key, b"SBL-tag-v1" + nonce + ciphertext)
commitment = SHA256(b"SBL-secret-v1" + secret.to_bytes(16, "big"))
```

Flag format: `lsCTF2026{...}`

---

## 3. Investigation and Methodology

### Mathematical Structure

- Two polynomial evaluations (batches) of degree ≤ 7 over prime field
- ≤ 5 errors per batch (Reed-Solomon / Berlekamp-Welch decoding)
- Second polynomial = first polynomial + unknown polynomial of degree ≤ 3
- Master secret = constant coefficient of first polynomial

### Approach

1. Use error correction (Berlekamp-Welch or list decoding) to recover the original degree-7 polynomial from each batch
2. The difference between the two recovered polynomials should be degree ≤ 3
3. Extract constant coefficient of first polynomial → master secret
4. Verify against SHA-256 commitment
5. Derive key → decrypt flag via SHAKE256 stream + HMAC-SHA256 tag verification

---

## 4. Current Status

**Unsolved.** The challenge requires implementing:
- Berlekamp-Welch algorithm for Reed-Solomon decoding over prime field
- Handling up to 5 errors in 8+ points (need at least 2e+1 = 11 points for unique decoding, or list decoding)
- Polynomial subtraction and degree verification
- SHAKE256 stream decryption with HMAC verification

No verified flag recovered yet.

---

## 5. Flag

**None recovered** — Challenge remains unsolved.

---

## 6. Lessons Learned (Expected)

1. **Reed-Solomon / Shamir secret sharing with errors** — Berlekamp-Welch decoding recovers polynomials from noisy evaluations.
2. **Polynomial difference constraint** — The degree-3 bound on the difference provides a cross-check between the two batches.
3. **Authenticated decryption** — SHAKE256 stream + HMAC-SHA256 tag ensures only the correct secret produces a valid flag.
4. **SHA-256 commitment** — Allows verification of the recovered secret without the flag ciphertext.

---

## 7. Tools Needed

- Python 3 with `hashlib` (SHAKE256, HMAC, SHA256)
- Prime field arithmetic (modular inverse, polynomial operations)
- Berlekamp-Welch implementation

---

## 8. Evidence and References

- `evidence/records.json` — Complete challenge data

---

## 4. Vulnerability / Technical Discovery

*Challenge not yet solved. Analysis pending.*

## 5. Exploitation / Solution

*Challenge not yet solved. Analysis pending.*

## 6. Flag

**Status: Unsolved** — No flag recovered yet.

## 7. Lessons Learned

*To be completed upon solving.*

## 8. Tools Used

*To be completed upon solving.*

## 9. Evidence and References

*To be completed upon solving.*

