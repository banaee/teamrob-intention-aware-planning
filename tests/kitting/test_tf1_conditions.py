# tests/kitting/test_tf1_conditions.py
"""
T-F part 1, the conditions human-unaware and intention-unaware (design_decisions.md and design_records.md, "T-F part
1: the conditions human-unaware and intention-unaware", R3, R5 to R7, A to F): the two run options `human_aware` and
`intention_aware`, the override (an option that is off sets every option above it to off, named in one line), the
`[run]` header's effective values, the gate's refusal `none(intention_off)` for both its callers, `none(no_human)`
asked before the gate, and one short run per condition on scenario_s10_02 (the MPB's crossing, the human's script
independent of the robot and its objects separate from the robot's).
Run from the repo root:  PYTHONHASHSEED=0 python -m pytest tests/kitting/test_tf1_conditions.py
"""

import dataclasses
import logging

import pytest

# first: puts the repo root and mesa_sim/ on the path, as the other test modules do
from tests.kitting.test_p_build import EXECUTING, HUMAN, belief, model, perceived, planner, projector  # noqa: F401
from tests.kitting.test_td1_adequacy import H
from tests.kitting.test_th1_tree import registered
from mesa_sim.sim_model import SimModel
from domains.kitting.registry import domain_config, register_kitting_domain
from shared.meta_planner import GateOutcome, MetaPlanner
from shared.types import RecognitionChange, ScenarioConfig

SCENARIO = "scenario_s10_02"
TICKS = 70          # the robot's one delivery ends by tick 67 in every condition (the verification's runs)


def sim(scenario, human_aware=True, intention_aware=True, assignment=True, context=True, stop=False):
    return SimModel(scenario=scenario, register_fn=register_kitting_domain,
                    task_model_schemas=domain_config["task_model"],
                    layout_path=domain_config["layouts"]["env_layout_12"],
                    setup_path=domain_config["setups"][scenario.setup],
                    state_declarations=domain_config["states"],
                    timeline_declarations=domain_config["timeline_facts"],
                    declared_context=domain_config["context_knowledge"],
                    human_aware=human_aware, intention_aware=intention_aware, assignment_knowledge=assignment,
                    context_knowledge=context, separation_stop=stop)


# ---------------------------------------------------------------------------
# R5: the override, its line, the header
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("stated,effective,line", [
    ((True, True, True, True, False), (True, True, True, True, False), None),
    ((True, True, True, True, True), (True, True, True, True, True), None),
    ((False, True, True, True, True), (False, False, False, False, False),
     "[run_mesa] options human_aware=off sets off: intention_aware assignment_knowledge context_knowledge separation_stop"),
    ((False, False, True, False, False), (False, False, False, False, False),
     "[run_mesa] options human_aware=off sets off: assignment_knowledge"),
    ((True, False, True, True, True), (True, False, False, False, True),
     "[run_mesa] options intention_aware=off sets off: assignment_knowledge context_knowledge"),
    ((True, False, False, False, False), (True, False, False, False, False), None),
])
def test_an_option_off_sets_every_option_above_it_off_and_names_them(stated, effective, line, caplog):
    with caplog.at_level(logging.INFO):
        m = sim(registered("env_layout_12", SCENARIO), *stated)
    assert (m.human_aware, m.intention_aware, m.assignment_knowledge, m.context_knowledge,
            m.separation_stop) == effective
    options = [r.getMessage() for r in caplog.records if r.getMessage().startswith("[run_mesa] options")]
    assert options == ([] if line is None else [line])
    on = lambda b: "on" if b else "off"
    header = next(r.getMessage() for r in caplog.records if r.getMessage().startswith("[run] "))
    assert (f"separation_stop={on(effective[4])} human_aware={on(effective[0])} intention_aware={on(effective[1])} "
            f"assignment_knowledge={on(effective[2])} context_knowledge={on(effective[3])} ") in header


# ---------------------------------------------------------------------------
# R6, A: the gate refuses for both its callers; R7, E: no human before the gate
# ---------------------------------------------------------------------------

def unaware(model, projector, human_agent_id=H):
    base = next(iter(model.robots.values())).meta_planner
    return MetaPlanner(task_model=base._task_model, projector=projector, recognizer=base._recognizer,
                       min_separation=50.0, human_agent_id=human_agent_id, intention_aware=False)


def test_the_gate_refuses_a_clearing_belief_with_intention_off(model, projector):
    assert planner(model, projector)._clears_gate(belief(0.9)) is GateOutcome.CLEARS
    assert unaware(model, projector)._clears_gate(belief(0.9)) is GateOutcome.INTENTION_OFF


