# Amazon / Alexa+ Friction Log

## 1. Proving protocol-version eligibility

Task attempted: Verify that the self-hosted MCP implementation satisfies the hackathon requirement for MCP spec 2025-11-25 or later over Streamable HTTP.

Steps taken: Built the server with the current MCP Python SDK v2, exercised it through a real HTTP client, and added a CI assertion that records the negotiated protocol version.

Expected: The version used by the client/server pair would be obvious from a normal tool-call smoke test.

Actual: A successful Streamable HTTP tool call proves the transport, but the original smoke test did not explicitly print or assert the negotiated protocol version.

Severity: Important.

Workaround: Inspect client.protocol_version in the connected MCP client and fail CI if the negotiated version is older than 2025-11-25.

Actionable suggestion: Provide an Alexa+ MCP starter that prints the negotiated protocol version and includes a ready-made compatibility test for the minimum accepted spec.

## 2. Safe public-host defaults

Task attempted: Prepare the MCP server for local development and eventual public deployment.

Steps taken: Initially used a conventional 0.0.0.0 bind in the server entry point, then ran an independent static-security scan.

Expected: Local and deployment behavior would be explicit and safe by default.

Actual: Static analysis correctly flagged the default all-interface bind as a medium-risk configuration.

Severity: Important.

Workaround: Default to 127.0.0.1; require an explicit HOST environment variable for public deployment.

Actionable suggestion: Self-hosted MCP deployment examples should distinguish safe local defaults from intentional public binding and show the recommended production configuration.
