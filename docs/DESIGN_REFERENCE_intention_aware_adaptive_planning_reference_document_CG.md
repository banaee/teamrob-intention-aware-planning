# Intention-Aware Adaptive Planning Framework â€” Summary & Design Guide

## Overview

This document provides a **clean, unified summary** of the full architectural decisions, design principles, and implementation roadmap for the **TeamRob Intention-Aware Adaptive Planning Framework**. It consolidates the final conceptual agreements into a clear reference suitable for starting a new repository and guiding further development.

---

# 1. High-Level Vision

The framework separates the robot architecture into two conceptual layers:

## **A) Cognitive Layer (â€œMindâ€)** â€” *Simulator-Agnostic Shared Modules*
Located in `shared/`.

These components implement:
- Human Intention Recognition
- Adaptive Planning
- Replanning Logic
- Task Knowledge / Decomposition Trees
- Canonical data types (Observation, BeliefState, WorldState, Plan)

They are **pure Python logic**, with **no Mesa or ROS dependencies**.

---

## **B) Embodiment Layer (â€œBodyâ€)** â€” *Simulator-Specific Implementations*
Two independent bodies:
- `mesa_sim/` â€” idealized discrete simulation
- `ros_sim/` â€” real-world continuous sensing & actuation

Each embodiment provides:
- Sensing (human-action detection)
- Internal world model
- WorldState builder (symbolic)
- Observation builder (discrete Âµâ‚œ)
- Execution (microactions or motion goals)
- Interface with actual simulation time

The key architectural principle:

> **Cognitive components are shared. Embodiment components are independent.**

---

# 2. Fundamental Design Decisions (The â€œBig Fourâ€)

These decisions shape the entire architecture.

## **Decision 1 â€” Planner Outputs High-Level Plans WITH Execution Hints**
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

## **Decision 2 â€” WorldState is Symbolic**
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

## **Decision 3 â€” Simulators Decide WHEN to Call Core; Core Decides WHAT to Do**
- Mesa calls IR every step
- ROS calls IR periodically or event-based

Core provides:
- `update_observation â†’ BeliefState`
- `should_replan â†’ bool`
- `plan â†’ AbstractPlan`

**Core never runs a loop**.  
Simulators own timing and scheduling.

---

## **Decision 4 â€” ROS Must Discretize Noisy Streams into Micro-Actions**
IR requires discrete Âµâ‚œ as evidence.  
Mesa has perfect Âµâ‚œ; ROS must classify from noisy sensor data.

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
- distribution Ï„ â†’ P
- most_likely Ï„
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
â”‚
â”œâ”€â”€ shared/
â”‚   â”œâ”€â”€ types.py
â”‚   â”œâ”€â”€ recognizer.py
â”‚   â”œâ”€â”€ planner.py
â”‚   â”œâ”€â”€ replanning.py
â”‚   â”œâ”€â”€ knowledge.py
â”‚   â”œâ”€â”€ utils.py            # optional
â”‚   â””â”€â”€ io_contracts.md
â”‚
â”œâ”€â”€ configs/
â”‚   â”œâ”€â”€ tasks.yaml
â”‚   â”œâ”€â”€ scenarios.yaml
â”‚   â””â”€â”€ costs.yaml
â”‚
â”œâ”€â”€ mesa_sim/
â”‚   â”œâ”€â”€ run_mesa.py
â”‚   â”œâ”€â”€ model.py
â”‚   â”œâ”€â”€ agents.py
â”‚   â”œâ”€â”€ obs_builder.py
â”‚   â”œâ”€â”€ world_state_builder.py
â”‚   â”œâ”€â”€ microactions.py
â”‚   â””â”€â”€ executor.py
â”‚
â”œâ”€â”€ ros_sim/
â”‚   â”œâ”€â”€ run_ros.py
â”‚   â”œâ”€â”€ robot_agent_node.py
â”‚   â”œâ”€â”€ obs_builder_ros.py
â”‚   â”œâ”€â”€ world_state_builder_ros.py
â”‚   â”œâ”€â”€ microaction_classifier_ros.py
â”‚   â””â”€â”€ goal_executor_ros.py
â”‚
â””â”€â”€ docs/
    â”œâ”€â”€ architecture.md
    â”œâ”€â”€ design_notes.md
    â””â”€â”€ roadmap.md
```

---

# 5. Implementation Roadmap (Step-by-Step)

This is the recommended order to begin developing the new framework.

---

## **Phase 1 â€” Foundations (Shared/Core)**
**1. Create the repo skeleton**  
Empty files, empty dirs â€” enforce separation from day one.

**2. Write `io_contracts.md`**  
This acts as the constitution of the framework.

**3. Implement `shared/types.py`**  
Only dataclasses/dicts for Observation, BeliefState, WorldState, Plan, Action.

No algorithms yet.

---

## **Phase 2 â€” Extract IR (Cognitive Layer)**
Move intention recognition logic from old code into:
- `shared/recognizer.py`
- `shared/replanning.py` (trigger logic)

Test using synthetic observation sequences.

Mesa/ROS not needed yet.

---

## **Phase 3 â€” Build Minimal Mesa Loop**
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

## **Phase 4 â€” Full Planning Logic**
Develop full adaptive planning in:
- `shared/planner.py`
- `shared/knowledge.py`
- Possibly `shared/utils.py` for helpers

---

## **Phase 5 â€” Visualization (Optional Later)**
Integrate Solara once Mesa loop is fully validated.

---

## **Phase 6 â€” ROS Embodiment**
ROS team builds:
- Âµâ‚œ classifier from sensors
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

âœ” This framework is fully aligned with the DAI paper formalization  
âœ” It supports both idealized simulation and real-world robotics  
âœ” It avoids duplicated logic  
âœ” It reduces long-term maintenance load  
âœ” It supports future simulators if needed  
âœ” It is simple enough to implement incrementally

---

# 8. Appendix: Quick Glossary

- **micro-action (Âµâ‚œ)** â€“ discrete atomic behavior ("move to shelf", "pick item")  
- **intention (Ï„)** â€“ high-level human or robot task  
- **AbstractAction** â€“ robot high-level actions  
- **AbstractPlan** â€“ full structured plan  
- **WorldState** â€“ symbolic snapshot used by planner  
- **Embodiment** â€“ simulator-specific sensing & acting  
- **Cognitive Layer** â€“ IR, planner, replanning logic  
- **Canonical Interfaces** â€“ Observation, WorldState, BeliefState  

---

This document is the definitive reference for the intention-aware adaptive planning architecture and should be considered the starting point for all implementation work.
