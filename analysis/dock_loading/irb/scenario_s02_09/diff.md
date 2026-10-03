# scenario_s02_09: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 243. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 244 | 0 |
| human_y | 244 | 0 |
| micro | 244 | 0 |
| holding | 244 | 0 |
| waited | 244 | 0 |
| obj_at | 244 | 0 |
| at | 244 | 0 |
| most_likely | 244 | 0 |
| confidence | 244 | 0 |
| finding | 244 | 0 |
| lifecycle | 244 | 0 |
| pins | 244 | 0 |
| reentries | 244 | 0 |
| boundary | 244 | 0 |
| gate | 244 | 0 |
| belief | 806 | 0 |
| S | 806 | 0 |
| member | 806 | 0 |
| adequacy | 806 | 0 |
| warrant | 806 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 244 | 0 |
| human_y | 244 | 0 |
| micro | 244 | 0 |
| most_likely | 244 | 0 |
| confidence | 244 | 0 |
| finding | 244 | 0 |
| lifecycle | 244 | 0 |
| pins | 244 | 0 |
| reentries | 244 | 0 |
| boundary | 244 | 0 |
| belief | 806 | 0 |
| S | 806 | 0 |
| member | 806 | 0 |
| adequacy | 806 | 0 |
| warrant | 806 | 0 |

Disagreements: 0

## Classification

None to classify.
