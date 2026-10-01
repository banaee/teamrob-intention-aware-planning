#!/usr/bin/env bash
# sweep.sh <out_dir> [run_mesa args...] — headless runs of every T6 fixture through run.py (PYTHONHASHSEED=0),
# each log copied to <out_dir>/<cond>_<off|on>.log (git-ignored). Conditions: $CONDS (default all eight)
# × assignment prior off/on, at the established step counts: s00 300, s10 450, s20 300, s30 200, s40 400,
# s50 300, s70 300, s71 300 (the caps for the stop-on runs that do not complete). T6_RHO / T6_SEP_CM pass
# through the environment to run.py. Sequential: each run's log is picked up as the newest logs/run_*.log.
# Run from the repo root.
set -e
OUT=$1; shift; PY=~/python-envs/teamrob-sp4-env/bin/python; mkdir -p "$OUT"
CONDS=${CONDS:-"s00 s10 s20 s30 s40 s50 s70 s71"}
declare -A LAY=([s00]="env_layout0 scenario_00 300" [s10]="env_layout1 scenario_10 450"
                [s20]="env_layout2 scenario_20 300" [s30]="env_layout3 scenario_30 200"
                [s40]="env_layout4 scenario_40 400" [s50]="env_layout5 scenario_50 300"
                [s70]="env_layout7 scenario_70 300" [s71]="env_layout7 scenario_71 300")
for c in $CONDS; do
  read -r lay sc st <<< "${LAY[$c]}"
  for p in false true; do
    tag=${c}_$([ $p = true ] && echo on || echo off)
    PYTHONHASHSEED=0 $PY analysis/t6_ablation/run.py --domain kitting --layout "$lay" --scenario "$sc" \
      --steps "$st" --assignment_prior $p "$@" > /dev/null 2>&1 || echo "$tag: exit $?"
    cp "$(ls -t logs/run_*.log | head -1)" "$OUT/$tag.log"
  done
done
