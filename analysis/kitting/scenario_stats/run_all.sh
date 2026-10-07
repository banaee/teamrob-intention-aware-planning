#!/bin/bash
# analysis/kitting/scenario_stats/run_all.sh <out dir> [workers] [scenario prefix]
# Every kitting scenario of the registry run once: intention-aware, assignment and context knowledge on, single_task,
# gate none, cost realized, stop off, test level 0.05, the scenario's first reference layout, the steps the MPB's
# safety cap (analysis/kitting/mpb/horizon.py). Out: <out dir>/yaml/<scenario>.yaml and <out dir>/runs/<scenario>.log
# and .rec. A run resolves its paths against the working directory and names its log pair by the second, so each
# worker runs in its own directory under <out dir>/work, linked to the repository except logs/. Not a baseline.
set -e
ROOT=$(cd "$(dirname "$0")/../../.." && pwd)
OUT=$(mkdir -p "$1" && cd "$1" && pwd); N=${2:-10}; PREFIX=${3:-scenario_}
PY=~/python-envs/ir-nomesa-env/bin/python
mkdir -p $OUT/yaml $OUT/runs
cd $ROOT && PYTHONHASHSEED=0 $PY - "$OUT/yaml" "$PREFIX" <<'PYEOF'
import sys; sys.path.insert(0, '.')
from domains.kitting.registry import domain_config
out, prefix = sys.argv[1], sys.argv[2]
for sid, sc in domain_config['scenarios'].items():
    if not sid.startswith(prefix): continue
    open(f"{out}/{sid}.yaml", "w").write(
        f"domain: kitting\nlayout: {sc.reference_layouts[0]}\nsetup: {sc.setup}\nscenario: {sid}\nsteps: 100\n"
        "human_aware: true\nintention_aware: true\nassignment_knowledge: true\ncontext_knowledge: true\n"
        "strategy: single_task\ngate_strategy: none\ncost_strategy: realized\nseparation_stop: false\ntest_level: 0.05\n")
PYEOF
run_one() {  # <run file> <worker dir>
  local y=$1 W=$2 sid; sid=$(basename $y .yaml)
  cd $W
  local cap; cap=$(PYTHONHASHSEED=0 $PY analysis/kitting/mpb/horizon.py $y 2>/dev/null | tail -1)
  PYTHONHASHSEED=0 $PY mesa_sim/run_mesa.py --run $y --steps $cap </dev/null >/dev/null 2>&1 && rc=0 || rc=$?
  local l; l=$(ls -t logs/*.log | head -1); mv $l $OUT/runs/$sid.log; mv ${l%.log}.rec $OUT/runs/$sid.rec
  echo "$sid $cap $rc"
}
ls $OUT/yaml/${PREFIX}*.yaml | sort > $OUT/list.txt
for w in $(seq 0 $((N - 1))); do
  mkdir -p $OUT/work/$w/logs
  for e in "$ROOT"/*; do b=$(basename "$e"); [ "$b" = logs ] || ln -sfn "$e" "$OUT/work/$w/$b"; done
  (awk -v n=$N -v w=$w 'NR % n == w' $OUT/list.txt | while read y; do run_one $y $OUT/work/$w; done > $OUT/done_$w.txt) &
done
wait
cat $OUT/done_*.txt | awk '{n++} $3 != 0 {f++} END {print n " runs, " f + 0 " failed"}'
