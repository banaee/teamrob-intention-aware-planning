# T-B3 — full_reorder beside single_task; the first full_reorder logs

A comparison table and a regression set, not an evaluation (generality is T-F's). Fixtures s80, s81, s83
(env_layout8, two tables), s20 (env_layout2) and s70 (env_layout7); `--strategy` single_task and full_reorder,
assignment prior off and on; cost realized, gate none, stop off; PYTHONHASHSEED=0; code at 2a44c65.

## The table

Completion from the world fact (the robot's last release + 1). Heads: the robot's tasks in the order it
delivered them (item numbers). Admitted: `[meta-b3]` calls with `selection=realized` (the projection admitted)
over all `[meta-b3]` calls; 0 admitted would mean the row says nothing about realized cost. Holds: executed
holds as start tick (ticks executed); none interrupted.

| fixture | prior | completion ST / FR | heads ST | heads FR | admitted ST | admitted FR | holds ST | holds FR |
|---|---|---|---|---|---|---|---|---|
| s80 | off | 265 / 224 | 6 1 7 4 | 7 4 6 1 | 6/12 | 4/11 | — | — |
| s80 | on | 265 / 224 | 6 1 7 4 | 7 4 6 1 | 6/12 | 4/11 | — | — |
| s81 | off | 268 / 224 | 6 1 7 4 | 7 4 6 1 | 8/12 | 6/11 | 40 (3) | — |
| s81 | on | 268 / 224 | 6 1 7 4 | 7 4 6 1 | 8/12 | 6/11 | 40 (3) | — |
| s83 | off | 265 / 226 | 6 1 7 4 | 7 4 1 6 | 6/12 | 8/12 | — | — |
| s83 | on | 265 / 226 | 6 1 7 4 | 7 4 1 6 | 7/12 | 8/12 | — | — |
| s20 | off | 237 / 221 | 4 6 7 | 6 4 7 | 4/10 | 4/10 | 20 (8), 31 (1) | — |
| s20 | on | 237 / 221 | 4 6 7 | 6 4 7 | 4/10 | 4/9 | 11 (8), 31 (1) | — |
| s70 | off | 186 / 186 | 2 1 | 2 1 | 3/10 | 3/10 | 61 (1) | 61 (1) |
| s70 | on | 186 / 186 | 2 1 | 2 1 | 3/10 | 3/10 | 60 (1) | 60 (1) |

- s20, one table: full_reorder takes a different head order and completes 16 ticks earlier without a hold.
- s70: the same course under both strategies; the logs differ in the decision lines alone (`[meta-cand]` against
  `[meta-ord]`, the `ordering=` field of `[meta-b3]`, the `[run]` line).

## R3 — separation inside the assessed window

Evaluation rule (corrected, TODO-90 check, `analysis/todo90_b2a_window/`): a defect is a robot STEP (a moving tick)
inside an assessed window that ends below min_separation; standing ticks are judged by whether realization projected
them (F1: the robot answers for its own motion only). The finding below is the stronger one, no sub-min_separation
tick inside a window at all.

No `[sep]` distance below min_separation (50 cm) falls inside the assessed window [trigger, T_h] of the decision
in effect, in any of the 20 runs. For information, every sub-s tick falls under a decision with no admitted
projection (no assessed window):

| run | ticks | min `[sep]` |
|---|---|---|
| s83 ST, both priors | 262–339 (completion 265) | 39.69 cm |
| s83 FR, both priors | 223–339 (completion 226; the arrival past T_h in `analysis/tb1c_realized_flip/`) | 42.87 cm |
| s20 ST, both priors | 57–58; 143–149; 231–299 (completion 237) | 37.49; 30.15; 4.23 cm |
| s20 FR, both priors | 127–135; 216–299 (completion 221) | 17.92; 3.94 cm |

## R4 — byte-identity

The eight single_task logs with a baseline regenerate byte-identical by md5: s20 and s70 against
`analysis/tb1a_destination/README.md` (T-B Q7), s80 and s81 against `analysis/tb1b_two_tables/README.md`. s83
has no single_task log in `analysis/tb1c_realized_flip/` (its sweep is full_reorder only), so its two
single_task logs had no baseline (baselined here since, below); its two full_reorder realized logs, and s80's, match that record's md5s.

## Logs (`sweep/`, local, git-ignored) — the diff target under full_reorder

Regenerated when a fixture changes. md5 at 2a44c65:

| log | md5 |
|---|---|
| s20_off | 921d61aceff9483d686744e63fb393f5 |
| s20_on | 9280684355c318deac1ec0cfe5ca6e22 |
| s70_off | 2e5c0bf17ba8ff24df211663a911c082 |
| s70_on | c37c7416c899950ceea6093369d6cf70 |
| s80_off | 004075a3e44afeef4ed611b2211f1a0b |
| s80_on | ab6e64456ff45a03c4e49d4e9e101aed |
| s81_off | f061d439f7bd5fdbac00a3bf4196ed04 |
| s81_on | 4415744aecf4c29f46c8fd787d6aaa13 |
| s83_off | 7b719acbbf4c63020146a83fbd5f3ff8 |
| s83_on | 36f29241b7f85f0255e14284d98e117e |

(files `sweep/<fixture>_full_reorder_<prior>.log`.)

s83 under single_task (realized, both priors) is baselined here too, since no earlier record holds it (Hadi,
at T-B3's close): `sweep/s83_single_task_<prior>.log`, md5 at 2a44c65:

| log | md5 |
|---|---|
| s83_single_task_off | 6d696902c38a9356a53c27764c40adc8 |
| s83_single_task_on | 4ecc5729f47b69195c5e6d67ad5e9ab6 |

## Run (repo root)

    analysis/tb3_full_reorder/sweep.sh <out_dir>

All 20 runs, and all 20 go to `sweep/` (T-L stage 3; before it, the full_reorder logs and s83's single_task logs
only): `cp <out_dir>/*.log <out_dir>/*.rec analysis/tb3_full_reorder/sweep/`, or give `sweep/` as `<out_dir>`.

## D3 (dd880be): `task_committed` is not a trigger — the logs from here on

Regenerated at dd880be with the same command, superseding the table above. Only the trigger set changed
(`shared/meta_planner.py`, `evaluate_triggers()`: `task_committed` removed; `docs/design_decisions.md`, "D3:
task_committed is not a trigger"). Against the previous logs, checked per tick: every `[sep]` line, every human
line, every `[IR] step=` and `[IR-dist]` line and the `[run]` header are byte-identical, and so is completion. What
changed: the `[meta*]` lines of the removed `task_committed` decisions (42 in these logs); and the executor's
bookkeeping, positions and ticks identical — no `_load_plan` at the grasp (the removed decision's reload of
`deliver_already_held`), a later `continue_plan` mapping `action_index 2->0` / `3->1` instead of `0->0` / `1->1`,
and `_on_task_complete` on the 4-action plan (`action_index=4 plan_len=4`) instead of the 2-action one.

HOLDS PLACED BY `task_committed` in the previous logs (their `[hold] … trigger=` field): none; no hold changed.

| log | md5 |
|---|---|
| s20_full_reorder_off | 2155ba892ceff37097da5e260a39189c |
| s20_full_reorder_on | 7da1edb6ee93bbd388446a2cb4ad8aec |
| s70_full_reorder_off | 927e0f255e8960a905efb6cfd43e49c9 |
| s70_full_reorder_on | 8e6c0dfabdb1a3822d3dcee9aa894743 |
| s80_full_reorder_off | 977403dd962b42a6209f51494afb7483 |
| s80_full_reorder_on | 121f2fe5b1f793019c1203ed1a83b868 |
| s81_full_reorder_off | a5987917b2da1cc4e4271af6685873ce |
| s81_full_reorder_on | 9a598c0ea55d9a92064263f4bd9022c8 |
| s83_full_reorder_off | 0a5a2bc13ab3c5705c9f767e84f8427a |
| s83_full_reorder_on | 7f3d9a97489fbfa4f2ae5825a771efd5 |
| s83_single_task_off | 00ed1992da92e01570d97bfcb6c3bf0f |
| s83_single_task_on | 669c440dcc011d6c9d9bed5d02dd9e13 |

## T-C2b (06093ee): the action-level human executor — the logs from here on

Regenerated at 06093ee with the same command, superseding the table above. CAUSE: the human's per-task completion
tick is dropped (`docs/design_decisions.md`, "The human action script (T-C1, decided)", AS BUILT T-C2b): its
executor is action-level and spends no tick between two tasks, and the human projection no longer carries that tick
(`HUMAN_TASK_COMPLETION_LATENCY` = 0). Against the previous logs every human line is identical once the human is
one tick earlier per task it completed before that tick (`task=` now `None`; the `_on_task_complete: human_0`
line and the human's `[planner]` lines are gone, one `[human] … primitive` line per primitive is new). Where the
human projection's shorter end reaches a hold, the hold is one tick shorter — the ruling in the AS BUILT note, not a
defect. Per log: the human's dropped ticks | first tick a world line (`[sep]`, `[IR] step=`, robot) differs |
completion (world tick) old -> new | holds (start:planned) old -> new.

| log | dropped | first diff | completion | holds old | holds new |
|---|---|---|---|---|---|
| s20_full_reorder_off | 56, 124 | 56 | 221 -> 221 | - | - |
| s20_full_reorder_on | 56, 124 | 56 | 221 -> 221 | - | - |
| s70_full_reorder_off | 56, 97, 145 | 56 | 186 -> 185 | 61:1 | - |
| s70_full_reorder_on | 56, 97, 145 | 56 | 186 -> 185 | 60:1 | - |
| s80_full_reorder_off | 55, 174 | 55 | 224 -> 224 | - | - |
| s80_full_reorder_on | 55, 174 | 55 | 224 -> 224 | - | - |
| s81_full_reorder_off | 72, 191 | 72 | 224 -> 224 | - | - |
| s81_full_reorder_on | 72, 191 | 72 | 224 -> 224 | - | - |
| s83_full_reorder_off | 98, 223 | 98 | 226 -> 226 | - | 190:2 |
| s83_full_reorder_on | 98, 223 | 98 | 226 -> 226 | - | 190:2 |
| s83_single_task_off | 98, 223 | 98 | 265 -> 265 | - | - |
| s83_single_task_on | 98, 223 | 98 | 265 -> 265 | - | - |

| log | md5 |
|---|---|
| s20_full_reorder_off | 190da00725e30e50955e4eb78ccd32f3 |
| s20_full_reorder_on | 37a0c82c9fd83bcf2e904040e07026a7 |
| s70_full_reorder_off | 7e08e1592e37715b0fea9725c649a12a |
| s70_full_reorder_on | 93a48953330beacdbb0efcba54c4538c |
| s80_full_reorder_off | 5b7fb8a80b4bd906c2fffbf472d5f413 |
| s80_full_reorder_on | 452d508e29aac60c33228e20038e1fc8 |
| s81_full_reorder_off | 47c131b72434a24837ed4d6536fe8922 |
| s81_full_reorder_on | c377e23a84e31adf834e098fe3198056 |
| s83_full_reorder_off | 2fc8cf8de5c4f9863ea28d7d522f6bde |
| s83_full_reorder_on | 730bfd280ce78befb0fed3301692b36a |
| s83_single_task_off | 3728b49a074a8cd630a43b539ac59a87 |
| s83_single_task_on | 1a45e0d17e477f34ee25d00221a2bb1a |

## T-H3: the human's script on the stack machine — the logs from here on

Regenerated after T-H3 with the same command, superseding the T-C2b table. CAUSE: every scenario's human script is a
`Script` run by the human's stack machine (`docs/design_decisions.md`, "T-H: the human behaviour model", as built
T-H3); the C1 list form is deleted. Against the T-C2b logs every line outside `[human]` is byte-identical, the human's
step lines included: the robot sees the same body. The `[human] … primitive k: <action>` lines are replaced by the
record's transitions (`entered:<task>`, `completed:<task>`), the step-0 one printed after the executor's `_load_plan`
line. Each log now has its `.rec` stream beside it (the human executor's record, one `[rec]` line per tick; the first
non-empty `.rec` baselines), git-ignored like the logs.

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| s20_full_reorder_off | 51d7e28f1250ec00fb0c04b53efc6f36 | 9f6d010e2fbc537952fa6ece4e96f469 |
| s20_full_reorder_on | 365aabf47468dd71ee75090eab258a36 | 9f6d010e2fbc537952fa6ece4e96f469 |
| s70_full_reorder_off | b021e2607f56832cdc43cb90de09e8bb | dab078d5ca51e5b378054ee6a60ccca7 |
| s70_full_reorder_on | 136b8f2838cbb0a1dd8c99bffa5d3d85 | dab078d5ca51e5b378054ee6a60ccca7 |
| s80_full_reorder_off | 45131c21bdf6a70155eb55d06f7c1995 | 8cf0930761924a3aab1f1713f3f4bf29 |
| s80_full_reorder_on | 61d72d8c85e8f4bdbba12bbae4cdcb7e | 8cf0930761924a3aab1f1713f3f4bf29 |
| s81_full_reorder_off | 9bbdb15562d6c83b21bdf6a98f43ec45 | 329590c9c1249859bfe20d107588c50a |
| s81_full_reorder_on | 3f7b3786eb420a89c2b323b7f1407b52 | 329590c9c1249859bfe20d107588c50a |
| s83_full_reorder_off | 7e5218e4e8640b0688729b857dac47e1 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| s83_full_reorder_on | b3913816203cb94cabc51562e64e4993 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| s83_single_task_off | 7d5c69a760b717a400f356800cdbd600 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| s83_single_task_on | 186db58f357d2bb33bd457e2a45287d5 | b9f1a0ec26cfa8c022b9951e9ec1b34b |

## T-H4: the record's queries and the coverage line — the logs from here on

Regenerated after T-H4 with the same command, superseding the T-H3 table. CAUSE: the loader prints one `[coverage]`
line per script entry for each robot observing the human, after the `[run]` headers (`docs/design_decisions.md`, "T-H:
the human behaviour model", as built T-H4). Against the T-H3 logs every other line is byte-identical, and every `.rec`
stream is byte-identical (its md5 unchanged).

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| s20_full_reorder_off | dfc33d336deffe06c2626674fb7ca21c | 9f6d010e2fbc537952fa6ece4e96f469 |
| s20_full_reorder_on | 009c18643ee3fc659731df9682fe3c62 | 9f6d010e2fbc537952fa6ece4e96f469 |
| s70_full_reorder_off | 42ffc9736db93ef773aa84cbed210a97 | dab078d5ca51e5b378054ee6a60ccca7 |
| s70_full_reorder_on | d939139ba4e430c7299dfd6b4dd7f575 | dab078d5ca51e5b378054ee6a60ccca7 |
| s80_full_reorder_off | 0ae7239c50a1efb172a6dd195e546204 | 8cf0930761924a3aab1f1713f3f4bf29 |
| s80_full_reorder_on | 8acd7f0596cfb665e9807fece14c80ff | 8cf0930761924a3aab1f1713f3f4bf29 |
| s81_full_reorder_off | bfad725788fa38e54e5fde6eed338bb4 | 329590c9c1249859bfe20d107588c50a |
| s81_full_reorder_on | c1a7845370c9c96b51ad66bba88dbacf | 329590c9c1249859bfe20d107588c50a |
| s83_full_reorder_off | 938770a788056decfea88a712c85b965 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| s83_full_reorder_on | d71f1095f56a7256eee1e406acc9f9dc | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| s83_single_task_off | 48a58e60036bc20165bdf7d3d52e0f15 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| s83_single_task_on | 1a5f59042de2d4c00c074fea014ed923 | b9f1a0ec26cfa8c022b9951e9ec1b34b |

## T-H follow-up: the scenario-coverage line — the logs from here on

Regenerated after the T-H follow-up with the same command, superseding the T-H4 table. CAUSE: the loader prints
one `[scenario-coverage]` line per robot observing the human, after its `[coverage]` lines: the script's composition
and scenario coverage (`docs/design_decisions.md`, "T-H: the human behaviour model", as built T-H follow-up). Against
the T-H4 logs every other line is byte-identical, and every `.rec` stream is byte-identical (its md5 unchanged).

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| s20_full_reorder_off | fd3219fea3ac0f2c2200a4819a228b0c | 9f6d010e2fbc537952fa6ece4e96f469 |
| s20_full_reorder_on | 88a9a818b2f3c638508badc5fe3c92d2 | 9f6d010e2fbc537952fa6ece4e96f469 |
| s70_full_reorder_off | f74c5d6eba853ee26299226e80b19245 | dab078d5ca51e5b378054ee6a60ccca7 |
| s70_full_reorder_on | 018df5bab595de1f17393780f173682d | dab078d5ca51e5b378054ee6a60ccca7 |
| s80_full_reorder_off | c479c77be59788c3523827a624949197 | 8cf0930761924a3aab1f1713f3f4bf29 |
| s80_full_reorder_on | 1a66f2d38ef2db57b897ac163fc59edf | 8cf0930761924a3aab1f1713f3f4bf29 |
| s81_full_reorder_off | 0bc9f94d93ae8a56442e9fd9d4657634 | 329590c9c1249859bfe20d107588c50a |
| s81_full_reorder_on | 4ba9fa0ae49750d3951a8fdb11b103c1 | 329590c9c1249859bfe20d107588c50a |
| s83_full_reorder_off | cc6125e8898e55b42f3faa36cee487a8 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| s83_full_reorder_on | 5d93baad6ee5ac87a483bf9ea99787d5 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| s83_single_task_off | 3402d6b87cb5ada4b0573f1602d000b3 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| s83_single_task_on | 11b9532998fa4a1d4cc8a9c74022f5d1 | b9f1a0ec26cfa8c022b9951e9ec1b34b |

## T-L stage 3: the serial ids — the logs from here on

Regenerated after T-L stage 3, superseding the T-H follow-up table. CAUSE: the rename to the serial ids (`docs/design_decisions.md`, "Layouts, setups and scenarios: the three artefacts of
a run", ruling 4 as amended, ruling 6); the runs do not change. Logs are named `<layout id>_<scenario id>_<run
options>.log` (ruling 6), each `.rec` beside its log; `docs/rename_table.md` maps the old tags (its last table).
Against the stage-2 logs (99563cc, run from scratch under the old ids and paired through the rename table) every log
differs in the `[run_mesa]` line alone (`layout=` and `scenario=`), and every `.rec` stream is byte-identical. T-L
stages 1 and 2 had changed the same line alone (the setup id added, then its serial id), with no section here; the
`.rec` md5s equal the T-H follow-up table's.

Regenerate from the repo root with `analysis/tb3_full_reorder/sweep.sh analysis/tb3_full_reorder/sweep`: all 20
runs are kept in `sweep/` from here on (Hadi, T-L stage 3), the `single_task` runs included.

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_03_scenario_s03_01_full_reorder_off | b5e0cf7207297420ea16b108b4a30416 | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_full_reorder_on | 1132659d63d79ad4db19ae65d7ffe3ad | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_single_task_off | 5cd1f49a2092a4107b8e3182afbac780 | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_single_task_on | 604dcb96d1a664ff29414be1df5fa7d6 | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_07_scenario_s05_01_full_reorder_off | 32c5a5067fb2aa40a9d27d4bf79c905e | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_full_reorder_on | 641da8acb13fa2052f7640b85ad8cdce | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_single_task_off | e154df49456562debdaa4dd0836d8d48 | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_single_task_on | 1ed075ccd307f73d36288b394d62cac9 | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_08_scenario_s06_01_full_reorder_off | fda5316eded9f2afdf3dc190c9001350 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_full_reorder_on | 38c80f2e69dc4fd4129a5668ed7d32ec | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_single_task_off | 0054b641ab77c15ef52fbd0e9b9a7737 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_single_task_on | bd4dea4c79485e202f2eda2b29a4f96f | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_02_full_reorder_off | 9dab2dbf04d3b10b6c83a48f62994c0c | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_full_reorder_on | 9f34a635646c527ba0c2805aa2ac6c4b | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_single_task_off | 41301096d8fa57a0691ac4b88139c97b | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_single_task_on | 0d8db6fb4067284052360722ca4756fe | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_03_full_reorder_off | 1eb4be9d9268bbbe68a472a85fe78b8f | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_full_reorder_on | ebe3d1cda8a8d81b9726503e16643f92 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_single_task_off | a13559d3096bea7722d04b0042128eaf | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_single_task_on | 5c32517b00b75d0be3cf293c4beb5f27 | b9f1a0ec26cfa8c022b9951e9ec1b34b |

## T-D R and E Stage 1: the recognizer without `unknown` — the logs from here on

Regenerated at the T-D Stage 1 build (27 September 2026, cycle 1 session 1.3), superseding the T-L stage 3 table.
CAUSE: a behaviour change of the recognizer (`docs/design_decisions.md`, "T-D R and E"): the `unknown` hypothesis,
u and the grade are gone and the belief is normalised over the live hypothesis set H (R1, R6); the `[IR]` line
carries the lifecycle state, the adequacy finding and the members' tail probabilities; the `[run]` header names
the test level and the body's speed; the `[IR-boundary]` line no longer says "+ unknown"; `none(unknown)` refusals
are gone. The `.rec` streams are byte-identical to the stage 3 ones (the human does not react to the robot). The
gate is unchanged; its input is now the leader's share over H, so admissions moved, and in prior-off runs the
robot's own remaining item is admitted once it is the lone live task after the human's last task (world lines
differ from that tick). Measured in session 1.4, not corrected here. Command: `analysis/tb3_full_reorder/sweep.sh analysis/tb3_full_reorder/sweep`.

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_03_scenario_s03_01_full_reorder_off | 0287781445c0771c49fe8d43572b058e | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_full_reorder_on | c9b69d11c05798eb0dea8fc97bc7fa88 | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_single_task_off | fed4cfcb7688034d07df4a0291ab3d22 | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_single_task_on | 9c37ad92ed42bbdd86cd313aa48a7c81 | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_07_scenario_s05_01_full_reorder_off | 54b85368a5e96c26a49867ca89762e78 | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_full_reorder_on | c66a587a070c1ef15529a71e72b8b320 | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_single_task_off | e7f104adff968cfb4ee628abf241d389 | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_single_task_on | c8477df1c0fe1b857012ea7db39f59b1 | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_08_scenario_s06_01_full_reorder_off | d1be76378eb7238911194a6b844ee99e | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_full_reorder_on | d0898e09833691bb85152ca1f4fad03a | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_single_task_off | 3fabb9df8c1bdbe4330ac035f290c33e | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_single_task_on | fda3109d2104c80d9d9b9a0d9e9c44e3 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_02_full_reorder_off | 50257f19df3fbce7482da3d4fcf17324 | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_full_reorder_on | a98099bdca62e7e31da9985d7e8588c3 | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_single_task_off | c27ccea8afd0bcb8d60efa80f751ff39 | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_single_task_on | e784144f2905a0bcb1f4a53512f272a8 | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_03_full_reorder_off | 0e6eae85c312d4da0471ec2960c6f79f | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_full_reorder_on | 358511c6c9c6198045ea644eeec4e0d4 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_single_task_off | 266dff09277761f18987200b1d540d15 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_single_task_on | 00a2702674df81f76c4ea50d2c1d5538 | b9f1a0ec26cfa8c022b9951e9ec1b34b |

## T-D Stage 1, E6 amended: stationary-phase members — the logs from here on

Regenerated at cycle 1 session 1.3b (27 September 2026), superseding the T-D R and E Stage 1 table. CAUSE: E6
amended (design_decisions.md, "T-D R and E"): a stationary phase within its priced duration is a member of the
adequacy test with S = 1. Only `[IR]` lines differ from the Stage 1 logs, and in them only the finding and the
tails (members added at S = 1; the belief and every existing member's S unchanged); every other line and the
`.rec` streams are byte-identical. Same commands as the section above.

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_03_scenario_s03_01_full_reorder_off | a1be6065a3169f88d3a31f055af8b5a8 | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_full_reorder_on | 2b40778b258aacbb239be453a650b9d0 | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_single_task_off | 5ac10a84262310b487474e3a503abb80 | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_single_task_on | cc2407b0a7baa038c827dce6ad07ae1a | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_07_scenario_s05_01_full_reorder_off | ed09ebd80a196948d6ad0e84a87b2745 | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_full_reorder_on | f58c3a3e89c3b73eb3ba60b5e14b947b | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_single_task_off | a76d2899a4aa89576776fbbad617e3f2 | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_single_task_on | 7fd86fd9b82820a2c1450ebb224c2d05 | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_08_scenario_s06_01_full_reorder_off | be05b6251fcc3c5547999bcb30d0f3a7 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_full_reorder_on | b9f756085305e49091005cbde9dc27ba | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_single_task_off | 8af7df2af74e80fae6e7bbf8a6fe592f | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_single_task_on | 2cf7861e47fa192870f8d8fb4b4d949e | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_02_full_reorder_off | 259da95765afaeaea012970cc7a7c32c | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_full_reorder_on | 995107cb8473be46307af9122cac5b6d | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_single_task_off | 8b02c0d458e525332d8d11136591b884 | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_single_task_on | e1d36827fb3bc877013eb17137265d4e | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_03_full_reorder_off | 94a9b707f68c58585001aa0cd16edecb | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_full_reorder_on | d395d91a396a323670b846f0ffbf1c88 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_single_task_off | 386969055f6f4028f019bdd5fc14d357 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_single_task_on | d11fbca7c112a7e847fe5fd0478a2d63 | b9f1a0ec26cfa8c022b9951e9ec1b34b |

## T-D cycle 1.5b: E8, E9, E10 and G1 — the logs from here on

Regenerated at cycle 1 session 1.5b (27 September 2026), superseding the "E6 amended" table above. CAUSE: E8 (the
advance tick a member at S = 1), E9 (s_exp by the Projector's attribution), E10 (the belief's evidence per phase
L(v·D)) and G1 (the guard on admission: `_clears_gate` also requires the leader's hypothesis adequacy to be adequate;
new refusals `none(leader_no_observation)`, `none(leader_inadequate)`); design_decisions.md, "T-D R and E", "1.5
rulings". Every `[IR]` line on a live tick differs (the new `leader_adequacy=` field; the tails under E8, E9); `[IR-dist]` differs
where standing now charges the belief (E10); decisions differ at admissions (G1) and wherever the belief moved.
World lines (the agents' per-tick lines) changed in 8 of 20 (s03_01 single_task on/off, s05_01 both strategies on/off, s06_03 both strategies off). The `.rec` streams are byte-identical to the table
above. Per-run diff and the acceptance: `analysis/td_stage1b/` (`baseline_diff.txt`, REPORT.md).

Command (from the repo root; the same as the sections above; restated because 7f4559a had dropped them, restored in 1.5c):
`analysis/tb3_full_reorder/sweep.sh analysis/tb3_full_reorder/sweep`

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_03_scenario_s03_01_full_reorder_off | 014e7d4db38f6f043f9881d35af69c89 | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_full_reorder_on | 28bf81dc4d3f8b3536ff6023149e16c6 | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_single_task_off | 4d047d15a6b6bd77221358c163d483dc | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_single_task_on | 521ebeac3f97ab4106f1174c6198460f | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_07_scenario_s05_01_full_reorder_off | e2b722adea65ff98a60aa85e993bf2d3 | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_full_reorder_on | f6a9ecbd880e01275de6655c5ee88381 | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_single_task_off | e320797265ceb5a4572adcfdc5a4b27a | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_single_task_on | 24d53d63e6a5fccbd14c13e05e5c74e8 | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_08_scenario_s06_01_full_reorder_off | 98d32dbd4fe4ccdf6f4c5d00f25a2ccc | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_full_reorder_on | 25a26eb6b44f3779dee9f94868554765 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_single_task_off | 9d2229e6ae945886574b2c261780b2a7 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_single_task_on | 2c2a9d79ef4932252f3afffe47c0887b | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_02_full_reorder_off | 3e4da85ded842e2fcaf85bcee0498b7b | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_full_reorder_on | d71ffb6539ffd04dcef4dc26ea0bf35e | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_single_task_off | 2824fd4ef817d8b87e358ea8ceca09dc | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_single_task_on | 5cafd2c3debfef3eece74af7be7f1073 | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_03_full_reorder_off | 3ade34d4da811f67c654b7a1a2f7ac8c | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_full_reorder_on | dbd8e0e7adab2415edd8d7db9209c7f7 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_single_task_off | 7730d87a85035f48362cc265d34666b5 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_single_task_on | 3a15f70a05d37e5e4d8e56134c6eccce | b9f1a0ec26cfa8c022b9951e9ec1b34b |

## T-D cycle 1.5c: E6 second amendment — the logs from here on

Regenerated at cycle 1 session 1.5c (27 September 2026), superseding the 1.5b table above. CAUSE: E6 amended a second
time (design_decisions.md, "T-D R and E"): a stationary tick with s ≤ s_exp in any phase with s_exp > 0 is an
observation with S = 1 (the latency tick after a grasp and after a boundary), and no hypothesis is a member on a
boundary tick. `[IR]` lines differ in the finding, the leader's adequacy and the tails on those ticks; `[IR-dist]`
is identical on every common tick (L = 1 there before and after; runs that end later add exhausted ticks); admissions that waited for the first walking tick after a boundary now
come on the latency tick (b + 1). World lines changed in 5 of 20 (s03_01 single_task on, s05_01 both strategies on, s06_03 both strategies off). The `.rec` streams are byte-identical to the
table above. Same command as the 1.5b section. Diff and acceptance: `analysis/td_stage1b/` (`baseline_diff_15c.txt`,
REPORT.md, section 1.5c).

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_03_scenario_s03_01_full_reorder_off | 7c24077db74b82836a134a91ae698447 | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_full_reorder_on | a681cf00d32963379921a590f9ec2a3c | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_single_task_off | 79b7def70dce00ec7e697500d5a5a76a | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_single_task_on | 0cf93e422dccf00ea52c688ad1e7411d | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_07_scenario_s05_01_full_reorder_off | 8572a86a65397b7bc1b0f582696d84bf | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_full_reorder_on | 6ee26f2d59644c700bbf9c81fb0db5a0 | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_single_task_off | 4fe0a73cb66172b723134540f8e453cd | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_single_task_on | 6908379e1152c6ea74813cf39bea418f | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_08_scenario_s06_01_full_reorder_off | a57beb0042671d6f864617087709388f | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_full_reorder_on | 6665cba47edcc0ffe5c4c33b893b9274 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_single_task_off | 7b2858b5209cbb3132914b9a0fbfef29 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_single_task_on | badc5d849f98902b889bb4ba53454f40 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_02_full_reorder_off | e5c29001b3851bb48bbf2be8291765d9 | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_full_reorder_on | 3417807b96cf69e68e9579928b4957f8 | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_single_task_off | c78a186d38f508fde6938a6ef0de4237 | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_single_task_on | 56d53436e78a880d0492d927a8b86997 | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_03_full_reorder_off | 762b472bae87c0f4114403e7f4a884ec | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_full_reorder_on | 5346b3572f22bf62287d6d648aa012d9 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_single_task_off | 0fe101800bf026ff5f7c19fc0c9cbb91 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_single_task_on | 3080642740a0e1c84180c4d2c9a93f7a | b9f1a0ec26cfa8c022b9951e9ec1b34b |

## IRB.2b: the cognitive loop does not end with the task pool — the logs from here on

Regenerated at IRB.2b (27 September 2026), superseding the 1.5c table above. CAUSE: the robot observes and recognizes
on every tick; after its terminal return it evaluates no trigger, decides nothing and does not step the executor
(design_decisions.md, "The cognitive loop does not end with the task pool"). Each log gains `[IR]` and `[IR-dist]`
lines from the tick after the declared completion tick to the run's last tick (all but
env_layout_03_scenario_s03_01_full_reorder_off, whose robot does not complete: TODO-118), and within every tick the robot's
`[IR]` and `[IR-dist]` lines now precede its `[meta-trig]` line, so every md5 changed. Criterion, met in all 20: the
log with every `[IR*]` line removed is byte-identical to the 1.5c log, the `[IR*]` lines are byte-identical up to and
including the declared tick, and the `.rec` streams are byte-identical to the table above. Command: `analysis/tb3_full_reorder/sweep.sh analysis/tb3_full_reorder/sweep`.
Check and measurements: `analysis/irb2b_exposed_interval/` (`baseline_diff.txt`, REPORT.md).

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_03_scenario_s03_01_full_reorder_off | 6713aefbe6f089c2f01c6fcf9a3397e6 | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_full_reorder_on | 67936925fd7712dcf33667cd2808147a | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_single_task_off | 2deffa36ed5510eb23e6bfb1797d63fd | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_single_task_on | cd0c43a79ff4dd79a388d25c15d6b3b7 | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_07_scenario_s05_01_full_reorder_off | 3184614616b190510a25493b0b5d9a69 | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_full_reorder_on | 92281b29b5c2afa3ae6bb3befb2f12ef | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_single_task_off | ee5495dcf581dbf806f744269090dc5d | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_single_task_on | 6625b270bec3d306ecd2619affc99c1b | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_08_scenario_s06_01_full_reorder_off | 9c72f9afa843ff8a10318457b7ddd560 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_full_reorder_on | 80e4303594ab810034033fb1243f35ee | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_single_task_off | 38cd2f289ad21f63152c9e58841f5d16 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_single_task_on | 33775f4d11d09f121657e15658ca7d09 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_02_full_reorder_off | 86f0855ccbfb0d019bb9eade41fd3f14 | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_full_reorder_on | fa0f65f613a46b95abaaf60d9e459b39 | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_single_task_off | b6b8d3f7ea45baaf305a8ce403035bb7 | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_single_task_on | ea5d850cad1da96d4bb1955dfce212c6 | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_03_full_reorder_off | 726a0c8a87a9b4db210d96a7eb016bd6 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_full_reorder_on | 825dd5add61122d239b199f5b42ce1f5 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_single_task_off | 76dd0fdce3805e7e6318907ddf84cb34 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_single_task_on | e7d1079712b0f6b544a34e5f24060c31 | b9f1a0ec26cfa8c022b9951e9ec1b34b |

## L-build: T-D L, the belief lifecycle — the logs from here on

Regenerated at L-build (28 September 2026), superseding the IRB.2b table above. CAUSE: design_decisions.md, "T-D L: the
belief lifecycle", as amended on the L-records report: the episode boundary is the observed agent's completion of a
terminal action (L1); a hypothesis is retired while its terminal fact holds and re-enters at 1/|H| (L4, `[IR-reentry]`,
new); `recognition_changed` also fires on the belief's episode boundary (L5 B) and on the recorded hypothesis's
inadequacy (retraction, L2 (ii)). Two format changes reach every log: `[meta-trig]` names the condition of a
`recognition_changed` (` cause=entered | replaced | boundary | retraction`), and `[IR-boundary]` names the completed
action (`completed place(item_2,kitting_table_0):` for `completed a task:`); so every md5 changed. No criterion of
identity (L changes behaviour); the `.rec` streams are byte-identical to the table above in all 20. With the two
format changes undone (`analysis/l_build/baseline_diff.py`): identical in 10 of 20 (L03 s03_01_full_reorder_on, L03 s03_01_single_task_off, L03 s03_01_single_task_on, L08 s06_01_full_reorder_on, L08 s06_01_single_task_on, L08 s06_02_full_reorder_on, L08 s06_02_single_task_on, L08 s06_03_full_reorder_off, L08 s06_03_full_reorder_on, L08 s06_03_single_task_on); the
recognizer's lines and the triggers moved, the robot's behaviour not, in none; the robot's behaviour
(`[meta]`, `[hold]`, `[sep]`, its lines) moved in L03 s03_01_full_reorder_off, L07 s05_01_full_reorder_off, L07 s05_01_full_reorder_on, L07 s05_01_single_task_off, L07 s05_01_single_task_on, L08 s06_01_full_reorder_off, L08 s06_01_single_task_off, L08 s06_02_full_reorder_off, L08 s06_02_single_task_off, L08 s06_03_single_task_off. Each moved number with its ticks and cause:
`analysis/l_build/REPORT.md`. Command: `analysis/tb3_full_reorder/sweep.sh analysis/tb3_full_reorder/sweep`.

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_03_scenario_s03_01_full_reorder_off | ad2b5de6932c59c78b687083788d6c4f | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_full_reorder_on | ebc8e72bf34b85d10f3f4e1c528fefea | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_single_task_off | 571105d0c3f20ade6a4d35d1765d855a | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_single_task_on | 853c74baf3ec2e15470d60857ad5f0ff | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_07_scenario_s05_01_full_reorder_off | 6f548c9c88d230bb1ce6e75ea96e2c0d | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_full_reorder_on | 9977b20a956f7c88610ee984c60f101a | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_single_task_off | 7584eda98d1fa912966c45020c27f61e | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_single_task_on | c22a3812a7fd4d189cacec6b3fadd13d | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_08_scenario_s06_01_full_reorder_off | 5b3c13c90958233b456b6e704d65e2f6 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_full_reorder_on | 28eb0514c3371c34114d56cca6e13517 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_single_task_off | a376a7d307bd268647f91d2dc2c38ec3 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_single_task_on | 890bcb753853e38ee7150cdf833e448c | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_02_full_reorder_off | 746c8d9845325557bf60d9a8cbdeb940 | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_full_reorder_on | 0b56e9b6d8e0e96bb42fa2a5de0a3714 | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_single_task_off | 82c68826f001529d8cff41530d8fb835 | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_single_task_on | bb5d442ae6ade49f2ef213c9659ff303 | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_03_full_reorder_off | 658eae46cb4e4d2f044791fc83a38481 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_full_reorder_on | 526f6fa31a183744edbf616cfb10dfd0 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_single_task_off | 1dd689cd41d4fcd47f9f2e0fbe47ea8d | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_single_task_on | 3afe6174d62b0a16686d25229d5a2421 | b9f1a0ec26cfa8c022b9951e9ec1b34b |

## P-build: T-D P, the fallback projection — the logs from here on

Regenerated at P-build (28 September 2026), superseding the L-build table above. CAUSE: design_decisions.md, "T-D P:
the fallback projection": where admission refuses and a human is observed, the decision realizes against the fallback
projection (the human's observed position and last displacement: standing, or a straight continuation to the
workspace boundary or the first fixed object's arrival radius, over each candidate's span); a candidate whose violation
is cleared only by the projection's end is refused (` refused=fallback` on `[meta-cand]`), and with none eligible the
robot waits without a task (`[meta] … wait`, `[meta-b3] … selection=wait`). Format: `[meta-proj]` names a fallback as
`projection=fallback refused=<the refusal's reason>`, so every log whose run refused an admission changed md5. No
criterion of identity (P changes behaviour). The `.rec` streams are byte-identical to the table above in all 20; with
the prior on, the recognizer's lines (`[IR]`, `[IR-…]`) are byte-identical in every run; with P's format additions
undone, the first differing line of every changed run is at tick 0, a decision under the fallback. WAITS: a run whose
robot is still waiting at its last tick has no completion tick; the table records "waits: occupied target (X)" for it
(the human's script ends standing at the robot's delivery table; the six scripts predate T-C2c's authoring convention
and are not edited; design_decisions.md, "T-D P", the deadlock). Completion is the world tick (T6), before (L-build) and
after. Command: `analysis/tb3_full_reorder/sweep.sh analysis/tb3_full_reorder/sweep`.

| log | md5 (.log) | md5 (.rec) | completion before | completion after |
|---|---|---|---|---|
| env_layout_03_scenario_s03_01_full_reorder_off | a2be0927cd2f2115051706aa66751ddd | 9f6d010e2fbc537952fa6ece4e96f469 | 227 | waits: occupied target (X), from 121 |
| env_layout_03_scenario_s03_01_full_reorder_on | 8e0a521fd1fe98d31f9a290f595937ee | 9f6d010e2fbc537952fa6ece4e96f469 | 221 | waits: occupied target (X), from 121 |
| env_layout_03_scenario_s03_01_single_task_off | 105842090c70cdc6b9994257a9acfbf7 | 9f6d010e2fbc537952fa6ece4e96f469 | 236 | waits: occupied target (X), from 121 |
| env_layout_03_scenario_s03_01_single_task_on | 3679a675eab527fd729ce624de65057f | 9f6d010e2fbc537952fa6ece4e96f469 | 238 | waits: occupied target (X), from 121 |
| env_layout_07_scenario_s05_01_full_reorder_off | 4a7e68b4d571d009e85c9e86b3f4aae7 | dab078d5ca51e5b378054ee6a60ccca7 | 194 | 206 |
| env_layout_07_scenario_s05_01_full_reorder_on | 25444962f3ac2f96a40f7047a43915f0 | dab078d5ca51e5b378054ee6a60ccca7 | 194 | 204 |
| env_layout_07_scenario_s05_01_single_task_off | 8fb8f82652c1648218fa08677ac94263 | dab078d5ca51e5b378054ee6a60ccca7 | 194 | 175 |
| env_layout_07_scenario_s05_01_single_task_on | dcb6b9a015d7ea7537920c998ced312d | dab078d5ca51e5b378054ee6a60ccca7 | 194 | 175 |
| env_layout_08_scenario_s06_01_full_reorder_off | 70b0875d92c479be9af11b195ebfe5c2 | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 225 |
| env_layout_08_scenario_s06_01_full_reorder_on | ef34c4c39f7dd5a4e30e35e83dcf3d9a | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 224 |
| env_layout_08_scenario_s06_01_single_task_off | cdb5bb197539112033717b0e5608dbba | 8cf0930761924a3aab1f1713f3f4bf29 | 265 | not complete in 340 steps |
| env_layout_08_scenario_s06_01_single_task_on | 7ec8c5862d00214b9d0a172bd94eb533 | 8cf0930761924a3aab1f1713f3f4bf29 | 265 | 267 |
| env_layout_08_scenario_s06_02_full_reorder_off | 7b694121c1dc0d5d6a57c224b4582e99 | 329590c9c1249859bfe20d107588c50a | 224 | 226 |
| env_layout_08_scenario_s06_02_full_reorder_on | fb19bfb7f5dfde9b8c06371aa1b184d5 | 329590c9c1249859bfe20d107588c50a | 224 | 225 |
| env_layout_08_scenario_s06_02_single_task_off | 7e1444ef0c42696d515d9cd138c7dc2d | 329590c9c1249859bfe20d107588c50a | 267 | 262 |
| env_layout_08_scenario_s06_02_single_task_on | 6c39f3d1d31e1f6a1199be193ca6790f | 329590c9c1249859bfe20d107588c50a | 267 | 269 |
| env_layout_08_scenario_s06_03_full_reorder_off | 5b3ee082a1e6cc81102aaabe822a6f87 | b9f1a0ec26cfa8c022b9951e9ec1b34b | 340 | 240 |
| env_layout_08_scenario_s06_03_full_reorder_on | 96cc0b0eff7c5766894e22079ceeae19 | b9f1a0ec26cfa8c022b9951e9ec1b34b | 226 | waits: occupied target (X), from 220 |
| env_layout_08_scenario_s06_03_single_task_off | 47012247ceb9886d6de9102732ecae8c | b9f1a0ec26cfa8c022b9951e9ec1b34b | 282 | waits: occupied target (X), from 238 |
| env_layout_08_scenario_s06_03_single_task_on | 3eeb80a594e0eb58f231adb1f8d8fbc3 | b9f1a0ec26cfa8c022b9951e9ec1b34b | 265 | waits: occupied target (X), from 220 |

## P4-build: T-D P4, persistence, and projection_expired — the logs from here on

Regenerated at P4-build (28 September 2026), superseding the P-build table above. CAUSE: design_decisions.md, "T-D P",
P4 and Q6: the fallback projects the observed persistence only (a straight run of k ticks continued k ticks, cut at the
workspace boundary or the first fixed object with no stand after it; a stand of k ticks held k ticks; no previous
observation, none), realized as any projection (F1), and `projection_expired` re-decides when the fallback a decision
rested on reaches its end (`[meta-trig] … trigger=projection_expired`, new); the refusal and the wait of the P-build
are removed. No criterion of identity (P4 changes behaviour). The `.rec` streams are byte-identical to the table above
in all 20; with the prior on, the recognizer's lines are byte-identical to the L-build table's. A run whose robot has
not delivered its last item at the run's last tick is recorded as "does not complete: occupied target (X), holds
lengthening, from <tick>": the human's script ends standing at the robot's delivery table (the scripts predate T-C2c's
authoring convention and are not edited), and from the first hold on that final stand the robot holds and
reconsiders at each expiry of a longer stand (scenario_s01_06 prior on, 800 steps: expiries at 165, 213, 309, 501,
holds 48, 96, 192, 384, never complete). Completion is the world tick (T6), before (P-build; "waits" there) and after.
Command: `analysis/tb3_full_reorder/sweep.sh analysis/tb3_full_reorder/sweep`.

| log | md5 (.log) | md5 (.rec) | completion before (P-build) | completion after (P4) |
|---|---|---|---|---|
| env_layout_03_scenario_s03_01_full_reorder_off | 3ba26bee9ddc5ccced03a269fd6a6585 | 9f6d010e2fbc537952fa6ece4e96f469 | waits: occupied target (X) | does not complete: occupied target (X), holds lengthening, from 124 |
| env_layout_03_scenario_s03_01_full_reorder_on | 504dd5829844a65c828efd2cfa245d31 | 9f6d010e2fbc537952fa6ece4e96f469 | waits: occupied target (X) | does not complete: occupied target (X), holds lengthening, from 124 |
| env_layout_03_scenario_s03_01_single_task_off | 928621c9a18cea06b1b17ecf2f5143df | 9f6d010e2fbc537952fa6ece4e96f469 | waits: occupied target (X) | does not complete: occupied target (X), holds lengthening, from 142 |
| env_layout_03_scenario_s03_01_single_task_on | d0cd58ea792b33693a990d4f079bff5a | 9f6d010e2fbc537952fa6ece4e96f469 | waits: occupied target (X) | does not complete: occupied target (X), holds lengthening, from 142 |
| env_layout_07_scenario_s05_01_full_reorder_off | a213dd3b9c20b73add34b4fbea91ef6a | dab078d5ca51e5b378054ee6a60ccca7 | 206 | 198 |
| env_layout_07_scenario_s05_01_full_reorder_on | 5d7a8e1c4e1f7341091c9a66d07a25ad | dab078d5ca51e5b378054ee6a60ccca7 | 204 | 194 |
| env_layout_07_scenario_s05_01_single_task_off | 2e09c47f47e86276a1c590e9c2b3beae | dab078d5ca51e5b378054ee6a60ccca7 | 175 | 198 |
| env_layout_07_scenario_s05_01_single_task_on | 29861d94faf3dec03cb4165471d65b5f | dab078d5ca51e5b378054ee6a60ccca7 | 175 | 194 |
| env_layout_08_scenario_s06_01_full_reorder_off | 01738643503d860be585f4b3c1be17f7 | 8cf0930761924a3aab1f1713f3f4bf29 | 225 | 224 |
| env_layout_08_scenario_s06_01_full_reorder_on | bfaeba739db5cb7f578f5f0e7ca84750 | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 224 |
| env_layout_08_scenario_s06_01_single_task_off | 1aff98e410789949a7ab283f8b972609 | 8cf0930761924a3aab1f1713f3f4bf29 | not complete in 340 steps | 265 |
| env_layout_08_scenario_s06_01_single_task_on | 1618a7efff2c9193f6204f54015f910d | 8cf0930761924a3aab1f1713f3f4bf29 | 267 | 265 |
| env_layout_08_scenario_s06_02_full_reorder_off | b70852b1ce7cab9a8e9beb7764e760d0 | 329590c9c1249859bfe20d107588c50a | 226 | 224 |
| env_layout_08_scenario_s06_02_full_reorder_on | 7b7ec37c2c8fc80e9eeda7b97f831d3b | 329590c9c1249859bfe20d107588c50a | 225 | 224 |
| env_layout_08_scenario_s06_02_single_task_off | d7506eae987c2276028a9d5374692659 | 329590c9c1249859bfe20d107588c50a | 262 | 267 |
| env_layout_08_scenario_s06_02_single_task_on | aa88a8cd08807205b66829d1e1b402d9 | 329590c9c1249859bfe20d107588c50a | 269 | 267 |
| env_layout_08_scenario_s06_03_full_reorder_off | 0dd6d1f4aeab7a8dab96987ee884da8b | b9f1a0ec26cfa8c022b9951e9ec1b34b | 240 | 340 |
| env_layout_08_scenario_s06_03_full_reorder_on | 9bdf7aed2df3252bf2c26a8f08a9b7e5 | b9f1a0ec26cfa8c022b9951e9ec1b34b | waits: occupied target (X) | 226 |
| env_layout_08_scenario_s06_03_single_task_off | f7d614cb4b15b5fe477675b6d075a8af | b9f1a0ec26cfa8c022b9951e9ec1b34b | waits: occupied target (X) | 304 |
| env_layout_08_scenario_s06_03_single_task_on | 6f0af33b82c044874e1811d88ee1329c | b9f1a0ec26cfa8c022b9951e9ec1b34b | waits: occupied target (X) | 268 |

CORRECTION (Track 2.5, 29 September 2026; the table above is left as written): the "340" cells are completions, not the run's end: `env_layout_08_scenario_s06_03_full_reorder_off` completes at 238 (its last release 237; the log declares `all tasks complete` at 238). The reader counted every `action=place micro=release` line, and after its pool empties the robot's per-tick line keeps its last action and micro (`task=None action=place micro=release`), so the last such line was the run's last tick, 339. `analysis/tb1a_destination/sep_classes.py` (Track 2.5) counts only the releases made while the robot has a task. The "340" cells of the earlier tables of this file are most likely the same reader's artefact; their logs are not kept, so this is not verified.

## 2.5: the exit walk on the six regression scripts (Track 2.5) — the logs from here on

Regenerated at Track 2.5 (29 September 2026), superseding the P4-build table above. CAUSE: `docs/assumptions.md` 1.1:
the human scripts of scenario_s01_01, s01_06, s02_01, s03_01, s04_01 and s06_03 end with the exit walk
`go_to("corner_SE")` (52295f7), and env_layout_02 and env_layout_08 declare the landmark corner_SE. The other
scenarios' scripts are unchanged; their logs and `.rec` streams are byte-identical to the P4-build table (env_layout_08's
new landmark moved nothing). The six scripts' `.rec` streams change from the tick the exit walk begins. Completion is
the world tick (T6), read by `analysis/tb1a_destination/sep_classes.py`: the tick after the robot's last release made
while it has a task; the "before" column is the same reader on the P4-build logs (one cell differs from that table, 238 for its "340"; the correction above). The `[sep]` minimum is
of the continuous distance; viol / stand / recede are F1's classes (`analysis/f1_robot_responsible/evaluate.py`, its
rule copied into the reader) of the ticks whose continuous minimum lies below min_separation (50 cm): the
near-encounters of `docs/assumptions.md` 4.6.
The four former occupied-target logs of scenario_s03_01 complete (off / on): single_task 266 / 238, full_reorder
265 / 221. scenario_s06_03 (its human differs from 222): full_reorder 236 (was 238) / 226 (unchanged), single_task
316 (was 304) / 272 (was 268). The other twelve logs are byte-identical.
Commands: `analysis/tb3_full_reorder/sweep.sh analysis/tb3_full_reorder/sweep`; `analysis/tb1a_destination/sep_classes.py analysis/tb3_full_reorder/sweep`.

| log | md5 (.log) | md5 (.rec) | completion before (P4) | completion after (2.5) | [sep] min, continuous (tick) | viol | stand | recede |
|---|---|---|---|---|---|---|---|---|
| env_layout_03_scenario_s03_01_full_reorder_off | 9498d8c769254b555b6b54e9bb60a33f | 515647f63e1b047aab15b0dc0ac91d08 | does not complete: occupied target (X) | 265 | 90.84 (125) | 0 | 0 | 0 |
| env_layout_03_scenario_s03_01_full_reorder_on | db49fd442217874483622573696366fe | 515647f63e1b047aab15b0dc0ac91d08 | does not complete: occupied target (X) | 221 | 90.84 (125) | 0 | 0 | 0 |
| env_layout_03_scenario_s03_01_single_task_off | dec9a6b025cb410dc17cdcb4ebc47d5b | 515647f63e1b047aab15b0dc0ac91d08 | does not complete: occupied target (X) | 266 | 48.25 (57) | 1 | 0 | 1 |
| env_layout_03_scenario_s03_01_single_task_on | 615410beadd91bd3e6bdf38ba0a22c43 | 515647f63e1b047aab15b0dc0ac91d08 | does not complete: occupied target (X) | 238 | 60.15 (58) | 0 | 0 | 0 |
| env_layout_07_scenario_s05_01_full_reorder_off | a213dd3b9c20b73add34b4fbea91ef6a | dab078d5ca51e5b378054ee6a60ccca7 | 198 | 198 | 58.31 (25) | 0 | 0 | 0 |
| env_layout_07_scenario_s05_01_full_reorder_on | 5d7a8e1c4e1f7341091c9a66d07a25ad | dab078d5ca51e5b378054ee6a60ccca7 | 194 | 194 | 58.31 (25) | 0 | 0 | 0 |
| env_layout_07_scenario_s05_01_single_task_off | 2e09c47f47e86276a1c590e9c2b3beae | dab078d5ca51e5b378054ee6a60ccca7 | 198 | 198 | 58.31 (25) | 0 | 0 | 0 |
| env_layout_07_scenario_s05_01_single_task_on | 29861d94faf3dec03cb4165471d65b5f | dab078d5ca51e5b378054ee6a60ccca7 | 194 | 194 | 58.31 (25) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_full_reorder_off | 01738643503d860be585f4b3c1be17f7 | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 224 | 412.25 (105) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_full_reorder_on | bfaeba739db5cb7f578f5f0e7ca84750 | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 224 | 412.25 (105) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_single_task_off | 1aff98e410789949a7ab283f8b972609 | 8cf0930761924a3aab1f1713f3f4bf29 | 265 | 265 | 153.74 (166) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_single_task_on | 1618a7efff2c9193f6204f54015f910d | 8cf0930761924a3aab1f1713f3f4bf29 | 265 | 265 | 153.74 (166) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_02_full_reorder_off | b70852b1ce7cab9a8e9beb7764e760d0 | 329590c9c1249859bfe20d107588c50a | 224 | 224 | 346.07 (114) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_02_full_reorder_on | 7b7ec37c2c8fc80e9eeda7b97f831d3b | 329590c9c1249859bfe20d107588c50a | 224 | 224 | 346.07 (114) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_02_single_task_off | d7506eae987c2276028a9d5374692659 | 329590c9c1249859bfe20d107588c50a | 267 | 267 | 63.37 (73) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_02_single_task_on | aa88a8cd08807205b66829d1e1b402d9 | 329590c9c1249859bfe20d107588c50a | 267 | 267 | 63.37 (73) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_03_full_reorder_off | d618371426083d9dbb12544fe0384904 | c9c444622f25d15abfd849fc495db540 | 238 | 236 | 90.80 (220) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_03_full_reorder_on | 14f93fee856ed59854e821047ccee258 | c9c444622f25d15abfd849fc495db540 | 226 | 226 | 54.58 (223) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_03_single_task_off | d5408bc3f3b37688872513771ac37200 | c9c444622f25d15abfd849fc495db540 | 304 | 316 | 70.62 (265) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_03_single_task_on | 7bd23cd70a937187b48cb0b6ea0b1848 | c9c444622f25d15abfd849fc495db540 | 268 | 272 | 28.69 (246) | 0 | 3 | 1 |

## G-build: T-D G, admission requires warrant — the logs from here on

Regenerated at G-build (29 September 2026), superseding the 2.5 table above. CAUSE: design_decisions.md, "T-D G:
admission" (AD1 to AD4): the gate also requires the leader to be warranted (commitment: one of the observed human's
assigned tasks, prior on; or the recognizer's observation warrant), and refuses an unwarranted leader as
`none(leader_unwarranted)`; the `[IR]` line ends with `warrant=[<key>=none|observation ...]` over the live
hypotheses, and `[meta-proj] projection=built` names its warrant source (`warrant=commitment`, `observation` or
both). Every log's md5 changes (the `[IR]` field). The diff rule checked on every log against the 2.5 logs: the `.rec`
streams byte-identical in all; prior on, every `[IR*]` line byte-identical once the trailing ` warrant=[...]` is removed,
and every other line identical once `[meta-proj]`'s ` warrant=...` is removed, except in the prior-on runs listed
below, whose first difference is a moved admission of a foreseeable task. Prior on, commitment warrant covers every
assigned task, so only admissions of foreseeable tasks can move. Completion is the world tick (T6),
`analysis/tb1a_destination/sep_classes.py` on both sets; the `[sep]` minimum of the continuous distance and F1's
classes (`docs/assumptions.md` 4.6) as in 2.5. Prior on first.
Prior on: scenario_s05_01 under both strategies as in `analysis/tb1a_destination/`: coffee_break's admission at 142
gone, refused `none(leader_unwarranted)` at 144 and 150; no completion, `[sep]` or F1 move. Nothing else moved
beyond the log fields.
Prior off (appendix): scenario_s06_01 single_task the admission of item_4 at 172 gone, full_reorder of item_1 at 188
gone; scenario_s06_02 the admissions at 189 gone (item_4 single_task, item_1 full_reorder), refused unwarranted at 191
and 197; scenario_s06_03 full_reorder the admission of item_1 at 221 gone, completion 236 → 226, `[sep]` 90.80 →
54.58 cm; scenario_s06_03 single_task item_4 admitted at 222 instead of 221, completion 316 → 314, `[sep]` 70.62 →
68.41 cm.
Commands: `analysis/tb3_full_reorder/sweep.sh analysis/tb3_full_reorder/sweep`; `analysis/tb1a_destination/sep_classes.py analysis/tb3_full_reorder/sweep`.

| log | md5 (.log) | md5 (.rec) | completion before (2.5) | completion after (G-build) | [sep] min, continuous (tick) | viol | stand | recede |
|---|---|---|---|---|---|---|---|---|
| env_layout_03_scenario_s03_01_full_reorder_on | 9396ff1e4afc6b24c44a242a1411f91e | 515647f63e1b047aab15b0dc0ac91d08 | 221 | 221 | 90.84 (125) | 0 | 0 | 0 |
| env_layout_03_scenario_s03_01_single_task_on | f9a3a12c7c0f0a61a6c5589112961e61 | 515647f63e1b047aab15b0dc0ac91d08 | 238 | 238 | 60.15 (58) | 0 | 0 | 0 |
| env_layout_07_scenario_s05_01_full_reorder_on | 3f06634b0f174655763ee57bd94982a7 | dab078d5ca51e5b378054ee6a60ccca7 | 194 | 194 | 58.31 (25) | 0 | 0 | 0 |
| env_layout_07_scenario_s05_01_single_task_on | 0f52f86aa773cefa1e0719d4f4d3d9b2 | dab078d5ca51e5b378054ee6a60ccca7 | 194 | 194 | 58.31 (25) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_full_reorder_on | f2b1c2c81d78c7657047699996dd7731 | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 224 | 412.25 (105) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_single_task_on | b07b1e31211c1135136a34528e2b7835 | 8cf0930761924a3aab1f1713f3f4bf29 | 265 | 265 | 153.74 (166) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_02_full_reorder_on | e3a478cc4ec7d321e65c406e22578c14 | 329590c9c1249859bfe20d107588c50a | 224 | 224 | 346.07 (114) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_02_single_task_on | ccbaf46c678c522e09c78a692999a620 | 329590c9c1249859bfe20d107588c50a | 267 | 267 | 63.37 (73) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_03_full_reorder_on | 2c734fb09410644d22f4a8cf8cf97a94 | c9c444622f25d15abfd849fc495db540 | 226 | 226 | 54.58 (223) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_03_single_task_on | 0b63ed6e9e4962e699384c8cfce0b767 | c9c444622f25d15abfd849fc495db540 | 272 | 272 | 28.69 (246) | 0 | 3 | 1 |
| env_layout_03_scenario_s03_01_full_reorder_off | 31046a0cbfdfdacd0a3100cb55a16072 | 515647f63e1b047aab15b0dc0ac91d08 | 265 | 265 | 90.84 (125) | 0 | 0 | 0 |
| env_layout_03_scenario_s03_01_single_task_off | 7d868fd4aefe10d3926e86619180ccad | 515647f63e1b047aab15b0dc0ac91d08 | 266 | 266 | 48.25 (57) | 1 | 0 | 1 |
| env_layout_07_scenario_s05_01_full_reorder_off | 2a6d00bc355b058d2cdff4ab2921a7e3 | dab078d5ca51e5b378054ee6a60ccca7 | 198 | 198 | 58.31 (25) | 0 | 0 | 0 |
| env_layout_07_scenario_s05_01_single_task_off | bda40c05ad083b0051e7ce64d455f009 | dab078d5ca51e5b378054ee6a60ccca7 | 198 | 198 | 58.31 (25) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_full_reorder_off | 8b621e3f1f757056ef8a8a3dc5903142 | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 224 | 412.25 (105) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_single_task_off | 4e89831c9236307b244ee7cd63d34cd5 | 8cf0930761924a3aab1f1713f3f4bf29 | 265 | 265 | 153.74 (166) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_02_full_reorder_off | a23d89a6e646be2285842adce2670dc9 | 329590c9c1249859bfe20d107588c50a | 224 | 224 | 346.07 (114) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_02_single_task_off | ed808863ff4d9887224de039cb5653fd | 329590c9c1249859bfe20d107588c50a | 267 | 267 | 63.37 (73) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_03_full_reorder_off | d86b3ef60143f3138296252450878822 | c9c444622f25d15abfd849fc495db540 | 236 | 226 | 54.58 (223) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_03_single_task_off | 35b4df6e43ab34fe83e7e7ab75140d57 | c9c444622f25d15abfd849fc495db540 | 316 | 314 | 68.41 (264) | 0 | 0 | 0 |

## The class-2 correction: the assessed trajectory is the executed one — the logs from here on

Regenerated at the MPB class-2 correction (30 September 2026), superseding the G-build table above. CAUSE:
design_decisions.md, "Realization as built", the dated correction, and "The meta-planner test-bed (MPB)", MPB-4's
class-2 record: the body reports its owed completion ticks and the action in flight (`ExecutorState`), every robot
candidate's projection states the owed ticks first and the continued task is projected from the action in flight, and
the executor spends owed ticks before a hold. Human projections, `realize()`, F1, the gate and the triggers unchanged.
The diff rule checked on every log against the G-build logs: the `.rec` streams byte-identical in all; every `[IR*]`
line byte-identical in all, both priors; in every run but one the robot's lines, `[sep]`, `[hold]` and `[meta]`
lines are identical and only the cost lines differ (`[meta-cand]`, `[meta-b3]`, `[meta-ord]`, `[meta-win]`: a
candidate's T_r now states the owed ticks, or drops a completed walk's re-priced acknowledgement). Prior on: no completion tick, `[sep]` minimum, F1 class, hold or selection moved. Prior off: no
behaviour moved (cost lines only). Completion is the world tick (T6), `analysis/tb1a_destination/sep_classes.py` on
both sets. Prior on first.
Commands: `analysis/tb3_full_reorder/sweep.sh analysis/tb3_full_reorder/sweep`; `analysis/tb1a_destination/sep_classes.py analysis/tb3_full_reorder/sweep`.

| log | md5 (.log) | md5 (.rec) | completion before (G-build) | completion after | [sep] min, continuous (tick) | viol | stand | recede |
|---|---|---|---|---|---|---|---|---|
| env_layout_03_scenario_s03_01_full_reorder_on | 9396ff1e4afc6b24c44a242a1411f91e | 515647f63e1b047aab15b0dc0ac91d08 | 221 | 221 | 90.84 (125) | 0 | 0 | 0 |
| env_layout_03_scenario_s03_01_single_task_on | f3c9b01818187664c285e04cad8a9e6b | 515647f63e1b047aab15b0dc0ac91d08 | 238 | 238 | 60.15 (58) | 0 | 0 | 0 |
| env_layout_07_scenario_s05_01_full_reorder_on | 7adae14aafb582e82acbc58795fb0d01 | dab078d5ca51e5b378054ee6a60ccca7 | 194 | 194 | 58.31 (25) | 0 | 0 | 0 |
| env_layout_07_scenario_s05_01_single_task_on | 3b2dad0e43aea6852ad24412930134a6 | dab078d5ca51e5b378054ee6a60ccca7 | 194 | 194 | 58.31 (25) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_full_reorder_on | cd389598a4f7606be7625dc35b484346 | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 224 | 412.25 (105) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_single_task_on | 7d79a662e46875c01c5ce9edac142eaf | 8cf0930761924a3aab1f1713f3f4bf29 | 265 | 265 | 153.74 (166) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_02_full_reorder_on | b9aea1ebbbfa77b48477882cf9197585 | 329590c9c1249859bfe20d107588c50a | 224 | 224 | 346.07 (114) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_02_single_task_on | ccbaf46c678c522e09c78a692999a620 | 329590c9c1249859bfe20d107588c50a | 267 | 267 | 63.37 (73) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_03_full_reorder_on | 2c734fb09410644d22f4a8cf8cf97a94 | c9c444622f25d15abfd849fc495db540 | 226 | 226 | 54.58 (223) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_03_single_task_on | 0b63ed6e9e4962e699384c8cfce0b767 | c9c444622f25d15abfd849fc495db540 | 272 | 272 | 28.69 (246) | 0 | 3 | 1 |
| env_layout_03_scenario_s03_01_full_reorder_off | f4cd62597c3826af263e1cf04524aef9 | 515647f63e1b047aab15b0dc0ac91d08 | 265 | 265 | 90.84 (125) | 0 | 0 | 0 |
| env_layout_03_scenario_s03_01_single_task_off | 187ae6ee9ee1383c79501eaa48c65772 | 515647f63e1b047aab15b0dc0ac91d08 | 266 | 266 | 48.25 (57) | 1 | 0 | 1 |
| env_layout_07_scenario_s05_01_full_reorder_off | f1f72fdf229d98fc7d7b91299a72405a | dab078d5ca51e5b378054ee6a60ccca7 | 198 | 198 | 58.31 (25) | 0 | 0 | 0 |
| env_layout_07_scenario_s05_01_single_task_off | df6b0cea8c59dba6a195b50ea965f392 | dab078d5ca51e5b378054ee6a60ccca7 | 198 | 198 | 58.31 (25) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_full_reorder_off | cea4392a46a5da7d5e6b922de8dc4da3 | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 224 | 412.25 (105) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_single_task_off | bf2ab7f80ba3e2f63ac896edca3e3fd7 | 8cf0930761924a3aab1f1713f3f4bf29 | 265 | 265 | 153.74 (166) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_02_full_reorder_off | ca71b3bd591ec9cac0b74af207aaa52d | 329590c9c1249859bfe20d107588c50a | 224 | 224 | 346.07 (114) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_02_single_task_off | 79eb0433ffac1c650293e2f2fbae48c4 | 329590c9c1249859bfe20d107588c50a | 267 | 267 | 63.37 (73) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_03_full_reorder_off | d86b3ef60143f3138296252450878822 | c9c444622f25d15abfd849fc495db540 | 226 | 226 | 54.58 (223) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_03_single_task_off | 35b4df6e43ab34fe83e7e7ab75140d57 | c9c444622f25d15abfd849fc495db540 | 314 | 314 | 68.41 (264) | 0 | 0 | 0 |

## The sort (1 October 2026): paths only, no change of behaviour

This folder moved from `analysis/tb3_full_reorder/` to `analysis/kitting/tb3_full_reorder/` when the earlier analyses were sorted by domain
(`docs/rename_table.md`, "Paths: the sort"). The logs, their `.rec` streams and the md5s of the sections above are
unchanged: the set was regenerated from the sorted tree and is byte-identical. The commands of the sections above read
`bash analysis/kitting/tb3_full_reorder/sweep.sh <dir>`, and `sep_classes.py` (with the parser `logparse.py`) is
`analysis/instruments/common/sep_classes.py`.

## The gate on the belief over the live hypotheses (T-K part 1, build stage 2, 4 October 2026) — the logs from here on

Regenerated at T-K part 1's gate stage (AM42; design_decisions.md, "T-K: context knowledge in the recognizer's belief",
R7's AM42; design_records.md, "T-K", THE BUILD, STAGE 2). Two changes since the table above, both named:
- stage 1 (b85494d), the rename of the run option (AM9): in every log the `[run]` header's `assignment_prior=` reads
  `assignment_knowledge=` and the `[IR-prior] switch=` line reads `[IR-assignment] knowledge=`; nothing else;
- stage 2 (91774ce, the gate): `confidence` is the leader's belief over the live hypotheses, before the floor and the
  pin scaling, and the gate compares θ with it. So `[IR]`, `[IR-dist]` and `[meta-proj]` print a higher confidence
  wherever a key is pinned or a live value floored (every log). `[IR-dist]`'s dist is the reported distribution, unchanged.
  Where the leader's value crosses θ one tick earlier, a `recognition_changed` (cause entered) admission moves
  one tick earlier, with the same winner and hold 0 (a continue): env_layout_08_scenario_s06_03_full_reorder_off at 44 (was 45).
  No robot motion, `[hold]`, `[sep]`, completion tick or F1 class moved in any log.
The `.rec` streams are byte-identical to the table above in every log. Completion is the world tick (T6).
The run files state `context_knowledge` from build stage 3 on; these logs were made before it. Prior on first.
Commands: `bash analysis/kitting/tb3_full_reorder/sweep.sh analysis/kitting/tb3_full_reorder/sweep`; `analysis/instruments/common/sep_classes.py analysis/kitting/tb3_full_reorder/sweep`.

| log | md5 (.log) | md5 (.rec) | completion | [sep] min, continuous (tick) | viol | stand | recede |
|---|---|---|---|---|---|---|---|
| env_layout_03_scenario_s03_01_full_reorder_on | d3c6aff86ad475f6ded30d79808ef686 | 515647f63e1b047aab15b0dc0ac91d08 | 221 | 90.84 (125) | 0 | 0 | 0 |
| env_layout_03_scenario_s03_01_single_task_on | 48dd6fda8aa93c5271f24fb2a0e84ca1 | 515647f63e1b047aab15b0dc0ac91d08 | 238 | 60.15 (58) | 0 | 0 | 0 |
| env_layout_07_scenario_s05_01_full_reorder_on | ab6cf17a693838c463e912533f3b2d11 | dab078d5ca51e5b378054ee6a60ccca7 | 194 | 58.31 (25) | 0 | 0 | 0 |
| env_layout_07_scenario_s05_01_single_task_on | 5e124082b52c44f74d57405dc3f21993 | dab078d5ca51e5b378054ee6a60ccca7 | 194 | 58.31 (25) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_full_reorder_on | 98387ebb32cc7dfec3b7b45333aaf55a | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 412.25 (105) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_single_task_on | b471aef943e9ce5c3c4ce0db6abc61e6 | 8cf0930761924a3aab1f1713f3f4bf29 | 265 | 153.74 (166) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_02_full_reorder_on | 96da6c7e8fda79bd39ba01ea1db82325 | 329590c9c1249859bfe20d107588c50a | 224 | 346.07 (114) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_02_single_task_on | ec8923a19370d7ca758e95e4f4deb779 | 329590c9c1249859bfe20d107588c50a | 267 | 63.37 (73) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_03_full_reorder_on | 20f611b268c4e59d85ce40c0edbca5f1 | c9c444622f25d15abfd849fc495db540 | 226 | 54.58 (223) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_03_single_task_on | ce59a1e1ddc20057a00e9bbfd5dac391 | c9c444622f25d15abfd849fc495db540 | 272 | 28.69 (246) | 0 | 3 | 1 |
| env_layout_03_scenario_s03_01_full_reorder_off | 3fc5fccb2ef6ab852596a2031a6e2bd4 | 515647f63e1b047aab15b0dc0ac91d08 | 265 | 90.84 (125) | 0 | 0 | 0 |
| env_layout_03_scenario_s03_01_single_task_off | e44b820331bb8c586c781590feb6bdf5 | 515647f63e1b047aab15b0dc0ac91d08 | 266 | 48.25 (57) | 1 | 0 | 1 |
| env_layout_07_scenario_s05_01_full_reorder_off | 42ebd3a27871f2221af05756a5dba549 | dab078d5ca51e5b378054ee6a60ccca7 | 198 | 58.31 (25) | 0 | 0 | 0 |
| env_layout_07_scenario_s05_01_single_task_off | 8fb8e02355ebc63dc3f827d3c204aca2 | dab078d5ca51e5b378054ee6a60ccca7 | 198 | 58.31 (25) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_full_reorder_off | 0e8d3c8127d5d66ac6d9a8c539978f5a | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 412.25 (105) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_single_task_off | e1466fd0bc8105b2ca1f71e41a3d27cf | 8cf0930761924a3aab1f1713f3f4bf29 | 265 | 153.74 (166) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_02_full_reorder_off | 5720891cb8e7c0b7dd70c01776385ab8 | 329590c9c1249859bfe20d107588c50a | 224 | 346.07 (114) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_02_single_task_off | 394a83251116d5272f7445f0e6f737b9 | 329590c9c1249859bfe20d107588c50a | 267 | 63.37 (73) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_03_full_reorder_off | 558404c21eff46da13f0004c7e485eb5 | c9c444622f25d15abfd849fc495db540 | 226 | 54.58 (223) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_03_single_task_off | c00a5a724d76c8ef607f8c03ea436a56 | c9c444622f25d15abfd849fc495db540 | 314 | 68.41 (264) | 0 | 0 | 0 |

## The build of context knowledge, final (T-K part 1, build stage 7, 4 October 2026) — the logs from here on

Regenerated at 766f7d3 (the build's stage 6; design_records.md, "T-K", THE BUILD, STAGES 3 TO 7), the run files and
the sweep stating `context_knowledge: false` (stage 3). Named lines since B2 (the gate stage's section above), and nothing else (each log compared with B2 after setting
them aside; 0 differ):
- stage 3 (bbb7227): the `[run]` header gains `context_knowledge=off`;
- stage 4a (f70f72f): a new line after the `[run_mesa]` start line, `[run_mesa] timeline source=none windows=[]` (no
  setup or scenario states a timeline);
- stage 4b (2393935): where an A/C activation runs, the action reads `switch_on` for `wait_at` in `[rec]`,
  `[human]`, the human's step lines and the executor's `_load_plan` line (AM43);
- stages 5 and 6 (e589731, 766f7d3): nothing (context knowledge off: every prior weight exactly 1, P1; no `[IR-context]` line).
The `.rec` streams differ from the table above only where an A/C activation runs (`switch_on`). Completion ticks,
the `[sep]` minima and F1's classes are the same as the table above in every log.
Commands: `bash analysis/kitting/tb3_full_reorder/sweep.sh analysis/kitting/tb3_full_reorder/sweep`; `analysis/instruments/common/sep_classes.py analysis/kitting/tb3_full_reorder/sweep`.

| log | md5 (.log) | md5 (.rec) | completion | [sep] min, continuous (tick) | viol | stand | recede |
|---|---|---|---|---|---|---|---|
| env_layout_03_scenario_s03_01_full_reorder_on | 12a779c93676f8a565155aa3343f4a36 | 515647f63e1b047aab15b0dc0ac91d08 | 221 | 90.84 (125) | 0 | 0 | 0 |
| env_layout_03_scenario_s03_01_single_task_on | bdc7a664bd97632ea627d9bc75b8861d | 515647f63e1b047aab15b0dc0ac91d08 | 238 | 60.15 (58) | 0 | 0 | 0 |
| env_layout_07_scenario_s05_01_full_reorder_on | 6dd8010d49e5bceb4f0802bd09ea2935 | a3927888957766c7da70eea660062fd5 | 194 | 58.31 (25) | 0 | 0 | 0 |
| env_layout_07_scenario_s05_01_single_task_on | ba1b15179dfc1ad36639a8a4a2dd46e0 | a3927888957766c7da70eea660062fd5 | 194 | 58.31 (25) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_full_reorder_on | 23830f099291c4d57795228e2acad745 | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 412.25 (105) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_single_task_on | 1cf6af1499d3826a5854b2f0bbd785da | 8cf0930761924a3aab1f1713f3f4bf29 | 265 | 153.74 (166) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_02_full_reorder_on | fc80003051546349edf6e2f496525d9c | 329590c9c1249859bfe20d107588c50a | 224 | 346.07 (114) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_02_single_task_on | b3a85c2d0410924c19c7064c726deb31 | 329590c9c1249859bfe20d107588c50a | 267 | 63.37 (73) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_03_full_reorder_on | a42cac39359bd429ebcd08c388adf7d9 | c9c444622f25d15abfd849fc495db540 | 226 | 54.58 (223) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_03_single_task_on | 211e648284557180b979c674e891fdd4 | c9c444622f25d15abfd849fc495db540 | 272 | 28.69 (246) | 0 | 3 | 1 |
| env_layout_03_scenario_s03_01_full_reorder_off | 396ddb46021ec4076ebb328cf9579394 | 515647f63e1b047aab15b0dc0ac91d08 | 265 | 90.84 (125) | 0 | 0 | 0 |
| env_layout_03_scenario_s03_01_single_task_off | ce4b01981202dadaffd5fec5b8c0b61f | 515647f63e1b047aab15b0dc0ac91d08 | 266 | 48.25 (57) | 1 | 0 | 1 |
| env_layout_07_scenario_s05_01_full_reorder_off | 1165926ffef0799882a0db0257cf0daf | a3927888957766c7da70eea660062fd5 | 198 | 58.31 (25) | 0 | 0 | 0 |
| env_layout_07_scenario_s05_01_single_task_off | e00487f9706f711a493d2ab6b1b42486 | a3927888957766c7da70eea660062fd5 | 198 | 58.31 (25) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_full_reorder_off | ff4785fa7a93d86d81b5f0e81ad50990 | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 412.25 (105) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_single_task_off | 581a076ae2cd1fab484bb404d26ad985 | 8cf0930761924a3aab1f1713f3f4bf29 | 265 | 153.74 (166) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_02_full_reorder_off | fef9b5a5c5dd5b93bb3ff9a015456f0f | 329590c9c1249859bfe20d107588c50a | 224 | 346.07 (114) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_02_single_task_off | 676defd1b29c6481e6d458f55a8bc0e9 | 329590c9c1249859bfe20d107588c50a | 267 | 63.37 (73) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_03_full_reorder_off | 30facb4519327e2457ee1666a46ce647 | c9c444622f25d15abfd849fc495db540 | 226 | 54.58 (223) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_03_single_task_off | d02ce3dc6f2852a0c42640e5487bdbaa | c9c444622f25d15abfd849fc495db540 | 314 | 68.41 (264) | 0 | 0 | 0 |
