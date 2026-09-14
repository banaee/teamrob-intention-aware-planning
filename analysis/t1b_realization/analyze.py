"""
analysis/t1b_realization/analyze.py  (T1b — measurement only)

captures.json -> every table in this directory. One ROW is one (condition,
trigger, candidate); every row is realized at every separation in SEPARATIONS
by the three realizers in realize.py (greedy = the design loop, exact = same
per-segment policy at its minimal hold, whole = T1's single shift).

Row classes (never pooled):
  primary        the trigger's human projection was ADMITTED (projection=built)
  counterfactual NOT admitted (below theta); realized against a projection of
                 that tick's below-theta most_likely, built after update()
  none           no projection possible (most_likely = unknown)
Tags: hyp_matches_actual (projected hypothesis == the human's actual scripted
task at that tick; False when the human has finished its script), degenerate
(projected human path < 30 cm, T1's rule).

Usage: python analysis/t1b_realization/analyze.py
"""
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import realize as R  # noqa: E402

SEPARATIONS = [5, 10, 20, 30, 40, 50, 75, 100, 150, 200, 300, 400, 600]
DEGENERATE_PATH_CM = 30.0
PROXIMITY_THRESHOLD = 30.0   # mesa_sim/world_state_builder.py: executor "at" rule, cm


def short(task):
    return task.split("=")[1].split(",")[0] if "?item=" in task else task.split("(")[0]


def path_len(plan):
    return sum(math.dist(s["start_pos"], s["end_pos"]) for s in plan["segments"])


def tail_min_distance(traj, hs):
    """Min distance, for tau >= T_h, between the realized robot chain and the
    human's FINAL projected position (T1's 'human held at its end')."""
    T_h = R.horizon(hs)
    Q = hs[-1].P1
    best = math.inf
    for c in traj:
        lo, hi = max(c.a, T_h), c.b
        if hi - lo <= R.EPS:
            continue
        A = c.P0 - c.v * c.a - Q
        bb = float(c.v @ c.v)
        if bb < 1e-12:
            d2 = float(A @ A)
        else:
            ts = min(max(-(A @ c.v) / bb, lo), hi)
            r = A + c.v * ts
            d2 = float(r @ r)
        best = min(best, math.sqrt(max(d2, 0.0)))
    return best


def held_end_plan(hplan, extra):
    """The human projection with a stationary segment appended at its final
    position for `extra` ticks: T1's 'human held at its end' variant."""
    last = hplan["segments"][-1]
    ext = dict(hplan)
    ext["segments"] = list(hplan["segments"]) + [{"start_pos": last["end_pos"], "end_pos": last["end_pos"],
                                                  "start_step": last["end_step"], "end_step": last["end_step"] + extra}]
    ext["actions"] = list(hplan["actions"]) + [{"action": "held_at_end", "phase": "held_at_end"}]
    return ext


def tail_lead(traj, hs, s):
    """Ticks after T_h until the realized robot chain first comes within s of the
    human's FINAL projected position; None if it never does."""
    T_h = R.horizon(hs)
    Q = hs[-1].P1
    best = None
    for c in traj:
        lo, hi = max(c.a, T_h), c.b
        if hi - lo <= R.EPS:
            continue
        iv = R.pair_violation(c.P0, c.v, c.a, c.D, R.Seg({"start_pos": Q.tolist(), "end_pos": Q.tolist(),
                                                          "start_step": lo, "end_step": hi}), s)
        if iv is not None:
            best = iv[0] - T_h
            break
    return best


def unassessed(T_r, delta, T_h):
    end = T_r + delta
    ticks = max(0.0, end - T_h)
    return ticks, ticks / end if end > 0 else 0.0


def hold_str(holds, rplan, hplan):
    parts = []
    for (i, dt, P, t0, t1) in holds:
        parts.append(f"seg{i}:{rplan['actions'][i]['phase']}:{dt:.2f}t@{t0:.1f}"
                     f"[human:{R.phase_at(hplan, t0)}]")
    return ";".join(parts)


