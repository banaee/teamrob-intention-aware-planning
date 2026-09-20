#!/usr/bin/env python3
"""
check.py — T-B2c: one minimal-shift search per entry, checked on every ordering B3.B prices.

Runs scenario_81 (prior off and on; cost realized, gate none, stop off) in process, under
full_reorder AND under single_task, and records the inputs of every B3 call (the pool, the world,
the belief, the human projection). The single_task runs are there because the two strategies take
different courses through the scenario: under full_reorder no ordering priced on scenario_81 meets
the human at all, so the rows of that run alone would check nothing; single_task's course does (its
hold at step 39). At a single_task call the orderings are priced by this script only. Then, outside
the run, for EVERY ordering of the pool at EVERY call:

  1. DOMINANCE (check 8). The cost under one search per entry (shared/realization.realize(), as
     built) against the cost under ONE COMMON SHIFT, the realization before T-B2c: the violating
     shift intervals of every segment of every entry pooled, one minimal-shift search from 0, the
     whole plan shifted by its result. The common-shift realizer is `common_shift()` below — for
     this check only; it is not in shared/. Per-entry cost HIGHER than the common-shift cost is a
     defect (weak dominance holds in general: design_decisions.md, T-B Q2).
  2. THE HEAD'S HOLD (requirement 5). The hold before the first entry of the ordering's
     RealizedPlan against the hold of the head projected and realized ALONE, as single_task does.
     They must be equal for every ordering.

  2b. NOT VACUOUS: how many priced orderings carry a hold at all, how many carry one before a LATER
     entry (the case T-B2c adds), and in how many the first hold differs from the common shift (same
     cost, the hold taken at a different place). Every ordering with a hold before a later entry is
     also sampled as in 3 and 4.

And for the WINNING ordering of each call with an admitted projection:

  3. VALIDITY by an independent method (check 9), as F1's validate.py validated realize(): the
     realized segments and the human projection are sampled at DT ticks over the assessed window
     (where both exist, up to T_h). At each sample the robot is moving or not, and the distance d
     and its derivative are exact for the two constant-velocity segments in force. Rule (a): the
     previous sample had d >= s and this one d < s while the robot moves; rule (b): the robot
     moves with d < s and d' <= 0. Both counts must be 0.
  4. MINIMALITY per entry: for an entry with a hold > 0, the same sampling with that entry's
     cumulative shift one tick smaller (later entries unchanged) must find a violation. A miss at
     DT is reported, not failed.

  5. A SYNTHETIC UNIT CASE, literal segments, no scenario: two entries, the second conflicting with
     the human, the first carrying an interval the second's clearing shift falls into. It shows the
     mechanism (strict dominance, the hold taken before the second entry, validity); it is a check
     of the code, not a finding about any fixture.

Usage (repo root):
    PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python analysis/tb2c_per_entry_holds/check.py \
        > analysis/tb2c_per_entry_holds/checks.md
"""
import itertools, logging, math, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "mesa_sim"))
logging.disable(logging.CRITICAL)
import numpy as np
from mesa_sim.sim_model import SimModel
from domains.kitting.registry import domain_config
from shared.types import Var
from shared.realization import realize, _realized_segments, _EPS
from shared.trajectory_algorithms import shift_violation_interval

DT = 0.001
CONDS = [("env_layout8", "scenario_81", prior, strategy)
         for strategy in ("full_reorder", "single_task") for prior in (False, True)]
STEPS = 340


def item(task):
    return task.bindings[Var("?item")].value.split("_")[-1]


def common_shift(plan, human_plan, s):
    """(shift, cost) under ONE common shift: realize() as it was before T-B2c."""
    robot = [seg for e in plan.entries for seg in e.segments]
    human = [seg for e in human_plan.entries for seg in e.segments] if human_plan is not None else []
    T_r = robot[-1].end_step - robot[0].start_step
    intervals = []
    for r in robot:
        for h in human:
            iv = shift_violation_interval(r, h, s)
            if iv is not None and iv[1] > 0.0:
                intervals.append(iv)
    intervals.sort()
    delta = 0
    for lo, hi in intervals:
        if lo + _EPS < delta < hi - _EPS:
            delta = math.ceil(hi - _EPS)
        elif lo > delta + _EPS:
            break
    return delta, T_r + delta


def seg_state(segments, t):
    """(pos, vel, moving) of a head-to-tail chain at t; None outside its span. (F1's validate.py)"""
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


