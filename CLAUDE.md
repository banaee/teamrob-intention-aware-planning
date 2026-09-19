# CLAUDE.md: teamrob-intention-aware-planning

Simulation-agnostic robot cognitive architecture for intention-aware human-robot teaming
(Scania kitting). Pipeline per robot step:
`obs_builder → recognizer → meta_planner → planner → executor`.

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
- `shared/*.py`: cognitive layer
- `mesa_sim/*.py` (top level only); `mesa_sim/viz/` only for visualization or when grepping
  for readers of a field
- `domains/kitting/`: the active domain
- `configs/experiment.yaml`, `configs/costs.yaml`, `mesa_sim/mesa_configs.yaml`
- Design record, in `docs/`: `design_decisions.md`, `roadmap.md`, `TODOS_AND_DEFERRED.md`;
  plus `shared/io_contracts.md` and `docs/recognizer_handback.md`
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

Layering
- `shared/` is the pure cognitive layer. It never imports from `mesa_sim/` or `ros_sim/`.
  `mesa_sim/` may import from `shared/`.
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
  Realization lives in the projection/trajectory layer; trajectory algorithms hold no policy.

## Current phase and status (affects what you may touch)

- Phase 4C: realization is built and total (T3, T4, T10, F1), the Mesa executor has the
  execution-time separation stop (C, run option, default off), wait durations come from the schema
  (TODO-32), scheduled bindings are type-checked at spawn (F47b), and the trigger set is settled
  (D2: `recognition_changed` against the decision record replaces `theta_crossed`), and the policy
  components are ablated (T6, `analysis/t6_ablation/`). The 4C queue is empty. The queue and its order
  are in `docs/roadmap.md`. Later phases, not to be started unasked: 4D (detour strategy),
  Phase 5 (evaluation), Phase 6 (ROS / PRIEST execution).
- `shared/meta_planner.py`: blocks B1 (human projection), B2 (`b2a`), B3 (selection on realized
  cost) exist. Change only what the task specifies; do not fill in unspecified block logic, flags or
  strategies.
- `shared/recognizer.py`: rebuilt and handed back (`docs/recognizer_handback.md`). Not under
  active change; touch it only if the task says so.
- ROS side is paused. Do not modify anything under `ros_sim/`.
- `domains/dock_loading/` is deferred. Do not modify it unless the task says so. It must still
  import without error (`run_mesa.py` imports its registry).
- `domains/kitting/env_layout9.json` is the old `env_layout1` with obstacles, kept for later and
  not registered.
- The code is the source of truth. Docs are maintained but can lag. Do not change code to match
  docs; report the contradiction. Edit docs only when the task says so.

## Methodology

- Scenarios are experiments for evaluating the design, not the specification for it. Never
  introduce a mechanism, threshold, margin or special case because it improves a scenario.
- Measure a premise rather than assume it. Premises stated in task prompts have been wrong more
  than once; measurement caught it. If a premise is wrong, report it.
- Findings are drawn only from the test set a task names. Few, well-understood scenarios are the
  default; broad testing with special cases is a separate, later activity.
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

Interpreter: `~/python-envs/teamrob-sp4-env/bin/python`.

```bash
# headless; --domain/--layout/--scenario are all needed for non-default scenarios
PYTHONHASHSEED=0 python mesa_sim/run_mesa.py --domain kitting --layout env_layout3 --scenario scenario_30 --steps 200
# evaluation switch (default off): robot knows the observed human's assigned-task pool
PYTHONHASHSEED=0 python mesa_sim/run_mesa.py --domain kitting --layout env_layout3 --scenario scenario_30 --steps 200 --assignment_prior true
# visualization
solara run mesa_sim/run_mesa.py -- --domain kitting --layout env_layout2 --scenario scenario_20
```

Logs go to `logs/run_<timestamp>.log`. Defaults come from `configs/experiment.yaml`; CLI flags
override. The flags: `--domain`, `--layout`, `--scenario`, `--steps`, `--assignment_prior`
(true/false), `--gate_strategy` (none | b2a | b2b), `--cost_strategy` (realized | plain),
`--separation_stop` (true/false), and `--experiment` (another yaml). Parsing is strict: an unknown
or misspelled flag, an unknown yaml key, or a bad value stops the run. Each robot's `[run]` header
names the policy and evaluation switches the run took (gate, cost, stop, assignment prior, θ, ρ,
min_separation).

