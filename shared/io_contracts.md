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

**Re-aligned after T3 (September 2026)** for §1.11 and §2.2c: `realize()` and `RealizedPlan` exist
(`shared/realization.py`, `shared/types.py`) as a standalone service, validated against T1b's `whole`
realizer on the test set. Nothing consumes them yet: `MetaPlanner` still runs the old B3 path, and the
sweep is byte-identical to the L2 baselines. The remaining PLANNED paragraphs are T4's (`b2a`) and
T10's (B3 on realized cost, `UpdateResult.hold`, the executor's hint).

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
`Projector.build_segments()` (formerly `MetaPlanner._build_segments()`) reads
`world.agent_positions[agent_id]` and `world.object_positions[target_id]` on every projection,
and `scenario_00` runs end-to-end without error. No longer a discrepancy.

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
    fired: bool                            # a cognitive-clock event occurred (was `replan`,
                                           # renamed: the consequence is the caller's business)
    reason: str
    score: Optional[float] = None

@dataclass
class UpdateResult:
    current_task: Optional[TaskInstance]   # None = all tasks complete (see §2.2, Update)
    queue: List[TaskInstance]
    # PLANNED (wait-decision revision, R1): the winner's hold δ, in ticks, at the robot's
    # position at the trigger tick — see below. None / 0 when no hold was placed (no human
    # projection, or the all_unrealizable fallback).
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

**The hold — PLANNED, not yet in the dataclass** (Phase 4C wait-decision revision, September
2026; amended at R1; design_decisions.md, "The robot can wait"). `update()` will return, with the
winning task, the HOLD its realization placed: ONE δ (ticks), taken at the robot's position at the
trigger tick — which may be partway along a walk — after which the plan runs unchanged (the
whole-trajectory minimal shift, TODO-70). There is no per-segment hold. Semantics across the
boundary:

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

**`ConflictPoint`** / **`InterferenceAssessment`** — interference-detection output.
`_detect_interference()` observes; `_cost()` values. The separation is deliberate
(DESIGN-08): conflicts are computed and carried but not currently priced.
SUPERSEDED IN DESIGN (wait-decision revision): both types describe the batch profile
realization replaces. Under realization a conflict is priced by construction — as the duration
of the hold that avoids it — and the observe / value split survives inside realization
(`shift_violation_interval` observes; holding values). The types stay until T10 lands realization
in B3; `RealizedPlan` (§1.11, built at T3) replaces `InterferenceAssessment` on the meta-planner side
there. `realize()` takes the projected segments of whatever ordering it is given — it does not assume
a single task.

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

### 1.11 `RealizedPlan` (T3)

**Produced by `realize()` (§2.2c); consumed by `MetaPlanner` (T4's B2, T10's B3).** What a
candidate's trajectory actually is, given the human: the hold-only realization under the
whole-trajectory minimal shift (design_decisions.md, "The robot can wait", the R1 decisions).

```python
@dataclass
class RealizedPlan:
    realizable: bool                      # a clearing shift exists (see §2.2c); always True without a human projection
    delta: Optional[float]                # the hold, steps ≥ 0; None when unrealizable
    cost: Optional[float]                 # T_r + delta over the FULL plan; None when unrealizable
    projected_duration: float             # T_r: the span of the plan's segments (fractional steps)
    segments: List[Segment]               # the hold (stationary, when of positive duration) then every
                                          # projected segment shifted by delta; [] when unrealizable
    hold_position: Tuple[float, float]    # the plan's first segment's start: where the robot is at the decision step
    hold_start: float                     # the decision step
    horizon: Optional[float]              # T_h, the end of the human projection; None without one
    unassessed_share: Optional[float]     # share of [hold_start, realized end] beyond T_h; 1.0 without a
                                          # human projection; None when unrealizable
    reason: str                           # "realized" | "no_human_projection" |
                                          # "hold_position_violated" | "hold_reaches_horizon"
```

- `cost` is the ONE number a candidate competes on (T10): T_r + δ, walking plus the hold. The tail
  beyond T_h is inside T_r and not corrected for (TODO-69, reading (1)); the share is logged so the
  bias can be reported, not priced.
- `delta` is what reaches the executor as the hold hint (§1.9, TODO-71): stand at `hold_position`
  for `delta` steps, then the plan.
- An unrealizable plan has no realized cost to rank on; `reason` says why. The caller's fallback
  when no candidate realizes is R1's: plain projected cost, logged `all_unrealizable` (§2.2).
