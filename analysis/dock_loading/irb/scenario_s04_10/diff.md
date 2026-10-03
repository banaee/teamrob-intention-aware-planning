# scenario_s04_10: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 100. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 101 | 0 |
| human_y | 101 | 0 |
| micro | 101 | 0 |
| holding | 101 | 0 |
| waited | 101 | 0 |
| obj_at | 101 | 0 |
| at | 101 | 0 |
| most_likely | 101 | 0 |
| confidence | 101 | 0 |
| finding | 101 | 0 |
| lifecycle | 101 | 0 |
| pins | 101 | 0 |
| reentries | 101 | 0 |
| boundary | 101 | 0 |
| gate | 101 | 0 |
| belief | 356 | 0 |
| S | 356 | 0 |
| member | 356 | 0 |
| adequacy | 356 | 0 |
| warrant | 356 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 101 | 0 |
| human_y | 101 | 0 |
| micro | 101 | 0 |
| most_likely | 101 | 0 |
| confidence | 101 | 0 |
| finding | 101 | 0 |
| lifecycle | 101 | 0 |
| pins | 101 | 0 |
| reentries | 101 | 0 |
| boundary | 101 | 0 |
| belief | 356 | 0 |
| S | 356 | 0 |
| member | 356 | 0 |
| adequacy | 356 | 0 |
| warrant | 356 | 0 |

Disagreements: 0

## Classification

None to classify.
