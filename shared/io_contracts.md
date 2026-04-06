# shared/io_contracts.md

This document defines the **minimal, simulator-agnostic I/O contracts** for the cognitive core in `shared/`.
Implementation details (Bayes, HTN search, etc.) are intentionally omitted.
All simulators (Mesa, ROS) must translate their internal data into these canonical forms.

---

## 0. Notation (matches paper)

- **τ** : an intention (task) from the intention set **T**
- **a** : a high-level action from action set **A**
- **μ** : a micro-action from micro-action set **M**
- **t** : logical time index (Mesa step or ROS window index)

Core algorithms reason over **discrete micro-actions** and **symbolic world predicates**.

---

## 1. Canonical Data Types (defined in `shared/types.py`)

### 1.1 `Observation`

**Produced by simulator**, consumed by `IntentionRecognizer`.

```python
@dataclass
class Observation:
    timestamp: float              # logical time (step index or timestamp)
    agent_id: str                 # observed agent (usually human)
    observer_id: str              # observing agent (usually robot)
    detected_microaction: str     # μ_t label e.g. "step", "grasp", "stand"
    spatial: SpatialContext       # position, zone — derived from world state
    action_context: ActionContext # current task/action labels on observed agent
    confidence: float             # 1.0 in Mesa (ground truth); <1.0 in ROS
```

**Hard requirement:**
Mesa provides `detected_microaction` perfectly from ground truth.
ROS must **discretize sensor streams** into microaction labels before calling IR.

---

### 1.2 `BeliefState`

**Produced by IR**, consumed by planner and replanning triggers.

```python
@dataclass
class BeliefState:
    timestamp: float
    agent_id: str                          # agent whose intention is being tracked
    distribution: Dict[str, float]         # {intention_name: probability}
    most_likely: str                       # argmax intention name
    confidence: float                      # max probability
    predicted_next_actions: Dict           # stub — Phase 4
```

**Invariants:**
- probabilities sum to 1.0 (within numerical tolerance)
- `most_likely` is a key in `distribution`

---

### 1.3 `WorldState`

**Produced by simulator**, consumed by planner and replanning triggers.

Symbolic predicate snapshot. The simulator maintains richer internal state but exports this canonical symbolic form.

```python
@dataclass
class WorldState:
    timestamp: float
    agent_states: Dict[str, AgentState]    # {agent_id: AgentState}
    object_locations: Dict[str, str]       # {item_id: location_id}
    object_zones: Dict[str, str]           # {item_id: zone_id}
    predicates: Set[Predicate]             # symbolic facts
```

**Predicate naming convention (important):**
- `in_zone(agent_id, zone_id)` — coarse zone-level context, used by IR context reasoning
- `at(agent_id, object_id)` — fine-grained object proximity, used by executor completion checking
- `holding(agent_id, item_id)` — agent is carrying item
- `obj_at(item_id, location_id)` — item rests at location

`in_zone` and `at` are intentionally distinct predicates.
Conflating them caused a semantic mismatch where `move_to` completion was never satisfied.

**Design rule:** core planners only use symbolic predicates; geometry stays in simulators.

---

### 1.4 `GroundedAction`

**Produced by planner**, consumed by simulator executor.

```python
@dataclass
class GroundedAction:
    action_name: str                       # e.g. "move_to", "pick_up"
    bindings: Dict[str, str]               # {var_name: concrete_value}
    completion_predicate: Predicate        # fully instantiated — executor checks this
    operator: ActionSchema                 # reference to schema for decomposer
```

All variables are fully resolved — no `Var` objects remain in a `GroundedAction`.
`completion_predicate` uses `Const` args only — executor checks set membership in
`WorldState.predicates` directly.

---

### 1.5 `AbstractPlan`

**Produced by planner**, consumed by simulator executor.

```python
@dataclass
class AbstractPlan:
    goal_intention: str                    # τ the robot is pursuing
    actions: List[GroundedAction]          # ordered grounded action sequence
```

---

## 2. Module Contracts

### 2.1 `IntentionRecognizer` (`shared/recognizer.py`)

#### Constructor

```python
IntentionRecognizer(knowledge: DomainKnowledgeBase)
```

#### Update

```python
update(
    obs: Observation,
    prev_belief: BeliefState | None = None
) -> BeliefState
```

**Inputs**
- `obs`: discrete microaction evidence + spatial/action context
- `prev_belief`: if provided, IR continues from that belief; else uses uniform prior

**Output**
- new `BeliefState` at `obs.timestamp`

**Side effects**
- None required by contract. Implementation may cache history internally.

---

