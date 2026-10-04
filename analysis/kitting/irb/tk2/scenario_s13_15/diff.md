# scenario_s13_15: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 427. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 428 | 0 |
| human_y | 428 | 0 |
| micro | 428 | 0 |
| holding | 428 | 0 |
| waited | 428 | 0 |
| obj_at | 428 | 0 |
| at | 428 | 0 |
| most_likely | 428 | 0 |
| confidence | 428 | 0 |
| finding | 428 | 0 |
| lifecycle | 428 | 0 |
| pins | 428 | 0 |
| reentries | 428 | 0 |
| boundary | 428 | 0 |
| gate | 428 | 0 |
| levels | 428 | 0 |
| recent | 428 | 0 |
| prior | 1202 | 0 |
| belief | 1202 | 0 |
| belief_h | 1202 | 0 |
| S | 1202 | 0 |
| member | 1202 | 0 |
| adequacy | 1202 | 0 |
| warrant | 1202 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 428 | 0 |
| human_y | 428 | 0 |
| micro | 428 | 0 |
| most_likely | 428 | 0 |
| confidence | 428 | 0 |
| finding | 428 | 0 |
| lifecycle | 428 | 0 |
| pins | 428 | 0 |
| reentries | 428 | 0 |
| boundary | 428 | 0 |
| levels | 428 | 0 |
| recent | 428 | 0 |
| prior | 1202 | 0 |
| belief | 1202 | 0 |
| S | 1202 | 0 |
| member | 1202 | 0 |
| adequacy | 1202 | 0 |
| warrant | 1202 | 0 |

Disagreements: 0

## Classification

None to classify.
