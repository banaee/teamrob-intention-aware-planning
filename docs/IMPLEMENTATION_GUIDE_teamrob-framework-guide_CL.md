# TeamRob Intention Recognition Framework
## Design Documentation & Implementation Guide

**Project:** Intention-Aware Adaptive Planning in Human-Robot Teams  
**Paper:** HCM AAAI 2026 Workshop Submission  
**Framework Goal:** Separate cognitive algorithms (IR + Planning) from simulator implementations (Mesa + ROS)

---

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Key Design Decisions](#key-design-decisions)
3. [Project Structure](#project-structure)
4. [Component Specifications](#component-specifications)
5. [Implementation Roadmap](#implementation-roadmap)
6. [Migration Guide](#migration-guide)
7. [Reference: Resolved Design Questions](#resolved-design-questions)

---

## Architecture Overview

### Conceptual Model: Mind vs Body

The framework implements the robot agent architecture from the DAI paper (Figure 1) by separating:

**COGNITIVE LAYER ("Mind")** - Simulator-agnostic
- Intention Recognition (Bayesian inference)
- Adaptive Planning (cost-based task selection)
- Replanning triggers (belief divergence detection)
- Domain knowledge (task schemas, decomposition trees)

**EMBODIMENT LAYER ("Body")** - Simulator-specific
- **Mesa:** Discrete-time simulation for IR evaluation
- **ROS:** Real-world deployment for robot experiments

### Information Flow

```
Simulator World
      ↓
[Sensing & Action Detection] ← Embodiment layer
      ↓
  Observation (discrete micro-action)
      ↓
[Intention Recognition] ← Cognitive layer
      ↓
  BeliefState (distribution over intentions)
      ↓
[Should Replan?] ← Cognitive layer
      ↓
[Adaptive Planning] ← Cognitive layer
      ↓
  AbstractPlan (actions + execution hints)
      ↓
[Motion Planning & Execution] ← Embodiment layer
      ↓
Simulator World
```

**Key Principle:** Cognitive layer operates on **symbolic abstractions** only. It never sees simulator-specific details (Mesa grids, ROS topics, etc.).

---

## Key Design Decisions

### Decision 1: Planner Output Structure
**Question:** What does the planner output?

**Answer:** High-level abstract actions WITH optional execution hints

```python
AbstractPlan = {
    "actions": [
        {
            "type": "navigate",
            "target": "shelf_3",
            "estimated_path": [(x1,y1), (x2,y2), ...],  # OPTIONAL hints
            "estimated_time": 5.0,
            "spatial_constraints": {"avoid": "zone_A"}
        }
    ]
}
```

**Rationale:**
- Mesa uses `estimated_path` directly as microactions (trusts planner)
- ROS uses `target` + `constraints`, computes real path with motion planner
- Planner can suggest without forcing implementation

### Decision 2: WorldState Representation
**Question:** Simulator-specific or abstract?

**Answer:** Symbolic state, built by simulators, consumed by core

```python
WorldState = {
    "robot_zone": "corridor",
    "human_zone": "shelf_3",
    "item_A_location": "shelf_2",
    "robot_holding": None,
    "predicates": {"path_clear", "human_moving_north"}
}
```

**Rationale:**
- Core planner reasons about symbolic state (not geometry)
- Simulators maintain detailed world (Mesa grid, ROS TF frames)
- Simulators translate to symbolic for core consumption

### Decision 3: Replanning Trigger Logic
**Question:** Who decides WHEN to replan?

**Answer:** Hybrid - simulators schedule calls, core defines logic

**Flow:**
1. Simulator controls **frequency** of IR calls (Mesa: every step, ROS: 1Hz)
2. IR updates belief, reports **magnitude of change**
3. Core `should_replan()` function decides if change warrants replanning
4. Simulator decides whether to execute replan immediately

**Rationale:**
- Simulators know their timing constraints
- Core knows what constitutes significant belief divergence
- Clean separation of concerns

### Decision 4: ROS Micro-action Classification
**Question:** How does ROS convert noisy sensors to discrete micro-actions?

**Answer:** ROS responsibility, not core's problem

**Implementation:** `ros_sim/microaction_classifier_ros.py`
- Rule-based heuristics (e.g., "if moving toward shelf → 'move_to_shelf'")
- OR ML classifier
- OR hybrid approach
- Core IR only receives discrete `Observation(detected_microaction="...")`

**Rationale:**
- DAI formalization assumes discrete observable micro-actions μ
- Both Mesa and ROS must provide discrete μ to IR
- HOW they obtain μ is their internal concern

---

## Project Structure

```
teamrob_intrec/
│
├── README.md                         # This file
├── requirements.txt
│
├── shared/                           # Cognitive layer ("mind")
│   ├── __init__.py
│   ├── types.py                      # Dataclasses: Observation, BeliefState, Plan, WorldState
│   ├── recognizer.py                 # IntentionRecognizer class (Bayesian IR)
│   ├── planner.py                    # AdaptivePlanner class (cost-based planning)
│   ├── replanning.py                 # should_replan() + divergence metrics
│   ├── knowledge.py                  # TaskSchemas, decomposition trees, domain model
│   ├── utils.py                      # [Optional] Helper functions
│   └── io_contracts.md               # Interface specifications
│
├── configs/                          # YAML configuration files
│   ├── tasks.yaml                    # Task definitions, decomposition τ→a→μ
│   ├── scenarios.yaml                # Initial conditions, agent roles
│   └── costs.yaml                    # Cost model parameters
│
├── mesa_sim/                         # Mesa simulator ("body 1")
│   ├── __init__.py
│   ├── run_mesa.py                   # Entry point (CLI + Solara viz)
│   ├── model.py                      # Mesa Model + environment objects
│   ├── agents.py                     # HumanAgent + RobotAgent
│   ├── obs_builder.py                # Mesa world → shared.Observation
│   ├── world_state_builder.py        # Mesa snapshot → shared.WorldState
│   ├── microactions.py               # AbstractPlan → Mesa microactions
│   └── executor.py                   # Microaction execution in Mesa
│
├── ros_sim/                          # ROS simulator ("body 2")
│   ├── README.md                     # ROS setup instructions
│   ├── run_ros.py                    # Entry point
│   ├── robot_agent_node.py           # Main ROS node
│   ├── obs_builder_ros.py            # ROS topics → shared.Observation
│   ├── world_state_builder_ros.py    # ROS TF/costmap → shared.WorldState
│   ├── microaction_classifier_ros.py # Sensor fusion → discrete μ labels
│   └── goal_executor_ros.py          # AbstractPlan → ROS action goals
│
├── tests/                            # [Recommended]
│   ├── test_recognizer.py
│   ├── test_planner.py
│   └── test_integration.py
│
└── docs/
    ├── architecture.md               # Detailed architecture notes
    └── design_notes.md               # Additional design rationale
```

### Import Rules (Critical)

✅ **ALLOWED:**
- `mesa_sim/` imports from `shared/`
- `ros_sim/` imports from `shared/`

❌ **FORBIDDEN:**
- `shared/` NEVER imports from `mesa_sim/` or `ros_sim/`
- `mesa_sim/` and `ros_sim/` don't know about each other

**Enforcement:** No simulator-specific code in `shared/`. Core algorithms must work with abstract types only.

---

## Component Specifications

### shared/types.py

**Purpose:** Define all data structures for communication between cognitive and embodiment layers.

**Key Classes:**
```python
@dataclass
class Observation:
    """Discrete observation of human behavior"""
    detected_microaction: str           # e.g., "move_to_shelf_3"
    spatial_context: SpatialContext
    action_context: ActionContext
    timestamp: float

@dataclass
class SpatialContext:
    position: Tuple[float, float]
    orientation: float
    zone: Optional[str]

@dataclass
class ActionContext:
    detected_microaction: str
    target_object: Optional[str]
    progress: float  # 0.0-1.0

@dataclass
class BeliefState:
    """Distribution over human intentions"""
    distribution: Dict[str, float]      # {task_id: probability}
    predicted_actions: Dict[str, List[str]]  # {task_id: [next_actions]}
    confidence: float
    timestamp: float

@dataclass
class WorldState:
    """Symbolic representation of environment"""
    agent_states: Dict[str, AgentState]
    object_locations: Dict[str, str]
    predicates: Set[str]  # "robot_at_shelf", "path_clear", etc.

@dataclass
class AbstractPlan:
    """High-level plan with execution hints"""
    goal_intention: str
    actions: List[AbstractAction]
    estimated_total_cost: float

@dataclass
class AbstractAction:
    action_type: str  # "navigate", "pick", "place", "wait"
    parameters: Dict[str, Any]
    
    # Execution hints (optional, for simulator use)
    estimated_path: Optional[List[Tuple[float, float]]]
    estimated_duration: float
    spatial_constraints: Dict[str, Any]
    temporal_constraints: Dict[str, Any]
```

---

### shared/recognizer.py

**Purpose:** Bayesian intention recognition

**Interface:**
```python
class IntentionRecognizer:
    def __init__(self, task_schemas: TaskSchemas, context_model: ContextModel):
        """Initialize with domain knowledge"""
        
    def update(self, observation: Observation) -> BeliefState:
        """
        INPUT: Observation (discrete micro-action + context)
        OUTPUT: BeliefState (distribution over intentions)
        
        DOES:
        1. Generate hypotheses from observation (tree matching)
        2. Compute likelihoods P(obs | intention)
        3. Apply Bayesian update with priors and context weights
        4. Predict next actions for each hypothesis
        """
```

**Key Algorithm:** `P(τ|μ_t) ∝ P(μ_t|τ) · P(τ) · ω_context(τ)`

---

### shared/planner.py

**Purpose:** Intention-aware adaptive planning

**Interface:**
```python
class AdaptivePlanner:
    def __init__(self, task_schemas: TaskSchemas, cost_model: CostModel):
        """Initialize with domain knowledge"""
        
    def plan(self, 
             my_intention: str,
             other_belief: BeliefState,
             world_state: WorldState) -> AbstractPlan:
        """
        INPUT:
        - my_intention: Robot's assigned task
        - other_belief: Current belief about human intentions
        - world_state: Symbolic environment state
        
        OUTPUT: AbstractPlan with actions + execution hints
        
        DOES:
        1. Decompose my_intention into candidate action sequences
        2. Predict human actions from other_belief
        3. Compute execution costs + cancellation costs
        4. Check feasibility (spatial-temporal conflicts)
        5. Select lowest-cost feasible plan
        6. Generate execution hints (path, timing, constraints)
        """
```

---

### shared/replanning.py

**Purpose:** Determine when replanning is needed

**Interface:**
```python
def should_replan(current_plan: AbstractPlan,
                  previous_belief: BeliefState,
                  new_belief: BeliefState,
                  world_state: WorldState) -> bool:
    """
    INPUT: Current plan, previous/new beliefs, world state
    OUTPUT: Boolean (replan needed?)
    
    LOGIC:
    1. Check belief divergence: KL-divergence or max probability shift
    2. Check plan feasibility: preconditions still satisfied?
    3. Check cost delta: is current plan now too expensive?
    
    RETURN: True if any trigger condition met
    """
```

---

### mesa_sim/agents.py

**Purpose:** Mesa agent implementations

**RobotAgent responsibilities:**
1. Own instances of `IntentionRecognizer` and `AdaptivePlanner`
2. Observe human agent each step
3. Build `Observation` via `obs_builder.py`
4. Update belief via `recognizer.update()`
5. Check `should_replan()`
6. Generate plan via `planner.plan()`
7. Discretize to microactions via `microactions.py`
8. Execute via `executor.py`

**HumanAgent responsibilities:**
1. Execute assigned or foreseeable tasks
2. Provide ground truth for IR evaluation
3. Generate observable microactions

---

### ros_sim/robot_agent_node.py

**Purpose:** ROS node implementing robot agent architecture

**Key differences from Mesa:**
- Asynchronous observation callbacks
- Periodic deliberation loop (e.g., 1Hz)
- Continuous low-level control (action servers)
- Must aggregate sensor streams into discrete observations

**Structure:**
```python
class RobotAgentNode:
    def __init__(self):
        # Cognitive components (from shared/)
        self.ir = IntentionRecognizer(...)
        self.planner = AdaptivePlanner(...)
        
        # ROS-specific
        self.observation_buffer = []
        rospy.Subscriber("/human_pose", PoseStamped, self.pose_callback)
        rospy.Timer(rospy.Duration(1.0), self.deliberation_callback)
        
    def pose_callback(self, msg):
        """Buffer observations"""
        
    def deliberation_callback(self, event):
        """Periodic IR + planning"""
```

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1)
**Goal:** Establish project structure and core types

**Tasks:**
1. Create repository with folder structure
2. Define `shared/types.py` (all dataclasses)
3. Write `shared/io_contracts.md` (interface specs)
4. Set up `configs/tasks.yaml` (from current implementation)
5. Write `README.md` (this document)

**Validation:** Can import types, load configs

---

### Phase 2: Extract Core Algorithms (Week 2)
**Goal:** Port IR and Planning to `shared/`

**Tasks:**
1. Extract Bayesian IR logic → `shared/recognizer.py`
   - Pull from current `intention_recognition.py`
   - Remove Mesa dependencies
   - Use only `shared/types.py`
   
2. Extract planning logic → `shared/planner.py`
   - Pull from current `planner.py`
   - Remove Mesa dependencies
   - Output `AbstractPlan` instead of microactions
   
3. Extract replanning triggers → `shared/replanning.py`
   
4. Write unit tests in `tests/`
   - Test IR with mock observations
   - Test planner with mock world states

**Validation:** Core algorithms work independently of simulators

---

### Phase 3: Build Mesa Embodiment (Week 3)
**Goal:** Reimplemented Mesa simulation using shared core

**Tasks:**
1. Port Mesa model → `mesa_sim/model.py`
   - Copy environment objects (shelves, stations)
   - Set up scheduler and space
   
2. Implement translation layer:
   - `mesa_sim/obs_builder.py`: Mesa → Observation
   - `mesa_sim/world_state_builder.py`: Mesa → WorldState
   - `mesa_sim/microactions.py`: AbstractPlan → microactions
   
3. Implement `mesa_sim/agents.py`:
   - RobotAgent uses `shared/recognizer.py` and `shared/planner.py`
   - HumanAgent executes scripted tasks
   
4. Wire up execution:
   - `mesa_sim/executor.py`: Execute microactions
   - `mesa_sim/run_mesa.py`: Entry point + visualization

**Validation:** Run simple scenario, compare to old implementation

---

### Phase 4: Validate & Iterate (Week 4)
**Goal:** Ensure new implementation matches old behavior

**Tasks:**
1. Run test scenarios from paper
2. Compare IR accuracy (new vs old)
3. Compare planning decisions
4. Fix discrepancies
5. Document differences (if any are intentional improvements)

**Validation:** New framework produces equivalent (or better) results

---

### Phase 5: ROS Integration (Parallel, ROS team)
**Goal:** Enable real-world deployment

**Tasks (ROS team):**
1. Set up ROS workspace with `shared/` in Python path
2. Implement `ros_sim/microaction_classifier_ros.py`
3. Implement translation layers (obs, world_state, goals)
4. Build `robot_agent_node.py`
5. Test with robot

**Your role:** Provide API documentation, example usage, support

---

## Migration Guide

### From Current Codebase to New Structure

**Current problematic patterns:**
- Mesa Model contains IR logic
- Robot agent owns planner directly
- WorldStateManager hardcoded to Mesa types
- Microactions mixed with high-level planning

**Migration checklist:**

#### Step 1: Inventory Current Code
Create a mapping document:
```
Current file → New location(s)

intention_recognition.py → shared/recognizer.py
planner.py → shared/planner.py + mesa_sim/microactions.py
executor.py → mesa_sim/executor.py
world_state_manager.py → mesa_sim/world_state_builder.py
factory_model.py → mesa_sim/model.py
robot_agent.py → mesa_sim/agents.py (RobotAgent class)
```

#### Step 2: Extract Shared Logic
For each file in current codebase:
1. Identify simulator-independent logic
2. Extract to `shared/`
3. Replace Mesa-specific types with `shared/types.py`
4. Add unit tests

#### Step 3: Build Translation Layers
For remaining Mesa-specific code:
1. Move to `mesa_sim/`
2. Implement builder pattern (Mesa world → shared types)
3. Keep Mesa complexity in `mesa_sim/`, not `shared/`

#### Step 4: Rewire Agents
Update robot agent to:
1. Import from `shared/` not local modules
2. Use builders to create `Observation` and `WorldState`
3. Call `should_replan()` instead of custom logic
4. Translate `AbstractPlan` to microactions

---

## Resolved Design Questions

### Q1: Do observations need to be identical in Mesa and ROS?
**Answer:** No, but both must provide discrete micro-actions.

**Mesa:** Perfect observation, knows exact micro-action  
**ROS:** Inferred from noisy sensors, classified to discrete label  
**Core IR:** Receives discrete micro-action label in both cases

---

### Q2: Does core planner know about microactions?
**Answer:** Planner can SUGGEST microactions, but doesn't require them.

**For Mesa:** Planner's suggested path used directly  
**For ROS:** Planner's spatial/temporal constraints used, real path computed by ROS  
**Core planner:** Outputs both suggestions and constraints

---

### Q3: Who decides WHEN to call IR?
**Answer:** Simulators decide timing, core defines significance.

**Mesa:** Calls IR every step (synchronous)  
**ROS:** Calls IR at deliberation rate (e.g., 1Hz)  
**Core:** `should_replan()` says whether change warrants action

---

### Q4: Is WorldState simulator-specific?
**Answer:** No, it's symbolic and simulator-agnostic.

**Mesa:** Maintains detailed grid world, translates to symbolic  
**ROS:** Maintains TF frames and costmaps, translates to symbolic  
**Core:** Only sees symbolic predicates (no geometry)

---

### Q5: How does ROS handle step-based formalization?
**Answer:** ROS discretizes continuous observations into windows.

**Implementation:** Buffer sensor data, sample at regular intervals (e.g., 1Hz), aggregate into single discrete observation per window

**Key insight:** Core IR doesn't care about update frequency, only that observations are discrete

---

### Q6: Should we use pip install / packaging?
**Answer:** No, keep simple for research code.

**Approach:** Direct imports via `sys.path` or `PYTHONPATH`  
**Rationale:** Avoids packaging overhead, easier to modify during development

---

### Q7: Do we need adapter/translation layers?
**Answer:** Yes, but keep them simple - just builder functions.

**Not:** Complex adapter pattern with interfaces  
**Instead:** Simple functions that build `shared/types` from simulator data

---

## Usage Examples

### Mesa Simulation

```python
# mesa_sim/run_mesa.py
from shared.recognizer import IntentionRecognizer
from shared.planner import AdaptivePlanner
from shared.knowledge import load_task_schemas
from mesa_sim.model import FactoryModel

# Load domain knowledge
task_schemas = load_task_schemas("configs/tasks.yaml")

# Create Mesa model
model = FactoryModel(
    width=500,
    height=500,
    task_schemas=task_schemas
)

# Run simulation
for i in range(100):
    model.step()
```

### Robot Agent Step

```python
# mesa_sim/agents.py (RobotAgent.step method)
def step(self):
    # 1. Observe human
    human = self.model.get_human_agent()
    obs = ObservationBuilder.from_mesa(self.model, human)
    
    # 2. Update belief (shared/)
    belief = self.ir.update(obs)
    
    # 3. Check replanning (shared/)
    world_state = WorldStateBuilder.from_mesa(self.model)
    
    if should_replan(self.current_plan, self.prev_belief, belief, world_state):
        # 4. Plan (shared/)
        plan = self.planner.plan(
            my_intention=self.assigned_task,
            other_belief=belief,
            world_state=world_state
        )
        
        # 5. Discretize (Mesa-specific)
        self.microactions = MicroactionBuilder.from_plan(plan, self.model)
    
    # 6. Execute (Mesa-specific)
    if self.microactions:
        self.executor.execute(self.microactions.pop(0))
```

---

## Development Workflow

### Adding New Features

**To modify IR algorithm:**
1. Edit `shared/recognizer.py`
2. Update unit tests in `tests/test_recognizer.py`
3. Both Mesa and ROS benefit automatically

**To add new task:**
1. Edit `configs/tasks.yaml`
2. Add decomposition tree
3. Both simulators load automatically

**To modify Mesa visualization:**
1. Edit `mesa_sim/run_mesa.py` only
2. Core logic unchanged

**To change ROS sensors:**
1. Edit `ros_sim/microaction_classifier_ros.py` only
2. Core logic unchanged

### Testing Strategy

**Unit tests** (`tests/shared/`):
- Test IR with synthetic observations
- Test planner with mock world states
- Fast, no simulation overhead

**Integration tests** (`tests/`):
- Test Mesa translation layers
- Test end-to-end Mesa scenarios

**Manual validation**:
- Run Mesa visualization
- Compare to ground truth (human intentions known)

---

## Common Pitfalls to Avoid

❌ **Importing Mesa types in `shared/`**  
→ Breaks simulator independence

❌ **Putting simulator logic in core algorithms**  
→ "If Mesa then X else Y" = wrong abstraction

❌ **Making WorldState too detailed**  
→ Keep symbolic, not geometric

❌ **Hardcoding microactions in planner**  
→ Planner suggests, simulators decide

❌ **Mixing observation and inference**  
→ Observation is data, IR is algorithm

---

## Contact & Collaboration

**Mesa development:** Your responsibility  
**ROS development:** ROS team (parallel)  
**Joint development:** `shared/planner.py` (collaborative)

**When starting new chat:**
1. Reference this document
2. Specify which component you're working on
3. Mention any deviations from this design

---

## Version History

**v1.0** (Current) - Initial design document  
- All 4 key decisions finalized
- Project structure defined
- Implementation roadmap established

---

**Next Steps:** Begin Phase 1 (Foundation) - Create `shared/types.py`
