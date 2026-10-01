# scenario_s02_05: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 244. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 245 | 0 |
| human_y | 245 | 0 |
| micro | 245 | 0 |
| holding | 245 | 0 |
| waited | 245 | 0 |
| obj_at | 245 | 0 |
| at | 245 | 0 |
| most_likely | 245 | 0 |
| confidence | 245 | 0 |
| finding | 245 | 0 |
| lifecycle | 245 | 0 |
| pins | 245 | 0 |
| reentries | 245 | 0 |
| boundary | 245 | 0 |
| gate | 245 | 0 |
| belief | 920 | 0 |
| S | 920 | 0 |
| member | 920 | 0 |
| adequacy | 920 | 0 |
| warrant | 920 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 245 | 0 |
| human_y | 245 | 0 |
| micro | 245 | 0 |
| most_likely | 245 | 0 |
| confidence | 245 | 0 |
| finding | 245 | 0 |
| lifecycle | 245 | 0 |
| pins | 245 | 0 |
| reentries | 245 | 0 |
| boundary | 245 | 0 |
| belief | 920 | 0 |
| S | 920 | 0 |
| member | 920 | 0 |
| adequacy | 920 | 0 |
| warrant | 920 | 0 |

Disagreements: 0

## Classification

None to classify.
