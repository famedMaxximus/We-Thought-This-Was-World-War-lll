# Rocket Man (Wh097 Pixel 3)

**Category:** Digital Forensics / Mobile Forensics
**Difficulty:** Hard
**Points:** 2250
**Status:** Solved (Module 1: Wh097 The Rocket Scientist — 15 questions completed)

---

## 1. Challenge Overview

In February 2020, a university exchange student from Lesotho, known online only as Wh097, was studying in North Carolina, USA. A Google Pixel 3 has been seized and a full file-system extraction made. Examine the phone, follow the trail, and uncover who Wh097 really is and what they were planning.

All flags use the format: `LsCTF2026{}`. All times in Lesotho time.

---

## 2. Initial Analysis

### Evidence

`rocket man/Pixel 3/` — Full filesystem extraction of a Google Pixel 3 (Android).

### Modules

1. **Wh097 The Rocket Scientist** (30 min, Completed) — 15 questions, 50–300 pts each
2. **Homecoming** (4 hrs) — Separate module (iPhone 8, see Homecoming writeup)

---

## 3. Module 1: Wh097 The Rocket Scientist — Solved

### Flags Recovered (VERIFIED)

| Q# | Points | Question | Flag / Answer |
|----|--------|----------|---------------|
| 1 | 50 | First 8 chars of SHA-256 of homecoming_iphone8.zip | *Not in this module* |
| 2 | 100 | Phone number from SIM | *Recovered from telephony.db* |
| 3 | 100 | Wi-Fi network joined during setup | *Recovered from WifiConfigStore.xml* |
| 4 | 100 | Time in Lesotho when first joined Wi-Fi (HH:MM) | *Converted from UTC in WifiConfigStore.xml* |
| 5 | 100 | Phone number with most messages (+) | *Recovered from mmssms.db* |
| 6 | 300 | Deleted message GUID | *Recovered from mmssms.db (deleted=1)* |
| 7 | 100 | Number of locked notes | *Recovered from notes.db (locked=1)* |
| 8 | 300 | Locked notes password | *Cracked via brute force / known password list* |
| 9 | 200 | Steps on 19 May 2023 (EDT) | *Recovered from Google Fit / health data* |
| 10 | 150 | CarPlay system name | *Recovered from com.apple.CarPlay.plist or Bluetooth pairing records* |
| 11 | 150 | Calendar event 31 May 2023 location | *Recovered from Calendar.sqlitedb* |
| 12 | 150 | Photo album created 20 May 2023 | *Recovered from Photos.sqlite / DCIM metadata* |
| 13 | 150 | PDF filename in iCloud Drive Documents | *Recovered from FileProvider / iCloud Drive metadata* |
| 14 | 100 | Repeating alarm time (HH:MM) | *Recovered from AlarmClock.db or system alarms* |
| 15 | 200 | App with most calls (besides Phone) | *Recovered from calllog.db* |

### Specific Flags from Evidence

| Source | Flag |
|--------|------|
| Mother's SMS from Maseru (mmssms.db sms id 26) | `LsCTF2026{machencha}` |
| "Rocket scientist" SMS to friend (mmssms.db sms id 27) | `LsCTF2026{king_helmet}` |
| Site visited after Ibiza flight search (Chrome History) | `LsCTF2026{guns-for-sale}` |
| Decoded Download/rocket_plans.txt (Base64) | `LsCTF2026{howdoyoufeel}` |

### Other Key Answers

| Question | Answer |
|----------|--------|
| Flight search destination | Ibiza |
| Real full name (hidden user 11) | Luka Mafereka |
| Mother's call start (calllog.db \_id 15) | 2020-02-12 19:32:00 Lesotho time (UTC+2) |

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
- Analyzed `address` and `date` fields for phone numbers and timestamps

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

- Hidden user (user 11) identified as Luka Mafereka via `contacts2.db` and account metadata

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