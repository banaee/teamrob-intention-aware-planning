# scenario_s02_07: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 200. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 201 | 0 |
| human_y | 201 | 0 |
| micro | 201 | 0 |
| holding | 201 | 0 |
| waited | 201 | 0 |
| obj_at | 201 | 0 |
| at | 201 | 0 |
| most_likely | 201 | 0 |
| confidence | 201 | 0 |
| finding | 201 | 0 |
| lifecycle | 201 | 0 |
| pins | 201 | 0 |
| reentries | 201 | 0 |
| boundary | 201 | 0 |
| gate | 201 | 0 |
| belief | 571 | 0 |
| S | 571 | 0 |
| member | 571 | 0 |
| adequacy | 571 | 0 |
| warrant | 571 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 201 | 0 |
| human_y | 201 | 0 |
| micro | 201 | 0 |
| most_likely | 201 | 0 |
| confidence | 201 | 0 |
| finding | 201 | 0 |
| lifecycle | 201 | 0 |
| pins | 201 | 0 |
| reentries | 201 | 0 |
| boundary | 201 | 0 |
| belief | 571 | 0 |
| S | 571 | 0 |
| member | 571 | 0 |
| adequacy | 571 | 0 |
| warrant | 571 | 0 |

Disagreements: 0

## Classification

None to classify.
