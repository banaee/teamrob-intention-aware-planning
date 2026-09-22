#!/usr/bin/env bash
# sweep.sh <out_dir> — the task_committed ablation. Each condition with --task_committed_trigger true and false,
# cost realized, stop off, PYTHONHASHSEED=0, run through capture.py (log unchanged; <tag>.json holds each decision's
# head projection for the release residual). Set A: s80 s81 s83 (340 steps), s20 s70 (300) x strategy single_task /
# full_reorder x prior off/on, gate none. Set B: s10 (450), s20 (300), s30 (200), gate b2a, single_task, prior off/on.
# Logs copied to <out_dir>/<tag>.log (git-ignored). Sequential. Run from the repo root.
set -e
OUT=$1; shift; PY=~/python-envs/teamrob-sp4-env/bin/python; mkdir -p "$OUT"
CAP=analysis/ablation_task_committed/capture.py
declare -A LAY=([s80]="env_layout8 scenario_80 340" [s81]="env_layout8 scenario_81 340"
                [s83]="env_layout8 scenario_83 340" [s20]="env_layout2 scenario_20 300"
                [s70]="env_layout7 scenario_70 300" [s10]="env_layout1 scenario_10 450"
                [s30]="env_layout3 scenario_30 200")
run() {  # tag cond strategy gate prior trig
  read -r lay sc st <<< "${LAY[$2]}"
  PYTHONHASHSEED=0 $PY $CAP "$OUT/$1.json" --domain kitting --layout "$lay" --scenario "$sc" --steps "$st" \
    --strategy $3 --gate_strategy $4 --cost_strategy realized --separation_stop false --assignment_prior $5 \
    --task_committed_trigger $6 > /dev/null 2>&1 || echo "$1: exit $?"
  cp "$(ls -t logs/run_*.log | head -1)" "$OUT/$1.log"
}
for t in true false; do tt=$([ $t = true ] && echo with || echo without)
  for p in false true; do pp=$([ $p = true ] && echo on || echo off)
    for c in ${CONDS_A-s80 s81 s83 s20 s70}; do for s in single_task full_reorder; do
      run ${c}_${s}_${pp}_$tt $c $s none $p $t; done; done
    for c in ${CONDS_B-s10 s20 s30}; do run ${c}_b2a_${pp}_$tt $c single_task b2a $p $t; done
  done
done
