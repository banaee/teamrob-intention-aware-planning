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

**Re-aligned after T7/T8 and the Phase 4C wait-decision revision (September 2026)** for §1.9,
§2.2 and §2.2b: the task pool's completion drop, the `[meta-proj]` reason set, and the
realization design — a per-candidate `realize()` whose holds price conflict as duration and
reach the executor as a hint. Where a paragraph below is marked PLANNED it describes the
contract realization will add; the code at this alignment still runs the superseded
`_detect_interference()` / `min_safe_distance` path, byte-identically to the T7/T8 baselines.

**Re-aligned after R1 and T9 (September 2026)** for §1.9, §2.2, §2.2b, §4.1 and §6: the realization
decisions taken after T1b (one hold δ at the trigger position, the whole-trajectory minimal shift;
realizable = no violation within [trigger, T_h]; cost = T_r + δ; `min_separation` = 2.5 × motion per
tick; all-unrealizable → plain cost; `b2a` with ρ) and the arrival radius the body now supplies to the
`Projector`. PLANNED paragraphs describe what T3 / T4 / T10 build; the code at this alignment runs
the old B3 path (`_detect_interference()`, `min_safe_distance = 1.0`, the `RuntimeError`).

**Re-aligned after T3 and T3b (September 2026)** for §1.11 and §2.2c: `realize()` and `RealizedPlan`
exist (`shared/realization.py`, `shared/types.py`) as a standalone service, validated against T1b's
`whole` realizer on eight conditions; the hold δ is in whole ticks and T_r fractional (T3b). Nothing
consumes them yet: `MetaPlanner` still runs the old B3 path, and the sweep is byte-identical to the L2
baselines. The remaining PLANNED paragraphs are T4's (`b2a`) and T10's (B3 on realized cost, the plain
cost as `projected_duration`, `UpdateResult.hold`, the executor's hint).

**Re-aligned after T4 and T10 (September 2026)** for §1.9, §2.2, §2.2b, §2.2c and §4.1: realization is
CONSUMED. B2 `b2a` realizes the current task alone (T4); B3 realizes every candidate and selects on
`RealizedPlan.cost` = T_r + δ, with the all-unrealizable fallback to the plain `projected_duration`
(T10). `UpdateResult.hold` carries the decision's δ and Mesa executes it as STAND ticks. The old B3
path — `_detect_interference()`, `_cost()`, `min_safe_distance`, the `interference_algorithm`
parameter, the `RuntimeError` — is gone; `MetaPlanner` takes `cost_strategy` ("realized" | "plain").
No PLANNED paragraph remains in these sections.

**Re-aligned after F1 (September 2026)** for §1.11, §2.2, §2.2b, §2.2c, §4.1 and §6: robot-responsible
separation. A violation is the robot MOVING within `min_separation` without the distance strictly
increasing; a standing robot never violates. The hold-position check (`first_approach_step`) and the
hold cap are gone, so `realize()` always returns a cost: `RealizedPlan` has no `realizable` flag and
only the reasons `realized` / `no_human_projection`; B3 has no fallback, B2 no escalate-on-unrealizable.
The `Projector` additionally takes the body's task-completion tick.

**Re-aligned after R2 (September 2026):** the `Projector` takes the body's `duration_to_steps`
conversion, and a stationary action whose schema names a duration binding (`ActionSchema.duration_key`;
`wait_at`'s `?duration`) is projected at that duration (TODO-32 closed).

**Re-aligned after F47b (September 2026)** for §4.1 and §6: a scheduled or assigned task's bindings are
TYPED — every bound object exists in the layout with the type the schema's `parameter_types` declares —
and the embodiment checks this at spawn (`shared.types.check_task_bindings`), an error, not a warning.

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

**Produced by simulator** (`mesa_sim/world_state_builder.py`), consumed by `planner.py`,
`recognizer.py`, `projection.py` and `meta_planner.py`. Ephemeral: rebuilt every tick, never stored.

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
    agent_states: Dict[str, AgentState]                          # {agent_id: AgentState}
    agent_positions: Dict[str, Tuple[float, float]] = {}         # {agent_id: (x, y)}
    object_locations: Dict[str, str] = {}                        # {object_id: location_id}, symbolic;
                                                                 # a carried object maps to its holder's agent id
    predicates: Set[Predicate] = set()
    object_zones: Dict[str, str] = {}                            # {item_id: zone_id}
    object_home_container: Dict[str, str] = {}                   # {item_id: original container_id}; static per
                                                                 # scenario, for the deliver_with_return guard
    object_positions: Dict[str, Tuple[float, float]] = {}        # {obj_id: (x, y)}: env objects and items
    metadata: Dict[str, Any] = {}
# (every `= {}` / `= set()` is a field(default_factory=...) in shared/types.py)
```

**Positions: the scoped exception.** `agent_positions` and `object_positions` are read in `shared/`
through one lookup, `shared/target_resolution.py`: `movement_target_position(action, world)` resolves a
grounded movement action's `movement_target_key` binding to the object's CURRENT position (a carried object
is wherever its holder is: `object_locations` names the holder, whose position is in `agent_positions`).
Grounding itself (which method, which bindings) is the planner's `decompose()`; target resolution does not
re-implement it. Two consumers:
- the recognizer's progress channel: the `excess_path` evaluator (`shared/likelihood_functions.py`,
  `excess_path_likelihood`) scores a movement stretch against its target's position (§2.1);
- the `Projector` (`shared/projection.py`), which builds the `Segment`s of a projection (§1.7) from the
  agent's position and the resolved targets.
`planner.py` and `executor.py` stay symbolic.

**Predicate naming convention (unchanged):**
- `in_zone(agent_id, zone_id)` — coarse zone-level context
- `at(agent_id, object_id)` — fine-grained object proximity, used by executor completion checking
- `holding(agent_id, item_id)` — agent is carrying item
- `obj_at(item_id, location_id)` — item rests at location

`in_zone` and `at` are intentionally distinct predicates. Conflating them caused a semantic
mismatch where `move_to` completion was never satisfied.

**Design rule:** core planners only use symbolic predicates; geometry stays in simulators, subject to the
scoped exception above (the recognizer's excess-path scoring and the Projector's segments).

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
    fired: bool                            # a cognitive-clock event occurred (was `replan`,
                                           # renamed: the consequence is the caller's business)
    reason: str
    score: Optional[float] = None

@dataclass
class UpdateResult:
    current_task: Optional[TaskInstance]   # None = all tasks complete (see §2.2, Update)
    queue: List[TaskInstance]
    hold: int = 0                          # the decision's hold δ, WHOLE ticks, at the robot's position
                                           # at the trigger tick (T4, T10) — see below. 0 when none was
                                           # placed (no human projection,
                                           # cost_strategy "plain", the terminal return).
```

**A continue decision (T5, TODO-43).** `update()` returning a `current_task` whose
`task_instance_key()` equals that of the `ExecutorState.current_task` it was given is a CONTINUE.
The embodiment must keep executing without interruption: no lost tick, no restart of the action
in flight, no observable difference from a tick on which no trigger fired. The task is still
re-decomposed from the live world (§2.3; plans are never resumed) and the fresh plan replaces the
one in flight — it may legitimately differ, and under realization it will carry the holds priced
on this trigger — but execution progress through the current action survives the swap. Identity
is the key, never object identity (`update()` happens to return the same `TaskInstance` object
today; the contract does not promise it) and never a domain string. A continue is not a second
decision path: which task is selected is `update()`'s alone, and the embodiment gains no rule
about when to re-plan. See design_decisions.md, "A continue decision costs nothing".

**The hold** (Phase 4C wait-decision revision, September 2026; amended at R1; BUILT T4 for B2, T10
for B3; design_decisions.md, "The robot can wait"). `update()` returns, with the winning task, the
HOLD its realization placed: ONE δ (whole ticks), taken at the robot's position at the trigger tick —
which may be partway along a walk — after which the plan runs unchanged (the whole-trajectory
minimal shift, TODO-70). There is no per-segment hold. It is B2's realization of the current task on
a `b2a` continue, or the winner's realization in B3, whether the winner is the current task or
another. Semantics across the boundary:

- It is an execution HINT, in the sense of design_decisions.md's first key decision: a preplan
  that saves the executor solving avoidance from scratch. The human may deviate within a few
  ticks, and each embodiment's own collision handling differs, so the executor may REFINE a
  hold (shorten or extend it as the world shows the way clear or blocked).
- It is not optional. The decision — which task, and that it waits — is made ONCE, in `shared/`.
  The embodiment must not decide independently whether to wait, which task to run, or drop the
  hold silently: the cost the task won on was computed with that hold, and a behaviour that
  departs from it silently leaves neither the cost nor the behaviour authoritative (the
  single-decision-path rule, §4.2 and TODOS_AND_DEFERRED.md). Refinement is the whole of the
  executor's latitude.
- Mesa executes the hold as δ STAND microactions at the trigger position, then continues the
  plan (TODO-71) — unless a later trigger re-decides, in which case the fresh `update()` re-realizes
  from wherever the robot then is (a hold re-realized identically keeps its countdown, §2.2 Continue).
  ROS treats it as a soft constraint on PRIEST, as it treats every hint.
- A hold is a POSITION: the robot waits where it is. Waiting elsewhere is a detour, a different
  realization strategy (Phase 4D).
- What the hold was computed on: no violation (robot–human distance below `min_separation`) within
  [trigger, T_h], T_h the end of the human's projection. Beyond T_h the plan is UNASSESSED — neither
  clear nor blocked — and is the execution layer's (design_decisions.md, "Assumption: execution-time
  avoidance past T_h").

**`ConflictPoint`** / **`InterferenceAssessment`** — REMOVED (TODO-83). They were the output of the
batch interference profile that realization REPLACED (T10); nothing produced or consumed them after
`_detect_interference()`, `_cost()` and `discretized_time_sampling()` went. `RealizedPlan` (§1.11) is what
the meta-planner consumes. Under realization a conflict is priced by construction — as the duration of the
hold that avoids it — and the observe / value split survives inside realization
(`shift_violation_interval` observes; holding values). `realize()` takes the projected segments of
whatever ordering it is given — it does not assume a single task.

Interference stays geometric, never zone co-occupancy (zones are arbitrary in size, so co-location
implies nothing about closeness). See
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

### 1.11 `RealizedPlan` (T3)

**Produced by `realize()` (§2.2c); consumed by `MetaPlanner` (T4's B2, T10's B3).** What a
candidate's trajectory actually is, given the human: the hold-only realization under the
whole-trajectory minimal shift (design_decisions.md, "The robot can wait", the R1 decisions).

```python
@dataclass
class RealizedPlan:
    delta: int                            # the hold, WHOLE ticks ≥ 0 (T3b); 0 without a human projection
    cost: float                           # T_r + delta over the FULL plan
    projected_duration: float             # T_r: the span of the plan's segments (fractional steps)
    segments: List[Segment]               # the hold (stationary, when of positive duration) then every
                                          # projected segment shifted by delta
    hold_position: Tuple[float, float]    # the plan's first segment's start: where the robot is at the decision step
    hold_start: float                     # the decision step
    horizon: Optional[float]              # T_h, the end of the human projection; None without one
    unassessed_share: float               # share of [hold_start, realized end] beyond T_h; 1.0 without a
                                          # human projection, or when the hold pushes the plan past T_h
    reason: str                           # "realized" | "no_human_projection"
```

Since F1 (robot-responsible separation, §2.2c) realization is TOTAL: a clearing shift always exists, so
there is no `realizable` flag and no unrealizable reason. The former `realizable: bool`,
`hold_position_violated` and `hold_reaches_horizon` are gone.

- `cost` is the ONE number a candidate competes on (T10): T_r + δ, walking plus the hold. The tail
  beyond T_h is inside T_r and not corrected for (TODO-69, reading (1)); the share is logged so the
  bias can be reported, not priced.
- `delta` is what reaches the executor as the hold hint (§1.9, TODO-71): stand at `hold_position`
  for `delta` steps, then the plan.
- Every plan has a realized cost to rank on (F1); the R1 fallback for "no candidate realizes" was
  built at T10 and removed at F1 (§2.2).
- `reason == "no_human_projection"` is the shape of "no projection admitted": δ = 0, cost = T_r,
  share 1.0. A caller may treat it exactly as it treats `human_projection is None` today.
- **Quantisation — DECIDED (T3b; design_decisions.md, "Realization as built").** `delta` is in
  WHOLE ticks: the smallest whole-tick shift that clears the assessed window, walked over the exact
  violating intervals (not the fractional minimum rounded up — feasibility in δ is not monotone, so
  ceil can land in a second violating interval and the walk continues past it). Reasoning: the hold
  is executed as STAND ticks, so the plan that is checked and costed must be the plan that is
  executed; rounding at execution would break the separation (down; the minimal shift has no
  margin) or leave the executed plan unchecked (up). T_r STAYS FRACTIONAL: it is the projection's
  continuous duration; execution quantises per walk and that is deliberately not compensated (L2);
  rounding the total would model nothing and could only turn an order into a tie. `cost` is one
  quantity — the projected duration of the realized trajectory. CONSEQUENCE FOR T10: the plain cost
  `update()` compares in the no-projection path and the all-unrealizable fallback must be the same
  T_r, `projected_duration`, not `ProjectedPlan.total_estimated_cost` (its integer rounding).
- The steps before the human projection's span (the observation offset, L2) are unassessed and NOT
  in `unassessed_share`, which counts the tail beyond T_h only (T3b ruling).
- A violation is strict: a single instant at exactly `min_separation` is not one (T3b ruling).

---

## 2. Module Contracts

### 2.1 `IntentionRecognizer` (`shared/recognizer.py`)

The current model is described in `docs/recognizer_handback.md` §1–§2 (the design record: the I2–I4d
entries in `design_decisions.md`). This section is the interface.

#### Constructor

```python
IntentionRecognizer(
    knowledge: DomainKnowledgeBase,
    context: ContextKnowledge,                        # background facts for ω_context weighting (output only)
    hypotheses: List[HypothesisKey],                  # precomputed hypothesis space for this scenario
    assigned_tasks: Optional[List[TaskInstance]] = None,   # OBSERVED agent's work order; None/empty = restriction off
    path_cost: Optional[PathCost] = None,             # C(a, b) for the excess path; straight line by default
)
```

`hypotheses` is built once at agent construction time via the free function below, from the domain schemas
and the objects present in the workspace — *not* from the human agent's `scheduled_tasks`, which the robot
never sees. The recognizer sorts them by `repr` (order-independent of the caller, TODO-42).

`assigned_tasks` carries the observed agent's work order — which tasks it was assigned, never in which order
it will do them. It restricts the SUPPORT, not the magnitude: the admissible set is the assigned tasks, every
foreseeable task (`TaskSchema.is_foreseeable`) and `unknown`; every other hypothesis is pinned at
`BELIEF_FLOOR` and never scored. Identity crosses the boundary as `task_instance_key()` (§1.10), which matches
`repr(HypothesisKey)` (§1.8); an assigned task matching no hypothesis is logged as a warning and ignored.
`None` or `[]` switches the restriction off (`--assignment_prior false`, the default).

`path_cost` is the cost of the walk between two positions that the excess path is measured against.
Straight-line distance by default (Mesa agents walk through obstacles); a domain or body with a better model
injects it. The constructor raises `ValueError` if a schema names a `progress_evaluator` not registered in
`likelihood_functions.PROGRESS_EVALUATORS`.

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

`world` is required: the phase is derived from it every tick. The recognizer OWNS its belief; `prev_belief`
is accepted for signature compatibility and not consulted (the reported distribution carries output-only
factors that must not be fed back).

Per live hypothesis, every tick:
1. **Phase, derived.** The planner decomposes the task against the current world for the observed agent (its
   guards select the method), the grounded actions are walked from the start, and the EXPECTED action is the
   first whose completion condition does not hold. Nothing stores an index into an action list.
2. **Completion.** If the task's terminal action's completion holds, the hypothesis is retired and pinned at
   the floor for the rest of the run, whoever completed it.
3. **Completion channel (an event).** A microaction in the declared vocabulary of the action the hypothesis
   expected on the previous tick is scored by detection reliability (`DETECTION_HIT_RATE` if that action's
   completion predicate holds, `DETECTION_FALSE_ALARM_RATE` if not) and multiplies into the evidence once.
4. **Phase change.** When the expected action changes, the closing stretch folds into the evidence once as
   odds L/u against `unknown` (nothing, if the stretch was empty), and the hypothesis's ORIGIN moves to the
   agent's position and odometer reading.
5. **Progress channel.** An action with a `progress_evaluator` (`excess_path`: `move_to`) is scored from the
   origin: excess = walked + C(pos, target) − C(origin, target), L = 2 / (1 + e^{β·excess}); one stretch
   toward one target is ONE observation, recomputed each tick and replacing the previous tick's value (v/u,
   on top of the evidence, never into it). An empty stretch is not an observation. An action with no graded
   signal scores the perfect-fit value.

`unknown` is the reference with the constant likelihood `UNKNOWN_LIKELIHOOD` (u) and takes no factor. The
episode is local: when a retirement is the observed agent's own (its expected action on the previous tick was
the terminal one), the belief re-initialises to the uniform prior over the live set and every origin moves to
the agent's position. Output = evidence × ω_context (`_context_weight`, output only), normalised, floored at
`BELIEF_FLOOR`, with completed and inadmissible hypotheses pinned.

