// Screenshots of the page in a real browser (T-viz 1a): the installed Google Chrome through playwright-core (no
// browser download), driving a running web-ui (mesa_sim/run_webui.py) through the page and its requests.
//
//   npm run shots -- [--url http://127.0.0.1:8000] [--out ../../docs/handoffs/tviz_1a] [--runs <json>]
//
// Per sim-run (domain, scenario): the view of its layout and of its layout with its setup, opened from the address and
// chosen in the page (increment (ii)); its start chosen in the page; a run option switched off and on again, the
// options it sets off marked; a moment after some steps (tilted and from above); play at full speed until it pauses
// where all agents have finished; and an end at a step limit; at 1440 x 900, and the moment after some steps also at
// 1920 x 1080. Each file is named <domain>_<n>_<state>_<width>.png.
//
// Then the address's cases (plan_T-viz_1a.md, section 5, "The address"), each checked, a failure stopping the script:
// a bookmark reopens its choice at its start; an address that cannot be opened says why and opens the default choice;
// with a stepped current sim-run the page shows it whatever the address says, and rewrites the address to it.

import { mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

import { chromium } from "playwright-core";

const here = dirname(fileURLToPath(import.meta.url));
const { values } = parseArgs({
  options: {
    url: { type: "string", default: "http://127.0.0.1:8000" },
    out: { type: "string", default: resolve(here, "../../../docs/handoffs/tviz_1a") },
    runs: { type: "string", default: "[]" },
    steps: { type: "string", default: "60" },
    limit: { type: "string", default: "40" },
    scale: { type: "string", default: "2" },
  },
});
const runs = JSON.parse(values.runs);    // [[domain, scenario], ...]
if (runs.length === 0) throw new Error("--runs '[[\"<domain>\", \"<scenario>\"], ...]' names the sim-runs");
const STEPS = Number(values.steps);
const LIMIT = Number(values.limit);
mkdirSync(values.out, { recursive: true });

async function api(path, body) {
  const response = await fetch(`${values.url}/api/${path}`, body === undefined ? undefined : {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
  });
  if (!response.ok) throw new Error(`${path}: ${response.status} ${await response.text()}`);
  return response.json();
}

const browser = await chromium.launch({ channel: "chrome", args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"] });

async function open(width, height) {
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: Number(values.scale) });
  page.on("console", (m) => { if (m.type() === "error" || m.type() === "warning") console.log(`[page] ${m.text()}`); });
  page.on("pageerror", (e) => console.log(`[page] ${e.message}`));
  return page;
}

async function settle(page) {
  await page.waitForSelector(".env-pane canvas");
  await page.waitForTimeout(1200);      // the floor text's font and the first frames
}

async function shot(page, name) {
  const file = resolve(values.out, `${name}_${page.viewportSize().width}.png`);
  await page.screenshot({ path: file });
  console.log(`[shots] ${file}`);
}

const catalogue = await api("catalogue");
const pathEndsWith = (page, s) =>
  page.waitForFunction((x) => document.querySelector(".page-path")?.textContent?.endsWith(x), s);

for (const [domain, scenario] of runs) {
  // The catalogue's default choice first, so that the run options are the start's (they stay as set when the
  // scenario changes, P13).
  await api("choose", catalogue.default_choice);
  const entry = catalogue.domains.find((d) => d.name === domain).scenarios.find((s) => s.id === scenario);
  const layout = entry.reference_layouts[0];
  const page = await open(1440, 900);
  // 0. The layout's view, opened from the address; then its setup chosen in the page.
  await page.goto(`${values.url}/?domain=${domain}&layout=${layout}`, { waitUntil: "load" });
  await pathEndsWith(page, layout);
  await settle(page);
  await shot(page, `${domain}_0_layout`);
  await page.getByRole("button", { name: new RegExp(`^${entry.setup}`) }).click();
  await pathEndsWith(page, entry.setup);
  await settle(page);
  await shot(page, `${domain}_0_setup`);
  // 1. The start, chosen in the page.
  await page.getByRole("button", { name: new RegExp(`^${scenario}`) }).click();
  await pathEndsWith(page, scenario);
  await settle(page);
  await shot(page, `${domain}_1_start`);
  // A run option switched off: the model is built again, and the options it sets off are marked; then on again.
  const first = catalogue.run_options.find((o) => o.kind === "switch");
  const row = page.locator(".option", { has: page.getByText(first.name, { exact: true }) });
  await row.getByRole("button").click();
  await page.locator(".option-effect").first().waitFor();
  await page.waitForTimeout(400);
  await shot(page, `${domain}_1_option_off`);
  await row.getByRole("button").click();
  await page.locator(".option-effect").first().waitFor({ state: "detached" });

  // 2. A moment after some steps, read again from the server (a reload shows the current sim-run).
  const { state } = await api("current");
  for (let k = 0; k < STEPS; k++) await api("step", { sim_run: state.description.sim_run });
  await page.reload({ waitUntil: "load" });
  await settle(page);
  await shot(page, `${domain}_2_tick${STEPS - 1}`);
  await page.getByRole("button", { name: "From above" }).click();
  await page.waitForTimeout(600);
  await shot(page, `${domain}_3_tick${STEPS - 1}_above`);
  const wide = await open(1920, 1080);
  await wide.goto(values.url, { waitUntil: "load" });
  await settle(wide);
  await shot(wide, `${domain}_2_tick${STEPS - 1}`);
  await wide.close();

  // 4. Play at full speed from the start until it pauses where all agents have finished.
  await page.getByRole("button", { name: "Tilted" }).click();
  await page.getByRole("button", { name: /Reset/ }).click();
  await page.waitForFunction(() => document.querySelector(".control-tick")?.textContent?.startsWith("start"));
  await page.getByLabel("Speed").selectOption("0");
  await page.getByRole("button", { name: /Play/ }).click();
  await page.getByText("All agents have finished", { exact: false }).waitFor({ timeout: 180000 });
  await page.getByRole("button", { name: /Play/ }).waitFor();
  await page.waitForTimeout(600);
  await shot(page, `${domain}_4_finished`);

  // 5. An end at a step limit: the same choice with a limit, stepped to it.
  const options = state.description.stated.options.map((o) => (o.kind === "limit" ? { ...o, value: LIMIT } : o));
  const limited = await api("choose", { domain, layout: entry.reference_layouts[0], scenario, options });
  for (let k = 0; k < LIMIT; k++) await api("step", { sim_run: limited.description.sim_run });
  await page.reload({ waitUntil: "load" });
  await settle(page);
  await shot(page, `${domain}_5_ended`);
  await page.close();
}

// The address's cases, on the first sim-run named.
{
  const [domain, scenario] = runs[0];
  const entry = catalogue.domains.find((d) => d.name === domain).scenarios.find((s) => s.id === scenario);
  const page = await open(1440, 900);
  const query = (s) => `domain=${domain}&layout=${entry.reference_layouts[0]}&setup=${entry.setup}&scenario=${s}`;
  // A bookmark reopens its choice at its start (a reset leaves an unstepped sim-run: the address wins).
  const { state } = await api("current");
  await api("reset", { sim_run: state.description.sim_run });
  await page.goto(`${values.url}/?${query(scenario)}&steps=7`, { waitUntil: "load" });
  await pathEndsWith(page, scenario);
  await page.waitForFunction(() => document.querySelector(".control-tick")?.textContent?.startsWith("start · 0 of 7"));
  console.log("[shots] address: a bookmark reopens its choice at its start, with its run options");
  // An address that cannot be opened says why, and opens the default choice.
  await page.goto(`${values.url}/?${query("scenario_none")}`, { waitUntil: "load" });
  await page.getByText("was not opened", { exact: false }).waitFor();
  await pathEndsWith(page, catalogue.default_choice.scenario);
  await settle(page);
  await shot(page, "address_not_opened");
  // A stepped current sim-run wins over the address, which is rewritten to it.
  const now = await api("current");
  await api("step", { sim_run: now.state.description.sim_run });
  await page.goto(`${values.url}/?${query(scenario)}`, { waitUntil: "load" });
  await pathEndsWith(page, catalogue.default_choice.scenario);
  await page.waitForFunction((s) => window.location.search.includes(`scenario=${s}`), catalogue.default_choice.scenario);
  await page.getByText("locked", { exact: true }).waitFor();
  console.log("[shots] address: a stepped current sim-run is shown whatever the address says");
  await page.close();
}
await browser.close();
