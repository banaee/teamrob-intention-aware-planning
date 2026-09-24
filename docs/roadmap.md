# TeamRob Framework — Implementation Roadmap

Stages and outcomes only. Mechanisms and their rationale are in `docs/design_decisions.md`; the recognizer's
current state, parameters and guarantees are in `docs/recognizer_handback.md`; open items in
`docs/TODOS_AND_DEFERRED.md`. Where this file and those disagree, they win. Terms are used as
`docs/glossary.md` defines them, in the phase records as in the plan: what a record CLAIMS is
untouched, only the words it claims it in.

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
  `env_layout99`, not registered), `env_layout2` / `scenario_20` (collinear decoys),
  `env_layout3` / `scenario_30` (mid-approach reveal), `env_layout4` / `scenario_40` (F1, Sept 2026:
  a scripted deviation sequence — delivery, coffee break, two AC-switch walks, a second delivery —
  the positive control for foreseeable-task recognition; F47b retyped the two walks' waypoints as AC
  switches so the script is well typed, baseline regenerated in `analysis/f47_fixtures/`).
  Evaluation fixtures, not in the regression sweep (F47 / F47b): `env_layout5` / `scenario_50`
  (scenario_20's end-state variant: the human steps aside for a coffee break), `env_layout7` /
  `scenario_70`, `scenario_71` (a foreseen human stay on the robot's route; alternative beside or
  across). `env_layout6` / scenario_60/61 (F47) are retired as ill-typed, kept unregistered as a record.
  Since F47b every scheduled and assigned task's bindings are type-checked at spawn (TODO-49).
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
- `shared/projection.py` — `Projector` — task + world → a `ProjectedPlan`'s segments; consumed by meta_planner, and by viz/evaluation later. Realization (`realize()`, hold-only first) belongs on this side, not in `MetaPlanner`
- `shared/trajectory_algorithms.py` — pluggable path-realization and interference-detection functions; `earliest_violation` (closed form, the role reserved for `closest_point_of_approach()`) to be built here for realization
- `shared/planner.py` — HTN decomposer, called by meta_planner per candidate AND by the recognizer per hypothesis per tick
- ~~`shared/replanning.py`~~ — **retired Sept 2026**, deleted; trigger role absorbed into `evaluate_triggers()`

**Key design decisions for Phase 4:**

- Robot's `scheduled_tasks` list order carries no semantic commitment (see design_decisions.md) — it's the same field type/name as the human agent's, just not consumed as a schedule. Initial queue `Q0` is produced by the same update() mechanism used for every later reorder: evaluate_triggers()'s "no current task" condition fires on the first call, no IR confidence required to run it (IR runs from t=0 with a uniform prior regardless). No separate base-cost heuristic.
- `planner.py` becomes a true recursive HTN decomposer: if a StepCall names a TaskSchema (not a primitive ActionSchema), it recurses. Output remains a flat `AbstractPlan` (single task, executor-facing).
- `meta_planner.py` owns task selection. It calls `planner.py` per candidate task to project action sequences, evaluates costs, and selects the next task. HTN does not schedule — it only decomposes.
- Selection is **single-task, receding-horizon** (DESIGN-16): one best next task per trigger, re-decided from fresh WorldState and belief at the next trigger — not a search over orderings of the remaining pool. `full_reorder` is retained as a documented, switchable alternative but is not implemented.
  REVISED (B3.B design revision, September 2026): `full_reorder` (B3.B) is designed and is the next build: a lookahead for the choice of the next task where geometry couples tasks (two-table kitting), not an order commitment. `single_task` stays the default. Entry in `design_decisions.md`, "B3.B (`full_reorder`) is lookahead for the choice of the next task, built next".
- `ProjectedPlan` (DESIGN-06) is the meta_planner's internal reasoning structure, never handed to the executor. Under `single_task` it always holds exactly one entry; the multi-entry shape is retained for `full_reorder`.
- Interference detection is **geometric, not zone-based** — actual Euclidean distance between projected positions over time. `ProjectedPlanEntry` carries `Segment`s, no zone.
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
hardcoded microaction strings in recognizer.py". The I1 audit (Sept 2026, `analysis/i1_ir_audit/` (deleted in the analysis cleanup, September 2026; carried in the I2 and I3 entries of design_decisions.md)) measured
the likelihood that actually ran: 0 of 5,579 likelihood calls in any condition ever reached a completion
check; nine domain literals in the recognizer (`"?item"`, `"move_to"`, `"holding"`, `"in_zone"`, the two
foreseeable task names, …); the decomposition taken from `methods[0]`; and the belief carried by a cosine
heading kernel (HIGH 4.0 / LOW 0.1 / NEUTRAL 1.0) that multiplied identical headings tick after tick, a
`ZONE_BOOST`, and a held-item rule — so every documented "reveal" was a held-item pin of the alternatives.
4A as described was not complete; the likelihood model was rebuilt in 4C-IR below.

**Phase 4B — HTN: recursive decomposition in planner.py** ✅ COMPLETE

- Recursive decomposer with real guard evaluation, derived variable
  resolution, `?agent` binding propagation

**Phase 4C — MetaPlanner + recognizer rebuild** 🔄 (`single_task` path built; the recognizer rebuilt and handed back; realization designed, measured, decided and BUILT — T3 the service, T4 `b2a`, T10 B3 on realized cost — then made total under robot-responsible separation (F1), with the execution-time separation stop in Mesa (C), blocked time as an outcome (R2), schema wait durations in projection (TODO-32) and typed scheduled bindings (F47b), and the trigger set settled (D2: `recognition_changed` against the decision record), and the policy components ablated (T6). The 4C queue is empty)

Built and running end-to-end. All three tasks complete, correct terminal state, zero errors.

*Implemented (meta-planner side):*
- `shared/meta_planner.py` — public: `evaluate_triggers()`, `update_human_projection()`,
  `update()`; internal: `seed_tasks()`, `_is_complete()` (T7), `_is_current_task_plausible()` (B2
  `b2a`, T4), `_replan_tasks()` (B3 on realized cost, T10). `_detect_interference()` and `_cost()`
  were removed at T10
- `shared/realization.py` — `realize(plan, human_plan, min_separation, decision_step) -> RealizedPlan`
  (T3): the whole-trajectory minimal shift on `shift_violation_interval()`; total since F1 (a clearing
  δ always exists; no `realizable` flag, no hold cap)
- `shared/projection.py` — `Projector` extracted from `MetaPlanner`: `project()`
  (single-task path), `project_human()`, `build_segments()`, `estimate_duration()`.
  Injected into `MetaPlanner` rather than constructed by it — one instance, held by the
  agent, shareable with viz/evaluation
- `shared/trajectory_algorithms.py` — `straight_line_path()`, `stationary_segment()`, `arrival_point()`;
  `obstacle_aware_path()` documented but deliberately unimplemented; `shift_violation_interval()` (T3,
  rewritten F1) is the closed form realization is built on; `discretized_time_sampling()` and
  `closest_point_of_approach()` removed at the 4C housekeeping (TODO-83)
- `shared/types.py` — `Segment`, `RealizedPlan` (T3), `ExecutorState`, `TriggerDecision`,
  `UpdateResult` (with `hold`, T4), `task_instance_key()`, `check_task_bindings()` (F47b),
  `ActionSchema.duration_key` (TODO-32); `ConflictPoint` and `InterferenceAssessment` removed
  (TODO-83); `ProjectedPlanEntry.spatial_zones` → `segments`
- `mesa_sim/sim_agents.py` — `RobotAgent` migrated off `replanning.py`; `task_index` and
  `_get_current_task_instance()` removed; `finished` flag added
- `domains/kitting/tasks.py` — third `MethodSchema` `deliver_already_held`, required by the
  re-decompose-from-scratch design (see design_decisions.md)
- `shared/replanning.py` — deleted
- T1 (conflict-geometry measurement, `analysis/t1_conflict_measurement/`) and T2 (projection in execution
  ticks; `min_safe_distance` exclusion now reachable) — measurement and units, no decision changed
- T7/T8 (Sept 2026): completed tasks leave the pool by world fact (`AdaptivePlanner.is_complete`);
  `unknown` is not admitted as a projection. `analysis/t7_t8_meta_bugs/` held the meta-planner-side
  regression baselines until T9; the current ones are F1's (`analysis/f1_robot_responsible/realized_none/`,
  with s10 superseded by TODO-32 and s40 by F47b — `analysis/f47_fixtures/`)
  (Analysis cleanup, September 2026: `analysis/t7_t8_meta_bugs/` is deleted, its numbers carried in
  design_decisions.md and TODO-67; F1's and F47's logs are dropped; the current baselines are the maintained
  sets named in CLAUDE.md, "Maintained baseline sets".)
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
  execution-time-avoidance assumption past T_h; fixtures (env_layout1 cleaned, env_layout99 kept
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
  `task_committed`); θ=0.75, no hysteresis, confidence gate-only. D2 (September 2026) replaced
  `theta_crossed` by `recognition_changed`: retention by identity against the decision record, the
  gate asked at admission only; the below-θ sub-question closed as hold, no band. D3 (September 2026)
  removed `task_committed`: two triggers, `no_current_task` and `recognition_changed`
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
β = 0.01 /cm (detour tolerance; supplied by the body since T-A1, `mesa_configs.yaml`), u = 0.1 (`unknown`'s per-observation likelihood, the unit of the
confidence ceiling 1/(1 + uⁿ)), detection hit / false-alarm rates 1.0 / 10⁻³, θ = 0.75 (the meta-planner's
gate, not a likelihood parameter). Two embodiment-side values are load-bearing: `PROXIMITY_THRESHOLD` = 30 cm
(when `at()` holds, hence when phases advance) and Mesa's straight-line walking (the Euclidean path cost is
exact only because of it).

