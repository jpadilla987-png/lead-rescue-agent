# TasteBridge — Qloo Agentic Hackathon work branch

Status: BUILD STARTED / NOT REGISTERED / LIVE QLOO CREDENTIAL NOT YET ISSUED.

TasteBridge is an evidence-first cultural context agent. It takes an explicitly provided public cultural anchor such as a brand, artist, film, venue, or category, resolves it through Qloo, and returns a structured evidence packet that a downstream agent can use without pretending to know anything about an individual person.

## Why this fits Qloo

The product is designed around aggregate cultural affinity rather than generic LLM guessing. The first live integration uses Qloo's supported CLI/API harness. Future steps will add recommendation / shortlist ranking workflows once the event credential is available.

## Safety boundary

- No names, emails, device IDs, account IDs, or private location history go to Qloo.
- No sensitive-trait inference.
- No employment, credit, insurance, housing, health, or political decisions.
- Qloo results are evidence, not causal claims or individual predictions.
- The API credential stays server-side and out of source control.

## Current implementation

`app.mjs` shells out to the official `qloo api search --json` path exposed by `@qloo/qloo-harness`.
It validates input, invokes Qloo, normalizes the result, and fails closed if Qloo cannot be reached.

## Run

1. Install Node.js 22.19+.
2. Install the official harness:
   `npm install --global @qloo/qloo-harness`
3. Obtain an event-issued credential and run `qloo setup --qloo`.
4. Run:
   `node qloo_taste_bridge/app.mjs "Agatha Christie"`

No credential should ever be pasted into a repo, chat, browser app, demo, or committed environment file.

## Next gates

1. Devpost registration requires user agreement to Qloo rules, Devpost terms, eligibility, team preference, and two registration answers.
2. Event-issued Qloo credential is required for a live call.
3. After live access, add one cross-domain recommendation workflow and a reproducible public demo.
