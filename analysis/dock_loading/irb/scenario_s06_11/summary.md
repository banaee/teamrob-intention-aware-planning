### scenario_s06_11

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 14 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 33 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 35 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 53 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 55 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 91; idle from 92 to 121. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 121 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 50 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 51 to 52 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 30 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 31 to 32 |
| office_break(office_chair) | move_to(office_door) | -1 to 121 |

Events (actual):

| tick | event |
|---|---|
| 33 | boundary |
| 33 | pin confirm_delivered_pallet(pallet_2) |
| 53 | boundary |
| 53 | pin confirm_delivered_pallet(pallet_0) |
| 71 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), office_break(office_chair). At the last entry (go_to(desk), ticks 55 to 91): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 13 | not reached | - | - | - |
| confirm_delivered_pallet(pallet_2) | 14 to 34 | 24 | 0.7600 | yes | adequate |
| confirm_delivered_pallet(pallet_0) | 35 to 54 | not reached | - | - | - |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 16 | office_break(office_chair) | move_to(office_door) | 0.0495 | 0.0451 | 344.9 | 344.9 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 23 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.1121 | 0.0472 | 340.3 | 340.3 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 26 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.1283 | 0.0479 | 339.0 | 339.0 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 45 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0285 | 0.0428 | 350.2 | 350.2 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 70 | office_break(office_chair) | move_to(office_door) | 0.4245 | 0.0478 | 339.0 | 339.0 | 0.0 | - |
| 71 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.5738 | 0.0488 | 337.0 | 337.0 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 33 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 34 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 53 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 54 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 71 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 32, 55 to 71 |
| confirm_delivered_pallet(pallet_0) | 0 to 30, 35 to 52 |
| confirm_delivered_pallet(pallet_2) | 0 to 32 |
| office_break(office_chair) | 0 to 15, 35 to 52, 55 to 68 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 17 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 18 to 23 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 24 to 32 | confirm_delivered_pallet(pallet_2) | clears |
| 33 to 34 | coffee_break(coffee_machine_0) | none(below_theta) |
| 35 to 52 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 53 to 54 | coffee_break(coffee_machine_0) | none(below_theta) |
| 55 to 63 | office_break(office_chair) | none(below_theta) |
| 64 to 121 | coffee_break(coffee_machine_0) | none(below_theta) |

The last entry (go_to(desk)): first step 55, last step 90, acknowledgement 91; the idle human from 92. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.4892 at 55; S < α from 71 (belief 0.5738; v·D 337.0 cm); the finding unexplained from 71.

- office_break(office_chair): belief 0.4958 at 55; S < α from 70 (belief 0.4245; v·D 339.0 cm); the finding unexplained from 71.

