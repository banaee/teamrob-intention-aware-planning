### scenario_s04_18

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 28 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 30 | stand(PT80S) | task_absent | stand | 0 | 1 |
| 71 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 85 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 2 |
| 106 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 2 |
| 137 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 184 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 185 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 187 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 202; idle from 203 to 232. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 103 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 104 to 134 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 137 to 232 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 25 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 26 to 27 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 181 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 182 to 184 |
| office_break(office_chair) | move_to(office_door) | -1 to 232 |

Events (actual):

| tick | event |
|---|---|
| 28 | boundary |
| 28 | pin confirm_delivered_pallet(pallet_0) |
| 46 | finding turns unexplained |
| 104 | finding turns adequate (from unexplained) |
| 135 | boundary |
| 135 | pin coffee_break(coffee_machine_0) |
| 137 | re-entry coffee_break(coffee_machine_0) |
| 185 | boundary |
| 185 | pin confirm_delivered_pallet(pallet_2) |
| 214 | finding turns unexplained |

Never pinned: office_break(office_chair). At the last entry (go_to(desk), ticks 187 to 202): lifecycle and finding adequate; on the idle ticks after it: adequate, unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 29 | 14 | 0.7579 | yes | adequate |
| confirm_delivered_pallet(pallet_2) | 71 to 84 | not reached | - | - | - |
| coffee_break(coffee_machine_0) | 85 to 136 | 98 | 0.7630 | yes | inadequate |
| confirm_delivered_pallet(pallet_2) | 137 to 186 | 156 | 0.7622 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 8 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0301 | 0.0431 | 349.6 | 349.6 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 15 | office_break(office_chair) | move_to(office_door) | 0.0406 | 0.0373 | 364.1 | 364.1 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 20 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0538 | 0.0427 | 350.6 | 350.6 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 46 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.3287 | 0.0474 | 340.0 | 0.0 | 340.0 | - |
| 46 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.3287 | 0.0474 | 340.0 | 0.0 | 340.0 | - |
| 46 | office_break(office_chair) | move_to(office_door) | 0.3287 | 0.0474 | 340.0 | 0.0 | 340.0 | - |
| 146 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0305 | 0.0401 | 356.9 | 356.9 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 165 | office_break(office_chair) | move_to(office_door) | 0.0529 | 0.0416 | 353.3 | 353.3 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 201 | office_break(office_chair) | move_to(office_door) | 0.0993 | 0.0491 | 336.3 | 336.3 | 0.0 | - |
| 214 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9089 | 0.0449 | 345.3 | 85.3 | 260.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 28 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 29 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 46 | adequate | unexplained | - |
| 104 | unexplained | adequate | coffee_break(coffee_machine_0) |
| 135 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 136 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 185 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 186 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 214 | adequate | unexplained | - |

Across the started task coffee_break(coffee_machine_0) (covered; actual): on top of the stack from 85 to 136, its hypothesis pinned at 135; the suspended task resumes at 137.

| tick | human action | truth | coffee_break(coffee_machine_0) belief / S | confirm_delivered_pallet(pallet_0) belief / S | confirm_delivered_pallet(pallet_2) belief / S | office_break(office_chair) belief / S | finding |
|---|---|---|---|---|---|---|---|
| 83 | move_to step | confirm_delivered_pallet(pallet_2) | 0.0565 / 0.0000 | retired | 0.5484 / 0.0004 | 0.3811 / 0.0003 | unexplained |
| 84 | move_to step | confirm_delivered_pallet(pallet_2) | 0.0459 / 0.0000 | retired | 0.5671 / 0.0004 | 0.3729 / 0.0003 | unexplained |
| 85 | move_to step | coffee_break(coffee_machine_0) | 0.0607 / 0.0000 | retired | 0.5853 / 0.0003 | 0.3400 / 0.0002 | unexplained |
| 86 | move_to step | coffee_break(coffee_machine_0) | 0.0800 / 0.0000 | retired | 0.5985 / 0.0002 | 0.3076 / 0.0001 | unexplained |
| 87 | move_to step | coffee_break(coffee_machine_0) | 0.1047 / 0.0000 | retired | 0.6055 / 0.0002 | 0.2758 / 0.0001 | unexplained |
| 134 | wait_at stand | coffee_break(coffee_machine_0) | 0.9840 / 1.0000 | retired | 0.0010 / 0.0000 | 0.0010 / 0.0000 | adequate |
| 135 | wait_at stand | coffee_break(coffee_machine_0) | retired | retired | 0.4925 / - | 0.4925 / - | unresolved |
| 136 | wait_at  | coffee_break(coffee_machine_0) | retired | retired | 0.4925 / 1.0000 | 0.4925 / 1.0000 | adequate |
| 137 | move_to step | confirm_delivered_pallet(pallet_2) | 0.3287 / - | retired | 0.3326 / 1.0000 | 0.3248 / 0.9666 | adequate |
| 138 | move_to step | confirm_delivered_pallet(pallet_2) | 0.2866 / 0.7480 | retired | 0.3583 / 1.0000 | 0.3411 / 0.9322 | adequate |
| 139 | move_to step | confirm_delivered_pallet(pallet_2) | 0.2405 / 0.5444 | retired | 0.3871 / 1.0000 | 0.3584 / 0.8967 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 27, 71 to 134, 187 to 232 |
| confirm_delivered_pallet(pallet_0) | 0 to 27 |
| confirm_delivered_pallet(pallet_2) | 71 to 134, 137 to 184 |
| office_break(office_chair) | 0 to 10, 71 to 96, 137 to 184, 187 to 193 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 13 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 14 to 27 | confirm_delivered_pallet(pallet_0) | clears |
| 28 to 70 | coffee_break(coffee_machine_0) | none(below_theta) |
| 71 to 93 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 94 to 97 | coffee_break(coffee_machine_0) | none(below_theta) |
| 98 to 103 | coffee_break(coffee_machine_0) | none(leader_inadequate) |
| 104 to 134 | coffee_break(coffee_machine_0) | clears |
| 135 to 155 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 156 to 184 | confirm_delivered_pallet(pallet_2) | clears |
| 185 to 195 | coffee_break(coffee_machine_0) | none(below_theta) |
| 196 to 213 | coffee_break(coffee_machine_0) | clears |
| 214 to 232 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(desk)): first step 187, last step 201, acknowledgement 202; the idle human from 203. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.5101 at 187; S < α from 214 (belief 0.9089; v·D 345.3 cm); the finding unexplained from 214.

- office_break(office_chair): belief 0.4749 at 187; S < α from 201 (belief 0.0993; v·D 336.3 cm); the finding unexplained from 214.

