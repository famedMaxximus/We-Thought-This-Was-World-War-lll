# Contributing Guidelines

Thank you for considering contributing to the Lesotho CTF Writeups repository! This document outlines the standards and process for contributions.

## Contribution Types

We welcome:
- **New challenge writeups** — Complete, verified solutions for unsolved challenges
- **Corrections/improvements** — Fixes to existing writeups (technical accuracy, clarity, formatting)
- **Additional evidence** — Solver scripts, PCAPs, binaries, screenshots
- **Verification** — Independent reproduction of unverified flags
- **Tooling** — Validation scripts, automation, helper utilities

## Writeup Standards

All writeups **must** follow the standard template:

```markdown
# Challenge Name

**Category:** Cryptography / Web / Forensics / etc.
**Difficulty:** Only if known
**Points:** Only if known
**Status:** Solved / Partially Solved / Unverified

## 1. Challenge Overview
## 2. Initial Analysis
## 3. Investigation and Methodology
## 4. Vulnerability / Technical Discovery
## 5. Exploitation / Solution
## 6. Flag
## 7. Lessons Learned
## 8. Tools Used
## 9. Evidence and References
```

### Requirements

1. **Accuracy over aesthetics** — A correct writeup with rough formatting beats a beautiful but wrong one
2. **Verified flags only** — Never mark a flag as VERIFIED without authenticated decryption (GCM tag, signature, or direct reproduction)
3. **No fabrication** — Do not invent flags, exploit steps, challenge descriptions, or results
4. **Cite evidence** — Link to supporting files in `evidence/` directory
5. **Professional terminology** — Use correct cybersecurity terms
6. **No AI-isms** — Write in clear, direct English; avoid filler phrases

## Verification Standards

| Status | Requirements |
|--------|--------------|
| **VERIFIED** | GCM tag check passes, signature verifies, or solver reproduces from original artifacts |
| **UNVERIFIED** | Flag reported but not independently reproduced; clearly labeled |
| **PARTIAL** | Multi-flag challenge; only some flags recovered |
| **LOCAL_ONLY** | Works locally but remote flag not captured |

## Submission Process

1. Fork the repository
2. Create a branch: `git checkout -b writeup/challenge-name`
3. Add challenge directory under correct category with:
   - `README.md` (following template)
   - `evidence/` (supporting files)
   - `solve.py` or exploit script (if applicable)
4. Update `FLAG_INDEX.md` and `CATEGORIES.md`
5. Run validation: `python3 scripts/validate_repo.py`
6. Submit PR with clear description

## Flag Handling

- **Never** commit flags for unsolved/active challenges
- **Only** include flags from the LsCTF 2026 event (already concluded)
- Mark unverified flags clearly with `⚠️ UNVERIFIED`
- Do not modify flag format to fit expectations

## Code Quality

- Solver scripts should be reproducible (`python3 solve.py <handout_dir>`)
- Document dependencies (requirements.txt or inline comments)
- Prefer standard library; note external deps
- Include verification assertions (GCM tag checks, etc.)

## Review Checklist

Before submitting, verify:
- [ ] Writeup follows template
- [ ] Flag status correctly labeled
- [ ] No fabricated technical details
- [ ] Evidence files in `evidence/`
- [ ] Solver script works (if included)
- [ ] FLAG_INDEX.md updated
- [ ] CATEGORIES.md updated (if new challenge)
- [ ] Validation script passes

## Questions?

Open an issue for discussion before starting major work.

---

*These guidelines ensure the repository remains a trustworthy, high-quality resource for the cybersecurity community.*