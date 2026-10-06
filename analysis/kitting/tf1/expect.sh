#!/usr/bin/env bash
# expect.sh <run file> — the expectations of one run of the measurement extended by full_reorder, before any of those
# runs (Hadi, 6 October 2026; design_records.md, "T-F part 1", THE MEASUREMENT EXTENDED BY FULL_REORDER): the human's
# replay (trajectory.py) and the oracle's per-tick table (mpb_oracle.py, theta the value of record, 0.75) at the run's
# step cap (kitting's horizon.py), into analysis/kitting/tf1/expectations/<scenario>/<run>/. run_set.sh writes the same
# two files beside the run; expectations_md5.md's md5s are checked against them after the runs. Parallel-safe (no
# simulation run). Usage: <run files> | xargs -P 11 -n 1 bash analysis/kitting/tf1/expect.sh
set -eo pipefail
RUN=$1; PY=~/python-envs/ir-nomesa-env/bin/python
name=$(basename $RUN .yaml); sid=$(awk '/^scenario:/ {print $2}' $RUN)
OUT=analysis/kitting/tf1/expectations/$sid/$name; mkdir -p $OUT
steps=$(PYTHONHASHSEED=0 $PY analysis/kitting/mpb/horizon.py $RUN 2>/dev/null | tail -1)
PYTHONHASHSEED=0 $PY analysis/instruments/irb/trajectory.py $RUN $steps $OUT/trajectory.json > /dev/null 2>&1
PYTHONHASHSEED=0 $PY analysis/instruments/mpb/mpb_oracle.py $OUT/trajectory.json $RUN theta=0.75 $OUT/expected_ticks.json > /dev/null 2>&1
