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
- **Robot**: initial ordering produced by meta_planner at t=0 using base-cost heuristic with null belief.
Treated as a mutable prioritised queue — meta_planner may reorder at any cognitive 
clock event based on IR output.
The scenario file's robot `scheduled_tasks` order is therefore only a fallback/hint
for t=0; it carries no semantic commitment beyond that.

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

**Robot receives assigned_tasks as an unordered set**
The robot's tasks are declared as a set in `AgentConfig` — no implicit ordering.
The meta_planner generates the initial queue Q0 at t=0 using a base-cost heuristic
(nearest item first, or similar) with a null/uniform belief state.
This makes the scenario file honest: it declares *what* the robot must do, not *how*
to sequence it. The human agent retains an ordered list (scripted ground truth).

**AbstractPlan vs ProjectedPlan — two distinct types**
`AbstractPlan`: single task, executor-facing. Output of `planner.py` (HTN decomposer).
Contains a flat list of `GroundedAction`s. "Abstract" means symbolic (not microactions).
`ProjectedPlan`: multi-task lookahead, meta_planner-facing only. Never handed to executor.
Concatenates AbstractPlans across the full task queue with estimated timing and spatial
occupancy per action. Used for interference detection and cost comparison.
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
