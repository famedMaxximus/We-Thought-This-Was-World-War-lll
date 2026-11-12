# Squeamish Squash

**Category:** Cryptography
**Difficulty:** Hard
**Points:** 700 (Flag 1: 200, Flag 2: 500)
**Status:** Partially Solved (Flag 1 verified, Flag 2 not recovered)

---

## 1. Challenge Overview

A signing device was recovered with its case cracked open. The bench crew extracted what they could: ECDSA signatures with a reused nonce, an RSA-260 ciphertext, and two encrypted flag blobs. The challenge involves recovering the private ECDSA key through nonce reuse, using the published RSA-260 factorization, and decrypting the flag blobs using keys derived from the recovered cryptographic material.

---

## 2. Initial Analysis

### Handout Files (`Squeamish Squash handout.zip`)

| File | Content |
|------|---------|
| `signatures.txt` | secp256k1 public key `Q`, two ECDSA signatures sharing the same `r` value |
| `ciphertext.txt` | 260-digit decimal integer `c` (RSA-260 ciphertext) |
| `flag1.enc` | 128 raw bytes (AES-GCM envelope) |
| `flag.txt` | secp256k1 fixed public point `P`, 69-byte hex blob (Flag 2 encrypted) |

### Hint Files (`Squeamish Hints/`)

- `Flag1 hint.wav` — Audio with Morse code (0–51s) and spectrogram text (52–75s)
- `Flag2 hint1.pdf` — Moon-phase images encoding text via Leandro Katz Lunar Alphabet

### Flag Format

`LsCTF2026{...}`

---

## 3. Investigation and Methodology

### 3.1 Audio Hint Decoding (Session 5)

The WAV file contains two layers:
- **0–51s**: 650 Hz Morse signal (60 ms dots) → `PUT THE TWO SIGNATURES SIDE BY SIDE. SOMETHING ABOUT THEM SHOULD NOT MATCH, AND THE SIGNER PAID FOR IT`
- **52–75s**: Spectrogram text → `A sealed file opens with a hash of two things: a shortened echo of this challenge's name, marked as flag one, and your key. — Mad1010_無心`

### 3.2 Moon-Phase PDF Decoding (Session 6)

The PDF contains 68 moon tiles. Using the Leandro Katz Lunar Alphabet (dCode), the phase sequence decodes to:
> `EVERYTHING IS CONNECTED WHAT YOU HAVE THUS FAR IS A DROP IN AN OCEAN BUT VERY USEFUL`

This confirms the recovered pieces (ECDSA private key `d`, shared point `S = d·P`, RSA plaintext `m`, RSA factors `p,q`) must be combined, and more remains to be found.

### 3.3 ECDSA Nonce Reuse (Verified)

Both signatures in `signatures.txt` share the same `r` value, indicating nonce reuse. With SHA-256 hashes of the messages (without surrounding quotes):

```
n = secp256k1 group order
z1, z2 = message hashes
k = (z1 - z2) * inverse(s1 - s2, n) mod n
x = (s1*k - z1) * inverse(r, n) mod n
```

Recovered values:
```
k = 41667246332565885209668308841167516170410697202289401632214205549524252523360
x = 84747631942840761409198475171043116002924132430274400095798688737583350222084
```

Verification: `x * G` exactly matches public point `Q`.

### 3.4 ECDH Shared Point

Using the fixed public point `P` from `flag.txt`:
```
S = x * P
Sx = 108423885412618137479942596537859473521289154120912266334220472858813192545908
Sy = 3271402251098107697184433328532725947345952158599779634754336033038067624590
```

### 3.5 RSA-260 Factorization (OSINT, Verified)

Eric Lu (@penlume) posted the factorization on X (2026-09-03):
```
q = 4397328654844826923795068102505872571721883526553349659561256924505973939597593482272505698004801207988043088656411102133523080581
p = 5028695206842569864686141618253083416610081090075366674776775706538324961364412200138116378509733307971876652984898985905923678379
N = p * q (matches RSA-260)
```

---

## 4. Vulnerability / Technical Discovery

### ECDSA Nonce Reuse
The critical flaw is the reuse of the ephemeral nonce `k` across two signatures. This is a textbook ECDSA failure: when `r` is shared, the private key `x` is recovered trivially.

### RSA-260 Public Factorization
The RSA-260 modulus was publicly factored (Cognition blog). The challenge uses this as a known piece of the puzzle.

### Flag Encryption Scheme Ambiguity
The handout does not specify:
- The RSA exponent `e`
- The final encryption/KDF rule for the flag blobs
- The "shortened echo of this challenge's name" for the Flag 1 key derivation

This is an **information gap**, not an effort gap. The author's exact encryption parameters are not derivable from the handout.

---

## 5. Exploitation / Solution

### Flag 1 Recovery (VERIFIED)

The hint indicates: `key = SHA-256("squeam-squash-flag1|" + x)` where `x` is the ECDSA private scalar.

```python
from Crypto.Cipher import AES
from hashlib import sha256

x = 84747631942840761409198475171043116002924132430274400095798688737583350222084
key = sha256(f"squeam-squash-flag1|{x}".encode()).digest()

with open("flag1.enc", "rb") as f:
    data = f.read()

nonce = data[:12]
tag = data[12:28]
ct = data[28:]

cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
pt = cipher.decrypt_and_verify(ct, tag)
print(pt.decode())
```

