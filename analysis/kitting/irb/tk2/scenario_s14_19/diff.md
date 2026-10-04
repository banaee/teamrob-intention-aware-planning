# scenario_s14_19: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 371. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 372 | 0 |
| human_y | 372 | 0 |
| micro | 372 | 0 |
| holding | 372 | 0 |
| waited | 372 | 0 |
| obj_at | 372 | 0 |
| at | 372 | 0 |
| most_likely | 372 | 0 |
| confidence | 372 | 0 |
| finding | 372 | 0 |
| lifecycle | 372 | 0 |
| pins | 372 | 0 |
| reentries | 372 | 0 |
| boundary | 372 | 0 |
| gate | 372 | 0 |
| levels | 372 | 0 |
| recent | 372 | 0 |
| prior | 1325 | 0 |
| belief | 1325 | 0 |
| belief_h | 1325 | 0 |
| S | 1325 | 0 |
| member | 1325 | 0 |
| adequacy | 1325 | 0 |
| warrant | 1325 | 0 |
| rank | 1325 | 0 |

Undetermined (D3; skipped, not compared): none

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 372 | 0 |
| human_y | 372 | 0 |
| micro | 372 | 0 |
| most_likely | 372 | 0 |
| confidence | 372 | 0 |
| finding | 372 | 0 |
| lifecycle | 372 | 0 |
| pins | 372 | 0 |
| reentries | 372 | 0 |
| boundary | 372 | 0 |
| levels | 372 | 0 |
| recent | 372 | 0 |
| prior | 1325 | 0 |
| belief | 1325 | 0 |
| S | 1325 | 0 |
| member | 1325 | 0 |
| adequacy | 1325 | 0 |
| warrant | 1325 | 0 |
| rank | 1325 | 0 |

Undetermined (D3; skipped, not compared): none

Disagreements: 0

## Classification

None to classify.
