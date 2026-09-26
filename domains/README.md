# Adding a New Domain

This folder contains one sub-package per case study domain.
Each domain is self-contained: tasks, actions, scenarios, environment layout, and a registry that wires them together.

```
domains/
    kitting/          ← reference implementation (fully filled)
    dock_delivery_loading/      ← skeleton ready to be filled
    <your_domain>/    ← copy the skeleton, fill it in
```

The `kitting/` domain is the authoritative reference. When in doubt, look there first.

---

## 1. Folder structure

Each domain package contains the same files:

```
domains/<your_domain>/
    __init__.py
    tasks.py            # TaskSchema definitions  — HTN compound tasks
    actions.py          # ActionSchema defs     — HTN primitive actions (leaves)
    registry.py         # builds the Tree, declares the task model; discovers
                        # layouts, setups and scenarios (domain_config)
    scenarios/          # a package (T-L stage 2): one module per setup,
                        # scenarios_sNN.py — every scenario whose setup is
                        # env_setup_NN and no other
    script.py           # the call forms the scenarios are written in (kitting)
    layouts/            # the layout files — the room (one file per layout)
    setups/             # the setup files — the shift (one file per setup,
                        # env_setup_NN.json; the file stem is the id)
```

Registration is by discovery (`domains/discovery.py`, T-L stage 2): layouts and setups by
the files in their folders, scenarios by a module scan of the scenarios package at import
of `domains.<domain>.registry`. No hand-written list; a duplicate scenario id is an error
at import. The serial in a module's name repeats its scenarios' validated `setup` field —
an authoring convention the code does not check.

---

## 2. The three artefacts of a run (T-L; docs/glossary.md §9)

A run is a triple (layout, setup, scenario) plus the run options.

**Layout — the room** (`layouts/env_layout<N>.json`): the space, its zones, and the fixed objects
with their positions (tables, shelves, machines, switches, landmarks; a fixed container
such as a truck belongs here too). No movable object and no agent. Coordinates use a
center-origin system `(0,0)` that matches the simulator grid directly. Zones use the
convention `zone_<descriptor>`. Top-level keys: `"space"`, `"zones"`, `"env_objects"`.
Every fixed object has a `"position"` and never an `"initial_container"`.

