# analysis/c_separation_stop — the execution-time separation stop (C)

Scripts that produced the C numbers recorded in design_decisions.md ("Execution-time separation stop")
and TODO-73. Logs are git-ignored; the md5s at the end of `comparison.md` identify the runs.

- `sweep.sh <out_dir> [run_mesa args]`: headless sweep (PYTHONHASHSEED=0); s00 300, s10 450, s20 300,
  s30 200 steps; `CONDS` picks fixtures. Sequential only.
- `evaluate.py`: per condition, stop off against the F1 realized baseline (byte-identical minus the
  `[run]` line), decision sequences off and on, every `[stop]` episode with its window label, the
  acceptance check (every robot step on Mesa's sequential motion against the F1 rule; must be 0 with the
  stop on) and the simultaneous-interpolation figure alongside. Output: `comparison.md`.

Regenerate from the repo root (~1 min):

    H=analysis/c_separation_stop
    $H/sweep.sh $H/stop_off --cost_strategy realized --gate_strategy none --separation_stop false
    $H/sweep.sh $H/stop_on  --cost_strategy realized --gate_strategy none --separation_stop true
    ~/python-envs/teamrob-sp4-env/bin/python $H/evaluate.py > $H/comparison.md

`stop_off/` equals the F1 baselines apart from the header; `stop_on/` is the comparison condition, not a
baseline: with the stop on, s00, s20 and s30 do not complete (the human idles at the table after its
script ends; see the design entry).