def test_recognition_changed_does_not_enter_with_intention_off(model, projector):
    world = perceived(model, HUMAN, (0.0, 0.0), standing=3)
    aware = planner(model, projector).evaluate_triggers(belief(0.9), world, EXECUTING)
    assert aware.reason == "recognition_changed" and aware.cause is RecognitionChange.ENTERED
    assert not unaware(model, projector).evaluate_triggers(belief(0.9), world, EXECUTING).fired


def test_admission_refuses_with_intention_off_and_rests_on_the_fallback(model, projector, caplog):
    mp = unaware(model, projector)
    world = perceived(model, HUMAN, (0.0, 0.0), standing=3)
    with caplog.at_level(logging.INFO):
        fb = mp.update_human_projection(belief(0.9), world)
    assert fb is not None and fb.entries[0].abstract_plan is None
    assert "projection=fallback refused=none(intention_off)" in caplog.text
    assert mp._projected_hypothesis is None and mp._fallback_expiry is not None
    later = dataclasses.replace(world, timestamp=mp._fallback_expiry)
    assert mp.evaluate_triggers(belief(0.9), later, EXECUTING).reason == "projection_expired"


@pytest.mark.parametrize("confidence", [0.5, 0.9])
def test_no_human_is_asked_before_the_gate(model, projector, confidence, caplog):
    base = next(iter(model.robots.values())).meta_planner
    mp = MetaPlanner(task_model=base._task_model, projector=projector, recognizer=base._recognizer,
                     min_separation=50.0, human_agent_id=None)
    with caplog.at_level(logging.INFO):
        assert mp.update_human_projection(belief(confidence), perceived(model, HUMAN, (0.0, 0.0))) is None
    assert "projection=none(no_human)" in caplog.text and mp._fallback_expiry is None


# ---------------------------------------------------------------------------
# One run per condition on scenario_s10_02
# ---------------------------------------------------------------------------

def run(m, ticks=TICKS):
    robot = next(iter(m.robots.values()))
    positions, beliefs = [], []
    for _ in range(ticks):
        m.step()
        positions.append(tuple(map(float, robot.pos)))
        beliefs.append(robot.belief)
    return positions, beliefs


def alone(scenario):
    """The robot-alone reference run's scenario (analysis/instruments/mpb/reference.py's)."""
    robots = [dataclasses.replace(a, observes=[]) for a in scenario.agents if a.agent_type == "robot"]
    return ScenarioConfig(id=scenario.id, description="reference", agents=robots, setup=scenario.setup,
                          reference_layouts=scenario.reference_layouts, timeline=scenario.timeline)


def lines(caplog, prefix):
    return [r.getMessage() for r in caplog.records if r.getMessage().startswith(prefix)]


def test_a_human_unaware_robot_moves_as_the_robot_alone(caplog):
    scenario = registered("env_layout_12", SCENARIO)
    reference, _ = run(sim(alone(scenario), context=False))
    caplog.clear()
    with caplog.at_level(logging.INFO):
        m = sim(scenario, human_aware=False)
        positions, beliefs = run(m)
    assert positions == reference
    assert all(b is None for b in beliefs) and lines(caplog, "[IR") == ["[IR-assignment] knowledge=off known=[]"]
    assert not lines(caplog, "[coverage]") and not lines(caplog, "[scenario-coverage]")
    assert {t.split("trigger=")[1] for t in lines(caplog, "[meta-trig]")} - {"none"} == {"no_current_task"}
    assert set(p.split("projection=")[1] for p in lines(caplog, "[meta-proj]")) == {"none(no_human)"}
    assert len(m.humans) == 1                                                        # the human is in the world


def test_an_intention_unaware_robot_rests_every_decision_on_the_fallback(caplog):
    with caplog.at_level(logging.INFO):
        m = sim(registered("env_layout_12", SCENARIO), intention_aware=False)
        _, beliefs = run(m)
    assert all(b is None for b in beliefs) and lines(caplog, "[IR") == ["[IR-assignment] knowledge=off known=[]"]
    assert not lines(caplog, "[coverage]") and not lines(caplog, "[scenario-coverage]")
    fired = {t.split("trigger=")[1] for t in lines(caplog, "[meta-trig]")} - {"none"}
    assert fired == {"no_current_task", "projection_expired"}
    projections = [p.split("projection=")[1] for p in lines(caplog, "[meta-proj]")]
    assert projections and all(p == "fallback refused=none(intention_off)" for p in projections)
