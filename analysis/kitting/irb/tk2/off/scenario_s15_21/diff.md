# scenario_s15_21: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 446. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 447 | 0 |
| human_y | 447 | 0 |
| micro | 447 | 0 |
| holding | 447 | 0 |
| waited | 447 | 0 |
| obj_at | 447 | 0 |
| at | 447 | 0 |
| most_likely | 447 | 0 |
| confidence | 447 | 0 |
| finding | 447 | 0 |
| lifecycle | 447 | 0 |
| pins | 447 | 0 |
| reentries | 447 | 0 |
| boundary | 447 | 0 |
| gate | 447 | 0 |
| levels | 447 | 0 |
| recent | 447 | 0 |
| prior | 1601 | 0 |
| belief | 1601 | 0 |
| belief_h | 1601 | 0 |
| S | 1601 | 0 |
| member | 1601 | 0 |
| adequacy | 1601 | 0 |
| warrant | 1601 | 0 |
| rank | 1601 | 0 |

Undetermined (D3; skipped, not compared): none

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 447 | 0 |
| human_y | 447 | 0 |
| micro | 447 | 0 |
| most_likely | 447 | 0 |
| confidence | 447 | 0 |
| finding | 447 | 0 |
| lifecycle | 447 | 0 |
| pins | 447 | 0 |
| reentries | 447 | 0 |
| boundary | 447 | 0 |
| levels | 447 | 0 |
| recent | 447 | 0 |
| prior | 1601 | 0 |
| belief | 1601 | 0 |
| S | 1601 | 0 |
| member | 1601 | 0 |
| adequacy | 1601 | 0 |
| warrant | 1601 | 0 |
| rank | 1601 | 0 |

Undetermined (D3; skipped, not compared): none

Disagreements: 0

## Classification

None to classify.
