"""
shared/types.py

Canonical data types for communication between cognitive and embodiment layers.
These types define the contract between simulator-agnostic algorithms and 
simulator-specific implementations.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Set, Union
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
class StepCall:
    """
    One step in an HTN method body — a call to an action schema with bindings.
    bindings map the action schema's Var parameters to Terms (Vars or Consts).
    Unresolved Vars are grounded by the planner against WorldState at plan time.
    e.g. StepCall('goto_zone', {Var('?zone'): Var('?item_zone')})
    """
    action_name: str
    bindings: Dict[Var, Term]  # may be partial — unresolved Vars grounded later


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
    step_calls: List[StepCall]               # ordered decomposition
    derived_vars: Dict[str, tuple] = field(default_factory=dict)
    # {var_name: (lookup_fn, source_var_name)} e.g. {"?item_zone": ("zone_of", "?item")}

@dataclass
class TaskSchema:
    """
    HTN compound task with one or more decomposition methods.
    The planner selects an applicable method and expands it into grounded actions.
    """
    name: str                           # e.g. 'deliver_item'
    parameters: List[Var]
    methods: List[MethodSchema]         # one now; multiple for conditional decomposition later
    is_assigned: bool = False
    is_foreseeable: bool = False # TODO: if we need it besides the is_assigned flag in TaskInstance — maybe not.
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
    # ongoing (not yet complete). e.g. "directional" for move_to (cosine-similarity
    # trajectory consistency). None for pick_up, place, wait_at, scan_it — these
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
    is_foreseeable is read from schema — not declared here.
    """
    schema: "TaskSchema"
    bindings: Dict[Var, Const]  # {Var("?item"): Const("item_1")}

def check_task_bindings(task: TaskInstance, object_type_by_id: Dict[str, str]) -> None:
    """
    A scheduled or assigned task must be well typed against the world it runs in: every
    bound object exists in the layout, and every parameter the schema types
    (TaskSchema.parameter_types, which also types a parameter the recognizer does not
    enumerate because another parameter determines it) is bound to an object of that
    type. Raises ValueError otherwise — an error,
    not a warning, because an ill-typed instance is a task the domain does not
    describe (a coffee break with no coffee machine), which the human would execute
    and the robot could never recognise (TODO-49 (2), the binding part; F47b). The
    embodiment supplies the id → type table; shared/ sees no simulator object.
    """
    expected_types = task.schema.parameter_types or {}
    for var, const in task.bindings.items():
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
    source object (T-B1a): assigned_tasks is the work order, the reference the
    robot's mind holds, so it describes the station, not a deviation. Raises
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

