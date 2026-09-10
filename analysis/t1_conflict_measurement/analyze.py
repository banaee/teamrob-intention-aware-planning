"""
analysis/t1_conflict_measurement/analyze.py  (T1 — measurement only)

Reads captures.json (written by measure.py) and produces the §5 tables and
plots. Nothing here touches the simulator or shared/. No thresholds are
proposed; the separations s ∈ {10, 25, 50, 100} are the ones the task fixed
for reporting.

Core quantity: d(t) = Euclidean distance between the robot candidate's
projected position and the human projection's position at integer projection
step t, over [0, floor(min(T_r, T_h))]. Positions come straight from the
Segments (piecewise-linear, head-to-tail), never from the ConflictPoint list.

Outputs (all in this directory):
  rows.csv                   §5.0 one row per (condition, trigger, candidate)
  a_conflict_profile.csv     §5.1 per row × s
  b_curves/*.csv, *.png      §5.2 d(t) curves for the three required triggers
  b_curves/all/*.png         same plot for every other row with a projection
  c_pause_delay.csv          §5.3 per primary row × s
  d_min_d_sorted.csv, d_min_d_hist.png, d_scale_context.csv   §5.4
  e_pairs.csv                §5.5 candidate pairs within a trigger
  f_theta_flips.csv, f_most_likely_changes.csv                §5.6
  g_tail.csv                 §5.7
  summary.md                 auto-generated tables quoted in REPORT.md

Usage: python analysis/t1_conflict_measurement/analyze.py
"""

import json
import math
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
SEPARATIONS = [10, 25, 50, 100]
AT_PROXIMITY = 30.0   # mesa_sim/world_state_builder.PROXIMITY_THRESHOLD, analysis-side copy

# dataviz reference palette (light surface); fixed categorical order
C_SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
C_TEXT, C_TEXT2, C_GRID = "#0b0b0b", "#52514e", "#e6e5e1"
COND_COLOR = {"s00_off": C_SERIES[0], "s00_on": C_SERIES[1], "s10_off": C_SERIES[2],
              "s10_on": C_SERIES[3], "s20_off": C_SERIES[4], "s20_on": C_SERIES[5]}


# =============================================================================
# Geometry on Segment chains
# =============================================================================

def short(task_key):
    """'deliver_item(?item=item_4,?kitting_table=kitting_table_0)' → 'item_4'; other tasks keep their name."""
    if task_key is None:
        return None
    if "?item=" in task_key:
        return task_key.split("?item=")[1].split(",")[0].split(")")[0]
    return task_key.split("(")[0]


def seg_index_at(segs, t):
    """Index of the segment active at step t (boundary → the segment that starts there)."""
    for i, s in enumerate(segs):
        if s["start_step"] <= t < s["end_step"]:
            return i
    if segs and t == segs[-1]["end_step"]:
        return len(segs) - 1
    for i, s in enumerate(segs):  # zero-length segment exactly at t
        if s["start_step"] <= t <= s["end_step"]:
            return i
    return None


def pos_at(segs, t):
    i = seg_index_at(segs, t)
    if i is None:
        return None
    s = segs[i]
    if s["end_step"] <= s["start_step"]:
        return np.array(s["start_pos"], dtype=float)
    f = (t - s["start_step"]) / (s["end_step"] - s["start_step"])
    a, b = np.array(s["start_pos"], dtype=float), np.array(s["end_pos"], dtype=float)
    return a + f * (b - a)


def positions(segs, t_max_int):
    return np.array([pos_at(segs, t) for t in range(0, t_max_int + 1)], dtype=float)


def phases_at(plan, t_max_int):
    """Phase label of the active action at every integer step."""
    segs = plan["segments"]
    return [plan["actions"][seg_index_at(segs, t)]["phase"] for t in range(0, t_max_int + 1)]


def intervals(mask):
    out = []
    start = None
    for i, m in enumerate(mask):
        if m and start is None:
            start = i
        if not m and start is not None:
            out.append((start, i - 1))
            start = None
    if start is not None:
        out.append((start, len(mask) - 1))
    return out


def fmt_counter(c):
    return ";".join(f"{k}:{v}" for k, v in sorted(c.items(), key=lambda kv: -kv[1])) if c else ""


# =============================================================================
# Row assembly
# =============================================================================

