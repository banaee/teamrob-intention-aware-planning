#!/usr/bin/env python3
"""
RETIRED (graded evidence, September 2026): the unit checks here encode the pre-grade values (a fitting stretch worth
1/u on its first step; unknown a constant per observation) and the sweep matrix describes the pre-grade HEAD.
They are the record of their report and no longer run at HEAD: `--unit` prints this note. The checks that survive
the grade are restated with graded expectations in analysis/g1_graded_evidence/unit_checks.py, which is the live
set.

analysis/i4_evidence_model/check_i4.py — the I4 sweep, the acceptance measurements and the variants.

Everything runs the robot's live recognizer inside SimModel (I1–I3's technique); the [IR]/[IR-dist]/
[meta]/[meta-cand] lines are replicated so an instrumented log cmp's against run_mesa.py's. The
likelihood constants are set on shared.likelihood_functions before the model is built (the recognizer
reads them through the module at call time), so a sweep point is one process-local assignment.

Modes
  --sweep [abs|frac]   joint grid over (beta, unknown) on the subset conditions (prior-on: s40, s30, s00),
                       one row per (point, condition) in sweep_<abs|frac>.csv plus derived tables
  --final              the eight conditions at the shipped constants: instrumented logs (logs_instrumented/base,
                       cmp'd against run_mesa.py's in new/), the
                       CSVs (expected_actions, phase_advances, completion_events, completions, excess),
                       summary.md; with --variants also the analysis-only monkeypatches:
                         ungated          every expected action judged at a discrete tick (TODO-56 re-check)
                         ownshelf         rivals decomposed as if nothing were held (TODO-55 re-measure)
                         reset_origin     what-if: every live origin moves to the agent's position and
                                          odometer when a hypothesis retires (the observed agent's task
                                          boundary as the recognizer can see it) — NOT shipped (TODO-53's
                                          named alternative)
                         reset_boundary   what-if: reset_origin plus the evidence state reset to uniform
                                          over the live keys and unknown at the same event — NOT shipped
                                          (TODO-55 reading (b))
                         costdif2         diagnostic: the `walked` term dropped (Masters & Sardina's
                                          costdif2; ranking-preserving, observation-independent)
                         rawlogistic      the raw logistic (0.5 at zero excess) instead of the normalised one
  --unit               unit checks U1–U6

    PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python analysis/i4_evidence_model/check_i4.py --sweep abs
"""
import csv
import logging
import math
import os
import re
import sys
from collections import defaultdict
from copy import copy
from itertools import product
from multiprocessing import Pool
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "mesa_sim"))
HERE = Path(__file__).parent

from shared.types import task_instance_key                                  # noqa: E402
from shared import likelihood_functions as LF                               # noqa: E402

THETA = 0.75
CONDITIONS = {
    "s00_off": ("env_layout0", "scenario_00", 300, False),
    "s00_on":  ("env_layout0", "scenario_00", 300, True),
    "s20_off": ("env_layout2", "scenario_20", 200, False),
    "s20_on":  ("env_layout2", "scenario_20", 200, True),
    "s30_off": ("env_layout3", "scenario_30", 200, False),
    "s30_on":  ("env_layout3", "scenario_30", 200, True),
    "s40_off": ("env_layout4", "scenario_40", 400, False),
    "s40_on":  ("env_layout4", "scenario_40", 400, True),
}
ORDER = list(CONDITIONS)
SWEEP_SUBSET = ["s40_on", "s30_on", "s00_on"]
# scenario_40's segments are the ground truth (F1): the wander legs are scripted as type-invalid
# ac_activation bindings and no hypothesis targets them, so their truth is `unknown`.
S40_SEGMENTS = {0: "seg1", 1: "seg2", 2: "seg3a", 3: "seg3b", 4: "seg4"}
S40_TRUTH = {"seg1": "d(item_3)", "seg2": "coffee", "seg3a": "unknown", "seg3b": "unknown",
             "seg4": "d(item_6)", "done": "unknown"}

GRID_ABS = {"beta": [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1],
            "unknown": [0.01, 0.02, 0.05, 0.1, 0.2, 0.35, 0.5]}
GRID_FRAC = {"beta": [0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0],
             "unknown": [0.01, 0.02, 0.05, 0.1, 0.2, 0.35, 0.5]}
# fine grid inside the working region the coarse absolute grid located (first-task criteria)
GRID_ABS_FINE = {"beta": [0.005, 0.007, 0.01, 0.014, 0.02],
                 "unknown": [0.05, 0.07, 0.1, 0.14, 0.2]}


