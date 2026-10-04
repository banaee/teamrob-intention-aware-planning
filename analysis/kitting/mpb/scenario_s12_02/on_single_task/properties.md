# scenario_s12_02: part 4 and the measures (single_task, prior on)

Completion (world tick) 161; terminal decision 163. [sep] minimum 33.61 (139), continuous 32.26 (140); near-encounters 4 ticks; F1 classes {'viol': 1, 'stand': 2, 'recede': 1, '?': 0}; holds [(75, 18), (133, 30), (134, 7), (135, 2), (137, 4)] (61 ticks).

## Declared properties

- **P12.2a**: holds. tick 75: winner deliver_item(?item=item_14,?kitting_table=kitting_table_6), hold 18
- **P12.2b**: holds. waiting point (-166.1, -579.8), the human there 104 to 134; the robot within 50 cm of it on ticks [142] to [146]
- **P12.2c**: holds. assessed window ticks 76 to 135 (T_h 59.52678098128861); F1 violations []

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=1 end=2.00 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 2 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=3 end=6.00 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 6 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=7 end=14.00 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 14 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=15 end=28.91 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 25 | recognition_changed | entered | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 33 | no_current_task |  | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 0 |
| 61 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=64.00 | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 0 |
| 64 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=2 end=67.00 | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 0 |
| 67 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=5 end=73.00 | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 0 |
| 73 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=11 end=85.00 | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 0 |
| 75 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 18 |
| 133 | recognition_changed | replaced | none(leader_no_observation) | deliver_item(?item=item_2) | fallback standing k=31 end=165.00 | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 30 |
| 134 | recognition_changed | entered | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 7 |
| 135 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=1 end=137.00 | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 2 |
| 137 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=3 end=141.00 | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 4 |
| 140 | recognition_changed | entered | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 0 |
| 163 | no_current_task |  | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | None | 0 |
