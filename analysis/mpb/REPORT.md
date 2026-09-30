# The meta-planner test-bed: report (MPB step 2, parts (iii) to (v), 29 to 30 September 2026)

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
- **Part (v): the five claimed cells of the coverage matrix are verified** (scenario_s12_01, _02, scenario_s11_03,
  scenario_s10_10, _11; the section "Part (v)" below). Zero disagreements on parts 1 to 3 under both strategies, prior
  on; every declared part-4 property holds under single_task. With them every materially distinct in-scope decision
  path of `coverage.md` is verified, unreachable with a recorded derivation, or outside the claimed mechanism with a
  recorded reason: **the MPB is closed.**

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

## The alteration test (MPB-4), on the sixteen (part (v); the eleven in part (iv))

One rule altered at a time, in a scratch copy; disagreements against the unchanged actual files (prior on,
single_task). Rerun on the sixteen in part (v); the eleven's columns reproduce part (iv)'s exactly.

| alteration | s10_01 | s10_02 | s10_03 | s10_04 | s10_05 | s10_06 | s10_07 | s10_08 | s10_09 | s10_10 | s10_11 | s11_01 | s11_02 | s11_03 | s12_01 | s12_02 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1: the fallback's end without the observation offset | 18 | 13 | 18 | 20 | 19 | 20 | 21 | 22 | 23 | 17 | 15 | 15 | 38 | 14 | 16 | 20 |
| A2: the run length by exact direction equality | 170 | 74 | 155 | 143 | 157 | 114 | 110 | 180 | 174 | 148 | 159 | 20 | 76 | 59 | 136 | 144 |
| A3: a turn resets the run length to 0 | 167 | 73 | 151 | 143 | 159 | 111 | 108 | 174 | 167 | 146 | 164 | 18 | 111 | 57 | 135 | 143 |
| A4: landmarks not counted as fixed objects | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 14 | 2 | 0 | 0 |
| A5: projection_expired before recognition_changed | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| B1: the admitted plan without the method guards | 1 | 0 | 2 | 0 | 1 | 0 | 2 | 1 | 0 | 2 | 1 | 0 | 0 | 0 | 0 | 1 |
| B2: the ray does not skip an object containing its start | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| B3: the moving fallback not cut | 3 | 1 | 2 | 1 | 1 | 1 | 2 | 2 | 8 | 1 | 1 | 0 | 21 | 2 | 1 | 1 |
| C1: commitment warrant ignored | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 2 | 16 | 0 | 0 | 0 | 0 | 4 |
| C2: the movement source loosened | 58 | 58 | 141 | 158 | 126 | 0 | 120 | 100 | 226 | 135 | 202 | 38 | 180 | 38 | 58 | 158 |
| C3: warrant asked before adequacy | 3 | 1 | 1 | 1 | 56 | 3 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 3 | 1 |
| D1: no retraction | 1 | 0 | 3 | 0 | 0 | 1 | 1 | 0 | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| D2: boundary asked before replaced | 4 | 2 | 4 | 4 | 4 | 2 | 2 | 4 | 2 | 4 | 2 | 0 | 0 | 0 | 4 | 4 |

Every alteration is detected by at least one scenario except B2, a property of the test set (above); the five of part
(v) do not change that.

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

## Coverage (post-(iv) records, 29 September 2026)

The coverage matrix is `coverage.md`: 47 rows, derived from the committed outputs of the 22 prior-on runs (no run).
31 verified, 5 unreachable with a derivation, 4 out of coverage with a reason, 5 reachable and claimed with no
instance (ruled by Hadi for part (v)), 1 reachable and not claimed (P3), 1 not a distinct path.

