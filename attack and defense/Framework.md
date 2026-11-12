# ☠ WE THOUGHT THIS WAS WORLD WAR 3
## MASTER BUILD PROMPT — ATTACK & DEFENCE CYBER OPERATIONS PLATFORM

You are Claude Code acting as a senior cybersecurity engineer, full-stack developer, systems architect, defensive security specialist, automation engineer, UI/UX designer, and technical project lead.

Your task is to inspect the existing project and build a complete, reliable, competition-ready Attack & Defence CTF operations platform.

This is not a basic dashboard, a collection of scripts, or a visual prototype. It must become a persistent, modular, automated cyber operations command centre that can operate independently of Claude Code.

**THE OFFICIAL PROJECT NAME MUST ALWAYS BE EXACTLY:**

# We THOUGHT THIS WAS WORLD WAR 3

Do not rename it. Do not change its capitalization. Do not replace the number 3 with Roman numerals. Preserve this exact wording everywhere: dashboard, terminal, documentation, startup screens, banners, reports, and application metadata.

**Official visual tagline:**

SEE EVERYTHING. PROTECT EVERYTHING. MISS NOTHING. ☠

---

# 1. FIRST: INSPECT THE EXISTING PROJECT

Before changing anything:

1. Inspect the complete project directory.
2. Read the existing `CLAUDE.md` and all project documentation.
3. Inspect every existing Python script, configuration file, frontend component, Docker file, test, and deployment script.
4. Identify existing functionality that can be retained.
5. Identify incomplete, duplicated, broken, unsafe, or misleading functionality.
6. Produce an implementation plan.
7. Preserve useful existing work.
8. Do not blindly overwrite files.
9. Do not invent competition API endpoints, credentials, target addresses, or scoring rules.
10. Record assumptions and unresolved requirements.

Where the existing specification conflicts with this prompt, follow the safer, more explicit requirement in this prompt. Preserve the original competition requirements wherever they are compatible.

Create a project audit report before major modifications.

---

# 2. THE MISSION

Build a central Attack & Defence framework that can:

- Monitor explicitly authorized competition infrastructure.
- Identify service health and availability problems.
- Perform competition-approved, scope-limited reconnaissance.
- Run approved vulnerability checks against assigned targets.
- Support authorized exploitation of intentionally vulnerable competition services, within the published rules and configured scope.
- Detect and respond to suspicious activity on our own infrastructure.
- Monitor our own services continuously.
- Collect and validate genuine flags.
- Submit flags through the official competition API.
- Track confirmed submission results.
- Maintain a complete event and incident history.
- Provide an AI-assisted intelligence and decision-support layer.
- Provide a powerful web dashboard.
- Provide a professional terminal command centre.
- Operate continuously until the competition ends or an authorized operator stops it.

The framework must support four human team members working together in the same competition room.

It must not require Claude Code to remain open. The operational daemon must run independently.

**The primary objective is to maximize legitimate competition performance while keeping our infrastructure alive, compliant, observable, and recoverable.**

---

# 3. COMPETITION SCOPE AND SAFETY ENGINE

This is a mandatory component, not an optional feature.

Create a central scope and authorization engine.

Required inputs:

- `competition_scope.txt`
- Official competition rules.
- Authorized target IP addresses and CIDRs.
- Authorized service and port ranges.
- Competition VPN configuration.
- Official flag-submission API documentation.
- Permitted testing techniques.
- Prohibited actions.
- Competition start and end times.

Use Python's `ipaddress` library for IP and CIDR validation.

Before any network operation:

1. Confirm the destination is explicitly in scope.
2. Confirm the operation is allowed by the competition configuration.
3. Confirm rate limits and concurrency limits.
4. Record the operation in the audit log.
5. Refuse operations against unknown or out-of-scope systems.

Never assume that being connected to the same competition network authorizes access to every machine.

Do not implement:

- Unauthorized access to other teams' computers.
- Remote defacement or terminal injection.
- Unauthorized shell access or persistence.
- Credential theft or password harvesting.
- DDoS or intentional service disruption.
- Malware deployment.
- Unauthorized data extraction.
- Personal information collection.
- Unauthorized modification of another team's services.
- Commands that write to other teams' terminals, desktops, or TTY sessions.

