# scenario_s12_01: part 4 and the measures (single_task, prior off)

Completion (world tick) 134; terminal decision 136. [sep] minimum 53.19 (47), continuous 52.20 (47); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [(27, 5), (95, 5)] (10 ticks).

## Declared properties

- **P12.1a**: DOES NOT HOLD. winners before 27: ['item_7']; at 27: deliver_item(?item=item_7,?kitting_table=kitting_table_3), hold 5; first grasp of item_7: 26
- **P12.1b**: holds. (tick, the layout's cost difference, item_7's hold): [(0, 1.568, 0), (2, 1.568, 0), (6, 1.568, 0), (14, 1.568, 0), (27, 2.499, 5)]

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
| 27 | recognition_changed | entered | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 5 |
| 61 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=64.00 | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 64 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=2 end=67.00 | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 67 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=5 end=73.00 | deliver_item(?item=item_13,?kitting_table=kitting_table_5) | 0 |
| 73 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=11 end=85.00 | deliver_item(?item=item_13,?kitting_table=kitting_table_5) | 0 |
| 85 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=23 end=91.88 | deliver_item(?item=item_13,?kitting_table=kitting_table_5) | 0 |
| 92 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback standing k=1 end=94.00 | deliver_item(?item=item_13,?kitting_table=kitting_table_5) | 0 |
| 94 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback standing k=3 end=98.00 | deliver_item(?item=item_13,?kitting_table=kitting_table_5) | 0 |
| 95 | recognition_changed | entered | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | deliver_item(?item=item_13,?kitting_table=kitting_table_5) | 5 |
| 124 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=127.00 | deliver_item(?item=item_13,?kitting_table=kitting_table_5) | 0 |
| 127 | projection_expired |  | none(below_theta) | deliver_item(?item=item_14) | fallback moving k=2 end=130.00 | deliver_item(?item=item_13,?kitting_table=kitting_table_5) | 0 |
| 130 | projection_expired |  | none(below_theta) | deliver_item(?item=item_14) | fallback moving k=5 end=136.00 | deliver_item(?item=item_13,?kitting_table=kitting_table_5) | 0 |
| 136 | no_current_task |  | none(below_theta) | deliver_item(?item=item_14) | fallback moving k=11 end=148.00 | None | 0 |
