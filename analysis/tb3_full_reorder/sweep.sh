#!/usr/bin/env bash
# sweep.sh <out_dir> — T-B3: s80, s81, s83 (env_layout8) and s20, s70 (one table) under --strategy single_task and
# full_reorder × assignment prior off/on; cost_strategy realized, gate none, stop off; PYTHONHASHSEED=0. s20 and s70
# 300 steps, the env_layout8 fixtures 340. Each log is copied to <out_dir>/<cond>_<strategy>_<prior>.log (git-ignored;
# md5s in the README). Sequential: each run's log is picked up as the newest logs/run_*.log. Run from the repo root.
set -e
OUT=$1; shift; PY=~/python-envs/teamrob-sp4-env/bin/python; mkdir -p "$OUT"
CONDS=${CONDS:-"s80 s81 s83 s20 s70"}
declare -A LAY=([s80]="env_layout8 scenario_80 340" [s81]="env_layout8 scenario_81 340"
                [s83]="env_layout8 scenario_83 340" [s20]="env_layout2 scenario_20 300"
                [s70]="env_layout7 scenario_70 300")
for c in $CONDS; do
  read -r lay sc st <<< "${LAY[$c]}"
  for s in single_task full_reorder; do
    for p in false true; do
      tag=${c}_${s}_$([ $p = true ] && echo on || echo off)
      PYTHONHASHSEED=0 $PY mesa_sim/run_mesa.py --domain kitting --layout "$lay" --scenario "$sc" --steps "$st" \
        --strategy $s --cost_strategy realized --gate_strategy none --separation_stop false \
        --assignment_prior $p > /dev/null 2>&1 || echo "$tag: exit $?"
      cp "$(ls -t logs/run_*.log | head -1)" "$OUT/$tag.log"
    done
  done
done
