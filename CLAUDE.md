# CLAUDE.md: teamrob-intention-aware-planning

Simulation-agnostic robot cognitive architecture for intention-aware human-robot teaming
(Scania kitting). Pipeline per robot step:
`obs_builder → recognizer → meta_planner → planner → executor`.

What the framework is about: how the robot reads the human and plans around them. What it is not
about: what the human produces. An abandoned delivery is in scope for what it does to the robot
(retraction, `unknown`, re-planning), not for the human's output (Hadi, T-C1).

## How sessions work

- The design is made in a separate design claude chat (we call it cchat) with Hadi. Also we may call the working tool of claude-code in local repository as ccode. A task prompt states what is decided
  and what to do. You implement, check, commit, and report. Hadi reviews and pushes.
- One task per session as a rule. A fresh session starts from what is committed, not from an
  earlier session's reading of it.
- What a task states as decided is settled: do not explore alternatives to it. How to
  implement, where things go, and how to structure outputs are yours.
- If a decided design turns out to be structurally or experimentally deadlocked when you apply
  it, stop and report. Do not work around it.

## Where to look, and what to skip

Do not explore the whole tree. Start from the files a task names; widen only with a reason.

Relevant (read as needed):
- `shared/*.py`: cognitive layer (the robot's mind)
- `world/*.py`: the world's side (T-H2): the human's executor (`world/human_executor.py`, the stack machine and
  the load-time replay) and its record (`world/record.py`)
- `mesa_sim/*.py` (top level only); `mesa_sim/viz/` only for visualization or when grepping
  for readers of a field
- `domains/kitting/`: the active domain (`domains/kitting/script.py`: the call forms a scenario is written in, T-H3).
  T-L stage 2: `layouts/` and `setups/` hold the layout and setup files (setups under their final ids
  `env_setup_NN`; env_setup3 and env_setup5 merged into env_setup_01 and env_setup_03; layouts under `env_layout_KK`
  and scenarios under `scenario_sNN_MM` since stage 3, `docs/rename_table.md` maps the old ids); `scenarios/` is a package,
  one module per setup (`scenarios_sNN.py`); the registry discovers all three (`domains/discovery.py`) — no hand
  list; `env_layout6.json` and `env_layout99.json` stay at the domain root, unsplit and unregistered;
  `mesa_sim/sim_agents.py` `HumanAgent`: the human's body-side driver of the stack machine (T-H2)
- `configs/experiment.yaml`, `configs/costs.yaml`, `mesa_sim/mesa_configs.yaml`
- `docs/glossary.md`: the terms and their one meaning each. Read it every session, before the
  design record. Use its terms in the code, in the documents and in reports.
  `docs/terminology_revision.md` is its explanatory companion for glossary §7 (human behaviour, model
  coverage, the `unknown` hypothesis and "unexplained"); the glossary stays authoritative.
- Design record, in `docs/`: `design_decisions.md`, `roadmap.md`, `TODOS_AND_DEFERRED.md`;
  plus `shared/io_contracts.md` and `docs/recognizer_handback.md`
- `docs/handoffs/handoff_T-H.md`: T-H, the human behaviour model (ruled 25 Sept 2026; design_decisions.md, "T-H: the
  human behaviour model"; glossary §6 and §7). Read it in every T-H session. `docs/terminology_revision.md` §8 states
  what T-H changed in the 24 Sept terms.
- `analysis/<task>/REPORT.md`: only the reports a task names. Rows in older reports may be
  stale (earlier projection, recognizer or layouts); their findings are cited, not re-derived.

Never read, edit, or treat as a source of truth:
- Any file or directory named `my_*`, `old_*`, `archive_*` (personal notes and backups).
- `__pycache__/`, `.venv/`, `.pytest_cache/`.

Skip in the current phase; read only if the task explicitly requires it:
- `mesa_sim/mesa_fork/`: vendored Mesa 3.0; treat as an installed library. Look inside only if
  a traceback points there.
- `ros_sim/`: paused.
- `domains/dock_loading/`: deferred.
- `scripts/`: not part of the run path.
- `logs/`: except logs you produced in the current task.

## Architecture invariants (never violate)

Layering: four homes
- `shared/` is the robot's mind, the pure cognitive layer. It never imports from `world/`, `domains/`,
  `mesa_sim/` or `ros_sim/`.
- `world/` is the world's side (T-H2): simulator-agnostic, use-case-agnostic code about what the human is and
  does (the human's executor and stack machine, the executor's record). It imports `shared/` only: no body, no use case. The robot's mind never reads it.
- `domains/` holds the use cases (kitting, dock_loading): schemas, layouts, setups, scenarios.
- `mesa_sim/` and `ros_sim/` are the bodies. A body may import from `shared/`, `world/` and `domains/`;
  it drives the human's executor and executes the robot's decisions.
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
- `at(agent, object)` (executor completion) and `in_zone(agent, zone)` (recognizer context) are
  distinct predicates. Never use `at(agent, zone)`.

Decisions
- Decisions are made once, inside `shared/`. Embodiment layers execute them and may refine them
  (for example a hold), but never implement a parallel heuristic or re-decide which task runs.
- The robot knows nothing of the human's script. It never reads the human's `scheduled_tasks`
  or their order. The optional `--assignment_prior` switch (default off) gives it only the
  human's assigned-task pool, as an evaluation condition.
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
  components are ablated (T6, `analysis/t6_ablation/`); the recognizer's evidence is graded by path
  covered and the gate stays a fixed share (graded evidence, the gate ruling). The 4C queue is done.
  The plan from here is T-A to T-G ("The plan from T-A" in `docs/roadmap.md`). T-B is under way: T-B2a
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
  run file, `--run`, and the overrides, `--override`, `mesa_sim/overrides.py`). Next is T-D, on T-H's structure
  (`docs/handoffs/handoff_T-D_onward.md`, "What T-D now stands on"); T-D starts with its design in cchat. Not to be
  started unasked: T-D to T-G, i.e. robustness, the demonstration, Phase 5
  (evaluation, T-F; the randomised harness TODO-47 is part of it), 4D (detour strategy) and Phase 6
  (ROS / PRIEST execution).
- `shared/meta_planner.py`: blocks B1 (human projection), B2 (`b2a`), B3 (selection on realized
  cost) exist. `full_reorder` (B3.B) is built (`_replan_orderings()`, T-B2b / T-B2c): orderings are ranked
  on their realized cost, `realize()` running one minimal-shift search per entry (T-B Q2), and the hold sent
  is the hold before the first entry; no `full_reorder` baselines are recorded, which stays with T-B3.
  Touch it only in a T-B task, and only the step that task names.
  B2 is an evaluation factor, not a design step: `b2b` stays a stub. Change only what the task
  specifies; do not fill in unspecified block logic, flags or strategies.
- `shared/recognizer.py`: rebuilt and handed back (`docs/recognizer_handback.md`). Not under
  active change; touch it only if the task says so.
- ROS side is paused. Do not modify anything under `ros_sim/`.
- `domains/dock_loading/` is deferred. Do not modify it unless the task says so. It must still
  import without error (`run_mesa.py` imports its registry).
  SUPERSEDED FOR T-L'S STAGES ONLY (26 Sept 2026): kitting and dock_loading migrate together, so T-L's stages may
  touch `domains/dock_loading/`; it must still import and run (design_decisions.md, "Layouts, setups and scenarios",
  ruling 8).
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
# evaluation switch (default off): robot knows the observed human's assigned-task pool
PYTHONHASHSEED=0 python mesa_sim/run_mesa.py --domain kitting --layout env_layout_04 --scenario scenario_s01_06 --steps 200 --assignment_prior true
# another run file, and one override of a fact of the run's artefacts (T-L stage 4; repeatable)
PYTHONHASHSEED=0 python mesa_sim/run_mesa.py --run my_run.yaml --override layout.shelf_2.position=-300,-300
# visualization
solara run mesa_sim/run_mesa.py -- --domain kitting --layout env_layout_03 --scenario scenario_s03_01
```

Logs go to `logs/run_<timestamp>.log`. Defaults come from the run file, `configs/experiment.yaml` or the yaml
`--run` names; CLI flags override. The flags: `--domain`, `--layout`, `--scenario`, `--steps`, `--assignment_prior`
(true/false), `--strategy` (single_task | full_reorder), `--gate_strategy` (none | b2a | b2b),
`--cost_strategy` (realized | plain),
`--separation_stop` (true/false), `--run` (another run file; it replaced `--experiment` in T-L stage 4, no alias) and
`--override <path>=<value>` (repeatable). Parsing is strict: an unknown
or misspelled flag, an unknown yaml key, or a bad value stops the run. Each robot's `[run]` header
names the policy and evaluation switches the run took (strategy, gate, cost, stop, assignment prior, θ, ρ,
min_separation and β, each with its source: the body supplies both, `mesa_sim/mesa_configs.yaml`, 50 cm
and 0.01 /cm).

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
| scenario_s04_01 | env_layout_05 | foreseeable task and two AC-switch walks (retyped F47b) |

Old ids (scenario_00 on env_layout0 and so on) are mapped in `docs/rename_table.md`; the frozen records keep them.

Use the step counts of the sweep scripts (`analysis/tb1a_destination/sweep.sh` for the five and the evaluation
fixtures; before T-L stage 3, the frozen `analysis/f1_robot_responsible/sweep.sh` and `analysis/f47_fixtures/sweep.sh`,
on the old ids). The current baselines are the T-L stage 3 regeneration of the four maintained sets below, with their
`.rec` streams, named `<layout id>_<scenario id>_<run options>.log`: `analysis/tb1a_destination/sweep/` (the five plus
scenario_s03_06 / scenario_s05_01 / scenario_s05_02, both priors, stop off, `single_task`; logs local, md5s in its
README, the "T-L stage 3" section), `analysis/tb1b_two_tables/sweep/` (scenario_s06_01 / scenario_s06_02),
`analysis/tb1c_realized_flip/sweep/` and `analysis/tb3_full_reorder/sweep/` (both strategies). They differ from the
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
superseded the graded-evidence sweep (`analysis/g1_graded_evidence/sweep/`; same world-level behaviour,
hypothesis keys no longer carry the table, and the `[run]` header changed with T-A1's β commit). No
`full_reorder` baselines before T-B3. The stop-on baselines (C's, `analysis/c_separation_stop/`, and F47's) predate graded evidence and are not
regenerated; their logs were dropped in the analysis cleanup, their READMEs stay as frozen records. Record
baselines before changing code, then diff.

### Maintained baseline sets

`analysis/tb1a_destination/` (16 logs), `analysis/tb1b_two_tables/` (4), `analysis/tb1c_realized_flip/` (8)
and `analysis/tb3_full_reorder/` (20) are the regression baselines. They are regenerated on every behaviour
change, with new md5s in a new section of each README (the commands are in those READMEs and their
`sweep.sh`). Every other `analysis/` folder is a frozen record at the commit its README states: never
regenerated, and never edited except for a superseding note.

Evaluation fixtures, not part of the regression sweep (run them only when a task names them):
scenario_s03_06 on env_layout_06 (scenario_s03_01's end-state variant), scenario_s05_01 / scenario_s05_02 on
env_layout_07 (a foreseen human stay on the robot's route; the beside / across alternative). Script:
`analysis/tb1a_destination/sweep.sh` (the record: `analysis/f47_fixtures/`, frozen). scenario_s06_01 / scenario_s06_02 on env_layout_08 (two kitting tables, T-B's fixture: the
greedy head is not the head of the cheapest ordering; a conflict past the head). Script, baselines and the
cost argument: `analysis/tb1b_two_tables/`.

```bash
grep "^\[meta\]"        <log>   # meta-planner winner per trigger
grep "meta-cand"        <log>   # per-candidate evaluation (fields change as realization lands)
grep "^\[meta-ord\]"    <log>   # full_reorder: per possible head, the cheapest ordering that starts with it
grep "^\[meta-win\]"    <log>   # full_reorder: the winning ordering (hold before each entry, last cumulative shift, share)
grep "^\[meta-b3\]"     <log>   # B3's decision; under full_reorder with ordering= appended
grep "^\[meta-proj\]"   <log>   # human projection admitted or not, and why
grep "^\[meta-pool\]"   <log>   # completed tasks dropped from the pool
grep "^\[IR\] step="    <log>   # most_likely and confidence per tick
grep "^\[IR-dist\]"     <log>   # full belief distribution per tick
grep "^\[IR-complete\]" <log>   # task completion pins
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
`[meta] step=N all tasks complete` is the declared tick, N − 2. Report the world tick; older reports
(D2 and before) give declared ticks. `analysis/t6_ablation/metrics.py` reads it from a log. Every completion
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
- "Task pool" at the `update()` level; "candidates" exist only inside B3. A candidate is the unit
  the argmin ranges over: an individual task under `single_task`, one ordering of the pool under
  `full_reorder` (DESIGN-16, terminology). An ordering is a permutation of the pool; it is never
  called a sequence.
- Triggers: `no_current_task`; `recognition_changed` (the belief no longer points at the
  hypothesis the last decision projected, or first clears the gate on one; replaced
  `theta_crossed` in D2, which older reports and logs still name). Two, and only two (D3):
  `task_committed` (the robot's own grasp) is not a trigger; older reports and logs still name it.
  Decision record: the projected hypothesis, one field.
- Plan names (`docs/roadmap.md`, "The plan from T-A"): T-A records (T-A1 the pipeline revision);
  T-B B3.B on two tables (B1 fixtures, B2 build, B3 evaluation); T-C the human action script (C1
  design, C2 build); T-H the human behaviour model (T-H1 to T-H4, before T-D); T-D robustness in kitting (change of mind, unmodelled behaviour, the blocked case); T-E
  demonstration; T-F evaluation (Phase 5); T-G later (second domain in Mesa, 4D, ROS). Task prompts
  and reports use these names.
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