# tests/test_th2_executor.py
"""
T-H2: the human's executor. The script form and its sugar, the stack machine
through the body (every event kind, a cut inside a walk and inside a stand and a
wait_at, a Drop, a refused second Start, inject), an infeasible resumption on
the machine alone, the load-time replay (anchors, occurrences, a during outside
its action, a Drop after the last action), the replay against the run, and the
guard that the robot's inputs carry nothing of the stack.
Run from the repo root:  PYTHONHASHSEED=0 python -m pytest tests/test_th2_executor.py
"""

import sys
from dataclasses import fields, is_dataclass, replace
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "mesa_sim"))

from shared.knowledge import Tree
from shared.planner import AdaptivePlanner
from world.record import (Boundary, Cut, Entered, Left, Outcome, Record, Refused, RefusalReason, Resumed,
                           Snapshot, Started, Transition, Unfired)
from shared.types import (
    ActionStep, AfterAction, AgentConfig, ConditionSchema, Const, Decision, Drop, DuringAction, Event, MethodSchema,
    Now, PersonalTask, Predicate, ScenarioConfig, Script, ScriptEntry, Start, TaskInstance, Trigger, Var,
    WorldState, drop,
)
from world.human_executor import Frame, Idle, RunAction, StackMachine, check_script
from domains.kitting.actions import move_to, pick_up, place, stand, wait_at
from domains.kitting.registry import domain_config, register_kitting_domain
from domains.kitting.tasks import coffee_break, deliver_item, go_to, stand_task
from mesa_sim.obs_builder import build_observation
from mesa_sim.sim_model import SimModel
from mesa_sim.world_state_builder import build_world_state

H = "human_0"
TICKS = {"PT2S": 1, "PT4S": 2, "PT6S": 3, "PT10S": 5, "PT20S": 10, "PT60S": 30}   # 2 s per step


def deliver(item, table="kitting_table_0"):
    return TaskInstance(schema=deliver_item, bindings={Var("?item"): Const(item), Var("?kitting_table"): Const(table)})


def coffee():
    return TaskInstance(schema=coffee_break, bindings={Var("?coffee_machine"): Const("coffee_machine_0")})


def st(duration):
    return TaskInstance(schema=stand_task, bindings={Var("?duration"): Const(duration)})


def goto(landmark):
    return TaskInstance(schema=go_to, bindings={Var("?landmark"): Const(landmark)})


def key(task):
    from shared.types import task_instance_key
    return task_instance_key(task)


def model_for(layout, sid, script, robot=True):
    """The registered scenario with the human's script replaced (and, without
    `robot`, the human alone)."""
    base = domain_config["scenarios"][sid]
    human = next(a for a in base.agents if a.agent_type == "human")
    cfg = AgentConfig(agent_id=human.agent_id, agent_type="human", start_position=human.start_position,
                      scheduled_tasks=script, assigned_tasks=human.assigned_tasks)
    others = [a for a in base.agents if a is not human] if robot else []
    scenario = ScenarioConfig(id="scenario_test", description="t", agents=[cfg] + others,
                              setup=base.setup, reference_layouts=base.reference_layouts)
    return SimModel(scenario=scenario, register_fn=register_kitting_domain,
                    task_model_schemas=domain_config["task_model"],
                    layout_path=domain_config["layouts"][layout],
                    setup_path=domain_config["setups"][base.setup])


def run(m, max_steps=400):
    """Step until the human's script is finished; the human agent."""
    h = m.humans[H]
    for _ in range(max_steps):
        m.step()
        if not h.machine.stack and h.machine.next_entry >= len(h.machine.entries):
            return h
    pytest.fail("the script did not finish")


def kinds(record):
    """The transitions, ticks dropped: (class, task key, outcome / trigger / reason)."""
    out = []
    for t in record.transitions:
        if isinstance(t, Left):
            out.append(("left", key(t.task), t.outcome))
        elif isinstance(t, Started):
            out.append(("started", key(t.task), type(t.trigger).__name__))
        elif isinstance(t, (Entered, Resumed)):
            out.append((type(t).__name__.lower(), key(t.task), None))
        elif isinstance(t, Refused):
            out.append(("refused", repr(t.decision), t.reason))
        else:
            out.append(("unfired", key(t.task), t.reason))
    return out


