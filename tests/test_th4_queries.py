# tests/test_th4_queries.py
"""
T-H4: the record's queries (world/queries.py) on the migrated scenarios, and
task equality (same_task). scenario_s01_03 abandon, scenario_s02_02
interruption and resumption, scenario_s06_06 / scenario_s07_03 binding level,
scenario_s05_01 the empty stack, scenario_s01_05 human-only tasks; a task model
without coffee_break; the [coverage] line the same with the prior on and off.
The queries run on the in-memory Record of an in-process run.
Run from the repo root:  PYTHONHASHSEED=0 python -m pytest tests/test_th4_queries.py
"""

import logging
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "mesa_sim"))

from shared.knowledge import TaskModel
from shared.recognizer import build_hypothesis_space
from shared.types import (
    AfterAction, AgentConfig, Const, Departure, Var, check_task_destinations, destination_departures, same_task,
)
from world.queries import (
    Assignment, BindingAbsent, Coverage, Covered, ObservingRobot, TaskAbsent, assigned, coverage, resumptions,
    switches, truth_at, unperformed,
)
from world.record import Boundary, Left, Outcome
from domains.kitting import tasks
from domains.kitting.actions import pick_up
from domains.kitting.registry import domain_config, register_kitting_domain
from domains.kitting.script import coffee_break, deliver_item, go_to, stand
from mesa_sim.sim_model import SimModel

H, R = "human_0", "robot_0"


def model_for(layout, sid, prior=False):
    cfg = domain_config["scenarios"][sid]
    return SimModel(scenario=cfg, register_fn=register_kitting_domain,
                    task_model_schemas=domain_config["task_model"],
                    layout_path=domain_config["layouts"][layout],
                    setup_path=domain_config["setups"][cfg.setup],
                    assignment_prior=prior)


def human_cfg(layout, sid):
    return next(a for a in domain_config["scenarios"][sid].agents if a.agent_id == H)


def run_script(m, max_steps=600):
    """Step until the human's script is finished; its record."""
    h = m.humans[H]
    for _ in range(max_steps):
        m.step()
        if not h.machine.stack and h.machine.next_entry >= len(h.machine.entries):
            return h.record
    pytest.fail("the script did not finish")


def script_tasks(cfg):
    return [e.task for e in cfg.scheduled_tasks.entries]


# ---------------------------------------------------------------------------
# the migrated scenarios
# ---------------------------------------------------------------------------

def test_s02_abandon():
    m = model_for("env_layout_01", "scenario_s01_03")
    record = run_script(m)
    cfg = human_cfg("env_layout_01", "scenario_s01_03")
    item_3, item_2 = script_tasks(cfg)
    assert any(isinstance(t, Left) and t.task is item_3 and t.outcome is Outcome.ABANDONED for t in record.transitions)
    assert switches(record) == [] and resumptions(record) == []
    destinations = m.observing[R].destinations
    assert unperformed(record, cfg.assigned_tasks, destinations) == [cfg.assigned_tasks[0]]
    assert assigned(item_3, cfg.assigned_tasks, destinations) == Assignment(cfg.assigned_tasks[0], ())
    assert all(isinstance(coverage(t, m.observing[R]), Covered) for t in (item_3, item_2))


def test_s11_interruption_and_resumption():
    m = model_for("env_layout_02", "scenario_s02_02")
    record = run_script(m)
    cfg = human_cfg("env_layout_02", "scenario_s02_02")
    delivery = cfg.scheduled_tasks.entries[0].task
    brk = cfg.scheduled_tasks.entries[0].events[0].decision.task
    [started] = switches(record)
    assert started.task is brk and started.trigger == AfterAction(pick_up)
    assert isinstance(started.where, Boundary) and started.where.action.schema is pick_up and started.where.occurrence == 0
    [resumed] = resumptions(record)
    assert resumed.task is delivery
    during = truth_at(record, started.tick)
    assert during.stack[0] is brk and during.stack[1] is delivery
    destinations = m.observing[R].destinations
    assert assigned(brk, cfg.assigned_tasks, destinations) is None
    cov = coverage(brk, m.observing[R])
    assert isinstance(cov, Covered) and cov.hypothesis.schema is tasks.coffee_break
    assert unperformed(record, cfg.assigned_tasks, destinations) == []


@pytest.mark.parametrize("layout,sid,item", [("env_layout_08", "scenario_s06_06", "item_0"),
                                              ("env_layout_09", "scenario_s07_03", "item_2")])
def test_binding_level_deviation(layout, sid, item):
    m = model_for(layout, sid)
    record = run_script(m)
    cfg = human_cfg(layout, sid)
    wrong, right = script_tasks(cfg)
    robot = m.observing[R]
    departure = Departure(Var("?kitting_table"), Const("kitting_table_0"), Const("kitting_table_1"))
    # the assigned task, and the binding the assignment did not give
    assert assigned(wrong, cfg.assigned_tasks, robot.destinations) == Assignment(cfg.assigned_tasks[0], (departure,))
    assert coverage(wrong, robot) == BindingAbsent(Var("?kitting_table"), Const("kitting_table_1"))
    assert assigned(right, cfg.assigned_tasks, robot.destinations) == Assignment(cfg.assigned_tasks[1], ())
    assert isinstance(coverage(right, robot), Covered)
    # delivered, to the wrong table: not performed
    assert any(isinstance(t, Left) and t.task is wrong and t.outcome is Outcome.COMPLETED for t in record.transitions)
    assert unperformed(record, cfg.assigned_tasks, robot.destinations) == [cfg.assigned_tasks[0]]
    assert cfg.assigned_tasks[0].bindings[Var("?item")] == Const(item)


