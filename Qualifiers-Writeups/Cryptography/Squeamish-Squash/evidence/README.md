# Evidence for Squeamish-Squash

Handout (`Squeamish Squash handout.zip`, not committed — `.txt`/`.enc` artifacts are git-ignored):

- `signatures.txt` — secp256k1 public key `Q`, two ECDSA signatures sharing `r`
- `ciphertext.txt` — RSA-260 ciphertext (decimal)
- `flag1.enc` — Flag 1 AES-GCM blob
- `flag.txt` — secp256k1 point `P` + 69-byte Flag 2 blob

Hints (`Squeamish Hints/`): `Flag1 hint.wav` (Morse + spectrogram), `Flag2 hint1.pdf` (lunar alphabet), and the later `seed2.png` final hint.

Solver: `../solve.py` (Flag 1 verified; Flag 2 harness).
