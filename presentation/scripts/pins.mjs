// The deck draws with the web-ui page's own code, so every package both use must be pinned to the same version in
// both. A difference stops the build: after an upgrade in webui/page, the deck's pin follows it.

import { readFileSync } from "node:fs";

const read = (path) => JSON.parse(readFileSync(new URL(path, import.meta.url), "utf8"));
const deck = read("../package.json");
const page = read("../../webui/page/package.json");
const pins = (p) => ({ ...p.dependencies, ...p.devDependencies });
const ours = pins(deck);
const theirs = pins(page);

const differ = Object.keys(ours).filter((name) => name in theirs && ours[name] !== theirs[name]);
if (differ.length > 0) {
  for (const name of differ) console.error(`[pins] ${name}: deck ${ours[name]}, webui/page ${theirs[name]}`);
  process.exit(1);
}
console.log(`[pins] ${Object.keys(ours).filter((name) => name in theirs).length} shared pins equal webui/page's`);
