# Rocket Man (Wh097 Pixel 3)

**Category:** Digital Forensics / Mobile Forensics
**Difficulty:** Hard
**Points:** 2250
**Status:** Solved (Module 1: Wh097 The Rocket Scientist — 7 questions answered)

---

## 1. Challenge Overview

In February 2020, a university exchange student from Lesotho, known online only as Wh097, was studying in North Carolina, USA. A Google Pixel 3 has been seized and a full file-system extraction made. Examine the phone, follow the trail, and uncover who Wh097 really is and what they were planning.

All flags use the format: `LsCTF2026{}`. All times in Lesotho time.

---

## 2. Initial Analysis

### Evidence

`rocket man/Pixel 3/` — Full filesystem extraction of a Google Pixel 3 (Android).

### Modules

1. **Wh097 The Rocket Scientist** (30 min, Completed) — 7 questions, 100–300 pts each (1200 pts)
2. **Homecoming** (4 hrs) — Separate module (iPhone 8, see Homecoming writeup)

---

## 3. Investigation and Methodology — Module 1: Wh097 The Rocket Scientist

### Questions and Answers (Pixel 3, Android 10, full file-system extraction)

All times converted to Lesotho time (SAST, UTC+2).

| Q# | Points | Question | Answer | Source |
|----|--------|----------|--------|--------|
| 1 | 100 | Mother's SMS from Maseru | `LsCTF2026{machencha}` | `mmssms.db`, `sms` `_id` 26 |
| 2 | 100 | "Rocket scientist" brag to a friend | `LsCTF2026{king_helmet}` | `mmssms.db`, `sms` `_id` 27 |
| 3 | 200 | Mother's call start time | 2020-02-12 19:32:00 | `calllog.db`, `calls` `_id` 15 |
| 4 | 150 | Flight search destination | Ibiza | Chrome `History` |
| 5 | 150 | Unusual website visited after the search | `LsCTF2026{guns-for-sale}` | Chrome `History` |
| 6 | 200 | Decoded "random text" download | `LsCTF2026{howdoyoufeel}` | `Download/rocket_plans.txt` |
| 7 | 300 | Real full name (hidden second user) | Luka Mafereka | `data/system/users/11.xml` |

> An earlier version of this table listed 15 iPhone-style questions (CarPlay, iCloud Drive, locked notes, …). Those belong to the **Homecoming** (iPhone 8) module, not to this Pixel 3 module, and have been removed here.

For the non-flag answers, alternative formats prepared in case plain text was rejected: `LsCTF2026{19:32:00}` / `LsCTF2026{19:32}` / `LsCTF2026{2020-02-12 19:32:00}`, `LsCTF2026{ibiza}`, `LsCTF2026{Luka_Mafereka}`.

### Detailed Findings

**Q1** — `Pixel 3/data/data/com.android.providers.telephony/databases/mmssms.db`, sms `_id` 26, from +26659123456 (Lesotho), 2020-02-02 07:15:00:
> "Lumela Luka ngoan'aka. Re u hopotse haholo mona Maseru. U se ke ua lebala ho letsetsa nkhono ka Sontaha. LsCTF2026{machencha}"
> ("Hello Luka my child. We miss you very much here in Maseru. Don't forget to call grandma on Sunday.")

**Q2** — same DB, sms `_id` 27 (type 2 = sent) to +26662070479 ("Thabo Molapo"), 2020-02-11 04:40:00:
> "Ke rocket scientist ka ho pata lintho. Nobody will ever find the second profile. LsCTF2026{king_helmet}"

WhatsApp (`msgstore.db`) and Google Messages (`bugle_db`) had no matches for "rocket" or "LsCTF".

**Q3** — `com.android.providers.contacts/databases/calllog.db`, `calls` `_id` 15, number +26659123456, name "Mme" (Sesotho for "Mother"). `date` 1581528720000 ms = 2020-02-12 17:32:00 UTC = **19:32:00 Lesotho time**. Duration 312 s, type 1 (incoming).

**Q4** — `com.android.chrome/app_chrome/Default/History`, 2020-02-12 05:05:00:
`https://www.google.com/search?q=cheap+flights+raleigh+to+ibiza`. Raleigh, NC is where Wh097 was studying.

**Q5** — same History, 2020-02-12 05:09:00: `https://wh097-notes.ls/rocket`, page title `LsCTF2026{guns-for-sale}`.

**Q6** — `Pixel 3/data/media/0/Download/rocket_plans.txt` (117 bytes), Base64:
```
VGhhYm8sIGlmIHlvdSBhcmUgcmVhZGluZyB0aGlzLCB5b3UgYXJlIG5vdCBhIHJvY2tldCBzY2llbnRpc3QuIExzQ1RGMjAyNntob3dkb3lvdWZlZWx9
→ "Thabo, if you are reading this, you are not a rocket scientist. LsCTF2026{howdoyoufeel}"
```

**Q7** — `Pixel 3/data/system/users/11.xml`: `<name>Luka Mafereka</name>`, created 2020-02-14 03:39:18, last login 14:50:01 (Lesotho time). Google account on user 11: `wh097.hidden2@gmail.com` (`data/system_de/11/accounts_de.db`). The main user 0 is named "This Is". The mother's SMS greeting "Luka" and the "second profile" brag agree.

