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
- Layouts and scenarios (serial ids since T-L stage 3; `docs/rename_table.md` maps the old ids, which the records
  below keep): `env_layout_01` / `scenario_s01_01` (Phase 4 dev), `env_layout_02` / `scenario_s02_01` (foreseeable tasks; dropped
  from the validation sweep in I2, **reinstated at R1/T9 on the cleaned layout** — no obstacles, coffee
  machine and AC switch side by side, item_1 near them; the old layout with obstacles is kept as
  `env_layout99`, not registered), `env_layout_03` / `scenario_s03_01` (collinear decoys),
  `env_layout_04` / `scenario_s01_06` (mid-approach reveal), `env_layout_05` / `scenario_s04_01` (F1, Sept 2026:
  a scripted deviation sequence — delivery, coffee break, two AC-switch walks, a second delivery —
  the positive control for foreseeable-task recognition; F47b retyped the two walks' waypoints as AC
  switches so the script is well typed, baseline regenerated in `analysis/f47_fixtures/`).
  Evaluation fixtures, not in the regression sweep (F47 / F47b): `env_layout_06` / `scenario_s03_06`
  (scenario_s03_01's end-state variant: the human steps aside for a coffee break), `env_layout_07` /
  `scenario_s05_01`, `scenario_s05_02` (a foreseen human stay on the robot's route; alternative beside or
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
- 30 September 2026: T-G in the plan from T-A (the second domain in Mesa).
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
- Interference detection is **geometric, not area-based** — actual Euclidean distance between projected positions over time. `ProjectedPlanEntry` carries `Segment`s, no area.
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
  SUPERSEDED IN PART (T-D R, 27 September 2026): the constant `unknown`, u and the ceiling 1/(1 + uⁿ) in the table, the one line and the parameters; the I4d row's odds against `unknown` (R1, R6). design_decisions.md, "T-D R and E".

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
   SUPERSEDED (T-D R, 27 September 2026): the grade leaves the belief (R1). design_decisions.md, "T-D R and E".
8. The gate ruling ✅ (September 2026, documentation only) — on the graded-evidence θ data
   (`analysis/g1_graded_evidence/crossings.md`): the admission gate stays `_clears_gate` on the normalised
   share, θ = 0.75. The live-set dependence was in the likelihood, not the gate; under the grade a walk
   crossing sits at about 3:1 or more over `unknown` whatever the live-set size, higher while a rival is
   unrefuted. Not taken: odds against `unknown`, the ratio of the top two, θ from the live set or the
   layout, a rate-of-growth gate. TODO-64 / 65 closed; entry in `design_decisions.md`, "The gate stays a
   fixed share"
   SUPERSEDED IN PART (T-D R1, 27 September 2026): reason superseded by R1; the gate stands; its justification is re-derived from Stage 1's admission measurement (G). Not reopened. design_decisions.md, "T-D R and E".

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

THE ORDER FROM 30 SEPTEMBER 2026 (ruled by Hadi; it supersedes every earlier statement of the order, here and in
the older records). Task letters are never reassigned; the order lives in this block and in CLAUDE.md's state
paragraph, not in the alphabet.

- THE PRESENT ORDER (Hadi, 3 October 2026; this block with V1 AND FW and the T-K bullet below): done T-A, T-B, T-C,
  T-H, T-L; T-D closed except its tail; T-G's stage 1 closed and T-G paused. Now: T-K part 1. Then: T-G's stage 2,
  track 4 (reduced form) and T-G's stage 3; T-F; T-V; track 3b; T-K part 2 at the end of the V1 queue. FW: the 4D
  detour, T-S, T-K's later directions. The numbered list below is the order of 30 September 2026.
- Done: T-A, T-B, T-C, T-H, T-L.
- (1) T-D close: tracks 1, L, P, 2.5, G, X and 3 are done; the MPB is CLOSED (its close-out, 30 September 2026).
- (2) T-G, the second domain in Mesa: dock_loading against `shared/` unchanged.
- (3) T-F, the evaluation (Phase 5), framed in TODO-144.
- (4) T-V, viewer, interface and interactive simulator: track 1 the viewer (T-E as originally defined), track 2
  Phase 7.
- (5) The T-D tail: track 3b (TODO-145); track 4 (TODO-140, TODO-131); the 4D detour strategy (TODO-70, TODO-15).
- (6) T-S, ROS/PRIEST (Phase 6), at the end of the queue.
- Unscheduled: the two-table re-examination of the recognizer and B2; belief-aware planning (TODO-97); the parked
  candidates TODO-132 (a), TODO-134, TODO-142, TODO-143 and P3. The documentation pass for the paper stays before the
  paper, not before the demonstration.
- Next: T-G's design, in a new design chat from a handoff.
- ADDED (Hadi, 2 and 3 October 2026; design_decisions.md, "T-K: context knowledge in the recognizer's belief";
  design_records.md, "T-K", THE TASK RENAMED: T-K AND ITS PARTS): T-K, context knowledge as a whole (K for knowledge), a
  task of the pipeline, not a stage of T-G, because it is framework-wide. T-K part 1 (V1, ongoing): crisp context
  knowledge (R1 to R8, AM1 to AM33). T-K part 2 (V1, at the end of the V1 queue, after track 3b): degrees (R5). Later,
  future work: the stream of context values with the world's dynamics, TODO-158 to TODO-161, TODO-163, TODO-164. A
  letter is never given to a different task; a task may be paused, resumed and revisited, and may hold a V1 part and a
  later part. T-G is paused after its stage 1; T-K part 1 runs now; T-G resumes at its stage 2 when T-K part 1 is
  closed.

V1 AND FW (Hadi, 1 October 2026, amended by Hadi 3 October 2026 for T-K; design_decisions.md, "T-G: the second domain's rulings", A1; T-G records 1). V1 is the first complete version of the framework,
the package for TeamRob and the publications: T-G (stages 1, 2 and 3, with track 4 in its reduced form after stage 2);
T-K part 1 and T-K part 2 (the amendment); T-F; T-V track 1 and track 2; the T-D tail's track 3b (TODO-145). FW (future
work, not designed, ruled or built within V1): the 4D detour; T-S; T-K's later directions (the stream of context
values with the world's dynamics, TODO-158 to TODO-161, TODO-163, TODO-164; the amendment); the conceptual directions
TODO-147 to TODO-150. The order block above is superseded in part:
track 4 leaves the T-D tail for its place inside T-G (after stage 2); the 4D detour and T-S leave the queue for FW. T-G
is open: its design is ruled (30 September and 1 October 2026) and build 1 is in (30 September 2026). Next, in order
(1 October 2026): the lifecycle question of the human's list (parked under A3), then the layout and the setup of T-G's
stage 1, agreed in the design chat, then stage 1's plan.
SUPERSEDED (T-G records 2, 1 October 2026): the lifecycle question is ruled (T-G Q12 to Q15; design_decisions.md, "T-G:
the second domain's rulings", A3, B13). Next: the layout and the setup of T-G's stage 1, then stage 1's plan. T-G's
order is stage 1, stage 2, track 4, stage 3; context knowledge (T-K part 1) runs between T-G's stage 1 and stage 2.
SUPERSEDED (Hadi and the design chat, 1 October 2026; design_decisions.md, "T-G: the second domain's rulings", B14): stage 1's rooms and setups are agreed. Next: stage 1's plan.
SUPERSEDED (Hadi, 1 October 2026; design_decisions.md, "T-G: the second domain's rulings", STAGE 1 PLAN APPROVED): stage 1's
plan is approved, `docs/handoffs/plan_T-G_stage1.md`. Next: stage 1's build, step 0, then step 1 (the rename).
SUPERSEDED (records, 1 October 2026; design_decisions.md, "T-G: the second domain's rulings", STAGE 1, STEPS 0 TO 5 BUILT): steps 0 to 5 of stage 1 are built and accepted. Next: the domain steps
6 and 7, then the milestone.
SUPERSEDED (records, 1 October 2026; design_decisions.md, "T-G: the second domain's rulings", STAGE 1, STEPS 6 TO 8 BUILT): steps 6 to 8 of stage 1 are built and the milestone
accepted. Next: the second simple scenario per room; then the sorting of the earlier analyses and tests under kitting,
with the preparation of the instruments; then the IRB scenarios, agreed with Hadi before they are authored.
SUPERSEDED (records, 1 October 2026; design_decisions.md, "T-G: the second domain's rulings", STAGE 1, THE SECOND MILESTONE SCENARIO BUILT): the second milestone scenario
is built and accepted; stage 1's milestone is complete. Next: the design of the IRB set with Hadi (first
question: TODO-155); then the sorting of the earlier analyses and tests under kitting, with the preparation of the
instruments; then the set's authoring and its runs.
SUPERSEDED (Hadi, 1 October 2026; design_decisions.md, "T-G: the second domain's rulings", T-G Q16's block, RULED, T-G records 8): TODO-155 is ruled
for now (the walk to the standby place stays without a hypothesis; H1 and H2 recorded, neither approved), office_break
lasts 90 seconds (TODO-157), and the IRB set on dock_loading is agreed (C1 to C14, M1 to M4, in all three
rooms). Next: the build step that sorts the earlier analyses and tests under kitting and prepares the instruments for
dock_loading; then the authoring of the set, its expectations and its runs.
SUPERSEDED (Hadi, 2 October 2026): the states after T-G Q16 are in the T-G entry below (stage 1's test-beds and close, the
housekeeping step); T-K is added (the order block above): its part 1's design is ruled, its build not started; its part 2
is at the end of the V1 queue. Next: T-K part 1's three open items, then its build's plan.
SUPERSEDED (Hadi, 3 October 2026; the T-K entry below, part 1's RULED line of 3 October 2026): T-K part 1's content
points 1 and 2 are ruled (AM10 to AM29); content point 3 (the tests) is open. Next: content point 3, then ccode's list
of the layouts with more than one A/C switch (AM19), then the build's plan.

- **T-A — Records.** T-A1: this revision (the decisions below; `min_separation` supplied by the body in
  physical units, the only code change, byte-identical). Then the handoff to the next design chat.
- **T-B — B3.B (`full_reorder`): a candidate is an ordering of the pool.** The head of the argmin
  ordering becomes the next task; the ordering past the head is lookahead, not an order commitment.
  - B1: two-table kitting layouts and scenarios, hand-built, after one design question: is an item's
    destination table a domain fact or a fact of the assigned tasks (design_decisions.md, B3.B entry, "THE FIXTURE
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
  stay is evidence (if so, a duration term, its own item, TODO-95; it was named T-H before 25 Sept 2026) and what `update()` does with `unknown` on top
  (candidate: the human projected stationary at its position for a bounded horizon); design_decisions.md,
  "A stationary human".
  SUPERSEDED IN PART (T-D R and E, 27 September 2026): whether a stay is evidence: time enters adequacy only, not the belief's likelihood (E3); "`unknown` on top" no longer occurs (R1). design_decisions.md, "T-D R and E".
  T-C1 ✅ (23 September 2026): design_decisions.md, "The human action script (T-C1, decided)". The executed
  script is a flat list of primitives (`MoveTo`, `PickUp`, `Place`, `Stay`), a task expanded at load by
  `expand(task)` with provenance on each primitive; the author writes `interrupt`, `deviate`, `abandon`, free
  `Stay(n)` and `MoveTo(landmark)`; the human executor is action-level. TODO-86 closed. Not decided in C1:
  TODO-85 (half (b) with T-D; half (a), if taken, TODO-95) and TODO-88, their own items.
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
- **T-H — The human behaviour model** (ruled by Hadi, 25 September 2026, with the rulings on the review; before
  T-D). CLOSED (26 September 2026): T-H1 to T-H4 built; the commits, the acceptance as measured and the deferred items
  (TODO-100, 101, 102, 105, 106, 109, the exporter, the label-C check) in `docs/handoffs/handoff_T-H.md`, its close-out. design_decisions.md, "T-H: the human behaviour model"; `docs/handoffs/handoff_T-H.md`. One tree of task
  schemas per use case (`WorkTask`, `PersonalTask`, `HumanOnlyTask`); each robot's task model, whole schemas of it
  chosen per experiment, a knowledge object of its own; the assigned tasks, a set; the human's script, an ordered list
  of fully bound task instances with typed events (`AfterAction` / `DuringAction` / `Now`; `Start` / `Drop`); the human
  executor owns a stack and writes a record, the ground truth (simulation only); coverage at two levels. `wait_at`
  stays; a `stand(?duration)` action is added. The robot's mind is unchanged. Each subtask is one session and follows
  CLAUDE.md's BUILD DISCIPLINE (a plan step confirmed by Hadi, then the build):
  - T-H1 the tree, the task model and the two knowledge objects; the `stand` action; the destination check's move;
    `dock_loading` and `ros_sim` begin their migration.
  - T-H2 the executor: `Event`, `Decision`, `Trigger`, `at`, `during`, `drop`, `inject`, the stack, the mid-action
    cut and the resumption rule, the record and its stream, the test that `world_state_builder` exposes nothing of the
    stack.
  - T-H3 the migration of the scenarios (and of `dock_loading`, `ros_sim`); deletion of the C1 vocabulary,
    `Deviation`, `Provenance`, `expand` / `resolve_script` as a separate form, the key-based checks, `Stay`,
    `MoveTo` / `PickUp` / `Place`. Built (25 Sept 2026): every scenario on the kitting call form; the `HumanOnlyTask`
    `go_to_and_stand` added to the kitting tree (design_decisions.md, T-H as built).
  - T-H4 the record's queries, `unperformed` and coverage; supersedes TODO-92. Built (26 Sept 2026): `world/queries.py`
    on the in-memory record, task equality `same_task`, the `[coverage]` line at load (design_decisions.md, T-H as
    built).
  Acceptance after each build: the 40 maintained baseline logs rerun; robot-side lines byte-identical; human-side
  differences listed and each explained; at the end of T-H3 the new logs replace the stored baselines.
- **Oracle-IR evaluation** (after T-H, its own pipeline task; TODO-101): three conditions on the same scenario, no IR,
  IR, and oracle IR (the meta-planner receives the record's `truth_at(tick)` instead of the belief, through that
  condition's explicit adapter only). Simulation only: a real human needs annotation of the record's form.
- **Alternative 1** (recorded as the next architecture direction, not scheduled): a human mind that generates the
  events, and a stack-aware IR.
- **T-L — Layouts, setups and scenarios: the three artefacts of a run** (ruled by Hadi, 26 September 2026). BUILT
  (26 September 2026, stages 1 to 4), before T-D. The facts one layout JSON holds today are separated by what they are about: the layout (the room: space,
  zones, fixed objects), the setup (the shift: movable objects, home containers, designated destinations), the
  scenario (the episode: agents, script, purpose, the setup it binds, its reference layouts); a run is the triple plus
  the run facts, validated at load. The mind receives the same facts through `WorldState`; the recognizer, planner and
  projector do not change. kitting and dock_loading migrate together; ros_sim stays parked (TODO-111). Each stage is
  its own ccode task:
  - stage 1: types (`ScenarioConfig` gains `setup` and `reference_layouts`, loses `name`), loader, resolver,
    validator; every registered layout split into a layout file and a setup file, object ids unchanged, the dead spawn
    entries deleted (`env_layout99.json` stays an unregistered file); scenarios unchanged in content and id; the tests'
    helpers move with the registry shape; the setup id added to the `[run_mesa]` line. Its docs pass covers the lines
    the T-L survey found contradicted (kept here so it is not lost): CLAUDE.md, `domains/` holds "schemas, layouts,
    scenarios" (no setups); CLAUDE.md, "Current phase", "Next is T-D"; CLAUDE.md, Running and the regression table
    (`--layout` given as required; the old ids, until stage 3); CLAUDE.md, the `env_layout99.json` line;
    `docs/handoffs/handoff_T-D_onward.md` §3, T-B1d, "the destination is a layout fact", and §5, "Next, in order: 1.
    T-D"; `docs/glossary.md` §6 **departure** ("where the layout designates") and **task model** ("built from the task
    model and the layout"), §6 **coverage** and §7 label B ("task model and layout"), all to read layout and setup;
    the T-H follow-up entry of design_decisions.md, "`ScenarioConfig` keeps its fields (id, name, description,
    agents)", to be marked superseded; the `env_layout` comment on `ScenarioConfig` in `shared/types.py`; and
    `domains/README.md`, `README.md`, `shared/io_contracts.md`, which stage 1 rewrites.
  - stage 2: the scenarios package (one module per theme), registration by discovery; `list_scenarios` and the tests'
    helpers on the declared pairs. AMENDED (Hadi, 26 Sept 2026, the stage-2 task): the division is one module per
    setup, `scenarios_sNN.py`, and the setups are finished in stage 2 — the identical setups merged and the final
    ids `env_setup_NN` given — because the module division keys on the setup serial; scenario and layout ids stay
    old until stage 3.
  - stage 3: the serial ids (ruling 4 as amended 26 Sept 2026: `env_layout_KK`, `env_setup_NN`, `scenario_sNN_MM`;
    the setup ids were finished in stage 2),
    the identical setups (0 = 3, 2 = 5) merged before numbering so numbering is done once [DONE IN STAGE 2], `docs/rename_table.md`
    (which says in one line that the frozen analysis scripts stay
    frozen at their commit), the four maintained sets regenerated under the new names, sweep scripts and READMEs.
    BUILT (26 Sept 2026): layouts `env_layout_KK` and scenarios `scenario_sNN_MM` in both domains, the variable the
    id; `docs/rename_table.md`; the four sets regenerated as `<layout id>_<scenario id>_<run options>.log` (tb1a gained
    its own `sweep.sh`; tb3 keeps all 20 runs), differing from stage 2 in the `[run_mesa]` line alone, every `.rec`
    byte-identical; one superseding line in each frozen analysis README.
  - stage 4: the run file and the override mechanism (three overridable facts: an agent's `start_position`, a fixed
    object's position, a movable object's home container), the viewer reading it.
    BUILT (26 Sept 2026): `--run` (replacing `--experiment`) and `--override <path>=<value>`, the paths
    `scenario.<agent>.start_position`, `layout.<object>.position`, `setup.<object>.initial_container`, the same in the
    run file's `overrides:` block (`mesa_sim/overrides.py`); applied by the loader before every check; printed as
    `[run_mesa] override …` after the start line; the viewer shows the run file and writes the three kinds into it
    (`ruamel.yaml`, comments kept). A run with no overrides byte-identical to stage 3; the four sweeps unchanged.
  Acceptance at every stage: the four maintained sweeps run from scratch and diffed against the previous stage's
  logs, no difference outside the lines the stage names (the triple line, the ids); AND pytest green. dock_loading's
  TODO-104 stands and T-L must not worsen it. design_decisions.md, "Layouts, setups and scenarios: the three artefacts
  of a run".
- **T-D — Robustness in kitting, on T-C.** NEXT after T-L (was next after T-H's close-out; `docs/handoffs/handoff_T-D_onward.md`, its
  section "What T-D now stands on"). (Resumes on T-H's structure: T-D Q1 stays "what the robot infers and does
  when no hypothesis explains the evidence, inside `unknown` or outside it", with the record's ground-truth cases: a
  switch to a modelled task, a switch to a modelled task outside the support, a switch to an unmodelled task, a
  binding-level deviation, no task on the stack, an
  episode's first ticks.) Scenarios for a change of mind mid-task, a walk to an empty
  corner (`unknown` as outcome), a declared stay at the table (the blocked case); the blocked event in
  `ExecutorState`, the trigger routed past B2, the reconsider policy (design in TODO-80 and D2); evaluation
  of retraction and re-recognition firing, `unknown` leading, blocked time and completion under wait
  against reconsider. design_decisions.md, "Robustness is tested in kitting".
  The recognizer pass (Q2 to Q4) opens with TODO-95: rule whether the stationarity channel joins it or stays
  recorded (TODO-95; "T-H" named it before 25 Sept 2026).
  SUPERSEDED IN PART (T-D R, 27 September 2026): `unknown` as outcome and `unknown` leading as a measure: the `unknown` hypothesis leaves the hypothesis space (R1); the outcome is the adequacy finding (R2). T-D R and E is ruled; its Stage 1 is next. design_decisions.md, "T-D R and E".
  SETTLED BY T-D R (27 September 2026): "inside `unknown` or outside it": outside; the adequacy finding takes the explanatory role; T-D Q1 itself unchanged, P's building block. design_decisions.md, "T-D R and E".
  CLOSED EXCEPT ITS TAIL (Hadi's order, 30 September 2026): tracks 1 (the IRB), L, P, 2.5, G, X and 3 (the
  MPB, CLOSED at its close-out) are done; design_decisions.md, the entries of those names. "NEXT after T-L" above is
  history. The T-D tail runs after T-V: track 3b, consequential activation under conflict (TODO-145); track 4, the
  workspace boundary and departure (TODO-140, TODO-131); the 4D detour strategy (TODO-70, TODO-15), the planner's
  remedy for the freezing robot (Phase 4D below).
  SUPERSEDED IN PART (T-G A1, A8, 1 October 2026): track 4, in its reduced form (monitored areas), is placed after T-G's
  stage 2 (TODO-140); the 4D detour is FW. Track 3b stays after T-V, in V1.
- **T-E — Demonstration.** The viewer shows belief, admitted projection, decision, hold, refusal; the run
  set covers switch and hold (scenario_s05_01 / scenario_s05_02), a two-table ordering, a change of mind, unmodelled behaviour; plain against
  realized, stop on, prior off. After T-B, T-C and T-D, so that it shows ordering, change of mind and
  unmodelled behaviour (and the belief's `unknown` leading), not only switch and hold.
  SUPERSEDED IN PART (T-D R, 27 September 2026): "the belief's `unknown` leading" no longer occurs (R1); what the demonstration shows in its place is not ruled. design_decisions.md, "T-D R and E".
  SUPERSEDED (30 September 2026) by T-V, track 1; T-E in older records means the viewer.
- **T-F — Evaluation (Phase 5).** Fixture generation completed (the randomised harness, TODO-47); factors
  `cost_strategy` × `gate_strategy` × `strategy` × `separation_stop` × prior (B2 is a factor here, not a
  design step: TODO-36); metrics on `recognition_changed`, completion from the world fact, blocked time,
  wrong-task ticks. The comparison against expected realized cost over the belief is a later item of this
  phase (TODO-84).
  θ sensitivity analysis: runs across several θ values on the fixture set, reporting decision differences and
  `[sep]` violations; the gate is kept and justified by this sweep, with TODO-84 (the expected-cost branch,
  over per-hypothesis costs) and TODO-97 (the joint-realization branch) as the two recorded alternatives.
  The θ values for the sweep are chosen at T-F, not now.
  REVISED (Hadi's order, 30 September 2026): T-F follows T-G and is framed in TODO-144; the randomised harness
  (TODO-47) stays in it. Tracks: kitting, dock_loading, cross-domain. The conditions as ablations (admission off,
  realization off, prior off a diagnostic), the measures, and the deviation dimension, as TODO-144 records them.
  Prerequisites: TODO-137 (the fallback-only control), TODO-135 (the near-encounter scenario), the evaluation scenario
  sets, MPB-5's horizon (TODO-138). Scope of the evaluation set: the human stays in the room and ends with the exit
  walk to the corner (docs/assumptions.md 1.1, 2.3); no genuine departure (track 4 follows T-F). LIMITATION OF ITS
  READING (recorded): track 3b follows T-F, in the T-D tail, so an evaluation before 3b measures without knowing that
  the adaptive branches fire under conflict; it cannot test behaviour in which the human projection conflicts with the
  robot's plan.
  T-G (1 October 2026; design_decisions.md, "T-G: the second domain's rulings", A8, A11): track 4's reduced form now comes before T-F (after T-G's stage 2).
  SCOPE REVISED (Hadi, 1 October 2026): T-F may use the unmonitored office on dock_loading; kitting's part of T-F stays
  without a departure; "no genuine departure (track 4 follows T-F)" above is superseded for dock_loading, and the
  details belong to T-F's own design. A layout authored so that routes cross shows that
  the robot adapts when an interaction exists, not how often interactions occur: T-F varies the placement and takes no
  interaction rate from crossing setups alone (TODO-144).
- **T-G — The second domain in Mesa: dock_loading** (revised by Hadi, 30 September 2026; before, "Later, in this
  order: a second domain in Mesa; 4D (detour); ROS": 4D moved to the T-D tail, ROS to T-S).
  `domains/dock_loading/` against `shared/` unchanged, executed by the Mesa body. Purpose: test whether the
  recognizer, the gate, the projection and the meta-planner stay domain-independent on a second task model.
  - The domain's task model: the assigned tasks, the foreseeable tasks (the phone call, talking to the dock worker),
    unmodelled behaviour; the driver's work order.
  - The domain's own elements: the truck as a container, the gate state as a method guard.
  - TODO-25's schema fixes (TODO-81 with them).
  - The script vocabulary, one controlled layout, setups and scenarios, following T-L.
  - The IRB, then the MPB, run on it; findings classified by the case classification of
    `docs/assumptions.md` and under MPB-4.
  - A shared ruling reopens on design grounds only; nothing domain-specific enters `shared/`.
  SUPERSEDED IN PART (T-G records 1, 1 October 2026): "the driver's work order" and the foreseeable candidates (the phone
  call, talking to the dock worker) are wrong under B1: the robot replaces the driver (an automated forklift), the
  observed human is the warehouse staff member who receives the delivery, and those candidates belong to the driver's
  role, which the robot holds; "work order" was superseded by "assigned tasks" at T-H. "The gate state as a method guard"
  reads: the gate open or closed, a state declared in the setup, opened on request (B5). "TODO-81 with them": TODO-81 was
  done in T-H1 (e571eed). "`shared/` unchanged": the rulings change `shared/` and `world/` where they are framework-wide
  (A3, A4, A5, A7, A8), each with its acceptance on kitting; nothing domain-specific enters `shared/`.
  RULED (Hadi, 30 September and 1 October 2026; design_decisions.md, "T-G: the second domain's rulings"; the parts keep their scope: A framework-wide, B
  dock_loading only, C staging). BUILD 1 (30 September 2026; 56e674e, 6e29c15, 62ebc4e): the form-only repairs and the
  viewing fixture scenario_s01_03; scenario_s01_01 and _02 still fail at load by intent (C2). The stages, all in V1;
  before each stage's plan the design chat and Hadi agree its layout and setup:
  - Stage 1, the basic domain: the robot delivers and returns (B11); the human scans, takes the two breaks, steps aside
    to the standby place; the gate is declared open; the office door has no state yet. The IRB, then the MPB.
    Its catch-up list is C3 (the domain's state after build 1).
    BUILDS: first, in its own commit with no change of behaviour, the zone mechanism renamed to "area" in the code (the
    plan reports the extent first: every occurrence, and whether the maintained sets' logs print it); the catch-up of
    dock_loading's forms to kitting's (C3); A3, the human's script form (`world/`), with the standby entry, once the
    lifecycle of a list entry is ruled (PARKED, the next design chat's first question; RULED 1 October 2026, T-G Q12 to
    Q15: open and closed entries, the repeatable standby entry, the dependence declaration for the load-time check, the
    closing part; dock_loading's closing part is the walk to the desk, a landmark that enters stage 1's layout, B13); A4, liveness by applicability (`shared/`); A5, generic object states and designations (used for the
    scanned state, `is_empty` and the destination); A6, the perception assumption; A9, the declared areas and the fact
    that an agent is in an area; B1 to B4, B8, B9, B11; B6 with `office_break` reduced (the office door has no state, the
    human passes it as a plain point; the office observed); B10, the room (whether the stores and the freezer are
    already in stage 1's layout is not ruled); the IRB on dock_loading, then the MPB. A3, A4, A5 and A9 change
    code outside the domain; each is accepted on kitting by the maintained sets staying byte-identical. A3 also by
    the kitting scenarios with a drop event and the test-bed sets with misdeliveries, run under the new form and
    compared with their present behaviour (expected: no difference; a difference returns to the design chat). The form
    built for A5 admits a fact that no action changes and that is not the state of a movable object (none authored in
    stage 1).
    R1 and R2 (Hadi, 1 October 2026; design_decisions.md, "T-G: the second domain's rulings", A3 and C1): every
    repeatable entry stands below every ordinary entry (the loader refuses another placement), and the load-time replay
    does not execute repeatable entries (R1); framework-wide, after a movement action the computed successor state
    represents the agent's resulting area consistently with the area fact the environment would emit, one definition for
    both; the plan names the shared representation and every consumer of a computed state that decomposes a later task,
    and proposes the form; acceptance on kitting byte-identical (R2).
    ROOMS AND SETUPS (Hadi and the design chat, 1 October 2026; design_decisions.md, "T-G: the second domain's rulings", B14): three rooms, env_layout_02, env_layout_03 and env_layout_04 (the
    hall, the office, the gate, the truck, the desk and the standby landmarks identical; the bays, the empties container
    and the coffee machine placed per room), and six setups, two kinds per room (kind 1 for the IRB: pallets in
    their delivery bays and one in the truck; kind 2 for the MPB: pallets in the truck, two empties); the empty pallets
    designated to the truck. env_layout_01, env_setup_01 and scenario_s01_01 to _03 are removed. Full observation in
    stage 1. A milestone before the IRB: one simple scenario per room runs from start to end. B10's room moves to
    stage 2.
    PLAN APPROVED (Hadi, 1 October 2026; design_decisions.md, "T-G: the second domain's rulings", STAGE 1 PLAN APPROVED;
    the plan, `docs/handoffs/plan_T-G_stage1.md`): the build order, steps 0 to 8: the rename; the areas and R2 (one
    definition of an agent's area; a fixed object's area derived from its position; the replay's walk ends where the body
    stops); A4; A5; A3; dock_loading's catch-up; its content (a method for every area the agent can be in: 8 per robot
    task, the human's for the hall and the office); the milestone, one scenario per room. Then the IRB and the
    MPB, whose instruments obtain the human's run-time sequence from the executor's own selection rule. A robot task with
    no applicable method stops the run: a ruling before stage 2 (TODO-152).
    BUILT, STEPS 0 TO 5 (1 October 2026; design_decisions.md, "T-G: the second domain's rulings", STAGE 1, STEPS 0 TO 5 BUILT): step 0 the reference runs (outside git); step 1 the rename
    (8d064ca, c21f001); step 2 the areas and R2 (b513b82, 9bca721); step 3 A4 (bd4bddc); step 4 A5 (b74485b); step 5
    A3 (048a36e); each accepted on kitting byte-identical, A3 also on the drop scenarios and both test-bed sets. Next:
    step 6 (dock_loading's catch-up) and step 7 (its content), then the milestone (step 8).
    BUILT, STEPS 6 TO 8 (1 October 2026; design_decisions.md, "T-G: the second domain's rulings", STAGE 1, STEPS 6 TO 8 BUILT): step 6 the catch-up
    (670cb78, 610fed9); step 7 the content (1492789, 512a452); step 8 the milestone (52b2aae, 8b9d267): scenario_s03_02,
    s05_02, s07_02, one per room; the acceptance held in all three (the robot completes both tasks at world ticks 64 and
    125, 64 and 125, 57 and 151; every entry of the human's script closed, the closing part included). The findings are
    recorded there (TODO-135's third instance, TODO-154 to TODO-157). ADDED (Hadi, 1 October 2026): a second simple
    scenario per room (the milestone did not exercise the standby walk or a meeting at a shared bay); then a step before
    the IRB and the MPB on dock_loading: the earlier analyses and the tests sorted under kitting, the instruments'
    code shared, their run sets, expectations and reports per domain (its own commit, no change of behaviour), with the
    preparation of the instruments. Next: the second simple scenario per room; then that step; then the IRB
    scenarios, agreed with Hadi before they are authored.
    BUILT, THE SECOND MILESTONE SCENARIO (1 October 2026; design_decisions.md, "T-G: the second domain's rulings", STAGE 1, THE SECOND MILESTONE SCENARIO BUILT):
    scenario_s03_03, s05_03, s07_03, one per room on the MPB setups (0371035): the robot delivers two pallets to the dry
    bay and one to the frozen bay and returns one empty pallet; the human scans the three, walks to the standby place
    between scans and closes at the desk. The acceptance held in all three rooms (the robot's last task completes at
    world tick 289, 276, 285; every entry of the human's script closed, the closing part included). Exercised: the
    priority rule, the standby walk, the frozen bay, each scan entering the live set on the tick of its delivery. Not
    exercised: the robot arriving at a bay where the human stands, two scans at once in one bay (the human finishes a
    scan before the next pallet arrives). Findings recorded there (TODO-135's fourth instance, TODO-145, TODO-154,
    TODO-155). Stage 1's milestone is complete. Next: the design of the IRB set with Hadi (first question:
    TODO-155); then the sorting step with the preparation of the instruments; then the set's authoring and its runs.
    RULED, THE IRB SET (Hadi, 1 October 2026; design_decisions.md, "T-G: the second domain's rulings", T-G Q16's block, RULED, T-G records 8):
    T-G Q16, the walk to the standby place stays without a hypothesis for now, the IRB set observing how the
    present recognizer explains it (the baseline); two candidates on TODO-155, neither approved (H1, a foreseeable task
    to step aside; H2, a hypothesis live only while no assigned task of the human is applicable); the walk as the scan's
    tail not taken. `office_break` lasts 90 seconds, `coffee_break` stays 60 (TODO-157; the value changed in the next
    build step). The set: 14 controlled scenarios (C1 to C14) and 4 mixed (M1 to M4), each in all three rooms on the
    room's IR setup; the controlled ones run and read first; expectations derived from the records before the runs;
    nothing adjusted to a result; for the standby walks (C13, C14, M4) the predictions under H1 and H2 written down
    beside the present model's expectation, which alone is compared. Next: the build step that sorts the earlier
    analyses and tests under kitting and prepares the instruments for dock_loading; then the authoring of the set, its
    expectations and its runs.
    BUILT, RUN AND ACCEPTED, THE IRB ON DOCK_LOADING (1 to 2 October 2026; accepted by Hadi 2 October 2026; design_decisions.md, "T-G: the second domain's rulings", STAGE 1, THE IRB ON DOCK_LOADING BUILT, RUN AND ACCEPTED;
    T-G records 9): the sort of kitting's analyses and tests (analysis/kitting/, analysis/instruments/,
    analysis/dock_loading/; the path table in docs/rename_table.md); the instruments prepared (the human's run-time
    sequence from the executor's own selection rule, the oracle with liveness by applicability, the separation counts
    with the passing and the standing human told apart); office_break at 90 seconds; the 54 scenarios (scenario_s02_02
    to _19, s04_02 to _19, s06_02 to _19); the expectations committed before the runs. 42 controlled and 12 mixed runs,
    zero disagreements: the recognizer behaves on dock_loading as the records specify; this does not establish the
    quality of the recognition. The baseline: 98 of 147 true stretches in the support reach the threshold (38, 40, 20 of
    49 by room), median 20 ticks (range 6 to 50; one tick is 2 seconds); 49 never, all scans (34 of 26 ticks or fewer, 9
    same-motion pairs, 3 second scans with no walk, 3 scans leaving the office on env_layout_02); every break reaches it.
    Findings, none ruled: the same-motion split (C5 confirmed; TODO-97); a short walk under equal shares (T-K part 1's
    question, TODO-154); the standby walk read as a break or, in M4, as an assigned scan never performed (TODO-155);
    one point per container (B9's note, LIMIT-04). The IRB of stage 1 is CLOSED. Next: the design of the MPB set
    with Hadi; open for it: a setup with pallets already in a bay while the robot delivers others; the robot's last task
    as a return; how expected decisions are derived when the human's sequence depends on the robot's decisions (C6).
    RULED, THE MPB ON DOCK_LOADING (Hadi, 2 October 2026; design_decisions.md, "T-G: the second domain's rulings", THE MPB
    ON DOCK_LOADING, MPB-DL1 to MPB-DL6; T-G records 10): a test and an analysis; nothing in the framework changes. Part
    1, a few of kitting's decision paths re-instantiated on dock_loading; part 2, one scenario for each of seven cases
    dock_loading adds; no full coverage claimed, kitting's coverage matrix not repeated. A new setup kind for the
    controlled scenarios: one full unscanned pallet already in each delivery bay, one full pallet in the truck for each
    bay, two empty pallets; the human scans only the pallets in the bays at the start. Controlled scenarios: scripts
    independent of the robot, full expectations committed before the run; mixed scenarios: a dependent script allowed,
    properties declared before the run, and no claim that they validate the recognizer's decisions (C6's third clause,
    for stage 1). The last-task-as-a-return proposal closed, not taken; in its place the per-room counts of ticks below
    the minimum separation with a standing robot, beside the violations with a moving robot (TODO-135). office_break
    stays 90 seconds. `single_task` primary, `full_reorder` second; two rooms, env_layout_03 and env_layout_04
    (env_layout_02 excluded as a reduction of scope, its late admission untested); about 8 controlled and 4 mixed
    scenarios, 48 runs. Next: the MPB set's scenarios, agreed with Hadi before they are authored.
    AGREED, THE MPB SET ON DOCK_LOADING (Hadi, 2 October 2026; design_decisions.md, "T-G: the second domain's rulings",
    THE MPB ON DOCK_LOADING, MPB-DL7, DISPOSITIONS and THE SET; T-G records 11): the disjointness rule for the controlled
    scenarios (no pallet named both by the robot's pool and by an assigned scan of the human); kind 3, "pallets in the
    bays", with two full pallets in each delivery bay, one setup each for env_layout_03 and env_layout_04; kind 4, "one
    bay", the conditional kind; the meeting at a bay in two forms (an admitted scan walk toward the robot's delivery
    bay; a `stand` at the bay, decided on the fallback projection); cases (i) and (vii) mixed. The set: 9 controlled
    scenarios (K1 to K9, kind 3) and 4 mixed (M1, M2, M4 on kind 2, dependent, with declared properties; M3 on kind 3,
    independent, with full expectations), in env_layout_03 and env_layout_04, both strategies: 52 runs. Kind 3 is a test
    condition, not the domain's work cycle. Next: the build's plan (the setups, the scenarios, every duration and cut
    point derived from path lengths, the per-room derivation of each declared case), approved by Hadi.
    BUILT AND RUN, THE MPB ON DOCK_LOADING, ITS SCOPE REDUCED FOR STAGE 1 (Hadi, 2 October 2026; design_decisions.md, the
    same block, THE BUILD'S PLAN CONFIRMED and SCOPE REDUCED AND THE MPB ON DOCK_LOADING RUN; T-G records 13 and 14):
    stage 1 establishes that the recognizer and the recognition-to-planning chain run on dock_loading and produce runs,
    logs and figures; the behavioural analysis belongs to stage 2. The 26 scenarios in two rooms under both strategies,
    52 runs, all completed; the 40 with full expectations agree with the oracle; the mixed runs' declared properties
    hold except M(iii) in env_layout_04 under single_task; the alteration test on dock_loading built, not run.
    analysis/dock_loading/mpb/. Next, as Hadi rules: the close of stage 1.
    CLOSED, T-G STAGE 1 (Hadi, 2 October 2026; design_decisions.md, the same block, T-G STAGE 1 CLOSED; T-G records 15):
    its purpose was an initial check that the recognizer and the recognition-to-planning chain run on dock_loading. The
    52 MPB runs completed; zero disagreements wherever full expectations exist; the regression audit byte-identical. It
    does not state that the scenarios are free of violations: M(iii) failed in three mixed runs and controlled runs
    contain recorded separation violations; findings carried to stage 2, unanalysed. TODO-153 to TODO-156 tagged [V1].
    Deferred to one housekeeping step: the sweep of old terms (TODO-153), the sizes of the files under docs/, what of
    analysis/ stays in git. Next: to be named by Hadi.
    DONE (2 October 2026), the housekeeping step after stage 1's close: the sweep of old terms ("zone" to "area" in
    wording; TODO-153 closed); the split of the records (docs/design_decisions.md holds the conceptual design of the
    shared core, docs/design_records.md everything else, one heading per task); the rule for analysis/ (git tracks
    reports and code only; data and figures stay on Hadi's disk). Open: the rewriting of each conceptual entry into one
    current rule; the destination of two old items under docs/ (the old ROS planner reference text, the folder of old
    layout pictures), deferred until Hadi names one. The next T-G design chat reads docs/handoffs/T-G_forward_inputs.md.
  - Paused after stage 1: context knowledge is T-K (below), framework-wide. T-K part 1 runs now; T-G resumes at its
    stage 2 when T-K part 1 is closed.
  - Stage 2: `store_pallet` (B7); the gate opened on request (B5); the office door's state (B5); after the MPB's first
    run, TODO-16 with the stepwise delivery (A7).
    ADDED (Hadi and the design chat, 1 October 2026; design_decisions.md, "T-G: the second domain's rulings", B14): B10's room (the stores), with its own layout, setup and scenarios; A8's rule on
    monitored areas reopened (the robot observes its own area only, or its own and every area behind an open passage;
    the trigger at disappearance and reappearance with it).
    BUILDS: B7 with the second designation; B5, the gate opened on request and the office door's state; A7, TODO-16,
    after the MPB's first run on dock_loading.
  - After stage 2: track 4 in its reduced form (A8, TODO-140).
  - Stage 3: check-in and check-out (B12), with the two optional items (a deadline on the robot's waiting; a pallet
    that blocks another in the truck).
  The order inside a stage is for that stage's plan; the mapping states content only (C1). No stage: A1, A2, A10, A11 and
  B12's items "not taken" (nothing is built for them).
- **T-V — Viewer, interface and interactive simulator** (ruled by Hadi, 30 September 2026), one task with tracks.
  - Track 1: T-E as originally defined, the viewer for pre-loaded scripts, showing belief, admitted projection,
    decision, hold, refusal and the script's events; demonstration only, nothing enters the mind.
  - Track 2: Phase 7 (below): live events through the human executor's injection path (`inject`, T-H2), the export
    as a script, the replay rule. The context stream is not track 2's: the pre-loaded context facts are T-K part 1's
    timeline, and the stream of context values with the world's dynamics is T-K's future work.
    SUPERSEDED IN PART (T-G C1, Hadi, 1 October 2026): the pre-loaded context stream moves to T-K part 1; track 2
    keeps the live events.
    T-G (1 October 2026; design_decisions.md, "T-G: the second domain's rulings", A3, A10): the human's choice among applicable tasks is one isolated point of
    its executor (a V1 requirement), so that a live user can supply it. An interruption of a busy human caused by a world
    fact, if wanted, is designed here as the same entry point as the live user's click.
- **T-K — Context knowledge** (ruled by Hadi, 2 October 2026; design_decisions.md, "T-K: context knowledge in the
  recognizer's belief"; design_records.md, "T-K"; `docs/handoffs/T-G_forward_inputs.md`, section 5). Context knowledge
  as a whole, framework-wide: it concerns kitting and dock_loading alike. Three parts.
  - Part 1, crisp context knowledge (V1, ongoing; Hadi, 1 October 2026; design_decisions.md, "T-G: the second domain's
    rulings", C1): framework-wide, after T-G's stage 1 and before T-G's stage 2, from its own handoff. Content (its design
    opens in part 1; nothing ruled): a context timeline in the scenario that changes a fact at an authored point of a run,
    applied by the environment; both domains' foreseeable tasks conditioned on such facts. Open questions: the form of a
    context fact; start only or interruption of a task in progress (A3, A10); liveness under A4 when a condition turns
    false during execution; the prior under context; the perception assumption for context facts. The pre-loaded
    context stream moves here from T-V track 2.
    ADDED (Hadi, 1 October 2026; T-G Q16's block, T-G records 8), NOT RULED: one design question, what sets a
    hypothesis's share at the start of an episode, with four determinants designed as one mechanism (the assignment;
    context facts; the task that just ended, a transition prior between tasks; an enabling event such as the robot's own
    delivery, TODO-154); and Hadi's ideas: the duration of a foreseeable task is not one fixed number; temporal context
    can be a fuzzy set with a degree of membership.
    RULED (Hadi, 2 October 2026; design_decisions.md, "T-K: context knowledge in the recognizer's belief", R1 to
    R8; design_records.md, "T-K", R9, the cut, the open items): context knowledge acts in the recognizer's
    belief only, never on the human (R1); belief = normalise(prior × evidence), the prior computed at each run from the
    present context facts (R2); the prior normalises the strengths of what is live, assigned work as a whole
    contributing 1 and each live foreseeable task its declared low or high strength by its occurrence condition (R3);
    equal division inside assigned work (R4); degrees (R5) built later, in T-K part 2; one declared duration (R6); the gate
    unchanged (R7). T-K part 1 builds R1 to R4, R6, R7, crisp context facts, the scenario's timeline of context facts and
    the removal of the domain task names and constants from the recognizer (TODO-66). The build is not started. Open:
    the values for the two domains (Hadi states them), the perception assumption, the tests. Future work:
    TODO-158 to TODO-162.
    AMENDED (Hadi, 3 October 2026; the same entry, AM1 to AM9): the re-entry and boundary rules are shares of the
    evidence (AM1); a strength per task, divided among its live hypotheses (AM2); two run options, both on by default at
    the build, `assignment_knowledge` (today's `assignment_prior`) and `context_knowledge`, context knowledge off giving
    today's equal prior, "work as a whole" covering both settings of the assignment option (AM3, AM9; replaces R9;
    TODO-162 superseded); every strength > 0 (AM4); R7 "before any distinguishing movement" (AM5); the passages on
    crossing θ on prior mass superseded in part (AM6); an occurrence condition is a conjunction in T-K part 1 (AM7); T-K part 2
    open on the representation of a context value and of a degree (AM8). The design is ruled and amended; the build is
    not started; the open items are unchanged (the values for kitting and dock_loading, the perception assumption, the
    tests). T-K is framework-wide: it concerns kitting and dock_loading alike.
    RULED (Hadi, 3 October 2026; the same entry, CONTENT POINTS 1 AND 2, AM10 to AM29; design_records.md, "T-K", CONTENT POINTS 1 AND 2): content points 1 (the values) and 2 (the perception assumption). Every fact is crisp
    (AM10); an occurrence condition reads timeline facts, object states and recency facts, with "and" and "not", "or"
    staying in T-K part 2 (AM11); context removes no hypothesis (AM12); the occurrence conditions, the recency durations and the
    strengths of coffee_break, ac_activation and office_break (AM13, AM14, AM16, AM17); the A/C switch with its object
    state ac_on, at most one per layout in V1, none in dock_loading's three existing rooms (AM18); the layouts with more
    than one A/C switch changed in their own step before the build (AM19); the long-shift rule leaves with no
    replacement (AM22); the build's acceptance (AM24); the timeline's facts known exactly and at once through the world
    state, the declared knowledge from the knowledge component, a recency fact from the mind's memory of an observed
    completion (AM25 to AM27). Future work: TODO-163, TODO-164 [FW]. Content point 3 (the tests) is open. The build is
    not started. Next: content point 3, then ccode's list of the layouts with more than one A/C switch (AM19), then the
    build's plan.
    RULED (Hadi, 3 October 2026; design_records.md, "T-K", CONTENT POINT 3, THE TESTS, KT1 to KT7; design_decisions.md,
    the same entry, AM11's AM34): content point 3, the tests. Kitting first, then dock_loading's stage 1 scenarios; in
    each domain the IRB with an idle robot, then the MPB with a working robot (KT1). On kitting Hadi's rooms
    env_layout_15 (no A/C switch), _16 (the coffee machine and the A/C switch in a dense cluster) and _17 (15 plus an
    A/C switch between two deliveries; the MPB or a mix); env_layout_10, _11 and _02 unchanged as a comparison; a
    further layout for the second coffee break and the recency fact is to come (KT2). The basic set varies only where
    a foreseeable task is placed, between tasks or inside a task between its actions; two setups per layout, five or
    more scenarios each, each run with context knowledge on and off; two MPB cases (a coffee break inside the break
    time, deliveries through the whole break time); the measure is the tick at which the true task reaches the
    threshold and is admitted, and whether a retraction follows; expectations before the runs; the duration mismatch
    waits for a later set (KT3). The setup, not the scenario, holds the timeline of context facts (KT4, AM34). A round
    without context knowledge comes first, before the build: rooms 15, 16 and 17 in the IRB with the present equal
    prior (KT5). Findings, none changing a value: KT6. The build is not started. Next: the round without context
    knowledge; then a new design chat takes the build of T-K part 1 (the list of the layouts with more than one A/C
    switch, the build's plan, the build, the runs with context knowledge on, dock_loading, the close); a later chat
    returns to T-G's stage 2.
  - Part 2, degrees of context facts (V1, at the end of the V1 queue, after track 3b; R5). The build of R5: a context fact
    satisfied to a degree in [0, 1], the membership function from a context value, the operators (minimum, maximum,
    1 minus the degree), strength = low + degree × (high − low). Part 1's crisp facts are its special case, so nothing
    in R2 to R4 changes with it. Not started.
    AMENDED (AM11, Hadi, 3 October 2026): "not" in an occurrence condition is part 1's; part 2 keeps "or" and the
    degrees.
    ADDED (Hadi's ideas and open items, the design chat of 3 October 2026; NOT RULED; design_records.md, "T-K",
    T-K part 2's OPEN ITEMS): soft edges of a window and a gradual return of the strength after a task (a membership
    function over the time since the last observed completion); "or" in an occurrence condition, with "long work without
    a break" (open with it: what counts as a break, when the count starts, its limit and source, the unobserved human).
    Open: whether succession between tasks affects the division inside work as a whole (R4), after T-G stage 2, to be
    argued with `store_pallet` present.
  - Later, future work: the stream of context values with the world's dynamics, the environment updating a value
    through its dynamics (the A/C lowers the temperature) and the robot deriving graded facts from the values (a sketch,
    not ruled: a crisp condition as an interval on one value); it needs a model of the world's physics, and nothing that
    V1 claims depends on it. A/C deactivation (TODO-163); several A/C switches in one layout (TODO-164); TODO-158 to
    TODO-161.
- **T-S — ROS/PRIEST** (ruled by Hadi, 30 September 2026; future work, removed from T-G, at the end of the queue).
  FW (T-G A1, 1 October 2026): not designed, ruled or built within V1.
  - TODO-75: the ROS guide and `env_layout99`.
  - The paused `ros_sim/`, including its stale `BeliefState` construction (flagged at G-build; first recorded here):
    `ros_sim/framework_HRI/framework_HRI/planner_2.py` passes 5 of `BeliefState`'s 11 fields, without those added
    since T-D Stage 1, and `most_likely="unknown"`.
  - Phase 6's execution layer (below).
  - The ROS-specific separation stop, via PRIEST.

The documentation pass for the paper comes before the paper, not before the demonstration.

Decisions recorded with this plan (T-A1), each where its entry lives: B2 is an evaluation factor (TODO-36
closed); the randomised harness moves to T-F, (f) stays in T-B, the separation half of (b) is removed and
β is not a scale item (TODO-47); β is a physical tolerance on wasted path, fixed on IR grounds (TODO-58);
the belief is used as a bar, not a magnitude, recorded as a limitation (design_decisions.md; TODO-84);
`min_separation` is supplied by the body in physical units (TODO-28; design_decisions.md).

**Phase 4D — Low-level execution adaptation**
- 30 September 2026: the detour strategy is in the T-D tail, the PRIEST side in T-S (the plan from T-A, its order).
- 1 October 2026: both are FW (T-G A1).
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
    SUPERSEDED IN PART (T-D R, 27 September 2026): "its ceiling 1/(1 + uⁿ)": the ceiling is gone (R1). design_decisions.md, "T-D R and E".
  - AP: plan adaptation latency (ticks from `theta_crossed` to new queue adopted), reordering frequency —
    noting that prior-off a recognition can fire several crossings (TODO-68)
  - Team efficiency: total ticks to complete all tasks vs. baseline (no IR, fixed queue)
- Analytical tools filed for this phase, not built: the radius of maximum probability (TODO-62 — predict a
  reveal location from geometry, then check it) and the rationality measure (TODO-63)

## Phase 6 — ROS Embodiment 🔲 *(ROS team; `ros_sim/` paused)*
- 30 September 2026: T-S in the plan from T-A, at the end of the queue.
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

## Phase 7 (recorded, not scheduled): interactive deviations 🔲 *(after T-G; nothing decided)*
- SCHEDULED (30 September 2026): T-V, track 2, in the plan from T-A (after T-G and T-F).
- Run-time deviation events into the human executor from a viewer, replayable as pre-loaded scripts: live runs
  demonstrate, pre-loaded scripts evaluate. PULLED FORWARD IN PART by T-H (25 Sept 2026): `executor.inject(Start(task) |
  Drop())` and the export of `Now` as `AfterAction` / `DuringAction` are T-H2's; events may cut mid-action; an
  injection on an empty stack is exported as a plain script entry; viewer walks go to landmarks only. The viewer's
  buttons stay here.
- A context-knowledge stream into the world state, read by the recognizer: not Phase 7's; it is T-K's (above). The
  pre-loaded context facts are T-K part 1's timeline; the stream of context values with the world's dynamics is T-K's
  future work.
  MOVED (T-G C1, Hadi, 1 October 2026): the pre-loaded context stream is T-K part 1 (context knowledge), above;
  the live events stay with T-V track 2.
- Communication as a robot action under a live `unknown` or block: its own task.
  SUPERSEDED IN PART (T-D R, 27 September 2026): "a live `unknown`": the `unknown` hypothesis leaves the hypothesis space (R1); X names communication on a persistent finding. design_decisions.md, "T-D R and E".
- Handoff: `docs/handoffs/phase7_interactive_deviations.md`.
