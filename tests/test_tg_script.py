# tests/test_tg_script.py
"""
T-G stage 1, step 5: the human's script form (A3, Q12 to Q15, R1). The
placement refusals; the priority list (an entry skipped and taken later, an
ordinary entry taken once whether completed, dropped or infeasible on
resumption, a suspended entry kept open); the repeatable entry's skip rule and
its retaking; Wait; the closing part (in order, waiting on an entry not
applicable, Idle after it); the load-time replay for both kinds of script, with
repeatable entries not replayed; the run-end statement; the exit walk on the
last closing entry; the choice point.
Run from the repo root:  PYTHONHASHSEED=0 python -m pytest tests/test_tg_script.py
"""

import logging
import sys
from dataclasses import replace
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "mesa_sim"))

from shared.knowledge import Tree
from shared.planner import AdaptivePlanner
from shared.types import (
    ActionStep, AgentConfig, Const, MethodSchema, PersonalTask, Predicate, RepeatableEntry, ScenarioConfig, Script,
    ScriptDependence, ScriptEntry, Start, TaskInstance, Var, drop,
)
from world.composition import ScenarioCoverage, scenario_composition
from world.human_executor import Idle, RunAction, ResumeAction, ScriptError, StackMachine, Wait, check_script
from world.record import ClosingRef, Entered, Left, OrdinaryRef, Outcome, Record, StillOpen
from domains.kitting.actions import move_to, pick_up, place
from domains.kitting.registry import domain_config, register_kitting_domain
from domains.kitting.script import deliver_item, stand
from mesa_sim.world_state_builder import build_world_state
from tests.test_th2_executor import H, TICKS, _carry_tree, goto, key, kinds, model_for, run, st

LAYOUT, SID = "env_layout_01", "scenario_s01_01"


def carry_task(carry):
    return TaskInstance(schema=carry, bindings={Var("?item"): Const("item_3"), Var("?target"): Const("kitting_table_0")})


def held(world):
    """`world` with item_3 in the human's hand: carry_to is applicable."""
    return replace(world, predicates=world.predicates | {Predicate("holding", (Const(H), Const("item_3")))},
                   object_locations={**world.object_locations, "item_3": H})


def at(world, target):
    return replace(world, predicates=world.predicates | {Predicate("at", (Const(H), Const(target)))})


def machine_for(script, tree=None, cls=StackMachine):
    tree = tree if tree is not None else _carry_tree()[0]
    return cls(script, AdaptivePlanner(knowledge=tree), H, lambda d: TICKS[d], Record())


def world0():
    return build_world_state(model_for(LAYOUT, SID, Script([]), robot=False))


def acknowledge(machine, world, tick):
    """The action in hand is completed at once."""
    nxt = machine.next(world, tick)
    assert isinstance(nxt, (RunAction, ResumeAction)), nxt
    machine.action_done(world, tick)
    return nxt


def entered(record):
    return [key(t.task) for t in record.transitions if isinstance(t, Entered)]


def carry_model(script, tree):
    """The scenario with the human alone running `script` on `tree`."""
    base = domain_config["scenarios"][SID]
    human = next(a for a in base.agents if a.agent_type == "human")
    cfg = AgentConfig(agent_id=H, agent_type="human", start_position=human.start_position, scheduled_tasks=script)
    scenario = ScenarioConfig(id="scenario_test", description="t", agents=[cfg],
                              setup=base.setup, reference_layouts=base.reference_layouts)
    from mesa_sim.sim_model import SimModel
    return SimModel(scenario=scenario, register_fn=lambda: tree, task_model_schemas=domain_config["task_model"],
                    layout_path=domain_config["layouts"][LAYOUT], setup_path=domain_config["setups"][base.setup])


# ---------------------------------------------------------------------------
# the form
# ---------------------------------------------------------------------------

def test_the_placement_refusals_and_the_stored_split():
    a, b, c, walk = st("PT2S"), st("PT4S"), st("PT6S"), goto("door")
    with pytest.raises(ValueError, match="below the repeatable entry"):
        Script([RepeatableEntry(walk), a])
    with pytest.raises(ValueError, match="closing part holds no repeatable entry"):
        Script([a], closing=[RepeatableEntry(walk)])
    with pytest.raises(TypeError, match="carries no events"):
        RepeatableEntry(walk.at(move_to, drop))
    standby = RepeatableEntry(walk)
    for name in ("at", "during", "events"):
        assert not hasattr(standby, name)
    with pytest.raises(TypeError, match="ScriptDependence"):
        Script([a], dependence="on_robot")
    s = Script([a, standby], closing=[b, c.at(move_to, drop)], dependence=ScriptDependence.ON_ROBOT)
    assert s.entries == [ScriptEntry(a, ())] and s.repeatable == [standby]
    assert [e.task for e in s.closing] == [b, c] and s.dependence is ScriptDependence.ON_ROBOT
    assert s.tasks() == [a, walk, b, c]
    assert Script([a]).dependence is ScriptDependence.INDEPENDENT and Script([a]).closing == []


