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
