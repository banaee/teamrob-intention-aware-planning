### scenario_s02_08

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 28 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 2 |
| 79 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 2 |
| 110 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 161 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 163 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 214 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 216 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 241; idle from 242 to 271. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 76 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 77 to 107 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 110 to 271 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 25 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 26 to 27 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 28 to 158 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 159 to 160 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 211 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 212 to 213 |
| office_break(office_chair) | move_to(office_door) | -1 to 271 |

Events (actual):

| tick | event |
|---|---|
| 28 | finding turns unexplained |
| 29 | finding turns adequate (from unexplained) |
| 37 | finding turns unexplained |
| 77 | finding turns adequate (from unexplained) |
| 108 | boundary |
| 108 | pin coffee_break(coffee_machine_0) |
| 110 | re-entry coffee_break(coffee_machine_0) |
| 161 | boundary |
| 161 | pin confirm_delivered_pallet(pallet_0) |
| 214 | boundary |
| 214 | pin confirm_delivered_pallet(pallet_2) |
| 232 | finding turns unexplained |

Never pinned: office_break(office_chair). At the last entry (go_to(desk), ticks 216 to 241): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 27 | 10 | 0.7745 | yes | adequate |
| coffee_break(coffee_machine_0) | 28 to 109 | 78 | 0.7786 | yes | adequate |
| confirm_delivered_pallet(pallet_0) | 110 to 162 | 137 | 0.7734 | yes | adequate |
| confirm_delivered_pallet(pallet_2) | 163 to 215 | 213 | 0.7759 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 8 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0409 | 0.0445 | 346.4 | 346.4 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 9 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0406 | 0.0409 | 355.0 | 355.0 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 15 | office_break(office_chair) | move_to(office_door) | 0.0475 | 0.0373 | 364.1 | 364.1 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 37 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.9707 | 0.0390 | 359.8 | 359.8 | 0.0 | coffee_break(coffee_machine_0) |
| 119 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0243 | 0.0389 | 360.0 | 360.0 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 121 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0279 | 0.0408 | 355.1 | 355.1 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 143 | office_break(office_chair) | move_to(office_door) | 0.0503 | 0.0393 | 358.9 | 358.9 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 195 | office_break(office_chair) | move_to(office_door) | 0.0337 | 0.0481 | 338.4 | 338.4 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 231 | office_break(office_chair) | move_to(office_door) | 0.3947 | 0.0449 | 345.3 | 345.3 | 0.0 | - |
| 232 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.5675 | 0.0466 | 341.6 | 341.6 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 28 | adequate | unexplained | coffee_break(coffee_machine_0) |
| 29 | unexplained | adequate | coffee_break(coffee_machine_0) |
| 37 | adequate | unexplained | coffee_break(coffee_machine_0) |
| 77 | unexplained | adequate | coffee_break(coffee_machine_0) |
| 108 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 109 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 161 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 162 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 214 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 215 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 232 | adequate | unexplained | - |

Across the started task coffee_break(coffee_machine_0) (covered; actual): on top of the stack from 28 to 109, its hypothesis pinned at 108; the suspended task resumes at 110.

| tick | human action | truth | coffee_break(coffee_machine_0) belief / S | confirm_delivered_pallet(pallet_0) belief / S | confirm_delivered_pallet(pallet_2) belief / S | office_break(office_chair) belief / S | finding |
|---|---|---|---|---|---|---|---|
| 26 | move_to step | confirm_delivered_pallet(pallet_0) | 0.0010 / 0.0000 | 0.9839 / 1.0000 | 0.0010 / 0.0001 | 0.0011 / 0.0008 | adequate |
| 27 | move_to  | confirm_delivered_pallet(pallet_0) | 0.0010 / 0.0000 | 0.9840 / 1.0000 | 0.0010 / 0.0001 | 0.0010 / 0.0007 | adequate |
| 28 | move_to step | coffee_break(coffee_machine_0) | 0.0010 / 0.0000 | 0.9840 / - | 0.0010 / 0.0001 | 0.0010 / 0.0007 | unexplained |
| 29 | move_to step | coffee_break(coffee_machine_0) | 0.0010 / 0.0000 | 0.9839 / 0.7405 | 0.0010 / 0.0001 | 0.0011 / 0.0007 | adequate |
| 30 | move_to step | coffee_break(coffee_machine_0) | 0.0010 / 0.0000 | 0.9836 / 0.5359 | 0.0010 / 0.0001 | 0.0014 / 0.0006 | adequate |
| 107 | wait_at stand | coffee_break(coffee_machine_0) | 0.9840 / 1.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | adequate |
| 108 | wait_at stand | coffee_break(coffee_machine_0) | retired | 0.3287 / - | 0.3287 / - | 0.3287 / - | unresolved |
| 109 | wait_at  | coffee_break(coffee_machine_0) | retired | 0.3287 / 1.0000 | 0.3287 / 1.0000 | 0.3287 / 1.0000 | adequate |
| 110 | move_to step | confirm_delivered_pallet(pallet_0) | 0.2467 / - | 0.2560 / 1.0000 | 0.2297 / 0.8588 | 0.2546 / 0.9923 | adequate |
| 111 | move_to step | confirm_delivered_pallet(pallet_0) | 0.2152 / 0.7401 | 0.2781 / 1.0000 | 0.2187 / 0.7206 | 0.2750 / 0.9841 | adequate |
| 112 | move_to step | confirm_delivered_pallet(pallet_0) | 0.1814 / 0.5354 | 0.3035 / 1.0000 | 0.2038 / 0.5902 | 0.2983 / 0.9753 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 53 to 107, 163 to 213, 216 to 231 |
| confirm_delivered_pallet(pallet_0) | 0 to 27, 110 to 160 |
| confirm_delivered_pallet(pallet_2) | 51 to 107, 163 to 213 |
| office_break(office_chair) | 0 to 10, 39 to 62, 110 to 160, 163 to 211, 216 to 226 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 9 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 10 to 27 | confirm_delivered_pallet(pallet_0) | clears |
| 28 to 28 | confirm_delivered_pallet(pallet_0) | none(leader_no_observation) |
| 29 to 36 | confirm_delivered_pallet(pallet_0) | clears |
| 37 to 45 | confirm_delivered_pallet(pallet_0) | none(leader_inadequate) |
| 46 to 50 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 51 to 55 | office_break(office_chair) | none(below_theta) |
| 56 to 67 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 68 to 77 | coffee_break(coffee_machine_0) | none(below_theta) |
| 78 to 107 | coffee_break(coffee_machine_0) | clears |
| 108 to 136 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 137 to 160 | confirm_delivered_pallet(pallet_0) | clears |
| 161 to 162 | coffee_break(coffee_machine_0) | none(below_theta) |
| 163 to 212 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 213 to 213 | confirm_delivered_pallet(pallet_2) | clears |
| 214 to 235 | coffee_break(coffee_machine_0) | none(below_theta) |
| 236 to 271 | office_break(office_chair) | none(below_theta) |

The last entry (go_to(desk)): first step 216, last step 240, acknowledgement 241; the idle human from 242. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.5102 at 216; S < α from 232 (belief 0.5675; v·D 341.6 cm); the finding unexplained from 232.

- office_break(office_chair): belief 0.4748 at 216; S < α from 231 (belief 0.3947; v·D 345.3 cm); the finding unexplained from 232.