### 2.2 Replanning Trigger (`shared/replanning.py`)

```python
should_replan(
    current_plan: AbstractPlan | None,
    new_belief: BeliefState,
    world: WorldState,
    prev_belief: BeliefState | None = None,
) -> dict
```

**Output**

```python
{
    "replan": bool,
    "reason": str,        # e.g. "belief_divergence", "precondition_broken"
    "score": float | None,
}
```

**Notes**
- Simulators decide WHEN to call this — Mesa calls every step, ROS calls periodically
- Core never schedules itself

---

### 2.3 `AdaptivePlanner` (`shared/planner.py`)

#### Constructor

```python
AdaptivePlanner(knowledge: DomainKnowledgeBase)
```

#### Plan

```python
plan(
    my_intention: str,                  # robot's assigned task name
    task_params: Dict[str, str],        # {var_name: concrete_value} e.g. {"?item": "item_3"}
    agent_id: str,                      # executing agent — injected as ?agent binding
    belief: BeliefState,
    world: WorldState,
    current_plan: AbstractPlan | None = None,
) -> AbstractPlan
```

**Output**
- `AbstractPlan` with fully grounded `GroundedAction` list
- All completion predicates instantiated with `Const` args
- No unresolved variables

**TODO Phase 4:** guard evaluation, belief-driven adaptation, cost-based selection.

---

### 2.4 `DomainKnowledgeBase` (`shared/domain_knowledge.py`)

```python
DomainKnowledgeBase.from_domain(domain: DomainModel) -> DomainKnowledgeBase
```

Domain operators are defined in Python (`domains/<domain>/`), not parsed from YAML.

Provides read-only access to:
- intention set **T** — via `get_all_intentions()` (filtered by `DomainModel.intentions`)
- assigned intentions — via `get_assigned_intentions()`
- foreseeable intentions — via `get_foreseeable_intentions()`
- task schemas — via `get_task_schema(name)`
- action operators — via `get_action_operator(name)`
- microaction set **M** — via `get_microactions()`
- reverse lookups for IR:
  - `get_tasks_for_action(action_name)` → candidate tasks
  - `get_actions_for_microaction(mu)` → candidate actions

**No simulator imports allowed.**

---

## 3. Domain Knowledge Structure (`domains/<domain>/`)

Domain knowledge lives outside `shared/` in domain-specific Python packages.

```
domains/kitting/
    tasks.py           # TaskSchema definitions — HTN non-primitive tasks
    actionOperators.py # ActionSchema definitions — HTN primitive tasks (leaves)
    registry.py        # builds DomainModel, declares intention set
    scenarios.py       # ScenarioConfig objects — typed Python, no YAML
    env1_layout.json   # environment spatial layout
```

**HTN alignment:**
- `TaskSchema` = non-primitive task — decomposes via `MethodSchema`
- `ActionSchema` = primitive task — executable leaf, not decomposed further in HTN layer
- Mesa expands primitive actions into microactions via `action_decomposer.py` — embodiment detail only

---

## 4. Simulator Responsibilities

### 4.1 Mesa (`mesa_sim/`)

- Maintains perfect synchronous ground truth
- Builds `Observation` each step from human agent state (`detected_microaction` known exactly)
- Builds `WorldState` each step from Mesa world — emits `in_zone` and `at` predicates
- Calls cognitive loop each step: `obs_builder → recognizer → replanning → planner → executor`
- Executes `GroundedAction` via `action_decomposer.py` → microaction queue → one microaction per step

### 4.2 ROS (`ros_sim/`)

- Maintains continuous noisy streams
- Must infer discrete microaction labels **outside core** before calling IR
- Builds `Observation` per window/event, `WorldState` from TF/perception
- Calls core functions on its own schedule
- Executes `GroundedAction` via ROS action servers

---

## 5. Non-Goals (explicitly out of scope)

- Exact probabilistic update equations
- Exact planning algorithms
- ROS classifier implementation
- Motion planning, collision checking, control loops
- Visualization or experiment tooling

---

## 6. Validation Rules

Simulators MUST ensure:

1. `Observation.detected_microaction` is never empty
2. `BeliefState.distribution` sums to 1.0 (±1e-6)
3. `BeliefState.most_likely` is a key in `distribution`
4. `WorldState.predicates` contains at minimum `in_zone` predicates for all active agents
5. `AbstractPlan.actions` is a non-empty list of fully grounded `GroundedAction` objects
6. No `Var` objects remain in any `GroundedAction.bindings` or `completion_predicate`
7. All intention names in `BeliefState.distribution` are registered in `DomainModel.intentions`

---
