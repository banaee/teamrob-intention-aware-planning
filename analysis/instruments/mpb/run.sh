#!/usr/bin/env bash
# run.sh <domain> [--expect] [-o out_root] [--strategy single_task|full_reorder] [--prior on|off] [run files] — the meta-planner
# test-bed (MPB; design_decisions.md, "The meta-planner test-bed (MPB)"; analysis/kitting/mpb/README.md). The code is
# shared by the domains since the sort (1 October 2026); horizon.py and properties.py are the domain's, in
# analysis/<domain>/mpb/ (with CONTROLS, the control scenarios whose reference run is made, and alteration.py). Per run file (default: every configs/<domain>/mpb/*.yaml): the safety cap (horizon.py, MPB-5) as the run's steps, the run, the trajectory and its check
# against the run's human lines (the IRB's trajectory.py), the in-process actual and the log (actual.py); prior
# on also the oracle's per-tick table (mpb_oracle.py), the chain (chain.py) and the comparison (compare.py); the
# declared properties and the measures (properties.py); for the control, the reference run (reference.py); the figure
# and the summary; every run, its one figure (plot.py, figure.png: the recognition, the decisions and the distance on one tick
# axis; with no oracle table the actual alone; the measurement of T-F part 1, N). Outputs in <out_root>/<scenario>/<prior>_<strategy>/; the logs and .rec in <out_root>/runs/
# (git-ignored). PYTHONHASHSEED=0. Sequential: each run's log is the newest logs/run_*.log. Run from the repo root.
set -eo pipefail
DOMAIN=$1; shift
PY=~/python-envs/ir-nomesa-env/bin/python; D=analysis/instruments/mpb; IR=analysis/instruments/irb
DOM=analysis/$DOMAIN/mpb; ROOT=$DOM
STRATEGY=single_task; PRIOR=on; RUNS=""; EXPECT=""
while [ $# -gt 0 ]; do
  case $1 in
    -o) ROOT=$2; shift 2;;
    --strategy) STRATEGY=$2; shift 2;;
    --prior) PRIOR=$2; shift 2;;
    --expect) EXPECT=1; shift;;
    *) RUNS="$RUNS $1"; shift;;
  esac
done
RUNS=${RUNS:-$(ls configs/$DOMAIN/mpb/*.yaml)}
[ "$PRIOR" = on ] && FLAG=true || FLAG=false
mkdir -p $ROOT/runs
for RUN in $RUNS; do
  sid=$(awk '/^scenario:/ {print $2}' $RUN); layout=$(awk '/^layout:/ {print $2}' $RUN)
  VAR=${PRIOR}_${STRATEGY}; OUT=$ROOT/$sid/$VAR; LOG=$ROOT/runs/${layout}_${sid}_${VAR}.log; mkdir -p $OUT
  steps=$(PYTHONHASHSEED=0 $PY $DOM/horizon.py $RUN 2>/dev/null | tail -1)
  last=$(PYTHONHASHSEED=0 $PY $IR/trajectory.py $RUN --length 2>/dev/null | tail -1)
  # a script declared dependent on the robot (T-G A3, Q13b): no expectations before the run (MPB-DL3: declared
  # properties only); the replay with an idle robot does not describe its run, so neither the trajectory check, the
  # oracle nor the compare is made, and the human's last acknowledgement is the run's own (its human lines)
  dep=$(PYTHONHASHSEED=0 $PY -c "import sys; sys.path[:0] = ['$IR', '.']; import yaml, trajectory as t; \
c = yaml.safe_load(open('$RUN')); sc = t.domain_of('$RUN')['scenarios'][c['scenario']]; \
print(next(a for a in sc.agents if a.agent_type == 'human').scheduled_tasks.dependence.value)" 2>/dev/null)
  own=$(awk '/^steps:/ {print $2}' $RUN)
  [ "$own" = "$steps" ] || echo "$sid: notice: the run file's steps ($own) differ from the cap ($steps); run with $steps"
  if [ -n "$EXPECT" ]; then
    [ "$dep" = on_robot ] && { echo "$sid: depends on the robot: no expectations before the run (MPB-DL3)"; continue; }
    # the expectations before any run: the trajectory and the oracle's per-tick table, theta the value of record (the
    # [run] header's theta=0.75, DEFAULT_THETA); the run's own oracle call must reproduce them byte for byte
    PYTHONHASHSEED=0 $PY $IR/trajectory.py $RUN $steps $OUT/trajectory.json 2>&1 | grep -v '^\['
    PYTHONHASHSEED=0 $PY $D/mpb_oracle.py $OUT/trajectory.json $RUN theta=0.75 $OUT/expected_ticks.json
    continue
  fi
  PYTHONHASHSEED=0 $PY mesa_sim/run_mesa.py --run $RUN --steps $steps --strategy $STRATEGY --assignment_knowledge $FLAG \
    < /dev/null > /dev/null 2>&1
  cp "$(ls -t logs/run_*.log | head -1)" $LOG
  cp "$(ls -t logs/run_*.rec | head -1)" ${LOG%.log}.rec
  if [ "$dep" = on_robot ]; then
    PYTHONHASHSEED=0 $PY $IR/trajectory.py $RUN $steps $OUT/trajectory.json 2>&1 | grep -v '^\['
    hid=$(awk '/^\s*step: [0-9]+: \[human/ {print $3; exit}' $LOG)
    last=$(awk -v h="$hid" '/^\s*step: [0-9]+: / && $3 == h && $5 != "action=None" {t = $2} END {sub(":", "", t); print t}' $LOG)
  else
    PYTHONHASHSEED=0 $PY $IR/trajectory.py $RUN $steps $OUT/trajectory.json $LOG 2>&1 | grep -v '^\['
  fi
  PYTHONHASHSEED=0 $PY $D/actual.py $RUN $steps $LOG $last $OUT --strategy $STRATEGY --assignment_knowledge $FLAG \
    2>&1 | grep -v -e '^\[' -e '^  step'
  if PYTHONHASHSEED=0 $PY -c "import sys; sys.path[:0] = ['$DOM', '.']; import properties; sys.exit(0 if '$sid' in properties.CONTROLS else 1)" 2>/dev/null; then   # the domain's control scenarios
    PYTHONHASHSEED=0 $PY $D/reference.py $RUN $steps $ROOT/runs/${layout}_${sid}_reference_${STRATEGY}.log \
      $OUT/reference.json --strategy $STRATEGY 2>&1 | grep -v -e '^\[' -e '^  step'
  fi
  if [ "$PRIOR" = on ] && [ "$dep" != on_robot ]; then
    if PYTHONHASHSEED=0 $PY $D/mpb_oracle.py $OUT/trajectory.json $RUN $LOG $OUT/expected_ticks.json; then
      if $PY $D/chain.py $OUT/expected_ticks.json $OUT/observed.json $OUT/expected_decisions.json; then
        $PY $D/compare.py $sid $OUT
      else
        echo "$sid: no chain and no comparison of decisions (D3: an undetermined gate at a decision)"
      fi
    fi
  fi
  PYTHONHASHSEED=0 $PY $DOM/properties.py $sid $OUT $LOG $RUN
  $PY $D/plot.py $sid $OUT $LOG   # the run's one figure (N); with no oracle table the actual alone
  $PY analysis/instruments/common/separation.py $LOG > $OUT/separation.md          # since the sort
done
