# scenario_s02_15: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 86. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 87 | 0 |
| human_y | 87 | 0 |
| micro | 87 | 0 |
| holding | 87 | 0 |
| waited | 87 | 0 |
| obj_at | 87 | 0 |
| at | 87 | 0 |
| most_likely | 87 | 0 |
| confidence | 87 | 0 |
| finding | 87 | 0 |
| lifecycle | 87 | 0 |
| pins | 87 | 0 |
| reentries | 87 | 0 |
| boundary | 87 | 0 |
| gate | 87 | 0 |
| belief | 202 | 0 |
| S | 202 | 0 |
| member | 202 | 0 |
| adequacy | 202 | 0 |
| warrant | 202 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 87 | 0 |
| human_y | 87 | 0 |
| micro | 87 | 0 |
| most_likely | 87 | 0 |
| confidence | 87 | 0 |
| finding | 87 | 0 |
| lifecycle | 87 | 0 |
| pins | 87 | 0 |
| reentries | 87 | 0 |
| boundary | 87 | 0 |
| belief | 202 | 0 |
| S | 202 | 0 |
| member | 202 | 0 |
| adequacy | 202 | 0 |
| warrant | 202 | 0 |

Disagreements: 0

## Classification

None to classify.
