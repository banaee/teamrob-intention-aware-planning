# scenario_s04_19: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 202. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 203 | 0 |
| human_y | 203 | 0 |
| micro | 203 | 0 |
| holding | 203 | 0 |
| waited | 203 | 0 |
| obj_at | 203 | 0 |
| at | 203 | 0 |
| most_likely | 203 | 0 |
| confidence | 203 | 0 |
| finding | 203 | 0 |
| lifecycle | 203 | 0 |
| pins | 203 | 0 |
| reentries | 203 | 0 |
| boundary | 203 | 0 |
| gate | 203 | 0 |
| belief | 753 | 0 |
| S | 753 | 0 |
| member | 753 | 0 |
| adequacy | 753 | 0 |
| warrant | 753 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 203 | 0 |
| human_y | 203 | 0 |
| micro | 203 | 0 |
| most_likely | 203 | 0 |
| confidence | 203 | 0 |
| finding | 203 | 0 |
| lifecycle | 203 | 0 |
| pins | 203 | 0 |
| reentries | 203 | 0 |
| boundary | 203 | 0 |
| belief | 753 | 0 |
| S | 753 | 0 |
| member | 753 | 0 |
| adequacy | 753 | 0 |
| warrant | 753 | 0 |

Disagreements: 0

## Classification

None to classify.
