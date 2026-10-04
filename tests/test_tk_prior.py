# tests/test_tk_prior.py
"""
T-K part 1, build stage 5: the prior from context knowledge, checked against docs/context_knowledge_method.md
(the plan, section 4, requirement 5). Framework-wide. Every expected value is the method document's: section 10's
eight rows (kitting's declared values: suppressed 0.005, ordinary 0.02, coffee_break raised 2, ac_activation raised
0.5), section 4's order (the suppressing condition first), section 11's beliefs (0.825 in state 2, 0.926 in state 1),
section 12's state 7 (0.8 against 0.2; the 0.77 example), section 13 (context knowledge off: the belief is the
normalised evidence exactly), AM4 (a strength <= 0 and a foreseeable task without an entry are refused). Then the
recognizer with context knowledge on (belief = normalise(prior x evidence)), the memory of observed completions on a
recorded run (AM47: the recency fact holds on exactly 90 ticks from the observed completion), a robot with context
knowledge on in every registered scenario of both domains, and that the three shared modules name no task, fact,
object or domain in a code string.
Run from the repo root:  PYTHONHASHSEED=0 python -m pytest tests/test_tk_prior.py
"""

import ast
import dataclasses
import math
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "mesa_sim"))

from shared.knowledge import Condition, ContextKnowledge, ForeseeableKnowledge, Strength, TaskModel, TimelineFact
from shared.recognizer import build_hypothesis_space, context_prior, IntentionRecognizer
from shared.types import Const, Predicate, StrengthLevel, Timeline
from domains.kitting import facts
from domains.kitting.registry import domain_config as kitting, register_kitting_domain
from domains.kitting.tasks import ac_activation, coffee_break, deliver_item
from domains.dock_loading.registry import domain_config as dock
from mesa_sim.sim_model import SimModel
from mesa_sim.world_state_builder import build_world_state
from tests.kitting.test_td1_adequacy import H, obs, recognizer
from tests.kitting.test_th1_tree import model_for, registered

CK = kitting["context_knowledge"]
BREAK, WARM, AC_ON = Predicate("break_time", ()), Predicate("room_warm", ()), Predicate("ac_on", (Const("ac_switch_0"),))
COFFEE, AC = "coffee_break(?coffee_machine=coffee_machine_0)", "ac_activation(?ac_switch=ac_switch_0)"


def prior(n_deliveries, predicates, recent=()):
    """The prior of section 10's room: n live deliveries, one coffee machine, one A/C switch; pi per key."""
    work = [f"deliver_item(?item=item_{i})" for i in range(n_deliveries)]
    groups = [([COFFEE], CK.strength(coffee_break, set(predicates), recent).value),
              ([AC], CK.strength(ac_activation, set(predicates), recent).value)]
    w = context_prior(work, groups)
    z = sum(w.values())
    return {k: v / z for k, v in w.items()}


# ---------------------------------------------------------------- section 10: the eight rows

ROWS = [  # (live deliveries, predicates, recent, each delivery, coffee, A/C)
    (3, (), (), 0.321, 0.019, 0.019),                     # 1 start, no fact holds
    (3, (BREAK,), (), 0.110, 0.662, 0.007),               # 2 break time begins
    (3, (BREAK,), (coffee_break,), 0.325, 0.005, 0.020),  # 3 coffee break observed complete, break time still holds
    (2, (WARM,), (), 0.329, 0.013, 0.329),                # 4 break time over, recency passed, one delivery done, room warm
    (2, (WARM, AC_ON), (), 0.488, 0.020, 0.005),          # 5 the human switched the A/C on, room still warm
    (1, (WARM, AC_ON), (), 0.976, 0.020, 0.005),          # 6 one delivery left
    (0, (AC_ON,), (), None, 0.8, 0.2),                    # 7 no delivery left, A/C on
    (3, (BREAK, WARM), (), 0.095, 0.571, 0.143),          # 8 break time and room warm, A/C off
]


@pytest.mark.parametrize("n,preds,recent,each,coffee,ac", ROWS)
def test_section_10_rows(n, preds, recent, each, coffee, ac):
    pi = prior(n, preds, recent)
    assert math.isclose(sum(pi.values()), 1.0, abs_tol=1e-12)
    assert abs(pi[COFFEE] - coffee) <= 5e-4 and abs(pi[AC] - ac) <= 5e-4
    for i in range(n):
        assert abs(pi[f"deliver_item(?item=item_{i})"] - each) <= 5e-4
    assert len(pi) == n + 2


