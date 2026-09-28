# tests/test_p_build.py
"""
T-D P, the fallback projection (design_decisions.md, "T-D P: the fallback projection"): P1 the fallback over the
candidate's own span and its refusal rule (a violation cleared only by the projection's end is refused; one cleared by
the projected motion within the horizon keeps its hold), P2 the shape (the last one-tick displacement: standing, or a
straight continuation to the workspace boundary or the first fixed object's arrival radius), the wait. Every expected
value is derived from the entry and from realize() on synthetic plans (v = 20 cm/tick, min_separation = 50 cm, the
observation offset 1 tick), none from a run.
Run from the repo root:  PYTHONHASHSEED=0 python -m pytest tests/test_p_build.py
"""

import logging
import math
from dataclasses import replace

import pytest

# first: puts the repo root and mesa_sim/ on the path, as the other test modules do
from tests.test_td1_adequacy import H
from tests.test_th1_tree import model_for, registered
from shared.meta_planner import DEFAULT_THETA, MetaPlanner
from shared.projection import AdmittedProjection, FallbackProjection
from shared.realization import realize
from shared.trajectory_algorithms import stationary_segment
from shared.types import (
    AdequacyFinding, BeliefState, Const, ExecutorState, HypothesisAdequacy, ProjectedPlan, ProjectedPlanEntry,
    RecognitionChange, RecognizerLifecycle, Segment, TaskInstance, Var, Workspace, task_instance_key,
)
from domains.kitting.tasks import deliver_item
from mesa_sim.world_state_builder import build_world_state

V, S, OFFSET, RADIUS = 20.0, 50.0, 1.0, 30.0
ROOM = Workspace(x_min=-1000.0, x_max=1000.0, y_min=-1000.0, y_max=1000.0)


def robot(waypoints, stops):
    """A robot candidate: straight walks at V between the waypoints, each followed by `stops[k]` stationary ticks
    (the Projector's priced standing), one entry, from step 0."""
    segs, t = [], 0.0
    for (a, b), k in zip(zip(waypoints, waypoints[1:]), stops):
        segs.append(Segment(a, t, b, t + math.dist(a, b) / V))
        t += math.dist(a, b) / V
        if k:
            segs.append(stationary_segment(b, t, k))
            t += k
    return ProjectedPlan([], [ProjectedPlanEntry(None, 0, int(t), segs)], int(t))


def fallback(position, displacement=None, objects=()):
    return FallbackProjection(position=position, displacement=displacement, start_step=OFFSET, workspace=ROOM,
                              fixed_objects=tuple(objects), arrival_radius=RADIUS)


def end_of(plan):
    return [s for e in plan.entries for s in e.segments][-1].end_step


def realized_against(candidate, fb):
    r = realize(candidate, fb.for_candidate(candidate), S, 0.0)
    return r, fb.realizable(candidate, r, S)


# ---------------------------------------------------------------------------
# P1: the table (the reason for rule 5), realize() against a stand
# ---------------------------------------------------------------------------

HUMAN = (400.0, 0.0)
TARGET_AT_HUMAN = robot([(0, 0), (370, 0)], [3])          # the walk ends 30 cm short of the human
CROSS_EARLY = robot([(0, 0), (1000, 0)], [3])
CROSS_JUST_PAST = robot([(0, 0), (500, 0)], [3])
AWAY = robot([(0, 0), (-400, 0)], [3])


@pytest.mark.parametrize("candidate,t_r,delta", [
    (TARGET_AT_HUMAN, 21.5, 4), (CROSS_EARLY, 53.0, 36), (CROSS_JUST_PAST, 28.0, 11), (AWAY, 23.0, 0),
])
def test_the_table_realize_against_a_stand(candidate, t_r, delta):
    r = realize(candidate, fallback(HUMAN).for_candidate(candidate), S, 0.0)
    assert r.projected_duration == pytest.approx(t_r) and r.delta == delta and r.horizon == pytest.approx(t_r)


def test_a_far_target_at_the_human_pays_T_h_minus_the_onset():
    # the robot enters min_separation of the human at x = 350 (t = 17.5): delta = ceil(T_h - 17.5) = ceil(21.5 - 17.5)
    r = realize(TARGET_AT_HUMAN, fallback(HUMAN).for_candidate(TARGET_AT_HUMAN), S, 0.0)
    assert r.delta == math.ceil(21.5 - 350.0 / V)


