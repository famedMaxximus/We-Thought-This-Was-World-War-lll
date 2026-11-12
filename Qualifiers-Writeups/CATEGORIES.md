# Challenge Categories

**Event:** Lesotho 2026 Cyber Security Hackathon (LsCTF)
**Team:** We Thought This Was World War

This document maps each challenge to its primary cybersecurity category. Challenges may involve multiple disciplines; the primary category reflects the core skill required.

## Category Definitions

- **Cryptography** — Mathematical cryptanalysis, protocol flaws, key recovery, side-channel attacks on crypto
- **Web Exploitation** — HTTP/HTTPS application flaws: IDOR, XSS, SQLi, template injection, auth bypass
- **Reverse Engineering** — Static/dynamic analysis of binaries, bytecode, or scripts to understand logic
- **Binary Exploitation / Pwn** — Memory corruption, ROP, format strings, heap exploitation, kernel exploits
- **Digital Forensics** — File system analysis, memory forensics, network traffic analysis, artifact recovery
- **Steganography** — Hidden data in images, audio, video, or other media
- **OSINT** — Open-source intelligence gathering from public sources
- **Network Security** — Protocol analysis, traffic interception, MITM, DNS tunneling
- **ICS / OT Security** — Industrial control systems, SCADA, PLC, Modbus, safety systems
- **Hardware Security** — Side-channel analysis (power, EM), fault injection, firmware extraction
- **Programming / Scripting** — Algorithmic challenges, custom VMs, esoteric languages
- **Web3 / Blockchain** — Smart contract analysis, calldata inspection, on-chain forensics
- **Mobile Forensics** — Android/iOS file system, app data, comms analysis
- **Miscellaneous** — Challenges not fitting other categories

---

## Challenges by Category

### Cryptography (27 challenges)

| Challenge | Sub-category | Difficulty | Points | Status |
|-----------|--------------|------------|--------|--------|
| Squeamish Squash | ECDSA nonce reuse, RSA-260, AES-GCM | Hard | 700 | Partial (Flag 1 only) |
| Macrodata Refinement | DNS exfil, LSB stego, LFSR correlation | Hard | 500 | Solved (2 flags) |
| Detention for the Curious | IDOR, alias normalization, AES-GCM | Intermediate | 300 | Solved |
| Same Shape, Different Fence | DH (Pohlig-Hellman), Knapsack (LLL), Sigma protocol | Hard | 500 | Solved |
| Young Sheldow | PNG trailer, ZipCrypto, Fermat, Pohlig-Hellman | Intermediate | 300 | Solved |
| Namunya Sacco | Affine AES S-box, linear algebra | Easy | 100 | Solved |
| Ninety-Six Boxes | Noisy graph isomorphism, AES-GCM | Hard | 500 | Solved |
| Seven Locks, One Lie | RSA, AES-GCM nonce reuse, LCG, ECDSA, LenExt, Shamir, Padding Oracle | Medium | 300 | Solved |
| A Signature From the Future | WOTS, Merkle tree, leaf reuse | Medium | 300 | Solved |
| Enkapune 1 | XOR, path traversal, source disclosure | Medium | 300 | Solved |
| Enkapune 2 | RSA (Wiener), XOR, file carving | Easy | 100 | Solved |
| Nonce upon a Time | Schnorr nonce reuse, SHA-256 stream | Medium | 300 | Solved |
| The Secret Between the Lines | Polynomial interpolation, Shamir, SHAKE256 | Medium | ? | Unsolved |
| Vault-Tec Cold Storage | Coppersmith, TLS 1.2 RSA, AES-GCM | Hard | ? | Partial (Flag 2 only) |
| Verification Service | LWE (Kannan embedding), Franklin-Reiter | Hard | 500 | Solved |
| Oil and Vinegar, Never Mixed | UOV, Geffe PRNG, correlation attack | Hard | 500 | Unverified |
| Rick's Portal Auth System | Unknown | Intermediate | 300 | Unsolved |
| Ndigiwa | Multi-encoding quiz automation, SVG comments | Medium | 300 | Solved |
| just_Passw0rd | String extraction, password comparison | Easy | ? | Solved |
| recursive | Recursive table indexing | Easy | ? | Solved |
| gates | Byte circuit constraints (Z3) | Easy | ? | Solved |
| Wubba Lubba Dub Cipher | Vigenère, AES-GCM | Easy | ? | Solved |
| Everything, Almost | NTRU (partial key), meet-in-the-middle | Hard | ? | Solved (2 flags) |
| Mohale Sensor Traces | 1st/2nd order CPA, AES-GCM | Hard | ? | Solved (2 flags) |
| Morija Gate Register | Unknown cipher, 4-digit codes | Hard | 500 | Unsolved |
| The Silent Partner | Unknown | ? | ? | Unsolved |
| Vault Description: Attachment Included | SMTP, base64, attachment extraction | Intermediate | 300 | Solved |

