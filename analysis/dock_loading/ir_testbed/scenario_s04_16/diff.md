# scenario_s04_16: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 268. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 269 | 0 |
| human_y | 269 | 0 |
| micro | 269 | 0 |
| holding | 269 | 0 |
| waited | 269 | 0 |
| obj_at | 269 | 0 |
| at | 269 | 0 |
| most_likely | 269 | 0 |
| confidence | 269 | 0 |
| finding | 269 | 0 |
| lifecycle | 269 | 0 |
| pins | 269 | 0 |
| reentries | 269 | 0 |
| boundary | 269 | 0 |
| gate | 269 | 0 |
| belief | 857 | 0 |
| S | 857 | 0 |
| member | 857 | 0 |
| adequacy | 857 | 0 |
| warrant | 857 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 269 | 0 |
| human_y | 269 | 0 |
| micro | 269 | 0 |
| most_likely | 269 | 0 |
| confidence | 269 | 0 |
| finding | 269 | 0 |
| lifecycle | 269 | 0 |
| pins | 269 | 0 |
| reentries | 269 | 0 |
| boundary | 269 | 0 |
| belief | 857 | 0 |
| S | 857 | 0 |
| member | 857 | 0 |
| adequacy | 857 | 0 |
| warrant | 857 | 0 |

Disagreements: 0

## Classification

None to classify.
