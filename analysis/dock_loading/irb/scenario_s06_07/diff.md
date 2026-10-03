# scenario_s06_07: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 197. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 198 | 0 |
| human_y | 198 | 0 |
| micro | 198 | 0 |
| holding | 198 | 0 |
| waited | 198 | 0 |
| obj_at | 198 | 0 |
| at | 198 | 0 |
| most_likely | 198 | 0 |
| confidence | 198 | 0 |
| finding | 198 | 0 |
| lifecycle | 198 | 0 |
| pins | 198 | 0 |
| reentries | 198 | 0 |
| boundary | 198 | 0 |
| gate | 198 | 0 |
| belief | 535 | 0 |
| S | 535 | 0 |
| member | 535 | 0 |
| adequacy | 535 | 0 |
| warrant | 535 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 198 | 0 |
| human_y | 198 | 0 |
| micro | 198 | 0 |
| most_likely | 198 | 0 |
| confidence | 198 | 0 |
| finding | 198 | 0 |
| lifecycle | 198 | 0 |
| pins | 198 | 0 |
| reentries | 198 | 0 |
| boundary | 198 | 0 |
| belief | 535 | 0 |
| S | 535 | 0 |
| member | 535 | 0 |
| adequacy | 535 | 0 |
| warrant | 535 | 0 |

Disagreements: 0

## Classification

None to classify.
