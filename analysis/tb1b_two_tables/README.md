# analysis/tb1b_two_tables — the two-table fixture for B3.B (T-B1b): the cost argument and the baselines

`env_layout8`, `scenario_80` / `scenario_81` (literals in `domains/kitting/scenarios.py`, registered the
ordinary way; first built through a generator, e76e4e0, which was reversed in the same task: fixtures are
read by people. The logs are byte-identical across the reversal). `scenario_82` on the same layout only opens
it in the viewer and is not a fixture. env_layout1's room (2000 × 1000 cm) and its eight
shelf positions; no coffee machine or AC switch and no item on shelf_2 / shelf_5 (every typed object is a
hypothesis; item_2 would shadow the human's bearing to item_0). θ, ρ, `min_separation`, β unchanged: the
fixture sets no parameter.

| object | position | | item | shelf (position) | table | whose |
|---|---|---|---|---|---|---|
| kitting_table_0 | (−700, −250) | | item_1 | shelf_1 (−950, −450) | kitting_table_0 | robot |
| kitting_table_1 | (700, −50) | | item_6 | shelf_6 (−500, −450) | kitting_table_0 | robot |
| robot start | (−100, −400) | | item_4 | shelf_4 (950, −300) | kitting_table_0 | robot |
| human start, scenario_80 | (−600, 400) | | item_7 | shelf_7 (300, −450) | kitting_table_1 | robot |
| human start, scenario_81 | (−300, 200) | | item_0 | shelf_0 (−950, 400) | kitting_table_0 | human |
| | | | item_3 | shelf_3 (950, 400) | kitting_table_1 | human |

## The cost argument: the greedy head is not the head of the cheapest ordering

Plain cost in ticks from the robot's own `Projector` (the Mesa body's constants: 20 cm / tick, arrival radius
30 cm, the completion latencies), no human. A full ordering is chained by projecting each task from the
position the previous one ended at; the single-task costs are from the robot's start.

Single task from the start: **item_6 39.27**, item_7 53.38, item_1 61.38, item_4 137.79. The cheapest first
task, the head single-task selection (B3.A) takes, is item_6.

| ordering (items) | total | vs best | per task |
|---|---|---|---|
| **7 4 6 1** | 221.08 | 0 | 53.4, 103.2, 29.8, 34.8 |
| 7 4 1 6 | 223.28 | +2.21 | 53.4, 103.2, 35.7, 31.0 |
| 6 7 4 1 | 260.98 | +39.91 | 39.3, 82.8, 103.2, 35.7 |
| **6 1 7 4** (greedy: repeated cheapest next) | 262.44 | **+41.36** | 39.3, 34.9, 85.1, 103.2 |
| 1 6 7 4 | 278.43 | +57.35 | 61.4, 31.0, 82.9, 103.2 |
| 1 7 4 6 | 279.38 | +58.30 | 61.4, 85.1, 103.2, 29.8 |
| 4 6 1 7 | 287.42 | +66.34 | 137.8, 29.7, 34.8, 85.1 |
| 4 1 6 7 | 287.42 | +66.35 | 137.8, 35.7, 31.0, 82.9 |
| 6 1 4 7 | 325.50 | +104.42 | 39.3, 34.9, 168.7, 82.6 |
| 6 4 1 7 | 326.50 | +105.42 | 39.3, 166.4, 35.7, 85.1 |
| 4 7 6 1 | 336.09 | +115.01 | 137.8, 82.6, 80.8, 34.9 |
| 7 6 4 1 | 336.24 | +115.17 | 53.4, 80.8, 166.4, 35.7 |
| 7 6 1 4 | 337.75 | +116.68 | 53.4, 80.8, 34.9, 168.7 |
| 4 1 7 6 | 339.37 | +118.29 | 137.8, 35.7, 85.1, 80.8 |
| 1 6 4 7 | 341.48 | +120.41 | 61.4, 31.0, 166.5, 82.6 |
| 1 4 6 7 | 342.69 | +121.61 | 61.4, 168.7, 29.7, 82.9 |
| 4 6 7 1 | 352.68 | +131.60 | 137.8, 29.7, 82.9, 102.2 |
| 7 1 6 4 | 353.11 | +132.03 | 53.4, 102.3, 31.0, 166.5 |
| 4 7 1 6 | 353.66 | +132.58 | 137.8, 82.6, 102.2, 31.0 |
| 7 1 4 6 | 354.05 | +132.98 | 53.4, 102.3, 168.7, 29.7 |
| 6 4 7 1 | 390.57 | +169.50 | 39.3, 166.4, 82.6, 102.2 |
| 6 7 1 4 | 393.04 | +171.97 | 39.3, 82.8, 102.2, 168.7 |
| 1 4 7 6 | 393.46 | +172.39 | 61.4, 168.7, 82.6, 80.8 |
| 1 7 6 4 | 393.62 | +172.54 | 61.4, 85.1, 80.8, 166.4 |

