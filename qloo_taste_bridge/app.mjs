import { execFile } from "node:child_process";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);

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

export function buildSearchArgs(anchor) {
  return ["api", "search", "--query", validateAnchor(anchor), "--json"];
}

export async function searchQloo(anchor, runner = execFileAsync) {
  const args = buildSearchArgs(anchor);
  try {
    const { stdout } = await runner("qloo", args, {
      timeout: 15000,
      maxBuffer: 1024 * 1024,
      env: process.env,
    });
    const parsed = JSON.parse(stdout);
    return {
      source: "qloo",
      query: validateAnchor(anchor),
      result: parsed,
      limitations: [
        "Aggregate cultural affinity is not evidence about an individual.",
        "Search matches are candidates and require semantic review.",
      ],
    };
  } catch (error) {
    throw new Error(`Qloo search failed closed: ${error.message}`);
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const anchor = process.argv.slice(2).join(" ");
  searchQloo(anchor)
    .then((value) => console.log(JSON.stringify(value, null, 2)))
    .catch((error) => {
      console.error(error.message);
      process.exitCode = 1;
    });
}
