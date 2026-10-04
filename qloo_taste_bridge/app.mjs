import { execFile } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);

export const QLOO_BASE_URL = "https://hackathon.api.qloo.com";
export const MIN_HARNESS_VERSION = "0.1.26";
export const TARGET_TYPES = Object.freeze({
  artist: "urn:entity:artist",
  movie: "urn:entity:movie",
  book: "urn:entity:book",
  place: "urn:entity:place",
  brand: "urn:entity:brand",
});

export function validateAnchor(value) {
  if (typeof value !== "string") throw new TypeError("anchor must be a string");
  const anchor = value.trim();
  if (anchor.length < 2 || anchor.length > 120) {
    throw new Error("anchor must be between 2 and 120 characters");
  }
  if (/[@]|https?:\/\/|\b\d{7,}\b/i.test(anchor)) {
    throw new Error("anchor looks like personal/contact data; use a public cultural entity");
  }
  return anchor;
}

export function validateEntityId(value) {
  if (typeof value !== "string") throw new TypeError("entityId must be a string");
  const id = value.trim();
  if (!/^[A-Za-z0-9:_-]{3,200}$/.test(id)) throw new Error("entityId is invalid");
  return id;
}

export function validateTargetType(value) {
  if (typeof value !== "string" || !(value in TARGET_TYPES)) {
    throw new Error("targetType must be artist, movie, book, place, or brand");
  }
  return value;
}

export function buildSearchArgs(anchor) {
  return ["api", "search", "--query", validateAnchor(anchor), "--take", "5", "--json"];
}

export function buildRecommendationArgs(entityId, targetType) {
  const id = validateEntityId(entityId);
  const type = TARGET_TYPES[validateTargetType(targetType)];
  const params = {"filter.type": type, "signal.interests.entities": id, take: 8};
  return ["api", "insights", "--type", type, "--params", JSON.stringify(params), "--json"];
}

export function integrationStatus(env = process.env) {
  return {
    provider: "Qloo via @qloo/qloo-harness >=" + MIN_HARNESS_VERSION,
    endpoint: QLOO_BASE_URL,
    connected: Boolean(env.QLOO_API_KEY),
  };
}

function resolveHarnessBin() {
  const entry = fileURLToPath(import.meta.resolve("@qloo/qloo-harness"));
  return path.join(path.dirname(entry), "bin.js");
}

function liveEnvironment(env) {
  if (!env.QLOO_API_KEY) throw new Error("QLOO_API_KEY is not configured on the server");
  return {
    PATH: env.PATH ?? "",
    HOME: "/tmp/tastebridge-qloo-home",
    QLOO_API_KEY: env.QLOO_API_KEY,
    QLOO_BASE_URL,
    QLOO_TRUSTED_BASE_URL: QLOO_BASE_URL,
    NO_COLOR: "1",
    CI: "true",
  };
}

export async function runQloo(args, runner = execFileAsync, env = process.env) {
  // Validate server credentials before resolving or executing the optional CLI harness.
  // This preserves the intended fail-closed error even when the harness is unavailable.
  const childEnv = liveEnvironment(env);
  const bin = resolveHarnessBin();
  try {
    const { stdout } = await runner(process.execPath, [bin, ...args], {
      timeout: 20000,
      maxBuffer: 2 * 1024 * 1024,
      windowsHide: true,
      env: childEnv,
    });
    return JSON.parse(stdout);
  } catch (error) {
    const diagnostic = String(error?.stderr || error?.stdout || error?.message || error);
    if (/401|403|unauthori|api.?key|authenticat/i.test(diagnostic)) throw new Error("Qloo rejected the event credential");
    if (/429|rate.?limit|quota/i.test(diagnostic)) throw new Error("Qloo rate limit reached; retry later");
    throw new Error("Qloo request failed closed: " + diagnostic.slice(0, 240));
  }
}

export function extractEntities(data) {
  const entities = Array.isArray(data)
    ? data
    : Array.isArray(data?.results)
      ? data.results
      : data?.results?.entities ?? data?.entities ?? data?.data?.entities;
  if (!Array.isArray(entities)) throw new Error("Qloo response did not contain an entity list");
  return entities.filter((entity) => entity && typeof entity.entity_id === "string" && typeof entity.name === "string");
}

function normalizeEntity(entity) {
  return {
    id: entity.entity_id,
    name: entity.name,
    kind: entity.subtype ?? entity.type ?? null,
    description: typeof entity.properties?.description === "string" ? entity.properties.description.slice(0, 240) : "",
    affinity: typeof entity.query?.affinity === "number" ? entity.query.affinity : typeof entity.affinity === "number" ? entity.affinity : null,
  };
}

export async function searchQloo(anchor, runner = execFileAsync, env = process.env) {
  const query = validateAnchor(anchor);
  const parsed = await runQloo(buildSearchArgs(query), runner, env);
  const candidates = extractEntities(parsed).slice(0, 5).map(normalizeEntity);
  if (!candidates.length) throw new Error("Qloo returned no matching cultural entities");
  return {
    source: "Qloo search",
    query,
    candidates,
    limitations: [
      "Search matches are candidates; the user should choose the intended public cultural entity.",
      "Aggregate cultural affinity is not evidence about an individual person.",
    ],
  };
}

export async function recommendQloo(entityId, targetType, runner = execFileAsync, env = process.env) {
  const id = validateEntityId(entityId);
  const target = validateTargetType(targetType);
  const parsed = await runQloo(buildRecommendationArgs(id, target), runner, env);
  const recommendations = extractEntities(parsed).slice(0, 8).map(normalizeEntity);
  if (!recommendations.length) throw new Error("Qloo returned no cross-domain recommendations");
  return {
    source: "Qloo insights",
    anchor_entity_id: id,
    target_type: target,
    recommendations,
    limitations: [
      "Recommendations are aggregate Qloo affinity results, not probabilities of individual preference.",
      "TasteBridge does not infer sensitive traits or use results for high-impact decisions.",
    ],
  };
}
