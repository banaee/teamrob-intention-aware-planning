"""
mesa_sim/webui_adapter.py

PURPOSE:
    Mesa's piece for the web-ui (T-viz 0.4): implements webui/simulator.py's interface over Mesa. It produces the
    web-ui's three messages (webui/messages.py): the catalogue from the domain registry and the run file, the run
    description and the tick updates from one sim-run (mesa_sim/sim_run.py's SimRun, built through
    mesa_sim/run_config.py). It only reads the model: a sim-run with messages produced writes the same log pair as the
    same sim-run without (tests/test_tviz_messages.py).

WHAT THIS MODULE DOES:
    - MesaSimulator: the catalogue (with each domain's scene appearance, and the notes of its layouts and setups,
      T-viz 1a), and the build of a sim-run from the screen-user's choice. A choice that cannot be built raises
      BuildFailed and writes no log pair (T-viz 0.4, Q4)
    - The view of a layout, or of a layout and a setup at its start (T-viz 1a): read through the loader's own functions
      (mesa_sim/sim_model.py: read_layout, read_setup_objects, read_setup_states), translated by the same functions as
      a sim-run's run description and tick update; no model is built, nothing is written
    - MesaSimRun: one sim-run; per step its tick update; its end and its discard
    - A sim-run's log pair takes only the lines of the thread the server calls it on, and does not echo to the
      terminal (webui/simulator.py, ONE THREAD; mesa_sim/sim_run.py, RunLog)
    - Reads, per step, the robot-human distance the sim-run's [sep] lines printed (T-viz 1c), and gives every task its
      identity (task equality), by which the page colours it
    - Reads, per tick, the first tick at which every agent had finished (the tick update's `run`, T-viz 1a): every
      human's script ended (every entry closed, the stack empty) and every robot's task pool empty
    - Keeps per sim-run what the model does not hold and a page reload must not lose: the order in which movable
      objects arrived in each fixed object, and each agent's direction of its most recent step that moved it, from
      its own positions. Neither is a world fact; neither is written anywhere
    - Names, per human (T-viz 1a (iv)), the script entry each task on the stack runs and the entry a task that left it
      ran (from the executor's frames, matched by object identity: a frame's task is its entry's task object), the
      script event a switch fired or an unfired event is (by identity with the script's events), and the tag of the
      task on top (world/tag.py, the one definition the analyses read too, on the model's timeline and the human's
      record)
    - Reads, per robot (T-viz 1b), its body and its mind after each step, into the messages' robot section beside the
      world: the action at its plan's cursor with its progress, the hold its last decision carries (the executor's);
      the belief (RobotAgent.belief); the gate's answer for the leader, asked at its one home
      (MetaPlanner._clears_gate, as the test-beds ask it), after the question admission asks first (no human observed);
      the last decision (RobotAgent.last_decision) with the projection it rested on; the recency facts of its memory of
      observed completions. It keeps each robot's last decision and the hold's ticks stood, as it keeps the order of
      arrival

WHAT THIS MODULE DOES NOT DO:
    - No rule of the web-ui (which sim-run is current, the end at the configured steps, the lock): the server's
    - No server, no transport, no page
    - No decision: it compares nothing with θ and calls nothing of the robot's mind that changes it

RUN OPTIONS BY NAME (T-viz 0.4, Q3, a deliberate exception at the input boundary): the web-ui knows the run options
only as the catalogue declares them, each identified by its name, so that it stays independent of the simulator's
options. The choice's values are matched to the declarations by name here, once, and handed to run_configuration,
which validates them as it validates a run file.
"""

import json
import math
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

from mesa_sim.run_config import (BOOL_OPTIONS, DOMAIN_REGISTRY, EXPERIMENT_CONFIG_PATH, ONE_OF_OPTIONS,
                                 OPTION_DEFAULTS, RUN_OPTIONS, load_experiment, resolve_triple, run_configuration,
                                 user_args_parser)
from mesa_sim.action_decomposer import _parse_duration_to_steps
from mesa_sim.sim_model import (SimModel, SimObject, declared_states, read_layout, read_setup_objects,
                                read_setup_states)
from mesa_sim.sim_run import RunLog, SimRun
from shared.meta_planner import GateOutcome
from shared.types import (AdequacyFinding, AfterAction, DuringAction, Drop, Event, EvidenceRank, GroundedAction,
                          HypothesisAdequacy, Now, ObservationWarrant, RecognitionChange, RecognizerLifecycle,
                          ScriptDependence, Start, StrengthLevel, TaskInstance, TimelineSource, Trigger, goal_bindings,
                          same_task, task_instance_key)
from world import record as rec
from world.queries import truth_at
from world.tag import Stretches, recent_tasks, tag_at
from webui import messages as msg
from webui.appearance import Appearance
from webui.simulator import BuildFailed

ROOT = Path(__file__).resolve().parent.parent

# The run options that are not the triple, by kind. Every run option of run_config's RUN_OPTIONS is of one kind; one
# with none stops the catalogue (_declarations).
TRIPLE = ("domain", "layout", "scenario")
LEVEL_OPTIONS = ("test_level",)
LIMIT_OPTIONS = ("steps",)
LIMIT_MINIMUM = 1   # a step limit, when one is set, is at least one step

# Each run option's value in effect: the model's (SimModel applies the rules between them, T-F part 1, R5), the
# configured steps the run configuration's.
_EFFECTIVE: Dict[str, Callable[[SimModel, dict], object]] = {
    "steps": lambda model, config: config["steps"],
    "human_aware": lambda model, config: model.human_aware,
    "intention_aware": lambda model, config: model.intention_aware,
    "assignment_knowledge": lambda model, config: model.assignment_knowledge,
    "context_knowledge": lambda model, config: model.context_knowledge,
    "strategy": lambda model, config: model.strategy,
    "gate_strategy": lambda model, config: model.gate_strategy,
    "cost_strategy": lambda model, config: model.cost_strategy,
    "separation_stop": lambda model, config: model.separation_stop,
    "test_level": lambda model, config: model.test_level,
}

