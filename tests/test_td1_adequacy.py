# tests/test_td1_adequacy.py
"""
T-D R and E, Stage 1: the recognizer without the `unknown` hypothesis (R1, R6) and
its adequacy finding (E1 to E7), with the membership ruling of 27 September 2026 (a
member is a live hypothesis with a derived phase whose phase holds an observation).
Every expected value is derived from the entry (design_decisions.md, "T-D R and E"),
none from a run. The world is env_layout_01's initial world, changed by hand: the
phase is derived from the world's predicates, the movement from the observed
positions, so a fixed world holds each hypothesis in one derived phase.
Run from the repo root:  PYTHONHASHSEED=0 python -m pytest tests/test_td1_adequacy.py
"""

import dataclasses
import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "mesa_sim"))

from shared import likelihood_functions
from shared.knowledge import ContextKnowledge
from shared.recognizer import BELIEF_FLOOR, HypothesisKey, IntentionRecognizer, build_hypothesis_space
from shared.types import (
    ActionContext, AdequacyFinding, Const, Observation, Predicate, RecognizerLifecycle, SpatialContext,
    TaskInstance, Var,
)
from domains.kitting.tasks import deliver_item
from mesa_sim.action_decomposer import _parse_duration_to_steps
from mesa_sim.world_state_builder import build_world_state
from tests.test_th1_tree import model_for, registered

H = "human_0"
TABLE = "kitting_table_0"
BETA, SPEED = 0.01, 20.0          # the body's values (mesa_configs.yaml), as the entry states them


@pytest.fixture(scope="module")
def model():
    return model_for("env_layout_01", registered("env_layout_01", "scenario_s01_01"))


def item(i):
    return HypothesisKey(deliver_item, {"?item": i})


def recognizer(m, hypotheses, alpha=0.05, assigned_tasks=None):
    robot = next(iter(m.robots.values()))
    return IntentionRecognizer(
        task_model=robot.recognizer.task_model, context=ContextKnowledge.default(), hypotheses=hypotheses,
        beta=BETA, speed=SPEED, duration_to_steps=lambda d: _parse_duration_to_steps(d, m),
        default_action_cost=1.0, alpha=alpha, assigned_tasks=assigned_tasks)


def pred(name, *args):
    return Predicate(name, tuple(Const(a) for a in args))


def world_with(w, add=(), remove=()):
    return dataclasses.replace(w, predicates=(set(w.predicates) - set(remove)) | set(add))


def obs(t, pos):
    return Observation(timestamp=float(t), agent_id=H, detected_microaction="STEP",
                       spatial_context=SpatialContext(position=pos, orientation=0.0),
                       action_context=ActionContext())


def live_set(rec):
    return {repr(h) for h in rec._hypotheses} - rec._inadmissible - rec._completed


def check_r6(rec, belief):
    """The R6 invariant at its two levels (ruled 27 Sept 2026): the normalised evidence
    sums to 1 over exactly H; the returned distribution sums to 1 with every key outside H
    at exactly BELIEF_FLOOR and no key outside the hypothesis space."""
    hs = live_set(rec)
    assert set(rec._evidence) == hs
    assert math.isclose(sum(rec._evidence.values()), 1.0, abs_tol=1e-9)
    space = {repr(h) for h in rec._hypotheses}
    assert set(belief.distribution) <= space
    assert math.isclose(sum(belief.distribution.values()), 1.0, abs_tol=1e-9)
    for k, v in belief.distribution.items():
        if k not in hs:
            assert v == BELIEF_FLOOR
    assert set(belief.tails) <= hs


# ---------------------------------------------------------------------------
# the tail probability S (E5)
# ---------------------------------------------------------------------------

def threshold(alpha, beta):
    """x at which S(x) = alpha: ln(1 + e^(-beta x)) = alpha ln 2."""
    return -math.log(2.0 ** alpha - 1.0) / beta


def test_tail_probability_at_the_entrys_thresholds():
    # v·D = 334 cm at alpha = 0.05, 497 cm at alpha = 0.01 (beta = 0.01 /cm)
    assert round(threshold(0.05, BETA)) == 334
    assert round(threshold(0.01, BETA)) == 497
    for alpha in (0.01, 0.05, 0.1):
        assert math.isclose(likelihood_functions.tail_probability(threshold(alpha, BETA), BETA), alpha, rel_tol=1e-12)
    assert likelihood_functions.tail_probability(334.0, BETA) > 0.05 > likelihood_functions.tail_probability(335.0, BETA)
    assert likelihood_functions.tail_probability(496.0, BETA) > 0.01 > likelihood_functions.tail_probability(497.0, BETA)