# ---------------------------------------------------------------------------
# the priority list
# ---------------------------------------------------------------------------

def test_an_entry_not_applicable_is_skipped_and_taken_later():
    tree, carry = _carry_tree()
    world, task, later = world0(), carry_task(carry), st("PT4S")
    machine = machine_for(Script([task, later]), tree)
    assert acknowledge(machine, world, 0).action.action_name == "stand"     # carry_to not applicable: the stand
    assert isinstance(machine.next(world, 1), Wait)                          # nothing applicable: wait
    assert machine.next(held(world), 2).action.action_name == "move_to"      # applicable now: taken
    assert entered(machine.record) == [key(later), key(task)]


def test_an_ordinary_entry_is_taken_once():
    world = world0()
    # completed: closed, never taken again
    a = st("PT2S")
    machine = machine_for(Script([a]))
    acknowledge(machine, world, 0)
    assert isinstance(machine.next(world, 1), Idle) and entered(machine.record) == [key(a)]
    # dropped: closed, the next entry is taken
    a, b = st("PT10S"), st("PT4S")
    machine = machine_for(Script([a, b]))
    machine.next(world, 0)
    machine.inject(drop, world, 1, 0)
    acknowledge(machine, world, 2)
    assert isinstance(machine.next(world, 3), Idle)
    assert entered(machine.record) == [key(a), key(b)]
    assert ("left", key(a), Outcome.ABANDONED) in kinds(machine.record)
    # infeasible on resumption: closed, not taken again once applicable
    tree, carry = _carry_tree()
    task, after = carry_task(carry), st("PT4S")
    machine = machine_for(Script([task, after]), tree)
    assert machine.next(held(world), 0).action.action_name == "move_to"
    machine.inject(Start(st("PT2S")), held(world), 1, 2)
    acknowledge(machine, held(world), 2)                  # the stand; carry_to resumes, the cut walk first
    acknowledge(machine, world, 3)                        # the walk done where the item is not held
    acknowledge(machine, world, 4)                        # infeasible: the next entry runs
    assert isinstance(machine.next(held(world), 5), Idle)
    assert ("left", key(task), Outcome.INFEASIBLE) in kinds(machine.record)
    assert entered(machine.record) == [key(task), key(after)]


def test_a_suspended_entry_stays_open():
    world, a, b = world0(), st("PT10S"), st("PT4S")
    machine = machine_for(Script([a, b]))
    machine.next(world, 0)
    machine.inject(Start(goto("door")), world, 1, 2)
    assert ("left", key(a), Outcome.SUSPENDED) in kinds(machine.record)
    assert machine.open_entries() == [OrdinaryRef(0), OrdinaryRef(1)]
    acknowledge(machine, world, 2)                        # the walk: a resumes
    assert machine.open_entries() == [OrdinaryRef(0), OrdinaryRef(1)]
    assert isinstance(acknowledge(machine, world, 3), ResumeAction)
    assert machine.open_entries() == [OrdinaryRef(1)]
    assert machine.next(world, 4).action.action_name == "stand" and machine.stack_tasks() == [b]


# ---------------------------------------------------------------------------
# the repeatable entry
# ---------------------------------------------------------------------------

def test_the_skip_rule_and_the_repeatable_entry_taken_again():
    tree, carry = _carry_tree()
    world, task, walk = world0(), carry_task(carry), goto("door")
    machine = machine_for(Script([task, RepeatableEntry(walk)]), tree)
    assert machine.next(world, 0).action.action_name == "move_to"  # carry_to not applicable: the standby walk
    machine.action_done(at(world, "door"), 0)
    assert isinstance(machine.next(at(world, "door"), 1), Wait)    # skipped while its completion condition holds
    assert machine.next(world, 2).action.action_name == "move_to"  # the human has left the place: taken again
    machine.action_done(at(world, "door"), 2)
    assert machine.next(held(at(world, "door")), 3).action.action_name == "move_to"
    assert machine.stack_tasks() == [task]                         # an applicable ordinary entry comes first
    assert entered(machine.record) == [key(walk), key(walk), key(task)]
    assert machine.open_entries() == [OrdinaryRef(0)]              # the repeatable entry is never listed


