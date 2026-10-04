import { validateAnchor } from "./app.mjs";
import { DOMAIN_TYPES, getInsights, searchEntity } from "./qloo_api.mjs";

const DEFAULT_DOMAINS = ["music", "places", "brands", "travel", "books", "movies"];

export function normalizeDomains(input) {
  const values = Array.isArray(input) ? input : String(input || "").split(",");
  const clean = [...new Set(values.map((x) => String(x).trim().toLowerCase()).filter(Boolean))];
  const selected = clean.length ? clean : DEFAULT_DOMAINS;
  const invalid = selected.filter((x) => !DOMAIN_TYPES[x]);
  if (invalid.length) throw new Error(`unsupported domains: ${invalid.join(", ")}`);
  if (selected.length > 6) throw new Error("choose at most 6 domains");
  return selected;
}

function extractResultRows(raw) {
  const candidates = [
    raw?.results,
    raw?.data?.results,
    raw?.data,
    raw?.entities,
  ];
  return candidates.find(Array.isArray) || [];
}

function summarize(row) {
  if (!row || typeof row !== "object") return { value: row };
  const entity = row.entity && typeof row.entity === "object" ? row.entity : row;
  return {
    id: entity.id || entity.entity_id || row.id || row.entity_id || null,
    name: entity.name || entity.title || row.name || row.title || null,
    affinity: row.affinity ?? entity.affinity ?? null,
    type: entity.type || row.type || null,
    location: entity.location || row.location || null,
  };
}

export async function buildTasteBridge(anchor, domains, deps = {}) {
  const cleanAnchor = validateAnchor(anchor);
  const chosen = normalizeDomains(domains);
  const search = deps.searchEntity || searchEntity;
  const insights = deps.getInsights || getInsights;

  const seed = await search(cleanAnchor);
  const resolved = await Promise.allSettled(
    chosen.map((domain) => insights(seed.entity.id, domain))
  );

  const recommendations = {};
  const notes = [];
  resolved.forEach((entry, index) => {
    const domain = chosen[index];
    if (entry.status === "fulfilled") {
      recommendations[domain] = extractResultRows(entry.value.raw).slice(0, 8).map(summarize);
    } else {
      recommendations[domain] = [];
      notes.push(`${domain}: ${entry.reason?.message || "Qloo insight call failed"}`);
    }
  });

  const successfulDomains = Object.entries(recommendations).filter(([, rows]) => rows.length).length;
  if (!successfulDomains) {
    throw new Error("Qloo resolved the seed but returned no usable cross-domain recommendations");
  }

  return {
    source: "qloo",
    mode: "cross-domain-taste-bridge",
    query: cleanAnchor,
    seed: { id: seed.entity.id, name: seed.entity.name },
    domains: chosen,
    recommendations,
    notes,
    provenance: {
      search: "Qloo /search",
      recommendations: "Qloo /v2/insights",
      qlooRequired: true,
    },
    limitations: [
      "Qloo affinities describe cultural relationships, not facts about an individual person.",
      "Recommendations should be reviewed for context, availability, and suitability before action.",
    ],
  };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const anchor = process.argv[2];
  const domains = process.argv.slice(3);
  buildTasteBridge(anchor, domains)
    .then((value) => console.log(JSON.stringify(value, null, 2)))
    .catch((error) => {
      console.error(error.message);
      process.exitCode = 1;
    });
}
