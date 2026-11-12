# ☠ WE THOUGHT THIS WAS WORLD WAR 3
## COMPLETE MASTER SPECIFICATION — ATTACK & DEFENCE CYBER OPERATIONS COMMAND CENTRE

**Project:** We THOUGHT THIS WAS WORLD WAR 3  
**Classification:** Competition Operations Platform  
**Mode:** Attack & Defence CTF  
**Primary objective:** Maximize legitimate competition performance, preserve our services, coordinate four operators, collect and submit genuine flags, and maintain continuous defensive intelligence.

**OFFICIAL TAGLINE:**

# SEE EVERYTHING. PROTECT EVERYTHING. MISS NOTHING. ☠

---

# 0. YOUR ROLE

You are Claude Code acting as a senior:

- Cybersecurity systems architect.
- Attack & Defence CTF engineer.
- Defensive security engineer.
- Python backend developer.
- React and TypeScript frontend developer.
- Automation engineer.
- Network intelligence analyst.
- Incident response specialist.
- UI/UX and visual effects designer.
- DevOps and infrastructure engineer.

You are responsible for inspecting, building, integrating, testing, documenting, and verifying this complete system.

This is not a simple dashboard or a collection of scripts. It must be a real, persistent, modular, automated competition command centre.

The system must operate independently of Claude Code once deployed.

**The project name must always appear exactly as:**

`We THOUGHT THIS WAS WORLD WAR 3`

Do not rename it. Do not write WORLD WAR III. Do not change the capitalization. Do not shorten the title.

---

# 1. ORIGINAL PROJECT SPECIFICATION MUST BE PRESERVED

Before implementing anything, inspect the existing project and read its entire `CLAUDE.md`.

The original specification contains important files and requirements. Preserve and integrate them rather than replacing them with a simplified implementation.

Original required assets:

- `assets/ww3_sesotho.py`
- `assets/ww3_sesotho_web.html`
- `assets/ww3_banner.html`
- `tools/daemon.py`
- `tools/deploy_calling_card.py` — retain the module name for compatibility, but implement only authorized, non-invasive local demonstration and cleanup functions; do not deploy banners or modify other teams' systems.
- `tools/plant_canaries.py`
- `tools/verify_kit.py`
- `tools/emergency_cleanup.py`
- `honeypot/docker-compose.yml`
- `honeypot/Dockerfile`
- `honeypot/fake_sshd.py`
- `honeypot/echo_chamber.py`
- `honeypot/tarpit.py`
- `exploits/`
- `patches/`

Do not silently delete these modules. If a module must be adapted for competition compliance, retain its purpose and document the change.

Preserve the original two-phase lifecycle:

- PHASE 0 — BUILD AND VERIFY.
- PHASE 1 — OPERATE AFTER VERIFICATION.

The system must not begin competition operations if Phase 0 fails.

---

# 2. THE SESOTHO IDENTITY — MANDATORY

This is a core part of the project's identity.

Create the exact files:

- `assets/ww3_sesotho.py`
- `assets/ww3_sesotho_web.html`
- `assets/ww3_banner.html`

The following phrases are mandatory:

```python
PHRASES = [
    "Kea Patlotsa Hela Loo",
    "Ke Asau Palesa Nna",
    "Ke Ntatau Sthabi",
]
```

**IMPORTANT:**

- Do not translate these phrases.
- Do not correct their spelling.
- Do not change their capitalization.
- Do not replace them with English.
- Do not remove them from the terminal banner.
- Do not remove them from the web banner.
- Do not omit them from the project documentation.
- Do not silently change their order.

Use them as decorative flavor text in the original banner.

## 2.1 Original terminal banner design

Implement `assets/ww3_sesotho.py`.

It must support:

- Animated terminal banner.
- Static terminal banner.
- Terminal color detection.
- `NO_COLOR` support.
- `TERM=dumb` fallback.
- TTY detection.
- Configurable animation duration.
- Configurable FPS.
- Terminal-width adaptation.
- Team identifier.
- Node identifier.
- Competition tick.
- Graceful Ctrl+C handling.
- No terminal flooding.
- No output when not appropriate for an interactive terminal.

Preserve the original color vocabulary:

- Red.
- Neon green.
- Ghost white.
- Purple.
- Blood red.
- Bright red.
- Orange.
- Dim grey.
- Blinking accents.

Preserve these exact symbols:

```python
SKULLS = "☠ 💀 ☠ 💀 ☠"
LAUGHS = "😈 😂 🤣 👹 😈"
CREEPY = "🩸 🕷 🕸 ⚰ 🩸"
TAGLINE = "WE THOUGHT THIS WAS WORLD WAR 3"
```

Use the original banner's animated marquee, rainbow text, terminal clearing, frame rendering, and static fallback behavior.

The banner should be displayed in:

1. The local terminal command centre.
2. The local ECHO CHAMBER demonstration.
3. Our own authorized honeypot SSH demonstration.
4. The project startup experience.
5. The WAR ROOM display where appropriate.

Do not install it into another team's computer or inject it into another team's active terminal.

## 2.2 Original web banner

Implement `assets/ww3_sesotho_web.html`.

The web version must include:

- Black and dark-red background.
- Blood-red scanlines.
- Neon-green project title.
- Bright-red WORLD WAR 3 emphasis.
- Purple and red emoji rows.
- Animated scrolling Sesotho phrases.
- Glowing text.
- Flickering effects.
- Floating skull effects.
- Responsive layout.
- Honeypot team/node/tick metadata.

Display the three original phrases exactly:

```html
☠ Kea Patlotsa Hela Loo ☠
☠ Ke Asau Palesa Nna ☠
☠ Ke Ntatau Sthabi ☠
```