Known properties of the evidence model — characterised, not defects (TODO-61; hand-back §4):
- (a) confirmation is length-blind: a fitting stretch scores the perfect fit after 15 cm as after 300 cm;
  evidence is strong at refutation, weak at confirmation;
- (b) accumulation is observation-count and decomposition sensitive: every fitting observation is worth 1/u
  whatever it observed, so how a method cuts a walk into phases sets how much evidence a hypothesis can gather.

*Validation gaps under 4C, checked against current state (Sept 2026):*
- TODO-28: DECIDED at R1 — `min_separation` = 2.5 × the robot's motion per tick (50 cm in Mesa),
  relative to motion so that it scales; the `assumed_speed` / time-scale half was RESOLVED by T2. Landed
  in B2 (T4) and B3 (T10). R2 records what the one value costs: it governs both crossing in the open and
  working side by side at a point place, where s ≤ 2r and opposite-side arrival would be needed (50 vs
  60 cm here: the rim only). Revisit under TODO-47 and ROS body sizes. REVISED (T-A1): supplied by the
  body in physical units (Mesa: `mesa_configs.yaml`, 50 cm), not 2.5 × motion per tick; set per body, not
  a scale-calibration item. Behaviour unchanged.
- TODO-29: `deliver_with_return` still unexercised under the MetaPlanner for the ROBOT. It is exercised every
  run by the recognizer for rival hypotheses of the human, and whether its guard is the right prediction there
  is now an open domain question (TODO-55 (e)).
