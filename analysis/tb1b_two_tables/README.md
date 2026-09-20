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
The executed greedy run completes at world tick 261 (scenario_80) against 262.4 projected.

**What this fixture does not settle.** The two best orderings, 7 4 6 1 and 7 4 1 6, differ by 2.21 ticks,
which is at the arrival-radius scale. The fixture settles the choice of HEAD (item_7 against item_6), not the
ordering of the tail. Do not read a tail result out of it.

The table was computed by a throwaway script (the chaining moves the robot's position in a copy of the
WorldState, since `Projector.project` is single-task until B3.B); B3.B's own multi-task projection replaces it.

## The scenarios under the current strategy (single_task; gate none, cost realized, stop off)

| | completion (world fact) | declared | min `[sep]` | holds | human releases |
|---|---|---|---|---|---|
| scenario_80, prior off / on | 261 / 261 | 263 | 217.2 cm | 0 | 53 (table_0), 172 (table_1) |
| scenario_81, prior off / on | 265 / 265 | 267 | 46.6 cm (step 73) | 1 | 70 (table_0), 189 (table_1) |

- scenario_80: the robot runs 6, 1, 7, 4. The projected cheapest ordering (7 4 6 1) against the human's
  executed positions: minimum 396 cm, so both the greedy and the cheapest ordering stay clear of the human.
- scenario_81: the human's item_0 task is projected at 71.9 ticks from its start; the robot's two short tasks
  (item_6, then item_1) at 39.3 + 34.9 = 74.2. When the human's projection is admitted (step 18 prior off, 16
  on) every candidate prices at δ = 0; at step 39, with item_1 the head, item_1 realizes at δ = 4 (cost 38.69,
  T_h 33.71): the conflict is in the second task of (item_6, item_1), not in its head. The full orderings
  cannot be priced against the human until B3.B's multi-task projection exists.
- The 46.6 cm tick (step 73, stop off) is the known arrival after the human's projection has ended, as in the
  existing fixtures; accepted as is.
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