def test_section_4_the_suppressing_condition_is_tested_first():
    assert CK.level(coffee_break, {BREAK}, (coffee_break,)) is StrengthLevel.SUPPRESSED          # row 3
    assert CK.level(ac_activation, {WARM, AC_ON}, ()) is StrengthLevel.SUPPRESSED                # row 5
    assert CK.level(coffee_break, {BREAK}, ()) is StrengthLevel.RAISED
    assert CK.level(coffee_break, set(), ()) is StrengthLevel.ORDINARY
    assert CK.strength(coffee_break, {BREAK}, ()).value == 2.0 and CK.strength(ac_activation, {WARM}, ()).value == 0.5
    assert CK.suppressed.value == 0.005 and CK.ordinary.value == 0.02


# ---------------------------------------------------------------- sections 11 and 12: from the prior to the belief

def belief(pi, evidence):
    unnorm = {k: pi[k] * evidence[k] for k in pi}
    z = sum(unnorm.values())
    return {k: v / z for k, v in unnorm.items()}


def test_section_11_the_invented_evidence():
    evidence = {"deliver_item(?item=item_0)": 0.90, "deliver_item(?item=item_1)": 0.04, "deliver_item(?item=item_2)": 0.03,
                COFFEE: 0.02, AC: 0.01}
    assert abs(belief(prior(3, (BREAK,)), evidence)["deliver_item(?item=item_0)"] - 0.825) <= 5e-4   # state 2
    assert abs(belief(prior(3, ()), evidence)["deliver_item(?item=item_0)"] - 0.926) <= 5e-4         # state 1


def test_section_12_no_assigned_task_live():
    pi = prior(0, (AC_ON,))
    assert math.isclose(pi[COFFEE], 0.8) and math.isclose(pi[AC], 0.2)
    b = belief(pi, {COFFEE: 0.45, AC: 0.55})
    assert abs(b[COFFEE] - 0.36 / 0.47) <= 1e-9 and abs(b[COFFEE] - 0.77) <= 5e-3
    assert math.isclose(prior(0, ())[COFFEE], 0.5)      # both ordinary: 0.5 and 0.5, as without context knowledge


# ---------------------------------------------------------------- section 13 and AM4

@pytest.fixture(scope="module")
def model():
    return model_for("env_layout_01", registered("env_layout_01", "scenario_s01_01"))


def test_section_13_context_knowledge_off_is_the_normalised_evidence_exactly(model):
    w = build_world_state(model)
    hyps = build_hypothesis_space(next(iter(model.robots.values())).recognizer.task_model, model._objects_by_type)
    rec = recognizer(model, hyps)                       # context=None
    x, y = w.agent_positions[H]
    for t in range(12):
        b = rec.update(obs(t, (x - 10.0 * t, y - 5.0 * t)), w)
        assert b.belief == rec._evidence                # dict equality: the same values bit for bit (P1)
        assert b.prior == {} and b.levels == {}


def test_am4_a_strength_at_or_below_zero_is_refused():
    for v in (0.0, -1.0, -0.005):
        with pytest.raises(ValueError, match="greater than zero"):
            Strength(v, "test")


def test_am4_a_foreseeable_task_without_an_entry_is_refused(model):
    robot = next(iter(model.robots.values()))
    only_coffee = ContextKnowledge(CK.suppressed, CK.ordinary, [CK.entry(coffee_break)])
    with pytest.raises(ValueError, match=r"declares nothing for the foreseeable tasks \['ac_activation'\]"):
        only_coffee.check_against(robot.recognizer.task_model)
    with pytest.raises(ValueError, match="declares nothing for the foreseeable tasks"):
        IntentionRecognizer(task_model=robot.recognizer.task_model, context=only_coffee,
                            hypotheses=build_hypothesis_space(robot.recognizer.task_model, model._objects_by_type),
                            beta=0.01, speed=20.0, duration_to_steps=float, default_action_cost=1.0,
                            action_completion_latency=1.0, observed_task_completion_latency=0.0, alpha=0.05)


def test_a_condition_naming_a_recency_fact_without_a_duration_is_refused():
    from shared.knowledge import RecencyFact
    bad = ForeseeableKnowledge(task=ac_activation, suppressing=Condition((RecencyFact(coffee_break),)))
    with pytest.raises(ValueError, match="declares no recency duration"):
        ContextKnowledge(CK.suppressed, CK.ordinary, [bad])


# ---------------------------------------------------------------- the recognizer with context knowledge on

