"""
shared/types.py

Canonical data types for communication between cognitive and embodiment layers.
These types define the contract between simulator-agnostic algorithms and 
simulator-specific implementations.
"""

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Sequence, Tuple, Any, Set, Union
from enum import Enum


# =============================================================================
# OBSERVATION TYPES
# =============================================================================

@dataclass
class SpatialContext:
    """Spatial information about an observed action."""
    position: Tuple[float, float]
    orientation: float
    zone: Optional[str] = None


@dataclass
class ActionContext:
    """Contextual information about an observed action."""
    target_object: Optional[str] = None
    progress: float = 0.0  # 0.0 to 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Observation:
    """
    Discrete observation of human behavior.
    This is what embodiment layers provide to the cognitive layer.
    """
    timestamp: float
    agent_id: str
    detected_microaction: str  # e.g., "move_to_shelf_3", "pick_item_7"
    spatial_context: SpatialContext
    action_context: ActionContext
    confidence: float = 1.0  # ROS might have < 1.0, Mesa always 1.0


# =============================================================================
# BELIEF STATE TYPES
# =============================================================================

@dataclass
class BeliefState:
    """
    Robot's belief distribution over human intentions.
    Output of intention recognition.
    """
    timestamp: float
    agent_id: str
    distribution: Dict[str, float]  # {intention_id: probability}
    most_likely: str  # intention_id with highest probability
    confidence: float  # overall confidence in belief
    # predicted_next_actions: Dict[str, List[str]] = field(default_factory=dict)  # {intention_id: [action_types]}  
                            # OUTDATED: current design uses ProjectedPlan for multi-step prediction; 
                            # this field is retained for backward compatibility but should not be used in new code.



@dataclass
class AgentState:
    """
    Symbolic state of a single agent.
    Built by: SIM_sim/world_state_builder.py while processing simulator state each MESA step or each ROS callback (or when requested by planner).
    Consumed by: shared/planner.py, shared/meta_planner.py
    """
    agent_id: str
    current_zone: str
    holding: Optional[str] = None  # item_id or None
    current_task: Optional[str] = None  # task_id or None
    metadata: Dict[str, Any] = field(default_factory=dict)

# =============================================================================
# Domain knowledge types (predicates, variables, constants) used in world state and planning. 
# =============================================================================


@dataclass(frozen=True)
class Var:
    """A formal planning variable. e.g. Var('?item'), Var('?zone')."""
    name: str  # must start with '?'

    def __str__(self):
        return self.name


@dataclass(frozen=True)
class Const:
    """A domain constant. e.g. Const('kitting_table'), Const('zone_SE')."""
    value: str

    def __str__(self):
        return self.value


# A Term is either a variable (unbound, resolved at grounding) or a constant.
Term = Union[Var, Const]


@dataclass(frozen=True)
class Predicate:
    """
    A logical predicate with typed arguments.
    args are Term objects — either Var (schema-level) or Const (grounded).
    e.g. Predicate('at', (Var('?agent'), Var('?zone')))         # schema
         Predicate('at', (Const('robot_0'), Const('zone_SE')))  # grounded
    """
    name: str
    args: Tuple[Term, ...]

    def __str__(self):
        return f"{self.name}({', '.join(str(a) for a in self.args)})"

    def __repr__(self):
        return self.__str__()
    
# =============================================================================
# WORLD STATE TYPES
# =============================================================================

    
@dataclass
class WorldState:
    """
    Symbolic representation (snapshot) of the environment at a given time.
    Built by embodiment layers, consumed by cognitive layer. 
    Bulit by SIM_sim/world_state_builder.py in each Mesa step or each ROS callback (or when requested by planner).
    Consumed by: shared/planner.py, shared/meta_planner.py
    Note: not persistent: created fresh each step, passed as argument, discarded.    
    """
    timestamp: float
    agent_states: Dict[str, AgentState]  # {agent_id: AgentState}
    agent_positions: Dict[str, Tuple[float, float]] = field(default_factory=dict)  # {agent_id: (x, y)}
    object_locations: Dict[str, str] = field(default_factory=dict)  # {item_id: location_id} 
    predicates: Set[Predicate] = field(default_factory=set)  # e.g., "path_clear", "human_at_table"
    object_zones: Dict[str, str] = field(default_factory=dict)  # {item_id: zone_id}
    object_home_container: Dict[str, str] = field(default_factory=dict)     # {item_id: container_id} — static per scenario, set once at load, 
                                                                            # never updated as item moves (unlike object_locations/object_zones)
    object_destination: Dict[str, str] = field(default_factory=dict)        # {item_id: destination_id} — static per scenario, set once at load
                                                                            # from the layout's "destination" (kitting: the item's designated table);
                                                                            # read through the planner's derived-var lookup "destination_of"
    object_positions: Dict[str, Tuple[float, float]] = field(default_factory=dict)  # {obj_id: (x, y)} — env objects + items, for IR direction reasoning
    metadata: Dict[str, Any] = field(default_factory=dict)

