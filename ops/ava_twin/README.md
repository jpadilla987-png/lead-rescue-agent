# AVA Twin Keeper v0.3 — zero-cost proof-first memory kernel

A **small, tested, offline component** for the existing AVA / Twin / Fuse family. It does not replace Fuse v0.2 or the existing Family infrastructure, and it is **not a second trained AI model**. It uses only Python's standard library and SQLite, no internet or API bill.

It fixes one recurring failure: confusing an interesting lead or marketing offer with money received. Keep prospects, claim deadlines, evidence provenance, human-only gates and an auditable event history across restarts. Fuse-style gates reject claims of income without a transaction receipt, duplicate claims from one source lineage, and treating restricted child funds as spendable cash.

## Run

```
python -m unittest -v test_twin_keeper.py
python twin_keeper.py --db ./private.sqlite add sample_lead.json
python twin_keeper.py --db ./private.sqlite report
```

A sample lead is intentionally fictional, so tests cannot be confused with actual earnings. `private.sqlite` is your durable local state; **do not commit it, email it or publish it**. The repository should include only code/tests/sample fixture without user financial details.

`status ID paid --receipt local://bank-confirmed-reference` **requires source verified** and only works for unrestricted cash. The command records a receipt reference, not a transfer or bank verification; human/operator must first verify the receipt independently.

## What it does not do

It does not log into banks, email, browse, trade, submit claims, charge cards, call an LLM or generate earnings. Connecting a model, browser worker, and authorized data requires a separate tested integration. High-impact actions always require account-owner authorization. Never place credentials or account identifiers in a public repository.

## Next integration target

Use the **existing** Twin Browser Worker / AVA HOME bridge (when brought online and authenticated by the owner) as input, with a no-spend verification adapter. Do not turn on unrelated dormant Make canaries, re-create Family tasks, or claim Supabase is live while the project is paused.