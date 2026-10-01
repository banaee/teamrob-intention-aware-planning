# scenario_s04_12: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 171. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 172 | 0 |
| human_y | 172 | 0 |
| micro | 172 | 0 |
| holding | 172 | 0 |
| waited | 172 | 0 |
| obj_at | 172 | 0 |
| at | 172 | 0 |
| most_likely | 172 | 0 |
| confidence | 172 | 0 |
| finding | 172 | 0 |
| lifecycle | 172 | 0 |
| pins | 172 | 0 |
| reentries | 172 | 0 |
| boundary | 172 | 0 |
| gate | 172 | 0 |
| belief | 495 | 0 |
| S | 495 | 0 |
| member | 495 | 0 |
| adequacy | 495 | 0 |
| warrant | 495 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 172 | 0 |
| human_y | 172 | 0 |
| micro | 172 | 0 |
| most_likely | 172 | 0 |
| confidence | 172 | 0 |
| finding | 172 | 0 |
| lifecycle | 172 | 0 |
| pins | 172 | 0 |
| reentries | 172 | 0 |
| boundary | 172 | 0 |
| belief | 495 | 0 |
| S | 495 | 0 |
| member | 495 | 0 |
| adequacy | 495 | 0 |
| warrant | 495 | 0 |

Disagreements: 0

## Classification

None to classify.
