### scenario_s06_19

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_1) | covered | move_to | 0 | 1 |
| 17 | confirm_delivered_pallet(pallet_1) | covered | scan_it | 0 | 1 |
| 19 | office_break(office_chair) | covered | move_to | 0 | 1 |
| 32 | office_break(office_chair) | covered | move_to | 1 | 1 |
| 40 | office_break(office_chair) | covered | wait_at | 0 | 1 |
| 86 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 92 | confirm_delivered_pallet(pallet_2) | covered | move_to | 1 | 1 |
| 124 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 126 | go_to(standby_place) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 150; idle from 151 to 180. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), confirm_delivered_pallet(pallet_4), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 33 |
| coffee_break(coffee_machine_0) | move_to(office_door) | 34 to 89 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 90 to 180 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 14 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 15 to 19 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 20 to 33 |
| confirm_delivered_pallet(pallet_0) | move_to(office_door) | 34 to 89 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 90 to 180 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 33 |
| confirm_delivered_pallet(pallet_2) | move_to(office_door) | 34 to 89 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 90 to 121 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 122 to 123 |
| office_break(office_chair) | move_to(office_door) | -1 to 29 |
| office_break(office_chair) | move_to(office_chair) | 30 to 37 |
| office_break(office_chair) | wait_at(PT90S,office_chair) | 38 to 83 |
| office_break(office_chair) | move_to(office_chair) | 86 to 93 |
| office_break(office_chair) | move_to(office_door) | 94 to 180 |

Events (actual):

| tick | event |
|---|---|
| 17 | boundary (no pin) |
| 84 | boundary |
| 84 | pin office_break(office_chair) |
| 86 | re-entry office_break(office_chair) |
| 124 | boundary |
| 124 | pin confirm_delivered_pallet(pallet_2) |
| 157 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_4). At the last entry (go_to(standby_place), ticks 126 to 150): lifecycle and finding adequate; on the idle ticks after it: adequate, unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_1) | 0 to 18 | outside the support (at the floor) | - | - | - |
| office_break(office_chair) | 19 to 85 | 27 | 0.7851 | yes | adequate |
| confirm_delivered_pallet(pallet_2) | 86 to 125 | 123 | 0.7770 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 16 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0440 | 0.0466 | 341.7 | 321.7 | 20.0 | confirm_delivered_pallet(pallet_1) |
| 27 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0451 | 0.0420 | 352.1 | 352.1 | 0.0 | office_break(office_chair) |
| 28 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0495 | 0.0433 | 349.2 | 349.2 | 0.0 | office_break(office_chair) |
| 29 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.0473 | 0.0393 | 358.8 | 358.8 | 0.0 | office_break(office_chair) |
| 47 | coffee_break(coffee_machine_0) | move_to(office_door) | 0.0010 | 0.0474 | 340.0 | 160.0 | 180.0 | office_break(office_chair) |
| 47 | confirm_delivered_pallet(pallet_0) | move_to(office_door) | 0.0010 | 0.0474 | 340.0 | 160.0 | 180.0 | office_break(office_chair) |
| 47 | confirm_delivered_pallet(pallet_2) | move_to(office_door) | 0.0010 | 0.0474 | 340.0 | 160.0 | 180.0 | office_break(office_chair) |
| 103 | office_break(office_chair) | move_to(office_door) | 0.0018 | 0.0389 | 360.0 | 360.0 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 114 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.0284 | 0.0361 | 367.6 | 367.6 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 140 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0504 | 0.0368 | 365.6 | 365.6 | 0.0 | - |
| 146 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.1218 | 0.0433 | 349.1 | 349.1 | 0.0 | - |
| 157 | office_break(office_chair) | move_to(office_door) | 0.9147 | 0.0471 | 340.5 | 180.5 | 160.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_1) |
| 17 | adequate | unresolved | confirm_delivered_pallet(pallet_1) |
| 18 | unresolved | adequate | confirm_delivered_pallet(pallet_1) |
| 84 | adequate | unresolved | office_break(office_chair) |
| 85 | unresolved | adequate | office_break(office_chair) |
| 124 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 125 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 157 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 14, 86 to 123, 126 to 134 |
| confirm_delivered_pallet(pallet_0) | 0 to 16, 86 to 123, 126 to 180 |
| confirm_delivered_pallet(pallet_2) | 0 to 16, 86 to 123 |
| confirm_delivered_pallet(pallet_4) | none |
| office_break(office_chair) | 0 to 16, 19 to 83, 126 to 180 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 16 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 17 to 18 | coffee_break(coffee_machine_0) | none(below_theta) |
| 19 to 20 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 21 to 26 | office_break(office_chair) | none(below_theta) |
| 27 to 83 | office_break(office_chair) | clears |
| 84 to 91 | coffee_break(coffee_machine_0) | none(below_theta) |
| 92 to 122 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 123 to 123 | confirm_delivered_pallet(pallet_2) | clears |
| 124 to 125 | coffee_break(coffee_machine_0) | none(below_theta) |
| 126 to 142 | office_break(office_chair) | none(below_theta) |
| 143 to 156 | office_break(office_chair) | clears |
| 157 to 180 | office_break(office_chair) | none(leader_inadequate) |

The last entry (go_to(standby_place)): first step 126, last step 149, acknowledgement 150; the idle human from 151. Live at its first tick: coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.3189 at 126; S < α from 140 (belief 0.0504; v·D 365.6 cm); the finding unexplained from 157.

- confirm_delivered_pallet(pallet_0): belief 0.3315 at 126; S < α from 146 (belief 0.1218; v·D 349.1 cm); the finding unexplained from 157.

- office_break(office_chair): belief 0.3356 at 126; S < α from 157 (belief 0.9147; v·D 340.5 cm); the finding unexplained from 157.

Entries still open at the run's end (the record; a script that depends on the robot):

- confirm_delivered_pallet(?pallet=pallet_4)
- go_to(?landmark=desk)

