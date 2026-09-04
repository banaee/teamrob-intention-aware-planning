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
- **Meta-Planning** — task selection, interference detection, cost comparison; decides *which*
  task the robot does next and *when* to re-decide
- **Adaptive Planning** — HTN decomposition of a single task into grounded actions
- **Trajectory Algorithms** — pluggable path-realization and interference-detection functions
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

Currently implemented: `domains/kitting/` (industrial kitting), `domains/dock_loading/`
(truck unloading, modeled on HITS3 Scenario 2)

---

## The Cognitive Loop

Each step, the robot agent runs:

```
obs_builder → recognizer → meta_planner → planner → executor
```

1. **`obs_builder`** turns simulator state into an `Observation` of the human
2. **`recognizer`** updates a Bayesian belief over human task hypotheses
3. **`meta_planner`** decides whether to re-evaluate, and if so, which task to do next
4. **`planner`** decomposes that task into a flat sequence of grounded actions
5. **`executor`** runs one microaction

Steps 3–4 only recompute when a cognitive-clock event fires — task completion, a belief
confidence threshold crossing, or the robot committing to a task by picking something up.

---

## Key Design Decisions

- **HTN-aligned representation**: tasks decompose to tasks or primitive actions; primitive actions are the leaves executed by the embodiment layer
- **Bidirectional tree**: same decomposition structure used top-down for planning and bottom-up for intention recognition
- **No string parsing**: all knowledge represented as typed Python dataclasses (`Var`, `Const`, `Predicate`, `TaskSchema`, `ActionSchema`)
- **Predicate semantics**: `at(agent, object)` for executor completion checking; `in_zone(agent, zone)` for IR context reasoning — kept strictly separate
- **Intention recognition drives task selection**: the robot observes human microactions, updates a Bayesian belief over task hypotheses, and re-selects its next task when that belief or the world changes
- **Receding-horizon selection**: the robot picks the single best *next* task at each cognitive event rather than committing to an ordering of everything remaining — decisions are re-made as the picture of the human improves
- **Plans are re-decomposed, never resumed**: there is no plan cursor; the world state is the record of progress, and HTN method guards encode what remains to be done from the current state

Full rationale for each is in `docs/design_decisions.md`.

---

## Pre-Requisites

Using Python 3.10+, and virtual environments (in the example below: `venv`) for dependency management.

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
python mesa_sim/run_mesa.py --scenario scenario_00 --steps 200
python mesa_sim/run_mesa.py --domain dock_loading --layout env_layout1 --scenario scenario_10
```

Logs are written to `logs/run_<timestamp>.log` as well as stdout.

### Visualization (Solara)

```bash
solara run mesa_sim/run_mesa.py
```

---

## Running the ROS Simulation

Todo: instructions for ROS embodiment once implemented.
See `ros_sim/ros_sim_guideline_v2.md` for the integration contract and constraints.

---

## Repository Structure

```
teamrob-intention-aware-planning/
├── shared/                      # Cognitive layer — simulator-agnostic
│   ├── types.py                    # Canonical dataclasses
│   ├── domain_knowledge.py         # DomainKnowledgeBase interface
│   ├── recognizer.py               # Intention recognition (Bayesian)
│   ├── likelihood_functions.py     # Pure likelihood math, registry-dispatched
│   ├── meta_planner.py             # Task selection, interference detection, cost
│   ├── trajectory_algorithms.py    # Path realization + interference algorithms
│   ├── planner.py                  # Adaptive planner (HTN decomposition)
│   └── io_contracts.md             # Interface specifications
│
├── domains/                     # Domain-specific knowledge (Python)
│   ├── kitting/
│   │   ├── actions.py              # HTN primitive tasks
│   │   ├── tasks.py                # HTN non-primitive tasks
│   │   ├── registry.py             # DomainModel construction
│   │   ├── scenarios.py            # Scenario definitions
│   │   ├── env_layout0.json        # Environment spatial layout
│   │   └── env_layout1.json
│   └── dock_loading/               # Same structure
│
├── mesa_sim/                    # Mesa embodiment layer
│   ├── sim_model.py                # SimModel (Mesa world + object loading)
│   ├── sim_agents.py               # HumanAgent, RobotAgent
│   ├── world_state_builder.py      # Mesa → WorldState translation
│   ├── obs_builder.py              # Mesa → Observation translation
│   ├── action_decomposer.py        # GroundedAction → microaction expansion
│   ├── executor.py                 # Microaction execution engine
│   ├── viz/                        # Solara + Plotly visualization
│   ├── mesa_fork/                  # Vendored Mesa 3.0 fork
│   ├── run_mesa.py                 # Entry point
│   └── mesa_configs.yaml           # Mesa-specific settings
│
├── ros_sim/                     # ROS embodiment (planned)
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
| Dock loading domain (`domains/dock_loading/`) | ✅ Complete (open items, see docs) |
| Mesa simulation loop | ✅ Running |
| Mesa visualization (Solara) | ✅ Running |
| Bayesian IR (`shared/recognizer.py`) | ✅ Complete (Phase 4A) |
| HTN decomposition (`shared/planner.py`) | ✅ Complete (Phase 4B) |
| Meta-planner (`shared/meta_planner.py`) | ✅ Complete (Phase 4C, single-task selection) |
| Trajectory algorithms (`shared/trajectory_algorithms.py`) | ✅ Complete (straight-line + sampled interference) |
| Full queue reordering | 🔲 Deferred — see `docs/TODOS_AND_DEFERRED.md`, DESIGN-16 |
| Obstacle-aware path planning | 🔲 Phase 4D |
| Evaluation & experiments | 🔲 Phase 5 |
| ROS embodiment | 🔲 Phase 6 |

---

## Documentation

| File | Contents |
|---|---|
| `shared/io_contracts.md` | Canonical types and module interfaces — the authoritative API contract |
| `docs/design_decisions.md` | *Why* the architecture is shaped the way it is |
| `docs/roadmap.md` | Phase-by-phase implementation plan and status |
| `docs/TODOS_AND_DEFERRED.md` | Open bugs, technical debt, and deliberately deferred design questions |
| `ros_sim/ros_sim_guideline_v2.md` | Integration contract and constraints for the ROS embodiment |
