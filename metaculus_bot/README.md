# Metaculus Fall 2026 — zero-cost bot lane

Status: **SMOKE-VERIFIED / MANUAL-ONLY / PRIZE ELIGIBILITY UNVERIFIED**.

## Verified now

- The Metaculus bot token/account path has successfully posted one test forecast plus one comment.
- The inference path uses OpenRouter's free-only router.
- A later free-provider run hit an upstream shared-pool HTTP 429; that was not a Metaculus authentication failure.
- No paid model fallback is configured.
- Scheduled posting is intentionally disabled.

## Hard truth boundaries

- Fall 2026 tournament ID: `fall-futureeval-2026`
- Optional MiniBench ID: `minibench`
- Inference model route: `openrouter/free` via LiteLLM name `openrouter/openrouter/free`
- Publishing requires **all three**:
  - `METACULUS_TOKEN`
  - `OPENROUTER_API_KEY`
  - `ALLOW_METACULUS_POSTS=true`
- GitHub Actions is **manual-only**. The dispatch form defaults `allow_posts` to false.
- Prize eligibility is not assumed. The Fall 2026 participant form remains a separate eligibility requirement to verify.
- Commercial bots are not prize eligible under the current FutureEval policy; hobbyist/open-source bots are the relevant lane.
- Prize pools are not cash until an award/payment is verified.

## Run policy

A manual GitHub Actions run must deliberately set `allow_posts=true` to post. Leaving the default false causes a SAFE HOLD.

The workflow runs a policy guard before the bot. This exists specifically to prevent a future edit from silently restoring automatic schedules or hard-coding publishing on.

## Current limitation

The free inference pool can rate-limit or fail upstream. That is acceptable: the project must fail closed rather than fall back to paid inference.

Do not merge or enable recurring forecasting until participant/prize eligibility is verified and the posting cadence is deliberately approved.
