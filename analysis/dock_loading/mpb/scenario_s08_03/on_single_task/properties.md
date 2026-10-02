# scenario_s08_03: part 4 and the measures (single_task, prior on)

Completion (world tick) 213; terminal decision 215. [sep] minimum 242.49 (109), continuous 242.47 (109); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

## Declared properties

None declared.

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## stand

{'stand_first_tick': 30, 'persistence_broke': 127, 'pallet_4_released': 212, 'human_at': [-498.32, 208.04], 'dry_bay': [-515, 215], 'decisions': [{'tick': 31, 'trigger': 'projection_expired', 'mode': 'standing', 'k': 5, 'end': 37.0, 'winner': 'deliver_pallet(?pallet=pallet_5)', 'hold': 0, 'holds': {'deliver_pallet(?pallet=pallet_5)': 0, 'deliver_pallet(?pallet=pallet_4)': 0, 'load_return(?pallet=pallet_6)': 0}}, {'tick': 37, 'trigger': 'projection_expired', 'mode': 'standing', 'k': 11, 'end': 49.0, 'winner': 'deliver_pallet(?pallet=pallet_5)', 'hold': 0, 'holds': {'deliver_pallet(?pallet=pallet_5)': 0, 'deliver_pallet(?pallet=pallet_4)': 0, 'load_return(?pallet=pallet_6)': 0}}, {'tick': 49, 'trigger': 'projection_expired', 'mode': 'standing', 'k': 23, 'end': 73.0, 'winner': 'deliver_pallet(?pallet=pallet_5)', 'hold': 0, 'holds': {'deliver_pallet(?pallet=pallet_5)': 0, 'deliver_pallet(?pallet=pallet_4)': 0, 'load_return(?pallet=pallet_6)': 0}}, {'tick': 60, 'trigger': 'no_current_task', 'mode': 'standing', 'k': 34, 'end': 95.0, 'winner': 'load_return(?pallet=pallet_6)', 'hold': 0, 'holds': {'deliver_pallet(?pallet=pallet_4)': 0, 'load_return(?pallet=pallet_6)': 0}}, {'tick': 95, 'trigger': 'projection_expired', 'mode': 'standing', 'k': 69, 'end': 165.0, 'winner': 'load_return(?pallet=pallet_6)', 'hold': 0, 'holds': {'load_return(?pallet=pallet_6)': 0, 'deliver_pallet(?pallet=pallet_4)': 0}}], 'holds_past_break': []}

## k3_switch

{'occurred': False, 'tick': None}

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=1 end=2.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 2 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=3 end=6.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 6 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=7 end=14.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 14 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_0) | admitted confirm_delivered_pallet(?pallet=pallet_0) | deliver_pallet(?pallet=pallet_5) | 0 |
| 28 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=31.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 31 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=5 end=37.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 37 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=11 end=49.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 49 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=23 end=73.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 60 | no_current_task |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=34 end=95.00 | load_return(?pallet=pallet_6) | 0 |
| 95 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=69 end=165.00 | load_return(?pallet=pallet_6) | 0 |
| 159 | no_current_task |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=33 end=171.77 | deliver_pallet(?pallet=pallet_4) | 0 |
| 172 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=1 end=174.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 174 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=3 end=178.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 178 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=7 end=186.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 186 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=15 end=202.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 202 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=31 end=234.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 215 | no_current_task |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=44 end=260.00 | None | 0 |
