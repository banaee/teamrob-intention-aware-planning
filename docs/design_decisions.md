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
consumed by direction_consistency_likelihood (shared/likelihood_functions.py),
by shared/target_resolution.py (the one lookup from a grounded action to a
position, since I2), and by its two callers — recognizer.py (chord target, zone)
and projection.py (segments, and through it meta_planner.py) — never by
planner.py or executor.py, which remain fully symbolic. (Updated in I2; the
earlier wording predated the projector, I1 audit 10.8.)

**IR likelihood dispatch: schema-driven, not microaction-string-driven**
ActionSchema declares two IR-relevant fields: `completion` (a ConditionSchema
checked for discrete actions like pick_up/place — declared and dispatched on,
but never reached in any run to date: the first action of every kitting method
is `move_to`, whose STEP* branch answers first, I1 audit 2.2; the per-hypothesis
phase of I3 is what makes it reachable) and `progress_evaluator`
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
REAFFIRMED (wait-decision revision, September 2026): the robot can now WAIT, and waiting is
still not a branch. A wait is a HOLD inside a candidate's realized cost, so "continue, paying
a 2-tick hold" and "switch, paying 19 ticks of walking" are compared by the same argmin. See
"The robot can wait", below.
REAFFIRMED AGAIN (R1, September 2026): B2 `b2a` (to be built, T4) is a COMMITMENT gate, not a
second decision path — it can only prevent a switch B3 would make (continue when the current
task's hold is small against the human's remaining projection), never select a task. The hold it
continues with is realization's, and B2 only carries it on the `UpdateResult` (wording corrected on
the T4 report). Inside B3 the current task still competes on its realized cost like any other.
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
UPDATE (wait-decision revision, September 2026): the uniform unit stands. A candidate's cost
is its REALIZED duration — walking plus the holds realization places to keep `min_separation`
from the human — so a conflict is priced as time by construction, with no conflict weight.
DESIGN-08 is resolved by that (see "The robot can wait", below); team-level semantic costs
remain parked as before (TODO-15).
DECIDED (R1, September 2026): realized cost = T_r + δ, where T_r is the candidate's projected
duration over its FULL plan and δ the single hold realization places (see "The robot can wait").
The part of the plan beyond the human's projected horizon T_h is inside T_r but is not assessed
for conflict; no correction is applied for that (TODO-69, reading (1)) — the unassessed share is
logged, not priced.

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
AMENDED (R1, September 2026): H is the end of the human's projected task, T_h. Realization
assesses the robot's plan only within [trigger, T_h] (Property 2, "The robot can wait"); the
robot's plan beyond T_h is UNASSESSED — recorded as such, treated neither as clear nor as blocked
— and what happens there is left to execution-time avoidance (see "Assumption: execution-time
avoidance past T_h", below).

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
Unchanged by the wait-decision revision (September 2026): realization's `earliest_violation`
is the same Euclidean test, asked per segment for a given start time instead of in batch over
two fixed trajectories.
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
SUPERSEDED IN PART (wait-decision revision, September 2026). Still true: two pluggable
families, and the algorithms measure only. What changed: the single policy value is
`min_separation`, the clearance realization must ACHIEVE, and it is passed INTO the
realization function rather than applied by `_detect_interference()` as an exclusion
threshold. The question asked of the interference family changes from "where do these two
fixed trajectories come close" to "earliest violation for this segment at this start time" —
the closed-form role `closest_point_of_approach()` was reserved for; `discretized_time_sampling()`
becomes a fallback that computes more than a hold needs. `obstacle_aware_path()` becomes the
detour strategy of realization (Phase 4D). See "The robot can wait", below.
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
SUPERSEDED IN PART (wait-decision revision, September 2026): the returned terminal state
stands. The `RuntimeError` does not: "every candidate excluded" now means "no candidate has a
realization within the human's horizon", which is a situation, not an anomaly. DECIDED (R1,
September 2026; resolves TODO-30 and TODO-52): when no candidate realizes, `update()` selects by
plain projected cost — the argmin over the pool with no hold, exactly the path taken when there is
no human projection — and logs the trigger as `all_unrealizable`. Nothing is raised. The
justification is the assumption recorded under "Assumption: execution-time avoidance past T_h"
(below): the robot proceeds and the residual conflict is the execution layer's. The raise is
removed when realization lands in the meta-planner (T10); until then the code still raises.
Files: shared/meta_planner.py (`update`), mesa_sim/sim_agents.py (RobotAgent.finished)
Reference: Phase 4C meta_planner build session, September 2026

**Interference is a hard gate only; conflicts are not yet priced** — SUPERSEDED (wait-decision
revision, September 2026) by "The robot can wait", below: conflict becomes cost BY CONSTRUCTION
as the duration of the holds realization places; `_detect_interference()` is replaced by a
per-candidate `realize()` with detection internal to it; `feasible=False` now means "no
realization within the horizon"; the observe/value split survives, relocated
(`earliest_violation` observes, holding values). Original entry retained as history; it still
describes the code until realization lands.
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
UPDATE (wait-decision revision, September 2026): the first of those consumers is now the
realization function (`realize()`, hold-only first — DESIGN-13's estimator partly pulled
forward into 4C), and it belongs on THIS side of the layering, not in `MetaPlanner`, which
supplies `min_separation` and consumes the result. The three-layer diagram above gains a
layer between geometry and projection — the four-layer diagram under "The robot can wait",
below, is the current one.

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

**θ has one home: the meta-planner owns the gate, and the gate is one method**
θ had TWO definitions and only one was read. `shared/recognizer.py` held
`CONFIDENCE_THRESHOLD = 0.75` that nothing imported, and `shared/meta_planner.py` held
`theta: float = 0.75` as a constructor default that governs every run. That is worse than a
plain duplicate: the recognizer's copy sat where a reader would look for it and editing it
did nothing. Grep at the time of the change: `MetaPlanner(` occurs at exactly ONE call site
in the repo, `mesa_sim/sim_agents.py`, and it does NOT pass `theta` — so the constructor
default is the real source, not a fossil of a call-site value. `ros_sim/` (paused) constructs
no MetaPlanner at all.

DECIDED (September 2026). The value lives in `shared/meta_planner.py` as a module-level
`DEFAULT_THETA = 0.75`, which the constructor takes as its `theta` default. The recognizer's
constant is DELETED, with a comment in its place saying where θ went and why it is not there.

Why the meta-planner and not the recognizer: the gate is a DECISION, not a likelihood
parameter. The recognizer produces the belief and never judges it — `recognizer_handback.md`
§2 already listed θ as "the meta-planner's gate, not a likelihood parameter", so the value
sitting in `recognizer.py` contradicted the recognizer's own hand-back. Why not a third,
neutral module: there is no home for it in the existing structure (`types.py` is dataclasses,
`domain_knowledge.py` is domain knowledge, `likelihood_functions.py` is the evidence model's
constants) and inventing one for a single value is a config system for a single value. A
module-level named constant keeps the number beside the one method that applies it while
staying importable — `from shared.meta_planner import DEFAULT_THETA` — for visualization or
evaluation code that wants to draw or report the bar without constructing a MetaPlanner.

The shape that matters is not where the number sits but that the gate is asked in ONE place.
`MetaPlanner._clears_gate(belief) -> bool` is now the only comparison against θ, and both
consumers ask it rather than comparing numbers themselves: `evaluate_triggers()` fires
`theta_crossed` when the predicate is False on the previous belief and True on this one (the
crossing stays an EVENT, DESIGN-07, unchanged), and `update_human_projection()` admits when
the predicate holds on the current belief. `self._theta` is now read in exactly two places:
inside `_clears_gate()`, and in the `[meta-proj]` log line that reports the bar.

This is deliberately the shape that survives both open directions, NEITHER of which is
implemented or favoured here: θ DERIVED rather than fixed (TODO-64) — a function of the live
hypothesis set, of layout geometry, or both, since a fixed 0.75 is a different evidential bar
over three live hypotheses than over eight when the reachable ceiling is 1/(1 + uⁿ); and a
MARGIN or likelihood-ratio gate replacing the absolute test (TODO-65) — fire when the leader
is far enough ahead of the runner-up, of `unknown`, or of the rest of the field, because 0.5
against a field of 0.1s is a stronger signal than 0.6 against a field of 0.2s and an absolute
number cannot see the difference. Both change how the bar is COMPUTED, not where it is asked,
so both land inside `_clears_gate()`. `belief.distribution` already carries the live set and
every rival's mass, so the current signature suffices for both; only a geometry-derived θ
would need a `world` argument, and both call sites already hold a `WorldState` to pass.

Not an argument for either direction: that a lower θ fires earlier. An earlier trigger is not
better by itself — M1 (`analysis/m1_theta_earlier/`) measured θ = 0.65 on scenario_30 and found
the first crossing moved 21 → 15 prior-on and 28 → 24 prior-off, with no decision change, no
extra trigger and byte-identical behaviour; and offline realization at the moved triggers came
out better in one prior and WORSE in the other, because what decides the outcome is whether the
trigger lands before, during or after the encounter, not how early it is.

Behaviour unchanged: same value, same comparison, all ten sweep conditions byte-identical.
Four analysis scripts still hardcode 0.75 to interpret their own logs
(`analysis/f1_foreseeable_fixture/measure.py`, `analysis/i3_phase_model/check_i3.py`,
`analysis/i4_evidence_model/check_i4.py`, `analysis/i4_evidence_model/pivot.py`) and are LEFT
hardcoded ON PURPOSE: they are records of runs made at θ = 0.75, and reading a live value would
silently reinterpret those logs if θ later changes or becomes derived. `analysis/i1_ir_audit/
measure.py` read the deleted recognizer constant and now carries the same literal for the same
reason. Recording θ in each run's log header would fix this properly (TODO-78) — it changes
logs, so it is not done here.
Files: shared/meta_planner.py (`DEFAULT_THETA`, `_clears_gate`, `evaluate_triggers`,
`update_human_projection`), shared/recognizer.py (constant deleted),
analysis/i1_ir_audit/measure.py
Reference: theta single-source session, September 2026; TODO-64, TODO-65, TODO-78; M1

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

Crossings after the change (PYTHONHASHSEED=0; runs 20260910_1552xx — superseded as regression
baselines by runs 20260911_0826xx after T2 rescaled projection time to execution ticks; the
`theta_crossed` steps below are unchanged in those runs, the built/selected columns are not —
see TODO-28 and TODO-30). `theta_crossed` = crossing events; "built" = admitted projections:

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

SUPERSEDED IN PART BY I3 (below). What stands: the kernel, HIGH/LOW/NEUTRAL, one normalization, the
retraction of the duplicate-counting reveals, and "replace, do not multiply" for movement. What no
longer holds: (1) there is no leg. The unit of a movement observation is now one HYPOTHESIS's stretch
toward one expected action, measured from that hypothesis's own origin, and nothing global closes
it — not a discrete event, not a stationary tick, not the body's synthetic `stand` (I1 audit 3.13,
drift 10.12: "a discrete observation … closes the current movement leg" was true of the code path
and false of its effect; both are gone). A turn without a phase change therefore does NOT start a
fresh chord any more: the chord is origin → current position and sweeps with the agent. (2) The
held-item refutation is deleted, not moved. (3) The floor is applied to the OUTPUT only; the evidence
state is normalized but not floored (it used to be re-floored at every leg base, a once-per-leg
recovery clamp that was never a stated decision).

**Projection steps are execution ticks; the body supplies the rate, and the sampling resolution has no default in `shared/` (T2)**
Until T2 the projector ran at `assumed_speed = 1.0`, so one projection step was one world unit
(cm) of motion and a stationary action was one unit: a candidate's "cost" was its path length
plus 1 per grasp/place, and a placement that takes a full Mesa tick was 20× shorter in the
projection than in execution. Costs were comparable between candidates and nothing else —
not to the human's projection in time, not to the executor's ticks, not to any `wait_at`
duration — and two agents projected to place at the same table a tick apart never coincided.

Decision. One projection step IS one execution tick. `RobotAgent` constructs
`Projector(assumed_speed=<Mesa step_size>, default_action_cost=1.0)` (mesa_sim/sim_agents.py,
`step_size` from mesa_configs.yaml), so a movement action lasts distance/20 ticks and a
stationary action one tick, for robot and human projections alike, and `[meta-cand] cost=`
reads in ticks (scenario_20 t=0: 54 / 71 / 103, formerly 1032 / 1372 / 2028). The body
supplies the rate; `shared/` learns no Mesa constant — the `1.0` defaults on `Projector` are
unit-less placeholders, not values `shared/` knows to be right. ROS supplies its own rate.

Follow-up, the same principle applied to the sampler: `discretized_time_sampling` spaces its
samples at `min(interval, max_spatial_step / max(speed_a, speed_b))`, speed read off each
Segment, so resolution is fixed in WORLD UNITS whatever the step size (a projection built at
20 units per tick is sampled 20 times per tick when `max_spatial_step` is 1). `max_spatial_step`
is keyword-only with NO DEFAULT: a resolution in world units is itself a unit-scale assumption
(1 cm in Mesa is not 1 m in ROS), and that is a fact about the body. The embodiment binds it
from its own config (`mesa_configs.yaml: simulation.interference_spatial_resolution`, a
required key) with `functools.partial` and passes the bound callable as
`MetaPlanner(interference_algorithm=...)`; an unbound call raises `TypeError` rather than
sampling at an assumed scale. The rule generalises: no world-unit constant in `shared/`.
Realization's `earliest_violation` is closed-form partly so that it needs no such constant
(see "The robot can wait").

