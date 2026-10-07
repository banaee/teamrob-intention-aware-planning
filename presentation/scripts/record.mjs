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

const VIEWS = [["kitting", "env_layout_01"]];     // [domain, layout], one per data file a slide reads

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
if (!existsSync(python)) stop(`no Python interpreter at ${python}`);
for (const [domain, layout] of VIEWS) {
  const run = spawnSync(python, [resolve(here, "record_view.py"), domain, layout], {
    cwd: repo, env: { ...process.env, PYTHONHASHSEED: "0" }, stdio: "inherit",
  });
  if (run.error) stop(`${python} could not be started: ${run.error.message}`);
  if (run.status !== 0) stop(`recording ${domain} ${layout} failed (exit ${run.status})`);
}
console.log(`[record] ${VIEWS.length} view(s) recorded with ${python}`);