- `reason == "no_human_projection"` is the shape of "no projection admitted": δ = 0, cost = T_r,
  share 1.0. A caller may treat it exactly as it treats `human_projection is None` today.
- T_r is the segments' span, fractional, not `ProjectedPlan.total_estimated_cost` (its integer
  rounding). Whether B3 compares fractional realized costs against integer plain costs in the
  all-unrealizable fallback is T10's to settle.

---

## 2. Module Contracts

### 2.1 `IntentionRecognizer` (`shared/recognizer.py`)

#### Constructor

```python
IntentionRecognizer(
    knowledge: DomainKnowledgeBase,
    context: ContextKnowledge,                        # background facts for ω_context weighting
    hypotheses: List[HypothesisKey],                  # precomputed hypothesis space for this scenario
    assigned_tasks: Optional[List[TaskInstance]] = None,   # OBSERVED agent's work order; None/empty = prior off
)
```

**Correction from previous version:** this is a 4-argument constructor, not
`IntentionRecognizer(knowledge)`. `hypotheses` is built once at agent construction time via
the free function below, from the domain schemas and the objects present in the workspace —
*not* from the human agent's `scheduled_tasks`, which the robot never sees.

`assigned_tasks` carries the observed agent's work order — which tasks it was assigned, never
in which order it will do them. Identity crosses the boundary as `task_instance_key()` (§1.10),
which matches `repr(HypothesisKey)` (§1.8); an assigned task matching no hypothesis is logged
as a warning and ignored. `None` or `[]` switches the persistent assignment prior off entirely
and `update()` runs its original unweighted path. See `design_decisions.md`, "Assignment
knowledge: `assigned_tasks` is the work order, `scheduled_tasks` is the script."

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
`mesa_sim/sim_agents.py`.

**Correction (leg session, September 2026):** the recognizer now OWNS its belief. It keeps
an evidence state (no context weights, no state refutations) and derives each tick's
`BeliefState` from it; `prev_belief` is accepted for signature compatibility and not
consulted — its distribution contains output-only factors that must not be fed back.
Evidence accounting: a discrete observation (microaction in some action schema's declared
vocabulary) is an event and multiplies onto the evidence state; a moving observation is one
chord from the start of the current movement leg, replacing that leg's earlier chords; a
stationary observation closes the leg. Output = evidence × ω_context, with hypotheses
refuted by the held item and inadmissible hypotheses pinned at `BELIEF_FLOOR`. See
`design_decisions.md`, "One leg is one observation".

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

Private methods (`_is_current_task_plausible`, `_replan_tasks`, `_is_complete`,
`_detect_interference`, `_cost`) are internal to the class and deliberately not part of this
contract; only the constructor and the public methods below are cross-boundary surface.
Projection (`project`, `build_segments`, `estimate_duration`) lives on `Projector`
(`shared/projection.py`), which is injected. Realization (`realize()`, §2.2c, built at T3 and
not yet called from here) lives on the projection / trajectory side as well, not on
`MetaPlanner`, which supplies `min_separation` and consumes the `RealizedPlan` (T4, T10).

#### Constructor

```python
MetaPlanner(
    knowledge: DomainKnowledgeBase,
    projector: Projector,
    recognizer: IntentionRecognizer,
    theta: float = DEFAULT_THETA,        # 0.75, module-level in shared/meta_planner.py
    min_safe_distance: float = 1.0,
    strategy: Literal["single_task", "full_reorder"] = "single_task",
    gate_strategy: Literal["none", "b2a", "b2b"] = "none",
    interference_algorithm: Callable[[Segment, Segment], List[ConflictPoint]] = discretized_time_sampling,
    human_agent_id: Optional[str] = None,
)
```

**Correction (September 2026):** `assumed_speed` and `default_action_cost` are `Projector`
constructor parameters, not `MetaPlanner`'s; `projector` is injected (one instance, held by
the agent); `gate_strategy` selects B2 — `"none"` (default) skips the gate entirely,
`"b2a"`/`"b2b"` raise `NotImplementedError` (TODO-36).