Consequence measured, not decided: with placement lasting a real tick, both agents' placement
segments sit at the identical table point in overlapping ticks whenever the arrival gap is
under a tick, so `min_dist` reaches exactly 0.0 and `min_safe_distance = 1.0` excludes those
candidates — TODO-30 became exercised by the time-scale fix, not by calibration (scenario_20
selections change at s20_on 11 and s20_off 24; scenario_10 hits the every-candidate-excluded
`RuntimeError` at 257, TODO-52). `min_safe_distance` was deliberately left untouched. The T1
report's costs and pause delays are in pre-T2 projection units (its units note); its distances
are world units and unchanged. Mesa logs for the follow-up are byte-identical to 2282c83.
Files: mesa_sim/sim_agents.py (Projector construction, the bound sampler), shared/projection.py
(`Projector.__init__`), shared/trajectory_algorithms.py (`discretized_time_sampling`),
mesa_sim/action_decomposer.py (`_get_interference_spatial_resolution`), mesa_sim/mesa_configs.yaml
Reference: T2 session, September 2026 (commits 2282c83, 3af5953); TODO-28, TODO-30

**Targets, methods and completions are the planner's — the recognizer resolves nothing itself (I2)**
Until I2 the recognizer resolved a hypothesis's target with its own copy of the lookup: read
the literal `"?item"`, take `methods[0]`, take the first `Const` bound to a step named
`"move_to"`, and read the item's container out of `object_locations`. It worked for kitting's
current schemas only, and where it did not (a `Var`-bound target: every carry leg, every
`coffee_break` / `ac_activation` chord) the hypothesis silently scored NEUTRAL — 64/261/61/54
likelihood calls per scenario in the I1 audit (`analysis/i1_ir_audit/REPORT.md` §3.1). The
audit found the same lookup, weaker, duplicated three times (§4.1–4.3) and every method chosen
by position (§9.3–9.5).

Decision. Every tick, for every live hypothesis, the recognizer asks the planner what the
observed agent would do if it held that intention — `AdaptivePlanner.decompose(task, bindings,
agent_id, world)`, the same guard-selected method, derived vars and step grounding the executor's
plans come from — and scores against those GroundedActions:
- the chord target is the first movement action's target (`ActionSchema.movement_target_key`),
  resolved to a position by `shared/target_resolution.py`; the projector uses the same function
  for its segments. There is one answer to "where is the thing this action targets", and it is
  the object's CURRENT location, a carried object resolving through its holder (its
  `object_locations` entry is an agent id, i.e. a key of `agent_positions`). The planner's
  `home_container_of` derived var answers a different question — where an object belongs, a
  symbolic return destination — and stays a derived var; the two are not merged;
- completion predicates are the ones the planner already grounded (`GroundedAction.
  completion_predicate`); `_resolve_term_value` and its `"?agent"` literal are gone;
- ZONE_BOOST's target zone is the zone of the same object the chord is scored against;
- the held-item rule reads `AgentState.holding` and refutes a hypothesis that binds a portable
  object (one that has an `object_locations` entry) other than the held one — no parameter name;
- the agent's zone comes from the observation it was given (`spatial_context.zone`), not from a
  rebuilt `in_zone` predicate.
Method selection is re-evaluated every tick against the live world ("the world is the cursor");
which action a hypothesis is *on* is not stored — that is I3's per-hypothesis phase.
A hypothesis the planner cannot decompose in this world (no method's guards hold, a derived var
without a value — `DecompositionError`, a subclass of `ValueError` raised only for these
world-dependent cases) is scored NEUTRAL and logged once per episode, so an unscorable
hypothesis is visible rather than indistinguishable from an uninformative one. An unbound
variable or unknown lookup is a schema error and still raises: a domain modelling mistake must
not look like uncertainty (dock_loading's `confirm_delivered_pallet`, TODO-25, now fails
loudly at the first tick instead of being NEUTRAL forever).

Consequences measured (`analysis/i2_ir_foundations/REPORT.md`; every difference from the I1/F1
baselines attributed by stage): no target is unresolved in any of the eight conditions; the
carried item's hypothesis now receives the carry chord (grasp 0.797 → 0.966 mid-carry in
s00/s20/s30); `coffee_break` receives the coffee walk (s40: 0.02 → 0.81, θ at step 142, the
F1 segment-2 criterion). Two consequences the phase model (I3) inherits rather than I2 fixes:
(1) while the human carries X, every other `deliver_item` hypothesis selects
`deliver_with_return`, whose first step walks back to X's home shelf — the carry is strong
evidence against all of them, so after the release the delivered item leads by 0.8 : 0.05
(C5, no completion event) and the next task's approach is credited to it: s00_on's second
θ crossing moves from step 81 (mid-approach) to 111 (the grasp), s20_on's from 82 to 89,
s30_on's does not fire at all (the winner flips above θ, TODO-48); (2) a foreseeable task,
never refuted by a grasp and never completed, becomes a permanent attractor: `coffee_break`
stays `most_likely` for the rest of s40 (0.96 at the grasp of item_6). Both readings are on
record in the report; the evidence that settles them is what the completion pin does to
these numbers in I3.

wait_at. Its completion was a `ProcessCompletion` — executor-internal queue exhaustion that
nothing outside the executor could observe, so a phase model would stall on it forever
(`coffee_break` and `ac_activation` both end in it). The body runs the timer, so the body
says when the wait is over: on the last STAND the executor records the nearest fixed object
(the proximity rule release already uses) as `agent.waited_at`, `world_state_builder` emits
`waited(agent, object)` from it, and kitting's `wait_at` declares that predicate as its
completion — an ordinary ConditionSchema, no special case in `shared/`. The fact persists until
the agent's next step/grasp/release/touch (measured: visible for three ticks after each wait
in s40); a second `wait_at` at the same object issued before the agent moves would therefore
complete at once (no scenario does this — surfaced, not judged; the alternative, clearing on
action advance, is executor-internal state). dock_loading's `wait_at` keeps
`ProcessCompletion` (deferred domain; the executor branch stays for it).

Also in I2: the hypothesis list is sorted by key at construction and pinned keys are emitted in
sorted order, so tie-breaks and log order no longer depend on the process hash seed (measured:
s40 byte-identical on the four regression greps under PYTHONHASHSEED=0/1/2; TODO-42 for the
recognizer); the robot observes the human once before the clock starts (`RobotAgent.
observe_initial`), because the human acts before the robot observes within a tick and the
first step was never scored (I1 2.12); `env_layout1.json`'s `AC_switch` is spelled
`ac_switch`, so scenario_10 has an `ac_activation` hypothesis for the first time (9 → 10 keys).
Files: shared/recognizer.py, shared/planner.py (`decompose`, `DecompositionError`),
shared/target_resolution.py (new), shared/projection.py, domains/kitting/actions.py (`wait_at`),
mesa_sim/executor.py, mesa_sim/action_decomposer.py, mesa_sim/world_state_builder.py,
mesa_sim/sim_agents.py, mesa_sim/sim_model.py, domains/kitting/env_layout1.json
Reference: I2 IR foundations session, September 2026; analysis/i2_ir_foundations/REPORT.md

**A task's likelihood is the likelihood of the action it expects now (I3, the phase model)**
Until I3 the recognizer decided "which action is the human on" with a single `holding` check that
worked for `deliver_item`'s two stages and generalised to nothing: the first action of the selected
method answered for every observation, so no completion predicate was ever evaluated (I1: 0 of
5,579 likelihood calls), every grasp and release handed 1.0 to every hypothesis, and the "grasp
reveal" in every run was the held-item pin of the alternatives.

Decision. P(o_t | τ) = P(o_t | a_φ(τ)). For every live hypothesis, every tick, the planner selects
τ's method by guards against the current world for the observed agent (I2), the grounded actions are
walked from the start, and the EXPECTED action is the first whose completion condition does not
hold. This is a marginalisation over a latent action that collapses because the phase is derived
deterministically — not a nested recognizer; there is one normalisation, at the task layer, over
every hypothesis and `unknown`. Consequences, each chosen deliberately:
- PHASE IS DERIVED, ORIGIN IS STORED. A hypothesis keeps the action it expected last tick and the
  agent's position when it began expecting it (its origin). It never stores an index into an
  action list, because method selection genuinely flips under it (`deliver_item(Y)` becomes
  `deliver_with_return` while X is carried: index 2 of six actions is not index 2 of two —
  TODO-51). A change of expected action — an advance, or a regress when `at(agent, X)` flickers off
  at 30 cm, both derived facts — folds the closing action's final chord into the evidence once and
  moves the origin to the agent's position. Nothing is shared across hypotheses: no leg, no global
  base, no leg closed by the body's `stand`.
- The completion channel is judged on the action the hypothesis expected BEFORE the event. The
  world after a grasp already satisfies `pick_up`'s completion, so the action derived against it
  has moved on; the literal order "derive, then check the derived action's completion" can never
  find a completion that holds. An event multiplies; a chord replaces.
- The channel is gated by the action's own vocabulary: `GRASP` is judged against `pick_up`'s
  completion because `pick_up` declares `["GRASP"]`; `move_to` declares `"STEP*"` and is NEUTRAL at
  a grasp, exactly as before. The ungated reading — every expected action LOW at a discrete tick
  unless complete — is a new factor (P(event | movement action) was NEUTRAL, never LOW) and was
  measured, not shipped: it hands `unknown` ×10 against every live task at every grasp and release,
  so `unknown` sits at 0.96–0.99 after every completion and no second θ crossing occurs in any
  condition (`analysis/i3_phase_model/summary.md`, variant `ungated`).
- Likelihoods are memoised per tick by their inputs — (evaluator, origin, target position) for the
  progress channel, the grounded predicate for the completion channel — so two hypotheses expecting
  the same thing from the same place receive one value computed once; two items on one shelf are
  identical by construction (check U1).
- The evidence state is kept per hypothesis in ONE common scale (`_base`, rescaled by the tick's
  total so Σ base · chord = 1). Storing each hypothesis's base as its normalised value at its own
  advance tick, as the per-tick spelling of the algorithm suggests, carries that tick's normaliser
  into the cross-hypothesis ratios (a rival advancing at a tick where the leader's chord is 4.0 is
  charged ≈ ×3.6 for nothing); the common scale makes the result exactly the product over the
  hypothesis's own segments.
- COMPLETED TASKS leave contention, judged on the TERMINAL action's completion condition directly,
  whoever did it — `obj_at(item_7, kitting_table_0)` is true because the robot delivered item_7,
  and that is the signal wanted: the task cannot be done again. Completion latches (the fact may be
  transient: `waited` is visible for three ticks); the hypothesis is skipped in the update AND
  pinned at BELIEF_FLOOR on output, for the rest of the run, never removed from the space (the
  meta-planner resolves its keys). `[IR-complete]` logs each one.
- REMOVED: the held-item rule (a domain shortcut the phase model subsumes — the rival's expected
  action is elsewhere and the geometry refutes it, with no `?item`, no carrying-capacity assumption,
  and in domains with no holding relation) and ZONE_BOOST (fired for the wrong hypothesis in 28 of
  52 measured episodes, I1 5.4). `holding` is read only as a world fact through a grounded
  completion condition, never as a phase signal (check U5).

Measured (`analysis/i3_phase_model/REPORT.md`, every difference staged and attributed: S1 ZONE_BOOST
off, S2 + held-item off, S3 phase model without the pin, S4 = HEAD): completion evidence fires for
the first time — `holding(human_0, item)` HIGH for the grasped item's hypothesis at every grasp
(×4; 0.586–0.880 at the grasp tick depending on the live set), nothing at a release because the pin
preempts the channel; `coffee_break` is pinned at 184 in s40 (the first `waited` tick) and never
returns (TODO-50 closed); the delivered item is pinned at its release, so s30_on's TODO-48 flip is a
θ crossing again (98). Two structural findings recorded for the next stages rather than tuned here:
(1) the rival-targeting effect of `deliver_with_return` (TODO-51) is NOT removed by the phase model —
while the human carries X, `deliver_item(Y)`'s guard-selected method is `deliver_with_return` and
its expected action is `place(X, shelf_X)` then `move_to(shelf_X)`, so rivals are refuted ≈ ×0.1 per
carry and the next task's θ crossing stays at its grasp (s00_on 111, s20_on 89, s30_on 98; the
variant `ownshelf`, rivals decomposed as if nothing were held, gives 97 / 77 / none); (2) a
hypothesis whose expected action never completes keeps its t=0 origin, so under the cosine kernel
its whole history is ONE chord from the start and it is never charged for the detour —
`ac_activation` is `most_likely` (0.45–0.69) from 184 to 271 in s40 on the chord start → shelf_6.
I4's excess-path-cost likelihood, which reads the distance walked since the origin, is the term that
charges it; it must not be patched here with a distance factor.
Files: shared/recognizer.py; analysis/i3_phase_model/ (check_i3.py, REPORT.md)
Reference: I3 phase-model session, September 2026

