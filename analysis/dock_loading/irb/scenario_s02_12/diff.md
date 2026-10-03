# scenario_s02_12: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 179. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 180 | 0 |
| human_y | 180 | 0 |
| micro | 180 | 0 |
| holding | 180 | 0 |
| waited | 180 | 0 |
| obj_at | 180 | 0 |
| at | 180 | 0 |
| most_likely | 180 | 0 |
| confidence | 180 | 0 |
| finding | 180 | 0 |
| lifecycle | 180 | 0 |
| pins | 180 | 0 |
| reentries | 180 | 0 |
| boundary | 180 | 0 |
| gate | 180 | 0 |
| belief | 510 | 0 |
| S | 510 | 0 |
| member | 510 | 0 |
| adequacy | 510 | 0 |
| warrant | 510 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 180 | 0 |
| human_y | 180 | 0 |
| micro | 180 | 0 |
| most_likely | 180 | 0 |
| confidence | 180 | 0 |
| finding | 180 | 0 |
| lifecycle | 180 | 0 |
| pins | 180 | 0 |
| reentries | 180 | 0 |
| boundary | 180 | 0 |
| belief | 510 | 0 |
| S | 510 | 0 |
| member | 510 | 0 |
| adequacy | 510 | 0 |
| warrant | 510 | 0 |

Disagreements: 0

## Classification

None to classify.
