# TeamRob Framework — Design Decisions

Key architectural agreements for the Intention-Aware Adaptive Planning Framework.
This is a living reference of *why* things are designed the way they are.

---

## Core Principle: Mind / Body Separation

The robot architecture from the HCM paper maps directly to two layers:

- **Cognitive layer (`shared/`)** — the robot's mind. Simulator-agnostic. Pure Python.
  Handles intention recognition, adaptive planning, meta-planning, and domain knowledge.

- **Embodiment layer (`mesa_sim/`, `ros_sim/`)** — the robot's body. Simulator-specific.
  Handles sensing, world-state building, observation building, and action execution.

These two layers communicate only through canonical symbolic types (`Observation`, `BeliefState`, `WorldState`, `AbstractPlan`). The cognitive layer never imports anything from a simulator.

---

## The Four Key Decisions

**1. Planner outputs AbstractPlan with optional execution hints**
The planner produces high-level symbolic actions, not microactions.
Optionally it may attach hints (estimated path, duration, spatial constraints).
Mesa may follow hints directly. ROS treats them as soft constraints for its own motion stack.
This keeps planning symbolic while giving simulators flexibility in execution.

**2. WorldState is symbolic**
Simulators build a canonical symbolic snapshot before calling core.
Geometry, positions, and sensor data stay inside the simulator.
The cognitive layer reasons only over predicates (zone, holding, task_progress, etc.).

**3. Simulators decide WHEN to call core — core decides WHAT to do**
Mesa calls the cognitive chain every step.
ROS calls it event-driven, tied to cognitive-layer events (task completion, belief
threshold, etc.) — never on a fixed timer, and never derived from its own
motion-clock tick rate (see Three-clock architecture below). A concrete case of
this anti-pattern was found when reviewing an alternative ROS implementation.
Core never runs its own loop. It is a stateless service called by the simulator.

**4. ROS must discretize sensor streams into micro-actions before calling IR**
Intention recognition requires discrete observable micro-actions as input.
Mesa has ground truth micro-actions directly available.
ROS must classify noisy sensor streams into discrete micro-action labels externally,
before passing them to the shared recognizer.

---

## Other Agreed Decisions

**Bayesian inference for intention recognition**
Uncertainty is fundamental in human behavior inference, not incidental.
Evidence must accumulate over time across multiple competing hypotheses.
Rule-based or classification alternatives were rejected for this reason.

**Python objects for domain knowledge**
Task schemas and action schemas are defined as typed Python objects (`TaskSchema`,
`ActionSchema`, `Var`/`Const` terms) in `domains/<domain>/`. YAML was rejected
for domain knowledge because it required string parsing in the cognitive layer,
which breaks the no-string-parsing principle. Scenarios and environment layout
remain in YAML/JSON as configuration (not knowledge).

**Skeleton-first development**
All modules are built with correct interfaces and dummy logic first.
This validates the architecture and data flow before investing in algorithms.
Real algorithms (Bayesian update, cost-based planning, guard evaluation)
replace dummy logic in Phase 4.

**Scenarios are simulator-agnostic**
`scenarios.yaml` defines agent roles, starting positions, and task assignments
for both Mesa and ROS. Mesa-specific settings (step count, step size) live
separately in `mesa_sim/mesa_configs.yaml`.

**One micro-action per Mesa step**
Each Mesa step advances exactly one micro-action per agent.
This enforces the observable micro-action assumption from the paper formalization.

**Two distinct predicate families in WorldState**
`in_zone(agent, zone)` — coarse zone membership, used by the IR recognizer for
context weighting (ω_context). `at(agent, object)` — proximity-based object
presence, used by the executor to check action completion. These are separate
concerns and must not be conflated. `GOTO_ZONE` was removed from the HTN
decomposition tree entirely; zone-level reasoning lives only in the recognizer.

**env_layout.json: single unified `env_objects` list, `SimObject.is_portable` distinguishes fixed vs. carryable**
Superseded decision (was: items in a separate top-level `"items"` section from
static `env_objects`). Items/pallets are now merged into the same flat
`"env_objects"` list as shelves, tables, gates, etc. — every entry carries a
`"type"` field (enumeration category, e.g. "item", "shelf", "gate") and an
optional `"subtype"` (domain-specific classification, e.g. "part_A", "frozen").
Robots and humans remain in separate top-level sections — they're Mesa agents
registered with the scheduler, not passive objects, a genuinely different
loading path.
`SimModel._init_objects()` loads the unified list in two passes: objects with
a direct `"position"` first, then objects with `"initial_container"` (items,
pallets), whose position/zone are derived from their container — two-pass
avoids depending on JSON array order.
`SimObject.is_portable: bool` is set once at load time (True only for the
`initial_container`-loaded branch) and never mutated afterward. This is
deliberately a separate, stable flag from `held_by`/`at_location`, which
change during carrying — `at_location` goes `None` while an item is held, so
using it as the "is this portable" signal caused a real bug: a carried item's
distance-to-agent is always 0, so it could win as its own release target
(`_nearest_env_object()` in executor.py). `is_portable` fixes this by staying
constant regardless of carry state.
`SimObject` fields kept fully explicit (no metadata dict) per deliberate
choice — trades some field sprawl across domains (e.g. `good_type`/`is_empty`
unused by kitting items) for full attribute visibility during development.
Rule: never add a new top-level JSON section for a new object type — add it
to `"env_objects"` with an appropriate `"type"` value.
Files: mesa_sim/sim_model.py, mesa_sim/executor.py, mesa_sim/world_state_builder.py
Reference: Phase 4C typed-parameter generalization session

**Three-clock architecture: motion, world state, cognitive**
Simulators run three decoupled clocks. Motion clock: fastest — Mesa scheduler step,
ROS PRIEST at 10Hz. World state clock: samples `WorldState` + `Observation` —
Mesa identical to motion clock, ROS configurable (default ≈ Mesa step rate).
Cognitive clock: event-driven, not time-based — fires on task completion, belief
threshold, or observation change. `shared/` operates only at the cognitive clock
level and is ignorant of motion and world state frequencies.