**Setup — the shift** (`setups/env_setup_NN.json`; the final serial ids since T-L stage 2,
which merged the content-identical env_setup3 into env_setup_01 and env_setup5 into
env_setup_03): the movable objects that exist, in one
`"env_objects"` list. Each entry has an `"initial_container"` (its home container, an
object of the layout), a `"destination"` where the domain determines one through
`destination_of` (kitting: the item's designated table), and any other per-object state
the domain declares (dock_loading: `subtype`, `is_empty`, `is_scanned`). A different
designation set is a different setup.

**Scenario — the episode** (`scenarios/scenarios_sNN.py`, its setup's module): per agent its `start_position`,
`assigned_tasks`, `observes` and, for a human, the script; the purpose as `description`;
the one `setup` it binds; and its `reference_layouts` (one or more layout ids). A run that
names no layout takes the scenario's first reference layout; `--layout` selects another
registered layout.

The loader validates the triple at load: every home container of the setup is an object of
the layout; every designated destination is an object of the layout with the type the
schema declares; every task binding names an object of the layout or setup with the
schema's type; every assigned task agrees with the setup's designations; every
`start_position` lies inside the space's bounds. A failure names the artefact and the
mismatch.

---

## 3. Concepts: tasks, actions, microactions

The framework uses a three-level hierarchy:

- **Tasks** (`tasks.py`) — high-level goals, decomposed into ordered sequences of actions via HTN methods. These are what the IR reasons about.
- **Actions** (`actions.py`) — primitive executable steps. Each has preconditions (checked at planning time), effects (declared world changes), and a `completion` predicate the executor monitors at runtime against the `WorldState`.
- **Microactions** — atomic simulator steps (STEP, GRASP, RELEASE, STAND). Produced by the embodiment layer, not defined here.

**Two important predicate families — do not conflate them:**
- `at(agent, object)` — fine-grained object proximity, used by the executor to check action completion.
- `in_zone(agent, zone)` — coarse zone-level context, used only by IR for context weighting.

Using `at` with a zone argument (instead of an object) is a silent bug: the executor will never see the completion predicate satisfied and the agent gets stuck.

---

## 4. Defining tasks

A `TaskSchema` has a name, parameters, and one or more decomposition methods. Each method is an ordered list of action calls with parameter bindings. The planner selects the first method whose guards hold in the current `WorldState`; an empty guard list is unconditionally applicable and serves as the fallback.

Tasks come in two categories, set by flags on the schema:

- `is_assigned=True` — part of the shared team task. The robot both plans with it and uses it to recognize the human doing it.
- `is_foreseeable=True` — a predictable human behavior not part of the team task. The robot never executes it, but must recognize it to avoid misinterpreting the human's actions.

A task can carry multiple methods to support **conditional decomposition** — for example, `DELIVER_PALLET` could have a method for delivering to the dock entrance (default) and a second method for carrying the pallet inside the building (if a condition such as `receiver_requested_inside` holds in the `WorldState`). The planner picks the first applicable method. This is fully supported by the current types via `MethodSchema.guards`; see `shared/types.py`.

---

## 5. Example: pallet shop domain (from HITS3 Scenario 2)

The HITS3 study (Olivia Stener, TRATON observations, Dec 2025) describes a normal dock delivery scenario: a driver and support vehicle unload pallets from a truck onto a platform connected to a warehouse. The receiver assigns delivery spots; the driver delivers one pallet at a time.

Three tasks from this scenario translate directly into our format:

### Assigned task: `DELIVER_PALLET(?pallet, ?dest)`

The core team task. The driver (or robot) moves to the pallet, picks it up, moves to the assigned delivery spot, and places it. Decomposes to `move_to(?pallet)` → `pick_up(?pallet)` → `move_to(?dest)` → `place(?pallet, ?dest)`. Structurally identical to `DELIVER_ITEM` in kitting.

### Foreseeable task: `DRIVER_PHONE_CALL()`

Listed explicitly in HITS3 as "DriverAgent receives phone call from logistics planner." The driver stops and stands in place for the duration. Decomposes to `move_to(neutral_spot)` → `wait_at(neutral_spot)`. Same shape as `COFFEE_BREAK` in kitting. The robot distinguishes this from an assigned task because the destination does not match any known delivery spot.

### Foreseeable task: `DRIVER_TALKS_TO_DOCKWORKER()`

Listed in HITS3 as "DriverAgent stands at DockWorkerAgent and talks." Decomposes to `move_to(?dockworker)` → `wait_at(?dockworker)`. Foreseeable, no manipulation, recognizable by destination mismatch with the delivery area.

**What was not translated and why:** the receiver dynamically assigning a new delivery location requires runtime parameter mutation, outside the current `ScenarioConfig` model. Communication acts (intercom calls, pallet scanning) have no observable microaction equivalent. Interleaved loading/unloading requires unordered or parallel steps, which the current sequential `MethodSchema` does not support. These are known limitations documented in the paper.

---

## 6. registry.py — wiring

The registry assembles all tasks and actions into a `DomainModel` and declares the `intentions` set — the tasks the IR will reason over, typically all tasks. See `domains/kitting/registry.py` for the pattern.

---

## 7. scenarios/ — concrete agent assignments

A `ScenarioConfig` assigns concrete task instances to each agent, with all parameters bound to specific values; it declares its `setup` and its `reference_layouts` (section 2). The human's script is a `Script` of task instances with events (T-H). Each scenario is one hand-written literal in its setup's module (`scenarios/scenarios_sNN.py`), registered by discovery at import — no list to maintain. See `domains/kitting/scenarios/` for the pattern.

### Scenario ids

Serial ids, nothing encoded beyond order of writing (T-L, ruling 4 as amended; built in stages 2 and 3): layouts `env_layout_KK`, setups `env_setup_NN`, scenarios `scenario_sNN_MM`, NN the serial of the scenario's `setup` and MM a counter per setup (`scenario_s01_06` is the sixth scenario of `scenarios_s01.py`, on `env_setup_01`). The Python variable equals the id. The setup serial in a scenario id repeats the `setup` field by convention; the code checks nothing about it, and an author who moves a scenario to another setup renames it. No layout serial is in a scenario id: a scenario has one or more reference layouts. `docs/rename_table.md` maps the old ids (`scenario_30` on `env_layout3`, and so on).

---

## 8. Checklist before marking a domain ready

- [ ] All objects and locations referenced in tasks/actions appear in `env_layout.json`
- [ ] Every action call in a task method resolves to an `ActionSchema` in `actions.py`
- [ ] Every action schema used in a task is registered in `registry.py`
- [ ] All task schemas appear in `registry.py` `intentions` set
- [ ] `is_assigned` / `is_foreseeable` flags match domain semantics
- [ ] `completion` predicate in each action matches what `world_state_builder.py` actually emits
- [ ] `register_<domain>_domain()` is imported and called in `sim_model.py`



## subtask nesting: an example

```
DELIVER_PALLET(?pallet, ?dest)          RETRIEVE_EMPTY_PALLET()
        |                                        |
  ACQUIRE_PALLET(?pallet)              ACQUIRE_PALLET(empty_stack)
  move_to → pick_up                    move_to → pick_up

DELIVER_PALLET → [ACQUIRE_PALLET, move_to(?dest), place]
                        |
                 [move_to, pick_up]     ← still just actions, no extra nesting

RETRIEVE_EMPTY_PALLET → [ACQUIRE_PALLET, move_to(?dest), place]
                        |
                 [move_to, pick_up]     ← same ACQUIRE_PALLET action schema, just different parameter bindings, good for IR reasoning... 

```

```
deliver_pallet = TaskSchema(
    name="deliver_pallet",
    parameters=[_pallet, _dest],
    methods=[
        MethodSchema(
            name="deliver_inside",
            parameters=[_pallet, _dest],
            guards=[
                ConditionSchema("requested_inside_delivery", (_agent,)),
            ],
            steps=[
                StepCall("move_to", {Var("?target"): _pallet}),
                StepCall("pick_up", {Var("?pallet"): _pallet}),
                StepCall("move_to", {Var("?target"): Const("building_interior")}),
                StepCall("place",   {Var("?pallet"): _pallet, Var("?target"): Const("building_interior")}),
            ],
        ),
        MethodSchema(
            name="deliver_entrance",   # fallback — guards=[] means always applicable
            parameters=[_pallet, _dest],
            guards=[],
            steps=[
                StepCall("move_to", {Var("?target"): _pallet}),
                StepCall("pick_up", {Var("?pallet"): _pallet}),
                StepCall("move_to", {Var("?target"): _dest}),
                StepCall("place",   {Var("?pallet"): _pallet, Var("?target"): _dest}),
            ],
        ),
    ],
    is_assigned=True,
    is_foreseeable=False,
)
```