_VALUE_OF = {msg.SwitchOption: msg.SwitchValue, msg.OneOfOption: msg.OneOfValue,
             msg.LevelOption: msg.LevelValue, msg.LimitOption: msg.LimitValue}

_OUTCOME = {rec.Outcome.COMPLETED: msg.Outcome.COMPLETED, rec.Outcome.SUSPENDED: msg.Outcome.SUSPENDED,
            rec.Outcome.ABANDONED: msg.Outcome.ABANDONED, rec.Outcome.INFEASIBLE: msg.Outcome.INFEASIBLE}
_DECISION_REFUSAL = {rec.RefusalReason.STACK_FULL: msg.DecisionRefusalReason.STACK_FULL,
                     rec.RefusalReason.EMPTY_STACK: msg.DecisionRefusalReason.EMPTY_STACK}
_UNFIRED = {rec.UnfiredReason.ANCHOR_ABSENT: msg.UnfiredReason.ANCHOR_ABSENT,
            rec.UnfiredReason.ANCHOR_AMBIGUOUS: msg.UnfiredReason.ANCHOR_AMBIGUOUS,
            rec.UnfiredReason.ANCHOR_OUT_OF_RANGE: msg.UnfiredReason.ANCHOR_OUT_OF_RANGE,
            rec.UnfiredReason.NEVER_REACHED: msg.UnfiredReason.NEVER_REACHED,
            rec.UnfiredReason.PAST_ACTION: msg.UnfiredReason.PAST_ACTION}
_DEPENDENCE = {ScriptDependence.INDEPENDENT: msg.ScriptDependence.INDEPENDENT,
               ScriptDependence.ON_ROBOT: msg.ScriptDependence.ON_ROBOT}
_TIMELINE_SOURCE = {TimelineSource.SCENARIO: msg.TimelineSource.SCENARIO, TimelineSource.SETUP: msg.TimelineSource.SETUP,
                    TimelineSource.NONE: msg.TimelineSource.NONE}
_ENTRY_PART = {rec.OrdinaryRef: msg.EntryPart.ORDINARY, rec.RepeatableRef: msg.EntryPart.REPEATABLE,
               rec.ClosingRef: msg.EntryPart.CLOSING}

# The robot's mind (T-viz 1b), translated value by value.
_GATE = {GateOutcome.CLEARS: msg.Gate.CLEARS, GateOutcome.INTENTION_OFF: msg.Gate.INTENTION_OFF,
         GateOutcome.BELOW_THETA: msg.Gate.BELOW_THETA,
         GateOutcome.LEADER_NO_OBSERVATION: msg.Gate.LEADER_NO_OBSERVATION,
         GateOutcome.LEADER_INADEQUATE: msg.Gate.LEADER_INADEQUATE,
         GateOutcome.LEADER_UNWARRANTED: msg.Gate.LEADER_UNWARRANTED,
         GateOutcome.LEADER_OUTRANKED: msg.Gate.LEADER_OUTRANKED}
# A trigger's reason is a string in shared/types.py (TriggerDecision.reason): a closed table of the three triggers a
# fired decision names; an unknown one stops the piece (_robot_tick).
_TRIGGER = {"no_current_task": msg.TriggerKind.NO_CURRENT_TASK,
            "recognition_changed": msg.TriggerKind.RECOGNITION_CHANGED,
            "projection_expired": msg.TriggerKind.PROJECTION_EXPIRED}
_CAUSE = {RecognitionChange.ENTERED: msg.Cause.ENTERED, RecognitionChange.REPLACED: msg.Cause.REPLACED,
          RecognitionChange.BOUNDARY: msg.Cause.BOUNDARY, RecognitionChange.RETRACTION: msg.Cause.RETRACTION}
_LIFECYCLE = {RecognizerLifecycle.LIVE: msg.Lifecycle.LIVE, RecognizerLifecycle.EXHAUSTED: msg.Lifecycle.EXHAUSTED}
_FINDING = {AdequacyFinding.UNRESOLVED: msg.Finding.UNRESOLVED, AdequacyFinding.ADEQUATE: msg.Finding.ADEQUATE,
            AdequacyFinding.UNEXPLAINED: msg.Finding.UNEXPLAINED}
_ADEQUACY = {HypothesisAdequacy.ADEQUATE: msg.Adequacy.ADEQUATE, HypothesisAdequacy.INADEQUATE: msg.Adequacy.INADEQUATE,
             HypothesisAdequacy.NO_OBSERVATION: msg.Adequacy.NO_OBSERVATION}
_WARRANT = {ObservationWarrant.OBSERVATION: msg.Warrant.OBSERVATION, ObservationWarrant.NONE: msg.Warrant.NONE}
_RANK = {EvidenceRank.OUTRANKED: msg.Rank.OUTRANKED, EvidenceRank.NOT_OUTRANKED: msg.Rank.NOT_OUTRANKED}
_LEVEL = {StrengthLevel.SUPPRESSED: msg.Level.SUPPRESSED, StrengthLevel.ORDINARY: msg.Level.ORDINARY,
          StrengthLevel.RAISED: msg.Level.RAISED}


# =============================================================================
# The catalogue
# =============================================================================

def _declarations(run_file_config: dict, step_limit: Optional[int]) -> Tuple[msg.RunOptionDeclaration, ...]:
    """The run options in RUN_OPTIONS's order, the triple excluded, each of its kind, its default the run
    configuration's value or else OPTION_DEFAULTS's, its description the flag's help text. The step limit's default is
    `step_limit`, never the run file's steps: the web-ui has no step limit unless one is set (T-viz 1a, P11)."""
    help_of = {action.dest: action.help for action in user_args_parser()._actions}
    declarations = []
    for name in RUN_OPTIONS:
        if name in TRIPLE:
            continue
        if name in LIMIT_OPTIONS:
            if step_limit is not None and step_limit < LIMIT_MINIMUM:
                raise ValueError(f"{name}={step_limit}: a step limit is at least {LIMIT_MINIMUM}")
            declarations.append(msg.LimitOption(name=name, default=step_limit, minimum=LIMIT_MINIMUM,
                                                description=help_of[name]))
            continue
        default = run_file_config.get(name, OPTION_DEFAULTS[name])
        if name in BOOL_OPTIONS:
            declarations.append(msg.SwitchOption(name=name, default=default, description=help_of[name]))
        elif name in ONE_OF_OPTIONS:
            declarations.append(msg.OneOfOption(name=name, values=tuple(ONE_OF_OPTIONS[name]), default=default,
                                                description=help_of[name]))
        elif name in LEVEL_OPTIONS:
            declarations.append(msg.LevelOption(name=name, default=float(default), description=help_of[name]))
        else:
            raise ValueError(f"run option '{name}' has no kind for the web-ui's catalogue")
    return tuple(declarations)