**`ProcessCompletion` as the sim-agnostic completion contract**
The cognitive layer signals action completion by process exhaustion — when the
microaction queue for a `GroundedAction` is empty, the action is done. Each
embodiment layer realizes this in its own temporal terms: Mesa uses step counts,
ROS uses action server feedback. The cognitive layer is ignorant of schedulers,
wall-clock time, or step size.

**WorldState carries object positions — a scoped exception to symbolic-only reasoning**
Decision #2 above states geometry stays inside the simulator. In practice,
WorldState.object_positions / agent_positions / object_zones are populated and
read by the recognizer. This is a deliberate, scoped exception, not drift:
move_to-type actions have a genuinely latent parameter (which target the
trajectory is heading toward) that cannot be resolved from microaction type
alone — the paper's "deterministic μ→a mapping" holds at the type level
(a run of STEP microactions is unambiguously a move_to) but not at the
parameter level (which target). Scoring trajectory-consistency against a
schema-declared target is legitimate cognitive-layer inference, not a
simulator leak — it is exactly the Bayesian disambiguation the paper's IR
formalization exists to do. The exception is scoped narrowly: positions are
only consumed by direction_consistency_likelihood (shared/likelihood_functions.py)
and target-resolution helpers (_get_expected_position, _get_target_zone) in
recognizer.py — never by planner.py or executor.py, which remain fully symbolic.

**IR likelihood dispatch: schema-driven, not microaction-string-driven**
ActionSchema declares two IR-relevant fields: `completion` (a ConditionSchema
checked for discrete actions like pick_up/place) and `progress_evaluator`
(a registered function name for continuous actions like move_to, e.g.
"directional" for cosine trajectory-consistency). recognizer.py dispatches
by testing whether the observed microaction is a member of a candidate
schema's own declared `microactions` vocabulary — never by comparing against
hardcoded literals like "grasp"/"step". Likelihood math lives in
shared/likelihood_functions.py as pure functions taking plain positions/
predicates, with zero knowledge of tasks, items, or simulators. Adding a new
ongoing-action type (e.g. a future duration-based wait_at evaluator) requires
writing one function, registering it in PROGRESS_EVALUATORS, and naming it
in the relevant ActionSchema — zero changes to recognizer orchestration logic.

---

## Phase 4 Architectural Decisions

**`scheduled_tasks` semantics differ by agent type**
The field name `scheduled_tasks` is kept on `AgentConfig` for both agent types, but semantics differ:

**`TaskSchema.parameter_types`: typed, multi-parameter enumeration for IR's hypothesis space**
Superseded decision (was: single `enumerable_param: Optional[str]`, one
enumerable parameter per task, defaulting to `"?item"`). Generalized after
recognizing that a second kitting table or coffee machine would require a
task to enumerate over *multiple* typed parameters simultaneously (e.g.
`deliver_item(?item, ?kitting_table)` — cartesian product over items ×
tables), not just one.
`TaskSchema.parameter_types: Dict[str, str]` maps each enumerable Var name to
an object type string (e.g. `{"?item": "item", "?kitting_table":
"kitting_table"}`). `shared/recognizer.py`'s `build_hypothesis_space()` takes
the cartesian product of `known_objects_by_type[type]` over every entry —
degenerates to exactly one combination when every type has a single known
instance, so single-instance domains behave identically to before.
`known_objects_by_type: Dict[str, List[str]]` is workspace/layout data, not
domain knowledge — it's threaded as a parameter into `build_hypothesis_space`
and `RobotAgent.__init__` (same pattern `known_item_ids` used previously),
built once in `SimModel._init_objects()` by grouping loaded `SimObject`s by
`.type`. It deliberately does NOT live on `DomainKnowledgeBase` — that class
is domain-general and built once per domain regardless of layout; object
instance counts are per-layout and would break that separation.
`?item` remains the actual naming convention in use across kitting AND
dock_loading (not renamed) — but `shared/` no longer hardcodes it as a
string; it reads whatever `parameter_types` declares per task.
`coffee_break`/`ac_activation` were converted from `Const`-bound singular
objects to typed `Var` parameters for consistency with `deliver_item`, even
though each currently has only one known instance — same rule as `?item`:
`Const` is fine while an object type is genuinely singular; convert to typed
`Var` + `parameter_types` once a second instance becomes plausible.
Files: shared/types.py (TaskSchema.parameter_types), shared/recognizer.py
(build_hypothesis_space), mesa_sim/sim_model.py (known_objects_by_type
construction), domains/kitting/tasks.py
Reference: Phase 4C typed-parameter generalization session

- **Human**: fixed ordered sequence of `TaskInstance`s (assigned + foreseeable interleaved).
Order encodes when deviations occur. Never reordered at runtime. Ground truth for IR evaluation.
- **Robot**: an unordered task *pool*, not a schedule. No base-cost heuristic produces an
initial ordering — Q0 comes from the same `update()` mechanism as every later
re-evaluation (see "Robot's `scheduled_tasks` order is a scenario-authoring convenience"
below). Under the `single_task` strategy (DESIGN-16), meta_planner selects one task at
each cognitive-clock event; the remaining pool carries no ordering commitment at any point.
The scenario file's robot `scheduled_tasks` order is never consumed as an execution order.

**Assignment knowledge: `assigned_tasks` is the work order, `scheduled_tasks` is the script**
The robot may know *which* tasks the observed human was assigned without knowing the
human's *plan* — order, timing, deviations. Three decisions make that separation concrete:

- **D1 — the unit of knowledge is `TaskInstance`**, not a task name and not a bare item id.
  Matching an assigned task to an IR hypothesis goes through `task_instance_key()`
  (`shared/types.py`), which produces the same string as `repr(HypothesisKey)` by design —
  e.g. `deliver_item(?item=item_3,?kitting_table=kitting_table_0)`. The two are kept in
  lockstep deliberately; io_contracts.md §1.10 and §1.8 are the contract.
