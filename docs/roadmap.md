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
- `shared/planner.py`: skeleton with raw action sequence output
- `shared/replanning.py`: skeleton with `no_plan` trigger

## Phase 3 — Kitting Domain + Mesa Simulation ✅
- `domains/kitting/`: `tasks.py`, `ActionSchemas.py`, `registry.py`, `scenarios.py`, `env1_layout.json`
- `mesa_sim/sim_model.py`, `sim_agents.py`, `world_state_builder.py`, `obs_builder.py`
- `mesa_sim/action_decomposer.py`, `executor.py`, `run_mesa.py`
- Headless simulation runs correctly: human and robot agents complete full assigned task sequences
- `ProcessCompletion` contract in place; two predicate families (`in_zone`, `at`) correctly separated

---

## Phase 2.2 — Mesa Visualization 🔄 *next*
- Solara + Plotly interactive visualization layer (`mesa_sim/viz/`)
- Live agent positions, task progress, belief state display
- Goal: accelerate debugging for subsequent domain work

## Phase 2.1 — Dock Inloading Domain 🔄 *next (parallel)*
- `domains/dock_inloading/` modeled on HITS3 Scenario 2 (Olivia Stener / TRATON)
- Three tasks identified: `DELIVER_PALLET` (assigned), `DRIVER_PHONE_CALL` and `DRIVER_TALKS_TO_DOCKWORKER` (foreseeable)
- Key challenge: intention recognition of execution *variants* (which path to a shared goal), not just task selection

---

## Phase 4 — Full Cognitive Algorithms 🔲
- Bayesian IR: real likelihood model, context weighting (ω_context), evidence accumulation
- Cost-based adaptive planning: guard evaluation, forward chaining over `effects`
- Replanning triggers: belief divergence, confidence threshold

## Phase 5 — Evaluation & Experiments 🔲
- Comparative evaluation: IR accuracy vs. ground truth (known human intentions)
- Kitting and dock inloading scenarios
- Metrics: early recognition, plan adaptation latency, task completion efficiency

## Phase 6 — ROS Embodiment 🔲 *(ROS team)*
- `ros_sim/`: microaction classifier from sensor streams, symbolic WorldState builder, goal executor via ROS action servers
- Core `shared/` requires no modification
- Architectural interface already defined in `shared/io_contracts.md`
