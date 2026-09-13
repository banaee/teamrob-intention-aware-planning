#!/usr/bin/env bash
# stages.sh — regenerate the I4b replay. Logs are gitignored (*.log); this is how they come back.
#   S0 baseline : I4 code (3545d4a), run_mesa.py                                   -> baseline/
#   new         : HEAD (boundary A), run_mesa.py                                     -> new/
#   harness     : check_i4b.py --final --variants: the instrumented base (cmp'd against new/), `nobound`
#                 (cmp'd against baseline/), the candidates A_release / B / C5 / D, the `fold` reading,
#                 ungated and ownshelf with the boundary; summary.md, metrics.csv, CSVs
#   candidates  : candidates.py (from I4's CSVs; needs analysis/i4_evidence_model/new/ — I4's stages.sh)
#   diffs       : diff_ir.py (I2's) baseline -> new and new -> each variant, per condition
# Usage: analysis/i4b_boundary/stages.sh   (from the repo root; needs git worktree, ~6 min)
set -e
HERE=$(cd "$(dirname "$0")" && pwd); ROOT=$(cd "$HERE/../.." && pwd); BASE=3545d4a
PY=~/python-envs/teamrob-sp4-env/bin/python
WT=$(mktemp -d)
trap 'cd "$ROOT"; git worktree remove --force "$WT/s0" 2>/dev/null || true; git worktree prune' EXIT
cd "$ROOT"
git worktree add -q "$WT/s0" $BASE; mkdir -p "$WT/s0/logs"
"$ROOT/analysis/i3_phase_model/sweep.sh" "$WT/s0" "$HERE/baseline"
"$ROOT/analysis/i3_phase_model/sweep.sh" "$ROOT"  "$HERE/new"
PYTHONHASHSEED=0 $PY "$HERE/check_i4b.py" --final --variants > /dev/null
mkdir -p "$HERE/diffs"
D="$ROOT/analysis/i2_ir_foundations/diff_ir.py"; I="$HERE/logs_instrumented"
for c in s00_off s00_on s20_off s20_on s30_off s30_on s40_off s40_on; do
  python3 $D "$HERE/baseline/$c.log" "$HERE/new/$c.log" > "$HERE/diffs/${c}_base_to_new.txt"
  for v in A_release B C5 D fold ungated ownshelf; do
    python3 $D "$HERE/new/$c.log" "$I/$v/$c.log" > "$HERE/diffs/${c}_new_to_${v}.txt"
  done
done
echo "stages regenerated"
