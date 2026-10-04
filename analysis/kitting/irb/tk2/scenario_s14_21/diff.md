# scenario_s14_21: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 346. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 347 | 0 |
| human_y | 347 | 0 |
| micro | 347 | 0 |
| holding | 347 | 0 |
| waited | 347 | 0 |
| obj_at | 347 | 0 |
| at | 347 | 0 |
| most_likely | 347 | 0 |
| confidence | 347 | 0 |
| finding | 347 | 0 |
| lifecycle | 347 | 0 |
| pins | 347 | 0 |
| reentries | 347 | 0 |
| boundary | 347 | 0 |
| gate | 347 | 0 |
| levels | 347 | 0 |
| recent | 347 | 0 |
| prior | 1250 | 0 |
| belief | 1250 | 0 |
| belief_h | 1250 | 0 |
| S | 1250 | 0 |
| member | 1250 | 0 |
| adequacy | 1250 | 0 |
| warrant | 1250 | 0 |
| rank | 1250 | 0 |

Undetermined (D3; skipped, not compared): none

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 347 | 0 |
| human_y | 347 | 0 |
| micro | 347 | 0 |
| most_likely | 347 | 0 |
| confidence | 347 | 0 |
| finding | 347 | 0 |
| lifecycle | 347 | 0 |
| pins | 347 | 0 |
| reentries | 347 | 0 |
| boundary | 347 | 0 |
| levels | 347 | 0 |
| recent | 347 | 0 |
| prior | 1250 | 0 |
| belief | 1250 | 0 |
| S | 1250 | 0 |
| member | 1250 | 0 |
| adequacy | 1250 | 0 |
| warrant | 1250 | 0 |
| rank | 1250 | 0 |

Undetermined (D3; skipped, not compared): none

Disagreements: 0

## Classification

None to classify.