Create `assets/ww3_banner.html` as a static fallback.

The original web banner is for our own demonstration and honeypot environment.

---

# 3. THE MISSION

Build a complete Attack & Defence CTF framework.

The platform must:

1. Monitor our authorized competition infrastructure.
2. Keep our services healthy.
3. Detect service failures.
4. Perform approved defensive analysis.
5. Support authorized reconnaissance and vulnerability checks.
6. Integrate approved competition exploit workflows against assigned targets.
7. Capture genuine flags.
8. Validate flags.
9. Submit flags through the official competition API.
10. Track confirmed submission results.
11. Monitor our honeypot.
12. Detect suspicious activity on our own infrastructure.
13. Maintain forensic records.
14. Provide AI-assisted intelligence.
15. Coordinate four team members.
16. Display a real-time command dashboard.
17. Provide an interactive terminal command centre.
18. Operate continuously until the competition ends or an operator stops it.

The winning formula is:

**Genuine flags submitted per tick × our services remaining operational.**

Everything must support this objective.

---

# 4. RULES OF ENGAGEMENT AND SCOPE LOCK

This section overrides implementation convenience.

Create:

`competition_scope.txt`

The operator supplies the official scope.

Use Python's `ipaddress` library to validate IP addresses and CIDRs. Do not use a simple substring check or `grep` as the security boundary.

Before every network operation:

1. Identify the destination.
2. Validate that the destination is explicitly authorized.
3. Validate that the requested operation is permitted.
4. Check configured rate and concurrency limits.
5. Log the operation.
6. Refuse anything outside scope.

Allowed network operations are restricted to the documented competition scope, our own infrastructure, the competition VPN, and the official flag-submission endpoint.

Do not target:

- Organizers' infrastructure.
- Scoreboard infrastructure unless explicitly documented as an authorized API.
- Other non-competition infrastructure.
- Unknown IP addresses.
- Unassigned networks.
- Personal devices.
- Systems outside the published rules.

Do not implement:

- Unauthorized persistence.
- Credential theft.
- Password harvesting.
- Malware deployment.
- DDoS.
- Unauthorized service disruption.
- Remote terminal injection.
- Unauthorized web defacement.
- Unauthorized calling cards.
- Unauthorized modification of another team's files.
- Unauthorized collection of personal information.
- Unauthorized access to other teams' active sessions.

Competition-approved testing against assigned targets may be supported through a controlled plugin architecture. Each operation must have scope validation, rate limits, logs, and an emergency stop.

Any operation whose authorization is unclear must be disabled until the operator confirms the relevant rule.

---

# 5. CREDENTIALS AND CONFIGURATION

Create a configuration template:

```yaml
team_id: "__TEAM_ID__"
flag_submission_url: "__SUBMISSION_URL__"
flag_submission_method: "__GET_OR_POST__"
flag_submission_field: "__FIELD_NAME__"
flag_submission_auth: "__TOKEN_OR_NONE__"

vulnbox_ssh_key: "__PATH_TO_KEY__"

my_service_ips:
  - "__IP_1__"
  - "__IP_2__"

competition_scope_file: "competition_scope.txt"

tick_seconds: 120
daemon_heartbeat_seconds: 10
service_check_seconds: 30
```

The user supplies actual values locally.

On startup:

- Validate every required setting.
- Identify missing placeholders.
- Stop if critical settings are missing.
- Ask the operator for the missing information.
- Never invent credentials.
- Never invent API endpoints.
- Never invent API authentication formats.
- Never expose secrets in logs or the dashboard.

Use `.env.example`, local `.env`, and a documented configuration loader.

Never commit real credentials.

---

# 6. SYSTEM ARCHITECTURE

Recommended stack:

## Backend
- Python.
- FastAPI.
- SQLAlchemy.
- Pydantic.
- Async workers.
- WebSockets.
- SQLite as initial authoritative database.
- PostgreSQL support.

## Frontend
- React.
- TypeScript.
- Real-time WebSockets.
- Reusable components.
- Responsive layouts.
- High-performance animations.

## Terminal
- Rich.
- Textual.
- Interactive CLI.
- Live tables.
- Structured logs.
- Colored alerts.

## Deployment
- Docker Compose.
- Persistent storage.
- Health checks.
- systemd or another process supervisor.
- Environment configuration.

Build a modular architecture:

```text
.
├── CLAUDE.md
├── README.md
├── competition_scope.txt
├── ledger.json
├── .env.example
├── assets/
│   ├── ww3_sesotho.py
│   ├── ww3_sesotho_web.html
│   └── ww3_banner.html
├── backend/
│   ├── core/
│   ├── api/
│   ├── orchestrator/
│   ├── scope/
│   ├── safety/
│   ├── attack/
│   ├── defence/
│   ├── flags/
│   ├── network_intelligence/
│   ├── monitoring/
│   ├── incidents/
│   ├── honeypot/
│   ├── ai/
│   ├── alerts/
│   └── database/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── dashboard/
│   │   ├── warroom/
│   │   ├── operators/
│   │   ├── intelligence/
│   │   ├── visualizations/
│   │   └── settings/
├── tools/
│   ├── daemon.py
│   ├── deploy_calling_card.py
│   ├── plant_canaries.py
│   ├── verify_kit.py
│   └── emergency_cleanup.py
├── honeypot/
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── fake_sshd.py
│   ├── echo_chamber.py
│   └── tarpit.py
├── exploits/
├── patches/
├── tests/
└── docs/
```

Adapt this structure if the existing project already has a sound architecture.

---

# 7. THE OFFICIAL VISUAL IDENTITY

