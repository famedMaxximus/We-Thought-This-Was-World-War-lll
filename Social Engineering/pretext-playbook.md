# Pretext, Vishing & Elicitation Playbook

> Authorized target + published rules only. Never elicit truly sensitive data (passwords, national
> IDs, card numbers) — those are usually banned and can disqualify you. Be kind to the human on the
> line; this is an awareness exercise, not a trick on a person.

## 1. Anatomy of a pretext

A pretext = a believable **reason to be calling** that makes helping you the normal thing to do.

```
PRETEXT = Persona + Reason + Ask
  Persona : who you are (role that plausibly calls this dept)
  Reason  : why you're calling now (ties to a dossier fact -> credibility)
  Ask     : the small, reasonable thing you want (-> a flag)
```

Good pretexts are **low-stakes, routine, and time-pressured but polite**. People resist big weird
requests; they auto-pilot through small routine ones.

### Pretext bank (map each to a dossier hook)

| Persona | Reason (hook) | Flags it unlocks |
|---------|---------------|------------------|
| **New employee / intern** | "First week, trying to get set up, so sorry to bother you" | helpdesk number, VPN name, email setup, OS, wifi, who to ask for X |
| **IT / helpdesk callback** | "Following up on a ticket / a system update we're rolling out" | OS, AV, browser, remote tool, patch process (NOT passwords) |
| **Vendor / MSP** (use the real vendor name from OSINT) | "Confirming your environment before scheduled maintenance" | tech stack, versions, contacts |
| **Survey / researcher** | "Quick anonymous survey on workplace IT, 3 questions" | software, satisfaction, process details |
| **Delivery / facilities** | "Dropping off / scheduling service, need to confirm details" | office hours, who's on site, cleaning/security vendor, badge/entry |
| **Journalist / student** | "Writing a piece on your company, could you confirm…" | org facts, people, operations |

Pick personas that **match your voice and the dossier**. A 19-year-old caller as "the new intern"
is more believable than as "the CFO".

## 2. The vishing call flow (booth)

```
0:00  OPEN      Warm, slightly rushed, human. Greet by first name if you have it.
                "Hi, it's <name> — hope I caught you at an okay time?"
0:15  ANCHOR    State persona + reason tied to a real fact (credibility).
                "I'm the new starter in <dept>, <manager-from-OSINT> said to call you."
0:40  RAPPORT   One human beat. Mirror their tone. A little self-deprecation.
                "Honestly it's my first week and I'm a bit lost, you'd be saving me."
1:00  EASY ASKS Bank low-risk flags first (office hours, who handles X, what system).
2:00  CORE ASKS Work toward higher-value flags using elicitation (§3). Chain facts.
~end  CLOSE     Thank sincerely. Leave them feeling helpful, not used.
                "You've been a lifesaver, thank you so much — have a great day."
```

**Delivery rules that win:**
- **Smile while you talk** — it's audible, it warms the voice.
- **Slow down.** Nervous speed reads as suspicious. Pause, breathe.
- **Be slightly rushed, never aggressive.** Mild time pressure ("before my manager gets back")
  nudges helpfulness without alarm.
- **Sound like you expect a yes.** Confidence is contagious; so is doubt.
- If challenged, **don't argue** — concede small, re-anchor, or gracefully exit.

## 3. Elicitation techniques (get info without asking for it)

People resist direct interrogation but volunteer during normal conversation. Use:

- **Assumed knowledge / deliberate false statement.** State something slightly wrong; people love to
  correct you. "You're still on the old Windows 7 machines, right?" → "Oh no, we're on Windows 11
  now." (flag captured)
- **Quid pro quo.** Share a (harmless) tidbit first; reciprocity makes them share back.
- **Flattery + appeal to expertise.** "You clearly know this inside out — how does the ticket system
  handle that?" People explain their tools in detail when praised.
- **Bracketing.** Guess a range: "Is the team like, 10 people? More?" → they give the real number.
- **Feigned ignorance / helplessness.** "I'm so bad with this stuff, which program do I even open?"
- **The silence.** Ask, then stop talking. People fill silence with information.
- **Complaint / commiseration.** "Ugh, VPNs are the worst — what do you guys use, so I know what I'm
  in for?" Shared frustration lowers guard.
- **Funnel:** open broad ("how's the setup here?"), then narrow to the specific flag.

Never pressure for banned data. If a flag requires a password/ID/card number — **skip it**.

## 4. Objection handling

| They say | You say |
|----------|---------|
| "Who is this again?" | Re-anchor calmly: name + persona + the real reason/fact. Don't get defensive. |
| "I can't give that out." | "Totally fair! No worries at all —" then pivot to an easy flag or a different angle. |
| "Let me transfer you / call IT." | Great — a transfer often reaches a chattier dept. Or: "I don't want to be a bother, maybe you'd know…" |
| "How do I know you're legit?" | Offer a graceful out: "Of course — want to take my name and call back through the main line?" Then thank & exit (don't fabricate credentials). |
| Suspicious / hostile | Thank them, end politely. Protect the org's goodwill; try another number. |

## 5. Phishing pretext design (if the format includes it)

For authorized/lab targets and seeded test accounts only.

A phishing pretext scores on **plausibility**:
- **Sender** mimics a trusted source the dossier confirms (the real MSP, O365, HR, a known vendor).
  Use their real branding/lingo. (In the lab — never spoof real third parties outside the exercise.)
- **Context** ties to something true: a real event, system, or deadline from OSINT.
- **Call to action** is small and routine: "confirm your details", "review the shared doc",
  "your ticket is updated" → link to the **lab** capture page.
- **Pressure** is mild and plausible: a deadline, a routine policy, a helpful favor — not panic.
- **Polish:** correct logos, correct email format (`first.last@`), no typos, matching tone.

Red-team the pretext yourself: what would a trained user notice (mismatched domain, odd urgency,
unexpected link)? Note those in your report as the defense recommendations.

## 6. Pre-slot checklist

- [ ] Dossier printed, flag sheet ready, Navigator can find any fact in <5s
- [ ] Top 2–3 pretexts written with script + objection handling
- [ ] Target numbers / departments ordered (easy/chatty first)
- [ ] Call script rehearsed out loud 3×; caller is calm and smiling
- [ ] Scribe log template ready (number, who, flags, time)
- [ ] Banned-flag list taped to the desk so you never ask for one
- [ ] Graceful-exit line memorized
- [ ] Defense recommendations drafted for the report
```
```
