# TeamRob Framework — Implementation Roadmap

---

## Phase 1 — Foundations ✅
- Repo skeleton with `shared/` / `mesa_sim/` / `ros_sim/` separation
- `shared/types.py`: canonical dataclasses (`Observation`, `BeliefState`, `WorldState`, `GroundedAction`, `AbstractPlan`)
- `shared/io_contracts.md`: interface specification between cognitive and embodiment layers
- `shared/domain_knowledge.py`: `DomainKnowledgeBase`, `DomainModel` interfaces
- HTN Python object model: `TaskSchema`, `ActionSchema`, `MethodSchema`, `Var`/`Const` typed terms

## Phase 2 — Cognitive Layer Skeletons ✅
- `shared/recognizer.py`: skeleton with uniform prior
- `shared/planner.py`: skeleton — flat method grounder (single-level decomposition, first method unconditionally)
- `shared/replanning.py`: skeleton with `no_plan` trigger *(retired Sept 2026 — absorbed into meta_planner.py)*

## Phase 3 — Kitting Domain + Mesa Simulation ✅
- `domains/kitting/`: `tasks.py`, `ActionSchemas.py`, `registry.py`, `scenarios.py`, `env1_layout.json`
- `mesa_sim/sim_model.py`, `sim_agents.py`, `world_state_builder.py`, `obs_builder.py`
- `mesa_sim/action_decomposer.py`, `executor.py`, `run_mesa.py`
- Headless simulation runs correctly: human and robot agents complete full assigned task sequences
- `ProcessCompletion` contract in place; two predicate families (`in_zone`, `at`) correctly separated

## Phase 2.2 — Mesa Visualization ✅
- Solara + Plotly interactive visualization layer (`mesa_sim/viz/`)
- Live agent positions, task progress, belief state display

## Phase 2.1 — Dock Loading Domain ✅
- `domains/dock_loading/` modeled on HITS3 Scenario 2 (Olivia Stener / TRATON)
- Tasks: `DELIVER_PALLET` (assigned), `DRIVER_PHONE_CALL`, `DRIVER_TALKS_TO_DOCKWORKER` (foreseeable)
- Open non-blocking bugs: BUG-03, BUG-04 (see TODOS_AND_DEFERRED.md)

---

## Phase 4 — Full Cognitive Algorithms 🔄 (4A ✅, 4B ✅, 4C ✅ single_task path, 4D 🔲)

### Conceptual design settled; 4A/4B/4C implemented

The robot operates with two planning levels and one recognition module, all in `shared/`:

**Module structure:**

- `shared/recognizer.py` — Bayesian IR (replaces dummy)
- `shared/meta_planner.py` — task scheduling, candidate evaluation, interference detection, cost comparison
- `shared/projection.py` — NEW: `Projector` — task + world → predicted trajectory; consumed by meta_planner, and by viz/evaluation later
- `shared/trajectory_algorithms.py` — NEW: pluggable path-realization and interference-detection functions
- `shared/planner.py` — HTN decomposer (called by meta_planner per candidate; replaces flat method grounder)
- ~~`shared/replanning.py`~~ — **retired Sept 2026**, deleted; trigger role absorbed into `evaluate_triggers()`

**Key design decisions for Phase 4:**

- Robot's `scheduled_tasks` list order carries no semantic commitment (see design_decisions.md) — it's the same field type/name as the human agent's, just not consumed as a schedule. Initial queue `Q0` is produced by the same update() mechanism used for every later reorder: evaluate_triggers()'s "no current task" condition fires on the first call, no IR confidence required to run it (IR runs from t=0 with a uniform prior regardless). No separate base-cost heuristic.
- `planner.py` becomes a true recursive HTN decomposer: if a StepCall names a TaskSchema (not a primitive ActionSchema), it recurses. Output remains a flat `AbstractPlan` (single task, executor-facing).
- `meta_planner.py` owns task selection. It calls `planner.py` per candidate task to project action sequences, evaluates costs, and selects the next task. HTN does not schedule — it only decomposes.
- Selection is **single-task, receding-horizon** (DESIGN-16): one best next task per trigger, re-decided from fresh WorldState and belief at the next trigger — not a search over orderings of the remaining pool. `full_reorder` is retained as a documented, switchable alternative but is not implemented.
- `ProjectedPlan` (DESIGN-06) is the meta_planner's internal reasoning structure, never handed to the executor. Under `single_task` it always holds exactly one entry; the multi-entry shape is retained for `full_reorder`.
- Interference detection is **geometric, not zone-based** — actual Euclidean distance between projected positions over time. `ProjectedPlanEntry` carries `Segment`s; `ConflictPoint` carries `position` + `distance`, no zone.
- Cost is measured uniformly in Mesa simulation steps (seconds in ROS): moves, detours, pauses all equal cost units. Team-level semantic costs parked as future extension (see DESIGN-08).
- Cancellation of a held-item task is handled by HTN method selection, not a meta_planner cost term — see design_decisions.md.

