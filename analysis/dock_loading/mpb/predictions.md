# The MPB on dock_loading: K8's table, written before its runs (DL-P1)

DL-P1 (design_decisions.md, "T-G: the second domain's rulings", THE MPB ON DOCK_LOADING): K8's cut falls on the last step
of the walk to pallet_0 (env_layout_03 after 26 executed ticks, PT52S; env_layout_04 after 15, PT30S). Before K8's runs,
its per-tick table is reported for both rooms, from scan 0's expected admission (or the walk's start if none) to 10 ticks
after the cut: the leader, scan 0's share, scan 0's hypothesis adequacy, the gate's outcome, and the expected cause of
each decision. Read from the committed `expected_ticks.json` (the oracle's table, kind 3's output floor included); the
decisions are the chain's (C1 to C6) assembled with no `no_current_task` tick of the robot in the window but tick 0, the
one assumption: the run's own `no_current_task` ticks enter at the compare step.

Outcome. env_layout_03: entered at 14 (scan 0 at 0.7510), retraction at 34 (scan 0 inadequate while it still leads at
0.7947): the case forms, K8 runs there. env_layout_04: scan 0 never clears; no admission and no retraction: the case does
not form; K8 runs there and the record states it.

## env_layout_03 (scenario_s08_08)

Scan 0's first expected clearing: 14; the cut at 26; window 14 to 36
| tick | leader | scan 0 share | scan 0 adequacy | gate | decision (cause) |
|---|---|---|---|---|---|
| 14 | confirm_delivered_pallet(?pallet=pallet_0) | 0.7510 | adequate | clears | recognition_changed (entered) |
| 15 | confirm_delivered_pallet(?pallet=pallet_0) | 0.7874 | adequate | clears |  |
| 16 | confirm_delivered_pallet(?pallet=pallet_0) | 0.8205 | adequate | clears |  |
| 17 | confirm_delivered_pallet(?pallet=pallet_0) | 0.8500 | adequate | clears |  |
| 18 | confirm_delivered_pallet(?pallet=pallet_0) | 0.8755 | adequate | clears |  |
| 19 | confirm_delivered_pallet(?pallet=pallet_0) | 0.8970 | adequate | clears |  |
| 20 | confirm_delivered_pallet(?pallet=pallet_0) | 0.9147 | adequate | clears |  |
| 21 | confirm_delivered_pallet(?pallet=pallet_0) | 0.9292 | adequate | clears |  |
| 22 | confirm_delivered_pallet(?pallet=pallet_0) | 0.9407 | adequate | clears |  |
| 23 | confirm_delivered_pallet(?pallet=pallet_0) | 0.9498 | adequate | clears |  |
| 24 | confirm_delivered_pallet(?pallet=pallet_0) | 0.9568 | adequate | clears |  |
| 25 | confirm_delivered_pallet(?pallet=pallet_0) | 0.9621 | adequate | clears |  |
| 26 | confirm_delivered_pallet(?pallet=pallet_0) | 0.9595 | adequate | clears |  |
| 27 | confirm_delivered_pallet(?pallet=pallet_0) | 0.9554 | adequate | clears |  |
| 28 | confirm_delivered_pallet(?pallet=pallet_0) | 0.9492 | adequate | clears |  |
| 29 | confirm_delivered_pallet(?pallet=pallet_0) | 0.9402 | adequate | clears |  |
| 30 | confirm_delivered_pallet(?pallet=pallet_0) | 0.9270 | adequate | clears |  |
| 31 | confirm_delivered_pallet(?pallet=pallet_0) | 0.9081 | adequate | clears |  |
| 32 | confirm_delivered_pallet(?pallet=pallet_0) | 0.8813 | adequate | clears |  |
| 33 | confirm_delivered_pallet(?pallet=pallet_0) | 0.8443 | adequate | clears |  |
| 34 | confirm_delivered_pallet(?pallet=pallet_0) | 0.7947 | inadequate | none(leader_inadequate) | recognition_changed (retraction) |
| 35 | confirm_delivered_pallet(?pallet=pallet_0) | 0.7308 | inadequate | none(below_theta) |  |
| 36 | confirm_delivered_pallet(?pallet=pallet_0) | 0.6526 | inadequate | none(below_theta) |  |