def action_sequence(record):
    """(task on top, action, occurrence), consecutive duplicates merged, the
    idle ticks after the script dropped."""
    out = []
    for s in record.snapshots:
        if not s.stack:
            continue
        item = (key(s.stack[0]), s.action.action_name if s.action else None, s.occurrence)
        if not out or out[-1] != item:
            out.append(item)
    return out


def holds(world, name, *args):
    return Predicate(name, tuple(Const(a) for a in args)) in world.predicates


# ---------------------------------------------------------------------------
# the script form
# ---------------------------------------------------------------------------

def test_sugar_builds_typed_events():
    # a TaskInstance's == is object identity (T-H4): the events hold the objects written
    d, c = deliver("item_3"), coffee()
    e = d.at(pick_up, c).during(move_to, "PT6S", drop, occurrence=1)
    assert isinstance(e, ScriptEntry) and len(e.events) == 2
    assert e.events[0] == Event(AfterAction(pick_up, None), Start(c))
    assert e.events[1] == Event(DuringAction(move_to, "PT6S", 1), Drop())
    assert Script([d]).entries[0] == ScriptEntry(d, ())
    for base in (Trigger, Decision):
        with pytest.raises(TypeError, match="not constructed directly"):
            base()
    with pytest.raises(TypeError, match="starts a TaskInstance or is `drop`"):
        deliver("item_3").at(pick_up, "coffee")
    with pytest.raises(TypeError, match="not a TaskInstance or a ScriptEntry"):
        Script([Start(coffee())])
    # a decision's task carries no events: the type excludes nesting
    assert not hasattr(Start(coffee()).task, "events")


# ---------------------------------------------------------------------------
# the stack through the body
# ---------------------------------------------------------------------------

def test_at_pick_up_start_suspends_and_resumes_re_expanded():
    m = model_for("env_layout1", "scenario_10", Script([deliver("item_2").at(pick_up, coffee()), deliver("item_5")]))
    h = run(m)
    assert kinds(h.record) == [
        ("entered", key(deliver("item_2")), None),
        ("left", key(deliver("item_2")), Outcome.SUSPENDED),
        ("started", key(coffee()), "AfterAction"),
        ("left", key(coffee()), Outcome.COMPLETED),
        ("resumed", key(deliver("item_2")), None),
        ("left", key(deliver("item_2")), Outcome.COMPLETED),
        ("entered", key(deliver("item_5")), None),
        ("left", key(deliver("item_5")), Outcome.COMPLETED),
    ]
    started = next(t for t in h.record.transitions if isinstance(t, Started))
    assert started.where == Boundary(started.where.action, 0) and started.where.action.action_name == "pick_up"
    # the resumption re-expanded the delivery in the resulting state: held item, no pick_up
    seq = action_sequence(h.record)
    i = seq.index((key(coffee()), "wait_at", 0))
    assert seq[i + 1:i + 3] == [(key(deliver("item_2")), "move_to", 0), (key(deliver("item_2")), "place", 0)]
    world = build_world_state(m)
    assert holds(world, "obj_at", "item_2", "kitting_table_0") and holds(world, "obj_at", "item_5", "kitting_table_0")
    # the human never shows a task to the world
    assert world.agent_states[H].current_task is None


def test_at_pick_up_drop_abandons_and_keeps_the_item():
    m = model_for("env_layout1", "scenario_10", Script([deliver("item_2").at(pick_up, drop), deliver("item_5")]))
    h = run(m)
    assert kinds(h.record)[:3] == [
        ("entered", key(deliver("item_2")), None),
        ("left", key(deliver("item_2")), Outcome.ABANDONED),
        ("entered", key(deliver("item_5")), None),
    ]
    tick = next(t.tick for t in h.record.transitions if isinstance(t, Left))
    snap = next(s for s in h.record.snapshots if s.tick == tick)
    # the next delivery expanded with a return of the held item (deliver_with_return)
    assert h.carrying is None
    seq = [a for t, a, _ in action_sequence(h.record) if t == key(deliver("item_5"))]
    assert seq == ["move_to", "place", "move_to", "pick_up", "move_to", "place"]
    world = build_world_state(m)
    assert holds(world, "obj_at", "item_2", "shelf_1") or world.object_locations["item_2"] != "kitting_table_0"


