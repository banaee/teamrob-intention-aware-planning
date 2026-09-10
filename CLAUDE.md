# CLAUDE.md — teamrob-intention-aware-planning

Simulation-agnostic robot cognitive architecture for intention-aware human-robot teaming
(Scania kitting). Pipeline per robot step:
`obs_builder → recognizer → meta_planner → planner → executor`.

## Where to look — and what to skip

Do not explore the whole tree. Start from the files a task names; widen only with a reason.

**Relevant (read as needed):**
- `shared/*.py` — cognitive layer
- `mesa_sim/*.py` (top level only), `mesa_sim/viz/` only for visualization or when grepping
  for readers of a field
- `domains/kitting/` — the active domain
- `configs/experiment.yaml`, `configs/costs.yaml`, `mesa_sim/mesa_configs.yaml`
- Reference only (may be stale): `docs/design_decisions.md`, `docs/roadmap.md`,
  `docs/TODOS_AND_DEFERRED.md`, `shared/io_contracts.md`. The canonical docs are in `docs/`.

**Never — read, edit, or treat as a source of truth:**
- Any file or directory named `my_*`, `old_*`, `archive_*` — personal notes and backups
  (e.g. `docs/my_*.md`, `configs/old_*.yaml`, root `my_*.txt`).
- `__pycache__/`, `.venv/`, `.pytest_cache/`.

**Skip in the current phase — read only if the task explicitly requires it:**
- `mesa_sim/mesa_fork/` — vendored Mesa 3.0; treat as an installed library. Look inside only
  if a traceback points there.
- `ros_sim/` — paused.
- `domains/dock_loading/` — deferred.
- `scripts/` — not part of the run path.
- `logs/` — except logs you produced in the current task.

## Architecture invariants (never violate)

- `shared/` is the pure cognitive layer. It never imports from `mesa_sim/` or `ros_sim/`.
  `mesa_sim/` may import from `shared/`.
- No string parsing in `shared/`. Bindings are typed `Var` / `Const`.
- No domain-specific strings in `shared/` (e.g. never hardcode `"?item"`, `"kitting_table"`).
  Domain facts come from schemas (`TaskSchema.parameter_types`, `ActionSchema` fields).
- `at(agent, object)` (executor completion) and `in_zone(agent, zone)` (IR context) are
  distinct predicates. Never use `at(agent, zone)`.
- `WorldState` is ephemeral: rebuilt every tick, never stored or mutated.
- Decisions are made once, inside `shared/`. Embodiment layers execute them; they never
  implement a parallel heuristic.

## Current project status (affects what you may touch)

- **ROS side is paused.** Do not modify anything under `ros_sim/`.
- **dock_loading domain is deferred.** Do not modify `domains/dock_loading/` unless the task
  explicitly says so. It must still *import* without error (run_mesa.py imports its registry).
- **`shared/meta_planner.py` is under active design elsewhere** (B2/B3 blocks). Do not modify
  it unless the task explicitly says so.
- **Docs lag the code.** `design_decisions.md`, `roadmap.md`, `TODOS_AND_DEFERRED.md`,
  `io_contracts.md` may be stale. The code is the source of truth. Do not "fix" code to
  match docs. Do not edit docs unless the task says so.

## Workflow rules

1. **Plan before editing.** For any multi-file task: read the relevant files, then present a
   plan (files, what changes, why) and wait for approval.
2. **One file at a time.** Show the diff for each file and wait for "ok" before the next.
3. **Surgical changes only.** Match existing style. No unrelated refactors, renames, or
   reformatting. No speculative abstractions or configurability.
4. **Ask, don't guess.** If the code doesn't match what the task describes, or a decision is
   ambiguous, stop and ask.
5. **Flag, don't fix.** Issues noticed outside the task scope: list them at the end, don't
   change them.
6. **Git:** work on a feature branch; commit in logical groups with clear messages; never
   push; never rewrite history.
7. Be concise in reports: what changed, where, verification result.

## Running

```bash
# headless; --domain/--layout/--scenario are all needed for non-default scenarios
python mesa_sim/run_mesa.py --domain kitting --layout env_layout0 --scenario scenario_00 --steps 200
python mesa_sim/run_mesa.py --domain kitting --layout env_layout2 --scenario scenario_20 --steps 200
# visualization
solara run mesa_sim/run_mesa.py -- --domain kitting --layout env_layout2 --scenario scenario_20
```

Logs go to `logs/run_<timestamp>.log`. Defaults come from `configs/experiment.yaml`;
CLI flags override.

## Regression checking

The simulator is deterministic **given a fixed hash seed**. Prefix every regression run with
`PYTHONHASHSEED=0` until TODO-42 is fixed — without it, hypothesis order varies per process
and `[IR-dist]` tie order flaps between runs of identical code (scenario_10 shows this;
scenario_00 and scenario_20 do not). Record baseline logs *before* changing code, then diff.

```bash
PYTHONHASHSEED=0 python mesa_sim/run_mesa.py --domain kitting --layout env_layout1 --scenario scenario_10 --steps 200

grep "^\[meta\]"        <log>   # meta-planner winner per trigger
grep "meta-cand"        <log>   # per-candidate cost / feasible / min_dist
grep "^\[IR\] step="    <log>   # most_likely + confidence per tick
grep "^\[IR-dist\]"     <log>   # full belief distribution per tick
```

A behaviour-preserving change must leave these greps byte-identical.

## Conventions

- Scenario ids are prefixed by layout number: `env_layout2` → `scenario_20`, `scenario_21`.
- Adding a layout needs three edits: `domains/kitting/env_layout<N>.json`,
  `domains/kitting/scenarios.py`, and `domains/kitting/registry.py` (import + `layouts` entry).
- Terminology: "task pool" at the `update()` level; "candidates" exist only inside B3.
