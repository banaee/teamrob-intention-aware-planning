# scenario_s05_04: part 4 and the measures (single_task, prior on)

Completion (world tick) 428; terminal decision 430. [sep] minimum 98.10 (162), continuous 96.94 (162); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

## Declared properties

- **M(i)**: holds. the terminal decision 430
- **M(ii)**: holds. entries still open at the run's end: []
- **M(iii)**: holds. F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}
- **M(iv)**: holds. (pallet, the tick its delivery is first observable, the scan's first live tick): [('pallet_2', 58, 58), ('pallet_3', 150, 150), ('pallet_0', 249, 249), ('pallet_1', 367, 367)]

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
| 60 | no_current_task |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=3 end=64.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 64 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=7 end=72.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 65 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_2) | admitted confirm_delivered_pallet(?pallet=pallet_2) | deliver_pallet(?pallet=pallet_3) | 0 |
| 84 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=87.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 87 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=2 end=90.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 90 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=5 end=96.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 96 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=11 end=108.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 108 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=23 end=109.50 | deliver_pallet(?pallet=pallet_3) | 0 |
| 109 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | deliver_pallet(?pallet=pallet_3) | 0 |
| 125 | recognition_changed | retraction | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=16 end=142.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 142 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=33 end=176.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 152 | no_current_task |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_3) | fallback moving k=3 end=156.00 | load_return(?pallet=pallet_4) | 0 |
| 156 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_3) | admitted confirm_delivered_pallet(?pallet=pallet_3) | deliver_pallet(?pallet=pallet_0) | 0 |
| 175 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=178.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 178 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=2 end=181.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 181 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=5 end=187.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 187 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=11 end=199.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 199 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=23 end=200.50 | deliver_pallet(?pallet=pallet_0) | 0 |
| 200 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | deliver_pallet(?pallet=pallet_0) | 0 |
| 216 | recognition_changed | retraction | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=16 end=233.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 233 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=33 end=267.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 251 | no_current_task |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=3 end=255.00 | load_return(?pallet=pallet_4) | 0 |
| 255 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=7 end=263.00 | load_return(?pallet=pallet_4) | 0 |
| 263 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_0) | admitted confirm_delivered_pallet(?pallet=pallet_0) | load_return(?pallet=pallet_4) | 0 |
| 278 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=281.00 | load_return(?pallet=pallet_4) | 0 |
| 281 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=2 end=284.00 | load_return(?pallet=pallet_4) | 0 |
| 284 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=5 end=290.00 | load_return(?pallet=pallet_4) | 0 |
| 290 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=11 end=302.00 | load_return(?pallet=pallet_4) | 0 |
| 296 | recognition_changed | entered | clears | office_break(?office_chair=office_chair) | admitted office_break(?office_chair=office_chair) | load_return(?pallet=pallet_4) | 0 |
| 307 | recognition_changed | retraction | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=2 end=310.00 | load_return(?pallet=pallet_4) | 0 |
| 310 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=5 end=316.00 | deliver_pallet(?pallet=pallet_1) | 0 |
| 316 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=11 end=328.00 | deliver_pallet(?pallet=pallet_1) | 0 |
| 328 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=23 end=352.00 | deliver_pallet(?pallet=pallet_1) | 0 |
| 352 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=47 end=400.00 | deliver_pallet(?pallet=pallet_1) | 0 |
| 369 | no_current_task |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=3 end=373.00 | load_return(?pallet=pallet_5) | 0 |
| 373 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_1) | fallback moving k=7 end=381.00 | load_return(?pallet=pallet_5) | 0 |
| 377 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_1) | admitted confirm_delivered_pallet(?pallet=pallet_1) | load_return(?pallet=pallet_5) | 0 |
| 394 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=397.00 | load_return(?pallet=pallet_5) | 0 |
| 397 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=2 end=400.00 | load_return(?pallet=pallet_5) | 0 |
| 400 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=5 end=406.00 | load_return(?pallet=pallet_5) | 0 |
| 406 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=11 end=418.00 | load_return(?pallet=pallet_5) | 0 |
| 418 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=23 end=440.84 | load_return(?pallet=pallet_5) | 0 |
| 430 | no_current_task |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=35 end=440.84 | None | 0 |
