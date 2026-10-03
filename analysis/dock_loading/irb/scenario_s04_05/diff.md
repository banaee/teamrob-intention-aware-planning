# scenario_s04_05: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 238. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 239 | 0 |
| human_y | 239 | 0 |
| micro | 239 | 0 |
| holding | 239 | 0 |
| waited | 239 | 0 |
| obj_at | 239 | 0 |
| at | 239 | 0 |
| most_likely | 239 | 0 |
| confidence | 239 | 0 |
| finding | 239 | 0 |
| lifecycle | 239 | 0 |
| pins | 239 | 0 |
| reentries | 239 | 0 |
| boundary | 239 | 0 |
| gate | 239 | 0 |
| belief | 914 | 0 |
| S | 914 | 0 |
| member | 914 | 0 |
| adequacy | 914 | 0 |
| warrant | 914 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 239 | 0 |
| human_y | 239 | 0 |
| micro | 239 | 0 |
| most_likely | 239 | 0 |
| confidence | 239 | 0 |
| finding | 239 | 0 |
| lifecycle | 239 | 0 |
| pins | 239 | 0 |
| reentries | 239 | 0 |
| boundary | 239 | 0 |
| belief | 914 | 0 |
| S | 914 | 0 |
| member | 914 | 0 |
| adequacy | 914 | 0 |
| warrant | 914 | 0 |

Disagreements: 0

## Classification

None to classify.