**The evidence model: excess-path likelihood, detection reliability, a stated `unknown` (I4)**
Until I4 the recognizer's belief rested on four numbers with no stated meaning — the cosine kernel's
HIGH 4.0 / LOW 0.1, NEUTRAL 1.0 (also `unknown`'s flat value), ZONE_BOOST 2.0 before it — and I1/I3
traced every asymmetry they exposed to `unknown` paying nothing while wrong hypotheses averaged 2.3–3.1
against its 1.0. The kernel read direction only, so a hypothesis was never charged for the distance it
had wasted (TODO-53) and walking 116° away from a shelf was still better evidence for it than for
`unknown` (F1, segment 3b).

Decision. The structure I3 built (per-hypothesis expected action and origin, fold at a phase advance,
one normalisation over every hypothesis and `unknown`, the terminal pin) is unchanged; what goes into
it is replaced by four constants, each with a physical meaning (`shared/likelihood_functions.py`):
- MOVEMENT is the excess-path likelihood — Masters & Sardina's costdif1 (IJCAI-18) through the
  logistic of Ramírez & Geffner's RG2. Per hypothesis, from the origin where it began expecting its
  current action: excess = walked + C(pos, g) − C(origin, g), where `walked` is a per-observed-agent
  odometer read at the origin and g is the expected action's target; L = 2/(1 + e^{β·excess}). The
  wasted distance under the hypothesis: 0 for a straight walk at g, growing with every step away —
  direction and distance in one quantity. The `walked` term is kept (costdif2 drops it, preserving
  the ranking but not the values the θ gate reads; it is also observation-independent, a continuous
  ZONE_BOOST — measured as variant `costdif2`: coffee "revealed" at 120 by proximity, `ac_activation`
  wrongly at 297). C is a distance, not a path: straight-line by default (Mesa agents walk through
  obstacles), injected through `IntentionRecognizer(path_cost=...)` for a domain with something
  better; no planner calls, no distance fields. Recomputed from the origin every tick and REPLACING
  the previous value (twenty ticks of one walk are one observation); a completion is an event and
  multiplies. Cost per tick: one distance evaluation per (expected action, origin, walked, target).
- The logistic is NORMALISED to 1 at zero excess (a spec correction, measured): with the raw form
  (0.5 at zero excess) every phase advance folded 0.5 into a hypothesis that had done nothing wrong
  and halved it against `unknown`, whose value is never folded — s40's positive control dropped
  0.83 → 0.71 at its own grasp; s00_off/s20_off never reached θ. The value at zero excess is therefore
  the multiplicative identity (PERFECT_FIT_LIKELIHOOD = 1.0), also scored by a hypothesis with no
  graded signal (`pick_up`, `place`, `wait_at`: the agent is within reach of where that action
  happens, or the walk would have regressed to the approach). There is no NEUTRAL: a stationary tick
  leaves the excess where it was.
- `unknown` scores a stated CONSTANT, UNKNOWN_LIKELIHOOD, every tick. Normalisation is over all
  hypotheses AND `unknown`, never over the hypotheses alone. The constant is the threshold between
  "fits badly enough to be unexplained" and "a real hypothesis", and the CEILING on confidence:
  1/(1 + u) with every rival refuted. u ≥ 1/3 makes θ = 0.75 unreachable by construction.
- COMPLETION is a detection-reliability model: P(signal | completed) = DETECTION_HIT_RATE,
  P(signal | not) = DETECTION_FALSE_ALARM_RATE. In Mesa the simulator's report IS ground truth, so
  these are stated (1.0 and 1e-3 — the latter non-zero only so a refuted hypothesis keeps a
  recoverable base), not tuned; a real cell's detector supplies its measured rates. Consequence under
  the (unchanged) vocabulary gate: a grasp is no longer evidence — the grasped item is multiplied by
  1.0 and rivals are not judged — so the approach carries every reveal.
- β = 0.01 /cm and u = 0.1, from a JOINT sweep (49-cell coarse grid, 25-cell fine grid, prior-on
  s40/s30/s00; full matrix once at the chosen values): the region where every first task is revealed
  pre-grasp with no wrong task at θ is β ∈ [0.005, 0.1] × u ∈ [0.01, 0.2], smooth (the reveal tick
  moves ~1 tick per 0.05 of u, 3–6 ticks per β step, no cliffs); the chosen point is its centre.
  Meanings: 100 cm of wasted path costs ×0.54, ≈ 294 cm is no better than unexplained, ceiling 0.909.
  β is in cm, so the tolerance is layout-scale dependent (TODO-28's class); the fractional reading
  (excess / C(origin, g)) was measured and rejected — its reference length goes to zero at every
  carry-phase or 30 cm-regress origin, and where it produced coffee crossings (β_f ∈ [0.2, 1], u ≤ 0.1)
  it did so by coffee having the longest direct distance among the stuck-origin hypotheses, with s30's
  first task then revealed after its grasp (TODO-58).
- The fourth load-bearing number is the world-state builder's PROXIMITY_THRESHOLD (30 cm): it decides
  when `at` holds, hence every phase advance and every origin. Not a likelihood constant, named here
  because it was previously documented as unrelated.

Measured (`analysis/i4_evidence_model/REPORT.md`; every difference staged S0 → S1 raw logistic → new
and attributed): the first task of every scenario is revealed mid-approach, before the grasp, in seven
of eight conditions (s00 39/11, s20 31/6, s30 28/21, s40 19/19 off/on; s20_off's 31 is after its grasp
at 22 because two decoys lie beyond the target on the same bearing); no wrong task above θ anywhere;
θ is reachable for a first task even with two foreseeable hypotheses in the space (s40 0.904; F1's
0.569 came from pinning); TODO-53 closed — `ac_activation` is charged 2373–5664 cm and is `most_likely`
for 0 ticks of 184–271 (was 88). AND the design as specified recognises no task after the observed
agent's first one, at any β, u: a hypothesis the agent has not started keeps its priming-tick origin
(coffee enters its own walk with 2144 cm of excess and its efficient walk adds nothing to it), and
every closed phase is folded permanently (item_6 carries ×3e-9 × 1e-9 from segment 1). `coffee_break`
never crosses θ in s40 (max 0.001 at the shipped values; 0.68 anywhere in the sweep, at a point where
`ac_activation` wins segment 3), the segment-3b retraction is real in the excess (550 → 1088 cm) and
invisible at the floor, and every next-task reveal is gone (TODO-55). The diagnosis is the phase state
across a task boundary, not the trajectory evidence, `unknown` or the hypothesis space: the
analysis-only what-ifs that move every origin to the observed agent's task boundary (TODO-53's named
alternative) and also reset the prior there (TODO-55 (b)) give coffee 0.90 in both prior settings by
the intended chain, item_6 rising to 0.79 while the human heads at shelf_6 and retracting to 0.08 after
the turn, and pre-grasp next-task reveals prior-on (80 / 56 / 76) — with the prior-off caveat that a
retirement fires on the robot's completions too. Neither is shipped: what a task boundary IS to the
recognizer is a design decision (TODO-57), deferred with TODO-55.
Files: shared/likelihood_functions.py (rewritten), shared/recognizer.py (`__init__`, `update`,
`_progress_likelihood`, `_completion_likelihood`), domains/kitting/actions.py (`move_to.progress_evaluator`);
analysis/i4_evidence_model/ (check_i4.py, REPORT.md, sweeps, chain.py)
Reference: I4 evidence-model session, September 2026

**The recognizer estimates the intention of the current behavioural episode — and an empty stretch is not an observation (I4b, I4c)**
I4 left one defect: a hypothesis's origin moved only when its expected ACTION changed, never when the
observed agent finished a TASK, so every task the agent had not started carried the whole previous task
as wasted path (coffee entered its own walk with 2144 cm of excess). I4b's principle for the fix — "reset
the geometry, keep the belief" — was measured and found wrong, and I4c replaced it. This entry describes
what the model does now; the I4b principle is not amended here because it is false.

Decision 1 — what a boundary is (I4b, unchanged). Four definitions were ranked from the architecture and
measured from the existing logs before any code (`analysis/i4b_boundary/candidates.py`): (A) a retirement
whose hypothesis expected its TERMINAL action on the previous tick; (A') a retirement on a RELEASE; (B) the
first phase advance after any retirement; (C) a sustained stop of N ticks; (D) any phase advance. A is
shipped: it is literally the thing meant (the observed agent's own derived phase had reached the
completing action), it needs nothing the recognizer does not already hold (`_expected` and the planner's
action list), no constant and no rule, and it fired at 18 of 18 human task boundaries in the sweep and at
none of the robot's five prior-off completions. Its one assumption is named: authorship is inferred from
the agent's phase, not read from the world (there is none — I1 finding 5); a domain in which another
agent can satisfy a terminal condition while the observed agent stands in its terminal phase would
attribute wrongly. Rejected with numbers: A' assumes tasks end in a discrete microaction (kitting's waits
do not; misses coffee at 184); B needs an arbitrary "which hypothesis" rule and fires mid-approach after
the robot's completions (23,621 cm of decoy discrimination dropped); C needs N, and stops track boundaries
in these data only because a place stop lasts one tick longer than a grasp stop (N = 5, a kitting-executor
accident; 9,531 cm dropped; the waypoint pauses are invisible to it too); D fires 74 times, two ticks
before every grasp and release, neutralises every fold by timing and collapses the excess to the current
leg (132,250 cm dropped, wrong reveals prior-off).

Decision 2 — what a boundary does: the episode's inference ends (I4c). A task hypothesis —
`deliver_item(item_3)` — means "this is the task being executed now". It is not a standing disposition,
a preference or a belief about future tasks, and this architecture has no representation in which "the
human seems uninterested in shelf_9" could live. Carrying evidence from a completed episode into the next
one gives the belief a meaning the hypothesis does not have, and trying to make one number carry both
meanings is what produced I4b's fold asymmetry: a hypothesis that never phase-advanced holds its charge in
its OPEN stretch, not its base, so I4b's origin move discarded exactly the charge that happened to be open
and kept exactly the folds that happened to be closed (item_6 kept its segment-1 folds because its method
flipped under the carry; coffee returned to its prior because its never did — evidence retention depended
on accidental phase history). Semantics now: WITHIN a task, a phase advance ends a STRETCH, not an
episode — the completed stretch's evidence folds and is retained, so a task becomes more likely as more of
its actions verifiably complete (prefix accumulation; a core property, kept). AT a task boundary (the
observed agent completes a task — Decision 1's criterion), the belief re-initialises to the admissible
prior over the hypotheses still live, uniformly, for every hypothesis, with no dependence on fold history;
every origin moves to the agent's current position; completed tasks stay pinned. The re-initialisation
target is the prior the recognizer already computes at construction, recomputed over the live set (one
helper, `_prior`); no new state, no new constant. NO PERSISTENCE LAYER: cross-episode information is
explicitly outside the task-hypothesis model. If it is ever wanted it needs its own representation; it is
not to be smuggled into task belief. Nobody re-adds it. Consequence recorded: the completion channel's
events, permanent within an episode, are discarded with the rest of the base at a boundary — the I4b gate
statement's "unresettable by construction" now reads "within an episode".

Decision 3 — the pin and the boundary do not share a criterion, and the difference is now visible. The
terminal pin (I3) fires on the world's completion condition whoever satisfied it: `obj_at(item_7, table)`
means the task is done and nobody can do it again — the right question for pinning. The boundary asks
whether the OBSERVED AGENT changed episode. A ROBOT completion therefore pins (the normalisation set
shrinks) but does not re-initialise: with the human idle after its last task, prior-off, the belief steps
from 1/3 each over {ac, item_5, unknown} to 1/2 each when the robot delivers item_5 (s40_off, tick 376).
That is correct, it looks odd in a log, and the two are deliberately not unified.

Decision 4 — an empty stretch is not an observation (I4c). dC = 0 used to mean two things: a perfectly
efficient walk, and no walk at all. A stationary tick after an origin reset produced the second and was
scored as the first, so a lone surviving hypothesis sat at 1/(1+u) = 0.909 on nothing and `unknown` was
implicitly penalised for the human standing still (I4b's 63 wrong-task ticks; TODO-59). dC is defined over
an OBSERVED MOVEMENT STRETCH; an empty stretch (nothing walked since the origin: the tick a hypothesis
enters an action, the ticks after a boundary before the agent moves, t = 0) contributes NO FACTOR — not
1.0, not a neutral constant — and `unknown`'s constant, being the likelihood of an observation, applies
only on a tick on which some hypothesis was scored on one. Rejected: L = 1 for tasks (frames absence as
perfect fit and penalises `unknown`); L = 1 for all including `unknown` (numerically the same per tick,
but asserts a likelihood where no observation exists); any neutral constant (no semantic basis). An
action with no graded signal (pick_up, place, wait_at) keeps I4's perfect-fit value: the agent within
reach of where the action happens is an observation with nothing to charge. Explicitly deferred and NOT
part of dC: stationarity as evidence AGAINST hypotheses that predict movement — a different observation
channel with its own model, recorded (TODO-59), not built.

Measured (`analysis/i4c_episode/REPORT.md`; `neither` — both changes reverted — reproduces I4b
byte-for-byte in all eight conditions): next-task reveals appear in every scenario (pre-grasp prior-on:
s00 81, s20 57, s30 77; prior-off 117/96/87), with no wrong crossing; coffee crosses θ at 135 (prior-on)
and 143 (prior-off), later than I4b's 125 because item_6 (and prior-off the robot's items) now compete
from the prior instead of from the floor; I4b's 63 wrong-task ticks are gone (the 47 idle-tail ticks by
Decision 4, the 16 segment-3a ticks by Decision 2, which makes item_6 a live competitor); segment 3b's
retraction is visible (item_6 0.790 → 0.083); retention across every boundary is uniform (every live base
equal at the boundary tick, with 0 to 3 advances in the ended episode). Two things Decision 4 exposes, for
I5: (1) `unknown`'s u is charged per OPEN observation and never folded (I4's ceiling design), so the belief
that carries forward on a tick with no observation is the base ratio — 1:1 against `unknown` for a task
with only perfect folds — and a lone live hypothesis dips from 0.905 to 0.498 on the grasp tick (TODO-60,
corrected in I4d — next entry); (2) confirmation is length-blind — L(0) = 1 after one step as after 400 cm — so
a 20-tick walk aligned with shelf_6 takes item_6 to 0.79 (11 wrong-task ticks, s40_on; TODO-61, open).
Files: shared/recognizer.py (`update`, `_begin_episode`, `_prior`, `_progress_likelihood`,
`_task_boundary`); analysis/i4b_boundary/, analysis/i4c_episode/
Reference: I4b task-boundary session and I4c episode-semantics session, September 2026

