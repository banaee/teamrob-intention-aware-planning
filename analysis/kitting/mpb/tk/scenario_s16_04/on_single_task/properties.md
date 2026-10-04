# scenario_s16_04: part 4 and the measures (single_task, prior on)

Completion (world tick) 90; terminal decision 92. [sep] minimum 68.48 (26), continuous 68.48 (26); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [(22, 32), (72, 29)] (61 ticks).

## Declared properties

- **PK1b**: holds. item_4 after the break: tick 73 recognition_changed/entered admitted deliver_item(item_4) hold 0; decisions on a fallback stand after 72: []
- **PK1c**: holds. violations in 38 to 75: []
- **PK1a**: holds. fallback decisions before 22: [0, 2, 6, 14]; tick 22 recognition_changed/entered admitted coffee_break hold 32

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
| 22 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 32 |
| 72 | recognition_changed | replaced | none(leader_no_observation) | deliver_item(?item=item_4) | fallback standing k=31 end=104.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 29 |
| 73 | recognition_changed | entered | clears | deliver_item(?item=item_4) | admitted deliver_item(?item=item_4) | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 92 | no_current_task |  | clears | deliver_item(?item=item_4) | admitted deliver_item(?item=item_4) | None | 0 |
