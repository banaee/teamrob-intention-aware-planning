// Clicks through the built deck in the installed Google Chrome (as webui/page/scripts/shots.mjs: playwright-core, no
// browser download), at the two screen sizes, from the first slide to the last, one mouse click per step, and takes a
// screenshot after every click. Every request that leaves the local server is blocked and counted; a blocked request,
// a page error, or a speaker note visible on the screen stops the script. Warnings are printed only (three.js 0.186
// warns that R3F uses its deprecated Clock).
//
//   npm run preview &   then   npm run shots -- [--url http://127.0.0.1:4173] [--only 2560]
//
// Writes shots/<width>x<height>/<nnn>_s<slide>_f<fragment>.png (untracked).

import { mkdirSync, rmSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

import { chromium } from "playwright-core";

const here = dirname(fileURLToPath(import.meta.url));

/** Waits until the slide has settled: at least `min` ms, then until no replay plays and no view moves (`data-busy`)
 * and no CSS transition runs (a fade, an arrow drawn), at most 30 s. A page is never captured in the middle of a
 * transition. */
async function settle(page, min) {
  await page.waitForTimeout(min);
  await page.waitForFunction(() => document.querySelector(".present [data-busy]") === null
    && document.getAnimations().every((a) => a.playState !== "running"), null, { timeout: 30000, polling: 100 })
    .catch(() => console.log("[settle] still busy after 30 s; captured as it is"));
  await page.waitForTimeout(150);
}

const { values } = parseArgs({
  options: {
    url: { type: "string", default: "http://127.0.0.1:4173" },
    out: { type: "string", default: resolve(here, "../shots") },
    only: { type: "string" },
    settle: { type: "string", default: "400" },     // ms at least after a click; then until the slide has settled
  },
});
const origin = new URL(values.url).origin;
const SIZES = [[2560, 1440], [1920, 1080]].filter(([w]) => values.only === undefined || String(w) === values.only);

const browser = await chromium.launch({ channel: "chrome", args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"] });
const outside = [];
const errors = [];
const warnings = [];
let notesShown = 0;
for (const [width, height] of SIZES) {
  const dir = resolve(values.out, `${width}x${height}`);
  rmSync(dir, { recursive: true, force: true });     // this script's own output folder only
  mkdirSync(dir, { recursive: true });
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
  await page.route("**/*", (route) => {
    if (new URL(route.request().url()).origin === origin || route.request().url().startsWith("data:")) return route.continue();
    outside.push(route.request().url());
    return route.abort();
  });
  page.on("console", (m) => {
    if (m.type() === "error") errors.push(m.text());
    if (m.type() === "warning") warnings.push(m.text());
  });
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto(`${values.url}/#/0`);
  await page.waitForFunction(() => window.deck !== undefined);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(1500);
  let n = 0;
  for (;;) {
    const at = await page.evaluate(() => {
      const i = window.deck.getIndices();
      const visibleNotes = [...document.querySelectorAll("aside.notes")]
        .filter((a) => getComputedStyle(a).display !== "none" && a.getBoundingClientRect().height > 0).length;
      return { h: i.h, f: i.f ?? -1, last: window.deck.isLastSlide() && !window.deck.availableFragments().next, visibleNotes };
    });
    notesShown += at.visibleNotes;
    n += 1;
    const file = resolve(dir, `${String(n).padStart(3, "0")}_s${at.h + 1}_f${at.f + 1}.png`);
    await page.screenshot({ path: file });
    if (at.last) break;
    await page.mouse.click(width / 2, height / 2);
    await settle(page, Number(values.settle));
  }
  console.log(`[shots] ${width}x${height}: ${n} steps, written to ${dir}`);
  await page.close();
}
await browser.close();
for (const url of outside) console.log(`[shots] outside request blocked: ${url}`);
for (const w of new Set(warnings)) console.log(`[shots] page warning: ${w}`);
for (const e of errors) console.log(`[shots] page error: ${e}`);
console.log(`[shots] outside requests: ${outside.length}, page errors: ${errors.length}, notes on screen: ${notesShown}`);
if (outside.length > 0 || errors.length > 0 || notesShown > 0) process.exit(1);
