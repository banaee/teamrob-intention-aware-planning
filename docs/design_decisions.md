# TeamRob Framework — Design Decisions

Key architectural agreements for the Intention-Aware Adaptive Planning Framework.
This is a living reference of *why* things are designed the way they are.

> **Terms:** `docs/glossary.md` gives each term one meaning. The entries below are the HISTORICAL
> RECORD and are left exactly as they were written, so some of them use a term differently from the
> glossary (the conflicts are listed in the glossary task's report). Read an entry in the terms of
> its own date; write new text in the glossary's.

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
avoidance past T_h", below; for Mesa that layer is the separation stop, C).

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
SUPERSEDED IN PART (D3, September 2026): `task_committed` is not a trigger, so re-decomposition after the grasp
is no longer guaranteed on every task; it happens at any re-decision while a task runs (a `recognition_changed`
whose B2 continues, the `continue_plan` 2->0 in the baselines). The requirement on domain authoring stands.

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
  (D3: task-commit is no trigger since September 2026; the triggers are `no_current_task` and
  `recognition_changed`, "D3: task_committed is not a trigger".)
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

REVISED (cchat, September 2026, after T6): `full_reorder` (B3.B) moves from retained alternative to
next in the pipeline. Two-table kitting couples tasks by geometry inside the domain we have, and the
sequence past the head is a lookahead for the choice of the next task, re-priced at the next boundary,
not an order commitment. `single_task` stays the default and the receding-horizon argument above
stands. The three prerequisites this decision named are re-derived there: the fourth bullet above holds
in part (retraction is needed; the general planner semantics are not), the DESIGN-12 bullet's asymmetry
does not arise (nothing is priced past T_h). See "B3.B (`full_reorder`) is lookahead for the choice of
the next task, built next" at the end of this file.

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
SUPERSEDED IN PART (D2, September 2026): `theta_crossed` is replaced by `recognition_changed`, which tracks the
identity of the projected hypothesis against the decision record rather than the crossing of the gate; the
open sub-question (below θ: hold or revert; single threshold or band) is closed as hold, by identity, no band.
`no_current_task` and `task_committed` stand. See "What a trigger is an event of", below.
SUPERSEDED IN PART (D3, September 2026): `task_committed` is removed; `evaluate_triggers()` has two conditions,
`no_current_task` and `recognition_changed`, and `_prev_executor_state` is gone with it. See "D3: task_committed
is not a trigger", below.
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
(below): the robot proceeds and the residual conflict is the execution layer's. The raise was
removed at T10. SUPERSEDED AGAIN (F1): no candidate is unrealizable, so the fallback built at T10 was
removed as well; `update()` never raises and never falls back.
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
better by itself — M1 (`analysis/m1_theta_earlier/` (deleted in the analysis cleanup, September 2026; its numbers are the ones given here)) measured θ = 0.65 on scenario_30 and found
the first crossing moved 21 → 15 prior-on and 28 → 24 prior-off, with no decision change, no
extra trigger and byte-identical behaviour; and offline realization at the moved triggers came
out better in one prior and WORSE in the other, because what decides the outcome is whether the
trigger lands before, during or after the encounter, not how early it is.

Behaviour unchanged: same value, same comparison, all ten sweep conditions byte-identical.
Four analysis scripts still hardcode 0.75 to interpret their own logs
(`analysis/f1_foreseeable_fixture/measure.py` (deleted in the analysis cleanup, September 2026; the folder's REPORT.md stays), `analysis/i3_phase_model/check_i3.py` (deleted in the analysis cleanup, September 2026; the folder's REPORT.md stays),
`analysis/i4_evidence_model/check_i4.py`, `analysis/i4_evidence_model/pivot.py` (deleted in the analysis cleanup, September 2026; the folder's REPORT.md stays)) and are LEFT
hardcoded ON PURPOSE: they are records of runs made at θ = 0.75, and reading a live value would
silently reinterpret those logs if θ later changes or becomes derived. `analysis/i1_ir_audit/
measure.py` (deleted in the analysis cleanup, September 2026; carried in the I2 and I3 entries of design_decisions.md) read the deleted recognizer constant and now carries the same literal for the same
reason. Recording θ in each run's log header would fix this properly (TODO-78) — it changes
logs, so it is not done here.
Files: shared/meta_planner.py (`DEFAULT_THETA`, `_clears_gate`, `evaluate_triggers`,
`update_human_projection`), shared/recognizer.py (constant deleted),
analysis/i1_ir_audit/measure.py (deleted in the analysis cleanup, September 2026; carried in the I2 and I3 entries of design_decisions.md)
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
likelihood calls per scenario in the I1 audit (`analysis/i1_ir_audit/REPORT.md` (deleted in the analysis cleanup, September 2026; carried in the I2 and I3 entries of design_decisions.md) §3.1). The
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
  condition (`analysis/i3_phase_model/summary.md` (deleted in the analysis cleanup, September 2026; the folder's REPORT.md stays), variant `ungated`).
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
measured from the existing logs before any code (`analysis/i4b_boundary/candidates.py` (deleted in the analysis cleanup, September 2026; carried in design_decisions.md, the I4b / I4c entry, and TODO-55 to TODO-59)): (A) a retirement
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
`_task_boundary`); analysis/i4b_boundary/ (deleted in the analysis cleanup, September 2026; carried in design_decisions.md, the I4b / I4c entry, and TODO-55 to TODO-59), analysis/i4c_episode/
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
AMENDED (T6 wrap-up, September 2026): "a completed current task is neither continued nor a candidate" was
true of B3 only. B1.5 still tested `executor_state.current_task`, so B2 `b2a` was asked about a current task
the pool had just dropped, and continued it (s71_off 108; the robot's next task started two ticks late).
One decision read two owners of one fact — a defect, not an accounting item. REQUIREMENT: `update()` never
continues a task its own pool has dropped as complete. B1.5 treats a current task dropped at pool assembly
as no current task, so B3 decides. Gate none is byte-identical by construction and measured so; five b2a
runs change, each to the none decision at that tick (`analysis/t6_ablation/` README, wrap-up).

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
(`is_complete`), analysis/t7_t8_meta_bugs/ (compare.py, stages.sh, summary.md; the folder is deleted in the
analysis cleanup, September 2026: the numbers above are its record)
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
  within the human's projected horizon. Rarer, and meaningful. SUPERSEDED (F1): nothing is infeasible;
  a clearing δ always exists.
- all-candidates-excluded raises `RuntimeError`: SUPERSEDED — the condition changed meaning and the
  outcome is DECIDED (R1; below): plain-cost argmin, logged `all_unrealizable`. Itself SUPERSEDED (F1):
  the condition cannot arise and the fallback is gone.
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
    (as built: unrealizable = RealizedPlan(realizable=False, reason); d in WHOLE ticks — T3b, below;
     SUPERSEDED (F1): the unrealizable branch is gone, d always exists)
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
(D3, September 2026: `task_committed` is no trigger at all now; the ruling stands, and its remaining route is a
`recognition_changed` whose projection is not admitted.)

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
B1.5 — there is nothing to continue). (Since D2 and D3: reached only by `recognition_changed`;
`task_committed` is removed by D3.) B3 = REORDER / SELECTION. Under `single_task` (the only
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
the current task is unrealizable (a branch gone since F1), it escalates to B3. `human_projection is None` still means continue.
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
SINCE R1: built in T3 / T4 / T10; F1 deleted the hold cap, the hold-position check and the
all-unrealizable outcome (realization is total); C built Mesa's execution-time layer (the separation
stop); D2 remains open.
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
SINCE C (September 2026): Mesa HAS that layer — the execution-time separation stop, a run option
(default off, so the earlier baselines stand), applying rule (a)/(b) against the human's actual
position before every STEP; the tail past T_h is left to it, and a stationary s / v tail in the
projection was considered and rejected (the C entry). F47b: with well-typed fixtures the stop fires
only past T_h and on deviations, since every stay the projection carries is priced by realization.
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

MEASURED (L2, `analysis/l2_execution_lag/REPORT.md` (deleted in the analysis cleanup, September 2026; carried in the L2 entry of design_decisions.md and TODO-77), TODO-77's own terms). The systematic whole-tick lag
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
Projector construction), analysis/l2_execution_lag/ (deleted in the analysis cleanup, September 2026; carried in the L2 entry of design_decisions.md and TODO-77)
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
EVALUATED (T3b, `analysis/t3_realize/validation.md` (deleted in the analysis cleanup, September 2026; carried in the T3 / T3b entry of design_decisions.md; realize() is re-validated by analysis/f1_robot_responsible/validate.py); eight conditions s00/s10/s20/s30 × prior
off/on, s = 50 cm, 94 admitted candidate rows): realizability agrees with T1b's fractional `whole`
in every row; 82 rows are identical and 12 differ only by the rounding, every one of them the ceil
of the fractional δ (no walk continued past a second interval, and no rounding reached T_h or the
hold bound in the fixtures). The rounding costs 0.05–0.87 tick per held row, moves no argmin, and
lifts the held rows' minimum distance from exactly 50 cm to 50.9–55.2 cm — a side effect of
execution's granularity, not a margin. The evaluation is consistent with the reasoning; it did not
decide it.
Files: shared/realization.py, shared/types.py (`RealizedPlan`), shared/trajectory_algorithms.py
(`shift_violation_interval`, `first_approach_step`), shared/io_contracts.md (§1.11, §2.2b, §2.2c),
analysis/t3_realize/ (deleted in the analysis cleanup, September 2026; carried in the T3 / T3b entry of design_decisions.md; realize() is re-validated by analysis/f1_robot_responsible/validate.py)
Reference: T3 and T3b sessions, September 2026; R1; T1b (`whole`); L2 (the offset, step quantisation)

**B3 selects on realized cost: the argmin of T_r + δ over the realizable candidates, the winner's hold executed, plain cost when nothing realizes (T10)**
B3.A as decided at R1 is built (T10, September 2026). `_replan_tasks` projects each candidate alone
from the live world at decision step 0 and realizes it — `realize(projection, human_projection,
min_separation, 0)`, the same `min_separation` B2 `b2a` hands in (2.5 × the body's motion per tick) —
and the winner is the argmin of `RealizedPlan.cost` = T_r + δ over the REALIZABLE candidates (ties by
pool order, as before; TODO-42 untouched). The winner's δ goes out as `UpdateResult.hold`, whether the
winner is the current task or another, and Mesa executes it as it executes B2's (T4). No human
projection: every candidate realizes with δ = 0 at T_r, so B3 is an argmin over projected durations.
ALL CANDIDATES UNREALIZABLE (R1, TODO-30 / TODO-52; SUPERSEDED at F1, the fallback removed): the argmin of the plain cost — the same fractional
T_r, `RealizedPlan.projected_duration`, never `ProjectedPlan.total_estimated_cost` (T3b) — with no
hold, logged `[meta-b3] ... selection=all_unrealizable`; the `RuntimeError` is gone. REMOVED from
selection: `_detect_interference()`, `_cost()`, `min_safe_distance`, the `interference_algorithm`
constructor parameter and the sampler binding in `sim_agents.py` (all superseded at R1). `ConflictPoint`
and `InterferenceAssessment` remain in `shared/types.py` as types only; `discretized_time_sampling`
has no consumer in the run path. A `cost_strategy` run option ("realized", the default; "plain": the
argmin of T_r alone, no human consideration, no hold, no filter) exists for comparison and the T6
ablation; both use the same T_r, so their difference is realization's effect and nothing else. The run
header (`[run]`, TODO-78) names `gate_strategy`, `cost_strategy`, θ, ρ and `min_separation`.

MEASURED (T10; `analysis/t10_b3_realized/comparison.md` (deleted in the analysis cleanup, September 2026; carried in the T10 entry of design_decisions.md, TODO-36 and TODO-79); s00/s10/s20/s30 × prior off/on, run to
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
robot anyway (56–57: 35.1 cm, past T_h). RESOLVED (F1, next entry but one: the flag and the
hold-position check are gone; item_4 wins at 57 with δ = 2). Mechanism as it was: realizability is a HARD GATE inside B3 whenever
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
analysis/t10_b3_realized/ (deleted in the analysis cleanup, September 2026; carried in the T10 entry of design_decisions.md, TODO-36 and TODO-79)
Reference: T10 session, September 2026; R1; T3b; T4 (`analysis/t4_b2a/comparison.md` (deleted in the analysis cleanup, September 2026; carried in TODO-36 and TODO-71))

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

MEASURED (F1; `analysis/f1_robot_responsible/` — validation.md, comparison.md; numbers there, not here):
every realized trajectory obeys rules (a) and (b) over its assessed window and every δ is minimal; plain
selection is identical to T10's; realization changes only s20 and s30 (same task order, reached later by
the holds), `none` and `b2a` decide identically; T10's two over-reactions are corrected — s20_on 57 keeps
item_4 with δ = 2 (completion 239 against T10's 292) and s30_on 21 realizes both candidates where T10
had its one all-unrealizable event; no tick violates rule (a) or (b) inside an assessed window in any
run, every remaining violation being in the tail (past T_h or under no projection). The s10 and s40
figures there predate TODO-32 and F47b (`analysis/f47_fixtures/README.md`).

THE GAP F1 LEAVES OPEN — recorded, no design proposed here. Past T_h the human vanishes from the
assessment, so the robot can approach a human still standing where its projection ended: T10's s20_on
ticks 54–56 (35.1 cm at 56, the human idle at the table two ticks past its projected end) is the
instance; the completion tick covers one of those two ticks, not the other. Every remaining rule
violation in the F1 sweep is of this kind (past T_h or no projection). CLOSED for Mesa by C, the
execution-time separation stop (next entry but one): the body refuses the step on the human's actual
position; realization stays unchanged.
Files: shared/trajectory_algorithms.py (`shift_violation_interval`; `first_approach_step` removed),
shared/realization.py, shared/types.py (`RealizedPlan`), shared/meta_planner.py (B2, B3),
shared/projection.py (`task_completion_latency`), mesa_sim/executor.py (`TASK_COMPLETION_LATENCY`),
mesa_sim/sim_agents.py, shared/io_contracts.md, analysis/f1_robot_responsible/
Reference: F1 session, September 2026; T10 (the s20_on 57 finding); L2 (the unmodelled trailing tick);
R1; T3b

**Execution-time separation stop: the Mesa body refuses a step that would break robot-responsible separation against the human's actual position (C; closes F1's gap 2 for Mesa)**
Past T_h realization has no prediction of the human and cannot price the tail (T10's s20_on ticks
54–56: the robot approached a human still standing at the table, 35.1 cm at 56). CONSIDERED AND
REJECTED: a tail of s / v ticks stationary at the human's final projected position. The speed bound
proves only that the human is within a DISC of radius s around that point for s / v ticks; modelling it
as standing at the POINT is a choice that is wrong both when the human stays longer and when it moves
toward the robot, and its length (2.5 ticks) happens to fit Mesa's short task transition — a fixture
fit under a physical-sounding name. Past T_h the robot has observations and no predictions, so the
layer that acts there acts on observations. DECIDED (C, September 2026): the execution-time separation
stop, body side, in `mesa_sim/executor.py`. Realization is unchanged; Property 2 stands.

THE RULE AND THE CHECK. Before executing a STEP microaction the robot checks the step against every
human's ACTUAL position this tick (Mesa's scheduler has already moved the human, so the human stands
at its new position while the robot steps) under the F1 rule: the step is refused if at any point
along it the robot–human distance is below `min_separation` and not strictly increasing. Closed form
(`Executor._separation_blocked`): with the human fixed and the robot on a straight line the distance
is convex in the step parameter t, minimal at t* = clamp(−(r0 − h)·(r1 − r0) / |r1 − r0|², 0, 1),
decreasing before t* and increasing after; the step is clear iff t* = 0 (moving away from the first
instant) or d(t*) ≥ `min_separation` (never within it). Whole step, not endpoint. `min_separation` is
the MetaPlanner's value, the one `realize()` uses. A refused step is a STAND this tick and is retried
next tick; the plan cursor and microaction queue are untouched. Only STEP is checked: grasp, release,
stand and the decided hold are stationary and always admissible. ADDITIVE: the stop never shortens or
cancels a decided hold and never advances the plan. No trigger fires on a stop; the Mesa human gets no
avoidance rule. A run option, `separation_stop` (default off, so the F1 baselines stand), named in the
`[run]` header. One `[stop]` line per refusal: tick, robot and human positions, distance, the step's
minimum, the delayed action, and whether the tick lies inside the assessed window of the decision in
effect (inside means the human deviated from its projection) or outside it (past T_h, or no
projection: the tail) — for D2.

TWO SCOPINGS, recorded. (1) T3b's "the plan checked is the plan executed" holds INSIDE the assessed
window; outside it the stop may add stand ticks that no cost priced. (2) The stop is a SAFETY category,
distinct from TODO-71's rule that the executor never decides to wait as a PLANNING choice: it refines
motion against an observed obstacle, decides nothing about whether to wait for planning reasons or
which task to run, and the two do not contradict each other.

THE INDEFINITE-WAIT LIMIT, accepted at the decision and MEASURED here to be the dominant effect on the
fixtures: a robot stopped near a standing human waits until the human leaves; hold-only cannot detour
(Phase 4D). In scenario_00, _20 and _30 the human's LAST scripted task ends at the shared kitting
table and the scripted human then idles there for the rest of the run, 20–30 cm from the table point;
with the 30 cm arrival radius every approach to the table comes within 36–44 cm of it, so the robot's
last delivery is refused every tick until the step cap. With the stop on, only scenario_10 completes
(its human ends elsewhere). Not fixed here and not to be fixed by a special case: it is the accepted
limit meeting two fixture and domain facts — a scripted human that never leaves (a real one would),
and a table modelled as a point with a single arrival radius (TODO-74). For the design claude chat (we call it cchat).

MEASURED (C; `analysis/c_separation_stop/comparison.md`, numbers there): the stop-off runs equal the F1
baselines apart from the `[run]` header; with the stop on no robot STEP in any run breaks the F1 rule
(acceptance 0, against 2–8 violating steps per run with it off, all in the tail); every stop is labelled
outside the assessed window — the two short episodes are the tail doing its job (s20_off 57–58, s30_off
21–24), the four long ones the indefinite wait above; decisions are identical to the stop-off runs until
the first long episode. The s10 rows there predate TODO-32.
Files: mesa_sim/executor.py (`_separation_blocked`, `_log_stop`, `set_assessed_window`, step() 5a),
mesa_sim/sim_agents.py (Executor construction, the window after each decision, `[run]`),
mesa_sim/sim_model.py, mesa_sim/run_mesa.py (`--separation_stop`), configs/experiment.yaml,
shared/io_contracts.md (§4.1), analysis/c_separation_stop/
Reference: C session, September 2026; F1 (the rule; gap 2); TODO-73; TODO-71; TODO-74

**After C: point places, one min_separation for two situations, the indefinite wait as a condition, the body's refusal is no threshold, the stop trigger left to D2, freezing, and what the stop-off baselines can support (R2)**
Recorded (R2, September 2026); no decision changed. Measurements: `analysis/c_separation_stop/blocked.md`.
- POINT PLACES. With arrival radius r and min_separation s, two agents at one place are at most 2r
  apart, so co-use of a place requires s ≤ 2r AND arrival on opposite sides. With s = 50 cm and 2r =
  60 cm co-use is possible only at the rim, and straight-line arrival makes it practically
  unreachable (C: every approach to the table comes within 36–44 cm of the standing human). A
  framework fact about body constants against policy, not a kitting fact; the table as one point is
  TODO-74.
- ONE VALUE, TWO SITUATIONS. One min_separation governs crossing paths in the open and working side by
  side at a shared place; collaborative practice treats these as different modes with different
  clearances. What the single value costs: set for passing, as now, it forbids working side by side at a
  point place; set for working it would thin the clearance on every crossing. Not changed here.
- THE INDEFINITE WAIT at an occupied place is correct behaviour under the rule (a stopped robot has no
  admissible motion; standing is always safe). The human's end state is an EXPERIMENTAL CONDITION:
  "stays at the place" (the current scripts) and "steps aside after its last task" are two conditions to
  be reported side by side; the variant fixture comes with TODO-47's harness, not here. Under the first,
  BLOCKED TIME is the outcome (`blocked.py`): completion is reported only when it happens; otherwise the
  run reports "blocked by an occupying human" with the blocked duration, place and action. Measured on
  the C runs (`analysis/c_separation_stop/blocked.md`): with the stop on, s00, s20 and s30 are blocked at
  the table from their last delivery to the cap, s10 never; human-borne proximity (the robot stands, the
  human within s) is a few ticks per run at most; robot violations 0 in every run.
- NOT AN EXCLUSION THRESHOLD. Marking a task not executable because the body refused its step (a
  candidate for D2) introduces no parameter: it reads a fact of execution, not a comparison against a
  distance. The T10 lesson forbids a tunable threshold inside selection; it does not forbid selection
  reading what the body did.
- OPEN, FOR D2: C's "no trigger fires on a stop" is expected to be reversed. The mind does not know the
  body has stopped (liveness); what event a stop is, and whether an episode length matters, is D2's
  question with the trigger set (TODO-68 / 48 / 54).
- FREEZING. A robot that stops safely and cannot progress is related to the freezing robot problem
  (P. Trautman and A. Krause, "Unfreezing the robot: navigation in dense, interacting crowds", IROS 2010;
  bibliographic details not verified in this session), though that arises from prediction uncertainty in
  a crowd, not an occupied goal; the closer analogue is execution monitoring of a failed precondition
  (the place is occupied). Human cooperation — communication, or a model of the human making room — is
  the principal remedy, recorded for Phase 4D (TODO-15).
- BASELINES WITH THE STOP OFF contain walk-throughs (F1's tail violations: s00 3, s20 6–8, s30 2–5
  violating robot steps per run) and cannot support safety claims. They are decision baselines.
Files: analysis/c_separation_stop/blocked.py, blocked.md; docs/TODOS_AND_DEFERRED.md (15, 28, 47, 73, 74)
Reference: R2 session, September 2026; C; F1

**The human's wait duration in the projection is the schema's, converted by the body (TODO-32, R2)**
FOUND: the duration was already domain knowledge — a constant in the method schema
(`domains/kitting/tasks.py`: `coffee_break_default` binds `?duration` to `PT60S`, `ac_activation_default`
to `PT2S`); scenario scripts carry no durations. The human's executor and the robot's projector
decompose the same schema, so knowledge and behaviour match by construction. TODO-32 was not a script
leak. DECIDED: the projection uses the wait duration bound on the grounded action the planner produced
instead of the action's default cost. The binding is named by a schema field (`ActionSchema.duration_key`,
`"?duration"` on `wait_at`), never by a literal in `shared/`. Converting an ISO-8601 duration to ticks
needs a parser and seconds per tick, both body facts: as with `assumed_speed` and the latencies, the
embodiment hands the `Projector` a `duration_to_steps` callable (Mesa: `action_decomposer.
_parse_duration_to_steps` over `seconds_per_step`, the same function its `STAND*` expansion uses, handed
in, not moved); `shared/` calls it and holds neither the parser nor the constant. Without one the action
falls back to the cost lookup / default cost (a placeholder, as the other defaults are).
ASSUMPTION, recorded: the robot's known duration and the human's actual duration are matched for now.
If a mismatch experiment is ever wanted, the human's instance gets its own duration in the scenario while
the robot keeps reading the schema value; the robot never reads the scenario's. A deviation is handled by
the separation stop and later re-recognition, not by the projection.
MEASURED (regression sweep, cost realized, gate none, stop off and on, PYTHONHASHSEED=0):
- s00, s20, s30: every regression grep and per-tick line byte-identical to the C baselines; the only
  differing lines are the `[planner]` debug repr of the plan, which now prints the new schema field.
- s10: the coffee_break projection at step 123 (`theta_crossed`, both priors) has T_h 34.00 instead of
  5.00 — 30 ticks for `PT60S` in place of the 1-tick default. The human's executed wait spans ticks
  125–155 (30 STAND + the acknowledgement tick), the projection's 30 + 1 latency. `PT2S` is 1 tick before
  and after.
- s40: T_h 14.30 → 43.30 (prior off, step 143) and 22.30 → 51.30 (prior on, step 135) at the coffee_break
  crossing, and 10.30 → 39.30 at step 147 (`no_current_task`, both).
- No decision, hold, `[meta-proj]`, `[IR]`, `[sep]` or per-tick line changes in any condition; only
  `[meta-cand] share` (the unassessed share of T_r) falls at those triggers: the longer wait covers more of
  the robot's plan without touching it, since in these fixtures the robot's candidates never pass the
  coffee machine. With the stop on: s10 no stops before and after; s40 29 blocked ticks (371–399) at the
  table before and after — the same indefinite wait as s00/s20/s30 (the human's last delivery ends at
  the table); s40 was not in C's set.
Files: shared/types.py (`ActionSchema.duration_key`), domains/kitting/actions.py (`wait_at`),
shared/projection.py (`duration_to_steps`, `_stated_duration`), mesa_sim/sim_agents.py, shared/io_contracts.md
Reference: R2 session, September 2026; TODO-32

**Scheduled bindings are typed; a stay the projection carries is absorbed by realization (F47, F47b)**
TYPED BINDINGS. A scheduled or assigned task implies that its bound objects exist in the layout with the types
the schema declares (`TaskSchema.parameter_types`, the table the recognizer enumerates hypotheses from). A
mismatch is a modelling error, not a tradeoff: it says the human executes a task the domain does not describe
(a coffee break in a world without a coffee machine), which the robot can never recognise. DECIDED (F47b,
September 2026): checked at spawn, an error, not a warning — `shared.types.check_task_bindings`, called in
`SimModel._spawn_agents` for every agent's scheduled and assigned tasks (TODO-49 (2), the binding part). It
found two registered fixtures ill-typed: scenario_40 (`ac_activation` at the waypoints wander_0 / wander_1) and
scenario_50 as first built (`coffee_break` at the waypoint rest_0); both were fixed by retyping the targets at
the same coordinates, and scenario_40's baseline was regenerated (`analysis/f47_fixtures/README.md`: same task
order and completion, different recognition ticks). The F47 fixtures scenario_60/61, built on the same
mismatch, are retired. A human behaviour outside the robot's domain knowledge may be a later addition, but it
must be DECLARED as such (TODO-80), never produced by a type mismatch or by repurposing a task.
A STAY THE PROJECTION CARRIES IS ABSORBED. Measured on the natural configuration (env_layout7, scenario_70/71:
a real coffee machine on the robot's route, the human's shelf beside it; F47's control on the retired layout
agrees): `coffee_break` crosses θ two ticks before the human stands, B3 re-decides on the projected 30-tick
wait, and the robot either switches to the alternative (beside: 80.15 against item_1 + hold 32 = 89; no
`[stop]`) or holds 32 ticks (across: 89 against 118) and then meets only the human's departure (3 refused
steps past T_h). No valid fixture produces a mid-run block at an occupied place: realization prices every stay
the projection carries, so the separation stop — and D2's blocked-execution event — is exercised only past
T_h and by deviations from the projection. Consequently the short / long variants of F47 have no valid
instance; what varies between scenario_70 and _71 is which planning response (switch or hold) the projected
stay produces. Not a failure of the fixtures but a fact about the design for D2: the event's domain is the
tail, not the foreseen stay. Fixtures and numbers: `analysis/f47_fixtures/`.
Files: shared/types.py (`check_task_bindings`), mesa_sim/sim_model.py, domains/kitting/env_layout4/5/7.json,
domains/kitting/scenarios.py, domains/kitting/registry.py, analysis/f47_fixtures/
Reference: F47 and F47b sessions, September 2026; TODO-47, TODO-49, TODO-80

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
and 30, s30_off 47 and 85: one tick lost each before, none after — `analysis/t5_continue/summary.md` (deleted in the analysis cleanup, September 2026; carried in TODO-43 and the T5 entry of design_decisions.md)). The
scenario_30 cancel-and-return that motivated the task is not in the record at HEAD.

