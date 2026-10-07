# CLAUDE.md: teamrob-intention-aware-planning

Simulation-agnostic robot cognitive architecture for intention-aware human-robot teaming
(Scania kitting). Pipeline per robot step:
`obs_builder → recognizer → meta_planner → planner → executor`.

What the framework is about: how the robot reads the human and plans around them. What it is not
about: what the human produces. An abandoned delivery is in scope for what it does to the robot
(retraction, the adequacy finding, re-planning), not for the human's output (Hadi, T-C1).

## How sessions work

- The design is made in a separate design claude chat (we call it cchat) with Hadi. Also we may call the working tool of claude-code in local repository as ccode. A task prompt states what is decided
  and what to do. You implement, check, commit, and report. Hadi reviews and pushes.
- One task per session as a rule. A fresh session starts from what is committed, not from an
  earlier session's reading of it.
- What a task states as decided is settled until Hadi rules otherwise. How to implement, where things go,
  and how to structure outputs are yours. (Hadi, 4 October 2026, replacing "do not explore alternatives to it" and the
  rule of 3 October below:) ccode decides how the approved design is built. On what is built and why, ccode may
  propose alternatives and raise objections, with reasons. ccode does not resolve a design question. Hadi rules what
  is built and why. Reason: Hadi decides the design, and ccode knows the code best, so its proposals and its doubts
  are wanted. The working rules of the design chat:
  `docs/handoffs/T-G_forward_inputs.md`, its last section.
- If a decided design turns out to be structurally or experimentally deadlocked when you apply
  it, stop and report. Do not work around it.
- Rules Hadi set on 3 October 2026 (also `docs/handoffs/T-G_forward_inputs.md`, section 11):
  - Durations are shown in ticks, not in seconds or minutes.
  - A prompt for ccode states what is decided, its purpose and why it was ruled; which files and names are affected
    and how ccode checks its work are ccode's. No micro-level instructions. (The sentence on ccode as the worker who is
    not asked for alternatives is replaced by Hadi's wording of 4 October 2026 above.)
  - One ccode session, one concern. A follow-up goes to the session it belongs to.
  - Once a plan with numbered steps is agreed, replies keep those step numbers.
  - ccode's chat reports stay short: what was built, what it shows in plain words, what surprised, what it suggests.
    Detail goes into the files the task already produces (a room's notes, a set's README, a report the task asked
    for); this rule creates no new report file (workflow rule 6).
- Rules Hadi set on 4 October 2026 (also `docs/handoffs/T-G_forward_inputs.md`, section 11, the design chat after
  step 5b):
  - A test or observation step needs no approval from Hadi. It runs on one model, with no pause between its stages.
  - When Hadi switches the model between stages, there is a pause at each stage boundary.
  - The model to use stands as the first line inside each prompt.
  - A new ccode session per step.

## Where to look, and what to skip

Do not explore the whole tree. Start from the files a task names; widen only with a reason.