- **D2 — the knowledge is a support restriction, not a prior.** The admissible set is the
  assigned tasks, plus every foreseeable task, plus `unknown`; inadmissible hypotheses are
  pinned at `BELIEF_FLOOR` and never accumulate evidence. See "Assigned-task pool is a support
  restriction, not a prior" below for the decision and the record of the 10× multiplier it
  replaced. The first build was a persistent, non-compounding weight w(τ) (`ASSIGNED_TASK_PRIOR`
  = 10.0 if assigned, 1.0 otherwise), divided out of the incoming belief and multiplied back
  in on output. That shape was chosen over two simpler ones — a one-time prior at t=0 is
  erased by `BELIEF_FLOOR` within the first task, and folding w into ω_context compounds to
  wⁿ, making the boost a function of the update rate — and those two rejections still stand.
  What did not survive is the weight itself; the entry below says why.
- **D3 — the knowledge lives on the scenario `AgentConfig`.** Human: `assigned_tasks` is the
  assignment (a fact), `scheduled_tasks` is the developer's execution script and drives
  `HumanAgent` only. Robot: `assigned_tasks` is its task pool, seeded into the meta_planner;
  robot `scheduled_tasks` is no longer read or declared. `AgentConfig.__post_init__`
  enforces that a human's `assigned_tasks` equal its non-foreseeable `scheduled_tasks`
  exactly — a foreseeable deviation is never part of a work order. Empty `assigned_tasks`
  skips validation, so un-migrated domains stay loadable.

Foreseeable tasks and `unknown` are never restricted away: a deviation is exactly what a
work order does not list, and must stay recognizable. The switch is global evaluation config
(`configs/experiment.yaml: assignment_prior`, default `false`, `--assignment_prior true` to
override; the name predates the restriction — TODO-44), not a scenario fact — which scenario
is being run and what the robot is permitted to know are independent axes. With the switch
off the recognizer runs its original code path unchanged, verified byte-identical on
`[meta]`, `[IR]` and `[IR-dist]` across scenario_00, scenario_10 and scenario_20 (with
`PYTHONHASHSEED=0`, see TODO-42).
With the switch on, t=0 belief is uniform over the admissible set, so the human's task is
resolved within a few observations rather than after a plateau. Fixtures that rely on a
mid-task reveal (scenario_20) must run with the switch off. Supports one observed human
(`RobotAgent` uses `observes[0]`); multiple observed agents would need `assigned_tasks` keyed
per agent.
Files: shared/types.py (AgentConfig), shared/recognizer.py, mesa_sim/sim_model.py,
mesa_sim/sim_agents.py, mesa_sim/run_mesa.py, configs/experiment.yaml,
domains/kitting/scenarios.py
Reference: assignment-prior session, September 2026

**Two planning levels, not one**
The HCM paper's "adaptive planning" block maps to two distinct modules in implementation:

- `meta_planner.py` — high-level: task scheduling, candidate ordering generation, cost
  comparison, reordering/reselection decisions. Owns the task queue.
- `planner.py` — HTN decomposition: given a single task, recursively decomposes it into
  a flat `AbstractPlan` of `GroundedAction`s. Called by meta_planner, not by the agent directly.
`replanning.py` (skeleton) is retired; its trigger logic is absorbed into `meta_planner.py`.

**HTN owns decomposition; meta_planner owns scheduling**
HTN (`planner.py`) answers: "how do I execute this task?" — recursive decomposition
until all steps are primitive `ActionSchema` leaves. It does not decide task ordering.
Meta_planner answers: "which tasks, in what order?" — uses IR predictions and cost
estimates to evaluate candidate orderings. These are strictly separate responsibilities.
Introducing a top-level `DELIVER_ALL` HTN task was considered and rejected: it would
force scheduling logic inside HTN, losing IR visibility and making replanning expensive.

**Current task competes as just another candidate — no special WAIT/RESELECT branch**
meta_planner's candidate set for every update() call is {current_task} ∪
remaining_tasks — current_task receives no special-case path distinct from other
candidates. Continuation vs. reselection falls out of cost comparison across the
full candidate set, not a separate "should I abandon this?" decision with its own
branch logic. Cross-checked against an alternative two-branch implementation
(separate WAIT/RESELECT cost paths) during the Fatemeh code review — the
uniform-candidate design closes off a class of bugs the branch-based version had
(an asymmetric cost term only one branch paid, an unused duration field); no gap
found that this design doesn't already handle.
Files: shared/meta_planner.py (Phase 4C)

