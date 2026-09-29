# The meta-planner test-bed: report (MPB step 2, parts (iii) and (iv), 29 September 2026)

The recognition-to-planning chain with a working robot, one authored scenario per decision, against an oracle that
states the expected decision before the run. The instrument, its rules and their sources are in `README.md`; the
artefacts and their derivations are in `authoring.md`. Prior on is the primary set; α = 0.05, θ = 0.75, gate none,
cost realized, separation stop off.

**Result.**
- **All eleven scenarios are verified.** There are zero disagreements on parts 1 to 3 at exact equality on every tick
  and every decision, prior on, against the in-process run and against the log, under both strategies.
- Every declared part-4 property holds under single_task.
- No class-2 finding.
- The eleven: MPB scenarios 1 to 8; scenario_s11_01 and _02 re-authored in part (iv); scenario_s10_07 to _09 added in
  part (iv) for coverage.

## Results

| scenario | variant | ticks compared | decisions other than no_current_task, expected / actual | per-tick | decision | log | completion | holds (tick, ticks) | F1 viol/stand/recede | [sep] min, continuous (tick) |
|---|---|---|---|---|---|---|---|---|---|---|
| scenario_s10_01 | on, single_task | 204 | 11 / 11 | 0 | 0 | 0 | 161 | none | 0/0/0 | 383.99 (59) |
| scenario_s10_01 | on, full_reorder | 204 | 10 / 10 | 0 | 0 | 0 | 137 | none | 0/0/0 | 340.69 (59) |
| scenario_s10_02 | on, single_task | 204 | 7 / 7 | 0 | 0 | 0 | 66 | (25, 5) | 0/0/0 | 52.20 (47) |
| scenario_s10_02 | on, full_reorder | 204 | 7 / 7 | 0 | 0 | 0 | 66 | (25, 5) | 0/0/0 | 52.20 (47) |
| scenario_s10_03 | on, single_task | 292 | 13 / 13 | 0 | 0 | 0 | 172 | none | 0/0/0 | 408.88 (155) |
| scenario_s10_03 | on, full_reorder | 292 | 13 / 13 | 0 | 0 | 0 | 163 | none | 0/0/0 | 385.93 (5) |
| scenario_s10_04 | on, single_task | 281 | 13 / 13 | 0 | 0 | 0 | 161 | none | 0/0/0 | 383.99 (59) |
| scenario_s10_04 | on, full_reorder | 281 | 12 / 12 | 0 | 0 | 0 | 137 | none | 0/0/0 | 340.69 (59) |
| scenario_s10_05 | on, single_task | 265 | 11 / 11 | 0 | 0 | 0 | 161 | none | 0/0/0 | 383.99 (59) |
| scenario_s10_05 | on, full_reorder | 265 | 11 / 11 | 0 | 0 | 0 | 137 | none | 0/0/0 | 340.69 (59) |
| scenario_s10_06 | on, single_task | 193 | 10 / 10 | 0 | 0 | 0 | 161 | none | 0/0/0 | 349.00 (47) |
| scenario_s10_06 | on, full_reorder | 169 | 9 / 9 | 0 | 0 | 0 | 137 | none | 0/0/0 | 309.35 (52) |
| scenario_s10_07 | on, single_task | 266 | 12 / 12 | 0 | 0 | 0 | 161 | none | 0/0/0 | 405.43 (120) |
| scenario_s10_07 | on, full_reorder | 266 | 11 / 11 | 0 | 0 | 0 | 137 | none | 0/0/0 | 441.32 (184) |
| scenario_s10_08 | on, single_task | 252 | 12 / 12 | 0 | 0 | 0 | 167 | none | 0/0/0 | 316.43 (0) |
| scenario_s10_08 | on, full_reorder | 252 | 13 / 13 | 0 | 0 | 0 | 158 | none | 0/0/0 | 302.97 (2) |
| scenario_s10_09 | on, single_task | 239 | 13 / 13 | 0 | 0 | 0 | 161 | none | 0/0/0 | 387.55 (66) |
| scenario_s10_09 | on, full_reorder | 239 | 10 / 10 | 0 | 0 | 0 | 137 | none | 0/0/0 | 345.87 (71) |
| scenario_s11_01 | on, single_task | 164 | 5 / 5 | 0 | 0 | 0 | 74 | (33, 23) | 0/0/0 | 66.15 (56) |
| scenario_s11_01 | on, full_reorder | 164 | 5 / 5 | 0 | 0 | 0 | 74 | (33, 23) | 0/0/0 | 66.15 (56) |
| scenario_s11_02 | on, single_task | 201 | 17 / 17 | 0 | 0 | 0 | 169 | (14, 2), (20, 2), (25, 2), (27, 4), (31, 8), (39, 16), (55, 32) | 0/0/0 | 50.44 (24) |
| scenario_s11_02 | on, full_reorder | 151 | 14 / 14 | 0 | 0 | 0 | 99 | none | 0/0/0 | 146.77 (15) |