**Phase 4A — IR: Bayesian belief updating** ✅ COMPLETE, validated against scenario_00

- Real likelihood model implemented: schema-driven dispatch via
  `PROGRESS_EVALUATORS` registry (shared/likelihood_functions.py) — no
  hardcoded microaction strings in recognizer.py
- `BELIEF_FLOOR = 1e-3` prevents probability collapse at task transitions;
  frozen-belief window shrank from 21 steps to 3
- Hypothesis space generalized: `TaskSchema.parameter_types` (multi-parameter,
  cartesian product) replaces earlier single-parameter design — supports any
  number of enumerable typed parameters per task, not just `?item`
- Output: `BeliefState` with full distribution + `most_likely` + `confidence`,
  verified against scenario_00 (200 steps, no regression)

**Phase 4B — HTN: recursive decomposition in planner.py** ✅ COMPLETE

- Recursive decomposer with real guard evaluation, derived variable
  resolution, `?agent` binding propagation

**Phase 4C — MetaPlanner: scheduling + interference detection + cost comparison** ✅ COMPLETE (`single_task` path), validated against scenario_00

Built and running end-to-end. All three tasks complete, correct terminal state, zero errors.

*Implemented:*
- `shared/meta_planner.py` — public: `evaluate_triggers()`, `update_human_projection()`,
  `update()`; internal: `seed_tasks()`, `_detect_interference()`, `_cost()`
- `shared/projection.py` — `Projector` extracted from `MetaPlanner`: `project()`
  (single-task path), `project_human()`, `build_segments()`, `estimate_duration()`.
  Injected into `MetaPlanner` rather than constructed by it — one instance, held by the
  agent, shareable with viz/evaluation
- `shared/trajectory_algorithms.py` — `straight_line_path()`, `stationary_segment()`,
  `discretized_time_sampling()`; `closest_point_of_approach()` and `obstacle_aware_path()`
  documented but deliberately unimplemented
- `shared/types.py` — `Segment`, `ConflictPoint` (retyped, zone-free),
  `InterferenceAssessment`, `ExecutorState`, `TriggerDecision`, `UpdateResult`,
  `task_instance_key()`; `ProjectedPlanEntry.spatial_zones` → `segments`
- `mesa_sim/sim_agents.py` — `RobotAgent` migrated off `replanning.py`; `task_index` and
  `_get_current_task_instance()` removed; `finished` flag added
- `domains/kitting/tasks.py` — third `MethodSchema` `deliver_already_held`, required by the
  re-decompose-from-scratch design (see design_decisions.md)
- `shared/replanning.py` — deleted

*Design questions resolved (Q1–Q4 from July 2026, plus September 2026 session):*
- Q1: `MetaPlanner` owns the task queue internally (not passed externally)
- Q2: human task projection uses `recognizer.get_hypothesis()` to resolve `belief.most_likely`
  back to its `HypothesisKey`; the recognizer is held **by reference** (same live instance the
  agent owns — `get_hypothesis()` is belief-stateless, so no staleness risk)
- Q3: `_estimate_duration` uses a self-contained geometric estimate (`distance / assumed_speed`)
- Q4: `replanning.py` retired in one commit after end-to-end validation ✅ done
- DESIGN-07 resolved: three triggers (`no_current_task`, `theta_crossed` as a *crossing event*,
  `task_committed`); θ=0.75, no hysteresis, confidence gate-only
