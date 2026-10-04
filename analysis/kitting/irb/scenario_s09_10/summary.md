### scenario_s09_10

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 30 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 32 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 61 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 63 | deliver_item(item_3,kitting_table_0) | covered | move_to | 0 | 1 |
| 84 | deliver_item(item_3,kitting_table_0) | covered | pick_up | 0 | 1 |
| 86 | deliver_item(item_3,kitting_table_0) | covered | move_to | 1 | 1 |
| 107 | deliver_item(item_3,kitting_table_0) | covered | place | 0 | 1 |
| 109 | go_to(corner_SE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 157; idle from 158 to 187. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_3).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 187 |
| deliver_item(item_1) | move_to(item_1) | -1 to 27 |
| deliver_item(item_1) | pick_up(item_1) | 28 to 29 |
| deliver_item(item_1) | move_to(kitting_table_0) | 30 to 58 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 59 to 60 |
| deliver_item(item_3) | move_to(item_3) | -1 to 29 |
| deliver_item(item_3) | place(item_1,shelf_1) | 30 to 31 |
| deliver_item(item_3) | move_to(shelf_1) | 32 to 60 |
| deliver_item(item_3) | move_to(item_3) | 61 to 81 |
| deliver_item(item_3) | pick_up(item_3) | 82 to 83 |
| deliver_item(item_3) | move_to(kitting_table_0) | 84 to 104 |
| deliver_item(item_3) | place(item_3,kitting_table_0) | 105 to 106 |

Events (actual):

| tick | event |
|---|---|
| 61 | boundary |
| 61 | pin deliver_item(item_1) |
| 107 | boundary |
| 107 | pin deliver_item(item_3) |
| 141 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(corner_SE), ticks 109 to 157): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_1) | 0 to 62 | 27 | 0.7744 | yes | adequate |
| deliver_item(item_3) | 63 to 108 | 74 | 0.7617 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 25 | deliver_item(item_3) | move_to(item_3) | 0.0438 | 0.0444 | 346.5 | 346.5 | 0.0 | deliver_item(item_1) |
| 34 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0574 | 0.0451 | 345.0 | 285.0 | 60.0 | deliver_item(item_1) |
| 41 | deliver_item(item_3) | move_to(shelf_1) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 83 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0598 | 0.0468 | 341.3 | 321.3 | 20.0 | deliver_item(item_3) |
| 141 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9970 | 0.0418 | 352.6 | 352.6 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_1) |
| 61 | adequate | unresolved | deliver_item(item_1) |
| 62 | unresolved | adequate | deliver_item(item_1) |
| 107 | adequate | unresolved | deliver_item(item_3) |
| 108 | unresolved | adequate | deliver_item(item_3) |
| 141 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 60, 63 to 103, 109 to 187 |
| deliver_item(item_1) | 0 to 60 |
| deliver_item(item_3) | 0 to 29, 63 to 106 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 26 | deliver_item(item_1) | none(below_theta) |
| 27 to 60 | deliver_item(item_1) | clears |
| 61 to 62 | coffee_break(coffee_machine_0) | none(below_theta) |
| 63 to 73 | deliver_item(item_3) | none(below_theta) |
| 74 to 106 | deliver_item(item_3) | clears |
| 107 to 107 | coffee_break(coffee_machine_0) | none(leader_no_observation) |
| 108 to 108 | coffee_break(coffee_machine_0) | none(leader_unwarranted) |
| 109 to 140 | coffee_break(coffee_machine_0) | clears |
| 141 to 187 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(corner_SE)): first step 109, last step 156, acknowledgement 157; the idle human from 158. Live at its first tick: coffee_break(coffee_machine_0).

- coffee_break(coffee_machine_0): belief 0.9970 at 109; S < α from 141 (belief 0.9970; v·D 352.6 cm); the finding unexplained from 141.

