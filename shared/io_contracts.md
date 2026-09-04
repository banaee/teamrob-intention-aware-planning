# shared/io_contracts.md

This document defines the **minimal, simulator-agnostic I/O contracts** for the cognitive core in `shared/`.
Implementation details (Bayes, HTN search, etc.) are intentionally omitted.
All simulators (Mesa, ROS) must translate their internal data into these canonical forms.

**Last aligned September 2026** against `shared/types.py`, `shared/planner.py`,
`shared/domain_knowledge.py`, `shared/recognizer.py`, `shared/meta_planner.py`, and
`shared/trajectory_algorithms.py`, following the Phase 4C MetaPlanner build. §2.2 is now
verified implementation, not proposed design; §2.2a (the retired `replanning.py` trigger)
has been deleted along with the module. The previously-flagged §1.3 discrepancy
(`object_positions`/`agent_positions`) is now confirmed resolved.

---

## 0. Notation (matches paper)

- **τ** : an intention (task) from the intention set **T**
- **a** : a high-level action from action set **A**
- **μ** : a micro-action from micro-action set **M**
- **t** : logical time index (Mesa step or ROS window index)

Core algorithms reason over **discrete micro-actions** and **symbolic world predicates**.

---

## 1. Canonical Data Types (defined in `shared/types.py`)

### 1.1 `Observation`

**Produced by simulator**, consumed by `IntentionRecognizer`.

```python
@dataclass
class SpatialContext:
    position: Tuple[float, float]
    orientation: float
    zone: Optional[str] = None

@dataclass
class ActionContext:
    target_object: Optional[str] = None
    progress: float = 0.0                  # 0.0 to 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Observation:
    timestamp: float
    agent_id: str                          # observed agent (usually human)
    detected_microaction: str              # μ_t label, e.g. "step", "grasp", "stand"
    spatial_context: SpatialContext
    action_context: ActionContext
    confidence: float = 1.0                # 1.0 in Mesa (ground truth); <1.0 in ROS
```

**Correction from previous version:** the field is `spatial_context`, not `spatial`. There is
no `observer_id` field — confirmed absent from both the dataclass and Mesa's `obs_builder.py`.

**Hard requirement:**
Mesa provides `detected_microaction` perfectly from ground truth.
ROS must **discretize sensor streams** into microaction labels before calling IR.

---

### 1.2 `BeliefState`

**Produced by IR**, consumed by `meta_planner.py`.

```python
@dataclass
class BeliefState:
    timestamp: float
    agent_id: str                          # agent whose intention is being tracked
    distribution: Dict[str, float]         # {intention_name: probability}
    most_likely: str                       # argmax intention name
    confidence: float                      # max probability
    # predicted_next_actions: Dict[str, List[str]] — DEPRECATED, commented out in the
    # dataclass itself. Multi-step prediction now goes through ProjectedPlan (§1.7) and
    # IntentionRecognizer.get_hypothesis() (§2.1), not this field. Do not use in new code.
```

**Invariants:**
- probabilities sum to 1.0 (within numerical tolerance)
- `most_likely` is a key in `distribution`

---

### 1.3 `WorldState`

**Produced by simulator**, consumed by `planner.py` and `meta_planner.py`.

```python
@dataclass
class AgentState:
    agent_id: str
    current_zone: str
    holding: Optional[str] = None          # item_id or None
    current_task: Optional[str] = None     # task_id or None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class WorldState:
    timestamp: float
    agent_states: Dict[str, AgentState] # {agent_id: AgentState}
    object_locations: Dict[str, str] # {object_id: location_id} — symbolic
    object_zones: Dict[str, str] # {item_id: zone_id}
    object_home_container: Dict[str, str] # {item_id: original container_id} — added for
    # the deliver_with_return cancellation guard
    object_positions: Dict[str, Tuple[float, float]] # {item_id: (x, y)} — decided design,
    # see status note below
    agent_positions: Dict[str, Tuple[float, float]] # {agent_id: (x, y)} — same status
    predicates: Set[Predicate] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)
```

