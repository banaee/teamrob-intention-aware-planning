# analysis/tb1d_designations — T-B1d closed as a record: which designations separate the greedy head from the ordering head

T-B1d was to add scenario_84, a two-table fixture whose ordering effect (single_task's greedy head differs from the
head of the cheapest ordering, plain cost) survives the removal of any single against-proximity designation, so that
T-B3a's claim would not rest on item_4 alone (TODO-47 (f-designations)). Ruling (Hadi, option (ii)): no scenario_84,
no env_layout8b; T-B1d closes as this record. Nothing is registered; the scratch layout copies used for pricing are
not committed.

**The prompt's error, recorded.** Both prompts asked for a scenario on env_layout8 differing from scenario_80 in the
robot's designations only. A designation is a layout fact (the `"destination"` per item; T-B Q1, T-B1a), and
`check_task_destinations` (`shared/types.py`) refuses at spawn an assigned task whose bound table is not the layout's.
No scenario can change a designation; a second designation set needs its own layout file.

## How the numbers were produced

`analysis/tb1b_two_tables/permutation_costs.py`'s `costs()` (unchanged: plain cost from the robot's start), called
in process on a scratch copy of `env_layout8.json` with only the items' `"destination"` edited and scenario_80's robot
pool bound to those tables; human side, robot start and pool as scenario_80. Greedy head: the cheapest single task
from the start. Gap: the cheapest ordering that starts with the greedy head minus the cheapest ordering.

Walk from each item's shelf to each table (straight line, 20 cm / tick):

| item | shelf | to kitting_table_0 (−700, −250) | to kitting_table_1 (700, −50) | nearer |
|---|---|---|---|---|
| item_1 | shelf_1 (−950, −450) | 16.0 | 84.9 | kitting_table_0 |
| item_6 | shelf_6 (−500, −450) | 14.1 | 63.2 | kitting_table_0 |
| item_4 | shelf_4 (950, −300) | 82.5 | 17.7 | kitting_table_1 |
| item_7 | shelf_7 (300, −450) | 51.0 | 28.3 | kitting_table_1 |

env_layout8 as built (scenario_80): item_1, item_6, item_4 → kitting_table_0, item_7 → kitting_table_1; item_4 is the
one against-proximity item.

## Answer 1 (first T-B1d prompt): item_4 kept on kitting_table_0, reversions of the other items only

Sets: **A1** = item_1 → table_0, item_6 → **table_1**, item_4 → table_0, item_7 → **table_0**.
**B1** = item_1 → **table_1**, item_6 → **table_1**, item_4 → table_0, item_7 → table_1. (Bold: changed from
env_layout8.)

| designation set | against proximity | single tasks from the start | greedy head | ordering head | cheapest ordering | gap |
|---|---|---|---|---|---|---|
| env_layout8 (scenario_80) | 4 | 6 39.3, 7 53.4, 1 61.4, 4 137.8 | 6 | 7 | 7 4 6 1, 221.08 | 39.91 |
| A1 | 4, 6, 7 | 1 61.4, 7 73.6, 6 85.9, 4 137.8 | 1 | 7 | 7 6 4 1, 293.92 | 56.64 |
| A1, item_6 → table_0 | 4, 7 | 6 39.3, 1 61.4, 7 73.6, 4 137.8 | 6 | 7 | 7 4 6 1, 304.26 | 39.95 |
| A1, item_7 → table_1 | 4, 6 | 7 53.4, 1 61.4, 6 85.9, 4 137.8 | 7 | 7 (same) | 7 4 1 6, 274.69 | 0.00 |
| B1 | 4, 1, 6 | 7 53.4, 6 85.9, 1 130.0, 4 137.8 | 7 | 6 | 6 7 4 1, 351.46 | 37.28 |
| B1, item_1 → table_0 | 4, 6 | 7 53.4, 1 61.4, 6 85.9, 4 137.8 | 7 | 7 (same) | 7 4 1 6, 274.69 | 0.00 |
| B1, item_6 → table_0 | 4, 1 | 6 39.3, 7 53.4, 1 130.0, 4 137.8 | 6 | 7 | 7 4 6 1, 290.04 | 13.98 |

## Answer 2 (second T-B1d prompt): the sets as given, every against-proximity item reverted in turn, item_4 included

Sets: **A2** = item_1 → table_0, item_6 → **table_1**, item_4 → table_0, item_7 → table_1.
**B2** = item_1 → **table_1**, item_6 → **table_1**, item_4 → table_0, item_7 → **table_0**.

| designation set | against proximity | single tasks from the start | greedy head | ordering head | cheapest ordering | gap |
|---|---|---|---|---|---|---|
| A2 | 4, 6 | 7 53.4, 1 61.4, 6 85.9, 4 137.8 | 7 | 7 (same) | 7 4 1 6, 274.69 | 0.00 |
| A2, item_4 → table_1 | 6 | 7 53.4, 1 61.4, 4 73.5, 6 85.9 | 7 | 1 | 1 6 7 4, 239.42 | 37.20 |
| A2, item_6 → table_0 (= env_layout8) | 4 | 6 39.3, 7 53.4, 1 61.4, 4 137.8 | 6 | 7 | 7 4 6 1, 221.08 | 39.91 |
| B2 | 4, 6, 1, 7 | 7 73.6, 6 85.9, 1 130.0, 4 137.8 | 7 | 7 (same) | 7 6 4 1, 362.91 | 0.00 |
| B2, item_4 → table_1 | 6, 1, 7 | 4 73.5, 7 73.6, 6 85.9, 1 130.0 | 4 | 6 | 6 7 1 4, 311.91 | 77.74 |
| B2, item_6 → table_0 | 4, 1, 7 | 6 39.3, 7 73.6, 1 130.0, 4 137.8 | 6 | 7 | 7 6 1 4, 310.84 | 39.16 |
| B2, item_1 → table_0 (= A1) | 4, 6, 7 | 1 61.4, 7 73.6, 6 85.9, 4 137.8 | 1 | 7 | 7 6 4 1, 293.92 | 56.64 |
| B2, item_7 → table_1 (= B1) | 4, 6, 1 | 7 53.4, 6 85.9, 1 130.0, 4 137.8 | 7 | 6 | 6 7 4 1, 351.46 | 37.28 |

Neither A2 nor B2 separates the heads, so T-B1d's R4 run was not made.

## The finding

single_task takes the cheapest task from the robot's position; full_reorder takes the task whose delivery leaves the
robot best placed for the remaining shelves; the two heads differ exactly when the cheapest-from-here task ends at a
table far from the remaining shelves, which the destination fact decides. Across the nine distinct sets priced on
env_layout8's geometry besides env_layout8's own (the rows above, duplicates counted once: against-proximity sets
{4,6,7}, {4,7}, {4,6}, {4,1,6}, {4,1}, {6}, {4,6,1,7}, {6,1,7}, {4,1,7}) the heads differ in seven (gaps 14 to 78
ticks) and coincide in two ({4,6} and {4,6,1,7}); every flip traces to the one designation that moves the cheapest
single task, which is the mechanism, not a weakness of any fixture. Generality across layouts is T-F's (randomised
layouts), not a hand-built scenario's (TODO-47 (f-designations)).

The T-B3 fixtures are unchanged by this record: scenario_80, scenario_81 (two tables), scenario_83 (the realized-cost
existence case, `analysis/tb1c_realized_flip/`) and the one-table regression set.
