# scenario_s12_01: part 4 and the measures (single_task, prior on)

Completion (world tick) 130; terminal decision 132. [sep] minimum 72.46 (78), continuous 72.14 (78); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

## Declared properties

- **P12.1a**: holds. winners before 8: ['item_7']; at 8: deliver_item(?item=item_13,?kitting_table=kitting_table_5), hold 0; first grasp of item_7: 95
- **P12.1b**: holds. (tick, the layout's cost difference, item_7's hold): [(0, 1.568, 0), (2, 1.568, 0), (6, 1.568, 0), (8, 1.568, 5)]

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=1 end=2.00 | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 2 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=3 end=6.00 | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 6 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=7 end=14.00 | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 8 | recognition_changed | entered | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_13,?kitting_table=kitting_table_5) | 0 |
| 61 | recognition_changed | replaced | none(leader_no_observation) | deliver_item(?item=item_2) | fallback standing k=2 end=64.00 | deliver_item(?item=item_13,?kitting_table=kitting_table_5) | 0 |
| 62 | recognition_changed | entered | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | deliver_item(?item=item_13,?kitting_table=kitting_table_5) | 0 |
| 65 | no_current_task |  | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 124 | recognition_changed | replaced | none(leader_no_observation) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=127.00 | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 126 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 132 | no_current_task |  | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | None | 0 |
