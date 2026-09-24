# Live Inference Gate

Status: **BLOCKED — credential not configured in repository CI**

A no-spend GitHub Actions check on 2026-09-24 confirmed:

```text
NEBIUS_API_KEY_PRESENT=false
```

No external API request was made and no inference credits were consumed.

## What this means

The deterministic application, adversarial tests, and security checks can continue normally, but the project must not claim a verified Nebius Token Factory / NVIDIA Nemotron runtime until a real key is configured and the dedicated live smoke test succeeds.

## Promotion rule

Do not change the release status to VERIFIED LIVE until:

1. `NEBIUS_API_KEY` is configured as a repository secret without exposing its value;
2. `python -m nebius_nighteye.live_smoke` executes against Nebius Token Factory;
3. the returned model identity is recorded;
4. the output passes the evidence-reference validator;
5. the successful run is attached to the proof record.

This file records the gate; it does not contain or request any secret value.
