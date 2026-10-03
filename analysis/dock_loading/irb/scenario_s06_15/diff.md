# scenario_s06_15: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 82. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 83 | 0 |
| human_y | 83 | 0 |
| micro | 83 | 0 |
| holding | 83 | 0 |
| waited | 83 | 0 |
| obj_at | 83 | 0 |
| at | 83 | 0 |
| most_likely | 83 | 0 |
| confidence | 83 | 0 |
| finding | 83 | 0 |
| lifecycle | 83 | 0 |
| pins | 83 | 0 |
| reentries | 83 | 0 |
| boundary | 83 | 0 |
| gate | 83 | 0 |
| belief | 192 | 0 |
| S | 192 | 0 |
| member | 192 | 0 |
| adequacy | 192 | 0 |
| warrant | 192 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 83 | 0 |
| human_y | 83 | 0 |
| micro | 83 | 0 |
| most_likely | 83 | 0 |
| confidence | 83 | 0 |
| finding | 83 | 0 |
| lifecycle | 83 | 0 |
| pins | 83 | 0 |
| reentries | 83 | 0 |
| boundary | 83 | 0 |
| belief | 192 | 0 |
| S | 192 | 0 |
| member | 192 | 0 |
| adequacy | 192 | 0 |
| warrant | 192 | 0 |

Disagreements: 0

## Classification

None to classify.
