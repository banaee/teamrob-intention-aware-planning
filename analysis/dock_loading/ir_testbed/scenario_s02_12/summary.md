### scenario_s02_12

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 28 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 30 | stand(PT80S) | task_absent | stand | 0 | 1 |
| 71 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 122 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 124 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 149; idle from 150 to 179. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 179 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 25 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 26 to 27 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 119 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 120 to 121 |
| office_break(office_chair) | move_to(office_door) | -1 to 179 |

Events (actual):

| tick | event |
|---|---|
| 28 | boundary |
| 28 | pin confirm_delivered_pallet(pallet_0) |
| 46 | finding turns unexplained |
| 120 | finding turns adequate (from unexplained) |
| 122 | boundary |
| 122 | pin confirm_delivered_pallet(pallet_2) |
| 140 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), office_break(office_chair). At the last entry (go_to(desk), ticks 124 to 149): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 29 | 10 | 0.7745 | yes | adequate |
| confirm_delivered_pallet(pallet_2) | 71 to 123 | 117 | 0.7500 | yes | inadequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 8 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0409 | 0.0445 | 346.4 | 346.4 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 9 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0406 | 0.0409 | 355.0 | 355.0 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 15 | office_break(office_chair) | move_to(office_door) | 0.0475 | 0.0373 | 364.1 | 364.1 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 46 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.3287 | 0.0474 | 340.0 | 0.0 | 340.0 | - |
| 46 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.3287 | 0.0474 | 340.0 | 0.0 | 340.0 | - |
| 46 | office_break(office_chair) | move_to(office_door) | 0.3287 | 0.0474 | 340.0 | 0.0 | 340.0 | - |
| 139 | office_break(office_chair) | move_to(office_door) | 0.3943 | 0.0447 | 345.9 | 345.9 | 0.0 | - |
| 140 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.5680 | 0.0464 | 342.0 | 342.0 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 28 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 29 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 46 | adequate | unexplained | - |
| 120 | unexplained | adequate | confirm_delivered_pallet(pallet_2) |
| 122 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 123 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 140 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 71 to 121, 124 to 139 |
| confirm_delivered_pallet(pallet_0) | 0 to 27 |
| confirm_delivered_pallet(pallet_2) | 71 to 121 |
| office_break(office_chair) | 0 to 10, 71 to 119, 124 to 134 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 9 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 10 to 27 | confirm_delivered_pallet(pallet_0) | clears |
| 28 to 70 | coffee_break(coffee_machine_0) | none(below_theta) |
| 71 to 116 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 117 to 119 | confirm_delivered_pallet(pallet_2) | none(leader_inadequate) |
| 120 to 121 | confirm_delivered_pallet(pallet_2) | clears |
| 122 to 143 | coffee_break(coffee_machine_0) | none(below_theta) |
| 144 to 179 | office_break(office_chair) | none(below_theta) |

The last entry (go_to(desk)): first step 124, last step 148, acknowledgement 149; the idle human from 150. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.5103 at 124; S < α from 140 (belief 0.5680; v·D 342.0 cm); the finding unexplained from 140.

- office_break(office_chair): belief 0.4747 at 124; S < α from 139 (belief 0.3943; v·D 345.9 cm); the finding unexplained from 140.