Notes on the table:
- **The per-tick columns:** the leader, the boundary, the adequacy finding (added in part (iv)), the gate, every live
  hypothesis's hypothesis adequacy and observation warrant, and the perception facts.
- **The decision columns:** part 1 as a set, parts 2 and 3 at every decision.
- **The horizon:** the first observed completion point + 30, capped at the steps (MPB-5).
- **In every run:**
  - the trajectory equals the run's human lines on every tick;
  - the in-process model lines are identical to the logged run's (the recorders changed nothing);
  - the oracle's process loaded none of the forbidden modules.
- **The rerun in part (iv).** All eleven were rerun under the instrument with the finding column. The six scenarios
  unchanged since part (iii) reproduce their 38 logs and `.rec` streams byte-identically. The re-authored pair's `.rec`
  streams are identical to part (iii)'s (the human's script is unchanged); their run logs changed.

**The invariant across strategies (MPB-6).** For each of the eleven:
- `expected_ticks.json` is byte-identical between single_task and full_reorder;
- the in-process per-tick human-side columns are identical over the common horizon;
- `trajectory.json` is byte-identical across all three variants of every scenario.

## Per scenario: the decision it exposes, expected and actual

Ticks are the oracle's, and every one equals the run's (single_task, prior on).

- **scenario_s10_01, admission after θ.**
  - (25, recognition_changed, entered | clears, deliver_item(item_1), commitment and observation | admitted).
  - (76, entered | clears, deliver_item(item_2) | admitted).
  - Fallback expiries before 25 at 2, 6 and 14. After: 61 replaced, 124 replaced, 126 entered (coffee_break on the exit
    walk), 157 retraction.
- **scenario_s10_02, the hold.**
  - (25, entered | clears, deliver_item(item_1) | admitted): winner deliver_item(item_7), **hold 5**.
  - **P2a holds.**
  - **P2b holds:** no F1 violation in its window, 26 to 63. The robot crosses at 52.20 cm, tick 47.
- **scenario_s10_03, the mid-action change.**
  - (25, entered); **(55, retraction | fallback moving, k = 10, end 66)**; **(66, projection_expired | coffee_break |
    fallback moving, k = 21, end 74.71)**; **(74, entered, coffee_break)**.
  - P3a, P3b and P3c hold (single_task): retention through a deviation, from 46 to 54. The delivery's observation
    warrant over that interval is `observation` throughout: entry-warranted.
- **scenario_s10_04, boundary re-admission on commitment.**
  - **(133, replaced | none(leader_no_observation), deliver_item(item_2) | fallback standing, k = 31)**.
  - **(134, entered | clears, deliver_item(item_2), commitment)**.
- **scenario_s10_05, the lone foreseeable hypothesis.**
  - **(124, replaced | none(leader_no_observation))**.
  - **(127, projection_expired | none(leader_unwarranted) | fallback standing, k = 5)**.
  - **(132, entered | coffee_break, observation)**.
