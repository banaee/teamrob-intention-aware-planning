#!/usr/bin/env python3
"""
permutation_costs.py — the plain cost of every ordering of a robot's task pool,
and of each task taken alone from its start position (T-B1b).

    PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python \
        analysis/tb1b_two_tables/permutation_costs.py <layout> <scenario> [robot_id]

Why it is committed rather than thrown away: the table for env_layout8 is the
argument that scenario_80 / scenario_81 can distinguish a head chosen greedily
from the head of the cheapest ordering, and T-B3a checks B3.B's chosen head
against it. A table nobody can regenerate leaves the two unarbitrable when they
disagree.

WHAT IT COMPUTES. The robot's own `Projector`, with the Mesa body's constants
(the ones sim_agents.py hands it: 20 cm per tick, arrival radius 30 cm, the
action and task completion latencies), over the robot's assigned_tasks as the
scenario states them. A task's cost is the span of its projected segments. An
ordering is chained: each task is projected from the position the previous one
ended at, by rebuilding the WorldState with the robot moved there (the live
WorldState is never mutated). The greedy ordering is the repeated cheapest
next task, ties broken by item id.

WHAT IT IS NOT. Not B3.B. `Projector.project` is single-task until B3.B is
built (multi-task projection needs the cross-task WorldState continuity of
DESIGN-16 / TODO-07), so the chaining here carries the start position only, not
the world a prior task would leave behind — enough for deliveries, whose only
cross-task coupling is where the robot ends up. It is plain cost: no human, no
belief, no realization, no hold. Nothing reads its output back; it sets
nothing.
"""

import dataclasses
import itertools
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "mesa_sim"))

logging.disable(logging.CRITICAL)   # a model is built here only to read geometry out of it

from mesa_sim.sim_model import SimModel                      # noqa: E402
from mesa_sim.world_state_builder import build_world_state    # noqa: E402
from domains.kitting.registry import domain_config            # noqa: E402
from shared.types import Var                                  # noqa: E402


def costs(layout_name: str, scenario_id: str, robot_id: str = "robot_0"):
    layout = domain_config["layouts"][layout_name]
    model = SimModel(layout["scenarios"][scenario_id], domain_config["register_fn"],
                     env_layout_path=layout["path"])
    robot = model.robots[robot_id]
    world = build_world_state(model)
    belief = robot._make_dummy_belief()
    start = world.agent_positions[robot_id]
    tasks = {t.bindings[Var("?item")].value: t for t in robot.assigned_tasks}

    def one(item, from_pos):
        """(cost in ticks, end position) of `item`'s delivery projected from `from_pos`."""
        w = dataclasses.replace(world, agent_positions={**world.agent_positions, robot_id: from_pos})
        segments = robot.projector.project([tasks[item]], w, robot_id, belief).entries[0].segments
        return segments[-1].end_step, segments[-1].end_pos

    single = {item: one(item, start)[0] for item in tasks}

    orderings = {}
    for ordering in itertools.permutations(sorted(tasks)):
        pos, total, per_task = start, 0.0, []
        for item in ordering:
            cost, pos = one(item, pos)
            total += cost
            per_task.append(cost)
        orderings[ordering] = (total, per_task)

    pos, remaining, greedy = start, set(tasks), []
    while remaining:
        item = min(sorted(remaining), key=lambda i: one(i, pos)[0])
        greedy.append(item)
        pos = one(item, pos)[1]
        remaining.discard(item)

    return single, orderings, tuple(greedy)


def main():
    if not 3 <= len(sys.argv) <= 4:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        raise SystemExit(2)
    layout_name, scenario_id = sys.argv[1], sys.argv[2]
    robot_id = sys.argv[3] if len(sys.argv) == 4 else "robot_0"

    single, orderings, greedy = costs(layout_name, scenario_id, robot_id)
    best_ordering, (best, _) = min(orderings.items(), key=lambda kv: kv[1][0])

    print(f"# {layout_name} / {scenario_id}: {robot_id}'s pool, plain cost in ticks\n")
    print("single task from the start: " + ", ".join(
        f"{i} {c:.2f}" for i, c in sorted(single.items(), key=lambda kv: kv[1])))
    greedy_head, optimal_head = greedy[0], best_ordering[0]
    print(f"greedy head {greedy_head}; head of the cheapest ordering {optimal_head}; "
          f"they {'DIFFER' if greedy_head != optimal_head else 'COINCIDE'}")
    print(f"greedy ordering {' '.join(greedy)} {orderings[tuple(greedy)][0]:.2f}, "
          f"cheapest {' '.join(best_ordering)} {best:.2f}, "
          f"gap {orderings[tuple(greedy)][0] - best:.2f}\n")

    print("| ordering (items) | total | vs best | per task |")
    print("|---|---|---|---|")
    for ordering, (total, per_task) in sorted(orderings.items(), key=lambda kv: kv[1][0]):
        mark = " (greedy)" if list(ordering) == greedy else ""
        items = " ".join(i.split("_")[-1] for i in ordering)
        print(f"| {items}{mark} | {total:.2f} | +{total - best:.2f} | "
              f"{', '.join(f'{c:.1f}' for c in per_task)} |")


if __name__ == "__main__":
    main()
