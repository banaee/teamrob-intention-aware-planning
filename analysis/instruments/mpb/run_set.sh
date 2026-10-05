#!/usr/bin/env bash
# run_set.sh <domain> -o <out_root> <run files> — the planning test-bed for a set whose settings live in its run files
# (T-F part 1; design_records.md, "T-F part 1: the conditions human-unaware and intention-unaware", I, R9 as amended by
# A, G). No setting is passed on the command line and none is in a name (I): a run is named by its run file
# (<name>.yaml, a serial), its outputs in <out_root>/<scenario>/<name>/ with its log and .rec there (<name>.log; K, the
# measurement of T-F part 1: one folder per scenario, the runs of its conditions inside it by serial); the settings are
# the run file's, printed in the run's [run] header and written as columns of <out_root>/results.csv (table.py).
# Per run file: the safety cap (the domain's horizon.py, MPB-5) as the run's steps; the run; the trajectory and its
# check; the in-process actual (actual.py); the settings (conditions.py: R5's reading of the run file against the
# header, the condition, whether the objects are separate); human-unaware with an independent script, the reference
# run (reference.py); the oracle's table, the chain and the comparison where a table is derivable before the run (an
# independent script, and in the intention-aware run assignment knowledge on, MPB-6); the measures with no declared
# property (measures.py); the run's one figure (plot.py, N); the separation counts. Last, table.py over the out_root.
# run.sh stays the runner of the maintained outputs (their names and folders unchanged). PYTHONHASHSEED=0. Sequential:
# each run's log is the newest logs/run_*.log. Run from the repo root.
set -eo pipefail
DOMAIN=$1; shift
PY=~/python-envs/ir-nomesa-env/bin/python; D=analysis/instruments/mpb; IR=analysis/instruments/irb
DOM=analysis/$DOMAIN/mpb; ROOT=""; RUNS=""
while [ $# -gt 0 ]; do
  case $1 in
    -o) ROOT=$2; shift 2;;
    *) RUNS="$RUNS $1"; shift;;
  esac
done
[ -n "$ROOT" ] && [ -n "$RUNS" ] || { echo "usage: run_set.sh <domain> -o <out_root> <run files>"; exit 2; }
mkdir -p $ROOT
for RUN in $RUNS; do
  name=$(basename $RUN .yaml); sid=$(awk '/^scenario:/ {print $2}' $RUN)
  OUT=$ROOT/$sid/$name; LOG=$OUT/$name.log; mkdir -p $OUT
  steps=$(PYTHONHASHSEED=0 $PY $DOM/horizon.py $RUN 2>/dev/null | tail -1)
  last=$(PYTHONHASHSEED=0 $PY $IR/trajectory.py $RUN --length 2>/dev/null | tail -1)
  PYTHONHASHSEED=0 $PY mesa_sim/run_mesa.py --run $RUN --steps $steps < /dev/null > /dev/null 2>&1
  cp "$(ls -t logs/run_*.log | head -1)" $LOG
  cp "$(ls -t logs/run_*.rec | head -1)" ${LOG%.log}.rec
  PYTHONHASHSEED=0 $PY $D/conditions.py $RUN $LOG $OUT
  read -r condition dep separate assignment strategy <<< "$($PY -c "import json; s = json.load(open('$OUT/settings.json')); \
e = s['effective']; print(s['condition'], s['dependence'], s['objects_separate'], e['assignment_knowledge'], e['strategy'])")"
  if [ "$dep" = on_robot ]; then
    # a script that depends on the robot (T-G A3, MPB-DL3, G): no table before the run; the human's last
    # acknowledgement is the run's own
    PYTHONHASHSEED=0 $PY $IR/trajectory.py $RUN $steps $OUT/trajectory.json 2>&1 | grep -v '^\[' || true
    hid=$(awk '/^\s*step: [0-9]+: \[human/ {print $3; exit}' $LOG)
    last=$(awk -v h="$hid" '/^\s*step: [0-9]+: / && $3 == h && $5 != "action=None" {t = $2} END {sub(":", "", t); print t}' $LOG)
  else
    PYTHONHASHSEED=0 $PY $IR/trajectory.py $RUN $steps $OUT/trajectory.json $LOG 2>&1 | grep -v '^\[' || true
  fi
  PYTHONHASHSEED=0 $PY $D/actual.py $RUN $steps $LOG $last $OUT 2>&1 | grep -v -e '^\[' -e '^  step' || true
  if [ "$condition" = human-unaware ] && [ "$dep" != on_robot ]; then
    PYTHONHASHSEED=0 $PY $D/reference.py $RUN $steps $OUT/${name}_reference.log $OUT/reference.json \
      --strategy $strategy 2>&1 | grep -v -e '^\[' -e '^  step' || true
  fi
  if [ "$dep" != on_robot ] && { [ "$condition" != intention-aware ] || [ "$assignment" = True ]; }; then
    if PYTHONHASHSEED=0 $PY $D/mpb_oracle.py $OUT/trajectory.json $RUN $LOG $OUT/expected_ticks.json; then
      if $PY $D/chain.py $OUT/expected_ticks.json $OUT/observed.json $OUT/expected_decisions.json; then
        $PY $D/compare.py $sid $OUT
      else
        echo "$name: no chain and no comparison of decisions (D3: an undetermined gate at a decision)"
      fi
    fi
  fi
  PYTHONHASHSEED=0 $PY $D/measures.py $sid $OUT $LOG $RUN
  $PY $D/plot.py $sid $OUT $LOG   # the run's one figure, the panels its condition has (N)
  $PY analysis/instruments/common/separation.py $LOG > $OUT/separation.md
done
$PY $D/table.py $ROOT
