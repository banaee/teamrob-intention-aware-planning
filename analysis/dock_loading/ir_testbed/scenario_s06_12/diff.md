# scenario_s06_12: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 151. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 152 | 0 |
| human_y | 152 | 0 |
| micro | 152 | 0 |
| holding | 152 | 0 |
| waited | 152 | 0 |
| obj_at | 152 | 0 |
| at | 152 | 0 |
| most_likely | 152 | 0 |
| confidence | 152 | 0 |
| finding | 152 | 0 |
| lifecycle | 152 | 0 |
| pins | 152 | 0 |
| reentries | 152 | 0 |
| boundary | 152 | 0 |
| gate | 152 | 0 |
| belief | 399 | 0 |
| S | 399 | 0 |
| member | 399 | 0 |
| adequacy | 399 | 0 |
| warrant | 399 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 152 | 0 |
| human_y | 152 | 0 |
| micro | 152 | 0 |
| most_likely | 152 | 0 |
| confidence | 152 | 0 |
| finding | 152 | 0 |
| lifecycle | 152 | 0 |
| pins | 152 | 0 |
| reentries | 152 | 0 |
| boundary | 152 | 0 |
| belief | 399 | 0 |
| S | 399 | 0 |
| member | 399 | 0 |
| adequacy | 399 | 0 |
| warrant | 399 | 0 |

Disagreements: 0

## Classification

None to classify.
