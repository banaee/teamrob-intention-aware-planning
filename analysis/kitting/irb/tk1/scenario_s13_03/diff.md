# scenario_s13_03: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 423. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 424 | 0 |
| human_y | 424 | 0 |
| micro | 424 | 0 |
| holding | 424 | 0 |
| waited | 424 | 0 |
| obj_at | 424 | 0 |
| at | 424 | 0 |
| most_likely | 424 | 0 |
| confidence | 424 | 0 |
| finding | 424 | 0 |
| lifecycle | 424 | 0 |
| pins | 424 | 0 |
| reentries | 424 | 0 |
| boundary | 424 | 0 |
| gate | 424 | 0 |
| belief | 1257 | 0 |
| belief_h | 1257 | 0 |
| S | 1257 | 0 |
| member | 1257 | 0 |
| adequacy | 1257 | 0 |
| warrant | 1257 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 424 | 0 |
| human_y | 424 | 0 |
| micro | 424 | 0 |
| most_likely | 424 | 0 |
| confidence | 424 | 0 |
| finding | 424 | 0 |
| lifecycle | 424 | 0 |
| pins | 424 | 0 |
| reentries | 424 | 0 |
| boundary | 424 | 0 |
| belief | 1257 | 0 |
| S | 1257 | 0 |
| member | 1257 | 0 |
| adequacy | 1257 | 0 |
| warrant | 1257 | 0 |

Disagreements: 0

## Classification

None to classify.
