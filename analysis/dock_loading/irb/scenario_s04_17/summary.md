### scenario_s04_17

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 14 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 1 |
| 32 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 1 |
| 63 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 109 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 111 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 162 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 164 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 209; idle from 210 to 239. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 29 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 30 to 60 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 63 to 239 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 159 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 160 to 161 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 106 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 107 to 108 |
| office_break(office_chair) | move_to(office_door) | -1 to 239 |

Events (actual):

| tick | event |
|---|---|
| 61 | boundary |
| 61 | pin coffee_break(coffee_machine_0) |
| 63 | re-entry coffee_break(coffee_machine_0) |
| 109 | boundary |
| 109 | pin confirm_delivered_pallet(pallet_2) |
| 162 | boundary |
| 162 | pin confirm_delivered_pallet(pallet_0) |
| 188 | finding turns unexplained |

Never pinned: office_break(office_chair). At the last entry (go_to(desk), ticks 164 to 209): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 13 | not reached | - | - | - |
| coffee_break(coffee_machine_0) | 14 to 62 | 25 | 0.7777 | yes | adequate |
| confirm_delivered_pallet(pallet_2) | 63 to 110 | 82 | 0.7621 | yes | adequate |
| confirm_delivered_pallet(pallet_0) | 111 to 163 | 144 | 0.7538 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 8 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0301 | 0.0431 | 349.6 | 349.6 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 14 | office_break(office_chair) | move_to(office_door) | 0.0517 | 0.0477 | 339.4 | 339.4 | 0.0 | coffee_break(coffee_machine_0) |
| 26 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.1580 | 0.0380 | 362.3 | 362.3 | 0.0 | coffee_break(coffee_machine_0) |
| 72 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0278 | 0.0408 | 355.1 | 355.1 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 75 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.0364 | 0.0448 | 345.7 | 345.7 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 91 | office_break(office_chair) | move_to(office_door) | 0.0509 | 0.0398 | 357.6 | 357.6 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 144 | office_break(office_chair) | move_to(office_door) | 0.0478 | 0.0465 | 341.9 | 341.9 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 152 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0625 | 0.0499 | 334.8 | 334.8 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 185 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.3237 | 0.0421 | 352.0 | 352.0 | 0.0 | - |
| 188 | office_break(office_chair) | move_to(office_door) | 0.6864 | 0.0411 | 354.3 | 354.3 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 61 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 62 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 109 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 110 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 162 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 163 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 188 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 60, 111 to 161, 164 to 193 |
| confirm_delivered_pallet(pallet_0) | 0 to 60, 111 to 161 |
| confirm_delivered_pallet(pallet_2) | 63 to 108 |
| office_break(office_chair) | 0 to 10, 63 to 108, 111 to 161, 164 to 200 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 20 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 21 to 24 | coffee_break(coffee_machine_0) | none(below_theta) |
| 25 to 60 | coffee_break(coffee_machine_0) | clears |
| 61 to 62 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 63 to 81 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 82 to 108 | confirm_delivered_pallet(pallet_2) | clears |
| 109 to 110 | coffee_break(coffee_machine_0) | none(below_theta) |
| 111 to 143 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 144 to 161 | confirm_delivered_pallet(pallet_0) | clears |
| 162 to 163 | coffee_break(coffee_machine_0) | none(below_theta) |
| 164 to 239 | office_break(office_chair) | none(below_theta) |

The last entry (go_to(desk)): first step 164, last step 208, acknowledgement 209; the idle human from 210. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.4904 at 164; S < α from 185 (belief 0.3237; v·D 352.0 cm); the finding unexplained from 188.

- office_break(office_chair): belief 0.4946 at 164; S < α from 188 (belief 0.6864; v·D 354.3 cm); the finding unexplained from 188.

