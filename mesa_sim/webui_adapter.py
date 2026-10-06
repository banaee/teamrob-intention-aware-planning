"""
mesa_sim/webui_adapter.py

PURPOSE:
    Mesa's piece for the web-ui (T-viz 0.4): implements webui/simulator.py's interface over Mesa. It produces the
    web-ui's three messages (webui/messages.py): the catalogue from the domain registry and the run file, the run
    description and the tick updates from one sim-run (mesa_sim/sim_run.py's SimRun, built through
    mesa_sim/run_config.py). It only reads the model: a sim-run with messages produced writes the same log pair as the
    same sim-run without (tests/test_tviz_messages.py).

WHAT THIS MODULE DOES:
    - MesaSimulator: the catalogue, and the build of a sim-run from the screen-user's choice. A choice that cannot be
      built raises BuildFailed and writes no log pair (T-viz 0.4, Q4)
    - MesaSimRun: one sim-run; per step its tick update; its end and its discard
    - Keeps per sim-run what the model does not hold and a page reload must not lose: the order in which movable
      objects arrived in each fixed object, and each agent's direction of its most recent step that moved it, from
      its own positions. Neither is a world fact; neither is written anywhere

WHAT THIS MODULE DOES NOT DO:
    - No rule of the web-ui (which sim-run is current, the end at the configured steps, the lock): the server's
    - No server, no transport, no page
    - Nothing of the robot's mind: the tick update's world is the environment and the human executor's record

RUN OPTIONS BY NAME (T-viz 0.4, Q3, a deliberate exception at the input boundary): the web-ui knows the run options
only as the catalogue declares them, each identified by its name, so that it stays independent of the simulator's
options. The choice's values are matched to the declarations by name here, once, and handed to run_configuration,
which validates them as it validates a run file.
"""

import json
import math
from typing import Callable, Dict, List, Optional, Tuple

from mesa_sim.run_config import (BOOL_OPTIONS, DOMAIN_REGISTRY, EXPERIMENT_CONFIG_PATH, ONE_OF_OPTIONS,
                                 OPTION_DEFAULTS, RUN_OPTIONS, load_experiment, resolve_triple, run_configuration,
                                 user_args_parser)
from mesa_sim.sim_model import SimModel
from mesa_sim.sim_run import RunLog, SimRun
from shared.types import (AfterAction, DuringAction, Drop, Event, GroundedAction, Now, ScriptDependence, Start,
                          TaskInstance, TimelineSource, Trigger, task_instance_key)
from world import record as rec
from world.queries import truth_at
from webui import messages as msg
from webui.simulator import BuildFailed

# The run options that are not the triple, by kind. Every run option of run_config's RUN_OPTIONS is of one kind; one
# with none stops the catalogue (_declarations).
TRIPLE = ("domain", "layout", "scenario")
LEVEL_OPTIONS = ("test_level",)
COUNT_OPTIONS = ("steps",)
COUNT_MINIMUM = 1   # a sim-run in the web-ui takes at least one step

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
             msg.LevelOption: msg.LevelValue, msg.CountOption: msg.CountValue}

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


# =============================================================================
# The catalogue
# =============================================================================

