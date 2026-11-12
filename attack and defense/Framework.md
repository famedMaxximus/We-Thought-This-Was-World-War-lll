# MASTER BUILD PROMPT
# We THOUGHT THIS WAS WORLD WAR 3
## Advanced Attack & Defence CTF Command, Control, Automation and Intelligence Framework

---

# 0. YOUR ROLE AND MISSION

You are the lead software architect, senior Python engineer, cybersecurity engineer, DevSecOps engineer, UI/UX designer, network security engineer, and autonomous CTF operations engineer responsible for building a complete Attack & Defence CTF command-and-control framework.

The official project name is:

# We THOUGHT THIS WAS WORLD WAR 3

This is the exact project name. Preserve the capitalization and wording everywhere:

- Source code and project metadata.
- Terminal banners.
- Web dashboard.
- Startup animations.
- Documentation.
- Reports.
- Logs and generated files.
- Honeypot interface.
- Installation screens.
- System notifications.

Never rename it to "World War III", "WORLD WAR 3", or another variation.

The mission is to build a complete, highly automated Attack & Defence competition framework that operates from ONE central machine and coordinates the team's competition operations.

The framework must be developed in two major phases:

**PHASE 0 — BUILD AND VERIFY**

Build the entire framework, implement its components, configure the environment, test every module, and verify that all safety controls work before competition operations begin.

**PHASE 1 — OPERATE**

After Phase 0 passes, operate continuously throughout the competition until I explicitly say `STOP`, `GAME OVER`, or the competition scoreboard is finalized.

Do not start competition operations while Phase 0 is incomplete.

## 0.1 Core objectives

The framework must:

1. Keep our assigned services running and healthy.
2. Continuously monitor our team's machines.
3. Identify service failures and security weaknesses in our own infrastructure.
4. Monitor authorized competition targets.
5. Perform permitted Attack & Defence reconnaissance and vulnerability validation.
6. Capture genuine flags through competition-authorized mechanisms.
7. Automatically validate and submit captured flags through the official submission API.
8. Track submissions and rejected flags.
9. Monitor network activity and detect attacks against our infrastructure.
10. Operate a controlled honeypot on infrastructure assigned to our team.
11. Record attacker activity and extract useful defensive intelligence.
12. Display all important activity in a live web dashboard.
13. Provide a powerful terminal command centre.
14. Maintain a reliable event ledger and complete audit history.
15. Continue running independently of the Claude Code session.
16. Notify me when human intervention is genuinely necessary.

The primary operational priorities are:

1. Keep our services up.
2. Submit every legitimate captured flag as quickly as possible.
3. Maintain complete visibility of our infrastructure.
4. Detect and respond to attacks.
5. Avoid unnecessary operations that could affect competition availability or violate the rules.

Everything must be measurable, logged, testable, and observable.

---

# 1. ARCHITECTURE

Build a centralized architecture.

There is ONE central control machine running the framework.

The central machine communicates with:

- Our assigned team machines.
- Our assigned competition services.
- Authorized opponent machines within the competition scope.
- Our honeypot infrastructure.
- The official scoreboard and flag submission API.
- The competition VPN.

The central machine must provide two primary interfaces:

**A. Web Command Centre**

A real-time browser-based dashboard for monitoring, operating, and investigating the competition.

**B. Terminal Command Centre**

A powerful CLI for controlling the framework, inspecting events, reviewing findings, managing submissions, and operating the system.

Both interfaces must use the same backend, database, event system, and operational state.

## 1.1 Recommended technology stack

Use the following unless a demonstrable technical reason requires a change:

Backend:
- Python 3.11+
- FastAPI
- Pydantic
- SQLAlchemy
- WebSockets
- AsyncIO

Frontend:
- React
- TypeScript
- Vite
- Tailwind CSS
- Recharts or an equivalent visualization library
- Framer Motion for controlled animations

Database:
- SQLite initially, with a clean PostgreSQL migration path.
- SQLAlchemy models.
- Transaction-safe event processing.

Infrastructure:
- Docker and Docker Compose.
- systemd or an equivalent process supervisor.
- Redis only if justified by actual concurrency requirements.
- Structured JSON logging.

Security and monitoring integrations, where available:
- Nmap.
- Zeek.
- Suricata.
- tshark.
- auditd.
- Wazuh.
- Linux service health checks.
- Docker health checks.

Do not assume every tool is installed. Detect dependencies and provide clear installation instructions.

## 1.2 Architecture requirements

Implement the following independent modules:

```text
core/
    orchestrator.py
    scheduler.py
    lifecycle.py
    configuration.py
    scope_manager.py
    safety_engine.py
    event_bus.py
    process_manager.py

attack/
    reconnaissance.py
    service_discovery.py
    vulnerability_assessment.py
    authorized_validation.py
    flag_discovery.py
    target_inventory.py
    evidence_manager.py

defence/
    service_monitor.py
    host_monitor.py
    network_monitor.py
    integrity_monitor.py
    process_monitor.py
    login_monitor.py
    incident_detector.py
    response_engine.py
    recovery_engine.py

intelligence/
    network_topology.py
    opponent_inventory.py
    service_fingerprinting.py
    attack_timeline.py
    threat_analysis.py
    intelligence_correlator.py

flags/
    flag_detector.py
    flag_validator.py
    submission_client.py
    submission_queue.py
    retry_manager.py
    submission_tracker.py

honeypot/
    honeypot_manager.py
    fake_sshd.py
    fake_services.py
    echo_chamber.py
    canary_manager.py
    activity_logger.py
    deception_dashboard.py

dashboard/
    backend/
    frontend/

terminal/
    cli.py
    commands.py
    terminal_dashboard.py
    banner.py

database/
    models.py
    connection.py
    migrations/
    repository.py

notifications/
    alert_manager.py
    escalation_manager.py

tools/
    verify_kit.py
    emergency_cleanup.py
    health_check.py
    backup.py

tests/
    unit/
    integration/
    security/
    simulation/

assets/
    banners/
    icons/
    animations/

config/
    config.example.yaml
    logging.yaml
    policies.yaml

logs/
reports/
patches/
exploits/
```