**Output:**
```
Second lock open. Flag 1:

LsCTF2026{tw0_s1gn4tur3s_0n3_r_g4m3_0v3r}

The third lock is still shut.
```

The GCM tag verifies, confirming the correctness of the key derivation.

### Flag 2 Status (UNVERIFIED)

Multiple approaches were exhausted:
- RSA decryption with `e=65537` → 861-bit random value
- Treating `x` (ECDSA private key) as RSA exponent → inconsistent (scalar is even, ciphertext is QNR mod p)
- Using ECDH shared point `S` with various KDFs and AEAD modes → zero tag successes
- "Seed stretching" hints (Session 7) → all negative

### Flag 2 — "seed2" final hint (released 2026-11-08)

A later hint image (`seed2.png`, "Flag the Second - Final Hint") stated the intended chain:

> "The scalar you recovered isn't only a key. It's also a seed. Stretch it with SHA-256 in counter mode into a few hundred bits, then adjust it until it's a valid RSA exponent for the modulus you already identified. This time there's no label. Use it on one of the artifacts from the handout. The result isn't text: it's a scalar for the curve, and the point in flag is where it goes. The x-coordinate of what comes out is hashed and used to unlock the blob, with the same counter scheme. When you get it right, the blob reads like a flag."

Decoded algorithm:

```text
seed   = d                                  # ECDSA scalar from Flag 1
e      = adjust(SHA256_counter(seed))       # a few hundred bits, gcd(e, phi(N)) == 1
s      = RSA(ciphertext.txt, e, N)          # N = RSA-260
R      = (s mod n) * P                      # P = point in flag.txt
key    = SHA256_counter(R.x)                # no label
flag   = unlock(blob)
```

Tried, all checked against the AES-GCM tag / "LsCTF" / printable oracles, all negative:

- Counter constructions: `sha256(seed||ctr)` with 1/2/4/8-byte BE and LE counters and ASCII counters, prefix and suffix, start 0 and 1; MGF1; HKDF-Expand / Extract+Expand; SP800-108; HMAC counter; hash chains. Every output width from 128 to 768 bits, BE and LE, bit- and byte-truncation.
- Seed encodings: 32-byte BE/LE, decimal string, minimal bytes, hex.
- Adjust rules: increment until coprime with φ(N), `e |= 1`, none, next prime.
- RSA direction `ct^e` and `ct^(e⁻¹ mod φ)`; scalar `s mod n` and low 256 bits; point bases P, Q, G.
- Final unlock: AES-256-GCM (several key/nonce layouts), AES-256-CTR, SHA-256 counter keystream XOR.

Before the hint, an exponent sweep over every odd `e` in [3, 100000] with ECDH/pipe-seal secrets, ~300 label variants and ~1600 KDF/AEAD combinations was also negative.

**Conclusion:** Flag 2 was not recovered. The algorithm is known, but the author's exact byte-level "SHA-256 counter mode" differs from every standard variant tried. The generation snippet, one intermediate value (e, scalar, x, or key), or the cipher mode of the blob would finish it.

---

## 6. Flag

### Flag 1 (VERIFIED)
```
LsCTF2026{tw0_s1gn4tur3s_0n3_r_g4m3_0v3r}
```

### Flag 2 (NOT RECOVERED)
Not recovered. An earlier version of this writeup listed `LsCTF2026{Kerne1_Intersecti0ns_Betray_The_0i1_Space_And_Signing_Is_1inear}` here; that is the **Oil and Vinegar, Never Mixed** flag, not a Squeamish Squash flag.

---

## 7. Lessons Learned

1. **ECDSA nonce reuse is catastrophic** — A single reused `k` exposes the private key immediately.
2. **Public factorizations are valid OSINT** — The RSA-260 factorization was publicly available and correctly used.
3. **Authenticated encryption prevents false positives** — The GCM tag on Flag 1 confirms the key derivation; the lack of tag success on Flag 2 definitively rules out guesses.
4. **Information gaps vs. effort gaps** — When all mathematically derivable values are exhausted and decryption still fails, the missing piece is challenge metadata (exponent, KDF label, mode), not computational effort.
5. **Never trust decoy flags** — Multiple fake flags were embedded in hints and source files.

---

## 8. Tools Used

- Python 3 with `pycryptodome`, `cryptography`
- `scipy` for spectrogram rendering
- `dCode.fr` Lunar Alphabet decoder
- `solve.py` (Flag 1 + Flag 2 harness)

---

## 9. Evidence and References

- `evidence/signatures.txt` — Original ECDSA signatures
- `evidence/flag1.enc` — Flag 1 ciphertext
- `evidence/flag.txt` — Point P and Flag 2 blob
- `evidence/ciphertext.txt` — RSA-260 ciphertext
- `evidence/Squeamish Hints/Flag1 hint.wav` — Audio hint
- `evidence/Squeamish Hints/Flag2 hint1.pdf` — Moon-phase hint
- `solve.py` — Complete solver for Flag 1 (reads `./handout/`), plus the Flag 2 attempt harness