def test_during_walk_cuts_and_resumes_from_the_position():
    script = Script([deliver("item_2").during(move_to, "PT6S", st("PT10S"), occurrence=0), deliver("item_5")])
    m = model_for("env_layout1", "scenario_10", script)
    h = m.humans[H]
    positions = []
    for _ in range(12):
        m.step()
        positions.append(h.pos)
    rec = h.record
    started = next(t for t in rec.transitions if isinstance(t, Started))
    assert started.tick == 3 and started.where == Cut(started.where.action, 0, 3)
    assert started.where.action.action_name == "move_to"
    # three steps walked, five ticks standing (PT10S) and the stand's
    # acknowledgement tick, then the walk goes on from there
    assert positions[2] == positions[3] == positions[8] and positions[8] != positions[9]
    assert [(s.done, s.total) for s in rec.snapshots if s.tick in (2, 3, 8, 9)] == [(3, 32), (1, 5), (5, 5), (4, 32)]
    assert [t.tick for t in rec.transitions if isinstance(t, Resumed)] == [9]
    run(m)
    assert holds(build_world_state(m), "obj_at", "item_2", "kitting_table_0")


def test_during_stand_keeps_the_remaining_stands():
    long, short = st("PT20S"), st("PT4S")
    m = model_for("env_layout0", "scenario_00", Script([long.during(stand, "PT4S", short)]), robot=False)
    h = run(m)
    outer = [(s.done, s.total) for s in h.record.snapshots if s.stack and s.stack[0] is long]
    assert outer == [(1, 10), (2, 10)] + [(k, 10) for k in range(3, 11)] + [(10, 10)]
    inner = [(s.done, s.total) for s in h.record.snapshots if s.stack and s.stack[0] is short]
    assert inner == [(1, 2), (2, 2), (2, 2)]
    assert [k[2] for k in kinds(h.record) if k[0] == "left"] == [Outcome.SUSPENDED, Outcome.COMPLETED, Outcome.COMPLETED]


def test_during_wait_at_keeps_the_countdown_and_records_waited():
    m = model_for("env_layout1", "scenario_10", Script([coffee().during(wait_at, "PT10S", st("PT4S"))]), robot=False)
    h = run(m)
    waits = [(s.done, s.total) for s in h.record.snapshots if s.action is not None and s.action.action_name == "wait_at"]
    assert waits[:5] == [(1, 30), (2, 30), (3, 30), (4, 30), (5, 30)] and waits[5] == (6, 30) and waits[-1] == (30, 30)
    assert holds(build_world_state(m), "waited", H, "coffee_machine_0")
    assert kinds(h.record)[-1] == ("left", key(coffee()), Outcome.COMPLETED)


def test_second_start_is_refused_and_recorded():
    d, c, s4 = deliver("item_2"), coffee(), st("PT4S")
    m = model_for("env_layout1", "scenario_10", Script([d.at(pick_up, c)]), robot=False)
    h = m.humans[H]
    while not any(isinstance(t, Started) for t in h.record.transitions):
        m.step()
    m.step()
    before = [(s.done, s.total) for s in h.record.snapshots][-1]
    h.inject(Start(s4))
    m.step()
    tick = int(m.schedule.steps) - 1
    assert h.record.transitions_at(tick) == [Refused(tick, Start(s4), RefusalReason.STACK_FULL)]
    assert h.machine.stack_tasks() == [c, d]
    after = [(s.done, s.total) for s in h.record.snapshots][-1]
    assert after == (before[0] + 1, before[1])          # the body was not stopped
    run(m)