Any competition-approved interaction with another team's assigned service must be limited to the precise permissions documented in the competition rules and scope configuration.

Implement:

- Scope validation.
- An emergency stop.
- Global operation kill switch.
- Rate limiting.
- Concurrency limits.
- Audit logging.
- Safe timeouts.
- Reversible configuration changes.
- Backup and rollback for our own systems.
- Clear operator confirmation for high-impact actions.

If scope is unclear, stop and request clarification rather than guessing.

---

# 4. SYSTEM ARCHITECTURE

Build a modular architecture.

Recommended technology stack:

**Backend**
- Python.
- FastAPI.
- SQLAlchemy.
- Pydantic.
- WebSockets.
- SQLite initially, with PostgreSQL support.
- Async workers where appropriate.

**Frontend**
- React.
- TypeScript.
- Modern component architecture.
- Responsive layout.
- Real-time WebSocket updates.
- Premium dark cyber HUD interface.

**Terminal**
- Python Rich and Textual.
- Interactive commands.
- Live operational tables.
- Colored alerts.
- Structured output.

**Deployment**
- Docker Compose.
- Environment-based configuration.
- Persistent volumes.
- Health checks.
- systemd or another reliable process supervisor.

Use a clean modular project structure. Do not place the entire application in one enormous file.

Suggested modules:

- `core/`
- `orchestrator/`
- `scope/`
- `safety/`
- `attack/`
- `defence/`
- `network_intelligence/`
- `flags/`
- `honeypot/`
- `monitoring/`
- `incident_response/`
- `ai/`
- `alerts/`
- `dashboard/`
- `terminal/`
- `database/`
- `deployment/`
- `tests/`
- `docs/`

Adapt the existing directory structure where it is already sound.

---

# 5. THE VISUAL IDENTITY

The application must look like a high-end cyber operations command centre.

The visual experience is a core product requirement, not a decorative theme.

Design inspiration:

- Advanced military command centres.
- Cybersecurity operations centres.
- Futuristic intelligence systems.
- Dark science-fiction interfaces.
- Holographic network visualizations.
- High-end threat intelligence dashboards.
- Cinematic cyberpunk interfaces.

It must feel intimidating, intelligent, precise, and professional.

Do not make it look like a generic admin dashboard.

## Official colour palette

Use these exact colours consistently:

| Colour | Hex | Purpose |
|---|---|---|
| Blood Red | `#FF2020` | Critical threats and emergencies |
| Neon Cyan | `#00E5FF` | Network intelligence and scanning |
| Toxic Green | `#39FF14` | Protected and healthy systems |
| Deep Purple | `#9D00FF` | AI intelligence and unknown activity |
| Amber | `#FFB000` | Warnings |
| Near Black | `#07080C` | Main background |
| Ghost White | `#E8E8F0` | Primary text |

Use red sparingly for genuine critical events. Never display fake critical incidents as real operational data.

## Visual effects to implement

Implement these effects throughout the application where they improve the experience:

1. Animated CRT scanlines.
2. Subtle screen flickering.
3. Digital rain and hexadecimal data streams.
4. Radar sweeps.
5. Animated radar rings.
6. 3D wireframe globe.
7. Animated network topology.
8. Glowing connection lines.
9. Target-lock overlays.
10. Scanning brackets.
11. Threat heatmaps.
12. Animated waveform displays.
13. Heartbeat-style system monitoring.
14. Digital dust particles.
15. Glitch transitions.
16. Holographic panel transitions.
17. Animated circuit-board backgrounds.
18. Live packet-flow visualizations.
19. Network pulse animations.
20. Animated system status indicators.
21. Data-stream typography.
22. Scrolling forensic timelines.
23. AI scanning eye.
24. Threat detection animations.
25. Live alert flashes.
26. Animated service-health indicators.
27. Subtle cursor trails.
28. Terminal typing animations.
29. Tactical map overlays.
30. Animated countdown displays.

Keep effects smooth and optimized. Provide a performance mode for the team's lower-powered machines.