def test_a_violation_from_the_decision_step_pays_the_candidates_own_length():
    # the robot 30 cm from the standing human, walking through it: it violates from u = 0, so delta = ceil(T_r)
    candidate = robot([(0, 0), (300, 0)], [3])
    r = realize(candidate, fallback((30.0, 0.0)).for_candidate(candidate), S, 0.0)
    assert r.delta == math.ceil(end_of(candidate))


# ---------------------------------------------------------------------------
# P1: the fallback over the candidate's span; the refusal under a stand
# ---------------------------------------------------------------------------

def test_the_fallback_spans_the_candidate_at_the_observed_position():
    stand = fallback(HUMAN).for_candidate(TARGET_AT_HUMAN)
    [entry] = stand.entries
    [seg] = entry.segments
    assert entry.abstract_plan is None
    assert seg.start_pos == seg.end_pos == HUMAN
    assert seg.start_step == OFFSET and seg.end_step == pytest.approx(end_of(TARGET_AT_HUMAN))


def test_the_fallbacks_span_is_the_orderings_under_full_reorder():
    # an ordering is one chained candidate: the stand ends where its last entry ends
    first = robot([(0, 0), (-400, 0)], [3]).entries[0]
    second_segs = [Segment(s.start_pos, s.start_step + 23.0, s.end_pos, s.end_step + 23.0)
                   for s in robot([(-400, 0), (-400, 400)], [3]).entries[0].segments]
    ordering = ProjectedPlan([], [first, ProjectedPlanEntry(None, 23, 23, second_segs)], 46)
    [seg] = fallback(HUMAN).for_candidate(ordering).entries[0].segments
    assert seg.end_step == pytest.approx(46.0)


@pytest.mark.parametrize("candidate,eligible", [
    (TARGET_AT_HUMAN, False), (CROSS_EARLY, False), (CROSS_JUST_PAST, False), (AWAY, True),
])
def test_under_a_stand_a_hold_is_refused_and_no_hold_is_eligible(candidate, eligible):
    r, ok = realized_against(candidate, fallback(HUMAN))
    assert ok is eligible and (r.delta == 0) is eligible


def test_an_absent_displacement_reads_as_standing():
    assert fallback(HUMAN, None).for_candidate(CROSS_EARLY) == fallback(HUMAN, (0.0, 0.0)).for_candidate(CROSS_EARLY)
    [seg] = fallback(HUMAN, None).for_candidate(CROSS_EARLY).entries[0].segments
    assert seg.start_pos == seg.end_pos == HUMAN


def test_an_admitted_projection_refuses_nothing():
    plan = fallback(HUMAN).for_candidate(TARGET_AT_HUMAN)
    admitted = AdmittedProjection(plan=plan)
    r = realize(TARGET_AT_HUMAN, admitted.for_candidate(TARGET_AT_HUMAN), S, 0.0)
    assert r.delta == 4 and admitted.realizable(TARGET_AT_HUMAN, r, S)


# ---------------------------------------------------------------------------
# P2: the moving cases
# ---------------------------------------------------------------------------

def test_a_human_walking_across_the_path_pays_a_hold():
    # the human at (200, 150) walking down at V crosses y = 0 at t = 8.5, the robot passes x = 200 at t = 10;
    # the human walks on (to the room's wall, past the horizon): the hold is cleared by its motion
    candidate = robot([(0, 0), (400, 0)], [3])
    r, ok = realized_against(candidate, fallback((200.0, 150.0), (0.0, -V)))
    assert r.delta > 0 and ok


def test_a_human_walking_to_the_candidates_target_is_refused():
    # the table at (400, 0): the human walks down to its arrival radius, (400, 30), at t = 1 + 270 / V = 14.5, and
    # stands there; the robot arrives at (370, 0) within min_separation of it: cleared only by the stand's end
    fb = fallback((400.0, 300.0), (0.0, -V), objects=[(400.0, 0.0)])
    segs = fb.for_candidate(TARGET_AT_HUMAN).entries[0].segments
    assert segs[0].end_pos == pytest.approx((400.0, 30.0)) and segs[0].end_step == pytest.approx(14.5)
    assert segs[1].start_pos == segs[1].end_pos
    r, ok = realized_against(TARGET_AT_HUMAN, fb)
    assert r.delta > 0 and not ok


