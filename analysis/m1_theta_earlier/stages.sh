#!/usr/bin/env bash
# stages.sh — regenerate M1 end to end (~1 min). Logs and captures are git-ignored.
#   logs/      four plain runs (run_mesa's own headless loop, [sep] included)
#   captures.json + logs_instrumented/   T1b's instrumented capture, same four runs
#   realization.md / .json   what realization would give at min_separation = 50 cm
#   why.md     hold budget vs shift needed, per admitted trigger and candidate
# theta is forced per process; shared/ is never edited.
# Usage: analysis/m1_theta_earlier/stages.sh   (from the repo root)
set -e
HERE=$(cd "$(dirname "$0")" && pwd); ROOT=$(cd "$HERE/../.." && pwd)
PY=~/python-envs/teamrob-sp4-env/bin/python
cd "$ROOT"; mkdir -p "$HERE/logs"
for t in 0.75 0.65; do
  for p in false true; do
    tag=s30_$([ $p = true ] && echo on || echo off)_t$(echo $t | tr -d '.')
    PYTHONHASHSEED=0 $PY "$HERE/run_theta.py" $t --domain kitting --layout env_layout3 \
        --scenario scenario_30 --steps 200 --assignment_prior $p > "$HERE/logs/$tag.stdout" 2>&1
    cp "$(ls -t logs/run_*.log | head -1)" "$HERE/logs/$tag.log"
  done
done
PYTHONHASHSEED=0 $PY "$HERE/capture.py" > /dev/null
$PY "$HERE/realize_m1.py" --sep 50 > /dev/null
$PY "$HERE/why.py" --sep 50 > /dev/null
echo "M1 regenerated"
