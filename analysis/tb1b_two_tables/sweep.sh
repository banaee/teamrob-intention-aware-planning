#!/usr/bin/env bash
# sweep.sh <out_dir> [run_mesa args...] — headless runs of the two-table fixture (T-B1b), PYTHONHASHSEED=0, each
# log copied to <out_dir>/<cond>.log (git-ignored). Conditions: $CONDS (default s80 s81) × assignment prior
# off/on, 340 steps each (both complete by 265). Extra args go to run_mesa.py. Sequential: each run's log is
# picked up as the newest logs/run_*.log. Run from the repo root.
set -e
OUT=$1; shift; PY=~/python-envs/teamrob-sp4-env/bin/python; mkdir -p "$OUT"
CONDS=${CONDS:-"s80 s81"}
declare -A LAY=([s80]="env_layout8 scenario_80 340" [s81]="env_layout8 scenario_81 340")
for c in $CONDS; do
  read -r lay sc st <<< "${LAY[$c]}"
  for p in false true; do
    tag=${c}_$([ $p = true ] && echo on || echo off)
    PYTHONHASHSEED=0 $PY mesa_sim/run_mesa.py --domain kitting --layout "$lay" --scenario "$sc" \
      --steps "$st" --assignment_prior $p "$@" > /dev/null 2>&1 || echo "$tag: exit $?"
    cp "$(ls -t logs/run_*.log | head -1)" "$OUT/$tag.log"
    cp "$(ls -t logs/run_*.rec | head -1)" "$OUT/$tag.rec"    # the human executor's record stream (T-H2)
  done
done