def test_inject_start_drop_and_empty_stack():
    m = model_for("env_layout1", "scenario_10", Script([deliver("item_2")]), robot=False)
    h = m.humans[H]
    for _ in range(5):
        m.step()
    h.inject(Start(st("PT4S")))                                # a cut inside the walk, five steps in
    m.step()
    t = int(m.schedule.steps) - 1
    assert kinds(h.record)[-2:] == [("left", key(deliver("item_2")), Outcome.SUSPENDED), ("started", key(st("PT4S")), "Now")]
    assert h.record.transitions[-1].where == Cut(h.record.transitions[-1].where.action, 0, 5)
    h.inject(drop)                                            # drops the stand; the delivery resumes its walk
    m.step()
    t = int(m.schedule.steps) - 1
    assert kinds(h.record)[-2:] == [("left", key(st("PT4S")), Outcome.ABANDONED), ("resumed", key(deliver("item_2")), None)]
    assert h.record.snapshots[-1].action.action_name == "move_to" and h.record.snapshots[-1].done == 6
    run(m)
    h.inject(drop)                                            # nothing to drop
    m.step()
    t = int(m.schedule.steps) - 1
    assert h.record.transitions_at(t) == [Refused(t, Drop(), RefusalReason.EMPTY_STACK)]
    s4 = st("PT4S")
    h.inject(Start(s4))                                       # a plain entry on the empty stack
    m.step()
    t = int(m.schedule.steps) - 1
    assert h.record.transitions_at(t) == [Started(t, s4, Now(), None)]
    for _ in range(3):
        m.step()
    assert kinds(h.record)[-1] == ("left", key(st("PT4S")), Outcome.COMPLETED)


def test_start_on_the_last_action_runs_after_completion():
    m = model_for("env_layout1", "scenario_10", Script([deliver("item_2").at(place, coffee()), deliver("item_5")]), robot=False)
    h = run(m)
    assert kinds(h.record)[:4] == [
        ("entered", key(deliver("item_2")), None),
        ("left", key(deliver("item_2")), Outcome.COMPLETED),
        ("started", key(coffee()), "AfterAction"),
        ("left", key(coffee()), Outcome.COMPLETED),
    ]
    assert not any(k[2] is Outcome.SUSPENDED for k in kinds(h.record))


# ---------------------------------------------------------------------------
# an infeasible resumption: the machine against a world that diverged
# ---------------------------------------------------------------------------

def _carry_tree():
    """kitting's tree plus a task whose only method needs the item in hand."""
    kit = register_kitting_domain()
    item, target, agent = Var("?item"), Var("?target"), Var("?agent")
    carry = PersonalTask(name="carry_to", parameters=[item, target],
                         parameter_types={"?item": "item", "?target": "kitting_table"},
                         methods=[MethodSchema("carry_held", [item, target], [ConditionSchema("holding", (agent, item))],
                                               [ActionStep(move_to, {target: target}), ActionStep(place, {item: item, target: target})])])
    tree = Tree(tasks=kit.task_schemas() + [carry], actions=kit.get_all_actions(), microactions=kit.get_microactions())
    return tree, carry


def test_infeasible_resumption_is_recorded_and_the_executor_moves_on():
    tree, carry = _carry_tree()
    m = model_for("env_layout0", "scenario_00", Script([deliver("item_3")]), robot=False)
    world = build_world_state(m)
    held = replace(world, predicates=world.predicates | {Predicate("holding", (Const(H), Const("item_3")))},
                   object_locations={**world.object_locations, "item_3": H})
    task = TaskInstance(schema=carry, bindings={Var("?item"): Const("item_3"), Var("?target"): Const("kitting_table_0")})
    record = Record()
    machine = StackMachine(Script([task, st("PT4S")]), AdaptivePlanner(knowledge=tree), H, lambda d: TICKS[d], record)
    nxt = machine.next(held, 0)
    assert isinstance(nxt, RunAction) and nxt.action.action_name == "move_to"
    machine.inject(Start(st("PT2S")), held, 1, 2)             # cut two steps into the walk
    assert isinstance(machine.next(held, 1), RunAction)
    machine.action_done(held, 2)                              # the stand is done: carry_to resumes, the walk first
    assert machine.next(held, 3).cut.done == 2
    machine.action_done(world, 4)                             # the walk done, in a world where the item is not held
    assert isinstance(machine.next(world, 5), RunAction)      # the next entry runs
    assert kinds(record) == [
        ("entered", key(task), None),
        ("left", key(task), Outcome.SUSPENDED), ("started", key(st("PT2S")), "Now"),
        ("left", key(st("PT2S")), Outcome.COMPLETED), ("resumed", key(task), None),
        ("left", key(task), Outcome.INFEASIBLE),
        ("entered", key(st("PT4S")), None),
    ]


# ---------------------------------------------------------------------------
# the load-time check
# ---------------------------------------------------------------------------

def load(layout, sid, script):
    return model_for(layout, sid, script, robot=False)


