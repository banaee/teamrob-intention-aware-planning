# scenario_s14_11: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 431. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 432 | 0 |
| human_y | 432 | 0 |
| micro | 432 | 0 |
| holding | 432 | 0 |
| waited | 432 | 0 |
| obj_at | 432 | 0 |
| at | 432 | 0 |
| most_likely | 432 | 0 |
| confidence | 432 | 0 |
| finding | 432 | 0 |
| lifecycle | 432 | 0 |
| pins | 432 | 0 |
| reentries | 432 | 0 |
| boundary | 432 | 0 |
| gate | 432 | 0 |
| belief | 1601 | 0 |
| belief_h | 1601 | 0 |
| S | 1601 | 0 |
| member | 1601 | 0 |
| adequacy | 1601 | 0 |
| warrant | 1601 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 432 | 0 |
| human_y | 432 | 0 |
| micro | 432 | 0 |
| most_likely | 432 | 0 |
| confidence | 432 | 0 |
| finding | 432 | 0 |
| lifecycle | 432 | 0 |
| pins | 432 | 0 |
| reentries | 432 | 0 |
| boundary | 432 | 0 |
| belief | 1601 | 0 |
| S | 1601 | 0 |
| member | 1601 | 0 |
| adequacy | 1601 | 0 |
| warrant | 1601 | 0 |

Disagreements: 0

## Classification

None to classify.