def test_the_belief_is_the_prior_times_the_evidence_normalised():
    model = model_for("env_layout_02", registered("env_layout_02", "scenario_s02_01"))   # a coffee machine, an A/C switch
    w = build_world_state(model)
    robot = next(iter(model.robots.values()))
    hyps = build_hypothesis_space(robot.recognizer.task_model, model._objects_by_type)
    human = next(a for a in registered("env_layout_02", "scenario_s02_01").agents if a.agent_type == "human")
    rec = IntentionRecognizer(task_model=robot.recognizer.task_model, context=CK, hypotheses=hyps,
                              beta=0.01, speed=20.0, duration_to_steps=float, default_action_cost=1.0,
                              action_completion_latency=1.0, observed_task_completion_latency=0.0, alpha=0.05,
                              assigned_tasks=human.assigned_tasks)
    x, y = w.agent_positions[H]
    with pytest.raises(ValueError, match="requires the recency facts"):
        rec.update(obs(0, (x, y)), w)
    for t in range(15):
        world = w if t < 8 else w.__class__(**{**w.__dict__, "predicates": set(w.predicates) | {BREAK}})
        b = rec.update(obs(t, (x - 10.0 * t, y - 5.0 * t)), world, recent=())
        assert set(b.prior) == set(rec._evidence) == set(b.belief)
        assert math.isclose(sum(b.prior.values()), 1.0, abs_tol=1e-12)
        expected = belief(b.prior, rec._evidence)
        for k in expected:
            assert math.isclose(b.belief[k], expected[k], rel_tol=1e-12), (t, k)
        assert b.confidence == b.belief[b.most_likely]
        assert b.levels["coffee_break"] is (StrengthLevel.RAISED if t >= 8 else StrengthLevel.ORDINARY)
        work = [k for k in b.prior if k.startswith("deliver_item")]
        assert math.isclose(b.prior[COFFEE] / (sum(b.prior[k] for k in work)), 2.0 if t >= 8 else 0.02)   # s = pi(f) / pi(A)


# ---------------------------------------------------------------- the memory on a recorded run (AM47)

def test_the_recency_fact_holds_on_exactly_90_ticks_from_the_observed_completion():
    sid = "scenario_s15_02"                     # round 1: the coffee break completes at 139 (its README)
    # its timeline stated empty: the setup's default break_time (step 4) would raise the level from 229
    cfg = dataclasses.replace(kitting["scenarios"][sid], timeline=Timeline(()))
    m = SimModel(scenario=cfg, register_fn=register_kitting_domain, task_model_schemas=kitting["task_model"],
                 layout_path=kitting["layouts"]["env_layout_17"], setup_path=kitting["setups"][cfg.setup],
                 state_declarations=kitting["states"], timeline_declarations=kitting["timeline_facts"],
                 declared_context=CK, assignment_knowledge=True, context_knowledge=True)
    robot = next(iter(m.robots.values()))
    recent, levels = {}, {}
    for t in range(240):
        m.step()
        recent[t] = [x.name for x in robot.memory.recent(t)]
        levels[t] = robot.belief.levels.get("coffee_break")
    assert robot.memory.completion_of(coffee_break) == 139
    assert [t for t in recent if recent[t] == ["coffee_break"]] == list(range(139, 229))   # 90 ticks, 139 included
    assert all(recent[t] == [] for t in list(range(0, 139)) + list(range(229, 240)))
    # retired on 139 and 140 (its terminal fact holds: no level), suppressed from its re-entry at 141 to 228
    assert levels[139] is None and levels[140] is None
    assert all(levels[t] is StrengthLevel.SUPPRESSED for t in range(141, 229))
    assert levels[229] is StrengthLevel.ORDINARY and levels[138] is StrengthLevel.ORDINARY


# ---------------------------------------------------------------- every registered scenario loads with it on

@pytest.mark.parametrize("domain", [kitting, dock])
def test_a_robot_with_context_knowledge_on_loads_in_every_registered_scenario(domain):
    n = 0
    for sid, cfg in domain["scenarios"].items():
        SimModel(scenario=cfg, register_fn=domain["register_fn"], task_model_schemas=domain["task_model"],
                 layout_path=domain["layouts"][cfg.reference_layouts[0]], setup_path=domain["setups"][cfg.setup],
                 state_declarations=domain["states"], timeline_declarations=domain["timeline_facts"],
                 declared_context=domain["context_knowledge"], assignment_knowledge=True, context_knowledge=True)
        n += 1
    assert n > 0


def test_dock_loadings_declarations_cover_its_task_model():
    tm = TaskModel(dock["register_fn"](), dock["task_model"])
    dock["context_knowledge"].check_against(tm)
    assert {e.task.name for e in dock["context_knowledge"].entries()} == {"coffee_break", "ac_activation", "office_break"}


# ---------------------------------------------------------------- no domain word in the shared modules' code strings

NAMES = ("coffee", "ac_", "break", "office", "kitting", "dock", "item", "shelf", "pallet", "warm", "deliver",
         "scan", "switch", "table")


def code_strings(path):
    """Every string constant in the module's code, docstrings excluded."""
    tree = ast.parse(path.read_text())
    doc_ids = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
                doc_ids.add(id(first.value))
    return [n.value for n in ast.walk(tree)
            if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in doc_ids]


@pytest.mark.parametrize("module", ["shared/recognizer.py", "shared/knowledge.py", "shared/completion_memory.py"])
def test_the_shared_modules_name_no_task_fact_object_or_domain(module):
    hits = [s for s in code_strings(ROOT / module) if any(w in s.lower() for w in NAMES)]
    assert hits == [], hits
