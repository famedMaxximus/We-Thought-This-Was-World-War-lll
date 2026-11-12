# The Silent Partner

**Category:** Cryptography (ECDSA / lattices / Coppersmith)
**Status:** Solved (Accepted by the platform on 2026-11-08)

---

## 1. Challenge Overview

A three-party protocol (auditor, Alice, Bob) leaves behind an audit log of
ECDSA signatures, a sealed file of "blinds", a session transcript and two more
sealed files. The final flag is sealed under the factorisation of Alice's RSA
modulus. Getting there takes three chained attacks.

---

## 2. Initial Analysis

### Handout (`The Silent Partner handout.zip`)

| File | Contents |
|------|----------|
| `audit_log.txt` | 120 auditor ECDSA signatures on P-256 |
| `blinds.enc` | 88 values `h_i`, sealed with the auditor key `str(d)` |
| `transcript.txt` | modulus `M`, Alice `N_A`, Bob `N_B`, joint modulus |
| `protocol.py` | protocol reference code |
| `vault.enc` | sealed with the correct mask string |
| `flag_final.enc` | sealed with `f"{p}|{q}"` |

All `.enc` files are AES-GCM: `key = SHA256(label || "|" || secret)`, so every
wrong secret fails the tag check — a built-in verifier for each stage.

---

## 3. Investigation and Methodology

1. **Biased ECDSA nonces.** `sign_audit` uses `k = randbits(252) | 1` on P-256
   (n ≈ 2^256), so the top 4 bits of every nonce are zero.
2. **Noisy knapsack.** The audit requires
   `|centred(Σ mask_i·h_i mod M)| < 2^10` for the 88 blinds `h_i`.
3. **Partial prime leak.** The vault holds `p_hi` with 486 unknown low bits of
   Alice's 1024-bit prime.

---

## 4. Vulnerability / Technical Discovery

- **4-bit nonce bias** over 120 signatures → Hidden Number Problem.
- **Planted short vectors** in the knapsack lattice, well below the Gaussian heuristic.
- **Too many known prime bits** (538 of 1024) → Coppersmith / Howgrave-Graham.

---

## 5. Exploitation / Solution

1. **HNP → auditor key.** LLL on 90 signatures recovers the auditor key `d`.
   It matches `pub`. `blinds.enc` is sealed with `str(d)`.
2. **Orthogonal lattice → mask.** BKZ on `[I | h ; 0 | M]` finds 3 planted short
   vectors. Three printable combinations all pass the audit. Two are decoys; one
   of them looks like a flag (`LsCTF2026{ha_ke_motsoalle...}`). Only
   `silent_partner_signs_nothing_yet_the_audit_sum_balances_out_and_the_epoch_closes_clean_9`
   opens `vault.enc`.
3. **Coppersmith.** The vault gives `p_hi` with 486 unknown low bits of Alice's
   1024-bit prime. A Howgrave-Graham lattice (m=t=12, dim 24) factors `N_A`.
4. `flag_final.enc` is sealed with `f"{p}|{q}"` → the flag.

`N_B` (Bob) did not need to be factored.

### Decoys and traps

- A flag-shaped string in a `protocol.py` comment:
  `LsCTF2026{b0b_c0unsel_test_fixture_n0t_the_flag}`.
- The ASCII mask `LsCTF2026{ha_ke_motsoalle_ho_sa_utloe_ke_tse_ling___…}`
  passes the audit but does not open the vault.
- Invisible Unicode tag characters (U+E00xx) in `protocol.py`, `transcript.txt`
  and `audit_log.txt` hide text that claims a different "accepted" flag. That
  text is fake and was ignored. `solve.py` strips these characters before
  parsing JSON.

### Run

```
python3 solve.py ["handout/The Silent Partner handout"]
```

Requires `fpylll`, `sympy`, `pycryptodome`. Takes about 60 s, mostly the
BKZ-30 mask step.

---

## 6. Flag

```
LsCTF2026{Biased_ECDSA_N0nces_Then_N0isy_1attice_Then_C0ppersmith}
```

Verified by AES-GCM authenticated decryption of `flag_final.enc`, and accepted
by the platform.

---

## 7. Lessons Learned

1. **Even 4 bits of nonce bias break ECDSA** given enough signatures.
2. **Passing a check is not the same as being the answer** — three masks passed
   the audit; only the GCM tag on the next stage identified the right one.
3. **Leaking half a prime is fatal** — Coppersmith recovers the rest.
4. **Watch for hidden Unicode** — tag characters carried a prompt-injection-style fake flag.

---

## 8. Tools Used

- Python 3, `fpylll` (LLL, BKZ-30), `sympy`, `pycryptodome`

---

## 9. Evidence and References

- `solve.py` — full reproducible chain
- `exploration/` — per-step working scripts
- `evidence/README.md` — handout file list