def sample(realized_segments, human_segments, s, t0, t_h):
    """(rule_a, rule_b, min distance while moving, samples) over the assessed window. (F1's validate.py)"""
    lo = max(t0, human_segments[0].start_step, realized_segments[0].start_step)
    hi = min(t_h, realized_segments[-1].end_step)
    if hi <= lo:
        return 0, 0, math.inf, 0
    a = b = n = 0; dmin = math.inf; prev_d = None
    for t in np.arange(lo, hi + DT / 2, DT):
        r = seg_state(realized_segments, t); h = seg_state(human_segments, t)
        if r is None or h is None:
            prev_d = None; continue
        (pr, vr, moving), (ph, vh, _) = r, h
        diff = pr - ph; d = float(np.hypot(*diff)); n += 1
        if moving:
            dmin = min(dmin, d)
            dd = float(diff @ (vr - vh)) / d if d > 0 else -1.0
            if d < s - 1e-9 and dd <= 1e-9: b += 1
            if prev_d is not None and prev_d >= s and d < s - 1e-9: a += 1
        prev_d = d
    return a, b, dmin, n


def run(layout_name, scenario_id, prior, strategy):
    layout = domain_config["layouts"][layout_name]
    m = SimModel(layout["scenarios"][scenario_id], domain_config["register_fn"], env_layout_path=layout["path"],
                 assignment_prior=prior, strategy=strategy, cost_strategy="realized", gate_strategy="none")
    robot = m.robots["robot_0"]; mp = robot.meta_planner
    calls = []
    inner = mp._replan_tasks

    def capture(**kw):
        result = inner(**kw)
        calls.append(dict(step=int(m.schedule.steps), trigger=mp._last_trigger_reason, pool=list(kw["task_pool"]),
                          belief=kw["belief"], world=kw["world"], against=kw["human_projection"], result=result))
        return result
    mp._replan_tasks = capture
    for _ in range(STEPS):
        m.step()
    return robot, calls


print("# T-B2c checks: one minimal-shift search per entry\n")
print(f"Generated by `check.py`. scenario_81, the B3 calls of the full_reorder run and of the single_task run; cost realized, gate none, stop off; "
      f"PYTHONHASHSEED=0; sampling step {DT} tick.\n")

totals = dict(orderings=0, admitted=0, differ=0, higher=0, head_mismatch=0, any_hold=0, later_hold=0, placed_elsewhere=0)
diff_rows, win_rows, later_rows = [], [], []
for layout_name, scenario_id, prior, strategy in CONDS:
    cond = f"s{scenario_id[-2:]}_{'on' if prior else 'off'} {'B3.B' if strategy == 'full_reorder' else 'B3.A'}"
    robot, calls = run(layout_name, scenario_id, prior, strategy)
    P, s = robot.projector, robot.meta_planner.min_separation
    for c in calls:
        pool, against = c["pool"], c["against"]
        best = None
        for indices in itertools.permutations(range(len(pool))):
            ordering = [pool[i] for i in indices]
            plan = P.project(ordering, c["world"], "robot_0", c["belief"], start_step=0.0)
            per_entry = realize(plan, against, s, 0.0)
            shift, common_cost = common_shift(plan, against, s)
            alone = realize(P.project(ordering[:1], c["world"], "robot_0", c["belief"], start_step=0.0), against, s, 0.0)
            totals["orderings"] += 1
            totals["admitted"] += against is not None
            if per_entry.holds[0] != alone.delta:
                totals["head_mismatch"] += 1
            if abs(per_entry.cost - common_cost) > 1e-9:
                totals["differ"] += 1
                totals["higher"] += per_entry.cost > common_cost + 1e-9
                diff_rows.append((cond, c["step"], c["trigger"], " ".join(item(t) for t in ordering),
                                  per_entry.holds, per_entry.cumulative_shifts, per_entry.cost, shift, common_cost))
            totals["any_hold"] += per_entry.cumulative_shifts[-1] > 0
            totals["placed_elsewhere"] += per_entry.holds[0] != shift
            if any(h > 0 for h in per_entry.holds[1:]):
                totals["later_hold"] += 1
                human = [seg for e in against.entries for seg in e.segments]
                a, b, dmin, n = sample(per_entry.segments, human, s, 0.0, per_entry.horizon)
                entries = [list(e.segments) for e in plan.entries]
                minimal = []
                for k, hold in enumerate(per_entry.holds):
                    if hold > 0:
                        shifts = list(per_entry.cumulative_shifts); shifts[k] -= 1
                        ma, mb, _, _ = sample(_realized_segments(entries, 0.0, shifts), human, s, 0.0, per_entry.horizon)
                        minimal.append(f"entry {k + 1}: {'violates' if ma + mb else 'NO VIOLATION FOUND'}")
                later_rows.append((cond, c["step"], c["trigger"], " ".join(item(t) for t in ordering), per_entry.holds,
                                   per_entry.cost, shift, common_cost, per_entry.horizon, a, b, dmin, "; ".join(minimal)))
            if best is None or per_entry.cost < best[0].cost:
                best = (per_entry, plan, ordering)
        if strategy != "full_reorder":
            continue
        realized, plan, ordering = best
        assert item(ordering[0]) == item(c["result"].current_task), "the script's winner is not the run's"
        row = dict(cond=cond, step=c["step"], trigger=c["trigger"], ordering=" ".join(item(t) for t in ordering),
                   holds=realized.holds, shift=realized.cumulative_shifts[-1], cost=realized.cost,
                   T_h=realized.horizon, share=realized.unassessed_share, sent=c["result"].hold)
        if against is not None:
            human = [seg for e in against.entries for seg in e.segments]
            row["a"], row["b"], row["dmin"], row["n"] = sample(realized.segments, human, s, 0.0, realized.horizon)
            entries = [list(e.segments) for e in plan.entries]
            minimal = []
            for k, hold in enumerate(realized.holds):
                if hold > 0:
                    shifts = list(realized.cumulative_shifts); shifts[k] -= 1
                    a, b, _, _ = sample(_realized_segments(entries, 0.0, shifts), human, s, 0.0, realized.horizon)
                    minimal.append(f"entry {k + 1}: {'violates' if a + b else 'NO VIOLATION FOUND'} at shift − 1")
            row["minimal"] = "; ".join(minimal) or "no hold"
        win_rows.append(row)