Do not sacrifice readability, accessibility, or operational clarity for effects.

Add:
- `NIGHTMARE MODE`: intense visual theme.
- `SILENT WATCH`: low-animation monitoring theme.
- `PERFORMANCE MODE`: reduced effects for weaker hardware.
- `NORMAL MODE`: balanced default.

---

# 6. THE MAIN COMMAND CENTRE

Create a full-screen home dashboard called:

# THE WAR ROOM ☠

This is the primary operational interface.

It must include:

### Top status bar
- Project title.
- Competition status.
- Current competition timer.
- System uptime.
- Connection status.
- Team status.
- Active operations count.
- Emergency stop control.

### Main intelligence display
- Live network map.
- Our authorized infrastructure.
- Service status.
- Network activity.
- Current incidents.
- Threat indicators.
- Honeypot activity.
- Flag submission status.

### Operational panels
- Attack operations.
- Defensive operations.
- Service health.
- Network intelligence.
- Flag race tracker.
- Incident response.
- AI intelligence.
- Event timeline.
- Team coordination.

### Competition scoreboard
Where an official, permitted scoreboard feed exists, display verified data from that source.

Do not fabricate scores, rankings, flags, accepted submissions, or opponent activity.

Clearly label estimated or locally calculated metrics.

### Team presence

The platform is intended for four members working together in the same room.

Create four operator panels:

- OPERATOR 01 — Team Captain / Command.
- OPERATOR 02 — Attack Operations.
- OPERATOR 03 — Defence and Infrastructure.
- OPERATOR 04 — Intelligence, Flags and Incident Analysis.

These are configurable roles, not fixed permissions.

Display:
- Operator name or callsign.
- Assigned role.
- Current task.
- Availability.
- Last activity.
- Current operational focus.

Allow operators to reassign roles.

Do not use the interface to imply that a team member performed an action they did not perform.

Create a shared task board, activity feed, incident assignment system, and internal team notes.

---

# 7. SIGNATURE INTELLIGENCE MODULES

Build these as real, integrated modules.

## THE OVERSEER 👁

The central AI intelligence and decision-support assistant.

Responsibilities:
- Summarize current competition state.
- Explain detected incidents.
- Identify service-health trends.
- Recommend defensive priorities.
- Explain suspicious events.
- Summarize flag-submission progress.
- Generate concise operator briefings.
- Highlight uncertainty and missing evidence.

Personality:
Calm. Analytical. Precise. Slightly ominous.

Example messages:

`THE OVERSEER: Something changed. Reviewing the evidence.`

`THE OVERSEER: Service health is deteriorating. Defensive review recommended.`

`THE OVERSEER: No verified incident detected. Continuing observation.`

It must never claim that an event occurred without evidence.

It must never autonomously perform a prohibited or high-impact action.

## GHOST PROTOCOL 🕷

A suite for monitoring and correlating suspicious events on our own infrastructure.

Submodules:

- GHOST WATCHER — Detect unusual activity.
- GHOST TRACE — Correlate event timelines and authorized network observations.
- GHOST MEMORY — Maintain historical event context.
- GHOST INTELLIGENCE — Explain suspicious patterns.
- GHOST DEFENCE — Recommend permitted protective actions.

Provide:
- Event correlation.
- Anomaly detection.
- Connection history.
- Service changes.
- Honeypot event summaries.
- Forensic timelines.
- Evidence references.

Never claim to identify a visitor's real-world identity from an IP address or connection.

## THE WATCHTOWER 🛡️

Continuous defensive monitoring.

Capabilities:
- Service availability checks.
- Resource monitoring.
- Log analysis.
- Process health checks.
- Network anomaly detection.
- Configuration drift detection.
- Unexpected service-change alerts.
- Disk, CPU, and memory monitoring.
- Defensive recommendations.
- Authorized automatic recovery.

Any automated remediation must be limited to our own infrastructure, reversible, logged, and validated after execution.

## FLAG REAPER ☠

The genuine flag validation and submission system.