def short(key):
    k = key.replace("deliver_item(?item=", "d(").replace(",?kitting_table=kitting_table_0)", ")")
    k = k.replace("coffee_break(?coffee_machine=coffee_machine_0)", "coffee")
    k = k.replace("ac_activation(?ac_switch=ac_switch_0)", "ac")
    return k


def act_str(a):
    if a is None:
        return "-"
    b = ",".join(f"{k}={v}" for k, v in sorted(a.bindings.items()) if k != "?agent")
    return f"{a.action_name}({b})"


# ---------------------------------------------------------------------------
# One instrumented run
# ---------------------------------------------------------------------------

def fractional_excess_path_likelihood(walked, origin, pos, target_pos, cost=LF.straight_line_cost):
    """The fractional reading of beta: excess as a fraction of the direct cost C(origin, target)."""
    direct = cost(origin, target_pos)
    excess = walked + cost(pos, target_pos) - direct
    return LF.logistic_of_excess(excess / max(direct, 1.0))


def costdif2_likelihood(walked, origin, pos, target_pos, cost=LF.straight_line_cost):
    """Masters & Sardina's costdif2: the walked term dropped. Diagnostic only."""
    return LF.logistic_of_excess(cost(pos, target_pos) - cost(origin, target_pos))


def apply_constants(beta, unknown, frac=False):
    LF.BETA = beta
    LF.UNKNOWN_LIKELIHOOD = unknown
    LF.PROGRESS_EVALUATORS["excess_path"] = fractional_excess_path_likelihood if frac else LF.excess_path_likelihood


