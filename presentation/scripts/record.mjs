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
// The sim-runs replayed on slides (scripts/record_run.py): [name, existing run file, first tick, last tick].
const TF1 = "configs/kitting/tf1/measurement";
const RUNS = [
  ["stage1_alone", `${TF1}/scenario_s12_02/run_061.yaml`, 0, 136],        // human-unaware
  ["stage2_reactive", `${TF1}/scenario_s10_02/run_006.yaml`, 24, 52],     // intention-unaware
  ["stage3_switch", `${TF1}/scenario_s12_01/run_060.yaml`, 0, 62],
  ["stage4_break", `${TF1}/scenario_s24_14/run_264.yaml`, 85, 150],
  ["stage5_breaktime", `${TF1}/scenario_s23_03/run_576.yaml`, 0, 62],
  ["stage6_switch", `${TF1}/scenario_s23_23/run_584.yaml`, 30, 100],
  ["stage7_stand", `${TF1}/scenario_s10_07/run_028.yaml`, 40, 125],
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
