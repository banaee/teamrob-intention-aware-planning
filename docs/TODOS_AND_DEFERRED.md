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
Files: `shared/planner.py`
Reference: Phase 4B

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
robot list is a mutable prioritised queue owned by meta_planner at runtime.
See design_decisions.md Phase 4 section for full specification.

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
Files: shared/types.py (ActionSchema.progress_evaluator field),
domains/kitting/actions.py, domains/dock_loading/actions.py,
shared/likelihood_functions.py (new), shared/recognizer.py
Reference: IR debugging session, behavior-verified against scenario_00

**TODO-20 — Persistent per-hypothesis tree cursor / notify_task_complete**
Recognizer currently re-derives "which action schema applies" fresh every
step by scanning the task tree (_get_relevant_action_schemas), rather than
tracking a persistent cursor per hypothesis. No explicit signal exists for
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
Files: domains/dock_loading/tasks.py, domains/dock_loading/scenarios.py, domains/dock_loading/registry.py
Reference: Phase 4C typed-parameter generalization session

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

**DESIGN-07 — Cognitive clock trigger conditions and θ hysteresis policy** [Phase 4 prereq]
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

**DESIGN-10 — Interference-detection sampling granularity** [Phase 4C, parked until _detect_interference implementation]
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

**DESIGN-12 — Horizon-projected confidence as recognizer output, not meta_planner computation** [parked, revisit during IR enhancement]
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

**LIMIT-06 — Robot task queue is pre-ordered in scenario file** [Phase 4]
Robot's `scheduled_tasks` is currently an ordered list in `AgentConfig`.
Ordering should be the meta_planner's responsibility. Accepted for Phases 1–3;
fix in Phase 4 via TODO-14.