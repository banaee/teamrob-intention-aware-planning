# tests/test_th1_tree.py
"""
T-H1: the tree, the task model and the two knowledge objects. The schema classes,
the knowledge objects' construction checks, the typed steps (with a TaskStep's
recursion), the support restriction on HypothesisKey values, and the human-only
tasks go_to and stand run through the C1 script layer.
Run from the repo root:  PYTHONHASHSEED=0 python -m pytest tests/test_th1_tree.py
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "mesa_sim"))

from shared.knowledge import Tree, TaskModel, ProceduralKnowledge, ContextKnowledge
from shared.planner import AdaptivePlanner
from shared.recognizer import HypothesisKey, IntentionRecognizer, build_hypothesis_space
from shared.types import (
    ActionSchema, ActionStep, AgentConfig, ConditionSchema, MethodSchema, PersonalTask, ScenarioConfig,
    Script, Step, TaskInstance, TaskSchema, TaskStep, Var, Const, WorkTask,
)
from domains.kitting.actions import move_to
from domains.kitting.registry import domain_config, register_kitting_domain
from domains.kitting.tasks import deliver_item, coffee_break, ac_activation, go_to, stand_task
from mesa_sim.sim_model import SimModel
from mesa_sim.world_state_builder import build_world_state

H = "human_0"
_x = Var("?x")


def model_for(layout, scenario_cfg):
    return SimModel(scenario=scenario_cfg, register_fn=register_kitting_domain,
                    task_model_schemas=domain_config["task_model"],
                    env_layout_path=domain_config["layouts"][layout]["path"])


def registered(layout, sid):
    return domain_config["layouts"][layout]["scenarios"][sid]


def with_human_script(base, script):
    human = next(a for a in base.agents if a.agent_type == "human")
    cfg = AgentConfig(agent_id=human.agent_id, agent_type="human", start_position=human.start_position,
                      scheduled_tasks=Script(script), assigned_tasks=[])
    return ScenarioConfig(id="scenario_test", name="t", description="t",
                          agents=[cfg] + [a for a in base.agents if a is not human])


# ---------------------------------------------------------------------------
# the schema classes and the steps
# ---------------------------------------------------------------------------

def test_base_classes_are_not_constructed():
    with pytest.raises(TypeError, match="WorkTask, a PersonalTask or a HumanOnlyTask"):
        TaskSchema(name="t", parameters=[], methods=[])
    with pytest.raises(TypeError, match="ActionStep or a TaskStep"):
        Step()
    with pytest.raises(TypeError, match="Tree or a TaskModel"):
        ProceduralKnowledge([], [], [])


def test_kitting_tree_classes():
    tree = register_kitting_domain()
    assert [type(t).__name__ for t in tree.task_schemas()] == \
        ["WorkTask", "PersonalTask", "PersonalTask", "HumanOnlyTask", "HumanOnlyTask", "HumanOnlyTask"]


def test_step_outside_the_tree_is_rejected():
    stray = ActionSchema(name="move_to", parameters=[], preconditions=[], effects=[],
                         completion=ConditionSchema("at", (Var("?agent"), Var("?target"))), microactions="STEP*")
    task = PersonalTask(name="t", parameters=[], methods=[MethodSchema("m", [], [], [ActionStep(stray, {})])])
    tree = register_kitting_domain()
    with pytest.raises(ValueError, match="not an action schema of this knowledge"):
        Tree(tasks=tree.task_schemas() + [task], actions=tree.get_all_actions(), microactions=[])


def test_task_step_recurses():
    # A compound task whose one step is the delivery: the same flat action list.
    wrap = WorkTask(name="wrap", parameters=[Var("?item")], parameter_types={"?item": "item"},
                    methods=[MethodSchema("m", [Var("?item")], [], [TaskStep(deliver_item, {Var("?item"): Var("?item")})])])
    kit = register_kitting_domain()
    tree = Tree(tasks=kit.task_schemas() + [wrap], actions=kit.get_all_actions(), microactions=kit.get_microactions())
    m = model_for("env_layout0", registered("env_layout0", "scenario_00"))
    world = build_world_state(m)
    planner = AdaptivePlanner(knowledge=tree)
    item = {Var("?item"): Const("item_3")}
    got = planner.decompose(TaskInstance(schema=wrap, bindings=item), H, world)
    want = planner.decompose(TaskInstance(schema=deliver_item, bindings=dict(item)), H, world)
    assert [(a.action_name, a.bindings) for a in got] == [(a.action_name, a.bindings) for a in want]
    # a sub-task outside the model: the TaskModel is refused
    solo = WorkTask(name="solo", parameters=[], methods=[MethodSchema("m", [], [], [TaskStep(coffee_break, {})])])
    tree2 = Tree(tasks=[deliver_item, coffee_break, solo], actions=kit.get_all_actions(), microactions=[])
    with pytest.raises(ValueError, match="not a task schema of this knowledge"):
        TaskModel(tree2, [deliver_item, solo])


# ---------------------------------------------------------------------------
# the task model
# ---------------------------------------------------------------------------

def test_task_model_construction():
    tree = register_kitting_domain()
    TaskModel(tree, [deliver_item])                                   # a PersonalTask may be omitted
    with pytest.raises(ValueError, match="every WorkTask of the tree is in it; missing: \\['deliver_item'\\]"):
        TaskModel(tree, [coffee_break])
    with pytest.raises(ValueError, match="'go_to' is a HumanOnlyTask"):
        TaskModel(tree, [deliver_item, go_to])
    with pytest.raises(ValueError, match="'stand' is a HumanOnlyTask"):
        TaskModel(tree, [deliver_item, stand_task])
    copy = WorkTask(name="deliver_item", parameters=deliver_item.parameters, methods=deliver_item.methods)
    with pytest.raises(ValueError, match="not a task schema of the tree"):
        TaskModel(tree, [copy])


def test_assigned_personal_task_is_rejected():
    t = TaskInstance(schema=coffee_break, bindings={Var("?coffee_machine"): Const("coffee_machine_0")})
    with pytest.raises(ValueError, match="an assigned task is a WorkTask instance"):
        AgentConfig(agent_id="robot_0", agent_type="robot", start_position=(0, 0), assigned_tasks=[t])


def test_hypothesis_space_from_the_task_model():
    m = model_for("env_layout1", registered("env_layout1", "scenario_10"))
    robot = next(iter(m.robots.values()))
    hyps = set(build_hypothesis_space(robot.recognizer.task_model, m._objects_by_type))
    by_type = m._objects_by_type
    want = ({HypothesisKey(deliver_item, {"?item": i}) for i in by_type["item"]}
            | {HypothesisKey(coffee_break, {"?coffee_machine": c}) for c in by_type["coffee_machine"]}
            | {HypothesisKey(ac_activation, {"?ac_switch": a}) for a in by_type["ac_switch"]})
    assert hyps == want


def test_support_restriction_on_hypothesis_keys():
    m = model_for("env_layout4", registered("env_layout4", "scenario_40"))
    robot = next(iter(m.robots.values()))
    human = next(a for a in registered("env_layout4", "scenario_40").agents if a.agent_type == "human")
    rec = IntentionRecognizer(task_model=robot.recognizer.task_model, context=ContextKnowledge.default(),
                              hypotheses=build_hypothesis_space(robot.recognizer.task_model, m._objects_by_type),
                              beta=0.01, assigned_tasks=human.assigned_tasks)
    assigned = {HypothesisKey(deliver_item, {"?item": t.bindings[Var("?item")].value}) for t in human.assigned_tasks}
    personal = {h for h in rec._hypotheses if h.schema is coffee_break or h.schema is ac_activation}
    assert rec._admissible == assigned | personal
    # a model that omits ac_activation: its hypotheses do not exist, so none is admissible
    small = TaskModel(m.tree, [deliver_item, coffee_break])
    rec2 = IntentionRecognizer(task_model=small, context=ContextKnowledge.default(),
                               hypotheses=build_hypothesis_space(small, m._objects_by_type),
                               beta=0.01, assigned_tasks=human.assigned_tasks)
    assert {h.task_name for h in rec2._admissible} == {"deliver_item", "coffee_break"}


def test_planner_is_bound_to_its_knowledge_by_identity():
    m = model_for("env_layout0", registered("env_layout0", "scenario_00"))
    world = build_world_state(m)
    robot = next(iter(m.robots.values()))
    walk = TaskInstance(schema=go_to, bindings={Var("?landmark"): Const("door")})
    AdaptivePlanner(knowledge=m.tree).decompose(walk, H, world)              # the tree holds go_to
    with pytest.raises(ValueError, match="'go_to' is not a task schema of this planner's knowledge"):
        robot.planner.decompose(walk, "robot_0", world)                      # the task model does not
    copy = WorkTask(name="deliver_item", parameters=deliver_item.parameters, methods=deliver_item.methods,
                    parameter_types=deliver_item.parameter_types,
                    determined_parameters=deliver_item.determined_parameters)
    with pytest.raises(ValueError, match="not a task schema of this planner's knowledge"):
        robot.planner.decompose(TaskInstance(schema=copy, bindings={Var("?item"): Const("item_3")}), "robot_0", world)


# ---------------------------------------------------------------------------
# go_to and stand through the human's script
# ---------------------------------------------------------------------------

def stand(duration):
    return TaskInstance(schema=stand_task, bindings={Var("?duration"): Const(duration)})


def goto(landmark):
    return TaskInstance(schema=go_to, bindings={Var("?landmark"): Const(landmark)})


def test_stand_and_go_to_run():
    base = registered("env_layout0", "scenario_00")
    m = model_for("env_layout0", with_human_script(base, [stand("PT10S"), goto("door")]))
    human = m.humans[H]
    assert [repr(e) for e in human.machine.entries] == ["stand(?duration=PT10S)", "go_to(?landmark=door)"]
    start = human.pos
    stood = 0
    for _ in range(200):
        m.step()
        world = build_world_state(m)
        assert not any(p.name == "waited" and p.args[0].value == H for p in world.predicates)
        if human.pos == start:
            stood += 1
        if any(p.name == "at" and p.args == (Const(H), Const("door")) for p in world.predicates):
            break
    else:
        pytest.fail("the human never reached the door")
    assert stood >= 5                         # PT10S at 2 s per step


def test_bad_duration_is_a_load_error():
    base = registered("env_layout0", "scenario_00")
    with pytest.raises(ValueError, match="scenario 'scenario_test', agent 'human_0': stand\\(\\?duration=soon\\).*not a duration"):
        model_for("env_layout0", with_human_script(base, [stand("soon")]))
    with pytest.raises(ValueError, match="not an object of this layout"):
        model_for("env_layout0", with_human_script(base, [goto("window")]))
