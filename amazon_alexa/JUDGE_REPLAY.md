# Blind Judge Replay Packet

This packet intentionally contains only what a judge should be able to see.

## First 20 seconds

A good lead should not die because the owner is on a ladder, in a truck, or helping another customer. Lead Rescue Voice identifies the leads going cold, explains why they matter now, and prepares the safest next follow-up.

## Demonstrated value

1. Rank a mixed queue of service leads.
2. Explain each rescue score in plain language.
3. Handle an urgent no-cooling request.
4. Detect a price-match request and refuse to invent a discount.
5. Escalate owner-only decisions.
6. Show reproducible test and security evidence.

## Technical evidence

- MCP Python SDK v2 server.
- Streamable HTTP endpoint.
- Protocol compatibility assertion: negotiated revision must be 2025-11-25 or later.
- Functional unit tests.
- Adversarial tests.
- Dependency vulnerability audit.
- Bandit static analysis.
- CodeQL analysis.

## Known limitations

- Demo data is synthetic.
- The current project prepares follow-ups; it does not autonomously send them.
- It does not invent appointment availability, discounts, price matches, warranty exceptions, or unusual commitments.
- Final public video is still a human/account upload gate.

## Significant-update disclosure

The repository existed before the hackathon. The amazon-alexa branch and the Alexa+/MCP implementation were created as a significant update during the submission window.
