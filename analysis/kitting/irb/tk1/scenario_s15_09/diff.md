# scenario_s15_09: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 375. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 376 | 0 |
| human_y | 376 | 0 |
| micro | 376 | 0 |
| holding | 376 | 0 |
| waited | 376 | 0 |
| obj_at | 376 | 0 |
| at | 376 | 0 |
| most_likely | 376 | 0 |
| confidence | 376 | 0 |
| finding | 376 | 0 |
| lifecycle | 376 | 0 |
| pins | 376 | 0 |
| reentries | 376 | 0 |
| boundary | 376 | 0 |
| gate | 376 | 0 |
| levels | 376 | 0 |
| recent | 376 | 0 |
| prior | 1487 | 0 |
| belief | 1487 | 0 |
| belief_h | 1487 | 0 |
| S | 1487 | 0 |
| member | 1487 | 0 |
| adequacy | 1487 | 0 |
| warrant | 1487 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 376 | 0 |
| human_y | 376 | 0 |
| micro | 376 | 0 |
| most_likely | 376 | 0 |
| confidence | 376 | 0 |
| finding | 376 | 0 |
| lifecycle | 376 | 0 |
| pins | 376 | 0 |
| reentries | 376 | 0 |
| boundary | 376 | 0 |
| levels | 376 | 0 |
| recent | 376 | 0 |
| prior | 1487 | 0 |
| belief | 1487 | 0 |
| S | 1487 | 0 |
| member | 1487 | 0 |
| adequacy | 1487 | 0 |
| warrant | 1487 | 0 |

Disagreements: 0

## Classification

None to classify.
