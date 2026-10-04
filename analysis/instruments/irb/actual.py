#!/usr/bin/env python3
"""
actual.py — the recognizer's outputs per tick, for the IRB's comparison (IRB.3b), from two sources (the plan
step's option B, confirmed by Hadi):

  actual_log.csv  read from the run log with tdlib.py (analysis/instruments/common/, copied from the frozen
                  analysis/kitting/l_build/tdlib.py at the sort; since L-build; before it
                  analysis/td_stage1b/tdlib.py, frozen, which has no `[IR-reentry]`): `[IR]` (most_likely, confidence
                  to 3 decimals, lifecycle, finding, the members' tails to 4 decimals), `[IR-dist]` (the belief to 3
                  decimals), `[IR-complete]`, `[IR-reentry]`, `[IR-boundary]`, the human's lines (position to 2
                  decimals, micro); the live set on a tick is the support minus the keys retired then (T-D L4);
  actual.csv      the same run re-executed in-process from its run file, reading after every tick the robot's public
                  `BeliefState` at full precision (distribution, tails, hypothesis_adequacy, finding, lifecycle,
                  most_likely, confidence) and the world the robot built that tick (the human's position and facts).
                  Its `[IR*]` lines are asserted byte-identical to the logged run's, so it is the same run.

Since G-build: the observation warrant per hypothesis (`BeliefState.observation_warrant`; in the log, the `[IR]` line's
`warrant=[...]`, which is removed before tdlib reads the line and parsed here), and in actual.csv the gate's outcome
per tick, the robot's meta-planner's `_clears_gate` on that tick's BeliefState (the gate's one home; the idle robot of
the test-bed asks admission at tick 0 only, so its answer is read here, not from the log).

Since T-K part 1's gate stage (AM42): `belief_h`, the belief over H per hypothesis (`BeliefState.belief`, the value
`confidence` reports for the leader and the gate reads), in actual.csv only (the log carries the leader's value alone).

Nothing in the recognizer is read beyond its output. The columns the recognizer does not output are left empty in
both files and skipped by the comparison: expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

    actual.py <run file> <steps> <run.log> <actual.csv> <actual_log.csv>

The steps are the run's (run.sh computes them from the replay and runs with them); the layout is the run file's, or
the scenario's first reference layout when it names none; the observed human is the scenario's one human.
"""
import csv
import logging
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "mesa_sim"))
sys.path.insert(0, str(ROOT / "analysis" / "instruments" / "common"))

import yaml
import tdlib
from oracle import COLUMNS



