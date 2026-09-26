#!/usr/bin/env bash
# sweep.sh <out_dir> [run_mesa args...] — headless runs of the two-table fixture (T-B1b), PYTHONHASHSEED=0, each
# log copied to <out_dir>/<layout id>_<scenario id>_<prior>.log, its .rec beside it (git-ignored). Runs: scenario_s06_01
# and scenario_s06_02 on env_layout_08 (the ids since T-L stage 3; $CONDS restricts to the scenario ids it names) ×
# assignment prior off/on, 340 steps each (both complete by 265). Extra args go to run_mesa.py. Sequential: each run's
# log is picked up as the newest logs/run_*.log. Run from the repo root.
set -e
OUT=$1; shift; PY=~/python-envs/teamrob-sp4-env/bin/python; mkdir -p "$OUT"
RUNS="env_layout_08 scenario_s06_01 340
env_layout_08 scenario_s06_02 340"
while read -r lay sc st; do
  [ -n "$CONDS" ] && [[ " $CONDS " != *" $sc "* ]] && continue
  for p in false true; do
    tag=${lay}_${sc}_$([ $p = true ] && echo on || echo off)
    PYTHONHASHSEED=0 $PY mesa_sim/run_mesa.py --domain kitting --layout "$lay" --scenario "$sc" \
      --steps "$st" --assignment_prior $p "$@" < /dev/null > /dev/null 2>&1 || echo "$tag: exit $?"
    cp "$(ls -t logs/run_*.log | head -1)" "$OUT/$tag.log"
    cp "$(ls -t logs/run_*.rec | head -1)" "$OUT/$tag.rec"    # the human executor's record stream (T-H2)
  done
done <<< "$RUNS"