### Binary Exploitation / Pwn (7 challenges)

| Challenge | Sub-category | Difficulty | Points | Status |
|-----------|--------------|------------|--------|--------|
| Pwn Master Level 1 | Stack overflow, printf pointer overwrite | Intermediate | 100 | Local only |
| Pwn Master Level 2 | Unknown | Intermediate | 100 | Unsolved |
| Pwn Master Level 3 | Unknown | Intermediate | 100 | Unsolved |
| Pwn Master Level 4 | Unknown | Intermediate | 300 | Solved |
| Pwn Master Level 5 | Unknown | Intermediate | ? | Solved |
| Pwn Master Level 6 | Unknown | Intermediate | 300 | Unsolved |
| Pwn Master Level 7 | Unknown | Intermediate | 300 | Unsolved |

### Reverse Engineering (4 challenges)

| Challenge | Sub-category | Difficulty | Points | Status |
|-----------|--------------|------------|--------|--------|
| wintls | Recursive flag checker (Windows) | Easy | 100 | Solved |
| Quiz | ELF quiz binary | Easy | 100 | Unsolved |
| jump | AArch64 flag checker with jumps | Hard | 500 | Unsolved |
| sed_programming | sed flag checker | Legendary | 700 | Unsolved |

### Digital Forensics (5 challenges)

| Challenge | Sub-category | Difficulty | Points | Status |
|-----------|--------------|------------|--------|--------|
| The Smuggled Archive | PCAP carving, ZIP extraction | Hard | 500 | Unsolved |
| Say Cheese | HTTP image carving, stego | Hard | 500 | Unsolved |
| Phone Home | C2 beacon analysis, PCAP | Hard | 500 | Unsolved |
| Rocket Man | Android Pixel 3 full filesystem | Hard | 2250 | **Solved (Module 1: 4 flags)** |
| Homecoming | iOS iPhone 8 full filesystem | Hard | ? | Partial |

### Web Exploitation (3 challenges + 10-module vault)

| Challenge | Sub-category | Difficulty | Points | Status |
|-----------|--------------|------------|--------|--------|
| Web Exploitation (10 modules) | Various web flaws | Intermediate | 3000 | Unsolved |
| Ndigiwa | Web/Crypto hybrid | Medium | 300 | Solved |
| Detention for the Curious | Web/Crypto hybrid | Intermediate | 300 | Solved |

### Web3 / Blockchain (1 challenge)

| Challenge | Sub-category | Difficulty | Points | Status |
|-----------|--------------|------------|--------|--------|
| Calldata Secret | Constructor calldata, reveal() | Intermediate | 300 | Solved |

### ICS / OT Security (1 challenge)

| Challenge | Sub-category | Difficulty | Points | Status |
|-----------|--------------|------------|--------|--------|
| Operation Quthing Storm | Firmware analysis, Modbus, SCADA | Hard | 4450 | Partial |

### Hardware Security (1 challenge)

| Challenge | Sub-category | Difficulty | Points | Status |
|-----------|--------------|------------|--------|--------|
| Mohale Sensor Traces | Power analysis (CPA) | Hard | ? | Solved (2 flags) |

### Steganography (covered within other challenges)

- Young Sheldow: PNG trailer data
- Macrodata Refinement: PNG LSB column-major
- Wubba Lubba Dub Cipher: Text-based stego
- Say Cheese: Image stego (unsolved)

### OSINT (covered within other challenges)

- Squeamish Squash: RSA-260 factorization via Twitter
- Enkapune 1: robots.txt, hidden paths

---

## Cross-Category Challenges

Many challenges span multiple categories. The table below shows the primary category (used for directory placement) and secondary categories involved.

| Challenge | Primary | Secondary |
|-----------|---------|-----------|
| Squeamish Squash | Cryptography | OSINT, Steganography |
| Macrodata Refinement | Cryptography | Network Security, Steganography, Programming |
| Detention for the Curious | Cryptography | Web Exploitation |
| Same Shape, Different Fence | Cryptography | Programming (LLL) |
| Young Sheldow | Cryptography | Steganography, Digital Forensics |
| Enkapune 1 | Cryptography | Web Exploitation |
| Ndigiwa | Cryptography | Web Exploitation, Programming |
| Verification Service | Cryptography | Programming (Lattice) |
| Oil and Vinegar, Never Mixed | Cryptography | Programming (Correlation) |
| Everything, Almost | Cryptography | Programming (Meet-in-the-middle) |
| Mohale Sensor Traces | Cryptography | Hardware Security |
| Vault-Tec Cold Storage | Cryptography | Network Security (TLS) |
| Calldata Secret | Web3 | Web Exploitation, Cryptography |
| Operation Quthing Storm | ICS/OT | Digital Forensics, Reverse Engineering |
| Rocket Man | Digital Forensics | Mobile Forensics |
| Homecoming | Digital Forensics | Mobile Forensics |

---

*Last updated: 2026-11-10*