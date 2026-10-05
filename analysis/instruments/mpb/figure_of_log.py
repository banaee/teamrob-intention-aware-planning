#!/usr/bin/env python3
"""
figure_of_log.py <run.log> <figure.png> — the per-tick figure of a run made by run_mesa.py directly (the four maintained
sets' sweep.sh, dock_loading's milestone runs), which no instrument ran (the measurement of T-F part 1, O: every test
and analysis run has its figure; Hadi, 5 October 2026).

The run is read from its own log: the triple and the steps from the `[run_mesa]` start line, the settings from the
`[run]` header (effective values; `human_aware` and `intention_aware` on where a log predates them). From them a run file
is written in a temporary folder, and the planning test-bed's own steps run on it there: the human's replay
(analysis/instruments/irb/trajectory.py; not for a script that depends on the robot, whose replay with an idle robot does
not describe the run), the in-process actual (actual.py, which asserts the in-process run is the logged run), and the
figure (plot.py), over the whole run (the horizon set to the run's steps). No oracle table: the actual values alone.
Only the figure is kept.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
IR = ROOT / "analysis" / "instruments" / "irb"
PY = sys.executable


def run_file_of(log):
    start = next(l for l in open(log) if l.startswith("[run_mesa] Starting"))
    s = dict(re.findall(r"(\w+)=(\S+)", start))
    h = dict(re.findall(r"(\w+)=(\S+)", next(l for l in open(log) if l.startswith("[run] "))))
    on = lambda k: h.get(k, "on") == "on"
    return dict(domain=s["domain"], layout=s["layout"], setup=s["setup"], scenario=s["scenario"],
                steps=int(s["steps"]), assignment_knowledge=on("assignment_knowledge"),
                context_knowledge=on("context_knowledge"), strategy=h["strategy"], gate_strategy=h["gate_strategy"],
                cost_strategy=h["cost_strategy"], separation_stop=on("separation_stop"),
                test_level=float(h["test_level"]), human_aware=on("human_aware"),
                intention_aware=on("intention_aware"))


def depends_on_robot(cfg):
    sys.path[:0] = [str(IR), str(ROOT)]
    import trajectory
    sc = trajectory.domain_of(cfg)["scenarios"][yaml.safe_load(open(cfg))["scenario"]]
    return next(a for a in sc.agents if a.agent_type == "human").scheduled_tasks.dependence.value == "on_robot"


def main(log, png):
    log, png = Path(log).resolve(), Path(png).resolve()
    cfg = run_file_of(log)
    env = dict(PYTHONHASHSEED="0")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        run = tmp / "run.yaml"
        yaml.safe_dump(cfg, open(run, "w"), sort_keys=False)
        steps = str(cfg["steps"])
        if depends_on_robot(run):
            traj = dict(scenario=cfg["scenario"], layout=cfg["layout"], actions=[])
            json.dump(traj, open(tmp / "trajectory.json", "w"))
        else:
            subprocess.run([PY, IR / "trajectory.py", run, steps, tmp / "trajectory.json"], cwd=ROOT, env=env,
                           check=True, capture_output=True)
        # the human's last acknowledgement from the run's own human lines (as run_set.sh for a dependent script)
        hid = next(l.split()[2] for l in open(log) if re.match(r"\s*step: \d+: \[human", l))
        last = max((int(l.split()[1].rstrip(":")) for l in open(log)
                    if re.match(r"\s*step: \d+: ", l) and l.split()[2] == hid and l.split()[4] != "action=None"),
                   default=0)
        subprocess.run([PY, HERE / "actual.py", run, steps, log, str(last), tmp], cwd=ROOT, env=env, check=True,
                       capture_output=True)
        obs = json.load(open(tmp / "observed.json"))
        obs["horizon"] = cfg["steps"]                      # the figure over the whole run
        json.dump(obs, open(tmp / "observed.json", "w"))
        subprocess.run([PY, HERE / "plot.py", cfg["scenario"], tmp, log], cwd=ROOT, env=env, check=True,
                       capture_output=True)
        png.write_bytes((tmp / "figure.png").read_bytes())


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
