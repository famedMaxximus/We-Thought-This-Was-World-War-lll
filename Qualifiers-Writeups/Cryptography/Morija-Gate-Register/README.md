# Morija Gate Register

**Category:** Cryptography (symmetric / SPN cryptanalysis)
**Difficulty:** Hard
**Points:** 500
**Status:** Solved (Verified)

---

## 1. Challenge Overview

> The Morija Arts & Cultural Festival printed every ticket as a four-digit code
> from a cipher a student wrote for the occasion. A laptop crash left the gate
> register only partly intact, and the volunteers' notice, sent under the same
> key, is still sealed. Read it.

---

## 2. Initial Analysis

### Handout (`Morija Gate Register handout.zip`)

- `mokorotlo.py` — the cipher: a **16-bit, 6-round substitution-permutation
  network** (a Heys-style toy SPN). Each round = `key mix → S-box → bit
  permutation` (last round omits the permutation), then a final key mix.
  **Seven independent 16-bit round keys** (not in the file).
- `gate_register.csv` — `serial,code`: **47,116 of 65,536** plaintext→ciphertext
  pairs (plaintext = `serial`, ciphertext = `code`). A partial codebook.
- `gate_notice.txt` — `iv 29c7` + 96 ciphertext blocks. The notice, encrypted in
  **CBC mode** under the same key.

### Codebook lookup fails

The natural first try is to treat the register as a codebook and look up each
notice block's plaintext (CBC: `P_i = D(C_i) XOR C_{i-1}`, `C_0 = IV`):

```
blocks missing from codebook: ['0xc97','0x1189',...]   # ALL 96 missing
```

**All 96** notice blocks are absent from the register. A random 72% subset
would contain ~69 of them; the probability of all 96 being absent by chance is
~`0.28^96` ≈ 0. The author deliberately removed exactly the rows needed, so the
key must be **recovered**.

---

## 3. Investigation and Methodology

### Why brute force / SAT fails

- Key space is `7 × 16 = 112` bits — no brute force.
- `z3` (SMT, bit-vector) could not invert the 6-round SPN in any reasonable
  time, with either the default engine or `qfbv`/bit-blast tactics.

### Linear cryptanalysis is viable

The S-box has max linear bias `6/16` (correlation `0.75`), so linear
cryptanalysis applies. The classic last-round attack (Matsui Algorithm 2)
recovers the final whitening key using an `(R-1)`-round linear approximation.

---

## 4. Vulnerability / Technical Discovery

- **16-bit block size** — ~72% of the full codebook is available as known plaintext.
- **High-bias S-box** — linear correlation 0.75 per active S-box.
- Together these let linear cryptanalysis recover all 112 key bits round by round.

---

## 5. Exploitation / Solution

### Linear cryptanalysis (Matsui Algorithm 2), peel-and-reduce

**1. Linear Approximation Table (LAT)** for the S-box, then a trail search
propagating input masks forward through `round = S-box → bit-permutation` to
enumerate many approximations `α·plaintext → γ·Z`, where `Z` is the input to the
last round's S-box layer.

**2. FWHT-accelerated Algorithm 2.** For each approximation `(α, γ)` and every
candidate last key `k`, the correlation

```
corr(k) = (1/N) Σ_p (-1)^{α·p ⊕ γ·S⁻¹(c ⊕ k)}
```

is an XOR-convolution of two 2¹⁶ vectors, computed for **all** `k` at once with
the Fast Walsh–Hadamard Transform. Accumulating the **capacity** `Σ corr²`
over hundreds of approximations (the full linear hull) makes the correct key
stand out even though any single 5-round trail is weak (`|corr| ≈ 0.03`).

**3. Peel and reduce.** Recover the outer whitening key `k6`; strip the last
round (`m = S⁻¹(c ⊕ k6)`), fold the bit-permutation (`m' = P⁻¹(m)`) to regain
the canonical "no-permutation-on-last-round" form with **one fewer round**;
repeat. Each reduced cipher has shorter, stronger trails, so `k5…k1` fall
easily; `k0` is read off the final 1-round relation. Recovered keys that fold
the permutation satisfy `k[i] = P(top_i)`.

The solver was validated end-to-end on randomly-keyed instances (full key
recovered, 0 mismatches) before running on the real data.

```
$ python3 solver.py real
  stage 6: top=0x3f35 ...
  ...
keys: ['0x49e1','0xdb10','0x8259','0xd464','0x67da','0xc4d','0x3f35']
mismatches(all): 0
```

**Round keys (k0..k6):** `49e1 db10 8259 d464 67da 0c4d 3f35`
(verified: they reproduce **all 47,116** register pairs exactly).

### Decrypting the notice

With the keys, build `D = E⁻¹` and CBC-decrypt (`P_i = D(C_i) ⊕ C_{i-1}`,
`C_0 = IV = 0x29c7`), packing each 16-bit block big-endian into 2 ASCII bytes:

```
$ python3 decrypt_notice.py
MORIJA ARTS AND CULTURAL FESTIVAL -- GATE OPERATIONS NOTICE -- STAFF PASS CODE
FOR MUSEUM ENTRANCE: LsCTF2026{m0r1j4_g4t3_r3g1st3r_l34ks_th3_k3y_thr0ugh_d1ff3r3nc3s}
-- DESTROY AFTER READING.
```

---

## 6. Flag

```
LsCTF2026{m0r1j4_g4t3_r3g1st3r_l34ks_th3_k3y_thr0ugh_d1ff3r3nc3s}
```

Verified: the recovered round keys reproduce all 47,116 register pairs, and the
CBC decryption yields readable English around the flag.

---

## 7. Lessons Learned

1. **A 16-bit block is far too small** — ~72% of the codebook plus a classic SPN
   with a high-bias S-box is enough to recover all 112 key bits.
2. **Use the linear hull, not one trail** — single 5-round trails were too weak;
   summing squared correlations over hundreds of approximations separated the key.
3. **Peel and reduce** — each recovered round key turns the problem into a shorter,
   easier cipher.
4. A cipher "a student wrote for the occasion" has no security margin.

---

## 8. Tools Used

- Python 3 + NumPy (LAT, trail search, FWHT)
- `z3` (tried, failed to invert the 6-round SPN)

---

## 9. Evidence and References

- `solver.py` — key recovery (LC Algorithm 2 + FWHT, peel-and-reduce). `test` mode
  self-validates on random keys; `real` mode recovers from the register.
- `lc5.py` — cipher model, LAT, trail search, FWHT Algorithm 2 (imported by solver).
- `decrypt_notice.py` — CBC-decrypts `gate_notice.txt` with `keys.json`.
- `mokorotlo.py` — the original cipher from the handout.
- `evidence/README.md` — handout file list and recovered keys.
