# T-F part 1, the measurement: what recognition adds to planning (kitting)

Written by ccode, 5 October 2026. The measurement of T-F part 1 (R10, H; the rulings K to O of 5 October 2026,
design_records.md, "T-F part 1", THE MEASUREMENT). Scenarios are test material: a result that looks bad is a finding,
not a reason to change anything. Nothing below is ruled, and no claim goes beyond the tables.

## What was run

- Four conditions on the same scenarios, all `single_task`, assignment knowledge as the condition leaves it (on where
  the recognizer runs): human-unaware (HU), intention-unaware (IU), intention-aware with context knowledge off (IA-off)
  and on (IA-on).
- 128 scenarios in all four: the planning test-bed's 16 (scenario_s10_01 to s12_02), step 5's 6 (scenario_s16_01 to
  _06; _02, _04 and _06 are the copies of _01, _03 and _05 with a timeline, run in all four as L names them), step 5e's
  106 in the form with no timeline fact. Step 5e's 176 copies with a timeline: IA-on only. 688 runs.
- Run files: `configs/kitting/tf1/measurement/<scenario>/run_NNN.yaml` (written by `make_runs.py`; the four
  conditions of a scenario consecutive, HU, IU, IA-off, IA-on). Outputs: `measurement/<scenario>/run_NNN/`, the log
  and `.rec` inside, the figure `figure.png` (N). The result table: `measurement/results.csv` and `results.md`
  (`analysis/instruments/mpb/table.py`), one row per run, the effective settings as columns. The tables below:
  `tables.py`.
- Command, per run file: `analysis/instruments/mpb/run_set.sh kitting -o analysis/kitting/tf1/measurement <run files>`
  (run through ten copies of the tree at 3d7a26a in parallel, each sequential, the outputs written here).
- Declared properties not checked (M). The oracle on every row where it applies.

Four example figures, one scenario in the four conditions (scenario_s05_01; finding 5):
`measurement/scenario_s05_01/run_105/figure.png` (HU), `run_106` (IU), `run_107` (IA-off), `run_108` (IA-on).

## The check

- The oracle compared on all 688 rows: 0 disagreements (per tick, decisions, log). Every row's header settings agree
  with R5's reading of its run file. Every human-unaware row (128) equals the robot-alone reference run on every
  compared tick (the objects separate in all 128).
- Step 5's timeline copies equal their bases in HU, IU and IA-off (scenario_s16_02 = _01, _04 = _03, _06 = _05, every
  measure): a timeline acts only through context knowledge.

## The measures

Completion is the world tick after the robot's last release, counted only where the pool completed (a terminal
decision); "-" the pool not completed within the cap. "below": the ticks whose continuous `[sep]` minimum lies below
min_separation (50 cm), by F1's class: viol, recede (a moving robot), passing, beside (a standing robot, the human
passing or beside it). A pair's counts: the scenarios in which the second condition is better / equal / worse than the
first (earlier completion; fewer ticks).

Rows 688; the oracle compared on 688 (0 disagreements); none derivable on 0; settings disagreeing with R5's reading: 0; human-unaware rows against the reference run: equal 128.

## the planning test-bed (16)

### human-unaware (HU): 16 runs, completed within the cap 16, held ticks 0, ticks below min_separation 46 (viol 23, recede 15, passing 0, beside 8), scenarios with a tick below 6

| scenario | run | completion | held | below | viol | recede | passing | beside | sep_min | decisions | oracle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| scenario_s10_01 | run_001 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 383.99 | 5 | 0 |
| scenario_s10_02 | run_005 | 61 | 0 | 4 | 3 | 1 | 0 | 0 | 18.54 | 2 | 0 |
| scenario_s10_03 | run_009 | 172 | 0 | 0 | 0 | 0 | 0 | 0 | 408.88 | 5 | 0 |
| scenario_s10_04 | run_013 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 383.99 | 5 | 0 |
| scenario_s10_05 | run_017 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 383.99 | 5 | 0 |
| scenario_s10_06 | run_021 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 349.00 | 5 | 0 |
| scenario_s10_07 | run_025 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 405.43 | 5 | 0 |
| scenario_s10_08 | run_029 | 167 | 0 | 0 | 0 | 0 | 0 | 0 | 316.43 | 5 | 0 |
| scenario_s10_09 | run_033 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 387.55 | 5 | 0 |
| scenario_s10_10 | run_037 | 171 | 0 | 0 | 0 | 0 | 0 | 0 | 352.81 | 5 | 0 |
| scenario_s10_11 | run_041 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 411.19 | 5 | 0 |
| scenario_s11_01 | run_045 | 48 | 0 | 9 | 2 | 3 | 0 | 4 | 11.33 | 3 | 0 |
| scenario_s11_02 | run_049 | 103 | 0 | 14 | 9 | 5 | 0 | 0 | 21.16 | 3 | 0 |
| scenario_s11_03 | run_053 | 35 | 0 | 9 | 2 | 3 | 0 | 4 | 11.33 | 3 | 0 |
| scenario_s12_01 | run_057 | 124 | 0 | 4 | 3 | 1 | 0 | 0 | 18.54 | 3 | 0 |
| scenario_s12_02 | run_061 | 136 | 0 | 6 | 4 | 2 | 0 | 0 | 25.29 | 3 | 0 |

### intention-unaware (IU): 16 runs, completed within the cap 16, held ticks 214, ticks below min_separation 6 (viol 0, recede 0, passing 6, beside 0), scenarios with a tick below 1

| scenario | run | completion | held | below | viol | recede | passing | beside | sep_min | decisions | oracle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| scenario_s10_01 | run_002 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 383.99 | 25 | 0 |
| scenario_s10_02 | run_006 | 66 | 5 | 0 | 0 | 0 | 0 | 0 | 52.20 | 12 | 0 |
| scenario_s10_03 | run_010 | 172 | 0 | 0 | 0 | 0 | 0 | 0 | 408.88 | 24 | 0 |
| scenario_s10_04 | run_014 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 383.99 | 21 | 0 |
| scenario_s10_05 | run_018 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 383.99 | 26 | 0 |
| scenario_s10_06 | run_022 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 349.00 | 21 | 0 |
| scenario_s10_07 | run_026 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 405.43 | 23 | 0 |
| scenario_s10_08 | run_030 | 167 | 0 | 0 | 0 | 0 | 0 | 0 | 316.43 | 26 | 0 |
| scenario_s10_09 | run_034 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 387.55 | 24 | 0 |
| scenario_s10_10 | run_038 | 171 | 0 | 0 | 0 | 0 | 0 | 0 | 352.81 | 25 | 0 |
| scenario_s10_11 | run_042 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 411.19 | 26 | 0 |
| scenario_s11_01 | run_046 | 74 | 23 | 0 | 0 | 0 | 0 | 0 | 66.15 | 8 | 0 |
| scenario_s11_02 | run_050 | 169 | 66 | 0 | 0 | 0 | 0 | 0 | 50.44 | 20 | 0 |
| scenario_s11_03 | run_054 | 113 | 62 | 0 | 0 | 0 | 0 | 0 | 51.33 | 8 | 0 |
| scenario_s12_01 | run_058 | 134 | 10 | 0 | 0 | 0 | 0 | 0 | 52.20 | 23 | 0 |
| scenario_s12_02 | run_062 | 184 | 48 | 6 | 0 | 0 | 6 | 0 | 12.16 | 26 | 0 |

### intention-aware, context knowledge off (IA-off): 16 runs, completed within the cap 16, held ticks 204, ticks below min_separation 4 (viol 1, recede 1, passing 2, beside 0), scenarios with a tick below 1

| scenario | run | completion | held | below | viol | recede | passing | beside | sep_min | decisions | oracle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| scenario_s10_01 | run_003 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 383.99 | 16 | 0 |
| scenario_s10_02 | run_007 | 66 | 5 | 0 | 0 | 0 | 0 | 0 | 52.20 | 8 | 0 |
| scenario_s10_03 | run_011 | 172 | 0 | 0 | 0 | 0 | 0 | 0 | 408.88 | 17 | 0 |
| scenario_s10_04 | run_015 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 383.99 | 15 | 0 |
| scenario_s10_05 | run_019 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 383.99 | 16 | 0 |
| scenario_s10_06 | run_023 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 349.00 | 15 | 0 |
| scenario_s10_07 | run_027 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 405.43 | 17 | 0 |
| scenario_s10_08 | run_031 | 167 | 0 | 0 | 0 | 0 | 0 | 0 | 316.43 | 17 | 0 |
| scenario_s10_09 | run_035 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 387.55 | 17 | 0 |
| scenario_s10_10 | run_039 | 171 | 0 | 0 | 0 | 0 | 0 | 0 | 352.81 | 17 | 0 |
| scenario_s10_11 | run_043 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 411.19 | 17 | 0 |
| scenario_s11_01 | run_047 | 74 | 23 | 0 | 0 | 0 | 0 | 0 | 66.15 | 8 | 0 |
| scenario_s11_02 | run_051 | 169 | 66 | 0 | 0 | 0 | 0 | 0 | 50.44 | 20 | 0 |
| scenario_s11_03 | run_055 | 113 | 62 | 0 | 0 | 0 | 0 | 0 | 51.33 | 8 | 0 |
| scenario_s12_01 | run_059 | 131 | 0 | 0 | 0 | 0 | 0 | 0 | 87.57 | 13 | 0 |
| scenario_s12_02 | run_063 | 161 | 48 | 4 | 1 | 1 | 2 | 0 | 32.26 | 14 | 0 |

### intention-aware, context knowledge on (IA-on): 16 runs, completed within the cap 16, held ticks 210, ticks below min_separation 4 (viol 0, recede 1, passing 3, beside 0), scenarios with a tick below 1

| scenario | run | completion | held | below | viol | recede | passing | beside | sep_min | decisions | oracle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| scenario_s10_01 | run_004 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 383.99 | 13 | 0 |
| scenario_s10_02 | run_008 | 66 | 5 | 0 | 0 | 0 | 0 | 0 | 52.20 | 7 | 0 |
| scenario_s10_03 | run_012 | 172 | 0 | 0 | 0 | 0 | 0 | 0 | 408.88 | 16 | 0 |
| scenario_s10_04 | run_016 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 383.99 | 15 | 0 |
| scenario_s10_05 | run_020 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 383.99 | 13 | 0 |
| scenario_s10_06 | run_024 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 349.00 | 12 | 0 |
| scenario_s10_07 | run_028 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 405.43 | 14 | 0 |
| scenario_s10_08 | run_032 | 167 | 0 | 0 | 0 | 0 | 0 | 0 | 316.43 | 12 | 0 |
| scenario_s10_09 | run_036 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 387.55 | 14 | 0 |
| scenario_s10_10 | run_040 | 171 | 0 | 0 | 0 | 0 | 0 | 0 | 352.81 | 13 | 0 |
| scenario_s10_11 | run_044 | 161 | 0 | 0 | 0 | 0 | 0 | 0 | 411.19 | 17 | 0 |
| scenario_s11_01 | run_048 | 74 | 23 | 0 | 0 | 0 | 0 | 0 | 66.15 | 8 | 0 |
| scenario_s11_02 | run_052 | 169 | 66 | 0 | 0 | 0 | 0 | 0 | 50.44 | 20 | 0 |
| scenario_s11_03 | run_056 | 113 | 62 | 0 | 0 | 0 | 0 | 0 | 51.33 | 8 | 0 |
| scenario_s12_01 | run_060 | 130 | 0 | 0 | 0 | 0 | 0 | 0 | 72.14 | 9 | 0 |
| scenario_s12_02 | run_064 | 162 | 54 | 4 | 0 | 1 | 3 | 0 | 33.61 | 14 | 0 |

### Pairs of conditions (the second against the first): scenarios better / equal / worse

| first | second | completion | ticks below min_separation | viol ticks |
|---|---|---|---|---|
| HU | IU | 0 / 10 / 6 | 5 / 11 / 0 | 6 / 10 / 0 |
| HU | IA-off | 0 / 10 / 6 | 6 / 10 / 0 | 6 / 10 / 0 |
| HU | IA-on | 0 / 10 / 6 | 6 / 10 / 0 | 6 / 10 / 0 |
| IU | IA-off | 2 / 14 / 0 | 1 / 15 / 0 | 0 / 15 / 1 |
| IU | IA-on | 2 / 14 / 0 | 1 / 15 / 0 | 0 / 16 / 0 |
| IA-off | IA-on | 1 / 14 / 1 | 0 / 16 / 0 | 1 / 15 / 0 |

## step 5's planning cases (6)

### human-unaware (HU): 6 runs, completed within the cap 6, held ticks 0, ticks below min_separation 36 (viol 22, recede 14, passing 0, beside 0), scenarios with a tick below 6

| scenario | run | completion | held | below | viol | recede | passing | beside | sep_min | decisions | oracle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| scenario_s16_01 | run_065 | 63 | 0 | 6 | 4 | 2 | 0 | 0 | 10.19 | 2 | 0 |
| scenario_s16_02 | run_069 | 63 | 0 | 6 | 4 | 2 | 0 | 0 | 10.19 | 2 | 0 |
| scenario_s16_03 | run_073 | 57 | 0 | 6 | 3 | 3 | 0 | 0 | 11.55 | 2 | 0 |
| scenario_s16_04 | run_077 | 57 | 0 | 6 | 3 | 3 | 0 | 0 | 11.55 | 2 | 0 |
| scenario_s16_05 | run_081 | 101 | 0 | 6 | 4 | 2 | 0 | 0 | 28.33 | 2 | 0 |
| scenario_s16_06 | run_085 | 101 | 0 | 6 | 4 | 2 | 0 | 0 | 28.33 | 2 | 0 |

### intention-unaware (IU): 6 runs, completed within the cap 6, held ticks 144, ticks below min_separation 14 (viol 2, recede 0, passing 6, beside 6), scenarios with a tick below 2

