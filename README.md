# Lead Rescue Voice — Amazon Alexa+ Hackathon Branch

This branch contains the **Amazon Developer Hackathon** build of Lead Rescue Voice.

The original repository was created before the Amazon submission period for a different competition. To preserve that judged work unchanged, all Amazon-specific implementation is isolated on the `amazon-alexa` branch and in `amazon_alexa/`.

## Amazon-specific implementation

The new build uses the current official **Model Context Protocol Python SDK** and exposes a self-hosted **Streamable HTTP** MCP endpoint at `/mcp`.

Implemented tools:

- `prioritize_leads(limit)` — ranks leads by rescue urgency with transparent reasons.
- `inspect_lead(lead_id)` — returns the lead, score, and why it needs attention.
- `prepare_follow_up(lead_id, tone)` — drafts a bounded follow-up and escalates owner-only decisions.
- `morning_rescue_brief` — an Alexa+-style reusable briefing prompt.

Safety boundary: the agent does not invent discounts, price matches, availability, warranty exceptions, or unusual commitments.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r amazon_alexa/requirements.txt
PYTHONPATH=amazon_alexa python amazon_alexa/server.py
```

MCP endpoint:

```text
http://127.0.0.1:8000/mcp
```

## Test

```bash
PYTHONPATH=amazon_alexa python -m unittest discover -s amazon_alexa/tests -v
PYTHONPATH=amazon_alexa python amazon_alexa/smoke.py
```

For a real network smoke test, start the server and run:

```bash
PYTHONPATH=amazon_alexa python amazon_alexa/http_smoke.py
```

See [amazon_alexa/README.md](amazon_alexa/README.md) for the detailed Amazon build notes.

## Significant-update disclosure

The repository predates the Amazon hackathon, but this Alexa+/MCP implementation is a new, significant update created during the Amazon submission period. The prior project files remain in the branch history for transparency.

## Build credit

Entrant: **Jose Padilla**  
AI engineering assistance: **ChatGPT by OpenAI**

## License

MIT
