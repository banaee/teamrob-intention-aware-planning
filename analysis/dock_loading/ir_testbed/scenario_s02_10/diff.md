# scenario_s02_10: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 110. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 111 | 0 |
| human_y | 111 | 0 |
| micro | 111 | 0 |
| holding | 111 | 0 |
| waited | 111 | 0 |
| obj_at | 111 | 0 |
| at | 111 | 0 |
| most_likely | 111 | 0 |
| confidence | 111 | 0 |
| finding | 111 | 0 |
| lifecycle | 111 | 0 |
| pins | 111 | 0 |
| reentries | 111 | 0 |
| boundary | 111 | 0 |
| gate | 111 | 0 |
| belief | 386 | 0 |
| S | 386 | 0 |
| member | 386 | 0 |
| adequacy | 386 | 0 |
| warrant | 386 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 111 | 0 |
| human_y | 111 | 0 |
| micro | 111 | 0 |
| most_likely | 111 | 0 |
| confidence | 111 | 0 |
| finding | 111 | 0 |
| lifecycle | 111 | 0 |
| pins | 111 | 0 |
| reentries | 111 | 0 |
| boundary | 111 | 0 |
| belief | 386 | 0 |
| S | 386 | 0 |
| member | 386 | 0 |
| adequacy | 386 | 0 |
| warrant | 386 | 0 |

Disagreements: 0

## Classification

None to classify.