def test_tail_probability_is_one_at_or_below_zero():
    for x in (0.0, -1.0, -500.0):
        assert likelihood_functions.tail_probability(x, BETA) == 1.0


# ---------------------------------------------------------------------------
# R1, R6: the belief over H
# ---------------------------------------------------------------------------

def test_no_unknown_key_and_two_rivals_start_even(model):
    w = build_world_state(model)
    rec = recognizer(model, [item("item_3"), item("item_2")])
    b = rec.update(obs(0, w.agent_positions[H]), w)
    assert set(b.distribution) == {repr(item("item_3")), repr(item("item_2"))}
    assert all(math.isclose(v, 0.5) for v in b.distribution.values())
    check_r6(rec, b)


def test_r6_invariant_every_tick_with_pins_and_a_retirement(model):
    w = build_world_state(model)
    human = next(a for a in registered("env_layout_01", "scenario_s01_01").agents if a.agent_type == "human")
    hyps = build_hypothesis_space(next(iter(model.robots.values())).recognizer.task_model, model._objects_by_type)
    rec = recognizer(model, hyps, assigned_tasks=human.assigned_tasks)
    assert rec._inadmissible                          # the support restriction pins some keys
    x, y = w.agent_positions[H]
    retired = None
    for t in range(40):
        world = w
        if t >= 20:
            # an item delivered by someone else: its hypothesis is retired (the pin), no boundary
            world = world_with(w, add=[pred("obj_at", "item_2", TABLE)])
        b = rec.update(obs(t, (x - 10.0 * t, y - 5.0 * t)), world)
        check_r6(rec, b)
        if t >= 20:
            retired = repr(item("item_2"))
            assert retired in rec._completed
            assert retired not in rec._evidence and retired not in b.tails
            assert b.distribution[retired] == BELIEF_FLOOR
    assert retired is not None


def test_a_lone_live_hypothesis_reads_one_on_no_evidence_unresolved(model):
    w = build_world_state(model)
    rec = recognizer(model, [item("item_3")])
    b = rec.update(obs(0, w.agent_positions[H]), w)
    assert b.most_likely == repr(item("item_3"))
    assert b.confidence == 1.0
    assert b.finding is AdequacyFinding.UNRESOLVED
    assert b.lifecycle is RecognizerLifecycle.LIVE
    assert b.tails == {}


# ---------------------------------------------------------------------------
# E1 to E7: D, the finding, the reset
# ---------------------------------------------------------------------------

def test_first_tick_is_unresolved(model):
    w = build_world_state(model)
    rec = recognizer(model, [item("item_3"), item("item_2"), item("item_4")])
    b = rec.update(obs(0, w.agent_positions[H]), w)
    assert b.finding is AdequacyFinding.UNRESOLVED and b.tails == {}


def test_a_stand_in_a_move_to_phase_is_charged_17_ticks(model):
    # E3, E5: s_exp = 0 in move_to; 17 ticks of standing is v·D = 340 cm > 334 cm (alpha 0.05),
    # 16 ticks is 320 cm < 334; at alpha = 0.01 the threshold is 497 cm (25 ticks).
    w = build_world_state(model)
    p = w.agent_positions[H]
    for alpha, unexplained_from in ((0.05, 17), (0.01, 25)):
        rec = recognizer(model, [item("item_3")], alpha=alpha)
        assert rec.update(obs(0, p), w).finding is AdequacyFinding.UNRESOLVED
        for s in range(1, 30):
            b = rec.update(obs(s, p), w)
            expected = AdequacyFinding.UNEXPLAINED if s >= unexplained_from else AdequacyFinding.ADEQUATE
            assert b.finding is expected, (alpha, s)
            assert math.isclose(b.tails[repr(item("item_3"))],
                                likelihood_functions.tail_probability(SPEED * s, BETA))
            assert b.confidence == 1.0                # time enters adequacy only (E3)


def test_a_walk_straight_away_is_charged_twice_its_length(model):
    # E5: 167 cm walked straight away from the target is v·D = 334 cm: 170 cm unexplained, 160 cm not.
    w = build_world_state(model)
    x0, y0 = w.agent_positions[H]
    gx, gy = w.object_positions["item_3"]
    d = math.hypot(x0 - gx, y0 - gy)
    ux, uy = (x0 - gx) / d, (y0 - gy) / d
    rec = recognizer(model, [item("item_3")])
    rec.update(obs(0, (x0, y0)), w)
    for k in range(1, 18):
        b = rec.update(obs(k, (x0 + 10.0 * k * ux, y0 + 10.0 * k * uy)), w)
        assert b.finding is (AdequacyFinding.UNEXPLAINED if k == 17 else AdequacyFinding.ADEQUATE), k


