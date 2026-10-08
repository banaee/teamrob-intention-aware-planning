// Exports the built deck as a PDF, one page per slide in its final step (every click of the slide made), from
// screenshots taken in the installed Google Chrome as scripts/shots.mjs takes them, at 2560 x 1440; Chrome then prints
// the pages into one file. The speaker notes are not in it. A fallback copy of the talk, and a handout for review.
//
//   npm run preview &   then   npm run pdf -- [--url http://127.0.0.1:4173] [--out pdf/deck_<yyyy-mm-dd-hh-mm>.pdf]

import { mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

import { chromium } from "playwright-core";

const here = dirname(fileURLToPath(import.meta.url));
/** The local date and time, yyyy-mm-dd-hh-mm. */
function stamp() {
  const d = new Date();
  const p = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}-${p(d.getHours())}-${p(d.getMinutes())}`;
}
const { values } = parseArgs({
  options: {
    url: { type: "string", default: "http://127.0.0.1:4173" },
    out: { type: "string", default: resolve(here, `../pdf/deck_${stamp()}.pdf`) },   // dated: earlier exports are kept
    settle: { type: "string", default: "1300" },
  },
});
const [W, H] = [2560, 1440];
const origin = new URL(values.url).origin;

const browser = await chromium.launch({ channel: "chrome", args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"] });
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
let outside = 0;
await page.route("**/*", (route) => {
  if (new URL(route.request().url()).origin === origin || route.request().url().startsWith("data:")) return route.continue();
  outside += 1;
  return route.abort();
});
await page.goto(`${values.url}/#/0`);
await page.waitForFunction(() => window.deck !== undefined);
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(1500);

const last = new Map();      // slide index -> its screenshot in its final step so far
for (;;) {
  const at = await page.evaluate(() => ({
    h: window.deck.getIndices().h,
    end: window.deck.isLastSlide() && !window.deck.availableFragments().next,
  }));
  last.set(at.h, await page.screenshot({ type: "png" }));
  if (at.end) break;
  await page.mouse.click(W / 2, H / 2);
  await page.waitForTimeout(Number(values.settle));
}

const pages = [...last.keys()].sort((a, b) => a - b).map((h) => last.get(h).toString("base64"));
const sheet = await browser.newPage();
await sheet.setContent(`<!doctype html><html><head><style>
  @page { size: ${W}px ${H}px; margin: 0; }
  html, body { margin: 0; }
  img { display: block; width: ${W}px; height: ${H}px; page-break-after: always; }
</style></head><body>${pages.map((p) => `<img src="data:image/png;base64,${p}">`).join("")}</body></html>`);
mkdirSync(dirname(values.out), { recursive: true });
await sheet.pdf({ path: values.out, width: `${W}px`, height: `${H}px`, printBackground: true, preferCSSPageSize: true });
await browser.close();
console.log(`[pdf] ${pages.length} slides written to ${values.out}; outside requests: ${outside}`);
if (outside > 0) process.exit(1);
