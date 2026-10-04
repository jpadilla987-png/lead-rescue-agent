import test from "node:test";
import assert from "node:assert/strict";
import { buildTasteBridge, normalizeDomains } from "./bridge.mjs";

test("normalizeDomains defaults to a cross-domain set", () => {
  const value = normalizeDomains();
  assert.ok(value.includes("music"));
  assert.ok(value.includes("places"));
  assert.ok(value.length >= 4);
});

test("bridge resolves one seed then fans out Qloo insights", async () => {
  const calls = [];
  const result = await buildTasteBridge("Agatha Christie", ["books", "travel"], {
    searchEntity: async (query) => {
      calls.push(["search", query]);
      return { entity: { id: "urn:seed:agatha", name: "Agatha Christie" } };
    },
    getInsights: async (id, domain) => {
      calls.push(["insights", id, domain]);
      return { raw: { results: [{ id: `urn:${domain}:1`, name: `${domain} pick`, affinity: 0.91 }] } };
    },
  });
  assert.equal(result.seed.id, "urn:seed:agatha");
  assert.equal(result.recommendations.books[0].affinity, 0.91);
  assert.equal(result.recommendations.travel[0].name, "travel pick");
  assert.equal(result.provenance.qlooRequired, true);
  assert.deepEqual(calls[0], ["search", "Agatha Christie"]);
});

test("one failed Qloo domain does not erase successful domains", async () => {
  const result = await buildTasteBridge("Bauhaus", ["brands", "music"], {
    searchEntity: async () => ({ entity: { id: "urn:seed:bauhaus", name: "Bauhaus" } }),
    getInsights: async (_id, domain) => {
      if (domain === "brands") throw new Error("temporary");
      return { raw: { results: [{ name: "Music Pick", affinity: 0.8 }] } };
    },
  });
  assert.equal(result.recommendations.brands.length, 0);
  assert.equal(result.recommendations.music.length, 1);
  assert.match(result.notes[0], /brands/);
});
