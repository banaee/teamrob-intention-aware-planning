# scenario_s08_06: part 4 and the measures (full_reorder, prior on)

Completion (world tick) 253; terminal decision 255. [sep] minimum 97.23 (235), continuous 96.89 (236); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [(141, 7)] (7 ticks).

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
| 14 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_0) | admitted confirm_delivered_pallet(?pallet=pallet_0) | load_return(?pallet=pallet_6) | 0 |
| 28 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=31.00 | load_return(?pallet=pallet_6) | 0 |
| 31 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=2 end=34.00 | load_return(?pallet=pallet_6) | 0 |
| 34 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=5 end=40.00 | load_return(?pallet=pallet_6) | 0 |
| 40 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=11 end=50.95 | load_return(?pallet=pallet_6) | 0 |
| 43 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | load_return(?pallet=pallet_6) | 0 |
| 81 | no_current_task |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback standing k=31 end=113.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 103 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_2) | admitted confirm_delivered_pallet(?pallet=pallet_2) | deliver_pallet(?pallet=pallet_4) | 0 |
| 130 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=133.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 133 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=2 end=136.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 136 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=5 end=142.00 | load_return(?pallet=pallet_7) | 0 |
| 141 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | load_return(?pallet=pallet_7) | 7 |
| 159 | recognition_changed | retraction | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=13 end=173.00 | load_return(?pallet=pallet_7) | 0 |
| 173 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=27 end=201.00 | load_return(?pallet=pallet_7) | 0 |
| 201 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=55 end=257.00 | load_return(?pallet=pallet_7) | 0 |
| 205 | no_current_task |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=59 end=265.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 255 | no_current_task |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=109 end=365.00 | None | 0 |
