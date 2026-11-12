# Ninety-Six Boxes

**Category:** Cryptography
**Difficulty:** Hard
**Points:** 500
**Status:** Solved (Verified)

---

## 1. Challenge Overview

> "Ninety-six boxes sit on a shelf. Each is a pair of symmetric 64×64 matrices over GF(2). Most are noise. Five are not."

The challenge involves identifying the five "special" boxes among 96 by analyzing their graph structure, then using their permutations to derive AES-GCM keys for two encrypted flags.

---

## 2. Initial Analysis

### Handout (`Ninety-Six Boxes handout.zip`)

| File | Content |
|------|---------|
| `boxes.bin` | 98,316 bytes: 96 boxes, each with two 64×64 symmetric matrices |
| `stage2.enc` | 845 bytes, AES-256-GCM |
| `flag.enc` | 86 bytes, AES-256-GCM |

### Parsing `boxes.bin`

- Header: `BOXES96\0`, u16 count=96, u16 dim=64
- Each box: matrix A (512 B) followed by matrix B (512 B)
- Each matrix: 64 rows of big-endian u64, column j at bit j (LSB first)
- Every A and B is symmetric with zero diagonal → **adjacency matrix of a graph on 64 vertices**

---

## 3. Investigation and Methodology

### 3.1 Structure: Smeared Graphs

- Every **A** is a 20-regular graph with a planted gadget: a 4-set X whose rows XOR to 0, with 14 common neighbours and 2 private neighbours per pair.
- Colour refinement with the gadget individualised gives a discrete partition → A has **no automorphisms**.
- Every **B** is a relabeled, noisy ("smeared") copy of A: `B = π(A) ⊕ E`.

### 3.2 Close Matching (Noisy Graph Isomorphism)

For each box, permutation π recovered as quadratic assignment problem:
- Seeded FAQ (Fast Quadratic Assignment)
- 2-swap local search
- Maximising edge overlap between A and relabeled B

Results: 560–606 of 640 edges overlapping (vs ~400 for random relabeling).

### 3.3 Identifying the Five Special Boxes

Counting flipped edges `|E| = popcount(π(A) ⊕ B)`:

| Boxes | Flips |
|-------|-------|
| 91 decoys | 136–144 (always even) |
| **5, 20, 48, 84, 87** | **exactly 128** |

**Decoys**: Noisy copies of a *non-isomorphic* graph (128 noise flips + a few degree-preserving edge swaps).
**Special boxes**: True noisy isomorphic copies of their A. Each has a unique optimal permutation; no transposition keeps the count at 128.

Recovered permutations saved in `results/special_perms.json`.

---

## 4. Vulnerability / Technical Discovery

The signal is the **flip count**: exactly 128 flipped edges (256 cells) marks the five real boxes against 136–144 for decoys.

Noisy graph isomorphism solved in practice by:
- QAP relaxation (`scipy.optimize.quadratic_assignment`, FAQ)
- 2-opt local search
- Seeded with the planted XOR-zero quartet

---

## 5. Exploitation / Solution

### Stage 2: Decrypt Checkpoint

Both `.enc` files use AES-256-GCM: `nonce(12) || tag(16) || ciphertext`.

Stage-2 key comes **only** from indices of the five genuine boxes:
```python
key2 = sha256(b"ninetysix-stage2|5,20,48,84,87")
```

Authenticated plaintext confirms the shortlist and specifies the final key:
> "Each genuine box is a relabelling of itself that was then smudged on the photocopier: `B[i][j] = A[p[i]][p[j]]` for a permutation p of all 64 coordinates, except for a number of cells flipped afterwards. Recover p for every one of the five, exactly."

### Final Key: Permutation Direction Matters

The matcher saved `p` with `A[i][j] ~ B[p[i]][p[j]]`, but the challenge wants `B[i][j] ~ A[p[i]][p[j]]` — the **inverse permutation**.

With saved direction → GCM tag check fails.
With inverse → GCM tag succeeds.

```python
canon = ";".join(f"{i}:" + ",".join(map(str, p[i])) for i in [5, 20, 48, 84, 87])
key = sha256(b"ninetysix-final|" + canon.encode() + b"|" +
             sha256(stage2_plaintext).hexdigest().encode()).digest()
```

---

## 6. Flags

### Flag 1 (VERIFIED)
Decrypted from `stage2.enc`:
```
LsCTF2026{sm34r3d_gr4ph5_n33d_cl053_m4tch35_4nd_p3rm_dl0g}
```

### Flag 2 (VERIFIED)
Decrypted from `flag.enc` using key derived from inverse permutations and stage2 plaintext hash:
```
LsCTF2026{sm34r3d_gr4ph5_n33d_cl053_m4tch35_4nd_p3rm_dl0g}
```
(Same flag content in both envelopes)

Both authenticated via AES-GCM tag checks.

---

## 7. Lessons Learned

1. **"Most are noise"**: The signal is the flip count. Exactly 128 flipped edges vs 136–144 marks the five real boxes.
2. **Noisy graph isomorphism** is solved well in practice by QAP relaxation (`scipy.optimize.quadratic_assignment`, FAQ) plus 2-opt, seeded with the planted XOR-zero quartet.
3. **Key derivation was not guessable** — Stage 2 had to be opened first, because it states the exact serialization and permutation direction.
4. **Authenticated encryption prevents false positives** — GCM tag verification confirms the correct permutation direction and serialization.

---

## 8. Tools Used

- Python 3: `numpy`, `scipy.optimize.quadratic_assignment`, `pycryptodome`
- `results/special_perms.json` — Recovered permutations for the 5 special boxes
- Solver script (`solve.py` or equivalent)

---

## 9. Evidence and References

- `evidence/boxes.bin` — Raw box data
- `evidence/stage2.enc` / `flag.enc` — Encrypted flags
- `results/special_perms.json` — Recovered permutations
- `evidence/flag.enc` solver snippet (see Section 5)