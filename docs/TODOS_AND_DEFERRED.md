# TeamRob Framework — TODOs, Bugs, and Deferred Items

Collected from Phase 2.1 (dock_loading domain) and 2.2 (visualization) sessions.
Each item has a category, priority, and the relevant file(s).
Items marked **[BLOCKING]** must be resolved before the simulation runs correctly end-to-end.

---

## 🐛 Active Bugs

**BUG-01 — `go_to_office` task skipped in dock_loading scenario** [BLOCKING]
Human agent skips the first task (`go_to_office`) and jumps directly to `scanning_pallet`.
Likely: task dequeue logic in `sim_agents.py` not initializing the queue correctly,
or `go_to_office` not registered in `registry.py` intentions set.
Files: `mesa_sim/sim_agents.py`, `domains/dock_loading/registry.py`

**BUG-02 — `scan_pallet` stuck with `micro=None`** [BLOCKING]
Human reaches delivery area position but `TOUCH` microaction never fires.
`_execute_touch` in `executor.py` may not be wired to the `"touch"` microaction name,
or `item.is_scanned` is not being set, so `scanned` predicate is never emitted.
Files: `mesa_sim/executor.py`, `mesa_sim/world_state_builder.py`

solved: `scan_pallet` method in `tasks.py` was calling `scan_pallet` action operator instead of `scan_it`, which is the one with the correct microaction and effect. Fixed method to call `scan_it`.


**BUG-03 — Robot one-step `task=None` gap between tasks**
After completing one task, robot shows `task=None action=None` for one step before
the planner seeds the next task. Benign but indicates a one-step planning delay.
Files: `mesa_sim/sim_agents.py`, `shared/planner.py`

**BUG-04 — Robot skips `dock_gate` waypoint**
`deliver_pallet` method includes `move_to(dock_gate)` as intermediate step, but robot
goes directly truck → delivery area. Likely: `gate_is_open(dock_gate)` predicate not
emitted by `world_state_builder`, so method guard fails and fallback has no gate step.
Files: `mesa_sim/world_state_builder.py`, `domains/dock_loading/tasks.py`

---

## 🔧 Technical TODOs

**TODO-01 — `action_decomposer._expand_fixed`: make fully generic**
Currently has hardcoded `if/elif` for `GRASP`, `RELEASE`, `TOUCH`.
Proper fix: `ActionOperator` declares `microaction_param_extractors` dict,
`_expand_fixed` iterates it generically. No domain-specific chains needed.
Files: `mesa_sim/action_decomposer.py`, `shared/types.py`
Reference: TODO #16

**TODO-02 — `world_state_builder`: emit `gate_is_open(dock_gate)` unconditionally**
Phase 2.1 shortcut: gate is always open. Emit the predicate unconditionally so
method guards in `deliver_pallet` and `load_return` evaluate correctly.
Files: `mesa_sim/world_state_builder.py`
Reference: TODO #8a

**TODO-03 — `SimModel`: B+C cleanup (rename + generic loader)**
Currently additive-only for safety. Full cleanup:
- Remove remaining kitting-specific `_init_*` helpers if any survive
- Remove hardcoded kitting import from `sim_model.py`
- Verify `_init_env_objects` handles all object types cleanly
Files: `mesa_sim/sim_model.py`
Reference: TODO B+C

**TODO-04 — Rename `"space"` key to `"environment"` in layout JSONs**
`"space"` (renamed from `"room"`) still implies a single room.
`"environment"` better captures the full spatial extent (hall + dock + truck + office).
Files: `domains/kitting/env_layout1.json`, `domains/dock_loading/env_layout1.json`, `mesa_sim/sim_model.py`
Reference: TODO #15

**TODO-05 — Rename `FactoryModel` → `SimModel` sweep**
Done in `sim_model.py` but may have residual references in comments or docs.
Files: all `mesa_sim/` files, `docs/`

**TODO-06 — `ItemObject` / `PalletObject` subclass refactor**
Currently `good_type`, `is_empty`, `is_scanned` are flat fields on `ItemObject`.
Proper design: `PalletObject(ItemObject)` subclass with pallet-specific fields,
`model.pallets` dict separate from `model.items`.
Requires updating `world_state_builder`, `executor`, `action_decomposer` type references.
Files: `shared/types.py`, `mesa_sim/sim_model.py`, `mesa_sim/world_state_builder.py`
Reference: TODO #13