def test_d_is_non_decreasing_within_a_phase(model):
    # E5: e and s only grow within a derived phase, so S never rises while the phase holds.
    w = build_world_state(model)
    x0, y0 = w.agent_positions[H]
    rec = recognizer(model, [item("item_3"), item("item_2")])
    path = [(x0, y0)]
    for k in range(1, 40):
        px, py = path[-1]
        if k % 5 == 0:
            path.append((px, py))                       # a stand
        elif (k // 7) % 2:
            path.append((px + 15.0, py))                # sideways
        else:
            path.append((px - 12.0, py - 9.0))          # toward the south-west
    last = {}
    for t, p in enumerate(path):
        b = rec.update(obs(t, p), w)
        for k, s in b.tails.items():
            assert s <= last.get(k, 1.0) + 1e-12
            last[k] = s


def test_the_finding_clears_at_a_phase_advance(model):
    w = build_world_state(model)
    p = w.agent_positions[H]
    rec = recognizer(model, [item("item_3")])
    for s in range(18):
        b = rec.update(obs(s, p), w)
    assert b.finding is AdequacyFinding.UNEXPLAINED
    # the agent is at the item: the derived phase advances to pick_up, the origin moves
    b = rec.update(obs(18, p), world_with(w, add=[pred("at", H, "item_3")]))
    assert b.finding is AdequacyFinding.UNRESOLVED and b.tails == {}


def test_the_finding_clears_at_a_boundary_then_exhausted(model):
    w = build_world_state(model)
    p = w.object_positions[TABLE]
    placing = world_with(w, add=[pred("holding", H, "item_3"), pred("at", H, TABLE)],
                         remove=[pred("obj_at", "item_3", "shelf_3")])
    rec = recognizer(model, [item("item_3"), item("item_2")])
    for s in range(19):
        b = rec.update(obs(s, p), placing)
    # both hypotheses stood 18 ticks in their phase: every member below alpha
    assert b.finding is AdequacyFinding.UNEXPLAINED
    assert set(b.tails) == {repr(item("item_3")), repr(item("item_2"))}
    # the release: item_3's terminal completion, expected on the previous tick: a boundary
    placed = world_with(placing, add=[pred("obj_at", "item_3", TABLE)], remove=[pred("holding", H, "item_3")])
    b = rec.update(obs(19, p), placed)
    assert b.finding is AdequacyFinding.UNRESOLVED and b.tails == {}
    # a lone live hypothesis: 1.0 in the evidence over H; in the output, the rest of the
    # mass beside the one pinned (retired) key (the two-level reading of R6)
    assert b.most_likely == repr(item("item_2"))
    assert rec._evidence == {repr(item("item_2")): 1.0}
    assert math.isclose(b.confidence, 1.0 - BELIEF_FLOOR)
    check_r6(rec, b)
    # item_2 delivered too: no hypothesis is live
    done = world_with(placed, add=[pred("obj_at", "item_2", TABLE)], remove=[pred("obj_at", "item_2", "shelf_2")])
    b = rec.update(obs(20, p), done)
    assert b.lifecycle is RecognizerLifecycle.EXHAUSTED
    assert b.finding is None and b.tails == {}
    assert b.most_likely is None and b.confidence == 0.0
    assert b.distribution == {repr(item("item_3")): BELIEF_FLOOR, repr(item("item_2")): BELIEF_FLOOR}
    assert rec._evidence == {}


def test_an_undecomposable_hypothesis_is_a_non_member():
    # The human holds an object with no home container: deliver_with_return's derived
    # container has no value, so every deliver_item hypothesis is undecomposable
    # (DecompositionError, a fact about this world) and has no derived phase.
    m = model_for("env_layout_05", registered("env_layout_05", "scenario_s04_01"))
    w = world_with(build_world_state(m), add=[pred("holding", H, "stray_box")])
    x0, y0 = w.agent_positions[H]
    robot = next(iter(m.robots.values()))
    hyps = build_hypothesis_space(robot.recognizer.task_model, m._objects_by_type)
    ghost = next(h for h in hyps if h.schema is deliver_item)
    coffee = next(h for h in hyps if h.task_name == "coffee_break")
    rec = recognizer(m, [ghost, coffee])
    for t in range(5):
        b = rec.update(obs(t, (x0 - 10.0 * t, y0)), w)
    assert rec._expected[repr(ghost)] is None and rec._expected[repr(coffee)] is not None
    assert repr(ghost) not in b.tails and repr(coffee) in b.tails
    # alone, it never makes the finding anything but unresolved
    rec = recognizer(m, [ghost])
    for t in range(30):
        b = rec.update(obs(t, (x0 - 10.0 * t, y0)), w)
        assert b.finding is AdequacyFinding.UNRESOLVED and b.tails == {}