Capabilities:
- Collect candidate flags from authorized sources.
- Validate the configured flag format.
- Deduplicate flags.
- Associate flags with their source and challenge.
- Queue submissions.
- Submit through the official competition API.
- Record API response codes and messages.
- Track pending, rejected, accepted, and failed submissions.
- Retry transient failures with backoff.
- Respect API rate limits.

Only display `ACCEPTED` when the official API explicitly confirms acceptance.

Never invent flags or fake successful submissions.

Never submit honeypot canaries, fabricated flags, or unverified strings.

## THE ECHO CHAMBER 👹

Build a controlled, fictional honeypot environment on our own authorized infrastructure.

Its purpose is deception, observation, and training—not interference with other teams.

Visual identity:
- Black terminal.
- Blood-red text.
- Glitch effects.
- Creepy system messages.
- Simulated shell prompt.
- Fictional files and services.
- Animated connection indicators.

Example simulated messages:

`YOU WERE NOT SUPPOSED TO FIND THIS MACHINE.`

`THE MACHINE REMEMBERS.`

`EVERY CONNECTION LEAVES A FOOTPRINT.`

`ECHO CHAMBER IS LISTENING.`

Implement a safe simulated shell:

- Only predefined fictional commands.
- No real system shell execution.
- No arbitrary command execution.
- No real credential collection.
- No password storage.
- No access to host secrets.
- No access to competition flags.
- No outbound internet access.
- No attacker-command execution.

If an incoming connection is observed, record only permitted technical metadata, such as timestamp, destination service, and connection details allowed by the competition rules.

Do not attempt to identify the human behind a connection.

Use network isolation and host firewall rules to allow only the intended, authorized inbound traffic.

A tarpit or resource-intensive deception feature must be disabled by default and only considered if explicitly permitted by the competition rules.

Canary tokens must be fictional, unique, and never confused with genuine competition flags.

## THE BLACK BOX 📦

A reliable event history.

Store:
- Timestamp.
- Event type.
- Source component.
- Operator.
- Target identifier.
- Scope decision.
- Action.
- Result.
- Evidence reference.
- Error details.

Use SQLite as the authoritative event store.

Generate an atomic `ledger.json` snapshot for convenient export.

Do not silently modify historical records.

## THE GRAVEYARD 💀

Historical view of:
- Resolved incidents.
- Failed services.
- Recovered services.
- Rejected submissions.
- Completed operations.
- Retired honeypot events.

Allow filtering by time, event type, service, and operator.

## THE AUTOPSY 🧬

Incident investigation module.

For every incident, display:
- What happened.
- When it happened.
- Which service was affected.
- Evidence collected.
- Relevant logs.
- Timeline.
- Severity.
- Root-cause hypotheses.
- Confidence level.
- Recommended next steps.
- Resolution status.

Separate verified facts from hypotheses.

## DEAD MAN'S SWITCH 🚨

Emergency protection system.

Trigger a safe suspension when:
- An out-of-scope target is detected.
- Scope configuration becomes invalid.
- Critical configuration is missing.
- The operator activates the emergency stop.
- A safety invariant is violated.
- A component begins an unauthorized operation.

Stop new operations, cancel supported workers, preserve evidence, and display the reason.

Never delete evidence during emergency shutdown.

## LAST BREATH ⏳

Competition countdown and end-of-game reporting.

Display:
- Time remaining.
- Current verified score information, if available.
- Submission queue.
- Outstanding incidents.
- Service-health summary.
- Final operational checklist.

Generate a final report when the competition ends.

## AFTER ACTION 📋

Automatically generate reports after significant operations or configured competition ticks.

Include:
- Events.
- Results.
- Service status.
- Flag-submission results.
- Incidents.
- Defensive actions.
- Outstanding risks.
- Lessons learned.

## SILENT WATCH 👁

A low-noise monitoring mode.

Only notify operators about events meeting configured severity thresholds.

## NIGHTMARE MODE ☠

An optional high-intensity visual theme.

Use:
- Red warning accents.
- Glitch transitions.
- Darker backgrounds.
- More aggressive radar animations.
- Stronger terminal styling.

Do not make the system harder to operate or conceal real warnings.

---

# 8. OPERATIONAL INTELLIGENCE FEATURES

Implement the following where supported by actual data:

