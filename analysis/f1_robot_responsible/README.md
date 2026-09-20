# analysis/f1_robot_responsible — robot-responsible separation (F1)

Scripts that produced the F1 numbers recorded in design_decisions.md ("Robot-responsible separation"),
TODO-30, TODO-73 and TODO-77. Logs are git-ignored; the md5s at the end of `comparison.md` identify the
baselines.

- `sweep.sh <out_dir> [run_mesa args]`: headless sweep (PYTHONHASHSEED=0), run to completion — s00 300,
  s10 450, s20 300, s30 200, s40 400; `CONDS` picks fixtures. Sequential only: each run's log is picked up
  as the newest `logs/run_*.log`.
- `validate.py`: runs the eight conditions in process, records every B3 `realize()` call, and checks each
  realized plan's segments independently against rules (a) and (b) by dense sampling, checks δ's minimality,
  and runs the T10 realizer (extracted from commit 08b1167 with `git show` into `_t10_realizer/`,
  git-ignored) on the same inputs. Output: `validation.md`.
- `evaluate.py`: per condition, the three configurations' decision sequences and where they differ, every
  hold, actual separation below 50 cm with each tick labelled by the F1 rule at execution (viol | stand |
  recede) and against the assessed window of the decision in effect, the distance from the T10 baselines,
  and the md5 table. Output: `comparison.md`.

Regenerate from the repo root (~2 min):

    H=analysis/f1_robot_responsible
    $H/sweep.sh $H/plain_none    --cost_strategy plain    --gate_strategy none
    CONDS="s00 s10 s20 s30 s40" $H/sweep.sh $H/realized_none --cost_strategy realized --gate_strategy none
    $H/sweep.sh $H/realized_b2a  --cost_strategy realized --gate_strategy b2a
    PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python $H/validate.py > $H/validation.md
    ~/python-envs/teamrob-sp4-env/bin/python $H/evaluate.py > $H/comparison.md

The three directories are the baselines from F1 on: `realized_none/` is the default configuration (the
regression sweep, ten conditions), `plain_none/` and `realized_b2a/` the comparison conditions. All are
run with the separation stop off and contain walk-throughs (the tail "viol" ticks in `comparison.md`):
they are decision baselines and support no safety claim (R2). Since TODO-32 (R2) the s10 and s40 logs
differ from these at HEAD in `[meta-b3] T_h` and `[meta-cand] share` at the coffee_break triggers only
(s10 step 123; s40 steps 135/143 and 147); decisions, holds and every other grep are unchanged. Since F47b
(scenario_40 retyped) the s40 logs and md5s here are superseded altogether: the current s40 baseline is
`analysis/f47_fixtures/baselines_s40/` (same task order and completion, different recognition ticks).
