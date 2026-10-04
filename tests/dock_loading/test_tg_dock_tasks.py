# tests/dock_loading/test_tg_dock_tasks.py
"""
T-G stage 1, step 7: dock_loading's tasks (docs/handoffs/plan_T-G_stage1.md,
section 4). Every robot method is selected from each of its areas and
held-object cases, with the route of the plan's tables; the scan is applicable
only once the pallet stands in its bay; load_return is not applicable to a full
pallet; the routes cross the gate exactly when the areas differ; the human's
tasks from the hall and the office; an agent outside its areas has no
applicable method.
Run from the repo root:  PYTHONHASHSEED=0 python -m pytest tests/dock_loading/test_tg_dock_tasks.py
"""

import sys
from dataclasses import replace
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "mesa_sim"))

from shared.planner import AdaptivePlanner, DecompositionError
from shared.types import AREA_FACT, AgentConfig, Const, Predicate, ScenarioConfig, Script, area_at, area_fact
from domains.dock_loading.registry import domain_config as dock, register_dock_loading_domain
from domains.dock_loading import tasks
from domains.dock_loading.script import (confirm_delivered_pallet, coffee_break, deliver_pallet, go_to,
                                         go_to_and_stand, load_return, office_break, stand)
from mesa_sim.sim_model import SimModel
from mesa_sim.world_state_builder import build_world_state

H, R = "human_0", "robot_0"
LAYOUT = "env_layout_02"
GATE, DOOR, TRUCK = "dock_gate", "office_door", "truck_interior"
DRY, EMPTIES = "dry_delivery_bay_0", "empty_pallet_bay_0"
# A point inside each area of env_layout_02.
POSITIONS = {"area_truck_side": (0, -370), "area_hall": (0, 0), "area_office": (0, 360)}


def dock_model(setup="env_setup_03", robot_tasks=None, script=Script([])):
    agents = [AgentConfig(agent_id=H, agent_type="human", start_position=(0, 0), scheduled_tasks=script),
              AgentConfig(agent_id=R, agent_type="robot", start_position=(0, -370), observes=[H],
                          assigned_tasks=list(robot_tasks or []))]
    scenario = ScenarioConfig(id="scenario_test", description="t", agents=agents, setup=setup,
                              reference_layouts=[LAYOUT])
    return SimModel(scenario=scenario, register_fn=register_dock_loading_domain,
                    task_model_schemas=dock["task_model"], state_declarations=dock["states"],
                    layout_path=dock["layouts"][LAYOUT], setup_path=dock["setups"][setup], assignment_knowledge=False, context_knowledge=False)


def placed(world, agent, area, held=None):
    """`world` with `agent` in `area` (its area fact by the one definition)
    and holding `held`, or nothing."""
    predicates = {p for p in world.predicates
                  if not (p.name in (AREA_FACT, "holding") and p.args[0] == Const(agent))}
    predicates.add(area_fact(agent, POSITIONS[area], world.areas))
    if held is not None:
        predicates.add(Predicate("holding", (Const(agent), Const(held))))
    return replace(world, predicates=predicates)


def route(task, agent, world):
    """The decomposition as (action, target or item[, target]) tuples."""
    steps = []
    for a in AdaptivePlanner(knowledge=MODEL.tree).decompose(task, agent, world):
        b = a.bindings
        steps.append({"move_to": lambda: ("go", b["?target"]), "pick_up": lambda: ("pick", b["?item"]),
                      "place": lambda: ("put", b["?item"], b["?target"]), "scan_it": lambda: ("scan", b["?item"]),
                      "wait_at": lambda: ("wait", b["?entity"]), "stand": lambda: ("stand",)}[a.action_name]())
    return steps


def applicable(task, agent, world):
    return AdaptivePlanner(knowledge=MODEL.tree).is_applicable(task, agent, world)


def go(x): return ("go", x)
def pick(x): return ("pick", x)
def put(x, y): return ("put", x, y)


MODEL = dock_model()                    # kind 2: four full pallets in the truck, two empty ones in the empties
WORLD = build_world_state(MODEL)
G = go(GATE)


# ---------------------------------------------------------------------------
# the robot's methods: two areas, four held-object cases
# ---------------------------------------------------------------------------

