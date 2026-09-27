#!/usr/bin/env python3
"""
actual.py — the recognizer's outputs per tick, for the IR test-bed's comparison (TB.3b), from two sources (the plan
step's option B, confirmed by Hadi):

  actual_log.csv  read from the run log with analysis/td_stage1b/tdlib.py: `[IR]` (most_likely, confidence to 3
                  decimals, lifecycle, finding, the members' tails to 4 decimals), `[IR-dist]` (the belief to 3
                  decimals), `[IR-complete]`, `[IR-boundary]`, the human's lines (position to 2 decimals, micro);
  actual.csv      the same run re-executed in-process from its run file, reading after every tick the robot's public
                  `BeliefState` at full precision (distribution, tails, hypothesis_adequacy, finding, lifecycle,
                  most_likely, confidence) and the world the robot built that tick (the human's position and facts).
                  Its `[IR*]` lines are asserted byte-identical to the logged run's, so it is the same run.

Nothing in the recognizer is read beyond its output. The columns the recognizer does not output are left empty in
both files and skipped by the comparison: expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

    actual.py <run file> <run.log> <actual.csv> <actual_log.csv>
"""
import csv
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "mesa_sim"))
sys.path.insert(0, str(ROOT / "analysis" / "td_stage1b"))

import yaml
import tdlib
from oracle import COLUMNS

H = "human_0"


def _write(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow({c: ("" if r.get(c) is None else repr(r[c]) if isinstance(r.get(c), float) else r[c])
                        for c in COLUMNS})


def from_log(log_path, alpha):
    # tdlib's [coverage] pattern does not match a line with a `start:` entry (scenario_s08_03 / _04); tdlib is a
    # frozen record, so it is handed the log without its [coverage] lines, which nothing here reads
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".log", delete=False) as f:
        f.writelines(l for l in open(log_path) if not l.startswith("[coverage]"))
    log = tdlib.parse(f.name)
    Path(f.name).unlink()
    keys = sorted(next(iter(log["dist"].values())))
    rows = []
    for t in sorted(log["ir"]):
        ir, dist = log["ir"][t], log["dist"][t]
        pins = [k for k, s in log["complete"].items() if s == t]
        live = [k for k in keys if not (k in log["complete"] and log["complete"][k] <= t)]
        act, micro, (x, y), _ = log["human"][t]
        common = dict(tick=t, human_x=x, human_y=y, micro=None if micro == "None" else micro,
                      most_likely=None if ir["ml"] == "none" else ir["ml"], confidence=ir["conf"],
                      finding=ir["finding"], lifecycle=ir["lifecycle"], pins=";".join(sorted(pins)),
                      boundary=int(t in log["boundary"]))
        if not live:
            rows.append(common)
        for k in live:
            S = ir["tails"].get(k)
            adequacy = "no_observation" if S is None else ("adequate" if S >= alpha else "inadequate")
            rows.append(dict(common, key=k, belief=dist[k], S=S, member=int(S is not None), adequacy=adequacy))
    return rows


class Collect(logging.Handler):
    def __init__(self):
        super().__init__()
        self.lines = []

    def emit(self, record):
        self.lines.append(record.getMessage())


def in_process(run_file, alpha):
    from domains.kitting.registry import domain_config, register_kitting_domain
    from mesa_sim.sim_model import SimModel
    from mesa_sim.world_state_builder import build_world_state
    cfg = yaml.safe_load(open(run_file))
    scenario = domain_config["scenarios"][cfg["scenario"]]
    collect = Collect()
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(collect)
    logging.getLogger("rec").propagate = False
    m = SimModel(scenario=scenario, register_fn=register_kitting_domain,
                 task_model_schemas=domain_config["task_model"],
                 layout_path=domain_config["layouts"][cfg["layout"]],
                 setup_path=domain_config["setups"][scenario.setup],
                 assignment_prior=bool(cfg["assignment_prior"]), strategy=cfg["strategy"],
                 gate_strategy=cfg["gate_strategy"], cost_strategy=cfg["cost_strategy"],
                 separation_stop=bool(cfg["separation_stop"]), test_level=float(cfg["test_level"]))
    robot = next(iter(m.robots.values()))
    human = m.humans[H]
    rows = []
    for t in range(int(cfg["steps"])):
        n0 = len(collect.lines)
        m.step()
        b = robot.belief
        new = collect.lines[n0:]
        pins = sorted(l.split()[2] for l in new if l.startswith("[IR-complete]"))
        world = build_world_state(m)
        facts = world.predicates
        at = sorted(p.args[1].value for p in facts if p.name == "at" and p.args[0].value == H)
        waited = next((p.args[1].value for p in facts if p.name == "waited" and p.args[0].value == H), None)
        common = dict(tick=t, human_x=float(human.pos[0]), human_y=float(human.pos[1]),
                      micro=human.current_microaction, holding=human.carrying, waited=waited,
                      obj_at=";".join(f"{i}@{l}" for i, l in sorted(world.object_locations.items())),
                      at=";".join(at), most_likely=b.most_likely, confidence=b.confidence,
                      finding=None if b.finding is None else b.finding.value, lifecycle=b.lifecycle.value,
                      pins=";".join(pins), boundary=int(any(l.startswith("[IR-boundary]") for l in new)))
        live = sorted(b.hypothesis_adequacy)
        if not live:
            rows.append(common)
        for k in live:
            S = b.tails.get(k)
            rows.append(dict(common, key=k, belief=b.distribution[k], S=S, member=int(S is not None),
                             adequacy=b.hypothesis_adequacy[k].value))
    root.removeHandler(collect)
    return rows, [l for l in collect.lines if l.startswith("[IR")]


if __name__ == "__main__":
    run_file, log_path, out_full, out_log = sys.argv[1:5]
    alpha = float(yaml.safe_load(open(run_file))["test_level"])
    _write(out_log, from_log(log_path, alpha))
    rows, ir_lines = in_process(run_file, alpha)
    logged = [l.rstrip("\n") for l in open(log_path) if l.startswith("[IR")]
    same = ir_lines == logged
    print(f"{run_file}: in-process [IR*] lines {'byte-identical to' if same else 'DIFFER from'} the logged run's "
          f"({len(ir_lines)} lines)")
    assert same, "the in-process run is not the logged run"
    _write(out_full, rows)
