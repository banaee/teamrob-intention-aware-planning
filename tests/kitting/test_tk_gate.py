# tests/kitting/test_tk_gate.py
"""
T-K part 1, AM42: the gate compares theta with the belief over the live hypotheses, not with the reported
distribution. `BeliefState.confidence` is the leader's belief over H (`BeliefState.belief`), before the floor and the
pin scaling; `distribution` keeps the floor and the pins (TODO-178). `MetaPlanner._clears_gate` reads `confidence` and
is unchanged. Every expected value is derived from the records, none from a run.
Run from the repo root:  PYTHONHASHSEED=0 python -m pytest tests/kitting/test_tk_gate.py
"""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "mesa_sim"))

from shared.meta_planner import GateOutcome
from shared.recognizer import BELIEF_FLOOR, build_hypothesis_space
from shared.types import (AdequacyFinding, BeliefState, HypothesisAdequacy, ObservationWarrant, RecognizerLifecycle)
from mesa_sim.world_state_builder import build_world_state
from tests.kitting.test_td1_adequacy import H, obs, recognizer
from tests.kitting.test_th1_tree import model_for, registered


@pytest.fixture(scope="module")
def model():
    return model_for("env_layout_01", registered("env_layout_01", "scenario_s01_01"))


def test_confidence_is_the_belief_over_h_before_the_floor_and_the_pins(model):
    # the support restriction pins the unassigned items' hypotheses: the reported distribution scales the live
    # mass by 1 - FLOOR * |pinned|, the belief over H does not
    w = build_world_state(model)
    human = next(a for a in registered("env_layout_01", "scenario_s01_01").agents if a.agent_type == "human")
    hyps = build_hypothesis_space(next(iter(model.robots.values())).recognizer.task_model, model._objects_by_type)
    rec = recognizer(model, hyps, assigned_tasks=human.assigned_tasks)
    pinned = len(rec._inadmissible)
    assert pinned > 0
    x, y = w.agent_positions[H]
    gx, gy = w.object_positions["item_3"]
    d = math.hypot(gx - x, gy - y)
    ux, uy = (gx - x) / d, (gy - y) / d
    b = None
    for t in range(25):                                  # a walk straight toward item_3
        b = rec.update(obs(t, (x + 20.0 * t * ux, y + 20.0 * t * uy)), w)
    assert set(b.belief) == set(rec._evidence)
    assert math.isclose(sum(b.belief.values()), 1.0, abs_tol=1e-12)
    ml = b.most_likely
    assert ml == max(b.belief, key=b.belief.get)
    assert b.confidence == b.belief[ml]
    # the reported leader value differs by the pin scaling (and by the floor where a live value is lifted)
    assert b.distribution[ml] < b.confidence
    assert b.distribution[ml] <= b.confidence * (1.0 - BELIEF_FLOOR * pinned) + 1e-12


def test_the_gate_clears_on_the_belief_over_h_with_pinned_keys(model):
    # a leader at exactly theta over H: with 5 pinned keys its reported value is 0.75 * 0.995 = 0.746 < theta.
    # The gate reads confidence (the belief over H) and clears (adequate, committed by the assigned tasks).
    robot = next(iter(model.robots.values()))
    mp = robot.meta_planner
    leader = next(k for k in (repr(h) for h in robot.recognizer._hypotheses) if "item_3" in k)
    belief = {leader: 0.75, "deliver_item(?item=item_2)": 0.25}
    distribution = {k: v * (1.0 - 5 * BELIEF_FLOOR) for k, v in belief.items()}
    distribution.update({f"deliver_item(?item=item_{i})": BELIEF_FLOOR for i in (4, 5, 6, 7, 8)})
    b = BeliefState(timestamp=0.0, agent_id=H, distribution=distribution, most_likely=leader, confidence=0.75,
                    finding=AdequacyFinding.ADEQUATE, lifecycle=RecognizerLifecycle.LIVE, tails={leader: 1.0},
                    hypothesis_adequacy={k: HypothesisAdequacy.ADEQUATE for k in belief},
                    observation_warrant={k: ObservationWarrant.OBSERVATION for k in belief},
                    episode_boundary=False, belief=belief)
    assert distribution[leader] < mp.theta <= b.confidence
    assert mp._clears_gate(b) is GateOutcome.CLEARS
    below = BeliefState(**{**b.__dict__, "confidence": distribution[leader]})
    assert mp._clears_gate(below) is GateOutcome.BELOW_THETA
