### scenario_s04_11

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 14 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 53 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 55 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 107 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 109 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 155; idle from 156 to 185. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 185 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 104 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 105 to 106 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 50 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 51 to 52 |
| office_break(office_chair) | move_to(office_door) | -1 to 185 |

Events (actual):

| tick | event |
|---|---|
| 22 | finding turns unexplained |
| 51 | finding turns adequate (from unexplained) |
| 53 | boundary |
| 53 | pin confirm_delivered_pallet(pallet_2) |
| 107 | boundary |
| 107 | pin confirm_delivered_pallet(pallet_0) |
| 133 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), office_break(office_chair). At the last entry (go_to(desk), ticks 109 to 155): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 13 | not reached | - | - | - |
| confirm_delivered_pallet(pallet_2) | 14 to 54 | 35 | 0.8038 | yes | inadequate |
| confirm_delivered_pallet(pallet_0) | 55 to 108 | 89 | 0.7742 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 8 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0301 | 0.0431 | 349.6 | 349.6 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 18 | office_break(office_chair) | move_to(office_door) | 0.1616 | 0.0472 | 340.4 | 340.4 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 19 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.1923 | 0.0420 | 352.2 | 352.2 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 22 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.4330 | 0.0403 | 356.4 | 356.4 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 88 | office_break(office_chair) | move_to(office_door) | 0.0503 | 0.0494 | 335.7 | 335.7 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 97 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0550 | 0.0434 | 349.0 | 349.0 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 130 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.3247 | 0.0485 | 337.6 | 337.6 | 0.0 | - |
| 133 | office_break(office_chair) | move_to(office_door) | 0.6885 | 0.0487 | 337.1 | 337.1 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 22 | adequate | unexplained | confirm_delivered_pallet(pallet_2) |
| 51 | unexplained | adequate | confirm_delivered_pallet(pallet_2) |
| 53 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 54 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 107 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 108 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 133 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 23, 55 to 106, 109 to 139 |
| confirm_delivered_pallet(pallet_0) | 0 to 27, 55 to 106 |
| confirm_delivered_pallet(pallet_2) | 27 to 52 |
| office_break(office_chair) | 0 to 10, 15 to 34, 55 to 106, 109 to 147 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 23 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 24 to 29 | office_break(office_chair) | none(below_theta) |
| 30 to 34 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 35 to 50 | confirm_delivered_pallet(pallet_2) | none(leader_inadequate) |
| 51 to 52 | confirm_delivered_pallet(pallet_2) | clears |
| 53 to 54 | coffee_break(coffee_machine_0) | none(below_theta) |
| 55 to 88 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 89 to 106 | confirm_delivered_pallet(pallet_0) | clears |
| 107 to 108 | coffee_break(coffee_machine_0) | none(below_theta) |
| 109 to 147 | office_break(office_chair) | none(below_theta) |
| 148 to 185 | office_break(office_chair) | none(leader_inadequate) |

The last entry (go_to(desk)): first step 109, last step 154, acknowledgement 155; the idle human from 156. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.4906 at 109; S < α from 130 (belief 0.3247; v·D 337.6 cm); the finding unexplained from 133.

- office_break(office_chair): belief 0.4944 at 109; S < α from 133 (belief 0.6885; v·D 337.1 cm); the finding unexplained from 133.

