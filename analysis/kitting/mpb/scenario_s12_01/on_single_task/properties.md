# scenario_s12_01: part 4 and the measures (single_task, prior on)

Completion (world tick) 131; terminal decision 133. [sep] minimum 87.76 (78), continuous 87.57 (79); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

## Declared properties

- **P12.1a**: holds. winners before 25: ['item_7']; at 25: deliver_item(?item=item_13,?kitting_table=kitting_table_5), hold 0; first grasp of item_7: 96
- **P12.1b**: holds. (tick, the layout's cost difference, item_7's hold): [(0, 1.568, 0), (2, 1.568, 0), (6, 1.568, 0), (14, 1.568, 0), (25, 2.499, 5)]

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=1 end=2.00 | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 2 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=3 end=6.00 | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 6 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=7 end=14.00 | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 14 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=15 end=28.91 | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 25 | recognition_changed | entered | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_13,?kitting_table=kitting_table_5) | 0 |
| 61 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=64.00 | deliver_item(?item=item_13,?kitting_table=kitting_table_5) | 0 |
| 64 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=2 end=67.00 | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 67 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=5 end=73.00 | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 73 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=11 end=85.00 | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 76 | recognition_changed | entered | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 124 | recognition_changed | replaced | none(leader_no_observation) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=127.00 | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 126 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 133 | no_current_task |  | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | None | 0 |
