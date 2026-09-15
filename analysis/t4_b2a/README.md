# analysis/t4_b2a — B2 `b2a` against no gate (T4)

Scripts that produced the T4 numbers recorded in TODO-36, TODO-71 and TODO-77. Logs are git-ignored.

- `sweep.sh <out_dir> [run_mesa args]`: headless sweep (PYTHONHASHSEED=0, L2 step counts; `CONDS` picks fixtures).
- `cf_b3.py`: a gated run that also logs, at every B2 continue, what B3 would have selected
  (`[cf-b3]`; B3 run with logging off and the queue restored, so the run itself is unchanged).
- `compare.py <base> <variant> [cf]`: per condition, B2 verdicts, decision-sequence diff, executed
  holds, `[sep]` episodes below 50 cm (`--sep` to change), counterfactual summary and a check that the
  cf log equals the plain run.
- `stages.sh`: all of it. It checks `none` against the L2 baselines byte for byte, runs `b2a` and the
  counterfactual on s00/s10/s20/s30 × prior off/on, and writes `comparison.md`.

Regenerate from the repo root:

    analysis/t4_b2a/stages.sh

For T6: point `compare.py` at any two sweep directories, e.g. a ρ variant against `none` or `b2a`.
The byte-identity check assumes `analysis/l2_execution_lag/new/` exists (that folder's `stages.sh`).
