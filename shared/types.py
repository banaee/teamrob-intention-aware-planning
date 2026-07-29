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
    predicted_next_actions: Dict[str, List[str]] = field(default_factory=dict)  # {intention_id: [action_types]}



@dataclass
class AgentState:
    """
    Symbolic state of a single agent.
    Built by: SIM_sim/world_state_builder.py while processing simulator state each MESA step or each ROS callback (or when requested by planner).
    Consumed by: shared/planner.py, shared/replanning.py
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
    Consumed by: shared/planner.py, shared/replanning.py
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
    Used for duration-based actions like wait_at where time is not world state.
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
    # Maps each enumerable Var name to its object type, e.g.
    # {"?item": "item", "?destination": "kitting_table"}.
    # IR's hypothesis space takes the cartesian product over every entry here.
    # A Var not listed here is not enumerated (fixed at plan time some other way,
    # or the task has no such parameter). Empty dict = no enumeration (coffee_break
    # today, one hypothesis total).

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


@dataclass
class AgentConfig:
    """
    Configuration for one agent in a scenario.
    scheduled_tasks semantics differ by agent type:
      - human:  fixed ordered sequence (assigned + foreseeable tasks interleaved).
                Order encodes when deviations occur. Never reordered at runtime.
      - robot:  initially ordered by meta_planner at t=0 using base-cost heuristic.
                Treated as a mutable prioritised set — meta_planner may reorder
                at any cognitive clock event based on IR output.
    Foreseeable tasks sit inline in the list at the correct position;
    schema.is_foreseeable identifies them — no special-casing needed.
    """
    agent_id: str
    agent_type: str                      # "human" or "robot"
    start_position: Tuple[float, float]
    scheduled_tasks: List[TaskInstance]  # fixed task sequence for human, flexible mutable task "set" for robot
    observes: List[str] = field(default_factory=list)  # agent_ids this agent observes


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
class ProjectedPlanEntry:
    """
    One task's contribution to a ProjectedPlan.
    Produced by meta_planner per candidate task in the queue.
    """
    abstract_plan: "AbstractPlan"
    estimated_start_step: int
    estimated_duration: int         # steps to complete this task
    spatial_zones: List[str]        # zones occupied during this task (for interference detection)


@dataclass
class ProjectedPlan:
    """
    Multi-task lookahead structure for meta_planner reasoning.
    Never handed to the executor — meta_planner internal only.
    Spans the full projected task queue with timing and spatial footprint per task.
    Used for interference detection and cost comparison across candidate orderings.
    """
    task_queue: List[str]               # task instance IDs in projected order
    entries: List[ProjectedPlanEntry]
    total_estimated_cost: int           # sum of durations + any inter-task gap steps
    
    