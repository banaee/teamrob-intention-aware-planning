# tests/test_l_build.py
"""
T-D L, the belief lifecycle (design_decisions.md, "T-D L: the belief lifecycle", as amended on the L-records report):
L1 the episode boundary is the observed agent's completion of a terminal action, read from the world's completion
conditions through the action's own binding (its preconditions held for the agent on the previous tick; a grounding
of its completion condition holds now and did not then); L2 (ii) retraction, the recorded hypothesis's hypothesis
adequacy inadequate; L4 retirement while the terminal fact holds, re-entry at exactly 1/|H| with the incumbents'
proportions kept; L5 B the boundary flag fires recognition_changed for a recorded decision. Every expected value is
derived from the entry, none from a run. As in test_td1_adequacy.py the world is a layout's initial world changed by
hand (the enlarged room, env_layout_11: two kitting tables, a coffee machine).
Run from the repo root:  PYTHONHASHSEED=0 python -m pytest tests/test_l_build.py
"""

import logging
import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "mesa_sim"))

from tests.test_td1_adequacy import H, check_r6, item, obs, pred, recognizer, world_with
from tests.test_th1_tree import model_for, registered
from shared.meta_planner import DEFAULT_THETA
from shared.recognizer import build_hypothesis_space
from shared.types import (
    ActionContext, AdequacyFinding, BeliefState, Const, ExecutorState, HypothesisAdequacy, Observation,
    RecognitionChange, RecognizerLifecycle, SpatialContext, TaskInstance, Var,
)
from domains.kitting.tasks import deliver_item
from mesa_sim.world_state_builder import build_world_state

KT0, KT1, MACHINE = "kitting_table_0", "kitting_table_1", "coffee_machine_0"


@pytest.fixture(scope="module")
def model():
    return model_for("env_layout_11", registered("env_layout_11", "scenario_s09_08"))


def coffee(m):
    robot = next(iter(m.robots.values()))
    return next(h for h in build_hypothesis_space(robot.recognizer.task_model, m._objects_by_type)
                if h.task_name == "coffee_break")


def release_obs(t, pos):
    return Observation(timestamp=float(t), agent_id=H, detected_microaction="RELEASE",
                       spatial_context=SpatialContext(position=pos, orientation=0.0), action_context=ActionContext())


def carrying(w, i, shelf):
    """The world with the human holding item i, as the body builds it (obj_at at the holder)."""
    return world_with(w, add=[pred("holding", H, i), pred("obj_at", i, H)], remove=[pred("obj_at", i, shelf)])


def placed(w, i, container):
    """The release: item i no longer held, placed at `container`."""
    return world_with(w, add=[pred("obj_at", i, container)], remove=[pred("holding", H, i), pred("obj_at", i, H)])


# ---------------------------------------------------------------------------
# L1: the boundary
# ---------------------------------------------------------------------------

def test_a_release_at_a_wrong_container_is_a_boundary_without_a_pin(model, caplog):
    w = build_world_state(model)
    p = w.object_positions[KT1]
    held = carrying(w, "item_1", "shelf_1")
    rec = recognizer(model, [item("item_1"), item("item_2")])
    b = rec.update(obs(0, p), held)
    assert not b.episode_boundary
    with caplog.at_level(logging.INFO):
        b = rec.update(release_obs(1, p), placed(held, "item_1", KT1))
    assert b.episode_boundary
    assert "completed place(item_1,kitting_table_1)" in caplog.text
    # no pin: deliver_item(item_1)'s terminal fact is obj_at(item_1, kitting_table_0); both live, at the prior
    assert rec._retired == set()
    assert rec._evidence == {repr(item("item_1")): 0.5, repr(item("item_2")): 0.5}
    assert b.finding is AdequacyFinding.UNRESOLVED and b.tails == {}
    check_r6(rec, b)


def test_a_bare_release_is_no_boundary(model):
    # the completion channel's RELEASE with the item still held: no completion condition changed
    w = build_world_state(model)
    p = w.object_positions[KT0]
    held = world_with(carrying(w, "item_1", "shelf_1"), add=[pred("at", H, KT0)])
    rec = recognizer(model, [item("item_1"), item("item_2")])
    rec.update(obs(0, p), held)
    b = rec.update(release_obs(1, p), held)
    assert not b.episode_boundary
    assert rec._retired == set()


