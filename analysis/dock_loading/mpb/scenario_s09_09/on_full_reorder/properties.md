# scenario_s09_09: part 4 and the measures (full_reorder, prior on)

Completion (world tick) 128; terminal decision 130. [sep] minimum 241.74 (95), continuous 241.74 (95); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

## Declared properties

None declared.

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## k9

{'admission': {'tick': 37, 'key': 'office_break(?office_chair=office_chair)', 'winner': 'load_return(?pallet=pallet_6)', 'hold': 0}, 'recorded_hypothesis_inadequate_from': 59, 'retraction': 59, 'masked_by_no_current_task': False}

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=1 end=2.00 | load_return(?pallet=pallet_6) | 0 |
| 2 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=3 end=6.00 | load_return(?pallet=pallet_6) | 0 |
| 6 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=7 end=14.00 | load_return(?pallet=pallet_6) | 0 |
| 14 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=15 end=24.31 | load_return(?pallet=pallet_6) | 0 |
| 21 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_2) | admitted confirm_delivered_pallet(?pallet=pallet_2) | load_return(?pallet=pallet_6) | 0 |
| 26 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=29.00 | load_return(?pallet=pallet_6) | 0 |
| 29 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=2 end=32.00 | load_return(?pallet=pallet_6) | 0 |
| 32 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=5 end=38.00 | load_return(?pallet=pallet_6) | 0 |
| 37 | recognition_changed | entered | clears | office_break(?office_chair=office_chair) | admitted office_break(?office_chair=office_chair) | load_return(?pallet=pallet_6) | 0 |
| 59 | recognition_changed | retraction | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=8 end=68.00 | load_return(?pallet=pallet_6) | 0 |
| 68 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=17 end=86.00 | load_return(?pallet=pallet_6) | 0 |
| 81 | no_current_task |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=30 end=112.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 112 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=9 end=122.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 122 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=19 end=142.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 130 | no_current_task |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=27 end=158.00 | None | 0 |