## Regression checking

The simulator is deterministic given a fixed hash seed. Prefix every run with `PYTHONHASHSEED=0`
until TODO-42 is fixed.

Regression sweep: five fixtures, each with assignment prior off and on, each run to completion:

| fixture | layout | note |
|---|---|---|
| scenario_00 | env_layout0 | crossing and table convergence |
| scenario_10 | env_layout1 | coffee break and AC activation; needs about 450 steps |
| scenario_20 | env_layout2 | table convergence; does not finish in 200 steps |
| scenario_30 | env_layout3 | mirror-symmetric crossing |
| scenario_40 | env_layout4 | foreseeable task and two AC-switch legs (retyped F47b) |

Use the step counts of the sweep scripts (`analysis/f1_robot_responsible/sweep.sh` for s00–s40,
`analysis/f47_fixtures/sweep.sh` for the evaluation fixtures). The current baselines are the
graded-evidence sweep, `analysis/g1_graded_evidence/sweep/` (the five plus s50 / s70 / s71, both
priors, stop off; logs local, md5s in its README), which superseded D2's
`analysis/d2_recognition_trigger/`. The stop-on baselines (C's `stop_on/`, F47's) are pre-grade. Record
baselines before changing code, then diff.

Evaluation fixtures, not part of the regression sweep (run them only when a task names them):
scenario_50 on env_layout5 (scenario_20's end-state variant), scenario_70 / scenario_71 on env_layout7
(a foreseen human stay on the robot's route; the beside / across alternative). Scripts and baselines:
`analysis/f47_fixtures/`.

```bash
grep "^\[meta\]"        <log>   # meta-planner winner per trigger
grep "meta-cand"        <log>   # per-candidate evaluation (fields change as realization lands)
grep "^\[meta-proj\]"   <log>   # human projection admitted or not, and why
grep "^\[meta-pool\]"   <log>   # completed tasks dropped from the pool
grep "^\[IR\] step="    <log>   # most_likely and confidence per tick
grep "^\[IR-dist\]"     <log>   # full belief distribution per tick
grep "^\[IR-complete\]" <log>   # task completion pins
grep "^\[sep\]"         <log>   # actual robot-human distance per tick
grep "^\[hold\]"        <log>   # decided holds: start, end, planned, executed, interrupted
grep "^\[stop\]"        <log>   # separation-stop refusals (stop on), with the assessed-window label
```

A behaviour-preserving change must leave these greps byte-identical.

Completion is measured from the world fact (T6): the tick after the robot's last release
(`action=place micro=release`), when the terminal condition is first observable. The empty-pool line
`[meta] step=N all tasks complete` is the declared tick, N − 2. Report the world tick; older reports
(D2 and before) give declared ticks. `analysis/t6_ablation/metrics.py` reads it from a log.

## Conventions and terminology

- Scenario ids are prefixed by layout number: `env_layout2` → `scenario_20`, `scenario_21`.
- Adding a layout needs three edits: `domains/kitting/env_layout<N>.json`,
  `domains/kitting/scenarios.py`, and `domains/kitting/registry.py` (import and `layouts` entry).
- "Task pool" at the `update()` level; "candidates" exist only inside B3. A candidate is an
  individual task, never an ordering.
- Triggers: `no_current_task`; `recognition_changed` (the belief no longer points at the
  hypothesis the last decision projected, or first clears the gate on one; replaced
  `theta_crossed` in D2, which older reports and logs still name); `task_committed` (the robot's
  own grasp, not the human's commitment). Decision record: the projected hypothesis, one field.
- cchat: the design chat with Hadi, where design is decided. ccode: this Claude Code session in
  the repository, which builds and checks; older reports call it Fable.
- Segment: one straight stretch of one robot or human action in a projection. Leg: the
  recognizer's term for a human walk. Do not mix the two.
- Hold: the robot stands still for δ ticks. T_r: a projected plan's duration. T_h: the end of
  the human's projection. `min_separation`: the distance realization must keep between agents.