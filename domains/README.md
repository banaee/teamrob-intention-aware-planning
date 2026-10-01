# Domains

This folder holds the use cases, one sub-package per domain: the tree of task schemas, the robot's task model, the
layouts, the setups and the scenarios. A domain imports `shared/` (the types) and nothing of the simulators.

```text
domains/
    discovery.py      ← registers layouts, setups and scenarios by discovery (T-L stage 2)
    kitting/          ← the reference domain: every form is first written here
    dock_loading/     ← the second domain (T-G): pallets between a truck and the delivery bays
```

`kitting/` is the reference for every form. A new domain copies its forms; where the two differ, kitting's is the
present one.

---

## 1. A domain's folder

```text
domains/<domain>/
    __init__.py
    actions.py          # ActionSchema definitions: the HTN primitive actions (leaves)
    tasks.py            # the task schemas (WorkTask, PersonalTask, HumanOnlyTask) and their methods
    script.py           # the call forms the scenarios are written in: one function per task schema
    registry.py         # builds the Tree; declares the task model and the object states (domain_config)
    layouts/            # the layout files, the room: env_layout_KK.json, the file stem is the id
    setups/             # the setup files, the shift: env_setup_NN.json
    scenarios/          # a package: scenarios_sNN.py holds every scenario whose setup is env_setup_NN
```

Registration is by discovery (`domains/discovery.py`): layouts and setups by the files in their folders, scenarios by a
module scan of the scenarios package at import of `domains.<domain>.registry`. No hand-written list; a duplicate
scenario id is an error at import. The simulator's `DOMAIN_REGISTRY` (`mesa_sim/run_mesa.py`) maps the domain's name to
its `domain_config`; `mesa_sim/list_scenarios.py` lists every registered scenario of every domain.

`registry.py` exports `domain_config`:

| key | what |
|---|---|
| `register_fn` | returns the domain's `Tree`: every task schema, every action schema, the microaction names |
| `task_model` | the task model every robot is given: every `WorkTask` and the `PersonalTask`s it foresees; no `HumanOnlyTask` |
| `states` | the object states the domain declares, `StateDeclaration(name, object_type)` (T-G A5); `object_type` None is a fact about no object |
| `layouts`, `setups`, `scenarios` | discovered (above) |

---

## 2. The three artefacts of a run (T-L; `docs/glossary.md` §9)

A run is a triple (layout, setup, scenario) plus the run options.

**Layout, the room** (`layouts/env_layout_KK.json`). Top-level keys `"space"`, `"areas"`, `"env_objects"`. The space
is centred on the origin, in cm, and holds every fixed object. `"areas"` declares the areas, each one rectangle
(`id`, `bounds`); a point on the boundary of two areas belongs to the first declared (`shared.types.area_at`).
`"env_objects"` lists the fixed objects with their `id`, `type`, `position` and `size`: tables, shelves, machines,
bays, a truck, a gate, landmarks. A fixed object's area is derived from its position, never declared. No movable
object and no agent. A landmark (type `landmark`) is a point only a `HumanOnlyTask` may name.

**Setup, the shift** (`setups/env_setup_NN.json`). The movable objects in one `"env_objects"` list, each with its
`"initial_container"` (an object of the layout; its origin, read by `home_container_of`) and a `"destination"` where
the domain designates one (read by `destination_of`). A `"states"` block lists the declared object states that hold at
the start, `{"state": <name>, "object": <id>}` (the object omitted for a fact about no object); a declared state not
listed does not hold. A different designation set is a different setup.

**Scenario, the episode** (`scenarios/scenarios_sNN.py`). A `ScenarioConfig` literal: its `id` (the Python variable
equals it), the one `setup` it binds, its `reference_layouts`, the purpose as `description`, and per agent its
`start_position`, `assigned_tasks`, `observes` and, for a human, the script. A run that names no layout takes the
first reference layout.

The loader validates the triple at load: every home container is an object of the layout; every destination is an
object whose type the schemas declare for that object's type; every task binding names an object with the schema's
type; every assigned task's determined parameter resolves to an object of its declared type; every state of the
`"states"` block is declared, names an existing object of the declared type; every start position lies inside the
space. A failure names the artefact and the mismatch.

