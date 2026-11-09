# Crypto Cheatsheet

> Tools: `pip install pycryptodome sympy gmpy2`; `sage` for hard number theory; CyberChef for quick stuff.
> See `../scripts/crypto_helpers.py` for runnable versions of the RSA/XOR attacks below.

## Identify first
- `LsCTF2026{` base64? `==` ending, charset → base64. Hex-only → hex. `U2FsdGVk` → OpenSSL AES.
- Equal-length blocks of 16/8 bytes → block cipher. Repeating 16-byte blocks → **AES-ECB**.
- `n, e, c` given → RSA. `p, g, A, B` → Diffie-Hellman. Matrix → Hill. Lattice-ish → go Sage.
- `hash-identifier` / `hashid` for unknown hashes.

## Encodings (try in this order)
```bash
echo "..." | base64 -d ; base32 -d ; xxd -r -p       # b64 / b32 / hex
echo "..." | rev ; tr 'A-Za-z' 'N-ZA-Mn-za-m'        # reverse / rot13
# base58/base85/base-N, URL-encode, morse, braille, binary -> use CyberChef "Magic"
python3 -c "print(bytes.fromhex('...').decode())"
```

## RSA — pick the attack by what's weird
| Clue | Attack |
|------|--------|
| `e` small (3) & `c` small | cube root: `m = iroot(c, e)` |
| same `m`, multiple `(n_i,e_i)` with same e | **Håstad broadcast** (CRT + e-th root) |
| same `n`, two `e` coprime | **common modulus** (extended GCD) |
| `n` factorable / small / in FactorDB | factor → d → decrypt |
| two keys share a prime | `gcd(n1,n2)` = p |
| `d` small | **Wiener's attack** (continued fractions) |
| `p,q` very close | **Fermat factorization** |
| partial key / high bits known | Coppersmith (Sage `small_roots`) |
```python
# core once you have p,q:
from Crypto.Util.number import inverse, long_to_bytes
phi=(p-1)*(q-1); d=inverse(e,phi); m=pow(c,d,n); print(long_to_bytes(m))
```
FactorDB: http://factordb.com  — paste n first, always.

## AES / block ciphers
- **ECB**: identical plaintext blocks → identical ciphertext. ECB cut-and-paste; byte-at-a-time
  **ECB decryption oracle** (append your input before secret, recover secret byte by byte).
- **CBC bit-flipping**: flip a byte in ciphertext block i to flip the same byte in plaintext block i+1.
- **CBC padding oracle**: if server leaks valid/invalid padding → decrypt without key (`padbuster` or script).
- **Nonce reuse** (CTR/GCM): XOR of two ciphertexts = XOR of plaintexts → crib-drag.

## XOR
```python
# single-byte: brute 0..255, score by printable/English freq
# repeating-key: find keylen via Hamming distance, then single-byte per column (Vigenère-style)
# known plaintext: key = cipher ^ known   (if you know "LsCTF2026{")
```

## Classical ciphers
- Caesar/ROT (brute 25), Vigenère (`dcode.fr` or kasiski), substitution (quipqiup.com),
  Atbash, rail fence, Playfair, affine, Bacon, Polybius, Morse. **dcode.fr** solves most instantly.

## Hashes / passwords
```bash
hashid HASH ; hash-identifier
john --wordlist=rockyou.txt hashes.txt ; john --show hashes.txt
hashcat -m <mode> hashes.txt rockyou.txt          # -m 0 md5, 100 sha1, 1400 sha256, 1800 sha512crypt
```
crackstation.net for quick lookups. Length-extension: `hashpump` (MD5/SHA1 MACs).

## PRNG / randomness
- Python `random` is Mersenne Twister → **predictable**: 624 consecutive 32-bit outputs recover
  state (`randcrack`). LCG: solve for a,c,m from a few outputs. `time()`-seeded → brute the seed.

## DH / ECC
- Small/ smooth prime → Pohlig-Hellman / baby-step giant-step for discrete log (Sage `.log()`).
- Repeated ECDSA nonce `k` → recover private key from two signatures.

## Go-to snippet
```python
from Crypto.Util.number import long_to_bytes, inverse, GCD
from sympy import factorint, isprime
import gmpy2
# iroot: gmpy2.iroot(c, e)   ->  (root, exact?)
```
