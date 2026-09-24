# TeamRob Framework — TODOs, Bugs, and Deferred Items

Collected from Phase 2.1 (dock_loading domain), 2.2 (visualization), and Phase 4 design sessions.
Each item has a category, priority, and the relevant file(s).
Items marked **[BLOCKING]** must be resolved before the simulation runs correctly end-to-end.

> **Terms:** `docs/glossary.md` gives each term one meaning. The entries below are the HISTORICAL
> RECORD and are left exactly as they were written, so some of them use a term differently from the
> glossary (the conflicts are listed in the glossary task's report). Read an entry in the terms of
> its own date; write new text in the glossary's.

---

## 🐛 Active Bugs

**BUG-01 — `office_break` task skipped in dock_loading scenario** ✅ RESOLVED
Root cause: `run_mesa.py` `parse_args()` used `parse_args()` instead of `parse_known_args()[0]`,
causing Solara args to conflict. Also `office_break` was missing from `registry.py` intentions set in an earlier version.
Fixed: `parse_known_args()[0]` in `parse_args()`; `office_break` confirmed registered.

**BUG-02 — `scan_it` TOUCH appeared stuck with `micro=None`** ✅ RESOLVED
Root cause: TOUCH fires and completes within a single Mesa step — invisible in every-10-steps log.
Also: task was renamed from `scan_pallet` to `confirm_delivered_pallet`, action from `scan_pallet` to `scan_it`.
Behavior is correct: TOUCH sets `is_scanned=True`, completion check passes, action advances — all in one step.

**BUG-03 — Robot one-step `task=None` gap between tasks**
After completing one task, robot shows `task=None action=None` for one step before
the planner seeds the next task. Benign but indicates a one-step planning delay.
Files: `mesa_sim/sim_agents.py`, `shared/planner.py`

**BUG-04 — Robot skips `dock_gate` waypoint**
`deliver_pallet` method includes `move_to(dock_gate)` as intermediate step, but robot
goes directly truck → delivery area. Likely: `gate_is_open(dock_gate)` predicate not
emitted by `world_state_builder`, so method guard fails and fallback has no gate step.
Files: `mesa_sim/world_state_builder.py`, `domains/dock_loading/tasks.py`

**BUG-05 — `place` action stalls forever: item released onto itself** ✅ RESOLVED
Root cause: `executor._nearest_env_object()` used `obj.at_location is not None`
as the "is this a portable object" filter. `at_location` is transiently `None`
while an item is being carried (set in `_execute_grasp`), so during
`_execute_release()`'s call to find a release target, the currently-held item
itself passed the filter — and since a carried item's position mirrors the
agent's every step, its distance to the agent is exactly 0, always winning as
"nearest." Item got released onto itself (`obj_at(item, item)`), never
matching the real completion predicate (`obj_at(item, kitting_table_0)`).
`place` action retried forever, task never completed.
Fix: added stable `SimObject.is_portable` flag, set once at load time, never
mutated — replaces `at_location is not None` in both
`executor._nearest_env_object()` and `world_state_builder.py`'s main object
loop.
Files: mesa_sim/sim_model.py, mesa_sim/executor.py, mesa_sim/world_state_builder.py
Reference: scenario_00 debugging session, Phase 4C typed-parameter work

---

## 🔧 Technical TODOs

**TODO-01 — `action_decomposer._expand_fixed`: make fully generic**
Currently has hardcoded `if/elif` for `GRASP`, `RELEASE`, `TOUCH`.
Proper fix: `ActionSchema` declares `microaction_param_extractors` dict,
`_expand_fixed` iterates it generically. No domain-specific chains needed.
Files: `mesa_sim/action_decomposer.py`, `shared/types.py`
Reference: TODO #16

**TODO-02 — `world_state_builder`: emit `gate_is_open(dock_gate)` unconditionally**
Phase 2.1 shortcut: gate is always open. Emit the predicate unconditionally so
method guards in `deliver_pallet` and `load_return` evaluate correctly.
Files: `mesa_sim/world_state_builder.py`
Reference: TODO #8a

**TODO-03 — `SimModel`: B+C cleanup (rename + generic loader)** ✅ RESOLVED
Fully superseded by the unified `_init_objects()` loader (Phase 4C typed-
parameter session) — single generic method for all object types, two-pass
(direct-position, then container-referenced), no domain-specific `_init_*`
helpers remain.
Files: mesa_sim/sim_model.py

**TODO-04 — Rename `"space"` key to `"environment"` in layout JSONs**
`"space"` (renamed from `"room"`) still implies a single room.
`"environment"` better captures the full spatial extent (hall + dock + truck + office).
Files: `domains/kitting/env_layout1.json`, `domains/dock_loading/env_layout1.json`, `mesa_sim/sim_model.py`
Reference: TODO #15

**TODO-05 — Rename `FactoryModel` → `SimModel` sweep**
Done in `sim_model.py` but may have residual references in comments or docs.
Files: all `mesa_sim/` files, `docs/`

**TODO-06 — `ItemObject` / `PalletObject` subclass refactor** ✅ SUPERSEDED
Resolved differently than originally proposed: rather than a `PalletObject`
subclass, `EnvObject`/`PortItemObject` were merged into one `SimObject` with
all fields explicit (deliberate choice — full attribute visibility over
metadata-dict flexibility; accepted field sprawl across domains as the cost).
`model.items`/`model.env_objects` collapsed into one `model.objects: Dict[str, SimObject]`.
Files: mesa_sim/sim_model.py
Reference: Phase 4C typed-parameter generalization session

**TODO-07 — `effects` field not consumed by live planner**
`ActionSchema.effects` are defined but the planner does not use them for forward
chaining. Required for full HTN planning with precondition checking.
UPDATED (Sept 2026): this is now the concrete blocker for DESIGN-16's `full_reorder`
strategy. Multi-task projection requires propagating a hypothetical WorldState across
tasks that have not executed — task 2's guards and duration estimate must see the world
as if task 1 completed. Applying declared effects generically is the correct mechanism,
but `ConditionSchema` has no retraction/negation semantics: `place`'s effects add
`not_holding(agent,item)` without removing the stale `holding(agent,item)` from the
earlier `pick_up`, so a naive union produces contradictory predicates and
`_guards_satisfied`'s existential matching would still find the stale fact. The existence
of `not_holding` as its own predicate name (never consumed anywhere) is itself a symptom
of this gap. Fixing it properly touches the core predicate model in `shared/types.py` and
deserves its own design session — deliberately NOT solved with a narrow position/holding
stopgap inside `_project()`, since that would silently fail for any future guard depending
on a different predicate (dock_loading gate state, `obj_at`, etc.).
Not blocking: `single_task` projects only from the real live WorldState.
(CORRECTED at T-B2b: the two paragraphs above describe the state BEFORE T-B2a. `project()` no longer
raises for orderings and `full_reorder` runs, on plain cost; see the T-B2a update below.)
UPDATED (B3.B design revision, September 2026): B3.B is next in the pipeline, and this entry APPLIES
TO IT IN PART. Needed, for projection only: effect application with retraction (at `task_committed` [D3: no
trigger now; the same holds at any re-decision mid-carry]
the live world holds `holding(robot, A)`; in the ordering (A, B) the stale fact would select
`deliver_with_return` for B), and the location of an object a projected action has moved (in (B, A)
with A held, A is fetched from its home container after B's return). Both go into a hypothetical
successor `WorldState` built and discarded inside one `project()` call; the live one is never stored
or mutated. NOT needed for B3.B: forward chaining and precondition checking in the live planner, which
is what this entry was filed for and which stays open. The smallest form (retraction marked on
`ConditionSchema` or add / delete lists; relocation declared on the action schema) is a PROPOSAL for
cchat, not decided. The warning above against a `holding`-specific stopgap stands.
design_decisions.md, "B3.B (`full_reorder`) is lookahead for the choice of the next task, built next".
UPDATED (T-B2a, September 2026): the part projection needs is BUILT and its form DECIDED: a delete list on
`ActionSchema` (`retracts`) and a declared relocation (`moved_object_key` / `moved_to_key`), applied by
`Projector._successor_state()`; design_decisions.md, "The successor state is derived from what the action
schemas declare: a delete list and a declared relocation". Kitting's `place` retracts `holding` and
`not_holding` is gone there (dock_loading still declares it, deferred). Forward chaining and precondition
checking in the live planner stay open, as filed.
OPEN FROM T-B2A, MEASURED: `pick_up` does not end `obj_at(item, shelf)`. The shelf is not a parameter of
`pick_up`, so a delete list with bound arguments cannot state it; it needs a wildcard or a functional fact
("an object is in one place"), which changes the fact representation, not a schema. The consequence is ONE
STALE PREDICATE in the successor state (`obj_at(item_6, shelf_6)` after item_6's delivery, scenario_80; the
only predicate on the robot or the item that the successor holds and the real world does not), READ BY
NOTHING TODAY: guards read `holding`, and target resolution reads the maps, which the relocation keeps right.
IT MUST BE RESOLVED BEFORE ANY CONSUMER READS `obj_at` FOR AN ITEM THAT HAS BEEN PICKED UP in a successor
state. The same form problem, also read by nothing: `move_to` does not end the previous `at(agent, ·)`, and
`waited` is ended by a later action of another kind.
Files: `shared/planner.py`, `shared/types.py` (ConditionSchema), `shared/meta_planner.py`
Reference: Phase 4B; Phase 4C meta_planner build session, September 2026

**TODO-08 — `dock_gate` open/close: implement `open_gate` ActionSchema**
`deliver_pallet` and `load_return` have a commented-out `gate_closed` method.
Implement `open_gate` action schemas and wire the second method when gate state
is modeled dynamically.
Files: `domains/dock_loading/ActionSchemas.py`, `domains/dock_loading/tasks.py`
Reference: TODO in tasks.py comments

**TODO-09 — Path planning: replace straight-line STEP* with obstacle-aware planning**
Currently `action_decomposer.steps_toward()` uses straight-line interpolation.
Agents walk through walls and obstacles. Replace with A* or RRT in Phase 4.
See DESIGN-13 for the broader plan: this becomes Mesa's use of the common
non-committed path-realization estimator, not a Mesa-only fix.
Files: `mesa_sim/action_decomposer.py`
Reference: Phase 4D

**TODO-10 — `scan_pallet` precondition: `obj_at(?item, delivery_area)` guard**
`scan_pallet` should only execute when the pallet has been delivered to the area.
Requires task eligibility condition evaluation (see DESIGN-01 below).
Files: `domains/dock_loading/tasks.py`, `shared/` cognitive loop
Reference: TODO #12

**TODO-11 — `space_drawer.py`: add dock color entries** ✅ RESOLVED
`OBJ_COLORS`/`ZONE_COLORS` both have dock_loading entries (truck, gate,
delivery_area, empty_bay, door / zone_hall_dry, zone_hall_frozen, etc.).

**TODO-12 — DONE** Layout selection via `experiment.yaml` `layout` field implemented.
`DOMAIN_REGISTRY` restructured as `domain → layout → scenario` hierarchy in
`domains/*/registry.py`. `run_mesa.py` resolves layout and scenario by name.

**TODO-13 — `logs/` directory: add to `.gitignore`**
Log files should not be committed to the repo.
Files: `.gitignore`

**TODO-14 — `AgentConfig.scheduled_tasks` → `assigned_tasks` (unordered set) for robot** ✅ RESOLVED
`scheduled_tasks` retained as field name on `AgentConfig` for both agent types.
Semantics split by agent type instead of renaming: human list is fixed/ordered ground truth;
robot list is an unordered task **pool** owned by meta_planner at runtime.
CORRECTED (Sept 2026): the earlier resolution text described the robot list as a "mutable
prioritised queue," which no longer holds. Under DESIGN-16's `single_task` strategy,
meta_planner selects one task per trigger and the remaining pool carries no ordering
commitment at any point — `MetaPlanner._queue`'s list order is storage order, not priority.
`seed_tasks()` loads the pool without ordering it; Q0 comes from the first `update()` call.
See design_decisions.md Phase 4 section for full specification.
Files: `shared/meta_planner.py`, `shared/types.py` (AgentConfig)

**TODO-15 — Team-level semantic costs: park as future cost function extension**
Current cost function = Mesa steps (moves, detours, pauses). Team-level costs
(human waiting time, shared resource conflicts, task dependency violations) are
intentionally excluded from Phase 4. Add as extension when team efficiency
metrics are introduced in Phase 5 or later.
INSTANCE (F1, September 2026): under robot-responsible separation (design_decisions.md,
"Robot-responsible separation") a standing robot may be in the human's path; in reality the human
walks around it, and that detour is a team-level cost parked here — realization prices only the
robot's own time. The Mesa human has no avoidance, so in Mesa the two agents simply come close or
overlap while the robot stands; those moments are not robot violations and are reported separately in
the evaluation ("stand"; `analysis/f1_robot_responsible/evaluate.py`).
FOR 4D (R2, September 2026): the robot that stops safely at an occupied place and cannot progress (C's
indefinite wait) has human cooperation as its principal remedy — communication, or a model of the human
making room — a team-level mechanism, parked here with the team-level costs. Related to the freezing
robot problem (design_decisions.md, "After C", the freezing point).
Files: `shared/meta_planner.py` (Phase 4 new)
Reference: Phase 4 design session; R2

**TODO-16 — Cost-aware method selection in `_select_method`**
Currently picks first applicable method (greedy). If multiple methods have
satisfied guards, the cheaper one may be missed.
Fix: pass cost estimator from meta_planner into _select_method, score all
applicable methods, return minimum cost.
Deferred until meta_planner cost model exists (Phase 4C).
Files: `shared/planner.py`
Reference: Phase 4B discussion

**TODO-18 — IR belief inertia at task transition** ✅ RESOLVED (partial)
Root cause identified: belief collapsed to exact 0.000 for suppressed hypotheses
(floating-point underflow through repeated multiplicative update), making recovery
after task completion impossible without new evidence overwhelming a zero prior.
Fix: BELIEF_FLOOR = 1e-3 applied post-normalization in recognizer.update().
Result (scenario_00, 200 steps): frozen-belief window after task 1 completion
shrank from 21 steps to 3 (steps 80→83); del(i6) transient wrong-winner at
transition (previously 3 steps) eliminated entirely; task-2 θ-crossing moved
from step 111 (required GRASP confirmation) to step 84 (direction evidence
alone sufficient).
Remaining gap (deferred, see TODO-20): no explicit reset-to-uniform on task
completion. The floor makes this non-blocking for Phase 4C but the reset would
give symmetric convergence rates between first and subsequent tasks.
Files: shared/recognizer.py, shared/likelihood_functions.py
Reference: Phase 4A validation, scenario_00, IR debugging session

**TODO-19 — Recognizer hardcoded simulator microaction strings** ✅ RESOLVED
`_likelihood` branched on literal `"grasp"`/`"step"` string comparisons —
coupling the cognitive layer to Mesa's specific microaction vocabulary.
Fix: dispatch now keyed by each hypothesis's ActionSchema fields
(`microactions` list membership, `progress_evaluator` name) instead of
hardcoded strings. Likelihood math extracted to new pure module
shared/likelihood_functions.py (completion_predicate_likelihood,
direction_consistency_likelihood, PROGRESS_EVALUATORS registry).
A new domain with a different microaction taxonomy needs zero recognizer
changes — only correctly populated ActionSchema objects.
Side effect (intentional, verified non-regressive): "release"/"touch"
microactions now also receive completion-predicate checks (previously
always NEUTRAL) — generalized for free, not hand-added.
CORRECTION (I1 audit 10.3, I2): that check has never been reached — the first
action of every kitting method is `move_to`, whose STEP* branch answers first for
every observation, so release ticks return 1.0 for every hypothesis. Unchanged by
I2 (dispatch order is the evidence model's, I3's business); the completion
predicate is now the planner-grounded one when the check is reached.
Files: shared/types.py (ActionSchema.progress_evaluator field),
domains/kitting/actions.py, domains/dock_loading/actions.py,
shared/likelihood_functions.py (new), shared/recognizer.py
Reference: IR debugging session, behavior-verified against scenario_00

**TODO-20 — Persistent per-hypothesis tree cursor / notify_task_complete**
Recognizer currently re-derives "which action schema applies" fresh every
step, rather than tracking a persistent cursor per hypothesis. (Until I2 it read
`methods[0]` and returned from its first schema — no tree was scanned, I1 10.5;
since I2 it decomposes each hypothesis through the planner's guard-selected
method every tick and dispatches over the grounded actions in order. Per-tick
re-selection, no stored phase: the phase is I3's.) UPDATE (I3): the per-hypothesis cursor
exists — derived every tick, with the expected action and origin stored
(design_decisions.md, I3 entry) — and completion is a pin, not a reset-to-uniform.
(b) remains open as TODO-55. No explicit signal exists for
"hypothesis h's task just completed → reset its belief contribution."
BELIEF_FLOOR (TODO-18) makes this non-blocking for Phase 4C, but a full
fix would: (a) track cursor state per hypothesis across cognitive clock
ticks, (b) reset belief to uniform on task_completion event, matching the
paper's Ht bottom-up tree-matching formalization more precisely.
Deferred to Phase 4C when the cognitive clock and meta_planner exist to
drive the reset trigger.
Files: shared/recognizer.py
Reference: Phase 4A validation, HCM_AAAI26 paper Hypothesis Generation section

**TODO-21 — Post-completion belief plateau: healthy uncertainty vs. artifact** [needs dedicated IR session]
Observed in a manual test run (scenario_00, item_6-carrying seed for deliver_with_return
validation, not an IR-focused test): after human_0 completes its scheduled tasks, belief
distribution over remaining robot task hypotheses settles at a near-even split (e.g.
item_3/item_4 ~0.498/0.498) and stays there for the rest of the run. Two explanations
are equally plausible from this trace alone: (a) genuine perceptual ambiguity — no
further observations exist to distinguish the hypotheses; (b) an artifact of
BELIEF_FLOOR + the post-completion frozen-belief window (see TODO-18). This run was not
designed to evaluate IR dynamics — no conclusion should be drawn either way. Needs a
dedicated session with a controlled test isolating post-task-completion belief behavior.
Files: `shared/recognizer.py`
Reference: cancellation-mechanism validation session, follow-up to TODO-18

**TODO-22 — Move `SimObject` from `mesa_sim/sim_model.py` to `shared/types.py`**
Currently kept in sim_model.py for expediency during the env_objects/items merge.
Should eventually live in shared/types.py — it's simulator-agnostic (generic
spatial object + runtime state), and the ROS embodiment will need the same shape.
Files: mesa_sim/sim_model.py → shared/types.py
Reference: Phase 4 design session, July 2026

**TODO-23 — `TaskSchema.parameter_types` declared at task level, not method level**
Typed-parameter enumeration (?item → "item" type, etc.) declared once per
TaskSchema. If a task ever needs different methods to target different object
types (e.g. deliver_pallet's two methods needing different destination types),
revisit and move parameter_types to MethodSchema instead.
Files: shared/types.py
Reference: Phase 4 design session, July 2026

**TODO-24 — `"obstacle"` type still hardcoded in `world_state_builder.py`**
`_add_proximity_predicates()` skips objects where `type == "obstacle"` — same
class of domain-string hardcoding as the old `"?item"` check, left in as a
judgment call (treated as a shared physics/rendering category, not a
domain-semantic label). Not rigorously justified.
General fix: derive "is this type ever a valid task target" from whether the
object's `type` appears anywhere in any TaskSchema.parameter_types.values()
for the active domain, rather than a hardcoded string comparison. Bigger,
cross-cutting mechanism — needs its own design, not an inline fix.
Files: mesa_sim/world_state_builder.py (_add_proximity_predicates)
Reference: Phase 4 design session, July 2026

**TODO-25 — dock_loading typed-parameter integration: not reviewed** [deferred]
`dock_loading/tasks.py`/`scenarios.py` were manually updated in parallel with
the kitting typed-parameter work (?pallet/?delivery_bay, office_break rename,
parameter_types added to deliver_pallet/load_return/coffee_break) but not
reviewed against the same rigor as kitting. Known issue: `confirm_delivered_pallet`
TaskSchema is missing `parameter_types` and its `parameters` list (`[_pallet]`
only) doesn't match `scenarios.py`, which binds both `?pallet` and
`?delivery_bay` to it — `?delivery_bay` isn't declared on the schema or used
in its step_calls. Also unconfirmed: whether `registry.py`'s import was
updated from `go_to_office` to `office_break`.
Since I2 the recognizer grounds every hypothesis through the planner each tick, so
`confirm_delivered_pallet`'s empty-bindings hypothesis raises `ValueError: unbound
variable '?pallet'` on the first tick of any dock_loading run — a modelling error
surfacing loudly, by design (see design_decisions.md, I2 entry), not a recognizer bug.
Fix the schema (add `parameter_types`) before running dock_loading. `office_break`'s
guarded-only method is handled: no applicable method → NEUTRAL, logged once.
dock_loading's `wait_at` still declares `ProcessCompletion` (kitting's does not since
I2); migrate it to `waited(?agent, ?entity)` with the rest of TODO-25.
Files: domains/dock_loading/tasks.py, domains/dock_loading/scenarios.py, domains/dock_loading/registry.py, domains/dock_loading/actions.py
Reference: Phase 4C typed-parameter generalization session; I2 IR foundations session

**TODO-26 — `HypothesisKey` documented in io_contracts.md §1.8 as a shared/types.py
dataclass; actually a hand-written class in shared/recognizer.py** (no `@dataclass`
decorator, manual `__eq__`/`__hash__`/`__repr__`). Doc corrected to reflect actual
location (see §1.8). Open question for later, not blocking: should it move to
types.py as a real dataclass for consistency with every other cross-boundary type
(BeliefState, ProjectedPlan, etc.), or is recognizer-internal placement fine since
it's only exposed externally via get_hypothesis()? Not needed for meta_planner.py
work — get_hypothesis()'s return type is unaffected either way.
Files: shared/recognizer.py, shared/io_contracts.md
Reference: Phase 4C meta_planner build session, July 2026

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

**DESIGN-03 — `office_break` as foreseeable task: naming and reusability**
Currently defined as a dock_loading-specific foreseeable task. In principle it is
a generic "agent leaves workspace temporarily" pattern applicable to any domain.
Consider whether to generalize or keep domain-specific.
Files: `domains/dock_loading/tasks.py`

**DESIGN-04 — Parallel task coordination between agents**
Robot and human run in parallel with no coordination mechanism. Human can attempt
to scan a pallet before robot has delivered it. Proper fix requires either:
(a) task eligibility conditions (DESIGN-01), or
(b) shared world state dependencies between agent task queues.
Currently mitigated by `office_break` delay hack in scenario.
Reference: TODO #12, DESIGN-01

**DESIGN-05 — `DOMAIN_REGISTRY` in `run_mesa.py`: scaling**
Currently requires manual addition of import + registry entry per domain.
Consider auto-discovery from `domains/` folder structure in future.
Files: `mesa_sim/run_mesa.py`

**DESIGN-06 — `ProjectedPlan` type: definition and relation to `AbstractPlan`** [Phase 4 prereq]
`AbstractPlan` is single-task and executor-facing (existing, keep as-is).
Phase 4 requires a separate `ProjectedPlan` — multi-task lookahead used only by
meta_planner for interference detection and cost comparison; never handed to executor.
Fields needed: `List[(AbstractPlan, estimated_start_step, estimated_duration, spatial_zones)]`.
"Abstract" in `AbstractPlan` refers to symbolic (vs microaction) level — naming is correct.
Must be defined in `shared/types.py` before Phase 4 implementation begins.
Files: `shared/types.py`
Reference: Phase 4 design session

**DESIGN-07 — Cognitive clock trigger conditions and θ hysteresis policy** ✅ RESOLVED (Sept 2026)
IMPLEMENTED: `evaluate_triggers()` has exactly three conditions — `no_current_task` (covers
both t=0 and ordinary completion in one condition), `theta_crossed` (a *crossing* event:
`prev < θ ≤ current`, not a per-tick threshold test, which would refire continuously), and
`task_committed` (`holding` transitions `None → not-None`). θ=0.75, single threshold, no
hysteresis; confidence is gate-only and never feeds `_cost()`. `MetaPlanner` owns
`_prev_belief`/`_prev_executor_state` internally rather than accepting them as parameters.
See design_decisions.md, "Three cognitive-clock triggers."
The remaining open sub-questions from the original entry (human-completes-task trigger,
human-enters-zone pre-trigger, within-action decision points) were NOT implemented and
remain available as future additions — none is required for Phase 4C. Also unresolved and
low-stakes: `theta_crossed` wins arbitrarily if it and `task_committed` fire on the same
tick (only the unused `score` field differs).
SUPERSEDED (D2, D3; September 2026): `theta_crossed` was replaced by `recognition_changed` (D2) and
`task_committed` is removed (D3). `evaluate_triggers()` has two conditions, `no_current_task` then
`recognition_changed`; `_prev_executor_state` is gone. design_decisions.md, "D3: task_committed is not a trigger".
Original entry retained below.

[original entry, Phase 4 prereq]
The cognitive clock is event-based. Confirmed triggers:
- Task completion — queue advances, re-evaluate ordering with latest belief
- Belief threshold θ crossed (confidence rises above θ for first time, or most_likely switches)
- Robot commits to task (picks up item) — cancellation cost changes discontinuously here

Open / to settle before Phase 4C implementation:
- Belief drops below θ again: hold last decision or revert to baseline queue?
  Single threshold or hysteresis band (enter at θ_high, exit at θ_low)?
- Human observed completing a task: changes interference picture, likely a trigger
- Human enters new zone: lightweight spatial pre-trigger before full threshold?
- Robot reaches path decision point within current action: time-sensitive re-evaluation

`replanning.py` trigger logic to be absorbed into `meta_planner.py`; `replanning.py` retired after migration.
Files: `shared/meta_planner.py` (Phase 4 new), `shared/replanning.py`
Reference: Phase 4 design session

**NOTE on DESIGN-07 — cognitive clock trigger must be event-driven, not periodic**
Confirmed requirement for `evaluate_triggers()` and any future `ros_sim/`
implementation: the cognitive-clock trigger must not run on a fixed timer, and
specifically must not be derived arithmetically from the motion-clock tick
rate. A periodic poll is the easy default in ROS (rclpy timers), so this needs
to be an explicit, stated constraint rather than left implicit — a concrete
case of exactly this pattern was observed during the Fatemeh code-review
session.
Files: shared/meta_planner.py (evaluate_triggers), ros_sim/ (future), ros_sim_guideline.md
Reference: Fatemeh code review session

**NOTE — single decision path requirement (no parallel shortcut logic in embodiment layer)**
Design rule for `evaluate_triggers()`/`update()` and any embodiment
integration: the RESELECT/WAIT (or equivalent) decision must be made once,
inside `shared/`, and the embodiment layer must only execute the returned
decision — it must not run its own parallel heuristic capable of
independently producing or short-circuiting that decision. State this
explicitly in `ros_sim_guideline.md` before `ros_sim/` integration work
begins, so a "temporary" fallback path doesn't end up being the only path
that actually fires.
Files: shared/meta_planner.py, ros_sim/ (future), ros_sim_guideline.md
Reference: Fatemeh code review session

**NOTE — current-task-as-candidate design confirmed sufficient** (not Q1 —
Q1 is queue ownership, see roadmap.md Phase 4C; this is a separate,
previously unlabeled principle)
This design (current task competes as just another candidate through the
same cost pipeline, no special WAIT/RESELECT branch) was cross-checked against
an alternative two-branch implementation encountered during the Fatemeh code
review and holds up — no gap found that the uniform-candidate approach doesn't
already close. No further action; noted for continuity.
Files: shared/meta_planner.py (Phase 4C)
Reference: Fatemeh code review session

**DESIGN-08 — Team-level semantic costs in cost function (parked)** ✅ RESOLVED as a placement question (wait-decision revision, Sept 2026); team-level costs still parked
The question this entry came to carry — WHERE a conflict becomes a number: priced in `_cost()`,
or gated in B2 — is settled by neither: conflict becomes cost BY CONSTRUCTION in realization, as
the duration of the holds placed to keep `min_separation` from the human. No conflict weight, no
term to tune. What survives: the OBSERVE / VALUE split, relocated — `earliest_violation` observes
(pure geometry), holding turns the observation into a number, and `min_separation` is passed in
rather than chosen by the geometry. Also surviving, unchanged: the team-level semantic costs
below (human waiting time, disruption, fairness) remain PARKED (TODO-15); realization prices only
the robot's own time. See design_decisions.md, "The robot can wait". Original entry retained.

[original entry]
Current cost function is purely step-based (Mesa steps / ROS seconds).
Future extension: incorporate team-level costs — human waiting time, shared resource
conflicts, task dependency violations. Deferred to post-Phase 4; keep in mind when
defining cost function interface in meta_planner so extension does not require redesign.
Files: `shared/meta_planner.py` (Phase 4 new)
Reference: Phase 4 design session

**DESIGN-09 — Pre-RESELECT cheap filter, separate from candidate cost calc** [Phase 4C, parked]
Cancellation cost is computed intrinsically by planner.py (guarded HTN method on
deliver_item — see design_decisions.md), not as a meta_planner cost term. This is
orthogonal to whether RESELECT should run at all. Open question: should meta_planner
apply a cheap pre-check (via _detect_interference or immediate evidence) before
enumerating and decomposing every candidate, vs. always running full enumerate-and-
minimize? Related to DESIGN-07's θ hysteresis question but distinct: DESIGN-07 gates
*when* re-evaluation triggers; this gates whether a triggered re-evaluation does full
candidate enumeration or short-circuits early.
NOTE (wait-decision revision, Sept 2026): B2 realizing the CURRENT TASK ALONE is exactly this
cheap pre-check — one candidate's realization instead of the pool's. Whether B2 survives as a
block at all (computation saving and hysteresis are its remaining roles) is TODO-36.
Files: `shared/meta_planner.py` (Phase 4C, `_detect_interference`)
Reference: Phase 4C design session, cancellation-mechanism discussion

**DESIGN-10 — Interference-detection sampling granularity** ✅ PARTIALLY RESOLVED (Sept 2026)
RESOLUTION: option (b) — resampled points along each projected trajectory — chosen; option
(a) endpoint-only rejected as structurally blind to mid-move conflicts. Implemented as
`discretized_time_sampling()` in `shared/trajectory_algorithms.py`: samples both `Segment`s
at fixed step intervals across their overlapping time window plus the window's exact end
point. `interval=1.0` is a placeholder, not calibrated.
Zone-vs-position is also resolved and NOT as originally framed — see design_decisions.md,
"Interference is geometric, not zone-based." `ConflictPoint` carries `position`+`distance`,
never a zone.
STILL OPEN: (i) whether to implement `closest_point_of_approach()` (documented in
trajectory_algorithms.py, exact rather than sampled, no interval tradeoff, but has
near-zero-relative-velocity edge cases); (ii) tuning `interval`; (iii) the volume problem —
see TODO-27. Original entry retained below for context.
UPDATE (wait-decision revision, Sept 2026): (i) is answered in role if not in code — the
closed-form quadratic is what realization's `earliest_violation` needs (the roots below
`min_separation²` give the violation interval and the earliest clear time; no sampling, no
resolution parameter, no world-unit constant in `shared/`). `discretized_time_sampling()`
becomes a fallback (first sample below the threshold, not the minimum over all samples).
(ii) and (iii) lapse with the batch profile: realization asks per segment, per start time.
Which is implemented first is an implementation choice of the realization task.

[original entry, Phase 4C, parked until _detect_interference implementation]
Two candidate approaches surfaced reviewing an alternative endpoint-only
implementation: (a) per-GroundedAction-goal points only (cheap, matches a
coarse endpoint-based pre-filter — see DESIGN-11 — may miss mid-action
conflicts on long moves), (b) resampled points along each action's projected
path (catches mid-action conflicts, cost/complexity depends on resampling
rate). This is distinct from DESIGN-09 (which decides WHEN detection runs) —
this decides WHAT granularity detection operates at once it runs. Producing
comparable (time-or-step, position/zone) samples from each backend's
simulation is a solved, per-embodiment concern (same pattern as
ProcessCompletion) and not the open part; the open part is which points along
the sequence shared/ should treat as points of interest. Decide against
actual ProjectedPlan/AbstractPlan structure once built, not abstractly.
Files: shared/meta_planner.py (Phase 4C, _detect_interference), shared/types.py (ProjectedPlan)
Reference: Fatemeh code review session, cost-function comparison

**DESIGN-11 — Endpoint-proximity pre-filter for interference detection (candidate)** [Phase 4C, parked]
Cheap first-pass option for DESIGN-09's pre-RESELECT filter: check whether a
candidate's final goal position lands near the human's predicted destination
(single point-in-radius comparison) before running full step-wise
_detect_interference() on that candidate. Proposed only as a coarse
pre-filter, not the detection mechanism itself. Candidates that clear this
check trivially skip full enumeration; candidates that don't still get the
real check.
Files: shared/meta_planner.py (Phase 4C, _detect_interference)
Reference: Fatemeh code review session, cost-function comparison

**NOTE on DESIGN-09/DESIGN-11 — pre-filter must stay domain-agnostic**
in_zone-based pre-filtering was considered and rejected: zone granularity is
too coarse to usefully narrow candidates before full interference detection,
and building the pre-check around zone/layout specifics would mean
customizing shared/ logic to how a particular environment is laid out —
against the mind/body separation principle. Any pre-filter (see DESIGN-11)
must work from generic position/prediction data only, not domain- or
layout-aware shortcuts.
Files: shared/meta_planner.py (Phase 4C)
Reference: Fatemeh code review session, cost-function comparison

**DESIGN-12 — Horizon-projected confidence as recognizer output, not meta_planner computation** [parked — now MOOT under single_task]
STATUS UPDATE (Sept 2026): this entry exists to serve multi-task candidate cost evaluation
(confidence-at-a-future-horizon for tasks further down a candidate ordering). DESIGN-16
adopted single-task selection, under which no task is ever costed before it starts — every
candidate is projected from the live WorldState with the live belief. The need disappears.
This entry becomes live again only if `full_reorder` is ever implemented. Not closed, since
that strategy is retained as a documented alternative; do not implement in the meantime.
STATUS UPDATE (B3.B design revision, September 2026): B3.B is now next in the pipeline, and this
entry DOES NOT APPLY to it as designed. B3.B realizes the robot's whole sequence against the ONE human
projection admitted at the trigger by the live belief, inside [trigger, T_h]; nothing past T_h is
assessed or charged, so no confidence at a future horizon is asked for. `single_task` already does the
same with one long candidate. The sentence above ("live again only if `full_reorder` is ever
implemented") is superseded: this entry becomes live only under a design that projects the human past
its current task. Still parked; do not implement. design_decisions.md, "B3.B (`full_reorder`) is
lookahead for the choice of the next task, built next", (d).
Original entry retained below.

[original entry, parked, revisit during IR enhancement]
Current-moment confidence already flows to planning as-is: BeliefState
(confidence, most_likely, distribution) is the object MetaPlanner.update()
receives, and DESIGN-07's θ-gate reads directly from it. Not a gap.

Open, distinct question: multi-task candidate cost evaluation (queue-wide
lookahead) needs confidence-at-a-future-horizon for tasks further down a
candidate ordering, where no real observation exists yet — a genuinely
different need from the live θ-gate, which only ever reads current
confidence. Surfaced reviewing an alternative implementation that fed a
decayed probability directly into cost as a magnitude — conflicting with
DESIGN-07's "confidence is a gate only, never feeds the cost function
itself," though that resolution was scoped to the live trigger and doesn't
by itself resolve this case.

Leaning: if built, this belongs as an attribute/output of recognizer.py
(e.g. an extended get_hypothesis()/projection call returning confidence-at-
horizon), not as decay math reimplemented inside meta_planner or cost
functions — belief evolution over an unobserved horizon is a property of
the belief distribution itself, not a planning computation. Keeps
meta_planner a pure consumer of whatever recognizer hands it, same pattern
as ProcessCompletion for embodiment mechanics.

Deliberately left open rather than decided now — revisit when IR is
enhanced, not before. Do not implement local belief-decay math in
meta_planner/costs in the meantime.
Files: shared/recognizer.py, shared/meta_planner.py (Phase 4C)
Reference: Fatemeh code review session, cost-function comparison

**DESIGN-13 — Common non-committed path-realization estimator ("action-estimator" adaptor)** [Phase 4C, parked — dedicated design session needed] — PARTLY PULLED FORWARD (wait-decision revision, Sept 2026)
The PAUSE half of this estimator is now Phase 4C's realization function, hold-only strategy:
`realize(projected_plan, human_projection, min_separation, start_tick) -> RealizedPlan | None`,
living on the projection / trajectory side of `shared/`, holding per segment until
`earliest_violation` clears. It differs from the entry below in two ways that are decided: it
is `shared/`-resident (a hold needs no obstacle geometry, only the two projections), and it
returns a plan AND its duration (the "(a) trajectory, (b) cost" return contract below,
confirmed). The DETOUR half (go around; needs a path planner and iteration between trajectory
and interference — `obstacle_aware_path()`'s role) and the OFF-THE-SHELF PLANNER (PRIEST or
equivalent, ROS) remain Phase 4D, as pluggable strategies of the same function. The hold
reaches the executor as a HINT it may refine but must not re-decide or cancel (TODO-71).
Original entry retained below.

[original entry]
Surfaced from the pause/detour cost discussion (DESIGN-10/11 context): a
common, cheap, non-committed path-planning estimator, used by BOTH backends
during cost estimation (called from _estimate_duration in meta_planner),
and additionally by Mesa as its real execution-time path realization
(replacing the Phase 4 TODO in mesa_sim/action_decomposer.py's
steps_toward — currently pure straight-line, no obstacle awareness; see
TODO-09). ROS keeps a two-tier split: this same cheap estimator for cost
estimation, but real execution still uses PRIEST (GPU CEM optimization) —
deliberately not unified on the ROS side, since PRIEST is heavy/stateful and
running it speculatively per candidate is not viable. This means
estimator-vs-actual divergence is an accepted, known gap on ROS specifically
(estimate from the common estimator vs. what PRIEST actually produces) — not
something this design eliminates.

Scope for this estimator, not yet designed — separate dedicated session
needed to build a skeleton and later the actual algorithm:
  - Not shared/-resident: needs real geometry (obstacles, walls), so must
    be implemented once and exposed per-backend through each backend's own
    adapter (Mesa/ROS), same pattern as layout_adapter — shared/ only ever
    calls through the adapter interface, never owns the algorithm.
  - Must handle both pause (temporal wait for a predicted-occupancy
    conflict to clear) and detour (spatial reroute around a static or
    moving obstacle) as outcomes of the SAME call — shared/ passes a
    conflict hint (what/where/when, derived from its own ProjectedPlan /
    _detect_interference), not a pre-decided pause-or-detour instruction.
    The estimator decides which resolution (or combination) fits, not
    shared/.
  - Return contract (interface, not implementation): should return both
    (a) a generated feasible trajectory/step-sequence and (b) its
    estimated cost — not just a cost number. Confirm this exact shape in
    the dedicated session; noted here so it isn't lost.
  - Open sub-question, not yet decided: whether the estimator should be
    parameterized with the same kinematic limits PRIEST respects (v_max,
    a_max) to narrow the estimate-vs-PRIEST gap on ROS, vs. staying purely
    geometric (e.g. A*/RRT-lite with no kinematic modeling). Deferred to
    the dedicated session, not a blocker for scoping the interface now.
  - Mesa-specific note: for Mesa, since real execution can use this same
    estimator's output directly, cost-estimation-time and execution-time
    path realization collapse into one function — no separate "light" vs
    "real" tier needed on Mesa, unlike ROS. A separate, more optimized
    Mesa-specific realizer is possible later but not needed now.

Explicitly NOT the place to design the algorithm itself (A*, RRT, or
otherwise) — this entry captures role/interface/scope only. Algorithm
design deferred to its own dedicated chat/session.
Files: shared/meta_planner.py (_estimate_duration), mesa_sim/action_decomposer.py
(steps_toward), mesa_sim/layout_adapter.py, ros_sim/ (future, PRIEST integration)
Reference: Fatemeh code review session, pause/detour/path-realization discussion

**DESIGN-14 — Dynamic object registry (future)**
Object-by-type registry is static-at-construction for now (built once from
layout JSON). If a scenario ever needs objects to appear/disappear mid-run
(e.g. robot breakdown, new task becoming available), this requires redesigning
IntentionRecognizer's belief update — currently assumes fixed hypothesis-space
size (BELIEF_FLOOR renormalization, uniform prior denominator). Not just a
registry change — inserting a hypothesis mid-run with no accumulated evidence
needs its own design (what prior does it get?).
Files: shared/recognizer.py, object registry (wherever it lands)
Reference: Phase 4 design session, July 2026

**DESIGN-15 — `office_break`: unresolved design questions (parked)** [was: go_to_office]
Task renamed from `go_to_office` to `office_break` (dock_loading). Three open
questions before this task is reliable:
1. `parameter_types={"?office_chair": "office_chair"}` doesn't match the
   office_chair object's actual "type": "chair" in env_layout1.json — one
   needs to change to match the other before this task can enumerate.
2. `door_is_open` guard has no fallback method and no confirmed emitter in
   world_state_builder.py — same unresolved-predicate class as gate_is_open
   (TODO-02). If never true, office_break has zero applicable methods.
3. Method ends by moving the human to dock_gate rather than returning to a
   neutral spot — confirm this is deliberate before relying on it.
Files: domains/dock_loading/tasks.py, mesa_sim/world_state_builder.py
Reference: Phase 4 design session, July 2026

**DESIGN-16 — Single-task RESELECT vs. full queue reordering (strategy flag)** ✅ RESOLVED (Sept 2026); REVISED (B3.B design revision, Sept 2026): `full_reorder` designed, to be built next; two open points
REVISED (cchat, September 2026, after T6): `full_reorder` (B3.B) moves from retained alternative to next
in the pipeline; `single_task` stays the default and the receding-horizon argument stands. Reason:
one-table kitting is why order has not mattered (every delivery ends at the one table); two-table
kitting, which the domain already expresses through `?kitting_table`, couples tasks by geometry with no
human at all; with a projection admitted the window to T_h can cover a later task of the sequence, so the
whole sequence is realized against the one human projection; and since the robot's own boundaries
re-decide, the sequence past the head is a lookahead for the choice of the head, not an order commitment.
The three prerequisites in the paragraph below ("To implement `full_reorder` ...") are SUPERSEDED:
  (i)   TODO-07 applies in part: retraction and object relocation in a hypothetical successor state for
        projection; not the planner's forward chaining (see TODO-07's update);
  (ii)  DESIGN-12 does not apply: nothing is priced past T_h (see DESIGN-12's update);
  (iii) brute permutation is acceptable at pools of 3 to 5 (6 to 120 orderings per trigger, prefixes
        shared); the scalability remark stands for larger pools.
"Do not implement piecemeal" is replaced by a proposed order: successor state and `project()` for
orderings, then B3.B on plain cost, then on realized cost.
OPEN, proposals recorded and marked, to be decided in cchat before the realized-cost step:
  (1) where a hold that clears a conflict in a later task is placed: one δ at the decision position
      (`realize()` today) or a hold at the boundary before that task (proposed: the boundary; only the
      head's δ is executed, so B3.A and B3.B differ in the choice alone);
  (2) what B2 commits to under B3.B, a task or an order (proposed: a task; `b2a` unchanged).
Evaluation: B3.A against B3.B on two-table fixtures, plain cost first, then realized; the one-table
fixtures are expected identical in choice (an expectation with two named exceptions, not an identity);
byte-identity is the default run with `strategy` = `single_task`. `strategy` needs a run option.
Full record: design_decisions.md, "B3.B (`full_reorder`) is lookahead for the choice of the next task,
built next". Fixtures: TODO-47 (f).

RESOLVED in favour of single-task, receding-horizon selection as the implemented default;
full reordering retained as a documented, switchable alternative. Full rationale in
design_decisions.md, "Single-task selection (receding horizon), not queue-wide reordering."

Implementation: `MetaPlanner._strategy: Literal["single_task", "full_reorder"]`, constructor
param, defaults to `"single_task"`. `update()` branches on it; `_project()` raises
`NotImplementedError` for orderings longer than 1. The seam exists in code, not only in docs,
so `full_reorder` is a known-cost extension rather than a rewrite.
(CORRECTED at T-B2b: as of T-B2a `Projector.project()` chains the entries of an ordering and raises
nothing; as of T-B2b `_replan_tasks()` dispatches `full_reorder` to `_replan_orderings()`, on plain cost,
and `--strategy` is a run option (T-B2d). Realizing an ordering is T-B2c.)

To implement `full_reorder`, three things are needed: (i) resolve TODO-07's effects/retraction
semantics for cross-task WorldState propagation, (ii) DESIGN-12's horizon-projected confidence,
(iii) a scalable ordering search — brute permutation is O(n!) and is the wrong shape for any
realistic task count. Do not implement piecemeal.

NOTE ON NUMBERING: this decision was referred to as "DESIGN-14" throughout the September 2026
build session before it was noticed that DESIGN-14/15 were already taken. Any code comment,
docstring, or chat reference to "DESIGN-14" regarding strategy/reordering means DESIGN-16.
Files: shared/meta_planner.py, shared/io_contracts.md §2.2
Reference: Phase 4C meta_planner build session, September 2026

**TODO-27 — `conflicts` list volume: no "worth recording" threshold** — ✅ OBSOLETE (T10: the batch profile is gone)
`_detect_interference()` concatenates every `ConflictPoint` from every time-overlapping
segment pair with no filtering. Observed in scenario_00: 900–1500 ConflictPoints for a single
candidate, since `discretized_time_sampling(interval=1.0)` emits one point per step per pair
over ~1700-step projections. Functionally correct (only the minimum distance is read) but
memory-wasteful, and makes the objects useless for logging/inspection.
Deliberately not fixed now: a second "only record below distance X" threshold was considered
and rejected as premature — the list is bounded and correctness is unaffected. Revisit if
profiling shows it matters, or when DESIGN-08's soft penalty needs to actually iterate these.
SUPERSEDED (wait-decision revision, Sept 2026): the batch profile goes with
`_detect_interference()`. Realization asks `earliest_violation` per segment at a start time and
receives one interval (or none), so there is no list to bound. ✅ CLOSED (T10): `_detect_interference()`
is gone; what remains of the sampler and its types is TODO-83.
Files: shared/meta_planner.py (_detect_interference), shared/trajectory_algorithms.py, shared/projection.py
Reference: Phase 4C scenario_00 validation, September 2026

**TODO-28 — `min_safe_distance` and `assumed_speed` are uncalibrated placeholders** — RESTATED (wait-decision revision, Sept 2026): `min_safe_distance` becomes `min_separation`, the clearance realization must ACHIEVE — ✅ DECIDED (R1, Sept 2026): `min_separation` = 2.5 × the robot's motion per tick — ✅ LANDED in B2 (T4) and B3 (T10); `min_safe_distance` removed — REVISED (T-A1, Sept 2026): supplied by the body in physical units, not a ratio × speed
REVISED (T-A1, September 2026): `min_separation` is supplied by the body in physical units, a required
`MetaPlanner(min_separation=...)` argument in world units with no default in `shared/`; Mesa reads it
from `mesa_configs.yaml` (`simulation.min_separation: 50`, cm) and the `[run]` header names value and
source (since T-A1 follow-up 2: `min_separation=50.00 min_separation_source=mesa_configs.yaml:simulation.min_separation beta=0.01 beta_source=mesa_configs.yaml:simulation.beta units=cm`; a run that overrides it, the T6
wrapper's `T6_SEP_CM`, names that source instead). REASON: a
standard sets a distance; the R1 form (2.5 × the body's motion per tick) coupled the safety distance
to the robot's speed, which violates "safety parameters are set from outside the planner" (T6). The
value is unchanged (50 cm) and so is behaviour: the sixteen graded-evidence baselines and the stop-on
s00 / s30 cells are byte-identical apart from the `[run]` line. The "relative to motion, so that it
scales" argument below is withdrawn with it: the value is not a scale-calibration item (TODO-47 (b)).
It is set per body (ROS: its own, from the standard and the body's sizes), not measured on fixtures.
The text below is the record of the R1 form.
DECIDED (R1, September 2026, on T1b's data): `min_separation` = 2.5 × the robot's motion per tick,
i.e. 50 cm on the current layouts (20 cm/tick), EXPRESSED RELATIVE TO MOTION so that it scales with
the body rather than as an absolute in `shared/`. T1b (`analysis/t1b_realization/REPORT.md`, Finding
1) bounded the value: below the executor's 30 cm arrival radius nothing is held and the only failures
are arrival-tick artefacts; at 20–100 cm holds are rare and short; from 150 cm (7.5 ticks of motion)
the dominant event is the human's path passing the robot's standing position, which a hold cannot
resolve. 2.5 ticks of motion sits inside the regime where holds are short and all-unrealizable is
rare (1 of 43 admitted triggers at 50–100 cm). To be revisited under randomised layouts (TODO-47 (b))
and real body sizes (ROS). LANDED in code in T4, for B2 only: `MetaPlanner(min_separation_in_motion_ticks=2.5)`
× `Projector.assumed_speed` (the body-supplied motion per tick), passed to `realize()` by `b2a`. B3
adopts it in T10; until then B3 keeps `min_safe_distance = 1.0` (ruling on the T4 report). The
`assumed_speed` half was resolved by T2 (below).
✅ LANDED FOR B3 (T10, September 2026): `min_safe_distance` and the `interference_algorithm` parameter
are removed from `MetaPlanner`; B3 hands `realize()` the same `min_separation` (2.5 × `assumed_speed`,
50 cm) B2 uses, and there is no exclusion threshold anywhere in selection. The run header names the
value (`[run] ... min_separation=50.00 (min_separation_in_motion_ticks=2.5 x assumed_speed=20)`,
TODO-78). What remains open is the VALUE under randomised layouts (TODO-47 (b)) and real body sizes.
RECORDED (R2, September 2026): the one value governs two situations — crossing paths in the open and
working side by side at a shared place — that collaborative practice treats as different modes; and at
a point place with arrival radius r co-use needs s ≤ 2r and arrival on opposite sides (50 vs 60 cm here:
the rim only). What the single value costs is in design_decisions.md, "After C". Not changed.
The parameter is no longer an exclusion threshold ("a ConflictPoint below it makes a candidate
infeasible") but the separation realization must achieve by holding: `earliest_violation` is
asked for the first time the two agents come within `min_separation`, and the robot holds until
that interval clears. Still the single policy decision, still passed in by `MetaPlanner`, still
uncalibrated — the code keeps the old name and value (1.0) until realization lands; nothing
selects on it differently today. What T1 established about its VALUE: it cannot be read off a
distribution (the conflicted values cluster at 4.9–29 and the clear ones at 93+, with nothing
between — a gap in the data, not a threshold the data chooses). It must be ARGUED, and expressed
RELATIVE to scale — agent motion per tick, or a layout length — not as an absolute, so that it
survives randomised layouts (TODO-47 (b)); the same defect class as β (TODO-58). Deciding it is
the one open parameter before realization can be implemented; it is decided on re-measured data,
not on the fixtures. Original entry retained below.

[original entry]
Both default to `1.0` in `MetaPlanner.__init__` with no calibration against Mesa's actual
distance/step scale (agent positions span roughly ±400 units; `interval` in
`discretized_time_sampling` is likewise `1.0`). `min_safe_distance=1.0` proved permissive in
scenario_00 — nothing was ever excluded, closest observed approach was ~2.9 — so the
infeasibility branch is effectively untested (see TODO-30). A too-large value would exclude
every candidate; a too-small one makes interference detection inert.
Needs a calibration pass against real layout geometry, ideally alongside `default_action_cost`.
Files: shared/projection.py (init — assumed_speed, default_action_cost), shared/meta_planner.py (init — min_safe_distance)
Reference: Phase 4C scenario_00 validation, September 2026

Calibration order (fixture-design session): calibrate only after the meta_planner's
confidence-gated human projection lands. Under today's ungated projection,
min_safe_distance=50 would exclude scenario_20's item_4 at t=0 against a 0.167 tie-break
projection (min_dist 20) — an exclusion, but not a legitimate one.

Update (evidence-gated projection admission session): the gate has landed; calibration is
unblocked. Findings from scenario_20, 200 steps, PYTHONHASHSEED=0, runs 20260910_144814
(switch off) and 20260910_144816 (switch on):
- scenario_20 now has two valid fixture conditions. Switch ON is the mid-approach-reveal
  condition: first admitted projection at step 2 (confidence 0.881, evidence-based — two
  directional updates over three admissible hypotheses), item_4 min_dist 14.98 vs item_6
  321.9, at ~9% of the robot's approach. Switch OFF is the late-reveal condition: first
  admission at step 22, the human's grasp, 100% of the approach spent.
  CORRECTION (leg session): the step-2 figure was duplicate counting and is retracted. After
  "One leg is one observation" the switch-ON reveal is at step 11 (0.780, ZONE_BOOST on
  zone_SW entry over one honest chord of 0.641; robot ~half way to shelf_4; item_4 min_dist
  14.98 at cost 812) and the switch-OFF reveal stays at the grasp, step 22 (0.797).
- The t=0 phantom projection is closed in both runs: `none(below_theta)` (0.167 off, 0.332 on).
- No selection changed in either run. `min_safe_distance=1.0` excludes nothing, `_cost()` is
  execution cost only, so B3 is pure argmin and the cheapest task wins every trigger. item_4
  reaches min_dist 4.90 (switch off, step 24 `task_committed`) on a ±600 layout and is still
  selected. This is the concrete demonstration that the pipeline cannot express "close is
  bad" — the gap B2 (TODO-36) and DESIGN-08 exist to fill.
- Calibration evidence for `min_safe_distance`: across both runs, conflicted values cluster
  at ~4.9–29 (4.90, 14.98, 15.45, 15.53, 24.90, 29.11) and clear values at ~93–819, with no
  observation between 30 and 93.
- Step 59, switch on: item_6 119.5 vs item_7 119.3 — indistinguishable on proximity, separated
  only by cost (1513 vs 1711). A worthiness score based on distance alone would have nothing
  to say here.

Update (T2, September 2026) — the `assumed_speed` / time-scale half is RESOLVED. Projection
steps are execution ticks: `RobotAgent` constructs `Projector(assumed_speed=<Mesa step_size>,
default_action_cost=1.0)` (mesa_sim/sim_agents.py; step_size read from mesa_configs.yaml), so a
movement action lasts distance/20 ticks and a stationary action one tick, for robot and human
projections alike. `shared/` still holds no Mesa constant. Sampling resolution is preserved in
world units: `discretized_time_sampling(max_spatial_step=...)` spaces samples so the faster
agent moves at most that many units between them (speed read off the Segment); the value is
bound on the body side from `mesa_configs.yaml: simulation.interference_spatial_resolution`
(1 cm) and has no default in `shared/`, since a world-unit resolution is itself a unit-scale
assumption. `[meta-cand] cost=` now
reads in ticks (scenario_20 t=0: 54 / 71 / 103, formerly 1032 / 1372 / 2028). The T1 evidence
above and in `analysis/t1_conflict_measurement/REPORT.md` is in world units and unchanged.
Consequence: with placement lasting a real tick, both agents' placement segments sit at the
identical table position in overlapping ticks whenever the arrival gap is under a tick, so
`min_dist` reaches exactly 0.0 and `min_safe_distance = 1.0` now EXCLUDES those candidates
(TODO-30 is exercised; scenario_10 step 257 hits the every-candidate-excluded `RuntimeError`).
`min_safe_distance` itself stays OPEN and was deliberately not touched.
Post-T2 regression baselines (PYTHONHASHSEED=0): runs 20260911_082601 (s00 off), _082604
(s00 on), _082606 (s10 off, aborts at step 257), _082609 (s10 on, aborts at 257), _082612
(s20 off), _082615 (s20 on).

**TODO-29 — `deliver_with_return` untested under MetaPlanner**
The guard was validated pre-MetaPlanner via a manual `robot.carrying` seed in
`sim_model.__init__`. That seed is now removed, and it would no longer exercise the path
anyway: a held item that is also one of the robot's own candidate tasks always wins on cost
(it is cheapest to deliver what you are holding), so `not_equal(?other, ?item)` fails and
`deliver_already_held` fires instead of `deliver_with_return`.
Re-testing needs a seed item that is NOT in the robot's candidate pool. Until then,
`deliver_with_return` is unexercised under the current selection mechanism.
Files: domains/kitting/tasks.py, mesa_sim/sim_model.py, domains/kitting/scenarios.py
Reference: Phase 4C scenario_00 validation, September 2026

**TODO-30 — Interference exclusion branch never exercised** — MEANING CHANGED (wait-decision revision, Sept 2026): "infeasible" = no realization within the human's horizon — ✅ RESOLVED by decision (R1, Sept 2026): all-unrealizable → plain projected cost, logged `all_unrealizable` — ✅ BUILT (T10): the `RuntimeError` is gone; one event measured — ✅ CLOSED (F1): realization is total, the branch no longer exists — ✅ CLOSED (F1: nothing is unrealizable)
CLOSED (F1, September 2026): under robot-responsible separation (design_decisions.md,
"Robot-responsible separation") a clearing hold always exists, `realize()` always returns a cost, and
there is no unrealizable candidate — neither the exclusion branch nor the all-unrealizable fallback
exists any more (both removed from `_replan_tasks`). s30_on 21, T10's one event, now realizes item_4
with δ = 7 (the robot stands while the human passes at 47.8 cm). Nothing left to exercise.
DECIDED (R1, September 2026, with TODO-52): when NO candidate realizes, `update()` selects by plain
projected cost — the argmin over the pool with no hold, exactly the path taken when there is no human
projection — and logs the trigger as `all_unrealizable`. The `RuntimeError` is superseded and is
removed when realization lands in the meta-planner (T10); until then the code still raises. The
justification is the assumption recorded in design_decisions.md, "Assumption: execution-time
avoidance past T_h": what realization cannot resolve within the human's projection is the execution
layer's. Of the three readings below this is (2) without a "least-bad" ranking (an unrealizable
candidate has no realized cost to rank on), and it records the event so that (3)'s question can be
asked of the logs. T1b: the condition is absent below 50 cm and occurs once at 50–100 cm (s30_on 21,
the mirror crossing) on the fixtures; from 150 cm it is the majority case.
✅ BUILT (T10, September 2026): `_replan_tasks` takes the argmin of `RealizedPlan.cost` over the
realizable candidates; when none realizes it takes the argmin of `RealizedPlan.projected_duration`
(the same fractional T_r, never `total_estimated_cost`), returns `hold=0`, and logs
`[meta-b3] ... selection=all_unrealizable`. The `RuntimeError` is gone. MEASURED (s00/s10/s20/s30 ×
prior off/on, `realized`, gate `none` and `b2a`): ONE event, s30_on step 21 (`theta_crossed`, the
mirror crossing: item_4 and item_2 both `hold_position_violated`, T_h 53.68) — the fallback keeps
item_4 (T_r 53.68 vs 65.45), where the L2 baseline's `min_safe_distance` exclusion had switched to
item_2. The residual conflict is real and measured: actual separation 36.6 / 11.0 / 14.6 cm at ticks
21–23 (continuous minimum 0.00 at tick 23, the agents pass through each other), all INSIDE that
decision's assessed window — exactly the case the execution-time-avoidance assumption (TODO-73) leaves
to a layer Mesa does not have. Note also the PARTIAL case, which is not this item: when SOME candidate
realizes, an unrealizable candidate cannot win however short it is (s20_on 57: item_4 at T_r 3.95
`hold_position_violated` loses to item_6 at 84.65; see design_decisions.md, "B3 selects on realized
cost", the finding recorded there).
Under realization a candidate is infeasible only when NO start time within the human's projected
horizon clears `min_separation` — rarer than the current "a ConflictPoint below the threshold",
and meaningful (e.g. a human standing at the kitting table for longer than the horizon blocks
every delivery in the pool). The T2 exclusions recorded below (arrival gap under a tick at the
table, `min_dist = 0.0`) are exactly the cases that become a short HOLD instead of an exclusion.
ALL CANDIDATES UNREALIZABLE: the `RuntimeError` is not the right answer to that condition and is
superseded; it stays in the code until realization lands (scenario_10's step-257 raise, TODO-52,
is this case). The outcome is OPEN — three readings, NONE CHOSEN:
  (1) hold and re-decide: stand still this tick, keep the current task, decide again at the next
      trigger. Needs a re-entry rule (what ends the hold) and a guard against deadlock if the
      human is idle and nothing triggers;
  (2) pick the least-bad candidate and let the executor handle the residual conflict —
      defensible precisely because the hold is a hint;
  (3) treat it as evidence that `min_separation` is set wrong, or that the human's horizon is
      too short, and record rather than act.
Belongs to the next decision point with TODO-28 and TODO-36. Original entry retained below.

[original entry]
Across scenario_00 validation runs every candidate returned `feasible=True`; no candidate was
ever excluded by `_detect_interference()`. The detection machinery runs and produces plausible
distances, but the branch that actually removes a candidate — and therefore the whole reason
interference detection exists — is unproven. Also unproven: `update()`'s `RuntimeError` when
*every* candidate is infeasible.
Needs a scenario deliberately constructed so the human's predicted trajectory blocks a robot
candidate (or a calibrated `min_safe_distance`, see TODO-28). This is the main gap before
Phase 4C can be called validated rather than merely working.
Files: shared/meta_planner.py (`_detect_interference`, `update`), domains/kitting/scenarios.py
Reference: Phase 4C scenario_00 validation, September 2026

Calibration order (fixture-design session): calibrate only after the meta_planner's
confidence-gated human projection lands. Under today's ungated projection,
min_safe_distance=50 would exclude scenario_20's item_4 at t=0 against a 0.167 tie-break
projection (min_dist 20) — an exclusion, but not a legitimate one.

Update (evidence-gated projection admission session): still never exercised. With the gate in
place, every candidate across scenario_00/10/20 is `feasible=True`, including item_4 at
min_dist 4.90 in scenario_20 (switch off, step 24). Calibration evidence and the two
scenario_20 fixture conditions are recorded under TODO-28.

Update (T2, September 2026): NOW EXERCISED, by the time-scale fix rather than by calibration.
With projection steps = execution ticks, a placement occupies a full tick, and two agents
projected to place at the same table within a tick of each other stand at the identical
point: `min_dist = 0.0 < 1.0`. scenario_20 switch on, step 11: item_4 `feasible=False`,
item_6 selected. scenario_20 switch off, step 24: item_4 excluded, item_6 selected.
scenario_10 (both switches), step 257: item_5 is the only remaining candidate and is
excluded → `RuntimeError` (every candidate infeasible), the run aborts. Both branches this
item asked for are therefore reached; whether the exclusion is *legitimate* (an arrival gap
under one tick at a 200 × 100 table modelled as a point) is the `min_safe_distance` question
under TODO-28, still open, and the "what does the robot do when everything is excluded"
question (no WAIT outcome) is now live rather than hypothetical.

**TODO-31 — `estimate_duration()` is unused internally**
`Projector.project()` calls `build_segments()` directly and derives duration from the
segments it already has, rather than calling `estimate_duration()` (which would trigger a
second, redundant geometry walk). Nothing currently calls `estimate_duration()`. It was
retained as a standalone convenience method, with its signature taking `agent_id`/`start_step`
explicitly instead of re-deriving `agent_id` from `plan.actions[0].bindings`. Likely callers
are viz or Phase 5 evaluation — either wire it in or delete it.
Files: shared/projection.py
Reference: Phase 4C meta_planner build session, September 2026

**TODO-32 — `wait_at` duration ignored in cost estimation** ✅ CLOSED (R2, September 2026)
✅ CLOSED (R2): the duration was already domain knowledge — a constant bound by the method schema
(`coffee_break_default`: `PT60S`; `ac_activation_default`: `PT2S`), not a scenario value — so the human's
executor and the robot's projector read one source by construction. The projection now uses the duration
bound on the grounded action (`ActionSchema.duration_key`, `"?duration"` on `wait_at`), converted by a
body-supplied `duration_to_steps` callable on the `Projector` (Mesa hands in
`action_decomposer._parse_duration_to_steps`; `shared/` holds neither parser nor seconds-per-tick).
Effect: s10's coffee_break projection T_h 5 → 34 at step 123, s40's 14.3 → 43.3 / 22.3 → 51.3 and 10.3 →
39.3; no decision or hold changes anywhere; s00/s20/s30 unchanged. The matched-duration assumption and
the mismatch experiment's shape are recorded in design_decisions.md, "The human's wait duration in the
projection".
ORIGINAL: `Projector.build_segments()` treats every non-movement action as costing
`knowledge.get_cost(action_name)` or `default_action_cost`, including `wait_at` — so a
`PT60S` coffee break and a `PT2S` AC toggle currently cost the same. The real ISO-8601
`?duration` binding is parsed in `mesa_sim/action_decomposer.py`, which `shared/` cannot
import. A known simplification, not a considered decision.
Matters specifically for foreseeable tasks (`coffee_break`, `ac_activation`), whose whole
point is that the robot should reason about how long the human will be occupied. Likely to
distort candidate costs once foreseeable-task scenarios are tested.
UPDATE (wait-decision revision, Sept 2026): now LOAD-BEARING, not merely distorting. Foreseeable
tasks are recognised (I2–I4d: `coffee_break` crosses θ in scenario_40), so the human's projection
contains a `wait_at` segment whose duration is one tick whatever the real wait; and under
realization the length of a stationary human segment IS the hold a robot task pays to pass it,
so a mis-timed occupation changes the wait/switch calculus directly — and whether a candidate is
realizable within the horizon at all (TODO-30). The `?duration` binding still parses only in
`mesa_sim/action_decomposer.py`; the projector needs the same value without importing it.
Files: shared/projection.py (build_segments), mesa_sim/action_decomposer.py
Reference: Phase 4C meta_planner build session, September 2026

**TODO-33 — Run loop does not stop when all agents are finished**
`RobotAgent.finished` was added (mirroring `HumanAgent.finished`) so the terminal state is
reachable, but nothing outside `sim_agents.py` reads either flag — confirmed by grep. A
200-step run continues stepping both agents as no-ops long after all tasks complete
(scenario_00: everything done by step 147).
Harmless, but wasteful and makes log tails uninformative. Fix belongs in the run loop
(`run_mesa.py` / `SimModel.step()`), not in the agents.
Files: mesa_sim/run_mesa.py, mesa_sim/sim_model.py
Reference: Phase 4C scenario_00 validation, September 2026

**TODO-34 — Pre-existing `obs` fragility in `RobotAgent.step()` logging**
The IR logging block guards on `self.belief is not None and human is not None`, then reads
`obs.timestamp`. But `obs` is only bound when *this step's* `build_observation()` returned
non-None, while `self.belief` persists across steps. If `human is not None` and
`build_observation()` returns `None` on a step where a belief already exists, `obs` is either
stale or unbound — `AttributeError`/`UnboundLocalError`.
Not introduced by the MetaPlanner migration; pre-existing, spotted while editing the
surrounding block. Not observed firing in scenario_00.
Files: mesa_sim/sim_agents.py (`RobotAgent.step`)
Reference: Phase 4C meta_planner build session, September 2026

**TODO-35 — `seed_tasks()` placement: private section but called externally**
`seed_tasks()` lives under `meta_planner.py`'s "Internal" section but is called by
`sim_agents.py` at agent construction, making it de facto public. Either move it to the
public interface section and document it in `io_contracts.md` §2.2, or have the constructor
take the initial task pool directly. Cosmetic/contract-hygiene only.
Files: shared/meta_planner.py, shared/io_contracts.md
Reference: Phase 4C meta_planner build session, September 2026


**TODO-36 — `MetaPlanner` block restructuring (B1/B2/B3) not yet implemented** — B2 `b2a` ✅ BUILT (T4); B3 with realized cost ✅ BUILT (T10); B2 vs none identical on the fixtures at ρ = 0.5 — ✅ CLOSED as a design step (T-A1): B2 is an evaluation factor of T-F
REVISED (T-A1, September 2026): B2 (`gate_strategy`) is an EVALUATION FACTOR in T-F, not a design step.
`none` and `b2a` are built and stay; `b2b` stays a stub. Whether the commitment gate earns its place is
a result of T-F's factorial (cost_strategy × gate_strategy × strategy × separation_stop × prior), not a
question to settle before other work: no step of the pipeline re-reads B2 first, and B3.B does not wait
for it (under B3.B `b2a` commits to a task and runs unchanged, open point 2 of the B3.B entry, settled at
T-B's design time). The entry is closed on that; the record below stands.
`update()` currently runs one flat pipeline: assemble candidates → project each → detect
interference → filter infeasible → cost → argmin. A block decomposition was designed
(September 2026) but not built:
  B1  human projection — DONE, extracted to `Projector.project_human()`, called via
      `MetaPlanner.update_human_projection()` once per fired trigger
  B2  plausibility gate on the current task — NOT BUILT. Decides whether to continue the
      current task or escalate to reorder. Two variants: B2.A (assess current task in
      isolation; needs a worthiness score that does not exist yet) and B2.B (compare
      current against other tasks individually — self-calibrating, but redundant with B3.A)
  B3  reorder — B3.A (single-task argmin, what `update()` does today) or B3.B
      (permutations, blocked on TODO-07 and the horizon question)
Also: `no_current_task` bypasses B2 entirely and goes straight to B3 — there is nothing to
continue. B2 is therefore specifically a *mid-task* commitment mechanism; the robot still
re-decides freely at every task boundary.
Both B2 and B3 to be independent flags, all four combinations runnable. B2.B+B3.A is a
redundancy control, not a policy — it computes the same argmin twice and selects identically
to `none`+B3.A, differing only in projection count (CORRECTED, R1: the earlier text said
"identically to B2.A+B3.A", which is wrong — B2.A can continue where B3.A would switch, so those
two are NOT equivalent; the equivalence is with no gate at all, as TODO-47 already states). Useful
in an ablation table, misleading if read as a fourth strategy.
BLOCKER: B2.A needs a scalar worthiness score turning `List[ConflictPoint]` into a number —
the same missing quantity as DESIGN-08's soft interference penalty. Build once, use for both.
Candidate formulas: minimum distance across conflicts; count below a radius; proximity
integrated over time; or estimated added cost from pausing/detouring (DESIGN-13), which would
make the score comparable to execution cost and remove the need for a separate threshold.
Also open: whether B2's threshold is distinct from B3's exclusion threshold — they are
different in kind (graded/effort-based vs. binary/safety-based), not merely in value.
Naming: `_is_current_task_plausible()` or similar — "feasible" is wrong, since the check is
about worthiness, not doability.
UPDATE (wait-decision revision, Sept 2026) — the BLOCKER is resolved and the block's REASON is
in question. The scalar exists: the last candidate formula above is the one taken — B2.A
realizes the CURRENT TASK ALONE and reads its hold δ (one candidate's realization, far cheaper
than B3). The block split as built (B1.5 bypass on `no_current_task`, B2 reached only by
`theta_crossed` / `task_committed` [since D2 / D3: `recognition_changed` alone], `human_projection is None` →
continue) stands. But B3's
argmin over REALIZED costs already accounts for conflict, so B2's original rationale — that B3
could not express "close is bad" — is gone; its remaining candidate roles are computation
saving and hysteresis (which matters more now that prior-off `theta_crossed` fires up to three
times per recognition, TODO-68). OPEN, next decision point: does B2 survive as a policy block?
And if it does, what is δ judged AGAINST — δ in isolation has no reference (two ticks is cheap
against a 19-tick switch, expensive against a 3-tick one). Three readings, none chosen:
  - δ against the human's REMAINING HORIZON — self-contained, needs no second candidate,
    distinguishes "hold briefly" from "hold until the human is gone";
  - δ as a fraction of the task's own duration (an overhead ratio) — arbitrary in the way a
    bare threshold is;
  - B2 reduces to computation saving and hysteresis, and is not a policy block.
B2.B (realize current + each other task; margin) is redundant with B3 by construction, as before.
The "distinct thresholds" question above dissolves: B3 has no exclusion threshold any more, only
`min_separation` inside realization (TODO-28) and the all-unrealizable outcome (TODO-30).
✅ DECIDED (R1, September 2026): `b2a` IS BUILT (task T4). It realizes the current task alone and
CONTINUES if δ ≤ ρ × (the human's remaining projected duration at the trigger, T_h − trigger) — the
first reading above; otherwise, or if the current task is unrealizable, it escalates to B3.
`human_projection is None` still means continue. ρ is an explicit `MetaPlanner` policy parameter,
default 0.5, a STATED ASSUMPTION to be varied in T6, not a calibrated value. B2's role is
COMMITMENT: it can only prevent a switch B3 would make, never select or hold on its own. `b2b` stays
a documented stub. B3 stays `single_task` (B3.A) with realized cost (T10); `full_reorder` stays out
of 4C. T1b's reference data (§8): under minimal holds no current-task δ at s ≤ 100 cm exceeds 0.20
of T_h remaining, so at ρ = 0.5 the gate would not have escalated on any held current-task row in the
fixtures — enough to show it does not fire spuriously, not enough to show when it should (5 held
rows in two fixtures). Consequence for D2 (TODO-68): under `b2a` repeated `theta_crossed` triggers
mostly end in a continue, which may also hide a real change of belief (TODO-48).
✅ BUILT (T4, September 2026). `_is_current_task_plausible()` returns the hold to continue with
(whole ticks) or None to escalate; `update()` returns `UpdateResult(current_task, queue, hold)` on a
continue. `b2a`: `human_projection is None` → continue, hold 0; otherwise the current task is
projected alone and realized at decision step 0 (`realize()`, `min_separation` =
`min_separation_in_motion_ticks` (2.5) × `Projector.assumed_speed`, i.e. 50 cm in Mesa); realizable
and δ ≤ ρ × (T_h − 0) → continue with hold δ; otherwise escalate to B3. `rho` is a constructor
parameter, default 0.5. One `[meta-b2]` log line per call (trigger, current task, projection
admitted, realizable, reason, δ, T_r, remaining, bound, verdict). `gate_strategy` stays `"none"` by
default (byte-identical to the L2 baselines in all ten regression conditions) and is selected per run
with `--gate_strategy b2a` or `configs/experiment.yaml`. `b2b` stays a stub (NotImplementedError).
B3 is unchanged (plain cost, `min_safe_distance` filter) until T10, so a B2 escalation reaches the old
B3 and a B3 decision carries no hold.
MEASURED (T4; s00/s10/s20/s30 × prior off/on, `b2a`, ρ = 0.5): 51 B2 calls, 49 continue (10 with a
hold δ = 1–7, 39 without; 9 of the 39 had no projection) and 2 escalate, both `hold_position_violated`
(s30_on 21: B3 switches to item_2, as in the `none` run; s20_on 57: B3 re-selects item_4). No
escalation on δ above the bound (largest δ / bound 0.40, s20_off 20). A counterfactual B3 at every
continue (instrumented run, identical logs otherwise) picks the current task in all 49. So B2 never
kept a task B3 would have switched away from, and its commitment role is not exercised by these
fixtures at ρ = 0.5. RULED (T4 report): this is a FINDING FOR T6, where ρ is varied, NOT a reason to
change `b2a`. What the gate changes on these fixtures is that holds are now executed. Scripts:
`analysis/t4_b2a/` (deleted in the analysis cleanup, September 2026; carried in TODO-36 and TODO-71) (`stages.sh`, `cf_b3.py`, `compare.py`). Repeated prior-off
`theta_crossed` (s00_off 109/113/115, s10_off 29/33/35, s20_off 20/24/30 and 87/91/95) all ended
in a continue, as expected above (D2).
✅ B3 BUILT (T10, September 2026): `_replan_tasks` realizes every candidate and selects on
`RealizedPlan.cost` = T_r + δ, carrying the winner's δ as `UpdateResult.hold`; the all-unrealizable
fallback (TODO-30) replaces the `RuntimeError`; `cost_strategy` ("realized" | "plain") is the B3 switch
for the T6 ablation, `gate_strategy` the B2 one; all four combinations run. MEASURED (T10;
`analysis/t10_b3_realized/` (deleted in the analysis cleanup, September 2026; carried in the T10 entry of design_decisions.md, TODO-36 and TODO-79); s00/s10/s20/s30 × prior off/on): the decision sequences of `realized`+`none`
and `realized`+`b2a` are IDENTICAL in all eight conditions, and so are the regression greps and the
holds — B2 continued exactly where B3 keeps the current task, and both escalations (s30_on 21
all-unrealizable, s20_on 57 current task unrealizable) reach a B3 that decides as it would have
without the gate. So at ρ = 0.5 on these fixtures `b2a` is a computation saving (one realization per
trigger instead of one per candidate) and nothing else; the commitment role is still unexercised
(T4's finding holds with the new B3). For T6.
MEASURED (T6, September 2026; `analysis/t6_ablation/`; s00–s71 × prior, stop off / on; ρ ∈ {0.1, 0.25, 0.5,
1.0} as an existence test, not a selection). The clean commitment comparison is none + realized against
b2a + realized; b2a + plain is not an ablation cell, since B2 realizes the current task whatever
`cost_strategy` is (gate and cost are not independent axes). ONE commitment decision in the whole set:
s70 at ρ 1.0, tick 23, δ = 32 within the bound 34, b2a keeps item_1 with a 32-tick hold where B3 switches
to item_2; it lost to the switch (+15 ticks prior on, +13 prior off). At ρ 0.1 / 0.25 / 0.5 and on every
table convergence (s20, s30, s50) at any ρ, b2a decides as none: a crossing hold is B3's argmin, so
continuing and re-selecting coincide, and ρ moves the verdict counts without moving a decision. B2's
remaining purpose, holding the current task against argmin flips on small cost differences, is unexercised
by any fixture here; its evaluation waits for TODO-47. NOTHING ABOUT B2 IS DECIDED FROM THESE FIXTURES, and
no value of ρ is selected by them. The review also found a defect, fixed in the T6 wrap-up: `update()`
called B2 on a current task its own pool had just dropped as complete (s71_off 108: b2a continued item_1 one
tick after the world fact, two ticks late); B1.5 now treats a dropped current task as no current task, and
b2a + realized equals none + realized at ρ 0.5 in all 16 conditions.
Files: shared/meta_planner.py (`update`, `_is_current_task_plausible`, `_replan_tasks`)
Reference: Phase 4C block-design session, September 2026; wait-decision session, September 2026; R1; T4; T10; T-A1


**TODO-37 — IR: delivered items become geometric decoys; `?item` hardcoded in three places** ✅ RESOLVED (I3)
I3: (a) a delivered task is pinned at BELIEF_FLOOR from the tick its terminal completion
`obj_at(item, table)` holds (`[IR-complete]`), whoever delivered it — the decoy cannot exist.
(b) is moot: ZONE_BOOST is removed. (c) the held-item rule is removed; the phase model refutes a
rival through the geometry of its own expected action. History below kept as the record.
Found during Phase 4C B2 design (September 2026), scenario_00 run_20260904_131808.
Three separable defects; only the third is fixed.
UPDATE (I2, September 2026): the `?item` literals are gone — the recognizer names no
parameter; targets come from the planner's grounded actions (design_decisions.md, I2
entry). (b) is fixed by construction: the target zone is the zone of the chord target, so
the carried item's hypothesis gets ZONE_BOOST when the human enters the table's zone
(measured: 20–50 new firings per condition, `analysis/i2_ir_foundations/zone_boost_episodes.csv` (deleted in the analysis cleanup, September 2026; the folder's REPORT.md stays)).
(a) is SHARPER, not fixed: the carry chord now scores (it was NEUTRAL, TODO-46), so a
delivered item leads by ≈ 0.8 : 0.05 after the release instead of ≈ 0.35 : 0.3, and the
next task's approach is credited to it until the grasp — s00_on's second θ crossing moved
from step 81 to 111. What removes it is a completion event that pins the delivered task
(I1 C5), i.e. I3's phase model — not a target-resolution rule.

(a) After delivery, `world.object_locations[item] = kitting_table_0`, so
`_get_expected_position()`'s phase-1 branch resolves a delivered item's expected position
to the delivery target — geometrically identical to every subsequent human carry leg. The
completed task remains a full-weight attractor for the rest of the run. NOT FIXED.

(b) `_get_target_zone()` has no phase-2 branch, unlike `_get_expected_position()`. While
the human carries item X, `object_locations[X]` is the carrier's agent_id, so
`object_zones.get("human_0")` returns None (agent id looked up in an object dict — silent
miss, not an error) and the CORRECT hypothesis loses its ZONE_BOOST exactly when the human
commits, while the delivered-item decoy gains one. NOT FIXED.
Measured cost (leg session): grasp confidence is 0.797, not the 0.888 that pinning and
renormalizing the pre-grasp belief predicts — item_3's ×2 vanishes on the grasp tick. The
obvious fix, resolving the held item's zone from the holder's position, is WRONG:
ZONE_BOOST means "the agent is in the zone of this hypothesis's TARGET", and in phase 2 the
target is the kitting table; an agent is always in the zone of what it carries, so every
carrying hypothesis would get a permanent free ×2. The correct phase-2 branch mirrors
`_get_expected_position()`: target zone = the kitting table's zone. Under that fix there is
still no boost during the carry until the human reaches the table; 0.797 stands.

(c) No hard constraint from `holding`. FIXED — originally as LOW_LIKELIHOOD inside
`_likelihood()`; since the leg session it is a hard pin on OUTPUT (`_refuted_by_holding` /
`_output`, design_decisions.md "One leg is one observation"), and since I2 it reads
`AgentState.holding` and refutes any hypothesis binding a different *portable* object (no
parameter name). (a) and (b) still apply during the approach phase, when nothing is held.

Observed impact before the fix: belief converged to 0.995 on `deliver_item(item_7)` — a
task the ROBOT had completed 28 steps earlier and never a human task — driving both
meta-planner decisions at steps 46 and 57 against a fabricated human trajectory,
including the first-ever candidate exclusion (min_dist=0.309) and the first-ever
mid-task reselection.

DESIGN DEBT: the fix reads the literal `"?item"` from hypothesis bindings, matching
existing precedent in `_get_expected_position()` and `_get_target_zone()`. That makes it
three instances — structural rather than incidental domain leakage into `shared/`. The
clean form derives the held-item parameter from `TaskSchema.parameter_types` instead.
Deferred deliberately to unblock Phase 4C meta-planning.
Files: shared/recognizer.py (`_likelihood`, `_get_expected_position`, `_get_target_zone`)
Reference: Phase 4C B2 design session, September 2026

**TODO-38 — IR: collinear decoys — under the excess path separated only by the arrival fold; under the grade, by distance covered** [OPEN DISCUSSION — not decided]
Heading restated (graded-evidence session, September 2026). The "direction-only likelihood" below is the
cosine kernel, gone since I4; the excess-path likelihood also cannot separate targets on one bearing
(both at zero excess for the whole walk; handback §3.3, §4 (a)) — until the grade: two collinear targets at
distances d_near < d_far now separate DURING the walk, since the nearer target's covered fraction grows
faster (odds ratio u^{−x (1/d_near − 1/d_far)} after x walked). That is option (a) below in effect, with
its risk: a decoy on the true bearing BEFORE the target gains mid-walk, not only at its arrival fold. No
fixture has such a decoy; the collinear decoys in s20 lie BEHIND the true target, and s20_off's first
reveal stays at the arrival (20). Options (b)–(d) are as written; nothing decided.
Observed: scenario_20 (run_20260910_083630). shelf_6 lies nearly behind the human's target
shelf_3 (9°→20° off heading over the approach). Likelihood is cosine-only — distance plays no
role — so item_6/item_3 ratio stays 0.97–0.99 per step; confidence plateaus at 0.516 and θ is
crossed only by GRASP at step 22. A side decoy (shelf_4, angle opens to 60°) resolves fine.

Question: correct uncertainty or a weakness? Options, none decided:
(a) Distance term (boost closer targets). Risk: compounds multiplicatively (1.05^20 ≈ 2.65),
    confidently wrong when the far shelf is the real target; tie-breaker variant needs an ε cutoff.
(b) Passed-target refutation (distance starts increasing → refute). Real evidence, but only
    after passing the near target — no help when the human stops there.
(c) Sharper kernel, e.g. exp(κ·cos). Faster rejection of side decoys; no help for decoys behind.
(d) Leave as-is; treat collinear ambiguity as a fixture-design constraint.

Decide on IR-quality grounds with a controlled IR-only test, not to make a fixture fire earlier.
Files: shared/likelihood_functions.py, shared/recognizer.py
Reference: Phase 4C fixture-design session, September 2026

Update (fixture-design session): scenario_20 no longer depends on this — its early reveal is
planned via assignment_prior on plus a confidence-gated human projection (meta_planner,
pending). Decide TODO-38 on IR-quality grounds only.

Update (evidence-gated projection admission session): first MEASURED instance of
"confidence ≠ correctness" — previously only a noted risk. scenario_10, assignment_prior on,
run_20260910_144817, step 80: the human has finished item_2 and is walking to the coffee
machine; belief goes to `deliver_item(item_6)` at 0.783 (0.991 by step 85), `theta_crossed`
fires, and `update_human_projection()` admits a projection for a task the human is not
doing. The projection is well-formed, its hypothesis is admissible (item_6 is in human_0's
pool), it is above θ — and it is wrong. `coffee_break` peaks at 0.016 during the walk; with
the switch off the same walk converges on item_0 instead, so this is the direction-only
shape above, not the restriction. `coffee_break` never becomes `most_likely` in any run,
including the unmodified prior-off baseline.
Bears on B2 (TODO-36) rather than on the recognizer: an admitted projection must not be
treated as ground truth, and B2's design should not assume otherwise.
CORRECTION (leg session): the 0.991 was duplicate counting (design_decisions.md, "One leg is
one observation") and `coffee_break`'s 0.016 was ω/renormalization — it receives no chord
evidence at all (TODO-46). After the leg change the same walk still crosses θ on item_6,
at 0.853 (step 107, switch on): one honest chord 27° off shelf_6 plus ZONE_BOOST. The
"confidence ≠ correctness" finding stands, on a smaller number.

Update (leg session) — SCOPE FOR THE NEXT TASK: this is the B2 unblocker, not cleanup. With
one chord per leg, the kernel alone decides whether any mid-approach reveal exists:
linear (current) → 0.64 on one chord against two alternatives, crossing at the grasp;
normalised von Mises σ ≤ 30° → 0.82–0.88, crossing at step 1; σ = 45° → 0.69, the grasp.
After this lands σ is LOAD-BEARING for every downstream B2 result — record any B2 finding
together with the σ it was obtained under. Includes the NEUTRAL merge: under a kernel
normalised as a density ratio against uniform, `unknown` = 1 by construction and the
current inconsistency (linear kernel circle-mean 2.05 vs NEUTRAL = 1.0, which handicaps
`unknown` 2× against a random heading) disappears without a separate constant. Decide σ
with a controlled IR-only test, ideally against recorded human walks when ROS resumes; do
not tune it toward a fixture.

**TODO-39 — Migrate `domains/dock_loading/scenarios.py` to `assigned_tasks`**
`AgentConfig.assigned_tasks` was added and all three kitting scenarios migrated; dock_loading
still declares only `scheduled_tasks` for both agent types. It imports and loads fine — empty
`assigned_tasks` skips `__post_init__` validation by design — but `SimModel._spawn_agents()`
already seeds robots from `assigned_tasks`, so a dock_loading robot gets an **empty task pool
today**: a dock_loading run has an idle robot right now, with no exception raised. Migrate
before running dock_loading again: humans get `assigned_tasks` = their non-foreseeable
`scheduled_tasks`; robots get `assigned_tasks=` in place of `scheduled_tasks=`.
Files: domains/dock_loading/scenarios.py
Reference: assignment-prior session, September 2026

**TODO-40 — Assignment prior strengthens TODO-37(a)** ✅ RESOLVED
The persistent assignment prior up-weighted an assigned hypothesis by 10× for the whole run,
including after that task was complete. Combined with TODO-37(a) — a delivered item's expected
position resolves to the delivery target, geometrically identical to every later human carry
leg — a *delivered assigned* item was a 10× decoy on every subsequent approach leg.
RESOLVED (Sept 2026): there is no 10× any more — the pool is a support restriction (see
design_decisions.md, "Assigned-task pool is a support restriction, not a prior"), and every
admissible hypothesis carries unit weight. A delivered assigned item may still be a decoy,
at unit weight; that residual is TODO-37(a) itself, unchanged.
Files: shared/recognizer.py
Reference: assignment-prior session, September 2026; resolved in the evidence-gated
projection admission session, September 2026

**TODO-41 — `ros_sim/planner_2.py` reads robot `scheduled_tasks`, now empty**
`ros_sim/framework_HRI/framework_HRI/planner_2.py:252` builds its task queue from
`scenario_10.agents["robot_0"].scheduled_tasks` (kitting). After the `assigned_tasks`
migration that list is empty, so the ROS planner would silently get **zero tasks** — no
exception, just an idle robot. ROS is paused, so this was flagged rather than fixed. Change to
`.assigned_tasks` when ROS resumes; check for other readers at the same time.
Files: ros_sim/framework_HRI/framework_HRI/planner_2.py
Reference: assignment-prior session, September 2026

**TODO-42 — `DomainModel.intentions` is a `Set`, so hypothesis order is nondeterministic** ✅ RESOLVED for the recognizer (I2)
The recognizer sorts its hypothesis list by key at construction, builds the initial prior in
that order, and emits pinned keys in sorted order, so `most_likely` tie-breaks and `[IR-dist]`
order are functions of the hypothesis space only. Measured: scenario_40, both prior settings,
byte-identical on `[meta]`, `[IR]`, `[IR-dist]`, `[meta-cand]` under PYTHONHASHSEED=0, 1 and 2.
`get_all_intentions()` itself is still unordered (nothing downstream depends on its order now);
keep PYTHONHASHSEED=0 in the regression recipe until every other consumer is checked.
Tie-breaks are now alphabetical by key (t=0 prior-off winner in s00 is item_2, was the
layout's first item) — reproducible, not meaningful, as noted below.
`DomainModel.intentions: Set[str]` (`shared/types.py`) and `get_all_intentions()` returns
`list(self._domain.intentions)`. Python randomizes string hashing per process, so that list
comes out in a different order on every run — five fresh processes gave three different
orders. `build_hypothesis_space()` iterates it, so `self._hypotheses` order, and therefore
`BeliefState.distribution`'s insertion order, varies per run. Consequences:
(a) `[IR-dist]` emits tied entries in a different order run-to-run (`sorted(key=-v)` is
    stable), so byte-identical log diffing fails spuriously;
(b) `max(distribution, ...)` breaks exact ties by insertion order, so t=0 `most_likely` — and
    the human projection the meta_planner builds from it — is nondeterministic when the
    initial prior is uniform and no evidence has arrived.
A deterministic order makes tie-breaks reproducible, not meaningful: with a uniform prior, t=0
`most_likely` is still whichever hypothesis comes first — for single-intention layouts, the
first item in the layout JSON (e.g. scenario_20's item_4).
Only visible when a layout's hypothesis space holds more than one intention type: env_layout1
(scenario_10) does, env_layout0/env_layout2 do not — their coffee_machine/ac_switch types are
absent, so only `deliver_item` hypotheses exist and there is nothing to reorder. This is
pre-existing, not introduced by the assignment prior; it was found while regression-diffing
that change and worked around with `PYTHONHASHSEED=0`.
Candidate fix: give `get_all_intentions()` a deterministic order (e.g. `sorted()`, or make
`intentions` an ordered collection). Tie order in logs will change when it lands — re-baseline
after fixing, do not treat that diff as a behaviour change.
Files: shared/types.py (`DomainModel.intentions`), shared/domain_knowledge.py
(`get_all_intentions`), shared/recognizer.py (`build_hypothesis_space`)
Reference: assignment-prior session, September 2026

**TODO-43 — A no-op `update()` costs the robot one tick** ✅ RESOLVED (T5)
When a trigger fires and B3 re-selects the task already executing, `RobotAgent` reloads the
plan (`[executor] _load_plan`) and the robot loses that tick. scenario_20, assignment_prior
off: the step-22 `theta_crossed` re-issues item_4 and the robot grasps at step 23; with the
prior on (no trigger at step 22) it grasps at step 22. Every later event shifts by one step,
and projection distances shift with it (`task_committed` item_4 min_dist 4.9 vs 24.9 — one
step of arrival gap). Harmless at today's trigger rate; a real cost once B2 fires often, since
every "continue" would stall the robot. Fix direction not decided; candidate: keep the
current plan when `UpdateResult.current_task` is the executing task.
FOUND (T5, `analysis/t5_continue/` (deleted in the analysis cleanup, September 2026; carried in TODO-43 and the T5 entry of design_decisions.md)): the loss has exactly one cause and one tick. A reload
resets the executor's cursor to the fresh plan's first action; if that action is one the world
already shows complete and the executor had ALREADY acknowledged it (advanced past it on the
previous tick), the tick is spent acknowledging it again. That is the tick after an arrival
acknowledgement — the grasp or release tick. Mid-walk a reload costs nothing (`expand()`
re-derives the same straight path from the current position), and on the acknowledgement tick
itself the reload does what a no-trigger tick does. At HEAD before the fix no continue in the
eight sweep conditions landed on a grasp/release tick — the prior-off triple crossings (s00_off
109/113/115, s20_off 87/91/95) are the HUMAN's grasp stop while the robot walks — so the sweep
was losing 0 ticks; the step-22 measurement above predates the recognizer rework that moved the
trigger ticks. Isolated with an injected trigger: a continue on s00_off 6 or 30, s30_off 47 or 85
lost one tick each before the fix and none after. The scenario_30 cancel-and-return attributed
to this loss is not in the record (no `deliver_with_return` execution in any baseline log).
DECIDED: a continue costs nothing; re-decomposition stays (never resumed); identity is
`task_instance_key()`; no plan cursor in `shared/`; no new decision path (design_decisions.md,
"A continue decision costs nothing"; io_contracts.md §1.9 / §2.2 / §4.1).
IMPLEMENTED: `RobotAgent.step` tests `task_instance_key(result.current_task)` against the
executing task's key (the `is` test is gone) and on a continue hands the fresh plan to
`Executor.continue_plan()`, which moves the cursor to the in-flight action if the fresh plan
contains it (GroundedAction equality) and keeps the microaction queue and completion
bookkeeping; otherwise the plan loads from its start as before (the `task_committed` case,
where `deliver_already_held` has no `pick_up`; the case is removed by D3). Sweep: decisions and `[IR]`/`[IR-dist]`
byte-identical to the T7/T8 baselines; `[meta-cand] min_dist` differs in the 14th–16th digit
where the kept queue's points replace re-interpolated ones. New baselines: `analysis/t5_continue/new/` (deleted in the analysis cleanup, September 2026; carried in TODO-43 and the T5 entry of design_decisions.md).
Files: mesa_sim/sim_agents.py (`RobotAgent.step`), mesa_sim/executor.py (`continue_plan`),
analysis/t5_continue/ (deleted in the analysis cleanup, September 2026; carried in TODO-43 and the T5 entry of design_decisions.md) (inject.py, compare.py, summary.md)
Reference: fixture-design session, September 2026; T5 session, September 2026

**TODO-44 — `assignment_prior` config key and CLI flag are misnamed**
`configs/experiment.yaml: assignment_prior` and `--assignment_prior` now switch a support
*restriction*, not a prior — nothing is weighted (design_decisions.md, "Assigned-task pool is
a support restriction, not a prior"). The name is a leftover from the first build. Also
reaches `SimModel.assignment_prior`, `run_mesa.py`'s argument plumbing, and the `[IR-prior]`
log tag. Flagged only; renaming was explicitly out of scope for the session that made the
switch a restriction, and touches files outside `shared/`.
Files: configs/experiment.yaml, mesa_sim/run_mesa.py, mesa_sim/sim_model.py,
mesa_sim/sim_agents.py
Reference: evidence-gated projection admission session, September 2026

**TODO-45 — Deferred idea: admit a projection when the admissible non-`unknown` set is a singleton**
With the restriction on, a human with one remaining assigned task has an admissible set of
{that task, foreseeable tasks, `unknown`}. The idea: treat "the human has one task, so we
know what they're doing" as sufficient to admit a projection without waiting for
`belief.confidence >= theta`. Rejected for now: it would have to ignore the foreseeable tasks
and `unknown`, i.e. assume the human will not deviate at exactly the moment there is no
evidence either way — and a foreseeable deviation is the case the robot most needs to catch.
Revisit once results with the θ gate are in, and only if the wait for θ is shown to cost
something.
Files: shared/meta_planner.py (`update_human_projection`)
Reference: evidence-gated projection admission session, September 2026

**TODO-46 — IR has never used completion evidence; only phase-1 shelf approach ever scores** ✅ RESOLVED (I2: (2), (3); I3: (1))
I3: the likelihood is that of the action the hypothesis expects now, so `pick_up`'s completion is
evaluated at every grasp for the hypothesis that expected it — `holding(human_0, item_X)` HIGH,
×4, in all eight conditions (`analysis/i3_phase_model/completion_events.csv` (deleted in the analysis cleanup, September 2026; the folder's REPORT.md stays)). `place` is never
reached by the channel: the task's terminal completion holds on the same tick and the pin
preempts it. No completion check ever returned LOW in the sweep (items sit on distinct shelves, so
no two hypotheses expect a grasp at once; check U4 shows the ×40 discrimination when they do).
I2: `_get_expected_position()` is gone; the target is the first movement action of the
planner's guard-selected method, grounded through task and step bindings and resolved by
`shared/target_resolution.py`. Measured (`analysis/i2_ir_foundations/summary.md` (deleted in the analysis cleanup, September 2026; the folder's REPORT.md stays)): 0 unresolved
targets in all eight conditions (was 64/261/61/54 per scenario); the carry chord scores
(0.797 → 0.966 mid-carry in s00/s20/s30); `coffee_break` gets the coffee walk (s40: 0.81, θ at
142). (1) — completion evidence at GRASP/RELEASE — is still unreachable because `move_to`
answers first in dispatch order; that is the per-hypothesis phase (I3), not target resolution.
One root cause, three symptoms. `_get_expected_position()` returns `None` — hence NEUTRAL —
whenever the target binding it inspects is a `Var` rather than a `Const`:
(1) Completion evidence is unreachable. `_likelihood()` returns from the FIRST schema in
    `methods[0]`'s decomposition; for `deliver_item` that is `deliver_already_held`, whose
    first step is `move_to` (progress branch), so `pick_up`/`place` completion predicates
    are never evaluated for any observation.
(2) Phase-2 carry targets are unresolvable: the last `move_to` binds `?target` to
    `Var("?kitting_table")`, so the carried item's hypothesis is NEUTRAL for the whole carry.
(3) Parameterised foreseeable targets are unresolvable: `coffee_break`'s `move_to` binds
    `?target` to `Var("?coffee_machine")`, so `coffee_break` has never received directional
    evidence; the walk to the coffee machine is credited to the nearest shelf hypothesis.
Net: the recognizer's ONLY working evidence path has ever been phase-1 shelf approach for
`?item` hypotheses, plus held-item refutation of the alternatives. Every "grasp reveal" and
"carry reveal" in every run to date was the held-item refutation; `unknown` has never been
refuted by anything but a chord. The failed coffee-leg criterion in the leg session
(scenario_10 switch on, `theta_crossed` at 107 on item_6 at 0.853) is a known consequence.
Fix direction: resolve task-level parameter bindings (`hyp.bindings`) when a step_call term
is a `Var` — the same lookup `_resolve_term_value()` already does for completion predicates
— and dispatch completion checks over the method whose vocabulary matches, not
`methods[0]`. A finding about the IR, not a footnote; deferred from the leg session so that
change stayed one semantic change.
Files: shared/recognizer.py (`_likelihood`, `_get_expected_position`, `_get_target_zone`,
`_get_relevant_action_schemas`)
Reference: leg-level evidence session, September 2026

**TODO-47 — Stress-test harness: randomised layouts, scenarios, parameters** [post-4C] — (d) end-state variant and (e) evaluation fixtures ✅ BUILT (F47, retyped F47b); (f) B3.B fixtures noted; (g) the gate's reopening condition noted — MOVED to T-F (T-A1); (f) is T-B's two-table fixtures
REVISED (T-A1, September 2026): the randomised harness is part of T-F (evaluation), not the next step
after 4C. What stays earlier: (f) is T-B's hand-built two-table layouts (below), and (a) programmatic
registration is built as the first part of fixture generation, in T-B, for them. (b) is reduced: its
separation half is removed by the T-A1 decision that `min_separation` is supplied by the body in
physical units (TODO-28), and β is not a scale-calibration item either (TODO-58). No value is rescaled
with the layout. (d), (e) stand as built; (g) is carried into T-F.
Plan: run every B2.X × B3.X combination over hundreds of generated simulations (randomised
layouts, scenarios, parameters) and compare outcomes. Not seed repetition — the sim is
deterministic under PYTHONHASHSEED=0, so variation must come from generated inputs.
Prerequisites:
(a) Programmatic layout/scenario registration — adding a layout today needs three manual
    edits (layout JSON, `scenarios.py`, `registry.py`).
    TRIED AND REVERSED (T-B1b, September 2026). A generator (`fixture_generation.py`: a layout builder,
    a delivery-scenario builder, a registration call; `fixture_two_tables.py` as its first user) was built
    for env_layout8 (e76e4e0) and removed again in the same task. Reason: fixtures are read by people, so
    they are written as literals. A fixture that cannot be read in `scenarios.py` cannot be checked by a
    person, and that outweighs saving the three manual edits. scenario_80 / scenario_81 are literals in
    `scenarios.py`, registered the ordinary way; `env_layout8.json` is an ordinary committed layout. The
    generator only reproduced what the literals state, so it was deleted rather than kept to drift. Whether
    the randomised harness (T-F) needs programmatic registration is left to its design; nothing is kept
    here for it.
(b) Scale-relative calibration — `min_separation` (formerly `min_safe_distance`, TODO-28; and
    any B2 reference for δ, TODO-36) must be expressed relative to layout scale or agent
    speed × steps, not as an absolute read off one fixture.
    REVISED (T-A1): withdrawn for `min_separation`, which is a distance the body supplies (a standard
    sets it; TODO-28), and for β, a physical tolerance fixed on IR grounds (TODO-58). ρ is already a
    share of the human's remaining horizon. Nothing of (b) remains to calibrate.
(d) The human's end state as a condition (R2): the current scripts leave the human idle at the
    kitting table after its last task, so with the separation stop on the robot's last delivery is
    refused until the cap (C). A variant in which the human steps aside after its last task is the
    second condition, to be reported side by side with the first (blocked time,
    `analysis/c_separation_stop/blocked.py`).
    ✅ BUILT (F47, retyped F47b, September 2026): `scenario_50` on `env_layout5` (= env_layout2 + a
    coffee machine 500 cm east of the table; a waypoint `rest_0` until F47b, an ill-typed binding):
    scenario_20 with a third human task, `coffee_break(coffee_machine_0)`, after its last delivery.
    Stop on: completes at 237 / 239 (prior off / on) where scenario_20 is refused at the table from 144
    to the cap. The machine makes `coffee_break` a live hypothesis from t=0, so the recognizer's set
    differs from scenario_20's: prior-on the first crossing and the hold move from 6 to 8. Read with
    scenario_20, not instead of it. `analysis/f47_fixtures/`.
    STILL OPEN FOR env_layout9 (T-B1b follow-up, September 2026): if layout9 ever becomes a measured
    fixture, its end state needs handling first. In scenario_90 the sampled separation is below
    `min_separation` (50 cm) from tick 358 to the end of a 500-step run — after the robot's last delivery
    at 361 — with both agents standing idle near kitting_table_1, which is where the human finished and
    where three of the robot's four deliveries go. Nothing during the work falls below it. The same
    end-state condition (d) is about, on a layout that has no variant for it yet.
(e) FIXTURES FOR D2 (F47 / F47b, September 2026): the condition on which D2's blocked-execution event and
    its reaction policy (wait, or reconsider and return) would differ is a human stay at a place the robot
    needs, mid-run, finite, with another task in the pool. F47 produced it with `coffee_break` bound to a
    waypoint — ill-typed (no coffee machine), retired in F47b (`analysis/f47_fixtures/`). F47b built the
    natural, well-typed configuration: `env_layout7`, `scenario_70` / `_71` — a real coffee machine on the
    robot's route to its first shelf, the human's shelf beside it, the human's break there, then its
    delivery, then the AC switch by the east wall; the alternative shelf beside the blocked one or across
    the table at the same distance (the F47 one-variable design). MEASURED: `coffee_break` crosses θ at
    tick 23, two ticks before the stand (25–55), and realization absorbs the projected wait — scenario_70
    switches to the alternative (no `[stop]`, done 187), scenario_71 holds 32 ticks and then meets only the
    human's departure (3 refused steps at 57–59 past T_h, done 207). NO VALID FIXTURE PRODUCES A MID-RUN
    BLOCK: a stay the projection carries is priced, so the blocked event is exercised only past T_h and by
    deviations (design_decisions.md, "Scheduled bindings are typed; a stay the projection carries is
    absorbed"). The short / long variants therefore have no valid instance; what varies between 70 and 71 is
    the planning response (switch vs hold). A principled unforeseen stay needs declared human behaviour
    outside the robot's domain knowledge (TODO-80). D2's evaluation uses scenario_20 / scenario_50 (the
    end-state pair, the tail block) and scenario_70 / _71 (the absorbed stay, the departure tail).
(f-designations) A DESIGN NOTE FOR ANY SCENARIO WITH MORE THAN ONE DESTINATION (T-B1b follow-up, September
    2026): in the current two-table scenarios most items are designated to the table NEAREST their shelf —
    5 of 6 in env_layout8 and 5 of 6 in env_layout9 (measured). That makes the destination fact nearly
    redundant with geometry: it weakens the ordering difference the fixture is for, and it weakens the
    recognizer's discrimination on the carry leg, since the table a carry heads for is the one proximity
    would have guessed. In both layouts the whole ordering effect rests on the single against-proximity
    item (env_layout8's item_4, farther by 64.9 ticks; env_layout9's item_1, by 26.8). Scenarios built to
    EVALUATE the algorithms must set designations deliberately, against proximity where that is what the
    test needs. The designations are Hadi's to decide per scenario, not to be left to follow from the
    layout. design_decisions.md, "An item's destination table is a fact of the station" (the fact is the
    station's; which station is a design choice).
    WHAT THIS SCOPES T-B3a TO (T-B1d, September 2026; supersedes the paragraph below). single_task takes the
    cheapest task from the robot's position; full_reorder takes the task whose delivery leaves the robot best
    placed for the remaining shelves; the two heads differ exactly when the cheapest-from-here task ends at a
    table far from the remaining shelves, which the destination fact decides. Across nine designation sets
    priced on env_layout8's geometry the heads differ in seven (gaps 14 to 78 ticks) and coincide in two;
    every flip traces to the one designation that moves the cheapest single task — the mechanism, not a
    weakness of any fixture. Generality across layouts is T-F's (randomised layouts), not a hand-built
    scenario's. `analysis/tb1d_designations/README.md`.
    SUPERSEDED (T-B1d): T-B's ordering result rests on a SINGLE against-proximity item in each
    layout (item_4 in env_layout8, item_1 in env_layout9), so any claim drawn from T-B3a is scoped to that
    fixture: it shows that ordering matters WHEN AN ITEM IS DESIGNATED AWAY FROM ITS NEAREST TABLE, not
    that reordering helps in general on a two-table station. An evaluation scenario meant to support the
    general claim needs SEVERAL against-proximity designations, or a geometry in which proximity does not
    order the tables cleanly. `analysis/tb1b_two_tables/README.md`, "What this fixture does not settle".
    A FINDING FOR T-B3, FROM T-B2c (September 2026): on every current fixture NO WINNING ORDERING UNDER `full_reorder` CARRIES A HOLD (scenario_80, scenario_81,
    scenario_00, both priors; every hold sent is 0 and every `[meta-win]` line reads `holds=0,...`), so T-B2c
    changes NOTHING EXECUTED against T-B2b. scenario_81 does not exercise realized cost under `full_reorder`: its
    conflict belongs to `single_task`'s course (heads 6, 1, 7, 4: the 4-tick hold before item_1 at step 39), and
    the course `full_reorder` chooses (7, 4, 6, 1) never meets the human (0 of the 206 orderings priced on that
    course carry any hold; the 12 that do, 8 of them before a later entry, are all priced on `single_task`'s
    course). Its saving (completion 220 against 265, world fact) therefore MIXES TWO CAUSES, the order of the
    tasks and not meeting the human, and cannot be attributed to either. A FIXTURE FOR T-B3b MUST PUT A CONFLICT
    INTO THE ORDERINGS `full_reorder` WOULD CHOOSE. Hadi designs it; no scenario, designation or constant is
    adjusted to make an effect appear.
    `analysis/tb2c_per_entry_holds/README.md`; design_decisions.md, "One hold per entry".
(f) B3.B (`full_reorder`, not in 4C): a future fixture needs SEVERAL remaining robot tasks whose ORDER, not
    only the next choice, changes cost under a human stay. Not built; every current fixture leaves the robot
    at most one alternative at the stay.
    REVISED (B3.B design revision, September 2026): "several remaining robot tasks whose order changes
    cost" now means TWO-TABLE KITTING LAYOUTS: a second object of type `kitting_table`, items assigned per
    table through the existing `?kitting_table` binding (no domain change), so that a task's end position,
    and with it the walking cost of the tasks after it, depends on the order. The coupling is geometric
    and present with no human; a human stay is not required for the order to matter, only for the
    realized-cost comparison. Hand-built fixtures for the B3.B build (layout JSON, `scenarios.py`,
    `registry.py`), before and independent of the randomised harness; not built yet. They evaluate
    B3.A against B3.B and set no parameter. To measure on them, outside B3.B: the hypothesis space is
    items × tables, so with the prior off the human's belief is expected to split between the two table
    hypotheses of an item until the carry walk. DESIGN-16 (revised); design_decisions.md, "B3.B
    (`full_reorder`) is lookahead for the choice of the next task, built next".
    T-B1 (T-A1, September 2026): a layout with a second table on the opposite side and each item
    assigned to one table. Example: items 4 and 6 to the north table, item 7 to the south table; from
    the north table item 7 is the far task, so (4, 6, 7) and (4, 7, 6) differ in walking cost with no
    human present, which single-task selection cannot see. DESIGN QUESTION, OPEN, to settle before the
    layout is written: is an item's destination table a DOMAIN fact (one hypothesis per item; the
    recognizer knows the table from the domain model) or a WORK-ORDER fact (hypotheses items × tables,
    restricted by the assignment prior)? Under the second reading the belief is expected to split
    between an item's two table hypotheses until the carry walk, so the human projection is admitted
    later. design_decisions.md, "B3.B ... THE FIXTURE SIDE".
    RESOLVED (T-B1a, September 2026): a fact of the station, the layout's `"destination"` per item; one
    hypothesis per item, the table determined from the item (`determined_parameters`). design_decisions.md,
    "An item's destination table is a fact of the station". TODO-86 / TODO-87 record what it leaves open.
    ✅ BUILT (T-B1b, September 2026): `env_layout8`, `scenario_80` (plain cost, ordering isolated) and
    `scenario_81` (a conflict in the second task of an ordering). Robot pool item_1 / 6 / 4 to
    kitting_table_0, item_7 to kitting_table_1: the cheapest single task from the start is item_6
    (39.3 ticks), the cheapest full ordering starts with item_7, and greedy is 41.4 ticks worse. The
    fixture settles the choice of head, not the tail (the two best orderings differ by 2.2 ticks). The
    permutation table, the runs and the baselines: `analysis/tb1b_two_tables/README.md`.
    ✅ T-B1c (September 2026): `scenario_83` exists as the existence case in which realized cost changes the
    head under `full_reorder`; `analysis/tb1c_realized_flip/`. `scenario_84` (several against-proximity
    designations) is T-B1d, not started.
(g) THE GATE'S REOPENING CONDITION (gate ruling, September 2026): a walk crossing of θ with a live rival at
    similar odds (top-two ratio near 1 at the crossing), where the normalised share and a margin gate would
    disagree. No current fixture shows one (lowest top-two ratio at a walk crossing 5.23, s00_off 37).
    Report it where the generated fixtures produce it (the crossing tick, top odds against `unknown`, the
    ratio of the top two, the live set, as in `analysis/g1_graded_evidence/crossings.md`); do not build a
    fixture for it. TODO-64 / 65, design_decisions.md, "The gate stays a fixed share".
(c) Fixture gap (T1, `analysis/t1_conflict_measurement/REPORT.md` §(a), §(c)): no current
    scenario has a correct-hypothesis *crossing* on the robot's current task. The only
    correct-hypothesis crossings measured are the never-selected item_7 alternatives in
    scenario_20 (robot approach across the human's carry path); every conflict on a current
    task is co-directional convergence into the kitting table. B2 continuation will therefore
    only be exercised on table convergence until a crossing fixture exists.
Also: B2.B+B3.A must select identically to none+B3.A under the same `_cost()` — treat as an
assertion in the harness; any divergence is a bug. Only projection count may differ.
Files: domains/kitting/registry.py, domains/kitting/scenarios.py, mesa_sim/run_mesa.py,
shared/meta_planner.py
Reference: Phase 4C B2/B3 session, September 2026

**TODO-48 — Hypothesis change above θ fires no trigger** ✅ CLOSED (D2, September 2026)
✅ CLOSED (D2): `recognition_changed` fires when `belief.most_likely` leaves the hypothesis the last decision was
projected against, above or below θ — a consequence of the one condition, not a case. design_decisions.md, D2 entry.
`theta_crossed` fires on a confidence crossing (`prev < θ ≤ now`), not on a change of
`most_likely`. If belief moves from one hypothesis to another while confidence stays ≥ θ
(e.g. a grasp pins the old top hypothesis and mass jumps to a new one in the same tick),
no trigger fires, B2 never runs, and the robot keeps the last trigger's projection until its
next grasp or task boundary. B2 is the mid-task evidence mechanism; this is the correction
case it cannot see. Candidate fix, undecided: fire on `most_likely` change while ≥ θ.
First measure whether it occurs in current scenarios.

Measured (T1, `analysis/t1_conflict_measurement/REPORT.md` §θ-flip scan, all six baselines,
PYTHONHASHSEED=0): it does not occur. UPDATE (I2): it now does — scenario_30, assignment_prior
on, step 98: `most_likely` flips from the delivered item_3 (0.782, ≥ θ) to item_7 at its grasp
(0.876) and no trigger fires; the robot keeps the projection built at step 39 (a task the human
finished at 73). Cause: the delivered-item lead created by scored carry legs (TODO-37(a),
I2). UPDATE (I3): with the completion pin the delivered item_3 is at BELIEF_FLOOR from 74, and
item_7's grasp at 98 is a `theta_crossed` again (0.885) — the flip is gone in the sweep. A new
shape appears instead: `theta_crossed` fires on `unknown` (s20_off step 136, 0.804) when the robot's
own delivery pins a live hypothesis and `unknown` inherits the mass — the meta-planner then builds a
projection from `unknown`. Meta-planner is paused; recorded, not handled (TODO-54). 0 of 25 `most_likely` changes happen with confidence
≥ θ at both the tick and the previous tick — 16 have both sides below θ, 6 are collapses
from ≥ θ to well below after the human's task completes, 3 coincide with a `theta_crossed`
trigger on the same tick. DEFERRED ON EVIDENCE: revisit when new scenarios exist
(TODO-47), not before — superseded by the I2 measurement above.
Files: shared/meta_planner.py (evaluate_triggers)
Reference: Phase 4C B2/B3 session, September 2026; T1 measurement session, September 2026; I2

**TODO-49 — Type-name mismatch between layout and schema silently empties a task's hypothesis space** — (2) binding part ✅ BUILT (F47b); (1) and (3) still proposed
`build_hypothesis_space()` does `known_objects_by_type.get(type, [])`; a task whose parameter
type has no object in the layout gets zero hypotheses. Legitimate when the layout genuinely
lacks the object (s00/s20/s30 have no coffee machine — DESIGN-14), a silent modelling error
when it is a spelling mismatch: `env_layout1.json` declared `AC_switch` against
`parameter_types` `ac_switch`, so scenario_10's scripted `ac_activation` was unrecognisable
for the whole life of the scenario and every audit count said "coffee_break is the only
foreseeable hypothesis" (fixed in I2: the layout now spells `ac_switch_0` / `ac_switch`, the
id the script already used). Proposal, not built (I2 report §6):
(1) `build_hypothesis_space()` logs one `[IR-space]` line per intention with its hypothesis
    count, so the log states which tasks are recognisable in this layout;
(2) a scenario's `scheduled_tasks` are validated at spawn: every scripted task's key must be in
    the hypothesis space, and every bound object id must exist in the layout — an error, not a
    warning, because the human is about to execute a task the robot cannot recognise, and no
    fixture can mean that on purpose;
(3) a parameter type that matches a layout type case-insensitively but not exactly is an
    error at hypothesis-space construction.
(1) is a log line; (2) and (3) are the small validation this needs, in `SimModel._spawn_agents`
/ `build_hypothesis_space`, not a framework.
✅ BUILT (F47b, September 2026), the binding part of (2): `shared.types.check_task_bindings(task,
object_type_by_id)` — every bound object must exist in the layout and every parameter the schema types must
be bound to an object of that type — is called in `SimModel._spawn_agents` for every agent's scheduled AND
assigned tasks; a mismatch raises (an error, not a warning). Result over the registered fixtures: scenario_40
(`ac_activation` at the waypoints wander_0 / wander_1) and scenario_50 as first built (`coffee_break` at the
waypoint rest_0) failed and were fixed by retyping the targets at the same coordinates (env_layout4:
`ac_switch_1` / `ac_switch_2`; env_layout5: `coffee_machine_0`); scenario_60/61 failed and were retired
(`analysis/f47_fixtures/`). STILL PROPOSED: (1) the `[IR-space]` line; (3) the case-insensitive type clash at
hypothesis-space construction; and the other half of (2), "every scripted task's key is in the hypothesis
space" — the type check implies it whenever the type has objects, but a scripted task whose parameter type has
no object at all is still refused only through the missing-object error, not stated as such.
NOTE (R1, September 2026): the scenario_10 / `env_layout1.json` statements above PREDATE the cleaned
`env_layout1` (no obstacles; coffee machine and AC switch side by side at x = −875, item_1 on the
shelf near them; the human's script and the robot's pool rewritten) and are STALE as descriptions of
the current fixture. The old layout with obstacles is kept as `env_layout99.json`, not registered.
The spelling fix itself (`ac_switch`) carries over.
Files: shared/recognizer.py (build_hypothesis_space), mesa_sim/sim_model.py
Reference: I1 audit 3.8, F1 report §1, I2 IR foundations session

**TODO-50 — A foreseeable task that is never completed becomes a permanent attractor** ✅ RESOLVED (I3)
I3: `coffee_break` is pinned at BELIEF_FLOOR at step 184 of s40 — the first tick
`waited(human_0, coffee_machine_0)` holds — and stays pinned (completion latches; the fact itself is
visible for three ticks only). It is never `most_likely` again; 0.001 at the grasp of item_6 (was
0.96). No decay, no refutation of foreseeable tasks. What it did NOT give: `coffee_break` ≥ θ during
the coffee walk (max 0.551 off / 0.645 on; I2's 0.81 at 142 was a ZONE_BOOST event), and `item_6`
is not `most_likely` at its grasp at 272 (0.29–0.32; `ac_activation` 0.48–0.53, TODO-53) — it is
from the first carry tick (274). History below.
Since I2 `coffee_break`'s target resolves, so it collects the coffee walk (correct) — and then
keeps its lead for the rest of scenario_40: it is never refuted by a grasp (no portable object
in its bindings), nothing marks it complete, and later legs still hand it moderate chord
credit (the walk away from the machine is 64° off it, L ≈ 2.9, better than any shelf). Measured
(`analysis/i2_ir_foundations/f1_traces/` (deleted in the analysis cleanup, September 2026; the folder's REPORT.md stays)): `most_likely` from step 118 to the end of the run,
0.96 at the human's grasp of item_6 (272), 0.89–0.90 while the human is idle. This is I1's C5
(no completion event) in its clearest form and the reason I2 made `wait_at` observable
(`waited(agent, entity)`, visible at steps 184–186): I3's phase model can complete
`coffee_break` on it. Do not add a decay or a refutation for foreseeable tasks — the fixture
shows the missing piece is completion, and its numbers are the reference for I3.
Files: shared/recognizer.py
Reference: I2 IR foundations session; analysis/i2_ir_foundations/REPORT.md §4

**TODO-51 — Per-tick method re-selection scores every other delivery against the held item's home shelf**
While the human carries X, `deliver_item(Y)` for every Y ≠ X selects `deliver_with_return`,
whose first movement is to X's home container — behind the human on every carry — so all of
them collect L ≈ 0.1 per carry leg under the held-item pin, and return after the release at
≈ 0.02–0.14 against the delivered item's 0.8 (I2 report §4). Two readings, both on record:
(a) correct — the domain says a human who wanted Y while holding X would return X first, and
    this human did not; the delivered item's lead afterwards is C5, fixed by completion;
(b) evidence for hypotheses under a hard refutation should not accumulate at all (they are
    refuted, not scored), in which case the pin should freeze their evidence — a change to
    the evidence model, I3/I4's.
The evidence that settles it: with I3's completion pin in place, do the next-task reveal
times (s00_on 81 → 111, s20_on 82 → 89, s30_on 77 → none) return to or improve on baseline?
MEASURED (I3): they do not, and the phase model does not remove the effect — it reproduces it
through the walk. While the human holds X, `deliver_item(Y)`'s guard-selected method is
`deliver_with_return`; the walk finds `move_to(shelf_X)` complete (`at(human, shelf_X)` at the
grasp), so the expected action is `place(X, shelf_X)` for two ticks and then, once the human is
30 cm away, `move_to(shelf_X)` from an origin on the table side of the shelf: chord ≈ 180° off,
L ≈ 0.1 for the carry, folded at the release (`rival_phase.csv`). The delivered item is pinned at
the release, so the rival no longer fights the 0.8 lead — but it fights `unknown` from a 1 : 3–8
deficit, and the kernel gives ×4 per leg: next-task crossings at the grasp in every prior-on
condition (s00_on 111, s20_on 89, s30_on 98; the s30_on one is new — TODO-48's flip became a
crossing). `unknown` is `most_likely` after every release (0.38–0.71). The task's criterion 2
("deliver_item(Y) at phase 0 must expect move_to(shelf_Y)") therefore does not hold under the
design as specified: the expected action is fixed by the domain's methods and guard selection, and
that is a decision about the DOMAIN (is `deliver_with_return` a human method at all?) or about
what a single-task hypothesis means while a different task is visibly under way, not about the
recognizer. Measured what the task's reading would give (variant `ownshelf`, rivals decomposed as
if nothing were held — analysis only): s00_on 97, s20_on 77, s40 item_6 ≥ θ at its grasp (272) —
and s30_on loses its crossing (item_7 reaches 0.795 at the RELEASE of item_3, 74, because shelf_7
is 39° off the carry direction: the collinear decoy, TODO-38). Decision open; both readings on
record. I4's path-cost kernel changes the magnitude of the carry refutation, not its sign.
Files: shared/recognizer.py (`_weigh`, `_output`), shared/planner.py (`decompose`)
Reference: I1 audit §9 (per-tick vs frozen selection); I2 IR foundations session

**TODO-52 — scenario_10's step-257 RuntimeError is latent, not fixed** ✅ RESOLVED by decision (R1, Sept 2026; with TODO-30) — the figures below are STALE (old layout)
R1 (September 2026): (a) the all-candidates outcome is DECIDED — plain projected cost, logged
`all_unrealizable` (TODO-30); the `RuntimeError` is removed in T10. (b) `env_layout1` was CLEANED
(no obstacles; coffee machine and AC switch side by side; item_1 near them; scenario_10's script and
pool rewritten) and the old layout is kept as `env_layout99`, NOT registered. scenario_10 is a SWEEP
FIXTURE AGAIN from T9 on (ten conditions: s00, s10, s20, s30, s40 × prior off/on). Every step number
below (257, 260, 142, …) refers to the OLD layout and is stale; what scenario_10 does on the new
layout is recorded in `analysis/t9_arrival_radius/REPORT.md`. Original entry retained below.
I1's O1 (`MetaPlanner._replan_tasks`: no feasible candidate, `min_dist=0.0`, at the
`theta_crossed` on the human's grasp of item_4 at 257) no longer fires after I2 — both prior
settings run 300 steps to completion — only because the belief at 257 is now `ac_activation`
at 0.69 (below θ; the AC hypothesis exists since the layout fix, TODO-49) so no crossing fires
there. The meta-planner condition that raised is untouched. Not a sweep scenario (dropped in I2);
keep it dropped until the meta-planner is unpaused, and expect the crash to return when the
belief changes again. UPDATE (I3): it did — run for the `waited` check only, s10_off raises at step
260 (`theta_crossed` on item_4 at its grasp at 257, 0.822; the carry tick 260 triggers the replan
with every candidate excluded). `waited(human_0, coffee_machine_0)` at 158–160 was attributed
correctly before the crash.
UPDATE (wait-decision revision, Sept 2026): the raise is superseded in design — the
all-candidates condition changes meaning under realization and its outcome is open (TODO-30,
three readings). Until realization lands the code still raises; keep scenario_10 dropped.
Files: shared/meta_planner.py
Reference: I1 audit O1; I2 IR foundations session

**TODO-53 — A hypothesis whose expected action never completes is judged by one chord from t=0** ✅ RESOLVED (I4) — and inverted; see TODO-57
Resolved by the excess-path likelihood: the stuck-origin hypothesis is charged for its whole path
(`ac_activation` in s40: 2373 cm of excess at 118, 5664 at 331; `most_likely` for 0 ticks of 184–271,
was 88 at 0.45–0.69; 0.001 at item_6's grasp, was 0.48–0.53). The same mechanism now OVER-charges every
task the observed agent has not started yet: `coffee_break`'s origin is the priming tick, so it enters
its own walk with 2144 cm of excess that its efficient walk never reduces. The alternative named
below — an origin reset on the observed agent's task boundary — was measured as the analysis-only
variant `reset_origin` (coffee 0.90, θ at 125, both prior settings) and is now TODO-57.
Original text:
Under the phase model the origin moves only when the expected action changes. A hypothesis whose
first action is never completed by the observed agent (`ac_activation` in s40; every
`deliver_item` the human never starts, until a shared completion such as `at(human, shelf_X)` flips
its method) keeps its t=0 origin for the whole run, and under the cosine kernel — which reads
direction only — its entire history is ONE chord from the start position to wherever the agent is
now, replaced each tick. It is never charged for the detour, while hypotheses whose phases flip
have their chords folded permanently. Measured (s40, both settings): `ac_activation` is
`most_likely` at 0.45–0.69 from 184 (coffee pinned) to 271, on the chord start → shelf_6 being 39°
off the switch's bearing (L ≈ 3.5), and item_6 — whose origin was reset to the table at 115 and
which carries the ×0.1–0.3 carry fold — is 0.09–0.13 until its grasp. Also why `coffee_break` is
`most_likely` at 0.65–0.69 at 115–117, before the coffee walk begins. Not a kernel to tune here: I4's
excess-path-cost likelihood reads the path length since the origin and charges exactly this. If
I4 does not close it, the candidate is an origin reset on the observed agent's task boundary — a
decision about what one hypothesis's "stretch" is, to be measured on s40 first.
Files: shared/recognizer.py (`update`: origin handling)
Reference: I3 phase-model session; analysis/i3_phase_model/REPORT.md §4

**TODO-54 — `theta_crossed` fires on `unknown` when a pin shrinks the live set** — admission side ✅ CLOSED (T8); trigger side ✅ CLOSED (D2, September 2026)
✅ CLOSED, trigger side (D2): `unknown` taking the top fires `recognition_changed` as a RETRACTION of the recorded
hypothesis (admission then returns `none(unknown)`, the record is cleared); nothing enters on `unknown`, since
the entering side asks the gate on a task hypothesis only. design_decisions.md, D2 entry.
s20_off step 136: the robot delivers item_6, the recognizer pins `deliver_item(item_6)`, and
`unknown` inherits its mass (0.654 → 0.804 ≥ θ) while the human stands idle. `evaluate_triggers`
fires `theta_crossed`, the meta-planner builds a projection for `unknown` and replans. Belief-side
this is correct (the human has no task); the trigger should probably not fire on `unknown`, and
the earlier question (TODO-48) of a `most_likely`-change trigger should be decided together with
it. Meta-planner paused: recorded only.
UPDATE (T8): "builds a projection for `unknown`" was not literally true, then or now: `unknown` is not in
the recognizer's hypothesis table, so `get_hypothesis("unknown")` returns None and `project_human()`
returned None — logged as `none(unresolved)`, the reason io_contracts.md reserved for a hypothesis the
projector cannot ground. What did happen is the pure-cost re-selection on the trigger. The admission was
therefore right by accident of the resolver, not by decision. Fix: `update_human_projection()` now refuses
`unknown` itself, before the projector is called, as `none(unknown)` — checked after `below_theta` and
`no_human`, before the projector; `unknown` is resolved through the recognizer's `UNKNOWN` constant, not a
literal. `none(unresolved)` again means what it says. No decision changes anywhere in the sweep (only the
reason string). At HEAD the event no longer occurs at s20_off 136 (the pin is at 144 and the belief stays at
0.498); `theta_crossed` on `unknown` occurs at s00_off 166 (0.995; coincides with the robot's own last
delivery — with T7 the pool is empty there and the run ends), s40_off 226 (0.751) and s40_on 223 (0.791).
At the two s40 crossings the trigger produces a pure-cost re-selection with no interference check — one
candidate each, item_7, the task already executing, re-confirmed (cost 17 / 20). `unknown ≥ θ` without a
crossing is also reached on `no_current_task` / `task_committed` at s00_on 168, s20_on 132 / 176, s30_on
123 / 159, s40 245: every one a pure-cost selection over the remaining pool. Whether the trigger should fire
on `unknown` at all, and the one-shot question, are the interface question of TODO-68 (with TODO-48) —
untouched here.
Files: shared/meta_planner.py (`update_human_projection`; `evaluate_triggers` for the open trigger side)
Reference: I3 phase-model session; T7/T8 session, September 2026

**TODO-55 — What a single-task hypothesis means while another task is visibly under way** ✅ (b) CLOSED by decision (I4c); (d) reported; (e) OPEN
The phase model judges `deliver_item(Y)` under the method the observed agent's world selects —
`deliver_with_return` while X is carried — so Y is refuted by X's carry (TODO-51, measured ≈ ×0.1
per carry) and every next-task reveal waits for the grasp (s00_on 111, s20_on 89, s30_on 98).
DEFERRED, not open for I4 to settle in passing: the severity above is measured against the
LOW_LIKELIHOOD cliff (0.1 for a chord ≈ 180° off), which I4 replaces with a gradient. Every reading
below must be re-measured after the I4 sweep before any of them is chosen; the I3 numbers say the
effect exists, not how large it is under the likelihood that will be in place.
Five readings, none chosen:
(a) correct as is — the domain says a human who wanted Y while holding X would return X first, and
    the belief after a release honestly favours `unknown` (0.38–0.71);
(b) reset the prior over the remaining tasks on the observed agent's task completion (the C5 event
    now exists: `[IR-complete]`), so a finished task's carry does not bury the next one —
    TODO-18/20's "reset-to-uniform", now implementable;
(c) decompose the human's hypotheses against a world without its own `holding` facts
    (`deliver_with_return` as a robot contingency) — a domain-specific filter; the analysis-only
    variant `ownshelf` gives s00_on 97, s20_on 77, s40 item_6 ≥ θ at its grasp, and s30_on loses
    its crossing to a collinear decoy (item_7 0.795 at the release of item_3);
(d) rebase a hypothesis's evidence when its selected METHOD changes, not only when its expected
    action changes: evidence accumulated while Y's predicted plan was "return X first" is evidence
    about a different predicted plan than "fetch Y", and carrying it across the re-selection
    conflates the two. The method name is not on `GroundedAction` today (I2 §9(c)): it would have
    to be added to the planner's output, not inferred from the action count;
(e) the domain model may be at fault rather than the recognizer: `deliver_with_return` describes
    someone holding a STRAY item, not someone holding an item they are assigned to deliver. Its
    guard (`holding(?agent, ?other)` ∧ `not_equal(?other, ?item)`) does not separate those, so the
    IR is faithfully predicting a bad plan. A domain question (`domains/kitting/tasks.py`),
    separable from the likelihood, and the one reading under which the recognizer is right and the
    fixture is wrong.
Evidence that settles it: the I4 sweep's next-task reveal ticks under (a); if the approach after a
release is decisive before the grasp there, (a) stands; if not, (b), (d) and (e) are the principled
candidates and (c) is not.
Files: shared/recognizer.py, shared/planner.py (method on the grounded output, for (d)),
domains/kitting/tasks.py (for (e))
Reference: I3 phase-model session; analysis/i3_phase_model/REPORT.md §5, §8

RE-MEASURED after I4 (β = 0.01, u = 0.1; `analysis/i4_evidence_model/REPORT.md` §8), no reading chosen:
- (a) as is: the rival's charge per task is two permanent folds, the first approach at its final
  excess and the carry phase's `move_to(shelf_X)` at its final excess — s00_on item_2 ×1.1e-5 then
  ×≈3e-6, s30_on item_7 ×0.006 then ×≈8e-6, s40 item_6 ×3e-9 then ×1e-9 (was ≈ ×0.1 per carry). Next-task
  reveals: NEVER, in all eight conditions (I3: at the grasp). `unknown` holds 0.995 from the first
  release. The approach after a release is not decisive before the grasp — it is not decisive at all —
  so by the criterion written above (a) does not stand.
- (c) `ownshelf`: identical to (a) — never, in all eight (s20_off 32 vs 31). The rival's t=0 origin
  then accumulates the whole first task as one excess (2358 cm at the release for s40's item_6). The
  carry-method charge (TODO-51) is no longer the binding one; (c) is out.
- (b) prior reset on the observed agent's task completion, measured as `reset_boundary` (origins and
  evidence state reset to uniform at every retirement): next-task reveals PRE-GRASP prior-on — s00_on 80
  (grasp 111), s20_on 56 (89), s30_on 76 (98) — and 117/96/96 prior-off (post-grasp in s00/s20), with
  three wrong crossings prior-off (s20_off item_7 136, s30_off item_6 156, s40_off ac 376), all on a
  reset fired by the ROBOT's completion while the human idles, and TODO-52's crash in s20_off at 142.
  Works when the boundary is the human's; needs a boundary the recognizer can attribute to the
  observed agent (TODO-57).
- (d), (e): not measured (changes outside the recognizer).
Remaining candidates: (b), (d), (e). The evidence that separates them: whether the first approach
after a release should carry the previous task's refutation at all ((b) says no; (d) says only until
the method re-selects; (e) says the method is wrong). Decide together with TODO-57.

RE-MEASURED after I4b's boundary (`analysis/i4b_boundary/REPORT.md` (deleted in the analysis cleanup, September 2026; carried in design_decisions.md, the I4b / I4c entry, and TODO-55 to TODO-59) §7), still no reading chosen:
(a) unchanged — never, in all eight (the rival's carry folds are in its base; the boundary keeps them).
(c) `ownshelf` + boundary is no longer identical to (a): with no method flip there is no fold, the
rival's approach excess from t = 0 is dropped at the human's release, and next-task reveals appear
PRE-GRASP prior-on — s00_on 80 (grasp 111), s20_on 56 (89), s30_on 76 (98) — post-grasp prior-off
(s00_off 116, s20_off 95; s30_off 87 pre-grasp) with wrong crossings on the idle human prior-off
(TODO-59) and TODO-52's crash (s20_off 142). In s40 it gives the fixture's shape (item_6 0.47 → 0.79
through 3a, 0.80 → 0.083 through 3b). The boundary made the inequality explicit: whether a rival's
previous-task charge survives the boundary depends on whether its guard selected `deliver_with_return`
under the carry — (d)'s point — so (a) as shipped treats hypotheses unequally at the boundary.

RESOLVED in I4c (`analysis/i4c_episode/REPORT.md`), reading by reading:
- (b) IS the episode semantics: the recognizer estimates the intention of the observed agent's current
  behavioural episode; at the observed agent's own task boundary the belief re-initialises to the
  admissible prior over the hypotheses still live, uniformly, and every origin moves. Adopted by decision,
  not by measurement; the measurement confirms it: next-task reveals in every condition (pre-grasp
  prior-on s00 81 / s20 57 / s30 77; prior-off 117 / 96 / 87), no wrong crossing, no crash (the crash and
  the prior-off wrong crossings of the I4 `reset_boundary` what-if were the lone-survivor effect, TODO-59,
  which I4c's other change removes — variant `episode_only` reproduces them: s20_off item_7 136–141 then
  the TODO-52 abort at 142; s00_off item_4 142–165; s30_off item_6 161–167; s40_off ac 376–382).
- (d) rebasing on a method change: within an episode a rival's method still flips under the carry and its
  fold history differs from a never-advanced hypothesis's (s40 episode 1: item_6 flips at 60, 62 and 115
  and holds its two folds in its base — 0.0 — while coffee and ac hold 2144 / 2349 cm in their open
  stretches — base 0.909, value 0.000); the posterior consequence within the episode is nil (all three at
  the floor at 114) and across the boundary it is nil by construction (all 0.25 at 115). No within-episode
  flip in the four scenarios is caused by anything but the observed agent's own grasp and release, so in
  kitting the unevenness never outlives the episode. That is a fact about kitting's guards, not a general
  argument; the general question — whether evidence accumulated under one method is evidence about another
  method's plan — stays as stated, dormant, with no case in the current domain.
- (c) out (I4); (a) superseded by (b).
- (e) OPEN: whether `deliver_with_return`'s guard should distinguish a stray item from one the agent is
  assigned to deliver. A domain-model question (`domains/kitting/tasks.py`), independent of the likelihood
  and of the episode semantics. I5: implicated in the prior-off repeated `theta_crossed` (TODO-68) — the
  rivals' `place`-back-on-the-shelf phase and the regress that follows are this method's phases, scored as
  observations the human never made.

**TODO-56 — The completion channel's gate is the old model's, and it is a decision** ✅ RESOLVED (I4b) — the gate stays, with its exclusion stated
Decided in I4b (`analysis/i4b_boundary/REPORT.md` (deleted in the analysis cleanup, September 2026; carried in design_decisions.md, the I4b / I4c entry, and TODO-55 to TODO-59) §6): under the detection model a hit is ×1.0, so the
ungated channel adds exactly one thing — the permanent ×10⁻³ false-alarm charge on every hypothesis
whose expected action is elsewhere at a discrete tick (108 of 124 ungated events, all on `move_to`; the
"rival expecting move_to(shelf_X) at a grasp at shelf_X" case is a hit, ×1.0, no information). That
charge is generatively right for a FIXED intention and, being an event, cannot be reset by the task
boundary: with it, coffee_break is 0.001 for ever in s40 (variant `ungated` + boundary). The movement
channel already carries the same fact in the one form the boundary can reset. Cost of withholding:
s20_off's reveal at 31 instead of the grasp tick 22 (two decoys beyond the target on the same bearing).
If a grasp-tick reveal of the CURRENT task is wanted, the mechanism is an event scoped to the current
task (resettable at the boundary), a change to the event channel's bookkeeping — I5, not a flag.
Original text:
I3 judges an event only against expected actions whose vocabulary declares it (GRASP → `pick_up`),
leaving movement actions NEUTRAL at a grasp as before. The other reading — every expected action
LOW at a discrete tick unless its completion holds — is generative-model-correct (a walker does not
emit GRASP) and was measured (variant `ungated`): `unknown`, which pays nothing, takes ×10 against
every live task at every grasp and release and ends at 0.96–0.99 after every completion; no second θ
crossing in any condition. The asymmetry is `unknown`'s flat likelihood, not the gate. If I4 gives
`unknown` a likelihood of its own, revisit the gate with it.
Files: shared/recognizer.py (`_in_vocabulary`)
Reference: I3 phase-model session; analysis/i3_phase_model/summary.md (deleted in the analysis cleanup, September 2026; the folder's REPORT.md stays)

RE-CHECKED under I4's constants (variant `ungated`, `analysis/i4_evidence_model/REPORT.md` §7): the
`unknown` sweep does not occur — `unknown`'s likelihood is a per-tick constant never multiplied into
its base, while the false-alarm rate (1e-3) multiplies into the rivals'. Crossings identical to the
gated code in seven of eight conditions; s20_off's reveal moves from 31 to 22, the grasp tick (the two
on-path decoys the approach cannot separate are charged at the grasp). The measurement no longer
rejects the ungated reading; it favours it slightly (one earlier reveal, no cost). Note also that under
the gate a grasp is no longer evidence at all (hit rate 1.0 against unjudged rivals at 1.0): if a
grasp-tick reveal is wanted, the ungated reading is the mechanism, not a constant. Decision open on
the generative argument (a walker does not emit GRASP); the gate stays until it is taken.

**TODO-57 — What a task boundary is to the recognizer (origin and evidence across the observed agent's completions)** ✅ RESOLVED (I4b origin, I4c evidence: the episode re-initialises to the prior — TODO-55 (b))
Shipped in I4b: a retirement whose hypothesis expected its terminal action on the previous tick (the
observed agent's own derived phase reached the completing action) moves every live origin to the
agent's position; bases, folds and events untouched. Fires at 18/18 human task boundaries, at none of
the robot's completions; coffee_break 0.904 in both prior settings; s00/s20/s30 byte-identical to I4.
Candidates A'/B/C/D rejected with numbers (`analysis/i4b_boundary/REPORT.md` (deleted in the analysis cleanup, September 2026; carried in design_decisions.md, the I4b / I4c entry, and TODO-55 to TODO-59) §2). Open questions (1)
and (2) below are answered (a retirement the phase state accounts for; origins only). Question (3)
stands: no boundary sees segment 3's waypoint pauses (1 tick, retire nothing) — SINCE F47b the two
segment-3 legs are well-typed `ac_activation` tasks at `ac_switch_1` / `ac_switch_2`, whose completions
pin and re-initialise like any other (scenario_40's baseline regenerated, `analysis/f47_fixtures/`), so
scenario_40 no longer has an unmodelled boundary; a declared unmodelled behaviour is TODO-80 — and a domain whose tasks
end in a ProcessCompletion has none. What the boundary does NOT fix — a rival's permanent folds from the
previous task (item_6 stays at the floor; §3 of the report) — is TODO-55's, and what it exposes — a
lone survivor at 0.909 on zero evidence — is TODO-59.
Original text:
The excess-path likelihood is correct within a task and blind to the observed agent finishing one task
and starting another: a hypothesis the agent has not started keeps its priming-tick origin (coffee in
s40 enters its own walk 2144 cm in the red), and every phase a rival lost is folded permanently
(item_6 carries ×3e-9 × 1e-9 into segment 2). Both are right for a fixed intention and wrong for a
sequence of them; no β, u pair reconciles the first-task and later-task requirements (they are a
factor ≥ 5 apart in β — `analysis/i4_evidence_model/REPORT.md` §4.2). Two analysis-only what-ifs
isolate the halves: `reset_origin` (every live origin moves to the agent at a retirement) gives
`coffee_break` 0.90 in both prior settings by the intended chain and leaves item_6 buried;
`reset_boundary` (origins + evidence state to uniform) also gives item_6 0.47 → 0.79 while the human
heads at shelf_6, 0.80 → 0.08 after the turn, 0.82 at its own grasp prior-off, and pre-grasp next-task
reveals prior-on. Neither is shipped. Open questions: (1) which event is the boundary — a retirement
fires on the robot's completions too (prior-off: s40 145/243/376, s20 52/136, s30 86/156, s00
31/93/166) and s40's waypoint stops retire nothing; the recognizer-side signal is a terminal completion
that held on a tick where the observed agent's own microaction was in the terminal action's
vocabulary (RELEASE → `place`; `waited(human, ·)` names the agent); (2) reset origins only, or the
evidence state too (TODO-55 (b)); (3) what happens at an unmodelled boundary (segment 3 → 4: item_6's
539 cm of segment-3 excess is never reset, so it stays at 0.08 through its own approach prior-on).
Constraints inherited from I2–I4: no global leg closed by the body's `stand`, no decay, no factor;
a boundary is an event, and an event is allowed to multiply and to move origins.
Files: shared/recognizer.py (`update`: retirement branch, `_origin`, `_origin_odo`, `_base`)
Reference: I4 evidence-model session; analysis/i4_evidence_model/REPORT.md §4.2, §6, §10

**TODO-59 — A zero-length stretch is scored as a perfect fit: a lone surviving hypothesis is at 1/(1+u) before the agent moves** ✅ RESOLVED (I4c)
An empty stretch — nothing walked since the origin — is not an observation: the movement channel
contributes no factor for it (not 1.0, not a neutral constant), and `unknown`'s constant applies only on
a tick on which some hypothesis was scored on an observation. Applies to a stationary tick after any
origin reset, phase advance or episode boundary, and to t = 0. Measured: the 63 wrong-task ticks are gone
(the 47 idle-tail ticks by this change alone — variant `episode_only` keeps ac at 0.904 for 331–378 —
and the 16 segment-3a ticks by the episode re-initialisation, which gives ac a live competitor); the
prior-off lone-survivor crossings of every reset what-if are gone with them. On a tick with no
observation the belief is the prior (after a boundary) or the base ratio (after an advance) — see
TODO-60 for what that exposes. Explicitly deferred, NOT part of dC and not built: stationarity as
evidence AGAINST hypotheses that predict movement (a human standing still may be informative; that is a
different observation channel with its own model).
Original text:
L(0) = 1 and `unknown` pays UNKNOWN_LIKELIHOOD = 0.1 on every tick, including a tick on which nothing
has been walked since the origin. At t = 0 in a one-task space, and after every task boundary (I4b)
for every surviving stuck hypothesis, the belief is therefore 1/(1+u) = 0.909 for that hypothesis with
no evidence: s40, `ac_activation` ≥ θ at 185–200 (segment 3a, human standing then walking 55° off the
switch) and 333–378 (idle after the last delivery), 63 wrong-task ticks, 0 in I4; also the prior-off
wrong reveals on the robot's undelivered items under `ownshelf`. The boundary exposes it (it
manufactures zero-length stretches mid-run); the cause is I4's per-tick constant for `unknown`.
Candidates, all semantic: `unknown`'s likelihood as a function of the evidence on the stretch (u per
unit walked, so that an unwalked stretch is uninformative for everyone), or re-priming hypotheses with
no folds from the prior at a boundary (TODO-55 (b), restricted). Not a retune of u (any u < 1/3
reproduces it). Out of I4b's scope (the likelihood form).
Files: shared/likelihood_functions.py (`UNKNOWN_LIKELIHOOD`, `logistic_of_excess`), shared/recognizer.py (`update`)
Reference: I4b task-boundary session; analysis/i4b_boundary/REPORT.md (deleted in the analysis cleanup, September 2026; carried in design_decisions.md, the I4b / I4c entry, and TODO-55 to TODO-59) §5, §8
See TODO-95 (23 Sept 2026): the deferred stationarity channel is taken up there as a design task.

**TODO-60 — `unknown`'s u is charged per OPEN observation and never folded: the belief with no observation is the base ratio** ✅ RESOLVED (I4d)
The accounting: for every live hypothesis k and tick t within an episode,
    E_t(k)/E_t(unknown) = [π(k)/π(unknown)] · Π_{closed stretches s of k} L_k(s)/u · Π_{events} c_k(e) · (v_k(t)/u | 1 if empty).
`unknown` is the reference; a task's odds against it are the product over the task's own observations of
L/u, and a fold moves a factor from the open term to the base without changing it. Implemented as: the fold
multiplies L/u into the base, the open observation multiplies v/u, `unknown` takes no factor. Checked by an
independent accumulator on every tick of the eight conditions (max |Δ log odds| 7e-15, 5,069 checks). The
re-triggers are gone (s00_on 0.905 → 0.986 → 0.995 through the grasp; no `theta_crossed` at 113/91/100).
Accepted with it: the ceiling is 1/(1+uⁿ) over n observations; an extra closed stretch is worth 1/u between
tasks of equal fit; regresses and no-graded-signal phases fold 1/u. New, reported not fixed: prior-off the
rivals' `deliver_with_return` phases at the grasp (a `place` worth 1/u, then a fresh stretch — TODO-61)
dip the true task under θ twice, three crossings per recognition (s00_off 109/113/115, s20_off 20/24/30 and
87/91/95). `analysis/i4d_fold_unknown/REPORT.md`.
Original text:
The hypotheses fold each closed stretch's value into their bases; `unknown`'s constant is applied only to
the open observation and never folded (I4's design — it is what makes 1/(1+u) a CEILING rather than a
value that climbs with prefix length). So the base ratio of a task with only perfect folds to `unknown`
is 1:1, and on a tick with no observation (I4c: an empty stretch) the reported belief is that ratio, not
the previous tick's posterior: a lone live hypothesis dips from 0.905 to 0.498 on its grasp tick and the
one after (s00_on 111–112, s20_on 89–90, s30_on 98–99 — the only live rival being pinned), recovers at the
first step, and the recovery fires a second `theta_crossed` (s00_on 113, s20_on 91, s30_on 100; the
meta-planner re-decides, harmlessly here). The spec's "the belief carries forward unchanged" holds for
the base and not for the posterior, because I4's model gives them different meanings for `unknown`. The
candidates are the likelihood form's: fold u per closed observation (the ceiling then rises with prefix
length — a task at its third perfect stretch is at 1/(1+u³)), or keep the ceiling and accept the dip.
Not a retune of u. Out of I4c's scope (the likelihood form).
Files: shared/recognizer.py (`update`: the fold and `unknown`'s factor), shared/likelihood_functions.py (`UNKNOWN_LIKELIHOOD`)
Reference: I4c episode-semantics session; analysis/i4c_episode/REPORT.md §5

**TODO-61 — The evidence model is one-sided and observation-counted: (a) confirmation is length-blind, (b) accumulation is observation-count and decomposition sensitive** [(a) CLOSED for walks by graded evidence, September 2026; (b) OPEN for the no-graded-signal phases]
UPDATE (graded-evidence session, September 2026; design_decisions.md, "A stretch's evidence against
`unknown` is graded by the share of the expected path it covers"): a stretch's odds against `unknown` are
now L / u^f, f the fraction of the hypothesis's expected path it has covered (1 at an arrival, by the
completion fact). (a) is closed for walks: a fitting stretch is worth 1 on its first step and 1/u at its
arrival, and a lone task clears θ at about half its path, not on one step. (b) is closed for walks in one
respect — the value of a path no longer depends on how the phase machinery segments it (two half-path
stretches multiply to the whole) — and OPEN for the no-graded-signal phases: `pick_up`, `place`, `wait_at`
and an undecomposable hypothesis are still one whole observation (1/u) each, so an arrival still counts
twice and the decomposition still sets how many such observations a hypothesis can gather. `unknown` now
pays u per whole expected path covered (its meaning, not its value, changed). The s40 illustrations below
(wander_0, 187, 203–213) are PRE-F47b — the leg is now `ac_activation(ac_switch_1)`, tied with item_6 until
its arrival fold at 205 (handback §9) — and pre-grade; the s00_off 114 / s20_off 25 regress dips are gone
under the grade (the rival's fresh stretch walked away from its target pays L alone). Kept as the record of
their time.
Broadened in I5 from (a) alone. DECISION and why: the two are kept under one item because they have one root
— costdif1 with a constant `unknown`: a fitting stretch scores L = 1 whatever its length, and every scored
observation is worth L/u against a constant reference — and because any remedy for one changes the other's
currency (grading confirmation by the fraction of the direct cost covered changes what a fitting observation
is worth, which is exactly what (b) counts; charging u per unit of evidence rather than per observation changes
both at once). The two I4d illustrations involve both at once (below). They are two SHARP statements, lettered,
each with its own mechanism and candidate remedy, so that either can be closed alone; a single blurred
"the evidence is weak at confirmation" would lose the decomposition sensitivity, which is the less obvious half.
(a) CONFIRMATION IS LENGTH-BLIND. dC discriminates by penalising wrong hypotheses, not by rewarding right
    ones: the correct hypothesis sits at zero excess however far it walks, L(0) = 1 after 15 cm as after
    300 cm. Evidence is one-sided — strong at refutation, weak at confirmation. Illustration: s40_on 187, one
    15 cm step toward wander_0 (on the bearing to shelf_6) takes item_6 from 0.333 to 0.485; the 20-tick walk
    to 0.79 (11 wrong-task ticks, 203–213, the only ones in the matrix), undone by the turn. Candidate remedy,
    not chosen: a confirmation term graded by covered fraction of C(origin, g) (neither Ramírez–Geffner nor
    Masters–Sardina has one; segment 3a is the ambiguous case they accept).
(b) ACCUMULATION IS OBSERVATION-COUNT AND DECOMPOSITION SENSITIVE. Each scored observation contributes its
    likelihood relative to the constant `unknown`, so a fitting observation is worth 1/u regardless of what it
    observed: a 300 cm walk straight at the target, a no-graded-signal phase (pick_up, place, wait_at), and a
    regress-generated zero-excess stretch are each 1/u. A hypothesis's DECOMPOSITION — how many phases its
    selected method has and where its steps sit — therefore sets how much evidence it can accumulate
    (`deliver_with_return` has six actions to `deliver_default`'s four). Illustrations: item_6 recognised at
    274 in s40 despite a 539 cm detour worth ×0.09, because two fitting observations at ×10 each (a
    stationary pick_up phase, one 15 cm carry step) outweigh it; s20_off's first reveal moving 31 → 20
    because the arrival's fold (×10) separates item_3 from its two collinear decoys before the grasp; and
    prior-off the rivals' `deliver_with_return` phases at the grasp (a `place` worth 1/u, then a fresh
    stretch — (a)) dipping the true task under θ twice (TODO-68). Candidate remedies, not chosen: u per unit
    of evidence (TODO-59's rejected alternative), or normalising accumulated odds by decomposition length —
    both change the meaning of `unknown` and would have to be decided with TODO-63.
Both were visible in I4d's accounting before they were measured; neither is a reason to touch β, u or the
likelihood form without a decision that names which of (a), (b) it addresses.
I4d note (as written then):
I4d note: with `unknown` folded (TODO-60) this property now also shows prior-off at every rival's regress
after the grasp — a fresh `move_to(shelf)` stretch at L ≈ 1 from its first step lifts the rival and dips the
true task under θ (s00_off 114, s20_off 25) — and in item_6's recognition at 274 after a 539 cm detour: the
detour is ×0.09, the first step of the carry ×10. A property of the chosen model, not an implementation
defect; left as it is by decision.
The excess-path likelihood charges wasted path and credits nothing for path covered: a hypothesis whose
target lies on the agent's bearing is at the perfect fit from the first step, however far the target is.
From the uniform base a boundary leaves, one 15 cm step toward wander_0 (on the bearing to shelf_6) takes
item_6 from 0.333 to 0.485 (s40_on, 187), and the 20-tick walk to 0.79 — 11 wrong-task ticks at 203–213,
the only ones left in the matrix, produced by real evidence (zero excess over ≈ 300 cm walked) and
undone by the turn (0.790 → 0.083 through 3b). Prior-off the same walk peaks at 0.462: the robot's live
items dilute it, not the evidence. Whether confirmation should be graded by the fraction of the direct
cost covered (Ramírez–Geffner's and Masters–Sardina's models do not; the fixture's segment 3a is exactly
the ambiguous case they accept) is a likelihood-form question. Recorded; not a reason to touch β or u.
Files: shared/likelihood_functions.py (`excess_path_likelihood`)
Reference: I4c episode-semantics session; analysis/i4c_episode/REPORT.md §4

**TODO-62 — Radius of maximum probability (Masters & Sardina, JAIR 64, 2019): a diagnostic ON the model, not built** [DEFERRED for scope]
Computes, from geometry alone, the cost-distance at which a goal becomes the most probable — so a reveal
location can be PREDICTED from the layout and the parameters and then checked against a run, instead of
being discovered by sweeping. A diagnostic on the evidence model, never called by the recognizer. Considered
during the I4 design and deliberately not built: scope, not prematurity. Under the current model the
prediction would need the closed form the I4c region analysis used (uniform base, no fold in the window),
extended by the fold's 1/u at each phase advance (TODO-61 (b)).
Trigger to build it: whenever choosing β or u starts to feel like tuning rather than measurement.
Files: none (analysis-side; would live under analysis/)
Reference: I4 evidence-model design discussion; I5 hand-back

**TODO-63 — Rationality measure (Masters & Sardina, AAMAS-19): competes with the constant `unknown`, not built** [DEFERRED by decision]
Estimates the observed agent's degree of suboptimality and lowers the recognizer's own confidence when the
behaviour fits no hypothesis well. It COMPETES with the constant `unknown` hypothesis for the same job —
holding the line on behaviour that fits nothing — and running both would make neither evaluable, which is
why it was not built. Considered during the I4 design.
Trigger to revisit: if the constant `unknown` is shown unable to hold the line on behaviour that fits
nothing (a wrong task above θ on a walk that fits no task, sustained). Decide together with TODO-61 (b)'s
remedies, which also change what `unknown` means.
Files: shared/likelihood_functions.py (`UNKNOWN_LIKELIHOOD`), shared/recognizer.py
Reference: I4 evidence-model design discussion; I5 hand-back

**TODO-64 — θ's reachability under the current model: the ceiling is 1/(1 + uⁿ), and reachability is a function of the live set** ✅ CLOSED (gate ruling, September 2026)
✅ CLOSED (cchat, on `analysis/g1_graded_evidence/crossings.md`): θ stays a fixed 0.75 on the normalised share,
not derived from the live set or the layout. The live-set dependence was in the likelihood, not the gate:
before the grade a stretch was worth L/u whatever its length, so the bar the share set depended on how many
rivals had to be outvoted by observation count. Under graded evidence a walk refutes its rivals as it goes and
the crossing odds against `unknown` are independent of the live-set size (25 of 30 walk crossings at 3.1–4.2
with 1 to 9 live keys; the other five at 5.2–9.4, each with one rival still live). A lone task clears at
f ≈ 0.48 of its expected path, a fraction, not a distance, so the layout's scale does not enter either.
Reopened only by a walk crossing with a live rival at similar odds (TODO-47 (g)). design_decisions.md,
"The gate stays a fixed share". The history below is kept as it was.
NOTE (F47, September 2026; also for TODO-65): with a ONE-task admissible pool (prior on, the human assigned a
single delivery and no foreseeable task on the layout) the uniform prior over {task, unknown} already puts
0.906 on the task at tick 0, before the human has moved, and a projection is built at t=0 (retired
scenario_60/61: `[IR] step=0 ... confidence=0.906`, `[meta-proj] projection=built`, T_h 109.5, a 2-tick hold).
Prior-on runs on such fixtures therefore do not test recognition; the gate is cleared by the live set's size.
F1 measured a perfect hypothesis reaching only 0.569 once two foreseeable hypotheses and `unknown` were in
the space (that figure came from the held-item pin, removed in I3); the 0.797 quoted for months exists only
in layouts with no foreseeable task. Restated under I4d: a lone fitting task's ceiling is 1/(1 + uⁿ) over
its n observations — 0.909 on its first stretch, 0.990 after one fold, 0.999 after two — and with rivals
live at the prior the confidence is 1/(1 + uⁿ + Σ_rivals odds_j). So θ = 0.75 is reachable on the FIRST
stretch only if the rivals' summed odds fall below 1/3 − u ≈ 0.233 (u = 0.1), and after one fold below
10 × that. The question now: is θ meant to be reachable on a first stretch (then the live-set size and the
layout's decoy geometry decide it — s20_off needs the arrival's fold), or only after a verifiable phase
(then θ is a prefix-length bar, not a fit bar)? Undecided; measure nothing until it is decided together
with TODO-65.
RESTATED AS AN OPEN DIRECTION (θ single-source session, September 2026): θ DERIVED RATHER THAN FIXED — a
function of the SIZE OF THE LIVE HYPOTHESIS SET, of LAYOUT GEOMETRY, or of both, instead of one constant.
A fixed 0.75 is a different evidential bar over a three-hypothesis live set than over an eight-hypothesis
one, because the reachable ceiling is 1/(1 + uⁿ) over n observations. OPEN, nothing chosen, nothing
measured. Where it would land in code: `MetaPlanner._clears_gate(belief)`, now the only place θ is applied
— `belief.distribution` already carries the live set, and a geometry-derived θ would add a `world`
argument there, which both call sites already hold. The consolidation that made this a one-method change
is recorded in design_decisions.md, "θ has one home".
NOT an argument for lowering θ: that it fires earlier. M1 (`analysis/m1_theta_earlier/` (deleted in the analysis cleanup, September 2026; its numbers are the ones given here)) measured θ = 0.65
on scenario_30 — the first crossing moved 21 → 15 prior-on and 28 → 24 prior-off with no decision change
and byte-identical behaviour, and offline realization at the moved triggers was better in one prior and
worse in the other. An earlier trigger is not better by itself.
Files: shared/recognizer.py (`_output`), shared/meta_planner.py (`_clears_gate`, `DEFAULT_THETA`)
Reference: F1 fixture session; I4b/I4c/I4d reports; I5 hand-back; θ single-source session, September 2026

**TODO-65 — Whether the gate should be a likelihood ratio rather than a normalised posterior** ✅ CLOSED (gate ruling, September 2026)
✅ CLOSED (cchat): the gate stays `confidence ≥ θ` on the normalised posterior. Under graded evidence the
share is odds_top / (1 + odds_top + Σ_rivals odds_j), so θ = 0.75 reads "at least about 3:1 over no model,
and more while rivals remain"; a later crossing under ambiguity is intended. Not taken: odds against
`unknown` (drops the rivals' term); the ratio of the top two (infinite for a lone task, adds nothing where
no rival stays competitive); a rate-of-growth gate (a threshold on the derivative of a noisy quantity).
The three margin references below are therefore not built. Reopened only by a walk crossing with a live
rival at similar odds, where share and margin disagree; none in the current fixtures (lowest top-two ratio
at a walk crossing 5.23, s00_off 37); TODO-47 (g). design_decisions.md, "The gate stays a fixed share".
Confidence is a normalised posterior over the live set, so θ = 0.75 is a different evidential bar in a
3-hypothesis run than in an 8-hypothesis one (prior-on vs prior-off: the same coffee walk crosses at 135
with three live rivals and 143 with seven). The recognizer's evidence state already IS a set of odds against
`unknown` (I4d's invariant); a gate on odds_k against `unknown`, or on the ratio of the top two, would be
live-set-invariant. An interface/design question for the meta-planner side (what `confidence` means at the
gate), not a likelihood question. Decide with TODO-64 and TODO-68.
RESTATED AS AN OPEN DIRECTION (θ single-source session, September 2026): a MARGIN gate replacing the
absolute test — fire when the leading hypothesis is sufficiently AHEAD, rather than sufficiently HIGH. 0.5
against a field of 0.1s is a stronger signal than 0.6 against a field of 0.2s, and an absolute threshold
cannot see the difference. Three candidate references, NONE CHOSEN: the margin against the RUNNER-UP (the
ratio of the top two); against `unknown` (the odds the evidence state already is, I4d); or against the
REST OF THE FIELD (the leader's mass over the summed rest). Each is live-set-invariant in a different way
and they disagree whenever the field is skewed rather than flat; picking one is the decision, and it has
not been made. OPEN, nothing measured. Where it would land in code: `MetaPlanner._clears_gate(belief)`,
now the only place the gate is asked — it already receives the whole `BeliefState`, so every one of the
three references is computable from `belief.distribution` without a signature change, and
`evaluate_triggers()` keeps asking for a CROSSING of whatever the predicate becomes (DESIGN-07's event
semantics is unaffected). See design_decisions.md, "θ has one home".
NOT an argument for any of the three: that a gate fires earlier — see the M1 note under TODO-64.
Files: shared/recognizer.py (`_output`, `BeliefState.confidence`), shared/meta_planner.py (`_clears_gate`)
Reference: I1 audit; I5 hand-back; θ single-source session, September 2026

**TODO-66 — The context / knowledge-representation pass: `_context_weight` branches on literal task names** [DEFERRED deliberately]
`_context_weight` still tests `hyp.task_name == "ac_activation"` and `"coffee_break"` and carries its own
constants (TEMPERATURE_BOOST 3.0, FATIGUE_BOOST 2.5, HIGH_TEMP_THRESHOLD 26.0, LONG_SHIFT_THRESHOLD 500) —
the one place in shared/ that names a domain task. Applied to the output only, never fed back, so it does
not touch the evidence state or the accounting. Deferred because fixing it properly reopens the ontology
and knowledge-representation questions (what a context fact is, which schema field declares a task's
sensitivity to it, where the constants live — a `ContextSchema`, not a branch). Not a bug in any measured
condition (no scenario sets the temperature or a long shift).
Files: shared/recognizer.py (`_context_weight`, the four constants), shared/domain_knowledge.py
Reference: I1 audit (architecture invariant "no domain-specific strings in shared/"); I5 hand-back

**TODO-67 — s30_off: the meta-planner selects the already-delivered item_2 at 87** ✅ FIXED (T7)
`[meta] step=87 trigger=theta_crossed winner=deliver_item(item_2)` one tick after the robot's own delivery
of item_2 (the recognizer's `[IR-complete]` at 86); `no_current_task` re-selects item_4 at 93 (I4c) / the
same in I4d. Either the robot's task pool drops a completed task a tick late or B3's candidate set does not
read the world's completion. Meta-planner paused: recorded, not investigated.
UPDATE (T7): both, and the second is the cause. The executor learns of its own task's completion up to two
ticks after the world does: RELEASE at 85; `obj_at(item_2, kitting_table_0)` is in the WorldState built at
86; the executor advances past `place` at 86 and calls `_on_task_complete` (→ `advance_task`, current task
cleared) at 87 — after the meta-planner has run that tick, since the cognitive loop precedes execution
within a step. In that window `update()` assembled its pool from the robot's bookkeeping alone
(`[current_task] + queue`) and never consulted the world, so the trigger at 87 offered the finished task as
a candidate; the planner, decomposing from the live world, turned `deliver_item(item_2)` with the item
already on the table into a four-action plan of cost 3 (zero-length walk, re-grasp from the table, re-place)
which beat item_4 at 69. The robot re-grasped its delivered item (`task_committed` at 89 re-selected it
again, cost 2) and re-placed it; item_4 began at 93. The same shape at s00_off 166 (the robot's last item,
re-grasped at 168, run end 172 instead of 166). Fix: completion is a WORLD fact, read generically — a new
`AdaptivePlanner.is_complete(task_name, task_params, agent_id, world)` (the terminal action's completion
condition of the guard-selected decomposition holds; the recognizer's `_terminal_complete` criterion,
indifferent to who did it) — and `update()` drops every complete task from the pool on every call, logged as
`[meta-pool] <task> complete in world: dropped from the pool`. Nothing is recorded: the queue invariant is
unchanged, B3's queue rewrite persists the drop, and an empty pool after the drop is the terminal return.
Sweep effect (PYTHONHASHSEED=0, analysis/t7_t8_meta_bugs/summary.md, deleted in the analysis cleanup; these
numbers are its record): s30_off — item_4 selected at 87
(was 93), its `task_committed` at 121 (was 127), delivered at 155 (was 161), run end 157 (was 163); s00_off —
`all tasks complete` at 166 (was 172). No other condition's decisions move. The recognizer's private
`_terminal_complete` implements the same test; making it delegate to the planner's method is recognizer-side
work, not done here.
Files: shared/meta_planner.py (`update`, `_is_complete`), shared/planner.py (`is_complete`)
Reference: I4c report ("Flagged, not fixed"); I5 hand-back; T7/T8 session, September 2026; design_decisions.md
"Task completion is a world fact"

**TODO-68 — `theta_crossed` as an interface event: repeated crossings per recognition prior-off** [INTERFACE / DESIGN question — not an evidence-model question] ✅ CLOSED (D2, September 2026)
✅ CLOSED (D2): the consumer changed, not the event's definition and not the evidence model. `recognition_changed`
tracks the identity of the projected hypothesis (the decision record), so a re-crossing of the same hypothesis
fires nothing and a dip below θ while it stays most likely fires nothing; no latch, no debounce, no odds gate.
Fires per run: `analysis/d2_recognition_trigger/README.md`. design_decisions.md, D2 entry.
D2 SCOPE (wrap-up after F47b, September 2026; designed in the design claude chat - we call it cchat): what a trigger is an event OF
— this item with TODO-48, TODO-54 and the human's task boundary — separating the events that change the
evidence from those the current machinery can respond to. Admission is restricted to evidence-changing
events; the remaining churn risk, an argmin flip on a re-decision, belongs to B2 (`b2a`'s commitment,
TODO-36). The blocked-execution event and the wait-versus-reconsider policy are recorded as design, their
evaluation deferred until a fixture legitimately produces a mid-run block (TODO-80, TODO-47).
Measured (I4d, confirmed at HEAD in I5): prior-off the true task crosses θ three times per recognition —
s00_off 109 / 113 / 115, s20_off 20 / 24 / 30 and 87 / 91 / 95. Three things, kept separate:
(a) RECOGNIZER BELIEF: the trajectory is exactly what the stated model implies (the I4d invariant holds to
    7e-15 on every one of these ticks). The true task rises above θ at its arrival (the `move_to` fold,
    ×10); at the grasp each rival's method flips to `deliver_with_return`, whose `place` phase back on the
    shelf is a no-graded-signal observation worth 1/u (TODO-61 (b)) and lifts the rival, dipping the true
    task below θ; on departure the rival regresses to a fresh zero-excess stretch at L ≈ 1 (TODO-61 (a))
    and dips it again; the walk away then refutes the rival. The same bumps existed in I4c below θ; I4d's
    ceiling made them cross. The recognizer is correctly implementing its model.
(b) THE EVENT'S SEMANTICS. `io_contracts.md` defines `theta_crossed` as "confidence crosses θ from below to
    at-or-above (prev < θ ≤ current) — a crossing event, not confidence ≥ θ per tick". It does NOT promise
    one crossing per task; it promises a crossing whenever the confidence trajectory crosses, which it did.
    What the meta-planner READS the event as — "a task has just become recognised" — is a stronger claim
    than the contract makes. If a one-shot semantics is wanted (one event per (task, episode)), that is an
    INTERFACE decision: a change to the event's definition or to the consumer's handling (a debounce, a
    per-episode latch, a gate on odds — TODO-65), not to the evidence model. Do not tune the likelihood to
    make the trajectory cross once.
(c) THE META-PLANNER'S HANDLING (out of scope): each crossing re-runs B2/B3 (s20_off re-decides at 20, 24,
    29, 30 and 87–103, moving the robot's item_4 delivery 52 → 60 and item_6's 136 → 144). Decide with
    TODO-48 (no trigger on a `most_likely` change above θ) and TODO-54 (`theta_crossed` on `unknown` after
    a pin): all three are the same question — what a trigger is an event OF.
Prior-on none of this occurs (no live rival flips); one crossing per recognition in every prior-on condition.
D2 (R1, September 2026 — to be decided from the T4 and T10 logs, together with TODO-48, TODO-54 and
TODO-64/65): under `b2a` (TODO-36) a repeated `theta_crossed` mostly ends in a CONTINUE — the current
task's hold is judged small against the human's remaining projection and B3 never runs — which
removes the re-decision churn recorded in (c) but may also hide a REAL change of belief (TODO-48's
case: `most_likely` moves while confidence stays above θ, or crosses again on a different task).
Whether the gate needs to see the hypothesis, not only δ, is D2's question.
Files: shared/io_contracts.md (`theta_crossed`), shared/meta_planner.py (`evaluate_triggers`)
Reference: analysis/i4d_fold_unknown/REPORT.md §6(a); analysis/i5_handback/; docs/recognizer_handback.md

**TODO-69 — The unassessed tail biases conflict-aware selection**
The human projection covers one recognised task. Beyond its end the robot's remaining segments
are shifted by any computed pause but not assessed, so they read as conflict-free by
construction. T1 measured a median unchecked share of ~49% per candidate; the bias is
systematic, since a longer candidate has more of its trajectory beyond the horizon and
therefore looks cleaner. Accepted deliberately for now (simplest option; decided with Hadi,
Sept 2026).
Three readings, none chosen: (1) ignore, as now; (2) compare candidates only over the common
assessed window; (3) carry the assessed fraction as a confidence on the cost, not a change to
its magnitude.
SINCE (F1, C, F47b): reading (1) stands and the tail is larger than T1 measured, since a hold may now
extend past T_h (F1: no hold cap). What happens in the tail is the separation stop's (C), and with
well-typed fixtures every stop so far fell in the tail (F47b) — the tail is where the blocked event lives.
Not to be closed by projecting the human's NEXT task from `scheduled_tasks`: that is the
script, not something the robot can know. The horizon can only be extended by observation.
Related: the "what is H" question (H bounds the human's projection, not the robot's ordering).
UPDATE (wait-decision revision, Sept 2026): A HOLD MAKES THIS WORSE. Realization estimates only
WITHIN the human's projected horizon; beyond it, segments are shifted but not assessed — and
every hold pushes MORE of the robot's trajectory past the horizon, so the candidate that waits
the most is also the one assessed the least. `RealizedPlan` carries the unassessed share for
this reason (a confidence on the cost, reading (3), can be computed from it; nothing consumes it
yet). Still accepted; still not to be closed by reading the script.
✅ DECIDED (R1, September 2026): reading (1). Realized cost = T_r + δ over the robot's FULL plan, no
correction for the unassessed tail; the unassessed share is LOGGED per candidate so that the bias can
be reported, not priced. Beyond T_h the plan is neither clear nor blocked (Property 2 as amended,
design_decisions.md "The robot can wait"); what happens there is the execution layer's (the
"execution-time avoidance past T_h" assumption). Readings (2) and (3) stay available as analyses of
the logged share.
Files: shared/meta_planner.py (_detect_interference, _cost), shared/projection.py
Reference: T1 measurement session; Phase 4C wait-decision session, September 2026

**TODO-70 — Per-segment vs whole-trajectory holds: confirm on data** ✅ DECIDED (R1, Sept 2026): whole-trajectory minimal shift; what remains open here is a hold at a chosen point ALONG a segment
DECIDED (R1, September 2026, on T1b): the hold policy is the WHOLE-TRAJECTORY MINIMAL SHIFT — one
hold δ at the robot's position at the trigger tick (possibly partway along a segment), every later
segment shifted by δ, δ the smallest shift ≥ 0 with no violation in [trigger, T_h] including at the
hold position itself. T1b (`analysis/t1b_realization/REPORT.md` §7, Finding 2): the per-segment
policy at its minimal hold and the whole shift agree on δ in every row both realize (0 of 87 rows
differ at any s); per-segment dead-ends where the whole shift does not (4 rows) and never the
reverse; and the loop as written in the design entry overshot the minimal hold by 5–25 ticks
(median) and reversed two argmins. Per-segment holds at segment boundaries are OUT. What this item
still holds open: a hold at a CHOSEN POINT ALONG a segment (walk part way, then stop), which may be
cheaper still but is a different convergence argument — DEFERRED, not scheduled in 4C. Original
entry retained below.
T1 measured ONE pause: the robot holds its start position for δ ticks, then runs its whole
projected trajectory unshifted against the unshifted human projection (`c_pause_delay.csv`).
The realization algorithm (design_decisions.md, "The robot can wait") holds PER SEGMENT — each
robot segment is placed at the earliest start time at which it clears, so a hold can sit before
the walk to the table rather than before the walk to the shelf, and later conflicts are
re-evaluated after every earlier hold. More precise, and its total hold can differ from T1's δ
in either direction (a hold placed later is shorter when the human has moved on; it is checked
at a position T1 never checked). Confirm on data when realization lands: re-run T1's rows with
both placements and record where they disagree and why. Out of scope by decision: a hold
placed MID-segment (walk part way, then stop), which may be cheaper still but is a different
convergence argument; and waiting elsewhere, which is a detour (a different strategy).
Files: shared/projection.py or the realization module (later task), analysis/t1_conflict_measurement/
Reference: Phase 4C wait-decision session, September 2026

**TODO-71 — The hold hint on the body side: execute, refine, never re-decide** — execution ✅ BUILT in Mesa (T4); refinement and its reporting OPEN
`UpdateResult` will carry the winner's realized holds (where, how long) as an execution HINT
(io_contracts.md §1.9, §4.1). The embodiment has to consume it, and the single-decision-path
rule (NOTE above, DESIGN-07's companion) fixes what consuming means: the executor stands still
for the hold (R1, September 2026: ONE hold δ, at the ROBOT'S POSITION AT THE TRIGGER TICK — the
"before the segment it precedes" wording of the per-segment design is superseded by the
whole-trajectory shift, TODO-70; in Mesa: STAND microactions at the trigger position for δ ticks,
then the plan, unless a later trigger re-decides), may REFINE it (the human deviated; its own
collision handling found the way clear earlier or later), and must never independently decide
whether to wait, which task to run, or silently drop the hold — the cost was computed on the
hold, and a behaviour that departs from it silently makes neither the cost nor the behaviour
authoritative. Open on the body side: how a refined hold is reported back (the world shows the
robot stationary; nothing says why), and whether a hold that the executor extends past the
next trigger should itself be a trigger. Mesa first (a STAND microaction per held tick, next
to `wait_at`'s existing STAND expansion in `action_decomposer.py`); ROS/PRIEST is Phase 6 and
treats the hold as a soft constraint, as it treats every hint.
✅ BUILT in Mesa (T4, September 2026). `UpdateResult.hold: int = 0` (whole ticks) carries δ. On
every non-terminal decision `RobotAgent.step()` calls `Executor.hold(result.hold, trigger)` after
the plan is adopted (`continue_plan()` on a continue). From that tick the executor runs one STAND
microaction per tick (no `remaining` param, so no `waited_at` / `waited()` fact) before it looks at
the plan. The cursor, microaction queue and completion bookkeeping are untouched, and the plan resumes
where it stood. The hold is not in `action_decomposer.py`: it is a decision about the task, not a step
of any action. INTERRUPTION: a later trigger re-decides as usual, and its decision REPLACES the hold
in progress with its own δ: a b2a continue's fresh realization, or 0 when the decision carries none
(B3 until T10, or no projection). The ticks not yet run are logged as interrupted. This matches T5's
"a hold re-realized identically keeps its countdown": in both interruptions measured (s10_off 29→33,
s20_off 20→24) the fresh δ equalled the planned δ minus the ticks already held (6−4 = 2, 7−4 = 3). The
executor adds, extends or drops no hold on its own. Logs: `[hold] step= <robot> start planned= trigger=
pos=` and `[hold] step= <robot> end planned= executed= interrupted= [by=]`.
MEASURED (T4, `b2a`, ρ = 0.5): 10 holds executed in s10/s20/s30_off (none in s00 or s30_on), 2
interrupted. Robot deliveries slip by the total hold: s10 +6, s20 +8, s30_off +7 ticks. Actual `[sep]`
below 50 cm around the held table deliveries: s10 unchanged in size (none 72–75, 4 ticks, min 30.87;
b2a 75–78, 4 ticks, min 30.87), because the robot now arrives as the human leaves instead of before
it; s20 6 ticks, min 11.64 → 3 ticks, min 25.40; s30_off 8 ticks, min 11.70 → 2 ticks, min 38.57.
Every remaining sub-50 tick falls past the hold decision's T_h, at the human's next task, which is
the "execution-time avoidance past T_h" assumption (TODO-73), with one exception: s10 tick 75, 49.15
cm, is inside the assessed window by 0.02–0.29 tick (step quantisation, a real residual under L2;
ruled on the T4 report, recorded in TODO-77). The measure still samples whole ticks (TODO-79). At the robot's grasp
(`task_committed`, or `theta_crossed` on the same tick) after a hold, re-realization added δ = 1 in
s20 (off and on) and s30_off. Execution was 0.79 / 0.14 ticks AHEAD of the projection that placed the
first hold: the latency the projection charges after `pick_up` is skipped when the `task_committed`
re-plan starts the carry on that tick. That is deterministic, robot-only and not quantisation (ruled on
the T4 report; TODO-77, fix with D2). The minimal whole-tick shift has no margin, so clearance currently
depends on that re-decision.
STALE AFTER T-B Q7, CLOSED BY D3 (September 2026): the body now spends the acknowledgement it states, so the
executed plan is the realized one, and the ablation (`analysis/ablation_task_committed/`, 26 pairs) removed the
trigger with no change in the world: `[sep]`, human and `[IR] step=` lines and completion byte-identical; the
1-tick holds at the grasp (s20 at 31, s30 b2a at 47) were the owed acknowledgement tick. No clearance depends on
the re-decision; the trigger is removed (design_decisions.md, "D3: task_committed is not a trigger").
STILL OPEN: refinement (the executor shortening or extending a hold against what the world shows),
and how a refined hold is reported back. Mesa has no refinement: it executes δ as decided. The
separation stop (C) is the other body-side stand — a safety refinement, not a hold — and whether the
mind is told of it is D2's question (TODO-73, R2).
✅ CLOSED (ruling on the T4 report): A DECISION WITH NO PROJECTION DROPS A HOLD IN PROGRESS, and that
stays. While the robot holds it stands, so its `holding` cannot change (`task_committed` cannot
fire; removed by D3) and its task cannot complete (`no_current_task` cannot fire, and B1.5 would skip B2 anyway).
The remaining route is `theta_crossed` whose projection is not admitted. Since the crossing already
clears the gate, that means `most_likely` is `unknown` or the hypothesis cannot be resolved: the
recognition behind the hold no longer stands, and a hold computed against it should not survive.
`b2a` then continues with hold 0, and the executor replaces the hold with that.
D3 (September 2026): whether a hold the executor extends past the next trigger should itself be a trigger — not a
trigger; if ever needed, its home is a body-side event (T-D), not the trigger set.
E2b, the hold's expiry event (dropped at D2; it has no entry of its own): not a trigger either; if ever needed,
its home is a body-side event (T-D).
Files: shared/types.py (UpdateResult), mesa_sim/executor.py, mesa_sim/action_decomposer.py,
mesa_sim/sim_agents.py, ros_sim/ (paused)
Reference: Phase 4C wait-decision session, September 2026; roadmap.md Phase 6 notes; T4


**TODO-72 — `io_contracts.md` §1.3 and §2.1 still describe the pre-I2 recognizer** [recognizer side] ✅ RESOLVED (4C housekeeping, Sept 2026)
RESOLVED: §1.3 now matches `shared/types.py` (field order and defaults) and names the one position lookup
(`shared/target_resolution.py`) with its two consumers, the `excess_path` evaluator and the `Projector`;
§2.1 describes the constructor as it is (`path_cost`, the support restriction, the evaluator-registry check)
and `update()` as the phase / evidence model of `recognizer_handback.md` §1, with the removed mechanisms
listed. Docs only.
Found while re-aligning the meta-planner sections after T7/T8 and the wait-decision revision
(September 2026); deliberately not edited then, since it is recognizer-side work. §1.3's
"scoped exception" paragraph names `direction_consistency_likelihood` and the resolver
helpers `_get_expected_position` / `_get_target_zone` in `recognizer.py`; §2.1's `update()`
correction describes the leg model (a discrete observation closes the leg, one chord per
leg, output = evidence × ω_context with the held-item refutation) and cites "One leg is one
observation". All of that is superseded by I2–I4d: targets resolve through
`shared/target_resolution.py` and the planner's `decompose()`; the movement likelihood is
the excess-path logistic (`excess_path`, `shared/likelihood_functions.py`) with a constant
`unknown`; there is no leg, no cosine kernel, no held-item rule, no ZONE_BOOST; the belief
re-initialises at the observed agent's task boundary; `unknown` folds with the stretch.
`recognizer_handback.md` §1–§2 is the current description to align §2.1 against, and the
I2–I4d entries in design_decisions.md the record. Also stale in the same passages: the
constructor paragraph's "persistent assignment prior" wording (it is a support restriction).
Files: shared/io_contracts.md (§1.3, §2.1), docs/recognizer_handback.md
Reference: wait-decision documentation session, September 2026

**TODO-73 — Mesa has no execution-time avoidance: agents may overlap** [post-4C; from R1] — the rule it must use is FIXED (F1) — ✅ CLOSED FOR MESA (C): the execution-time separation stop
✅ CLOSED FOR MESA (C, September 2026; design_decisions.md, "Execution-time separation stop"): before
every STEP the robot checks the step against the human's actual position this tick under the F1 rule
and stands instead when the step would break it (`Executor._separation_blocked`; run option
`separation_stop`, default off). Additive to the decided hold, no trigger, no rule for the Mesa human,
one `[stop]` line per refusal with the assessed-window label for D2. ACCEPTANCE: 0 violating robot
steps in every run with the stop on (`analysis/c_separation_stop/comparison.md`). ROS brings its own
implementation of the same rule (PRIEST, Phase 6). WHAT THE STOP EXPOSED, not fixed: in s00, s20 and
s30 the scripted human's last task ends at the shared table and it idles there for the rest of the run,
so the robot's last delivery is refused every tick and the run does not complete (only s10 does) — the
accepted indefinite-wait limit meeting a human that never leaves and a point table with one arrival
radius (TODO-74). F1's gap 2 (the robot approaching a human still at the table past T_h) is closed by
this for Mesa.
AFTER C (R2, September 2026; design_decisions.md, "After C"): the indefinite wait is correct under the
rule and the human's end state is an experimental condition (TODO-47 (d)); blocked time is the outcome
under the current scripts (`analysis/c_separation_stop/blocked.md`: s00 139, s20 156–158, s30 44–48
blocked ticks, s10 0; with TODO-32 landed, s40 29). OPEN FOR D2: "no trigger fires on a stop" is expected
to be reversed — the mind does not know the body has stopped; and marking a task not executable because
the body refused its step would introduce no parameter (not an exclusion threshold in T10's sense). The
stop-off baselines contain walk-throughs and support decision comparison, not safety claims.
THE RULE (F1, September 2026): when built, Mesa's execution-time avoidance uses robot-responsible
separation, the same definition realization checks (design_decisions.md, "Robot-responsible
separation"): the robot may not move so that the robot–human distance goes from at least
`min_separation` to below it, nor move within `min_separation` without the distance strictly
increasing; standing is always safe, so "stop" is always an admissible response. One definition for the
plan checked and the behaviour executed. Grounding of the stance (passive motion safety; ISO/TS 15066
speed and separation monitoring) and its scope are recorded in that entry. The gap it must cover is
also recorded there: past T_h the human vanishes from the assessment (s20_on ticks 54–56, 35.1 cm at
56 in the T10 baselines); in the F1 sweep every remaining rule violation at execution is past T_h or
under no projection.
THE STANDING-ROBOT CONSEQUENCE (F1): a standing robot may be in the human's path; the human's detour
is a team-level cost (TODO-15). The Mesa human has no avoidance, so while the robot stands the two
agents can come arbitrarily close or overlap — such moments are not robot violations. Evaluation of
actual separation counts as robot violations only moments breaking rule (a) or (b); moments where the
robot stands and the human closes are reported separately, not as failures. Reference classification:
`analysis/f1_robot_responsible/evaluate.py` (viol | stand | recede, inside / outside the assessed
window).
Realization decides only within the human's projection (design_decisions.md, "Assumption:
execution-time avoidance past T_h"); everything after T_h, and the residual conflict of an
all-unrealizable trigger, is left to an execution-time avoidance layer that Mesa does not have —
agents are points and may overlap. T9 adds a per-tick measure of the actual robot–human distance
(`[sep]` lines in the headless log) so that later tasks can report how often and by how much actual
separation falls below `min_separation`; nothing avoids anything. To build: Mesa's own local
avoidance, possibly using realization's output (the hold, the assessed window) as hints — the
Phase 4D role of a detour-capable realization also serving as execution-time path realization
(roadmap.md). Must respect the single-decision-path rule: refine motion, never decide whether to
wait or which task to run.
Files: mesa_sim/executor.py, mesa_sim/action_decomposer.py, mesa_sim/sim_agents.py
Reference: R1 decision record, September 2026; T9

**TODO-74 — The kitting table is one point; separate placement positions are a domain modelling question** [later]
Every delivery, robot's and human's, targets `kitting_table_0`'s single position, so two placements
within a tick of each other coincide exactly (T2's `min_dist = 0.0`, T1b's table convergences) and
every hold in the fixtures is a hold at the table. A real table (200 × 100 cm) has room for several
placement positions. Whether to model them — as several objects, as a parameter of `place`, or as an
executor-side offset — is a DOMAIN question for later, not a realization one; do not solve it inside
`shared/`.
THE POINT-PLACE FACT (R2, September 2026): with arrival radius r and min_separation s, two agents at one
place are at most 2r apart, so co-use requires s ≤ 2r and arrival on opposite sides — 50 vs 60 cm here,
the rim only, practically unreachable by straight-line arrival. A framework fact about body constants
against policy (design_decisions.md, "After C"); it is what makes C's indefinite wait the outcome at
every table delivery with the human standing there.
Files: domains/kitting/env_layout*.json, domains/kitting/actions.py, domains/kitting/tasks.py
Reference: R1 decision record, September 2026

**TODO-75 — `ros_sim/framework_HRI/guide.txt` refers to `env_layout1` with obstacles** [ROS side, paused]
NOT DONE at the 4C housekeeping: both remedies are outside what may be touched now — the guide is under
`ros_sim/` (paused, not modified), and registering `env_layout99` is excluded by CLAUDE.md (kept, not
registered). Do it when the ROS side resumes.
The ROS/PRIEST guide describes `env_layout1.json` with obstacles and scenario_10 with the robot
assigned item_5 / item_1 / item_7. Since R1 `env_layout1` is the cleaned layout (no obstacles, new
scenario_10 pool) and the old layout is `env_layout99.json`, which is NOT registered in
`domains/kitting/registry.py`. The ROS path would need `env_layout99` registered (or its own copy) to
reproduce what the guide describes. Not touched: `ros_sim/` is paused.
Files: ros_sim/framework_HRI/guide.txt, domains/kitting/registry.py
Reference: R1 decision record, September 2026

**TODO-76 — The trigger name `task_committed` reads as the human's commitment; it is the robot's grasp** [naming only]
`evaluate_triggers()` fires `task_committed` when the ROBOT's `holding` goes from None to an item —
the robot has grasped and its method set changes (`deliver_already_held`). Read next to the
recognizer's vocabulary the name suggests the observed human committing to a task, which it never
means. Rename (e.g. `robot_grasped`) when a session touches the trigger set; a rename changes every
`[meta-trig]` / `[meta]` line, so do it with a baseline regeneration, not in passing.
✅ MOOT (D3, September 2026): the trigger is removed, so there is nothing to rename.
Files: shared/meta_planner.py (`evaluate_triggers`), shared/io_contracts.md (§2.2)
Reference: R1 decision record, September 2026

**TODO-77 — Projection runs ahead of execution by the executor's acknowledgement ticks** ✅ RESOLVED (L2 Sept 2026; the residual closed at T-B Q7, Sept 2026) — the systematic whole-tick lag was removed at L2; the robot-only tick recorded below as open was the body cancelling a completion tick at a reload, and is fixed in the body at T-B Q7; WHAT REMAINS IS STEP QUANTISATION ALONE, uncompensated by decision (L2) — the task-completion tick ✅ ADDED (F1)
THE TASK-COMPLETION TICK (F1, September 2026): the trailing tick the L2 report left unmodelled — the
tick `Executor.step()` spends in `_on_task_complete()` after the last action's acknowledgement — is
now charged once per projected task, for both agents (measured: human release 54 / ack 55 / complete
56 / first step 57; robot release 30 / ack 31 / complete 32 / first step 33), from
`mesa_sim/executor.TASK_COMPLETION_LATENCY = 1.0` through `Projector(task_completion_latency=...)`,
appended by `project()` as a stationary segment at the task's end position. Effect: T_h one tick
later per human task, every T_r one tick longer; every T10 hold at s20/s30 grew by one; plain
decisions unchanged. Still uncompensated: step quantisation and the robot's skipped acknowledgement
(below).
REMOVED (L2): (a) the ACKNOWLEDGEMENT LATENCY is now charged per action, as a stationary segment at the
position the action ended at, from a constant the body supplies
(`mesa_sim/executor.ACTION_COMPLETION_LATENCY = 1.0`, passed to `Projector`); (b) the OBSERVATION
OFFSET is gone — `project_human()` starts the human's projection at
`mesa_sim/sim_agents.OBSERVATION_OFFSET = 1.0` rather than at 0, so both projections sit on one clock
(Mesa's scheduler moves the human before the robot observes it). Placement lead medians, this item's
own measure: robot −1.46/−3.32 → −0.46/−0.32 and human −2.21/−5.32 → −0.21/−1.32 (2-/4-action plans).
Full record and the method: `analysis/l2_execution_lag/REPORT.md` (deleted in the analysis cleanup, September 2026; carried in the L2 entry of design_decisions.md and TODO-77).
WHAT REMAINS, deliberately uncompensated:
  - STEP QUANTISATION. A walk of projected duration `dur` executes as ceil(dur) discrete steps and the
    walker stops on the first step INSIDE the arrival radius rather than on it, so it finishes
    ceil(dur) − dur ticks late AND the next walk starts up to one step off the projected start, which
    can make that walk a whole step longer. Per walk it is under a tick; over a two-walk plan it can
    exceed one (the human's 4-action median is −1.32). Decided at L2: not compensated, and no safety
    margin anywhere to absorb it.
    T4 (`b2a`, executed holds): a real residual under L2. In s10 (off and on) the actual `[sep]` at tick
    75 is 49.15 cm, INSIDE the assessed window of the hold decision (step 47 vs T_h 47.29 off, step 51
    vs 51.02 on), where the realized plan cleared 50 cm (its minimum 50.93 / 55.24 cm). Step
    quantisation; recorded, not compensated. (`[sep]` samples whole ticks, TODO-79.)
  - THE ROBOT'S SKIPPED ACKNOWLEDGEMENT (4-action plans only, +1 tick, the projection running LONG)
    ✅ FIXED IN THE BODY (T-B Q7, September 2026). This bullet and the ORDERINGS paragraph below are the
    record as it stood when the item was open; what changed is stated at the end of that paragraph.
    The projection charges four latencies, but the robot re-plans at its own `task_committed` trigger,
    which fires on the tick that would have acknowledged the `pick_up`; the fresh `deliver_already_held`
    plan does not contain that `pick_up`, so `continue_plan()` loads from the start and the carry begins
    on that tick. One charged latency is never spent. Modelling it would require the projection to
    predict the robot's own future triggers, which are decided FROM the projection — circular, and not
    attempted. It partly cancels the quantisation in those rows (median −0.32), which is arithmetic, not
    accuracy. OPEN as a known bias; revisit only if T3/T10 show it mattering.
    T4 SHOWS IT MATTERING (accepted for now). In s20 (off and on) and s30_off the first hold's
    clearance depended on the robot's own grasp trigger re-realizing it. The projection that placed
    the hold charges a latency after `pick_up`; execution skips it, because the `task_committed`
    re-plan starts the carry on that tick. At that re-decision execution was 0.79 (s20) / 0.14
    (s30_off) ticks ahead of the placing projection, and `b2a` re-realized δ = 1 (s20_off 30, s20_on
    30, s30_off 46). Deterministic, robot-only, not quantisation. The minimal whole-tick hold has no
    margin, so CLEARANCE CURRENTLY DEPENDS ON THAT RE-DECISION: without the grasp trigger's re-plan
    the robot would execute a plan that no longer clears. ROUTED BY D2 (September 2026): not a trigger
    question after all — D2 kept this item out of the trigger set deliberately, as a projector
    accounting item (design_decisions.md, "What a trigger is an event of"). `task_committed` is
    unchanged by D2, so the dependency above stands as measured; the fix, if one is made, is on the
    projection side (charge no latency execution does not spend), not a trigger.
    STALE AFTER T-B Q7, CLOSED BY D3 (September 2026): "clearance currently depends on that re-decision" no longer
    holds. T-B Q7 made the body spend the acknowledgement, and the ablation on that body
    (`analysis/ablation_task_committed/`, 26 pairs, with and without `task_committed`) changed nothing in the
    world: `[sep]`, human and `[IR] step=` lines and completion byte-identical, in-window sub-min_separation ticks
    unchanged (TODO-90); the 1-tick holds at the grasp (s20 at 31, s30 b2a at 47) were the owed acknowledgement
    tick, spent as the `pick_up` acknowledgement at the same position without the trigger. The trigger is removed
    (design_decisions.md, "D3: task_committed is not a trigger").
VERIFIED: a discrete-step forward model of the executor, using no execution data, predicts the actual
release tick exactly for all 68 human and robot 2-action rows and exactly one tick early for all 35
robot 4-action rows — so the residual is fully attributed, with nothing unexplained.
UNDER ORDERINGS (T-B2a, September 2026; recorded, NOT acted on): the skipped acknowledgement reaches the
NEXT ENTRY's start step. Every entry projected with a `pick_up` ends one tick later than execution reaches, so
entry k+1 starts late by about one tick per preceding entry that contains a `pick_up`, cumulative, partly
masked by quantisation. Measured on scenario_80: from the first decision entry 1 ends at 39.265 projected, the
real next decision is at 39 ticks; the carry part alone 17.38 projected against 18 real; so the fetch part
runs 0.885 long = +1 − 0.115 quantisation. RULED: on plain cost the extra tick is nearly constant across the
orderings of one pool, so T-B2b is unaffected. On REALIZED cost it is not harmless: a later entry sits late
against the human projection, so its violating shift intervals are evaluated at the wrong time. A design
question for cchat BEFORE T-B2c; not to be fixed unasked.
RULED AND BUILT (T-B Q7, September 2026; design_decisions.md, "A reload never cancels a completion tick the
body states"). The fix is the BODY'S, not the projection's: the `Projector` holds no latency of its own, and
`io_contracts.md` §6 invariant 12 already required the embodiment to supply the ticks its executor actually
spends — the body stated a value its own executor did not keep. Nothing in `shared/` changed and
`ACTION_COMPLETION_LATENCY` keeps its value. `Executor._reload()` now keeps whatever completion tick the
replaced plan is owed and `step()` spends it, executing nothing: a completed action's acknowledgement and a
finished task's completion tick alike, both of them where the completed action is the plan's last, and
whichever way the plan is replaced (a continue past the action in flight, a switch, or a trigger landing on
the completion tail, which used to cut it short). A hold decided at that trigger CARRIES the owed tick as its
first tick rather than adding one, so the executed plan equals the plan that was realized. RESIDUAL, with a
hold of 0: the plan resumes one tick after the start that decision's own projection assumed — one tick, on the
HEAD only, at a robot re-decision that reloads, NOT ACCUMULATING, and invisible to `shared/` without the
circular prediction above. MEASURED: the executed fetch part of every scenario_80 delivery gains exactly one
tick and the carry part is untouched (total executed minus projected −0.27 → +0.73, +0.31 → +1.31,
+0.32 → +1.32, +0.89 → +1.89, every residual now positive as ceil-per-walk requires); completion from the
world fact moves one tick per robot delivery across the 20 baselines, less where a hold carried the tick.
WHAT IS LEFT OF THIS ITEM IS STEP QUANTISATION, uncompensated by decision (L2), above.
GONE WITH THE TRIGGER (D3, September 2026): the "RESIDUAL, with a hold of 0" above was measured at the
`task_committed` reload; that decision no longer exists, and without it the release residual is the whole plan's
quantisation (the ablation's table). The body's rule stands for any other re-decision that reloads on an owed tick.
ALSO NOTED at L2, out of scope there: with the two agents in phase the superseded
`min_safe_distance = 1.0` exclusion fires again (once in the ten-condition sweep, scenario_30 prior-on
step 21, `min_dist` 0.49 cm at the mirror crossing) and changes that run's decision sequence. The
threshold is already superseded (R1, TODO-30) and goes with T10; it is a vestigial mechanism reacting
to a newly-accurate number, not a new policy. And: there are now TWO segments per action, so anything
indexing a plan's actions by segment position must use the stride (`analysis/t1b_realization/analyze.py`
`phase_at` does; L2's own scripts read the stride and handle both).
[original entry]
With walks ending at the arrival radius (T9) the projection no longer over-estimates any walk, and
what remains is on the body side: the executor spends one tick ACKNOWLEDGING each completed action
(the tick on which `at` / `holding` / `obj_at` is seen true and the cursor advances; `micro=None` in
the log) — a delivery pays three before its release (the robot two: the `task_committed` continue
loads `deliver_already_held` and skips the grasp's acknowledgement); each walk also ends on a discrete
step 10–29 cm from the target rather than at 30 (0 to ~1 tick later, with `ceil`); and the human's
projection starts from its position AFTER the trigger tick's step (it moves before the robot
observes), one tick later than the robot's own. Measured (`analysis/t9_arrival_radius/REPORT.md`):
placement lead −1.0 to −6.4 ticks, never positive; medians robot −1.5 / −3.3 (after / before the
grasp), human −2.2 / −5.3. Options, none chosen: model the acknowledgement as a body-supplied
per-action overhead in the `Projector` (as `default_action_cost` is supplied); remove the
acknowledgement tick from the executor (a behaviour change to both agents, every baseline moves);
accept it and read T_r and T_h as 1–4 ticks optimistic. It matters for realization because every
hold is measured against T_h and every arrival gap at the table is of the order of these offsets.
Files: mesa_sim/executor.py (`step`, `_is_action_complete`), shared/projection.py, mesa_sim/sim_agents.py
Reference: T9 (`analysis/t9_arrival_radius/REPORT.md`, "The premise, measured")

**TODO-78 — A run's log does not record the θ it was produced at** ✅ RESOLVED (T10): one `[run]` header line per robot
Nothing in a headless log states the gate's value, so a log cannot be interpreted without knowing which
code produced it. Five analysis scripts therefore hardcode 0.75 to read their own logs
(`analysis/f1_foreseeable_fixture/measure.py` (deleted in the analysis cleanup, September 2026; the folder's REPORT.md stays), `analysis/i3_phase_model/check_i3.py` (deleted in the analysis cleanup, September 2026; the folder's REPORT.md stays),
`analysis/i4_evidence_model/check_i4.py` and `pivot.py` (deleted in the analysis cleanup, September 2026; the folder's REPORT.md stays), `analysis/i1_ir_audit/measure.py` (deleted in the analysis cleanup, September 2026; carried in the I2 and I3 entries of design_decisions.md)) — correctly,
since they are records of runs made at that value and reading a live constant would silently reinterpret
old logs the day θ changes or becomes derived (TODO-64, TODO-65). The `[meta-proj]` line does carry
`theta=`, but only on ticks where a trigger fired and a projection was considered, so it is not a header
and is absent from runs with no admitted trigger. Proper fix: one run-header line naming the parameters a
log was produced under (θ at least; `min_separation` and ρ join it when T10 and T4 land). It CHANGES EVERY
LOG, so it needs a baseline regeneration and does not belong in a behaviour-preserving change; do it when
a task is regenerating baselines anyway. Until then the hardcoded literals stay, and are correct.
✅ BUILT (T10, September 2026): one `[run] <robot> gate_strategy= cost_strategy= theta= rho=
min_separation= (min_separation_in_motion_ticks= x assumed_speed=)` line per robot at construction
(`mesa_sim/sim_agents.py`, from read-only `MetaPlanner` properties). Landed in its own commit, the
rest of the log byte-identical; the T10 baselines carry it. The hardcoded literals in the older
analysis scripts stay, correctly, as records of runs made before the header existed.
Files: mesa_sim/sim_agents.py (the `[run]` line), shared/meta_planner.py (parameter properties), analysis/*/ (readers)
Reference: θ single-source session, September 2026; T10

**TODO-58 — β is in centimetres: the detour tolerance is layout-scale dependent** — REWORDED (T-A1, Sept 2026): β is a physical tolerance on wasted path, fixed; not a scale item
REWORDED (T-A1, September 2026): β is a PHYSICAL tolerance on the path a walking human wastes against the
direct path to a target, in length units (0.01 /cm: an excess of 100 cm gives L ≈ 0.54), and it is FIXED.
A detour of a metre is a metre in a small room or a large one: how much a person strays from a direct
walk is a property of people walking, not of the layout, so the defect stated below ("a layout twice as
large needs half the β") is withdrawn. The value is decided on IR grounds (what excess a walker toward a
target plausibly shows; the 30 cm `PROXIMITY_THRESHOLD` slop it must tolerate), NOT measured or tuned on
fixtures, and it is not part of TODO-47's calibration. What stays true below: the fractional reading was
measured and rejected, and the Euclidean path cost is exact only in Mesa (hand-back §3.3). The original
entry is the record of the scale-dependent reading.
✅ BUILT (T-A1 follow-up 2, September 2026): β has left `shared/`. `BETA` is removed from
`likelihood_functions.py`; `IntentionRecognizer(beta=...)` is a required argument in the body's length units,
passed to the excess-path evaluator; Mesa supplies 0.01 /cm from `mesa_configs.yaml` (`simulation.beta`, no
fallback) and the `[run]` header names value and source. Reason: β carries a unit, so its number means
something only in the body's units, and `shared/` computes in whatever units the body reports positions in
and must not hold a value that fixes them (the `min_separation` reasoning, TODO-28). One fixed value per
embodiment, decided on IR grounds; not per layout, and no fixture chooses it. Behaviour byte-identical at 0.01
on the regression and evaluation fixtures.
`BETA = 0.01 /cm` was chosen on layouts of 800–2000 cm; a layout twice as large needs half the β
(TODO-28's class of defect). The fractional reading — excess as a fraction of C(origin, target) — was
measured and rejected: its reference length goes to zero at every origin that sits near its target
(every `deliver_with_return` carry phase, every regress at the 30 cm proximity threshold), so a 100 cm
excess there is an infinite detour, and where it produced coffee crossings it did so by coffee having
the longest direct distance among the stuck-origin hypotheses (s30's first task then reveals after its
grasp). A scale-invariant form would normalise by a layout-level length (workspace diagonal, mean
inter-target distance), which `WorldState` does not carry. Also load-bearing and in cm:
PROXIMITY_THRESHOLD (30) sets the geometric slop β must tolerate (×0.85 at β = 0.01).
Files: mesa_sim/mesa_configs.yaml (`simulation.beta`, since T-A1), shared/recognizer.py (`beta`), mesa_sim/world_state_builder.py (`PROXIMITY_THRESHOLD`)
Reference: I4 evidence-model session; analysis/i4_evidence_model/REPORT.md §4.3

**TODO-79 — The `[sep]` execution measure samples whole ticks and misses minima between ticks** ✅ DECIDED (T10): `min=` alongside `dist=`, and sub-min_separation moments classified against the assessed window
`[sep]` (T9; `mesa_sim/run_mesa.py`) logs the robot–human distance once per tick, at the tick's end
positions. Between ticks both agents move up to 20 cm, so a close pass between two samples is read at
the nearer sample, not at its minimum. L2 measured the case: scenario_30's head-on pass reads 11.0 cm
in `[sep]` while the continuous minimum is near 0 (the agents pass through each other between ticks 22
and 23; `analysis/l2_execution_lag/REPORT.md` (deleted in the analysis cleanup, September 2026; carried in the L2 entry of design_decisions.md and TODO-77)). Realization's own definition is continuous — a
violation is any moment strictly below `min_separation`, along straight-line motion within a segment
(T3, `shared/realization.py`) — so an evaluation that reads `[sep]` against `min_separation` would
compare a sampled execution against a continuous decision and under-count violations by up to one
tick of motion per agent. TO DECIDE IN T10: whether the evaluation measures distance along straight-line
motion between consecutive tick positions (the minimum over the tick, closed form, the same geometry
as `shift_violation_interval`) instead of at the tick positions only. Not a change to behaviour either
way; it is the measure.
✅ DECIDED AND BUILT (T10, September 2026): the `[sep]` line carries both — `dist=` (the tick-sampled
figure, unchanged) and `min=`, the continuous minimum over the tick with both agents moving in a
straight line from their previous positions to these, the closed-form clamped projection
(`run_mesa._min_separation_over_tick`). A small change (one function, one field); the measure only.
Evaluation (`analysis/t10_b3_realized/evaluate.py` (deleted in the analysis cleanup, September 2026; carried in the T10 entry of design_decisions.md, TODO-36 and TODO-79)) classifies every tick below `min_separation`
against the assessed window of the decision in effect: inside (its motion lies in [1, T_h] on that
decision's projection clock), edge (straddles the offset or T_h), outside (past T_h, no projection, or
the robot finished). MEASURED on the T10 baselines: the continuous minimum lowers the crossing minima
(s30 tick 23: 11.03 → 0.00, the pass-through L2 found; s20_off crossing: 11.64 at tick 51 → 9.02 over tick 52) and extends each
episode by one tick at its end; it moves no tick from outside to inside. The only INSIDE sub-50 tick
that is not a fallback's is s10 tick 75 at 49.15 cm (dist and min agree — the minimum is at the tick's
end), TODO-77's step-quantisation residual; every other sub-50 moment is past T_h, under no projection,
after the robot finished, or inside the s30_on all-unrealizable fallback's window (TODO-30).
Files: mesa_sim/run_mesa.py (`[sep]`, `_min_separation_over_tick`), analysis/t10_b3_realized/evaluate.py (deleted in the analysis cleanup, September 2026; carried in the T10 entry of design_decisions.md, TODO-36 and TODO-79)
Reference: T3 session, September 2026; L2 report; T9 (`[sep]` introduced); T10

---

## 🧹 Refactoring / Cleanup TODOs

**REFACTOR-01 — Normalize kitting `env_layout1.json` to flat `env_objects` format** ✅ RESOLVED
Both kitting layouts (`env_layout0.json`, `env_layout1.json`) now use the
unified `env_objects` list, items merged in with `type`/`subtype` fields.
Files: domains/kitting/env_layout0.json, domains/kitting/env_layout1.json

**REFACTOR-02 — `parse_args()` called twice in `run_mesa.py`**
Both `_make_domain_model()` and `run_headless()` call `parse_args()` independently.
Refactor to parse once at module level and pass config around.
Files: `mesa_sim/run_mesa.py`

**REFACTOR-03 — `domains/README.md`: update domain folder name references**
README still references `dock_delivery_loading` in the folder listing.
Update to `dock_loading`.
Files: `domains/README.md`

**REFACTOR-04 — `roadmap.md`: Phase 2.1 and 2.2 status and Phase 4 expansion** ✅ DONE
Updated in this session.

---

## 📋 Known Limitations (Accepted for Phase 2.1)

**LIMIT-01 — Straight-line agent movement through walls**
Agents move in straight lines ignoring walls between hall/dock/truck.
Accepted: same as kitting. Fix deferred to Phase 4 path planning (TODO-09, DESIGN-13).

**LIMIT-02 — Parallel task independence: human scans before robot delivers**
Human `scan_pallet` executes without waiting for robot `deliver_pallet` to complete.
Mitigated by `office_break` delay in scenario. Proper fix: DESIGN-01.

**LIMIT-03 — Gate always open**
`gate_is_open(dock_gate)` emitted unconditionally. Gate state not modeled dynamically.
Fix: TODO-08 (`open_gate` action schema + `gate_closed` method).

**LIMIT-04 — All pallets start at same position (truck center)**
Pallets 0–5 all share `truck_interior` center position. No individual slot positions.
Deferred: individual pallet slot positions within truck area.

**LIMIT-05 — Empty pallet bays not wired to `LOAD_RETURN` task execution yet**
`load_return` tasks defined and in scenario but may not complete correctly
until BUG-01 and BUG-02 are resolved and full scenario runs end-to-end.

**LIMIT-06 — Robot task queue is pre-ordered in scenario file** [Phase 4] ✅ RESOLVED
Robot's `scheduled_tasks` is currently an ordered list in `AgentConfig`.
Ordering should be the meta_planner's responsibility. Accepted for Phases 1–3;
fix in Phase 4 via TODO-14.
Resolved: the robot's task pool is `AgentConfig.assigned_tasks` (unordered); ordering is the
meta_planner's (assignment-prior session, September 2026).

**TODO-80 — Declared human behaviour outside the robot's domain knowledge** [later extension; from F47b]
Every human stay a fixture can script today comes from a task the robot's domain describes, so the robot
recognises it (at arrival at the latest, the move_to fold) and realization prices it (F47b: no valid fixture
produces a mid-run block). Testing an unforeseen stay — the case D2's blocked-execution event serves —
therefore needs human behaviour the ROBOT'S knowledge does not cover, declared as such: a scenario-side
behaviour vocabulary for the human executor (a stay of a stated length at a stated place) that is NOT a task
schema and adds no hypothesis, or a domain given to the human that is a superset of the robot's. Never by a
type mismatch (F47's waypoint coffee break) or by repurposing an existing task in a role its schema does not
describe. Design question for the design claude chat (we call it cchat); nothing built.
REVISED (T-A1, September 2026): the scenario-side vocabulary is T-C's HUMAN ACTION SCRIPT: the human's
scenario is a sequence of primitive actions (move_to a named object or a point, pick_up, place, wait, stay
for a stated number of ticks), run by the human executor on the scenario layer. The declared stay is one
script action (`stay` at the kitting table for N ticks after a delivery), not a mechanism; it adds no
hypothesis and the robot's mind receives nothing from the script. The blocked-execution event below and
the wait / reconsider pair are built and evaluated in T-D, on that fixture. design_decisions.md, "The
human's scenario is an action script" and "Robustness is tested in kitting".
THE BLOCKED-EXECUTION EVENT, designed in D2 (September 2026), to be built here when a valid fixture blocks
mid-run: the separation stop's refusal of a STEP becomes a fact in `ExecutorState` (the body reports, it
decides nothing; no threshold — R2, "not an exclusion threshold"); `evaluate_triggers()` fires `blocked` once
per blocked EPISODE (the first refused tick), not per refused tick; `update()` routes it past B2 as
`no_current_task` is routed (B2 is commitment to a plan that is executable; a refused plan is not the case
B2 judges). Response policy: WAIT now — the decision stands, the robot re-decides at the next trigger;
RECONSIDER recorded as the alternative — B3 with the blocked task marked not executable now (a mark on the
candidate, not a cost). Under wait the trigger cannot change a decision, so it fixes no liveness: with the
stop on, every block in the current fixtures is the human's terminal stay at the table with one task left
(`analysis/c_separation_stop/blocked.md`), where neither policy has anything to choose. The earlier claim
that D2 removes that deadlock is withdrawn; the remedy is reconsider with a fixture that has an alternative,
or 4D's human cooperation (TODO-15).
OBSERVED (T-C2c, `analysis/tc2c_scripts/`, scenario_01): the declared stay is scriptable; after `Stay(40)` the script
ends and the human stands at the table, so with the stop on the robot is refused from 79 to the end (121 ticks), the
terminal-stay block above; a stay that ends needs content after it.
T-D (the play, `analysis/tc2c_scripts/play.md`): T-D's blocked fixture uses a stay that ENDS. A stay that ends is waited out with the stop on
(scenario_94: refused 144–186, completion 413 against 370; scenario_23's mid-run stay likewise); only the human's
end-of-script stand at a table deadlocks (01, 02, 04, 23). Scenario-authoring convention since 23 Sept 2026: a
script ends with the human leaving the workspace, unless the scenario is about that terminal stand
(design_decisions.md, "The human action script (T-C1, decided)", AS BUILT convention).
Files: domains/kitting/scenarios.py, mesa_sim/sim_agents.py (HumanAgent), shared/types.py
Reference: F47b session, September 2026; design_decisions.md, "Scheduled bindings are typed"

**TODO-81 — The Mesa decomposer reads the literal `"?duration"`; the schema names the binding (`duration_key`)** [housekeeping; from R2]
NOT DONE at the 4C housekeeping, because the fix as filed is not behaviour-preserving: `dock_loading`'s
`wait_at` is `STAND*` with a `?duration` binding (`PT60S`, `domains/dock_loading/tasks.py`) but declares
no `duration_key`, so reading `action.schema.duration_key` would shrink its waits to one tick. Kitting is
unaffected. Needs `duration_key="?duration"` on dock_loading's `wait_at` in the same change (a deferred
domain; which also makes its Projector price the wait, the mismatch this item is about).
`action_decomposer._expand_stand` reads `action.bindings.get("?duration", "PT1S")` while the projector reads
the key the schema declares (`ActionSchema.duration_key`, TODO-32). Two spellings of one key in two layers is
a mismatch risk; the decomposer should read `action.schema.duration_key` (falling back to one tick when the
schema names none). Same numbers today; fix when `action_decomposer.py` is next touched, with the regression
sweep (behaviour-preserving, byte-identical).
Files: mesa_sim/action_decomposer.py (`_expand_stand`), shared/types.py (`ActionSchema.duration_key`)
Reference: R2 session, September 2026

**TODO-82 — The planner's debug line prints whole schema objects, so any schema field breaks byte-identity** [housekeeping; from R2] ✅ RESOLVED (4C housekeeping, Sept 2026)
RESOLVED: the line is emitted by `HumanAgent.step()` in `mesa_sim/sim_agents.py` (not `shared/planner.py`)
and now prints `[action{bindings}, ...]`. Every `[planner] self.current_plan` line changed (2–5 per log in
the regression sweep); no other line, and none of the regression greps.
`[planner] self.current_plan for ...` logs the `AbstractPlan` repr, which includes every `GroundedAction`'s
`schema` dataclass. Adding a field to `ActionSchema` (TODO-32's `duration_key`) changed that line in every log
without any behaviour change, so "byte-identical" had to be qualified. The regression greps do not include
the line, so drift detection is unaffected. Print the plan's action names and bindings, not the schema, or
drop the line.
Files: shared/planner.py (or wherever the `[planner] self.current_plan` line is emitted)
Reference: R2 session, September 2026

**TODO-83 — Unused interference machinery: `ConflictPoint`, `InterferenceAssessment`, `discretized_time_sampling`, `closest_point_of_approach`, `interference_spatial_resolution`** [housekeeping; from T10 / F1] ✅ RESOLVED (4C housekeeping, Sept 2026)
RESOLVED: removed, with the helpers only the sampler used (`_position_at`, `_distance`, `_midpoint`,
`_speed` in `trajectory_algorithms.py`) and `action_decomposer._get_interference_spatial_resolution`.
Regression greps byte-identical. `analysis/t1*` scripts that call the sampler or read the config key are
historical and do not run at HEAD (they already depended on `_detect_interference`, gone since T10); F1's
`validate.py` reads `types.py` from commit 08b1167 and is unaffected. io_contracts §1.9 / §2.2b and the
roadmap updated.
Since T10 nothing in the run path consumes `discretized_time_sampling()` or its `ConflictPoint` list;
`InterferenceAssessment` is produced by nothing; `closest_point_of_approach()` is an unbuilt stub whose
`NotImplementedError` message still calls the sampler "the current default interference algorithm";
`mesa_configs.yaml: simulation.interference_spatial_resolution` and
`action_decomposer._get_interference_spatial_resolution` bind a resolution nothing samples with. Realization
uses `shift_violation_interval()` only. Remove or re-home when a task touches these files; the `analysis/t1*`
reports cite the sampler historically. io_contracts §1.10 / §2.3 describe the types as retired.
Files: shared/trajectory_algorithms.py, shared/types.py, mesa_sim/action_decomposer.py, mesa_sim/mesa_configs.yaml,
mesa_sim/sim_agents.py
Reference: T10; F1; wrap-up, September 2026

**TODO-84 — Selection against the expected realized cost over the belief** [Phase 5 comparison; from T-A1]
Today the belief is used as a bar, not a magnitude: `_clears_gate` admits the most likely hypothesis's
projection, and B3 realizes every candidate against that one projection as if it were certain
("confidence is a gate, never a magnitude"). A belief of 0.76 and one of 0.99 on the same hypothesis give
the same decision, and a rival at 0.2 prices nothing. Recorded as a limitation in design_decisions.md
("The belief is used as a bar, not a magnitude"). The comparison to make, later, in Phase 5: selection on
the EXPECTED realized cost over the belief (each candidate realized against each admitted hypothesis's
projection, weighted by its probability) against the current bar. A comparison, not a change: nothing in
the design is changed by recording it.
Files: shared/meta_planner.py (`_clears_gate`, `update_human_projection`, `_replan_tasks`)
Reference: T-A1, September 2026

**TODO-85 — A stationary human: a stay as evidence (a) and the robot's action under `unknown` (b)** [T-C open item; from T-A1]
A tick with nothing walked is not an observation (the empty-stretch rule, I4c), so a human who stops produces
no evidence for or against anything, however long: picked up item_2 and stood fifty ticks, the belief stays
with `deliver_item(item_2)` on top; `unknown` rises only from walked excess. With `unknown` on top, admission
returns `none(unknown)`: no projection, B3 prices no hold, only the separation stop reads the human's position.
T-C's script makes a stay expressible, so this can no longer stay implicit. (a) Recognizer: should N ticks
standing still count against pursuing a task and for `unknown`? A duration term with its own form, on IR
grounds, not a constant; if taken, a separate item T-H. (b) Meta-planner: under `unknown`, CANDIDATE only,
project the human as stationary at its current position for a bounded horizon, so realization prices holds
against where the human is. Both open, decided together in T-C1. Fixed either way: the recognizer judges
nothing, the meta-planner owns admission, the stop covers what no projection covers. Exposing fixture: pick up
an item and stay still mid-carry; expected today: frozen belief, no trigger, a hold placed for a moving human,
the conflict later than realized, refused by the stop inside the assessed window (the first fixture where the
stop and realization overlap). design_decisions.md, "A stationary human".
OBSERVED (T-C2c, `analysis/tc2c_scripts/`, scenario_11): a stay mid-carry (30 ticks at the coffee machine holding
item_2) freezes the belief (`deliver_item(item_2)` 0.550, `coffee_break` 0.345, `unknown` 0.088) with no trigger,
as expected. For (b), observed in scenario_01: once the human's hypothesis space is exhausted (its last assigned
task pinned), `unknown` reads 0.995 and no projection exists, so a finished work order and unmodelled behaviour are
indistinguishable to `update()`. T-D decides.
THE GENERAL FORM OF (b) (the play, `analysis/tc2c_scripts/play.md`): the robot is blind after EVERY human task completion, not only when the
hypothesis space is exhausted. The episode boundary resets the belief to the prior, below θ, so no projection is
admitted, while the human stands at the table it just delivered to, which is where the robot delivers. scenario_72:
the robot's carry passes 0.78 cm from the standing human (tick 100), before the robot's own completion; 01, 02, 04,
22, 24, 52 show 1–15 cm at the end of the run (stop off). Only the separation stop covers it. T-D's opening item.
Files: shared/recognizer.py (`_progress_likelihood`), shared/meta_planner.py (`update_human_projection`)
Reference: T-A1, September 2026
See TODO-95 (23 Sept 2026): the deferred stationarity channel is taken up there as a design task.

**TODO-86 — AgentConfig's key equality blocks a scripted delivery to another table** [deviation-case prerequisite; from T-B1a] ✅ CLOSED by T-C1 (23 Sept 2026): the work order and the script are compared by provenance (every assigned task exactly once), not by key equality; a delivery to another table is a `deviate` edit of an assigned task. design_decisions.md, "The human action script (T-C1, decided)". ✅ BUILT (T-C2a): `shared.types.check_work_order`, run by `AgentConfig.__post_init__` and by the loader on the resolved script; a `deviate` to another table keeps the assigned task's provenance
`AgentConfig.__post_init__` (shared/types.py) requires the human's `assigned_tasks` keys to equal the
non-foreseeable `scheduled_tasks` keys exactly. Since T-B1a the human's `scheduled_tasks` may bind
`?kitting_table` to a table other than the item's designated one (the precedence rule keeps the binding),
but such a task has a different `task_instance_key` from its assigned counterpart (which must bind the
designated table, `check_task_destinations`), so the scenario is rejected at construction ("Scripted but not
assigned ..."). Checked in T-B1a: with that check bypassed, the scenario loads, and a bound table grounds
the carry walk to that table. Not in T-B. It is a prerequisite of the deviation case, which arrives with action-level
scripting of the human (T-C); decide there what the correspondence between work order and script compares.
Recorded, not fixed.
Files: shared/types.py (`AgentConfig.__post_init__`)
Reference: T-B1a, September 2026; design_decisions.md, "An item's destination table is a fact of the station"

**TODO-87 — A delivery to another table: no task boundary, no pin, no pool drop** [deviation case; from T-B1a]
From the code (T-B1a, report item 10). The observed agent's task boundary fires only inside the retirement
branch of `IntentionRecognizer.update()`: a hypothesis retires when its TERMINAL action's completion holds
(`_terminal_complete`), and the retirement is a boundary when the hypothesis expected that action on the
previous tick (`_task_boundary`). A hypothesis is grounded with the station's table, so its terminal
completion is `obj_at(item, designated_table)`. If the human places the item on another table, that never
holds: the hypothesis is not pinned, no boundary fires, the belief is not re-initialised, and every origin
stays where it was. `MetaPlanner._is_complete` uses the same criterion (`AdaptivePlanner.is_complete`), so
the pool does not drop the task either. Where it matters: the deviation case (T-C / T-D), in which the
human delivers an item to a table other than its designated one; not reachable by any current fixture
(TODO-86). Recorded, nothing changed.
REPRODUCED (the play, `analysis/tc2c_scripts/play.md`; reachable since T-C2a's `deviate`): scenario_85 (env_layout8) and scenario_92
(env_layout9). No pin and no boundary at the misdelivery; after the next boundary `deliver_item(item)` leads again
(about 0.9: the item lies on the wrong table, so its delivery is still open), and the robot plans against a projected
human carrying it back, who stands still.
Files: shared/recognizer.py (`update`, `_terminal_complete`, `_task_boundary`), shared/meta_planner.py
(`_is_complete`), shared/planner.py (`is_complete`)
Reference: T-B1a, September 2026

**TODO-88 — With the prior off, an item the robot carries stays a live hypothesis about the human, with a target that moves with the robot** [recognizer finding; from T-B Q7]
Found while checking T-B Q7's acceptance, which expected a robot-side timing fix to leave every `[IR]` line
unchanged. It does not, and the two channels are the recognizer's own inputs rather than a defect of the fix.
(a) A CARRIED ITEM'S POSITION IS THE CARRIER'S (`world_state_builder`: a held object's location is its holder
and its position follows it), so while the robot carries item X the hypothesis `deliver_item(X)` is scored
against a target that moves with the ROBOT. (b) TASK COMPLETION IS A WORLD FACT, so the pin retiring
`deliver_item(X)` falls on the tick the ROBOT's release makes `obj_at(X, table)` hold. MEASURED (the 20
baseline runs, T-B Q7): with the prior ON every `[IR]` line is identical before and after the fix — the
support is the human's assigned pool and holds none of the robot's items; with it OFF, 1 to 29 `[IR]` steps
per run differ, by at most 0.165 in confidence where `most_likely` is unchanged (the moving target) and by up
to 0.497 at the pin ticks (the retirement arriving 1 to 3 ticks later). The human's own lines are
byte-identical in all 20, so nothing reaches the OBSERVATION; both channels are the WorldState.
THE POINT FOR cchat: the human cannot deliver an item the robot holds. With the prior off the live hypothesis
set therefore carries tasks the observed agent cannot perform, and their movement likelihood is measured
against a target the robot is carrying away. Whether the robot's `holding` should retire such a hypothesis,
freeze it, or leave it as it is, is an IR design question and not a bug. Recorded, nothing changed.
Files: shared/recognizer.py, mesa_sim/world_state_builder.py (held objects' positions and locations)
Reference: T-B Q7, September 2026; docs/recognizer_handback.md §1.4, §1.6; design_decisions.md, "Robot-responsible separation" (completion as a world fact)

**TODO-89 — Where within the arrival radius an approach stops decides a conflict at s, with a margin of the order of the projection's stop-point error** [observation; from T-B1c]
An observation, not a proposal. A walk to a target stops at the first point within the arrival radius (30 cm)
along its straight line, so two approaches to one table from different sides stop at different points of the
radius. Against a human standing at the table, which of them comes within min_separation (s = 50 cm) is then
decided by that stop point, and the margin can be far smaller than the difference between the projected and the
executed stop point (10 to 15 cm, step quantisation of the arrival). ILLUSTRATION, scenario_83 at step 159: the
human's projection stands at (−709.8, −221.6); the robot's item_1 carry (from shelf_1, south-west) is projected to
stop 49.22 cm from it and its item_6 carry (from shelf_6, south-east) 58.54 cm. The conflict that makes realized
cost change the head is decided by 0.78 cm against s; executed, the two stops were 37.48 and 42.87 cm from the
human. `analysis/tb1c_realized_flip/README.md`. The same subject as TODO-74 (the table is one point; the
point-place fact that co-use needs s ≤ 2r): this is its consequence for realization's verdict, not a separate
modelling question. Recorded, nothing changed.
Files: shared/projection.py (the arrival radius in a projected walk), mesa_sim/world_state_builder.py (PROXIMITY_THRESHOLD)
Reference: T-B1c, September 2026; TODO-74

**TODO-90 — Two in-window sub-min_separation approaches under gate `b2a`** [from D3] ✅ CLOSED (TODO-90 check, Sept 2026): no defect
Measured in the `task_committed` ablation (`analysis/ablation_task_committed/`), present with and without the
trigger, identical in both: s10 (both priors) 30.87 cm at ticks 72 to 74, under the B2 continue at step 29
(δ = 0); s30 prior on 15.47 cm at tick 23 (ticks 23 and 24 below 50 cm), under that tick's decision (a B2
continue that placed the 7-tick hold 23 (7)). Both lie inside the assessed window of the
decision in effect, where realization should have kept min_separation. Either a hole in realization under
`b2a` (a continue re-realizes the current task alone, and its δ = 0 is not re-checked against a later projection)
or an attribution artefact of "decision in effect" after T-B Q7 (which decision's window a tick belongs to, now
that the body spends the owed ticks). Nothing changed for it. To be checked in a bounded task before T-C: which
decision's realized plan covers those ticks, and whether that plan cleared 50 cm there.
Files: shared/meta_planner.py (B2, `realize()`), analysis/ablation_task_committed/measure.py (the window rule)
Reference: D3, September 2026; analysis/ablation_task_committed/ (142deaa); T4 (TODO-71, s10 72–75)
CHECKED (TODO-90 check, September 2026; `analysis/todo90_b2a_window/README.md`, main at 7f122fd). Neither a hole
nor, except at one tick, an attribution artefact. The robot STANDS in every sub-min_separation tick inside an
assessed window: s10 off 72–74 (decision 29) and s10 on 72–73 (decision 24; 74 on the window's edge; the decision is
at 24 under prior on, not 29 as stated above) are the robot at the table after its last step (move_to acknowledgement,
release, place acknowledgement) while the human walks in, and that decision's own realization projected them below
min_separation (47.16 / 42.89 cm; 43.10 / 42.81 cm); its closest moving approach was 67.2 / 80.5 cm. A stationary robot
segment has no violating shift interval (F1), so δ = 0 was the correct realization; executed 30.87 cm because the
human's walk stopped 14.26 cm farther along than projected (TODO-89). s30 prior on tick 24 is the robot standing in its
decided 7-tick hold as the human crosses, projected exactly (15.47 cm min over the tick, both). The one attribution
artefact is s30 tick 23 (15.47 cm): it covers [0, 1] on the decision's clock, the observation offset, before the human
projection's span, so it lies in no window; the ablation's `measure.py` tested the tick's end instant against [1, T_h]
rather than the whole tick, and omitted the realized plan's span (hence also s10 on tick 74). The ablation counted
distance inside a window; F1 makes the robot responsible for its motion only, and no robot step inside a window came
within 50 cm. Nothing changed.
CLOSED (Hadi's ruling, September 2026): the verdict above stands. The evaluation rule, corrected where it is written
(`analysis/tb3_full_reorder/README.md`, `analysis/todo90_b2a_window/README.md`; superseding note in
`analysis/ablation_task_committed/README.md`): a defect is a robot STEP (a moving tick) inside an assessed window that
ends below min_separation; standing ticks are judged by whether realization projected them (F1: the robot answers for
its own motion only). The label difference found here is TODO-91.

**TODO-91 — The executor's `[stop]` window label uses T_h alone** [label only; from TODO-90]
`Executor.set_assessed_window()` / `_log_stop()` (`mesa_sim/executor.py`, window set in `mesa_sim/sim_agents.py`)
label a tick inside when it lies in [1, T_h] on the decision's clock. The glossary ("assessed window") and
`realize()` intersect the window with the realized plan's span as well. The two differ only at the plan's tail
(scenario_10 b2a prior on, tick 74: [50, 51] straddles the realized end 50.81, inside by the label, edge by the
glossary). Label only: the stop's refusal does not read it, no behaviour depends on it. Not fixed.
Files: mesa_sim/executor.py (`set_assessed_window`, `_log_stop`), mesa_sim/sim_agents.py
Reference: TODO-90 check, September 2026; analysis/todo90_b2a_window/README.md

**TODO-92 — An observed history of the human's tasks in the robot's mind** [T-D; from T-C1]
The robot's mind keeps nothing from the human's script (T-C1), and today it keeps no record of what it has
observed of the human either: completions reach it as world facts, retractions and `unknown` episodes as
belief changes, and nothing accumulates them. Recorded for evaluation: a history, in the robot's mind, of the
human's tasks as observed — completed, dropped, `unknown` episodes. Built from what the robot observes, never
from the script. Designed in T-D. The robot taking over an abandoned task is a separate item (TODO-15).
NOTE (24 Sept 2026, the terminology ruling; `docs/glossary.md` §7): the evaluation will also need the WORLD labels
of each human behaviour, label A (assigned task or deviation) and label B (modelled or unmodelled behaviour: whether a
`HypothesisKey` of the robot's hypothesis space describes it), and the label-C check of a scenario (its declared
experimental condition against the computed coverage; a mismatch means unintended unmodelled behaviour). They are
ground truth, computable from the script (with its provenance) and the hypothesis space, and kept OUTSIDE the
robot's mind, unlike this history, which is built from observation. Not built; recorded here because the
evaluation compares the two: unexplained (the robot's finding) against unmodelled (the label).
`docs/terminology_revision.md`, sections 2 and 4.
Reference: T-C1, 23 September 2026; design_decisions.md, "The human action script (T-C1, decided)"

**TODO-93 — The completion of a foreseeable task ends the episode while an assigned delivery is visibly in progress** [T-D; from T-C2c]
Observed in scenario_11 (`analysis/tc2c_scripts/`): the human picks up item_2, walks to the coffee machine holding
it and waits there. At 75 `waited(human_0, coffee_machine_0)` pins `coffee_break`, and because that hypothesis
expected its terminal action on the previous tick, the retirement is an episode boundary: every base becomes the
uniform prior and every origin moves, although the human still holds item_2 and the delivery is in progress. The
belief falls from `deliver_item(item_2)` 0.550 to 0.248 (four-way tie) and the delivery is recognised again from
scratch (it clears θ at 100). Nothing is wrong by the current rule (docs/recognizer_handback.md §1.6: the observed
agent finished a task); whether a task completed INSIDE another, with its item in hand, should end the episode is
for T-D. Recorded, nothing changed.
REPRODUCED (the play, `analysis/tc2c_scripts/play.md`): scenario_12, scenario_41 and scenario_72, on layouts 1, 4 and 7.
Files: shared/recognizer.py (`update`, `_task_boundary`)
Reference: T-C2c, September 2026; docs/recognizer_handback.md §1.6

**TODO-94 — Re-recognition inside an episode depends on the length of the misleading walk** [T-D; from the T-C2c play]
Observed (`analysis/tc2c_scripts/play.md`). The evidence a walk lays against the hypotheses it does not serve (refutation by wasted path)
persists until an episode boundary, and only a task completion makes one: nothing else resets excess path. So a
change of mind, or a detour mid-task, is recognised again only if the misleading walk was short. Short (12–22 ticks:
scenario_51, scenario_24, the return in scenario_31, scenario_52's near corner): the task the human now does recovers,
sometimes a few ticks before its release. Long (the 77-tick walks of scenario_84 and scenario_91; the long detours
of scenario_93 and scenario_22): it never recovers, and the robot sees `unknown` (0.994) for the whole second
delivery. scenario_02's return is the same pattern (`deliver_item(item_2)` leads two ticks before its release). The
same mechanism hides a foreseeable task: in scenario_41 `coffee_break` never rose on the walk to the machine (the walk
to item_3 had refuted it), where in scenario_11 it rose to 0.345. The recognizer judges nothing; whether evidence
should decay, be reset by another event, or stand, is a recognizer question for T-D. Recorded, nothing changed.
Files: shared/recognizer.py
Reference: T-C2c play, 23 September 2026; docs/recognizer_handback.md §1.4, §1.6

**TODO-95: Stationary behaviour leaves no evidence; the robot's response to `unknown` and a stationarity channel (design task, raised at T-D Q1, 23 Sept 2026)** [OPEN]
Status: open. To be raised at the T-D recognizer pass (Q2 to Q4): rule there whether this joins
the pass or stays recorded for T-H.
TERMS (24 Sept 2026, `docs/glossary.md` §7): this entry predates the terminology ruling. Where it says "unknown
(unmodelled)", "unknown behaviour" or "assigned, foreseeable and unknown behaviour", read unmodelled behaviour (a
world label); `unknown` in code font is the residual hypothesis of the belief. The two are not the same thing: a
stand is unmodelled and leaves `unknown` unmoved. `docs/terminology_revision.md`.

Origin. While ruling T-D Q1, Hadi questioned whether projecting the human as stationary right
after a human task completion is a principled response or a device that gives the meta-planner
something to cost against. The discussion moved from the projection to the underlying question:
what the robot should reason and plan for human behaviour its models do not cover (standing
still, walking to a corner or window, leaving by the door for lunch or the WC), which it can
neither recognise as a modelled hypothesis nor project, and so has no basis for choosing a
response (continue with a hold, switch task, stop, communicate).

Observation (Hadi). A kitting worker standing in one place for 5 minutes is behaviour, not the
absence of behaviour; a human colleague would notice and interpret it. It is either
foreseeable (a break, a wait) or unknown (unmodelled), and the robot should recognise it in one
of those forms.

Current state.
- I4c Decision 4: an empty stretch is not an observation. A stationary tick contributes no
  factor to any hypothesis, and `unknown`'s likelihood applies only on ticks where some
  hypothesis was scored on an observation. The core of the decision fixed a real defect
  (TODO-59: standing scored as a perfect walk, a lone hypothesis at 1/(1+u) = 0.909 on
  nothing) and stands: standing must never confirm a movement-phase hypothesis. Its deferred
  part, stationarity as evidence in its own right, is what this TODO takes up.
- Consequence: after an episode boundary, a human who stands keeps the belief at the uniform
  prior indefinitely. `unknown` rises only from walking that wastes path against every
  hypothesis, never from standing. A stationary unknown behaviour leaves no evidence.
- Planner side: before T-D Q1, with no admitted hypothesis the meta-planner gives `realize()`
  no human projection. T-D Q1 (option 1, ruled) projects the human as standing at its observed
  position over each candidate's own span. That is the decision-time response to a standing
  human the recognizer cannot interpret; it stays valid whatever this TODO decides. T-D Q1 adds
  no trigger: a human task completion does not by itself re-decide; the projection is used only
  at decisions that fire for the existing reasons.

The limitation has two parts.
1. Recognition. `unknown` is the residual: the probability mass not explained by any modelled
   hypothesis. The residual cannot be emptied (a model of unmodelled behaviour in general is a
   contradiction). It can be narrowed by modelling more foreseeable tasks (for example leaving
   by the door at a meal time as a lunch-break schema), and the evidence feeding it can be
   improved. The present gap is narrow: stationary behaviours leave no evidence.
2. Projection and response. With no model there is no projected trajectory, but the human's
   observed position is known at every tick. The response under `unknown` is a design space
   with four levels (recorded, not decided):
   1. Decision level: cost candidates against the observed position (T-D Q1).
   2. Execution level: the blocked event, WAIT against RECONSIDER (T-D Q5).
   3. Interaction level: communicate, ask, alarm (TODO-96; no channel exists).
   4. Recognition level: give sustained standing evidential meaning (this TODO), so part of
      today's `unknown` becomes an admitted stay with its own projection.

Hadi's proposed flow, to be weighed when this is taken up: after a human task completion, do
not project and re-decide at once; give the standing time; let the recognizer raise a stay or
`unknown` from the standing; when admitted, trigger; project it as stationary as the observed
history supports; then respond (continue with a hold, switch task, stop, communicate). Notes:
under the current recognizer this sequence cannot occur (Decision 4). Even with the channel
there is a window between the boundary and the channel's θ crossing in which decisions are
taken; T-D Q1 covers that window. A waiting period before projecting would be a constant with
no source.

Design questions to rule.
1. The observation: a stand of n ticks at position p as a second observation type beside the
   stretch; where its clock starts (t = 0, a phase advance, an episode boundary); whether a
   stand folds when walking resumes.
2. Direction per hypothesis: standing confirms a hypothesis whose current phase expects
   standing (`wait_at`), disconfirms one whose phase expects motion (`MoveTo`), and is brief
   and within reach for `pick_up` / `place`. Derivable from the action type; rule whether any
   schema change is needed.
3. The likelihood form (the hard part): time is the only measure of a stand, so evidence per
   tick needs a rate, and a bare rate is a constant with no source. Candidate form: wasted
   time, symmetric to wasted path; standing beyond every hypothesis's expected stationary
   duration (task models carry them, for example `wait_at` inside `coffee_break`) is scored as
   waste, with a tolerance in the role β has for path. Requires re-deriving the
   odds-against-`unknown` invariant (docs/recognizer_handback.md §1.5) with two observation
   types, and extending the independent accumulator that verifies it.
4. TODO-59 must not return: standing never confirms a movement-phase hypothesis, and
   `unknown`'s charging follows the new grading.
5. What an admitted stay, or `unknown` read as stationary, means to the meta-planner: its
   projection (stationary by its meaning), and which response level it selects.
6. Whether a stay is a new foreseeable hypothesis (a stay schema), a reading of `unknown`, or
   both. Constraint from T-D: no hypothesis is added for a script action.

Research questions (Hadi, framework level).
- What should the robot reason and plan for human behaviour it has no prior knowledge of:
  stationary, directed to a landmark, or leaving the workspace?
- How much of the response should rest on the little that is observed (position), and what
  should it do beyond that?
- Framework purpose, as stated in CLAUDE.md (T-C1) and discussed again here: a container that
  shows IR dealing with assigned, foreseeable and unknown behaviour and a planner adapting to
  what IR reports; not a perfect simulator. Making the residual explicit and giving it a
  graded, principled response is part of the contribution.

Size, estimated at recording: comparable to I4c plus I4d; one to two design rounds and one to
two build-and-verify rounds (i4d-style invariant check with a reversion variant), all
baselines regenerated; about the size of the T-D Q2 to Q4 pass itself.
Related: TODO-59 (deferred part), TODO-85 half (a), TODO-80, TODO-92, TODO-96, T-D Q1, T-D Q5.

**TODO-96: Communication as a response under sustained `unknown` or a block (recorded, T-D Q1 discussion, 23 Sept 2026)** [OPEN, recorded only]
TERMS (24 Sept 2026, `docs/glossary.md` §7): "unknown behaviour" below means unmodelled behaviour; "sustained
`unknown`" is the belief's residual mass, which is not the same condition.
Status: open, recorded only. Hadi: under unknown behaviour the robot may stop and communicate
(ask the human what is happening, raise an alarm) instead of, or after, re-planning. No
communication channel exists in the framework. Level 3 of the response structure in TODO-95.
Its condition (sustained `unknown`, or a blocked event WAIT and RECONSIDER do not resolve)
must be defensible without a constant taken from a scenario. To be argued at T-D Q5 or after;
not part of T-D Q1.

**TODO-97: Belief-aware planning: a joint realization against the hypotheses that cover the belief (recorded, 24 Sept 2026)** [OPEN, recorded only; later, after the T-D Q2 to Q4 recognizer pass]
Status: open, recorded only. Not on the T-D agenda, not in the handoff order.

Claim it would support: robustness to intention AMBIGUITY, two or more live hypotheses sharing the
mass and none clearing θ. Not robustness to intention uncertainty in general: a confident wrong
belief (T-D Q4) and unmodelled behaviour (`unknown`) are untouched by it.
TERMS (24 Sept 2026, `docs/glossary.md` §7): "unmodelled behaviour (`unknown`)" pairs a world label with the belief's
residual hypothesis; they diverge (a stand is unmodelled with `unknown` unmoved; a finished work order has `unknown`
high by normalisation). `docs/terminology_revision.md`, section 3.

Mechanism, one candidate, not decided.
- The covering set S_ε: the smallest set of hypotheses holding at least 1 − ε of the belief mass.
- One realization per candidate against all projections in S_ε JOINTLY: a joint-realization
  criterion, not a criterion over per-hypothesis costs (that is TODO-84's expected realized cost,
  a different comparison).
- `unknown` in S_ε projects the T-D Q1 stationary object.
- The guarantee is stated in belief mass, never as a probability of safety.

Equivalence. Above the gate it equals today's mechanism with ε = 1 − θ. The two differ only below
θ: today the T-D Q1 stationary projection, here the union of the projections in S_ε.

Constants that remain: ε, and the condition that redefines `recognition_changed` as "S_ε changed".
Both reopen DESIGN-07 and D3, and are argued at that time.

Precondition: hypotheses affect the robot only through interference. Shared-resource conflicts,
or the robot taking over an abandoned task (TODO-15), would need more than realized duration.

Gate on doing it: after the Q2 to Q4 pass, measure on the existing fixtures, on the decision ticks
at which the leading share is below θ, the count of those at which the smallest set of task
hypotheses (`unknown` excluded) whose mass reaches θ has two or more members. That is the covering
set at ε = 1 − θ, the mechanism's own definition: no new constant. Report the count and, beside it,
the distribution of the second-leading share on those ticks. A small count closes this TODO.

Evaluation, if opened: one shared-corridor ambiguity fixture and one conservatism fixture, a
comparison table in the T-B3 style.

Nothing in T-D Q1's build is shaped for it. Sub-ruling 4c of Q1 (`realize()` not special-cased, the
projection passed through `update_human_projection()`) is the only seam it needs.
Related: TODO-84, TODO-95, TODO-15, DESIGN-07, D3; design_decisions.md, "Belief-aware planning".

**T-D OPENING AGENDA, from the T-C2c play** (`analysis/tc2c_scripts/play.md`; recorded 23 September 2026)
1. The robot is blind after every human task completion: TODO-85 (b), its general form (scenario_72, 0.78 cm).
2. Re-recognition inside an episode depends on the length of the misleading walk: TODO-94.
3. Reproduced: TODO-93 (a foreseeable completion ends the episode mid-delivery) and TODO-87 (a delivery to another
   table: no pin, no boundary, a projection of a task the human will not do).
4. T-D's blocked fixture uses a stay that ends (TODO-80; the scenario-authoring convention).
5. At the recognizer pass (T-D Q2 to Q4): raise TODO-95 (stationarity channel) and rule whether it joins the pass or
   stays recorded for T-H.