# =============================================================================
# TASK KNOWLEDGE TYPES (HTN-style, formal term system)
# Defined in shared/domain.py, consumed by KnowledgeBase, planner, recognizer.
# No string parsing anywhere downstream.
# =============================================================================

@dataclass
class ConditionSchema:
    """
    A predicate condition used in preconditions, effects, or completion checks.
    Args are Terms — Var for schema-level, Const for domain constants.
    Roles:
        guard       — method applicability condition (checked at decomposition time)
        precondition — action feasibility (checked at planning time)
        effect      — declared world change (used by planner for forward reasoning)
        completion  — runtime execution monitor (checked by executor against WorldState)
    """
    name: str
    args: Tuple[Term, ...]

    def to_predicate(self, bindings: Dict[str, str]) -> Predicate:
        """
        Ground this condition into a Predicate by substituting Vars from bindings.
        bindings: {var_name: concrete_string} e.g. {'?agent': 'robot_0'}
        """
        resolved = []
        for arg in self.args:
            if isinstance(arg, Var):
                resolved.append(Const(bindings[arg.name]))
            else:
                resolved.append(arg)
        return Predicate(self.name, tuple(resolved))


@dataclass
class ProcessCompletion:
    """
    Completion determined by process exhaustion, not world state.
    Executor signals done when microaction queue empties naturally.
    Planner treats this action as always satisfiable in forward chaining.
    Nothing outside the executor can observe such a completion, so a recognizer
    cannot see the action end. kitting's wait_at no longer uses it: the body
    emits waited(agent, entity) when its timer runs out (see
    domains/kitting/actions.py). Still used by dock_loading's wait_at (deferred).
    """
    pass


@dataclass
class Step:
    """
    One step in an HTN method body (T-H): an ActionStep (a primitive action) or a
    TaskStep (a compound sub-task). The step holds the schema OBJECT it calls,
    never its name; the planner branches on the step's class. Not constructed
    directly.
    """
    def __post_init__(self):
        if type(self) is Step:
            raise TypeError("Step is not constructed directly: write an ActionStep or a TaskStep")


@dataclass
class ActionStep(Step):
    """
    A call to an action schema. bindings map the action schema's Var parameters
    to Terms (Vars or Consts); unresolved Vars are grounded by the planner
    against WorldState at plan time.
    e.g. ActionStep(move_to, {Var('?target'): Var('?item')})
    """
    action: "ActionSchema"
    bindings: Dict[Var, Term]  # may be partial — unresolved Vars grounded later


@dataclass
class TaskStep(Step):
    """
    A call to a compound sub-task: bindings map the sub-task's Var parameters to
    Terms, and the planner decomposes it recursively into the same flat action
    list. No domain writes one today.
    """
    task: "TaskSchema"
    bindings: Dict[Var, Term]


@dataclass
class MethodSchema:
    """
    One HTN decomposition method for a compound task.
    A task may have multiple methods; the planner selects the first whose
    guards hold in the current WorldState.
    guards=[] means unconditionally applicable.
    derived_vars: optional mapping of Var names to lookup functions for dynamic grounding.
    e.g. {"?item_zone": ("zone_of", "?item")} means ?item_zone is derived from the zone of ?item at grounding time.
    """
    name: str
    parameters: List[Var]
    guards: List[ConditionSchema]       # empty = unconditional
    steps: List[Step]                   # ordered decomposition
    derived_vars: Dict[str, tuple] = field(default_factory=dict)
    # {var_name: (lookup_fn, source_var_name)} e.g. {"?item_zone": ("zone_of", "?item")}

@dataclass
class TaskSchema:
    """
    HTN compound task with one or more decomposition methods.
    The planner selects an applicable method and expands it into grounded actions.
    The base of the tree's three classes (T-H): every schema is a WorkTask, a
    PersonalTask or a HumanOnlyTask, and the class is the declaration. Not
    constructed directly.
    """
    name: str                           # e.g. 'deliver_item'
    parameters: List[Var]
    methods: List[MethodSchema]         # one now; multiple for conditional decomposition later
    parameter_types: Dict[str, str] = field(default_factory=dict)
    # The TYPE of each parameter, e.g. {"?item": "item", "?kitting_table":
    # "kitting_table"}: a bound value is validated against it at load
    # (check_task_bindings). IR's hypothesis space takes the cartesian product
    # over every entry here that is NOT in determined_parameters. Empty dict =
    # no enumeration (coffee_break today, one hypothesis total).
    determined_parameters: Dict[str, tuple] = field(default_factory=dict)
    # {var_name: (lookup_fn, source_var_name)} — a parameter whose value is not
    # free but follows from another parameter through a planner lookup, e.g.
    # {"?kitting_table": ("destination_of", "?item")}: the item's table is a
    # fact of the station (T-B1a). Not enumerated by the recognizer; resolved
    # by the planner before method selection. For "destination_of" an explicit
    # binding in the task instance is used as given and the lookup fills only
    # an unbound parameter. Distinct from MethodSchema.derived_vars, which are
    # variables used inside one method's steps, not task parameters.

    def __post_init__(self):
        if type(self) is TaskSchema:
            raise TypeError(
                f"task '{self.name}': a TaskSchema is not constructed directly; declare a "
                f"WorkTask, a PersonalTask or a HumanOnlyTask"
            )