Dispatches by schema-declared `microactions` membership and `progress_evaluator` name — never by hardcoded
microaction strings. See `design_decisions.md`, "IR likelihood dispatch."

Removed and not to return (handback §8): the leg model and the cosine trajectory kernel, the held-item rule,
`ZONE_BOOST`, the HIGH / LOW / NEUTRAL likelihoods, the 10× assignment multiplier, belief persistence across
an episode boundary.

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

Private methods (`_is_current_task_plausible`, `_replan_tasks`, `_is_complete`, `_clears_gate`)
are internal to the class and deliberately not part of this contract; only the constructor, the
public methods below and the read-only parameter properties (`theta`, `rho`, `min_separation`,
`gate_strategy`, `cost_strategy`; for the run-log header, TODO-78) are cross-boundary surface.
Projection (`project`, `build_segments`, `estimate_duration`) lives on `Projector`
(`shared/projection.py`), which is injected. Realization (`realize()`, §2.2c) lives on the
projection / trajectory side as well, not on `MetaPlanner`, which supplies `min_separation` and
consumes the `RealizedPlan` — once per candidate in B3 (T10) and once for the current task in B2
`b2a` (T4).

#### Constructor

```python
MetaPlanner(
    knowledge: DomainKnowledgeBase,
    projector: Projector,
    recognizer: IntentionRecognizer,
    theta: float = DEFAULT_THETA,        # 0.75, module-level in shared/meta_planner.py
    strategy: Literal["single_task", "full_reorder"] = "single_task",
    gate_strategy: Literal["none", "b2a", "b2b"] = "none",
    cost_strategy: Literal["realized", "plain"] = "realized",
    human_agent_id: Optional[str] = None,
    min_separation_in_motion_ticks: float = 2.5,
    rho: float = 0.5,
)
```

