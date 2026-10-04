# scenario_s14_05: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 381. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 382 | 0 |
| human_y | 382 | 0 |
| micro | 382 | 0 |
| holding | 382 | 0 |
| waited | 382 | 0 |
| obj_at | 382 | 0 |
| at | 382 | 0 |
| most_likely | 382 | 0 |
| confidence | 382 | 0 |
| finding | 382 | 0 |
| lifecycle | 382 | 0 |
| pins | 382 | 0 |
| reentries | 382 | 0 |
| boundary | 382 | 0 |
| gate | 382 | 0 |
| levels | 382 | 0 |
| recent | 382 | 0 |
| prior | 1401 | 0 |
| belief | 1401 | 0 |
| belief_h | 1401 | 0 |
| S | 1401 | 0 |
| member | 1401 | 0 |
| adequacy | 1401 | 0 |
| warrant | 1401 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 382 | 0 |
| human_y | 382 | 0 |
| micro | 382 | 0 |
| most_likely | 382 | 0 |
| confidence | 382 | 0 |
| finding | 382 | 0 |
| lifecycle | 382 | 0 |
| pins | 382 | 0 |
| reentries | 382 | 0 |
| boundary | 382 | 0 |
| levels | 382 | 0 |
| recent | 382 | 0 |
| prior | 1401 | 0 |
| belief | 1401 | 0 |
| S | 1401 | 0 |
| member | 1401 | 0 |
| adequacy | 1401 | 0 |
| warrant | 1401 | 0 |

Disagreements: 0

## Classification

None to classify.