def test_waited_starting_is_a_boundary_and_a_pin(model):
    w = build_world_state(model)
    p = w.object_positions[MACHINE]
    standing = world_with(w, add=[pred("at", H, MACHINE)])
    c = coffee(model)
    rec = recognizer(model, [c, item("item_1"), item("item_2")])
    rec.update(obs(0, p), standing)
    b = rec.update(obs(1, p), world_with(standing, add=[pred("waited", H, MACHINE)]))
    assert b.episode_boundary
    assert rec._retired == {repr(c)}
    assert rec._evidence == {repr(item("item_1")): 0.5, repr(item("item_2")): 0.5}
    check_r6(rec, b)
    # the next tick, waited still holding: no second boundary
    b = rec.update(obs(2, p), world_with(standing, add=[pred("waited", H, MACHINE)]))
    assert not b.episode_boundary


def test_a_mid_task_return_is_a_boundary(model):
    # deliver_item(item_2) under deliver_with_return: its first place returns item_1 to shelf_1 (consequence D)
    w = build_world_state(model)
    p = w.object_positions["shelf_1"]
    held = world_with(carrying(w, "item_1", "shelf_1"), add=[pred("at", H, "shelf_1")])
    rec = recognizer(model, [item("item_1"), item("item_2")])
    rec.update(obs(0, p), held)
    assert rec._expected[repr(item("item_2"))].action_name == "place"          # the return
    b = rec.update(obs(1, p), placed(held, "item_1", "shelf_1"))
    assert b.episode_boundary
    assert rec._retired == set()


def test_another_agents_delivery_is_a_pin_without_a_boundary(model):
    w = build_world_state(model)
    robot = next(iter(model.robots))
    x, y = w.agent_positions[H]
    rec = recognizer(model, [item("item_1"), item("item_2")])
    held = world_with(w, add=[pred("holding", robot, "item_2"), pred("obj_at", "item_2", robot)],
                      remove=[pred("obj_at", "item_2", "shelf_2")])
    rec.update(obs(0, (x, y)), held)
    b = rec.update(obs(1, (x - 20.0, y)),
                   world_with(held, add=[pred("obj_at", "item_2", KT0)],
                              remove=[pred("holding", robot, "item_2"), pred("obj_at", "item_2", robot)]))
    assert not b.episode_boundary
    assert rec._retired == {repr(item("item_2"))}


# ---------------------------------------------------------------------------
# L4: liveness and re-entry
# ---------------------------------------------------------------------------

def walk(rec, worlds_positions, t0):
    b = None
    for k, (world, pos) in enumerate(worlds_positions):
        b = rec.update(obs(t0 + k, pos), world)
        check_r6(rec, b)
    return b


def test_coffee_re_enters_when_waited_clears_at_one_over_h_with_the_incumbents_proportions_kept(model):
    w = build_world_state(model)
    p = w.object_positions[MACHINE]
    ix, iy = w.object_positions["item_1"]
    standing = world_with(w, add=[pred("at", H, MACHINE)])
    waited = world_with(standing, add=[pred("waited", H, MACHINE)])
    away = world_with(w, add=[pred("waited", H, MACHINE)])       # still holding while the human walks, by hand
    d = math.hypot(ix - p[0], iy - p[1])
    toward = [(p[0] + 20.0 * k * (ix - p[0]) / d, p[1] + 20.0 * k * (iy - p[1]) / d) for k in range(1, 6)]
    c = coffee(model)
    # the same ticks seen with and without coffee_break in the space: the incumbents' ratio on the re-entry tick is
    # the ratio they have without it
    rec = recognizer(model, [c, item("item_1"), item("item_2")])
    ref = recognizer(model, [item("item_1"), item("item_2")])
    ticks = [(standing, p), (waited, p)] + [(away, q) for q in toward]
    walk(rec, ticks, 0)
    walk(ref, ticks, 0)
    assert rec._retired == {repr(c)}
    q = (toward[-1][0] + 20.0 * (ix - p[0]) / d, toward[-1][1] + 20.0 * (iy - p[1]) / d)
    cleared = w                                                    # waited clears on the agent's next step
    b = rec.update(obs(len(ticks), q), cleared)
    r = ref.update(obs(len(ticks), q), cleared)
    check_r6(rec, b)
    assert not b.episode_boundary and rec._retired == set()
    assert rec._evidence[repr(c)] == pytest.approx(1.0 / 3.0, abs=1e-12)
    i1, i2 = repr(item("item_1")), repr(item("item_2"))
    assert rec._evidence[i1] / rec._evidence[i2] == pytest.approx(ref._evidence[i1] / ref._evidence[i2], rel=1e-12)
    assert rec._evidence[i1] + rec._evidence[i2] == pytest.approx(2.0 / 3.0, abs=1e-12)
    assert rec._evidence[i1] != rec._evidence[i2]                  # the walk toward item_1 made them differ
    # an ordinary first observation: origin here, no entry latency
    assert rec._origin[repr(c)] == q and rec._entry_latency[repr(c)] == 0.0


