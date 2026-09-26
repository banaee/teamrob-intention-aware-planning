# tests/test_th3_scenarios.py
"""
T-H3: the scenarios on the T-H script. Every registered kitting scenario loads
(its script replayed at load by the stack machine); the list form is refused;
the kitting call forms build the same instances as the explicit form; go_to_and_stand
is one interruption (suspend, walk and stand, resume); a load error names the
scenario; the landmark rule; dock_loading imports.
Run from the repo root:  PYTHONHASHSEED=0 python -m pytest tests/test_th3_scenarios.py
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "mesa_sim"))

from shared.knowledge import Tree, TaskModel
from shared.types import (
    ActionStep, AgentConfig, Const, HumanOnlyTask, MethodSchema, PersonalTask, ScenarioConfig, Script, TaskInstance,
    Var, task_instance_key,
)
from world.record import Left, Outcome, Resumed, Started
from domains.kitting import tasks
from domains.kitting.actions import move_to, wait_at
from domains.kitting.registry import domain_config, register_kitting_domain
from domains.kitting.script import ac_activation, coffee_break, deliver_item, go_to, go_to_and_stand, stand
from mesa_sim.sim_model import SimModel

H = "human_0"


def model_for(layout, scenario):
    cfg = domain_config["scenarios"][scenario]
    return SimModel(scenario=cfg, register_fn=register_kitting_domain,
                    task_model_schemas=domain_config["task_model"],
                    layout_path=domain_config["layouts"][layout],
                    setup_path=domain_config["setups"][cfg.setup])


def test_every_registered_scenario_loads():
    for sid, scenario in domain_config["scenarios"].items():
        for agent in scenario.agents:
            assert isinstance(agent.scheduled_tasks, Script), (sid, agent.agent_id)
        for layout in scenario.reference_layouts:
            m = model_for(layout, sid)
            for human in m.humans.values():
                assert human.machine is not None, sid


def test_the_list_form_is_refused():
    with pytest.raises(TypeError, match="scheduled_tasks is a Script"):
        AgentConfig(agent_id=H, agent_type="human", start_position=(0, 0),
                    scheduled_tasks=[deliver_item("item_3")])


def test_call_forms_build_the_explicit_instances():
    explicit = [
        (deliver_item("item_3", table="kitting_table_0"),
         TaskInstance(tasks.deliver_item, {Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")})),
        (deliver_item("item_3"), TaskInstance(tasks.deliver_item, {Var("?item"): Const("item_3")})),
        (coffee_break("coffee_machine_0"),
         TaskInstance(tasks.coffee_break, {Var("?coffee_machine"): Const("coffee_machine_0")})),
        (ac_activation("ac_switch_1"), TaskInstance(tasks.ac_activation, {Var("?ac_switch"): Const("ac_switch_1")})),
        (go_to("door"), TaskInstance(tasks.go_to, {Var("?landmark"): Const("door")})),
        (stand("PT40S"), TaskInstance(tasks.stand_task, {Var("?duration"): Const("PT40S")})),
        (go_to_and_stand("corner_NE", "PT60S"),
         TaskInstance(tasks.go_to_and_stand, {Var("?landmark"): Const("corner_NE"), Var("?duration"): Const("PT60S")})),
    ]
    for call, instance in explicit:
        assert call.schema is instance.schema
        assert task_instance_key(call) == task_instance_key(instance)


def test_go_to_and_stand_is_human_only_and_kept_out_of_a_task_model():
    tree = register_kitting_domain()
    assert isinstance(tasks.go_to_and_stand, HumanOnlyTask) and tree.holds(tasks.go_to_and_stand)
    with pytest.raises(ValueError):
        TaskModel(tree, domain_config["task_model"] + [tasks.go_to_and_stand])


def test_go_to_and_stand_interrupts_and_the_delivery_resumes():
    # scenario_s01_04: deliver(item_3).at(pick_up, go_to_and_stand(corner_NE, PT60S)), then deliver(item_2)
    m = model_for("env_layout_01", "scenario_s01_04")
    for _ in range(200):
        m.step()
    record = m.humans[H].record
    delivery = "deliver_item(?item=item_3,?kitting_table=kitting_table_0)"
    pause = "go_to_and_stand(?duration=PT60S,?landmark=corner_NE)"
    seen = [(type(t).__name__, task_instance_key(t.task), getattr(t, "outcome", None))
            for t in record.transitions if isinstance(t, (Started, Left, Resumed))]
    assert seen[:5] == [
        ("Left", delivery, Outcome.SUSPENDED),
        ("Started", pause, None),
        ("Left", pause, Outcome.COMPLETED),
        ("Resumed", delivery, None),
        ("Left", delivery, Outcome.COMPLETED),
    ]


def test_loader_errors_name_the_scenario():
    base = domain_config["scenarios"]["scenario_s01_01"]
    human = base.agents[0]
    # a delivery has no wait_at: the anchor is absent from its expansion
    cfg = AgentConfig(agent_id=human.agent_id, agent_type="human", start_position=human.start_position,
                      scheduled_tasks=Script([deliver_item("item_3", table="kitting_table_0").at(wait_at, stand("PT4S"))]),
                      assigned_tasks=human.assigned_tasks)
    scenario = ScenarioConfig(id="scenario_test", description="t", agents=[cfg, base.agents[1]],
                              setup=base.setup, reference_layouts=base.reference_layouts)
    with pytest.raises(ValueError, match=r"scenario 'scenario_test', agent 'human_0': .*wait_at"):
        SimModel(scenario=scenario, register_fn=register_kitting_domain,
                 task_model_schemas=domain_config["task_model"],
                 layout_path=domain_config["layouts"]["env_layout_01"],
                 setup_path=domain_config["setups"][base.setup])


def test_landmark_parameter_rejected():
    # T-H: only a HumanOnlyTask may type a parameter as a landmark (Tree's constructor).
    _place = Var("?place")
    bad = PersonalTask(name="go_to_corner", parameters=[_place], parameter_types={"?place": "landmark"},
                       methods=[MethodSchema("m", [_place], [], [ActionStep(move_to, {Var("?target"): _place})])])
    tree = register_kitting_domain()              # kitting as it is (go_to, go_to_and_stand HumanOnlyTasks): accepted
    with pytest.raises(ValueError, match="only a HumanOnlyTask may type a parameter as a landmark"):
        Tree(tasks=tree.task_schemas() + [bad], actions=tree.get_all_actions(), microactions=tree.get_microactions())


def test_env_layout_01_landmarks():
    m = model_for("env_layout_01", "scenario_s01_01")
    assert sorted(m._objects_by_type["landmark"]) == ["corner_NE", "corner_NW", "corner_SE", "corner_SW", "door"]


def test_dock_loading_imports():
    from domains.dock_loading.registry import domain_config as dock_config
    for scenario in dock_config["scenarios"].values():
        for agent in scenario.agents:
            assert isinstance(agent.scheduled_tasks, Script)