You may improve this structure as the project develops, but maintain clear separation of responsibilities.

Do not put the entire application into one Python file.

---

# 2. RULES OF ENGAGEMENT AND SAFETY ENGINE

This section is mandatory.

Every operation must follow the official competition rules and the scope I provide.

## 2.1 Competition scope

The file:

`competition_scope.txt`

will contain the IP addresses and CIDR ranges explicitly authorized for competition operations.

Use Python's `ipaddress` library to parse and validate IPs and CIDRs.

Do not use simple substring matching or grep as the security boundary.

Before every network operation:

1. Identify the destination.
2. Resolve the destination if applicable.
3. Validate it against the authorized scope.
4. Verify the operation is allowed by the competition policy.
5. Apply rate limits.
6. Record the decision.
7. Execute only if all checks pass.

The scope manager must distinguish:

- Our own assigned infrastructure.
- Authorized opponent competition targets.
- Competition VPN infrastructure.
- Official scoreboard and submission endpoints.
- Organizer infrastructure.
- Unknown or unauthorized destinations.

The scoreboard and submission endpoint may only be contacted for their documented competition functions.

Never attack organizer infrastructure or scoreboard infrastructure.

Never use a network target simply because it is reachable.

## 2.2 Mandatory restrictions

The framework must NEVER:

- Attack machines outside the explicitly authorized competition scope.
- Disable security controls, sandboxing, hooks, or policy enforcement.
- Modify remote SSH authentication configuration.
- Modify remote password databases or PAM configuration.
- Delete or corrupt remote service binaries.
- Execute destructive operations.
- Perform denial-of-service attacks.
- Use uncontrolled network flooding.
- Establish unauthorized persistence.
- Steal credentials or collect real passwords.
- Inject content into active terminal sessions.
- Use `wall`, `write`, or `/dev/pts/*` against other machines.
- Deface other teams' websites.
- Plant calling cards on opponents' machines.
- Modify another team's SSH login environment.
- Manipulate another team's service availability.
- Impersonate another team.
- Exfiltrate personal information.
- Run arbitrary commands obtained from a remote machine.
- Treat an obtained shell as unrestricted permission.

Do not implement remote calling-card deployment.

Replace that original feature with a local verified-access intelligence record that displays the target, evidence, timestamp, and competition-authorized status.

## 2.3 Human approval

Automate routine, explicitly permitted tasks.

Require human approval for:

- Ambiguous competition permissions.
- Potentially disruptive tests.
- Changes that could interrupt a service.
- Unrecognized remediation actions.
- Operations with uncertain scope.
- Actions outside predefined allowlists.

The AI assistant must never override the safety engine.

## 2.4 Emergency stop

Implement an immediate emergency stop.

The following commands must stop active operations:

```text
STOP
GAME OVER
ww3 stop
ww3 emergency
```

The emergency stop must:

- Stop new attack jobs.
- Stop new scanning jobs.
- Stop submission retries.
- Stop scheduled operations.
- Preserve the database and logs.
- Safely stop managed local containers and processes.
- Preserve the final competition state.
- Generate a final report.

Do not terminate unrelated system processes.

---

# 3. CONFIGURATION AND CREDENTIALS

I will provide competition credentials and configuration locally.

Never ask me to paste passwords, API tokens, or private keys into a prompt or source file.

Create a configuration wizard.

Example configuration:

```yaml
project:
  name: "We THOUGHT THIS WAS WORLD WAR 3"
  environment: "competition"
  timezone: "Africa/Maseru"

competition:
  team_id: ""
  competition_name: ""
  tick_seconds: 120
  competition_end_time: null

network:
  vpn_interface: ""
  scope_file: "competition_scope.txt"

submission:
  enabled: false
  api_url: ""
  method: ""
  flag_field: ""
  authentication_type: ""
  token_environment_variable: ""

team:
  machines: []
  services: []

honeypot:
  enabled: true
  listen_interface: ""
  allowed_ports: []

operations:
  automated_defence: true
  automated_reconnaissance: true
  automated_flag_submission: true
  require_approval_for_disruptive_actions: true
```

This is an example schema, not a real credential configuration.

Use environment variables or an operating-system credential store for secrets.

Create:

```text
.env.example
```

Never commit `.env`.

On startup:

- Detect missing credentials.
- Detect unconfigured submission endpoints.
- Detect missing scope entries.
- Detect invalid configuration.
- Explain what is missing.
- Stop operations that depend on incomplete configuration.

Do not invent API endpoints, authentication formats, request fields, or competition rules.

I will supply the official API documentation or configuration.

Build the submission adapter around the actual documentation.

---

# 4. PHASE 0 — BUILD EVERYTHING BEFORE OPERATIONS

This phase has priority over everything else.

Build the entire system first.

Do not begin competition scanning or attack operations during development.

## 4.1 Development sequence

Work in the following order.

### Step 1: Inspect the environment

- Inspect the existing project directory.
- Read `CLAUDE.md` fully.
- Inspect existing files and folders.
- Identify available system tools.
- Identify Python and Node versions.
- Identify Docker availability.
- Identify available network interfaces.
- Identify installed monitoring tools.
- Identify existing competition configuration.
- Preserve useful existing work.

