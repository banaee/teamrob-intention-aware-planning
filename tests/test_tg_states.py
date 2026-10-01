# tests/test_tg_states.py
"""
T-G stage 1, step 4 (A5): object states and designations. The domain declares
its states, the setup states which hold at the start, the environment validates
and holds them and the builder emits them to every WorldState. An unknown state
and a state on a wrong type are refused; a declared state not listed does not
hold; the scan's state is applied when its TOUCH has run and seen from the next
tick, where its completion is acknowledged; a fact about no object loads and is
emitted; the gate's state is emitted and read by a method's guard; the
designation check refuses and accepts, on the setup's destinations and on an
assigned task's determined parameter.
Run from the repo root:  PYTHONHASHSEED=0 python -m pytest tests/test_tg_states.py
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "mesa_sim"))

from shared.knowledge import StateDeclaration, Tree
from shared.planner import AdaptivePlanner
from shared.types import (
    ActionStep, AgentConfig, Const, MethodSchema, Predicate, ScenarioConfig, Script, TaskInstance, Var, WorkTask,
)
from domains.dock_loading.actions import move_to, pick_up, place, scan_it, wait_at
from domains.dock_loading.registry import domain_config as dock, register_dock_loading_domain
from domains.dock_loading.tasks import confirm_delivered_pallet, deliver_pallet
from mesa_sim.sim_model import SimModel
from mesa_sim.world_state_builder import build_world_state

H, R = "human_0", "robot_0"
LAYOUT = "env_layout_02"


def is_(state, obj=None):
    return Predicate(state, (Const(obj),) if obj is not None else ())


def setup_file(tmp_path, base, states=None, destinations=None):
    """A copy of the registered setup `base` with its states block and some
    destinations replaced."""
    with open(dock["setups"][base]) as f:
        setup = json.load(f)
    if states is not None:
        setup["states"] = states
    for obj in setup["env_objects"]:
        if destinations and obj["id"] in destinations:
            obj["destination"] = destinations[obj["id"]]
    path = tmp_path / f"{base}_test.json"
    path.write_text(json.dumps(setup))
    return str(path)


def dock_model(setup="env_setup_03", setup_path=None, script=Script([]), robot_tasks=(), register_fn=None,
               task_model=None, states=None):
    agents = [AgentConfig(agent_id=H, agent_type="human", start_position=(0, 0), scheduled_tasks=script)]
    if robot_tasks is not None:
        agents.append(AgentConfig(agent_id=R, agent_type="robot", start_position=(0, -370), observes=[H],
                                  assigned_tasks=list(robot_tasks)))
    scenario = ScenarioConfig(id="scenario_test", description="t", agents=agents, setup=setup,
                              reference_layouts=[LAYOUT])
    return SimModel(scenario=scenario, register_fn=register_fn or register_dock_loading_domain,
                    task_model_schemas=task_model or dock["task_model"],
                    layout_path=dock["layouts"][LAYOUT], setup_path=setup_path or dock["setups"][setup],
                    state_declarations=dock["states"] if states is None else states)


# ---------------------------------------------------------------------------
# validation
# ---------------------------------------------------------------------------

def test_an_unknown_state_is_refused(tmp_path):
    path = setup_file(tmp_path, "env_setup_03", states=[{"state": "is_broken", "object": "pallet_0"}])
    with pytest.raises(ValueError, match="'is_broken' is not a state the domain declares"):
        dock_model(setup_path=path)


def test_a_state_on_a_wrong_type_is_refused(tmp_path):
    for entry, match in (({"state": "is_empty", "object": "dock_gate"}, "of type 'gate', but is declared for type 'pallet'"),
                         ({"state": "is_empty", "object": "pallet_9"}, "not an object of this run"),
                         ({"state": "is_empty"}, "names none")):
        with pytest.raises(ValueError, match=match):
            dock_model(setup_path=setup_file(tmp_path, "env_setup_03", states=[entry]))


def test_the_default_does_not_hold():
    world = build_world_state(dock_model())
    states = {p for p in world.predicates if p.name in ("is_empty", "is_scanned", "is_open")}
    assert states == {is_("is_empty", "pallet_4"), is_("is_empty", "pallet_5"), is_("is_open", "dock_gate")}


# ---------------------------------------------------------------------------
# the scan: applied when its TOUCH has run, seen and acknowledged on the next tick
# ---------------------------------------------------------------------------

def test_the_scan_timing():
    scan = TaskInstance(schema=confirm_delivered_pallet, bindings={Var("?pallet"): Const("pallet_0")})
    m = dock_model(setup="env_setup_02", script=Script([scan]), robot_tasks=None)
    executor = m.humans[H].executor
    scanned = is_("is_scanned", "pallet_0")
    for tick in range(1, 200):
        assert scanned not in build_world_state(m).predicates
        m.step()
        if executor.current_microaction == "touch":
            break
    else:
        pytest.fail("the human never touched")
    assert executor.current_action == "scan_it"
    assert scanned in m.state_facts                              # applied on the TOUCH's tick
    m.step()                                                     # the next tick: seen, and the action acknowledged
    assert scanned in build_world_state(m).predicates
    assert executor.current_microaction is None and executor.action_index == 1
    assert {p for p in m.state_facts if p.name == "is_scanned"} == {scanned}


# ---------------------------------------------------------------------------
# a fact about no object; the gate
# ---------------------------------------------------------------------------

def test_a_fact_about_no_object_loads_and_is_emitted(tmp_path):
    states = list(dock["states"]) + [StateDeclaration("shift_running", None)]
    path = setup_file(tmp_path, "env_setup_03", states=[{"state": "shift_running"}])
    m = dock_model(setup_path=path, states=states)
    assert is_("shift_running") in build_world_state(m).predicates
    m.step()
    assert is_("shift_running") in build_world_state(m).predicates
    with pytest.raises(ValueError, match="a fact about no object, but names 'dock_gate'"):
        dock_model(setup_path=setup_file(tmp_path, "env_setup_03",
                                         states=[{"state": "shift_running", "object": "dock_gate"}]), states=states)


def test_the_gates_state_is_emitted_and_read_by_a_guard(tmp_path):
    delivery = TaskInstance(schema=deliver_pallet, bindings={Var("?pallet"): Const("pallet_0"),
                                                             Var("?delivery_bay"): Const("dry_delivery_bay_0")})
    for setup in ("env_setup_02", "env_setup_03", "env_setup_04", "env_setup_05", "env_setup_06", "env_setup_07"):
        assert is_("is_open", "dock_gate") in build_world_state(dock_model(setup=setup)).predicates, setup
    m = dock_model()
    assert AdaptivePlanner(knowledge=m.tree).is_applicable(delivery, R, build_world_state(m))
    closed = dock_model(setup_path=setup_file(tmp_path, "env_setup_03", states=[]))
    assert is_("is_open", "dock_gate") not in build_world_state(closed).predicates
    assert not AdaptivePlanner(knowledge=closed.tree).is_applicable(delivery, R, build_world_state(closed))


# ---------------------------------------------------------------------------
# designations: the setup's destination types, an assigned task's determined parameter
# ---------------------------------------------------------------------------

_pallet, _bay, _truck, _target = Var("?pallet"), Var("?bay"), Var("?truck"), Var("?target")
bring = WorkTask(name="bring", parameters=[_pallet, _bay],
                 parameter_types={"?pallet": "pallet", "?bay": "delivery_bay"},
                 determined_parameters={"?bay": ("destination_of", "?pallet")},
                 methods=[MethodSchema("bring_default", [_pallet, _bay], [], [ActionStep(move_to, {_target: _bay})])])
send_back = WorkTask(name="send_back", parameters=[_pallet, _truck],
                     parameter_types={"?pallet": "pallet", "?truck": "truck"},
                     determined_parameters={"?truck": ("destination_of", "?pallet")},
                     methods=[MethodSchema("send_back_default", [_pallet, _truck], [],
                                           [ActionStep(move_to, {_target: _truck})])])


def designation_tree():
    return Tree(tasks=[bring, send_back], actions=[move_to, pick_up, place, wait_at, scan_it],
                microactions=["STEP", "GRASP", "RELEASE", "STAND", "TOUCH"])


def designated(tmp_path=None, destinations=None, robot_tasks=()):
    path = setup_file(tmp_path, "env_setup_03", destinations=destinations) if destinations else None
    return dock_model(setup_path=path, robot_tasks=robot_tasks, register_fn=designation_tree,
                      task_model=[bring, send_back])


def task(schema, pallet):
    return TaskInstance(schema=schema, bindings={Var("?pallet"): Const(pallet)})


def test_the_declared_destination_types():
    assert designation_tree().get_types_with_destination() == {"pallet": frozenset({"delivery_bay", "truck"})}


def test_the_setups_destination_must_have_a_declared_type(tmp_path):
    designated()                                                                     # bays and the truck: accepted
    with pytest.raises(ValueError, match="of type 'coffee_machine', but the domain declares for type 'pallet'"):
        designated(tmp_path, destinations={"pallet_0": "coffee_machine_0"})


def test_an_assigned_tasks_determined_parameter_must_have_its_type():
    designated(robot_tasks=[task(bring, "pallet_0"), task(send_back, "pallet_4")])   # accepted
    with pytest.raises(ValueError, match=r"\?bay resolves to 'truck_interior'.*requires type 'delivery_bay'"):
        designated(robot_tasks=[task(bring, "pallet_4")])                            # an empty pallet's delivery
    with pytest.raises(ValueError, match=r"\?truck resolves to 'dry_delivery_bay_0'.*requires type 'truck'"):
        designated(robot_tasks=[task(send_back, "pallet_0")])
