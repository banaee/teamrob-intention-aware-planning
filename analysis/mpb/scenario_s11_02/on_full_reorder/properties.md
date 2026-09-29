# scenario_s11_02: part 4 and the measures (full_reorder, prior on)

Completion (world tick) 99; terminal decision 101. [sep] minimum 146.80 (14), continuous 146.77 (15); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

## Declared properties

None declared.

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## todo132a

{'stand_first_tick': 26, 'persistence_broke': 57, 'decisions': [(32, 'recognition_changed', 8, 41.0, 0), (41, 'projection_expired', 17, 59.0, 0)], 'last_projection_end': 59.0, 'holds_past_break': []}

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | deliver_item(?item=item_10) | fallback moving k=1 end=2.00 | deliver_item(?item=item_11,?kitting_table=kitting_table_1) | 0 |
| 2 | projection_expired |  | none(below_theta) | deliver_item(?item=item_10) | fallback moving k=3 end=6.00 | deliver_item(?item=item_11,?kitting_table=kitting_table_1) | 0 |
| 6 | projection_expired |  | none(below_theta) | deliver_item(?item=item_10) | fallback moving k=7 end=14.00 | deliver_item(?item=item_11,?kitting_table=kitting_table_1) | 0 |
| 14 | projection_expired |  | none(below_theta) | deliver_item(?item=item_10) | fallback moving k=15 end=20.00 | deliver_item(?item=item_11,?kitting_table=kitting_table_1) | 0 |
| 20 | projection_expired |  | none(below_theta) | deliver_item(?item=item_10) | fallback standing k=1 end=22.00 | deliver_item(?item=item_11,?kitting_table=kitting_table_1) | 0 |
| 22 | recognition_changed | entered | clears | deliver_item(?item=item_10) | admitted deliver_item(?item=item_10) | deliver_item(?item=item_11,?kitting_table=kitting_table_1) | 0 |
| 32 | recognition_changed | retraction | none(leader_inadequate) | deliver_item(?item=item_10) | fallback standing k=8 end=41.00 | deliver_item(?item=item_11,?kitting_table=kitting_table_1) | 0 |
| 41 | projection_expired |  | none(leader_inadequate) | deliver_item(?item=item_10) | fallback standing k=17 end=59.00 | deliver_item(?item=item_11,?kitting_table=kitting_table_1) | 0 |
| 58 | no_current_task |  | none(leader_inadequate) | deliver_item(?item=item_10) | fallback moving k=2 end=61.00 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 0 |
| 61 | projection_expired |  | none(leader_inadequate) | deliver_item(?item=item_10) | fallback moving k=5 end=67.00 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 0 |
| 67 | projection_expired |  | none(below_theta) | deliver_item(?item=item_10) | fallback moving k=11 end=79.00 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 0 |
| 79 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=23 end=97.46 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 0 |
| 98 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=42 end=119.01 | deliver_item(?item=item_10,?kitting_table=kitting_table_1) | 0 |
| 101 | no_current_task |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=45 end=119.01 | None | 0 |