- **scenario_s10_06, the control.**
  - **P8a, P8b and P8c hold under both strategies.** No hold. Completion equals the reference (161, or 137 with
    full_reorder), and so does every robot position.
- **scenario_s10_07, the sudden stand mid-carry** (part (iv)).
  - (25, entered).
  - **(62, retraction | none(leader_inadequate) | fallback standing, k = 17, end 80)**, 17 standing ticks into the
    stand, which began at 46.
  - (67, no_current_task | standing, k = 22).
  - **(90, projection_expired | standing, k = 45)**: the doubling.
  - (110, no_current_task | moving, k = 4); **(115, projection_expired | moving, k = 9)**: the resumed walk.
  - **(120, entered, deliver_item(item_1))**: only at the carry's advance to `place`.
  - (123, replaced) at the boundary; 127 and 131 expired.
  - **(138, entered, deliver_item(item_2))**, at b + 15: coffee_break is live after the boundary, so the prior gives each
    1/2.
  - full_reorder: 62 retraction, 72 no_current_task (standing, k = 27), 100 expiry (standing, k = 55), 116
    no_current_task (moving, k = 10), 120 entered, 123 replaced, 138 entered.
- **scenario_s10_08, the change of mind** (part (iv)).
  - (25, entered, item_1).
  - **(33, replaced | none(below_theta), coffee_break | fallback standing, k = 5)**. The return's place is a boundary,
    and coffee_break leads on the prior's tie order: the human's change from delivery 1 to delivery 2 passes through
    the coffee hypothesis in the recognizer's chain.
  - (37, no_current_task), (41, expired).
  - **(47, entered | clears, deliver_item(item_2), commitment and observation)**.
  - (108, replaced), (135, entered, item_1).
  - No retraction.
- **scenario_s10_09, the misdelivery** (part (iv)).
  - (25, entered).
  - **(60, retraction | none(leader_inadequate) | fallback moving, k = 29, end 71.99)**.
  - (67, no_current_task | refused); (72, 74, 78, 83, 93 expired).
  - **(102, entered, deliver_item(item_2))**.
  - No re-admission of item_1: its terminal fact never holds.
  - **X5's ground (1), measured:** the finding is unexplained from 60 to 72. The refused re-decisions inside are 60, 67
    and 72 (full_reorder: 60 and 72). The finding has outlived a re-decision from 61. This is an evidence line, not a
    mechanism.
- **scenario_s11_01, the occupied target** (re-authored).
  - Every decision is refused (`none(below_theta)`; the tie 0.498) and rests on a fallback stand: 0, 2, 6, 14, 30.
  - **P6.1 holds** (both strategies): the switch to deliver_item(item_9) at the expiry of 14, before the grasp of item_8
    (64), with the human standing.
  - **P6.2 holds** (single_task): item_8's hold is 0, 0, 0 at 0, 2, 6, and 7 at 14, against the layout's cost difference
    of 3.5. The fallback stand ends at 1 + k, so the hold is at most k + 1.
  - After the switch, at 33, the occupied task alone holds 23.
- **scenario_s11_02, walker and stander** (re-authored).
  - Every decision is refused and rests on the fallback.
  - The walk's expiries: 2, 6, 14 (k = 15, cut at door_N's radius, end 20), 20, 22.
  - The stand's expiries: 25, 27, 31, 39, 55, then 87 (k = 1, 3, 7, 15, 31).
  - Holds (single_task): 2, 2, 2, 4, 8, 16, 32.

## Disagreements, classified

- **Part (iii), scenario_s11_01 and scenario_s11_02 as first authored.** Class 1 and class 4, 426 and 485
  disagreements.
  - The human had no assigned tasks. An empty assignment switches the support restriction off
    (`shared/io_contracts.md` §2.1).
  - Class 1: the oracle's support rule lacked that clause; corrected with rule M0.
  - Class 4: MPB-3's precondition failed.
  - Remedy (Hadi): re-authored in part (iv) with an assigned delivery the human never performs. Now 0 disagreements.
