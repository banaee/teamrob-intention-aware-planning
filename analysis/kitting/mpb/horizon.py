#!/usr/bin/env python3
"""
horizon.py — the meta-planner test-bed's safety cap for a run (MPB-5; TODO-138, ruled for MPB runs; design_decisions.md,
"The meta-planner test-bed (MPB)"): the robot's pool chained along its AUTHORED order from the robot's start on plain
cost, plus the human's replay length, plus the idle margin. A safety cap, not a behavioural timeout: a run that does not
complete within it is classified (class 2 or 4), never given a longer cap. The comparison horizon (the first observed
completion point plus the margin) is compare.py's, from the run.

    horizon.py <run file>          prints the cap (the run's steps)

The plain chain is computed from the layout's path lengths and the body's step rule, never from the projector or the
planner (the instrument's own computation, MPB-3): per robot task of the kitting schema deliver_item (deliver_default
from an empty hand, the chain's state throughout):
  a walk from the current position to the item's shelf, ceil((d - arrival) / step) steps, the arrival radius short of
  the shelf; its acknowledgement; the grasp; its acknowledgement; the carry from that arrival point to the item's
  designated table, ceil((d - arrival) / step) steps; its acknowledgement; the release; its acknowledgement; the
  robot's task-completion tick. The next task starts where the carry ended.
The human's replay length is the replay's last acknowledgement tick + 1 (analysis/ir_testbed/trajectory.py, the same
expansion the oracle reads). MARGIN is the IR test-bed's idle margin (E5's standing threshold at alpha = 0.01 is 25
ticks; 30 covers it).
"""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT), str(ROOT / "mesa_sim"), str(ROOT / "analysis" / "instruments" / "ir_testbed")]

import yaml
from domains.kitting.registry import domain_config
from mesa_sim.world_state_builder import PROXIMITY_THRESHOLD
import trajectory

MARGIN = 30
STATIONARY_PER_TASK = 3 + 3 + 1     # walk ack, grasp, ack; carry ack, release, ack; task completion


def _arrival(frm, to, radius):
    """Where a straight walk from `frm` toward `to` stops: the radius short of `to` (the chain's approximation of the
    body's first step within the radius, which it can only overshoot by less than one step)."""
    d = math.dist(frm, to)
    if d <= radius:
        return tuple(frm)
    return (to[0] - (to[0] - frm[0]) * radius / d, to[1] - (to[1] - frm[1]) * radius / d)


def plain_chain(run_file):
    """The robot's authored pool chained from its start: (total ticks, per-task ticks)."""
    cfg = yaml.safe_load(open(run_file))
    sc = domain_config["scenarios"][cfg["scenario"]]
    layout = json.load(open(ROOT / domain_config["layouts"][cfg.get("layout") or sc.reference_layouts[0]]))
    setup = json.load(open(ROOT / domain_config["setups"][sc.setup]))
    fixed = {o["id"]: tuple(o["position"]) for o in layout["env_objects"]}
    items = {o["id"]: o for o in setup["env_objects"]}
    step = float(yaml.safe_load(open(ROOT / "mesa_sim" / "mesa_configs.yaml"))["simulation"]["step_size"])
    robot = next(a for a in sc.agents if a.agent_type == "robot")
    pos, per = tuple(robot.start_position), []
    for task in robot.assigned_tasks:
        item = next(c.value for v, c in task.bindings.items() if v.name == "?item")
        shelf, table = fixed[items[item]["initial_container"]], fixed[items[item]["destination"]]
        walk = max(0, math.ceil((math.dist(pos, shelf) - PROXIMITY_THRESHOLD) / step))
        at_shelf = _arrival(pos, shelf, PROXIMITY_THRESHOLD)
        carry = max(0, math.ceil((math.dist(at_shelf, table) - PROXIMITY_THRESHOLD) / step))
        pos = _arrival(at_shelf, table, PROXIMITY_THRESHOLD)
        per.append(walk + carry + STATIONARY_PER_TASK)
    return sum(per), per


def cap(run_file):
    robot_ticks, _ = plain_chain(run_file)
    return robot_ticks + (trajectory.expand(run_file) + 1) + MARGIN


if __name__ == "__main__":
    print(cap(sys.argv[1]))
