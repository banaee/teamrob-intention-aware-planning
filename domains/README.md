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

Each domain package contains the same five files:

```
domains/<your_domain>/
    __init__.py
    tasks.py            # TaskSchema definitions  — HTN compound tasks
    actions.py          # ActionSchema defs     — HTN primitive actions (leaves)
    registry.py         # assembles DomainModel, declares intention set
    scenarios.py        # ScenarioConfig objects  — concrete agent assignments
    env_layout.json     # named locations and zones in the environment
```

---

## 2. env_layout.json — spatial constants

This file defines the named locations, zones, and fixed objects in the environment. Coordinates use a center-origin system `(0,0)` that matches the simulator grid directly.

Every named location or object that appears in `tasks.py` or `actions.py` must have an entry here. Zones use the convention `zone_<descriptor>`. This file contains no logic — only named spatial anchors.

**JSON structure rules:**
All static physical objects — shelves, tables, machines, obstacles, delivery areas,
gates, doors — go in the `"env_objects"` list with a `"type"` field. Do not create
new top-level sections for new object types.
Only these top-level keys are valid alongside `"env_objects"`:

- `"space"` — dimensions and units of entire environment space
- `"zones"` — IR context zones with bounds
- `"items"` — movable objects with runtime state
- `"robots"` — robot agent spawn configs
- `"humans"` — human agent spawn configs

**`items` vs `env_objects` — the actual criterion:** not "movable vs static."
An object goes in `items` if a task schema references it via an unbound `Var`
that IR must enumerate over multiple candidates (e.g. `deliver_item(?item)` —
could be any known item, one hypothesis per instance). An object goes in
`env_objects` if a task schema references it as a fixed `Const` already
resolved at design time (e.g. `coffee_break`'s target is `Const("coffee_machine_0")`,
not `Var`) — singular and unambiguous, nothing to enumerate. If a domain ever
needs multiple instances of something currently modeled as a fixed `Const`
(e.g. a second coffee machine), it conceptually belongs in `items`, regardless
of which JSON key it's under. `items` is a generic term for "enumerable
deliverable/target thing" across domains — not kitting-specific; dock_loading's
pallets are also `items` under this convention.

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

## 7. scenarios.py — concrete agent assignments

A `ScenarioConfig` assigns concrete task instances to each agent, with all parameters bound to specific values. Foreseeable tasks sit inline in the human's task list at the position where the deviation is expected. See `domains/kitting/scenarios.py` for the pattern.

### Scenario Naming Convention

Scenario names are prefixed by their layout number so the layout–scenario relationship is visible from the name alone:

- `env_layout0` → `scenario_00`, `scenario_01`, ...
- `env_layout1` → `scenario_10`, `scenario_11`, ...

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
