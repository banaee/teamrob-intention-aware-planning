# tests/test_tg_areas.py
"""
T-G stage 1, step 2 (A9 and R2): the declared areas and the agent's area in a
computed state. area_at's boundary rule (interior, edge, outside); the body's
world-state builder and successor_state() agree at the body's walk end; a
chained ordering selects the next entry's method by the area the previous entry
ends in; the gate approached from each side stays in the area of approach (the
body's stop, the Projector's arrival point, the replay's advance); the replay's
cut world carries the area.
Run from the repo root:  PYTHONHASHSEED=0 python -m pytest tests/test_tg_areas.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "mesa_sim"))

from shared.knowledge import Tree, TaskModel
from shared.planner import AdaptivePlanner
from shared.projection import Projector, successor_state
from shared.trajectory_algorithms import arrival_point
from shared.types import (
    AREA_FACT, ActionStep, Area, ConditionSchema, Const, GroundedAction, MethodSchema, PersonalTask,
    Predicate, Script, TaskInstance, Var, WorkTask, area_at, area_fact,
)
from world.human_executor import StackMachine, advance, check_script
from domains.kitting.actions import move_to
from domains.kitting.registry import register_kitting_domain
from domains.dock_loading.actions import move_to as dock_move_to
from domains.dock_loading.registry import domain_config as dock_config, register_dock_loading_domain
from mesa_sim.action_decomposer import _get_step_size, _parse_duration_to_steps, walk_positions
from mesa_sim.sim_model import SimModel
from mesa_sim.world_state_builder import PROXIMITY_THRESHOLD, build_world_state
from tests.kitting.test_th2_executor import H, goto, model_for, st


def area_facts(world, agent):
    return {p for p in world.predicates if p.name == AREA_FACT and p.args[0] == Const(agent)}


# ---------------------------------------------------------------------------
# the boundary rule
# ---------------------------------------------------------------------------

def test_area_at_interior_edge_and_outside():
    west, east = Area("west", 0, 10, 0, 10), Area("east", 10, 20, 0, 10)
    assert area_at((5, 5), (west, east)) is west
    assert area_at((15, 0), (west, east)) is east                   # a corner of the closed rectangle
    assert area_at((10, 5), (west, east)) is west                   # the shared edge: the first declared
    assert area_at((10, 5), (east, west)) is east
    assert area_at((30, 5), (west, east)) is None
    assert area_fact("a", (30, 5), (west, east)) is None
    assert area_fact("a", (15, 5), (west, east)) == Predicate(AREA_FACT, (Const("a"), Const("east")))


# ---------------------------------------------------------------------------
# one definition: the builder and every computed state
# ---------------------------------------------------------------------------

def test_the_builder_and_successor_state_agree_at_the_body_walk_end():
    m = model_for("env_layout_01", "scenario_s01_01", Script([]), robot=False)
    world = build_world_state(m)
    walk = lambda a, b: walk_positions(a, b, _get_step_size(m))
    [action] = AdaptivePlanner(knowledge=m.tree).decompose(goto("corner_SW"), H, world)
    end = walk(world.agent_positions[H], world.object_positions["corner_SW"])[-1]
    advanced = advance(world, [action], H, walk)
    assert advanced.agent_positions[H] == end
    h = m.humans[H]
    m.space.move_agent(h, end)
    h.pos = end
    built = build_world_state(m)
    assert area_facts(built, H) != area_facts(world, H)              # the walk leaves the start's area
    assert area_facts(advanced, H) == area_facts(built, H) == {area_fact(H, end, built.areas)}
    assert area_facts(successor_state(world, [], H, end), H) == area_facts(built, H)


def _probe_tree():
    """kitting's tree, a walk as a PersonalTask, and a task whose method is selected by the agent's area."""
    kit = register_kitting_domain()
    agent, spot, a, b, target = Var("?agent"), Var("?spot"), Var("?a"), Var("?b"), Var("?target")
    walk_to = PersonalTask(name="walk_to", parameters=[spot], parameter_types={"?spot": "shelf"},
                           methods=[MethodSchema("walk_to_default", [spot], [], [ActionStep(move_to, {target: spot})])])
    probe = PersonalTask(name="probe", parameters=[a, b], parameter_types={"?a": "shelf", "?b": "shelf"},
                         methods=[MethodSchema("probe_from_SE", [a, b], [ConditionSchema(AREA_FACT, (agent, Const("zone_SE")))],
                                               [ActionStep(move_to, {target: a})]),
                                  MethodSchema("probe_from_NW", [a, b], [ConditionSchema(AREA_FACT, (agent, Const("zone_NW")))],
                                               [ActionStep(move_to, {target: b})])])
    tree = Tree(tasks=kit.task_schemas() + [walk_to, probe], actions=kit.get_all_actions(),
                microactions=kit.get_microactions())
    schemas = [t for t in tree.task_schemas() if isinstance(t, WorkTask)] + [walk_to, probe]
    return TaskModel(tree, schemas), walk_to, probe


def test_a_chained_ordering_selects_the_next_entrys_method_by_area():
    m = model_for("env_layout_01", "scenario_s01_01", Script([]), robot=False)
    world = build_world_state(m)
    tm, walk_to, probe = _probe_tree()
    projector = Projector(task_model=tm, assumed_speed=_get_step_size(m), arrival_radius=PROXIMITY_THRESHOLD)
    probe_task = TaskInstance(schema=probe, bindings={Var("?a"): Const("shelf_3"), Var("?b"): Const("shelf_2")})
    for spot, target in (("shelf_4", "shelf_3"), ("shelf_7", "shelf_2")):    # shelf_4 in zone_SE, shelf_7 in zone_NW
        first = TaskInstance(schema=walk_to, bindings={Var("?spot"): Const(spot)})
        plan = projector.project([first, probe_task], world, H, belief=None)
        [action] = plan.entries[1].abstract_plan.actions
        assert action.bindings["?target"] == target, spot


# ---------------------------------------------------------------------------
# the gate: the area of approach
# ---------------------------------------------------------------------------

def _dock_model():
    base = dock_config["scenarios"]["scenario_s03_01"]
    return SimModel(scenario=base, register_fn=register_dock_loading_domain,
                    task_model_schemas=dock_config["task_model"],
                    layout_path=dock_config["layouts"]["env_layout_02"],
                    setup_path=dock_config["setups"][base.setup],
                    state_declarations=dock_config["states"])


def test_the_gate_approached_from_each_side():
    m = _dock_model()
    world = build_world_state(m)
    agent = next(iter(m.humans))
    gate = m.objects["dock_gate"].position
    walk = lambda a, b: walk_positions(a, b, _get_step_size(m))
    move = GroundedAction(action_name="move_to", bindings={"?agent": agent, "?target": "dock_gate"},
                          completion_predicate=None, schema=dock_move_to)
    sides = set()
    for start in ((gate[0], gate[1] + 300), (gate[0], gate[1] - 300)):
        side = area_at(start, m.areas)
        stop = walk(start, gate)[-1]
        assert 10 <= abs(stop[1] - gate[1]) <= 30
        assert area_at(stop, m.areas) is side                                       # the body's stop
        assert area_at(arrival_point(start, gate, PROXIMITY_THRESHOLD), m.areas) is side   # the Projector's
        advanced = advance(successor_state(world, [], agent, start), [move], agent, walk)
        assert area_facts(advanced, agent) == {area_fact(agent, stop, m.areas)}       # the replay's
        sides.add(side.id)
    assert len(sides) == 2


# ---------------------------------------------------------------------------
# the replay's cut world
# ---------------------------------------------------------------------------

def test_the_cut_world_carries_the_area(monkeypatch):
    script = Script([goto("corner_SW").during(move_to, "PT60S", st("PT2S"))])
    m = model_for("env_layout_01", "scenario_s01_01", script, robot=False)
    world = build_world_state(m)
    cut_worlds = []
    original = StackMachine.cut
    def cut(self, w, tick, n):
        cut_worlds.append(w)
        return original(self, w, tick, n)
    monkeypatch.setattr(StackMachine, "cut", cut)
    check_script(script, AdaptivePlanner(knowledge=m.tree), world, H, lambda d: _parse_duration_to_steps(d, m),
                 lambda a, b: walk_positions(a, b, _get_step_size(m)))
    [w] = cut_worlds
    position = w.agent_positions[H]
    assert area_facts(w, H) != area_facts(world, H)                  # the cut lies in another area than the start
    assert area_facts(w, H) == {area_fact(H, position, w.areas)}