Three facts of the whole set:
- The cause boundary fired in no run.
- Every admitted record ended before its T_h (at a replaced boundary, a retraction or the robot's own decision).
- No record was kept through a dip below θ: on every tick a record stood, its hypothesis led and the gate cleared.

X5's ground (2), measured (new at this step): in scenario_s11_02, single_task, every candidate's realized plan holds at
the expiries of 25, 27, 31, 39 and 55 (two candidates each; `[meta-cand] delta=`), so the ground holds at a decision and
at the next re-decision from 25 on, until 87 (hold 0). An evidence line, not a mechanism; full_reorder logs no
per-candidate hold (TODO-141).

## Part (v): the five claimed cells (30 September 2026)

One authored instance for each reachable decision path the coverage matrix found without an instance and the
contribution claims (`coverage.md`; Hadi's rulings of 29 September 2026). The artefacts and their pre-run derivations
are in `authoring.md`, part (v).

| scenario | cell | variant | ticks compared | decisions other than no_current_task, expected / actual | per-tick | decision | log | completion | holds (tick, ticks) | F1 viol/stand/recede | [sep] min, continuous (tick) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| scenario_s12_01 | D8 | on, single_task | 204 | 11 / 11 | 0 | 0 | 0 | 131 | none | 0/0/0 | 87.57 (79) |
| scenario_s12_01 | D8 | on, full_reorder | 204 | 10 / 10 | 0 | 0 | 0 | 135 | (26, 4), (76, 7) | 3/0/1 | 38.05 (47) |
| scenario_s12_02 | C2 | on, single_task | 281 | 14 / 14 | 0 | 0 | 0 | 161 | (76, 18), (133, 30), (134, 7), (135, 2), (137, 4) | 1/2/1 | 32.26 (140) |
| scenario_s12_02 | C2 | on, full_reorder | 281 | 14 / 14 | 0 | 0 | 0 | 161 | the same | 1/2/1 | 32.26 (140) |
| scenario_s11_03 | D9 | on, single_task | 164 | 5 / 5 | 0 | 0 | 0 | 113 | (6, 3), (14, 16), (53, 43) | 0/0/0 | 51.33 (13) |
| scenario_s11_03 | D9 | on, full_reorder | 164 | 5 / 5 | 0 | 0 | 0 | 113 | the same | 0/0/0 | 51.33 (13) |
| scenario_s10_10 | E6 | on, single_task | 282 | 13 / 13 | 0 | 0 | 0 | 171 | none | 0/0/0 | 352.81 (1) |
| scenario_s10_10 | E6 | on, full_reorder | 282 | 13 / 13 | 0 | 0 | 0 | 162 | none | 0/0/0 | 320.43 (4) |
| scenario_s10_11 | A4 | on, single_task | 215 | 11 / 11 | 0 | 0 | 0 | 161 | none | 0/0/0 | 411.19 (127) |
| scenario_s10_11 | A4 | on, full_reorder | 215 | 9 / 9 | 0 | 0 | 0 | 137 | none | 0/0/0 | 437.79 (134) |

In every run the trajectory equals the run's human lines on every tick, the in-process model lines equal the logged
run's, and the oracle's process loaded none of the forbidden modules. The expected per-tick tables are byte-identical
between the strategies.

### Per cell: expected and actual

Single_task, prior on; every tick equals the oracle's.

- **D8, the switch against an admitted projection (scenario_s12_01).**
  - Decisions before the admission at 0, 2, 6 and 14: fallbacks, both tasks hold 0, item_7 wins (cost difference
    1.568).
  - **26, entered (deliver_item(item_1), commitment and observation): item_7's hold is 4, above the authored difference
    of 2.499, and the winner switches to item_13 with hold 0.** item_7 is grasped only at 96.
  - P12.1a and P12.1b hold.
  - The admission is at 26, not scenario_s10_02's 25: env_setup_12's output floor (seven keys against five), found
    before the run (`authoring.md`).
- **C2, the hold against an admitted standing segment (scenario_s12_02).**
  - **76, entered (coffee_break, observation): item_14's hold is 18.** The robot is mid-walk to shelf_10 and would have
    passed the waiting point inside the admitted wait (104 to 134).
  - The robot comes within 50 cm of the waiting point on 142 to 146, after the human left it at 135.
  - No F1 violation in the window 77 to 135.
  - P12.2a to P12.2c hold.
- **D9, the switch while carrying (scenario_s11_03).**
  - item_8 is grasped at 4.
  - The expiries while carrying: 6 (hold 3, return difference 9.08) and 14 (hold 16, return difference 16.36), both
    continue.
  - **30 (k = 31): hold 32, above 16.36: the switch to item_9 while carrying**, under both strategies.
  - item_8 is released at shelf_3 at 35 (19.4 cm from it); item_9 is grasped at 41.
  - P11.3a to P11.3c hold. At 14 the margin was 0.36 ticks, as the pre-run derivation flagged.
- **E6, a record kept through a dip below θ (scenario_s10_10).**
  - **25, entered; no decision from 26 to 36; the record stays deliver_item(item_1)** through the proximity regress at
    31 (no observation) and **the dip at 34 to 36** (item_1 leads below θ, adequate).
  - **37, replaced** (coffee_break overtakes).
  - P10.10 holds under both strategies.
- **A4, the cause boundary (scenario_s10_11, env_layout_13).**
  - 7, entered (item_1).
  - **53, recognition_changed with cause boundary**: item_1 placed at kitting_table_3, not pinned, leads the reset's
    tie; the gate refuses below θ, a standing fallback.
  - Then 60 entered (item_2), 135 replaced, 136 entered (item_1, commitment), 147 retraction.
  - The first instance of the cause in any MPB run, under both strategies.

### Classified

- **scenario_s12_01 under full_reorder: P12.1a does not hold.** Not a disagreement: parts 1 to 3 agree exactly, and
  MPB-6 does not require full_reorder to reproduce every part-4 property (as scenario_s10_03's P3a).
  - The candidate is the ordering, and its tail's return walks enter the cost. At 26, [item_7, item_13] costs 103.93
    (its hold 4 included) against 105.25 for [item_13, item_7], so the head stays item_7.
  - The switch is a single_task property by the authored parameter: the difference is set between the two tasks, not
    between the two orderings.
- **scenario_s12_01 under full_reorder: three F1 robot violations inside the admission's assessed window.** Checked
  (below). CLASS 2, READING (a) (Hadi, 30 September 2026), corrected: the section "The class-2 correction".
  - The decision of 26 keeps item_7 with a hold of 4 (its window 27 to 63). The robot passes the crossing at 45 to 47
    within 50 cm of the human's carry, 38.05 cm at its closest.
  - The same pattern as scenario_s10_02 prior off in part (iii) (the admission at 26, hold 4, three violations). The
    hold of 5 from 25 (scenario_s10_02 prior on) kept the separation.
  - No declared property covers it: P12.1a is single_task's.
  - **The check (30 September 2026).** The run was re-executed in-process (the headless log and `.rec` byte-identical
    to the committed ones; the in-process model lines identical to the log) with a recorder on `realize()` at 26. The
    projection clock, established on the data: step s is the end of world tick 25 + s. Since the close-out the values
    are saved in `actual_decisions.json` (`human_segments`, `robot_segments`) and the check is read-only.

    | tick | projected human / actual human (gap) | planned robot / executed robot (gap) | planned separation, end / min over the tick | executed separation, end / min |
    |---|---|---|---|---|
    | 45 | (−204.8, 5.5) / (−207.1, 3.0) (3.4) | (−159.7, −48.1) / (−174.1, −34.3) (20.0) | 70.07 / 70.07 | 49.83 / 49.83, viol |
    | 46 | (−191.0, 20.0) / (−193.3, 17.5) (3.4) | (−174.1, −34.3) / (−188.6, −20.5) (20.0) | 56.82 / 56.82 | 38.25 / 38.25, viol |
    | 47 | (−177.1, 34.4) / (−179.5, 31.9) (3.4) | (−188.6, −20.5) / (−203.0, −6.7) (20.0) | 56.09 / 54.64 | 45.18 / 38.05, viol |

    - The plan satisfies F1: its minimum over the assessed window is 54.64 cm (tick 46.55).
    - The executed robot runs one step ahead of its plan. After the hold, the plan prices three stationary ticks before
      the carry (a zero-length walk segment, then three one-tick segments); the body spends two, the grasp at 30 and
      its acknowledgement at 31, and steps at 32. The walk's acknowledgement was spent at 25, before the decision. The
      signature is TODO-77's "projection running long" (its skipped-acknowledgement bullet, fixed in the body at
      T-B Q7); whether it is that case is not established.
    - The human's projection is 3.4 cm off the actual human on every tick: the projected walk ends 1.7 cm short of the
      body's last step, and the projected carry starts at step 5.914 (tick 30.9) against the body's first carry step on
      tick 32.
    - Crossed: the planned robot against the actual human gives 69.8, 55.2, 53.2 cm (no violation); the executed robot
      against the projected human gives 50.2, 40.5, 48.6 cm (the violations). The robot's one-tick lead produces them.
    - By the rule the check was run under, this is reading (c) (projected differs from actual): the difference
      reported, no class assigned. scenario_s10_02 prior off is the same decision (a hold of 4 from 26 at the same
      position, identical executed separations at 45 to 48); it takes the same reading.
- **scenario_s12_02: a near-encounter after the declared window, class 5.**
  - 33.61 cm at 139, one F1 robot violation, 138 to 140.
  - The human leaves the machine at 135 and walks north-east toward shelf_2, toward the robot carrying west along the
    route.
  - The decisions it rests on are 135 (replaced, a moving fallback with k = 1, hold 2) and 137 (expired, k = 3, hold 4).
    That is P4's recorded known error (little evidence protects little) and X3's case (the human walking toward the
    robot; TODO-135). Recorded, not designed for.
- **scenario_s12_02: TODO-132 (a) again** (ruling 2: recorded, not the property). At 133, the coffee break's boundary,
  the fallback stand of k = 31 is projected to 165 and sends a hold of 30. The human leaves at 135.
- No class-2 finding.

### Prior off (appendix, no oracle comparison, no ruling)

| scenario | completion | holds (tick, ticks) | near-encounters | F1 viol/stand/recede | [sep] min, continuous (tick) |
|---|---|---|---|---|---|
| scenario_s12_01 | 134 | (27, 6), (96, 6) | 0 | 0/0/0 | 52.20 (47) |
| scenario_s12_02 | 184 | (91, 18), (133, 30) | 4 | 0/4/0 | 33.61 (139) |
| scenario_s11_03 | 113 | (6, 3), (14, 16), (53, 43) | 0 | 0/0/0 | 51.33 (13) |
| scenario_s10_10 | 171 | none | 0 | 0/0/0 | 352.81 (1) |
| scenario_s10_11 | 161 | none | 0 | 0/0/0 | 411.19 (127) |

Prior off, scenario_s12_01's admission falls at 27, after item_7's grasp at 26, so P12.1a does not hold there.

### The whole-set facts, re-measured on the sixteen (32 prior-on runs)

- The cause boundary fires in scenario_s10_11 only (53, both strategies).
- Every admitted record still ends before its T_h: no P3 exposure.
- The only record kept while the gate refuses is scenario_s10_10's (31, 34 to 36).

### Regression audit, part (v)

- **The suite:** 211 passed. The discovery test's inventory is 71 scenarios, setups 01 to 12.
- **The eleven verified scenarios**, rerun under all three variants: every log, `.rec` stream and reference log
  byte-identical to part (iv)'s md5s (68 of 68), and no committed output changed.
- **The four maintained sweeps:** 96 of 96 logs and `.rec` streams byte-identical to their G-build baselines.
- No file under `shared/`, `mesa_sim/`, `world/` or the run loop changed.

## The class-2 correction (30 September 2026)

Objection 1 of part (v) (scenario_s12_01, full_reorder: three F1 robot violations inside the admission's window) is
**class 2, reading (a)** (Hadi, 30 September 2026): the implementation departs from the ruling. The invariant: the
trajectory realize() assesses is the trajectory the robot executes from the decision tick onward. The evidence was the
cross-pairing (part (v), "Classified"): the plan kept 54.64 cm, the executed robot ran one step ahead of it.

**The family, measured before the fix on the saved segments** (the lag of the executed robot against its plan at its
first executed move after each admitted decision, the 32 prior-on runs):

| state at the decision | lag | decisions |
|---|---|---|
| (a) after a walk's acknowledgement, the next (stationary) action not begun | +1 (the plan one tick long: it re-priced the completed walk and its acknowledgement) | s12_01 full_reorder 26 |
| (b) on a pick_up's acknowledgement tick | −1 (an owed acknowledgement no plan stated) | s10_01 full_reorder 126, s10_06 14, s10_11 full_reorder 7 |
| (c) on a finished task's completion tick; the tick after a release | −1; −2 | s10_10 40; s10_03 121, s10_08 full_reorder 135 |

**The fix** (design_decisions.md, "Realization as built", the dated correction): the body reports its owed completion
ticks and the action in flight (`ExecutorState`); every robot candidate's projection states the owed ticks first, and
the continued task is projected from the action in flight; the executor spends owed ticks before a hold. Tests:
`tests/test_executed_is_assessed.py`.

**Re-verification of the sixteen** (rerun under all three variants):
- Parts 1 to 3: zero disagreements in all 32 prior-on comparisons. The expected per-tick tables are unchanged. One chain
  moved with the robot's own `no_current_task` ticks: scenario_s12_01 full_reorder, where the robot now finishes at
  67, whose decision is `no_current_task` masking the expiry that fired there before.
- Part 4: every declared property holds under single_task, as before. P12.1b: item_7's hold at the admission is 5
  (was 4), above the 2.499-tick difference. The known exceptions stand: P3a under full_reorder, P12.1a under
  full_reorder and prior off.
- Positions moved in two runs only:
  - scenario_s12_01 full_reorder: holds 4 → 5 at 26 and 7 → 6 at 76; F1 3/0/1 → 0/0/0; the `[sep]` minimum
    38.05 → 52.20 cm; completion 135 as before.
  - scenario_s10_02 prior off (appendix): hold 4 → 5 at 26; F1 3/0/1 → 0/0/0; the `[sep]` minimum 38.05 → 52.20 cm;
    completion 65 → 66; P2b now holds.
- In four runs only labels moved: scenario_s10_02 under both strategies, scenario_s11_02 prior off, scenario_s12_01
  prior off. The owed acknowledgement is now spent before the hold, so two ticks swap their microaction label; every
  position is the same. In scenario_s12_01 prior off the holds read 5 instead of 6: one owed tick plus 5, the same six
  standing ticks.
- The `.rec` streams are byte-identical in all 48; every `[IR*]` line prior on is byte-identical.

**The cross-pairing re-checked** (scenario_s12_01 full_reorder, read from the saved segments; step s = end of world tick
25 + s):

| tick | projected human / actual human (gap) | planned robot / executed robot (gap) | planned separation | executed separation, end / min |
|---|---|---|---|---|
| 45 | (−204.8, 5.5) / (−207.1, 3.0) (3.4) | (−159.7, −48.1) / (−159.7, −48.1) (0.0) | 70.07 | 69.78 / 69.78 |
| 46 | (−191.0, 20.0) / (−193.3, 17.5) (3.4) | (−174.1, −34.3) / (−174.1, −34.3) (0.0) | 56.82 | 55.23 / 55.23 |
| 47 | (−177.1, 34.4) / (−179.5, 31.9) (3.4) | (−188.6, −20.5) / (−188.6, −20.5) (0.0) | 56.09 | 53.19 / 52.20 |

The planned and the executed robot are equal from 26 to the end of the first walk. The 3.4 cm is the P-side residual
(design_decisions.md, the class-2 record; TODO-146), not the cause.

**scenario_s10_02 prior off, re-read.** It was the same decision (a hold of 4 from 26 at the same position). It now
holds 5, the executed robot keeps 52.20 cm, and there are no violations.

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

## Runs (git-ignored; md5s; regenerated at the class-2 correction, 30 September 2026)

```
ff405ae96bb70aa1901043a79b47ac47  runs/env_layout_12_scenario_s10_01_off_single_task.log
8451bf1f7048ec68b33375c2cc99cb15  runs/env_layout_12_scenario_s10_01_off_single_task.rec
3c1e7bc66dd09ab3aa8228a0f93cbf0d  runs/env_layout_12_scenario_s10_01_on_full_reorder.log
8451bf1f7048ec68b33375c2cc99cb15  runs/env_layout_12_scenario_s10_01_on_full_reorder.rec
ad1a4020ff0da1eb5d4dbfcafe60361e  runs/env_layout_12_scenario_s10_01_on_single_task.log
8451bf1f7048ec68b33375c2cc99cb15  runs/env_layout_12_scenario_s10_01_on_single_task.rec
815dee9bd3b3ecfe86a4c7b56139839b  runs/env_layout_12_scenario_s10_02_off_single_task.log
321732473c562c43b06ae158ca81cdef  runs/env_layout_12_scenario_s10_02_off_single_task.rec
a0a6bff6d1a3f73149eab2b80859940b  runs/env_layout_12_scenario_s10_02_on_full_reorder.log
321732473c562c43b06ae158ca81cdef  runs/env_layout_12_scenario_s10_02_on_full_reorder.rec
ed061081de759217002890ab9ba36c5e  runs/env_layout_12_scenario_s10_02_on_single_task.log
321732473c562c43b06ae158ca81cdef  runs/env_layout_12_scenario_s10_02_on_single_task.rec
497ea01b58f671b2fa1d852ea31d877d  runs/env_layout_12_scenario_s10_03_off_single_task.log
7fa9d641f1a0df5af13e70ec188ad19e  runs/env_layout_12_scenario_s10_03_off_single_task.rec
a02bdb459fcb2d8b74898ab5ca90145a  runs/env_layout_12_scenario_s10_03_on_full_reorder.log
7fa9d641f1a0df5af13e70ec188ad19e  runs/env_layout_12_scenario_s10_03_on_full_reorder.rec
0ac37ed728ba00ccfa741a444da20206  runs/env_layout_12_scenario_s10_03_on_single_task.log
7fa9d641f1a0df5af13e70ec188ad19e  runs/env_layout_12_scenario_s10_03_on_single_task.rec
2d9aeecce69f7a802ece0c16c2edcfdc  runs/env_layout_12_scenario_s10_04_off_single_task.log
88dcf2598e25a94807b1e1f981218bff  runs/env_layout_12_scenario_s10_04_off_single_task.rec
e4a8db77bdad1a6dd1f5aeaabdb39b12  runs/env_layout_12_scenario_s10_04_on_full_reorder.log
88dcf2598e25a94807b1e1f981218bff  runs/env_layout_12_scenario_s10_04_on_full_reorder.rec
a46a710d3cf5115481c6563179432a7c  runs/env_layout_12_scenario_s10_04_on_single_task.log
88dcf2598e25a94807b1e1f981218bff  runs/env_layout_12_scenario_s10_04_on_single_task.rec
ebea0cee5f87cc13d80e401c0c701817  runs/env_layout_12_scenario_s10_05_off_single_task.log
c0b3c52826984a71c0637d8dfc8eba55  runs/env_layout_12_scenario_s10_05_off_single_task.rec
6f3ad07dc6ce2b3a57737b62f0b5c68d  runs/env_layout_12_scenario_s10_05_on_full_reorder.log
c0b3c52826984a71c0637d8dfc8eba55  runs/env_layout_12_scenario_s10_05_on_full_reorder.rec
9f2cf65204ed963e1fcd030cff3d95a5  runs/env_layout_12_scenario_s10_05_on_single_task.log
c0b3c52826984a71c0637d8dfc8eba55  runs/env_layout_12_scenario_s10_05_on_single_task.rec
ca2af7c25ac931caa1c9bc17819d2dfb  runs/env_layout_12_scenario_s10_06_off_single_task.log
4bdc76ccc6f1ee3244e89c5458b19ffe  runs/env_layout_12_scenario_s10_06_off_single_task.rec
2acb8b5d303077c62210044a57aafd62  runs/env_layout_12_scenario_s10_06_on_full_reorder.log
4bdc76ccc6f1ee3244e89c5458b19ffe  runs/env_layout_12_scenario_s10_06_on_full_reorder.rec
f15ebb8578b481f7365cc78fc819394d  runs/env_layout_12_scenario_s10_06_on_single_task.log
4bdc76ccc6f1ee3244e89c5458b19ffe  runs/env_layout_12_scenario_s10_06_on_single_task.rec
cd1e26dd376f01c48781e6cbeaafc612  runs/env_layout_12_scenario_s10_06_reference_full_reorder.log
a0df65782d76940a31cd5196a86f42f2  runs/env_layout_12_scenario_s10_06_reference_single_task.log
de58991297afb977b519fc4f959126f6  runs/env_layout_12_scenario_s10_07_off_single_task.log
9f6bde960f345934b2423236f91fa158  runs/env_layout_12_scenario_s10_07_off_single_task.rec
b215a8ee1c1ce094e202f4cb3f423756  runs/env_layout_12_scenario_s10_07_on_full_reorder.log
9f6bde960f345934b2423236f91fa158  runs/env_layout_12_scenario_s10_07_on_full_reorder.rec
f58c4f4a9f50a495b5e5081869f4a83c  runs/env_layout_12_scenario_s10_07_on_single_task.log
9f6bde960f345934b2423236f91fa158  runs/env_layout_12_scenario_s10_07_on_single_task.rec
d4a3b4be4561ceb8a8be9873f704c008  runs/env_layout_12_scenario_s10_08_off_single_task.log
33ee73bcf6ffefa2c81b3607397ac879  runs/env_layout_12_scenario_s10_08_off_single_task.rec
eb174a09d163194f0b5718290324d6f3  runs/env_layout_12_scenario_s10_08_on_full_reorder.log
33ee73bcf6ffefa2c81b3607397ac879  runs/env_layout_12_scenario_s10_08_on_full_reorder.rec
b10ca58e31510b196d1ca86344049c6d  runs/env_layout_12_scenario_s10_08_on_single_task.log
33ee73bcf6ffefa2c81b3607397ac879  runs/env_layout_12_scenario_s10_08_on_single_task.rec
218b626cabc466897983913d603bdf18  runs/env_layout_12_scenario_s10_09_off_single_task.log
ebcb27b9f5dbf9cfcfa67e4b25a2ba3a  runs/env_layout_12_scenario_s10_09_off_single_task.rec
16a99356fc133a3b9b7590e898877ee4  runs/env_layout_12_scenario_s10_09_on_full_reorder.log
ebcb27b9f5dbf9cfcfa67e4b25a2ba3a  runs/env_layout_12_scenario_s10_09_on_full_reorder.rec
eaa8e01774b9e925254c2fcbb96027b6  runs/env_layout_12_scenario_s10_09_on_single_task.log
ebcb27b9f5dbf9cfcfa67e4b25a2ba3a  runs/env_layout_12_scenario_s10_09_on_single_task.rec
fd71f715d2ee6331a4024c1c40a192d4  runs/env_layout_12_scenario_s10_10_off_single_task.log
4251537079b3d12ed72aa11e6771f5e0  runs/env_layout_12_scenario_s10_10_off_single_task.rec
2894aa687e2128bdcb3340d9ef53d766  runs/env_layout_12_scenario_s10_10_on_full_reorder.log
4251537079b3d12ed72aa11e6771f5e0  runs/env_layout_12_scenario_s10_10_on_full_reorder.rec
f3299d52a633692e539ad0f0c9310f53  runs/env_layout_12_scenario_s10_10_on_single_task.log
4251537079b3d12ed72aa11e6771f5e0  runs/env_layout_12_scenario_s10_10_on_single_task.rec
d78bb83dee4865e37a0ed6fde6f8a3e2  runs/env_layout_12_scenario_s11_01_off_single_task.log
2b20839311f61f384b627483ddebc626  runs/env_layout_12_scenario_s11_01_off_single_task.rec
51b4ab69237ff81e38bcbb87931365f4  runs/env_layout_12_scenario_s11_01_on_full_reorder.log
2b20839311f61f384b627483ddebc626  runs/env_layout_12_scenario_s11_01_on_full_reorder.rec
9b673e2bf65bd1d41cb1fa7e92215173  runs/env_layout_12_scenario_s11_01_on_single_task.log
2b20839311f61f384b627483ddebc626  runs/env_layout_12_scenario_s11_01_on_single_task.rec
54e265873e49cc50466876788fa419f3  runs/env_layout_12_scenario_s11_02_off_single_task.log
86397e984d81ec47aa978760989c152f  runs/env_layout_12_scenario_s11_02_off_single_task.rec
7e78211cb8ab6073fc34030b32482be7  runs/env_layout_12_scenario_s11_02_on_full_reorder.log
86397e984d81ec47aa978760989c152f  runs/env_layout_12_scenario_s11_02_on_full_reorder.rec
580ae9fd3ae2455d251086223a6c5867  runs/env_layout_12_scenario_s11_02_on_single_task.log
86397e984d81ec47aa978760989c152f  runs/env_layout_12_scenario_s11_02_on_single_task.rec
2a9c8daf7b192827db7d81b335ebd2ea  runs/env_layout_12_scenario_s11_03_off_single_task.log
bd84a77d4d232d4657b782614615bccb  runs/env_layout_12_scenario_s11_03_off_single_task.rec
a2001d12159a70510cdea9ca483d5751  runs/env_layout_12_scenario_s11_03_on_full_reorder.log
bd84a77d4d232d4657b782614615bccb  runs/env_layout_12_scenario_s11_03_on_full_reorder.rec
31d5f0f5e16cdd71e301cf77182aa311  runs/env_layout_12_scenario_s11_03_on_single_task.log
bd84a77d4d232d4657b782614615bccb  runs/env_layout_12_scenario_s11_03_on_single_task.rec
fde498fd3ab38f150e275a71cd9ef5d6  runs/env_layout_13_scenario_s10_11_off_single_task.log
955c7b71a51a1cf3d80a3f8ed51931da  runs/env_layout_13_scenario_s10_11_off_single_task.rec
d0e3bad1b2ef8c48a3885b5db8216317  runs/env_layout_13_scenario_s10_11_on_full_reorder.log
955c7b71a51a1cf3d80a3f8ed51931da  runs/env_layout_13_scenario_s10_11_on_full_reorder.rec
f7f275edfcc056ca12dd9ce67554675b  runs/env_layout_13_scenario_s10_11_on_single_task.log
955c7b71a51a1cf3d80a3f8ed51931da  runs/env_layout_13_scenario_s10_11_on_single_task.rec
f8eb27408542ff7acd555591de45eca5  runs/env_layout_14_scenario_s12_01_off_single_task.log
fc4ef52bbf1c640efa64a535a9385f7f  runs/env_layout_14_scenario_s12_01_off_single_task.rec
f0e681aa7b0376acf2df37ccef57cae9  runs/env_layout_14_scenario_s12_01_on_full_reorder.log
fc4ef52bbf1c640efa64a535a9385f7f  runs/env_layout_14_scenario_s12_01_on_full_reorder.rec
e1e9a758799a488b3bf022fe8c8b92ae  runs/env_layout_14_scenario_s12_01_on_single_task.log
fc4ef52bbf1c640efa64a535a9385f7f  runs/env_layout_14_scenario_s12_01_on_single_task.rec
c77779465dcf2d64c4716973ed58b280  runs/env_layout_14_scenario_s12_02_off_single_task.log
eeff90b54d1ee23e20d5635de4ce1a07  runs/env_layout_14_scenario_s12_02_off_single_task.rec
72b73591793951438b743150f183589f  runs/env_layout_14_scenario_s12_02_on_full_reorder.log
eeff90b54d1ee23e20d5635de4ce1a07  runs/env_layout_14_scenario_s12_02_on_full_reorder.rec
93053e69c0d69ae637fb82b0c9399eb2  runs/env_layout_14_scenario_s12_02_on_single_task.log
eeff90b54d1ee23e20d5635de4ce1a07  runs/env_layout_14_scenario_s12_02_on_single_task.rec
```
