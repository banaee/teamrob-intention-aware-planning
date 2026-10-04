# scenario_s13_06: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 430. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 431 | 0 |
| human_y | 431 | 0 |
| micro | 431 | 0 |
| holding | 431 | 0 |
| waited | 431 | 0 |
| obj_at | 431 | 0 |
| at | 431 | 0 |
| most_likely | 431 | 0 |
| confidence | 431 | 0 |
| finding | 431 | 0 |
| lifecycle | 431 | 0 |
| pins | 431 | 0 |
| reentries | 431 | 0 |
| boundary | 431 | 0 |
| gate | 431 | 0 |
| levels | 431 | 0 |
| recent | 431 | 0 |
| prior | 1348 | 0 |
| belief | 1348 | 0 |
| belief_h | 1348 | 0 |
| S | 1348 | 0 |
| member | 1348 | 0 |
| adequacy | 1348 | 0 |
| warrant | 1348 | 0 |
| rank | 1348 | 0 |

Undetermined (D3; skipped, not compared): none

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 431 | 0 |
| human_y | 431 | 0 |
| micro | 431 | 0 |
| most_likely | 431 | 0 |
| confidence | 431 | 0 |
| finding | 431 | 0 |
| lifecycle | 431 | 0 |
| pins | 431 | 0 |
| reentries | 431 | 0 |
| boundary | 431 | 0 |
| levels | 431 | 0 |
| recent | 431 | 0 |
| prior | 1348 | 0 |
| belief | 1348 | 0 |
| S | 1348 | 0 |
| member | 1348 | 0 |
| adequacy | 1348 | 0 |
| warrant | 1348 | 0 |
| rank | 1348 | 0 |

Undetermined (D3; skipped, not compared): none

Disagreements: 0

## Classification

None to classify.
