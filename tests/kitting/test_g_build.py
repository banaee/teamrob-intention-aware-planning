"""
G-build (design_decisions.md, "T-D G: admission", AD1 to AD4): observation warrant, the recognizer's third output,
and the gate's warrant condition. Every expectation is derived from the entry, none from a run.

Observation warrant, per live hypothesis (AD1): OBSERVATION when its current derived phase was entered by the
completion of its previous expected action in this episode (the completion E8 reads), for any phase; or, for a phase
with a movement target whose position is resolved, when the path-cost gain toward it since the phase origin is
positive, C(o, g) - C(p, g) > 0. It resets with the origins, at a boundary and at a phase change. The gate (AD1, AD4):
theta, then the leader's hypothesis adequacy, then warrant (commitment: the leader is one of the observed human's
assigned tasks, by same_task; or observation); an unwarranted leader is refused as none(leader_unwarranted). Loss of
warrant fires nothing (AD3).
"""
import dataclasses
import logging
import math

import pytest

# first: puts the repo root and mesa_sim/ on the path, as the other test modules do
from tests.kitting.test_td1_adequacy import H, SPEED, TABLE, item, obs, pred, recognizer, world_with
from tests.kitting.test_td15_build import ARRIVAL, GRASP, coffee_key, delivery, start_of
from tests.kitting.test_th1_tree import model_for, registered
from domains.kitting.registry import domain_config
from domains.kitting.tasks import deliver_item
from shared.meta_planner import DEFAULT_THETA, GateOutcome, MetaPlanner
from shared.types import (
    AdequacyFinding, BeliefState, Const, ExecutorState, HypothesisAdequacy, ObservationWarrant, RecognizerLifecycle,
    TaskInstance, Var,
)
from mesa_sim.world_state_builder import build_world_state

NONE, OBS = ObservationWarrant.NONE, ObservationWarrant.OBSERVATION


@pytest.fixture(scope="module")
def model():
    return model_for("env_layout_01", registered("env_layout_01", "scenario_s01_01"))


@pytest.fixture(scope="module")
def model5():
    return model_for("env_layout_05", registered("env_layout_05", "scenario_s04_01"))


def walk(rec, points, w, t0=0):
    """One update per point, the same world; the beliefs."""
    return [rec.update(obs(t0 + t, p), w) for t, p in enumerate(points)]


# ---------------------------------------------------------------------------
# The warrant output per phase kind
# ---------------------------------------------------------------------------

def test_a_walk_toward_the_target_is_warranted_after_one_step(model):
    # a move_to entered at the first observation (no completion): nothing walked at t0 (gain 0), one step
    # straight toward item_3 gains 20 cm
    start = start_of(model)
    rec = recognizer(model, [item("item_3")])
    k = repr(item("item_3"))
    b0, b1 = walk(rec, [start, (start[0], start[1] - SPEED)], build_world_state(model))
    assert rec._expected[k].action_name == "move_to"
    assert b0.observation_warrant == {k: NONE}
    assert b1.observation_warrant == {k: OBS}


def test_a_walk_away_or_across_is_not_warranted(model):
    # one step straight away (gain -20 cm), and one step perpendicular to the bearing (the target farther:
    # C(p, g) > C(o, g)): no gain, no warrant. The walk away stays adequate (S = 0.74 at 20 cm), not warranted.
    start = start_of(model)
    k = repr(item("item_3"))
    for p in [(start[0], start[1] + SPEED), (start[0] + SPEED, start[1])]:
        rec = recognizer(model, [item("item_3")])
        b = walk(rec, [start, p], build_world_state(model))[-1]
        assert b.hypothesis_adequacy[k] is HypothesisAdequacy.ADEQUATE
        assert b.observation_warrant == {k: NONE}