**`unknown` folds with the stretch: a hypothesis's evidence is its odds against `unknown` over its own observations (I4d)**
The defect (TODO-60) was a FALSE EVENT at the IR / meta-planner interface: a task's stretch folded into its
base as L alone, `unknown`'s u for that same stretch was charged only while the stretch was open, so on the
fold tick the task's odds against `unknown` fell from 1/u to 1 — a lone live hypothesis dropped from 0.905
to 0.498 on its own grasp tick, recovered at the first step, and `theta_crossed` fired a second time with
nothing new observed (s00_on 113, s20_on 91, s30_on 100). Not a retune and not a new evidence source: the
evidence a stretch provided for "this task rather than unexplained behaviour" was lost in the transition
from open to folded.

The accounting, stated before the implementation and checked after it. For every live hypothesis k and every
tick t within an episode:

    E_t(k) / E_t(unknown) = [π(k)/π(unknown)] · Π_{stretches s of k closed by t} L_k(s)/u
                            · Π_{events e of k} c_k(e) · ( v_k(t)/u if k's open stretch is an observation, else 1 )

`unknown` is the reference hypothesis. Each task's odds against it are the product over that task's OWN
observations of L/u — closed stretches and events in its base, the open stretch multiplied on top as v/u —
and a fold moves one factor from the open term to the base without changing it. `unknown`'s base is the
reference and takes no factor; the empty-stretch rule (TODO-59) is untouched: no observation, nothing on
either side. Representation: `_base[k]` holds k's closed odds; `_base[unknown]` only rescales. Verified by an
independent accumulator driven only by the phase state and the likelihood functions: max |Δ log odds|
7e-15 over 5,069 tick-hypothesis checks in the eight conditions (`analysis/i4d_fold_unknown/invariant.csv`);
the reversion variant reproduces I4c byte-for-byte in all eight.

What the accounting makes explicit, and is accepted with it: (1) a lone fitting task's ceiling is 1/(1+uⁿ)
over its n observations — 0.905 on the first stretch, 0.986 after the first fold, 0.995 after the second —
no longer 1/(1+u); (2) between two tasks of equal fit an extra closed stretch is worth 1/u, so a phase advance
is evidence and the plan's segmentation of the trajectory matters (prefix accumulation, I4c's stated core
property, now real against `unknown` and between tasks); (3) a regress folds too, and a phase with no graded
signal folds its perfect-fit value as 1/u; (4) on a mixed tick the hypothesis whose stretch is empty pays
nothing while its rivals pay their L/u — I4c's global "u if some hypothesis was scored" was this rule's
approximation; (5) events and the episode boundary are unchanged.

Measured (`analysis/i4d_fold_unknown/REPORT.md`): the three re-triggers are gone (0.905 → 0.986 through the
grasp, no `[meta]` line); I4c's results hold — next-task reveals 81/57/77 prior-on and 87 in s30_off, coffee
135/143, the 63 wrong-task ticks still gone, 3b's retraction 0.790 → 0.083, s30 pre-grasp, TODO-53 closed;
the working region is unchanged (the closed-form windows contain no fold). Reported, not fixed: prior-off the
correction lifts the true task above θ at its ARRIVAL (s00_off 109, s20_off 20 and 87 — pre-grasp, where I4c
had 117/31/96), and the rivals' method flip at the grasp then opens a `place` phase worth 1/u (point 3) and,
on departure, a fresh zero-excess stretch (TODO-61), so the true task dips under θ twice and `theta_crossed`
fires three times per recognition (109/113/115, 20/24/30, 87/91/95) — the same interface defect with a
different producer, the rivals' phase structure under `deliver_with_return`, which belongs to TODO-55 (e) and
TODO-61, both open. Also: item_6 is recognised at 274 after its 539 cm detour (×0.09) is outweighed by two
fitting observations (×10 each) — point 2 in action.
Files: shared/recognizer.py (`update`: the fold and the open term); analysis/i4d_fold_unknown/
Reference: I4d fold-unknown session, September 2026

**I5 — confirmation and hand-back: what the recognizer guarantees, what is a characterised limitation, what travels to the meta-planner work**
No model change. The final matrix at HEAD (`analysis/i5_handback/`) reproduces I4d's logs byte-for-byte, the
I4d reversion reproduces I4c's, the invariant holds to 7e-15, and every result carried forward from I4–I4d is
asserted (`criteria.md`). The hand-back — `docs/recognizer_handback.md` — is the central artifact: the model
in a paragraph, the four parameters, the GUARANTEE STATEMENT (prior-on and prior-off separately; what is
conditional on β/u/θ, and what on Mesa's straight lines, PROXIMITY_THRESHOLD = 30 cm and kitting's guards),
the characterised limitations, the `theta_crossed` interface question, the open items, and the removed
mechanisms that must not return.

Decisions recorded here: (1) TODO-61 is BROADENED to one item with two lettered, separately closable
statements — (a) confirmation is length-blind, (b) accumulation is observation-count and decomposition
sensitive — because they share one root (costdif1 with a constant `unknown`) and any remedy for one changes
the other's currency; both are PROPERTIES OF THE CHOSEN MODEL, visible in I4d's accounting, not defects
found in I4d. (2) The prior-off repeated `theta_crossed` is three separate things and stays so: the belief
trajectory is what the model implies (recognizer correct); the contract defines a crossing event and does
not promise one per task, so a one-shot semantics would be an interface decision (TODO-68), not an evidence
question; the meta-planner's handling is handed over with TODO-48/54. (3) Two analytical tools from the I4
design discussion are filed, not built: the radius of maximum probability (TODO-62, a diagnostic on the
model) and the rationality measure (TODO-63, which competes with the constant `unknown`). (4) The
paper-facing divergence is flagged in the hand-back: the HCM paper writes P(task | O) over a sequence of
ACTIONS; the recognizer observes a microaction and a position, the action is LATENT, and
P(o | τ) = P(o | a_φ(τ)) is that marginalisation collapsed by the derived phase (the I3 entry above). The
paper is a position paper, outdated relative to this design, and not a specification.
Files: docs/recognizer_handback.md, docs/TODOS_AND_DEFERRED.md (TODO-61 to TODO-68), analysis/i5_handback/
Reference: I5 hand-back session, September 2026

