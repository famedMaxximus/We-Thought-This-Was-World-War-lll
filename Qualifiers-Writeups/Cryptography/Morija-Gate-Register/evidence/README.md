# Evidence for Morija-Gate-Register

Handout (`Morija Gate Register handout.zip`, not committed — archives are git-ignored):

- `mokorotlo.py` — the cipher (16-bit, 6-round SPN); a copy is kept in the challenge directory
- `gate_register.csv` — 47,116 `serial,code` plaintext/ciphertext pairs
- `gate_notice.txt` — `iv 29c7` + 96 CBC ciphertext blocks

Solver files (in the challenge directory):

- `solver.py` — linear-cryptanalysis key recovery (`test` / `real` modes)
- `lc5.py` — cipher model, LAT, trail search, FWHT Algorithm 2
- `decrypt_notice.py` — CBC-decrypts the notice with the recovered keys

Recovered round keys (`keys.json`): `49e1 db10 8259 d464 67da 0c4d 3f35`
