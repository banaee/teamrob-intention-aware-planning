# scenario_s08_04: part 4 and the measures (full_reorder, prior on)

Completion (world tick) 221; terminal decision 223. [sep] minimum 23.78 (128), continuous 21.96 (129); near-encounters 5 ticks; F1 classes {'viol': 0, 'stand': 5, 'recede': 0, '?': 0}; holds [(49, 13), (73, 48), (121, 96)] (157 ticks).

## Declared properties

None declared.

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## stand

{'stand_first_tick': 30, 'persistence_broke': 127, 'pallet_4_released': 220, 'human_at': [-498.32, 208.04], 'dry_bay': [-515, 215], 'decisions': [{'tick': 31, 'trigger': 'projection_expired', 'mode': 'standing', 'k': 5, 'end': 37.0, 'winner': 'deliver_pallet(?pallet=pallet_4)', 'hold': 0, 'holds': {}}, {'tick': 37, 'trigger': 'projection_expired', 'mode': 'standing', 'k': 11, 'end': 49.0, 'winner': 'deliver_pallet(?pallet=pallet_4)', 'hold': 0, 'holds': {}}, {'tick': 49, 'trigger': 'projection_expired', 'mode': 'standing', 'k': 23, 'end': 73.0, 'winner': 'deliver_pallet(?pallet=pallet_4)', 'hold': 13, 'holds': {}}, {'tick': 73, 'trigger': 'projection_expired', 'mode': 'standing', 'k': 47, 'end': 121.0, 'winner': 'deliver_pallet(?pallet=pallet_4)', 'hold': 48, 'holds': {}}, {'tick': 121, 'trigger': 'projection_expired', 'mode': 'standing', 'k': 95, 'end': 217.0, 'winner': 'deliver_pallet(?pallet=pallet_4)', 'hold': 96, 'holds': {}}], 'holds_past_break': [(121, 96)]}

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=1 end=2.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 2 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=3 end=6.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 6 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=7 end=14.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 14 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_0) | admitted confirm_delivered_pallet(?pallet=pallet_0) | deliver_pallet(?pallet=pallet_4) | 0 |
| 28 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=31.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 31 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=5 end=37.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 37 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=11 end=49.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 49 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=23 end=73.00 | deliver_pallet(?pallet=pallet_4) | 13 |
| 73 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=47 end=121.00 | deliver_pallet(?pallet=pallet_4) | 48 |
| 121 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=95 end=217.00 | deliver_pallet(?pallet=pallet_4) | 96 |
| 217 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=46 end=264.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 223 | no_current_task |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=52 end=276.00 | None | 0 |
