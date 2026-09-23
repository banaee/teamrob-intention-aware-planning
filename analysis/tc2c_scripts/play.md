# analysis/tc2c_scripts/play.md — T-C2c play: six scratch scripts

Play, cheap form: nothing measured, nothing judged, nothing a fixture. The six scenarios are NOT registered: they are
built in `play.py` from s00 / s10 / s80 (robot side unchanged, the human's script and work order replaced), injected
into the kitting registry in memory as `scenario_91` … `scenario_96`, and run through the normal headless runner.
Code at feabe3d. One run each: prior on, `single_task`, cost realized, gate none, stop off; 92 and 96 also stop on.

    PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python analysis/tc2c_scripts/play.py scenario_91 --steps 340 \
        --assignment_prior true --strategy single_task --cost_strategy realized --gate_strategy none --separation_stop false

Steps: 340 on env_layout8, 300 on env_layout0, 500 on env_layout1. Logs local.

NO SCRIPT FAILED TO LOAD AND NO PRIMITIVE FAILED AT RUN TIME. The anchors are action boundaries, so "turns" in 1
means after the walk to the first item is complete; there is no mid-walk turn in the vocabulary.

## 1. Change of mind before the pick-up (91, env_layout8)
`abandon(deliver(item_3), before="pick_up")`, `deliver(item_0)`; both assigned.
- Human: walks to item_3 (0–76), turns without picking it up, walks to item_0 (77), picks it up (170), places it on
  kitting_table_0 (206), stands there.
- Belief: `deliver_item(item_3)` leads 0–90 (0.985 at 76, gate cleared at 37); `unknown` leads 91–205 at 0.994;
  `deliver_item(item_0)` stays at 0.001 throughout the walk to item_0 and its carry. At 206 item_0 pinned, boundary;
  the prior's one hypothesis left is the abandoned `deliver_item(item_3)`, 0.497, to the end.
  recognition_changed: 37 (gate cleared, item_3), 91 (below θ).
- Robot: item_6, item_1, item_7, item_4 (decisions 0, 40, 76, 162); projections at 37, 40, 76 only; no hold. [sep]
  minimum 38.3 cm (262), 78 ticks below 50 cm, the robot's last delivery at the table the human stands at.
- Completion (world fact): 265.
- Odd: the change of mind is never recognised. The walk to item_3 counted against `deliver_item(item_0)` and no
  boundary resets it, so the robot sees `unknown` for the whole second delivery.

## 2. Change of mind after the pick-up, the return case (92, env_layout0)
`abandon(deliver(item_3), after="pick_up", then=[deliver(item_2)])`.
- Human: picks up item_3 (41), returns it to shelf_3 (43–44: sequential expansion inserted the return), walks to
  item_2 (46), picks it up (81), places it (112), stands at the table.
- Belief: `deliver_item(item_3)` leads to 65 (gate cleared at 20); `unknown` 66–109 (0.951 at 100, `deliver_item(item_2)`
  0.045); `deliver_item(item_2)` leads only 110–111, two ticks before its release. After the boundary at 112 the
  abandoned `deliver_item(item_3)` leads at 0.498. recognition_changed: 20, 66.
- Robot: item_7, item_6, item_4 (0, 34, 97); no hold. Stop off: [sep] minimum 7.35 cm (166), 136 ticks below 50 cm,
  at the table the human stands at. Stop on: refused from 164 to the end (136, all `outside(no_projection)`), item_4
  never delivered.
- Completion: 169 stop off; none in 300 stop on.
- Odd: the return to the shelf is no boundary, so `deliver_item(item_2)` is not recognised on its own walk (as in 1).

## 3. Wrong destination (93, env_layout8)
`deviate(deliver(item_0), destination=kitting_table_1)`, `deliver(item_3)`.
- Human: item_0 picked (17), carried to kitting_table_1 (103), item_3 picked (131), placed on kitting_table_1 (158),
  stands there.
- Belief: `deliver_item(item_0)` leads to 49 (gate at 8); `unknown` 50–157. No pin and no boundary at 103 (TODO-87).
  item_3 pinned at 158, boundary; `deliver_item(item_0)` then returns to lead (0.905 at 200): item_0 lies on the
  wrong table, so its delivery to kitting_table_0 is still open. recognition_changed: 8, 50, 159.
- Robot: item_6, item_1, item_7, item_4 (0, 40, 76, 162); from 159 it plans against a projected human carrying item_0
  from kitting_table_1 to kitting_table_0 (T_h 76.65), who in fact stands still; no hold. [sep] minimum 26.0 cm (157).
- Completion: 265.
- Odd: after the misdelivery the robot's projection is of a task the human will not do (TODO-87's consequence).

