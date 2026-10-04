# scenario_s13_09: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 429. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 430 | 0 |
| human_y | 430 | 0 |
| micro | 430 | 0 |
| holding | 430 | 0 |
| waited | 430 | 0 |
| obj_at | 430 | 0 |
| at | 430 | 0 |
| most_likely | 430 | 0 |
| confidence | 430 | 0 |
| finding | 430 | 0 |
| lifecycle | 430 | 0 |
| pins | 430 | 0 |
| reentries | 430 | 0 |
| boundary | 430 | 0 |
| gate | 430 | 0 |
| levels | 430 | 0 |
| recent | 430 | 0 |
| prior | 1344 | 0 |
| belief | 1344 | 0 |
| belief_h | 1344 | 0 |
| S | 1344 | 0 |
| member | 1344 | 0 |
| adequacy | 1344 | 0 |
| warrant | 1344 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 430 | 0 |
| human_y | 430 | 0 |
| micro | 430 | 0 |
| most_likely | 430 | 0 |
| confidence | 430 | 0 |
| finding | 430 | 0 |
| lifecycle | 430 | 0 |
| pins | 430 | 0 |
| reentries | 430 | 0 |
| boundary | 430 | 0 |
| levels | 430 | 0 |
| recent | 430 | 0 |
| prior | 1344 | 0 |
| belief | 1344 | 0 |
| S | 1344 | 0 |
| member | 1344 | 0 |
| adequacy | 1344 | 0 |
| warrant | 1344 | 0 |

Disagreements: 0

## Classification

None to classify.