- TODO-30: CLOSED (F1). Under robot-responsible separation a clearing hold always exists, so no candidate
  is unrealizable; the exclusion branch, the all-unrealizable fallback (built at T10) and the `RuntimeError`
  are all gone. The exclusion T10 still had (s20_on 57, a task 4 ticks from done dropped for a standing
  placement) was the finding that led to F1.
- TODO-32: CLOSED (R2). The wait duration is the method schema's (`PT60S`, `PT2S`), read from the grounded
  action through the schema's `duration_key` and converted by the embodiment's `duration_to_steps`
  callable; knowledge and behaviour match by construction. A mismatch experiment keeps the robot on the
  schema value and gives the human's instance its own.

*Waiting on the meta-planner side (from the hand-back):*
- `theta_crossed` as an interface event (TODO-68, with TODO-48 and TODO-54): prior-off the true task can
  cross θ three times within one grasp stop, because rivals' `deliver_with_return` phases lift them briefly.
  The recognizer is correctly implementing its model and the contract in `io_contracts.md` promises a
  crossing event, not one crossing per task; whether the meta-planner needs a one-shot semantics is an
  interface decision, not an evidence-model one. Prior-on: one crossing per recognition. DECIDED (D2):
  the trigger tracks the identity of the projected hypothesis, not the gate; a re-crossing of the same
  hypothesis fires nothing, a change of hypothesis or its end fires. No change to the recognizer.