def run_condition(name, beta, unknown, frac=False, variant="base", log_dir=None, collect=False, setup=None):
    """Returns (trace rows, stats). trace rows: one per tick the IR ran.
    `setup(rec, model, human)`: an optional caller-supplied monkeypatch applied after the named variant
    (check_i4b.py's boundary candidates)."""
    apply_constants(beta, unknown, frac)
    from mesa_sim.sim_model import SimModel
    from domains.kitting.registry import domain_config
    layout, scenario, steps, prior = CONDITIONS[name]
    lay = domain_config["layouts"][layout]
    scen = lay["scenarios"][scenario]
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)
    fh = None
    if log_dir is not None:
        log_path = Path(log_dir) / f"{name}.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_path, mode="w"); fh.setFormatter(logging.Formatter("%(message)s"))
        root.addHandler(fh); root.setLevel(logging.INFO)
    else:
        root.addHandler(logging.NullHandler()); root.setLevel(logging.CRITICAL)
    logging.info(f"[run_mesa] Starting headless run — domain=kitting scenario={scenario} steps={steps}")

    if variant == "costdif2":
        LF.PROGRESS_EVALUATORS["excess_path"] = costdif2_likelihood
    if variant == "rawlogistic":
        LF.PERFECT_FIT_LIKELIHOOD = 0.5
        LF.PROGRESS_EVALUATORS["excess_path"] = (
            lambda walked, origin, pos, target_pos, cost=LF.straight_line_cost:
            0.5 * LF.excess_path_likelihood(walked, origin, pos, target_pos, cost))

    model = SimModel(scenario=scen, register_fn=domain_config["register_fn"],
                     env_layout_path=lay["path"], assignment_prior=prior)
    robot = model.robots["robot_0"]; human = model.humans["human_0"]
    rec = robot.recognizer
    hyps = [repr(h) for h in rec._hypotheses] + ["unknown"]

    stats = {"expected": [], "advances": [], "events": [], "completions": [], "excess": [],
             "progress_calls": 0, "kernel_evals": 0, "completion_calls": 0, "completion_evals": 0}
    for k, a in rec._expected.items():
        stats["expected"].append((-1, k, act_str(a), rec._origin.get(k), rec._origin_odo.get(k)))

    # --- variants (analysis-only monkeypatches) ---
    if variant == "ungated":
        discrete = {"GRASP", "RELEASE"}
        rec._in_vocabulary = lambda action, mu: mu in discrete
    if variant == "ownshelf":
        from shared.planner import DecompositionError
        def grounded(hyp, agent_id, world):
            key = repr(hyp)
            if key in rec._tick_actions:
                return rec._tick_actions[key]
            held = world.agent_states[agent_id].holding
            w = world
            if held is not None and held not in hyp.bindings.values():
                w = copy(world)
                w.predicates = {p for p in world.predicates
                                if not (p.name == "holding" and p.args[0].value == agent_id)}
            try:
                acts = rec._planner.decompose(hyp.task_name, hyp.bindings, agent_id, w)
            except DecompositionError:
                acts = None
            rec._tick_actions[key] = acts
            return acts
        rec._grounded_actions = grounded

    if setup is not None:
        setup(rec, model, human)

    # --- counters ---
    orig_kernel = LF.PROGRESS_EVALUATORS["excess_path"]
    def kernel(*a, **k):
        stats["kernel_evals"] += 1
        return orig_kernel(*a, **k)
    LF.PROGRESS_EVALUATORS["excess_path"] = kernel
    orig_cpl = LF.completion_predicate_likelihood
    def cpl(predicate, world_predicates):
        stats["completion_evals"] += 1
        return orig_cpl(predicate, world_predicates)
    LF.completion_predicate_likelihood = cpl
    orig_prog = rec._progress_likelihood
    def prog(action, origin, walked, pos, world, memo):
        stats["progress_calls"] += 1
        return orig_prog(action, origin, walked, pos, world, memo)
    rec._progress_likelihood = prog
    orig_comp = rec._completion_likelihood
    def comp(action, world, memo):
        stats["completion_calls"] += 1
        v = orig_comp(action, world, memo)
        stats["_events_this_tick"].append((act_str(action), str(action.completion_predicate), v))
        return v
    rec._completion_likelihood = comp
    stats["_events_this_tick"] = []

    orig_update = rec.update
    def update(obs, world, prev_belief=None):
        before = dict(rec._expected)
        completed_before = set(rec._completed)
        stats["_events_this_tick"] = []
        b = orig_update(obs, world, prev_belief)
        step = int(obs.timestamp)
        mu = (obs.detected_microaction or "").upper()
        newly = rec._completed - completed_before
        if variant in ("reset_origin", "reset_boundary") and newly:
            # What-if (NOT shipped): the observed agent's task boundary, as the recognizer can see
            # it (a retirement this tick). reset_origin moves every live origin to here;
            # reset_boundary also resets the evidence state to uniform over the live keys and
            # unknown (TODO-55 reading (b)). Prior-off the robot's deliveries retire hypotheses
            # too, so the boundary fires at the robot's completions as well — noted in the report.
            pos = obs.spatial_context.position; odo = rec._odometer[obs.agent_id]
            for k in list(rec._origin):
                rec._origin[k], rec._origin_odo[k] = pos, odo
            if variant == "reset_boundary":
                n = len(rec._base)
                for k in rec._base:
                    rec._base[k] = 1.0 / n
                rec._evidence = {k: rec._base[k] * (LF.UNKNOWN_LIKELIHOOD if k == "unknown" else
                                 rec._progress_likelihood(rec._expected.get(k), rec._origin.get(k, pos), 0.0, pos, world, {}))
                                 for k in rec._evidence}
                tot = sum(rec._evidence.values()); rec._evidence = {k: v / tot for k, v in rec._evidence.items()}
                b = rec._output(obs, world)
                from shared.types import BeliefState
                ml = max(b, key=lambda k: b[k])
                b = BeliefState(timestamp=obs.timestamp, agent_id=obs.agent_id, distribution=b, most_likely=ml, confidence=b[ml])
                robot.belief = b
        if collect:
            for k, a in rec._expected.items():
                stats["expected"].append((step, k, act_str(a), rec._origin.get(k), round(rec._origin_odo.get(k, 0), 1)))
                if k in before and not rec._same_action(before[k], a):
                    stats["advances"].append((step, k, act_str(before[k]), act_str(a)))
            for k in newly:
                stats["completions"].append((step, k, human.current_action, human.current_microaction))
            if stats["_events_this_tick"]:
                by_action = defaultdict(list)
                for k, a in before.items():
                    by_action[act_str(a)].append(k)
                for astr, pred, v in stats["_events_this_tick"]:
                    for k in by_action.get(astr, ["?"]):
                        stats["events"].append((step, mu, k, astr, pred, v, b.distribution.get(k)))
            # excess per live hypothesis (recomputed here from the recognizer's state, for the tables)
            from shared.target_resolution import movement_target_position
            pos = obs.spatial_context.position; odo = rec._odometer[obs.agent_id]
            for k, a in rec._expected.items():
                tp = movement_target_position(a, world) if a is not None else None
                if tp is None or a.schema.progress_evaluator is None:
                    ex = ""
                else:
                    o = rec._origin[k]; walked = odo - rec._origin_odo[k]
                    ex = round(walked + LF.straight_line_cost(pos, tp) - LF.straight_line_cost(o, tp), 1)
                stats["excess"].append((step, k, act_str(a), ex, round(rec._base.get(k, 0), 6), round(b.distribution.get(k, 0), 4)))
        return b
    rec.update = update

    rows = []
    stats["aborted"] = None
    for step in range(steps):
        try:
            model.step()
        except RuntimeError as e:           # TODO-52's latent meta-planner crash (every candidate excluded)
            stats["aborted"] = (step, str(e).split(":")[0])
            logging.info(f"[check_i4] run aborted at step {step}: {e}")
            break
        for aid, h in model.humans.items():
            logging.info(f"  step: {step}: [{aid}] task={h.current_task} action={h.current_action} "
                         f"micro={h.current_microaction} pos={np.round(h.pos, 2)}")
        for aid, r in model.robots.items():
            logging.info(f"  step: {step}: [{aid}] task={r.current_task} action={r.current_action} "
                         f"micro={r.current_microaction} pos={np.round(r.pos, 2)}")
        b = robot.belief
        if b is None or int(b.timestamp) != step:
            continue
        ti = human.get_current_task_instance()
        if name.startswith("s40"):
            seg = S40_SEGMENTS.get(human.script_index, "done") if not human.finished else "done"
            truth = S40_TRUTH[seg]
        else:
            seg = ""
            truth = short(task_instance_key(ti)) if (ti and not human.finished) else "unknown"
        rows.append({"step": step, "segment": seg, "truth": truth,
                     "human_action": human.current_action or "", "human_micro": human.current_microaction or "",
                     "human_holding": human.carrying or "",
                     "most_likely": short(b.most_likely), "confidence": b.confidence,
                     "dist": {short(k): b.distribution.get(k, float("nan")) for k in hyps}})
    logging.info("[run_mesa] Headless run complete.")
    if fh is not None:
        fh.flush(); root.removeHandler(fh)
    LF.PROGRESS_EVALUATORS["excess_path"] = LF.excess_path_likelihood
    LF.completion_predicate_likelihood = orig_cpl
    LF.PERFECT_FIT_LIKELIHOOD = 1.0
    return rows, stats


