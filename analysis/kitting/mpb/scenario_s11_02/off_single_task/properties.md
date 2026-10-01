# scenario_s11_02: part 4 and the measures (single_task, prior off)

Completion (world tick) 132; terminal decision 134. [sep] minimum 53.42 (19), continuous 53.42 (19); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [(14, 2), (20, 2), (41, 14)] (18 ticks).

## Declared properties

None declared.

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## todo132a

{'stand_first_tick': 26, 'persistence_broke': 57, 'decisions': [(32, 'recognition_changed', 8, 41.0, 0), (41, 'projection_expired', 17, 59.0, 14)], 'last_projection_end': 59.0, 'holds_past_break': []}

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | deliver_item(?item=item_10) | fallback moving k=1 end=2.00 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 0 |
| 2 | projection_expired |  | none(below_theta) | deliver_item(?item=item_10) | fallback moving k=3 end=6.00 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 0 |
| 6 | projection_expired |  | none(below_theta) | deliver_item(?item=item_10) | fallback moving k=7 end=14.00 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 0 |
| 14 | projection_expired |  | none(below_theta) | deliver_item(?item=item_10) | fallback moving k=15 end=20.00 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 2 |
| 20 | projection_expired |  | none(below_theta) | deliver_item(?item=item_10) | fallback standing k=1 end=22.00 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 2 |
| 22 | recognition_changed | entered | clears | deliver_item(?item=item_10) | admitted deliver_item(?item=item_10) | deliver_item(?item=item_11,?kitting_table=kitting_table_1) | 0 |
| 32 | recognition_changed | retraction | none(leader_inadequate) | deliver_item(?item=item_10) | fallback standing k=8 end=41.00 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 0 |
| 41 | projection_expired |  | none(leader_inadequate) | deliver_item(?item=item_10) | fallback standing k=17 end=59.00 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 14 |
| 59 | projection_expired |  | none(leader_inadequate) | deliver_item(?item=item_10) | fallback moving k=3 end=63.00 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 0 |
| 63 | projection_expired |  | none(below_theta) | deliver_item(?item=item_10) | fallback moving k=7 end=71.00 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 0 |
| 71 | projection_expired |  | none(below_theta) | deliver_item(?item=item_11) | fallback moving k=15 end=87.00 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 0 |
| 81 | no_current_task |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=25 end=97.46 | deliver_item(?item=item_11,?kitting_table=kitting_table_1) | 0 |
| 98 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=42 end=119.01 | deliver_item(?item=item_11,?kitting_table=kitting_table_1) | 0 |
| 120 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=1 end=122.00 | deliver_item(?item=item_11,?kitting_table=kitting_table_1) | 0 |
| 122 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=126.00 | deliver_item(?item=item_11,?kitting_table=kitting_table_1) | 0 |
| 126 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=7 end=134.00 | deliver_item(?item=item_11,?kitting_table=kitting_table_1) | 0 |
| 134 | no_current_task |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=15 end=150.00 | None | 0 |
