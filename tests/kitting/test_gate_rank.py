"""
The build of the two gate rulings (docs/handoffs/plan_T-K_gate.md; design_decisions.md, "T-K: context knowledge in the
recognizer's belief", R7's AM67, AM68, AM73, AM75, AM76). Every expectation is derived from the rulings, none from a run.

The recognizer's evidence rank (AM76), per live hypothesis: OUTRANKED when the evidence alone (the movement
likelihood of the present episode over the live hypotheses, without the prior) ranks another live hypothesis strictly
above it; NOT_OUTRANKED otherwise, a tie included. The comparison is exact, with no tolerance (AM75). Keys exactly H,
in hypothesis order; empty when exhausted.
"""
import dataclasses
import math

import pytest

# first: puts the repo root and mesa_sim/ on the path, as the other test modules do
from tests.kitting.test_td1_adequacy import H, SPEED, item, obs, recognizer
from tests.kitting.test_td15_build import start_of
from tests.kitting.test_th1_tree import model_for, registered
from shared.types import BeliefState, EvidenceRank
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
