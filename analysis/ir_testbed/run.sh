#!/usr/bin/env bash
# run.sh [scenario ids] — the IR test-bed (TB.3b): per scenario, the run (its run file in configs/ir_testbed/), the
# trajectory and its check against the run's human lines, the expectations, the actual outputs, the comparison and
# the figure. Outputs in analysis/ir_testbed/<scenario>/; the run's log and .rec in analysis/ir_testbed/runs/
# (git-ignored; md5s in README.md). PYTHONHASHSEED=0. Sequential: each run's log is picked up as the newest
# logs/run_*.log. Run from the repo root.
set -eo pipefail
PY=~/python-envs/ir-nomesa-env/bin/python; D=analysis/ir_testbed
IDS=${*:-"scenario_s08_01 scenario_s08_02 scenario_s08_03 scenario_s08_04"}
mkdir -p $D/runs
for sid in $IDS; do
  RUN=configs/ir_testbed/$sid.yaml; OUT=$D/$sid; LOG=$D/runs/env_layout_10_${sid}_on.log; mkdir -p $OUT
  steps=$(awk '/^steps:/ {print $2}' $RUN)
  PYTHONHASHSEED=0 $PY mesa_sim/run_mesa.py --run $RUN < /dev/null > /dev/null 2>&1
  cp "$(ls -t logs/run_*.log | head -1)" $LOG
  cp "$(ls -t logs/run_*.rec | head -1)" ${LOG%.log}.rec
  PYTHONHASHSEED=0 $PY $D/trajectory.py $sid $steps $OUT/trajectory.json $LOG 2>&1 | grep -v '^\['
  PYTHONHASHSEED=0 $PY $D/oracle.py $OUT/trajectory.json $RUN $OUT/expected.csv $OUT/phases.json
  PYTHONHASHSEED=0 $PY $D/actual.py $RUN $LOG $OUT/actual.csv $OUT/actual_log.csv 2>&1 | grep -v -e '^\[' -e '^  step'
  $PY $D/compare.py $sid $OUT/expected.csv $OUT/actual.csv $OUT/actual_log.csv $OUT/diff.md
  $PY $D/plot.py $OUT
done