The cheapest ordering starts with item_7: its delivery ends beside item_4's shelf, and item_4's delivery ends
beside the two short tasks at kitting_table_0. The greedy ordering is 41.36 ticks (about 830 cm) worse, and
the best ordering with the greedy head (6 7 4 1) is 39.91 worse; the arrival radius is 30 cm, 1.5 ticks.
The executed greedy run completes at world tick 265 (scenario_80) against 262.4 projected; the 2.6 ticks
are step quantisation, uncompensated by decision (L2). Before T-B Q7 it completed at 261, one tick short per
delivery — see "Baselines" below.

**What this fixture does not settle: the tail.** The two best orderings, 7 4 6 1 and 7 4 1 6, differ by 2.21
ticks, which is at the arrival-radius scale (30 cm, 1.5 ticks). The fixture settles the choice of HEAD
(item_7 against item_6), not the ordering of the tail. Do not read a tail result out of it.

This is a property of these two-table geometries, not of one layout. env_layout9 (the realistic placement,
below) is tighter still: its two cheapest orderings differ by 0.31 ticks. With three deliveries to one table
and one to the other, the tail permutations collapse toward each other, because once the odd task is done the
robot shuttles between the same two endpoints and only the order of interchangeable tasks is left. Both
layouts settle the choice of head; neither settles the tail, and a geometry that settled it would have to be
designed for that question.

**What it does not settle either: the generality of the ordering result.** It rests on a single
against-proximity item in each layout — item_4 in env_layout8 (designated 64.9 ticks farther than its nearer
table), item_1 in env_layout9 (26.8) — since 5 of 6 items in each go to the table nearest their shelf. A
claim drawn from T-B3a is therefore scoped to this fixture: it shows that ordering matters when an item is
designated away from its nearest table, NOT that reordering helps in general on a two-table station. A
scenario built to support the general claim needs several against-proximity designations, or a geometry in
which proximity does not order the tables cleanly. TODOS_AND_DEFERRED.md, TODO-47 (f-designations).

**env_layout9, the realistic variant (not a fixture).** Both of layout8's tables stand in open floor; in
env_layout9 they stand against opposite walls (kitting_table_0 north at (−500, 450), kitting_table_1 south at
(500, −450)), which was chosen over both-on-the-north-wall because it separates the tables more (67.3 against
50.0 ticks) and spreads the per-shelf difference between the tables wider (max 61.4 against 49.9). Its head
property holds as the geometry gives it, not by design for it: greedy head item_5 (76.42 alone), head of the
cheapest ordering item_6, gap 46.23 ticks (`permutation_costs.py env_layout9 scenario_90`). It stays a
realism and viewing layout: layout8 keeps the T-B fixtures because scenario_80 / scenario_81 are built,
measured and baselined. Whether the ordering result reproduces on a realistic station is a question for after
T-B3. scenario_90 opens and runs it (completion 365 at T-B Q7, both priors; 361 before it) and is not
measured.

The table is a PROJECTION and is unchanged by T-B Q7: the fix is on what the body spends executing, and
`permutation_costs.py` chains projections without executing anything, so every cost above stands as written.
What moved is the executed run it is compared against (265, above).

The table is regenerated by `permutation_costs.py`, committed here, which reproduces every row above:

    PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python \
        analysis/tb1b_two_tables/permutation_costs.py env_layout8 scenario_80

It chains single-task projections by moving the robot's position in a copy of the WorldState, since
`Projector.project` is single-task until B3.B; it is plain cost, no human and no realization. T-B3a checks
B3.B's chosen head against this table, so it is a tool and not a throwaway.

## The scenarios under the current strategy (single_task; gate none, cost realized, stop off)

Every row is at T-B Q7 (de70e98); the same rows before it, when the body spent one completion tick fewer per
robot delivery, are given in the second table.

| | completion (world fact) | declared | min `[sep]` | holds | human releases |
|---|---|---|---|---|---|
| scenario_80, prior off / on | 265 / 265 | 267 | 170.0 cm (step 167) | 0 | 53 (table_0), 172 (table_1) |
| scenario_81, prior off / on | 268 / 268 | 270 | 63.4 cm (step 74) | 1 (3 ticks) | 70 (table_0), 189 (table_1) |