| scenario | run | completion | held | below | viol | recede | passing | beside | sep_min | decisions | oracle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| scenario_s16_01 | run_066 | 69 | 6 | 7 | 1 | 0 | 3 | 3 | 36.95 | 11 | 0 |
| scenario_s16_02 | run_070 | 69 | 6 | 7 | 1 | 0 | 3 | 3 | 36.95 | 11 | 0 |
| scenario_s16_03 | run_074 | 118 | 61 | 0 | 0 | 0 | 0 | 0 | 55.51 | 13 | 0 |
| scenario_s16_04 | run_078 | 118 | 61 | 0 | 0 | 0 | 0 | 0 | 55.51 | 13 | 0 |
| scenario_s16_05 | run_082 | 106 | 5 | 0 | 0 | 0 | 0 | 0 | 60.39 | 17 | 0 |
| scenario_s16_06 | run_086 | 106 | 5 | 0 | 0 | 0 | 0 | 0 | 60.39 | 17 | 0 |

### intention-aware, context knowledge off (IA-off): 6 runs, completed within the cap 6, held ticks 144, ticks below min_separation 14 (viol 2, recede 0, passing 6, beside 6), scenarios with a tick below 2

| scenario | run | completion | held | below | viol | recede | passing | beside | sep_min | decisions | oracle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| scenario_s16_01 | run_067 | 69 | 6 | 7 | 1 | 0 | 3 | 3 | 36.95 | 8 | 0 |
| scenario_s16_02 | run_071 | 69 | 6 | 7 | 1 | 0 | 3 | 3 | 36.95 | 8 | 0 |
| scenario_s16_03 | run_075 | 113 | 61 | 0 | 0 | 0 | 0 | 0 | 59.53 | 9 | 0 |
| scenario_s16_04 | run_079 | 113 | 61 | 0 | 0 | 0 | 0 | 0 | 59.53 | 9 | 0 |
| scenario_s16_05 | run_083 | 106 | 5 | 0 | 0 | 0 | 0 | 0 | 60.39 | 15 | 0 |
| scenario_s16_06 | run_087 | 106 | 5 | 0 | 0 | 0 | 0 | 0 | 60.39 | 15 | 0 |

### intention-aware, context knowledge on (IA-on): 6 runs, completed within the cap 6, held ticks 159, ticks below min_separation 6 (viol 4, recede 2, passing 0, beside 0), scenarios with a tick below 2

| scenario | run | completion | held | below | viol | recede | passing | beside | sep_min | decisions | oracle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| scenario_s16_01 | run_068 | 68 | 5 | 3 | 2 | 1 | 0 | 0 | 41.66 | 2 | 0 |
| scenario_s16_02 | run_072 | 67 | 4 | 3 | 2 | 1 | 0 | 0 | 29.33 | 7 | 0 |
| scenario_s16_03 | run_076 | 89 | 79 | 0 | 0 | 0 | 0 | 0 | 55.51 | 12 | 0 |
| scenario_s16_04 | run_080 | 91 | 61 | 0 | 0 | 0 | 0 | 0 | 68.48 | 8 | 0 |
| scenario_s16_05 | run_084 | 106 | 5 | 0 | 0 | 0 | 0 | 0 | 60.39 | 11 | 0 |
| scenario_s16_06 | run_088 | 106 | 5 | 0 | 0 | 0 | 0 | 0 | 60.39 | 11 | 0 |

### Pairs of conditions (the second against the first): scenarios better / equal / worse

| first | second | completion | ticks below min_separation | viol ticks |
|---|---|---|---|---|
| HU | IU | 0 / 0 / 6 | 4 / 0 / 2 | 6 / 0 / 0 |
| HU | IA-off | 0 / 0 / 6 | 4 / 0 / 2 | 6 / 0 / 0 |
| HU | IA-on | 0 / 0 / 6 | 6 / 0 / 0 | 6 / 0 / 0 |
| IU | IA-off | 2 / 4 / 0 | 0 / 6 / 0 | 0 / 6 / 0 |
| IU | IA-on | 4 / 2 / 0 | 2 / 4 / 0 | 0 / 4 / 2 |
| IA-off | IA-on | 4 / 2 / 0 | 2 / 4 / 0 | 0 / 4 / 2 |

## step 5e's planning scenarios, no timeline (106)

### human-unaware (HU): 106 runs, completed within the cap 106, held ticks 0, ticks below min_separation 779 (viol 92, recede 52, passing 204, beside 431), scenarios with a tick below 56

| scenario | run | completion | held | below | viol | recede | passing | beside | sep_min | decisions | oracle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| scenario_s02_01 | run_089 | 422 | 0 | 7 | 0 | 3 | 2 | 2 | 30.87 | 5 | 0 |
| scenario_s02_02 | run_093 | 422 | 0 | 297 | 6 | 3 | 0 | 288 | 6.97 | 5 | 0 |
| scenario_s03_06 | run_097 | 229 | 0 | 11 | 5 | 2 | 2 | 2 | 9.02 | 4 | 0 |
| scenario_s04_01 | run_101 | 379 | 0 | 0 | 0 | 0 | 0 | 0 | 59.89 | 4 | 0 |
| scenario_s05_01 | run_105 | 171 | 0 | 10 | 6 | 4 | 0 | 0 | 30.00 | 3 | 0 |
| scenario_s05_02 | run_109 | 172 | 0 | 10 | 6 | 4 | 0 | 0 | 30.00 | 3 | 0 |
| scenario_s17_12 | run_113 | 279 | 0 | 5 | 0 | 0 | 2 | 3 | 40.58 | 4 | 0 |
| scenario_s17_18 | run_117 | 305 | 0 | 0 | 0 | 0 | 0 | 0 | 86.67 | 4 | 0 |
| scenario_s17_24 | run_121 | 289 | 0 | 11 | 7 | 4 | 0 | 0 | 1.14 | 4 | 0 |
| scenario_s17_30 | run_125 | 326 | 0 | 0 | 0 | 0 | 0 | 0 | 66.46 | 4 | 0 |
| scenario_s17_36 | run_129 | 332 | 0 | 0 | 0 | 0 | 0 | 0 | 124.64 | 4 | 0 |
| scenario_s18_02 | run_133 | 340 | 0 | 6 | 2 | 0 | 2 | 2 | 23.55 | 4 | 0 |
| scenario_s18_08 | run_137 | 331 | 0 | 0 | 0 | 0 | 0 | 0 | 234.61 | 4 | 0 |
| scenario_s18_14 | run_141 | 310 | 0 | 0 | 0 | 0 | 0 | 0 | 317.41 | 4 | 0 |
| scenario_s18_20 | run_145 | 337 | 0 | 0 | 0 | 0 | 0 | 0 | 144.23 | 4 | 0 |
| scenario_s18_26 | run_149 | 362 | 0 | 2 | 2 | 0 | 0 | 0 | 45.21 | 4 | 0 |
| scenario_s19_07 | run_153 | 379 | 0 | 0 | 0 | 0 | 0 | 0 | 73.31 | 4 | 0 |
| scenario_s19_13 | run_157 | 379 | 0 | 6 | 3 | 3 | 0 | 0 | 23.51 | 4 | 0 |
| scenario_s19_19 | run_161 | 282 | 0 | 8 | 0 | 0 | 5 | 3 | 28.78 | 4 | 0 |
| scenario_s19_25 | run_165 | 379 | 0 | 0 | 0 | 0 | 0 | 0 | 142.83 | 4 | 0 |
| scenario_s19_31 | run_169 | 282 | 0 | 0 | 0 | 0 | 0 | 0 | 164.51 | 4 | 0 |
| scenario_s20_02 | run_173 | 253 | 0 | 10 | 1 | 0 | 6 | 3 | 12.44 | 4 | 0 |
| scenario_s20_08 | run_177 | 272 | 0 | 4 | 3 | 1 | 0 | 0 | 15.39 | 4 | 0 |
| scenario_s20_14 | run_181 | 276 | 0 | 8 | 0 | 0 | 5 | 3 | 12.43 | 4 | 0 |
| scenario_s20_20 | run_185 | 271 | 0 | 0 | 0 | 0 | 0 | 0 | 122.13 | 4 | 0 |
| scenario_s20_26 | run_189 | 281 | 0 | 12 | 2 | 1 | 6 | 3 | 8.97 | 4 | 0 |
| scenario_s21_07 | run_193 | 229 | 0 | 14 | 7 | 3 | 2 | 2 | 9.02 | 4 | 0 |
| scenario_s21_11 | run_197 | 229 | 0 | 0 | 0 | 0 | 0 | 0 | 73.19 | 4 | 0 |
| scenario_s21_17 | run_201 | 229 | 0 | 0 | 0 | 0 | 0 | 0 | 145.59 | 4 | 0 |
| scenario_s21_23 | run_205 | 201 | 0 | 6 | 1 | 3 | 2 | 0 | 11.45 | 4 | 0 |
| scenario_s21_29 | run_209 | 229 | 0 | 0 | 0 | 0 | 0 | 0 | 98.09 | 4 | 0 |
| scenario_s22_02 | run_213 | 118 | 0 | 15 | 0 | 0 | 9 | 6 | 12.13 | 3 | 0 |
| scenario_s22_06 | run_217 | 118 | 0 | 13 | 0 | 0 | 10 | 3 | 12.00 | 3 | 0 |
| scenario_s22_12 | run_221 | 131 | 0 | 17 | 4 | 4 | 6 | 3 | 9.85 | 3 | 0 |
| scenario_s22_18 | run_225 | 118 | 0 | 35 | 0 | 0 | 11 | 24 | 6.27 | 3 | 0 |
| scenario_s22_24 | run_229 | 125 | 0 | 11 | 3 | 1 | 4 | 3 | 5.38 | 3 | 0 |
| scenario_s23_09 | run_233 | 171 | 0 | 3 | 2 | 1 | 0 | 0 | 28.28 | 3 | 0 |
| scenario_s23_15 | run_237 | 171 | 0 | 8 | 0 | 0 | 5 | 3 | 14.81 | 3 | 0 |
| scenario_s23_21 | run_241 | 172 | 0 | 5 | 0 | 0 | 2 | 3 | 45.73 | 3 | 0 |
| scenario_s23_27 | run_245 | 171 | 0 | 0 | 0 | 0 | 0 | 0 | 392.09 | 3 | 0 |
| scenario_s23_31 | run_249 | 172 | 0 | 5 | 0 | 0 | 2 | 3 | 41.41 | 3 | 0 |
| scenario_s24_02 | run_253 | 244 | 0 | 7 | 4 | 3 | 0 | 0 | 0.00 | 4 | 0 |
| scenario_s24_08 | run_257 | 244 | 0 | 10 | 8 | 0 | 2 | 0 | 4.68 | 4 | 0 |
| scenario_s24_14 | run_261 | 261 | 0 | 16 | 6 | 5 | 2 | 3 | 0.08 | 4 | 0 |
| scenario_s24_20 | run_265 | 261 | 0 | 7 | 0 | 0 | 4 | 3 | 26.57 | 4 | 0 |
| scenario_s24_26 | run_269 | 261 | 0 | 6 | 3 | 3 | 0 | 0 | 0.06 | 4 | 0 |
| scenario_s25_02 | run_273 | 122 | 0 | 7 | 0 | 0 | 4 | 3 | 40.29 | 3 | 0 |
| scenario_s25_06 | run_277 | 58 | 0 | 9 | 0 | 0 | 6 | 3 | 13.18 | 3 | 0 |
| scenario_s25_10 | run_281 | 150 | 0 | 2 | 2 | 0 | 0 | 0 | 44.31 | 3 | 0 |
| scenario_s25_16 | run_285 | 97 | 0 | 4 | 2 | 0 | 2 | 0 | 23.72 | 3 | 0 |
| scenario_s25_22 | run_289 | 74 | 0 | 7 | 0 | 0 | 4 | 3 | 31.60 | 3 | 0 |
| scenario_s25_28 | run_293 | 145 | 0 | 0 | 0 | 0 | 0 | 0 | 246.62 | 3 | 0 |
| scenario_s25_34 | run_297 | 150 | 0 | 14 | 0 | 0 | 11 | 3 | 8.03 | 3 | 0 |
| scenario_s25_40 | run_301 | 122 | 0 | 0 | 0 | 0 | 0 | 0 | 215.68 | 3 | 0 |
| scenario_s25_44 | run_305 | 111 | 0 | 6 | 0 | 0 | 3 | 3 | 41.05 | 3 | 0 |
| scenario_s25_50 | run_309 | 87 | 0 | 6 | 0 | 0 | 3 | 3 | 37.53 | 3 | 0 |
| scenario_s26_02 | run_313 | 232 | 0 | 0 | 0 | 0 | 0 | 0 | 308.68 | 3 | 0 |
| scenario_s26_06 | run_317 | 162 | 0 | 17 | 0 | 0 | 11 | 6 | 2.67 | 3 | 0 |
| scenario_s26_10 | run_321 | 271 | 0 | 0 | 0 | 0 | 0 | 0 | 52.77 | 3 | 0 |
| scenario_s26_16 | run_325 | 277 | 0 | 15 | 3 | 1 | 8 | 3 | 8.39 | 3 | 0 |
| scenario_s26_22 | run_329 | 250 | 0 | 9 | 0 | 0 | 6 | 3 | 11.25 | 3 | 0 |
| scenario_s26_28 | run_333 | 272 | 0 | 0 | 0 | 0 | 0 | 0 | 111.20 | 3 | 0 |
| scenario_s26_32 | run_337 | 272 | 0 | 2 | 1 | 1 | 0 | 0 | 45.75 | 3 | 0 |
| scenario_s26_38 | run_341 | 214 | 0 | 0 | 0 | 0 | 0 | 0 | 471.78 | 3 | 0 |
| scenario_s26_42 | run_345 | 267 | 0 | 9 | 0 | 0 | 6 | 3 | 0.25 | 3 | 0 |
| scenario_s26_48 | run_349 | 239 | 0 | 11 | 1 | 1 | 6 | 3 | 3.58 | 3 | 0 |
| scenario_s27_02 | run_353 | 86 | 0 | 0 | 0 | 0 | 0 | 0 | 378.96 | 3 | 0 |
| scenario_s27_06 | run_357 | 74 | 0 | 0 | 0 | 0 | 0 | 0 | 1045.56 | 3 | 0 |
| scenario_s27_10 | run_361 | 151 | 0 | 7 | 0 | 0 | 4 | 3 | 25.63 | 3 | 0 |
| scenario_s27_14 | run_365 | 97 | 0 | 7 | 0 | 0 | 4 | 3 | 39.98 | 3 | 0 |
| scenario_s27_20 | run_369 | 65 | 0 | 8 | 0 | 0 | 5 | 3 | 20.88 | 3 | 0 |
| scenario_s27_26 | run_373 | 118 | 0 | 0 | 0 | 0 | 0 | 0 | 948.68 | 3 | 0 |
| scenario_s27_30 | run_377 | 116 | 0 | 0 | 0 | 0 | 0 | 0 | 141.88 | 3 | 0 |
| scenario_s27_36 | run_381 | 116 | 0 | 0 | 0 | 0 | 0 | 0 | 119.53 | 3 | 0 |
| scenario_s27_42 | run_385 | 100 | 0 | 0 | 0 | 0 | 0 | 0 | 87.99 | 3 | 0 |
| scenario_s27_44 | run_389 | 59 | 0 | 0 | 0 | 0 | 0 | 0 | 1012.12 | 3 | 0 |
| scenario_s28_02 | run_393 | 288 | 0 | 3 | 2 | 1 | 0 | 0 | 43.60 | 4 | 0 |
| scenario_s28_06 | run_397 | 107 | 0 | 0 | 0 | 0 | 0 | 0 | 710.19 | 3 | 0 |
| scenario_s28_10 | run_401 | 98 | 0 | 5 | 0 | 0 | 2 | 3 | 35.42 | 3 | 0 |
| scenario_s28_16 | run_405 | 211 | 0 | 0 | 0 | 0 | 0 | 0 | 196.87 | 3 | 0 |
| scenario_s28_22 | run_409 | 171 | 0 | 0 | 0 | 0 | 0 | 0 | 199.99 | 3 | 0 |
| scenario_s28_28 | run_413 | 101 | 0 | 8 | 0 | 0 | 5 | 3 | 17.86 | 3 | 0 |
| scenario_s28_32 | run_417 | 143 | 0 | 7 | 0 | 0 | 4 | 3 | 30.12 | 3 | 0 |
| scenario_s28_38 | run_421 | 178 | 0 | 0 | 0 | 0 | 0 | 0 | 890.68 | 3 | 0 |
| scenario_s28_42 | run_425 | 250 | 0 | 0 | 0 | 0 | 0 | 0 | 55.02 | 3 | 0 |
| scenario_s28_48 | run_429 | 93 | 0 | 0 | 0 | 0 | 0 | 0 | 267.60 | 3 | 0 |
| scenario_s29_02 | run_433 | 167 | 0 | 0 | 0 | 0 | 0 | 0 | 329.53 | 3 | 0 |
| scenario_s29_06 | run_437 | 242 | 0 | 0 | 0 | 0 | 0 | 0 | 185.81 | 3 | 0 |
| scenario_s29_10 | run_441 | 219 | 0 | 0 | 0 | 0 | 0 | 0 | 72.05 | 3 | 0 |
| scenario_s29_16 | run_445 | 209 | 0 | 0 | 0 | 0 | 0 | 0 | 167.83 | 3 | 0 |
| scenario_s29_22 | run_449 | 256 | 0 | 0 | 0 | 0 | 0 | 0 | 332.24 | 3 | 0 |
| scenario_s29_28 | run_453 | 160 | 0 | 0 | 0 | 0 | 0 | 0 | 646.71 | 3 | 0 |
| scenario_s29_34 | run_457 | 182 | 0 | 0 | 0 | 0 | 0 | 0 | 696.04 | 3 | 0 |
| scenario_s29_40 | run_461 | 184 | 0 | 7 | 0 | 0 | 4 | 3 | 24.32 | 3 | 0 |
| scenario_s29_44 | run_465 | 214 | 0 | 0 | 0 | 0 | 0 | 0 | 90.99 | 3 | 0 |
| scenario_s29_48 | run_469 | 267 | 0 | 0 | 0 | 0 | 0 | 0 | 226.90 | 3 | 0 |
| scenario_s30_02 | run_473 | 101 | 0 | 0 | 0 | 0 | 0 | 0 | 1367.57 | 3 | 0 |
| scenario_s30_06 | run_477 | 145 | 0 | 9 | 0 | 0 | 6 | 3 | 3.99 | 3 | 0 |
| scenario_s30_10 | run_481 | 151 | 0 | 0 | 0 | 0 | 0 | 0 | 603.01 | 3 | 0 |
| scenario_s30_16 | run_485 | 162 | 0 | 7 | 0 | 0 | 4 | 3 | 26.57 | 3 | 0 |
| scenario_s30_22 | run_489 | 92 | 0 | 0 | 0 | 0 | 0 | 0 | 926.69 | 3 | 0 |
| scenario_s30_28 | run_493 | 149 | 0 | 0 | 0 | 0 | 0 | 0 | 262.69 | 3 | 0 |
| scenario_s30_34 | run_497 | 154 | 0 | 0 | 0 | 0 | 0 | 0 | 1334.76 | 3 | 0 |
| scenario_s30_38 | run_501 | 151 | 0 | 0 | 0 | 0 | 0 | 0 | 514.55 | 3 | 0 |
| scenario_s30_42 | run_505 | 92 | 0 | 0 | 0 | 0 | 0 | 0 | 697.37 | 3 | 0 |
| scenario_s30_46 | run_509 | 107 | 0 | 8 | 0 | 0 | 5 | 3 | 20.46 | 3 | 0 |

