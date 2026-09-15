# TeamRob Framework — Implementation Roadmap

Stages and outcomes only. Mechanisms and their rationale are in `docs/design_decisions.md`; the recognizer's
current state, parameters and guarantees are in `docs/recognizer_handback.md`; open items in
`docs/TODOS_AND_DEFERRED.md`. Where this file and those disagree, they win.

---

## Phase 1 — Foundations ✅
- Repo skeleton with `shared/` / `mesa_sim/` / `ros_sim/` separation
- `shared/types.py`: canonical dataclasses (`Observation`, `BeliefState`, `WorldState`, `GroundedAction`, `AbstractPlan`)
- `shared/io_contracts.md`: interface specification between cognitive and embodiment layers
- `shared/domain_knowledge.py`: `DomainKnowledgeBase`, `DomainModel` interfaces
- HTN Python object model: `TaskSchema`, `ActionSchema`, `MethodSchema`, `Var`/`Const` typed terms

## Phase 2 — Cognitive Layer Skeletons ✅
- `shared/recognizer.py`: skeleton with uniform prior
- `shared/planner.py`: skeleton — flat method grounder (single-level decomposition, first method unconditionally)
- `shared/replanning.py`: skeleton with `no_plan` trigger *(retired Sept 2026 — absorbed into meta_planner.py)*

## Phase 3 — Kitting Domain + Mesa Simulation ✅
- `domains/kitting/`: `tasks.py`, `actions.py`, `registry.py`, `scenarios.py`
- Layouts and scenarios (scenario ids are prefixed by layout number):
  `env_layout0` / `scenario_00` (Phase 4 dev), `env_layout1` / `scenario_10` (foreseeable tasks; dropped
  from the validation sweep in I2, **reinstated at R1/T9 on the cleaned layout** — no obstacles, coffee
  machine and AC switch side by side, item_1 near them; the old layout with obstacles is kept as
  `env_layout9`, not registered), `env_layout2` / `scenario_20` (collinear decoys),
  `env_layout3` / `scenario_30` (mid-approach reveal), `env_layout4` / `scenario_40` (F1, Sept 2026:
  a scripted deviation sequence — delivery, coffee break, a wander that is no task, a second delivery —
  the positive control for foreseeable-task recognition)
- `mesa_sim/sim_model.py`, `sim_agents.py`, `world_state_builder.py`, `obs_builder.py`
- `mesa_sim/action_decomposer.py`, `executor.py`, `run_mesa.py`
- Headless simulation runs correctly: human and robot agents complete full assigned task sequences
- `ProcessCompletion` contract in place; two predicate families (`in_zone`, `at`) correctly separated; the
  body emits `waited(agent, object)` when a wait ends (I2), so waits are observable to the recognizer

## Phase 2.2 — Mesa Visualization ✅
- Solara + Plotly interactive visualization layer (`mesa_sim/viz/`)
- Live agent positions, task progress, belief state display

## Phase 2.1 — Dock Loading Domain ✅ *(deferred since Phase 4C — must keep importing, is not run)*
- `domains/dock_loading/` modeled on HITS3 Scenario 2 (Olivia Stener / TRATON)
- Tasks: `DELIVER_PALLET` (assigned), `DRIVER_PHONE_CALL`, `DRIVER_TALKS_TO_DOCKWORKER` (foreseeable)
- Open non-blocking bugs: BUG-03, BUG-04 (see TODOS_AND_DEFERRED.md). Its action schemas were touched once
  since (I4b: the movement evaluator name), because recognizer construction now rejects an unregistered
  evaluator name — a check the domain must pass to import.

---

## Phase 4 — Full Cognitive Algorithms 🔄 (4A ⚠️ superseded by 4C-IR, 4B ✅, 4C 🔄, 4D 🔲)

### Conceptual design settled; 4A/4B/4C implemented

The robot operates with two planning levels and one recognition module, all in `shared/`:

**Module structure:**

