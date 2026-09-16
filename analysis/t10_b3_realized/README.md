# analysis/t10_b3_realized — B3 on realized cost (T10)

Scripts that produced the T10 numbers recorded in design_decisions.md ("B3 selects on realized cost"),
TODO-30, TODO-36, TODO-78 and TODO-79. Logs are git-ignored; the md5s at the end of `comparison.md`
identify the baselines.

- `sweep.sh <out_dir> [run_mesa args]`: headless sweep (PYTHONHASHSEED=0), run to completion — s00 300,
  s10 450, s20 300 (200 in L2; it did not finish there), s30 200, s40 400; `CONDS` picks fixtures. Sequential
  only: each run's log is picked up as the newest `logs/run_*.log`.
- `evaluate.py`: per condition, the three configurations' decision sequences and where they differ, every
  `all_unrealizable` event, every hold, actual separation below 50 cm (tick-sampled `dist` and continuous
  `min`) with each tick labelled inside / edge / outside the assessed window of the decision in effect, the
  distance from the L2 baselines, and the md5 table.
- `comparison.md`: its output.

Regenerate from the repo root (~1 min):

    H=analysis/t10_b3_realized
    $H/sweep.sh $H/plain_none    --cost_strategy plain    --gate_strategy none
    CONDS="s00 s10 s20 s30 s40" $H/sweep.sh $H/realized_none --cost_strategy realized --gate_strategy none
    $H/sweep.sh $H/realized_b2a  --cost_strategy realized --gate_strategy b2a
    ~/python-envs/teamrob-sp4-env/bin/python $H/evaluate.py > $H/comparison.md

The three directories are the baselines from T10 on: `realized_none/` is the default configuration
(the regression sweep, ten conditions), `plain_none/` and `realized_b2a/` the comparison conditions.
For T6: point `evaluate.py`'s `CONFIGS` at any sweep directories with the same layout.
