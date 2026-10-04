# scenario_s09_12: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 204. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 205 | 0 |
| human_y | 205 | 0 |
| micro | 205 | 0 |
| holding | 205 | 0 |
| waited | 205 | 0 |
| obj_at | 205 | 0 |
| at | 205 | 0 |
| most_likely | 205 | 0 |
| confidence | 205 | 0 |
| finding | 205 | 0 |
| lifecycle | 205 | 0 |
| pins | 205 | 0 |
| reentries | 205 | 0 |
| boundary | 205 | 0 |
| gate | 205 | 0 |
| belief | 390 | 0 |
| belief_h | 390 | 0 |
| S | 390 | 0 |
| member | 390 | 0 |
| adequacy | 390 | 0 |
| warrant | 390 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 205 | 0 |
| human_y | 205 | 0 |
| micro | 205 | 0 |
| most_likely | 205 | 0 |
| confidence | 205 | 0 |
| finding | 205 | 0 |
| lifecycle | 205 | 0 |
| pins | 205 | 0 |
| reentries | 205 | 0 |
| boundary | 205 | 0 |
| belief | 390 | 0 |
| S | 390 | 0 |
| member | 390 | 0 |
| adequacy | 390 | 0 |
| warrant | 390 | 0 |

Disagreements: 0

## Classification

None to classify.
