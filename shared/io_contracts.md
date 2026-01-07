# shared/io_contracts.md

This document defines the **minimal, simulator‑agnostic I/O contracts** for the cognitive core in `shared/`.
Implementation details (Bayes, PDDL, etc.) are intentionally omitted.  
All simulators (Mesa, ROS) must translate their internal data into these canonical forms.

---

## 0. Notation (matches paper)

- **τ** : an intention (task) from the intention set **T**
- **a** : a high‑level action from action set **A**
- **μ** : a micro‑action from micro‑action set **M**
- **t** : logical time index (Mesa step or ROS window index)

Core algorithms reason over **discrete micro‑actions** and **symbolic world predicates**.

---

## 1. Canonical Data Types (defined in `shared/types.py`)

### 1.1 `Observation`

**Produced by simulator**, consumed by `IntentionRecognizer`.

```python
Observation = {
  "t": float | int,                 # logical time (step index or timestamp)
  "observer_id": str,               # usually robot id
  "observed_agent_id": str,         # usually human id

  # REQUIRED discrete evidence for IR
  "micro_action": str,              # μ_t label, e.g., "move_to_shelf_3", "pick_part_A"

  # OPTIONAL context (only if available)
  "position": (float, float) | None,  # observed agent position in shared coordinate frame
  "zone": str | None,                 # symbolic zone label, e.g., "corridor", "shelf_3"
  "objects_nearby": list[str] | None, # symbolic object ids
  "confidence": float | None,         # confidence of micro_action classifier (0..1)
  "meta": dict | None                 # extra simulator data (ignored by core unless used)
}
```

**Hard requirement:**  
Mesa provides `micro_action` perfectly from ground truth.  
ROS must **discretize sensor streams** into `micro_action` labels before calling IR.

---

### 1.2 `BeliefState`

**Produced by IR**, consumed by planner and replanning triggers.

```python
BeliefState = {
  "t": float | int,
  "distribution": {                 # P(τ | evidence≤t)
      str: float                    # intention_id -> probability
  },
  "most_likely": str,               # argmax intention_id
  "confidence": float,              # max probability
  "meta": dict | None               # any diagnostics
}
```

**Invariants:**

- probabilities sum to 1.0 (within numerical tolerance)
- `most_likely` is a key in `distribution`

---

### 1.3 `WorldState`

**Produced by simulator**, consumed by planner and replanning triggers.

Symbolic predicate snapshot. The simulator may maintain a richer internal state, but must export **this canonical symbolic form**.

```python
WorldState = {
  "t": float | int,

  # agent symbolic locations / statuses
  "robot_zone": str,
  "human_zone": str,
  "robot_pos": (float, float) | None,
  "human_pos": (float, float) | None,

  # object predicates (examples)
  "object_locs": { str: str },      # object_id -> zone_id
  "robot_holding": str | None,
  "human_holding": str | None,

  # task progress predicates (examples)
  "task_progress": { str: str },    # intention_id -> stage label
  "blocked_zones": list[str] | None,

  "meta": dict | None
}
```

**Design rule:** core planners only use symbolic predicates; geometry stays in simulators.

---

### 1.4 `AbstractAction`

A high‑level action the robot may execute.

```python
AbstractAction = {
  "action_id": str,                 # unique identifier, e.g., "nav_001", "pick_002"
  "action_type": str,               # e.g., "navigate", "pick", "place", "wait"
  "params": dict,                   # symbolic parameters (targets, items, zones)

  "preconditions": list[str] | None,
  "effects": list[str] | None,

  # OPTIONAL execution hints (Decision 1)
  "hints": {
      "estimated_time": float | None,
      "estimated_path": list[tuple[float,float]] | None,
      "spatial_constraints": dict | None,
      "temporal_constraints": dict | None
  } | None
}
```

Hints are **advisory**:

- Mesa may follow them directly.
- ROS treats them as soft constraints for its own motion/action stack.

---

### 1.5 `AbstractPlan`

**Produced by planner**, consumed by simulator executor.

```python
AbstractPlan = {
  "t": float | int,
  "goal_intention": str,            # τ the robot is pursuing
  "actions": list[AbstractAction],  # discrete high-level sequence

  # OPTIONAL contingencies for belief uncertainty
    "contingencies": {         # intention_id -> AbstractPlan     
    "fetch_shelf_1": AbstractPlan(...),  # if human switches to shelf_1
    "coffee_break": AbstractPlan(...)     # if human takes break
  } | None,
  "meta": dict | None
}
```

### Meta Fields

All types include optional `"meta": dict | None` for:

