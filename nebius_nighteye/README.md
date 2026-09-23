# NIGHTEYE Evidence Engine — Nebius x NVIDIA build

An evidence-first agent that detects material change, separates observation from inference, generates competing explanations, names a falsifier, preserves explicit unknowns, and recommends reversible next actions.

## Required hackathon technology

The live path is designed for **Nebius Token Factory** through its OpenAI-compatible API and defaults to the NVIDIA open-source model:

`nvidia/nemotron-3-super-120b-a12b`

Configuration is environment-only:

```bash
export NEBIUS_API_KEY=...
export NEBIUS_BASE_URL=https://api.tokenfactory.us-central1.nebius.com/v1/
export NEBIUS_MODEL=nvidia/nemotron-3-super-120b-a12b
```

Never commit the API key.

## Run locally

```bash
python -m pip install -r nebius_nighteye/requirements.txt
python -m nebius_nighteye.demo
```

Or start the API:

```bash
uvicorn nebius_nighteye.app:app --host 127.0.0.1 --port 8080
```

Then POST to `/analyze` with a topic and evidence list.

## Evidence discipline

- The model receives only evidence supplied in the request.
- Every observation must cite one or more allowed evidence IDs.
- Unknown or invented evidence IDs are rejected.
- At least two competing explanations are required.
- The response must include a falsifier and explicit unknowns.
- The default temperature is 0.1 to reduce avoidable variation.
- Real performance/quality claims are withheld until a live Nebius/NVIDIA run is completed.

## Testing

```bash
python -m unittest discover -s nebius_nighteye/tests -v
```

Normal CI uses a fake backend so tests are deterministic and never spend API credits. The separate live-smoke workflow is manual and requires a repository secret named `NEBIUS_API_KEY`.

## Build credit

Entrant: Jose Padilla  
AI engineering assistance: ChatGPT by OpenAI

## Release status

Deterministic CI must pass before a live Token Factory smoke test is attempted. Live inference remains blocked until a Nebius API key is configured outside chat.
