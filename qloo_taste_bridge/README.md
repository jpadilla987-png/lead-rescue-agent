# TasteBridge

Status: cross-domain Qloo workflow implemented and CI-tested; live Qloo event credential and external deployment still required.

TasteBridge is a privacy-first cultural bridge built around Qloo. A user supplies one public cultural anchor — a book, film, artist, place, brand, destination, or other public cultural concept. TasteBridge resolves that seed through Qloo, then uses the resolved Qloo entity as the interest signal for multiple Qloo Insights calls across other cultural domains.

The product is intentionally Qloo-dependent: if Qloo cannot resolve the seed or return usable affinities, TasteBridge fails closed instead of inventing generic LLM recommendations.

## Why Qloo is essential

The core flow is:

1. Resolve a public cultural seed with Qloo search.
2. Use the resolved Qloo entity ID as `signal.interests.entities`.
3. Fan out to Qloo `/v2/insights` across selected domains.
4. Return a compact provenance packet with affinity values where supplied by Qloo.
5. Isolate partial domain failures instead of fabricating fallbacks.

Current domains: music, places, brands, travel/destinations, books, movies, TV, games, and taste tags at the API layer. The public demo exposes a focused six-domain set.

## Implementation

- Node.js 22.19+
- Qloo event API: `https://hackathon.api.qloo.com`
- Qloo search: `/search`
- Qloo insights: `/v2/insights`
- Event harness pinned: `@qloo/qloo-harness 0.1.26`
- Server-side credential only: `QLOO_API_KEY`
- CI: GitHub Actions on the `qloo-taste-bridge` branch

Important files:

- `app.mjs` — original event-harness search + single-domain insight adapter
- `qloo_api.mjs` — direct Qloo search/insights client
- `bridge.mjs` — multi-domain Qloo orchestration
- `web.mjs` — public demo server and API routes
- `test.mjs`, `bridge.test.mjs`, `web.test.mjs` — validation and workflow tests

## Run

From `qloo_taste_bridge`:

```bash
npm install
export QLOO_API_KEY="event-issued-key"
npm start
```

Open `http://localhost:3000`.

## Test

```bash
npm test
```

Tests cover input validation, contact-data rejection, Qloo request construction, seed resolution, multi-domain fan-out, partial-domain failure isolation, provenance, web routes, fail-closed behavior, and credential non-disclosure.

## Safety boundary

- Public cultural concepts only.
- No email addresses, account/device identifiers, or private location history.
- No sensitive-trait inference.
- No employment, credit, insurance, housing, health, or political decisions.
- Qloo affinities are aggregate cultural relationships, not probabilities about an individual.
- No synthetic recommendation fallback if Qloo is unavailable.

## Remaining release gates

1. Complete the organizer/API-key access step and receive a legitimate event-issued Qloo credential.
2. Run and preserve a real seed-to-multi-domain Qloo trace.
3. Deploy externally with `QLOO_API_KEY` stored in the host secret manager.
4. Verify the public demo end-to-end.
5. Complete Devpost registration only after Jose explicitly accepts the official rules/eligibility terms.
6. Submit the live demo URL, public repository, and final text description before October 30, 2026 at 11:45 PM ET.