# ---------------------------------------------------------------------------
# Derived metrics
# ---------------------------------------------------------------------------

def crossings(rows):
    out, prev = [], None
    for r in rows:
        if prev is not None and prev < THETA <= r["confidence"]:
            out.append((r["step"], r["most_likely"], r["truth"], r["human_action"], round(r["confidence"], 3)))
        prev = r["confidence"]
    return out


def metrics(name, rows):
    m = {"condition": name}
    cr = crossings(rows)
    m["crossings"] = " ".join(f"{s}:{w}{'' if w == t else '!'}" for s, w, t, _, _ in cr)
    m["n_cross"] = len(cr)
    m["n_wrong_cross"] = sum(1 for s, w, t, _, _ in cr if w != t)
    above = [r for r in rows if r["confidence"] >= THETA]
    m["wrong_theta_ticks"] = sum(1 for r in above if r["most_likely"] != r["truth"])
    m["wrong_theta_task_ticks"] = sum(1 for r in above if r["most_likely"] != r["truth"] and r["most_likely"] != "unknown")
    m["correct_theta_ticks"] = sum(1 for r in above if r["most_likely"] == r["truth"])
    m["max_conf"] = round(max(r["confidence"] for r in rows), 3)
    # first correct reveal per human task, and where the grasp was
    reveals = []
    for task in dict.fromkeys(r["truth"] for r in rows if r["truth"] != "unknown"):
        trs = [r for r in rows if r["truth"] == task]
        grasp = next((r["step"] for r in trs if r["human_micro"] == "grasp"), None)
        rv = next((r for r in trs if r["confidence"] >= THETA and r["most_likely"] == task), None)
        if rv is None:
            reveals.append(f"{task}:never(max {max(r['dist'][task] for r in trs):.2f})")
        else:
            when = "pre-grasp" if (grasp is not None and rv["step"] < grasp) else ("no-grasp" if grasp is None else "post-grasp")
            reveals.append(f"{task}:{rv['step']}({when},grasp {grasp})")
    m["reveals"] = " ".join(reveals)
    m["unknown_when_idle"] = round(np.mean([r["dist"]["unknown"] for r in rows if r["truth"] == "unknown"]), 3) if any(r["truth"] == "unknown" for r in rows) else ""
    if name.startswith("s40"):
        seg = lambda s: [r for r in rows if r["segment"] == s]
        s2, s3a, s3b = seg("seg2"), seg("seg3a"), seg("seg3b")
        m["coffee_max_seg2"] = round(max(r["dist"]["coffee"] for r in s2), 3)
        m["coffee_theta_ticks_seg2"] = sum(1 for r in s2 if r["dist"]["coffee"] >= THETA)
        m["deliver_max_seg2"] = round(max(v for r in s2 for k, v in r["dist"].items() if k.startswith("d(")), 3)
        m["item6_3b_start_end"] = f"{s3b[0]['dist']['d(item_6)']:.3f}->{s3b[-1]['dist']['d(item_6)']:.3f}"
        m["item6_3a_end"] = round(s3a[-1]["dist"]["d(item_6)"], 3)
        m["item6_3b_falls"] = s3b[-1]["dist"]["d(item_6)"] < s3b[0]["dist"]["d(item_6)"]
        m["max_task_seg3"] = round(max(v for r in s3a + s3b for k, v in r["dist"].items() if k != "unknown"), 3)
        m["unknown_end_seg3"] = round(s3b[-1]["dist"]["unknown"], 3)
        win = [r for r in rows if 184 <= r["step"] <= 271]
        m["ac_max_184_271"] = round(max(r["dist"]["ac"] for r in win), 3)
        m["ac_most_likely_ticks_184_271"] = sum(1 for r in win if r["most_likely"] == "ac")
        g = next(r for r in rows if r["step"] == 272)
        m["at_272"] = f"{g['most_likely']} {g['confidence']:.3f} (item_6 {g['dist']['d(item_6)']:.3f})"
    return m


