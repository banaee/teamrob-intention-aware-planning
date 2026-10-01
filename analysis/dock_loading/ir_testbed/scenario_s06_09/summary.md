### scenario_s06_09

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 14 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 2 |
| 37 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 2 |
| 68 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 91 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 92 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 94 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 111 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 113 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 154; idle from 155 to 184. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 34 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 35 to 65 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 68 to 184 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 88 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 89 to 91 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 108 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 109 to 110 |
| office_break(office_chair) | move_to(office_door) | -1 to 184 |

Events (actual):

| tick | event |
|---|---|
| 66 | boundary |
| 66 | pin coffee_break(coffee_machine_0) |
| 68 | re-entry coffee_break(coffee_machine_0) |
| 92 | boundary |
| 92 | pin confirm_delivered_pallet(pallet_0) |
| 111 | boundary |
| 111 | pin confirm_delivered_pallet(pallet_2) |
| 136 | finding turns unexplained |

Never pinned: office_break(office_chair). At the last entry (go_to(desk), ticks 113 to 154): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 13 | not reached | - | - | - |
| coffee_break(coffee_machine_0) | 14 to 67 | 34 | 0.7552 | yes | adequate |
| confirm_delivered_pallet(pallet_0) | 68 to 93 | not reached | - | - | - |
| confirm_delivered_pallet(pallet_2) | 94 to 112 | not reached | - | - | - |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 16 | office_break(office_chair) | move_to(office_door) | 0.0589 | 0.0495 | 335.6 | 335.6 | 0.0 | coffee_break(coffee_machine_0) |
| 23 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.1080 | 0.0363 | 367.1 | 367.1 | 0.0 | coffee_break(coffee_machine_0) |
| 32 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.3337 | 0.0481 | 338.4 | 338.4 | 0.0 | coffee_break(coffee_machine_0) |
| 77 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0224 | 0.0389 | 360.0 | 360.0 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 83 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0311 | 0.0439 | 347.8 | 347.8 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 102 | office_break(office_chair) | move_to(office_door) | 0.0300 | 0.0419 | 352.5 | 352.5 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 129 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.1776 | 0.0379 | 362.5 | 362.5 | 0.0 | - |
| 136 | office_break(office_chair) | move_to(office_door) | 0.9198 | 0.0431 | 349.7 | 349.7 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 66 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 67 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 92 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 93 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 111 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 112 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 136 | adequate | unexplained | - |

Across the started task coffee_break(coffee_machine_0) (covered; actual): on top of the stack from 14 to 67, its hypothesis pinned at 66; the suspended task resumes at 68.

| tick | human action | truth | coffee_break(coffee_machine_0) belief / S | confirm_delivered_pallet(pallet_0) belief / S | confirm_delivered_pallet(pallet_2) belief / S | office_break(office_chair) belief / S | finding |
|---|---|---|---|---|---|---|---|
| 12 | move_to step | confirm_delivered_pallet(pallet_0) | 0.0846 / 0.1203 | 0.5289 / 1.0000 | 0.2460 / 0.3820 | 0.1274 / 0.1851 | adequate |
| 13 | move_to step | confirm_delivered_pallet(pallet_0) | 0.0723 / 0.0945 | 0.5697 / 1.0000 | 0.2365 / 0.3357 | 0.1085 / 0.1443 | adequate |
| 14 | move_to step | coffee_break(coffee_machine_0) | 0.0820 / 0.0945 | 0.5546 / 0.8090 | 0.2623 / 0.3273 | 0.0881 / 0.1019 | adequate |
| 15 | move_to step | coffee_break(coffee_machine_0) | 0.0948 / 0.0945 | 0.5244 / 0.6236 | 0.2958 / 0.3183 | 0.0720 / 0.0712 | adequate |
| 16 | move_to step | coffee_break(coffee_machine_0) | 0.1109 / 0.0945 | 0.4805 / 0.4634 | 0.3366 / 0.3084 | 0.0589 / 0.0495 | adequate |
| 65 | wait_at stand | coffee_break(coffee_machine_0) | 0.9840 / 1.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0001 | 0.0010 / 0.0000 | adequate |
| 66 | wait_at stand | coffee_break(coffee_machine_0) | retired | 0.3287 / - | 0.3287 / - | 0.3287 / - | unresolved |
| 67 | wait_at  | coffee_break(coffee_machine_0) | retired | 0.3287 / 1.0000 | 0.3287 / 1.0000 | 0.3287 / 1.0000 | adequate |
| 68 | move_to step | confirm_delivered_pallet(pallet_0) | 0.2467 / - | 0.2505 / 1.0000 | 0.2406 / 0.9441 | 0.2491 / 0.9916 | adequate |
| 69 | move_to step | confirm_delivered_pallet(pallet_0) | 0.2113 / 0.7402 | 0.2672 / 1.0000 | 0.2445 / 0.8819 | 0.2640 / 0.9828 | adequate |
| 70 | move_to step | confirm_delivered_pallet(pallet_0) | 0.1745 / 0.5354 | 0.2858 / 1.0000 | 0.2463 / 0.8133 | 0.2804 / 0.9734 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 65, 94 to 110, 113 to 127 |
| confirm_delivered_pallet(pallet_0) | 0 to 28, 68 to 91 |
| confirm_delivered_pallet(pallet_2) | 0 to 65, 68 to 80, 94 to 110 |
| office_break(office_chair) | 0 to 16, 68 to 91, 113 to 150 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 17 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 18 to 29 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 30 to 33 | coffee_break(coffee_machine_0) | none(below_theta) |
| 34 to 65 | coffee_break(coffee_machine_0) | clears |
| 66 to 91 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 92 to 93 | coffee_break(coffee_machine_0) | none(below_theta) |
| 94 to 110 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 111 to 112 | coffee_break(coffee_machine_0) | none(below_theta) |
| 113 to 126 | office_break(office_chair) | none(below_theta) |
| 127 to 135 | office_break(office_chair) | clears |
| 136 to 184 | office_break(office_chair) | none(leader_inadequate) |

The last entry (go_to(desk)): first step 113, last step 153, acknowledgement 154; the idle human from 155. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.4924 at 113; S < α from 129 (belief 0.1776; v·D 362.5 cm); the finding unexplained from 136.

- office_break(office_chair): belief 0.4926 at 113; S < α from 136 (belief 0.9198; v·D 349.7 cm); the finding unexplained from 136.

