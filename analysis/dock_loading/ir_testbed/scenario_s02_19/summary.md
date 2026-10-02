### scenario_s02_19

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_1) | covered | move_to | 0 | 1 |
| 28 | confirm_delivered_pallet(pallet_1) | covered | scan_it | 0 | 1 |
| 30 | office_break(office_chair) | covered | move_to | 0 | 1 |
| 55 | office_break(office_chair) | covered | move_to | 1 | 1 |
| 64 | office_break(office_chair) | covered | wait_at | 0 | 1 |
| 110 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 117 | confirm_delivered_pallet(pallet_2) | covered | move_to | 1 | 1 |
| 143 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 145 | go_to(standby_place) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 171; idle from 172 to 201. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), confirm_delivered_pallet(pallet_4), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 56 |
| coffee_break(coffee_machine_0) | move_to(office_door) | 57 to 114 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 115 to 116 |
| coffee_break(coffee_machine_0) | move_to(office_door) | 117 to 117 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 118 to 201 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 25 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 26 to 29 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 30 to 56 |
| confirm_delivered_pallet(pallet_0) | move_to(office_door) | 57 to 114 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 115 to 116 |
| confirm_delivered_pallet(pallet_0) | move_to(office_door) | 117 to 117 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 118 to 201 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 56 |
| confirm_delivered_pallet(pallet_2) | move_to(office_door) | 57 to 114 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 115 to 116 |
| confirm_delivered_pallet(pallet_2) | move_to(office_door) | 117 to 117 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 118 to 140 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 141 to 142 |
| office_break(office_chair) | move_to(office_door) | -1 to 52 |
| office_break(office_chair) | move_to(office_chair) | 53 to 61 |
| office_break(office_chair) | wait_at(PT90S,office_chair) | 62 to 107 |
| office_break(office_chair) | move_to(office_chair) | 110 to 117 |
| office_break(office_chair) | move_to(office_door) | 118 to 201 |

Events (actual):

| tick | event |
|---|---|
| 28 | boundary (no pin) |
| 108 | boundary |
| 108 | pin office_break(office_chair) |
| 110 | re-entry office_break(office_chair) |
| 143 | boundary |
| 143 | pin confirm_delivered_pallet(pallet_2) |
| 183 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_4). At the last entry (go_to(standby_place), ticks 145 to 171): lifecycle and finding adequate; on the idle ticks after it: adequate, unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_1) | 0 to 29 | outside the support (at the floor) | - | - | - |
| office_break(office_chair) | 30 to 109 | 63 | 0.7792 | yes | adequate |
| confirm_delivered_pallet(pallet_2) | 110 to 144 | not reached | - | - | - |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 8 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0409 | 0.0445 | 346.4 | 346.4 | 0.0 | confirm_delivered_pallet(pallet_1) |
| 9 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0406 | 0.0409 | 355.0 | 355.0 | 0.0 | confirm_delivered_pallet(pallet_1) |
| 15 | office_break(office_chair) | move_to(office_door) | 0.0475 | 0.0373 | 364.1 | 364.1 | 0.0 | confirm_delivered_pallet(pallet_1) |
| 39 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.0180 | 0.0393 | 358.9 | 358.9 | 0.0 | office_break(office_chair) |
| 69 | coffee_break(coffee_machine_0) | move_to(office_door) | 0.0320 | 0.0476 | 339.6 | 199.6 | 140.0 | office_break(office_chair) |
| 69 | confirm_delivered_pallet(pallet_0) | move_to(office_door) | 0.0010 | 0.0476 | 339.6 | 199.6 | 140.0 | office_break(office_chair) |
| 69 | confirm_delivered_pallet(pallet_2) | move_to(office_door) | 0.0461 | 0.0476 | 339.6 | 199.6 | 140.0 | office_break(office_chair) |
| 127 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.0231 | 0.0418 | 352.7 | 352.7 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 127 | office_break(office_chair) | move_to(office_door) | 0.0060 | 0.0391 | 359.5 | 359.5 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 158 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0341 | 0.0382 | 361.8 | 361.8 | 0.0 | - |
| 172 | office_break(office_chair) | move_to(office_door) | 0.1217 | 0.0481 | 338.3 | 298.3 | 40.0 | - |
| 183 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.8833 | 0.0477 | 339.2 | 79.2 | 260.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_1) |
| 28 | adequate | unresolved | confirm_delivered_pallet(pallet_1) |
| 29 | unresolved | adequate | confirm_delivered_pallet(pallet_1) |
| 108 | adequate | unresolved | office_break(office_chair) |
| 109 | unresolved | adequate | office_break(office_chair) |
| 118 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 119 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 143 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 144 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 183 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 30 to 56, 110 to 116, 119 to 142, 145 to 151 |
| confirm_delivered_pallet(pallet_0) | 0 to 27, 110 to 116, 145 to 201 |
| confirm_delivered_pallet(pallet_2) | 30 to 56, 110 to 116, 119 to 142 |
| confirm_delivered_pallet(pallet_4) | none |
| office_break(office_chair) | 0 to 10, 30 to 107, 145 to 201 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 9 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 10 to 27 | confirm_delivered_pallet(pallet_0) | clears |
| 28 to 29 | coffee_break(coffee_machine_0) | none(below_theta) |
| 30 to 30 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 31 to 62 | office_break(office_chair) | none(below_theta) |
| 63 to 107 | office_break(office_chair) | clears |
| 108 to 116 | coffee_break(coffee_machine_0) | none(below_theta) |
| 117 to 142 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 143 to 144 | coffee_break(coffee_machine_0) | none(below_theta) |
| 145 to 166 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 167 to 182 | confirm_delivered_pallet(pallet_0) | clears |
| 183 to 201 | confirm_delivered_pallet(pallet_0) | none(leader_inadequate) |

The last entry (go_to(standby_place)): first step 145, last step 170, acknowledgement 171; the idle human from 172. Live at its first tick: coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.3167 at 145; S < α from 158 (belief 0.0341; v·D 361.8 cm); the finding unexplained from 183.

- confirm_delivered_pallet(pallet_0): belief 0.3360 at 145; S < α from 183 (belief 0.8833; v·D 339.2 cm); the finding unexplained from 183.

- office_break(office_chair): belief 0.3333 at 145; S < α from 172 (belief 0.1217; v·D 338.3 cm); the finding unexplained from 183.

Entries still open at the run's end (the record; a script that depends on the robot):

- confirm_delivered_pallet(?pallet=pallet_4)
- go_to(?landmark=desk)

