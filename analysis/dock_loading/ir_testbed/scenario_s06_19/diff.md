# scenario_s06_19: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 180. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 181 | 0 |
| human_y | 181 | 0 |
| micro | 181 | 0 |
| holding | 181 | 0 |
| waited | 181 | 0 |
| obj_at | 181 | 0 |
| at | 181 | 0 |
| most_likely | 181 | 0 |
| confidence | 181 | 0 |
| finding | 181 | 0 |
| lifecycle | 181 | 0 |
| pins | 181 | 0 |
| reentries | 181 | 0 |
| boundary | 181 | 0 |
| gate | 181 | 0 |
| belief | 665 | 0 |
| S | 665 | 0 |
| member | 665 | 0 |
| adequacy | 665 | 0 |
| warrant | 665 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 181 | 0 |
| human_y | 181 | 0 |
| micro | 181 | 0 |
| most_likely | 181 | 0 |
| confidence | 181 | 0 |
| finding | 181 | 0 |
| lifecycle | 181 | 0 |
| pins | 181 | 0 |
| reentries | 181 | 0 |
| boundary | 181 | 0 |
| belief | 665 | 0 |
| S | 665 | 0 |
| member | 665 | 0 |
| adequacy | 665 | 0 |
| warrant | 665 | 0 |

Disagreements: 0

## Classification

None to classify.
