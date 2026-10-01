# scenario_s12_02: part 4 and the measures (single_task, prior off)

Completion (world tick) 184; terminal decision 186. [sep] minimum 33.61 (139), continuous 33.61 (139); near-encounters 4 ticks; F1 classes {'viol': 0, 'stand': 4, 'recede': 0, '?': 0}; holds [(91, 18), (133, 30)] (48 ticks).

## Declared properties

- **P12.2a**: holds. tick 91: winner deliver_item(?item=item_14,?kitting_table=kitting_table_6), hold 18
- **P12.2b**: holds. waiting point (-166.1, -579.8), the human there 104 to 134; the robot within 50 cm of it on ticks [165] to [169]
- **P12.2c**: holds. assessed window ticks 92 to 135 (T_h 43.52678098128861); F1 violations []

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
| 27 | recognition_changed | entered | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 33 | no_current_task |  | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 0 |
| 61 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=64.00 | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 0 |
| 64 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=2 end=67.00 | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 0 |
| 67 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=5 end=73.00 | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 0 |
| 73 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=11 end=85.00 | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 0 |
| 85 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=23 end=102.53 | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 0 |
| 91 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 18 |
| 133 | recognition_changed | replaced | none(below_theta) | deliver_item(?item=item_13) | fallback standing k=31 end=165.00 | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 30 |
| 165 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=31 end=167.89 | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 0 |
| 168 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback standing k=1 end=170.00 | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 0 |
| 170 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback standing k=3 end=174.00 | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 0 |
| 174 | recognition_changed | entered | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | deliver_item(?item=item_14,?kitting_table=kitting_table_6) | 0 |
| 186 | no_current_task |  | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | None | 0 |
