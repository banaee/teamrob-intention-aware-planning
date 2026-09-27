# tests/test_td15_build.py
"""
T-D R and E, cycle 1.5b: E8 (the advance tick), E9 (s_exp by the Projector's attribution),
E10 (standing in the belief, L(v·D)) and G1 (the guard on admission). Every expected value is
derived from the entry (design_decisions.md, "T-D R and E", "1.5 rulings") or, for s_exp, from the
Projector's own segments; none from a run. As in test_td1_adequacy.py the world is a layout's
initial world changed by hand: the phase is derived from the predicates, the movement from the
observed positions.
Run from the repo root:  PYTHONHASHSEED=0 python -m pytest tests/test_td15_build.py
"""

import dataclasses
import logging
import math

import pytest

# first: puts the repo root and mesa_sim/ on the path, as the other test modules do
from tests.test_td1_adequacy import (
    BETA, H, SPEED, TABLE, check_r6, item, obs, pred, recognizer, world_with,
)
from tests.test_th1_tree import model_for, registered
from shared import likelihood_functions
from shared.meta_planner import DEFAULT_THETA, GateOutcome
from shared.planner import AdaptivePlanner
from shared.projection import Projector
from shared.recognizer import build_hypothesis_space
from shared.types import AdequacyFinding, HypothesisAdequacy
from mesa_sim.executor import ACTION_COMPLETION_LATENCY
from mesa_sim.sim_agents import HUMAN_TASK_COMPLETION_LATENCY
from mesa_sim.world_state_builder import build_world_state


@pytest.fixture(scope="module")
def model():
    return model_for("env_layout_01", registered("env_layout_01", "scenario_s01_01"))


@pytest.fixture(scope="module")
def model5():
    return model_for("env_layout_05", registered("env_layout_05", "scenario_s04_01"))


def L(x):
    """The belief's likelihood shape, the logistic 2 / (1 + e^(βx))."""
    return likelihood_functions.logistic_of_excess(x, BETA)


def S(x):
    return likelihood_functions.tail_probability(x, BETA)


def coffee_key(m):
    robot = next(iter(m.robots.values()))
    return next(h for h in build_hypothesis_space(robot.recognizer.task_model, m._objects_by_type)
                if h.task_name == "coffee_break")


def gate(m):
    return next(iter(m.robots.values())).meta_planner


# ---------------------------------------------------------------------------
# A delivery of item_3 walked by hand: from 600 cm north of the item straight south to it,
# the arrival where at() holds (20 cm short, inside the 30 cm radius), the walk's latency tick,
# the grasp, the grasp's latency tick, then the carry straight toward the table. The body's
# sequence (analysis/td_stage1/REPORT.md, G: arrival, latency, grasp, latency, walk).
# ---------------------------------------------------------------------------

ARRIVAL = 29                          # 600 − 29·20 = 20 cm from item_3


def start_of(model):
    gx, gy = build_world_state(model).object_positions["item_3"]
    return (gx, gy + 600.0)


def delivery(model):
    w = build_world_state(model)
    start = start_of(model)
    at_item = world_with(w, add=[pred("at", H, "item_3")])
    held = world_with(at_item, add=[pred("holding", H, "item_3")], remove=[pred("obj_at", "item_3", "shelf_3")])
    carrying = world_with(held, remove=[pred("at", H, "item_3")])
    steps = [((start[0], start[1] - SPEED * k), w) for k in range(ARRIVAL)]
    arrival = (start[0], start[1] - SPEED * ARRIVAL)
    steps += [(arrival, at_item), (arrival, at_item), (arrival, held), (arrival, held)]
    tx, ty = w.object_positions[TABLE]
    d = math.hypot(tx - arrival[0], ty - arrival[1])
    ux, uy = (tx - arrival[0]) / d, (ty - arrival[1]) / d
    steps += [((arrival[0] + SPEED * ux * k, arrival[1] + SPEED * uy * k), carrying) for k in range(1, 4)]
    return steps


def foreseeable(m, name):
    robot = next(iter(m.robots.values()))
    return next(h for h in build_hypothesis_space(robot.recognizer.task_model, m._objects_by_type)
                if repr(h) == name)


GRASP = ARRIVAL + 2


