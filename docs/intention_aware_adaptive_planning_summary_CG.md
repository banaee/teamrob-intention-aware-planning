# Intention-Aware Adaptive Planning Framework — Summary & Design Guide

## Overview

This document provides a **clean, unified summary** of the full architectural decisions, design principles, and implementation roadmap for the **TeamRob Intention-Aware Adaptive Planning Framework**. It consolidates the final conceptual agreements into a clear reference suitable for starting a new repository and guiding further development.

---

# 1. High-Level Vision

The framework separates the robot architecture into two conceptual layers:

## **A) Cognitive Layer (“Mind”)** — *Simulator-Agnostic Shared Modules*
Located in `shared/`.

These components implement:
- Human Intention Recognition
- Adaptive Planning
- Replanning Logic
- Task Knowledge / Decomposition Trees
- Canonical data types (Observation, BeliefState, WorldState, Plan)

They are **pure Python logic**, with **no Mesa or ROS dependencies**.

---

## **B) Embodiment Layer (“Body”)** — *Simulator-Specific Implementations*
Two independent bodies:
- `mesa_sim/` — idealized discrete simulation
- `ros_sim/` — real-world continuous sensing & actuation

Each embodiment provides:
- Sensing (human-action detection)
- Internal world model
- WorldState builder (symbolic)
- Observation builder (discrete µₜ)
- Execution (microactions or motion goals)
- Interface with actual simulation time

The key architectural principle:

> **Cognitive components are shared. Embodiment components are independent.**

---

# 2. Fundamental Design Decisions (The “Big Four”)

These decisions shape the entire architecture.

## **Decision 1 — Planner Outputs High-Level Plans WITH Execution Hints**
The planner returns:
- A list of discrete **AbstractActions**
- Optional **ExecutionHints**:
  - estimated path
  - estimated time
  - spatial or temporal constraints
  - suggested micro-action patterns (optional)

Mesa may follow hints directly.  
ROS uses them as soft constraints for real path/motion planners.

---

## **Decision 2 — WorldState is Symbolic**
Simulators build a **canonical symbolic snapshot**:
```python
WorldState = {
  "robot_zone": "station_A",
  "human_zone": "shelf_3",
  "object_locs": {"item1": "shelf_2"},
  "robot_holding": None,
  "human_holding": "itemA",
  "task_progress": {...}
}
```

The planner **does not operate on geometry**.  
Geometry stays in simulators.

---

## **Decision 3 — Simulators Decide WHEN to Call Core; Core Decides WHAT to Do**
- Mesa calls IR every step
- ROS calls IR periodically or event-based

Core provides:
- `update_observation → BeliefState`
- `should_replan → bool`
- `plan → AbstractPlan`

**Core never runs a loop**.  
Simulators own timing and scheduling.

---

## **Decision 4 — ROS Must Discretize Noisy Streams into Micro-Actions**
IR requires discrete µₜ as evidence.  
Mesa has perfect µₜ; ROS must classify from noisy sensor data.

Both simulators must feed IR with the same **canonical Observation** structure.

---

# 3. Shared I/O Contracts (Critical Reference)

The core relies on the following canonical types (see `shared/io_contracts.md`):

### **Observation**
- timestamp
- `micro_action` (mandatory)
- optional: position, zone, confidence, objects_nearby, meta

### **BeliefState**
- timestamp
- distribution τ → P
- most_likely τ
- confidence

### **WorldState**
Symbolic predicates describing robot + human state + environment.

### **AbstractAction**
High-level discrete action with optional hints.

### **AbstractPlan**
Sequence of AbstractActions with contingencies.

---

# 4. Repository Structure (Approved Final Layout)