## 4. Landmark walk and stay mid-carry (94, env_layout0)
`interrupt(deliver(item_3), after="pick_up", with_=[MoveTo(corner_NE), Stay(30)])`, `deliver(item_2)`.
- Human: picks item_3 (41), walks to corner_NE with it (43–91), stands 30 (92–121), carries it to the table (122–144),
  then item_2 (146–206), stands at the table.
- Belief: `deliver_item(item_3)` leads to 87; `unknown` 88–134 (through the stay, frozen); `deliver_item(item_3)`
  again from 135, pinned at 144; `deliver_item(item_2)` then leads. recognition_changed: 20, 88, 142, 144, 160.
- Robot: item_7, item_6, item_4 (0, 34, 97); no hold. [sep] minimum 8.19 cm (204): the human arriving with item_2
  at the table where the finished robot stands; 99 ticks below 50 cm.
- Completion: 169.
- Odd: nothing beyond the known: the landmark detour reads as `unknown`, the stay mid-carry freezes it (TODO-85).

## 5. Coffee, a stay at the table, an abandon after pick-up (95, env_layout1)
`interrupt(deliver(item_2), after="pick_up", with_=[coffee_break])`, `Stay(20)`, `abandon(deliver(item_5),
after="pick_up")`.
- Human: as scenario_11 to the release of item_2 (124), stands at the table 126–145, walks to item_5 (146), picks it
  up (207), and stands there holding it to the end (script ended).
- Belief: as scenario_11 to 124 (the coffee break's pin ends the episode at 75, TODO-93); `deliver_item(item_5)` leads
  from 146 to the end, rising 0.355 → 0.981 and frozen at 0.981 once the human stands holding it. recognition_changed: 24, 75, 100, 124,
  176.
- Robot: item_7, item_6, item_1, item_4 (0, 75, 169, 286); no hold. [sep] minimum 236.6 cm: the robot never comes
  near the table stay or the shelf.
- Completion: 422.
- Odd: the robot plans to the end against a human projected to deliver item_5, who stands holding it (the TODO-85
  mid-carry case, with no end).

## 6. Free actions, then the one assigned delivery (96, env_layout0)
`MoveTo(door)`, `Stay(20)`, `MoveTo(corner_SW)`, `deliver(item_3)`.
- Human: door (0–33), stands 20 (34–53), corner_SW (54–76), item_3 (77–84), places it (123), stands at the table.
- Belief: with one hypothesis in the prior, `deliver_item(item_3)` leads at 0.58–0.61 through the door walk and stay;
  `unknown` 71–81; `deliver_item(item_3)` from 82 (gate at 86), pinned at 123; then `unknown` 0.995 (hypothesis space
  exhausted, TODO-85 (b)). recognition_changed: 86, 123.
- Robot: item_7, item_6, item_4 (0, 34, 97); no hold. Stop off: [sep] minimum 22.8 cm (166), 135 ticks below 50 cm,
  at the table. Stop on: refused from 165 to the end (135, all `outside(no_projection)`), item_4 never delivered.
- Completion: 169 stop off; none in 300 stop on.
- Odd: the walk to the door is not read as `unknown`: the one live hypothesis keeps 0.58–0.61 against `unknown`.

## Across the six
- The script mechanism held: every shape loaded, expanded and ran; the return in 2 came from sequential expansion.
- A change of mind is not re-recognised (1, 2): the evidence the first walk laid against the second task persists
  with no boundary between them, so the robot sees `unknown` until the second task's release.
- The human's end-of-script stand at the table is the recurring proximity case, and with the stop on it deadlocks
  (2, 6, as scenario_01): the terminal stay of TODO-80.
