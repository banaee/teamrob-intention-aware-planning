# scenario_s09_04: part 4 and the measures (single_task, prior on)

Completion (world tick) 211; terminal decision 213. [sep] minimum 33.81 (118), continuous 33.80 (119); near-encounters 4 ticks; F1 classes {'viol': 0, 'stand': 4, 'recede': 0, '?': 0}; holds [(38, 10), (62, 48), (110, 96)] (154 ticks).

## Declared properties

None declared.

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## stand

{'stand_first_tick': 19, 'persistence_broke': 116, 'pallet_4_released': 210, 'human_at': [-244.65, 206.27], 'dry_bay': [-255, 215], 'decisions': [{'tick': 20, 'trigger': 'projection_expired', 'mode': 'standing', 'k': 5, 'end': 26.0, 'winner': 'deliver_pallet(?pallet=pallet_4)', 'hold': 0, 'holds': {'deliver_pallet(?pallet=pallet_4)': 0}}, {'tick': 26, 'trigger': 'projection_expired', 'mode': 'standing', 'k': 11, 'end': 38.0, 'winner': 'deliver_pallet(?pallet=pallet_4)', 'hold': 0, 'holds': {'deliver_pallet(?pallet=pallet_4)': 0}}, {'tick': 38, 'trigger': 'projection_expired', 'mode': 'standing', 'k': 23, 'end': 62.0, 'winner': 'deliver_pallet(?pallet=pallet_4)', 'hold': 10, 'holds': {'deliver_pallet(?pallet=pallet_4)': 10}}, {'tick': 62, 'trigger': 'projection_expired', 'mode': 'standing', 'k': 47, 'end': 110.0, 'winner': 'deliver_pallet(?pallet=pallet_4)', 'hold': 48, 'holds': {'deliver_pallet(?pallet=pallet_4)': 48}}, {'tick': 110, 'trigger': 'projection_expired', 'mode': 'standing', 'k': 95, 'end': 206.0, 'winner': 'deliver_pallet(?pallet=pallet_4)', 'hold': 96, 'holds': {'deliver_pallet(?pallet=pallet_4)': 96}}], 'holds_past_break': [(110, 96)]}

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
| 110 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=95 end=206.00 | deliver_pallet(?pallet=pallet_4) | 96 |
| 206 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=56 end=263.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 213 | no_current_task |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=63 end=277.00 | None | 0 |
