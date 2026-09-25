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

All 20 runs; the full_reorder logs and s83's single_task logs go to `sweep/`
(`cp <out_dir>/*_full_reorder_*.log <out_dir>/s83_single_task_*.log analysis/tb3_full_reorder/sweep/`).

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