### intention-unaware (IU): 106 runs, completed within the cap 105, held ticks 797, ticks below min_separation 412 (viol 12, recede 23, passing 229, beside 148), scenarios with a tick below 47

| scenario | run | completion | held | below | viol | recede | passing | beside | sep_min | decisions | oracle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| scenario_s02_01 | run_090 | 422 | 0 | 7 | 0 | 3 | 2 | 2 | 30.87 | 43 | 0 |
| scenario_s02_02 | run_094 | - | 478 | 0 | 0 | 0 | 0 | 0 | 60.28 | 35 | 0 |
| scenario_s03_06 | run_098 | 239 | 10 | 0 | 0 | 0 | 0 | 0 | 53.80 | 31 | 0 |
| scenario_s04_01 | run_102 | 379 | 0 | 0 | 0 | 0 | 0 | 0 | 59.89 | 41 | 0 |
| scenario_s05_01 | run_106 | 216 | 29 | 0 | 0 | 0 | 0 | 0 | 58.31 | 23 | 0 |
| scenario_s05_02 | run_110 | 233 | 61 | 0 | 0 | 0 | 0 | 0 | 50.00 | 23 | 0 |
| scenario_s17_12 | run_114 | 279 | 0 | 5 | 0 | 0 | 2 | 3 | 40.58 | 36 | 0 |
| scenario_s17_18 | run_118 | 305 | 0 | 0 | 0 | 0 | 0 | 0 | 86.67 | 37 | 0 |
| scenario_s17_24 | run_122 | 297 | 8 | 5 | 0 | 1 | 4 | 0 | 7.88 | 35 | 0 |
| scenario_s17_30 | run_126 | 326 | 0 | 0 | 0 | 0 | 0 | 0 | 66.46 | 39 | 0 |
| scenario_s17_36 | run_130 | 332 | 0 | 0 | 0 | 0 | 0 | 0 | 124.64 | 27 | 0 |
| scenario_s18_02 | run_134 | 340 | 0 | 6 | 2 | 0 | 2 | 2 | 23.55 | 44 | 0 |
| scenario_s18_08 | run_138 | 331 | 0 | 0 | 0 | 0 | 0 | 0 | 234.61 | 39 | 0 |
| scenario_s18_14 | run_142 | 310 | 0 | 0 | 0 | 0 | 0 | 0 | 317.41 | 36 | 0 |
| scenario_s18_20 | run_146 | 337 | 0 | 0 | 0 | 0 | 0 | 0 | 144.23 | 31 | 0 |
| scenario_s18_26 | run_150 | 363 | 1 | 2 | 1 | 1 | 0 | 0 | 45.98 | 37 | 0 |
| scenario_s19_07 | run_154 | 379 | 0 | 0 | 0 | 0 | 0 | 0 | 73.31 | 37 | 0 |
| scenario_s19_13 | run_158 | 404 | 25 | 8 | 2 | 4 | 2 | 0 | 2.22 | 42 | 0 |
| scenario_s19_19 | run_162 | 282 | 0 | 8 | 0 | 0 | 5 | 3 | 28.78 | 31 | 0 |
| scenario_s19_25 | run_166 | 379 | 0 | 0 | 0 | 0 | 0 | 0 | 142.83 | 45 | 0 |
| scenario_s19_31 | run_170 | 282 | 0 | 0 | 0 | 0 | 0 | 0 | 164.51 | 23 | 0 |
| scenario_s20_02 | run_174 | 253 | 0 | 10 | 1 | 0 | 6 | 3 | 12.44 | 29 | 0 |
| scenario_s20_08 | run_178 | 275 | 0 | 0 | 0 | 0 | 0 | 0 | 61.97 | 35 | 0 |
| scenario_s20_14 | run_182 | 276 | 0 | 8 | 0 | 0 | 5 | 3 | 12.43 | 30 | 0 |
| scenario_s20_20 | run_186 | 271 | 0 | 0 | 0 | 0 | 0 | 0 | 122.13 | 30 | 0 |
| scenario_s20_26 | run_190 | 294 | 13 | 16 | 0 | 0 | 10 | 6 | 8.97 | 30 | 0 |
| scenario_s21_07 | run_194 | 248 | 19 | 4 | 0 | 1 | 3 | 0 | 35.84 | 33 | 0 |
| scenario_s21_11 | run_198 | 229 | 0 | 0 | 0 | 0 | 0 | 0 | 73.19 | 32 | 0 |
| scenario_s21_17 | run_202 | 229 | 0 | 0 | 0 | 0 | 0 | 0 | 145.59 | 37 | 0 |
| scenario_s21_23 | run_206 | 201 | 0 | 6 | 1 | 3 | 2 | 0 | 11.45 | 28 | 0 |
| scenario_s21_29 | run_210 | 230 | 1 | 0 | 0 | 0 | 0 | 0 | 115.76 | 36 | 0 |
| scenario_s22_02 | run_214 | 118 | 0 | 15 | 0 | 0 | 9 | 6 | 12.13 | 20 | 0 |
| scenario_s22_06 | run_218 | 118 | 0 | 13 | 0 | 0 | 10 | 3 | 12.00 | 17 | 0 |
| scenario_s22_12 | run_222 | 134 | 3 | 9 | 0 | 0 | 6 | 3 | 9.85 | 17 | 0 |
| scenario_s22_18 | run_226 | 118 | 0 | 35 | 0 | 0 | 11 | 24 | 6.27 | 21 | 0 |
| scenario_s22_24 | run_230 | 128 | 3 | 12 | 1 | 1 | 7 | 3 | 2.84 | 20 | 0 |
| scenario_s23_09 | run_234 | 173 | 2 | 0 | 0 | 0 | 0 | 0 | 56.57 | 27 | 0 |
| scenario_s23_15 | run_238 | 171 | 0 | 8 | 0 | 0 | 5 | 3 | 14.81 | 26 | 0 |
| scenario_s23_21 | run_242 | 172 | 0 | 5 | 0 | 0 | 2 | 3 | 45.73 | 23 | 0 |
| scenario_s23_27 | run_246 | 171 | 0 | 0 | 0 | 0 | 0 | 0 | 392.09 | 21 | 0 |
| scenario_s23_31 | run_250 | 172 | 0 | 5 | 0 | 0 | 2 | 3 | 41.41 | 18 | 0 |
| scenario_s24_02 | run_254 | 283 | 39 | 13 | 0 | 3 | 7 | 3 | 11.53 | 36 | 0 |
| scenario_s24_08 | run_258 | 251 | 7 | 5 | 1 | 1 | 3 | 0 | 4.13 | 35 | 0 |
| scenario_s24_14 | run_262 | 310 | 36 | 5 | 0 | 0 | 2 | 3 | 35.18 | 35 | 0 |
| scenario_s24_20 | run_266 | 261 | 0 | 7 | 0 | 0 | 4 | 3 | 26.57 | 27 | 0 |
| scenario_s24_26 | run_270 | 285 | 11 | 0 | 0 | 0 | 0 | 0 | 52.78 | 33 | 0 |
| scenario_s25_02 | run_274 | 122 | 0 | 7 | 0 | 0 | 4 | 3 | 40.29 | 14 | 0 |
| scenario_s25_06 | run_278 | 58 | 0 | 9 | 0 | 0 | 6 | 3 | 13.18 | 15 | 0 |
| scenario_s25_10 | run_282 | 151 | 1 | 1 | 1 | 0 | 0 | 0 | 48.13 | 21 | 0 |
| scenario_s25_16 | run_286 | 102 | 5 | 0 | 0 | 0 | 0 | 0 | 61.63 | 14 | 0 |
| scenario_s25_22 | run_290 | 74 | 0 | 7 | 0 | 0 | 4 | 3 | 31.60 | 11 | 0 |
| scenario_s25_28 | run_294 | 145 | 0 | 0 | 0 | 0 | 0 | 0 | 246.62 | 22 | 0 |
| scenario_s25_34 | run_298 | 150 | 0 | 14 | 0 | 0 | 11 | 3 | 8.03 | 17 | 0 |
| scenario_s25_40 | run_302 | 122 | 0 | 0 | 0 | 0 | 0 | 0 | 215.68 | 17 | 0 |
| scenario_s25_44 | run_306 | 111 | 0 | 6 | 0 | 0 | 3 | 3 | 41.05 | 15 | 0 |
| scenario_s25_50 | run_310 | 87 | 0 | 6 | 0 | 0 | 3 | 3 | 37.53 | 15 | 0 |
| scenario_s26_02 | run_314 | 232 | 0 | 0 | 0 | 0 | 0 | 0 | 308.68 | 23 | 0 |
| scenario_s26_06 | run_318 | 162 | 0 | 17 | 0 | 0 | 11 | 6 | 2.67 | 20 | 0 |
| scenario_s26_10 | run_322 | 271 | 0 | 0 | 0 | 0 | 0 | 0 | 52.77 | 34 | 0 |
| scenario_s26_16 | run_326 | 287 | 10 | 16 | 1 | 0 | 9 | 6 | 8.39 | 34 | 0 |
| scenario_s26_22 | run_330 | 250 | 0 | 9 | 0 | 0 | 6 | 3 | 11.25 | 28 | 0 |
| scenario_s26_28 | run_334 | 272 | 0 | 0 | 0 | 0 | 0 | 0 | 111.20 | 31 | 0 |
| scenario_s26_32 | run_338 | 273 | 1 | 0 | 0 | 0 | 0 | 0 | 54.54 | 26 | 0 |
| scenario_s26_38 | run_342 | 214 | 0 | 0 | 0 | 0 | 0 | 0 | 471.78 | 27 | 0 |
| scenario_s26_42 | run_346 | 267 | 0 | 9 | 0 | 0 | 6 | 3 | 0.25 | 31 | 0 |
| scenario_s26_48 | run_350 | 245 | 6 | 14 | 0 | 2 | 9 | 3 | 3.58 | 27 | 0 |
| scenario_s27_02 | run_354 | 86 | 0 | 0 | 0 | 0 | 0 | 0 | 378.96 | 16 | 0 |
| scenario_s27_06 | run_358 | 74 | 0 | 0 | 0 | 0 | 0 | 0 | 1045.56 | 17 | 0 |
| scenario_s27_10 | run_362 | 151 | 0 | 7 | 0 | 0 | 4 | 3 | 25.63 | 20 | 0 |
| scenario_s27_14 | run_366 | 97 | 0 | 7 | 0 | 0 | 4 | 3 | 39.98 | 17 | 0 |
| scenario_s27_20 | run_370 | 65 | 0 | 8 | 0 | 0 | 5 | 3 | 20.88 | 12 | 0 |
| scenario_s27_26 | run_374 | 118 | 0 | 0 | 0 | 0 | 0 | 0 | 948.68 | 15 | 0 |
| scenario_s27_30 | run_378 | 116 | 0 | 0 | 0 | 0 | 0 | 0 | 141.88 | 15 | 0 |
| scenario_s27_36 | run_382 | 116 | 0 | 0 | 0 | 0 | 0 | 0 | 119.53 | 22 | 0 |
| scenario_s27_42 | run_386 | 100 | 0 | 0 | 0 | 0 | 0 | 0 | 87.99 | 13 | 0 |
| scenario_s27_44 | run_390 | 59 | 0 | 0 | 0 | 0 | 0 | 0 | 1012.12 | 8 | 0 |
| scenario_s28_02 | run_394 | 292 | 4 | 7 | 1 | 3 | 3 | 0 | 2.54 | 34 | 0 |
| scenario_s28_06 | run_398 | 107 | 0 | 0 | 0 | 0 | 0 | 0 | 710.19 | 13 | 0 |
| scenario_s28_10 | run_402 | 98 | 0 | 5 | 0 | 0 | 2 | 3 | 35.42 | 13 | 0 |
| scenario_s28_16 | run_406 | 211 | 0 | 0 | 0 | 0 | 0 | 0 | 196.87 | 29 | 0 |
| scenario_s28_22 | run_410 | 171 | 0 | 0 | 0 | 0 | 0 | 0 | 199.99 | 23 | 0 |
| scenario_s28_28 | run_414 | 101 | 0 | 8 | 0 | 0 | 5 | 3 | 17.86 | 15 | 0 |
| scenario_s28_32 | run_418 | 143 | 0 | 7 | 0 | 0 | 4 | 3 | 30.12 | 17 | 0 |
| scenario_s28_38 | run_422 | 178 | 0 | 0 | 0 | 0 | 0 | 0 | 890.68 | 23 | 0 |
| scenario_s28_42 | run_426 | 250 | 0 | 0 | 0 | 0 | 0 | 0 | 55.02 | 33 | 0 |
| scenario_s28_48 | run_430 | 93 | 0 | 0 | 0 | 0 | 0 | 0 | 267.60 | 16 | 0 |
| scenario_s29_02 | run_434 | 167 | 0 | 0 | 0 | 0 | 0 | 0 | 329.53 | 22 | 0 |
| scenario_s29_06 | run_438 | 242 | 0 | 0 | 0 | 0 | 0 | 0 | 185.81 | 28 | 0 |
| scenario_s29_10 | run_442 | 219 | 0 | 0 | 0 | 0 | 0 | 0 | 72.05 | 23 | 0 |
| scenario_s29_16 | run_446 | 233 | 24 | 0 | 0 | 0 | 0 | 0 | 207.48 | 27 | 0 |
| scenario_s29_22 | run_450 | 256 | 0 | 0 | 0 | 0 | 0 | 0 | 332.24 | 29 | 0 |
| scenario_s29_28 | run_454 | 160 | 0 | 0 | 0 | 0 | 0 | 0 | 646.71 | 15 | 0 |
| scenario_s29_34 | run_458 | 182 | 0 | 0 | 0 | 0 | 0 | 0 | 696.04 | 22 | 0 |
| scenario_s29_40 | run_462 | 184 | 0 | 7 | 0 | 0 | 4 | 3 | 24.32 | 25 | 0 |
| scenario_s29_44 | run_466 | 214 | 0 | 0 | 0 | 0 | 0 | 0 | 90.99 | 29 | 0 |
| scenario_s29_48 | run_470 | 267 | 0 | 0 | 0 | 0 | 0 | 0 | 226.90 | 31 | 0 |
| scenario_s30_02 | run_474 | 101 | 0 | 0 | 0 | 0 | 0 | 0 | 1367.57 | 24 | 0 |
| scenario_s30_06 | run_478 | 145 | 0 | 9 | 0 | 0 | 6 | 3 | 3.99 | 19 | 0 |
| scenario_s30_10 | run_482 | 151 | 0 | 0 | 0 | 0 | 0 | 0 | 603.01 | 19 | 0 |
| scenario_s30_16 | run_486 | 162 | 0 | 7 | 0 | 0 | 4 | 3 | 26.57 | 21 | 0 |
| scenario_s30_22 | run_490 | 92 | 0 | 0 | 0 | 0 | 0 | 0 | 926.69 | 14 | 0 |
| scenario_s30_28 | run_494 | 149 | 0 | 0 | 0 | 0 | 0 | 0 | 262.69 | 21 | 0 |
| scenario_s30_34 | run_498 | 154 | 0 | 0 | 0 | 0 | 0 | 0 | 1334.76 | 15 | 0 |
| scenario_s30_38 | run_502 | 151 | 0 | 0 | 0 | 0 | 0 | 0 | 514.55 | 22 | 0 |
| scenario_s30_42 | run_506 | 92 | 0 | 0 | 0 | 0 | 0 | 0 | 697.37 | 14 | 0 |
| scenario_s30_46 | run_510 | 107 | 0 | 8 | 0 | 0 | 5 | 3 | 20.46 | 14 | 0 |