- `shared/recognizer.py` — Bayesian IR, rebuilt I1–I5 (see 4C-IR below)
- `shared/likelihood_functions.py` — the evidence model's functions and its four constants
- `shared/target_resolution.py` — where a movement action's target is now (I2; shared by recognizer and projector)
- `shared/meta_planner.py` — task scheduling, candidate evaluation, cost comparison; supplies `min_separation` to realization and consumes its result (the 4C wait-decision revision moves interference detection out of it)
- `shared/projection.py` — `Projector` — task + world → predicted trajectory; consumed by meta_planner, and by viz/evaluation later. Realization (`realize()`, hold-only first) belongs on this side, not in `MetaPlanner`
- `shared/trajectory_algorithms.py` — pluggable path-realization and interference-detection functions; `earliest_violation` (closed form, the role reserved for `closest_point_of_approach()`) to be built here for realization
- `shared/planner.py` — HTN decomposer, called by meta_planner per candidate AND by the recognizer per hypothesis per tick
- ~~`shared/replanning.py`~~ — **retired Sept 2026**, deleted; trigger role absorbed into `evaluate_triggers()`

**Key design decisions for Phase 4:**

- Robot's `scheduled_tasks` list order carries no semantic commitment (see design_decisions.md) — it's the same field type/name as the human agent's, just not consumed as a schedule. Initial queue `Q0` is produced by the same update() mechanism used for every later reorder: evaluate_triggers()'s "no current task" condition fires on the first call, no IR confidence required to run it (IR runs from t=0 with a uniform prior regardless). No separate base-cost heuristic.
- `planner.py` becomes a true recursive HTN decomposer: if a StepCall names a TaskSchema (not a primitive ActionSchema), it recurses. Output remains a flat `AbstractPlan` (single task, executor-facing).
- `meta_planner.py` owns task selection. It calls `planner.py` per candidate task to project action sequences, evaluates costs, and selects the next task. HTN does not schedule — it only decomposes.
- Selection is **single-task, receding-horizon** (DESIGN-16): one best next task per trigger, re-decided from fresh WorldState and belief at the next trigger — not a search over orderings of the remaining pool. `full_reorder` is retained as a documented, switchable alternative but is not implemented.
- `ProjectedPlan` (DESIGN-06) is the meta_planner's internal reasoning structure, never handed to the executor. Under `single_task` it always holds exactly one entry; the multi-entry shape is retained for `full_reorder`.
- Interference detection is **geometric, not zone-based** — actual Euclidean distance between projected positions over time. `ProjectedPlanEntry` carries `Segment`s; `ConflictPoint` carries `position` + `distance`, no zone.
- Cost is measured in execution ticks (T2: projection steps are Mesa ticks; seconds in ROS): moves, detours, pauses all equal cost units. Since the 4C wait-decision revision a candidate's cost is its REALIZED duration — walking plus the holds placed to keep `min_separation` from the human — so a conflict is priced as time by construction (DESIGN-08 resolved). Team-level semantic costs parked as future extension (TODO-15).
- The robot can WAIT (4C wait-decision revision, Sept 2026): a hold is computed from the human's projection, enters the cost, and reaches the executor as an execution HINT the executor may refine but never re-decide or cancel. Waiting is not a branch — B2 realizes the current task alone and judges its hold; B3 realizes every candidate and takes the argmin. See design_decisions.md, "The robot can wait".
  Settled at R1 (Sept 2026, after T1b): one hold δ at the trigger position (whole-trajectory minimal
  shift); a violation is a distance below `min_separation` = 2.5 × motion per tick; realizable = no
  violation within [trigger, T_h], the tail unassessed; cost = T_r + δ; all-unrealizable → plain cost,
  logged; `b2a` continues when δ ≤ ρ × (T_h − trigger), ρ = 0.5; B3.A with realized cost.
- Projected walks end where the executor stops (T9): the body supplies its stopping distance to the
  `Projector` as it supplies its motion rate; `shared/` holds no simulator constant.
- Cancellation of a held-item task is handled by HTN method selection, not a meta_planner cost term — see design_decisions.md.
- The recognizer resolves nothing itself: targets, methods and completions are the planner's (I2). The scenarios are experiments for evaluating the algorithm, never its specification (I-series standing rule).

**Phase 4A — IR: Bayesian belief updating** ⚠️ SUPERSEDED — what it delivered and what replaced it

Delivered and still standing: the generalized hypothesis space (`TaskSchema.parameter_types`, cartesian
product over typed workspace objects — any number of enumerable parameters per task); `BeliefState` with
the full distribution, `most_likely` and `confidence`; `BELIEF_FLOOR = 1e-3` against probability collapse;
the assignment restricting the belief's SUPPORT, not its magnitude (the 10× multiplier removed).

