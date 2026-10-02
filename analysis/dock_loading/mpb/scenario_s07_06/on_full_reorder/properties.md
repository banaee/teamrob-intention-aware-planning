# scenario_s07_06: part 4 and the measures (full_reorder, prior on)

Completion (world tick) 433; terminal decision 435. [sep] minimum 13.83 (456), continuous 13.75 (458); near-encounters 23 ticks; F1 classes {'viol': 0, 'stand': 19, 'recede': 4, '?': 0}; holds [(63, 6), (206, 5)] (11 ticks).

## Declared properties

- **M(i)**: holds. the terminal decision 435
- **M(ii)**: holds. entries still open at the run's end: []
- **M(iii)**: holds. F1 classes {'viol': 0, 'stand': 19, 'recede': 4, '?': 0}
- **M(iv)**: holds. (pallet, the tick its delivery is first observable, the scan's first live tick): [('pallet_0', 57, 57), ('pallet_1', 200, 200), ('pallet_2', 342, 342), ('pallet_3', 433, 433)]

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=1 end=2.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 2 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=6.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 6 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=7 end=14.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 14 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=15 end=30.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 30 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=31 end=62.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 59 | no_current_task |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=3 end=63.00 | load_return(?pallet=pallet_4) | 0 |
| 63 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=7 end=71.00 | load_return(?pallet=pallet_4) | 6 |
| 69 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_0) | admitted confirm_delivered_pallet(?pallet=pallet_0) | load_return(?pallet=pallet_4) | 0 |
| 74 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=77.00 | load_return(?pallet=pallet_4) | 0 |
| 77 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=2 end=80.00 | load_return(?pallet=pallet_4) | 0 |
| 80 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=5 end=86.00 | load_return(?pallet=pallet_4) | 0 |
| 86 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=11 end=90.50 | load_return(?pallet=pallet_4) | 0 |
| 91 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=1 end=93.00 | load_return(?pallet=pallet_4) | 0 |
| 93 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=97.00 | load_return(?pallet=pallet_4) | 0 |
| 97 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=7 end=105.00 | load_return(?pallet=pallet_4) | 0 |
| 105 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=15 end=121.00 | load_return(?pallet=pallet_4) | 0 |
| 121 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=31 end=153.00 | load_return(?pallet=pallet_4) | 0 |
| 153 | no_current_task |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=63 end=217.00 | deliver_pallet(?pallet=pallet_1) | 0 |
| 202 | no_current_task |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_1) | fallback moving k=3 end=206.00 | load_return(?pallet=pallet_5) | 0 |
| 206 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_1) | fallback moving k=7 end=214.00 | load_return(?pallet=pallet_5) | 5 |
| 211 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_1) | admitted confirm_delivered_pallet(?pallet=pallet_1) | load_return(?pallet=pallet_5) | 0 |
| 216 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=219.00 | load_return(?pallet=pallet_5) | 0 |
| 219 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=2 end=222.00 | load_return(?pallet=pallet_5) | 0 |
| 222 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=5 end=228.00 | load_return(?pallet=pallet_5) | 0 |
| 228 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=11 end=232.50 | load_return(?pallet=pallet_5) | 0 |
| 233 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=1 end=235.00 | load_return(?pallet=pallet_5) | 0 |
| 235 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=239.00 | load_return(?pallet=pallet_5) | 0 |
| 239 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=7 end=247.00 | load_return(?pallet=pallet_5) | 0 |
| 247 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=15 end=263.00 | load_return(?pallet=pallet_5) | 0 |
| 263 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=31 end=295.00 | load_return(?pallet=pallet_5) | 0 |
| 295 | no_current_task |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=63 end=359.00 | deliver_pallet(?pallet=pallet_2) | 0 |
| 344 | no_current_task |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=3 end=348.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 348 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=7 end=356.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 356 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=15 end=365.60 | deliver_pallet(?pallet=pallet_3) | 0 |
| 361 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_2) | admitted confirm_delivered_pallet(?pallet=pallet_2) | deliver_pallet(?pallet=pallet_3) | 0 |
| 367 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=370.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 370 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=2 end=373.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 373 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=5 end=379.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 378 | recognition_changed | entered | clears | office_break(?office_chair=office_chair) | admitted office_break(?office_chair=office_chair) | deliver_pallet(?pallet=pallet_3) | 0 |
| 400 | recognition_changed | retraction | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=8 end=409.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 409 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=17 end=427.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 427 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=35 end=463.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 435 | no_current_task |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=3 end=439.00 | None | 0 |
