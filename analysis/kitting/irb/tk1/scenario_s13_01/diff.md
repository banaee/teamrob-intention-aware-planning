# scenario_s13_01: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 360. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 361 | 0 |
| human_y | 361 | 0 |
| micro | 361 | 0 |
| holding | 361 | 0 |
| waited | 361 | 0 |
| obj_at | 361 | 0 |
| at | 361 | 0 |
| most_likely | 361 | 0 |
| confidence | 361 | 0 |
| finding | 361 | 0 |
| lifecycle | 361 | 0 |
| pins | 361 | 0 |
| reentries | 361 | 0 |
| boundary | 361 | 0 |
| gate | 361 | 0 |
| belief | 1070 | 0 |
| belief_h | 1070 | 0 |
| S | 1070 | 0 |
| member | 1070 | 0 |
| adequacy | 1070 | 0 |
| warrant | 1070 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 361 | 0 |
| human_y | 361 | 0 |
| micro | 361 | 0 |
| most_likely | 361 | 0 |
| confidence | 361 | 0 |
| finding | 361 | 0 |
| lifecycle | 361 | 0 |
| pins | 361 | 0 |
| reentries | 361 | 0 |
| boundary | 361 | 0 |
| belief | 1070 | 0 |
| S | 1070 | 0 |
| member | 1070 | 0 |
| adequacy | 1070 | 0 |
| warrant | 1070 | 0 |

Disagreements: 0

## Classification

None to classify.