def test_the_grasp_tick_is_a_member_with_s_one(model5):
    # E8 (the scenario_s02_01 247 pattern, env_layout_05): on the grasp the true hypothesis
    # advances into its carry walk with nothing walked; it stays a member with S = 1, and the
    # finding is adequate though the only other member is a refuted foreseeable rival
    # (ac_activation(ac_switch_0), whose walk the grasp does not change). Without E8 the rival
    # alone decides.
    rival = foreseeable(model5, "ac_activation(?ac_switch=ac_switch_0)")
    rec = recognizer(model5, [item("item_3"), rival])
    steps = delivery(model5)
    for t, (p, w) in enumerate(steps[:GRASP + 1]):
        b = rec.update(obs(t, p), w)
        check_r6(rec, b)
    k3, k2 = repr(item("item_3")), repr(rival)
    assert rec._expected[k3].action_name == "move_to"             # advanced into the carry walk
    assert b.tails[k3] == 1.0
    assert b.hypothesis_adequacy[k3] is HypothesisAdequacy.ADEQUATE
    assert b.tails[k2] < 0.05                                      # the rival refuted by the walk
    assert b.hypothesis_adequacy[k2] is HypothesisAdequacy.INADEQUATE
    assert b.finding is AdequacyFinding.ADEQUATE


def test_the_grasps_latency_tick_holds_no_observation_for_the_carry_walk(model5):
    # E9 with E6 (2): the tick after the grasp is the pick_up's latency, priced to the carry walk
    # (s = 1 = s_exp), and the walk has nothing walked: the true hypothesis is not a member.
    # The finding is then the refuted rival's alone: unexplained. The first carry tick makes the
    # true hypothesis a member again at D = 0 (a straight walk, no standing beyond s_exp).
    rival = foreseeable(model5, "ac_activation(?ac_switch=ac_switch_0)")
    rec = recognizer(model5, [item("item_3"), rival])
    k3 = repr(item("item_3"))
    steps = delivery(model5)
    for t, (p, w) in enumerate(steps):
        b = rec.update(obs(t, p), w)
        if t == GRASP + 1:
            assert b.hypothesis_adequacy[k3] is HypothesisAdequacy.NO_OBSERVATION and k3 not in b.tails
            assert b.finding is AdequacyFinding.UNEXPLAINED
        if t == GRASP + 2:
            assert b.tails[k3] == 1.0 and b.finding is AdequacyFinding.ADEQUATE


def test_s_exp_is_the_projectors_attribution(model):
    # E9: s_exp for a phase is the Projector's priced stationary ticks within its span. Derived
    # here from the Projector's own segments for the same task, with the body's values: per
    # action its own segment then a latency segment; a phase opened by the previous action's
    # completion receives that latency. Expected: 0, 2, 1, 2 (move_to, pick_up, move_to, place).
    robot = next(iter(model.robots.values()))
    tm = robot.recognizer.task_model
    projector = Projector(task_model=tm, assumed_speed=SPEED, default_action_cost=1.0,
                          action_completion_latency=ACTION_COMPLETION_LATENCY,
                          observed_task_completion_latency=HUMAN_TASK_COMPLETION_LATENCY)
    w = world_with(build_world_state(model), remove=[pred("at", H, "item_3")])
    w = dataclasses.replace(w, agent_positions={**w.agent_positions, H: start_of(model)})
    plan = AdaptivePlanner(knowledge=tm).plan(task=item("item_3").task_instance(), agent_id=H,
                                              belief=None, world=w)
    segments = projector.build_segments(plan, w, H)
    assert len(segments) == 2 * len(plan.actions)
    own = [0.0 if a.schema.movement_target_key is not None else segments[2 * i].end_step - segments[2 * i].start_step
           for i, a in enumerate(plan.actions)]
    latency = [segments[2 * i + 1].end_step - segments[2 * i + 1].start_step for i in range(len(plan.actions))]
    derived = [own[0]] + [latency[i - 1] + own[i] for i in range(1, len(plan.actions))]
    assert [a.action_name for a in plan.actions] == ["move_to", "pick_up", "move_to", "place"]
    assert derived == [0.0, 2.0, 1.0, 2.0]
    after_boundary = latency[-1] + HUMAN_TASK_COMPLETION_LATENCY    # the first walk of the next episode
    assert after_boundary == 1.0

    # the recognizer's s_exp on the same walk, at each phase
    rec = recognizer(model, [item("item_3"), item("item_2")])
    k3 = repr(item("item_3"))
    seen = {}
    for t, (p, w) in enumerate(delivery(model)):
        rec.update(obs(t, p), w)
        a = rec._expected[k3]
        seen.setdefault((a.action_name, a.bindings.get(a.schema.movement_target_key)), rec._priced_standing(k3, a))
    assert list(seen.values()) == derived[:3]


