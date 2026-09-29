# The meta-planner test-bed: report (MPB step 2, 29 September 2026)

The recognition-to-planning chain with a working robot, one authored scenario per decision, against an oracle that
states the expected decision before the run. The instrument, its rules and their sources are in `README.md`; the
artefacts and their derivations are in `authoring.md`. Prior on is the primary set; α = 0.05, θ = 0.75, gate none,
cost realized, separation stop off.

**Result.**
- **Six of the eight scenarios are verified** (MPB-1 to MPB-3, scenarios 1 to 5 and the control, 8): zero
  disagreements on parts 1 to 3 at exact equality on every tick and every decision, prior on, against the in-process
  run and against the log, under both strategies; every declared part-4 property holds under single_task.
- **Scenarios 6 and 7 (scenario_s11_01, _02) are not verified.** Their disagreements are class 1 and class 4 (below):
  as authored, the human has no assigned tasks, and an empty assignment switches the support restriction off. MPB-3's
  pre-run independence then does not hold. Their remedy (re-author or park) is Hadi's.
- **No class-2 finding.**

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
| scenario_s11_01 | on, single_task | 164 | 5 / 5 | 410 | 8 | 8 | 74 | (33, 23) | 0/0/0 | 66.15 (56) |
| scenario_s11_02 | on, single_task | 164 | 14 / 14 | 458 | 20 | 7 | 132 | (14, 2), (20, 2), (41, 14) | 0/0/0 | 53.42 (19) |

Notes on the table:
- **The per-tick columns:** the leader, the boundary, the gate, every live hypothesis's hypothesis adequacy and
  observation warrant, and the perception facts.
- **The decision columns:** part 1 as a set, parts 2 and 3 at every decision.
- **The horizon:** the first observed completion point + 30, capped at the steps (MPB-5).
- **In every run:**
  - the trajectory equals the run's human lines on every tick;
  - the in-process model lines are identical to the logged run's (the recorders changed nothing);
  - the oracle's process loaded none of the forbidden modules.
- **The scenario_s11 full_reorder runs** have no table: the oracle's rule M0 (below) refuses them.

**The invariant across strategies (MPB-6).** For each of the six comparable scenarios:
- `expected_ticks.json` is byte-identical between single_task and full_reorder;
- the in-process per-tick human-side columns are identical over the common horizon;
- the chains differ only through the run's `no_current_task` ticks, which differ by strategy;
- `trajectory.json` is byte-identical across all three variants of every scenario.

## Per scenario: the decision it exposes, expected and actual

Ticks are the oracle's, and every one equals the run's (single_task, prior on). The authoring previews
(`authoring.md`) agreed with every one.

