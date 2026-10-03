# scenario_s04_13: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 130. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 131 | 0 |
| human_y | 131 | 0 |
| micro | 131 | 0 |
| holding | 131 | 0 |
| waited | 131 | 0 |
| obj_at | 131 | 0 |
| at | 131 | 0 |
| most_likely | 131 | 0 |
| confidence | 131 | 0 |
| finding | 131 | 0 |
| lifecycle | 131 | 0 |
| pins | 131 | 0 |
| reentries | 131 | 0 |
| boundary | 131 | 0 |
| gate | 131 | 0 |
| belief | 475 | 0 |
| S | 475 | 0 |
| member | 475 | 0 |
| adequacy | 475 | 0 |
| warrant | 475 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 131 | 0 |
| human_y | 131 | 0 |
| micro | 131 | 0 |
| most_likely | 131 | 0 |
| confidence | 131 | 0 |
| finding | 131 | 0 |
| lifecycle | 131 | 0 |
| pins | 131 | 0 |
| reentries | 131 | 0 |
| boundary | 131 | 0 |
| belief | 475 | 0 |
| S | 475 | 0 |
| member | 475 | 0 |
| adequacy | 475 | 0 |
| warrant | 475 | 0 |

Disagreements: 0

## Classification

None to classify.