def test_a_human_walking_away_frees_the_candidate():
    # the same target, the human leaving it (its start inside the table's radius: the table is skipped)
    fb = fallback((400.0, 0.0), (0.0, V), objects=[(400.0, 0.0)])
    r, ok = realized_against(TARGET_AT_HUMAN, fb)
    assert r.delta == 0 and ok
    _, ok_standing = realized_against(TARGET_AT_HUMAN, fallback((400.0, 0.0)))
    assert not ok_standing


def test_the_horizon_cut_is_refused():
    # the human at (400, 100) walking down at 4 cm/tick, towards the robot's arrival point, still walking at the
    # candidate's end (no object, the wall far): the hold clears the violation only because the walk is cut at T_r
    fb = fallback((400.0, 100.0), (0.0, -4.0))
    [walk] = fb.for_candidate(TARGET_AT_HUMAN).entries[0].segments
    assert walk.end_step == pytest.approx(end_of(TARGET_AT_HUMAN)) and walk.start_pos != walk.end_pos
    r, ok = realized_against(TARGET_AT_HUMAN, fb)
    assert r.delta > 0 and not ok


def test_a_passed_object_stops_the_tail():
    # a known error, recorded: the human walking down past a shelf at (0, 100) is projected to stop at its radius
    fb = fallback((0.0, 300.0), (0.0, -V), objects=[(0.0, 100.0)])
    walk, stand = fb.for_candidate(CROSS_EARLY).entries[0].segments
    assert walk.end_pos == pytest.approx((0.0, 130.0)) and walk.end_step == pytest.approx(OFFSET + 170.0 / V)
    assert stand.start_pos == stand.end_pos == pytest.approx((0.0, 130.0))
    assert stand.end_step == pytest.approx(end_of(CROSS_EARLY))


def test_the_boundary_stops_the_tail():
    fb = FallbackProjection(position=(0.0, 300.0), displacement=(0.0, V), start_step=OFFSET,
                            workspace=Workspace(-500.0, 500.0, -400.0, 400.0), fixed_objects=(), arrival_radius=RADIUS)
    walk, stand = fb.for_candidate(CROSS_EARLY).entries[0].segments
    assert walk.end_pos == pytest.approx((0.0, 400.0)) and walk.end_step == pytest.approx(OFFSET + 100.0 / V)


# ---------------------------------------------------------------------------
# The meta-planner: admission, the refusal in B3, the wait, the record, B2
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def model():
    return model_for("env_layout_01", registered("env_layout_01", "scenario_s01_01"))


def task(i):
    return TaskInstance(schema=deliver_item, bindings={Var("?item"): Const(i)})


class Stub:
    """A projector standing in for the Projector: one fixed plan per task, the fallback it was given."""
    def __init__(self, plans, fb):
        self.plans, self.fb = plans, fb

    def project(self, ordering, world, agent_id, belief, start_step=0.0):
        return self.plans[task_instance_key(ordering[0])]

    def project_human(self, **kwargs):
        return None

    def project_fallback(self, world, human_agent_id):
        return self.fb


def belief(confidence, adequacy=HypothesisAdequacy.ADEQUATE):
    key = task_instance_key(task("item_3"))
    return BeliefState(timestamp=0.0, agent_id=H, distribution={key: confidence}, most_likely=key,
                       confidence=confidence, finding=AdequacyFinding.ADEQUATE, lifecycle=RecognizerLifecycle.LIVE,
                       tails={}, hypothesis_adequacy={key: adequacy}, episode_boundary=False)


def planner(model, plans, fb=None, gate_strategy="none"):
    base = next(iter(model.robots.values())).meta_planner
    return MetaPlanner(task_model=base._task_model, projector=Stub(plans, fb if fb else fallback(HUMAN)),
                       recognizer=base._recognizer, min_separation=S, human_agent_id=H, gate_strategy=gate_strategy)


def test_a_refused_admission_with_a_human_observed_yields_the_fallback(model, caplog):
    mp = planner(model, {})
    with caplog.at_level(logging.INFO):
        fb = mp.update_human_projection(belief(0.5), build_world_state(model))
    assert isinstance(fb, FallbackProjection)
    assert "projection=fallback refused=none(below_theta)" in caplog.text


def test_no_human_observed_yields_none(model):
    base = next(iter(model.robots.values())).meta_planner
    w = build_world_state(model)
    w = replace(w, agent_positions={a: p for a, p in w.agent_positions.items() if a != H})
    mp = MetaPlanner(task_model=base._task_model, projector=base._projector, recognizer=base._recognizer,
                     min_separation=S, human_agent_id=H)
    assert mp.update_human_projection(belief(0.5), w) is None


