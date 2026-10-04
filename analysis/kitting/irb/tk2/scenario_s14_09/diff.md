# scenario_s14_09: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 349. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 350 | 0 |
| human_y | 350 | 0 |
| micro | 350 | 0 |
| holding | 350 | 0 |
| waited | 350 | 0 |
| obj_at | 350 | 0 |
| at | 350 | 0 |
| most_likely | 350 | 0 |
| confidence | 350 | 0 |
| finding | 350 | 0 |
| lifecycle | 350 | 0 |
| pins | 350 | 0 |
| reentries | 350 | 0 |
| boundary | 350 | 0 |
| gate | 350 | 0 |
| levels | 350 | 0 |
| recent | 350 | 0 |
| prior | 1273 | 0 |
| belief | 1273 | 0 |
| belief_h | 1273 | 0 |
| S | 1273 | 0 |
| member | 1273 | 0 |
| adequacy | 1273 | 0 |
| warrant | 1273 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 350 | 0 |
| human_y | 350 | 0 |
| micro | 350 | 0 |
| most_likely | 350 | 0 |
| confidence | 350 | 0 |
| finding | 350 | 0 |
| lifecycle | 350 | 0 |
| pins | 350 | 0 |
| reentries | 350 | 0 |
| boundary | 350 | 0 |
| levels | 350 | 0 |
| recent | 350 | 0 |
| prior | 1273 | 0 |
| belief | 1273 | 0 |
| S | 1273 | 0 |
| member | 1273 | 0 |
| adequacy | 1273 | 0 |
| warrant | 1273 | 0 |

Disagreements: 0

## Classification

None to classify.
