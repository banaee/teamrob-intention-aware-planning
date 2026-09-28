# tests/test_p_build.py
"""
T-D P, the fallback projection, as ruled with P4 and Q6 (design_decisions.md, "T-D P: the fallback projection"):
where admission refuses and a human is observed, the robot projects what it observed for as long as it observed it —
a straight run of k ticks continued k ticks (ended earlier at the workspace boundary or the first fixed object's
arrival radius, with no stand after it), a stand of k ticks held k ticks, nothing without a previous observation —
realize() prices it as any projection, and projection_expired re-decides when the fallback a decision rested on
reaches its end. Every expected value is derived from the entry and from realize() on synthetic plans (v = 20 cm/tick,
min_separation = 50 cm, the observation offset 1 tick), none from a run.
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
from shared.projection import Projector
from shared.realization import realize
from shared.trajectory_algorithms import stationary_segment
from shared.types import (
    AdequacyFinding, BeliefState, Const, ExecutorState, HypothesisAdequacy, ProjectedPlan, ProjectedPlanEntry,
    RecognitionChange, RecognizerLifecycle, Segment, TaskInstance, Var, Workspace, task_instance_key,
)
from domains.kitting.tasks import deliver_item
from mesa_sim.sim_agents import DIRECTION_RESOLUTION
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


def stand(position, end):
    """A hand-built stand over [OFFSET, end]: realize()'s input for the table."""
    return ProjectedPlan([], [ProjectedPlanEntry(None, 1, int(end - OFFSET),
                                                 [stationary_segment(position, OFFSET, end - OFFSET)])], 0)


def end_of(plan):
    return [s for e in plan.entries for s in e.segments][-1].end_step


@pytest.fixture(scope="module")
def model():
    return model_for("env_layout_01", registered("env_layout_01", "scenario_s01_01"))


@pytest.fixture(scope="module")
def projector(model):
    base = next(iter(model.robots.values())).meta_planner
    return Projector(task_model=base._task_model, assumed_speed=V, arrival_radius=RADIUS, observation_offset=OFFSET)


def perceived(model, position, displacement, run=0, standing=0, objects=None, timestamp=0.0):
    """The robot's world model with the observed human at `position` and its perception facts."""
    w = build_world_state(model)
    return replace(w, timestamp=timestamp, agent_positions={**w.agent_positions, H: position},
                   agent_displacements={H: displacement}, agent_run_lengths={H: run},
                   agent_standing_counts={H: standing}, workspace=ROOM,
                   fixed_object_positions=objects if objects is not None else {})


# ---------------------------------------------------------------------------
# The table (P1's measurement, kept as a test of realize() against a stand)
# ---------------------------------------------------------------------------

HUMAN = (400.0, 0.0)
TARGET_AT_HUMAN = robot([(0, 0), (370, 0)], [3])          # the walk ends 30 cm short of the human
CROSS_EARLY = robot([(0, 0), (1000, 0)], [3])
CROSS_JUST_PAST = robot([(0, 0), (500, 0)], [3])
AWAY = robot([(0, 0), (-400, 0)], [3])


@pytest.mark.parametrize("candidate,t_r,delta", [
    (TARGET_AT_HUMAN, 21.5, 4), (CROSS_EARLY, 53.0, 36), (CROSS_JUST_PAST, 28.0, 11), (AWAY, 23.0, 0),
])
def test_the_table_realize_against_a_stand_over_the_candidate(candidate, t_r, delta):
    r = realize(candidate, stand(HUMAN, end_of(candidate)), S, 0.0)
    assert r.projected_duration == pytest.approx(t_r) and r.delta == delta


def test_a_far_target_at_the_human_pays_T_h_minus_the_onset():
    # the robot enters min_separation of the human at x = 350 (t = 17.5): delta = ceil(T_h - 17.5)
    r = realize(TARGET_AT_HUMAN, stand(HUMAN, 21.5), S, 0.0)
    assert r.delta == math.ceil(21.5 - 350.0 / V)


def test_a_violation_from_the_decision_step_pays_the_stands_length():
    # the robot 30 cm from the standing human, walking through it: it violates from u = 0, so delta = ceil(T_h)
    candidate = robot([(0, 0), (300, 0)], [3])
    r = realize(candidate, stand((30.0, 0.0), end_of(candidate)), S, 0.0)
    assert r.delta == math.ceil(end_of(candidate))


# ---------------------------------------------------------------------------
# P4: the fallback from the evidence
# ---------------------------------------------------------------------------

def test_a_run_of_k_ticks_projects_k_ticks(model, projector):
    fb = projector.project_fallback(perceived(model, (0.0, 300.0), (0.0, -V), run=5), H)
    [walk] = fb.entries[0].segments
    assert walk.start_step == OFFSET and walk.end_step == pytest.approx(OFFSET + 5)
    assert walk.end_pos == pytest.approx((0.0, 200.0))


