#!/usr/bin/env python3
"""
validate.py — F1: every realized trajectory checked independently against robot-responsible
separation, and compared with the T10 (joint-state) realizer on the same inputs.

Runs the eight conditions (scenario_00/10/20/30 × prior off/on; cost realized, gate none) in
process, recording every realize() call B3 makes (the robot plan, the human projection,
min_separation, the decision step, the RealizedPlan). Then, per call with an admitted projection:

  1. RULE CHECK at the returned δ. The realized trajectory (hold, then the shifted plan) and the
     human projection are sampled at DT ticks over the assessed window (where both exist, up to
     T_h). At each sample the robot is moving or not (its segment's endpoints differ), the distance
     d and its derivative d' = (R − Q)·(v_r − v_h)/d are exact for the two constant-velocity
     segments in force. A sample violates rule (a) when the previous sample had d ≥ s and this one
     has d < s while the robot moves; rule (b) when the robot moves with d < s and d' ≤ 0. Both
     counts must be 0.
  2. MINIMALITY. For δ > 0 the same check at δ − 1 must find at least one violation (δ is the
     smallest whole tick outside every violating shift interval). A miss at DT is reported, not
     failed.
  3. AGAINST T10. The T10 realizer (commit 08b1167: joint-state violation, hold-position check,
     hold cap) is run on the same inputs from a copy extracted with `git show`. Reported: how many
     rows it called unrealizable and with which reason, and that the F1 δ never exceeds the T10 δ
     where both realized (F1's violating set is a subset of T10's).

Usage (repo root):  PYTHONHASHSEED=0 python analysis/f1_robot_responsible/validate.py > validation.md
"""
import logging, math, subprocess, sys, importlib.util, types as pytypes
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "mesa_sim"))
logging.disable(logging.CRITICAL)
import numpy as np
from mesa_sim.sim_model import SimModel
from domains.kitting.registry import domain_config
import shared.meta_planner as MP
from shared.types import Segment
from shared.realization import realize as realize_f1

DT = 0.001
S = 50.0
CONDS = [("env_layout0", "scenario_00", 300), ("env_layout1", "scenario_10", 450),
         ("env_layout2", "scenario_20", 300), ("env_layout3", "scenario_30", 200)]

# ---- the T10 realizer, extracted from git into a scratch package ----------------------------
def load_old():
    d = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "analysis/f1_robot_responsible/_t10_realizer"
    d.mkdir(parents=True, exist_ok=True)
    (d / "__init__.py").write_text("")
    for name in ("realization.py", "trajectory_algorithms.py"):
        src = subprocess.check_output(["git", "show", f"08b1167:shared/{name}"], cwd=ROOT, text=True)
        src = src.replace("from shared.trajectory_algorithms import", "from _t10_realizer.trajectory_algorithms import")
        src = src.replace("from shared.types import ProjectedPlan, RealizedPlan, Segment", "from _t10_realizer.types import ProjectedPlan, RealizedPlan, Segment")
        (d / name).write_text(src)
    types_src = subprocess.check_output(["git", "show", "08b1167:shared/types.py"], cwd=ROOT, text=True)
    i = types_src.index("@dataclass\nclass RealizedPlan:"); j = types_src.index("@dataclass\nclass ConflictPoint:")
    (d / "types.py").write_text("from dataclasses import dataclass\nfrom typing import List, Optional, Tuple\n"
                                "from shared.types import ProjectedPlan, Segment\n\n" + types_src[i:j])
    sys.path.insert(0, str(d.parent))
    import _t10_realizer.realization as old
    return old.realize

# ---- sampling geometry ------------------------------------------------------------------------
def seg_state(segments, t):
    """(pos, vel, moving) of a head-to-tail chain at t; None outside its span."""
    for sg in segments:
        if sg.start_step - 1e-12 <= t <= sg.end_step + 1e-12:
            L = sg.end_step - sg.start_step
            if L <= 0:
                return np.array(sg.start_pos, float), np.zeros(2), False
            f = (t - sg.start_step) / L
            p0, p1 = np.array(sg.start_pos, float), np.array(sg.end_pos, float)
            v = (p1 - p0) / L
            return p0 + f * (p1 - p0), v, bool(np.any(p1 != p0))
    return None

def check(realized_segments, human_segments, s, t0, t_h):
    """(rule_a, rule_b, min_dist_while_moving, samples) over the assessed window."""
    lo = max(t0, human_segments[0].start_step, realized_segments[0].start_step)
    hi = min(t_h, realized_segments[-1].end_step)
    if hi <= lo: return 0, 0, math.inf, 0
    a = b = n = 0; dmin = math.inf; prev_d = None
    for t in np.arange(lo, hi + DT / 2, DT):
        r = seg_state(realized_segments, t); h = seg_state(human_segments, t)
        if r is None or h is None: prev_d = None; continue
        (pr, vr, moving), (ph, vh, _) = r, h
        diff = pr - ph; d = float(np.hypot(*diff)); n += 1
        if moving:
            dmin = min(dmin, d)
            dd = float(diff @ (vr - vh)) / d if d > 0 else -1.0
            if d < s - 1e-9 and dd <= 1e-9: b += 1
            if prev_d is not None and prev_d >= s and d < s - 1e-9: a += 1
        prev_d = d
    return a, b, dmin, n

