#!/usr/bin/env bash
# stages.sh — regenerate the I4 replay. Logs are gitignored (*.log); this is how they come back.
#   S0 baseline : I3 code (1669011), unpatched, run_mesa.py                          -> baseline/
#   S2 new      : HEAD, run_mesa.py at the shipped constants                          -> new/
#   harness     : HEAD through check_i4.py --final --variants: the instrumented base run
#                 (logs_instrumented/base, cmp'd against new/), the CSVs, summary.md, and the
#                 analysis-only variants — S1 `rawlogistic` (the spec's literal logistic, 0.5 at
#                 zero excess), `costdif2`, `ungated`, `ownshelf`, `reset_origin`, `reset_boundary`
#   sweeps      : NOT rerun here (sweep_abs.csv, sweep_frac.csv, sweep_abs_fine.csv are committed);
#                 `check_i4.py --sweep abs|frac|"abs fine"` regenerates them (~4 min each, 4 cores)
#   diffs       : diff_ir.py (I2's) base -> S1 -> new and new -> each what-if, per condition
# Usage: analysis/i4_evidence_model/stages.sh   (from the repo root; needs git worktree, ~5 min)
set -e
HERE=$(cd "$(dirname "$0")" && pwd); ROOT=$(cd "$HERE/../.." && pwd); BASE=1669011
PY=~/python-envs/teamrob-sp4-env/bin/python
WT=$(mktemp -d)
trap 'cd "$ROOT"; git worktree remove --force "$WT/s0" 2>/dev/null || true; git worktree prune' EXIT
cd "$ROOT"
git worktree add -q "$WT/s0" $BASE; mkdir -p "$WT/s0/logs"
"$ROOT/analysis/i3_phase_model/sweep.sh" "$WT/s0" "$HERE/baseline"
"$ROOT/analysis/i3_phase_model/sweep.sh" "$ROOT"  "$HERE/new"
PYTHONHASHSEED=0 $PY "$HERE/check_i4.py" --final --variants > /dev/null
mkdir -p "$HERE/diffs"
D="$ROOT/analysis/i2_ir_foundations/diff_ir.py"; I="$HERE/logs_instrumented"
for c in s00_off s00_on s20_off s20_on s30_off s30_on s40_off s40_on; do
  python3 $D "$HERE/baseline/$c.log"  "$I/rawlogistic/$c.log" > "$HERE/diffs/${c}_base_to_s1raw.txt"
  python3 $D "$I/rawlogistic/$c.log"  "$HERE/new/$c.log"      > "$HERE/diffs/${c}_s1raw_to_new.txt"
  python3 $D "$HERE/baseline/$c.log"  "$HERE/new/$c.log"      > "$HERE/diffs/${c}_base_to_new.txt"
  for v in costdif2 ungated ownshelf reset_origin reset_boundary; do
    python3 $D "$HERE/new/$c.log" "$I/$v/$c.log" > "$HERE/diffs/${c}_new_to_${v}.txt"
  done
done
echo "stages regenerated"
