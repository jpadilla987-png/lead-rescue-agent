# Lead Rescue Voice — Amazon Developer Hackathon Submission Notes

## One-line pitch

Lead Rescue Voice is an Alexa+ style lead-recovery agent that ranks leads by rescue urgency, explains the evidence, prepares safe follow-up, and stops when a decision belongs to the business owner.

## Primary track

Alexa+

## Mini challenge

Open Source

Public hackathon branch:
https://github.com/jpadilla987-png/lead-rescue-agent/tree/amazon-alexa

## What it does

Lead Rescue Voice helps small service businesses recover inquiries that are at risk of going cold while preserving explicit authority boundaries.

The judgeable flow:
1. ranks leads by rescue urgency with transparent reasons;
2. lets the user inspect the evidence behind each priority;
3. prepares a safe next follow-up;
4. gives critical service needs a priority floor so they cannot be outranked by a larger but noncritical opportunity;
5. escalates price-match and other owner-only decisions instead of inventing discounts, availability, warranty exceptions, or unusual commitments;
6. exposes an MCP-style tool trace so the agent's actions can be reviewed.

Synthetic demo data keeps the run reproducible.

## Technical implementation

The Amazon-specific implementation on this branch uses a self-hosted Model Context Protocol server with Streamable HTTP.

MCP tools:
- `prioritize_leads`
- `inspect_lead`
- `prepare_follow_up`

MCP prompt:
- `morning_rescue_brief`

The real HTTP smoke test connects to `/mcp`, calls a tool, and checks that the negotiated MCP protocol revision is 2025-11-25 or later.

The project also includes:
- deterministic unit tests;
- adversarial tests;
- dependency auditing;
- Bandit;
- CodeQL;
- a reusable release gate.

A security review caught an unsafe default all-interface bind. The server now defaults to `127.0.0.1` and requires an explicit `HOST` value for public deployment.

## Safety / authority boundary

The system does not autonomously:
- send customer messages;
- invent appointment slots;
- grant discounts or price matches;
- make warranty exceptions;
- make unusual business commitments.

When authority belongs to the owner, the agent fails closed and escalates.

## Verified checkpoint

Verified:
- deterministic and adversarial suites pass;
- MCP server path implemented;
- HTTP protocol smoke path implemented;
- browser simulation implemented;
- security review passes after the bind fix;
- public open-source branch exists with license and source.

Do not claim:
- a public YouTube/Vimeo demo until one is actually uploaded and playable;
- final Devpost submission until `submitted_at` is non-null;
- customer production usage or paid-client results.

## Demo video plan — target 2:45 or less

**0:00–0:20 — Problem and promise**
Show the browser simulation and explain: busy field-service owners lose leads while working; Lead Rescue prioritizes the ones that need action without giving the agent pricing authority.

**0:20–0:55 — Rescue queue**
Run the morning brief. Show the ranked leads and the reasons each lead received its priority.

**0:55–1:25 — Urgent lead**
Open the critical-service example. Show the evidence and explain the priority-floor behavior.

**1:25–1:55 — Safety boundary**
Open the price-match example. Show that the system does not invent a discount and instead escalates the decision.

**1:55–2:25 — MCP implementation**
Show the MCP tool trace and briefly point to the self-hosted Streamable HTTP server and the three tools.

**2:25–2:45 — Close**
Explain that the same bounded pattern can support HVAC, roofing, electrical, landscaping, garage-door, and similar service businesses.

## Product feedback prompts to answer truthfully at submission

For each Amazon tool/API/SDK actually used:
- what it was used for;
- what worked well;
- what was difficult or missing;
- how onboarding felt;
- whether we would build with it again.

Only report direct experience. Do not invent ratings, usage, or integrations that were not actually run.

## Significant-update disclosure

The repository existed before this hackathon. The Amazon work is isolated on the `amazon-alexa` branch. That branch adds the Alexa+/MCP server, Streamable HTTP implementation, compatibility testing, browser simulation, adversarial/security testing, friction notes, demo plan, and submission tooling created during the hackathon window.

## Build credit

Entrant: Jose Padilla

AI engineering assistance: ChatGPT by OpenAI