Do not overwrite valuable files without inspecting them.

### Step 2: Build the backend

Implement:

- Application configuration.
- Database.
- Authentication for the local dashboard.
- Scope enforcement.
- Safety engine.
- Event bus.
- Orchestrator.
- Scheduler.
- Module interfaces.
- Audit logging.
- API endpoints.
- WebSocket events.

### Step 3: Build the operational engines

Implement the attack, defence, intelligence, flag, and honeypot modules.

### Step 4: Build the dashboard

Build the full command centre.

### Step 5: Build the terminal interface

Implement all terminal commands and interactive displays.

### Step 6: Build the independent daemon

Create a background service that runs independently of Claude Code.

### Step 7: Build the test suite

Test each module individually and as an integrated system.

### Step 8: Verify everything

Run the full verification process.

Only when every critical check passes may the framework enter competition operation mode.

---

# 5. CENTRAL COMMAND CENTRE — WEB DASHBOARD

The dashboard is a core component, not a decorative afterthought.

It must look like an advanced military cyber operations centre, SOC, and futuristic intelligence platform.

The visual experience should be inspired by sophisticated fictional cyber command systems.

## 5.1 Visual identity

Official title:

**We THOUGHT THIS WAS WORLD WAR 3**

Design direction:

- Near-black background.
- Deep charcoal panels.
- Neon red threat indicators.
- Electric cyan and blue intelligence displays.
- Green operational indicators.
- Amber warnings.
- White typography.
- Monospaced technical typography.
- Subtle glowing borders.
- Animated scanning lines.
- Radar rings.
- Network grids.
- Live telemetry.
- 3D wireframe effects where performance allows.
- Targeting overlays.
- Moving data traces.
- Waveforms.
- Tactical maps.
- Animated alert indicators.
- Command-line-inspired elements.

The interface must feel alive.

Use motion purposefully.

Do not make the interface cluttered.

Do not sacrifice readability or responsiveness for effects.

Support desktop and smaller displays.

## 5.2 Dashboard navigation

Create these main sections:

1. OVERVIEW
2. ATTACK OPERATIONS
3. DEFENCE OPERATIONS
4. NETWORK INTELLIGENCE
5. TARGET INVENTORY
6. FLAG CONTROL
7. HONEYPOT
8. INCIDENT RESPONSE
9. SERVICES
10. ACTIVITY TIMELINE
11. ALERTS
12. TERMINAL
13. SYSTEM HEALTH
14. SETTINGS

## 5.3 Overview dashboard

The main screen must display:

### Competition status

- Competition name.
- Team ID.
- Current tick.
- Elapsed competition time.
- Competition status.
- Connection status.
- VPN status.
- Framework status.
- Daemon status.

### Operational statistics

- Total flags discovered.
- Total flags validated.
- Total flags submitted.
- Accepted flags.
- Rejected flags.
- Pending submissions.
- Submission success rate.
- Average capture-to-submit time.
- Our services online.
- Our services offline.
- Active incidents.
- Honeypot connections.
- Security alerts.
- Active authorized jobs.

### Visual components

- Live network topology.
- Service health overview.
- Attack and defence activity timeline.
- Flag submission chart.
- Network traffic visualization.
- Threat radar.
- Recent events.
- Active incidents.
- System health.
- Current operational status.

All production dashboard data must come from the real backend.

Never invent live results.

Clearly label simulated test data.

## 5.4 Network topology

Build an interactive network map.

Show:

- Our central machine.
- Our team machines.
- Our services.
- Authorized opponent targets.
- Honeypot.
- Competition VPN.
- Official submission endpoint.

Each node must have a status.

Possible states:

- ONLINE
- OFFLINE
- UNKNOWN
- UNDER INVESTIGATION
- WARNING
- COMPROMISED — VERIFIED
- PROTECTED
- HONEYPOT

Only show COMPROMISED when supported by actual authorized evidence.

Clicking a node opens its details.

## 5.5 Live activity feed

Show a live stream of important events.

Examples:

```text
[16:04:11] SYSTEM       Framework initialized
[16:04:12] NETWORK      VPN connection verified
[16:04:14] DEFENCE      Web service health check passed
[16:04:18] ATTACK       Authorized assessment started
[16:04:21] FLAGS        Genuine flag candidate detected
[16:04:22] FLAGS        Flag validation passed
[16:04:23] SUBMISSION   Official API accepted submission
[16:04:29] HONEYPOT     New inbound connection detected
```

Use timestamps and severity indicators.

Events must be real and generated by the backend.

## 5.6 Threat radar

Create a live threat radar displaying:

- Detected source IPs.
- Honeypot activity.
- Suspicious connections.
- Unusual traffic.
- Failed login attempts.
- Port scanning indicators.
- Attack patterns.
- Incident severity.

The radar must be backed by actual collected events.

Do not fabricate attackers or attribution.

---

# 6. ATTACK OPERATIONS ENGINE

This module is responsible for authorized competition reconnaissance, assessment, and flag discovery.

It must be modular and rule-aware.

## 6.1 Target inventory

Import targets from:

```text
competition_scope.txt
```

Classify each target.

Track:

- IP address.
- Hostname.
- Team classification, if officially known.
- Discovered ports.
- Services.
- Service versions.
- Last seen.
- Last scan.
- Assessment status.
- Findings.
- Evidence.
- Flags discovered.
- Operational notes.

## 6.2 Reconnaissance

Implement controlled reconnaissance.

Use tools such as:

- Nmap.
- Service fingerprinting.
- DNS lookups where authorized.
- TCP connectivity checks.
- HTTP service discovery.
- TLS certificate inspection.
- Banner identification.

Use configurable scan profiles.

