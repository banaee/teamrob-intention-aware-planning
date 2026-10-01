# scenario_s06_05: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 148. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 149 | 0 |
| human_y | 149 | 0 |
| micro | 149 | 0 |
| holding | 149 | 0 |
| waited | 149 | 0 |
| obj_at | 149 | 0 |
| at | 149 | 0 |
| most_likely | 149 | 0 |
| confidence | 149 | 0 |
| finding | 149 | 0 |
| lifecycle | 149 | 0 |
| pins | 149 | 0 |
| reentries | 149 | 0 |
| boundary | 149 | 0 |
| gate | 149 | 0 |
| belief | 483 | 0 |
| S | 483 | 0 |
| member | 483 | 0 |
| adequacy | 483 | 0 |
| warrant | 483 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 149 | 0 |
| human_y | 149 | 0 |
| micro | 149 | 0 |
| most_likely | 149 | 0 |
| confidence | 149 | 0 |
| finding | 149 | 0 |
| lifecycle | 149 | 0 |
| pins | 149 | 0 |
| reentries | 149 | 0 |
| boundary | 149 | 0 |
| belief | 483 | 0 |
| S | 483 | 0 |
| member | 483 | 0 |
| adequacy | 483 | 0 |
| warrant | 483 | 0 |

Disagreements: 0

## Classification

None to classify.
