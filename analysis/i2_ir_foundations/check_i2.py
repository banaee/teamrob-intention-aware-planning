#!/usr/bin/env python3
"""
analysis/i2_ir_foundations/check_i2.py — acceptance checks and measurements for I2.

Part 1, unit checks on synthetic domains (no simulator):
  U1  a hypothesis whose only method has an unsatisfiable guard and no fallback
      (dock_loading's office_break shape) is scored NEUTRAL, does not raise, and
      is logged once; it scores again once the guard fact appears.
  U2  a hypothesis with an unbound step variable (no parameter_types, TODO-25)
      raises ValueError — a modelling error surfaces, it is not absorbed.
  U3  target_resolution.object_position resolves a carried object through its
      holder's position and a resting object through its own.

Part 2, instrumented runs of the eight sweep conditions (s00/s20/s30/s40 ×
prior off/on, PYTHONHASHSEED=0), wrappers on the robot's live recognizer, the
same technique as the I1 audit; the run's [IR]/[IR-dist]/[meta] lines are
replicated so the instrumented log can be cmp'd against run_mesa.py's:
  M1  every progress-likelihood call: did the target resolve? (must be 0 None)
  M2  which method the planner selected per hypothesis per tick (by shape of
      the grounded action list — analysis-side inference, not a mechanism)
  M3  ZONE_BOOST firings (tick × hypothesis), and which of them are new kinds:
      the held item's hypothesis boosted during its carry (target = table
      zone, the TODO-37(b) branch), or a robot-carried item's zone
  M4  the "already at target" HIGH branch of the kernel (lf: target_norm < 1e-6)
  M5  ticks at which waited(human_0, X) is in world.predicates
  M6  the generic held-item refutation equals the old "?item" rule on every tick
Writes summary.md and the CSVs listed there.

    PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python analysis/i2_ir_foundations/check_i2.py
"""
import csv
import logging
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "mesa_sim"))
HERE = Path(__file__).parent

from shared.types import (                                   # noqa: E402
    Var, Const, ConditionSchema, StepCall, MethodSchema, TaskSchema, ActionSchema,
    DomainModel, WorldState, AgentState, Observation, SpatialContext, ActionContext,
    Predicate, GroundedAction,
)
from shared.domain_knowledge import DomainKnowledgeBase, ContextKnowledge   # noqa: E402
from shared.recognizer import IntentionRecognizer, HypothesisKey, UNKNOWN   # noqa: E402
from shared.planner import DecompositionError                               # noqa: E402
from shared.target_resolution import object_position, movement_target_position, movement_target_id  # noqa: E402
from shared.likelihood_functions import HIGH_LIKELIHOOD, NEUTRAL_LIKELIHOOD  # noqa: E402
from domains.kitting.actions import move_to, wait_at                        # noqa: E402

CONDITIONS = [
    ("s00_off", "env_layout0", "scenario_00", 300, False),
    ("s00_on",  "env_layout0", "scenario_00", 300, True),
    ("s20_off", "env_layout2", "scenario_20", 200, False),
    ("s20_on",  "env_layout2", "scenario_20", 200, True),
    ("s30_off", "env_layout3", "scenario_30", 200, False),
    ("s30_on",  "env_layout3", "scenario_30", 200, True),
    ("s40_off", "env_layout4", "scenario_40", 400, False),
    ("s40_on",  "env_layout4", "scenario_40", 400, True),
]


# ---------------------------------------------------------------------------
# Part 1 — unit checks
# ---------------------------------------------------------------------------

class _Capture(logging.Handler):
    def __init__(self):
        super().__init__(); self.records = []
    def emit(self, record):
        self.records.append(record.getMessage())


def _obs(agent, pos, mu="step", t=0.0):
    return Observation(timestamp=t, agent_id=agent, detected_microaction=mu,
                       spatial_context=SpatialContext(position=pos, orientation=0.0, zone="z"),
                       action_context=ActionContext())


def _world(agent, pos, predicates=(), objects=None, t=0.0):
    return WorldState(timestamp=t, agent_states={agent: AgentState(agent, "z")},
                      agent_positions={agent: pos}, predicates=set(predicates),
                      object_positions=dict(objects or {}), object_zones={k: "z" for k in (objects or {})})


