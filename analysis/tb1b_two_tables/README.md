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
