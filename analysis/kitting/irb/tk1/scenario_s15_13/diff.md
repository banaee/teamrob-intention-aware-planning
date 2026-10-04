# scenario_s15_13: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 452. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 453 | 0 |
| human_y | 453 | 0 |
| micro | 453 | 0 |
| holding | 453 | 0 |
| waited | 453 | 0 |
| obj_at | 453 | 0 |
| at | 453 | 0 |
| most_likely | 453 | 0 |
| confidence | 453 | 0 |
| finding | 453 | 0 |
| lifecycle | 453 | 0 |
| pins | 453 | 0 |
| reentries | 453 | 0 |
| boundary | 453 | 0 |
| gate | 453 | 0 |
| levels | 453 | 0 |
| recent | 453 | 0 |
| prior | 1890 | 0 |
| belief | 1890 | 0 |
| belief_h | 1890 | 0 |
| S | 1890 | 0 |
| member | 1890 | 0 |
| adequacy | 1890 | 0 |
| warrant | 1890 | 0 |
| rank | 1854 | 0 |

Undetermined (D3; skipped, not compared): rank 36

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 453 | 0 |
| human_y | 453 | 0 |
| micro | 453 | 0 |
| most_likely | 453 | 0 |
| confidence | 453 | 0 |
| finding | 453 | 0 |
| lifecycle | 453 | 0 |
| pins | 453 | 0 |
| reentries | 453 | 0 |
| boundary | 453 | 0 |
| levels | 453 | 0 |
| recent | 453 | 0 |
| prior | 1890 | 0 |
| belief | 1890 | 0 |
| S | 1890 | 0 |
| member | 1890 | 0 |
| adequacy | 1890 | 0 |
| warrant | 1890 | 0 |
| rank | 1854 | 0 |

Undetermined (D3; skipped, not compared): rank 36

Disagreements: 0

## Classification

None to classify.
