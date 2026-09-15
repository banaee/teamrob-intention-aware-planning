"""
analysis/t3_realize/validate.py  (T3 — validation of shared/realization.realize())

Runs the eight test-set conditions (T3b: scenario_00 on env_layout0,
scenario_10 on env_layout1, scenario_20 on env_layout2, scenario_30 on
env_layout3; assignment prior off and on; the L2 baselines' step counts) with
T1b's instance-level
wrappers (analysis/t1b_realization/measure.py: shared/ untouched, no decision
changed), which record at every fired trigger the human projection and every
candidate projection B3 built. Then, at every ADMITTED trigger
(projection=built), for every candidate:

  1. realize()  — shared/realization.py, min_separation 50 cm, decision step 0
     (the step every candidate projection starts at: _replan_tasks projects
     with start_step=0.0).
  2. T1b's analysis realizer `whole` (analysis/t1b_realization/realize.py,
     realize_whole): T1's single shift, smallest δ on a 0.01-tick grid,
     strict horizon rule. Its inputs are the same Segment dicts realize()'s
     ProjectedPlans are rebuilt from. Adaptations, and only these:
       - none to the geometry: it reads segments as they are, so L2's
         stationary latency segments and the human's start at the
         observation offset (1.0) pass straight through; its hold starts at
         0.0, which is the decision step here;
       - the HOLD CAP (R1, decided after T1b): `whole` reports a shift that
         reaches T_h as realized with `shift_past_horizon=True`; here such a
         row counts as UNREALIZABLE, which is what the cap says.
     Agreement, with realize()'s δ in WHOLE ticks (T3b) and `whole`'s on a
     0.01 grid: realizability; δ; cost = T_r + δ. Rows are classified:
       identical      — same realizability, δ equal (both 0, or whole's δ is
                        already a whole tick within the grid), cost equal;
       quantisation   — both realizable, realize()'s δ is the first whole
                        tick at or above whole's δ (ceil), cost differs by
                        exactly that;
       quant:skip     — both realizable, realize()'s δ is LARGER than
                        ceil(whole's δ): that whole tick sits inside a later
                        violating interval (non-monotone feasibility), so the
                        walk continued;
       quant:cap/hold — whole realizes at a fractional δ but the whole-tick
                        δ reaches T_h or the hold bound, so realize() reports
                        unrealizable;
       DISAGREE       — anything else.
  3. Independent checks of realize()'s realized trajectory (hold + shifted
     segments) against the human projection over the assessed window:
       (a) T1b's closed-form per-pair minimum (segment_clear / hold_clear) at
           exactly realize()'s δ — a different derivation (minimum over the
           window for a fixed shift) of the same geometry;
       (b) dense sampling of the robot–human distance at 0.001 tick over
           [0, T_h] wherever both chains exist (the hold is in the chain): the
           minimum must not be below 50 cm.
  4. Per trigger: the candidate realization would select (argmin realized
     cost; all unrealizable → plain-cost argmin, R1) next to the logged winner
     and the plain-cost argmin. Information only.

Also checks that the instrumented logs equal the L2 baselines
(analysis/l2_execution_lag/new/) minus the [sep] lines, so the projections
realized here are the baselines'.

Usage (PYTHONHASHSEED=0 is mandatory, TODO-42):
    PYTHONHASHSEED=0 python analysis/t3_realize/validate.py
Writes captures.json and logs_instrumented/ (git-ignored) and validation.md.
"""
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "mesa_sim"))
sys.path.insert(0, str(ROOT / "analysis" / "t1b_realization"))

import measure as M                                   # noqa: E402  T1b's capture wrappers
import realize as R                                   # noqa: E402  T1b's analysis realizer
from shared.realization import realize                # noqa: E402
from shared.types import (                            # noqa: E402
    AbstractPlan, ProjectedPlan, ProjectedPlanEntry, Segment,
)

