### scenario_s02_05

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 28 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 30 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 81 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 83 | confirm_delivered_pallet(pallet_1) | covered | move_to | 0 | 1 |
| 134 | confirm_delivered_pallet(pallet_1) | covered | scan_it | 0 | 1 |
| 136 | confirm_delivered_pallet(pallet_3) | covered | move_to | 0 | 1 |
| 187 | confirm_delivered_pallet(pallet_3) | covered | scan_it | 0 | 1 |
| 189 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 214; idle from 215 to 244. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_1), confirm_delivered_pallet(pallet_2), confirm_delivered_pallet(pallet_3), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 244 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 25 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 26 to 27 |
| confirm_delivered_pallet(pallet_1) | move_to(pallet_1) | -1 to 25 |
| confirm_delivered_pallet(pallet_1) | scan_it(pallet_1) | 26 to 29 |
| confirm_delivered_pallet(pallet_1) | move_to(pallet_1) | 30 to 131 |
| confirm_delivered_pallet(pallet_1) | scan_it(pallet_1) | 132 to 133 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 78 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 79 to 80 |
| confirm_delivered_pallet(pallet_3) | move_to(pallet_3) | -1 to 78 |
| confirm_delivered_pallet(pallet_3) | scan_it(pallet_3) | 79 to 82 |
| confirm_delivered_pallet(pallet_3) | move_to(pallet_3) | 83 to 184 |
| confirm_delivered_pallet(pallet_3) | scan_it(pallet_3) | 185 to 186 |
| office_break(office_chair) | move_to(office_door) | -1 to 244 |

Events (actual):

| tick | event |
|---|---|
| 28 | boundary |
| 28 | pin confirm_delivered_pallet(pallet_0) |
| 81 | boundary |
| 81 | pin confirm_delivered_pallet(pallet_2) |
| 134 | boundary |
| 134 | pin confirm_delivered_pallet(pallet_1) |
| 187 | boundary |
| 187 | pin confirm_delivered_pallet(pallet_3) |
| 205 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), office_break(office_chair). At the last entry (go_to(desk), ticks 189 to 214): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 29 | not reached | - | - | - |
| confirm_delivered_pallet(pallet_2) | 30 to 82 | not reached | - | - | - |
| confirm_delivered_pallet(pallet_1) | 83 to 135 | 111 | 0.7771 | yes | adequate |
| confirm_delivered_pallet(pallet_3) | 136 to 188 | 186 | 0.7742 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 8 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0236 | 0.0445 | 346.4 | 346.4 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 9 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0229 | 0.0409 | 355.0 | 355.0 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 9 | confirm_delivered_pallet(pallet_3) | move_to(pallet_3) | 0.0229 | 0.0409 | 355.0 | 355.0 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 15 | office_break(office_chair) | move_to(office_door) | 0.0244 | 0.0373 | 364.1 | 364.1 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 39 | confirm_delivered_pallet(pallet_1) | move_to(pallet_1) | 0.0132 | 0.0391 | 359.4 | 359.4 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 62 | office_break(office_chair) | move_to(office_door) | 0.0225 | 0.0488 | 337.1 | 337.1 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 92 | confirm_delivered_pallet(pallet_3) | move_to(pallet_3) | 0.0246 | 0.0389 | 360.0 | 360.0 | 0.0 | confirm_delivered_pallet(pallet_1) |
| 94 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0255 | 0.0386 | 360.7 | 360.7 | 0.0 | confirm_delivered_pallet(pallet_1) |
| 116 | office_break(office_chair) | move_to(office_door) | 0.0459 | 0.0357 | 368.8 | 368.8 | 0.0 | confirm_delivered_pallet(pallet_1) |
| 168 | office_break(office_chair) | move_to(office_door) | 0.0341 | 0.0487 | 337.1 | 337.1 | 0.0 | confirm_delivered_pallet(pallet_3) |
| 204 | office_break(office_chair) | move_to(office_door) | 0.3940 | 0.0447 | 345.9 | 345.9 | 0.0 | - |
| 205 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.5683 | 0.0465 | 341.9 | 341.9 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 28 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 29 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 81 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 82 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 134 | adequate | unresolved | confirm_delivered_pallet(pallet_1) |
| 135 | unresolved | adequate | confirm_delivered_pallet(pallet_1) |
| 187 | adequate | unresolved | confirm_delivered_pallet(pallet_3) |
| 188 | unresolved | adequate | confirm_delivered_pallet(pallet_3) |
| 205 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 30 to 80, 136 to 186, 189 to 204 |
| confirm_delivered_pallet(pallet_0) | 0 to 27 |
| confirm_delivered_pallet(pallet_1) | 0 to 27, 83 to 133 |
| confirm_delivered_pallet(pallet_2) | 30 to 80 |
| confirm_delivered_pallet(pallet_3) | 30 to 80, 136 to 186 |
| office_break(office_chair) | 0 to 10, 30 to 78, 83 to 133, 136 to 184, 189 to 199 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 27 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 28 to 29 | coffee_break(coffee_machine_0) | none(below_theta) |
| 30 to 30 | confirm_delivered_pallet(pallet_1) | none(below_theta) |
| 31 to 80 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 81 to 82 | coffee_break(coffee_machine_0) | none(below_theta) |
| 83 to 83 | confirm_delivered_pallet(pallet_3) | none(below_theta) |
| 84 to 110 | confirm_delivered_pallet(pallet_1) | none(below_theta) |
| 111 to 133 | confirm_delivered_pallet(pallet_1) | clears |
| 134 to 135 | coffee_break(coffee_machine_0) | none(below_theta) |
| 136 to 185 | confirm_delivered_pallet(pallet_3) | none(below_theta) |
| 186 to 186 | confirm_delivered_pallet(pallet_3) | clears |
| 187 to 208 | coffee_break(coffee_machine_0) | none(below_theta) |
| 209 to 244 | office_break(office_chair) | none(below_theta) |

The last entry (go_to(desk)): first step 189, last step 213, acknowledgement 214; the idle human from 215. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.5102 at 189; S < α from 205 (belief 0.5683; v·D 341.9 cm); the finding unexplained from 205.

- office_break(office_chair): belief 0.4748 at 189; S < α from 204 (belief 0.3940; v·D 345.9 cm); the finding unexplained from 205.