@dataclass
class AgentConfig:
    """
    Configuration for one agent in a scenario.
    Two task fields, with semantics differing by agent type:
      - human:  assigned_tasks  — the work order the human was given. A fact the
                                  robot may know: WHICH tasks, never their order.
                scheduled_tasks — the developer's execution script: fixed ordered
                                  sequence (assigned + foreseeable interleaved).
                                  Order encodes when deviations occur. Never
                                  reordered at runtime. Drives HumanAgent only;
                                  the robot has no access to it.
      - robot:  assigned_tasks  — its task pool, seeded into the meta_planner.
                                  Unordered: the meta_planner produces Q0 and every
                                  later ordering from IR output.
                scheduled_tasks — not read for robots.
    Foreseeable tasks sit inline in scheduled_tasks at the correct position;
    schema.is_foreseeable identifies them — no special-casing needed. They never
    appear in assigned_tasks: a deviation is not part of a work order.
    """
    agent_id: str
    agent_type: str                      # "human" or "robot"
    start_position: Tuple[float, float]
    scheduled_tasks: List[TaskInstance] = field(default_factory=list)  # human execution script; unread for robot
    observes: List[str] = field(default_factory=list)  # agent_ids this agent observes
    assigned_tasks: List[TaskInstance] = field(default_factory=list)   # the work order — see docstring

    def __post_init__(self):
        """
        Validate assigned_tasks against what this agent declares.
        Empty assigned_tasks skips validation entirely, so scenarios not yet
        migrated stay loadable.
        Identity is the task_instance_key() string throughout: TaskInstance is
        deliberately unhashable, so duplicate/set checks run on keys, never on
        instances.
        """
        if not self.assigned_tasks:
            return

        assigned_keys = [task_instance_key(t) for t in self.assigned_tasks]
        dupes = sorted({k for k in assigned_keys if assigned_keys.count(k) > 1})
        if dupes:
            raise ValueError(
                f"AgentConfig '{self.agent_id}': duplicate assigned_tasks keys: {dupes}"
            )

        if self.agent_type != "human":
            return

        scripted_keys = [
            task_instance_key(t)
            for t in self.scheduled_tasks
            if not t.schema.is_foreseeable
        ]
        scripted_dupes = sorted({k for k in scripted_keys if scripted_keys.count(k) > 1})
        if scripted_dupes:
            raise ValueError(
                f"AgentConfig '{self.agent_id}': duplicate non-foreseeable "
                f"scheduled_tasks keys: {scripted_dupes}"
            )

        missing = sorted(set(scripted_keys) - set(assigned_keys))
        extra = sorted(set(assigned_keys) - set(scripted_keys))
        if missing or extra:
            raise ValueError(
                f"AgentConfig '{self.agent_id}': assigned_tasks must match the "
                f"non-foreseeable scheduled_tasks exactly. "
                f"Scripted but not assigned: {missing}. "
                f"Assigned but not scripted: {extra}."
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
    
    
@dataclass
class DomainModel:
    """
    The complete HTN planning domain: all task schemas and action schemas.
    Defined once in shared/domain.py, injected into KnowledgeBase at startup.
    Consumed by planner (top-down decomposition) and recognizer (bottom-up inference).
    """
    tasks: Dict[str, TaskSchema]        # {task_name: TaskSchema}
    actions: Dict[str, ActionSchema]  # {action_name: ActionSchema}
    microactions: List[str]             # terminal symbols e.g. ['STEP', 'GRASP', ...]
    intentions: Set[str]                # set of all intention IDs (task names that can be root tasks). in practice top-lelev HTN tasks.

    def get_tasks_for_action(self, action_name: str) -> List[TaskSchema]:
        """Return all tasks whose methods contain a step calling this action."""
        result = []
        for task in self.tasks.values():
            for method in task.methods:
                if any(step.action_name == action_name for step in method.step_calls):
                    result.append(task)
                    break
        return result

    def get_actions_for_microaction(self, mu: str) -> List[ActionSchema]:
        """Return all action schemas that decompose to this microaction."""
        result = []
        for op in self.actions.values():
            if isinstance(op.microactions, list) and mu in op.microactions:
                result.append(op)
            elif isinstance(op.microactions, str) and op.microactions.startswith(mu):
                result.append(op)
        return result
    


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
    One action's straight-line motion (or stationary stretch) through space and
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
    segments: List[Segment]         # per-action motion or stationary stretch, for interference detection / realization
    
    
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
    candidate's trajectory actually is, given the human: the hold-only
    realization under the whole-trajectory minimal shift — one hold δ at the
    robot's position at the decision step, then the projected plan run
    unchanged, shifted by δ. Realization prices conflict as duration: a
    conflicted plan costs more because avoiding the human takes longer. No
    conflict weight, no penalty term. Since F1 (robot-responsible separation:
    a standing robot never violates, and there is no hold cap) realization is
    TOTAL — every plan realizes, and this carries a cost always; the former
    `realizable` flag and the reasons "hold_position_violated" /
    "hold_reaches_horizon" are gone.

    delta:             the hold, in WHOLE steps (≥ 0): the number of STAND
                       ticks the body executes, so the plan that was checked
                       is the plan that runs (T3b; design_decisions.md,
                       "Realization as built"). 0 when there is no human
                       projection.
    cost:              T_r + delta over the FULL plan, T_r the plain projected
                       duration (the span of the plan's segments, FRACTIONAL
                       steps — the projection's continuous duration; execution
                       quantises per walk and that is deliberately not
                       compensated, L2). One quantity: the projected duration
                       of the realized trajectory. A caller comparing it with
                       a plain cost must use the same T_r —
                       `projected_duration`, not ProjectedPlan's integer
                       `total_estimated_cost`. The tail beyond T_h is inside
                       T_r and is not corrected for (TODO-69, reading (1)).
    projected_duration: T_r.
    segments:          the realized trajectory, head-to-tail: the stationary
                       hold at `hold_position` from `hold_start` to the shifted
                       plan's start (present only when that stretch has
                       positive duration), then every projected segment shifted
                       by delta.
    hold_position:     where the robot stands during the hold — the plan's
                       first segment's start, i.e. where the robot is at the
                       decision step (which may be partway along a walk).
    hold_start:        the decision step.
    horizon:           T_h; None when there is no human projection.
    unassessed_share:  the share of the realized plan's span [hold_start, end]
                       lying beyond T_h — the part that was neither cleared nor
                       blocked, logged so that the bias can be reported
                       (TODO-69); 1.0 when the hold pushes the whole plan past
                       T_h. The steps before the human projection's span (the
                       observation offset, L2) are unassessed too but not
                       counted. 1.0 when there is no human projection.
    reason:            "realized"; "no_human_projection" (delta 0, fully
                       unassessed — the caller treats it as it treats no
                       projection today).
    """
    delta: int
    cost: float
    projected_duration: float
    segments: List[Segment]
    hold_position: Tuple[float, float]
    hold_start: float
    horizon: Optional[float]
    unassessed_share: float
    reason: str


@dataclass
class ExecutorState:
    """
    Single immutable per-tick snapshot passed to both evaluate_triggers() and
    update() so they never independently re-derive robot state and drift apart.
    """
    agent_id: str
    current_task: Optional["TaskInstance"]
    holding: Optional[str]   # item_id or None — convenience snapshot for evaluate_triggers()'s
                              # tick-to-tick task-commit detection; WorldState.predicates carries
                              # the same fact per-agent but is rebuilt fresh each tick with no
                              # memory to compare against


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