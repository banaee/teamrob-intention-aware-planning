# scenario_s14_13: expected against actual

expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks 0 to 378. Not compared (the recognizer does not output them): expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence.

## Against actual.csv (relative tolerance 1e-9)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 379 | 0 |
| human_y | 379 | 0 |
| micro | 379 | 0 |
| holding | 379 | 0 |
| waited | 379 | 0 |
| obj_at | 379 | 0 |
| at | 379 | 0 |
| most_likely | 379 | 0 |
| confidence | 379 | 0 |
| finding | 379 | 0 |
| lifecycle | 379 | 0 |
| pins | 379 | 0 |
| reentries | 379 | 0 |
| boundary | 379 | 0 |
| gate | 379 | 0 |
| levels | 379 | 0 |
| recent | 379 | 0 |
| prior | 1391 | 0 |
| belief | 1391 | 0 |
| belief_h | 1391 | 0 |
| S | 1391 | 0 |
| member | 1391 | 0 |
| adequacy | 1391 | 0 |
| warrant | 1391 | 0 |
| rank | 1391 | 0 |

Undetermined (D3; skipped, not compared): none

Disagreements: 0

## Against actual_log.csv (print precision)

Rows (tick, live hypothesis) present on one side only: 0

| column | compared | disagree |
|---|---|---|
| human_x | 379 | 0 |
| human_y | 379 | 0 |
| micro | 379 | 0 |
| most_likely | 379 | 0 |
| confidence | 379 | 0 |
| finding | 379 | 0 |
| lifecycle | 379 | 0 |
| pins | 379 | 0 |
| reentries | 379 | 0 |
| boundary | 379 | 0 |
| levels | 379 | 0 |
| recent | 379 | 0 |
| prior | 1391 | 0 |
| belief | 1391 | 0 |
| S | 1391 | 0 |
| member | 1391 | 0 |
| adequacy | 1391 | 1 |
| warrant | 1391 | 0 |
| rank | 1391 | 0 |

Undetermined (D3; skipped, not compared): none

Disagreements: 1

| tick | hypothesis | column | expected | actual |
|---|---|---|---|---|
| 181 | ac_activation(?ac_switch=ac_switch_0) | adequacy | inadequate | adequate |

## Classification

(written after investigation)
