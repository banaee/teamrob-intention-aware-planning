# scenario_s09_04: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 281. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 282 | 0 |
| human_y | 282 | 0 |
| micro | 282 | 0 |
| holding | 282 | 0 |
| waited | 282 | 0 |
| obj_at | 282 | 0 |
| at | 282 | 0 |
| most_likely | 282 | 0 |
| confidence | 282 | 0 |
| finding | 282 | 0 |
| lifecycle | 282 | 0 |
| pins | 282 | 0 |
| reentries | 282 | 0 |
| boundary | 282 | 0 |
| belief | 621 | 0 |
| S | 621 | 0 |
| member | 621 | 0 |
| adequacy | 621 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 282 | 0 |
| human_y | 282 | 0 |
| micro | 282 | 0 |
| most_likely | 282 | 0 |
| confidence | 282 | 0 |
| finding | 282 | 0 |
| lifecycle | 282 | 0 |
| pins | 282 | 0 |
| reentries | 282 | 0 |
| boundary | 282 | 0 |
| belief | 621 | 0 |
| S | 621 | 0 |
| member | 621 | 0 |
| adequacy | 621 | 0 |

Disagreements: 0

## Classification

None to classify.