def test_a_warranted_walk_loses_its_warrant_when_the_gain_is_undone(model):
    # the gain is read from the origin, not tick to tick: two steps toward, three back past the origin
    start = start_of(model)
    rec = recognizer(model, [item("item_3")])
    k = repr(item("item_3"))
    ys = [0, -1, -2, -1, 0, 1]
    bs = walk(rec, [(start[0], start[1] + SPEED * y) for y in ys], build_world_state(model))
    assert [b.observation_warrant[k] for b in bs] == [NONE, OBS, OBS, OBS, NONE, NONE]


def test_a_stationary_phase_entered_by_a_completion_is_warranted(model):
    # the walk's at() completion opens pick_up (no movement target): warranted through its entry, on the entry
    # tick and while the human stands in it (the walk's latency tick)
    rec = recognizer(model, [item("item_3")])
    k = repr(item("item_3"))
    steps = delivery(model)
    for t, (p, w) in enumerate(steps[:ARRIVAL + 2]):
        b = rec.update(obs(t, p), w)
        if t >= ARRIVAL:
            assert rec._expected[k].action_name == "pick_up"
            assert b.observation_warrant == {k: OBS}, t


def test_a_move_to_entered_by_a_completion_is_warranted_whatever_the_walk(model):
    # the carry after the grasp: entered by pick_up's completion (the entry source, any phase), warranted on its
    # latency tick and on steps away from the table alike
    rec = recognizer(model, [item("item_3")])
    k = repr(item("item_3"))
    steps = delivery(model)
    for t, (p, w) in enumerate(steps[:GRASP + 2]):
        b = rec.update(obs(t, p), w)
    assert rec._expected[k].action_name == "move_to" and b.observation_warrant == {k: OBS}
    p, w = steps[GRASP + 1]
    tx, ty = w.object_positions[TABLE]
    d = math.hypot(tx - p[0], ty - p[1])
    away = (p[0] - SPEED * (tx - p[0]) / d, p[1] - SPEED * (ty - p[1]) / d)
    carrying = world_with(w, remove=[pred("at", H, "item_3")])
    b = rec.update(obs(GRASP + 2, away), carrying)
    assert rec._expected[k].action_name == "move_to"
    assert b.observation_warrant == {k: OBS}


def test_a_stationary_phase_not_entered_by_a_completion_is_not_warranted(model5):
    # coffee_break first observed at the machine, in its wait_at phase (AD1's set-aside case): no movement target,
    # no entry by a completion: adequate (S = 1 within its priced standing) and unwarranted on every tick
    coffee = coffee_key(model5)
    machine = coffee.bindings["?coffee_machine"]
    w = world_with(build_world_state(model5), add=[pred("at", H, machine)])
    rec = recognizer(model5, [coffee])
    for b in walk(rec, [w.object_positions[machine]] * 5, w):
        assert rec._expected[repr(coffee)].action_name == "wait_at"
        assert b.hypothesis_adequacy[repr(coffee)] is not HypothesisAdequacy.INADEQUATE
        assert b.observation_warrant == {repr(coffee): NONE}


def test_wait_at_entered_by_the_walks_completion_is_warranted(model5):
    # the walk to the machine completes (at holds): wait_at entered by the completion, warranted
    coffee = coffee_key(model5)
    machine = coffee.bindings["?coffee_machine"]
    w = build_world_state(model5)
    mx, my = w.object_positions[machine]
    rec = recognizer(model5, [coffee])
    k = repr(coffee)
    b = walk(rec, [(mx, my + 60.0), (mx, my + 40.0)], w)[-1]
    assert rec._expected[k].action_name == "move_to" and b.observation_warrant == {k: OBS}
    b = rec.update(obs(2, (mx, my + 20.0)), world_with(w, add=[pred("at", H, machine)]))
    assert rec._expected[k].action_name == "wait_at" and b.observation_warrant == {k: OBS}


