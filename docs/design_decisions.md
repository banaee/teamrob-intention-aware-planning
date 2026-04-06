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

**1. Planner outputs `AbstractPlan` with `List[GroundedAction]`**
The planner produces fully grounded symbolic actions — all variables resolved to
concrete values, each carrying a `completion_predicate` for the executor.
No microactions, no geometry. Mesa and ROS each interpret grounded actions
through their own embodiment layers (`action_decomposer.py`, `goal_executor_ros.py`).

**2. WorldState is symbolic**
Simulators build a canonical symbolic snapshot before calling core.
Geometry, positions, and sensor data stay inside the simulator.
The cognitive layer reasons only over predicates (`at`, `in_zone`, `holding`, `obj_at`).

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

**Domain knowledge is Python, configuration is YAML**
Task schemas, action operators, and scenarios are defined in Python inside
`domains/<domain>/` — typed, inspectable, no parsing layer.
YAML is reserved for true configuration: `costs.yaml`, `mesa_configs.yaml`.
Reason: the cognitive layer needs the decomposition tree as a queryable data
structure for both planning (top-down) and intention recognition (bottom-up).
YAML + string parsing was rejected because it collapsed structure that the
recognizer needs to traverse.

**HTN-style knowledge representation**
`TaskSchema` = HTN non-primitive tasks (decompose via methods).
`ActionSchema` = HTN primitive tasks (executable leaves, not decomposed further).
Only tasks decompose. Actions are the leaves of the decomposition tree.
Mesa expands primitive actions into microactions via `action_decomposer.py` —
this is embodiment-level detail, not part of the HTN structure.

**GOTO_ZONE removed — zone reasoning belongs in IR context**
`GOTO_ZONE` was removed as an intermediate action because:
- It was not a meaningful semantic abstraction — just a navigation wrapper
- Its completion predicate conflated zone arrival with object arrival
- Zone-level reasoning belongs in the recognizer's context weighting (`ωcontext`),
  not in the task decomposition tree
Zone information is still available via `in_zone(agent, zone)` predicates in
WorldState — used by IR, not by the executor.

**Predicate naming is explicit and distinct**
Two spatial predicate families with distinct semantics:
- `in_zone(agent, zone)` — coarse zone-level context, used by IR
- `at(agent, object)` — fine-grained object proximity, used by executor completion checking
Conflating these under a single `at` predicate caused a semantic mismatch where
`move_to` completion was never satisfied. Kept permanently separate.

**Scenarios are Python `ScenarioConfig` objects**
Scenarios live in `domains/<domain>/scenarios.py` as typed Python objects.
Task assignments reference `TaskSchema` and `TaskInstance` directly — no string
parsing, no YAML loading, no `?` prefix conventions at the config level.
Mesa-specific settings (step count, step size) remain in `mesa_configs.yaml`.

**Skeleton-first development**
All modules are built with correct interfaces and dummy logic first.
This validates the architecture and data flow before investing in algorithms.
Real algorithms (Bayesian update, cost-based planning, guard evaluation)
replace dummy logic in Phase 4.

**One micro-action per Mesa step**
Each Mesa step advances exactly one micro-action per agent.
This enforces the observable micro-action assumption from the paper formalization.

**Reactive/contingency behaviors belong in `replanning.py`**
Unexpected world events (dropped items, human deviations) are handled by the
replanning trigger — not encoded in task schemas.
Task schemas describe intended behavior. Contingency response is a runtime concern.
This boundary is not an HTN limitation — PDDL, HDDL, and all plan-representation
formalisms share it. Reactive architectures (BDI/PRS) handle it separately.

**Human agent has fixed plan per task — no replanning**
`HumanAgent` builds a plan once per `TaskInstance` and reuses it until the task
completes. This is a deliberate modeling assumption: the human is scripted and
provides ground truth for IR evaluation. Replanning logic exists only on `RobotAgent`.