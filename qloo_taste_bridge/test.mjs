import test from "node:test";
import assert from "node:assert/strict";
import {
  buildRecommendationArgs,
  buildSearchArgs,
  extractEntities,
  integrationStatus,
  recommendQloo,
  searchQloo,
  validateAnchor,
  validateEntityId,
  validateTargetType,
} from "./app.mjs";

const fakeEnv = { PATH: process.env.PATH, QLOO_API_KEY: "test-event-key" };

test("accepts a public cultural anchor", () => {
  assert.equal(validateAnchor("Agatha Christie"), "Agatha Christie");
});

test("rejects email-like personal data", () => {
  assert.throws(() => validateAnchor("person@example.com"), /personal\/contact/);
});

test("validates entity and target type", () => {
  assert.equal(validateEntityId("urn:entity:book:abc_123"), "urn:entity:book:abc_123");
  assert.equal(validateTargetType("movie"), "movie");
  assert.throws(() => validateTargetType("credit_score"), /targetType/);
});

test("builds supported Qloo search command", () => {
  assert.deepEqual(
    buildSearchArgs("Agatha Christie"),
    ["api", "search", "--query", "Agatha Christie", "--take", "5", "--json"],
  );
});

test("builds nontrivial Qloo insights command", () => {
  const args = buildRecommendationArgs("urn:entity:book:abc", "movie");
  assert.equal(args[0], "api");
  assert.equal(args[1], "insights");
  assert.equal(args[3], "urn:entity:movie");
  const params = JSON.parse(args[5]);
  assert.equal(params["signal.interests.entities"], "urn:entity:book:abc");
  assert.equal(params["filter.type"], "urn:entity:movie");
  assert.equal(params.take, 8);
});

test("normalizes search output and retains provenance", async () => {
  const fakeRunner = async (_cmd, argv) => {
    assert.equal(argv.includes("search"), true);
    return { stdout: JSON.stringify({ results: [{ entity_id: "x1", name: "Agatha Christie", subtype: "person" }] }) };
  };
  const value = await searchQloo("Agatha Christie", fakeRunner, fakeEnv);
  assert.equal(value.source, "Qloo search");
  assert.equal(value.candidates[0].id, "x1");
});

test("uses Qloo insights for cross-domain recommendations", async () => {
  const fakeRunner = async (_cmd, argv) => {
    assert.equal(argv.includes("insights"), true);
    return { stdout: JSON.stringify({ results: [{ entity_id: "m1", name: "Knives Out", subtype: "movie", affinity: 0.82 }] }) };
  };
  const value = await recommendQloo("urn:entity:book:abc", "movie", fakeRunner, fakeEnv);
  assert.equal(value.source, "Qloo insights");
  assert.equal(value.target_type, "movie");
  assert.equal(value.recommendations[0].name, "Knives Out");
});

test("fails closed without a server credential", async () => {
  const never = async () => { throw new Error("runner should not execute"); };
  await assert.rejects(
    () => searchQloo("Agatha Christie", never, { PATH: process.env.PATH }),
    /QLOO_API_KEY/,
  );
});

test("extractEntities rejects unexpected responses", () => {
  assert.throws(() => extractEntities({ nope: true }), /entity list/);
});

test("integration status never exposes the key", () => {
  const status = integrationStatus({ QLOO_API_KEY: "secret" });
  assert.equal(status.connected, true);
  assert.equal(JSON.stringify(status).includes("secret"), false);
});