Not delivered as described. 4A was recorded as "schema-driven dispatch via `PROGRESS_EVALUATORS`, no
hardcoded microaction strings in recognizer.py". The I1 audit (Sept 2026, `analysis/i1_ir_audit/`) measured
the likelihood that actually ran: 0 of 5,579 likelihood calls in any condition ever reached a completion
check; nine domain literals in the recognizer (`"?item"`, `"move_to"`, `"holding"`, `"in_zone"`, the two
foreseeable task names, …); the decomposition taken from `methods[0]`; and the belief carried by a cosine
heading kernel (HIGH 4.0 / LOW 0.1 / NEUTRAL 1.0) that multiplied identical headings tick after tick, a
`ZONE_BOOST`, and a held-item rule — so every documented "reveal" was a held-item pin of the alternatives.
4A as described was not complete; the likelihood model was rebuilt in 4C-IR below.

**Phase 4B — HTN: recursive decomposition in planner.py** ✅ COMPLETE

- Recursive decomposer with real guard evaluation, derived variable
  resolution, `?agent` binding propagation

**Phase 4C — MetaPlanner + recognizer rebuild** 🔄 (`single_task` path built and validated on scenario_00; the recognizer rebuilt and handed back; the meta-planner side resumed with T7/T8 and the wait-decision revision — realization designed, measured (T1b), decided (R1) and baselined (T9); to be built in T3 / T4 / T10)

Built and running end-to-end. All three tasks complete, correct terminal state, zero errors.

*Implemented (meta-planner side):*
- `shared/meta_planner.py` — public: `evaluate_triggers()`, `update_human_projection()`,
  `update()`; internal: `seed_tasks()`, `_is_complete()` (T7), `_detect_interference()`, `_cost()`
  — the last two are superseded in design by realization (below) and stay until it lands
- `shared/projection.py` — `Projector` extracted from `MetaPlanner`: `project()`
  (single-task path), `project_human()`, `build_segments()`, `estimate_duration()`.
  Injected into `MetaPlanner` rather than constructed by it — one instance, held by the
  agent, shareable with viz/evaluation
- `shared/trajectory_algorithms.py` — `straight_line_path()`, `stationary_segment()`,
  `discretized_time_sampling()`; `closest_point_of_approach()` and `obstacle_aware_path()`
  documented but deliberately unimplemented — now with assigned roles: the closed-form
  `earliest_violation` realization needs, and the detour strategy (4D)
- `shared/types.py` — `Segment`, `ConflictPoint` (retyped, zone-free),
  `InterferenceAssessment`, `ExecutorState`, `TriggerDecision`, `UpdateResult`,
  `task_instance_key()`; `ProjectedPlanEntry.spatial_zones` → `segments`
- `mesa_sim/sim_agents.py` — `RobotAgent` migrated off `replanning.py`; `task_index` and
  `_get_current_task_instance()` removed; `finished` flag added
- `domains/kitting/tasks.py` — third `MethodSchema` `deliver_already_held`, required by the
  re-decompose-from-scratch design (see design_decisions.md)
- `shared/replanning.py` — deleted
- T1 (conflict-geometry measurement, `analysis/t1_conflict_measurement/`) and T2 (projection in execution
  ticks; `min_safe_distance` exclusion now reachable) — measurement and units, no decision changed
- T7/T8 (Sept 2026): completed tasks leave the pool by world fact (`AdaptivePlanner.is_complete`);
  `unknown` is not admitted as a projection. `analysis/t7_t8_meta_bugs/` holds the meta-planner-side
  regression baselines from here on
- WAIT-DECISION REVISION (Sept 2026, documents only): T1 showed the fixtures' interference is a TIMING
  conflict (both agents reach the table within a tick), so the proportionate response is a short wait,
  which the robot could not express — its only lever was which task to do. Decided: the robot can wait.
  A per-candidate `realize()` (projection side; hold-only strategy first) holds each robot segment until
  `earliest_violation` against the human's projection clears at `min_separation`; the candidate's cost
  is the realized duration (walking + holds), so conflict is priced by construction; the winner's holds
  reach the executor as a HINT. Supersedes `_detect_interference()` as a B3 step, DESIGN-08 as posed,
  `min_safe_distance` as an exclusion threshold (now `min_separation`, the clearance to achieve) and the
  all-excluded `RuntimeError` (outcome open, TODO-30). B2 and B3 both consume realization: B2 realizes
  the current task alone and judges its hold δ; B3 realizes every candidate and takes the argmin.
  Whether B2 survives as a policy block is open (TODO-36). The one parameter before implementation is
  `min_separation`'s value, relative to scale (TODO-28). Full record: design_decisions.md, "The robot
  can wait"; new items TODO-70 (per-segment vs whole-trajectory holds), TODO-71 (the hint on the body side)
