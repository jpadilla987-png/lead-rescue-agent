# TasteBridge — Qloo Agentic Hackathon submission draft

## One-line pitch

TasteBridge turns one public cultural anchor into a cross-domain recommendation map grounded in Qloo's taste graph, without requiring personal data.

## What it does

A user enters a public cultural anchor such as Agatha Christie, Bauhaus, Brian Eno, a restaurant, a brand, or a destination. TasteBridge resolves that input to a real Qloo entity and uses the resulting entity ID as a taste signal. It then fans out across multiple Qloo Insights domains — for example music, movies, books, places, brands, and travel — and returns an evidence packet showing the recommendations and Qloo provenance.

If Qloo cannot resolve the seed or produce usable insight results, TasteBridge fails closed. It does not replace missing Qloo data with generic LLM guesses.

## Why this is Qloo-powered

TasteBridge's useful output is created by Qloo's cross-domain affinity graph. The application does not simply ask an LLM to invent related recommendations. Qloo resolves the seed and supplies the cross-category affinity results. Without Qloo, the core recommendation packet does not exist.

## Problem

General-purpose assistants are good at producing plausible recommendation prose but often have no grounded model of how taste transfers across cultural categories. TasteBridge is designed for people and downstream agents that need a compact, inspectable cultural context layer without collecting identity-level personal data.

## Technical implementation

- Qloo /search resolves the cultural seed.
- The chosen Qloo entity becomes signal.interests.entities.
- Qloo /v2/insights is called across selected entity types.
- Domain calls fan out independently so one weak category does not erase the rest of the result.
- Qloo affinity values are retained when available.
- Results include explicit provenance and limitations.
- Credentials remain server-side.
- Public inputs are validated and obvious contact/private identifiers are rejected.

## Safety and privacy

TasteBridge uses public cultural concepts rather than personal identifiers. It does not infer sensitive traits and is not intended for employment, credit, insurance, housing, medical, or political decision-making.

## Current verification

The cross-domain workflow, web API route, fail-closed behavior, and credential handling are covered by automated tests in GitHub Actions.

## Remaining before submission

A legitimate event-issued Qloo API key is still required for the first preserved live Qloo trace and external deployment. Devpost registration and final entry remain gated on Jose's explicit acceptance of the official rules and eligibility terms.
