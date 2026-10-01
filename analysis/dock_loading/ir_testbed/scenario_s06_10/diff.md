# scenario_s06_10: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 106. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 107 | 0 |
| human_y | 107 | 0 |
| micro | 107 | 0 |
| holding | 107 | 0 |
| waited | 107 | 0 |
| obj_at | 107 | 0 |
| at | 107 | 0 |
| most_likely | 107 | 0 |
| confidence | 107 | 0 |
| finding | 107 | 0 |
| lifecycle | 107 | 0 |
| pins | 107 | 0 |
| reentries | 107 | 0 |
| boundary | 107 | 0 |
| gate | 107 | 0 |
| belief | 354 | 0 |
| S | 354 | 0 |
| member | 354 | 0 |
| adequacy | 354 | 0 |
| warrant | 354 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 107 | 0 |
| human_y | 107 | 0 |
| micro | 107 | 0 |
| most_likely | 107 | 0 |
| confidence | 107 | 0 |
| finding | 107 | 0 |
| lifecycle | 107 | 0 |
| pins | 107 | 0 |
| reentries | 107 | 0 |
| boundary | 107 | 0 |
| belief | 354 | 0 |
| S | 354 | 0 |
| member | 354 | 0 |
| adequacy | 354 | 0 |
| warrant | 354 | 0 |

Disagreements: 0

## Classification

None to classify.