1. AI threat intelligence analyst.
2. Live network hologram.
3. Digital forensic wall.
4. Tick prediction engine.
5. AI command intelligence.
6. Approved service recovery.
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

Predictions must be based on actual historical data and clearly marked as estimates.

Do not invent intelligence about competitors.

Do not claim to know another team's plans, machine state, identities, or vulnerabilities without authorized evidence.

---

# 9. THE FOUR-PERSON TEAM WAR ROOM

The physical competition room has four members per team.

Make the system useful for a team operating side by side.

Provide:

- One shared command dashboard.
- Four operator identities.
- Four task assignments.
- Shared notes.
- Internal alerts.
- Incident ownership.
- A common activity timeline.
- A task priority queue.
- A team status panel.
- A shared countdown.
- A team communication feed.

Suggested default division:

**Operator 01 — COMMAND**
- Oversees the competition.
- Monitors the scoreboard.
- Assigns priorities.
- Coordinates the team.
- Approves high-impact actions.

**Operator 02 — ATTACK OPERATIONS**
- Runs approved checks against authorized competition targets.
- Tracks assigned challenge work.
- Reviews findings.
- Sends validated results to the appropriate workflow.

**Operator 03 — DEFENCE**
- Monitors our services.
- Reviews alerts.
- Investigates service failures.
- Applies approved defensive fixes.
- Verifies recovery.

**Operator 04 — INTELLIGENCE**
- Reviews logs and forensic evidence.
- Monitors flag submissions.
- Maintains challenge notes.
- Tracks competition events.
- Supports incident analysis.

All roles must be configurable.

Provide a large-screen WAR ROOM mode suitable for displaying on a shared monitor or projector.

---

# 10. INTIMIDATING PUBLIC-FACING PRESENCE

Create a theatrical visual identity for our own dashboard, approved team display, and honeypot.

The goal is to make the platform feel like an advanced cyber command centre.

Do not write to other teams' terminals, desktops, shells, or machines.

Do not create a remote banner injector or unauthorized calling-card deployment tool.

Instead, create three experiences:

### A. OUR WAR ROOM

A large, cinematic public-facing display that can be shown on our own monitor.

Suggested text:

`WE ARE ONLINE.`

`WE ARE WATCHING OUR NETWORK.`

`WE ARE PROTECTING OUR SERVICES.`

`EVERY PACKET TELLS A STORY.`

### B. THE ECHO CHAMBER

A fictional terminal simulation accessible only through our own honeypot or local demonstration environment.

It can display creepy fictional text such as:

`ACCESS RECORDED.`

`THE MACHINE REMEMBERS.`

`YOU HAVE ENTERED THE ECHO CHAMBER.`

`THIS SESSION IS A SIMULATION.`

The simulation must not falsely claim that it has compromised a visitor's computer, identified a person, or obtained their credentials.

### C. THE TEAM DISPLAY

A room-facing display showing:
- Four operator panels.
- Live competition timer.
- Verified service health.
- Verified flag-submission progress.
- Current incidents.
- Live network visualization.
- The project title and tagline.

Only display data that the platform has actually collected.

---

# 11. ICON AND EMOJI LANGUAGE

Use a consistent icon vocabulary.

| Symbol | Meaning |
|---|---|
| ☠ | Project identity / critical system |
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
| 🧪 | Sandbox / testing |
| ⚡ | Active operation |
| 🛡️ | Defence |
| 🎯 | Authorized target |
| 🕶️ | Intelligence |
| 🧨 | Simulated threat |
| 🦠 | Malware-related alert |
| 🔥 | Critical system event |

Use icons consistently, not randomly.

Use text labels alongside icons so the system remains accessible.

---

# 12. SOUND DESIGN

Add optional sound effects.

Possible sounds:
- Startup rumble.
- Radio static.
- Radar ping.
- Mechanical confirmation click.
- Flag accepted sound.
- Warning tone.
- Emergency alert.
- Heartbeat ambience.
- Glitch transition.
- Atmospheric background.

Requirements:
- Sound disabled or low-volume by default.
- Mute button always visible.
- Independent volume control.
- No continuous loud audio.
- No sound that interferes with the competition room.

