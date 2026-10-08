# tf_demo: the demo-day round of T-F

A further round of T-F after T-F part 1, in its format (the run options, the result table, the figures, the comparison
report), for the statistics of Hadi's demo-day talk (Hadi, 8 October 2026). Test and analysis: no change to the
framework. Not T-F part 2 (parked) and not a baseline. The folder's name is ccode's, neutral; Hadi has not named the
round.

## What was decided (Hadi, 8 October 2026)

1. One layout, env_layout_100 (24 shelves on the four walls, kitting_table_0 north, kitting_table_1 south,
   coffee_machine_1, ac_switch_0, corner_SE); its notes rewritten to describe this room, no geometry changed.
2. Five setups, env_setup_100 to env_setup_104: shelf_k holds item_k; each destination drawn between the two tables; one
   timeline fact per setup, break_time over a window of 100 ticks, its start drawn.
3. Ten scenarios per setup, 50 in all: the robot 8 to 13 deliveries, the human 3 to 7, drawn, disjoint. Group a
   (_01, _02): the assigned deliveries only; group b (_03 to _06): plus one coffee break at a drawn place; group c
   (_07, _08) the mix: a switch mid-task, a coffee break, an unmodelled behaviour; (_09, _10) unmodelled behaviour only.
4. One recorded seed; ordinary files a person reads; every scenario passes the load-time check; generated and committed
   before the first run (8890ed9); no draw repeated or edited after a result; an invalid draw redrawn by a rule stated in
   advance.
5. Seven runs per scenario, 350: human-unaware (the stop off, R5); intention-unaware, intention-aware with context
   knowledge off, intention-aware with context knowledge on, each with the separation stop off and on. Fixed:
   single_task, min_separation 50 cm, θ at its default, assignment knowledge at its default (on), the step cap 2000; a
   run with no terminal decision within the cap is unfinished.
6. No setting in a file or folder name; the settings are columns of the result table, the separation stop included.

## The files

- `generate.py` — the draws (seed 20261008) and their rules, stated in its docstring before the first draw: the
  setups (`domains/kitting/setups/env_setup_100.json` to `_104.json`) and the scenarios
  (`domains/kitting/scenarios/scenarios_s100.py` to `_s104.py`). Each scenario's source is executed and built by the
  loader (the load-time replay and every load check) before the next draw; one draw was discarded by the redraw rule
  (scenario_s104_08's first draw: no free delivery entry for the misdelivery). Fixed by ccode, where the decisions are
  silent: the starts (the human at (5, 380) before kitting_table_0, the robot at (0, -380) before kitting_table_1); the
  window's start uniform on [0, 200]; a "place" between entries or inside a delivery at one of its three anchors; the
  switch mid-task is a change of mind to another of the human's deliveries (after the walk to the shelf or after the
  grasp); the unmodelled behaviours are a stand where the human is, a walk to corner_SE with a stand there (both
  TASK_ABSENT; 20 to 60 ticks) and a misdelivery to the other table (BINDING_ABSENT); "unmodelled only" holds two.
- `make_runs.py` — the 350 run files, `configs/kitting/tf_demo/<scenario>/run_NNN.yaml`, the seven conditions of a
  scenario consecutive (its docstring lists them).
- `stats.py` — the per-run measures (`runs/per_run.csv`), lead and stay per admission, the tables and the paired
  comparisons, the sentence rule, all stated in its docstring; writes `COMPARISON.md`.
- `COMPARISON.md` — the comparison report, generated.
- `runs/` (untracked, on Hadi's disk): one folder per scenario, the runs inside by serial; `results.csv` and
  `results.md` (the result table), `tags.csv` (the tag per task), `per_run.csv`; per run its log and record, the
  oracle's comparison where derivable, `measures.md` and `figure.png`.

## How to run

```bash
python analysis/kitting/tf_demo/generate.py          # only to check: it rewrites the committed files identically
python analysis/kitting/tf_demo/make_runs.py
analysis/instruments/mpb/run_set.sh kitting -s 2000 -o analysis/kitting/tf_demo/runs configs/kitting/tf_demo/*/run_*.yaml
python analysis/instruments/mpb/tag.py analysis/kitting/tf_demo/runs
python analysis/kitting/tf_demo/stats.py
```

The runner is sequential (each run's log is the newest in `logs/`). This round ran it in eight workers, each in its own
directory of symlinks to the repository with its own `logs/`; then `table.py` once over `runs/`. While the first
launch ran, another writer edited a scenario module of another setup in the working tree (scenarios_s31.py); a
half-saved state broke the registry's import and four workers stopped. The 132 runs complete by then were kept (their
inputs, the committed files, unchanged; the runs deterministic); the other 218 were run from a frozen copy of the
commit (`git archive` of 8890ed9; its shared/, world/, mesa_sim/ and this round's files equal to the working tree), each
over its own partial folder.
The generator and make_runs.py were checked afterwards: they rewrite the committed files byte-identically.

## The instruments, changed for this round

- `analysis/instruments/mpb/run_set.sh`: `-s <steps>`, one fixed cap for every run (decision 5); without it the
  domain's horizon.py as before.
- `analysis/instruments/mpb/table.py`: the columns `separation_stop` (the header's effective value) and `stop_ticks`
  (the run's `[stop]` lines).
