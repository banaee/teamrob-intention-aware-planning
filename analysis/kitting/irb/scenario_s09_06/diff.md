# scenario_s09_06: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 245. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 246 | 0 |
| human_y | 246 | 0 |
| micro | 246 | 0 |
| holding | 246 | 0 |
| waited | 246 | 0 |
| obj_at | 246 | 0 |
| at | 246 | 0 |
| most_likely | 246 | 0 |
| confidence | 246 | 0 |
| finding | 246 | 0 |
| lifecycle | 246 | 0 |
| pins | 246 | 0 |
| reentries | 246 | 0 |
| boundary | 246 | 0 |
| gate | 246 | 0 |
| belief | 515 | 0 |
| belief_h | 515 | 0 |
| S | 515 | 0 |
| member | 515 | 0 |
| adequacy | 515 | 0 |
| warrant | 515 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 246 | 0 |
| human_y | 246 | 0 |
| micro | 246 | 0 |
| most_likely | 246 | 0 |
| confidence | 246 | 0 |
| finding | 246 | 0 |
| lifecycle | 246 | 0 |
| pins | 246 | 0 |
| reentries | 246 | 0 |
| boundary | 246 | 0 |
| belief | 515 | 0 |
| S | 515 | 0 |
| member | 515 | 0 |
| adequacy | 515 | 0 |
| warrant | 515 | 0 |

Disagreements: 0

## Classification

None to classify.