@dataclass
class WorkTask(TaskSchema):
    """May appear in a human's assigned tasks (deliver_item); a robot's own
    assigned tasks are WorkTasks. Never left out of a robot's task model."""


@dataclass
class PersonalTask(TaskSchema):
    """Never assigned (coffee_break, ac_activation). A PersonalTask in a robot's
    task model is a foreseeable task; one may be omitted from a task model."""


@dataclass
class HumanOnlyTask(PersonalTask):
    """A PersonalTask never given to any robot (go_to, stand): rejected when a
    task model is built. The only class that may type a parameter as a landmark."""

@dataclass
class ActionSchema:
    """
    HTN primitive action — directly executable, not decomposed further into subtasks.
    Decomposes to microactions (STEP*, GRASP, etc.) in the embodiment layer.
    preconditions: feasibility check at planning time
    effects:       declared world changes (forward reasoning, Phase 4)
    completion:    runtime predicate checked by executor against WorldState
    progress_evaluator: names a registered IR likelihood function (shared/likelihood_functions.py)
                   used to score in-progress (not-yet-complete) evidence for this action.
                   None means this action has no meaningful in-progress signal —
                   only its completion predicate carries evidence.
    """
    name: str                           # e.g. 'goto_zone'
    parameters: List[Var]
    preconditions: List[ConditionSchema]
    effects: List[ConditionSchema]
    completion: Union[ConditionSchema, ProcessCompletion]    # either conditionSchema or ProcessCompletion
    microactions: Union[str, List[str]] # 'STEP*' / 'STAND*' or ['GRASP'] etc.
    movement_target_key: Optional[str] = None
    # Binding key whose value is the movement target position.
    # e.g. "?zone" for goto_zone, "?target" for move_to.
    # None for non-movement actions (pick_up, place, wait_at).
    movement_target_type: Optional[str] = None
    # "zone" or "object" — tells decomposer how to resolve the movement target.
    # None for non-movement actions.
    progress_evaluator: Optional[str] = None
    # Name of the IR progress-likelihood function to apply while this action is
    # ongoing (not yet complete). e.g. "excess_path" for move_to (the wasted-path
    # likelihood, I4; the earlier "directional" cosine kernel was removed, handback
    # §8). None for pick_up, place, wait_at, scan_it — these
    # have no graded in-progress signal, only a completion predicate.
    # Looked up in shared.likelihood_functions.PROGRESS_EVALUATORS by the recognizer.
    # Recognizer dispatches by this name only — never by microaction string.
    duration_key: Optional[str] = None
    # Binding key whose value is the action's DURATION, for a stationary action
    # whose length the domain states (wait_at: "?duration", an ISO-8601 string
    # bound by the method). None for actions whose duration is the body's own
    # (pick_up, place: one microaction). The body's decomposer executes it and
    # the Projector prices it through the body's duration-to-steps callable
    # (TODO-32), so knowledge and behaviour read the same binding.
    retracts: List[ConditionSchema] = field(default_factory=list)
    # Facts that are no longer true once the action is done — the delete list
    # beside `effects`, the add list. e.g. place retracts holding(?agent, ?item).
    # Its own list and not a negation flag on ConditionSchema, because a
    # ConditionSchema is also a guard, a precondition and a completion, where
    # such a flag would be declared and never read. Every Var must be one the
    # grounded action binds. Read by the Projector's successor state only
    # (T-B2a; the part of TODO-07 projection needs); the live planner does no
    # forward chaining.
    moved_object_key: Optional[str] = None
    moved_to_key: Optional[str] = None
    # Binding keys naming the object the action moves and where the action puts
    # it: an agent that then holds it, or an object it then lies at. e.g.
    # pick_up ("?item", "?agent"), place ("?item", "?target"). Declared as
    # movement_target_key declares the movement target. None for an action that
    # moves no object. Where an object is has two representations in a
    # WorldState, a predicate and the object_locations / object_positions maps
    # target resolution reads; this declares the second, which no predicate
    # name in shared/ could (T-B2a).

@dataclass
class GroundedAction:
    """
    A fully grounded action: all Vars resolved to Consts.
    Produced by the planner, consumed by the executor.
    completion_predicate is fully instantiated — executor checks membership
    in WorldState.predicates directly, no string parsing.
    """
    action_name: str
    bindings: Dict[str, str]            # {var_name: concrete_value} e.g. {'?zone': 'zone_SE'}
    completion_predicate: Optional[Predicate]     # fully grounded, ready for set membership check (or None if completion is ProcessCompletion)
    schema: ActionSchema            # back-reference for decomposer


