import test from "node:test";
import assert from "node:assert/strict";
import { buildSearchArgs, searchQloo, validateAnchor } from "./app.mjs";

test("accepts a public cultural anchor", () => {
  assert.equal(validateAnchor("Agatha Christie"), "Agatha Christie");
});

test("rejects email-like personal data", () => {
  assert.throws(() => validateAnchor("person@example.com"), /personal\/contact/);
});

test("builds the official Qloo API search command", () => {
  assert.deepEqual(
    buildSearchArgs("Agatha Christie"),
    ["api", "search", "--query", "Agatha Christie", "--json"],
  );
});

test("normalizes successful Qloo output", async () => {
  const fakeRunner = async () => ({ stdout: JSON.stringify({ results: [{ id: "x1" }] }) });
  const value = await searchQloo("Agatha Christie", fakeRunner);
  assert.equal(value.source, "qloo");
  assert.equal(value.result.results[0].id, "x1");
  assert.equal(value.limitations.length, 2);
});

test("fails closed on Qloo error", async () => {
  const fakeRunner = async () => { throw new Error("401"); };
  await assert.rejects(() => searchQloo("Agatha Christie", fakeRunner), /failed closed/);
});