Relevant (read as needed):
- `shared/*.py`: cognitive layer (the robot's mind)
- `world/*.py`: the world's side (T-H2): the human's executor (`world/human_executor.py`, the stack machine and
  the load-time replay) and its record (`world/record.py`); the tag per task, one definition for the analyses and the
  web-ui (`world/tag.py`, T-viz 1a)
- `mesa_sim/*.py` (top level only); `mesa_sim/viz/` only for visualization or when grepping
  for readers of a field
- `mesa_sim/run_config.py`: the run configuration (run file, flags, or any mapping) read and checked, and the
  `SimModel` built from it; one definition for every start (T-viz 0.2)
- `mesa_sim/sim_run.py`: one sim-run: the model stepped, its log pair (`.log` and `.rec`) and the run-level lines
  (T-viz 0.2)
- `mesa_sim/webui_adapter.py`: Mesa's piece for the web-ui: the catalogue, the run description and the tick updates of
  a sim-run, read from the model only (T-viz 0.4)
- `mesa_sim/run_webui.py`: the web-ui's start: the headless start's run file and flags, and `--port`; Mesa's piece
  handed to the web-ui's server (T-viz 1a)
- `webui/`: the web-ui, independent of every simulator and domain: the messages (`messages.py`), the interface a
  simulator's piece implements (`simulator.py`), the scene appearance (`appearance.py`), the page's schema
  (`schema.py`), the server (`server.py`, T-viz 1a), and the page (`page/`: React, TypeScript, Vite, three.js;
  `node_modules/` and `dist/` are not read)
- `domains/kitting/`: the active domain (`domains/kitting/script.py`: the call forms a scenario is written in, T-H3).
  T-L stage 2: `layouts/` and `setups/` hold the layout and setup files (setups under their final ids
  `env_setup_NN`; env_setup3 and env_setup5 merged into env_setup_01 and env_setup_03; layouts under `env_layout_KK`
  and scenarios under `scenario_sNN_MM` since stage 3, `docs/rename_table.md` maps the old ids); `scenarios/` is a package,
  one module per setup (`scenarios_sNN.py`); the registry discovers all three (`domains/discovery.py`) — no hand
  list; `env_layout6.json` and `env_layout99.json` stay at the domain root, unsplit and unregistered;
  `mesa_sim/sim_agents.py` `HumanAgent`: the human's body-side driver of the stack machine (T-H2)
- `domains/dock_loading/`: the second domain, T-G's (open; its rulings in design_decisions.md, "T-G: the second
  domain's rulings", part B dock_loading only; its state after build 1 in part C, C3)
- `configs/experiment.yaml`, `configs/costs.yaml`, `mesa_sim/mesa_configs.yaml`
- `docs/glossary.md`: the terms and their one meaning each. Read it every session, before the
  design record. Use its terms in the code, in the documents and in reports.
  `docs/terminology_revision.md` is its explanatory companion for glossary §7 (human behaviour, model
  coverage, the adequacy finding and "unexplained"); the glossary stays authoritative.
- Design record, in `docs/`: `design_decisions.md`, `roadmap.md`, `TODOS_AND_DEFERRED.md`;
  plus `shared/io_contracts.md` and `docs/recognizer_handback.md`
- The record of planning and building (the records split, 2 October 2026): `docs/design_records.md`, one heading per
  task (phase4, T-A, T-B, T-C, T-H, T-L, T-D, T-G, T-G stage 1, T-K, T-F part 1, T-viz). A session reads its own task's heading. In
  `design_decisions.md` an index line `→ RECORD [<id>]` stands where a moved block was; `design_records.md` heads the
  block with the entry's title and the same id, so a citation by title and label resolves.
- `docs/handoffs/handoff_T-H.md`: T-H, the human behaviour model (ruled 25 Sept 2026; design_decisions.md, "T-H: the
  human behaviour model"; glossary §6 and §7). Read it in every T-H session. `docs/terminology_revision.md` §8 states
  what T-H changed in the 24 Sept terms.
- `docs/handoffs/handoff_T-viz.md`: T-viz, the web-ui (the design chat of 4 to 6 October 2026; design_records.md,
  "T-viz, the web-ui"; roadmap.md, the T-viz bullet; TODO-186 to TODO-197; reference images in
  `docs/handoffs/tviz_refs/`). Read it in full in every T-viz session. T-viz records use its status words (open,
  preferred, preferred, replaceable, proposed by cchat, verified, not verified), never "ruling" or "ruled"; "sim-run"
  is a word of the T-viz records only. "The viewer" in older records and in code means the solara-ui (a tentative
  name for the existing program, `solara run mesa_sim/run_mesa.py`) or T-V's planned viewer, now T-viz stage 1;
  nothing is renamed without Hadi's word.
- `analysis/`, sorted by domain (the sort, 1 October 2026; `analysis/README.md`): `analysis/instruments/` holds the
  test-beds' code both domains run (`run.sh <domain>`), `analysis/kitting/` every earlier analysis with kitting's run
  sets, expectations and reports, `analysis/dock_loading/` dock_loading's; the run files under `configs/<domain>/`, the
  tests under `tests/kitting/`, `tests/dock_loading/`, `tests/instruments/` (three two-domain tests at `tests/`). Old
  paths in dated entries and frozen reports: `docs/rename_table.md`, "Paths: the sort".
- Deleted 5 October 2026 (T-F part 1's close, part E; analysis/README.md): the frozen analyses td_stage1, td_stage1b, l_build, irb2b_exposed_interval (tb2b_exposed_interval before 3 October), ablation_task_committed, f47_fixtures, t1_conflict_measurement, todo90_b2a_window, tc2c_scripts, tb1d_designations, tb2c_per_entry_holds and big_picture under analysis/kitting/ (analysis/ before the sort); the runs and run files of T-K part 1's steps 5 and 5b (planning) and 5e and of T-F part 1's stage 2 check (configs/kitting/mpb/tk, mpb/tk5b, tk5e, tf1/check; their READMEs and reports stay). A path cited below under these names is held by commit 362af19 (`git checkout 362af19 -- <path>`).
- `analysis/<domain>/<task>/REPORT.md`: only the reports a task names. Rows in older reports may be
  stale (earlier projection, recognizer or layouts); their findings are cited, not re-derived.

Where a ruling is recorded (Hadi, 2 October 2026). `docs/design_decisions.md` holds conceptual design: what the
framework's mind, the world's side or their contract does or must do, in any domain and at any stage, superseded
statements of that kind included, with the measurement that is its stated premise. Everything else a task rules or
does goes to `docs/design_records.md`, under the task's heading: the method of verifying the design, authoring
conventions, domain rulings, staging, plans, build blocks with commits, acceptance, test-bed sets, expectations,
dispositions, results. A ruling made in a domain or test-bed discussion goes by its content. A mixed ruling is cut at
the block: its conceptual part under its entry in `design_decisions.md`, its record part in `design_records.md` under
the task's heading and the same entry title. A dated amendment goes where the text it amends is; a short BUILT
line goes with the ruling it reports. Unclear: ask Hadi.

The method of context knowledge (Hadi, 4 October 2026). `docs/context_knowledge_method.md` states the method of context
knowledge (T-K): the concept, the formulas of the prior and worked examples, the statement of the prior that a build
reads. The design records hold the rulings and win where the two disagree. A ruling that changes the method of context
knowledge updates this document in the same records step. ccode does not change the method itself: it flags a
contradiction with its evidence, and Hadi rules.

Never read, edit, or treat as a source of truth:
- Any file or directory named `my_*`, `old_*`, `archive_*` (personal notes and backups).
- `__pycache__/`, `.venv/`, `.pytest_cache/`.

Skip in the current phase; read only if the task explicitly requires it:
- `mesa_sim/mesa_fork/`: vendored Mesa 3.0; treat as an installed library. Look inside only if
  a traceback points there.
- `ros_sim/`: paused.
- `scripts/`: not part of the run path.
- `logs/`: except logs you produced in the current task.

## Architecture invariants (never violate)

Layering: four homes
- `shared/` is the robot's mind, the pure cognitive layer. It never imports from `world/`, `domains/`,
  `mesa_sim/` or `ros_sim/`.
- `world/` is the world's side (T-H2): simulator-agnostic, use-case-agnostic code about what the human is and
  does (the human's executor and stack machine, the executor's record). It imports `shared/` only: no body, no use case. The robot's mind never reads it.
- `domains/` holds the use cases (kitting, dock_loading): schemas, layouts, setups, scenarios.
- `mesa_sim/` and `ros_sim/` are the simulators (T-G A2; glossary §10): each implements the environment (the room, its
  objects and their true states, belonging to no agent) and the agents' bodies. A simulator may import from `shared/`,
  `world/` and `domains/`; it drives the human's executor and executes the robot's decisions. (Older records say "the
  bodies" or "the embodiment layer" for it; the robot's body is the part that builds its WorldState and carries out its
  decisions; the Mesa class `RobotAgent` still holds mind parts and body parts together, TODO-131.)
- `shared/` holds no simulator constant and no unit-scale default. Whatever depends on the body
  (speed, arrival radius, execution latency, spatial resolution) is supplied by the embodiment
  layer and passed in.
- No string parsing in `shared/`. Bindings are typed `Var` / `Const`.
- No domain-specific strings in `shared/` (never hardcode `"?item"`, `"kitting_table"`). Domain
  facts come from schemas (`TaskSchema.parameter_types`, `ActionSchema` fields).

World and facts
- `WorldState` is ephemeral: rebuilt every tick, never stored or mutated.
- One fact, one owner. Task completion is a fact about the world (the task's terminal condition
  holds, via `planner.is_complete()`), not about who performed it or about bookkeeping.
- `at(agent, object)` (executor completion) and `in_area(agent, area)` (recognizer context) are
  distinct predicates. Never use `at(agent, area)`.
  CORRECTED (2 October 2026): "(recognizer context)" is false since I3 (a7a4f8c): the recognizer reads no area.
  `in_area(agent, area)` is read by method guards through the planner's method selection; `at(agent, object)` is also
  `move_to`'s completion condition, which the recognizer's phase model reads.

Decisions
- Decisions are made once, inside `shared/`. Embodiment layers execute them and may refine them
  (for example a hold), but never implement a parallel heuristic or re-decide which task runs.
- The robot knows nothing of the human's script. It never reads the human's `scheduled_tasks`
  or their order. The run option `--assignment_knowledge` (on by default since T-K part 1's build; `--assignment_prior`,
  default off, before it) gives it only the human's assigned-task pool; off is an ablation. A second option,
  `--context_knowledge` (on by default), gives the recognizer's prior the domain's declared context knowledge; off is
  the equal prior (T-K part 1, AM3, AM9).
- The recognizer emits a belief distribution and gates nothing. The confidence gate θ belongs
  to the meta-planner (`DEFAULT_THETA` in `shared/meta_planner.py`), and is asked in one place
  (`MetaPlanner._clears_gate`). Do not weld comparisons against θ into other call sites.
- Conflict with the human becomes cost by construction: a conflicted task costs more because
  avoiding the human takes longer. No conflict weight, no exclusion threshold to tune.
  Realization lives on the projection side; the geometry in `shared/trajectory_algorithms.py`
  holds no policy.

## Current phase and status (affects what you may touch)

- Phase 4C: realization is built and total (T3, T4, T10, F1), the Mesa executor has the
  execution-time separation stop (C, run option, default off), wait durations come from the schema
  (TODO-32), scheduled bindings are type-checked at spawn (F47b), and the trigger set is settled
  (D2: `recognition_changed` against the decision record replaces `theta_crossed`; D3: `task_committed`
  removed, the robot's grasp is no trigger), and the policy
  components are ablated (T6, `analysis/kitting/t6_ablation/`, deleted 4 Oct 2026); the gate stays a fixed share (the gate ruling). The 4C
  queue is done.
  The plan from here is T-A to T-G ("The plan from T-A" in `docs/roadmap.md`; the order revised 30 Sept 2026, below).
  T-B is under way: T-B2a
  (`Projector.project()` chains the entries of an ordering, through a successor state derived from what the
  action schemas declare), T-B2b and T-B2c (`full_reorder`: an ordering realized against the human
  projection, one minimal-shift search and one hold per entry) and T-B2d (the `--strategy` run option) are
  built, which completes B3.B; next is T-B3, its evaluation. The body now spends every completion tick it
  states to the projection (T-B Q7: a reload never cancels one), which closes TODO-77's residual — what is
  left of it is step quantisation, uncompensated by decision. T-C2 (the human action script: C2a the scenario
  layer, C2b sequential expansion and the action-level human executor, which spends no per-task completion
  tick and reports 0 for it to the projector) is built, and T-C2c's two literal scenarios are run. T-H (the human
  behaviour model, ruled 25 Sept 2026: one tree of task schemas, the robot's task model, the script of task
  instances with events, the human executor's stack and record) was built in four sessions T-H1 to T-H4, before
  T-D. T-H1 (the tree, the task model) and T-H2 (the executor: `Script` of `TaskInstance`s with typed events,
  `at` / `during` / `inject`, the one-level stack in `world/human_executor.py`, the mid-action cut through the shared
  Mesa `Executor`'s `suspend` / `resume`, the load-time replay `check_script`, the record and its `[rec]` stream in
  `logs/run_<timestamp>.rec`) are built, and T-H3 (every scenario migrated to the `Script` in the kitting call form,
  the `HumanOnlyTask` `go_to_and_stand` added, the C1 script layer deleted) and T-H4 (the record's typed queries in
  `world/queries.py`: `truth_at`, `switches`, `resumptions`, `assigned`, `unperformed`, `coverage`, on the in-memory
  record; task equality `same_task`; the `[coverage]` line at load) are built. T-H is closed (26 Sept 2026; the
  close-out in `docs/handoffs/handoff_T-H.md`: commits, acceptance, deferred items). T-L (the three artefacts
  of a run, stages 1 to 4; design_decisions.md, "Layouts, setups and scenarios") is built (26 Sept 2026; stage 4: the
  run file, `--run`, and the overrides, `--override`, `mesa_sim/overrides.py`). T-D is under way, on T-H's structure
  (`docs/handoffs/handoff_T-D_onward.md`, "What T-D now stands on"). T-D R and E (design_decisions.md, ruled 26 to
  27 Sept 2026) Stage 1 is built (27 Sept 2026, cycle 1 session 1.3): the `unknown` hypothesis, u and the grade are
  gone, the belief is normalised over the live hypothesis set H only (R1, R6), and beside it the recognizer reports
  the adequacy finding (unresolved | adequate | unexplained, from the projected completion delay D and its tail
  probability S per live hypothesis per derived phase, at the test level α, the run option `--test_level`, default
  0.05), the lifecycle state (live | exhausted) and the members' tail probabilities. Session 1.4 verified it
  (`analysis/kitting/td_stage1/REPORT.md`), and cycle 1.5 is ruled on it (27 Sept 2026; design_decisions.md, "T-D R and E",
  "1.5 rulings"), and built in session 1.5b (27 Sept 2026): E8 (on the tick a hypothesis's expected action completes
  it is a member with S = 1), E9 (s_exp is the Projector's priced stationary ticks within the phase: 2 for `pick_up`
  and `place`, 1 for a walk entered from a completion, 0 for the initial walk; the recognizer receives the body's
  action and observed-task completion latencies), E10 (the belief's evidence per phase is L(v·D), the same D the
  adequacy test reads through S; walking evidence unchanged, standing beyond the priced standing charged) and G1 (the
  recognizer reports every live hypothesis's hypothesis adequacy, adequate | inadequate | no observation; the gate,
  `_clears_gate`, now returns a `GateOutcome` and also requires the leader's to be adequate; refusals
  `none(leader_no_observation)`, `none(leader_inadequate)`). The four maintained baseline sets are regenerated under
  it; acceptance is `analysis/kitting/td_stage1b/REPORT.md`. Session 1.5c closed cycle 1 (27 Sept 2026): E6 amended a second
  time (a stationary tick within the priced standing of any phase with s_exp > 0 is an observation at S = 1; no
  member on a boundary tick), zero false unexplained on modelled ticks; the 1.5b findings are cycle 2 inputs
  (TODO-87, TODO-118, TODO-119). Next: the IRB track, then cycle 2, L, P, the rest of G, and X, each ruled
  on these results. The IRB (ruled 27 Sept 2026; design_decisions.md, "The intention-recognition test-bed (IRB)") tests the
  recognizer in isolation, on a layout, setup and scenarios written for it, against expectations derived from the entry
  before the run, in three sessions: IRB.1r (records), IRB.2b (the cognitive-loop correction), IRB.3b (the artefacts, the
  expectation generator, the runs, the report; `analysis/kitting/irb/`). The cognitive loop does not end with the task
  pool (ruled 27 Sept 2026; design_decisions.md, the entry of that name; built in IRB.2b): observation and
  recognition run on every tick, and an empty pool stops planning and execution only. IRB.3b built the IRB
  (27 Sept 2026; env_layout_10, env_setup_08, scenario_s08_01 to _04, run files in `configs/kitting/irb/`, the
  instrument in `analysis/instruments/irb/`, its report in `analysis/kitting/irb/`): the recognizer's public outputs agree with the independent
  oracle on every compared tick of the four runs. IRB.4b made the instrument independent of the layout and added the
  enlarged room (env_layout_11, env_setup_09, scenario_s09_01 to _12: the IRB.3b scripts, the deviations and the
  same-side alternates; the s08 artefacts and outputs unchanged): zero disagreements at 1e-9 on all twelve.
  The IRB track is closed (IRB close-out, 27 Sept 2026; design_decisions.md, "The intention-recognition test-bed (IRB)", its foot); next
  is cycle 2, L.
  L, the belief lifecycle, is ruled (L-records, 27 Sept 2026; design_decisions.md, "T-D L: the belief lifecycle", L1 to
  L5: the boundary on a terminal action's completion, retraction by the meta-planner, liveness while the terminal fact
  holds); L-build built it (28 Sept 2026: the boundary on the observed agent's completion of a terminal action, the
  live set read from the terminal facts every tick with re-entry at 1/|H|, retraction and the boundary flag in
  `recognition_changed`; `analysis/kitting/l_build/REPORT.md`, the IRB agreeing at 1e-9); next is P.
  P, the fallback projection, is built and closed (28 Sept 2026; design_decisions.md, "T-D P"): when admission refuses
  and a human is observed, a short-term physical projection from the observed position and the last displacement
  (standing, or a straight continuation to the wall or the first fixed object) over each candidate's span; a
  candidate whose violation is cleared only by the projection's end is refused, and with none eligible the robot
  waits without a task (16 of the 48 baselines end waiting at an occupied target, X). P3 is open. Next is G.
  P4 (persistence, ruled 28 Sept 2026; design_decisions.md, "T-D P", P4 and Q6) reopens P: the fallback projects the
  observed persistence only (a straight run of k ticks projects k ticks, a stand of k ticks k ticks), the refusal and
  the wait are dropped, and a third trigger, `projection_expired`, re-decides when the fallback a decision rested on
  runs out. P is closed with P4 (P4-build, 28 Sept 2026; the four maintained sets regenerated, six prior-on logs not
  completing at the occupied target with holds lengthening, X's case); P3 and TODO-134 stay open.
  Track 2.5 (ruled by Hadi 28 Sept 2026, built 29 Sept 2026): the framework assumptions and authoring conventions are
  recorded in `docs/assumptions.md` (a case is classified first: intended phenomenon, boundary, authoring artefact,
  prior-off artefact); the six regression scripts behind the occupied-target logs (scenario_s01_01, s01_06, s02_01,
  s03_01, s04_01, s06_03) end with the exit walk `go_to("corner_SE")` (1.1; env_layout_02 and env_layout_08 gained
  corner_SE), and the four maintained sets are regenerated (the "2.5" sections: every log completes; the `[sep]` minimum
  and F1's classes per run, `analysis/instruments/common/sep_classes.py`); scenario_s09_13 (the mid-action change, a
  coffee_break cut into a carry) agrees with the IRB's oracle, extended to cuts; TODO-95 closed (3.4), TODO-135
  to TODO-139 recorded. G is ruled (29 Sept 2026; design_decisions.md, "T-D G: admission", AD1 to AD5): admission
  also requires warrant (commitment or observation that justifies admission; not the support restriction), a third
  output beside belief and adequacy; TODO-119 closed, TODO-132 (a) and TODO-134 parked. G is built (G-build, 29 Sept
  2026; design_decisions.md, "T-D G", BUILT): `BeliefState.observation_warrant` (the entry and the movement source; an
  unresolved `move_to` has the entry source only), the meta-planner's `observed_assigned_tasks` (commitment warrant),
  `none(leader_unwarranted)` after `none(leader_inadequate)`, `[IR] ... warrant=[...]` and `[meta-proj] projection=built
  warrant=...`; the IRB's oracle extended (warrant and the gate's outcome per tick, 0 disagreements on the
  seventeen); the four maintained sets regenerated ("G-build" sections: prior on, only the lone coffee_break's admission
  at b + 1 moves, no completion). Recorded: the movement source is a half-plane test (the exit walk warrants the lone
  coffee_break in scenario_s09_01 from 126; a competitor is TODO-140's). Next is X.
  X is ruled (29 Sept 2026; design_decisions.md, "T-D X: response", X1 to X5), records only, nothing built for it: the
  occupied target gets no special handling (X1, verified in track 3), no blocked event and no fourth trigger (X2; P3 the
  residual), the human walking toward the robot is an evaluation case (X3), the fallback is the response after a
  retraction (X4), and the two grounds for communication are recorded, persistent by the robot's re-decision cadence
  (X5; TODO-96, TODO-141). Next is track 3 (TODO-130); track 4 (TODO-140) first if the evaluation needs a departure.
  Track 3, the meta-planner test-bed (MPB), is ruled (29 Sept 2026; design_decisions.md, "The meta-planner test-bed
  (MPB)", MPB-1 to MPB-6), records only: eight scenarios on env_layout_12, an oracle for the trigger and cause, the
  gate and the projection (per-tick tables pre-run, the chain assembled with the run's `no_current_task` ticks), part 4
  as declared properties; prior off a diagnostic appendix. MPB step 2 is built and the MPB closed (29 to 30 Sept 2026; parts (i) to (v);
  `analysis/kitting/mpb/`, REPORT.md; env_layout_12, env_setup_10/11, scenario_s10_01 to _09 and s11_01, _02, `configs/kitting/mpb/`):
  - all eleven scenarios verified: zero disagreements on parts 1 to 3 under both strategies, prior on; every declared
    part-4 property holds under single_task;
  - AD3 is not exercisable in the MPB set (the AD3 line);
  - the skip rule is a design question (P4's dated line, TODO-142);
  - an observed human with no work under the prior on has no representation (TODO-143).
  The coverage matrix is recorded (`analysis/kitting/mpb/coverage.md`; MPB-2 as amended: the layout-and-setup rule, the three
  kinds of cell). Part (v) built its five reachable claimed cells, one authored instance each, all verified (30 Sept
  2026; env_layout_13, env_layout_14, env_setup_12, scenario_s12_01, _02, s11_03, s10_10, _11): the switch against an
  admitted projection, the hold against an admitted standing segment, the switch while carrying, a record kept through
  a dip below θ, the cause boundary. A class-2 finding, reading (a), was corrected (30 Sept 2026; MPB-4's class-2
  record; design_decisions.md, "Realization as built", the dated correction): the invariant is that the trajectory
  realize() assesses is the trajectory the robot executes from the decision tick onward. The body reports
  `ExecutorState.owed_completion_ticks` and `action_in_flight`; every robot candidate's projection states the owed ticks
  first (`Projector.project`, `lead_in`) and the continued task is projected from the action in flight (`resume_from`);
  owed ticks run before a hold (T-B Q7's "the hold carries the tick" superseded in part). Tests:
  `tests/kitting/test_executed_is_assessed.py`. The four maintained sets were regenerated ("class-2 correction" sections; one hold
  moved, scenario_s02_01 prior on). The human side's counterpart is TODO-146, recorded only.
  The MPB is CLOSED (the close-out, 30 Sept 2026): every materially distinct in-scope decision path is verified,
  unreachable with a recorded derivation, or outside the claimed mechanism with a recorded reason. It establishes
  structural branch reachability and execution of the recognition-to-planning chain, not consequential activation under
  human-robot interaction conflict. The progression: track 1 recognition, track 2 semantics, track 3 reachability, track
  3b consequence under conflict (TODO-145, not ruled), T-F benefit (TODO-144). The MPB instrument saves the belief and S
  per tick and the projected human and planned robot segments per admitted decision, and draws `figure_ir.png` beside
  `figure.png`.
  The order of the tasks (Hadi; `docs/roadmap.md`, "The plan from T-A", its order block; task letters are never
  reassigned, the order is not the alphabet). Done: T-A, T-B, T-C, T-H, T-L; T-D is closed except its tail; T-G's
  stage 1 is closed and T-G is paused. Now: T-K part 1 (crisp context knowledge). Then, in order: T-G's stage 2, track 4
  (its reduced form, TODO-140) and T-G's stage 3; T-F (the evaluation, framed in TODO-144, the randomised harness
  TODO-47 part of it; kitting's part without a departure, dock_loading's may use the unmonitored office (Hadi, 1 Oct
  2026); before track 3b it measures without knowing that the adaptive branches fire under conflict); T-viz stage 1
  (the web-ui's first version; T-V track 1, the viewer, which was T-E; in T-V's place, proposed by ccode, 6 Oct 2026);
  track 3b (TODO-145); T-K part 2 (degrees) at the end of the V1 queue. T-viz stage 0 is closed (6 Oct 2026); stage 1a is closed (6 Oct 2026); stage 1b is built (6 Oct 2026; panel 4b, reviewed 7 Oct 2026); stage 1c is built (7 Oct 2026; panel 4c, the past view, one colour per task; Hadi's review open); stage 1's order 1b, 1c, 1d, 1e.
  FW: the 4D detour strategy, T-S (ROS/PRIEST, Phase 6), T-K's later directions, and T-viz stages 2 and 3 (stage 3 is
  T-V track 2, Phase 7; the default until Hadi draws the V1 border inside the web-ui).
  V1 and FW (Hadi, 1 Oct 2026, amended by Hadi 3 Oct 2026 and 6 Oct 2026 for T-viz; design_decisions.md, "T-G: the second
  domain's rulings", A1): V1, the first complete version, holds T-G, T-K part 1 and T-K part 2 (the amendment), T-F,
  T-viz stages 0 and 1 (T-V track 1 is T-viz stage 1; T-V track 2 is T-viz stage 3, FW for now),
  track 3b (TODO-145) and track 4 in a reduced form (monitored areas, A8, TODO-140), placed after T-G's stage 2; FW (not
  designed, ruled or built within V1) holds the 4D detour, T-S, T-K's later directions (the stream of context values
  with the world's dynamics, TODO-158 to TODO-161, TODO-163, TODO-164; the amendment) and the conceptual directions
  TODO-147 to TODO-150. Open TODOs carry [V1] or [FW] beside their status when next touched by
  Hadi's ruling; untagged means not yet ruled.
  T-G is OPEN: its design is ruled (30 Sept and 1 Oct 2026; the entry above, by scope: part A framework-wide, some of
  it changing `shared/` or `world/` when built, each with kitting byte-identical or no decision changed as acceptance;
  part B dock_loading only; part C the stages), and build 1 is in (30 Sept 2026; 56e674e, 6e29c15, 62ebc4e: form-only
  repairs). Stage 1's rooms and setups are agreed and written (B14, 1 Oct 2026): env_layout_02 to _04, six setups (two
  kinds per room: the IRB's, the MPB's), one viewing fixture per pair; env_layout_01, env_setup_01 and build 1's
  scenarios removed; full observation in stage 1. Stages (what
  each first builds: the entry's C1): 1 the basic domain, opened by the rename of the zone mechanism to "area" (its own
  commit, no change of behaviour), with the forms' catch-up (C3) and the framework-wide A3 (the script's priority form,
  `world/`, with the lifecycle of a list entry ruled as T-G Q12 to Q15, 1 Oct 2026: open and closed entries, the
  repeatable standby entry, the dependence declaration for the load-time check, the closing part; also checked on the
  kitting drop scenarios and the test-bed misdeliveries), A4 (liveness by applicability, `shared/`), A5 (object states
  and designations; its form admits a fact no action changes) and A9 (areas), each accepted on kitting byte-identical;
  dock_loading's closing part is the walk to the desk, a landmark in stage 1's layout (B13); then the IRB and the
  MPB on dock_loading, after a milestone (one simple scenario per room runs from start to end); then T-G pauses for
  context knowledge, T-K part 1 (framework-wide, from its own handoff; the pre-loaded context stream moved there from
  T-V track 2); 2 `store_pallet` with B10's room (the stores), the gate opened on request,
  the office door's state, A7 (TODO-16), A8's monitored-area rule reopened; then track 4 (A8); 3 check-in and check-out.
  Before each stage's plan the design chat and Hadi agree its layout and setup. Next: stage 1's plan.
  Stage 1's plan is APPROVED (Hadi, 1 Oct 2026; design_decisions.md, "T-G: the second domain's rulings", STAGE 1 PLAN
  APPROVED): `docs/handoffs/plan_T-G_stage1.md`, which every stage-1 build session reads first. Build order, steps 0 to
  8: HEAD runs of the extended set; the rename (zone to area); the areas and R2 (one definition of an agent's area, a
  fixed object's area derived from its position, the replay's walk ends where the body stops, the unread carriers
  removed); A4; A5; A3; dock_loading's catch-up (area ids `area_hall`, `area_office`, `area_truck_side`); its content (a
  method for every area the agent can be in: 8 per robot task, the human's for the hall and the office); the milestone
  (scenario_s03_02, s05_02, s07_02). A robot task with no applicable method stops the run (TODO-152, a ruling before
  stage 2). Next: stage 1's build, step 0 then step 1.
  Steps 0 to 5 are BUILT and accepted (1 Oct 2026; design_decisions.md, "T-G: the second domain's rulings", STAGE 1,
  STEPS 0 TO 5 BUILT): the rename (8d064ca, c21f001); the areas and R2 (b513b82, 9bca721; the shared function is
  `area_at`, the planner's lookup keeps `area_of`); A4 (bd4bddc); A5 (b74485b); A3 (048a36e). Next: the domain steps 6
  (dock_loading's catch-up) and 7 (its content), then the milestone (step 8).
  Steps 6 to 8 are BUILT and the milestone accepted (1 Oct 2026; design_decisions.md, "T-G: the second domain's
  rulings", STAGE 1, STEPS 6 TO 8 BUILT): the catch-up (670cb78, 610fed9); the content (1492789, 512a452); the milestone
  (52b2aae, 8b9d267), scenario_s03_02, s05_02, s07_02, one per room, prior on, 800 steps: the robot completes both
  tasks and every entry of the human's script is closed in all three. Its findings are recorded there (a gap of the
  scenario: no standby walk, no meeting at a shared bay; TODO-135's third instance; TODO-154 to TODO-157). Next: a
  second simple scenario per room; then a step of its own (no change of behaviour): the earlier analyses in `analysis/`
  and the tests sorted under kitting, the instruments' code shared and their run sets, expectations and reports per
  domain, every path named in a record or a README updated, with the preparation of the instruments; then the IRB scenarios on dock_loading, agreed with Hadi before they are authored.
  The second milestone scenario is BUILT and accepted, and stage 1's milestone is complete (1 Oct 2026;
  design_decisions.md, "T-G: the second domain's rulings", STAGE 1, THE SECOND MILESTONE SCENARIO BUILT): scenario_s03_03,
  s05_03, s07_03 (0371035), one per room, prior on, `single_task`, 1000 steps: the robot completes its four tasks and
  every entry of the human's script is closed in all three. Not exercised: the robot arriving at a bay where the human
  stands, two scans at once in one bay (the human finishes a scan before the next pallet arrives). Its findings are
  recorded there (five of six standby walks admitted as a break, TODO-155; TODO-135's fourth instance; TODO-145;
  TODO-154). Next: the design of the IRB set with Hadi (first question: TODO-155); then the sorting of the
  earlier analyses and tests under kitting, with the preparation of the instruments; then the set's authoring and its
  runs.
  The IRB set on dock_loading is AGREED (Hadi, 1 Oct 2026; design_decisions.md, "T-G: the second domain's
  rulings", T-G Q16's block, RULED, T-G records 8): T-G Q16, the walk to the standby place stays without a hypothesis
  for now (the set observes the present recognizer; H1 and H2 on TODO-155, neither approved); `office_break` lasts 90
  seconds (TODO-157, the value changed in the next build step); 14 controlled scenarios (C1 to C14) and 4 mixed (M1 to
  M4), each in all three rooms on the IR setups, expectations derived before the runs, the controlled read first; for
  T-K part 1, the share at an episode's start (TODO-154), not ruled. Next: the build step that sorts the earlier analyses
  and tests under kitting and prepares the instruments for dock_loading; then the authoring of the set, its expectations
  and its runs.
  The IRB on dock_loading is BUILT, RUN AND ACCEPTED, and the IRB of stage 1 is CLOSED (1 to 2 Oct 2026;
  design_decisions.md, "T-G: the second domain's rulings", STAGE 1, THE IRB ON DOCK_LOADING BUILT, RUN AND ACCEPTED): the sort (the tree in "Where to look"), the instruments prepared (the human's sequence from the executor's own
  selection rule; A4 in the oracle; the separation counts), office_break at 90 seconds (45 ticks: one tick is 2
  seconds), 54 scenarios (scenario_s02_02 to _19, s04_02 to _19, s06_02 to _19; C1 to C14 as _02 to _15, M1 to M4 as
  _16 to _19), expectations committed before the runs; 42 controlled and 12 mixed runs, zero disagreements (the
  recognizer behaves as the records specify, not a measure of recognition quality). The baseline: 98 of 147 true
  stretches reach the threshold, median 20 ticks; 49 never, all scans. Findings, none ruled: the same-motion split (T-G
  C5 confirmed, TODO-97), a short walk under equal shares (T-K part 1, TODO-154), the standby walk (TODO-155), one point
  per container (B9's note). Next: the design of the MPB set with Hadi (open: pallets already in a bay while the robot
  delivers others; the robot's last task as a return; expected decisions when the human's sequence depends on the
  robot's, C6).
  The MPB on dock_loading is RULED (Hadi, 2 Oct 2026; design_decisions.md, "T-G: the second domain's rulings", THE MPB
  ON DOCK_LOADING, MPB-DL1 to MPB-DL6): a test and an analysis, no framework change; part 1 a few of kitting's decision
  paths, part 2 one scenario per case dock_loading adds (seven), no full coverage claimed; a new setup kind for the
  controlled scenarios (one full pallet already in each delivery bay; the human scans only those); controlled scenarios
  with full expectations before the run, mixed ones (a dependent script allowed) with declared properties only, never
  claimed to validate the recognizer's decisions; the last-task-as-a-return proposal not taken, the per-room separation
  counts with a standing robot reported instead (TODO-135); office_break stays 90 seconds; `single_task` primary;
  env_layout_03 and env_layout_04 only; about 8 controlled and 4 mixed scenarios, 48 runs. Next: the MPB set's
  scenarios, agreed with Hadi before they are authored.
  The MPB set on dock_loading is AGREED (Hadi, 2 Oct 2026; the same block, MPB-DL7, DISPOSITIONS, THE SET): the
  disjointness rule for controlled scenarios (no pallet named both by the robot's pool and by an assigned scan); kind 3,
  "pallets in the bays" (two full pallets in each bay), one setup each for env_layout_03 and env_layout_04; 9 controlled
  (K1 to K9, kind 3) and 4 mixed (M1, M2, M4 on kind 2 with declared properties; M3 on kind 3 with full expectations),
  both strategies, 52 runs; kind 3 is a test condition, not the work cycle. Next: the build's plan, approved by Hadi.
  The MPB on dock_loading is BUILT AND RUN, its scope reduced for stage 1 (Hadi, 2 Oct 2026; the same block, THE BUILD'S
  PLAN CONFIRMED, DL-P1 to DL-P9, and SCOPE REDUCED AND THE MPB ON DOCK_LOADING RUN): stage 1 establishes that the chain
  runs on dock_loading and produces runs, logs and figures; the behavioural analysis is stage 2's. env_setup_08 and _09
  (kind 3), scenario_s08_01 to _10, s09_01 to _10, s05_04 to _06, s07_04 to _06, run files in configs/dock_loading/mpb/,
  outputs and REPORT.md in analysis/dock_loading/mpb/; the MPB instrument's shared part 4 (measures.py) and alteration
  engine in analysis/instruments/mpb/. 52 runs, all completed; the 40 with full expectations agree with the oracle (0
  disagreements); M(iii) fails in env_layout_04 under single_task (one moving-robot violation); the alteration test on
  dock_loading built, not run. Observations for stage 2 listed unanalysed in the record. Next, as Hadi rules: the close
  of stage 1.
  T-G stage 1 is CLOSED (Hadi, 2 Oct 2026; the same block, T-G STAGE 1 CLOSED): an initial check that the recognizer and
  the chain run on dock_loading; the findings (M(iii)'s failure at 387, the recorded separation violations) go to stage
  2 unanalysed; TODO-153 to TODO-156 tagged [V1].
  The housekeeping step after stage 1's close is DONE (2 Oct 2026): the sweep of old terms ("zone" to "area" in
  wording; TODO-153 closed); the split of the records (`docs/design_decisions.md` the conceptual design of the shared
  core, `docs/design_records.md` everything else, one heading per task); the rule for analysis/ (git tracks reports
  and code only; data and figures stay on Hadi's disk). Open: the rewriting of each conceptual entry into one current
  rule; the destination of two old items under docs/ (the old ROS planner reference text, the folder of old layout
  pictures), deferred until Hadi names one.
  The entry point for the next T-G design chat is `docs/handoffs/T-G_forward_inputs.md` (what is ruled, open and parked
  per stage after stage 1). Next: the stage to be named by Hadi.
  T-K part 1 (context knowledge) is RULED AND AMENDED, its build NOT STARTED (Hadi, 2 and 3 October 2026;
  design_decisions.md, "T-K: context knowledge in the recognizer's belief", R1 to R8, A1 to A7, AM1 to AM9;
  design_records.md, "T-K", the cut, the open items). T-K is framework-wide: it concerns kitting and
  dock_loading alike. Context knowledge acts in the recognizer's belief only, never on the human; belief =
  normalise(prior × evidence), the prior computed at each run from the present context facts as the normalisation of
  the strengths of what is live (assigned work as a whole 1, each live foreseeable task its declared low or high
  strength by its occurrence condition, divided among the task's live hypotheses), equal division inside work as a
  whole; the re-entry and boundary rules are shares of the evidence, not of the belief (AM1); every strength > 0
  (AM4); one declared duration; the gate unchanged; the earlier entry "Assigned-task pool is a support restriction,
  not a prior" superseded in part (R8, AM6). Two independent run options, both on by default at the build:
  `assignment_knowledge` (today's `assignment_prior`, not renamed before the build) and `context_knowledge` (new);
  context knowledge off gives today's equal prior (AM3, AM9; replaces R9). T-K part 1 builds R1 to R4, R6, R7, crisp context facts, the setup's timeline of context facts (AM34; since AM40 the default, which a scenario's own timeline replaces whole) and
  the removal of the domain task names and constants from the recognizer (TODO-66); an occurrence condition is a
  conjunction (AM7). Open, before the build, unchanged: the values for kitting and dock_loading (Hadi states them), the
  perception assumption, the tests. T-K part 2 (the build of R5, degrees; open: the representation of a context value
  and of a degree, AM8) is at the end of the V1 queue, after track 3b. Future work: TODO-158 to TODO-161 [FW]
  (TODO-162 superseded by AM3). Next: T-K part 1's open
  items, then its build's plan.
  T-K part 1's content points 1 (the values) and 2 (the perception assumption) are RULED (Hadi, 3 October 2026;
  design_decisions.md, the same entry, CONTENT POINTS 1 AND 2, AM10 to AM29; design_records.md, "T-K", CONTENT
  POINTS 1 AND 2): every fact crisp (AM10); an occurrence condition reads timeline facts, object states and recency
  facts, with "and" and "not", "or" staying in T-K part 2 (AM11, amends AM7); coffee_break: break_time and not recent;
  ac_activation: room_warm and not ac_on; office_break: not recent (AM13); a recency fact per task, 3 times the task's
  wait, from the observed completion (AM14, AM16); the strengths (AM17); the A/C switch, an object with the state ac_on,
  at most one per layout in V1, ac_activation and room_warm in both domains, none in dock_loading's existing rooms
  (AM18); the long-shift rule leaves with no replacement (AM22); acceptance "identical except for the lines the build
  names" (AM24); the timeline's facts known exactly and at once through the world state, a recency fact from the mind's
  memory of an observed completion (AM25 to AM27; `docs/assumptions.md` 5.4, 6.1 to 6.3). Content point 3 (the tests)
  is open. Future work: TODO-163, TODO-164 [FW]. Nothing built. Next: content point 3, then ccode's list of the layouts
  with more than one A/C switch and what rests on them (AM19; Hadi decides on it; the layout change and the
  regeneration before the build), then the build's plan.
  T-K part 1's content point 3 (the tests) is RULED (Hadi, 3 October 2026; design_records.md, "T-K", CONTENT POINT 3,
  THE TESTS, KT1 to KT7; design_decisions.md, the same entry, AM11's AM34): kitting first, then dock_loading's stage 1
  scenarios, in each the IRB with an idle robot before the MPB with a working robot (KT1); on kitting Hadi's rooms
  env_layout_15 (no A/C switch), _16 (coffee machine and A/C switch in a dense cluster), _17 (15 plus an A/C switch
  between two deliveries; MPB or mix), env_layout_10, _11, _02 as they are, as a comparison (KT2; env_layout_02 after
  Hadi's correction of its object sizes, 4191202, which only the viewer reads); the basic set varies
  only where a foreseeable task is placed (between tasks, or inside a task between its actions), two setups per layout
  (dropped by KT13, 4 October 2026),
  five or more scenarios each, context knowledge on and off, two MPB cases, the measure the tick at which the true task
  reaches the threshold and is admitted and whether a retraction follows, expectations before the runs, the duration
  mismatch a later set (KT3); the setup, not the scenario, holds the timeline of context facts (KT4, AM34; amended by AM40, 4 October 2026: the setup
  states the default timeline, a scenario may state its own, which replaces it whole); a round
  without context knowledge first (KT5); findings, none changing a value (KT6). Nothing built. Next: the round without
  context knowledge (rooms 15, 16, 17 in the IRB with the present equal prior); then a new design chat takes the build
  of T-K part 1 (the list of the layouts with more than one A/C switch, AM19; the build's plan; the build; the runs with
  context knowledge on; dock_loading; the close); a later chat returns to T-G's stage 2.
  The round without context knowledge (round 1) is BUILT, RUN AND ACCEPTED (3 October 2026; 4cd7bca, 4c71b44;
  design_records.md, "T-K", ROUND 1, KT8 to KT12; `analysis/kitting/irb/tk1/`, README.md and REPORT.md): 31 scenarios
  (scenario_s13_01 to _07, s14_01 to _11, s15_01 to _13 on env_setup_13 to _15), robot idle, expectations committed
  before the runs, 0 disagreements at 1e-9, every run below step 500 (TODO-66's weight never acts); env_layout_16 lost
  its two south-east shelves before the runs, the cluster unchanged (KT9). The comparison reads three conditions: A
  context knowledge off (round 1), B on with the fact not holding, C on with it holding (KT11); for the A/C the measure
  is its belief at arrival (KT10). Next: a new design chat takes the rest of T-K part 1 from
  `docs/handoffs/T-G_forward_inputs.md`, section 5: the layouts with more than one A/C switch (AM19), the build's plan,
  the build, the setups' timelines and the runs in B and C, the two MPB cases, dock_loading's part, the close.
  T-G stage 1.5 was renamed T-K part 1 on 3 October 2026; git commit messages use the old name.
  T-K (design_records.md, "T-K", THE TASK RENAMED: T-K AND ITS PARTS) is context knowledge as a whole, a task of the
  pipeline (framework-wide), not a stage of T-G. Part 1 (V1, ongoing):
  crisp context knowledge, R1 to R8, AM1 to AM39, KT1 to KT12, the state above. Part 2 (V1, at the end of the V1 queue after track
  3b): degrees (R5: membership functions, soft edges of a window, the gradual return after a task, "or", with "long
  work without a break" its open item; succession, R4, after T-G stage 2). Later, future work: the stream of context
  values with the world's dynamics, TODO-163, TODO-164, TODO-158 to TODO-161. A letter is never given to a different
  task; a task may be paused, resumed and revisited. T-G is paused after its stage 1; T-K part 1 runs now; T-G resumes
  at its stage 2 when T-K part 1 is closed. Next: the rest of T-K part 1 in a new design chat, as above.
  The strengths are REVISED (Hadi, 3 October 2026, the design chat on the rest of T-K part 1; recorded 4 October 2026;
  design_decisions.md, the same entry, R3's AM35, AM36, AM39; design_records.md, "T-K", AM37 under AM13, AM38 under
  AM17, THE STRENGTHS REVISED). It supersedes the low and the high strength, the occurrence condition, "not" in T-K part
  1 and the values of AM13 and AM17 stated above. "Work as a whole" reads "the assigned tasks as a whole" (AM35, wording
  only). Three levels per foreseeable task (AM36): if its suppressing condition is satisfied, the suppressed strength
  0.005; otherwise, if its raising condition is satisfied, its raised strength; otherwise the ordinary strength 0.02;
  each condition optional, one fact or a conjunction of facts from the three sources, no "not" ("not" and "or" are T-K
  part 2's). coffee_break: suppressed by its recency fact, raised to 2 by break_time; ac_activation: suppressed by
  ac_on, raised to 0.5 by room_warm; office_break: suppressed by its recency fact, no raising condition; recency
  durations unchanged, 90 and 135 ticks (AM37, AM38). The reading per value, s / (1 + s) of task starts, still proposed
  (AM39). Stale and marked: the coffee break's prior equal to θ (now 2/3), the expected directions with context
  knowledge on (the design chat restates them before those runs), R5's linear rule (restated for two conditions, T-K
  part 2), the form for "not". Open for the build's plan: which value the gate compares with θ (ruled by AM42, 4 October
  2026: the belief over the live hypotheses). The statement of the
  prior: `docs/context_knowledge_method.md` (the rule in "Where to look"). Nothing built. Next: unchanged (KT12's steps,
  from `docs/handoffs/T-G_forward_inputs.md`, section 5).
  Step 1 of T-K part 1 is DONE (Hadi's ruling of 4 October 2026 on AM19; design_records.md, "T-K", STEP 1; 32029d3,
  098b1a8, 35c9db8): env_layout_05 keeps one A/C switch, ac_switch_1, and scenario_s04_01 one ac_activation; every
  layout of both domains holds at most one A/C switch; tb1a's two s04_01 logs regenerated, every other maintained
  baseline byte-identical; 14 early frozen analyses deleted (analysis/README.md). Next: the plan for the build of
  context knowledge (BUILD DISCIPLINE, step 1), after one design question that the design chat puts to Hadi first.
  Step 2 of T-K part 1, the build's plan, is WRITTEN AND RULED (4 October 2026; `docs/handoffs/plan_T-K_part1.md`;
  design_decisions.md, the same entry, AM40 to AM53; design_records.md, "T-K", THE TIMELINE IN THE SCENARIO and THE
  BUILD'S PLAN, RULED). Where the timeline is stated (AM40): the setup states the default; a scenario may state its own,
  which replaces it whole; the run's header prints the timeline in force and its source; the second setup per room is
  dropped (KT13); the tests read context knowledge off against on, each case labelled by the state the script meets
  (KT14); the override of the timeline is later work (AM41, TODO-177). The plan's decisions: the gate compares θ with
  the belief over the live hypotheses, the floor and the pin scaling staying in the reported distribution only (AM42;
  its removal there TODO-178), in its own commit with its own regenerated baseline (AM53); the A/C's action switch_on
  with the effect ac_on (AM43); an object-state condition holds for any object of its type (AM44); dock_loading's
  ac_activation from the hall only (AM45); windows in ticks, half-open (AM46); the memory's recording rule (AM47); the
  regression scope (AM48); the instruments' check on round 1 (AM49); a timeline fact stated by a timeline only (AM50);
  `SimModel` takes both run options explicitly (AM51); no condition of a schema names a timeline fact (AM52, AM54);
  ccode's P1 to P5 accepted. On the cross-check (AM55 to AM58): the gate's stage reruns round 1 and kitting's IRB and
  MPB sets, outputs replaced, and stops on a failed declared property; dock_loading's IRB and MPB sets stale until its
  step; TODO-179 (the boundary label for switch_on), TODO-180 (the viewer's confidence). On its consequences (AM59 to
  AM63): one external copy of the three kitting sets' untracked data before they are replaced; the gate's stage
  committed only after its checks pass; its stop conditions; the run without assignment knowledge never stops the
  build. The plan is approved; a new design chat takes the build from `docs/handoffs/T-G_forward_inputs.md`, section 5. Nothing built. Next: the build (BUILD DISCIPLINE, step 2), stage by stage as the plan states.
  Step 3 of T-K part 1, the build, is DONE (4 October 2026; design_records.md, "T-K", THE BUILD, STAGES 1 AND 2 and THE
  BUILD, STAGES 3 TO 7; the session's state file `docs/handoffs/build_T-K_part1_state.md`; the roadmap's STEP 3 DONE
  line). The eight stages of the plan are built, each checked against the previous stage's outputs: 0 the baselines
  B0; 1 the rename `assignment_prior` → `assignment_knowledge` (b85494d); 2 the gate on the belief over the live
  hypotheses (AM42; 91774ce, 3b05a8a, 733e593), round 1 and kitting's IRB and MPB sets rerun under it and their outputs
  replaced (B2, the baseline of every later stage), no stop condition met; 3 the run option `context_knowledge` and the
  removal of the context weight and its constants (TODO-66 closed; bbb7227, 67b899e); 4 the timeline of context facts
  (`Timeline`, `Window`, the setup's `"timeline"` list and the scenario's `window(...)` form, the resolution at load, the
  `[run_mesa] timeline` line, the load checks; f70f72f) and the facts break_time, room_warm, ac_on with the action
  switch_on and dock_loading's ac_activation (2393935); 5 the mind (e589731: `ContextKnowledge` as the domain's declared
  context knowledge in its registry, `shared/completion_memory.py` the memory of observed completions, the prior in the
  recognizer with `BeliefState.belief`, `prior`, `levels` and the `[IR-context]` line; both run options on by default,
  TODO-139 closed); 6 the instruments (the IRB's oracle computes the prior on its own from the declared values and the
  method document, rules 29 to 33; the columns prior, levels, recent; the readers label each case by the state the
  script meets, KT14, and give the A/C's belief at arrival, KT10); 7 these records. With context knowledge off every
  maintained log and every instrument output is B2's except the named lines (the `[run]` field, the timeline line,
  switch_on's name and its effect ac_on in `[rec]`, `[human]` and the trajectory, the new columns); round 1 with it on
  agrees with the oracle in all 31 runs (AM49; results not read). Step 4 on kitting with the idle robot is DONE (4 October
  2026; design_records.md, "T-K", STEP 4; `analysis/kitting/irb/tk2/`): env_setup_13 to _15 state break_time 178 to 300,
  the A/C scripts room_warm from 150, 26 scenarios state their own; 59 runs agree with the oracle; the directions are
  read per side in its REPORT.md. Question S is ruled (AM65, 4 October 2026): the four strengths stay as ruled, not
  tuned to the movement evidence. The reading for question G (admission and retraction under context knowledge) is in
  step 4's REPORT.md ("The reading for question G"; design_records.md, "T-K", THE READING FOR QUESTION G). Question G
  is ruled (AM66, 4 October 2026): the gate and the retraction stay as ruled. Step 5, the planning cases (five, KT15),
  is DONE (4 October 2026; env_layout_18, env_setup_16, scenario_s16_01 to _06; analysis/kitting/mpb/tk/REPORT.md: 9
  runs, 0 disagreements with the oracle; findings for TODO-146 and TODO-132 (a)). Step 5b, the existing kitting sets
  with context knowledge on, is DONE (4 October 2026; analysis/kitting/mpb/tk5b/REPORT.md: 33 runs, 0 disagreements;
  12 of the planning set's 16 authored cases reached, E6, D9 and A8 without an instance with it on). A design
  discussion followed and is closed: Hadi ruled (4 October 2026; design_decisions.md, "T-K", AM67 to AM72 under R7 and
  R3; design_records.md, "T-K", THE GATE AFTER STEP 5B, RULED): observation warrant is required at admission for every
  hypothesis (commitment warrant alone no longer admits); the gate refuses a leader that the evidence alone ranks below
  another live hypothesis (rank only, an exact tie passes; the leader is "outranked", reported by the recognizer as a category per live hypothesis); the end of an admission
  and all strengths unchanged. Nothing built. Next: open. The build's plan is approved (Hadi,
  4 October 2026, D1 to D7; `docs/handoffs/plan_T-K_gate.md`; design_records.md, "T-K", THE GATE'S BUILD PLAN, RULED;
  D4 closed the coverage-matrix question). The build is DONE (4 October 2026; design_records.md, "T-K", THE GATE
  RULINGS, BUILT: `BeliefState.evidence_rank` and the `[IR-rank]` line; `none(leader_outranked)` asked last;
  commitment warrant removed from the meta-planner, `[meta-proj] built warrant=observation`; the instruments; the four
  maintained sets regenerated, 17 logs moved by AM67). Step 5d, the measurements after the gate change (Hadi named the
  gate's discussion to build step 5c, these measurements step 5d), is DONE (5 October 2026; analysis/kitting/tk5d/REPORT.md;
  design_records.md, "T-K", STEP 5D): 0 disagreements after D3 amended (Hadi: exact ties in the oracle are ties); every
  moved case as expected by ruling; the true task's admissions unchanged, the wrong ones and the two cases below
  min_separation from a wrong admission removed. The steps of T-K part 1 stand as a tree at the top of
  `docs/handoffs/T-G_forward_inputs.md`, section 5. Step 5e, context knowledge on kitting's rooms 02, 05, 06, 07 and on env_layout_19 and _20 (copies of 08 and 09 with a
  coffee machine), with 100 new scripts, is DONE (5 October 2026; analysis/kitting/tk5e/REPORT.md; design_records.md,
  "T-K", STEP 5E): 772 runs, 0 disagreements. Step 6, dock_loading's stage 1 measured in full in kitting's form, is DONE
  (6 October 2026; design_records.md, "T-K", STEP 6; analysis/dock_loading/tk6/, COMPARISON.md): 568 runs, 0
  disagreements; ccode's provisional decisions (TODO-185's reading of the tag among them) wait for Hadi. Step 7 (the
  close) is on hold.
  T-F part 1, the conditions human-unaware and intention-unaware, is RULED (Hadi, 5 October 2026; design_decisions.md
  and design_records.md, the entry of that title, R1 to R10; glossary §9): two run options `human_aware` and
  `intention_aware`, both on by default, an option off setting the options above it off; intention-unaware is
  TODO-137's fallback-only control (the gate refuses for both callers, `none(intention_off)`); human-unaware is a
  condition of the mind, not of perception. The plan (`docs/handoffs/plan_T-F_part1.md`) is approved with A to G
  (5 October 2026: under `intention_aware` off the recognizer computes nothing; human-unaware covers the mind and the
  separation stop; `none(no_human)` before the gate in every run). Stage 1 is BUILT (5 October 2026; design_records.md,
  the same title, STAGE 1 BUILT): the two options, the override and its line, the header, the refusals; with both on
  every existing run is identical but for the two header fields and the reference logs' `none(no_human)`. Stage 2 is
  BUILT (5 October 2026; design_records.md, the same title, STAGE 2 BUILT): `analysis/instruments/mpb/run_set.sh`, a set
  whose settings live in its run files, a run named by its run file (I), the result table with the settings as columns
  (`table.py`), the oracle extended to both conditions; the check (the planning test-bed's 16 in each condition,
  `configs/kitting/tf1/check/`, `analysis/kitting/tf1/check/`) 0 disagreements. Next: the measurement (H), after
  Hadi's rulings on its open points. The rest of T-F keeps its place after T-G.
  The measurement is RUN (5 October 2026; rulings K to O, design_records.md, "T-F part 1", THE MEASUREMENT;
  `analysis/kitting/tf1/REPORT.md`): 128 scenarios in the four conditions and step 5e's 176 timeline copies
  intention-aware with context knowledge on, 688 runs, `single_task`, 0 disagreements with the oracle; outputs one
  folder per scenario, the runs by serial (K); one figure per run on one tick axis (N).
  T-F part 1 is CLOSED (Hadi, 5 October 2026; design_records.md, "T-F part 1", THE CLOSE; for a reader outside the
  repository `analysis/kitting/tf1/COMPARISON.md`): steps 2 and 3a (recognition; context knowledge with no timeline
  fact in force, the prior alone) show no difference this set can distinguish from zero; with a timeline fact in force
  (step 3b), a fact in accord with the human's task speeds its
  admission and one not in accord delays it, with little change in completion and violations (COMPARISON.md, "Step 3b: context knowledge with a timeline fact in force"); part E executed (analysis/ 16,488 files, 2.0 GB; analysis/README.md). T-F part 2
  is parked (docs/handoffs/handoff_T-F_part1.md). Next: T-G's next stage with T-K part 1's steps on dock_loading
  (docs/handoffs/T-G_forward_inputs.md).
  Not to be
  started unasked: T-F (part 1 closed, part 2 parked), T-V, the T-D tail, T-K part 2 and T-S, i.e. Phase 5
  (evaluation, T-F; the randomised harness TODO-47 is part of it), the viewer and the demonstration, 4D (detour
  strategy) and Phase 6 (ROS / PRIEST execution); and no T-G stage before its task.
  ASKED FOR (Hadi, 6 October 2026): T-viz, the web-ui (`docs/handoffs/handoff_T-viz.md`; design_records.md, "T-viz, the
  web-ui"). Its stage 0 is done and closed (6 October 2026), one step per session (0.1 recording done, 6 October 2026; 0.2 code structure done, 6 October
  2026: `mesa_sim/run_config.py` reads the run configuration and builds the model, `mesa_sim/sim_run.py` is one
  sim-run with its log pair, every start uses both, the headless start imports no Solara; 0.4 messages done, 6 October
  2026: `webui/` at the root, the message definitions and the interface a simulator's piece implements, independent of
  every simulator and domain, and Mesa's piece `mesa_sim/webui_adapter.py`; glossary §11; 0.3 the style trial done,
  6 October 2026: `webui/page/`, the env-pane drawn from saved messages (`mesa_sim/webui_export.py`), the scene appearance
  `webui/appearance.py` with `domains/<domain>/appearance.json`, the theme `webui/page/src/theme.ts`; its look accepted by
  Hadi "for now and for stage 0", its technology the web-ui's: React, TypeScript, Vite, three.js through React Three
  Fiber and drei, uPlot planned for 1c, no UI kit). Stage 1a is CLOSED (Hadi, 6 October 2026, preferred;
  design_records.md, "T-viz, the web-ui", 1a, STAGE 1a CLOSED; its plan `docs/handoffs/plan_T-viz_1a.md`): increments
  (i) to (iv) built (the server `webui/server.py`, the start `mesa_sim/run_webui.py`, the page's frame; the full
  selection, the views, the address; the free camera, looks by state, display places; panel 4a with the human's script,
  the world's context and the tag per task, test 2); one polishing round follows after stage 1c, from Hadi's list; the
  solara-ui is not archived, an alternative start kept running with a light check (after a change to code it uses: it
  starts and one sim-run takes a few steps without an error, in one domain; none after a change to the page alone). The
  web-ui's logic is tested, its look is not (the plan's P25, corrected). A new T-viz session reads the handoff's section
  "State after stage 1a" first. Stage 1b is BUILT (6 October 2026; design_records.md, "T-viz, the
  web-ui", 1b, THE RIGHT PANEL, BUILT): panel 4b in five blocks (body, belief, admission, projection, decision), the
  messages' `robots` section, `RobotAgent.last_decision` for readers; five readings provisional, raised to Hadi; his
  review open. Stage 1c is BUILT (7 October 2026; design_records.md, "T-viz, the web-ui", 1c, THE BOTTOM PANEL, BUILT): panel
  4c in five lanes, drawn by the page's own canvas; the past view; one colour per task; `WorldTick.separations` and
  `TaskRef.identity` in the messages; Hadi's review open. Stage 1's order is 1b, 1c, 1d, 1e (1d, 1e: paths as stripes on the floor; TODO-197). Next: 1d; a later
  T-viz stage starts only when Hadi asks for it. T-viz is the name for all web-ui work (Hadi, 6 October 2026, preferred): T-V track 1 is
  T-viz stage 1, T-V track 2 (Phase 7, live events) is T-viz stage 3; stages 2 and 3 are [FW] for now. "T-V" and "the
  viewer and the demonstration" above read as those T-viz stages (docs/rename_table.md, "Task names").
- `shared/meta_planner.py`: blocks B1 (human projection), B2 (`b2a`), B3 (selection on realized
  cost) exist. `full_reorder` (B3.B) is built (`_replan_orderings()`, T-B2b / T-B2c): orderings are ranked
  on their realized cost, `realize()` running one minimal-shift search per entry (T-B Q2), and the hold sent
  is the hold before the first entry; no `full_reorder` baselines are recorded, which stays with T-B3.
  Touch it only in a T-B task, and only the step that task names.
  B2 is an evaluation factor, not a design step: `b2b` stays a stub. Change only what the task
  specifies; do not fill in unspecified block logic, flags or strategies.
- `shared/recognizer.py`: rebuilt and handed back (`docs/recognizer_handback.md`, rewritten to HEAD at the T-D
  Stage 1 build). Touch it only if the task says so.
- ROS side is paused. Do not modify anything under `ros_sim/`.
- `domains/dock_loading/` is deferred. Do not modify it unless the task says so. It must still
  import without error (`run_mesa.py` imports its registry).
  SUPERSEDED FOR T-L'S STAGES ONLY (26 Sept 2026): kitting and dock_loading migrate together, so T-L's stages may
  touch `domains/dock_loading/`; it must still import and run (design_decisions.md, "Layouts, setups and scenarios",
  ruling 8).
  SUPERSEDED (T-G, 1 Oct 2026): dock_loading is no longer deferred; it is T-G's domain, touched by T-G tasks only, and
  it must still import.
- `domains/kitting/env_layout99.json` is the old `env_layout1` with obstacles, kept for later and
  not registered; it stays unsplit (T-L stage 1).
- The code is the source of truth. Docs are maintained but can lag. Do not change code to match
  docs; report the contradiction. Edit docs only when the task says so.

## Methodology

- Scenarios are experiments for evaluating the design, not the specification for it. Never
  introduce a mechanism, threshold, margin or special case because it improves a scenario.
- Measure a premise rather than assume it. Premises stated in task prompts have been wrong more
  than once; measurement caught it. If a premise is wrong, report it.
- Findings are drawn only from the test set a task names. Few, well-understood scenarios are the
  default; broad testing with special cases is a separate, later activity.
- Layouts, scenarios and the saved logs are debugging examples, not a settled evaluation reference.
  Hadi may change or rearrange any of them at any time; the logs are then regenerated; no design
  argument rests on them.
- Keep measurement tasks and build tasks apart. A build task is the change plus the check it
  needs, not a characterisation study.
- Prior. Runs, tests, debugging and the ccode reports assume the prior ON: the robot knows the human's assigned tasks,
  and the hypothesis space is that pool plus the foreseeable tasks. Prior OFF (the robot does not know the human's
  assigned tasks) is a later test mode, run once the framework is stable, when both modes are tested and reported.
  Until then a prior-OFF measurement is an appendix, never the primary set, and no ruling is made on prior-OFF numbers
  alone. Revised in `docs/assumptions.md` 1.4: prior off is a recognizer diagnostic and ablation configuration; an
  artefact produced only under it never produces a rule. The run option's default is still off (TODO-139).
  SINCE T-K PART 1'S BUILD (4 October 2026): the option is `assignment_knowledge`, on by default, beside
  `context_knowledge`, on by default (TODO-139 closed). The maintained sweeps run both settings of the assignment
  option with context knowledge off; the runs with it on are step 4 of T-K part 1 (the timelines are not authored).
- Every run made through a test or analysis instrument produces its per-tick figure (Hadi, 5 October 2026, standing;
  design_records.md, "T-F part 1", THE FIGURES): with the recognizer running, the belief, the adequacy, the gate and
  the decisions per tick, and with context knowledge on the context facts in force beneath the belief; in a
  human-unaware or intention-unaware run the decisions, their projection (none or the fallback), the holds and the
  robot–human distance against min_separation. A set gets its figures when it is next run; no old set is rerun only to
  make figures. Reason: Hadi reads a run from its figure. Since the measurement of T-F part 1 (N): one figure file per
  run (`figure.png`), every panel on one shared tick axis, the distance on a scale readable near min_separation; a run
  made by `run_mesa.py` directly gets it from its log (`analysis/instruments/mpb/figure_of_log.py`).
- When a task delegates a decision, decide from the design: state the reasoning before implementing, then evaluate. If the evaluation contradicts the reasoning, report it; do not switch the decision to fit the results.

## Workflow rules

1. Work autonomously within the task. Plan for yourself; do not wait for approval unless the
   task defines a checkpoint.
2. Surgical changes only. Match existing style. No unrelated refactors, renames, or
   reformatting. No speculative abstractions or configurability.
3. Ask, don't guess. If the code does not match what the task describes in a way that changes
   what to build, or a decision is genuinely ambiguous, stop and report.
4. Flag, don't fix. Issues outside the task scope: list them at the end of the report.
5. Git: commit directly on `main`, in logical groups with clear messages, once the task's checks
   pass. Use a feature branch only when asked. Never push. Never rewrite history. If the working
   tree holds changes you did not make, ask before committing them.
6. Report in the chat reply, concisely: commits; what changed and where; the numbers the task
   asked for; contradictions with the task or the docs; flags. Do not create a REPORT.md, an
   analysis directory, checksums or regeneration scripts unless the task asks for them.
7. Do not delete or overwrite a file that this session did not create. A script that removes files must target only
   its own output folder. Ask before any other deletion.

## BUILD DISCIPLINE

A standing convention for every build or refactor session.

- Two steps. Step 1, plan only: report the intended structure (classes, fields, what is removed, which files), the
  cases the design does not cover, and the tests to run. No code, no commit; wait for Hadi's confirmation. Step 2:
  build what was confirmed.
- No hidden assumptions: where the design is silent, ask.
- No shortcut to reach a running state; a run that works by a workaround is a failure of the task.
- Nothing left untyped: no `List[Any]`, no `Union` of unrelated types, no kind strings, no booleans standing for a
  class.
- No new check function that works by string or key matching, and no patch that goes around the conceptual design;
  identity is object identity or value equality of typed objects.
- If a rule above blocks progress, stop and report why; that report is the deliverable.
- Conceptual changes need Hadi's ruling (Hadi, 1 Oct 2026, standing): the recognizer's scoring and admission, the
  meta-planner's candidate evaluation and cost, the projection's semantics, the planner's method selection and the
  trigger set are not changed at the conceptual level without Hadi's ruling. A change to `shared/` or `world/`
  is domain-agnostic and named in an approved plan. Otherwise stop and report before changing anything.

## Cost discipline

Sessions are metered. Keep them cheap by default, without weakening what protects the work.

Cheap by default:
- Ask only what feeds the next decision. Report the numbers the task names, not a full
  characterisation.
- Measure one value, not a sweep, once a value has been decided. Sweep only when the question is
  genuinely "where does behaviour change".
- Narrow the conditions to the ones that can answer the question.
- Do not re-verify what a committed report in `analysis/` already establishes (numerical method
  checks, grid independence, instrumentation neutrality). Cite it.

Never sacrificed:
- Drift detection before a task is called done: run the regression sweep and diff the greps.
  Silent behaviour drift is the failure mode this project has actually had. Differences outside
  the task's test set are listed one line each (condition, first differing step, grep), not
  analysed.
- Byte-identity when a task claims to change no behaviour. Then any difference is a bug.
- Measuring a premise rather than assuming it.

If a task cannot be done within these limits, say so and propose a smaller version rather than
silently running the large one.

## Running

Interpreter: `~/python-envs/ir-nomesa-env/bin/python`, the working environment; `requirements.txt` is pinned to it.
It needs `ruamel.yaml` (in `requirements.txt` since T-L stage 4): the viewer writes the run file's overrides block
round-trip, so the file's comments are kept.

```bash
# headless; --layout is optional (T-L stage 1): a run that names none takes the scenario's first reference layout.
# The [run_mesa] start line names the triple; setup ids are env_setup_NN since stage 2 (the setup is the scenario's, never a flag).
PYTHONHASHSEED=0 python mesa_sim/run_mesa.py --domain kitting --layout env_layout_04 --scenario scenario_s01_06 --steps 200
# the two knowledge options (both on by default since T-K part 1's build): assignment knowledge (the robot knows the
# observed human's assigned-task pool; `--assignment_prior` before the build) and context knowledge (the prior from the
# domain's declared context knowledge; off: the equal prior)
PYTHONHASHSEED=0 python mesa_sim/run_mesa.py --domain kitting --layout env_layout_04 --scenario scenario_s01_06 --steps 200 --assignment_knowledge true --context_knowledge false
# another run file, and one override of a fact of the run's artefacts (T-L stage 4; repeatable)
PYTHONHASHSEED=0 python mesa_sim/run_mesa.py --run my_run.yaml --override layout.shelf_2.position=-300,-300
# visualization
solara run mesa_sim/run_mesa.py -- --domain kitting --layout env_layout_03 --scenario scenario_s03_01
# the web-ui (T-viz 1a): the page built once (cd webui/page && npm ci && npm run build), then http://127.0.0.1:8000/
PYTHONHASHSEED=0 python mesa_sim/run_webui.py --domain kitting --scenario scenario_s01_01
```

Logs go to `logs/run_<timestamp>.log`, with the `.rec` stream beside it: one pair per sim-run, not per process (T-viz
0.2, `mesa_sim/sim_run.py`), opened at the sim-run's first step or its end, so a model built and never stepped writes
none; a start that fails still writes its pair (empty on a flag error), so the newest pair is always the last start's;
a name already taken gets `_2`, `_3`. The reading of the run file and flags and the building of the model are
`mesa_sim/run_config.py`'s, one definition for every start. Defaults come from the run file, `configs/experiment.yaml` or the yaml
`--run` names; CLI flags override. The flags: `--domain`, `--layout`, `--scenario`, `--steps`, `--human_aware` and `--intention_aware` (true/false; T-F
part 1: off the human-unaware and the intention-unaware robot, an option off setting the options above it off),
`--assignment_knowledge`
(true/false; `--assignment_prior` before T-K part 1's build, no alias), `--context_knowledge` (true/false), `--strategy` (single_task | full_reorder), `--gate_strategy` (none | b2a | b2b),
`--cost_strategy` (realized | plain),
`--separation_stop` (true/false), `--test_level` (the recognizer's adequacy test level α, strictly between 0 and 1), `--run` (another run file; it replaced `--experiment` in T-L stage 4, no alias) and
`--override <path>=<value>` (repeatable). Parsing is strict: an unknown
or misspelled flag, an unknown yaml key, or a bad value stops the run. Each robot's `[run]` header
names the policy and evaluation switches the run took (strategy, gate, cost, stop, assignment knowledge, context
knowledge, θ, ρ, min_separation and β, each with its source: the body supplies both, `mesa_sim/mesa_configs.yaml`, 50 cm
and 0.01 /cm; since T-D Stage 1 also the test level α and the body's speed, 20 cm/tick). After the `[run_mesa]` start
line every log prints `[run_mesa] timeline source=<scenario|setup|none> windows=[...]`, the timeline of context facts in
force (T-K part 1, AM40). A run with `human_aware` or `intention_aware` off then prints `[run_mesa] options <option>=off
sets off: ...`, the options the override set off (T-F part 1, R5); the `[run]` header prints `human_aware` and
`intention_aware` and every option's effective value.

Overrides (T-L stage 4; design_decisions.md, "Layouts, setups and scenarios", ruling 7; glossary §9): a closed list of
three, one path each, the same in the run file's `overrides:` block (a mapping path: value) and in `--override`:
`scenario.<agent>.start_position` (two numbers), `layout.<fixed object>.position` (two numbers),
`setup.<movable object>.initial_container` (an id); every other path is refused. `mesa_sim/overrides.py` reads them
into typed classes, the loader (`SimModel`) applies them to the artefacts as read, before any check, and each is
printed as `[run_mesa] override <path>=<value>` after the start line, sorted by path, in the `--override` form. A run
with an override is never a fixture or a baseline. The viewer (`solara run`) shows the run file's triple and overrides,
and its form writes the three kinds into the run file it was started from, then reloads: started on
`configs/experiment.yaml`, an override it writes there reaches every run that takes the default file, the sweeps
included (their diffs show it on the override lines); start the viewer on a copy (`-- --run my_run.yaml`).

## Regression checking

The simulator is deterministic given a fixed hash seed. Prefix every run with `PYTHONHASHSEED=0`
until TODO-42 is fixed.

Regression sweep: five fixtures, each with assignment prior off and on, each run to completion:

| fixture | layout | note |
|---|---|---|
| scenario_s01_01 | env_layout_01 | intersecting paths and table convergence |
| scenario_s02_01 | env_layout_02 | coffee break and AC activation; needs about 450 steps |
| scenario_s03_01 | env_layout_03 | table convergence; does not finish in 200 steps |
| scenario_s01_06 | env_layout_04 | mirror-symmetric intersecting paths |
| scenario_s04_01 | env_layout_05 | foreseeable task and one AC-switch walk (one switch since T-K part 1, step 1) |

Old ids (scenario_00 on env_layout0 and so on) are mapped in `docs/rename_table.md`; the frozen records keep them.

Use the step counts of the sweep scripts (`analysis/kitting/tb1a_destination/sweep.sh` for the five and the evaluation
fixtures; before T-L stage 3, the frozen `analysis/kitting/f1_robot_responsible/sweep.sh` (deleted 4 Oct 2026) and `analysis/kitting/f47_fixtures/sweep.sh`,
on the old ids). The current baselines are the Track 2.5 regeneration of the four maintained sets below (their "2.5"
README sections; before it L-build, P-build and P4-build, each with its own section); what follows is the T-L stage 3
regeneration's description, whose folders and names still hold, with their
`.rec` streams, named `<layout id>_<scenario id>_<run options>.log`: `analysis/kitting/tb1a_destination/sweep/` (the five plus
scenario_s03_06 / scenario_s05_01 / scenario_s05_02, both priors, stop off, `single_task`; logs local, md5s in its
README, the "T-L stage 3" section), `analysis/kitting/tb1b_two_tables/sweep/` (scenario_s06_01 / scenario_s06_02),
`analysis/kitting/tb1c_realized_flip/sweep/` and `analysis/kitting/tb3_full_reorder/sweep/` (both strategies). They differ from the
stage-2 logs (99563cc) in the `[run_mesa]` line alone (the ids), the `.rec` streams byte-identical; T-L stages 1 and 2
had changed the same line alone (the setup id), with no README section. The T-H follow-up set differed from the T-H4
regeneration (e4fe110) by the `[scenario-coverage]` line at load alone (the scenario's composition and scenario
coverage), the `.rec` streams byte-identical. The T-H4 set differed from the T-H3 regeneration (0af3c0a) by the `[coverage]` lines at load alone,
the `.rec` streams byte-identical. The T-H3 set differed from the T-C2b regeneration
(06093ee) in the `[human]` lines alone (the record's transitions for the C1 primitives) and has the first non-empty
`.rec` baselines. The T-C2b set superseded the D3 regeneration (dd880be) by
the human's dropped per-task completion tick (T-C2b: the human one tick earlier per task it completed, a hold
one tick shorter where the human projection's end reaches it). The D3 set superseded the T-B Q7 regeneration, from
which they differ in the removed `task_committed` decisions and the executor's reload bookkeeping alone, the
world lines byte-identical. The T-B Q7 set superseded T-B2d's, which the body's completion ticks
moved (T-B Q7: the robot spends one more tick per delivery, less where a hold carried it); T-B2d's had
differed from T-B1a follow-up 2's in the `[run]` line alone, which names the strategy, and follow-up 2's had
superseded the graded-evidence sweep (`analysis/kitting/g1_graded_evidence/sweep/`, deleted 4 Oct 2026; same world-level behaviour,
hypothesis keys no longer carry the table, and the `[run]` header changed with T-A1's β commit). No
`full_reorder` baselines before T-B3. The stop-on baselines (C's, `analysis/kitting/c_separation_stop/`, and F47's) predate graded evidence and are not
regenerated; their logs were dropped in the analysis cleanup, their READMEs stay as frozen records (C's folder deleted
4 Oct 2026). Record
baselines before changing code, then diff.

### Maintained baseline sets

`analysis/kitting/tb1a_destination/` (16 logs), `analysis/kitting/tb1b_two_tables/` (4), `analysis/kitting/tb1c_realized_flip/` (8)
and `analysis/kitting/tb3_full_reorder/` (20) are the regression baselines. They are regenerated on every behaviour
change, with new md5s in a new section of each README (the commands are in those READMEs and their
`sweep.sh`). Every other folder under `analysis/kitting/` is a frozen record at the commit its README states: never
regenerated, and never edited except for a superseding note.

Evaluation fixtures, not part of the regression sweep (run them only when a task names them):
scenario_s03_06 on env_layout_06 (scenario_s03_01's end-state variant), scenario_s05_01 / scenario_s05_02 on
env_layout_07 (a foreseen human stay on the robot's route; the beside / across alternative). Script:
`analysis/kitting/tb1a_destination/sweep.sh` (the record: `analysis/kitting/f47_fixtures/`, frozen). scenario_s06_01 / scenario_s06_02 on env_layout_08 (two kitting tables, T-B's fixture: the
greedy head is not the head of the cheapest ordering; a conflict past the head). Script, baselines and the
cost argument: `analysis/kitting/tb1b_two_tables/`.

```bash
grep "^\[meta\]"        <log>   # meta-planner winner per trigger
grep "meta-cand"        <log>   # per-candidate evaluation (fields change as realization lands)
grep "^\[meta-ord\]"    <log>   # full_reorder: per possible head, the cheapest ordering that starts with it
grep "^\[meta-win\]"    <log>   # full_reorder: the winning ordering (hold before each entry, last cumulative shift, share)
grep "^\[meta-b3\]"     <log>   # B3's decision; under full_reorder with ordering= appended
grep "^\[meta-proj\]"   <log>   # human projection admitted or not, and why (G1: none(leader_no_observation), none(leader_inadequate))
grep "^\[meta-pool\]"   <log>   # completed tasks dropped from the pool
grep "^\[IR\] step="    <log>   # most_likely, confidence, lifecycle, finding, the leader's hypothesis adequacy, the members' tails
grep "^\[IR-dist\]"     <log>   # full belief distribution per tick
grep "^\[IR-complete\]" <log>   # task completion pins (a pin lasts while the terminal fact holds, T-D L4)
grep "^\[IR-reentry\]"  <log>   # a retired hypothesis live again, its terminal fact no longer holding (L4)
grep "^\[IR-assignment\]" <log>  # at load: assignment knowledge on|off and the known assigned tasks (`[IR-prior] switch=` before T-K part 1)
grep "^\[IR-context\]"   <log>   # context knowledge on: per tick the facts, the recency facts, the foreseeable tasks' levels and the prior (T-K part 1)
grep "^\[run_mesa\] timeline" <log>   # the timeline of context facts in force and its source (T-K part 1, AM40)
grep "^\[run_mesa\] options" <log>    # the options the override set off (T-F part 1, R5)
grep "^\[sep\]"         <log>   # actual robot-human distance per tick
grep "^\[hold\]"        <log>   # decided holds: start, end, planned, executed, interrupted
grep "^\[stop\]"        <log>   # separation-stop refusals (stop on), with the assessed-window label
grep "^\[rec\]"         <log .rec>   # the human executor's record (T-H2): per tick the stack (top first), the action
                                  # in hand with its occurrence and progress, and the tick's transitions; its own
                                  # file beside the run log (logs/run_<timestamp>.rec)
grep "^\[human\]"       <log>   # the record's transitions, repeated in the run log
grep "^\[coverage\]"    <log>   # at load, per script entry and observing robot: each task's coverage (T-H4)
grep "^\[scenario-coverage\]" <log>   # at load, per observing robot: the script's composition and scenario coverage
```

A behaviour-preserving change must leave these greps byte-identical, the `.rec` stream included (T-H2; the
sweep scripts copy it beside each log).

Completion is measured from the world fact (T6): the tick after the robot's last release
(`action=place micro=release`), when the terminal condition is first observable. The empty-pool line
`[meta] step=N all tasks complete` is the declared tick: the world tick is N − 2 when `no_current_task` ends the
pool, and N when a `recognition_changed` of that tick ends it (the robot's own last item changes the belief and
`update()` drops the completed task; TODO-127). Report the world tick; older reports
(D2 and before) give declared ticks. `analysis/instruments/common/sep_classes.py` reads it from a log (T6's `metrics.py` was deleted with its folder, 4 Oct
2026). Every completion
tick recorded BEFORE T-B Q7 is one tick shorter per robot delivery than the behaviour from here on (less
where a decided hold carried the tick): the body used to cancel a completion tick when a reload landed on it
(design_decisions.md, "A reload never cancels a completion tick the body states"). Do not compare a number
across that commit without it.

## Conventions and terminology

- Scenario ids are prefixed by layout number: `env_layout2` → `scenario_20`, `scenario_21`.
  SUPERSEDED (T-L, 26 Sept 2026; ruling 4 as amended, built in stages 2 and 3): serial ids, nothing encoded beyond
  order of writing, unique within the domain and artefact kind: layouts `env_layout_KK`, setups `env_setup_NN`,
  scenarios `scenario_sNN_MM` (NN the scenario's setup serial, MM a counter per setup); the Python variable equals the
  id. The setup serial in a scenario id repeats its `setup` field, an authoring convention the code does not check;
  an author who moves a scenario to another setup renames it. `docs/rename_table.md` maps the old ids.
- Adding a layout needs three edits: `domains/kitting/env_layout<N>.json`,
  `domains/kitting/scenarios.py`, and `domains/kitting/registry.py` (import and `layouts` entry).
  Fixtures are written as literals, because they are read by people; generated fixtures were tried and
  reversed (T-B1b, TODO-47 (a)). scenario_s06_04 only opens env_layout_08 in the viewer: not a fixture, nothing
  is measured from it.
  SUPERSEDED IN PART (T-L, 26 Sept 2026; rulings 1, 3 and 5, built in stages 1 and 2): the three edits and the
  registry entry. A layout (the room) and a setup (the shift) are files registered by their files
  (`domains/<d>/layouts/`, `domains/<d>/setups/`); a scenario
  declares its setup and its reference layouts and is registered by discovery at import (stage 2): a new scenario is
  one literal in its setup's module `scenarios_sNN.py`, no registry edit; a duplicate id is an error at import. The
  serial in a module's name repeats its scenarios' `setup` field — an authoring convention the code does not check,
  as the serial in a scenario id is. Fixtures stay hand-written
  literals.
- Every term has one meaning: `docs/glossary.md`. The entries below are the ones a task prompt
  leans on most; the glossary is the full list and carries the pointers.
- Framework assumptions and authoring conventions: `docs/assumptions.md` (Track 2.5). Classify a case found in a run
  before acting on it: an intended phenomenon (design it), a boundary (record it), an authoring artefact (correct the
  fixture), a prior-off artefact (never framework semantics, never a rule). Baseline human scripts end with the exit
  walk (1.1); a run's step count follows 1.3 (derived for human-script and test-bed runs; literal in the maintained
  sets until TODO-138).
- "Task pool" at the `update()` level; "candidates" exist only inside B3. A candidate is the unit
  the argmin ranges over: an individual task under `single_task`, one ordering of the pool under
  `full_reorder` (DESIGN-16, terminology). An ordering is a permutation of the pool; it is never
  called a sequence.
- Triggers: `no_current_task`; `recognition_changed` (the belief no longer points at the
  hypothesis the last decision projected, or first clears the gate on one; replaced
  `theta_crossed` in D2, which older reports and logs still name); `projection_expired` (T-D P4 / Q6: the fallback
  projection the last decision rested on has reached its end; after `recognition_changed`, through B2). Three since
  P4 (two, and only two, from D3): `task_committed` (the robot's own grasp) is not a trigger; older reports and logs
  still name it. Decision record: the projected hypothesis, and since P4 the tick at which the fallback it rested on
  expires.
- Plan names (`docs/roadmap.md`, "The plan from T-A"): T-A records (T-A1 the pipeline revision);
  T-B B3.B on two tables (B1 fixtures, B2 build, B3 evaluation); T-C the human action script (C1
  design, C2 build); T-H the human behaviour model (T-H1 to T-H4, before T-D); T-D robustness in kitting (change of mind, unmodelled behaviour, the blocked case; closed except its tail: track 3b,
  track 4, 4D); T-E the demonstration's viewer (superseded by T-V, track 1; T-E in older records means the viewer);
  T-F evaluation (Phase 5); T-G the second domain in Mesa (dock_loading; 4D and ROS left it on 30 Sept 2026); T-V
  viewer, interface and interactive simulator (track 1 the viewer, track 2 Phase 7; carried out as T-viz since 6 Oct
  2026: track 1 is T-viz stage 1, track 2 is T-viz stage 3); T-K context knowledge (part 1 crisp
  context knowledge, between T-G's stage 1 and stage 2; part 2 degrees of context facts, R5, after track 3b); T-S
  ROS/PRIEST (Phase 6); T-viz the web-ui, the name for all web-ui work (asked for 6 October 2026; stages 0 to 3, a name
  not a letter; stages 0 and 1 in V1, 2 and 3 [FW] for now; the solara-ui is the existing Solara program). Task
  prompts and reports use these names; the order is the roadmap's, not the alphabet's.
- cchat: the design chat with Hadi, where design is decided. ccode: this Claude Code session in
  the repository, which builds and checks; older reports call it Fable.
- Segment: one straight-line motion, or one stationary interval (a stationary segment), of one robot or human action in a
  projection. Entry: one task's part of a projected plan, with several segments. Stretch: the
  recognizer's unit of movement evidence. Do not mix them. "Leg" is not used: a human's movement is
  a walk.
- Head: the first task of an ordering; tail: the rest of it, lookahead only. Queue: the pool without
  the current task (`UpdateResult.queue`), unordered.
- Conflict: an entry's inherited shift lies inside one of its violating shift intervals. Crossing:
  a θ crossing only; for paths the word is violation. Robot trigger:
  `no_current_task`, the only one since D3; it bypasses B2, `recognition_changed` goes through it.
- Hold: with one entry, the shift that was chosen, δ ticks in which the robot stands still; per
  entry since T-B Q2 (`RealizedPlan.holds`), the cumulative shift of entry k
  (`RealizedPlan.cumulative_shifts`) minus that of entry k−1. Walk: an agent's
  movement, never a loop or a search in the code (the loop in `realize()` is the minimal-shift
  search). T_r: a projected plan's duration. T_h: the end of
  the human's projection. `min_separation`: the distance realization must keep between agents.