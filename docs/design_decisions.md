# TeamRob Framework — Design Decisions

Key architectural agreements for the Intention-Aware Adaptive Planning Framework.
This is a living reference of *why* things are designed the way they are.

---

## Core Principle: Mind / Body Separation

The robot architecture from the HCM paper maps directly to two layers:

- **Cognitive layer (`shared/`)** — the robot's mind. Simulator-agnostic. Pure Python.
  Handles intention recognition, adaptive planning, replanning logic, and domain knowledge.

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
Real algorithms (Bayesian update, cost-based planning) replace dummy logic later.

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
