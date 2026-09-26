#!/usr/bin/env bash
# sweep.sh <out_dir> — the tb1a baselines (T-L stage 3; before it, analysis/f1_robot_responsible/sweep.sh and
# analysis/f47_fixtures/sweep.sh, frozen with the old ids): the regression five and the evaluation fixtures, gate none,
# cost realized, stop off, assignment prior off and on; PYTHONHASHSEED=0. Each log is copied to
# <out_dir>/<layout id>_<scenario id>_<prior>.log, its .rec beside it (git-ignored; md5s in the README). $CONDS
# (default: all eight) restricts the runs to the scenario ids it names. Sequential: each run's log is picked up as the
# newest logs/run_*.log. Run from the repo root.
set -e
OUT=$1; shift; PY=~/python-envs/ir-nomesa-env/bin/python; mkdir -p "$OUT"
RUNS="env_layout_01 scenario_s01_01 300
env_layout_02 scenario_s02_01 450
env_layout_03 scenario_s03_01 300
env_layout_04 scenario_s01_06 200
env_layout_05 scenario_s04_01 400
env_layout_06 scenario_s03_06 300
env_layout_07 scenario_s05_01 300
env_layout_07 scenario_s05_02 300"
while read -r lay sc st; do
  [ -n "$CONDS" ] && [[ " $CONDS " != *" $sc "* ]] && continue
  for p in false true; do
    tag=${lay}_${sc}_$([ $p = true ] && echo on || echo off)
    PYTHONHASHSEED=0 $PY mesa_sim/run_mesa.py --domain kitting --layout "$lay" --scenario "$sc" --steps "$st" \
      --cost_strategy realized --gate_strategy none --separation_stop false \
      --assignment_prior $p < /dev/null > /dev/null 2>&1 || echo "$tag: exit $?"
    cp "$(ls -t logs/run_*.log | head -1)" "$OUT/$tag.log"
    cp "$(ls -t logs/run_*.rec | head -1)" "$OUT/$tag.rec"    # the human executor's record stream (T-H2)
  done
done <<< "$RUNS"
