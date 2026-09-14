#!/usr/bin/env bash
# stages.sh — regenerate the T7/T8 comparison. Logs are gitignored (*.log); this is how they come back.
#   baseline : adf9aea (HEAD before T7/T8), run_mesa.py -> baseline/
#   new      : HEAD, run_mesa.py -> new/   (the meta-planner-side regression baselines from T7/T8 on)
#   compare.py -> summary.md
# Usage: analysis/t7_t8_meta_bugs/stages.sh   (from the repo root; needs git worktree, ~4 min)
set -e
HERE=$(cd "$(dirname "$0")" && pwd); ROOT=$(cd "$HERE/../.." && pwd); BASE=adf9aea
PY=~/python-envs/teamrob-sp4-env/bin/python
WT=$(mktemp -d)
trap 'cd "$ROOT"; git worktree remove --force "$WT/s0" 2>/dev/null || true; git worktree prune' EXIT
cd "$ROOT"
git worktree add -q "$WT/s0" $BASE; mkdir -p "$WT/s0/logs"
"$ROOT/analysis/i3_phase_model/sweep.sh" "$WT/s0" "$HERE/baseline"
"$ROOT/analysis/i3_phase_model/sweep.sh" "$ROOT"  "$HERE/new"
$PY "$HERE/compare.py" > /dev/null
echo "stages regenerated"