```
teamrob_intrec/
│
├── shared/
│   ├── types.py
│   ├── recognizer.py
│   ├── planner.py
│   ├── replanning.py
│   ├── knowledge.py
│   ├── utils.py            # optional
│   └── io_contracts.md
│
├── configs/
│   ├── tasks.yaml
│   ├── scenarios.yaml
│   └── costs.yaml
│
├── mesa_sim/
│   ├── run_mesa.py
│   ├── model.py
│   ├── agents.py
│   ├── obs_builder.py
│   ├── world_state_builder.py
│   ├── microactions.py
│   └── executor.py
│
├── ros_sim/
│   ├── run_ros.py
│   ├── robot_agent_node.py
│   ├── obs_builder_ros.py
│   ├── world_state_builder_ros.py
│   ├── microaction_classifier_ros.py
│   └── goal_executor_ros.py
│
└── docs/
    ├── architecture.md
    ├── design_notes.md
    └── roadmap.md
```

---

# 5. Implementation Roadmap (Step-by-Step)

This is the recommended order to begin developing the new framework.

---

## **Phase 1 — Foundations (Shared/Core)**
**1. Create the repo skeleton**  
Empty files, empty dirs — enforce separation from day one.

**2. Write `io_contracts.md`**  
This acts as the constitution of the framework.

**3. Implement `shared/types.py`**  
Only dataclasses/dicts for Observation, BeliefState, WorldState, Plan, Action.

No algorithms yet.

---

## **Phase 2 — Extract IR (Cognitive Layer)**
Move intention recognition logic from old code into:
- `shared/recognizer.py`
- `shared/replanning.py` (trigger logic)

Test using synthetic observation sequences.

Mesa/ROS not needed yet.

---

## **Phase 3 — Build Minimal Mesa Loop**
Create a minimal embodiment:

- Human agent with deterministic actions
- Robot agent calling:
  - obs_builder
  - world_state_builder
  - recognizer/update
  - replanning
  - planner
  - microaction execution

No visualization yet.

Validate:
- IR responds to changes
- Planner produces consistent abstract plans
- Replanning triggers correctly

---

## **Phase 4 — Full Planning Logic**
Develop full adaptive planning in:
- `shared/planner.py`
- `shared/knowledge.py`
- Possibly `shared/utils.py` for helpers

---

## **Phase 5 — Visualization (Optional Later)**
Integrate Solara once Mesa loop is fully validated.

---

## **Phase 6 — ROS Embodiment**
ROS team builds:
- µₜ classifier from sensors
- symbolic WorldState builder
- observation builder
- goal executor

The core requires no modification.

---

# 6. Design Philosophy (Summary)

### **Focus on clarity and correctness, not heavy abstraction**
- No plugin architecture
- No dependency inversion
- No complex inheritance trees
- No adapters unless absolutely necessary

### **Simulator-agnostic core**
- IR, planner, world-state, types all live in shared/

### **Simulators free to implement embodiment in their own natural style**
- Mesa: synchronous, step-based, micro-actions executed directly
- ROS: asynchronous, event/timer-based, micro-actions become motion goals

### **Canonical symbolic interface**
Everything passes through:
- `Observation`
- `BeliefState`
- `WorldState`
- `AbstractPlan`

This makes reasoning consistent across both simulators.

---

# 7. Final Notes

✔ This framework is fully aligned with the DAI paper formalization  
✔ It supports both idealized simulation and real-world robotics  
✔ It avoids duplicated logic  
✔ It reduces long-term maintenance load  
✔ It supports future simulators if needed  
✔ It is simple enough to implement incrementally

---

# 8. Appendix: Quick Glossary

- **micro-action (µₜ)** – discrete atomic behavior ("move to shelf", "pick item")  
- **intention (τ)** – high-level human or robot task  
- **AbstractAction** – robot high-level actions  
- **AbstractPlan** – full structured plan  
- **WorldState** – symbolic snapshot used by planner  
- **Embodiment** – simulator-specific sensing & acting  
- **Cognitive Layer** – IR, planner, replanning logic  
- **Canonical Interfaces** – Observation, WorldState, BeliefState  

---

This document is the definitive reference for the intention-aware adaptive planning architecture and should be considered the starting point for all implementation work.

