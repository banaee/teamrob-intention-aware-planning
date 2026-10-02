# scenario_s05_05: part 4 and the measures (full_reorder, prior on)

Completion (world tick) 383; terminal decision 385. [sep] minimum 18.72 (441), continuous 17.95 (442); near-encounters 9 ticks; F1 classes {'viol': 0, 'stand': 9, 'recede': 0, '?': 0}; holds [] (0 ticks).

## Declared properties

- **M(i)**: holds. the terminal decision 385
- **M(ii)**: holds. entries still open at the run's end: []
- **M(iii)**: holds. F1 classes {'viol': 0, 'stand': 9, 'recede': 0, '?': 0}
- **M(iv)**: holds. (pallet, the tick its delivery is first observable, the scan's first live tick): [('pallet_0', 64, 64), ('pallet_1', 182, 182), ('pallet_2', 292, 292), ('pallet_3', 383, 383)]

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## m2

{'two_scans_live_in_one_bay': [], 'decisions_at_an_occupied_bay': [319]}

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=1 end=2.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 2 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=6.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 6 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=7 end=14.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 14 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=15 end=30.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 30 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=31 end=62.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 62 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=63 end=126.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 66 | no_current_task |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=3 end=70.00 | load_return(?pallet=pallet_4) | 0 |
| 70 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=7 end=78.00 | load_return(?pallet=pallet_4) | 0 |
| 76 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_0) | admitted confirm_delivered_pallet(?pallet=pallet_0) | load_return(?pallet=pallet_4) | 0 |
| 92 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=95.00 | load_return(?pallet=pallet_4) | 0 |
| 95 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=2 end=98.00 | load_return(?pallet=pallet_4) | 0 |
| 98 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=5 end=104.00 | load_return(?pallet=pallet_4) | 0 |
| 104 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=11 end=116.00 | load_return(?pallet=pallet_4) | 0 |
| 110 | recognition_changed | entered | clears | office_break(?office_chair=office_chair) | admitted office_break(?office_chair=office_chair) | load_return(?pallet=pallet_4) | 0 |
| 121 | recognition_changed | retraction | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=2 end=124.00 | load_return(?pallet=pallet_4) | 0 |
| 124 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=5 end=130.00 | load_return(?pallet=pallet_4) | 0 |
| 127 | no_current_task |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=8 end=136.00 | deliver_pallet(?pallet=pallet_1) | 0 |
| 136 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=17 end=154.00 | deliver_pallet(?pallet=pallet_1) | 0 |
| 154 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=35 end=190.00 | deliver_pallet(?pallet=pallet_1) | 0 |
| 184 | no_current_task |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=3 end=188.00 | load_return(?pallet=pallet_5) | 0 |
| 188 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_1) | fallback moving k=7 end=196.00 | load_return(?pallet=pallet_5) | 0 |
| 192 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_1) | admitted confirm_delivered_pallet(?pallet=pallet_1) | load_return(?pallet=pallet_5) | 0 |
| 209 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=212.00 | load_return(?pallet=pallet_5) | 0 |
| 212 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=2 end=215.00 | load_return(?pallet=pallet_5) | 0 |
| 215 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=5 end=221.00 | load_return(?pallet=pallet_5) | 0 |
| 221 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=11 end=233.00 | load_return(?pallet=pallet_5) | 0 |
| 227 | recognition_changed | entered | clears | office_break(?office_chair=office_chair) | admitted office_break(?office_chair=office_chair) | load_return(?pallet=pallet_5) | 0 |
| 238 | recognition_changed | retraction | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=2 end=241.00 | load_return(?pallet=pallet_5) | 0 |
| 241 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=5 end=247.00 | load_return(?pallet=pallet_5) | 0 |
| 245 | no_current_task |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=9 end=255.00 | deliver_pallet(?pallet=pallet_2) | 0 |
| 255 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=19 end=275.00 | deliver_pallet(?pallet=pallet_2) | 0 |
| 275 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=39 end=315.00 | deliver_pallet(?pallet=pallet_2) | 0 |
| 294 | no_current_task |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=3 end=298.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 298 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=7 end=306.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 300 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_2) | admitted confirm_delivered_pallet(?pallet=pallet_2) | deliver_pallet(?pallet=pallet_3) | 0 |
| 319 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=322.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 322 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=2 end=325.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 325 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=5 end=331.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 331 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=11 end=343.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 340 | recognition_changed | entered | clears | office_break(?office_chair=office_chair) | admitted office_break(?office_chair=office_chair) | deliver_pallet(?pallet=pallet_3) | 0 |
| 385 | no_current_task |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback standing k=30 end=416.00 | None | 0 |