def test_a_delivery_re_enters_when_its_item_leaves_the_table(model):
    w = build_world_state(model)
    p = w.object_positions[KT0]
    at_table = world_with(w, add=[pred("at", H, KT0)])
    held = carrying(at_table, "item_1", "shelf_1")
    delivered = placed(held, "item_1", KT0)
    rec = recognizer(model, [item("item_1"), item("item_2"), item("item_3")])
    rec.update(obs(0, p), held)
    b = rec.update(obs(1, p), delivered)                          # the pin and a boundary
    assert b.episode_boundary and rec._retired == {repr(item("item_1"))}
    b = rec.update(obs(2, p), delivered)
    assert rec._retired == {repr(item("item_1"))}
    # the human picks item_1 up again: obj_at(item_1, kitting_table_0) no longer holds
    regrasped = world_with(delivered, add=[pred("holding", H, "item_1"), pred("obj_at", "item_1", H)],
                           remove=[pred("obj_at", "item_1", KT0)])
    b = rec.update(obs(3, p), regrasped)
    check_r6(rec, b)
    assert rec._retired == set()
    assert rec._evidence[repr(item("item_1"))] == pytest.approx(1.0 / 3.0, abs=1e-12)
    assert b.lifecycle is RecognizerLifecycle.LIVE


# ---------------------------------------------------------------------------
# L2 (ii) and L5 B: the meta-planner's two conditions
# ---------------------------------------------------------------------------

I1, I2 = "deliver_item(?item=item_1)", "deliver_item(?item=item_2)"


def belief(leader, adequacy, confidence=0.9, boundary=False):
    rival = I2 if leader == I1 else I1
    return BeliefState(timestamp=0.0, agent_id=H, distribution={leader: confidence, rival: 1.0 - confidence},
                       most_likely=leader, confidence=confidence, finding=AdequacyFinding.ADEQUATE,
                       lifecycle=RecognizerLifecycle.LIVE, tails={}, hypothesis_adequacy=adequacy,
                       episode_boundary=boundary)


