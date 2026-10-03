# scenario_s15_04: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 408. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 409 | 0 |
| human_y | 409 | 0 |
| micro | 409 | 0 |
| holding | 409 | 0 |
| waited | 409 | 0 |
| obj_at | 409 | 0 |
| at | 409 | 0 |
| most_likely | 409 | 0 |
| confidence | 409 | 0 |
| finding | 409 | 0 |
| lifecycle | 409 | 0 |
| pins | 409 | 0 |
| reentries | 409 | 0 |
| boundary | 409 | 0 |
| gate | 409 | 0 |
| belief | 1573 | 0 |
| S | 1573 | 0 |
| member | 1573 | 0 |
| adequacy | 1573 | 0 |
| warrant | 1573 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 409 | 0 |
| human_y | 409 | 0 |
| micro | 409 | 0 |
| most_likely | 409 | 0 |
| confidence | 409 | 0 |
| finding | 409 | 0 |
| lifecycle | 409 | 0 |
| pins | 409 | 0 |
| reentries | 409 | 0 |
| boundary | 409 | 0 |
| belief | 1573 | 0 |
| S | 1573 | 0 |
| member | 1573 | 0 |
| adequacy | 1573 | 0 |
| warrant | 1573 | 0 |

Disagreements: 0

## Classification

None to classify.
