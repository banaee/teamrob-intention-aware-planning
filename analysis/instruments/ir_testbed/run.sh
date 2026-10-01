#!/usr/bin/env bash
# run.sh <domain> [--expect] [-o out_root] [run files] — the IR test-bed (TB.3b, made layout-independent in TB.4b; the code shared
# by the domains since the sort, 1 October 2026): per run file (default: every configs/<domain>/ir_testbed/*.yaml), the
# run length from the trajectory (the executor's rule, since the sort), the run, the trajectory and its check against the
# run's human lines, the expectations, the actual outputs, the comparison, the figure, the summary and the separation
# counts (separation.md, since the sort). With --expect: the trajectory and the expectations only, no run. Outputs in
# <out_root>/<scenario>/ (default analysis/<domain>/ir_testbed/); the run's log and .rec in <out_root>/runs/
# (git-ignored; md5s in that folder's README.md). PYTHONHASHSEED=0. Sequential: each run's log is picked up as the newest logs/run_*.log. Run from the
# repo root.
# The run length (TB.3b's rule, Q3 of TB.4b): the replay's last acknowledgement tick + 1 + MARGIN, MARGIN covering E5's
# standing threshold at the lowest reported level (alpha = 0.01: 25 ticks). Computed here and passed as --steps, so a
# changed room needs a rerun and nothing else; a run file whose own `steps` differs is named in a notice.
set -eo pipefail
MARGIN=30
DOMAIN=$1; shift
PY=~/python-envs/ir-nomesa-env/bin/python; D=analysis/instruments/ir_testbed; ROOT=analysis/$DOMAIN/ir_testbed
EXPECT=""
if [ "$1" = "--expect" ]; then EXPECT=1; shift; fi
if [ "$1" = "-o" ]; then ROOT=$2; shift 2; fi
RUNS=${*:-$(ls configs/$DOMAIN/ir_testbed/*.yaml)}
mkdir -p $ROOT/runs
for RUN in $RUNS; do
  sid=$(awk '/^scenario:/ {print $2}' $RUN); layout=$(awk '/^layout:/ {print $2}' $RUN)
  OUT=$ROOT/$sid; LOG=$ROOT/runs/${layout}_${sid}_on.log; mkdir -p $OUT
  last=$(PYTHONHASHSEED=0 $PY $D/trajectory.py $RUN --length 2>/dev/null | tail -1)
  steps=$((last + 1 + MARGIN)); own=$(awk '/^steps:/ {print $2}' $RUN)
  [ "$own" = "$steps" ] || echo "$sid: notice: the run file's steps ($own) differ from the rule's ($steps); run with $steps"
  if [ -n "$EXPECT" ]; then
    # the expectations before any run (since the sort): the trajectory and the oracle's tables, with theta the value
    # of record (the [run] header's theta=0.75, DEFAULT_THETA); the run's own oracle call must reproduce them
    PYTHONHASHSEED=0 $PY $D/trajectory.py $RUN $steps $OUT/trajectory.json 2>&1 | grep -v '^\['
    PYTHONHASHSEED=0 $PY $D/oracle.py $OUT/trajectory.json $RUN $OUT/expected.csv $OUT/phases.json theta=0.75
    continue
  fi
  PYTHONHASHSEED=0 $PY mesa_sim/run_mesa.py --run $RUN --steps $steps < /dev/null > /dev/null 2>&1
  cp "$(ls -t logs/run_*.log | head -1)" $LOG
  cp "$(ls -t logs/run_*.rec | head -1)" ${LOG%.log}.rec
  PYTHONHASHSEED=0 $PY $D/trajectory.py $RUN $steps $OUT/trajectory.json $LOG 2>&1 | grep -v '^\['
  PYTHONHASHSEED=0 $PY $D/oracle.py $OUT/trajectory.json $RUN $OUT/expected.csv $OUT/phases.json $LOG
  PYTHONHASHSEED=0 $PY $D/actual.py $RUN $steps $LOG $OUT/actual.csv $OUT/actual_log.csv 2>&1 | grep -v -e '^\[' -e '^  step'
  $PY $D/compare.py $sid $OUT/expected.csv $OUT/actual.csv $OUT/actual_log.csv $OUT/diff.md
  $PY $D/plot.py $OUT $LOG
  $PY $D/summary.py $OUT $LOG > $OUT/summary.md
  $PY analysis/instruments/common/separation.py $LOG > $OUT/separation.md
done
