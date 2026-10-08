// Exports the built deck as a PDF, one page per slide in its final step (every click of the slide made), from
// screenshots taken in the installed Google Chrome as scripts/shots.mjs takes them, at 2560 x 1440; Chrome then prints
// the pages into one file. The speaker notes are not in it. A fallback copy of the talk, and a handout for review.
//
//   npm run preview &   then   npm run pdf -- [--url http://127.0.0.1:4173] [--out pdf/deck_<yyyy-mm-dd-hh-mm>.pdf]
//
// --quick (npm run pdf:quick): a fast, rough copy for a quick check, pdf/deck_<yyyy-mm-dd-hh-mm>_quick.pdf: 1280 x 720,
// JPEG pages, each slide jumped to its last step with a short wait (no click played; a replay shows whatever frame it
// has reached).
// --quick --steps (npm run pdf:steps): the same, one page per step (every click of every slide),
// pdf/deck_<yyyy-mm-dd-hh-mm>_quick_steps.pdf.

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
    out: { type: "string" },     // default: pdf/deck_<stamp>.pdf, dated so that earlier exports are kept
    settle: { type: "string", default: "1300" },
    quick: { type: "boolean", default: false },
    steps: { type: "boolean", default: false },
  },
});
const quick = values.quick || values.steps;
const suffix = values.steps ? "_quick_steps" : quick ? "_quick" : "";
const out = values.out ?? resolve(here, `../pdf/deck_${stamp()}${suffix}.pdf`);
const [W, H] = quick ? [1280, 720] : [2560, 1440];
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
const shot = () => page.screenshot(quick ? { type: "jpeg", quality: 70 } : { type: "png" });
if (quick) {
  // Each slide at its last step, by jumping there: no click is played, only a short wait for the slide to draw.
  const count = await page.evaluate(() => window.deck.getTotalSlides());
  for (let h = 0; h < count; h++) {
    console.log(`[pdf] slide ${h + 1} of ${count}`);
    const n = await page.evaluate((i) => window.deck.getSlide(i).querySelectorAll(".fragment").length, h);
    // --steps: every step, from the slide as it opens (fragment -1) to its last; otherwise its last step only
    for (let f = values.steps ? -1 : n - 1; f < n; f++) {
      await page.evaluate(([i, j]) => window.deck.slide(i, 0, j), [h, f]);
      await page.waitForTimeout(700);
      last.set(`${String(h).padStart(3, "0")}.${String(f + 1).padStart(3, "0")}`, await shot());
    }
  }
} else {
  for (;;) {
    const at = await page.evaluate(() => ({
      h: window.deck.getIndices().h,
      end: window.deck.isLastSlide() && !window.deck.availableFragments().next,
    }));
    const key = String(at.h).padStart(3, "0");
    if (!last.has(key)) console.log(`[pdf] slide ${at.h + 1}`);     // progress: the export takes a few minutes
    last.set(key, await shot());
    if (at.end) break;
    await page.mouse.click(W / 2, H / 2);
    await page.waitForTimeout(Number(values.settle));
  }
}

const pages = [...last.keys()].sort((a, b) => (a < b ? -1 : a > b ? 1 : 0)).map((k) => last.get(k).toString("base64"));
const sheet = await browser.newPage();
await sheet.setContent(`<!doctype html><html><head><style>
  @page { size: ${W}px ${H}px; margin: 0; }
  html, body { margin: 0; }
  img { display: block; width: ${W}px; height: ${H}px; page-break-after: always; }
</style></head><body>${pages.map((p) => `<img src="data:image/${quick ? "jpeg" : "png"};base64,${p}">`).join("")}</body></html>`);
mkdirSync(dirname(out), { recursive: true });
await sheet.pdf({ path: out, width: `${W}px`, height: `${H}px`, printBackground: true, preferCSSPageSize: true });
await browser.close();
console.log(`[pdf] ${pages.length} pages written to ${out}; outside requests: ${outside}`);
if (outside > 0) process.exit(1);