# ---------------------------------------------------------------------------
# the closing part
# ---------------------------------------------------------------------------

def test_the_closing_part_in_written_order_through_the_body_and_the_replay():
    a, walk, b = st("PT2S"), goto("door"), st("PT4S")
    script = Script([a], closing=[walk, b])
    m = model_for(LAYOUT, SID, script, robot=False)
    h = m.humans[H]
    from mesa_sim.action_decomposer import _parse_duration_to_steps, _get_step_size, walk_positions
    replay = check_script(script, h.machine.planner, build_world_state(m), H,
                          lambda d: _parse_duration_to_steps(d, m), lambda p, q: walk_positions(p, q, _get_step_size(m)))
    run(m)
    assert entered(h.record) == [key(a), key(walk), key(b)]
    assert kinds(replay) == kinds(h.record)


def test_the_closing_part_waits_until_the_list_is_finished_and_on_an_entry_not_applicable():
    tree, carry = _carry_tree()
    world, task, a, b = world0(), carry_task(carry), st("PT2S"), st("PT4S")
    machine = machine_for(Script([task], closing=[a]), tree)
    assert isinstance(machine.next(world, 0), Wait)               # the list is not finished: no closing entry
    machine = machine_for(Script([a], closing=[task, b]), tree)
    acknowledge(machine, world, 0)
    assert isinstance(machine.next(world, 1), Wait)               # the next closing entry is not applicable
    assert machine.next(held(world), 2).action.action_name == "move_to" and machine.stack_tasks() == [task]


def test_idle_after_the_closing_part_no_repeatable_entry():
    world, a, b, walk = world0(), st("PT2S"), st("PT4S"), goto("door")
    machine = machine_for(Script([a, RepeatableEntry(walk)], closing=[b]))
    acknowledge(machine, world, 0)
    acknowledge(machine, world, 1)                                # the closing stand, not the standby walk
    assert isinstance(machine.next(world, 2), Idle)               # not at the door, yet nothing more
    assert entered(machine.record) == [key(a), key(b)]


# ---------------------------------------------------------------------------
# the load-time replay
# ---------------------------------------------------------------------------

def _put_tree():
    """kitting's tree plus carry_to (needs the item in hand), grab (takes it)
    and put_down (places it on a shelf)."""
    kit = register_kitting_domain()
    tree, carry = _carry_tree()
    item, target = Var("?item"), Var("?target")
    grab = PersonalTask(name="grab", parameters=[item], parameter_types={"?item": "item"},
                        methods=[MethodSchema("grab_default", [item], [],
                                              [ActionStep(move_to, {target: item}), ActionStep(pick_up, {item: item})])])
    put = PersonalTask(name="put_down", parameters=[item, target],
                       parameter_types={"?item": "item", "?target": "shelf"},
                       methods=[MethodSchema("put_default", [item, target], [],
                                             [ActionStep(move_to, {target: target}),
                                              ActionStep(place, {item: item, target: target})])])
    tree = Tree(tasks=kit.task_schemas() + [carry, grab, put], actions=kit.get_all_actions(),
                microactions=kit.get_microactions())
    return tree, carry, grab, put


def replay(script, tree, world):
    return check_script(script, AdaptivePlanner(knowledge=tree), world, H, lambda d: TICKS[d], lambda a, b: [b])


def test_the_replay_of_an_independent_script_stops_on_an_entry_left_open():
    tree, carry = _carry_tree()
    task, b = carry_task(carry), st("PT4S")
    with pytest.raises(ScriptError, match=r"left open: entry=0 carry_to\(.*\); closing=0 stand\(\?duration=PT4S\)"):
        replay(Script([task], closing=[b]), tree, world0())


def test_the_replay_of_a_dependent_script_reports_and_loads(caplog):
    tree, carry = _carry_tree()
    task, a, b = carry_task(carry), st("PT2S"), st("PT4S")
    script = Script([task, a], closing=[b], dependence=ScriptDependence.ON_ROBOT)
    record = replay(script, tree, world0())
    still = [t for t in record.transitions if isinstance(t, StillOpen)]
    assert [(t.entry, key(t.task)) for t in still] == [(OrdinaryRef(0), key(task)), (ClosingRef(0), key(b))]
    assert entered(record) == [key(a)]
    with caplog.at_level(logging.INFO):
        carry_model(script, tree)
    assert (f"[replay] {H} not replayed: entry=0 {key(task)} closing=0 {key(b)}"
            in [r.getMessage() for r in caplog.records])


