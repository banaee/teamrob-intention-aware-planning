### scenario_s02_18

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 28 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 30 | stand(PT80S) | task_absent | stand | 0 | 1 |
| 71 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 85 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 2 |
| 122 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 2 |
| 153 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 162 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 163 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 165 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 189; idle from 190 to 219. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 119 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 120 to 150 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 153 to 219 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 25 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 26 to 27 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 159 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 160 to 162 |
| office_break(office_chair) | move_to(office_door) | -1 to 219 |

Events (actual):

| tick | event |
|---|---|
| 28 | boundary |
| 28 | pin confirm_delivered_pallet(pallet_0) |
| 46 | finding turns unexplained |
| 120 | finding turns adequate (from unexplained) |
| 151 | boundary |
| 151 | pin coffee_break(coffee_machine_0) |
| 153 | re-entry coffee_break(coffee_machine_0) |
| 163 | boundary |
| 163 | pin confirm_delivered_pallet(pallet_2) |
| 180 | finding turns unexplained |

Never pinned: office_break(office_chair). At the last entry (go_to(desk), ticks 165 to 189): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 29 | 10 | 0.7745 | yes | adequate |
| confirm_delivered_pallet(pallet_2) | 71 to 84 | not reached | - | - | - |
| coffee_break(coffee_machine_0) | 85 to 152 | 118 | 0.7652 | yes | inadequate |
| confirm_delivered_pallet(pallet_2) | 153 to 164 | not reached | - | - | - |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 8 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0409 | 0.0445 | 346.4 | 346.4 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 9 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0406 | 0.0409 | 355.0 | 355.0 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 15 | office_break(office_chair) | move_to(office_door) | 0.0475 | 0.0373 | 364.1 | 364.1 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 46 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.3287 | 0.0474 | 340.0 | 0.0 | 340.0 | - |
| 46 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.3287 | 0.0474 | 340.0 | 0.0 | 340.0 | - |
| 46 | office_break(office_chair) | move_to(office_door) | 0.3287 | 0.0474 | 340.0 | 0.0 | 340.0 | - |
| 180 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.5092 | 0.0484 | 337.8 | 337.8 | 0.0 | - |
| 180 | office_break(office_chair) | move_to(office_door) | 0.4758 | 0.0452 | 344.8 | 344.8 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 28 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 29 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 46 | adequate | unexplained | - |
| 120 | unexplained | adequate | coffee_break(coffee_machine_0) |
| 151 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 152 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 163 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 164 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 180 | adequate | unexplained | - |

Across the started task coffee_break(coffee_machine_0) (covered; actual): on top of the stack from 85 to 152, its hypothesis pinned at 151; the suspended task resumes at 153.

| tick | human action | truth | coffee_break(coffee_machine_0) belief / S | confirm_delivered_pallet(pallet_0) belief / S | confirm_delivered_pallet(pallet_2) belief / S | office_break(office_chair) belief / S | finding |
|---|---|---|---|---|---|---|---|
| 83 | move_to step | confirm_delivered_pallet(pallet_2) | 0.3247 / 0.0004 | retired | 0.3440 / 0.0004 | 0.3173 / 0.0004 | unexplained |
| 84 | move_to step | confirm_delivered_pallet(pallet_2) | 0.3248 / 0.0004 | retired | 0.3462 / 0.0004 | 0.3150 / 0.0004 | unexplained |
| 85 | move_to step | coffee_break(coffee_machine_0) | 0.3299 / 0.0004 | retired | 0.3494 / 0.0004 | 0.3068 / 0.0003 | unexplained |
| 86 | move_to step | coffee_break(coffee_machine_0) | 0.3357 / 0.0004 | retired | 0.3532 / 0.0004 | 0.2971 / 0.0003 | unexplained |
| 87 | move_to step | coffee_break(coffee_machine_0) | 0.3425 / 0.0004 | retired | 0.3577 / 0.0004 | 0.2858 / 0.0003 | unexplained |
| 150 | wait_at stand | coffee_break(coffee_machine_0) | 0.9840 / 1.0000 | retired | 0.0010 / 0.0000 | 0.0010 / 0.0000 | adequate |
| 151 | wait_at stand | coffee_break(coffee_machine_0) | retired | retired | 0.4925 / - | 0.4925 / - | unresolved |
| 152 | wait_at  | coffee_break(coffee_machine_0) | retired | retired | 0.4925 / 1.0000 | 0.4925 / 1.0000 | adequate |
| 153 | move_to step | confirm_delivered_pallet(pallet_2) | 0.3287 / - | retired | 0.3408 / 1.0000 | 0.3166 / 0.9011 | adequate |
| 154 | move_to step | confirm_delivered_pallet(pallet_2) | 0.2959 / 0.7674 | retired | 0.3719 / 1.0000 | 0.3182 / 0.8053 | adequate |
| 155 | move_to step | confirm_delivered_pallet(pallet_2) | 0.2566 / 0.5663 | retired | 0.4097 / 1.0000 | 0.3196 / 0.7133 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 71 to 150, 165 to 179 |
| confirm_delivered_pallet(pallet_0) | 0 to 27 |
| confirm_delivered_pallet(pallet_2) | 71 to 150, 153 to 162 |
| office_break(office_chair) | 0 to 10, 71 to 117, 153 to 162, 165 to 175 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 9 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 10 to 27 | confirm_delivered_pallet(pallet_0) | clears |
| 28 to 70 | coffee_break(coffee_machine_0) | none(below_theta) |
| 71 to 92 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 93 to 117 | coffee_break(coffee_machine_0) | none(below_theta) |
| 118 to 119 | coffee_break(coffee_machine_0) | none(leader_inadequate) |
| 120 to 150 | coffee_break(coffee_machine_0) | clears |
| 151 to 162 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 163 to 180 | coffee_break(coffee_machine_0) | none(below_theta) |
| 181 to 219 | office_break(office_chair) | none(below_theta) |

The last entry (go_to(desk)): first step 165, last step 188, acknowledgement 189; the idle human from 190. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.5105 at 165; S < α from 180 (belief 0.5092; v·D 337.8 cm); the finding unexplained from 180.

- office_break(office_chair): belief 0.4745 at 165; S < α from 180 (belief 0.4758; v·D 344.8 cm); the finding unexplained from 180.