**TODO-07 — `effects` field not consumed by live planner**
`ActionOperator.effects` are defined but the planner does not use them for forward
chaining. Required for full HTN planning with precondition checking.
Files: `shared/planner.py`
Reference: Phase 4 TODO

**TODO-08 — `dock_gate` open/close: implement `open_gate` ActionOperator**
`deliver_pallet` and `load_return` have a commented-out `gate_closed` method.
Implement `open_gate` action operator and wire the second method when gate state
is modeled dynamically.
Files: `domains/dock_loading/actionOperators.py`, `domains/dock_loading/tasks.py`
Reference: TODO in tasks.py comments

**TODO-09 — Path planning: replace straight-line STEP* with obstacle-aware planning**
Currently `action_decomposer.steps_toward()` uses straight-line interpolation.
Agents walk through walls and obstacles. Replace with A* or RRT in Phase 4.
Files: `mesa_sim/action_decomposer.py`
Reference: Phase 4 TODO

**TODO-10 — `scan_pallet` precondition: `obj_at(?item, delivery_area)` guard**
`scan_pallet` should only execute when the pallet has been delivered to the area.
Requires task eligibility condition evaluation (see DESIGN-01 below).
Files: `domains/dock_loading/tasks.py`, `shared/` cognitive loop
Reference: TODO #12

**TODO-11 — `space_drawer.py`: add dock color entries**
`OBJ_COLORS` and `ZONE_COLORS` missing entries for dock object types.
Without these, dock env objects render in default gray.
Files: `mesa_sim/viz/space_drawer.py`
Reference: TODO #11 (original list)

**TODO-12 — `run_mesa.py`: use `config["layout"]` number for layout path selection**
Currently layout number from `experiment.yaml` is read but ignored — path is hardcoded
per domain. Wire layout number to select `env_layout{N}.json` when multiple layouts exist.
Files: `mesa_sim/run_mesa.py`, `DOMAIN_REGISTRY`

**TODO-13 — `logs/` directory: add to `.gitignore`**
Log files should not be committed to the repo.
Files: `.gitignore`

---

## 🏗️ Design TODOs

**DESIGN-01 — Task eligibility conditions and scenario task scheduling mechanism** [Phase 2.3]
Human tasks in `scenarios.py` are a flat queue executed sequentially regardless of
world state. The proper mechanism: `TaskSchema.entry_conditions: List[ConditionSchema]`
checked against `WorldState` before task dequeue. If unsatisfied, agent idles.
This is simulator-agnostic (uses WorldState predicates only) and lives in `shared/`.
Both Mesa and ROS would benefit. Needs dedicated design session.
Files: `shared/types.py`, `shared/` cognitive loop, `mesa_sim/sim_agents.py`
Reference: TODO #17

**DESIGN-02 — Existential parameter binding in planner**
`scan_pallet` with unbound `?item` — planner should search `model.items` for first
pallet satisfying `obj_at(?item, delivery_area) ∧ ¬scanned(?item)` and bind at
planning time. Eliminates need to pre-assign pallet IDs in `scenarios.py`.
Requires planner extension for existential search over world state.
Files: `shared/planner.py`
Reference: discussed in Phase 2.1

**DESIGN-03 — `go_to_office` as foreseeable task: naming and reusability**
Currently defined as a dock_loading-specific foreseeable task. In principle it is
a generic "agent leaves workspace temporarily" pattern applicable to any domain.
Consider whether to generalize or keep domain-specific.
Files: `domains/dock_loading/tasks.py`

**DESIGN-04 — Parallel task coordination between agents**
Robot and human run in parallel with no coordination mechanism. Human can attempt
to scan a pallet before robot has delivered it. Proper fix requires either:
(a) task eligibility conditions (DESIGN-01), or
(b) shared world state dependencies between agent task queues.
Currently mitigated by `go_to_office` delay hack in scenario.
Reference: TODO #12, DESIGN-01

**DESIGN-05 — `DOMAIN_REGISTRY` in `run_mesa.py`: scaling**
Currently requires manual addition of import + registry entry per domain.
Consider auto-discovery from `domains/` folder structure in future.
Files: `mesa_sim/run_mesa.py`

