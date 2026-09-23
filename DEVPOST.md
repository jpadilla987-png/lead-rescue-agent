# NIGHTEYE Evidence Engine — Devpost Working Draft

## One-line pitch

An evidence-first Nemotron agent that detects meaningful change, challenges its own explanation, and produces an auditable next-action brief.

## Inspiration

People rarely suffer from a shortage of information. They suffer from too much information and weak separation between what was observed, what was inferred, and what remains unknown.

NIGHTEYE is designed to make that boundary explicit.

## What it does

A user supplies a monitoring question and a packet of timestamped evidence. NIGHTEYE:

1. identifies whether a material change occurred;
2. separates observation from inference;
3. generates competing explanations;
4. names a falsifier for the leading explanation;
5. preserves explicit unknowns;
6. recommends reversible next actions;
7. returns evidence IDs so the reasoning can be audited.

## How it is built

The reasoning call is implemented through **Nebius Token Factory** using the OpenAI-compatible API and an **NVIDIA Nemotron** model. The default model configured in the project is:

`nvidia/nemotron-3-super-120b-a12b`

FastAPI provides the application layer. A browser interface lets a judge submit an evidence packet and inspect the resulting brief.

The application validates model output after inference. A model response that cites evidence IDs that were never supplied is rejected rather than accepted as fact.

## Track

Best Apps and Agents.

## What is already verified

- deterministic core tests pass;
- security scan passes;
- browser and API paths are implemented;
- container packaging is ready;
- Token Factory client path is implemented.

## What is not yet claimed

A successful live Token Factory/Nemotron inference is not claimed until the live smoke workflow runs with a real Nebius API key and passes.

## Significant-update disclosure

The repository predates this hackathon. The `nebius-nighteye` branch and the `nebius_nighteye/` implementation are the significant hackathon-window update. Older Lead Rescue files are pre-existing and are not part of the Nebius application runtime.

## Build credit

Entrant: Jose Padilla  
AI engineering assistance: ChatGPT by OpenAI