**Correction (September 2026):** `assumed_speed` and `default_action_cost` are `Projector`
constructor parameters, not `MetaPlanner`'s; `projector` is injected (one instance, held by
the agent); `gate_strategy` selects B2 — `"none"` (default) skips the gate entirely, `"b2a"` is
built (T4), `"b2b"` raises `NotImplementedError` (a documented stub). `cost_strategy` selects what
B3 selects on (T10; below). `min_safe_distance` and `interference_algorithm` were removed at T10.

Owns the task queue internally (Q1) — not passed in on each call. `theta` is a cognitive-
clock policy parameter (DESIGN-07), kept as an explicit constructor default rather than
read from `costs.yaml` — `costs.yaml` holds domain-specific step costs, a different concern
from IR confidence-gating. Its single definition is `shared.meta_planner.DEFAULT_THETA`
(September 2026; a second, unread copy in `recognizer.py` was deleted — the gate is the
meta-planner's decision, not a likelihood parameter). No call site passes `theta`, so the
default governs every run. θ is applied in exactly one private method,
`_clears_gate(belief) -> bool`, which both `evaluate_triggers()` (on the entering side of
`recognition_changed`, D2) and `update_human_projection()` (as admission) ask; it is deliberately one method so that a
change to how the bar is computed would not change where it is asked. See design_decisions.md,
"θ has one home". The gate ruling (September 2026) kept the fixed share: a derived θ (TODO-64)
and a margin gate (TODO-65) were considered and not taken; design_decisions.md, "The gate stays
a fixed share".

`recognizer` is the **same live instance** the owning agent holds, not a second one built
here — `get_hypothesis()` is a static lookup built once at recognizer construction and is
stateless with respect to belief, so holding this reference carries no staleness risk. It
also avoids constructor bloat (`context`, `hypotheses`) and a redundant unused `_history`.

`strategy`, `gate_strategy` and `cost_strategy` are independent switches; every combination is
meant to be runnable (DESIGN-16; TODO-36; the T6 ablation). `human_agent_id=None` means no human
projection is built and every candidate realizes with δ = 0 at its plain projected duration —
mirroring `RobotAgent.observed_agent_id`'s existing optionality.

**`min_separation`** (TODO-28; R1; landed T4 for B2, T10 for B3): the clearance realization must
ACHIEVE by holding, passed into `realize()` — not a threshold below which a candidate is excluded.
The policy value is the unit-less ratio `min_separation_in_motion_ticks` (2.5); the world-unit
`min_separation` handed to `realize()` is it × the `Projector`'s body-supplied `assumed_speed`
(50 cm in Mesa at 20 cm/tick), so `shared/` holds no absolute distance. One value, used by B2 and B3
alike; readable as `MetaPlanner.min_separation`.

**ρ** (`rho`, T4): `gate_strategy="b2a"` continues the current task when its hold δ ≤ ρ × (T_h −
trigger), the human's remaining projected duration; otherwise, or if the current task is
unrealizable, B3 runs. `human_projection is None` still means continue. 0.5 is a stated assumption
(T6 varies it), not a calibrated value.

**`cost_strategy`** (T10; F1): `"realized"` (default) — B3 realizes every candidate and takes the
argmin of `RealizedPlan.cost` = T_r + δ over all of them, carrying the winner's δ as the hold (since F1
every candidate realizes; the T10 all-unrealizable fallback is gone).
`"plain"` — the argmin of `projected_duration` alone, no human consideration, no hold, no filter; a
comparison condition for the T6 ablation, not a policy. Both use the same T_r (the fractional
segment span, never `ProjectedPlan.total_estimated_cost`), so their difference is realization's
effect alone.

