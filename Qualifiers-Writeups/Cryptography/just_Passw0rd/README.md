# just_Passw0rd

**Category:** Cryptography / Reverse Engineering
**Difficulty:** Easy
**Points:** Unknown
**Status:** Solved (Verified)

---

## 1. Challenge Overview

An ELF binary with a straightforward password check. The complete flag is embedded as an ordinary printable string in the binary.

---

## 2. Initial Analysis

### Handout (`files.zip` → `files/just_password`)

ELF binary containing:
- Complete flag in a printable string
- Password check: `main` requires 8-byte input, loads immediate `0x5778413832553370`, compares its 8 bytes with input

---

## 3. Investigation and Methodology

### Password Recovery

On little-endian x86-64, the immediate `0x5778413832553370` is the string:
```
p3U28AxW
```

Supplying this password prints `Correct!` and the flag.

### Flag Extraction

```bash
strings files/just_password
# → LsCTF2026{1234_P@ssw0rd_admin_toor_qwerty}
```

Also recoverable via `objdump -d -Mintel files/just_password`.

---

## 4. Vulnerability / Technical Discovery

| Component | Flaw |
|-----------|------|
| Password storage | Hardcoded immediate value in binary (trivial to extract) |
| Flag storage | Plaintext string in binary (no encryption/obfuscation) |

---

## 5. Exploitation / Solution

```bash
# Extract flag
strings files/just_password | grep LsCTF

# Or run with recovered password
./files/just_password <<< "p3U28AxW"
# → Correct!
# → LsCTF2026{1234_P@ssw0rd_admin_toor_qwerty}
```

### Solver (`solve.py`)

Extracts flag from ELF and runs binary with recovered password, asserting success message appears.

---

## 6. Flag

```
LsCTF2026{1234_P@ssw0rd_admin_toor_qwerty}
```
(Verified by binary output `Correct!`)

---

## 7. Lessons Learned

1. **Hardcoded secrets in binaries are trivial to extract** — `strings` and `objdump` reveal them immediately.
2. **Password checks against immediates** — The comparison value is visible in the disassembly.
3. **Flag in plaintext** — No need to reverse the logic fully; the flag is just sitting in the binary.

---

## 8. Tools Used

- `strings` — Extract printable strings
- `objdump -d -Mintel` — Disassembly
- Python 3 (solver)

---

## 9. Evidence and References

- `evidence/files/just_password` — Original ELF binary
- `solve.py` — Packaged solver