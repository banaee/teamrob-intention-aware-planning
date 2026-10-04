"""
The trajectory realize() assesses is the trajectory the robot executes from the decision tick onward (the MPB class-2
finding, 30 September 2026; design_decisions.md, "Realization as built", the dated correction; design_records.md, MPB-4, its class-2
record). One test per state in which the body's execution and the projection diverged before the fix, with and without
a hold:

  (a) after a walk's acknowledgement, the next (stationary) action not begun: the fresh decomposition re-contains the
      completed walk as a zero-length move_to; the body continues past it (Executor.continue_plan), so the projection
      is resumed from the action in flight (ExecutorState.action_in_flight, Projector.project resume_from);
  (b) on a pick_up's acknowledgement tick: the body owes the acknowledgement and spends it first
      (ExecutorState.owed_completion_ticks, Projector.project lead_in);
  (c) after a release: the body owes the place's acknowledgement and the task's completion tick (two), or, a tick
      later, the completion tick (one), and spends them before the next task.

Each test runs scenario_s12_01's robot alone (env_layout_14, env_setup_12: item_7 from shelf_5, then item_13), forces a
decision at the state's tick (robot alone: the walk to shelf_5 ends at 24, its acknowledgement 25, the grasp 26, its
acknowledgement 27, the release 60, its acknowledgement 61, the completion tick 62), and compares the winner's realized
plan with the executed robot, TICK FOR TICK: planned position at projection step s equals the executed position at the
end of world tick (decision tick - 1 + s), from the decision to the end of the plan's first walk. (Past a walk's end the
executor's last discrete step and the projection's arrival radius differ by less than a step: the per-walk step
quantisation the record leaves uncompensated, TODO-77; not what these tests assert.) The hold is forced by a synthetic
human projection, a stand on the robot's next walk; the hold's value is realize()'s.
"""
import dataclasses
import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "mesa_sim"))

from domains.kitting.registry import domain_config, register_kitting_domain
from mesa_sim.sim_model import SimModel
import shared.meta_planner as meta_planner_module
from shared.types import (ProjectedPlan, ProjectedPlanEntry, RecognitionChange, Segment, TriggerDecision,
                          task_instance_key)

SCENARIO, LAYOUT = "scenario_s12_01", "env_layout_14"


def robot_alone():
    sc = domain_config["scenarios"][SCENARIO]
    robots = [dataclasses.replace(a, observes=[]) for a in sc.agents if a.agent_type == "robot"]
    return dataclasses.replace(sc, agents=robots)


def stand_at(point, until):
    """A synthetic human projection: a stand at `point` from the observation offset (step 1) to `until`."""
    seg = Segment(start_pos=point, start_step=1.0, end_pos=point, end_step=float(until))
    return ProjectedPlan(task_queue=["synthetic_stand"],
                         entries=[ProjectedPlanEntry(abstract_plan=None, estimated_start_step=1,
                                                     estimated_duration=int(until) - 1, segments=[seg])],
                         total_estimated_cost=int(until) - 1)


def at(segments, s):
    for g in segments:
        if g.start_step - 1e-9 <= s <= g.end_step + 1e-9:
            f = 0.0 if g.end_step == g.start_step else (s - g.start_step) / (g.end_step - g.start_step)
            return (g.start_pos[0] + f * (g.end_pos[0] - g.start_pos[0]),
                    g.start_pos[1] + f * (g.end_pos[1] - g.start_pos[1]))
    return None