# ---------------------------------------------------------------------------
# Sweep
# ---------------------------------------------------------------------------

def _sweep_point(args):
    beta, unknown, frac, name = args
    rows, _ = run_condition(name, beta, unknown, frac)
    m = metrics(name, rows)
    m.update({"beta": beta, "unknown": unknown})
    return m


def sweep(frac, fine=False):
    grid = GRID_FRAC if frac else (GRID_ABS_FINE if fine else GRID_ABS)
    tag = "frac" if frac else ("abs_fine" if fine else "abs")
    jobs = [(b, u, frac, c) for b in grid["beta"] for u in grid["unknown"] for c in SWEEP_SUBSET]
    with Pool(int(os.environ.get("I4_JOBS", "4"))) as pool:
        results = pool.map(_sweep_point, jobs, chunksize=1)
    fields = ["beta", "unknown", "condition", "crossings", "n_cross", "n_wrong_cross", "wrong_theta_ticks",
              "wrong_theta_task_ticks", "correct_theta_ticks", "max_conf", "reveals", "unknown_when_idle",
              "coffee_max_seg2", "coffee_theta_ticks_seg2", "deliver_max_seg2", "item6_3a_end", "item6_3b_start_end",
              "item6_3b_falls", "max_task_seg3", "unknown_end_seg3", "ac_max_184_271", "ac_most_likely_ticks_184_271", "at_272"]
    with open(HERE / f"sweep_{tag}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore"); w.writeheader(); w.writerows(results)
    print(f"wrote sweep_{tag}.csv ({len(results)} rows)")
    return results


# ---------------------------------------------------------------------------
# Unit checks
# ---------------------------------------------------------------------------