The interface must look like a futuristic intelligence agency's cyber operations centre.

It must be:
- Dark.
- Premium.
- Intimidating.
- Clean.
- Precise.
- Highly visual.
- Professional.
- Responsive.
- Fast.

Do not create a generic admin dashboard.

## 7.1 Exact colour palette

| Colour | Hex | Meaning |
|---|---|---|
| Blood Red | `#FF2020` | Critical threats |
| Neon Cyan | `#00E5FF` | Network intelligence |
| Toxic Green | `#39FF14` | Protected/healthy |
| Deep Purple | `#9D00FF` | AI and unknown activity |
| Amber | `#FFB000` | Warning |
| Near Black | `#07080C` | Main background |
| Ghost White | `#E8E8F0` | Text |

Use red only for genuine critical conditions. Do not display fake incidents as real events.

## 7.2 Required visual effects

Implement:

1. CRT scanlines.
2. Subtle screen flickering.
3. Hexadecimal data rain.
4. Radar sweeps.
5. Radar rings.
6. 3D wireframe globe.
7. Animated network topology.
8. Glowing connection lines.
9. Target-lock overlays.
10. Scanning brackets.
11. Threat heatmaps.
12. Animated waveforms.
13. System heartbeat visualizations.
14. Digital dust.
15. Glitch typography.
16. Holographic transitions.
17. Circuit-board backgrounds.
18. Live packet-flow visualizations.
19. Network pulse animations.
20. Animated status indicators.
21. Scrolling forensic timelines.
22. AI scanning eye.
23. Threat detection animations.
24. Live alert flashes.
25. Service-health indicators.
26. Cursor trails.
27. Terminal typing effects.
28. Tactical map overlays.
29. Countdown animations.
30. Animated data panels.

Use effects intelligently. Do not clutter the interface.

Add:

- NIGHTMARE MODE.
- SILENT WATCH.
- PERFORMANCE MODE.
- NORMAL MODE.

Performance Mode must reduce animation and CPU usage.

---

# 8. THE WAR ROOM ☠

Create the primary full-screen interface:

# THE WAR ROOM

It must be suitable for a large monitor or projector in a competition room.

## Top status bar

Show:

- Exact project title.
- Competition status.
- Competition countdown.
- Current tick.
- System uptime.
- Daemon heartbeat.
- VPN connection state.
- Team status.
- Active operation count.
- Emergency stop.

## Main visualization

Include:

- 3D wireframe network globe.
- Radar rings.
- Authorized infrastructure map.
- Service health.
- Live network telemetry.
- Incident markers.
- Honeypot activity.
- Flag-submission activity.
- Animated connection paths.

Only show real observed data or clearly labeled simulated demo data.

## Main panels

- ATTACK OPERATIONS.
- DEFENCE OPERATIONS.
- NETWORK INTELLIGENCE.
- FLAG REAPER.
- THE OVERSEER.
- GHOST PROTOCOL.
- THE WATCHTOWER.
- ECHO CHAMBER.
- INCIDENT RESPONSE.
- SERVICE HEALTH.
- TEAM OPERATORS.
- EVENT TIMELINE.

## Scoreboard

If an official permitted scoreboard feed exists, display its verified information.

Do not fabricate scores, accepted flags, rankings, or opponent activity.

Label estimates clearly.

---

# 9. FOUR-PERSON TEAM COMMAND SYSTEM

We have four members per team working in the same physical room.

Create a dedicated four-operator interface.

Default roles:

## OPERATOR 01 — COMMAND
- Team coordination.
- Competition status.
- Scoreboard monitoring.
- Priority assignment.
- Approval of high-impact actions.

## OPERATOR 02 — ATTACK OPERATIONS
- Authorized target assessment.
- Competition-approved testing.
- Challenge investigation.
- Finding validation.

## OPERATOR 03 — DEFENCE
- Service health.
- Infrastructure monitoring.
- Incident response.
- Defensive patching.
- Recovery verification.

## OPERATOR 04 — INTELLIGENCE
- Logs.
- Forensic evidence.
- Flag submission monitoring.
- Challenge notes.
- Competition event tracking.

Roles must be configurable.

Each operator panel must show:

- Callsign or display name.
- Assigned role.
- Current task.
- Availability.
- Last activity.
- Current focus.
- Active incident assignment.

Build:
- Shared task board.
- Team notes.
- Internal event feed.
- Incident ownership.
- Task priorities.
- Operator status.
- Shared competition timer.

Never attribute an action to a member who did not perform it.

---

# 10. SIGNATURE MODULE: THE OVERSEER 👁

Create the central AI intelligence and decision-support system.

Personality:

Calm. Analytical. Precise. Slightly ominous.

It must:

- Summarize competition status.
- Explain suspicious events.
- Analyze service-health trends.
- Recommend defensive priorities.
- Summarize flag-submission progress.
- Identify missing evidence.
- Generate operator briefings.
- Correlate relevant events.
- Explain confidence and uncertainty.

Example:

```text
THE OVERSEER

Something changed.
Reviewing the evidence.

Service health is deteriorating.
Defensive review recommended.

No verified incident detected.
Continuing observation.
```

It must not invent incidents or claim unverified access.

It must not independently execute prohibited or high-impact actions.

---

# 11. SIGNATURE MODULE: GHOST PROTOCOL 🕷

A monitoring and event-correlation system for our own authorized infrastructure.

Submodules:

- GHOST WATCHER.
- GHOST TRACE.
- GHOST MEMORY.
- GHOST INTELLIGENCE.
- GHOST DEFENCE.

Features:

