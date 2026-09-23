# Lead Rescue Voice — Amazon Alexa+ MCP build

This directory is the Amazon Developer Hackathon implementation of **Lead Rescue Voice**. It is isolated from the older Agents for Humans submission so the prior judged project remains unchanged.

## What is new for the Amazon hackathon

The original repository predates the Amazon submission period. This \`amazon-alexa\` branch is a significant new build created for the Amazon Alexa+ track:

- a current MCP Python SDK v2 server;
- Streamable HTTP at \`/mcp\`;
- lead-priority and lead-inspection MCP tools;
- a guarded follow-up tool that escalates pricing authority rather than inventing discounts;
- an Alexa+-style morning briefing prompt;
- in-process MCP tests and a real Streamable HTTP client smoke test;
- branch CI that installs the current MCP SDK and exercises both paths.

## Run

Python 3.10+ is required.

\`\`\`bash
python -m venv .venv
source .venv/bin/activate
pip install -r amazon_alexa/requirements.txt
PYTHONPATH=amazon_alexa python amazon_alexa/server.py
\`\`\`

The MCP endpoint is then:

\`\`\`text
http://127.0.0.1:8000/mcp
\`\`\`

The server uses the official MCP Python SDK and runs with \`transport="streamable-http"\`, \`stateless_http=True\`, and JSON responses.

## Test

\`\`\`bash
PYTHONPATH=amazon_alexa python -m unittest discover -s amazon_alexa/tests -v
PYTHONPATH=amazon_alexa python amazon_alexa/smoke.py
\`\`\`

To exercise the network transport, start the server and run:

\`\`\`bash
PYTHONPATH=amazon_alexa python amazon_alexa/http_smoke.py
\`\`\`

## MCP surface

- \`prioritize_leads(limit=3)\` — returns a transparent, ranked rescue queue.
- \`inspect_lead(lead_id)\` — returns the lead plus its score and explanation.
- \`prepare_follow_up(lead_id, tone="warm")\` — creates a bounded draft and escalates decisions outside the agent's authority.
- \`morning_rescue_brief\` — reusable prompt for an Alexa+-style host.

## Safety boundary

Lead Rescue Voice does not independently promise discounts, price matches, availability, warranty exceptions, or unusual commitments. Those cases are surfaced to the owner with the reason for escalation.

## Build credit

Entrant: **Jose Padilla**  
AI engineering assistance: **ChatGPT by OpenAI**

## License

The repository is MIT licensed.