- θ was a live-set-dependent bar (TODO-64, TODO-65); the guarantee statement (hand-back §3) says what the
  meta-planner may and must not assume, prior-on and prior-off separately. DECIDED (the gate ruling,
  September 2026): the dependence was the likelihood's, removed by graded evidence; the gate stays
  `confidence ≥ 0.75` on the normalised share. TODO-64 / 65 closed.
- TODO-52's crash is resolved by decision (R1; the fallback is built in T10); TODO-67 (s30_off selects
  an already-delivered item) was fixed in T7; the context / knowledge-representation pass (TODO-66).

*The 4C queue (from R1, September 2026) — in this order:*
1. R1 + T9 — the decision record (this), projection ending at the body's stopping distance, the
   actual-distance measure, new baselines over ten conditions ✅
2. T3 — `realize()` as a service on the projection side (whole-trajectory minimal shift,
   `shift_violation_interval` closed form, `RealizedPlan`), validated against T1b's `whole` realizer ✅
   (`analysis/t3_realize/` (deleted in the analysis cleanup, September 2026; carried in the T3 / T3b entry of design_decisions.md; realize() is re-validated by analysis/f1_robot_responsible/validate.py); T3b the whole-tick hold; L2 then removed the acknowledgement lag, TODO-77)
3. T4 — `b2a`: B2 realizes the current task alone; continue iff δ ≤ ρ × (T_h − trigger), ρ = 0.5;
   the hold δ on `UpdateResult`, executed by Mesa as STAND at the robot's position ✅
   (`analysis/t4_b2a/` (deleted in the analysis cleanup, September 2026; carried in TODO-36 and TODO-71); TODO-36, TODO-71, TODO-77)
4. T10 — B3.A with realized cost T_r + δ; `min_separation` replaces `min_safe_distance`; the
   `RuntimeError` removed; B3's winner's δ on `UpdateResult.hold`; the `[run]` header (TODO-78) ✅
   (`analysis/t10_b3_realized/` (deleted in the analysis cleanup, September 2026; carried in the T10 entry of design_decisions.md, TODO-36 and TODO-79); its all-unrealizable fallback was removed again at F1)
   Then, in order (all ✅, September 2026): T5 (a continue costs nothing), L2 (projection time includes
   the body's acknowledgement and observation offset), F1 (robot-responsible separation: rules (a)/(b),
   realization total, hold cap and fallback gone, the task-completion tick projected —
   `analysis/f1_robot_responsible/`), C (the execution-time separation stop in the Mesa executor, default
   off, same rule; the s / v tail rejected — `analysis/c_separation_stop/`), R2 (the point-place fact,
   one s for two situations, blocked time and human-borne proximity as outcomes, TODO-32 closed),
   F47 / F47b (typed scheduled bindings at spawn; the evaluation fixtures; a stay the projection carries
   is absorbed by realization — `analysis/f47_fixtures/`)
5. D2 ✅ (September 2026) — what a trigger is an event OF: a change in what `update()` decided on.
   `recognition_changed` replaces `theta_crossed`: the meta-planner records the hypothesis it projected
   (the decision record, one field) and fires when `most_likely` leaves it or when a task hypothesis
   first clears the gate with none recorded; TODO-48 / 54 / 68 are consequences, not cases. Robot-side
   triggers unchanged (until D3, which removed `task_committed`). The blocked-execution event (the separation stop's refusal as a fact in
   `ExecutorState`, per blocked episode, past B2, wait now / reconsider recorded) is designed, not
   built: under wait it cannot change a decision, and reconsider has no valid fixture (F47b), so it
   waits for TODO-80 or TODO-47. TODO-77 stays a projector accounting item. Entry in
   `design_decisions.md`; the re-baselined sweep in `analysis/d2_recognition_trigger/`