- DESIGN-16 resolved: single-task receding-horizon selection; strategy flag for `full_reorder`
- Cancellation resolved (July): guarded HTN method, not a `_cost()` term
- Queue invariant: `_queue` excludes the executing task; candidates = `[current_task] + queue`
- Task exhaustion returned as `UpdateResult(current_task=None, queue=[])`, not raised
- `_cost()` is hard-gate only — `conflicts` computed and carried but not priced (DESIGN-08)
- Q0 needs no bespoke heuristic — `no_current_task` covers t=0 and completion identically

*Known validation gaps (not blocking, tracked in TODOS_AND_DEFERRED.md):*
- TODO-30: interference **exclusion** branch never exercised — every candidate was feasible
  in every run. The detection machinery runs, but its whole purpose is unproven.
- TODO-29: `deliver_with_return` unexercised under MetaPlanner (a held item that is also a
  candidate always wins on cost, so `deliver_already_held` fires instead)
- TODO-28: `min_safe_distance` / `assumed_speed` uncalibrated placeholders
- TODO-32: `wait_at` duration ignored — matters once foreseeable tasks are tested

*Next for Phase 4C:* stress-testing with scenarios that force actual reselection and
interference exclusion, and with the human performing foreseeable tasks.

**Phase 4D — Low-level execution adaptation**
- Executor continues to handle within-action adaptation (detour, pause) guided by execution hints in AbstractPlan
- No structural change to executor interface; hints richer than current skeleton
- Now scoped more concretely via DESIGN-13 (see TODOS_AND_DEFERRED.md): a
  common, non-committed path-realization estimator called from
  `_estimate_duration`, handling both pause and detour as outcomes of one
  call driven by a conflict hint from `_detect_interference`. For Mesa, this
  estimator can also serve as real execution-time realization (replacing
  straight-line `steps_toward`), collapsing cost-time and execution-time
  path realization into one function. ROS keeps a two-tier split (this
  estimator for cost estimation, PRIEST for real execution) — still a
  dedicated design session away from being built

### Prerequisites before implementation

- DESIGN-06: define `ProjectedPlan` type in `shared/types.py` ✅ DONE
- TODO-14: `AgentConfig.scheduled_tasks` semantics split by agent type ✅ DONE (resolution text corrected Sept 2026 — robot list is an unordered *pool*, not a prioritised queue)
- DESIGN-07: cognitive clock triggers + θ policy settled ✅ DONE (no hysteresis; three triggers implemented)
- New simple kitting layout (Layout 0) and scenario for Phase 4 dev ✅ DONE (env_layout0/scenario_00)
- Q1–Q4 meta_planner design questions ✅ RESOLVED (see Phase 4C above)
- Typed-parameter object model (SimObject/is_portable/parameter_types) ✅ DONE, verified against scenario_00
- DESIGN-16: selection strategy (single-task vs. full reorder) ✅ RESOLVED (Sept 2026)

---

## Phase 5 — Evaluation & Experiments 🔲
- Comparative evaluation: IR accuracy vs. ground truth (known human intentions from scripted human)
- Domains: kitting (Layout 0 simple scenario first, then full), dock loading
- Metrics:
  - IR: early recognition step, posterior convergence rate, accuracy at task completion
  - AP: plan adaptation latency (steps from θ crossed to new queue adopted), reordering frequency
  - Team efficiency: total steps to complete all tasks vs. baseline (no IR, fixed queue)

## Phase 6 — ROS Embodiment 🔲 *(ROS team)*
- `ros_sim/`: microaction classifier from sensor streams, symbolic WorldState builder, goal executor via ROS action servers
- Core `shared/` requires no modification for ROS integration
- Architectural interface already defined in `shared/io_contracts.md`
- Note: Phase 4 may add fields to `BeliefState` and introduce `ProjectedPlan` — ROS team should not build tightly against current `AbstractPlan` shape
- Before implementation: cognitive-clock trigger must be event-driven, never
  a fixed timer or derived from the motion-clock (PRIEST) tick rate; and the
  RESELECT/WAIT (or equivalent) decision must be made once, in `shared/` —
  the embodiment layer must only execute the returned decision, never run a
  parallel heuristic capable of independently producing or short-circuiting
  it. Both constraints surfaced concretely reviewing an early ROS
  integration attempt; see TODOS_AND_DEFERRED.md (NOTE on DESIGN-07, and the
  single-decision-path NOTE) before starting ros_sim/.