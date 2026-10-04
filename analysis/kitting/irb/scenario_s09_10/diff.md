# scenario_s09_10: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 187. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 188 | 0 |
| human_y | 188 | 0 |
| micro | 188 | 0 |
| holding | 188 | 0 |
| waited | 188 | 0 |
| obj_at | 188 | 0 |
| at | 188 | 0 |
| most_likely | 188 | 0 |
| confidence | 188 | 0 |
| finding | 188 | 0 |
| lifecycle | 188 | 0 |
| pins | 188 | 0 |
| reentries | 188 | 0 |
| boundary | 188 | 0 |
| gate | 188 | 0 |
| levels | 188 | 0 |
| recent | 188 | 0 |
| prior | 356 | 0 |
| belief | 356 | 0 |
| belief_h | 356 | 0 |
| S | 356 | 0 |
| member | 356 | 0 |
| adequacy | 356 | 0 |
| warrant | 356 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 188 | 0 |
| human_y | 188 | 0 |
| micro | 188 | 0 |
| most_likely | 188 | 0 |
| confidence | 188 | 0 |
| finding | 188 | 0 |
| lifecycle | 188 | 0 |
| pins | 188 | 0 |
| reentries | 188 | 0 |
| boundary | 188 | 0 |
| levels | 188 | 0 |
| recent | 188 | 0 |
| prior | 356 | 0 |
| belief | 356 | 0 |
| S | 356 | 0 |
| member | 356 | 0 |
| adequacy | 356 | 0 |
| warrant | 356 | 0 |

Disagreements: 0

## Classification

None to classify.
