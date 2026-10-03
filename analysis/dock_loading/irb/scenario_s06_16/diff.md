# scenario_s06_16: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 274. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 275 | 0 |
| human_y | 275 | 0 |
| micro | 275 | 0 |
| holding | 275 | 0 |
| waited | 275 | 0 |
| obj_at | 275 | 0 |
| at | 275 | 0 |
| most_likely | 275 | 0 |
| confidence | 275 | 0 |
| finding | 275 | 0 |
| lifecycle | 275 | 0 |
| pins | 275 | 0 |
| reentries | 275 | 0 |
| boundary | 275 | 0 |
| gate | 275 | 0 |
| belief | 840 | 0 |
| S | 840 | 0 |
| member | 840 | 0 |
| adequacy | 840 | 0 |
| warrant | 840 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 275 | 0 |
| human_y | 275 | 0 |
| micro | 275 | 0 |
| most_likely | 275 | 0 |
| confidence | 275 | 0 |
| finding | 275 | 0 |
| lifecycle | 275 | 0 |
| pins | 275 | 0 |
| reentries | 275 | 0 |
| boundary | 275 | 0 |
| belief | 840 | 0 |
| S | 840 | 0 |
| member | 840 | 0 |
| adequacy | 840 | 0 |
| warrant | 840 | 0 |

Disagreements: 0

## Classification

None to classify.
