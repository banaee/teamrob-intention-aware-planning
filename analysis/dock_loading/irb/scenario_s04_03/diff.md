# scenario_s04_03: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 157. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 158 | 0 |
| human_y | 158 | 0 |
| micro | 158 | 0 |
| holding | 158 | 0 |
| waited | 158 | 0 |
| obj_at | 158 | 0 |
| at | 158 | 0 |
| most_likely | 158 | 0 |
| confidence | 158 | 0 |
| finding | 158 | 0 |
| lifecycle | 158 | 0 |
| pins | 158 | 0 |
| reentries | 158 | 0 |
| boundary | 158 | 0 |
| gate | 158 | 0 |
| belief | 422 | 0 |
| S | 422 | 0 |
| member | 422 | 0 |
| adequacy | 422 | 0 |
| warrant | 422 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 158 | 0 |
| human_y | 158 | 0 |
| micro | 158 | 0 |
| most_likely | 158 | 0 |
| confidence | 158 | 0 |
| finding | 158 | 0 |
| lifecycle | 158 | 0 |
| pins | 158 | 0 |
| reentries | 158 | 0 |
| boundary | 158 | 0 |
| belief | 422 | 0 |
| S | 422 | 0 |
| member | 422 | 0 |
| adequacy | 422 | 0 |
| warrant | 422 | 0 |

Disagreements: 0

## Classification

None to classify.
