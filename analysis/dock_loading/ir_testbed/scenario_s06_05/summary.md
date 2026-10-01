### scenario_s06_05

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 17 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 19 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 37 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 39 | confirm_delivered_pallet(pallet_1) | covered | move_to | 0 | 1 |
| 56 | confirm_delivered_pallet(pallet_1) | covered | scan_it | 0 | 1 |
| 58 | confirm_delivered_pallet(pallet_3) | covered | move_to | 0 | 1 |
| 75 | confirm_delivered_pallet(pallet_3) | covered | scan_it | 0 | 1 |
| 77 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 118; idle from 119 to 148. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_1), confirm_delivered_pallet(pallet_2), confirm_delivered_pallet(pallet_3), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 148 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 14 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 15 to 16 |
| confirm_delivered_pallet(pallet_1) | move_to(pallet_1) | -1 to 14 |
| confirm_delivered_pallet(pallet_1) | scan_it(pallet_1) | 15 to 19 |
| confirm_delivered_pallet(pallet_1) | move_to(pallet_1) | 20 to 53 |
| confirm_delivered_pallet(pallet_1) | scan_it(pallet_1) | 54 to 55 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 34 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 35 to 36 |
| confirm_delivered_pallet(pallet_3) | move_to(pallet_3) | -1 to 34 |
| confirm_delivered_pallet(pallet_3) | scan_it(pallet_3) | 35 to 38 |
| confirm_delivered_pallet(pallet_3) | move_to(pallet_3) | 39 to 72 |
| confirm_delivered_pallet(pallet_3) | scan_it(pallet_3) | 73 to 74 |
| office_break(office_chair) | move_to(office_door) | -1 to 148 |

Events (actual):

| tick | event |
|---|---|
| 17 | boundary |
| 17 | pin confirm_delivered_pallet(pallet_0) |
| 37 | boundary |
| 37 | pin confirm_delivered_pallet(pallet_2) |
| 56 | boundary |
| 56 | pin confirm_delivered_pallet(pallet_1) |
| 75 | boundary |
| 75 | pin confirm_delivered_pallet(pallet_3) |
| 100 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), office_break(office_chair). At the last entry (go_to(desk), ticks 77 to 118): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 18 | not reached | - | - | - |
| confirm_delivered_pallet(pallet_2) | 19 to 38 | not reached | - | - | - |
| confirm_delivered_pallet(pallet_1) | 39 to 57 | not reached | - | - | - |
| confirm_delivered_pallet(pallet_3) | 58 to 76 | not reached | - | - | - |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 16 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0233 | 0.0466 | 341.7 | 321.7 | 20.0 | confirm_delivered_pallet(pallet_0) |
| 27 | office_break(office_chair) | move_to(office_door) | 0.0187 | 0.0417 | 353.0 | 353.0 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 29 | confirm_delivered_pallet(pallet_1) | move_to(pallet_1) | 0.0188 | 0.0396 | 358.1 | 358.1 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 48 | confirm_delivered_pallet(pallet_3) | move_to(pallet_3) | 0.0250 | 0.0389 | 360.0 | 360.0 | 0.0 | confirm_delivered_pallet(pallet_1) |
| 49 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0266 | 0.0405 | 355.9 | 355.9 | 0.0 | confirm_delivered_pallet(pallet_1) |
| 66 | office_break(office_chair) | move_to(office_door) | 0.0306 | 0.0427 | 350.5 | 350.5 | 0.0 | confirm_delivered_pallet(pallet_3) |
| 93 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.1785 | 0.0387 | 360.5 | 360.5 | 0.0 | - |
| 100 | office_break(office_chair) | move_to(office_door) | 0.9202 | 0.0442 | 347.1 | 347.1 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 17 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 18 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 37 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 38 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 56 | adequate | unresolved | confirm_delivered_pallet(pallet_1) |
| 57 | unresolved | adequate | confirm_delivered_pallet(pallet_1) |
| 75 | adequate | unresolved | confirm_delivered_pallet(pallet_3) |
| 76 | unresolved | adequate | confirm_delivered_pallet(pallet_3) |
| 100 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 14, 19 to 36, 58 to 74, 77 to 91 |
| confirm_delivered_pallet(pallet_0) | 0 to 16 |
| confirm_delivered_pallet(pallet_1) | 0 to 16, 39 to 55 |
| confirm_delivered_pallet(pallet_2) | 0 to 16, 19 to 36 |
| confirm_delivered_pallet(pallet_3) | 0 to 16, 19 to 36, 58 to 74 |
| office_break(office_chair) | 0 to 16, 39 to 55, 77 to 114 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 16 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 17 to 18 | coffee_break(coffee_machine_0) | none(below_theta) |
| 19 to 20 | confirm_delivered_pallet(pallet_1) | none(below_theta) |
| 21 to 36 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 37 to 38 | coffee_break(coffee_machine_0) | none(below_theta) |
| 39 to 55 | confirm_delivered_pallet(pallet_1) | none(below_theta) |
| 56 to 57 | coffee_break(coffee_machine_0) | none(below_theta) |
| 58 to 74 | confirm_delivered_pallet(pallet_3) | none(below_theta) |
| 75 to 77 | coffee_break(coffee_machine_0) | none(below_theta) |
| 78 to 91 | office_break(office_chair) | none(below_theta) |
| 92 to 99 | office_break(office_chair) | clears |
| 100 to 148 | office_break(office_chair) | none(leader_inadequate) |

The last entry (go_to(desk)): first step 77, last step 117, acknowledgement 118; the idle human from 119. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.4925 at 77; S < α from 93 (belief 0.1785; v·D 360.5 cm); the finding unexplained from 100.

- office_break(office_chair): belief 0.4925 at 77; S < α from 100 (belief 0.9202; v·D 347.1 cm); the finding unexplained from 100.

