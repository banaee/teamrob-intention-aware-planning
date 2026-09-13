# TeamRob Framework — TODOs, Bugs, and Deferred Items

Collected from Phase 2.1 (dock_loading domain), 2.2 (visualization), and Phase 4 design sessions.
Each item has a category, priority, and the relevant file(s).
Items marked **[BLOCKING]** must be resolved before the simulation runs correctly end-to-end.

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
Files: `shared/meta_planner.py` (Phase 4 new)
Reference: Phase 4 design session

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

**DESIGN-08 — Team-level semantic costs in cost function (parked)**
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

**DESIGN-13 — Common non-committed path-realization estimator ("action-estimator" adaptor)** [Phase 4C, parked — dedicated design session needed]
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

**DESIGN-16 — Single-task RESELECT vs. full queue reordering (strategy flag)** ✅ RESOLVED (Sept 2026)
RESOLVED in favour of single-task, receding-horizon selection as the implemented default;
full reordering retained as a documented, switchable alternative. Full rationale in
design_decisions.md, "Single-task selection (receding horizon), not queue-wide reordering."

Implementation: `MetaPlanner._strategy: Literal["single_task", "full_reorder"]`, constructor
param, defaults to `"single_task"`. `update()` branches on it; `_project()` raises
`NotImplementedError` for orderings longer than 1. The seam exists in code, not only in docs,
so `full_reorder` is a known-cost extension rather than a rewrite.

To implement `full_reorder`, three things are needed: (i) resolve TODO-07's effects/retraction
semantics for cross-task WorldState propagation, (ii) DESIGN-12's horizon-projected confidence,
(iii) a scalable ordering search — brute permutation is O(n!) and is the wrong shape for any
realistic task count. Do not implement piecemeal.

NOTE ON NUMBERING: this decision was referred to as "DESIGN-14" throughout the September 2026
build session before it was noticed that DESIGN-14/15 were already taken. Any code comment,
docstring, or chat reference to "DESIGN-14" regarding strategy/reordering means DESIGN-16.
Files: shared/meta_planner.py, shared/io_contracts.md §2.2
Reference: Phase 4C meta_planner build session, September 2026

**TODO-27 — `conflicts` list volume: no "worth recording" threshold** [Phase 4C, deferred]
`_detect_interference()` concatenates every `ConflictPoint` from every time-overlapping
segment pair with no filtering. Observed in scenario_00: 900–1500 ConflictPoints for a single
candidate, since `discretized_time_sampling(interval=1.0)` emits one point per step per pair
over ~1700-step projections. Functionally correct (only the minimum distance is read) but
memory-wasteful, and makes the objects useless for logging/inspection.
Deliberately not fixed now: a second "only record below distance X" threshold was considered
and rejected as premature — the list is bounded and correctness is unaffected. Revisit if
profiling shows it matters, or when DESIGN-08's soft penalty needs to actually iterate these.
Files: shared/meta_planner.py (_detect_interference), shared/trajectory_algorithms.py, shared/projection.py
Reference: Phase 4C scenario_00 validation, September 2026

**TODO-28 — `min_safe_distance` and `assumed_speed` are uncalibrated placeholders**
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

**TODO-30 — Interference exclusion branch never exercised**
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

**TODO-32 — `wait_at` duration ignored in cost estimation**
`Projector.build_segments()` treats every non-movement action as costing
`knowledge.get_cost(action_name)` or `default_action_cost`, including `wait_at` — so a
`PT60S` coffee break and a `PT2S` AC toggle currently cost the same. The real ISO-8601
`?duration` binding is parsed in `mesa_sim/action_decomposer.py`, which `shared/` cannot
import. A known simplification, not a considered decision.
Matters specifically for foreseeable tasks (`coffee_break`, `ac_activation`), whose whole
point is that the robot should reason about how long the human will be occupied. Likely to
distort candidate costs once foreseeable-task scenarios are tested.
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


**TODO-36 — `MetaPlanner` block restructuring (B1/B2/B3) not yet implemented**
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
to B2.A+B3.A, differing only in projection count. Useful in an ablation table, misleading if
read as a fourth strategy.
BLOCKER: B2.A needs a scalar worthiness score turning `List[ConflictPoint]` into a number —
the same missing quantity as DESIGN-08's soft interference penalty. Build once, use for both.
Candidate formulas: minimum distance across conflicts; count below a radius; proximity
integrated over time; or estimated added cost from pausing/detouring (DESIGN-13), which would
make the score comparable to execution cost and remove the need for a separate threshold.
Also open: whether B2's threshold is distinct from B3's exclusion threshold — they are
different in kind (graded/effort-based vs. binary/safety-based), not merely in value.
Naming: `_is_current_task_plausible()` or similar — "feasible" is wrong, since the check is
about worthiness, not doability.
Files: shared/meta_planner.py (`update`)
Reference: Phase 4C block-design session, September 2026


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
(measured: 20–50 new firings per condition, `analysis/i2_ir_foundations/zone_boost_episodes.csv`).
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

