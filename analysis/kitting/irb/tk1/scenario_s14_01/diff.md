# scenario_s14_01: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 335. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 336 | 0 |
| human_y | 336 | 0 |
| micro | 336 | 0 |
| holding | 336 | 0 |
| waited | 336 | 0 |
| obj_at | 336 | 0 |
| at | 336 | 0 |
| most_likely | 336 | 0 |
| confidence | 336 | 0 |
| finding | 336 | 0 |
| lifecycle | 336 | 0 |
| pins | 336 | 0 |
| reentries | 336 | 0 |
| boundary | 336 | 0 |
| gate | 336 | 0 |
| belief | 1219 | 0 |
| belief_h | 1219 | 0 |
| S | 1219 | 0 |
| member | 1219 | 0 |
| adequacy | 1219 | 0 |
| warrant | 1219 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 336 | 0 |
| human_y | 336 | 0 |
| micro | 336 | 0 |
| most_likely | 336 | 0 |
| confidence | 336 | 0 |
| finding | 336 | 0 |
| lifecycle | 336 | 0 |
| pins | 336 | 0 |
| reentries | 336 | 0 |
| boundary | 336 | 0 |
| belief | 1219 | 0 |
| S | 1219 | 0 |
| member | 1219 | 0 |
| adequacy | 1219 | 0 |
| warrant | 1219 | 0 |

Disagreements: 0

## Classification

None to classify.
