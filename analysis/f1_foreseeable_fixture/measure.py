"""
analysis/f1_foreseeable_fixture/measure.py  — baseline belief traces for scenario_40.

Runs env_layout4 / scenario_40 headless with assignment_prior off and on
(PYTHONHASHSEED=0), reads the robot's BeliefState after every tick (no wrappers,
nothing inside shared/ is touched or patched), labels every tick with the
human's actual segment (script index + executor action — analysis-side ground
truth the robot never sees), and writes:

  trace_<cond>.csv      one row per tick: step, segment, human state, belief
  segments_<cond>.csv   one row per (segment, human action): step range and what
                        the recognizer did there
  angles.csv            bearings / angular separations computed from the layout
  summary.md            the segment tables as markdown

Also checks the run's log is byte-identical to run_mesa.py's own log for the
same condition (the per-step lines are replicated exactly, as in T1/I1).

    PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python analysis/f1_foreseeable_fixture/measure.py
"""

import csv
import json
import logging
import math
import os
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "mesa_sim"))

from mesa_sim.sim_model import SimModel                     # noqa: E402
from domains.kitting.registry import domain_config          # noqa: E402
from shared.types import task_instance_key                  # noqa: E402

HERE = Path(__file__).parent
LAYOUT, SCENARIO, STEPS = "env_layout4", "scenario_40", 400
THETA = 0.75   # MetaPlanner default; read back from the live instance below and asserted

SEGMENT_NAMES = {0: "seg1_deliver_item_3", 1: "seg2_coffee", 2: "seg3a_toward_shelf_6",
                 3: "seg3b_turn_away", 4: "seg4_deliver_item_6"}


def short(key):
    if key.startswith("deliver_item("):
        for part in key[len("deliver_item("):-1].split(","):
            k, v = part.split("=")
            if k == "?item":
                return v
    return key.split("(")[0]


