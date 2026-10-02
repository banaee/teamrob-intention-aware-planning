# scenario_s08_01: part 4 and the measures (single_task, prior on)

Completion (world tick) 125; terminal decision 127. [sep] minimum 331.36 (107), continuous 331.36 (107); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

## Declared properties

- **P1a**: holds. holds []
- **P1b**: holds. completion 125, the reference's 125
- **P1c**: holds. ticks where the robot's positions differ: []

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

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
| 37 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | deliver_pallet(?pallet=pallet_4) | 0 |
| 55 | recognition_changed | retraction | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=13 end=69.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 66 | no_current_task |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=24 end=91.00 | load_return(?pallet=pallet_6) | 0 |
| 91 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=49 end=141.00 | load_return(?pallet=pallet_6) | 0 |
| 127 | no_current_task |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=85 end=213.00 | None | 0 |
