# NIGHTEYE Evidence Engine — Nebius x NVIDIA Hackathon

This branch contains the Nebius x NVIDIA Global AI Hackathon build of **NIGHTEYE Evidence Engine**.

The hackathon implementation lives in `nebius_nighteye/`. Older Lead Rescue files elsewhere in the repository predate this hackathon and are not part of the Nebius runtime.

## What NIGHTEYE does

NIGHTEYE turns a small packet of time-stamped evidence into an auditable change brief. It is designed to answer:

- What actually changed?
- Which statements are observations versus inference?
- What competing explanations still fit the evidence?
- What evidence would falsify the leading explanation?
- What is still unknown?
- What is the safest next reversible action?

The design goal is not to make an AI sound confident. The goal is to make its reasoning inspectable.

## Hackathon stack

- **Nebius Token Factory**
- **NVIDIA Nemotron 3 Super 120B A12B** by default
- Python 3.12
- FastAPI
- OpenAI-compatible Token Factory API
- Docker
- Deterministic validation and evidence-reference checks
- GitHub Actions CI + dependency/security review

Default model:

```text
nvidia/nemotron-3-super-120b-a12b
```

Default Token Factory endpoint:

```text
https://api.tokenfactory.us-central1.nebius.com/v1/
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r nebius_nighteye/requirements.txt
export NEBIUS_API_KEY=...
python -m uvicorn nebius_nighteye.app:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000`.

The API key stays server-side and is never exposed to the browser.

## Run the deterministic test suite

```bash
python -m unittest discover -s nebius_nighteye/tests -v
```

CI also runs compile checks, dependency auditing, Bandit static analysis, and CodeQL.

## Live Token Factory proof

The repository includes a dedicated live smoke test:

```bash
python -m nebius_nighteye.live_smoke
```

That smoke test is intentionally separate from deterministic CI because it requires a real `NEBIUS_API_KEY` and consumes live inference credits. It must pass before the project is described as having verified live Nebius/Nemotron inference.

## Evidence-first contract

Model output is validated before it is accepted. Evidence citations must reference IDs that were actually supplied in the request. Unsupported evidence IDs fail validation instead of being silently accepted.

The output schema preserves:

- material-change judgment;
- observations;
- competing explanations;
- falsifier;
- unknowns;
- next actions;
- evidence references.

## Track

Primary fit: **Best Apps and Agents**.

NIGHTEYE is being built as an app someone can actually use, with Nemotron providing the reasoning step and the surrounding application enforcing evidence structure and auditability.

## Significant-update disclosure

This repository existed before the Nebius hackathon. The `nebius-nighteye` branch and `nebius_nighteye/` application are the hackathon-specific implementation added during the submission period. Pre-existing Lead Rescue code is not represented as new Nebius work.

## Current verified state

Verified now:

- deterministic evidence-processing tests pass;
- browser/API application is implemented;
- Docker packaging is present;
- security workflow passes;
- Token Factory client code targets NVIDIA Nemotron through Nebius.

Still required before final submission:

- a successful live Token Factory/Nemotron inference run;
- a public hosted demo;
- a public YouTube demo video under three minutes;
- factual ratings/feedback based on real Nebius/Nemotron usage;
- required submitter attestations.

## License

MIT

## Build credit

Entrant: Jose Padilla  
AI engineering assistance: ChatGPT by OpenAI
