# Capability Trial 002 — Contract Guard

This experiment started from a Sable finding: some n8n runs can look healthy forever while returning a plausible-but-wrong result.

Independent verification changed the scope:

- **Stable zero-output is already covered by Ran Fine** when output monitoring is enabled, even without a healthy history baseline.
- **Static wrong-since-birth workflow defects already have dedicated checks** in Ran Fine.
- **Static known values can already be asserted** with `expect_present` / `expect_within_days`.

The surviving gap is narrower: a **dynamic relational invariant** inside the current execution, such as:

```
requested.id == result.id
input.customer.id == output.customer.id
```

A history/shape monitor can miss this forever if the wrong output is stable and plausible. A static blessed-value list cannot express it when the expected value changes every run.

## Prototype

`semantic_guard.py` implements user-declared field-equality contracts. It does not infer meaning.

It returns:
- `contract_mismatch` when both fields exist but differ.
- `contract_unverifiable` when a required field is missing.
- nothing when the explicit contract holds.

## Evidence discipline

This is **not** a replacement for Ran Fine and not a claim of general semantic monitoring.

It is a minimal test of one specific surviving blind spot: dynamic per-run invariants.

## Run

```bash
cd joint/capability_trial_002
python -m unittest -v test_semantic_guard.py
```

Current local validation before publishing: **6/6 tests passed**.