def main():
    C = json.load(open(HERE / "captures.json"))

    rows = []           # row-level tags
    real = []           # row x separation
    checks = {"first_violation_max_abs_diff": 0.0, "first_violation_n": 0,
              "first_violation_n_bad": 0, "sampled_min_d_below_s": 0, "sampled_n": 0,
              "sampled_worst_margin": math.inf,
              "grid_exact_max_abs_diff": 0.0, "grid_whole_max_abs_diff": 0.0,
              "grid_status_mismatch": 0, "grid_n": 0,
              "pool_order_argmin_matches_log": 0, "pool_order_argmin_mismatch": 0,
              "one_segment_per_action_violations": 0}
    triggers = []       # per (condition, trigger)

    for cond in C["conditions"]:
        cname = cond["name"]
        for tr in cond["triggers"]:
            if not tr.get("candidates"):
                continue
            admitted = tr.get("projection_reason") == "built"
            hplan = tr.get("human_projection") if admitted else tr.get("counterfactual_human_projection")
            if admitted:
                rclass = "primary"
            elif hplan is not None:
                rclass = "counterfactual"
            else:
                rclass = "none"
            hyp = tr.get("most_likely")
            actual = tr.get("human_actual_task")
            match = (actual is not None and hyp == actual)
            degenerate = (hplan is not None and path_len(hplan) < DEGENERATE_PATH_CM)
            T_h = hplan["segments"][-1]["end_step"] if hplan else None
            trig = {"condition": cname, "layout": cond["layout"], "step": tr["step"],
                    "trigger": tr["trigger"], "row_class": rclass, "admitted": admitted,
                    "hypothesis": hyp, "human_actual": actual, "hyp_matches_actual": match,
                    "human_finished": actual is None, "degenerate": degenerate,
                    "confidence": tr.get("confidence"), "T_h": T_h,
                    "robot_current_task": tr.get("robot_current_task"),
                    "robot_holding": tr.get("robot_holding"),
                    "pool_size": len(tr["candidates"]),
                    "current_in_pool": any(c["is_current_task"] for c in tr["candidates"]),
                    "cost_winner_logged": tr["winner"],
                    "cost_winner": min(tr["candidates"], key=lambda c: c["cost"])["task"]}
            # sanity: the logged winner is the pool-order argmin of int cost, except
            # where the superseded min_safe_distance=1.0 exclusion removed the cheapest
            am = trig["cost_winner"]
            if am == tr["winner"]:
                checks["pool_order_argmin_matches_log"] += 1
            else:
                checks["pool_order_argmin_mismatch"] += 1

            per_s = {s: [] for s in SEPARATIONS}
            for cand in tr["candidates"]:
                rplan = cand["projection"]
                if not rplan["one_segment_per_action"]:
                    checks["one_segment_per_action_violations"] += 1
                T_r = rplan["segments"][-1]["end_step"]
                row = dict(trig)
                row.update({"candidate": cand["task"], "cand": short(cand["task"]),
                            "is_current_task": cand["is_current_task"], "cost": cand["cost"],
                            "T_r": T_r, "n_segments": rplan["n_segments"],
                            "phases": "|".join(a["phase"] for a in rplan["actions"]),
                            "logged_feasible": cand.get("logged_feasible"),
                            "logged_min_dist": cand.get("logged_min_dist"),
                            "unassessed_before_ticks": (max(0.0, T_r - T_h) if T_h else None),
                            "unassessed_before_share": (max(0.0, T_r - T_h) / T_r if T_h else None)})
                rows.append(row)
                if hplan is None:
                    continue
                hs = R.segs(hplan)
                for s in SEPARATIONS:
                    trace = []
                    g = R.realize_greedy(rplan, hplan, s, trace=trace)
                    lit = R.realize_greedy(rplan, hplan, s, mode="literal")
                    ex = R.realize_exact(rplan, hplan, s)
                    wh = R.realize_whole(rplan, hplan, s)

                    # ---- checks: closed form vs sampling ---------------------
                    for it in trace:
                        sf = R.sampled_first_violation(it["P0"], it["v"], it["t"], it["D"], hs, s)
                        checks["first_violation_n"] += 1
                        if sf is None:
                            checks["first_violation_n_bad"] += 1
                        else:
                            diff = abs(sf - it["start"])
                            checks["first_violation_max_abs_diff"] = max(checks["first_violation_max_abs_diff"], diff)
                            if diff > 0.0100001:
                                checks["first_violation_n_bad"] += 1
                    for res in (g, ex):
                        if res["status"] == "realized":
                            traj = R.realized_trajectory(rplan, res)
                            md, _ = R.sampled_min_distance(traj, hs, min(res["end"], T_h))
                            checks["sampled_n"] += 1
                            checks["sampled_worst_margin"] = min(checks["sampled_worst_margin"], md - s)
                            if md < s - 1e-6:
                                checks["sampled_min_d_below_s"] += 1
                    if wh["status"] == "realized":
                        d = wh["delta"]
                        traj = [R.Seg({"start_pos": rplan["segments"][0]["start_pos"], "end_pos": rplan["segments"][0]["start_pos"],
                                       "start_step": 0.0, "end_step": d})] + \
                               [R.Seg({"start_pos": sg["start_pos"], "end_pos": sg["end_pos"],
                                       "start_step": sg["start_step"] + d, "end_step": sg["end_step"] + d}) for sg in rplan["segments"]]
                        md, _ = R.sampled_min_distance(traj, hs, min(wh["end"], T_h))
                        checks["sampled_n"] += 1
                        checks["sampled_worst_margin"] = min(checks["sampled_worst_margin"], md - s)
                        if md < s - 1e-6:
                            checks["sampled_min_d_below_s"] += 1
                    # ---- checks: grid resolution -----------------------------
                    for grid in (0.05, 0.002):
                        ex2 = R.realize_exact(rplan, hplan, s, grid=grid)
                        wh2 = R.realize_whole(rplan, hplan, s, grid=grid)
                        checks["grid_n"] += 1
                        if ex2["status"] != ex["status"] or wh2["status"] != wh["status"]:
                            checks["grid_status_mismatch"] += 1
                        if ex2["delta"] is not None and ex["delta"] is not None:
                            checks["grid_exact_max_abs_diff"] = max(checks["grid_exact_max_abs_diff"], abs(ex2["delta"] - ex["delta"]))
                        if wh2["delta"] is not None and wh["delta"] is not None:
                            checks["grid_whole_max_abs_diff"] = max(checks["grid_whole_max_abs_diff"], abs(wh2["delta"] - wh["delta"]))

                    # ---- tail (T1's human-held-at-end) --------------------------
                    unheld = R.segs(rplan)
                    tail_before = tail_min_distance(unheld, hs)
                    lead_before = tail_lead(unheld, hs, s)
                    lead_g = tail_lead(R.realized_trajectory(rplan, g), hs, s) if g["status"] == "realized" else None
                    lead_e = tail_lead(R.realized_trajectory(rplan, ex), hs, s) if ex["status"] == "realized" else None
                    lead_w = tail_lead(traj, hs, s) if wh["status"] == "realized" else None
                    # human held at its final position, holds capped at the ORIGINAL horizon (T1's
                    # delta_ext_human_held_at_end): realizable here = clear without relying on the tail
                    hplan_held = held_end_plan(hplan, T_r + T_h + 10.0)
                    g_held = R.realize_greedy(rplan, hplan_held, s, t_max=T_h)
                    ex_held = R.realize_exact(rplan, hplan_held, s, grid=0.05, t_max=T_h)
                    wh_held = R.realize_whole(rplan, hplan_held, s, grid=0.05, t_max=T_h)

                    fv = g["first_violation"]
                    ua_after = unassessed(T_r, g["delta"], T_h) if g["status"] == "realized" else (None, None)
                    ua_before = unassessed(T_r, 0.0, T_h)
                    rec = {k: row[k] for k in ("condition", "layout", "step", "trigger", "row_class", "admitted",
                                                "hyp_matches_actual", "human_finished", "degenerate", "candidate", "cand",
                                                "is_current_task", "robot_holding", "cost", "T_r", "T_h", "pool_size")}
                    rec.update({
                        "s": s,
                        "g_status": g["status"], "g_delta": g["delta"],
                        "g_delta_frac": (g["delta"] / T_r if g["delta"] is not None else None),
                        "g_delta_partial": g["delta_partial"],
                        "g_realized_cost": (T_r + g["delta"] if g["delta"] is not None else None),
                        "g_n_iter": g["n_iter"], "g_n_segment_end_truncations": g["n_segment_end_truncations"],
                        "g_fail_segment": g["fail_segment"],
                        "g_fail_phase": (rplan["actions"][g["fail_segment"]]["phase"] if g["fail_segment"] is not None else None),
                        "g_holds": hold_str(g["holds"], rplan, hplan),
                        "g_n_holds": len(g["holds"]),
                        "first_violation_t": (fv["t"] if fv else None),
                        "first_violation_segment": (fv["segment"] if fv else None),
                        "first_violation_robot_phase": (rplan["actions"][fv["segment"]]["phase"] if fv else None),
                        "first_violation_human_phase": (R.phase_at(hplan, fv["t"]) if fv else None),
                        "unassessed_before_ticks": ua_before[0], "unassessed_before_share": ua_before[1],
                        "unassessed_after_ticks": ua_after[0], "unassessed_after_share": ua_after[1],
                        "unassessed_widening_ticks": (ua_after[0] - ua_before[0] if ua_after[0] is not None else None),
                        "tail_min_d_before": tail_before, "tail_lead_before": lead_before,
                        "g_tail_lead": lead_g, "g_held_end_status": g_held["status"], "g_held_end_delta": g_held["delta"],
                        "g_clears_via_tail": (g["status"] == "realized" and g["delta"] > 1e-9 and g_held["status"] != "realized"),
                        "lit_status": lit["status"], "lit_delta": lit["delta_partial"], "lit_outlasts": lit["outlasts_horizon"],
                        "lit_realized_cost": (T_r + lit["delta_partial"] if lit["status"] in ("realized",) or lit["outlasts_horizon"] else None),
                        "ex_status": ex["status"], "ex_delta": ex["delta"],
                        "ex_realized_cost": (T_r + ex["delta"] if ex["delta"] is not None else None),
                        "ex_holds": hold_str(ex["holds"], rplan, hplan), "ex_fail_segment": ex["fail_segment"],
                        "ex_fail_phase": (rplan["actions"][ex["fail_segment"]]["phase"] if ex["fail_segment"] is not None else None),
                        "ex_tail_lead": lead_e, "ex_held_end_status": ex_held["status"], "ex_held_end_delta": ex_held["delta"],
                        "ex_clears_via_tail": (ex["status"] == "realized" and ex["delta"] > 1e-9 and ex_held["status"] != "realized"),
                        "wh_status": wh["status"], "wh_delta": wh["delta"],
                        "wh_realized_cost": (T_r + wh["delta"] if wh["delta"] is not None else None),
                        "wh_tail_lead": lead_w, "wh_held_end_status": wh_held["status"], "wh_held_end_delta": wh_held["delta"],
                        "wh_clears_via_tail": (wh["status"] == "realized" and wh["delta"] > 1e-9 and wh_held["status"] != "realized"),
                        "wh_shift_past_horizon": wh.get("shift_past_horizon"),
                    })
                    real.append(rec)
                    per_s[s].append(rec)

            if hplan is None:
                triggers.append(dict(trig, s=None))
                continue
            for s in SEPARATIONS:
                recs = per_s[s]
                t = dict(trig, s=s)

                def argmin(key_status, key_cost):
                    ok = [r for r in recs if r[key_status] == "realized"]
                    if not ok:
                        return None, 0
                    return min(ok, key=lambda r: r[key_cost])["candidate"], len(ok)
                t["g_winner"], t["g_n_realizable"] = argmin("g_status", "g_realized_cost")
                t["ex_winner"], t["ex_n_realizable"] = argmin("ex_status", "ex_realized_cost")
                t["wh_winner"], t["wh_n_realizable"] = argmin("wh_status", "wh_realized_cost")
                okl = [r for r in recs if r["lit_status"] == "realized"]
                t["lit_winner"] = min(okl, key=lambda r: r["lit_realized_cost"])["candidate"] if okl else None
                t["lit_n_realizable"] = len(okl)
                t["g_all_unrealizable"] = t["g_n_realizable"] == 0
                t["ex_all_unrealizable"] = t["ex_n_realizable"] == 0
                t["wh_all_unrealizable"] = t["wh_n_realizable"] == 0
                t["logged_winner_differs_from_pure_cost"] = trig["cost_winner_logged"] != trig["cost_winner"]
                t["g_winner_vs_logged"] = (t["g_winner"] is not None and t["g_winner"] != trig["cost_winner_logged"])
                t["g_winner_changed"] = (t["g_winner"] is not None and t["g_winner"] != trig["cost_winner"])
                t["ex_winner_changed"] = (t["ex_winner"] is not None and t["ex_winner"] != trig["cost_winner"])
                t["wh_winner_changed"] = (t["wh_winner"] is not None and t["wh_winner"] != trig["cost_winner"])
                t["lit_winner_changed"] = (t["lit_winner"] is not None and t["lit_winner"] != trig["cost_winner"])
                # B2 reference (item 8): current-task rows only
                cur = next((r for r in recs if r["is_current_task"]), None)
                if cur is not None:
                    alts = [r for r in recs if not r["is_current_task"] and r["g_status"] == "realized"]
                    best = min(alts, key=lambda r: r["g_realized_cost"]) if alts else None
                    t.update({"cur_candidate": cur["candidate"], "cur_T_r": cur["T_r"],
                              "cur_g_status": cur["g_status"], "cur_g_delta": cur["g_delta"],
                              "cur_ex_delta": cur["ex_delta"], "cur_ex_status": cur["ex_status"],
                              "cur_delta_over_T_r": (cur["g_delta"] / cur["T_r"] if cur["g_delta"] is not None else None),
                              "cur_delta_over_T_h": (cur["g_delta"] / trig["T_h"] if cur["g_delta"] is not None else None),
                              "best_alt": (best["candidate"] if best else None),
                              "best_alt_realized_cost": (best["g_realized_cost"] if best else None),
                              "best_alt_delta": (best["g_delta"] if best else None),
                              "cur_realized_cost": cur["g_realized_cost"],
                              "cur_margin_vs_best_alt": ((best["g_realized_cost"] - cur["g_realized_cost"])
                                                         if best and cur["g_realized_cost"] is not None else None),
                              "g_keeps_current": t["g_winner"] == cur["candidate"]})
                triggers.append(t)

    rows_df = pd.DataFrame(rows)
    real_df = pd.DataFrame(real)
    trig_df = pd.DataFrame(triggers)
    rows_df.to_csv(HERE / "rows.csv", index=False)
    real_df.to_csv(HERE / "a_realization.csv", index=False)
    trig_df.to_csv(HERE / "b_triggers_argmin.csv", index=False)
    checks["sampled_worst_margin"] = None if math.isinf(checks["sampled_worst_margin"]) else checks["sampled_worst_margin"]
    json.dump(checks, open(HERE / "checks.json", "w"), indent=1)

    # ---- scale context (item 9) -------------------------------------------
    scale = []
    for cond in C["conditions"]:
        if cond["assignment_prior"]:
            continue  # geometry is identical across the prior pair
        legs = defaultdict(list)
        T_rs, T_hs, approach, carry, dists = [], [], [], [], []
        for tr in cond["triggers"]:
            for cand in tr.get("candidates", []):
                p = cand["projection"]
                T_rs.append(p["segments"][-1]["end_step"])
                for a, sg in zip(p["actions"], p["segments"]):
                    L = math.dist(sg["start_pos"], sg["end_pos"])
                    if a["action"] == "move_to":
                        legs[a["phase"]].append(L)
            hp = tr.get("human_projection") or tr.get("counterfactual_human_projection")
            if hp:
                T_hs.append(hp["segments"][-1]["end_step"])
                for a, sg in zip(hp["actions"], hp["segments"]):
                    if a["action"] == "move_to":
                        legs["human:" + a["phase"]].append(math.dist(sg["start_pos"], sg["end_pos"]))
            if "agent_positions" in tr:
                dists.append(math.dist(tr["agent_positions"]["robot_0"], tr["agent_positions"]["human_0"]))
        sp = cond["layout_space"]
        objs = {k: v for k, v in cond["object_positions"].items() if cond["object_types"][k] != "item"}
        xs = [p[0] for p in objs.values()]; ys = [p[1] for p in objs.values()]
        row = {"layout": cond["layout"], "scenario": cond["scenario"], "width": sp["width"], "height": sp["height"],
               "diagonal": math.hypot(sp["width"], sp["height"]),
               "task_object_bbox": f"x[{min(xs):.0f},{max(xs):.0f}] y[{min(ys):.0f},{max(ys):.0f}]",
               "step_size_cm_per_tick": cond["config"]["mesa_step_size"],
               "executor_proximity_cm": PROXIMITY_THRESHOLD,
               "interference_spatial_resolution_cm": cond["config"]["interference_spatial_resolution"],
               "theta": cond["config"]["theta"], "min_safe_distance": cond["config"]["min_safe_distance"],
               "n_candidate_projections": len(T_rs),
               "task_duration_ticks_min_med_max": f"{min(T_rs):.1f} / {np.median(T_rs):.1f} / {max(T_rs):.1f}",
               "human_horizon_ticks_min_med_max": (f"{min(T_hs):.1f} / {np.median(T_hs):.1f} / {max(T_hs):.1f}" if T_hs else None),
               "robot_human_distance_at_trigger_min_med_max": f"{min(dists):.0f} / {np.median(dists):.0f} / {max(dists):.0f}"}
        for k, v in sorted(legs.items()):
            row[f"leg_{k}_cm_min_med_max"] = f"{min(v):.0f} / {np.median(v):.0f} / {max(v):.0f}"
        scale.append(row)
    pd.DataFrame(scale).to_csv(HERE / "f_scale.csv", index=False)

    write_summary(rows_df, real_df, trig_df, checks, pd.DataFrame(scale))


