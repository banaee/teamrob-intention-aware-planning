# scenario_s08_09: part 4 and the measures (single_task, prior on)

Completion (world tick) 125; terminal decision 127. [sep] minimum 297.35 (107), continuous 297.35 (107); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

## Declared properties

None declared.

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## k9

{'admission': {'tick': 51, 'key': 'coffee_break(?coffee_machine=coffee_machine_0)', 'winner': 'deliver_pallet(?pallet=pallet_4)', 'hold': 0}, 'recorded_hypothesis_inadequate_from': 67, 'retraction': 67, 'masked_by_no_current_task': False}

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=1 end=2.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 2 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=3 end=6.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 6 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=7 end=14.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 8 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_2) | admitted confirm_delivered_pallet(?pallet=pallet_2) | deliver_pallet(?pallet=pallet_4) | 0 |
| 26 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=29.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 29 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=2 end=32.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 32 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=5 end=38.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 38 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=11 end=50.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 50 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=23 end=51.50 | deliver_pallet(?pallet=pallet_4) | 0 |
| 51 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | deliver_pallet(?pallet=pallet_4) | 0 |
| 66 | no_current_task |  | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | load_return(?pallet=pallet_6) | 0 |
| 67 | recognition_changed | retraction | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=16 end=84.00 | load_return(?pallet=pallet_6) | 0 |
| 84 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=1 end=86.00 | load_return(?pallet=pallet_6) | 0 |
| 86 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=3 end=90.00 | load_return(?pallet=pallet_6) | 0 |
| 90 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=7 end=98.00 | load_return(?pallet=pallet_6) | 0 |
| 98 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=15 end=101.60 | load_return(?pallet=pallet_6) | 0 |
| 102 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=1 end=104.00 | load_return(?pallet=pallet_6) | 0 |
| 104 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=108.00 | load_return(?pallet=pallet_6) | 0 |
| 108 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=7 end=116.00 | load_return(?pallet=pallet_6) | 0 |
| 116 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=15 end=132.00 | load_return(?pallet=pallet_6) | 0 |
| 127 | no_current_task |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=26 end=154.00 | None | 0 |
