### scenario_s09_12

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 30 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 32 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 61 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 63 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 93 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 95 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 124 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 126 | go_to(corner_SE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 174; idle from 175 to 204. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 204 |
| deliver_item(item_1) | move_to(item_1) | -1 to 29 |
| deliver_item(item_1) | place(item_2,shelf_2) | 30 to 31 |
| deliver_item(item_1) | move_to(shelf_2) | 32 to 60 |
| deliver_item(item_1) | move_to(item_1) | 61 to 90 |
| deliver_item(item_1) | pick_up(item_1) | 91 to 92 |
| deliver_item(item_1) | move_to(kitting_table_0) | 93 to 121 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 122 to 123 |
| deliver_item(item_2) | move_to(item_2) | -1 to 27 |
| deliver_item(item_2) | pick_up(item_2) | 28 to 29 |
| deliver_item(item_2) | move_to(kitting_table_0) | 30 to 58 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 59 to 60 |

Events (actual):

| tick | event |
|---|---|
| 61 | boundary |
| 61 | pin deliver_item(item_2) |
| 124 | boundary |
| 124 | pin deliver_item(item_1) |
| 157 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(corner_SE), ticks 126 to 174): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_2) | 0 to 62 | 7 | 0.7549 | yes | adequate |
| deliver_item(item_1) | 63 to 125 | 63 | 0.9807 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver_item(item_1) | move_to(item_1) | 0.0511 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver_item(item_2) |
| 24 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0023 | 0.0420 | 352.1 | 352.1 | 0.0 | deliver_item(item_2) |
| 41 | deliver_item(item_1) | move_to(shelf_2) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_2) |
| 97 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0011 | 0.0408 | 355.2 | 295.2 | 60.0 | deliver_item(item_1) |
| 157 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9970 | 0.0469 | 341.1 | 341.1 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_2) |
| 61 | adequate | unresolved | deliver_item(item_2) |
| 62 | unresolved | adequate | deliver_item(item_2) |
| 124 | adequate | unresolved | deliver_item(item_1) |
| 125 | unresolved | adequate | deliver_item(item_1) |
| 157 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 60, 63 to 123, 126 to 204 |
| deliver_item(item_1) | 0 to 1, 63 to 123 |
| deliver_item(item_2) | 0 to 60 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 6 | deliver_item(item_2) | none(below_theta) |
| 7 to 60 | deliver_item(item_2) | clears |
| 61 to 61 | deliver_item(item_1) | none(leader_no_observation) |
| 62 to 123 | deliver_item(item_1) | clears |
| 124 to 124 | coffee_break(coffee_machine_0) | none(leader_no_observation) |
| 125 to 125 | coffee_break(coffee_machine_0) | none(leader_unwarranted) |
| 126 to 156 | coffee_break(coffee_machine_0) | clears |
| 157 to 204 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

Context knowledge (actual): per foreseeable task its level, and the recency facts, as stretches of ticks (the prior's inputs; `[IR-context]`).

| what | stretches |
|---|---|
| level of coffee_break | 0 to 204 ordinary |
| recency facts | 0 to 204 none |

The last entry (go_to(corner_SE)): first step 126, last step 173, acknowledgement 174; the idle human from 175. Live at its first tick: coffee_break(coffee_machine_0).

- coffee_break(coffee_machine_0): belief 0.9970 at 126; S < α from 157 (belief 0.9970; v·D 341.1 cm); the finding unexplained from 157.

