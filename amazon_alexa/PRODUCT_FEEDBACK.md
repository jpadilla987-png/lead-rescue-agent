# Product feedback draft

This is based on tools actually used in the Amazon build.

## Tools, APIs, and SDKs used and what for

- MCP Python SDK v2: implemented the Alexa+ track self-hosted MCP server, tool registration, prompt registration, Streamable HTTP transport, in-process testing, and HTTP client smoke testing.
- Python 3.12 / unittest: deterministic lead scoring, owner-approval boundaries, malformed-input checks, and regression tests.
- GitHub Actions: reproducible functional, adversarial, dependency-audit, static-security, CodeQL, and Project Factory checks.
- Vanilla HTML/CSS/JavaScript: judge-facing Alexa+ style simulated web experience that mirrors the MCP tools and safety behavior.

## What worked well

The MCP Python SDK made the core tool surface compact and readable. Tool and prompt registration are easy to inspect in code, and the same implementation can be exercised in-process and over Streamable HTTP. The connected client exposes protocol metadata, which makes compatibility testable instead of implicit. GitHub Actions made it straightforward to turn those checks into repeatable evidence.

## What needs work

The biggest friction was proving the exact protocol-revision requirement rather than merely proving that the transport worked. A normal successful tool-call smoke test did not make the negotiated MCP revision visible in the output. An Alexa+ focused starter project with a protocol-version assertion, deployment-safe host defaults, and a minimal end-to-end test would remove uncertainty.

## Onboarding experience

Getting from zero to a working MCP tool surface was fast once the current SDK API shape was established. The slower part was converting “it runs” into “it is demonstrably compatible with the exact hackathon requirement.” The additional compatibility and security checks are now automated in CI.

## Would you build with these tools again?

Yes. The MCP tool model is a strong fit for bounded business actions because the callable surface is explicit and testable. I would use the SDK again, especially with automated protocol-version, adversarial, and security checks included from the beginning.
