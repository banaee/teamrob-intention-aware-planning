#!/usr/bin/env bash
# supp_sweep.sh <out_dir> — the supplementary runs of session 1.4, section H (the wrong table): scenario_s06_06 on
# env_layout_08 and scenario_s07_03 on env_layout_09, with the tb1a sweep's options (gate none, cost realized, stop off,
# single_task), assignment prior off and on, PYTHONHASHSEED=0, 300 steps. Not baselines. Run from the repo root (HEAD),
# or from a worktree at 84309e9 for the pre-build logs. Logs git-ignored; md5s in REPORT.md.
set -e
OUT=$1; shift; PY=~/python-envs/ir-nomesa-env/bin/python; mkdir -p "$OUT"
RUNS="env_layout_08 scenario_s06_06 300
env_layout_09 scenario_s07_03 300"
while read -r lay sc st; do
  for p in false true; do
    tag=${lay}_${sc}_$([ $p = true ] && echo on || echo off)
    PYTHONHASHSEED=0 $PY mesa_sim/run_mesa.py --domain kitting --layout "$lay" --scenario "$sc" --steps "$st" \
      --cost_strategy realized --gate_strategy none --separation_stop false \
      --assignment_prior $p < /dev/null > /dev/null 2>&1 || echo "$tag: exit $?"
    cp "$(ls -t logs/run_*.log | head -1)" "$OUT/$tag.log"
    cp "$(ls -t logs/run_*.rec | head -1)" "$OUT/$tag.rec"
  done
done <<< "$RUNS"
