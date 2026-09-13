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
  `env_layout0` / `scenario_00` (Phase 4 dev), `env_layout1` / `scenario_10` (foreseeable tasks; **dropped
  from the validation sweep**, see Phase 4C), `env_layout2` / `scenario_20` (collinear decoys),
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
- `shared/meta_planner.py` — task scheduling, candidate evaluation, interference detection, cost comparison
- `shared/projection.py` — `Projector` — task + world → predicted trajectory; consumed by meta_planner, and by viz/evaluation later
- `shared/trajectory_algorithms.py` — pluggable path-realization and interference-detection functions
- `shared/planner.py` — HTN decomposer, called by meta_planner per candidate AND by the recognizer per hypothesis per tick
- ~~`shared/replanning.py`~~ — **retired Sept 2026**, deleted; trigger role absorbed into `evaluate_triggers()`

**Key design decisions for Phase 4:**

- Robot's `scheduled_tasks` list order carries no semantic commitment (see design_decisions.md) — it's the same field type/name as the human agent's, just not consumed as a schedule. Initial queue `Q0` is produced by the same update() mechanism used for every later reorder: evaluate_triggers()'s "no current task" condition fires on the first call, no IR confidence required to run it (IR runs from t=0 with a uniform prior regardless). No separate base-cost heuristic.
- `planner.py` becomes a true recursive HTN decomposer: if a StepCall names a TaskSchema (not a primitive ActionSchema), it recurses. Output remains a flat `AbstractPlan` (single task, executor-facing).
- `meta_planner.py` owns task selection. It calls `planner.py` per candidate task to project action sequences, evaluates costs, and selects the next task. HTN does not schedule — it only decomposes.
- Selection is **single-task, receding-horizon** (DESIGN-16): one best next task per trigger, re-decided from fresh WorldState and belief at the next trigger — not a search over orderings of the remaining pool. `full_reorder` is retained as a documented, switchable alternative but is not implemented.
- `ProjectedPlan` (DESIGN-06) is the meta_planner's internal reasoning structure, never handed to the executor. Under `single_task` it always holds exactly one entry; the multi-entry shape is retained for `full_reorder`.
- Interference detection is **geometric, not zone-based** — actual Euclidean distance between projected positions over time. `ProjectedPlanEntry` carries `Segment`s; `ConflictPoint` carries `position` + `distance`, no zone.
- Cost is measured in execution ticks (T2: projection steps are Mesa ticks; seconds in ROS): moves, detours, pauses all equal cost units. Team-level semantic costs parked as future extension (see DESIGN-08).
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

**Phase 4C — MetaPlanner + recognizer rebuild** 🔄 (`single_task` path built and validated on scenario_00; the recognizer rebuilt and handed back; the meta-planner side resumes on the hand-back)

Built and running end-to-end. All three tasks complete, correct terminal state, zero errors.

*Implemented (meta-planner side):*
- `shared/meta_planner.py` — public: `evaluate_triggers()`, `update_human_projection()`,
  `update()`; internal: `seed_tasks()`, `_detect_interference()`, `_cost()`
- `shared/projection.py` — `Projector` extracted from `MetaPlanner`: `project()`
  (single-task path), `project_human()`, `build_segments()`, `estimate_duration()`.
  Injected into `MetaPlanner` rather than constructed by it — one instance, held by the
  agent, shareable with viz/evaluation
- `shared/trajectory_algorithms.py` — `straight_line_path()`, `stationary_segment()`,
  `discretized_time_sampling()`; `closest_point_of_approach()` and `obstacle_aware_path()`
  documented but deliberately unimplemented
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
- B1/B2/B3 (evidence-gated human projection, mid-task evidence, candidate selection) under active design;
  the meta-planner has been PAUSED during 4C-IR and resumes from `docs/recognizer_handback.md`

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
- `_cost()` is hard-gate only — `conflicts` computed and carried but not priced (DESIGN-08)
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
- TODO-28: `min_safe_distance` still an uncalibrated placeholder (T1 gives the calibration evidence); the
  `assumed_speed` / time-scale half was RESOLVED by T2.
- TODO-29: `deliver_with_return` still unexercised under the MetaPlanner for the ROBOT. It is exercised every
  run by the recognizer for rival hypotheses of the human, and whether its guard is the right prediction there
  is now an open domain question (TODO-55 (e)).
- TODO-30: the interference exclusion branch is NOW EXERCISED (T2): candidates are excluded at `min_dist = 0`
  (scenario_20 steps 11 / 24) and every-candidate-excluded raises (scenario_10 step 257). Whether those
  exclusions are legitimate is TODO-28's question; what the robot does when everything is excluded is open.
- TODO-32: `wait_at` duration still ignored in COST estimation (projector side). The recognizer side is done:
  waits are observable (`waited`) and `coffee_break` is recognised mid-walk in scenario_40.

*Waiting on the meta-planner side (from the hand-back):*
- `theta_crossed` as an interface event (TODO-68, with TODO-48 and TODO-54): prior-off the true task can
  cross θ three times within one grasp stop, because rivals' `deliver_with_return` phases lift them briefly.
  The recognizer is correctly implementing its model and the contract in `io_contracts.md` promises a
  crossing event, not one crossing per task; whether the meta-planner needs a one-shot semantics is an
  interface decision, not an evidence-model one. Prior-on: one crossing per recognition.
- θ is a live-set-dependent bar (TODO-64, TODO-65); the guarantee statement (hand-back §3) says what the
  meta-planner may and must not assume, prior-on and prior-off separately.
- TODO-52's latent crash and TODO-67 (s30_off selects an already-delivered item); the context /
  knowledge-representation pass (TODO-66).

**Phase 4D — Low-level execution adaptation**
- Executor continues to handle within-action adaptation (detour, pause) guided by execution hints in AbstractPlan
- No structural change to executor interface; hints richer than current skeleton
- Now scoped more concretely via DESIGN-13 (see TODOS_AND_DEFERRED.md): a
  common, non-committed path-realization estimator called from
  `_estimate_duration`, handling both pause and detour as outcomes of one
  call driven by a conflict hint from `_detect_interference`. For Mesa, this
  estimator can also serve as real execution-time realization (replacing
  straight-line `steps_toward`), collapsing cost-time and execution-time
  path realization into one function. ROS keeps a two-tier split (this
  estimator for cost estimation, PRIEST for real execution) — still a
  dedicated design session away from being built

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