CONDITIONS = [
    ("s00_off", "env_layout0", "scenario_00", 300, False),
    ("s00_on",  "env_layout0", "scenario_00", 300, True),
    ("s10_off", "env_layout1", "scenario_10", 450, False),
    ("s10_on",  "env_layout1", "scenario_10", 450, True),
    ("s20_off", "env_layout2", "scenario_20", 200, False),
    ("s20_on",  "env_layout2", "scenario_20", 200, True),
    ("s30_off", "env_layout3", "scenario_30", 200, False),
    ("s30_on",  "env_layout3", "scenario_30", 200, True),
]
BASELINES = ROOT / "analysis" / "l2_execution_lag" / "new"
S = 50.0            # min_separation, cm (2.5 × 20 cm motion per tick, R1)
DECISION = 0.0      # every candidate projection starts at step 0
GRID = R.GRID       # whole's δ grid, 0.01 tick
SAMPLE_DT = 0.001   # dense sampling step for check (b)


def short(task):
    return task.split("=")[1].split(",")[0] if "?item=" in task else task.split("(")[0]


def to_plan(d):
    """Segment dicts (measure.py's plan_to_dict) -> a ProjectedPlan realize() reads."""
    segs = [Segment(tuple(s["start_pos"]), s["start_step"], tuple(s["end_pos"]), s["end_step"])
            for s in d["segments"]]
    entry = ProjectedPlanEntry(
        abstract_plan=AbstractPlan(goal_intention=d["task_queue"][0], actions=[]),
        estimated_start_step=int(segs[0].start_step),
        estimated_duration=d["estimated_duration"],
        segments=segs,
    )
    return ProjectedPlan(task_queue=list(d["task_queue"]), entries=[entry],
                         total_estimated_cost=d["total_estimated_cost"])


def baseline_identity(name):
    """Instrumented log == baseline minus [sep] lines?"""
    inst = (HERE / "logs_instrumented" / f"{name}.log").read_text().splitlines()
    base = [ln for ln in (BASELINES / f"{name}.log").read_text().splitlines()
            if not ln.startswith("[sep]")]
    return inst == base


def t1b_exact_check(rplan_dict, hplan_dict, delta):
    """T1b's closed form at exactly delta: hold at P0 over [0, delta] and every segment shifted."""
    rs, hs = R.segs(rplan_dict), R.segs(hplan_dict)
    tp = np.array([delta])
    ok = bool(R.hold_clear(rs[0].P0, 0.0, tp, hs, S)[0])
    for r in rs:
        ok &= bool(R.segment_clear(r.P0, r.v, r.a + tp, r.D, hs, S)[0])
    return ok


def sampled_check(realized_segments, hplan_dict):
    """Min sampled robot–human distance over [0, T_h] where both chains exist."""
    chain = [R.Seg({"start_pos": list(s.start_pos), "end_pos": list(s.end_pos),
                    "start_step": s.start_step, "end_step": s.end_step})
             for s in realized_segments]
    hs = R.segs(hplan_dict)
    T_h = R.horizon(hs)
    return R.sampled_min_distance(chain, hs, T_h, dt=SAMPLE_DT)


def fmt(x, nd=2):
    return "–" if x is None else f"{x:.{nd}f}"