# =============================================================================
# summary.md
# =============================================================================

def md(df, floatfmt=".2f"):
    """Markdown table without the tabulate dependency."""
    if len(df) == 0:
        return "(empty)"
    cols = [str(c) for c in df.columns]

    def fmt(v):
        if v is None or (isinstance(v, float) and math.isnan(v)):
            return ""
        if isinstance(v, (float, np.floating)):
            return format(float(v), floatfmt)
        if isinstance(v, (bool, np.bool_)):
            return "True" if v else "False"
        return str(v)
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(fmt(r[c]) for c in df.columns) + " |")
    return "\n".join(lines)


def write_summary(rows_df, real_df, trig_df, checks, scale_df):
    out = ["# T1b — realization sweep: auto-generated tables", "",
           "Generated by analyze.py from captures.json. Ticks unless stated; distances in cm. "
           "P = primary (admitted projection), CF = counterfactual (not admitted), "
           "correct = hypothesis matches the human's actual task, non-degenerate.", ""]

    def sec(title):
        out.extend(["", f"## {title}", ""])

    sec("Population")
    pop = rows_df.groupby(["row_class", "hyp_matches_actual", "degenerate"]).agg(
        rows=("candidate", "size"), triggers=("step", lambda x: len(set(zip(rows_df.loc[x.index, "condition"], x))))).reset_index()
    out.append(md(pop))
    out.append("")
    out.append("Per condition (primary rows / triggers with admitted projection):")
    pc = rows_df[rows_df.row_class == "primary"].groupby("condition").agg(
        rows=("candidate", "size"), triggers=("step", "nunique"),
        current_task_rows=("is_current_task", "sum")).reset_index()
    out.append(md(pc))

    P = real_df[(real_df.row_class == "primary") & real_df.hyp_matches_actual & ~real_df.degenerate]
    W = real_df[(real_df.row_class == "primary") & ~(real_df.hyp_matches_actual & ~real_df.degenerate)]
    CF = real_df[(real_df.row_class == "counterfactual") & real_df.hyp_matches_actual & ~real_df.degenerate]

    sec("1. Realization status and hold δ per separation — P, correct hypothesis")
    for name, D in (("greedy (design loop, strict horizon)", "g"), ("exact (same policy, minimal hold)", "ex"), ("whole (T1 single shift)", "wh")):
        out.append(f"**{name}**"); out.append("")
        g = []
        for s, grp in P.groupby("s"):
            st = grp[f"{D}_status"].value_counts()
            d = grp.loc[grp[f"{D}_status"] == "realized", f"{D}_delta"]
            dpos = d[d > 1e-9]
            frac = (grp.loc[grp[f"{D}_status"] == "realized", f"{D}_delta"] / grp.loc[grp[f"{D}_status"] == "realized", "T_r"])
            g.append({"s": s, "rows": len(grp), "realized": int(st.get("realized", 0)),
                      "δ=0": int((d <= 1e-9).sum()), "δ>0": int(len(dpos)),
                      "δ>0 min/med/max": (f"{dpos.min():.2f} / {dpos.median():.2f} / {dpos.max():.2f}" if len(dpos) else "-"),
                      "δ/T_r max": (f"{frac.max():.3f}" if len(frac) else "-"),
                      "clears via tail": int(grp[f"{D}_clears_via_tail"].sum()),
                      **{k: int(v) for k, v in st.items() if k != "realized"}})
        out.append(md(pd.DataFrame(g).fillna(0)))
        out.append("")

    out.append("**literal (design pseudo-code: break AND PLACE when the clear time is past the horizon)** — "
               "'outlasts' = placed with an open violation at T_h (counted realized by the pseudo-code, not by the task's rule)")
    out.append("")
    g = []
    for s, grp in P.groupby("s"):
        st = grp["lit_status"].value_counts()
        d = grp.loc[grp.lit_status == "realized", "lit_delta"]
        g.append({"s": s, "rows": len(grp), "realized": int(st.get("realized", 0)),
                  "of which outlasts": int((grp.lit_outlasts & (grp.lit_status == "realized")).sum()),
                  "δ>0": int((d > 1e-9).sum()),
                  "strict≠literal status": int((grp.g_status != grp.lit_status).sum()),
                  **{k: int(v) for k, v in st.items() if k != "realized"}})
    out.append(md(pd.DataFrame(g).fillna(0)))
    out.append("")

    sec("1b. Same, wrong-hypothesis / degenerate / human-finished primary rows (reported separately)")
    g = []
    for s, grp in W.groupby("s"):
        st = grp["g_status"].value_counts()
        d = grp.loc[grp.g_status == "realized", "g_delta"]
        g.append({"s": s, "rows": len(grp), "realized": int(st.get("realized", 0)), "δ>0": int((d > 1e-9).sum()),
                  **{k: int(v) for k, v in st.items() if k != "realized"}})
    out.append(md(pd.DataFrame(g).fillna(0)))
    out.append("")
    out.append("Counterfactual rows (projection NOT admitted), correct hypothesis, greedy:")
    g = []
    for s, grp in CF.groupby("s"):
        st = grp["g_status"].value_counts()
        d = grp.loc[grp.g_status == "realized", "g_delta"]
        g.append({"s": s, "rows": len(grp), "realized": int(st.get("realized", 0)), "δ>0": int((d > 1e-9).sum()),
                  **{k: int(v) for k, v in st.items() if k != "realized"}})
    out.append(md(pd.DataFrame(g).fillna(0)))

    sec("2. Where the holds sit — greedy, P correct; robot phase of the held segment × human phase at hold start")
    hp = []
    for s, grp in P.groupby("s"):
        c = Counter()
        for h in grp.g_holds:
            if not isinstance(h, str) or not h:
                continue
            for part in h.split(";"):
                seg, phase, rest = part.split(":", 2)
                human = rest.split("[human:")[1].rstrip("]")
                c[(phase, human)] += 1
        for (phase, human), n in sorted(c.items()):
            hp.append({"s": s, "robot segment": phase, "human phase at hold start": human, "holds": n})
    out.append(md(pd.DataFrame(hp)) if hp else "(no holds)")
    out.append("")
    out.append("First violation (unheld projection at the first violated placement), robot phase × human phase, P correct, s = 30 / 100:")
    fv = P[P.first_violation_t.notna() & P.s.isin([30, 100])].groupby(["s", "first_violation_robot_phase", "first_violation_human_phase"]).size().reset_index(name="rows")
    out.append(md(fv))

    sec("3. Why no realization — greedy, P correct, by failing segment's phase")
    nf = P[P.g_status != "realized"].groupby(["s", "g_status", "g_fail_phase"]).size().reset_index(name="rows")
    out.append(md(nf) if len(nf) else "(none)")
    out.append("")
    out.append("exact realizer, failing segment's phase:")
    nf = P[P.ex_status != "realized"].groupby(["s", "ex_fail_phase"]).size().reset_index(name="rows")
    out.append(md(nf) if len(nf) else "(none)")

    sec("4. Unassessed share — P correct, greedy-realized rows")
    ua = []
    for s, grp in P[P.g_status == "realized"].groupby("s"):
        held = grp[grp.g_delta > 1e-9]
        ua.append({"s": s, "realized rows": len(grp),
                   "share before (min/med/max)": f"{grp.unassessed_before_share.min():.2f} / {grp.unassessed_before_share.median():.2f} / {grp.unassessed_before_share.max():.2f}",
                   "share after (min/med/max)": f"{grp.unassessed_after_share.min():.2f} / {grp.unassessed_after_share.median():.2f} / {grp.unassessed_after_share.max():.2f}",
                   "held rows": len(held),
                   "widening ticks, held rows (min/med/max)": (f"{held.unassessed_widening_ticks.min():.2f} / {held.unassessed_widening_ticks.median():.2f} / {held.unassessed_widening_ticks.max():.2f}" if len(held) else "-"),
                   "held rows fully unassessed after": int((held.unassessed_after_share >= 0.999).sum()) if len(held) else 0})
    out.append(md(pd.DataFrame(ua)))
    out.append("")
    out.append("Ticks after T_h until the realized trajectory first comes within s of the human's final position "
               "(greedy-realized rows; 'never' = the trajectory ends first or stays clear):")
    tl = []
    for s, grp in P[P.g_status == "realized"].groupby("s"):
        for held, sub in (("δ=0", grp[grp.g_delta <= 1e-9]), ("δ>0", grp[grp.g_delta > 1e-9])):
            v = sub.g_tail_lead.dropna()
            tl.append({"s": s, "rows": held, "n": len(sub), "never": int(sub.g_tail_lead.isna().sum()),
                       "lead min/med/max": (f"{v.min():.2f} / {v.median():.2f} / {v.max():.2f}" if len(v) else "-"),
                       "lead < 1 tick": int((v < 1).sum()), "lead < 5": int((v < 5).sum()),
                       "held-at-end still realizable (greedy/exact/whole)": f"{int((sub.g_held_end_status == 'realized').sum())} / {int((sub.ex_held_end_status == 'realized').sum())} / {int((sub.wh_held_end_status == 'realized').sum())}"})
    out.append(md(pd.DataFrame(tl)))

    sec("5. Argmin over the pool per (condition, trigger) — admitted triggers only")
    T = trig_df[(trig_df.row_class == "primary") & trig_df.s.notna()]
    Tc = T[T.hyp_matches_actual & ~T.degenerate]
    am = []
    for s, grp in Tc.groupby("s"):
        am.append({"s": s, "triggers": len(grp),
                   "greedy winner ≠ cost winner": int(grp.g_winner_changed.sum()),
                   "exact winner ≠ cost": int(grp.ex_winner_changed.sum()),
                   "whole winner ≠ cost": int(grp.wh_winner_changed.sum()),
                   "literal winner ≠ cost": int(grp.lit_winner_changed.sum()),
                   "greedy all-unrealizable": int(grp.g_all_unrealizable.sum()),
                   "exact all-unrealizable": int(grp.ex_all_unrealizable.sum()),
                   "whole all-unrealizable": int(grp.wh_all_unrealizable.sum()),
                   "literal all-unrealizable": int((grp.lit_n_realizable == 0).sum())})
    out.append(md(pd.DataFrame(am)))
    out.append("")
    out.append("Per trigger (correct hypothesis): first s at which the greedy winner differs from the cost winner, and first s at which nothing realizes:")
    pt = []
    for (c, st), grp in Tc.groupby(["condition", "step"]):
        grp = grp.sort_values("s")
        ch = grp[grp.g_winner_changed]
        au = grp[grp.g_all_unrealizable]
        exch = grp[grp.ex_winner_changed]
        exau = grp[grp.ex_all_unrealizable]
        pt.append({"condition": c, "step": st, "trigger": grp.trigger.iloc[0], "pool": int(grp.pool_size.iloc[0]),
                   "current in pool": bool(grp.current_in_pool.iloc[0]), "cost winner": short(grp.cost_winner.iloc[0]),
                   "greedy: first s winner changes": (int(ch.s.iloc[0]) if len(ch) else "-"),
                   "greedy: new winner": (short(ch.g_winner.iloc[0]) if len(ch) else "-"),
                   "greedy: first s all-unrealizable": (int(au.s.iloc[0]) if len(au) else "-"),
                   "exact: first s winner changes": (int(exch.s.iloc[0]) if len(exch) else "-"),
                   "exact: first s all-unrealizable": (int(exau.s.iloc[0]) if len(exau) else "-")})
    out.append(md(pd.DataFrame(pt)))
    out.append("")
    out.append("Wrong-hypothesis / degenerate admitted triggers (separate):")
    Tw = T[~(T.hyp_matches_actual & ~T.degenerate)]
    pt = []
    for (c, st), grp in Tw.groupby(["condition", "step"]):
        grp = grp.sort_values("s")
        ch = grp[grp.g_winner_changed]; au = grp[grp.g_all_unrealizable]
        pt.append({"condition": c, "step": st, "hypothesis": short(grp.hypothesis.iloc[0]), "actual": (short(grp.human_actual.iloc[0]) if grp.human_actual.iloc[0] else None),
                   "greedy: first s winner changes": (int(ch.s.iloc[0]) if len(ch) else "-"),
                   "greedy: first s all-unrealizable": (int(au.s.iloc[0]) if len(au) else "-")})
    out.append(md(pd.DataFrame(pt)) if pt else "(none)")

    out.append("")
    out.append("Counterfactual triggers (projection NOT admitted; correct hypothesis) — same columns, separate:")
    Tcf = trig_df[(trig_df.row_class == "counterfactual") & trig_df.s.notna() & trig_df.hyp_matches_actual & ~trig_df.degenerate]
    am = []
    for s, grp in Tcf.groupby("s"):
        am.append({"s": s, "triggers": len(grp), "greedy winner ≠ cost winner": int(grp.g_winner_changed.sum()),
                   "exact winner ≠ cost": int(grp.ex_winner_changed.sum()), "greedy all-unrealizable": int(grp.g_all_unrealizable.sum()),
                   "exact all-unrealizable": int(grp.ex_all_unrealizable.sum())})
    out.append(md(pd.DataFrame(am)))
    out.append("")
    out.append("Admitted triggers where the LOGGED winner already differs from the pure cost argmin "
               "(the superseded min_safe_distance=1.0 exclusion removed the cheapest candidate):")
    lw = T[T.logged_winner_differs_from_pure_cost & (T.s == SEPARATIONS[0])][["condition", "step", "trigger", "cost_winner", "cost_winner_logged"]].copy()
    lw["cost_winner"] = lw.cost_winner.map(short); lw["cost_winner_logged"] = lw.cost_winner_logged.map(short)
    out.append(md(lw) if len(lw) else "(none)")

    sec("6. All-unrealizable (condition, trigger) cases — P correct, by pool composition")
    au = []
    for s, grp in Tc.groupby("s"):
        a = grp[grp.g_all_unrealizable]
        au.append({"s": s, "admitted triggers": len(grp), "greedy all-unrealizable": len(a),
                   "of which pool size 1": int((a.pool_size == 1).sum()),
                   "of which current task in pool": int(a.current_in_pool.sum()),
                   "exact all-unrealizable": int(grp.ex_all_unrealizable.sum()),
                   "whole all-unrealizable": int(grp.wh_all_unrealizable.sum())})
    out.append(md(pd.DataFrame(au)))

    sec("7. Per-segment vs whole-trajectory — P correct rows")
    sv = []
    for s, grp in P.groupby("s"):
        both = grp[(grp.g_status == "realized") & (grp.wh_status == "realized")]
        diff = both[(both.g_delta - both.wh_delta).abs() > 0.011]
        eb = grp[(grp.ex_status == "realized") & (grp.wh_status == "realized")]
        ediff = eb[(eb.ex_delta - eb.wh_delta).abs() > 0.011]
        sv.append({"s": s, "rows": len(grp),
                   "greedy ok / whole none": int(((grp.g_status == "realized") & (grp.wh_status != "realized")).sum()),
                   "greedy none / whole ok": int(((grp.g_status != "realized") & (grp.wh_status == "realized")).sum()),
                   "both ok, δ differ": len(diff), "greedy > whole": int((diff.g_delta > diff.wh_delta).sum()),
                   "greedy−whole max": (f"{(diff.g_delta - diff.wh_delta).max():.2f}" if len(diff) else "-"),
                   "exact none / whole ok": int(((grp.ex_status != "realized") & (grp.wh_status == "realized")).sum()),
                   "exact ok / whole none": int(((grp.ex_status == "realized") & (grp.wh_status != "realized")).sum()),
                   "exact vs whole, both ok, δ differ": len(ediff),
                   "exact < whole": int((ediff.ex_delta < ediff.wh_delta).sum()), "exact > whole": int((ediff.ex_delta > ediff.wh_delta).sum()),
                   "exact−whole min/max": (f"{(ediff.ex_delta - ediff.wh_delta).min():.2f} / {(ediff.ex_delta - ediff.wh_delta).max():.2f}" if len(ediff) else "-")})
    out.append(md(pd.DataFrame(sv)))
    out.append("")
    out.append("Greedy vs exact (same per-segment policy): rows where they differ, P correct:")
    ge = []
    for s, grp in P.groupby("s"):
        both = grp[(grp.g_status == "realized") & (grp.ex_status == "realized")]
        diff = both[(both.g_delta - both.ex_delta).abs() > 0.011]
        ge.append({"s": s, "greedy none / exact ok": int(((grp.g_status != "realized") & (grp.ex_status == "realized")).sum()),
                   "greedy ok / exact none": int(((grp.g_status == "realized") & (grp.ex_status != "realized")).sum()),
                   "both ok, δ differ": len(diff), "greedy > exact": int((diff.g_delta > diff.ex_delta).sum()),
                   "greedy−exact med/max": (f"{(diff.g_delta - diff.ex_delta).median():.2f} / {(diff.g_delta - diff.ex_delta).max():.2f}" if len(diff) else "-"),
                   "greedy iterations with segment-end truncation": int(grp.g_n_segment_end_truncations.sum())})
    out.append(md(pd.DataFrame(ge)))

    sec("8. B2 reference — current-task rows at admitted, correct-hypothesis triggers (greedy)")
    b2 = Tc[Tc.cur_candidate.notna()].sort_values(["condition", "step", "s"])
    cols = ["condition", "step", "trigger", "s", "cur_T_r", "T_h", "cur_g_status", "cur_g_delta", "cur_ex_delta",
            "cur_delta_over_T_r", "cur_delta_over_T_h", "best_alt", "best_alt_realized_cost", "cur_realized_cost",
            "cur_margin_vs_best_alt", "g_keeps_current"]
    b2v = b2[b2.s.isin([10, 30, 50, 100, 200])][cols].copy()
    b2v["best_alt"] = b2v.best_alt.map(lambda x: short(x) if isinstance(x, str) else x)
    out.append(md(b2v))

    sec("9. Scale context per layout")
    out.append(md(scale_df.T.reset_index().rename(columns={"index": "quantity"}), floatfmt=".2f"))

    sec("Checks")
    out.append("```"); out.append(json.dumps(checks, indent=1)); out.append("```")

    (HERE / "summary.md").write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    if "--summary-only" in sys.argv:
        write_summary(pd.read_csv(HERE / "rows.csv"), pd.read_csv(HERE / "a_realization.csv"),
                      pd.read_csv(HERE / "b_triggers_argmin.csv"), json.load(open(HERE / "checks.json")),
                      pd.read_csv(HERE / "f_scale.csv"))
    else:
        main()