Example:

```text
LIGHT
STANDARD
DETAILED
MANUAL
```

All profiles must respect:

- Competition scope.
- Rate limits.
- Time budgets.
- Explicitly permitted techniques.

Do not use aggressive scan profiles by default.

## 6.3 Service discovery

Identify:

- HTTP.
- HTTPS.
- SSH.
- FTP.
- DNS.
- SMTP.
- Databases.
- Custom TCP services.
- Other discovered competition services.

Record service fingerprints and changes over time.

## 6.4 Vulnerability assessment

Implement a finding system that records:

- Finding ID.
- Target.
- Service.
- Vulnerability category.
- Severity.
- Evidence.
- Timestamp.
- Validation status.
- Recommended remediation.
- Competition rule reference.

Use safe validation first.

Only execute competition-authorized exploit modules that are explicitly configured and compatible with the rules.

Never run arbitrary exploit scripts simply because they exist in the `exploits/` directory.

Every module must declare:

- Supported target types.
- Required permissions.
- Expected impact.
- Network requirements.
- Timeout.
- Rate limit.
- Cleanup requirements.
- Safety classification.

Require approval when an action is potentially disruptive or outside the established allowlist.

## 6.5 Flag discovery

Implement a flag detection pipeline.

A flag candidate must include:

- Candidate ID.
- Source target.
- Source service.
- Discovery method.
- Discovery timestamp.
- Tick.
- Evidence reference.
- Validation result.
- Submission status.

Validate the flag format against the actual competition format.

Do not treat arbitrary text as a valid flag.

Never submit honeypot canaries or invented flags.

Never expose actual flags in ordinary logs or dashboard notifications unnecessarily.

Store sensitive flag values securely in the database.

---

# 7. FLAG CONTROL AND OFFICIAL SUBMISSION ENGINE

This is one of the highest-priority modules.

The framework must submit legitimate captured flags quickly and reliably.

## 7.1 Submission pipeline

```text
FLAG DETECTED
      |
      v
VALIDATION
      |
      v
DUPLICATE CHECK
      |
      v
SUBMISSION QUEUE
      |
      v
OFFICIAL API REQUEST
      |
      v
RESPONSE VERIFICATION
      |
      v
DATABASE UPDATE
      |
      v
DASHBOARD + EVENT NOTIFICATION
```

## 7.2 Submission states

Implement:

- DISCOVERED
- VALIDATING
- INVALID
- DUPLICATE
- QUEUED
- SUBMITTING
- ACCEPTED
- REJECTED
- PENDING
- RETRYING
- ERROR

Only mark a flag ACCEPTED when the official API explicitly confirms acceptance.

Never infer acceptance from:

- HTTP 200 alone.
- A successful TCP connection.
- A local simulation.
- A command returning without an error.
- A fabricated response.

Parse the documented API response.

## 7.3 Submission reliability

Implement:

- Deduplication.
- Persistent queue.
- Atomic database transactions.
- Retry with exponential backoff.
- Request timeouts.
- API rate-limit handling.
- Idempotency where supported.
- Error classification.
- Submission history.
- Per-flag audit records.

The submission worker must operate independently of the dashboard.

Target a capture-to-submission time below 10 seconds where the API and competition rules permit.

Never bypass API rate limits.

## 7.4 Flag dashboard

Display:

- Captured flags.
- Validated flags.
- Submitted flags.
- Accepted flags.
- Rejected flags.
- Pending flags.
- Submission history.
- API health.
- Submission latency.
- Failure reasons.

Provide filters by:

- Tick.
- Target.
- Service.
- Status.
- Time.
- Discovery source.

---

# 8. DEFENCE OPERATIONS ENGINE

Defence is a top operational priority.

Our services must remain available throughout the competition.

The framework must continuously monitor our assigned infrastructure.

## 8.1 Service monitoring

Monitor every configured service.

Track:

- Host.
- Port.
- Protocol.
- Service name.
- Health status.
- Response time.
- HTTP response.
- Expected response.
- Last successful check.
- Last failure.
- Uptime percentage.

Check services at configurable intervals.

Default target interval: every 30 seconds.

## 8.2 Host monitoring

Where authorized and supported, monitor:

- CPU utilization.
- Memory usage.
- Disk usage.
- Network utilization.
- Running processes.
- Service state.
- System load.
- Authentication logs.
- Unusual process changes.

## 8.3 Network monitoring

Detect:

- Unusual inbound connections.
- Unexpected outbound connections.
- Repeated connection attempts.
- Suspicious ports.
- Traffic spikes.
- Unexpected listening services.
- Network configuration changes.

Use available integrations such as Zeek, Suricata, and tshark.

## 8.4 File integrity monitoring

Monitor important files on our own machines.

Detect:

- Unexpected changes.
- Modified service configurations.
- Changed binaries.
- New files in sensitive directories.
- Unexpected permission changes.
- Unexpected startup entries.

Maintain approved baseline hashes.

## 8.5 Login monitoring

Monitor our own assigned systems for:

- Failed authentication attempts.
- Successful unexpected logins.
- Repeated login attempts.
- Unusual login times.
- New accounts.
- Privilege changes.

Do not collect passwords.

## 8.6 Automatic defence

The response engine may automatically perform approved, reversible actions on our own infrastructure.

Examples:

- Restarting a failed managed service.
- Restarting an unhealthy local container.
- Restoring an approved configuration backup.
- Reapplying a known-good configuration.
- Disabling an unauthorized local service when explicitly allowlisted.
- Isolating a managed container when policy permits.

Before every change:

1. Record the incident.
2. Capture the current state.
3. Create a backup.
4. Validate the proposed change.
5. Apply the change.
6. Verify service health.
7. Roll back if verification fails.
8. Record the result.

