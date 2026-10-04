# scenario_s09_05: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 269. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 270 | 0 |
| human_y | 270 | 0 |
| micro | 270 | 0 |
| holding | 270 | 0 |
| waited | 270 | 0 |
| obj_at | 270 | 0 |
| at | 270 | 0 |
| most_likely | 270 | 0 |
| confidence | 270 | 0 |
| finding | 270 | 0 |
| lifecycle | 270 | 0 |
| pins | 270 | 0 |
| reentries | 270 | 0 |
| boundary | 270 | 0 |
| gate | 270 | 0 |
| levels | 270 | 0 |
| recent | 270 | 0 |
| prior | 588 | 0 |
| belief | 588 | 0 |
| belief_h | 588 | 0 |
| S | 588 | 0 |
| member | 588 | 0 |
| adequacy | 588 | 0 |
| warrant | 588 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 270 | 0 |
| human_y | 270 | 0 |
| micro | 270 | 0 |
| most_likely | 270 | 0 |
| confidence | 270 | 0 |
| finding | 270 | 0 |
| lifecycle | 270 | 0 |
| pins | 270 | 0 |
| reentries | 270 | 0 |
| boundary | 270 | 0 |
| levels | 270 | 0 |
| recent | 270 | 0 |
| prior | 588 | 0 |
| belief | 588 | 0 |
| S | 588 | 0 |
| member | 588 | 0 |
| adequacy | 588 | 0 |
| warrant | 588 | 0 |

Disagreements: 0

## Classification

None to classify.
