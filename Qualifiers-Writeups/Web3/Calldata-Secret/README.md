# Calldata Secret

**Category:** Web3 / Blockchain
**Difficulty:** Intermediate
**Points:** 300
**Status:** Solved (Verified)

---

## 1. Challenge Overview

A secret was used to create a contract's commitment hash. The constructor calldata is forever visible on-chain. Inspect the deployment transaction's input data, decode the secret, and call `reveal()`.

---

## 2. Initial Analysis

### Handout (`calldata-secret-player-kit.zip`)

- Player kit with contract source and deployment info
- Challenge runs on a local Anvil instance (or similar)
- Web interface at `http://ip:3000`

### Kit Structure (`kit/lsctf-kit-calldata-secret/`)

- `server/` — Node.js web server (Express)
- `server/index.js` — Main server logic
- `server/views/index.html` — Frontend
- `server/public/style.css` — Styling
- Smart contract (Solidity) with `reveal()` function

---

## 3. Investigation and Methodology

### On-Chain Analysis

The constructor calldata contains the encoded secret. By inspecting the deployment transaction's input data, the secret can be decoded.

### Contract Interaction

1. Decode the secret from deployment calldata
2. Call `reveal(secret)` on the contract
3. Contract returns the flag

### Solver (`solve.py`)

```python
# Calls reveal(secret) via anvil's unlocked account 0
# Fetches the flag, writes flag.txt
```

The solver uses the Anvil RPC endpoint to interact with the deployed contract.

---

## 4. Flag

```
LsCTF2026{calldata-secret_a5df52d066c3be7f16c8c3b8978ea69c}
```
(Verified from `Calldata Secret/flag.txt`)

---

## 5. Lessons Learned

1. **Constructor calldata is public** — All deployment data is visible on-chain forever.
2. **Secrets in constructors are not secret** — Anyone can inspect the deployment transaction.
3. **Anvil/local chains for CTF** — The challenge uses a local Anvil instance with unlocked accounts for easy interaction.
4. **Web3 + Web hybrid** — The challenge has a web frontend but the core logic is on-chain.

---

## 6. Tools Used

- Python 3: `web3.py` (or direct RPC calls)
- Anvil / Foundry (local Ethereum node)
- Browser dev tools (for web interface)

---

## 7. Evidence and References

- `evidence/calldata-secret-player-kit.zip` — Player kit
- `evidence/kit/lsctf-kit-calldata-secret/` — Server and contract source
- `evidence/solve.py` — Solver script
- `evidence/flag.txt` — Recovered flag

---

## 4. Vulnerability / Technical Discovery

*Challenge not yet solved. Analysis pending.*

## 5. Exploitation / Solution

*Challenge not yet solved. Analysis pending.*

## 6. Flag

**Status: Unsolved** — No flag recovered yet.

## 7. Lessons Learned

*To be completed upon solving.*

## 8. Tools Used

*To be completed upon solving.*

## 9. Evidence and References

*To be completed upon solving.*