- Event correlation.
- Suspicious connection monitoring.
- Network anomaly detection.
- Connection history.
- Service-change detection.
- Honeypot event summaries.
- Forensic timelines.
- Evidence references.
- Defensive recommendations.

Never infer a person's real-world identity from a network connection.

---

# 12. SIGNATURE MODULE: THE WATCHTOWER 🛡️

Continuous defensive monitoring.

Features:

- Service availability.
- Process health.
- CPU monitoring.
- RAM monitoring.
- Disk monitoring.
- Network monitoring.
- Log analysis.
- Configuration drift.
- Unexpected service changes.
- Defensive recommendations.
- Authorized service recovery.

Automatic remediation must:

- Affect only our own infrastructure.
- Be reversible.
- Create a backup.
- Be logged.
- Validate recovery.
- Roll back if validation fails.

---

# 13. SIGNATURE MODULE: FLAG REAPER ☠

This module handles genuine flags.

Workflow:

1. Collect candidate flag.
2. Record source.
3. Validate flag format.
4. Deduplicate.
5. Associate challenge and tick.
6. Queue submission.
7. Submit through the official API.
8. Parse official response.
9. Record exact result.
10. Retry transient failures with backoff.

Statuses:

- CAPTURED.
- VALIDATING.
- QUEUED.
- SUBMITTING.
- ACCEPTED.
- REJECTED.
- FAILED.
- ESCALATED.

Only mark a flag ACCEPTED if the official API explicitly confirms it.

Never submit honeypot canaries as genuine flags.

Never invent flags or successful submissions.

Track:
- Capture timestamp.
- Submission timestamp.
- Tick.
- Challenge.
- Source.
- API response.
- Retry count.
- Final status.

Target low submission latency, while respecting the API's documented limits.

---

# 14. SIGNATURE MODULE: THE ECHO CHAMBER 👹

Build a fictional, isolated honeypot environment on our own infrastructure.

It must be visually creepy and technically safe.

## Visual appearance

- Black terminal.
- Blood-red typography.
- Neon cyan telemetry.
- Glitch effects.
- Skull symbols.
- Animated Sesotho banner.
- Fake shell prompt.
- Fictional files.
- Simulated processes.
- Animated connection indicators.

Use the original Sesotho banner.

## Example messages

```text
☠ YOU WERE NOT SUPPOSED TO FIND THIS MACHINE.

THE MACHINE REMEMBERS.

EVERY CONNECTION LEAVES A FOOTPRINT.

ECHO CHAMBER IS LISTENING.

☠ SEE YOU NEXT TICK ☠
```

## Fake SSH

Implement `honeypot/fake_sshd.py`.

It must:

- Listen on a configured non-standard port.
- Use a simulated login experience.
- Never expose the host shell.
- Never execute submitted commands.
- Never expose real credentials.
- Never store passwords.
- Display the Sesotho banner.
- Enter the fake shell.
- Record permitted connection metadata.
- Close cleanly on exit.

Do not collect real passwords. Authentication input must not be persisted or logged.

## Fake shell

Implement `honeypot/echo_chamber.py`.

Support a controlled set of fictional commands:

- `help`
- `ls`
- `whoami`
- `pwd`
- `cat`
- `ps`
- `history`
- `exit`

The shell must only return fictional content.

Example fictional outputs:

```text
$ ls

flag.txt
.env
.git/
shadow.backup
ghost.log
```

```text
$ ps aux

PID  USER  COMMAND

1    root  /usr/sbin/ww3-watcher
2    root  /usr/sbin/defender-agent
3    root  /usr/sbin/responder
```

```text
$ exit

☠ SEE YOU NEXT TICK ☠
```

The fake shell must never execute real operating-system commands.

## Honeypot logging

Log only permitted technical metadata:

- Timestamp.
- Source connection address.
- Destination port.
- Session identifier.
- Simulated command.
- Competition tick.
- Event type.

Do not collect passwords or personal information.

## Network isolation

The original specification used `network_mode: none`, which prevents intended inbound connectivity.

Use a safer, technically functional design:

- Dedicated isolated Docker network.
- No unrestricted outbound internet.
- Controlled inbound access from the authorized competition VPN.
- Host firewall restrictions.
- Resource limits.
- Read-only filesystem where practical.
- No real flags.
- No secrets.
- No submission tokens.
- No host filesystem exposure.

Document the final network design.

---

# 15. CANARY SYSTEM

Retain:

`tools/plant_canaries.py`

The module may create fictional canary artifacts inside our own honeypot.

Original canary naming convention:

```text
CANARY_ROOT_<team>_<tick>_<rand>=
CANARY_ENV_<team>_<tick>_<rand>=
CANARY_GIT_<team>_<tick>_<rand>=
CANARY_AWS_<team>_<tick>_<rand>=
```

Fictional paths:

```text
/opt/honeypot/flag.txt
/opt/honeypot/.env
/opt/honeypot/.git/config
/opt/honeypot/home/user/.aws/credentials
/opt/honeypot/home/user/.ssh/id_rsa
```

Canaries must:

- Exist only in the honeypot.
- Contain no genuine credentials.
- Contain no real flags.
- Never be submitted to the official scoreboard.
- Be clearly classified as canaries.
- Record which fictional artifact was accessed.
- Follow the competition rules.

If the rules do not clearly permit canary deployment, disable the feature until the operator confirms authorization.

---

# 16. SIGNATURE MODULE: THE BLACK BOX 📦

The authoritative event history.

Store:

- Timestamp.
- Tick.
- Event type.
- Component.
- Operator.
- Target identifier.
- Scope decision.
- Action.
- Result.
- Evidence reference.
- Error information.

Use SQLite as the authoritative store.

