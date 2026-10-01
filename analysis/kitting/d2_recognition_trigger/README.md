# D2 — `recognition_changed` replaces `theta_crossed`: the re-baselined sweep

> Superseding note (T-L stage 3, 26 Sept 2026): the layout and scenario ids here are the old ones; `docs/rename_table.md` maps them to the serial ids. The scripts and records stay frozen at their commit.

Regression sweep (`sweep/`: s00–s40, prior off / on, `analysis/f1_robot_responsible/sweep.sh` step counts)
and the evaluation fixtures (`fixtures/`: s50, s70, s71, `analysis/f47_fixtures/sweep.sh`) at the D2 HEAD,
PYTHONHASHSEED=0, gate_strategy none, cost_strategy realized, separation stop off. Logs are local
(git-ignored, as every baseline directory); regenerate with the two sweep scripts. Pre-D2 baselines: F1's
`realized_none/` (s00, s20, s30), TODO-32's s10, F47b's `baselines_s40/` and the F47b fixture runs — the
pre-D2 HEAD reproduced all of them byte-for-byte on the `[meta]` grep before the change.

The decision: `docs/design_decisions.md`, "What a trigger is an event of". The trigger fires when
`belief.most_likely` leaves the recorded projected hypothesis, or when a task hypothesis clears the gate
with none recorded. Retraction fires (admission then refuses) all decided a continue.

| condition | fires old → new (replaced trigger) | decisions vs old | completion old → new | note |
|---|---|---|---|---|
| s00_off | 5 → 4 | re-crossings 113 / 115 gone; retractions 78, 142 added | 166 → 168 | motion identical; completion declared by `no_current_task` |
| s00_on | 2 → 4 | retractions 78, 142 added | 168 | identical modulo reason string |
| s10_off | 6 → 7 | re-crossings 33 / 35 gone; 4 retractions added | 420 | motion identical |
| s10_on | 4 → 7 | 4 retractions added | 420 | identical modulo reason string |
| s20_off | 7 → 4 | 24 / 30 / 91 / 95 gone; 54, 122 added; hold at 20 uninterrupted (8, not 4 + 4) | 235 → 237 | motion identical; completion declared later |
| s20_on | 2 → 4 | 54, 122 added | 239 | identical modulo reason string |
| s30_off | 2 → 4 | 74, 121 added | 162 | identical modulo reason string |
| s30_on | 2 → 4 | 74, 121 added | 162 | identical modulo reason string |
| s40_off | 5 → 10 | 5 retractions added | 378 | identical modulo reason string |
| s40_on | 5 → 10 | 5 retractions added | 378 | identical modulo reason string |
| s50_off | 8 → 6 | as s20_off, plus retraction 178 | 235 → 237 | motion identical; completion declared later |
| s50_on | 3 → 6 | 3 retractions added | 237 | identical modulo reason string |
| s70_off | 5 → 6 | re-crossing 65 gone; 3 retractions added | 187 | motion identical |
| s70_on | 3 → 6 | 3 retractions added | 187 | identical modulo reason string |
| s71_off | 5 → 7 | 65 gone; 54, 95, 143 added; 72 item_5 re-enters after the grasp trigger at 69 admitted nothing (dip, 0.572) | 204 → 201 | hold's last tick replaced at 54; switch to item_3 at 108, was 111 |
| s71_on | 3 → 6 | 54, 95, 143 added | 204 → 203 | hold's last tick replaced at 54 (executed 31 of 32) |

"Completion declared later" (s00_off, s20_off, s50_off): the old `theta_crossed` on `unknown` at the robot's
own last delivery declared the empty pool on that tick; nothing enters on `unknown` now, so `no_current_task`
declares it two ticks later, when the executor's bookkeeping learns of the completion. `[sep]` is
byte-identical in those runs; the two trailing `[IR]` lines are the only other difference.