6. T6 ✅ (September 2026) — ablation of the meta-planner's policy components on the eight kitting fixtures:
   gate {none, b2a} × cost {plain, realized} × separation stop {off, on} × prior, and a ρ existence test.
   Gate and cost are not independent axes (b2a realizes the current task under either cost); the clean
   comparisons are none + plain against none + realized (realization) and none + realized against
   b2a + realized (commitment). Realization holds or switches at each fixture's one crossing; b2a took
   one commitment decision (s70 at ρ 1.0), which lost to the switch; the stop removes every robot-side
   violation at the cost of blocked time at the table. The s sweep was dropped: `min_separation` is a
   safety parameter set outside the planner, and no fixture result selects s, ρ or any other value.
   The review found one defect, fixed in the wrap-up: `update()` continued a current task its own pool
   had dropped as complete (B1.5). Completion is measured from the world fact from here on (the declared
   empty-pool tick minus 2). `analysis/t6_ablation/`; TODO-36
7. Graded evidence ✅ (September 2026) — a stretch's evidence against `unknown` is graded by the share of the
   hypothesis's expected path it covers: L / u^f, f = 1 at an arrival by the completion fact; u, β and θ
   unchanged, the I4d accounting invariant re-checked (7.1e-15). The one-task reveals follow the walk
   (θ at f ≈ 0.48) instead of the human's first step; no wrong task at θ; robot motion changed in six of
   sixteen conditions. New baselines: `analysis/g1_graded_evidence/sweep/`, replacing D2's. Entry in
   `design_decisions.md`, "A stretch's evidence against `unknown` is graded by the share of the expected
   path it covers"; `analysis/g1_graded_evidence/`; TODO-61 (a) closed for walks
8. The gate ruling ✅ (September 2026, documentation only) — on the graded-evidence θ data
   (`analysis/g1_graded_evidence/crossings.md`): the admission gate stays `_clears_gate` on the normalised
   share, θ = 0.75. The live-set dependence was in the likelihood, not the gate; under the grade a walk
   crossing sits at about 3:1 or more over `unknown` whatever the live-set size, higher while a rival is
   unrefuted. Not taken: odds against `unknown`, the ratio of the top two, θ from the live set or the
   layout, a rate-of-growth gate. TODO-64 / 65 closed; entry in `design_decisions.md`, "The gate stays a
   fixed share"

9. B3.B design revision ✅ (September 2026, documentation only) — `full_reorder` moves from retained
   alternative to next in the pipeline: one-table kitting is why order has not mattered; two-table kitting
   couples tasks by geometry; the whole robot ordering is realized against the one human projection inside
   [trigger, T_h]; the tail is a lookahead, re-priced at the next robot trigger. Prerequisites
   re-derived from the code: TODO-07 applies in part (retraction and object relocation in a hypothetical
   successor state, for projection only), DESIGN-12 does not apply, brute permutation is acceptable at
   pools of 3 to 5. Two points open with marked proposals: where a later task's hold is placed, and what
   B2 commits to. Entry in `design_decisions.md`, "B3.B (`full_reorder`) is lookahead for the choice of
   the next task, built next"; DESIGN-16 (revised), TODO-07, DESIGN-12, TODO-47 (f)

*Next step (superseded by "The plan from T-A" below, T-A1):* B3.B (`full_reorder`), in this order, each its own task: the two open points decided in
cchat (the hold placement before the realized-cost step at the latest); the successor state and
`Projector.project()` for orderings longer than 1; the two-table kitting layouts and scenarios (TODO-47
(f), hand-built); B3.B on plain cost, then on realized cost; the evaluation of B3.A against B3.B (plain
first, then realized; the one-table fixtures expected identical in choice). The order of the build steps
is a proposal of the design entry, not decided.

*After it (superseded, T-A1: the harness moved to T-F):* the randomised fixtures (TODO-47: generated layouts and scenarios, its prerequisites (a)
programmatic registration and (b) scale-relative calibration). They carry the one condition that reopens
the gate, a walk crossing with a live rival at similar odds (TODO-47 (g)), which no current fixture shows.

Later, not scheduled: TODO-80 (a declared unmodelled-behaviour condition: a stay no hypothesis describes),
Phase 4D (the detour
strategy, a hold at a chosen point along a segment TODO-70, human cooperation as the remedy for the
freezing robot TODO-15), TODO-74 (placement positions on the table), TODO-71 (the hint's body-side refinement and its reporting), TODO-75 (the ROS guide and
`env_layout99`, with the ROS side), TODO-81 (not behaviour-preserving as filed: dock_loading).
Phase 4C housekeeping (done): strict run options and the `[run]` header, `analysis/logparse.py`,
io_contracts §1.3 / §2.1 (TODO-72), TODO-82, TODO-83.

