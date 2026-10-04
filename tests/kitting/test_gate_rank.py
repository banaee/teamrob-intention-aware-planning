"""
The build of the two gate rulings (docs/handoffs/plan_T-K_gate.md; design_decisions.md, "T-K: context knowledge in the
recognizer's belief", R7's AM67, AM68, AM73, AM75, AM76). Every expectation is derived from the rulings, none from a run.

The recognizer's evidence rank (AM76), per live hypothesis: OUTRANKED when the evidence alone (the movement
likelihood of the present episode over the live hypotheses, without the prior) ranks another live hypothesis strictly
above it; NOT_OUTRANKED otherwise, a tie included. The comparison is exact, with no tolerance (AM75). Keys exactly H,
in hypothesis order; empty when exhausted.
"""
import dataclasses
import logging
import math

import pytest

# first: puts the repo root and mesa_sim/ on the path, as the other test modules do
from tests.kitting.test_td1_adequacy import H, SPEED, item, obs, recognizer
from tests.kitting.test_td15_build import start_of
from tests.kitting.test_th1_tree import model_for, registered
from domains.kitting.tasks import deliver_item
from shared.meta_planner import DEFAULT_THETA, GateOutcome, MetaPlanner
from shared.types import (AdequacyFinding, BeliefState, Const, EvidenceRank, ExecutorState, HypothesisAdequacy,
                          ObservationWarrant, RecognizerLifecycle, TaskInstance, Var)
from mesa_sim.world_state_builder import build_world_state

OUT, NOT = EvidenceRank.OUTRANKED, EvidenceRank.NOT_OUTRANKED
ITEMS = ("item_2", "item_3", "item_4")


@pytest.fixture(scope="module")
def model():
    return model_for("env_layout_01", registered("env_layout_01", "scenario_s01_01"))


def walk_toward(model, rec, target, ticks):
    """A walk straight toward `target` from the human's start, one update per tick, the same world; the beliefs."""
    w = build_world_state(model)
    x, y = start_of(model)
    gx, gy = w.object_positions[target]
    d = math.hypot(gx - x, gy - y)
    ux, uy = (gx - x) / d, (gy - y) / d
    return [rec.update(obs(t, (x + SPEED * t * ux, y + SPEED * t * uy)), w) for t in range(ticks)]


# ---------------------------------------------------------------------------
# Stage 1: the recognizer's output (AM76)
# ---------------------------------------------------------------------------

def test_rank_keys_are_exactly_h_in_hypothesis_order(model):
    rec = recognizer(model, [item(i) for i in ITEMS])
    for b in walk_toward(model, rec, "item_3", 6):
        assert list(b.evidence_rank) == [repr(h) for h in rec._hypotheses if repr(h) in rec._evidence]
        assert set(b.evidence_rank) == set(b.belief)


def test_nothing_is_outranked_while_the_evidence_is_equal(model):
    # the first observation: nothing walked, the evidence equal over H (as on a boundary tick, where it restarts equal)
    rec = recognizer(model, [item(i) for i in ITEMS])
    b0 = walk_toward(model, rec, "item_3", 1)[0]
    assert len(set(rec._evidence.values())) == 1
    assert set(b0.evidence_rank.values()) == {NOT}


def test_a_walk_toward_one_target_outranks_the_others(model):
    rec = recognizer(model, [item(i) for i in ITEMS])
    b = walk_toward(model, rec, "item_3", 12)[-1]
    k3 = repr(item("item_3"))
    assert b.evidence_rank[k3] is NOT
    assert all(v is OUT for k, v in b.evidence_rank.items() if k != k3)


def test_the_comparison_is_exact(model):
    # AM75: one ulp below the top outranks; equal values do not
    rec = recognizer(model, [item(i) for i in ITEMS])
    walk_toward(model, rec, "item_3", 1)
    k2, k3, k4 = (repr(item(i)) for i in ITEMS)
    top = 0.4
    rec._evidence = {k2: top, k3: math.nextafter(top, 0.0), k4: 1.0 - top - math.nextafter(top, 0.0)}
    assert rec._evidence_rank() == {k2: NOT, k3: OUT, k4: OUT}
    rec._evidence = {k2: 0.4, k3: 0.4, k4: 0.2}
    assert rec._evidence_rank() == {k2: NOT, k3: NOT, k4: OUT}


def test_empty_when_no_hypothesis_is_live(model):
    rec = recognizer(model, [item(i) for i in ITEMS])
    walk_toward(model, rec, "item_3", 1)
    rec._evidence = {}
    assert rec._evidence_rank() == {}