def _declarations(run_file_config: dict) -> Tuple[msg.RunOptionDeclaration, ...]:
    """The run options in RUN_OPTIONS's order, the triple excluded, each of its kind, its default the run file's value
    or else OPTION_DEFAULTS's, its description the flag's help text."""
    help_of = {action.dest: action.help for action in user_args_parser()._actions}
    declarations = []
    for name in RUN_OPTIONS:
        if name in TRIPLE:
            continue
        if name in COUNT_OPTIONS:
            if name not in run_file_config:
                raise ValueError(f"the run file states no '{name}'; the catalogue's default is the run file's")
            declarations.append(msg.CountOption(name=name, default=run_file_config[name], minimum=COUNT_MINIMUM,
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


def _layout_title(path: str, layout_id: str) -> str:
    with open(path, "r") as f:
        return json.load(f)["space"].get("name", layout_id)


def _domain_entry(name: str, domain: dict) -> msg.DomainEntry:
    return msg.DomainEntry(
        name=name,
        layouts=tuple(msg.LayoutEntry(id=lid, title=_layout_title(path, lid)) for lid, path in domain["layouts"].items()),
        setups=tuple(msg.SetupEntry(id=sid) for sid in domain["setups"]),
        scenarios=tuple(msg.ScenarioEntry(id=s.id, setup=s.setup, reference_layouts=tuple(s.reference_layouts),
                                          description=s.description)
                        for s in domain["scenarios"].values()),
    )


class MesaSimulator:
    """Mesa's side of the web-ui (webui.simulator.Simulator). `run_path` is the run file the catalogue's defaults and
    default choice come from."""

    def __init__(self, run_path: str = EXPERIMENT_CONFIG_PATH):
        self.run_path = run_path
        self._run_file_config = load_experiment(run_path, {})
        self._declarations = _declarations(self._run_file_config)

    def catalogue(self) -> msg.Catalogue:
        config = self._run_file_config
        _, layout_id, _, scenario = resolve_triple(config)
        default_choice = msg.SimRunChoice(
            domain=config["domain"], layout=layout_id, scenario=scenario.id,
            options=tuple(_value(d, d.default) for d in self._declarations))
        return msg.Catalogue(
            domains=tuple(_domain_entry(name, domain) for name, domain in DOMAIN_REGISTRY.items()),
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
        log = RunLog()
        try:
            run = SimRun(config, log)
        except Exception as e:
            log.close()
            raise BuildFailed(str(e)) from e
        return MesaSimRun(sim_run, choice, run, self._declarations)

    def _configuration(self, choice: msg.SimRunChoice) -> dict:
        """The run configuration's mapping of the choice: the triple, and one value per declared run option, matched
        by name (the exception at the input boundary, above); a value of another kind, a missing, repeated or
        undeclared option, or a count below its minimum, is refused."""
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
            if isinstance(declaration, msg.CountOption) and value.value < declaration.minimum:
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
    return msg.TaskRef(task=task.schema.name,
                       bindings=tuple(msg.Binding(parameter=var.name, value=const.value)
                                      for var, const in task.bindings.items()),
                       label=task_instance_key(task))


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


def _transition(t: rec.Transition) -> msg.Transition:
    if isinstance(t, rec.Entered):
        return msg.Entered(task=_task_ref(t.task))
    if isinstance(t, rec.Started):
        return msg.Started(task=_task_ref(t.task), trigger=_trigger(t.trigger), where=_where(t.where))
    if isinstance(t, rec.Resumed):
        return msg.Resumed(task=_task_ref(t.task))
    if isinstance(t, rec.Left):
        return msg.Left(task=_task_ref(t.task), outcome=_OUTCOME[t.outcome])
    if isinstance(t, rec.Refused):
        return msg.Refused(decision=_decision(t.decision), reason=_DECISION_REFUSAL[t.reason])
    if isinstance(t, rec.Unfired):
        return msg.Unfired(task=_task_ref(t.task), event=_event(t.event), reason=_UNFIRED[t.reason])
    if isinstance(t, rec.StillOpen):
        return msg.StillOpen(task=_task_ref(t.task), entry=_entry_position(t.entry))
    raise TypeError(f"unknown transition {t!r}")


def _point(xy) -> msg.Point:
    return msg.Point(x=float(xy[0]), y=float(xy[1]))


def _extent(xy) -> msg.Extent:
    return msg.Extent(x=float(xy[0]), y=float(xy[1]))


def _bounds(x_min, x_max, y_min, y_max) -> msg.Bounds:
    return msg.Bounds(x_min=float(x_min), x_max=float(x_max), y_min=float(y_min), y_max=float(y_max))


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

        _, layout_id, setup_id, scenario = resolve_triple(run.config)
        self.description = msg.RunDescription(
            sim_run=sim_run,
            run=msg.RunTriple(domain=run.config["domain"], layout=layout_id, setup=setup_id, scenario=scenario.id),
            stated=choice,
            effective=tuple(_value(d, _EFFECTIVE[d.name](model, run.config)) for d in declarations),
            world=self._world_description(),
        )
        self._update = msg.TickUpdate(sim_run=sim_run, tick=None, world=self._world_tick(None), end=None)

    # ------------------------------------------------------------------
    # SimRunSide
    # ------------------------------------------------------------------

    def state(self) -> msg.TickUpdate:
        return self._update

    def step(self) -> msg.TickUpdate:
        if self._ended:
            raise RuntimeError(f"sim-run {self.sim_run} has ended")
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
        self._update = msg.TickUpdate(sim_run=self.sim_run, tick=tick, world=self._world_tick(tick), end=None)
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
            space=msg.Space(title=model.env_display_name,
                            bounds=_bounds(model.space.x_min, model.space.x_max, model.space.y_min, model.space.y_max)),
            areas=tuple(msg.Area(id=a.id, bounds=_bounds(a.x_min, a.x_max, a.y_min, a.y_max)) for a in model.areas),
            fixed_objects=tuple(
                msg.FixedObject(id=oid, type=objects[oid].type, subtype=objects[oid].subtype,
                                position=_point(objects[oid].position), size=_extent(objects[oid].size))
                for oid in self._fixed),
            movable_objects=tuple(
                msg.MovableObject(id=oid, type=objects[oid].type, subtype=objects[oid].subtype,
                                  size=_extent(objects[oid].size), home_container=objects[oid].home_container,
                                  destination=objects[oid].destination)
                for oid in self._movable),
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
        states = sorted(model.state_facts, key=lambda p: (p.name, tuple(a.value for a in p.args)))
        return msg.WorldTick(
            humans=tuple(agent_tick(hid) for hid in model.humans),
            robots=tuple(agent_tick(rid) for rid in model.robots),
            fixed_object_contents=tuple(msg.FixedObjectContents(fixed_object=fixed, movable_objects=tuple(held))
                                        for fixed, held in self._contents.items() if held),
            carried=tuple(msg.Carried(agent=objects[oid].held_by, movable_object=oid)
                          for oid in self._movable if objects[oid].held_by is not None),
            object_states=tuple(msg.ObjectState(state=p.name, object=p.args[0].value if p.args else None)
                                for p in states),
            timeline_facts=tuple(sorted(p.name for p in model.timeline.facts_at(0 if tick is None else tick))),
            activity=tuple(self._activity(hid, human, tick) for hid, human in model.humans.items()),
        )

    @staticmethod
    def _activity(hid: str, human, tick: Optional[int]) -> msg.HumanActivity:
        machine, record = human.machine, human.record
        if tick is None:
            stack, action, transitions = machine.stack_tasks(), None, ()
        else:
            snap = truth_at(record, tick)
            stack = snap.stack
            action = (None if snap.action is None else
                      msg.ActionInHand(action=_action_ref(snap.action), occurrence=snap.occurrence,
                                       done=snap.done, total=snap.total))
            transitions = tuple(_transition(t) for t in record.transitions_at(tick))
        return msg.HumanActivity(human=hid, stack=tuple(_task_ref(t) for t in stack), action=action,
                                 transitions=transitions,
                                 open_entries=tuple(_entry_position(r) for r in machine.open_entries()))
