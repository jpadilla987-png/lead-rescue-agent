# Frozen Phase-1 test protocol v0.1

Freeze date: 2026-10-04 PT, before Phase-1 submission opening.

A test case contains a query time, claims, evidence availability dates, validity intervals, supersession edges, and expected eligible/ineligible evidence.

Pass conditions:
- zero use of evidence after query time;
- zero assertion outside validity interval;
- superseded claims remain recoverable when historically valid;
- contradictory eligible evidence is retained;
- identical pinned inputs produce identical audit packets.

Negative controls:
- shuffle evidence availability dates;
- remove validity intervals;
- run static-KG baseline that ignores time;
- inject one future-dated evidence edge and require leakage detection.

No threshold may be changed after inspecting challenge benchmark outcomes. Any later change creates a new version and requires untouched validation.
