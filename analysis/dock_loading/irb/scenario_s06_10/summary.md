### scenario_s06_10

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 14 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 33 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 35 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 76; idle from 77 to 106. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 106 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 106 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 30 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 31 to 32 |
| office_break(office_chair) | move_to(office_door) | -1 to 106 |

Events (actual):

| tick | event |
|---|---|
| 33 | boundary |
| 33 | pin confirm_delivered_pallet(pallet_2) |
| 58 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), office_break(office_chair). At the last entry (go_to(desk), ticks 35 to 76): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 13 | not reached | - | - | - |
| confirm_delivered_pallet(pallet_2) | 14 to 34 | 24 | 0.7600 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 16 | office_break(office_chair) | move_to(office_door) | 0.0495 | 0.0451 | 344.9 | 344.9 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 23 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.1121 | 0.0472 | 340.3 | 340.3 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 26 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.1283 | 0.0479 | 339.0 | 339.0 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 51 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.1450 | 0.0399 | 357.4 | 357.4 | 0.0 | - |
| 51 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.1797 | 0.0496 | 335.2 | 335.2 | 0.0 | - |
| 58 | office_break(office_chair) | move_to(office_door) | 0.8361 | 0.0478 | 339.1 | 339.1 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 33 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 34 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 58 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 32, 35 to 49 |
| confirm_delivered_pallet(pallet_0) | 0 to 30, 35 to 51 |
| confirm_delivered_pallet(pallet_2) | 0 to 32 |
| office_break(office_chair) | 0 to 15, 35 to 73 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 17 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 18 to 23 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 24 to 32 | confirm_delivered_pallet(pallet_2) | clears |
| 33 to 36 | coffee_break(coffee_machine_0) | none(below_theta) |
| 37 to 53 | office_break(office_chair) | none(below_theta) |
| 54 to 57 | office_break(office_chair) | clears |
| 58 to 106 | office_break(office_chair) | none(leader_inadequate) |

The last entry (go_to(desk)): first step 35, last step 75, acknowledgement 76; the idle human from 77. Live at its first tick: coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.3311 at 35; S < α from 51 (belief 0.1450; v·D 357.4 cm); the finding unexplained from 58.

- confirm_delivered_pallet(pallet_0): belief 0.3245 at 35; S < α from 51 (belief 0.1797; v·D 335.2 cm); the finding unexplained from 58.

- office_break(office_chair): belief 0.3303 at 35; S < α from 58 (belief 0.8361; v·D 339.1 cm); the finding unexplained from 58.