- **scenario_s10_01, admission after θ.**
  - (25, recognition_changed, entered | clears, deliver_item(item_1), commitment and observation | admitted).
  - (76, entered | clears, deliver_item(item_2) | admitted).
  - Before 25: fallback expiries at 2, 6 and 14 (moving, k = 1, 3, 7, 15; the last cut at shelf_1's radius, end 28.91).
  - After: 61 replaced, 64 and 73 expired, 124 replaced (`none(leader_no_observation)`), 126 entered (coffee_break on
    the exit walk, the half-plane consequence), 157 retraction.
  - The robot's `no_current_task`: 0, 29, 67, 110, 163.
- **scenario_s10_02, the hold.**
  - (25, entered | clears, deliver_item(item_1) | admitted): winner deliver_item(item_7), **hold 5**.
  - **P2a holds.**
  - **P2b holds:** no F1 violation in the assessed window, ticks 26 to 63 (T_h 37.33). The robot crosses the diagonal
    after the human, at 52.20 cm, tick 47.
- **scenario_s10_03, the mid-action change.**
  - (25, entered, deliver_item(item_1)).
  - **(55, retraction | none(leader_inadequate) | fallback, moving, k = 10, end 66)**.
  - **(66, projection_expired | none(below_theta), coffee_break | fallback, moving, k = 21, cut at the machine's radius,
    end 74.71)**.
  - **(74, entered | clears, coffee_break | admitted)**: re-admission at the next fitting phase.
  - Then 105 replaced (stand, k = 31), 121 entered, 149 replaced, 153 and 157 expired, 164 entered.
  - P3a, P3b and P3c hold (single_task): no decision from 46 to 54; the record is deliver_item(item_1) throughout; the
    leader is the assigned delivery.
  - The delivery's observation warrant from 46 to 54, measured: `observation` on every tick (AD3, below).
- **scenario_s10_04, boundary re-admission on commitment.**
  - (75, entered, coffee_break).
  - **(133, recognition_changed, replaced | none(leader_no_observation), deliver_item(item_2) | fallback, standing,
    k = 31)** = b refused.
  - **(134, entered | clears, deliver_item(item_2), commitment | admitted)** = b + 1.
  - Then (135, replaced): coffee_break re-enters as `waited` clears, and the leader moves to it at 1/2.
  - Then (140, entered, deliver_item(item_2)).
- **scenario_s10_05, the lone foreseeable hypothesis.**
  - **(124, replaced | none(leader_no_observation), coffee_break | fallback, standing, k = 2, end 127)**.
  - **(127, projection_expired | none(leader_unwarranted) | fallback, standing, k = 5)**: the refusal on standing, at a
    decision.
  - **(132, entered | clears, coffee_break, observation)**: on the first step toward the machine.
- **scenario_s10_06, the control.**
  - Entered 14 (deliver_item(item_2)), replaced 61, entered 63 (coffee_break on the exit walk), retraction 94.
  - Expiries of the idle stand at corner_SE: 112, 116, 124, 140 (k = 3, 7, 15, 31).
  - **P8a** (no hold at any decision, every candidate's delta 0), **P8b** (completion 161 = the reference's 161;
    full_reorder 137 = 137) and **P8c** (the robot's positions identical on every tick) hold, under both strategies.

## Disagreements, classified

- **scenario_s11_01 and scenario_s11_02, prior on, single_task.** All 426 and 485 disagreements have one cause.
  - The human has no assigned tasks. With the prior on, the robot is given the empty list, and `shared/io_contracts.md`
    §2.1 (the recognizer's constructor: "None or [] switches the restriction off") and the recognizer's docstring
    switch the support restriction off. The logs show it: `[IR-prior] switch=on known=[]`.
  - So every hypothesis is live, the robot's own items' deliveries included. In scenario_s11_02 the robot's own
    deliver_item(item_10) became the human's leader and was admitted at 22.
  - **Class 1:** the MPB oracle took the IR test-bed's support rule (its rule 1), which never met an empty assignment
    and omits the empty-list clause. Corrected by derivation: rule M0 refuses a scenario with the restriction off, since
    its table is then not derivable before the run.
  - **Class 4:** the scenarios as authored break MPB-3's precondition. The plan's premise ("with the prior on,
    coffee_break is the lone live hypothesis") was mine, and the records contradict it. Hadi accepted the authoring
    choice on that premise. Re-author or park: Hadi's call (the proposal below).
  - The framework agrees with the records, so no class 2.
  - Recorded as observations only, from runs outside the verified domain:
    - scenario_s11_01's X1 switch happens as the authoring check derived: at the expiry of 14, item_8's hold 7 >
      ΔC 3.5, before the grasp; P6.1 and P6.2 hold as booleans.
    - After it, at 33, item_8 has no alternative and a hold of 23.
- **scenario_s10_03, full_reorder: P3a does not hold.** The robot's own `no_current_task` falls at 48, inside 46 to 54.
  The pre-run timing check was made on single_task's timeline, and full_reorder's differs. Parts 1 to 3 agree exactly,
  and this is not a disagreement of them. P3 is declared for single_task only: MPB-6, "part-4 properties where defined".
- **Prior off (appendix, no ruling).** scenario_s10_02 prior off: P2b does not hold (3 F1 violations; the admission
  moves to 26, hold 4). The robot's own item is admissible there. It is recorded, not examined (`docs/assumptions.md`
  1.4).

## AD3 (Hadi's addition): not exercised by the test set

The addition's premise ("its observation warrant lost from the cut") does not hold by the records.
- The carry phase `move_to(kitting_table_0)` is entered by the grasp's completion, and AD1's entry source warrants a
  phase so entered for the whole phase.
- It resets only with the origins, at a boundary or a phase change, and the cut is neither.
- Measured on every run of the set (in-process): no recorded hypothesis loses its observation warrant on any tick.
- P3a to P3c therefore evidence D2's retention by identity through a deviation until its retraction (L2 (ii)), not
  AD3.
- Evidence for AD3 needs a recorded hypothesis warranted by movement only (its phase entered at a boundary or a first
  observation, not by a completion) that turns so its gain falls to 0 or below while still adequate: a turn early in
  such a walk, since inadequacy comes first otherwise. A question to Hadi.

## The alteration test (MPB-4)

One rule altered at a time, in a scratch copy; disagreements against the unchanged actual files (prior on,
single_task).

| alteration | s10_01 | s10_02 | s10_03 | s10_04 | s10_05 | s10_06 |
|---|---|---|---|---|---|---|
| A1: the fallback's end without the observation offset | 18 | 13 | 18 | 20 | 19 | 20 |
| A2: the run length by exact direction equality (no 1e-9) | 170 | 74 | 155 | 143 | 157 | 114 |
| A3: a turn resets the run length to 0 | 167 | 73 | 151 | 143 | 159 | 111 |
| A4: landmarks not counted as fixed objects for the ray | 2 | 0 | 0 | 0 | 0 | 1 |
| A5: projection_expired before recognition_changed on a shared tick | 0 | 0 | 0 | 0 | 0 | 2 |
| B1: the admitted plan decomposed without the method guards | 1 | 0 | 2 | 0 | 1 | 0 |
| B2: the ray does not skip an object whose radius contains its start | 0 | 0 | 0 | 0 | 0 | 0 |
| B3: the moving fallback not cut at the wall or the first object | 3 | 1 | 2 | 1 | 1 | 1 |
| C1: commitment warrant ignored | 0 | 0 | 0 | 4 | 0 | 0 |
| C2: the movement source loosened to any walked path | 58 | 58 | 141 | 158 | 126 | 0 |
| C3: warrant asked before the leader's adequacy | 3 | 1 | 1 | 1 | 56 | 3 |
| D1: no retraction | 1 | 0 | 3 | 0 | 0 | 1 |
| D2: boundary asked before replaced | 4 | 2 | 4 | 4 | 4 | 2 |

Every alteration is detected by at least one scenario except **B2**. That is a property of the test set, and it
strengthens the plan's objection 1:
- A ray that starts inside an object's radius while the human moves away from it is already excluded, because the
  object lies behind the ray (the direction test).
- So the skip rule changes the fallback only when the human moves toward the object while inside its radius, that is,
  on an arrival or a pass through.
- That is exactly the case its stated reason ("the human is leaving it") does not describe.
- No decision fell on such a tick; the arrival-tick detector found none in any run.

C1 is detected only by scenario_s10_04 (b + 1 on commitment), and A5 only by the control. Those scenarios are where
those rules decide.

## The reference run (the control)

scenario_s10_06's robot alone was built in-process and not registered.
- It loads and runs with no code change: part (i)'s fact.
- Completion: 161 (single_task, terminal 163) and 137 (full_reorder, terminal 139).
- Every decision `none(below_theta)`, no fallback, hold 0.
- The control equals it on completion and on every tick's position.

## The prior-off appendix (MPB-6; no oracle comparison, no ruling)

| scenario | completion | holds (tick, ticks) | near-encounters (ticks < 50 cm) | F1 viol/stand/recede | [sep] min, continuous (tick) |
|---|---|---|---|---|---|
| scenario_s10_01 | 161 | none | 0 | 0/0/0 | 383.99 (59) |
| scenario_s10_02 | 65 | (26, 4) | 4 | 3/0/1 | 38.05 (47) |
| scenario_s10_03 | 172 | none | 0 | 0/0/0 | 408.88 (155) |
| scenario_s10_04 | 161 | none | 0 | 0/0/0 | 383.99 (59) |
| scenario_s10_05 | 161 | none | 0 | 0/0/0 | 383.99 (59) |
| scenario_s10_06 | 161 | none | 0 | 0/0/0 | 349.00 (47) |
| scenario_s11_01 | 74 | (33, 23) | 0 | 0/0/0 | 66.15 (56) |
| scenario_s11_02 | 132 | (14, 2), (20, 2), (41, 14) | 0 | 0/0/0 | 53.42 (19) |

The scenario_s11 prior-off runs equal their prior-on runs: an empty assignment switches the restriction off either way.

## The detectors and the parked items

- **TODO-134** (a decision on a fallback stand whose first robot tick violates): no instance in any run.
- **The arrival-tick ray** (Hadi's point 5): no decision rested on one in any run.
- **TODO-132 (a)**, recorded as evidence from scenario_s11_02, a class-4 run outside the verified domain:
  - The stand at spot_E begins at 26 and its persistence breaks at 57 (the first step).
  - The decisions on it: 32 (a retraction of the robot's own item_10, fallback stand k = 8, end 41) and 41 (expiry,
    k = 17, end 59, hold 14).
  - No hold ran past the break.
  - scenario_s11_01 after the switch: at 33 the occupied table's task alone holds 23 against a stand projected to 68;
    the human stood until 59.
  - Nothing is concluded; the question returns to the design chat.

## The independence boundary, demonstrated

- The oracle's process imports `shared.types`, `shared.knowledge`, `shared.planner`, `domains.kitting.registry` and
  the IR test-bed's `oracle.py`.
- In every run (24 invocations) it asserted at exit that none of these was loaded: `shared.meta_planner`,
  `shared.realization`, `shared.projection`, `shared.recognizer`, `shared.likelihood_functions`,
  `world.human_executor`, `mesa_sim.*`. The test `test_the_oracle_loads_nothing_...` checks the same in a clean
  interpreter.
- Its perception facts, ray and fallback are its own (M3 to M6, from P4's text).
- The chain assembly imports the standard library and `mpblib` only.
- The robot enters at the compare step alone, through the observed `no_current_task` and terminal ticks.

## Regression audit

- The suite: 210 passed.
- The four maintained sweeps rerun (48 logs): every log and every `.rec` stream is byte-identical to the G-build
  sections' md5s (96 of 96).
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
b75bb9a750a35e3dc08d619f236cfd8a  runs/env_layout_12_scenario_s11_01_off_single_task.log
86a804715fdf107f307ba2ac7483cc0b  runs/env_layout_12_scenario_s11_01_on_full_reorder.log
c0c70144a7ea3fcf6ef676105704e217  runs/env_layout_12_scenario_s11_01_on_single_task.log
0f272842e3247d2ec183793e4aa9bf51  runs/env_layout_12_scenario_s11_02_off_single_task.log
4337ea6eb3d874dcf7978a64d0b2a773  runs/env_layout_12_scenario_s11_02_on_full_reorder.log
dc9e0f9379294146d63af762397b811f  runs/env_layout_12_scenario_s11_02_on_single_task.log
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
2b20839311f61f384b627483ddebc626  runs/env_layout_12_scenario_s11_01_off_single_task.rec
2b20839311f61f384b627483ddebc626  runs/env_layout_12_scenario_s11_01_on_full_reorder.rec
2b20839311f61f384b627483ddebc626  runs/env_layout_12_scenario_s11_01_on_single_task.rec
86397e984d81ec47aa978760989c152f  runs/env_layout_12_scenario_s11_02_off_single_task.rec
86397e984d81ec47aa978760989c152f  runs/env_layout_12_scenario_s11_02_on_full_reorder.rec
86397e984d81ec47aa978760989c152f  runs/env_layout_12_scenario_s11_02_on_single_task.rec
```