def main():
    if os.environ.get("PYTHONHASHSEED") != "0":
        sys.exit("Run with PYTHONHASHSEED=0 (TODO-42).")

    captures = {"conditions": []}
    for cond in CONDITIONS:
        print(f"running {cond[0]} ...", flush=True)
        captures["conditions"].append(M.run_condition(*cond, out_dir=HERE))
    with open(HERE / "captures.json", "w") as f:
        json.dump(captures, f, indent=1)

    identity = {c[0]: baseline_identity(c[0]) for c in CONDITIONS}

    rows, triggers = [], []
    for cond in captures["conditions"]:
        cname = cond["name"]
        for tr in cond["triggers"]:
            if not tr.get("fired") or tr.get("projection_reason") != "built":
                continue
            hdict = tr["human_projection"]
            hplan = to_plan(hdict)
            T_h = hdict["segments"][-1]["end_step"]
            trig_rows = []
            for cand in tr["candidates"]:
                rdict = cand["projection"]
                res = realize(to_plan(rdict), hplan, S, DECISION)
                wh = R.realize_whole(rdict, hdict, S)
                wh_ok = wh["status"] == "realized" and not wh["shift_past_horizon"]
                wh_delta = wh["delta"] if wh_ok else None
                wh_cost = wh["end"] if wh_ok else None
                wh_note = ("shift_past_horizon" if wh["status"] == "realized" and not wh_ok
                           else wh["status"])
                # classification against `whole` (fractional δ on a 0.01 grid)
                if res.realizable and wh_ok:
                    ceil_wh = math.ceil(wh_delta - GRID - 1e-9)      # first whole tick at/above whole's δ
                    cost_gap_ok = abs((res.cost - wh_cost) - (res.delta - wh_delta)) <= 1e-6
                    if res.delta == ceil_wh and abs(res.delta - wh_delta) <= GRID + 1e-9 and cost_gap_ok:
                        cls = "identical"
                    elif res.delta == ceil_wh and cost_gap_ok:
                        cls = "quantisation"
                    elif res.delta > ceil_wh and cost_gap_ok:
                        cls = "quant:skip"
                    else:
                        cls = "DISAGREE"
                elif (not res.realizable) and (not wh_ok):
                    cls = "identical"
                elif wh_ok and not res.realizable and res.reason in ("hold_reaches_horizon", "hold_position_violated"):
                    cls = "quant:cap/hold"
                else:
                    cls = "DISAGREE"
                agree_r = (res.realizable == wh_ok)
                agree_d = cls == "identical"
                agree_c = cls == "identical"
                exact_ok = t1b_exact_check(rdict, hdict, res.delta) if res.realizable else None
                smin, sarg = sampled_check(res.segments, hdict) if res.realizable else (None, None)
                sampled_ok = (smin >= S - 1e-6) if smin is not None else None
                row = {
                    "condition": cname, "step": tr["step"], "trigger": tr["trigger"],
                    "candidate": cand["task"], "current": cand["is_current_task"],
                    "T_r": res.projected_duration, "T_h": T_h, "plain_cost": cand["cost"],
                    "logged_feasible": cand.get("logged_feasible"),
                    "realizable": res.realizable, "delta": res.delta, "cost": res.cost,
                    "share": res.unassessed_share, "reason": res.reason,
                    "wh_realizable": wh_ok, "wh_delta": wh_delta, "wh_cost": wh_cost,
                    "wh_note": wh_note,
                    "agree": cls != "DISAGREE", "cls": cls,
                    "agree_r": agree_r, "agree_d": agree_d, "agree_c": agree_c,
                    "exact_ok": exact_ok, "sampled_min": smin, "sampled_at": sarg,
                    "sampled_ok": sampled_ok,
                }
                rows.append(row)
                trig_rows.append(row)
            realized = [r for r in trig_rows if r["realizable"]]
            plain_winner = min(trig_rows, key=lambda r: r["plain_cost"])["candidate"]
            if realized:
                sel = min(realized, key=lambda r: r["cost"])["candidate"]
                how = "realized argmin"
            else:
                sel = plain_winner
                how = "all_unrealizable → plain cost"
            triggers.append({
                "condition": cname, "step": tr["step"], "trigger": tr["trigger"],
                "pool": trig_rows, "logged": tr["winner"], "plain": plain_winner,
                "selected": sel, "how": how,
            })

    # ---- validation.md -----------------------------------------------------
    out = []
    out.append("# T3b — realize() (whole-tick δ) validated against T1b's `whole` realizer (eight conditions, s = 50 cm)\n")
    out.append("Generated by `validate.py`. Conditions: s00, s10, s20, s30 × prior off/on, the L2 baselines' step "
               "counts, PYTHONHASHSEED=0. Units: ticks; distances cm. δ = the hold (realize(): whole ticks; whole: "
               "0.01 grid); T_r = projected duration (segment span); T_h = end of the human projection; share = "
               "unassessed share. Row classes: see the script docstring.\n")
    out.append("## Baseline identity (instrumented log == L2 baseline minus `[sep]`)\n")
    out.append("| condition | identical |\n|---|---|")
    for k, v in identity.items():
        out.append(f"| {k} | {'yes' if v else 'NO'} |")
    n = len(rows)
    n_ag = sum(r["agree"] for r in rows)
    n_real = sum(r["realizable"] for r in rows)
    n_held = sum(1 for r in rows if r["realizable"] and r["delta"] > 0)
    n_ex = sum(1 for r in rows if r["exact_ok"] is True)
    n_sm = sum(1 for r in rows if r["sampled_ok"] is True)
    out.append(f"\n## Summary\n\n- rows (admitted trigger × candidate): {n}; triggers: {len(triggers)}")
    out.append(f"- realize(): realizable {n_real}, of which held (δ > 0) {n_held}; unrealizable {n - n_real}")
    from collections import Counter
    cc = Counter(r["cls"] for r in rows)
    out.append(f"- agreement with `whole` (no unexplained difference): {n_ag} of {n}; classes: "
               + ", ".join(f"{k} {v}" for k, v in sorted(cc.items())))
    out.append(f"- realizability agrees with `whole`: {sum(r['agree_r'] for r in rows)} of {n}")
    out.append(f"- per condition: " + "; ".join(
        f"{c[0]} rows {sum(r['condition'] == c[0] for r in rows)}, held {sum(r['condition'] == c[0] and r['realizable'] and r['delta'] > 0 for r in rows)}, "
        f"unrealizable {sum(r['condition'] == c[0] and not r['realizable'] for r in rows)}" for c in CONDITIONS))
    out.append(f"- independent checks on realized rows: T1b closed form at δ clear {n_ex} of {n_real}; "
               f"sampled min distance ≥ 50 cm {n_sm} of {n_real}")
    worst = min((r["sampled_min"] for r in rows if r["sampled_min"] is not None), default=None)
    out.append(f"- smallest sampled min distance over realized rows: {fmt(worst, 4)} cm")
    out.append("\n## Rows\n")
    out.append("| condition | step | trigger | candidate | current | T_r | T_h | realize | δ | cost | share "
               "| whole | whole δ | class | closed-form check | sampled min (at) |")
    out.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        out.append(
            f"| {r['condition']} | {r['step']} | {r['trigger']} | {short(r['candidate'])} | "
            f"{'yes' if r['current'] else ''} | {r['T_r']:.2f} | {r['T_h']:.2f} | {r['reason']} | "
            f"{'–' if r['delta'] is None else r['delta']} | {fmt(r['cost'])} | {fmt(r['share'])} | {r['wh_note']} | "
            f"{fmt(r['wh_delta'])} | {r['cls']} | "
            f"{'clear' if r['exact_ok'] else ('–' if r['exact_ok'] is None else 'VIOLATED')} | "
            f"{fmt(r['sampled_min'])}{'' if r['sampled_at'] is None else f' ({r[chr(115)+chr(97)+chr(109)+chr(112)+chr(108)+chr(101)+chr(100)+chr(95)+chr(97)+chr(116)]:.2f})'} |")
    dis = [r for r in rows if r["cls"] != "identical"]
    out.append("\n## Differences from `whole` (all rows not classed identical)\n")
    if not dis:
        out.append("none")
    for r in dis:
        out.append(f"- {r['cls']}: {r['condition']} {r['step']} {short(r['candidate'])}: realize {r['reason']} "
                   f"δ={fmt(r['delta'])} cost={fmt(r['cost'])}; whole {r['wh_note']} "
                   f"δ={fmt(r['wh_delta'])} cost={fmt(r['wh_cost'])}")
    out.append("\n## Selection per trigger (information only)\n")
    out.append("| condition | step | trigger | pool: candidate (plain cost → realized cost) | logged winner "
               "| plain-cost argmin | realization would select | how |")
    out.append("|---|---|---|---|---|---|---|---|")
    for t in triggers:
        pool = "; ".join(
            f"{short(r['candidate'])} ({r['plain_cost']} → {fmt(r['cost']) if r['realizable'] else r['reason']})"
            for r in t["pool"])
        flag = "" if t["selected"] == t["logged"] else " **≠ logged**"
        out.append(f"| {t['condition']} | {t['step']} | {t['trigger']} | {pool} | {short(t['logged'])} | "
                   f"{short(t['plain'])} | {short(t['selected'])}{flag} | {t['how']} |")
    (HERE / "validation.md").write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
