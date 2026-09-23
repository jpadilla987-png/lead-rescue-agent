# AI-vs-AI release loop

Every serious release candidate must move through six distinct review roles:

1. **Builder** — explains what changed, what was tested, and what is still uncertain.
2. **Tester** — attacks functionality, edge cases, malformed inputs, and failure behavior.
3. **Critic** — identifies weak reasoning, overclaims, missing evidence, and unnecessary complexity.
4. **Rules auditor** — checks the official competition rules, required fields, dates, eligibility assumptions, and disclosure language.
5. **User reviewer** — evaluates whether the product is understandable, useful, and usable by a real person.
6. **Judge** — evaluates the finished evidence package against the competition rubric.

## Gate

A candidate is not submission-ready unless:
- all six roles have produced evidence-backed findings;
- there are no unresolved blocker or high-severity findings;
- at least one reproducible test evidence reference exists;
- at least one proof-vault reference exists.

A medium or low finding may remain only when it is explicitly accepted and documented.

## Required loop

Builder -> Tester -> Critic -> Rules Auditor -> User Reviewer -> Judge -> Fix -> Retest -> Rejudge.

The point is not to create artificial consensus. Reviewers should disagree when the evidence supports disagreement. The release gate is designed to prevent a single optimistic reviewer from declaring victory.
