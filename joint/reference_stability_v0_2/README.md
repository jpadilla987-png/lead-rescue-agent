# Reference Stability Certificate v0.2

Status: **FROZEN PROTOCOL / SCORER BUILT / OUTCOME NOT YET INGESTED**

This branch supersedes the v0.1 primary CMRG-label holdout design. v0.1 remains preserved as history and must not be rewritten.

v0.2 uses only pre-outcome structural/reference predictors and tests them against an out-of-time 2026 HG002 v5.0q cross-reference benchmarkability outcome.

Files:
- FROZEN_PROTOCOL.md — frozen design and validation gates.
- score.py — deterministic SIS-P2 scorer, outcome classifier, and leakage guard.
- self_test.py — zero-dependency checks.

Do not load v5.0q outcome fields into predictor construction. Do not call any high-scoring locus a discovery.
