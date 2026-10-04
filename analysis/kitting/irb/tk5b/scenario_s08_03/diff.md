# scenario_s08_03: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 270. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 271 | 0 |
| human_y | 271 | 0 |
| micro | 271 | 0 |
| holding | 271 | 0 |
| waited | 271 | 0 |
| obj_at | 271 | 0 |
| at | 271 | 0 |
| most_likely | 271 | 0 |
| confidence | 271 | 0 |
| finding | 271 | 0 |
| lifecycle | 271 | 0 |
| pins | 271 | 0 |
| reentries | 271 | 0 |
| boundary | 271 | 0 |
| gate | 271 | 0 |
| levels | 271 | 0 |
| recent | 271 | 0 |
| prior | 587 | 0 |
| belief | 587 | 0 |
| belief_h | 587 | 0 |
| S | 587 | 0 |
| member | 587 | 0 |
| adequacy | 587 | 0 |
| warrant | 587 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 271 | 0 |
| human_y | 271 | 0 |
| micro | 271 | 0 |
| most_likely | 271 | 0 |
| confidence | 271 | 0 |
| finding | 271 | 0 |
| lifecycle | 271 | 0 |
| pins | 271 | 0 |
| reentries | 271 | 0 |
| boundary | 271 | 0 |
| levels | 271 | 0 |
| recent | 271 | 0 |
| prior | 587 | 0 |
| belief | 587 | 0 |
| S | 587 | 0 |
| member | 587 | 0 |
| adequacy | 587 | 0 |
| warrant | 587 | 0 |

Disagreements: 0

## Classification

None to classify.
