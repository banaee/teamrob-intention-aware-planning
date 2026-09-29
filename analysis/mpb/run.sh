#!/usr/bin/env bash
# run.sh [-o out_root] [--strategy single_task|full_reorder] [--prior on|off] [run files] — the meta-planner test-bed
# (MPB; design_decisions.md, "The meta-planner test-bed (MPB)"; analysis/mpb/README.md). Per run file (default: every
# configs/mpb/*.yaml): the safety cap (horizon.py, MPB-5) as the run's steps, the run, the trajectory and its check
# against the run's human lines (the IR test-bed's trajectory.py), the in-process actual and the log (actual.py); prior
# on also the oracle's per-tick table (mpb_oracle.py), the chain (chain.py) and the comparison (compare.py); the
# declared properties and the measures (properties.py); for the control, the reference run (reference.py); the figure
# and the summary. Outputs in <out_root>/<scenario>/<prior>_<strategy>/; the logs and .rec in <out_root>/runs/
# (git-ignored). PYTHONHASHSEED=0. Sequential: each run's log is the newest logs/run_*.log. Run from the repo root.
set -eo pipefail
PY=~/python-envs/ir-nomesa-env/bin/python; D=analysis/mpb; IR=analysis/ir_testbed; ROOT=$D
STRATEGY=single_task; PRIOR=on; RUNS=""
while [ $# -gt 0 ]; do
  case $1 in
    -o) ROOT=$2; shift 2;;
    --strategy) STRATEGY=$2; shift 2;;
    --prior) PRIOR=$2; shift 2;;
    *) RUNS="$RUNS $1"; shift;;
  esac
done
RUNS=${RUNS:-$(ls configs/mpb/*.yaml)}
[ "$PRIOR" = on ] && FLAG=true || FLAG=false
mkdir -p $ROOT/runs
for RUN in $RUNS; do
  sid=$(awk '/^scenario:/ {print $2}' $RUN); layout=$(awk '/^layout:/ {print $2}' $RUN)
  VAR=${PRIOR}_${STRATEGY}; OUT=$ROOT/$sid/$VAR; LOG=$ROOT/runs/${layout}_${sid}_${VAR}.log; mkdir -p $OUT
  steps=$(PYTHONHASHSEED=0 $PY $D/horizon.py $RUN 2>/dev/null | tail -1)
  last=$(PYTHONHASHSEED=0 $PY $IR/trajectory.py $RUN --length 2>/dev/null | tail -1)
  own=$(awk '/^steps:/ {print $2}' $RUN)
  [ "$own" = "$steps" ] || echo "$sid: notice: the run file's steps ($own) differ from the cap ($steps); run with $steps"
  PYTHONHASHSEED=0 $PY mesa_sim/run_mesa.py --run $RUN --steps $steps --strategy $STRATEGY --assignment_prior $FLAG \
    < /dev/null > /dev/null 2>&1
  cp "$(ls -t logs/run_*.log | head -1)" $LOG
  cp "$(ls -t logs/run_*.rec | head -1)" ${LOG%.log}.rec
  PYTHONHASHSEED=0 $PY $IR/trajectory.py $RUN $steps $OUT/trajectory.json $LOG 2>&1 | grep -v '^\['
  PYTHONHASHSEED=0 $PY $D/actual.py $RUN $steps $LOG $last $OUT --strategy $STRATEGY --assignment_prior $FLAG \
    2>&1 | grep -v -e '^\[' -e '^  step'
  if [ "$sid" = scenario_s10_06 ]; then
    PYTHONHASHSEED=0 $PY $D/reference.py $RUN $steps $ROOT/runs/${layout}_${sid}_reference_${STRATEGY}.log \
      $OUT/reference.json --strategy $STRATEGY 2>&1 | grep -v -e '^\[' -e '^  step'
  fi
  if [ "$PRIOR" = on ]; then
    if PYTHONHASHSEED=0 $PY $D/mpb_oracle.py $OUT/trajectory.json $RUN $LOG $OUT/expected_ticks.json; then
      $PY $D/chain.py $OUT/expected_ticks.json $OUT/observed.json $OUT/expected_decisions.json
      $PY $D/compare.py $sid $OUT
    fi
  fi
  PYTHONHASHSEED=0 $PY $D/properties.py $sid $OUT $LOG $RUN
  $PY $D/plot.py $sid $OUT
done
