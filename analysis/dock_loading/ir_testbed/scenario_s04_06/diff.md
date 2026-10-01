# scenario_s04_06: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 177. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 178 | 0 |
| human_y | 178 | 0 |
| micro | 178 | 0 |
| holding | 178 | 0 |
| waited | 178 | 0 |
| obj_at | 178 | 0 |
| at | 178 | 0 |
| most_likely | 178 | 0 |
| confidence | 178 | 0 |
| finding | 178 | 0 |
| lifecycle | 178 | 0 |
| pins | 178 | 0 |
| reentries | 178 | 0 |
| boundary | 178 | 0 |
| gate | 178 | 0 |
| belief | 512 | 0 |
| S | 512 | 0 |
| member | 512 | 0 |
| adequacy | 512 | 0 |
| warrant | 512 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 178 | 0 |
| human_y | 178 | 0 |
| micro | 178 | 0 |
| most_likely | 178 | 0 |
| confidence | 178 | 0 |
| finding | 178 | 0 |
| lifecycle | 178 | 0 |
| pins | 178 | 0 |
| reentries | 178 | 0 |
| boundary | 178 | 0 |
| belief | 512 | 0 |
| S | 512 | 0 |
| member | 512 | 0 |
| adequacy | 512 | 0 |
| warrant | 512 | 0 |

Disagreements: 0

## Classification

None to classify.