| before T-B Q7 | completion (world fact) | declared | min `[sep]` | holds |
|---|---|---|---|---|
| scenario_80, prior off / on | 261 / 261 | 263 | 217.2 cm (step 165) | 0 |
| scenario_81, prior off / on | 265 / 265 | 267 | 46.6 cm (step 73) | 1 (4 ticks) |

- scenario_80: the robot runs 6, 1, 7, 4. The projected cheapest ordering (7 4 6 1) against the human's
  executed positions: minimum 396 cm, so both the greedy and the cheapest ordering stay clear of the human.
- scenario_81: the human's item_0 task is projected at 71.9 ticks from its start; the robot's two short tasks
  (item_6, then item_1) at 39.3 + 34.9 = 74.2. When the human's projection is admitted (step 18 prior off, 16
  on) every candidate prices at δ = 0; at step 40, with item_1 the head, item_1 realizes at δ = 3 (T_r 34.69,
  cost 37.69, T_h 32.71): the conflict is in the second task of (item_6, item_1), not in its head. The full
  orderings cannot be priced against the human until B3.B's multi-task projection exists. Before T-B Q7 the
  same decision fell at step 39 and realized δ = 4 (cost 38.69, T_h 33.71): the robot reaches that decision one
  tick later, so one fewer tick of shift clears the same human — the hold is minimal in both.
- The closest approach is now 63.4 cm at step 74; the 46.6 cm tick at step 73 recorded before T-B Q7 does not
  occur any more, the same geometry being walked one tick later. Both are past the human's projection, the
  known arrival the existing fixtures show; recorded as an observation of this fixture, from which no
  separation value follows.
- Belief, prior off: item_0 leads from step 0 in both scenarios, no rival ahead at any tick of the fetch.
  scenario_81 (34-tick fetch): 0.48 at step 8, clears θ at 18, 0.985 at 32, about 0.99 through the carry to
  the boundary at 70; nearest rival task at step 10 item_1 0.127 (`unknown` 0.262). Prior on: clears θ at 16.
  scenario_80 (17-tick fetch): clears θ at 11 (off), 8 (on).
- Hypothesis space: one `deliver_item` per item (item_0, 1, 3, 4, 6, 7) plus `unknown`; grounded tables
  item_0 / 1 / 4 / 6 → kitting_table_0, item_3 / 7 → kitting_table_1. No "matches no hypothesis" line.
- The eight existing fixtures, both priors, are byte-identical to `analysis/tb1a_destination/sweep/` with the
  fixture registered.

## Baselines (`sweep/`, logs git-ignored)

    analysis/tb1b_two_tables/sweep.sh analysis/tb1b_two_tables/sweep \
        --cost_strategy realized --gate_strategy none --separation_stop false

| log | md5 |
|---|---|
| s80_off | fa32e1d8ec88bc85cd1be36a555013c2 |
| s80_on | cb44b42525e1326ef4c85a2c53ad20f7 |
| s81_off | 6ee3d48444a72085fb85de60b08cc356 |
| s81_on | e701876c57a54f3c2e6c0109a7ed0d4b |

### T-B2d (79fb0ee): the `[run]` header names the strategy — the baselines from here on

Regenerated with the same command at 79fb0ee, superseding the table above. Each log differs from its
predecessor in the `[run]` line alone (` strategy=single_task` added); see `analysis/tb1a_destination/README.md`,
"T-B2d". `single_task` only: no `full_reorder` baselines before T-B2c.

| log | md5 |
|---|---|
| s80_off | 13d435fa54388b1d44a5346d0e23244f |
| s80_on | 826aca3708633e723e04fa7aaf95033d |
| s81_off | 70654005c5d5678500f551646e14ef25 |
| s81_on | be667aadf5717b5787d13d1188d81147 |

### T-B Q7 (de70e98): the body spends every completion tick it states — the baselines from here on