def test_a_run_stops_at_the_first_object_with_no_stand(model, projector):
    # the shelf at (0, 150): its arrival radius is entered 120 cm on, 6 ticks, before the run's 10
    fb = projector.project_fallback(perceived(model, (0.0, 300.0), (0.0, -V), run=10, objects={"s": (0.0, 150.0)}), H)
    [walk] = fb.entries[0].segments
    assert walk.end_pos == pytest.approx((0.0, 180.0)) and walk.end_step == pytest.approx(OFFSET + 6)


def test_an_object_containing_the_start_is_skipped_and_the_boundary_stops_the_walk(model, projector):
    w = replace(perceived(model, (0.0, 390.0), (0.0, V), run=10, objects={"t": (0.0, 380.0)}),
                workspace=Workspace(-500.0, 500.0, -400.0, 400.0))
    [walk] = projector.project_fallback(w, H).entries[0].segments
    assert walk.end_pos == pytest.approx((0.0, 400.0)) and walk.end_step == pytest.approx(OFFSET + 0.5)


def test_a_stand_of_k_ticks_projects_k_ticks(model, projector):
    [seg] = projector.project_fallback(perceived(model, HUMAN, (0.0, 0.0), standing=7), H).entries[0].segments
    assert seg.start_pos == seg.end_pos == HUMAN
    assert seg.start_step == OFFSET and seg.end_step == pytest.approx(OFFSET + 7)


def test_no_previous_observation_gives_no_projection(model, projector):
    w = build_world_state(model)          # the builder writes no perception facts
    assert not w.agent_displacements and projector.project_fallback(w, H) is None


def test_a_crossing_candidate_pays_a_finite_hold(model, projector):
    # the human at (200, 150) has walked down at V for 20 ticks: projected 20 ticks on, across the robot's path
    fb = projector.project_fallback(perceived(model, (200.0, 150.0), (0.0, -V), run=20), H)
    candidate = robot([(0, 0), (400, 0)], [3])
    r = realize(candidate, fb, S, 0.0)
    assert 0 < r.delta < math.inf and r.horizon == pytest.approx(OFFSET + 20)


def test_little_evidence_protects_little(model, projector):
    # a known error, recorded: one step into the same walk projects 20 cm, and the crossing is not seen
    fb = projector.project_fallback(perceived(model, (200.0, 150.0), (0.0, -V), run=1), H)
    r = realize(robot([(0, 0), (400, 0)], [3]), fb, S, 0.0)
    assert r.delta == 0


# ---------------------------------------------------------------------------
# The perception facts on RobotAgent
# ---------------------------------------------------------------------------

def test_the_run_and_the_standing_count(model):
    robot_agent = next(iter(model.robots.values()))
    human = model.humans[H]
    w = build_world_state(model)
    robot_agent._previous_human_position = None
    robot_agent._previous_human_direction = None
    robot_agent._human_run_length = robot_agent._human_standing_count = 0

    def at(p):
        return robot_agent._perceive(replace(w, agent_positions={**w.agent_positions, H: p}), human)

    assert not at((0.0, 0.0)).agent_displacements                        # no previous observation: absent
    assert at((20.0, 0.0)).agent_run_lengths[H] == 1
    assert at((40.0, 0.0)).agent_run_lengths[H] == 2
    # a direction change within the body's resolution continues the run
    step = (20.0, 20.0 * DIRECTION_RESOLUTION / 10)
    assert at((60.0 + step[0] - 20.0, step[1])).agent_run_lengths[H] == 3
    turned = at((60.0, 20.0))                                            # a turn: a run of 1
    assert turned.agent_run_lengths[H] == 1 and turned.agent_standing_counts[H] == 0
    stopped = at((60.0, 20.0))                                           # a stop: run 0, standing 1
    assert stopped.agent_run_lengths[H] == 0 and stopped.agent_standing_counts[H] == 1
    assert stopped.agent_displacements[H] == (0.0, 0.0)
    assert at((60.0, 20.0)).agent_standing_counts[H] == 2
    moved = at((60.0, 40.0))                                             # a step ends the stand
    assert moved.agent_run_lengths[H] == 1 and moved.agent_standing_counts[H] == 0


# ---------------------------------------------------------------------------
# The meta-planner: admission, the record, projection_expired, B2
# ---------------------------------------------------------------------------

def task(i):
    return TaskInstance(schema=deliver_item, bindings={Var("?item"): Const(i)})


def belief(confidence, adequacy=HypothesisAdequacy.ADEQUATE):
    key = task_instance_key(task("item_3"))
    return BeliefState(timestamp=0.0, agent_id=H, distribution={key: confidence}, most_likely=key,
                       confidence=confidence, finding=AdequacyFinding.ADEQUATE, lifecycle=RecognizerLifecycle.LIVE,
                       tails={}, hypothesis_adequacy={key: adequacy}, episode_boundary=False)


