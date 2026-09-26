#!/usr/bin/env bash
# sweep.sh <out_dir> — T-B3: scenario_s06_01, scenario_s06_02, scenario_s06_03 (env_layout_08) and scenario_s03_01
# (env_layout_03), scenario_s05_01 (env_layout_07) — the ids since T-L stage 3 — under --strategy single_task and
# full_reorder × assignment prior off/on; cost_strategy realized, gate none, stop off; PYTHONHASHSEED=0. The one-table
# runs 300 steps, the env_layout_08 runs 340. Each log is copied to <out_dir>/<layout id>_<scenario id>_<strategy>_
# <prior>.log, its .rec beside it (git-ignored; md5s in the README). $CONDS restricts to the scenario ids it names.
# Sequential: each run's log is picked up as the newest logs/run_*.log. Run from the repo root.
set -e
OUT=$1; shift; PY=~/python-envs/teamrob-sp4-env/bin/python; mkdir -p "$OUT"
RUNS="env_layout_08 scenario_s06_01 340
env_layout_08 scenario_s06_02 340
env_layout_08 scenario_s06_03 340
env_layout_03 scenario_s03_01 300
env_layout_07 scenario_s05_01 300"
while read -r lay sc st; do
  [ -n "$CONDS" ] && [[ " $CONDS " != *" $sc "* ]] && continue
  for s in single_task full_reorder; do
    for p in false true; do
      tag=${lay}_${sc}_${s}_$([ $p = true ] && echo on || echo off)
      PYTHONHASHSEED=0 $PY mesa_sim/run_mesa.py --domain kitting --layout "$lay" --scenario "$sc" --steps "$st" \
        --strategy $s --cost_strategy realized --gate_strategy none --separation_stop false \
        --assignment_prior $p < /dev/null > /dev/null 2>&1 || echo "$tag: exit $?"
      cp "$(ls -t logs/run_*.log | head -1)" "$OUT/$tag.log"
      cp "$(ls -t logs/run_*.rec | head -1)" "$OUT/$tag.rec"    # the human executor's record stream (T-H2)
    done
  done
done <<< "$RUNS"