- T1b (Sept 2026, `analysis/t1b_realization/`): what realization would produce, measured on the live
  projections with four throwaway realizers over 13 separations — the design's per-segment loop
  overshoots the minimal hold and reverses argmins; the whole-trajectory shift and the per-segment
  minimal hold agree wherever both realize; every hold in the fixtures is a hold into the unassessed
  tail; all-unrealizable is absent below 50 cm. Measurement only; nothing in `shared/` changed
- R1 (Sept 2026, documents only): the decisions T1b raised, recorded — whole-trajectory minimal shift
  (TODO-70), a violation is a distance, Property 2 amended and the hold cap, cost = T_r + δ (TODO-69
  reading (1)), `realize()` not single-task, the hold as an executed hint at the trigger position
  (TODO-71), `min_separation` = 2.5 × motion per tick (TODO-28), all-unrealizable → plain cost logged
  `all_unrealizable` (TODO-30, TODO-52), `b2a` with ρ = 0.5 (TODO-36), B3.A with realized cost; the
  execution-time-avoidance assumption past T_h; fixtures (env_layout1 cleaned, env_layout9 kept
  unregistered, scenario_10 back in the sweep); TODO-73 to TODO-76
- T9 (Sept 2026): projected walks end where the executor stops — the body supplies its stopping
  distance (`PROXIMITY_THRESHOLD`) to the `Projector` as it supplies its rate; a per-tick actual
  robot–human distance measure (`[sep]`); new baselines over ten conditions (s00, s10, s20, s30, s40 ×
  prior off/on) that T3, T4 and T10 are built and judged on — `analysis/t9_arrival_radius/`

*Design questions resolved (Q1–Q4 from July 2026, plus September 2026 session):*
- Q1: `MetaPlanner` owns the task queue internally (not passed externally)
- Q2: human task projection uses `recognizer.get_hypothesis()` to resolve `belief.most_likely`
  back to its `HypothesisKey`; the recognizer is held **by reference** (same live instance the
  agent owns — `get_hypothesis()` is belief-stateless, so no staleness risk)
- Q3: `_estimate_duration` uses a self-contained geometric estimate (`distance / assumed_speed`)
- Q4: `replanning.py` retired in one commit after end-to-end validation ✅ done
- DESIGN-07 resolved: three triggers (`no_current_task`, `theta_crossed` as a *crossing event*,
  `task_committed`); θ=0.75, no hysteresis, confidence gate-only
- DESIGN-16 resolved: single-task receding-horizon selection; strategy flag for `full_reorder`
- Cancellation resolved (July): guarded HTN method, not a `_cost()` term
- Queue invariant: `_queue` excludes the executing task; candidates = `[current_task] + queue`
- Task exhaustion returned as `UpdateResult(current_task=None, queue=[])`, not raised
- ~~`_cost()` is hard-gate only — `conflicts` computed and carried but not priced (DESIGN-08)~~ — superseded
  by the wait-decision revision: `_cost()` becomes the realized duration; DESIGN-08 resolved by construction
- Q0 needs no bespoke heuristic — `no_current_task` covers t=0 and completion identically

**Phase 4C-IR — the recognizer rebuild, I1–I5 (Sept 2026)** ✅ handed back

Each stage staged its runs against the previous commit's logs with a reversion variant, so every behaviour
difference across the series is attributed (`analysis/i*/REPORT.md`). scenario_10 was dropped from the
sweep in I2 (its meta-planner crash is latent, TODO-52, and its belief tie order flaps without
`PYTHONHASHSEED=0`, TODO-42); the matrix is s00, s20, s30, scenario_40 × assignment prior off/on.

