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
ROS calls it periodically or event-driven.
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

**env_layout.json structure: flat `env_objects` for static geometry, separate sections for dynamic entities**
Static physical objects (shelves, tables, machines, obstacles, delivery areas, gates,
doors) live in a flat `"env_objects"` list with a `"type"` field per entry.
`SimModel._init_env_objects()` loads all of them generically — no domain-specific
loaders needed, no new top-level JSON sections for new object types.
Items (`"items"`), robots (`"robots"`), and humans (`"humans"`) stay in separate
top-level sections because they have distinct loading logic: items carry runtime
state fields (`held_by`, `at_location`, `is_scanned`, etc.), agents are instantiated
as Mesa objects and registered with the scheduler. Merging them into `"env_objects"`
would conflate static geometry with dynamic runtime entities.
Rule: never add a new top-level JSON section for a new object type — add it to
`"env_objects"` with an appropriate `"type"` value.

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

---

## Phase 4 Architectural Decisions

**`scheduled_tasks` semantics differ by agent type**
The field name `scheduled_tasks` is kept on `AgentConfig` for both agent types, but semantics differ:

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
Cancellation cost of a held-item task includes return-to-shelf steps before reordering.
Team-level semantic costs (human waiting, shared resource conflicts) are parked as a
future extension — the cost function interface must be designed to allow this extension
without requiring meta_planner redesign (see DESIGN-08).

**IR runs from t=0 with uniform prior; meta_planner gates action on confidence θ**
The recognizer updates belief every cognitive clock tick from the start of simulation.
It does not wait for "enough" observations. The meta_planner uses a confidence threshold
θ to gate reordering decisions: below θ, the current queue is maintained; above θ,
candidate evaluation is triggered. This gives continuous reasoning without premature
reordering on weak evidence.

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
