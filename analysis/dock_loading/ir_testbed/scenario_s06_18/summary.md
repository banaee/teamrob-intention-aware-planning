### scenario_s06_18

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 17 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 19 | stand(PT80S) | task_absent | stand | 0 | 1 |
| 60 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 74 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 2 |
| 87 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 2 |
| 118 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 129 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 130 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 132 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 173; idle from 174 to 203. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 84 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 85 to 115 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 118 to 203 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 14 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 15 to 16 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 126 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 127 to 129 |
| office_break(office_chair) | move_to(office_door) | -1 to 203 |

Events (actual):

| tick | event |
|---|---|
| 17 | boundary |
| 17 | pin confirm_delivered_pallet(pallet_0) |
| 35 | finding turns unexplained |
| 85 | finding turns adequate (from unexplained) |
| 116 | boundary |
| 116 | pin coffee_break(coffee_machine_0) |
| 118 | re-entry coffee_break(coffee_machine_0) |
| 130 | boundary |
| 130 | pin confirm_delivered_pallet(pallet_2) |
| 155 | finding turns unexplained |

Never pinned: office_break(office_chair). At the last entry (go_to(desk), ticks 132 to 173): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 18 | not reached | - | - | - |
| confirm_delivered_pallet(pallet_2) | 60 to 73 | not reached | - | - | - |
| coffee_break(coffee_machine_0) | 74 to 117 | 81 | 0.7968 | yes | inadequate |
| confirm_delivered_pallet(pallet_2) | 118 to 131 | 129 | 0.7753 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 16 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0440 | 0.0466 | 341.7 | 321.7 | 20.0 | confirm_delivered_pallet(pallet_0) |
| 35 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.3287 | 0.0474 | 340.0 | 0.0 | 340.0 | - |
| 35 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.3287 | 0.0474 | 340.0 | 0.0 | 340.0 | - |
| 35 | office_break(office_chair) | move_to(office_door) | 0.3287 | 0.0474 | 340.0 | 0.0 | 340.0 | - |
| 127 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0367 | 0.0390 | 359.7 | 359.7 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 148 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.1637 | 0.0367 | 365.8 | 365.8 | 0.0 | - |
| 155 | office_break(office_chair) | move_to(office_door) | 0.9320 | 0.0494 | 335.7 | 335.7 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 17 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 18 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 35 | adequate | unexplained | - |
| 85 | unexplained | adequate | coffee_break(coffee_machine_0) |
| 116 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 117 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 130 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 131 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 155 | adequate | unexplained | - |

Across the started task coffee_break(coffee_machine_0) (covered; actual): on top of the stack from 74 to 117, its hypothesis pinned at 116; the suspended task resumes at 118.

| tick | human action | truth | coffee_break(coffee_machine_0) belief / S | confirm_delivered_pallet(pallet_0) belief / S | confirm_delivered_pallet(pallet_2) belief / S | office_break(office_chair) belief / S | finding |
|---|---|---|---|---|---|---|---|
| 72 | move_to step | confirm_delivered_pallet(pallet_2) | 0.3416 / 0.0002 | retired | 0.6405 / 0.0004 | 0.0039 / 0.0000 | unexplained |
| 73 | move_to step | confirm_delivered_pallet(pallet_2) | 0.3211 / 0.0002 | retired | 0.6622 / 0.0004 | 0.0027 / 0.0000 | unexplained |
| 74 | move_to step | coffee_break(coffee_machine_0) | 0.3481 / 0.0002 | retired | 0.6357 / 0.0004 | 0.0022 / 0.0000 | unexplained |
| 75 | move_to step | coffee_break(coffee_machine_0) | 0.3875 / 0.0002 | retired | 0.5967 / 0.0003 | 0.0019 / 0.0000 | unexplained |
| 76 | move_to step | coffee_break(coffee_machine_0) | 0.4416 / 0.0002 | retired | 0.5428 / 0.0002 | 0.0016 / 0.0000 | unexplained |
| 115 | wait_at stand | coffee_break(coffee_machine_0) | 0.9840 / 1.0000 | retired | 0.0010 / 0.0000 | 0.0010 / 0.0000 | adequate |
| 116 | wait_at stand | coffee_break(coffee_machine_0) | retired | retired | 0.4925 / - | 0.4925 / - | unresolved |
| 117 | wait_at  | coffee_break(coffee_machine_0) | retired | retired | 0.4925 / 1.0000 | 0.4925 / 1.0000 | adequate |
| 118 | move_to step | confirm_delivered_pallet(pallet_2) | 0.3287 / - | retired | 0.3400 / 1.0000 | 0.3173 / 0.9065 | adequate |
| 119 | move_to step | confirm_delivered_pallet(pallet_2) | 0.2899 / 0.7410 | retired | 0.3734 / 1.0000 | 0.3226 / 0.8160 | adequate |
| 120 | move_to step | confirm_delivered_pallet(pallet_2) | 0.2472 / 0.5363 | retired | 0.4119 / 1.0000 | 0.3268 / 0.7291 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 14, 60 to 115, 132 to 146 |
| confirm_delivered_pallet(pallet_0) | 0 to 16 |
| confirm_delivered_pallet(pallet_2) | 0 to 16, 60 to 115, 118 to 129 |
| office_break(office_chair) | 0 to 16, 118 to 129, 132 to 171 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 16 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 17 to 59 | coffee_break(coffee_machine_0) | none(below_theta) |
| 60 to 76 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 77 to 80 | coffee_break(coffee_machine_0) | none(below_theta) |
| 81 to 84 | coffee_break(coffee_machine_0) | none(leader_inadequate) |
| 85 to 115 | coffee_break(coffee_machine_0) | clears |
| 116 to 128 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 129 to 129 | confirm_delivered_pallet(pallet_2) | clears |
| 130 to 134 | coffee_break(coffee_machine_0) | none(below_theta) |
| 135 to 145 | office_break(office_chair) | none(below_theta) |
| 146 to 154 | office_break(office_chair) | clears |
| 155 to 203 | office_break(office_chair) | none(leader_inadequate) |

The last entry (go_to(desk)): first step 132, last step 172, acknowledgement 173; the idle human from 174. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.4935 at 132; S < α from 148 (belief 0.1637; v·D 365.8 cm); the finding unexplained from 155.

- office_break(office_chair): belief 0.4915 at 132; S < α from 155 (belief 0.9320; v·D 335.7 cm); the finding unexplained from 155.