def build_rows(captures):
    rows = []
    for cond in captures["conditions"]:
        for tr in cond["triggers"]:
            hp = tr.get("human_projection")
            cf = tr.get("counterfactual_human_projection")
            if hp is not None:
                data_class, hplan = "primary", hp
            elif cf is not None:
                data_class, hplan = "counterfactual", cf
            else:
                data_class, hplan = "none", None
            for cd in tr["candidates"]:
                r = {
                    "condition": cond["name"], "scenario": cond["scenario"],
                    "layout": cond["layout"], "assignment_prior": cond["assignment_prior"],
                    "step": tr["step"], "trigger": tr["trigger"],
                    "confidence": round(tr["confidence"], 3),
                    "projection_reason": tr["projection_reason"], "data_class": data_class,
                    "most_likely": short(tr["most_likely"]),
                    "human_actual_task": short(tr["human_actual_task"]),
                    "hypothesis_matches_actual": (tr["most_likely"] == tr["human_actual_task"]),
                    "human_actual_action": tr["human_actual_action"],
                    "robot_holding": tr["robot_holding"],
                    "robot_current_task": short(tr["robot_current_task"]),
                    "candidate": short(cd["task"]), "is_current_task": cd["is_current_task"],
                    "cost": cd["cost"], "feasible": cd.get("feasible", True),
                    "winner": short(tr["winner"]), "is_winner": tr["winner"] == cd["task"],
                    "robot_phases": "|".join(a["phase"] for a in cd["projection"]["actions"]),
                    "human_phases": "|".join(a["phase"] for a in hplan["actions"]) if hplan else "",
                    "logged_min_dist": (cd.get("logged_min_dist") if data_class == "primary"
                                        else cd.get("counterfactual_logged_min_dist")),
                    "_rplan": cd["projection"], "_hplan": hplan,
                    "_robot_pos": tr["agent_positions"]["robot_0"],
                    "_human_pos": tr["agent_positions"]["human_0"],
                }
                r["T_r"] = cd["projection"]["segments"][-1]["end_step"]
                r["T_h"] = hplan["segments"][-1]["end_step"] if hplan else None
                # Degenerate counterfactual: the human has finished its script, or the
                # below-theta hypothesis projects an already-delivered / being-placed item,
                # so the "trajectory" is two agents standing at the kitting table. Criterion:
                # no actual human task, or no projected human movement leg reaches the
                # executor's at-proximity threshold (30 world units). Such rows say nothing
                # about interference; kept out of (d) and (e), listed separately.
                if hplan is not None:
                    longest_leg = max((math.dist(sg["start_pos"], sg["end_pos"]) for sg in hplan["segments"]), default=0.0)
                    r["human_longest_leg"] = round(longest_leg, 1)
                    r["degenerate"] = (tr["human_actual_task"] is None) or (longest_leg < AT_PROXIMITY)
                else:
                    r["human_longest_leg"] = None
                    r["degenerate"] = False
                rows.append(r)
    return rows


def compute_profile(r):
    """d(t) and everything §5.1/§5.7 derive from it, for one row with a projection."""
    T = min(r["T_r"], r["T_h"])
    n = int(math.floor(T))
    R = positions(r["_rplan"]["segments"], n)
    H = positions(r["_hplan"]["segments"], n)
    d = np.linalg.norm(R - H, axis=1)
    rph = phases_at(r["_rplan"], n)
    hph = phases_at(r["_hplan"], n)
    r["_d"], r["_rph"], r["_hph"] = d, rph, hph
    r["window_steps"] = n + 1
    r["min_d"] = float(d.min())
    r["argmin_t"] = int(d.argmin())
    r["robot_action_at_min"] = rph[r["argmin_t"]]
    r["human_action_at_min"] = hph[r["argmin_t"]]
    r["min_at_window_end"] = (r["argmin_t"] == n)
    r["tail_T_r_minus_T_h"] = r["T_r"] - r["T_h"]
    r["tail_steps_unchecked"] = max(0.0, r["T_r"] - r["T_h"])
    r["tail_share_of_cost"] = max(0.0, r["T_r"] - r["T_h"]) / r["T_r"] if r["T_r"] > 0 else 0.0
    prof = []
    for s in SEPARATIONS:
        mask = d < s
        iv = intervals(mask)
        below = np.where(mask)[0]
        prof.append({
            "s": s, "steps_below": int(mask.sum()), "n_intervals": len(iv),
            "first_step": int(below[0]) if len(below) else None,
            "last_step": int(below[-1]) if len(below) else None,
            "intervals": ";".join(f"{a}-{b}" for a, b in iv),
            "robot_phase_steps": fmt_counter(Counter(rph[i] for i in below)),
            "human_phase_steps": fmt_counter(Counter(hph[i] for i in below)),
        })
    r["_profile"] = prof


