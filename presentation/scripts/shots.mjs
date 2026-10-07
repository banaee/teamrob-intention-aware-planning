// Screenshots of the built deck in the installed Google Chrome (as webui/page/scripts/shots.mjs: playwright-core, no
// browser download), at the two screen sizes, with every request that leaves the local server blocked and counted.
// A blocked request or a page error stops the script: the built deck must load nothing from outside. Warnings are
// printed only (three.js 0.186 warns that R3F uses its deprecated Clock).
//
//   npm run preview &   then   npm run shots -- [--url http://127.0.0.1:4173] [--slides 1]
//
// Writes shots/slide<n>_<width>x<height>.png (untracked).

import { mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

import { chromium } from "playwright-core";

const here = dirname(fileURLToPath(import.meta.url));
const { values } = parseArgs({
  options: {
    url: { type: "string", default: "http://127.0.0.1:4173" },
    out: { type: "string", default: resolve(here, "../shots") },
    slides: { type: "string", default: "1" },
  },
});
mkdirSync(values.out, { recursive: true });
const origin = new URL(values.url).origin;
const SIZES = [[2560, 1440], [1920, 1080]];

const browser = await chromium.launch({ channel: "chrome", args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"] });
const outside = [];
const errors = [];
const warnings = [];
for (const [width, height] of SIZES) {
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
  for (let n = 1; n <= Number(values.slides); n++) {
    await page.goto(`${values.url}/#/${n - 1}`);
    await page.waitForSelector("section.present canvas");
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(1200);      // the first frames
    const file = resolve(values.out, `slide${n}_${width}x${height}.png`);
    await page.screenshot({ path: file });
    console.log(`[shots] ${file}`);
  }
  await page.close();
}
await browser.close();
for (const url of outside) console.log(`[shots] outside request blocked: ${url}`);
for (const w of new Set(warnings)) console.log(`[shots] page warning: ${w}`);
for (const e of errors) console.log(`[shots] page error: ${e}`);
console.log(`[shots] outside requests: ${outside.length}, page errors: ${errors.length}`);
if (outside.length > 0 || errors.length > 0) process.exit(1);