Never blindly patch a production service.

Never apply unverified patches automatically.

## 8.7 Defence dashboard

Display:

- Services online/offline.
- Uptime.
- Health-check results.
- Active incidents.
- Recent failed logins.
- Suspicious processes.
- File integrity changes.
- Recent remediation.
- Recovery history.
- Defence alerts.

---

# 9. NETWORK INTELLIGENCE AND OPPONENT INVENTORY

Create an intelligence module that organizes information obtained through authorized competition observations.

Maintain an inventory of discovered competition services.

For every target, track:

```text
Target ID
IP address
Team association, if officially known
Open ports
Detected services
Service versions
Observed changes
Assessment findings
Evidence
Relevant flags
Last observation
Confidence
```

Create a timeline of observations.

Identify service changes between ticks.

Correlate observations with relevant security findings.

Do not claim a vulnerability is confirmed without evidence.

Do not claim a machine is compromised without verified evidence.

Do not attempt to identify individual people behind IP addresses.

Do not collect personal information.

## 9.1 Intelligence correlation

Correlate:

- Service changes.
- Network observations.
- Honeypot activity.
- Attack indicators.
- Flag discoveries.
- Submission events.
- Our own service health.

Provide useful summaries.

Example:

```text
INTELLIGENCE UPDATE

Target: 10.10.5.12
Observation: HTTP service changed
Previous fingerprint: nginx
Current fingerprint: Apache
Confidence: High
Evidence: Service fingerprint comparison
Recommended action: Reassess exposed application surface
```

---

# 10. HONEYPOT AND DECEPTION SYSTEM

Build a dedicated honeypot system on infrastructure assigned to our team.

Its purpose is to detect unauthorized access attempts, collect safe behavioral telemetry, and provide defensive intelligence.

It must never expose real flags, credentials, internal source code, or sensitive data.

## 10.1 Network isolation

The honeypot must:

- Run in a dedicated Docker container.
- Have no unrestricted outbound internet access.
- Use a controlled inbound path through the competition VPN and host firewall.
- Be isolated from our production services.
- Use resource limits.
- Avoid exposing the Docker socket.
- Avoid privileged container execution.
- Use read-only filesystem access wherever practical.
- Store logs in a controlled persistent volume.

Important technical correction:

Do not use `network_mode: none` if the honeypot is expected to receive inbound connections.

Instead, configure a dedicated internal Docker network and controlled inbound routing through the host firewall.

Block outbound internet access.

Verify isolation through actual tests.

Do not simply assume the container is isolated.

## 10.2 Fake SSH service

Build a fake SSH-like interaction service on a non-standard port.

It must:

- Record connection metadata.
- Record timestamps.
- Record source IP.
- Record attempted usernames.
- Never store attempted passwords.
- Never authenticate against real accounts.
- Never execute attacker-supplied commands.
- Never provide access to the host filesystem.
- Never expose real credentials.
- Never execute real shell commands.

Provide a completely simulated shell.

Commands such as:

```text
help
ls
pwd
whoami
uname -a
ps aux
cat /etc/passwd
cat flag.txt
exit
```

must return fabricated, harmless responses.

Log command attempts and session behavior.

Do not impersonate real teams or insert personal information into fake output.

## 10.3 Echo chamber

Create a fake command-response engine.

It must:

- Simulate a Linux-like environment.
- Return fabricated filesystem listings.
- Display harmless fake processes.
- Display synthetic configuration files.
- Show synthetic service information.
- Record commands.
- Display the official project branding.
- Disconnect cleanly.

The fake shell must never pass attacker commands to `subprocess`, `os.system`, a real shell, or the host.

## 10.4 Canary system

Build a canary manager for our own honeypot.

Canaries may include synthetic files and unique identifiers.

Example:

```text
CANARY_ROOT_<TEAM>_<TICK>_<RANDOM>
CANARY_ENV_<TEAM>_<TICK>_<RANDOM>
CANARY_GIT_<TEAM>_<TICK>_<RANDOM>
```

Possible synthetic locations:

```text
/opt/honeypot/flag.txt
/opt/honeypot/.env
/opt/honeypot/.git/config
/opt/honeypot/home/user/.aws/credentials
/opt/honeypot/home/user/.ssh/id_rsa
```

All contents must be fake.

Never put real credentials or real competition flags in these files.

Before enabling canaries, check the competition rules.

If fake flags or deceptive scoreboard artifacts are prohibited or unclear, disable flag-shaped canaries and use non-submittable unique identifiers instead.

Never submit a canary as a competition flag.

## 10.5 Tarpit

Implement an optional, resource-limited decoy service.

It must operate only on our own honeypot infrastructure.

It must not consume excessive resources, flood connections, or disrupt legitimate scanners.

Make it configurable and disable it by default until competition rules have been checked.

## 10.6 Honeypot intelligence

Record:

- Connection ID.
- Source IP.
- Source port.
- Destination port.
- Timestamp.
- Session duration.
- Attempted username.
- Commands attempted.
- Services accessed.
- Canary identifier accessed.
- Observed behavior.
- Risk classification.

Do not store passwords.

Do not execute commands.

## 10.7 Original Sesotho banner

Create the original terminal banner:

`assets/ww3_sesotho.py`

Preserve these three phrases exactly as written:

```text
Kea Patlotsa Hela Loo
Ke Asau Palesa Nna
Ke Ntatau Sthabi
```

They are decorative flavor text.

Do not translate, explain, rewrite, or alter them.

Preserve the skulls, creepy emojis, animations, and terminal styling from the original specification.

Use the exact project title:

