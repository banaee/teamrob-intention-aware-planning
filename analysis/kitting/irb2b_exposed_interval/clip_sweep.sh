#!/usr/bin/env bash
# clip_sweep.sh — clip_ticks.py over the 17 prior-off conditions of analysis/td_stage1b/clip_ticks.txt, each at its
# sweep's step count (tb1a: s02_01 450, s04_01 400, s01_06 200, the rest 300; env_layout_08 340), the tb1a options
# otherwise. Run from the repo root (IRB.2b: at HEAD for clip_ticks.txt, and in a worktree at cecf5ec, before the
# build, for clip_ticks_pre.txt).
PY=~/python-envs/ir-nomesa-env/bin/python; S=analysis/irb2b_exposed_interval/clip_ticks.py
while read -r lay sc st opts; do
  echo "== $lay $sc $opts (prior off)"
  PYTHONHASHSEED=0 $PY $S "$st" --domain kitting --layout "$lay" --scenario "$sc" $opts --gate_strategy none \
    --separation_stop false --assignment_prior false
done <<'RUNS'
env_layout_01 scenario_s01_01 300 --cost_strategy realized
env_layout_02 scenario_s02_01 450 --cost_strategy realized
env_layout_03 scenario_s03_01 300 --cost_strategy realized
env_layout_04 scenario_s01_06 200 --cost_strategy realized
env_layout_05 scenario_s04_01 400 --cost_strategy realized
env_layout_06 scenario_s03_06 300 --cost_strategy realized
env_layout_07 scenario_s05_01 300 --cost_strategy realized
env_layout_07 scenario_s05_02 300 --cost_strategy realized
env_layout_08 scenario_s06_01 340 --cost_strategy realized
env_layout_08 scenario_s06_02 340 --cost_strategy realized
env_layout_08 scenario_s06_03 340 --strategy full_reorder --cost_strategy realized
env_layout_08 scenario_s06_03 340 --strategy full_reorder --cost_strategy plain
env_layout_08 scenario_s06_01 340 --strategy full_reorder --cost_strategy plain
env_layout_08 scenario_s06_02 340 --strategy full_reorder --cost_strategy realized
env_layout_08 scenario_s06_03 340 --strategy single_task --cost_strategy realized
env_layout_03 scenario_s03_01 300 --strategy full_reorder --cost_strategy realized
env_layout_07 scenario_s05_01 300 --strategy full_reorder --cost_strategy realized
RUNS
