### scenario_s04_12

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 28 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 30 | stand(PT80S) | task_absent | stand | 0 | 1 |
| 71 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 123 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 125 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 141; idle from 142 to 171. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 171 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 25 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 26 to 27 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 120 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 121 to 122 |
| office_break(office_chair) | move_to(office_door) | -1 to 171 |

Events (actual):

| tick | event |
|---|---|
| 28 | boundary |
| 28 | pin confirm_delivered_pallet(pallet_0) |
| 46 | finding turns unexplained |
| 121 | finding turns adequate (from unexplained) |
| 123 | boundary |
| 123 | pin confirm_delivered_pallet(pallet_2) |
| 152 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), office_break(office_chair). At the last entry (go_to(desk), ticks 125 to 141): lifecycle and finding adequate; on the idle ticks after it: adequate, unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 29 | 14 | 0.7579 | yes | adequate |
| confirm_delivered_pallet(pallet_2) | 71 to 124 | 92 | 0.7626 | yes | inadequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 8 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0301 | 0.0431 | 349.6 | 349.6 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 15 | office_break(office_chair) | move_to(office_door) | 0.0406 | 0.0373 | 364.1 | 364.1 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 20 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0538 | 0.0427 | 350.6 | 350.6 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 46 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.3287 | 0.0474 | 340.0 | 0.0 | 340.0 | - |
| 46 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.3287 | 0.0474 | 340.0 | 0.0 | 340.0 | - |
| 46 | office_break(office_chair) | move_to(office_door) | 0.3287 | 0.0474 | 340.0 | 0.0 | 340.0 | - |
| 139 | office_break(office_chair) | move_to(office_door) | 0.0972 | 0.0470 | 340.8 | 340.8 | 0.0 | - |
| 152 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9224 | 0.0490 | 336.4 | 96.4 | 240.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 28 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 29 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 46 | adequate | unexplained | - |
| 121 | unexplained | adequate | confirm_delivered_pallet(pallet_2) |
| 123 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 124 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 152 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 27, 71 to 88, 125 to 171 |
| confirm_delivered_pallet(pallet_0) | 0 to 27 |
| confirm_delivered_pallet(pallet_2) | 71 to 122 |
| office_break(office_chair) | 0 to 10, 71 to 116, 125 to 130 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 13 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 14 to 27 | confirm_delivered_pallet(pallet_0) | clears |
| 28 to 70 | coffee_break(coffee_machine_0) | none(below_theta) |
| 71 to 91 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 92 to 120 | confirm_delivered_pallet(pallet_2) | none(leader_inadequate) |
| 121 to 122 | confirm_delivered_pallet(pallet_2) | clears |
| 123 to 133 | coffee_break(coffee_machine_0) | none(below_theta) |
| 134 to 151 | coffee_break(coffee_machine_0) | clears |
| 152 to 171 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(desk)): first step 125, last step 140, acknowledgement 141; the idle human from 142. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.5102 at 125; S < α from 152 (belief 0.9224; v·D 336.4 cm); the finding unexplained from 152.

- office_break(office_chair): belief 0.4748 at 125; S < α from 139 (belief 0.0972; v·D 340.8 cm); the finding unexplained from 152.