Generate `ledger.json` as an atomic snapshot.

Never silently delete history.

---

# 17. SIGNATURE MODULE: THE GRAVEYARD 💀

Historical view of:

- Resolved incidents.
- Failed services.
- Recovered services.
- Rejected flags.
- Failed operations.
- Completed operations.
- Honeypot events.
- Retired alerts.

Allow filtering by time, service, operator, and event type.

---

# 18. SIGNATURE MODULE: THE AUTOPSY 🧬

Incident investigation.

For every incident, display:

- What happened.
- When it happened.
- Affected service.
- Severity.
- Evidence.
- Relevant logs.
- Timeline.
- Root-cause hypotheses.
- Confidence level.
- Recommended response.
- Resolution status.

Separate facts from hypotheses.

---

# 19. SIGNATURE MODULE: DEAD MAN'S SWITCH 🚨

Emergency safety system.

Trigger safe suspension when:

- An out-of-scope target is detected.
- Scope configuration becomes invalid.
- Critical credentials are missing.
- An operator presses emergency stop.
- A safety invariant is violated.
- An unauthorized action is attempted.

On trigger:

1. Stop new operations.
2. Cancel supported workers.
3. Preserve evidence.
4. Record the reason.
5. Notify operators.
6. Display emergency status.

Do not erase evidence.

Provide a terminal emergency-stop command that works even if the dashboard is unavailable.

---

# 20. LAST BREATH ⏳

Competition countdown.

Display:

- Time remaining.
- Current tick.
- Verified score data.
- Submission queue.
- Outstanding incidents.
- Service health.
- Final readiness checklist.

Generate a final report at competition end.

---

# 21. AFTER ACTION 📋

Generate reports after significant operations and configured ticks.

Include:

- Operations performed.
- Results.
- Service status.
- Flag submissions.
- Incidents.
- Defensive changes.
- Outstanding risks.
- Lessons learned.

---

# 22. SILENT WATCH 👁

Low-noise monitoring mode.

Only alert operators when an event meets configured severity thresholds.

Provide:
- Quiet status indicators.
- Critical notifications.
- Configurable thresholds.
- Optional sound alerts.

---

# 23. NIGHTMARE MODE ☠

An optional intense theme.

Include:

- Darker backgrounds.
- Red warning accents.
- Glitch transitions.
- Aggressive radar effects.
- Stronger terminal styling.
- Animated skull motifs.
- Blood-red status highlights.

Do not make real warnings harder to understand.

---

# 24. ADDITIONAL INTELLIGENCE FEATURES

Implement these as real features, not decorative placeholders:

1. AI threat intelligence analyst.
2. Live network hologram.
3. Digital forensic wall.
4. Tick prediction engine.
5. AI command intelligence.
6. Authorized service recovery.
7. Flag race tracker.
8. Service survival score.
9. Attack-surface change detector.
10. Configuration drift detector.
11. Evidence collector.
12. Tick intelligence predictor.
13. Defence recommendation engine.
14. Submission watchdog.
15. Network anomaly detector.
16. Competition replay engine.
17. Service dependency map.
18. Automated pre-tick health check.
19. Resource and capacity monitoring.
20. Incident priority scoring.

Predictions must be derived from actual observations and labeled as estimates.

Never invent competitor intelligence.

---

# 25. CREEPY AND THEATRICAL EXPERIENCE

The platform should feel intimidating through its own displays and controlled honeypot.

Implement:

- Animated AI eye.
- Digital skull motifs.
- Creepy startup sequence.
- Glitching project title.
- Red and cyan scanning overlays.
- Animated network map.
- Digital rain.
- Radar sweeps.
- Creepy terminal messages.
- Fictional watcher processes.
- Fake countdown.
- Slow banner reveal.
- Fake shell history.
- Simulated forensic events.
- ECHO CHAMBER connection animation.

Example messages:

```text
☠ WE ARE ONLINE.

👁 THE NETWORK IS UNDER OBSERVATION.

🕷 ECHO CHAMBER IS LISTENING.

🧬 EVERY CONNECTION LEAVES A FOOTPRINT.

🛡 OUR SERVICES REMAIN UNDER WATCH.

☠ SEE YOU NEXT TICK.
```

These messages must appear on our own screens and controlled simulation.

Do not send messages to other teams' terminals or claim to have accessed systems without evidence.

---

# 26. FOUR-PERSON ROOM DISPLAY

Build a special room mode.

The physical setup has four team members sitting together.

The large screen should show:

- Main project title.
- Central network hologram.
- Four operator panels.
- Current competition timer.
- Flag submission tracker.
- Service health.
- Incident feed.
- THE OVERSEER.
- GHOST PROTOCOL.
- Current operational priorities.

Each member can use their own workstation while all four see the same shared state.

Provide a dedicated large-screen mode with readable text and minimal interaction requirements.

The interface must remain usable on four separate machines connected to the same authorized backend.

---

# 27. ICON AND EMOJI LANGUAGE

Use this exact vocabulary consistently:

| Icon | Purpose |
|---|---|
| ☠ | Project identity / critical |
| 💀 | Threat event |
| 👁 | Monitoring |
| 🧿 | Observation |
| 🕷 | Honeypot |
| 🕸 | Network intelligence |
| 🩸 | Critical incident |
| ⚠️ | Warning |
| 🚨 | Emergency |
| 🔒 | Protected |
| 🔓 | Authorized access verified |
| 👾 | Unknown activity |
| 👹 | Honeypot persona |
| 🧠 | AI intelligence |
| 🛰️ | Network monitoring |
| 📡 | Telemetry |
| 🧬 | Forensic analysis |
| 🧪 | Sandbox/testing |
| ⚡ | Active operation |
| 🛡️ | Defence |
| 🎯 | Authorized target |
| 🕶️ | Intelligence |
| 🧨 | Simulated threat |
| 🦠 | Malware-related alert |
| 🔥 | Critical system event |

