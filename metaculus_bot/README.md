# Metaculus Fall 2026 — zero-cost bot lane

Status: **BUILT / NOT LIVE** until both required account secrets are present.

This branch is an isolated, zero-spend attempt for the Fall 2026 FutureEval Bot Tournament. It uses the official `forecasting-tools` package and OpenRouter's free-only router.

## Hard truth boundaries

- Fall 2026 tournament ID: `fall-futureeval-2026`
- Optional MiniBench ID: `minibench`
- Inference model route: `openrouter/free` via LiteLLM name `openrouter/openrouter/free`
- No paid model fallback is configured.
- The bot refuses to post unless **both** `METACULUS_TOKEN` and `OPENROUTER_API_KEY` exist **and** `ALLOW_METACULUS_POSTS=true`.
- A missing secret is a SAFE HOLD, not a failed forecast.
- Metaculus account activation / Terms acceptance and creation of access tokens remain user-only gates.
- Prize eligibility is never assumed; actual competition rules control.

## GitHub secrets needed

`METACULUS_TOKEN` — access token from the user's Metaculus bot account.

`OPENROUTER_API_KEY` — user's OpenRouter API key. The configured model route is free-only; no card/spend should be added for this project.

## Design

One research pass + three independent forecast samples per question. The same free model is used for research/reasoning/parsing to avoid paid-provider dependencies. `skip_previously_forecasted_questions=True` prevents redundant repeat work.

The GitHub Action checks every 30 minutes. With missing secrets it exits cleanly without posting. Once the two secrets exist, it forecasts the Fall seasonal tournament and current MiniBench.

## Current limitation

This scaffold has not posted a live forecast because the authenticated Metaculus token and OpenRouter key are not available to the connected tooling. Do not call it registered, live, prize-eligible, or earning money until actual Metaculus receipts exist.