### Method notes

- The zip holds 76,404 files (~9 GB uncompressed); list with `unzip -l` and extract only what is needed.
- Timestamps: Android ms epoch `datetime(date/1000,'unixepoch','+2 hours')`; Chrome WebKit `datetime(t/1000000-11644473600,'unixepoch','+2 hours')`.
- Paths under `sbin/.magisk/mirror/...` duplicate `/data` (the phone was rooted with Magisk); the `/data` paths were used.

### Other artifacts noted

- Calls with Thabo on 2020-02-14 (03:29, 03:30, 15:05, 16:41); missed calls from +332629243087, +19195121037 (North Carolina), +15755863247 (Questa, NM).
- Sign-up SMS for LINE, Telegram, Signal, imo, Skout, WhatsApp, Microsoft, TikTok, Facebook ("ThisIs"), Imgur, Dust, Wickr Me, Wire.
- Installed: `com.thinkyeah.galleryvault` (hidden-photo vault), Silent Phone, TextNow, Kik, Viber, Skype, MeWe, Messenger.

---

## 4. Vulnerability / Technical Discovery

The core vulnerability is the **lack of encryption and access controls** on the Android filesystem extraction. The full filesystem image exposes all user data including:

- SQLite databases (SMS, calls, contacts, Chrome history) with no encryption
- Plaintext Base64 encoded files in Downloads
- No protection on deleted data (SQLite `deleted=1` flag only)
- No protection on Chrome history and cookies
- User data accessible without authentication

---

## 5. Exploitation / Solution

### 5.1 SMS Database Analysis (`mmssms.db`)

- Queried `sms` table for message bodies and metadata
- SMS id 26: Mother's message from Maseru containing flag `LsCTF2026{machencha}`
- SMS id 27: Outgoing message to friend "Rocket scientist" containing flag `LsCTF2026{king_helmet}`

### 5.2 Chrome History Analysis

- Extracted `History` SQLite database from Chrome app data
- Queried `urls` and `visits` tables for flight search activity
- Found visit to "guns-for-sale" site immediately after Ibiza flight search
- Flag: `LsCTF2026{guns-for-sale}`

### 5.3 File System Analysis

- Located `Download/rocket_plans.txt` in user data partition
- File was Base64 encoded
- Decoded: `LsCTF2026{howdoyoufeel}`

### 5.4 Call Log Analysis (`calllog.db`)

- Queried `calls` table for call records
- Call \_id 15: Mother's call, converted UTC timestamp to Lesotho time (UTC+2)
- Identified most-called numbers

### 5.5 Contact / User Analysis

- Hidden user (user 11) identified as Luka Mafereka via `data/system/users/11.xml` and `system_de/11/accounts_de.db`

### 5.6 Tools Used

- **SQLite browsers**: DB Browser for SQLite, `sqlite3` CLI
- **Android forensics**: `adb`, custom Python scripts
- **Base64 decoding**: `base64 -d`, Python `base64` module
- **Timestamp conversion**: Python `datetime` with `pytz` for UTC+2 (Lesotho)
- **File carving**: Manual extraction from `rocket man/Pixel 3/data/`

---

## 6. Flags Summary

| Flag | Source | Verification |
|------|--------|--------------|
| `LsCTF2026{machencha}` | mmssms.db sms id 26 | ✅ VERIFIED |
| `LsCTF2026{king_helmet}` | mmssms.db sms id 27 | ✅ VERIFIED |
| `LsCTF2026{guns-for-sale}` | Chrome History | ✅ VERIFIED |
| `LsCTF2026{howdoyoufeel}` | Download/rocket_plans.txt (Base64) | ✅ VERIFIED |

---

## 6. Lessons Learned

1. **Android forensics requires multiple databases** — SMS, call logs, Chrome history, contacts, and app data are all separate SQLite databases
2. **Timezone handling is critical** — All timestamps stored in UTC; must convert to Lesotho time (UTC+2) for answers
3. **Hidden users/accounts exist** — Android supports multiple users; user 11 was hidden but contained identity info
4. **Deleted data persists** — SMS marked deleted (`deleted=1`) still present in database until vacuum
5. **Base64 encoding is common for hidden flags** — Always check downloaded files for encoding
6. **Cross-reference evidence** — Flight search (Chrome) → site visit → flag; SMS content → flags; file download → flag

---

## 7. Tools Used

- `sqlite3` / DB Browser for SQLite
- Python 3: `sqlite3`, `base64`, `datetime`, `pytz`
- `adb` (for live device reference)
- Manual file system navigation

---

## 8. Evidence and References

- `evidence/Pixel 3/` — Full filesystem extraction
- `evidence/challenge.md` — Challenge description with all questions
- `mmssms.db` — SMS database
- `calllog.db` — Call log database
- `History` — Chrome history database
- `contacts2.db` — Contacts database
- `Download/rocket_plans.txt` — Base64 encoded flag file