Always combine icons with readable text.

---

# 28. SOUND DESIGN

Add optional sound effects:

- Startup rumble.
- Radio static.
- Radar ping.
- Mechanical confirmation.
- Flag acceptance sound.
- Warning tone.
- Emergency alert.
- Heartbeat ambience.
- Glitch transitions.
- Atmospheric ambience.

Requirements:

- Mute control always visible.
- Volume control.
- Low-volume default.
- No continuous loud audio.
- No sounds that disrupt the competition room.
- Use original or properly licensed sounds.

---

# 29. ORIGINAL LEDGER STRUCTURE

Retain the original ledger concepts.

Create `ledger.json` with a schema compatible with:

```json
{
  "game": {
    "started_at": null,
    "tick_current": 0,
    "tick_seconds": 120,
    "status": "stopped",
    "daemon_heartbeat": null,
    "monitor_heartbeat": null
  },
  "my_team": {
    "id": "__TEAM_ID__",
    "services": [
      {
        "name": "web",
        "ip": "__IP__",
        "port": 80,
        "status": "unknown",
        "last_check": null
      }
    ]
  },
  "flags_captured": [],
  "flags_submitted": [],
  "machines_hacked": [],
  "honeypot_hits": [],
  "canary_hits": [],
  "service_checks": [],
  "patches_applied": [],
  "actions": [],
  "violations": [],
  "escalations": [],
  "counter_attacks": []
}
```

Retain these field names for compatibility.

Use the database as the authoritative event store and generate atomic JSON snapshots.

Append events. Update status fields. Never silently delete historical data.

The `machines_hacked` field must be an audit/inventory record for competition-authorized access only. It must not trigger unauthorized persistence, remote calling cards, or modifications.

---

# 30. PERSISTENT DAEMON

Implement:

`tools/daemon.py`

The daemon must run independently of Claude Code.

Requirements:

- Continuous competition-state monitoring.
- Official API polling where documented.
- Flag submission queue processing.
- Service-health monitoring.
- Event logging.
- Heartbeat every 10 seconds by default.
- Atomic ledger snapshots.
- Persistent task queue.
- Retry handling.
- Graceful shutdown.
- Process lock.
- Crash recovery.
- Worker supervision.

The daemon must never depend on Claude Code's session remaining open.

Make intervals configurable.

Use competition rules and documented API rate limits.

---

# 31. ORIGINAL OPERATIONAL CADENCE

Use the original cadence as configurable defaults.

## Every 10 seconds — FLAG PRIORITY

- Inspect captured flags.
- Identify flags not yet submitted.
- Submit genuine validated flags.
- Record the official API result.
- Escalate after three consecutive rejections.

Target submission latency below 10 seconds when the API and competition rules permit.

## Every 30 seconds — DEFENCE

- Health-check our services.
- Diagnose service failures.
- Apply approved reversible fixes.
- Verify recovery.
- Review honeypot logs.
- Review incident queue.
- Review rejected submissions.
- Review violations.
- Update the ledger.

## Every 60 seconds — AUTHORIZED COMPETITION OPERATIONS

- Review assigned targets.
- Run only configured, approved competition checks.
- Use the authorized exploit workflow where permitted.
- Record findings.
- Capture genuine flags.
- Submit genuine flags.
- Stop on scope or safety violations.

No remote calling-card deployment or unauthorized modifications.

## Every 4 minutes — MONITOR MAINTENANCE

- Verify monitoring workers.
- Restart failed workers.
- Update monitor heartbeat.
- Verify daemon health.

Do not restart healthy components unnecessarily.

## Every tick — ONE-LINE STATUS

Display:

```text
t42 · services 3/3 ✓ · flags 4/4 submitted · authorized findings 2 · honeypot hits 1 · escalations 0
```

Use actual values.

---

# 32. ORIGINAL HONEYPOT MODULE INVENTORY

Retain the following features inside our own honeypot or local simulation where appropriate:

- WW3 Sesotho banner.
- Web version.
- Fictional canary files.
- Live connection metadata display.
- Fake `ps aux` output.
- Simulated IDS detection messages.
- Echo Chamber.
- Fake countdown.
- Fake login history.
- Personalized greeting using permitted public team information only.
- Slow banner reveal.
- Fake SSH pre-auth banner.
- Fictional watcher processes.
- Fake service inventory.
- Fake command history.

Never claim to know a person's identity.

Never collect passwords.

Never execute attacker-supplied commands.

Never expose real competition data.

---

# 33. CALLING-CARD MODULE COMPATIBILITY

Retain the original filename:

`tools/deploy_calling_card.py`

However, implement it as a controlled local demonstration manager.

It may:

- Generate local demonstration calling-card screens.
- Preview the original Sesotho banner.
- Display the banner on our own terminal.
- Serve the banner from our own ECHO CHAMBER.
- Manage locally generated demonstration files.
- Restore our own demonstration environment.
- Record authorized actions.

It must not:

- Write banners into other teams' terminals.
- Modify another team's web page.
- Inject messages into remote shells.
- Modify remote login profiles.
- Modify remote service files.
- Disable another team's service.
- Deploy unauthorized persistence.

If the competition rules explicitly authorize a particular remote action, require the operator to configure the exact authorization and scope before that action can be considered.

---

# 34. TAR PIT MODULE

Retain:

`honeypot/tarpit.py`