def test_infeasible_stays_a_load_error_for_both_kinds():
    # a task begun that cannot continue: carry_to suspended by a put_down,
    # resumed with the item no longer in hand
    tree, carry, grab, put = _put_tree()
    take = TaskInstance(schema=grab, bindings={Var("?item"): Const("item_3")})
    put_down = TaskInstance(schema=put, bindings={Var("?item"): Const("item_3"), Var("?target"): Const("shelf_2")})
    for dependence in ScriptDependence:
        script = Script([take, carry_task(carry).at(move_to, put_down)], dependence=dependence)
        with pytest.raises(ScriptError, match="infeasible:carry_to"):
            replay(script, tree, world0())


def test_repeatable_entries_are_not_replayed():
    tree, carry = _carry_tree()
    a, walk, task = st("PT2S"), goto("door"), carry_task(carry)
    record = replay(Script([a, RepeatableEntry(walk)]), tree, world0())
    assert entered(record) == [key(a)]
    record = replay(Script([task, RepeatableEntry(walk)], dependence=ScriptDependence.ON_ROBOT), tree, world0())
    assert entered(record) == [] and [key(t.task) for t in record.transitions if isinstance(t, StillOpen)] == [key(task)]
    with pytest.raises(ScriptError, match="left open: entry=0 carry_to"):
        replay(Script([task, RepeatableEntry(walk)]), tree, world0())


# ---------------------------------------------------------------------------
# the run's end
# ---------------------------------------------------------------------------

def test_the_run_end_statement_for_a_dependent_script_only(caplog):
    tree, carry = _carry_tree()
    task, a, walk = carry_task(carry), st("PT2S"), goto("door")
    m = carry_model(Script([task, a], closing=[walk], dependence=ScriptDependence.ON_ROBOT), tree)
    h = m.humans[H]
    for _ in range(5):
        m.step()
    with caplog.at_level(logging.INFO):
        h.end_run(5)
    still = [t for t in h.record.transitions if isinstance(t, StillOpen)]
    assert [(t.tick, t.entry, key(t.task)) for t in still] == [(5, OrdinaryRef(0), key(task)),
                                                               (5, ClosingRef(0), key(walk))]
    assert h.record.end_line(5) == f"[rec] end step=5 open={key(task)};{key(walk)}"
    assert f"[human] step=5 {H} open:{key(task)}" in [r.getMessage() for r in caplog.records]
    # an independent script writes nothing
    m = model_for(LAYOUT, SID, Script([st("PT2S")]), robot=False)
    h = run(m)
    before = list(h.record.transitions)
    h.end_run(int(m.schedule.steps))
    assert h.record.transitions == before


# ---------------------------------------------------------------------------
# the exit walk, the choice point
# ---------------------------------------------------------------------------

def test_the_exit_walk_is_the_last_closing_entry():
    from tests.test_th_composition import R, model_for as composition_model
    robot = composition_model(LAYOUT, "scenario_s01_05").observing[R]
    assert scenario_composition(Script([deliver_item("item_3")], closing=[goto("door")]), robot)[1] \
        is ScenarioCoverage.MODELLED_ONLY
    # with a closing part, the last ordinary entry is no exit walk
    assert scenario_composition(Script([deliver_item("item_3"), goto("door")], closing=[stand("PT10S")]), robot)[1] \
        is ScenarioCoverage.TASK_ABSENT


def test_choose_is_the_one_replaceable_choice():
    tree, carry = _carry_tree()
    world, task, a, b = world0(), carry_task(carry), st("PT2S"), st("PT4S")
    offered = []

    class Last(StackMachine):
        def choose(self, candidates):
            offered.append(list(candidates))
            return candidates[-1]

    machine = machine_for(Script([task, a, b]), tree, Last)
    machine.next(world, 0)
    assert offered == [[OrdinaryRef(1), OrdinaryRef(2)]] and machine.stack_tasks() == [b]

    class Elsewhere(StackMachine):
        def choose(self, candidates):
            return OrdinaryRef(0)

    with pytest.raises(ValueError, match="not one of"):
        machine_for(Script([task, a]), tree, Elsewhere).next(world, 0)
