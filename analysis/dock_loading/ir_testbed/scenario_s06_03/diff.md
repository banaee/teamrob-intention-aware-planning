# scenario_s06_03: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 113. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 114 | 0 |
| human_y | 114 | 0 |
| micro | 114 | 0 |
| holding | 114 | 0 |
| waited | 114 | 0 |
| obj_at | 114 | 0 |
| at | 114 | 0 |
| most_likely | 114 | 0 |
| confidence | 114 | 0 |
| finding | 114 | 0 |
| lifecycle | 114 | 0 |
| pins | 114 | 0 |
| reentries | 114 | 0 |
| boundary | 114 | 0 |
| gate | 114 | 0 |
| belief | 299 | 0 |
| S | 299 | 0 |
| member | 299 | 0 |
| adequacy | 299 | 0 |
| warrant | 299 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 114 | 0 |
| human_y | 114 | 0 |
| micro | 114 | 0 |
| most_likely | 114 | 0 |
| confidence | 114 | 0 |
| finding | 114 | 0 |
| lifecycle | 114 | 0 |
| pins | 114 | 0 |
| reentries | 114 | 0 |
| boundary | 114 | 0 |
| belief | 299 | 0 |
| S | 299 | 0 |
| member | 299 | 0 |
| adequacy | 299 | 0 |
| warrant | 299 | 0 |

Disagreements: 0

## Classification

None to classify.
