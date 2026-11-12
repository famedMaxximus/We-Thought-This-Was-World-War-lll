# Lesotho 2026 Cyber Security Hackathon — Finals Battle Plan

**Team:** We Thought This Was World War III  
**Event:** Lesotho 2026 Cyber Security Hackathon — Finals  
**Date:** 2026-11-16  
**Target:** 🥇 **1ST PLACE**  
**Current Rank:** 🥈 2nd Place (Qualifiers) — 27,360 pts  
**Gap to 1st:** 560 points

---

## 🎯 Mission Statement

> **Qualification was the warmup. Finals are where we take the crown.**

We finished 2nd in qualifiers with 27,360/32,890 points (83.2%). The gap to 1st (M47) is **560 points**. Our analysis shows **1,400+ points** are available in unsolved/partially-solved vaults. With focused execution, we can close the gap and take 1st.

---

## 👥 Team Roles & Responsibilities

| Member | Handle | Primary | Secondary | Tertiary | Comms Channel |
|--------|--------|---------|-----------|----------|---------------|
| **Captain** | famed_maxximus | Crypto / Pwn Lead | Flag submission | Team sync / Strategy | #captain |
| **Member** | Palesa Ntaote | Web / Forensics | OSINT | Flag verification | #web-forensics |
| **Member** | Napo Qheku | RE / Binary | Pwn assist | Tooling / Automation | #re-pwn |
| **Member** | s202321271 | Crypto / Math | Side-channels | Flag formatting | #crypto |

---

## ⏰ Time Allocation (8-Hour Window)

| Phase | Time | Duration | Focus | Owner |
|-------|------|----------|-------|-------|
| **Recon** | 0:00-0:30 | 30 min | Enumerate vaults, identify categories, prioritize | All |
| **Crypto/Forensics Sprint** | 0:30-2:00 | 90 min | Clear our strongest categories (target 50%+ vaults) | famed, s202321271 |
| **Pwn/RE Sprint** | 2:00-4:00 | 120 min | Parallel: RE (Napo), Pwn (famed), Crypto (s202321271) | All |
| **Web/ICS Sprint** | 4:00-6:00 | 120 min | Web (Palesa), ICS (famed), Web3 (Napo) | All |
| **Hard Vaults / Swarm** | 6:00-7:30 | 90 min | Team swarm on remaining high-value vaults | All |
| **Submission & Verify** | 7:30-8:00 | 30 min | Verify flags, bulk submit, confirm scoreboard | famed |

---

## 🎯 Vault Priority Matrix

| Priority | Vault | Category | Est. Points | Assigned | Status |
|----------|-------|----------|-------------|----------|--------|
| 🔴 **CRITICAL** | Pwn Master 2,3,6,7 | Pwn | ~400 | famed + Napo | Unsolved |
| 🔴 **CRITICAL** | jump, Quiz, sed | RE | ~300 | Napo | Unsolved |
| 🔴 **CRITICAL** | Operation Quthing Storm | ICS/OT | ~200 | famed | Partial |
| 🔴 **CRITICAL** | Web 10-module vault | Web | ~500 | Palesa | Unsolved |
| 🟡 **HIGH** | The Smuggled Archive | Forensics | ~500 | Palesa | Unsolved |
| 🟡 **HIGH** | Say Cheese | Forensics | ~500 | Palesa | Unsolved |
| 🟡 **HIGH** | Phone Home | Forensics | ~500 | Palesa | Unsolved |
| 🟡 **HIGH** | Homecoming (iPhone 8) | Forensics | ~500 | Palesa | Partial |
| 🟢 **MEDIUM** | Oil and Vinegar | Crypto | ~500 | s202321271 | Unverified |
| 🟢 **MEDIUM** | The Secret Between the Lines | Crypto | ? | s202321271 | Unsolved |
| 🟢 **MEDIUM** | Vault-Tec Flag 1 | Crypto | ? | famed | Unsolved |
| 🟢 **MEDIUM** | Morija Gate Register | Crypto | 500 | s202321271 | Unsolved |
| 🟢 **MEDIUM** | The Silent Partner | Crypto | ? | s202321271 | Unsolved |

**Total Available: ~1,400+ points** — We only need 560 to overtake M47.

---

## 🛠️ Pre-Staged Tooling & Automation

### Pre-Built Solvers (Ready to Run)
```bash
scripts/solvers/
├── crypto/
│   ├── squeamish_squash_solve.py
│   ├── macrodata_refinement_solve.py
│   ├── mohale_sensor_traces_solve.py
│   ├── verification_service_solve.py
│   └── ...
├── pwn/
│   ├── pwn_master_1_exploit.py
│   ├── pwn_master_4_exploit.py
│   └── ...
├── forensics/
│   ├── rocket_man_sms_extract.py
│   ├── smuggled_archive_carve.py
│   └── ...
├── web/
│   ├── ndigiwa_quiz_solver.py
│   ├── web_vault_scanner.py
│   └── ...
└── re/
    ├── jump_emulator.py
    ├── quiz_solver.py
    └── ...
```

