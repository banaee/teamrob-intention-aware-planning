# scenario_s10_06: part 4 and the measures (single_task, prior off)

Completion (world tick) 161; terminal decision 163. [sep] minimum 349.00 (47), continuous 349.00 (47); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

## Declared properties

- **P8a**: holds. holds []
- **P8b**: holds. completion 161, the reference's 161
- **P8c**: holds. ticks where the robot's positions differ: []

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=1 end=2.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 2 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=3 end=6.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 6 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=7 end=14.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 14 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=15 end=28.91 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 20 | recognition_changed | entered | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 29 | no_current_task |  | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 61 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=64.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 64 | projection_expired |  | none(below_theta) | deliver_item(?item=item_7) | fallback moving k=2 end=67.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 67 | no_current_task |  | none(below_theta) | deliver_item(?item=item_7) | fallback moving k=5 end=73.00 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 73 | projection_expired |  | none(below_theta) | deliver_item(?item=item_7) | fallback moving k=11 end=85.00 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 85 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=23 end=109.00 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 91 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 94 | recognition_changed | retraction | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=32 end=109.52 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 110 | no_current_task |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=1 end=112.00 | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 112 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=116.00 | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 116 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=7 end=124.00 | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 124 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=15 end=140.00 | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 140 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=31 end=172.00 | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 163 | no_current_task |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=54 end=218.00 | None | 0 |
