### scenario_s09_08

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_1,kitting_table_1) | binding_absent | move_to | 0 | 1 |
| 30 | deliver_item(item_1,kitting_table_1) | binding_absent | pick_up | 0 | 1 |
| 32 | deliver_item(item_1,kitting_table_1) | binding_absent | move_to | 1 | 1 |
| 75 | deliver_item(item_1,kitting_table_1) | binding_absent | place | 0 | 1 |
| 77 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 99 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 101 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 131 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 133 | go_to(corner_SE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 180; idle from 181 to 210. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 210 |
| deliver_item(item_1) | move_to(item_1) | -1 to 27 |
| deliver_item(item_1) | pick_up(item_1) | 28 to 29 |
| deliver_item(item_1) | move_to(kitting_table_0) | 30 to 74 |
| deliver_item(item_1) | pick_up(item_1) | 75 to 76 |
| deliver_item(item_1) | move_to(item_1) | 77 to 98 |
| deliver_item(item_1) | place(item_2,shelf_2) | 99 to 100 |
| deliver_item(item_1) | move_to(shelf_2) | 101 to 130 |
| deliver_item(item_1) | move_to(item_1) | 131 to 210 |
| deliver_item(item_2) | move_to(item_2) | -1 to 29 |
| deliver_item(item_2) | place(item_1,shelf_1) | 30 to 31 |
| deliver_item(item_2) | move_to(shelf_1) | 32 to 74 |
| deliver_item(item_2) | move_to(item_2) | 75 to 96 |
| deliver_item(item_2) | pick_up(item_2) | 97 to 98 |
| deliver_item(item_2) | move_to(kitting_table_0) | 99 to 128 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 129 to 130 |

Events (actual):

| tick | event |
|---|---|
| 66 | finding turns unexplained |
| 75 | boundary (no pin) |
| 75 | finding turns unresolved (from unexplained) |
| 131 | boundary |
| 131 | pin deliver_item(item_2) |
| 164 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), deliver_item(item_1). At the last entry (go_to(corner_SE), ticks 133 to 180): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_2) | 77 to 132 | 96 | 0.7531 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver_item(item_2) | move_to(item_2) | 0.0315 | 0.0399 | 357.3 | 357.3 | 0.0 | - |
| 35 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0561 | 0.0427 | 350.5 | 290.5 | 60.0 | - |
| 41 | deliver_item(item_2) | move_to(shelf_1) | 0.0010 | 0.0391 | 359.4 | 359.4 | 0.0 | - |
| 66 | deliver_item(item_1) | move_to(kitting_table_0) | 0.9970 | 0.0453 | 344.5 | 344.5 | 0.0 | - |
| 86 | deliver_item(item_1) | move_to(item_1) | 0.0322 | 0.0410 | 354.8 | 354.8 | 0.0 | deliver_item(item_2) |
| 106 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0586 | 0.0457 | 343.7 | 283.7 | 60.0 | deliver_item(item_2) |
| 110 | deliver_item(item_1) | move_to(shelf_2) | 0.0010 | 0.0394 | 358.8 | 358.8 | 0.0 | deliver_item(item_2) |
| 149 | deliver_item(item_1) | move_to(item_1) | 0.1001 | 0.0384 | 361.2 | 361.2 | 0.0 | - |
| 164 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9934 | 0.0482 | 338.2 | 338.2 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | - |
| 66 | adequate | unexplained | - |
| 75 | unexplained | unresolved | - |
| 76 | unresolved | adequate | - |
| 131 | adequate | unresolved | deliver_item(item_2) |
| 132 | unresolved | adequate | deliver_item(item_2) |
| 164 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 66, 77 to 130, 133 to 210 |
| deliver_item(item_1) | 0 to 74, 133 to 146 |
| deliver_item(item_2) | 0 to 1, 77 to 130 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 24 | deliver_item(item_1) | none(below_theta) |
| 25 to 65 | deliver_item(item_1) | clears |
| 66 to 74 | deliver_item(item_1) | none(leader_inadequate) |
| 75 to 76 | coffee_break(coffee_machine_0) | none(below_theta) |
| 77 to 77 | deliver_item(item_1) | none(below_theta) |
| 78 to 95 | deliver_item(item_2) | none(below_theta) |
| 96 to 130 | deliver_item(item_2) | clears |
| 131 to 143 | coffee_break(coffee_machine_0) | none(below_theta) |
| 144 to 163 | coffee_break(coffee_machine_0) | clears |
| 164 to 210 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(corner_SE)): first step 133, last step 179, acknowledgement 180; the idle human from 181. Live at its first tick: coffee_break(coffee_machine_0), deliver_item(item_1).

- coffee_break(coffee_machine_0): belief 0.5083 at 133; S < α from 164 (belief 0.9934; v·D 338.2 cm); the finding unexplained from 164.

- deliver_item(item_1): belief 0.4897 at 133; S < α from 149 (belief 0.1001; v·D 361.2 cm); the finding unexplained from 164.

