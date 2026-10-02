# scenario_s02_16: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 330. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 331 | 0 |
| human_y | 331 | 0 |
| micro | 331 | 0 |
| holding | 331 | 0 |
| waited | 331 | 0 |
| obj_at | 331 | 0 |
| at | 331 | 0 |
| most_likely | 331 | 0 |
| confidence | 331 | 0 |
| finding | 331 | 0 |
| lifecycle | 331 | 0 |
| pins | 331 | 0 |
| reentries | 331 | 0 |
| boundary | 331 | 0 |
| gate | 331 | 0 |
| belief | 1092 | 0 |
| S | 1092 | 0 |
| member | 1092 | 0 |
| adequacy | 1092 | 0 |
| warrant | 1092 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 331 | 0 |
| human_y | 331 | 0 |
| micro | 331 | 0 |
| most_likely | 331 | 0 |
| confidence | 331 | 0 |
| finding | 331 | 0 |
| lifecycle | 331 | 0 |
| pins | 331 | 0 |
| reentries | 331 | 0 |
| boundary | 331 | 0 |
| belief | 1092 | 0 |
| S | 1092 | 0 |
| member | 1092 | 0 |
| adequacy | 1092 | 0 |
| warrant | 1092 | 0 |

Disagreements: 0

## Classification

None to classify.
