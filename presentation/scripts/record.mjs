// Records, before every build and every start of the dev server, what the deck's slides read from the simulator's side:
// the view of each layout below and its domain's appearance (scripts/record_view.py, through the web-ui's own piece),
// from the original files. The old recording is deleted first; if a recording fails, this script stops with a message
// and the build does not run, so a slide is never built from an old recording.
//
// The Python environment: TEAMROB_PYTHON if set, else the repository's working environment
// (~/python-envs/ir-nomesa-env/bin/python, CLAUDE.md, "Running").

import { spawnSync } from "node:child_process";
import { existsSync, rmSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const VIEWS = [["kitting", "env_layout_01"], ["dock_loading", "env_layout_03"]];   // [domain, layout], one per data file
// The sim-runs replayed on slides (scripts/record_run.py): [name, run file, first tick, last tick]. Talk stage 3's is T-F
// part 1's run file; the others run Hadi's scenarios for the talk (tpres-v4), or copies of them under new ids (tpres-v5:
// scenario_s305_01), from their own run files under configs/kitting/tpres/, outside every measured set.
const TF1 = "configs/kitting/tf1/measurement";
const TPRES = "configs/kitting/tpres";
const RUNS = [
  ["stage1_alone", `${TPRES}/stage1_s301_01.yaml`, 0, 150],                // human-unaware, no human in the scenario
  ["stage2_reactive", `${TPRES}/stage2_s305_01.yaml`, 0, 44],              // intention-unaware; a copy of scenario_s302_02
  ["stage3_switch", `${TF1}/scenario_s12_01/run_060.yaml`, 0, 62],
  ["stage4_break", `${TPRES}/stage4_s304_14_ck_off.yaml`, 70, 150],        // context knowledge off
  ["stage5_context", `${TPRES}/stage5_s304_14_ck_on.yaml`, 70, 150],      // the same scenario, context knowledge on
  ["stage6_unmodelled", `${TPRES}/stage6_s111_02.yaml`, 0, 39],
  ["stage8_dock", "configs/dock_loading/tpres/stage8_dl_s11_01.yaml", 50, 120],              // dock_loading, Hadi's scenario_s11_01
];

const here = dirname(fileURLToPath(import.meta.url));
const repo = resolve(here, "../..");
const python = process.env.TEAMROB_PYTHON ?? join(homedir(), "python-envs/ir-nomesa-env/bin/python");

function stop(message) {
  console.error(`[record] STOPPED: ${message}`);
  console.error("[record] The deck is not built from an old recording. Set TEAMROB_PYTHON to the Python environment");
  console.error("[record] the simulator runs in (it needs the repository's requirements.txt), or fix the error above.");
  process.exit(1);
}

for (const [domain, layout] of VIEWS) rmSync(resolve(repo, `presentation/data/${domain}_${layout}.json`), { force: true });
for (const [name] of RUNS) rmSync(resolve(repo, `presentation/data/run_${name}.json`), { force: true });
if (!existsSync(python)) stop(`no Python interpreter at ${python}`);
for (const [domain, layout] of VIEWS) {
  const run = spawnSync(python, [resolve(here, "record_view.py"), domain, layout], {
    cwd: repo, env: { ...process.env, PYTHONHASHSEED: "0" }, stdio: "inherit",
  });
  if (run.error) stop(`${python} could not be started: ${run.error.message}`);
  if (run.status !== 0) stop(`recording ${domain} ${layout} failed (exit ${run.status})`);
}
for (const [name, run, first, last] of RUNS) {
  const r = spawnSync(python, [resolve(here, "record_run.py"), name, run, String(first), String(last)], {
    cwd: repo, env: { ...process.env, PYTHONHASHSEED: "0" }, stdio: "inherit",
  });
  if (r.error) stop(`${python} could not be started: ${r.error.message}`);
  if (r.status !== 0) stop(`recording the sim-run ${name} failed (exit ${r.status})`);
}
console.log(`[record] ${VIEWS.length} view(s) and ${RUNS.length} sim-run(s) recorded with ${python}`);
