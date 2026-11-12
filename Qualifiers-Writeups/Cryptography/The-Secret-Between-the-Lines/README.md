# The Secret Between the Lines

**Category:** Cryptography (secret sharing / Reed-Solomon decoding)
**Difficulty:** Medium
**Status:** Solved (Verified)

---

## 1. Challenge Overview

A vault recovery drill produced two batches of custody records. Each batch was created from a polynomial of degree at most seven over the same prime field. The custodians report that no more than five records in either batch were altered during transfer. The second batch was generated after a maintenance operation that changed the recovery polynomial by an unknown polynomial of degree at most three.

The vault's original master secret is the constant coefficient of the first batch (amber). Its SHA-256 commitment is provided to verify recovery.

---

## 2. Initial Analysis

### Handout (`the_secret_between_the_lines_player.zip`)

- `README.txt` — scenario and archive specification
- `records.json` — field prime, 36 custody records (18 "amber", 18 "cobalt"), the encrypted archive (nonce, ciphertext, tag) and a SHA-256 commitment to the secret

Key facts from `README.txt`:

- Each batch is a set of evaluations (x, y) of a polynomial of degree ≤ 7 over GF(p), p = 170141183460469231731687303715884105727 (= 2^127 − 1).
- At most 5 records in each batch were altered.
- The cobalt batch comes from the amber polynomial plus an unknown polynomial of degree ≤ 3.
- The master secret is the constant term of the amber polynomial.

### Archive specification

```
key        = SHA256(secret.to_bytes(16, "big"))
keystream  = SHAKE256(b"SBL-stream-v1" + key + nonce)
plaintext  = ciphertext XOR keystream
tag        = HMAC-SHA256(key, b"SBL-tag-v1" + nonce + ciphertext)
commitment = SHA256(b"SBL-secret-v1" + secret.to_bytes(16, "big"))
```

Flag format for this challenge: `lsCTF2026{...}` (lowercase `l`, as given in the handout).

---

## 3. Investigation and Methodology

This is Shamir-style secret sharing in which some shares have been altered. In coding terms, each batch is a Reed-Solomon codeword:

- message length k = 8 (degree ≤ 7 means 8 coefficients)
- code length n = 18 (records per batch)
- errors e ≤ 5

A Reed-Solomon code corrects e errors when n ≥ k + 2e. Here k + 2e = 8 + 10 = 18 = n. The bound is met exactly, so the amber batch can be decoded on its own and the true polynomial is unique.

**Uniqueness:** any two degree-7 polynomials that each match at least 13 of the 18 points agree on at least 13 + 13 − 18 = 8 points, and two degree-7 polynomials that agree on 8 points are identical. So exactly one polynomial matches at least 13 points.

The cobalt batch and the degree-3 "maintenance" polynomial are a distraction (or a fallback for solving both batches together). They are not needed.

---

## 4. Vulnerability / Technical Discovery

The share corruption is within the unique-decoding radius of the Reed-Solomon code (n = k + 2e), so the error tolerance the custodians report is exactly what lets an attacker recover the secret from one batch alone.

---

## 5. Exploitation / Solution

Berlekamp-Welch would decode this directly. Because the numbers are small, brute force is simpler:

```
for every 8-subset of the 18 amber points   (C(18,8) = 43,758 subsets):
    fit the degree-7 polynomial through those 8 points (Lagrange)
    count how many of the 18 points it matches
    if it matches >= 13 (at most 5 errors): stop, this is the polynomial
```

Any subset of 8 uncorrupted points produces the true polynomial. There are C(13,8) = 1,287 such subsets, so one turns up quickly.

The secret is the polynomial evaluated at x = 0:

```
secret = 27743386527693643865245782052125903145
```

```
$ python3 solve.py records.json
secret 27743386527693643865245782052125903145 True
tag ok True
lsCTF2026{p0lyn0m14ls_h1de_1n_pl41n_s1ght}
```

---

## 6. Flag

```
lsCTF2026{p0lyn0m14ls_h1de_1n_pl41n_s1ght}
```

Verified: `SHA256(b"SBL-secret-v1" + secret)` equals the published commitment, and the HMAC-SHA256 tag over the archive checks out.

---

## 7. Lessons Learned

1. **Shamir secret sharing with corrupted shares is Reed-Solomon decoding** — remember the bound n ≥ k + 2e.
2. **When the bound is met exactly, one batch is enough** — extra material (the cobalt batch and the degree-3 offset) can be a red herring.
3. **Check the candidate against the commitment or MAC** before trusting the decryption.

---

## 8. Tools Used

- Python 3 standard library (`itertools`, `hashlib`, `hmac`)

---

## 9. Evidence and References

- `solve.py` — brute-force Reed-Solomon decode + decryption (`python3 solve.py records.json`)
- `evidence/README.md` — handout file list
