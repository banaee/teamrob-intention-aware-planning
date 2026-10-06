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
- **Scenarios** — typed agent assignments and task instances; each declares its setup and its reference layouts
- **Layouts and setups** — JSON files: the room (space, areas, fixed objects) and the shift (movable objects, home containers, designated destinations); a run is the triple (layout, setup, scenario)

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
- **Predicate semantics**: `at(agent, object)` for executor completion checking; `in_area(agent, area)` for IR context reasoning — kept strictly separate
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

Each start has its own command; there is no single start command with subcommands (T-viz, TODO-196). Run them from the
repository's root, with the hash seed fixed (`PYTHONHASHSEED=0`) wherever a run must repeat.

### Headless (default)

```bash
python mesa_sim/run_mesa.py
python mesa_sim/run_mesa.py --scenario scenario_s01_01 --steps 200
python mesa_sim/run_mesa.py --domain dock_loading --scenario scenario_s01_01
```

`--layout` is optional: a run that names none takes the scenario's first reference layout.

Logs are written to `logs/run_<timestamp>.log` (and the human executor's record to `logs/run_<timestamp>.rec`) as
well as the terminal: one pair per sim-run, written from its first step (`mesa_sim/sim_run.py`).

### Visualization (Solara): the solara-ui

```bash
solara run mesa_sim/run_mesa.py
solara run mesa_sim/run_mesa.py -- --domain kitting --scenario scenario_s01_01   # the start's own flags after --
```

### The web-ui (T-viz)

The framework's own page in the browser and a small Python server (stage 1a, increment (i)): choose a sim-run, then
play, pause, step and reset it, and watch the env-pane. The page is built once with Node.js 22.12 or later (every
dependency pinned in `webui/page/package.json` and its lock file), and again after a change of the page's sources; the
start stops and says so when the built page is missing or older than its sources.

```bash
cd webui/page && npm ci && npm run build && cd ../..                    # once, and after a change of the page
PYTHONHASHSEED=0 python mesa_sim/run_webui.py                           # then open http://127.0.0.1:8000/
PYTHONHASHSEED=0 python mesa_sim/run_webui.py --domain dock_loading --scenario scenario_s08_01 --steps 300 --port 8001
```

The start takes the headless start's run file and flags, and `--port`. It opens on the run file's sim-run at its start.
The web-ui has no step limit unless `--steps` (or, from increment (ii), the page) sets one; the run file's `steps` is
not used. A sim-run's log pair is the one the same sim-run writes headless; Ctrl+C stops the server and ends a stepped
sim-run. More in `webui/page/README.md`; the state of the web-ui's work in `docs/handoffs/handoff_T-viz.md`, "State after
stage 0", and the plan of stage 1a in `docs/handoffs/plan_T-viz_1a.md`.

### Layout drawings

`scripts/layout_tool.py` draws a layout as a PNG and derives a new layout by dragging its fixed objects: `scripts/README.md`.

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
│   ├── discovery.py                # Registration by discovery (T-L stage 2)
│   ├── kitting/
│   │   ├── actions.py              # HTN primitive tasks
│   │   ├── tasks.py                # HTN non-primitive tasks
│   │   ├── registry.py             # Tree construction; discovers layouts, setups, scenarios
│   │   ├── scenarios/              # Scenario definitions — one module per setup (scenarios_sNN.py)
│   │   ├── layouts/                # The layouts — the room (env_layout_01.json, ...)
│   │   └── setups/                 # The setups — the shift (env_setup_01.json, ...)
│   └── dock_loading/               # Same structure
│
├── mesa_sim/                    # Mesa embodiment layer
│   ├── sim_model.py                # SimModel (Mesa world + object loading)
│   ├── sim_agents.py               # HumanAgent, RobotAgent
│   ├── world_state_builder.py      # Mesa → WorldState translation
│   ├── obs_builder.py              # Mesa → Observation translation
│   ├── action_decomposer.py        # GroundedAction → microaction expansion
│   ├── executor.py                 # Microaction execution engine
│   ├── viz/                        # Solara + Plotly visualization (the solara-ui; solara_page.py its page)
│   ├── mesa_fork/                  # Vendored Mesa 3.0 fork
│   ├── run_config.py               # The run configuration (run file, flags) and the model built from it
│   ├── sim_run.py                  # One sim-run: the model stepped, its log pair and run-level lines
│   ├── run_mesa.py                 # Entry point: the headless start and the solara-ui's start
│   ├── run_webui.py                # Entry point: the web-ui's start
│   ├── webui_adapter.py            # Mesa's piece for the web-ui: the messages from a sim-run
│   └── mesa_configs.yaml           # Mesa-specific settings
│
├── webui/                       # The web-ui (T-viz): messages, the simulator interface, the scene appearance, the server, the page
│   └── page/                       # The page: React, TypeScript, Vite, three.js through React Three Fiber
│
├── ros_sim/                     # ROS embodiment (planned)
├── configs/                     # Cross-domain config (costs.yaml)
├── docs/                        # Design documentation
└── scripts/                     # Utility scripts (layout_tool.py: layout drawings and editor)
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
