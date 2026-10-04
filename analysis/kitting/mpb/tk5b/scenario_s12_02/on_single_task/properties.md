# scenario_s12_02: part 4 and the measures (single_task, prior on)

Completion (world tick) 162; terminal decision 164. [sep] minimum 33.61 (139), continuous 33.61 (139); near-encounters 4 ticks; F1 classes {'viol': 0, 'stand': 3, 'recede': 1, '?': 0}; holds [(93, 18), (133, 30), (134, 7)] (55 ticks).

## Declared properties

- **P12.2a**: holds. tick 93: winner deliver_item(?item=item_14,?kitting_table=kitting_table_6), hold 18
- **P12.2b**: holds. waiting point (-166.1, -579.8), the human there 104 to 134; the robot within 50 cm of it on ticks [143] to [147]
- **P12.2c**: holds. assessed window ticks 94 to 135 (T_h 41.52678098128861); F1 violations []

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=1 end=2.00 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 2 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=3 end=6.00 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 6 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=7 end=14.00 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 8 | recognition_changed | entered | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 33 | no_current_task |  | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 0 |
| 61 | recognition_changed | replaced | none(leader_no_observation) | deliver_item(?item=item_2) | fallback standing k=2 end=64.00 | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 0 |
| 62 | recognition_changed | entered | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 0 |
| 84 | recognition_changed | retraction | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=22 end=102.53 | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 0 |
| 93 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 18 |
| 133 | recognition_changed | replaced | none(leader_no_observation) | deliver_item(?item=item_2) | fallback standing k=31 end=165.00 | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 30 |
| 134 | recognition_changed | entered | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 7 |
| 164 | no_current_task |  | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | None | 0 |