def test_s70_empty_stack_after_the_script():
    m = model_for("env_layout_07", "scenario_s05_01")
    for _ in range(300):
        m.step()
    record = m.humans[H].record
    cfg = human_cfg("env_layout_07", "scenario_s05_01")
    ac = script_tasks(cfg)[-1]
    [done] = [t for t in record.transitions if isinstance(t, Left) and t.task is ac]
    assert done.outcome is Outcome.COMPLETED
    last = record.snapshots[-1].tick
    assert last == 299
    assert all(truth_at(record, t).stack == [] for t in range(done.tick + 1, last + 1))
    assert unperformed(record, cfg.assigned_tasks, m.observing[R].destinations) == []
    with pytest.raises(ValueError):
        truth_at(record, last + 1)


def test_task_absent():
    m = model_for("env_layout_01", "scenario_s01_05")
    robot = m.observing[R]
    door, st, corner, delivery = script_tasks(human_cfg("env_layout_01", "scenario_s01_05"))
    assert coverage(door, robot) == TaskAbsent(tasks.go_to)
    assert coverage(st, robot) == TaskAbsent(tasks.stand_task)
    assert isinstance(coverage(delivery, robot), Covered)
    # a PersonalTask omitted from the task model (env_layout_02 has the coffee machine)
    m = model_for("env_layout_02", "scenario_s02_02")
    robot = m.observing[R]
    schemas = [s for s in domain_config["task_model"] if s is not tasks.coffee_break]
    model = TaskModel(m.tree, schemas)
    without = ObservingRobot(model, frozenset(build_hypothesis_space(model, m._objects_by_type)), robot.destinations)
    assert coverage(coffee_break("coffee_machine_0"), without) == TaskAbsent(tasks.coffee_break)
    assert isinstance(coverage(coffee_break("coffee_machine_0"), robot), Covered)


def test_enumerated_binding_absent_carries_the_first_in_parameter_order():
    m = model_for("env_layout_08", "scenario_s06_06")
    robot = m.observing[R]
    narrowed = ObservingRobot(robot.task_model,
                              frozenset(h for h in robot.hypotheses if h.bindings.get("?item") != "item_0"),
                              robot.destinations)
    assert coverage(deliver_item("item_0", table="kitting_table_1"), narrowed) == \
        BindingAbsent(Var("?item"), Const("item_0"))


@pytest.mark.parametrize("layout,sid", [("env_layout_02", "scenario_s02_02"), ("env_layout_08", "scenario_s06_06")])
def test_coverage_line_is_the_same_with_the_prior_on_and_off(layout, sid, caplog):
    lines = {}
    for prior in (False, True):
        caplog.clear()
        with caplog.at_level(logging.INFO):
            model_for(layout, sid, prior)
        lines[prior] = [r.getMessage() for r in caplog.records if r.getMessage().startswith("[coverage]")]
    assert lines[False] and lines[False] == lines[True]
    assert len(lines[False]) == len(human_cfg(layout, sid).scheduled_tasks.entries)


# ---------------------------------------------------------------------------
# task equality
# ---------------------------------------------------------------------------

def test_same_task_is_the_goal():
    assert same_task(deliver_item("item_1"), deliver_item("item_1", table="kitting_table_0"))
    assert same_task(deliver_item("item_1", table="kitting_table_2"), deliver_item("item_1", table="kitting_table_0"))
    assert not same_task(deliver_item("item_1"), deliver_item("item_2"))
    assert same_task(stand("PT10S"), stand("PT50S"))          # a duration is not part of the goal
    assert not same_task(go_to("door"), go_to("corner_NE"))
    assert deliver_item("item_1") != deliver_item("item_1")   # == is object identity


def test_duplicate_assigned_tasks_by_same_task():
    with pytest.raises(ValueError, match="duplicate assigned tasks"):
        AgentConfig(agent_id="h", agent_type="human", start_position=(0, 0),
                    assigned_tasks=[deliver_item("item_1"), deliver_item("item_1", table="kitting_table_0")])
    AgentConfig(agent_id="h", agent_type="human", start_position=(0, 0),
                assigned_tasks=[deliver_item("item_1"), deliver_item("item_2")])


def test_departures_and_the_destination_check():
    station = {"item_0": "kitting_table_0"}
    assert destination_departures(deliver_item("item_0"), station) == ()
    assert destination_departures(deliver_item("item_0", table="kitting_table_0"), station) == ()
    assert destination_departures(deliver_item("item_0", table="kitting_table_1"), station) == \
        (Departure(Var("?kitting_table"), Const("kitting_table_0"), Const("kitting_table_1")),)
    with pytest.raises(ValueError, match=r"\?kitting_table is bound to 'kitting_table_1', but the layout designates "
                                         r"'kitting_table_0' for \?item='item_0'"):
        check_task_destinations(deliver_item("item_0", table="kitting_table_1"), station)


def test_coverage_is_not_constructed_directly():
    with pytest.raises(TypeError):
        Coverage()
