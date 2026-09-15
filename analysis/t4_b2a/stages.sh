#!/usr/bin/env bash
# stages.sh — regenerate T4's comparison (~3 min). Logs are git-ignored; this is how they come back.
#   none/   gate_strategy none, the ten regression conditions; must equal the L2 baselines
#           (analysis/l2_execution_lag/new/, regenerate with that folder's stages.sh) byte for byte
#   b2a/    gate_strategy b2a (rho 0.5), s00/s10/s20/s30 × prior off/on
#   cf/     cf_b3.py over the same eight conditions (B3 counterfactual at every B2 continue)
#   comparison.md   compare.py none b2a cf
# Usage: analysis/t4_b2a/stages.sh   (from the repo root)
set -e
HERE=$(cd "$(dirname "$0")" && pwd); ROOT=$(cd "$HERE/../.." && pwd)
PY=~/python-envs/teamrob-sp4-env/bin/python
cd "$ROOT"
"$HERE/sweep.sh" "$HERE/none"
L2="$ROOT/analysis/l2_execution_lag/new"
for f in "$HERE"/none/*.log; do
  c=$(basename "$f")
  if [ -f "$L2/$c" ]; then cmp -s "$f" "$L2/$c" && echo "none $c == L2 baseline" || echo "none $c DIFFERS from L2 baseline"; fi
done
CONDS="s00 s10 s20 s30" "$HERE/sweep.sh" "$HERE/b2a" --gate_strategy b2a
mkdir -p "$HERE/cf"
declare -A LAY=([s00]="env_layout0 scenario_00 300" [s10]="env_layout1 scenario_10 450"
                [s20]="env_layout2 scenario_20 200" [s30]="env_layout3 scenario_30 200")
for c in s00 s10 s20 s30; do
  read -r lay sc st <<< "${LAY[$c]}"
  for p in false true; do
    PYTHONHASHSEED=0 $PY "$HERE/cf_b3.py" "$lay" "$sc" $p "$st" "$HERE/cf/${c}_$([ $p = true ] && echo on || echo off).log" b2a &
  done
done
wait
$PY "$HERE/compare.py" "$HERE/none" "$HERE/b2a" "$HERE/cf" > "$HERE/comparison.md"
echo "T4 regenerated"