def _write(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow({c: ("" if r.get(c) is None else repr(r[c]) if isinstance(r.get(c), float) else r[c])
                        for c in COLUMNS})


def support(keys, known, domain_config):
    """The support under the prior (docs/recognizer_handback.md §1.1): the known (assigned) tasks' hypotheses and every
    PersonalTask hypothesis of the task model; the log prints the known tasks with their determined parameters
    ([IR-assignment]; [IR-prior] before T-K part 1), the hypothesis keys without them. A key outside it is pinned at the floor and never live."""
    import re
    from shared.types import PersonalTask
    schemas = {s.name: s for s in domain_config["task_model"]}
    def key(task):
        m = re.match(r"(\w+)\((.*)\)$", task)
        det = schemas[m[1]].determined_parameters or {}
        return f"{m[1]}(" + ",".join(b for b in m[2].split(",") if b and b.split("=")[0] not in det) + ")"
    known_keys = {key(t) for t in known}
    return [k for k in keys if k in known_keys or isinstance(schemas[k.split("(")[0]], PersonalTask)]


WARRANT = re.compile(r"^\[IR\] step=(-?\d+) .* warrant=\[(.*)\]$")


def domain_of(run_file):
    """The run file's domain's registry: domains/<domain>/registry.py, the place every domain keeps it."""
    import importlib
    return importlib.import_module(f"domains.{yaml.safe_load(open(run_file))['domain']}.registry").domain_config


def from_log(log_path, alpha, domain_config):
    # tdlib's [coverage] pattern does not match a line with a `start:` entry (scenario_s08_03 / _04; TODO-125), so it
    # is handed the log without its [coverage] lines, which nothing here reads; and without the [IR] line's warrant
    # field (G-build), which its tails pattern would swallow: parsed here instead
    import tempfile
    warrant = {}
    with tempfile.NamedTemporaryFile("w", suffix=".log", delete=False) as f:
        for l in open(log_path):
            if l.startswith("[coverage]"):
                continue
            m = WARRANT.match(l.rstrip("\n"))
            if m:
                warrant[int(m[1])] = dict(e.rsplit("=", 1) for e in m[2].split("  ") if e)
                l = l[:l.rindex(" warrant=[")] + "\n"
            f.write(l)
    log = tdlib.parse(f.name)
    Path(f.name).unlink()
    keys = sorted(next(iter(log["dist"].values())))
    admissible = support(keys, log["known"], domain_config)
    rows = []
    for t in sorted(log["ir"]):
        ir, dist = log["ir"][t], log["dist"][t]
        pins = [k for s, k in log["pins"] if s == t]
        reentries = [k for s, k in log["reentries"] if s == t]
        live = [k for k in admissible if not tdlib.retired(log, k, t) and not tdlib.inapplicable(log, k, t)]
        act, micro, (x, y), _ = log["human"][t]
        common = dict(tick=t, human_x=x, human_y=y, micro=None if micro == "None" else micro,
                      most_likely=None if ir["ml"] == "none" else ir["ml"], confidence=ir["conf"],
                      finding=ir["finding"], lifecycle=ir["lifecycle"], pins=";".join(sorted(pins)),
                      reentries=";".join(sorted(reentries)), boundary=int(t in log["boundary"]))
        if not live:
            rows.append(common)
        for k in live:
            S = ir["tails"].get(k)
            adequacy = "no_observation" if S is None else ("adequate" if S >= alpha else "inadequate")
            rows.append(dict(common, key=k, belief=dist[k], S=S, member=int(S is not None), adequacy=adequacy,
                             warrant=warrant[t][k]))
    return rows


class Collect(logging.Handler):
    def __init__(self):
        super().__init__()
        self.lines = []

    def emit(self, record):
        self.lines.append(record.getMessage())


def in_process(run_file, steps, alpha):
    domain_config = domain_of(run_file)
    from mesa_sim.sim_model import SimModel
    from mesa_sim.world_state_builder import build_world_state
    cfg = yaml.safe_load(open(run_file))
    scenario = domain_config["scenarios"][cfg["scenario"]]
    layout = cfg.get("layout") or scenario.reference_layouts[0]
    H = next(a for a in scenario.agents if a.agent_type == "human").agent_id
    collect = Collect()
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(collect)
    logging.getLogger("rec").propagate = False
    m = SimModel(scenario=scenario, register_fn=domain_config["register_fn"],
                 state_declarations=domain_config["states"],
                 task_model_schemas=domain_config["task_model"],
                 layout_path=domain_config["layouts"][layout],
                 setup_path=domain_config["setups"][scenario.setup],
                 assignment_knowledge=bool(cfg["assignment_knowledge"]), strategy=cfg["strategy"],
                 gate_strategy=cfg["gate_strategy"], cost_strategy=cfg["cost_strategy"],
                 separation_stop=bool(cfg["separation_stop"]), test_level=float(cfg["test_level"]),
                 context_knowledge=bool(cfg["context_knowledge"]))
    robot = next(iter(m.robots.values()))
    human = m.humans[H]
    rows = []
    for t in range(steps):
        n0 = len(collect.lines)
        m.step()
        b = robot.belief
        new = collect.lines[n0:]
        pins = sorted(l.split()[2] for l in new if l.startswith("[IR-complete]"))
        reentries = sorted(l.split()[2] for l in new if l.startswith("[IR-reentry]"))
        world = build_world_state(m)
        facts = world.predicates
        at = sorted(p.args[1].value for p in facts if p.name == "at" and p.args[0].value == H)
        waited = next((p.args[1].value for p in facts if p.name == "waited" and p.args[0].value == H), None)
        common = dict(tick=t, human_x=float(human.pos[0]), human_y=float(human.pos[1]),
                      micro=human.current_microaction, holding=human.carrying, waited=waited,
                      obj_at=";".join(f"{i}@{l}" for i, l in sorted(world.object_locations.items())),
                      at=";".join(at), most_likely=b.most_likely, confidence=b.confidence,
                      finding=None if b.finding is None else b.finding.value, lifecycle=b.lifecycle.value,
                      pins=";".join(pins), reentries=";".join(reentries),
                      boundary=int(any(l.startswith("[IR-boundary]") for l in new)),
                      gate=robot.meta_planner._clears_gate(b).value)
        live = sorted(b.hypothesis_adequacy)
        if not live:
            rows.append(common)
        for k in live:
            S = b.tails.get(k)
            rows.append(dict(common, key=k, belief=b.distribution[k], belief_h=b.belief[k], S=S, member=int(S is not None),
                             adequacy=b.hypothesis_adequacy[k].value, warrant=b.observation_warrant[k].value))
    root.removeHandler(collect)
    return rows, [l for l in collect.lines if l.startswith("[IR")]


if __name__ == "__main__":
    run_file, steps, log_path, out_full, out_log = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5]
    alpha = float(yaml.safe_load(open(run_file))["test_level"])
    _write(out_log, from_log(log_path, alpha, domain_of(run_file)))
    rows, ir_lines = in_process(run_file, steps, alpha)
    logged = [l.rstrip("\n") for l in open(log_path) if l.startswith("[IR")]
    same = ir_lines == logged
    print(f"{run_file}: in-process [IR*] lines {'byte-identical to' if same else 'DIFFER from'} the logged run's "
          f"({len(ir_lines)} lines)")
    assert same, "the in-process run is not the logged run"
    _write(out_full, rows)
