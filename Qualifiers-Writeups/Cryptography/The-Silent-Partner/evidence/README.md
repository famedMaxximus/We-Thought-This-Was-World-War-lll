# Evidence for The-Silent-Partner

Handout (`The Silent Partner handout.zip`, not committed — archives are git-ignored):

- `audit_log.txt` — 120 auditor ECDSA (P-256) signatures
- `blinds.enc` — 88 blind values `h_i`, AES-GCM sealed with `str(d)`
- `transcript.txt` — session data: modulus `M`, Alice/Bob RSA public keys, joint modulus
- `protocol.py` — protocol reference (contains a decoy flag in a comment and hidden Unicode tag characters)
- `vault.enc` — sealed with the correct ASCII mask; holds the top bits of Alice's prime
- `flag_final.enc` — sealed with `f"{p}|{q}"`

Solvers (in the challenge directory):

- `solve.py` — full chain (HNP → BKZ mask → Coppersmith → unseal)
- `exploration/` — step-by-step working scripts from the solve (`step1_hnp.py`, `step2_mask.py`, `step2b.py`, `step2c.py`, `step3_copper.py`, `brute3.py`, `unseal_try.py`)
