# analysis/f47_fixtures — evaluation fixtures for D2 (F47, F47b)

Scripts and records behind TODO-47 (d)/(e), TODO-49 and the design entry "Scheduled bindings are typed; a stay
the projection carries is absorbed by realization". Logs are git-ignored; the md5s below identify the runs.

- `typecheck.py`: applies `shared.types.check_task_bindings` (F47b: every scheduled and assigned task's bound
  objects must exist in the layout with the schema's `parameter_types`) to every registered kitting fixture and
  to the retired scenario_60/61. No simulator run.
- `sweep.sh <out_dir> [run_mesa args]`: headless runs (PYTHONHASHSEED=0) of the evaluation fixtures; `CONDS`
  picks among s40 (400 steps), s50, s70, s71 (300); prior off and on. Sequential.
- `verify.py <log>...`: the F47 conditions from a stop-on log — every `[stop]` episode with the decision in
  effect, its candidates (the alternatives), whether the blocked task was the robot's last, the human's stand
  ticks, completion.
- `control_run.py`: the F47 control (record only; see its docstring): the retired env_layout6 with the
  waypoint retyped as a coffee machine, so the stay is MODELLED. No stop fired: B3 switched (beside) or held
  (across) at the crossing.
- `retired_scenarios_60_61.py`: the F47 fixtures, unregistered. They bound `coffee_break` to a waypoint — a
  coffee break in a world with no coffee machine — which ran only because scheduled bindings were not
  type-checked; `typecheck.py` refuses them. `domains/kitting/env_layout6.json` stays as their layout,
  unregistered.
- `blocked.md`: the R2 measures (`analysis/c_separation_stop/blocked.py`) over `stop_off/` and `stop_on/`.

Regenerate from the repo root (~2 min):

    H=analysis/f47_fixtures
    ~/python-envs/teamrob-sp4-env/bin/python $H/typecheck.py
    CONDS="s40" $H/sweep.sh $H/baselines_s40 --cost_strategy realized --gate_strategy none --separation_stop false
    $H/sweep.sh $H/stop_off --cost_strategy realized --gate_strategy none --separation_stop false
    $H/sweep.sh $H/stop_on  --cost_strategy realized --gate_strategy none --separation_stop true
    ~/python-envs/teamrob-sp4-env/bin/python analysis/c_separation_stop/blocked.py $H/stop_off $H/stop_on > $H/blocked.md

## Type check (F47b)

Registered at HEAD: s00, s10, s20, s30, s40, s50, s70, s71 all PASS. Before F47b, scenario_40 bound
`ac_activation` to the waypoints wander_0 / wander_1 and scenario_50 bound `coffee_break` to the waypoint
rest_0: both FAIL the check as they were. Fixed by retyping the targets at the same coordinates: env_layout4's
wander_0 / wander_1 are now `ac_switch_1` / `ac_switch_2` (type `ac_switch`), env_layout5's rest_0 is
`coffee_machine_0` (type `coffee_machine`). scenario_60 / 61: FAIL, retired.

## scenario_40 baseline, regenerated (`baselines_s40/`, stop off)

The retyping changes the hypothesis space (`ac_activation` has three hypotheses instead of one) and so the IR
lines from tick 0. Against the pre-F47b logs (HEAD after R2): the robot's task order (item_4, item_7, item_5)
and completion (378) are unchanged in both priors; the first crossing moves 19 → 21; the coffee crossing moves
from 143 (off) / 135 (on) to 153 (both; peak 0.915 / 0.917 instead of 0.982 / 0.984); the two AC-switch walks are now
recognised (205: ac_switch_1 0.784 / 0.878; 221: ac_switch_2 0.772 / 0.853) and pinned complete at 207 and
228; an item_6 crossing appears at 266 (off) / 250 (on). These supersede the s40 rows of
`analysis/f1_robot_responsible/comparison.md` and the s40 figures in `docs/recognizer_handback.md`.

## md5

`stop_on/` rows: the graded-evidence regeneration (September 2026; pre-grade md5s in git history at 5b9cca0).
Against the post-D2 stop-on reference (T6's `core/gnone_crealized_son`) the grade leaves the `[stop]` grep and
every completion tick unchanged on s50 / s70 / s71; `[sep]` moves in s50_on (8) and s70_on (60), the decision
ticks as in `analysis/g1_graded_evidence/summary.md`. `baselines_s40/` and `stop_off/` are pre-grade and
superseded by `analysis/g1_graded_evidence/sweep/`.

| log | md5 |
|---|---|
| baselines_s40/s40_off | a89adcf93b96477c5940bfd09ec65d25 |
| baselines_s40/s40_on | ef4c1f0dd9505a2b8f495f5235d2dc5a |
| stop_off/s50_off | c3a89c8f37f9342629fa05d7a3688c07 |
| stop_off/s50_on | 54fedac7a773939c5aaa5748781be403 |
| stop_off/s70_off | ee1d4b375ae98483c917dcf5196d9c65 |
| stop_off/s70_on | 748e0a1c09080892334e0499b1ed5cf9 |
| stop_off/s71_off | 9d6741b0ec585403b4b62fc1a55d2eb5 |
| stop_off/s71_on | 33c5251231d2f7a34cc3c85ad9b2c3cc |
| stop_on/s50_off | 04d77ac7fe0001316338d6fbefb378b8 |
| stop_on/s50_on | de2a0b5c90b8b2f15d41864345a0e0f4 |
| stop_on/s70_off | dfb486bfe6c034495c9f6d37ef9879f6 |
| stop_on/s70_on | a55233abd6874d807383a419e2ad630b |
| stop_on/s71_off | 23a2c4fe1fd8e46818e723d160f56dd9 |
| stop_on/s71_on | 30df2f20cc631e3f3710e19b417edf7f |
