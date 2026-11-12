# Evidence for Vault-Tec-Cold-Storage

Handout (`Vault-Tec Cold Storage handout.zip`, not committed — binaries are git-ignored):

- `coldmem.dmp` (1,810,874 bytes) — memory dump with `VTKEYC01`, `VTSESS01`, `VTLOGC01` records
- `tls_session.bin` (791 bytes) — TLS 1.2 handshake + one application-data record (suite 0x009c)
- `flag1.enc` (249 bytes) — Flag 1 (not recovered)

Derived: `enc_pms.bin` (128-byte ClientKeyExchange ciphertext), `server.der` (opaque 300-byte certificate body).

Solvers: `../scripts/solve_rsa.py`, `../scripts/solve_tls.py`, `../scripts/cs2.py`.