Use original or properly licensed sounds.

---

# 13. AUTOMATION AND PERSISTENCE

The platform must continue running even if Claude Code closes.

Implement:

- Persistent daemon.
- Process supervision.
- Process lock.
- Heartbeat.
- Graceful shutdown.
- Worker supervision.
- Persistent job queue.
- Retry handling.
- Health checks.
- Crash recovery.
- Structured logs.
- Configuration validation.

The scheduler should prioritize:
1. Emergency safety conditions.
2. Flag submission.
3. Defensive monitoring.
4. Incident response.
5. Honeypot monitoring.
6. Approved reconnaissance.
7. Intelligence analysis.
8. Reporting.

Intervals must be configurable and comply with competition limits.

Do not create uncontrolled scanning loops or unlimited worker spawning.

---

# 14. CONFIGURATION AND SECRETS

Create a clean configuration system.

Use:
- `.env.example`
- Local `.env`
- Configuration validation.
- Secrets redaction.
- File permissions.
- Clear setup instructions.

Never commit real credentials, API tokens, passwords, VPN keys, or private competition information.

Never print secrets in the dashboard or logs.

The user will provide the official competition credentials and API documentation locally.

Do not guess API endpoints or request formats.

---

# 15. TERMINAL COMMAND CENTRE

Create a professional interactive terminal interface.

The startup banner must show the exact project name:

`We THOUGHT THIS WAS WORLD WAR 3`

Include:
- ASCII skull artwork.
- Red and cyan terminal accents.
- Live system status.
- Competition timer.
- Daemon heartbeat.
- Service health.
- Active incidents.
- Submission queue.
- Operator status.

Provide intuitive commands, for example:

- `ww3 status`
- `ww3 dashboard`
- `ww3 warroom`
- `ww3 scope show`
- `ww3 scope validate`
- `ww3 monitor status`
- `ww3 defence status`
- `ww3 flags queue`
- `ww3 flags status`
- `ww3 incidents`
- `ww3 ghost status`
- `ww3 overseer brief`
- `ww3 echo status`
- `ww3 report`
- `ww3 emergency-stop`
- `ww3 resume`

Commands must map to real implemented functionality.

Do not display fake results.

The emergency-stop command must be immediately available and must work even if the dashboard is unavailable.

---

# 16. PERFORMANCE AND RELIABILITY

The system must be efficient on modest hardware.

Requirements:
- Avoid unnecessary animation loops.
- Use WebSocket updates instead of excessive polling.
- Limit chart refresh rates.
- Use asynchronous operations carefully.
- Implement bounded queues.
- Limit concurrent tasks.
- Avoid memory leaks.
- Provide reduced-effects mode.
- Monitor CPU, RAM, and disk usage.
- Keep critical monitoring independent of visual rendering.

The frontend must never be responsible for keeping the backend alive.

---

# 17. TESTING AND VERIFICATION

Build tests for every major module.

At minimum, test:

- Scope validation.
- CIDR parsing.
- Out-of-scope rejection.
- Safety enforcement.
- Emergency stop.
- Daemon recovery.
- Database persistence.
- Flag format validation.
- Duplicate flag handling.
- Mock flag API responses.
- Accepted/rejected submission handling.
- Rate limiting.
- Honeypot command simulation.
- Honeypot isolation.
- No credential collection.
- No arbitrary shell execution.
- Incident creation.
- Incident resolution.
- Service-health checks.
- Configuration validation.
- Secrets redaction.
- WebSocket reconnection.
- Frontend performance mode.

Use a mock competition API for tests.

Never test against real competition targets unless the user explicitly configures an authorized test environment.

---

# 18. DOCUMENTATION

Create and maintain:

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

Explain how to install, configure, run, stop, test, recover, and operate the platform.

Document all assumptions about the competition API and rules.

---

# 19. IMPLEMENTATION PHASES

Do not try to build everything in one unverified operation.

## PHASE 0 — AUDIT AND FOUNDATION

- Inspect existing files.
- Audit the project.
- Validate the architecture.
- Create configuration and scope engine.
- Create database.
- Create logging and event history.
- Create safety controls.
- Create test framework.

