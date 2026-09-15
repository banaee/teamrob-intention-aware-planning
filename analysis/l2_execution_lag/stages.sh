#!/usr/bin/env bash
# stages.sh — regenerate L2 end to end (~1 min). Logs and captures are git-ignored.
#   new/                    the ten sweep conditions at HEAD (the T3/T4/T10 baselines)
#   captures_new/           T1b's instrumented capture over its eight conditions
#   comparison.md           decisions vs the T9 baselines
#   timing_*.md             TODO-77's measure, before and after, by the same script
# Usage: analysis/l2_execution_lag/stages.sh   (from the repo root)
set -e
HERE=$(cd "$(dirname "$0")" && pwd); ROOT=$(cd "$HERE/../.." && pwd)
PY=~/python-envs/teamrob-sp4-env/bin/python
cd "$ROOT"
"$ROOT/analysis/t9_arrival_radius/sweep.sh" "$ROOT" "$HERE/new"
PYTHONHASHSEED=0 $PY analysis/t1b_realization/measure.py --out "$HERE/captures_new" > /dev/null
$PY "$HERE/compare.py" > /dev/null
$PY "$HERE/timing.py" analysis/t9_arrival_radius/captures_new/captures.json \
    analysis/t9_arrival_radius/new "(before L2)" > "$HERE/timing_before.md"
$PY "$HERE/timing.py" "$HERE/captures_new/captures.json" "$HERE/new" "(after L2)" > "$HERE/timing_after.md"
$PY "$HERE/residual.py" "$HERE/captures_new/captures.json" "$HERE/new" > "$HERE/residual.md"
PYTHONHASHSEED=0 $PY "$HERE/ablate.py" env_layout3 scenario_30 true 60 21 > "$HERE/ablation.md"
echo "L2 regenerated"