def test_with_context_knowledge_off_the_leader_is_never_outranked(model):
    # the equal prior: the belief is the evidence, so its leader is the evidence's top (F7 of the plan)
    rec = recognizer(model, [item(i) for i in ITEMS])
    assert rec._context is None
    for target in ("item_2", "item_4"):
        rec = recognizer(model, [item(i) for i in ITEMS])
        for b in walk_toward(model, rec, target, 15):
            assert b.evidence_rank[b.most_likely] is NOT


def test_every_belief_states_the_rank():
    # a required field: no constructor leaves it out
    names = {f.name for f in dataclasses.fields(BeliefState) if f.default is dataclasses.MISSING
             and f.default_factory is dataclasses.MISSING}
    assert "evidence_rank" in names


# ---------------------------------------------------------------------------
# Stage 2: the gate refuses an outranked leader, asked last (AM68, D1)
# ---------------------------------------------------------------------------

A, I, N = HypothesisAdequacy.ADEQUATE, HypothesisAdequacy.INADEQUATE, HypothesisAdequacy.NO_OBSERVATION
WN, WO = ObservationWarrant.NONE, ObservationWarrant.OBSERVATION
I5, I2 = "deliver_item(?item=item_5)", "deliver_item(?item=item_2)"


def belief(adequacy, warrant, rank, confidence=0.9, leader=I5):
    rival = I2
    return BeliefState(timestamp=0.0, agent_id=H, distribution={leader: confidence, rival: 1.0 - confidence},
                       most_likely=leader, confidence=confidence, finding=AdequacyFinding.ADEQUATE,
                       lifecycle=RecognizerLifecycle.LIVE, tails={}, hypothesis_adequacy={leader: adequacy, rival: A},
                       observation_warrant={leader: warrant, rival: WO},
                       evidence_rank={leader: rank, rival: NOT if rank is OUT else OUT}, episode_boundary=False)


def planner(model):
    """A meta-planner on the model's robot's parts; the gate's subject is the belief alone."""
    robot = next(iter(model.robots.values()))
    return MetaPlanner(task_model=robot.meta_planner._task_model, projector=robot.projector,
                       recognizer=robot.recognizer, min_separation=50.0, human_agent_id=H)


def test_an_outranked_leader_is_refused(model):
    mp = planner(model)
    assert mp._clears_gate(belief(A, WO, OUT)) is GateOutcome.LEADER_OUTRANKED
    assert GateOutcome.LEADER_OUTRANKED.value == "none(leader_outranked)"


def test_a_leader_tied_for_the_top_clears(model):
    # a tie passes (AM75): NOT_OUTRANKED is the tie's value as well as the top's
    assert planner(model)._clears_gate(belief(A, WO, NOT)) is GateOutcome.CLEARS


def test_the_outranked_check_is_asked_last(model):
    # D1: every other refusal keeps its reason when the leader is also outranked
    mp = planner(model)
    assert mp._clears_gate(belief(A, WO, OUT, confidence=DEFAULT_THETA - 0.01)) is GateOutcome.BELOW_THETA
    assert mp._clears_gate(belief(I, WO, OUT)) is GateOutcome.LEADER_INADEQUATE
    assert mp._clears_gate(belief(N, WO, OUT)) is GateOutcome.LEADER_NO_OBSERVATION
    assert mp._clears_gate(belief(A, WN, OUT)) is GateOutcome.LEADER_UNWARRANTED


def test_the_refusal_is_logged_and_nothing_is_recorded(model, caplog):
    # the world as built carries no previous observation of the human, so no fallback: the reason alone
    mp = planner(model)
    with caplog.at_level(logging.INFO):
        assert mp.update_human_projection(belief(A, WO, OUT), build_world_state(model)) is None
    assert "projection=none(leader_outranked)" in caplog.text
    assert mp._projected_hypothesis is None


def test_the_entering_side_waits_while_the_leader_is_outranked(model):
    # no record: recognition_changed does not fire on an outranked leader; once it is not outranked, it does
    executing = ExecutorState(agent_id="robot_0", holding=None,
                              current_task=TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4")}))
    mp = planner(model)
    w = build_world_state(model)
    assert not mp.evaluate_triggers(belief(A, WO, OUT), w, executing).fired
    assert mp.evaluate_triggers(belief(A, WO, NOT), w, executing).fired


def test_an_admission_is_not_ended_by_the_rank(model):
    # AM68 is a condition of admission only (AM69): a recorded leader that becomes outranked fires nothing
    executing = ExecutorState(agent_id="robot_0", holding=None,
                              current_task=TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4")}))
    mp = planner(model)
    mp._projected_hypothesis = I5
    assert not mp.evaluate_triggers(belief(A, WO, OUT), build_world_state(model), executing).fired
