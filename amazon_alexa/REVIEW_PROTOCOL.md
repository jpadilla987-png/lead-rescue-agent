# Independent review protocol

Lead Rescue Voice should not be treated as finished just because the happy path works.

Every release candidate should be reviewed in three separate roles:

1. **Builder review** — confirm the feature works as designed and the setup is reproducible.
2. **Adversarial review** — try malformed inputs, edge cases, ambiguous user requests, authority-boundary failures, and misleading output.
3. **Security review** — inspect dependency, secret-handling, unsafe action, injection, and data-exposure risks.

A reviewer should report:
- finding;
- severity: blocker / high / medium / low;
- evidence;
- reproduction steps;
- proposed fix;
- retest result.

No claim is considered verified until there is test evidence or a reproducible manual check.

## Current focus

For the Amazon Alexa+ submission, reviewers should specifically challenge:
- whether the MCP server is genuinely reachable over Streamable HTTP;
- whether lead ranking is deterministic and bounded;
- whether pricing/discount authority fails closed;
- whether unknown lead IDs and invalid parameters are rejected safely;
- whether the README matches the actual branch contents;
- whether the Devpost claims are supported by code and tests.
