# scenario_s04_17: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 239. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 240 | 0 |
| human_y | 240 | 0 |
| micro | 240 | 0 |
| holding | 240 | 0 |
| waited | 240 | 0 |
| obj_at | 240 | 0 |
| at | 240 | 0 |
| most_likely | 240 | 0 |
| confidence | 240 | 0 |
| finding | 240 | 0 |
| lifecycle | 240 | 0 |
| pins | 240 | 0 |
| reentries | 240 | 0 |
| boundary | 240 | 0 |
| gate | 240 | 0 |
| belief | 749 | 0 |
| S | 749 | 0 |
| member | 749 | 0 |
| adequacy | 749 | 0 |
| warrant | 749 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 240 | 0 |
| human_y | 240 | 0 |
| micro | 240 | 0 |
| most_likely | 240 | 0 |
| confidence | 240 | 0 |
| finding | 240 | 0 |
| lifecycle | 240 | 0 |
| pins | 240 | 0 |
| reentries | 240 | 0 |
| boundary | 240 | 0 |
| belief | 749 | 0 |
| S | 749 | 0 |
| member | 749 | 0 |
| adequacy | 749 | 0 |
| warrant | 749 | 0 |

Disagreements: 0

## Classification

None to classify.
