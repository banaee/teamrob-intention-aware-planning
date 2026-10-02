# scenario_s09_03: part 4 and the measures (single_task, prior on)

Completion (world tick) 245; terminal decision 247. [sep] minimum 86.11 (165), continuous 85.73 (166); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

## Declared properties

None declared.

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## stand

{'stand_first_tick': 19, 'persistence_broke': 116, 'pallet_4_released': 105, 'human_at': [-244.65, 206.27], 'dry_bay': [-255, 215], 'decisions': [{'tick': 20, 'trigger': 'projection_expired', 'mode': 'standing', 'k': 5, 'end': 26.0, 'winner': 'deliver_pallet(?pallet=pallet_5)', 'hold': 0, 'holds': {'deliver_pallet(?pallet=pallet_5)': 0, 'deliver_pallet(?pallet=pallet_4)': 0, 'load_return(?pallet=pallet_6)': 0}}, {'tick': 26, 'trigger': 'projection_expired', 'mode': 'standing', 'k': 11, 'end': 38.0, 'winner': 'deliver_pallet(?pallet=pallet_5)', 'hold': 0, 'holds': {'deliver_pallet(?pallet=pallet_5)': 0, 'deliver_pallet(?pallet=pallet_4)': 0, 'load_return(?pallet=pallet_6)': 0}}, {'tick': 38, 'trigger': 'projection_expired', 'mode': 'standing', 'k': 23, 'end': 62.0, 'winner': 'deliver_pallet(?pallet=pallet_5)', 'hold': 0, 'holds': {'deliver_pallet(?pallet=pallet_5)': 0, 'deliver_pallet(?pallet=pallet_4)': 0, 'load_return(?pallet=pallet_6)': 0}}, {'tick': 59, 'trigger': 'no_current_task', 'mode': 'standing', 'k': 44, 'end': 104.0, 'winner': 'deliver_pallet(?pallet=pallet_4)', 'hold': 0, 'holds': {'deliver_pallet(?pallet=pallet_4)': 0, 'load_return(?pallet=pallet_6)': 0}}, {'tick': 104, 'trigger': 'projection_expired', 'mode': 'standing', 'k': 89, 'end': 194.0, 'winner': 'load_return(?pallet=pallet_6)', 'hold': 0, 'holds': {'deliver_pallet(?pallet=pallet_4)': 51, 'load_return(?pallet=pallet_6)': 0}}], 'holds_past_break': []}

## k3_switch

{'occurred': True, 'tick': 104}

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=1 end=2.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 2 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=3 end=6.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 6 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=7 end=14.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 14 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_0) | admitted confirm_delivered_pallet(?pallet=pallet_0) | deliver_pallet(?pallet=pallet_5) | 0 |
| 17 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=20.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 20 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=5 end=26.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 26 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=11 end=38.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 38 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=23 end=62.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 59 | no_current_task |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=44 end=104.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 104 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=89 end=194.00 | load_return(?pallet=pallet_6) | 0 |
| 194 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=44 end=239.00 | load_return(?pallet=pallet_6) | 0 |
| 198 | no_current_task |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=48 end=247.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 247 | no_current_task |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=97 end=345.00 | None | 0 |
