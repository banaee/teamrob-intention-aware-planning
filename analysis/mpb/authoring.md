# The meta-planner test-bed: authoring and its derivations (MPB step 2, part (i))

The artefacts of the meta-planner test-bed (design_decisions.md, "The meta-planner test-bed (MPB)", MPB-2) and the
geometric and timing checks they were authored against, before any MPB run. 29 September 2026.

**Status of every number here: an authoring check.** The distances and ticks below were derived by hand from the layout
and, where stated, by the pre-run checks (the robot alone, the IR test-bed's expansion and oracle on each script). They
show that each scenario can expose its decision. They are previews, not expectations: the expectations are the MPB
oracle's (analysis/mpb/README.md, the derivations of parts 1 to 3), and a preview never becomes an oracle rule.

## The room: env_layout_12

W 1000 × H 1400 cm, centred origin, x ∈ [−500, 500], y ∈ [−700, 700].

The human's side is the 10/11 pattern (env_layout_10 / _11) translated by (0, −200). Every object keeps its relative
arrangement and its distance to the south and east walls, and the room gains 400 cm to the north for the robot. The
recognizer reads distances only, so a TB script run here has the IR test-bed's trajectory, translated. The belief
differs only through the output floor: the setup's inadmissible robot items count among the keys held at the floor.
The pre-run check below found the recognition ticks unchanged.

| id | position | role |
|---|---|---|
| kitting_table_0 | (0, 220) | the human's table |
| shelf_1, shelf_2 | (−420, −220), (420, −220) | the human's shelves |
| coffee_machine_0 | (−170, −600) | the machine |
| corner_SE | (450, −650) | the exit landmark |
| kitting_table_1; shelf_4, shelf_7, shelf_8, shelf_9 | (60, 640); (460, 640), (460, 360), (260, 360), (260, 640) | the robot's NE work area |
| shelf_5, kitting_table_3 | (20, −220), (−440, 220) | the crossing |
| shelf_3, shelf_6; kitting_table_2, kitting_table_4 | (−420, 620), (−420, 690); (−270, 620), (−270, 690) | the occupied target and its alternative |
| door_N, spot_E | (300, 690), (380, 610) | the walker's end and the stand beside the route |

One room serves all eight scenarios. No scenario needs a second layout: every physical fact MPB-2 names is placed in
this room, as follows.

- **The crossing (scenario 2).**
  - The diagonal kitting_table_0 – shelf_1 is 608.3 cm long, with u = (−0.6905, −0.7234), n = (0.7234, −0.6905) and
    midpoint M = (−210, 0).
  - shelf_5 ≈ M + 318·n and kitting_table_3 ≈ M − 318·n, so the robot's carry is the diagonal's perpendicular bisector
    and crosses it at M.
  - The human:
    - its walk passes M after 15.2 steps (between ticks 14 and 15);
    - the walk takes 29 steps and ends 28.3 cm from shelf_1;
    - the carry starts at 32 and reaches M after 13.8 steps (between ticks 44 and 45).
  - The robot starts at p0 = M + 830·n ≈ (390, −573):
    - walk 511.7 cm, 25 steps, ending 11.7 cm short;
    - ack, grasp, ack;
    - carry from 28, reaching M after 16.5 steps.
  - The robot alone (no human, no hold) is 9.7 cm from M at the end of tick 43 and 10.4 cm at the end of tick 44.
  - The two passages coincide, so the admitted delivery conflicts with the robot's task at shift 0 whenever admission
    comes before about tick 44.
  - Clearance of the robot's route from the east diagonal: ≥ 287 cm. From the exit line: ≥ 184 cm, except p0 itself,
    which is 18 cm from it and occupied at t = 0 only.
- **The occupied target (scenario 6).**
  - Robot start (−420, 280).
  - Walk 340 cm to shelf_3 (arrival (−420, 590)); walk 410 cm to shelf_6 on the same bearing (arrival (−420, 660)).
  - Both carries are 153 cm.
  - So the plain-cost difference is ΔC = 70/20 = 3.5 ticks at every point of the walk north: the stationary
    structures are equal.
  - The alternative's carry passes no closer than 70.5 cm to kitting_table_2's centre, where the human stands, so its
    hold is 0.
- **Clear routes (scenario 8, the control).** Measured on the reference run's executed robot path, the minimum
  distance is 287.5 cm to each of:
  - every human position of the script;
  - every fallback segment a decision at any tick could rest on (the observed persistence, cut at the walls and at the
    first arrival-radius disc; a disc containing the start skipped), including the arrival-tick ray below;
  - every admitted plan's path (to shelf_2 and back, and to the machine from anywhere on the human's path).
