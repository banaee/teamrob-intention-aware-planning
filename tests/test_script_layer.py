# tests/test_script_layer.py
"""
T-C2a: the human action script, scenario layer. List-level checks, no runs: expand()
with provenance, the seven shapes of the vocabulary, the landmark rejection, the work
order by provenance, and the loader's resolution of every registered scenario.
Run from the repo root:  PYTHONHASHSEED=0 python -m pytest tests/test_script_layer.py
"""

import sys
from pathlib import Path

import pytest

# The paths run_mesa.py sets: the repo root, and mesa_sim/ for the vendored Mesa.
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "mesa_sim"))

from shared.planner import AdaptivePlanner, DecompositionError
from shared.knowledge import Tree
from shared.types import (
    ActionStep, AgentConfig, MethodSchema, PersonalTask, ScenarioConfig, ScriptAction, TaskInstance, Var, Const,
    check_work_order,
)
from domains.script import expand, ground, resolve_script
from domains.kitting.registry import domain_config, register_kitting_domain
from domains.kitting.actions import move_to
from domains.kitting.tasks import deliver_item, coffee_break
from domains.kitting.script import MoveTo, PickUp, Place, Stay, interrupt, deviate, abandon
from mesa_sim.sim_model import SimModel
from mesa_sim.world_state_builder import build_world_state

H = "human_0"


def model_for(layout, scenario):
    lay = domain_config["layouts"][layout]
    return SimModel(scenario=lay["scenarios"][scenario], register_fn=register_kitting_domain,
                    task_model_schemas=domain_config["task_model"], env_layout_path=lay["path"])


def ctx(layout, scenario):
    m = model_for(layout, scenario)
    return m, AdaptivePlanner(knowledge=m.tree), build_world_state(m)


def deliver(item, table="kitting_table_0"):
    return TaskInstance(schema=deliver_item, bindings={Var("?item"): Const(item), Var("?kitting_table"): Const(table)})


def coffee():
    return TaskInstance(schema=coffee_break, bindings={Var("?coffee_machine"): Const("coffee_machine_0")})


def WaitAt(entity, duration):
    return ScriptAction.of("wait_at", {"?entity": entity, "?duration": duration})


@pytest.fixture(scope="module")
def l0():
    return ctx("env_layout0", "scenario_00")


# ---------------------------------------------------------------------------
# expand() and provenance
# ---------------------------------------------------------------------------

def test_expand_deliver_item(l0):
    m, planner, world = l0
    t = deliver("item_3")
    got = expand(t, planner, world, H)
    assert got == [MoveTo("item_3"), PickUp("item_3"), MoveTo("kitting_table_0"), Place("item_3", "kitting_table_0")]
    assert all(e.provenance is got[0].provenance for e in got)
    assert got[0].provenance.key == "deliver_item(?item=item_3,?kitting_table=kitting_table_0)"
    # grounding reproduces the planner's own grounded actions
    planned = planner.decompose(t, H, world)
    for e, g in zip(got, planned):
        ge = ground(e, H, m.tree)
        assert (ge.action_name, ge.bindings, ge.completion_predicate) == (g.action_name, g.bindings, g.completion_predicate)


def test_expand_determined_destination(l0):
    _, planner, world = l0
    t = TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3")})
    assert expand(t, planner, world, H)[-1] == Place("item_3", "kitting_table_0")


def test_expand_coffee_break():
    m, planner, world = ctx("env_layout1", "scenario_10")
    got = expand(coffee(), planner, world, H)
    assert got == [MoveTo("coffee_machine_0"), WaitAt("coffee_machine_0", "PT60S")]
    assert got[0].provenance.key == "coffee_break(?coffee_machine=coffee_machine_0)"
    assert str(ground(got[1], H, m.tree).completion_predicate) == "waited(human_0, coffee_machine_0)"