@dataclass
class TaskInstance:
    """
    A concrete instantiation of a TaskSchema with specific parameter bindings.
    Used in scenario definitions and agent task assignments.
    bindings map Vars declared in the schema to concrete Const values.
    Its class (WorkTask, PersonalTask, HumanOnlyTask) is its schema's.
    """
    schema: "TaskSchema"
    bindings: Dict[Var, Const]  # {Var("?item"): Const("item_1")}

    # The authored forms of an event on a script entry (T-H, item 5; built in
    # T-H2): sugar that constructs Event(AfterAction | DuringAction, Start | Drop)
    # on a ScriptEntry holding this task. `what` is the TaskInstance to start or
    # `drop`; `occurrence` selects the k-th (0-based) occurrence of `action` in
    # the entry's expansion when the method repeats it.
    def at(self, action: "ActionSchema", what: "Union[TaskInstance, Decision]",
           occurrence: Optional[int] = None) -> "ScriptEntry":
        return ScriptEntry(self, ()).at(action, what, occurrence)

    def during(self, action: "ActionSchema", time: str, what: "Union[TaskInstance, Decision]",
               occurrence: Optional[int] = None) -> "ScriptEntry":
        return ScriptEntry(self, ()).during(action, time, what, occurrence)

def check_task_bindings(task: TaskInstance, object_type_by_id: Dict[str, str],
                        check_duration: Callable[[str], Any]) -> None:
    """
    A scheduled or assigned task must be well typed against the world it runs in: every
    bound object exists in the layout, and every parameter the schema types
    (TaskSchema.parameter_types, which also types a parameter the recognizer does not
    enumerate because another parameter determines it) is bound to an object of that
    type. Raises ValueError otherwise — an error,
    not a warning, because an ill-typed instance is a task the domain does not
    describe (a coffee break with no coffee machine), which the human would execute
    and no hypothesis could describe: unmodelled behaviour by accident (TODO-49
    (2), the binding part; F47b). The embodiment supplies the id → type table;
    shared/ sees no simulator object.
    A duration parameter (duration_parameters(), typed through an action's
    duration_key, not parameter_types) names no object: its value is handed to
    `check_duration`, the body's own duration parser, which raises ValueError on
    a value it cannot read (T-H).
    """
    expected_types = task.schema.parameter_types or {}
    durations = duration_parameters(task.schema)
    for var, const in task.bindings.items():
        if var in durations:
            try:
                check_duration(const.value)
            except ValueError as e:
                raise ValueError(
                    f"{task_instance_key(task)}: {var.name} is bound to '{const.value}', "
                    f"which is not a duration: {e}"
                ) from e
            continue
        actual = object_type_by_id.get(const.value)
        if actual is None:
            raise ValueError(
                f"{task_instance_key(task)}: {var.name} is bound to '{const.value}', "
                f"which is not an object of this layout"
            )
        expected = expected_types.get(var.name)
        if expected is not None and actual != expected:
            raise ValueError(
                f"{task_instance_key(task)}: {var.name} is bound to '{const.value}' of type "
                f"'{actual}', but the schema requires type '{expected}'"
            )


def duration_parameters(schema: TaskSchema) -> Set[Var]:
    """
    The task parameters that are durations: those a method step binds to its
    action's duration_key (stand(?duration) -> the stand action's ?duration). The
    type of a duration parameter is declared through the action's duration_key,
    not parameter_types (T-H, item 9); read from the typed step, never from a name.
    """
    params = set(schema.parameters)
    found: Set[Var] = set()
    for method in schema.methods:
        for step in method.steps:
            if isinstance(step, ActionStep) and step.action.duration_key is not None:
                term = step.bindings.get(Var(step.action.duration_key))
                if isinstance(term, Var) and term in params:
                    found.add(term)
    return found


DESTINATION_LOOKUP = "destination_of"


def destination_derivations(schema: "TaskSchema") -> List[Tuple[str, str]]:
    """
    The (parameter, source parameter) pairs a task schema determines through
    the "destination_of" lookup (TaskSchema.determined_parameters), in
    declaration order. Read from the schema, never from a var name.
    """
    return [(var_name, source_var)
            for var_name, (lookup_fn, source_var) in schema.determined_parameters.items()
            if lookup_fn == DESTINATION_LOOKUP]


