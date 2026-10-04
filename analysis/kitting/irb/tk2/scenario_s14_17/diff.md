# scenario_s14_17: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 347. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 348 | 0 |
| human_y | 348 | 0 |
| micro | 348 | 0 |
| holding | 348 | 0 |
| waited | 348 | 0 |
| obj_at | 348 | 0 |
| at | 348 | 0 |
| most_likely | 348 | 0 |
| confidence | 348 | 0 |
| finding | 348 | 0 |
| lifecycle | 348 | 0 |
| pins | 348 | 0 |
| reentries | 348 | 0 |
| boundary | 348 | 0 |
| gate | 348 | 0 |
| levels | 348 | 0 |
| recent | 348 | 0 |
| prior | 1265 | 0 |
| belief | 1265 | 0 |
| belief_h | 1265 | 0 |
| S | 1265 | 0 |
| member | 1265 | 0 |
| adequacy | 1265 | 0 |
| warrant | 1265 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 348 | 0 |
| human_y | 348 | 0 |
| micro | 348 | 0 |
| most_likely | 348 | 0 |
| confidence | 348 | 0 |
| finding | 348 | 0 |
| lifecycle | 348 | 0 |
| pins | 348 | 0 |
| reentries | 348 | 0 |
| boundary | 348 | 0 |
| levels | 348 | 0 |
| recent | 348 | 0 |
| prior | 1265 | 0 |
| belief | 1265 | 0 |
| S | 1265 | 0 |
| member | 1265 | 0 |
| adequacy | 1265 | 0 |
| warrant | 1265 | 0 |

Disagreements: 0

## Classification

None to classify.