**Status: RESOLVED (September 2026).** `object_positions`/`agent_positions` were previously
flagged here as an open discrepancy — documented as decided design, but unconfirmed as
present in the dataclass. Both are confirmed implemented and live:
`MetaPlanner._build_segments()` reads `world.agent_positions[agent_id]` and
`world.object_positions[target_id]` on every projection, and `scenario_00` runs end-to-end
without error. No longer a discrepancy.

**Scoped exception, per design_decisions.md:** exists specifically for `move_to`'s latent
target-parameter inference (trajectory-consistency scoring in the recognizer) — the one case
where the deterministic μ→a mapping holds at the action-type level but not the parameter
level. Consumed only by `shared/likelihood_functions.py`'s `direction_consistency_likelihood`
and target-resolution helpers (`_get_expected_position`, `_get_target_zone`) in
`recognizer.py` — never by `planner.py` or `executor.py`, which stay fully symbolic.

**Predicate naming convention (unchanged):**
- `in_zone(agent_id, zone_id)` — coarse zone-level context, used by IR context reasoning
- `at(agent_id, object_id)` — fine-grained object proximity, used by executor completion checking
- `holding(agent_id, item_id)` — agent is carrying item
- `obj_at(item_id, location_id)` — item rests at location

`in_zone` and `at` are intentionally distinct predicates. Conflating them caused a semantic
mismatch where `move_to` completion was never satisfied.

**Design rule:** core planners only use symbolic predicates; geometry stays in simulators —
subject to the two scoped exceptions above, both now confirmed live: IR's trajectory-
consistency scoring, and `MetaPlanner`'s duration/interference estimation, which reads
positions to build `Segment`s (§1.7). `planner.py` and `executor.py` remain fully symbolic.

---

### 1.4 `GroundedAction`

**Produced by planner**, consumed by simulator executor.

```python
@dataclass
class GroundedAction:
    action_name: str
    bindings: Dict[str, str]               # {var_name: concrete_value}, e.g. {'?zone': 'zone_SE'}
    completion_predicate: Optional[Predicate]  # None if completion is ProcessCompletion (§1.9)
    schema: ActionSchema                   # back-reference for decomposer
```

**Correction from previous version:** the back-reference field is `schema: ActionSchema`
(current name), not `operator: ActionOperator` (an older name found in some stale indexed
chunks — `ActionSchema` is confirmed current via `domain_knowledge.py`'s
`get_action_schema() -> Optional[ActionSchema]`). `completion_predicate` is `Optional` —
`None` specifically for `ProcessCompletion`-based actions (e.g. `wait_at`), not always present
as the previous contract implied.

All variables are fully resolved — no `Var` objects remain in a `GroundedAction`.

---

### 1.5 `AbstractPlan`

**Produced by `planner.py`**, consumed by simulator executor. Single task only.

```python
@dataclass
class AbstractPlan:
    goal_intention: str                    # τ the robot is pursuing
    actions: List[GroundedAction]          # ordered grounded action sequence
    estimated_total_cost: float = 0.0
    contingencies: Dict[str, Any] = field(default_factory=dict)   # future
    metadata: Dict[str, Any] = field(default_factory=dict)
```

---

### 1.6 `TaskInstance`

**Used in scenario definitions and agent task assignments** — the schema-level bindings
representation, distinct from `GroundedAction.bindings` (plain strings, post-grounding).

```python
@dataclass
class TaskInstance:
    schema: "TaskSchema"
    bindings: Dict[Var, Const]             # {Var("?item"): Const("item_1")}
```

---

### 1.7 `ProjectedPlan` — meta_planner-internal only

**Produced and consumed only by `meta_planner.py`.** Never handed to the executor. Under
the `single_task` strategy (DESIGN-16, the implemented default) a `ProjectedPlan` always
holds exactly one entry — the multi-entry shape is retained for the deferred
`full_reorder` strategy, which is not implemented.

