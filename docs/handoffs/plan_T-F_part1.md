# T-F part 1: the plan of the build of the conditions human-unaware and intention-unaware

Written by ccode, 5 October 2026 (BUILD DISCIPLINE, step 1: plan only, no code). Status: PROPOSED, not approved.
The rulings and their reasons: design_decisions.md and design_records.md, "T-F part 1: the conditions human-unaware
and intention-unaware" (R1 to R10); terms: glossary §9. Every build session reads this file first.

Two stages, a pause between them: 1 the two run options, the override and its message, the log, the tests; 2 the
planning test-bed's instruments (R9). The measurement (R10) is a separate step, not planned here.

---

## 1. Facts from the code (the plan rests on these; from ccode's verification of 5 October 2026)

- F1. The gate has two callers in `shared/`: `evaluate_triggers` (the entering side of `recognition_changed`, asked only
  while no hypothesis is recorded) and `update_human_projection` (admission). No other decision reads the belief;
  `planner.plan()` takes it and reads nothing of it.
- F2. Admission asks the gate first, then `none(no_human)`, then `none(unprojectable)`. A robot with no observed human
  therefore prints `none(below_theta)` (the dummy belief, confidence 0).
- F3. A robot's observed human is the scenario's `observes[0]` (`SimModel._spawn_agents`); with none, the recognizer is
  never called, the meta-planner gets the dummy belief, no fallback is built, and only `no_current_task` fires. Its
  per-tick positions equal the robot-alone reference run's (scenario_s10_02, scenario_s06_02).
- F4. `[sep]` is logged by `run_mesa.py` for every robot–human pair, whatever `observes` states.
- F5. `SimModel` takes `assignment_knowledge` and `context_knowledge` with no default (AM51); it is built by
  `run_mesa.py` (headless and viewer, through `resolve_model_params`), `mesa_sim/list_scenarios.py`, 17 test files,
  `analysis/instruments/mpb/{actual,reference}.py`, `analysis/instruments/irb/{actual,trajectory}.py`, and two frozen
  scripts (`analysis/kitting/tb1b_two_tables/permutation_costs.py`, `analysis/kitting/tb1c_realized_flip/check.py`).
- F6. The `[coverage]` and `[scenario-coverage]` lines are written per robot whose scenario `observes` the human.

## 2. Stage 1: the options, the override, the log, the tests

What changes, where:
- `mesa_sim/run_mesa.py`: `human_aware` and `intention_aware` in `BOOL_OPTIONS`; `--human_aware`, `--intention_aware`
  (true/false); `resolve_model_params` passes both as stated (fallback `True`). The override is not applied here.
- `configs/experiment.yaml`: the two keys, `true`, with one comment each; the stale comment on `assignment_knowledge`
  ("an assigned task has commitment warrant") corrected.
- `mesa_sim/sim_model.py`: `SimModel` takes `human_aware` and `intention_aware` with no default (AM51's form). The
  override (R5) is applied here, its one home, so the headless run, the viewer and the instruments get the same
  effective values: `human_aware` off sets `intention_aware`, both knowledge options and `separation_stop` off;
  `intention_aware` off sets both knowledge options off. One message line after the timeline line, naming only the
  options whose stated or default value was on, for example
  `[run_mesa] options human_aware=off sets off: intention_aware assignment_knowledge context_knowledge`;
  no line when nothing was set off. The effective values are the model's attributes, read by everything after.
  With `human_aware` off the robot is given no observed agent (Q1) and no observed assigned tasks.
- `mesa_sim/sim_agents.py`: the `[run]` header gains `human_aware=on|off intention_aware=on|off` before
  `assignment_knowledge` (effective values); `MetaPlanner(..., intention_aware=...)`.
- `shared/meta_planner.py` (domain-agnostic; R6, R7):
  - `GateOutcome.INTENTION_OFF = "none(intention_off)"`, asked first in `_clears_gate` when the meta-planner was built
    with `intention_aware=False`; both callers get it, so `recognition_changed` cannot enter and admission refuses
    with that reason, then builds the fallback as today.
  - admission asks `none(no_human)` before the gate (R7; Q2 on its scope).
  - the constructor's `intention_aware: bool = True` (the meta-planner's other options have defaults); the docstrings
    of `GateOutcome`, `_clears_gate`, `update_human_projection`; `evaluate_triggers`' "Two real triggers" corrected.
- Tests, `tests/test_tf1_conditions.py`: the override for every combination of the four options (effective values, the
  message); `_clears_gate` returns `INTENTION_OFF` on a belief that clears; the entering side does not fire; admission
  logs `fallback refused=none(intention_off)` and sets the fallback's expiry; a meta-planner with no human logs
  `none(no_human)`; one short headless run per condition on scenario_s10_02 (human-unaware: positions equal the
  reference run's, `[sep]` present, no `[IR]`, triggers `no_current_task` only; intention-unaware: `[IR]` on every
  tick, no `recognition_changed`, every `[meta-proj]` refused with `none(intention_off)`). The 17 test files and the
  other `SimModel` call sites of F5 pass `human_aware=True, intention_aware=True` (the frozen scripts as at AM51).
