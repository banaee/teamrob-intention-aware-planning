# scenario_s02_17: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 222. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 223 | 0 |
| human_y | 223 | 0 |
| micro | 223 | 0 |
| holding | 223 | 0 |
| waited | 223 | 0 |
| obj_at | 223 | 0 |
| at | 223 | 0 |
| most_likely | 223 | 0 |
| confidence | 223 | 0 |
| finding | 223 | 0 |
| lifecycle | 223 | 0 |
| pins | 223 | 0 |
| reentries | 223 | 0 |
| boundary | 223 | 0 |
| gate | 223 | 0 |
| belief | 681 | 0 |
| S | 681 | 0 |
| member | 681 | 0 |
| adequacy | 681 | 0 |
| warrant | 681 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 223 | 0 |
| human_y | 223 | 0 |
| micro | 223 | 0 |
| most_likely | 223 | 0 |
| confidence | 223 | 0 |
| finding | 223 | 0 |
| lifecycle | 223 | 0 |
| pins | 223 | 0 |
| reentries | 223 | 0 |
| boundary | 223 | 0 |
| belief | 681 | 0 |
| S | 681 | 0 |
| member | 681 | 0 |
| adequacy | 681 | 0 |
| warrant | 681 | 0 |

Disagreements: 0

## Classification

None to classify.
