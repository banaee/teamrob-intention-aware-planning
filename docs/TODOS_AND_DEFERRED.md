# TeamRob Framework — TODOs, Bugs, and Deferred Items

Deleted 5 October 2026 (T-F part 1's close, part E; analysis/README.md): the frozen analyses td_stage1, td_stage1b, l_build, irb2b_exposed_interval (tb2b_exposed_interval before 3 October), ablation_task_committed, f47_fixtures, t1_conflict_measurement, todo90_b2a_window, tc2c_scripts, tb1d_designations, tb2c_per_entry_holds and big_picture under analysis/kitting/ (analysis/ before the sort); the runs and run files of T-K part 1's steps 5 and 5b (planning) and 5e and of T-F part 1's stage 2 check (configs/kitting/mpb/tk, mpb/tk5b, tk5e, tf1/check; their READMEs and reports stay). A path cited below under these names is held by commit 362af19 (`git checkout 362af19 -- <path>`).

Collected from Phase 2.1 (dock_loading domain), 2.2 (visualization), and Phase 4 design sessions.
Each item has a category, priority, and the relevant file(s).
Items marked **[BLOCKING]** must be resolved before the simulation runs correctly end-to-end.

> **Terms:** `docs/glossary.md` gives each term one meaning. The entries below are the HISTORICAL
> RECORD and are left exactly as they were written, so some of them use a term differently from the
> glossary (the conflicts are listed in the glossary task's report). Read an entry in the terms of
> its own date; write new text in the glossary's.
>
> **Terms for human behaviour, model coverage and the robot's inference (superseding note, 24 Sept 2026;
> `docs/glossary.md` §7, `docs/terminology_revision.md`).** Entries written before that ruling use these
> phrases; read them as follows (WORLD terms describe the human, ROBOT terms the robot's mind):
> - "unknown behaviour", "a stationary unknown behaviour", "unknown (unmodelled)", "assigned, foreseeable and
>   unknown behaviour" (TODO-95, TODO-96) → unmodelled behaviour (WORLD). Assigned / foreseeable / unknown are
>   not three categories of intention: label A (assigned task / deviation) and label B (modelled / unmodelled)
>   are independent, and a foreseeable task is a deviation that is modelled.
> - "unmodelled behaviour (`unknown`)" (TODO-97) → unmodelled behaviour (WORLD); `unknown` is the residual
>   hypothesis (ROBOT), and the two diverge.
> - "the hypothesis space is exhausted" (TODO-85) → no task hypothesis is left live ("exhausted" is not a term).
> - "a finished work order and unmodelled behaviour are indistinguishable to `update()`" (TODO-85) → the idle
>   stand after a finished work order IS unmodelled (label A has no value then); what `update()` cannot tell apart
>   is `unknown` high by normalisation (nothing unexplained) from `unknown` raised by evidence (unexplained).
> - "Foreseeable tasks are recognised (… crosses θ)" (TODO-32 update), "a task has just become recognised"
>   (TODO-68), "one recognised task" (TODO-69), "the robot recognises it" (TODO-80), "recognised again" (TODO-93,
>   TODO-94) → the task's hypothesis clears θ / is admitted (ROBOT).
> - "a task the robot cannot recognise" (TODO-49) → a task no hypothesis describes: unmodelled behaviour (WORLD).
> - "exercised only past T_h and by deviations" (TODO-47 (e)), "(the human deviated; …)" (TODO-71) → by the
>   human's departures from its projection. "Deviation" means a departure from the work order only (label A).
> - "declared human behaviour outside the robot's domain knowledge", "an unforeseen stay", "human behaviour the
>   ROBOT'S knowledge does not cover" (TODO-80, TODO-47 (e)) → declared unmodelled behaviour: a scenario's
>   purpose (label C) whose behaviour is unmodelled (label B).
>
> **T-H: the human behaviour model (superseding note, 25 Sept 2026; design_decisions.md, the entry of that name;
> `docs/glossary.md` §6, §7).**
> - "work order" → the assigned tasks.
> - "deviation" (label A, any departure from the work order) → since T-H a node of the human's realised plan tree
>   that the robot's tree does not contain; labels A and B are queries on the executor's record (TODO-92 → T-H4).
> - "T-H" as the recognizer's duration term for a stay (TODO-85 (a), TODO-95, the T-D opening agenda item 5) → that
>   item is TODO-95; T-H now names the human behaviour model.
> - `Stay`, `MoveTo`, `interrupt` / `deviate` / `abandon`, provenance, `check_work_order`: T-C1's vocabulary, deleted
>   in T-H3 (`stand(n)`, `go_to`, events with `at` / `drop`, plain instances).
>
> **Tags [V1] / [FW] (T-G A1, ruled by Hadi, 1 Oct 2026; design_decisions.md, "T-G: the second domain's rulings", A1).** An open item may carry
> a tag beside its status: [V1] (inside the first complete version) or [FW] (future work: conceptual directions only).
> An untagged item is not yet ruled. No full pass: an item is tagged when next touched by Hadi's ruling, a new item
> when recorded. Numbers and identifiers are kept for good: no renumbering, no renaming.

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
T-G (T-G records 1, 1 Oct 2026): the gate becomes a state declared in the setup and opened on request (B5), passed by a plain step to the
gate's centre (B11); design_decisions.md, "T-G: the second domain's rulings", B5, B11. The guard's predicate is emitted today (TODO-02's note).
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

**TODO-02 — `world_state_builder`: emit `gate_is_open(dock_gate)` unconditionally** ⛔ SUPERSEDED (T-G A5, B5)
SUPERSEDED (T-G records 1, 1 Oct 2026): built as an emission for every object of type `gate` whose `is_open` is not False (never loaded,
so always); the gate is a state declared in the setup, held by the environment, with no simulator code for one domain
(A5, B5). design_decisions.md, "T-G: the second domain's rulings", A5, B5.
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
Files: `domains/kitting/layouts/env_layout_KK.json`, `domains/dock_loading/layouts/env_layout_01.json`, `mesa_sim/sim_model.py`
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
STALE PREDICATE in the successor state (`obj_at(item_6, shelf_6)` after item_6's delivery, scenario_s06_01; the
only predicate on the robot or the item that the successor holds and the real world does not), READ BY
NOTHING TODAY: guards read `holding`, and target resolution reads the maps, which the relocation keeps right.
IT MUST BE RESOLVED BEFORE ANY CONSUMER READS `obj_at` FOR AN ITEM THAT HAS BEEN PICKED UP in a successor
state. The same form problem, also read by nothing: `move_to` does not end the previous `at(agent, ·)`, and
`waited` is ended by a later action of another kind.
Files: `shared/planner.py`, `shared/types.py` (ConditionSchema), `shared/meta_planner.py`
Reference: Phase 4B; Phase 4C meta_planner build session, September 2026

**TODO-08 — `dock_gate` open/close: implement `open_gate` ActionSchema** ⛔ SUPERSEDED for the gate (T-G B5)
SUPERSEDED (T-G records 1, 1 Oct 2026): the gate is open or closed, declared in the setup; the robot moves to the closed gate and honks
(an action that sets "opening requested"); the human's assigned task "open the gate" presses the button; no action
closes it in V1; the robot never opens it itself (B5). The commented `gate_closed` methods are not the form: a method per
starting area, the gate's condition on a method that crosses it (B11). Stage 2 (C1). design_decisions.md, "T-G: the second domain's rulings", B5, B11.
`deliver_pallet` and `load_return` have a commented-out `gate_closed` method.
Implement `open_gate` action schemas and wire the second method when gate state
is modeled dynamically.
Files: `domains/dock_loading/ActionSchemas.py`, `domains/dock_loading/tasks.py`
Reference: TODO in tasks.py comments

**TODO-09 — Path planning: replace straight-line STEP* with obstacle-aware planning**
T-G (T-G records 1, 1 Oct 2026): within V1, dock_loading's answer is B11: passing the gate is a plain step "move to the gate", one method
per starting area; routing through openings as a property of movement was not taken (it changes the projection and
the recognizer in `shared/`). This item itself is not tagged. design_decisions.md, "T-G: the second domain's rulings", B11.
Currently `action_decomposer.steps_toward()` uses straight-line interpolation.
Agents walk through walls and obstacles. Replace with A* or RRT in Phase 4.
See DESIGN-13 for the broader plan: this becomes Mesa's use of the common
non-committed path-realization estimator, not a Mesa-only fix.
Files: `mesa_sim/action_decomposer.py`
Reference: Phase 4D

**TODO-10 — `scan_pallet` precondition: `obj_at(?item, delivery_area)` guard**
ANSWERED, NOT BUILT (T-G records 1, 1 Oct 2026): `confirm_delivered_pallet` (was `scan_pallet`) states its condition in the task model, the
pallet in its delivery container (B2); the human takes it only when it is applicable (A3), by its own planning in
`world/`, not in the `shared/` cognitive loop. design_decisions.md, "T-G: the second domain's rulings", A3, B2.
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

**TODO-16 — Cost-aware method selection in `_select_method`** [V1] [RULED (T-G A7, 1 Oct 2026); its design question open]
RULED (T-G A7, Hadi, 1 Oct 2026; design_decisions.md, "T-G: the second domain's rulings", A7): inside T-G stage 2, after the MPB's first run on dock_loading.
When two or more methods of a task apply in the same world state, the robot chooses by realized cost; the
meta-planner's candidates become pairs of task and method. Its case in dock_loading: a delivery in one cycle (truck to
bay) against a stepwise delivery (truck to gate, then gate to bay). It changes `shared/`; Hadi's ruling is the design
ground. Its own design question comes before any build: how the candidates are formed; whether the recognizer also
considers several applicable methods. Acceptance on kitting: no decision changes. The fix as filed below (a cost
estimator passed into `_select_method`) is not the ruled form: the choice is the meta-planner's, on realized cost.
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
Observed in a manual test run (scenario_s01_01, item_6-carrying seed for deliver_with_return
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

**TODO-25 — dock_loading typed-parameter integration: not reviewed** [deferred] [V1]
CORRECTED (T-G records 1, 1 Oct 2026): the error below is raised at model construction (`RobotAgent.observe_initial()`, in
`SimModel.__init__`), not "on the first tick", once TODO-104's errors are past. T-G build 1 (30 Sept 2026, 56e674e)
typed `confirm_delivered_pallet` (`?pallet: pallet`) and keyed the steps of `pick_up`, `place`, `scan_it` on `?item`:
the error is gone and scenario_s01_03 loads. Left: `wait_at` still completes on `ProcessCompletion` (the `waited`
migration), and scenario_s01_02 binds `?delivery_bay` on `confirm_delivered_pallet`, which the schema does not declare
(the replay stops at `office_break` before it is read). "NEUTRAL" below is the perfect-fit value L = 1 since I4 (the I2
entry's note); T-G A4 replaces that scoring when built. Stage 1 (C3). design_decisions.md, "T-G: the second domain's rulings", C2, C3.
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
T-G (Hadi's order, 30 September 2026): its schema fixes are part of T-G, the second domain in Mesa (roadmap, "The plan
from T-A", T-G).
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
NOTE (T-G Q12 to Q15, Hadi, 1 Oct 2026): the lifecycle of an entry of the human's list is ruled (open and closed
entries, the repeatable standby entry, the closing part, the dependence declaration for the load-time check).
design_decisions.md, "T-G: the second domain's rulings", A3 (RULED).
ANSWERED, NOT BUILT (T-G A3, T-G records 1, 1 Oct 2026): a task can start only when it is applicable (one of its methods applies), decided by
the human agent's own HTN planning against the true state it perceives; the script is a priority list scanned from the
top whenever the human is free; if nothing is applicable the human waits. In `world/` (the human's executor), not a
`TaskSchema.entry_conditions` field read in `shared/`. design_decisions.md, "T-G: the second domain's rulings", A3.
Human tasks in `scenarios.py` are a flat queue executed sequentially regardless of
world state. The proper mechanism: `TaskSchema.entry_conditions: List[ConditionSchema]`
checked against `WorldState` before task dequeue. If unsatisfied, agent idles.
This is simulator-agnostic (uses WorldState predicates only) and lives in `shared/`.
Both Mesa and ROS would benefit. Needs dedicated design session.
Files: `shared/types.py`, `shared/` cognitive loop, `mesa_sim/sim_agents.py`
Reference: TODO #17

**DESIGN-02 — Existential parameter binding in planner**
NOT TAKEN (T-G A3, T-G records 1, 1 Oct 2026): a generic task whose object is bound at run time removes the allocation the assignment prior
relies on. design_decisions.md, "T-G: the second domain's rulings", A3.
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
ANSWERED, NOT BUILT (T-G records 1, 1 Oct 2026): (a) is taken: applicability (A3) with the scan's condition (B2). Shared work between the
two agents is an FW direction (TODO-147). design_decisions.md, "T-G: the second domain's rulings", A3, B2, A10.
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
ANSWERED (T-G records 1, 1 Oct 2026): 1. T-G build 1 typed the layout's object `office_chair` (56e674e). 2. The office door is open or closed,
declared in the setup; the agent that passes it opens it, one method for the open state and one that opens first (B5).
3. `office_break` ends at its chair with a wait, the chair inside the office (B6). design_decisions.md, "T-G: the second domain's rulings", B5, B6.
Task renamed from `go_to_office` to `office_break` (dock_loading). Three open
questions before this task is reliable:
1. `parameter_types={"?office_chair": "office_chair"}` doesn't match the
   office_chair object's actual "type": "chair" in env_layout_01.json — one
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
scenario_s01_01 — nothing was ever excluded, closest observed approach was ~2.9 — so the
infeasibility branch is effectively untested (see TODO-30). A too-large value would exclude
every candidate; a too-small one makes interference detection inert.
Needs a calibration pass against real layout geometry, ideally alongside `default_action_cost`.
Files: shared/projection.py (init — assumed_speed, default_action_cost), shared/meta_planner.py (init — min_safe_distance)
Reference: Phase 4C scenario_s01_01 validation, September 2026

Calibration order (fixture-design session): calibrate only after the meta_planner's
confidence-gated human projection lands. Under today's ungated projection,
min_safe_distance=50 would exclude scenario_s03_01's item_4 at t=0 against a 0.167 tie-break
projection (min_dist 20) — an exclusion, but not a legitimate one.

Update (evidence-gated projection admission session): the gate has landed; calibration is
unblocked. Findings from scenario_s03_01, 200 steps, PYTHONHASHSEED=0, runs 20260910_144814
(switch off) and 20260910_144816 (switch on):
- scenario_s03_01 now has two valid fixture conditions. Switch ON is the mid-approach-reveal
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
reads in ticks (scenario_s03_01 t=0: 54 / 71 / 103, formerly 1032 / 1372 / 2028). The T1 evidence
above and in `analysis/t1_conflict_measurement/REPORT.md` is in world units and unchanged.
Consequence: with placement lasting a real tick, both agents' placement segments sit at the
identical table position in overlapping ticks whenever the arrival gap is under a tick, so
`min_dist` reaches exactly 0.0 and `min_safe_distance = 1.0` now EXCLUDES those candidates
(TODO-30 is exercised; scenario_s02_01 step 257 hits the every-candidate-excluded `RuntimeError`).
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
Reference: Phase 4C scenario_s01_01 validation, September 2026

**TODO-30 — Interference exclusion branch never exercised** — MEANING CHANGED (wait-decision revision, Sept 2026): "infeasible" = no realization within the human's horizon — ✅ RESOLVED by decision (R1, Sept 2026): all-unrealizable → plain projected cost, logged `all_unrealizable` — ✅ BUILT (T10): the `RuntimeError` is gone; one event measured — ✅ CLOSED (F1): realization is total, the branch no longer exists — ✅ CLOSED (F1: nothing is unrealizable)
NOTE (T-G records 7, 1 Oct 2026): design_decisions.md, "T-G: the second domain's rulings", C4 cited this item for "how
the meta-planner behaves when the pool holds tasks and none is applicable"; the citation is corrected. This item concerns
realizability and stays closed; applicability is TODO-152.
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
(scenario_s01_01: everything done by step 147).
Harmless, but wasteful and makes log tails uninformative. Fix belongs in the run loop
(`run_mesa.py` / `SimModel.step()`), not in the agents.
NOTE (IRB.1r, 27 Sept 2026): the cognitive-loop ruling (design_decisions.md, "The cognitive loop does not end with the task pool") does not touch this item.
HADI'S IDEA, NOT DECIDED (Hadi, 6 October 2026, at the plan of T-viz 1a): every start stops when no agent has anything
left scheduled or scripted. The web-ui of 1a only pauses play at that point and goes on when asked (design_records.md,
"T-viz, the web-ui", 1a, HADI'S ANSWERS ON THE PLAN, item 6). Three facts recorded with the idea:
- The maintained baseline logs run past that point, so a stop there would change them. Measured by ccode (6 October
  2026, the 48 logs on disk of the four maintained sets; the point as MPB-5 names it, the robot's `[meta] ... all tasks
  complete` line and the human's last tick with a non-empty stack in the `.rec`): 46 of 48 run past it, by 5 to 116
  ticks. The two of scenario_s02_01 (450 steps, prior off and on) end at tick 449 with the human 86 of 91 ticks into the
  closing walk to corner_SE, five ticks before the point; a stop there would leave them unchanged.
- Some sim-runs never reach the point: a stand to the run's end, or a script that depends on the robot with an entry
  that never becomes applicable (TODO-184). So headless keeps its step limit.
- The robot's recognition continues after its pool is empty (the cognitive-loop ruling above), and the test-beds read a
  margin after the point (MPB-5's 30 ticks, from the IRB's E5).
Files: mesa_sim/run_mesa.py, mesa_sim/sim_model.py
Reference: Phase 4C scenario_s01_01 validation, September 2026

**TODO-34 — Pre-existing `obs` fragility in `RobotAgent.step()` logging**
The IR logging block guards on `self.belief is not None and human is not None`, then reads
`obs.timestamp`. But `obs` is only bound when *this step's* `build_observation()` returned
non-None, while `self.belief` persists across steps. If `human is not None` and
`build_observation()` returns `None` on a step where a belief already exists, `obs` is either
stale or unbound — `AttributeError`/`UnboundLocalError`.
Not introduced by the MetaPlanner migration; pre-existing, spotted while editing the
surrounding block. Not observed firing in scenario_s01_01.
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
SUPERSEDED IN PART (T-D R, 27 September 2026): the separation "under the grade" (the title; the odds ratio u^{−x (1/d_near − 1/d_far)}): the grade leaves the belief (R1). design_decisions.md, "T-D R and E".
SUPERSEDED IN PART (T-D R1, 27 September 2026): reason superseded by R1 (the grade leaves the belief). Not reopened. design_decisions.md, "T-D R and E".
Heading restated (graded-evidence session, September 2026). The "direction-only likelihood" below is the
cosine kernel, gone since I4; the excess-path likelihood also cannot separate targets on one bearing
(both at zero excess for the whole walk; handback §3.3, §4 (a)) — until the grade: two collinear targets at
distances d_near < d_far now separate DURING the walk, since the nearer target's covered fraction grows
faster (odds ratio u^{−x (1/d_near − 1/d_far)} after x walked). That is option (a) below in effect, with
its risk: a decoy on the true bearing BEFORE the target gains mid-walk, not only at its arrival fold. No
fixture has such a decoy; the collinear decoys in scenario_s03_01 lie BEHIND the true target, and s20_off's first
reveal stays at the arrival (20). Options (b)–(d) are as written; nothing decided.
Observed: scenario_s03_01 (run_20260910_083630). shelf_6 lies nearly behind the human's target
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

Update (fixture-design session): scenario_s03_01 no longer depends on this — its early reveal is
planned via assignment_prior on plus a confidence-gated human projection (meta_planner,
pending). Decide TODO-38 on IR-quality grounds only.

Update (evidence-gated projection admission session): first MEASURED instance of
"confidence ≠ correctness" — previously only a noted risk. scenario_s02_01, assignment_prior on,
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

**TODO-39 — Migrate `domains/dock_loading/scenarios.py` to `assigned_tasks`** [V1]
`AgentConfig.assigned_tasks` was added and all three kitting scenarios migrated; dock_loading
still declares only `scheduled_tasks` for both agent types. It imports and loads fine — empty
`assigned_tasks` skips `__post_init__` validation by design — but `SimModel._spawn_agents()`
already seeds robots from `assigned_tasks`, so a dock_loading robot gets an **empty task pool
today**: a dock_loading run has an idle robot right now, with no exception raised. Migrate
before running dock_loading again: humans get `assigned_tasks` = their non-foreseeable
`scheduled_tasks`; robots get `assigned_tasks=` in place of `scheduled_tasks=`.
T-G build 1 (30 Sept 2026): the robots' tasks of scenario_s01_01 and _02 moved to `assigned_tasks`; their humans'
assigned tasks are left to T-G's design (TODO-104); the new scenario_s01_03 states both agents' assigned tasks.
THE HUMAN'S SIDE (T-G records 1, 1 Oct 2026): scenario_s01_01 and _02 declare no assigned tasks for the human, so with the prior on no
scan hypothesis is admissible. Ruled (B1): the human's assigned scans follow from the robot's assigned deliveries and
are known at load. The two scenarios are replaced in stage 1 (B10, C3). design_decisions.md, "T-G: the second domain's rulings", B1.
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
T-H1 (25 Sept 2026): `DomainModel.intentions` and `get_all_intentions()` are removed; `build_hypothesis_space`
iterates `TaskModel.task_schemas()` (shared/knowledge.py, `ProceduralKnowledge`), which is in declaration order, so
this source of order is gone; the recognizer's sort by key stays.
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
FLAGGED AGAIN (T-K part 1, Hadi, 2 Oct 2026; design_decisions.md, "T-K: context knowledge in the
recognizer's belief", NAMES FLAGGED): with the context weight (ω_context) and the prior base, for renaming at T-K part
1's build, not now. R3 gives the robot a prior made of declared strengths, so the switch's name now collides with a
term of its own (glossary §5, **prior**).
RULED (AM9, Hadi, 3 Oct 2026; design_decisions.md, "T-K: context knowledge in the recognizer's belief", NAMES FLAGGED, AM9): the name is `assignment_knowledge`, beside the new
option `context_knowledge`; each is on or off and states what the robot knows. Reason: the option says only whether
the robot is told which tasks the human was assigned, and that knowledge restricts the support and sets no prior. The
rename (code, configuration, commands; the `[IR-prior]` tag and the `[run]` header's field with them) belongs to T-K part
1's build, with the regression audit; older records keep the old name.
CORRECTED (C4, Hadi, 3 Oct 2026): "restricts the support and sets no prior" reads "restricts the support and sets no
weight". Under AM3 the option decides which hypotheses work as a whole contains, so it shapes the prior through the
support.
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
✅ CLOSED by R1 (T-D R, 27 September 2026): a singleton admissible set reads 1.0 by normalisation over the live hypothesis set (R1), so the projection this idea asked for is admitted without it; the guard against admitting on no evidence is now the adequacy finding, under G. design_decisions.md, "T-D R and E".
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
    for env_layout_08 (e76e4e0) and removed again in the same task. Reason: fixtures are read by people, so
    they are written as literals. A fixture that cannot be read in `scenarios.py` cannot be checked by a
    person, and that outweighs saving the three manual edits. scenario_s06_01 / scenario_s06_02 are literals in
    `scenarios.py`, registered the ordinary way; `env_layout_08.json` is an ordinary committed layout. The
    generator only reproduced what the literals state, so it was deleted rather than kept to drift. Whether
    the randomised harness (T-F) needs programmatic registration is left to its design; nothing is kept
    here for it.
    DISTINCTION (T-L, 26 September 2026): what was reversed is a generator that PRODUCED fixtures, not a
    mechanism that LISTS them. T-L registers hand-written `ScenarioConfig` literals by discovery at import of the
    domain package (no side effect beyond adding to a dict; a duplicate id is an error), and layouts and setups by
    their files; the fixtures stay literals, read by people. design_decisions.md, "Layouts, setups and scenarios:
    the three artefacts of a run", ruling 5.
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
    ✅ BUILT (F47, retyped F47b, September 2026): `scenario_s03_06` on `env_layout_06` (= env_layout_03 + a
    coffee machine 500 cm east of the table; a waypoint `rest_0` until F47b, an ill-typed binding):
    scenario_s03_01 with a third human task, `coffee_break(coffee_machine_0)`, after its last delivery.
    Stop on: completes at 237 / 239 (prior off / on) where scenario_s03_01 is refused at the table from 144
    to the cap. The machine makes `coffee_break` a live hypothesis from t=0, so the recognizer's set
    differs from scenario_s03_01's: prior-on the first crossing and the hold move from 6 to 8. Read with
    scenario_s03_01, not instead of it. `analysis/f47_fixtures/`.
    STILL OPEN FOR env_layout_09 (T-B1b follow-up, September 2026): if env_layout_09 ever becomes a measured
    fixture, its end state needs handling first. In scenario_s07_01 the sampled separation is below
    `min_separation` (50 cm) from tick 358 to the end of a 500-step run — after the robot's last delivery
    at 361 — with both agents standing idle near kitting_table_1, which is where the human finished and
    where three of the robot's four deliveries go. Nothing during the work falls below it. The same
    end-state condition (d) is about, on a layout that has no variant for it yet.
(e) FIXTURES FOR D2 (F47 / F47b, September 2026): the condition on which D2's blocked-execution event and
    its reaction policy (wait, or reconsider and return) would differ is a human stay at a place the robot
    needs, mid-run, finite, with another task in the pool. F47 produced it with `coffee_break` bound to a
    waypoint — ill-typed (no coffee machine), retired in F47b (`analysis/f47_fixtures/`). F47b built the
    natural, well-typed configuration: `env_layout_07`, `scenario_s05_01` / `scenario_s05_02` — a real coffee machine on the
    robot's route to its first shelf, the human's shelf beside it, the human's break there, then its
    delivery, then the AC switch by the east wall; the alternative shelf beside the blocked one or across
    the table at the same distance (the F47 one-variable design). MEASURED: `coffee_break` crosses θ at
    tick 23, two ticks before the stand (25–55), and realization absorbs the projected wait — scenario_s05_01
    switches to the alternative (no `[stop]`, done 187), scenario_s05_02 holds 32 ticks and then meets only the
    human's departure (3 refused steps at 57–59 past T_h, done 207). NO VALID FIXTURE PRODUCES A MID-RUN
    BLOCK: a stay the projection carries is priced, so the blocked event is exercised only past T_h and by
    deviations (design_decisions.md, "Scheduled bindings are typed; a stay the projection carries is
    absorbed"). The short / long variants therefore have no valid instance; what varies between 70 and 71 is
    the planning response (switch vs hold). A principled unforeseen stay needs declared human behaviour
    outside the robot's domain knowledge (TODO-80). D2's evaluation uses scenario_s03_01 / scenario_s03_06 (the
    end-state pair, the tail block) and scenario_s05_01 / scenario_s05_02 (the absorbed stay, the departure tail).
(f-designations) A DESIGN NOTE FOR ANY SCENARIO WITH MORE THAN ONE DESTINATION (T-B1b follow-up, September
    2026): in the current two-table scenarios most items are designated to the table NEAREST their shelf —
    5 of 6 in env_layout_08 and 5 of 6 in env_layout_09 (measured). That makes the destination fact nearly
    redundant with geometry: it weakens the ordering difference the fixture is for, and it weakens the
    recognizer's discrimination on the carry leg, since the table a carry heads for is the one proximity
    would have guessed. In both layouts the whole ordering effect rests on the single against-proximity
    item (env_layout_08's item_4, farther by 64.9 ticks; env_layout_09's item_1, by 26.8). Scenarios built to
    EVALUATE the algorithms must set designations deliberately, against proximity where that is what the
    test needs. The designations are Hadi's to decide per scenario, not to be left to follow from the
    layout. design_decisions.md, "An item's destination table is a fact of the station" (the fact is the
    station's; which station is a design choice).
    WHAT THIS SCOPES T-B3a TO (T-B1d, September 2026; supersedes the paragraph below). single_task takes the
    cheapest task from the robot's position; full_reorder takes the task whose delivery leaves the robot best
    placed for the remaining shelves; the two heads differ exactly when the cheapest-from-here task ends at a
    table far from the remaining shelves, which the destination fact decides. Across nine designation sets
    priced on env_layout_08's geometry the heads differ in seven (gaps 14 to 78 ticks) and coincide in two;
    every flip traces to the one designation that moves the cheapest single task — the mechanism, not a
    weakness of any fixture. Generality across layouts is T-F's (randomised layouts), not a hand-built
    scenario's. `analysis/tb1d_designations/README.md`.
    SUPERSEDED (T-B1d): T-B's ordering result rests on a SINGLE against-proximity item in each
    layout (item_4 in env_layout_08, item_1 in env_layout_09), so any claim drawn from T-B3a is scoped to that
    fixture: it shows that ordering matters WHEN AN ITEM IS DESIGNATED AWAY FROM ITS NEAREST TABLE, not
    that reordering helps in general on a two-table station. An evaluation scenario meant to support the
    general claim needs SEVERAL against-proximity designations, or a geometry in which proximity does not
    order the tables cleanly. `analysis/tb1b_two_tables/README.md`, "What this fixture does not settle".
    A FINDING FOR T-B3, FROM T-B2c (September 2026): on every current fixture NO WINNING ORDERING UNDER `full_reorder` CARRIES A HOLD (scenario_s06_01, scenario_s06_02,
    scenario_s01_01, both priors; every hold sent is 0 and every `[meta-win]` line reads `holds=0,...`), so T-B2c
    changes NOTHING EXECUTED against T-B2b. scenario_s06_02 does not exercise realized cost under `full_reorder`: its
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
    ✅ BUILT (T-B1b, September 2026): `env_layout_08`, `scenario_s06_01` (plain cost, ordering isolated) and
    `scenario_s06_02` (a conflict in the second task of an ordering). Robot pool item_1 / 6 / 4 to
    kitting_table_0, item_7 to kitting_table_1: the cheapest single task from the start is item_6
    (39.3 ticks), the cheapest full ordering starts with item_7, and greedy is 41.4 ticks worse. The
    fixture settles the choice of head, not the tail (the two best orderings differ by 2.2 ticks). The
    permutation table, the runs and the baselines: `analysis/tb1b_two_tables/README.md`.
    ✅ T-B1c (September 2026): `scenario_s06_03` exists as the existence case in which realized cost changes the
    head under `full_reorder`; `analysis/tb1c_realized_flip/`. `scenario_s06_05` (several against-proximity
    designations) is T-B1d, not started.
(g) THE GATE'S REOPENING CONDITION (gate ruling, September 2026): a walk crossing of θ with a live rival at
    similar odds (top-two ratio near 1 at the crossing), where the normalised share and a margin gate would
    disagree. No current fixture shows one (lowest top-two ratio at a walk crossing 5.23, s00_off 37).
    Report it where the generated fixtures produce it (the crossing tick, top odds against `unknown`, the
    ratio of the top two, the live set, as in `analysis/g1_graded_evidence/crossings.md`); do not build a
    fixture for it. TODO-64 / 65, design_decisions.md, "The gate stays a fixed share".
    SUPERSEDED IN PART (T-D R1, 27 September 2026): the `unknown` route no longer exists; its replacement is G. Not closed: the downstream response is G and X. design_decisions.md, "T-D R and E".
(c) Fixture gap (T1, `analysis/t1_conflict_measurement/REPORT.md` §(a), §(c)): no current
    scenario has a correct-hypothesis *crossing* on the robot's current task. The only
    correct-hypothesis crossings measured are the never-selected item_7 alternatives in
    scenario_s03_01 (robot approach across the human's carry path); every conflict on a current
    task is co-directional convergence into the kitting table. B2 continuation will therefore
    only be exercised on table convergence until a crossing fixture exists.
Also: B2.B+B3.A must select identically to none+B3.A under the same `_cost()` — treat as an
assertion in the harness; any divergence is a bug. Only projection count may differ.
Files: domains/kitting/registry.py, domains/kitting/scenarios.py, mesa_sim/run_mesa.py,
shared/meta_planner.py
Reference: Phase 4C B2/B3 session, September 2026

**TODO-48 — Hypothesis change above θ fires no trigger** ✅ CLOSED (D2, September 2026)
SUPERSEDED IN PART (T-D R1, 27 September 2026): the `unknown` route no longer exists; its replacement is G. Not closed: the downstream response is G and X. design_decisions.md, "T-D R and E".
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
lacks the object (scenario_s01_01 / scenario_s03_01 / scenario_s01_06 have no coffee machine — DESIGN-14), a silent modelling error
when it is a spelling mismatch: `env_layout_02.json` declared `AC_switch` against
`parameter_types` `ac_switch`, so scenario_s02_01's scripted `ac_activation` was unrecognisable
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
assigned tasks; a mismatch raises (an error, not a warning). Result over the registered fixtures: scenario_s04_01
(`ac_activation` at the waypoints wander_0 / wander_1) and scenario_s03_06 as first built (`coffee_break` at the
waypoint rest_0) failed and were fixed by retyping the targets at the same coordinates (env_layout_05:
`ac_switch_1` / `ac_switch_2`; env_layout_06: `coffee_machine_0`); scenario_60/61 failed and were retired
(`analysis/f47_fixtures/`). STILL PROPOSED: (1) the `[IR-space]` line; (3) the case-insensitive type clash at
hypothesis-space construction; and the other half of (2), "every scripted task's key is in the hypothesis
space" — the type check implies it whenever the type has objects, but a scripted task whose parameter type has
no object at all is still refused only through the missing-object error, not stated as such.
NOTE (R1, September 2026): the scenario_s02_01 / `env_layout_02.json` statements above PREDATE the cleaned
`env_layout_02` (no obstacles; coffee machine and AC switch side by side at x = −875, item_1 on the
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
SUPERSEDED IN PART (T-D R1, 27 September 2026): the `unknown` route no longer exists; its replacement is G. Not closed: the downstream response is G and X. design_decisions.md, "T-D R and E".
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
    SUPERSEDED IN PART (T-D R1, 27 September 2026): after a release the belief is uniform over the remaining live
    hypotheses with the finding unresolved (E6), or exhausted when none remain (R4); the window is P's.
    design_decisions.md, "T-D R and E".
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
SUPERSEDED IN PART (T-D R1, 27 September 2026): reason superseded by R1 (the grade leaves the belief). Not reopened. design_decisions.md, "T-D R and E".
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

**TODO-59 — A zero-length stretch is scored as a perfect fit: a lone surviving hypothesis is at 1/(1+u) before the agent moves** ✅ RESOLVED (I4c); its deferred part (stationarity as evidence) ✅ CLOSED by decision (T-D R and E, 27 September 2026: E2, E3; time enters adequacy, not the belief)
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
T-D R AND E (27 Sept 2026; design_decisions.md, "T-D R and E: the recognizer's output under a removed `unknown`
hypothesis"): the deferred part is CLOSED BY DECISION. Stationarity is not evidence in the belief: a stand in a
`move_to` phase is charged in the adequacy finding, against s_exp = 0, as the standing component of the projected
completion delay (E2, E3); the belief's likelihood and the empty-stretch rule are unchanged (R6). No second observation
channel is added to the belief. Note: under R1 a lone live hypothesis reads 1.0 at zero evidence, by normalisation over
the live hypothesis set, not by scoring; the symptom this TODO measured (a lone hypothesis high before the agent moves)
thus returns in another form, expected by R1 and measured in Stage 1, not corrected. This TODO is not reopened by it.

**TODO-60 — `unknown`'s u is charged per OPEN observation and never folded: the belief with no observation is the base ratio** ✅ RESOLVED (I4d)
SUPERSEDED (T-D R, 27 September 2026): u and the odds-against-`unknown` accounting leave the belief (R1); the invariant is sum-to-1 over the live hypothesis set H (R6). design_decisions.md, "T-D R and E".
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
SUPERSEDED IN PART (T-D R1, 27 September 2026): (a): its closure for walks by the grade — reason superseded by R1 (the grade leaves the belief). Not reopened. design_decisions.md, "T-D R and E".
SUPERSEDED IN PART (T-D R1, 27 September 2026): (b): the grade-based mechanism and reason — the 1/u per no-graded-signal phase, and the grade's closure of (b) for walks — are superseded by R1; the measurements and the questions stand. design_decisions.md, "T-D R and E".
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
SUPERSEDED IN PART (T-D R1, 27 September 2026): "the fold's 1/u at each phase advance": u leaves the belief (R1); the diagnostic and its question stand. design_decisions.md, "T-D R and E".
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
REFRAMED (T-D R and E, 27 Sept 2026; design_decisions.md, "T-D R and E: the recognizer's output under a removed
`unknown` hypothesis"). The constant `unknown` leaves the hypothesis space (R1); the job it competed for, holding the
line on behaviour that fits nothing, is now the adequacy finding's (R2, E4): unexplained when every live hypothesis's
tail probability is below the test level. A rationality measure would compete with the adequacy finding's reference
distribution (E5), not with `unknown`: another statement of how far observed behaviour may fall from a hypothesis's
model before the model is judged wrong. Still DEFERRED, not built. Trigger to revisit: E5's reopening condition
(limitation (c): data establishing a null whose spread depends on phase duration), or a ground-truth case the
per-phase test cannot express (limitation (a)). The trigger above is superseded by this one.

**TODO-64 — θ's reachability under the current model: the ceiling is 1/(1 + uⁿ), and reachability is a function of the live set** ✅ CLOSED (gate ruling, September 2026)
SUPERSEDED IN PART (T-D R, 27 September 2026): the ceiling 1/(1 + uⁿ) is gone; a lone live hypothesis reads 1.0 at zero evidence (R1). design_decisions.md, "T-D R and E".
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
SUPERSEDED IN PART (T-D R1, 27 September 2026): reason superseded by R1; the gate stands; its justification is re-derived from Stage 1's admission measurement (G). Not reopened. design_decisions.md, "T-D R and E".
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

**TODO-66 — The context / knowledge-representation pass: `_context_weight` branches on literal task names** [CLOSED, T-K part 1's build, 4 Oct 2026]
CLOSED (T-K part 1's build, stage 3, bbb7227, and stage 5, e589731; design_records.md, "T-K", THE BUILD): `_context_weight`
and its four constants are removed; the recognizer, the knowledge component and the memory of observed completions
name no task, fact, object or domain (a test asserts it, `tests/test_tk_prior.py`); the domain's declared context
knowledge lives in its registry (`"context_knowledge"`), and the prior of R2 and R3 takes the weight's place. The
long-shift rule leaves with no replacement (AM22; a stated limitation until T-K part 2).
RULED (T-K part 1, Hadi, 2 Oct 2026; design_decisions.md, "T-K: context knowledge in the recognizer's
belief"; design_records.md, "T-K", THE CUT): T-K part 1's build removes the domain task names and constants
from the recognizer and closes this item; the context weight is replaced by the prior of R2 and R3. Not built.
NOTE (T-G C1, Hadi, 1 Oct 2026; design_decisions.md, "T-G: the second domain's rulings", C1): T-K part 1, context
knowledge (framework-wide, after T-G's stage 1 and before its stage 2, from its own handoff), opens the question this item defers:
a context timeline in the scenario changing a fact at an authored point of a run, applied by the environment, and both
domains' foreseeable tasks conditioned on such facts; the form of a context fact is its first open question. It is the
pre-loaded context stream, moved from T-V track 2 (Phase 7). Whether T-K part 1 closes this item is for its design.
`_context_weight` still tests `hyp.task_name == "ac_activation"` and `"coffee_break"` and carries its own
constants (TEMPERATURE_BOOST 3.0, FATIGUE_BOOST 2.5, HIGH_TEMP_THRESHOLD 26.0, LONG_SHIFT_THRESHOLD 500) —
the one place in shared/ that names a domain task. Applied to the output only, never fed back, so it does
not touch the evidence state or the accounting. Deferred because fixing it properly reopens the ontology
and knowledge-representation questions (what a context fact is, which schema field declares a task's
sensitivity to it, where the constants live — a `ContextSchema`, not a branch). Not a bug in any measured
condition (no scenario sets the temperature or a long shift).
CORRECTED (C2, Hadi, 3 Oct 2026; measured in the review of the T-K part 1 records): "no scenario sets ... a long shift"
is wrong. The long-shift rule is reached by step count in any run of 500 steps or more: the shift starts at step 0
(`ContextKnowledge.default()`) and the step count serves as the clock, so coffee_break is multiplied by 2.5 from step
500 in every run. The runs it potentially confounds: design_records.md, "T-G stage 1", SCOPE REDUCED AND THE MPB ON
DOCK_LOADING RUN, its CAVEAT. T-K part 1's build still closes this item (the RULED line above).
RULED (AM22, Hadi, 3 Oct 2026; design_decisions.md, "T-K: context knowledge in the recognizer's belief",
CONTENT POINTS 1 AND 2): the hardcoded long-shift rule (the step count since the shift's start) leaves at the build,
and nothing replaces it in T-K part 1: the robot's expectation of coffee_break does not rise with the duration of work.
A stated limitation until T-K part 2 ("or" with "long work without a break" is among T-K part 2's open items, NOT RULED).
Files: shared/recognizer.py (`_context_weight`, the four constants), shared/knowledge.py (`ContextKnowledge`;
was shared/domain_knowledge.py)
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
SUPERSEDED IN PART (T-D R1, 27 September 2026): the `unknown` route no longer exists; its replacement is G. Not closed: the downstream response is G and X. design_decisions.md, "T-D R and E".
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
SUPERSEDED IN PART (T-D R1, 27 September 2026): the `unknown` route no longer exists; its replacement is G. Not closed: the downstream response is G and X. design_decisions.md, "T-D R and E".
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
assigned item_5 / item_1 / item_7. Since R1 `env_layout1` (since T-L stage 3 `env_layout_02`) is the cleaned layout
(no obstacles, new scenario_10 pool; now scenario_s02_01) and the old layout is `env_layout99.json`, which is NOT registered in
`domains/kitting/registry.py`. The ROS path would need `env_layout99` registered (or its own copy) to
reproduce what the guide describes. Not touched: `ros_sim/` is paused.
T-S (Hadi's order, 30 September 2026): done in T-S, ROS/PRIEST, when `ros_sim/` resumes (roadmap, "The plan from T-A",
T-S).
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
REOPENED AND CORRECTED (the MPB class-2 finding, 30 Sept 2026; design_decisions.md, "Realization as built", the dated
correction; T-B Q7 superseded in part): the robot's projection and its execution still differed at the head of the plan
in three executor states: (a) after a walk's acknowledgement the plan re-priced the completed walk (+1 tick), (b) and (c)
the owed acknowledgement and task completion ticks the body spends first were stated by no plan (−1, −2); T-B Q7's
"accepted" hold-0 residual was (b)/(c). Corrected: the body reports ExecutorState.owed_completion_ticks and
action_in_flight, the robot's projection states them (lead_in, resume_from), owed ticks run before a hold. Step
quantisation per walk stays uncompensated, as before. The human side's counterpart is TODO-146.
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
the nearer sample, not at its minimum. L2 measured the case: scenario_s01_06's head-on pass reads 11.0 cm
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

**REFACTOR-03 — `domains/README.md`: update domain folder name references** [V1]
WIDENED (T-G records 1, 1 Oct 2026): the README is stale throughout (`is_assigned` / `is_foreseeable`, `StepCall`, `DomainModel`,
`intentions`, `dock_delivery_loading/`, "pallet scanning has no microaction", which `scan_it` / TOUCH contradicts, the
driver reading of B1). Rewritten with T-G stage 1's build, not before. design_decisions.md, "T-G: the second domain's rulings", C3.
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
NOTE (T-G Q13b, Hadi, 1 Oct 2026): a script whose scans wait for the robot's deliveries is one the author declares
dependent on the robot: the loader reports the entries left open by the load-time replay and loads. design_decisions.md,
"T-G: the second domain's rulings", A3 (RULED).
ANSWERED, NOT BUILT (T-G records 1, 1 Oct 2026): `scan_pallet` is the old name of `confirm_delivered_pallet` (BUG-02). Answered by A3
(applicability; the human waits) and B2 (the scan's condition: the pallet in its delivery container). design_decisions.md, "T-G: the second domain's rulings", A3, B2.
Human `scan_pallet` executes without waiting for robot `deliver_pallet` to complete.
Mitigated by `office_break` delay in scenario. Proper fix: DESIGN-01.

**LIMIT-03 — Gate always open**
ANSWERED, NOT BUILT (T-G records 1, 1 Oct 2026): the gate's state is declared in the setup and opened on request (B5, stage 2); stage 1
declares it open (C1). design_decisions.md, "T-G: the second domain's rulings", B5.
`gate_is_open(dock_gate)` emitted unconditionally. Gate state not modeled dynamically.
Fix: TODO-08 (`open_gate` action schema + `gate_closed` method).

**LIMIT-04 — All pallets start at same position (truck center)** [FW]
[FW] (T-G A10, B9, T-G records 1, 1 Oct 2026): in V1 a container is one point, its centre, with no constraint, and may hold several pallets
(B9); authored pallet places are not taken. A container divided into positions, the position chosen when an object is
put down, is FW, with no new item. Pallets drawn on top of each other are a drawing matter for T-V. design_decisions.md, "T-G: the second domain's rulings", A10, B9.
NOTE (records, 2 October 2026; T-G records 9; design_decisions.md, "T-G: the second domain's rulings", STAGE 1, THE IRB ON DOCK_LOADING BUILT, RUN AND ACCEPTED; B9's note): a property of "one point per container": two pallets
in one container stand on one point, so the second scan has no walk (C3: three stretches of 3 ticks, never at the
threshold) and no walk between them exists that an event could cut (M3 as first written was not buildable).
Pallets 0–5 all share `truck_interior` center position. No individual slot positions.
Deferred: individual pallet slot positions within truck area.

**LIMIT-05 — Empty pallet bays not wired to `LOAD_RETURN` task execution yet**
NOTE (T-G records 1, 1 Oct 2026): it conditions on BUG-01 and BUG-02, both resolved. Its content is replaced by B4 (a pallet's full/empty
condition as the state fact `is_empty(pallet)`, read by the methods) and B11 (one method per starting area). design_decisions.md, "T-G: the second domain's rulings", B4.
`load_return` tasks defined and in scenario but may not complete correctly
until BUG-01 and BUG-02 are resolved and full scenario runs end-to-end.

**LIMIT-06 — Robot task queue is pre-ordered in scenario file** [Phase 4] ✅ RESOLVED
Robot's `scheduled_tasks` is currently an ordered list in `AgentConfig`.
Ordering should be the meta_planner's responsibility. Accepted for Phases 1–3;
fix in Phase 4 via TODO-14.
Resolved: the robot's task pool is `AgentConfig.assigned_tasks` (unordered); ordering is the
meta_planner's (assignment-prior session, September 2026).

**TODO-80 — Declared human behaviour outside the robot's domain knowledge** [later extension; from F47b] [mind side SUPERSEDED (T-D X2)]
SUPERSEDED IN PART (T-D X, X2, ruled by Hadi 29 Sept 2026; design_decisions.md, "T-D X: response"): the
blocked-execution event below is not built on the mind side (no fourth trigger; the WAIT / RECONSIDER pair is not
built): the stop's refusal adds no information the mind needs; P4's `projection_expired` and L2 (ii)'s retraction
re-decide on where the human is. The separation stop (C) is unchanged. The declared-stay fixture notes below stand as
history.
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
OBSERVED (T-C2c, `analysis/tc2c_scripts/`, scenario_s01_02): the declared stay is scriptable; after `Stay(40)` the script
ends and the human stands at the table, so with the stop on the robot is refused from 79 to the end (121 ticks), the
terminal-stay block above; a stay that ends needs content after it.
T-D (the play, `analysis/tc2c_scripts/play.md`): T-D's blocked fixture uses a stay that ENDS. A stay that ends is waited out with the stop on
(scenario_s07_05: refused 144–186, completion 413 against 370; scenario_s03_03's mid-run stay likewise); only the human's
end-of-script stand at a table deadlocks (01, 02, 04, 23). Scenario-authoring convention since 23 Sept 2026: a
script ends with the human leaving the workspace, unless the scenario is about that terminal stand
(design_decisions.md, "The human action script (T-C1, decided)", AS BUILT convention).
Files: domains/kitting/scenarios.py, mesa_sim/sim_agents.py (HumanAgent), shared/types.py
Reference: F47b session, September 2026; design_decisions.md, "Scheduled bindings are typed"
T-H (25 Sept 2026; design_decisions.md, "T-H: the human behaviour model"): the declared behaviour this item asks for is a `HumanOnlyTask` instance in the human's script, `stand(?duration)` for a stay of a stated length wherever the human is (its stand action emits no world fact), `go_to(?landmark)` for a walk; it is in the tree and never in a robot's task model, so it adds no hypothesis (coverage `TASK_ABSENT`). The scenario-side vocabulary and the superset domain of the text above become one tree and a task model. The terminal stand at a table stays undeclared by the authoring convention.

**TODO-81 — The Mesa decomposer reads the literal `"?duration"`; the schema names the binding (`duration_key`)** [housekeeping; from R2] ✅ CLOSED (T-H1, e571eed)
CLOSED (T-G records 1, 1 Oct 2026): both halves were done in T-H1 (e571eed, 25 Sept 2026): `action_decomposer._expand_stand` reads
`action.schema.duration_key`, and dock_loading's `wait_at` declares `duration_key="?duration"`. The T-G line below and
the roadmap's "TODO-81 with them" are history.
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
T-G (Hadi's order, 30 September 2026): done in T-G with TODO-25's schema fixes; `duration_key="?duration"` on
dock_loading's `wait_at` in the same change (roadmap, "The plan from T-A", T-G).
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

**TODO-85 — A stationary human: a stay as evidence (a) and the robot's action under `unknown` (b)** [T-C open item; from T-A1] (a) ✅ CLOSED by decision (T-D R and E, 27 September 2026: E2, E3; time enters adequacy, not the belief); (b) OPEN (T-D Q1, P)
SUPERSEDED IN PART (E10, 1.5 rulings, 27 September 2026): (a)'s "time enters adequacy, not the belief": standing beyond a phase's priced duration enters the belief through L(v·D) as well as adequacy through S(v·D); (a) stays closed. design_decisions.md, "T-D R and E", "1.5 rulings".
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
OBSERVED (T-C2c, `analysis/tc2c_scripts/`, scenario_s02_02): a stay mid-carry (30 ticks at the coffee machine holding
item_2) freezes the belief (`deliver_item(item_2)` 0.550, `coffee_break` 0.345, `unknown` 0.088) with no trigger,
as expected. For (b), observed in scenario_s01_02: once the human's hypothesis space is exhausted (its last assigned
task pinned), `unknown` reads 0.995 and no projection exists, so a finished work order and unmodelled behaviour are
indistinguishable to `update()`. T-D decides.
THE GENERAL FORM OF (b) (the play, `analysis/tc2c_scripts/play.md`): the robot is blind after EVERY human task completion, not only when the
hypothesis space is exhausted. The episode boundary resets the belief to the prior, below θ, so no projection is
admitted, while the human stands at the table it just delivered to, which is where the robot delivers. scenario_s05_03:
the robot's carry passes 0.78 cm from the standing human (tick 100), before the robot's own completion; 01, 02, 04,
22, 24, 52 show 1–15 cm at the end of the run (stop off). Only the separation stop covers it. T-D's opening item.
Files: shared/recognizer.py (`_progress_likelihood`), shared/meta_planner.py (`update_human_projection`)
Reference: T-A1, September 2026
See TODO-95 (23 Sept 2026): the deferred stationarity channel is taken up there as a design task.
T-H (25 Sept 2026; design_decisions.md, "T-H: the human behaviour model"): half (a)'s "separate item T-H" is TODO-95; the name T-H now means the human behaviour model. The stay is written as the `stand` task, and the record says whether the human is standing inside a task (the `wait_at` of `coffee_break`), in a `stand` task (`TASK_ABSENT`) or with nothing on the stack; "a finished work order" reads "every assigned task done". Half (b) stays T-D Q1, whose ground-truth cases the record now gives.
T-D R AND E (27 Sept 2026; design_decisions.md, "T-D R and E: the recognizer's output under a removed `unknown`
hypothesis"): half (a) is CLOSED BY DECISION. Standing counts against pursuing a task whose phase prices no standing,
but in the adequacy finding, not in the belief and not for `unknown`, which leaves the hypothesis space (R1): the
standing component of the projected completion delay against the phase's priced standing (E2, E3), read against the
reference distribution (E5); the belief's likelihood is unchanged (R6). Half (b) stays open: T-D Q1 (option 1) is
unchanged and is P's building block; what the meta-planner does with belief, finding and lifecycle is G and X (R5).
The observation "once the hypothesis space is exhausted `unknown` reads 0.995" is replaced by the lifecycle state
exhausted (R4), in which no finding is reported.

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
T-H (25 Sept 2026; design_decisions.md, "T-H: the human behaviour model"): the correspondence between the assigned tasks and the script is no longer checked by provenance: `check_work_order` and `Provenance` are deleted in T-H3 and the record's query `unperformed(assigned_tasks)` replaces the check, and a delivery to another table is a plain instance `deliver_item("item_1", table=...)`, checked for types only. Whether it counts as an assigned task is `assigned(task)`'s type, settled in T-H4.

**TODO-87 — A delivery to another table: no task boundary, no pin, no pool drop** [deviation case; from T-B1a] [RULED (T-D L1, 27 Sept 2026); built in L-build]
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
REPRODUCED (the play, `analysis/tc2c_scripts/play.md`; reachable since T-C2a's `deviate`): scenario_s06_06 (env_layout_08) and scenario_s07_03
(env_layout_09). No pin and no boundary at the misdelivery; after the next boundary `deliver_item(item)` leads again
(about 0.9: the item lies on the wrong table, so its delivery is still open), and the robot plans against a projected
human carrying it back, who stands still.
Files: shared/recognizer.py (`update`, `_terminal_complete`, `_task_boundary`), shared/meta_planner.py
(`_is_complete`), shared/planner.py (`is_complete`)
Reference: T-B1a, September 2026
T-H (25 Sept 2026; design_decisions.md, "T-H: the human behaviour model"): the wrong-table delivery is written as a plain instance with the other binding and is labelled on the record `coverage` `BINDING_ABSENT`. The recognizer-side behaviour recorded here (no pin, no boundary, no pool drop) is unchanged by T-H and stays with T-D Q4, now with ground truth for it.
T-D Stage 1 (27 Sept 2026; `analysis/td_stage1/REPORT.md`, 1.4 finding 5): the item's hypothesis keeps leading at 0.995
into the human's next task (scenario_s06_06 prior on after the release at 103, scenario_s07_03 after 94). Cycle 2 (L).
T-D 1.5b (27 Sept 2026; `analysis/td_stage1b/REPORT.md`, finding 5): G1 refuses the wrong-table carry (76, 79:
`none(leader_inadequate)`), but after the release the misdelivered item's hypothesis is admitted again at 0.995
(scenario_s06_06 at 103, scenario_s07_03 at 94, both priors): with no boundary at a misdelivery, its new derived phase
(pick the item up where it now lies) is a member at S = 1. Cycle 2 input (L).
IRB (IRB.4b, 27 Sept 2026; `analysis/irb/REPORT.md`, scenario_s09_08, prior on): item_1 released on kitting_table_1 at 75, no pin and no boundary; `deliver_item(item_1)` keeps leading into the next delivery (0.997 at 86, 0.897 at 120) while the true `deliver_item(item_2)` never reaches θ (at most 0.483, at 130); it is never pinned in the run.
RULED (T-D L1, Hadi, 27 Sept 2026; design_decisions.md, "T-D L: the belief lifecycle"): the episode boundary fires when
the observed agent completes an action that is terminal in the task model (`place`, `wait_at`), read from the completion
channel, whatever its binding; the pin stays the world's terminal fact. The misdelivery is a boundary (scenario_s09_08 at
75), no pin: `deliver_item(item_1)` stays live and starts the next episode at the prior. The pool side (no pool drop) is
unchanged: the task is not complete in the world. Built in L-build.
AMENDED (Hadi, on the L-records report, 27 Sept 2026): not "read from the completion channel": the boundary fires when a terminal action's
own completion condition becomes true for the observed agent (the item it held on the previous tick placed at a
container; `waited(agent, ·)` starting). A bare RELEASE is no boundary. design_decisions.md, "T-D L", L1 as amended.
BUILT (L-build, 28 Sept 2026; 2c54c4a): the misdeliveries are boundaries without a pin (scenario_s09_08 at 75,
scenario_s06_06 at 103, scenario_s07_03 at 94); the delivery stays live; `analysis/l_build/REPORT.md`. The pool side
unchanged, as ruled.

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
executed stop point (10 to 15 cm, step quantisation of the arrival). ILLUSTRATION, scenario_s06_03 at step 159: the
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
(scenario_s02_01 b2a prior on, tick 74: [50, 51] straddles the realized end 50.81, inside by the label, edge by the
glossary). Label only: the stop's refusal does not read it, no behaviour depends on it. Not fixed.
Files: mesa_sim/executor.py (`set_assessed_window`, `_log_stop`), mesa_sim/sim_agents.py
Reference: TODO-90 check, September 2026; analysis/todo90_b2a_window/README.md

**TODO-92 — An observed history of the human's tasks in the robot's mind** [T-D; from T-C1] ⛔ SUPERSEDED by T-H4 (25 Sept 2026) for its ground-truth half: the WORLD labels are queries on the human executor's record (`assigned(task)`, `coverage(task, robot)`, `truth_at(tick)`), not computed from the script and provenance. The history in the robot's mind, built from observation, is not part of T-H and stays with T-D. T-H4 built the queries (`world/queries.py`; design_decisions.md, "T-H: the human behaviour model", as built T-H4).
The robot's mind keeps nothing from the human's script (T-C1), and today it keeps no record of what it has
observed of the human either: completions reach it as world facts, retractions and `unknown` episodes as
belief changes, and nothing accumulates them. Recorded for evaluation: a history, in the robot's mind, of the
human's tasks as observed — completed, dropped, `unknown` episodes. Built from what the robot observes, never
from the script. Designed in T-D. The robot taking over an abandoned task is a separate item (TODO-15).
NOTE (24 Sept 2026, the terminology ruling; `docs/glossary.md` §7): the evaluation will also need the WORLD labels
of each human behaviour, label A (assigned task or deviation) and label B (modelled or unmodelled behaviour: whether a
`HypothesisKey` of the robot's hypothesis space describes it), and the label-C check of a scenario (its purpose
against the computed coverage; a mismatch means unintended unmodelled behaviour). They are
ground truth, computable from the script (with its provenance) and the hypothesis space, and kept OUTSIDE the
robot's mind, unlike this history, which is built from observation. Not built; recorded here because the
evaluation compares the two: unexplained (the robot's finding) against unmodelled (the label).
The I4 harness (`analysis/i4_evidence_model/check_i4.py`, reused by I4c, I4d and I5) labels its ground truth
`"unknown"` while the human is idle or wandering, and so counts `unknown` leading as correct on those ticks. Any
evaluation that reuses the harness must rescore against labels A and B.
`docs/terminology_revision.md`, sections 2 and 4.
Reference: T-C1, 23 September 2026; design_decisions.md, "The human action script (T-C1, decided)"

**TODO-93 — The completion of a foreseeable task ends the episode while an assigned delivery is visibly in progress** [T-D; from T-C2c] [CLOSED by design (T-D L3, 27 Sept 2026)]
Observed in scenario_s02_02 (`analysis/tc2c_scripts/`): the human picks up item_2, walks to the coffee machine holding
it and waits there. At 75 `waited(human_0, coffee_machine_0)` pins `coffee_break`, and because that hypothesis
expected its terminal action on the previous tick, the retirement is an episode boundary: every base becomes the
uniform prior and every origin moves, although the human still holds item_2 and the delivery is in progress. The
belief falls from `deliver_item(item_2)` 0.550 to 0.248 (four-way tie) and the delivery is recognised again from
scratch (it clears θ at 100). Nothing is wrong by the current rule (docs/recognizer_handback.md §1.6: the observed
agent finished a task); whether a task completed INSIDE another, with its item in hand, should end the episode is
for T-D. Recorded, nothing changed.
REPRODUCED (the play, `analysis/tc2c_scripts/play.md`): scenario_s02_03, scenario_s04_02 and scenario_s05_03, on env_layout_02, env_layout_05 and env_layout_07.
Files: shared/recognizer.py (`update`, `_task_boundary`)
Reference: T-C2c, September 2026; docs/recognizer_handback.md §1.6
CLOSED BY DESIGN (T-D L3, Hadi, 27 Sept 2026; design_decisions.md, "T-D L: the belief lifecycle"): no change under L1.
Every terminal action is a boundary regardless of task class; the suspension is carried by the world (the held item
re-derives both hypotheses from the first tick of the new episode: scenario_s09_03 from 84, `deliver_item(item_1)` at θ
again at 100), not by the belief; empty-handed (scenario_s09_04 from 82) nothing persists (I4c Decision 2). The belief
near 0.5 after a break is genuine ambiguity. Set aside: a class exception for foreseeable terminal actions; a
suspended-task representation.

**TODO-94 — Re-recognition inside an episode depends on the length of the misleading walk** [T-D; from the T-C2c play] [RULED (T-D L2, 27 Sept 2026); the meta-planner side built in L-build]
SUPERSEDED IN PART (T-D R1, 27 September 2026): wording superseded by R1; the case stays L. design_decisions.md, "T-D R and E".
Observed (`analysis/tc2c_scripts/play.md`). The evidence a walk lays against the hypotheses it does not serve (refutation by wasted path)
persists until an episode boundary, and only a task completion makes one: nothing else resets excess path. So a
change of mind, or a detour mid-task, is recognised again only if the misleading walk was short. Short (12–22 ticks:
scenario_s03_07, scenario_s03_04, the return in scenario_s01_07, scenario_s03_08's near corner): the task the human now does recovers,
sometimes a few ticks before its release. Long (the 77-tick walks of scenario_s06_05 and scenario_s07_02; the long detours
of scenario_s07_04 and scenario_s03_02): it never recovers, and the robot sees `unknown` (0.994) for the whole second
delivery. scenario_s01_03's return is the same pattern (`deliver_item(item_2)` leads two ticks before its release). The
same mechanism hides a foreseeable task: in scenario_s04_02 `coffee_break` never rose on the walk to the machine (the walk
to item_3 had refuted it), where in scenario_s02_02 it rose to 0.345. The recognizer judges nothing; whether evidence
should decay, be reset by another event, or stand, is a recognizer question for T-D. Recorded, nothing changed.
Files: shared/recognizer.py
Reference: T-C2c play, 23 September 2026; docs/recognizer_handback.md §1.4, §1.6
IRB (IRB.4b, 27 Sept 2026; `analysis/irb/REPORT.md`, scenario_s09_05, prior on): the corner walk mid-delivery, 32 to 79; `deliver_item(item_1)`'s one derived phase `move_to(kitting_table_0)` runs 30 to 125, its S below α from 48; the finding is unexplained 48 to 125, through the resumed carry (80 to 125), where the delivery reaches θ at 87 while inadequate; adequate again at 126 (its advance to `place`).
IRB (IRB.4b, 27 Sept 2026; `analysis/irb/REPORT.md`, scenario_s09_07, prior on): the change of mind: after item_1's grasp (30) `deliver_item(item_2)` is started (32) and returns item_1 to its shelf (33); `deliver_item(item_2)`, whose S the first walk had put below α at 14, rises from 0.000 at 35 to θ at 64, 32 ticks after the switch, adequate throughout; `deliver_item(item_1)` falls below α at 44 and, resumed at 110 after the boundary at 108, reaches θ again at 135. The finding stays adequate until the exit walk (204).
RULED (T-D L2, Hadi, 27 Sept 2026; design_decisions.md, "T-D L: the belief lifecycle"): (i) recognizer, no change: the
evidence of a misleading walk stands; inadequacy attaches to the phase and is not retracted when behaviour becomes
consistent again (scenario_s09_05: inadequate 48 to 125, adequate at the advance, 126); no reopening on the finding, no
turn-back rule, no window. (ii) meta-planner: `recognition_changed` also fires when the projected hypothesis leaves
adequate (retraction; TODO-118). (iii) "consistent again" is meaningful at the next phase advance; a resumed carry is
unprojected until its advance (46 ticks in scenario_s09_05).
AMENDED (Hadi, on the L-records report, 27 Sept 2026): (ii) "leaves adequate" is adequate to inadequate, the recorded hypothesis only (built
as the state: it is inadequate); no P fallback. (iii) "consistent again" arrives at the next phase change, advance or
regress. design_decisions.md, "T-D L", L2 as amended.

**TODO-95: Stationary behaviour leaves no evidence; the robot's response to `unknown` and a stationarity channel (design task, raised at T-D Q1, 23 Sept 2026)** [CLOSED (Track 2.5, Hadi, 28 Sept 2026; docs/assumptions.md 3.4); its open levels moved to X and TODO-132 (b)]
CLOSED (Track 2.5; ruled by Hadi 28 Sept 2026, recorded 29 Sept 2026). The recognition level, closed by decision in T-D R
and E, closes as not needed (docs/assumptions.md 3.4): a stand inside a task is a pause while it lies within the
standing its derived phase prices (s_exp, E9, E10); beyond that the phase does not fit and, if no other live hypothesis
fits, the finding is unexplained. Standing contributes no hypothesis-specific evidence while the live hypotheses price
the standing equally; a movement of the probabilities is a consequence of the evidence function and the normalisation,
not evidence that one hypothesis explains the stand better (the probabilities are not claimed invariant: scenario_s09_06,
deliver_item(item_1) 0.8608 to 0.9184 over its stand). No stay hypothesis is introduced; P4's fallback projection
carries an observed stand. The open levels move, explicitly: level 1 (decision level) is built as T-D P (P4's observed
stand); level 2 (execution: the blocked event, WAIT against RECONSIDER) and level 3 (interaction: communication,
TODO-96) are X's; the sustained stand as a question for the meta-planner is TODO-132 (b). The text below is kept as the
record.
LEVELS 2 AND 3 DISPOSED (T-D X, ruled by Hadi 29 Sept 2026; design_decisions.md, "T-D X: response"): level 2 by X2 (the
blocked event is not built; the re-decision comes from P4 and L2 (ii); the stop stays an execution safeguard); level 3
by X5 (the two grounds for communication recorded, no act built; TODO-96). Nothing of TODO-95 stays open.
Status: open. To be raised at the T-D recognizer pass (Q2 to Q4): rule there whether this joins
the pass or stays recorded for T-H.
T-D R AND E (Hadi, 26 to 27 Sept 2026; design_decisions.md, "T-D R and E: the recognizer's output under a removed
unknown hypothesis"). Supersedes the status line above. The RECOGNITION LEVEL (level 4 below) is CLOSED BY DECISION
(E3, E5): a stand does not become evidence in the belief. Time enters the adequacy finding only (E3), as the standing
component of the projected completion delay D against the phase's priced standing s_exp (E2), read against the
reference distribution of E5; the belief's likelihood and the empty-stretch rule stand (R6), and the `unknown`
hypothesis leaves the hypothesis space (R1). The design questions below, as answered there: 1 (the observation) by
E1, E2 and E6: the unit is each live hypothesis's derived phase, from its origin; standing beyond s_exp is an
observation for adequacy, not for the belief; the finding clears at a phase advance or a boundary (E7). 2 (direction
per hypothesis) by E2's s_exp per action (0 for move_to, 1 tick for pick_up and place, the bound duration for
wait_at); the schema durations of pick_up and place are a dependency to verify in the build. 3 (the likelihood form):
not a likelihood; D and the tail S of E5; the odds-against-`unknown` invariant no longer exists, replaced by R6's
sum-to-1 over the live hypothesis set H. 4 (TODO-59 must not return): standing confirms nothing in the belief (E3,
R6); R1's lone live hypothesis at 1.0 on zero evidence is by normalisation, expected and measured in Stage 1 (R1). 5
(what it means to the meta-planner) is G, open. 6: "a reading of `unknown`" is gone with R1; whether a stay is ever
written as a foreseeable task is not ruled by R and E.
THE OTHER LEVELS STAY OPEN: level 1 (decision level) is T-D Q1 (option 1), unchanged, P's building block, not built;
level 2 (the blocked event, WAIT against RECONSIDER) and level 3 (communication on a persistent finding, TODO-96) are
X; what the meta-planner does with belief, finding and lifecycle is G (R5). Each is ruled on Stage 1's results.
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
IRB (IRB.4b, 27 Sept 2026; `analysis/irb/REPORT.md`, scenario_s09_06, prior on): `stand(PT80S)` at shelf_1 30 to 70, inside `deliver_item(item_1)`'s `pick_up` phase (s_exp 2); its S below α at 47 (17 standing ticks beyond s_exp); the finding unexplained 47 to 71 while the belief holds at about 0.92 (the rival is charged for the same ticks); adequate at the grasp, 72.

**TODO-96: Communication as a response under sustained `unknown` or a block (recorded, T-D Q1 discussion, 23 Sept 2026)** [OPEN; future work, with TODO-136; rewritten to X5's two grounds, 29 Sept 2026]
T-G A10 (T-G records 1, 1 Oct 2026): two communication acts stay under this item and X5, with no FW item of their own: the human assigning
or changing a delivery location during the run; the robot informing a third party. design_decisions.md, "T-G: the second domain's rulings", A10.
REWRITTEN (T-D X, X5, ruled by Hadi 29 Sept 2026; design_decisions.md, "T-D X: response"). Communication is an X-level
response considered when the robot reaches a persistent situation its recognition-and-planning machinery cannot
resolve, on two grounds, each an existing observable with no constant: (1) not understanding: the adequacy finding is
unexplained and has outlived at least one re-decision (a trigger fired, admission refused, the finding still
unexplained), persistence measured by the robot's own re-decision cadence; (2) understanding without resolution: at a
decision every candidate's realized plan holds against the projected human, and at the robot's next re-decision the
same structural condition still holds. No mechanism and no runtime event; both are read from the logs in the
evaluation analysis (ground (2) under `full_reorder` needs TODO-141). The condition "a blocked event that WAIT and
RECONSIDER do not resolve" below is retired as an independent condition and folds into ground (2) (X2: no blocked
event). The act, its channel and its effect are future work with the reactive human (TODO-136). The text below is kept
as the record.
SUPERSEDED IN PART (T-D R, 27 September 2026): the condition "sustained `unknown`": the `unknown` hypothesis leaves the hypothesis space (R1); X names communication on a persistent finding. design_decisions.md, "T-D R and E".
TERMS (24 Sept 2026, `docs/glossary.md` §7): "unknown behaviour" below means unmodelled behaviour; "sustained
`unknown`" is the belief's residual mass, which is not the same condition.
Status: open, recorded only. Hadi: under unknown behaviour the robot may stop and communicate
(ask the human what is happening, raise an alarm) instead of, or after, re-planning. No
communication channel exists in the framework. Level 3 of the response structure in TODO-95.
Its condition (sustained `unknown`, or a blocked event WAIT and RECONSIDER do not resolve)
must be defensible without a constant taken from a scenario. To be argued at T-D Q5 or after;
not part of T-D Q1.
LINKED (T-K part 1, AM71, Hadi, 4 October 2026; design_decisions.md, "T-K: context knowledge in the recognizer's
belief", R7's AM71): communication or slowing down on a weak admission (the discussion's 4.A after step 5b) is not taken
in the framework and is possible future work, under this item. Its cases: an admission that can be wrong while the
robot plans on the admitted task alone (scenario_s16_05, 28.3 cm; scenario_s11_03, 11.3 cm). No condition for "weak"
is ruled.

**TODO-97: Belief-aware planning: a joint realization against the hypotheses that cover the belief (recorded, 24 Sept 2026)** [OPEN, recorded only; later, after the T-D Q2 to Q4 recognizer pass]
LINKED (T-K part 1, AM71, Hadi, 4 October 2026; design_decisions.md, "T-K: context knowledge in the recognizer's
belief", R7's AM71): the discussion's 3.B after step 5b, the robot's plan checked against the admitted task's projection
and the fallback projection together, is not taken in the framework and is possible future work. Hadi's position in
the discussion: it changes the meta-planner and mixes high-level planning with a lower level; it may be part of future
work on planning that uses the belief, which is this item's direction. design_records.md, "T-K", THE DESIGN DISCUSSION
AFTER STEP 5B and THE GATE AFTER STEP 5B, RULED.
SUPERSEDED IN PART (T-D R1, 27 September 2026): `unknown` is not a member of S_ε; the finding's role in belief-aware planning is G; TODO-97's gate is unchanged. design_decisions.md, "T-D R and E".
Status: open, recorded only. Not on the T-D agenda, not in the handoff order.
LINKED (records, 2 October 2026; T-G records 9; design_decisions.md, "T-G: the second domain's rulings", STAGE 1, THE IRB ON DOCK_LOADING BUILT, RUN AND ACCEPTED): the IRB on dock_loading confirmed T-G's watched item
C5, a finding about the mind, NOT RULED: hypotheses that predict the same motion divide the belief and none is admitted
(two unscanned pallets in one bay: in C3 and on C4's first two walks, all three rooms, 9 stretches never reach the
threshold). The direction recorded here, acting on a set of hypotheses with the same projection (the covering set S_ε,
one joint realization), is the one this finding returns to the design chat with.

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
THE UNION PROJECTION, TWO VARIANTS (recorded at the G/X handoff, 29 Sept 2026; a decision of the design chat, parked):
planning against the plans of several hypotheses when none clears θ has two variants to distinguish when this is taken
up: the fit-set variant (realize against every adequate hypothesis's plan) and the belief-weighted variant (weight the
hypotheses' plans by their belief). The case that decides between them: a hypothesis adequate for one tick with almost
no probability. In the priority of projections the design chat stated (admitted projection, then the union, then the
physical fallback; in no entry, TODO-119 records only that an admitted projection outranks the fallback), the union
sits in the middle, parked. Reference: docs/handoffs/handoff_G_X_onward.md, 2.3 and 2.4.
Related: TODO-84, TODO-95, TODO-15, DESIGN-07, D3; design_decisions.md, "Belief-aware planning".

**TODO-98: A foreseeable task is kept out of `assigned_tasks` by convention only (recorded, 24 Sept 2026)** [OPEN, recorded only]
Nothing checks it: `check_work_order` treats a foreseeable task in the script as free, and neither `AgentConfig` nor
the loader rejects one listed in `assigned_tasks`. If one were placed there, the behaviour would be both an assigned
task and a foreseeable task, which label A (assigned task or deviation; a foreseeable task is a modelled deviation)
cannot express. Recorded only; no check added.
Files: shared/types.py (`AgentConfig`, `check_work_order`)
Reference: terminology follow-up, 24 September 2026; `docs/glossary.md` §6 (foreseeable task), §7 (label A)
T-H (25 Sept 2026; design_decisions.md, "T-H: the human behaviour model"): resolved by the tree: a `PersonalTask` is never assigned and foreseeable is defined as a `PersonalTask` in the task model, so a foreseeable task in the assigned tasks is a type error, checked when T-H1 builds the classes. ✅ CLOSED by T-H1: `AgentConfig` rejects an assigned task whose schema is not a `WorkTask`.

**TODO-99: `during`'s authored form (recorded, T-H, 25 Sept 2026)** [OPEN; built when the live-run exporter needs it] ✅ CLOSED by the rulings on the T-H review (25 Sept 2026): the authored form `during(action, ticks=n, do=...)`, a `DuringAction` trigger, is built in T-H2, not deferred; the text below is the record of the first ruling.
`during(action, ticks=n, do=...)` is the event trigger for a cut inside an action, n ticks into it; no fraction or
position forms (T-H item 5). T-H2 builds the mid-action cut (reached by `inject`) but not the authored form. Until it
is built, an injection that lands inside an action cannot be exported, so the byte-identical replay of T-H item 8
covers injections at an action boundary (exported as `at`).
Reference: design_decisions.md, "T-H: the human behaviour model", items 5 and 8

**TODO-100: Nested interruptions beyond one level (recorded, T-H, 25 Sept 2026)** [OPEN, recorded only]
The human executor's stack is one level deep in T-H: an event on a task that is itself a decision's task is not
admitted. The stack structure allows nesting; the restriction is lifted only when a scenario needs it.
Reference: design_decisions.md, "T-H: the human behaviour model", items 6 and 10

**TODO-101: Oracle-IR evaluation (recorded, T-H, 25 Sept 2026)** [OPEN; its own pipeline task after T-H]
Three conditions on the same scenario: no IR; IR; oracle IR, where the meta-planner receives the record's
`truth_at(tick)` instead of the belief. It separates what the planning side does with a correct intention from what
the recognizer's errors cost.
The interface it needs (recorded, not designed):
- from the record (T-H2, T-H4): `truth_at(tick)`, the stack at a tick, top first (the task on top, or none), and
  `coverage(task, robot)`;
- `truth_at` enters the robot's mind only through this condition's explicit adapter (ruling, 25 Sept 2026); nothing
  else in the mind reads the record, and `world_state_builder` exposes nothing of the human's stack (T-H2's test);
- simulation only: the record exists for a simulated human; a real human needs annotation of the same form;
- in the robot's mind: one seam where the belief enters. Today the `BeliefState` is taken by
  `MetaPlanner.evaluate_triggers()`, `update_human_projection()` and `update()`; the oracle condition substitutes its
  source there, as a belief with all mass on the `HypothesisKey` of the task on top when its coverage is `COVERED`.
  `shared/` receives a belief as today and never imports the record;
- open for that task: what the oracle hands over when the task on top is not covered (the projector resolves a task
  through the recognizer's hypothesis, so an uncovered task has none) or the stack is empty; and what "no IR" feeds the
  three calls (no belief: no admitted projection, `recognition_changed` never fires).
- THE SEAM (recorded at T-H4, not built): `world/queries.py` gives `truth_at(record, tick)`, the tick's `Snapshot`
  (`stack[0]` the task on top, or an empty stack), and `coverage(top, robot)` against the robot's `ObservingRobot`
  (`SimModel.observing[robot_id]`). A `Covered` result carries the `HypothesisKey` that describes the task: the
  adapter's belief puts all mass on it. The adapter is the body's (it holds the record and the robot's side) and hands
  the meta-planner a `BeliefState` as today; `TaskAbsent`, `BindingAbsent` and the empty stack are the open cases
  above.
- THE T-D STAGE 1 EVALUATION (T-D R and E, 27 Sept 2026; design_decisions.md, "T-D R and E: the recognizer's output
  under a removed `unknown` hypothesis", Staging): after the Stage 1 build (the recognizer side, the baselines
  regenerated, the gate left as it is), verify the arithmetic invariant of R6 (on every tick the returned
  probabilities sum to 1 over exactly the live hypothesis set H) and, separately, the adequacy accounting; the
  recognizer's outputs (belief, adequacy finding, lifecycle state) per ground-truth case against oracle IR; admissions
  before and after on the maintained baselines; false-unexplained per phase and per run, missed findings and detection
  delay, at every test level α (0.01, 0.05, 0.1). The ground truth is the record's (`truth_at`, `coverage`); the oracle
  interface above serves it.
- THE IRB (ruled 27 Sept 2026; design_decisions.md, "The intention-recognition test-bed (IRB)"): the recognizer tested in
  isolation against expectations derived from the entry "T-D R and E" before the run, not through this oracle
  adapter, which stays unbuilt. The cases the 48 fixtures lack (the corner walk, a switch outside the support) are its
  layer 4, TODO-122.
- 1.4 (27 Sept 2026, `analysis/td_stage1/REPORT.md`) measured against the record directly (`truth_at`, `coverage`);
  oracle IR is still unbuilt.
- The 48 logs of the maintained baseline sets contain no `TASK_ABSENT` case and no case outside the hypothesis
  space's support (every entry `COVERED`, no `go_to`, no exit walk; 1.4 §H case 1). The IRB, a separate
  track, will.
Reference: design_decisions.md, "T-H: the human behaviour model", item 10; roadmap, "The plan from T-A"

**TODO-102: A per-robot task model on the robot's `AgentConfig` (recorded, T-H1, 25 Sept 2026)** [OPEN, recorded only]
T-H1 gives every robot the task model its use case declares (`domain_config["task_model"]` in the registry), built per
robot by the loader. "Chosen per experiment" (T-H item 3) needs a place to state it: a task model on the robot's
`AgentConfig`, the `PersonalTask`s kept (every `WorkTask` is in it by construction). Needed first when an experiment
omits a `PersonalTask` (coverage `TASK_ABSENT`, T-H4; T-D Q1's switch to an unmodelled task).
Files: shared/types.py (`AgentConfig`), mesa_sim/sim_model.py (`_spawn_agents`), domains/*/registry.py
Reference: design_decisions.md, "T-H: the human behaviour model", item 3; Hadi's ruling on the T-H1 plan (Q3)

**TODO-103: A stale test in tests/test_script_layer.py (recorded, T-H1, 25 Sept 2026)** [CLOSED, T-H3: the file
was deleted with the C1 layer; its surviving checks are in tests/test_th3_scenarios.py]
`test_loader_errors_name_the_scenario` fails at ea4446c (before T-H1) and after it: its second case expects the
loader to refuse a script that abandons a task after `pick_up` with "T-C2b" (the compatibility path of T-C2a), which
T-C2b removed. Error text:
`tests/test_script_layer.py:240: Failed: DID NOT RAISE ValueError` (at `pytest.raises(ValueError, match="T-C2b")`).
The case goes with the C1 vocabulary in T-H3, or is deleted before.
Files: tests/test_script_layer.py

**TODO-105: A resumed fetch walk toward an item the robot has delivered (recorded, T-H2, 25 Sept 2026)** [OPEN, recorded only]
The resumption rule completes the cut action first, one rule for every action type. A delivery cut during its fetch
walk, and the item delivered by the robot meanwhile: on resumption the human walks to where the item now is (the
table) and the re-expansion then finds the task complete. The rule's reason holds (no world fact about progress is
needed); the walk is for nothing. The alternative, named and not taken: judge the terminal condition before
finishing the cut action, which breaks "one rule for every action type". Revisit if a T-D scenario meets it.
Reference: design_decisions.md, "T-H: the human behaviour model", as built (T-H2), D3.

**TODO-106: The load-time replay cannot see body-derived facts (recorded, T-H2, 25 Sept 2026)** [OPEN, recorded only]
The replay advances the symbolic state by what the schemas declare (`successor_state`). Two facts of the Mesa body
are not declared: `waited(agent, entity)` is retracted by the body on the agent's next step / grasp / release
(no schema retracts it), so the replay keeps it, and a later coffee_break RESUMED before its own wait would read as
completed at load; and `at(agent, object)` is never emitted for an object the agent holds, so a walk to an item in
hand never completes in Mesa while the replay adds the effect (an authoring hazard, met in a T-H2 test). The
robot's projection has the same limitation (TODO-07's remainder). Options, not decided: declare the retraction on
the movement schemas (needs a wildcard on the entity), or a body-supplied fact filter for the replay.
Reference: world/human_executor.py, `advance()`; mesa_sim/world_state_builder.py.

**TODO-104: dock_loading's two scenarios do not load (recorded, T-H1, 25 Sept 2026)** [OPEN; domain deferred] [V1]
Both fail at load at ea4446c (before T-H1) and identically after it; the domain imports, and its tree and task model
build. Error text (current at T-L stage 3, 26 Sept 2026, under the serial ids; scenario_10 and scenario_11 before it,
`docs/rename_table.md`):
- scenario_s01_01: `scenario 'scenario_s01_01', agent 'human_0': the script cannot run as written:
  infeasible:office_break()` (recorded at T-H1 as `AdaptivePlanner: no applicable method for task 'office_break' in
  current world state. Bindings: {'?agent': 'human_0'}`; the same failure, now reported by the load-time replay)
- scenario_s01_02: `scenario 'scenario_s01_02', agent 'human_0': office_break(?office_chair=office_chair):
  ?office_chair is bound to 'office_chair' of type 'chair', but the schema requires type 'office_chair'`
Files: domains/dock_loading/scenarios/scenarios_s01.py, domains/dock_loading/tasks.py (`office_break`), its layout
(`layouts/env_layout_01.json`) and setup (`setups/env_setup_01.json`)
T-H3: the scripts were wrapped as `Script([...])` syntactically, the robots' `scheduled_tasks` too (TODO-39: they
belong in `assigned_tasks`); the domain imports; both scenarios still fail with the same two errors.
T-G build 1 (30 Sept 2026): the form-only repairs (the steps of `pick_up`, `place`, `scan_it` bind `?item`;
`confirm_delivered_pallet` typed; the layout's `office_chair` typed `office_chair`) and the viewing fixture
scenario_s01_03, which loads; both scenarios now fail at the same place, `infeasible:office_break(...)` in the
load-time replay (its `door_is_open` guard, which no body emits), their content left to T-G's design.
TWO CAUSES (T-G records 1, 1 Oct 2026; the survey of 30 Sept 2026): scenario_s01_01 fails on two causes, the door condition
(`door_is_open(office_door)`, which no body emits) and the empty binding (`office_break` bound with `{}`): with the guard
removed, the replay stops at `unbound variable '?office_chair'`. Ruled (B5, B6): the door's state is declared in the
setup; both scenarios are replaced in stage 1, the present layout and setup kept for scenario_s01_03 (B10). design_decisions.md, "T-G: the second domain's rulings", C2.

**TODO-107: The duplicate check on assigned tasks compares task instance keys (recorded, T-H3, 25 Sept 2026)**
[CLOSED, T-H4: task equality is `same_task` (same schema by identity, equal goal bindings), the duplicate check and
every other comparison of tasks read it; design_decisions.md, "T-H: the human behaviour model", as built T-H4]
`AgentConfig.__post_init__` refuses duplicate `assigned_tasks` by comparing `task_instance_key()` strings, since
`TaskInstance` is unhashable. It served the assigned tasks, not the C1 form, so T-H3 kept it; its identity is to be
settled with T-H4's task equality (whether `assigned(task)` compares the whole instance or its enumerated bindings).
Files: shared/types.py (`AgentConfig`)
Reference: design_decisions.md, "T-H: the human behaviour model", as built (T-H3)

**TODO-108: ros_sim's planner_2 reads the robot's scheduled_tasks where assigned_tasks is meant (recorded, T-H3,
26 Sept 2026)** [OPEN; ros_sim paused]
`ros_sim/framework_HRI/framework_HRI/planner_2.py` seeds its task queue from kitting scenario_10's robot
`scheduled_tasks`, which the robot never reads and which is empty (the robot's tasks are its `assigned_tasks`), so the
queue is empty. T-H3 only kept it compiling (`.scheduled_tasks.tasks()`, the list form deleted). Fix when ros_sim
resumes: read `assigned_tasks`.
Files: ros_sim/framework_HRI/framework_HRI/planner_2.py

**TODO-109: The `[rec]` stream carries no agent id (recorded, T-H4, 26 Sept 2026)** [OPEN, recorded only]
`HumanAgent` writes one `[rec] step=<n> stack=… action=… progress=… events=…` line per tick to the run's `.rec` file,
with no agent id. With two humans the lines of both interleave and cannot be told apart. No scenario has two humans.
Adding the id changes every `.rec` baseline; do it when a scenario with two humans is written. The queries are
unaffected: they run on each human's in-memory `Record`.
Files: world/record.py (`Record.line`), mesa_sim/sim_agents.py (`HumanAgent._step_stack`)
Reference: design_decisions.md, "T-H: the human behaviour model", as built T-H4

**TODO-110: Selecting scenarios by composition or scenario coverage (recorded, T-H follow-up, 26 Sept 2026)**
[OPEN, recorded only]
Batch runs and the viewer are to select scenarios by what they contain ("modelled only", "has an interruption"). Not
built. What a selector calls: `world/composition.scenario_composition(script, robot)`, which returns the scenario's
`Composition` (task classes, decisions, triggers, coverage results) and its `ScenarioCoverage`, against the
`ObservingRobot` a `SimModel` builds at load (`SimModel.observing`); `mesa_sim/list_scenarios.py` is its one reader
over the registry. Never a tag stored on `ScenarioConfig`.
Files: world/composition.py, mesa_sim/list_scenarios.py; the batch harness (TODO-47), the viewer
Reference: design_decisions.md, "T-H: the human behaviour model", as built (T-H follow-up); glossary §7
POINTER (T-L, 26 September 2026): selection runs after T-L, over the declared (layout, scenario) pairs, never the
product of artefacts; the run file and its overrides are ruling 7 of design_decisions.md, "Layouts, setups and
scenarios: the three artefacts of a run".
POINTER (6 October 2026): the program that would read the selector is now planned as the web-ui (T-viz); its stage 1a
selection panel follows the scenario's declared setup and reference layouts; selection by composition is among its
stage 2's open questions (TODO-186). design_records.md, "T-viz, the web-ui".
POINTER (Hadi, 6 October 2026, preferred, T-viz stage 1a): the scenario list of stage 1a offers a plain text filter
over the scenarios' ids and descriptions; the structured filter by composition is stage 2, [FW]. design_records.md,
"T-viz, the web-ui", 1a, HADI'S PREFERENCES, item 4.

**TODO-111: ros_sim's layout readers move to T-L's sources when ros_sim resumes (recorded, T-L, 26 Sept 2026)**
[OPEN; ros_sim paused]
T-L splits each layout JSON into a layout (the room) and a setup (the shift) and deletes the dead `"robots"` /
`"humans"` spawn entries; agent start positions live on the scenario. ros_sim reads the old single file directly and
reads those spawn entries: `planner_2.py` (`LAYOUT_PATH`, `load_layout`, `raw["robots"][0]`, `raw["humans"][0]`),
`planner_3.py` (the same, on dock_loading's layout), `world_con.py` (`ContinuousWorld`, `layout.get("robots")`,
`layout.get("humans")`), `run_continuous.py` (`LAYOUT_PATH`). When ros_sim resumes, these read the layout, the setup
and the scenario through the same loader as Mesa, together with TODO-108. T-L's stages do not touch ros_sim.
Stage 2 adds: `planner_2.py`'s `from domains.kitting.scenarios import scenario_10` stops resolving (scenarios.py is
now a package whose names live in its modules); it joins the readers above for the resume.
Stage 3 adds: the import names change again (kitting scenario_10 is `scenario_s02_01`, in
`domains/kitting/scenarios/scenarios_s02.py`; the layout files are `layouts/env_layout_KK.json`; `docs/rename_table.md`).
T-G stage 1 adds (T-G records 7, 1 Oct 2026; design_decisions.md, "T-G: the second domain's rulings", STAGE 1 PLAN
APPROVED): the rename of "zone" to "area" in the code leaves ros_sim passing the old field names
(`world_state_builder_continuous.py`: `current_zone=`, `object_zones=`, `in_zone`; `planner_2.py`: `current_zone=`), and
the carriers nothing reads (`AgentState`'s area among them) are removed; ros_sim is not touched.
Files: ros_sim/framework_HRI/framework_HRI/{planner_2,planner_3,world_con,run_continuous}.py
Reference: design_decisions.md, "Layouts, setups and scenarios: the three artefacts of a run", ruling 8; TODO-108

**TODO-112: A run file without `steps` fails with a bare KeyError (recorded, T-L stage 4, 26 Sept 2026)**
[OPEN] A headless run whose run file states no `steps`, and no `--steps` given, stops at `config["steps"]` in
`run_headless()` with `KeyError: 'steps'` instead of an error naming the run file and the missing key. Older than stage
4; recorded now because the run file is a user-facing artefact (`--run`, `docs/artefacts_user_guide.md`).
Files: mesa_sim/run_mesa.py (`run_headless`, `load_experiment`)
Reference: design_decisions.md, "Layouts, setups and scenarios", ruling 7

**TODO-113: The standing duration of `pick_up` and `place` as a schema fact (recorded, T-D Stage 1 build, 27 Sept 2026)**
[OPEN, deferred until the Projector is in scope] The adequacy test's priced standing s_exp (T-D E2) is "the Projector's
priced standing for the phase": 1 tick for `pick_up` and `place`. The schema states no duration for either action; the
Projector prices them by the body's `default_action_cost` (1.0, `mesa_sim/sim_agents.py`, "a stationary action is one
tick"), after `task_model.get_cost()` (no costs in kitting). Ruled by Hadi on the Stage 1 plan (27 Sept 2026): the
recognizer reads the same source as the Projector (the body's value, one source), not a new schema field the Projector
would not read. The standing duration of an action is a domain fact: it should become a schema fact read by both the
Projector and the recognizer (one source), which changes the Projector and so waits for a cycle that has it in scope.
Files: shared/types.py (`ActionSchema`), domains/kitting/actions.py, shared/projection.py (`build_segments`),
shared/recognizer.py (`_priced_standing`), mesa_sim/sim_agents.py
Reference: design_decisions.md, "T-D R and E", E2 and "Dependencies to verify in the build"
REVISED BY E9 (1.5 rulings, 27 Sept 2026): s_exp is the Projector's priced stationary ticks within the phase's span,
2 for `pick_up` and `place` (the walk's latency tick and the action's own); the source stays the body's
`default_action_cost` through the Projector's rule, and this TODO's schema-fact form is unchanged.

**TODO-114: `_get_step_size` falls back to 20.0 in code (recorded, T-D 1.5r, 27 Sept 2026)** [OPEN; remove when the
body is next in scope]
`mesa_sim/action_decomposer.py` `_get_step_size` returns `simulation.step_size` with an in-code fallback of 20.0 when
the key is absent, against T-A1's rule for the body's parameters to the mind (no fallback: a missing value stops the
run; `_get_min_separation`, `_get_beta`). It predates the T-D Stage 1 build, which hands the same value to the
recognizer as v (D = e/v + (s − s_exp)) besides the Projector's `assumed_speed`. `_get_seconds_per_step` beside it has
the same form (fallback 2.0; it feeds `duration_to_steps`, so s_exp of `wait_at`). No behaviour changes today: both keys
are set in `mesa_configs.yaml`.
Files: mesa_sim/action_decomposer.py (`_get_step_size`, `_get_seconds_per_step`)
Reference: T-A1 (the body supplies β and `min_separation`, no default); design_decisions.md, "T-D R and E", E2

**TODO-115: Six frozen analysis scripts import symbols the T-D Stage 1 build removed (recorded, T-D 1.5r, 27 Sept 2026)**
[OPEN, recorded only; no fix: the folders are frozen records]
The Stage 1 build (367a3a7) deleted `UNKNOWN`, `UNKNOWN_LIKELIHOOD`, `graded_unknown_likelihood`, `covered_fraction` and
the recognizer's `_unknown_likelihood`, `_completion_holds` and `_begin_episode`. These scripts use them and no longer
run at HEAD: `analysis/g1_graded_evidence/check.py` and `unit_checks.py` (`UNKNOWN_LIKELIHOOD`, `covered_fraction`),
`analysis/i4_evidence_model/check_i4.py` (`UNKNOWN_LIKELIHOOD`, the `unknown` key), `analysis/i4c_episode/check_i4c.py`
(`_begin_episode`, `UNKNOWN_LIKELIHOOD`), `analysis/i4d_fold_unknown/check_i4d.py` (`UNKNOWN_LIKELIHOOD`, the `unknown`
key) and `analysis/t1b_realization/measure.py` (`from shared.recognizer import UNKNOWN`). Three of them
(`unit_checks.py`, `check_i4c.py`, `check_i4d.py`) already failed before the build, since T-H1 (c5cd1a0) removed
`shared.domain_knowledge` and `shared.types.DomainModel`. Their READMEs record the commit they ran at.
Files: the six scripts named
Reference: design_decisions.md, "T-D R and E", R1

**TODO-116: The projector's docstring still names `unknown` (recorded, T-D 1.5r, 27 Sept 2026)** [OPEN; fix when the
projector is in scope]
`shared/projection.py` around lines 324 and 330 (the docstring of the hypothesis-resolving call): "cannot resolve
belief.most_likely (e.g. "unknown")" and "`unknown` before calling this (T8)". The `unknown` hypothesis left the
hypothesis space with R1 and the meta-planner's `none(unknown)` refusal is gone; the text is stale, the code unaffected.
Files: shared/projection.py
Reference: design_decisions.md, "T-D R and E", R1

**TODO-117: Do foreseeable hypotheses count as live after the work order? (recorded for L, T-D 1.5r, 27 Sept 2026)**
[RULED (T-D L4, 27 Sept 2026); built in L-build]
With the prior on, the hypothesis space is the assigned pool plus the foreseeable tasks. Once every assigned task is
complete, a foreseeable hypothesis still live keeps the recognizer from reading exhausted: scenario_s04_01 prior on,
`ac_switch_0` alone live at 0.992 from 327, admitted at 327, the finding adequate to 343 and unexplained from 344
(α = 0.05; `analysis/td_stage1/REPORT.md` §H case 2), while the human is idle. Whether a foreseeable hypothesis stays
live after the work order is complete is for L.
THE IRB (ruled 27 Sept 2026; corrected in IRB.2b records): its room has no AC switch, so with the prior on
the hypothesis space is the two deliveries plus `coffee_break`. The test-bed constructs this case in its two-deliveries
scenario only (`scenario_s08_01`): in the three coffee scenarios `coffee_break` is retired once `waited` holds, no
hypothesis is live after the second delivery, and the lifecycle reads exhausted (design_decisions.md, "The intention-recognition test-bed (IRB)"). Its expectations are generated from the current records; it does not resolve L.
A FACT FOR L (IRB.2b records, 27 Sept 2026): under the current completion pin a foreseeable task is recognisable once
per run. The pin retires a hypothesis for the rest of the run once its terminal completion predicate holds
(`docs/recognizer_handback.md` §1.6), although `waited(agent, machine)` itself is cleared when the agent's next
action starts; so a second coffee break in the same run has no live hypothesis.
Files: shared/recognizer.py (the live set H)
Reference: design_decisions.md, "T-D R and E", R4; `analysis/td_stage1/REPORT.md` §H
IRB (IRB.4b, 27 Sept 2026; `analysis/irb/REPORT.md`): scenario_s09_01 (as scenario_s08_01) and scenario_s09_10, prior on: `coffee_break` lone live at 0.997 after the last delivery (from 124 and from 107), its S below α on the exit walk (157 and 141), the finding unexplained from there to the end of the run, the idle human included.
RULED (T-D L4, Hadi, 27 Sept 2026; design_decisions.md, "T-D L: the belief lifecycle"): yes. Retirement lasts exactly as
long as the hypothesis's terminal fact holds, read from the world on every tick (T7's criterion); a hypothesis whose
fact stops holding re-enters the live set with the prior base and the current position as origin. `coffee_break` is
live again when `waited` clears, so the once-per-run fact above dissolves; after the work order the live set is the
foreseeable tasks in every scenario and the exit walk reads unexplained; exhausted becomes rare (scenario_s09_02 to _04,
exhausted today from 201, 191, 202). Set aside: foreseeable retirement on an exhausted assigned pool.
AMENDED (Hadi, on the L-records report, 27 Sept 2026): re-entry takes exactly 1/|H|, the incumbents keep their proportions (arithmetic C);
the criterion is T7's test, not its permanence (the pool side: TODO-128). design_decisions.md, "T-D L", L4 as amended.
BUILT (L-build, 28 Sept 2026; 2c54c4a): `coffee_break` re-enters the tick `waited` clears; after the work order the
test-bed's coffee scenarios read unexplained on the exit walk (exhausted 80 → 0 ticks each); scenario_s04_01 prior on
reads four foreseeable hypotheses live at 0.249 after its work order (`analysis/l_build/REPORT.md`).

**TODO-118: Retraction of an admitted projection when its leader turns inadequate (recorded for L, T-D 1.5c, 27 Sept 2026)**
[RULED (T-D L2 (ii), 27 Sept 2026); built in L-build]
An admitted projection outlives its leader's adequacy: the gate (G1) is asked at admission only, and D2 retains the
decision record by identity, so no trigger fires when the recorded hypothesis turns inadequate. The recognizer already
reports it (`leader_adequacy=inadequate`); the meta-planner has no event for it. Measured (1.5b, prior off):
scenario_s01_01 admitted at 143, inadequate from 159, the 31-tick hold runs to 173; scenario_s03_01 full_reorder
admitted at 131, inadequate from 139, the 89-tick hold runs to 219 and the run does not complete.
Files: shared/meta_planner.py (`evaluate_triggers`, the decision record)
Reference: `analysis/td_stage1b/REPORT.md`, D and finding 2; design_decisions.md, D2, "T-D R and E", G1
RULED (T-D L2 (ii), Hadi, 27 Sept 2026; design_decisions.md, "T-D L: the belief lifecycle"): `recognition_changed` also
fires when the hypothesis the decision was projected against leaves adequate, that hypothesis only, never a rival's
transition (the grasp flicker, scenario_s09_09 83 to 87). Admission is re-asked, G1 refuses, the decision realizes
against no human plan (P's fallback replaces the projection); re-admission through D2's entering side. The act is
retraction (glossary §4); the recognizer retracts nothing.
AMENDED (Hadi, on the L-records report, 27 Sept 2026): "leaves adequate" is adequate to inadequate (built as the state "the recorded
hypothesis is inadequate"); SUPERSEDES "(P's fallback replaces the projection)": there is no P fallback, the decision
realizes against no human plan, as below θ. `[meta-trig] … cause=retraction`. design_decisions.md, "T-D L", L2.
BUILT (L-build, 28 Sept 2026; 493c095): the two measured cases retract at the tick the leader turns inadequate:
scenario_s01_01 prior off at 159 (completion 201 → 186), scenario_s03_01 full_reorder prior off at 139 (it now completes,
world 227); 23 retractions over the 52 baseline runs (`analysis/l_build/REPORT.md`).

**TODO-119: A lone hypothesis is adequate right after a boundary with the human idle (recorded for P and G, T-D 1.5c, 27 Sept 2026)**
[CLOSED: the P part by T-D P1 and P2 (28 Sept 2026) as far as a refusal goes; the G part by T-D G, AD1 (29 Sept 2026)]
Prior off, after the human's last task the robot's own remaining item is the lone live hypothesis (belief 1.0 by
normalisation), and the idle stand leaves its walk adequate for about 16 ticks (S from 0.86 down to α) before it
turns inadequate; the gate admits it in that window (scenario_s01_01 prior off at 143 in 1.5b, a 31-tick hold). Under
the second E6 amendment (1.5c) the latency tick b + 1 is itself an observation at S = 1, so a lone hypothesis is
admitted at b + 1 on a belief of 1.0 and one priced standing tick. Whether admission should need walking evidence, or
the projection come from observation, is P's and G's.
Files: shared/meta_planner.py (`_clears_gate`), shared/recognizer.py (membership)
Reference: `analysis/td_stage1b/REPORT.md`, D, finding 3 and section 1.5c; design_decisions.md, "T-D R and E", G1
NOT RULED BY L (27 Sept 2026): its P part stays open. Under L2 (ii) such an admission is retracted once the lone
hypothesis leaves adequate (scenario_s01_01 prior off: admitted at 143, inadequate from 159; TODO-118), which bounds the
hold, not the admission. Under L4 the case widens: a foreseeable hypothesis that re-enters the live set is a lone
hypothesis after the work order in every scenario. design_decisions.md, "T-D L: the belief lifecycle".
CONSEQUENCES FOR G (L-records amendments and the L-build plan step, 27 Sept 2026, recorded, not ruled): after the work
order a lone foreseeable hypothesis is admitted at 1.0 by normalisation on the tick after the boundary (b + 1) and
retracted later wherever the robot still works. Under L5 B every human boundary that meets a recorded decision clears
the projection (no member on the boundary tick, G1 refuses): the decision on the boundary tick is unprojected and a
lone hypothesis is re-admitted at b + 1, two decisions per such boundary. A re-entering `coffee_break` still within
reach of its machine re-enters in its `wait_at` phase and is a member at S = 1 for a tick or two as the human walks
away. design_decisions.md, "T-D L", L4 and L5 as amended.
P PART CLOSED FOR REFUSALS (T-D P, ruled by Hadi, 28 Sept 2026): where admission refuses and a human is observed, the
decision realizes against the fallback projection, the short-term physical projection from the observed position and
the last displacement (P1, P2 as reopened); a candidate whose violation is cleared only by the projection's end is
refused, and with none eligible the robot waits. The lone-hypothesis admission at b + 1 is G: P leaves it, and an
admitted projection outranks the fallback.
G PART: whether that admission should stand; the rest of G's first questions are TODO-132.
design_decisions.md, "T-D P: the fallback projection".
G PART CLOSED BY AD1 (T-D G, ruled by Hadi, 29 Sept 2026): admission also requires warrant (commitment or observation
that justifies admission). A lone foreseeable hypothesis at b + 1 has no commitment warrant and no observation warrant
(its phase was opened by the boundary, not by the completion of its previous step in this episode) and is refused
until the human walks toward its target; the last assigned delivery at b + 1 is admitted as now, on commitment warrant.
To be built in G-build. design_decisions.md, "T-D G: admission".

**TODO-120: Three small flags from the 1.5b acceptance (recorded, T-D 1.5c, 27 Sept 2026)** [OPEN; documentation]
- `analysis/td_stage1/supp_sweep.sh` was committed without the executable bit (made executable in 1.5c; run it with
  `bash` at older commits).
- 1.4's `e_reveals.py` prints an `unknown` column; on logs after the Stage 1 build it reads 0.000 (no such key).
- `analysis/td_stage1b/g_priced_standing.py` shows, per action of an admitted projection, the first s_exp the
  recognizer took for it in the run, not the one in force when the projection was made (item_2 projected at 80: its
  initial walk's 0, not the post-boundary 1).
Reference: `analysis/td_stage1b/REPORT.md`, flags

**TODO-121: The 1.4 and 1.5b measurements cover the truncated interval (recorded, IRB.1r, 27 Sept 2026)** [CLOSED; IRB.2b, 27 Sept 2026]
In every run the robot stopped observing at its terminal return (`RobotAgent.finished`): the `[IR]` and `[IR-dist]`
lines end at the robot's completion, and the recognizer's output over the human's remaining behaviour is in no
baseline. The measurements of 1.4 (`analysis/td_stage1/`) and of 1.5b and 1.5c (`analysis/td_stage1b/`) were taken
over that truncated interval. Once the cognitive-loop correction is built, they are rerun over the newly exposed
interval in IRB.2b, with every change reported and no previous statistic preserved for comparability.
CLOSED (IRB.2b, 27 Sept 2026; `analysis/irb2b_exposed_interval/REPORT.md`): the scripts are rerun over the exposed
interval (the tick after the robot's declared completion to the run's end). In every baseline run that interval is the
idle human after its script: no modelled tick, boundary, pin or decision lies in it, so false unexplained (0 at every
α), non-member, adequate-below-θ, boundaries and admissions are unchanged; what moved is the output over the idle
human: exhausted ticks (+1,983 prior on) and unexplained ticks against a lone live hypothesis nothing will complete
(+50 prior on: scenario_s04_01's `ac_switch_0`, TODO-117; scenario_s06_06's wrong-table `item_0`, TODO-87). Every
moved tick lies in the exposed interval.
Files: analysis/td_stage1/, analysis/td_stage1b/ (the scripts rerun on the regenerated baselines)
Reference: design_decisions.md, "The cognitive loop does not end with the task pool"

**TODO-122: The IRB's deviation scenarios, layer 4 (recorded, IRB.1r, 27 Sept 2026)** [CLOSED; IRB.4b, 27 Sept 2026]
The test-bed's first scenarios hold modelled behaviour and the exit walk only. The deviations are authored later, with
P and X: the corner walk (`TASK_ABSENT`, the case Design B was ruled for), a switch outside the support, the wrong
table (`BINDING_ABSENT`), the long stand, the finished assigned tasks. Same rules as the test-bed's first scenarios:
the layout is not adjusted to a desired result, and the expectations are derived from the entry before the run.
Files: domains/kitting/ (scenarios), analysis/irb/
Reference: design_decisions.md, "The intention-recognition test-bed (IRB)"; TODO-101; `docs/handoff_T-D_cycle2_and_IRB.md` §8, layer 4
CLOSED (IRB.4b, 27 Sept 2026; `analysis/irb/REPORT.md`, its IRB.4b section): layer 4 built on the enlarged room (env_layout_11, env_setup_09), ahead of P and X: the corner walk (scenario_s09_05, `TASK_ABSENT`), the long stand (_06), the change of mind (_07), the wrong table (_08, `BINDING_ABSENT`), a delivery outside the support (_09, covered, outside the support); the finished assigned tasks are the exit walks of _01 and _10 (TODO-117). Zero disagreements at 1e-9 against the recognizer's public outputs.

**TODO-123: `SimModel._spawn_agents`'s docstring misdescribes the robot's pool under the prior (recorded, IRB.2b, 27 Sept 2026)** [CLOSED; G-build, 29 Sept 2026: the docstring corrected in 81a9f86, where the observed human's assigned tasks also became the meta-planner's input (commitment warrant, T-D G AD2)]
The docstring says the robot "receives its assigned_tasks as its task pool, plus (when the assignment_prior switch is
on) the observed human's assigned_tasks". The observed human's assigned tasks go to the recognizer only, as its
support restriction (`RobotAgent.__init__`, `IntentionRecognizer(assigned_tasks=observed_assigned_tasks)`); the
robot's pool is its own `assigned_tasks` (`meta_planner.seed_tasks(assigned_tasks)`), with the prior on or off. The code
is right, the text is stale.
Files: mesa_sim/sim_model.py (`_spawn_agents`)
Reference: IRB.2b plan step, 27 Sept 2026

**TODO-124: The run log prints S to four decimals (recorded, IRB close-out, 27 Sept 2026)** [OPEN; recorded only]
The `[IR]` line prints the members' tail probabilities to four decimals, so a hypothesis adequacy read from the log is
undetermined within 5·10⁻⁵ of α: scenario_s09_07 at tick 35, `coffee_break`'s S = 0.0499824 printed `0.0500` and read
from the log as adequate, where the recognizer's own output is inadequate. The in-process `BeliefState` is
authoritative; the IRB compares against it at 1e-9 and against the log at print precision only.
Files: mesa_sim/sim_agents.py (the `[IR]` line's `tails=` format); analysis/irb/actual.py (the log reader)
Reference: `analysis/irb/REPORT.md`, IRB.4b, "Disagreements, classified"

**TODO-125: tdlib.py cannot parse a `[coverage]` line with a `start:` entry (recorded, IRB close-out, 27 Sept 2026)** [OPEN; recorded only]
`analysis/td_stage1b/tdlib.py`'s `[coverage]` pattern does not match a line that carries a `start:` entry (any script
with a `Start` event), and `parse` then raises. tdlib is a frozen record and is not edited; the IRB's log reader
hands it a copy of the log without its `[coverage]` lines, which nothing there reads.
Files: analysis/td_stage1b/tdlib.py (frozen); analysis/irb/actual.py (`from_log`)
Reference: `analysis/irb/REPORT.md`, IRB.3b flags

**TODO-126: The registry inventory literal in the discovery test (recorded, IRB close-out, 27 Sept 2026)** [CLOSED, 6 October 2026: the test no longer pins a count or a set of ids]
`tests/test_tl2_discovery.py::test_the_registry_is_the_union_of_the_modules` pins the registry's inventory as literals
(the scenario count and the set of setup ids), so it must be edited with every new scenario or setup: 38 to 42 in IRB.3b,
42 to 54 and setups 01 to 09 in IRB.4b.
CLOSED (Hadi, 6 October 2026, T-viz 1a (iv)'s second part): the test now checks, for both domains, that every module's
scenarios are registered and nothing else, that no id is there twice, and that every module's setup is registered; no
count and no list of ids is pinned, so a scenario or a setup added by hand needs no edit. It also runs alone (it imports
`mesa_sim.run_config`, which puts `mesa_sim/` on the path for `mesa_fork`).
Files: tests/test_tl2_discovery.py
Reference: `analysis/irb/REPORT.md`, IRB.3b and IRB.4b, "Runs and tests that disagree with the mechanism"

**TODO-127: `d_decisions.txt`'s world completion tick equals the declared one prior off, declared − 2 prior on (recorded, L-records, 27 Sept 2026)** [RESOLVED as wording (T-D P records, 28 Sept 2026): CLAUDE.md's sentence fixed]
Flagged in IRB.2b (`analysis/irb2b_exposed_interval/REPORT.md`, flags) and not examined: for the prior-off runs
`d_decisions.txt` prints a world completion tick (`tdlib.robot_completion`, T6) equal to the declared one (scenario_s06_02
off: world 267, declared 267), where the prior-on runs read world = declared − 2 (scenario_s01_01 on: 169 / 171), the
relation CLAUDE.md states for every run. Identical before and after IRB.2b, so not IRB.2b's. Either `tdlib.robot_completion`
reads another line prior off, or the declared tick differs by prior; to be checked before a completion tick from
`analysis/td_stage1b/tdlib.py` is compared across priors (the 1.5c and IRB.2b measures rerun in L-build).
CHECKED (L-build, 28 Sept 2026; `analysis/l_build/REPORT.md`, "Completion ticks"): not a reader defect. The declared
tick equals the world tick when the pool empties on a `recognition_changed` of that tick (the robot's own item pinned
changes most_likely and `update()` drops the completed task, T7), and is world + 2 when `no_current_task` ends the pool;
prior off, the robot's remaining item is often the recorded leader, hence the pattern. CLAUDE.md's "declared = N,
world = N − 2" holds for `no_current_task` endings only (flagged, CLAUDE.md not edited). Under L2 (ii) several of these
runs now end by `no_current_task` (declared + 2, world unchanged).
RESOLVED AS WORDING (T-D P records, 28 Sept 2026): CLAUDE.md, "Regression checking", now states that the declared tick
is the world tick + 2 only when `no_current_task` ends the pool, and equals it when a `recognition_changed` of that tick
ends it.
Files: analysis/td_stage1b/tdlib.py (frozen), analysis/td_stage1b/d_decisions.py
Reference: `analysis/irb2b_exposed_interval/REPORT.md`, "Flags (not fixed)"; CLAUDE.md, "Regression checking" (completion)

**TODO-128: A moved item does not re-enter the robot's pool (recorded, L-build records, 27 Sept 2026)** [OPEN; recorded only]
The recognizer's live set uses T7's completion test on every tick, not its permanence (T-D L4): a delivery whose item
leaves its table is live again. The robot's pool keeps the permanence: `update()` drops a task complete in the world
and B3's queue rewrite persists the drop, so a task whose terminal fact later stops holding is not re-added. Whether
the pool should follow the world both ways is for later; nothing in the current scenarios moves a delivered item.
Files: shared/meta_planner.py (`update`, the pool)
Reference: design_decisions.md, "T-D L: the belief lifecycle", L4 as amended; T7

**TODO-129: A retired hypothesis whose terminal fact cannot be read on a later tick stays retired (recorded, T-D P records, 28 Sept 2026)** [OPEN; recorded only]
L-build's reading (flagged there): the live set is read from the terminal facts every tick (T-D L4), but a retired
hypothesis the planner cannot decompose on a later tick has no terminal fact to read, and stays retired. No scenario
reaches it.
Files: shared/recognizer.py (`_retired`)
Reference: `analysis/l_build/REPORT.md`, "Flags (not fixed)"; design_decisions.md, "T-D L", L4, and its BUILT paragraph

**TODO-130: The meta-planner test-bed (track 3), after X (recorded, T-D P records, 28 Sept 2026)** [CLOSED (the MPB close-out, 30 Sept 2026): sixteen scenarios verified; every materially distinct in-scope decision path verified, unreachable with a derivation, or out of coverage with a reason; objection 1 read as class 2 (a) and corrected]
REWRITTEN (MPB, ruled by Hadi, 29 Sept 2026; design_decisions.md, "The meta-planner test-bed (MPB)"): the earlier track
note and its X amendment are superseded by the entry; their content is in it.
The recognition-to-planning chain (recognizer, gate, projection, meta-planner) tested with a working robot, one authored
scenario per decision, against an oracle that states the expected decision before the run; a disagreement is
classified, never fitted. The eight scenarios (MPB-2), scenario_sNN_MM on env_setup_NN, on env_layout_12 (a second
controlled layout only where the geometry must change): (1) admission after θ, on the tick the gate clears
(`recognition_changed`, cause entered); (2) the hold against an admitted projection crossing the robot's route; (3) the
planning side of the mid-action change (scenario_s09_13's chain: retraction, the fallback, re-admission at the next
fitting phase); (4) boundary re-admission, b refused, b + 1 admitted on commitment; (5) the lone foreseeable hypothesis
after the work order, unwarranted on standing, admitted (entered) on the first warranted tick; (6) the occupied target
with an alternative task (X1's derived condition; the switch by cost); (7) the fallback against a walker and a stander
(the expiry cadence; evidence for TODO-132 (a)); (8) the control (no hold at any decision, completion identical to the
setup run without the human).
The six rulings: MPB-1, a decision's four parts (trigger and cause, gate, projection, selection); per-tick tables of
parts 1 to 3 pre-run, the (tick, cause) chain assembled at the compare step with the run's `no_current_task` ticks;
part 4 as declared properties; the oracle imports nothing of the planner, the recognizer, the projection or the robot's
perception. MPB-2, the scenarios and the environment. MPB-3, the disjointness rule (the robot's items and shelves
disjoint from the human's, checked per scenario) and the compare levels; the planner's logged values are observed inputs
to a property only. MPB-4, verification (zero disagreements on parts 1 to 3, prior on; every part-4 property), the
alteration test, five disagreement classes. MPB-5, the parked items and the comparison horizon (TODO-138). MPB-6, prior
on primary, prior off a diagnostic appendix with no exact comparison; `single_task` primary, `full_reorder` a second
run with identical tables, not identical chains.
Files: analysis/ (the MPB instrument, step 2), domains/kitting/ (env_layout_12, env_setup_10 onward, scenarios_s10.py
onward), configs/ (the run files)
MPB STEP 2 (29 Sept 2026; design_decisions.md, "The meta-planner test-bed (MPB)", BUILT IN PART; analysis/mpb/REPORT.md):
- Verified: scenarios 1 to 5 and the control, zero disagreements on parts 1 to 3 under both strategies, prior on.
- Not verified: scenarios 6 and 7 (scenario_s11_01, _02). Their human has no assigned tasks, which switches the support restriction off, so MPB-3's precondition fails (class 4; the oracle corrected, class 1).
- Open: the re-authoring of scenarios 6 and 7; the AD3 addition (not exercised); the skip rule on an arrival tick (objection 1).
MPB PART (iv) (29 Sept 2026; design_decisions.md, "The meta-planner test-bed (MPB)", BUILT): all eleven verified (zero
disagreements on parts 1 to 3, both strategies, prior on; every declared part-4 property under single_task).
- Scenarios 6 and 7 re-authored: an assigned delivery the human never performs.
- scenario_s10_07 to _09 added for coverage.
- AD3 recorded as not exercisable in the MPB set.
- The skip rule is TODO-142; the observed human with no work under the prior on is TODO-143.
THE COVERAGE MATRIX AND PART (v) (Hadi, 29 Sept 2026; design_decisions.md, "The meta-planner test-bed (MPB)", MPB-2 as
amended and NOT CLOSED; analysis/mpb/coverage.md): the eleven runs sorted into 47 decision paths, 31 verified, 5
unreachable with a derivation, 4 out of coverage with a reason, 1 reachable and not claimed (P3), 1 not a distinct
path, 5 reachable and claimed with no instance. Part (v) authors those five, one instance each: the switch against an
admitted projection; the hold against an admitted standing segment; the switch while carrying; a record kept through a
dip below θ; the cause boundary (a new layout without the coffee machine). The MPB closes when every materially distinct
in-scope decision path is verified, unreachable with a recorded derivation, or outside the claimed mechanism with a
recorded reason.
PART (v) BUILT, THE MPB CLOSED (30 Sept 2026; design_decisions.md, "The meta-planner test-bed (MPB)", PART (v) and
CLOSED; analysis/mpb/REPORT.md, "Part (v)"): scenario_s12_01 (D8), scenario_s12_02 (C2), scenario_s11_03 (D9),
scenario_s10_10 (E6), scenario_s10_11 (A4), all verified; env_layout_13, env_layout_14 and env_setup_12 authored for
them. Recorded for Hadi: three F1 robot violations in scenario_s12_01 under full_reorder inside the admission's window;
checked on the re-executed realization (analysis/mpb/REPORT.md, part (v)): reading (c), no class assigned, pending his
reading. The instrument now saves the belief and S per tick, and the projected human and planned robot segments per
admitted decision, and draws the IRB's figure per run (figure_ir.png; analysis/mpb/README.md).
Reference: design_decisions.md, "The meta-planner test-bed (MPB)"; "The intention-recognition test-bed (IRB)"; "T-D X" (X1)

**TODO-131: A robot-mind object in shared/ that owns the world model and the cognition components (recorded, T-D P, 28 Sept 2026)** [OPEN; recorded only]
PROPOSED, NOT RULED (the T-G design chat; T-G records 1, 1 Oct 2026): track 4's reduced form (T-G A8) does not need the mind object, so its
landing in track 4 below is no longer implied; its placement is open. The Mesa class `RobotAgent` still holds mind parts
and body parts together (glossary §10, **body**). design_decisions.md, "T-G: the second domain's rulings", A2, A8, PROPOSALS.
WorldState is the robot's world model, not simulator state (T-D P). Today `RobotAgent` (the Mesa body) holds the
recognizer, the meta-planner and, since P, the human's previous observed position, from which it writes
`WorldState.agent_displacements` each tick. The form to build: a robot-mind object in `shared/` owning the world model
and the cognition components, the Mesa agent as its body. Its robot-internal record stays bounded to what components
read, never a growing history: since P4 (28 Sept 2026) four numbers per observed agent, the previous position, the
previous unit direction, the run length and the standing count, from which `RobotAgent` writes
`agent_displacements`, `agent_run_lengths` and `agent_standing_counts`.
WHERE IT LANDS (recorded at the G/X handoff, 29 Sept 2026; a decision of the design chat): the perception layer and the
mind object land in track 4 (TODO-140), whose observable-area rule is their first case: the first time the robot's
world model must differ from the simulator's state.
Files: mesa_sim/sim_agents.py (`RobotAgent`), shared/ (the new object)
Reference: design_decisions.md, "T-D P: the fallback projection", mechanics

**TODO-132: G's first questions after P (recorded, T-D P, 28 Sept 2026)** [OPEN in part: (a) parked under G, to track 3; (b), (c), (d), (e) closed]
(a) The staleness of a fallback: the human stopped, turned or walked past what the fallback projected; what
observation establishes it (a departure from the projected position by `min_separation` is one candidate, not a
ruling, because `min_separation` is the body's safety constraint), and whether it is a trigger. RULED IN PART by P4 /
Q6 (28 Sept 2026): the fallback's own end is a trigger (`projection_expired`); a departure from it before its end is
still G's. (b) TODO-95's sustained
stand (the one open question TODO-95 left at its closure, Track 2.5, 29 Sept 2026: what the meta-planner does
with a sustained stand; the recognizer side is docs/assumptions.md 3.4). (c) The no-decision on a reset tick (every boundary that meets a record clears the projection, L5 B). (d)
Whether the wait's polling by `no_current_task` stands, or a staleness or reconsideration trigger replaces it (P1:
provisional until G). CLOSED by P4 / Q6: there is no wait; the robot reconsiders when the fallback it planned against
runs out (`projection_expired`). (e) Whether the lone-hypothesis admission at b + 1 stands (TODO-119's G part).
Evidence for (a) and (d), measured on the P-build baselines: a fallback can refuse every candidate while the human
walks, a consequence of P's ruling 3 (the candidate's own horizon); scenario_s05_01 under `full_reorder` waits 23
ticks from tick 0 in both priors (the ground for P4, which removes the refusal). P3 (open, design_decisions.md, "T-D P"): what the meta-planner projects when an
admitted projection reaches its horizon, the open part being a projection ending at a non-terminal action
(scenario_s05_01 prior on, tick 92: T_h 4.00, δ 0, `[sep]` 6.96 cm).
MEASURED AT (recorded at G-records, 29 Sept 2026): the P3 case was measured on the P-build baselines (fa26176) and does
not occur under P4 and Track 2.5 (verified 29 Sept 2026 at a412b39: tick 92 has no decision; the run's minimum `[sep]`
is 58.31 cm at tick 25). P3 stays parked, with no instance in the maintained sets.
G-RECORDS (T-D G, ruled by Hadi, 29 Sept 2026; design_decisions.md, "T-D G: admission"):
- (a) PARKED under G, with a candidate principle that is not a ruling: a fallback projection is warranted only while
  the evidence it was built from holds, so its expiry can occur by reaching its time horizon or by the underlying
  persistence breaking (the run length or the standing count no longer equal to k + the elapsed ticks, k derivable from
  the recorded expiry; a state reading in L2 (ii)'s form, one new trigger condition on an existing observable).
  Evidence: scenario_s05_02 prior on (42 ticks held against a 23-tick stay; completion 214, against 195 before P). To
  be decided at track 3 (TODO-130), whose oracle can state the expected decision tick before the run. Not implemented.
  MPB (29 Sept 2026; design_decisions.md, "The meta-planner test-bed (MPB)", MPB-5): scenario 7's stand records the
  re-decision ticks, the holds and the tick the persistence broke, as evidence; nothing built; the question returns
  to the design chat after the runs.
  MPB STEP 2 EVIDENCE (29 Sept 2026; analysis/mpb/REPORT.md), from scenario_s11_02, a run outside the verified domain
  (class 4: the support restriction off):
  - the stand at spot_E from 26; its persistence broke at 57;
  - the decisions on it at 32 (a stand of k = 8, projected to 41) and 41 (k = 17, projected to 59, hold 14);
  - no hold ran past the break.
  scenario_s11_01 after its switch: a hold of 23 at 33 against a stand projected to 68, the human standing until 59.
  To be re-taken on the re-authored scenario.
  SUPERSEDED (29 Sept 2026): these numbers come from scenario_s11_02 as first authored, outside the verified domain;
  the part (iv) evidence below, on the re-authored and verified scenario, replaces them.
  MPB PART (iv) EVIDENCE (29 Sept 2026; analysis/mpb/REPORT.md), scenario_s11_02 re-authored (verified), single_task:
  - the stand at spot_E from 26; its persistence broke at 57;
  - the decisions on it at 27, 31, 39 and 55 (a stand of k = 3, 7, 15, 31) sent holds of 4, 8, 16 and 32;
  - the last runs to 87, 30 ticks past the stay.
  Under full_reorder the robot was elsewhere at the stand: no hold. The question returns to the design chat.
  MPB PART (v) EVIDENCE (30 Sept 2026; analysis/mpb/REPORT.md, "Part (v)"), scenario_s12_02, both strategies: at the
  coffee break's boundary (133) the fallback stand of k = 31 is projected to 165 and sends a hold of 30; the human leaves
  the machine at 135. Recorded, not the scenario's property (Hadi's ruling 2 on part (v)).
  THE CANDIDATE'S MEASURED COST (the MPB post-(iv) records, 29 Sept 2026): under the candidate principle above (a
  fallback expires when the persistence it was built from breaks) the decision of 55 would have been re-taken when the
  stand broke at 57; as built it re-decides at the projection's end, 87. The measured cost of its absence in this
  instance is the last hold's 30 ticks past the stay (holds 4, 8, 16, 32 at 27, 31, 39, 55). A measurement, not a
  ruling.
  T-K PART 1, STEP 5 EVIDENCE (4 October 2026; analysis/kitting/mpb/tk/REPORT.md; recorded by Hadi's acceptance of
  ccode's suggestion, step 5b): scenario_s16_03, context knowledge off, single_task. At the coffee break's boundary (72)
  the decision rests on the fallback stand of the observed 31-tick stand, projected to 104, and sends a hold of 30; the
  human leaves the machine at 74, and the robot holds 25 ticks while the human walks away, until deliver_item(item_4) is
  admitted at 97 (completion 113). Both sides with context knowledge on end the stale hold at 73 by admitting the lone
  delivery (completion 89 and 90). A measurement, not a ruling.
- (b) CLOSED into X's occupied-target item (`docs/handoffs/handoff_G_X_onward.md` §5).
- (c) CLOSED as answered: L5 B refuses on the boundary tick (no hypothesis is a member there), and the decision at
  b + 1 is AD1's.
- (e) CLOSED by AD1 (TODO-119's G part).
Files: shared/meta_planner.py (`evaluate_triggers`, `_clears_gate`, `update_human_projection`)
Reference: design_decisions.md, "T-D P", consequence recorded; TODO-95, TODO-119

**TODO-133: scenario_s06_01 `single_task` prior off does not finish in 340 steps, with no wait (recorded, P-build, 28 Sept 2026)** [CLOSED (P4-build, 28 Sept 2026): no longer reproduces]
On the P-build baselines (`analysis/tb1b_two_tables/`, `analysis/tb3_full_reorder/`), env_layout_08 scenario_s06_01
`single_task` prior off completed at 265 before P and does not complete within the sweep's 340 steps after it, with no
wait logged. Prior off is an appendix; not examined.
CLOSED (P4-build, 28 Sept 2026): under P4 the run completes at 265, as before P (the P4-build sections of
`analysis/tb1b_two_tables/README.md` and `analysis/tb3_full_reorder/README.md`); the P-build behaviour behind it is
gone with the refusal it came from. Not examined further.
Files: analysis/tb1b_two_tables/sweep/, analysis/tb3_full_reorder/sweep/
Reference: design_decisions.md, "T-D P", BUILT

**TODO-134: Does L2's observation offset apply to a fallback stand? (recorded, P4-build, 28 Sept 2026)** [PARKED (T-D G records, 29 Sept 2026)]
Every human projection starts at the observation offset (L2: the observed position is true at step 1 of the robot's
projection), so the robot's first tick after a decision is unassessed against the human (T3b). For a fallback stand
the position at the decision tick is the observation itself: the human stood there and, standing, is there on the
robot's first tick too. Measured: scenario_s03_01 `single_task` (both priors) passes 30.12 cm from the standing human
at tick 171 inside that first tick (violating shifts (0.06, 53) from the offset, (−0.94, 53) from step 0). Whether the
stand should start at step 0 is the question; a design decision, not a fix.
TRACK 2.5 (29 Sept 2026): with the exit walk on scenario_s03_01 (docs/assumptions.md 1.1) the case no longer occurs in
the maintained sets (`[sep]` minimum 48.25 cm prior off, 60.15 cm prior on, single_task); the question stands.
PARKED (G-records, Hadi, 29 Sept 2026; design_decisions.md, "T-D G: admission"): to be ruled only if track 3
(TODO-130) produces an instance in scope.
MPB (29 Sept 2026; design_decisions.md, "The meta-planner test-bed (MPB)", MPB-5): no scenario authored for it; a
decision inside the gap against a fallback stand, if one occurs in MPB scenario 6 or 7, is classified and recorded.
Files: shared/projection.py (`Projector.project_fallback`), shared/realization.py (the assessed window)
Reference: design_decisions.md, "T-D P", BUILT (P4-build), the observation-offset gap; L2; T3b

**TODO-135: The near-encounter evaluation scenario: the human walks toward the robot (recorded, Track 2.5, 29 Sept 2026)** [OPEN; authored with X]
docs/assumptions.md 4.6: near-encounters (ticks with the robot–human distance below `min_separation`) are an evaluation
measure of the planner, classified per F1 (viol / stand / recede), compared between the IR planner and the no-IR
planner; scenarios in which the human walks toward the robot stay in scope as evaluation cases for the communication
question (X). To author: a scenario whose declared intent is that approach, with X.
FIRST INSTANCE (Track 2.5 baselines, `analysis/tb1a_destination/README.md`, "2.5"): scenario_s01_06, both priors,
`[sep]` 5.23 cm at 147: the human's exit walk from the table to corner_SE passes through the robot holding mid-carry at
(262, −76) on a fallback hold from 144; F1: stands and a recede, no robot violation. An instance produced by the exit
walk, not a scenario authored for it.
T-D X (29 Sept 2026; design_decisions.md, "T-D X: response", X3): the human walking toward the robot gets no planning
rule; it is an evaluation case, and this scenario is it (realization responds at the next re-decision; the interval
before it is what the near-encounter measures).
T-F (29 Sept 2026): this scenario is one row of the evaluation's scenario dimension (TODO-144).
SECOND INSTANCE (MPB part (v), 30 Sept 2026; analysis/mpb/REPORT.md, "Part (v)", class 5): scenario_s12_02, 33.61 cm at
139, one F1 robot violation (138 to 140): the human leaves the coffee machine and walks toward the robot carrying west;
the decisions rest on moving fallbacks of k = 1 and 3 (P4's recorded error). An instance produced by the scenario, not
authored for it.
THIRD INSTANCE (T-G stage 1, the milestone, 1 Oct 2026; design_decisions.md, "T-G: the second domain's rulings", STAGE 1, STEPS 6 TO 8 BUILT): scenario_s07_02 on
env_layout_04 (dock_loading), 22.53 cm at 68, ticks 66 to 69 below `min_separation`; F1 over the continuous minimum: 3
stands, 2 recedes, no robot violation. The robot, leaving the bay toward the empties, decided a hold at 63 on a fallback
(the scan admitted at 69) and stood about 95 cm from the bay's point, on the human's straight line to the bay; the
simulated human does not react to the robot. In dock_loading the case is structural: a scan becomes applicable at the
moment of delivery, so the human walks to a bay when the robot leaves it. Whether to reopen this parked case is decided
after the MPB on dock_loading, with counts from all rooms. An instance produced by the scenario, not authored for it.
FOURTH INSTANCE (T-G stage 1, the second milestone scenario, 1 Oct 2026; design_decisions.md, "T-G: the second domain's rulings", STAGE 1, THE SECOND MILESTONE SCENARIO BUILT):
scenario_s03_03, s05_03, s07_03 (dock_loading), at the end of every run: the robot's last task is a delivery, and with
an empty pool it stays at the bay; the human walks up to it for the last scan: 8.69 cm at 320 (env_layout_02), 13.41 cm
at 301 (env_layout_03), 8.11 cm at 299 (env_layout_04); 9 / 8 / 8 ticks below `min_separation` with a standing robot, 0
with a moving robot. An instance produced by the scenario, not authored for it. PROPOSAL for stage 1, NOT RULED: an
authoring convention that the robot's last assigned task is a return.
PROPOSAL CLOSED, NOT TAKEN (Hadi, 2 Oct 2026; design_decisions.md, "T-G: the second domain's rulings", THE MPB ON
DOCK_LOADING, MPB-DL4): the robot's pool is unordered and the meta-planner selects by cost, so an author cannot fix the
last task without constraining the selection. In its place the MPB on dock_loading reports, per room, the ticks below
`min_separation` with a standing robot, beside the violations with a moving robot. These counts serve Hadi's later
ruling on whether to reopen this item. Nothing is ruled on this item itself.
Files: domains/kitting/ (the scenario), analysis/tb1a_destination/sep_classes.py (the measure)
Reference: docs/assumptions.md 4.2, 4.5, 4.6; design_decisions.md, F1; TODO-96, TODO-137, TODO-144

**TODO-136: A reactive human that gives the robot space (recorded, Track 2.5, 29 Sept 2026)** [OPEN; future work]
docs/assumptions.md 4.2: the scripted human is open-loop, it does not react to the robot's motion (the Mesa human has no
avoidance; it reads only what the robot does to objects, T-H2 D3, TODO-105). Future work: a human executor that
reacts to the robot's execution, for example by giving it space. Not scheduled.
T-D X (29 Sept 2026; design_decisions.md, "T-D X: response", X5): the communication act, its channel and its effect are
future work with this reactive human; the two grounds on which communication is warranted are recorded in X5 (TODO-96).
Files: world/human_executor.py, mesa_sim/sim_agents.py (`HumanAgent`)
Reference: docs/assumptions.md 4.2; design_decisions.md, "T-H" (item 10, Alternative 1)

**TODO-137: The fallback-only control for the near-encounter comparison (recorded, Track 2.5, 29 Sept 2026)** [CLOSED (T-F part 1, 5 Oct 2026): built and measured] [V1]
docs/assumptions.md 4.6 compares the IR planner (realized cost) with the no-IR planner: plain cost (`--cost_strategy
plain`, candidates ranked without realization) and the fallback-only control (the planner realizing against the
fallback projection always, admission never). The second is no run option today (the flags: `--strategy`,
`--gate_strategy`, `--cost_strategy`, `--separation_stop`, `--assignment_prior`, `--test_level`). To build with 4.6's
evaluation.
T-D X (29 Sept 2026; design_decisions.md, "T-D X: response", X3): the walk toward the robot (TODO-135) is compared with
plain cost and this control.
MPB (29 Sept 2026; design_decisions.md, "The meta-planner test-bed (MPB)", MPB-5): an evaluation item, not built in
the meta-planner test-bed.
T-F (29 Sept 2026): the admission-off condition of the evaluation, a prerequisite of it (TODO-144).
CORRECTED (5 Oct 2026): the flags listed above are those of 29 Sept 2026; `--assignment_prior` is `--assignment_knowledge`
since T-K part 1's build, and `--context_knowledge` was added beside it.
ANSWERED (Hadi, 5 October 2026; design_decisions.md and design_records.md, "T-F part 1: the conditions human-unaware
and intention-unaware"): this control is the **intention-unaware** condition, the run option `intention_aware` off;
the gate refuses for both its callers with `none(intention_off)` (R6). Ruled with it: the **human-unaware** condition
(`human_aware` off). The build is T-F part 1's; its plan: docs/handoffs/plan_T-F_part1.md. Closed when built.
CLOSED (T-F part 1's close, 5 October 2026; design_records.md, "T-F part 1", THE CLOSE): built (stages 1 and 2) and
measured (analysis/kitting/tf1/REPORT.md, COMPARISON.md): over the fallback alone, recognition shows no difference
this set can distinguish from zero.
Files: mesa_sim/run_mesa.py (the option), shared/meta_planner.py (admission)
Reference: docs/assumptions.md 4.6; design_decisions.md, "T-D P"; TODO-135, TODO-144

**TODO-138: The horizon of runs in which the robot has work (recorded, Track 2.5, 29 Sept 2026)** [RULED for MPB runs (MPB-5, 29 Sept 2026); nothing built]
docs/assumptions.md 1.3 derives a run's step count from the human's load-time replay plus the idle margin (IRB.3b's rule)
for human-script and test-bed runs only: the replay has no term for the robot's work, which in the maintained sets ends
after the human's. The maintained sets keep their literal step counts until this is ruled. Evidence: scenario_s04_01
completes at 384 of the sweep's 400 steps under Track 2.5 (16 ticks of margin; was the occupied target before).
RULED (MPB, ruled by Hadi, 29 Sept 2026; design_decisions.md, "The meta-planner test-bed (MPB)", MPB-5), for MPB runs:
the comparison horizon is the first observed completion point (the human's script has ended and the robot's pool is
empty) plus the IRB's idle margin (30 ticks, from E5); the safety cap for the run is the derived plain-cost
horizon (the robot's pool chained along its authored order from the robot's start, plus the human's replay length,
plus the margin), not a behavioural timeout: a run that does not complete within it is classified (class 2 or 4),
never given a longer cap. No change to the run loop or the body (TODO-33 unchanged). The maintained sets keep their
literal step counts.
Files: analysis/*/sweep.sh, configs/ (run files)
Reference: docs/assumptions.md 1.3; analysis/irb/run.sh; TODO-33

**TODO-139: Align the run option's default assignment prior with docs/assumptions.md 1.4 (recorded, Track 2.5, 29 Sept 2026)** [CLOSED, T-K part 1's build, 4 Oct 2026]
CLOSED (T-K part 1's build, stages 1 and 5, b85494d and e589731): the option is `assignment_knowledge`, on by default in
`configs/experiment.yaml` and in the loader's fallback, beside `context_knowledge`, also on by default; CLAUDE.md and
docs/assumptions.md 1.4 updated. The maintained sweeps still run both settings of the assignment option.
1.4: the framework's experiments use the prior-on configuration; prior off is a diagnostic and ablation configuration.
The default of `--assignment_prior` is still off (`configs/experiment.yaml`, `assignment_prior: false`; CLAUDE.md,
"(default off)"). Not changed in Track 2.5.
RULED (T-K part 1, AM3 and AM9, Hadi, 3 Oct 2026; design_decisions.md, "T-K: context knowledge in the recognizer's belief", R3's AM3; design_records.md, "T-K"): the
option is on by default, named `assignment_knowledge`, beside a new option `context_knowledge`, also on by default. The
default change and the rename belong to T-K part 1's build, with the regression audit; this item closes there.
Files: configs/experiment.yaml, CLAUDE.md
Reference: docs/assumptions.md 1.4

**TODO-140: Track 4, the workspace boundary and human departure (recorded at the G/X handoff, 29 Sept 2026)** [OPEN; after track 3, or before it if the evaluation needs a genuine departure] [V1, reduced form]
NOTE (T-G B13, Hadi, 1 Oct 2026; design_decisions.md, "T-G: the second domain's rulings", B13): no exit from the room is
defined for dock_loading now; its script ends with the walk to the desk, the closing part (A3, Q14).
NOTE (T-G B14, Hadi and the design chat, 1 Oct 2026; design_decisions.md, "T-G: the second domain's rulings", A8): the
rule "monitored areas are fixed per layout and do not depend on where the robot is" is reopened at T-G's stage 2, with
the trigger at the human's disappearance and reappearance; stage 1 keeps full observation.
RULED, REDUCED FORM (T-G A8, Hadi, 1 Oct 2026; design_decisions.md, "T-G: the second domain's rulings", A8), [V1]: "The layout declares monitored areas. The robot's
WorldState holds the human, and facts about the human, only while the human is inside one. While no human is observed,
the recognizer does not update, no human projection exists, and the planner plans as with no human present. The
human's disappearance and its reappearance each cause a new decision. The reappearance starts a new episode from the
prior base. The human's own execution is unaffected. dock_loading's office is one unmonitored area." Monitored areas
are fixed per layout, independent of where the robot is; kitting monitors its whole room. The mind keeps no last
observed position (the log and the viewer may show it). Not taken: the last position kept and marked stale; resuming
the old belief on return; sensor-specific observation; a robot that expects the return at the office door belongs to
TODO-97.
PLACEMENT (A8, C1): its own increment after T-G's stage 2; it changes `shared/`. It supersedes the placement in the T-D
tail (the PLACEMENT REVISED line below). RULED (Hadi, 1 Oct 2026): track 4 is built before T-F; T-F may use the
unmonitored office on dock_loading, kitting's part of T-F stays without a departure (TODO-144).
CONSEQUENCES REVISED: the first case where the robot's WorldState differs from the environment's state stands (the
human outside every monitored area); "track 4 builds the perception layer and the mind object (TODO-131)" no longer
follows (a proposal, not ruled: TODO-131's note); how the new decision on disappearance and reappearance is triggered
(the trigger set has three members) is track 4's plan. NOT RULED HERE, kept for track 4's own design: `leave()`, the
exit through a door, P4's use of the boundary, the scripts' switch and its regeneration.
NEAR TERMS (glossary §10, **monitored area**, not merged): "the shared work area", "the robot's operational area", "the
outside area" and "observable" below; "the shared workspace" in docs/assumptions.md 1.1, 2.3.
PLACEMENT REVISED (Hadi's order, 30 September 2026): track 4 is in the T-D tail, after T-F and T-V (roadmap, "The plan
from T-A"); "after track 3, or before it" in the header is history. T-F runs without a genuine departure (TODO-144).
Hadi's framing (docs/handoffs/handoff_G_X_onward.md, section 7): the shared work area gets a boundary and the human can
pass through a door into an outside area (a corridor or rest area); the script's terminal task becomes `leave()`;
whether the outside area is observable is a track 4 design question (observable: the human is seen but outside the
robot's operational area; unobservable: the first genuine "no human observed", docs/assumptions.md 2.3). Principle
ruled: the robot's observation is restricted to what it can sense from its area; a human outside is an absence of
observation, never a message; departure and re-entry are emergent (observed, not observed, observed again; a returning
human has no memory in the mind). Consequences: the first case where the robot's world model must differ from the
simulator's state, so track 4 builds the perception layer and the mind object (TODO-131); P4's fallback then uses the
shared work area's boundary; the six corrected scripts and the test-bed scripts switch to `leave()`, with one
regeneration. Until then 1.1's corner walk stands.
DECLINED FOR NOW (a decision of the design chat, 29 Sept 2026): a "leave the workspace" foreseeable task as a domain
addition was proposed and declined (option (a): the exit walk stays unmodelled behaviour); revisit with track 4 or the
demonstration.
OPEN POINT (Hadi, 3 Oct 2026; design_records.md, "T-K", THE TASK RENAMED: T-K AND ITS PARTS, point 5): whether the
robot's world state still holds the terminal fact of a task that the human completed outside the monitored areas. If it
does, the robot gets a recency fact for a completion it did not observe, against AM27 and AM33.
Files: domains/kitting/ (layouts, scripts), mesa_sim/ (the body's observation), shared/ (the mind object, TODO-131)
Reference: docs/assumptions.md 1.1, 2.3; TODO-131; design_decisions.md, "T-D P" (the workspace boundary in the tail)

**TODO-141: Per-candidate holds under `full_reorder` for X5's ground (2) (recorded, T-D X records, 29 Sept 2026)** [OPEN; evaluation]
X5's ground (2) (every candidate's realized plan holds, at a decision and at the next re-decision) is read from
`single_task` logs (`[meta-cand] delta=` per candidate); `full_reorder` logs no per-candidate hold (`[meta-ord]` the
cost per head, `[meta-win]` the winner's holds only). Evaluation-time logging, not a design change.
MPB (29 Sept 2026; design_decisions.md, "The meta-planner test-bed (MPB)", MPB-5, MPB-6): an evaluation item, not built
in the meta-planner test-bed; `full_reorder` is not required to reproduce every part-4 property there.
T-F (29 Sept 2026): evaluation-time logging for the full_reorder rows of the evaluation (TODO-144).
Files: shared/meta_planner.py (`_replan_orderings`, its log lines)
Reference: design_decisions.md, "T-D X: response", X5; TODO-96, TODO-144

**TODO-142: The fallback's skip rule: what principle does it implement, and does P4 need it? (recorded, MPB part (iv), 29 Sept 2026)** [OPEN; a design question]
P2's rule, kept by P4 (`Projector.project_fallback`, `_reach`): "an object whose arrival radius contains the ray's start
is skipped (the human is leaving it)". Its stated reason does not match its activation condition. A ray leaving an
object is already excluded by the direction test (the object lies behind it), so the skip changes the fallback only
when the human moves toward an object inside its radius: an arrival or a pass-through tick, where the projected walk
then runs through the object for up to the observed run length. No decision fell on such a tick in the meta-planner
test-bed's runs, and its alteration test detects the rule's removal in none of the eleven scenarios (classified 3 under
MPB-4). Kept as built. To be ruled on an instance or a design analysis.
Files: shared/projection.py (`_reach`)
Reference: design_decisions.md, "T-D P", P4 (the dated line on the skip rule); analysis/mpb/REPORT.md

**TODO-143: An observed human with no work under the prior on (recorded, MPB part (iv), 29 Sept 2026)** [OPEN; recorded only]
The framework has no representation of an observed human with no work under the prior on. The robot is given the
human's assigned tasks, and an empty list switches the support restriction off (shared/io_contracts.md §2.1): the
diagnostic mode, with every hypothesis admissible, the robot's own items' deliveries included. Found in the MPB (part
(iii), scenarios 6 and 7 as first authored, class 4); the scenarios were re-authored with an assigned task the human
never performs. Recorded only.
NOTE (T-G stage 1, the milestone's findings, 1 Oct 2026; design_decisions.md, "T-G: the second domain's rulings", STAGE 1, STEPS 6 TO 8 BUILT): on a dock_loading fixture
with no assigned tasks for the human (the viewing fixtures), every task of the robot's task model becomes a hypothesis:
this parked case. With the restriction off, two hypotheses about empty pallets become possible: artefacts of running
without the prior (docs/assumptions.md 1.4), never a rule.
T-K: T-K part 1 rules the prior when no work task is live: it runs over the live foreseeable tasks alone
(design_decisions.md, "T-K: context knowledge in the recognizer's belief", R3).
Files: shared/recognizer.py (`_build_admissible`), mesa_sim/sim_model.py (`observed_assigned`)
Reference: design_decisions.md, "The meta-planner test-bed (MPB)", BUILT (the record line); analysis/mpb/REPORT.md

**TODO-144: T-F, the evaluation: framing (not ruled) (recorded, the MPB post-(iv) records, 29 Sept 2026)** [OPEN; a future item, after the MPB closes] [V1]
NOTE (T-G B13, Hadi, 1 Oct 2026; design_decisions.md, "T-G: the second domain's rulings", B13): the scope line on the exit
walk is a kitting statement; dock_loading's ending (the walk to the desk, its closing part) is for T-F's own design.
T-G A11 (T-G records 1, 1 Oct 2026; design_decisions.md, "T-G: the second domain's rulings", A11): a layout authored so that routes cross shows that the robot adapts when an interaction
exists; it does not show how often interactions occur. T-F varies the placement and takes no interaction rate from
crossing setups alone.
SCOPE REVISED (Hadi, 1 Oct 2026; design_decisions.md, "T-G: the second domain's rulings", A8): track 4 is built after T-G's stage 2, so before T-F. T-F
may use the unmonitored office on dock_loading (a genuine departure); kitting's part of T-F stays without a departure,
the human staying in the room and ending with the exit walk. The details belong to T-F's own design. The scope lines
below ("no genuine departure") are superseded for dock_loading.
REVISED (Hadi's order, 30 September 2026; roadmap, "The plan from T-A", T-F): T-F follows T-G; tracks kitting,
dock_loading and cross-domain; the randomised harness (TODO-47) stays in it.
- Track 3b (TODO-145) follows T-F, in the T-D tail. The line "Before the evaluation: track 3b" below is history; the
  dependency is a limitation of T-F's reading, not a prerequisite: an evaluation before 3b measures without knowing
  that the adaptive branches fire under conflict.
- The track 4 prerequisite below lapses. Scope of the evaluation set: the human stays in the room and ends with the
  exit walk to the corner (docs/assumptions.md 1.1, 2.3); no genuine departure.
A framing for Phase 5 (T-F), recorded so the evaluation starts from what the MPB established; nothing here is ruled.
- The conditions, as ablations of the decision levels:
  - admission off: the fallback-only control (the planner realizing against the fallback projection always, admission
    never; TODO-137, no run option today);
  - realization off: plain cost (`--cost_strategy plain`, candidates ranked without realization);
  - prior off: a diagnostic, never the primary set (`docs/assumptions.md` 1.4).
- The measures: the completion tick (the world tick, CLAUDE.md, "Regression checking"); the held ticks; the
  near-encounters classified by F1's classes (a robot violation, a stand, a recede; `docs/assumptions.md` 4.6); the
  separation stop off.
  ADDED (T-G stage 1, the milestone's findings, 1 Oct 2026; design_decisions.md, "T-G: the second domain's rulings", STAGE 1, STEPS 6 TO 8 BUILT): the number of ticks in
  which the human passes a standing robot closer than `min_separation`, reported separately from violations by a
  moving robot. Reason: the hold turns a closeness that would count against a moving robot into one the present
  measure does not count. Nothing added to the code for it at the milestone.
- The scenario dimension: deviation kinds (a change of mind, a mid-action change, a sudden stand, a misdelivery, an
  occupied target, the walk toward the robot of TODO-135, ...) and the points in the task where they occur, with several
  instances per kind. A row is a condition and a kind. Layouts vary independently where geometry is a factor.
- What makes the numbers attributable: the MPB's verified chains (design_decisions.md, "The meta-planner test-bed
  (MPB)"; analysis/mpb/coverage.md). A difference between conditions can be traced to a decision path the MPB verified,
  not inferred from the outcome.
- Prerequisites: TODO-137 built; TODO-135's scenario authored; the evaluation set authored; MPB-5's horizon applied to
  the evaluation runs (TODO-138); the track 4 decision (TODO-140), whether the evaluation needs a genuine departure.
- The during form (the MPB close-out, 30 Sept 2026): a mid-action deviation is authored today in the absolute form
  (`during(action, "PTnS", ...)`, a stated physical time into the action). The relative form (a fraction of the replayed
  action, resolved at load time against the load-time replay and exported absolute) is the candidate when the evaluation
  set is authored, so that one deviation kind lands at comparable points across instances; an authoring-method question,
  first taken up in track 3b (TODO-145), not ruled.
- OPEN ITEM (the design chat of T-K part 1, 3 Oct 2026; NOT RULED; design_records.md, "T-K", CONTENT
  POINTS 1 AND 2, NOT RULED): the time-scale convention for the evaluation. Hadi's idea: a work day (8:00 to 16:00)
  scaled to a fixed number of steps, one factor used wherever a scale is needed; walking stays physical. The chat's
  finding: motion is not compressed, so every scheduled duration must stay longer than a task; 8 hours in 800 ticks
  does not satisfy this. Two clocks: the motion clock (2 seconds per tick) and a compressed schedule clock. Not
  decided. Related: `docs/assumptions.md` 6.3 (the declared durations are at a compressed demonstration scale).
  ADDED (Hadi, 3 October 2026; design_records.md, "T-K", CONTENT POINT 3, THE TESTS, KT6; no value changed): the
  recency duration of 90 ticks (coffee_break, T-K AM16) was derived from the wait, which is compressed, while walking
  is not; in env_layout_15 to _17 the walk from the coffee machine to the table and back takes about 84 to 94 ticks.
- Before the evaluation: track 3b (TODO-145), consequential activation under conflict.
NOTE (T-F part 1, Hadi, 5 October 2026; design_records.md, "T-F part 1: the conditions human-unaware and
intention-unaware", R1, R8, R10): T-F part 1 builds the conditions human-unaware and intention-unaware now (admission
off above is intention-unaware, TODO-137); the rest of T-F keeps its place after T-G. Realization off (`--cost_strategy
plain`): the human-unaware condition covers its comparison (the same behaviour in the verification's two runs; plain
differs by construction, re-deciding at triggers whose results it ignores); `plain` stays untouched, is not a column
of T-F part 1's measurement, and keeping or retiring it is ruled with T-F.
NOTE (T-F part 2, Hadi, 5 October 2026; design_records.md, "T-F part 1", J): `full_reorder` becomes the default
strategy of the evaluation's runs; strategy a second dimension of the result table (I); the human-unaware condition
then needs its own reference run per strategy; TODO-141 applies.
Files: analysis/ (the evaluation), domains/kitting/ (the evaluation set), mesa_sim/run_mesa.py (TODO-137's option)
Reference: docs/assumptions.md 1.4, 4.6; design_decisions.md, "The meta-planner test-bed (MPB)", F1; TODO-47,
TODO-135, TODO-137, TODO-138, TODO-140, TODO-141

**T-D OPENING AGENDA, from the T-C2c play** (`analysis/tc2c_scripts/play.md`; recorded 23 September 2026)
1. The robot is blind after every human task completion: TODO-85 (b), its general form (scenario_s05_03, 0.78 cm).
2. Re-recognition inside an episode depends on the length of the misleading walk: TODO-94.
3. Reproduced: TODO-93 (a foreseeable completion ends the episode mid-delivery) and TODO-87 (a delivery to another
   table: no pin, no boundary, a projection of a task the human will not do).
4. T-D's blocked fixture uses a stay that ends (TODO-80; the scenario-authoring convention).
5. At the recognizer pass (T-D Q2 to Q4): raise TODO-95 (stationarity channel) and rule whether it joins the pass or
   stays recorded for T-H.
PART 1 CLOSED (5 October 2026; design_records.md, "T-F part 1", THE CLOSE): the conditions human-unaware and
intention-unaware built (TODO-137) and measured on 128 kitting scenarios under `single_task` (analysis/kitting/tf1/
REPORT.md, COMPARISON.md): planning against the observed human removes violation ticks (137 → 14) at a mean delay of
+5.83 ticks; recognition, and context knowledge with no timeline fact in force (the prior alone), show no difference
this set can distinguish from zero. T-F part 2
parked; its notes (full_reorder the default strategy, strategy a column of the same result table, J; no setting in a
name, K): docs/handoffs/handoff_T-F_part1.md.
With a timeline fact in force (the last step's part 1, 5 October 2026; COMPARISON.md): a fact in accord with the
human's task speeds its admission (52 of 66 stretches earlier), one not in accord delays it (70 of 119 later); completion
and violations change little. Not ruled.

**TODO-145: Track 3b: consequential activation under conflict (not ruled) (recorded, the MPB close-out, 30 Sept 2026)** [OPEN; after the MPB, before T-F] [V1]
[V1] (T-G A1, T-G records 1, 1 Oct 2026): in V1. design_decisions.md, "T-G: the second domain's rulings", A1.
PLACEMENT REVISED (Hadi's order, 30 September 2026): track 3b is in the T-D tail, after T-F and T-V (roadmap, "The
plan from T-A"); "before T-F" in the header and the "Placed before T-F" line below are history. The dependency is
recorded as a limitation of T-F's reading (TODO-144), not as a prerequisite: an evaluation before 3b measures without
knowing that the adaptive branches fire under conflict.
Framing recorded at the close of the meta-planner test-bed; nothing here is ruled.
- Purpose. The MPB established structural branch reachability and execution of the recognition-to-planning chain, not
  consequential activation of those branches under human-robot interaction conflict. Track 3b shows that when a recognized
  deviation produces a projection that changes a planner quantity, the adaptive branch activates.
- The causal chain, per cell: a human deviation; a recognition change; a changed projection; the projection intersects or
  constrains the robot's plan; a changed realized consequence; the adaptive decision.
- The closure criterion: one consequential instance per materially distinct adaptive branch:
  - B2 continue with a hold;
  - a B3 switch;
  - a hold with no alternative;
  - re-selection after a retraction.
  The deviation kind is chosen as the mechanism that produces the conflict, not crossed exhaustively with the branches.
- "Conflict" is defined by the planner's own quantities, not by proximity: a separation constraint, a hold cost, an
  occupied target, a changed completion, an alternative's cost, a plan that cannot execute.
- Environments: a minimal isolated room per cell, with a separated twin as the control. The twin has the same deviation
  and recognition chain with the consequence removed (delta = 0), so the activation is attributable to the conflict.
  MPB-2's layout-and-setup rule and MPB-4's disagreement classes (with its three readings of class 2 and the loop) carry
  over.
- The instrument: the MPB's, reused. Parts 1 to 3 exact; the adaptation as the declared property; F1's classes measured;
  the separation stop off. The saved segments (projected human, planned robot, per admitted decision) keep the invariant
  checkable read-only.
- Authoring method, a question inside 3b: the relative during form (a fraction of the replayed action, resolved at load
  time, exported absolute; TODO-144's during line).
- Prerequisites: the MPB closed, and the invariant fixed (the trajectory realize() assesses is the one executed; the
  class-2 correction, 30 Sept 2026). Both met at this session's close.
- Placed before T-F. Reason: an environment that gives IR nothing to influence makes IR look irrelevant; the evaluation's
  numbers are attributable only where the consequence under conflict has been shown to activate.
NOTED (T-G stage 1, the second milestone scenario, 1 Oct 2026; design_decisions.md, "T-G: the second domain's rulings", STAGE 1, THE SECOND MILESTONE SCENARIO BUILT): scenario_s05_03 on
env_layout_03 (dock_loading), tick 64: a B3 switch decided on the fallback projection while the gate refuses (below
theta). At 60 the three candidates lay within 0.6 and `load_return` won; at 64 the fallback (the human walking straight
toward the robot) charged `load_return` a shift of 4 and `deliver_pallet(pallet_0)` won, 94.68 against 97.46. The
conflict enters the cost and decides the choice; consistent with the design. An instance produced by a scenario, not a
3b cell; nothing is ruled.
Files: domains/kitting/ (the rooms, setups and scenarios), analysis/ (the instrument, reused from analysis/mpb/)
Reference: design_decisions.md, "The meta-planner test-bed (MPB)" (CLOSED; MPB-2, MPB-4); TODO-130, TODO-144

**TODO-146: The human projection's stationary accounting and rounding: should it resume from the recognized phase? (recorded, the MPB class-2 finding, 30 Sept 2026)** [OPEN; a P-side residual, out of scope of the class-2 correction]
The robot's projection now starts from what its body reports (ExecutorState.owed_completion_ticks, action_in_flight);
the human's projection still re-decomposes the admitted hypothesis from the live world (Projector.project_human), which
the robot cannot correct by a report: it sees no executor cursor of the human. Measured on the MPB's saved segments
(analysis/mpb/, `human_segments`, prior on):
- rounding: the projected walk ends at the arrival radius, the body's last discrete step up to a step beyond it; the
  human's projection runs 0.17 to 0.25 tick ahead at a walk's start (scenario_s12_01 at 26: 3.4 cm on every tick of the
  carry, the projected carry starting at step 5.914 against the body's first carry step on tick 32);
- one tick early at a decision falling on the human's own walk-acknowledgement tick (+1; scenario_s10_01, s10_04,
  s10_05, s10_06 at 29, and one more), the analogue of the robot's state (a): the completed walk re-decomposed and its
  acknowledgement re-priced;
- one −0.96 (scenario_s10_03 at 164).
The question: whether the human projection should resume from the recognized phase (the observed cursor: the phase
advance E8 reads, the expected action the recognizer derives) instead of re-decomposing from the live world. Not the
cause of the class-2 violations (the cross-pairing: the planned robot against the actual human keeps F1). Not built.
T-K PART 1, STEP 5 MEASUREMENT, AT A TURN (4 October 2026; analysis/kitting/mpb/tk/REPORT.md, "What surprised";
recorded by Hadi's acceptance of ccode's suggestion, step 5b): scenario_s16_01 and _02, context knowledge on,
single_task, the human's turn at shelf_4. The admitted plan has the human stop at the arrival radius (145, -420) and
leave at 47.1; the executed human walks on to (148, -438) and leaves at 48: about one tick and 18 cm on the human's side,
with about 11 cm on the robot's (step quantisation). The planned minimum of 54.8 cm (s16_01) and 51.0 cm (s16_02)
became an executed 41.7 cm and 29.3 cm, below min_separation (F1 violations at 49, 50 and at 48, 49).
Files: shared/projection.py (project_human), shared/meta_planner.py (update_human_projection)
Reference: design_decisions.md, "The meta-planner test-bed (MPB)", MPB-4's class-2 record; TODO-77; T-D R and E (E8, E9)

**TODO-147: Shared work between the human and the robot (recorded, T-G records 1, 1 Oct 2026)** [FW]
NOTE (T-G Q13a, Hadi, 1 Oct 2026; design_decisions.md, "T-G: the second domain's rulings", A3): an entry whose task ends
INFEASIBLE is closed and not reopened by a later applicable state; no V1 ruling produces the case. This item reopens
that question if it produces a case (the other agent's task stopping being applicable during its execution).
A conceptual direction (T-G A10). The Q1 template (A3: assignment static, availability and order dynamic) makes a task
assigned to both agents expressible; each agent's applicable set shrinks when the other takes or delivers the object.
To design first: both agents choose the same object in the same interval; one picks it up; the other's task stops being
applicable during its execution: what that agent does; what the robot believes in that interval; whether the robot
avoids a task the human is recognized to pursue. Smallest instance: the human opening the gate unasked, or supporting
single steps of a delivery.
Files: world/ (the human's executor), shared/ (the recognizer, the meta-planner), domains/ (a task assigned to both)
Reference: design_decisions.md, "T-G: the second domain's rulings", A3, A10; docs/assumptions.md 2.2; TODO-15,
TODO-105; DESIGN-04

**TODO-148: A human that chooses its own tasks (recorded, T-G records 1, 1 Oct 2026)** [FW]
NOTE (T-G Q12, Hadi, 1 Oct 2026; design_decisions.md, "T-G: the second domain's rulings", A3): a retry of a dropped task
by rule (a choice rule of the human that no author wrote) is not taken for V1 and is named as this item's direction; in
V1 a retry exists only as a second authored entry of that task.
A conceptual direction (T-G A10): a human planner in place of the author's priority list. It supplies the choice at the
one isolated point of the human's executor that A3 requires in V1 (the point a live user supplies in T-V track 2).
Files: world/ (the human's executor)
Reference: design_decisions.md, "T-G: the second domain's rulings", A3, A10; roadmap, T-V track 2

**TODO-149: The robot modelling a human who waits for the robot's own action (recorded, T-G records 1, 1 Oct 2026)** [FW]
A conceptual direction (T-G A10): Q3's alternative M3. Under A4 a human-task hypothesis with no applicable method leaves
the live set; a model of the human waiting for what the robot will do next is not in V1.
Files: shared/recognizer.py
Reference: design_decisions.md, "T-G: the second domain's rulings", A4, A10

**TODO-150: Several observed humans (recorded, T-G records 1, 1 Oct 2026)** [FW]
A conceptual direction (T-G A10): a passing colleague, a colleague talking to the observed human. docs/assumptions.md 5.2
allows one observed human for the current contribution.
Files: mesa_sim/world_state_builder.py (one observed human per robot), shared/ (the recognizer, the projection)
Reference: design_decisions.md, "T-G: the second domain's rulings", A10; docs/assumptions.md 5.2

**TODO-151: Two generic load checks in shared/ let malformed input through (recorded, T-G records 1, 1 Oct 2026)** [PROPOSED by the design chat, not ruled]
Found by ccode's dock_loading survey (30 Sept 2026); generic, not domain-specific. (1) `check_task_bindings` accepts a
binding of a variable the schema does not declare and does not require every parameter to be bound, so
scenario_s01_02's `?delivery_bay` on `confirm_delivered_pallet` surfaced late, with a misleading message. (2) The `Tree`
constructor does not check that a step's binding keys are the parameters of the action it calls, so dock_loading's
`{?pallet: ...}` steps (before build 1) surfaced at decomposition. A proposal; untagged until Hadi rules it.
PARKED HERE (records, 1 Oct 2026; T-G stage 1, step 4): a setup entry that still carries the old per-object state
fields (`is_empty`, `is_scanned`) is ignored for those fields, not refused: an authoring risk of the same kind (malformed
input let through). Step 4 was not widened. design_decisions.md, "T-G: the second domain's rulings", STAGE 1, STEPS 0 TO
5 BUILT, notes.
Files: shared/types.py (`check_task_bindings`), shared/knowledge.py (`Tree`)
Reference: design_decisions.md, "T-G: the second domain's rulings", PROPOSALS; TODO-25, TODO-104

**TODO-152: A robot task with no applicable method stops the run (recorded, T-G records 7, 1 Oct 2026)** [OPEN; a ruling before T-G stage 2] [V1]
Found by T-G stage 1's plan (approved by Hadi, 1 Oct 2026). `MetaPlanner.update()` judges every task of the pool through
`_is_complete` (`AdaptivePlanner.is_complete`, which decomposes it), and projects candidates through the planner; a task
with no applicable method raises `DecompositionError`, which nothing catches, and the run stops. Stage 1 cannot reach it:
every robot task has a method for every area the robot can be in, and the gate is open (B11 as amended). Stage 2 reaches
it: the robot at a closed gate has no applicable task and stands (B5). A ruling is needed before stage 2's build. The
case was first cited under TODO-30, which concerns realizability (corrected).
Files: shared/meta_planner.py (`update`, `_is_complete`, `_replan_tasks`, `_replan_orderings`), shared/projection.py
Reference: design_decisions.md, "T-G: the second domain's rulings", B5, B11 (AMENDED), C4, STAGE 1 PLAN APPROVED;
docs/handoffs/plan_T-G_stage1.md, section 5
TAGGED [V1] (records, 1 Oct 2026): it must be ruled before stage 2.

**TODO-153: The remaining "zone" wording, for the sweep of old terms at stage 1's close (recorded, records after T-G stage 1 step 5, 1 Oct 2026)** [V1] [CLOSED, 2 Oct 2026: swept; what remains below]
TAGGED [V1] (Hadi, 2 October 2026; T-G records 15; design_decisions.md, "T-G: the second domain's rulings", T-G STAGE 1
CLOSED). The sweep is deferred to one housekeeping step with the sizes of the files under docs/ and what of
analysis/ stays in git; not done at stage 1's close.
The rename (T-G stage 1, step 1, 8d064ca) changed the code names; "zone" remains in wording. Listed once here, measured
at 576f2b2 over the tracked files outside `ros_sim/`, `scripts/`, `analysis/` and the personal files. Occurrences
(case-insensitive) per file:
CORRECTED (2 October 2026, the housekeeping step): the numbers below count lines that contain "zone", not occurrences.
- Records: docs/design_decisions.md 59, docs/TODOS_AND_DEFERRED.md 33, docs/handoffs/plan_T-G_stage1.md 9,
  docs/roadmap.md 8, docs/glossary.md 6, shared/io_contracts.md 6, docs/recognizer_handback.md 4, CLAUDE.md 4,
  docs/handoffs/handoff_T-G_stage1_onward.md 2, domains/README.md 1 (the area-id convention `zone_<descriptor>`). Much
  of it is history (I2's zone context, ZONE_BOOST, the rename's own records), which stays as written.
- Comments and docstrings: mesa_sim/viz/space_drawer.py 14 (the colour keys `zone_NW` ... `zone_office`, keyed by area
  id; the viewer is T-V's), domains/kitting/actions.py 11 (the commented-out `goto_zone`), shared/types.py 7 (examples
  `Const('zone_SE')`, `goto_zone`, `movement_target_type` "zone", `GOTO_ZONE`), shared/projection.py 2 (the zone movement
  target removed from the live domain), tests/test_tg_areas.py 3 (kitting's area ids).
  NOTE (T-G stage 1, step 8, 52b2aae, 1 Oct 2026): the viewer's six old dock_loading colour keys (`zone_hall_dry` ...
  `zone_office`) are replaced by the three area ids; kitting's four keys (`zone_NW` ...) stay, as its area ids do.
- Scenario descriptions quoting old values: domains/kitting/scenarios/scenarios_s01.py 1, scenarios_s03.py 2 (ZONE_BOOST,
  `zone_SW`).
- Not wording: kitting's area ids (`zone_NW`, `zone_SE`, ...) in its layouts stay (the plan's answer 3); dock_loading's
  change in step 6. `ros_sim/` keeps the old field names (TODO-111's note). Four frozen analysis scripts need the old
  field names and no longer run (design_decisions.md, "T-G: the second domain's rulings", STAGE 1, STEPS 0 TO 5 BUILT,
  notes); frozen records are not edited.
Files: as listed
Reference: design_decisions.md, "T-G: the second domain's rulings", A2 (the rename), STAGE 1 PLAN APPROVED;
CLOSED (Hadi, 2 October 2026; the housekeeping step after T-G stage 1's close): the sweep is done in the files listed
above. "zone" became "area" where the word names the concept as it is today: CLAUDE.md's predicate invariant
(`in_area(agent, area)`, `at(agent, area)`), design_decisions.md's "WorldState is symbolic", the two-pass loading note and
the body of "Interference is geometric, not zone-based" with its summary line, roadmap.md's interference line,
glossary.md's layout entry, shared/io_contracts.md's two interference notes. Left as written: area ids and code names
(kitting's `zone_NW` ... in its layouts, the viewer's keys, the examples in shared/types.py and the tests), removed code
names quoted in history (`ZONE_BOOST`, `spatial_zones`, `goto_zone`, `GOTO_ZONE`, `object_zones`, `_get_target_zone`),
the movement-target literal "zone" and projection.py's runtime message, the records of the rename itself, dated
entries, the scenario descriptions (printed at load), the vendored mesa_fork ("timezone"), ros_sim/ and analysis/.
What remains, not wording: the entry title "Interference is geometric, not zone-based" and its quotations are kept as
the entry's name; three undated passages of design_decisions.md ("Two distinct predicate families in WorldState", the
`object_zones` line of "WorldState carries object positions" and its "recognizer.py (chord target, zone)") state that
the recognizer reads zones, which is no longer true since I4; a word swap would make them read as current, so they are
left for a records correction by Hadi.
docs/handoffs/plan_T-G_stage1.md, section 1

**TODO-154: The robot does not anticipate the scan its own delivery makes applicable (recorded, T-G stage 1 milestone, 1 Oct 2026)** [CANDIDATE FINDING about the mind; NOT RULED] [V1]
TAGGED [V1] (Hadi, 2 October 2026; T-G records 15; design_decisions.md, "T-G: the second domain's rulings", T-G STAGE 1
CLOSED).
The robot's own delivery makes the human's scan of that pallet applicable (the guard `obj_at(?pallet, ?delivery_bay)`),
and the robot does not anticipate the human's walk to that bay: the scan hypothesis enters the live set at the tick of
delivery (A4, `[IR-reentry] ... live again: applicable`) at an equal share, and is admitted 8 to 12 ticks after the
human starts (the milestone: 64 to 72 on env_layout_02, 64 to 76 on env_layout_03, 57 to 69 on env_layout_04). Until
then the robot plans against the fallback; on env_layout_04 this interval holds the near-encounter of TODO-135's third
instance. Recorded only; nothing is changed for it.
EVIDENCE (T-G stage 1, the second milestone scenario, 1 Oct 2026; design_decisions.md, "T-G: the second domain's rulings", STAGE 1, THE SECOND MILESTONE SCENARIO BUILT): each scan hypothesis
enters the live set on the tick of its delivery in all three rooms; entry to admission, env_layout_02 64 to 72 and 182
to 188; env_layout_03 58 to 65 and 159 to 173; env_layout_04 57 to 76 and 148 to 160. The scan at the frozen bay is late
where the coffee machine lies in the same direction from the standby place: env_layout_04, admitted 19 ticks after it
enters; env_layout_02, leading 19 ticks after it enters (308) and clearing theta at 315. The last scan of each run is
never admitted: an empty pool gives no further decision (noted, no action).
NOTE (Hadi, 1 Oct 2026; T-G records 8; design_decisions.md, "T-G: the second domain's rulings", C1, T-K PART 1): an
enabling event, such as the robot's own delivery, is one of four determinants recorded for T-K part 1's design question,
NOT RULED: what sets a hypothesis's share at the start of an episode (the assignment, which exists; context facts; the
task that just ended, a transition prior between tasks; an enabling event). They are designed as one mechanism.
BASELINE (records, 2 October 2026; T-G records 9; design_decisions.md, "T-G: the second domain's rulings", STAGE 1, THE IRB ON DOCK_LOADING BUILT, RUN AND ACCEPTED), a finding about the mind, NOT RULED: a short walk gives too
little evidence under equal shares at the start of an episode. Over the 54 runs of the IRB on dock_loading, 98
of the 147 true stretches in the support reach the threshold (38, 40, 20 of 49 by room), median 20 ticks (range 6 to
50; one tick is 2 seconds); of the 49 that never do, all scans, 34 last 26 ticks or fewer (on env_layout_04, 16 steps
from the standby place to the dry bay, scan 0's first walk never reaches it with three or more rivals live). It joins
T-K part 1's question on what sets a hypothesis's share at the start of an episode as its measured baseline (the per-row
table: the T-G block named above).
RULED (T-K part 1, Hadi, 2 Oct 2026; design_decisions.md, "T-K: context knowledge in the recognizer's
belief", R2 to R4), on the four determinants: the assignment and context facts set the prior (R3); the share is
divided equally inside assigned work (R4); the task that just ended (succession) is open, an item of T-K part 2 after
T-G stage 2 (R4); a preference for a task that has just become applicable, the enabling event of this item, is not
taken and is not future work (R4: no defensible meaning or magnitude). Not built.
T-K: its prior part is ruled in T-K (the RULED line above), and its baseline is re-measured in T-K part 1.
Files: shared/recognizer.py, shared/meta_planner.py (no change)
Reference: design_decisions.md, "T-G: the second domain's rulings", STAGE 1, STEPS 6 TO 8 BUILT; TODO-135, TODO-155

**TODO-155: Hypotheses for the walks to the standby place and to the desk (recorded, T-G stage 1 milestone, 1 Oct 2026)** [PARKED; NOT RULED; now with evidence] [RULED FOR NOW, 1 Oct 2026 (T-G Q16): no hypothesis; H1 and H2 recorded, neither approved] [V1]
TAGGED [V1] (Hadi, 2 October 2026; T-G records 15; design_decisions.md, "T-G: the second domain's rulings", T-G STAGE 1
CLOSED).
Whether the robot's mind holds hypotheses for the human's walk to the standby place (the repeatable entry) and to the
desk (the closing part). Neither is in the robot's task model (the plan's section 5: a scenario with a standby entry is
classed as containing unmodelled behaviour). The approval parked the related question of the human stepping aside
(STAGE 1 PLAN APPROVED, notes). Evidence from the milestone: during the stay at the standby place the live set holds
the two breaks only, the finding turns unexplained after 15 ticks and the robot plans against the fallback; during the
walk to the desk the walk is read as the nearest modelled task, and on env_layout_02 admitted as coffee_break at 112
(the half-plane test, TODO-140); no consequence in those runs. Not ruled.
EVIDENCE AND PLACEMENT (T-G stage 1, the second milestone scenario, 1 Oct 2026; design_decisions.md, "T-G: the second domain's rulings", STAGE 1, THE SECOND MILESTONE SCENARIO BUILT): five of the
six walks to the standby place are admitted as coffee_break or office_break on the observation warrant, wrongly
(env_layout_02 at 114 and 231; env_layout_03 at 109 and 206; env_layout_04 at 94; the sixth never clears theta); the
finding turns unexplained once the human stands. In this domain the walk follows almost every scan, so the case is
frequent. It becomes the first design question before the IRB set on dock_loading. NOT RULED.
RULED FOR NOW (Hadi, 1 Oct 2026; T-G Q16; design_decisions.md, "T-G: the second domain's rulings", T-G Q16's block,
RULED, T-G records 8): the walk to the standby place stays without a hypothesis for now. The IRB set observes how
the present recognizer explains it; that is the baseline. Two candidates are recorded here, neither approved for
building:
- H1: a foreseeable task "the human steps aside to the standby place", always possible, with the standby place as a
  fixed object.
- H2: a hypothesis that is live only while no assigned task of the human is applicable.
The difference: the human steps aside only when no other pallet is applicable, so H1 states an unconditional behaviour
that the human does not perform, and competes with the scans when a pallet waits; H2 matches the condition and changes
the rule for the live set (A4).
Not taken: the walk as the tail of the scan task. Reasons: the human would step aside after every scan, also when a
pallet waits; the condition "no other pallet waits" cannot be stated in a method; the scan's terminal fact would hold in
the middle of the task.
In the IRB set the standby walks (C13, C14, M4) are diagnostic observations: beside the expectation under the
present model, the predictions under H1 and under H2 are written down before the run; only the present model's
expectation is compared with the run.
CORRECTED (Hadi, 1 October 2026, at the approval of the IRB's build; recorded 2 October 2026, T-G records 9): H2
is worded "a hypothesis live only while no assigned task of the human is live" (a scanned pallet's scan stays
applicable, its guards not reading is_scanned). NOTE (the same records): H1, an always-possible standby task, as a walk
only would make move_to a terminal action and every arrival an episode boundary (L1); a wait at its end avoids that.
EVIDENCE (records, 2 October 2026; T-G records 9; design_decisions.md, "T-G: the second domain's rulings", STAGE 1, THE IRB ON DOCK_LOADING BUILT, RUN AND ACCEPTED; analysis/dock_loading/irb/predictions.md, written
before the runs), a finding about the mind, NOT RULED: the actual readings equal the present model's expectation in all
nine runs.
- C13 (from the dry bay) and C14 (from the frozen bay): the walk is admitted as a break in five of six runs, by the
  room's bearings: coffee_break on env_layout_02 in C13 (gate clears 50 to 70) and env_layout_03 in C14 (51 to 66);
  office_break on env_layout_03 in C13 (46 to 56), env_layout_02 in C14 (38 to 56) and env_layout_04 in C14 (37 to 58);
  never above θ in C13 on env_layout_04. The finding turns unexplained once the human stands; the scan of pallet_4
  never enters the live set (A4).
- M4: on env_layout_02 the walk is admitted as the scan of pallet_0 (gate clears 167 to 182), an assigned task the
  human never performs and that stays live with its commitment warrant; on env_layout_03 read as it, never above θ; on
  env_layout_04 as office_break (143 to 156).
- The predictions written before the runs: H1 leads the walk at zero excess, clears it and is pinned on arrival, in
  every row; H2 (no assigned task live) is live from the scan's pin in C13 and C14 and reads the walk as H1, and is
  never live in M4 (scan 0 live to the end), so its prediction there equals the present model's. C13 and C14 separate
  the conditional candidate from the present model; M4 does not.
NOTE (T-G records 8, not a ruling): Q16 concerns the walk to the standby place; the walk to the desk, this item's second
walk, is not ruled by it (B13's note: the desk is a landmark in stage 1, so no hypothesis, as for kitting's exit walk).
Related, for T-K part 1, NOT RULED: what sets a hypothesis's share at the start of an episode (the assignment, context
facts, the task that just ended, an enabling event; one mechanism); design_decisions.md, C1, T-K PART 1.
NOT TAKEN FOR T-K PART 1 (T-K part 1, R3, Hadi, 2 Oct 2026; design_decisions.md, "T-K: context knowledge in
the recognizer's belief"), recorded here: a share of the prior for "none of the modelled tasks". When no assigned task
is live the prior is normalised over the live foreseeable tasks alone and is conditional on one of them. Such a share
would reopen T-D R1 (no residual hypothesis).
T-K: the prior part of this item is ruled in T-K (the line above, R3); the hypotheses for the two walks (H1, H2) stay
with this item.
Files: domains/dock_loading/tasks.py (the task model), shared/recognizer.py
Reference: design_decisions.md, "T-G: the second domain's rulings", STAGE 1, STEPS 6 TO 8 BUILT; docs/handoffs/plan_T-G_stage1.md, section 5; TODO-140, TODO-154

**TODO-156: Route selection in dock_loading's robot methods: a design question for stage 2 (recorded, the review of the task file, 1 Oct 2026)** [OPEN; to rule before `store_pallet`] [V1]
TAGGED [V1] (Hadi, 2 October 2026; T-G records 15; design_decisions.md, "T-G: the second domain's rulings", T-G STAGE 1
CLOSED).
The independent review of dock_loading's task file against kitting's (the file follows kitting's building blocks and
rules; no special case for dock_loading exists in shared code) found that the robot's methods use a pallet's emptiness
as a proxy for the side of the gate on which its origin lies (return_empty against return_full). True for every pallet
the robot handles in stage 1; false in stage 2, when a full pallet has an origin in the hall (`store_pallet`). The
question: a route is selected from the areas of the agent and of the object, not from the kind of task and the pallet's
state. To rule before `store_pallet` is built.
Files: domains/dock_loading/tasks.py
Reference: design_decisions.md, "T-G: the second domain's rulings", STAGE 1, STEPS 6 TO 8 BUILT, the review's notes; design_decisions.md, B7, B11 (AMENDED); docs/handoffs/plan_T-G_stage1.md,
section 4

**TODO-157: The duration of office_break (recorded, the review of the task file, 1 Oct 2026)** [OPEN; Hadi's word pending] [CLOSED AS RULED, 1 Oct 2026: 90 seconds; the value is changed in the next build step]
`office_break` waits 60 seconds, a value copied from `coffee_break`; no record gives it. Hadi's word is pending.
CLOSED AS RULED (Hadi, 1 Oct 2026; design_decisions.md, "T-G: the second domain's rulings", T-G Q16's block, RULED,
T-G records 8; B6's note): `office_break` lasts 90 seconds; `coffee_break` stays 60. Reason: a long absence lets pallets
accumulate in a bay, which gives two scans possible at once and the robot arriving at an occupied bay; it differs
clearly from the coffee break. The change of the value is made in the next build step.
BUILT (edbe34f, 1 October 2026). CORRECTED (records, 2 October 2026; T-G records 9; B6's note): one tick is 2 seconds,
so the wait is 45 ticks and the human's absence about 110 ticks (C6 on env_layout_02: the dry bay left at 30, the frozen
bay reached at 141), a little more than one round trip of the robot (about 96 ticks); the value is reviewed with the
MPB's design.
REVIEWED (Hadi, 2 Oct 2026; design_decisions.md, "T-G: the second domain's rulings", THE MPB ON DOCK_LOADING, MPB-DL5):
the value stays 90 seconds for the MPB. Reason: no value is changed for a test set.
Files: domains/dock_loading/tasks.py (`office_break`)
Reference: design_decisions.md, "T-G: the second domain's rulings", STAGE 1, STEPS 6 TO 8 BUILT, the review's notes; design_decisions.md, B6

**TODO-158: Duration uncertainty and a projection that depends on context (recorded, T-K part 1 rulings, 2 Oct 2026)** [FW]
A conceptual direction (T-K part 1, R6). In V1 a task keeps one declared duration, and context changes how strongly
the robot considers a task, not the content of a projection; the only path from context to the projection is prior,
belief, gate, projection of the admitted task. An uncertain or context-dependent duration (Hadi's example: an office
visit of 20 to 30 seconds to fetch something, or 90 to 120 seconds of office work) changes what a projection is and how
realization reads it: planning under an uncertain projection, separate from the prior. A5 of the rulings (the robot's
declared duration and the human's actual duration match) holds until then.
Files: shared/projection.py, shared/meta_planner.py (realization)
Reference: design_decisions.md, "T-K: context knowledge in the recognizer's belief", R6, A5; "The human's
wait duration in the projection is the schema's, converted by the body (TODO-32, R2)"

**TODO-159: Unobservable states of the human as context (recorded, T-K part 1 rulings, 2 Oct 2026)** [FW]
A conceptual direction. In T-K part 1 a context fact is derived from context values, measured or scheduled quantities of
the situation (glossary §5); a state of the human the robot cannot observe (fatigue, for one; the present
`ContextKnowledge.shift_duration` calls itself a proxy for it) is not one. Whether and how such a state enters the
robot's knowledge is not designed in V1.
NOTE (AM31, Hadi, 3 Oct 2026; design_decisions.md, "T-K: context knowledge in the recognizer's belief",
AM14's AM31): a recency fact is a context fact derived from a value the robot measures from its own observation (the
time since an observed completion); it is not an unobservable state of the human.
Files: shared/knowledge.py (`ContextKnowledge`), shared/recognizer.py
Reference: design_decisions.md, "T-K: context knowledge in the recognizer's belief"; TODO-66

**TODO-160: Scopes of knowledge (general, sector, domain) and norms (recorded, T-K part 1 rulings, 2 Oct 2026)** [FW]
A conceptual direction. In T-K part 1 the context facts, occurrence conditions and strengths are declared per domain,
each strength with its source. Knowledge that holds at a wider scope (general, a sector, a domain) and norms of a site
are not designed in V1.
NOTE (AM36, Hadi, 3 Oct 2026): "occurrence conditions and strengths" reads "suppressing and raising conditions and the
three levels of a strength" (the suppressed and the ordinary strength per domain, the raised strength per task).
Files: shared/knowledge.py, domains/
Reference: design_decisions.md, "T-K: context knowledge in the recognizer's belief", R3, A4

**TODO-161: Validation of the strengths on site data (recorded, T-K part 1 rulings, 2 Oct 2026)** [FW]
A conceptual direction (T-K part 1, R3, A4). A declared strength is a modelling assumption until a site measures
it. Its proposed operational meaning, to be validated and not claimed: a ratio of counted task starts (starts of the
foreseeable task over starts of any assigned task), counted over task starts at which both were applicable, in the
stated situation; a ratio of counts, not a probability. Validating it, and the stability of the strengths across sites
(A4: not claimed), needs site data.
NOTE (AM39, Hadi, 3 Oct 2026; design_decisions.md, the same entry, R3's AM39): the reading stated per value, still
proposed and not validated: at a task start, with only this foreseeable task and the assigned tasks live, the
probability that the start is the foreseeable task is s / (1 + s); 0.005: 1 of 201 task starts, 0.02: 1 of 51, 0.5:
1 of 3, 2: 2 of 3.
Files: domains/ (the declared strengths and their sources)
Reference: design_decisions.md, "T-K: context knowledge in the recognizer's belief", R3, A4

**TODO-162: The robot without knowledge of the assignment (recorded, T-K part 1 rulings, 2 Oct 2026)** [FW] ⛔ SUPERSEDED by AM3 (3 Oct 2026)
SUPERSEDED (AM3, Hadi, 3 Oct 2026; design_decisions.md, "T-K: context knowledge in the recognizer's belief", R3's AM3; design_records.md, "T-K", R9's mark): no
future-work direction any more. Assignment knowledge is a run option, on by default; with it off, "work as a whole" is
every work task of the task model, and R3's formula covers the case. The off setting is an ablation or a diagnostic.
A conceptual direction (T-K part 1, R9): the support restriction (the switch named `assignment_prior`) is on by
default for every further analysis and test in V1; the robot that does not know the human's assigned tasks is future
work. Recorded only: the run option's default is still off (TODO-139), and prior off stays a recognizer diagnostic and
ablation configuration (`docs/assumptions.md` 1.4). R3's prior is stated for a robot that knows the assignment
(assigned work as a whole contributes 1).
Files: configs/experiment.yaml, shared/recognizer.py
Reference: design_records.md, "T-K", R9; design_decisions.md, "T-K: context knowledge in the
recognizer's belief", R3; TODO-44, TODO-139

**TODO-163: A/C deactivation (recorded, T-K part 1, content points 1 and 2, 3 Oct 2026)** [FW]
A conceptual direction, by Hadi's ruling (3 Oct 2026). In T-K part 1 ac_activation sets the A/C switch's object state
ac_on, and its occurrence condition is room_warm and not ac_on (AM13, AM18). Notes from the design chat: a context fact
room_cold; two tasks, not one task with two methods (that needs "or"); the state of the switch would then move into the
tasks' conditions, and object states would leave the occurrence condition.
NOTE (AM36, AM37, Hadi, 3 Oct 2026): ac_activation's suppressing condition is ac_on and its raising condition room_warm
(raised strength 0.5); T-K part 1 has no "not". "Room_warm and not ac_on" and "the occurrence condition" above read in
that form.
Files: domains/kitting/tasks.py (ac_activation; dock_loading gains it at T-K part 1's build, AM18), the domains' context knowledge
Reference: design_records.md, "T-K", CONTENT POINTS 1 AND 2, AM13, AM18, NOT RULED; design_decisions.md,
"T-K: context knowledge in the recognizer's belief", AM11

**TODO-164: Several A/C switches in one layout (recorded, T-K part 1, content points 1 and 2, 3 Oct 2026)** [FW]
A conceptual direction, by Hadi's ruling (3 Oct 2026). The V1 rule is at most one A/C switch per layout, in every
domain (AM18). Several switches need an occurrence condition that differs per hypothesis of one task, with the
division of the strength among the task's live hypotheses (AM2) reconsidered.
NOTE (AM36, Hadi, 3 Oct 2026): "an occurrence condition" reads "a suppressing or a raising condition".
Files: the domains' layouts, the domains' context knowledge, shared/recognizer.py (the prior)
Reference: design_records.md, "T-K", CONTENT POINTS 1 AND 2, AM18, AM19, NOT RULED; design_decisions.md,
"T-K: context knowledge in the recognizer's belief", R3's AM2

**TODO-165: Object rectangles crossing the outline of the space (recorded, layout tool, 3 Oct 2026)** open
In env_layout_12, env_layout_13 and env_layout_14 (kitting) the rectangles (position ± size/2) of shelf_6 and
kitting_table_4 (all three layouts) and kitting_table_6 (env_layout_14) cross the outline of the space, while their
centres are inside. domains/README.md, section 2, says the space holds every fixed object; the loader reads an object's
position as a point and its size for drawing only, so no check refuses it. Found when drawing the layouts with
scripts/layout_tool.py; the layouts are not changed (Hadi, 3 Oct 2026). The tool's edit page refuses a dragged object
whose centre leaves the space, not one whose rectangle does (Hadi, 3 Oct 2026).
Files: domains/kitting/layouts/env_layout_12.json, env_layout_13.json, env_layout_14.json
Reference: domains/README.md, section 2; mesa_sim/sim_model.py (`_init_objects`)

**TODO-166: orientation_deg, a field no code reads (recorded, layout tool, 3 Oct 2026)** open
The layout field `orientation_deg` is read by no code: the loader (`mesa_sim/sim_model.py`, `_init_objects`) keeps an
object's `position` and `size` only, and every rectangle is axis-aligned. The field exists only in kitting
env_layout_02 and in env_layout99 (unregistered). scripts/layout_tool.py does not draw it. Open question: remove the
field or implement it.
Also (3 Oct 2026): `orientation_deg` occurs on an item in kitting env_setup_02 (item_0, -90), a movable object. The
loader reads no such field for a movable object either.
Files: domains/kitting/layouts/env_layout_02.json, domains/kitting/env_layout99.json, domains/kitting/setups/env_setup_02.json, mesa_sim/sim_model.py
Reference: domains/README.md, section 2

**TODO-167: dock_loading, part of the space in no area (recorded, layout tool, 3 Oct 2026)** open
In dock_loading env_layout_02, env_layout_03 and env_layout_04 part of the space belongs to no area: above y = 300 and
outside the office (area_office: x in [-170, 170], y in [300, 415]; the space reaches y = 740). Seen in the layout
tool's drawings, not analysed. Open questions: what `shared.types.area_at` returns for a position there, and whether an
agent can reach that region.
Files: domains/dock_loading/layouts/env_layout_02.json, env_layout_03.json, env_layout_04.json; shared/types.py (`area_at`)
Reference: domains/README.md, section 2; design_decisions.md, "T-G: the second domain's rulings", A9

**TODO-168: Layout and picture files outside layouts/ (recorded, layout tool, 3 Oct 2026)** open
Layout files and pictures exist outside the domains' `layouts/` folders: domains/kitting/env_layout6.json and
domains/kitting/env_layout99.json (neither registered; CLAUDE.md keeps env_layout99 "for later"), and the picture files
at the top level of domains/dock_loading/ (env_layout1_original.svg, env_layout1_present_original.png,
env_layout1_present_original.svg, env_layout_original.jpg). Open question: keep, move or delete. The files are not
changed.
Files: domains/kitting/env_layout6.json, domains/kitting/env_layout99.json, domains/dock_loading/env_layout1_original.svg,
env_layout1_present_original.png, env_layout1_present_original.svg, env_layout_original.jpg
Reference: CLAUDE.md, "Where to look, and what to skip"; domains/discovery.py (`discover_files`)

**TODO-169: Deviation in dock_loading: a pallet delivered to a bay of the wrong subtype (recorded, 3 Oct 2026)** open
The human delivers a pallet to a delivery bay of the wrong subtype, and the robot recognises it. The subtype of pallets
and bays can feed this. Not designed yet. With one bay per subtype the deviation equals "placed in a bay that is not
the destination"; subtype adds information only with two or more bays per subtype.
Files: domains/dock_loading/layouts/, domains/dock_loading/setups/
Reference: design_decisions.md, "`subtype` is a stated fact of an object"

**TODO-170: tdlib.py reads meaning from the text of an id (recorded, 3 Oct 2026)** open
`analysis/instruments/common/tdlib.py:237` applies a pattern on kitting_table ids (`,?kitting_table=kitting_table_\d+`).
It violates the opaque-name rule.
Files: analysis/instruments/common/tdlib.py
Reference: design_decisions.md, "An object id is an opaque name"

**TODO-171: space_drawer OBJ_COLORS keys do not match dock_loading's types (recorded, 3 Oct 2026)** open
`mesa_sim/viz/space_drawer.py` `OBJ_COLORS` has the keys `delivery_area` and `empty_bay`; the layouts use
`delivery_bay` and `empty_pallet_bay`.
Files: mesa_sim/viz/space_drawer.py, domains/dock_loading/layouts/

**TODO-172: Kitting items carry subtype in the setups, no code reads it (recorded, 3 Oct 2026)** open
Kitting items carry `subtype` in the setups, and no code reads it (`SimObject.subtype` is loaded and unused).
Files: domains/kitting/setups/, mesa_sim/sim_model.py
Reference: design_decisions.md, "`subtype` is a stated fact of an object"

**TODO-173: Slots in containers (recorded, layout tool, 3 Oct 2026; T-G, covers both domains)** [FW]
A possible change from one position per container to named slots inside a container (kitting `shelf` and
`kitting_table`, dock_loading containers). A movable object would have a designated slot, and the world would state
which slot is empty or full. The existing `slots` field on kitting shelves is kept for this. The terms need glossary
entries before design work starts. Not designed.
Files: domains/kitting/layouts/ (the `slots` field of shelves), domains/dock_loading/layouts/, domains/*/setups/
Reference: docs/glossary.md, §10 **container**; design_decisions.md, "T-G: the second domain's rulings", B9
DEFERRED (Hadi, 6 October 2026, the slots discussion; its text verbatim in docs/handoffs/handoff_T-viz.md, section 9):
slots in containers are deferred to the framework's next version. In the current version the web-ui alone spreads the
movable objects of one container across that container's footprint (a display place, never written to the world, a
log or a file); the world does not change. Whether "the framework's next version" makes this item [FW] is Hadi's to
tag. The display side is T-viz's (design_records.md, "T-viz, the web-ui").
TAGGED [FW] (Hadi, 6 October 2026).

**TODO-174: "door" names two things (recorded, layout tool, 3 Oct 2026)** open
"door" is a type in dock_loading (`office_door`, size [100, 10]) and the id of a landmark in kitting (size [80, 20]).
One word names two things. Open question: whether one of them is renamed.
Files: domains/dock_loading/layouts/, domains/kitting/layouts/env_layout_01.json, env_layout_03.json to _07, env_layout_09.json
Reference: docs/glossary.md, §6 **landmark**; design_decisions.md, "An object id is an opaque name"

**TODO-175: Named logs in logs/ cited as evidence, logs/ git-ignored (recorded, 3 Oct 2026)** open
Named logs in logs/ are evidence for statements in the records, and logs/ is git-ignored: 3 in TODOS_AND_DEFERRED.md,
6 in analysis/kitting/t1_conflict_measurement/REPORT.md, 2 in analysis/kitting/f1_foreseeable_fixture/REPORT.md. 2 of
the 11 cannot be reproduced (the first two named in TODOS_AND_DEFERRED.md). 3 lack only their commit
(run_20260910_144817 and the two f1 logs). 6 are reproducible at commit 372d925 (the t1 logs). Open question: copy each cited log into the folder of the record that cites it, so that
git tracks the evidence.
Files: docs/TODOS_AND_DEFERRED.md (lines citing run_20260904_131808, run_20260910_083630, run_20260910_144817),
analysis/kitting/t1_conflict_measurement/REPORT.md, analysis/kitting/f1_foreseeable_fixture/REPORT.md
Reference: CLAUDE.md, Workflow rules, 7

**TODO-176: layout_tool.py reads the number in existing ids to generate a new id (recorded, 3 Oct 2026)** [CLOSED, 3 Oct 2026: fixed]
scripts/layout_tool.py generates a new id by reading the number in existing ids of the form <type>_<N>. This violates
the rule on object ids. Fix: form candidates <type>_0, <type>_1, ... and take the first that equals no existing id, by
whole-id equality only. The layout tool's session owns the fix.
CLOSED (3 Oct 2026): the generator forms <type>_0, <type>_1, ... and takes the first that equals no id of the source
layout and no id used on the page, an id deleted during the edit included; whole-id equality only. The prefix test, the
slice and the pattern on an id are removed from the tool's page. The only string tests left in the tool are on the name
the user types for the new layout (its file stem: a separator, a `.json` ending, a leading `.`), not on an object id.
Files: scripts/layout_tool.py (the id of an added object), scripts/README.md
Reference: design_decisions.md, "An object id is an opaque name"

**TODO-177: An override of the timeline of context facts (recorded, T-K part 1, AM41, 4 Oct 2026)** open
Later work, by Hadi's ruling (4 Oct 2026): an override of the timeline from the run file and from the viewer, which
takes precedence over the setup's and the scenario's timeline. Not built in T-K part 1. The build resolves the timeline
in force at load in one place (the scenario's, else the setup's, else none), so the override is a further branch there,
with no change to the recognizer. A change of a fact during a run is not this item: it belongs to the interactive phase
(T-V track 2).
Files: mesa_sim/sim_model.py (the timeline's resolution at load), mesa_sim/overrides.py, mesa_sim/viz/run_file_panel.py
Reference: design_decisions.md, "T-K: context knowledge in the recognizer's belief", AM11's AM41;
docs/handoffs/plan_T-K_part1.md, 3.2

**TODO-178: The floor and the scaling by the pinned hypotheses in the reported distribution (recorded, T-K part 1, AM42, 4 Oct 2026)** open
Later work, by Hadi's ruling (4 Oct 2026). Since AM42 the gate compares the threshold with the belief over the live
hypotheses; the floor (BELIEF_FLOOR) and the scaling of the live mass by the pinned hypotheses stay in the reported
distribution only (`[IR-dist]`, `BeliefState.distribution`). The item: remove them from the reported distribution as
well. The output is not fed back (the recognizer's `prev_belief` is not consulted), so the floor's stated reason (no
recovery from exact zero under a multiplicative update) no longer acts on the inference.
Files: shared/recognizer.py (`_output`, `_finalize`, `_pin`), docs/recognizer_handback.md §1.7, the instruments'
oracle (analysis/instruments/irb/oracle.py, `output`) and log readers
Reference: design_decisions.md, "T-K: context knowledge in the recognizer's belief", R7's AM42;
docs/handoffs/plan_T-K_part1.md, section 5 (a)

**TODO-179: The episode-boundary line names wait_at for a completed switch_on (recorded, T-K part 1, AM56, 4 Oct 2026)** open
A log names what happened (Hadi, 4 Oct 2026); deferred because the correction is not small. When T-K part 1's build
adds switch_on (AM43), an A/C activation's completion makes waited(human, switch) newly hold, and both terminal actions
wait_at and switch_on have an enabled grounding at the switch (the same precondition at(agent, entity), the same
completion waited(agent, entity); wait_at's ?entity has no type in its schema). `_observed_terminal_completion` returns
the first in declaration order, so `[IR-boundary]` reads `completed wait_at(ac_switch_…)`. The boundary's tick is right.
A correct label needs the terminal actions' parameter types derived from the methods that call them and the objects'
types in the robot's world state, a change to the boundary's as-built reading (T-D L1), which needs a ruling.
switch_on's effect ac_on newly holding distinguishes the two only when the A/C was off. Reordering the terminal actions
moves the wrong label to the coffee break. Readers of the label: `analysis/instruments/common/tdlib.py`
(`boundary_action`).
Files: shared/recognizer.py (`_observed_terminal_completion`, `_action_label`), shared/knowledge.py
(`terminal_actions`), shared/types.py (WorldState), analysis/instruments/common/tdlib.py
Reference: design_records.md, "T-K", THE CROSS-CHECK, RULED, AM56; docs/handoffs/plan_T-K_part1.md, section 11, X3

**TODO-180: The viewer's confidence (recorded, T-K part 1, AM58, 4 Oct 2026)** open
Since AM42 the gate reads the leader's belief over the live hypotheses (`BeliefState.confidence`), and the reported
distribution keeps the floor and the pin scaling, so the leader's value in `distribution` can differ from
`confidence`. The viewer is not checked for which value it shows as the confidence. ccode's check (4 Oct 2026): no file
under mesa_sim/viz/ reads `confidence` or `distribution` today, so the viewer shows no recognizer value now; the item
applies when it does (T-V track 1).
POINTER (6 October 2026): the first program to show a recognizer value is planned as the web-ui's panel 4b (T-viz stage
1b; design_records.md, "T-viz, the web-ui"); the item applies there.
Files: mesa_sim/viz/
Reference: design_records.md, "T-K", THE CROSS-CHECK, RULED, AM58; docs/handoffs/plan_T-K_part1.md, section 11, X2

**TODO-181: Execution-time collision avoidance in a human-unaware run (recorded, T-F part 1, ruling C, 5 Oct 2026)** open
`human_aware` off sets the separation stop off, so a human-unaware run has no check against the human at execution.
For runs that simulate execution fully, not only compare recognition and planning: an execution-time collision
avoidance that also acts in a human-unaware run. Future work; not designed.
Files: mesa_sim/executor.py, mesa_sim/sim_model.py
Reference: design_decisions.md, "T-F part 1: the conditions human-unaware and intention-unaware", C; TODO-73

**TODO-182: Human-unaware with the observed human kept (recorded, T-F part 1, ruling D, 5 Oct 2026)** open
Hadi's alternative to D: the robot keeps the observed human and each component of the mind skips its computation,
instead of the loader giving the robot no observed human. Its reason: an execution-time avoidance (TODO-181) could then
still use the human. Future work.
Files: mesa_sim/sim_model.py, mesa_sim/sim_agents.py
Reference: design_records.md, "T-F part 1: the conditions human-unaware and intention-unaware", D; TODO-181

**TODO-183: May a domain forbid a run condition? (recorded, T-F part 1, ruling G, 5 Oct 2026)** open, for T-G's next stage; not ruled
Example: a mandatory check-in. If the robot learns of it as a state of an object, a human-unaware robot still waits for
it. If the robot must recognise the human's act, a human-unaware run is not a meaningful baseline there.
Files: domains/dock_loading/, mesa_sim/run_mesa.py
Reference: design_records.md, "T-F part 1: the conditions human-unaware and intention-unaware", G; T-G stage 3
(check-in and check-out)
FORWARDED (T-F part 1's close, 5 October 2026): an input of T-G's next stage (docs/handoffs/T-G_forward_inputs.md).

**TODO-184: A stand at the robot's target that does not end (recorded, T-F part 1's close, 5 Oct 2026)** open; not ruled
X1's case with no alternative task, measured (design_records.md, "T-F part 1", THE CLOSE, FINDINGS): in
scenario_s02_02 (env_layout_02; its script ends with the human delivering at kitting_table_0 and no exit walk,
docs/assumptions.md 1.1) the human stands at the robot's remaining target from tick 250 to the run's end. The three
conditions that observe the human hold on fallback projections of the stand, each as long as the stand so far (P4), and
do not finish within the cap of 704 ticks (holds up to 256 ticks at 502, intention-unaware; 384 at 630, intention-aware);
human-unaware completes at 422. The question: what the robot does when a stand at its target does not end. X1 set
aside a give-up threshold (a constant) and pointed to communication (X5, TODO-96, TODO-141). Whether the script is an
authoring artefact (1.1) or the case is to be designed is the first decision.
Files: shared/meta_planner.py (the fallback's re-decision), shared/projection.py (the fallback projection)
Reference: design_decisions.md, "T-D X: response", X1, X5; "T-D P", P4; TODO-96, TODO-141

**TODO-185: "In accord" for a fact that lowers a task (recorded, the tag per task, 5 Oct 2026)** open; not ruled; for Hadi's next chat
The tag per task (design_records.md, "T-F part 1", THE TAG PER TASK; glossary §7, **in accord**) is defined for facts
that raise a task (break_time raises coffee_break; room_warm raises ac_activation). For a fact that lowers a task (a
suppressing condition: the human just had a break, the A/C is on), what "in accord" and "not in accord" mean is not
decided.
FOLLOWED PROVISIONALLY (Hadi, 6 October 2026, T-viz 1a (iv)): the web-ui's panel 4a shows the tag with the provisional
rule of T-K step 6 (a fact that lowers a task gives no tag), from the one definition `world/tag.py`; still open.
Reference: design_decisions.md, "T-K: context knowledge in the recognizer's belief", AM36 (the three levels)

**TODO-186: T-viz stage 2, editing: the open questions (recorded, T-viz 0.1, 6 Oct 2026)** open [FW]; decided when the stage is reached
TAGGED [FW] (Hadi, 6 October 2026, preferred): T-viz stages 2 and 3 are after V1 for now, the default until Hadi draws
the V1 border inside the web-ui. Stage 0's choice of technology still considers this stage (handoff, 6.1, item 6).
In T-viz records the status words are the handoff's (open, preferred, proposed by cchat), not "ruled". Hadi's words:
stage 2 allows editing of layouts (scene arrangement, add or remove objects), setups (placements) and scenarios
(scripted human behaviour, the timeline of context facts), each saved as a new artefact. The questions, all open:
- The three override kinds (`mesa_sim/overrides.py`, offered today by the solara-ui's run-file panel): whether the web-ui
  offers them in stage 1 or stage 2.
- Scripts have no typed textual form: scenarios are Python literals (`ScenarioConfig`), layouts and setups JSON.
  Editing a script in a page needs a structured form of scripts that the page can show, change and write back, a core
  design matter. Proposed by cchat: stage 2 begins with layouts and setups, scripts after that core step.
- The draft (the chosen artefacts plus the edits, held in the server's memory) and its saving as new artefacts with
  their own serial ids (a change worth keeping is a new artefact).
- A preview without a model while a draft does not load (alternative C of the handoff's 7.5).
- Validation: the page shows the loader's error when a draft fails.
- The existing layout tool (`scripts/layout_tool.py`, `scripts/README.md`): its relation to stage 2.1.
- Selection by composition and coverage for the selection panel (TODO-110).
Files: mesa_sim/overrides.py, shared/types.py (ScenarioConfig), scripts/layout_tool.py
Reference: docs/handoffs/handoff_T-viz.md, sections 7.5, 7.6, 13.1; design_records.md, "T-viz, the web-ui"

**TODO-187: T-viz stage 2, sim-runs side by side: the open questions (recorded, T-viz 0.1, 6 Oct 2026)** open [FW]; decided when the stage is reached
TAGGED [FW] (Hadi, 6 October 2026, preferred): as TODO-186.
Hadi's idea: two env-panes on the same triple, for example one with `intention_aware` on and one off, the two sim-runs
fully isolated. Three ways (a mode of one server with two `SimModel`s stepped together; two tabs on one server; two
starts in two windows) and their trade-offs: the handoff, 13.2. Proposed by cchat: the mode, since a comparison is
meaningful at equal ticks. Open: what may differ between the two sides; what happens when one sim-run ends earlier;
the page layout with two env-panes. Isolation in one process: read in 0.1 (design_records.md, "T-viz, the web-ui",
THE VERIFICATIONS, fact 10): no global random source in use and no registry changed by the load; the run log and the
`.rec` stream are process-wide (one file pair per process, set up at import of `mesa_sim/run_mesa.py`), so two models
in one process would write into one log. The decisive check (proposed by cchat): step two models alternately in one
process and compare each one's log with the same sim-run executed alone and headless. A limit: the side-by-side view
demonstrates; evaluation numbers come from headless sim-runs.
LOGGING SINCE T-VIZ 0.2 (ccode, 6 October 2026, verified; what follows the first sentence is proposed by ccode, open):
the log pair is a sim-run's (`mesa_sim/sim_run.py`, `RunLog`), not a process's, but logging stays process-wide: the
model, its agents and `shared/` write through the root logger and the logger `rec`, so one pair is attached at a time
and a new sim-run closes the one before it. Two sim-runs stepped alternately in one process would therefore not get
their own logs. They could be separated later without changing `SimModel`: the sim-run sets a context variable to
itself around its build, each step and its end, and each pair's handlers take only the records emitted while their
sim-run is the current one (a `logging.Filter` reading the variable); a record emitted outside every sim-run then goes
to none. The decisive check above stays the test of it.
Files: mesa_sim/sim_run.py (the log pair), mesa_sim/sim_model.py
Reference: docs/handoffs/handoff_T-viz.md, sections 5.10, 13.2; design_records.md, "T-viz, the web-ui"

**TODO-188: T-viz stage 3, changes during a sim-run: the open questions (recorded, T-viz 0.1, 6 Oct 2026)** open [FW]; decided when the stage is reached
ANSWERED AND TAGGED [FW] (Hadi, 6 October 2026, preferred): T-V track 2 (Phase 7, live events on the human's script)
is T-viz stage 3: stage 3 means T-V, the live-event mechanism included, not only the page's side. It is after V1 for
now, the default until Hadi draws the V1 border inside the web-ui. "Proposed by cchat, not answered" below is
superseded.
Hadi's words: stage 3 allows interactive changes during a sim-run, such as adding events, interruptions and deviations
to the human's scripted behaviour. Hadi placed the change of the human's behaviour during a sim-run in T-V track 2
(Phase 7). Proposed by cchat, not answered: stage 3 is the page's side of T-V track 2; the mechanism (the human
executor's injection path `inject`, the replay rule, the event log) stays T-V's. The server already holds the model, so
an "inject" request would be an addition. Within stages 0 to 2 nothing is edited while a sim-run is in progress
(preferred).
Files: world/human_executor.py (`inject`)
Reference: docs/handoffs/handoff_T-viz.md, sections 5.8, 13.3; docs/handoffs/phase7_interactive_deviations.md;
design_decisions.md, "A run-time deviation is the same operation as a load-time edit (Phase 7, recorded)"

**TODO-189: T-viz, items with no stage (recorded, T-viz 0.1, 6 Oct 2026)** open
Raised in the design chat of 4 to 6 October 2026, no stage assigned:
- Clicking an object or an agent during a pause to inspect it.
- An automatic pause at an event of the robot's cognition. Not built in the solara-ui (0.1, fact 9); the design of an
  earlier chat named `theta_crossed` and `task_committed`, two triggers that no longer exist (D2, D3): the event list
  would be today's triggers (`no_current_task`, `recognition_changed`, `projection_expired`) or other events.
- Moving back along the ticks for display, from the tick updates the page keeps.
- Replay of a finished sim-run without Mesa, from the tick updates written to a file.
- Saving the page's choice as a run file, so that a sim-run configured in the page repeats headless (proposed by
  cchat).
Hadi's global freeze button: with the clock proposed by cchat (the page requests each step) it is the pause.
UPDATED (T-viz 1a, 6 October 2026): the page's choice is mirrored in its address (a bookmark reopens a choice at its
start); the address is not a run file, so the last item stays open. The page holds every tick update of a sim-run
(`current` answers with them), which moving back along the ticks would read.
UPDATED (Hadi, 7 October 2026, preferred; design_records.md, "T-viz, the web-ui", 1c, THE BOTTOM PANEL, item 6): moving
back along the ticks for display is taken out of this list without a stage: in stage 1c a click on panel 4c's plot
shows an earlier tick (the scene and both side panels), play or step returns to the latest tick; the sim-run never goes
back and its log is not affected. The other items stay open, with no stage.
Reference: docs/handoffs/handoff_T-viz.md, sections 7.3, 7.4, 8.5, 13.4

**TODO-190: The V1 border inside the web-ui: four open points (recorded, T-viz, 6 Oct 2026)** open; Hadi decides later
Hadi, 6 October 2026 (preferred for now): "Put everything in FW, I decide later." T-viz stages 2 and 3, TODO-173 and
TODO-186 to TODO-188 are [FW] until Hadi draws the V1 border inside the web-ui. No ruling is amended. The four points to
settle then, each open, Hadi decides later:
1. The [FW] tags against A1's tag rule (design_records.md, "T-G, the second domain", A1, Tags; glossary, **FW**): [FW]
   is for conceptual, higher-level directions only, and the web-ui's stages 2 and 3 and TODO-173 are build work.
2. A3's text (design_decisions.md, "T-G: the second domain's rulings", A3): the human's choice among applicable tasks is
   isolated "so that a live user (T-V track 2, in V1)" can supply it, "a V1 requirement"; the live user (T-viz stage 3)
   is now FW. The isolation is built (048a36e).
3. Track 3b and track 4 placed "after T-V" (roadmap.md, T-D's tail lines; glossary, **T-D tail**; TODO-140, TODO-145,
   PLACEMENT REVISED), with T-V now split into T-viz stage 1 (V1) and stage 3 (FW).
4. The place of T-viz stage 1 in the order: ccode's proposal, in T-V's place, after T-F and before track 3b (roadmap.md,
   the order block's line of 6 October 2026).
Reference: design_records.md, "T-viz, the web-ui", HADI'S ANSWERS and HADI'S ANSWER ON THE CONTRADICTIONS AND THE PLACE

**TODO-191: The two run-level lines that say "headless" for every start (recorded, T-viz 0.2, 6 Oct 2026)** open
Since T-viz 0.2 every start writes the start line `[run_mesa] Starting headless run — ...`, and every start that ends
its sim-run the end line `[run_mesa] Headless run complete.` (`mesa_sim/sim_run.py`, `SimRun`): the solara-ui writes
the start line now (it never ends a sim-run), the web-ui will write both (when a sim-run ends there is open). The
text was kept for byte-identity with the maintained baseline sets (Hadi, 6 October 2026, agreed with ccode's proposal).
To be renamed at the next regeneration of the baseline sets. Readers of the text (6 October 2026):
`analysis/instruments/mpb/figure_of_log.py` and `analysis/instruments/irb/summary.py` (the start line), tests/kitting/
test_tl4_overrides.py and tests/test_tviz_sim_run.py.
UPDATED (T-viz 1a, 6 October 2026): the web-ui writes both lines since increment (i) (a sim-run ends at a step limit,
a reset, a change of choice or the server's stop), and a web-ui sim-run without a step limit writes `steps=none` on the
start line.
Files: mesa_sim/sim_run.py
Reference: design_records.md, "T-viz, the web-ui", 0.2

**TODO-192: The orientation of fixed objects, stated in a layout file and dropped by the loader (recorded, T-viz 0.4, 6 Oct 2026)** open
One layout file states an orientation per fixed object, `orientation_deg` (domains/kitting/layouts/env_layout_02.json,
11 objects, 0 or -90), and one setup file per movable object (env_setup_02.json). The loader does not keep it
(`mesa_sim/sim_model.py`, `SimObject` has no orientation) and no code reads it; the solara-ui's drawer does not either.
So the web-ui's messages carry none (T-viz 0.4, Q7, Hadi, 6 October 2026: left out of stage 1a). Open, for the scene's
look (a shelf's front, a figure facing a table): whether an orientation becomes a stated fact of a fixed object, kept by
the loader and carried by the run description, with the layouts that lack it given one; or whether the per-domain
visualisation configuration supplies it. Either is its own change before the scene needs it. The `slots` field of
kitting's layouts (TODO-173, FW) is likewise in the files and unread.
Files: mesa_sim/sim_model.py, webui/messages.py, domains/*/layouts/
Reference: design_records.md, "T-viz, the web-ui", 0.4

**TODO-193: Dark mode of the web-ui (recorded, at the close of T-viz stage 0, 6 Oct 2026)** open [FW]; stage 2 or 3
Hadi, 6 October 2026 (preferred): no dark mode in stage 1; it is recorded for stage 2 or 3, which are [FW] until Hadi
draws the V1 border for the web-ui (TODO-190). The theme file holds every colour of the page and the scene in one place
(`webui/page/src/theme.ts`), so a dark mode is a second set of its values.
Files: webui/page/src/theme.ts
Reference: docs/handoffs/handoff_T-viz.md, "State after stage 0" and 10.7; design_records.md, "T-viz, the web-ui",
STAGE 0 CLOSED

**TODO-194: An object's state changes its shape in the scene (recorded, at the close of T-viz stage 0, 6 Oct 2026)** DONE in T-viz 1a (iii), 6 Oct 2026
Hadi, 6 October 2026 (preferred): an object's state may change its shape, for example an empty pallet or an open gate,
with minimal effort, in stage 1a. The tick update carries the object states that hold (`ObjectState`); the scene
appearance (`webui/appearance.py`) maps an object type to a form and does not yet map a state to anything. Found in
0.3: an empty pallet is drawn as a full one, and the gate's `is_open` is not drawn. Open for stage 1a: how the
appearance data names a state and its effect on the form, without a domain word in the page's code.
DONE (T-viz 1a (iii), 9e1bef1, e42bd2b): looks by state in the appearance data, checked against the domain's declared
states; dock_loading's loaded and empty pallet and its open gate.
Files: webui/appearance.py, webui/page/src/env-pane/forms.tsx, domains/*/appearance.json
Reference: design_records.md, "T-viz, the web-ui", 0.3 and STAGE 0 CLOSED

**TODO-195: The free camera of the env-pane (recorded, at the close of T-viz stage 0, 6 Oct 2026)** DONE in T-viz 1a (iii), 6 Oct 2026
Hadi, 6 October 2026 (preferred): the tilted view at 35° and the view from above stay as presets, and in stage 1a the
screen-user can change the camera freely during a sim-run: rotate, tilt, zoom and move. Open for stage 1a: the controls,
and how they sit beside the two presets. The trial's camera is `webui/page/src/env-pane/camera.tsx` (an orthographic
camera framed on the space).
DONE (T-viz 1a (iii), e42bd2b): drei's orbit controls beside the two presets; tuning, if any, in the polishing round
after stage 1c.
Files: webui/page/src/env-pane/camera.tsx
Reference: docs/handoffs/handoff_T-viz.md, 10.6 item 5 and 10.8; design_records.md, "T-viz, the web-ui", STAGE 0 CLOSED

**TODO-196: One start command with subcommands (recorded, at the close of T-viz stage 0, 6 Oct 2026)** answered for now (6 Oct 2026); returns when a second simulator exists
Hadi, 6 October 2026 (preferred): no single "mother" start command now; each start (headless, the solara-ui, the trial
page of 0.3) has its own command, which the README states. The question of one command with subcommands returns in
stage 1a, when the web-ui's start command is defined.
Files: mesa_sim/run_mesa.py, README.md
Reference: docs/handoffs/handoff_T-viz.md, 7.3; design_records.md, "T-viz, the web-ui", STAGE 0 CLOSED
ANSWERED FOR NOW (Hadi, 6 October 2026, preferred, for stage 1a): one command per start. The web-ui's start command is
a file in `mesa_sim/` that accepts the same run file and flags as the headless start, so that the page can open with a
sim-run already chosen; `webui/` stays at the repository's root and imports no simulator. The question returns when a
second simulator exists. design_records.md, "T-viz, the web-ui", 1a, HADI'S PREFERENCES, item 6; the start proposed
in `docs/handoffs/plan_T-viz_1a.md`, section 4, item 6.

**TODO-197: Paths in the scene (recorded, at the close of T-viz stage 0, 6 Oct 2026)** open; stage 1b
Hadi, 6 October 2026 (preferred; at 0.4 and at the close of stage 0): stage 1a shows no planned path; whether and which
paths the scene shows is a question for stage 1b. Verified in 0.1: no module writes `agent.planned_path`, and the model
holds no path per agent. The handoff's 8.4 raises whether a path is world content or mind content; it is open. The
handoff's "a straight line now, replaced later" (6.2) is superseded in part.
Files: webui/messages.py, mesa_sim/webui_adapter.py
Reference: docs/handoffs/handoff_T-viz.md, 5.4, 6.2, 8.4; design_records.md, "T-viz, the web-ui", 0.1 (fact 3), 0.4
ANSWERED (Hadi, 6 October 2026, preferred; design_records.md, "T-viz, the web-ui", 1b, THE RIGHT PANEL'S CONTENT AND
STAGES 1d AND 1e): the scene shows paths in two stages added after 1c: 1d the movement of the current task of the human
and of the robot as wide, semi-transparent stripes on the floor (the walk segments; a first try, the form open); 1e the
robot's projection of the human (the admitted task's plan or the fallback projection) in the same way. The simulator's
side derives the segments, the page computes none; the human's real movement is a world fact, the robot's plan and its
projection belong to the robot's section of the messages (proposed by cchat). Stage 1b draws no path.
