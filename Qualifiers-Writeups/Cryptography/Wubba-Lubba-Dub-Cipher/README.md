# Wubba Lubba Dub Cipher

**Category:** Cryptography
**Difficulty:** Easy
**Points:** Unknown
**Status:** Solved (Verified)

---

## 1. Challenge Overview

A repeating-key cipher (Vigenère-like) preserving spaces and punctuation. The hint defines the flag key derivation from the recovered passphrase.

---

## 2. Initial Analysis

### Handout (`Wubba Lubba Dub Cipher handout.zip` → `extracted/`)

| File | Content |
|------|---------|
| `hint` | Defines flag key derivation |
| `flag.enc` | AES-GCM envelope (nonce 12, tag 16, ciphertext) |

---

## 3. Investigation and Methodology

### Ciphertext Analysis

The ciphertext preserves spaces and punctuation. Trying repeating-key periods and scoring letter shifts against English frequencies gives a clear result at **period 12**.

### Key Recovery

An effective Vigenère decryption key is `EVPXNAQZBEGL`, advancing the key only for uppercase letters. This recovers readable text beginning:

> `INTERDIMENSIONAL COUNCIL OF RICKS SECURITY BULLETIN`

The message explicitly states that the current passphrase is **`GAZORPAZORP`**.

### Hint Defines Flag Key

```
SHA-256("wubba-flag|" + "GAZORPAZORP")
```

Resulting key:
```
8f5d9c1ef20d98b1fe92811bb9c222ee310e5d0c74c0bb7f2a73bf22af3da020
```

### Flag Decryption

Treat `flag.enc` as AES-GCM envelope: 12-byte nonce, 16-byte authentication tag, then ciphertext.

Authenticated decryption yields the flag.

---

## 4. Vulnerability / Technical Discovery

| Component | Flaw |
|-----------|------|
| Repeating-key cipher | Vigenère with period 12; frequency analysis trivially breaks it |
| Passphrase in plaintext | Decrypted message explicitly reveals the passphrase `GAZORPAZORP` |
| Key derivation | Simple SHA-256 of label + passphrase |

---

## 5. Exploitation / Solution

```python
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# 1. Vigenère decrypt with period 12, key "EVPXNAQZBEGL" (uppercase only)
#    → reveals passphrase "GAZORPAZORP"

# 2. Derive AES key
key = hashlib.sha256(b"wubba-flag|" + b"GAZORPAZORP").digest()

# 3. Decrypt flag.enc
with open('flag.enc', 'rb') as f:
    data = f.read()
nonce = data[:12]
tag = data[12:28]
ct = data[28:]

flag = AESGCM(key).decrypt(nonce, ct + tag, None).decode()
print(flag)
# LsCTF2026{st4ck1ng_w34k_c1ph3rs_1sn7_s3cur17y}
```

### Solver (`solve.py --challenge wubba`)

Reproduces the full chain.

---

## 6. Flag

```
LsCTF2026{st4ck1ng_w34k_c1ph3rs_1sn7_s3cur17y}
```
(Verified via AES-GCM tag authentication)

---

## 7. Lessons Learned

1. **Repeating-key ciphers are weak** — Vigenère with known period falls to frequency analysis instantly.
2. **Stacking weak ciphers isn't security** — The challenge title says it: "stacking weak ciphers isn't security."
3. **Passphrase exposure in plaintext** — The decrypted message literally tells you the passphrase.
4. **Authenticated encryption confirms correctness** — AES-GCM tag verifies the key derivation.

---

## 8. Tools Used

- Python 3: `pycryptodome` (AES-GCM), `hashlib`
- Frequency analysis (manual or scripted)
- `solve.py` — Packaged solver

---

## 9. Evidence and References

- `evidence/extracted/hint` — Flag key derivation
- `evidence/extracted/flag.enc` — AES-GCM envelope
- `solve.py` — Packaged solver