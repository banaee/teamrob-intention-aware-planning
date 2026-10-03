# scenario_s02_19: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 201. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 202 | 0 |
| human_y | 202 | 0 |
| micro | 202 | 0 |
| holding | 202 | 0 |
| waited | 202 | 0 |
| obj_at | 202 | 0 |
| at | 202 | 0 |
| most_likely | 202 | 0 |
| confidence | 202 | 0 |
| finding | 202 | 0 |
| lifecycle | 202 | 0 |
| pins | 202 | 0 |
| reentries | 202 | 0 |
| boundary | 202 | 0 |
| gate | 202 | 0 |
| belief | 747 | 0 |
| S | 747 | 0 |
| member | 747 | 0 |
| adequacy | 747 | 0 |
| warrant | 747 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 202 | 0 |
| human_y | 202 | 0 |
| micro | 202 | 0 |
| most_likely | 202 | 0 |
| confidence | 202 | 0 |
| finding | 202 | 0 |
| lifecycle | 202 | 0 |
| pins | 202 | 0 |
| reentries | 202 | 0 |
| boundary | 202 | 0 |
| belief | 747 | 0 |
| S | 747 | 0 |
| member | 747 | 0 |
| adequacy | 747 | 0 |
| warrant | 747 | 0 |

Disagreements: 0

## Classification

None to classify.