## env_layout_04 (scenario_s09_08)

Scan 0's first expected clearing: None; the cut at 15; window 0 to 25
| tick | leader | scan 0 share | scan 0 adequacy | gate | decision (cause) |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(?pallet=pallet_0) | 0.2530 | adequate | none(below_theta) | no_current_task |
| 1 | confirm_delivered_pallet(?pallet=pallet_0) | 0.2628 | adequate | none(below_theta) |  |
| 2 | confirm_delivered_pallet(?pallet=pallet_0) | 0.2741 | adequate | none(below_theta) | projection_expired |
| 3 | confirm_delivered_pallet(?pallet=pallet_0) | 0.2871 | adequate | none(below_theta) |  |
| 4 | confirm_delivered_pallet(?pallet=pallet_0) | 0.3021 | adequate | none(below_theta) |  |
| 5 | confirm_delivered_pallet(?pallet=pallet_0) | 0.3194 | adequate | none(below_theta) |  |
| 6 | confirm_delivered_pallet(?pallet=pallet_0) | 0.3394 | adequate | none(below_theta) | projection_expired |
| 7 | confirm_delivered_pallet(?pallet=pallet_0) | 0.3622 | adequate | none(below_theta) |  |
| 8 | confirm_delivered_pallet(?pallet=pallet_0) | 0.3882 | adequate | none(below_theta) |  |
| 9 | confirm_delivered_pallet(?pallet=pallet_0) | 0.4175 | adequate | none(below_theta) |  |
| 10 | confirm_delivered_pallet(?pallet=pallet_0) | 0.4501 | adequate | none(below_theta) |  |
| 11 | confirm_delivered_pallet(?pallet=pallet_0) | 0.4857 | adequate | none(below_theta) |  |
| 12 | confirm_delivered_pallet(?pallet=pallet_0) | 0.5241 | adequate | none(below_theta) |  |
| 13 | confirm_delivered_pallet(?pallet=pallet_0) | 0.5645 | adequate | none(below_theta) |  |
| 14 | confirm_delivered_pallet(?pallet=pallet_0) | 0.6062 | adequate | none(below_theta) | projection_expired |
| 15 | confirm_delivered_pallet(?pallet=pallet_0) | 0.5875 | adequate | none(below_theta) |  |
| 16 | confirm_delivered_pallet(?pallet=pallet_0) | 0.5524 | adequate | none(below_theta) | projection_expired |
| 17 | confirm_delivered_pallet(?pallet=pallet_0) | 0.5037 | adequate | none(below_theta) |  |
| 18 | confirm_delivered_pallet(?pallet=pallet_0) | 0.4444 | adequate | none(below_theta) |  |
| 19 | confirm_delivered_pallet(?pallet=pallet_2) | 0.3789 | adequate | none(below_theta) | projection_expired |
| 20 | confirm_delivered_pallet(?pallet=pallet_2) | 0.3123 | adequate | none(below_theta) |  |
| 21 | confirm_delivered_pallet(?pallet=pallet_2) | 0.2495 | adequate | none(below_theta) |  |
| 22 | confirm_delivered_pallet(?pallet=pallet_2) | 0.1941 | adequate | none(below_theta) |  |
| 23 | confirm_delivered_pallet(?pallet=pallet_2) | 0.1479 | inadequate | none(below_theta) |  |
| 24 | confirm_delivered_pallet(?pallet=pallet_2) | 0.1111 | inadequate | none(below_theta) |  |
| 25 | confirm_delivered_pallet(?pallet=pallet_2) | 0.0826 | inadequate | none(below_theta) | projection_expired |