class Stub:
    """A projector standing in for the Projector: one fixed plan per task; the fallback from a real Projector."""
    def __init__(self, plans, projector):
        self.plans, self.projector = plans, projector

    def project(self, ordering, world, agent_id, belief, start_step=0.0):
        return self.plans[task_instance_key(ordering[0])]

    def project_human(self, **kwargs):
        return None

    def project_fallback(self, world, human_agent_id):
        return self.projector.project_fallback(world, human_agent_id)


def planner(model, projector, plans=None, gate_strategy="none"):
    base = next(iter(model.robots.values())).meta_planner
    return MetaPlanner(task_model=base._task_model, projector=Stub(plans or {}, projector),
                       recognizer=base._recognizer, min_separation=S, human_agent_id=H, gate_strategy=gate_strategy)


EXECUTING = ExecutorState(agent_id="robot_0", current_task=task("item_4"), holding=None)


def test_a_refused_admission_with_evidence_yields_the_fallback(model, projector, caplog):
    mp = planner(model, projector)
    with caplog.at_level(logging.INFO):
        fb = mp.update_human_projection(belief(0.5), perceived(model, HUMAN, (0.0, 0.0), standing=3))
    assert fb is not None and fb.entries[0].abstract_plan is None
    assert "projection=fallback refused=none(below_theta)" in caplog.text


def test_no_human_observed_or_no_previous_observation_yields_none(model, projector, caplog):
    mp = planner(model, projector)
    w = build_world_state(model)
    with caplog.at_level(logging.INFO):
        assert mp.update_human_projection(belief(0.5), w) is None
    assert "projection=none(below_theta)" in caplog.text
    assert mp._fallback_expiry is None
    gone = replace(perceived(model, HUMAN, (0.0, 0.0), standing=3),
                   agent_positions={a: p for a, p in w.agent_positions.items() if a != H})
    assert mp.update_human_projection(belief(0.5), gone) is None


def test_the_record_stays_empty_under_a_fallback_and_the_next_admission_fires_entered(model, projector):
    mp = planner(model, projector)
    assert mp.update_human_projection(belief(0.5), perceived(model, HUMAN, (0.0, 0.0), standing=3)) is not None
    assert mp._projected_hypothesis is None
    admitted = belief(0.9)
    assert admitted.confidence >= DEFAULT_THETA
    d = mp.evaluate_triggers(admitted, perceived(model, HUMAN, (0.0, 0.0), standing=4, timestamp=1.0), EXECUTING)
    assert d.fired and d.cause is RecognitionChange.ENTERED


def test_projection_expired_fires_at_the_fallbacks_end(model, projector):
    # a stand of 4 ticks observed at tick 10: the fallback spans [1, 5] on the decision's clock, so it expires at 15
    mp = planner(model, projector)
    mp.update_human_projection(belief(0.5), perceived(model, HUMAN, (0.0, 0.0), standing=4, timestamp=10.0))
    assert mp._fallback_expiry == pytest.approx(15.0)
    assert not mp.evaluate_triggers(belief(0.5), perceived(model, HUMAN, (0.0, 0.0), standing=8, timestamp=14.0),
                                    EXECUTING).fired
    d = mp.evaluate_triggers(belief(0.5), perceived(model, HUMAN, (0.0, 0.0), standing=9, timestamp=15.0), EXECUTING)
    assert d.fired and d.reason == "projection_expired" and d.cause is None


def test_projection_expired_reads_the_truncation_not_the_evidence_horizon(model, projector):
    # a run of 10 ticks cut by a shelf 2 ticks on: the fallback ends at 1 + 2, so the decision at 10 expires at 13
    mp = planner(model, projector)
    w = perceived(model, (0.0, 300.0), (0.0, -V), run=10, objects={"s": (0.0, 230.0)}, timestamp=10.0)
    mp.update_human_projection(belief(0.5), w)
    assert mp._fallback_expiry == pytest.approx(13.0)


def test_an_admission_clears_the_expiry(model, projector):
    mp = planner(model, projector)
    mp.update_human_projection(belief(0.5), perceived(model, HUMAN, (0.0, 0.0), standing=4))
    assert mp._fallback_expiry is not None
    mp.update_human_projection(belief(0.5), build_world_state(model))       # no previous observation: no fallback
    assert mp._fallback_expiry is None


def test_b2_reads_the_fallback_as_any_projection(model, projector):
    a = task("item_4")
    w = perceived(model, (200.0, 150.0), (0.0, -V), run=20)
    crossing = robot([(0, 0), (400, 0)], [3])
    mp = planner(model, projector, {task_instance_key(a): crossing}, gate_strategy="b2a")
    result = mp.update(belief(0.5), w, EXECUTING, mp.update_human_projection(belief(0.5), w))
    r = realize(crossing, projector.project_fallback(w, H), S, 0.0)
    assert result.current_task is EXECUTING.current_task and result.hold == r.delta > 0
    assert result.horizon == pytest.approx(OFFSET + 20)
