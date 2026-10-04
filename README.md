# TasteBridge — Qloo Agentic Hackathon

TasteBridge turns one public cultural anchor into explainable cross-domain recommendations using Qloo's taste graph.

This branch is the Qloo-specific hackathon build. The repository existed before the event; the TasteBridge application and Qloo integration were added during the submission period.

## Why Qloo is essential

A generic language model can invent a plausible “if you like X, try Y” list. TasteBridge instead uses Qloo twice:

1. Qloo search resolves the entered public cultural anchor into real Qloo entities.
2. The user chooses the intended entity.
3. Qloo Insights uses that Qloo entity ID to retrieve recommendations in another cultural domain.
4. TasteBridge preserves Qloo provenance and presents limitations separately.

Remove Qloo and the core recommendation flow stops.

## Technical implementation

- Node.js 22.19+
- official @qloo/qloo-harness pinned to 0.1.26
- server-side Qloo search
- server-side Qloo Insights
- event endpoint locked to https://hackathon.api.qloo.com
- explicit public-entity disambiguation
- fail-closed credential handling
- browser UI plus HTTP API
- automated tests

Source lives under qloo_taste_bridge.

## Responsible use

TasteBridge rejects obvious personal/contact-like input and keeps credentials server-side. Aggregate cultural affinity is not represented as an individual prediction, causal claim, or evidence for a high-impact decision.

## Verification state

Verified in code/tests:
- two-stage Qloo search to Insights architecture;
- cross-domain target allowlist;
- browser/API routing;
- credential non-disclosure;
- fail-closed behavior.

Not yet claimed:
- live Qloo request;
- live Qloo recommendation quality;
- public end-to-end deployment;
- Devpost registration/submission.

Those require the event credential and user-controlled Devpost agreements.

## License

MIT

Entrant: Jose Padilla
AI engineering assistance: ChatGPT by OpenAI