**TODO-38 — IR: direction-only likelihood cannot separate collinear decoys** [OPEN DISCUSSION — not decided]
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

**TODO-43 — A no-op `update()` costs the robot one tick**
When a trigger fires and B3 re-selects the task already executing, `RobotAgent` reloads the
plan (`[executor] _load_plan`) and the robot loses that tick. scenario_20, assignment_prior
off: the step-22 `theta_crossed` re-issues item_4 and the robot grasps at step 23; with the
prior on (no trigger at step 22) it grasps at step 22. Every later event shifts by one step,
and projection distances shift with it (`task_committed` item_4 min_dist 4.9 vs 24.9 — one
step of arrival gap). Harmless at today's trigger rate; a real cost once B2 fires often, since
every "continue" would stall the robot. Fix direction not decided; candidate: keep the
current plan when `UpdateResult.current_task` is the executing task.
Files: mesa_sim/sim_agents.py (`RobotAgent.step`), shared/meta_planner.py (`update`)
Reference: fixture-design session, September 2026

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
×4, in all eight conditions (`analysis/i3_phase_model/completion_events.csv`). `place` is never
reached by the channel: the task's terminal completion holds on the same tick and the pin
preempts it. No completion check ever returned LOW in the sweep (items sit on distinct shelves, so
no two hypotheses expect a grasp at once; check U4 shows the ×40 discrimination when they do).
I2: `_get_expected_position()` is gone; the target is the first movement action of the
planner's guard-selected method, grounded through task and step bindings and resolved by
`shared/target_resolution.py`. Measured (`analysis/i2_ir_foundations/summary.md`): 0 unresolved
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

**TODO-47 — Stress-test harness: randomised layouts, scenarios, parameters** [post-4C]
Plan: run every B2.X × B3.X combination over hundreds of generated simulations (randomised
layouts, scenarios, parameters) and compare outcomes. Not seed repetition — the sim is
deterministic under PYTHONHASHSEED=0, so variation must come from generated inputs.
Prerequisites:
(a) Programmatic layout/scenario registration — adding a layout today needs three manual
    edits (layout JSON, `scenarios.py`, `registry.py`).
(b) Scale-relative calibration — `min_safe_distance` (and any B2 threshold) must be expressed
    relative to layout scale or agent speed × steps, not as an absolute read off one fixture.
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

**TODO-48 — Hypothesis change above θ fires no trigger**
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

**TODO-49 — Type-name mismatch between layout and schema silently empties a task's hypothesis space**
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
(`analysis/i2_ir_foundations/f1_traces/`): `most_likely` from step 118 to the end of the run,
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

**TODO-52 — scenario_10's step-257 RuntimeError is latent, not fixed**
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
Files: shared/meta_planner.py
Reference: I1 audit O1; I2 IR foundations session

**TODO-53 — A hypothesis whose expected action never completes is judged by one chord from t=0**
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

**TODO-54 — `theta_crossed` fires on `unknown` when a pin shrinks the live set**
s20_off step 136: the robot delivers item_6, the recognizer pins `deliver_item(item_6)`, and
`unknown` inherits its mass (0.654 → 0.804 ≥ θ) while the human stands idle. `evaluate_triggers`
fires `theta_crossed`, the meta-planner builds a projection for `unknown` and replans. Belief-side
this is correct (the human has no task); the trigger should probably not fire on `unknown`, and
the earlier question (TODO-48) of a `most_likely`-change trigger should be decided together with
it. Meta-planner paused: recorded only.
Files: shared/meta_planner.py (evaluate_triggers)
Reference: I3 phase-model session

**TODO-55 — What a single-task hypothesis means while another task is visibly under way** [DEFERRED by decision — re-measure after I4, not before]
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

**TODO-56 — The completion channel's gate is the old model's, and it is a decision**
I3 judges an event only against expected actions whose vocabulary declares it (GRASP → `pick_up`),
leaving movement actions NEUTRAL at a grasp as before. The other reading — every expected action
LOW at a discrete tick unless its completion holds — is generative-model-correct (a walker does not
emit GRASP) and was measured (variant `ungated`): `unknown`, which pays nothing, takes ×10 against
every live task at every grasp and release and ends at 0.96–0.99 after every completion; no second θ
crossing in any condition. The asymmetry is `unknown`'s flat likelihood, not the gate. If I4 gives
`unknown` a likelihood of its own, revisit the gate with it.
Files: shared/recognizer.py (`_in_vocabulary`)
Reference: I3 phase-model session; analysis/i3_phase_model/summary.md

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