**We THOUGHT THIS WAS WORLD WAR 3**

Use the original visual language:

- ☠
- 💀
- 😈
- 😂
- 🤣
- 👹
- 🩸
- 🕷
- 🕸
- ⚰

Create both:

```text
assets/ww3_sesotho.py
assets/ww3_sesotho_web.html
```

Also create:

```text
assets/ww3_banner.html
```

as a static fallback.

The banner must be used on our own honeypot and dashboard.

Do not inject it into other teams' terminals or machines.

---

# 11. CONTINUOUS OPERATIONS DAEMON

This is a critical architectural requirement.

Claude Code is not the daemon.

The framework must continue operating even when the Claude Code session closes.

Create:

`tools/daemon.py`

The daemon must run independently under systemd or a suitable process supervisor.

It must:

- Start the orchestrator.
- Run scheduled jobs.
- Monitor operational health.
- Process flag queues.
- Perform official API submissions.
- Monitor our services.
- Collect honeypot events.
- Record heartbeats.
- Handle recoverable errors.
- Restart managed workers when appropriate.
- Preserve state across restarts.
- Shut down gracefully.

Use a process lock to prevent duplicate daemon instances.

Do not rely on Claude Code Monitor sessions as the primary source of continuous operation.

## 11.1 Scheduling

Use configurable intervals.

Initial defaults:

| Operation | Interval |
|---|---:|
| Flag submission queue | Continuous |
| Daemon heartbeat | 10 seconds |
| Service health checks | 30 seconds |
| Honeypot event processing | 30 seconds |
| Authorized reconnaissance | 60 seconds |
| Network intelligence refresh | 60 seconds |
| System health review | 60 seconds |
| Monitor health review | 4 minutes |

The competition tick duration must be configurable.

The original default is 120 seconds, but use the actual competition configuration when provided.

Do not let a slow scanning task block flag submission or service monitoring.

Use separate asynchronous workers and bounded concurrency.

Prioritize:

1. Flag submissions.
2. Critical service health.
3. Incident response.
4. Honeypot event processing.
5. Authorized reconnaissance.
6. Intelligence enrichment.

## 11.2 Daemon reliability

Implement:

- Graceful shutdown.
- Heartbeat.
- Process locking.
- Worker supervision.
- Retry management.
- Crash recovery.
- Database transactions.
- Structured logs.
- Health endpoints.
- Startup recovery.
- Persistent queues.

Do not restart the entire application because one worker fails.

---

# 12. DATABASE AND EVENT LEDGER

Use SQLite as the initial authoritative store.

The database must contain:

- Competition.
- Team.
- Machine.
- Service.
- Target.
- Scan.
- Finding.
- Flag.
- Submission.
- Incident.
- Honeypot session.
- Canary event.
- Network observation.
- Action.
- Alert.
- Escalation.
- System heartbeat.

Every important operation must generate an event.

Maintain an append-only event history.

Current status fields may be updated, but historical records must not be deleted.

## 12.1 Ledger snapshot

Also maintain:

`ledger.json`

Example:

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
    "id": "",
    "services": []
  },
  "flags_captured": [],
  "flags_submitted": [],
  "machines_observed": [],
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

SQLite is authoritative.

`ledger.json` is a generated snapshot for inspection and compatibility.

Do not maintain two independent sources of truth.

Use safe atomic snapshot generation and file locking.

---

# 13. TERMINAL COMMAND CENTRE

Build a powerful CLI named:

`ww3`

The terminal should feel like an advanced cyber command centre.

Display the original animated banner when appropriate.

Use Rich or Textual for:

- Tables.
- Live panels.
- Status displays.
- Progress indicators.
- Alerts.
- Network summaries.
- Interactive menus.

## 13.1 Commands

Implement these commands:

```bash
ww3
ww3 start
ww3 stop
ww3 emergency
ww3 status
ww3 dashboard
ww3 config
ww3 verify
ww3 doctor

ww3 targets
ww3 targets list
ww3 targets show <target>

ww3 scan
ww3 scan --profile light
ww3 scan --profile standard

ww3 services
ww3 services status
ww3 services check

ww3 attack status
ww3 attack findings
ww3 attack history

ww3 defence status
ww3 defence incidents
ww3 defence health
ww3 defence recover

ww3 network topology
ww3 network connections

ww3 flags
ww3 flags captured
ww3 flags pending
ww3 flags accepted
ww3 flags rejected
ww3 flags submit

ww3 honeypot status
ww3 honeypot sessions
ww3 honeypot logs

ww3 alerts
ww3 incidents
ww3 timeline
ww3 logs
ww3 report
ww3 backup
ww3 cleanup
```

Commands that perform network actions must always use the scope manager.

Commands that modify infrastructure must follow the approval and rollback policies.

The CLI must clearly explain invalid commands.

## 13.2 Live terminal status

Display a continuously updating status panel.

Example:

```text
☠ We THOUGHT THIS WAS WORLD WAR 3 ☠

SYSTEM STATUS: OPERATIONAL
COMPETITION: ACTIVE
CURRENT TICK: 042
VPN: CONNECTED
DAEMON: RUNNING
DATABASE: HEALTHY

DEFENCE
Services Online:       3/3
Active Incidents:      0
Uptime:                100%

ATTACK
Authorized Jobs:       2
Verified Findings:     4
Flags Discovered:      8

FLAG CONTROL
Accepted:              7
Pending:               0
Rejected:              1

HONEYPOT
Active Sessions:       1
Total Connections:     24
Canary Events:         3

SYSTEM
CPU:                   18%
Memory:                42%
Database:              HEALTHY

[16:04:22] Official API accepted submission.
[16:04:29] Honeypot detected a new connection.
```