def test_ambiguous_anchor_needs_an_occurrence():
    with pytest.raises(ValueError, match="scenario 'scenario_test', agent 'human_0'.*anchor_ambiguous"):
        load("env_layout1", "scenario_10", Script([deliver("item_2").at(move_to, coffee())]))
    m = load("env_layout1", "scenario_10", Script([deliver("item_2").at(move_to, coffee(), occurrence=1)]))
    h = run(m)
    started = next(t for t in h.record.transitions if isinstance(t, Started))
    assert started.where == Boundary(started.where.action, 1) and started.where.action.action_name == "move_to"
    with pytest.raises(ValueError, match="anchor_out_of_range"):
        load("env_layout1", "scenario_10", Script([deliver("item_2").at(move_to, coffee(), occurrence=2)]))


def _grab_tree():
    """kitting's tree plus a task that takes an item in hand."""
    kit = register_kitting_domain()
    item = Var("?item")
    grab = PersonalTask(name="grab", parameters=[item], parameter_types={"?item": "item"},
                        methods=[MethodSchema("grab_default", [item], [],
                                              [ActionStep(move_to, {Var("?target"): item}), ActionStep(pick_up, {item: item})])])
    tree = Tree(tasks=kit.task_schemas() + [grab], actions=kit.get_all_actions(), microactions=kit.get_microactions())
    return tree, grab


def test_anchor_absent_from_the_re_expansion_is_a_load_error():
    # a grab during the fetch walk leaves the item in hand: the delivery resumes
    # as deliver_already_held, and its pick_up anchor is absent
    tree, grab = _grab_tree()
    base = domain_config["scenarios"]["scenario_10"]
    human = next(a for a in base.agents if a.agent_type == "human")
    took = TaskInstance(schema=grab, bindings={Var("?item"): Const("item_2")})

    def model(script):
        cfg = AgentConfig(agent_id=H, agent_type="human", start_position=human.start_position, scheduled_tasks=script)
        scenario = ScenarioConfig(id="scenario_test", description="t", agents=[cfg],
                                  setup=base.setup, reference_layouts=base.reference_layouts)
        return SimModel(scenario=scenario, register_fn=lambda: tree,
                        task_model_schemas=domain_config["task_model"],
                        layout_path=domain_config["layouts"]["env_layout1"],
                        setup_path=domain_config["setups"][base.setup])

    with pytest.raises(ValueError, match="anchor_absent"):
        model(Script([deliver("item_2").at(move_to, took, occurrence=0).at(pick_up, st("PT2S"))]))
    # an anchor the re-expansion still has is fine, and fires there
    h = run(model(Script([deliver("item_2").at(move_to, took, occurrence=0).at(place, st("PT2S"), occurrence=0)])))
    assert [k for k in kinds(h.record) if k[0] == "started"] == [("started", key(took), "AfterAction"), ("started", key(st("PT2S")), "AfterAction")]
    assert [a for t, a, _ in action_sequence(h.record) if t == key(deliver("item_2"))] == ["move_to", "move_to", "place"]


def test_during_outside_its_action_is_a_load_error():
    with pytest.raises(ValueError, match="past_action"):
        load("env_layout1", "scenario_10", Script([deliver("item_2").during(pick_up, "PT2S", st("PT2S"))]))
    with pytest.raises(ValueError, match="past_action"):
        load("env_layout0", "scenario_00", Script([st("PT4S").during(stand, "PT10S", st("PT2S"))]))
    with pytest.raises(ValueError, match="past_action"):
        load("env_layout1", "scenario_10", Script([deliver("item_2").during(move_to, "PT2M", st("PT2S"), occurrence=0)]))
    with pytest.raises(ValueError, match="not a duration"):
        load("env_layout1", "scenario_10", Script([deliver("item_2").during(move_to, "soon", st("PT2S"), occurrence=0)]))


def test_drop_after_the_last_action_and_never_reached_anchors_are_load_errors():
    with pytest.raises(ValueError, match="refused:drop:empty_stack"):
        load("env_layout1", "scenario_10", Script([deliver("item_2").at(place, drop)]))
    with pytest.raises(ValueError, match="never_reached"):
        load("env_layout1", "scenario_10", Script([deliver("item_2").at(pick_up, drop).at(place, coffee())]))


