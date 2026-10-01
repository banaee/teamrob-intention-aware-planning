# scenario_s02_02: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 138. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 139 | 0 |
| human_y | 139 | 0 |
| micro | 139 | 0 |
| holding | 139 | 0 |
| waited | 139 | 0 |
| obj_at | 139 | 0 |
| at | 139 | 0 |
| most_likely | 139 | 0 |
| confidence | 139 | 0 |
| finding | 139 | 0 |
| lifecycle | 139 | 0 |
| pins | 139 | 0 |
| reentries | 139 | 0 |
| boundary | 139 | 0 |
| gate | 139 | 0 |
| belief | 387 | 0 |
| S | 387 | 0 |
| member | 387 | 0 |
| adequacy | 387 | 0 |
| warrant | 387 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 139 | 0 |
| human_y | 139 | 0 |
| micro | 139 | 0 |
| most_likely | 139 | 0 |
| confidence | 139 | 0 |
| finding | 139 | 0 |
| lifecycle | 139 | 0 |
| pins | 139 | 0 |
| reentries | 139 | 0 |
| boundary | 139 | 0 |
| belief | 387 | 0 |
| S | 387 | 0 |
| member | 387 | 0 |
| adequacy | 387 | 0 |
| warrant | 387 | 0 |

Disagreements: 0

## Classification

None to classify.