def test_an_unresolved_move_to_has_no_movement_warrant(model):
    # a move_to whose target position cannot be resolved this tick: a movement target, but no gain computable
    # (ruled at the G-build plan step): no warrant however the human walks. Distinct from a stationary phase,
    # which has no movement target at all.
    start = start_of(model)
    w = build_world_state(model)
    unresolved = dataclasses.replace(w, object_positions={o: p for o, p in w.object_positions.items()
                                                          if o != "item_3"})
    rec = recognizer(model, [item("item_3")])
    k = repr(item("item_3"))
    bs = walk(rec, [start, (start[0], start[1] - SPEED), (start[0], start[1] - 2 * SPEED)], unresolved)
    assert rec._expected[k].action_name == "move_to"
    assert rec._expected[k].schema.movement_target_key is not None
    assert [b.observation_warrant[k] for b in bs] == [NONE, NONE, NONE]


# ---------------------------------------------------------------------------
# The reset: at a boundary, at a phase change
# ---------------------------------------------------------------------------

def test_warrant_resets_at_a_boundary(model):
    # the release of item_3 is a boundary: item_2's walk is opened by it, with every origin at the human; on the
    # boundary tick and the latency tick after it (standing) nothing is warranted; one step toward item_2 warrants it
    w = build_world_state(model)
    p = w.object_positions[TABLE]
    placing = world_with(w, add=[pred("holding", H, "item_3"), pred("at", H, TABLE)],
                         remove=[pred("obj_at", "item_3", "shelf_3")])
    placed = world_with(placing, add=[pred("obj_at", "item_3", TABLE)], remove=[pred("holding", H, "item_3")])
    rec = recognizer(model, [item("item_3"), item("item_2")])
    k2 = repr(item("item_2"))
    rec.update(obs(0, p), placing)
    b = rec.update(obs(1, p), placed)
    assert b.episode_boundary and b.observation_warrant == {k2: NONE}
    b = rec.update(obs(2, p), placed)
    assert b.hypothesis_adequacy[k2] is HypothesisAdequacy.ADEQUATE and b.observation_warrant == {k2: NONE}
    gx, gy = w.object_positions["item_2"]
    d = math.hypot(gx - p[0], gy - p[1])
    b = rec.update(obs(3, (p[0] + SPEED * (gx - p[0]) / d, p[1] + SPEED * (gy - p[1]) / d)), placed)
    assert b.observation_warrant == {k2: OBS}


def test_neither_source_crosses_a_boundary_within_one_phase(model5):
    # A boundary that leaves item_3's phase unchanged (a wait_at's completion: waited(human, machine) starts to
    # hold; the world constructed for the boundary alone, the human "at" the machine throughout): the phase's
    # origin moves to the human and no phase of the new episode was entered by a completion, so both sources
    # reset. First the movement source (a warranted walk), then the entry source (pick_up entered by the walk's
    # completion).
    machine = coffee_key(model5).bindings["?coffee_machine"]
    at_machine = dict(add=[pred("at", H, machine)])
    waited = [pred("at", H, machine), pred("waited", H, machine)]
    k3 = repr(item("item_3"))
    steps = delivery(model5)

    rec = recognizer(model5, [item("item_3")])
    for t, (p, w) in enumerate(steps[:3]):
        b = rec.update(obs(t, p), world_with(w, **at_machine))
    assert rec._expected[k3].action_name == "move_to" and b.observation_warrant == {k3: OBS}
    p, w = steps[2]
    b = rec.update(obs(3, p), world_with(w, add=waited))
    assert b.episode_boundary and rec._expected[k3].action_name == "move_to"
    assert b.observation_warrant == {k3: NONE}

    rec = recognizer(model5, [item("item_3")])
    for t, (p, w) in enumerate(steps[:ARRIVAL + 1]):
        b = rec.update(obs(t, p), world_with(w, **at_machine))
    assert rec._expected[k3].action_name == "pick_up" and b.observation_warrant == {k3: OBS}
    p, w = steps[ARRIVAL]
    b = rec.update(obs(ARRIVAL + 1, p), world_with(w, add=waited))
    assert b.episode_boundary and rec._expected[k3].action_name == "pick_up"
    assert b.observation_warrant == {k3: NONE}


