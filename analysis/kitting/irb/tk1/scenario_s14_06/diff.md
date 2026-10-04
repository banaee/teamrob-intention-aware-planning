# scenario_s14_06: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 462. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 463 | 0 |
| human_y | 463 | 0 |
| micro | 463 | 0 |
| holding | 463 | 0 |
| waited | 463 | 0 |
| obj_at | 463 | 0 |
| at | 463 | 0 |
| most_likely | 463 | 0 |
| confidence | 463 | 0 |
| finding | 463 | 0 |
| lifecycle | 463 | 0 |
| pins | 463 | 0 |
| reentries | 463 | 0 |
| boundary | 463 | 0 |
| gate | 463 | 0 |
| belief | 1725 | 0 |
| belief_h | 1725 | 0 |
| S | 1725 | 0 |
| member | 1725 | 0 |
| adequacy | 1725 | 0 |
| warrant | 1725 | 0 |

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 463 | 0 |
| human_y | 463 | 0 |
| micro | 463 | 0 |
| most_likely | 463 | 0 |
| confidence | 463 | 0 |
| finding | 463 | 0 |
| lifecycle | 463 | 0 |
| pins | 463 | 0 |
| reentries | 463 | 0 |
| boundary | 463 | 0 |
| belief | 1725 | 0 |
| S | 1725 | 0 |
| member | 1725 | 0 |
| adequacy | 1725 | 0 |
| warrant | 1725 | 0 |

Disagreements: 0

## Classification

None to classify.