| stage | outcome |
|---|---|
| I1 audit | measured what the 4A likelihood actually did (above); no fixes |
| F1 fixture | `env_layout4` / `scenario_40`: the foreseeable-task and forced-reselection fixture 4C's "next" step asked for |
| I2 foundations | the recognizer resolves nothing itself: targets, methods, completions come from the planner and the schemas; typed bindings; `waited` observable; no domain literals in the evidence path |
| I3 phase model | a task's likelihood is the likelihood of the action it expects NOW, phase derived from the world every tick; terminal completion pins a task for the run; held-item rule and `ZONE_BOOST` removed |
| I4 evidence model | excess-path (wasted distance) likelihood in logistic form, detection reliability for completion signals, a stated constant `unknown`; the four parameters with physical meanings; the cosine kernel and HIGH/LOW/NEUTRAL removed |
| I4b boundary | the observed agent's own task completion is a boundary; the completion gate kept, with its exclusion stated |
| I4c episode semantics | the recognizer estimates the intention of the CURRENT behavioural episode: the belief re-initialises to the prior at the agent's task boundary; an empty movement stretch is not an observation; no persistence across episodes |
| I4d accounting | `unknown` folds with the stretch: a hypothesis's evidence is its odds against `unknown` over its own observations, verified by an independent accumulator on every tick (7e-15) |
| I5 hand-back | final matrix confirmed; guarantee statement, characterised limitations, open items — `docs/recognizer_handback.md` |

What the recognizer is now, in one line: per-hypothesis derived phase, action-level likelihood, excess-path
cost in logistic form, detection reliability, a constant `unknown`, an episode-local boundary and a terminal
pin. Four parameters, values and meanings in `shared/likelihood_functions.py` and the hand-back §2:
β = 0.01 /cm (detour tolerance), u = 0.1 (`unknown`'s per-observation likelihood, the unit of the
confidence ceiling 1/(1 + uⁿ)), detection hit / false-alarm rates 1.0 / 10⁻³, θ = 0.75 (the meta-planner's
gate, not a likelihood parameter). Two embodiment-side values are load-bearing: `PROXIMITY_THRESHOLD` = 30 cm
(when `at()` holds, hence when phases advance) and Mesa's straight-line walking (the Euclidean path cost is
exact only because of it).

Known properties of the evidence model — characterised, not defects (TODO-61; hand-back §4):
- (a) confirmation is length-blind: a fitting stretch scores the perfect fit after 15 cm as after 300 cm;
  evidence is strong at refutation, weak at confirmation;
- (b) accumulation is observation-count and decomposition sensitive: every fitting observation is worth 1/u
  whatever it observed, so how a method segments a trajectory sets how much evidence a hypothesis can gather.

*Validation gaps under 4C, checked against current state (Sept 2026):*
- TODO-28: DECIDED at R1 — `min_separation` = 2.5 × the robot's motion per tick (50 cm in Mesa),
  relative to motion so that it scales; the `assumed_speed` / time-scale half was RESOLVED by T2. Lands
  in code with T10; revisit under TODO-47 and ROS body sizes.
- TODO-29: `deliver_with_return` still unexercised under the MetaPlanner for the ROBOT. It is exercised every
  run by the recognizer for rival hypotheses of the human, and whether its guard is the right prediction there
  is now an open domain question (TODO-55 (e)).
- TODO-30: the interference exclusion branch is NOW EXERCISED (T2): candidates are excluded at `min_dist = 0`
  (scenario_20 steps 11 / 24) and every-candidate-excluded raises (scenario_10 step 257). Whether those
  exclusions are legitimate is TODO-28's question; what the robot does when everything is excluded is open.
  Under realization those exclusions become short holds; "infeasible" means no realization within the
  human's horizon. The all-unrealizable outcome is DECIDED at R1 (TODO-30): plain projected cost,
  logged `all_unrealizable`; the `RuntimeError` goes with T10. The scenario_10 figures above are from
  the old layout (stale since R1).
- TODO-32: `wait_at` duration still ignored in COST estimation (projector side). The recognizer side is done:
  waits are observable (`waited`) and `coffee_break` is recognised mid-walk in scenario_40. Now load-bearing:
  a human's projected occupation is the hold a robot task pays to pass it.

*Waiting on the meta-planner side (from the hand-back):*
- `theta_crossed` as an interface event (TODO-68, with TODO-48 and TODO-54): prior-off the true task can
  cross θ three times within one grasp stop, because rivals' `deliver_with_return` phases lift them briefly.
  The recognizer is correctly implementing its model and the contract in `io_contracts.md` promises a
  crossing event, not one crossing per task; whether the meta-planner needs a one-shot semantics is an
  interface decision, not an evidence-model one. Prior-on: one crossing per recognition.
