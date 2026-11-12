# wintls

**Category:** Reverse Engineering
**Difficulty:** Easy
**Points:** 100
**Status:** Solved (Verified)

---

## 1. Challenge Overview

A Windows program that checks your flag by calling itself recursively. Follow the recursion and rebuild the flag it expects.

---

## 2. Initial Analysis

### Handout (`files.zip`)

Windows executable (PE32). The program recursively validates the flag character by character.

---

## 3. Investigation and Methodology

### Recursive Flag Checking

The program implements a recursive validation where each recursive call checks one character of the flag against expected values. By analyzing the recursion pattern and the comparison logic, the expected flag can be reconstructed.

### Flag Recovery

The flag was recovered through static analysis of the recursive checking function.

---

## 4. Flag

```
LsCTF2026{f%sAP$uT98Nv#FFHyrh2o+Lh0@8c9yoa98$ySoCW3rJPH3y&a83Xb}
```
(Verified from `rev/wintls/flag.txt`)

---

## 5. Current Status

**Solved but writeup incomplete.** The flag was recovered, but the detailed reverse engineering methodology has not been documented in this repository. The binary needs to be fully analyzed to produce a complete writeup.

---

## 6. Evidence and References

- `evidence/files.zip` — Original challenge archive
- `evidence/flag.txt` — Recovered flag
- `evidence/wintls_files/` — Extracted binary files

---

## 4. Vulnerability / Technical Discovery

*To be documented.*

## 5. Exploitation / Solution

*To be documented.*

## 6. Flag

*Flag to be documented upon solving.*

## 7. Lessons Learned

*To be completed.*

## 8. Tools Used

*To be completed.*

## 9. Evidence and References

*To be completed.*

