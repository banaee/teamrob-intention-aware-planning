#!/usr/bin/env bash
# sweep.sh <out_dir> [run_mesa args...] — headless runs of the F47/F47b evaluation fixtures, PYTHONHASHSEED=0,
# each log copied to <out_dir>/<cond>.log (git-ignored). Conditions: $CONDS (default s50 s70 s71) × assignment
# prior off/on: s40 400 steps (the regression fixture, regenerated in F47b), s50 300, s70 300, s71 300. Extra
# args go to run_mesa.py, e.g. --separation_stop true. Sequential: each run's log is picked up as the newest
# logs/run_*.log. Run from the repo root.
set -e
OUT=$1; shift; PY=~/python-envs/teamrob-sp4-env/bin/python; mkdir -p "$OUT"
CONDS=${CONDS:-"s50 s70 s71"}
declare -A LAY=([s40]="env_layout4 scenario_40 400" [s50]="env_layout5 scenario_50 300"
                [s70]="env_layout7 scenario_70 300" [s71]="env_layout7 scenario_71 300")
for c in $CONDS; do
  read -r lay sc st <<< "${LAY[$c]}"
  for p in false true; do
    tag=${c}_$([ $p = true ] && echo on || echo off)
    PYTHONHASHSEED=0 $PY mesa_sim/run_mesa.py --domain kitting --layout "$lay" --scenario "$sc" \
      --steps "$st" --assignment_prior $p "$@" > /dev/null 2>&1 || echo "$tag: exit $?"
    cp "$(ls -t logs/run_*.log | head -1)" "$OUT/$tag.log"
  done
done