### Automation Scripts (Ready)
- `scripts/utils/flag_formatter.py` — Normalize, validate, deduplicate flags
- `scripts/utils/scoreboard_monitor.py` — Live LCA scoreboard (10s refresh)
- `scripts/utils/flag_submitter.py` — Bulk submit with retries & deduplication
- `scripts/validate_repo.py` — Pre-finals validation

### Pre-Staged Environment
```bash
# One-command environment
docker build -t lsctf-finals .
docker run -it --rm -v $(pwd):/ctf lsctf-finals
```
Includes: Ghidra, pwntools, z3, fpylll, all solvers, automation scripts.

---

## 📡 Communications Protocol

### Discord Channels
| Channel | Purpose | Members |
|---------|---------|---------|
| #captain | Strategy, decisions, escalations | famed_maxximus |
| #crypto | Crypto/math discussion | famed, s202321271 |
| #re-pwn | RE/Pwn coordination | Napo, famed |
| #web-forensics | Web/Forensics coordination | Palesa, famed |
| #flags | **Flag submissions ONLY** | All (read), famed (write) |
| #scoreboard | Live score updates | All (read), bot (write) |
| #general | General chat, breaks | All |

### Flag Submission Format
```
SOLVED: <vault_name> <flag>
```
Example: `SOLVED: Pwn_Master_Level_2 LsCTF2026{example_flag_here}`

### Flag Verification Checklist (before submit)
- [ ] Format: `LsCTF2026{...}`
- [ ] Not in `submitted_flags.txt`
- [ ] Verified via solver/GCM tag/manual check
- [ ] Posted to #flags channel

---

## 🏁 Day-of Execution Checklist

### T-24 Hours (Nov 15)
- [ ] Docker image built & tested: `docker build -t lsctf-finals .`
- [ ] All solvers tested locally: `python scripts/solvers/.../solve.py`
- [ ] Flag submitter tested with LCA staging API
- [ ] Scoreboard monitor tested on LCA staging
- [ ] Discord channels created & permissions set
- [ ] `submitted_flags.txt` initialized (empty)
- [ ] `LCA_TEAM_TOKEN` and `LCA_SUBMIT_URL` env vars set
- [ ] Team briefing call (30 min)

### T-1 Hour (Finals Start - 1h)
- [ ] Docker container running: `docker run -it --rm -v $(pwd):/ctf lsctf-finals`
- [ ] Scoreboard monitor running on 2nd screen: `python scripts/utils/scoreboard_monitor.py`
- [ ] Discord voice connected
- [ ] Shared notes (Obsidian/Notion) open
- [ ] Water/snacks ready

### During Finals
- [ ] Every 30 min: Captain sync via voice
- [ ] Every flag: Post to #flags, Captain submits via `flag_submitter.py`
- [ ] Every hour: Captain updates strategy based on scoreboard
- [ ] Last 30 min: STOP new solves, focus on verification & submission

### Post-Finals
- [ ] Final scoreboard screenshot
- [ ] Export submitted flags
- [ ] Team debrief (what worked, what didn't)
- [ ] Update writeups with finals solves

---

## 🧠 Psychological & Physical Prep

| Aspect | Guideline |
|--------|-----------|
| **Sleep** | 8h night before, no all-nighters |
| **Nutrition** | High protein, complex carbs, hydration (2L water) |
| **Breaks** | 5 min every hour, 15 min every 3 hours |
| **Caffeine** | Max 400mg, stop 4h before end |
| **Posture** | Standing desk or regular stretches |
| **Mindset** | "We've done the work. Now execute." |

---

## 📊 Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| LCA API down | Low | Critical | Offline flag prep, manual submit backup |
| Network issues | Medium | High | Mobile hotspot backup, offline solvers |
| Flag format error | Low | Medium | Automated formatter + validator |
| Team burnout | Medium | High | Enforced breaks, rotation |
| M47 solves more | Medium | Medium | Focus on high-value vaults first |
| Tool failure | Low | Medium | Docker environment = consistent |

---

## 📈 Success Metrics

| Metric | Target |
|--------|--------|
| Final Rank | 🥇 1st Place |
| Points | > 28,000 (overtake M47's 27,920) |
| Vaults Solved | > 55/61 |
| First Bloods | > 5 |
| Submission Accuracy | > 95% |
| Zero missed submissions | 100% |

---

## 🗣️ Final Words

> **We've done the work. We've built the tools. We've mapped the terrain.**
> 
> **Now we execute.**
> 
> **Finals: 2026-11-16. Target: 1st Place.**
> 
> — *Team "We Thought This Was World War III"*

---

*Document Version: 1.0 | Last Updated: 2026-11-10 | Classification: TEAM INTERNAL*