# scenario_s15_05: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 435. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 436 | 0 |
| human_y | 436 | 0 |
| micro | 436 | 0 |
| holding | 436 | 0 |
| waited | 436 | 0 |
| obj_at | 436 | 0 |
| at | 436 | 0 |
| most_likely | 436 | 0 |
| confidence | 436 | 0 |
| finding | 436 | 0 |
| lifecycle | 436 | 0 |
| pins | 436 | 0 |
| reentries | 436 | 0 |
| boundary | 436 | 0 |
| gate | 436 | 0 |
| belief | 1804 | 0 |
| belief_h | 1804 | 0 |
| S | 1804 | 0 |
| member | 1804 | 0 |
| adequacy | 1804 | 0 |
| warrant | 1804 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 436 | 0 |
| human_y | 436 | 0 |
| micro | 436 | 0 |
| most_likely | 436 | 0 |
| confidence | 436 | 0 |
| finding | 436 | 0 |
| lifecycle | 436 | 0 |
| pins | 436 | 0 |
| reentries | 436 | 0 |
| boundary | 436 | 0 |
| belief | 1804 | 0 |
| S | 1804 | 0 |
| member | 1804 | 0 |
| adequacy | 1804 | 0 |
| warrant | 1804 | 0 |

Disagreements: 0

## Classification

None to classify.
