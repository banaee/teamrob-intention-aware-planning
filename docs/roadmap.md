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
- Cancellation of a held-item task includes return-to-shelf cost before reordering.

**Phase 4A — IR: Bayesian belief updating**
- Real likelihood model: P(intention | observations) via Bayesian update
- Context weighting ω_context: spatial zone, time-of-day, task history
- Evidence accumulation across steps; prior → posterior as microactions observed
- IR runs from t=0 with uniform prior; meta_planner gates reordering on confidence threshold θ
- Output: `BeliefState` with full distribution + `most_likely` + `confidence`

**Phase 4B — HTN: recursive decomposition in planner.py**
- Replace flat method grounder with recursive decomposer
- Guard evaluation: select method whose preconditions hold in `WorldState`
- Forward chaining over `ActionSchema.effects` for state projection
- Output: `AbstractPlan` (flat grounded action list, single task)

**Phase 4C — MetaPlanner: scheduling + interference detection + cost comparison**
- At t=0: generate initial queue Q0 from assigned_tasks set (base cost, no IR)
- On cognitive clock event: receive BeliefState, ProjectedPlan, WorldState
- Predict human action sequence over horizon H (from IR most_likely + task decomposition)
- Align robot's ProjectedPlan against predicted human sequence → detect spatial/temporal interference
- Enumerate candidate task orderings (current queue + reorderings + cancellation variants)
- For each candidate: call planner.py (HTN) → projected action sequence → estimate cost
- Select minimum-cost candidate; update queue and ProjectedPlan if changed
- Cognitive clock triggers: task completion, belief threshold θ crossed, robot picks up item (cancellation cost changes discontinuously), human observed completing a task
- Open: hysteresis band for θ (θ_low / θ_high) vs single threshold — see DESIGN-07

**Phase 4D — Low-level execution adaptation**
- Executor continues to handle within-action adaptation (detour, pause) guided by execution hints in AbstractPlan
- No structural change to executor interface; hints richer than current skeleton

### Prerequisites before implementation
- DESIGN-06: define `ProjectedPlan` type in `shared/types.py`
- TODO-14: rename `AgentConfig.scheduled_tasks` → `assigned_tasks` (set) for robot
- DESIGN-07: settle cognitive clock trigger conditions and θ hysteresis policy
- New simple kitting layout (Layout 0) and scenario defined for Phase 4 development and testing

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
