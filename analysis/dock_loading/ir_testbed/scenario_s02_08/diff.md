# scenario_s02_08: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 271. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 272 | 0 |
| human_y | 272 | 0 |
| micro | 272 | 0 |
| holding | 272 | 0 |
| waited | 272 | 0 |
| obj_at | 272 | 0 |
| at | 272 | 0 |
| most_likely | 272 | 0 |
| confidence | 272 | 0 |
| finding | 272 | 0 |
| lifecycle | 272 | 0 |
| pins | 272 | 0 |
| reentries | 272 | 0 |
| boundary | 272 | 0 |
| gate | 272 | 0 |
| belief | 917 | 0 |
| S | 917 | 0 |
| member | 917 | 0 |
| adequacy | 917 | 0 |
| warrant | 917 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 272 | 0 |
| human_y | 272 | 0 |
| micro | 272 | 0 |
| most_likely | 272 | 0 |
| confidence | 272 | 0 |
| finding | 272 | 0 |
| lifecycle | 272 | 0 |
| pins | 272 | 0 |
| reentries | 272 | 0 |
| boundary | 272 | 0 |
| belief | 917 | 0 |
| S | 917 | 0 |
| member | 917 | 0 |
| adequacy | 917 | 0 |
| warrant | 917 | 0 |

Disagreements: 0

## Classification

None to classify.