```python
@dataclass
class Segment:
    start_pos: Tuple[float, float]
    start_step: float
    end_pos: Tuple[float, float]
    end_step: float

@dataclass
class ProjectedPlanEntry:
    abstract_plan: AbstractPlan
    estimated_start_step: int
    estimated_duration: int
    segments: List[Segment]

@dataclass
class ProjectedPlan:
    task_queue: List[str]        # task_instance_key() strings, not TaskInstance objects
    entries: List[ProjectedPlanEntry]
    total_estimated_cost: int
```

`spatial_zones` was removed — zone membership was rejected as a proximity criterion
(zones are arbitrary in size; co-location in one zone doesn't imply closeness). Replaced
by `segments`, which carry actual geometry for distance-based interference detection.
See `shared/trajectory_algorithms.py`.

---

### 1.8 `HypothesisKey`

**Defined in `shared/recognizer.py`, not `shared/types.py`** — a hand-written class
(not a `@dataclass`), despite living in this "canonical types" document. Documented
here because it crosses the recognizer → meta_planner boundary via `get_hypothesis()`.
See TODO-26 for the open question of whether it should move to `types.py`.

**Used by `IntentionRecognizer`** to represent one point in the hypothesis space — a
specific (task, parameter-binding) combination the recognizer tracks belief over.

```python
@dataclass
class HypothesisKey:
    task_name: str
    bindings: Dict[str, str]               # {} for parameterless tasks (e.g. coffee_break)
```

One `HypothesisKey` exists per combination in the cartesian product of a task's
`parameter_types` over `known_objects_by_type` — see `build_hypothesis_space()`, §2.1.

---

### 1.9 `ExecutorState`, `TriggerDecision`, `UpdateResult`

**`ExecutorState`** — single immutable per-tick snapshot, built once per cognitive-clock
event and passed to both `evaluate_triggers()` and `update()` so they never independently
re-derive robot state and drift apart.

```python
@dataclass
class ExecutorState:
    agent_id: str
    current_task: Optional[TaskInstance]
    holding: Optional[str]                 # item_id or None
```

**`TriggerDecision`** / **`UpdateResult`** — typed returns for `MetaPlanner`'s two public
methods (§2.2), replacing an earlier dict-shaped draft inherited from `replanning.py`'s
`should_replan()`. Kept consistent with every other cross-boundary type in this file.

```python
@dataclass
class TriggerDecision:
    replan: bool
    reason: str
    score: Optional[float] = None

@dataclass
class UpdateResult:
    current_task: Optional[TaskInstance]   # None = all tasks complete (see §2.2, Update)
    queue: List[TaskInstance]
```

**`ConflictPoint`** / **`InterferenceAssessment`** — interference-detection output.
`_detect_interference()` observes; `_cost()` values. The separation is deliberate
(DESIGN-08): conflicts are computed and carried but not currently priced.

```python
@dataclass
class ConflictPoint:
    step: float                            # may be fractional — continuous sampling
    position: Tuple[float, float]          # midpoint between the two agents
    distance: float                        # actual Euclidean separation at this point

@dataclass
class InterferenceAssessment:
    feasible: bool                         # False = candidate excluded before costing
    conflicts: List[ConflictPoint]         # all observed, feasible or not
```

No `zone` field: zone co-occupancy was rejected as a proximity criterion (zones are
arbitrary in size, so co-location implies nothing about closeness). See
design_decisions.md, "Interference is geometric, not zone-based."

---

### 1.10 `task_instance_key()`

**Free function in `shared/types.py`**, not a method. Derives a stable identity string
for a `TaskInstance` (schema name + sorted bindings), used for `ProjectedPlan.task_queue`.
`TaskInstance` has no `id` field and its `bindings` dict is unhashable, so it cannot be a
set member or dict key directly.

```python
task_instance_key(task: TaskInstance) -> str    # "deliver_item(?item=item_3)"
```

Two `TaskInstance`s with identical schema+bindings produce the same key by design — that
is correct, not a collision to guard against. Mirrors `HypothesisKey.__repr__`'s pattern.

---

## 2. Module Contracts

### 2.1 `IntentionRecognizer` (`shared/recognizer.py`)

#### Constructor

```python
IntentionRecognizer(
    knowledge: DomainKnowledgeBase,
    context: ContextKnowledge,             # background facts for ω_context weighting
    hypotheses: List[HypothesisKey],       # precomputed hypothesis space for this scenario
)
```

**Correction from previous version:** this is a 3-argument constructor, not
`IntentionRecognizer(knowledge)`. `hypotheses` is built once at agent construction time via
the free function below, derived from the human agent's `scheduled_tasks`.

```python
def build_hypothesis_space(
    knowledge: DomainKnowledgeBase,
    known_objects_by_type: Dict[str, List[str]],   # workspace/layout data, not domain knowledge
) -> List[HypothesisKey]:
    ...
```

Takes the cartesian product of `known_objects_by_type[type]` over every entry in each
task's `TaskSchema.parameter_types`. Degenerates to one hypothesis for parameterless tasks.

#### Update

```python
update(
    obs: Observation,
    world: WorldState,
    prev_belief: BeliefState | None = None,
) -> BeliefState
```

**Correction (September 2026):** the previous contract omitted `world: WorldState`. It is a
required positional parameter — the recognizer needs world predicates and positions for
likelihood evaluation. Confirmed against `shared/recognizer.py` and the call site in
`mesa_sim/sim_agents.py`. The recognizer holds no belief internally: `prev_belief` comes in,
a new `BeliefState` goes out, and the caller owns the state.

Dispatches by schema-declared `microactions` membership and `progress_evaluator` name —
never by hardcoded microaction strings. See `design_decisions.md`, "IR likelihood dispatch."

#### Get Hypothesis

```python
get_hypothesis(hypothesis_key: str) -> Optional[HypothesisKey]
```

Resolves `belief.most_likely` back to its concrete task name and bindings — used by
`meta_planner.py` to ground the predicted human task without re-parsing the repr string.
Answers Q2 (Phase 4C design session): no separate geometric inference step is needed for
binding resolution.

---

### 2.2 `MetaPlanner` (`shared/meta_planner.py`) — IMPLEMENTED (`single_task` path)

Verified against `shared/meta_planner.py` and validated end-to-end against `scenario_00`
(September 2026). The `full_reorder` strategy is **not** implemented — `update()` and
`_project()` both raise `NotImplementedError` for it (DESIGN-16).

Private methods (`_project`, `_build_segments`, `_detect_interference`, `_cost`,
`_estimate_duration`) are internal to the class and deliberately not part of this contract;
only the constructor and the two public methods below are cross-boundary surface.

#### Constructor

```python
MetaPlanner(
    knowledge: DomainKnowledgeBase,
    recognizer: IntentionRecognizer,
    theta: float = 0.75,
    assumed_speed: float = 1.0,
    default_action_cost: float = 1.0,
    min_safe_distance: float = 1.0,
    strategy: Literal["single_task", "full_reorder"] = "single_task",
    interference_algorithm: Callable = discretized_time_sampling,
    human_agent_id: Optional[str] = None,
)
```

Owns the task queue internally (Q1) — not passed in on each call. `theta` is a cognitive-
clock policy parameter (DESIGN-07), kept as an explicit constructor default rather than
read from `costs.yaml` — `costs.yaml` holds domain-specific step costs, a different concern
from IR confidence-gating.

`recognizer` is the **same live instance** the owning agent holds, not a second one built
here — `get_hypothesis()` is a static lookup built once at recognizer construction and is
stateless with respect to belief, so holding this reference carries no staleness risk. It
also avoids constructor bloat (`context`, `hypotheses`) and a redundant unused `_history`.

`strategy` and `interference_algorithm` are swap points (DESIGN-16, DESIGN-10).
`human_agent_id=None` means no human projection is built and every candidate is treated as
feasible — mirroring `RobotAgent.observed_agent_id`'s existing optionality.

`assumed_speed`, `default_action_cost`, and `min_safe_distance` are **uncalibrated
placeholders**, not tuned values (TODO-28).

#### Evaluate Triggers
```python
evaluate_triggers(
    belief: BeliefState,
    world: WorldState,
    executor_state: ExecutorState,
) -> TriggerDecision
```
Event-driven only. Exactly three conditions (DESIGN-07, resolved):

- `no_current_task` — `executor_state.current_task is None`. Covers **both** t=0 and ordinary
  task completion in one condition; there is no separate initialization path. This assumes the
  embodiment layer clears `current_task` when a task's plan finishes.
- `theta_crossed` — confidence crosses θ from below to at-or-above (`prev < θ ≤ current`).
  A *crossing event*, not `confidence >= θ` per tick, which would refire continuously.
- `task_committed` — `executor_state.holding` transitions `None → not-None`.

θ=0.75, single threshold, no hysteresis. Confidence is a gate here, never a magnitude fed
into `_cost()`. `MetaPlanner` owns `_prev_belief`/`_prev_executor_state` internally — unlike
the retired `should_replan()`, these are not parameters.

#### Update
```python
update(
    belief: BeliefState,
    world: WorldState,
    executor_state: ExecutorState,
) -> UpdateResult
```
`current_task` competes as just another candidate — no special-case WAIT/RESELECT branch;
continuation vs. reselection falls out of cost comparison across the full candidate set.
Cancellation cost is not computed here — resolved intrinsically by `planner.py`'s guarded
method selection on the task itself (`deliver_with_return`, see `design_decisions.md`).

**Queue invariant:** `self._queue` holds only tasks NOT currently executing; the in-progress
task lives solely in `ExecutorState.current_task`. Candidates = `[current_task] + queue`.

**Strategy (DESIGN-16).** "Candidate" always means an individual task, never an ordering.
`self._strategy` controls only how much of the queue one `update()` call rewrites:

- `single_task` (default, implemented) — each candidate is projected alone from the live
  `WorldState`, infeasible ones dropped, argmin becomes the new `current_task`. The rest of
  the queue carries no ordering commitment; it is re-decided at the next trigger.
- `full_reorder` (not implemented) — would score permutations of the candidate set and
  replace the whole queue. Blocked on cross-task `WorldState` propagation (TODO-07).

The human's projection is built once per call via `recognizer.get_hypothesis(belief.most_likely)`
and reused for every candidate. If `human_agent_id is None`, or the hypothesis cannot be
resolved, no interference check runs that call and every candidate is treated as feasible.

**Terminal state:** `update()` returns `UpdateResult(current_task=None, queue=[])` when no
candidates remain — all assigned tasks are complete. Callers check
`result.current_task is None`. Task exhaustion is never signalled by exception; "all tasks
done" is a fact `shared/` discovers about its own state, so it is returned through the
contract rather than raised for the embodiment layer to catch and reinterpret.

`update()` does still raise `RuntimeError` when candidates exist but **every** one is
excluded as infeasible — a genuine anomaly, deliberately distinguishable from exhaustion.

#### Seed Tasks
```python
seed_tasks(tasks: List[TaskInstance]) -> None
```
Loads the initial task pool. Does **not** order it — Q0 comes from the first `update()` call,
fired by `no_current_task`, through the identical pipeline used for every later
re-evaluation. There is no base-cost heuristic and no special t=0 path. Called once by the
embodiment layer at agent construction (see TODO-35 on its placement).

---

### 2.2b `trajectory_algorithms` (`shared/trajectory_algorithms.py`)

Pure free functions operating on `Segment` / `ConflictPoint` — no classes, no state, no
simulator imports. Two families, each a deliberate swap point rather than fixed logic.
`MetaPlanner` selects the interference algorithm via its `interference_algorithm`
constructor parameter, so replacing one never requires editing `_detect_interference()`.

**Path realization** — how one action's motion is computed:
```python
straight_line_path(start_pos, start_step, end_pos, assumed_speed) -> Segment
stationary_segment(pos, start_step, duration) -> Segment          # non-movement actions
obstacle_aware_path(...)                                          # NOT IMPLEMENTED
```
`obstacle_aware_path()` is the documented placeholder for DESIGN-13 / TODO-09's
non-linear, obstacle-aware realization (Phase 4D). Note it may require `Segment` itself to
grow (e.g. a waypoint list), since a non-linear path is not captured by a start/end pair.

**Interference detection** — given two `Segment`s, where and how close do they get:
```python
discretized_time_sampling(segment_a, segment_b, interval=1.0) -> List[ConflictPoint]
closest_point_of_approach(segment_a, segment_b) -> List[ConflictPoint]   # NOT IMPLEMENTED
```
Both are symmetric in their arguments and return an empty list when the segments do not
overlap in step-time. `discretized_time_sampling()` is the current default;
`closest_point_of_approach()` (CPA) is documented with its analytic approach but unbuilt —
exact rather than sampled, no interval tradeoff, but with real edge cases (clamping the
analytic minimum to the overlap window, near-zero relative velocity).

These functions **measure only and hold no policy**. The single policy decision — what
distance counts as unsafe — lives in `MetaPlanner._detect_interference()` as
`min_safe_distance`.

---

### 2.3 `AdaptivePlanner` (`shared/planner.py`)

#### Constructor
```python
AdaptivePlanner(knowledge: DomainKnowledgeBase)
```

#### Plan
```python
plan(
    my_intention: str,
    task_params: Dict[str, str],           # {"?item": "item_3"} — task-level bindings only
    agent_id: str,                         # executing agent, injected as ?agent, not in task_params
    belief: BeliefState,
    world: WorldState,
    current_plan: AbstractPlan | None = None,
) -> AbstractPlan
```

**Confirmed unchanged from the previous contract** — this signature matches the live
`shared/planner.py` exactly, including `task_params` as a flat `Dict[str, str]` (not
`Dict[Var, Const]` — that representation is `TaskInstance.bindings`, §1.6, a different,
earlier stage than what `plan()` consumes).

**Status:** guard evaluation, recursive decomposition, derived variable resolution, and
`?agent` binding propagation are all implemented (Phase 4B, complete). **Still TODO:**
cost-aware method selection (TODO-16) — deferred until `meta_planner.py`'s cost model exists.

---

### 2.4 `DomainKnowledgeBase` (`shared/domain_knowledge.py`)

```python
DomainKnowledgeBase.from_domain(domain: DomainModel, costs_path: str = None) -> DomainKnowledgeBase
```

Provides read-only access to:
- `get_task_schema(name) -> Optional[TaskSchema]`
- `get_all_intentions() -> List[str]`
- `get_assigned_intentions() -> List[str]`
- `get_foreseeable_intentions() -> List[str]`
- `get_intention_schemas() -> List[TaskSchema]`
- `get_action_schema(name) -> Optional[ActionSchema]`
- `get_microactions() -> List[str]`
- `get_tasks_for_action(action_name) -> List[TaskSchema]` — reverse lookup for IR
- `get_actions_for_microaction(mu) -> List[ActionSchema]` — reverse lookup for IR
- `get_cost(key) -> Optional[float]` — reads from `costs.yaml` if loaded

**Deliberately absent:** no `get_objects_by_type()` method. `known_objects_by_type` is
workspace/layout data, not domain knowledge — it's passed as a parameter into
`build_hypothesis_space()` directly, not queried through this class. See
`design_decisions.md`, "`TaskSchema.parameter_types`."

**Companion class, not in previous contract:** `ContextKnowledge` — background context facts
(shift info, environment state) used by IR for ω_context weighting. Required constructor
argument for `IntentionRecognizer` (§2.1).

**No simulator imports allowed.**

---

## 3. Domain Knowledge Structure (`domains/<domain>/`)

Domain knowledge lives outside `shared/` in domain-specific Python packages.

```
domains/kitting/
    tasks.py           # TaskSchema definitions — HTN non-primitive tasks
    actions.py          # ActionSchema definitions — HTN primitive tasks (leaves)
    registry.py        # builds DomainModel, declares intention set
    scenarios.py       # ScenarioConfig objects — typed Python, no YAML
    env_layout0.json   # environment spatial layout (one file per layout)
    env_layout1.json
```

**Corrections from previous versions:** the file is `actions.py`, not `ActionSchemas.py`;
layout files are `env_layout0.json` / `env_layout1.json`, not `env1_layout.json`. Each
layout carries its own scenarios, registered in `registry.py`'s `domain_config["layouts"]`.

**HTN alignment:**
- `TaskSchema` = non-primitive task — decomposes via `MethodSchema`
- `ActionSchema` = primitive task — executable leaf, not decomposed further in HTN layer
- Mesa expands primitive actions into microactions via `action_decomposer.py` — embodiment detail only

---

## 4. Simulator Responsibilities

### 4.1 Mesa (`mesa_sim/`)

- Maintains perfect synchronous ground truth
- Builds `Observation` each step from human agent state (`detected_microaction` known exactly)
- Builds `WorldState` each step from Mesa world — emits `in_zone` and `at` predicates
- Calls cognitive loop each step: `obs_builder → recognizer → meta_planner
  (evaluate_triggers/update, §2.2) → planner → executor`
- Builds one `ExecutorState` per step and passes the same instance to both
  `evaluate_triggers()` and `update()` — never re-derives it between the two calls
- Clears `current_task` on task completion (this is what makes `no_current_task` fire) and
  sets its own `finished` flag when `update()` returns `current_task=None`
- Executes `GroundedAction` via `action_decomposer.py` → microaction queue → one microaction per step

### 4.2 ROS (`ros_sim/`)

- Maintains continuous noisy streams
- Must infer discrete microaction labels **outside core** before calling IR
- Builds `Observation` per window/event, `WorldState` from TF/perception
- Calls core functions on cognitive-layer events — never on a fixed timer, never derived
  from the motion-clock (PRIEST) tick rate. See `ros_sim/ros_sim_guideline.md` for the
  full constraint and a concrete case of this anti-pattern found in an early integration.
- Executes `GroundedAction` via ROS action servers

---

## 5. Non-Goals (explicitly out of scope)

- Exact probabilistic update equations
- Exact planning algorithms
- ROS classifier implementation
- Motion planning, collision checking, control loops
- Visualization or experiment tooling

---

## 6. Validation Rules

Simulators MUST ensure:

1. `Observation.detected_microaction` is never empty
2. `BeliefState.distribution` sums to 1.0 (±1e-6)
3. `BeliefState.most_likely` is a key in `distribution`
4. `WorldState.predicates` contains at minimum `in_zone` predicates for all active agents
5. `AbstractPlan.actions` is a non-empty list of fully grounded `GroundedAction` objects
6. No `Var` objects remain in any `GroundedAction.bindings` or `completion_predicate`
7. All intention names in `BeliefState.distribution` are registered in `DomainModel.intentions`
8. `ExecutorState` is built once per cognitive-clock event and passed unchanged to both
   `evaluate_triggers()` and `update()`
9. `ExecutorState.current_task` is cleared to `None` when a task's plan completes — omitting
   this silently disables the `no_current_task` trigger and the robot never advances
10. A task's `MethodSchema` set covers every world state that task can start *or resume*
    from — plans are re-decomposed from scratch at every trigger, never resumed from a
    cursor (see design_decisions.md)

---
