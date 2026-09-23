# analysis/tc2c_scripts/play.md — T-C2c play: six scratch scripts

Play, cheap form: nothing measured, nothing judged, nothing a fixture. The six scripts were run unregistered (built in
memory from s00 / s10 / s80, the robot side unchanged); since registered as SCRIPT EXAMPLES in the author form, not
measured fixtures: 1 `scenario_84`, 2 `scenario_02`, 3 `scenario_85`, 4 `scenario_03`, 5 `scenario_12`, 6
`scenario_04`. The registered runs reproduce the runs below line for line (the header's scenario name aside).
`play.py <n>` runs play scenario n.
Code at feabe3d. One run each: prior on, `single_task`, cost realized, gate none, stop off; 2 and 6 also stop on.

    PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python analysis/tc2c_scripts/play.py 1 --steps 340 \
        --assignment_prior true --strategy single_task --cost_strategy realized --gate_strategy none --separation_stop false

Steps: 340 on env_layout8, 300 on env_layout0, 500 on env_layout1. Logs local.

NO SCRIPT FAILED TO LOAD AND NO PRIMITIVE FAILED AT RUN TIME. The anchors are action boundaries, so "turns" in 1
means after the walk to the first item is complete; there is no mid-walk turn in the vocabulary.

## 1. Change of mind before the pick-up (scenario_84, env_layout8)
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

## 2. Change of mind after the pick-up, the return case (scenario_02, env_layout0)
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

## 3. Wrong destination (scenario_85, env_layout8)
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

## 4. Landmark walk and stay mid-carry (scenario_03, env_layout0)
`interrupt(deliver(item_3), after="pick_up", with_=[MoveTo(corner_NE), Stay(30)])`, `deliver(item_2)`.
- Human: picks item_3 (41), walks to corner_NE with it (43–91), stands 30 (92–121), carries it to the table (122–144),
  then item_2 (146–206), stands at the table.
- Belief: `deliver_item(item_3)` leads to 87; `unknown` 88–134 (through the stay, frozen); `deliver_item(item_3)`
  again from 135, pinned at 144; `deliver_item(item_2)` then leads. recognition_changed: 20, 88, 142, 144, 160.
- Robot: item_7, item_6, item_4 (0, 34, 97); no hold. [sep] minimum 8.19 cm (204): the human arriving with item_2
  at the table where the finished robot stands; 99 ticks below 50 cm.
- Completion: 169.
- Odd: nothing beyond the known: the landmark detour reads as `unknown`, the stay mid-carry freezes it (TODO-85).

## 5. Coffee, a stay at the table, an abandon after pick-up (scenario_12, env_layout1)
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

## 6. Free actions, then the one assigned delivery (scenario_04, env_layout0)
`MoveTo(door)`, `Stay(20)`, `MoveTo(corner_SW)`, `deliver(item_3)`.
- Human: door (0–33), stands 20 (34–53), corner_SW (54–76), item_3 (77–84), places it (123), stands at the table.
- Belief: with one hypothesis in the prior, `deliver_item(item_3)` leads at 0.58–0.61 through the door walk and stay;
  `unknown` 71–81; `deliver_item(item_3)` from 82 (gate at 86), pinned at 123; then `unknown` 0.995 (hypothesis space
  exhausted, TODO-85 (b)). recognition_changed: 86, 123.
- Robot: item_7, item_6, item_4 (0, 34, 97); no hold. Stop off: [sep] minimum 22.8 cm (166), 135 ticks below 50 cm,
  at the table. Stop on: refused from 165 to the end (135, all `outside(no_projection)`), item_4 never delivered.
- Completion: 169 stop off; none in 300 stop on.
- Odd: the walk to the door is not read as `unknown`: the one live hypothesis keeps 0.58–0.61 against `unknown`.

## Four more, on layouts the script had not touched (7–10)

Same form: one run each, prior on, `single_task`, cost realized, gate none, stop off, 450 steps; `play.py 7` … `10`.
env_layout9 (tables against the walls, base s90) gained the five landmarks of env_layout0 for 9: corners 50 cm in
from both walls (±950, ±450), the door 20 cm inside the south wall (0, -480). scenario_90 is byte-identical with
and without them. The coffee-break shape runs on env_layout4 (base s40): its human has two assigned deliveries,
s70's on env_layout7 has one. No script failed to load, no primitive failed at run time.

### 7. Change of mind before the pick-up, tables at the walls (scenario_91, env_layout9)
`abandon(deliver(item_3), before="pick_up")`, `deliver(item_2)`.
- Human: walks to item_3 (0–77), turns, walks back to item_2 (78), picks it up (159), places it on kitting_table_0
  (182), stands there.
- Belief: `deliver_item(item_3)` leads to 91 (gate at 37); `unknown` 92–181 at 0.994, `deliver_item(item_2)` never
  recovers; after 182 the abandoned item_3 at 0.497. recognition_changed: 37, 92.
- Robot: item_5, item_4, item_6, item_1 (0, 79, 139, 245); no hold. [sep] minimum 30.2 cm (240), 8 ticks below 50 cm:
  its item_6 delivery at kitting_table_0, where the human stands.
- Completion: 365.
- Odd: as 1: the change of mind is not recognised.

### 8. Wrong destination, tables at the walls (scenario_92, env_layout9)
`deviate(deliver(item_2), destination=kitting_table_1)`, `deliver(item_3)`.
- Human: item_2 picked (9), carried the length of the room to kitting_table_1 (94), item_3 picked (142), placed on
  kitting_table_1 (189), stands there.
- Belief: `deliver_item(item_2)` leads to 40 (gate at 5); `unknown` 41–188; no pin at 94 (TODO-87); after item_3's
  pin at 189 `deliver_item(item_2)` leads again (item_2 lies on the wrong table). recognition_changed: 5, 41, 190.
- Robot: item_5, item_4, item_6, item_1 (0, 79, 139, 245); from 190 it plans against a projected human carrying item_2
  back (T_h 72.1), who stands; no hold. [sep] minimum 39.7 cm (362), 88 ticks below 50 cm, its last delivery at
  kitting_table_1 where the human stands.
- Completion: 365.
- Odd: as 3.

### 9. Landmark walk and stay mid-carry, tables at the walls (scenario_93, env_layout9)
`interrupt(deliver(item_2), after="pick_up", with_=[MoveTo(corner_NE), Stay(30)])`, `deliver(item_3)`.
- Human: item_2 picked (9), carried to corner_NE across the room (11–104), stands 30 (105–134), carries it back to
  kitting_table_0 (206), then item_3 to kitting_table_1 (315), stands there.
- Belief: `deliver_item(item_2)` leads to 47 (gate at 5); `unknown` 48–205, through the stay and the whole carry back
  (item_2 never recovers); after 206 `deliver_item(item_3)` (gate at 236); after 315 `unknown` 0.994 (hypothesis
  space exhausted). recognition_changed: 5, 48, 236, 315.
- Robot: item_5, item_4, item_6, item_1 (0, 79, 139, 245); no hold. [sep] minimum 33.2 cm (362), 88 ticks below 50 cm,
  at kitting_table_1.
- Completion: 365.
- Odd: unlike 4, the delivery is not recognised again when the human carries the item back: on this layout the detour
  is long enough that the evidence against it is not recovered before the release.

### 10. Coffee break, stay at the table, abandon after pick-up (scenario_41, env_layout4)
`interrupt(deliver(item_3), after="pick_up", with_=[coffee_break])`, `Stay(20)`, `abandon(deliver(item_6),
after="pick_up")`.
- Human: item_3 picked (60), carried to the coffee machine (62–107), waits (108–137), delivers item_3 (176), stands at
  the table 178–197, picks up item_6 (255) and stands there holding it to the end.
- Belief: `deliver_item(item_3)` leads (0.982 at the pick-up); on the walk to the machine it falls (0.811 at 100,
  0.539 at 130) and `unknown` rises (0.453 at 130); `coffee_break` stays at or below 0.001 from the pick-up on (0.076
  at 20). The coffee break's pin at 137 ends the episode (TODO-93); `deliver_item(item_3)` leads again and is pinned
  at 176; `deliver_item(item_6)` from 201, 0.982 frozen while the human holds it. recognition_changed: 30, 137, 170,
  176, 233.
- Robot: item_4, item_7, item_5 (0, 148, 247); no hold. [sep] minimum 177.6 cm: the robot never comes near.
- Completion: 379.
- Odd: `coffee_break` does not rise on the walk to the machine, unlike scenario_11 (0.345): the walk to item_3 had
  already refuted it, and nothing resets it before the detour.

## Twelve more, across layouts 2, 3, 4, 5, 7 and 9 (11–22)

Same form, 500 steps; `play.py 11` … `22`. Layouts 2, 3, 4, 5 and 7 gained the five landmarks (corners 50 cm in from
both walls, the door 20 cm inside the south wall); every regression fixture on them (s20, s30, s40, s50, s70, s71,
both priors; s20 and s70 under `full_reorder`) is byte-identical to its baseline with them. `scenario_21` exists (a
Phase 4C fixture), so layout2's three are 22–24. layout5 has one table, so its "wrong destination" is a change of
mind before the pick-up. s70's human is assigned one delivery; scenario_72 assigns it item_3 as well, for the
abandon. [sep] minima are given up to the robot's last release (after it, both stand at the table). No script failed
to load, no primitive failed at run time.

### 11. Landmark stay after the pick-up (scenario_22, env_layout2)
- Human: item_3 picked (22), carried to corner_SE (24–60), stands 30, back to the table (139), item_2 (205), stands.
- Belief: `deliver_item(item_3)` to 42; `unknown` 43–138 (not recovered on the carry back); item_2 after the pin;
  `unknown` 0.995 after 205. recognition_changed: 11, 43, 156, 205.
- Robot: item_4, item_6, item_7 (0, 62, 147); hold 7 at 11 (s20's). [sep] minimum 1.99 cm (233), the last delivery
  at the table the human stands at.
- Completion: 236.
- Odd: as 9.

### 12. Table stay, robot converging (scenario_23, env_layout2)
`deliver(item_3)`, `Stay(40)`, `deliver(item_2)`.
- Human: item_3 placed (54), stands at the table 56–95, item_2 placed (161), stands.
- Belief: item_3 pinned at 54, boundary; `deliver_item(item_2)` leads from 54 at the prior (0.498), clears θ at 111
  (on the walk); `unknown` 0.995 after 161. The stay is not evidence: the belief sits at the prior through it.
  recognition_changed: 11, 54, 111, 161.
- Robot: item_4, item_6, item_7 (0, 62, 147); holds 7 at 11 and 16 at 147, the second at the table, against the
  human's projected arrival with item_2. Stop off: [sep] minimum 3.85 cm (247). Stop on: 40 refusals during the stay
  (56–95), item_4 delivered at 101 once the human left, then refused from 161 to the end (316) at the human's final
  stand; one delivery of three.
- Completion: 250 stop off; none in 500 stop on.
- Odd: the mid-run stay is survived with the stop on; the end-of-script stand is not.

### 13. Change of mind before the pick-up (scenario_24, env_layout2)
- Human: walks toward item_3 (0–21), turns to item_2 (22), picks it (50), places it (84), stands.
- Belief: item_3 to 35; `unknown` 36–78; `deliver_item(item_2)` recovers at 79 (0.509), 5 ticks before its release;
  after 84 the abandoned item_3. recognition_changed: 11, 36, 82, 84.
- Robot: item_4, item_6, item_7; hold 7 at 11. [sep] minimum 1.1 cm (233), at the table.
- Completion: 236.
- Odd: a short first walk (22 ticks) lets the second task recover, late; in 1 and 7 (77 ticks) it never does.

### 14. Change of mind after the pick-up, the return (scenario_31, env_layout3)
- Human: item_3 picked (39), returned to shelf_3 (41–42), item_7 picked (70), placed (93), stands.
- Belief: item_3 to 63; `unknown` 64–67; `deliver_item(item_7)` 0.900 from 68. recognition_changed: 23, 64, 68, 93.
- Robot: item_4, item_2 (0, 83); hold 6 at 23. [sep] minimum 8.47 cm (23): s30's own crossing, the same tick and
  distance as s30's baseline, not the script's.
- Completion: 160.
- Odd: recovery is quick here (the return is 2 ticks).

### 15. Free actions, then the deliveries (scenario_32, env_layout3)
`MoveTo(door)`, `Stay(20)`, `MoveTo(corner_SW)`, `deliver(item_3)`, `deliver(item_7)`.
- Human: door (0–36), stands 20, corner_SW (57–79), item_3 (placed 128), item_7, stands.
- Belief: item_3 at ~0.35–0.5 through the free part, `unknown` 69–105, item_3 from 106, item_7 after 128.
  recognition_changed: 123, 128, 139.
- Robot: item_4, item_2 (0, 77); no hold. [sep] minimum 83.5 cm.
- Completion: 154.
- Odd: none.

### 16. Abandon after the pick-up, to a corner holding the item (scenario_42, env_layout4)
`deliver(item_3)`, `abandon(deliver(item_6), after="pick_up", then=[MoveTo(corner_SE)])`.
- Human: item_3 placed (115), item_6 picked (175), walks to corner_SE with it (177–) and stands there to the end.
- Belief: item_3 (low shares, 0.157 at the start: s40's wide space); item_6 from 121; `unknown` 0.517 from 192 on
  the walk to the corner, frozen there. recognition_changed: 30, 115, 153, 192.
- Robot: item_4, item_7, item_5 (0, 148, 247); no hold. [sep] minimum 73.3 cm.
- Completion: 379.
- Odd: none; the carried item never reaches a table and the belief stays `unknown`.

### 17. Change of mind before the pick-up (scenario_51, env_layout5)
- Human: toward item_2 (0–11), turns to item_3 (12), picks it (40), places it (72), stands.
- Belief: item_2 to 25; `unknown` 26–37; `deliver_item(item_3)` 0.865 from 38. After 72 `coffee_break` leads (0.332,
  the prior over the two hypotheses left). recognition_changed: 8, 26, 38, 72.
- Robot: item_4, item_6, item_7 (0, 55, 140); no hold. [sep] minimum 8.8 cm (140).
- Completion: 229.
- Odd: the first walk is 12 ticks and the second task is recognised 32 ticks before its release (cf. 13, 1).

### 18. Landmark stay mid-carry (scenario_52, env_layout5)
- Human: item_3 picked (22), to corner_NW (24–58), stands 30, back to the table (116), item_2 (184), stands.
- Belief: item_3 to 54; `unknown` 55–97; item_3 again from 98 (recovered on the carry back); item_2; `coffee_break`
  at the prior after 184. recognition_changed: 11, 55, 113, 116, 136, 184.
- Robot: item_4, item_6, item_7; hold 7 at 11. [sep] minimum 3.67 cm (233), at the table.
- Completion: 236.
- Odd: recovered here (a nearer corner), not in 9 and 11.

### 19. Table stay after the deliveries, then coffee (scenario_53, env_layout5)
`deliver(item_3)`, `deliver(item_2)`, `Stay(40)`, `coffee_break`.
- Human: item_3 (54), item_2 (121), stands 40 at the table (123–162), coffee break (216), stays at the machine.
- Belief: after 121 `coffee_break` leads at the prior (0.497) through the stay; pinned at 216; `unknown` 0.994 after.
  recognition_changed: 11, 54, 74, 121, 174, 216.
- Robot: item_4, item_6, item_7; hold 7 at 11. [sep] minimum 30.1 cm (147).
- Completion: 236.
- Odd: the stay ends by a walk the robot recognises, so the table is free for its last delivery (s50's design).

### 20. Coffee break, table stay, abandon (scenario_72, env_layout7)
- Human: item_5 picked (30), coffee machine 3 ticks away, waits (35–65), places item_5 (96), stands at the table 98–117,
  picks item_3 (far north) and stands holding it.
- Belief: `coffee_break` 0.985 at 33 (the machine is next to the shelf); pinned at 64, boundary (TODO-93); item_5
  0.762 by 81, pinned at 96; then `ac_activation` at the prior 0.332, below θ, through the table stay; item_3 from 118.
  recognition_changed: 23, 28, 33, 64, 81, 96, 140.
- Robot: item_1, item_2, item_1, item_2 (0, 23, 28, 105); holds 16 at 33 and 3 at 81. [sep] minimum 0.78 cm (100):
  after the boundary at 96 no projection is admitted, and the robot's carry to the table passes through the human
  standing at it.
- Completion: 195.
- Odd: the closest pass in the play set, and before the robot's completion (see below).

### 21. Free actions, then the delivery (scenario_73, env_layout7)
`MoveTo(door)`, `Stay(20)`, `MoveTo(corner_NW)`, `deliver(item_5)`.
- Human: door (0–32), stands 20, corner_NW across the whole room (53–159), item_5 (placed 277).
- Belief: `unknown` leads from 14 to the robot's end (173). recognition_changed: none.
- Robot: item_1, item_2 (0, 80); no hold. [sep] minimum 135.7 cm.
- Completion: 171 (the robot finishes before the human's delivery).
- Odd: none.

### 22. Table stay, robot converging (scenario_94, env_layout9)
`deliver(item_2)`, `deliver(item_3)`, `Stay(40)`, `MoveTo(corner_SE)`.
- Human: item_2 (33), item_3 to kitting_table_1 (144), stands there 146–185, walks to corner_SE, stands.
- Belief: item_3 at the prior from 33, clears θ at 64; `unknown` 0.994 after 144. recognition_changed: 5, 33, 64, 144.
- Robot: item_5, item_4, item_6, item_1 (0, 79, 139, 250); hold 7 at 139, at kitting_table_1 after its item_4
  delivery, against the human's projected arrival there: the robot stands at the human's destination and the human
  walks up to it (interrupted at 144 by the boundary). Stop off: [sep] minimum 1.1 cm (145). Stop on: refused 144–186
  (43) while the human stands, then continues.
- Completion: 370 stop off; 413 stop on.
- Odd: the first stop-on run in the play set that completes: the stay ends, and the stop waits it out.

## Across the twenty-two
- The script mechanism held: every shape loaded, expanded and ran; the return in 2 came from sequential expansion.
- A change of mind is not re-recognised (1, 2): the evidence the first walk laid against the second task persists
  with no boundary between them, so the robot sees `unknown` until the second task's release.
- The human's end-of-script stand at the table is the recurring proximity case, and with the stop on it deadlocks
  (2, 6, as scenario_01): the terminal stay of TODO-80.
- 7–10 add the same pattern from another side: evidence a walk lays against a hypothesis is not recovered without a
  boundary, so a change of mind (7), a long detour (9) and a foreseeable task after an unrelated walk (10) read as
  `unknown` rather than as the task the human is doing. Stop-on runs were not repeated for 7–9 (the human's terminal
  stand at a table the robot delivers to, as in 2 and 6).
- 11–22: a change of mind or a detour is recovered when the misleading walk is short (13, 14, 17, 18) and not when it
  is long (1, 7, 9, 11). After every episode boundary the belief sits at the prior, below θ, so no projection is
  admitted while the human stands where it just delivered; the robot's next carry to that table passes within
  centimetres of it (20: 0.78 cm, before the robot's completion). With the stop on, a stay that ends is waited out
  (12 in its middle part, 22); only the end-of-script stand deadlocks.
