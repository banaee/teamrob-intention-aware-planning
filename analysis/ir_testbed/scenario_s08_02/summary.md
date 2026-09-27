### scenario_s08_02

Script actions (replay expanded per tick; the first tick of each action):

| tick | task | action | occurrence |
|---|---|---|---|
| 0 | deliver item_1 | move_to | 0 |
| 30 | deliver item_1 | pick_up | 0 |
| 32 | deliver item_1 | move_to | 1 |
| 61 | deliver item_1 | place | 0 |
| 63 | coffee_break | move_to | 0 |
| 104 | coffee_break | wait_at | 0 |
| 135 | deliver item_2 | move_to | 0 |
| 169 | deliver item_2 | pick_up | 0 |
| 171 | deliver item_2 | move_to | 1 |
| 201 | deliver item_2 | place | 0 |
| 203 | go_to(?landmark=corner_SE) | move_to | 0 |

Last acknowledgement tick 250; idle from 251 to 280.

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break | move_to(?target=coffee_machine_0) | -1 to 101 |
| coffee_break | wait_at(?duration=PT60S,?entity=coffee_machine_0) | 102 to 132 |
| deliver item_1 | move_to(?target=item_1) | -1 to 27 |
| deliver item_1 | pick_up(?item=item_1) | 28 to 29 |
| deliver item_1 | move_to(?target=kitting_table_0) | 30 to 58 |
| deliver item_1 | place(?item=item_1,?target=kitting_table_0) | 59 to 60 |
| deliver item_2 | move_to(?target=item_2) | -1 to 29 |
| deliver item_2 | place(?item=item_1,?target=shelf_1) | 30 to 31 |
| deliver item_2 | move_to(?target=shelf_1) | 32 to 60 |
| deliver item_2 | move_to(?target=item_2) | 61 to 166 |
| deliver item_2 | pick_up(?item=item_2) | 167 to 168 |
| deliver item_2 | move_to(?target=kitting_table_0) | 169 to 198 |
| deliver item_2 | place(?item=item_2,?target=kitting_table_0) | 199 to 200 |

Events (actual):

| tick | event |
|---|---|
| 61 | boundary |
| 61 | pin deliver item_1 |
| 133 | boundary |
| 133 | pin coffee_break |
| 201 | boundary |
| 201 | exhausted (no live hypothesis) from here |
| 201 | pin deliver item_2 |

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver item_1 | 0 to 62 | 25 | 0.7552 | yes | adequate |
| coffee_break | 63 to 134 | 75 | 0.7552 | yes | adequate |
| deliver item_2 | 135 to 202 | 135 | 0.9980 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver item_2 | move_to(?target=item_2) | 0.0315 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver item_1 |
| 34 | coffee_break | move_to(?target=coffee_machine_0) | 0.0579 | 0.0451 | 345.0 | 285.0 | 60.0 | deliver item_1 |
| 41 | deliver item_2 | move_to(?target=shelf_1) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver item_1 |
| 84 | deliver item_2 | move_to(?target=item_2) | 0.0554 | 0.0430 | 349.9 | 349.9 | 0.0 | coffee_break |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver item_1 |
| 61 | adequate | unresolved | deliver item_1 |
| 62 | unresolved | adequate | deliver item_1 |
| 133 | adequate | unresolved | coffee_break |
| 134 | unresolved | adequate | coffee_break |
| 201 | adequate | exhausted | deliver item_2 |

Exit walk (go_to corner_SE): first step 203, last step 249, acknowledgement 250; the idle human from 251. Live at its first tick: none (exhausted).

