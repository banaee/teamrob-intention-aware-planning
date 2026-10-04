# scenario_s16_03: part 4 and the measures (single_task, prior on)

Completion (world tick) 89; terminal decision 91. [sep] minimum 55.51 (43), continuous 55.51 (43); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [(42, 1), (44, 4), (48, 8), (55, 33), (72, 32), (74, 1)] (79 ticks).

## Declared properties

- **PK4a.r**: holds. tick 0 no_current_task/None fallback hold 0 gate none(leader_outranked); first admission: tick 55 recognition_changed/entered admitted coffee_break hold 33
- **PK4b.r**: holds. retraction decisions before 55: []
- **PK4d**: holds. next admission: tick 55 recognition_changed/entered admitted coffee_break hold 33
- **PK4e.r**: holds. item_4 after the break: tick 74 recognition_changed/entered admitted deliver_item(item_4) hold 1; decisions on a fallback stand after 72: []

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(leader_outranked) | deliver_item(?item=item_4) | fallback moving k=1 end=2.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 2 | projection_expired |  | none(leader_outranked) | deliver_item(?item=item_4) | fallback moving k=3 end=6.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 6 | projection_expired |  | none(leader_outranked) | deliver_item(?item=item_4) | fallback moving k=7 end=14.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 14 | projection_expired |  | none(leader_outranked) | deliver_item(?item=item_4) | fallback moving k=15 end=30.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 30 | projection_expired |  | none(leader_outranked) | deliver_item(?item=item_4) | fallback moving k=31 end=41.84 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 42 | projection_expired |  | none(leader_outranked) | deliver_item(?item=item_4) | fallback standing k=1 end=44.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 1 |
| 44 | projection_expired |  | none(below_theta) | deliver_item(?item=item_4) | fallback standing k=3 end=48.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 4 |
| 48 | projection_expired |  | none(below_theta) | deliver_item(?item=item_4) | fallback standing k=7 end=56.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 8 |
| 55 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 33 |
| 72 | recognition_changed | replaced | none(leader_no_observation) | deliver_item(?item=item_4) | fallback standing k=31 end=104.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 32 |
| 74 | recognition_changed | entered | clears | deliver_item(?item=item_4) | admitted deliver_item(?item=item_4) | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 1 |
| 91 | no_current_task |  | clears | deliver_item(?item=item_4) | admitted deliver_item(?item=item_4) | None | 0 |
