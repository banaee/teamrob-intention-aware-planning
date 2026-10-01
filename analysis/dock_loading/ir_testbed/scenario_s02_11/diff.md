# scenario_s02_11: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 182. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 183 | 0 |
| human_y | 183 | 0 |
| micro | 183 | 0 |
| holding | 183 | 0 |
| waited | 183 | 0 |
| obj_at | 183 | 0 |
| at | 183 | 0 |
| most_likely | 183 | 0 |
| confidence | 183 | 0 |
| finding | 183 | 0 |
| lifecycle | 183 | 0 |
| pins | 183 | 0 |
| reentries | 183 | 0 |
| boundary | 183 | 0 |
| gate | 183 | 0 |
| belief | 524 | 0 |
| S | 524 | 0 |
| member | 524 | 0 |
| adequacy | 524 | 0 |
| warrant | 524 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 183 | 0 |
| human_y | 183 | 0 |
| micro | 183 | 0 |
| most_likely | 183 | 0 |
| confidence | 183 | 0 |
| finding | 183 | 0 |
| lifecycle | 183 | 0 |
| pins | 183 | 0 |
| reentries | 183 | 0 |
| boundary | 183 | 0 |
| belief | 524 | 0 |
| S | 524 | 0 |
| member | 524 | 0 |
| adequacy | 524 | 0 |
| warrant | 524 | 0 |

Disagreements: 0

## Classification

None to classify.
