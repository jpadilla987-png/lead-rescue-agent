# Lead Rescue — Devpost Submission Notes

## One-line pitch

Lead Rescue is an autonomous Strands agent that clears routine small-business lead follow-up and interrupts the owner only when a real business decision is required.

## Inspiration

Local service-business owners often lose good leads while they are driving, working on-site, quoting jobs, or juggling calls. Traditional CRM software can create another queue to babysit. Lead Rescue flips that model: the agent does the routine work and surfaces only decisions that require human judgment.

## What it does

Lead Rescue loads business policies, reads new leads, checks real calendar availability, replies to routine customer inquiries, schedules follow-ups, and escalates discounts or price negotiations to the owner. The included demo processes an urgent cooling failure, a price-match request, and a routine tune-up request in one autonomous batch.

## How it was built

- Strands Agents SDK
- Amazon Bedrock
- Python custom tools using the Strands `@tool` decorator
- Human-in-the-loop guardrails for owner-only decisions

## Demo video outline — under 5 minutes

**0:00-0:35 — Problem**
Explain that a busy service-business owner loses leads because they cannot answer every inquiry quickly.

**0:35-1:05 — Architecture**
Show the README Mermaid diagram and explain that Strands chooses between business context, calendar, reply, follow-up, and owner-escalation tools while Amazon Bedrock provides reasoning.

**1:05-3:20 — Live run**
Run `python lead_rescue.py`. Show all three leads being processed. Highlight that normal work is completed automatically but the price-match request is stopped and surfaced as an owner decision.

**3:20-4:10 — Safety**
Show the prompt/tool boundary that forbids invented appointment slots, discounts, unsupported promises, and owner-only commitments.

**4:10-4:45 — Commercial value**
Explain that the same engine can be adapted to HVAC, roofers, electricians, landscapers, garage-door companies, and similar local businesses.

## Disclosure

Newly built during the 2026 hackathon period. AI coding assistance was used. No pre-existing application code was incorporated.
