# recursive

**Category:** Cryptography / Reverse Engineering
**Difficulty:** Easy
**Points:** Unknown
**Status:** Solved (Verified)

---

## 1. Challenge Overview

A program checks a 42-byte flag using a recursive table indexing scheme. At a one-character leaf, `check` compares the input character with `table[index]`. For longer input, it splits and recurses with modified indices.

---

## 2. Initial Analysis

### Handout

ELF binary with a `table` at virtual address `0x4020` (file offset `0x3020`).

### Check Logic

```c
// Pseudocode
check(n, index):
    if n == 1:
        return input[0] == table[index]
    h = n // 2
    return check(h, index) && check(n - h, index + h*h)
```

No transformation of a character at a leaf. Reconstructing the flag means following the same indexing recursion over the table.

---

## 3. Investigation and Methodology

### Recovery Algorithm

```python
def recover(n, index=0):
    if n == 1:
        return bytes([table[index]])
    h = n // 2
    return recover(h, index) + recover(n - h, index + h*h)
```

Apply `recover(42)` → produces the flag.

Feeding it to the unmodified binary prints `FLAG: Correct!`.

---

## 4. Vulnerability / Technical Discovery

**Recursive index calculation with no per-character transformation** — The flag characters are stored directly in the table at computed indices. The recursion is purely structural; no cryptographic operations protect the flag.

---

## 5. Exploitation / Solution

```python
# Read table from file offset 0x3020
with open('files/recursive', 'rb') as f:
    f.seek(0x3020)
    table = f.read(256)  # enough for all indices

flag = recover(42)
print(flag.decode())
# LsCTF2026{r3curs1v3_c4l1_1s_4_v3ry_u53fu1}
```

### Solver (`solve.py --challenge recursive`)

Reproduces the recovery and verifies against the binary.

---

## 6. Flag

```
LsCTF2026{r3curs1v3_c4l1_1s_4_v3ry_u53fu1}
```
(Verified by binary output `FLAG: Correct!`)

---

## 7. Lessons Learned

1. **Recursive indexing without transformation** — If the check only compares against a table at computed indices, the flag is directly reconstructible.
2. **Table at fixed offset** — The table location is deterministic (virtual address → file offset).
3. **No per-character encryption** — Each flag byte is stored raw in the table.

---

## 8. Tools Used

- Python 3 (stdlib only)
- `objdump` / `readelf` for locating table
- `solve.py` — Packaged solver

---

## 9. Evidence and References

- `evidence/files/recursive` — Original ELF binary
- `solve.py` — Packaged solver