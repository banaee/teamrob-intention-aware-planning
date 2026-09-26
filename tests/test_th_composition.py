# tests/test_th_composition.py
"""
A scenario's composition and its scenario coverage (world/composition.py; T-H
follow-up), computed at load from the script and an observing robot: the
scenario coverage of scenario_s02_02, scenario_s01_03, scenario_s06_06,
scenario_s01_05, scenario_s01_04; scenario_s02_02 against a task model without
coffee_break; the exit-walk exemption; the four sets of scenario_s02_02; the
[scenario-coverage] line.
Run from the repo root:  PYTHONHASHSEED=0 python -m pytest tests/test_th_composition.py
"""

import logging
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "mesa_sim"))

from shared.knowledge import TaskModel
from shared.recognizer import build_hypothesis_space
from shared.types import AfterAction, PersonalTask, Script, Start, WorkTask, drop
from world.composition import Composition, ScenarioCoverage, scenario_composition
from world.queries import Covered, ObservingRobot, TaskAbsent
from domains.kitting import tasks
from domains.kitting.actions import move_to
from domains.kitting.registry import domain_config, register_kitting_domain
from domains.kitting.script import deliver_item, go_to, go_to_and_stand, stand
from mesa_sim.sim_model import SimModel

H, R = "human_0", "robot_0"


def model_for(layout, sid):
    cfg = domain_config["scenarios"][sid]
    return SimModel(scenario=cfg, register_fn=register_kitting_domain,
                    task_model_schemas=domain_config["task_model"],
                    layout_path=domain_config["layouts"][layout],
                    setup_path=domain_config["setups"][cfg.setup])


def script_of(layout, sid):
    return next(a for a in domain_config["scenarios"][sid].agents
                if a.agent_id == H).scheduled_tasks


@pytest.mark.parametrize("layout,sid,expected", [
    ("env_layout_02", "scenario_s02_02", ScenarioCoverage.MODELLED_ONLY),
    ("env_layout_01", "scenario_s01_03", ScenarioCoverage.MODELLED_ONLY),
    ("env_layout_08", "scenario_s06_06", ScenarioCoverage.BINDING_ABSENT),
    ("env_layout_01", "scenario_s01_05", ScenarioCoverage.TASK_ABSENT),
    ("env_layout_01", "scenario_s01_04", ScenarioCoverage.TASK_ABSENT),
])
def test_scenario_coverage(layout, sid, expected):
    _, scenario_coverage = scenario_composition(script_of(layout, sid), model_for(layout, sid).observing[R])
    assert scenario_coverage is expected


def test_a_task_model_without_coffee_break_moves_s11_to_task_absent():
    m = model_for("env_layout_02", "scenario_s02_02")
    model = TaskModel(m.tree, [s for s in domain_config["task_model"] if s is not tasks.coffee_break])
    without = ObservingRobot(model, frozenset(build_hypothesis_space(model, m._objects_by_type)),
                             m.observing[R].destinations)
    composition, scenario_coverage = scenario_composition(script_of("env_layout_02", "scenario_s02_02"), without)
    assert scenario_coverage is ScenarioCoverage.TASK_ABSENT
    assert composition.coverage == frozenset({Covered, TaskAbsent})


def test_the_exit_walk_is_not_counted():
    robot = model_for("env_layout_01", "scenario_s01_05").observing[R]
    composition, scenario_coverage = scenario_composition(Script([deliver_item("item_3"), go_to("door")]), robot)
    assert scenario_coverage is ScenarioCoverage.MODELLED_ONLY
    assert composition.coverage == frozenset({Covered, TaskAbsent})    # the composition still holds it
    # counted when it is not last, when it carries an event, for a terminal stand (no landmark), and for a
    # terminal go_to_and_stand (a walk to the landmark and a stand: not exactly one movement action)
    for script in (Script([go_to("door"), deliver_item("item_3")]),
                   Script([deliver_item("item_3"), go_to("door").at(move_to, drop)]),
                   Script([deliver_item("item_3"), stand("PT10S")]),
                   Script([deliver_item("item_3"), go_to_and_stand("door", "PT10S")])):
        assert scenario_composition(script, robot)[1] is ScenarioCoverage.TASK_ABSENT


def test_the_four_sets_of_s11():
    composition, _ = scenario_composition(script_of("env_layout_02", "scenario_s02_02"),
                                          model_for("env_layout_02", "scenario_s02_02").observing[R])
    assert composition == Composition(task_classes=frozenset({WorkTask, PersonalTask}),
                                      decisions=frozenset({Start}),
                                      triggers=frozenset({AfterAction}),
                                      coverage=frozenset({Covered}))


def test_the_scenario_coverage_line(caplog):
    with caplog.at_level(logging.INFO):
        model_for("env_layout_01", "scenario_s01_04")
    lines = [r.getMessage() for r in caplog.records if r.getMessage().startswith("[scenario-coverage]")]
    assert lines == ["[scenario-coverage] human_0 robot_0 scenario_coverage=task_absent tasks=WorkTask,HumanOnlyTask "
                     "decisions=Start triggers=AfterAction coverage=Covered,TaskAbsent"]