def check_task_destinations(task: TaskInstance, destination_by_id: Dict[str, str]) -> None:
    """
    An ASSIGNED task that binds a var the schema otherwise resolves through
    "destination_of" must bind the destination the layout declares for its
    source object (T-B1a): assigned_tasks are the assigned tasks, the reference
    the robot's mind holds, so they describe the station, not a deviation. Raises
    ValueError naming the task, the source object and both values. Not applied
    to a human's scheduled_tasks, which may send an object elsewhere.
    """
    bound = {var.name: const.value for var, const in task.bindings.items()}
    for var_name, source_var in destination_derivations(task.schema):
        if var_name not in bound or source_var not in bound:
            continue
        source = bound[source_var]
        designated = destination_by_id.get(source)
        if bound[var_name] != designated:
            raise ValueError(
                f"{task_instance_key(task)}: {var_name} is bound to '{bound[var_name]}', "
                f"but the layout designates '{designated}' for {source_var}='{source}'"
            )


def task_instance_key(task: TaskInstance) -> str:
    """
    Derived identity string for a TaskInstance — schema name + sorted bindings,
    e.g. "deliver_item(?item=item_3)". Two TaskInstances with identical
    schema+bindings produce the same key by design (not a bug to guard
    against — see design_decisions.md). Mirrors HypothesisKey.__repr__ in
    shared/recognizer.py; introduced here rather than as a stored id field
    on TaskInstance (would touch every construction site in
    domains/*/scenarios.py for no benefit).
    """
    if not task.bindings:
        return f"{task.schema.name}()"
    params = ",".join(
        f"{var.name}={const.value}"
        for var, const in sorted(task.bindings.items(), key=lambda kv: kv[0].name)
    )
    return f"{task.schema.name}({params})"


# The object type of a landmark: a symbolic place a layout may declare. Only a
# HumanOnlyTask may type a parameter as one (Tree's constructor, T-H), so no
# hypothesis binds one and no robot action grounds to one. A framework term,
# not a domain one.
LANDMARK_TYPE = "landmark"


# =============================================================================
# THE HUMAN'S SCRIPT (T-H, item 5; built in T-H2)
# An ordered list of fully bound task instances of the tree with typed events
# attached. An event is a Trigger and a Decision: no unions, no sentinels, no
# kind strings. Nothing here reaches the robot's mind. The stack machine that
# runs a Script is world/human_executor.py; the record it writes is
# world/record.py.
# =============================================================================

@dataclass(frozen=True)
class Trigger:
    """What fires an event (the glossary's "event trigger"). Not constructed
    directly: an AfterAction, a DuringAction or Now."""
    def __post_init__(self):
        if type(self) is Trigger:
            raise TypeError("Trigger is not constructed directly: write AfterAction, DuringAction or Now")


@dataclass(frozen=True)
class AfterAction(Trigger):
    """Fires after `action` of the entry's expansion completes (written with
    `at`). `occurrence` is the 0-based occurrence of the schema in the
    expansion; None means it must occur exactly once (else a load error)."""
    action: "ActionSchema"
    occurrence: Optional[int] = None

    def __repr__(self):
        return f"at({_anchor_text(self.action, self.occurrence)})"


@dataclass(frozen=True)
class DuringAction(Trigger):
    """A cut `time` (ISO-8601, the form durations use; the body converts it)
    into `action` of the entry's expansion (written with `during`). The cut
    happens once that many of the body's ticks of the action are executed."""
    action: "ActionSchema"
    time: str
    occurrence: Optional[int] = None

    def __repr__(self):
        return f"during({_anchor_text(self.action, self.occurrence)},{self.time})"


@dataclass(frozen=True)
class Now(Trigger):
    """A live event (inject): fires on the tick it is applied."""

    def __repr__(self):
        return "now"


def _anchor_text(action: "ActionSchema", occurrence: Optional[int]) -> str:
    return action.name if occurrence is None else f"{action.name}#{occurrence}"


@dataclass(frozen=True)
class Decision:
    """What an event does. Not constructed directly: a Start or a Drop."""
    def __post_init__(self):
        if type(self) is Decision:
            raise TypeError("Decision is not constructed directly: write Start(task) or drop")


@dataclass(frozen=True)
class Start(Decision):
    """Suspend the current task and run `task` (any TaskInstance of the tree).
    It holds a TaskInstance, never a ScriptEntry: a decision's task carries no
    events, so the one-level stack is a property of the type (TODO-100)."""
    task: TaskInstance

    def __repr__(self):
        return f"start({task_instance_key(self.task)})"


@dataclass(frozen=True)
class Drop(Decision):
    """Remove the top of the stack: the task in hand is abandoned."""

    def __repr__(self):
        return "drop"


drop = Drop()


@dataclass(frozen=True)
class Event:
    trigger: Trigger
    decision: Decision

    def __repr__(self):
        return f"{self.trigger!r}->{self.decision!r}"


def _decision_of(what: "Union[TaskInstance, Decision]") -> Decision:
    """The sugar's one dispatch on the class of what the author wrote: a
    TaskInstance is started, a Decision is taken as it is."""
    if isinstance(what, TaskInstance):
        return Start(what)
    if isinstance(what, Decision):
        return what
    raise TypeError(f"an event starts a TaskInstance or is `drop`; got {what!r}")


