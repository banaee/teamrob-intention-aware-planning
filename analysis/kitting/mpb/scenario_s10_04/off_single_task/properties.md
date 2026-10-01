# scenario_s10_04: part 4 and the measures (single_task, prior off)

Completion (world tick) 161; terminal decision 163. [sep] minimum 383.99 (59), continuous 383.99 (59); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

## Declared properties

None declared.

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=1 end=2.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 2 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=3 end=6.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 6 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=7 end=14.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 14 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=15 end=28.91 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 26 | recognition_changed | entered | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 29 | no_current_task |  | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 61 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=64.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 64 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=2 end=67.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 67 | no_current_task |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=5 end=73.00 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 73 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=11 end=85.00 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 85 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=23 end=102.53 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 86 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 110 | no_current_task |  | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 133 | recognition_changed | replaced | none(below_theta) | deliver_item(?item=item_2) | fallback standing k=31 end=165.00 | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 158 | recognition_changed | entered | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 163 | no_current_task |  | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | None | 0 |
