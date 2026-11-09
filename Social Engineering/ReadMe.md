# Social Engineering — Competition Playbook

> **AUTHORIZED SCOPE ONLY.** Everything here is for the **sanctioned Lesotho Cybersecurity
> Hackathon SE event**, performed against the **organizer-designated target(s)** under the
> published rules of engagement. Do not use these techniques on anyone outside that scope —
> it is illegal and gets you disqualified. When in doubt, ask a judge.

## 1. What an SE competition usually looks like

SE CTFs (modelled on DEF CON's SECTF / SECTF4Teens) run in one or more of these formats. Confirm
which at the briefing:

- **OSINT report + live call.** You get a target *organization* (and sometimes a persona). First you
  do **passive OSINT only** and submit a report of "flags" (facts) found online. Then, in a booth,
  you **place live phone calls (vishing)** to the org and capture more flags by eliciting info —
  *in front of judges and sometimes an audience*.
- **Phishing pretext design.** You craft a phishing email/SMS pretext for an authorized target and
  are scored on realism, pretext quality, and (in a lab) click/credential capture against **seeded
  test accounts**.
- **Tabletop / scenario.** You're given a scenario and must explain the attack chain, the pretext,
  and the defense — scored on method, not live action.
- **Capture-the-info live exercise.** Judges role-play staff; you elicit "flags" through conversation.

Each captured **flag** is a scored piece of info (e.g. "what browser do they use", "who is the
cleaning contractor", "is there a cafeteria", "what OS/AV", "name of the ERP system"). **Hard
flags** (passwords, actually visiting a malicious URL) are worth more.

## 2. Rules of engagement — read these FIRST (and the official ones)

Typical SE-CTF rules you MUST follow (always defer to the official brief):

- **No illegal acts.** No real financial/data theft, no breaking into systems, no touching
  out-of-scope people or systems.
- **No "shame" flags.** You may NOT elicit: social-security/national-ID numbers, real passwords
  used in production, credit-card numbers, or anything that truly endangers a person. (Some comps
  explicitly forbid these; getting one can *disqualify* you.)
- **No threats, no impersonating law enforcement / government**, no claiming a real emergency.
- **Record-keeping:** you typically must log every call, number dialed, and pretext used.
- **Time-boxed booth slot** (often ~20–25 min live). Prep is unlimited beforehand.
- **Passive OSINT only** before the live phase — no calling/emailing the target during recon.
- Be professional and courteous; the person on the phone is a real human doing their job.

## 3. The workflow

```
PHASE 1 — OSINT (passive)      -> osint-recon.md
    Build a dossier: org structure, tech stack, vendors, locations, people, lingo.
    Every fact = a potential flag. Cite the source for each (judges want provenance).

PHASE 2 — Pretext design       -> pretext-playbook.md
    Pick 2-3 pretexts that fit the dossier. Write a goal, a persona, a script, and
    objection handling for each. Prepare a flag-capture call sheet.

PHASE 3 — Live execution (booth)
    Run the strongest pretext first. Stay calm, use elicitation, bank easy flags early,
    pivot pretext if a call fails. Log everything.

PHASE 4 — Report / debrief
    Submit flags with evidence/sources. Note defenses you'd recommend (scores points in
    many comps + it's the ethical close).
```

## 4. Team roles for the live phase

| Role | Job |
|------|-----|
| **Caller** | The voice. Calm, confident, friendly. Runs the script, improvises. |
| **Navigator** | Sits beside caller with the dossier + flag sheet; passes notes, cues next question. |
| **Scribe** | Logs each call: number, who answered, flags captured, timestamp. |
| **OSINT backup** | Looks up anything that comes up live (passive only, if allowed). |

Rehearse the call out loud at least 3× before the slot. The #1 differentiator is **calm delivery**.

## 5. Scoring strategy

- **Bank easy flags first.** Open with low-risk questions ("are you open on weekends?", "what time
  does the office close?") to build the count and warm up the rapport before harder asks.
- **Rapport before requests.** People help people they like and trust. Spend the first 30–60s being
  a normal, slightly-rushed human with a reasonable reason to call.
- **Chain flags.** One fact unlocks the next pretext ("I see you use [ERP]; our rep [name from
  OSINT] asked me to confirm the version…").
- **Know when to stop.** If a target gets suspicious, thank them and hang up gracefully — don't burn
  the whole org. Move to a different department/number.
- **Document sources** for OSINT flags; judges reward verifiable provenance.

## 6. Files

| File | What |
|------|------|
| `ReadMe.md` | This playbook + rules. |
| `osint-recon.md` | Passive recon methodology, sources, dossier template, flag ideas. |
| `pretext-playbook.md` | Pretext design, vishing call flow, elicitation techniques, phishing pretext, objection handling. |

## 7. Ethics close (say this in your report)

SE wins because people are helpful. The point of the exercise is to **show the organization where
its awareness gaps are so it can train against them** — not to embarrass staff. Always frame your
report constructively and recommend defenses (verification procedures, callback policies, awareness
training). That professionalism scores points *and* is the reason this competition exists.