def unit_checks():
    out = []
    _agent, _chair, _target = Var("?agent"), Var("?chair"), Var("?target")
    # U1 — guarded-only method, no fallback
    guarded = TaskSchema(
        name="guarded_task", parameters=[_chair], parameter_types={"?chair": "chair"},
        methods=[MethodSchema(name="only", parameters=[_chair],
                              guards=[ConditionSchema("door_is_open", (Const("door_0"),))],
                              step_calls=[StepCall("move_to", {_target: _chair})])],
        is_foreseeable=True)
    kb = DomainKnowledgeBase(DomainModel(tasks={"guarded_task": guarded},
                                         actions={"move_to": move_to, "wait_at": wait_at},
                                         microactions=["STEP", "STAND"], intentions={"guarded_task"}))
    hyp = HypothesisKey("guarded_task", {"?chair": "chair_0"})
    rec = IntentionRecognizer(knowledge=kb, context=ContextKnowledge.default(), hypotheses=[hyp])
    cap = _Capture(); logging.getLogger().addHandler(cap)
    objs = {"chair_0": (100.0, 0.0)}
    beliefs = []
    for t, x in enumerate([0.0, 20.0, 40.0]):          # walking straight at the chair, door closed
        beliefs.append(rec.update(_obs("h", (x, 0.0), t=t), _world("h", (x, 0.0), objects=objs, t=t)))
    key = repr(hyp)
    neutral_ok = all(abs(b.distribution[key] - 0.5) < 1e-9 for b in beliefs)   # 2 keys, NEUTRAL: stays 1/2
    warned = [m for m in cap.records if "not decomposable" in m]
    # door opens: the guard holds, the method applies, the chord now scores HIGH
    b = rec.update(_obs("h", (60.0, 0.0), t=3),
                   _world("h", (60.0, 0.0), predicates=[Predicate("door_is_open", (Const("door_0"),))], objects=objs, t=3))
    scored_after = b.distribution[key] > 0.5
    logging.getLogger().removeHandler(cap)
    out.append(("U1 unsatisfiable guard, no fallback: NEUTRAL, no exception",
                neutral_ok, f"P(hyp)={[round(b.distribution[key], 3) for b in beliefs]}"))
    out.append(("U1 logged once, not per tick", len(warned) == 1, f"{len(warned)} warning(s)"))
    out.append(("U1 scores again once the guard holds", scored_after, f"P(hyp)={b.distribution[key]:.3f} (HIGH vs NEUTRAL → 0.8)"))

    # U2 — unbound variable (no parameter_types): a schema error, must raise
    _pallet = Var("?pallet")
    unbound = TaskSchema(name="unbound_task", parameters=[_pallet],
                         methods=[MethodSchema(name="m", parameters=[_pallet], guards=[],
                                               step_calls=[StepCall("move_to", {_target: _pallet})])])
    kb2 = DomainKnowledgeBase(DomainModel(tasks={"unbound_task": unbound}, actions={"move_to": move_to},
                                          microactions=["STEP"], intentions={"unbound_task"}))
    rec2 = IntentionRecognizer(knowledge=kb2, context=ContextKnowledge.default(),
                               hypotheses=[HypothesisKey("unbound_task", {})])
    raised = None
    try:
        rec2.update(_obs("h", (0.0, 0.0)), _world("h", (0.0, 0.0)))    # raises on the first tick (the output pass grounds every live hypothesis)
    except DecompositionError as e:
        raised = f"DecompositionError (wrong class): {e}"
    except ValueError as e:
        raised = "ValueError"
    out.append(("U2 unbound step variable raises ValueError (not absorbed)", raised == "ValueError", str(raised)))

    # U3 — position through the holder
    w = WorldState(timestamp=0, agent_states={}, agent_positions={"robot_0": (5.0, 5.0)},
                   object_locations={"item_1": "robot_0", "item_2": "shelf_2"},
                   object_positions={"item_1": (0.0, 0.0), "item_2": (7.0, 7.0), "shelf_2": (7.0, 7.0)})
    out.append(("U3 carried object resolves through its holder", object_position("item_1", w) == (5.0, 5.0),
                f"{object_position('item_1', w)}"))
    out.append(("U3 resting object resolves to its own position", object_position("item_2", w) == (7.0, 7.0),
                f"{object_position('item_2', w)}"))
    out.append(("U3 unknown object → None", object_position("nothing", w) is None, ""))
    return out


# ---------------------------------------------------------------------------
# Part 2 — instrumented sweep
# ---------------------------------------------------------------------------