### intention-aware, context knowledge off (IA-off): 106 runs, completed within the cap 105, held ticks 1067, ticks below min_separation 406 (viol 14, recede 20, passing 227, beside 145), scenarios with a tick below 46

| scenario | run | completion | held | below | viol | recede | passing | beside | sep_min | decisions | oracle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| scenario_s02_01 | run_091 | 422 | 0 | 7 | 0 | 3 | 2 | 2 | 30.87 | 31 | 0 |
| scenario_s02_02 | run_095 | - | 734 | 0 | 0 | 0 | 0 | 0 | 60.28 | 24 | 0 |
| scenario_s03_06 | run_099 | 237 | 8 | 2 | 1 | 1 | 0 | 0 | 48.25 | 14 | 0 |
| scenario_s04_01 | run_103 | 379 | 0 | 0 | 0 | 0 | 0 | 0 | 59.89 | 25 | 0 |
| scenario_s05_01 | run_107 | 194 | 13 | 0 | 0 | 0 | 0 | 0 | 58.31 | 22 | 0 |
| scenario_s05_02 | run_111 | 214 | 78 | 0 | 0 | 0 | 0 | 0 | 50.00 | 22 | 0 |
| scenario_s17_12 | run_115 | 279 | 0 | 5 | 0 | 0 | 2 | 3 | 40.58 | 18 | 0 |
| scenario_s17_18 | run_119 | 305 | 0 | 0 | 0 | 0 | 0 | 0 | 86.67 | 23 | 0 |
| scenario_s17_24 | run_123 | 299 | 10 | 5 | 0 | 1 | 4 | 0 | 9.74 | 22 | 0 |
| scenario_s17_30 | run_127 | 326 | 0 | 0 | 0 | 0 | 0 | 0 | 66.46 | 26 | 0 |
| scenario_s17_36 | run_131 | 332 | 0 | 0 | 0 | 0 | 0 | 0 | 124.64 | 22 | 0 |
| scenario_s18_02 | run_135 | 340 | 0 | 6 | 2 | 0 | 2 | 2 | 23.55 | 29 | 0 |
| scenario_s18_08 | run_139 | 331 | 0 | 0 | 0 | 0 | 0 | 0 | 234.61 | 30 | 0 |
| scenario_s18_14 | run_143 | 310 | 0 | 0 | 0 | 0 | 0 | 0 | 317.41 | 28 | 0 |
| scenario_s18_20 | run_147 | 337 | 0 | 0 | 0 | 0 | 0 | 0 | 144.23 | 28 | 0 |
| scenario_s18_26 | run_151 | 369 | 7 | 0 | 0 | 0 | 0 | 0 | 50.61 | 26 | 0 |
| scenario_s19_07 | run_155 | 379 | 0 | 0 | 0 | 0 | 0 | 0 | 73.31 | 25 | 0 |
| scenario_s19_13 | run_159 | 405 | 28 | 8 | 1 | 3 | 3 | 1 | 2.22 | 31 | 0 |
| scenario_s19_19 | run_163 | 282 | 0 | 8 | 0 | 0 | 5 | 3 | 28.78 | 16 | 0 |
| scenario_s19_25 | run_167 | 379 | 0 | 0 | 0 | 0 | 0 | 0 | 142.83 | 30 | 0 |
| scenario_s19_31 | run_171 | 282 | 0 | 0 | 0 | 0 | 0 | 0 | 164.51 | 22 | 0 |
| scenario_s20_02 | run_175 | 254 | 1 | 9 | 0 | 0 | 6 | 3 | 12.44 | 17 | 0 |
| scenario_s20_08 | run_179 | 275 | 0 | 0 | 0 | 0 | 0 | 0 | 61.97 | 19 | 0 |
| scenario_s20_14 | run_183 | 276 | 0 | 8 | 0 | 0 | 5 | 3 | 12.43 | 17 | 0 |
| scenario_s20_20 | run_187 | 271 | 0 | 0 | 0 | 0 | 0 | 0 | 122.13 | 18 | 0 |
| scenario_s20_26 | run_191 | 292 | 13 | 16 | 1 | 1 | 8 | 6 | 8.97 | 23 | 0 |
| scenario_s21_07 | run_195 | 240 | 11 | 6 | 1 | 2 | 3 | 0 | 33.85 | 21 | 0 |
| scenario_s21_11 | run_199 | 229 | 0 | 0 | 0 | 0 | 0 | 0 | 73.19 | 18 | 0 |
| scenario_s21_17 | run_203 | 229 | 0 | 0 | 0 | 0 | 0 | 0 | 145.59 | 25 | 0 |
| scenario_s21_23 | run_207 | 201 | 0 | 6 | 1 | 3 | 2 | 0 | 11.45 | 21 | 0 |
| scenario_s21_29 | run_211 | 229 | 0 | 0 | 0 | 0 | 0 | 0 | 98.09 | 20 | 0 |
| scenario_s22_02 | run_215 | 118 | 0 | 15 | 0 | 0 | 9 | 6 | 12.13 | 14 | 0 |
| scenario_s22_06 | run_219 | 118 | 0 | 13 | 0 | 0 | 10 | 3 | 12.00 | 13 | 0 |
| scenario_s22_12 | run_223 | 134 | 3 | 9 | 0 | 0 | 6 | 3 | 9.85 | 12 | 0 |
| scenario_s22_18 | run_227 | 118 | 0 | 35 | 0 | 0 | 11 | 24 | 6.27 | 9 | 0 |
| scenario_s22_24 | run_231 | 141 | 16 | 6 | 1 | 1 | 4 | 0 | 1.37 | 16 | 0 |
| scenario_s23_09 | run_235 | 173 | 2 | 0 | 0 | 0 | 0 | 0 | 56.57 | 18 | 0 |
| scenario_s23_15 | run_239 | 171 | 0 | 8 | 0 | 0 | 5 | 3 | 14.81 | 20 | 0 |
| scenario_s23_21 | run_243 | 172 | 0 | 5 | 0 | 0 | 2 | 3 | 45.73 | 20 | 0 |
| scenario_s23_27 | run_247 | 171 | 0 | 0 | 0 | 0 | 0 | 0 | 392.09 | 16 | 0 |
| scenario_s23_31 | run_251 | 172 | 0 | 5 | 0 | 0 | 2 | 3 | 41.41 | 15 | 0 |
| scenario_s24_02 | run_255 | 301 | 55 | 11 | 0 | 1 | 10 | 0 | 3.95 | 25 | 0 |
| scenario_s24_08 | run_259 | 252 | 8 | 5 | 1 | 1 | 3 | 0 | 4.11 | 22 | 0 |
| scenario_s24_14 | run_263 | 272 | 8 | 11 | 2 | 0 | 4 | 5 | 28.43 | 21 | 0 |
| scenario_s24_20 | run_267 | 261 | 0 | 7 | 0 | 0 | 4 | 3 | 26.57 | 21 | 0 |
| scenario_s24_26 | run_271 | 261 | 0 | 0 | 0 | 0 | 0 | 0 | 353.53 | 24 | 0 |
| scenario_s25_02 | run_275 | 122 | 0 | 7 | 0 | 0 | 4 | 3 | 40.29 | 12 | 0 |
| scenario_s25_06 | run_279 | 58 | 0 | 9 | 0 | 0 | 6 | 3 | 13.18 | 12 | 0 |
| scenario_s25_10 | run_283 | 152 | 2 | 0 | 0 | 0 | 0 | 0 | 51.94 | 12 | 0 |
| scenario_s25_16 | run_287 | 100 | 3 | 0 | 0 | 0 | 0 | 0 | 61.63 | 9 | 0 |
| scenario_s25_22 | run_291 | 74 | 0 | 7 | 0 | 0 | 4 | 3 | 31.60 | 8 | 0 |
| scenario_s25_28 | run_295 | 145 | 0 | 0 | 0 | 0 | 0 | 0 | 246.62 | 12 | 0 |
| scenario_s25_34 | run_299 | 150 | 0 | 14 | 0 | 0 | 11 | 3 | 8.03 | 13 | 0 |
| scenario_s25_40 | run_303 | 122 | 0 | 0 | 0 | 0 | 0 | 0 | 215.68 | 14 | 0 |
| scenario_s25_44 | run_307 | 111 | 0 | 6 | 0 | 0 | 3 | 3 | 41.05 | 9 | 0 |
| scenario_s25_50 | run_311 | 87 | 0 | 6 | 0 | 0 | 3 | 3 | 37.53 | 15 | 0 |
| scenario_s26_02 | run_315 | 232 | 0 | 0 | 0 | 0 | 0 | 0 | 308.68 | 14 | 0 |
| scenario_s26_06 | run_319 | 162 | 0 | 17 | 0 | 0 | 11 | 6 | 2.67 | 11 | 0 |
| scenario_s26_10 | run_323 | 271 | 0 | 0 | 0 | 0 | 0 | 0 | 52.77 | 21 | 0 |
| scenario_s26_16 | run_327 | 286 | 9 | 11 | 0 | 0 | 8 | 3 | 8.39 | 19 | 0 |
| scenario_s26_22 | run_331 | 250 | 0 | 9 | 0 | 0 | 6 | 3 | 11.25 | 15 | 0 |
| scenario_s26_28 | run_335 | 272 | 0 | 0 | 0 | 0 | 0 | 0 | 111.20 | 22 | 0 |
| scenario_s26_32 | run_339 | 281 | 9 | 0 | 0 | 0 | 0 | 0 | 124.91 | 13 | 0 |
| scenario_s26_38 | run_343 | 214 | 0 | 0 | 0 | 0 | 0 | 0 | 471.78 | 16 | 0 |
| scenario_s26_42 | run_347 | 267 | 0 | 9 | 0 | 0 | 6 | 3 | 0.25 | 18 | 0 |
| scenario_s26_48 | run_351 | 257 | 18 | 15 | 2 | 1 | 7 | 5 | 3.58 | 11 | 0 |
| scenario_s27_02 | run_355 | 86 | 0 | 0 | 0 | 0 | 0 | 0 | 378.96 | 13 | 0 |
| scenario_s27_06 | run_359 | 74 | 0 | 0 | 0 | 0 | 0 | 0 | 1045.56 | 10 | 0 |
| scenario_s27_10 | run_363 | 151 | 0 | 7 | 0 | 0 | 4 | 3 | 25.63 | 11 | 0 |
| scenario_s27_14 | run_367 | 97 | 0 | 7 | 0 | 0 | 4 | 3 | 39.98 | 15 | 0 |
| scenario_s27_20 | run_371 | 65 | 0 | 8 | 0 | 0 | 5 | 3 | 20.88 | 8 | 0 |
| scenario_s27_26 | run_375 | 118 | 0 | 0 | 0 | 0 | 0 | 0 | 948.68 | 12 | 0 |
| scenario_s27_30 | run_379 | 116 | 0 | 0 | 0 | 0 | 0 | 0 | 141.88 | 9 | 0 |
| scenario_s27_36 | run_383 | 116 | 0 | 0 | 0 | 0 | 0 | 0 | 119.53 | 16 | 0 |
| scenario_s27_42 | run_387 | 100 | 0 | 0 | 0 | 0 | 0 | 0 | 87.99 | 11 | 0 |
| scenario_s27_44 | run_391 | 59 | 0 | 0 | 0 | 0 | 0 | 0 | 1012.12 | 6 | 0 |
| scenario_s28_02 | run_395 | 293 | 7 | 7 | 1 | 2 | 3 | 1 | 2.54 | 24 | 0 |
| scenario_s28_06 | run_399 | 107 | 0 | 0 | 0 | 0 | 0 | 0 | 710.19 | 8 | 0 |
| scenario_s28_10 | run_403 | 98 | 0 | 5 | 0 | 0 | 2 | 3 | 35.42 | 7 | 0 |
| scenario_s28_16 | run_407 | 211 | 0 | 0 | 0 | 0 | 0 | 0 | 196.87 | 22 | 0 |
| scenario_s28_22 | run_411 | 171 | 0 | 0 | 0 | 0 | 0 | 0 | 199.99 | 18 | 0 |
| scenario_s28_28 | run_415 | 101 | 0 | 8 | 0 | 0 | 5 | 3 | 17.86 | 5 | 0 |
| scenario_s28_32 | run_419 | 143 | 0 | 7 | 0 | 0 | 4 | 3 | 30.12 | 12 | 0 |
| scenario_s28_38 | run_423 | 178 | 0 | 0 | 0 | 0 | 0 | 0 | 890.68 | 13 | 0 |
| scenario_s28_42 | run_427 | 250 | 0 | 0 | 0 | 0 | 0 | 0 | 55.02 | 20 | 0 |
| scenario_s28_48 | run_431 | 93 | 0 | 0 | 0 | 0 | 0 | 0 | 267.60 | 12 | 0 |
| scenario_s29_02 | run_435 | 167 | 0 | 0 | 0 | 0 | 0 | 0 | 329.53 | 12 | 0 |
| scenario_s29_06 | run_439 | 242 | 0 | 0 | 0 | 0 | 0 | 0 | 185.81 | 14 | 0 |
| scenario_s29_10 | run_443 | 219 | 0 | 0 | 0 | 0 | 0 | 0 | 72.05 | 12 | 0 |
| scenario_s29_16 | run_447 | 217 | 24 | 0 | 0 | 0 | 0 | 0 | 207.48 | 14 | 0 |
| scenario_s29_22 | run_451 | 256 | 0 | 0 | 0 | 0 | 0 | 0 | 332.24 | 16 | 0 |
| scenario_s29_28 | run_455 | 160 | 0 | 0 | 0 | 0 | 0 | 0 | 646.71 | 9 | 0 |
| scenario_s29_34 | run_459 | 182 | 0 | 0 | 0 | 0 | 0 | 0 | 696.04 | 11 | 0 |
| scenario_s29_40 | run_463 | 184 | 0 | 7 | 0 | 0 | 4 | 3 | 24.32 | 12 | 0 |
| scenario_s29_44 | run_467 | 214 | 0 | 0 | 0 | 0 | 0 | 0 | 90.99 | 15 | 0 |
| scenario_s29_48 | run_471 | 267 | 0 | 0 | 0 | 0 | 0 | 0 | 226.90 | 29 | 0 |
| scenario_s30_02 | run_475 | 101 | 0 | 0 | 0 | 0 | 0 | 0 | 1367.57 | 13 | 0 |
| scenario_s30_06 | run_479 | 145 | 0 | 9 | 0 | 0 | 6 | 3 | 3.99 | 13 | 0 |
| scenario_s30_10 | run_483 | 151 | 0 | 0 | 0 | 0 | 0 | 0 | 603.01 | 15 | 0 |
| scenario_s30_16 | run_487 | 162 | 0 | 7 | 0 | 0 | 4 | 3 | 26.57 | 18 | 0 |
| scenario_s30_22 | run_491 | 92 | 0 | 0 | 0 | 0 | 0 | 0 | 926.69 | 11 | 0 |
| scenario_s30_28 | run_495 | 149 | 0 | 0 | 0 | 0 | 0 | 0 | 262.69 | 15 | 0 |
| scenario_s30_34 | run_499 | 154 | 0 | 0 | 0 | 0 | 0 | 0 | 1334.76 | 16 | 0 |
| scenario_s30_38 | run_503 | 151 | 0 | 0 | 0 | 0 | 0 | 0 | 514.55 | 19 | 0 |
| scenario_s30_42 | run_507 | 92 | 0 | 0 | 0 | 0 | 0 | 0 | 697.37 | 10 | 0 |
| scenario_s30_46 | run_511 | 107 | 0 | 8 | 0 | 0 | 5 | 3 | 20.46 | 14 | 0 |

