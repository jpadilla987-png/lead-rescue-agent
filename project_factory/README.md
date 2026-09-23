# Jose + AI Project Factory

This directory is the reusable internal layer for turning opportunities into finished, auditable projects instead of isolated one-off builds.

## Core ideas

1. **Opportunity scoring** — rank new competitions by prize, runway, AI-doability, friction, hardware dependence, code reuse, judging fit, and commercial value.
2. **Proof vault** — every important project claim should point to reproducible evidence.
3. **Judge panel** — review each release from multiple roles instead of relying on a single optimistic pass.
4. **AI-vs-AI loop** — Builder -> Tester -> Critic -> Fix -> Judge -> Retest.
5. **Money fork** — every competition project should identify a commercial reuse path.

## Release rule

A project is not "done" because code exists. A release candidate must have:
- working implementation;
- automated tests;
- adversarial tests;
- security review;
- proof-backed claims;
- rubric review;
- explicit unresolved risks;
- reproducible setup;
- demo evidence.

This folder is intentionally generic so the same process can be reused for Amazon, Nebius, FutureEval, NIGHTEYE, biomedical work, and later competition entries.
