### scenario_s06_08

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 17 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 2 |
| 40 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 2 |
| 71 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 93 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 95 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 112 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 114 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 155; idle from 156 to 185. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 37 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 38 to 68 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 71 to 185 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 14 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 15 to 17 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 18 to 90 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 91 to 92 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 109 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 110 to 111 |
| office_break(office_chair) | move_to(office_door) | -1 to 185 |

Events (actual):

| tick | event |
|---|---|
| 33 | finding turns unexplained |
| 38 | finding turns adequate (from unexplained) |
| 69 | boundary |
| 69 | pin coffee_break(coffee_machine_0) |
| 71 | re-entry coffee_break(coffee_machine_0) |
| 93 | boundary |
| 93 | pin confirm_delivered_pallet(pallet_0) |
| 112 | boundary |
| 112 | pin confirm_delivered_pallet(pallet_2) |
| 137 | finding turns unexplained |

Never pinned: office_break(office_chair). At the last entry (go_to(desk), ticks 114 to 155): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 16 | not reached | - | - | - |
| coffee_break(coffee_machine_0) | 17 to 70 | 38 | 0.7717 | yes | adequate |
| confirm_delivered_pallet(pallet_0) | 71 to 94 | not reached | - | - | - |
| confirm_delivered_pallet(pallet_2) | 95 to 113 | not reached | - | - | - |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 16 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0440 | 0.0466 | 341.7 | 321.7 | 20.0 | confirm_delivered_pallet(pallet_0) |
| 17 | office_break(office_chair) | move_to(office_door) | 0.0478 | 0.0495 | 335.4 | 315.4 | 20.0 | coffee_break(coffee_machine_0) |
| 27 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.1896 | 0.0394 | 358.6 | 358.6 | 0.0 | coffee_break(coffee_machine_0) |
| 33 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.4806 | 0.0479 | 339.0 | 319.0 | 20.0 | coffee_break(coffee_machine_0) |
| 80 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0227 | 0.0389 | 360.0 | 360.0 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 86 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0266 | 0.0370 | 365.1 | 365.1 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 103 | office_break(office_chair) | move_to(office_door) | 0.0298 | 0.0414 | 353.7 | 353.7 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 130 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.1776 | 0.0389 | 360.0 | 360.0 | 0.0 | - |
| 137 | office_break(office_chair) | move_to(office_door) | 0.9215 | 0.0451 | 345.0 | 345.0 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 33 | adequate | unexplained | coffee_break(coffee_machine_0) |
| 38 | unexplained | adequate | coffee_break(coffee_machine_0) |
| 69 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 70 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 93 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 94 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 112 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 113 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 137 | adequate | unexplained | - |

Across the started task coffee_break(coffee_machine_0) (covered; actual): on top of the stack from 17 to 70, its hypothesis pinned at 69; the suspended task resumes at 71.

| tick | human action | truth | coffee_break(coffee_machine_0) belief / S | confirm_delivered_pallet(pallet_0) belief / S | confirm_delivered_pallet(pallet_2) belief / S | office_break(office_chair) belief / S | finding |
|---|---|---|---|---|---|---|---|
| 15 | move_to step | confirm_delivered_pallet(pallet_0) | 0.0504 / 0.0567 | 0.6542 / 1.0000 | 0.2087 / 0.2507 | 0.0736 / 0.0835 | adequate |
| 16 | move_to  | confirm_delivered_pallet(pallet_0) | 0.0440 / 0.0466 | 0.6923 / 1.0000 | 0.1862 / 0.2084 | 0.0644 / 0.0687 | adequate |
| 17 | move_to step | coffee_break(coffee_machine_0) | 0.0450 / 0.0466 | 0.7080 / 1.0000 | 0.1862 / 0.2034 | 0.0478 / 0.0495 | adequate |
| 18 | move_to step | coffee_break(coffee_machine_0) | 0.0458 / 0.0466 | 0.7212 / - | 0.1850 / 0.1981 | 0.0349 / 0.0354 | adequate |
| 19 | move_to step | coffee_break(coffee_machine_0) | 0.0544 / 0.0466 | 0.6895 / 0.7432 | 0.2136 / 0.1922 | 0.0295 / 0.0251 | adequate |
| 68 | wait_at stand | coffee_break(coffee_machine_0) | 0.9840 / 1.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | adequate |
| 69 | wait_at stand | coffee_break(coffee_machine_0) | retired | 0.3287 / - | 0.3287 / - | 0.3287 / - | unresolved |
| 70 | wait_at  | coffee_break(coffee_machine_0) | retired | 0.3287 / 1.0000 | 0.3287 / 1.0000 | 0.3287 / 1.0000 | adequate |
| 71 | move_to step | confirm_delivered_pallet(pallet_0) | 0.2467 / - | 0.2509 / 1.0000 | 0.2400 / 0.9387 | 0.2494 / 0.9913 | adequate |
| 72 | move_to step | confirm_delivered_pallet(pallet_0) | 0.2115 / 0.7401 | 0.2680 / 1.0000 | 0.2429 / 0.8708 | 0.2646 / 0.9822 | adequate |
| 73 | move_to step | confirm_delivered_pallet(pallet_0) | 0.1750 / 0.5354 | 0.2870 / 1.0000 | 0.2435 / 0.7963 | 0.2815 / 0.9724 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 14, 17 to 68, 95 to 111, 114 to 128 |
| confirm_delivered_pallet(pallet_0) | 0 to 17, 71 to 92 |
| confirm_delivered_pallet(pallet_2) | 0 to 68, 71 to 82, 95 to 111 |
| office_break(office_chair) | 0 to 18, 71 to 92, 114 to 151 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 23 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 24 to 33 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 34 to 37 | coffee_break(coffee_machine_0) | none(below_theta) |
| 38 to 68 | coffee_break(coffee_machine_0) | clears |
| 69 to 92 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 93 to 94 | coffee_break(coffee_machine_0) | none(below_theta) |
| 95 to 111 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 112 to 114 | coffee_break(coffee_machine_0) | none(below_theta) |
| 115 to 128 | office_break(office_chair) | none(below_theta) |
| 129 to 136 | office_break(office_chair) | clears |
| 137 to 185 | office_break(office_chair) | none(leader_inadequate) |

The last entry (go_to(desk)): first step 114, last step 154, acknowledgement 155; the idle human from 156. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.4927 at 114; S < α from 130 (belief 0.1776; v·D 360.0 cm); the finding unexplained from 137.

- office_break(office_chair): belief 0.4923 at 114; S < α from 137 (belief 0.9215; v·D 345.0 cm); the finding unexplained from 137.