- **Part (iv), authoring, scenario_s11_02 with item_12 on shelf_2.** Class 4, found before any run.
  - The exit walk passes within 2.3 cm of shelf_2, and the delivery was admitted at 97 (again at 101).
  - Stopped and reported; Hadi ruled shelf_1 (`authoring.md`, part (iv)).
- **scenario_s10_03 under full_reorder: P3a does not hold.**
  - The robot's own `no_current_task` falls at 48, inside 46 to 54.
  - P3 is declared for single_task, whose timing check keeps the interval clear.
  - Parts 1 to 3 agree exactly.
- **Deviations from the rulings' text, which are the oracle's values and stand:**
  - scenario_s10_07's item_2 at b + 15 (138), not b + 1;
  - scenario_s10_08's item_2 at 47, not the IR test-bed's 46: the output floor of this setup's five inadmissible robot
    items;
  - scenario_s10_09's retraction at 60.
- **Prior off (appendix, no ruling).** scenario_s10_02: P2b does not hold (3 F1 violations; the admission moves to 26,
  hold 4).

## AD3 and the skip rule

- **AD3** is not exercisable in the MPB set (Hadi, option (a); recorded under AD3).
  - Loss of observation warrant while still adequate requires an admission after less than about 167 cm of gain (at
    α = 0.05).
  - That occurs only for a lone hypothesis admitted at once, followed by a turn back: a foreseeable task on its first
    step, or a delivery on commitment at b + 1.
  - Measured on every run: no recorded hypothesis loses its observation warrant.
- **The skip rule** (class 3; recorded under P4; TODO-142).
  - It changes the fallback only on an arrival or pass-through tick; a ray leaving an object is already excluded by the
    direction test.
  - Its stated reason ("the human is leaving it") describes neither.
  - No decision fell on such a tick in any run. Alteration B2 is detected by none of the eleven.

## The alteration test (MPB-4), on the eleven

One rule altered at a time, in a scratch copy; disagreements against the unchanged actual files (prior on,
single_task).

| alteration | s10_01 | s10_02 | s10_03 | s10_04 | s10_05 | s10_06 | s10_07 | s10_08 | s10_09 | s11_01 | s11_02 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A1: the fallback's end without the observation offset | 18 | 13 | 18 | 20 | 19 | 20 | 21 | 22 | 23 | 15 | 38 |
| A2: the run length by exact direction equality | 170 | 74 | 155 | 143 | 157 | 114 | 110 | 180 | 174 | 20 | 76 |
| A3: a turn resets the run length to 0 | 167 | 73 | 151 | 143 | 159 | 111 | 108 | 174 | 167 | 18 | 111 |
| A4: landmarks not counted as fixed objects | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 14 |
| A5: projection_expired before recognition_changed | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| B1: the admitted plan without the method guards | 1 | 0 | 2 | 0 | 1 | 0 | 2 | 1 | 0 | 0 | 0 |
| B2: the ray does not skip an object containing its start | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| B3: the moving fallback not cut | 3 | 1 | 2 | 1 | 1 | 1 | 2 | 2 | 8 | 0 | 21 |
| C1: commitment warrant ignored | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C2: the movement source loosened | 58 | 58 | 141 | 158 | 126 | 0 | 120 | 100 | 226 | 38 | 180 |
| C3: warrant asked before adequacy | 3 | 1 | 1 | 1 | 56 | 3 | 1 | 1 | 0 | 0 | 0 |
| D1: no retraction | 1 | 0 | 3 | 0 | 0 | 1 | 1 | 0 | 1 | 0 | 0 |
| D2: boundary asked before replaced | 4 | 2 | 4 | 4 | 4 | 2 | 2 | 4 | 2 | 0 | 0 |

Every alteration is detected by at least one scenario except B2, a property of the test set (above).

## The reference run (the control)

