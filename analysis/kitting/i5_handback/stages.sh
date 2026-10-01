#!/usr/bin/env bash
# stages.sh — regenerate the I5 confirmation. Logs are gitignored (*.log); this is how they come back.
#   baseline : I4c code (ac240a8, the I4d reversion reference), run_mesa.py                                  -> baseline/
#   new      : HEAD (I5: no model change), run_mesa.py -> new/
#   harness  : check_i5.py: the instrumented base (cmp'd against new/), the variant nofold
#              (cmp'd against baseline/); summary.md, metrics.csv, the CSVs, invariant.csv, retrigger.md,
#              retention.csv, chains.md, region.md
#   diffs    : diff_ir.py (I2's) baseline -> new, and new -> each variant, per condition
# Usage: analysis/i5_handback/stages.sh   (from the repo root; needs git worktree, ~5 min; no diffs (new/ is I4d's))
set -e
HERE=$(cd "$(dirname "$0")" && pwd); ROOT=$(cd "$HERE/../.." && pwd); BASE=ac240a8
PY=~/python-envs/teamrob-sp4-env/bin/python
WT=$(mktemp -d)
trap 'cd "$ROOT"; git worktree remove --force "$WT/s0" 2>/dev/null || true; git worktree prune' EXIT
cd "$ROOT"
git worktree add -q "$WT/s0" $BASE; mkdir -p "$WT/s0/logs"
"$ROOT/analysis/i3_phase_model/sweep.sh" "$WT/s0" "$HERE/baseline"
"$ROOT/analysis/i3_phase_model/sweep.sh" "$ROOT"  "$HERE/new"
PYTHONHASHSEED=0 $PY "$HERE/check_i5.py" > /dev/null
echo "stages regenerated"
