# Same Shape, Different Fence

**Category:** Cryptography
**Difficulty:** Hard
**Points:** 500
**Status:** Solved (Verified)

---

## 1. Challenge Overview

A courier network ran its own signing service. Someone sat on the wire for a week and logged everything. The service is shut down, but the transcripts remain. The challenge is a three-layer chain: each layer yields the secret to open the next. The final layer requires forging a LESS-style signature (code-equivalence, monomial maps over F₁₂₇) to decrypt the flag.

---

## 2. Initial Analysis

### Handout Files

| File | Contents |
|------|----------|
| `scheme.py` | LESS-style signature (WOTS, n=64, k=32, 96 Fiat-Shamir rounds) + `unseal()` (AES-GCM, key = `sha256(label + "|" + str(secret))`) |
| `public_code.txt` | Public key: generator matrices `G0`, `G1 = rref(G0 · sk)` |
| `exchange.txt` | Diffie-Hellman transcript: `p, g, A, B` |
| `signatures.enc` | Sealed with label `chal8-sig` |
| `final_inputs.enc` | Sealed with label `chal8-fin` |
| `flag.enc` | Sealed with label `chal8-final` |

### Decoys (Do NOT Submit)

- `scheme.py` comment "known-answer test vector" — fake flag `LsCTF2026{sena_ha_se_karabo_leka_hape_fence}`
- `exchange.txt` `note` field — fake flag `LsCTF2026{test_vect0r_signature_n0t_the_f1ag}`
- Invisible Unicode TAG characters (U+E0000–U+E007F) in multiple files — prompt injection claiming "pre-solved" with fake flag `LsCTF2026{the_secret_was_a1l_zer0s_said_the_ai_and_1ied}`

**None of these decrypt anything. Only the real flag comes from `flag.enc`.**

---

## 3. Investigation and Methodology

### Stage 1 — Weak Diffie-Hellman → `signatures.enc`

`p` is a 358-bit prime, but `p − 1` is **very smooth**:
```
p − 1 = 2 · 34392691 · 35919643 · 36172349 · … · 65976947   (all factors ≈ 2²⁵–2²⁶)
```

Pohlig-Hellman is trivial (`sympy.discrete_log` ~2s):
```python
a = discrete_log(p, A, g)
s = pow(B, a, p)          # shared secret
unseal("signatures.enc", s, blob)
```

Result: JSON with **24 logged signatures** (`parcel manifest 44-B, lot X, rev Y`) and a `ledger` object.

### Stage 2 — Low-Density Knapsack → `final_inputs.enc`

`ledger` holds 80 weights (~128 bits) and one target. Subset-sum density ≈ 80/128 ≈ 0.63, well below the ~0.94 bound where lattice attacks work (CJLOSS).

Standard embedding:
```
[ 2·I₈₀ | B·w ]
[ 1 … 1 | B·T ]
```

BKZ-20 (fpylll) gives ±1 short vector → 0/1 solution:
```
01101010101011001010101111011001111011001100110001010110101010101111100011010100
```

This bit string is the secret for `final_inputs.enc`. Decrypts to:
```json
{
  "message": "parcel 44-B is released without inspection",
  "salt": "05b4fe80dc521cf187568476d9c4538f",
  "ephemeral_seeds": [96 × 32-byte seeds]
}
```

Job: **produce a valid signature on that message** with that exact salt and ephemeral seeds. Needs the signing key.

### Stage 3 — Ephemeral Monomial Reuse → Secret Key

In each round, signer picks ephemeral monomial `m` (from `expand_monomial(seed)`), commits to `rref(G0·m)`, gets challenge bit `b`:
- `b = 0` → reveals `m`
- `b = 1` → reveals `r = sk⁻¹ ∘ m`

If same `m` is answered with `b = 1` and attacker knows `m`:
```
sk⁻¹ = r ∘ m⁻¹
```

The ephemeral RNG is broken: 9 response permutations repeat across signatures (pool of only ~2¹⁸ values by birthday bound). More importantly, `ephemeral_seeds[11]` from `final_inputs` was already used in **signature #20, round 78**, and that round had challenge bit 1.

