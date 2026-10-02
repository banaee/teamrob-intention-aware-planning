# scenario_s09_07: part 4 and the measures (full_reorder, prior on)

Completion (world tick) 265; terminal decision 267. [sep] minimum 95.33 (186), continuous 95.28 (186); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

## Declared properties

None declared.

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=1 end=2.00 | load_return(?pallet=pallet_6) | 0 |
| 2 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=3 end=6.00 | load_return(?pallet=pallet_6) | 0 |
| 6 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=7 end=14.00 | load_return(?pallet=pallet_6) | 0 |
| 14 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=15 end=15.18 | load_return(?pallet=pallet_6) | 0 |
| 16 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback standing k=1 end=18.00 | load_return(?pallet=pallet_6) | 0 |
| 18 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=22.00 | load_return(?pallet=pallet_6) | 0 |
| 22 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=4 end=27.00 | load_return(?pallet=pallet_6) | 0 |
| 25 | recognition_changed | entered | clears | office_break(?office_chair=office_chair) | admitted office_break(?office_chair=office_chair) | load_return(?pallet=pallet_6) | 0 |
| 81 | no_current_task |  | clears | office_break(?office_chair=office_chair) | admitted office_break(?office_chair=office_chair) | deliver_pallet(?pallet=pallet_4) | 0 |
| 84 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=46 end=131.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 123 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_2) | admitted confirm_delivered_pallet(?pallet=pallet_2) | deliver_pallet(?pallet=pallet_4) | 0 |
| 124 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=127.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 127 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=2 end=130.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 130 | no_current_task |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=5 end=136.00 | load_return(?pallet=pallet_7) | 0 |
| 136 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=11 end=148.00 | load_return(?pallet=pallet_7) | 0 |
| 141 | recognition_changed | entered | clears | office_break(?office_chair=office_chair) | admitted office_break(?office_chair=office_chair) | load_return(?pallet=pallet_7) | 0 |
| 149 | recognition_changed | retraction | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback moving k=24 end=166.37 | load_return(?pallet=pallet_7) | 0 |
| 167 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=1 end=169.00 | load_return(?pallet=pallet_7) | 0 |
| 169 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=3 end=173.00 | load_return(?pallet=pallet_7) | 0 |
| 173 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=7 end=181.00 | load_return(?pallet=pallet_7) | 0 |
| 181 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=15 end=197.00 | load_return(?pallet=pallet_7) | 0 |
| 197 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=31 end=229.00 | load_return(?pallet=pallet_7) | 0 |
| 218 | no_current_task |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=52 end=271.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 267 | no_current_task |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=101 end=369.00 | None | 0 |
