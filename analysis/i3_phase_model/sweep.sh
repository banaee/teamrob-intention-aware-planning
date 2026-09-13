#!/usr/bin/env bash
# sweep.sh <repo_root> <out_dir>  — the eight sweep conditions, PYTHONHASHSEED=0, logs copied to out_dir/<cond>.log
set -e
ROOT=$1; OUT=$2; PY=~/python-envs/teamrob-sp4-env/bin/python
mkdir -p "$OUT"
cd "$ROOT"
for c in "s00 env_layout0 scenario_00 300" "s20 env_layout2 scenario_20 200" "s30 env_layout3 scenario_30 200" "s40 env_layout4 scenario_40 400"; do
  set -- $c
  for p in false true; do
    tag=$1_$([ $p = true ] && echo on || echo off)
    PYTHONHASHSEED=0 $PY mesa_sim/run_mesa.py --domain kitting --layout $2 --scenario $3 --steps $4 --assignment_prior $p > /dev/null 2>&1
    new=$(ls -t logs/run_*.log | head -1)
    cp "$new" "$OUT/$tag.log"
  done
done
echo "done $OUT"
