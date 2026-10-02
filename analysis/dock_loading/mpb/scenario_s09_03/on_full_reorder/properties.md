# scenario_s09_03: part 4 and the measures (full_reorder, prior on)

Completion (world tick) 347; terminal decision 349. [sep] minimum 69.64 (61), continuous 69.64 (61); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [(38, 10), (62, 48)] (58 ticks).

## Declared properties

None declared.

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## stand

{'stand_first_tick': 19, 'persistence_broke': 116, 'pallet_4_released': 150, 'human_at': [-244.65, 206.27], 'dry_bay': [-255, 215], 'decisions': [{'tick': 20, 'trigger': 'projection_expired', 'mode': 'standing', 'k': 5, 'end': 26.0, 'winner': 'deliver_pallet(?pallet=pallet_4)', 'hold': 0, 'holds': {}}, {'tick': 26, 'trigger': 'projection_expired', 'mode': 'standing', 'k': 11, 'end': 38.0, 'winner': 'deliver_pallet(?pallet=pallet_4)', 'hold': 0, 'holds': {}}, {'tick': 38, 'trigger': 'projection_expired', 'mode': 'standing', 'k': 23, 'end': 62.0, 'winner': 'deliver_pallet(?pallet=pallet_4)', 'hold': 10, 'holds': {}}, {'tick': 62, 'trigger': 'projection_expired', 'mode': 'standing', 'k': 47, 'end': 110.0, 'winner': 'deliver_pallet(?pallet=pallet_4)', 'hold': 48, 'holds': {}}, {'tick': 110, 'trigger': 'projection_expired', 'mode': 'standing', 'k': 95, 'end': 206.0, 'winner': 'deliver_pallet(?pallet=pallet_5)', 'hold': 0, 'holds': {}}], 'holds_past_break': []}

## k3_switch

{'occurred': True, 'tick': 110}

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=1 end=2.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 2 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=3 end=6.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 6 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=7 end=14.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 14 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_0) | admitted confirm_delivered_pallet(?pallet=pallet_0) | deliver_pallet(?pallet=pallet_4) | 0 |
| 17 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=20.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 20 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=5 end=26.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 26 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=11 end=38.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 38 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=23 end=62.00 | deliver_pallet(?pallet=pallet_4) | 10 |
| 62 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=47 end=110.00 | deliver_pallet(?pallet=pallet_4) | 48 |
| 110 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=95 end=206.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 201 | no_current_task |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=51 end=253.00 | load_return(?pallet=pallet_6) | 0 |
| 253 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=103 end=357.00 | load_return(?pallet=pallet_6) | 0 |
| 300 | no_current_task |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=150 end=451.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 349 | no_current_task |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=199 end=549.00 | None | 0 |