def shifted(plan_segments, hold_pos, t0, delta):
    out = []
    if plan_segments[0].start_step + delta - t0 > 0:
        out.append(Segment(start_pos=hold_pos, start_step=t0, end_pos=hold_pos, end_step=plan_segments[0].start_step + delta))
    for sg in plan_segments:
        out.append(Segment(start_pos=sg.start_pos, start_step=sg.start_step + delta, end_pos=sg.end_pos, end_step=sg.end_step + delta))
    return out

# ---- capture ----------------------------------------------------------------------------------
records = []
def capturing(plan, human_plan, min_separation, decision_step):
    r = realize_f1(plan, human_plan, min_separation, decision_step)
    records.append(dict(cond=CUR, step=STEP[0], plan=plan, human=human_plan, s=min_separation, t0=decision_step, r=r))
    return r
MP.realize = capturing
_orig_update = MP.MetaPlanner.update
STEP = [None]

realize_old = load_old()
rows = []
for lay, sc, steps in CONDS:
    for prior in (False, True):
        CUR = f"{sc.replace('scenario_', 's')}_{'on' if prior else 'off'}"
        L = domain_config["layouts"][lay]
        model = SimModel(scenario=L["scenarios"][sc], register_fn=domain_config["register_fn"],
                         env_layout_path=L["path"], assignment_prior=prior, gate_strategy="none", cost_strategy="realized")
        for k in range(steps):
            STEP[0] = k
            model.step()

for rec in records:
    r, hp = rec["r"], rec["human"]
    if hp is None or not any(e.segments for e in hp.entries):
        continue
    human_segments = [sg for e in hp.entries for sg in e.segments]
    plan_segments = [sg for e in rec["plan"].entries for sg in e.segments]
    t_h = human_segments[-1].end_step
    a, b, dmin, n = check(r.segments, human_segments, rec["s"], rec["t0"], t_h)
    if r.delta > 0:
        a1, b1, _, _ = check(shifted(plan_segments, r.hold_position, rec["t0"], r.delta - 1), human_segments, rec["s"], rec["t0"], t_h)
        minimal = "yes" if a1 + b1 > 0 else "NOT CONFIRMED"
    else:
        minimal = "n/a (δ=0)"
    old = realize_old(rec["plan"], hp, rec["s"], rec["t0"])
    old_delta = old.delta if old.realizable else None
    rows.append(dict(cond=rec["cond"], step=rec["step"], task=rec["plan"].task_queue[0],
                     T_r=r.projected_duration, T_h=t_h, delta=r.delta, cost=r.cost, share=r.unassessed_share,
                     a=a, b=b, dmin=dmin, n=n, minimal=minimal, old=("realized" if old.realizable else old.reason), old_delta=old_delta))

def short(k): return k.replace("deliver_item(?item=", "").split(",")[0]
print("# F1 — realize() under robot-responsible separation, validated (eight conditions, s = 50 cm)\n")
print(f"Generated by `validate.py`. Cost realized, gate none; PYTHONHASHSEED=0; sampling step {DT} tick. "
      "Rows: every B3 realize() call with an admitted human projection. a / b: rule (a) / rule (b) violation samples "
      "in the realized trajectory over the assessed window (must be 0); min moving: the smallest robot–human distance "
      "while the robot moves within the window (may be below s only while the distance increases); minimal: δ−1 violates; "
      "T10: what the T10 realizer (joint-state violation, hold-position check, hold cap) returned on the same inputs.\n")
tot = len(rows); viol = sum(1 for x in rows if x["a"] + x["b"] > 0); held = sum(1 for x in rows if x["delta"] > 0)
notmin = sum(1 for x in rows if x["minimal"] == "NOT CONFIRMED")
old_unreal = [x for x in rows if x["old"] != "realized"]
delta_up = [x for x in rows if x["old_delta"] is not None and x["delta"] > x["old_delta"]]
delta_down = [x for x in rows if x["old_delta"] is not None and x["delta"] < x["old_delta"]]
below_s_moving = [x for x in rows if x["dmin"] < S]
print("## Summary\n")
print(f"- rows: {tot}; held (δ > 0): {held}; rows with any rule (a)/(b) violation: {viol}; minimality not confirmed: {notmin}")
print(f"- rows where the robot moves within s during the window (distance increasing, allowed): {len(below_s_moving)}")
old_list = ", ".join("%s %s %s %s" % (x["cond"], x["step"], short(x["task"]), x["old"]) for x in old_unreal) or "none"
print(f"- T10 realizer on the same inputs: unrealizable {len(old_unreal)} ({old_list})")
print(f"- F1 δ vs T10 δ where both realized: smaller in {len(delta_down)}, larger in {len(delta_up)} (must be 0), equal otherwise")
for x in delta_up: print(f"  - LARGER: {x['cond']} {x['step']} {short(x['task'])} F1 δ={x['delta']} T10 δ={x['old_delta']}")
print()
print("## Rows\n")
print("| condition | step | candidate | T_r | T_h | δ | cost | share | a | b | min moving | minimal | T10 | T10 δ |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for x in rows:
    dmin_s = "—" if x["dmin"] == math.inf else "%.2f" % x["dmin"]
    print(f"| {x['cond']} | {x['step']} | {short(x['task'])} | {x['T_r']:.2f} | {x['T_h']:.2f} | {x['delta']} | {x['cost']:.2f} | {x['share']:.2f} | "
          f"{x['a']} | {x['b']} | {dmin_s} | {x['minimal']} | {x['old']} | {x['old_delta'] if x['old_delta'] is not None else '—'} |")
