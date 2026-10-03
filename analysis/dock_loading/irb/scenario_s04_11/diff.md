# scenario_s04_11: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 185. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 186 | 0 |
| human_y | 186 | 0 |
| micro | 186 | 0 |
| holding | 186 | 0 |
| waited | 186 | 0 |
| obj_at | 186 | 0 |
| at | 186 | 0 |
| most_likely | 186 | 0 |
| confidence | 186 | 0 |
| finding | 186 | 0 |
| lifecycle | 186 | 0 |
| pins | 186 | 0 |
| reentries | 186 | 0 |
| boundary | 186 | 0 |
| gate | 186 | 0 |
| belief | 532 | 0 |
| S | 532 | 0 |
| member | 532 | 0 |
| adequacy | 532 | 0 |
| warrant | 532 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 186 | 0 |
| human_y | 186 | 0 |
| micro | 186 | 0 |
| most_likely | 186 | 0 |
| confidence | 186 | 0 |
| finding | 186 | 0 |
| lifecycle | 186 | 0 |
| pins | 186 | 0 |
| reentries | 186 | 0 |
| boundary | 186 | 0 |
| belief | 532 | 0 |
| S | 532 | 0 |
| member | 532 | 0 |
| adequacy | 532 | 0 |
| warrant | 532 | 0 |

Disagreements: 0

## Classification

None to classify.
