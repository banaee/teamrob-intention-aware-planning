#!/usr/bin/env bash
# sweep.sh <out_dir> — the T-B1c records: scenario_s06_03 and scenario_s06_01 on env_layout_08 (the ids since T-L
# stage 3) under --strategy full_reorder, cost_strategy realized and plain, assignment prior off and on; gate none,
# stop off; 340 steps; PYTHONHASHSEED=0. Each log is copied to <out_dir>/<layout id>_<scenario id>_<cost>_<prior>.log,
# its .rec beside it (git-ignored; md5s in the README). These are records of an existence case, NOT baselines
# (full_reorder baselines are T-B3's). Sequential: each run's log is picked up as the newest logs/run_*.log. Run from
# the repo root.
set -e
OUT=$1; shift; PY=~/python-envs/teamrob-sp4-env/bin/python; mkdir -p "$OUT"
LAY=env_layout_08
for sc in scenario_s06_03 scenario_s06_01; do
  for cost in realized plain; do
    for p in false true; do
      tag=${LAY}_${sc}_${cost}_$([ $p = true ] && echo on || echo off)
      PYTHONHASHSEED=0 $PY mesa_sim/run_mesa.py --domain kitting --layout $LAY --scenario "$sc" --steps 340 \
        --strategy full_reorder --cost_strategy $cost --gate_strategy none --separation_stop false \
        --assignment_prior $p "$@" > /dev/null 2>&1 || echo "$tag: exit $?"
      cp "$(ls -t logs/run_*.log | head -1)" "$OUT/$tag.log"
      cp "$(ls -t logs/run_*.rec | head -1)" "$OUT/$tag.rec"    # the human executor's record stream (T-H2)
    done
  done
done
