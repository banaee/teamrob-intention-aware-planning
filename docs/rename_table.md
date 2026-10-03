# Rename table: old ids to the serial ids (T-L)

Every old layout, setup and scenario id and its id under ruling 4 as amended (`docs/design_decisions.md`, "Layouts,
setups and scenarios: the three artefacts of a run"; glossary §9). Setups got their ids in T-L stage 2, layouts and
scenarios in stage 3 (26 September 2026). A scenario's MM is its place in its setup's module (`scenarios_sNN.py`) as
it stood at stage 2, not the order of the old numbers.

The frozen analysis scripts and records (every `analysis/` folder but the four maintained sets, the frozen entries of
`docs/design_decisions.md`, closed TODOs, older README sections) stay frozen at their commit and keep the old ids;
this table maps them.

## kitting

### Layouts

| old | new |
|---|---|
| env_layout0 | env_layout_01 |
| env_layout1 | env_layout_02 |
| env_layout2 | env_layout_03 |
| env_layout3 | env_layout_04 |
| env_layout4 | env_layout_05 |
| env_layout5 | env_layout_06 |
| env_layout7 | env_layout_07 |
| env_layout8 | env_layout_08 |
| env_layout9 | env_layout_09 |

Not renamed, unregistered: `env_layout6.json` (with the retired scenario_60 / scenario_61) and `env_layout99.json`
(the old env_layout1 with obstacles), both at the domain root.

### Setups (stage 2)

| old | new |
|---|---|
| env_setup0 | env_setup_01 |
| env_setup3 | env_setup_01 (merged: content-identical to env_setup0) |
| env_setup1 | env_setup_02 |
| env_setup2 | env_setup_03 |
| env_setup5 | env_setup_03 (merged: content-identical to env_setup2) |
| env_setup4 | env_setup_04 |
| env_setup7 | env_setup_05 |
| env_setup8 | env_setup_06 |
| env_setup9 | env_setup_07 |

### Scenarios

| old | new | old | new |
|---|---|---|---|
| scenario_00 | scenario_s01_01 | scenario_40 | scenario_s04_01 |
| scenario_01 | scenario_s01_02 | scenario_41 | scenario_s04_02 |
| scenario_02 | scenario_s01_03 | scenario_42 | scenario_s04_03 |
| scenario_03 | scenario_s01_04 | scenario_70 | scenario_s05_01 |
| scenario_04 | scenario_s01_05 | scenario_71 | scenario_s05_02 |
| scenario_30 | scenario_s01_06 | scenario_72 | scenario_s05_03 |
| scenario_31 | scenario_s01_07 | scenario_73 | scenario_s05_04 |
| scenario_32 | scenario_s01_08 | scenario_80 | scenario_s06_01 |
| scenario_10 | scenario_s02_01 | scenario_81 | scenario_s06_02 |
| scenario_11 | scenario_s02_02 | scenario_83 | scenario_s06_03 |
| scenario_12 | scenario_s02_03 | scenario_82 | scenario_s06_04 |
| scenario_20 | scenario_s03_01 | scenario_84 | scenario_s06_05 |
| scenario_22 | scenario_s03_02 | scenario_85 | scenario_s06_06 |
| scenario_23 | scenario_s03_03 | scenario_90 | scenario_s07_01 |
| scenario_24 | scenario_s03_04 | scenario_91 | scenario_s07_02 |
| scenario_21 | scenario_s03_05 | scenario_92 | scenario_s07_03 |
| scenario_50 | scenario_s03_06 | scenario_93 | scenario_s07_04 |
| scenario_51 | scenario_s03_07 | scenario_94 | scenario_s07_05 |
| scenario_52 | scenario_s03_08 | | |
| scenario_53 | scenario_s03_09 | | |

Retired, no new id: scenario_60, scenario_61 (F47; `analysis/f47_fixtures/retired_scenarios_60_61.py`).

Short tags in the frozen records name a scenario by its old number (`s20`, `s70_off`, `s83_full_reorder_on`): read
them through the scenario table (`s20` = scenario_20 = scenario_s03_01).

## dock_loading

| old | new |
|---|---|
| env_layout1 | env_layout_01 |
| env_setup1 | env_setup_01 (stage 2) |
| scenario_10 | scenario_s01_01 |
| scenario_11 | scenario_s01_02 |

Note (1 October 2026, T-G stage 1, step 1): the dock_loading rows above name artefacts since removed. env_layout_01, env_setup_01
and build 1's scenarios (scenario_s01_01, scenario_s01_02) were replaced by stage 1's rooms (B14): env_layout_02 to
env_layout_04, env_setup_02 to env_setup_07 and the viewing fixtures scenario_s02_01 to scenario_s07_01. The rows stay as the
record of the T-L rename.

## The maintained baseline logs

Named `<layout id>_<scenario id>_<run options>.log` (ruling 6) from stage 3 on; the old condition tags map as:

| set | old tag | new name stem |
|---|---|---|
| tb1a | s00 | env_layout_01_scenario_s01_01 |
| tb1a | s10 | env_layout_02_scenario_s02_01 |
| tb1a | s20 | env_layout_03_scenario_s03_01 |
| tb1a | s30 | env_layout_04_scenario_s01_06 |
| tb1a | s40 | env_layout_05_scenario_s04_01 |
| tb1a | s50 | env_layout_06_scenario_s03_06 |
| tb1a | s70 | env_layout_07_scenario_s05_01 |
| tb1a | s71 | env_layout_07_scenario_s05_02 |
| tb1b, tb1c, tb3 | s80 | env_layout_08_scenario_s06_01 |
| tb1b, tb3 | s81 | env_layout_08_scenario_s06_02 |
| tb1c, tb3 | s83 | env_layout_08_scenario_s06_03 |
| tb3 | s20 | env_layout_03_scenario_s03_01 |
| tb3 | s70 | env_layout_07_scenario_s05_01 |

The option suffixes are unchanged (`_off` / `_on`; tb1c `_<cost>_<prior>`; tb3 `_<strategy>_<prior>`).

## Paths: the sort (1 October 2026)

The earlier analyses, the test-beds' run sets and the tests were sorted by domain before the IRB runs on
dock_loading (design_decisions.md, "T-G: the second domain's rulings", the step added before the IRB; the plan
approved by Hadi, 1 October 2026). No behaviour changed. Dated entries, frozen reports, the scenarios' descriptions, the
layouts' and setups' notes and the comments in `shared/` and `world/` keep the old paths; this table maps them. The
frozen scripts moved one folder down and do not run from the new place (their paths count folders up from their own);
they run at the commit their READMEs state, as every frozen record.

| old | new |
|---|---|
| `analysis/<folder>/` for each of: `ablation_task_committed`, `big_picture`, `c_separation_stop`, `d2_recognition_trigger`, `f1_foreseeable_fixture`, `f1_robot_responsible`, `f47_fixtures`, `g1_graded_evidence`, `i2_ir_foundations`, `i3_phase_model`, `i4_evidence_model`, `i4c_episode`, `i4d_fold_unknown`, `i5_handback`, `l_build`, `t1_conflict_measurement`, `t1b_realization`, `t6_ablation`, `t9_arrival_radius`, `tb1a_destination`, `tb1b_two_tables`, `tb1c_realized_flip`, `tb1d_designations`, `tb2b_exposed_interval`, `tb2c_per_entry_holds`, `tb3_full_reorder`, `tc2c_scripts`, `td_stage1`, `td_stage1b`, `todo90_b2a_window` | `analysis/kitting/<folder>/` (`tb2b_exposed_interval` is `analysis/kitting/irb2b_exposed_interval/` since 3 October 2026) |
| `analysis/ir_testbed/` `README.md`, `REPORT.md`, `scenario_s08_*/`, `scenario_s09_*/`, `runs/` | `analysis/kitting/irb/` (kitting's set) |
| `analysis/ir_testbed/` `trajectory.py`, `oracle.py`, `actual.py`, `compare.py`, `plot.py`, `summary.py`, `run.sh` | `analysis/instruments/irb/` (the shared code; `run.sh <domain> [-o root] [run files]`) |
| `analysis/mpb/` `README.md`, `REPORT.md`, `authoring.md`, `coverage.md`, `.gitignore`, `scenario_*/`, `runs/` | `analysis/kitting/mpb/` (kitting's set) |
| `analysis/mpb/` `properties.py`, `horizon.py`, `alteration.py` | `analysis/kitting/mpb/` (kitting-bound: the declared properties, the MPB-5 cap, the alterations) |
| `analysis/mpb/` `actual.py`, `chain.py`, `compare.py`, `mpblib.py`, `mpb_oracle.py`, `plot.py`, `plot_ir.py`, `reference.py`, `run.sh` | `analysis/instruments/mpb/` (the shared code; `run.sh <domain> ...`) |
| `analysis/logparse.py` | `analysis/instruments/common/logparse.py` |
| `analysis/tb1a_destination/sep_classes.py` | `analysis/instruments/common/sep_classes.py` |
| `analysis/l_build/tdlib.py` | `analysis/kitting/l_build/tdlib.py` (frozen); the instruments read a copy, `analysis/instruments/common/tdlib.py` |
| `configs/ir_testbed/` | `configs/kitting/irb/` |
| `configs/mpb/` | `configs/kitting/mpb/` |
| `tests/<file>` for each of: `test_executed_is_assessed.py`, `test_g_build.py`, `test_l_build.py`, `test_p_build.py`, `test_tb2b_cognitive_loop.py`, `test_td15_build.py`, `test_td1_adequacy.py`, `test_tg_liveness.py`, `test_tg_script.py`, `test_th1_tree.py`, `test_th2_executor.py`, `test_th4_queries.py`, `test_th_composition.py`, `test_tl1_artefacts.py`, `test_tl4_overrides.py` | `tests/kitting/<file>` (`test_tb2b_cognitive_loop.py` is `tests/kitting/test_irb2b_cognitive_loop.py` since 3 October 2026) |
| `tests/test_tg_dock_tasks.py`, `tests/test_tg_states.py` | `tests/dock_loading/` |
| `tests/test_mpb_instrument.py` | `tests/instruments/` |
| `tests/test_tg_areas.py`, `tests/test_th3_scenarios.py`, `tests/test_tl2_discovery.py`, `tests/tl2_fixture_dup/` | unchanged (both domains) |

Commands: `bash analysis/ir_testbed/run.sh ...` reads `bash analysis/instruments/irb/run.sh kitting ...`, and
`bash analysis/mpb/run.sh ...` reads `bash analysis/instruments/mpb/run.sh kitting ...`; a maintained set's
`bash analysis/<set>/sweep.sh <dir>` reads `bash analysis/kitting/<set>/sweep.sh <dir>`.
