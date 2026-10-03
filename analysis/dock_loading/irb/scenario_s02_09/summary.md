### scenario_s02_09

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 14 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 2 |
| 52 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 2 |
| 83 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 133 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 134 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 136 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 186 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 188 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 213; idle from 214 to 243. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 49 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 50 to 80 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 83 to 243 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 130 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 131 to 133 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 183 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 184 to 185 |
| office_break(office_chair) | move_to(office_door) | -1 to 243 |

Events (actual):

| tick | event |
|---|---|
| 22 | finding turns unexplained |
| 50 | finding turns adequate (from unexplained) |
| 81 | boundary |
| 81 | pin coffee_break(coffee_machine_0) |
| 83 | re-entry coffee_break(coffee_machine_0) |
| 134 | boundary |
| 134 | pin confirm_delivered_pallet(pallet_0) |
| 186 | boundary |
| 186 | pin confirm_delivered_pallet(pallet_2) |
| 204 | finding turns unexplained |

Never pinned: office_break(office_chair). At the last entry (go_to(desk), ticks 188 to 213): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 13 | 10 | 0.7745 | yes | adequate |
| coffee_break(coffee_machine_0) | 14 to 82 | 51 | 0.7676 | yes | adequate |
| confirm_delivered_pallet(pallet_0) | 83 to 135 | 109 | 0.7533 | yes | adequate |
| confirm_delivered_pallet(pallet_2) | 136 to 187 | 185 | 0.7643 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 8 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0409 | 0.0445 | 346.4 | 346.4 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 9 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0406 | 0.0409 | 355.0 | 355.0 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 18 | office_break(office_chair) | move_to(office_door) | 0.1967 | 0.0487 | 337.2 | 337.2 | 0.0 | coffee_break(coffee_machine_0) |
| 22 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.4639 | 0.0407 | 355.3 | 355.3 | 0.0 | coffee_break(coffee_machine_0) |
| 92 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0244 | 0.0389 | 360.0 | 360.0 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 94 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0266 | 0.0387 | 360.6 | 360.6 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 115 | office_break(office_chair) | move_to(office_door) | 0.0603 | 0.0478 | 339.0 | 339.0 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 168 | office_break(office_chair) | move_to(office_door) | 0.0276 | 0.0389 | 359.9 | 359.9 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 203 | office_break(office_chair) | move_to(office_door) | 0.3880 | 0.0420 | 352.2 | 352.2 | 0.0 | - |
| 204 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.5757 | 0.0449 | 345.5 | 345.5 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 22 | adequate | unexplained | coffee_break(coffee_machine_0) |
| 50 | unexplained | adequate | coffee_break(coffee_machine_0) |
| 81 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 82 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 134 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 135 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 186 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 187 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 204 | adequate | unexplained | - |

Across the started task coffee_break(coffee_machine_0) (covered; actual): on top of the stack from 14 to 82, its hypothesis pinned at 81; the suspended task resumes at 83.

| tick | human action | truth | coffee_break(coffee_machine_0) belief / S | confirm_delivered_pallet(pallet_0) belief / S | confirm_delivered_pallet(pallet_2) belief / S | office_break(office_chair) belief / S | finding |
|---|---|---|---|---|---|---|---|
| 12 | move_to step | confirm_delivered_pallet(pallet_0) | 0.0112 / 0.0095 | 0.8544 / 1.0000 | 0.0161 / 0.0137 | 0.1054 / 0.0918 | adequate |
| 13 | move_to step | confirm_delivered_pallet(pallet_0) | 0.0078 / 0.0064 | 0.8852 / 1.0000 | 0.0115 / 0.0094 | 0.0824 / 0.0687 | adequate |
| 14 | move_to step | coffee_break(coffee_machine_0) | 0.0095 / 0.0064 | 0.8684 / 0.7448 | 0.0140 / 0.0094 | 0.0951 / 0.0651 | adequate |
| 15 | move_to step | coffee_break(coffee_machine_0) | 0.0120 / 0.0064 | 0.8454 / 0.5421 | 0.0174 / 0.0093 | 0.1123 / 0.0613 | adequate |
| 16 | move_to step | coffee_break(coffee_machine_0) | 0.0153 / 0.0064 | 0.8147 / 0.3870 | 0.0222 / 0.0093 | 0.1348 / 0.0573 | adequate |
| 80 | wait_at stand | coffee_break(coffee_machine_0) | 0.9840 / 1.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | adequate |
| 81 | wait_at stand | coffee_break(coffee_machine_0) | retired | 0.3287 / - | 0.3287 / - | 0.3287 / - | unresolved |
| 82 | wait_at  | coffee_break(coffee_machine_0) | retired | 0.3287 / 1.0000 | 0.3287 / 1.0000 | 0.3287 / 1.0000 | adequate |
| 83 | move_to step | confirm_delivered_pallet(pallet_0) | 0.2467 / - | 0.2564 / 1.0000 | 0.2289 / 0.8534 | 0.2549 / 0.9920 | adequate |
| 84 | move_to step | confirm_delivered_pallet(pallet_0) | 0.2154 / 0.7402 | 0.2788 / 1.0000 | 0.2171 / 0.7114 | 0.2756 / 0.9835 | adequate |
| 85 | move_to step | confirm_delivered_pallet(pallet_0) | 0.1818 / 0.5355 | 0.3046 / 1.0000 | 0.2014 / 0.5789 | 0.2992 / 0.9743 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 27 to 80, 136 to 185, 188 to 203 |
| confirm_delivered_pallet(pallet_0) | 0 to 27, 83 to 133 |
| confirm_delivered_pallet(pallet_2) | 25 to 80, 136 to 185 |
| office_break(office_chair) | 0 to 10, 15 to 35, 83 to 133, 136 to 183, 188 to 197 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 9 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 10 to 17 | confirm_delivered_pallet(pallet_0) | clears |
| 18 to 23 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 24 to 28 | office_break(office_chair) | none(below_theta) |
| 29 to 38 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 39 to 50 | coffee_break(coffee_machine_0) | none(below_theta) |
| 51 to 80 | coffee_break(coffee_machine_0) | clears |
| 81 to 108 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 109 to 133 | confirm_delivered_pallet(pallet_0) | clears |
| 134 to 135 | coffee_break(coffee_machine_0) | none(below_theta) |
| 136 to 184 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 185 to 185 | confirm_delivered_pallet(pallet_2) | clears |
| 186 to 207 | coffee_break(coffee_machine_0) | none(below_theta) |
| 208 to 243 | office_break(office_chair) | none(below_theta) |

The last entry (go_to(desk)): first step 188, last step 212, acknowledgement 213; the idle human from 214. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.5104 at 188; S < α from 204 (belief 0.5757; v·D 345.5 cm); the finding unexplained from 204.

- office_break(office_chair): belief 0.4746 at 188; S < α from 203 (belief 0.3880; v·D 352.2 cm); the finding unexplained from 204.

