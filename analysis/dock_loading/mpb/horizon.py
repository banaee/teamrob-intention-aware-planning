#!/usr/bin/env python3
"""
horizon.py — dock_loading's safety cap for an MPB run (MPB-5, TODO-138, ruled for MPB runs; for a script that depends on
the robot, DL-P7; design_decisions.md, "T-G: the second domain's rulings", THE MPB ON DOCK_LOADING): the robot's pool
chained along its AUTHORED order from the robot's start on plain cost, plus the human's replay length, plus the idle
margin. A safety cap, not a behavioural timeout and not an expectation: a run that reaches it is reported as such, and
the cap is not raised after a run.

    horizon.py <run file>          prints the cap (the run's steps)

The plain chain (the instrument's own computation, MPB-3): per task, the method the planner's decomposition selects in
the chain's state (AdaptivePlanner.decompose: the guards on the robot's area, what it holds, the pallet's states;
DL-P8: the cap is this decomposition's only use, and no module of the oracle imports this file), then per action: a
walk, ceil((d - arrival) / step) steps from the chain's position toward the target's position, the arrival radius
short of it, and its acknowledgement; a pick_up or a place, its microaction and its acknowledgement; per task, the
robot's task-completion tick. The chain's state follows: the robot's position and area, the pallet it holds, each
pallet's container. Never the projector, the realization or the selection.
The human's replay length: the replay's last acknowledgement tick + 1 (analysis/instruments/ir_testbed/trajectory.py,
the executor's own selection rule). For a script declared dependent on the robot (DL-P7) the replay runs on the state
after the robot's chain (each pallet of the pool in the container the chain leaves it in, as the run's overrides of
`setup.<pallet>.initial_container` read it); with the robot idle that script's scans never become applicable.
MARGIN is the IR test-bed's idle margin (E5's standing threshold at alpha = 0.01 is 25 ticks; 30 covers it).
"""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT), str(ROOT / "mesa_sim"), str(ROOT / "analysis" / "instruments" / "ir_testbed")]

import yaml
from mesa_sim.world_state_builder import PROXIMITY_THRESHOLD
from mesa_sim.overrides import HomeContainerOverride
from shared.knowledge import TaskModel
from shared.planner import AdaptivePlanner
from shared.types import AgentState, Const, Predicate, ScriptDependence, WorldState, area_fact
import oracle as ir
import trajectory

MARGIN = 30


def _walk(frm, to, step, radius):
    """The body's walk: whole steps toward `to` until within the radius; (steps, the stop position)."""
    d = math.dist(frm, to)
    if d <= radius:
        return 0, tuple(frm)
    n = math.ceil((d - radius) / step)
    return n, (frm[0] + (to[0] - frm[0]) * step * n / d, frm[1] + (to[1] - frm[1]) * step * n / d)


def plain_chain(run_file):
    """The robot's authored pool chained from its start: (total ticks, per-task ticks, the containers at the end)."""
    cfg = yaml.safe_load(open(run_file))
    domain_config = ir.domain_of(run_file)
    sc = domain_config["scenarios"][cfg["scenario"]]
    layout_id = cfg.get("layout") or sc.reference_layouts[0]
    layout = json.load(open(ROOT / domain_config["layouts"][layout_id]))
    setup = json.load(open(ROOT / domain_config["setups"][sc.setup]))
    fixed = {o["id"]: tuple(o["position"]) for o in layout["env_objects"]}
    pallets = {o["id"]: o for o in setup["env_objects"]}
    states = {(s["state"], s["object"]) for s in setup.get("states", [])}
    areas = ir.areas_of(domain_config, layout_id)
    step = float(yaml.safe_load(open(ROOT / "mesa_sim" / "mesa_configs.yaml"))["simulation"]["step_size"])
    planner = AdaptivePlanner(knowledge=TaskModel(domain_config["register_fn"](), domain_config["task_model"]))
    robot = next(a for a in sc.agents if a.agent_type == "robot")
    rid = robot.agent_id
    pos, holding = tuple(robot.start_position), None
    where = {p: o["initial_container"] for p, o in pallets.items()}          # a pallet's container, or the robot
    per = []
    for task in robot.assigned_tasks:
        preds = {Predicate("obj_at", (Const(p), Const(c))) for p, c in where.items() if c != rid}
        preds |= {Predicate(s, (Const(o),)) for s, o in states}
        if holding is not None:
            preds.add(Predicate("holding", (Const(rid), Const(holding))))
        fact = area_fact(rid, pos, areas)
        if fact is not None:
            preds.add(fact)
        positions = dict(fixed)
        positions.update({p: (pos if c == rid else fixed[c]) for p, c in where.items()})
        world = WorldState(timestamp=0.0, agent_states={rid: AgentState(agent_id=rid, holding=holding)},
                           agent_positions={rid: pos}, object_locations=dict(where), predicates=preds,
                           object_home_container={p: o["initial_container"] for p, o in pallets.items()},
                           object_destination={p: o["destination"] for p, o in pallets.items()},
                           object_positions=positions, areas=areas)
        ticks = 0
        for a in planner.decompose(task, rid, world):
            if a.action_name == "move_to":
                target = a.bindings["?target"]
                n, pos = _walk(pos, positions[target], step, PROXIMITY_THRESHOLD)
                ticks += n + 1                                             # the steps and the acknowledgement
            elif a.action_name == "pick_up":
                holding = a.bindings["?item"]; where[holding] = rid
                ticks += 2                                                 # the grasp and its acknowledgement
            elif a.action_name == "place":
                where[a.bindings["?item"]] = a.bindings["?target"]; holding = None
                ticks += 2                                                 # the release and its acknowledgement
            else:
                raise ValueError(f"horizon: no plain-cost rule for the robot's action {a.action_name}")
        per.append(ticks + 1)                                              # the task-completion tick
    return sum(per), per, where


def cap(run_file):
    robot_ticks, _, where = plain_chain(run_file)
    cfg = yaml.safe_load(open(run_file))
    sc = ir.domain_of(run_file)["scenarios"][cfg["scenario"]]
    human = next(a for a in sc.agents if a.agent_type == "human")
    overrides = ()
    if human.scheduled_tasks.dependence is ScriptDependence.ON_ROBOT:       # DL-P7
        robot = next(a for a in sc.agents if a.agent_type == "robot")
        moved = {c.value for t in robot.assigned_tasks for v, c in t.bindings.items() if v.name == "?pallet"}
        overrides = tuple(HomeContainerOverride(p, where[p]) for p in sorted(moved))
    return robot_ticks + (trajectory.expand(run_file, overrides=overrides) + 1) + MARGIN


if __name__ == "__main__":
    print(cap(sys.argv[1]))
