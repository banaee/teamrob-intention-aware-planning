### scenario_s02_11

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 14 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 53 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 55 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 105 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 107 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 152; idle from 153 to 182. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 182 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 102 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 103 to 104 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 50 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 51 to 52 |
| office_break(office_chair) | move_to(office_door) | -1 to 182 |

Events (actual):

| tick | event |
|---|---|
| 22 | finding turns unexplained |
| 51 | finding turns adequate (from unexplained) |
| 53 | boundary |
| 53 | pin confirm_delivered_pallet(pallet_2) |
| 105 | boundary |
| 105 | pin confirm_delivered_pallet(pallet_0) |
| 156 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), office_break(office_chair). At the last entry (go_to(desk), ticks 107 to 152): lifecycle and finding adequate; on the idle ticks after it: adequate, unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 13 | 10 | 0.7745 | yes | adequate |
| confirm_delivered_pallet(pallet_2) | 14 to 54 | 45 | 0.7562 | yes | inadequate |
| confirm_delivered_pallet(pallet_0) | 55 to 106 | 83 | 0.7944 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 8 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0409 | 0.0445 | 346.4 | 346.4 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 9 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0406 | 0.0409 | 355.0 | 355.0 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 21 | office_break(office_chair) | move_to(office_door) | 0.3685 | 0.0486 | 337.3 | 337.3 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 22 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.4227 | 0.0453 | 344.6 | 344.6 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 66 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0241 | 0.0360 | 367.7 | 367.7 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 87 | office_break(office_chair) | move_to(office_door) | 0.0574 | 0.0454 | 344.4 | 344.4 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 131 | office_break(office_chair) | move_to(office_door) | 0.0715 | 0.0406 | 355.6 | 355.6 | 0.0 | - |
| 156 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9840 | 0.0433 | 349.2 | 249.2 | 100.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 22 | adequate | unexplained | confirm_delivered_pallet(pallet_2) |
| 51 | unexplained | adequate | confirm_delivered_pallet(pallet_2) |
| 53 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 54 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 105 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 106 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 156 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 27 to 52, 107 to 182 |
| confirm_delivered_pallet(pallet_0) | 0 to 28, 55 to 104 |
| confirm_delivered_pallet(pallet_2) | 25 to 52 |
| office_break(office_chair) | 0 to 10, 15 to 39, 55 to 104, 107 to 143 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 9 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 10 to 17 | confirm_delivered_pallet(pallet_0) | clears |
| 18 to 22 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 23 to 30 | office_break(office_chair) | none(below_theta) |
| 31 to 44 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 45 to 50 | confirm_delivered_pallet(pallet_2) | none(leader_inadequate) |
| 51 to 52 | confirm_delivered_pallet(pallet_2) | clears |
| 53 to 54 | coffee_break(coffee_machine_0) | none(below_theta) |
| 55 to 82 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 83 to 104 | confirm_delivered_pallet(pallet_0) | clears |
| 105 to 123 | coffee_break(coffee_machine_0) | none(below_theta) |
| 124 to 155 | coffee_break(coffee_machine_0) | clears |
| 156 to 182 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(desk)): first step 107, last step 151, acknowledgement 152; the idle human from 153. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.4973 at 107; S < α from 156 (belief 0.9840; v·D 349.2 cm); the finding unexplained from 156.

- office_break(office_chair): belief 0.4877 at 107; S < α from 131 (belief 0.0715; v·D 355.6 cm); the finding unexplained from 156.

