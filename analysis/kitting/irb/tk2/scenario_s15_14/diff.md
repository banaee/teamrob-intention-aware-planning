# scenario_s15_14: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 420. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 421 | 0 |
| human_y | 421 | 0 |
| micro | 421 | 0 |
| holding | 421 | 0 |
| waited | 421 | 0 |
| obj_at | 421 | 0 |
| at | 421 | 0 |
| most_likely | 421 | 0 |
| confidence | 421 | 0 |
| finding | 421 | 0 |
| lifecycle | 421 | 0 |
| pins | 421 | 0 |
| reentries | 421 | 0 |
| boundary | 421 | 0 |
| gate | 421 | 0 |
| levels | 421 | 0 |
| recent | 421 | 0 |
| prior | 1729 | 0 |
| belief | 1729 | 0 |
| belief_h | 1729 | 0 |
| S | 1729 | 0 |
| member | 1729 | 0 |
| adequacy | 1729 | 0 |
| warrant | 1729 | 0 |
| rank | 1729 | 0 |

Undetermined (D3; skipped, not compared): none

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 421 | 0 |
| human_y | 421 | 0 |
| micro | 421 | 0 |
| most_likely | 421 | 0 |
| confidence | 421 | 0 |
| finding | 421 | 0 |
| lifecycle | 421 | 0 |
| pins | 421 | 0 |
| reentries | 421 | 0 |
| boundary | 421 | 0 |
| levels | 421 | 0 |
| recent | 421 | 0 |
| prior | 1729 | 0 |
| belief | 1729 | 0 |
| S | 1729 | 0 |
| member | 1729 | 0 |
| adequacy | 1729 | 0 |
| warrant | 1729 | 0 |
| rank | 1729 | 0 |

Undetermined (D3; skipped, not compared): none

Disagreements: 0

## Classification

None to classify.