@pytest.fixture
def recorded(model):
    """The meta-planner with I1 recorded: a projection admitted on an adequate leader above theta."""
    mp = next(iter(model.robots.values())).meta_planner
    mp._projected_hypothesis = None
    w = build_world_state(model)
    b = belief(I1, {I1: HypothesisAdequacy.ADEQUATE, I2: HypothesisAdequacy.ADEQUATE})
    assert b.confidence >= DEFAULT_THETA
    assert mp.update_human_projection(b, w) is not None
    assert mp._projected_hypothesis == I1
    executing = ExecutorState(agent_id=next(iter(model.robots)), holding=None,
                              current_task=TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3")}))
    return mp, w, executing


def test_the_recorded_hypothesis_turning_inadequate_fires_a_retraction(recorded, caplog):
    mp, w, ex = recorded
    b = belief(I1, {I1: HypothesisAdequacy.INADEQUATE, I2: HypothesisAdequacy.ADEQUATE})
    d = mp.evaluate_triggers(b, w, ex)
    assert d.fired and d.reason == "recognition_changed" and d.cause is RecognitionChange.RETRACTION
    with caplog.at_level(logging.INFO):
        assert mp.update_human_projection(b, w) is None
    assert "projection=none(leader_inadequate)" in caplog.text
    assert mp._projected_hypothesis is None
    # retracted once: nothing recorded, and the inadequate leader does not clear the gate
    assert not mp.evaluate_triggers(b, w, ex).fired


def test_a_rivals_inadequacy_fires_nothing(recorded):
    mp, w, ex = recorded
    b = belief(I1, {I1: HypothesisAdequacy.ADEQUATE, I2: HypothesisAdequacy.INADEQUATE})
    assert not mp.evaluate_triggers(b, w, ex).fired


def test_leaving_adequate_for_no_observation_fires_nothing_then_inadequate_fires(recorded):
    # the state reading: a no-observation tick between adequate and inadequate (a regress) does not hide it
    mp, w, ex = recorded
    b = belief(I1, {I1: HypothesisAdequacy.NO_OBSERVATION, I2: HypothesisAdequacy.ADEQUATE})
    assert not mp.evaluate_triggers(b, w, ex).fired
    b = belief(I1, {I1: HypothesisAdequacy.INADEQUATE, I2: HypothesisAdequacy.ADEQUATE})
    assert mp.evaluate_triggers(b, w, ex).cause is RecognitionChange.RETRACTION


def test_a_boundary_fires_without_a_leader_change(recorded, caplog):
    mp, w, ex = recorded
    b = belief(I1, {I1: HypothesisAdequacy.NO_OBSERVATION, I2: HypothesisAdequacy.NO_OBSERVATION}, boundary=True)
    d = mp.evaluate_triggers(b, w, ex)
    assert d.fired and d.cause is RecognitionChange.BOUNDARY
    with caplog.at_level(logging.INFO):
        assert mp.update_human_projection(b, w) is None
    assert "projection=none(leader_no_observation)" in caplog.text
    assert mp._projected_hypothesis is None


def test_a_dip_below_theta_still_fires_nothing(recorded):
    mp, w, ex = recorded
    b = belief(I1, {I1: HypothesisAdequacy.ADEQUATE, I2: HypothesisAdequacy.ADEQUATE}, confidence=0.6)
    assert not mp.evaluate_triggers(b, w, ex).fired


def test_a_replacement_is_still_reported_as_replaced(recorded):
    mp, w, ex = recorded
    b = belief(I2, {I1: HypothesisAdequacy.ADEQUATE, I2: HypothesisAdequacy.ADEQUATE}, boundary=True)
    assert mp.evaluate_triggers(b, w, ex).cause is RecognitionChange.REPLACED


def test_a_re_entry_keeps_the_tie_break_in_hypothesis_order(model):
    # one incumbent and coffee_break returning: 1/2 each exactly; ties go to the first live key in sorted order
    # (handback §1.7), coffee_break(...) before deliver_item(...), whatever order the re-entry was computed in
    w = build_world_state(model)
    p = w.object_positions[MACHINE]
    standing = world_with(w, add=[pred("at", H, MACHINE)])
    c = coffee(model)
    rec = recognizer(model, [c, item("item_2")])
    rec.update(obs(0, p), standing)
    rec.update(obs(1, p), world_with(standing, add=[pred("waited", H, MACHINE)]))
    b = rec.update(obs(2, (p[0] + 20.0, p[1])), w)
    assert rec._evidence == {repr(c): 0.5, repr(item("item_2")): 0.5}
    assert list(rec._evidence) == [repr(c), repr(item("item_2"))]
    assert b.most_likely == repr(c)
    # and at a later boundary, the prior over the live set is in hypothesis order too (item_2 delivered to kitting_table_1,
    # a boundary without a pin: coffee_break and item_2 at 1/2 again)
    q = w.object_positions[KT1]
    held = carrying(w, "item_2", "shelf_2")
    rec.update(obs(3, q), held)
    b = rec.update(obs(4, q), placed(held, "item_2", KT1))
    assert b.episode_boundary
    assert list(rec._evidence) == [repr(c), repr(item("item_2"))] and b.most_likely == repr(c)
