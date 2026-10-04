# TasteBridge

Status: working integration code; live Qloo credential still required.

TasteBridge is a Qloo-powered cultural bridge. A user enters one public cultural anchor such as a book, film, artist, place, or brand. The app resolves that text through Qloo search, shows the returned Qloo candidates so the user can disambiguate the intended entity, then uses the chosen Qloo entity ID as an interest signal for Qloo Insights in a different cultural domain.

That second Qloo call is the core product behavior. TasteBridge is intentionally not a generic LLM recommender that would behave the same without Qloo.

## Official Qloo surface

The implementation pins the public event harness:

- @qloo/qloo-harness 0.1.26
- Node 22.19+
- official event endpoint https://hackathon.api.qloo.com
- supported server-side surfaces: qloo api search and qloo api insights

The event credential remains server-side. It is never sent to the browser, committed to Git, or placed in command arguments.

## Flow

1. Search a public cultural anchor through Qloo.
2. Show Qloo's entity candidates instead of silently guessing identity.
3. Let the user choose the intended entity.
4. Call Qloo Insights with that entity as the interest signal.
5. Return cross-domain recommendations with Qloo provenance and explicit limitations.

Supported target domains in this build: movies, books, music artists, places, and brands.

## Run

From qloo_taste_bridge:

npm install
QLOO_API_KEY must be configured in the server environment.
npm start

Open http://localhost:3000.

## Test

npm test

Tests verify search and insights request construction, public-anchor validation, personal/contact-data rejection, cross-domain normalization, fail-closed behavior without a credential, browser routes, and credential non-disclosure.

## Safety boundary

- Public cultural concepts only.
- No email addresses, device IDs, account IDs, or private location history.
- No sensitive-trait inference.
- No employment, credit, insurance, housing, health, or political decisions.
- Qloo results are aggregate affinity evidence, not causal claims or probabilities about an individual.

## Remaining release gates

1. Receive an event-issued Qloo credential or organizer-approved authenticated gateway.
2. Execute and save a real search-to-insights Qloo trace.
3. Deploy the server-side app externally with the credential in the host secret manager.
4. Verify the public demo end-to-end.
5. Complete Devpost registration after Jose supplies the required explicit agreements and answers.
6. Submit the functional demo URL and public repository.