def test_the_ticks_after_a_boundary_stay_unresolved_until_the_walk(model):
    # E9: after the release (the boundary), the place's latency tick is priced to the next walk
    # (s_exp = 1): unresolved on the boundary tick and on the latency tick, adequate from the
    # first walking tick (item_2's walk from the table, straight: D = 0, S = 1).
    w = build_world_state(model)
    p = w.object_positions[TABLE]
    placing = world_with(w, add=[pred("holding", H, "item_3"), pred("at", H, TABLE)],
                         remove=[pred("obj_at", "item_3", "shelf_3")])
    placed = world_with(placing, add=[pred("obj_at", "item_3", TABLE)], remove=[pred("holding", H, "item_3")])
    rec = recognizer(model, [item("item_3"), item("item_2")])
    k2 = repr(item("item_2"))
    rec.update(obs(0, p), placing)
    b = rec.update(obs(1, p), placed)                                  # the boundary
    assert b.finding is AdequacyFinding.UNRESOLVED
    assert rec._priced_standing(k2, rec._expected[k2]) == ACTION_COMPLETION_LATENCY + HUMAN_TASK_COMPLETION_LATENCY
    b = rec.update(obs(2, p), placed)                                  # the latency tick
    assert b.finding is AdequacyFinding.UNRESOLVED and b.tails == {}
    assert b.hypothesis_adequacy == {k2: HypothesisAdequacy.NO_OBSERVATION}
    gx, gy = w.object_positions["item_2"]
    d = math.hypot(gx - p[0], gy - p[1])
    q = (p[0] + SPEED * (gx - p[0]) / d, p[1] + SPEED * (gy - p[1]) / d)
    b = rec.update(obs(3, q), placed)                                  # the first walking tick
    assert b.finding is AdequacyFinding.ADEQUATE
    assert math.isclose(b.tails[k2], 1.0)
    check_r6(rec, b)


def test_standing_beyond_the_priced_duration_charges_the_belief_by_v_per_tick(model):
    # E10: item_3 in pick_up (the human at the item from the first observation: s_exp = its own
    # tick, 1), item_2 in its walk (s_exp = 0). Standing s ticks: item_2's evidence is L(v·s),
    # item_3's L(v·(s − 1)) past its priced duration; the ratio of the evidence is theirs.
    w = world_with(build_world_state(model), add=[pred("at", H, "item_3")])
    p = w.object_positions["item_3"]
    rec = recognizer(model, [item("item_3"), item("item_2")])
    k3, k2 = repr(item("item_3")), repr(item("item_2"))
    for s in range(0, 12):
        b = rec.update(obs(s, p), w)
        check_r6(rec, b)
        expected = L(SPEED * s) / (L(SPEED * max(s - 1, 0)) if s > 1 else 1.0)
        assert math.isclose(rec._evidence[k2] / rec._evidence[k3], expected, rel_tol=1e-12), s


def test_a_coffee_walk_tie_breaks_past_theta_after_nine_standing_ticks(model5):
    # E10: coffee_break at its machine (wait_at, within its priced 30 ticks: L = 1) against a walk
    # rival (s_exp = 0), even at 0.5. Standing s ticks the rival pays L(v·s); coffee's share is
    # 1 / (1 + L(v·s)) >= theta = 0.75 iff L <= 1/3 iff v·s >= ln 5 / beta = 160.9 cm: s >= 9.
    coffee = coffee_key(model5)
    machine = coffee.bindings["?coffee_machine"]
    w = world_with(build_world_state(model5), add=[pred("at", H, machine)])
    p = w.object_positions[machine]
    rival = item("item_3")
    rec = recognizer(model5, [coffee, rival])
    assert math.log(5.0) / BETA / SPEED > 8.0
    for s in range(0, 12):
        b = rec.update(obs(s, p), w)
        check_r6(rec, b)
        share = rec._evidence[repr(coffee)]
        assert math.isclose(share, 1.0 / (1.0 + L(SPEED * s)), rel_tol=1e-12)
        assert (share >= DEFAULT_THETA) == (s >= 9), s
        assert b.tails[repr(coffee)] == 1.0


# ---------------------------------------------------------------------------
# E10: walking-only evidence is 1.3b's
# ---------------------------------------------------------------------------

