# tests/test_tg_liveness.py
"""
T-G A4, liveness by applicability (docs/handoffs/plan_T-G_stage1.md, 3b): a hypothesis is live only while its task is
applicable, i.e. the planner decomposes it for the observed agent in the present world (AdaptivePlanner.is_applicable).
Not applicable: it leaves the live set H as a retired one does, pinned at BELIEF_FLOOR; applicable again: retired if its
terminal fact holds, else it re-enters through L4's returning path at 1/|H|. Not applicable on the first tick, it never
enters H. A retired hypothesis that becomes inapplicable stays retired. Every expected value is derived from the
ruling, none from a run. As in test_td1_adequacy.py the world is env_layout_01's initial world changed by hand: the
human holds item_2 and item_2 has no home container, so deliver_item(item_3) and deliver_item(item_4) select
deliver_with_return, whose derived container has no value (DecompositionError), while deliver_item(item_2) selects
deliver_already_held.
Run from the repo root:  PYTHONHASHSEED=0 python -m pytest tests/test_tg_liveness.py
"""

import dataclasses
import logging
import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "mesa_sim"))

from tests.test_td1_adequacy import H, TABLE, check_r6, item, obs, pred, recognizer, world_with
from tests.test_th1_tree import model_for, registered
from shared.planner import AdaptivePlanner
from shared.recognizer import BELIEF_FLOOR
from shared.types import RecognizerLifecycle
from mesa_sim.world_state_builder import build_world_state


@pytest.fixture(scope="module")
def model():
    return model_for("env_layout_01", registered("env_layout_01", "scenario_s01_01"))


def holding_item_2(w):
    """The human holds item_2: every deliver_item hypothesis applicable."""
    return world_with(w, add=[pred("holding", H, "item_2"), pred("obj_at", "item_2", H)],
                      remove=[pred("obj_at", "item_2", "shelf_2")])


def without_home_of_item_2(w):
    """item_2 has no home container: deliver_item(item_3) and (item_4) not applicable, deliver_item(item_2) is."""
    return dataclasses.replace(
        w, object_home_container={k: v for k, v in w.object_home_container.items() if k != "item_2"})


@pytest.fixture(scope="module")
def worlds(model):
    applicable = holding_item_2(build_world_state(model))
    return applicable, without_home_of_item_2(applicable)


def lines(caplog, tag):
    return [r.getMessage() for r in caplog.records if r.getMessage().startswith(tag)]


def test_applicability_is_the_planners(model, worlds):
    applicable, inapplicable = worlds
    planner = AdaptivePlanner(knowledge=next(iter(model.robots.values())).recognizer.task_model)
    for i in ("item_2", "item_3", "item_4"):
        assert planner.is_applicable(item(i).task_instance(), H, applicable)
    assert planner.is_applicable(item("item_2").task_instance(), H, inapplicable)
    assert not planner.is_applicable(item("item_3").task_instance(), H, inapplicable)
    # the recognizer's inapplicable set is the planner's answer, hypothesis by hypothesis
    rec = recognizer(model, [item("item_2"), item("item_3"), item("item_4")])
    rec.update(obs(0, (350.0, 200.0)), inapplicable)
    assert rec._inapplicable == {repr(h) for h in rec._hypotheses
                                 if not planner.is_applicable(h.task_instance(), H, inapplicable)}


def test_an_inapplicable_hypothesis_leaves_the_live_set_and_is_pinned(model, worlds, caplog):
    applicable, inapplicable = worlds
    k2, k3, k4 = repr(item("item_2")), repr(item("item_3")), repr(item("item_4"))
    rec = recognizer(model, [item("item_2"), item("item_3"), item("item_4")])
    with caplog.at_level(logging.INFO):
        for t in range(3):
            b = rec.update(obs(t, (350.0 - 10.0 * t, 200.0)), applicable)
        assert set(rec._evidence) == {k2, k3, k4}
        b = rec.update(obs(3, (320.0, 200.0)), inapplicable)
        b = rec.update(obs(4, (310.0, 200.0)), inapplicable)
    # it leaves H: no evidence, no phase state, no finding output; the others carry the belief
    assert set(rec._evidence) == {k2}
    assert rec._inapplicable == {k3, k4} and rec._retired == set()
    for k in (k3, k4):
        assert k not in rec._base and k not in rec._expected and k not in rec._origin
        assert k not in b.tails and k not in b.hypothesis_adequacy and k not in b.observation_warrant
    # the pin, as for a retired hypothesis
    assert b.distribution[k3] == BELIEF_FLOOR and b.distribution[k4] == BELIEF_FLOOR
    assert b.most_likely == k2 and math.isclose(b.confidence, 1.0 - 2 * BELIEF_FLOOR)
    check_r6(rec, b)
    # logged once per leaving, at the tick it leaves
    assert lines(caplog, "[IR-inapplicable]") == [
        f"[IR-inapplicable] step=3 {k3} leaves the live set: no applicable method",
        f"[IR-inapplicable] step=3 {k4} leaves the live set: no applicable method",
    ]


