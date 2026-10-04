const DEFAULT_BASE = process.env.QLOO_API_URL || "https://hackathon.api.qloo.com";

export const DOMAIN_TYPES = Object.freeze({
  music: "urn:entity:artist",
  places: "urn:entity:place",
  brands: "urn:entity:brand",
  travel: "urn:entity:destination",
  books: "urn:entity:book",
  movies: "urn:entity:movie",
  tv: "urn:entity:tv_show",
  games: "urn:entity:videogame",
  tags: "urn:tag",
});

function apiKey() {
  const key = process.env.QLOO_API_KEY;
  if (!key) throw new Error("QLOO_API_KEY is required for live Qloo calls");
  return key;
}

async function qlooGet(path, params, fetchImpl = fetch) {
  const url = new URL(path, DEFAULT_BASE);
  for (const [key, value] of Object.entries(params || {})) {
    if (value !== undefined && value !== null && value !== "") {
      url.searchParams.set(key, String(value));
    }
  }
  const response = await fetchImpl(url, {
    headers: { "X-Api-Key": apiKey(), accept: "application/json" },
    signal: AbortSignal.timeout(15000),
  });
  const text = await response.text();
  let body;
  try { body = text ? JSON.parse(text) : {}; }
  catch { throw new Error(`Qloo returned non-JSON HTTP ${response.status}`); }
  if (!response.ok) {
    const detail = body?.message || body?.error || text || response.statusText;
    throw new Error(`Qloo HTTP ${response.status}: ${detail}`);
  }
  return body;
}

function arraysDeep(value, found = []) {
  if (Array.isArray(value)) {
    found.push(value);
    for (const item of value) arraysDeep(item, found);
  } else if (value && typeof value === "object") {
    for (const item of Object.values(value)) arraysDeep(item, found);
  }
  return found;
}

function entityId(item) {
  if (!item || typeof item !== "object") return null;
  return item.entity_id || item.entityId || item.id || item?.entity?.id || item?.entity?.entity_id || null;
}

function label(item) {
  if (!item || typeof item !== "object") return "";
  return item.name || item.title || item.label || item?.entity?.name || item?.entity?.title || "";
}

export function pickEntity(searchBody) {
  const candidates = arraysDeep(searchBody)
    .flat()
    .filter((item) => entityId(item));
  if (!candidates.length) throw new Error("Qloo search returned no resolvable entity");
  const first = candidates[0];
  return { id: entityId(first), name: label(first) || String(entityId(first)), raw: first };
}

export async function searchEntity(query, fetchImpl = fetch) {
  const body = await qlooGet("/search", { query, limit: 8 }, fetchImpl);
  return { query, entity: pickEntity(body), raw: body };
}

export async function getInsights(entityIdValue, domain, fetchImpl = fetch) {
  const type = DOMAIN_TYPES[domain];
  if (!type) throw new Error(`unsupported domain: ${domain}`);
  const body = await qlooGet("/v2/insights", {
    "filter.type": type,
    "signal.interests.entities": entityIdValue,
    take: 8,
  }, fetchImpl);
  return { domain, type, raw: body };
}