### The plan from T-A (T-A1, September 2026)

The 4C queue above is the record of what was done; this is the plan from here. Each item is a task name
later sessions use (T-B2, T-C1, ...). The state before this revision: `analysis/big_picture/STATUS.md`.
Reasoning: design_decisions.md, "The pipeline from T-A: what moved, and why".

- **T-A — Records.** T-A1: this revision (the decisions below; `min_separation` supplied by the body in
  physical units, the only code change, byte-identical). Then the handoff to the next design chat.
- **T-B — B3.B (`full_reorder`): a candidate is an ordering of the pool.** The head of the argmin
  ordering becomes the next task; the ordering past the head is lookahead, not an order commitment.
  - B1: two-table kitting layouts and scenarios, hand-built, after one design question: is an item's
    destination table a domain fact or a work-order fact (design_decisions.md, B3.B entry, "THE FIXTURE
    SIDE"; TODO-47 (f)). Registered programmatically, as the first part of fixture generation (TODO-47 (a)).
    T-B1c ✅ (September 2026): `scenario_83` on env_layout8, a fixture (Hadi's ruling): the existence case in
    which realized cost changes the head under `full_reorder` (a conflict after the head; step 159, head
    item_6 under plain cost, item_1 under realized, gap 1.44 < shift 3). `analysis/tb1c_realized_flip/`.
    KNOWN LIMIT: `analysis/tb1b_two_tables/permutation_costs.py` prices only from the robot's start over its
    assigned tasks, not from the position and pool at a decision; not extended.
    T-B1d ✅ closed as a record (September 2026, Hadi's ruling (ii)): no `scenario_84`, no layout variant; the
    designation pricing and the mechanism (the heads differ when the cheapest-from-here task ends at a table
    far from the remaining shelves, which the destination fact decides): `analysis/tb1d_designations/`.
    T-B1 IS COMPLETE. The fixtures for T-B3: scenario_80, scenario_81 (two tables), scenario_83 (the
    realized-cost existence case) and the one-table regression set.
  - B2: the build in the recorded order: the successor state and `project()` for orderings; B3.B on plain
    cost; then on realized cost; a `strategy` run option. Open points settled at design time: the hold at
    the boundary before the task it clears; B2 commits to a task.
    STATE (September 2026): T-B2a ✅ (`project()` chains the entries; the successor state from what the
    schemas declare), T-B2b ✅ (`full_reorder` on plain cost), T-B2d ✅ (`--strategy`), T-B2c ✅ (an
    ordering realized, one minimal-shift search and one hold per entry; orderings ranked on that cost).
    B3.B is complete. ~~No `full_reorder` baselines are recorded until Hadi confirms T-B2c.~~ Superseded by
    T-B3: the `full_reorder` baselines are in `analysis/tb3_full_reorder/`. OPEN for cchat:
    the projection's extra tick per entry with a `pick_up` accumulates over an ordering (TODO-77); it is
    an error in the input to `realize()` and is not compensated.
  - B3: B3.A against B3.B on the two-table fixtures, realized only, T-B3 (plain was T-B2b); the one-table
    fixtures byte-identical for the default run.
    T-B3 ✅ (September 2026): single_task beside full_reorder on s80, s81, s83, s20, s70 (realized, both
    priors), a comparison table and the first `full_reorder` logs, the diff target from here on (not an
    evaluation): `analysis/tb3_full_reorder/`.
- **D3** ✅ (September 2026): `task_committed` is not a trigger. A trigger is a change in what the last decision
  rested on (the human's hypothesis, the robot's task set); the robot's grasp was in the plan it priced. The
  trigger set is {`recognition_changed`, `no_current_task`}; no re-timing mechanism added. The ablation
  (`analysis/ablation_task_committed/`) changed nothing in the world in 26 pairs; the maintained baselines
  (tb1a, tb1b, tb1c, tb3) are regenerated. design_decisions.md, "D3: task_committed is not a trigger";
  TODO-90 (two in-window approaches under `b2a`) to be checked in a bounded task before T-C.
- **Two-table re-examination of the recognizer and B2** (a separate task, not scheduled): on two tables the
  carry walk is discriminative; projections of rival hypotheses diverge spatially; B2's outcome is more
  sensitive to which hypothesis was admitted; B3.A's own costs differ.
- **T-C — The human action script.** The human's scenario is a sequence of actions (`move_to` a target or
  a point, `pick_up`, `place`, `wait`, `stay`), run by the human executor on the scenario layer; the mind
  knows nothing of it; a part may still be written as a task, so the regression fixtures are unchanged.
  C1 design chat; C2 build. TODO-80's declared stay becomes one script action. design_decisions.md, "The
  human's scenario is an action script". Open item decided in C1: a stationary human (TODO-85): whether a
  stay is evidence (if so, a duration term, its own item T-H) and what `update()` does with `unknown` on top
  (candidate: the human projected stationary at its position for a bounded horizon); design_decisions.md,
  "A stationary human".
  T-C1 ✅ (23 September 2026): design_decisions.md, "The human action script (T-C1, decided)". The executed
  script is a flat list of primitives (`MoveTo`, `PickUp`, `Place`, `Stay`), a task expanded at load by
  `expand(task)` with provenance on each primitive; the author writes `interrupt`, `deviate`, `abandon`, free
  `Stay(n)` and `MoveTo(landmark)`; the human executor is action-level. TODO-86 closed. Not decided in C1:
  TODO-85 (half (b) with T-D; half (a), if taken, T-H) and TODO-88, their own items.
  - **T-C2 — the build.** C2a the script layer: primitives, `expand`, the vocabulary, landmarks, the
    provenance check (built, T-C2a). C2b the human executor, action-level, and sequential expansion against the
    successor state (`shared.projection.successor_state()`), not the initial world, so a task after an abandoned
    pick-up expands from what the human holds (built, T-C2b). Fixtures s00, s20, s70, s80, s83, prior on:
    the human's lines identical up to the dropped per-task completion tick; the human projection also loses that
    tick (the human's body reports 0), which moved one hold before the first dropped tick (s20 `single_task`);
    the baselines regenerated once. C2a and C2b closed.
    T-C2c ✅: the two literal scenarios (scenario_11, an interrupted delivery; scenario_01, a declared stay), one
    run each, observed (`analysis/tc2c_scripts/`). T-C closed.
  - From here debugging runs use prior on only; off / on returns for the paper.
- **T-D — Robustness in kitting, on T-C.** Scenarios for a change of mind mid-task, a walk to an empty
  corner (`unknown` as outcome), a declared stay at the table (the blocked case); the blocked event in
  `ExecutorState`, the trigger routed past B2, the reconsider policy (design in TODO-80 and D2); evaluation
  of retraction and re-recognition firing, `unknown` leading, blocked time and completion under wait
  against reconsider. design_decisions.md, "Robustness is tested in kitting".
  The recognizer pass (Q2 to Q4) opens with TODO-95: rule whether the stationarity channel joins it or stays
  recorded for T-H.
- **T-E — Demonstration.** The viewer shows belief, admitted projection, decision, hold, refusal; the run
  set covers switch and hold (s70 / s71), a two-table ordering, a change of mind, unmodelled behaviour; plain against
  realized, stop on, prior off. After T-B, T-C and T-D, so that it shows ordering, change of mind and
  unmodelled behaviour (and the belief's `unknown` leading), not only switch and hold.
- **T-F — Evaluation (Phase 5).** Fixture generation completed (the randomised harness, TODO-47); factors
  `cost_strategy` × `gate_strategy` × `strategy` × `separation_stop` × prior (B2 is a factor here, not a
  design step: TODO-36); metrics on `recognition_changed`, completion from the world fact, blocked time,
  wrong-task ticks. The comparison against expected realized cost over the belief is a later item of this
  phase (TODO-84).
  θ sensitivity analysis: runs across several θ values on the fixture set, reporting decision differences and
  `[sep]` violations; the gate is kept and justified by this sweep, with TODO-84 (the expected-cost branch,
  over per-hypothesis costs) and TODO-97 (the joint-realization branch) as the two recorded alternatives.
  The θ values for the sweep are chosen at T-F, not now.
- **T-G — Later, in this order:** a second domain in Mesa; 4D (detour); ROS.

The documentation pass for the paper comes before the paper, not before the demonstration.

Decisions recorded with this plan (T-A1), each where its entry lives: B2 is an evaluation factor (TODO-36
closed); the randomised harness moves to T-F, (f) stays in T-B, the separation half of (b) is removed and
β is not a scale item (TODO-47); β is a physical tolerance on wasted path, fixed on IR grounds (TODO-58);
the belief is used as a bar, not a magnitude, recorded as a limitation (design_decisions.md; TODO-84);
`min_separation` is supplied by the body in physical units (TODO-28; design_decisions.md).

**Phase 4D — Low-level execution adaptation**
- Executor continues to handle within-action adaptation (detour, pause) guided by execution hints in AbstractPlan
- No structural change to executor interface; hints richer than current skeleton
- DESIGN-13's realization estimator is PARTLY PULLED FORWARD into 4C by the wait-decision
  revision: the PAUSE outcome is 4C's `realize()` with the hold-only strategy, `shared/`-resident
  (a hold needs only the two projections, no obstacle geometry), returning the placed plan and
  its duration. What remains 4D, as further pluggable strategies of the same function: DETOUR
  (go around — needs a path planner, `obstacle_aware_path()`'s role, and introduces iteration
  between path realization and interference) and the OFF-THE-SHELF PLANNER (PRIEST or equivalent,
  ROS). For Mesa, a detour-capable realization can also serve as execution-time path
  realization (replacing straight-line `steps_toward`), collapsing cost-time and execution-time
  realization into one function. ROS keeps a two-tier split (this estimator for cost
  estimation, PRIEST for real execution) — still a dedicated design session away from being built
- The hold hint's consumption on the body side (execute, refine, never re-decide) is TODO-71;
  Mesa executes it (T4: one hold δ at the trigger position, STAND before the plan continues);
  refinement and its reporting stay open
- Execution-time avoidance past the human's projection: for Mesa it is the separation stop (C, a run
  option, default off) — the body refuses a STEP that would break robot-responsible separation against
  the human's actual position and stands instead; it cannot detour, so a human occupying the place the
  robot must reach blocks it until the human leaves (R2: blocked time is the outcome). The detour is
  4D's; with valid fixtures the stop fires only past T_h and where the human departs from its projection (F47b). `[sep]` (T9) measures
  the actual distance per tick; the stop-off baselines contain walk-throughs and support no safety claim

### Prerequisites before implementation

- DESIGN-06: define `ProjectedPlan` type in `shared/types.py` ✅ DONE
- TODO-14: `AgentConfig.scheduled_tasks` semantics split by agent type ✅ DONE (resolution text corrected Sept 2026 — robot list is an unordered *pool*, not a prioritised queue)
- DESIGN-07: cognitive clock triggers + θ policy settled ✅ DONE (no hysteresis; three triggers implemented;
  two since D3, `task_committed` removed)
- New simple kitting layout (Layout 0) and scenario for Phase 4 dev ✅ DONE (env_layout0/scenario_00)
- Q1–Q4 meta_planner design questions ✅ RESOLVED (see Phase 4C above)
- Typed-parameter object model (SimObject/is_portable/parameter_types) ✅ DONE, verified against scenario_00
- DESIGN-16: selection strategy (single-task vs. full reorder) ✅ RESOLVED (Sept 2026); revised Sept 2026: `full_reorder` designed, next build
- Foreseeable-task / forced-reselection fixture ✅ DONE (F1: env_layout4/scenario_40, in the validation matrix)

---

## Phase 5 — Evaluation & Experiments 🔲 *(T-F in the plan from T-A; the factors and metrics there supersede the list below where they differ)*
- Comparative evaluation: IR accuracy vs. ground truth (known human intentions from scripted human)
- Domains: kitting (the five regression fixtures and the evaluation fixtures, roadmap Phase 3), dock loading (deferred)
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

## Phase 7 (recorded, not scheduled): interactive deviations and a context stream 🔲 *(after T-G; nothing decided)*
- Run-time deviation events into the human executor from a viewer, replayable as pre-loaded scripts: live runs
  demonstrate, pre-loaded scripts evaluate.
- A context-knowledge stream into the world state, read by the recognizer: its own task.
- Communication as a robot action under a live `unknown` or block: its own task.
- Handoff: `docs/handoffs/phase7_interactive_deviations.md`.
