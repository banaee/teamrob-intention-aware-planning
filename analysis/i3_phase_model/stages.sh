#!/usr/bin/env bash
# stages.sh — regenerate the I3 replay stages. Logs are gitignored (*.log); this is how they come back.
#   S0 baseline     : I2 code (5a8c480), unpatched                       -> baseline/
#   S1 stage1_zone  : S0 with ZONE_BOOST = 1.0                            -> stage1_zone/
#   S2 stage2_held  : S1 with _refuted_by_holding returning the empty set -> stage2_held/
#   S3 nopin        : HEAD with the terminal pin disabled (check_i3.py variant `nopin`) -> logs_instrumented/nopin/
#   S4 new          : HEAD                                                -> new/
# Usage: analysis/i3_phase_model/stages.sh   (from the repo root; needs git worktree, ~2 min)
set -e
HERE=$(cd "$(dirname "$0")" && pwd); ROOT=$(cd "$HERE/../.." && pwd); BASE=5a8c480
WT=$(mktemp -d)
trap 'cd "$ROOT"; for s in s0 s1 s2; do git worktree remove --force "$WT/$s" 2>/dev/null || true; done; git worktree prune' EXIT
cd "$ROOT"
for s in s0 s1 s2; do git worktree add -q "$WT/$s" $BASE; mkdir -p "$WT/$s/logs"; done
sed -i 's/^ZONE_BOOST         = 2.0/ZONE_BOOST         = 1.0/' "$WT/s1/shared/recognizer.py" "$WT/s2/shared/recognizer.py"
python3 - "$WT/s2/shared/recognizer.py" <<'PY'
import sys; p=sys.argv[1]; s=open(p).read()
old="""        agent_state = world.agent_states.get(obs.agent_id)
        held = agent_state.holding if agent_state is not None else None
        if held is None:
            return set()"""
assert old in s
open(p,"w").write(s.replace(old, """        held = None   # STAGE S2: held-item rule disabled
        if held is None:
            return set()"""))
PY
"$HERE/sweep.sh" "$WT/s0" "$HERE/baseline"
"$HERE/sweep.sh" "$WT/s1" "$HERE/stage1_zone"
"$HERE/sweep.sh" "$WT/s2" "$HERE/stage2_held"
"$HERE/sweep.sh" "$ROOT"  "$HERE/new"
PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python "$HERE/check_i3.py" --variants > /dev/null
mkdir -p "$HERE/diffs"
for c in s00_off s00_on s20_off s20_on s30_off s30_on s40_off s40_on; do
  D="$ROOT/analysis/i2_ir_foundations/diff_ir.py"; I="$HERE/logs_instrumented/nopin"
  python3 $D "$HERE/baseline/$c.log"    "$HERE/stage1_zone/$c.log" > "$HERE/diffs/${c}_base_to_s1.txt"
  python3 $D "$HERE/stage1_zone/$c.log" "$HERE/stage2_held/$c.log" > "$HERE/diffs/${c}_s1_to_s2.txt"
  python3 $D "$HERE/stage2_held/$c.log" "$I/$c.log"                > "$HERE/diffs/${c}_s2_to_s3nopin.txt"
  python3 $D "$I/$c.log"                "$HERE/new/$c.log"         > "$HERE/diffs/${c}_s3nopin_to_new.txt"
  python3 $D "$HERE/stage2_held/$c.log" "$HERE/new/$c.log"         > "$HERE/diffs/${c}_s2_to_new.txt"
  python3 $D "$HERE/baseline/$c.log"    "$HERE/new/$c.log"         > "$HERE/diffs/${c}_base_to_new.txt"
done
echo "stages regenerated"
