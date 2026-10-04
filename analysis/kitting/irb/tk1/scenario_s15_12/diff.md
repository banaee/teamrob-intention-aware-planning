# scenario_s15_12: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 424. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 425 | 0 |
| human_y | 425 | 0 |
| micro | 425 | 0 |
| holding | 425 | 0 |
| waited | 425 | 0 |
| obj_at | 425 | 0 |
| at | 425 | 0 |
| most_likely | 425 | 0 |
| confidence | 425 | 0 |
| finding | 425 | 0 |
| lifecycle | 425 | 0 |
| pins | 425 | 0 |
| reentries | 425 | 0 |
| boundary | 425 | 0 |
| gate | 425 | 0 |
| levels | 425 | 0 |
| recent | 425 | 0 |
| prior | 1744 | 0 |
| belief | 1744 | 0 |
| belief_h | 1744 | 0 |
| S | 1744 | 0 |
| member | 1744 | 0 |
| adequacy | 1744 | 0 |
| warrant | 1744 | 0 |
| rank | 1708 | 0 |

Undetermined (D3; skipped, not compared): rank 36

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 425 | 0 |
| human_y | 425 | 0 |
| micro | 425 | 0 |
| most_likely | 425 | 0 |
| confidence | 425 | 0 |
| finding | 425 | 0 |
| lifecycle | 425 | 0 |
| pins | 425 | 0 |
| reentries | 425 | 0 |
| boundary | 425 | 0 |
| levels | 425 | 0 |
| recent | 425 | 0 |
| prior | 1744 | 0 |
| belief | 1744 | 0 |
| S | 1744 | 0 |
| member | 1744 | 0 |
| adequacy | 1744 | 0 |
| warrant | 1744 | 0 |
| rank | 1708 | 0 |

Undetermined (D3; skipped, not compared): rank 36

Disagreements: 0

## Classification

None to classify.
