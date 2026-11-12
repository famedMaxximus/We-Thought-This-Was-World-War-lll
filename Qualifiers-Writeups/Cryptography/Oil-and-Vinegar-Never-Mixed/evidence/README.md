# Evidence for Oil-and-Vinegar-Never-Mixed

Handout (`Oil and Vinegar, Never Mixed handout.zip`, not committed — binaries are git-ignored):

- `uov.py` — UOV over GF(16) (N=96, V=72, O=24, M=24) + `unseal` helper (contains decoy flags and hidden Unicode tag text)
- `device_prng.py` — Geffe generator, LFSRs of length 19/21/23
- `selftest.bin` — 4096 keystream bits
- `pubkey.bin` — 24 upper-triangular 96×96 public forms
- `reports.bin` — 96 masked 96×96 matrices
- `sealed_a.enc`, `flag.enc` — AES-GCM sealed blobs

Solvers (in the challenge directory): `solve.py`, `geffe.c`.
