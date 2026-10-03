# scenario_s08_02: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 280. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 281 | 0 |
| human_y | 281 | 0 |
| micro | 281 | 0 |
| holding | 281 | 0 |
| waited | 281 | 0 |
| obj_at | 281 | 0 |
| at | 281 | 0 |
| most_likely | 281 | 0 |
| confidence | 281 | 0 |
| finding | 281 | 0 |
| lifecycle | 281 | 0 |
| pins | 281 | 0 |
| reentries | 281 | 0 |
| boundary | 281 | 0 |
| gate | 281 | 0 |
| belief | 541 | 0 |
| S | 541 | 0 |
| member | 541 | 0 |
| adequacy | 541 | 0 |
| warrant | 541 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 281 | 0 |
| human_y | 281 | 0 |
| micro | 281 | 0 |
| most_likely | 281 | 0 |
| confidence | 281 | 0 |
| finding | 281 | 0 |
| lifecycle | 281 | 0 |
| pins | 281 | 0 |
| reentries | 281 | 0 |
| boundary | 281 | 0 |
| belief | 541 | 0 |
| S | 541 | 0 |
| member | 541 | 0 |
| adequacy | 541 | 0 |
| warrant | 541 | 0 |

Disagreements: 0

## Classification

None to classify.