def _value(declaration, value) -> msg.RunOptionValue:
    return _VALUE_OF[type(declaration)](name=declaration.name, value=value)


def _read_json(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def _layout_entry(layout_id: str, path: str) -> msg.LayoutEntry:
    space = _read_json(path)["space"]
    return msg.LayoutEntry(id=layout_id, title=space.get("name", layout_id), notes=space.get("notes"))


def _setup_entry(setup_id: str, path: str) -> msg.SetupEntry:
    return msg.SetupEntry(id=setup_id, notes=_read_json(path).get("notes"))


def appearance(domain: str) -> Appearance:
    """The domain's scene appearance, domains/<domain>/appearance.json, validated against webui/appearance.py; the
    defaults when the domain has no file. Not a world fact: the simulation never reads it. Every state a look by state
    names is a state the domain declares for the entry's object type (T-viz 1a (iii)); else ValueError."""
    path = ROOT / "domains" / domain / "appearance.json"
    look = Appearance.model_validate_json(path.read_text()) if path.is_file() else Appearance()
    check_looks_by_state(look, DOMAIN_REGISTRY[domain]["states"], f"{path.relative_to(ROOT)}")
    return look


def check_looks_by_state(look: Appearance, states, where: str) -> None:
    """Every state a look by state names is one of `states` (the domain's declarations) for the entry's object type;
    else ValueError naming `where`, the entry and the declared states."""
    declared = {d.name: d for d in states}
    for object_type, entry in list(look.fixed.items()) + list(look.movable.items()):
        for by_state in entry.states:
            declaration = declared.get(by_state.state)
            if declaration is None or declaration.object_type != object_type:
                raise ValueError(
                    f"{where}: the look of '{object_type}' names the state '{by_state.state}', which is not declared "
                    f"for type '{object_type}' (declared: "
                    f"{sorted((d.name, d.object_type) for d in declared.values() if d.object_type is not None)})")


def _domain_entry(name: str, domain: dict, look: Appearance) -> msg.DomainEntry:
    return msg.DomainEntry(
        name=name,
        layouts=tuple(_layout_entry(lid, path) for lid, path in domain["layouts"].items()),
        setups=tuple(_setup_entry(sid, path) for sid, path in domain["setups"].items()),
        scenarios=tuple(msg.ScenarioEntry(id=s.id, setup=s.setup, reference_layouts=tuple(s.reference_layouts),
                                          description=s.description)
                        for s in domain["scenarios"].values()),
        appearance=look,
    )


class MesaSimulator:
    """Mesa's side of the web-ui (webui.simulator.Simulator). `config` is the start's run configuration (the run file
    and the flags, run_config.load_experiment), from which the catalogue's defaults and its default choice come; by
    default the run file configs/experiment.yaml. `step_limit` is the default step limit (the web-ui's start: its
    --steps), None for none; the run file's steps is not used."""

    def __init__(self, config: Optional[dict] = None, step_limit: Optional[int] = None):
        self._run_file_config = load_experiment(EXPERIMENT_CONFIG_PATH, {}) if config is None else config
        self._declarations = _declarations(self._run_file_config, step_limit)
        # Each domain's scene appearance, checked once, at the start (ValueError: a state no type of it declares)
        self._appearances = {name: appearance(name) for name in DOMAIN_REGISTRY}

    def catalogue(self) -> msg.Catalogue:
        config = self._run_file_config
        _, layout_id, _, scenario = resolve_triple(config)
        default_choice = msg.SimRunChoice(
            domain=config["domain"], layout=layout_id, scenario=scenario.id,
            options=tuple(_value(d, d.default) for d in self._declarations))
        return msg.Catalogue(
            domains=tuple(_domain_entry(name, domain, self._appearances[name])
                          for name, domain in DOMAIN_REGISTRY.items()),
            run_options=self._declarations,
            default_choice=default_choice,
        )

    def build(self, choice: msg.SimRunChoice, sim_run: msg.SimRunId) -> "MesaSimRun":
        """The sim-run of `choice`, at its start. Its log pair is attached from here on (logging is process-wide: the
        caller ends or discards the current sim-run first). A choice that cannot be built raises BuildFailed and
        writes no log pair."""
        try:
            config = run_configuration(self._configuration(choice), "web-ui choice")
        except ValueError as e:
            raise BuildFailed(str(e)) from e
        log = RunLog(echo=False, own_thread_only=True)
        try:
            run = SimRun(config, log)
        except Exception as e:
            log.close()
            raise BuildFailed(str(e)) from e
        return MesaSimRun(sim_run, choice, run, self._declarations)

    def view(self, choice: msg.ViewChoice) -> msg.LayoutView:
        """The view of a layout, or of a layout and a setup at its start: the layout and the setup read and checked by
        the loader's functions, as a model built on them reads them. A layout or a setup that is not registered, or
        that the loader refuses, raises BuildFailed."""
        domain = DOMAIN_REGISTRY.get(choice.domain)
        if domain is None:
            raise BuildFailed(f"unknown domain '{choice.domain}'. Available: {list(DOMAIN_REGISTRY)}")
        layout_path = domain["layouts"].get(choice.layout)
        if layout_path is None:
            raise BuildFailed(f"unknown layout '{choice.layout}' for domain '{choice.domain}'")
        setup_path = None
        if choice.setup is not None:
            setup_path = domain["setups"].get(choice.setup)
            if setup_path is None:
                raise BuildFailed(f"unknown setup '{choice.setup}' for domain '{choice.domain}'")
        try:
            layout = read_layout(_read_json(layout_path), layout_path)
            setup = None
            if setup_path is not None:
                env_setup = _read_json(setup_path)
                movable = read_setup_objects(env_setup.get("env_objects", []), layout.fixed_objects,
                                             domain["register_fn"]().get_types_with_destination(), layout_path,
                                             setup_path)
                states, timeline_facts = declared_states(domain["states"], domain["timeline_facts"])
                facts = read_setup_states(env_setup.get("states", []), setup_path, {**layout.fixed_objects, **movable},
                                          states, timeline_facts)
                setup = msg.SetupView(
                    id=choice.setup,
                    movable_objects=tuple(_movable_object(m) for m in movable.values()),
                    fixed_object_contents=tuple(
                        msg.FixedObjectContents(fixed_object=fid, movable_objects=held)
                        for fid in layout.fixed_objects
                        for held in [tuple(mid for mid, m in movable.items() if m.home_container == fid)] if held),
                    object_states=_object_states(facts))
        except ValueError as e:
            raise BuildFailed(str(e)) from e
        return msg.LayoutView(
            domain=choice.domain, layout=choice.layout,
            space=_space(layout.display_name, layout.x_min, layout.x_max, layout.y_min, layout.y_max),
            areas=tuple(_area(a) for a in layout.areas),
            fixed_objects=tuple(_fixed_object(f) for f in layout.fixed_objects.values()),
            setup=setup)

    def _configuration(self, choice: msg.SimRunChoice) -> dict:
        """The run configuration's mapping of the choice: the triple, and one value per declared run option, matched
        by name (the exception at the input boundary, above); a value of another kind, a missing, repeated or
        undeclared option, or a limit below its minimum, is refused. No limit is the configuration's steps None."""
        declared = {d.name: d for d in self._declarations}
        config = {"domain": choice.domain, "layout": choice.layout, "scenario": choice.scenario}
        for value in choice.options:
            declaration = declared.get(value.name)
            if declaration is None:
                raise BuildFailed(f"run option '{value.name}' is not declared by the catalogue")
            if value.name in config:
                raise BuildFailed(f"run option '{value.name}' is given twice")
            if not isinstance(value, _VALUE_OF[type(declaration)]):
                raise BuildFailed(f"run option '{value.name}': a {declaration.kind} value is expected")
            if (isinstance(declaration, msg.LimitOption) and value.value is not None
                    and value.value < declaration.minimum):
                raise BuildFailed(f"run option '{value.name}': at least {declaration.minimum}")
            config[value.name] = value.value
        missing = [name for name in declared if name not in config]
        if missing:
            raise BuildFailed(f"run options without a value: {missing}")
        return config


# =============================================================================
# The translation of the world's and the record's types
# =============================================================================

def _task_ref(task: TaskInstance) -> msg.TaskRef:
    """A task; its identity (T-viz 1c) the key of the task its goal bindings name (task equality, same_task), the
    form of a hypothesis key."""
    return msg.TaskRef(task=task.schema.name,
                       bindings=tuple(msg.Binding(parameter=var.name, value=const.value)
                                      for var, const in task.bindings.items()),
                       label=task_instance_key(task),
                       identity=task_instance_key(TaskInstance(schema=task.schema, bindings=goal_bindings(task))))


def _action_ref(action: GroundedAction) -> msg.ActionRef:
    return msg.ActionRef(action=action.action_name,
                         bindings=tuple(msg.Binding(parameter=p, value=v) for p, v in action.bindings.items()))


def _trigger(trigger: Trigger) -> msg.Trigger:
    if isinstance(trigger, AfterAction):
        return msg.AfterActionTrigger(action=trigger.action.name, occurrence=trigger.occurrence)
    if isinstance(trigger, DuringAction):
        return msg.DuringActionTrigger(action=trigger.action.name, time=trigger.time, occurrence=trigger.occurrence)
    if isinstance(trigger, Now):
        return msg.NowTrigger()
    raise TypeError(f"unknown trigger {trigger!r}")


def _decision(decision) -> msg.Decision:
    if isinstance(decision, Start):
        return msg.StartDecision(task=_task_ref(decision.task))
    if isinstance(decision, Drop):
        return msg.DropDecision()
    raise TypeError(f"unknown decision {decision!r}")


def _event(event: Event) -> msg.Event:
    return msg.Event(trigger=_trigger(event.trigger), decision=_decision(event.decision))


def _where(where: Optional[rec.Where]) -> Optional[msg.Where]:
    if where is None:
        return None
    if isinstance(where, rec.Boundary):
        return msg.AtBoundary(action=_action_ref(where.action), occurrence=where.occurrence)
    if isinstance(where, rec.Beginning):
        return msg.AtBeginning()
    if isinstance(where, rec.Cut):
        return msg.AtCut(action=_action_ref(where.action), occurrence=where.occurrence, done=where.done)
    raise TypeError(f"unknown where {where!r}")


def _entry_position(ref: rec.EntryRef) -> msg.EntryPosition:
    return msg.EntryPosition(part=_ENTRY_PART[type(ref)], index=ref.index)


class _HumanSide:
    """What the piece keeps per human to name entries and events and to tag the task on top (T-viz 1a (iv)): the script
    entry of every task seen on the stack, by object identity (a frame's task is its entry's task object; a task an
    event started has none); the script's events with their positions; the completions and the stretches of the
    record (world/tag.py)."""

    def __init__(self, machine):
        self.machine = machine
        self.refs: List[rec.EntryRef] = ([rec.OrdinaryRef(i) for i in range(len(machine.entries))]
                                         + [rec.RepeatableRef(i) for i in range(len(machine.repeatable))]
                                         + [rec.ClosingRef(j) for j in range(len(machine.closing))])
        self.events: List[Tuple[Event, msg.EventPosition]] = [
            (ev, msg.EventPosition(entry=_entry_position(ref), index=k))
            for ref, entries in ((rec.OrdinaryRef(i), e) for i, e in enumerate(machine.entries))
            for k, ev in enumerate(entries.events)] + [
            (ev, msg.EventPosition(entry=_entry_position(rec.ClosingRef(j)), index=k))
            for j, e in enumerate(machine.closing) for k, ev in enumerate(e.events)]
        self.entries: List[Tuple[TaskInstance, Optional[rec.EntryRef]]] = []
        self.completions: List[Tuple[int, object]] = []
        self.stretches = Stretches()
        self.tagged: Optional[msg.TaskTagged] = None

    def observe(self, transitions) -> None:
        """Registers the tasks on the stack with their frames' entries, and a task entered and left within the tick
        by the one entry whose task object it is (ambiguous or none: no entry)."""
        for frame in self.machine.stack:
            if not any(task is frame.task for task, _ in self.entries):
                self.entries.append((frame.task, frame.entry))
        for t in transitions:
            if isinstance(t, rec.Entered) and not any(task is t.task for task, _ in self.entries):
                refs = [r for r in self.refs if self.machine.entry_task(r) is t.task]
                self.entries.append((t.task, refs[0] if len(refs) == 1 else None))

    def entry_of(self, task: TaskInstance) -> Optional[msg.EntryPosition]:
        ref = next((entry for known, entry in self.entries if known is task), None)
        return None if ref is None else _entry_position(ref)

    def event_of(self, match) -> Optional[msg.EventPosition]:
        return next((position for ev, position in self.events if match(ev)), None)


def _transition(t: rec.Transition, side: _HumanSide) -> msg.Transition:
    if isinstance(t, rec.Entered):
        return msg.Entered(task=_task_ref(t.task))
    if isinstance(t, rec.Started):
        return msg.Started(task=_task_ref(t.task), trigger=_trigger(t.trigger), where=_where(t.where),
                           event=side.event_of(lambda ev: ev.trigger is t.trigger))
    if isinstance(t, rec.Resumed):
        return msg.Resumed(task=_task_ref(t.task))
    if isinstance(t, rec.Left):
        return msg.Left(task=_task_ref(t.task), outcome=_OUTCOME[t.outcome], entry=side.entry_of(t.task))
    if isinstance(t, rec.Refused):
        return msg.Refused(decision=_decision(t.decision), reason=_DECISION_REFUSAL[t.reason])
    if isinstance(t, rec.Unfired):
        position = side.event_of(lambda ev: ev is t.event)
        if position is None:
            raise ValueError(f"unfired event {t.event!r} is not an event of the script")
        return msg.Unfired(task=_task_ref(t.task), event=_event(t.event), reason=_UNFIRED[t.reason],
                           position=position)
    if isinstance(t, rec.StillOpen):
        return msg.StillOpen(task=_task_ref(t.task), entry=_entry_position(t.entry))
    raise TypeError(f"unknown transition {t!r}")


def _point(xy) -> msg.Point:
    return msg.Point(x=float(xy[0]), y=float(xy[1]))


def _extent(xy) -> msg.Extent:
    return msg.Extent(x=float(xy[0]), y=float(xy[1]))


def _bounds(x_min, x_max, y_min, y_max) -> msg.Bounds:
    return msg.Bounds(x_min=float(x_min), x_max=float(x_max), y_min=float(y_min), y_max=float(y_max))


# The world's things, translated by one function each for a sim-run's messages and for a view (T-viz 1a).

def _space(title: str, x_min, x_max, y_min, y_max) -> msg.Space:
    return msg.Space(title=title, bounds=_bounds(x_min, x_max, y_min, y_max))


def _area(area) -> msg.Area:
    return msg.Area(id=area.id, bounds=_bounds(area.x_min, area.x_max, area.y_min, area.y_max))


def _fixed_object(obj: SimObject) -> msg.FixedObject:
    return msg.FixedObject(id=obj.obj_id, type=obj.type, subtype=obj.subtype, position=_point(obj.position),
                           size=_extent(obj.size))


def _movable_object(obj: SimObject) -> msg.MovableObject:
    return msg.MovableObject(id=obj.obj_id, type=obj.type, subtype=obj.subtype, size=_extent(obj.size),
                             home_container=obj.home_container, destination=obj.destination)


def _object_states(facts) -> Tuple[msg.ObjectState, ...]:
    """The object states that hold, in the order of their names and arguments."""
    return tuple(msg.ObjectState(state=p.name, object=p.args[0].value if p.args else None)
                 for p in sorted(facts, key=lambda p: (p.name, tuple(a.value for a in p.args))))


# =============================================================================
# One sim-run
# =============================================================================

class MesaSimRun:
    """One sim-run on Mesa's side (webui.simulator.SimRunSide), over a SimRun it steps and ends."""

    def __init__(self, sim_run: msg.SimRunId, choice: msg.SimRunChoice, run: SimRun,
                 declarations: Tuple[msg.RunOptionDeclaration, ...]):
        self.sim_run = sim_run
        self._run = run
        model = run.model
        self._model = model
        self._ended = False
        self._fixed: List[str] = [oid for oid, obj in model.objects.items() if not obj.is_portable]
        self._movable: List[str] = [oid for oid, obj in model.objects.items() if obj.is_portable]   # the setup's order
        # The order of arrival per fixed object (the module's docstring); at the start, the setup's order.
        self._contents: Dict[str, List[str]] = {oid: [] for oid in self._fixed}
        self._place()
        self._positions: Dict[str, Tuple[float, float]] = {aid: self._position(a) for aid, a in self._agents()}
        self._last_motion: Dict[str, Optional[msg.Direction]] = {aid: None for aid, _ in self._agents()}
        self._finished_at: Optional[int] = None
        self._sides: Dict[str, _HumanSide] = {hid: _HumanSide(h.machine) for hid, h in model.humans.items()}
        for side in self._sides.values():
            side.observe(())
        # The tag per task (world/tag.py): the domain's declared context knowledge (None: no tag) and its recency
        # durations in ticks, the body's conversion, as the robot's memory of observed completions has them.
        self._knowledge = model.declared_context
        self._recency = ([] if self._knowledge is None else
                         [(e.task, int(_parse_duration_to_steps(e.recency.duration, model)))
                          for e in self._knowledge.entries() if e.recency is not None])

        # Per robot (T-viz 1b): its last decision as sent, and the ticks its hold had stood after the last step.
        self._decisions: Dict[str, Optional[msg.DecisionMade]] = {rid: None for rid in model.robots}
        self._stood: Dict[str, int] = {rid: 0 for rid in model.robots}

        _, layout_id, setup_id, scenario = resolve_triple(run.config)
        self.description = msg.RunDescription(
            sim_run=sim_run,
            run=msg.RunTriple(domain=run.config["domain"], layout=layout_id, setup=setup_id, scenario=scenario.id),
            stated=choice,
            effective=tuple(_value(d, _EFFECTIVE[d.name](model, run.config)) for d in declarations),
            world=self._world_description(),
            robots=tuple(self._robot_description(rid, robot, scenario) for rid, robot in model.robots.items()),
        )
        self._update = msg.TickUpdate(sim_run=sim_run, tick=None, world=self._world_tick(None),
                                      run=msg.RunTick(finished_at=None), end=None,
                                      robots=tuple(self._robot_tick(rid, robot, None, None)
                                                   for rid, robot in model.robots.items()))

    # ------------------------------------------------------------------
    # SimRunSide
    # ------------------------------------------------------------------

    def state(self) -> msg.TickUpdate:
        return self._update

    def step(self) -> msg.TickUpdate:
        if self._ended:
            raise RuntimeError(f"sim-run {self.sim_run} has ended")
        # each robot's task before the step: what its decision on this tick starts, continues or switches
        before = {rid: robot.current_task_instance for rid, robot in self._model.robots.items()}
        self._run.step()
        tick = self._run.steps_done - 1     # the run log's number of the step executed
        self._place()
        for aid, agent in self._agents():
            position = self._position(agent)
            dx, dy = position[0] - self._positions[aid][0], position[1] - self._positions[aid][1]
            if dx != 0.0 or dy != 0.0:
                norm = math.hypot(dx, dy)
                self._last_motion[aid] = msg.Direction(x=dx / norm, y=dy / norm)
            self._positions[aid] = position
        if self._finished_at is None and self._all_finished():
            self._finished_at = tick
        self._update = msg.TickUpdate(sim_run=self.sim_run, tick=tick, world=self._world_tick(tick),
                                      run=msg.RunTick(finished_at=self._finished_at), end=None,
                                      robots=tuple(self._robot_tick(rid, robot, tick, before[rid])
                                                   for rid, robot in self._model.robots.items()))
        return self._update

    def end(self, reason: msg.EndReason) -> msg.TickUpdate:
        if self._ended:
            raise RuntimeError(f"sim-run {self.sim_run} has ended")
        self._run.end()
        self._ended = True
        end_tick = int(self._model.schedule.steps)   # the tick end_run states the open entries at
        still_open = tuple(
            msg.StillOpenEntry(human=hid, task=_task_ref(t.task), entry=_entry_position(t.entry))
            for hid, human in self._model.humans.items()
            for t in human.record.transitions_at(end_tick) if isinstance(t, rec.StillOpen))
        self._update = self._update.model_copy(update={"end": msg.RunEnd(reason=reason, still_open=still_open)})
        return self._update

    def discard(self) -> None:
        self._run.close()
        self._ended = True

    # ------------------------------------------------------------------
    # Reading the model
    # ------------------------------------------------------------------

    def _agents(self):
        return list(self._model.humans.items()) + list(self._model.robots.items())

    def _all_finished(self) -> bool:
        """Every human's script has ended (no script, or every ordinary and closing entry closed with the stack
        empty: the executor selects nothing more) and every robot's task pool is empty (`RobotAgent.finished`, set on
        the tick of its `[meta] ... all tasks complete` line). The point MPB-5 names (T-viz 1a, P12)."""
        humans_done = all(h.machine is None or (h.machine.all_closed() and not h.machine.stack_tasks())
                          for h in self._model.humans.values())
        return humans_done and all(r.finished for r in self._model.robots.values())

    @staticmethod
    def _position(agent) -> Tuple[float, float]:
        return float(agent.pos[0]), float(agent.pos[1])

    def _place(self) -> None:
        """The order of arrival brought to the tick: an object that left a fixed object is removed from its list, an
        object that arrived is appended (two on one tick in the setup's order)."""
        objects = self._model.objects
        for fixed, held in self._contents.items():
            held[:] = [oid for oid in held if objects[oid].at_location == fixed]
        for oid in self._movable:
            fixed = objects[oid].at_location
            if fixed is None:
                continue
            if fixed not in self._contents:
                raise ValueError(f"movable object '{oid}' is in '{fixed}', which is not a fixed object")
            if oid not in self._contents[fixed]:
                self._contents[fixed].append(oid)

    def _world_description(self) -> msg.WorldDescription:
        model = self._model
        objects = model.objects
        return msg.WorldDescription(
            space=_space(model.env_display_name, model.space.x_min, model.space.x_max, model.space.y_min,
                         model.space.y_max),
            areas=tuple(_area(a) for a in model.areas),
            fixed_objects=tuple(_fixed_object(objects[oid]) for oid in self._fixed),
            movable_objects=tuple(_movable_object(objects[oid]) for oid in self._movable),
            humans=tuple(msg.AgentEntry(id=hid) for hid in model.humans),
            robots=tuple(msg.AgentEntry(id=rid) for rid in model.robots),
            scripts=tuple(self._script(hid, human) for hid, human in model.humans.items()),
            timeline=msg.TimelineInForce(
                source=_TIMELINE_SOURCE[model.timeline_source],
                windows=tuple(msg.TimelineWindow(fact=w.fact.name, start=w.start, until=w.end)
                              for w in model.timeline.windows)),
        )

    @staticmethod
    def _script(hid: str, human) -> msg.HumanScript:
        machine = human.machine
        entry = lambda e: msg.ScriptEntry(task=_task_ref(e.task), events=tuple(_event(ev) for ev in e.events))
        return msg.HumanScript(
            human=hid,
            dependence=_DEPENDENCE[human.scheduled_dependence],
            entries=tuple(entry(e) for e in machine.entries),
            repeatable=tuple(msg.RepeatableEntry(task=_task_ref(r.task)) for r in machine.repeatable),
            closing=tuple(entry(e) for e in machine.closing),
        )

    def _world_tick(self, tick: Optional[int]) -> msg.WorldTick:
        """The world at `tick` (None: the start). The timeline facts are those in force on the tick, as the world
        state of that tick has them (the start's are tick 0's, as the robot's first observation has them)."""
        model = self._model
        objects = model.objects
        agent_tick = lambda aid: msg.AgentTick(id=aid, position=_point(self._positions[aid]),
                                               last_motion=self._last_motion[aid])
        return msg.WorldTick(
            humans=tuple(agent_tick(hid) for hid in model.humans),
            robots=tuple(agent_tick(rid) for rid in model.robots),
            fixed_object_contents=tuple(msg.FixedObjectContents(fixed_object=fixed, movable_objects=tuple(held))
                                        for fixed, held in self._contents.items() if held),
            carried=tuple(msg.Carried(agent=objects[oid].held_by, movable_object=oid)
                          for oid in self._movable if objects[oid].held_by is not None),
            object_states=_object_states(model.state_facts),
            timeline_facts=tuple(sorted(p.name for p in model.timeline.facts_at(0 if tick is None else tick))),
            activity=tuple(self._activity(hid, human, tick) for hid, human in model.humans.items()),
            separations=() if tick is None else self._separations(),
        )

    def _separations(self) -> Tuple[msg.Separation, ...]:
        """The robot-human distance of the step just executed (T-viz 1c): the values its [sep] lines printed, kept by
        the sim-run; below the robot's min_separation (its meta-planner's) as the analyses count it, by the minimum."""
        robots = self._model.robots
        return tuple(msg.Separation(robot=rid, human=hid, distance=dist, minimum=minimum,
                                    below=minimum < float(robots[rid].meta_planner.min_separation))
                     for (rid, hid), (dist, minimum) in self._run.separation.items())

    def _activity(self, hid: str, human, tick: Optional[int]) -> msg.HumanActivity:
        machine, record, side = human.machine, human.record, self._sides[hid]
        if tick is None:
            stack, action, transitions, tagged = machine.stack_tasks(), None, (), None
        else:
            snap = truth_at(record, tick)
            stack = snap.stack
            action = (None if snap.action is None else
                      msg.ActionInHand(action=_action_ref(snap.action), occurrence=snap.occurrence,
                                       done=snap.done, total=snap.total))
            raw = record.transitions_at(tick)
            side.observe(raw)
            transitions = tuple(_transition(t, side) for t in raw)
            tagged = self._tag(side, tick, stack, raw)
        return msg.HumanActivity(human=hid, stack=tuple(_task_ref(t) for t in stack),
                                 stack_entries=tuple(side.entry_of(t) for t in stack), action=action,
                                 transitions=transitions,
                                 open_entries=tuple(_entry_position(r) for r in machine.open_entries()),
                                 tag=tagged)

    def _tag(self, side: _HumanSide, tick: int, stack, transitions) -> Optional[msg.TaskTagged]:
        """The tag of the task on top at `tick` (world/tag.py), computed at its stretch's first tick and kept through
        it; called once per tick, in order. The completions of the tick count at it (the reader's rule)."""
        side.completions += [(tick, t.task.schema) for t in transitions
                             if isinstance(t, rec.Left) and t.outcome is rec.Outcome.COMPLETED]
        start = side.stretches.at(tick, task_instance_key(stack[0]) if stack else None)
        if start is None or self._knowledge is None:
            side.tagged = None
        elif start == tick or side.tagged is None or side.tagged.since != start:
            found = tag_at(self._knowledge, stack[0].schema, set(self._model.timeline.facts_at(tick)),
                           recent_tasks(self._knowledge, side.completions, self._recency, tick))
            side.tagged = msg.TaskTagged(tag=msg.TagValue(found.tag.value), since=start,
                                         raised=tuple(sorted(s.name for s in found.raised)),
                                         lowered=tuple(sorted(s.name for s in found.lowered)))
        return side.tagged

    # ------------------------------------------------------------------
    # The robot: its body and its mind (T-viz 1b)
    # ------------------------------------------------------------------

    def _robot_description(self, rid: str, robot, scenario) -> msg.RobotDescription:
        """What is constant of the robot's mind: its condition (the model's effective run options), the human it
        observes, θ and min_separation (its meta-planner's), α, its hypothesis space in the recognizer's order (sorted
        by key), its own assigned tasks, and the observed human's assigned tasks it was given (as the loader gives
        them: assignment knowledge on and a human observed; else None)."""
        model = self._model
        condition = (msg.RobotCondition.HUMAN_UNAWARE if not model.human_aware else
                     msg.RobotCondition.INTENTION_UNAWARE if not model.intention_aware else
                     msg.RobotCondition.INTENTION_AWARE)
        observed = robot.observed_agent_id
        observed_cfg = next((a for a in scenario.agents if a.agent_id == observed), None)
        known = (tuple(_task_ref(t) for t in observed_cfg.assigned_tasks)
                 if model.assignment_knowledge and observed_cfg is not None else None)
        return msg.RobotDescription(
            robot=rid, condition=condition, observes=observed, theta=float(robot.meta_planner.theta),
            test_level=float(model.test_level), min_separation=float(robot.meta_planner.min_separation),
            context_knowledge=bool(model.context_knowledge),
            hypotheses=tuple(msg.Hypothesis(key=repr(h), task=h.task_name,
                                            bindings=tuple(msg.Binding(parameter=k, value=v)
                                                           for k, v in sorted(h.bindings.items())))
                             for h in sorted(model.observing[rid].hypotheses, key=repr)),
            assigned=tuple(_task_ref(t) for t in robot.assigned_tasks),
            known_assigned=known)

    def _robot_tick(self, rid: str, robot, tick: Optional[int], before: Optional[TaskInstance]) -> msg.RobotTick:
        """The robot at `tick` (None: the start), read after the step. The gate is asked of the belief the
        meta-planner receives (the robot's, or the body's belief before any observation), after the question admission
        asks first: a robot that observes no human is refused before the gate. A decision taken on this tick (its
        record's tick) is translated once and kept."""
        belief = robot.belief or robot._make_dummy_belief()
        gate = (msg.Gate.NO_HUMAN if robot.observed_agent_id is None
                else _GATE[robot.meta_planner._clears_gate(belief)])
        decided = robot.last_decision
        if tick is not None and decided is not None and decided.tick == tick:
            self._decisions[rid] = self._decision(robot, decided, gate, belief, before)
        return msg.RobotTick(robot=rid, body=self._body(rid, robot, tick),
                             belief=None if robot.belief is None else self._belief(robot, tick),
                             gate_answer=gate, decision=self._decisions[rid])

    def _body(self, rid: str, robot, tick: Optional[int]) -> msg.RobotBody:
        """The body: the task its last decision chose, while it runs; the action at the plan's cursor and its
        progress; the microaction of the tick; the hold, while ticks of it remain or it stood on this tick."""
        executor = robot.executor
        plan = executor.current_plan
        action = None
        if plan is not None and executor.action_index < len(plan.actions):
            progress = executor.progress()
            action = msg.RobotAction(action=_action_ref(plan.actions[executor.action_index]), done=progress.done,
                                     total=progress.total)
        decision = self._decisions[rid]
        stood = executor._hold_executed
        stood_now = stood > 0 and (stood > self._stood[rid] or (decision is not None and decision.tick == tick))
        hold = None
        if executor._hold_planned > 0 and (executor._hold_remaining > 0 or stood_now):
            hold = msg.HoldInProgress(decided_at=decision.tick, planned=executor._hold_planned, stood=stood)
        self._stood[rid] = stood
        task = robot.current_task_instance
        return msg.RobotBody(task=None if task is None else _task_ref(task), action=action,
                             microaction=robot.current_microaction, hold=hold, finished=bool(robot.finished))

    def _belief(self, robot, tick: int) -> msg.RobotBelief:
        """The recognizer's outputs: every live hypothesis (the keys of the belief over H) in the recognizer's order,
        with its prior (context knowledge on), adequacy, tail (a member only), warrant and rank; the levels and the
        recency facts of the memory (context knowledge on)."""
        b = robot.belief
        order = sorted(b.belief)     # the recognizer's order: its hypotheses sorted by key
        live = tuple(msg.HypothesisBelief(key=k, belief=float(b.belief[k]),
                                          prior=float(b.prior[k]) if k in b.prior else None,
                                          adequacy=_ADEQUACY[b.hypothesis_adequacy[k]],
                                          tail=float(b.tails[k]) if k in b.tails else None,
                                          warrant=_WARRANT[b.observation_warrant[k]], rank=_RANK[b.evidence_rank[k]])
                     for k in order)
        recent = () if robot.memory is None else tuple(t.name for t in robot.memory.recent(tick))
        return msg.RobotBelief(leader=b.most_likely, confidence=float(b.confidence), lifecycle=_LIFECYCLE[b.lifecycle],
                               finding=None if b.finding is None else _FINDING[b.finding],
                               boundary=bool(b.episode_boundary), live=live,
                               levels=tuple(msg.TaskLevel(task=name, level=_LEVEL[level])
                                            for name, level in b.levels.items()),
                               recent=recent)

    def _decision(self, robot, decided, gate: msg.Gate, belief, before: Optional[TaskInstance]) -> msg.DecisionMade:
        trigger = _TRIGGER.get(decided.trigger.reason)
        if trigger is None:
            raise ValueError(f"a fired trigger the web-ui does not know: '{decided.trigger.reason}'")
        result = decided.result
        chosen = result.current_task
        change = (msg.TaskChange.FINISHES if chosen is None else
                  msg.TaskChange.STARTS if before is None else
                  msg.TaskChange.CONTINUES if same_task(chosen, before) else msg.TaskChange.SWITCHES)
        return msg.DecisionMade(
            tick=decided.tick, trigger=trigger,
            cause=None if decided.trigger.cause is None else _CAUSE[decided.trigger.cause],
            gate_answer=gate, projection=self._projection(robot, decided, belief), change=change,
            chosen=None if chosen is None else _task_ref(chosen), hold=int(result.hold),
            queue=tuple(_task_ref(t) for t in result.queue))

    @staticmethod
    def _projection(robot, decided, belief) -> msg.Projection:
        """The projection the decision rested on, by its own form: none; the fallback (its one entry has no plan); or
        the admitted hypothesis's (the leader's at the decision). Its end, T_h, is its last segment's end step, on the
        decision's projection clock (step s ends world tick decision − 1 + s)."""
        projection = decided.projection
        if projection is None:
            return msg.NoProjection(reason=msg.NoProjectionReason.NO_HUMAN if robot.observed_agent_id is None
                                    else msg.NoProjectionReason.UNASSESSED)
        segments = [seg for entry in projection.entries for seg in entry.segments]
        t_h = float(segments[-1].end_step)
        until = decided.tick - 1 + t_h
        entry = projection.entries[0]
        if entry.abstract_plan is None:
            moving = any(tuple(seg.start_pos) != tuple(seg.end_pos) for seg in segments)
            return msg.FallbackProjection(mode=msg.FallbackMode.MOVING if moving else msg.FallbackMode.STANDING,
                                          span=t_h - float(segments[0].start_step), until=until)
        return msg.AdmittedProjection(hypothesis=belief.most_likely,
                                      plan=tuple(_action_ref(a) for a in entry.abstract_plan.actions), until=until)