def pause_delay(r):
    """
    §5.3. Robot holds its start position for δ steps, then runs its projected
    trajectory unchanged; the human projection is not shifted. d_δ(t) is
    checked at every integer t where both exist: t ∈ [0, floor(min(T_r+δ, T_h))].
    The hold counts (robot at start position for t < δ).
    Search δ ∈ [0, ceil(T_h)); unresolvable if nothing clears — not capped.
    Extra column delta_ext: same search, but the human is HELD at its final
    position after T_h so the robot's whole trajectory is checked. It is only
    there to make the 'clears via tail' flag interpretable; not a requested
    quantity.
    """
    Tr, Th = r["T_r"], r["T_h"]
    nR, nH = int(math.floor(Tr)), int(math.floor(Th))
    R = positions(r["_rplan"]["segments"], nR)          # R[u], u = 0..nR
    H = positions(r["_hplan"]["segments"], nH)          # H[t], t = 0..nH
    dmax = int(math.ceil(Th))                            # δ ∈ [0, dmax)
    minD = np.empty(dmax)
    minD_ext = np.empty(dmax)
    Hend = H[-1]
    for delta in range(dmax):
        t_max = int(math.floor(min(Tr + delta, Th)))
        t = np.arange(0, t_max + 1)
        u = np.clip(t - delta, 0, nR)
        dd = np.linalg.norm(R[u] - H[t], axis=1)
        minD[delta] = dd.min()
        # extended human: t up to nR + delta, human held at Hend beyond nH
        t2 = np.arange(0, nR + delta + 1)
        u2 = np.clip(t2 - delta, 0, nR)
        Ht = np.where((t2 <= nH)[:, None], H[np.clip(t2, 0, nH)], Hend)
        minD_ext[delta] = np.linalg.norm(R[u2] - Ht, axis=1).min()
    d0 = np.linalg.norm(R[0] - H, axis=1)               # hold position vs human over its projection
    out = []
    for s in SEPARATIONS:
        ok = np.where(minD >= s)[0]
        hold_conf = np.where(d0 < s)[0]
        hold_first = int(hold_conf[0]) if len(hold_conf) else None
        rec = {"s": s, "hold_first_conflict_t": hold_first,
               "hold_position_within_s": hold_first is not None}
        if len(ok):
            delta = int(ok[0])
            rec.update({"status": "cleared", "delta": delta, "delta_over_cost": delta / r["cost"],
                        "unchecked_share_at_delta": max(0.0, Tr - (Th - delta)) / Tr})
            # tail flag: what happened to the violations of δ-1?
            if delta > 0:
                dm = delta - 1
                t_max = int(math.floor(min(Tr + dm, Th)))
                t = np.arange(0, t_max + 1)
                u = np.clip(t - dm, 0, nR)
                viol_t = t[np.linalg.norm(R[u] - H[t], axis=1) < s]
                viol_u = viol_t - dm                    # robot-trajectory steps (all ≥ 0 since δ cleared)
                pushed = int(np.sum(viol_u + delta > nH))
                rec.update({"n_viol_at_delta_minus_1": int(len(viol_t)),
                            "n_pushed_past_T_h": pushed,
                            "n_separated": int(len(viol_t)) - pushed,
                            "clears_via_tail": pushed > 0,
                            "clears_via_tail_only": pushed == len(viol_t) and len(viol_t) > 0})
            else:
                rec.update({"n_viol_at_delta_minus_1": 0, "n_pushed_past_T_h": 0, "n_separated": 0,
                            "clears_via_tail": False, "clears_via_tail_only": False})
        else:
            cause = "hold_position" if hold_first is not None else "no_clearing_shift"
            rec.update({"status": f"unresolvable({cause})", "delta": None, "delta_over_cost": None,
                        "unchecked_share_at_delta": None, "n_viol_at_delta_minus_1": None,
                        "n_pushed_past_T_h": None, "n_separated": None,
                        "clears_via_tail": None, "clears_via_tail_only": None})
        ok_ext = np.where(minD_ext >= s)[0]
        rec["delta_ext_human_held_at_end"] = int(ok_ext[0]) if len(ok_ext) else "unresolvable"
        rec["max_delta_searched"] = dmax - 1
        out.append(rec)
    r["_pause"] = out


# =============================================================================
# Plots
# =============================================================================