### intention-aware, context knowledge on (IA-on): 106 runs, completed within the cap 105, held ticks 1148, ticks below min_separation 411 (viol 19, recede 25, passing 224, beside 143), scenarios with a tick below 47

| scenario | run | completion | held | below | viol | recede | passing | beside | sep_min | decisions | oracle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| scenario_s02_01 | run_092 | 422 | 0 | 7 | 0 | 3 | 2 | 2 | 30.87 | 29 | 0 |
| scenario_s02_02 | run_096 | - | 734 | 0 | 0 | 0 | 0 | 0 | 60.28 | 21 | 0 |
| scenario_s03_06 | run_100 | 238 | 9 | 0 | 0 | 0 | 0 | 0 | 60.15 | 12 | 0 |
| scenario_s04_01 | run_104 | 379 | 0 | 0 | 0 | 0 | 0 | 0 | 59.89 | 26 | 0 |
| scenario_s05_01 | run_108 | 197 | 75 | 5 | 3 | 2 | 0 | 0 | 30.00 | 14 | 0 |
| scenario_s05_02 | run_112 | 198 | 75 | 5 | 3 | 2 | 0 | 0 | 30.00 | 14 | 0 |
| scenario_s17_12 | run_116 | 279 | 0 | 5 | 0 | 0 | 2 | 3 | 40.58 | 13 | 0 |
| scenario_s17_18 | run_120 | 305 | 0 | 0 | 0 | 0 | 0 | 0 | 86.67 | 22 | 0 |
| scenario_s17_24 | run_124 | 299 | 10 | 5 | 0 | 1 | 4 | 0 | 9.74 | 19 | 0 |
| scenario_s17_30 | run_128 | 326 | 0 | 0 | 0 | 0 | 0 | 0 | 66.46 | 19 | 0 |
| scenario_s17_36 | run_132 | 332 | 0 | 0 | 0 | 0 | 0 | 0 | 124.64 | 18 | 0 |
| scenario_s18_02 | run_136 | 340 | 0 | 6 | 2 | 0 | 2 | 2 | 23.55 | 20 | 0 |
| scenario_s18_08 | run_140 | 331 | 0 | 0 | 0 | 0 | 0 | 0 | 234.61 | 23 | 0 |
| scenario_s18_14 | run_144 | 310 | 0 | 0 | 0 | 0 | 0 | 0 | 317.41 | 27 | 0 |
| scenario_s18_20 | run_148 | 337 | 0 | 0 | 0 | 0 | 0 | 0 | 144.23 | 24 | 0 |
| scenario_s18_26 | run_152 | 369 | 7 | 0 | 0 | 0 | 0 | 0 | 50.61 | 26 | 0 |
| scenario_s19_07 | run_156 | 379 | 0 | 0 | 0 | 0 | 0 | 0 | 73.31 | 20 | 0 |
| scenario_s19_13 | run_160 | 405 | 28 | 8 | 1 | 3 | 3 | 1 | 2.22 | 23 | 0 |
| scenario_s19_19 | run_164 | 282 | 0 | 8 | 0 | 0 | 5 | 3 | 28.78 | 15 | 0 |
| scenario_s19_25 | run_168 | 379 | 0 | 0 | 0 | 0 | 0 | 0 | 142.83 | 24 | 0 |
| scenario_s19_31 | run_172 | 282 | 0 | 0 | 0 | 0 | 0 | 0 | 164.51 | 20 | 0 |
| scenario_s20_02 | run_176 | 254 | 1 | 9 | 0 | 0 | 6 | 3 | 12.44 | 16 | 0 |
| scenario_s20_08 | run_180 | 275 | 0 | 0 | 0 | 0 | 0 | 0 | 61.97 | 15 | 0 |
| scenario_s20_14 | run_184 | 276 | 0 | 8 | 0 | 0 | 5 | 3 | 12.43 | 17 | 0 |
| scenario_s20_20 | run_188 | 271 | 0 | 0 | 0 | 0 | 0 | 0 | 122.13 | 17 | 0 |
| scenario_s20_26 | run_192 | 292 | 13 | 16 | 1 | 1 | 8 | 6 | 8.97 | 23 | 0 |
| scenario_s21_07 | run_196 | 242 | 13 | 4 | 0 | 1 | 3 | 0 | 34.35 | 19 | 0 |
| scenario_s21_11 | run_200 | 229 | 0 | 0 | 0 | 0 | 0 | 0 | 73.19 | 19 | 0 |
| scenario_s21_17 | run_204 | 229 | 0 | 0 | 0 | 0 | 0 | 0 | 145.59 | 24 | 0 |
| scenario_s21_23 | run_208 | 201 | 0 | 6 | 1 | 3 | 2 | 0 | 11.45 | 24 | 0 |
| scenario_s21_29 | run_212 | 229 | 0 | 0 | 0 | 0 | 0 | 0 | 98.09 | 19 | 0 |
| scenario_s22_02 | run_216 | 118 | 0 | 15 | 0 | 0 | 9 | 6 | 12.13 | 13 | 0 |
| scenario_s22_06 | run_220 | 118 | 0 | 13 | 0 | 0 | 10 | 3 | 12.00 | 12 | 0 |
| scenario_s22_12 | run_224 | 134 | 3 | 9 | 0 | 0 | 6 | 3 | 9.85 | 12 | 0 |
| scenario_s22_18 | run_228 | 118 | 0 | 35 | 0 | 0 | 11 | 24 | 6.27 | 8 | 0 |
| scenario_s22_24 | run_232 | 141 | 16 | 6 | 1 | 1 | 4 | 0 | 3.47 | 10 | 0 |
| scenario_s23_09 | run_236 | 173 | 2 | 0 | 0 | 0 | 0 | 0 | 56.57 | 12 | 0 |
| scenario_s23_15 | run_240 | 171 | 0 | 8 | 0 | 0 | 5 | 3 | 14.81 | 15 | 0 |
| scenario_s23_21 | run_244 | 179 | 7 | 10 | 3 | 2 | 2 | 3 | 19.34 | 16 | 0 |
| scenario_s23_27 | run_248 | 171 | 0 | 0 | 0 | 0 | 0 | 0 | 392.09 | 14 | 0 |
| scenario_s23_31 | run_252 | 172 | 0 | 5 | 0 | 0 | 2 | 3 | 41.41 | 14 | 0 |
| scenario_s24_02 | run_256 | 313 | 67 | 11 | 0 | 1 | 10 | 0 | 5.68 | 19 | 0 |
| scenario_s24_08 | run_260 | 252 | 8 | 5 | 1 | 1 | 3 | 0 | 4.11 | 19 | 0 |
| scenario_s24_14 | run_264 | 279 | 8 | 5 | 0 | 0 | 2 | 3 | 35.18 | 25 | 0 |
| scenario_s24_20 | run_268 | 261 | 0 | 7 | 0 | 0 | 4 | 3 | 26.57 | 20 | 0 |
| scenario_s24_26 | run_272 | 261 | 0 | 0 | 0 | 0 | 0 | 0 | 353.53 | 19 | 0 |
| scenario_s25_02 | run_276 | 122 | 0 | 7 | 0 | 0 | 4 | 3 | 40.29 | 7 | 0 |
| scenario_s25_06 | run_280 | 58 | 0 | 9 | 0 | 0 | 6 | 3 | 13.18 | 12 | 0 |
| scenario_s25_10 | run_284 | 152 | 2 | 0 | 0 | 0 | 0 | 0 | 51.94 | 14 | 0 |
| scenario_s25_16 | run_288 | 100 | 3 | 0 | 0 | 0 | 0 | 0 | 61.63 | 8 | 0 |
| scenario_s25_22 | run_292 | 74 | 0 | 7 | 0 | 0 | 4 | 3 | 31.60 | 7 | 0 |
| scenario_s25_28 | run_296 | 145 | 0 | 0 | 0 | 0 | 0 | 0 | 246.62 | 13 | 0 |
| scenario_s25_34 | run_300 | 150 | 0 | 14 | 0 | 0 | 11 | 3 | 8.03 | 9 | 0 |
| scenario_s25_40 | run_304 | 122 | 0 | 0 | 0 | 0 | 0 | 0 | 215.68 | 13 | 0 |
| scenario_s25_44 | run_308 | 111 | 0 | 6 | 0 | 0 | 3 | 3 | 41.05 | 12 | 0 |
| scenario_s25_50 | run_312 | 87 | 0 | 6 | 0 | 0 | 3 | 3 | 37.53 | 15 | 0 |
| scenario_s26_02 | run_316 | 232 | 0 | 0 | 0 | 0 | 0 | 0 | 308.68 | 12 | 0 |
| scenario_s26_06 | run_320 | 162 | 0 | 17 | 0 | 0 | 11 | 6 | 2.67 | 11 | 0 |
| scenario_s26_10 | run_324 | 271 | 0 | 0 | 0 | 0 | 0 | 0 | 52.77 | 22 | 0 |
| scenario_s26_16 | run_328 | 286 | 9 | 11 | 0 | 0 | 8 | 3 | 8.39 | 16 | 0 |
| scenario_s26_22 | run_332 | 250 | 0 | 9 | 0 | 0 | 6 | 3 | 11.25 | 15 | 0 |
| scenario_s26_28 | run_336 | 272 | 0 | 0 | 0 | 0 | 0 | 0 | 111.20 | 18 | 0 |
| scenario_s26_32 | run_340 | 281 | 9 | 0 | 0 | 0 | 0 | 0 | 124.91 | 14 | 0 |
| scenario_s26_38 | run_344 | 214 | 0 | 0 | 0 | 0 | 0 | 0 | 471.78 | 14 | 0 |
| scenario_s26_42 | run_348 | 267 | 0 | 9 | 0 | 0 | 6 | 3 | 0.25 | 19 | 0 |
| scenario_s26_48 | run_352 | 256 | 18 | 15 | 2 | 2 | 6 | 5 | 3.58 | 12 | 0 |
| scenario_s27_02 | run_356 | 86 | 0 | 0 | 0 | 0 | 0 | 0 | 378.96 | 10 | 0 |
| scenario_s27_06 | run_360 | 74 | 0 | 0 | 0 | 0 | 0 | 0 | 1045.56 | 9 | 0 |
| scenario_s27_10 | run_364 | 151 | 0 | 7 | 0 | 0 | 4 | 3 | 25.63 | 9 | 0 |
| scenario_s27_14 | run_368 | 97 | 0 | 7 | 0 | 0 | 4 | 3 | 39.98 | 15 | 0 |
| scenario_s27_20 | run_372 | 65 | 0 | 8 | 0 | 0 | 5 | 3 | 20.88 | 7 | 0 |
| scenario_s27_26 | run_376 | 118 | 0 | 0 | 0 | 0 | 0 | 0 | 948.68 | 12 | 0 |
| scenario_s27_30 | run_380 | 116 | 0 | 0 | 0 | 0 | 0 | 0 | 141.88 | 7 | 0 |
| scenario_s27_36 | run_384 | 116 | 0 | 0 | 0 | 0 | 0 | 0 | 119.53 | 15 | 0 |
| scenario_s27_42 | run_388 | 100 | 0 | 0 | 0 | 0 | 0 | 0 | 87.99 | 11 | 0 |
| scenario_s27_44 | run_392 | 59 | 0 | 0 | 0 | 0 | 0 | 0 | 1012.12 | 7 | 0 |
| scenario_s28_02 | run_396 | 293 | 7 | 7 | 1 | 2 | 3 | 1 | 2.54 | 18 | 0 |
| scenario_s28_06 | run_400 | 107 | 0 | 0 | 0 | 0 | 0 | 0 | 710.19 | 5 | 0 |
| scenario_s28_10 | run_404 | 98 | 0 | 5 | 0 | 0 | 2 | 3 | 35.42 | 8 | 0 |
| scenario_s28_16 | run_408 | 211 | 0 | 0 | 0 | 0 | 0 | 0 | 196.87 | 21 | 0 |
| scenario_s28_22 | run_412 | 171 | 0 | 0 | 0 | 0 | 0 | 0 | 199.99 | 15 | 0 |
| scenario_s28_28 | run_416 | 101 | 0 | 8 | 0 | 0 | 5 | 3 | 17.86 | 3 | 0 |
| scenario_s28_32 | run_420 | 143 | 0 | 7 | 0 | 0 | 4 | 3 | 30.12 | 13 | 0 |
| scenario_s28_38 | run_424 | 178 | 0 | 0 | 0 | 0 | 0 | 0 | 890.68 | 10 | 0 |
| scenario_s28_42 | run_428 | 250 | 0 | 0 | 0 | 0 | 0 | 0 | 55.02 | 23 | 0 |
| scenario_s28_48 | run_432 | 93 | 0 | 0 | 0 | 0 | 0 | 0 | 267.60 | 11 | 0 |
| scenario_s29_02 | run_436 | 167 | 0 | 0 | 0 | 0 | 0 | 0 | 329.53 | 10 | 0 |
| scenario_s29_06 | run_440 | 242 | 0 | 0 | 0 | 0 | 0 | 0 | 185.81 | 11 | 0 |
| scenario_s29_10 | run_444 | 219 | 0 | 0 | 0 | 0 | 0 | 0 | 72.05 | 8 | 0 |
| scenario_s29_16 | run_448 | 216 | 24 | 0 | 0 | 0 | 0 | 0 | 213.35 | 16 | 0 |
| scenario_s29_22 | run_452 | 256 | 0 | 0 | 0 | 0 | 0 | 0 | 332.24 | 13 | 0 |
| scenario_s29_28 | run_456 | 160 | 0 | 0 | 0 | 0 | 0 | 0 | 646.71 | 10 | 0 |
| scenario_s29_34 | run_460 | 182 | 0 | 0 | 0 | 0 | 0 | 0 | 696.04 | 11 | 0 |
| scenario_s29_40 | run_464 | 184 | 0 | 7 | 0 | 0 | 4 | 3 | 24.32 | 12 | 0 |
| scenario_s29_44 | run_468 | 214 | 0 | 0 | 0 | 0 | 0 | 0 | 90.99 | 15 | 0 |
| scenario_s29_48 | run_472 | 267 | 0 | 0 | 0 | 0 | 0 | 0 | 226.90 | 24 | 0 |
| scenario_s30_02 | run_476 | 101 | 0 | 0 | 0 | 0 | 0 | 0 | 1367.57 | 12 | 0 |
| scenario_s30_06 | run_480 | 145 | 0 | 9 | 0 | 0 | 6 | 3 | 3.99 | 13 | 0 |
| scenario_s30_10 | run_484 | 151 | 0 | 0 | 0 | 0 | 0 | 0 | 603.01 | 14 | 0 |
| scenario_s30_16 | run_488 | 162 | 0 | 7 | 0 | 0 | 4 | 3 | 26.57 | 18 | 0 |
| scenario_s30_22 | run_492 | 92 | 0 | 0 | 0 | 0 | 0 | 0 | 926.69 | 10 | 0 |
| scenario_s30_28 | run_496 | 149 | 0 | 0 | 0 | 0 | 0 | 0 | 262.69 | 17 | 0 |
| scenario_s30_34 | run_500 | 154 | 0 | 0 | 0 | 0 | 0 | 0 | 1334.76 | 16 | 0 |
| scenario_s30_38 | run_504 | 151 | 0 | 0 | 0 | 0 | 0 | 0 | 514.55 | 16 | 0 |
| scenario_s30_42 | run_508 | 92 | 0 | 0 | 0 | 0 | 0 | 0 | 697.37 | 8 | 0 |
| scenario_s30_46 | run_512 | 107 | 0 | 8 | 0 | 0 | 5 | 3 | 20.46 | 12 | 0 |