def unit_checks():
    from shared.types import (Var, Const, ConditionSchema, StepCall, MethodSchema, TaskSchema, DomainModel,
                              WorldState, AgentState, Observation, SpatialContext, ActionContext, Predicate)
    from shared.domain_knowledge import DomainKnowledgeBase, ContextKnowledge
    from shared.recognizer import IntentionRecognizer, HypothesisKey
    from domains.kitting.actions import move_to, pick_up, place
    from domains.kitting.tasks import deliver_item
    apply_constants(0.01, 0.1)
    out = []

    def _obs(agent, pos, mu="step", t=0.0):
        return Observation(timestamp=t, agent_id=agent, detected_microaction=mu,
                           spatial_context=SpatialContext(position=pos, orientation=0.0, zone="z"),
                           action_context=ActionContext())

    def _world(agent, pos, predicates=(), objects=None, locations=None, holding=None, t=0.0):
        return WorldState(timestamp=t, agent_states={agent: AgentState(agent, "z", holding=holding)},
                          agent_positions={agent: pos}, predicates=set(predicates),
                          object_positions=dict(objects or {}), object_locations=dict(locations or {}),
                          object_zones={k: "z" for k in (objects or {})},
                          object_home_container=dict(locations or {}))
    kb = DomainKnowledgeBase(DomainModel(tasks={"deliver_item": deliver_item},
                                         actions={"move_to": move_to, "pick_up": pick_up, "place": place},
                                         microactions=["STEP", "GRASP", "RELEASE"], intentions={"deliver_item"}))
    objs = {"shelf_a": (400.0, 0.0), "item_a": (400.0, 0.0), "shelf_b": (0.0, 400.0), "item_b": (0.0, 400.0),
            "table_0": (0.0, -400.0)}
    locs = {"item_a": "shelf_a", "item_b": "shelf_b"}
    ha = HypothesisKey("deliver_item", {"?item": "item_a", "?kitting_table": "table_0"})
    hb = HypothesisKey("deliver_item", {"?item": "item_b", "?kitting_table": "table_0"})

    # U1 — walk straight east 200 cm: excess 0 for a, 2·(...) for b; a's value is exactly the perfect fit
    rec = IntentionRecognizer(knowledge=kb, context=ContextKnowledge.default(), hypotheses=[ha, hb])
    rec.update(_obs("h", (0.0, 0.0), t=0), _world("h", (0.0, 0.0), objects=objs, locations=locs, t=0))
    for i in range(1, 11):
        b = rec.update(_obs("h", (20.0 * i, 0.0), t=i), _world("h", (20.0 * i, 0.0), objects=objs, locations=locs, t=i))
    ex_b = 200 + math.hypot(200, 400) - 400
    exp_b = LF.logistic_of_excess(ex_b)
    pa, pb, pu = b.distribution[repr(ha)], b.distribution[repr(hb)], b.distribution["unknown"]
    ok = abs(pa / pu - 1.0 / 0.1) < 1e-9 and abs(pb / pu - exp_b / 0.1) < 1e-9
    out.append(("U1 straight walk: target's excess 0 (value 1.0 = perfect fit), off-target excess = walked + C(p,g) − C(o,g)",
                ok, f"P(a)/P(u)={pa/pu:.3f} (1/u={10}), P(b)/P(u)={pb/pu:.4f} (expected {exp_b/0.1:.4f}, excess {ex_b:.1f} cm)"))

    # U2 — replace, not multiply: standing still for 20 ticks changes nothing
    b0 = dict(b.distribution)
    for i in range(11, 31):
        b = rec.update(_obs("h", (200.0, 0.0), "stand", t=i), _world("h", (200.0, 0.0), objects=objs, locations=locs, t=i))
    same = all(abs(b.distribution[k] - b0[k]) < 1e-12 for k in b0)
    out.append(("U2 twenty stationary ticks leave the belief unchanged (replace, not multiply)", same, ""))

    # U3 — a detour is charged by its length, not its direction: out 200 and back 200 → excess 400 for a
    rec = IntentionRecognizer(knowledge=kb, context=ContextKnowledge.default(), hypotheses=[ha, hb])
    rec.update(_obs("h", (0.0, 0.0), t=0), _world("h", (0.0, 0.0), objects=objs, locations=locs, t=0))
    path = [(20.0 * i, 0.0) for i in range(1, 11)] + [(200.0 - 20.0 * i, 0.0) for i in range(1, 11)]
    for i, p in enumerate(path, 1):
        b = rec.update(_obs("h", p, t=i), _world("h", p, objects=objs, locations=locs, t=i))
    pa, pu = b.distribution[repr(ha)], b.distribution["unknown"]
    ok = abs(pa / pu - LF.logistic_of_excess(400.0) / 0.1) < 1e-9
    out.append(("U3 out 200 cm and back: the target's excess is 400 cm although the agent is where it started",
                ok, f"P(a)/P(u)={pa/pu:.4f}, expected {LF.logistic_of_excess(400.0)/0.1:.4f}"))

    # U4 — fold continuity: a phase advance with zero excess does not move the evidence
    rec = IntentionRecognizer(knowledge=kb, context=ContextKnowledge.default(), hypotheses=[ha, hb])
    rec.update(_obs("h", (0.0, 0.0), t=0), _world("h", (0.0, 0.0), objects=objs, locations=locs, t=0))
    for i in range(1, 20):
        p = (20.0 * i, 0.0)
        preds = [Predicate("at", (Const("h"), Const("shelf_a"))), Predicate("at", (Const("h"), Const("item_a")))] if 400 - 20 * i <= 30 else []
        b = rec.update(_obs("h", p, t=i), _world("h", p, predicates=preds, objects=objs, locations=locs, t=i))
        if i == 18:
            r18 = b.distribution[repr(ha)] / b.distribution["unknown"]
    # at i=19 (380 cm) at(h, item_a) holds → ha expects pick_up; the closing move_to had excess 0
    r19 = b.distribution[repr(ha)] / b.distribution["unknown"]
    ok = abs(r19 - r18) < 1e-9 and act_str(rec._expected[repr(ha)]).startswith("pick_up")
    out.append(("U4 a phase advance whose closing phase had zero excess leaves the evidence unchanged against unknown (fold = 1.0)",
                ok, f"P(a)/P(u) {r18:.4f} → {r19:.4f}, now expects {act_str(rec._expected[repr(ha)])}"))

    # U5 — detection: the grasped item's hypothesis keeps its evidence (hit rate 1.0), a rival that also
    # expected a grasp (both items within reach) is charged the false-alarm rate
    objs2 = {"shelf_0": (200.0, 0.0), "item_a": (200.0, 0.0), "item_b": (200.0, 0.0), "table_0": (0.0, 400.0)}
    locs2 = {"item_a": "shelf_0", "item_b": "shelf_0"}
    rec = IntentionRecognizer(knowledge=kb, context=ContextKnowledge.default(), hypotheses=[ha, hb])
    at = [Predicate("at", (Const("h"), Const("shelf_0"))), Predicate("at", (Const("h"), Const("item_a"))), Predicate("at", (Const("h"), Const("item_b")))]
    rec.update(_obs("h", (180.0, 0.0), "stand", t=0), _world("h", (180.0, 0.0), predicates=at, objects=objs2, locations=locs2, t=0))
    b0 = rec.update(_obs("h", (180.0, 0.0), "stand", t=1), _world("h", (180.0, 0.0), predicates=at, objects=objs2, locations=locs2, t=1))
    w1 = _world("h", (180.0, 0.0), predicates=at[:1] + at[2:] + [Predicate("holding", (Const("h"), Const("item_a")))],
                objects={**objs2, "item_a": (180.0, 0.0)}, locations={"item_a": "h", "item_b": "shelf_0"}, holding="item_a", t=2)
    w1.object_home_container = dict(locs2)
    b1 = rec.update(_obs("h", (180.0, 0.0), "grasp", t=2), w1)
    ev = rec._evidence    # the evidence state (the output floors hb at BELIEF_FLOOR)
    ratio = ev[repr(ha)] / ev[repr(hb)]
    ok = abs(ratio - LF.DETECTION_HIT_RATE / LF.DETECTION_FALSE_ALARM_RATE) < 1e-6 and abs(ev[repr(ha)] / ev["unknown"] - b0.distribution[repr(ha)] / b0.distribution["unknown"]) < 1e-9
    out.append(("U5 grasp: hit rate (1.0) for the grasped item — unchanged against unknown — and the false-alarm rate for the rival that expected a grasp (evidence ratio 1000; output floored)",
                ok, f"evidence ratio a:b {ratio:.1f}, output P(b)={b1.distribution[repr(hb)]:.3f}; a:unknown before {b0.distribution[repr(ha)]/b0.distribution['unknown']:.3f} after {ev[repr(ha)]/ev['unknown']:.3f}"))

    # U6 — source grep: no predicate / removed mechanism / old constant in the recognizer
    src = (ROOT / "shared" / "recognizer.py").read_text()
    code = "\n".join(l for l in src.splitlines() if not l.strip().startswith("#"))
    code_no_doc = re.sub(r'"""[\s\S]*?"""', "", code)
    bad = [w for w in ('"holding"', '"in_zone"', '"at"', '"obj_at"', '"waited"', '"?item"', '"move_to"', "ZONE_BOOST",
                       "_refuted_by_holding", "HIGH_LIKELIHOOD", "LOW_LIKELIHOOD", "NEUTRAL_LIKELIHOOD") if w in code_no_doc]
    out.append(("U6 recognizer.py code names no predicate / parameter / action / removed mechanism / old constant", not bad, f"found: {bad}" if bad else ""))
    return out