All numbers must come from actual application state.

---

# 14. NOTIFICATIONS AND ESCALATION

The framework must not overwhelm me with unnecessary notifications.

Use severity levels:

- INFO
- NOTICE
- WARNING
- HIGH
- CRITICAL

Escalate for:

1. An assigned service remains down after an approved recovery attempt.
2. A legitimate flag is rejected repeatedly.
3. An out-of-scope operation was blocked.
4. The official submission system is unavailable for an extended period.
5. The central daemon is unhealthy.
6. A critical security incident requires human intervention.

Example:

```text
🚨 HUMAN ACTION REQUIRED

Reason: Assigned web service remains offline.
Machine: TEAM-WEB-01
Service: HTTP/80
Attempts: 2
Last status: Connection refused

Recommended action:
Inspect the service and approve recovery.

Time: 16:04:22
```

Do not escalate every temporary connection failure.

Do not escalate harmless honeypot activity.

Keep an escalation history.

---

# 15. EMERGENCY CLEANUP

Create:

`tools/emergency_cleanup.py`

The cleanup process must:

1. Stop accepting new jobs.
2. Stop scheduled reconnaissance.
3. Stop submission retries.
4. Allow in-flight API requests to finish or time out safely.
5. Stop managed background workers.
6. Stop managed honeypot containers.
7. Preserve all logs.
8. Generate the final ledger snapshot.
9. Generate a final report.
10. Record cleanup results.

Only clean up processes and infrastructure managed by this framework.

Never execute arbitrary remote cleanup commands.

Never assume an opponent machine should be modified or restored.

Do not delete evidence or history.

Provide a final summary.

---

# 16. TESTING AND VERIFICATION

The framework must have a serious test suite.

Do not declare the project complete simply because the application starts.

## 16.1 Unit tests

Test:

- Configuration loading.
- Scope validation.
- CIDR matching.
- Safety engine.
- Flag validation.
- Duplicate detection.
- Submission state transitions.
- Retry handling.
- Database transactions.
- Event bus.
- Scheduler.
- Service monitoring.
- Honeypot command simulation.
- Alert severity.
- Emergency stop.

## 16.2 Integration tests

Test:

- Backend and database.
- Dashboard and backend.
- WebSocket updates.
- Terminal and backend.
- Flag queue and mock API.
- Daemon and scheduler.
- Honeypot and event collector.
- Service health monitoring.
- Backup and restore.

Use a mock official submission API during development.

Never send test flags to the real competition endpoint.

## 16.3 Safety tests

Verify that:

- Out-of-scope IPs are blocked.
- Invalid CIDRs are rejected.
- Unknown network destinations are rejected.
- Rate limits work.
- Disallowed actions cannot run.
- Remote arbitrary shell commands cannot run.
- Fake shell commands are never executed.
- Honeypot cannot reach the unrestricted internet.
- Honeypot cannot access production credentials.
- Canaries cannot enter the submission queue.
- Emergency stop works.
- Secrets never appear in logs.

## 16.4 Performance tests

Test:

- Concurrent event ingestion.
- Dashboard updates.
- Submission queue throughput.
- Database growth.
- Daemon restart recovery.
- Memory consumption.
- Long-running operation.

## 16.5 Verification command

Implement:

```bash
python3 tools/verify_kit.py
```

The verifier must check:

1. Required project files exist.
2. Configuration is valid.
3. Required placeholders are resolved for the selected operation.
4. Scope file exists and parses.
5. Database initializes.
6. Backend starts.
7. Dashboard builds.
8. Terminal commands load.
9. Daemon starts and reports healthy.
10. Submission mock tests pass.
11. Honeypot isolation tests pass.
12. Emergency stop tests pass.
13. Unit tests pass.
14. Integration tests pass.

Output:

```text
=============================================
☠ We THOUGHT THIS WAS WORLD WAR 3 ☠
=============================================

[PASS] Configuration
[PASS] Scope validation
[PASS] Database
[PASS] Backend
[PASS] Dashboard build
[PASS] Terminal
[PASS] Daemon
[PASS] Flag pipeline
[PASS] Defence engine
[PASS] Honeypot isolation
[PASS] Emergency stop
[PASS] Unit tests
[PASS] Integration tests

SYSTEM VERIFICATION: KIT OK
```

If a critical test fails:

```text
SYSTEM VERIFICATION: KIT FAIL
```

Do not enter Phase 1.

---

# 17. INSTALLATION AND DEPLOYMENT

Create a one-command setup process.

Provide:

```bash
./install.sh
```

It must:

- Check dependencies.
- Create a Python virtual environment.
- Install Python dependencies.
- Install frontend dependencies.
- Build the dashboard.
- Initialize the database.
- Create required folders.
- Generate `.env.example`.
- Generate example configuration.
- Create systemd service files where supported.
- Run verification.

Provide:

```bash
./start.sh
./stop.sh
./verify.sh
./cleanup.sh
```

Create a comprehensive README.

The README must include:

- Project overview.
- Architecture.
- Requirements.
- Installation.
- Configuration.
- Competition setup.
- Scope configuration.
- API integration.
- Starting the framework.
- Dashboard access.
- Terminal commands.
- Troubleshooting.
- Emergency stop.
- Security considerations.

Do not include actual credentials.

---

# 18. FIRST-RUN PROCEDURE

When I first run the project:

1. Read this specification completely.
2. Inspect the project directory.
3. Inspect the existing `CLAUDE.md`.
4. Inspect existing assets and code.
5. Identify missing configuration.
6. Build Phase 0.
7. Run unit tests.
8. Run integration tests.
9. Run safety tests.
10. Run the complete verifier.
11. Show me the verification report.
12. Explain any unresolved configuration requirements.
13. Do not start competition operations until I explicitly authorize the transition.

