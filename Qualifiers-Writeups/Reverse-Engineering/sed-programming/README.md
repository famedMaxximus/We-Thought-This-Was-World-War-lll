# sed_programming

**Category:** Reverse Engineering
**Difficulty:** Legendary
**Points:** 700
**Status:** Unsolved (No verified flag)

---

## 1. Challenge Overview

Who needs a real programming language? This flag checker is written entirely in `sed`. Usage: `echo 'LsCTF2026{...}' | sed -f checker.sed`

---

## 2. Initial Analysis

### Handout (`files.zip`)

- `checker.sed` — sed script that validates the flag

### Checker Logic

The sed script implements a flag validator using only sed commands. The flag format regex is embedded:
```
/^LsCTF2026{[02-9A-HJ-Z_a-km-z]*}$/!{
```
This validates the flag format (LsCTF2026{...} with specific character set excluding 0, 1, l, o).

---

## 3. Current Status

**Unsolved.** The sed script is complex and has not been fully reverse engineered to extract the flag.

---

## 4. Flag

**None recovered** — Challenge remains unsolved.

---

## 5. Evidence and References

- `evidence/files.zip` — Original challenge archive
- `evidence/checker.sed` — The sed flag checker
- `evidence/ex/` — Extracted files

---

## 3. Investigation and Methodology

*Investigation not yet completed. Planned approach: [TODO]*

## 4. Vulnerability / Technical Discovery

*Challenge not yet solved. Analysis pending.*

## 5. Exploitation / Solution

*Challenge not yet solved. Analysis pending.*

## 6. Flag

**Status: Unsolved** — No flag recovered yet.

## 7. Lessons Learned

*To be completed upon solving.*

## 8. Tools Used

*To be completed upon solving.*

## 9. Evidence and References

*To be completed upon solving.*