def test_under_the_fallback_a_refused_candidate_loses_to_an_eligible_one(model):
    a, b = task("item_4"), task("item_6")
    mp = planner(model, {task_instance_key(a): TARGET_AT_HUMAN, task_instance_key(b): AWAY})
    mp.seed_tasks([a, b])
    w = build_world_state(model)
    fb = mp.update_human_projection(belief(0.5), w)
    result = mp.update(belief(0.5), w, ExecutorState(agent_id="robot_0", current_task=None, holding=None), fb)
    # TARGET_AT_HUMAN is cheaper on plain cost (21.5 < 23.0) but needs a hold under the stand: refused
    assert result.current_task is b and result.hold == 0 and result.horizon == pytest.approx(23.0)


def test_with_every_candidate_refused_the_robot_waits_and_the_next_tick_re_asks(model):
    a = task("item_4")
    mp = planner(model, {task_instance_key(a): TARGET_AT_HUMAN})
    mp.seed_tasks([a])
    w = build_world_state(model)
    idle = ExecutorState(agent_id="robot_0", current_task=None, holding=None)
    fb = mp.update_human_projection(belief(0.5), w)
    result = mp.update(belief(0.5), w, idle, fb)
    assert result.current_task is None and result.queue == [a] and result.hold == 0 and result.horizon is None
    trigger = mp.evaluate_triggers(belief(0.5), w, idle)
    assert trigger.fired and trigger.reason == "no_current_task"


def test_the_record_stays_empty_under_a_fallback_and_the_next_admission_fires_entered(model):
    a = task("item_4")
    mp = planner(model, {task_instance_key(a): AWAY})
    w = build_world_state(model)
    executing = ExecutorState(agent_id="robot_0", current_task=a, holding=None)
    assert isinstance(mp.update_human_projection(belief(0.5), w), FallbackProjection)
    assert mp._projected_hypothesis is None
    admitted = belief(0.9)
    assert admitted.confidence >= DEFAULT_THETA
    d = mp.evaluate_triggers(admitted, w, executing)
    assert d.fired and d.cause is RecognitionChange.ENTERED


def test_b2_reads_the_fallback_as_any_projection(model):
    a = task("item_4")
    w = build_world_state(model)
    executing = ExecutorState(agent_id="robot_0", current_task=a, holding=None)
    # eligible, no hold: B2 continues with hold 0 and the candidate's own horizon
    mp = planner(model, {task_instance_key(a): AWAY}, gate_strategy="b2a")
    result = mp.update(belief(0.5), w, executing, mp.update_human_projection(belief(0.5), w))
    assert result.current_task is a and result.hold == 0 and result.horizon == pytest.approx(23.0)
    # a crossing cleared by the human's motion: B2 continues with the hold, as under an admitted projection
    crossing = robot([(0, 0), (400, 0)], [3])
    mp = planner(model, {task_instance_key(a): crossing}, fallback((200.0, 150.0), (0.0, -V)), gate_strategy="b2a")
    result = mp.update(belief(0.5), w, executing, mp.update_human_projection(belief(0.5), w))
    r = realize(crossing, fallback((200.0, 150.0), (0.0, -V)).for_candidate(crossing), S, 0.0)
    assert result.current_task is a and result.hold == r.delta > 0
    # refused: B2 escalates, and B3 with the current task alone waits
    mp = planner(model, {task_instance_key(a): TARGET_AT_HUMAN}, gate_strategy="b2a")
    result = mp.update(belief(0.5), w, executing, mp.update_human_projection(belief(0.5), w))
    assert result.current_task is None and result.queue == [a]


# ---------------------------------------------------------------------------
# The robot's perception: WorldState.agent_displacements
# ---------------------------------------------------------------------------

def test_the_displacement_is_absent_before_a_second_observation_then_the_observed_step(model):
    robot_agent = next(iter(model.robots.values()))
    human = model.humans[H]
    w = build_world_state(model)
    robot_agent._previous_human_position = None
    assert H not in robot_agent._perceive(w, human).agent_displacements
    x, y = w.agent_positions[H]
    moved = replace(w, agent_positions={**w.agent_positions, H: (x + 20.0, y - 5.0)})
    assert robot_agent._perceive(moved, human).agent_displacements[H] == pytest.approx((20.0, -5.0))
    assert not w.agent_displacements   # the builder writes none: the field is the robot's perception