Ids are serial, nothing encoded beyond order of writing: `env_layout_KK`, `env_setup_NN`, `scenario_sNN_MM` (NN the
setup's serial, MM a counter per setup). Scenario ids are unique within a domain. `docs/rename_table.md` maps old ids.

---

## 3. Tasks, actions, microactions

- **Task schemas** (`tasks.py`) are decomposed by HTN methods into actions. Each is one of three classes
  (`shared/types.py`):
  - `WorkTask`: may be assigned, to the human or to the robot. Always in the robot's task model.
  - `PersonalTask`: never assigned. In the task model it is a foreseeable task the robot recognises.
  - `HumanOnlyTask`: a `PersonalTask` never given to a robot (`go_to`, `stand`, `go_to_and_stand`); no hypothesis
    describes it. The only class whose parameter may be typed `landmark`.
- **Methods** (`MethodSchema`): guards and steps. The planner takes the first method whose guards hold in the present
  `WorldState`; an empty guard list always holds. A task with no method whose guards hold is not applicable
  (`AdaptivePlanner.is_applicable`, the one definition: the human's script form and the recognizer's liveness read
  it). A guard may bind one free variable existentially (`holding(?agent, ?other)`); `not_equal` is built in.
  `derived_vars` resolve a variable after selection (`home_container_of`); a task's `determined_parameters` resolve
  a parameter from another before selection (`destination_of`: the object's designation; a binding written in the
  task instance is kept).
- **Action schemas** (`actions.py`): preconditions, effects, retractions, and a `completion` the executor reads in the
  `WorldState`. `moved_object_key` / `moved_to_key` declare what an action moves, for the successor state (T-B2a) and
  for the body's grasp. An effect or retraction whose name is a declared state is applied by the environment when the
  action's last microaction has run (`scan_it` sets `is_scanned`).
- **Microactions** (STEP, GRASP, RELEASE, STAND, TOUCH) are the simulator's.

Two predicate families, never conflated:
- `at(agent, object)`: object proximity, the completion of a walk.
- `in_area(agent, area)`: the area an agent is in (`shared.types.area_fact`), emitted for every agent; a method guard
  may read it. Never `at(agent, area)`.

---

## 4. The human's script (T-H; T-G A3)

`Script(entries, closing=(), dependence=ScriptDependence.INDEPENDENT)`, written with the call forms of `script.py`:
- `entries`, the priority list: ordinary entries (a task instance, with events through `.at` / `.during`) and, below
  every ordinary entry, `RepeatableEntry(task)` (no events). When free, the human takes the first applicable open
  ordinary entry; with none applicable, the first applicable repeatable entry whose task is not complete in the present
  state; else it waits. An ordinary entry is closed once its task has left the stack completed, abandoned or
  infeasible.
- `closing`: taken in written order once every ordinary entry is closed; then the human selects nothing more.
- `dependence`: `ON_ROBOT` when entries wait for the robot's work; the load-time replay then reports the entries it
  could not replay instead of refusing the load.

---

## 5. The two domains

**kitting.** The robot and the human deliver items from shelves to a kitting table (`deliver_item`, a `WorkTask` whose
table is the item's designation); foreseeable tasks `coffee_break`, `ac_activation`; every method has no area guard.
Declares no object state. A script needs no closing part: its last entry is the exit walk (`docs/assumptions.md` 1.1).

**dock_loading** (T-G; `docs/handoffs/plan_T-G_stage1.md`). The robot, an automated forklift, delivers full pallets
from the truck to their delivery bays (`deliver_pallet`) and returns empty pallets to the truck (`load_return`); the
human, the staff member receiving the delivery, scans each delivered pallet (`confirm_delivered_pallet`); foreseeable
tasks `coffee_break`, `office_break`. Three areas: `area_truck_side`, `area_hall` and `area_office`, divided by the
gate (`dock_gate`) and the office door (`office_door`). Declared states: `is_empty(pallet)`, `is_scanned(pallet)`,
`is_open(gate)`. A pallet's destination is its designation: a delivery bay for a full pallet, the truck for an empty
one. Landmarks: `standby_place` (the repeatable standby entry) and `desk` (the closing part).

---

## 6. Checklist for a domain

- [ ] Every object a method names (`Const`) exists in every layout the domain's scenarios reference.
- [ ] Every action schema a method calls is registered in `register_fn`'s `Tree`.
- [ ] The task model holds every `WorkTask`, the foreseeable `PersonalTask`s, and no `HumanOnlyTask`.
- [ ] Every completion predicate is a fact the environment emits or a declared state an action sets.
- [ ] Every object state a method reads is declared in `states`.
- [ ] Every registered scenario loads: `PYTHONHASHSEED=0 python mesa_sim/list_scenarios.py`.
