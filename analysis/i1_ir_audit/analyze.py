"""
analysis/i1_ir_audit/analyze.py  — captures.json → the tables quoted in REPORT.md.

Reads only captures.json (written by measure.py). Writes CSVs (one per table)
and summary.md (all tables as markdown). No simulation, no shared/ import.

    ~/python-envs/teamrob-sp4-env/bin/python analysis/i1_ir_audit/analyze.py
"""

import csv
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
C = json.load(open(HERE / "captures.json"))
COND = list(C.keys())
OUT = []   # (title, header, rows) for summary.md


def write(name, header, rows, title):
    with open(HERE / name, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    OUT.append((title, header, rows))


def fmt(v):
    if isinstance(v, float):
        return f"{v:.3f}"
    return "" if v is None else str(v)


def short(key):
    """deliver_item(?item=item_3,?kitting_table=kitting_table_0) -> item_3; coffee_break(...) -> coffee_break"""
    if key.startswith("deliver_item("):
        for part in key[len("deliver_item("):-1].split(","):
            k, v = part.split("=")
            if k == "?item":
                return v
    return key.split("(")[0]


def human_task_short(t):
    return short(t["human_actual_task"]) if t["human_actual_task"] else "-"


# =============================================================================
# (a) evidence paths per condition
# =============================================================================
rows = []
for n in COND:
    c = C[n]
    ticks = c["ticks"]
    kinds = Counter(t["kind"] for t in ticks)
    calls = [l for t in ticks for l in t["likelihoods"]]
    branch = Counter(l["branch"] for l in calls)
    chord = sum(1 for l in calls if l["branch"] == "progress" and not l.get("target_none")
                and l.get("move_norm", 0) > 1e-6 and l.get("target_dist_from_origin", 0) > 1e-6)
    at_target = sum(1 for l in calls if l["branch"] == "progress" and not l.get("target_none")
                    and l.get("move_norm", 0) > 1e-6 and l.get("target_dist_from_origin", 1) <= 1e-6)
    zero_move = sum(1 for l in calls if l["branch"] == "progress" and not l.get("target_none")
                    and l.get("move_norm", 0) <= 1e-6)
    tnone_phase2 = sum(1 for l in calls if l.get("target_none") and l.get("expected_branch") == "phase2_last_move_to")
    tnone_noitem = sum(1 for l in calls if l.get("target_none") and l.get("expected_branch") == "no_item_binding")
    tnone_other = sum(1 for l in calls if l.get("target_none")) - tnone_phase2 - tnone_noitem
    origin_none = sum(1 for l in calls if l.get("origin_none"))
    zone = sum(1 for t in ticks for o in t["omega"].values() if o["zone_fired"])
    temp = sum(1 for t in ticks for o in t["omega"].values() if o["temp_fired"])
    fat = sum(1 for t in ticks for o in t["omega"].values() if o["fatigue_fired"])
    ref_ticks = sum(1 for t in ticks if t["refuted"])
    ref_pairs = sum(len(t["refuted"]) for t in ticks)
    clamp_out = sum(len(f["clamped_to_floor"]) for t in ticks for f in t["finalize"] if f["where"] == "output")
    clamp_ev = sum(len(f["clamped_to_floor"]) for t in ticks for f in t["finalize"] if f["where"] == "evidence")
    term_res = sum(1 for l in calls if l.get("term_resolutions"))
    rows.append([n, len(ticks), c["crash"]["step"] if c["crash"] else "",
                 len(c["hypotheses"]), len(c["inadmissible"]),
                 kinds["moving"], kinds["discrete"], kinds["stationary"],
                 len(calls), branch["progress"], branch["completion"], branch["completion_unresolved"],
                 branch["fallthrough"], term_res,
                 chord, at_target, zero_move, tnone_phase2, tnone_noitem, tnone_other, origin_none,
                 zone, temp, fat, ref_ticks, ref_pairs, clamp_ev, clamp_out])
write("a_evidence_paths.csv",
      ["condition", "ticks", "crash_step", "n_hyp", "n_inadmissible",
       "moving_ticks", "discrete_ticks", "stationary_ticks",
       "likelihood_calls", "branch_progress", "branch_completion", "branch_completion_unresolved",
       "branch_fallthrough", "resolve_term_value_calls",
       "chord_scored", "at_target_HIGH", "zero_move_NEUTRAL", "target_none_phase2_var",
       "target_none_no_item_binding", "target_none_other", "origin_none",
       "zone_boost_pairs", "temp_boost_pairs", "fatigue_boost_pairs",
       "held_refutation_ticks", "held_refutation_pairs", "floor_clamps_evidence", "floor_clamps_output"],
      rows, "(a) Evidence paths per condition — counts over (tick × hypothesis) likelihood calls")

# =============================================================================
# (b) target resolution outcome per hypothesis
# =============================================================================
rows = []
for n in COND:
    c = C[n]
    per = defaultdict(Counter)
    tbl_pos = {oid for oid, ty in c["object_types"].items() if ty == "kitting_table"}
    for t in c["ticks"]:
        for l in t["likelihoods"]:
            per[l["hyp"]][l.get("expected_branch")] += 1
    for h in c["hypotheses"]:
        k = h["key"]
        cnt = per.get(k, Counter())
        rows.append([n, short(k), h["task"], k in c["inadmissible"], sum(cnt.values()),
                     cnt.get("phase1_container:shelf", 0), cnt.get("phase1_container:kitting_table", 0),
                     cnt.get("phase1_container_unpositioned_fallback_item_pos", 0),
                     cnt.get("phase2_last_move_to", 0), cnt.get("no_item_binding", 0),
                     cnt.get("phase1_item_pos", 0)])
write("b_target_resolution.csv",
      ["condition", "hyp", "task", "inadmissible", "calls", "phase1_shelf", "phase1_table_delivered_decoy",
       "phase1_container_is_agent_fallback_item_pos", "phase2_var_target_NEUTRAL",
       "no_item_binding_NEUTRAL", "phase1_item_pos"],
      rows, "(b) _get_expected_position outcome per hypothesis (likelihood calls, moving+discrete ticks only)")

# =============================================================================
# (c) zone boost episodes
# =============================================================================
rows = []
for n in COND:
    c = C[n]
    cur = {}
    for t in c["ticks"]:
        for k, o in t["omega"].items():
            fired = o["zone_fired"]
            if fired and k not in cur:
                cur[k] = {"start": t["step"], "zone": o["target_zone"], "human": human_task_short(t),
                          "action": t["human_action"], "ml_before": short(t["most_likely"])}
            elif not fired and k in cur:
                e = cur.pop(k)
                rows.append([n, short(k), e["zone"], e["start"], t["step"] - 1, e["human"], e["action"],
                             short(k) == e["human"]])
    for k, e in cur.items():
        rows.append([n, short(k), e["zone"], e["start"], c["ticks"][-1]["step"], e["human"], e["action"],
                     short(k) == e["human"]])
rows.sort(key=lambda r: (r[0], r[3], r[1]))
write("c_zone_boost_episodes.csv",
      ["condition", "hyp", "zone", "first_step", "last_step", "human_task_at_start", "human_action_at_start",
       "hyp_is_human_task"],
      rows, "(c) ZONE_BOOST episodes — maximal step ranges where ω_context carried ×2 for a hypothesis")

# =============================================================================
# (d) held-item refutation episodes
# =============================================================================
rows = []
for n in COND:
    c = C[n]
    cur = None
    prev_ml = None
    for t in c["ticks"]:
        if t["refuted"] and cur is None:
            cur = {"start": t["step"], "item": t["held_item_seen"], "n": len(t["refuted"]),
                   "ml_before": prev_ml, "ml_at": short(t["most_likely"]), "conf_at": t["confidence"],
                   "human": human_task_short(t)}
        elif not t["refuted"] and cur is not None:
            rows.append([n, cur["start"], t["step"] - 1, cur["item"], cur["n"], cur["human"],
                         cur["ml_before"], cur["ml_at"], cur["conf_at"], short(t["most_likely"]), t["confidence"]])
            cur = None
        prev_ml = short(t["most_likely"])
    if cur is not None:
        t = c["ticks"][-1]
        rows.append([n, cur["start"], t["step"], cur["item"], cur["n"], cur["human"],
                     cur["ml_before"], cur["ml_at"], cur["conf_at"], "", ""])
write("d_held_item_refutation_episodes.csv",
      ["condition", "first_step", "last_step", "held_item", "n_refuted", "human_task",
       "most_likely_tick_before", "most_likely_at_start", "confidence_at_start",
       "most_likely_after_release", "confidence_after_release"],
      rows, "(d) Held-item refutation episodes — while holding(human, X) is in the world")

# =============================================================================
# (e) legs — global movement legs vs. the human's action boundaries
# =============================================================================
rows = []
for n in COND:
    c = C[n]
    ticks = c["ticks"]
    leg = None
    for i, t in enumerate(ticks):
        if t["kind"] == "moving":
            if leg is None:
                leg = {"start": t["step"], "origin": t["leg_start_after"], "ai0": t["human_action_index"],
                       "task0": human_task_short(t), "act0": t["human_action"], "n": 0,
                       "ai_set": set(), "task_set": set()}
            leg["n"] += 1
            leg["ai_set"].add((t["human_script_index"], t["human_action_index"]))
            leg["task_set"].add(human_task_short(t))
            # a leg also restarts silently if the origin changed without a non-moving tick
            if t["leg_start_before"] != leg["origin"] and t["leg_start_before"] != t["leg_start_after"]:
                pass
        else:
            if leg is not None:
                rows.append([n, leg["start"], ticks[i - 1]["step"], leg["n"], leg["task0"], leg["act0"],
                             len(leg["ai_set"]), len(leg["task_set"]), t["kind"], t["obs_microaction"]])
                leg = None
    if leg is not None:
        rows.append([n, leg["start"], ticks[-1]["step"], leg["n"], leg["task0"], leg["act0"],
                     len(leg["ai_set"]), len(leg["task_set"]), "end_of_run", ""])
write("e_legs.csv",
      ["condition", "first_moving_step", "last_moving_step", "n_moving_ticks", "human_task_at_start",
       "human_action_at_start", "distinct_human_actions_spanned", "distinct_human_tasks_spanned",
       "closed_by", "closing_microaction"],
      rows, "(e) Movement legs (one global leg for all hypotheses) against the human's actual action boundaries")

# =============================================================================
# (f) completion-condition reachability — human's live plan
# =============================================================================
rows = []
for n in COND:
    c = C[n]
    seen = {}
    for t in c["ticks"]:
        pc = t["plan_completion"]
        if not pc:
            continue
        key_task = t["human_actual_task"]
        for a in pc:
            k = (key_task, a["index"], a["action"])
            if k not in seen:
                seen[k] = {"pred": a["completion"], "first_true": None, "n_true": 0,
                           "first_current": None, "last_current": None}
            s = seen[k]
            if a["holds"]:
                s["n_true"] += 1
                if s["first_true"] is None:
                    s["first_true"] = t["step"]
            if a["is_current"]:
                if s["first_current"] is None:
                    s["first_current"] = t["step"]
                s["last_current"] = t["step"]
    for (task, idx, act), s in seen.items():
        rows.append([n, short(task), idx, act, s["pred"] or "ProcessCompletion", s["first_current"],
                     s["last_current"], s["first_true"], s["n_true"]])
write("f_completion_reachability_human_plan.csv",
      ["condition", "human_task", "action_index", "action", "completion_predicate",
       "first_tick_executing", "last_tick_executing", "first_tick_predicate_true", "ticks_predicate_true"],
      rows, "(f) Completion predicates of the human's LIVE plan, evaluated externally against the WorldState the recognizer saw")

# =============================================================================
# (f2) completion conditions ground-able from hypothesis bindings (static)
# =============================================================================
rows = []
for n in COND:
    c = C[n]
    if not n.endswith("_off"):
        continue
    truth = Counter()
    for t in c["ticks"]:
        for h, mi, si in t["hyp_completion_true"]:
            truth[(h, mi, si)] += 1
    seen_task = set()
    for r in c["method_table"]:
        task = C[n]["hypotheses"][[h["key"] for h in c["hypotheses"]].index(r["hyp"])]["task"]
        key = (task, r["method_index"], r["step_index"])
        if key in seen_task:
            continue
        seen_task.add(key)
        # aggregate truth across hypotheses of the same task
        n_true = sum(v for (h, mi, si), v in truth.items()
                     if mi == r["method_index"] and si == r["step_index"]
                     and C[n]["hypotheses"][[x["key"] for x in c["hypotheses"]].index(h)]["task"] == task)
        rows.append([n, task, r["method_index"], r["method"], "; ".join(r["guards"]) or "-", r["step_index"],
                     r["action"], str(r["microactions"]), r["completion_type"], r["grounding"],
                     r["completion_grounded"].replace(r["hyp"].split("(")[0], "") if r["completion_grounded"] else "",
                     n_true])
write("f2_completion_groundable_from_hypothesis.csv",
      ["condition", "task", "method_index", "method", "guards", "step_index", "action", "microactions",
       "completion_type", "groundable_from_hyp_bindings", "example_grounding", "hyp_ticks_true_sum"],
      rows, "(f2) Every action of every method, grounded from hypothesis bindings only (analysis-side); ticks (summed over hypotheses of that task) where the grounded predicate held")

# =============================================================================
# (g) belief events — attribution
# =============================================================================
rows = []
for n in COND:
    c = C[n]
    theta = c["constants"]["theta_meta_planner"]
    prev = None
    for t in c["ticks"]:
        ml, conf = short(t["most_likely"]), t["confidence"]
        ev = []
        if prev is None:
            ev.append("first")
        else:
            if ml != prev[0]:
                ev.append("most_likely_change")
            if prev[1] < theta <= conf:
                ev.append("theta_up")
            if conf < theta <= prev[1]:
                ev.append("theta_down")
        if ev:
            zone_now = sorted(short(k) for k, o in t["omega"].items() if o["zone_fired"])
            zone_prev = sorted(short(k) for k, o in prev[2].items() if o["zone_fired"]) if prev else []
            rows.append([n, t["step"], "+".join(ev), t["kind"], t["obs_microaction"], ml, conf,
                         prev[0] if prev else "", prev[1] if prev else "",
                         human_task_short(t), t["human_action"], ml == human_task_short(t),
                         "leg_start" if (t["kind"] == "moving" and (prev is None or prev[3] != "moving")) else "",
                         ",".join(zone_now), ",".join(zone_prev),
                         len(t["refuted"] or []), len(prev[4] or []) if prev else 0,
                         t["held_item_seen"] or ""])
        prev = (ml, conf, t["omega"], t["kind"], t["refuted"])
write("g_belief_events.csv",
      ["condition", "step", "event", "kind", "microaction", "most_likely", "confidence", "prev_most_likely",
       "prev_confidence", "human_task", "human_action", "correct", "leg_start", "zone_boosted_now",
       "zone_boosted_prev", "n_refuted_now", "n_refuted_prev", "held_item"],
      rows, "(g) Belief events (most_likely changes, θ crossings) with the state factors active at that tick")

# =============================================================================
# (h) kernel values
# =============================================================================
rows = []
for n in COND:
    c = C[n]
    vals = [l for t in c["ticks"] for l in t["likelihoods"]
            if l["branch"] == "progress" and l.get("cosine") is not None]
    cos = [l["cosine"] for l in vals]
    v = [l["value"] for l in vals]
    correct = [l for t in c["ticks"] for l in t["likelihoods"]
               if l.get("cosine") is not None and short(l["hyp"]) == human_task_short(t)]
    wrong = [l for t in c["ticks"] for l in t["likelihoods"]
             if l.get("cosine") is not None and short(l["hyp"]) != human_task_short(t)]
    def stats(xs):
        return (min(xs), sum(xs) / len(xs), max(xs)) if xs else (None, None, None)
    rows.append([n, len(vals), *stats(cos), *stats(v),
                 sum(1 for x in v if abs(x - 4.0) < 1e-9), sum(1 for x in v if x < 1.0),
                 *stats([l["value"] for l in correct]), *stats([l["value"] for l in wrong])])
write("h_kernel_values.csv",
      ["condition", "chords", "cos_min", "cos_mean", "cos_max", "L_min", "L_mean", "L_max",
       "L_equals_HIGH", "L_below_NEUTRAL", "L_correct_min", "L_correct_mean", "L_correct_max",
       "L_wrong_min", "L_wrong_mean", "L_wrong_max"],
      rows, "(h) Chord likelihood values actually produced by the linear cosine kernel")

# =============================================================================
# (i) per-tick summary (for spot checks) — compact
# =============================================================================
rows = []
for n in COND:
    c = C[n]
    for t in c["ticks"]:
        zone = sorted(short(k) for k, o in t["omega"].items() if o["zone_fired"])
        rows.append([n, t["step"], t["kind"], t["obs_microaction"], t["obs_zone"],
                     human_task_short(t), t["human_action"], t["human_action_index"], t["human_holding"] or "",
                     short(t["most_likely"]), t["confidence"], ",".join(zone),
                     len(t["refuted"] or []), len(t["likelihoods"]),
                     ";".join(f"{short(l['hyp'])}={l['value']:.3f}" for l in t["likelihoods"])])
write("i_ticks.csv",
      ["condition", "step", "kind", "microaction", "zone", "human_task", "human_action", "human_action_index",
       "human_holding", "most_likely", "confidence", "zone_boosted", "n_refuted", "n_likelihoods", "likelihoods"],
      rows, None)

# =============================================================================
# (j) discrete-tick likelihoods
# =============================================================================
rows = []
for n in COND:
    c = C[n]
    for t in c["ticks"]:
        if t["kind"] != "discrete":
            continue
        vals = Counter(round(l["value"], 3) for l in t["likelihoods"])
        rows.append([n, t["step"], t["obs_microaction"], human_task_short(t), t["human_action"],
                     dict(vals), t["weigh"]["origin"] if t["weigh"] else None,
                     round(t["confidence"], 3), short(t["most_likely"])])
write("j_discrete_ticks.csv",
      ["condition", "step", "microaction", "human_task", "human_action", "likelihood_values",
       "origin_passed", "confidence", "most_likely"],
      rows, "(j) Discrete (event) ticks — the likelihood every hypothesis received from the event itself")

# =============================================================================
# summary.md
# =============================================================================
with open(HERE / "summary.md", "w") as f:
    f.write("# Auto-generated summary tables (analyze.py)\n\n")
    for title, header, rows in OUT:
        if title is None:
            continue
        f.write(f"## {title}\n\n")
        f.write("| " + " | ".join(header) + " |\n")
        f.write("|" + "---|" * len(header) + "\n")
        for r in rows:
            f.write("| " + " | ".join(fmt(v) for v in r) + " |\n")
        f.write("\n")
print("wrote", [n for n in sorted(p.name for p in HERE.glob('*.csv'))], "and summary.md", file=sys.stderr)
