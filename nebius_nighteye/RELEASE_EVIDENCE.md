# Release Evidence — NIGHTEYE Evidence Engine

Verified 2026-09-24.

## Current branch

Branch: `nebius-nighteye`

Latest benchmark release evidence:

- Nebius NIGHTEYE CI — **PASS** — run 35993484509
- Nebius NIGHTEYE Security — **PASS** — run 35993484506

Live-credential gate:

- Secret presence workflow latest clean gate — run 35993050074
- Observed result: `NEBIUS_API_KEY_PRESENT=false`
- No external inference request was made and no credits were consumed.

## Verified claims

- Evidence-first application is implemented.
- Prompt-injection text in evidence is treated as untrusted data.
- Unsupported evidence IDs in observations and competing explanations are rejected.
- Malformed JSON, invalid material-change types, and duplicate explanations are rejected.
- FastAPI browser/API application exists.
- Docker packaging exists.
- Fixed four-case benchmark exists for live Nemotron evaluation.
- Deterministic/adversarial CI and security scans pass.

## Not yet verified / release gates

- Live Nebius Token Factory inference.
- Actual NVIDIA Nemotron runtime model identity.
- Live benchmark results.
- Public hosted application.
- Public YouTube demo.
- Live-use quality and experience ratings.
- Required submitter attestations.