scenario_s10_06's robot alone was built in-process and not registered.
- It loads and runs with no code change.
- Completion: 161 with single_task and 137 with full_reorder.
- Every decision `none(below_theta)`, no fallback, hold 0.

## The prior-off appendix (MPB-6; no oracle comparison, no ruling)

| scenario | completion | holds (tick, ticks) | near-encounters | F1 viol/stand/recede | [sep] min, continuous (tick) |
|---|---|---|---|---|---|
| scenario_s10_01 | 161 | none | 0 | 0/0/0 | 383.99 (59) |
| scenario_s10_02 | 65 | (26, 4) | 4 | 3/0/1 | 38.05 (47) |
| scenario_s10_03 | 172 | none | 0 | 0/0/0 | 408.88 (155) |
| scenario_s10_04 | 161 | none | 0 | 0/0/0 | 383.99 (59) |
| scenario_s10_05 | 161 | none | 0 | 0/0/0 | 383.99 (59) |
| scenario_s10_06 | 161 | none | 0 | 0/0/0 | 349.00 (47) |
| scenario_s10_07 | 161 | none | 0 | 0/0/0 | 405.43 (120) |
| scenario_s10_08 | 167 | none | 0 | 0/0/0 | 316.43 (0) |
| scenario_s10_09 | 161 | none | 0 | 0/0/0 | 387.55 (66) |
| scenario_s11_01 | 74 | (33, 23) | 0 | 0/0/0 | 66.15 (56) |
| scenario_s11_02 | 132 | (14, 2), (20, 2), (41, 14) | 0 | 0/0/0 | 53.42 (19) |

## The detectors and the parked items

- **TODO-134:** no instance in any run.
- **The arrival-tick ray:** no decision rested on one in any run.
- **TODO-132 (a), evidence from scenario_s11_02** (the re-authored scenario, verified), single_task:
  - The stand at spot_E begins at 26; its persistence breaks at 57.
  - The decisions on it: 27 (k = 3, hold 4), 31 (k = 7, hold 8), 39 (k = 15, hold 16), 55 (k = 31, projected to 87,
    hold 32).
  - The last hold runs past the break, 30 ticks beyond the stay.
  - Under full_reorder the robot is elsewhere at the stand: no hold.
  - scenario_s11_01 after its switch: at 33 the occupied task alone holds 23, against a stand projected to 68; the human
    stood until 59.
  - Nothing is concluded; the question returns to the design chat.

## The independence boundary, demonstrated

- The oracle's process imports `shared.types`, `shared.knowledge`, `shared.planner`, `domains.kitting.registry` and
  the IR test-bed's `oracle.py`.
- In every run it asserted at exit that none of these was loaded: `shared.meta_planner`, `shared.realization`,
  `shared.projection`, `shared.recognizer`, `shared.likelihood_functions`, `world.human_executor`, `mesa_sim.*`. A test
  checks the same in a clean interpreter.
- Its perception facts, ray and fallback are its own (M3 to M6).
- The chain assembly imports the standard library and `mpblib` only.

## Regression audit

- The suite: 211 passed.
- The four maintained sweeps: 96 of 96 logs and `.rec` streams byte-identical to their G-build md5s.
- No file under `shared/`, `mesa_sim/`, `world/` or the run loop changed.

## Runs (git-ignored; md5s)