The rule, on the body side (`Executor.continue_plan`): the fresh plan replaces the in-flight one; if the
action in flight appears in the fresh plan (GroundedAction dataclass equality — name, bindings, completion
predicate, schema), the cursor moves to it and the microaction queue and completion bookkeeping are KEPT, so
the tick proceeds exactly as it would have — a step, an acknowledgement, the grasp; a `stand` in progress
keeps its countdown. If it does not appear, the decomposition genuinely changed and the plan loads from its
start, as any new plan does — the `task_committed` continue (a case removed by D3), where `deliver_already_held` has no `pick_up` to
acknowledge and the carry starts on the trigger tick (one tick earlier than a no-trigger run, pre-existing,
unchanged). The world remains the cursor: what the executor carries across the swap is where it is in the
action it was already doing, never a record of progress the world does not show. Consequence for realization
(TODO-71): a hold that is re-realized on a continue with a different duration is a different action and is
executed as the fresh plan says; a hold re-realized identically keeps its countdown.

Rejected: keeping the in-flight plan on a continue (TODO-43's candidate). It would have made a continue free
too, but the plan the meta-planner priced would then not be the plan executed — the fiction "The robot can
wait" rules out — and a hold computed on a continue would never reach the executor.

Sweep (PYTHONHASHSEED=0, `analysis/t5_continue/` (deleted in the analysis cleanup, September 2026; carried in TODO-43 and the T5 entry of design_decisions.md)): decisions, `[IR]`/`[IR-dist]` and the robot's per-tick lines
are byte-identical to the T7/T8 baselines in all eight conditions; `[meta-cand] min_dist` differs in the
14th–16th significant digit where the kept queue's step points replace re-interpolated ones on the same
line. These are the meta-planner-side regression baselines from here on.
Files: mesa_sim/executor.py (`continue_plan`), mesa_sim/sim_agents.py (`RobotAgent.step`),
shared/io_contracts.md (§1.9, §2.2, §4.1), analysis/t5_continue/ (deleted in the analysis cleanup, September 2026; carried in TODO-43 and the T5 entry of design_decisions.md)
Reference: T5 session, September 2026; TODO-43

**What a trigger is an event of: `recognition_changed` against the decision record replaces `theta_crossed`; the blocked event designed, not built (D2)**
Decided in cchat from ccode's plan-mode reflection (September 2026); built in D2.

A TRIGGER IS A CHANGE IN WHAT `update()` DECIDED ON. The decision rested on a hypothesis (the one it was
projected against) and on the robot's own task state. Re-decide when the belief no longer points at that
hypothesis, or first points at one strongly enough to act on; and when the robot's own task state changes
(`no_current_task`, `task_committed`, unchanged). Three triggers, as DESIGN-07 had; the second replaced.
SUPERSEDED (D3, September 2026): "three triggers, as DESIGN-07 had" no longer holds. The robot's own grasp is
not a change in what the decision rested on, and `task_committed` is removed; the trigger set is
{`recognition_changed`, `no_current_task`}. See "D3: task_committed is not a trigger", below.

THE DECISION RECORD is one field, `MetaPlanner._projected_hypothesis`: `belief.most_likely` on the tick
`update_human_projection()` built a projection, `None` when admission refused (`none(below_theta)`,
`none(no_human)`, `none(unknown)`, `none(unresolved)`) or before any trigger fired. Cleared on a refusal
rather than kept, because nothing was projected, so no decision rests on the old hypothesis; a kept record
would make the trigger fire on every later tick the belief points elsewhere, against a hypothesis no
decision used. Nothing else is read by any trigger: T_h and the hold were needed only for the dropped
expiry event (E2b), and the body keeps its own `(decision tick, T_h)` for the `[stop]` label.

`recognition_changed`: ONE condition read from two sides, never two named triggers. A hypothesis is
recorded and `belief.most_likely` is no longer it — replaced by another (TODO-48), the human's task ended
and the belief re-initialised (the recognizer's `[IR-boundary]` tick), or `unknown` took over after a pin
(TODO-54); or none is recorded and the belief clears `_clears_gate()` on a task hypothesis (`unknown` is
no hypothesis and has no projection; admission refuses it, so nothing enters on it). The gate is asked at
admission, as before, and on the entering side only. RETENTION IS BY IDENTITY: a recorded hypothesis that
dips below θ while staying most likely fires nothing, and keeps its projection until it is replaced, ends,
or the human stops. That consequence is accepted and written down here; a margin or a duration on the dip
would be a second threshold, the fix not to make (DESIGN-07: single threshold, no band). The rule is
justified without fixtures: a trigger on the crossing of a threshold over a noisy scalar chatters in every
scenario; the identity of what the decision rests on does not. The baseline table (plan-mode reflection,
before the build) was used to REJECT the design chat's first wording — "the hypothesis the belief supports
under the gate, or none, differs from the recorded one" — because it fired on every dip and re-crossing,
contradicting its own goal (s20_off 12 fires against 7 today), not to choose the mechanism. TODO-48, TODO-54
and TODO-68 are consequences of the one condition, not cases; no latch, no debounce, no odds gate, no
change to the recognizer or to the contract's event semantics on the recognizer side.

When two conditions hold on one tick the order is `no_current_task`, `recognition_changed`,
`task_committed` — arbitrary, as before; only the reported reason and score differ.
SUPERSEDED (D3, September 2026): two conditions remain; on a shared tick the order is `no_current_task`, then
`recognition_changed`.

THE BLOCKED EVENT is designed, not built (recorded in TODO-80, to be built with it): the separation stop's
refusal of a STEP as a fact in `ExecutorState`, fired once per blocked episode, routed past B2 as
`no_current_task` is, response policy wait now and reconsider as the recorded alternative. Under wait the
trigger cannot change a decision, so it fixes no liveness; with the stop on, every block in the current
fixtures is the human's terminal stay at the table with one task left (R2, `blocked.md`), where neither
policy has anything to choose. The design chat's earlier claim that D2 removes that deadlock is withdrawn.
TODO-77 (the projector's pick_up accounting) stays out of D2: a projector item, not a trigger question.

MEASURED (PYTHONHASHSEED=0; the sweep and the evaluation fixtures, prior off / on; baselines at the
pre-D2 HEAD agree byte-for-byte with F1's and F47b's on the decision grep):
- Fires of the replaced trigger, old `theta_crossed` → new `recognition_changed`: s00 5→4 / 2→4, s10 6→7 /
  4→7, s20 7→4 / 2→4, s30 2→4 / 2→4, s40 5→10 / 5→10, s50 8→6 / 3→6, s70 5→6 / 3→6, s71 5→7 / 3→6. The new
  count is two per human task everywhere (a recognition, then its end) except s71_off, where item_5 enters
  twice (61 and 72): the robot's own `task_committed` at 69 fell inside item_5's dip (0.572), its admission
  refused, the record was cleared, and item_5's next clearing of the gate is a new recognition. A property
  of the rule, stated here: the record is what the LAST decision projected, whichever trigger made it, so
  the guarantee is "no fire while a projection stands", not one fire per hypothesis. Every fire that retracts — admission `none(below_theta)` or
  `none(unknown)` — decided a CONTINUE in all 16 conditions.
- PRIOR-ON: decisions identical modulo the reason string and the added retraction continues in s00, s10,
  s20, s30, s40, s50, s70 (completion 168 / 420 / 239 / 162 / 378 / 237 / 187, unchanged; `[sep]`
  byte-identical). s71_on: the retraction at the human's boundary, step 54, replaces the last tick of the
  32-tick hold placed against the coffee stay that ended on that tick (executed 31, interrupted); the
  robot leaves one tick earlier, completion 204 → 203. Expected under T4's rule that a later decision
  replaces the hold in progress.
- PRIOR-OFF: the repeated crossings no longer decide (s00 113 / 115, s10 33 / 35, s20 and s50 24 / 30 /
  91 / 95, s70 and s71 65); s20 and s50's first hold runs its 8 ticks in one piece instead of 4 + 4
  (interrupted and re-realized at 24). Robot motion identical in s00, s10, s20, s30, s40, s50, s70
  (`[sep]` byte-identical). Completion DECLARED two ticks later in s00, s20, s50 (166 → 168, 235 → 237,
  235 → 237): the old `theta_crossed` on `unknown` at the robot's own last delivery (TODO-54) declared the
  empty pool on that tick; nothing enters on `unknown` now, so `no_current_task` declares it when the
  executor's bookkeeping learns of the completion, two ticks later. The run's behaviour is the same;
  two trailing `[IR]` lines are the only other difference. s71_off: the boundary retraction at 54
  interrupts the hold's last tick as prior-on, the switch to item_3 comes at 108 instead of 111,
  completion 204 → 201.
These are the meta-planner-side regression baselines from here on: `analysis/d2_recognition_trigger/`
(`sweep/` for s00–s40, `fixtures/` for s50 / s70 / s71; logs local, README committed).
Files: shared/meta_planner.py (`evaluate_triggers`, `update_human_projection`, `_projected_hypothesis`),
shared/io_contracts.md (§2.2), CLAUDE.md, docs/roadmap.md, docs/TODOS_AND_DEFERRED.md (48, 54, 68, 80),
docs/recognizer_handback.md (§5 pointer), analysis/d2_recognition_trigger/
Reference: D2 session, September 2026; cchat D2 design; DESIGN-07; TODO-48 / 54 / 68 / 77 / 80; R2


**A stretch's evidence against `unknown` is graded by the share of the expected path it covers (graded evidence)**

THE DEFECT (handback §4, the open design item since I5): a stretch's evidence against `unknown` was L/u
whatever its length. One fitting step moved the odds by 1/u, the same as a completed walk; with one live
hypothesis the gate opened on the human's first step after a boundary (s00_on 81, s20_on 57, s30_on 77,
s10_on 314). The model counted stretches; it did not grade them by how much they revealed.

DECIDED (cchat, September 2026): the grade is the fraction of the hypothesis's expected path that the stretch
covers, read from the world and the planner's expected action as the excess already is, no domain fact in
`shared/`; it enters the stretch's odds against `unknown`, monotone in the grade, equal to L/u when the
stretch covers the whole expected path, no factor at zero (an unwalked stretch stays uninformative); u, β and
θ stay; the fold session's accounting invariant holds and is re-checked; acceptance on the regression five
plus s50 / s70 / s71, prior off and on. The functional shape was ccode's, with its reason.

THE GRADE, as built: f = (C(o, g) − C(p, g)) / C(o, g), the share of the direct cost from the stretch's
origin o to its target g that the agent at p has closed, clipped to [0, 1]; 0 for an empty expected path
(`likelihood_functions.covered_fraction`). At a fold whose closing action's completion predicate holds, f = 1
by that fact: the world says the path is covered, so the grade needs no arrival radius (the body's 30 cm is
not this layer's, and a distance-only grade would leave every arrival at 1 − 30 cm / C(o, g), a value that
differs per layout). An observation with no path — an action without evaluator or target: `pick_up`,
`place`, `wait_at`, an undecomposable hypothesis — is ungraded, one whole observation, as before.

THE FORM: the stretch's likelihood under `unknown` is u^f (`graded_unknown_likelihood`), so its odds are
L / u^f. Two reasons. (1) Log-linear in f: evidence accrues at a constant rate per unit of expected path, and
two stretches covering the halves of one path multiply to the whole, so what a path is worth does not depend
on how the phase machinery segments it (for walks, this is TODO-61 (b)'s "u per unit of evidence", the unit
being the hypothesis's own expected path). (2) L is untouched: refutation by wasted path is charged in full
whatever the grade. A stretch walked away from its target (f = 0) pays L alone, so the grade meters
confirmation only (TODO-61 (a)); the rival's fresh post-grasp stretch, which lifted it by 1/u on its first
step, now lifts nothing (I4d's regress dips, s00_off 114 / s20_off 25, are gone). Rejected: (L/u)^f, which
loses refutation at f = 0 and is not monotone in f when L < u; a linear u_f = 1 − f (1 − u), which back-loads
the walk (its last tenth worth as much as its first nine) and does not compose. Reading: `unknown` now pays u
per whole expected path covered, not per stretch. Its meaning changed (docstring; handback §2); its value did
not, and nothing was swept.

WHERE: `IntentionRecognizer._unknown_likelihood`, the one reader of the grade, asked at the fold (with
`arrived` = the closing action's completion holds, `_completion_holds`) and for the open term; update()'s
structure is otherwise unchanged. The accounting invariant (I4d) is restated with u^f in update()'s docstring
and handback §1.5, and re-checked by an independent accumulator on all sixteen conditions: max |Δ log odds|
7.1e-15 over 12,865 checks (`analysis/g1_graded_evidence/summary.md`); the instrumented logs equal the plain
sweep on every CLAUDE.md grep.

CLOSED FORMS: a lone live task on its first stretch has confidence 1 / (1 + u^f), so θ = 0.75 is reached at
f = ln 3 / ln 10 ≈ 0.48 of the path (a little more with pins); n whole observations still give 1 / (1 + uⁿ).

MEASURED (PYTHONHASHSEED=0, sixteen conditions, gate none, realized, stop off; `check.py`):
- The one-hypothesis reveals moved and follow the walk: s00_on 81 → 95, s20_on 57 → 72, s30_on 77 → 87, s10_on
  314 → 339, s70_on / s71_on ac_switch_0 98 → 120, s50_on coffee 125 → 136; also s10_on item_5 163 → 202 (two
  live) and s40_on item_6 250 → 254. Each crosses at odds 3.1–3.4 against `unknown`: about half the walk.
- The prior-off first-task reveals moved little: s00 39 → 37, s10 29, s20 20, s30 28 → 27, s50 20, s70 / s71
  23 unchanged. The exception is s40, 21 → 30 in both priors (grasp at 60): the longest first walk, where at 21
  item_3 had covered a third of its path and its odds were u^{−0.35} ≈ 2.2, not 10.
- No wrong-task crossing anywhere. The prior-off re-crossings within one recognition mostly go (s00 113 /
  115, s10 33 / 35, s70 / s71 65 / 72); s20 / s50 keep one each (27, 92).
- Meta-planner consequences, reported, not judged: the `recognition_changed` fires move with the reveals in
  every condition; robot motion changes in six (s20_on: the hold decided at 6 is decided at 11, completion
  237 → 235; s30_off 27; s30_on 23; s50_on 11; s70_on 60; s71_off: the switch to item_3 at 108 is gone,
  item_1 runs to completion and item_3 enters by `no_current_task` at 110, completion 199 → 201); `[sep]`
  byte-identical in the other ten.
- THE θ DATA (deferred: whether θ stays a fixed share, becomes a ratio of the top two, or is derived from the
  live set or the layout is decided on this): `analysis/g1_graded_evidence/crossings.md`, every crossing ± 2
  ticks with the top odds against `unknown`, the ratio of the top two and the live-set size. At every walk
  crossing the top odds are 3.1–4.2 whatever the live set (1 to 9 keys); at every arrival crossing about 100
  (the fold at f = 1 times the open no-graded phase); the ratio of the top two runs from 3.3 (s20_off 92) to
  246, and ∞ for a lone task.

NOT BUILT, by scope: no grading of the no-graded-signal phases (`pick_up`, `place`, `wait_at` stay one whole
observation each; the arrival still counts twice), so TODO-61 (b) stays open for them. A consequence to
record, not judged: for two targets on one bearing the grade is a distance term — the nearer target's fraction
grows faster, odds ratio u^{−x (1/d_near − 1/d_far)} after x walked — which is TODO-38's option (a) in
effect, and its risk (a decoy on the true bearing BEFORE the target) now acts mid-walk, not only at the
decoy's arrival fold. No fixture has such a decoy (handback §3.3).

BASELINES from here: `analysis/g1_graded_evidence/sweep/` (sixteen conditions, stop off; logs local, md5s in
the README), replacing D2's. The stop-on baselines (C's, F47's) are pre-grade.

Files: shared/likelihood_functions.py (`covered_fraction`, `graded_unknown_likelihood`, the docstrings),
shared/recognizer.py (`_unknown_likelihood`, `_completion_holds`, `update()`), docs/recognizer_handback.md
(§1.4, §1.5, §1.8, §1.9, §2, §3, §4, §6, §9), docs/TODOS_AND_DEFERRED.md (38, 61), CLAUDE.md,
analysis/g1_graded_evidence/
Reference: graded-evidence session, September 2026; cchat decision; I4d; TODO-61 / 63 / 64 / 65


**The gate stays a fixed share: `_clears_gate` on the normalised belief, θ = 0.75 (the gate ruling)**

DECIDED (cchat, September 2026, on the graded-evidence θ data, `analysis/g1_graded_evidence/crossings.md`):
the admission gate is unchanged. `MetaPlanner._clears_gate(belief)` tests `confidence ≥ θ` on the normalised
share, θ = `DEFAULT_THETA` = 0.75, owned by the meta-planner ("θ has one home"). Nothing in code changed.

THE REASON: the pool-size defect was in the likelihood, not in the gate. Before the grade a stretch's odds
against `unknown` were L/u whatever its length, so a lone task cleared θ on the human's first step and a
larger live set had to be outvoted by observation count: the bar the share set depended on how many rivals
there were. Under graded evidence a walk's odds against `unknown` accrue per unit of expected path (u^{−f}),
and the walk refutes its rivals through L as it goes. The share is then set by the top hypothesis's odds
against `unknown` plus the residual odds of whatever rivals the walk has not yet refuted:
confidence = odds_top / (1 + odds_top + Σ_rivals odds_j). θ on the share therefore means "at least about 3:1
over no model, and more while rivals remain". A crossing that comes later under ambiguity is the intended
behaviour, not a defect of the gate. A lone task clears at f = ln 3 / ln 10 ≈ 0.48 of its expected path
(a little more with pins): a fraction of the path, not a distance, so the bar does not depend on the layout's
scale.

THE DATA it rests on (crossings.md, sixteen conditions): 30 walk crossings, 14 arrival crossings (top odds
about 100, the fold at f = 1 times the open no-graded phase) and two post-arrival re-crossings (s20_off /
s50_off 27 and 92, odds 116–136). Of the walk crossings, 25 sit at top odds 3.1–4.2 against `unknown` with
live sets of 1 to 9 keys (s40_off 30: nine live, odds 3.26); the lone-task crossings at 3.14–3.39, i.e.
f ≈ 0.50–0.53. The other five sit at 5.2–9.4 (s00_off 37, s10_off 245, s10_on 24, s30_off 27, s40_off 265),
each with one rival still live at the crossing (top-two ratio 5.2–12.3): the "more while rivals remain"
term; their live sets (3 to 6 keys) lie inside the first group's range. CORRECTION to the graded-evidence entry
above (and to hand-back §4 as it stood): "at every walk crossing the top odds are 3.1–4.2" holds for 25 of
the 30, not for all of them. The ruling's reasoning is not affected; its "3 to 4" is the floor, not the range.
The lowest top-two ratio at any walk crossing is 5.23 (s00_off 37); the 3.26 of s20_off / s50_off 92 is a
post-arrival re-crossing at odds 116, not a walk.

NOT TAKEN, one reason each:
- a gate on the odds against `unknown`: it drops the rivals' term, so a crossing would ignore a rival the
  walk has not yet refuted;
- the ratio of the top two: infinite for a lone task, and it adds nothing where no rival stays competitive;
- θ derived from the live-set size: the crossing odds are independent of it (above);
- θ derived from layout or world state: the grade already carries the geometry (f is a share of the
  hypothesis's own expected path);
- a rate-of-growth gate: a threshold on the derivative of a noisy quantity.

WHAT REOPENS IT: a walk crossing with a live rival at similar odds (top-two ratio near 1 at the crossing),
where the share and a margin gate would disagree. No current fixture shows it (lowest walk ratio 5.23); it
belongs to the randomised fixtures (TODO-47), not to a fixture built for it.

CLOSES: TODO-64 (θ's reachability as a function of the live set) and TODO-65 (the gate's form). The
rationality-measure alternative to `unknown` (TODO-63) is untouched by this ruling.

Files: docs/design_decisions.md, docs/TODOS_AND_DEFERRED.md (47, 64, 65), docs/recognizer_handback.md (§4, §5,
§6), docs/roadmap.md, shared/io_contracts.md (§2.2 θ paragraph)
Reference: gate ruling, cchat, September 2026; graded-evidence entry; `analysis/g1_graded_evidence/crossings.md`;
TODO-47 / 63 / 64 / 65

**B3.B (`full_reorder`) is lookahead for the choice of the next task, built next: geometry couples tasks in two-table kitting (DESIGN-16 revised)**

DECIDED (cchat, September 2026, on the state after T6): B3.B is designed now and built next in the
pipeline, with two-table kitting layouts and scenarios as its fixtures (later tasks). This entry is the
design record that build follows. Documentation only; nothing in code changed. It revises the "retained
alternative" ruling of "Single-task selection (receding horizon), not queue-wide reordering" (DESIGN-16)
and replaces that entry's three prerequisites.

WHY THE RULING CHANGED.
1. In one-table kitting order barely matters, and that is a property of the layouts, not of the
   framework. Every delivery ends at the one table, so every ordering of the remaining tasks walks
   table → item → table for each task after the first; orderings differ in their first task, which
   single-task selection already chooses. That is why no current fixture separates B3.A from B3.B.
   (How exact this is, measured: "THE ONE-TABLE EXPECTATION" below.)
2. Several stations is a normal kitting layout, and the domain already carries the table as a task
   parameter: `deliver_item(?item, ?kitting_table)`. With two tables and items assigned per table, a
   task's end position depends on its table, so the walking cost of the tasks after it depends on which
   task came first. This is coupling by geometry (DESIGN-16's "travel/setup costs between tasks"),
   present with no human at all, inside the domain we have. No domain change is needed: a second
   object of type `kitting_table` in a layout and scenario bindings that name it.
3. With a human projection admitted, the window from the trigger to T_h can cover the second or third
   task of an ordering when the robot's tasks are short. So B3.B is not "pick the first task with
   lookahead on walking cost": the whole robot sequence (the segments of task 1, then task 2, ...) is
   realized against the ONE human projection, and a conflict, and therefore a hold, can sit in a later
   task of the sequence. This stays inside the current horizon; nothing past T_h is assessed or charged,
   exactly as `realize()` is today.
4. The robot's own boundaries (`task_committed`, `no_current_task`) trigger a re-decision, so the sequence
   past task 1 is a LOOKAHEAD FOR THE CHOICE OF TASK 1, re-priced at the next boundary. It is not a
   commitment to the whole order. Pools are 3 to 5 tasks.
   CORRECTED (D3, September 2026): `task_committed` is not a trigger. The tail is re-priced at the next
   trigger, which is one of two: `no_current_task` (the robot's own boundary, past B2) or
   `recognition_changed` (through B2, which may keep the current task and never reach B3).

WHAT DID NOT CHANGE. `single_task` remains the default, and the receding-horizon argument of DESIGN-16
stands: decisions are re-made from fresh WorldState and belief at every trigger, and no multi-task
schedule is committed to against a forecast that will be better informed at the next trigger. B3.B as
decided here is consistent with that argument, not an exception to it: it changes what the choice of the
next task is priced on (the cheapest sequence that starts with it, instead of the task alone), not how
long the choice binds. This narrows what `full_reorder` means. The earlier text ("the argmin permutation
becomes the entire new queue", "how much of the queue an `update()` call rewrites") described an order
commitment; under point 4 the order past the head carries none. "Candidate" is still the unit the argmin
ranges over, an ordering under `full_reorder` (terminology of DESIGN-16, unchanged).

THE PREREQUISITES, RE-DERIVED FROM THE CODE'S SEAMS. DESIGN-16 named three: TODO-07 (cross-task
WorldState propagation), DESIGN-12 (horizon-projected confidence), a scalable ordering search; "do not
implement piecemeal". Read against the code as it stands:

(a) `Projector.project()` for orderings longer than 1 (`shared/projection.py`; it raises today). What a
    later task's projection READS from the WorldState, by seam:
    - the start position: `build_segments()` reads `world.agent_positions[agent_id]`. For task k+1 this
      must be where task k's segments end (after T9, a point `arrival_radius` short of the table, on the
      side task k approached from);
    - the start step: `start_step` is already a parameter; task k+1 starts where task k's last segment
      (its task-completion latency, F1) ends;
    - method selection: `AdaptivePlanner._select_method()` matches guards against `world.predicates`. In
      kitting the only guards are `holding(?agent, ?item)` (`deliver_already_held`) and
      `holding(?agent, ?other)` + `not_equal` (`deliver_with_return`);
    - movement targets: `target_resolution.object_position()` reads `world.object_locations` (a carried
      object is wherever its holder is) and `world.object_positions`;
    - derived vars: `object_home_container`, `object_zones` (static per scenario for what is read here).
    `ProjectedPlan` already holds one entry per task, and `total_estimated_cost` / the entries'
    `estimated_start_step` chain without a type change.
(b) THE CHAINED ROBOT STATE. Position and step are geometry: they come from the previous entry's
    segments, and no predicate is involved. But position is NOT enough, and this is the part of the
    expected answer that the code contradicts:
    - `task_committed` is a trigger of every task, and at it the live world holds
      `holding(robot, A)` for the current task A. (D3: `task_committed` is no trigger now; the same
      holds at any re-decision while the robot carries A, so the point stands.) In the ordering (A, B),
      A decomposes as
      `deliver_already_held`; if B is then decomposed against the live predicates, the stale
      `holding(robot, A)` selects `deliver_with_return` for B (return A, which is already delivered in
      that hypothetical world) instead of `deliver_default`. So the chained state must RETRACT
      `holding` after a `place`. This is exactly the gap TODO-07 names (`place` declares
      `not_holding(agent, item)` and nothing removes `holding(agent, item)`); it cannot be avoided.
    - `deliver_with_return` itself can only be selected for the FIRST task of a sequence (every robot
      task in the pool ends in `place`, so nothing is held at a later boundary), and the first task is
      decomposed from the live world as today. Its CONSEQUENCE reaches later tasks, though: in the
      ordering (B, A) with A held, B returns A to its home container, and A is then fetched from there.
      `object_position(A)` must then resolve to the container, not through the stale
      `object_locations[A] = robot`, which would put A at the robot's hypothetical position and price
      the fetch walk at zero: a silent mis-estimate, the failure TODO-07's text warns of. So the chained
      state must also carry the location of an object a projected action has moved.
    - Delivered items are not read by any later task of the sequence (each item is delivered once, and
      the pool is filtered for completion once per `update()`, on the live world). Nothing else in the
      robot's decomposition reads the human's state; the human's own projected effects inside the window
      are not applied to the chained state, which is the same limitation `single_task` has today.
    What this needs is therefore a SUCCESSOR STATE: a new, hypothetical `WorldState` value built inside
    one `project()` call from the previous one and the entry just projected, and discarded with the
    call. The live `WorldState` is never stored or mutated (the ephemerality invariant holds). It must
    be derived from schemas, with no predicate or parameter name in `shared/` (the domain-string
    invariant), which rules out a `holding`-specific stopgap. PROPOSAL (not decided; for cchat), the
    smallest form that satisfies the seams above:
      (i)   effects with retraction: `ActionSchema.effects` applied generically to `predicates`, with a
            typed way to say "this effect removes a fact" (a flag on `ConditionSchema`, or separate
            add / delete lists). `place` then deletes `holding(?agent, ?item)`, and the unconsumed
            `not_holding` predicate goes;
      (ii)  the agent's position from the entry's last segment (geometry, no schema needed);
      (iii) object relocation declared on the action schema, as `movement_target_key` declares the
            movement target today: which binding is the moved object and which is its new holder or
            place. The fact has two representations in `WorldState` (`obj_at` / `holding` predicates and
            the `object_locations` / `object_positions` maps the builder derives); the successor must
            keep the one target resolution reads consistent. How that is declared is the open part.
(c) TODO-07: APPLIES IN PART. Needed: the effect application with retraction of (b)(i) and the
    relocation of (b)(iii), for projection only. Not needed: what TODO-07 was filed for, forward
    chaining and precondition checking in the live planner, and any general theory of effects beyond
    what the projected actions declare. The expectation that TODO-07's semantics are "more than this
    case needs" is right about the planner and wrong about retraction: the retraction is needed at the
    most common trigger.
(d) DESIGN-12 (horizon-projected confidence): DOES NOT APPLY. It asked for confidence at a future
    horizon to price tasks further down an ordering. Under point 3 there is one human projection,
    admitted once at the trigger by the live belief through the gate, and later tasks of the sequence
    are realized against that same projection inside [trigger, T_h]; past T_h nothing is assessed
    (`realize()`: "nothing past T_h is assessed or charged"). That is what `single_task` already does
    with one long candidate: in the current baselines a 93-tick candidate is realized against a
    projection ending at 59. B3.B asks nothing new of the belief. DESIGN-12 stays parked for a design
    that would project the human past its current task.
(e) THE SEARCH: brute permutation is acceptable at this pool size. 3 to 5 tasks are 6 to 120 orderings
    per trigger, and triggers are events, not ticks. Orderings that share a prefix share its projection
    and chained state (a tree of 15 / 64 / 325 task projections for 3 / 4 / 5 tasks). DESIGN-16's
    remark stands for larger pools (bounded-depth lookahead, routing formulation, beam search); no depth
    cap is introduced now, since it would be a parameter with nothing in the design to set it.
    Ties: orderings are enumerated in pool order and the first minimum wins, so that on a tie the head is
    the task `single_task`'s rule would pick (TODO-42, unchanged).
(f) `realize()` over a multi-task trajectory: the seam exists. `realize()` flattens "every entry's
    segments, in order; not assumed to be one task" ("The robot can wait", INPUT), and the closed-form
    shift intervals are per segment pair. What it does today with such a plan is ONE δ at the decision
    position; whether that is what B3.B wants is the open point below.
"Do not implement piecemeal" is replaced by an order (PROPOSAL): the successor state and `project()` for
orderings first, checked alone (a length-1 ordering byte-identical; a later entry equal to the same task
projected alone from a world in which the earlier task has really been done); then B3.B on plain cost;
then on realized cost, once the hold placement is decided. This is also the order of the evaluation.

OPEN POINT 1: WHERE A HOLD THAT CLEARS A CONFLICT IN A LATER TASK IS PLACED. Two options:
  (A) one δ at the decision position, the whole sequence shifted, as T4 / `realize()` does today;
  (B) a hold at the boundary before the task it clears: δ_1 at the decision position for task 1 (today's
      realization of task 1, unchanged), δ_2 where task 1 ended (at the table) before task 2 starts, and
      so on. Each is still "a hold where the robot is", on a segment boundary: not a detour (4D) and not
      partway along a segment (TODO-70).
PROPOSAL (not decided): (B), for these reasons.
  - Point 4. Only the head's hold is executed before the next re-decision. Under (A) a conflict in task 2
    makes the robot stand NOW, before task 1, on the strength of a lookahead that is re-priced at the
    next boundary: the executed hold would commit to the order, which point 4 says the order is not.
    Under (B) `UpdateResult.hold` = δ_1 is exactly the hold `single_task` would execute for the same
    head, so B3.A and B3.B differ in WHICH task is chosen and in nothing else, which is also what makes
    the evaluation readable.
  - Cost. The per-boundary minimal shifts are optimal among boundary placements and never cost more than
    (A): with Δ_k the cumulative shift of task k, taking Δ_k = the smallest whole tick ≥ Δ_{k−1} outside
    task k's violating intervals gives, by induction, Δ_k ≤ any feasible non-decreasing sequence's, and
    (A)'s single δ is one such sequence. Task k's violating intervals do not depend on the earlier shifts
    (positions are unchanged; the human's projection is fixed), so this is `realize()`'s one-pass walk,
    once per entry. The cost of an ordering is Σ T_r + Δ_n.
  - A concrete case in the current baselines (an illustration, not a specification): s00_on, the
    `recognition_changed` decision with three candidates: item_7 costs 12.58 with δ = 0, T_h = 59.48,
    and item_6 alone has δ = 8. In (item_7, item_6) a conflict can only lie in item_6; (A) would stand
    the robot before item_7 for it, (B) at the table after item_7, if it is still there from the new
    start.
  AGAINST (B), to be weighed in cchat: the boundary is at a table, where the human converges. A standing
  robot never violates (F1), but it may be in the human's way there more than at the decision position;
  that is the team-level cost of TODO-15, not priced by either option. And (B) changes `RealizedPlan`
  (one `delta` / `hold_position` today) to per-entry holds, where (A) needs no type change.

OPEN POINT 2: WHAT B2 COMMITS TO UNDER B3.B, a task or an order. PROPOSAL (not decided): a task. B2 is a
mid-task commitment gate on the CURRENT task (`b2a`: realize it alone, continue iff δ ≤ ρ × (T_h − now));
under point 4 the order past the head was never committed to, so there is nothing of it to keep, and
`b2a` runs unchanged. Committing to an order would need the order stored as decision state, against the
one-field decision record (D2) and the unordered queue. Consequence to state in the build: `UpdateResult.queue`
is then the winning order's tail, informational only; `_queue` order carries no commitment, as today.

THE ONE-TABLE EXPECTATION, MEASURED. Point 1's "B3.A and B3.B cannot differ on any current fixture" is an
expectation, not an identity. Two mechanisms can separate them on one table:
  - the arrival point (T9): a delivery ends `arrival_radius` (30 cm in Mesa, 1.5 ticks) short of the
    table on the side it approached from, so the next walk's length depends on the previous task by up
    to that scale per boundary;
  - point 3 itself: where T_h reaches past the head, orderings with the same head differ in the
    conflicts of their later tasks. Measured on the graded-evidence baselines
    (`analysis/g1_graded_evidence/sweep/`, the five fixtures, both priors): of the B3 decisions with an
    admitted projection and more than one candidate, T_h exceeds the winner's cost in s00_on (1 of 3:
    12.58 against 59.48), s10_off (2 of 3: 45.81 / 48.29, 37.27 / 67.05) and s10_on (3 of 4: 50.81 /
    53.02, 80.09 / 110.05, 58.27 / 88.05), and in none of s20, s30, s40.
The candidate gaps at those decisions are tens of ticks, so identical choices are still expected; but a
difference there is to be traced to one of the two mechanisms, not presumed a bug. The byte-identity
check is the default run: with `strategy` left at `single_task`, the greps must not move.

THE EVALUATION (B3.A against B3.B, to be run when the build and the fixtures exist):
  1. plain cost first (`cost_strategy` plain: geometry only, no human consideration) on the two-table
     fixtures: does the head differ, and the completion tick (world fact, T6);
  2. then realized cost on the same fixtures, under the hold placement decided from open point 1;
  3. the current one-table fixtures under B3.B, expected identical in choice (above), as the check that
     the lookahead adds nothing where geometry does not couple tasks.
Needed for it and not present today: `strategy` has no run option (`gate_strategy` and `cost_strategy`
do); the build adds one. The fixtures set no parameter and select no value (as T6).
A consequence of two tables to MEASURE on those fixtures, outside B3.B: the recognizer's hypothesis space
is the product over typed parameters, so `deliver_item` has items × tables hypotheses, and the two table
hypotheses of one item share the fetch walk. With the assignment prior off, the belief is expected to
split between them until the carry walk discriminates, which would move the admission of the human
projection later than in one-table layouts. Expected from the code, not measured.

THE FIXTURE SIDE (T-A1, September 2026; T-B1). A kitting layout with a second table on the opposite side
of the room and each item assigned to one table. Example: items 4 and 6 go to the north table, item 7 to
the south table. From the north table item 7 is the far task, so the orderings (4, 6, 7) and (4, 7, 6)
differ in walking cost with no human present: that difference is what single-task selection cannot see,
and it is the first thing the evaluation looks for (plain cost). Hand-built, registered programmatically
(TODO-47 (a), built here as the first part of fixture generation).
ONE DESIGN QUESTION BEFORE THE LAYOUT IS WRITTEN, OPEN: what kind of fact is an item's destination table?
  - A DOMAIN fact: the domain model says where each item goes. One `deliver_item` hypothesis per item; the
    recognizer knows the table from the domain, and the belief is as in one-table kitting.
  - A WORK-ORDER fact: the table is a binding of the task instance, as `?kitting_table` is today. The
    hypothesis space is items × tables; the assignment prior (when on) restricts it to the assigned
    pairs. Expected recognizer effect with the prior off: the two table hypotheses of one item share the
    fetch walk, so the belief splits between them until the carry walk discriminates, and the human
    projection is admitted later than in one-table layouts. Expected from the code, not measured.
The two readings put the same layout to different uses (the first tests ordering with the recognizer as
it behaves now; the second also tests the recognizer on a split it has not met). The choice is cchat's.
RESOLVED (T-B1a, September 2026): a fact of the station, declared in the layout; one hypothesis per item.
See "An item's destination table is a fact of the station". The items × tables consequence above no
longer applies.
Open points 1 and 2 above are settled at design time in T-B2 (the proposals: the hold at the boundary
before the task it clears; B2 commits to a task).
The proposal of (b), (i) to (iii), is decided and built (T-B2a): see "The successor state is derived from what
the action schemas declare: a delete list and a declared relocation".
OPEN POINTS 1 AND 2 ARE DECIDED AND BUILT (T-B Q2, T-B Q3; T-B2c): see "One hold per entry: an ordering is realized
by one minimal-shift search per entry, and B2 commits to the current task". The argument AGAINST (B) recorded
above is carried there and stays unpriced.

Files: docs/design_decisions.md, docs/TODOS_AND_DEFERRED.md (TODO-07, DESIGN-12, DESIGN-16, TODO-47 (f)),
docs/roadmap.md, shared/meta_planner.py (docstring), shared/projection.py (docstring),
shared/io_contracts.md (§2.2 strategy paragraph)
Reference: B3.B design revision, cchat, September 2026; DESIGN-16; "The robot can wait"; "Realization as
built"; `analysis/g1_graded_evidence/sweep/`

---

**`min_separation` is supplied by the body in physical units, not derived in `shared/` from the body's speed (T-A1)**

DECIDED (cchat, September 2026; built in T-A1): `min_separation` is a distance the body supplies in world
units — a required `MetaPlanner(min_separation=...)` argument with no default in `shared/` — instead of the
R1 form, the ratio `min_separation_in_motion_ticks` = 2.5 times the `Projector`'s `assumed_speed`.

WHY. A standard sets a distance. The R1 form made the safety distance a function of the robot's speed, so a
faster or slower body would silently change the clearance the planner keeps; that violates "safety
parameters are set from outside the planner" (T6). The R1 argument for the ratio ("relative to motion, so
that it scales") treated the value as a scale-calibration item; it is not one (TODO-47 (b), TODO-28): it is
set per body, not measured on fixtures and not rescaled with layouts.

AS BUILT. Mesa supplies it from `mesa_sim/mesa_configs.yaml` (`simulation.min_separation: 50`, cm), read by
`action_decomposer._get_min_separation()` beside `step_size` and `seconds_per_step`, with no fallback (a
missing value stops the run rather than running under a value nobody set). The same value reaches
realization (B2 `b2a`, B3) and the Mesa separation stop, as before. The `[run]` header names the value and
its source (as first built, `min_separation=50.00 (source=mesa_configs.yaml simulation.min_separation, cm)`;
since follow-up 2 `min_separation=50.00 min_separation_source=mesa_configs.yaml:simulation.min_separation beta=0.01 beta_source=mesa_configs.yaml:simulation.beta units=cm`, and a run that overrides the value names
its own source, e.g. the T6 wrapper's `env:T6_SEP_CM`: a header that misstated its source would defeat the
reason it is printed). The value is
unchanged, and so is behaviour: the sixteen graded-evidence baselines (`analysis/g1_graded_evidence/sweep/`)
and the stop-on s00 / s30 cells (`analysis/c_separation_stop/stop_on/`) are byte-identical apart from the
`[run]` line.

Files: shared/meta_planner.py, mesa_sim/mesa_configs.yaml, mesa_sim/action_decomposer.py,
mesa_sim/sim_agents.py, shared/io_contracts.md (§2.2), analysis/t6_ablation/run.py (the keyword)
Reference: T-A1, September 2026; TODO-28; R1; T6

---

**The pipeline from T-A: what moved, and why (T-A1)**

DECIDED (cchat, September 2026, after reading the state in `analysis/big_picture/STATUS.md`). The plan from
here is T-A (records) → T-B (B3.B on two tables) → T-C (the human action script) → T-D (robustness in
kitting) → T-E (demonstration) → T-F (evaluation, Phase 5) → T-G (later: a second domain in Mesa, 4D,
ROS); `docs/roadmap.md` holds it. Four decisions shape that order.
1. B2 (`gate_strategy`) IS AN EVALUATION FACTOR, NOT A DESIGN STEP. STATUS.md named "does the commitment
   gate survive?" as the first question for generated fixtures. It is not a question to answer before
   other work: `none` and `b2a` are both built, nothing downstream depends on which one wins, and B3.B
   leaves `b2a` unchanged (it commits to a task). So it is one factor of T-F's factorial, and no step
   re-reads B2 first. TODO-36 closes on this.
2. THE RANDOMISED HARNESS (TODO-47) MOVES TO T-F. It was "the next step" because three questions (B2, the
   gate's reopening condition, the scale of `min_separation` and β) were said to be answerable only there.
   Of these, B2 is a factor (1), the gate's reopening condition (TODO-47 (g)) is a T-F condition, and the
   scale question is gone: `min_separation` is a distance the body supplies ("`min_separation` is supplied
   by the body", above) and β is a physical tolerance ("β is a physical tolerance", below). What was
   genuinely blocking is the ordering fixture, so TODO-47 (f) stays in T-B as hand-built two-table layouts,
   with programmatic registration built there as the first part of fixture generation.
3. THE DEMONSTRATION COMES AFTER T-B, T-C AND T-D. Built now it could show switch and hold (s70 / s71) only.
   After them it shows what the framework claims: a two-table ordering, a change of mind, `unknown` as an
   outcome, as well as switch and hold, plain against realized cost, the stop on, prior off.
4. THE DOCUMENTATION PASS FOR THE PAPER COMES BEFORE THE PAPER, NOT BEFORE THE DEMONSTRATION. The demo is
   an instrument for seeing behaviour, and it needs the viewer, not polished documents; the paper needs
   the record consolidated once the evaluation's content is known.
Reference: T-A1, September 2026; `analysis/big_picture/STATUS.md`; TODO-36; TODO-47

---

**β is a physical tolerance on wasted path, fixed, decided on IR grounds (T-A1)**

DECIDED (cchat, September 2026). β (`BETA` = 0.01 /cm, `shared/likelihood_functions.py`) is the tolerance
of the excess-path likelihood: how much path a human walking toward a target may waste against the direct
path before the evidence turns against that target (an excess of 100 cm gives L ≈ 0.54). It is a physical
quantity about people walking, in length units, and it is fixed. TODO-58 read it as a layout-scale defect
("a layout twice as large needs half the β"); that reading is withdrawn: a metre of detour is a metre in
any room, and a larger layout does not make people stray further per walk. The value is set on IR grounds
(what a walker toward a target plausibly wastes, and the 30 cm arrival slop it must tolerate, I4) and is
not measured, tuned or rescaled on fixtures; it is not part of TODO-47's calibration. What stays open is
what the hand-back already says: the Euclidean path cost is exact only in Mesa, and a real cell needs an
injected path cost (hand-back §3.3).
SUPPLIED BY THE BODY (T-A1 follow-up 2; built). Because β is physical and carries a unit, its number means
something only in the body's units. `shared/` is unit-agnostic: it computes in whatever units the body reports
positions in, and must not hold a value that fixes those units. So β left `shared/likelihood_functions.py`,
by the same reasoning as `min_separation`: `IntentionRecognizer(beta=...)` is required, with no default;
Mesa supplies 0.01 /cm from `mesa_configs.yaml` (`simulation.beta`, no fallback) and the `[run]` header
names value and source. What does not change: one fixed value per embodiment, decided on IR grounds, not a
per-layout quantity, and no fixture may choose it. Behaviour byte-identical at 0.01 on the regression and
evaluation fixtures.
Reference: T-A1, September 2026; TODO-58; I4

---

**The belief is used as a bar, not a magnitude: a limitation, recorded (T-A1)**

RECORDED (cchat, September 2026). "Confidence is a gate, never a magnitude" (DESIGN-07; io_contracts §2.2;
hand-back §3) is a design rule, and it has a cost worth stating: the meta-planner uses the belief only to
decide WHETHER to admit one hypothesis's projection (`_clears_gate`, θ = 0.75), then prices every candidate
against that one projection as if it were certain. So a belief of 0.76 and one of 0.99 on the same task
give the same decision, and a rival hypothesis at 0.2 contributes nothing, even where its projection would
make a candidate's hold much longer. What the rule buys is that no cost carries a probability that the
recognizer does not calibrate (its confidence ceiling rises with the observation count, I4), and that the
decision rests on one hypothesis that can be recorded (D2's decision record). The alternative, selecting on
the expected realized cost over the belief, is a comparison for Phase 5 (TODO-84), not a change: nothing in
the design moves by recording it.
Reference: T-A1, September 2026; DESIGN-07; D2; the gate ruling; TODO-84

---

**The human's scenario is an action script, run on the scenario layer (T-C, recorded in T-A1)**

DECIDED IN DIRECTION (cchat, September 2026); its design is T-C1, its build T-C2. Nothing built.

WHAT CHANGES. Today the human's scenario is a list of tasks, and the human executor loads each task's plan
from the planner and runs it to completion. So the human can only behave as a robot task looks, and the
recognizer is only ever tested against behaviour that exactly matches one of its hypotheses. Under the
change the scenario states a sequence of primitive actions the human performs, in order, and the human
executor runs that sequence: `move_to` a named object or a point (x, y); `pick_up`; `place`; `wait`; `stay`
at a place for a stated number of ticks. A part of a script may still be written as a task, which expands
to its actions, so the existing scenarios stay readable and the regression fixtures are unchanged in
behaviour (the check T-C2 must pass: byte-identical greps).

WHY. It makes expressible what the framework claims to handle and has never met. Three cases, each an
expectation from the design, not a measurement:
  1. CHANGE OF MIND. The human walks toward item_2 and, ten ticks into the walk, turns to the coffee
     machine. Expected: the item_2 hypothesis is refuted by the geometry of its own expected action (the
     excess path grows; no completion pin, so no episode boundary and no re-initialisation);
     `coffee_break` rises; `recognition_changed` fires twice, once for the retraction (most_likely leaves
     the recorded hypothesis) and once for the new recognition (it clears the gate), and the robot
     re-decides twice. Never observed, because no script could produce it.
  2. `unknown` AS THE OUTCOME. The human walks to an empty corner, with no shelf or foreseeable object near
     it. Expected: every hypothesis accumulates excess, their odds against `unknown` fall below 1,
     `unknown` leads; admission refuses (T8: `unknown` is not admitted), so the robot plans with no human
     projection, on plain cost. `unknown` has so far only been refuted, never confirmed, in a live run:
     this is the first test of the constant-`unknown` design (I4, I4d).
  3. THE DECLARED STAY. The human stands at the kitting table for N ticks after a delivery. This is
     TODO-80's declared behaviour outside the robot's domain knowledge, now one script action (`stay`)
     instead of a mechanism. It is T-D's fixture for the blocked case.

THE BOUNDARY. The script lives on the scenario layer: the Mesa human executor and the scenario files. The
recognizer and the meta-planner receive nothing from it; they see the trajectory, as now ("the robot knows
nothing of the human's script"). The recognizer's hypotheses stay task-level. Aligning free actions with
tasks is what the excess-path evidence does, and the script is how that alignment is tested; no
hypothesis is added for a script action.
Reference: T-A1, September 2026; TODO-80; D2; I4; T8

---

**Robustness is tested in kitting, on the script: `unknown` and the blocked case (T-D, recorded in T-A1)**

DECIDED (cchat, September 2026). `unknown` and the blocked case are tested in kitting, now, with T-C's
script vocabulary; they do not wait for a second domain. T-D builds on T-C.

SCENARIOS. A change of mind mid-task; a walk to an empty corner (`unknown` as outcome); a declared stay at
the table (the blocked case). The first two need no new mechanism, only the script; they test what is
built (retraction and re-recognition through `recognition_changed`; `unknown` leading and admission
refusing).

THE BLOCKED EVENT, built as designed in D2 and recorded under TODO-80: the separation stop's refusal of a
STEP becomes a fact in `ExecutorState` (the body reports, it decides nothing); `evaluate_triggers()` fires
once per blocked episode (the first refused tick); `update()` routes it past B2 as `no_current_task` is
routed. The response policy is a pair: WAIT (stand; the decision stands and the robot re-decides at the
next trigger) against RECONSIDER (mark the blocked task not executable now, a mark on the candidate and not
a cost, and select among the others). Under wait the trigger cannot change the decision, so the pair is
built and evaluated together, with the declared stay as the fixture that makes the comparison possible
(F47b found that no task-scripted fixture blocks mid-run: a stay the projection carries is priced).

MEASURE. Blocked time and completion (the world fact, T6), wait against reconsider; and on the other two
scenarios, whether retraction and re-recognition fire as expected and whether `unknown` leads.
Reference: T-A1, September 2026; D2; TODO-80; F47b; C; R2

---

**A stationary human: what a stay means as evidence, and what the robot does when `unknown` leads (T-C, open; recorded in T-A1)**

RECORDED (cchat, September 2026) as an open item of T-C. Both halves are open; they are one behaviour (what a
stay means, and what the robot does about it) and are decided together in T-C's design chat (T-C1).

THE MODEL AS IT IS (from the code).
- The recognizer's evidence is walked path. Each stretch the human walks is compared with the path each
  hypothesis expects, and the excess is what moves the belief. A tick with nothing walked is not an
  observation: the empty-stretch rule (I4c; `_progress_likelihood` returns None for an empty stretch and
  the caller applies no factor). The rule was introduced as a fix: without it a stationary tick counted as
  a full fitting observation for the top hypothesis and pushed it toward certainty while nothing happened.
- Consequence: a human who stops, for any length of time, produces no evidence for or against anything.
  If the human picks up item_2 and stands still for fifty ticks, the belief stays where it was, with
  `deliver_item(item_2)` on top. `unknown` rises only from walked excess, movement that fits no hypothesis.
- On the meta-planner side, when `unknown` is on top admission returns `none(unknown)`: no human projection,
  B3 selects with every candidate realized at δ = 0 (plain cost in effect), and the separation stop is the
  only thing that reads the human's actual position.

WHY IT IS AN ITEM NOW. The human action script (T-C) makes a stay expressible (`stay`, and any pause in a
script), so the question can no longer be left implicit. The empty-stretch rule was correct as a fix. Its
consequence, that duration carries no information about intention, is a simplification of the model, kept
so that the recognizer and the meta-planner could be built and measured.

HALF (a), THE RECOGNIZER: A STAY AS EVIDENCE. Should standing still for N ticks count against the hypothesis
of pursuing a task, and in favour of `unknown`? That is a question about the likelihood model: what a stay of
N ticks looks like under "pursuing task X" against "no model". If it is added, it is a duration term with its
own form and its own reasoning on IR grounds, not a constant to set, and it is a separate item (T-H), not
part of T-C's script work. (The recognizer already notes the channel: "stationarity as evidence AGAINST an
action that predicts movement would be a different observation channel".) Not decided.

HALF (b), THE META-PLANNER: WHAT `update()` DOES WITH `unknown` ON TOP. Today's answer, no projection, was
chosen when `unknown` meant "the recognizer has nothing". A stationary human at a known position is a
different case: the mind knows where the human is even though it cannot say what the human intends.
CANDIDATE, marked as a candidate only: under `unknown`, project the human as stationary at its current
position for a bounded horizon, so that `realize()` prices holds against where the human is instead of
leaving that entirely to the separation stop. Not decided (how the horizon is bounded is part of it).

WHAT STAYS FIXED, whichever way it goes: the recognizer judges nothing (it emits a belief and gates nothing);
the meta-planner owns admission; the separation stop keeps its role for whatever no projection covers.

THE FIXTURE THAT EXPOSES THE CASE (a T-C script): the human picks up an item and stays still mid-carry.
Expected today, from the code, not measured: the belief is frozen with the carried item's delivery on top,
so no trigger fires; the robot's hold was placed against a projection of a MOVING human (the carry walk);
the conflict happens later than realized, where the human actually stands; and the separation stop refuses
the robot's step inside the assessed window. That is also the first fixture in which the stop and
realization overlap: so far, with valid fixtures, the stop fires only past T_h and on deviations (F47b).
Reference: T-A1, September 2026; I4c; T8; D2; C; F47b; TODO-80; TODO-85

---

**An item's destination table is a fact of the station: a layout declaration, determined from the item, not enumerated (T-B1a, the T-B1 fixture question Q1)**

DECIDED (cchat, September 2026), closing the open question of the B3.B entry's FIXTURE SIDE ("what kind of
fact is an item's destination table?"): a fact of the station, not of the work order.

WHAT IT RESTS ON. Where a part goes is a fact of the station, known independently of who carries it. Who
carries it is the work order, and that is what the assignment prior already expresses. With the table as an
enumerated task parameter, the hypothesis space was items × tables, and the two table hypotheses of one item
are indistinguishable during the fetch walk, so neither could clear the gate before the carry walk: a
modelling artefact, not a property of the human's behaviour. Separating the two leaves one `deliver_item`
hypothesis per item, with the table taken from the station.

THE ROUTE INTO shared/, the one the origin container already takes. Each item in a layout declares
`"destination"` next to its `"initial_container"`. The Mesa loader stores it on `SimObject.destination`; the
world-state builder copies it into `WorldState.object_destination` ({item_id: destination_id}, static per
scenario, like `object_home_container`); the planner reads it through the lookup `destination_of`. `shared/`
holds no layout knowledge and no domain string: which object types need a destination, and of which type, is
read from the task schemas (`DomainKnowledgeBase.get_types_with_destination`).

THE PRECEDENCE RULE. `deliver_item`'s `?kitting_table` is resolved from `?item` through `destination_of` when
the task instance does not bind it. When the task instance binds it, the binding is used as given and the
layout does not override it. Only `destination_of` behaves this way; `zone_of` and `home_container_of` always
derive. Reason: the human's `scheduled_tasks` must be able to send an item to a table other than its
designated one (a deviation the robot is meant to notice later), while the robot's own execution and its
hypotheses about the human follow the station. A missing destination at grounding is a modelling error
(`ValueError`), never a world fact to score around (`DecompositionError`): the recognizer must not produce an
ungrounded hypothesis from it.

THE LOAD-TIME CHECKS (mesa_sim/sim_model.py). (1) Every object of a type the domain resolves through
`destination_of` declares a destination, naming an object of the layout of the type the schema declares for
the determined parameter; otherwise an error naming the object and the layout, never a default. (2)
`check_task_bindings` types every bound parameter, the table included. (3) `check_task_destinations`: every
agent's `assigned_tasks`, robot and human, must bind the table the layout designates; a disagreement is an
error naming the task, the item and both tables. `assigned_tasks` on the human side is the reference set the
robot's mind holds, so it must describe the station, not a deviation. The human's `scheduled_tasks` is
deliberately not checked against the layout: it is the script, and the script is where a deviation is
written (its bindings are still typed by (2)).

THE TWO JOBS OF `parameter_types`, SEPARATED (T-B1a follow-up, correction 1). T-B1a first obtained one
hypothesis per item by removing `?kitting_table` from `parameter_types`, which conflated declaring a
parameter's type (which binding validation needs) with defining what the recognizer enumerates, and lost the
type check on a bound table. Now `parameter_types` declares the type of every parameter, and
`TaskSchema.determined_parameters` ({var: (lookup, source var)}) declares, at the task, which parameters are
determined by another parameter and through which lookup. The recognizer enumerates `parameter_types` minus
`determined_parameters`; the planner fills determined parameters before method selection, with the same
lookup code as a method's `derived_vars`. The declaration sits at the task, not inferred by scanning the
methods, because it is a property of the task's parameters (it decides the hypothesis space and binding
validation, which are task-level), and because the reason a parameter is not enumerated should be readable
where the parameter is declared. `MethodSchema.derived_vars` keeps its own role: variables used inside one
method's steps (`deliver_with_return`'s return container), not task parameters.

IDENTITY AND THE PRIOR'S MATCHING (T-B1a follow-up 2). A task instance and a hypothesis are built from
different sources and are deliberately not the same shape. A task instance is written in the scenario and
names the item and the table it goes to. A hypothesis is one of the robot's guesses about the human, built at
construction from the schemas and the layout's objects, never from the human's tasks (with the prior off,
the default, the robot has no work order for the human at all), and it enumerates the item alone. So:
- `task_instance_key` keeps the table: a key is read by people, and a delivery reads as the item and the
  table it goes to. Every kitting scenario states the table in `assigned_tasks` and `scheduled_tasks`.
  (Dropping the table from the key would have bought byte-identity with T-B1a's baselines; a convenience of
  that task, not an argument about identity.)
- With the prior on, an assigned task is matched to a hypothesis on what the two share, the enumerated
  parameters (the task's bindings minus its determined parameters). The table is not compared: what makes a
  stated table right is agreement with the station, established at load by `check_task_destinations`, which
  rejects a disagreeing scenario before the recognizer is built. An earlier attempt matched the two as whole
  strings; with the table restored, every assigned task matched no hypothesis and the prior lost its pool in
  silence (measured, s00 prior on: the belief differed from step 0).
Measured: on the eight one-table fixtures, both priors, the world-level behaviour is unchanged through T-B1a
and both follow-ups; the logs differ only in the key text (`analysis/tb1a_destination/README.md`).

Open consequences, recorded in TODOS_AND_DEFERRED.md: TODO-86 (AgentConfig's key equality blocks a scripted
delivery to another table) and TODO-87 (the task boundary and the pool drop need the designated completion).
Files: domains/kitting/env_layout*.json, domains/kitting/tasks.py, domains/kitting/scenarios.py,
shared/types.py (`WorldState.object_destination`, `TaskSchema.determined_parameters`,
`check_task_destinations`), shared/planner.py (`_resolve_lookups`), shared/recognizer.py
(`build_hypothesis_space`, `_build_admissible_keys`), shared/domain_knowledge.py, mesa_sim/sim_model.py,
mesa_sim/world_state_builder.py
Reference: T-B1a, T-B1a follow-up, T-B1a follow-up 2, September 2026; B3.B design revision (THE FIXTURE
SIDE); `analysis/tb1a_destination/`

---

**The successor state is derived from what the action schemas declare: a delete list and a declared relocation (T-B2a)**

DECIDED (September 2026; built in T-B2a). This settles the part the B3.B entry left as a proposal ((b), (i) to
(iii): "how that is declared is the open part"). WHO DECIDED WHAT: the delete list was ruled in cchat, on the
T-B2a report, with the reasoning given below. The relocation keys were ccode's proposal, made in the T-B2a
build and ACCEPTED AT REVIEW: they follow the `movement_target_key` style, name parameters and no domain
content, and check 5 passed with them.

WHAT IS BUILT. `Projector.project()` accepts an ordering of n tasks and returns one `ProjectedPlan` with n
entries. Entry k+1 starts at the step and the position at which entry k's last segment ends, and is decomposed
against the SUCCESSOR STATE of entry k (`Projector._successor_state()`): a new `WorldState` value built from
the previous one and the entry's grounded actions, in plan order, and dropped when the call returns. It
applies, per action: `ActionSchema.retracts` (the grounded fact is no longer true), then
`ActionSchema.effects` (the grounded fact is true), then the relocation declared by `moved_object_key` /
`moved_to_key` (`object_locations` names the agent or object the moved object is now at; `object_positions`
follows, read at the end of the plan). The agent's position is geometry, the end of the entry's last segment.
No predicate, parameter or task name appears in `shared/`. An ordering of one task builds no successor state.

THE FORM OF A RETRACTION (ruled in cchat): a delete list on `ActionSchema` (`retracts`), not a negation flag on
`ConditionSchema`. A `ConditionSchema` is also a guard, a precondition and a completion; a flag on it would be
declared in those three roles and read in none of them. A delete list exists only where it has a meaning.
`place` retracts `holding(?agent, ?item)`; the added predicate `not_holding`, which nothing consumed and which
left `holding` true (TODO-07), goes from the kitting schemas.

THE FORM OF A RELOCATION (ccode's proposal, accepted at review): two binding keys on `ActionSchema`, as `movement_target_key` declares the movement
target. Where an object is has two representations in a `WorldState`, the `obj_at` predicate and the
`object_locations` / `object_positions` maps target resolution reads. The predicate side is covered by
`effects` / `retracts`; the map side could not be reached from a predicate name without a domain string in
`shared/`, so it is declared. `pick_up` moves `?item` to `?agent`, `place` moves `?item` to `?target`.

THE KITTING SCHEMA EDIT IS PART OF THE REQUIREMENT, not a fix beside it: the successor state is derived from
what the schemas declare, so a schema that does not declare its retraction is what the requirement needs.
Measured on scenario_80 with the schemas as they were: entry 2 of every ordering decomposed as
`deliver_with_return` (the stale `holding`), a moved object stayed where it had been, and in (B, A) with A held
the fetch of A was priced at 0 ticks.

HYPOTHETICAL, AND HOW THAT WAS ESTABLISHED. The `WorldState` passed in is only read: every container that
differs in the successor is a copy, bound to a local name inside `project()`. The `Projector` stores no
`WorldState`, and a `ProjectedPlan` has no field that could carry one. Checked by projecting all 24 orderings
of scenario_80's pool from a real world with nothing held and from the real `task_committed` world: the world
afterwards equals a deep copy taken before, and its containers are the same objects.

CHECKED. Entry 2 of (A, B) equals B projected alone (same actions, segments equal under `==`) from the REAL
world at the robot's own next decision after it delivered A, with only the robot's position set to entry 1's
projected end (step quantisation is decided uncompensated, TODO-77); the same from the real `task_committed`
world (entry 1 `deliver_already_held`, entry 2 `deliver_default`); and (B, A) with A held against a ground
truth set as the executor's release sets it and rebuilt by `build_world_state()` (entry 2 fetches A from its
home container, a 12.79-tick walk). All 24 orderings agree with `analysis/tb1b_two_tables/permutation_costs.py`
to 5.7e-14 (summation order). The 20 baseline logs are whole-file identical.

LEFT UNDECLARED, CORRECTLY (ruled). What no projection seam reads today and the present form cannot state:
`pick_up` does not end `obj_at(item, shelf)` (the shelf is not a parameter of `pick_up`; it needs a wildcard or
a functional fact, which changes the fact representation rather than a schema; TODO-07 carries the measured
consequence and the condition under which it must be resolved); `move_to` does not end the previous
`at(agent, ·)` (same form problem); `waited` is ended by a later action of another kind; `in_zone`,
`object_zones` and `AgentState` are derived by the body and stated by no action; the observed agent's own
projected effects are not applied, as under `single_task`.

RECORDED, NOT FIXED. `ProjectedPlanEntry.estimated_start_step` is an int and truncates a later entry's
fractional start step. Nothing reads it; the segments carry the exact step.
`domains/dock_loading/actions.py` still declares `not_holding` (deferred, untouched).

Files: shared/projection.py (`project`, `_successor_state`), shared/types.py (`ActionSchema.retracts`,
`moved_object_key`, `moved_to_key`), domains/kitting/actions.py (`pick_up`, `place`), shared/io_contracts.md
(§1.7, §3), docs/TODOS_AND_DEFERRED.md (TODO-07, TODO-77)
Reference: T-B2a, September 2026; "B3.B (`full_reorder`) is lookahead for the choice of the next task, built
next", (a) to (c); TODO-07

---

**B3.B on plain cost: the internal queue stays in pool order, and until T-B2c `full_reorder` is a hybrid (T-B2b, T-B2d)**

THE HYBRID ENDED AT T-B2C: orderings are now ranked on their realized cost and the hold sent is the hold before
the first entry of the winning ordering ("One hold per entry", below). The paragraphs "PLAIN COST THROUGH THE
EXISTING MECHANISM", "THE HOLD", "UNTIL T-B2C ..." and the `[meta-head]` line describe the state between T-B2b
and T-B2c and are kept as the record of it (ruled: the entry stays, marked as ended). The queue ruling, the
tie rule, the run option and `[meta-ord]` stand.

DECIDED (cchat rulings on the T-B2b report, September 2026; built in T-B2b / T-B2d).

WHAT IS BUILT. Under `--strategy full_reorder` (a strict run option, default `single_task`, named in the
`[run]` header) B3's candidates are the orderings of the same pool `single_task` ranks, the current task
included when there is one. Each is projected with T-B2a's chained `project()`; the head of the cheapest
becomes `current_task`. Orderings are enumerated in pool order and the first minimum wins, so a tie between
heads goes to the one earlier in the pool, the task `single_task`'s rule would pick (TODO-42 unchanged). No cap
on the pool and no depth limit: nothing in the design sets one. Measured: one B3 call with a pool of four (24
orderings) takes about 6 ms, against about 1 ms under `single_task`.

PLAIN COST THROUGH THE EXISTING MECHANISM (accepted). An ordering costs the sum of its entries' T_r, obtained
as `cost_strategy plain` obtains a task's: `realize(plan, None, ...)`, δ = 0 and cost = the span of the plan's
segments. The entries of a chained ordering are contiguous, so the span is that sum. `realize()` is unchanged.

THE HOLD is the one `single_task` would send for the same head: the head projected alone, as one entry, and
realized against the human projection (`cost_strategy realized`) or none (`plain`). Under one hold per entry
(T-B Q2) the hold before the first entry is exactly that value, so this part already sends what T-B2c will
send, and the robot is never sent out unrealized.

THE INTERNAL QUEUE STAYS IN POOL ORDER; ONLY `UpdateResult.queue` LISTS THE TAIL (accepted, ccode's reasoning).
The pool of the next call is the current task plus the internal queue, in that order, and ties are broken by
pool order. Writing the tail's order into the internal queue would therefore carry the winning ordering into
the next call's tie-breaks: a commitment to the order, which T-B Q3 excluded (B2 commits to the current task;
the tail is lookahead, re-priced at the next robot trigger). So `_replan_orderings()` leaves the internal
queue as `single_task` leaves it, the pool without the head in pool order, and the winning ordering is stored
nowhere. `UpdateResult.queue` lists the tail in the ordering's order, as information only.

UNTIL T-B2C `full_reorder` WITH `cost_strategy realized` IS A HYBRID: orderings are ranked on PLAIN cost under
either `cost_strategy`, and only the head's hold is realized. The `[run]` header does not show this
(`strategy=full_reorder cost_strategy=realized` reads as if orderings were realized); the `[meta-b3]` line
does (`selection=plain`). For that reason NO `full_reorder` BASELINES ARE RECORDED BEFORE T-B2C.

THE LOG (accepted), under `full_reorder` only, `single_task`'s lines unchanged: `[meta-ord]` per possible head,
in pool order (the cheapest ordering that starts with it, its cost, how many orderings start with it);
`[meta-head]`, the chosen head realized alone, with `[meta-cand]`'s fields (the source of the hold; not called
a candidate, since under `full_reorder` a candidate is an ordering); `[meta-b3]` with `selection=plain`, the
winning ordering's cost, the number of orderings as `candidates`, and `ordering=` appended.

CHECKED. The 20 baselines under the default differ from the previous ones in the `[run]` line alone; removing
` strategy=single_task` from it restores each byte for byte. scenario_80, prior off: `single_task` heads 6, 1,
7, 4, completion 261 (world fact); `full_reorder` heads 7, 4, 6, 1, completion 220; at the first call the head
is item_7 from 7 > 4 > 6 > 1 at 221.08, the cheapest ordering of `analysis/tb1b_two_tables/permutation_costs.py`,
and all four per-head costs match its table. scenario_00, both priors: no choice, hold or completion tick
differs from `single_task` (nor from `single_task` on plain cost, the control): a null result, as expected
where geometry does not couple tasks. The full comparison is T-B3.

Files: shared/meta_planner.py (`_replan_tasks`, `_replan_orderings`, `strategy`), mesa_sim/run_mesa.py,
mesa_sim/sim_model.py, mesa_sim/sim_agents.py (`[run]` header), configs/experiment.yaml,
shared/io_contracts.md (§1.7, §2.2), docs/glossary.md, docs/roadmap.md, CLAUDE.md
Reference: T-B2b, T-B2d, September 2026; "B3.B (`full_reorder`) is lookahead for the choice of the next task,
built next"; T-B Q2, T-B Q3

---

**One hold per entry: an ordering is realized by one minimal-shift search per entry, and B2 commits to the current task (T-B Q2, T-B Q3; T-B2c)**

DECIDED (cchat, September 2026: T-B Q2 and T-B Q3, the two open points of the B3.B entry; built in T-B2c). This
completes B3.B and ends the hybrid of T-B2b.

THE QUESTION (T-B Q2). B3.B prices an ordering against the ONE human projection inside [trigger, T_h], and a
conflict can lie in a later entry, not in the first. Which realization defines the ordering's cost? Before
T-B2c `realize()` pooled the violating shift intervals of every segment of every entry and ran one
minimal-shift search, so ONE COMMON SHIFT was applied to all entries (option (A) of the B3.B entry).

DECIDED: ONE MINIMAL-SHIFT SEARCH PER ENTRY (option (B)). In the plan's order, search k ranges over the
violating shift intervals of entry k's own segments, with the cumulative shift of entry k−1 as its lower bound
(0 for the first entry). Its result is the CUMULATIVE SHIFT of entry k; the HOLD before entry k is the
difference of the two (docs/glossary.md keeps the terms apart, and `RealizedPlan` does: `cumulative_shifts`,
`holds`). While it holds before entry k the robot stands where entry k−1 ended, at the decision position for
the first entry; a standing robot never violates (F1; `shift_violation_interval` returns none for a stationary
robot segment), so the stretch needs no check. The cost of a plan is the sum of its entries' T_r plus the
cumulative shift of the last entry. Nothing past T_h is assessed or charged, and the unassessed share keeps its
definition, on the realized end.

WHY: WEAK DOMINANCE, which holds in general and is not drawn from a fixture. Under one common shift the shift
must lie outside the violating intervals of EVERY entry, so a conflict in entry 3 delays entries 1 and 2 as
well, and the shift can be pushed further by an interval of an earlier entry that entry 3's own conflict never
needed. With one search per entry each entry is delayed only as far as it needs, given what it inherits. Entry
k's violating intervals do not depend on the earlier shifts (its positions are unchanged; the human projection
is fixed). By induction, with Δ_k the cumulative shift of entry k: Δ_k is the smallest whole tick ≥ Δ_{k−1}
outside entry k's intervals; the common shift δ is a whole tick outside them too, and δ ≥ Δ_{k−1} by the
induction hypothesis, so Δ_k ≤ δ. For every entry the cumulative shift is no larger than the common shift, and
the ordering's cost is never higher.

THE RELATION TO R1. This is not the per-segment policy R1 rejected. Inside one entry nothing changes: every
segment of the entry receives the same shift, the R1 whole-trajectory minimal shift, applied per entry (the
glossary keeps the policy's name). The only new place for a hold is before the first segment of an entry,
which is a segment boundary where the robot already stands still (the task-completion latency ends there):
not a detour (4D) and not partway along a segment (TODO-70). A plan of ONE entry is one search with lower
bound 0, so `single_task` and B2 `b2a`, which pass one entry, read exactly what they read before: an identity,
and the 20 baselines are byte-identical.

THE ARGUMENT AGAINST, recorded and not answered by this decision. The boundary at which a later hold is taken
is where the previous entry ended: at a table, where the human converges. A standing robot never violates (F1),
but it may be in the human's way there more than at the decision position. That is the team-level cost of
TODO-15 (the human's detour around a standing robot), PRICED BY NEITHER OPTION: not by the common shift, which
stands at the decision position, and not by one hold per entry, which stands at a table. It weighed against
(B) in the B3.B entry and still stands; what reduces its weight is that a hold before a later entry is
lookahead (below): it is priced, and is executed only if the next re-decision places it again as a first hold.
Also noted there: (B) changes `RealizedPlan` from one `delta` to per-entry lists; done as `holds` and
`cumulative_shifts`, with `delta` a read-only property, the hold before the first entry.

WHAT IS SENT, AND WHAT B2 COMMITS TO (T-B Q3). The robot's own triggers re-decide, so the tail of the winning
ordering is lookahead for the choice of the head, not an order commitment. `UpdateResult.hold` is the hold
before the FIRST entry of the winning ordering's RealizedPlan. It equals the head realized alone — search 1
ranges over the first entry's own intervals from 0, and the first entry is the head projected from the live
world — so B3.A and B3.B differ in WHICH task is chosen and in nothing else, and T-B2b's separate realization
of the head (`[meta-head]`) is removed. Holds before later entries are priced and never sent. B2 commits to
the CURRENT TASK: `b2a` is unchanged (it realizes the current task alone; continue iff δ ≤ ρ × (T_h − now));
the winning ordering is not stored, and the internal queue stays in pool order ("B3.B on plain cost: the
internal queue stays in pool order").

AS BUILT. `shared/realization.py`: `realize()` runs the searches and `_realized_segments()` places each
entry at its cumulative shift, with the stationary stretch of each hold where it is taken.
`shared/types.py`: `RealizedPlan.holds`, `.cumulative_shifts`, `.delta` (property). `shared/meta_planner.py`:
`_replan_orderings()` realizes every ordering against the human projection (`cost_strategy realized`) or none
(`plain`) and ranks on `RealizedPlan.cost`. Orderings with a common prefix share no work (accepted at
review, ccode's reasoning): sharing the prefix's
projection would need a successor state that outlives a `project()` call, which T-B2a rules out; measured, one
B3 call with a pool of four costs about 32 ms with an admitted projection (8 ms without; `single_task` about
1 ms), and triggers are events. Log, `full_reorder` only: `[meta-ord]` as in T-B2b; `[meta-win]` for the
winning ordering (`holds` per entry, `shift` the cumulative shift of the last entry, `T_r`, `cost`, `share`);
`[meta-b3]` with `selection` as under `single_task` and `ordering=`.

CHECKED (`analysis/tb2c_per_entry_holds/`, scenario_81, both priors; the B3 calls of the `full_reorder` run and
of the `single_task` run, every ordering of the pool at every call: 402 orderings, 260 against an admitted
projection).
- DOMINANCE: 0 rows where the per-entry cost differs from the common-shift cost (computed in the script only),
  so none where it is higher. A null result, as R1 measured that more places for a hold seldom change the
  total. It is not vacuous: 12 orderings carry a hold, 8 of them before a LATER entry (item_1 after item_6,
  holds [0, 2, 0, 0] and [0, 3, 0, 0]); in those 8 the cost equals the common shift's and the hold is taken
  elsewhere (at the table after entry 1, not at the decision position). All 12 are on the `single_task` run's
  course; under `full_reorder` no ordering priced on scenario_81 carries any hold.
- THE HEAD'S HOLD: the hold before the first entry equals the head realized alone in all 402.
- VALIDITY, by F1's independent method (sampling at 0.001 tick inside [trigger, T_h], rules (a) and (b)): the
  14 winning orderings with an admitted projection and the 8 orderings with a later hold have no violating
  sample; each later hold is minimal (its entry at shift − 1 violates).
- A synthetic two-entry case (literal segments; a check of the code, not a finding): per entry [0, 14], cost
  34; one common shift 24, cost 44; both clear under sampling; entry 2 at shift − 1 violates.
- BEHAVIOUR: scenario_80 and scenario_81, both priors: `single_task` heads 6, 1, 7, 4 (completion 261 and 265
  from the world fact; one 4-tick hold in scenario_81), `full_reorder` heads 7, 4, 6, 1, completion 220, no
  hold. scenario_00, both priors: identical to `single_task`. The executed behaviour under `full_reorder` is
  the same as at T-B2b on these fixtures; the full comparison is T-B3.
- IDENTITY: the 20 baselines byte-identical under the default strategy; `b2a` runs (scenario_20 with executed
  holds, scenario_81; both priors) byte-identical between the commit before and the change.

A FINDING FOR T-B3. On every current fixture no winning ordering under `full_reorder` carries a hold, so
T-B2c changes nothing executed. scenario_81 does not exercise realized cost under `full_reorder`: its conflict
belongs to `single_task`'s course (6, 1, 7, 4), and the course `full_reorder` chooses (7, 4, 6, 1) never meets
the human, so its saving mixes two causes, the order of the tasks and not meeting the human. A fixture for
T-B3b must put a conflict into the orderings `full_reorder` would choose; Hadi designs it (TODO-47,
f-designations).

NOT PART OF THIS DECISION. Entries after the first are projected about one tick late per preceding entry with a
`pick_up` (TODO-77). It is an error in the input to `realize()`, present under `single_task` too, and is not
compensated here; cchat decides it. No `full_reorder` baselines are recorded until Hadi confirms T-B2c.

Files: shared/realization.py, shared/types.py (`RealizedPlan`), shared/meta_planner.py (`_replan_orderings`),
shared/io_contracts.md (§1.11, §2.2, §2.2c), docs/glossary.md, docs/roadmap.md, CLAUDE.md,
analysis/tb2c_per_entry_holds/
Reference: T-B Q2, T-B Q3, T-B2c, September 2026; "B3.B (`full_reorder`) is lookahead for the choice of the
next task, built next" (open points 1 and 2); "The robot can wait" (R1); "Robot-responsible separation" (F1);
TODO-15, TODO-70, TODO-77

---

**A reload never cancels a completion tick the body states: the Mesa executor spends the acknowledgement after the robot's pick_up (T-B Q7)**

THE FAULT. The Mesa body gives the `Projector` one completion latency for every action
(`ACTION_COMPLETION_LATENCY`, one tick, L2) and one for every task (`TASK_COMPLETION_LATENCY`, F1), and did
not spend all of them. On the tick after the robot's grasp a trigger fires, the decision re-decomposes the
task as `deliver_already_held`, and the fresh plan no longer contains the `pick_up`: `continue_plan()` loaded
it from its start and the first step of the carry executed on the tick that would have been the
acknowledgement. The robot's `pick_up` therefore took ONE TICK LESS than the body says it does. The human has
no triggers and spends every tick the body states. Found as TODO-77's residual, measured at T-B2a (item 8)
and T-B2b.

WHY IT WAS FIXED NOW. Under `full_reorder` the error accumulates: `project()` chains the entries of an
ordering, each starting where the previous one ends, so entry k is projected about one tick late per
preceding entry that contains a `pick_up` and its violating shift intervals are evaluated against the human
projection at the wrong time. T-B3 records `full_reorder` baselines; they are recorded once, on the corrected
body.

WHY THE FIX IS THE BODY'S AND NOT THE PROJECTION'S. The framework is simulation-agnostic. The `Projector`
holds no latency of its own; it uses what the embodiment states, and `shared/io_contracts.md` §6 invariant 12
already required that what the embodiment supplies be the ticks its executor ACTUALLY SPENDS. The body stated
a value its own executor did not keep, so the fault was the body's and so is the fix. Teaching the projection
which acknowledgement is not spent was considered and REJECTED: it would need a latency per action and per
agent, it would carry a quirk of one body into the interface of `shared/`, and it is circular — the
projection would have to predict the robot's own future triggers, which are decided FROM the projection
(TODO-77). Nothing in `shared/` changed and `ACTION_COMPLETION_LATENCY` keeps its value.

THE RULE, decided general rather than for the grasp alone. A RELOAD NEVER CANCELS A COMPLETION TICK THE BODY
STATES. Those ticks are the execution loop's, not the plan's: a decision landing on one is a decision, not a
reason for the body to become faster than it says it is. Every path that loads a plan from its start now goes
through `Executor._reload()`, which asks `_owed_completion()` — in the same terms `step()` asks them, the
world it was handed this tick — what the replaced plan is still owed, and hands it to `step()` to spend,
executing nothing, one tick per tick. Three cases, one rule:
  (a) the decision CONTINUES the task and re-decomposes it past the action in flight — the robot's grasp;
  (b) the decision SWITCHES task on the tick an action finished;
  (c) the decision arrives while the finished task's OWN completion tick is still outstanding (a trigger
      landing on the completion tail, which used to cut it short).
The trigger's name does not enter: the post-grasp re-decision is attributed to `recognition_changed` rather
than `task_committed` wherever both fire on the tick (s10_on, s81_off). The trigger fires and the decision is
made on the tick they always were.

THE TWO-TICK CASE. Where the completed action is the plan's LAST one, the body owes TWO ticks — that action's
acknowledgement and the task completion tick after it — and spends both, in that order, before the loaded
plan's first microaction. `_task_completion_spent` keeps the task tick owed ONCE rather than once per reload;
that is what leaves the human's path untouched, since the human's next plan is always loaded the tick after
`_on_task_complete()` ran.

THE HOLD CARRIES AN OWED TICK, IT DOES NOT FOLLOW IT. A hold decided at the same trigger and an owed
completion tick are ONE standing tick, not two: both are the robot standing where the decision found it,
while the body learns what it learns. So the hold's first tick is the owed tick, and the plan resumes at
decision + δ — WHERE REALIZATION PUT IT — instead of a tick later. This is the one thing the ordering had to
preserve: the executed plan equals the plan that was realized. Where two ticks are owed and δ ≥ 2 the hold
carries both, one per tick.

THE RESIDUAL, WITH A HOLD OF 0. When the decision carries no hold there is nothing to carry the owed tick, so
the plan resumes ONE TICK AFTER the start that decision's own projection assumed. It is one tick, on the HEAD
only, at a robot re-decision that reloads (the `task_committed` case in the fixtures), and IT DOES NOT
ACCUMULATE: the tick is spent once, the entry chain of the ordering is now right, and the next decision
projects from where the robot actually is. `shared/` cannot see it without predicting the robot's own
triggers, which is the circularity above. Accepted, recorded, not compensated — the same standing as step
quantisation.
GONE WITH THE TRIGGER (D3, September 2026): the case the fixtures showed, the reload at `task_committed`, no
longer occurs; the residual measured at those decisions is gone with them. The body's rule stands for any other
re-decision that reloads on an owed tick.

WHAT REMAINS UNCOMPENSATED. STEP QUANTISATION only (L2's decision, unchanged): a walk of projected duration
`dur` executes as ceil(dur) steps and the walker stops on the first step inside the arrival radius, so it
finishes late and the next walk may start up to one step off its projected start. Measured per delivery on
scenario_80, executed minus projected, before → after: fetch part −0.89 → +0.11, −0.36 → +0.64, −0.60 → +0.40,
+0.41 → +1.41; carry part unchanged (+0.62, +0.67, +0.92, +0.48); total −0.27 → +0.73, +0.31 → +1.31,
+0.32 → +1.32, +0.89 → +1.89. The executed fetch gains EXACTLY one tick in all four deliveries. Before the
fix three of the four ran SHORTER than projected — the skipped acknowledgement masking quantisation; after
it every residual is positive, which ceil-per-walk alone produces. TODO-77's residual is closed with that.

MEASURED, the 20 baselines (both priors; `analysis/tb1a_destination/`, `analysis/tb1b_two_tables/`).
Completion from the world fact moves by one tick per robot delivery, less where a hold carried the tick:
s00 166 → 169, s10 418 → 422, s20 235 → 237, s30 160 → 161, s40 376 → 379, s50 235 → 237, s70 185 → 186,
s71 201 → 203, s80 261 → 265, s81 265 → 268. The three carried ticks: s20 / s50 and s30, where the post-grasp
decision already held for δ = 1; s70, where the hold at step 61 / 60 re-realized 2 → 1, and s81, where the
hold at step 39 → 40 re-realized 4 → 3 — the robot reaches those decisions one tick later, so one fewer tick
of shift clears the same human, minimal in both. THE DECISION SEQUENCES ARE OTHERWISE UNCHANGED, with two
exceptions, both traced to a trigger that used to land on a cancelled completion tick: s10 (both priors) and
s00_on, where the run now spends it; and one decision that was never separately raised before, s81_off's
`task_committed` at 132, because the grasp and a belief change no longer share a tick. Changed decisions are
explained, never adjusted. The human's lines are byte-identical in all 20 runs, and 17 of the 20 were
byte-identical between the grasp-only fix and the general rule — including the three whose post-grasp hold
carries the acknowledgement, so moving that absorption from `hold()` into `step()` preserves behaviour.

THE ACCEPTANCE CRITERION THAT WAS WRONG, CORRECTED. The task expected every `[IR]` line to be byte-identical,
on the ground that the robot does not touch the human and the recognizer observes the human only. The second
half does not follow: the recognizer reads the `WorldState`, and the robot writes into it (a) a carried
item's position, which IS the carrier's, so while the robot carries item X the hypothesis `deliver_item(X)`
is scored against a target that moves with the ROBOT, and (b) task completion as a WORLD FACT, so the pin
retiring that hypothesis falls on the tick the robot's release makes `obj_at` hold. Measured: with the prior
ON every `[IR]` line is identical (the support is the human's assigned pool and holds none of the robot's
items); with it OFF 1 to 29 steps per run differ, by at most 0.165 in confidence where `most_likely` is
unchanged and by up to 0.497 at the pin ticks. The human's own lines are byte-identical in all 20, so nothing
reaches the OBSERVATION. The criterion as corrected is met. The recognizer question this exposes — with the
prior off, a live hypothesis about the human whose item the robot is carrying away — is
`docs/TODOS_AND_DEFERRED.md`, TODO-88, for cchat; nothing was changed for it.

Files: mesa_sim/executor.py (`_reload`, `_owed_completion`, `step()` 1b, `continue_plan`, `hold`,
`_on_task_complete`), mesa_sim/sim_agents.py (`continue_plan` call), analysis/tb1a_destination/README.md,
analysis/tb1b_two_tables/README.md, analysis/tb2c_per_entry_holds/README.md,
docs/TODOS_AND_DEFERRED.md (TODO-77, TODO-88), CLAUDE.md
Reference: T-B Q7, September 2026; TODO-77 (L2, T4, T-B2a, T-B2b); "Projection time includes what the body
spends finishing an action" (L2); "Robot-responsible separation" (F1, the completion tick); "The robot can
wait" (R1); shared/io_contracts.md §6 invariant 12


**D3: `task_committed` is not a trigger**
RULED (cchat, September 2026). A TRIGGER IS A CHANGE IN WHAT THE LAST DECISION RESTED ON: the human's hypothesis
(`recognition_changed`, against the decision record) or the robot's task set (`no_current_task`). The robot's own
grasp is neither: it was in the plan the last decision priced, which projected the `pick_up` and everything after
it. The trigger set is {`recognition_changed`, `no_current_task`}; on a shared tick the order is
`no_current_task`, then `recognition_changed`, arbitrary as before (only the reported reason and score differ).
No re-timing mechanism is added in its place, and the trigger is deleted, not made optional: the ablation's run
option is discarded.

THE ABLATION it rests on (`analysis/ablation_task_committed/`, 142deaa; on the corrected body, T-B Q7): 26 pairs,
with and without the trigger. Nothing in the world changes in any of them: every `[sep]` line, every human line,
every `[IR] step=` line and completion are byte-identical. The 1-tick holds the trigger placed at the grasp
(s20 at 31, s30 b2a at 47) were the owed acknowledgement tick: without the trigger the robot spends the
`pick_up` acknowledgement there instead, at the same position. No clearance depends on the re-decision (TODO-77's
T4 dependency, stale after T-B Q7), and B2 is still reached, from `recognition_changed` alone.

AS BUILT (dd880be): `evaluate_triggers()` asks two conditions; the `task_committed` branch and
`_prev_executor_state`, which it alone read, are gone. `ExecutorState.holding` stays (analysis scripts read it;
nothing on the run path does). The regenerated baselines (tb1a 16, tb1b 4, tb1c 8, tb3 12, at 36b3978) differ
from the previous ones only in the removed decisions' `[meta*]` lines (133 decisions), the six 1-tick holds they
placed (tb1a: s20 and s50 at tick 31, s30 at tick 47, both priors; the robot's line at that tick reads the
acknowledged `pick_up` instead of a stand), and the executor's bookkeeping of the reload that no longer happens
(no `_load_plan` at the grasp; a later `continue_plan` maps `2->0` / `3->1`; `_on_task_complete` on the
4-action plan). `[sep]`, human, `[IR]` lines, the `[run]` header and completion are byte-identical.

NOT TRIGGERS EITHER, and where they would live: a hold the executor extends past the next trigger (TODO-71) and
the hold's expiry (E2b, dropped at D2). If either is ever needed, its home is a body-side event (T-D), not the
trigger set.

OPEN (TODO-90): two in-window sub-`min_separation` approaches under gate `b2a`, present with and without the
trigger, to be checked in a bounded task before T-C.
Files: shared/meta_planner.py (`evaluate_triggers`), shared/types.py (`ExecutorState.holding` comment),
shared/io_contracts.md (§2.2), docs/glossary.md, docs/TODOS_AND_DEFERRED.md (TODO-71, 76, 77, 90), CLAUDE.md,
docs/roadmap.md, analysis/tb1a_destination/, analysis/tb1b_two_tables/, analysis/tb1c_realized_flip/,
analysis/tb3_full_reorder/ (READMEs)
Reference: D3, September 2026; cchat ruling; analysis/ablation_task_committed/ (142deaa); D2; DESIGN-07

---

**A run-time deviation is the same operation as a load-time edit (Phase 7, recorded)**

RECORDED, NOT DECIDED (cchat, Hadi, 23 September 2026). A later phase, after T-G (roadmap, Phase 7).

The human executor's injection path serves both: a deviation from T-C's vocabulary applied to the action script
at load, and the same deviation arriving as an event during the run (from a viewer), applied at the next action
boundary. Only the source and the tick differ. The robot's mind receives nothing from either; it sees the
trajectory, as now ("the robot knows nothing of the human's script").

THE FIRST DECISION OF THE PHASE, the replay rule: the viewer offers a fixed set of events (the deviation
vocabulary, nothing free-form), every event is logged with its tick and arguments, and a finished live run
exports its event log as a pre-loaded script that reproduces it from a fresh start. Live runs demonstrate;
every evaluation number comes from pre-loaded scripts.
Reference: docs/handoffs/phase7_interactive_deviations.md; T-C ("The human's scenario is an action script"); T-E