@dataclass(frozen=True)
class ScriptEntry:
    """One entry of a human's script: a task instance with its events, in
    authored order. Each event fires once, when its anchor is reached, and is
    then consumed."""
    task: TaskInstance
    events: Tuple[Event, ...] = ()

    def at(self, action: "ActionSchema", what: "Union[TaskInstance, Decision]",
           occurrence: Optional[int] = None) -> "ScriptEntry":
        event = Event(AfterAction(action, occurrence), _decision_of(what))
        return ScriptEntry(self.task, self.events + (event,))

    def during(self, action: "ActionSchema", time: str, what: "Union[TaskInstance, Decision]",
               occurrence: Optional[int] = None) -> "ScriptEntry":
        event = Event(DuringAction(action, time, occurrence), _decision_of(what))
        return ScriptEntry(self.task, self.events + (event,))

    def __repr__(self):
        return f"{task_instance_key(self.task)}{list(self.events) if self.events else ''}"


class Script:
    """
    The human's script (T-H): its entries in order. A plain TaskInstance is an
    entry with no events. The only form of AgentConfig.scheduled_tasks (the C1
    list form was deleted in T-H3).
    """

    def __init__(self, entries: Sequence["Union[TaskInstance, ScriptEntry]"]):
        self.entries: List[ScriptEntry] = []
        for e in entries:
            if isinstance(e, TaskInstance):
                self.entries.append(ScriptEntry(e, ()))
            elif isinstance(e, ScriptEntry):
                self.entries.append(e)
            else:
                raise TypeError(f"script entry {e!r}: not a TaskInstance or a ScriptEntry")

    def tasks(self) -> List[TaskInstance]:
        """Every task the script names: each entry's, and each Start's."""
        out: List[TaskInstance] = []
        for entry in self.entries:
            out.append(entry.task)
            out.extend(ev.decision.task for ev in entry.events if isinstance(ev.decision, Start))
        return out

    def __repr__(self):
        return f"Script({self.entries})"


@dataclass
class AgentConfig:
    """
    Configuration for one agent in a scenario.
    Two task fields, with semantics differing by agent type:
      - human:  assigned_tasks  — the assigned tasks the human was given. A fact
                                  the robot may know: WHICH tasks, never their order.
                scheduled_tasks — the human's script (T-H): a Script of
                                  fully bound task instances with events, run
                                  by the human's stack machine
                                  (world/human_executor.py). Drives HumanAgent
                                  only; the robot has no access to it.
      - robot:  assigned_tasks  — its task pool, seeded into the meta_planner.
                                  Unordered: the meta_planner produces Q0 and every
                                  later ordering from IR output.
                scheduled_tasks — not read for robots.
    Every assigned task, for either agent type, is a WorkTask instance (T-H;
    rejected otherwise). A PersonalTask or a HumanOnlyTask is written in the
    script as an entry or as an event's Start. Nothing ties the assigned tasks
    to the script at load: an assigned task may go unperformed (the record's
    `unperformed` query, T-H4).
    """
    agent_id: str
    agent_type: str                      # "human" or "robot"
    start_position: Tuple[float, float]
    scheduled_tasks: Script = field(default_factory=lambda: Script([]))  # the human's script (see docstring); unread for robot
    observes: List[str] = field(default_factory=list)  # agent_ids this agent observes
    assigned_tasks: List[TaskInstance] = field(default_factory=list)   # the assigned tasks — see docstring

    def __post_init__(self):
        """
        Validate what this agent declares: scheduled_tasks is a Script, and
        assigned_tasks are WorkTask instances without duplicates.
        Empty assigned_tasks skips their validation.
        The duplicate check compares task_instance_key() strings: TaskInstance
        is deliberately unhashable (TODO-107: settled with T-H4's task equality).
        """
        if not isinstance(self.scheduled_tasks, Script):
            raise TypeError(
                f"AgentConfig '{self.agent_id}': scheduled_tasks is a Script, not {type(self.scheduled_tasks).__name__}"
            )
        if not self.assigned_tasks:
            return

        not_work = [task_instance_key(t) for t in self.assigned_tasks if not isinstance(t.schema, WorkTask)]
        if not_work:
            raise ValueError(
                f"AgentConfig '{self.agent_id}': an assigned task is a WorkTask instance; "
                f"these are not: {not_work}"
            )

        assigned_keys = [task_instance_key(t) for t in self.assigned_tasks]
        dupes = sorted({k for k in assigned_keys if assigned_keys.count(k) > 1})
        if dupes:
            raise ValueError(
                f"AgentConfig '{self.agent_id}': duplicate assigned_tasks keys: {dupes}"
            )


@dataclass
class ScenarioConfig:
    """
    Complete scenario definition — agents, their tasks, and environment reference.
    Lives in domains/<domain>/scenarios.py, not in configs/.
    """
    id: str
    name: str
    description: str
    agents: List[AgentConfig]
    # env_layout: str                      # removed. will be handled in domains/<domain>/registry.py 
    
    
