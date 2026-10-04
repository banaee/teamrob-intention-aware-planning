# scenario_s11_02: part 4 and the measures (single_task, prior on)

Completion (world tick) 169; terminal decision 171. [sep] minimum 50.44 (24), continuous 50.44 (24); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [(14, 2), (20, 2), (25, 2), (27, 4), (31, 8), (39, 16), (55, 32)] (66 ticks).

## Declared properties

None declared.

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## todo132a

{'stand_first_tick': 26, 'persistence_broke': 57, 'decisions': [(27, 'projection_expired', 3, 31.0, 4), (31, 'projection_expired', 7, 39.0, 8), (39, 'projection_expired', 15, 55.0, 16), (55, 'projection_expired', 31, 87.0, 32)], 'last_projection_end': 87.0, 'holds_past_break': [(55, 32)]}

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(leader_unwarranted) | deliver_item(?item=item_12) | fallback moving k=1 end=2.00 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 0 |
| 2 | projection_expired |  | none(leader_unwarranted) | deliver_item(?item=item_12) | fallback moving k=3 end=6.00 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 0 |
| 6 | projection_expired |  | none(leader_unwarranted) | deliver_item(?item=item_12) | fallback moving k=7 end=14.00 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 0 |
| 14 | projection_expired |  | none(leader_inadequate) | deliver_item(?item=item_12) | fallback moving k=15 end=20.00 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 2 |
| 20 | projection_expired |  | none(leader_inadequate) | deliver_item(?item=item_12) | fallback standing k=1 end=22.00 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 2 |
| 22 | projection_expired |  | none(leader_inadequate) | deliver_item(?item=item_12) | fallback moving k=2 end=24.22 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 0 |
| 25 | projection_expired |  | none(leader_inadequate) | deliver_item(?item=item_12) | fallback standing k=1 end=27.00 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 2 |
| 27 | projection_expired |  | none(leader_inadequate) | deliver_item(?item=item_12) | fallback standing k=3 end=31.00 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 4 |
| 31 | projection_expired |  | none(leader_inadequate) | deliver_item(?item=item_12) | fallback standing k=7 end=39.00 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 8 |
| 39 | projection_expired |  | none(leader_inadequate) | deliver_item(?item=item_12) | fallback standing k=15 end=55.00 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 16 |
| 55 | projection_expired |  | none(leader_inadequate) | deliver_item(?item=item_12) | fallback standing k=31 end=87.00 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 32 |
| 87 | projection_expired |  | none(leader_inadequate) | deliver_item(?item=item_12) | fallback moving k=31 end=97.46 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 0 |
| 98 | projection_expired |  | none(leader_inadequate) | deliver_item(?item=item_12) | fallback moving k=42 end=119.01 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 0 |
| 118 | no_current_task |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=62 end=119.01 | deliver_item(?item=item_11,?kitting_table=kitting_table_1) | 0 |
| 120 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=1 end=122.00 | deliver_item(?item=item_11,?kitting_table=kitting_table_1) | 0 |
| 122 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=126.00 | deliver_item(?item=item_11,?kitting_table=kitting_table_1) | 0 |
| 126 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=7 end=134.00 | deliver_item(?item=item_11,?kitting_table=kitting_table_1) | 0 |
| 134 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=15 end=150.00 | deliver_item(?item=item_11,?kitting_table=kitting_table_1) | 0 |
| 150 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=31 end=182.00 | deliver_item(?item=item_11,?kitting_table=kitting_table_1) | 0 |
| 171 | no_current_task |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=52 end=224.00 | None | 0 |
