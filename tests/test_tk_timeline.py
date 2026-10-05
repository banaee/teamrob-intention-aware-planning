# tests/test_tk_timeline.py
"""
T-K part 1, build stage 4a: the timeline of context facts (AM34, AM40, AM46, AM50; AM20, AM52, AM54). Framework-wide.
- the form: a window is half-open in ticks, its end optional; two windows of one fact do not overlap;
- the resolution at load: the scenario's own timeline, stated empty, not stated with a setup timeline, a setup with
  none (the four cases of the plan's stage 4a), the source printed;
- the environment applies it as a function of the tick: the builder emits a timeline fact on exactly its window's
  ticks;
- each refusal at load: a timeline fact in an action's precondition, completion condition, effect or retraction, in a
  method's guard; in the setup's "states" block; an undeclared fact in a timeline; overlapping windows.
The declarations are a test's own (no domain declares a value here), on kitting's env_layout_01.
Run from the repo root:  PYTHONHASHSEED=0 python -m pytest tests/test_tk_timeline.py
"""

import dataclasses
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "mesa_sim"))

from shared.knowledge import Tree
from shared.types import (
    ActionSchema, ActionStep, ConditionSchema, MethodSchema, Predicate, ScenarioConfig, StateDeclaration, Timeline,
    TimelineSource, Var, Window, WorkTask,
)
from domains.kitting import actions
from domains.kitting.registry import domain_config, register_kitting_domain
from mesa_sim.sim_model import SimModel
from mesa_sim.world_state_builder import build_world_state

LAYOUT, SID = "env_layout_01", "scenario_s01_01"
WARM = StateDeclaration("warm_test", None)
BREAK = StateDeclaration("break_test", None)
DECLARED = [WARM, BREAK]


def setup_file(tmp_path, timeline=None, states=None):
    base = domain_config["scenarios"][SID].setup
    setup = json.load(open(domain_config["setups"][base]))
    if timeline is not None:
        setup["timeline"] = timeline
    if states is not None:
        setup["states"] = states
    path = tmp_path / "setup_test.json"
    path.write_text(json.dumps(setup))
    return str(path)


def model(setup_path=None, timeline=None, register_fn=register_kitting_domain, declared=DECLARED):
    scenario = domain_config["scenarios"][SID]
    if timeline is not None:
        scenario = dataclasses.replace(scenario, timeline=timeline)
    return SimModel(scenario=scenario, register_fn=register_fn, task_model_schemas=domain_config["task_model"],
                    layout_path=domain_config["layouts"][LAYOUT],
                    setup_path=setup_path or domain_config["setups"][scenario.setup],
                    timeline_declarations=declared, human_aware=True, intention_aware=True, assignment_knowledge=False, context_knowledge=False)


# ---------------------------------------------------------------- the form

def test_a_window_is_half_open_in_ticks():
    w = Window(WARM, 3, 6)
    assert [t for t in range(10) if w.holds_at(t)] == [3, 4, 5]
    assert [t for t in range(10) if Window(WARM, 7).holds_at(t)] == [7, 8, 9]
    assert Timeline((w, Window(BREAK, 0, 4))).facts_at(3) == {Predicate("warm_test", ()), Predicate("break_test", ())}
    assert Timeline((w,)).facts_at(6) == frozenset()


@pytest.mark.parametrize("start,end", [(-1, 5), (5, 5), (6, 5), (1.5, 4)])
def test_a_bad_window_is_refused(start, end):
    with pytest.raises(ValueError):
        Window(WARM, start, end)


def test_overlapping_windows_of_one_fact_are_refused():
    with pytest.raises(ValueError, match="overlap"):
        Timeline((Window(WARM, 0, 10), Window(WARM, 9, 20)))
    with pytest.raises(ValueError, match="overlap"):
        Timeline((Window(WARM, 0), Window(WARM, 50, 60)))
    Timeline((Window(WARM, 0, 10), Window(WARM, 10, 20), Window(BREAK, 5, 15)))   # adjacent, and another fact


def test_a_window_on_a_state_about_an_object_is_refused():
    with pytest.raises(ValueError, match="about no object"):
        Window(StateDeclaration("ac_on", "ac_switch"), 0, 5)


# ---------------------------------------------------------------- the resolution at load

def test_the_scenarios_timeline_replaces_the_setups(tmp_path):
    path = setup_file(tmp_path, timeline=[{"fact": "warm_test", "from": 0}])
    m = model(path, timeline=Timeline((Window(BREAK, 2, 4),)))
    assert m.timeline_source is TimelineSource.SCENARIO
    assert m.timeline == Timeline((Window(BREAK, 2, 4),))


