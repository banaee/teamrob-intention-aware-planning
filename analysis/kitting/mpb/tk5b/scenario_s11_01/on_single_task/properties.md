# scenario_s11_01: part 4 and the measures (single_task, prior on)

Completion (world tick) 76; terminal decision 78. [sep] minimum 66.17 (58), continuous 66.15 (58); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [(34, 24)] (24 ticks).

## Declared properties

- **P6.1**: DOES NOT HOLD. switch at 16 (recognition_changed); first grasp of item_8: 66; the human standing: True
- **P6.2**: holds. (tick, the layout's cost difference, item_8's hold): [(0, 3.5, 0), (16, 3.582, 10)]

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | clears | deliver_item(?item=item_12) | admitted deliver_item(?item=item_12) | deliver_item(?item=item_8,?kitting_table=kitting_table_2) | 0 |
| 16 | recognition_changed | retraction | none(leader_inadequate) | deliver_item(?item=item_12) | fallback standing k=17 end=34.00 | deliver_item(?item=item_9,?kitting_table=kitting_table_4) | 0 |
| 34 | no_current_task |  | none(leader_inadequate) | deliver_item(?item=item_12) | fallback standing k=35 end=70.00 | deliver_item(?item=item_8,?kitting_table=kitting_table_2) | 24 |
| 70 | projection_expired |  | none(leader_inadequate) | deliver_item(?item=item_12) | fallback moving k=10 end=81.00 | deliver_item(?item=item_8,?kitting_table=kitting_table_2) | 0 |
| 78 | no_current_task |  | none(leader_inadequate) | deliver_item(?item=item_12) | fallback moving k=18 end=97.00 | None | 0 |
