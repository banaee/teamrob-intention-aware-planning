# scenario_s09_13: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 291. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 292 | 0 |
| human_y | 292 | 0 |
| micro | 292 | 0 |
| holding | 292 | 0 |
| waited | 292 | 0 |
| obj_at | 292 | 0 |
| at | 292 | 0 |
| most_likely | 292 | 0 |
| confidence | 292 | 0 |
| finding | 292 | 0 |
| lifecycle | 292 | 0 |
| pins | 292 | 0 |
| reentries | 292 | 0 |
| boundary | 292 | 0 |
| gate | 292 | 0 |
| levels | 292 | 0 |
| recent | 292 | 0 |
| prior | 651 | 0 |
| belief | 651 | 0 |
| belief_h | 651 | 0 |
| S | 651 | 0 |
| member | 651 | 0 |
| adequacy | 651 | 0 |
| warrant | 651 | 0 |
| rank | 651 | 0 |

Undetermined (D3; skipped, not compared): none

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 292 | 0 |
| human_y | 292 | 0 |
| micro | 292 | 0 |
| most_likely | 292 | 0 |
| confidence | 292 | 0 |
| finding | 292 | 0 |
| lifecycle | 292 | 0 |
| pins | 292 | 0 |
| reentries | 292 | 0 |
| boundary | 292 | 0 |
| levels | 292 | 0 |
| recent | 292 | 0 |
| prior | 651 | 0 |
| belief | 651 | 0 |
| S | 651 | 0 |
| member | 651 | 0 |
| adequacy | 651 | 0 |
| warrant | 651 | 0 |
| rank | 651 | 0 |

Undetermined (D3; skipped, not compared): none

Disagreements: 0

## Classification

None to classify.