def plot_curves(rows_for_trigger, path_png, path_csv, title):
    rows_for_trigger = sorted(rows_for_trigger, key=lambda r: r["cost"])
    k = len(rows_for_trigger)
    fig, axes = plt.subplots(k, 1, figsize=(11, 3.3 * k), sharex=True, squeeze=False)
    tmax = max(r["T_r"] for r in rows_for_trigger)
    csv = {}
    for ax, r in zip(axes[:, 0], rows_for_trigger):
        d = r["_d"]
        t = np.arange(len(d))
        ax.set_facecolor("#fcfcfb")
        for s in SEPARATIONS:
            ax.axhline(s, color=C_GRID, lw=1, zorder=1)
            ax.text(tmax * 1.005, s, f"s={s}", va="center", ha="left", fontsize=7, color=C_TEXT2)
        # unchecked tail (human projection ended)
        if r["T_r"] > r["T_h"]:
            ax.axvspan(r["T_h"], r["T_r"], color="#eeeeea", zorder=0)
            if (r["T_r"] - r["T_h"]) > 0.08 * tmax:
                ax.text((r["T_h"] + r["T_r"]) / 2, d.max() * 0.5,
                        "human projection\nended (unchecked)", ha="center", fontsize=7, color=C_TEXT2)
        ax.plot(t, d, color=C_SERIES[0], lw=2, zorder=3)
        ax.plot(r["argmin_t"], r["min_d"], "o", ms=6, color=C_SERIES[0], mec="white", mew=1, zorder=4)
        ax.annotate(f"min d = {r['min_d']:.1f} @ t={r['argmin_t']}", (r["argmin_t"], r["min_d"]),
                    xytext=(6, 10), textcoords="offset points", fontsize=8, color=C_TEXT)
        ymax = max(d.max(), 120) * 1.12
        # robot action boundaries (top labels), human boundaries (bottom labels)
        for i, (seg, a) in enumerate(zip(r["_rplan"]["segments"], r["_rplan"]["actions"])):
            ax.axvline(seg["start_step"], color=C_SERIES[1], lw=1, ls="--", zorder=2)
            ax.text(seg["start_step"] + 3, ymax * (0.97 - 0.06 * (i % 2)), f"R: {a['phase']}", va="top",
                    fontsize=7, color=C_SERIES[1])
        for i, (seg, a) in enumerate(zip(r["_hplan"]["segments"], r["_hplan"]["actions"])):
            ax.axvline(seg["start_step"], color=C_SERIES[2], lw=1, ls=":", zorder=2)
            ax.text(seg["start_step"] + 3, ymax * (0.04 + 0.06 * (i % 2)), f"H: {a['phase']}", va="bottom",
                    fontsize=7, color=C_SERIES[2])
        ax.axvline(r["T_h"], color=C_SERIES[2], lw=1, ls=":")
        ax.axvline(r["T_r"], color=C_SERIES[1], lw=1, ls="--")
        ax.set_ylim(0, ymax)
        ax.set_ylabel("d(t)  [world units]", fontsize=8)
        ax.set_title(f"{r['candidate']}  cost={r['cost']}  T_r={r['T_r']:.0f}  T_h={r['T_h']:.0f}"
                     f"  {'current task' if r['is_current_task'] else ''}"
                     f"  {'WINNER' if r['is_winner'] else ''}", fontsize=9, loc="left", color=C_TEXT)
        ax.grid(False)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        csv[f"d_{r['candidate']}"] = pd.Series(d, index=t)
        csv[f"robot_phase_{r['candidate']}"] = pd.Series(r["_rph"], index=t)
    csv["human_phase"] = pd.Series(rows_for_trigger[0]["_hph"], index=np.arange(len(rows_for_trigger[0]["_hph"])))
    axes[-1, 0].set_xlabel("projection step t  (1 step = 1 world unit at assumed_speed=1; 1 Mesa tick = 20 units)", fontsize=8)
    fig.suptitle(title + "   (orange dashed = robot action boundaries, teal dotted = human)", fontsize=10, color=C_TEXT)
    fig.tight_layout()
    fig.savefig(path_png, dpi=110)
    plt.close(fig)
    df = pd.DataFrame(csv)
    df.index.name = "t"
    df.to_csv(path_csv)


