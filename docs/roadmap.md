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
- `shared/replanning.py`: skeleton with `no_plan` trigger

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

## Phase 4 — Full Cognitive Algorithms 🔲

### Conceptual design settled (not yet implemented)

The robot operates with two planning levels and one recognition module, all in `shared/`:

**Module structure:**
- `shared/recognizer.py` — Bayesian IR (replaces dummy)
- `shared/meta_planner.py` — NEW: task scheduling, candidate generation, cost evaluation, reordering decisions
- `shared/planner.py` — HTN decomposer (called by meta_planner per task; replaces flat method grounder)
- `shared/replanning.py` — to be absorbed into meta_planner (retire after migration)

**Key design decisions for Phase 4:**
- Robot receives `assigned_tasks` as an **unordered set**, not a pre-ordered list. Initial queue `Q0` is produced by meta_planner at t=0 using base-cost heuristic (no IR evidence yet).
- `planner.py` becomes a true recursive HTN decomposer: if a StepCall names a TaskSchema (not a primitive ActionSchema), it recurses. Output remains a flat `AbstractPlan` (single task, executor-facing).
- `meta_planner.py` owns task ordering. It calls `planner.py` per candidate ordering to project action sequences, evaluates costs, and selects the best queue. HTN does not schedule — it only decomposes.
- A new `ProjectedPlan` type (see DESIGN-06) spans the full task queue for lookahead reasoning. It is never handed to the executor — it is the meta_planner's internal reasoning structure.
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

**Phase 4C — MetaPlanner: scheduling + interference detection + cost comparison** 🔲 NOT STARTED
Design questions resolved (session ending July 2026), implementation not yet begun:
- Q1: `MetaPlanner` owns the task queue internally (not passed externally)
- Q2: human task projection uses `recognizer.get_hypothesis()` to resolve
  `belief.most_likely` back to its `HypothesisKey` (task_name + bindings) —
  binding inference already solved by the hypothesis-space design, no
  separate geometric inference step needed
- Q3: `_estimate_duration` uses a self-contained geometric estimate
  (`distance / assumed_speed`, constructor param with default) — keeps
  `shared/` decoupled from simulator step-size config
- Q4: `replanning.py` held (wired in parallel) until Phase 4C validates
  end-to-end against scenario_00, then retired in one commit
- Separate from Q1–Q4 (not itself numbered): current_task competes as just
  another candidate in every `update()` call — no special-case WAIT/RESELECT
  branch. Continuation vs. reselection falls out of cost comparison across
  the full candidate set. Previously undocumented despite being decided; now
  written down after cross-checking against an alternative branch-based
  implementation during the Fatemeh code review.
- DESIGN-07 resolved: single threshold θ=0.75, no hold-last-decision
  hysteresis — confidence is gate-only, doesn't feed the cost function
- Cancellation resolved: not a meta_planner cost term. `deliver_item` gets a
  second, guarded HTN method (`deliver_with_return`) selected via existential
  guard matching in `_guards_satisfied` — `_cost()` needs no `carrying` param
  and no cancellation branch, it just decomposes each candidate and counts
  steps. Validated against scenario_00. See design_decisions.md. New open
  item from this: DESIGN-09 (cheap pre-check before full candidate
  enumeration — separate from cancellation itself).
- Prerequisite typed-parameter/object-model work completed as an unplanned
  but necessary dependency: `SimObject` unification (`is_portable` flag),
  `TaskSchema.parameter_types`, `known_objects_by_type` registry — needed
  once multi-instance object types (kitting_table, coffee_machine) were
  considered for `?destination`-style task parameters
- Still to build: `meta_planner.py` itself (`initialize_queue`, `update`,
  `_project`, `_estimate_duration`, `_detect_interference`, `_cost`), per
  the interface and flow already designed — `_cost()`'s signature drops
  `carrying` (no longer needed, per cancellation resolution above)
  
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
- TODO-14: `AgentConfig.scheduled_tasks` semantics split by agent type ✅ DONE
- DESIGN-07: cognitive clock triggers + θ policy settled ✅ DONE (no hysteresis)
- New simple kitting layout (Layout 0) and scenario for Phase 4 dev ✅ DONE (env_layout0/scenario_00)
- Q1–Q4 meta_planner design questions ✅ RESOLVED (see Phase 4C above)
- Typed-parameter object model (SimObject/is_portable/parameter_types) ✅ DONE, verified against scenario_00

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