def test_warrant_resets_at_a_regress(model):
    # pick_up, entered by the walk's completion, is warranted; at() lost (a regress at the proximity threshold)
    # opens the walk again, from no completion: unwarranted while nothing is gained, warranted after a step toward
    rec = recognizer(model, [item("item_3")])
    k = repr(item("item_3"))
    steps = delivery(model)
    for t, (p, w) in enumerate(steps[:ARRIVAL + 1]):
        b = rec.update(obs(t, p), w)
    assert rec._expected[k].action_name == "pick_up" and b.observation_warrant == {k: OBS}
    p, _ = steps[ARRIVAL]
    w = build_world_state(model)
    b = rec.update(obs(ARRIVAL + 1, p), w)
    assert rec._expected[k].action_name == "move_to" and b.observation_warrant == {k: NONE}
    b = rec.update(obs(ARRIVAL + 2, (p[0], p[1] - 5.0)), w)
    assert b.observation_warrant == {k: OBS}


def test_warrant_is_empty_when_exhausted(model):
    w = build_world_state(model)
    p = w.object_positions[TABLE]
    done = world_with(w, add=[pred("obj_at", "item_3", TABLE)], remove=[pred("obj_at", "item_3", "shelf_3")])
    rec = recognizer(model, [item("item_3")])
    b = rec.update(obs(0, p), done)
    assert b.lifecycle is RecognizerLifecycle.EXHAUSTED and b.observation_warrant == {}


# ---------------------------------------------------------------------------
# The gate: theta, adequacy, warrant (AD1, AD4); commitment (AD2); AD3
# ---------------------------------------------------------------------------

I3, I2 = "deliver_item(?item=item_3)", "deliver_item(?item=item_2)"
I5 = "deliver_item(?item=item_5)"


def belief(leader, adequacy, warrant, confidence=0.9):
    rival = I5 if leader != I5 else I2
    return BeliefState(timestamp=0.0, agent_id=H, distribution={leader: confidence, rival: 1.0 - confidence},
                       most_likely=leader, confidence=confidence, finding=AdequacyFinding.ADEQUATE,
                       lifecycle=RecognizerLifecycle.LIVE, tails={}, hypothesis_adequacy={leader: adequacy},
                       observation_warrant={leader: warrant}, episode_boundary=False)


def planner(model, assigned):
    """A meta-planner on the model's robot's parts, given the observed human's assigned tasks (None: prior off)."""
    robot = next(iter(model.robots.values()))
    return MetaPlanner(task_model=robot.meta_planner._task_model, projector=robot.projector,
                       recognizer=robot.recognizer, min_separation=50.0, human_agent_id=H,
                       observed_assigned_tasks=assigned)


def human_assigned(sid):
    """The scenario's human's assigned tasks, as the loader passes them with the prior on: with the determined
    parameter (the kitting table) the hypothesis keys omit."""
    return next(a for a in domain_config["scenarios"][sid].agents if a.agent_type == "human").assigned_tasks


def test_the_gates_three_conditions_in_order(model):
    # scenario_s01_01's human is assigned item_3 and item_2; item_5 is not assigned
    mp = planner(model, human_assigned("scenario_s01_01"))
    A, I, N = HypothesisAdequacy.ADEQUATE, HypothesisAdequacy.INADEQUATE, HypothesisAdequacy.NO_OBSERVATION
    below = DEFAULT_THETA - 0.01
    assert mp._clears_gate(belief(I5, A, NONE, confidence=below)) is GateOutcome.BELOW_THETA
    assert mp._clears_gate(belief(I5, N, NONE)) is GateOutcome.LEADER_NO_OBSERVATION
    assert mp._clears_gate(belief(I5, I, OBS)) is GateOutcome.LEADER_INADEQUATE       # inadequacy asked first
    assert mp._clears_gate(belief(I3, I, NONE)) is GateOutcome.LEADER_INADEQUATE      # commitment does not help
    assert mp._clears_gate(belief(I5, A, NONE)) is GateOutcome.LEADER_UNWARRANTED
    assert mp._clears_gate(belief(I5, A, OBS)) is GateOutcome.CLEARS                  # observation warrant
    assert mp._clears_gate(belief(I3, A, NONE)) is GateOutcome.CLEARS                 # commitment warrant
    assert mp._clears_gate(belief(I2, A, NONE)) is GateOutcome.CLEARS