### Pairs of conditions (the second against the first): scenarios better / equal / worse

| first | second | completion | ticks below min_separation | viol ticks |
|---|---|---|---|---|
| HU | IU | 0 / 81 / 25 | 15 / 84 / 7 | 23 / 83 / 0 |
| HU | IA-off | 0 / 82 / 24 | 19 / 82 / 5 | 23 / 82 / 1 |
| HU | IA-on | 0 / 81 / 25 | 19 / 81 / 6 | 23 / 81 / 2 |
| IU | IA-off | 11 / 84 / 11 | 6 / 96 / 4 | 5 / 96 / 5 |
| IU | IA-on | 11 / 83 / 12 | 6 / 96 / 4 | 5 / 96 / 5 |
| IA-off | IA-on | 3 / 97 / 6 | 3 / 100 / 3 | 3 / 100 / 3 |

## step 5e's copies with a timeline (176; IA-on only)

### intention-aware, context knowledge on (IA-on): 176 runs, completed within the cap 174, held ticks 2258, ticks below min_separation 700 (viol 27, recede 40, passing 384, beside 249), scenarios with a tick below 79

| scenario | run | completion | held | below | viol | recede | passing | beside | sep_min | decisions | oracle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| scenario_s17_03 | run_513 | 422 | 0 | 7 | 0 | 3 | 2 | 2 | 30.87 | 19 | 0 |
| scenario_s17_05 | run_514 | 422 | 0 | 7 | 0 | 3 | 2 | 2 | 30.87 | 31 | 0 |
| scenario_s17_08 | run_515 | - | 734 | 0 | 0 | 0 | 0 | 0 | 60.28 | 20 | 0 |
| scenario_s17_10 | run_516 | - | 734 | 0 | 0 | 0 | 0 | 0 | 60.28 | 21 | 0 |
| scenario_s17_14 | run_517 | 279 | 0 | 5 | 0 | 0 | 2 | 3 | 40.58 | 13 | 0 |
| scenario_s17_16 | run_518 | 279 | 0 | 5 | 0 | 0 | 2 | 3 | 40.58 | 13 | 0 |
| scenario_s17_20 | run_519 | 305 | 0 | 0 | 0 | 0 | 0 | 0 | 86.67 | 15 | 0 |
| scenario_s17_22 | run_520 | 305 | 0 | 0 | 0 | 0 | 0 | 0 | 86.67 | 22 | 0 |
| scenario_s17_26 | run_521 | 299 | 10 | 5 | 0 | 1 | 4 | 0 | 9.74 | 16 | 0 |
| scenario_s17_28 | run_522 | 299 | 10 | 5 | 0 | 1 | 4 | 0 | 9.74 | 21 | 0 |
| scenario_s17_32 | run_523 | 326 | 0 | 0 | 0 | 0 | 0 | 0 | 66.46 | 20 | 0 |
| scenario_s17_34 | run_524 | 326 | 0 | 0 | 0 | 0 | 0 | 0 | 66.46 | 19 | 0 |
| scenario_s17_38 | run_525 | 332 | 0 | 0 | 0 | 0 | 0 | 0 | 124.64 | 23 | 0 |
| scenario_s17_40 | run_526 | 332 | 0 | 0 | 0 | 0 | 0 | 0 | 124.64 | 21 | 0 |
| scenario_s18_04 | run_527 | 340 | 0 | 6 | 2 | 0 | 2 | 2 | 23.55 | 22 | 0 |
| scenario_s18_06 | run_528 | 340 | 0 | 6 | 2 | 0 | 2 | 2 | 23.55 | 24 | 0 |
| scenario_s18_10 | run_529 | 331 | 0 | 0 | 0 | 0 | 0 | 0 | 234.61 | 17 | 0 |
| scenario_s18_12 | run_530 | 331 | 0 | 0 | 0 | 0 | 0 | 0 | 234.61 | 24 | 0 |
| scenario_s18_16 | run_531 | 310 | 0 | 0 | 0 | 0 | 0 | 0 | 317.41 | 18 | 0 |
| scenario_s18_18 | run_532 | 310 | 0 | 0 | 0 | 0 | 0 | 0 | 317.41 | 30 | 0 |
| scenario_s18_22 | run_533 | 337 | 0 | 0 | 0 | 0 | 0 | 0 | 144.23 | 25 | 0 |
| scenario_s18_24 | run_534 | 337 | 0 | 0 | 0 | 0 | 0 | 0 | 144.23 | 24 | 0 |
| scenario_s18_28 | run_535 | 369 | 7 | 0 | 0 | 0 | 0 | 0 | 50.61 | 27 | 0 |
| scenario_s18_30 | run_536 | 369 | 7 | 0 | 0 | 0 | 0 | 0 | 50.61 | 26 | 0 |
| scenario_s19_03 | run_537 | 379 | 0 | 0 | 0 | 0 | 0 | 0 | 59.89 | 23 | 0 |
| scenario_s19_05 | run_538 | 379 | 0 | 0 | 0 | 0 | 0 | 0 | 59.89 | 27 | 0 |
| scenario_s19_09 | run_539 | 379 | 0 | 0 | 0 | 0 | 0 | 0 | 73.31 | 21 | 0 |
| scenario_s19_11 | run_540 | 379 | 0 | 0 | 0 | 0 | 0 | 0 | 73.31 | 20 | 0 |
| scenario_s19_15 | run_541 | 405 | 28 | 8 | 1 | 3 | 3 | 1 | 2.22 | 23 | 0 |
| scenario_s19_17 | run_542 | 405 | 28 | 8 | 2 | 3 | 2 | 1 | 2.22 | 25 | 0 |
| scenario_s19_21 | run_543 | 282 | 0 | 8 | 0 | 0 | 5 | 3 | 28.78 | 12 | 0 |
| scenario_s19_23 | run_544 | 282 | 0 | 8 | 0 | 0 | 5 | 3 | 28.78 | 17 | 0 |
| scenario_s19_27 | run_545 | 379 | 0 | 0 | 0 | 0 | 0 | 0 | 142.83 | 24 | 0 |
| scenario_s19_29 | run_546 | 379 | 0 | 0 | 0 | 0 | 0 | 0 | 142.83 | 27 | 0 |
| scenario_s19_33 | run_547 | 282 | 0 | 0 | 0 | 0 | 0 | 0 | 164.51 | 20 | 0 |
| scenario_s20_04 | run_548 | 254 | 1 | 9 | 0 | 0 | 6 | 3 | 12.44 | 17 | 0 |
| scenario_s20_06 | run_549 | 254 | 1 | 9 | 0 | 0 | 6 | 3 | 12.44 | 16 | 0 |
| scenario_s20_10 | run_550 | 275 | 0 | 0 | 0 | 0 | 0 | 0 | 61.97 | 11 | 0 |
| scenario_s20_12 | run_551 | 275 | 0 | 0 | 0 | 0 | 0 | 0 | 61.97 | 16 | 0 |
| scenario_s20_16 | run_552 | 276 | 0 | 8 | 0 | 0 | 5 | 3 | 12.43 | 15 | 0 |
| scenario_s20_18 | run_553 | 276 | 0 | 8 | 0 | 0 | 5 | 3 | 12.43 | 17 | 0 |
| scenario_s20_22 | run_554 | 271 | 0 | 0 | 0 | 0 | 0 | 0 | 122.13 | 19 | 0 |
| scenario_s20_24 | run_555 | 271 | 0 | 0 | 0 | 0 | 0 | 0 | 122.13 | 18 | 0 |
| scenario_s20_28 | run_556 | 292 | 13 | 16 | 1 | 1 | 8 | 6 | 8.97 | 23 | 0 |
| scenario_s20_30 | run_557 | 292 | 13 | 16 | 1 | 1 | 8 | 6 | 8.97 | 23 | 0 |
| scenario_s21_03 | run_558 | 238 | 9 | 0 | 0 | 0 | 0 | 0 | 60.15 | 12 | 0 |
| scenario_s21_05 | run_559 | 238 | 9 | 0 | 0 | 0 | 0 | 0 | 60.15 | 13 | 0 |
| scenario_s21_09 | run_560 | 242 | 13 | 4 | 0 | 1 | 3 | 0 | 34.35 | 20 | 0 |
| scenario_s21_13 | run_561 | 229 | 0 | 0 | 0 | 0 | 0 | 0 | 73.19 | 14 | 0 |
| scenario_s21_15 | run_562 | 229 | 0 | 0 | 0 | 0 | 0 | 0 | 73.19 | 19 | 0 |
| scenario_s21_19 | run_563 | 229 | 0 | 0 | 0 | 0 | 0 | 0 | 145.59 | 20 | 0 |
| scenario_s21_21 | run_564 | 229 | 0 | 0 | 0 | 0 | 0 | 0 | 145.59 | 24 | 0 |
| scenario_s21_25 | run_565 | 201 | 0 | 6 | 1 | 3 | 2 | 0 | 11.45 | 19 | 0 |
| scenario_s21_27 | run_566 | 201 | 0 | 6 | 1 | 3 | 2 | 0 | 11.45 | 25 | 0 |
| scenario_s21_31 | run_567 | 229 | 0 | 0 | 0 | 0 | 0 | 0 | 98.09 | 22 | 0 |
| scenario_s22_04 | run_568 | 118 | 0 | 15 | 0 | 0 | 9 | 6 | 12.13 | 14 | 0 |
| scenario_s22_08 | run_569 | 118 | 0 | 13 | 0 | 0 | 10 | 3 | 12.00 | 12 | 0 |
| scenario_s22_10 | run_570 | 118 | 0 | 13 | 0 | 0 | 10 | 3 | 12.00 | 12 | 0 |
| scenario_s22_14 | run_571 | 134 | 3 | 9 | 0 | 0 | 6 | 3 | 9.85 | 12 | 0 |
| scenario_s22_16 | run_572 | 134 | 3 | 9 | 0 | 0 | 6 | 3 | 9.85 | 12 | 0 |
| scenario_s22_20 | run_573 | 118 | 0 | 35 | 0 | 0 | 11 | 24 | 6.27 | 8 | 0 |
| scenario_s22_22 | run_574 | 118 | 0 | 35 | 0 | 0 | 11 | 24 | 6.27 | 9 | 0 |
| scenario_s22_26 | run_575 | 141 | 16 | 6 | 1 | 1 | 4 | 0 | 3.47 | 16 | 0 |
| scenario_s23_03 | run_576 | 189 | 5 | 0 | 0 | 0 | 0 | 0 | 58.31 | 18 | 0 |
| scenario_s23_04 | run_577 | 206 | 73 | 0 | 0 | 0 | 0 | 0 | 50.00 | 18 | 0 |
| scenario_s23_06 | run_578 | 197 | 75 | 5 | 3 | 2 | 0 | 0 | 30.00 | 14 | 0 |
| scenario_s23_07 | run_579 | 198 | 75 | 5 | 3 | 2 | 0 | 0 | 30.00 | 14 | 0 |
| scenario_s23_11 | run_580 | 177 | 0 | 0 | 0 | 0 | 0 | 0 | 297.17 | 15 | 0 |
| scenario_s23_13 | run_581 | 173 | 2 | 0 | 0 | 0 | 0 | 0 | 56.57 | 12 | 0 |
| scenario_s23_17 | run_582 | 171 | 0 | 8 | 0 | 0 | 5 | 3 | 14.81 | 14 | 0 |
| scenario_s23_19 | run_583 | 171 | 0 | 8 | 0 | 0 | 5 | 3 | 14.81 | 20 | 0 |
| scenario_s23_23 | run_584 | 224 | 77 | 0 | 0 | 0 | 0 | 0 | 52.06 | 20 | 0 |
| scenario_s23_25 | run_585 | 179 | 7 | 10 | 3 | 2 | 2 | 3 | 19.34 | 16 | 0 |
| scenario_s23_29 | run_586 | 171 | 0 | 0 | 0 | 0 | 0 | 0 | 392.09 | 15 | 0 |
| scenario_s23_33 | run_587 | 172 | 0 | 5 | 0 | 0 | 2 | 3 | 41.41 | 15 | 0 |
| scenario_s23_35 | run_588 | 172 | 0 | 5 | 0 | 0 | 2 | 3 | 41.41 | 14 | 0 |
| scenario_s24_04 | run_589 | 313 | 67 | 11 | 0 | 1 | 10 | 0 | 5.68 | 25 | 0 |
| scenario_s24_06 | run_590 | 313 | 67 | 11 | 0 | 1 | 10 | 0 | 5.68 | 21 | 0 |
| scenario_s24_10 | run_591 | 254 | 10 | 5 | 0 | 1 | 4 | 0 | 3.94 | 17 | 0 |
| scenario_s24_12 | run_592 | 252 | 8 | 5 | 1 | 1 | 3 | 0 | 4.11 | 20 | 0 |
| scenario_s24_16 | run_593 | 279 | 8 | 5 | 0 | 0 | 2 | 3 | 35.18 | 19 | 0 |
| scenario_s24_18 | run_594 | 279 | 8 | 5 | 0 | 0 | 2 | 3 | 35.18 | 25 | 0 |
| scenario_s24_22 | run_595 | 261 | 0 | 7 | 0 | 0 | 4 | 3 | 26.57 | 21 | 0 |
| scenario_s24_24 | run_596 | 261 | 0 | 7 | 0 | 0 | 4 | 3 | 26.57 | 21 | 0 |
| scenario_s24_28 | run_597 | 261 | 0 | 0 | 0 | 0 | 0 | 0 | 353.53 | 17 | 0 |
| scenario_s24_30 | run_598 | 261 | 0 | 0 | 0 | 0 | 0 | 0 | 353.53 | 23 | 0 |
| scenario_s25_04 | run_599 | 122 | 0 | 7 | 0 | 0 | 4 | 3 | 40.29 | 8 | 0 |
| scenario_s25_08 | run_600 | 58 | 0 | 9 | 0 | 0 | 6 | 3 | 13.18 | 12 | 0 |
| scenario_s25_12 | run_601 | 152 | 2 | 0 | 0 | 0 | 0 | 0 | 51.94 | 9 | 0 |
| scenario_s25_14 | run_602 | 152 | 2 | 0 | 0 | 0 | 0 | 0 | 51.94 | 14 | 0 |
| scenario_s25_18 | run_603 | 100 | 3 | 0 | 0 | 0 | 0 | 0 | 61.63 | 8 | 0 |
| scenario_s25_20 | run_604 | 100 | 3 | 0 | 0 | 0 | 0 | 0 | 61.63 | 13 | 0 |
| scenario_s25_24 | run_605 | 74 | 0 | 7 | 0 | 0 | 4 | 3 | 31.60 | 7 | 0 |
| scenario_s25_26 | run_606 | 74 | 0 | 7 | 0 | 0 | 4 | 3 | 31.60 | 7 | 0 |
| scenario_s25_30 | run_607 | 145 | 0 | 0 | 0 | 0 | 0 | 0 | 246.62 | 11 | 0 |
| scenario_s25_32 | run_608 | 145 | 0 | 0 | 0 | 0 | 0 | 0 | 246.62 | 13 | 0 |
| scenario_s25_36 | run_609 | 150 | 0 | 14 | 0 | 0 | 11 | 3 | 8.03 | 9 | 0 |
| scenario_s25_38 | run_610 | 150 | 0 | 14 | 0 | 0 | 11 | 3 | 8.03 | 10 | 0 |
| scenario_s25_42 | run_611 | 122 | 0 | 0 | 0 | 0 | 0 | 0 | 215.68 | 15 | 0 |
| scenario_s25_46 | run_612 | 111 | 0 | 6 | 0 | 0 | 3 | 3 | 41.05 | 9 | 0 |
| scenario_s25_48 | run_613 | 111 | 0 | 6 | 0 | 0 | 3 | 3 | 41.05 | 12 | 0 |
| scenario_s25_52 | run_614 | 87 | 0 | 6 | 0 | 0 | 3 | 3 | 37.53 | 15 | 0 |
| scenario_s26_04 | run_615 | 232 | 0 | 0 | 0 | 0 | 0 | 0 | 308.68 | 15 | 0 |
| scenario_s26_08 | run_616 | 162 | 0 | 17 | 0 | 0 | 11 | 6 | 2.67 | 11 | 0 |
| scenario_s26_12 | run_617 | 271 | 0 | 0 | 0 | 0 | 0 | 0 | 52.77 | 20 | 0 |
| scenario_s26_14 | run_618 | 271 | 0 | 0 | 0 | 0 | 0 | 0 | 52.77 | 22 | 0 |
| scenario_s26_18 | run_619 | 286 | 9 | 11 | 0 | 0 | 8 | 3 | 8.39 | 12 | 0 |
| scenario_s26_20 | run_620 | 286 | 9 | 11 | 0 | 0 | 8 | 3 | 8.39 | 16 | 0 |
| scenario_s26_24 | run_621 | 250 | 0 | 9 | 0 | 0 | 6 | 3 | 11.25 | 9 | 0 |
| scenario_s26_26 | run_622 | 250 | 0 | 9 | 0 | 0 | 6 | 3 | 11.25 | 15 | 0 |
| scenario_s26_30 | run_623 | 272 | 0 | 0 | 0 | 0 | 0 | 0 | 111.20 | 19 | 0 |
| scenario_s26_34 | run_624 | 281 | 9 | 0 | 0 | 0 | 0 | 0 | 124.91 | 12 | 0 |
| scenario_s26_36 | run_625 | 281 | 9 | 0 | 0 | 0 | 0 | 0 | 124.91 | 18 | 0 |
| scenario_s26_40 | run_626 | 214 | 0 | 0 | 0 | 0 | 0 | 0 | 471.78 | 16 | 0 |
| scenario_s26_44 | run_627 | 267 | 0 | 9 | 0 | 0 | 6 | 3 | 0.25 | 16 | 0 |
| scenario_s26_46 | run_628 | 267 | 0 | 9 | 0 | 0 | 6 | 3 | 0.25 | 20 | 0 |
| scenario_s26_50 | run_629 | 256 | 18 | 15 | 2 | 2 | 6 | 5 | 3.58 | 9 | 0 |
| scenario_s26_52 | run_630 | 256 | 18 | 15 | 2 | 2 | 6 | 5 | 3.58 | 12 | 0 |
| scenario_s27_04 | run_631 | 86 | 0 | 0 | 0 | 0 | 0 | 0 | 378.96 | 10 | 0 |
| scenario_s27_08 | run_632 | 74 | 0 | 0 | 0 | 0 | 0 | 0 | 1045.56 | 14 | 0 |
| scenario_s27_12 | run_633 | 151 | 0 | 7 | 0 | 0 | 4 | 3 | 25.63 | 10 | 0 |
| scenario_s27_16 | run_634 | 97 | 0 | 7 | 0 | 0 | 4 | 3 | 39.98 | 13 | 0 |
| scenario_s27_18 | run_635 | 97 | 0 | 7 | 0 | 0 | 4 | 3 | 39.98 | 17 | 0 |
| scenario_s27_22 | run_636 | 65 | 0 | 8 | 0 | 0 | 5 | 3 | 20.88 | 7 | 0 |
| scenario_s27_24 | run_637 | 65 | 0 | 8 | 0 | 0 | 5 | 3 | 20.88 | 7 | 0 |
| scenario_s27_28 | run_638 | 118 | 0 | 0 | 0 | 0 | 0 | 0 | 948.68 | 12 | 0 |
| scenario_s27_32 | run_639 | 116 | 0 | 0 | 0 | 0 | 0 | 0 | 141.88 | 7 | 0 |
| scenario_s27_34 | run_640 | 116 | 0 | 0 | 0 | 0 | 0 | 0 | 141.88 | 9 | 0 |
| scenario_s27_38 | run_641 | 116 | 0 | 0 | 0 | 0 | 0 | 0 | 119.53 | 14 | 0 |
| scenario_s27_40 | run_642 | 116 | 0 | 0 | 0 | 0 | 0 | 0 | 119.53 | 16 | 0 |
| scenario_s27_46 | run_643 | 59 | 0 | 0 | 0 | 0 | 0 | 0 | 1012.12 | 7 | 0 |
| scenario_s27_48 | run_644 | 59 | 0 | 0 | 0 | 0 | 0 | 0 | 1012.12 | 7 | 0 |
| scenario_s28_04 | run_645 | 293 | 7 | 7 | 1 | 2 | 3 | 1 | 2.54 | 24 | 0 |
| scenario_s28_08 | run_646 | 107 | 0 | 0 | 0 | 0 | 0 | 0 | 710.19 | 8 | 0 |
| scenario_s28_12 | run_647 | 98 | 0 | 5 | 0 | 0 | 2 | 3 | 35.42 | 6 | 0 |
| scenario_s28_14 | run_648 | 98 | 0 | 5 | 0 | 0 | 2 | 3 | 35.42 | 8 | 0 |
| scenario_s28_18 | run_649 | 211 | 0 | 0 | 0 | 0 | 0 | 0 | 196.87 | 19 | 0 |
| scenario_s28_20 | run_650 | 211 | 0 | 0 | 0 | 0 | 0 | 0 | 196.87 | 25 | 0 |
| scenario_s28_24 | run_651 | 171 | 0 | 0 | 0 | 0 | 0 | 0 | 199.99 | 11 | 0 |
| scenario_s28_26 | run_652 | 171 | 0 | 0 | 0 | 0 | 0 | 0 | 199.99 | 15 | 0 |
| scenario_s28_30 | run_653 | 101 | 0 | 8 | 0 | 0 | 5 | 3 | 17.86 | 3 | 0 |
| scenario_s28_34 | run_654 | 143 | 0 | 7 | 0 | 0 | 4 | 3 | 30.12 | 12 | 0 |
| scenario_s28_36 | run_655 | 143 | 0 | 7 | 0 | 0 | 4 | 3 | 30.12 | 14 | 0 |
| scenario_s28_40 | run_656 | 178 | 0 | 0 | 0 | 0 | 0 | 0 | 890.68 | 10 | 0 |
| scenario_s28_44 | run_657 | 250 | 0 | 0 | 0 | 0 | 0 | 0 | 55.02 | 19 | 0 |
| scenario_s28_46 | run_658 | 250 | 0 | 0 | 0 | 0 | 0 | 0 | 55.02 | 29 | 0 |
| scenario_s29_04 | run_659 | 167 | 0 | 0 | 0 | 0 | 0 | 0 | 329.53 | 13 | 0 |
| scenario_s29_08 | run_660 | 242 | 0 | 0 | 0 | 0 | 0 | 0 | 185.81 | 12 | 0 |
| scenario_s29_12 | run_661 | 219 | 0 | 0 | 0 | 0 | 0 | 0 | 72.05 | 8 | 0 |
| scenario_s29_14 | run_662 | 219 | 0 | 0 | 0 | 0 | 0 | 0 | 72.05 | 9 | 0 |
| scenario_s29_18 | run_663 | 211 | 24 | 0 | 0 | 0 | 0 | 0 | 207.48 | 13 | 0 |
| scenario_s29_20 | run_664 | 216 | 24 | 0 | 0 | 0 | 0 | 0 | 213.35 | 16 | 0 |
| scenario_s29_24 | run_665 | 256 | 0 | 0 | 0 | 0 | 0 | 0 | 332.24 | 13 | 0 |
| scenario_s29_26 | run_666 | 256 | 0 | 0 | 0 | 0 | 0 | 0 | 332.24 | 15 | 0 |
| scenario_s29_30 | run_667 | 160 | 0 | 0 | 0 | 0 | 0 | 0 | 646.71 | 8 | 0 |
| scenario_s29_32 | run_668 | 160 | 0 | 0 | 0 | 0 | 0 | 0 | 646.71 | 10 | 0 |
| scenario_s29_36 | run_669 | 182 | 0 | 0 | 0 | 0 | 0 | 0 | 696.04 | 11 | 0 |
| scenario_s29_38 | run_670 | 182 | 0 | 0 | 0 | 0 | 0 | 0 | 696.04 | 11 | 0 |
| scenario_s29_42 | run_671 | 184 | 0 | 7 | 0 | 0 | 4 | 3 | 24.32 | 13 | 0 |
| scenario_s29_46 | run_672 | 214 | 0 | 0 | 0 | 0 | 0 | 0 | 90.99 | 15 | 0 |
| scenario_s29_50 | run_673 | 267 | 0 | 0 | 0 | 0 | 0 | 0 | 226.90 | 24 | 0 |
| scenario_s30_04 | run_674 | 101 | 0 | 0 | 0 | 0 | 0 | 0 | 1367.57 | 12 | 0 |
| scenario_s30_08 | run_675 | 145 | 0 | 9 | 0 | 0 | 6 | 3 | 3.99 | 13 | 0 |
| scenario_s30_12 | run_676 | 151 | 0 | 0 | 0 | 0 | 0 | 0 | 603.01 | 11 | 0 |
| scenario_s30_14 | run_677 | 151 | 0 | 0 | 0 | 0 | 0 | 0 | 603.01 | 14 | 0 |
| scenario_s30_18 | run_678 | 162 | 0 | 7 | 0 | 0 | 4 | 3 | 26.57 | 13 | 0 |
| scenario_s30_20 | run_679 | 162 | 0 | 7 | 0 | 0 | 4 | 3 | 26.57 | 23 | 0 |
| scenario_s30_24 | run_680 | 92 | 0 | 0 | 0 | 0 | 0 | 0 | 926.69 | 10 | 0 |
| scenario_s30_26 | run_681 | 92 | 0 | 0 | 0 | 0 | 0 | 0 | 926.69 | 10 | 0 |
| scenario_s30_30 | run_682 | 149 | 0 | 0 | 0 | 0 | 0 | 0 | 262.69 | 12 | 0 |
| scenario_s30_32 | run_683 | 149 | 0 | 0 | 0 | 0 | 0 | 0 | 262.69 | 17 | 0 |
| scenario_s30_36 | run_684 | 154 | 0 | 0 | 0 | 0 | 0 | 0 | 1334.76 | 16 | 0 |
| scenario_s30_40 | run_685 | 151 | 0 | 0 | 0 | 0 | 0 | 0 | 514.55 | 17 | 0 |
| scenario_s30_44 | run_686 | 92 | 0 | 0 | 0 | 0 | 0 | 0 | 697.37 | 8 | 0 |
| scenario_s30_48 | run_687 | 107 | 0 | 8 | 0 | 0 | 5 | 3 | 20.46 | 12 | 0 |
| scenario_s30_50 | run_688 | 107 | 0 | 8 | 0 | 0 | 5 | 3 | 20.46 | 13 | 0 |


