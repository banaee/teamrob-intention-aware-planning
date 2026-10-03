# scenario_s06_09: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 184. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 185 | 0 |
| human_y | 185 | 0 |
| micro | 185 | 0 |
| holding | 185 | 0 |
| waited | 185 | 0 |
| obj_at | 185 | 0 |
| at | 185 | 0 |
| most_likely | 185 | 0 |
| confidence | 185 | 0 |
| finding | 185 | 0 |
| lifecycle | 185 | 0 |
| pins | 185 | 0 |
| reentries | 185 | 0 |
| boundary | 185 | 0 |
| gate | 185 | 0 |
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
| human_x | 185 | 0 |
| human_y | 185 | 0 |
| micro | 185 | 0 |
| most_likely | 185 | 0 |
| confidence | 185 | 0 |
| finding | 185 | 0 |
| lifecycle | 185 | 0 |
| pins | 185 | 0 |
| reentries | 185 | 0 |
| boundary | 185 | 0 |
| belief | 571 | 0 |
| S | 571 | 0 |
| member | 571 | 0 |
| adequacy | 571 | 0 |
| warrant | 571 | 0 |

Disagreements: 0

## Classification

None to classify.
