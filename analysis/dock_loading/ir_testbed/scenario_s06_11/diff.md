# scenario_s06_11: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 121. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 122 | 0 |
| human_y | 122 | 0 |
| micro | 122 | 0 |
| holding | 122 | 0 |
| waited | 122 | 0 |
| obj_at | 122 | 0 |
| at | 122 | 0 |
| most_likely | 122 | 0 |
| confidence | 122 | 0 |
| finding | 122 | 0 |
| lifecycle | 122 | 0 |
| pins | 122 | 0 |
| reentries | 122 | 0 |
| boundary | 122 | 0 |
| gate | 122 | 0 |
| belief | 330 | 0 |
| S | 330 | 0 |
| member | 330 | 0 |
| adequacy | 330 | 0 |
| warrant | 330 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 122 | 0 |
| human_y | 122 | 0 |
| micro | 122 | 0 |
| most_likely | 122 | 0 |
| confidence | 122 | 0 |
| finding | 122 | 0 |
| lifecycle | 122 | 0 |
| pins | 122 | 0 |
| reentries | 122 | 0 |
| boundary | 122 | 0 |
| belief | 330 | 0 |
| S | 330 | 0 |
| member | 330 | 0 |
| adequacy | 330 | 0 |
| warrant | 330 | 0 |

Disagreements: 0

## Classification

None to classify.
