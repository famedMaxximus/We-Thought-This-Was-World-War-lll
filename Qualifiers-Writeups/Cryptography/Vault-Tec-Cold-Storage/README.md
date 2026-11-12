# Vault-Tec Cold Storage

**Category:** Cryptography
**Difficulty:** Hard
**Points:** Unknown
**Status:** Partially Solved (Flag 2 verified, Flag 1 not recovered)

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

`enc_pms.bin` is the 128-byte RSA ciphertext from the ClientKeyExchange record in `tls_session.bin`.

```bash
python3 scripts/solve_rsa.py <handout>/coldmem.dmp   # Coppersmith -> writes p.txt, q.txt
python3 scripts/solve_tls.py <handout>               # needs enc_pms.bin, tls_session.bin
```

Output (reproduced from the original handout):

```
RECOVERED low=240 m=16: p=0xdbaae389cf2f68b5...fa7f17efda05089be5b247b3
p*q==n: True p prime True q prime True
RSA decrypt head: 0002fa
premaster (48 bytes): 03032cd562af5972...
DECRYPTED server seq=1: b'VAULT-TEC RESPONSE // OVERSEER CHANNEL // LsCTF2026{st4t1c_rsa_k3y_3xch4ng3_h4s_n0_f0rw4rd_s3cr3cy}\n'
```

The known high bytes of `p` sit at dump offset `0x1e0dc` (34 bytes) inside the `VTKEYC01` record at `0x1e041`; `n` is the 128 bytes at record offset +24. Of the four `VTKEYC01` records, only this one holds a valid (odd, 1024-bit) modulus; the other three "moduli" are even and appear to be decoys.

**Does not claim to decrypt `flag1.enc`.**

---

## 6. Flags

### Flag 2 (VERIFIED)
```
LsCTF2026{st4t1c_rsa_k3y_3xch4ng3_h4s_n0_f0rw4rd_s3cr3cy}
```

### Flag 1 (NOT RECOVERED)

`flag1.enc` (249 bytes, high entropy) was not decrypted. Ruled out, with all material available (RSA `p,q,d,n`, premaster, master secret, TLS key block):

- AES-GCM / AES-CTR / ChaCha20(-Poly1305) with every 16/24/32-byte window of the memory dump as key
- Fernet (249 = 57 + 192 fits, but the version byte is `0xec`, not `0x80`)
- RSA hybrid (OAEP: zero hits; `flag1[:128] >= n`), textbook RSA on every `< n` window
- XOR against every 249-byte memory window; repeating-key XOR (data looks random)
- Derived keys (master, premaster, client/server write keys, `p`, `q`, `d`, `n`; raw and SHA/MD5/SHA1/SHA512) × GCM/CTR/CBC/ChaCha
- TLS exporter PRF with ~19 guessed labels; extended key-expansion slices; `flag1` as a TLS-GCM record with seq 0..63
- `VTSESS01` / `VTLOGC01` blobs as keys

Untried ideas at the time work stopped: GCM with an 8-byte prepended nonce or non-empty AAD; ChaCha20 with a 12-byte IETF nonce; a second TLS session behind the second `VTSESS01` blob.

---

## 7. Lessons Learned

1. **Partial key exposure is fatal** — 272 bits of a 512-bit RSA prime enables Coppersmith factorization.
2. **Static RSA key exchange has no forward secrecy** — Once the private key is recovered, all recorded TLS sessions can be decrypted.
3. **TLS 1.2 PRF with fixed IVs** — The 4-byte fixed IVs (from RFC) + sequence number construct the nonce for AES-GCM.
4. **Memory forensics + crypto** — Carving key material from memory dumps is a realistic attack vector.

---

## 8. Tools Used

- Python 3: `fpylll` (LLL), `sympy`, `cryptography` (AES-GCM)
- Custom carving of `VTKEYC01` records (fixed offsets in `coldmem.dmp`)
- TLS 1.2 PRF implementation (RFC 5246)

---

## 9. Evidence and References

- `scripts/cs2.py` — Coppersmith (known MSBs of a factor) lattice
- `scripts/solve_rsa.py` — carves `n` and the partial prime from `coldmem.dmp`, recovers `p`, `q`
- `scripts/solve_tls.py` — RSA-decrypts the premaster, TLS 1.2 PRF, AES-128-GCM decrypt of the app-data record
- `evidence/README.md` — handout file list