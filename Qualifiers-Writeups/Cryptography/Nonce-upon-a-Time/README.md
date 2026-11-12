# Nonce Upon a Time

**Category:** Cryptography
**Difficulty:** Medium
**Points:** 300
**Status:** Solved (Verified)

---

## 1. Challenge Overview

Kamukunji Research Institute evidence: Schnorr-style signatures over parameters (p, q, g, public_key), three signed records, and a sealed (XOR-stream) record. The vulnerability is a reused nonce across two signatures.

---

## 2. Initial Analysis

### Evidence (`evidence.json`)

- Parameters: `p`, `q`, `g`, `public_key`
- Three signed records with Schnorr-style signatures
- One sealed record (XOR-stream encrypted)
- Rules given in-file:
  - `challenge c = SHA256(decimal(commitment) + "|" + message) mod q`
  - `response s = nonce k + c * secret (mod q)`
  - Archive: `key = SHA256(decimal(secret))`, `stream_block = SHA256(key || nonce || uint32_be(counter))`, `ct = pt XOR stream`

---

## 3. Investigation and Methodology

### Vulnerability — Reused Nonce

Signatures #1 and #2 have the **same commitment**:
```
83943354632956118653980254618689240352
```
⇒ Same nonce `k` was used.

With shared `k`:
```
s1 = k + c1*x
s2 = k + c2*x
s1 - s2 = (c1 - c2)*x   (mod q)
x = (s1 - s2) * (c1 - c2)^-1  (mod q)
```

### Recovery

```python
secret x = 23367712963332023260984516818447676423
```

Verified:
- `pow(g, x, p) == public_key` ✓
- `k = s1 - c1*x` reproduces the shared commitment ✓
- Third signature's commitment also checks out ✓

### Decrypt Sealed Record

```
key    = SHA256(decimal(x))
nonce  = "archive-v1"
stream = SHA256(key || nonce || counter_be) blocks
pt     = ciphertext XOR stream
```

---

## 4. Vulnerability / Technical Discovery

**Schnorr nonce reuse** — Identical to ECDSA nonce reuse. When the same `k` is used for two different messages (different challenges `c1`, `c2`), the secret `x` is recovered immediately via linear algebra. The commitment (which is `g^k mod p`) being identical is the smoking gun.

---

## 5. Exploitation / Solution

Complete solution in Python standard library (no external deps):

```python
import json, hashlib

# Load evidence.json
# Compute c1, c2 from messages and shared commitment
# x = (s1 - s2) * pow(c1 - c2, -1, q) % q
# Verify: pow(g, x, p) == pubkey
# key = hashlib.sha256(str(x).encode()).digest()
# Decrypt sealed record with SHA256 stream
```

---

## 6. Flag

```
LsCTF2026{r3us3d_n0nc3s_l34v3_tr4c3s}
```
(Verified by successful decryption of sealed record)

---

## 7. Lessons Learned

1. **Nonce reuse in Schnorr signatures is fatal** — Same as ECDSA: identical `k` for two messages exposes the secret immediately.
2. **Commitment = `g^k` is the fingerprint** — If two signatures have the same commitment, they used the same `k`.
3. **XOR stream from SHA-256 is not authenticated** — The sealed record has no integrity check; the Schnorr signature verification on the other records is what authenticates the recovered secret.
4. **Solved entirely offline with stdlib** — No external crypto libraries needed; pure Python `hashlib` and `pow` suffice.

---

## 8. Tools Used

- Python 3 (stdlib only: `json`, `hashlib`)
- `evidence.json` — Challenge data

---

## 9. Evidence and References

- `evidence/evidence.json` — Parameters, signatures, sealed record