## Findings (none ruled)

1. **The human-unaware robot is never slower, and comes closest.** No scenario of any set completes earlier in another
   condition than in HU (the pair tables: 0 better in every pair with HU first); HU holds 0 ticks. It has ticks below
   min_separation in 68 of 128 scenarios and moving-robot violations in 38 (the planning test-bed: s10_02, s11_01,
   s11_02, s11_03, s12_01, s12_02, minimum 11.33 cm in s11_01 and s11_03; step 5: all six; step 5e: 26).
2. **scenario_s02_02 is not completed within the cap (704 ticks) in IU, IA-off and IA-on**, nor are its two step 5e
   copies with a timeline, scenario_s17_08 and _10 (IA-on). The human's script ends at tick 250 standing at
   (−190, 396), with no exit walk; the robot, with item_1 to deliver, stands about 60 cm away at (−237, 359) and holds
   on fallback projections of the standing human whose persistence doubles: IU 128 ticks from 374, 256 from 502;
   IA-off, IA-on and the copies 192 from 438, 384 from 630 (734 held ticks in each). HU completes at 422, as the robot
   alone. Its last release is at 166 in every condition: the result table's `completion` column (167) does not show the
   unfinished pool; the tables here count completion only with a terminal decision.
3. **Recognition against the fallback alone (IU → IA-off).** The planning test-bed: 2 earlier (s12_01 134 → 131,
   s12_02 184 → 161), 14 equal; step 5: s16_03 and _04 earlier (118 → 113); step 5e: 11 earlier, 84 equal, 11 later
   (the largest: s24_14 310 → 272, s24_26 285 → 261, s05_01 216 → 194, s05_02 233 → 214, s29_16 233 → 217 earlier;
   s24_02 283 → 301, s22_24 128 → 141, s26_48 245 → 257, s26_32 273 → 281 later). Held ticks in step 5e: IU 797,
   IA-off 1067, IA-on 1148.