**Task completion is a world fact: the pool reads it from the WorldState, not from the executor's bookkeeping (T7)**
`MetaPlanner.update()` assembled its task pool from the robot's own bookkeeping — `ExecutorState.current_task`
plus the queue — and nothing in the meta-planner asked the world whether a pooled task was already done.
That made the executor a second owner of "what remains to do", and it is a lagging one: the embodiment's
executor learns of its own task's completion up to two ticks after the terminal condition holds (the fact is
in the WorldState the tick after the RELEASE; the executor advances past the action that tick and clears the
task the tick after, and the cognitive loop runs before execution within a step). A trigger inside that window
(s30_off 87, `theta_crossed` one tick after the robot's `[IR-complete]` at 86; s00_off 166) offered the
finished task as a candidate, and since the planner decomposes from the live world with no notion of a
satisfied goal, `deliver_item` of an item already on the table projects as a cost-3 re-grasp-and-re-place,
which wins any argmin. The robot re-did its own delivery (TODO-67).

Decision: a task's completion is a fact about the WORLD — its terminal condition holds, whoever made it hold —
and the meta-planner reads it from the world on every call, never from who performed it and never from a
flag it keeps. The generic test lives on the planner, the owner of decomposition, as
`AdaptivePlanner.is_complete(task_name, task_params, agent_id, world)`: a `TaskSchema` declares no goal of
its own, so a task's completion is the completion condition of the terminal action of the method its guards
select — derived from the schema through the same decomposition the executor and the recognizer use, no
predicate name known anywhere in `shared/`. It is the criterion the recognizer already retires a hypothesis on
(`_terminal_complete`; that private copy should delegate to the planner's method in a recognizer-side change).
`update()` drops every complete task at pool assembly (`[meta-pool] … complete in world: dropped from the
pool`), before B1.5/B2/B3, so a completed current task is neither continued nor a candidate. Nothing is
duplicated: the queue invariant (`_queue` holds only tasks not executing; the in-progress task lives solely in
`ExecutorState.current_task`) is untouched, B3's queue rewrite persists the drop, and an empty pool after the
drop is the existing terminal return — "all assigned tasks are complete" now means exactly that, including
tasks someone else finished. `no_current_task` still fires from the executor's clearing; the pool no longer
depends on it for correctness.

Companion (T8): `update_human_projection()` refuses `belief.most_likely == UNKNOWN` as `none(unknown)` before
calling the projector. Mass on `unknown` above θ is not a recognition (recognizer_handback.md §3.4: something
outside the hypothesis space, between tasks, or a deviation) and there is no trajectory to project. The
projector had been returning None for it by accident — `unknown` has no hypothesis entry to resolve — under
the `none(unresolved)` reason, so admission was correct by the resolver's ignorance rather than by decision;
`none(unresolved)` again means an unresolvable hypothesis only. The trigger still fires on `unknown`; whether it
should, and the one-shot semantics, are TODO-68's interface question, deliberately not decided here.

Sweep (PYTHONHASHSEED=0, analysis/t7_t8_meta_bugs/): decisions move only where the re-delivery was — s30_off
item_4 at 87 instead of 93, run end 157 instead of 163; s00_off run end 166 instead of 172 — and `[IR]` /
`[IR-dist]` lines are byte-identical up to the tick the robot's earlier delivery changes the world the
recognizer reads (s30_off 155, the item_4 pin; s00_off's are a prefix, the run simply ends earlier). The
recognizer is untouched. These runs are the meta-planner-side regression baselines from here on.
Files: shared/meta_planner.py (`update`, `_is_complete`, `update_human_projection`), shared/planner.py
(`is_complete`), analysis/t7_t8_meta_bugs/ (compare.py, stages.sh, summary.md)
Reference: T7/T8 session, September 2026; TODO-67, TODO-54, TODO-68

**The robot can wait: realization prices a conflict as duration, and B2 and B3 both consume it (Phase 4C wait-decision revision)**
Phase 4C paused on one question — whether the robot can WAIT for the human — and it is settled here,
together with the restructuring of `update()` that follows from it. This entry RECORDS the design; the
realization function itself lands in a later task, after its one open parameter (`min_separation`,
TODO-28) is decided on re-measured data. Nothing below is implemented at the time of writing except
the comment-level consequences (see the T7/T8 baselines: byte-identical after this entry).

THE DECISION. T1 (`analysis/t1_conflict_measurement/`) established that the interference in our
fixtures is a TIMING conflict, not a path conflict: both agents arrive at the shared kitting table
within a tick of each other. The proportionate response is to wait briefly, not to abandon the task.
The robot could not wait — its only lever was WHICH task to do, so the only available response to a
conflict was to switch, the over-reaction — and pricing a conflict the robot would never act on would
have been a cost fiction. Decided: the robot can wait. A pause is computed from the human's
projection, it enters the cost, and it reaches the executor as an execution HINT. A hint, not a
command, because the human may deviate within a few ticks and the executor's own collision handling
differs per embodiment; the hint is a preplan that saves the executor solving avoidance from scratch.
The line this must not cross (roadmap Phase 6, the single-decision-path NOTE in TODOS_AND_DEFERRED):
the decision is made ONCE, in `shared/`. The executor may REFINE a hold. It must not independently
decide whether to wait, or which task to run, or silently cancel the decision — that would produce
the cost in one place and the behaviour in another, with neither authoritative. Rejected: "estimate
the pause now, execute it in 4D" — a cost containing a hold the robot never takes is a fiction, and
any B2/B3 result measured on it would describe a plan that was not executed.

THE SECOND FINDING: A BATCH INTERFERENCE PROFILE CANNOT PLACE A HOLD. `_detect_interference()`
answers "over these two FIXED trajectories, where do they come close". It cannot see that holding at
the first conflict shifts everything after it, so later conflicts may vanish, shrink or worsen; its
answer is stale the moment a hold is placed. T1 also measured that its aggregates mislead: every
conflicted `min_dist` was at the LAST step of the shared window (an arrival-time gap, not a closest
approach), and exposure (steps below s) ranked candidates OPPOSITE to the pause they actually require
(s20_on step 11, pre-T2 projection units: item_4 close for 188 steps needs δ = 67, item_7 close
for 36 steps needs δ = 144).
A gate built on those aggregates would gate on a misleading number.

WHAT REPLACES WHAT.
- `_detect_interference()` as a public step in B3 (project → detect → drop infeasible → `_cost`):
  SUPERSEDED by one `realize()` per candidate; interference detection becomes INTERNAL to it.
- DESIGN-08 (`_detect_interference` observes, `_cost()` the only place a conflict COULD become a
  number; computed, carried, unused): RESOLVED — conflict becomes cost BY CONSTRUCTION. A conflicted
  task is dearer because avoiding the human genuinely takes longer. No conflict weight, no term to
  tune. See "what survives" below.
- `min_safe_distance` as an exclusion threshold: RESTATED as `min_separation`, the clearance
  realization must ACHIEVE. Still the single policy decision. DECIDED (R1, September 2026,
  TODO-28): `min_separation` = 2.5 × the robot's motion per tick — 50 cm on the current layouts
  (20 cm/tick) — expressed relative to motion so that it scales with the body, not as an absolute
  in `shared/`. To be revisited under randomised layouts (TODO-47) and real body sizes (ROS).
- "infeasible" = a ConflictPoint below the threshold: RESTATED — "infeasible" = NO REALIZATION EXISTS
  within the human's projected horizon. Rarer, and meaningful.
- all-candidates-excluded raises `RuntimeError`: SUPERSEDED — the condition changed meaning and the
  outcome is DECIDED (R1; below): plain-cost argmin, logged `all_unrealizable`.
- interference measured in BATCH over whole trajectories (~900–1500 ConflictPoints, TODO-27):
  SUPERSEDED by PER SEGMENT, earliest violation given a start time.
- B2 has no scalar to compute (stub, TODO-36): RESOLVED — realization gives B2 the current task's
  hold δ. What δ is judged against is DECIDED (R1; below): the human's remaining projected
  duration at the trigger, through the policy parameter ρ.
UNCHANGED and reaffirmed: DESIGN-16 single-task receding horizon (realization changes what a candidate
COSTS, not how many are chosen); trajectory algorithms MEASURE ONLY and hold no policy (realization
asks them a different question; `min_separation` is passed IN); the queue invariant (`_queue` excludes
the executing task; candidates = `[current_task] + queue`); cancellation is an HTN method choice,
never a cost term (realization adds HOLDS, never methods); plans are re-decomposed from scratch and
realization produces no persistent state; interference is geometric, not zone-based; projection is a
service separate from selection — realization belongs on the projection / trajectory side, NOT in
`MetaPlanner`, which supplies `min_separation` and consumes the result; task exhaustion is returned,
not raised.

DESIGN-08 — WHAT IS RESOLVED AND WHAT SURVIVES. DESIGN-08 asked WHERE conflict becomes a number: in
`_cost()`, or gated in B2. The answer is NEITHER — it becomes a number in realization, as duration.
The question is settled rather than answered as posed. What survives, recorded so that "DESIGN-08
closed" is never read as "the split was abandoned": the separation between OBSERVATION and VALUATION
is intact, relocated. `earliest_violation` OBSERVES (pure geometry, no policy); holding is what turns
that observation into a number. Realization is GIVEN `min_separation` rather than choosing it, so no
policy has leaked into the geometry. Also surviving, unchanged: team-level semantic costs (a human's
time valued differently from the robot's, disruption, fairness) remain PARKED as a future extension
(TODO-15). Realization prices only the robot's own time.

THE REALIZATION FUNCTION. Lives in the projection / trajectory layer. Its placement, one-way, no
cycles (supersedes the three-layer diagram under "Projection is a service, separate from
selection"):

    trajectory_algorithms.py   pure geometry   segments in -> earliest violation / conflicts out
            |
    realization (hold-only)    "what would this trajectory actually be, given the human?"
            |
    projection.py              Projector       task + world -> predicted trajectory
            |
    meta_planner.py            MetaPlanner     which trajectory to pick

`MetaPlanner` consumes `realize()` from the projection layer — the one call it makes below itself
besides `Projector`, and it supplies `min_separation` (CORRECTED at T3b: the earlier "never reaches
below `projection.py`" wording contradicted the `update()` sketch below, which calls `realize()`
directly); realization never reaches above `trajectory_algorithms.py` for its geometry and knows
nothing of tasks, beliefs or selection.
Pluggable strategies, mirroring how `trajectory_algorithms.py` is organised:
- hold-only — TO BE IMPLEMENTED (later task): stand still until the way is clear, then proceed;
- detour — documented, unimplemented: go around. Needs a path planner and introduces iteration
  between trajectory and interference (`obstacle_aware_path()`'s role; Phase 4D);
- off-the-shelf planner (PRIEST or equivalent, ROS) — documented, unimplemented (Phase 4D).
Interface (design; the exact signature is the implementer's):

    realize(projected_plan, human_projection, min_separation, start_tick)
        -> RealizedPlan | None        # None: no realization within the horizon
    AS BUILT (T3; ruling T3b): realize(plan, human_plan, min_separation, decision_step)
        -> RealizedPlan               # never None: `realizable` flag and a `reason`
    AS BUILT (F1): the same signature; always a cost, no `realizable` flag

`RealizedPlan` carries: the placed (shifted) segments; the hold δ (where — the trigger position —
and how long); the realized cost T_r + δ; and the share of the trajectory lying BEYOND the human's
horizon and therefore unassessed (TODO-69).

HOLD POLICY — DECIDED (R1, September 2026, after T1b): WHOLE-TRAJECTORY MINIMAL SHIFT. One hold δ,
taken at the robot's position at the trigger tick (which may be partway along a segment — the plan is
projected from where the robot is); every later segment shifts by δ. δ is the SMALLEST shift ≥ 0 such
that the shifted trajectory — including the stationary hold stretch at the trigger position itself —
has no violation in the assessed window. In outline:

    δ = min { d ≥ 0 : no violation in [trigger, T_h] of
              hold at p_trigger for [trigger, trigger + d],
              then the projected segments shifted by d }
    if no such d exists, or the only ones extend the hold to T_h: unrealizable (None)
    (as built: unrealizable = RealizedPlan(realizable=False, reason); d in WHOLE ticks — T3b, below)
    return RealizedPlan(shifted segments, hold = (p_trigger, δ), cost = T_r + δ, unassessed share)

This REPLACES the per-segment loop written in the first version of this entry (hold each segment at
its start until its earliest violation clears, then re-check the next). T1b (`analysis/t1b_realization/
REPORT.md`, Finding 2) measured that loop and showed it was not the policy it described: its hold ran
from the segment's start to the clear time rather than the minimal shift, and when a violation ran to
the robot's arrival it held a full segment, overshooting the minimal hold by 5–25 ticks (median) in
every differing row, reversing two argmins the minimal hold keeps, and turning the same table
convergence into "hold a carry" or "unrealizable" depending on which agent arrived first. The
per-segment policy at its minimal hold and the whole-trajectory shift agreed on δ in every row where
both realized, and differed only where per-segment dead-ended at the table by committing an early
segment. Per-segment holds at segment boundaries are therefore OUT. A hold at a chosen point ALONG a
segment (walk part way, then stop) is DEFERRED (TODO-70). Waiting somewhere other than where you are
is a DETOUR, a different strategy (Phase 4D).

A VIOLATION IS A DISTANCE. Agents are points; a violation is any moment at which their distance is
below `min_separation`. Conflicts of position or of path (for example head-on on the same line, or
the human's path passing the robot's standing position) need no special case: they come out as
UNREALIZABLE through the hold-position check, because no shift clears a hold whose position the human
passes within `min_separation`. SUPERSEDED (F1): a violation is the ROBOT'S MOTION within
`min_separation` without the distance increasing; the human passing a standing robot is not one, and
nothing is unrealizable.

PROPERTY 1 (unchanged): A HOLD IS A POSITION — while holding, the robot stands where it is, and that
stationary stretch is checked like any other segment; T1 found holds that "cleared" only because the
waiting position was never checked. SUPERSEDED (F1, "Robot-responsible separation"): a standing robot
is never in violation, so the hold is no longer checked — deliberately, not by omission.
PROPERTY 2 (AMENDED, R1): REALIZABLE means NO VIOLATION WITHIN [trigger, T_h], where T_h is the end
of the human's projection. The robot's plan beyond T_h is UNASSESSED: recorded as such (the unassessed
share on `RealizedPlan`), and treated neither as clear nor as blocked. A violation cut off by T_h is
still a violation. (The first version's "termination" property belonged to the loop; the minimal
shift has no iteration to terminate — its search is bounded by the hold cap below.)
HOLD CAP: a hold may not extend to T_h. A candidate that clears only by waiting until the human's
projection ends is UNREALIZABLE, not "realized with a long hold" — T1b showed that every hold in the
fixtures is a hold into the unassessed tail, and a hold reaching T_h would be clearing by outlasting
the assessment rather than by avoiding anything within it. DELETED (F1): holding is always admissible;
a hold to or past T_h is priced as T_r + δ and leaves the plan in the accepted unassessed tail.
COST: realized cost = T_r + δ over the robot's FULL plan, with T_r the plain projected duration. The
unassessed tail is inside T_r and is not corrected for (TODO-69 decided as reading (1): no correction;
the unassessed share is logged).
INPUT: `realize()` does not assume its input is a single task's plan — it takes the projected
segments of whatever ordering it is given, so B3's `full_reorder` could use it later without a second
realization. It lives in the projection / trajectory layer, not in `MetaPlanner` (already settled
above).
THE HOLD IS AN EXECUTED HINT: δ travels in `UpdateResult` with the winning task; the body executes it
— in Mesa as STAND microactions at the trigger position, before the plan continues — unless a later
trigger re-decides (a fresh `update()` re-realizes from the robot's then-current position; a hold
re-realized identically keeps its countdown, T5). TODO-71's "hold before the segment it precedes"
wording is superseded by this: there is one hold, and it is at the trigger position.
AS BUILT (T4): `UpdateResult.hold` (whole ticks) and `Executor.hold()`. Every decision replaces the
hold in progress with its own δ, and the ticks not yet run are logged as interrupted. In both
measured interruptions the fresh δ was exactly the remainder, which is T5's "keeps its countdown".
RULED (T4 report): A DECISION WITH NO PROJECTION DROPS A HOLD IN PROGRESS. While the robot holds it
stands, so `task_committed` cannot fire; its task cannot complete, so there is no `no_current_task`,
which B1.5 would route past B2 anyway. The remaining route is a `theta_crossed` whose projection is
not admitted (`most_likely` `unknown` or unresolvable, since the crossing clears the gate). The
recognition behind the hold then no longer stands, and a hold computed against it should not survive.
Recorded in TODO-71.

`earliest_violation`: per robot segment against each time-overlapping human segment. Both have
constant velocity, so relative motion is linear and squared distance is a quadratic in time — no real
root below `min_separation²` means no violation; the roots give the violation interval. CLOSED FORM:
no sampling, no resolution parameter, and no world-unit constant in `shared/` (the class of assumption
the T2 follow-up removed). This is what `closest_point_of_approach` was reserved for. Under the
whole-trajectory shift the geometry is asked "is there any violation in [trigger, T_h] for the
trajectory shifted by d", and the minimal d is found from the violation intervals (T1b's `whole`
realizer is the reference: `analysis/t1b_realization/realize.py`, validated by sampling to 0.01 tick).
`discretized_time_sampling` can serve as a fallback but computes more than a hold needs.

THE ROLE OF REALIZATION IN B2 AND B3 — BOTH CONSUME IT. This changes what each block IS.
B2 = PLAUSIBILITY. Mid-task, is the current task still worth continuing? A gate: continue, or
escalate to B3. Reached only by `theta_crossed` and `task_committed` (`no_current_task` bypasses via
B1.5 — there is nothing to continue). B3 = REORDER / SELECTION. Under `single_task` (the only
implemented strategy, DESIGN-16) it picks the best NEXT task; the rest of the pool becomes the queue,
unordered. `full_reorder` stays a documented flag. REALIZATION IS SHARED MACHINERY, NOT OWNED BY
EITHER BLOCK. Both consume it; they differ in how many tasks they realize and what they do with the
result: B2 realizes the CURRENT TASK ALONE and judges its hold δ — one candidate's work, far cheaper
than B3, and the graded worthiness scalar B2 always lacked; B3 realizes EVERY candidate and takes the
argmin of realized cost — "continue, paying a 2-tick hold" and "switch, paying 19 ticks of walking"
become directly comparable numbers. CONSEQUENCE: B3's argmin now already accounts for conflict, so
B2's original rationale — that B3 could not express "close is bad" (TODO-28's scenario_20 finding) —
is gone. B2's remaining candidate roles are narrower: computation saving, and hysteresis (which
matters more now that prior-off `theta_crossed` can fire up to three times per recognition, TODO-68).
DECIDED (R1, September 2026, TODO-36): B2 SURVIVES, as `b2a`, and its role is COMMITMENT — it can
only prevent a switch B3 would make. `b2a` realizes the current task alone and CONTINUES if
δ ≤ ρ × (the human's remaining projected duration at the trigger, T_h − trigger); otherwise, or if
the current task is unrealizable, it escalates to B3. `human_projection is None` still means continue.
ρ is an explicit `MetaPlanner` policy parameter, default 0.5 — a stated assumption to be varied in the
ablation (T6), not a calibrated value. RULED (T4 report): the human's remaining projected duration is
T_h − 0, from the decision instant to T_h, not T_h minus the observation offset. The human is acting
from the decision instant; the offset (L2) concerns where its position is known, not how long it is
still acting. `b2b` stays a documented stub. B3 stays `single_task` (B3.A)
with realized cost (T10); `full_reorder` stays out of 4C. Under `b2a` a repeated `theta_crossed`
(TODO-68) mostly ends in a continue, which may also hide a real change of belief (TODO-48) — to be
decided from the T4 and T10 logs (D2). To be built: `b2a` in T4, B3.A with realized cost in T10.
`_cost()` becomes the realized duration and stops being a place where a policy could hide. When
`human_projection is None` — now a ROUTINE mid-run state, because the belief re-initialises at every
human task boundary (I4c) — realization is not called and cost is the plain projected duration,
exactly as today.

`update()` after the revision (design shape, not a patch):

    update(belief, world, executor_state, human_projection) -> UpdateResult
      # Block 0 — pool assembly (unchanged, incl. the T7 completion drop)
      pool = ([current_task] if not None else []) + _queue
      drop tasks already complete in the world (planner.is_complete)
      if pool is empty: return UpdateResult(None, [])
      # B1.5 — branch, unchanged
      if current_task is None: goto B3
      # B2 — commitment gate (R1)
      #   "none": False always (default)
      #   "b2a" : realize the CURRENT TASK ALONE (T4); continue iff it realizes
      #           and δ ≤ ρ × (T_h − now), ρ = 0.5 by default
      #   "b2b" : documented stub                                     [redundant with B3]
      #   human_projection is None -> True (continue)
      if _is_current_task_plausible(...): return UpdateResult(current_task, _queue)
      # B3 — reorder / selection (single_task; realized cost from T10)
      for task in pool:
          proj     = projector.project(task, world)
          realized = realize(proj, human_projection, min_separation, now)
          if realized is None: continue        # unrealizable within [now, T_h]
          cost = realized.cost                 # T_r + δ, ONE number
      if no candidate realized:                # all_unrealizable (R1)
          cost = plain projected duration for every task (as with no human projection)
          log "all_unrealizable"; hold = none
      winner = argmin cost
      _queue = pool - winner
      return UpdateResult(winner, _queue, hold = winner's δ at the trigger position)

ALL CANDIDATES UNREALIZABLE (SUPERSEDED, F1: the condition cannot arise; the fallback built at T10 was
removed) — the condition means: for every task, no shift within the human's
horizon clears the separation (e.g. the human's path passes the robot's standing position within
`min_separation`, or a human at the kitting table blocks every delivery in the pool). DECIDED (R1,
September 2026; resolves TODO-30 and TODO-52): select by PLAIN PROJECTED COST — the argmin with no
hold, exactly as when there is no human projection — and log the trigger as `all_unrealizable`. The
`RuntimeError` is superseded. The justification is the assumption recorded in the next entry: what
realization cannot resolve within the projection is left to execution-time avoidance. Of the three
readings once listed here, this is (2) without the "least-bad" ranking — a candidate that does not
realize has no realized cost to rank on, so the plain cost is used for all of them — and it records
the event so that (3)'s question (a mis-set `min_separation`, a short horizon) can be asked of the
logs. T1b measured the condition to be absent below 50 cm and rare (1 of 43 admitted triggers) at
50–100 cm on the fixtures; from 150 cm it is the majority case.

DECIDED at R1 (September 2026), after T1b, in one place: the whole-trajectory minimal shift (above,
TODO-70); a violation is a distance; Property 2 as amended and the hold cap; cost = T_r + δ with
TODO-69 as reading (1); `realize()` not single-task; the hold as an executed hint (TODO-71 wording
superseded); `min_separation` = 2.5 × motion per tick (TODO-28); all-unrealizable → plain cost
(TODO-30, TODO-52); `b2a` with ρ = 0.5 (TODO-36); B3.A with realized cost. STILL OPEN: what a trigger
is an event OF (TODO-68 / 48 / 54 / 64 / 65) — D2, to be decided from the T4 and T10 logs; the hold
at a chosen point along a segment (TODO-70); the body-side details of the hint beyond "STAND at the
trigger position" (TODO-71: how a refined hold is reported back, a hold outlasting the next trigger);
Mesa's own execution-time avoidance (TODO-73). The order of work is in roadmap.md (Phase 4C queue).
Files: docs only at this revision and at R1. To be touched when realization lands: shared/projection.py
or a new realization module (`realize`, `RealizedPlan`), shared/trajectory_algorithms.py
(`earliest_violation` — the role reserved for `closest_point_of_approach`), shared/meta_planner.py
(`_replan_tasks`, `_cost`, `_is_current_task_plausible`, `min_separation`, ρ), shared/types.py
(`UpdateResult.hold`), mesa_sim/executor.py (the hint)
Reference: Phase 4C wait-decision session, September 2026; T1 measurement session; T1b
(`analysis/t1b_realization/REPORT.md`); R1 decision record, September 2026

**Assumption: execution-time avoidance past T_h — realization decides only within the human's projection (R1)**
Realization assesses the robot's plan against the human's projection and nothing else, so it can
only decide within [trigger, T_h]. What happens after T_h — the robot's unassessed tail, the human's
next task, a hold that was refined away — is NOT the meta-planner's to decide and is left to an
EXECUTION-TIME AVOIDANCE layer: local, reactive, simulator-dependent, and belonging to later phases
(Phase 4D for Mesa, PRIEST in ROS). This assumption is what makes two R1 decisions safe to take:
Property 2's "beyond T_h is unassessed, neither clear nor blocked", and the all-unrealizable fallback
to plain cost (the robot proceeds; the residual conflict is the execution layer's). Stated plainly
because Mesa has NO such layer today: agents are points that may overlap, so in the Mesa baselines a
separation below `min_separation` at execution time is possible and is MEASURED (T9's per-tick
robot–human distance), never avoided. Building Mesa's avoidance, possibly seeded by realization's
output as hints, is TODO-73. The single-decision-path rule is untouched: that layer refines motion;
it never decides whether to wait or which task to run. F1 fixes the rule that layer must implement — robot-responsible
separation: stop when the next motion would violate (a) or (b); standing is always safe — so that
execution and realization obey one definition (TODO-73).
Files: docs only. Later: mesa_sim/ (TODO-73), ros_sim/ (Phase 6)
Reference: R1 decision record, September 2026; T1b (every hold in the fixtures is a hold into the
unassessed tail)

**Projected walks end where the executor stops, not at the target point (T9)**
The executor completes a `move_to` when the body's `at(agent, object)` predicate holds, which Mesa
emits within `PROXIMITY_THRESHOLD` (30 cm) of the target — the robot stops there, on the last discrete
step that lands inside the radius, and its next action (grasp, release, wait) happens from that
position. Until T9 the projection walked every segment to the exact target point, so projection and
execution disagreed by the stopping distance on every walk and by the accumulated difference over a
plan. DECIDED (R1, September 2026; built in T9): a projected walk ends at the body's STOPPING
DISTANCE from its target, along the straight line, and the following stationary segment and the next
walk start from that point. The stopping distance is SUPPLIED BY THE BODY to the `Projector`, exactly
as the motion rate (`assumed_speed`) already is (T2): `shared/` holds no simulator constant, and its
default is a unit-less placeholder. Mesa supplies the same constant that makes its `at` predicate true,
so projection and completion cannot drift apart by definition; ROS supplies its own. The human's
execution stops short in the same way (same executor, same predicate), so the human's projection
gets the same treatment from the same source. What the projection still does not model: the residual
of at most one step between "exactly the stopping distance" and the discrete step position the
executor actually stops on, and the tick the executor spends acknowledging a completed action.
Measured consequences and the regression record: `analysis/t9_arrival_radius/REPORT.md`.
MEASURED (T9): both agents stop 10–29 cm from every target (the last discrete step inside the
radius). Before the change the robot's full-task placements executed a median 1.25 ticks BEFORE
the projection and the human's a median 1.2 ticks AFTER it — the target-point error (1.5 ticks per
walk, early) was cancelling the executor's acknowledgement ticks (one per completed action, late).
After it, no placement executes ahead of projection: robot −1.5 / −3.3 ticks (after / before the
grasp), human −2.2 / −5.3 — the acknowledgement ticks, step quantization, and the human's one-tick
observation offset, all body facts the projection still does not model (TODO-77). The change
removed the `min_dist = 0.0` placement coincidence T2 had produced: the four T2 exclusions (s20_off
20, s20_on 6, s30_off 28, s30_on 21) no longer fire and item_4 wins there on plain cost, as T1b's
cost argmin predicted; s00, s10, s40 decide identically. `[IR]` lines change only downstream of
those decisions, through world facts (the completion pin), never through projected positions.
Files: shared/projection.py (`Projector.__init__`, `build_segments`), shared/trajectory_algorithms.py
(`arrival_point`), mesa_sim/sim_agents.py (Projector construction), mesa_sim/run_mesa.py (`[sep]`),
analysis/t9_arrival_radius/
Reference: R1 decision record and T9 session, September 2026; T1b "Not measured" (the executor's
actual arrival time vs the projection)

**Projection time includes what the body spends finishing an action, and the human's projection starts when it was observed (L2)**
T9 removed the projection's own error (walks ending at the target rather than at the body's stopping
distance) and by doing so exposed the body's: execution ran BEHIND projection by 1.5 to 3.3 ticks for
the robot and 2.2 to 5.3 for the human (TODO-77). M1 then showed a minimal hold clears with no margin,
so a lag of that size would have made every hold realization computes wrong from the moment it was
computed. Realization is built on the projection, so the projection had to match execution first.

DECIDED (September 2026), two causes, each removed at its source, with the body supplying the constant
exactly as it supplies motion rate and stopping distance — `shared/` learns neither:

ACKNOWLEDGEMENT LATENCY. The executor does not learn an action is finished the instant it finishes: it
sees the completion predicate in the WorldState it is handed on the NEXT tick, advances its cursor and
returns, executing no microaction. One tick per action, and a four-action delivery pays four of them.
`Projector` takes an `action_completion_latency` and charges it once per action as a STATIONARY segment
at the position that action ended at — the agent is standing still, not moving slowly, and that hold is
checked by interference like any other. Mesa supplies
`mesa_sim/executor.ACTION_COMPLETION_LATENCY = 1.0`, which lives in the executor because it is a
property of that loop, the way `PROXIMITY_THRESHOLD` is a property of `world_state_builder`'s `at`. The
`shared/` default is 0.0, a unit-less placeholder for an instantaneous body, and at 0.0 no segment is
emitted, so a bare `Projector` produces exactly the segments it did before. CONSEQUENCE for consumers:
there are now TWO segments per action, not one — read the count off the segments, never off the plan's
actions.

OBSERVATION OFFSET. The two projections were not on the same clock. Mesa's scheduler runs the human
before the robot within a tick, so at the instant the robot decides, the human has already moved and
the robot has not: the robot's projection started from where the robot stood at the end of the previous
tick, the human's from where the human stood at the end of THIS one. Comparing them at a common `t`
compared the robot's position with the human's position one tick later. `Projector` takes an
`observation_offset` and `project_human()` starts the human's projection there instead of at 0. Mesa
supplies `mesa_sim/sim_agents.OBSERVATION_OFFSET = 1.0`, beside the scheduler fact that causes it and
that `observe_initial()` already existed for; ROS would derive it from its own timestamps. The human's
projection then says nothing about [0, offset) — nothing was observed of the human at the robot's now —
and that interval is simply outside its span; interference geometry intersects windows, so no hole
appears anywhere. Not papered over with an invented position.

NOT COMPENSATED, by decision. Step quantisation stays: a walk of projected duration `dur` is executed
as ceil(dur) discrete steps and the walker stops on the first step INSIDE the arrival radius, not on
it. Two effects, both left alone — the walk finishes ceil(dur) − dur ticks late, and the next walk
starts up to one step off the projected start, so it can be a whole step longer. No safety margin is
added anywhere to absorb any of this.

MEASURED (L2, `analysis/l2_execution_lag/REPORT.md`, TODO-77's own terms). The systematic whole-tick lag
is gone: medians move from −1.46/−3.32 to −0.46/−0.32 for the robot (2- and 4-action plans) and from
−2.21/−5.32 to −0.21/−1.32 for the human. What remains is exactly the two things above: a discrete-step
forward model of the executor, using no execution data, predicts the actual release tick EXACTLY for all
68 human and robot 2-action rows, and exactly one tick early for all 35 robot 4-action rows. That last
+1 is not quantisation and is not compensated either: the robot re-plans at its own `task_committed`
trigger, which fires on the tick that would have acknowledged the `pick_up`; the fresh
`deliver_already_held` plan does not contain that `pick_up`, so `continue_plan()` loads from the start
and the carry begins on that very tick. One of the four charged latencies is never spent. Modelling it
would mean the projection predicting the robot's own future triggers, which are decided FROM the
projection — recorded in TODO-77, not fixed.

CONSEQUENCE, and a correction to the expectation this task was set with. "B3 is plain-cost argmin, so
any change comes from durations" is not what the code does: B3 is an argmin over candidates that
`_detect_interference()` has not excluded, and that filter is still live. Across the ten sweep
conditions the latency changed every cost (by one tick per action) and reordered NO candidate set at any
of the 93 triggers compared. The single decision change in the sweep comes from the offset instead:
with the two agents finally in phase, scenario_30's mirror crossing is projected as the near-coincidence
it is (`min_dist` 15.37 → 0.49 cm, the continuous-time minimum of two agents passing through each other
— `[sep]`'s 11.0 cm was the closest integer-tick sample), and the superseded `min_safe_distance = 1.0`
excludes the candidate. Ablation confirms it: latency alone changes no decision, offset alone produces
the whole change. That threshold is already superseded (R1; removed in T10), so the exclusion is a
vestigial mechanism firing on a newly-accurate number, not a new policy.
Files: shared/projection.py (`Projector.__init__`, `build_segments`, `project_human`),
mesa_sim/executor.py (`ACTION_COMPLETION_LATENCY`), mesa_sim/sim_agents.py (`OBSERVATION_OFFSET`,
Projector construction), analysis/l2_execution_lag/
Reference: L2 session, September 2026; TODO-77; T9; M1

**Realization as built: RealizedPlan with a flag, the hold in whole ticks, T_r fractional, the horizon and offset edges (T3, T3b)**
`realize()` exists (`shared/realization.py`, T3) as a standalone service, validated against T1b's
`whole` realizer, and not yet consumed (T4, T10). Its geometry is exact: for one robot segment
against one human segment the set of violating SHIFTS is one open interval (with u the robot's time
into its segment the relative position is affine in (u, d); the violating set is convex and its
intersection with the moments both exist projects onto d as one interval), enumerated in closed form
(`trajectory_algorithms.shift_violation_interval`); the hold-position check is
`first_approach_step`. No sampling in time, none in d. The rulings taken on the T3 report, and the
quantisation decision, are recorded here.

RULINGS (T3b):
- `realize()` RETURNS A `RealizedPlan`, never None: `realizable` is a flag and `reason` says why
  ("realized", "no_human_projection", "hold_position_violated", "hold_reaches_horizon"). The
  `RealizedPlan | None` in the interface sketch above is superseded. An unrealizable plan has no
  `delta`, `cost`, segments or share. SUPERSEDED (F1): the flag and the two unrealizable reasons are
  gone; every plan has `delta`, `cost`, segments and share.
- THE HOLD CAP as implemented: plan start + δ ≥ T_h is unrealizable ("hold_reaches_horizon");
  δ = 0 is never a hold and is never capped, so a plan that starts at or after T_h is realizable and
  fully unassessed. DELETED (F1).
- THE OBSERVATION OFFSET IS UNASSESSED AND NOT IN THE SHARE: the human's projection starts at the
  offset (L2), so the first tick of every plan is outside the assessed window — nothing was observed
  of the human there — and the unassessed share counts only the part of the realized plan beyond T_h,
  the tail a hold pushes past the horizon (TODO-69). The offset is a property of the observation,
  the same for every candidate at a trigger.
- LAYERING WORDING: `MetaPlanner` consumes `realize()` from the projection layer (corrected above).
- A VIOLATION IS STRICT: a single instant at exactly `min_separation` is not a violation. The
  violating shift intervals are open, and their endpoints — where the distance touches
  `min_separation` — are clear. (Unchanged under F1, which adds "the robot is moving and the distance
  is not increasing" to the condition.)

QUANTISATION OF δ AND COST — DECIDED (T3b), from the design, before the evaluation:
δ IS IN WHOLE TICKS. `realize()` returns the smallest whole-tick shift that clears the assessed
window, found by walking the exact violating intervals over the integers (δ starts at 0 and, whenever
an interval strictly contains it, jumps to the first whole tick at or after that interval's end; one
sorted pass suffices since δ never decreases). Reasoning: the hold reaches the body as STAND
microactions, one per tick (T4, TODO-71), so a fractional δ cannot be executed as computed; rounding
at execution is unsafe both ways — down breaks the separation, because the minimal shift has no
margin, and up is not guaranteed to clear, because feasibility in δ is not monotone (a shift can
clear one crossing and walk into the next, so ceil(δ) may sit inside a second violating interval).
With δ whole the plan that is checked and costed is the plan that is executed. The whole-tick δ is
therefore NOT ceil of the fractional minimum — where ceil lands inside a later interval the walk
continues past it. Rejected: fractional δ with the body rounding up (d1), for the reasons above.
T_r STAYS FRACTIONAL. T_r is the projection's continuous duration (the span of the plan's segments);
execution quantises per WALK (each walk runs ceil(dur) steps), and L2 decided not to compensate
that. Rounding the total would be a second quantisation that models nothing — it is neither the
per-walk ceil execution applies nor anything the body does — and, being monotone, it cannot reorder
candidates, only turn an order into a tie resolved by pool order. cost = T_r + δ is then ONE
quantity: the projected duration of the realized trajectory, its hold in whole ticks because the
hold is executed as ticks. CONSEQUENCE FOR T10: the plain cost `update()` compares in the
no-projection path and in the all-unrealizable fallback must be the same T_r —
`RealizedPlan.projected_duration`, the fractional span — not `ProjectedPlan.total_estimated_cost`,
whose integer rounding is a display convenience and would put the fallback in a different quantity
from B3's argmin.
EVALUATED (T3b, `analysis/t3_realize/validation.md`; eight conditions s00/s10/s20/s30 × prior
off/on, s = 50 cm, 94 admitted candidate rows): realizability agrees with T1b's fractional `whole`
in every row; 82 rows are identical and 12 differ only by the rounding, every one of them the ceil
of the fractional δ (no walk continued past a second interval, and no rounding reached T_h or the
hold bound in the fixtures). The rounding costs 0.05–0.87 tick per held row, moves no argmin, and
lifts the held rows' minimum distance from exactly 50 cm to 50.9–55.2 cm — a side effect of
execution's granularity, not a margin. The evaluation is consistent with the reasoning; it did not
decide it.
Files: shared/realization.py, shared/types.py (`RealizedPlan`), shared/trajectory_algorithms.py
(`shift_violation_interval`, `first_approach_step`), shared/io_contracts.md (§1.11, §2.2b, §2.2c),
analysis/t3_realize/
Reference: T3 and T3b sessions, September 2026; R1; T1b (`whole`); L2 (the offset, step quantisation)

**B3 selects on realized cost: the argmin of T_r + δ over the realizable candidates, the winner's hold executed, plain cost when nothing realizes (T10)**
B3.A as decided at R1 is built (T10, September 2026). `_replan_tasks` projects each candidate alone
from the live world at decision step 0 and realizes it — `realize(projection, human_projection,
min_separation, 0)`, the same `min_separation` B2 `b2a` hands in (2.5 × the body's motion per tick) —
and the winner is the argmin of `RealizedPlan.cost` = T_r + δ over the REALIZABLE candidates (ties by
pool order, as before; TODO-42 untouched). The winner's δ goes out as `UpdateResult.hold`, whether the
winner is the current task or another, and Mesa executes it as it executes B2's (T4). No human
projection: every candidate realizes with δ = 0 at T_r, so B3 is an argmin over projected durations.
ALL CANDIDATES UNREALIZABLE (R1, TODO-30 / TODO-52): the argmin of the plain cost — the same fractional
T_r, `RealizedPlan.projected_duration`, never `ProjectedPlan.total_estimated_cost` (T3b) — with no
hold, logged `[meta-b3] ... selection=all_unrealizable`; the `RuntimeError` is gone. REMOVED from
selection: `_detect_interference()`, `_cost()`, `min_safe_distance`, the `interference_algorithm`
constructor parameter and the sampler binding in `sim_agents.py` (all superseded at R1). `ConflictPoint`
and `InterferenceAssessment` remain in `shared/types.py` as types only; `discretized_time_sampling`
has no consumer in the run path. A `cost_strategy` run option ("realized", the default; "plain": the
argmin of T_r alone, no human consideration, no hold, no filter) exists for comparison and the T6
ablation; both use the same T_r, so their difference is realization's effect and nothing else. The run
header (`[run]`, TODO-78) names `gate_strategy`, `cost_strategy`, θ, ρ and `min_separation`.

MEASURED (T10; `analysis/t10_b3_realized/comparison.md`; s00/s10/s20/s30 × prior off/on, run to
completion, PYTHONHASHSEED=0; `plain`+`none`, `realized`+`none`, `realized`+`b2a` with ρ = 0.5):
- PLAIN against L2: identical in every condition but s30_on, where at step 21 the superseded
  `min_safe_distance` exclusion no longer fires and item_4 stays selected (the L2 report predicted
  this). Plain is therefore the old B3 minus the vestigial filter, on the fractional T_r.
- REALIZED against PLAIN — realization's effect. s00 (both priors): identical; every δ is 0. s10, s20,
  s30: the same TASK ORDER except s20_on (below), reached later: the holds B2 executed under T4's
  `b2a` are now B3's, at the same triggers with the same δ (s10 29/33/35 → 6, 2, 0; s20_off 20/24/30
  → 7, 3, 1; s20_on 6/30 → 7, 1; s30_off 28/46 → 6, 1), plus s30_on 40/77 → 7, 1, which T4 did not
  have because its old B3 had switched to item_2 at 21. 12 holds, 43 ticks held, 2 interrupted
  (s10_off 29→33 and s20_off 20→24, the remainder re-decided as at T4). Completion slips by the held
  ticks: s10 +6, s20_off +8, s30 +7/+8. ONE all-unrealizable event, s30_on 21 (the mirror crossing,
  both candidates `hold_position_violated`): the fallback keeps item_4 on plain cost, which is what
  plain does too; its residual conflict is the 0.00 cm pass-through at tick 23, inside that window.
- REALIZED, `none` against `b2a`: IDENTICAL decision sequences, greps and holds in all eight
  conditions. B2 continued exactly where B3 keeps the current task, and both escalations reach a B3
  that decides as it would have without the gate. On these fixtures at ρ = 0.5 `b2a` is a computation
  saving (one realization per trigger instead of one per candidate) and nothing else (TODO-36).
- s40 (regression sweep only, `realized`+`none`): byte-identical to L2 on every grep — no δ > 0.
- ACTUAL SEPARATION (TODO-79, `dist` and the continuous `min`): every moment below 50 cm is past T_h,
  under no projection, after the robot finished, or inside the s30_on fallback's window, EXCEPT s10
  tick 75 at 49.15 cm (both priors, both realized configurations) — TODO-77's step-quantisation
  residual, inside the step-35 decision's window by 0.29 tick. The continuous minimum lowers the
  crossing minima (s30 tick 23: 11.03 → 0.00; s20_off crossing: 11.64 at tick 51 → 9.02 over tick 52) and extends episodes by
  one tick; it moves nothing from outside to inside.

FINDING (RESOLVED by F1, "Robot-responsible separation", which redefined the violation; the mechanism
below is corrected there: it was the robot's stationary placement, not its walk, that the joint-state
rule counted), recorded at T10: s20_on, step 57 (`theta_crossed`, the human's next
task admitted). The robot is carrying item_4, 3.95 projected ticks from placing it. The human has just
placed at the table and is walking away, and at the trigger stands 37.5 cm from the robot — already
inside `min_separation`. item_4's plan converges on the departing human at δ = 0 and its hold position
is violated at step 1, so it is UNREALIZABLE; item_6's plan (return item_4 to its shelf first, then
fetch item_6 — six actions) walks away from the human and realizes at δ = 0, cost 84.65. B3 selects
item_6. Under plain the robot had delivered item_4 at 54 (no holds earlier); under realized the
step-6 and step-30 holds placed the robot's arrival exactly where the human departs. Consequence:
completion 292 vs 228 ticks (+64), item_4 delivered third instead of first, and the human passed the
robot anyway (56–57: 35.1 cm, past T_h). Mechanism: realizability is a HARD GATE inside B3 whenever
some candidate realizes — the argmin ranges over realizable candidates only, so an unrealizable
candidate cannot win however short its plan — and `hold_position_violated` fires here not on a
projected conflict but on the PRESENT state (the human already within `min_separation` of where the
robot stands), which no hold can change and which afflicts every candidate whose first step converges.
This is the over-reaction the wait revision set out to remove, returning through the realizability
flag: switching cost 64 ticks to avoid a 4-tick completion whose "conflict" was the human leaving.
The design as decided says this is what B3 does (the all-unrealizable fallback covers only the case
where NOTHING realizes), so it was built as decided and is reported here. Where it belongs: T6 (the
ablation will show it as the largest realized-vs-plain difference) and D2 / the R1 follow-up — whether
an unrealizable current task a few ticks from completion should compete on plain cost, whether a
present-state violation is a realization question at all, or whether this is `min_separation`'s value
(TODO-28) at the table. Nothing here was tuned.
Files: shared/meta_planner.py (`_replan_tasks`, constructor, properties), shared/types.py
(`UpdateResult.hold` doc), mesa_sim/sim_agents.py (`[run]`, MetaPlanner construction),
mesa_sim/sim_model.py, mesa_sim/run_mesa.py (`--cost_strategy`, `[sep] min=`),
configs/experiment.yaml, shared/io_contracts.md (§1.9, §2.2, §2.2b, §2.2c, §4.1, §6),
analysis/t10_b3_realized/
Reference: T10 session, September 2026; R1; T3b; T4 (`analysis/t4_b2a/comparison.md`)

**Robot-responsible separation: min_separation binds the robot's motion, realization is total, and the body's task-completion tick is projected (F1)**
T10's s20_on step 57 showed realization was not total: with the human already within `min_separation`
at the decision, a standing robot was in violation, so a task 3.95 ticks from done was excluded and
B3 switched to one costing 84.65. Together with the hold cap and the all-unrealizable fallback, the
`realizable` flag was a hard exclusion threshold at `min_separation`, the very thing "The robot can
wait" said the design had none of. DECIDED (F1, September 2026): the violation is redefined so that
realization always yields a cost.

THE VIOLATION. `min_separation` binds the ROBOT'S MOTION, not the joint state. A violation is either
(a) the robot's motion taking the robot–human distance from at least `min_separation` to below it, or
(b) the robot moving while within `min_separation` without the distance strictly increasing. Standing
still within `min_separation` is never a violation. Moving so that the distance strictly increases is
never a violation. Equivalently, at any moment: the robot is moving, the distance is strictly below
`min_separation`, and its time derivative is ≤ 0 — (a) is the instant after the crossing, (b) the
rest. A stationary robot segment (a hold, a grasp, a latency) therefore never violates.

THE GEOMETRY (`trajectory_algorithms.shift_violation_interval`, rewritten; exact, no sampling). For
one robot segment against one human segment, with u the robot's time into its segment and d the
shift, the relative position X = C + B u − w d is affine in (u, d). "Within min_separation" is the open
set |X|² < s² (an ellipse interior, or a strip), "not strictly increasing" is 2 X·B ≤ 0, a CLOSED
HALF-PLANE in (u, d) (the whole plane when B = 0: equal velocities keep the distance constant, so a
robot moving within s violates throughout), and "both exist" is the parallelogram. Their intersection
is convex, so its projection onto d is still ONE interval, whose endpoints lie at a vertex of the
polygon (parallelogram clipped by the half-plane, at most five vertices) inside the disc, a root of
|X|² = s² along one of its edges, or the ellipse's own d-extremum inside the polygon. All enumerated;
the smallest whole-tick δ outside every interval is read off exactly as before. Every interval is
bounded, so a clearing δ ALWAYS EXISTS.

DELETED. The hold-position check (`first_approach_step`, Property 1's "the hold is checked like any
other segment"): a standing robot is never in violation. The hold cap ("a hold may not extend to T_h"):
holding is always admissible, and a hold past T_h leaves the plan in the unassessed tail exactly as any
plan starting after T_h — this SUPERSEDES the T_h cap ruling (R1, T3b) and makes the design consistent
with TODO-69's accepted tail. `RealizedPlan.realizable` and the reasons `hold_position_violated` /
`hold_reaches_horizon`: `realize()` returns a cost always, `reason` ∈ {realized, no_human_projection}.
B3's all-unrealizable fallback and its `all_unrealizable` log (R1, TODO-30, built T10): there is no
unrealizable candidate. B2 `b2a`'s escalate-on-unrealizable branch: it escalates only when δ > ρ ×
(T_h − now). The single-task argmin ranges over EVERY candidate on one quantity, T_r + δ.

STANCE, recorded: a standing robot may be in the human's way; the human's detour around it is a
team-level cost (TODO-15), not priced by realization, which prices only the robot's own time. This
same rule — stop when your next motion would violate (a) or (b); standing is always safe — is the one
Mesa's execution-time avoidance must use when it is built (TODO-73), so that the plan realization
checks and the behaviour execution produces obey one definition.

CONSEQUENCE FOR MESA AND FOR EVALUATION. The Mesa human has no avoidance of its own: it walks its
scripted straight line whatever the robot does. So while the robot stands, the two agents can come
arbitrarily close or overlap (agents are points), and such moments are NOT robot violations under
F1 — they are the human's detour that Mesa does not model (point 1 above). Evaluation of actual
separation therefore counts as a ROBOT VIOLATION only a moment that breaks rule (a) or (b): the robot
moved and the distance fell below `min_separation` or failed to increase within it. Moments where the
robot stands and the human closes are reported separately ("stand"), as are moments where the robot
moves away ("recede"); neither is a failure. The reference classification is
`analysis/f1_robot_responsible/evaluate.py` (labels viol | stand | recede, each also placed inside or
outside the assessed window of the decision in effect).

GROUNDING (documentation of correspondence, not a claim of validation). Two established notions share
F1's stance.
- Passive motion safety (Fraichard and colleagues): a robot is held responsible for a collision only
  if the collision happens while the robot is moving; a robot at rest when contact occurs is passively
  safe. F1's "standing still within min_separation is never a violation" is this notion.
  T. Fraichard, "A Short Paper About Motion Safety", IEEE ICRA 2007 (the motion safety criteria);
  S. Bouraine, T. Fraichard, H. Salhi, "Provably safe navigation for mobile robots with limited
  field-of-views in dynamic environments", Autonomous Robots 32(3), 2012 (passive motion safety).
  Bibliographic details as supplied by Hadi; not independently verified in this session.
- Speed and separation monitoring, ISO/TS 15066:2016 (collaborative robots, with ISO 10218-1/-2): the
  robot maintains a protective separation distance from the human and stops when it would be
  violated; stopping is the safe state. F1 shares the stance that separation is a constraint on the
  robot's motion and that holding is always admissible.
Scope of the correspondence: F1 is a planning-level rule applied to projected trajectories, not a
certified safety function; neither reference validates F1. F1's clause allowing motion within
`min_separation` that strictly increases the distance is OUR extension — passive motion safety covers
only being at rest, and whether ISO/TS 15066 permits retreat inside the protective distance is not
established here. And `min_separation` in F1 is a fixed planning constant (2.5 × motion per tick),
whereas ISO/TS 15066's protective separation distance is computed from robot and human speeds,
reaction and stopping times.

THE TASK-COMPLETION TICK. The L2 report left the executor's trailing task-completion tick unmodelled:
after the last action's acknowledgement, `Executor.step()` spends one tick in `_on_task_complete()`
before the next task's first microaction. Measured on the T10 logs, both agents pay it (human: release
54, acknowledgement 55, completion 56, first step 57 in s20_on; robot: release 30, acknowledgement 31,
completion 32, next task's first step 33 in s00_off). DECIDED: the body supplies it as it supplies the
acknowledgement latency — `mesa_sim/executor.TASK_COMPLETION_LATENCY = 1.0`, handed to the
`Projector` as `task_completion_latency` (default 0.0 in `shared/`) — and `Projector.project()` appends
it as a stationary segment at the end of every projected task, robot candidates and the human's
projection alike. T_h grows by one tick per human task; every candidate's T_r by one, so plain
selection cannot reorder.

MEASURED (F1; `analysis/f1_robot_responsible/`; s00/s10/s20/s30 × prior off/on, run to completion,
PYTHONHASHSEED=0; `plain`+`none`, `realized`+`none`, `realized`+`b2a` at ρ = 0.5):
- VALIDATION (`validation.md`): 101 admitted candidate rows; every realized trajectory sampled at
  0.001 tick over its assessed window has 0 rule (a) and 0 rule (b) violations; for all 12 held rows
  δ − 1 violates (δ minimal); the T10 realizer on the same inputs calls 2 rows unrealizable (s30_on 21,
  both candidates, hold_position_violated) and gives a larger δ in 4 rows (s10: 7 where F1 gives 0)
  and a smaller one in none — F1's violating set is a subset of T10's.
- PLAIN: identical decisions to T10 in every condition (the completion tick shifts every T_r by one).
- REALIZED against PLAIN — realization's effect: s00 and s10 identical (s10's T10 holds are gone: the
  robot arrives at the table first and STANDS while the human comes within 50 cm, which is no longer
  its violation); s20 and s30: the same task order in every condition, reached later by the holds.
- REALIZED, `none` against `b2a`: identical decisions, greps and holds in all eight conditions, as at T10.
- s20_on STEP 57: item_4 (T_r 5.95) realizes with δ = 2 — the robot stands two ticks while the human
  walks off, then places — and wins over item_6 (83.06); completion 239 against T10's 292 and plain's
  228. Attribution: with the realizer alone (before the completion tick) δ was 0 at 57 and completion
  236; the completion tick lengthens the step-6 hold from 7 to 8, so the robot reaches the table one
  tick later and its last walk overlaps the human's departure. The T10 mechanism, corrected: item_4
  was excluded at T10 not because its walk converged on the human but because its stationary
  PLACEMENT stood within 50 cm of the departing human — a standing robot, which the joint-state rule
  counted and the hold-position check then refused to shift.
- s30_on STEP 21 (the mirror crossing, T10's one all-unrealizable event): item_4 realizes with δ = 7,
  item_2 with δ = 4; item_4 wins (61.68 vs 70.45). The robot stands while the human passes it at
  47.8 cm (ticks 22–23, "stand inside": allowed), then walks. Under T10 the fallback ran the robot
  through the human (continuous minimum 0.00 at tick 23). Completion 162 in both.
- HOLDS: 10 started, 36 ticks held, 1 interrupted (s20_off 20 → 24, remainder 4 = 8 − 4), identical in
  both realized configurations: s20_off 20/24/31 → 8, 4, 1; s20_on 6/31/57 → 8, 1, 2; s30_off 28/47 →
  7, 1; s30_on 21/47 → 7, 1. Every T10 hold at s20/s30 grew by one with the completion tick.
- ACTUAL SEPARATION, each sub-50 tick classified by the F1 rule at execution (viol | stand | recede)
  and against the assessed window: NO tick violates rule (a) or (b) inside an assessed window in any
  run. Inside a window there are only "stand" ticks (s10 72–74, the human arriving at the robot's
  placement; s30_on 22–23, the head-on pass). Every "viol" tick is past T_h, under no projection, or
  after the robot finished — the tail (below).
- s40 (regression sweep only): decisions and greps identical to T10.

THE GAP F1 LEAVES OPEN — recorded, no design proposed here. Past T_h the human vanishes from the
assessment, so the robot can approach a human still standing where its projection ended: T10's s20_on
ticks 54–56 (35.1 cm at 56, the human idle at the table two ticks past its projected end) is the
instance; the completion tick covers one of those two ticks, not the other. Every remaining rule
violation in the F1 sweep is of this kind (past T_h or no projection). Under design discussion.
Files: shared/trajectory_algorithms.py (`shift_violation_interval`; `first_approach_step` removed),
shared/realization.py, shared/types.py (`RealizedPlan`), shared/meta_planner.py (B2, B3),
shared/projection.py (`task_completion_latency`), mesa_sim/executor.py (`TASK_COMPLETION_LATENCY`),
mesa_sim/sim_agents.py, shared/io_contracts.md, analysis/f1_robot_responsible/
Reference: F1 session, September 2026; T10 (the s20_on 57 finding); L2 (the unmodelled trailing tick);
R1; T3b

**A continue decision costs nothing: the executor adopts the re-decomposed plan without restarting (T5, TODO-43)**
When `update()` returns the task the robot is already executing — a CONTINUE, decided by
`task_instance_key()` equality between `UpdateResult.current_task` and `ExecutorState.current_task`, never by
object identity and never by a domain string — the robot continues without interruption: no lost tick, no
restart of the action in flight, no observable difference from a tick on which no trigger fired. This is
part of the interface contract between `shared/` and the embodiment (io_contracts.md §1.9, §2.2, §4.1), not
an implementation detail of `sim_agents.py`.

What is NOT changed: "Plans are re-decomposed from scratch, never resumed" (above) stands. The planner still
decomposes the continued task from the live world on every trigger, and the plan it produces may legitimately
differ from the one in flight (the world moved; under realization it will carry different holds). There is
still no plan cursor or resumable plan state in `shared/`. Which task is selected is untouched, and the body
gains no rule about when to re-plan: the decision is made once, in `shared/`; the body executes it.

The distinction is between DECIDING and RE-STARTING. The loss had one cause, in the executor: `_load_plan`
resets the cursor to the fresh plan's first action, and on the tick after an arrival acknowledgement — the
executor has advanced past the completed `move_to` and would grasp or release now — that first action is
the completed `move_to`, so the tick is spent acknowledging it a second time. Mid-walk nothing was lost (the
walk is re-expanded to the same straight path from the current position), and on the acknowledgement tick
itself a reload does what a no-trigger tick does. Measured: no continue in the eight sweep conditions at HEAD
landed on a grasp/release tick (the prior-off triple `theta_crossed` fires inside the HUMAN's grasp stop while
the robot walks), so the sweep lost 0 ticks; the mechanism was isolated with an injected trigger (s00_off 6
and 30, s30_off 47 and 85: one tick lost each before, none after — `analysis/t5_continue/summary.md`). The
scenario_30 cancel-and-return that motivated the task is not in the record at HEAD.

The rule, on the body side (`Executor.continue_plan`): the fresh plan replaces the in-flight one; if the
action in flight appears in the fresh plan (GroundedAction dataclass equality — name, bindings, completion
predicate, schema), the cursor moves to it and the microaction queue and completion bookkeeping are KEPT, so
the tick proceeds exactly as it would have — a step, an acknowledgement, the grasp; a `stand` in progress
keeps its countdown. If it does not appear, the decomposition genuinely changed and the plan loads from its
start, as any new plan does — the `task_committed` continue, where `deliver_already_held` has no `pick_up` to
acknowledge and the carry starts on the trigger tick (one tick earlier than a no-trigger run, pre-existing,
unchanged). The world remains the cursor: what the executor carries across the swap is where it is in the
action it was already doing, never a record of progress the world does not show. Consequence for realization
(TODO-71): a hold that is re-realized on a continue with a different duration is a different action and is
executed as the fresh plan says; a hold re-realized identically keeps its countdown.

Rejected: keeping the in-flight plan on a continue (TODO-43's candidate). It would have made a continue free
too, but the plan the meta-planner priced would then not be the plan executed — the fiction "The robot can
wait" rules out — and a hold computed on a continue would never reach the executor.

Sweep (PYTHONHASHSEED=0, `analysis/t5_continue/`): decisions, `[IR]`/`[IR-dist]` and the robot's per-tick lines
are byte-identical to the T7/T8 baselines in all eight conditions; `[meta-cand] min_dist` differs in the
14th–16th significant digit where the kept queue's step points replace re-interpolated ones on the same
line. These are the meta-planner-side regression baselines from here on.
Files: mesa_sim/executor.py (`continue_plan`), mesa_sim/sim_agents.py (`RobotAgent.step`),
shared/io_contracts.md (§1.9, §2.2, §4.1), analysis/t5_continue/
Reference: T5 session, September 2026; TODO-43
