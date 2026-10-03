# scenario_s04_04: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 108. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 109 | 0 |
| human_y | 109 | 0 |
| micro | 109 | 0 |
| holding | 109 | 0 |
| waited | 109 | 0 |
| obj_at | 109 | 0 |
| at | 109 | 0 |
| most_likely | 109 | 0 |
| confidence | 109 | 0 |
| finding | 109 | 0 |
| lifecycle | 109 | 0 |
| pins | 109 | 0 |
| reentries | 109 | 0 |
| boundary | 109 | 0 |
| gate | 109 | 0 |
| belief | 277 | 0 |
| S | 277 | 0 |
| member | 277 | 0 |
| adequacy | 277 | 0 |
| warrant | 277 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 109 | 0 |
| human_y | 109 | 0 |
| micro | 109 | 0 |
| most_likely | 109 | 0 |
| confidence | 109 | 0 |
| finding | 109 | 0 |
| lifecycle | 109 | 0 |
| pins | 109 | 0 |
| reentries | 109 | 0 |
| boundary | 109 | 0 |
| belief | 277 | 0 |
| S | 277 | 0 |
| member | 277 | 0 |
| adequacy | 277 | 0 |
| warrant | 277 | 0 |

Disagreements: 0

## Classification

None to classify.
