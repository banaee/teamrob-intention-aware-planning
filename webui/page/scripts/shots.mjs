// Screenshots of the page in a real browser (T-viz 0.3): every exported sample, tilted and from above.
// Uses the installed Google Chrome through playwright-core (no browser download). The page must be served
// (`npm run dev`, or `npm run preview` after a build).
//
//   npm run shots -- [--url http://localhost:5173] [--out ../../docs/handoffs/tviz_trial] [--width 1600 --height 1000]

import { mkdirSync, readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

import { chromium } from "playwright-core";

const here = dirname(fileURLToPath(import.meta.url));
const { values } = parseArgs({
  options: {
    url: { type: "string", default: "http://localhost:5173" },
    out: { type: "string", default: resolve(here, "../../../docs/handoffs/tviz_trial") },
    width: { type: "string", default: "1600" },
    height: { type: "string", default: "1000" },
    scale: { type: "string", default: "2" },
  },
});

const samples = JSON.parse(readFileSync(resolve(here, "../public/samples/index.json"), "utf8"));
mkdirSync(values.out, { recursive: true });

const browser = await chromium.launch({ channel: "chrome", args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"] });
const page = await browser.newPage({
  viewport: { width: Number(values.width), height: Number(values.height) },
  deviceScaleFactor: Number(values.scale),
});
page.on("console", (m) => { if (m.type() === "error" || m.type() === "warning") console.log(`[page] ${m.text()}`); });
page.on("pageerror", (e) => console.log(`[page] ${e.message}`));

for (const sample of samples) {
  for (const view of ["tilted", "top"]) {
    await page.goto(`${values.url}/?sample=${sample.name}&view=${view}`, { waitUntil: "load" });
    await page.waitForSelector(".env-pane canvas");
    await page.waitForTimeout(1500);    // the floor text's font and the first frames
    const file = resolve(values.out, `${sample.name}_${view}.png`);
    await page.screenshot({ path: file });
    console.log(`[shots] ${file}`);
  }
}
await browser.close();
