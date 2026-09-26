# Family Joint 001 — Dual-AI Lead Gate

A tiny deterministic gate for AVA + Sable collaboration.

## Why this exists

Sable is better positioned to surface fresh X/web buyer signals. AVA is better positioned to verify Gmail history, connected-account state, build artifacts, and execute outbound actions. Fuse is supposed to kill weak assumptions before money or attention is wasted.

This tool keeps those roles separate and prevents either AI from turning a vague lead into fake progress.

## Promotion rule

A lead can only become \`SURVIVES\` when all factual gates pass **and** at least two independent reviews are \`PASS\`.

Hard gates:
- <=48 hours old
- compensation/payment path verified
- **an explicit monetary amount exists in the pay quote**
- direct route verified
- $0 upfront cost
- fit >=4/5
- no mandatory live/video conflict
- no unsupported credential/experience requirement
- not already contacted/killed/stale

Review outcomes:
- 2+ PASS and no KILL/UNKNOWN -> \`SURVIVES\`
- PASS + KILL -> \`EVIDENCE_REQUIRED\`
- missing review or any UNKNOWN -> \`EVIDENCE_REQUIRED\`
- hard-gate failure -> \`KILLED\`
- otherwise-valid lead with a protected human step -> \`HUMAN_GATE\`

## Roles

- **Sable:** fresh outside signal + independent first-pass review. No outbound.
- **AVA:** source verification, exact Gmail dedupe, connected-tool execution. One outbound maximum.
- **Fuse:** adversarial review. A disagreement triggers an evidence check, not a vote.
- **Jose:** only genuine protected gates.

## Run

\`\`\`bash
python -m unittest -v joint/test_lead_gate.py
python joint/lead_gate.py joint/sample_packet.json
\`\`\`

This project does not send messages, apply to jobs, spend money, or bypass protected account steps. It only decides whether a candidate is worth the next action.