```
68a56309456062f61ca91be9fc9b3e59  runs/env_layout_12_scenario_s10_01_off_single_task.log
2bcc18b57ef8bc2dd27581a67486122d  runs/env_layout_12_scenario_s10_01_on_full_reorder.log
9a35a1b15f37d877e865c301494d604c  runs/env_layout_12_scenario_s10_01_on_single_task.log
84243392243cb881655ec701edabb89a  runs/env_layout_12_scenario_s10_02_off_single_task.log
fbc98aba4a96f85e6dbd501175fb0651  runs/env_layout_12_scenario_s10_02_on_full_reorder.log
261221bbaaf4639801652a2b8003b69e  runs/env_layout_12_scenario_s10_02_on_single_task.log
8c685e811d98e7faf11937804ca3d03c  runs/env_layout_12_scenario_s10_03_off_single_task.log
a02bdb459fcb2d8b74898ab5ca90145a  runs/env_layout_12_scenario_s10_03_on_full_reorder.log
a9901a7af59ad78a65afc3179434a2e9  runs/env_layout_12_scenario_s10_03_on_single_task.log
5a3d61aefb5633013b05344313579b15  runs/env_layout_12_scenario_s10_04_off_single_task.log
74664de5ab8f8052bf494fb70af71328  runs/env_layout_12_scenario_s10_04_on_full_reorder.log
751eedb2c3ad3dbdeccf2b6abbdb3151  runs/env_layout_12_scenario_s10_04_on_single_task.log
477d1112d57bae236a295694383c2260  runs/env_layout_12_scenario_s10_05_off_single_task.log
fa1c28edcdda9ba7356d243787a3dfbd  runs/env_layout_12_scenario_s10_05_on_full_reorder.log
bacc21befccd638cfcd0f1101f805443  runs/env_layout_12_scenario_s10_05_on_single_task.log
fbf5a0c149c8fb5cf5abb3f1b5adc95c  runs/env_layout_12_scenario_s10_06_off_single_task.log
ac6e817d61791c9fd4b1d690983d26d4  runs/env_layout_12_scenario_s10_06_on_full_reorder.log
65a9facce7cdd1621a081aa1f7980890  runs/env_layout_12_scenario_s10_06_on_single_task.log
cd1e26dd376f01c48781e6cbeaafc612  runs/env_layout_12_scenario_s10_06_reference_full_reorder.log
a0df65782d76940a31cd5196a86f42f2  runs/env_layout_12_scenario_s10_06_reference_single_task.log
a0d489c9b0297049fcce7949bab37539  runs/env_layout_12_scenario_s10_07_off_single_task.log
0c75ad1e19299a1a72e315d5ac8395c8  runs/env_layout_12_scenario_s10_07_on_full_reorder.log
86a511f42b9eb6756cdcd6fb6e8d65fe  runs/env_layout_12_scenario_s10_07_on_single_task.log
9129312726660b5c5098d3122e447558  runs/env_layout_12_scenario_s10_08_off_single_task.log
af2c63635463036b61ccb2f03e81b675  runs/env_layout_12_scenario_s10_08_on_full_reorder.log
3edb658f33a62c60ecb8296c14b9c8c4  runs/env_layout_12_scenario_s10_08_on_single_task.log
4edb550f5d765a309eca536d5f501701  runs/env_layout_12_scenario_s10_09_off_single_task.log
08923e70b14546325cc4fa3007d14efa  runs/env_layout_12_scenario_s10_09_on_full_reorder.log
5728f8b4f018b256af74c47aa3de9744  runs/env_layout_12_scenario_s10_09_on_single_task.log
452622fae327fa490c1c6994a933df8e  runs/env_layout_12_scenario_s11_01_off_single_task.log
9d29f212dbd1ff55bc104fd3b2a36776  runs/env_layout_12_scenario_s11_01_on_full_reorder.log
60987425011281575480cc73a7c093ab  runs/env_layout_12_scenario_s11_01_on_single_task.log
af0d765662155e91d28ce4e5fee043af  runs/env_layout_12_scenario_s11_02_off_single_task.log
7ac2195a7811d1f4efca3021481b6fa8  runs/env_layout_12_scenario_s11_02_on_full_reorder.log
580ae9fd3ae2455d251086223a6c5867  runs/env_layout_12_scenario_s11_02_on_single_task.log
8451bf1f7048ec68b33375c2cc99cb15  runs/env_layout_12_scenario_s10_01_off_single_task.rec
8451bf1f7048ec68b33375c2cc99cb15  runs/env_layout_12_scenario_s10_01_on_full_reorder.rec
8451bf1f7048ec68b33375c2cc99cb15  runs/env_layout_12_scenario_s10_01_on_single_task.rec
321732473c562c43b06ae158ca81cdef  runs/env_layout_12_scenario_s10_02_off_single_task.rec
321732473c562c43b06ae158ca81cdef  runs/env_layout_12_scenario_s10_02_on_full_reorder.rec
321732473c562c43b06ae158ca81cdef  runs/env_layout_12_scenario_s10_02_on_single_task.rec
7fa9d641f1a0df5af13e70ec188ad19e  runs/env_layout_12_scenario_s10_03_off_single_task.rec
7fa9d641f1a0df5af13e70ec188ad19e  runs/env_layout_12_scenario_s10_03_on_full_reorder.rec
7fa9d641f1a0df5af13e70ec188ad19e  runs/env_layout_12_scenario_s10_03_on_single_task.rec
88dcf2598e25a94807b1e1f981218bff  runs/env_layout_12_scenario_s10_04_off_single_task.rec
88dcf2598e25a94807b1e1f981218bff  runs/env_layout_12_scenario_s10_04_on_full_reorder.rec
88dcf2598e25a94807b1e1f981218bff  runs/env_layout_12_scenario_s10_04_on_single_task.rec
c0b3c52826984a71c0637d8dfc8eba55  runs/env_layout_12_scenario_s10_05_off_single_task.rec
c0b3c52826984a71c0637d8dfc8eba55  runs/env_layout_12_scenario_s10_05_on_full_reorder.rec
c0b3c52826984a71c0637d8dfc8eba55  runs/env_layout_12_scenario_s10_05_on_single_task.rec
4bdc76ccc6f1ee3244e89c5458b19ffe  runs/env_layout_12_scenario_s10_06_off_single_task.rec
4bdc76ccc6f1ee3244e89c5458b19ffe  runs/env_layout_12_scenario_s10_06_on_full_reorder.rec
4bdc76ccc6f1ee3244e89c5458b19ffe  runs/env_layout_12_scenario_s10_06_on_single_task.rec
9f6bde960f345934b2423236f91fa158  runs/env_layout_12_scenario_s10_07_off_single_task.rec
9f6bde960f345934b2423236f91fa158  runs/env_layout_12_scenario_s10_07_on_full_reorder.rec
9f6bde960f345934b2423236f91fa158  runs/env_layout_12_scenario_s10_07_on_single_task.rec
33ee73bcf6ffefa2c81b3607397ac879  runs/env_layout_12_scenario_s10_08_off_single_task.rec
33ee73bcf6ffefa2c81b3607397ac879  runs/env_layout_12_scenario_s10_08_on_full_reorder.rec
33ee73bcf6ffefa2c81b3607397ac879  runs/env_layout_12_scenario_s10_08_on_single_task.rec
ebcb27b9f5dbf9cfcfa67e4b25a2ba3a  runs/env_layout_12_scenario_s10_09_off_single_task.rec
ebcb27b9f5dbf9cfcfa67e4b25a2ba3a  runs/env_layout_12_scenario_s10_09_on_full_reorder.rec
ebcb27b9f5dbf9cfcfa67e4b25a2ba3a  runs/env_layout_12_scenario_s10_09_on_single_task.rec
2b20839311f61f384b627483ddebc626  runs/env_layout_12_scenario_s11_01_off_single_task.rec
2b20839311f61f384b627483ddebc626  runs/env_layout_12_scenario_s11_01_on_full_reorder.rec
2b20839311f61f384b627483ddebc626  runs/env_layout_12_scenario_s11_01_on_single_task.rec
86397e984d81ec47aa978760989c152f  runs/env_layout_12_scenario_s11_02_off_single_task.rec
86397e984d81ec47aa978760989c152f  runs/env_layout_12_scenario_s11_02_on_full_reorder.rec
86397e984d81ec47aa978760989c152f  runs/env_layout_12_scenario_s11_02_on_single_task.rec
```
