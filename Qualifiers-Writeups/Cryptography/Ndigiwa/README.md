# Ndigiwa — The Assessment

**Category:** Cryptography / Web Exploitation
**Difficulty:** Medium
**Points:** 300
**Status:** Solved (Verified)

---

## 1. Challenge Overview

A portal littered with FAKE flags ("Careless ones submit the first shiny string they find"). The real path: base32 hint in HTML → hidden `/assessment` page → timed quiz decoding an obscured country name → answer its CONTINENT → survive every encoding before global timer runs out → "Assessment passed" page issues an exam SLIP (SVG) → the REAL flag is embedded as a comment inside the slip, NOT on the pass page.

---

## 2. Initial Analysis

### Lab Instance

`https://5dc944d667d4.labs.ctfroom.com` (per-account instance)
Signed in as `"A. Kamau - BIT/TOUR-210"`

### Decoys Everywhere

Home page / courses / assessment pages sprinkled with decoy flags in HTML comments:
```
LsCTF2026{f4k3_fl4g_try_h4rd3r}
LsCTF2026{almost_but_n0p3}
LsCTF2026{th1s_1s_n0t_1t_br0}
LsCTF2026{n0t_fr0m_th3_st4rt_p4g3}
LsCTF2026{p4ss_p4g3_1s_n0t_3n0ugh}        ← on "passed" page
LsCTF2026{n0t_th3_r3al_0n3_k33p_l00k1ng}  ← labelled "decoy:" in slip
```
**All are red herrings.**

### Useful Hint

Home page comment:
```html
<!-- exam-note: F5QXG43FONZW2ZLOOQ====== -->
```
Base32 decodes to `/assessment`.

---

## 3. Investigation and Methodology

### The Hidden Assessment

1. `GET /assessment` → "Start assessment" form (POST action=start)
2. Flask signed session cookie issued; keep a cookie jar
3. `POST action=start` → 302 → `GET /assessment` shows a question:
   ```html
   <p class="timer" data-deadline="...">Time allowed: 30s ...</p>
   Where is <span id="encoded">01001110 01100101 ...</span> located?
   <script id="challenge-data">{"encoded":"...","q":1}</script>
   ```
   Answer with the **CONTINENT in plaintext**.

Each question:
- Obscures a **COUNTRY name** with a random encoding
- POST `action=answer&answer=<Continent>`
- Per-question timer AND tight global time budget → **must be solved by SCRIPT**

Number of questions: random (~30-40). Answer all in time → "Assessment passed".

### Encodings Observed

| Encoding | Example | Decodes To |
|----------|---------|------------|
| Plain text | "India" | India |
| Binary (8-bit groups) | `01001110 01100101 ...` | Nepal |
| Hex | `45637561646f72` | Ecuador |
| Octal (space sep) | `124 157 156 147 141` | Tonga |
| Decimal ASCII (space sep) | `120 145 162 165` | Peru |
| Morse (/ = word gap) | `-.-. --- ... - .- / ...` | Costa Rica |
| Base32 | `I5SXE3LBNZ4Q====` | Germany |
| Base64 | `TmVwYWw=` | Nepal |
| Base58 | `3X2CcMtCa4` | Bolivia |
| Atbash | `Senapr` | France |
| ROT13 | `Pbybzovn` | Colombia |
| ROT47 | `qC2K:=` | Brazil |
| Caesar (various shifts) | `Bshsf` | Japan |
| URL-encoded | `South%20Africa` | South Africa |

Country → continent mapping done with `pycountry_convert`.

---

## 4. Vulnerability / Technical Discovery

| Component | Flaw |
|-----------|------|
| Hidden endpoint | `/assessment` not linked, only discoverable via Base32 hint in HTML comment |
| Timed quiz | Multi-encoding, timer-gated quiz only solvable by automated script |
| Decoy flags | Multiple planted flags to catch "first shiny string" submitters |
| Real flag location | Embedded in SVG exam slip comment, NOT on the pass page |

---

## 5. Exploitation / Solution

### Solver Core Logic

```python
import re, base64, codecs, urllib.parse, requests
import pycountry_convert as pcc

B = "https://5dc944d667d4.labs.ctfroom.com"
s = requests.Session()
CONT = {"AF":"Africa","AS":"Asia","EU":"Europe","NA":"North America",
        "SA":"South America","OC":"Oceania","AN":"Antarctica"}

# try_decode(enc) returns candidate plaintexts for ALL encodings above
#   binary / octal / decimal / morse / hex / base32 / base64 / base58 /
#   atbash / rot13 / rot47 / caesar(1..25) / url-decode / plain

def to_continent(name):
    name = re.sub(r'[^A-Za-z \-]','',name).strip()
    for n in (name, name.title()):
        try:
            a2 = pcc.country_name_to_country_alpha2(n)
            return CONT[pcc.country_alpha2_to_continent_code(a2)]
        except: pass

# Flow:
s.get(B+"/assessment")
s.post(B+"/assessment", data={"action":"start"})
r = s.get(B+"/assessment")
while True:
    m = re.search(r'id="challenge-data">(\{.*?\})</script>', r.text)
    enc = json.loads(html.unescape(m.group(1)))["encoded"]
    cont = next(c for d in try_decode(enc) if (c:=to_continent(d)))
    r = s.post(B+"/assessment", data={"action":"answer","answer":cont})
    if '"encoded"' not in r.text:      # pass or fail page
        break

# On success: fetch SLIP with same session cookie
# slip_url = re.search(r'/assessment/slip/[^"]+', r.text).group(0)
slip = s.get(B + slip_url).text
# Real flag in SVG comment: <!-- LsCTF2026{Int3rv13w_p@ss3d_cOngrats!!!} -->
```

**Key point: speed** — Global deadline, so keep one persistent `requests.Session` (keep-alive) and zero manual delay.

---

## 6. Flag

```
LsCTF2026{Int3rv13w_p@ss3d_cOngrats!!!}
```
(Verified in SVG exam slip comment)

---

## 7. Lessons Learned

1. **Don't grab the first flag-shaped string** — Several decoys planted precisely to catch that.
2. **Hidden content pointed to via encoded hint** (Base32), not a menu link.
3. **Automate-the-CTF challenge** — Multi-encoding, timer-gated quiz only solvable by a script that recognizes every encoding and resolves country → continent programmatically.
4. **Proof of completion (exam slip) carries the real flag** — Always inspect downloaded/generated files (SVG/PDF/images) for embedded data.
5. **pycountry_convert** — Essential for country→continent mapping; install locally with `pip install --target ./pylibs pycountry_convert`.

---

## 8. Tools Used

- Python 3: `requests`, `pycountry_convert`, `base64`, `codecs`, `re`, `json`, `html`
- Browser dev tools (initial recon)
- `pip install --target ./pylibs pycountry_convert` (local install for isolated env)

---

## 9. Evidence and References

- `evidence/home_page.html` — HTML with Base32 hint
- `evidence/assessment_page.html` — Quiz page structure
- `evidence/slip.svg` — Exam slip with real flag in comment
- `solve.py` — Complete automated solver