- Simulator-specific debugging data
- Performance metrics
- Visualization hints

**Core algorithms MUST ignore `meta` unless explicitly documented.**

---

## 2. Module Contracts

### 2.1 `IntentionRecognizer` (`shared/recognizer.py`)

#### Constructor

```python
IntentionRecognizer(knowledge: KnowledgeBase, priors: dict, params: dict)
```

- `knowledge` provides task schemas and micro‑action likelihood models.
- `priors` maps intention_id -> prior probability.
- `params` holds hyperparameters (update thresholds etc.)

#### Update

```python
update(
  obs: Observation,
  prev_belief: BeliefState | None = None
) -> BeliefState
```

**Inputs**

- `obs`: discrete micro‑action evidence + optional context
- `prev_belief`: if provided, IR continues from that belief; else uses priors

**Output**

- new `BeliefState` at `obs.t`

**Side effects**

- None required by contract. (Implementation may cache internally.)

---

### 2.2 Replanning Trigger Logic (`shared/replanning.py`)

Core provides **what counts as a replanning trigger**.

```python
should_replan(
  current_plan: AbstractPlan | None,
  new_belief: BeliefState,
  world: WorldState,
  prev_belief: BeliefState | None = None,
  params: dict | None = None
) -> dict
```

**Output**

```python
{
  "replan": bool,
  "reason": str,                # e.g., "belief_divergence", "precondition_broken"
  "score": float | None,        # trigger strength (0..1) if available
  "meta": dict | None
}
```

**Notes**

- **Simulators decide WHEN to call this.**
  - Mesa: each step or after each new obs
  - ROS: periodic window or event‑based callback
- Core never schedules itself.

---

### 2.3 `AdaptivePlanner` (`shared/planner.py`)

#### Constructor

```python
AdaptivePlanner(knowledge: KnowledgeBase, cost_model: dict, params: dict)
```

#### Plan

```python
plan(
  my_intention: str,                 # robot's assigned intention τ_A
  belief: BeliefState,               # belief over human intentions τ_H
  world: WorldState,
  current_plan: AbstractPlan | None = None
) -> AbstractPlan
```

**Inputs**

- `my_intention`: robot task intention id
- `belief`: current belief over human intentions
- `world`: canonical symbolic world snapshot
- `current_plan`: optional; allows plan repair vs full replanning

**Output**

- a discrete `AbstractPlan` with optional hints and contingencies

---

### 2.4 `KnowledgeBase` (`shared/knowledge.py`)

```python
KnowledgeBase.from_yaml(tasks_yaml: str, scenarios_yaml: str | None = None) -> KnowledgeBase
```

Provides read‑only access to:

- intention set **T**
- action set **A**
- micro‑action set **M**
- task decomposition trees (τ → a → μ)
- foreseeable task sets (T_F)
- any likelihood tables used by IR
- any symbolic preconditions/effects used by planner

**No simulator imports allowed.**

---

## 3. Simulator Responsibilities

### 3.1 Mesa (`mesa_sim/`)

- Maintains perfect, synchronous ground truth.
- Builds:
  - `Observation` each step from human state (`micro_action` known)
  - `WorldState` each step from Mesa world
- Calls:
  - `recognizer.update(obs, prev_belief)`
  - `should_replan(...)`
  - `planner.plan(...)` only if replan trigger true
- Executes plans by discretizing to Mesa micro‑actions.

### 3.2 ROS (`ros_sim/`)

- Maintains continuous, noisy streams.
- Must:
  - infer discrete `micro_action` labels **outside core**
  - aggregate stream into periodic/event windows
- Builds:
  - `Observation` for each window/event
  - `WorldState` snapshot from TF/perception into canonical symbolic form
- Calls core functions exactly like Mesa, but on its own schedule.
- Executes plans via ROS action servers; treats hints as soft constraints.

---

## 4. Non‑Goals (explicitly out of scope here)

- Exact probabilistic update equations
- Exact planning algorithms
- ROS classifier implementation
- Motion planning, collision checking, control loops
- Visualization or experiment tooling

These belong to implementation phases inside `shared/` (algorithms) and `mesa_sim/` / `ros_sim/` (embodiment).

## 5. Validation Rules

Simulators MUST ensure:

1. `Observation.micro_action` is never empty/null
2. `BeliefState.distribution` sums to 1.0 (±1e-6)
3. `WorldState` contains at minimum: robot_zone, human_zone
4. `AbstractPlan.actions` is non-empty list
5. All string IDs reference valid entities in KnowledgeBase

---