def run(prior):
    name = f"s40_{'on' if prior else 'off'}"
    lay = domain_config["layouts"][LAYOUT]
    scen = lay["scenarios"][SCENARIO]
    log_path = HERE / "logs_instrumented" / f"{name}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)
    fh = logging.FileHandler(log_path, mode="w")
    fh.setFormatter(logging.Formatter("%(message)s"))
    root.addHandler(fh)
    root.setLevel(logging.INFO)
    logging.info(f"[run_mesa] Starting headless run — domain=kitting scenario={SCENARIO} steps={STEPS}")

    model = SimModel(scenario=scen, register_fn=domain_config["register_fn"],
                     env_layout_path=lay["path"], assignment_prior=prior)
    robot = model.robots["robot_0"]
    human = model.humans["human_0"]
    assert robot.meta_planner._theta == THETA
    hyps = [repr(h) for h in robot.recognizer._hypotheses] + ["unknown"]

    rows = []
    for step in range(STEPS):
        model.step()
        for aid, h in model.humans.items():
            logging.info(f"  step: {step}: [{aid}] task={h.current_task} action={h.current_action} "
                         f"micro={h.current_microaction} pos={np.round(h.pos, 2)}")
        for aid, r in model.robots.items():
            logging.info(f"  step: {step}: [{aid}] task={r.current_task} action={r.current_action} "
                         f"micro={r.current_microaction} pos={np.round(r.pos, 2)}")
        b = robot.belief
        ti = human.get_current_task_instance()
        row = {
            "step": step,
            "segment": SEGMENT_NAMES.get(human.script_index, "done") if not human.finished else "done",
            "human_task": task_instance_key(ti) if ti else "",
            "human_action": human.current_action or "",
            "human_action_index": human.executor.action_index,
            "human_micro": human.current_microaction or "",
            "human_x": round(human.pos[0], 1), "human_y": round(human.pos[1], 1),
            "human_holding": human.carrying or "",
            "robot_task": robot.current_task or "", "robot_holding": robot.carrying or "",
            "ir_called": b is not None and int(b.timestamp) == step,
            "most_likely": short(b.most_likely) if b else "",
            "confidence": round(b.confidence, 4) if b else "",
        }
        for k in hyps:
            row[f"p_{short(k)}"] = round(b.distribution.get(k, float("nan")), 4) if b else ""
        rows.append(row)
    logging.info("[run_mesa] Headless run complete.")
    fh.flush()

    with open(HERE / f"trace_{name}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    return name, rows, hyps


def segment_table(name, rows, hyps):
    """Per (segment, human action) block: step range and what the belief did."""
    out = []
    blocks = []
    for r in rows:
        key = (r["segment"], r["human_task"], r["human_action"])
        if blocks and blocks[-1]["key"] == key:
            blocks[-1]["rows"].append(r)
        else:
            blocks.append({"key": key, "rows": [r]})
    pcols = [f"p_{short(k)}" for k in hyps]
    for b in blocks:
        rs = [r for r in b["rows"] if r["ir_called"]]
        if not rs:
            continue
        seg, task, action = b["key"]
        first, last = rs[0], rs[-1]
        conf_max = max(rs, key=lambda r: r["confidence"])
        above = [r for r in rs if r["confidence"] >= THETA]
        deliver_above = sorted({r["most_likely"] for r in above if r["most_likely"].startswith("item_")})
        coffee_max = max(r["p_coffee_break"] for r in rs)
        unknown_min = min(r["p_unknown"] for r in rs)
        unknown_max = max(r["p_unknown"] for r in rs)
        winners = []
        for r in rs:
            if not winners or winners[-1][0] != r["most_likely"]:
                winners.append((r["most_likely"], r["step"]))
        out.append([name, seg, short(task) if task else "-", action or "-", first["step"], last["step"], len(rs),
                    first["most_likely"], first["confidence"], last["most_likely"], last["confidence"],
                    conf_max["most_likely"], conf_max["confidence"], conf_max["step"],
                    len(above), ",".join(deliver_above) or "-",
                    coffee_max, unknown_min, unknown_max,
                    " > ".join(f"{w}@{s}" for w, s in winners)])
    return out


def angles():
    d = json.load(open(ROOT / "domains" / "kitting" / "env_layout4.json"))
    P = {o["id"]: tuple(o["position"]) for o in d["env_objects"] if "position" in o}
    for o in d["env_objects"]:
        if "initial_container" in o:
            P[o["id"]] = P[o["initial_container"]]

    def bearing(a, b):
        return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))

    def sep(x, y):
        dd = abs(x - y) % 360
        return min(dd, 360 - dd)

    targets = ["shelf_3", "shelf_6", "shelf_4", "shelf_7", "shelf_5", "kitting_table_0", "coffee_machine_0", "ac_switch_0"]
    legs = [("seg1", "human_start", (100, 550), "shelf_3"),
            ("seg2", "kitting_table_0", P["kitting_table_0"], "coffee_machine_0"),
            ("seg3a", "coffee_machine_0", P["coffee_machine_0"], "wander_0"),
            ("seg3b", "wander_0", P["wander_0"], "wander_1"),
            ("seg4", "wander_1", P["wander_1"], "shelf_6")]
    rows = []
    for seg, oname, origin, dest in legs:
        b = bearing(origin, P[dest])
        for t in targets:
            if t == dest or t == oname:
                continue
            bt = bearing(origin, P[t])
            rows.append([seg, oname, dest, round(b, 1), round(math.dist(origin, P[dest])), t, round(bt, 1),
                         round(sep(b, bt), 1), round(math.dist(origin, P[t]))])
    with open(HERE / "angles.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["segment", "origin", "destination", "bearing_deg", "length_cm", "target", "target_bearing_deg",
                    "separation_deg", "target_dist_cm"])
        w.writerows(rows)
    return rows


def main():
    if os.environ.get("PYTHONHASHSEED") != "0":
        sys.exit("Run with PYTHONHASHSEED=0 (TODO-42).")
    header = ["condition", "segment", "human_task", "human_action", "first_step", "last_step", "ir_ticks",
              "most_likely_first", "conf_first", "most_likely_last", "conf_last",
              "most_likely_at_max", "conf_max", "step_of_max", "ticks_at_or_above_theta",
              "deliver_item_above_theta", "p_coffee_max", "p_unknown_min", "p_unknown_max", "winner_sequence"]
    all_rows = []
    for prior in (False, True):
        name, rows, hyps = run(prior)
        seg_rows = segment_table(name, rows, hyps)
        with open(HERE / f"segments_{name}.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(seg_rows)
        all_rows.append((name, seg_rows))
        print(f"{name}: {sum(1 for r in rows if r['ir_called'])} IR ticks, human finished at "
              f"{next((r['step'] for r in rows if r['segment'] == 'done'), None)}", file=sys.stderr)
    ang = angles()
    with open(HERE / "summary.md", "w") as f:
        f.write("# Auto-generated tables (measure.py)\n\n")
        for name, seg_rows in all_rows:
            f.write(f"## Segments — {name}\n\n| " + " | ".join(header) + " |\n|" + "---|" * len(header) + "\n")
            for r in seg_rows:
                f.write("| " + " | ".join(str(v) for v in r) + " |\n")
            f.write("\n")
        f.write("## Angles\n\n| segment | origin | destination | bearing | length | target | target bearing | separation | target dist |\n|---|---|---|---|---|---|---|---|---|\n")
        for r in ang:
            f.write("| " + " | ".join(str(v) for v in r) + " |\n")


if __name__ == "__main__":
    main()