- θ is a live-set-dependent bar (TODO-64, TODO-65); the guarantee statement (hand-back §3) says what the
  meta-planner may and must not assume, prior-on and prior-off separately.
- TODO-52's crash is resolved by decision (R1; the fallback is built in T10); TODO-67 (s30_off selects
  an already-delivered item) was fixed in T7; the context / knowledge-representation pass (TODO-66).

*The 4C queue (from R1, September 2026) — in this order:*
1. R1 + T9 — the decision record (this), projection ending at the body's stopping distance, the
   actual-distance measure, new baselines over ten conditions ✅
2. T3 — `realize()` as a service on the projection / trajectory side (whole-trajectory minimal shift,
   `earliest_violation` closed form, `RealizedPlan`), validated against T1b's `whole` realizer on the
   T9 baselines. Open before its numbers are read as exact: TODO-77 (T9 found the projection still
   1–6 ticks ahead of execution through the executor's acknowledgement ticks — a decision, not a fix)
3. T4 — `b2a`: B2 realizes the current task alone; continue iff δ ≤ ρ × (T_h − trigger), ρ = 0.5
4. T10 — B3.A with realized cost T_r + δ; the all-unrealizable fallback (plain cost, logged);
   `min_separation` = 2.5 × motion per tick replaces `min_safe_distance`; the `RuntimeError` removed;
   the hold δ on `UpdateResult`, executed by Mesa as STAND at the trigger position
5. D2 — what a trigger is an event of (TODO-68 / 48 / 54 / 64 / 65), decided from the T4 and T10 logs
6. T6 — ablation: B2 {none, b2a} × B3.A {plain, realized}, sweeps of ρ and of s (`min_separation`)
Later, not scheduled: TODO-47 (randomised layouts), TODO-32 (`wait_at` duration in projection),
`full_reorder` with `realize()`, TODO-70 (a hold at a chosen point along a segment), TODO-71 (the
hint's body-side details), TODO-73 (Mesa execution-time avoidance), TODO-74 (placement positions on
the table), TODO-75 (the ROS guide and `env_layout9`).

**Phase 4D — Low-level execution adaptation**
- Executor continues to handle within-action adaptation (detour, pause) guided by execution hints in AbstractPlan
- No structural change to executor interface; hints richer than current skeleton
- DESIGN-13's realization estimator is PARTLY PULLED FORWARD into 4C by the wait-decision
  revision: the PAUSE outcome is 4C's `realize()` with the hold-only strategy, `shared/`-resident
  (a hold needs only the two projections, no obstacle geometry), returning the placed plan and
  its duration. What remains 4D, as further pluggable strategies of the same function: DETOUR
  (go around — needs a path planner, `obstacle_aware_path()`'s role, and introduces iteration
  between trajectory and interference) and the OFF-THE-SHELF PLANNER (PRIEST or equivalent,
  ROS). For Mesa, a detour-capable realization can also serve as execution-time path
  realization (replacing straight-line `steps_toward`), collapsing cost-time and execution-time
  realization into one function. ROS keeps a two-tier split (this estimator for cost
  estimation, PRIEST for real execution) — still a dedicated design session away from being built
- The hold hint's consumption on the body side (execute, refine, never re-decide) is TODO-71;
  Mesa first — one hold δ at the trigger position, executed as STAND before the plan continues (R1)
- Execution-time avoidance past the human's projection is assumed, not built: Mesa's agents may
  overlap (TODO-73); T9 measures the actual robot–human distance per tick so that the assumption's
  cost can be reported

### Prerequisites before implementation

- DESIGN-06: define `ProjectedPlan` type in `shared/types.py` ✅ DONE
- TODO-14: `AgentConfig.scheduled_tasks` semantics split by agent type ✅ DONE (resolution text corrected Sept 2026 — robot list is an unordered *pool*, not a prioritised queue)
- DESIGN-07: cognitive clock triggers + θ policy settled ✅ DONE (no hysteresis; three triggers implemented)
- New simple kitting layout (Layout 0) and scenario for Phase 4 dev ✅ DONE (env_layout0/scenario_00)
- Q1–Q4 meta_planner design questions ✅ RESOLVED (see Phase 4C above)
- Typed-parameter object model (SimObject/is_portable/parameter_types) ✅ DONE, verified against scenario_00
- DESIGN-16: selection strategy (single-task vs. full reorder) ✅ RESOLVED (Sept 2026)
- Foreseeable-task / forced-reselection fixture ✅ DONE (F1: env_layout4/scenario_40, in the validation matrix)

---

## Phase 5 — Evaluation & Experiments 🔲
- Comparative evaluation: IR accuracy vs. ground truth (known human intentions from scripted human)
- Domains: kitting (the four sweep layouts), dock loading (deferred)
- Metrics, restated after 4C-IR (what each now means, and what it cannot mean):
  - IR: **reveal tick** — the first `theta_crossed` on the task actually under way, relative to the grasp
    (pre-/post-grasp); this is the "early recognition step", measured throughout I1–I5. **Wrong-task ticks
    above θ** and **crossings per recognition** replace "posterior convergence rate": confidence is
    non-monotone by design (it falls when the next expected action stops fitting), its ceiling 1/(1 + uⁿ)
    rises with the number of observations, and it depends on the live set's size — a convergence rate would
    measure the layout and the prior setting, not the recognizer. "Accuracy at task completion" is not
    measurable: at completion the task is pinned and the belief re-initialises; measure accuracy DURING
    execution (ticks above θ with the right winner), prior-on and prior-off separately.
  - AP: plan adaptation latency (ticks from `theta_crossed` to new queue adopted), reordering frequency —
    noting that prior-off a recognition can fire several crossings (TODO-68)
  - Team efficiency: total ticks to complete all tasks vs. baseline (no IR, fixed queue)
- Analytical tools filed for this phase, not built: the radius of maximum probability (TODO-62 — predict a
  reveal location from geometry, then check it) and the rationality measure (TODO-63)

## Phase 6 — ROS Embodiment 🔲 *(ROS team; `ros_sim/` paused)*
- `ros_sim/`: microaction classifier from sensor streams, symbolic WorldState builder, goal executor via ROS action servers
- Core `shared/` requires no modification for ROS integration
- Architectural interface already defined in `shared/io_contracts.md`
- Note: Phase 4 may add fields to `BeliefState` and introduce `ProjectedPlan` — ROS team should not build tightly against current `AbstractPlan` shape
- Before implementation: cognitive-clock trigger must be event-driven, never
  a fixed timer or derived from the motion-clock (PRIEST) tick rate; and the
  RESELECT/WAIT (or equivalent) decision must be made once, in `shared/` —
  the embodiment layer must only execute the returned decision, never run a
  parallel heuristic capable of independently producing or short-circuiting
  it. Both constraints surfaced concretely reviewing an early ROS
  integration attempt; see TODOS_AND_DEFERRED.md (NOTE on DESIGN-07, and the
  single-decision-path NOTE) before starting ros_sim/.
- The same rule applies to the HOLD the meta-planner will return with its decision (4C
  wait-decision revision; TODO-71): it is an execution hint — PRIEST may refine a hold as it
  refines any hint, but must not decide independently whether to wait, which task to run, or
  drop the hold silently. The cost was computed on that hold; a body that departs from it
  silently leaves neither the cost nor the behaviour authoritative.
- The recognizer now depends on the embodiment in four places the ROS team should know before building
  (hand-back §3.3):
  - **Paths are assumed straight.** The excess-path likelihood measures wasted distance against a Euclidean
    cost; in Mesa agents walk through obstacles so the true hypothesis's excess is exactly zero. In a real
    cell every detour around an obstacle is charged to the true hypothesis unless a path cost is injected
    (`IntentionRecognizer(path_cost=…)`). Every confidence figure in the hand-back is conditional on this.
  - **`PROXIMITY_THRESHOLD` = 30 cm** (`mesa_sim/world_state_builder.py`) decides when `at(agent, x)` holds,
    hence when every phase advances and every reveal happens. The ROS world-state builder must choose its
    own and expect every tick figure to move with it.
  - The body must emit the completion facts the schemas name — `at`, `holding`, `obj_at`, `waited` — as
    world predicates; the recognizer reads nothing else.
  - The completion channel's detection rates (hit 1.0, false alarm 10⁻³) describe Mesa's perfect reporting;
    set them from the real microaction classifier's measured rates.