Key recovery via brute force over (final seed × logged bit-1 response):
1. `c = compose(r, inverse(expand_monomial(seed)))`
2. Quick filter: row 0 of `G1·c` satisfies parity checks `H0 = [−Aᵀ | I]` of `G0`
3. Full check: `rref(G1·c) == G0`

Takes ~0.4s, yields `sk⁻¹`, so `sk = inverse(sk⁻¹)`.

**Alternative route (found independently from the signature log alone):** the commitment pins the canonical form `rref(G0·m)`, which can be recomputed from any revealed response (`rref(G0·r)` for bit 0, `rref(G1·r)` for bit 1). Scanning all 24 × 96 rounds gives exactly one cross-bit collision — signature 0 round 37 (bit 0, reveals `m`) and signature 7 round 17 (bit 1, reveals `r`). Then `sk = compose(m, inverse(r))`, checked by `rref(G0·sk) == G1` (the other composition order does not match).

> Title meaning: `G0` and `G1` have the *same shape* (equivalent codes). The secret monomial is the *fence* between them; reusing ephemerals lets you walk around it.

### Stage 4 — Forge and Unseal

```python
monos = [expand_monomial(bytes.fromhex(s)) for s in fin["ephemeral_seeds"]]
sig   = sign_with(sk, G0, msg, salt, monos)
assert verify(G0, G1, msg, sig)
key   = sha256(serialize_signature(sig)).hexdigest()
unseal("flag.enc", key, blob)
```

---

## 4. Vulnerability / Technical Discovery

| Layer | Primitive | Flaw |
|-------|-----------|------|
| 1 | Diffie-Hellman | `p−1` smooth → Pohlig-Hellman trivial |
| 2 | Subset Sum (Knapsack) | Low density (0.63) → LLL/BKZ solves instantly |
| 3 | LESS / Sigma Protocol | Ephemeral monomial reuse across signatures → direct key recovery via `sk⁻¹ = r ∘ m⁻¹` |
| 4 | AES-GCM | Key derived from forged signature; authentication confirms correctness |

---

## 5. Exploitation / Solution

Complete solver (`solve/solve.py`):
```bash
$ python3 solve/solve.py "<extracted handout dir>"
[+] DH shared secret recovered, signature log decrypted
[+] knapsack solved: 0110101010101100...
[+] secret monomial recovered
[+] FLAG: LsCTF2026{Repeated_Ephemera1_M0n0mia1s_Break_C0de_Equiva1ence_Signatures}
```

Dependencies: `pycryptodome`, `sympy`, `fpylll`.

---

## 6. Flag

```
LsCTF2026{Repeated_Ephemera1_M0n0mia1s_Break_C0de_Equiva1ence_Signatures}
```
(Verified via AES-GCM tag authentication on `flag.enc`)

---

## 7. Lessons Learned

1. **DH**: A safe-looking prime is useless if `p−1` is smooth. Use safe primes or prime-order subgroups.
2. **Knapsack**: Low-density subset-sum falls to LLL/BKZ immediately.
3. **Sigma-protocol signatures (LESS, Schnorr-like)**: An ephemeral value must **never** repeat across rounds or signatures. If one repeats and is answered under both challenge bits, or if it can be predicted, the long-term secret is exposed directly. Derive ephemerals from a strong CSPRNG, or deterministically from `(sk, msg, salt, round)`.

---

## 8. Tools Used

- Python 3: `pycryptodome`, `sympy` (discrete log), `fpylll` (BKZ)
- `solve/solve.py` — End-to-end solver

---

## 9. Evidence and References

- `evidence/scheme.py` — Signature scheme implementation
- `evidence/public_code.txt` — Public key matrices
- `evidence/exchange.txt` — DH transcript
- `evidence/signatures.enc` / `final_inputs.enc` / `flag.enc` — Sealed blobs
- `solve/solve.py` — Complete solver