def test_a_scenario_stated_empty_has_no_timeline_fact(tmp_path):
    path = setup_file(tmp_path, timeline=[{"fact": "warm_test", "from": 0}])
    m = model(path, timeline=Timeline(()))
    assert m.timeline_source is TimelineSource.SCENARIO and m.timeline.windows == ()
    assert not any(p.name in ("warm_test", "break_test") for p in build_world_state(m).predicates)


def test_not_stated_the_setups_applies(tmp_path):
    path = setup_file(tmp_path, timeline=[{"fact": "warm_test", "from": 0, "until": 3}, {"fact": "break_test", "from": 2}])
    m = model(path)
    assert m.timeline_source is TimelineSource.SETUP
    assert m.timeline == Timeline((Window(WARM, 0, 3), Window(BREAK, 2)))


def test_a_setup_with_none_and_no_scenario_timeline():
    m = model()
    assert m.timeline_source is TimelineSource.NONE and m.timeline.windows == ()


def test_the_builder_emits_a_timeline_fact_on_its_windows_ticks(tmp_path):
    m = model(setup_file(tmp_path, timeline=[{"fact": "warm_test", "from": 2, "until": 4}]))
    seen = []
    for t in range(6):
        world = build_world_state(m)
        assert world.timestamp == t
        seen.append(Predicate("warm_test", ()) in world.predicates)
        m.step()
    assert seen == [False, False, True, True, False, False]


# ---------------------------------------------------------------- refusals at load

def test_an_undeclared_fact_in_a_timeline_is_refused(tmp_path):
    with pytest.raises(ValueError, match="not a timeline fact the domain declares"):
        model(setup_file(tmp_path, timeline=[{"fact": "cold_test", "from": 0}]))
    with pytest.raises(ValueError, match="not a timeline fact this domain declares"):
        model(timeline=Timeline((Window(StateDeclaration("cold_test", None), 0),)))


def test_overlapping_windows_in_a_setup_are_refused(tmp_path):
    with pytest.raises(ValueError, match="overlap"):
        model(setup_file(tmp_path, timeline=[{"fact": "warm_test", "from": 0, "until": 5},
                                             {"fact": "warm_test", "from": 4}]))


def test_the_states_block_refuses_a_timeline_fact(tmp_path):
    with pytest.raises(ValueError, match="stated by a timeline only"):
        model(setup_file(tmp_path, states=[{"state": "warm_test"}]))


def tree_with(action=None, task=None):
    """kitting's tree (its registry's own schemas), with one action schema replaced by `action` (same name) or one
    task schema added."""
    base = register_kitting_domain()
    acts = base.get_all_actions()
    ts = base.task_schemas()
    if action is not None:
        acts = [action if a.name == action.name else a for a in acts]

        def swap(schema):   # the methods must call the replacing object, by identity
            return dataclasses.replace(schema, methods=[dataclasses.replace(
                m, steps=[ActionStep(action, s.bindings) if s.action.name == action.name else s for s in m.steps])
                for m in schema.methods])
        ts = [swap(t) for t in ts]
    if task is not None:
        ts = ts + [task]
    return lambda: Tree(tasks=ts, actions=acts, microactions=base.get_microactions())


WARM_COND = ConditionSchema("warm_test", ())


@pytest.mark.parametrize("field,place", [("preconditions", "a precondition"), ("effects", "an effect"),
                                         ("retracts", "a retraction")])
def test_a_timeline_fact_in_an_action_list_is_refused(field, place):
    action = dataclasses.replace(actions.wait_at, **{field: list(getattr(actions.wait_at, field)) + [WARM_COND]})
    with pytest.raises(ValueError, match=f"action 'wait_at': {place} names the timeline fact 'warm_test'"):
        model(register_fn=tree_with(action=action))


def test_a_timeline_fact_as_a_completion_condition_is_refused():
    action = dataclasses.replace(actions.wait_at, completion=WARM_COND)
    with pytest.raises(ValueError, match="action 'wait_at': the completion condition names the timeline fact"):
        model(register_fn=tree_with(action=action))


def test_a_timeline_fact_in_a_guard_is_refused():
    guarded = WorkTask(name="warm_walk", parameters=[Var("?target")], parameter_types={"?target": "kitting_table"},
                       methods=[MethodSchema(name="warm_walk_default", parameters=[Var("?target")], guards=[WARM_COND],
                                             steps=[ActionStep(actions.move_to, {Var("?target"): Var("?target")})])])
    with pytest.raises(ValueError, match="task 'warm_walk', method 'warm_walk_default': a guard names the timeline"):
        model(register_fn=tree_with(task=guarded))
