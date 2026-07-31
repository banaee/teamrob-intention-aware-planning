# shared/io_contracts.md

This document defines the **minimal, simulator-agnostic I/O contracts** for the cognitive core in `shared/`.
Implementation details (Bayes, HTN search, etc.) are intentionally omitted.
All simulators (Mesa, ROS) must translate their internal data into these canonical forms.

**Regenerated in full** against current `shared/types.py`, `shared/planner.py`,
`shared/domain_knowledge.py`, `shared/recognizer.py` — the previous version had drifted
significantly (missing `meta_planner.py` entirely, wrong `Observation`/`BeliefState` field
names, stale `IntentionRecognizer` constructor, stale filenames). One item below is flagged
as an open discrepancy rather than silently resolved — see §1.3.

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

**Produced by IR**, consumed by `meta_planner.py` (proposed) and `replanning.py` (current).

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

**Produced by simulator**, consumed by `planner.py`, `replanning.py`, and `meta_planner.py` (proposed).

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

**Status note, not a silent assumption:** `object_positions`/`agent_positions` are included
here because `design_decisions.md` records them as decided, deliberate design — the same
treatment given to `meta_planner.py` (§2.2), which is also documented ahead of being built.
Unlike `meta_planner.py`, there's no clean "NOT STARTED"-style signal for these two fields —
it's genuinely unclear whether they're implemented and my search just didn't surface them,
or genuinely not yet added to the dataclass. Confirm directly against `shared/types.py`
before depending on this in code.

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

**Design rule:** core planners only use symbolic predicates; geometry stays in simulators
(subject to the §1.3 discrepancy above, which is the one narrow exception if it exists).

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

**Produced and consumed only by `meta_planner.py`** (proposed, not yet implemented — see
§2.2). Never handed to the executor. Multi-task lookahead across a candidate ordering, used
for interference detection and cost comparison.

```python
@dataclass
class ProjectedPlanEntry:
    abstract_plan: AbstractPlan
    estimated_start_step: float
    estimated_duration: float
    spatial_zones: List[str]

@dataclass
class ProjectedPlan:
    task_queue: List[TaskInstance]
    entries: List[ProjectedPlanEntry]
    total_estimated_cost: float
```

**Invariant:** only `AbstractPlan` (single task) crosses the meta_planner → planner →
executor boundary. `ProjectedPlan` never does.

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
    current_task: TaskInstance
    queue: List[TaskInstance]
```

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
    prev_belief: BeliefState | None = None
) -> BeliefState
```

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

### 2.2 `MetaPlanner` (`shared/meta_planner.py`) — PROPOSED, not yet implemented

Per `roadmap.md`, Phase 4C is 🔲 NOT STARTED — this section documents resolved design
questions (Q1–Q4, DESIGN-07, DESIGN-09, the cancellation resolution), not verified code.
Confirm against actual `shared/meta_planner.py` once it exists, before relying on exact
signatures.

#### Constructor
```python
MetaPlanner(knowledge: DomainKnowledgeBase, theta: float = 0.75)
```
Owns the task queue internally (Q1) — not passed in on each call. `theta` is a cognitive-
clock policy parameter (DESIGN-07), kept as an explicit constructor default rather than
read from `costs.yaml` — `costs.yaml` holds domain-specific step costs, a different concern
from IR confidence-gating.

#### Evaluate Triggers
```python
evaluate_triggers(
    belief: BeliefState,
    world: WorldState,
    executor_state: ExecutorState,
) -> TriggerDecision
```
Absorbs `replanning.py`'s trigger role (§2.2a). Event-driven only — task completion, belief
threshold θ crossed (single threshold θ=0.75, no hysteresis), or task commit (holding state
change). Confidence is a gate here, never a magnitude fed into `_cost()`.

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

---

### 2.2a Replanning Trigger (`shared/replanning.py`) — current, transitional

```python
should_replan(
    current_plan: AbstractPlan | None,
    new_belief: BeliefState,
    world: WorldState,
    prev_belief: BeliefState | None = None,
) -> dict   # {"replan": bool, "reason": str, "score": float | None}
```

**This is the actually-callable trigger mechanism today.** Held wired in parallel (Q4) until
`meta_planner.py` validates end-to-end against `scenario_00`, then retired in one commit — at
that point §2.2a is deleted from this document, not just marked superseded.

**Notes**
- Simulators decide WHEN to call this — Mesa calls every step; ROS ties this to
  cognitive-layer events, never a fixed timer or the motion-clock tick rate.
  "Periodically" is not a valid calling pattern on either backend.
- Core never schedules itself

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
    env1_layout.json   # environment spatial layout
```

**Correction from previous version:** the file is `actions.py`, not `ActionSchemas.py`.

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
- Calls cognitive loop each step: `obs_builder → recognizer → meta_planner (absorbs
  replanning's trigger role via evaluate_triggers(), §2.2) → planner → executor`
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

---
