### scenario_s04_07

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 28 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 30 | office_break(office_chair) | covered | move_to | 0 | 1 |
| 55 | office_break(office_chair) | covered | move_to | 1 | 1 |
| 64 | office_break(office_chair) | covered | wait_at | 0 | 1 |
| 110 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 117 | confirm_delivered_pallet(pallet_2) | covered | move_to | 1 | 1 |
| 146 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 148 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 164; idle from 165 to 194. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 56 |
| coffee_break(coffee_machine_0) | move_to(office_door) | 57 to 114 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 115 to 194 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 25 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 26 to 27 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 56 |
| confirm_delivered_pallet(pallet_2) | move_to(office_door) | 57 to 114 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 115 to 143 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 144 to 145 |
| office_break(office_chair) | move_to(office_door) | -1 to 52 |
| office_break(office_chair) | move_to(office_chair) | 53 to 61 |
| office_break(office_chair) | wait_at(PT90S,office_chair) | 62 to 107 |
| office_break(office_chair) | move_to(office_chair) | 110 to 117 |
| office_break(office_chair) | move_to(office_door) | 118 to 194 |

Events (actual):

| tick | event |
|---|---|
| 28 | boundary |
| 28 | pin confirm_delivered_pallet(pallet_0) |
| 108 | boundary |
| 108 | pin office_break(office_chair) |
| 110 | re-entry office_break(office_chair) |
| 146 | boundary |
| 146 | pin confirm_delivered_pallet(pallet_2) |
| 175 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(desk), ticks 148 to 164): lifecycle and finding adequate; on the idle ticks after it: adequate, unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 29 | 14 | 0.7579 | yes | adequate |
| office_break(office_chair) | 30 to 109 | 60 | 0.7970 | yes | adequate |
| confirm_delivered_pallet(pallet_2) | 110 to 147 | 124 | 0.7730 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 8 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0301 | 0.0431 | 349.6 | 349.6 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 15 | office_break(office_chair) | move_to(office_door) | 0.0406 | 0.0373 | 364.1 | 364.1 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 20 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0538 | 0.0427 | 350.6 | 350.6 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 43 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0298 | 0.0425 | 351.0 | 351.0 | 0.0 | office_break(office_chair) |
| 69 | coffee_break(coffee_machine_0) | move_to(office_door) | 0.0010 | 0.0476 | 339.6 | 199.6 | 140.0 | office_break(office_chair) |
| 69 | confirm_delivered_pallet(pallet_2) | move_to(office_door) | 0.0314 | 0.0476 | 339.6 | 199.6 | 140.0 | office_break(office_chair) |
| 127 | office_break(office_chair) | move_to(office_door) | 0.0076 | 0.0393 | 358.8 | 358.8 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 130 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0483 | 0.0377 | 363.0 | 363.0 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 162 | office_break(office_chair) | move_to(office_door) | 0.0920 | 0.0418 | 352.8 | 352.8 | 0.0 | - |
| 175 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9250 | 0.0452 | 344.7 | 104.7 | 240.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 28 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 29 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 108 | adequate | unresolved | office_break(office_chair) |
| 109 | unresolved | adequate | office_break(office_chair) |
| 146 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 147 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 175 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 27, 30 to 30, 110 to 145, 148 to 194 |
| confirm_delivered_pallet(pallet_0) | 0 to 27 |
| confirm_delivered_pallet(pallet_2) | 30 to 56, 110 to 145 |
| office_break(office_chair) | 0 to 10, 30 to 107, 148 to 151 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 13 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 14 to 27 | confirm_delivered_pallet(pallet_0) | clears |
| 28 to 29 | coffee_break(coffee_machine_0) | none(below_theta) |
| 30 to 59 | office_break(office_chair) | none(below_theta) |
| 60 to 107 | office_break(office_chair) | clears |
| 108 to 116 | coffee_break(coffee_machine_0) | none(below_theta) |
| 117 to 123 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 124 to 145 | confirm_delivered_pallet(pallet_2) | clears |
| 146 to 156 | coffee_break(coffee_machine_0) | none(below_theta) |
| 157 to 174 | coffee_break(coffee_machine_0) | clears |
| 175 to 194 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(desk)): first step 148, last step 163, acknowledgement 164; the idle human from 165. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.5107 at 148; S < α from 175 (belief 0.9250; v·D 344.7 cm); the finding unexplained from 175.

- office_break(office_chair): belief 0.4743 at 148; S < α from 162 (belief 0.0920; v·D 352.8 cm); the finding unexplained from 175.