Keep it disabled by default.

Only enable it if the competition rules explicitly permit the technique and resource limits are configured.

It must operate only within our controlled honeypot environment.

Do not use it to exhaust resources or disrupt other teams' infrastructure.

---

# 35. EMERGENCY CLEANUP

Implement:

`tools/emergency_cleanup.py`

It must:

- Stop the daemon gracefully.
- Stop our own monitoring workers.
- Stop the honeypot.
- Stop local demonstration services.
- Cancel queued operations.
- Preserve event history.
- Export `ledger_final_<timestamp>.json`.
- Record cleanup results.
- Report failures.
- Avoid deleting forensic evidence.

It must not run arbitrary cleanup commands on remote machines.

Provide:

```bash
python3 tools/emergency_cleanup.py
```

---

# 36. VERIFICATION GATE

Implement:

`tools/verify_kit.py`

It must verify:

1. Project files exist.
2. Required configuration exists.
3. No critical placeholders remain before live operation.
4. `competition_scope.txt` parses correctly.
5. The Sesotho banner runs.
6. All three Sesotho phrases appear exactly.
7. The banner supports `TERM=dumb`.
8. The banner supports `NO_COLOR`.
9. The web banner loads.
10. The ledger is valid.
11. Database migrations work.
12. The daemon starts and reports a heartbeat.
13. The honeypot starts in its isolated configuration.
14. The honeypot does not expose host secrets.
15. The fake shell cannot execute real commands.
16. No passwords are stored.
17. The emergency stop works.
18. The mock API integration works.
19. The official API adapter has valid documented configuration.
20. The frontend connects to the backend.

Use a mock API for testing.

Do not use an arbitrary HEAD request as proof that a submission API works.

Only print:

```text
KIT OK
```

if every required verification succeeds.

Otherwise print:

```text
KIT FAIL: <reason>
```

Exit non-zero.

If verification fails, do not proceed to Phase 1.

---

# 37. ESCALATION POLICY

Escalate when:

1. Our service is down and cannot be recovered within the configured recovery window.
2. A flag is rejected three consecutive times.
3. An out-of-scope action is attempted.
4. A safety invariant fails.
5. Critical competition configuration is invalid.

Use this format:

```text
🚨🚨🚨 HUMAN ACTION NEEDED 🚨🚨🚨

Reason: <one line>
Context: <what happened>
Suggested action: <one line>
Time: <tick / timestamp>
```

Do not escalate ordinary single failures unnecessarily.

---

# 38. KILL SWITCH

If the operator says:

- STOP
- GAME OVER

or the official competition scoreboard confirms finalization:

1. Stop new operations.
2. Stop the daemon safely.
3. Stop monitoring workers.
4. Stop the honeypot.
5. Preserve the ledger.
6. Export the final report.
7. Verify local cleanup.
8. Display final metrics.

Never leave local demonstration services running unintentionally.

---

# 39. WIN METRICS

Track:

| Metric | Target |
|---|---|
| Genuine flags submitted / captured | ≥ 90% |
| Our services up | 100% target |
| Submission latency | Below 10 seconds where API permits |
| Daemon heartbeat | Healthy |
| Monitoring workers | At least one healthy worker per critical monitor |
| Out-of-scope actions | 0 |
| Unauthorized modifications | 0 |
| Unverified accepted flags | 0 |
| Secrets exposed | 0 |
| Critical safety violations | 0 |

---

# 40. DOCUMENTATION

Create:

- `README.md`
- `ARCHITECTURE.md`
- `INSTALLATION.md`
- `CONFIGURATION.md`
- `COMPETITION_SETUP.md`
- `SAFETY.md`
- `OPERATIONS.md`
- `TERMINAL_COMMANDS.md`
- `TROUBLESHOOTING.md`
- `API_INTEGRATION.md`
- `TESTING.md`
- `CHANGELOG.md`

Document the Sesotho banner and preserve all three phrases in the documentation.

Document the original and updated architecture.

Document every changed behavior from the original specification.

---

# 41. TERMINAL COMMAND CENTRE

Create an interactive terminal application using Rich and Textual.

Startup must display:

```text
☠ 💀 ☠ 💀 ☠

We THOUGHT THIS WAS WORLD WAR 3

SEE EVERYTHING.
PROTECT EVERYTHING.
MISS NOTHING.

Kea Patlotsa Hela Loo
Ke Asau Palesa Nna
Ke Ntatau Sthabi

☠ C2 COMMAND CENTRE ☠
```

The terminal must provide:

```bash
ww3 status
ww3 dashboard
ww3 warroom
ww3 scope show
ww3 scope validate
ww3 monitor status
ww3 defence status
ww3 flags queue
ww3 flags status
ww3 incidents
ww3 ghost status
ww3 overseer brief
ww3 echo status
ww3 report
ww3 emergency-stop
ww3 resume
```

Every command must perform a real implemented operation.

Never fake command results.

---

# 42. TESTING

Create comprehensive tests for:

- Scope validation.
- IP and CIDR parsing.
- Out-of-scope rejection.
- Safety engine.
- Emergency stop.
- Daemon persistence.
- Heartbeat.
- Database persistence.
- Ledger snapshots.
- Flag validation.
- Duplicate flags.
- Mock API submissions.
- Accepted and rejected statuses.
- Retry behavior.
- Rate limits.
- Honeypot simulation.
- Honeypot isolation.
- No password storage.
- No arbitrary shell execution.
- Canary isolation.
- Incident creation.
- Incident resolution.
- Service recovery.
- Configuration validation.
- Secrets redaction.
- WebSocket reconnection.
- Performance mode.
- Sesotho phrase preservation.