print("## 1. Dominance (check 8) and the head's hold (requirement 5): every ordering at every B3 call\n")
print(f"- orderings priced: {totals['orderings']} ({totals['admitted']} against an admitted human projection)")
print(f"- rows where the per-entry cost differs from the common-shift cost: {totals['differ']}")
print(f"- rows where the per-entry cost is HIGHER (a defect): {totals['higher']}")
print(f"- rows where the hold before the first entry differs from the head realized alone: {totals['head_mismatch']}\n")
print(f"- orderings with any hold: {totals['any_hold']}; with a hold before a LATER entry: {totals['later_hold']}; "
      f"where the first hold differs from the common shift (the hold is taken elsewhere): {totals['placed_elsewhere']}\n")
if later_rows:
    print("Orderings with a hold before a later entry, each sampled (rules a / b must be 0) and checked for minimality at shift − 1:\n")
    print("| cond | step | trigger | ordering | holds per entry | per-entry cost | common shift | common-shift cost | T_h | rule a | rule b | min d moving | minimality |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for cond, step, trig, o, holds, cost, shift, ccost, th, a, b, dmin, minimal in later_rows:
        print(f"| {cond} | {step} | {trig} | {o} | {holds} | {cost:.2f} | {shift} | {ccost:.2f} | {th:.2f} | {a} | {b} | {dmin:.2f} | {minimal} |")
    print()
if diff_rows:
    print("| cond | step | trigger | ordering | holds per entry | cumulative shifts | per-entry cost | common shift | common-shift cost | saved |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for cond, step, trig, o, holds, shifts, cost, shift, ccost in diff_rows:
        print(f"| {cond} | {step} | {trig} | {o} | {holds} | {shifts} | {cost:.2f} | {shift} | {ccost:.2f} | {ccost - cost:.2f} |")

print("\n## 2. The winning ordering of each B3 call of the full_reorder runs: validity (check 9) and minimality\n")
print("| cond | step | trigger | ordering | holds per entry | last cumulative shift | cost | T_h | share | hold sent | rule a | rule b | min d moving | samples | minimality |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in win_rows:
    th = "None" if r["T_h"] is None else f"{r['T_h']:.2f}"
    tail = (f"{r['a']} | {r['b']} | {r['dmin']:.2f} | {r['n']} | {r['minimal']}" if "a" in r
            else "– | – | – | – | no projection")
    print(f"| {r['cond']} | {r['step']} | {r['trigger']} | {r['ordering']} | {r['holds']} | {r['shift']} | "
          f"{r['cost']:.2f} | {th} | {r['share']:.2f} | {r['sent']} | {tail} |")
bad = [r for r in win_rows if r.get("a", 0) or r.get("b", 0)]
print(f"\n- winning orderings sampled against an admitted projection: {sum('a' in r for r in win_rows)}; "
      f"with a rule (a) or rule (b) sample: {len(bad)}")
DEFECTS = []
if not win_rows or not any("a" in r for r in win_rows):
    DEFECTS.append("no winning ordering was sampled: check 9 was not produced")
if bad:
    DEFECTS.append(f"{len(bad)} winning orderings have a violating sample")
if totals["higher"]:
    DEFECTS.append(f"{totals['higher']} orderings cost MORE per entry than under one common shift")
if totals["head_mismatch"]:
    DEFECTS.append(f"{totals['head_mismatch']} orderings whose first hold is not the head's, realized alone")
if any(a or b for *_, a, b, _dmin, _minimal in later_rows):
    DEFECTS.append("an ordering with a hold before a later entry has a violating sample")


# ---- 5. the synthetic unit case --------------------------------------------------------------
from shared.types import Segment, ProjectedPlan, ProjectedPlanEntry, AbstractPlan

def _entry(segments):
    return ProjectedPlanEntry(abstract_plan=AbstractPlan(goal_intention="unit", actions=[]),
                              estimated_start_step=int(segments[0].start_step), estimated_duration=0, segments=segments)

# Robot, out and back along y = 0 at 20 per tick: entry 1 walks (0,0) -> (200,0) over [0,10], entry 2 walks
# back (200,0) -> (0,0) over [10,20]. Human: comes down x = 100 fast, (100,400) -> (100,50) over [1,8],
# then slowly through the robot's line, (100,50) -> (100,-50) over [8,28] = T_h, within s of the line the
# whole time. Unshifted, entry 1 passes x = 100 before the human is near; entry 2 meets it. Entry 2 must
# wait until the window is over; a common shift of that size puts ENTRY 1 into the human as well, so
# the common shift is pushed further, by an interval entry 2's conflict never needed.
S_UNIT = 50.0
robot_plan = ProjectedPlan(task_queue=["e1", "e2"], total_estimated_cost=20, entries=[
    _entry([Segment((0.0, 0.0), 0.0, (200.0, 0.0), 10.0)]),
    _entry([Segment((200.0, 0.0), 10.0, (0.0, 0.0), 20.0)]),
])
human_plan = ProjectedPlan(task_queue=["h"], total_estimated_cost=28, entries=[_entry([
    Segment((100.0, 400.0), 1.0, (100.0, 50.0), 8.0),
    Segment((100.0, 50.0), 8.0, (100.0, -50.0), 28.0),
])])
unit = realize(robot_plan, human_plan, S_UNIT, 0.0)
u_shift, u_cost = common_shift(robot_plan, human_plan, S_UNIT)
human = [seg for e in human_plan.entries for seg in e.segments]
ua, ub, udmin, un = sample(unit.segments, human, S_UNIT, 0.0, unit.horizon)
print("\n## 3. Synthetic unit case (literal segments; a check of the code, not a finding)\n")
print("Robot, out and back along y = 0: entry 1 walks (0,0) -> (200,0) over [0,10], entry 2 back (200,0) -> (0,0) over "
      "[10,20]. Human: (100,400) -> (100,50) over [1,8], then slowly through the robot's line, (100,50) -> (100,-50) "
      "over [8,28] = T_h. s = 50.\n")
for k, e in enumerate(robot_plan.entries):
    ivs = sorted(iv for seg in e.segments for h in human
                 if (iv := shift_violation_interval(seg, h, S_UNIT)) is not None and iv[1] > 0.0)
    print(f"- entry {k + 1}: violating shift intervals {[(round(lo, 2), round(hi, 2)) for lo, hi in ivs]}")
print(f"- per entry: holds {unit.holds}, cumulative shifts {unit.cumulative_shifts}, cost {unit.cost:.2f}")
print(f"- one common shift: {u_shift}, cost {u_cost:.2f}; per-entry saves {u_cost - unit.cost:.2f}")
print(f"- realized segments: " + "; ".join(
    f"{'stand' if g.start_pos == g.end_pos else 'move'} [{g.start_step:g}, {g.end_step:g}] at/to ({g.end_pos[0]:g},{g.end_pos[1]:g})"
    for g in unit.segments))
print(f"- sampled: rule a {ua}, rule b {ub}, min distance while moving {udmin:.2f}, {un} samples")
one = realize(ProjectedPlan(task_queue=["e1"], total_estimated_cost=10, entries=robot_plan.entries[:1]), human_plan, S_UNIT, 0.0)
ca, cb, _, _ = sample(_realized_segments([list(e.segments) for e in robot_plan.entries], 0.0, [u_shift, u_shift]),
                      human, S_UNIT, 0.0, unit.horizon)
ma, mb, _, _ = sample(_realized_segments([list(e.segments) for e in robot_plan.entries], 0.0,
                                         [unit.cumulative_shifts[0], unit.cumulative_shifts[1] - 1]), human, S_UNIT, 0.0, unit.horizon)
print(f"- the common-shift realization sampled the same way: rule a {ca}, rule b {cb} (valid too, and dearer)")
print(f"- minimality: entry 2 at its cumulative shift − 1: rule a {ma}, rule b {mb} (must violate)")
print(f"- entry 1 realized alone: delta {one.delta} (the hold before the first entry above: {unit.holds[0]})")

print("\n## 4. Verdict\n")
print("- " + ("; ".join(DEFECTS) if DEFECTS else "no defect: dominance, the head's hold, validity of every winning ordering "
             "and of every ordering with a later hold all hold"))
if DEFECTS:
    sys.exit(1)