def test_expand_method(l0):
    _, planner, world = l0
    t = deliver("item_3")
    assert expand(t, planner, world, H, method="deliver_default") == expand(t, planner, world, H)
    with pytest.raises(DecompositionError):
        expand(t, planner, world, H, method="deliver_already_held")   # not holding at the start
    with pytest.raises(ValueError, match="no method"):
        expand(t, planner, world, H, method="no_such_method")


def test_hand_written_primitives_carry_no_provenance():
    assert MoveTo("corner_NE").provenance is None and not hasattr(Stay(), "provenance")


# ---------------------------------------------------------------------------
# the seven shapes
# ---------------------------------------------------------------------------

def test_shape_1_unedited(l0):
    _, planner, world = l0
    assert resolve_script([deliver("item_3")], planner, world, H) == expand(deliver("item_3"), planner, world, H)


def test_shape_2_interrupt_coffee_after_pickup():
    _, planner, world = ctx("env_layout1", "scenario_10")
    got = resolve_script(interrupt(deliver("item_2"), after="pick_up", with_=[coffee()]), planner, world, H)
    assert got == [MoveTo("item_2"), PickUp("item_2"),
                   MoveTo("coffee_machine_0"), WaitAt("coffee_machine_0", "PT60S"),
                   MoveTo("kitting_table_0"), Place("item_2", "kitting_table_0")]
    keys = [e.provenance.key.split("(")[0] for e in got]
    assert keys == ["deliver_item"] * 2 + ["coffee_break"] * 2 + ["deliver_item"] * 2


def test_shape_3_deviate_to_other_table():
    _, planner, world = ctx("env_layout8", "scenario_80")
    t = TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_1")})
    got = resolve_script(deviate(t, destination="kitting_table_1"), planner, world, H)
    assert got == [MoveTo("item_1"), PickUp("item_1"), MoveTo("kitting_table_1"), Place("item_1", "kitting_table_1")]
    assert {e.provenance.key for e in got} == {"deliver_item(?item=item_1)"}


def test_shape_4_abandon_after_pickup(l0):
    _, planner, world = l0
    got = resolve_script(abandon(deliver("item_3"), after="pick_up"), planner, world, H)
    assert got == [MoveTo("item_3"), PickUp("item_3")]


def test_shape_5_change_of_mind(l0):
    _, planner, world = l0
    got = resolve_script(abandon(deliver("item_3"), before="pick_up", then=[deliver("item_2")]), planner, world, H)
    assert got == [MoveTo("item_3"),
                   MoveTo("item_2"), PickUp("item_2"), MoveTo("kitting_table_0"), Place("item_2", "kitting_table_0")]


def test_shape_6_stay_at_table_after_delivery(l0):
    _, planner, world = l0
    got = resolve_script(interrupt(deliver("item_3"), after="place", with_=[Stay(30)]), planner, world, H)
    assert got == expand(deliver("item_3"), planner, world, H) + [Stay(30)]


def test_shape_7_abandon_to_landmark(l0):
    _, planner, world = l0
    got = resolve_script(abandon(deliver("item_3"), after=1, then=[MoveTo("corner_NE"), Stay()]), planner, world, H)
    assert got == [MoveTo("item_3"), PickUp("item_3"), MoveTo("corner_NE"), Stay()]


def test_anchor_errors(l0):
    _, planner, world = l0
    with pytest.raises(ValueError, match=r"anchor 'move_to': must occur exactly once, occurs at \[0, 2\]"):
        resolve_script(interrupt(deliver("item_3"), after="move_to", with_=[Stay(5)]), planner, world, H)
    with pytest.raises(ValueError, match="index out of range"):
        resolve_script(abandon(deliver("item_3"), after=4), planner, world, H)
    with pytest.raises(ValueError, match="exactly one of"):
        interrupt(deliver("item_3"), after=0, before=1)


# ---------------------------------------------------------------------------
# landmarks (R4)
# ---------------------------------------------------------------------------