Owns the task queue internally (Q1) — not passed in on each call. `theta` is a cognitive-
clock policy parameter (DESIGN-07), kept as an explicit constructor default rather than
read from `costs.yaml` — `costs.yaml` holds domain-specific step costs, a different concern
from IR confidence-gating. Its single definition is `shared.meta_planner.DEFAULT_THETA`
(September 2026; a second, unread copy in `recognizer.py` was deleted — the gate is the
meta-planner's decision, not a likelihood parameter). No call site passes `theta`, so the
default governs every run. θ is applied in exactly one private method,
`_clears_gate(belief) -> bool`, which both `evaluate_triggers()` (as a crossing) and
`update_human_projection()` (as admission) ask; it is deliberately one method so that a
derived θ (TODO-64) or a margin gate (TODO-65) would change how the bar is computed without
changing where it is asked. See design_decisions.md, "θ has one home".

`recognizer` is the **same live instance** the owning agent holds, not a second one built
here — `get_hypothesis()` is a static lookup built once at recognizer construction and is
stateless with respect to belief, so holding this reference carries no staleness risk. It
also avoids constructor bloat (`context`, `hypotheses`) and a redundant unused `_history`.

`strategy` and `interference_algorithm` are swap points (DESIGN-16, DESIGN-10).
`human_agent_id=None` means no human projection is built and every candidate is treated as
feasible — mirroring `RobotAgent.observed_agent_id`'s existing optionality.

`min_safe_distance` here, and `assumed_speed` / `default_action_cost` on `Projector`, are
**uncalibrated placeholders**, not tuned values (TODO-28). RESTATED by the wait-decision
revision: the parameter becomes `min_separation`, the clearance realization must ACHIEVE by
holding, passed into `realize()` — no longer a threshold below which a candidate is excluded.
DECIDED (R1): `min_separation` = 2.5 × the robot's motion per tick (50 cm in Mesa), expressed
relative to motion so that it scales with the body; the constructor keeps the old name and value
until T10 lands it (the exact parameter form — a multiple of the `Projector`'s rate, or a
world-unit value the body derives — is T10's). Also PLANNED (T4): `gate_strategy="b2a"` takes a
policy parameter ρ (default 0.5): B2 continues the current task when its hold δ ≤ ρ × (T_h −
trigger), the human's remaining projected duration; otherwise, or if the current task is
unrealizable, B3 runs. `human_projection is None` still means continue.

`Projector` (T9) additionally takes the body's **stopping distance** (`arrival_radius`), supplied
exactly as `assumed_speed` is: Mesa passes the same constant that makes its `at(agent, object)`
predicate hold (`PROXIMITY_THRESHOLD`, 30 cm), so a projected walk ends where the executor stops
and the next action is projected from that point. Its default in `shared/` is a unit-less
placeholder (0.0), not a value `shared/` knows to be right.

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

**Blocks.** 0: pool assembly (above); terminal return if empty. B1.5: no current task → straight
to B3. B2: `_is_current_task_plausible()`, the mid-task plausibility gate — `gate_strategy`
`"none"` (default) never continues; `"b2a"` / `"b2b"` raise `NotImplementedError` (TODO-36).
B3: `_replan_tasks()`, selection. PLANNED (wait-decision revision, decided at R1): both B2 and
B3 consume realization — B2 (`b2a`, T4) realizes the current task alone and continues when its
hold δ ≤ ρ × (T_h − trigger), a COMMITMENT gate that can only prevent a switch B3 would make; B3
(T10) realizes every candidate and takes the argmin of realized cost T_r + δ. When
`human_projection` is `None` realization is not called and the cost is the plain projected
duration, exactly as today.

**Strategy (DESIGN-16).** "Candidate" means the unit the argmin ranges over — an individual
task under `single_task`, a permuted ordering under `full_reorder` (design_decisions.md,
DESIGN-16, terminology). `self._strategy` controls only how much of the queue one `update()`
call rewrites:

- `single_task` (default, implemented) — each candidate is projected alone from the live
  `WorldState`, infeasible ones dropped, argmin becomes the new `current_task`. The rest of
  the queue carries no ordering commitment; it is re-decided at the next trigger.
- `full_reorder` (not implemented) — would score permutations of the candidate set and
  replace the whole queue. Blocked on cross-task `WorldState` propagation (TODO-07).

The human's projection is built once per fired trigger by `update_human_projection()` (below)
and passed in as `human_projection`; it is reused for every candidate, never rebuilt here.
`human_projection=None` means no interference check runs that call and every candidate is
treated as feasible — `_replan_tasks()` substitutes `InterferenceAssessment(feasible=True,
conflicts=[])`. It is never treated as always-conflicting. `None` is a ROUTINE mid-run state,
not an edge case: the belief re-initialises at every human task boundary (I4c), so most
`no_current_task` triggers and every trigger between the human's tasks run without a projection.

**Terminal state:** `update()` returns `UpdateResult(current_task=None, queue=[])` when no
candidates remain — all assigned tasks are complete. Callers check
`result.current_task is None`. Task exhaustion is never signalled by exception; "all tasks
done" is a fact `shared/` discovers about its own state, so it is returned through the
contract rather than raised for the embodiment layer to catch and reinterpret.

`update()` does still raise `RuntimeError` when candidates exist but **every** one is
excluded as infeasible — a genuine anomaly, deliberately distinguishable from exhaustion.
SUPERSEDED IN DESIGN (wait-decision revision): under realization "every candidate infeasible"
means no candidate has a shift within the human's horizon that clears `min_separation` — a
situation, not an anomaly. DECIDED (R1, TODO-30): `update()` then selects by PLAIN PROJECTED
COST (the argmin with no hold, the same path as when there is no human projection), returns no
hold, and logs the trigger as `all_unrealizable`. Nothing is raised. The raise stays in the code
until T10 lands realization in B3.

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
discretized_time_sampling(segment_a, segment_b, interval=1.0, *, max_spatial_step) -> List[ConflictPoint]
closest_point_of_approach(segment_a, segment_b) -> List[ConflictPoint]   # NOT IMPLEMENTED
```
Both are symmetric in their arguments and return an empty list when the segments do not
overlap in step-time. `discretized_time_sampling()` is the current default; its sampling
spacing is `min(interval, max_spatial_step / max(speed_a, speed_b))` with each Segment's
speed read off the Segment itself, so resolution is fixed in world units whatever the
embodiment's step size — projection steps are execution ticks (T2, September 2026).
`max_spatial_step` is keyword-only with **no default**: it is a world-unit quantity and
therefore a body-side fact; the embodiment layer binds it from its own config
(`functools.partial`, see `mesa_sim/sim_agents.py` and `mesa_configs.yaml:
simulation.interference_spatial_resolution`) and passes the bound callable as
`MetaPlanner(interference_algorithm=...)`. Unbound, the first check raises `TypeError`;
`closest_point_of_approach()` (CPA) is documented with its analytic approach but unbuilt —
exact rather than sampled, no interval tradeoff, but with real edge cases (clamping the
analytic minimum to the overlap window, near-zero relative velocity).

**Realization's geometry (BUILT, T3)** — realization asks this family a different question from
"where do two fixed trajectories come close": for which SHIFTS of a robot segment is there a
violation against a human segment, and when does the human first come within the separation of
a fixed point. Both are closed form; neither samples.
```python
shift_violation_interval(robot_segment, human_segment, min_separation) -> Optional[Tuple[float, float]]
first_approach_step(pos, human_segment, min_separation, from_step) -> Optional[float]
```
`shift_violation_interval` returns the open interval of shifts d for which `robot_segment`,
delayed by d along the same path, is strictly within `min_separation` of `human_segment` at some
moment both exist, or `None`. It is ONE interval by convexity: with u the robot's time into its
segment, the relative position is affine in (u, d), so the violating set is an ellipse interior
(or a strip) and the moments both exist are a parallelogram; their intersection is convex and
projects onto d as one interval, whose endpoints are enumerated exactly (the ellipse's own
d-extrema, its crossings with the parallelogram's edges, the vertices inside the disc). A
VIOLATION IS A DISTANCE: agents are points, and any moment strictly closer than `min_separation`
is one, including one cut off by T_h; the interval's endpoints are where the distance touches
`min_separation`, and are clear. `first_approach_step` is the hold-position check: the first step
at which the human is strictly within the separation of where the robot stands. Tolerances in
both are floating-point slack (1e-9 relative), not a margin. `closest_point_of_approach()` stays an
unbuilt drop-in for `discretized_time_sampling()`; `obstacle_aware_path()` becomes the detour
strategy of realization (Phase 4D).

These functions **measure only and hold no policy**. The single policy decision — what
distance counts as unsafe — lives in `MetaPlanner._detect_interference()` as
`min_safe_distance`. RESTATED (wait-decision revision): the single policy value is
`min_separation`, the clearance realization must achieve; `MetaPlanner` supplies it and
realization is GIVEN it, so no policy enters the geometry.

---

### 2.2c `realize()` (`shared/realization.py`) — BUILT (T3), not yet consumed

The realization service (design_decisions.md, "The robot can wait"; the R1 decisions). Sits
between `trajectory_algorithms.py` and `projection.py` in the one-way layering: it reads
`ProjectedPlan`s and `Segment`s only, knows nothing of tasks, beliefs or selection, imports no
simulator, and holds no policy — `min_separation` is passed in. `MetaPlanner` will call it once per
candidate (B3, T10) and once for the current task (B2 `b2a`, T4).

```python
realize(
    plan: ProjectedPlan,                  # the robot's; every entry's segments, in order — not assumed one task
    human_plan: Optional[ProjectedPlan],  # the admitted human projection, or None
    min_separation: float,                # world units; the caller's policy value
    decision_step: float,                 # the robot's now on the projection clock (0.0 at a trigger)
) -> RealizedPlan                         # never None; unrealizable is reported with a reason (§1.11)
```

**Policy (R1, TODO-70): the whole-trajectory minimal shift.** One hold δ at the robot's position
at `decision_step` (the plan's first segment's start, which may be partway along a walk), then the
whole plan shifted by δ. δ is the smallest shift ≥ 0 such that the shifted trajectory — including
the stationary hold at that position over [decision_step, plan start + δ] — has no violation in the
assessed window. Exact: δ is the right end of the union of violating shift intervals
(`shift_violation_interval`, one per robot × human segment pair) that covers 0, or 0 itself. No
search, no grid: the feasible set in δ is not monotone (a shift can clear one crossing and walk into
the next), so bisection would be invalid and a grid would make δ sampled.

**The assessed window** is where both projections exist and the realized plan lies within
[decision_step, T_h], T_h the end of the human projection: nothing past T_h is assessed or charged,
and nothing before the human projection's span (it starts at the observation offset, L2) is
assessed either. Segments are taken as they are — L2's stationary latency segments included —
and no stride is assumed.

**The hold is a position.** The human's projection must not come strictly within
`min_separation` of the hold position while the robot stands there. Since the hold only grows with
δ, the first step at which it does (`first_approach_step`) bounds δ from above; a minimal clearing
δ beyond that bound means no shift clears — `realizable=False`, `reason="hold_position_violated"`.
This is how head-on, same-line and "the human walks past the standing robot" conflicts come out,
with no special case.

**The hold cap.** A hold (δ > 0) may not extend to T_h: if plan start + δ ≥ T_h the plan is
unrealizable, `reason="hold_reaches_horizon"` — it would clear by outlasting the assessment. δ = 0
is not a hold and is never capped; a plan that starts at or after T_h is simply unassessed.

**No human projection** (`None`, or one without segments): `realizable=True`, δ = 0, cost = T_r,
`unassessed_share=1.0`, `reason="no_human_projection"`. The caller treats it as it treats an absent
projection today.

**Raises** `ValueError` for a plan with no segments, or one starting before `decision_step`.

**Validated (T3, `analysis/t3_realize/validate.py`)** against T1b's `whole` realizer
(`analysis/t1b_realization/realize.py`, a 0.01-tick grid over the same shift) at 50 cm on the test
set (scenario_20, scenario_30, prior off and on): 38 of 38 admitted candidate rows agree on
realizability, δ and cost to the grid; every realized trajectory is clear by T1b's closed form and
by dense sampling. Not exercised there: `hold_reaches_horizon` (no test-set row holds that long).

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
- PLANNED (TODO-71, R1): executes the hold δ `UpdateResult` carries as STAND microactions at
  the robot's position at the trigger tick, then continues the plan — unless a later trigger
  re-decides; may refine the hold against what the world shows, never decides independently
  whether to wait or drops it silently (§1.9, the hold)
- Supplies the `Projector` its motion rate (`step_size`, T2) AND its stopping distance (T9): the
  same `PROXIMITY_THRESHOLD` that makes `at(agent, object)` hold, so projected walks end where the
  executor stops, for robot and human projections alike
- Logs the actual robot–human distance once per tick (`[sep]` lines, headless run; T9) so that
  actual separation below `min_separation` can be reported — Mesa has no execution-time
  avoidance (TODO-73); the measure is a measure, not a behaviour

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
11. PLANNED (wait-decision revision): the hold δ returned by `update()` is executed, at the
    trigger position. The embodiment may refine it; it must not run a parallel heuristic that
    decides whether to wait or which task to run, and must not drop the hold silently (§1.9,
    the hold; the single-decision-path NOTE in TODOS_AND_DEFERRED.md)
12. The stopping distance the embodiment supplies to the `Projector` is the distance at which
    its own `at(agent, object)` predicate holds — one constant, one source (T9), as the motion
    rate it supplies is the one its executor moves at (T2)

---