def test_commitment_is_matched_by_task_equality(model):
    # the assigned task names the kitting table (a determined parameter); the hypothesis does not: same_task
    # matches them, as the support restriction does. A task that differs in its goal binding does not match.
    assigned = human_assigned("scenario_s01_01")
    assert any(Var("?kitting_table") in t.bindings for t in assigned)
    mp = planner(model, assigned)
    assert mp._warrant(belief(I3, HypothesisAdequacy.ADEQUATE, NONE))
    other = [TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_5")})]
    assert not planner(model, other)._warrant(belief(I3, HypothesisAdequacy.ADEQUATE, NONE))


def test_prior_off_has_no_commitment_warrant(model):
    # no assigned tasks known: an assigned delivery needs observation warrant like any hypothesis (expected, 1.4)
    for assigned in (None, []):
        mp = planner(model, assigned)
        assert mp._clears_gate(belief(I3, HypothesisAdequacy.ADEQUATE, NONE)) is GateOutcome.LEADER_UNWARRANTED
        assert mp._clears_gate(belief(I3, HypothesisAdequacy.ADEQUATE, OBS)) is GateOutcome.CLEARS


def test_the_refusal_is_logged_and_the_record_stays_empty(model, caplog):
    # the world as built carries no previous observation of the human, so no fallback: the reason alone
    mp = planner(model, None)
    w = build_world_state(model)
    with caplog.at_level(logging.INFO):
        assert mp.update_human_projection(belief(I5, HypothesisAdequacy.ADEQUATE, NONE), w) is None
    assert "projection=none(leader_unwarranted)" in caplog.text
    assert mp._projected_hypothesis is None


@pytest.mark.parametrize("leader, warrant, assigned, printed", [
    (I3, NONE, True, "warrant=commitment"),
    (I5, OBS, True, "warrant=observation"),
    (I3, OBS, True, "warrant=commitment,observation"),
])
def test_the_admissions_warrant_source_is_named(model, caplog, leader, warrant, assigned, printed):
    # the admission's [meta-proj] line names its sources (AD4); both when both hold. The projector is not the
    # subject: it is stood in for so that the admission is built.
    mp = planner(model, human_assigned("scenario_s01_01") if assigned else None)
    mp._projector = type("Stub", (), {"project_human": lambda self, **kw: object()})()
    with caplog.at_level(logging.INFO):
        mp.update_human_projection(belief(leader, HypothesisAdequacy.ADEQUATE, warrant), build_world_state(model))
    line = next(l for l in caplog.text.splitlines() if "[meta-proj]" in l)
    assert line.endswith(f"projection=built {printed}")
    assert mp._projected_hypothesis == leader


EXECUTING = ExecutorState(agent_id="robot_0", holding=None,
                          current_task=TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4")}))


def test_the_entering_side_waits_for_warrant(model):
    # no record: an adequate leader at theta without warrant does not fire recognition_changed; warranted, it does
    mp = planner(model, None)
    w = build_world_state(model)
    assert not mp.evaluate_triggers(belief(I5, HypothesisAdequacy.ADEQUATE, NONE), w, EXECUTING).fired
    assert mp.evaluate_triggers(belief(I5, HypothesisAdequacy.ADEQUATE, OBS), w, EXECUTING).fired


def test_loss_of_warrant_fires_nothing(model):
    # AD3: the recorded hypothesis, still most likely and adequate, loses its observation warrant: no trigger
    mp = planner(model, None)
    mp._projected_hypothesis = I5
    w = build_world_state(model)
    d = mp.evaluate_triggers(belief(I5, HypothesisAdequacy.ADEQUATE, NONE), w, EXECUTING)
    assert not d.fired
