#!/usr/bin/env bash
# stages.sh — regenerate the I4d replay. Logs are gitignored (*.log); this is how they come back.
#   baseline : I4c code (ac240a8), run_mesa.py                                  -> baseline/
#   new      : HEAD (I4d: unknown folds with the stretch), run_mesa.py -> new/
#   harness  : check_i4d.py --final: the instrumented base (cmp'd against new/), the variant nofold
#              (cmp'd against baseline/); summary.md, metrics.csv, the CSVs, invariant.csv, retrigger.md,
#              retention.csv, chains.md, region.md
#   diffs    : diff_ir.py (I2's) baseline -> new, and new -> each variant, per condition
# Usage: analysis/i4d_fold_unknown/stages.sh   (from the repo root; needs git worktree, ~5 min)
set -e
HERE=$(cd "$(dirname "$0")" && pwd); ROOT=$(cd "$HERE/../.." && pwd); BASE=ac240a8
PY=~/python-envs/teamrob-sp4-env/bin/python
WT=$(mktemp -d)
trap 'cd "$ROOT"; git worktree remove --force "$WT/s0" 2>/dev/null || true; git worktree prune' EXIT
cd "$ROOT"
git worktree add -q "$WT/s0" $BASE; mkdir -p "$WT/s0/logs"
"$ROOT/analysis/i3_phase_model/sweep.sh" "$WT/s0" "$HERE/baseline"
"$ROOT/analysis/i3_phase_model/sweep.sh" "$ROOT"  "$HERE/new"
PYTHONHASHSEED=0 $PY "$HERE/check_i4d.py" --final > /dev/null
mkdir -p "$HERE/diffs"
D="$ROOT/analysis/i2_ir_foundations/diff_ir.py"; I="$HERE/logs_instrumented"
for c in s00_off s00_on s20_off s20_on s30_off s30_on s40_off s40_on; do
  python3 $D "$HERE/baseline/$c.log" "$HERE/new/$c.log" > "$HERE/diffs/${c}_base_to_new.txt"
  for v in nofold; do
    python3 $D "$HERE/new/$c.log" "$I/$v/$c.log" > "$HERE/diffs/${c}_new_to_${v}.txt"
  done
done
echo "stages regenerated"
