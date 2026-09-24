# NIGHTEYE Benchmark

The benchmark gives the live Nemotron path a fixed evaluation set before final submission.

Cases cover:

1. clear multi-source operational change;
2. a single unverified rumor contradicted by a primary source;
3. prompt-injection text embedded inside evidence;
4. conflicting regional and aggregate evidence.

The benchmark is intentionally small and transparent. It does not pretend to prove broad model accuracy. It checks whether the live application preserves the evidence-first contract across representative failure modes.

When a real Nebius API key is configured, run:

```bash
python -m nebius_nighteye.live_benchmark
```

The report records the actual model/provider plus per-case structural checks. Final submission feedback should use that live report rather than invented ratings.