4. **Moving-robot violations in IA-off where IU has none**, each with the decision in force: s03_06 tick 57 and s21_07
   tick 57 (a `recognition_changed` / replaced at 54 refused `none(below_theta)`, a standing fallback k = 2 to 57, then
   a moving fallback k = 2 at 57); s20_26 tick 99 (the same form, 96 to 99; also IA-on); s22_24 tick 136 (the same form,
   133 to 136, IU's violation at 52 instead; also IA-on); s12_02 tick 140 (the tick of an admission, `entered`,
   deliver_item(item_2), hold 0); s24_14 ticks 268 to 269 (the last decision at 191 on the admitted
   deliver_item(item_53), none after it until the violation); s26_48 ticks 180 and 184 (IA-on 180 and 183; the last
   decision at 72 on the admitted deliver_item(item_20), hold 15, none after it until 180; HU 1 violation, IU none). And
   the reverse, IU's violations that IA-off does not have: s18_26 343, s19_13 51, s20_02 247, s25_10 147, s26_16 207.
5. **Context knowledge on against off (IA-off → IA-on).** Step 5e: 3 earlier, 97 equal, 6 later; ticks below 3 / 100
   / 3; violations 3 / 100 / 3. With it on, an admission of deliver_item(item_5) at tick 0 in s05_01 and s05_02 (hold 2;
   the next decision at 40), and of deliver_item(item_4) in s16_01 (at 0, hold 5) and s16_02 (at 38, `entered`, hold
   4), and the robot violates at 27 to 29 (s05_01, s05_02, minimum 30.0 cm) and 49 to 50 / 48 to 49 (s16_01 / _02)
   before its next decision. In s05_01 and s05_02 the human's first task is coffee_break: at tick 0 no timeline fact
   holds, and the belief over H puts deliver_item(item_5) at about 0.97 (the oracle's value as well), so the gate
   clears on it from tick 0 until 23. With it off those ticks rest on
   fallback decisions (s05: no tick below; s16: one violation at 44). s23_21: admitted deliver_item(item_5) at 36, hold
   7, violations 52 to 54 (minimum 19.3 cm), where the other three conditions have none. Earlier with it on, the largest: s16_03 and
   _04 (113 → 89 and 91), s05_02 (214 → 198); later, the largest: s23_21 (172 → 179), s24_02 (301 → 313), s24_14
   (272 → 279).
6. **A standing robot passed by the human.** Most ticks below min_separation in IU and IA are a standing robot's
   (step 5e IA-off: 227 passing, 145 beside, 14 viol, 20 recede of 406). Seven step 5e scenarios have more ticks below
   in IU than in HU (s19_13 6 → 8, s20_26 12 → 16, s22_24 11 → 12, s24_02 7 → 13, s26_16 15 → 16, s26_48 11 → 14,
   s28_02 3 → 7), all with more ticks of a standing robot.
7. **The 176 copies with a timeline (IA-on):** 174 completed (the two of finding 2), 700 ticks below in 79, 27
   violations; no comparison is drawn here (one condition only).
