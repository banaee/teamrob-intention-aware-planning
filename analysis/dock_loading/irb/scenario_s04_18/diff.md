# scenario_s04_18: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 232. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 233 | 0 |
| human_y | 233 | 0 |
| micro | 233 | 0 |
| holding | 233 | 0 |
| waited | 233 | 0 |
| obj_at | 233 | 0 |
| at | 233 | 0 |
| most_likely | 233 | 0 |
| confidence | 233 | 0 |
| finding | 233 | 0 |
| lifecycle | 233 | 0 |
| pins | 233 | 0 |
| reentries | 233 | 0 |
| boundary | 233 | 0 |
| gate | 233 | 0 |
| belief | 677 | 0 |
| S | 677 | 0 |
| member | 677 | 0 |
| adequacy | 677 | 0 |
| warrant | 677 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 233 | 0 |
| human_y | 233 | 0 |
| micro | 233 | 0 |
| most_likely | 233 | 0 |
| confidence | 233 | 0 |
| finding | 233 | 0 |
| lifecycle | 233 | 0 |
| pins | 233 | 0 |
| reentries | 233 | 0 |
| boundary | 233 | 0 |
| belief | 677 | 0 |
| S | 677 | 0 |
| member | 677 | 0 |
| adequacy | 677 | 0 |
| warrant | 677 | 0 |

Disagreements: 0

## Classification

None to classify.