def run_condition(name, layout, scenario, steps, prior):
    from mesa_sim.sim_model import SimModel
    from mesa_sim.world_state_builder import build_world_state
    from domains.kitting.registry import domain_config
    lay = domain_config["layouts"][layout]
    scen = lay["scenarios"][scenario]
    log_path = HERE / "logs_instrumented" / f"{name}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)
    fh = logging.FileHandler(log_path, mode="w"); fh.setFormatter(logging.Formatter("%(message)s"))
    root.addHandler(fh); root.setLevel(logging.INFO)
    logging.info(f"[run_mesa] Starting headless run — domain=kitting scenario={scenario} steps={steps}")

    model = SimModel(scenario=scen, register_fn=domain_config["register_fn"],
                     env_layout_path=lay["path"], assignment_prior=prior)
    robot = model.robots["robot_0"]; human = model.humans["human_0"]
    rec = robot.recognizer
    rec_hyps = list(rec._hypotheses)

    stats = {"progress_calls": 0, "target_none": 0, "at_target_high": [], "likelihood": Counter(),
             "methods": Counter(), "zone": [], "waited": [], "refute_mismatch": 0, "refute_ticks": 0,
             "undecomposable": 0}
    tick = {"step": None, "human_holding": None, "robot_holding": None}

    # M1 / M4 — progress likelihood: target resolution and the at-target branch
    orig_progress = rec._progress_likelihood
    def progress(obs, world, action, origin):
        stats["progress_calls"] += 1
        tp = movement_target_position(action, world)
        if tp is None:
            stats["target_none"] += 1
        elif origin is not None and math.hypot(tp[0] - origin[0], tp[1] - origin[1]) < 1e-6:
            cur = obs.spatial_context.position
            if math.hypot(cur[0] - origin[0], cur[1] - origin[1]) >= 1e-6:
                stats["at_target_high"].append((tick["step"], movement_target_id(action)))
        return orig_progress(obs, world, action, origin)
    rec._progress_likelihood = progress

    # M2 — method shape per hypothesis
    orig_grounded = rec._grounded_actions
    def grounded(hyp, agent_id, world):
        first = repr(hyp) not in rec._tick_actions
        acts = orig_grounded(hyp, agent_id, world)
        if first:
            if acts is None:
                stats["undecomposable"] += 1
            else:
                shape = f"{hyp.task_name}:{len(acts)}"
                stats["methods"][shape] += 1
        return acts
    rec._grounded_actions = grounded

    # likelihood values (NEUTRAL count)
    orig_lik = rec._likelihood
    def lik(obs, world, hyp, origin=None):
        v = orig_lik(obs, world, hyp, origin)
        stats["likelihood"][round(v, 3)] += 1
        return v
    rec._likelihood = lik

    # M3 — ω per (tick, hyp)
    orig_cw = rec._context_weight
    def cw(obs, world, hyp):
        w = orig_cw(obs, world, hyp)
        if w != 1.0:
            acts = rec._tick_actions.get(repr(hyp))
            target = movement_target_id(acts[0]) if acts else None
            held_by_human = world.agent_states[obs.agent_id].holding
            held_by_robot = world.agent_states["robot_0"].holding
            kind = "phase2_table" if (held_by_human is not None and held_by_human in hyp.bindings.values()) else (
                   "robot_carried" if (target is not None and world.object_locations.get(target) == "robot_0") else "phase1")
            stats["zone"].append((tick["step"], repr(hyp), w, target, kind))
        return w
    rec._context_weight = cw

    # M6 — generic refutation vs the old "?item" rule
    orig_ref = rec._refuted_by_holding
    def ref(obs, world):
        r = orig_ref(obs, world)
        held = next((p.args[1].value for p in world.predicates
                     if p.name == "holding" and p.args[0].value == obs.agent_id), None)
        old = set() if held is None else {repr(h) for h in rec_hyps
                                         if h.bindings.get("?item") is not None and h.bindings.get("?item") != held}
        if held is not None:
            stats["refute_ticks"] += 1
        if r != old:
            stats["refute_mismatch"] += 1
        return r
    rec._refuted_by_holding = ref

    for step in range(steps):
        tick["step"] = step
        model.step()
        for aid, h in model.humans.items():
            logging.info(f"  step: {step}: [{aid}] task={h.current_task} action={h.current_action} "
                         f"micro={h.current_microaction} pos={np.round(h.pos, 2)}")
        for aid, r in model.robots.items():
            logging.info(f"  step: {step}: [{aid}] task={r.current_task} action={r.current_action} "
                         f"micro={r.current_microaction} pos={np.round(r.pos, 2)}")
        # M5 — waited predicate, read from a fresh world snapshot
        w = build_world_state(model)
        for p in w.predicates:
            if p.name == "waited" and p.args[0].value == "human_0":
                stats["waited"].append((step, p.args[1].value, human.current_action, human.current_microaction))
    logging.info("[run_mesa] Headless run complete.")
    fh.flush(); root.removeHandler(fh)
    return stats, rec_hyps


