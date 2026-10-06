#!/usr/bin/env bash
# expect.sh <run file> — the expectations of one run before any run (T-K part 1, step 6; as step 5e's --expect): for a
# script independent of the robot, the human's replay (trajectory.py) and the oracle's per-tick table (mpb_oracle.py,
# theta the value of record, 0.75) at the run's step cap (horizon.py), into
# analysis/dock_loading/tk6/expectations/<scenario>/<run>/. A script that depends on the robot has none (MPB-DL3).
# run_set.sh writes the same two files beside the run; the README's md5s (expectations_md5.md) are checked against
# them after the runs. Parallel-safe (no simulation run). Usage: ls configs/dock_loading/tk6/*/*.yaml | xargs -P 10 -n 1 bash expect.sh
set -eo pipefail
RUN=$1; PY=~/python-envs/ir-nomesa-env/bin/python
name=$(basename $RUN .yaml); sid=$(awk '/^scenario:/ {print $2}' $RUN)
OUT=analysis/dock_loading/tk6/expectations/$sid/$name; mkdir -p $OUT
dep=$(PYTHONHASHSEED=0 $PY -c "import sys; sys.path[:0] = ['.', 'mesa_sim', 'analysis/instruments/mpb']; import conditions; print(conditions.dependence('$RUN'))")
[ "$dep" = on_robot ] && { rmdir $OUT; exit 0; }
steps=$(PYTHONHASHSEED=0 $PY analysis/dock_loading/mpb/horizon.py $RUN 2>/dev/null | tail -1)
PYTHONHASHSEED=0 $PY analysis/instruments/irb/trajectory.py $RUN $steps $OUT/trajectory.json > /dev/null 2>&1
PYTHONHASHSEED=0 $PY analysis/instruments/mpb/mpb_oracle.py $OUT/trajectory.json $RUN theta=0.75 $OUT/expected_ticks.json > /dev/null 2>&1
