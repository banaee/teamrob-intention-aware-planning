# scenario_s15_07: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 480. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 481 | 0 |
| human_y | 481 | 0 |
| micro | 481 | 0 |
| holding | 481 | 0 |
| waited | 481 | 0 |
| obj_at | 481 | 0 |
| at | 481 | 0 |
| most_likely | 481 | 0 |
| confidence | 481 | 0 |
| finding | 481 | 0 |
| lifecycle | 481 | 0 |
| pins | 481 | 0 |
| reentries | 481 | 0 |
| boundary | 481 | 0 |
| gate | 481 | 0 |
| levels | 481 | 0 |
| recent | 481 | 0 |
| prior | 2024 | 0 |
| belief | 2024 | 0 |
| belief_h | 2024 | 0 |
| S | 2024 | 0 |
| member | 2024 | 0 |
| adequacy | 2024 | 0 |
| warrant | 2024 | 0 |
| rank | 1988 | 0 |

Undetermined (D3; skipped, not compared): rank 36

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 481 | 0 |
| human_y | 481 | 0 |
| micro | 481 | 0 |
| most_likely | 481 | 0 |
| confidence | 481 | 0 |
| finding | 481 | 0 |
| lifecycle | 481 | 0 |
| pins | 481 | 0 |
| reentries | 481 | 0 |
| boundary | 481 | 0 |
| levels | 481 | 0 |
| recent | 481 | 0 |
| prior | 2024 | 0 |
| belief | 2024 | 0 |
| S | 2024 | 0 |
| member | 2024 | 0 |
| adequacy | 2024 | 0 |
| warrant | 2024 | 0 |
| rank | 1988 | 0 |

Undetermined (D3; skipped, not compared): rank 36

Disagreements: 0

## Classification

None to classify.
