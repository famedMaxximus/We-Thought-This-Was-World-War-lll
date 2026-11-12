# gates

**Category:** Cryptography / Reverse Engineering
**Difficulty:** Easy
**Points:** Unknown
**Status:** Solved (Verified)

---

## 1. Challenge Overview

A binary reads 37 input bytes and evaluates a table of 296 nodes. The table defines a circuit of byte operations (add, XOR, copy). The output nodes are compared against 37 target bytes. Solve by modeling as Z3 constraints.

---

## 2. Initial Analysis

### Handout

ELF binary (`files/gates`). Table starts at file offset `0x3020`; every node occupies 16 bytes:
```
int32 operation, int32 input_a, int32 input_b,
uint8 ready, uint8 value, padding[2]
```

First 37 nodes hold the input. Constant nodes have operation 0.
Operations:
- 1: add modulo 256
- 2: add modulo 256 (same)
- 3: XOR
- 4: copy input

Nodes 259–295 compared with 37 target bytes at file offset `0x42a0`.

**Critical**: The evaluator can recompute arithmetic nodes even when their initial `ready` field is set, so treating every initially ready node as a constant gives the wrong model.

---

## 3. Investigation and Methodology

### Constraint Solving with Z3

Model input bytes as 8-bit Z3 bit-vectors (`BitVec(8)`), propagate expressions through the circuit, and constrain output nodes (259–295) to equal the target bytes.

Eight-bit arithmetic automatically supplies the required wraparound.

The satisfying assignment decodes to the flag.

---

## 4. Vulnerability / Technical Discovery

**Byte circuit with known outputs** — The circuit is essentially a straight-line program of byte operations. With known targets at the output, the inputs are uniquely determined (assuming the circuit is well-constrained). Z3 solves the resulting system of modular equations instantly.

---

## 5. Exploitation / Solution

```python
from z3 import *

# Parse table from offset 0x3020
# targets from offset 0x42a0

s = Solver()
inputs = [BitVec(f'in_{i}', 8) for i in range(37)]
nodes = inputs[:]  # first 37 are inputs

for i in range(37, 296):
    op, a, b, ready, val = parse_node(i)
    if op == 0:  # constant
        nodes.append(BitVecVal(val, 8))
    elif op == 1 or op == 2:  # add mod 256
        nodes.append((nodes[a] + nodes[b]) & 0xFF)
    elif op == 3:  # XOR
        nodes.append(nodes[a] ^ nodes[b])
    elif op == 4:  # copy
        nodes.append(nodes[a])

# Constrain outputs 259-295
for i, target in enumerate(targets):
    s.add(nodes[259 + i] == target)

assert s.check() == sat
m = s.model()
flag = ''.join(chr(m[inp].as_long()) for inp in inputs)
print(flag)
# LsCTF2026{INTr0dUction_70_R3v3R$1NG1}
```

### Solver (`solve.py --challenge gates`)

Passes the assignment to the original executable and checks its `Correct!` response.

---

## 6. Flag

```
LsCTF2026{INTr0dUction_70_R3v3R$1NG1}
```
(Verified by binary output `Correct!`)

---

## 7. Lessons Learned

1. **Circuit constraint solving** — A byte-level circuit with known outputs is a perfect fit for Z3 bit-vector constraints.
2. **Ready field ≠ constant** — Nodes marked `ready` may still be recomputed; only `operation == 0` indicates a true constant.
3. **8-bit wraparound** — Z3's `BitVec(8)` naturally handles modulo-256 arithmetic.

---

## 8. Tools Used

- Python 3 with `z3-solver`
- Binary parsing (struct.unpack)
- `solve.py` — Packaged solver

---

## 9. Evidence and References

- `evidence/files/gates` — Original ELF binary
- `solve.py` — Packaged solver with Z3 constraints