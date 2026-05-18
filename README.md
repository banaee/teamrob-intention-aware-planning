# TeamRob Intention-Aware Planning Framework

A simulation-agnostic robot cognitive architecture for human-robot teaming in industrial scenarios.
The framework enables robots to infer human intentions through hierarchical Bayesian reasoning
and adapt their plans proactively.

Part of the Swedish Knowledge Foundation's **TeamRob Synergy Project**, in collaboration with Scania.

---

## Architecture

The framework enforces a strict **mind/body separation**:

### Cognitive Layer (`shared/`)

Simulator-agnostic pure Python. Contains:

- **Intention Recognition** — Bayesian inference over human task hypotheses
- **Adaptive Planning** — HTN-style grounded action generation
- **Replanning** — trigger logic for plan revision
- **Domain Knowledge** — typed task/action schemas, inspectable decomposition trees
- **Canonical Types** — `Observation`, `BeliefState`, `WorldState`, `AbstractPlan`, `GroundedAction`

The cognitive layer never imports from any simulator.

### Embodiment Layers

Simulator-specific implementations that translate between physical world and symbolic layer:

- `mesa_sim/` — discrete step-based simulation (Mesa 3.0)
- `ros_sim/` — real-world deployment (planned)

Each embodiment provides: observation building, world state building, and action execution.
The cognitive layer is called by the embodiment — it never runs its own loop.

### Domain Knowledge (`domains/`)

Domain-specific task and action definitions in typed Python — no YAML parsing.
Each domain defines:

- **Action schemas** — HTN primitive tasks (directly executable)
- **Task schemas** — HTN non-primitive tasks (decompose via methods)
- **Scenarios** — typed agent assignments and task instances
- **Environment layout** — JSON spatial configuration

Currently implemented: `domains/kitting/` (industrial kitting scenario)

---

## Key Design Decisions

- **HTN-aligned representation**: tasks decompose to tasks or primitive actions; primitive actions are the leaves executed by the embodiment layer
- **Bidirectional tree**: same decomposition structure used top-down for planning and bottom-up for intention recognition
- **No string parsing**: all knowledge represented as typed Python dataclasses (`Var`, `Const`, `Predicate`, `TaskSchema`, `ActionSchema`)
- **Predicate semantics**: `at(agent, object)` for executor completion checking; `in_zone(agent, zone)` for IR context reasoning — kept strictly separate
- **Intention recognition drives replanning**: robot observes human microactions, updates Bayesian belief over task hypotheses, replans when belief diverges from current plan assumptions

---

## Pre-Requisites

Using Python 3.10+, and vistual environments (in the example below: `venv`) for dependency management.

```bash
python3 -m venv ~/python-envs/tr-env
source ~/python-envs/tr-env/bin/activate
pip install -r requirements.txt
```

The Mesa fork is included directly at `mesa_sim/mesa_fork/` — no separate installation needed.

Use any IDE (e.g., [VS Code](https://code.visualstudio.com/)) or editor of your choice to explore the codebase. The cognitive layer is in `shared/`, domain knowledge in `domains/`, and the Mesa embodiment in `mesa_sim/`.


---

## Running the MESA Simulation

### Headless (default)

```bash
python mesa_sim/run_mesa.py
python mesa_sim/run_mesa.py --scenario scenario_11 --steps 200
```

### Visualization (Solara)

```bash
solara run mesa_sim/run_mesa.py
```

---

## Running the ROS Simulation

Todo: instructions for ROS embodiment once implemented.

---

## Repository Structure

```
teamrob-intention-aware-planning/
├── shared/                      # Cognitive layer — simulator-agnostic
│   ├── types.py                    # Canonical dataclasses
│   ├── domain_knowledge.py         # DomainKnowledgeBase interface
│   ├── recognizer.py               # Intention recognition (Bayesian)
│   ├── planner.py                  # Adaptive planner (HTN grounding)
│   ├── replanning.py               # Replanning trigger logic
│   └── io_contracts.md             # Interface specifications
│
├── domains/                     # Domain-specific knowledge (Python)
│   └── kitting/
│       ├── ActionSchemas.py      # HTN primitive tasks
│       ├── tasks.py                # HTN non-primitive tasks
│       ├── registry.py             # DomainModel construction
│       ├── scenarios.py            # Scenario definitions
│       └── env1_layout.json        # Environment spatial layout
│
├── mesa_sim/                    # Mesa embodiment layer
│   ├── sim_model.py                # SimModel (Mesa)   --- > WorldState translation
│   ├── sim_agents.py               # HumanAgent, RobotAgent
│   ├── world_state_builder.py      # Mesa → WorldState translation
│   ├── obs_builder.py              # Mesa → Observation translation
│   ├── action_decomposer.py        # GroundedAction → microaction expansion
│   ├── executor.py                 # Microaction execution engine
│   ├── run_mesa.py                 # Entry point
│   └── mesa_configs.yaml           # Mesa-specific settings
│
├── ros_sim/                     # ROS embodiment (planned)
│   ├── ...                         # ...
├── configs/                     # Cross-domain config (costs.yaml)
├── docs/                        # Design documentation
└── scripts/                     # Utility scripts
```

---

## Implementation Status

| Component | Status |
|---|---|
| Canonical types (`shared/types.py`) | ✅ Complete |
| Domain knowledge (`shared/domain_knowledge.py`) | ✅ Complete |
| Kitting domain (`domains/kitting/`) | ✅ Complete |
| Planner skeleton (`shared/planner.py`) | ✅ Skeleton |
| Recognizer skeleton (`shared/recognizer.py`) | ✅ Skeleton (uniform prior) |
| Replanning skeleton (`shared/replanning.py`) | ✅ Skeleton |
| Mesa simulation loop | ✅ Running |
| Bayesian IR algorithm | 🔄 Phase 4 |
| Cost-based planning | 🔄 Phase 4 |
| Guard evaluation | 🔄 Phase 4 |
| ROS embodiment | 🔄 Future |
