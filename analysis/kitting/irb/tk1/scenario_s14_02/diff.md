# scenario_s14_02: expected against actual

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
| belief | 1391 | 0 |
| S | 1391 | 0 |
| member | 1391 | 0 |
| adequacy | 1391 | 0 |
| warrant | 1391 | 0 |

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
| belief | 1391 | 0 |
| S | 1391 | 0 |
| member | 1391 | 0 |
| adequacy | 1391 | 1 |
| warrant | 1391 | 0 |

Disagreements: 1

| tick | hypothesis | column | expected | actual |
|---|---|---|---|---|
| 181 | ac_activation(?ac_switch=ac_switch_0) | adequacy | inadequate | adequate |

## Classification

(written after investigation, 3 October 2026)

Tick 181, ac_activation, adequacy against the log: the records do not determine the value at the log's print precision.
S = 0.049970 (expected and in-process alike, agreeing at 1e-9), just below α = 0.05, so the hypothesis is inadequate;
the log prints S to four decimals as 0.0500, from which the reader derives adequate. The in-process source is
authoritative: 0 disagreements against actual.csv. The IRB's known flag (analysis/kitting/irb/REPORT.md, IRB.4b flags,
1). Not a disagreement of the recognizer with the records.
