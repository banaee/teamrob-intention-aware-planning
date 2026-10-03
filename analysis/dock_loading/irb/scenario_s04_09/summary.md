### scenario_s04_09

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 14 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 2 |
| 32 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 2 |
| 63 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 85 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 86 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 88 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 140 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 142 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 157; idle from 158 to 187. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 29 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 30 to 60 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 63 to 187 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 82 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 83 to 85 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 137 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 138 to 139 |
| office_break(office_chair) | move_to(office_door) | -1 to 187 |

Events (actual):

| tick | event |
|---|---|
| 61 | boundary |
| 61 | pin coffee_break(coffee_machine_0) |
| 63 | re-entry coffee_break(coffee_machine_0) |
| 86 | boundary |
| 86 | pin confirm_delivered_pallet(pallet_0) |
| 140 | boundary |
| 140 | pin confirm_delivered_pallet(pallet_2) |
| 169 | finding turns unexplained |

Never pinned: office_break(office_chair). At the last entry (go_to(desk), ticks 142 to 157): lifecycle and finding adequate; on the idle ticks after it: adequate, unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 13 | not reached | - | - | - |
| coffee_break(coffee_machine_0) | 14 to 62 | 25 | 0.7777 | yes | adequate |
| confirm_delivered_pallet(pallet_0) | 63 to 87 | 78 | 0.7727 | yes | adequate |
| confirm_delivered_pallet(pallet_2) | 88 to 141 | 112 | 0.7617 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 8 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0301 | 0.0431 | 349.6 | 349.6 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 14 | office_break(office_chair) | move_to(office_door) | 0.0517 | 0.0477 | 339.4 | 339.4 | 0.0 | coffee_break(coffee_machine_0) |
| 26 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.1580 | 0.0380 | 362.3 | 362.3 | 0.0 | coffee_break(coffee_machine_0) |
| 72 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0295 | 0.0399 | 357.3 | 357.3 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 76 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0464 | 0.0479 | 338.8 | 338.8 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 85 | office_break(office_chair) | move_to(office_door) | 0.0587 | 0.0467 | 341.4 | 301.4 | 40.0 | confirm_delivered_pallet(pallet_0) |
| 105 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0327 | 0.0416 | 353.3 | 353.3 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 118 | office_break(office_chair) | move_to(office_door) | 0.0589 | 0.0467 | 341.5 | 341.5 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 156 | office_break(office_chair) | move_to(office_door) | 0.0927 | 0.0429 | 350.0 | 350.0 | 0.0 | - |
| 169 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9130 | 0.0415 | 353.4 | 93.4 | 260.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 61 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 62 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 86 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 87 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 140 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 141 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 169 | adequate | unexplained | - |

Across the started task coffee_break(coffee_machine_0) (covered; actual): on top of the stack from 14 to 62, its hypothesis pinned at 61; the suspended task resumes at 63.

| tick | human action | truth | coffee_break(coffee_machine_0) belief / S | confirm_delivered_pallet(pallet_0) belief / S | confirm_delivered_pallet(pallet_2) belief / S | office_break(office_chair) belief / S | finding |
|---|---|---|---|---|---|---|---|
| 12 | move_to step | confirm_delivered_pallet(pallet_0) | 0.2174 / 0.2523 | 0.6776 / 1.0000 | 0.0085 / 0.0091 | 0.0836 / 0.0918 | adequate |
| 13 | move_to step | confirm_delivered_pallet(pallet_0) | 0.1954 / 0.2108 | 0.7186 / 1.0000 | 0.0061 / 0.0061 | 0.0669 / 0.0687 | adequate |
| 14 | move_to step | coffee_break(coffee_machine_0) | 0.2163 / 0.2108 | 0.7137 / 0.8585 | 0.0052 / 0.0048 | 0.0517 / 0.0477 | adequate |
| 15 | move_to step | coffee_break(coffee_machine_0) | 0.2415 / 0.2108 | 0.7009 / 0.7240 | 0.0045 / 0.0037 | 0.0400 / 0.0329 | adequate |
| 16 | move_to step | coffee_break(coffee_machine_0) | 0.2719 / 0.2108 | 0.6801 / 0.5995 | 0.0039 / 0.0028 | 0.0311 / 0.0226 | adequate |
| 60 | wait_at stand | coffee_break(coffee_machine_0) | 0.9840 / 1.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | adequate |
| 61 | wait_at stand | coffee_break(coffee_machine_0) | retired | 0.3287 / - | 0.3287 / - | 0.3287 / - | unresolved |
| 62 | wait_at  | coffee_break(coffee_machine_0) | retired | 0.3287 / 1.0000 | 0.3287 / 1.0000 | 0.3287 / 1.0000 | adequate |
| 63 | move_to step | confirm_delivered_pallet(pallet_0) | 0.2467 / - | 0.2597 / 1.0000 | 0.2319 / 0.8531 | 0.2487 / 0.9399 | adequate |
| 64 | move_to step | confirm_delivered_pallet(pallet_0) | 0.2185 / 0.7462 | 0.2847 / 1.0000 | 0.2238 / 0.7202 | 0.2600 / 0.8796 | adequate |
| 65 | move_to step | confirm_delivered_pallet(pallet_0) | 0.1870 / 0.5426 | 0.3139 / 1.0000 | 0.2141 / 0.6018 | 0.2720 / 0.8192 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 60, 88 to 105, 142 to 187 |
| confirm_delivered_pallet(pallet_0) | 0 to 60, 63 to 85 |
| confirm_delivered_pallet(pallet_2) | 88 to 139 |
| office_break(office_chair) | 0 to 10, 63 to 85, 88 to 135, 142 to 146 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 20 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 21 to 24 | coffee_break(coffee_machine_0) | none(below_theta) |
| 25 to 60 | coffee_break(coffee_machine_0) | clears |
| 61 to 77 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 78 to 85 | confirm_delivered_pallet(pallet_0) | clears |
| 86 to 87 | coffee_break(coffee_machine_0) | none(below_theta) |
| 88 to 111 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 112 to 139 | confirm_delivered_pallet(pallet_2) | clears |
| 140 to 150 | coffee_break(coffee_machine_0) | none(below_theta) |
| 151 to 168 | coffee_break(coffee_machine_0) | clears |
| 169 to 187 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(desk)): first step 142, last step 156, acknowledgement 157; the idle human from 158. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.5107 at 142; S < α from 169 (belief 0.9130; v·D 353.4 cm); the finding unexplained from 169.

- office_break(office_chair): belief 0.4743 at 142; S < α from 156 (belief 0.0927; v·D 350.0 cm); the finding unexplained from 169.