def zone_episodes(zone_rows):
    """Maximal step ranges per (hypothesis, kind)."""
    by = defaultdict(list)
    for step, key, w, target, kind in zone_rows:
        by[(key, kind, target)].append(step)
    eps = []
    for (key, kind, target), steps in by.items():
        steps.sort(); start = prev = steps[0]
        for s in steps[1:]:
            if s != prev + 1:
                eps.append((key, kind, target, start, prev)); start = s
            prev = s
        eps.append((key, kind, target, start, prev))
    return sorted(eps, key=lambda e: (e[3], e[0]))


def short(key):
    return (key.replace("deliver_item(?item=", "d(").replace(",?kitting_table=kitting_table_0)", ")")
               .replace("coffee_break(?coffee_machine=coffee_machine_0)", "coffee")
               .replace("ac_activation(?ac_switch=ac_switch_0)", "ac"))


def main():
    lines = ["# I2 checks — generated by check_i2.py\n"]
    lines.append("## Unit checks\n\n| check | result | detail |\n|---|---|---|")
    ok_all = True
    for name, ok, detail in unit_checks():
        ok_all &= ok
        lines.append(f"| {name} | {'PASS' if ok else 'FAIL'} | {detail} |")
    lines.append("")

    lines.append("## Instrumented sweep\n")
    lines.append("| condition | progress calls | target None | at-target HIGH firings | NEUTRAL likelihoods | "
                 "methods selected (task:len) | undecomposable | zone firings (pairs) | phase-2 / robot-carried firings | "
                 "refutation ticks / mismatches | waited ticks |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
    zone_csv, at_csv, waited_csv, method_csv = [], [], [], []
    for name, layout, scenario, steps, prior in CONDITIONS:
        stats, hyps = run_condition(name, layout, scenario, steps, prior)
        eps = zone_episodes(stats["zone"])
        n_p2 = sum(1 for z in stats["zone"] if z[4] == "phase2_table")
        n_rc = sum(1 for z in stats["zone"] if z[4] == "robot_carried")
        methods = ", ".join(f"{k}={v}" for k, v in sorted(stats["methods"].items()))
        waited = ", ".join(f"{s}:{obj}" for s, obj, _, _ in stats["waited"])
        lines.append(f"| {name} | {stats['progress_calls']} | {stats['target_none']} | {len(stats['at_target_high'])} | "
                     f"{stats['likelihood'].get(1.0, 0)} | {methods} | {stats['undecomposable']} | {len(stats['zone'])} | "
                     f"{n_p2} / {n_rc} | {stats['refute_ticks']} / {stats['refute_mismatch']} | {waited or '-'} |")
        zone_csv += [(name, short(k), kind, target, a, b) for k, kind, target, a, b in eps]
        at_csv += [(name, s, t) for s, t in stats["at_target_high"]]
        waited_csv += [(name, s, obj, act, mu) for s, obj, act, mu in stats["waited"]]
        method_csv += [(name, k, v) for k, v in sorted(stats["methods"].items())]
        if stats["target_none"] or stats["refute_mismatch"] or stats["undecomposable"]:
            ok_all = False
    for fname, header, rows in [
        ("zone_boost_episodes.csv", ["condition", "hypothesis", "kind", "target", "start", "end"], zone_csv),
        ("at_target_firings.csv", ["condition", "step", "target"], at_csv),
        ("waited_ticks.csv", ["condition", "step", "object", "human_action", "human_micro"], waited_csv),
        ("method_selection.csv", ["condition", "task:actions", "count"], method_csv),
    ]:
        with open(HERE / fname, "w", newline="") as f:
            w = csv.writer(f); w.writerow(header); w.writerows(rows)
    lines.append("\nCSVs: zone_boost_episodes.csv (maximal ranges per hypothesis and kind), at_target_firings.csv, "
                 "waited_ticks.csv, method_selection.csv (deliver_item:4 = deliver_default, :2 = deliver_already_held, "
                 ":6 = deliver_with_return; coffee_break/ac_activation:2).\n")
    lines.append(f"\nOVERALL: {'PASS' if ok_all else 'FAIL'}\n")
    (HERE / "summary.md").write_text("\n".join(lines))
    print("\n".join(lines))
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
