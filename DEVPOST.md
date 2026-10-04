# TasteBridge — Qloo Agentic Hackathon submission draft

## One-line pitch

TasteBridge turns one public cultural anchor into explainable cross-domain recommendations by resolving the anchor through Qloo and crossing Qloo's taste graph into a different domain.

## Problem

Cross-domain recommendations are easy for a language model to make up and difficult for a user to audit. A plausible connection between a favorite book and a movie, place, artist, or brand may have no evidence behind it.

## What TasteBridge does

1. The user enters a public cultural anchor.
2. Qloo search resolves the text to Qloo entities.
3. The user selects the intended entity.
4. TasteBridge sends that Qloo entity ID into Qloo Insights.
5. Qloo returns recommendations in the selected target domain.
6. The app displays those results with Qloo provenance and explicit limitations.

## Why it is Qloo-powered

TasteBridge's core flow requires Qloo twice: first for entity resolution, then for aggregate cross-domain affinity. Remove Qloo and the recommendation engine stops. The application does not substitute a generic LLM list.

## Technological implementation

- Node.js 22.19+
- @qloo/qloo-harness 0.1.26
- qloo api search
- qloo api insights
- server-only event credential
- HTTP UI/API
- Node test runner
- fail-closed input and credential handling

## Responsible-data boundary

Only public cultural concepts/entities are accepted. The project rejects obvious personal/contact-like input and does not use Qloo for sensitive-trait inference or high-impact decisions. Qloo affinity is described as aggregate cultural evidence, not an individual probability.

## Significant update disclosure

The repository existed before the Qloo Agentic Hackathon. The qloo-taste-bridge branch and qloo_taste_bridge application are the hackathon-window implementation. Older Lead Rescue code is pre-existing and is not represented as new Qloo work.

## Current proof state

Code and tests: implemented.
Real Qloo credential: pending organizer/event access.
Real two-call Qloo trace: pending credential.
Public hosted demo: pending credential and deployment.
Devpost registration/submission: pending Jose's explicit registration agreements and required answers.