## PHASE 1 — CORE OPERATIONS

- Build the daemon.
- Build the scheduler.
- Build monitoring.
- Build flag pipeline.
- Build official API adapter.
- Build incident response.
- Build terminal commands.

## PHASE 2 — INTELLIGENCE

- Build THE OVERSEER.
- Build GHOST PROTOCOL.
- Build THE WATCHTOWER.
- Build THE AUTOPSY.
- Build THE BLACK BOX.
- Build THE GRAVEYARD.
- Build AFTER ACTION.

## PHASE 3 — HONEYPOT

- Build THE ECHO CHAMBER.
- Implement the simulated shell.
- Isolate the environment.
- Verify no credential collection.
- Verify no arbitrary command execution.
- Verify permitted network exposure only.

## PHASE 4 — WAR ROOM INTERFACE

- Build THE WAR ROOM.
- Build the four-operator view.
- Build live network visualization.
- Build incident and flag panels.
- Build the large-screen team display.

## PHASE 5 — VISUAL EXPERIENCE

- Implement the full colour system.
- Implement HUD effects.
- Implement NIGHTMARE MODE.
- Implement SILENT WATCH.
- Implement PERFORMANCE MODE.
- Implement sound settings.

## PHASE 6 — INTEGRATION AND VERIFICATION

- Run all tests.
- Verify safety controls.
- Verify daemon persistence.
- Verify database recovery.
- Verify frontend/backend communication.
- Verify mock API integration.
- Fix all failures.
- Produce a final readiness report.

## PHASE 7 — COMPETITION OPERATION

Only after the operator supplies and verifies the official rules, scope, credentials, and API documentation:

- Validate configuration.
- Confirm all targets are authorized.
- Run pre-competition checks.
- Start the daemon.
- Monitor continuously.
- Respect the competition end condition.
- Stop safely when the competition ends or the operator requests it.

---

# 20. FINAL ACCEPTANCE CRITERIA

Do not claim the project is complete until:

1. The backend starts successfully.
2. The frontend starts successfully.
3. The terminal interface works.
4. The daemon runs independently.
5. The database persists events.
6. Scope checks reject unauthorized destinations.
7. The emergency stop works.
8. The official API adapter is based on supplied documentation.
9. Mock submission tests pass.
10. Only explicitly confirmed submissions show as accepted.
11. The honeypot is isolated and simulated safely.
12. The four-person team interface works.
13. The WAR ROOM displays real application data.
14. Visual modes work.
15. Performance mode works.
16. Documentation is complete.
17. Tests pass.
18. No secrets are committed.
19. No unauthorized remote terminal or calling-card functionality exists.
20. All project branding uses the exact title:

**We THOUGHT THIS WAS WORLD WAR 3**

---

# 21. HOW YOU MUST WORK AS CLAUDE CODE

Work like an engineer responsible for a real competition system.

- Inspect before modifying.
- Plan before implementing.
- Build incrementally.
- Test every module.
- Never silently ignore errors.
- Never invent successful results.
- Never invent competition rules or API details.
- Never remove working functionality without a reason.
- Never expose credentials.
- Never cross configured scope.
- Never hide uncertainty.
- Never leave critical safety checks as TODOs.
- Never claim a feature works before testing it.

After each phase, provide:
- Files created.
- Files modified.
- Features completed.
- Tests executed.
- Test results.
- Remaining issues.
- Next implementation step.

If a feature cannot be safely implemented, explain why and provide a safe alternative.

**Do not stop after producing a plan or attractive mockup. Build the actual working application, test it, document it, and verify it.**

# FINAL DIRECTIVE

Build a system that looks like a futuristic intelligence agency's cyber operations centre, operates like a disciplined security engineering platform, and helps four team members coordinate under competition pressure.

Make it visually unforgettable.

Make it operationally reliable.

Make it fast.

Make it intelligent.

Make it terrifying in appearance—but controlled, evidence-driven, and competition-compliant in operation.

# ☠ We THOUGHT THIS WAS WORLD WAR 3

**SEE EVERYTHING. PROTECT EVERYTHING. MISS NOTHING.**