def test_walking_only_ticks_give_the_1_3b_belief(model):
    # On a walk with no standing (every live hypothesis in its first walk, s = 0 = s_exp), v·D is
    # the excess e and L(v·D) = L(e): the evidence is 1.3b's, normalise(prod_k L(e_k)), with e_k
    # measured from the first observation (the fixture's start), for every hypothesis of the
    # fixture's space (prior off). The walk: from the fixture human's start toward item_3, with a
    # detour, never standing, never within reach of a target.
    robot = next(iter(model.robots.values()))
    hyps = build_hypothesis_space(robot.recognizer.task_model, model._objects_by_type)
    w = build_world_state(model)
    o = w.agent_positions[H]
    rec = recognizer(model, hyps)
    keys = [repr(h) for h in rec._hypotheses]
    targets = {repr(h): w.object_positions[h.bindings["?item"]] for h in rec._hypotheses}
    path = [o]
    for k in range(1, 25):
        px, py = path[-1]
        path.append((px + 20.0, py) if 8 <= k < 12 else (px - 16.0, py - 12.0))
    walked = 0.0
    for t, p in enumerate(path):
        if t:
            walked += math.hypot(p[0] - path[t - 1][0], p[1] - path[t - 1][1])
        b = rec.update(obs(t, p), w)
        check_r6(rec, b)
        assert all(rec._expected[k].action_name == "move_to" for k in keys)
        u = {k: (1.0 if t == 0 else L(likelihood_functions.excess_path(
            walked, o, p, targets[k], likelihood_functions.straight_line_cost))) for k in keys}
        z = sum(u.values())
        for k in keys:
            assert math.isclose(rec._evidence[k], u[k] / z, rel_tol=1e-12), (t, k)


# ---------------------------------------------------------------------------
# G1: the guard on admission
# ---------------------------------------------------------------------------

def test_the_guard_refuses_a_lone_hypothesis_at_a_boundary(model):
    w = build_world_state(model)
    p = w.object_positions[TABLE]
    placing = world_with(w, add=[pred("holding", H, "item_3"), pred("at", H, TABLE)],
                         remove=[pred("obj_at", "item_3", "shelf_3")])
    placed = world_with(placing, add=[pred("obj_at", "item_3", TABLE)], remove=[pred("holding", H, "item_3")])
    rec = recognizer(model, [item("item_3"), item("item_2")])
    rec.update(obs(0, p), placing)
    b = rec.update(obs(1, p), placed)
    assert b.most_likely == repr(item("item_2")) and b.confidence >= DEFAULT_THETA
    assert b.hypothesis_adequacy[b.most_likely] is HypothesisAdequacy.NO_OBSERVATION
    assert gate(model)._clears_gate(b) is GateOutcome.LEADER_NO_OBSERVATION


def test_the_guard_refuses_an_inadequate_leader(model):
    # a lone hypothesis in its walk, the human standing: S < alpha from 17 ticks (v·D = 340 cm)
    w = build_world_state(model)
    p = w.agent_positions[H]
    rec = recognizer(model, [item("item_3")])
    for s in range(18):
        b = rec.update(obs(s, p), w)
        assert b.confidence >= DEFAULT_THETA
        expected = (GateOutcome.LEADER_NO_OBSERVATION if s == 0
                    else GateOutcome.LEADER_INADEQUATE if s >= 17 else GateOutcome.CLEARS)
        assert gate(model)._clears_gate(b) is expected, s


def test_the_guard_admits_the_coffee_leader_during_its_priced_stand(model5):
    coffee = coffee_key(model5)
    machine = coffee.bindings["?coffee_machine"]
    w = world_with(build_world_state(model5), add=[pred("at", H, machine)])
    p = w.object_positions[machine]
    rec = recognizer(model5, [coffee, item("item_3")])
    for s in range(10):
        b = rec.update(obs(s, p), w)
    assert b.most_likely == repr(coffee) and b.confidence >= DEFAULT_THETA
    assert b.hypothesis_adequacy[repr(coffee)] is HypothesisAdequacy.ADEQUATE
    assert gate(model5)._clears_gate(b) is GateOutcome.CLEARS


def test_the_guard_refusal_is_logged_and_clears_the_record(model, caplog):
    # admission refuses as below theta does: no projection, no decision record, the reason logged
    w = build_world_state(model)
    p = w.agent_positions[H]
    rec = recognizer(model, [item("item_3")])
    for s in range(18):
        b = rec.update(obs(s, p), w)
    mp = gate(model)
    with caplog.at_level(logging.INFO):
        assert mp.update_human_projection(b, w) is None
    assert "projection=none(leader_inadequate)" in caplog.text
    assert mp._projected_hypothesis is None
