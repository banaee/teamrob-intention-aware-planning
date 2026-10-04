# scenario_s16_03: part 4 and the measures (single_task, prior on)

Completion (world tick) 113; terminal decision 115. [sep] minimum 59.53 (27), continuous 59.53 (27); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [(36, 31), (72, 30)] (61 ticks).

## Declared properties

- **PK1off**: holds. tick 36 recognition_changed/entered admitted coffee_break hold 31
- **PK1off.stale**: holds. tick 72 recognition_changed/replaced fallback hold 30; first item_4 admission: tick 97 recognition_changed/entered admitted deliver_item(item_4) hold 0

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=1 end=2.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 2 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=3 end=6.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 6 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=7 end=14.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 14 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=15 end=30.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 30 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=31 end=41.84 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 36 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 31 |
| 72 | recognition_changed | replaced | none(below_theta) | ac_activation(?ac_switch=ac_switch_0) | fallback standing k=31 end=104.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 30 |
| 97 | recognition_changed | entered | clears | deliver_item(?item=item_4) | admitted deliver_item(?item=item_4) | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 115 | no_current_task |  | clears | deliver_item(?item=item_4) | admitted deliver_item(?item=item_4) | None | 0 |