If competition credentials, scope, or API documentation are missing, do not invent them.

Build everything that can be safely built without those details.

Use mock services for development and testing.

Do not confuse a successful local test with successful competition connectivity.

---

# 19. PHASE 1 — COMPETITION OPERATIONS

Only enter Phase 1 after:

- Phase 0 passes.
- Scope is configured.
- Competition rules are reviewed.
- Official API configuration is verified.
- I authorize competition operations.

On startup:

```text
☠ We THOUGHT THIS WAS WORLD WAR 3 ☠

C2 INITIALIZATION

[+] Loading configuration
[+] Verifying competition scope
[+] Connecting to competition VPN
[+] Initializing database
[+] Starting event engine
[+] Starting defence monitoring
[+] Starting flag submission worker
[+] Starting intelligence engine
[+] Starting honeypot
[+] Starting dashboard
[+] Starting terminal command centre

SYSTEM STATUS: OPERATIONAL
```

Do not print successful status messages unless the underlying checks really passed.

## 19.1 Continuous operation

Continue operating until:

- I say `STOP`.
- I say `GAME OVER`.
- The scoreboard officially finalizes.
- A critical safety condition requires suspension.

The framework must not rely on Claude Code staying open.

## 19.2 Priority scheduling

At all times:

**Priority 1 — Flag submission**

Process genuine validated flags as quickly as possible.

**Priority 2 — Defence**

Ensure our assigned services are healthy.

**Priority 3 — Incident response**

Investigate and handle security events.

**Priority 4 — Honeypot intelligence**

Collect and classify activity.

**Priority 5 — Authorized reconnaissance**

Perform allowed, rate-limited competition reconnaissance.

**Priority 6 — Intelligence enrichment**

Correlate findings and produce operational summaries.

## 19.3 Tick status

At each competition tick, print a one-line status.

Example:

```text
t42 · services 3/3 ✓ · flags 7/8 accepted · pending 0 · findings 4 · honeypot hits 12 · incidents 0
```

Do not count a rejected or pending flag as accepted.

---

# 20. PERFORMANCE TARGETS

Track these metrics:

| Metric | Target |
|---|---|
| Genuine captured flags submitted | At least 90% |
| Capture-to-submit time | Under 10 seconds where API permits |
| Our assigned services | 100% uptime target |
| Daemon availability | Continuous |
| Out-of-scope operations | Zero |
| Unauthorized modifications | Zero |
| Unapproved disruptive operations | Zero |
| Flag duplication | Prevented |
| False accepted submissions | Zero |
| Honeypot password collection | Zero |
| Real credentials in honeypot | Zero |
| Event history loss | Zero |

Display these metrics in the dashboard.

---

# 21. IMPLEMENTATION RULES FOR CLAUDE CODE

These are your software development instructions.

1. Do not simply generate a project plan. Build the actual application.
2. Inspect existing files before modifying them.
3. Implement one module at a time.
4. Keep modules functional and testable.
5. Use real integrations when configured.
6. Use mocks when external configuration is unavailable.
7. Never fake production data.
8. Never claim a feature is complete if it is only a placeholder.
9. Never leave important modules as empty stubs.
10. Add tests for every important function.
11. Handle exceptions properly.
12. Avoid unnecessary dependencies.
13. Keep the UI responsive.
14. Keep the backend asynchronous where appropriate.
15. Prevent duplicate daemon instances.
16. Protect secrets.
17. Maintain complete audit logs.
18. Do not silently ignore errors.
19. Do not disable safety controls to make a test pass.
20. Do not start competition operations without authorization.

When a task is too large to complete in one development session:

- Break it into implementation phases.
- Complete the current phase properly.
- Test the completed work.
- Update the project documentation.
- Record outstanding work.
- Continue from the documented state.

Do not pretend unfinished work is complete.

---

# 22. REQUIRED DEVELOPMENT DELIVERABLES

At the end of Phase 0, I expect a working project containing:

1. Complete Python backend.
2. Complete web dashboard.
3. Complete terminal command centre.
4. Central orchestrator.
5. Independent background daemon.
6. Competition scope engine.
7. Attack operations modules.
8. Defence monitoring modules.
9. Network intelligence module.
10. Genuine flag validation and submission pipeline.
11. Honeypot system.
12. Original Sesotho terminal banner.
13. Original Sesotho web banner.
14. Database and event ledger.
15. Alert and escalation system.
16. Emergency cleanup.
17. Installation scripts.
18. Configuration wizard.
19. Documentation.
20. Unit tests.
21. Integration tests.
22. Safety tests.
23. Verification tool.
24. System service configuration.

The final project must be operational, modular, secure, and maintainable.

---

# 23. FINAL INSTRUCTION

You are building:

# We THOUGHT THIS WAS WORLD WAR 3

This is not supposed to be a simple port scanner, a basic dashboard, or a collection of scripts.

It is a complete centralized Attack & Defence CTF operations platform.

The central machine must provide one place to monitor our infrastructure, coordinate authorized competition activities, process flags, investigate attacks, observe honeypot activity, and maintain operational awareness.

The web dashboard and terminal command centre must feel like two interfaces to the same advanced cyber operations system.

Build it with a strong engineering foundation.

Prioritize reliability, automation, visibility, speed, security, and operational correctness.

**Do not stop at designing the architecture. Inspect the repository, implement the system, test it, verify it, document it, and show me the working result.**

First action: inspect the existing project and `CLAUDE.md`, then report the current state and begin Phase 0 implementation.

**WE THOUGHT THIS WAS WORLD WAR 3.**
