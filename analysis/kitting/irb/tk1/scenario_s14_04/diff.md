# scenario_s14_04: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 386. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 387 | 0 |
| human_y | 387 | 0 |
| micro | 387 | 0 |
| holding | 387 | 0 |
| waited | 387 | 0 |
| obj_at | 387 | 0 |
| at | 387 | 0 |
| most_likely | 387 | 0 |
| confidence | 387 | 0 |
| finding | 387 | 0 |
| lifecycle | 387 | 0 |
| pins | 387 | 0 |
| reentries | 387 | 0 |
| boundary | 387 | 0 |
| gate | 387 | 0 |
| levels | 387 | 0 |
| recent | 387 | 0 |
| prior | 1423 | 0 |
| belief | 1423 | 0 |
| belief_h | 1423 | 0 |
| S | 1423 | 0 |
| member | 1423 | 0 |
| adequacy | 1423 | 0 |
| warrant | 1423 | 0 |
| rank | 1399 | 0 |

Undetermined (D3; skipped, not compared): rank 24

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 387 | 0 |
| human_y | 387 | 0 |
| micro | 387 | 0 |
| most_likely | 387 | 0 |
| confidence | 387 | 0 |
| finding | 387 | 0 |
| lifecycle | 387 | 0 |
| pins | 387 | 0 |
| reentries | 387 | 0 |
| boundary | 387 | 0 |
| levels | 387 | 0 |
| recent | 387 | 0 |
| prior | 1423 | 0 |
| belief | 1423 | 0 |
| S | 1423 | 0 |
| member | 1423 | 0 |
| adequacy | 1423 | 0 |
| warrant | 1423 | 0 |
| rank | 1399 | 0 |

Undetermined (D3; skipped, not compared): rank 24

Disagreements: 0

## Classification

None to classify.