# =============================================================================
# PLANNING TYPES
# =============================================================================

class ActionType(Enum):
    """High-level action types the robot can perform."""
    NAVIGATE = "navigate"
    PICK = "pick"
    PLACE = "place"
    WAIT = "wait"
    HANDOVER = "handover"


@dataclass
class AbstractAction:
    """
    High-level action with optional execution hints.
    The planner outputs these; embodiment layers interpret them.
    """
    action_type: ActionType
    parameters: Dict[str, Any]  # e.g., {"target": "shelf_3", "item": "item_7"}
    action_name: str = ""  # e.g. "GOTO_ZONE", "PICK_UP" — added to AbstractAction for better mapping from raw action strings in KnowledgeBase 
    
    # Optional execution hints (Mesa may use directly, ROS may ignore)
    estimated_path: Optional[List[Tuple[float, float]]] = None
    estimated_duration: float = 0.0
    spatial_constraints: Dict[str, Any] = field(default_factory=dict)
    temporal_constraints: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AbstractPlan:
    """
    Complete plan for robot execution.
    Output of adaptive planning.
    """

    goal_intention: str  # What robot is trying to achieve
    actions: List[GroundedAction]  # Sequence of grounded actions to execute
    estimated_total_cost: float = 0.0
    contingencies: Dict[str, Any] = field(default_factory=dict)  # Future: alternative plans
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Segment:
    """
    One action's straight-line motion (or stationary segment) through space and
    step-time — the unit interference-detection algorithms operate on. Several
    segments make up one ProjectedPlanEntry.

    Straight-line/constant-speed only, matching the same assumption
    Projector.build_segments() already makes (distance / assumed_speed) and
    Mesa's current steps_toward(). Non-movement actions (grasp, wait, place)
    are stationary segments — start_pos == end_pos, spanning the action's
    duration — still valid input to interference algorithms (e.g. a human
    passing close while the robot is stationary mid-pickup). A HOLD placed by
    realization (Phase 4C wait-decision revision) is a stationary segment of
    exactly this shape, and is checked like any other: the robot waits where
    it is.

    Path-realization beyond straight-line (static-obstacle-aware, non-linear)
    is the detour strategy of realization (DESIGN-13, Phase 4D) — out of
    scope here by design. Swapping it in later should only require changing
    how Projector.build_segments() computes each segment's path, not this
    shape.
    """
    start_pos: Tuple[float, float]
    start_step: float
    end_pos: Tuple[float, float]
    end_step: float
    
@dataclass
class ProjectedPlanEntry:
    """
    One task's part of a ProjectedPlan, produced by Projector.project().
    An ordering of n tasks projects to ONE ProjectedPlan with n entries, in
    the ordering's order.
    """
    abstract_plan: "AbstractPlan"
    estimated_start_step: int
    estimated_duration: int         # steps to complete this task
    segments: List[Segment]         # per-action motion or stationary segment, for interference detection / realization
    
    
@dataclass
class ProjectedPlan:
    """
    Multi-task lookahead structure for meta_planner reasoning.
    Never handed to the executor — meta_planner internal only.
    Spans one projected ordering, one entry per task, with timing and spatial
    footprint per task. Used for interference detection and cost comparison
    across candidates.
    """
    task_queue: List[str]               # task instance keys, in the ordering's order
    entries: List[ProjectedPlanEntry]
    total_estimated_cost: int           # sum of durations + any inter-task gap steps

