# scenario_s06_04: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 87. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 88 | 0 |
| human_y | 88 | 0 |
| micro | 88 | 0 |
| holding | 88 | 0 |
| waited | 88 | 0 |
| obj_at | 88 | 0 |
| at | 88 | 0 |
| most_likely | 88 | 0 |
| confidence | 88 | 0 |
| finding | 88 | 0 |
| lifecycle | 88 | 0 |
| pins | 88 | 0 |
| reentries | 88 | 0 |
| boundary | 88 | 0 |
| gate | 88 | 0 |
| belief | 213 | 0 |
| S | 213 | 0 |
| member | 213 | 0 |
| adequacy | 213 | 0 |
| warrant | 213 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 88 | 0 |
| human_y | 88 | 0 |
| micro | 88 | 0 |
| most_likely | 88 | 0 |
| confidence | 88 | 0 |
| finding | 88 | 0 |
| lifecycle | 88 | 0 |
| pins | 88 | 0 |
| reentries | 88 | 0 |
| boundary | 88 | 0 |
| belief | 213 | 0 |
| S | 213 | 0 |
| member | 213 | 0 |
| adequacy | 213 | 0 |
| warrant | 213 | 0 |

Disagreements: 0

## Classification

None to classify.
