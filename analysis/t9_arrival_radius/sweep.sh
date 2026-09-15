#!/usr/bin/env bash
# sweep.sh <repo_root> <out_dir> — the ten T9 conditions (s00, s10, s20, s30, s40 × assignment prior
# off/on), PYTHONHASHSEED=0, each headless log copied to <out_dir>/<cond>.log. Logs are git-ignored
# (*.log); this is how they come back. Step counts: the T5/T1b sweep's for s00–s40; 450 for s10 (the robot's last task starts at 283 and its carry ends past 400).
# Usage: analysis/t9_arrival_radius/sweep.sh "$PWD" analysis/t9_arrival_radius/new   (~30 s)
set -e
ROOT=$1; OUT=$2; PY=~/python-envs/teamrob-sp4-env/bin/python
mkdir -p "$OUT"
cd "$ROOT"
for c in "s00 env_layout0 scenario_00 300" "s10 env_layout1 scenario_10 450" "s20 env_layout2 scenario_20 200" "s30 env_layout3 scenario_30 200" "s40 env_layout4 scenario_40 400"; do
  set -- $c
  for p in false true; do
    tag=$1_$([ $p = true ] && echo on || echo off)
    PYTHONHASHSEED=0 $PY mesa_sim/run_mesa.py --domain kitting --layout $2 --scenario $3 --steps $4 --assignment_prior $p > "$OUT/$tag.stdout" 2>&1 || echo "$tag: exit $?"
    new=$(ls -t logs/run_*.log | head -1)
    cp "$new" "$OUT/$tag.log"
  done
done
echo "done $OUT"
