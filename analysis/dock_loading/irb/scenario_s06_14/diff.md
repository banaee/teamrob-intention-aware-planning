# scenario_s06_14: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 64. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 65 | 0 |
| human_y | 65 | 0 |
| micro | 65 | 0 |
| holding | 65 | 0 |
| waited | 65 | 0 |
| obj_at | 65 | 0 |
| at | 65 | 0 |
| most_likely | 65 | 0 |
| confidence | 65 | 0 |
| finding | 65 | 0 |
| lifecycle | 65 | 0 |
| pins | 65 | 0 |
| reentries | 65 | 0 |
| boundary | 65 | 0 |
| gate | 65 | 0 |
| belief | 147 | 0 |
| S | 147 | 0 |
| member | 147 | 0 |
| adequacy | 147 | 0 |
| warrant | 147 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 65 | 0 |
| human_y | 65 | 0 |
| micro | 65 | 0 |
| most_likely | 65 | 0 |
| confidence | 65 | 0 |
| finding | 65 | 0 |
| lifecycle | 65 | 0 |
| pins | 65 | 0 |
| reentries | 65 | 0 |
| boundary | 65 | 0 |
| belief | 147 | 0 |
| S | 147 | 0 |
| member | 147 | 0 |
| adequacy | 147 | 0 |
| warrant | 147 | 0 |

Disagreements: 0

## Classification

None to classify.
