#!/usr/bin/env bash
# stages.sh — regenerate the T5 comparison. Logs are gitignored (*.log); this is how they come back.
#   baseline : the T7/T8 baselines, analysis/t7_t8_meta_bugs/new/ (regenerate with that folder's stages.sh)
#   new      : HEAD, run_mesa.py -> new/   (the meta-planner-side regression baselines from T5 on)
#   compare.py -> summary.md;  inject.py -> the isolated mechanism (see summary.md, "The mechanism")
# Usage: analysis/t5_continue/stages.sh   (from the repo root; ~2 min)
set -e
HERE=$(cd "$(dirname "$0")" && pwd); ROOT=$(cd "$HERE/../.." && pwd)
PY=~/python-envs/teamrob-sp4-env/bin/python
cd "$ROOT"
"$ROOT/analysis/i3_phase_model/sweep.sh" "$ROOT" "$HERE/new"
$PY "$HERE/compare.py" > /dev/null
for inj in "" 3 5 6 29 30; do PYTHONHASHSEED=0 $PY "$HERE/inject.py" env_layout0 scenario_00 false 40 2 8 $inj; done > "$HERE/inject_s00_off.txt"
for inj in "" 46 47 84 85; do PYTHONHASHSEED=0 $PY "$HERE/inject.py" env_layout3 scenario_30 false 100 44 50 $inj; done > "$HERE/inject_s30_off.txt"
echo "stages regenerated"