# ---------------------------------------------------------------------------
# Final matrix
# ---------------------------------------------------------------------------

def compare_logs(a, b):
    def greps(p):
        return [l for l in open(p) if l.startswith(("[IR] ", "[IR-dist]", "[meta]", "[meta-cand]"))]
    return greps(a) == greps(b)


def final(variants):
    beta, unknown = LF.BETA, LF.UNKNOWN_LIKELIHOOD
    lines = [f"# I4 checks — generated by check_i4.py (BETA={beta}, UNKNOWN_LIKELIHOOD={unknown}, "
             f"hit {LF.DETECTION_HIT_RATE}, false alarm {LF.DETECTION_FALSE_ALARM_RATE})\n"]
    lines.append("## Unit checks\n\n| check | result | detail |\n|---|---|---|")
    ok_all = True
    for n, ok, d in unit_checks():
        ok_all &= ok
        lines.append(f"| {n} | {'PASS' if ok else 'FAIL'} | {d} |")
    lines.append("")
    csv_rows = defaultdict(list)
    all_metrics = []
    for variant in ["base"] + variants:
        lines.append(f"## {'Instrumented sweep (variant `base` = the shipped code)' if variant == 'base' else f'Variant `{variant}` (analysis-only monkeypatch)'}\n")
        lines.append("| condition | log == run_mesa | progress calls / evals | completion calls / evals | advances | completions | θ crossings (`!` = winner ≠ truth) | reveals | wrong-θ ticks (task) | max conf |")
        lines.append("|---|---|---|---|---|---|---|---|---|---|")
        for name in ORDER:
            log_dir = HERE / f"logs_instrumented/{variant}"
            rows, st = run_condition(name, beta, unknown, variant=variant, log_dir=log_dir, collect=True)
            m = metrics(name, rows); m["variant"] = variant
            all_metrics.append(m)
            same = ""
            if variant == "base":
                ref = HERE / "new" / f"{name}.log"        # run_mesa.py's log at the shipped constants (sweep.sh)
                same = compare_logs(log_dir / f"{name}.log", ref) if ref.exists() else "n/a"
                if same is False:
                    ok_all = False
            comps = ", ".join(f"{s}:{short(k)}" for s, k, _, _ in st["completions"])
            if st["aborted"]:
                comps += f" — ABORTED at step {st['aborted'][0]} ({st['aborted'][1]}, TODO-52)"
            lines.append(f"| {name} | {same} | {st['progress_calls']} / {st['kernel_evals']} | {st['completion_calls']} / {st['completion_evals']} | "
                         f"{len(st['advances'])} | {comps} | {m['crossings'] or '-'} | {m['reveals']} | {m['wrong_theta_ticks']} ({m['wrong_theta_task_ticks']}) | {m['max_conf']} |")
            tag = name if variant == "base" else f"{variant}/{name}"
            big = variant == "base" or name.startswith("s40")   # per-tick CSVs: variants only for s40 (size)
            if big:
                csv_rows["expected_actions"] += [(tag, s, short(k), a, o, oo) for s, k, a, o, oo in st["expected"]]
            csv_rows["phase_advances"] += [(tag, s, short(k), a, b) for s, k, a, b in st["advances"]]
            csv_rows["completion_events"] += [(tag, s, mu, short(k), a, p, v, f"{o:.3f}" if o is not None else "") for s, mu, k, a, p, v, o in st["events"]]
            csv_rows["completions"] += [(tag, s, short(k), act, mu) for s, k, act, mu in st["completions"]]
            if big:
                csv_rows["excess"] += [(tag, s, short(k), a, ex, base, p) for s, k, a, ex, base, p in st["excess"]]
                csv_rows["trace"] += [(tag, r["step"], r["segment"], r["truth"], r["human_action"], r["human_micro"], r["human_holding"],
                                       r["most_likely"], round(r["confidence"], 4)) + tuple(round(v, 4) for v in r["dist"].values()) for r in rows]
            if name.startswith("s40"):
                lines_s40 = "; ".join(f"{k}={m[k]}" for k in ("coffee_max_seg2", "coffee_theta_ticks_seg2", "deliver_max_seg2", "item6_3a_end",
                                                                "item6_3b_start_end", "max_task_seg3", "unknown_end_seg3", "ac_max_184_271",
                                                                "ac_most_likely_ticks_184_271", "at_272"))
                lines.append(f"| ↳ s40 | {lines_s40} | | | | | | | | |")
        lines.append("")
    headers = {
        "expected_actions": ["condition", "step", "hypothesis", "expected_action", "origin", "origin_odo"],
        "phase_advances": ["condition", "step", "hypothesis", "from", "to"],
        "completion_events": ["condition", "step", "microaction", "hypothesis", "judged_action", "predicate", "likelihood", "output_belief"],
        "completions": ["condition", "step", "hypothesis", "human_action", "human_micro"],
        "excess": ["condition", "step", "hypothesis", "expected_action", "excess_cm", "base", "belief"],
        "trace": ["condition", "step", "segment", "truth", "human_action", "human_micro", "human_holding", "most_likely", "confidence", "dist..."],
    }
    for fname, header in headers.items():
        with open(HERE / f"{fname}.csv", "w", newline="") as f:
            w = csv.writer(f); w.writerow(header); w.writerows(csv_rows[fname])
    with open(HERE / "metrics.csv", "w", newline="") as f:
        keys = sorted({k for m in all_metrics for k in m}, key=lambda k: (k not in ("variant", "condition"), k))
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(all_metrics)
    lines.append(f"\nOVERALL: {'PASS' if ok_all else 'FAIL'}\n")
    (HERE / "summary.md").write_text("\n".join(lines))
    print("\n".join(lines))
    return 0 if ok_all else 1


if __name__ == "__main__":
    if "--unit" in sys.argv:
        print("RETIRED: the I4 unit checks encode the pre-grade evidence model; run analysis/g1_graded_evidence/unit_checks.py")
        sys.exit(0)
        for n, ok, d in unit_checks():
            print(f"{'PASS' if ok else 'FAIL'}  {n}  {d}")
    elif "--sweep" in sys.argv:
        frac = "frac" in sys.argv
        sweep(frac, fine="fine" in sys.argv)
    elif "--final" in sys.argv:
        v = ["ungated", "ownshelf", "reset_origin", "reset_boundary", "costdif2", "rawlogistic"] if "--variants" in sys.argv else []
        sys.exit(final(v))