`Projector` (T9) additionally takes the body's **stopping distance** (`arrival_radius`), supplied
exactly as `assumed_speed` is: Mesa passes the same constant that makes its `at(agent, object)`
predicate hold (`PROXIMITY_THRESHOLD`, 30 cm), so a projected walk ends where the executor stops
and the next action is projected from that point. Its default in `shared/` is a unit-less
placeholder (0.0), not a value `shared/` knows to be right.

`Projector` (R2, TODO-32) additionally takes **`duration_to_steps: Callable[[str], float]`**: the
body's conversion of the duration bound on a grounded action (the value under
`ActionSchema.duration_key` — `"?duration"` on `wait_at`, an ISO-8601 string the method schema binds)
into execution steps. Both the parser and the seconds one step lasts are body facts; Mesa hands in
`action_decomposer._parse_duration_to_steps` (over `mesa_configs.yaml`'s `seconds_per_step`), the
function its own `STAND*` expansion uses, so the projected wait and the executed wait are one number.
`shared/` reads the key from the schema and calls the callable; it holds no literal, no parser and no
constant. `None` (the default) leaves such an action at the cost lookup / `default_action_cost`.

#### Evaluate Triggers
```python
evaluate_triggers(
    belief: BeliefState,
    world: WorldState,
    executor_state: ExecutorState,
) -> TriggerDecision
```
Event-driven only. Exactly three conditions (DESIGN-07, resolved; the second replaced in D2):

- `no_current_task` — `executor_state.current_task is None`. Covers **both** t=0 and ordinary
  task completion in one condition; there is no separate initialization path. This assumes the
  embodiment layer clears `current_task` when a task's plan finishes.
- `recognition_changed` (D2) — the belief no longer points at the hypothesis the last decision was
  projected against. One condition read from two sides, against the **decision record**
  (`MetaPlanner._projected_hypothesis`: `belief.most_likely` on the tick `update_human_projection()`
  built a projection; `None` when admission refused or before any trigger fired):
  - a hypothesis is recorded and `belief.most_likely` is no longer it — replaced by another
    (TODO-48), the human's task ended and the belief re-initialised (the `[IR-boundary]` tick), or
    `unknown` took over after a pin (TODO-54). Admission then decides what, if anything, is
    projected next;
  - none is recorded and the belief clears `_clears_gate()` on a task hypothesis (not `unknown`,
    which admission refuses). The first recognition of a task, as `theta_crossed` fired it.

  The gate is asked at admission, never for retention: a recorded hypothesis that dips below θ while
  staying most likely fires nothing (TODO-68's repeated crossings) and keeps its projection until it
  is replaced, ends, or the human stops — an accepted consequence, recorded in the D2 entry; a margin
  or a duration on the dip would be a second threshold. Supersedes `theta_crossed` (the crossing
  `prev < θ ≤ current`, which fired on every re-crossing and never on a change of hypothesis).
- `task_committed` — `executor_state.holding` transitions `None → not-None`.

θ=0.75, single threshold, no hysteresis. Confidence is a gate here, never a magnitude fed
into a cost. `MetaPlanner` owns `_prev_executor_state` and the decision record internally —
unlike the retired `should_replan()`, these are not parameters. When two conditions hold on one
tick the order is `no_current_task`, `recognition_changed`, `task_committed`; only the reported
reason and score differ.

#### Update
```python
update(
    belief: BeliefState,
    world: WorldState,
    executor_state: ExecutorState,
    human_projection: Optional[ProjectedPlan],
) -> UpdateResult
```
`human_projection` is required (no default): the result of `update_human_projection()` for
this trigger, or `None`.
`current_task` competes as just another candidate — no special-case WAIT/RESELECT branch;
continuation vs. reselection falls out of cost comparison across the full candidate set. Under
the wait-decision revision that remains true with waiting added: a wait is a HOLD inside a
candidate's realized cost, not a branch.
Cancellation cost is not computed here — resolved intrinsically by `planner.py`'s guarded
method selection on the task itself (`deliver_with_return`, see `design_decisions.md`).

**Task pool (T7).** `update()` assembles `([current_task] if not None else []) + queue` and
drops every task already COMPLETE in `world` — its terminal condition holds, whoever made it
hold, by `AdaptivePlanner.is_complete()` — before any block runs, logging
`[meta-pool] <task> complete in world: dropped from the pool`. Completion is a world fact read
on every call, never a flag kept here; the executor's own bookkeeping lags it by up to two ticks.

**Queue invariant:** `self._queue` holds only tasks NOT currently executing; the in-progress
task lives solely in `ExecutorState.current_task`. Candidates = `[current_task] + queue`.

**Continue (T5).** Whether the winner is the executing task is decided by the caller with
`task_instance_key()` (§1.9, "A continue decision"); `update()` neither flags it nor treats it
differently — B2's continuation return and B3 re-selecting the current task are the same
outcome at the boundary. A continue costs the robot nothing; that is the embodiment's
obligation (§4.1), not a change to selection.

**Blocks.** 0: pool assembly (above); terminal return if empty. B1.5: no current task, or the pool
has just dropped the current task as complete in the world → straight to B3 (one owner of
completion: `update()` never continues a task its own pool dropped, whatever
`ExecutorState.current_task` still holds; T6 wrap-up). B2: `_is_current_task_plausible()`, the mid-task plausibility gate — `gate_strategy`
`"none"` (default) never continues; `"b2a"` (T4) realizes the current task alone (decision step 0,
`min_separation`) and continues with its hold δ when δ ≤ ρ × (T_h − 0), a COMMITMENT gate that can
only prevent a switch B3 would make; it escalates when δ is above the bound (since F1 there is no
unrealizable current task); `human_projection is None` → continue, hold 0. One `[meta-b2]` line per
call. `"b2b"` raises `NotImplementedError`. B3: `_replan_tasks()` (T10, F1) — every candidate projected
alone from the live world at decision step 0 and realized against `human_projection`; the argmin of
`RealizedPlan.cost` over all candidates wins (ties: pool order, `min()` keeps the first), its δ goes
out as `UpdateResult.hold`; the rest form the queue. When `human_projection` is `None` `realize()`
reports `no_human_projection` for every candidate (δ = 0, cost = T_r), so B3 is an argmin over
projected durations. One `[meta-cand]` line per candidate (`reason`, `T_r`, `delta`, `cost`, `share`)
and one `[meta-b3]` line per call (`trigger`, `cost_strategy`, `selection` ∈ `realized` |
`no_projection` | `plain`, `winner`, `cost`, `hold`, `T_h`, `candidates`).

**Strategy (DESIGN-16).** "Candidate" means the unit the argmin ranges over — an individual
task under `single_task`, a permuted ordering under `full_reorder` (design_decisions.md,
DESIGN-16, terminology). `self._strategy` controls only how much of the queue one `update()`
call rewrites:

- `single_task` (default, implemented) — each candidate is projected alone from the live
  `WorldState` and realized; the argmin of realized cost over the realizable candidates becomes
  the new `current_task`. The rest of the queue carries no ordering commitment; it is re-decided
  at the next trigger.
- `full_reorder` (not implemented) — would score permutations of the candidate set and
  replace the whole queue. Blocked on cross-task `WorldState` propagation (TODO-07).

The human's projection is built once per fired trigger by `update_human_projection()` (below)
and passed in as `human_projection`; it is reused for every candidate, never rebuilt here.
`human_projection=None` means every candidate is realized against no human plan — δ = 0, cost =
T_r (`reason="no_human_projection"`). It is never treated as always-conflicting. `None` is a
ROUTINE mid-run state, not an edge case: the belief re-initialises at every human task boundary
(I4c), so most `no_current_task` triggers and every trigger between the human's tasks run without
a projection.

**Terminal state:** `update()` returns `UpdateResult(current_task=None, queue=[])` when no
candidates remain — all assigned tasks are complete. Callers check
`result.current_task is None`. Task exhaustion is never signalled by exception; "all tasks
done" is a fact `shared/` discovers about its own state, so it is returned through the
contract rather than raised for the embodiment layer to catch and reinterpret.

**No unrealizable candidate** (F1). Under robot-responsible separation a clearing hold always exists,
so every candidate carries a realized cost and B3 needs no fallback: the T10 `all_unrealizable` path
(R1, TODO-30) is removed, as the `RuntimeError` was before it. Nothing is raised, nothing is excluded.

#### Update Human Projection
```python
update_human_projection(
    belief: BeliefState,
    world: WorldState,
) -> Optional[ProjectedPlan]
```
Called once per fired trigger, between `evaluate_triggers()` and `update()`; the result is
`update()`'s `human_projection` argument. Projection **admission** is decided here — a
MetaPlanner policy, not a `Projector` one — then delegated to `Projector.project_human()`.

Returns `None`, checked in this order, when:

- `belief.confidence < theta` — the projector is not called. θ gates admission as it gates
  triggering (DESIGN-07); it still never feeds `_cost()`.
- `human_agent_id is None` — no human observed.
- `belief.most_likely` is the recognizer's `unknown` (T8) — the projector is not called. Mass
  on `unknown` above θ is not a recognition and there is no trajectory to project. Reachable
  since the completion pin: a hypothesis retired by the robot's own delivery hands its mass to
  `unknown` (TODO-54). The trigger still fires on it (TODO-68).
- the hypothesis is unresolvable — `Projector.project_human()` returned `None` (its task name
  is not in the domain).

Emits one `[meta-proj] confidence=<c> theta=<θ> projection=<reason>` line per call, with
`reason` ∈ `built`, `none(below_theta)`, `none(no_human)`, `none(unknown)`, `none(unresolved)`.
No `step` or `trigger` field: both belong to the caller and are recoverable from the
`[meta-trig]` line of the same tick.

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

Pure free functions operating on `Segment` — no classes, no state, no simulator imports. Two
families: path realization and realization's closed-form interference geometry. Since T10 `MetaPlanner`
selects no interference algorithm; the batch sampler `discretized_time_sampling()`, its unbuilt
analytic alternative `closest_point_of_approach()`, and the body-side
`mesa_configs.yaml: simulation.interference_spatial_resolution` it was bound with were removed
(TODO-83).

**Path realization** — how one action's motion is computed:
```python
straight_line_path(start_pos, start_step, end_pos, assumed_speed) -> Segment
stationary_segment(pos, start_step, duration) -> Segment          # non-movement actions
obstacle_aware_path(...)                                          # NOT IMPLEMENTED
```
`obstacle_aware_path()` is the documented placeholder for DESIGN-13 / TODO-09's
non-linear, obstacle-aware realization (Phase 4D). Note it may require `Segment` itself to
grow (e.g. a waypoint list), since a non-linear path is not captured by a start/end pair.

**Realization's geometry (BUILT, T3; redefined F1)** — realization asks this family a different
question from "where do two fixed trajectories come close": for which SHIFTS of a robot segment is
there a violation against a human segment. Closed form; no sampling.
```python
shift_violation_interval(robot_segment, human_segment, min_separation) -> Optional[Tuple[float, float]]
```
`shift_violation_interval` returns the open interval of shifts d for which `robot_segment`,
delayed by d along the same path, VIOLATES robot-responsible separation against `human_segment` at
some moment both exist, or `None`. THE VIOLATION (F1; design_decisions.md, "Robot-responsible
separation"): the robot is MOVING, strictly within `min_separation` of the human, and the distance
is not strictly increasing — (a) the instant after its motion takes the distance below
`min_separation`, or (b) moving within it without the distance increasing. A standing robot never
violates (a stationary robot segment returns `None` at once); moving away never violates. It is ONE
interval by convexity: with u the robot's time into its segment, the relative position X is affine
in (u, d); "within `min_separation`" is an ellipse interior (or a strip), "not strictly increasing"
is the closed half-plane 2 X·B ≤ 0 (the whole plane when the velocities are equal), and the moments
both exist are a parallelogram; the intersection is convex and projects onto d as one interval,
whose endpoints are enumerated exactly (the vertices of the parallelogram clipped by the half-plane
that lie inside the disc, the roots of |X|² = s² along that polygon's edges, the ellipse's own
d-extrema inside it). Every interval is bounded, so a clearing shift always exists. The interval's
endpoints are where the violating set is touched, and are clear. `first_approach_step`, the former
hold-position check, was removed at F1. Tolerances are floating-point slack (1e-9 relative), not a
margin. `obstacle_aware_path()` becomes the detour strategy of realization (Phase 4D).

These functions **measure only and hold no policy**. The single policy value is
`min_separation`, the clearance realization must achieve; `MetaPlanner` supplies it and
realization is GIVEN it, so no policy enters the geometry (the former `min_safe_distance`
threshold in `MetaPlanner._detect_interference()` is gone, T10).

---

### 2.2c `realize()` (`shared/realization.py`) — BUILT (T3), consumed by B2 (T4) and B3 (T10), TOTAL since F1

The realization service (design_decisions.md, "The robot can wait"; the R1 decisions). Sits
between `trajectory_algorithms.py` and `projection.py` in the one-way layering: it reads
`ProjectedPlan`s and `Segment`s only, knows nothing of tasks, beliefs or selection, imports no
simulator, and holds no policy — `min_separation` is passed in. `MetaPlanner` calls it once per
candidate in B3 (T10; under `cost_strategy="plain"` with `human_plan=None`, so the plain cost is the
same `projected_duration`) and once for the current task in B2 `b2a` (T4), always at decision step
0.0, the trigger.

```python
realize(
    plan: ProjectedPlan,                  # the robot's; every entry's segments, in order — not assumed one task
    human_plan: Optional[ProjectedPlan],  # the admitted human projection, or None
    min_separation: float,                # world units; the caller's policy value
    decision_step: float,                 # the robot's now on the projection clock (0.0 at a trigger)
) -> RealizedPlan                         # always, with a cost (§1.11): a clearing shift always exists (F1)
```

**Policy (R1, TODO-70; the violation redefined at F1): the whole-trajectory minimal shift.** One hold
δ at the robot's position at `decision_step` (the plan's first segment's start, which may be partway
along a walk), then the whole plan shifted by δ. δ is the smallest shift ≥ 0 such that the shifted
trajectory has no violation in the assessed window, IN WHOLE TICKS (T3b) — a violation being the
robot's motion within `min_separation` without the distance increasing (§2.2b), so the stationary
hold is never one. Exact: the violating shift intervals (`shift_violation_interval`, one per MOVING
robot segment × human segment pair) are walked in order of their start;
δ starts at 0 and, whenever an interval strictly contains it, jumps to the first whole tick at or
after that interval's end. No search, no grid: the feasible set in δ is not monotone (a shift can
clear one crossing and walk into the next), so bisection would be invalid, a grid would make δ
sampled, and the whole-tick δ is not simply the fractional minimum rounded up.

**The assessed window** is where both projections exist and the realized plan lies within
[decision_step, T_h], T_h the end of the human projection: nothing past T_h is assessed or charged,
and nothing before the human projection's span (it starts at the observation offset, L2) is
assessed either. Segments are taken as they are — L2's stationary latency segments included —
and no stride is assumed.

**The hold is a position, and a standing robot never violates (F1).** The human may pass within
`min_separation` of the hold position, or through it, while the robot stands there; nothing bounds δ
from above. Head-on, same-line and "the human walks past the standing robot" conflicts realize as a
hold until the robot's own motion is clear. The human's detour around a standing robot is a
team-level cost (TODO-15), not priced here.

**No hold cap (F1).** A hold may extend to or past T_h; the shifted plan then lies in the unassessed
tail, exactly as a plan starting at or after T_h does, and `unassessed_share` reaches 1.0. Every
violating interval is bounded, so a clearing δ always exists: `realize()` is total.

**No human projection** (`None`, or one without segments): δ = 0, cost = T_r, `unassessed_share=1.0`,
`reason="no_human_projection"`. The caller treats it as it treats an absent projection today.

**Raises** `ValueError` for a plan with no segments, or one starting before `decision_step`.

**Validated (T3, T3b; `analysis/t3_realize/validate.py`)** against T1b's `whole` realizer
(`analysis/t1b_realization/realize.py`, a 0.01-tick grid over the same shift, fractional δ) at 50 cm
on eight conditions (scenario_00/10/20/30, prior off and on): 94 of 94 admitted candidate rows agree
on realizability; 82 are identical and 12 differ only by the whole-tick rounding (each the ceil of
the fractional δ); every realized trajectory is clear by T1b's closed form and by dense sampling,
hold included. **Re-validated under F1 (`analysis/f1_robot_responsible/validate.py`)** on the same
eight conditions: 101 admitted candidate rows, every realized trajectory sampled at 0.001 tick has no
rule (a) or (b) violation in its assessed window, every held row's δ − 1 violates (minimal), and F1's
δ never exceeds the T10 realizer's on the same inputs (its violating set is a subset).

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

#### Decompose
```python
decompose(
    task_name: str,
    task_params: Dict[str, str],
    agent_id: str,
    world: WorldState,
) -> List[GroundedAction]
```
The bare decomposition `plan()` wraps — the same guard-selected method, derived vars and step
grounding — without the `AbstractPlan` envelope. Added in I2 for the recognizer, which asks it
every tick, per hypothesis, what the observed agent would do if it held that intention. Raises
`DecompositionError` (a `ValueError` subclass) only for world-dependent failures — no method's
guards hold, a derived var without a value — so callers can treat "unscorable here" apart from
a schema error, which still raises plainly.

#### Is Complete
```python
is_complete(
    task_name: str,
    task_params: Dict[str, str],
    agent_id: str,
    world: WorldState,
) -> bool
```
The generic completion test (T7). A `TaskSchema` declares no goal of its own, so a task is
complete when the completion condition of the TERMINAL action of its decomposition for
`agent_id` holds in `world` — derived through `decompose()`, never from a predicate name.
Indifferent to who did it: `obj_at(item, table)` holds whoever delivered the item, and that is
the fact wanted — the task cannot be done again. A terminal `ProcessCompletion` (no predicate)
never reads as complete. Raises `DecompositionError` as `decompose()` does. Consumers:
`MetaPlanner.update()`'s pool assembly (§2.2, "Task pool"), and — the same criterion, in a
private copy that should delegate here — the recognizer's terminal pin (`_terminal_complete`).

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
- On a continue decision (§1.9: `UpdateResult.current_task` has the executing task's
  `task_instance_key()`) hands the re-decomposed plan to `Executor.continue_plan()`: the cursor
  moves to the action in flight if the fresh plan contains it (GroundedAction equality) and the
  microaction queue is kept; otherwise the plan loads from its start. The tick is spent exactly
  as it would have been with no trigger — never lost, never a restart (T5, TODO-43)
- Executes the hold δ `UpdateResult` carries (T4, TODO-71) as one STAND microaction per tick at
  the robot's position, starting on the decision tick, before the plan continues
  (`Executor.hold()`, called on every non-terminal decision after the plan is adopted). A later
  decision REPLACES the hold in progress with its own δ (0 when it carries none); the ticks not yet
  run are logged as interrupted. Mesa does not refine a hold; it never decides independently
  whether to wait and drops none silently (§1.9, the hold). Logs `[hold] ... start planned= trigger=
  pos=` and `[hold] ... end planned= executed= interrupted=`
- Logs one `[run]` header line per robot at construction naming the policy values the run was
  produced under: `gate_strategy`, `cost_strategy`, `separation_stop`, θ, ρ, `min_separation` and its
  ratio × rate (TODO-78); a run option (`--gate_strategy`, `--cost_strategy`, `--separation_stop`,
  `configs/experiment.yaml`) is a run fact, never a scenario fact
- Checks every agent's scheduled and assigned task bindings against the layout at spawn
  (`shared.types.check_task_bindings`, F47b): the bound object exists and carries the type the schema's
  `parameter_types` declares; a mismatch raises. A task the domain does not describe is never executed by
  the human and never invisible to the robot by accident (TODO-49; a declared out-of-domain behaviour is
  TODO-80)
- Supplies the `Projector` its motion rate (`step_size`, T2), its stopping distance (T9: the
  same `PROXIMITY_THRESHOLD` that makes `at(agent, object)` hold, so projected walks end where the
  executor stops), its per-action acknowledgement latency and observation offset (L2), and its
  per-task completion tick (F1: `TASK_COMPLETION_LATENCY`, the tick `Executor.step()` spends in
  `_on_task_complete()`, paid by both agents), for robot and human projections alike, and its
  duration-to-steps conversion (R2: `_parse_duration_to_steps`, the one its executor's wait uses)
- Logs the actual robot–human distance once per tick (`[sep]` lines, headless run; T9) so that
  actual separation below `min_separation` can be reported — Mesa has no execution-time
  avoidance (TODO-73); the measure is a measure, not a behaviour. `dist=` samples the end-of-tick
  positions; `min=` (T10, TODO-79) is the continuous minimum over the tick with both agents moving
  in a straight line between their consecutive positions, the motion model realization assumes.
  BUILT (C, `separation_stop` run option, default off): before a STEP microaction the robot checks the
  step against every human's actual position this tick under robot-responsible separation (F1) and
  STANDS instead when the step would bring the distance below `min_separation` without it increasing;
  queue and cursor untouched, retried next tick; only STEP is checked; additive to the decided hold;
  no trigger; the human gets no rule. One `[stop]` line per refusal (tick, positions, distance, step
  minimum, delayed action, inside / outside the assessed window of the decision in effect). Off, the
  log is the same as without the option apart from the `[run]` header naming it

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
11. The hold δ returned by `update()` (`UpdateResult.hold`, T4/T10) is executed, at the robot's
    position on the decision tick, before the plan continues; every decision replaces the hold in
    progress. The embodiment may refine it; it must not run a parallel heuristic that decides
    whether to wait or which task to run, and must not drop the hold silently (§1.9, the hold; the
    single-decision-path NOTE in TODOS_AND_DEFERRED.md)
12. The stopping distance the embodiment supplies to the `Projector` is the distance at which
    its own `at(agent, object)` predicate holds — one constant, one source (T9), as the motion
    rate it supplies is the one its executor moves at (T2), and the acknowledgement and
    task-completion ticks it supplies are the ticks its executor actually spends (L2, F1)

---
13. Every scheduled and assigned task's bindings name objects that exist in the layout with the types
    the schema's `parameter_types` declares; the embodiment refuses the scenario at spawn otherwise
    (`check_task_bindings`, F47b). Fixtures may not rely on an ill-typed instance
