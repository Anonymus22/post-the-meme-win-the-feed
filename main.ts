import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const postPath = join(here, "POST.json");

// Validate POST.json before copying: it must be JSON with a string "url"
// field that points at an X/Twitter status (…/status/<digits>).
let post: unknown;
try {
  post = JSON.parse(readFileSync(postPath, "utf8"));
} catch (err) {
  throw new Error(`POST.json is not valid JSON: ${(err as Error).message}`);
}
const url =
  post !== null && typeof post === "object"
    ? (post as Record<string, unknown>).url
    : undefined;
const STATUS_URL =
  /^https:\/\/(www\.|mobile\.)?(x\.com|twitter\.com)\/[^/]+\/status\/\d+\/?$/;
if (typeof url !== "string" || !STATUS_URL.test(url)) {
  throw new Error(
    `POST.json must contain a string "url" matching an X/Twitter status URL ` +
      `(https://x.com/<handle>/status/<digits>); got: ${JSON.stringify(url)}`,
  );
}

mkdirSync("/output", { recursive: true });
copyFileSync(postPath, "/output/POST.json");