# deliver_pallet(pallet_0): from the truck to the dry bay. Another empty pallet: pallet_4 (origin the empties);
# another full one: pallet_1 (origin the truck).
DELIVER = {
    ("held", "area_truck_side", "pallet_0"): [G, go(DRY), put("pallet_0", DRY)],
    ("held", "area_hall", "pallet_0"): [go(DRY), put("pallet_0", DRY)],
    ("return_empty", "area_truck_side", "pallet_4"): [G, go(EMPTIES), put("pallet_4", EMPTIES), G, go("pallet_0"),
                                                      pick("pallet_0"), G, go(DRY), put("pallet_0", DRY)],
    ("return_empty", "area_hall", "pallet_4"): [go(EMPTIES), put("pallet_4", EMPTIES), G, go("pallet_0"),
                                                pick("pallet_0"), G, go(DRY), put("pallet_0", DRY)],
    ("return_full", "area_truck_side", "pallet_1"): [go(TRUCK), put("pallet_1", TRUCK), go("pallet_0"),
                                                     pick("pallet_0"), G, go(DRY), put("pallet_0", DRY)],
    ("return_full", "area_hall", "pallet_1"): [G, go(TRUCK), put("pallet_1", TRUCK), go("pallet_0"),
                                               pick("pallet_0"), G, go(DRY), put("pallet_0", DRY)],
    ("default", "area_truck_side", None): [go("pallet_0"), pick("pallet_0"), G, go(DRY), put("pallet_0", DRY)],
    ("default", "area_hall", None): [G, go("pallet_0"), pick("pallet_0"), G, go(DRY), put("pallet_0", DRY)],
}

# load_return(pallet_4): from the empties into the truck. Another empty pallet: pallet_5 (origin the empties);
# another full one: pallet_0 (origin the truck).
LOAD = {
    ("held", "area_truck_side", "pallet_4"): [go(TRUCK), put("pallet_4", TRUCK)],
    ("held", "area_hall", "pallet_4"): [G, go(TRUCK), put("pallet_4", TRUCK)],
    ("return_empty", "area_truck_side", "pallet_5"): [G, go(EMPTIES), put("pallet_5", EMPTIES), go("pallet_4"),
                                                      pick("pallet_4"), G, go(TRUCK), put("pallet_4", TRUCK)],
    ("return_empty", "area_hall", "pallet_5"): [go(EMPTIES), put("pallet_5", EMPTIES), go("pallet_4"),
                                                pick("pallet_4"), G, go(TRUCK), put("pallet_4", TRUCK)],
    ("return_full", "area_truck_side", "pallet_0"): [go(TRUCK), put("pallet_0", TRUCK), G, go("pallet_4"),
                                                     pick("pallet_4"), G, go(TRUCK), put("pallet_4", TRUCK)],
    ("return_full", "area_hall", "pallet_0"): [G, go(TRUCK), put("pallet_0", TRUCK), G, go("pallet_4"),
                                               pick("pallet_4"), G, go(TRUCK), put("pallet_4", TRUCK)],
    ("default", "area_truck_side", None): [G, go("pallet_4"), pick("pallet_4"), G, go(TRUCK), put("pallet_4", TRUCK)],
    ("default", "area_hall", None): [go("pallet_4"), pick("pallet_4"), G, go(TRUCK), put("pallet_4", TRUCK)],
}

ROBOT_CASES = ([(deliver_pallet("pallet_0"), tasks.deliver_pallet, key, steps) for key, steps in DELIVER.items()]
               + [(load_return("pallet_4"), tasks.load_return, key, steps) for key, steps in LOAD.items()])


@pytest.mark.parametrize("task, schema, key, expected", ROBOT_CASES,
                         ids=[f"{s.name}_{k[0]}_{k[1][5:]}" for _, s, k, _ in ROBOT_CASES])
def test_every_robot_method_is_selected_from_its_area_and_held_case(task, schema, key, expected):
    case, area, held = key
    world = placed(WORLD, R, area, held)
    assert route(task, R, world) == expected
    method = f"{schema.name}_{case}_{area[5:]}"
    assert AdaptivePlanner(knowledge=MODEL.tree).decompose(task, R, world, method=method) == \
        AdaptivePlanner(knowledge=MODEL.tree).decompose(task, R, world)


def test_sixteen_robot_methods():
    names = {m.name for s in (tasks.deliver_pallet, tasks.load_return) for m in s.methods}
    assert len(names) == 16
    assert names == {f"{s}_{c}_{a[5:]}" for s in ("deliver_pallet", "load_return") for c, a, _ in
                     (DELIVER if s == "deliver_pallet" else LOAD)}


@pytest.mark.parametrize("task, schema, key, expected", ROBOT_CASES,
                         ids=[f"{s.name}_{k[0]}_{k[1][5:]}" for _, s, k, _ in ROBOT_CASES])
def test_the_routes_cross_the_gate_exactly_when_the_areas_differ(task, schema, key, expected):
    """From the start area, each move_to(dock_gate) passes to the other side
    of the gate; every other walk ends in the area the robot is then in."""
    case, area, held = key
    world = placed(WORLD, R, area, held)
    other_side = {"area_truck_side": "area_hall", "area_hall": "area_truck_side"}
    gated = False
    for step in route(task, R, world):
        if step == G:
            area, gated = other_side[area], True
        elif step[0] == "go":
            assert area_at(WORLD.object_positions[step[1]], WORLD.areas).id == area, (key, step)
    method = next(m for m in schema.methods if m.name == f"{schema.name}_{case}_{key[1][5:]}")
    assert gated == (Predicate("is_open", (Const(GATE),)) in
                     {Predicate(g.name, tuple(a for a in g.args)) for g in method.guards})