@dataclass
class RealizedPlan:
    """
    Output of shared/realization.realize() for one robot ProjectedPlan against
    the human's (T3; design_decisions.md, "The robot can wait"). What a
    candidate's segments actually become, given the human: the hold-only
    realization under the whole-trajectory minimal shift, applied PER ENTRY
    (T-B Q2, T-B2c) — before each entry one hold, taken where the previous
    entry ended (at the robot's position at the decision step for the first),
    then that entry run unchanged at its cumulative shift. With ONE entry:
    one hold δ, then the projected plan shifted by δ, as before T-B2c.
    Realization prices conflict as duration: a
    conflicted plan costs more because avoiding the human takes longer. No
    conflict weight, no penalty term. Since F1 (robot-responsible separation:
    a standing robot never violates, and there is no hold cap) realization is
    TOTAL — every plan realizes, and this carries a cost always; the former
    `realizable` flag and the reasons "hold_position_violated" /
    "hold_reaches_horizon" are gone.

    holds:             THE HOLD BEFORE EACH ENTRY, one per entry in the plan's
                       order, in WHOLE steps (≥ 0): the ticks the robot stands
                       still at the boundary before that entry —
                       cumulative_shifts[k] − cumulative_shifts[k−1] (the
                       first entry's is cumulative_shifts[0]). Whole steps,
                       because a hold reaches the body as STAND ticks, so the
                       plan that was checked is the plan that runs (T3b;
                       design_decisions.md, "Realization as built"). All 0
                       when there is no human projection.
    cumulative_shifts: THE CUMULATIVE SHIFT OF EACH ENTRY: the ticks by which
                       it starts later than projected — the result of its own
                       minimal-shift search, whose lower bound is the previous
                       entry's cumulative shift (0 for the first). Never
                       decreasing. Not a hold: docs/glossary.md keeps the two
                       apart, and so do these two fields.
    delta:             (read-only property) holds[0], the hold before the
                       FIRST entry. With one entry it is the one hold and the
                       one shift — what B2 `b2a` and single_task read, exactly
                       as before T-B2c. With several it is the only hold that
                       is executed before the next re-decision
                       (UpdateResult.hold); it is NOT the plan's total shift,
                       which is cumulative_shifts[-1].
    cost:              T_r + cumulative_shifts[-1] over the FULL plan — the sum
                       of the entries' T_r plus the cumulative shift of the
                       last entry; with one entry, T_r + delta. T_r the plain projected
                       duration (the span of the plan's segments, FRACTIONAL
                       steps — the projection's continuous duration; execution
                       quantises per walk and that is deliberately not
                       compensated, L2). One quantity: the projected duration
                       of the RealizedPlan's segments. A caller comparing it with
                       a plain cost must use the same T_r —
                       `projected_duration`, not ProjectedPlan's integer
                       `total_estimated_cost`. The tail beyond T_h is inside
                       T_r and is not corrected for (TODO-69, reading (1)).
    projected_duration: T_r.
    segments:          the realized plan's segments, head-to-tail: per entry,
                       the stationary segment of its hold where the hold is
                       taken — the entry's first segment's start, which is
                       where the previous entry ended — up to the entry's
                       shifted start (present only when that stretch has
                       positive duration), then the entry's projected segments
                       shifted by its cumulative shift.
    hold_position:     where the robot stands during the FIRST hold — the plan's
                       first segment's start, i.e. where the robot is at the
                       decision step (which may be partway along a walk). A
                       later hold's position is read off `segments`.
    hold_start:        the decision step (the first hold's start).
    horizon:           T_h; None when there is no human projection.
    unassessed_share:  the share of the realized plan's span [hold_start, end]
                       lying beyond T_h — the part that was neither cleared nor
                       blocked, logged so that the bias can be reported
                       (TODO-69); 1.0 when the hold pushes the whole plan past
                       T_h. The steps before the human projection's span (the
                       observation offset, L2) are unassessed too but not
                       counted. 1.0 when there is no human projection.
    reason:            "realized"; "no_human_projection" (every hold 0, fully
                       unassessed — the caller treats it as it treats no
                       projection today).
    """
    holds: List[int]
    cumulative_shifts: List[int]
    cost: float
    projected_duration: float
    segments: List[Segment]
    hold_position: Tuple[float, float]
    hold_start: float
    horizon: Optional[float]
    unassessed_share: float
    reason: str

    @property
    def delta(self) -> int:
        """The hold before the first entry (see the class docstring)."""
        return self.holds[0]


@dataclass
class ExecutorState:
    """
    Single immutable per-tick snapshot passed to both evaluate_triggers() and
    update() so they never independently re-derive robot state and drift apart.
    """
    agent_id: str
    current_task: Optional["TaskInstance"]
    holding: Optional[str]   # item_id or None — convenience snapshot; evaluate_triggers() no
                              # longer reads it (task_committed removed, D3); kept for the
                              # analysis scripts that read it


@dataclass
class TriggerDecision:
    """Return type of MetaPlanner.evaluate_triggers()."""
    fired: bool          # a cognitive-clock event occurred; what the caller does with
                         # it is the caller's business (renamed from `replan`, which
                         # presumed the consequence — inherited from should_replan())
    reason: str
    score: Optional[float] = None


@dataclass
class UpdateResult:
    """Return type of MetaPlanner.update().
    Note: current_task/queue are quoted forward refs ("TaskInstance") since 
    TaskInstance is defined earlier in the TASK KNOWLEDGE TYPES section, 
    above PLANNING TYPES — matching the existing pattern already used 
    for "AbstractPlan" in ProjectedPlanEntry.
    hold: the hold δ the decision carries, in WHOLE ticks (T4): the robot
    stands where it is for `hold` ticks, starting on the decision tick, then
    continues the plan — an executed hint (io_contracts.md §1.9, TODO-71).
    Set by B2 `b2a` when it continues the current task with its realized
    hold, and by B3 to the winner's realized δ (T10), whether the winner is
    the current task or another; 0 otherwise (no hold: no human projection,
    cost_strategy "plain", the terminal
    return). The executor may refine a hold, never re-decide or drop it
    silently; a later trigger's decision replaces it.
    """
    current_task: "TaskInstance"
    queue: List["TaskInstance"]
    hold: int = 0