---

## 🧹 Refactoring / Cleanup TODOs

**REFACTOR-01 — Normalize kitting `env_layout1.json` to flat `env_objects` format**
Kitting JSON still uses named sections (`shelves`, `kitting_table`, etc.).
Normalize to flat `env_objects` list matching dock format.
Blocked by: need to verify `_init_env_objects` handles all kitting object types.
Files: `domains/kitting/env_layout1.json`
Reference: B+C Step 2

**REFACTOR-02 — `parse_args()` called twice in `run_mesa.py`**
Both `_make_domain_model()` and `run_headless()` call `parse_args()` independently.
Refactor to parse once at module level and pass config around.
Files: `mesa_sim/run_mesa.py`

**REFACTOR-03 — `domains/README.md`: update domain folder name references**
README still references `dock_delivery_loading` in the folder listing.
Update to `dock_loading`.
Files: `domains/README.md`

**REFACTOR-04 — `roadmap.md`: update Phase 2.1 and 2.2 status**
Phase 2.2 (visualization) is complete. Phase 2.1 (dock_loading) is partially complete
— domain files done, simulation runs but two bugs remain (BUG-01, BUG-02).
Add Phase 2.3 (task eligibility conditions).
Files: `docs/roadmap.md`

---

## 📋 Known Limitations (Accepted for Phase 2.1)

**LIMIT-01 — Straight-line agent movement through walls**
Agents move in straight lines ignoring walls between hall/dock/truck.
Accepted: same as kitting. Fix deferred to Phase 4 path planning.

**LIMIT-02 — Parallel task independence: human scans before robot delivers**
Human `scan_pallet` executes without waiting for robot `deliver_pallet` to complete.
Mitigated by `go_to_office` delay in scenario. Proper fix: DESIGN-01.

**LIMIT-03 — Gate always open**
`gate_is_open(dock_gate)` emitted unconditionally. Gate state not modeled dynamically.
Fix: TODO-08 (`open_gate` action operator + `gate_closed` method).

**LIMIT-04 — All pallets start at same position (truck center)**
Pallets 0–5 all share `truck_interior` center position. No individual slot positions.
Deferred: individual pallet slot positions within truck area.

**LIMIT-05 — Empty pallet bays not wired to `LOAD_RETURN` task execution yet**
`load_return` tasks defined and in scenario but may not complete correctly
until BUG-01 and BUG-02 are resolved and full scenario runs end-to-end.

---

## 🗂️ Reference: Original TODO List (from Phase 2.1 session)

For traceability, the original numbered list from the session:

| # | Item | Status |
|---|------|--------|
| 1 | `env_layout_dock.json` | ✅ Done (`env_layout1.json`) |
| 2 | `actionOperators.py` | ✅ Done |
| 3 | `tasks.py` | ✅ Done |
| 4 | `registry.py` | ✅ Done |
| 5 | `scenarios.py` | ✅ Done |
| 6 | `sim_model.py` generic loader + parameterized registry | ✅ Done (additive) |
| 7 | `ItemObject` — `good_type`, `is_empty`, `is_scanned` fields | ✅ Done |
| 8 | `world_state_builder.py` — `scanned` + `gate_is_open` | ⚠️ Partial (gate_is_open may not be emitting, see BUG-04) |
| 9 | `executor.py` — `TOUCH` handler | ✅ Done (wired but BUG-02 remains) |
| 10 | `run_mesa.py` — domain selection wiring | ✅ Done |
| 11 | `space_drawer.py` — dock color entries | ❌ Not done (TODO-11) |
| 12 | `scan_pallet` precondition guard | ❌ Deferred (DESIGN-01) |
| 13 | `ItemObject`/`PalletObject` subclass refactor | ❌ Deferred (TODO-06) |
| 14 | Rename `FactoryModel` → `SimModel` | ✅ Done |
| 15 | Rename `"room"` → `"environment"` in JSON | ❌ Not done (TODO-04) |
| 16 | `action_decomposer` generic microaction extractor | ❌ Deferred (TODO-01) |
| 17 | Task eligibility conditions (Phase 2.3) | ❌ Deferred (DESIGN-01) |