def test_ill_typed_tasks_in_a_script_are_load_errors():
    with pytest.raises(ValueError, match="not an object of this layout"):
        load("env_layout0", "scenario_00", Script([deliver("item_3").at(pick_up, goto("window"))]))
    with pytest.raises(ValueError, match="not a duration"):
        load("env_layout0", "scenario_00", Script([st("soon")]))


def test_infeasible_at_load_is_an_error():
    tree, carry = _carry_tree()
    m = load("env_layout0", "scenario_00", Script([deliver("item_3")]))
    task = TaskInstance(schema=carry, bindings={Var("?item"): Const("item_3"), Var("?target"): Const("kitting_table_0")})
    with pytest.raises(ValueError, match="infeasible"):
        check_script(Script([task]), AdaptivePlanner(knowledge=tree), build_world_state(m), H,
                     lambda d: TICKS[d], lambda a, b: [b])


# ---------------------------------------------------------------------------
# the replay is the run
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("script", [
    Script([deliver("item_2").at(pick_up, coffee()), deliver("item_5")]),
    Script([deliver("item_2").at(pick_up, drop), deliver("item_5")]),
    Script([deliver("item_2").during(move_to, "PT6S", st("PT10S"), occurrence=0).during(move_to, "PT10S", st("PT4S"), occurrence=1)]),
    Script([coffee().during(wait_at, "PT10S", st("PT4S")), deliver("item_2").at(place, coffee())]),
])
def test_replay_equals_run(script):
    m = model_for("env_layout1", "scenario_10", script, robot=False)
    h = m.humans[H]
    from mesa_sim.action_decomposer import _parse_duration_to_steps, _get_step_size, steps_toward
    replay = check_script(script, h.machine.planner, build_world_state(m), H,
                          lambda d: _parse_duration_to_steps(d, m),
                          lambda a, b: [mu.params["target_pos"] for mu in steps_toward(a, b, _get_step_size(m))])
    run(m)
    assert kinds(replay) == kinds(h.record)
    assert action_sequence(replay) == action_sequence(h.record)


# ---------------------------------------------------------------------------
# the robot's inputs carry nothing of the stack
# ---------------------------------------------------------------------------

HIDDEN = (TaskInstance, Event, Trigger, Decision, Frame, Record, Snapshot, Transition, StackMachine)


def _walk(value, seen=None):
    seen = seen if seen is not None else set()
    if id(value) in seen:
        return
    seen.add(id(value))
    assert not isinstance(value, HIDDEN), f"{type(value).__name__} reached the robot's input"
    if is_dataclass(value):
        for f in fields(value):
            _walk(getattr(value, f.name), seen)
    elif isinstance(value, dict):
        for k, v in value.items():
            _walk(k, seen); _walk(v, seen)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for v in value:
            _walk(v, seen)


def test_world_state_and_observation_expose_nothing_of_the_stack():
    m = model_for("env_layout1", "scenario_10", Script([deliver("item_2").at(pick_up, coffee())]))
    h = m.humans[H]
    while len(h.machine.stack) < 2:
        m.step()
    world = build_world_state(m)
    obs = build_observation(h, m, float(m.schedule.steps))
    _walk(world)
    _walk(obs)
    assert world.agent_states[H].current_task is None and h.current_task is None
    assert {f.name for f in fields(WorldState)} == {"timestamp", "agent_states", "agent_positions", "object_locations",
                                                    "predicates", "object_zones", "object_home_container",
                                                    "object_destination", "object_positions", "metadata"}
    assert world.agent_states[H].metadata == {} and world.metadata == {}


# ---------------------------------------------------------------------------
# the four homes: world/ imports shared/ only, shared/ imports no side
# ---------------------------------------------------------------------------

def test_world_imports_shared_only():
    import re
    root = Path(__file__).parent.parent
    for module in (root / "world").glob("*.py"):
        for line in module.read_text().splitlines():
            m = re.match(r"\s*(?:from|import)\s+([\w.]+)", line)
            if m:
                top = m.group(1).split(".")[0]
                assert top in {"shared", "world", "typing", "dataclasses", "enum"}, f"{module.name}: {line.strip()}"
    for module in (root / "shared").glob("*.py"):
        for line in module.read_text().splitlines():
            m = re.match(r"\s*(?:from|import)\s+([\w.]+)", line)
            assert not m or m.group(1).split(".")[0] not in {"world", "mesa_sim", "ros_sim", "domains"}, \
                f"{module.name}: {line.strip()}"
