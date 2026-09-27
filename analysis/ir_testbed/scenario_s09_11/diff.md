# scenario_s09_11: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 275. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 276 | 0 |
| human_y | 276 | 0 |
| micro | 276 | 0 |
| holding | 276 | 0 |
| waited | 276 | 0 |
| obj_at | 276 | 0 |
| at | 276 | 0 |
| most_likely | 276 | 0 |
| confidence | 276 | 0 |
| finding | 276 | 0 |
| lifecycle | 276 | 0 |
| pins | 276 | 0 |
| reentries | 276 | 0 |
| boundary | 276 | 0 |
| belief | 530 | 0 |
| S | 530 | 0 |
| member | 530 | 0 |
| adequacy | 530 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 276 | 0 |
| human_y | 276 | 0 |
| micro | 276 | 0 |
| most_likely | 276 | 0 |
| confidence | 276 | 0 |
| finding | 276 | 0 |
| lifecycle | 276 | 0 |
| pins | 276 | 0 |
| reentries | 276 | 0 |
| boundary | 276 | 0 |
| belief | 530 | 0 |
| S | 530 | 0 |
| member | 530 | 0 |
| adequacy | 530 | 0 |

Disagreements: 0

## Classification

None to classify.