def run_forced(tick, human, steps=170):
    """Run the robot alone; at `tick` force a decision against `human` (a ProjectedPlan, or None). Returns the
    ExecutorState the body reported at the decision, the winner's realized plan, the UpdateResult and the robot's
    executed positions per tick."""
    m = SimModel(scenario=robot_alone(), register_fn=register_kitting_domain,
                 task_model_schemas=domain_config["task_model"], layout_path=domain_config["layouts"][LAYOUT],
                 setup_path=domain_config["setups"]["env_setup_12"], assignment_knowledge=True, strategy="single_task",
                 gate_strategy="none", cost_strategy="realized", separation_stop=False, test_level=0.05)
    robot = next(iter(m.robots.values()))
    mp = robot.meta_planner
    seen = {}
    now = lambda: int(m.schedule.steps)
    orig_triggers, orig_projection, orig_update = mp.evaluate_triggers, mp.update_human_projection, mp.update
    orig_realize = meta_planner_module.realize

    def triggers(belief, world, executor_state):
        d = orig_triggers(belief=belief, world=world, executor_state=executor_state)
        if now() == tick:
            seen["state"] = executor_state
            return TriggerDecision(fired=True, reason="recognition_changed", cause=RecognitionChange.ENTERED)
        return d

    def projection(belief, world):
        return human if now() == tick else orig_projection(belief=belief, world=world)

    def update(**kw):
        r = orig_update(**kw)
        if now() == tick:
            seen["result"] = r
        return r

    def realize(plan, human_plan, min_separation, decision_step):
        r = orig_realize(plan, human_plan, min_separation, decision_step)
        if now() == tick:
            seen.setdefault("realized", []).append((plan, r))
        return r

    mp.evaluate_triggers, mp.update_human_projection, mp.update = triggers, projection, update
    meta_planner_module.realize = realize
    try:
        positions = {}
        for _ in range(steps):
            t = now()
            m.step()
            positions[t] = (float(robot.pos[0]), float(robot.pos[1]))
    finally:
        meta_planner_module.realize = orig_realize
    winner = task_instance_key(seen["result"].current_task)
    realized = min((r for p, r in seen["realized"] if p.task_queue[0] == winner), key=lambda r: r.cost)
    return seen["state"], realized, seen["result"], positions


def assert_executed_is_assessed(tick, realized, positions):
    """Planned = executed, tick for tick, from the decision to the end of the plan's first walk."""
    first_walk = next(g for g in realized.segments if g.start_pos != g.end_pos)
    s = 1
    while s < first_walk.end_step - 1e-9:
        planned, executed = at(realized.segments, s), positions[tick - 1 + s]
        assert math.dist(planned, executed) < 1e-6, (
            f"step {s} (tick {tick - 1 + s}): planned {planned}, executed {executed}")
        s += 1
    assert s > first_walk.start_step + 1, "the comparison must reach into the first walk"


# the state's tick, its expected report (owed completion ticks, the action in flight's name), and a point on the
# robot's next walk for the forced hold: at shelf_5, a point both candidates pass (item_7's carry and the walk to
# shelf_11), 52 cm from the robot standing there, so the winner holds whichever it is
CASES = {
    "a_after_walk_ack": (26, 0, "pick_up", (-10.0, -192.0)),
    "b_pick_up_ack": (27, 1, "move_to", (-10.0, -192.0)),
    "c_after_release": (61, 2, None, (-250.0, 30.0)),
    "c_completion_tick": (62, 1, None, (-250.0, 30.0)),
}


@pytest.mark.parametrize("case", sorted(CASES))
@pytest.mark.parametrize("with_hold", [False, True])
def test_executed_is_assessed(case, with_hold):
    tick, owed, in_flight, point = CASES[case]
    human = stand_at(point, 40) if with_hold else None
    state, realized, result, positions = run_forced(tick, human)
    assert state.owed_completion_ticks == owed
    assert (state.action_in_flight.action_name if state.action_in_flight else None) == in_flight
    assert (result.hold > 0) == with_hold
    assert_executed_is_assessed(tick, realized, positions)


def test_the_resumed_projection_drops_the_completed_walk():
    """(a): the continued task's projection starts at the pick_up, not at a zero-length walk and its acknowledgement."""
    state, realized, result, positions = run_forced(26, None)
    assert result.hold == 0
    stationary_before_walk = [g for g in realized.segments[:4] if g.start_pos == g.end_pos]
    assert [round(g.end_step - g.start_step, 9) for g in stationary_before_walk][:2] == [1.0, 1.0]
    assert realized.segments[2].start_pos != realized.segments[2].end_pos   # the grasp, its acknowledgement, the carry
