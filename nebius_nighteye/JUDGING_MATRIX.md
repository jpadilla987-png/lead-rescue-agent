# Nebius Judging Matrix — NIGHTEYE Evidence Engine

Official judging criteria checked on 2026-09-23.

## Technological Implementation

Evidence:
- FastAPI application;
- Nebius Token Factory OpenAI-compatible client;
- NVIDIA Nemotron 3 Super 120B A12B configured as the default model;
- structured evidence contract;
- rejection of unsupported evidence IDs in observations and explanations;
- prompt-injection defensive instruction treating evidence as untrusted data;
- deterministic/adversarial CI;
- dependency audit, Bandit, and CodeQL.

Current blocker:
- a live Token Factory/Nemotron inference run is still required before claiming verified runtime use.

## Design

Evidence:
- browser UI lets a user submit a topic plus timestamped evidence and inspect an auditable brief;
- output keeps material-change judgment, observations, competing explanations, falsifier, unknowns, and next actions separate;
- API key remains server-side.

Remaining risk:
- no public hosted application yet.

## Potential Impact

Target users:
- operators, analysts, founders, researchers, and teams that need to know whether new information materially changes a decision.

Specific problem:
- ordinary AI summaries compress evidence and inference together, making unsupported confidence hard to detect.

Product value:
- NIGHTEYE makes uncertainty and falsification visible instead of hiding them.

## Quality of the Idea

Differentiator:
- Nemotron is not used only to summarize. The surrounding application forces evidence IDs, competing explanations, falsifiers, explicit unknowns, and reversible next actions, then validates the model output before accepting it.

## Release blockers

- successful live Nebius Token Factory + NVIDIA Nemotron inference;
- hosted working demo URL;
- public YouTube video <= 3 minutes showing the real runtime;
- feedback and ratings based on actual live use;
- submitter country / Canada N/A;
- age-of-majority attestation;
- promotion-entity employee/representative/agent attestation.
