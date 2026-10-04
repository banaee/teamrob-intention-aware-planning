### scenario_s08_02

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 30 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 32 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 61 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 63 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 1 |
| 104 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 1 |
| 135 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 169 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 171 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 201 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 203 | go_to(corner_SE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 250; idle from 251 to 280. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 101 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 102 to 132 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 135 to 280 |
| deliver_item(item_1) | move_to(item_1) | -1 to 27 |
| deliver_item(item_1) | pick_up(item_1) | 28 to 29 |
| deliver_item(item_1) | move_to(kitting_table_0) | 30 to 58 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 59 to 60 |
| deliver_item(item_2) | move_to(item_2) | -1 to 29 |
| deliver_item(item_2) | place(item_1,shelf_1) | 30 to 31 |
| deliver_item(item_2) | move_to(shelf_1) | 32 to 60 |
| deliver_item(item_2) | move_to(item_2) | 61 to 166 |
| deliver_item(item_2) | pick_up(item_2) | 167 to 168 |
| deliver_item(item_2) | move_to(kitting_table_0) | 169 to 198 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 199 to 200 |

Events (actual):

| tick | event |
|---|---|
| 61 | boundary |
| 61 | pin deliver_item(item_1) |
| 133 | boundary |
| 133 | pin coffee_break(coffee_machine_0) |
| 135 | re-entry coffee_break(coffee_machine_0) |
| 201 | boundary |
| 201 | pin deliver_item(item_2) |
| 234 | finding turns unexplained |

Never pinned: none. At the last entry (go_to(corner_SE), ticks 203 to 250): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_1) | 0 to 62 | 8 | 0.7837 | yes | adequate |
| coffee_break(coffee_machine_0) | 63 to 134 | 93 | 0.7917 | yes | adequate |
| deliver_item(item_2) | 135 to 202 | 135 | 0.9950 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver_item(item_2) | move_to(item_2) | 0.0505 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver_item(item_1) |
| 34 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0025 | 0.0451 | 345.0 | 285.0 | 60.0 | deliver_item(item_1) |
| 41 | deliver_item(item_2) | move_to(shelf_1) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 84 | deliver_item(item_2) | move_to(item_2) | 0.7450 | 0.0430 | 349.9 | 349.9 | 0.0 | coffee_break(coffee_machine_0) |
| 144 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0010 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver_item(item_2) |
| 234 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9980 | 0.0447 | 346.0 | 346.0 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_1) |
| 61 | adequate | unresolved | deliver_item(item_1) |
| 62 | unresolved | adequate | deliver_item(item_1) |
| 133 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 134 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 201 | adequate | unresolved | deliver_item(item_2) |
| 202 | unresolved | adequate | deliver_item(item_2) |
| 234 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 60, 63 to 132, 203 to 280 |
| deliver_item(item_1) | 0 to 60 |
| deliver_item(item_2) | 0 to 1, 63 to 95, 135 to 200 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 7 | deliver_item(item_1) | none(below_theta) |
| 8 to 60 | deliver_item(item_1) | clears |
| 61 to 61 | deliver_item(item_2) | none(leader_no_observation) |
| 62 to 83 | deliver_item(item_2) | clears |
| 84 to 88 | deliver_item(item_2) | none(below_theta) |
| 89 to 92 | coffee_break(coffee_machine_0) | none(below_theta) |
| 93 to 132 | coffee_break(coffee_machine_0) | clears |
| 133 to 133 | deliver_item(item_2) | none(leader_no_observation) |
| 134 to 200 | deliver_item(item_2) | clears |
| 201 to 201 | coffee_break(coffee_machine_0) | none(leader_no_observation) |
| 202 to 202 | coffee_break(coffee_machine_0) | none(leader_unwarranted) |
| 203 to 233 | coffee_break(coffee_machine_0) | clears |
| 234 to 280 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

Context knowledge (actual): per foreseeable task its level, and the recency facts, as stretches of ticks (the prior's inputs; `[IR-context]`).

| what | stretches |
|---|---|
| level of coffee_break | 0 to 132 ordinary, 133 to 134 retired, 135 to 222 suppressed, 223 to 280 ordinary |
| recency facts | 0 to 132 none, 133 to 222 coffee_break, 223 to 280 none |

The last entry (go_to(corner_SE)): first step 203, last step 249, acknowledgement 250; the idle human from 251. Live at its first tick: coffee_break(coffee_machine_0).

- coffee_break(coffee_machine_0): belief 0.9980 at 203; S < α from 234 (belief 0.9980; v·D 346.0 cm); the finding unexplained from 234.

