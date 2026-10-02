# scenario_s07_04: part 4 and the measures (single_task, prior on)

Completion (world tick) 469; terminal decision 471. [sep] minimum 25.48 (386), continuous 25.13 (387); near-encounters 4 ticks; F1 classes {'viol': 1, 'stand': 2, 'recede': 1, '?': 0}; holds [(382, 6)] (6 ticks).

## Declared properties

- **M(i)**: holds. the terminal decision 471
- **M(ii)**: holds. entries still open at the run's end: []
- **M(iii)**: DOES NOT HOLD. F1 classes {'viol': 1, 'stand': 2, 'recede': 1, '?': 0}
- **M(iv)**: holds. (pallet, the tick its delivery is first observable, the scan's first live tick): [('pallet_2', 57, 57), ('pallet_3', 148, 148), ('pallet_0', 239, 239), ('pallet_1', 376, 376)]

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=1 end=2.00 | deliver_pallet(?pallet=pallet_2) | 0 |
| 2 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=6.00 | deliver_pallet(?pallet=pallet_2) | 0 |
| 6 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=7 end=14.00 | deliver_pallet(?pallet=pallet_2) | 0 |
| 14 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=15 end=30.00 | deliver_pallet(?pallet=pallet_2) | 0 |
| 30 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=31 end=62.00 | deliver_pallet(?pallet=pallet_2) | 0 |
| 59 | no_current_task |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=3 end=63.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 63 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=7 end=71.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 71 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=15 end=81.31 | deliver_pallet(?pallet=pallet_3) | 0 |
| 76 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_2) | admitted confirm_delivered_pallet(?pallet=pallet_2) | deliver_pallet(?pallet=pallet_3) | 0 |
| 83 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=86.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 86 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=2 end=89.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 89 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=5 end=95.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 94 | recognition_changed | entered | clears | office_break(?office_chair=office_chair) | admitted office_break(?office_chair=office_chair) | deliver_pallet(?pallet=pallet_3) | 0 |
| 116 | recognition_changed | retraction | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=8 end=125.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 125 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=17 end=143.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 143 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=35 end=179.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 150 | no_current_task |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=3 end=154.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 154 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_3) | fallback moving k=7 end=162.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 155 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_3) | admitted confirm_delivered_pallet(?pallet=pallet_3) | deliver_pallet(?pallet=pallet_0) | 0 |
| 173 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=176.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 176 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=2 end=179.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 179 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=5 end=185.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 184 | recognition_changed | entered | clears | office_break(?office_chair=office_chair) | admitted office_break(?office_chair=office_chair) | deliver_pallet(?pallet=pallet_0) | 0 |
| 206 | recognition_changed | retraction | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=8 end=215.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 215 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=17 end=233.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 233 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=35 end=269.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 241 | no_current_task |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=3 end=245.00 | load_return(?pallet=pallet_4) | 0 |
| 245 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=7 end=253.00 | load_return(?pallet=pallet_4) | 0 |
| 251 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_0) | admitted confirm_delivered_pallet(?pallet=pallet_0) | load_return(?pallet=pallet_4) | 0 |
| 255 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=258.00 | load_return(?pallet=pallet_4) | 0 |
| 258 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=2 end=261.00 | load_return(?pallet=pallet_4) | 0 |
| 261 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=5 end=267.00 | load_return(?pallet=pallet_4) | 0 |
| 267 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=11 end=271.20 | load_return(?pallet=pallet_4) | 0 |
| 272 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=1 end=274.00 | load_return(?pallet=pallet_4) | 0 |
| 274 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=278.00 | load_return(?pallet=pallet_4) | 0 |
| 278 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=7 end=286.00 | load_return(?pallet=pallet_4) | 0 |
| 286 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=15 end=302.00 | load_return(?pallet=pallet_4) | 0 |
| 302 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=31 end=334.00 | load_return(?pallet=pallet_4) | 0 |
| 329 | no_current_task |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=58 end=388.00 | deliver_pallet(?pallet=pallet_1) | 0 |
| 378 | no_current_task |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_1) | fallback moving k=3 end=382.00 | load_return(?pallet=pallet_5) | 0 |
| 382 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_1) | fallback moving k=7 end=390.00 | load_return(?pallet=pallet_5) | 6 |
| 387 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_1) | admitted confirm_delivered_pallet(?pallet=pallet_1) | load_return(?pallet=pallet_5) | 0 |
| 392 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=395.00 | load_return(?pallet=pallet_5) | 0 |
| 395 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=2 end=398.00 | load_return(?pallet=pallet_5) | 0 |
| 398 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=5 end=404.00 | load_return(?pallet=pallet_5) | 0 |
| 404 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=11 end=408.21 | load_return(?pallet=pallet_5) | 0 |
| 409 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=16 end=426.00 | load_return(?pallet=pallet_5) | 0 |
| 426 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=33 end=428.05 | load_return(?pallet=pallet_5) | 0 |
| 429 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=1 end=431.00 | load_return(?pallet=pallet_5) | 0 |
| 431 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=435.00 | load_return(?pallet=pallet_5) | 0 |
| 435 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=7 end=443.00 | load_return(?pallet=pallet_5) | 0 |
| 443 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=15 end=459.00 | load_return(?pallet=pallet_5) | 0 |
| 459 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=31 end=491.00 | load_return(?pallet=pallet_5) | 0 |
| 471 | no_current_task |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=43 end=515.00 | None | 0 |
