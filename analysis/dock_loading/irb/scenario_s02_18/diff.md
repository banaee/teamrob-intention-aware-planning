# scenario_s02_18: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 219. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 220 | 0 |
| human_y | 220 | 0 |
| micro | 220 | 0 |
| holding | 220 | 0 |
| waited | 220 | 0 |
| obj_at | 220 | 0 |
| at | 220 | 0 |
| most_likely | 220 | 0 |
| confidence | 220 | 0 |
| finding | 220 | 0 |
| lifecycle | 220 | 0 |
| pins | 220 | 0 |
| reentries | 220 | 0 |
| boundary | 220 | 0 |
| gate | 220 | 0 |
| belief | 629 | 0 |
| S | 629 | 0 |
| member | 629 | 0 |
| adequacy | 629 | 0 |
| warrant | 629 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 220 | 0 |
| human_y | 220 | 0 |
| micro | 220 | 0 |
| most_likely | 220 | 0 |
| confidence | 220 | 0 |
| finding | 220 | 0 |
| lifecycle | 220 | 0 |
| pins | 220 | 0 |
| reentries | 220 | 0 |
| boundary | 220 | 0 |
| belief | 629 | 0 |
| S | 629 | 0 |
| member | 629 | 0 |
| adequacy | 629 | 0 |
| warrant | 629 | 0 |

Disagreements: 0

## Classification

None to classify.