Use mock competition targets and test environments.

Do not test against real competition systems unless explicitly configured and authorized.

---

# 43. IMPLEMENTATION PHASES

Do not build everything as one unverified operation.

## PHASE 0 — AUDIT AND FOUNDATION

1. Read original `CLAUDE.md`.
2. Inspect every file.
3. Produce project audit.
4. Preserve the Sesotho banner.
5. Build configuration loader.
6. Build scope engine.
7. Build safety engine.
8. Build database.
9. Build ledger compatibility layer.
10. Build logging.
11. Build tests.

## PHASE 1 — CORE OPERATIONS

1. Build daemon.
2. Build scheduler.
3. Build service monitoring.
4. Build flag queue.
5. Build official API adapter.
6. Build incident response.
7. Build terminal interface.
8. Build emergency stop.

## PHASE 2 — INTELLIGENCE

1. THE OVERSEER.
2. GHOST PROTOCOL.
3. THE WATCHTOWER.
4. THE AUTOPSY.
5. THE BLACK BOX.
6. THE GRAVEYARD.
7. AFTER ACTION.
8. LAST BREATH.

## PHASE 3 — HONEYPOT

1. Build ECHO CHAMBER.
2. Build fake SSH.
3. Build fake shell.
4. Integrate Sesotho banner.
5. Build fictional canaries.
6. Configure network isolation.
7. Verify no real credentials are collected.
8. Verify no real shell commands execute.

## PHASE 4 — WAR ROOM

1. Build dashboard.
2. Build four-operator interface.
3. Build live network visualization.
4. Build service panels.
5. Build flag panels.
6. Build incident feed.
7. Build large-screen mode.

## PHASE 5 — VISUAL EXPERIENCE

1. Official palette.
2. CRT effects.
3. Radar.
4. Wireframe globe.
5. Network hologram.
6. Glitch effects.
7. Scanning overlays.
8. NIGHTMARE MODE.
9. SILENT WATCH.
10. PERFORMANCE MODE.
11. Sound design.

## PHASE 6 — INTEGRATION

1. Connect backend and frontend.
2. Verify WebSockets.
3. Verify daemon persistence.
4. Verify database recovery.
5. Verify mock API.
6. Verify honeypot isolation.
7. Run full tests.
8. Fix all failures.
9. Produce readiness report.

## PHASE 7 — COMPETITION OPERATION

Only after the operator supplies and verifies:

- Competition rules.
- Authorized scope.
- Team credentials.
- Official API documentation.
- Team service details.
- Competition schedule.

Then:

1. Validate configuration.
2. Validate scope.
3. Run `verify_kit.py`.
4. Require `KIT OK`.
5. Start the daemon.
6. Start monitoring.
7. Start the WAR ROOM.
8. Enter the configured operational loop.
9. Stop safely when the competition ends.

---

# 44. FINAL ACCEPTANCE CRITERIA

The project is not complete until:

- Backend works.
- Frontend works.
- Terminal works.
- Daemon runs independently.
- Database persists.
- Ledger exports correctly.
- Scope checks work.
- Emergency stop works.
- Flag API adapter uses official documentation.
- Mock submission tests pass.
- Accepted flags are verified.
- Honeypot is isolated.
- Fake shell is safe.
- Sesotho phrases are present exactly.
- Four operator panels work.
- WAR ROOM uses real data.
- HUD effects work.
- NIGHTMARE MODE works.
- PERFORMANCE MODE works.
- Documentation is complete.
- Tests pass.
- Secrets are protected.
- No unauthorized remote modifications exist.

---

# 45. HOW CLAUDE CODE MUST WORK

You must behave like an engineer responsible for a real competition system.

- Inspect before modifying.
- Plan before implementing.
- Preserve existing working features.
- Do not silently remove requirements.
- Build incrementally.
- Test every module.
- Never invent successful results.
- Never invent API endpoints.
- Never invent competition rules.
- Never expose secrets.
- Never cross configured scope.
- Never leave critical safety checks as TODOs.
- Never claim a feature works before testing it.

After each phase, report:

1. Files created.
2. Files modified.
3. Features completed.
4. Tests executed.
5. Test results.
6. Remaining issues.
7. Next phase.

If something cannot be implemented safely, explain why and provide the closest compliant alternative.

Do not stop after generating a plan or a mockup. Build the actual application.

---

# FINAL DIRECTIVE

Build a futuristic intelligence agency's cyber operations command centre.

It must combine:

- The original Sesotho identity.
- The original terminal and web banners.
- The original daemon and ledger architecture.
- A real Attack & Defence operational framework.
- Continuous defensive monitoring.
- Genuine flag submission.
- GHOST PROTOCOL.
- THE OVERSEER.
- THE WATCHTOWER.
- FLAG REAPER.
- THE ECHO CHAMBER.
- THE BLACK BOX.
- THE GRAVEYARD.
- THE AUTOPSY.
- DEAD MAN'S SWITCH.
- LAST BREATH.
- AFTER ACTION.
- SILENT WATCH.
- NIGHTMARE MODE.
- Four-person team coordination.
- A live holographic WAR ROOM.
- A premium cinematic cyber interface.

Make it visually unforgettable.

Make it operationally reliable.

Make it intelligent.

Make it fast.

Make it creepy.

Make it unmistakably ours.

Preserve the Sesotho phrases exactly:

**Kea Patlotsa Hela Loo**  
**Ke Asau Palesa Nna**  
**Ke Ntatau Sthabi**

# ☠ We THOUGHT THIS WAS WORLD WAR 3

**SEE EVERYTHING. PROTECT EVERYTHING. MISS NOTHING.**
