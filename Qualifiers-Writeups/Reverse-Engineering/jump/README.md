# jump

**Category:** Reverse Engineering
**Difficulty:** Hard
**Points:** 500
**Status:** Unsolved (No verified flag)

---

## 1. Challenge Overview

An AArch64 flag checker that likes jumping around. You may need `qemu-aarch64` or an ARM64 machine to run it.

---

## 2. Initial Analysis

### Handout (`files.zip`)

AArch64 ELF binary. The flag checker uses complex control flow with many jumps.

### Solver Scripts

Multiple solver scripts exist in the `jump/` directory:
- `solve.py`
- `solve_optimized.py`
- `solve_remaining.py`
- `solve_ptr.py`
- `solve_ptr2.py`
- `find_solutions.py`
- `full_search.py`
- `brute.py`
- `trace_checks.py`
- `emulate.py`
- `unicorn_emul.py`

These suggest extensive work was done on emulating and solving the binary, but no verified flag was recovered.

### Partial Flag Attempts

From the solver scripts, attempted flag formats include:
- `LsCTF2026{5h4k3_XXXXXXXXYYYYYYYYZZZZZZZZ}`
- `LsCTF2026{5h4k3_flagctf_lesotho_hackathon}`
- Various other attempts in `solve_ptr2.py`

---

## 3. Current Status

**Unsolved.** Significant effort invested (multiple solver scripts, unicorn emulation) but no verified flag recovered. The binary appears to be a complex flag checker with anti-analysis tricks.

---

## 4. Flag

**None recovered** — Challenge remains unsolved.

---

## 5. Evidence and References

- `evidence/files.zip` — Original challenge archive
- `evidence/solve*.py` — Multiple solver attempts
- `evidence/files/` — Extracted binary

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