- Records at the stage's end: io_contracts.md §2.2 (the constructor, `INTENTION_OFF`, the admission order),
  recognizer_handback.md (the list of refusals), glossary §9 and design_records.md BUILT lines, CLAUDE.md (the flags,
  the message's grep).

What does not change: the recognizer, the belief and its outputs; the gate's rule in the intention-aware run; the
trigger rule; the decision record; the fallback projection; the candidates, realization and cost; B2; the planner;
the executor (it gets `separation_stop` off as any run with the stop off); `world/`; `domains/`; every layout, setup,
scenario and run file but `configs/experiment.yaml`.

How the existing runs are shown identical with both options on:
- B0 at HEAD before the stage, outside the repository: the four maintained sets (48 logs with `.rec`), the kitting MPB
  set through `run.sh` under both strategies and the prior-off appendix, the IRB's s08 and s09 sets (17), dock_loading's
  six milestone runs, and pytest.
- After the stage, the same: every log and `.rec` byte-identical after removing ` human_aware=on intention_aware=on`
  from the `[run]` line; every instrument output identical. Named exception if Q2 is answered "every run": the
  `[meta-proj]` lines of the robot-alone reference logs (`none(below_theta)` → `none(no_human)`), no other line.
- Not rerun: round 1, steps 4 to 5e (their committed outputs stand; the change with both options on is the header
  only, which the maintained sets and the MPB set check).
- The two conditions, beyond the tests: scenario_s10_02 and scenario_s06_02 run in both, headless, outside the
  repository, read against the verification's runs.

## 3. Stage 2: the instruments (R9)

- `analysis/instruments/mpb/run.sh`: a `--condition human_unaware|intention_unaware` argument passing the two options
  to `run_mesa.py` and `actual.py`; outputs in `<scenario>/<condition>_<strategy>/` (the intention-aware folders keep
  their names).
- `actual.py`: builds `SimModel` with the options; under human-unaware records no recognition (the belief is None).
- `mpb_oracle.py`: intention-unaware: the gate column `none(intention_off)` on every tick, no admitted projection, the
  fallback a decision on the tick would rest on (mpblib, as today), the recognition columns as R9 states (but see
  flag 1); human-unaware: no recognition, no gate, no projection.
- `chain.py`: unchanged rules (with the gate never clearing, C3 never enters); human-unaware: `no_current_task` only.
- `compare.py`: human-unaware also compares hold 0 at every decision and the robot's positions with `reference.py`'s
  (run for every scenario whose script is independent, not only the controls).
- `measures.py` and each domain's `properties.py`: the measures for every run; the declared properties skipped in both
  conditions. `plot.py`: the new gate value; `plot_ir.py` not drawn under human-unaware.
- `tests/instruments/test_mpb_instrument.py`: one case per condition.
- Check: the kitting MPB set (16) in both conditions, `single_task`: 0 disagreements expected; every intention-aware
  output identical to stage 1's. Not extended: the alteration test (MPB-4), the IRB.

## 4. Open points for Hadi (questions, not choices made)

- Q1. How `human_aware` off reaches the mind, `observes` being a scenario fact. Proposed: the loader reads the scenario
  as written and hands the robot no observed agent; the scenario is not changed and no override path is added. Or
  another form?
- Q2. R7 needs admission to ask `none(no_human)` before the gate. For every run (today it only changes the robot-alone
  reference logs' `[meta-proj]` line) or only under `human_aware` off?
- Q3. Human-unaware: are the `[coverage]` and `[scenario-coverage]` lines dropped (the robot observes no one) or kept
  (they describe the scenario against the robot's task model and no run reads them)?
- Q4. R7's scope: does "no label states a setting not in effect" cover the header's constants (θ under
  intention-unaware; θ, α, β under human-unaware), or only the run options?
- Q5. dock_loading's six scripts that depend on the robot (M1, M2, M4 on env_layout_03 and _04): in both conditions no
  oracle and measures only, as MPB-DL3 does for them today? The human's run changes with the robot's, so the
  human-unaware reference-position check does not apply to them.
- Q6. Under human-unaware, where the robot's and the human's objects are not disjoint, the robot's positions may
  differ from the reference run's by R4's limit (flag 2). Is such a case a disagreement of the oracle, or a recorded
  finding of R4's limit?
- Q7. Flag 1 (below): the recognition columns of the intention-unaware run under R5.

## 5. Flags on the rulings (ccode's review; Hadi rules)

1. R5 against R6 (third item) and R9 (first item). `intention_aware` off sets `assignment_knowledge` off, so the
   recognizer that runs and logs under intention-unaware is the assignment-knowledge-off recognizer: its log shows what
   an intention-aware run with both knowledge options off would admit, not the default run's (R6's reason). And MPB-6
   rules no exact oracle comparison with assignment knowledge off (every hypothesis admissible, the robot's acts change
   the human-side hypotheses, MPB-3's pre-run independence fails), so R9's "the recognition columns as today" cannot be
   derived for these runs; `docs/assumptions.md` 1.4 classes the configuration a diagnostic. R5's premise for decisions
   holds.
2. R4's "no component of the mind uses them" holds where the robot's and the human's objects are disjoint (MPB-3).
   In general the mind reads the human's facts: `shared/target_resolution.object_position` resolves an object the
   human carries to the human's position, and the pool's completion and the planner's method applicability read world
   facts the human's actions change. R9's position equality inherits this condition.
3. R5 sets the separation stop off, a check of the body (the executor), while R4 calls human-unaware a condition of the
   mind. The reason holds; R4's sentence then reads "the mind, and the body's stop".
4. R2 says the meta-planner "receives no human", R4 that the world state it receives keeps the human's facts. Read
   together: no observed human (no observation, no observed agent), not no human in the world state.