- **The arrival-tick ray (objection 1 of the plan; Hadi's point 5).**
  - On the tick a walk ends inside its target's arrival radius, the skip rule lets the fallback continue through the
    target, for up to the whole run length.
  - The control's clearance includes those rays.
  - In the other scenarios, if such a ray is what a decision rests on, the run records it with its ticks. It is
    classified 3 under MPB-4 and returns to Hadi. It is not assumed harmless.
- **The walker and the stand (scenario 7).**
  - The walk (300, 260) → door_N crosses the robot's route (y = 640, shelf_4 → kitting_table_1) at x = 300 at tick 18.
  - The ray north from x = 300 passes shelf_9 at 40 cm (outside its 30 cm radius) and is cut first at door_N's radius
    (y = 660).
  - spot_E is 30 cm below the route.
  - The robot alone passes x = 300 at tick 19 (y = 628.5), when the walker is at (300, 660), 31.5 cm away.

## Setups

One robot item per shelf; no setup at HEAD puts two items on one shelf.

- **env_setup_10:**
  - item_1 (shelf_1) and item_2 (shelf_2) → kitting_table_0 (the human's);
  - item_3, item_4, item_5, item_6 (shelf_4, shelf_7, shelf_8, shelf_9) → kitting_table_1;
  - item_7 (shelf_5) → kitting_table_3.
- **env_setup_11:**
  - item_8 (shelf_3) → kitting_table_2;
  - item_9 (shelf_6) → kitting_table_4;
  - item_10 (shelf_4) and item_11 (shelf_7) → kitting_table_1.

## Scenarios

The robot's NE pool is item_3 to item_6 (env_setup_10). Disjointness (MPB-3), checked per scenario (the pools, the
assigned tasks, the script's items and the setup's item placement):

| id | MPB scenario | human's items (shelves) | robot's items (shelves) | disjoint |
|---|---|---|---|---|
| scenario_s10_01 | 1, admission after θ | item_1, item_2 (shelf_1, shelf_2) | item_3–6 (shelf_4, 7, 8, 9) | yes |
| scenario_s10_02 | 2, the hold | item_1, item_2 (shelf_1, shelf_2) | item_7 (shelf_5) | yes |
| scenario_s10_03 | 3, the mid-action change | item_1, item_2 (shelf_1, shelf_2) | item_3–6 | yes |
| scenario_s10_04 | 4, boundary re-admission | item_1, item_2 (shelf_1, shelf_2) | item_3–6 | yes |
| scenario_s10_05 | 5, the lone foreseeable | item_1, item_2 (shelf_1, shelf_2) | item_3–6 | yes |
| scenario_s10_06 | 8, the control | item_2 (shelf_2) | item_3–6 | yes |
| scenario_s11_01 | 6, the occupied target | none | item_8, item_9 (shelf_3, shelf_6) | yes |
| scenario_s11_02 | 7, walker and stander | none | item_10, item_11 (shelf_4, shelf_7) | yes |

SUPERSEDED IN PART (29 September 2026): the two env_setup_11 rows are part (i)'s first authoring. Since part (iv) the
human of scenario_s11_01 and scenario_s11_02 is assigned `deliver_item(item_12)` (shelf_1), never performed; the check
against the robot's items 8 to 11 (shelves 3, 6, 4, 7) is in part (iv), below. The three scenarios added in part (iv)
(scenario_s10_07 to _09) keep the rows above for env_setup_10: the human's item_1 and item_2 (shelf_1, shelf_2) against
the robot's NE pool, item_3 to item_6 (shelf_4, 7, 8, 9); scenario_s10_09's wrong table, kitting_table_2, is used by no
robot task in it (checked on the committed literals, 29 September 2026).

Scenarios 6 and 7 give the human no assigned tasks: an accepted authoring choice (Hadi, point 3). With the prior on,
coffee_break is the lone live hypothesis and is refused throughout, so every decision rests on the fallback. Scenario
5's ten-tick stand is the other accepted choice: it puts a decision on standing. Each scenario's description states
what it is authored to expose.

### Previews per scenario

Recognition ticks come from the IR test-bed's expansion and oracle on each script (θ = 0.75, α = 0.05), before any MPB
run. They are identical to the IR test-bed's committed gate tables for the same scripts (scenario_s09_01, _02, _13).
No robot decision is assumed in them. The expiry ticks are hand-derived from P4's persistence rule.

- **scenario_s10_01.**
  - The chain: entered 25 (deliver_item(item_1)), replaced 61, entered 76 (deliver_item(item_2)), replaced 124, entered
    126 (coffee_break on the exit walk, the half-plane consequence), retraction 157.
  - Before 25: fallback expiries at 2, 6 and 14.
  - Exposed: entered at 25 and at 76.
- **scenario_s10_02.**
  - The chain: the same human side.
  - Exposed: the decision at 25 (entered).
  - Declared property: its hold is positive, and there is no F1 robot violation within its assessed window.
- **scenario_s10_03.**
  - The chain: entered 25, retraction 55 (deliver_item(item_1)'s carry inadequate) with a fallback moving along the
    cut walk (run 10 at 55, expiry about 66), entered 74 (coffee_break at its advance to wait_at), replaced 105,
    entered 121, replaced 149, entered 164.
  - Exposed: 55, 66 and 74.
- **scenario_s10_04.**
  - The chain: entered 25, replaced 61, entered 75 (coffee_break), **replaced 133** (the recorded coffee_break pinned,
    most_likely changes; admission refuses, no observation on the boundary tick), **entered 134** (deliver_item(item_2),
    the single live hypothesis, commitment warrant), replaced 135, entered 140, replaced 201, entered 203, retraction 234.
  - Exposed: 133 and 134.
  - Boundary stays a possible cause only where the recorded hypothesis remains the leader.
- **scenario_s10_05.**
  - The chain: as scenario_s10_01 to **replaced 124** (the recorded deliver_item(item_2) pinned; boundary is possible
    only where the recorded hypothesis remains the leader).
  - Its fallback, a stand with count 2, expires at 127, within the stand (126 to 130): a decision refused
    `none(leader_unwarranted)`.
  - Then **entered 132**, on the first step toward the machine.
  - Exposed: 124, 127 and 132.
- **scenario_s10_06.** The chain: entered 14, replaced 61, entered 63 (coffee_break on the exit walk), retraction 94.
  Exposed: every decision (no hold).
- **scenario_s11_01.**
  - No recognition_changed, only no_current_task and projection_expired.
  - The stand is observed from tick 0 (count t + 1), so the expiries fall at 0, 2, 6, 14 and 30.
  - The fallback stand ends at 1 + k ticks from the decision (the projected fallback duration), so item_8's hold is at
    most k + 1.
  - Hand-derived: at 14 the robot is at (−420, 560). item_8's first violating moment is 1.5 + 3 + 5.15 = 9.65 ticks
    ahead, and the projection ends at 16, so the hold is ⌈16 − 9.65⌉ = 7 > ΔC = 3.5. The switch to item_9 is expected at
    the expiry of tick 14, before the grasp.
  - At 6 the first violating moment (17.65) lies past the projection's end (8): hold 0.
- **scenario_s11_02.**
  - Expiries of the walk: 2, 6, 14 (run 15, cut at door_N's radius), 20, 22, 25.
  - Expiries of the stand: 27, 31, 39, 55, 87 (counts 1, 3, 7, 15, 31).
  - The stand ends at 55 and its last projection runs to 87: evidence for TODO-132 (a).

## The pre-run timing check, and the robot starts it moved

The robot's plain timeline is taken from the robot alone: the reference construction, the human removed, so no hold.
A start is moved when one of the robot's `no_current_task` decisions falls within 3 ticks of a decision the scenario
exposes. The terminal decision is no masking: nothing is decided after it.

| scenario | robot start | robot alone: [meta] decisions | exposed | result |
|---|---|---|---|---|
| scenario_s10_01 | (460, 480) | 0, 29, 67, 110, 163 | 25, 76 | kept |
| scenario_s10_02 | (390, −573) | 0, 63 | 25 | kept |
| scenario_s10_03 | **(−250, 560)**, moved from the nominal (460, 480) | 0, 40, 79, 123, 174 | 55, 66, 74 | moved: at (460, 480) the robot completes a task at 67, within 3 of the expiry at 66; (−250, 560) is the first start of the search with no completion within 3 of 25, 55, 66 or 74 |
| scenario_s10_04 | (460, 480) | 0, 29, 67, 110, 163 | 133, 134 | kept |
| scenario_s10_05 | (460, 480) | 0, 29, 67, 110, 163 | 124, 127, 132 | kept |
| scenario_s10_06 | (460, 480) | 0, 29, 67, 110, 163 | every decision | kept |
| scenario_s11_01 | (−420, 280) | 0, 30, 50 | 2, 6, 14 | kept |
| scenario_s11_02 | (−100, 600) | 0, 52, 105 | the cadence | kept; the robot alone completes at 52, 3 ticks before the expiry at 55, but this scenario is authored for holds, which move the robot's timeline, so the check cannot predict it; a masking changes the cadence, which the chain assembly reads from the run |

Scenarios 2, 6 and 7 are authored for holds, so their runs will depart from the robot-alone timeline.

## The run files and their safety cap

`configs/mpb/scenario_sNN_MM.yaml`: prior on, single_task, gate none, cost realized, separation stop off, α = 0.05.
Their steps are MPB-5's safety cap (`analysis/mpb/horizon.py`): the robot's pool chained along its authored order from
its start on plain cost (path lengths and the body's step rule), plus the human's replay length, plus 30.

| run file | cap |
|---|---|
| scenario_s10_01 | 348 |
| scenario_s10_02 | 268 |
| scenario_s10_03 | 463 |
| scenario_s10_04 | 425 |
| scenario_s10_05 | 409 |
| scenario_s10_06 | 285 |
| scenario_s11_01 | 212 |
| scenario_s11_02 | 254 |

## The control's fact, confirmed by running it

`analysis/mpb/reference.py configs/mpb/scenario_s10_06.yaml 285 ...` runs scenario_s10_06's robot alone, in-process,
through the same SimModel. The human agent is removed and the robot's `observes` emptied. The ScenarioConfig is built
by the instrument and not registered: a reference run, not a scenario.

It loads and runs with no code change. Every decision refuses `none(below_theta)` and builds no fallback: the dummy
belief is below θ, and there is no human_agent_id. Every decision is `selection=no_projection`, hold 0.

| strategy | terminal decision | completion (world tick) | decisions |
|---|---|---|---|
| single_task | 163 | 161 | 0, 29, 67, 110, 163 |
| full_reorder | 139 | 137 | 0, 35, 72, 116, 139 |

Logs: `analysis/mpb/runs/` (git-ignored).

# Part (iv): scenarios 6 and 7 re-authored, three scenarios added (29 September 2026)

Hadi's rulings of 29 September 2026 on part (iii): scenarios 6 and 7 re-authored (class 4, not parked); three scenarios
added for coverage. As above, every number here is an authoring check made before any MPB run. Most come from the MPB
oracle's own per-tick table chained with the robot-alone decisions (`reference.py`); the oracle's values in the runs are
the expectations.

**Provenance.** The three scenarios were added for a coverage gap found in review, not because a run failed.

**The coverage principle** (recorded in the MPB entry). Each materially distinct mapping from a deviation kind to a
decision chain that the MPB claims to verify has one authored instance; a different location of the same chain is
covered by type.

## Scenarios 6 and 7 re-authored: an assigned delivery the human does not execute

**The first authoring and its case.** The first authoring gave the human no assigned tasks. An empty assignment
switches the support restriction off (`shared/io_contracts.md` §2.1), which made the robot's items live hypotheses of the
human and broke MPB-3's precondition (part (iii), class 4).

**The re-authoring.**
- `env_setup_11` gains `item_12`, designated to kitting_table_0. The human is assigned `deliver_item(item_12)` and never
  performs it.
- This is a different in-scope case: an assigned task the human does not execute, which carries commitment warrant.
- It is not the original "no assigned work". The framework has no representation of an observed human with no work
  under the prior on, since an empty list is the diagnostic mode (TODO-143, recorded only).
- Disjointness: the human's item_12 (shelf_1) against the robot's items 8 to 11 (shelves 3, 6, 4, 7).

### The derivation from the records

- **The live set.** With the restriction on, the live set is deliver_item(item_12) and coffee_break. The robot's items
  are outside the support.
- **The stand (scenario_s11_01, ticks 0 to 59).**
  - Both hypotheses are in their initial walk phases (origin at the start, s_exp = 0). With nothing walked, e = 0, so
    both have D = s and the same L(v·s) every tick: the prior's 1/2 each.
  - With 4 keys held at the output floor, the confidence is 0.5 × 0.996 = 0.498 < θ.
  - Both turn inadequate at s = 17, tick 16: S(340) = 0.047 < α.
  - On the exit walk D ≥ s; D cannot fall within a phase, and the human reaches neither target.
- **The walk north (scenario_s11_02)**, with item_12 on shelf_1:
  - the delivery leads the coffee break, at a highest share while adequate of 0.627 at tick 9 (below θ);
  - coffee_break is inadequate from 8 and the delivery from 10;
  - no phase changes afterwards.
- **Every decision rests on the fallback.** Checked on the oracle's table over the whole run: the gate clears on no tick
  of either scenario. The pre-run chains, per strategy, contain `no_current_task` and `projection_expired` decisions
  only, all refused.

### The shelf_2 case: a class-4 authoring artefact

`item_12` was first placed on shelf_2. The oracle's table, before any run, showed an admission:
- scenario_s11_02's exit walk (spot_E → corner_SE) passes within 2.3 cm of shelf_2 (19.3 cm at 97, 2.3 at 98);
- at 97, deliver_item(item_12)'s `move_to` completes and it advances to `pick_up` (a member at S = 1, warranted by
  entry and by commitment), leading at 0.886, so the gate clears and it is entered;
- after the regress at 100, the fresh walk phase clears again at 101 (0.905).

The hand derivation had checked only scenario 6's exit walk (214 cm from shelf_2). Stopped and reported; Hadi ruled
option (a), shelf_1, which neither script approaches.

## scenario_s10_07, the sudden stand mid-carry

- **The authoring.** A stand of 60 ticks (`stand("PT120S")`) cut into the carry of item_1 at PT28S (14 of its 28
  steps), as scenario_s09_13 cuts it. The carry's phase is a walk, s_exp = 0.
- **The stand's length** was derived before the check, with no robot decision assumed:
  - the retraction falls 17 standing ticks into the stand (v·17 = 340 > 334 cm): 46 + 16 = 62;
  - the standing fallback k = 17 ends at 80 (inside the stand), k = 35 ends at 116;
  - a stand ending between 102 and 115 puts that expiry in the resumed walk: 60 ticks, ending at 106.
- **The chain as derived** (the oracle's table, the robot-alone decisions):
  - single_task (decisions 0, 29, 67, 110, 163):
    - 25 entered (deliver_item(item_1));
    - **62 retraction** (standing fallback, k = 17);
    - 67 `no_current_task` (standing, k = 22);
    - **90 expiry** (standing, k = 45: the doubling);
    - 110 `no_current_task` and **115 expiry** (the resumed walk: moving, k = 4 and 9);
    - **120 entered** (the delivery again, only at its carry's advance to `place`, L2 (iii));
    - **123 replaced** (the boundary at the place);
    - 127 and 131 expiries;
    - **138 entered** (item_2).
  - full_reorder (decisions 0, 35, 72, 116, 139): 62 retraction; 72 `no_current_task` (standing, k = 27); **100 expiry**
    (k = 55); 116 `no_current_task` (moving, k = 10); 120 entered; 123 replaced; 138 entered.
- **item_2 is admitted at b + 15 (138), not at b + 1.** coffee_break is live after the boundary (it was never taken),
  so the prior gives each 1/2 and θ is not cleared: MPB-2's note on scenarios 4 and 5 applies. This is the oracle's
  value, and it stands over the ruling's text.

## scenario_s10_08, the change of mind between assigned tasks

scenario_s09_07's script:
- 25 entered (item_1);
- **33 replaced**: the return of item_1 to shelf_1 is a terminal place, a boundary (L1, consequence D). All three
  hypotheses fall back to the prior, and coffee_break leads on its tie order. So the human's change from delivery 1 to
  delivery 2 passes through the coffee hypothesis in the recognizer's chain;
- expiries;
- **47 entered** (item_2, commitment and observation);
- 108 replaced;
- 135 entered (item_1 again);
- then the exit.

The IR test-bed's 46 was on env_layout_11. Here env_setup_10's five inadmissible robot items at the output floor lower
the confidence enough to move the crossing to 47: the oracle's value, and it stands. No retraction. AD3 has no
property here: it is not exercisable in the MPB set (design_decisions.md, "T-D G", AD3).

## scenario_s10_09, the misdelivery

- **The script.** scenario_s09_08's, with this room's wrong table: `kitting_table_2`, which the robot does not use in
  this scenario.
- **The geometry.** From the grasp at (−400.4, −199.5), the carry to kitting_table_2 (829.8 cm, arriving at 71) makes
  item_1's hypothesis (target kitting_table_0) accumulate excess: e(560) = 319.9, e(580) = 345.3. So it is inadequate at
  w ≈ 570, tick 60.
- **The unexplained interval.** From 60 to the place at about 73, with every member inadequate. It is chosen for its
  length: it exposes X5's ground (1), measured.
- **The chain:**
  - 25 entered;
  - **60 retraction** (moving fallback, k = 29, cut at kitting_table_2's radius, end 71.99);
  - the robot's `no_current_task` at 67 (single_task) or 72 (full_reorder), refused inside the interval;
  - 72 to 93 expiries;
  - no re-admission of item_1, whose terminal fact never holds;
  - **102 entered** (item_2).

## The pre-run timing check, per strategy

A start moves when a robot `no_current_task` decision falls within 3 ticks of a decision the scenario exposes; the
terminal decision masks nothing. The robot alone, no hold:

| scenario | start | single_task | full_reorder | exposed | result |
|---|---|---|---|---|---|
| scenario_s10_07 | (460, 480) | 0, 29, 67, 110, 163 | 0, 35, 72, 116, 139 | 25, 62, 120, 123, 138 | kept (139 is full_reorder's terminal) |
| scenario_s10_08 | **(−165, 490)**, moved from (460, 480) | 0, 37, 74, 118, 169 | 0, 43, 94, 137, 160 | 25, 33, 47 | moved: at (460, 480) full_reorder's first completion is at 35, 2 ticks after 33; (−165, 490) is the first start of the search clear under both strategies |
| scenario_s10_09 | (460, 480) | 0, 29, 67, 110, 163 | 0, 35, 72, 116, 139 | 25, 60, 102 | kept |
| scenario_s11_01 | (−420, 280) | 0, 30, 50 | 0, 30, 50 | 2, 6, 14 | kept |
| scenario_s11_02 | (−100, 600) | 0, 52, 105 | 0, 58, 101 | the cadence | kept, as in part (i) (authored for holds) |

Caps (MPB-5): scenario_s10_07 410, scenario_s10_08 419, scenario_s10_09 383; scenario_s11_01 212 and scenario_s11_02 254
are unchanged.