Regenerated with the same command at de70e98, superseding the table above. The Mesa executor now spends the
completion ticks a reload used to cancel (`docs/design_decisions.md`, "A reload never cancels a completion tick
the body states"); nothing in `shared/` changed. FOR A READER COMPARING WITH THE RECORD: every completion tick
recorded above, and in the T-B2b / T-B2c record, IS ONE TICK SHORTER PER ROBOT DELIVERY than the behaviour
from here on, less where a decided hold carried the tick. Here: scenario_80 261 → 265 (four deliveries, no
hold), scenario_81 265 → 268 (four deliveries, one of them carried by the hold before item_1, which
re-realized 4 ticks at step 39 → 3 at step 40). Both priors, both fixtures. The human's lines and the head
order are unchanged.

`single_task` only: no `full_reorder` baselines are recorded, which stays with T-B3. Measured there for the
record, not baselined: under `--strategy full_reorder` both fixtures complete at 224 (world fact, both priors,
head order 7, 4, 6, 1, no hold), against 220 before T-B Q7.

| log | md5 |
|---|---|
| s80_off | 6f542bfa12275536282f7dadd336c5e7 |
| s80_on | e30f83e0cc804d75232ece20f206377b |
| s81_off | 13eba624a5baf541de912ecc82246c98 |
| s81_on | 42c25ac908b18965de087bbc84760a21 |

### D3 (dd880be): `task_committed` is not a trigger — the baselines from here on

Regenerated at dd880be with the same command, superseding the table above. Only the trigger set changed
(`shared/meta_planner.py`, `evaluate_triggers()`: `task_committed` removed; `docs/design_decisions.md`, "D3:
task_committed is not a trigger"). Against the previous logs, checked per tick: every `[sep]` line, every human
line, every `[IR] step=` and `[IR-dist]` line and the `[run]` header are byte-identical, and so is completion. What
changed: the `[meta*]` lines of the removed `task_committed` decisions (16 in these logs); and the executor's
bookkeeping, positions and ticks identical — no `_load_plan` at the grasp (the removed decision's reload of
`deliver_already_held`), a later `continue_plan` mapping `action_index 2->0` / `3->1` instead of `0->0` / `1->1`,
and `_on_task_complete` on the 4-action plan (`action_index=4 plan_len=4`) instead of the 2-action one.

HOLDS PLACED BY `task_committed` in the previous logs (their `[hold] … trigger=` field): none; no hold changed.

| log | md5 |
|---|---|
| s80_off | 19a59f492213be5402ca918dcf26d128 |
| s80_on | 6b6227b77d4623160894f6443c38b9f1 |
| s81_off | c24ce309cc4a1aef054111d8b34c3404 |
| s81_on | 656847aceea194d6d4990f243dfab2be |

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
| s80_off | 55, 174 | 55 | 265 -> 265 | - | - |
| s80_on | 55, 174 | 55 | 265 -> 265 | - | - |
| s81_off | 72, 191 | 42 | 268 -> 267 | 40:3 | 40:2 |
| s81_on | 72, 191 | 42 | 268 -> 267 | 40:3 | 40:2 |

| log | md5 |
|---|---|
| s80_off | ff694fedefc908f409160547a8620659 |
| s80_on | 7d0d540fbf873e48d79a26f8b8f7ca1d |
| s81_off | 5687bdadecf377af8cd257f3a25bc53d |
| s81_on | 9fb470e4e11fa6494e86314dfaf1986d |

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
| s80_off | 77df42e20bbdf1f75db70ebff9fcc242 | 8cf0930761924a3aab1f1713f3f4bf29 |
| s80_on | cfdb673f72a5fb7eb1ddac9b621daea0 | 8cf0930761924a3aab1f1713f3f4bf29 |
| s81_off | 0483180acbe5ae39ef08a13b73d0b0e4 | 329590c9c1249859bfe20d107588c50a |
| s81_on | d2a27a4d972bfd48d7a5781db354fd76 | 329590c9c1249859bfe20d107588c50a |

## T-H4: the record's queries and the coverage line — the logs from here on

Regenerated after T-H4 with the same command, superseding the T-H3 table. CAUSE: the loader prints one `[coverage]`
line per script entry for each robot observing the human, after the `[run]` headers (`docs/design_decisions.md`, "T-H:
the human behaviour model", as built T-H4). Against the T-H3 logs every other line is byte-identical, and every `.rec`
stream is byte-identical (its md5 unchanged).

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| s80_off | f3408a14ac20412e64f938ff6e7432b2 | 8cf0930761924a3aab1f1713f3f4bf29 |
| s80_on | 2ed5dcf1ea92ec89051b224fbf87ce74 | 8cf0930761924a3aab1f1713f3f4bf29 |
| s81_off | 39686f37181674b300991b610098f4d3 | 329590c9c1249859bfe20d107588c50a |
| s81_on | 206682a2db1ee59e4dcc3ed5c1b8290d | 329590c9c1249859bfe20d107588c50a |

## T-H follow-up: the scenario-coverage line — the logs from here on

Regenerated after the T-H follow-up with the same command, superseding the T-H4 table. CAUSE: the loader prints
one `[scenario-coverage]` line per robot observing the human, after its `[coverage]` lines: the script's composition
and scenario coverage (`docs/design_decisions.md`, "T-H: the human behaviour model", as built T-H follow-up). Against
the T-H4 logs every other line is byte-identical, and every `.rec` stream is byte-identical (its md5 unchanged).

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| s80_off | 44119685b7d511bb9b43bb4b688da3c3 | 8cf0930761924a3aab1f1713f3f4bf29 |
| s80_on | 1801536e2024853d4a9c62ec6a7cfb2a | 8cf0930761924a3aab1f1713f3f4bf29 |
| s81_off | 49ca6dc210be42feef6714bbc4caf040 | 329590c9c1249859bfe20d107588c50a |
| s81_on | e66b645c2bdffcee8549203daf5c3ee0 | 329590c9c1249859bfe20d107588c50a |

## T-L stage 3: the serial ids — the logs from here on

Regenerated after T-L stage 3, superseding the T-H follow-up table. CAUSE: the rename to the serial ids (`docs/design_decisions.md`, "Layouts, setups and scenarios: the three artefacts of
a run", ruling 4 as amended, ruling 6); the runs do not change. Logs are named `<layout id>_<scenario id>_<run
options>.log` (ruling 6), each `.rec` beside its log; `docs/rename_table.md` maps the old tags (its last table).
Against the stage-2 logs (99563cc, run from scratch under the old ids and paired through the rename table) every log
differs in the `[run_mesa]` line alone (`layout=` and `scenario=`), and every `.rec` stream is byte-identical. T-L
stages 1 and 2 had changed the same line alone (the setup id added, then its serial id), with no section here; the
`.rec` md5s equal the T-H follow-up table's.

Regenerate from the repo root (arguments as before; without them the defaults of `configs/experiment.yaml` are the
same, and the `[run]` line does not record which):

    analysis/tb1b_two_tables/sweep.sh analysis/tb1b_two_tables/sweep \
        --cost_strategy realized --gate_strategy none --separation_stop false

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_08_scenario_s06_01_off | 0054b641ab77c15ef52fbd0e9b9a7737 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_on | bd4dea4c79485e202f2eda2b29a4f96f | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_02_off | 41301096d8fa57a0691ac4b88139c97b | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_on | 0d8db6fb4067284052360722ca4756fe | 329590c9c1249859bfe20d107588c50a |

## T-D R and E Stage 1: the recognizer without `unknown` — the logs from here on

Regenerated at the T-D Stage 1 build (27 September 2026, cycle 1 session 1.3), superseding the T-L stage 3 table.
CAUSE: a behaviour change of the recognizer (`docs/design_decisions.md`, "T-D R and E"): the `unknown` hypothesis,
u and the grade are gone and the belief is normalised over the live hypothesis set H (R1, R6); the `[IR]` line
carries the lifecycle state, the adequacy finding and the members' tail probabilities; the `[run]` header names
the test level and the body's speed; the `[IR-boundary]` line no longer says "+ unknown"; `none(unknown)` refusals
are gone. The `.rec` streams are byte-identical to the stage 3 ones (the human does not react to the robot). The
gate is unchanged; its input is now the leader's share over H, so admissions moved, and in prior-off runs the
robot's own remaining item is admitted once it is the lone live task after the human's last task (world lines
differ from that tick). Measured in session 1.4, not corrected here. Command: `analysis/tb1b_two_tables/sweep.sh analysis/tb1b_two_tables/sweep --cost_strategy realized --gate_strategy none --separation_stop false`.

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_08_scenario_s06_01_off | 3fabb9df8c1bdbe4330ac035f290c33e | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_on | fda3109d2104c80d9d9b9a0d9e9c44e3 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_02_off | c27ccea8afd0bcb8d60efa80f751ff39 | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_on | e784144f2905a0bcb1f4a53512f272a8 | 329590c9c1249859bfe20d107588c50a |

## T-D Stage 1, E6 amended: stationary-phase members — the logs from here on

Regenerated at cycle 1 session 1.3b (27 September 2026), superseding the T-D R and E Stage 1 table. CAUSE: E6
amended (design_decisions.md, "T-D R and E"): a stationary phase within its priced duration is a member of the
adequacy test with S = 1. Only `[IR]` lines differ from the Stage 1 logs, and in them only the finding and the
tails (members added at S = 1; the belief and every existing member's S unchanged); every other line and the
`.rec` streams are byte-identical. Same commands as the section above.

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_08_scenario_s06_01_off | 8af7df2af74e80fae6e7bbf8a6fe592f | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_on | 2cf7861e47fa192870f8d8fb4b4d949e | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_02_off | 8b02c0d458e525332d8d11136591b884 | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_on | e1d36827fb3bc877013eb17137265d4e | 329590c9c1249859bfe20d107588c50a |

## T-D cycle 1.5b: E8, E9, E10 and G1 — the logs from here on

Regenerated at cycle 1 session 1.5b (27 September 2026), superseding the "E6 amended" table above. CAUSE: E8 (the
advance tick a member at S = 1), E9 (s_exp by the Projector's attribution), E10 (the belief's evidence per phase
L(v·D)) and G1 (the guard on admission: `_clears_gate` also requires the leader's hypothesis adequacy to be adequate;
new refusals `none(leader_no_observation)`, `none(leader_inadequate)`); design_decisions.md, "T-D R and E", "1.5
rulings". Every `[IR]` line on a live tick differs (the new `leader_adequacy=` field; the tails under E8, E9); `[IR-dist]` differs
where standing now charges the belief (E10); decisions differ at admissions (G1) and wherever the belief moved.
World lines (the agents' per-tick lines) changed in none. The `.rec` streams are byte-identical to the table
above. Per-run diff and the acceptance: `analysis/td_stage1b/` (`baseline_diff.txt`, REPORT.md).

Command (from the repo root; the same as the sections above; restated because 7f4559a had dropped them, restored in 1.5c):
`analysis/tb1b_two_tables/sweep.sh analysis/tb1b_two_tables/sweep --cost_strategy realized --gate_strategy none --separation_stop false`

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_08_scenario_s06_01_off | 9d2229e6ae945886574b2c261780b2a7 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_on | 2c2a9d79ef4932252f3afffe47c0887b | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_02_off | 2824fd4ef817d8b87e358ea8ceca09dc | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_on | 5cafd2c3debfef3eece74af7be7f1073 | 329590c9c1249859bfe20d107588c50a |

## T-D cycle 1.5c: E6 second amendment — the logs from here on

Regenerated at cycle 1 session 1.5c (27 September 2026), superseding the 1.5b table above. CAUSE: E6 amended a second
time (design_decisions.md, "T-D R and E"): a stationary tick with s ≤ s_exp in any phase with s_exp > 0 is an
observation with S = 1 (the latency tick after a grasp and after a boundary), and no hypothesis is a member on a
boundary tick. `[IR]` lines differ in the finding, the leader's adequacy and the tails on those ticks; `[IR-dist]`
is identical on every common tick (L = 1 there before and after; runs that end later add exhausted ticks); admissions that waited for the first walking tick after a boundary now
come on the latency tick (b + 1). World lines changed in none. The `.rec` streams are byte-identical to the
table above. Same command as the 1.5b section. Diff and acceptance: `analysis/td_stage1b/` (`baseline_diff_15c.txt`,
REPORT.md, section 1.5c).

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_08_scenario_s06_01_off | 7b2858b5209cbb3132914b9a0fbfef29 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_on | badc5d849f98902b889bb4ba53454f40 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_02_off | c78a186d38f508fde6938a6ef0de4237 | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_on | 56d53436e78a880d0492d927a8b86997 | 329590c9c1249859bfe20d107588c50a |

## TB.2b: the cognitive loop does not end with the task pool — the logs from here on

Regenerated at TB.2b (27 September 2026), superseding the 1.5c table above. CAUSE: the robot observes and recognizes
on every tick; after its terminal return it evaluates no trigger, decides nothing and does not step the executor
(design_decisions.md, "The cognitive loop does not end with the task pool"). Each log gains `[IR]` and `[IR-dist]`
lines from the tick after the declared completion tick to the run's last tick, and within every tick the robot's
`[IR]` and `[IR-dist]` lines now precede its `[meta-trig]` line, so every md5 changed. Criterion, met in all 4: the
log with every `[IR*]` line removed is byte-identical to the 1.5c log, the `[IR*]` lines are byte-identical up to and
including the declared tick, and the `.rec` streams are byte-identical to the table above. Command: `analysis/tb1b_two_tables/sweep.sh analysis/tb1b_two_tables/sweep --cost_strategy realized --gate_strategy none --separation_stop false`.
Check and measurements: `analysis/tb2b_exposed_interval/` (`baseline_diff.txt`, REPORT.md).

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_08_scenario_s06_01_off | 38cd2f289ad21f63152c9e58841f5d16 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_on | 33775f4d11d09f121657e15658ca7d09 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_02_off | b6b8d3f7ea45baaf305a8ce403035bb7 | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_on | ea5d850cad1da96d4bb1955dfce212c6 | 329590c9c1249859bfe20d107588c50a |

## L-build: T-D L, the belief lifecycle — the logs from here on

Regenerated at L-build (28 September 2026), superseding the TB.2b table above. CAUSE: design_decisions.md, "T-D L: the
belief lifecycle", as amended on the L-records report: the episode boundary is the observed agent's completion of a
terminal action (L1); a hypothesis is retired while its terminal fact holds and re-enters at 1/|H| (L4, `[IR-reentry]`,
new); `recognition_changed` also fires on the belief's episode boundary (L5 B) and on the recorded hypothesis's
inadequacy (retraction, L2 (ii)). Two format changes reach every log: `[meta-trig]` names the condition of a
`recognition_changed` (` cause=entered | replaced | boundary | retraction`), and `[IR-boundary]` names the completed
action (`completed place(item_2,kitting_table_0):` for `completed a task:`); so every md5 changed. No criterion of
identity (L changes behaviour); the `.rec` streams are byte-identical to the table above in all 4. With the two
format changes undone (`analysis/l_build/baseline_diff.py`): identical in 2 of 4 (L08 s06_01_on, L08 s06_02_on); the
recognizer's lines and the triggers moved, the robot's behaviour not, in none; the robot's behaviour
(`[meta]`, `[hold]`, `[sep]`, its lines) moved in L08 s06_01_off, L08 s06_02_off. Each moved number with its ticks and cause:
`analysis/l_build/REPORT.md`. Command: `analysis/tb1b_two_tables/sweep.sh analysis/tb1b_two_tables/sweep`.

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_08_scenario_s06_01_off | a376a7d307bd268647f91d2dc2c38ec3 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_on | 890bcb753853e38ee7150cdf833e448c | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_02_off | 82c68826f001529d8cff41530d8fb835 | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_on | bb5d442ae6ade49f2ef213c9659ff303 | 329590c9c1249859bfe20d107588c50a |

## P-build: T-D P, the fallback projection — the logs from here on

Regenerated at P-build (28 September 2026), superseding the L-build table above. CAUSE: design_decisions.md, "T-D P:
the fallback projection": where admission refuses and a human is observed, the decision realizes against the fallback
projection (the human's observed position and last displacement: standing, or a straight continuation to the
workspace boundary or the first fixed object's arrival radius, over each candidate's span); a candidate whose violation
is cleared only by the projection's end is refused (` refused=fallback` on `[meta-cand]`), and with none eligible the
robot waits without a task (`[meta] … wait`, `[meta-b3] … selection=wait`). Format: `[meta-proj]` names a fallback as
`projection=fallback refused=<the refusal's reason>`, so every log whose run refused an admission changed md5. No
criterion of identity (P changes behaviour). The `.rec` streams are byte-identical to the table above in all 4; with
the prior on, the recognizer's lines (`[IR]`, `[IR-…]`) are byte-identical in every run; with P's format additions
undone, the first differing line of every changed run is at tick 0, a decision under the fallback. WAITS: a run whose
robot is still waiting at its last tick has no completion tick; the table records "waits: occupied target (X)" for it
(the human's script ends standing at the robot's delivery table; the six scripts predate T-C2c's authoring convention
and are not edited; design_decisions.md, "T-D P", the deadlock). Completion is the world tick (T6), before (L-build) and
after. Command: `analysis/tb1b_two_tables/sweep.sh analysis/tb1b_two_tables/sweep`.

| log | md5 (.log) | md5 (.rec) | completion before | completion after |
|---|---|---|---|---|
| env_layout_08_scenario_s06_01_off | cdb5bb197539112033717b0e5608dbba | 8cf0930761924a3aab1f1713f3f4bf29 | 265 | not complete in 340 steps |
| env_layout_08_scenario_s06_01_on | 7ec8c5862d00214b9d0a172bd94eb533 | 8cf0930761924a3aab1f1713f3f4bf29 | 265 | 267 |
| env_layout_08_scenario_s06_02_off | 7e1444ef0c42696d515d9cd138c7dc2d | 329590c9c1249859bfe20d107588c50a | 267 | 262 |
| env_layout_08_scenario_s06_02_on | 6c39f3d1d31e1f6a1199be193ca6790f | 329590c9c1249859bfe20d107588c50a | 267 | 269 |

## P4-build: T-D P4, persistence, and projection_expired — the logs from here on

Regenerated at P4-build (28 September 2026), superseding the P-build table above. CAUSE: design_decisions.md, "T-D P",
P4 and Q6: the fallback projects the observed persistence only (a straight run of k ticks continued k ticks, cut at the
workspace boundary or the first fixed object with no stand after it; a stand of k ticks held k ticks; no previous
observation, none), realized as any projection (F1), and `projection_expired` re-decides when the fallback a decision
rested on reaches its end (`[meta-trig] … trigger=projection_expired`, new); the refusal and the wait of the P-build
are removed. No criterion of identity (P4 changes behaviour). The `.rec` streams are byte-identical to the table above
in all 4; with the prior on, the recognizer's lines are byte-identical to the L-build table's. A run whose robot has
not delivered its last item at the run's last tick is recorded as "does not complete: occupied target (X), holds
lengthening, from <tick>": the human's script ends standing at the robot's delivery table (the scripts predate T-C2c's
authoring convention and are not edited), and from the first hold on that final stand the robot holds and
reconsiders at each expiry of a longer stand (scenario_s01_06 prior on, 800 steps: expiries at 165, 213, 309, 501,
holds 48, 96, 192, 384, never complete). Completion is the world tick (T6), before (P-build; "waits" there) and after.
Command: `analysis/tb1b_two_tables/sweep.sh analysis/tb1b_two_tables/sweep`.

| log | md5 (.log) | md5 (.rec) | completion before (P-build) | completion after (P4) |
|---|---|---|---|---|
| env_layout_08_scenario_s06_01_off | 1aff98e410789949a7ab283f8b972609 | 8cf0930761924a3aab1f1713f3f4bf29 | not complete in 340 steps | 265 |
| env_layout_08_scenario_s06_01_on | 1618a7efff2c9193f6204f54015f910d | 8cf0930761924a3aab1f1713f3f4bf29 | 267 | 265 |
| env_layout_08_scenario_s06_02_off | d7506eae987c2276028a9d5374692659 | 329590c9c1249859bfe20d107588c50a | 262 | 267 |
| env_layout_08_scenario_s06_02_on | aa88a8cd08807205b66829d1e1b402d9 | 329590c9c1249859bfe20d107588c50a | 269 | 267 |

## 2.5: the exit walk on the six regression scripts (Track 2.5) — the logs from here on

Regenerated at Track 2.5 (29 September 2026), superseding the P4-build table above. CAUSE: `docs/assumptions.md` 1.1:
the human scripts of scenario_s01_01, s01_06, s02_01, s03_01, s04_01 and s06_03 end with the exit walk
`go_to("corner_SE")` (52295f7), and env_layout_02 and env_layout_08 declare the landmark corner_SE. The other
scenarios' scripts are unchanged; their logs and `.rec` streams are byte-identical to the P4-build table (env_layout_08's
new landmark moved nothing). The six scripts' `.rec` streams change from the tick the exit walk begins. Completion is
the world tick (T6), read by `analysis/tb1a_destination/sep_classes.py`: the tick after the robot's last release made
while it has a task; the "before" column is the same reader on the P4-build logs. The `[sep]` minimum is
of the continuous distance; viol / stand / recede are F1's classes (`analysis/f1_robot_responsible/evaluate.py`, its
rule copied into the reader) of the ticks whose continuous minimum lies below min_separation (50 cm): the
near-encounters of `docs/assumptions.md` 4.6.
Nothing changed: the four logs and `.rec` streams are byte-identical to the P4-build table (scenario_s06_01 and
scenario_s06_02 are not edited; env_layout_08's new landmark moved nothing).
Commands: `analysis/tb1b_two_tables/sweep.sh analysis/tb1b_two_tables/sweep`; `analysis/tb1a_destination/sep_classes.py analysis/tb1b_two_tables/sweep`.

| log | md5 (.log) | md5 (.rec) | completion before (P4) | completion after (2.5) | [sep] min, continuous (tick) | viol | stand | recede |
|---|---|---|---|---|---|---|---|---|
| env_layout_08_scenario_s06_01_off | 1aff98e410789949a7ab283f8b972609 | 8cf0930761924a3aab1f1713f3f4bf29 | 265 | 265 | 153.74 (166) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_on | 1618a7efff2c9193f6204f54015f910d | 8cf0930761924a3aab1f1713f3f4bf29 | 265 | 265 | 153.74 (166) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_02_off | d7506eae987c2276028a9d5374692659 | 329590c9c1249859bfe20d107588c50a | 267 | 267 | 63.37 (73) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_02_on | aa88a8cd08807205b66829d1e1b402d9 | 329590c9c1249859bfe20d107588c50a | 267 | 267 | 63.37 (73) | 0 | 0 | 0 |
