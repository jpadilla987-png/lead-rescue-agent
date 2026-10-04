# NIGHTEYE Reference Stability Certificate v0.2 — FROZEN TEMPORAL PROTOCOL

Frozen: 2026-10-03 PT
Branch: reference-stability-v0-2
Scope: public benchmark/reference data only. No personal genomics. No diagnosis, pathogenicity, or personal-risk inference.

## Why v0.2 exists
RSC v0.1 used historical CMRG inclusion/exclusion as the primary outcome. That design is superseded because CMRG exclusion reasons overlap the same structural properties the score is intended to predict, creating leakage/circularity risk.

v0.2 changes the target to an out-of-time 2026 benchmark outcome and forbids outcome-like predictors.

## Primary question
Can pre-outcome structural/reference context predict which medically relevant genes show materially different benchmarkable coverage across references in the 2026 HG002 v5.0q benchmark?

## Predictor cutoff
All predictor evidence must be frozen from sources available before the v5.0q outcome release being scored. Predictor construction may use historical structural/reference annotations, but MUST NOT use:
- v5.0q benchmark-region coverage,
- v5.0q truth-set inclusion/exclusion,
- v5.0q manual curation,
- CMRG included/excluded labels as predictors,
- later benchmark success/failure labels,
- any field derived from the target being scored.

Exact source/version provenance is mandatory for every predictor row.

## Fixed score: SIS-P2, 0–7
The score is intentionally simple and fixed before outcome ingestion.

1. Segmental-duplication burden, 0–2
   - 0: no overlap in gene body + 20 kb flanks.
   - 1: >0% and <20% overlap.
   - 2: >=20% overlap.

2. Low-mappability / near-identical paralog burden, 0–2
   - 0: no qualifying evidence.
   - 1: >0% and <20% low-mappability overlap OR documented homolog without the high-complexity condition.
   - 2: >=20% low-mappability overlap OR documented >=95%-identity paralog/pseudogene that materially complicates unique mapping.

3. Copy-number / collapsed-duplication complexity, 0–2
   - 0: no pre-outcome evidence.
   - 1: structural variability documented without confirmed reference/haplotype copy-count mismatch.
   - 2: pre-outcome evidence of false duplication, collapsed sequence, copy-count mismatch, or locus-level duplication/deletion that changes one-to-one representation.

4. Cross-reference representation discordance, 0–1
   - 0: one-to-one representation supported across GRCh38 and T2T-CHM13v2.0 context.
   - 1: pre-outcome evidence of a gap, false duplication, structural error, lossy lift, or non-one-to-one representation.

SIS-P2 = sum of components.
Frozen high-risk threshold: SIS-P2 >= 5.

## Cohort
Primary cohort: challenging medically relevant autosomal genes from the GIAB CMRG source universe for which a defensible coordinate representation can be established on both GRCh38 and T2T-CHM13v2.0.

Genes without defensible one-to-one/explicitly represented coordinates on both references are not silently dropped. They are recorded as UNRESOLVED for the certificate and excluded from the primary AUC denominator with the reason preserved.

## 2026 temporal outcome
Use HG002 v5.0q benchmark regions on GRCh38 and T2T-CHM13v2.0.

Compute, separately for small-variant and structural-variant benchmark regions:

coverage_ref = benchmark-region bases overlapping the gene body / evaluable gene-body bases on that reference.

Primary binary outcome, REFERENCE-SENSITIVE:
absolute(coverage_GRCh38 - coverage_T2T_CHM13v2) >= 0.10.

Secondary severe outcome:
absolute coverage difference >= 0.25.

Do not combine small-variant and SV outcomes into one primary label. Score them separately.

Gene +20 kb context may be reported as a secondary analysis only; the primary outcome uses gene body to avoid arbitrary flank-driven label changes.

## Frozen validation gates
For each outcome class separately:
- ROC AUC for SIS-P2.
- Odds ratio for high-risk (SIS-P2 >= 5) versus lower-risk genes.
- Sensitivity and specificity at SIS-P2 >= 5.

PASS requires BOTH:
- AUC >= 0.70, and
- high-risk odds ratio > 2.0.

If either gate fails, v0.2 fails for that outcome class. Preserve the negative result; do not retune thresholds from the scored outcome.

A pass does NOT establish novelty. It establishes only practical predictive usefulness for reference-sensitivity screening.

## Missingness / anti-cherry-picking
- Predeclare every eligible gene before outcome scoring.
- Never remove a gene because it hurts performance.
- Missing predictor data -> score the known components and mark predictor completeness.
- Missing outcome coordinates/benchmarkability -> UNRESOLVED, with reason.
- Report counts for eligible, scored, unresolved, and excluded-by-protocol genes.

## Leakage guard
Any feature table supplied to the scorer must reject outcome-like columns, including names containing:
cmrg_included, cmrg_excluded, benchmark_status, benchmark_included, benchmark_excluded, v5q_coverage, v5_coverage, manual_curation, truth_label, outcome, target, false_positive, false_negative, precision, recall, f1.

The deny-list is a floor, not permission to encode the same information under another name.

## Orthogonal validation
A high-scoring/reference-sensitive locus may only advance after:
1. targeted prior-art search for the same reference-specific failure,
2. independent long-read/assembly or pangenome evidence,
3. exact reference/assembly release provenance,
4. confirmation that the apparent instability is not merely a coordinate/liftover artifact.

## Certificate output
Only:
- STABLE
- REFERENCE-SENSITIVE
- UNRESOLVED

The certificate is a provenance/benchmarkability tool. It is not a clinical interpretation.

## Release/version note
NIST states HG002 v5.0q is based on T2T-HG002 v1.1 and provides benchmarks on GRCh37, GRCh38, and T2T-CHM13v2.0. HG002 v1.2 was released later (Aug 2026) with 612 patched problematic regions. Therefore v1.2 evidence is post-target orthogonal evidence, not a predictor for this frozen v0.2 primary test.

## Explicit non-claims
- No discovery claim from a high SIS-P2 score.
- No claim that T2T is universally superior.
- No personal genetic inference.
- No disease diagnosis or pathogenicity classification.
