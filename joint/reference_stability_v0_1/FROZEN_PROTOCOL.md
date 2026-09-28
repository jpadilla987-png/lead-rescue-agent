# NIGHTEYE Reference Stability Certificate v0.1 — FROZEN PROTOCOL

Frozen: 2026-09-27 PT
Branch: reference-stability-v0-1
Scope: public benchmark/reference data only. No personal genomics. No clinical diagnosis or risk inference.

## Objective
Test whether an a-priori locus-structure score predicts known benchmark instability in difficult medically relevant genes. Only after this holdout test may the system scan for previously under-highlighted high-risk loci.

## Integrity rule
The predictive score and split rule are frozen before ingesting the full CMRG included/excluded gene labels into this branch. No coefficient, threshold, or split may be changed after holdout labels are loaded. A failed holdout is retained as a negative result.

## Deterministic split
For each eligible gene symbol, compute SHA256("NIGHTEYE-RSC-v0.1-2026-09-27|" + uppercase_gene_symbol).
Holdout = first unsigned byte < 64 (~25%).
Development = all others.
The holdout membership is therefore deterministic and cannot be hand-picked.

## Primary predictor: Structural Instability Score (SIS-P), 0–7
Only structural/reference-context features may enter the prospective predictor.

1. Segmental duplication burden, 0–2
   - 0: no overlap in the gene + 20 kb flanks.
   - 1: >0% and <20% overlap on either evaluated reference.
   - 2: >=20% overlap on either evaluated reference.

2. Low-mappability / near-identical paralog burden, 0–2
   - 0: no qualifying low-mappability/paralog evidence.
   - 1: >0% and <20% low-mappability overlap OR a documented homolog that does not meet the high-complexity criterion below.
   - 2: >=20% low-mappability overlap OR a documented >=95%-identity paralog/pseudogene that materially complicates unique mapping.

3. Copy-number / collapsed-duplication complexity, 0–2
   - 0: no public evidence of copy-number/reference-collapse complexity.
   - 1: structural variability is documented but there is no confirmed reference/haplotype copy-count mismatch.
   - 2: public assembly/benchmark evidence shows a false duplication, collapsed sequence, copy-count mismatch, or locus-level duplication/deletion that changes one-to-one representation.

4. Cross-reference representation discordance, 0–1
   - 0: one-to-one representation is supported across GRCh38 and the evaluated T2T/pangenome context.
   - 1: a gap, false duplication, structural error, broken/lossy lift, or non-one-to-one representation is documented.

SIS-P = sum of components. High-risk threshold is frozen at SIS-P >= 5.

## Holdout outcome
Primary binary outcome: known benchmark instability on the official CMRG challenge set, defined as exclusion/unresolved status under the CMRG benchmark construction or an explicitly documented reference-specific failure that prevents stable one-to-one benchmarking.

The outcome label is NOT a component of SIS-P.

## Primary validation metrics
- ROC AUC for SIS-P against the binary holdout outcome.
- Odds ratio for high-risk (SIS-P >= 5) versus lower-risk genes.
- Sensitivity and specificity at the frozen threshold.

PASS requires BOTH:
- AUC >= 0.70, and
- high-risk odds ratio > 2.0.

If either condition fails, v0.1 is KILLED/REVISE; no novel-locus scan is allowed from this score.

## Secondary certificate fields — not part of the predictive holdout score
After the primary holdout is locked and scored, a final per-locus certificate may append:
- benchmark inclusion/exclusion status,
- cross-technology discordance,
- variant-calling performance,
- exact assembly/reference release,
- provenance links,
- orthogonal long-read/assembly confirmation status.

These fields may change the final label STABLE / REFERENCE-SENSITIVE / UNRESOLVED, but they may not retroactively alter SIS-P or the v0.1 holdout result.

## Novelty gate
A high SIS-P gene is NOT a discovery.
A candidate may be promoted only if:
1. it scores high under this frozen protocol,
2. it was not already highlighted in benchmark/pangenome literature for the same failure,
3. the instability reproduces on an independent public dataset or orthogonal long-read/assembly evidence,
4. the finding survives a targeted prior-art search.

## Data provenance targets
- NIST Genome in a Bottle HG002 v5.0q and stratifications.
- GIAB CMRG benchmark and manuscript supplementary data.
- T2T-CHM13 / T2T-HG002 release-specific annotations.
- HPRC/pangenome public resources.
- Independent long-read/assembly benchmark studies where needed.

## Explicit non-claims
This protocol does not diagnose disease, estimate personal risk, establish pathogenicity, or imply that T2T/pangenome references are universally superior. It tests reference stability and benchmarkability only.