**Robot's `scheduled_tasks` order is a scenario-authoring convenience, not a schedule**
Both agent types use the same `AgentConfig.scheduled_tasks` field — no separate
unordered-set type, no field split by agent_type. For the robot, list order carries
no semantic commitment: it's a fallback/hint for how the scenario file reads, never
consumed as an execution order (see below, "scenario file's robot scheduled_tasks
order"). Q0 — the real initial ordering — is produced by the identical mechanism
used for every later reorder: evaluate_triggers()'s "no current task" condition
fires unconditionally the first time update() is called (the agent has no
current_task yet), running the normal enumerate → project → detect interference →
cost pipeline over the full task pool. No separate base-cost heuristic exists —
an earlier design considered one and it was superseded once current_task-as-
candidate (below) made a bespoke t=0 heuristic redundant with the mechanism
already needed for every mid-run reorder. The human agent's list remains genuinely
ordered (scripted ground truth) — this asymmetry is agent_type-driven, not
field-driven.

**AbstractPlan vs ProjectedPlan — two distinct types**
`AbstractPlan`: single task, executor-facing. Output of `planner.py` (HTN decomposer).
Contains a flat list of `GroundedAction`s. "Abstract" means symbolic (not microactions).
`ProjectedPlan`: meta_planner-facing only. Never handed to executor. Wraps an
`AbstractPlan` with estimated timing and a list of `Segment`s (per-action geometry).
Used for interference detection and cost comparison.
Under the implemented `single_task` strategy (DESIGN-16) a `ProjectedPlan` always holds
exactly one entry. The multi-entry shape is retained for the deferred `full_reorder`
strategy — `_project()` raises `NotImplementedError` for orderings longer than 1.
Both types are defined in `shared/types.py`.

**Cost function: Mesa steps as the uniform cost unit**
All robot behaviors carry equal cost per step: moving, detouring, pausing/waiting.
Total cost of a candidate plan = total Mesa steps to complete all tasks in the horizon.
This captures team efficiency (faster completion = better) without semantic complexity.
Team-level semantic costs (human waiting, shared resource conflicts) are parked as a
future extension — the cost function interface must be designed to allow this extension
without requiring meta_planner redesign (see DESIGN-08).

**Cancellation is not a meta_planner cost term — it is an HTN method choice**
Originally specified as a `Ccancel(τcur)` term added explicitly in `_cost()`:

    detect_interference()
      ↓
    compute cancellation cost
      ↓
    for each candidate:
        cost(candidate) = execution_cost + cancellation_cost

This made cancellation a meta_planner-level concern, requiring `carrying` state to be
threaded through `_cost()`/`_project()`, and requiring meta_planner to know *why* a
candidate costs what it does.

Implemented instead as a second, guarded `MethodSchema` on the task itself
(`deliver_with_return` in `domains/kitting/tasks.py`, tried before the unconditional
`deliver_default`), selected via existential guard matching in `_guards_satisfied`
(`shared/planner.py`):

    detect_interference()
      ↓
    if replan:
        for each candidate:
            decompose(candidate)   # planner.py picks the applicable method
              → task's own guarded method decides: continue directly, or return
                the held item first (holding(?agent, ?other) ∧ ?other != ?item)
              → resulting plan (4 or 6 steps) determines cost

`meta_planner._cost()` needs no `carrying` parameter and no cancellation branch — it
simply decomposes each candidate via `planner.py` and counts the resulting actions.
It does not know, and does not need to know, why one candidate came back longer than
another. This also collapses the paper's CONTINUATION vs. RESELECT split into the same
mechanism: if the candidate is the task the held item belongs to, `not_equal` fails,
the plain method runs, no extra cost; if it's a different task, the guard fires and the
return steps are already counted in that candidate's own plan length. See DESIGN-09 for
the separate, still-open question of whether to run this evaluation for every candidate
on every trigger, or apply a cheap pre-check first.
Validated (not just designed): `robot.carrying` seeded before a `scenario_00` run
produced a 6-action `AbstractPlan` (vs. the normal 4) with the correct return-to-shelf-first
ordering, with no regression to the ordinary path in a separate unmodified run.

**IR runs from t=0 with uniform prior; meta_planner gates action on confidence θ**
The recognizer updates belief every cognitive clock tick from the start of simulation.
It does not wait for "enough" observations. The meta_planner uses a confidence threshold
θ to gate reordering decisions: below θ, the current queue is maintained; above θ,
candidate evaluation is triggered. This gives continuous reasoning without premature
reordering on weak evidence.
Confidence functions as a gate only — it determines *whether* candidate evaluation
runs, never feeds into `_cost()` as a magnitude (e.g. scaling an interference term
by belief probability). This distinction was implicit rather than stated; made
explicit after reviewing an alternative implementation that fed decayed belief
directly into cost as a multiplier. Whether *horizon-projected* confidence (for
tasks further down a multi-task candidate ordering) should ever feed cost is a
separate, deliberately open question — see TODOS_AND_DEFERRED.md DESIGN-12.

**Prediction horizon H bounds the lookahead**
IR produces a predicted human action sequence with confidence decaying over horizon H.
Meta_planner reasons only over the overlap between H and the robot's ProjectedPlan.
Beyond H, prediction uncertainty makes cost estimates unreliable.
In small scenarios (few tasks), H may span the full queue. In longer shifts, H caps
the effective lookahead naturally. H is a function of IR confidence, not a fixed value.

**Prediction horizon H is derived from IR belief, not a fixed parameter**
Once IR confidence exceeds θ and most_likely intention is committed, the full HTN
decomposition of that task is known. The predicted human action sequence — and therefore
the horizon H — is derived directly from the task schema plus estimated step counts:
del(item) → moveto(item): i steps, pick(item): j steps, moveto(KT): k steps, place(item): l steps
Step counts i and k are estimated from layout geometry (distance / step_size).
Step counts j and l are fixed action costs from the domain schema (e.g. GRASP = 1 step).
H is therefore belief-coupled (only meaningful above θ) and task-bounded (ends at predicted
task completion, beyond which uncertainty resumes). Below θ, the distribution spans multiple
competing hypotheses with conflicting predicted sequences — no reliable horizon exists and
meta_planner holds the current queue.

**Plans are re-decomposed from scratch; the world state is the execution cursor**
There is no plan cursor, action index, or resumption mechanism. Every cognitive trigger
re-decomposes the chosen task via `planner.plan()` against the current WorldState, and
`_project()` does the same for every candidate during cost comparison. Nothing carries
forward from a partially-executed plan — `plan()` accepts a `current_plan` parameter but
does not read it.

This was chosen over tracking execution position: no action cursor, no partial-action
state, and no possibility of the plan's recorded progress diverging from what the world
actually shows. The world is the record of progress.

The consequence is a requirement on domain authoring: each task's `MethodSchema` set must
cover every world state the task can legitimately start *or resume* from. Guards encode
"what remains to be done from here," not merely "how to begin." This is not edge-case
handling — the trigger design guarantees mid-task re-decomposition (`task_committed` fires
immediately after every successful `pick_up`), so the partially-executed states are reached
on every task, every run.

`deliver_item`'s three methods are complete under this rule, ordered most-specific-first
since `_select_method` returns the first method whose guards pass:
  1. `deliver_already_held` — guard `holding(?agent, ?item)`; the target is in hand, only
     `move_to(kitting_table) → place` remains.
  2. `deliver_with_return` — guard `holding(?agent, ?other)` + `not_equal(?other, ?item)`;
     an unrelated item is held and must be returned first.
  3. `deliver_default` — unguarded fallback; nothing held.

Omitting (1) is a selection bug, not only wasted motion: the current task's projected cost
would include a redundant `move_to` + `pick_up`, inflating it relative to alternatives and
potentially causing the robot to abandon a task it is halfway through.
**Single-task selection (receding horizon), not queue-wide reordering** [DESIGN-16]
meta_planner selects the single best *next* task at each trigger, then re-decides at the
next trigger from fresh WorldState and belief. It does not search permutations of the
remaining task pool for a globally optimal ordering.

The two are not equivalent, and this is an accepted trade-off rather than an approximation
of a settled objective. Full reordering can exploit downstream task interactions (task A is
cheapest now, but doing B first makes C much cheaper); single-task selection cannot see that
and will miss such cases. The argument for accepting that loss:

- The whole architecture exists to keep improving information about a human teammate.
  Optimizing the robot's *entire* future queue against a prediction we know will be better
  informed at the next trigger inverts that premise. Triggers fire often (task completion,
  θ-crossing, task-commit), so decisions are re-made from fresh evidence continuously.
- Prediction horizon H is already belief-bounded and task-bounded (see above). Committing to
  a multi-task robot schedule optimized against an uncertain horizon has weaker justification
  than re-deciding within it. A mathematically optimal permutation under an inaccurate
  forecast is not a better policy.
- Queue-wide projection created an asymmetry: human prediction bounded by H, robot
  optimization potentially spanning the entire remaining queue. DESIGN-12 (horizon-projected
  confidence) exists only to patch that asymmetry, and becomes moot under single-task.
- Multi-task projection requires propagating a *hypothetical* WorldState across tasks that
  have not executed (task 2's guards must see the world as if task 1 completed). That needs
  effects/retraction semantics `ConditionSchema` does not have today (TODO-07) — a change to
  the core predicate model. Single-task projection always starts from the real, live
  WorldState, so the question does not arise.

The last point is *supporting evidence, not the justification*. The architecture was chosen
because the decision semantics favour receding-horizon selection; the fact that it also
eliminates a large speculative-state machinery problem is a consequence, not the reason.

This is a domain-dependent choice, not a universal one. Domains with strong task-to-task
coupling — travel/setup costs between tasks, deadlines, dependencies, shared resources,
batching — would justify deeper lookahead. `full_reorder` is retained as a documented,
switchable alternative for that case (see below). Note that if it is ever built for a
larger task set, brute permutation is the wrong shape (O(n!)); it would need bounded-depth
lookahead, a routing/assignment formulation, or beam search.

Terminology, fixed: **"candidate" means the unit being selected** — whatever the argmin
ranges over. Under `single_task` that is an individual task; under `full_reorder` it is a
permuted ordering. This keeps `_cost(candidate)`, "feasible candidates," and "argmin over
candidates" reading correctly regardless of strategy. (This reverses an earlier rule fixing
"candidate" to mean an individual task always — that rule made every downstream phrase
strategy-dependent once orderings entered the picture.) Tasks inside a fixed ordering are
not candidates: they compete for nothing. What differs between strategies is only how much
of the queue a given `update()` call rewrites — the head (single_task) or the whole thing
(full_reorder). "Greedy" is deliberately avoided as a description: it presupposes
full-sequence optimization is the true objective being approximated, which is exactly what
is not established here.
Files: shared/meta_planner.py (`_strategy` flag, `update()`), shared/projection.py (`project()`)
Reference: Phase 4C meta_planner build session, September 2026

**Interference is geometric, not zone-based**
Zone co-occupancy was rejected as the proximity criterion for interference detection.
Zones are arbitrary in size and shape; two agents in one large zone may be far apart, and
two agents in adjacent zones may be adjacent in space. This extends the existing rejection
of zone-based *pre-filtering* (NOTE on DESIGN-09/DESIGN-11) to the detection mechanism
itself, for the same underlying reason.

Interference detection instead computes actual Euclidean distance between the robot's and
the human's projected positions over time. Since interference is conceptually a
coarse-grained analogue of collision checking, it uses what collision checking uses.
`ProjectedPlanEntry.spatial_zones: List[str]` was accordingly removed and replaced by
`segments: List[Segment]`; `ConflictPoint` lost its `zone: str` field and gained
`position: Tuple[float, float]` and `distance: float`.
Files: shared/types.py (Segment, ConflictPoint, ProjectedPlanEntry),
shared/trajectory_algorithms.py, shared/meta_planner.py (`_detect_interference`)
Reference: Phase 4C meta_planner build session, September 2026

**Trajectory algorithms are pluggable free functions, not embedded logic**
`shared/trajectory_algorithms.py` holds pure functions operating on `Segment`/`ConflictPoint`,
in two families, each a deliberate swap point rather than a fixed implementation:

- *Path realization* — how one action's motion is computed. `straight_line_path()` and
  `stationary_segment()` are the current defaults, consumed by `_build_segments()`.
  `obstacle_aware_path()` is a documented, unimplemented placeholder (DESIGN-13 / TODO-09).
- *Interference detection* — given two `Segment`s, where and how close do they get.
  `discretized_time_sampling()` is the current default; `closest_point_of_approach()` (CPA)
  is documented with its analytic approach but not implemented.

`MetaPlanner` holds `interference_algorithm` as a constructor parameter, so swapping
algorithms — including to approaches from the planning literature not considered here — is a
one-argument change, never an edit to `_detect_interference()`. Discretized sampling was
implemented first rather than CPA deliberately: it is verifiable by inspection and exercises
the pluggable interface, whereas CPA has real edge cases (clamping the analytic minimum to
the overlap window, near-zero relative velocity) better added behind a proven seam.

The algorithms measure only; they hold no policy. The single policy decision — what distance
counts as unsafe — lives in `_detect_interference()` as `min_safe_distance`.
Files: shared/trajectory_algorithms.py, shared/meta_planner.py
Reference: Phase 4C meta_planner build session, September 2026

**Three cognitive-clock triggers; θ-crossing is an event, not a threshold test**
`evaluate_triggers()` implements exactly three conditions (resolving DESIGN-07):

- `no_current_task` — `ExecutorState.current_task is None`. Covers both t=0 and ordinary
  task completion in one condition. There is no separate t=0 path and no separate
  task-completed check; the embodiment layer clearing `current_task` on completion is what
  makes these the same event.
- `theta_crossed` — belief confidence crosses θ from below to at-or-above it. Explicitly a
  *crossing* (`prev < θ ≤ current`), not `confidence >= θ` evaluated per tick, which would
  refire continuously for as long as confidence stayed high.
- `task_committed` — `holding` transitions `None → not-None` (the robot just picked
  something up).

`MetaPlanner` owns `_prev_belief`/`_prev_executor_state` internally to detect the two
transition-based triggers, rather than accepting them as parameters as `should_replan()` did.
Unresolved and low-stakes: if `theta_crossed` and `task_committed` both hold on one tick,
`theta_crossed` wins arbitrarily. Only the reported `score` differs, and `score` is not
consumed anywhere yet.
Files: shared/meta_planner.py (`evaluate_triggers`)
Reference: Phase 4C meta_planner build session, September 2026

**Queue invariant: the executing task is not in the queue**
`MetaPlanner._queue` holds only tasks that are *not* currently executing. The in-progress
task lives solely in `ExecutorState.current_task`, supplied fresh each call by the
embodiment layer. Candidates are assembled as `[current_task] + queue`.

The alternative — queue always contains every incomplete task including the running one —
was rejected because it duplicates a fact across two independently-maintained pieces of
state that must then be kept in agreement, and because `TaskInstance.bindings` is an
unhashable dict, making identity comparison awkward. One fact, one owner.
Files: shared/meta_planner.py (`update`), shared/types.py (ExecutorState)
Reference: Phase 4C meta_planner build session, September 2026

**Task exhaustion is returned, not raised**
When no candidates remain, `update()` returns `UpdateResult(current_task=None, queue=[])`
rather than raising. "All tasks complete" is a fact the cognitive layer discovers about its
own state; signalling it by exception would force the embodiment layer to catch and
translate it into a decision `shared/` already made. That inverts the mind/body separation,
where `shared/` decides and simulators execute.

This is consistent with the rest of the interface: `evaluate_triggers()` already returns a
typed "nothing to do" decision rather than signalling absence otherwise, and
`ExecutorState.current_task` is already `Optional`.

The remaining `RuntimeError` in `update()` — every candidate excluded as infeasible by
interference — deliberately stays an exception. That is a genuine anomaly, not a normal end
state, and keeping the two distinguishable matters: using one mechanism for both would force
callers to inspect the message string to tell them apart.
Files: shared/meta_planner.py (`update`), mesa_sim/sim_agents.py (RobotAgent.finished)
Reference: Phase 4C meta_planner build session, September 2026

**Interference is a hard gate only; conflicts are not yet priced**
`_detect_interference()` observes (returns all `ConflictPoint`s plus a `feasible` verdict);
`_cost()` values. This separation is per DESIGN-08 and is already reflected in the types.
Currently `_cost()` returns execution cost alone: `feasible=False` removes a candidate
entirely before cost is computed, and a candidate that is feasible-but-close pays no penalty.
"Near but safe" is therefore not yet penalized — only "unsafe" is excluded.

`assessment.conflicts` is deliberately computed, carried, and left unused by `_cost()`, so
adding a soft penalty later requires no new computation and no interface change — only a
formula. That formula is DESIGN-08's open question and is not decided here.

Note also that no separate "trigger a reselect" step exists. An infeasible `current_task` is
simply excluded like any other candidate, and whatever wins the argmin over survivors becomes
the new current task — which *looks* like a reselect but is not a distinct decision path.
This is the current-task-as-candidate principle applied consistently to feasibility.
Files: shared/meta_planner.py (`_detect_interference`, `_cost`, `update`)
Reference: Phase 4C meta_planner build session, September 2026


**Projection is a service, separate from selection**
`shared/projection.py` (`Projector`) owns turning a task into a predicted trajectory:
`project()`, `project_human()`, `build_segments()`, `estimate_duration()`. These were
originally private methods on `MetaPlanner` (`_project`, `_build_segments`,
`_estimate_duration`, plus inline human-projection code in `update()`).

Extracted because projection is not selection logic — `MetaPlanner` merely consumes it.
Three planned consumers want projection without wanting selection: DESIGN-13's
path-realization estimator (Phase 4D), visualization drawing predicted paths, and Phase 5
evaluation measuring prediction quality. Under the old structure each would have had to
reach into `MetaPlanner`'s privates or duplicate the logic.

Layering, one-way:

    trajectory_algorithms.py   pure geometry
            ↓
    projection.py              task + world → trajectory
            ↓
    meta_planner.py            which trajectory to pick

The `Projector` is **injected**, not constructed by `MetaPlanner` — one instance, held by
the agent, shareable with viz/evaluation later. `assumed_speed` and `default_action_cost`
live on `Projector` only; duplicating them on `MetaPlanner` would give two sources of truth
that could silently disagree.

The human's projection is built once per fired trigger via
`MetaPlanner.update_human_projection()` (a thin wrapper supplying the recognizer and
`human_agent_id`) and passed to `update()` as an explicit parameter rather than stored on
the instance. Passing it makes the ordering requirement a type-level fact instead of a
runtime convention — `update()` cannot be called without one, so there is no stale-state
failure mode to guard against. Consistent with how `BeliefState` already flows: computed by
one call, passed explicitly to the next, never stashed.
Files: shared/projection.py, shared/meta_planner.py, mesa_sim/sim_agents.py
Reference: Phase 4C meta_planner build session, September 2026

**Assigned-task pool is a support restriction, not a prior**
What the robot knows when it knows the human's `assigned_tasks` is *"the human's task lies
in this set"* — a restriction on the support of the belief. The first build encoded it as a
magnitude: hypotheses in the pool weighed `ASSIGNED_TASK_PRIOR` = 10.0, all others 1.0. A
soft number standing in for a hard fact, and the number, not the evidence, decided when
θ was crossed. Measured in scenario_20: evidence alone plateaus near 0.36 for twenty steps
(0.167 → 0.252 → 0.304 → 0.364 at steps 0/1/2/8, 0.840 only at the human's grasp, step 22);
with the multiplier, confidence is 0.417 at t=0 and 0.774 at step 2 — over θ on prior mass,
before the human has done anything distinguishing. No value of θ and no value of the
constant fixes that: the crossing is a property of the constant.

The restriction removes the blend. The admissible set is the pool, plus every foreseeable
task (`TaskSchema.is_foreseeable` — schema-derived, so `shared/` names no task), plus
`unknown`. Admissible hypotheses take the ordinary update, normalized over admissible mass;
inadmissible ones are pinned at `BELIEF_FLOOR` and never accumulate evidence (skipped in the
update, restored pinned on output, so the distribution still spans the full space and sums
to 1.0). No weight, no divide-out/multiply-back: a mask needs no compensation, and with the
switch off nothing is masked, so the original path runs by construction. Confidence is then
a function of the admissible set size and of the evidence alone — with three admissible
hypotheses in scenario_20, t=0 is 0.332 and step 2 is 0.881, on two directional updates.
CORRECTION (leg session, September 2026): the 0.881 was two copies of ONE observation
multiplied together, not two updates — see "One leg is one observation" below. The honest
value of that walk is 0.641, and the restriction's t=0 figure (0.332) stands.

This is the same principle as the held-item constraint already in `_likelihood()` (TODO-37c):
a hypothesis the robot *knows* to be wrong is refuted, not down-weighted. It also removes
the hypotheses that were doing the flattening — in scenario_20 they are the robot's own
items, whose shelf sits 9–20° off the human's heading. That is general, not fixture-specific:
a robot's own tasks are systematically wrong hypotheses for its human, and often nearby,
because both agents work the same shelves. Cost: the log cannot distinguish a pinned
hypothesis from an admissible one refuted by evidence — both read `BELIEF_FLOOR`.

Foreseeable tasks and `unknown` stay admissible deliberately. `coffee_break` and
`ac_activation` are not in `assigned_tasks` precisely because they are the deviations the
robot must be able to recognize; restricting them away would make scenario_10's coffee break
unrecognizable, and `unknown` is the escape hatch for behaviour outside the model. Verified:
with the switch on, `coffee_break` stays live during scenario_10's deviation (0.004 → 0.016)
while the four out-of-pool items sit pinned — CORRECTION (leg session): that movement was
ω_context and renormalization, not chord evidence; `coffee_break` has never received
directional evidence at all (TODO-46). Admissibility held; recognition did not. An empty pool (dock_loading,
TODO-39) admits everything and degrades to the original path, never to an empty set.
Files: shared/recognizer.py (`_build_admissible_keys`, `_pin_inadmissible`, `update`)
Reference: evidence-gated projection admission session, September 2026

**θ gates projection admission as well as triggering**
`MetaPlanner.update_human_projection()` now returns `None` without calling the projector
when `belief.confidence < θ`. Extends DESIGN-07: θ already decided *whether* candidate
evaluation runs (`theta_crossed`); it now also decides whether the human's most-likely
hypothesis is trustworthy enough to project against. Below θ, `most_likely` is a tie-break
over near-uniform mass — in scenario_20 at t=0 it is item_4, a robot task, chosen by
insertion order (TODO-42) — and an interference check against it is a check against noise.
`update()` already handled `human_projection=None` (every candidate feasible, no
interference check), so the gate needed no downstream change. Admission is a MetaPlanner
decision; `Projector` stays a pure projection service holding no policy.

The gate is only meaningful because of the restriction above: with the 10× multiplier,
`belief.confidence` crossed θ on prior mass, so gating on it would have admitted a
projection built on almost no observation. Once the pool is a restriction,
`belief.confidence` *is* evidence confidence, and no `BeliefState` field was needed.

θ still never feeds `_cost()`. One θ serves both roles — triggering and admission — until
evidence separates them; if a run shows the two want different thresholds, that is the
point to split them, not before. Observed effect with the switch off: `none(below_theta)`
at t=0 in every scenario, and also at scenario_00's step-7 `task_committed` (0.388) and
step-95 `no_current_task` (0.642), where the human is between tasks; the t=0 `[meta-cand]`
lines lose their conflict counts (`conflicts=0 min_dist=None`), winners and costs unchanged.
Logged once per call as `[meta-proj] confidence=… theta=… projection=built |
none(below_theta) | none(no_human) | none(unresolved)`; no step or trigger field, since
step counts are a simulator concept and the trigger belongs to the caller — both are
recoverable from the `[meta-trig]` line of the same tick.
Files: shared/meta_planner.py (`update_human_projection`)
Reference: evidence-gated projection admission session, September 2026

**One leg is one observation — replace, do not multiply**
Measured in every leg of every run (scenarios 00/10/20, switch off and on,
PYTHONHASHSEED=0): the human's heading varies by **≤ 0.04°** within a movement leg, so
consecutive STEP observations are exact duplicates of one another. The recognizer multiplied
them: the per-step likelihood ratio of the correct hypothesis against `unknown` is 4.00
(HIGH/NEUTRAL) and against a hypothesis behind the human ~40, so n steps of one straight walk
gave 4ⁿ and belief saturated at 0.995 within three to six ticks — from one heading. Against
a collinear decoy the same walk gave 1.03ⁿ, which is why the 20°-off shelf never separated
(TODO-38). Diagnosis: not a kernel-sharpness problem but an INDEPENDENCE one — the kernel is
in fact too flat near the peak (a 10° miss costs 0.7 %, 30° costs 6.5 %) and its ratio
against NEUTRAL is what set the compounding rate.

RETRACTED as artefacts of duplicate counting: the "mid-approach reveals" measured in the
projection-admission session — scenario_20 switch-on at step 2 (0.881), scenario_00 at step
3, scenario_10 at step 2 — and the two confident wrong answers on scenario_10's coffee walk
(0.991 on item_6 switch-on, 0.971 on item_0 switch-off). None of them was evidence.

Decision. The recognizer keeps an EVIDENCE state and derives the output belief from it each
tick:
- A discrete observation (microaction in some action schema's declared vocabulary — built
  from every method of every task in the hypothesis space, not `methods[0]`) is an EVENT:
  it multiplies onto the evidence state and closes the current movement leg.
- A moving observation is ONE chord from the leg start to the current position, scored on
  top of the evidence the leg started from and REPLACING the leg's earlier chords. The chord
  is compared against the bearing to the target from the leg start — a τ-walker would have
  gone straight from there. Comparing against the current position was considered and
  rejected: a passed target's swinging bearing would re-import the accumulation one step at
  a time.
- A stationary observation changes nothing and closes the leg. A leg is a maximal run of
  moving observations, so a turn without a discrete event (the walk from the kitting table
  to the coffee machine and on to shelf_4 in scenario_10 has none) still starts a fresh
  chord. Without this rule the chord from the kitting table rotated through the whole
  coffee walk and drove a false crossing on the delivered item at step 194.
- ω_context and the held-item refutation are facts about the current STATE, not events.
  They are applied to the output only and never fed back; folding them into the evidence
  state counted them twice at every leg boundary (measured: ×2 ×2 at steps 78–79). The
  recognizer therefore owns its belief; `update()`'s `prev_belief` is accepted for contract
  compatibility and not consulted.
- The held-item constraint is a HARD refutation: hypotheses bound to a different item than
  the one held are pinned at `BELIEF_FLOOR` on output, the same treatment as
  inadmissibility. It was a ×0.1 factor per step; under per-step multiplication that was de
  facto elimination, under one-observation-per-leg it would have been a one-shot nudge —
  a soft multiplier standing in for a hard fact, the same pattern as the 10× prior and the
  duplicate chord. `unknown` and hypotheses with no item binding are never refuted by a
  grasp.

Two premises of the analysis that preceded this were wrong and are corrected here:
(1) "ω_context ≡ 1 in these layouts" — false. Zones are top-level quadrants in all three
layouts and ZONE_BOOST fires as state (item_2 ×2 at step 4, item_3 ×2 at step 11 in
scenario_20 switch-on). It was hidden by saturation. (2) "The grasp gives ×40" — false. It
gives ×10 via the held-item refutation of the OTHER items; the grasped item's own completion
predicate has never been evaluated (TODO-46). Every "grasp reveal" and "carry reveal" in
every run to date was held-item refutation of the alternatives.

Grasp confidence is 0.797, not the 0.888 obtained by pinning and renormalizing the step-21
belief: that arithmetic assumed ω constant across the grasp. It is not — the moment
`holding` appears, the held item's container is the agent, `_get_target_zone()` finds no
zone, and item_3's ×2 vanishes (TODO-37(b)); 0.248 : 0.062 = 4 : 1 → 0.80 minus floor mass.
The obvious fix — resolve a held item's zone from the holder's position — is wrong:
ZONE_BOOST means "the agent is in the zone of this hypothesis's TARGET", and in phase 2 the
target is the kitting table, not the item; an agent is always in the zone of what it
carries, so that fix would hand every carrying hypothesis a permanent free ×2. The correct
phase-2 branch mirrors `_get_expected_position()`: target zone = the kitting table's zone,
under which there is still no boost during the carry until the human reaches the table.
0.797 stands either way.

Crossings after the change (PYTHONHASHSEED=0; runs 20260910_1552xx). `theta_crossed` =
crossing events; "built" = admitted projections:

| run      | first ≥ θ            | theta_crossed | built projections  | note |
|----------|----------------------|---------------|--------------------|------|
| s20 off  | 22 (0.797), grasp    | 22, 89        | 22, 24, 89, 96     | late-reveal condition |
| s20 on   | **11 (0.780)**       | 11, 82        | 11, 23, 82, 95     | PRE-GRASP: human crosses x=0 into zone_SW at 11 (13.99 → −2.92) and ZONE_BOOST doubles item_3 (0.641 → 0.780); robot at (−393, 85), its move_to to shelf_4 completes at 21 — roughly half the approach; projection built, item_4 min_dist 14.98 at cost 812. This is the fixture condition B2 needs. It is a zone-state reveal on top of one honest chord (0.641), not an accumulation. |
| s00 off  | 41 (0.797), grasp    | 41, 111       | 41, 63, 111, 131   | |
| s00 on   | 41 (0.797), grasp    | 41, 81        | 41, 63, 81, 95, 131| leg-2 first chord 0.856 (carry-leg chord had already favoured shelf_2, 49° off, L 3.4) |
| s10 off  | 257 (0.769), grasp of item_4 | 257   | 257, 262           | grasp of item_2 at 31 gives 0.662: item_2 : coffee : unknown = 4 : 1 : 1 — coffee has no item binding and survives the pin |
| s10 on   | **107 (0.853) on item_6 — wrong** | 107, 257 | 107, 142, 200, 257, 262 | coffee-leg criterion FAILED, known consequence of TODO-46: `coffee_break` gets no chord evidence, so the walk to the coffee machine is credited to shelf_6 (27° off) and doubled on zone_SW entry |

Every belief change in all six runs is attributable to a leg start, a discrete event, a
quadrant crossing, or a world change (a robot-carried item's expected position moving with
the robot — switch-off only, since those hypotheses are inadmissible switch-on). No
per-step accumulation remains; within-leg values are flat to the third decimal.

KNOWN DEPENDENCY, recorded so it is not mistaken later: with one chord per leg, the kernel
alone decides whether any mid-approach reveal exists. Under the current linear kernel one
honest chord carries 0.64 against two alternatives (0.80 against `unknown` alone); a
normalised von Mises at σ ≤ 30° carries 0.82–0.88 (step-1 crossing in the two-hypothesis
pools), σ = 45° carries 0.69 (crossing at the grasp). After TODO-38 lands, **σ becomes
load-bearing for the whole meta-planner**: every downstream B2 result is conditional on it,
and a B2 finding that moves with σ is a σ artefact, not a robust result. The scenario_20
switch-on reveal at step 11 above is a zone-state reveal and does not depend on σ; the
step-2 reveals that would appear under σ ≤ 30° do.
Files: shared/recognizer.py (`update`, `_weigh`, `_output`, `_refuted_by_holding`,
`_progress_likelihood`, `_finalize`, `_pin`)
Reference: leg-level evidence session, September 2026
