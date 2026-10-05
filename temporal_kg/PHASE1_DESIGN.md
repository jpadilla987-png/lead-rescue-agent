# TimeGuard KG — Phase 1 frozen design v0.1

Status: PRE-REGISTRATION BUILD. This is an engineering artifact, not a claim of NIH registration or submission.

## Core idea

TimeGuard KG treats **query time** as a first-class constraint. Every biomedical claim is coupled to provenance, evidence availability time, and a validity interval. Historical reasoning is reconstructed using only evidence that was available at the requested time. Later evidence can revise today's graph but is forbidden from leaking backward into an earlier decision reconstruction.

## Frozen invariants

1. **No-future-information leakage:** evidence with `availableAt > queryTime` cannot support an inference evaluated at `queryTime`.
2. **Validity containment:** a claim may be asserted at query time only if the query time lies inside its validity interval.
3. **Supersession is temporal, not deletion:** superseded guidance remains addressable for historical reconstruction.
4. **Contradiction is preserved:** conflicting claims are represented with provenance and time rather than silently collapsed.
5. **Unknown is explicit:** absence of valid evidence yields UNRESOLVED, not a fabricated answer.
6. **Auditability:** every inference packet must expose supporting evidence IDs, versions, availability dates, validity interval, and query cutoff.

These rules are frozen before challenge evaluation data or Phase-2 benchmark data exist. They must not be retuned after outcomes.

## Biomedical use case

Primary Phase-1 use case: **time-correct clinical-guideline and evidence retrieval**. A clinician/researcher asks what evidence/guidance was valid at a historical date or what is valid now. Static KGs can merge superseded guidance with later evidence. TimeGuard produces a query-time-safe evidence packet and flags temporal leakage.

This is a research/information architecture, not a medical decision maker.

## Representation

The ontology excerpt uses OWL/RDF concepts plus OWL-Time and PROV-O-compatible provenance. Planned integration maps biomedical entities/relations to Biolink Model categories/predicates and established NLM/OBO identifiers rather than inventing replacements.

Core objects:
- Claim / Guideline
- Evidence
- ValidityInterval
- EvidenceState: SUPPORTED / CONTRADICTED / UNRESOLVED
- DecisionContext with queryTime
- supersedes relation
- TemporalLeakageViolation audit result

## Reasoning procedure

For query time tq:
1. Retrieve candidate claims relevant to the biomedical entity/relation.
2. Filter supporting evidence to `availableAt <= tq`.
3. Filter claims to validity intervals containing tq.
4. Preserve contradictory eligible claims rather than selecting by recency alone.
5. Apply logical/temporal constraints.
6. Return the inference plus provenance packet.
7. Run an independent leakage audit: any dependency dated after tq invalidates the historical inference.

## Evaluation plan

Head-to-head baseline: identical graph content with time metadata ignored.

Frozen primary correctness metrics:
- temporal-leakage violations per query;
- invalid-interval assertions per query;
- correct historical-guideline reconstruction rate;
- contradiction-preservation rate;
- provenance completeness.

Secondary KG metrics will include the Phase-2 metrics NIH specifies: logical inconsistencies/unsatisfiable classes, triple count, relationship richness, attribute richness, class/property instantiation ratio, and interlinking completeness.

## Falsifiers

TimeGuard fails its central claim if, on untouched evaluation cases:
- it permits future evidence into historical inference;
- it increases temporal/logical errors versus the static baseline without a compensating predefined benefit;
- its rules cannot be represented/interchanged with established ontology infrastructure;
- or independent reproduction cannot recover the same inference packets from pinned inputs.

## Phase-1 scoring alignment

- Temporal Modeling Innovation (25%): validity + evidence-availability + supersession + evolving evidence.
- Reasoning Correctness (25%): explicit query-time firewall and leakage audit.
- Ontology Rigor (20%): machine-readable OWL/RDF excerpt with logical properties; standards integration plan.
- Feasibility (15%): implementable filtering/reasoning/audit pipeline over existing KGs.
- Workflow Impact (15%): prevents historically impossible evidence/guideline retrieval.

## Human gate

NIH registration requires the participant to accept the Official Rules, Terms and Conditions, and Participation Agreement. No Family agent should claim registration or submission until Jose completes that protected acceptance step.
