### scenario_s08_03

Script actions (replay expanded per tick; the first tick of each action):

| tick | task | action | occurrence |
|---|---|---|---|
| 0 | deliver item_1 | move_to | 0 |
| 30 | deliver item_1 | pick_up | 0 |
| 32 | coffee_break | move_to | 0 |
| 55 | coffee_break | wait_at | 0 |
| 86 | deliver item_1 | move_to | 0 |
| 127 | deliver item_1 | place | 0 |
| 129 | deliver item_2 | move_to | 0 |
| 159 | deliver item_2 | pick_up | 0 |
| 161 | deliver item_2 | move_to | 1 |
| 191 | deliver item_2 | place | 0 |
| 193 | go_to(?landmark=corner_SE) | move_to | 0 |

Last acknowledgement tick 240; idle from 241 to 270.

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break | move_to(?target=coffee_machine_0) | -1 to 52 |
| coffee_break | wait_at(?duration=PT60S,?entity=coffee_machine_0) | 53 to 83 |
| deliver item_1 | move_to(?target=item_1) | -1 to 27 |
| deliver item_1 | pick_up(?item=item_1) | 28 to 29 |
| deliver item_1 | move_to(?target=kitting_table_0) | 30 to 124 |
| deliver item_1 | place(?item=item_1,?target=kitting_table_0) | 125 to 126 |
| deliver item_2 | move_to(?target=item_2) | -1 to 29 |
| deliver item_2 | place(?item=item_1,?target=shelf_1) | 30 to 32 |
| deliver item_2 | move_to(?target=shelf_1) | 33 to 126 |
| deliver item_2 | move_to(?target=item_2) | 127 to 156 |
| deliver item_2 | pick_up(?item=item_2) | 157 to 158 |
| deliver item_2 | move_to(?target=kitting_table_0) | 159 to 188 |
| deliver item_2 | place(?item=item_2,?target=kitting_table_0) | 189 to 190 |

Events (actual):

| tick | event |
|---|---|
| 84 | boundary |
| 84 | pin coffee_break |
| 127 | boundary |
| 127 | pin deliver item_1 |
| 191 | boundary |
| 191 | exhausted (no live hypothesis) from here |
| 191 | pin deliver item_2 |

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver item_1 | 0 to 31 | 25 | 0.7552 | yes | adequate |
| coffee_break | 32 to 85 | 45 | 0.8044 | yes | adequate |
| deliver item_1 | 86 to 128 | 100 | 0.7779 | yes | adequate |
| deliver item_2 | 129 to 192 | 129 | 0.9980 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver item_2 | move_to(?target=item_2) | 0.0315 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver item_1 |
| 42 | deliver item_2 | move_to(?target=shelf_1) | 0.0010 | 0.0422 | 351.8 | 351.8 | 0.0 | coffee_break |
| 43 | deliver item_1 | move_to(?target=kitting_table_0) | 0.3117 | 0.0440 | 347.5 | 347.5 | 0.0 | coffee_break |
| 107 | deliver item_2 | move_to(?target=shelf_1) | 0.0553 | 0.0429 | 350.0 | 350.0 | 0.0 | deliver item_1 |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver item_1 |
| 84 | adequate | unresolved | coffee_break |
| 85 | unresolved | adequate | coffee_break |
| 127 | adequate | unresolved | deliver item_1 |
| 128 | unresolved | adequate | deliver item_1 |
| 191 | adequate | exhausted | deliver item_2 |

Across the coffee boundary (actual): the coffee_break starts at 32 (its walk), is pinned at 84 (the boundary), and the suspended delivery resumes at 86.

| tick | human action | truth | coffee_break belief / S | deliver item_1 belief / S | deliver item_2 belief / S | finding |
|---|---|---|---|---|---|---|
| 30 | pick_up grasp | deliver item_1 | 0.1374 / 0.1199 | 0.8616 / 1.0000 | 0.0010 / 1.0000 | adequate |
| 31 | pick_up  | deliver item_1 | 0.1169 / 0.0989 | 0.8821 / 1.0000 | 0.0010 / 1.0000 | adequate |
| 32 | move_to step | coffee_break | 0.1319 / 0.0989 | 0.8671 / 0.8248 | 0.0010 / 1.0000 | adequate |
| 33 | move_to step | coffee_break | 0.1511 / 0.0989 | 0.8479 / 0.6702 | 0.0010 / - | adequate |
| 34 | move_to step | coffee_break | 0.1756 / 0.0989 | 0.8234 / 0.5366 | 0.0010 / 0.7594 | adequate |
| 83 | wait_at stand | coffee_break | 0.9980 / 1.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | adequate |
| 84 | wait_at stand | coffee_break | retired | 0.4995 / - | 0.4995 / - | unresolved |
| 85 | wait_at  | coffee_break | retired | 0.4995 / 1.0000 | 0.4995 / 1.0000 | adequate |
| 86 | move_to step | deliver item_1 | retired | 0.5076 / 1.0000 | 0.4914 / 0.9544 | adequate |
| 87 | move_to step | deliver item_1 | retired | 0.5167 / 1.0000 | 0.4823 / 0.9068 | adequate |
| 88 | move_to step | deliver item_1 | retired | 0.5269 / 1.0000 | 0.4721 / 0.8571 | adequate |

Exit walk (go_to corner_SE): first step 193, last step 239, acknowledgement 240; the idle human from 241. Live at its first tick: none (exhausted).