def test_a_robot_method_that_crosses_the_gate_needs_it_open():
    closed = replace(WORLD, predicates={p for p in WORLD.predicates if p.name != "is_open"})
    for task, schema, key, expected in ROBOT_CASES:
        world = placed(closed, R, key[1], key[2])
        assert applicable(task, R, world) == (G not in expected), key


# ---------------------------------------------------------------------------
# applicability: load_return to an empty pallet only; the scan once the pallet is in its bay
# ---------------------------------------------------------------------------

def test_load_return_is_not_applicable_to_a_full_pallet():
    for area in ("area_truck_side", "area_hall"):
        for held in (None, "pallet_0", "pallet_1", "pallet_4"):
            world = placed(WORLD, R, area, held)
            assert not applicable(load_return("pallet_0"), R, world), (area, held)
            assert applicable(load_return("pallet_4"), R, world), (area, held)


def test_deliver_pallet_has_no_condition_on_the_pallet_being_full():
    world = placed(WORLD, R, "area_hall")
    assert applicable(deliver_pallet("pallet_4"), R, world)


def test_the_scan_is_applicable_only_once_the_pallet_stands_in_its_bay():
    model = dock_model(robot_tasks=[deliver_pallet("pallet_0")])
    scan = confirm_delivered_pallet("pallet_0")
    in_bay = Predicate("obj_at", (Const("pallet_0"), Const(DRY)))
    for tick in range(300):
        world = build_world_state(model)
        if in_bay in world.predicates:
            break
        assert not applicable(scan, H, world), tick
        model.step()
    else:
        pytest.fail("the robot never placed pallet_0 in its bay")
    assert applicable(scan, H, world)
    assert route(scan, H, world) == [go("pallet_0"), ("scan", "pallet_0")]


def test_the_scan_of_a_pallet_in_the_truck_is_not_applicable():
    world = build_world_state(dock_model(setup="env_setup_02"))      # kind 1: pallet_0 in its bay, pallet_4 in the truck
    assert applicable(confirm_delivered_pallet("pallet_0"), H, world)
    assert not applicable(confirm_delivered_pallet("pallet_4"), H, world)


# ---------------------------------------------------------------------------
# the human's tasks from the hall and the office
# ---------------------------------------------------------------------------

KIND_1 = build_world_state(dock_model(setup="env_setup_02"))
HUMAN = {
    "confirm_delivered_pallet": (confirm_delivered_pallet("pallet_0"), [go("pallet_0"), ("scan", "pallet_0")]),
    "coffee_break": (coffee_break("coffee_machine_0"), [go("coffee_machine_0"), ("wait", "coffee_machine_0")]),
    "go_to": (go_to("desk"), [go("desk")]),
    "go_to_and_stand": (go_to_and_stand("standby_place", "PT4S"), [go("standby_place"), ("stand",)]),
}


@pytest.mark.parametrize("name", sorted(HUMAN))
def test_the_humans_tasks_from_the_hall_and_the_office(name):
    task, hall_route = HUMAN[name]
    assert route(task, H, placed(KIND_1, H, "area_hall")) == hall_route
    assert route(task, H, placed(KIND_1, H, "area_office")) == [go(DOOR)] + hall_route


def test_office_break_ends_at_the_chair():
    task = office_break("office_chair")
    rest = [go("office_chair"), ("wait", "office_chair")]
    assert route(task, H, placed(KIND_1, H, "area_hall")) == [go(DOOR)] + rest
    assert route(task, H, placed(KIND_1, H, "area_office")) == rest


def test_eleven_human_methods():
    schemas = (tasks.confirm_delivered_pallet, tasks.coffee_break, tasks.office_break, tasks.go_to,
               tasks.go_to_and_stand, tasks.stand_task)
    assert sum(len(s.methods) for s in schemas) == 11


# ---------------------------------------------------------------------------
# an agent outside its areas has no applicable method
# ---------------------------------------------------------------------------

def test_an_agent_outside_its_areas_has_no_applicable_method():
    robot_in_office = placed(WORLD, R, "area_office")
    for task in (deliver_pallet("pallet_0"), load_return("pallet_4")):
        with pytest.raises(DecompositionError):
            AdaptivePlanner(knowledge=MODEL.tree).decompose(task, R, robot_in_office)
    human_on_truck_side = placed(KIND_1, H, "area_truck_side")
    for task in (confirm_delivered_pallet("pallet_0"), coffee_break("coffee_machine_0"),
                 office_break("office_chair"), go_to("desk"), go_to_and_stand("desk", "PT4S")):
        assert not applicable(task, H, human_on_truck_side), task
    assert applicable(stand("PT4S"), H, human_on_truck_side)      # stand has one method, with no guard