def plot_hist(prim, path):
    vals = sorted(prim, key=lambda r: r["min_d"])
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), gridspec_kw={"height_ratios": [1, 1.4]})
    x = [r["min_d"] for r in vals]
    bins = np.arange(0, math.ceil(max(x) / 25) * 25 + 26, 25)
    ax1.hist(x, bins=bins, color=C_SERIES[0], edgecolor="white", lw=1)
    ax1.set_xlabel("min d(t) over the shared window  [world units], bin width 25")
    ax1.set_ylabel("primary rows")
    ax1.set_title(f"Distribution of min d(t), primary rows only (n={len(x)})", loc="left", fontsize=10)
    for sp in ("top", "right"):
        ax1.spines[sp].set_visible(False)
    conds = list(COND_COLOR)
    for i, r in enumerate(vals):
        col = COND_COLOR[r["condition"]]
        mk = "o"
        ax2.plot(r["min_d"], i, mk, color=col, ms=7 if r["is_winner"] else 5,
                 mfc=col if r["is_winner"] else "white", mew=1.5)
        if r["is_current_task"]:
            ax2.plot(r["min_d"], i, "s", ms=11, mfc="none", mec=col, mew=0.8)
        ax2.text(r["min_d"] + 6, i, f"{r['condition']} t={r['step']} {r['candidate']}"
                 f"{' (wrong hyp)' if not r['hypothesis_matches_actual'] else ''}",
                 fontsize=6, va="center", color=C_TEXT2)
    ax2.set_yticks([])
    ax2.set_xlabel("min d(t)  [world units] — filled = winner, hollow = not selected, square ring = candidate is the current task")
    ax2.set_title("Sorted values (one marker per primary row)", loc="left", fontsize=10)
    for c in conds:
        ax2.plot([], [], "o", color=COND_COLOR[c], label=c)
    ax2.legend(fontsize=7, frameon=False, loc="lower right")
    for sp in ("top", "right", "left"):
        ax2.spines[sp].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


# =============================================================================
# Main
# =============================================================================

def md_table(df, floatfmt=".2f"):
    """Markdown table without the optional 'tabulate' dependency."""
    def cell(v):
        if isinstance(v, float):
            return "" if math.isnan(v) else format(v, floatfmt)
        return "" if v is None else str(v)
    cols = list(df.columns)
    lines = ["| " + " | ".join(str(c) for c in cols) + " |", "|" + "---|" * len(cols)]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(cell(row[c]) for c in cols) + " |")
    return "\n".join(lines)


