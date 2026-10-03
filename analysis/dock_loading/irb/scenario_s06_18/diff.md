# scenario_s06_18: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 203. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 204 | 0 |
| human_y | 204 | 0 |
| micro | 204 | 0 |
| holding | 204 | 0 |
| waited | 204 | 0 |
| obj_at | 204 | 0 |
| at | 204 | 0 |
| most_likely | 204 | 0 |
| confidence | 204 | 0 |
| finding | 204 | 0 |
| lifecycle | 204 | 0 |
| pins | 204 | 0 |
| reentries | 204 | 0 |
| boundary | 204 | 0 |
| gate | 204 | 0 |
| belief | 553 | 0 |
| S | 553 | 0 |
| member | 553 | 0 |
| adequacy | 553 | 0 |
| warrant | 553 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 204 | 0 |
| human_y | 204 | 0 |
| micro | 204 | 0 |
| most_likely | 204 | 0 |
| confidence | 204 | 0 |
| finding | 204 | 0 |
| lifecycle | 204 | 0 |
| pins | 204 | 0 |
| reentries | 204 | 0 |
| boundary | 204 | 0 |
| belief | 553 | 0 |
| S | 553 | 0 |
| member | 553 | 0 |
| adequacy | 553 | 0 |
| warrant | 553 | 0 |

Disagreements: 0

## Classification

None to classify.
