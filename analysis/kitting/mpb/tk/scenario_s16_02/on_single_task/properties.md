# scenario_s16_02: part 4 and the measures (single_task, prior on)

Completion (world tick) 67; terminal decision 69. [sep] minimum 30.68 (49), continuous 29.33 (49); near-encounters 3 ticks; F1 classes {'viol': 2, 'stand': 0, 'recede': 1, '?': 0}; holds [(38, 4)] (4 ticks).

## Declared properties

- **PK2b**: DOES NOT HOLD. violations [48, 49]; below [48, 49, 50] (40 to 60)
- **PK2a**: holds. fallback decisions before 38: [0, 2, 6, 14, 30]; tick 38 recognition_changed/entered admitted deliver_item(item_4) hold 4

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=1 end=2.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 2 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=3 end=6.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 6 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=7 end=14.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 14 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=15 end=30.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 30 | projection_expired |  | none(below_theta) | deliver_item(?item=item_4) | fallback moving k=31 end=44.12 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 38 | recognition_changed | entered | clears | deliver_item(?item=item_4) | admitted deliver_item(?item=item_4) | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 4 |
| 69 | no_current_task |  | clears | deliver_item(?item=item_4) | admitted deliver_item(?item=item_4) | None | 0 |