def main():
    captures = json.load(open(HERE / "captures.json"))
    rows = build_rows(captures)
    for r in rows:
        if r["data_class"] != "none":
            compute_profile(r)
    prim = [r for r in rows if r["data_class"] == "primary"]
    for r in prim:
        pause_delay(r)

    public = [k for k in rows[0] if not k.startswith("_")]
    extra = ["window_steps", "min_d", "argmin_t", "robot_action_at_min", "human_action_at_min",
             "min_at_window_end", "tail_T_r_minus_T_h", "tail_steps_unchecked", "tail_share_of_cost"]

    # ---- rows.csv (§5.0) --------------------------------------------------
    df_rows = pd.DataFrame([{**{k: r.get(k) for k in public}, **{k: r.get(k) for k in extra}} for r in rows])
    df_rows.to_csv(HERE / "rows.csv", index=False)

    # ---- (a) conflict profile ------------------------------------------------
    recs = []
    for r in rows:
        if r["data_class"] == "none":
            continue
        for p in r["_profile"]:
            recs.append({"condition": r["condition"], "step": r["step"], "trigger": r["trigger"],
                         "data_class": r["data_class"], "hypothesis_matches_actual": r["hypothesis_matches_actual"],
                         "degenerate": r["degenerate"],
                         "candidate": r["candidate"], "is_current_task": r["is_current_task"],
                         "is_winner": r["is_winner"], "cost": r["cost"], "window_steps": r["window_steps"],
                         "min_d": round(r["min_d"], 2), "argmin_t": r["argmin_t"],
                         "robot_action_at_min": r["robot_action_at_min"],
                         "human_action_at_min": r["human_action_at_min"], **p})
    df_a = pd.DataFrame(recs)
    df_a.to_csv(HERE / "a_conflict_profile.csv", index=False)

    # ---- (b) curves --------------------------------------------------------
    (HERE / "b_curves" / "all").mkdir(parents=True, exist_ok=True)
    required = [("s20_on", 11), ("s20_on", 23)]
    first_built_off = min(r["step"] for r in prim if r["condition"] == "s20_off")
    required.append(("s20_off", first_built_off))
    done = set()
    for r in rows:
        key = (r["condition"], r["step"])
        if r["data_class"] == "none" or r["degenerate"] or key in done:
            continue
        done.add(key)
        grp = [x for x in rows if (x["condition"], x["step"]) == key and x["data_class"] != "none"]
        tag = "" if r["data_class"] == "primary" else "_COUNTERFACTUAL"
        title = (f"{r['condition']} step {r['step']} {r['trigger']} conf={r['confidence']} "
                 f"projection={r['projection_reason']}{tag}  human hyp={r['most_likely']} "
                 f"actual={r['human_actual_task']}")
        sub = HERE / "b_curves" if key in required else HERE / "b_curves" / "all"
        name = f"{r['condition']}_step{r['step']:03d}{tag}"
        plot_curves(grp, sub / f"{name}.png", sub / f"{name}.csv", title)

    # ---- (c) pause delay ---------------------------------------------------
    recs = []
    for r in prim:
        for p in r["_pause"]:
            recs.append({"condition": r["condition"], "step": r["step"], "trigger": r["trigger"],
                         "hypothesis_matches_actual": r["hypothesis_matches_actual"],
                         "candidate": r["candidate"], "is_current_task": r["is_current_task"],
                         "is_winner": r["is_winner"], "cost": r["cost"], "T_r": round(r["T_r"], 1),
                         "T_h": round(r["T_h"], 1), "min_d": round(r["min_d"], 2), **p})
    df_c = pd.DataFrame(recs)
    df_c.to_csv(HERE / "c_pause_delay.csv", index=False)

    # ---- (d) min d distribution + scale context ------------------------------
    df_d = pd.DataFrame([{"condition": r["condition"], "step": r["step"], "trigger": r["trigger"],
                          "candidate": r["candidate"], "is_winner": r["is_winner"],
                          "is_current_task": r["is_current_task"],
                          "hypothesis_matches_actual": r["hypothesis_matches_actual"],
                          "cost": r["cost"], "min_d": round(r["min_d"], 2), "argmin_t": r["argmin_t"],
                          "min_at_window_end": r["min_at_window_end"]}
                         for r in sorted(prim, key=lambda r: r["min_d"])])
    df_d.to_csv(HERE / "d_min_d_sorted.csv", index=False)
    plot_hist(prim, HERE / "d_min_d_hist.png")

    scale = []
    for cond in captures["conditions"]:
        objs = {k: v for k, v in cond["object_positions"].items() if cond["object_types"][k] != "obstacle"}
        xs = [p[0] for p in objs.values()]
        ys = [p[1] for p in objs.values()]
        legs = []
        for tr in cond["triggers"]:
            plans = [c["projection"] for c in tr["candidates"]]
            for hp in (tr.get("human_projection"), tr.get("counterfactual_human_projection")):
                if hp:
                    plans.append(hp)
            for pl in plans:
                for seg, a in zip(pl["segments"], pl["actions"]):
                    L = math.dist(seg["start_pos"], seg["end_pos"])
                    if a["action"] == "move_to":
                        legs.append((a["phase"], L))
        t0 = cond["triggers"][0]
        full_costs = {short(c["task"]): c["cost"] for c in t0["candidates"]}
        all_costs = [c["cost"] for tr in cond["triggers"] for c in tr["candidates"]]
        legdf = pd.DataFrame(legs, columns=["phase", "len"])
        scale.append({
            "condition": cond["name"], "layout": cond["layout"],
            "space_w_x_h": f"{cond['layout_space']['width']}x{cond['layout_space']['height']}",
            "space_diagonal": round(math.hypot(cond["layout_space"]["width"], cond["layout_space"]["height"]), 1),
            "task_object_bbox": f"x[{min(xs):.0f},{max(xs):.0f}] y[{min(ys):.0f},{max(ys):.0f}]",
            "assumed_speed": cond["config"]["assumed_speed"],
            "default_action_cost": cond["config"]["default_action_cost"],
            "mesa_step_size": cond["config"]["mesa_step_size"],
            "min_safe_distance": cond["config"]["min_safe_distance"],
            "theta": cond["config"]["theta"],
            "full_task_costs_at_t0": str(full_costs),
            "candidate_cost_min_med_max": f"{min(all_costs)}/{int(np.median(all_costs))}/{max(all_costs)}",
            "n_projected_legs": len(legs),
            "leg_len_min_med_max": f"{legdf.len.min():.0f}/{legdf.len.median():.0f}/{legdf.len.max():.0f}",
            "approach_leg_med": round(legdf[legdf.phase == "approach_shelf"].len.median(), 0),
            "carry_leg_med": round(legdf[legdf.phase == "carry_to_table"].len.median(), 0),
        })
    df_scale = pd.DataFrame(scale)
    df_scale.to_csv(HERE / "d_scale_context.csv", index=False)

    # ---- (e) pairs ---------------------------------------------------------
    recs = []
    keys = sorted({(r["condition"], r["step"]) for r in rows if r["data_class"] != "none" and not r["degenerate"]})
    for key in keys:
        grp = sorted([r for r in rows if (r["condition"], r["step"]) == key and r["data_class"] != "none" and not r["degenerate"]],
                     key=lambda r: r["cost"])
        for i in range(len(grp)):
            for j in range(i + 1, len(grp)):
                A, B = grp[i], grp[j]   # A cheaper (cost prefers A)
                rec = {"condition": key[0], "step": key[1], "trigger": A["trigger"],
                       "data_class": A["data_class"], "hypothesis_matches_actual": A["hypothesis_matches_actual"],
                       "A_cheaper": A["candidate"], "B": B["candidate"],
                       "A_is_winner": A["is_winner"], "A_is_current": A["is_current_task"],
                       "cost_A": A["cost"], "cost_B": B["cost"], "d_cost": B["cost"] - A["cost"],
                       "min_d_A": round(A["min_d"], 1), "min_d_B": round(B["min_d"], 1),
                       "d_min_d": round(B["min_d"] - A["min_d"], 1),
                       "disagree_min_d": B["min_d"] > A["min_d"]}
                for s_i, s in enumerate(SEPARATIONS):
                    a, b = A["_profile"][s_i]["steps_below"], B["_profile"][s_i]["steps_below"]
                    rec[f"below{s}_A"], rec[f"below{s}_B"], rec[f"d_below{s}"] = a, b, b - a
                    rec[f"disagree_below{s}"] = b < a
                    if A["data_class"] == "primary":
                        da, db = A["_pause"][s_i]["delta"], B["_pause"][s_i]["delta"]
                        rec[f"delta{s}_A"] = "unres" if da is None else da
                        rec[f"delta{s}_B"] = "unres" if db is None else db
                        rec[f"d_delta{s}"] = (db - da) if (da is not None and db is not None) else "n/a"
                        rec[f"disagree_delta{s}"] = (db is not None and (da is None or db < da))
                recs.append(rec)
    df_e = pd.DataFrame(recs)
    df_e.to_csv(HERE / "e_pairs.csv", index=False)

    # ---- (5.6) θ-flip scan ---------------------------------------------------
    flips, changes = [], []
    for cond in captures["conditions"]:
        theta = cond["config"]["theta"]
        ticks = cond["ticks"]
        fired = [t["step"] for t in ticks if t["trigger"] not in (None, "none")]
        prev = None
        for t in ticks:
            ml, cf = t["ir_most_likely"], t["ir_confidence"]
            if ml is None:
                continue
            if prev is not None and ml != prev["ir_most_likely"]:
                nxt = [s for s in fired if s >= t["step"]]
                rec = {"condition": cond["name"], "step": t["step"],
                       "old": short(prev["ir_most_likely"]), "new": short(ml),
                       "conf_prev": prev["ir_confidence"], "conf_now": cf,
                       "both_above_theta": prev["ir_confidence"] >= theta and cf >= theta,
                       "robot_task_at_tick": short(t["pre_task"]), "robot_holding_at_tick": t["pre_holding"],
                       "trigger_this_tick": t["trigger"],
                       "next_fired_trigger_step": nxt[0] if nxt else None,
                       "human_actual_task": short(t["human_actual_task"])}
                changes.append(rec)
                if rec["both_above_theta"]:
                    flips.append(rec)
            prev = t
    pd.DataFrame(flips).to_csv(HERE / "f_theta_flips.csv", index=False)
    pd.DataFrame(changes).to_csv(HERE / "f_most_likely_changes.csv", index=False)

    # ---- (5.7) tail ---------------------------------------------------------
    df_g = pd.DataFrame([{"condition": r["condition"], "step": r["step"], "trigger": r["trigger"],
                          "candidate": r["candidate"], "is_winner": r["is_winner"], "cost": r["cost"],
                          "T_r": round(r["T_r"], 1), "T_h": round(r["T_h"], 1),
                          "T_r_minus_T_h": round(r["tail_T_r_minus_T_h"], 1),
                          "unchecked_steps": round(r["tail_steps_unchecked"], 1),
                          "share_of_cost": round(r["tail_share_of_cost"], 3),
                          "robot_phases_in_tail": "|".join(
                              a["phase"] for seg, a in zip(r["_rplan"]["segments"], r["_rplan"]["actions"])
                              if seg["end_step"] > r["T_h"]),
                          "min_at_window_end": r["min_at_window_end"]} for r in prim])
    df_g.to_csv(HERE / "g_tail.csv", index=False)

    # ---- summary.md ---------------------------------------------------------
    out = []
    out.append("# Auto-generated summary tables (analyze.py)\n")
    out.append(f"rows: total {len(rows)}, primary {len(prim)}, counterfactual "
               f"{sum(r['data_class']=='counterfactual' for r in rows)} (of which degenerate "
               f"{sum(r['degenerate'] for r in rows)}), none {sum(r['data_class']=='none' for r in rows)}\n")
    out.append("\n## Primary rows\n")
    cols = ["condition", "step", "trigger", "confidence", "most_likely", "human_actual_task",
            "hypothesis_matches_actual", "robot_holding", "candidate", "is_current_task", "cost",
            "is_winner", "min_d", "argmin_t", "min_at_window_end", "robot_action_at_min",
            "human_action_at_min", "T_r", "T_h"]
    out.append(md_table(df_rows[df_rows.data_class == "primary"][cols]))
    out.append("\n\n## Counterfactual rows (below-θ triggers, projection of that tick's most_likely) — NOT pooled with primary\n")
    out.append(md_table(df_rows[(df_rows.data_class == "counterfactual") & (~df_rows.degenerate)][cols]))
    out.append("\n\n## Degenerate counterfactual rows (human finished, or hypothesis projects an item already at the table) — excluded from (d) and (e)\n")
    out.append(md_table(df_rows[(df_rows.data_class == "counterfactual") & (df_rows.degenerate)][cols + ["human_actual_action", "human_longest_leg"]]))
    out.append("\n\n## Rows with no projection\n")
    out.append(md_table(df_rows[df_rows.data_class == "none"][["condition", "step", "trigger", "confidence",
                                                               "projection_reason", "most_likely", "candidate", "cost", "is_winner"]]))
    out.append("\n\n## (a) Conflict profile, primary rows, steps with d(t) < s\n")
    piv = df_a[df_a.data_class == "primary"].pivot_table(
        index=["condition", "step", "candidate", "cost", "min_d"], columns="s",
        values=["steps_below", "n_intervals"], aggfunc="first")
    piv.columns = [f"{a}@{b}" for a, b in piv.columns]
    out.append(md_table(piv.reset_index()))
    out.append("\n\n## (a) Where the close steps fall (primary rows with any step below 100)\n")
    sub = df_a[(df_a.data_class == "primary") & (df_a.steps_below > 0)]
    out.append(md_table(sub[["condition", "step", "candidate", "s", "steps_below", "n_intervals", "first_step",
                             "last_step", "robot_phase_steps", "human_phase_steps"]]))
    out.append("\n\n## (c) Pause delay, primary rows\n")
    out.append(md_table(df_c[["condition", "step", "candidate", "is_winner", "cost", "T_r", "T_h", "min_d", "s", "status",
                              "delta", "delta_over_cost", "clears_via_tail", "clears_via_tail_only",
                              "unchecked_share_at_delta", "hold_first_conflict_t", "delta_ext_human_held_at_end"]],
                        floatfmt=".3f"))
    out.append("\n\n## (d) min d sorted, primary rows\n")
    out.append(md_table(df_d))
    out.append("\n\n## (d) scale context\n")
    out.append(md_table(df_scale.astype(str).T.reset_index().rename(columns={"index": "field"})))
    out.append("\n\n## (e) pairs, primary triggers\n")
    ecols = ["condition", "step", "A_cheaper", "B", "A_is_winner", "d_cost", "min_d_A", "min_d_B", "d_min_d",
             "disagree_min_d"] + [c for c in df_e.columns if c.startswith("d_below") or c.startswith("disagree_below")] \
            + [c for c in df_e.columns if c.startswith("delta") or c.startswith("d_delta") or c.startswith("disagree_delta")]
    out.append(md_table(df_e[df_e.data_class == "primary"][ecols]))
    out.append("\n\n## (e) pairs, counterfactual triggers\n")
    ecols2 = [c for c in ecols if "delta" not in c]
    out.append(md_table(df_e[df_e.data_class == "counterfactual"][ecols2]))
    out.append("\n\n## (5.6) most_likely changes with both confidences ≥ θ\n")
    out.append(md_table(pd.DataFrame(flips)) if flips else "(none)")
    out.append("\n\n## (5.6) all most_likely changes\n")
    out.append(md_table(pd.DataFrame(changes), floatfmt=".3f"))
    out.append("\n\n## (5.7) tail beyond the human projection, primary rows\n")
    out.append(md_table(df_g, floatfmt=".3f"))
    (HERE / "summary.md").write_text("\n".join(out) + "\n")
    print("done; primary rows", len(prim))


if __name__ == "__main__":
    main()
