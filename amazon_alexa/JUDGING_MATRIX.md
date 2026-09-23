# Amazon Judging Matrix — Lead Rescue Voice

Official judging criteria checked on 2026-09-23.

## Tech Implementation

Evidence:
- self-hosted MCP server using the current MCP Python SDK;
- real Streamable HTTP smoke test;
- negotiated MCP protocol assertion >= 2025-11-25;
- tools for lead prioritization, inspection, and guarded follow-up;
- adversarial tests, dependency audit, Bandit, and CodeQL;
- security finding on default network binding was fixed and retested.

Remaining risk:
- final public video must show the implementation clearly enough that judges can distinguish the real MCP path from the browser simulation.

## Design

Evidence:
- browser simulation presents a morning rescue queue, urgent lead handling, price-match escalation, and an MCP-style trace;
- owner-only pricing decisions are surfaced explicitly;
- synthetic data keeps the demo reproducible.

Remaining risk:
- no public hosted judge link yet; video therefore carries more of the UX burden.

## Potential Impact

Target user:
- field-service businesses such as HVAC, roofing, electrical, landscaping, and similar owner-operated services.

Specific problem:
- valuable inquiries decay while the owner is driving, working on-site, or handling another customer.

Product boundary:
- prioritize and prepare safe follow-up automatically;
- keep discounts, unusual commitments, and unsupported availability under owner control.

Commercial fork:
- package the same bounded rescue workflow as a subscription product for service businesses after the hackathon.

## Quality of the Idea

Differentiator:
- the project is not just “AI follow-up.” It combines transparent rescue scoring with an explicit authority boundary so the agent can act on routine work but fails closed on owner-only decisions.

## Release blockers

- public English YouTube/Vimeo video under 3 minutes;
- submitter country;
- Canada province or N/A;
- age-of-majority attestation;
- eligible-jurisdiction attestation;
- promotion-entity employee/representative/agent attestation.