def test_landmark_parameter_rejected():
    # T-H: only a HumanOnlyTask may type a parameter as a landmark (Tree's constructor).
    _place = Var("?place")
    bad = PersonalTask(name="go_to_corner", parameters=[_place], parameter_types={"?place": "landmark"},
                       methods=[MethodSchema("m", [_place], [], [ActionStep(move_to, {Var("?target"): _place})])])
    tree = register_kitting_domain()              # kitting as it is (go_to a HumanOnlyTask): accepted
    with pytest.raises(ValueError, match="only a HumanOnlyTask may type a parameter as a landmark"):
        Tree(tasks=tree.task_schemas() + [bad], actions=tree.get_all_actions(), microactions=tree.get_microactions())


def test_layout0_landmarks(l0):
    m, _, _ = l0
    assert sorted(m._objects_by_type["landmark"]) == ["corner_NE", "corner_NW", "corner_SE", "corner_SW", "door"]


# ---------------------------------------------------------------------------
# the work order (R5)
# ---------------------------------------------------------------------------

S00_ASSIGNED = [deliver("item_3"), deliver("item_2")]


def test_every_registered_scenario_loads():
    for layout, lay in domain_config["layouts"].items():
        for sid in lay["scenarios"]:
            m = model_for(layout, sid)
            for h in m.humans:
                assert all(isinstance(e, (ScriptAction, Stay)) for e in m.humans[h].script)


def test_work_order_accepts_abandoned_assigned_task(l0):
    _, planner, world = l0
    script = [*abandon(deliver("item_3"), after="pick_up", then=[MoveTo("door")]), deliver("item_2")]
    check_work_order(H, script, S00_ASSIGNED)
    check_work_order(H, resolve_script(script, planner, world, H), S00_ASSIGNED)
    AgentConfig(agent_id=H, agent_type="human", start_position=(0, 0),
                scheduled_tasks=script, assigned_tasks=S00_ASSIGNED)


def test_work_order_rejects_missing_and_repeated(l0):
    _, planner, world = l0
    with pytest.raises(ValueError, match=r"not scripted: \['deliver_item\(\?item=item_2"):
        AgentConfig(agent_id=H, agent_type="human", start_position=(0, 0),
                    scheduled_tasks=[deliver("item_3"), MoveTo("item_2")], assigned_tasks=S00_ASSIGNED)
    twice = [deliver("item_3"), *abandon(deliver("item_3"), after=0), deliver("item_2")]
    with pytest.raises(ValueError, match="more than once"):
        check_work_order(H, twice, S00_ASSIGNED)
    with pytest.raises(ValueError, match="more than once"):
        check_work_order(H, resolve_script(twice, planner, world, H), S00_ASSIGNED)


def test_loader_errors_name_the_scenario():
    lay = domain_config["layouts"]["env_layout0"]
    base = lay["scenarios"]["scenario_00"]

    def with_script(script):
        human = base.agents[0]
        cfg = AgentConfig(agent_id=human.agent_id, agent_type="human", start_position=human.start_position,
                          scheduled_tasks=script, assigned_tasks=human.assigned_tasks)
        return ScenarioConfig(id="scenario_test", name="t", description="t", agents=[cfg, base.agents[1]])

    with pytest.raises(ValueError, match=r"scenario 'scenario_test', agent 'human_0': anchor 'move_to'.*expansion \[0: move_to"):
        SimModel(scenario=with_script([*interrupt(deliver("item_3"), after="move_to", with_=[Stay(3)]), deliver("item_2")]),
                 register_fn=register_kitting_domain,
                 task_model_schemas=domain_config["task_model"], env_layout_path=lay["path"])
    with pytest.raises(ValueError, match="T-C2b"):   # compatibility path: primitives wait for C2b
        SimModel(scenario=with_script([*abandon(deliver("item_3"), after="pick_up"), deliver("item_2")]),
                 register_fn=register_kitting_domain,
                 task_model_schemas=domain_config["task_model"], env_layout_path=lay["path"])
    with pytest.raises(ValueError, match="not an object of this layout"):
        SimModel(scenario=with_script([deliver("item_3"), deliver("item_2"), MoveTo("window")]),
                 register_fn=register_kitting_domain,
                 task_model_schemas=domain_config["task_model"], env_layout_path=lay["path"])
