# scenario_s15_10: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 373. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 374 | 0 |
| human_y | 374 | 0 |
| micro | 374 | 0 |
| holding | 374 | 0 |
| waited | 374 | 0 |
| obj_at | 374 | 0 |
| at | 374 | 0 |
| most_likely | 374 | 0 |
| confidence | 374 | 0 |
| finding | 374 | 0 |
| lifecycle | 374 | 0 |
| pins | 374 | 0 |
| reentries | 374 | 0 |
| boundary | 374 | 0 |
| gate | 374 | 0 |
| levels | 374 | 0 |
| recent | 374 | 0 |
| prior | 1468 | 0 |
| belief | 1468 | 0 |
| belief_h | 1468 | 0 |
| S | 1468 | 0 |
| member | 1468 | 0 |
| adequacy | 1468 | 0 |
| warrant | 1468 | 0 |
| rank | 1468 | 0 |

Undetermined (D3; skipped, not compared): none

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 374 | 0 |
| human_y | 374 | 0 |
| micro | 374 | 0 |
| most_likely | 374 | 0 |
| confidence | 374 | 0 |
| finding | 374 | 0 |
| lifecycle | 374 | 0 |
| pins | 374 | 0 |
| reentries | 374 | 0 |
| boundary | 374 | 0 |
| levels | 374 | 0 |
| recent | 374 | 0 |
| prior | 1468 | 0 |
| belief | 1468 | 0 |
| S | 1468 | 0 |
| member | 1468 | 0 |
| adequacy | 1468 | 0 |
| warrant | 1468 | 0 |
| rank | 1468 | 0 |

Undetermined (D3; skipped, not compared): none

Disagreements: 0

## Classification

None to classify.
