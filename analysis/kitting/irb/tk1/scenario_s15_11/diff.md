# scenario_s15_11: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 440. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 441 | 0 |
| human_y | 441 | 0 |
| micro | 441 | 0 |
| holding | 441 | 0 |
| waited | 441 | 0 |
| obj_at | 441 | 0 |
| at | 441 | 0 |
| most_likely | 441 | 0 |
| confidence | 441 | 0 |
| finding | 441 | 0 |
| lifecycle | 441 | 0 |
| pins | 441 | 0 |
| reentries | 441 | 0 |
| boundary | 441 | 0 |
| gate | 441 | 0 |
| belief | 1829 | 0 |
| belief_h | 1829 | 0 |
| S | 1829 | 0 |
| member | 1829 | 0 |
| adequacy | 1829 | 0 |
| warrant | 1829 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 441 | 0 |
| human_y | 441 | 0 |
| micro | 441 | 0 |
| most_likely | 441 | 0 |
| confidence | 441 | 0 |
| finding | 441 | 0 |
| lifecycle | 441 | 0 |
| pins | 441 | 0 |
| reentries | 441 | 0 |
| boundary | 441 | 0 |
| belief | 1829 | 0 |
| S | 1829 | 0 |
| member | 1829 | 0 |
| adequacy | 1829 | 0 |
| warrant | 1829 | 0 |

Disagreements: 0

## Classification

None to classify.
