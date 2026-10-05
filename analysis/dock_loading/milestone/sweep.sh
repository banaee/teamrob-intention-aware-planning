#!/usr/bin/env bash
# sweep.sh <out_dir> — dock_loading's six milestone runs (T-G stage 1, steps 6 to 8 and the second milestone scenario;
# design_records.md, "T-G: the second domain's rulings"): one simple scenario per room, two per room, headless, assignment
# knowledge on, context knowledge off (the regression sweeps' setting), single_task, gate none, cost realized, stop off;
# PYTHONHASHSEED=0. Each log is copied to <out_dir>/<layout id>_<scenario id>.log, its .rec beside it, and its per-tick
# figure drawn beside it (<...>.png; analysis/instruments/mpb/figure_of_log.py; the measurement of T-F part 1, O). Logs,
# .rec and figures are git-ignored. Sequential: each run's log is picked up as the newest logs/run_*.log. Run from the
# repo root.
set -e
OUT=$1; shift; PY=~/python-envs/ir-nomesa-env/bin/python; mkdir -p "$OUT"
RUNS="env_layout_02 scenario_s03_02 800
env_layout_03 scenario_s05_02 800
env_layout_04 scenario_s07_02 800
env_layout_02 scenario_s03_03 1000
env_layout_03 scenario_s05_03 1000
env_layout_04 scenario_s07_03 1000"
while read -r lay sc st; do
  tag=${lay}_${sc}
  PYTHONHASHSEED=0 $PY mesa_sim/run_mesa.py --domain dock_loading --layout "$lay" --scenario "$sc" --steps "$st" \
    --strategy single_task --cost_strategy realized --gate_strategy none --separation_stop false \
    --assignment_knowledge true --context_knowledge false < /dev/null > /dev/null 2>&1 || echo "$tag: exit $?"
  cp "$(ls -t logs/run_*.log | head -1)" "$OUT/$tag.log"
  cp "$(ls -t logs/run_*.rec | head -1)" "$OUT/$tag.rec"
  PYTHONHASHSEED=0 $PY analysis/instruments/mpb/figure_of_log.py "$OUT/$tag.log" "$OUT/$tag.png"
done <<< "$RUNS"
