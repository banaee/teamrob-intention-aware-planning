### scenario_s09_11

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 30 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 32 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 61 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 63 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 1 |
| 104 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 1 |
| 135 | deliver_item(item_3,kitting_table_0) | covered | move_to | 0 | 1 |
| 171 | deliver_item(item_3,kitting_table_0) | covered | pick_up | 0 | 1 |
| 173 | deliver_item(item_3,kitting_table_0) | covered | move_to | 1 | 1 |
| 195 | deliver_item(item_3,kitting_table_0) | covered | place | 0 | 1 |
| 197 | go_to(corner_SE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 245; idle from 246 to 275. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_3).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 101 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 102 to 132 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 135 to 275 |
| deliver_item(item_1) | move_to(item_1) | -1 to 27 |
| deliver_item(item_1) | pick_up(item_1) | 28 to 29 |
| deliver_item(item_1) | move_to(kitting_table_0) | 30 to 58 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 59 to 60 |
| deliver_item(item_3) | move_to(item_3) | -1 to 29 |
| deliver_item(item_3) | place(item_1,shelf_1) | 30 to 31 |
| deliver_item(item_3) | move_to(shelf_1) | 32 to 60 |
| deliver_item(item_3) | move_to(item_3) | 61 to 168 |
| deliver_item(item_3) | pick_up(item_3) | 169 to 170 |
| deliver_item(item_3) | move_to(kitting_table_0) | 171 to 192 |
| deliver_item(item_3) | place(item_3,kitting_table_0) | 193 to 194 |

Events (actual):

| tick | event |
|---|---|
| 61 | boundary |
| 61 | pin deliver_item(item_1) |
| 133 | boundary |
| 133 | pin coffee_break(coffee_machine_0) |
| 135 | re-entry coffee_break(coffee_machine_0) |
| 195 | boundary |
| 195 | pin deliver_item(item_3) |
| 229 | finding turns unexplained |

Never pinned: none. At the last entry (go_to(corner_SE), ticks 197 to 245): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_1) | 0 to 62 | 27 | 0.7736 | yes | adequate |
| coffee_break(coffee_machine_0) | 63 to 134 | 73 | 0.7789 | yes | adequate |
| deliver_item(item_3) | 135 to 196 | 140 | 0.8044 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 25 | deliver_item(item_3) | move_to(item_3) | 0.0438 | 0.0444 | 346.5 | 346.5 | 0.0 | deliver_item(item_1) |
| 34 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0574 | 0.0451 | 345.0 | 285.0 | 60.0 | deliver_item(item_1) |
| 41 | deliver_item(item_3) | move_to(shelf_1) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 80 | deliver_item(item_3) | move_to(item_3) | 0.0508 | 0.0392 | 359.2 | 359.2 | 0.0 | coffee_break(coffee_machine_0) |
| 144 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0510 | 0.0394 | 358.8 | 358.8 | 0.0 | deliver_item(item_3) |
| 229 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9970 | 0.0416 | 353.2 | 353.2 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_1) |
| 61 | adequate | unresolved | deliver_item(item_1) |
| 62 | unresolved | adequate | deliver_item(item_1) |
| 133 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 134 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 195 | adequate | unresolved | deliver_item(item_3) |
| 196 | unresolved | adequate | deliver_item(item_3) |
| 229 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 60, 63 to 132, 197 to 275 |
| deliver_item(item_1) | 0 to 60 |
| deliver_item(item_3) | 0 to 29, 63 to 80, 135 to 194 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 26 | deliver_item(item_1) | none(below_theta) |
| 27 to 60 | deliver_item(item_1) | clears |
| 61 to 72 | coffee_break(coffee_machine_0) | none(below_theta) |
| 73 to 132 | coffee_break(coffee_machine_0) | clears |
| 133 to 133 | deliver_item(item_3) | none(leader_no_observation) |
| 134 to 134 | deliver_item(item_3) | clears |
| 135 to 135 | coffee_break(coffee_machine_0) | none(below_theta) |
| 136 to 139 | deliver_item(item_3) | none(below_theta) |
| 140 to 194 | deliver_item(item_3) | clears |
| 195 to 195 | coffee_break(coffee_machine_0) | none(leader_no_observation) |
| 196 to 196 | coffee_break(coffee_machine_0) | none(leader_unwarranted) |
| 197 to 228 | coffee_break(coffee_machine_0) | clears |
| 229 to 275 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(corner_SE)): first step 197, last step 244, acknowledgement 245; the idle human from 246. Live at its first tick: coffee_break(coffee_machine_0).

- coffee_break(coffee_machine_0): belief 0.9970 at 197; S < α from 229 (belief 0.9970; v·D 353.2 cm); the finding unexplained from 229.

