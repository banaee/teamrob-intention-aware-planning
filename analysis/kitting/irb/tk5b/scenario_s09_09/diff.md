# scenario_s09_09: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 251. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 252 | 0 |
| human_y | 252 | 0 |
| micro | 252 | 0 |
| holding | 252 | 0 |
| waited | 252 | 0 |
| obj_at | 252 | 0 |
| at | 252 | 0 |
| most_likely | 252 | 0 |
| confidence | 252 | 0 |
| finding | 252 | 0 |
| lifecycle | 252 | 0 |
| pins | 252 | 0 |
| reentries | 252 | 0 |
| boundary | 252 | 0 |
| gate | 252 | 0 |
| levels | 252 | 0 |
| recent | 252 | 0 |
| prior | 485 | 0 |
| belief | 485 | 0 |
| belief_h | 485 | 0 |
| S | 485 | 0 |
| member | 485 | 0 |
| adequacy | 485 | 0 |
| warrant | 485 | 0 |
| rank | 485 | 0 |

Undetermined (D3; skipped, not compared): none

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 252 | 0 |
| human_y | 252 | 0 |
| micro | 252 | 0 |
| most_likely | 252 | 0 |
| confidence | 252 | 0 |
| finding | 252 | 0 |
| lifecycle | 252 | 0 |
| pins | 252 | 0 |
| reentries | 252 | 0 |
| boundary | 252 | 0 |
| levels | 252 | 0 |
| recent | 252 | 0 |
| prior | 485 | 0 |
| belief | 485 | 0 |
| S | 485 | 0 |
| member | 485 | 0 |
| adequacy | 485 | 0 |
| warrant | 485 | 0 |
| rank | 485 | 0 |

Undetermined (D3; skipped, not compared): none

Disagreements: 0

## Classification

None to classify.
