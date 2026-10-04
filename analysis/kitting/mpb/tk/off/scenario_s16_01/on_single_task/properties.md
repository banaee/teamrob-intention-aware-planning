# scenario_s16_01: part 4 and the measures (single_task, prior on)

Completion (world tick) 69; terminal decision 71. [sep] minimum 36.95 (48), continuous 36.95 (48); near-encounters 7 ticks; F1 classes {'viol': 1, 'stand': 6, 'recede': 0, '?': 0}; holds [(45, 2), (47, 4)] (6 ticks).

## Declared properties

- **PK3off**: holds. first admission: tick 47 recognition_changed/entered admitted deliver_item(item_4) hold 4
- **PK3off.sep**: holds. ticks below min_separation in 40 to 60: [44, 45, 46, 47, 48, 49, 50]

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | deliver_item(?item=item_4) | fallback moving k=1 end=2.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 2 | projection_expired |  | none(below_theta) | deliver_item(?item=item_4) | fallback moving k=3 end=6.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 6 | projection_expired |  | none(below_theta) | deliver_item(?item=item_4) | fallback moving k=7 end=14.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 14 | projection_expired |  | none(below_theta) | deliver_item(?item=item_4) | fallback moving k=15 end=30.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 30 | projection_expired |  | none(below_theta) | deliver_item(?item=item_4) | fallback moving k=31 end=44.12 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 45 | projection_expired |  | none(below_theta) | deliver_item(?item=item_4) | fallback standing k=1 end=47.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 2 |
| 47 | recognition_changed | entered | clears | deliver_item(?item=item_4) | admitted deliver_item(?item=item_4) | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 4 |
| 71 | no_current_task |  | clears | deliver_item(?item=item_4) | admitted deliver_item(?item=item_4) | None | 0 |
