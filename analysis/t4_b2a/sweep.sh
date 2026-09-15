#!/usr/bin/env bash
# sweep.sh <out_dir> [run_mesa args...] — headless runs, PYTHONHASHSEED=0, each log copied to
# <out_dir>/<cond>.log (git-ignored). Conditions: $CONDS (default all five fixtures) × assignment
# prior off/on, at the L2 baselines' step counts (s00 300, s10 450, s20 200, s30 200, s40 400).
# Extra args go to run_mesa.py, e.g. --gate_strategy b2a. Run from the repo root; sequential, since
# each run's log is picked up as the newest logs/run_*.log.
set -e
OUT=$1; shift; PY=~/python-envs/teamrob-sp4-env/bin/python; mkdir -p "$OUT"
CONDS=${CONDS:-"s00 s10 s20 s30 s40"}
declare -A LAY=([s00]="env_layout0 scenario_00 300" [s10]="env_layout1 scenario_10 450"
                [s20]="env_layout2 scenario_20 200" [s30]="env_layout3 scenario_30 200"
                [s40]="env_layout4 scenario_40 400")
for c in $CONDS; do
  read -r lay sc st <<< "${LAY[$c]}"
  for p in false true; do
    tag=${c}_$([ $p = true ] && echo on || echo off)
    PYTHONHASHSEED=0 $PY mesa_sim/run_mesa.py --domain kitting --layout "$lay" --scenario "$sc" \
      --steps "$st" --assignment_prior $p "$@" > /dev/null 2>&1 || echo "$tag: exit $?"
    cp "$(ls -t logs/run_*.log | head -1)" "$OUT/$tag.log"
  done
done
