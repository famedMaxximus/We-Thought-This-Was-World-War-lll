# A Signature From the Future

**Category:** Cryptography
**Difficulty:** Medium
**Points:** 300
**Status:** Solved (Verified)

---

## 1. Challenge Overview

Chronos Cryptographic Systems uses a **Winternitz one-time signature (WOTS)** with Winternitz parameter `w=16`, sitting under a 16-leaf Merkle tree. The signing leaf is chosen by the state, and the captured log signs several messages with the **same WOTS key** — catastrophic for a one-time signature scheme.

---

## 2. Initial Analysis

### Scheme (from `verify.py`)

- **WOTS**: `w=16` (4 bits per chain)
- **Message hash**: `SHA256("CHRONOS|v2|" + msg)[:5]` = 10 nibble "body" digits
- **Checksum**: 2-nibble `sum(15 - digit)` → 12 chains total
- **Chain**: length-16 hash ladder `block -> SHA256(chain||round||block)`
  - Secret = position 0, Public = position 15
  - Signature reveals chain value at position `digit`
  - Verifier advances to 15, hashes all 12 endpoints into leaf commitment
- **Merkle tree**: 16 leaves, `combine = SHA256("NODE" + l + r)`
- **Leaf selection**: `leaf = SHA256("IDX|" + state)[0] & 15`

---

## 3. Investigation and Methodology

### The Vulnerability — Reused One-Time Leaves

WOTS is **one-time**, but `leaf_index` maps the 32-bit state through only 4 bits, so many different states collide onto the same leaf. The captured log signs several messages with the **same WOTS key** (leaf 7).

### Attack

1. Target release order maps to **leaf 7** (commissioned). 5 captured records also land on leaf 7.
2. A hash chain can only be advanced **forward** (toward the public end). Across the 5 reused signatures, for each of the 12 chains take the revealed value with the **smallest digit** — the point closest to the secret we can reach.
3. The target message's digits are all **≥** those minimums for every chain, so we advance each captured value forward to the target digit → a valid forged signature for the frozen release order. (The checksum can't save it because the reused keys expose low enough points on every chain.)

### Merkle Path

All 16 leaves are published in `authorization.json`, so the sibling path for leaf 7 to the root is computed directly (`combine = SHA256("NODE"+l+r)`); verified it reconstructs the published `root`.

---

## 4. Vulnerability / Technical Discovery

**WOTS key reuse across different messages** — The leaf selection function has only 4 bits of entropy (16 leaves), so collisions are frequent. When multiple signatures use the same WOTS key (same leaf), the secret chain positions are exposed at various digits. Since chains only advance forward, the minimum exposed position per chain becomes the effective "secret" for forging any message whose digits are ≥ those minimums.

---

## 5. Exploitation / Solution

### Forgery Process

```python
# 1. Collect all signatures on leaf 7 from captured log
# 2. For each of 12 chains, find minimum digit revealed
# 3. For target message (leaf 7), compute its 12 digits + checksum
# 4. Advance each captured chain value from min_digit to target_digit
# 5. Compute leaf commitment from forged signature
# 6. Compute Merkle path from authorization.json (all 16 leaves known)
# 7. Build authentication.json with forged signature + Merkle path
```

### Verification

```bash
$ python3 verify.py authentication.json
accept
LsCTF2026{chronos-release-9c3e7a1b04d8}
```

The verifier then XOR-opens the capsule keyed on the forged signature bytes.

---

## 6. Flag

```
LsCTF2026{chronos-release-9c3e7a1b04d8}
```
(Verified by `verify.py` acceptance)

---

## 7. Lessons Learned

1. **WOTS is one-time** — The "one-time" in Winternitz OTS is not a suggestion. Reusing a key for different messages destroys security.
2. **Leaf selection entropy matters** — Mapping a 32-bit state to 4 bits (16 leaves) guarantees collisions. The leaf index must be derived from a collision-resistant hash of the message, not a small slice of state.
3. **Hash chains only go forward** — This property is what makes WOTS secure when used once, but when reused, the lowest exposed position becomes the effective secret.
4. **Merkle trees don't fix key reuse** — The tree only binds leaves to a root; it doesn't prevent the underlying OTS from being broken.
5. **Solved offline, stdlib only** — No external dependencies needed for the forgery.

---

## 8. Tools Used

- Python 3 (stdlib only: `hashlib`, `json`)
- `verify.py` — Provided verifier
- `authorization.json` — Published leaves and root

---

## 9. Evidence and References

- `evidence/verify.py` — Verification script
- `evidence/authorization.json` — 16 published leaves + root
- `evidence/target.json` — Target message and state
- `evidence/captured_log.json` — 5 signatures on leaf 7
- `authentication.json` — Forged artifact (saved)