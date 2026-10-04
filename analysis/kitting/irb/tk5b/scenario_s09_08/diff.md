# scenario_s09_08: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 210. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 211 | 0 |
| human_y | 211 | 0 |
| micro | 211 | 0 |
| holding | 211 | 0 |
| waited | 211 | 0 |
| obj_at | 211 | 0 |
| at | 211 | 0 |
| most_likely | 211 | 0 |
| confidence | 211 | 0 |
| finding | 211 | 0 |
| lifecycle | 211 | 0 |
| pins | 211 | 0 |
| reentries | 211 | 0 |
| boundary | 211 | 0 |
| gate | 211 | 0 |
| levels | 211 | 0 |
| recent | 211 | 0 |
| prior | 553 | 0 |
| belief | 553 | 0 |
| belief_h | 553 | 0 |
| S | 553 | 0 |
| member | 553 | 0 |
| adequacy | 553 | 0 |
| warrant | 553 | 0 |
| rank | 553 | 0 |

Undetermined (D3; skipped, not compared): none

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 211 | 0 |
| human_y | 211 | 0 |
| micro | 211 | 0 |
| most_likely | 211 | 0 |
| confidence | 211 | 0 |
| finding | 211 | 0 |
| lifecycle | 211 | 0 |
| pins | 211 | 0 |
| reentries | 211 | 0 |
| boundary | 211 | 0 |
| levels | 211 | 0 |
| recent | 211 | 0 |
| prior | 553 | 0 |
| belief | 553 | 0 |
| S | 553 | 0 |
| member | 553 | 0 |
| adequacy | 553 | 0 |
| warrant | 553 | 0 |
| rank | 553 | 0 |

Undetermined (D3; skipped, not compared): none

Disagreements: 0

## Classification

None to classify.