def test_an_applicable_again_hypothesis_re_enters_at_one_over_h(model, worlds, caplog):
    applicable, inapplicable = worlds
    k2, k3, k4 = repr(item("item_2")), repr(item("item_3")), repr(item("item_4"))
    rec = recognizer(model, [item("item_2"), item("item_3"), item("item_4")])
    for t in range(3):
        rec.update(obs(t, (350.0 - 10.0 * t, 200.0)), applicable)
    rec.update(obs(3, (320.0, 200.0)), inapplicable)
    with caplog.at_level(logging.INFO):
        b = rec.update(obs(4, (310.0, 200.0)), applicable)
    # L4's returning path: each returning hypothesis takes exactly 1/|H|, as a first observation
    assert rec._inapplicable == set() and set(rec._evidence) == {k2, k3, k4}
    for k in (k3, k4):
        assert math.isclose(rec._evidence[k], 1.0 / 3.0)
        assert rec._origin[k] == (310.0, 200.0) and rec._entry_latency[k] == 0.0
    assert math.isclose(sum(rec._evidence.values()), 1.0)
    check_r6(rec, b)
    assert lines(caplog, "[IR-reentry]") == [
        f"[IR-reentry] step=4 {k3} live again: applicable",
        f"[IR-reentry] step=4 {k4} live again: applicable",
    ]


def test_not_applicable_on_the_first_tick_never_enters(model, worlds, caplog):
    applicable, inapplicable = worlds
    k2, k3 = repr(item("item_2")), repr(item("item_3"))
    rec = recognizer(model, [item("item_2"), item("item_3")])
    with caplog.at_level(logging.INFO):
        b = rec.update(obs(0, (350.0, 200.0)), inapplicable)
    # H is item_2 alone: the prior over H, never a share for item_3
    assert rec._evidence == {k2: 1.0}
    assert b.distribution == {k2: 1.0 - BELIEF_FLOOR, k3: BELIEF_FLOOR}
    assert k3 not in rec._expected
    check_r6(rec, b)
    assert lines(caplog, "[IR-inapplicable]") == [
        f"[IR-inapplicable] step=0 {k3} does not enter the live set: no applicable method"]
    # applicable later: it enters through the returning path, at 1/|H|
    rec.update(obs(1, (340.0, 200.0)), applicable)
    assert math.isclose(rec._evidence[k3], 0.5)


def test_exhausted_when_no_hypothesis_is_applicable(model, worlds):
    applicable, inapplicable = worlds
    k3, k4 = repr(item("item_3")), repr(item("item_4"))
    rec = recognizer(model, [item("item_3"), item("item_4")])
    b = rec.update(obs(0, (350.0, 200.0)), inapplicable)
    assert b.lifecycle is RecognizerLifecycle.EXHAUSTED
    assert b.finding is None and b.tails == {} and b.hypothesis_adequacy == {}
    assert b.most_likely is None and b.confidence == 0.0
    assert b.distribution == {k3: BELIEF_FLOOR, k4: BELIEF_FLOOR}
    assert rec._evidence == {}
    # live again from exhaustion: the returning hypotheses share H uniformly
    b = rec.update(obs(1, (340.0, 200.0)), applicable)
    assert b.lifecycle is RecognizerLifecycle.LIVE
    assert rec._evidence == {k3: 0.5, k4: 0.5}


def test_a_retired_hypothesis_that_becomes_inapplicable_stays_retired(model, worlds, caplog):
    applicable, inapplicable = worlds
    k2, k3 = repr(item("item_2")), repr(item("item_3"))
    delivered = [pred("obj_at", "item_3", TABLE)], [pred("obj_at", "item_3", "shelf_3")]
    rec = recognizer(model, [item("item_2"), item("item_3")])
    with caplog.at_level(logging.INFO):
        rec.update(obs(0, (350.0, 200.0)), world_with(applicable, *delivered))
        assert rec._retired == {k3}
        # inapplicable while retired: retired still, not inapplicable, nothing logged
        b = rec.update(obs(1, (340.0, 200.0)), world_with(inapplicable, *delivered))
        assert rec._retired == {k3} and rec._inapplicable == set()
        assert b.distribution[k3] == BELIEF_FLOOR
        check_r6(rec, b)
        # applicable again with its terminal fact still holding: still retired, no re-entry
        rec.update(obs(2, (330.0, 200.0)), world_with(applicable, *delivered))
        assert rec._retired == {k3}
    assert lines(caplog, "[IR-inapplicable]") == [] and lines(caplog, "[IR-reentry]") == []


def test_an_inapplicable_hypothesis_whose_terminal_fact_holds_by_its_return_is_retired(model, worlds, caplog):
    applicable, inapplicable = worlds
    k3 = repr(item("item_3"))
    rec = recognizer(model, [item("item_2"), item("item_3")])
    with caplog.at_level(logging.INFO):
        rec.update(obs(0, (350.0, 200.0)), applicable)
        rec.update(obs(1, (340.0, 200.0)), inapplicable)
        assert rec._inapplicable == {k3}
        # the item is delivered while the hypothesis is not live; applicable again, it is retired (L4)
        rec.update(obs(2, (330.0, 200.0)), world_with(applicable, add=[pred("obj_at", "item_3", TABLE)],
                                                      remove=[pred("obj_at", "item_3", "shelf_3")]))
    assert rec._retired == {k3} and rec._inapplicable == set() and k3 not in rec._evidence
    assert lines(caplog, "[IR-reentry]") == []
    assert len(lines(caplog, "[IR-complete]")) == 1
