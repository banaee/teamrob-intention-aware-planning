# Record of planning and building: T-G, the second domain: stage 1 (plan, build, test-beds, close)

Moved verbatim from `docs/design_decisions.md` on 2 October 2026 (Hadi's ruling of that day: one record file per task;
the conceptual design stays in design_decisions.md). Each block is headed by the title of the entry it comes from
and its id; in design_decisions.md an index line with the same id stands where the block was.

**T-G: the second domain's rulings (ruled by Hadi, 30 September and 1 October 2026)** — RECORD [T-G_stage1/1], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
STAGE 1 PLAN APPROVED (Hadi, 1 October 2026; recorded in T-G records 7). The approved plan, with the answers merged in,
is `docs/handoffs/plan_T-G_stage1.md`; every build session of stage 1 reads it. The answers to the plan's nine questions:
1. `deliver_pallet` has no condition on the pallet being full. Reason: the designation and the load check (an assigned
   task's determined parameter, resolved from the station, must have its declared type) exclude an empty pallet, and the
   planner needs no negated condition. It answers B4 for `deliver_pallet`; `load_return`'s methods read `is_empty`.
2. A fixed object's area is derived from its position; the declared per-object field is dropped (A9 AMENDED).
3. dock_loading's area ids are `area_hall`, `area_office`, `area_truck_side`; kitting's ids stay.
4. The carriers of the area that nothing reads are removed (`AgentState`'s area, the observation's area,
   `SimObject`'s area and its query); the `in_area` fact stays.
5. The load-time replay ends a walk where the body stops. Reason: the replay and the run must select the same method at
   the gate and at the office door.
6. Not as recommended: a task has a method for every area the agent can be in, not for every area (B11 AMENDED).
7. The task model names `dock_gate`, `office_door` and the area ids, as this domain's convention.
8. The milestone scenarios as proposed, one per room (scenario_s03_02, s05_02, s07_02).
9. The build may edit `shared/io_contracts.md`, `README.md`, `domains/README.md` and the note in `docs/rename_table.md`;
   the glossary and this file stay with records steps.
Also approved: the names in the plan's section 6 as proposed; the build order, steps 0 to 8, with their acceptance and
stop conditions.
Notes (not rulings):
- A pallet's origin is the setup's initial container in stage 1; stage 2 needs it recorded at the pick-up (C4).
- The rename leaves `ros_sim/` passing the old field names (`current_zone`, `object_zones`); `ros_sim/` is not touched
  (TODO-111's note).
- The walk to the standby place has no hypothesis in the robot's task model, so a scenario with a standby entry is
  classed as containing unmodelled behaviour, and its purpose says so (`docs/assumptions.md` 1.2). PARKED for after the
  milestone, not ruled: whether the robot's mind holds a hypothesis for the human stepping aside.
- In the IR test-bed setup (B14, kind 1) the case with the assigned scan of the pallet in the truck is declared
  dependent on the robot; its priority list never finishes, so that run has no walk to the desk (B13, assumptions 1.1).
- REQUIREMENT on the later preparation of the IR test-bed and the MPB on dock_loading: the instruments obtain the human's
  run-time sequence from the executor's own selection rule; they do not implement that rule a second time. Reason: one
  definition. (Under R1 the load-time replay no longer gives that sequence for a script with a standby entry.)
- Finding: a robot task with no applicable method stops the run (C4, TODO-152).

STAGE 1, STEPS 0 TO 5 BUILT (1 October 2026; built and accepted, each against the plan's acceptance and stop conditions).
- Step 0: the HEAD runs of the extended set (the four maintained sets, the ten kitting drop scenarios, the IR and MPB
  test-bed sets), kept outside git as the reference set of every later step; no commit.
- Step 1, the rename "zone" to "area": 8d064ca; the stale references to removed dock_loading files: c21f001.
  ADDED (records, 1 October 2026): acceptance, 655 reference files byte-identical, 220 tests.
- Step 2, the declared areas and the agent's area in a computed state (A9, R2): b513b82; the layout's per-object area
  field dropped: 9bca721; `shared/io_contracts.md`: a76054f.
  ADDED (records, 1 October 2026): acceptance, 844 reference files byte-identical, 225 tests.
- Step 3, liveness by applicability (A4) and `AdaptivePlanner.is_applicable`: bd4bddc.
  ADDED (records, 1 October 2026): acceptance, 847 reference files byte-identical, 232 tests.
- Step 4, object states and designations (A5): b74485b; `shared/io_contracts.md`, `domains/README.md`: 50f2fb8.
  ADDED (records, 1 October 2026): acceptance, 847 reference files byte-identical, 241 tests.
- Step 5, the human's script form (A3): 048a36e; `shared/io_contracts.md`: 576f2b2.
Next: step 6 (dock_loading's catch-up, with the area ids), step 7 (the domain's content), then the milestone (step 8).
NOTES (records, 1 October 2026; facts of the build, not rulings):
- The shared function for a position's area is `area_at(position, areas)` (the plan's 3d named it `area_of`); the
  planner's lookup for an object's area keeps the name `area_of`.
- A setup entry that still carries the old per-object state fields (`is_empty`, `is_scanned`) is ignored for those
  fields, not refused. An authoring risk, parked under TODO-151; step 4 was not widened.
- A dock_loading grasp raises an explicit error (the action declares no `moved_object_key`) until step 6 gives `pick_up`
  its final form. Intended; no fixture grasps.
- Step 2 made the walks of kitting's load-time replay 1 to 3 ticks shorter (the replay's walk ends where the body stops,
  answer 5); no maintained output contains them.
- Step 3 removed two dead branches, in the adequacy test and in the warrant, with no change of output.
- A closing entry begun and not finished at the run's end counts as open. A dependent script always writes its end line
  (`[rec] end step=n open=-` when no entry is open).
- The log wording for a hypothesis that never enters the live set, `[IR-inapplicable] step=N <key> does not enter the
  live set: no applicable method`, is confirmed as built.
- Four frozen analysis scripts no longer run since the rename (step 1): `analysis/i4_evidence_model/check_i4.py`,
  `analysis/g1_graded_evidence/unit_checks.py`, `analysis/i4c_episode/check_i4c.py`,
  `analysis/i4d_fold_unknown/check_i4d.py`; they need the old field names. Frozen records: not edited.

STAGE 1, STEPS 6 TO 8 BUILT (1 October 2026; built and accepted, each against the plan's acceptance and stop
conditions; the milestone accepted by Hadi).
- Step 6, dock_loading's catch-up (the forms brought up to kitting's; the area ids `area_hall`, `area_office`,
  `area_truck_side`; `domains/dock_loading/script.py`; `domains/README.md` rewritten): 670cb78; `list_scenarios.py`
  lists every domain, `SimModel.get_movable_objects` removed (no reader): 610fed9.
- Step 7, the domain's content (the plan's section 4: 16 robot methods, 11 human methods, the declared states, the task
  model): 1492789; its tests, `tests/test_tg_dock_tasks.py`: 512a452.
- Step 8, the milestone: the two allowed one-line corrections (the stale note on `ProcessCompletion` in
  `shared/types.py`; the viewer's colour keys for the three area ids): 52b2aae; the three scenarios, scenario_s03_02
  (env_layout_02, env_setup_03), scenario_s05_02 (env_layout_03, env_setup_05), scenario_s07_02 (env_layout_04,
  env_setup_07), as the plan's answer 8 states them: 8b9d267. Prior on, 800 steps, headless. The acceptance held in all
  three rooms: the run ends with no error; the robot completes both tasks; every entry of the human's script is closed,
  the closing part included (`[rec] end step=800 open=-`). The maintained sets byte-identical, 301 tests.
  Completion ticks (the world tick; the declared tick in brackets), env_layout_02 / env_layout_03 / env_layout_04:
  `deliver_pallet(pallet_0)` 64 / 64 / 57; `load_return(pallet_4)` 125 (127) / 125 (127) / 151 (153); the scan,
  `is_scanned` holds / the record closes the entry, 92, 94 / 92, 94 / 74, 76; `go_to(desk)` completes 140 / 140 / 112.
FINDINGS OF THE MILESTONE (Hadi and the design chat, 1 October 2026, on ccode's report; each with its classification):
- The walk to the standby place and the meeting at a shared bay (the plan's section 5, last point) were not exercised:
  the human starts at the standby place, where `go_to(standby_place)` is complete, so the machine waits there (the skip
  rule), and the robot's second task was a return. A gap of the scenario. A second simple scenario per room follows.
  The three descriptions state that the standby walk is not taken.
- env_layout_02 and env_layout_03 produced identical motion: the scenario uses neither of the two objects that differ
  between them (the frozen bay, the coffee machine). The recognition differs (the coffee machine), the motion does not.
- In env_layout_04 the human passes the standing robot at 22.5 cm (ticks 66 to 69). The robot had left the bay toward
  the empties, decided to hold at tick 63 before the scan was admitted (admitted at 69), and stood about 95 cm from the
  bay's point, on the human's straight line to the bay. Classified: the parked case of the human walking toward the
  robot (X3, TODO-135); a standing robot does not violate by definition (F1); the simulated human does not react to the
  robot. Note: in this domain the case is structural, because a scan becomes applicable at the moment of delivery, so
  the human walks to a bay when the robot leaves it. Whether to reopen the parked case is decided after the MPB, with
  counts from all rooms.
- A measure for the evaluation: the number of ticks in which the human passes a standing robot closer than the minimum
  separation, reported separately from violations by a moving robot. Reason: the hold turns a closeness that would
  count against a moving robot into one the present measure does not count. Nothing is added to the code for it now
  (TODO-144, TODO-135).
- In env_layout_02 the walk to the desk is admitted as coffee_break (tick 112). The recorded effect of an unmodelled
  walk read as the nearest modelled task ("T-D G", the movement source's half-plane test; TODO-140); no consequence in
  this run.
- Candidate finding about the mind, NOT RULED: the robot's own delivery makes the scan applicable, and the robot does
  not anticipate the human's walk to that bay; the scan hypothesis enters at an equal share and is admitted 8 to 12
  ticks after the human starts (TODO-154).
- Parked question, now with evidence, NOT RULED: whether the robot's mind holds hypotheses for the walks to the standby
  place and to the desk (TODO-155; it carries the approval's parked note on the human stepping aside).
- On a fixture with no assigned tasks for the human, every task of the robot's task model becomes a hypothesis: the
  parked case TODO-143. With the restriction off, two hypotheses about empty pallets become possible: artefacts of
  running without the prior (`docs/assumptions.md` 1.4).
NOTES FROM THE INDEPENDENT REVIEW of dock_loading's task file against kitting's (records, 1 October 2026). The file
follows kitting's building blocks and rules; no special case for dock_loading exists in shared code.
- The robot's methods use a pallet's emptiness as a proxy for the side of the gate on which its origin lies. True for
  every pallet the robot handles in stage 1. False in stage 2, when a full pallet has an origin in the hall (TODO-156).
- The method for "holding another full pallet" (return_full) has no condition of its own; it is correct through its
  position after the method for an empty one (return_empty) and through equal gate conditions.
- `stand` has one method with no area condition: over-broad, and the stated exception to "the absence of a method is
  the check" (the plan's section 4).
- `office_break` waits 60 seconds, copied from `coffee_break`; no record gives the value; Hadi's word is pending
  (TODO-157).
- One dictionary is shared by eight methods: a maintainability risk with no behavioural effect.
- A design question for stage 2, to rule before `store_pallet`: a route is selected from the areas of the agent and of
  the object, not from the kind of task and the pallet's state (TODO-156).
A STEP ADDED (Hadi, 1 October 2026), before the IR test-bed and the MPB run on dock_loading: the earlier analyses in
`analysis/` and the tests are sorted under kitting, so that nothing of kitting is mixed with dock_loading's. The
instruments' code is shared; their run sets, expectations and reports are per domain. Its own commit, no change of
behaviour; the maintained sets and the reference set byte-identical; every path named in a record or a README updated.
Next: the second simple scenario per room; then the step added above, with the preparation of the instruments (the
plan's section 7, "After the milestone"); then the IR test-bed scenarios, agreed with Hadi before they are authored.
STAGE 1, THE SECOND MILESTONE SCENARIO BUILT (1 October 2026; built and accepted, records 1 October 2026).
- Built: scenario_s03_03 (env_layout_02, env_setup_03), scenario_s05_03 (env_layout_03, env_setup_05), scenario_s07_03
  (env_layout_04, env_setup_07), one per room on the MPB setups, identical in content: the robot is assigned
  `deliver_pallet` of pallet_0 and pallet_1 (the dry bay) and of pallet_2 (the frozen bay) and `load_return(pallet_4)`;
  the human is assigned the three scans, with the script [the three scans, the dry bay's first,
  `RepeatableEntry(go_to("standby_place"))`], closing [`go_to("desk")`], `ScriptDependence.ON_ROBOT`. Each description
  states the purpose and the unmodelled behaviour (the walk to and the stay at the standby place, the walk to the desk).
  0371035. Prior on, `single_task`, 1000 steps, headless. The acceptance held in all three rooms: the run ends with no
  error; the robot completes its four tasks; every entry of the human's script is closed, the closing part included
  (`[rec] end step=1000 open=-`). The maintained sets byte-identical, 301 tests.
  Completion ticks (the world tick; the declared tick of the last task in brackets), env_layout_02 / env_layout_03 /
  env_layout_04: `deliver_pallet(pallet_0)` 64 / 159 / 148; `deliver_pallet(pallet_1)` 182 / 276 (278) / 285 (287);
  `deliver_pallet(pallet_2)` 289 (291) / 58 / 57; `load_return(pallet_4)` 125 / 220 / 236; the scans, `is_scanned`
  holds / the record closes the entry: pallet_0 92, 94 / 188, 190 / 164, 166; pallet_1 209, 211 / 303, 305 / 301, 303;
  pallet_2 318, 320 / 84, 86 / 83, 85; `go_to(desk)` completes 346 / 351 / 339.
- Exercised:
  - The priority rule: the first applicable open entry is taken. In env_layout_03 and env_layout_04 the robot delivered
    pallet_2 first, and the human scanned it first, against the written order.
  - The walk to the standby place between scans: two per room (env_layout_02 94 to 121 and 211 to 238; env_layout_03 86
    to 111 and 190 to 217; env_layout_04 85 to 110 and 166 to 182).
  - The frozen bay, which makes the three rooms differ in motion and in recognition.
  - Each scan hypothesis enters the live set on the tick of its delivery (A4, `[IR-reentry] ... live again:
    applicable`).
- Not exercised: the robot arriving at a bay where the human stands, and two scans possible at once in one bay. Reason:
  a round trip to the truck takes about 96 ticks and a scan from the standby place 16 to 30, so the human finishes
  before the next pallet arrives; at every delivery the human was at the standby place, and the live intervals of the
  scans never overlap. The note on B14 ("that conflict is certain whenever both concern the same bay") is corrected
  there: it requires that the human is still at the bay when the robot arrives. Consequence recorded for the MPB's
  design on dock_loading, NOT RULED: a setup in which some pallets already stand in a bay while the robot delivers
  others.
FINDINGS OF THE SECOND MILESTONE SCENARIO (Hadi and the design chat, 1 October 2026, on ccode's report; each with its
classification):
- Five of the six walks to the standby place are admitted as coffee_break or office_break on the observation warrant,
  wrongly (env_layout_02 at 114 and 231, coffee_break; env_layout_03 at 109, coffee_break, and 206, office_break;
  env_layout_04 at 94, office_break; the sixth, env_layout_04 166 to 182, never clears theta). The finding turns
  unexplained once the human stands, and the gate refuses with `none(leader_inadequate)`. No consequence on a decision
  in these runs. The parked question TODO-155: the walk follows almost every scan in this domain, so the case is
  frequent. It becomes the first design question before the IR test-bed set. NOT RULED.
- At the end of every run the human walks up to the standing robot: 8.69 cm (env_layout_02, at 320), 13.41 cm
  (env_layout_03, at 301), 8.11 cm (env_layout_04, at 299); 9 / 8 / 8 ticks below the minimum separation with a
  standing robot, 0 with a moving robot in all three. The robot's last task is a delivery, and a robot with an empty
  pool stays where it is, at the bay the last scan walks to. The parked case of the human walking toward the robot
  (X3, TODO-135). PROPOSAL for stage 1, NOT RULED: an authoring convention that the robot's last assigned task is a
  return.
  CLOSED, NOT TAKEN (Hadi, 2 October 2026; T-G records 10; THE MPB ON DOCK_LOADING, MPB-DL4): the robot's pool is
  unordered and the meta-planner selects by cost. In its place the MPB reports the separation counts per room.
- In env_layout_03 at tick 64 the robot changes its task on the fallback projection while the gate refuses (below
  theta): at 60 the three candidates lay within 0.6 and `load_return` won; at 64 the fallback, the human walking
  straight toward the robot, charged `load_return` a shift of 4 and `deliver_pallet(pallet_0)` won, 94.68 against
  97.46. The conflict enters the cost and decides the choice. Consistent with the design; noted for track 3b
  (TODO-145).
- The scan at the frozen bay is late because the coffee machine lies in the same direction from the standby place:
  in env_layout_04 it enters at 57 and is admitted at 76, 19 ticks after; in env_layout_02 it enters at 289, leads from
  308 (19 ticks after) and clears theta at 315 (it is the last scan, see the next point). TODO-154, with the room's
  geometry.
- The last scan is never admitted (env_layout_02 pallet_2, env_layout_03 and env_layout_04 pallet_1), because an empty
  pool gives no further decision. Noted, no action.
Next: the design of the IR test-bed set with Hadi (first question: TODO-155); then the sorting of the earlier analyses
and tests under kitting, with the preparation of the instruments (the step added above); then the set's authoring and
its runs.
RULED (Hadi, 1 October 2026; recorded in T-G records 8, 1 October 2026): T-G Q16, the duration of office_break, and the
IR test-bed set on dock_loading. Records only; nothing in this block is built.
- Q16, the walk to the standby place in the robot's mind (TODO-155).
  The walk stays without a hypothesis for now. The IR test-bed set observes how the present recognizer explains it; that
  is the baseline.
  Two candidates are recorded on TODO-155, neither approved for building:
  - H1: a foreseeable task "the human steps aside to the standby place", always possible, with the standby place as a
    fixed object.
  - H2: a hypothesis that is live only while no assigned task of the human is applicable.
    CORRECTED (Hadi, at the approval of the IR test-bed's build, 1 October 2026; recorded 2 October 2026, T-G records
    9): worded "a hypothesis that is live only while no assigned task of the human is live". Reason: a scanned pallet's
    scan stays applicable (its guards do not read is_scanned), so read as "applicable" H2 would never be live after a
    scan.
  The difference: the human steps aside only when no other pallet is applicable. H1 states an unconditional behaviour
  that the human does not perform, and competes with the scans when a pallet waits; H2 matches the condition and changes
  the rule for the live set (A4).
  Not taken: the walk as the tail of the scan task. Reasons: the human would step aside after every scan, also when a
  pallet waits; the condition "no other pallet waits" cannot be stated in a method; the scan's terminal fact would hold
  in the middle of the task.
  NOTE (records, 2 October 2026; T-G records 9), on H1: the always-possible standby task, as a walk only, would make
  move_to a terminal action of the task model (the last action of one of its methods), so under L1 every arrival at any
  target would be an episode boundary. A wait at its end would avoid that.
  For stage 1.5, one design question, NOT RULED: what sets a hypothesis's share at the start of an episode. Four
  determinants are recorded for it: the assignment (exists); context facts; the task that just ended (a transition prior
  between tasks, Hadi's idea); an enabling event, such as the robot's own delivery (TODO-154). They are designed as one
  mechanism. Recorded under C1, STAGE 1.5.
  Also for stage 1.5, Hadi's ideas, NOT RULED: the duration of a foreseeable task is not one fixed number; temporal
  context can be a fuzzy set with a degree of membership. Recorded under C1, STAGE 1.5.
- The duration of office_break (TODO-157, closed as ruled): `office_break` lasts 90 seconds; `coffee_break` stays 60.
  Reason: a long absence lets pallets accumulate in a bay, which gives two scans possible at once and the robot arriving
  at an occupied bay; it differs clearly from the coffee break. The change of the value is made in the next build step.
  B6's note.
- The IR test-bed set for dock_loading, agreed: 14 controlled scenarios (C1 to C14) and 4 mixed (M1 to M4), each in all
  three rooms (env_layout_02, env_layout_03, env_layout_04), on the room's IR setup (kind 1 of B14: env_setup_02,
  env_setup_04, env_setup_06; pallet_0 and pallet_1 in the dry bay, pallet_2 and pallet_3 in the frozen bay, pallet_4 in
  the truck), the robot idle on the gate's centre, the human starting at the standby place, the closing part the walk to
  the desk (B13). "scan n" is `confirm_delivered_pallet` of pallet_n; where no assignment is named, the assigned tasks
  are the script's scans. The script of each, with its purpose:
  - C1: scan 0, scan 2 (assigned work, two bays).
  - C2: scan 2, scan 0 (order).
  - C3: scan 0, scan 1 (two scans with the same motion).
  - C4: scan 0, 2, 1, 3 (lifecycle over many episodes).
  - C5: scan 0, coffee_break, scan 2 (a foreseeable task between scans).
  - C6: scan 0, office_break, scan 2 (the office and its door).
  - C7: scan 0 with coffee_break started on arrival at the pallet; scan 2 (a foreseeable task inside a scan).
  - C8: scan 0 with coffee_break cut into the walk to the pallet; scan 2 (an interruption inside a walk).
  - C9: scan 0 dropped during its walk; scan 2 (a dropped scan).
  - C10: scan 0 dropped; scan 2; scan 0 as a second entry (an authored retry; Q12).
  - C11: scan 0; a stand in the hall; scan 2 (the long stand).
  - C12: assigned the scans of 0 and 2; script: scan 1, scan 2 (a scan outside the assigned set).
  - C13: assigned the scans of 0 and 4; script: scan 0, scan 4, the standby entry; dependent (the standby walk from the
    dry bay; a hypothesis never live).
  - C14: assigned the scans of 2 and 4; script: scan 2, scan 4, the standby entry; dependent (the standby walk from the
    frozen bay).
  - M1: scan 0 with coffee_break on arrival; office_break; scan 2.
  - M2: scan 0 dropped; coffee_break; scan 2; scan 0.
  - M3: scan 0; a stand; scan 1 with coffee_break cut into the walk.
  - M4: assigned 0, 2, 4; script: scan 1; office_break; scan 2; scan 4; the standby entry; dependent.
  Rules of the set:
  - The controlled scenarios run and are read first; a mixed scenario is read only against what the controlled ones have
    shown.
  - Expectations are derived from the records before the runs (as in "The IR test-bed").
  - Nothing is adjusted to a result; findings are classified (`docs/assumptions.md`).
  - The standby walks (C13, C14, M4) are diagnostic observations. Beside the expectation under the present model, the
    predictions under H1 and under H2 (Q16) are written down before the run. Only the present model's expectation is
    compared with the run.
  NOTE (T-G records 8, not a ruling; a consequence of Q14 and B14 to be confirmed by Hadi): in C13, C14 and M4 the scan
  of pallet_4 never becomes applicable (the robot is idle, pallet_4 stays in the truck), so its entry stays open, the
  priority list is never finished and the closing part, the walk to the desk, is not taken; the record states the
  entries still open at the run's end (Q13b).
Next: the build step that sorts the earlier analyses and tests under kitting and prepares the instruments for dock_loading
(the step added above, with the plan's section 7, "After the milestone"); then the authoring of the set, its
expectations and its runs.

STAGE 1, THE IR TEST-BED ON DOCK_LOADING BUILT, RUN AND ACCEPTED (1 to 2 October 2026; accepted by Hadi, 2 October
2026; records 2 October 2026, T-G records 9). The results are recorded here because the design chat cannot read
analysis/; the report is analysis/dock_loading/ir_testbed/REPORT.md.
BUILT, with the commits and the acceptance of each part:
- The sort of kitting's analyses and tests (746fae6, 9a35af1, ae77689): analysis/kitting/ (every earlier analysis,
  the four maintained sets, kitting's IR test-bed and MPB sets), analysis/instruments/ (the shared code;
  run.sh <domain>), analysis/dock_loading/; the run files under configs/kitting/; the tests under tests/kitting/,
  tests/dock_loading/, tests/instruments/ (three two-domain tests stay at tests/). The path table:
  docs/rename_table.md, "Paths: the sort"; dated entries, frozen reports, descriptions and comments keep the old paths.
  Acceptance: the reference set regenerated from the sorted tree, 847 files, 844 byte-identical and the three stdout
  files differing in the run-file path token only; the four maintained sets byte-identical; 301 tests, the same ids;
  the moves pure renames apart from 14 path-edited scripts and 33 run-file headers; 83 scenarios load.
- The instruments prepared for dock_loading (65273e8, cbeefe4, e573e9e; then 3ea4b60, 736eb01, e4fc88c):
  - the human's run-time sequence from the executor's own selection rule: the trajectory drives a StackMachine on the
    whole script (repeatable entries and the closing part included) as the body drives it, against the world the
    environment's builder makes; the load-time replay is no longer the source (R1 skips the standby entry);
  - the oracle brought to liveness by applicability (A4), the agent's area (A9, R2) and the boundary through each
    terminal action's preconditions and completion (L1's as-built reading; adds scan_it), the domain from the run file;
  - the log reader: the pool read without kitting's words, the [IR-inapplicable] lines;
  - the separation counts per run (separation.md): a moving robot violating or receding, and a standing robot with
    the human passing (moved on the tick) or standing beside it (did not);
  - the figure: a fourth colour and a facet beyond four hypotheses; the summary's open entries; baseline.py (reporting).
  Acceptance: kitting's 17 IR and 16 MPB trajectories and 17 expectation tables byte-identical before any run; the 17
  IR runs and the 16 MPB scenarios under each strategy byte-identical in every output apart from the new separation
  files (17 and 32); 301 tests.
- office_break at 90 seconds (edbe34f). Acceptance: the four maintained sets byte-identical (96 files); the milestone
  reruns identical except scenario_s05_03 at tick 206 and scenario_s07_03 at tick 94, the decision admitting
  office_break (T_h 15 ticks longer, one candidate's share; winner, cost and hold unchanged, the .rec identical).
- The 54 scenarios (51e5e1c): scenario_s02_02 to _19 (env_layout_02, env_setup_02), s04_02 to _19 (env_layout_03,
  env_setup_04), s06_02 to _19 (env_layout_04, env_setup_06), in domains/dock_loading/scenarios/scenarios_s02.py,
  _s04.py, _s06.py; _02 to _15 the controlled rows C1 to C14, _16 to _19 the mixed M1 to M4; run files in
  configs/dock_loading/ir_testbed/. Authoring values approved by Hadi: a cut or a drop during a walk at PT28S; the
  stand at the bay just scanned, stand(PT80S); M3 with scan 2 in place of scan 1; C13, C14, M4 dependent on the robot.
  Acceptance: 137 scenarios load; the three dependent scripts report the entries not replayed.
- The expectations committed before the runs (54edb71): per scenario the trajectory, expected.csv and phases.json (θ =
  0.75, the value of record) and predictions.md (C13, C14, M4: the present model beside H1 and H2); every run's own
  oracle call reproduced them byte for byte.
RESULT: 42 controlled runs (4d9011d) and 12 mixed runs (b20a67f), zero disagreements, zero unmatched rows; every
trajectory equal to the run's human lines on every tick; separation counts 0 (the closest approach 115.85 cm). What it
establishes: the recognizer behaves on dock_loading as the records specify (rules 1 to 27 of the instrument). It does
not establish the quality of the recognition.
THE BASELINE (all 54 runs; one tick is 2 seconds): of 153 true stretches, 147 lie in the support (6 outside: the scan
of pallet_1 in C12 and M4). 98 of the 147 reach the threshold within the stretch (38, 40 and 20 of 49 on env_layout_02,
_03, _04); the median delay is 20 ticks (range 6 to 50; 28, 16 and 17 by room). 49 never reach it, all scans: 34
stretches of 26 ticks or fewer, 9 same-motion pairs, 3 second scans with no walk, 3 scans leaving the office in
env_layout_02. Every coffee_break and office_break stretch reaches it. Ticks from each true stretch's start to the
threshold, per row and room ("never": not within the stretch; "out": outside the support):
| row | env_layout_02 | env_layout_03 | env_layout_04 |
|---|---|---|---|
| C1 | scan 0 10, scan 2 50 | scan 0 14, scan 2 24 | scan 0 never, scan 2 never |
| C2 | scan 2 25, scan 0 28 | scan 2 8, scan 0 34 | scan 2 21, scan 0 never |
| C3 | scan 0 never, scan 1 never | scan 0 never, scan 1 never | scan 0 never, scan 1 never |
| C4 | scan 0 never, scan 2 never, scan 1 28, scan 3 50 | scan 0 never, scan 2 never, scan 1 34, scan 3 24 | scan 0 never, scan 2 never, scan 1 never, scan 3 never |
| C5 | scan 0 10, coffee 49, scan 2 never | scan 0 14, coffee 13, scan 2 19 | scan 0 never, coffee 17, scan 2 10 |
| C6 | scan 0 10, office 33, scan 2 never | scan 0 14, office 30, scan 2 14 | scan 0 never, office 6, scan 2 37 |
| C7 | scan 0 10, coffee 50, scan 0 27, scan 2 50 | scan 0 14, coffee 17, scan 0 15, scan 2 24 | scan 0 never, coffee 21, scan 0 never, scan 2 never |
| C8 | scan 0 10, coffee 37, scan 0 26, scan 2 49 | scan 0 never, coffee 11, scan 0 15, scan 2 24 | scan 0 never, coffee 20, scan 0 never, scan 2 never |
| C9 | scan 0 10, scan 2 31 | scan 0 never, scan 2 21 | scan 0 never, scan 2 10 |
| C10 | scan 0 10, scan 2 31, scan 0 28 | scan 0 never, scan 2 21, scan 0 34 | scan 0 never, scan 2 10, scan 0 never |
| C11 | scan 0 10, scan 2 46 | scan 0 14, scan 2 21 | scan 0 never, scan 2 17 |
| C12 | scan 1 out, scan 2 50 | scan 1 out, scan 2 24 | scan 1 out, scan 2 never |
| C13 | scan 0 9 | scan 0 14 | scan 0 14 |
| C14 | scan 2 25 | scan 2 8 | scan 2 21 |
| M1 | scan 0 10, coffee 50, scan 0 27, office 34, scan 2 never | scan 0 14, coffee 17, scan 0 15, office 30, scan 2 13 | scan 0 never, coffee 21, scan 0 never, office 6, scan 2 36 |
| M2 | scan 0 10, coffee 37, scan 2 never, scan 0 28 | scan 0 never, coffee 11, scan 2 19, scan 0 33 | scan 0 never, coffee 20, scan 2 never, scan 0 never |
| M3 | scan 0 10, scan 2 never, coffee 33, scan 2 never | scan 0 14, scan 2 never, coffee 13, scan 2 19 | scan 0 never, scan 2 never, coffee 7, scan 2 11 |
| M4 | scan 1 out, office 33, scan 2 never | scan 1 out, office 30, scan 2 15 | scan 1 out, office 8, scan 2 37 |
FINDINGS (classified as findings about the mind; none ruled):
- Hypotheses that predict the same motion divide the belief and are not admitted: the watched item C5, confirmed (C5's
  note). Linked to the recorded direction on acting on a set of hypotheses with the same projection (TODO-97).
- A short walk gives too little evidence under equal shares at the start of an episode (34 of the 49 stretches that
  never reach the threshold last 26 ticks or fewer; on env_layout_04, 16 steps from the standby place to the dry bay,
  scan 0's first walk never reaches it with three or more rivals live). It joins stage 1.5's question on what sets a
  hypothesis's share at the start of an episode, as its measured baseline (C1, STAGE 1.5; TODO-154).
- The walk to the standby place: admitted as a break in five of six controlled runs (C13 and C14: coffee_break or
  office_break by the room's bearings, cleared 8 to 23 ticks into the walk; never above θ in scenario_s06_14); in M4
  admitted on env_layout_02 as the scan of pallet_0 (from 167), an assigned task the human never performs and that stays
  live with its commitment warrant. The finding turns unexplained once the human stands. On TODO-155, with the written
  predictions: C13 and C14 separate the conditional candidate (H2) from the present model, M4 does not (H2 is never live
  there, scan 0 being live).
- Two pallets in one container stand on one point: the second scan has no walk and a walk between them cannot be cut;
  a property of "one point per container" (B9's note).
CORRECTIONS of earlier notes: one tick is 2 seconds (B6's note: office_break's wait 45 ticks, the absence about 110
ticks, reviewed with the MPB's design); H2 worded "no assigned task is live" (Q16's block); the always-possible standby
task as a walk only would make every arrival an episode boundary (Q16's block).
The IR test-bed of stage 1 is CLOSED. Next: the design of the MPB set with Hadi. Open for it: a setup with pallets
already in a bay while the robot delivers others; the robot's last task as a return (the PROPOSAL of the second
milestone's findings); how expected decisions are derived when the human's sequence depends on the robot's decisions
(C6).

RULED (Hadi, 2 October 2026; recorded in T-G records 10, 2 October 2026): THE MPB ON DOCK_LOADING, its design, ruled as
one package (MPB-DL1 to MPB-DL6; the labels are this block's, distinct from kitting's MPB-1 to MPB-6). Records only;
nothing in this block is built. The MPB of stage 1 is a test and an analysis; it changes nothing in the framework. The
scenario set itself is not yet agreed and is not recorded here. "As kitting's MPB rules" refers to "The meta-planner
test-bed (MPB)".
- MPB-DL1, the claim.
  The MPB on dock_loading has two parts.
  Part 1: a few of kitting's decision paths re-instantiated on dock_loading.
  Part 2: one scenario for each case that dock_loading adds:
  (i) a hypothesis that enters the live set during the run through the robot's own act (a scan becomes live when the
      robot puts the pallet down; liveness by applicability, A4);
  (ii) decisions on the fallback projection as the frequent case;
  (iii) two hypotheses with the same motion waiting in one bay, so that the gate refuses during the walk;
  (iv) an admission that is correct by the records and wrong about the human (the walk to the standby place admitted as
       a break). The expectation states that admission before the run. The run agreeing with it is not a disagreement;
       the wrong reading is a finding about the mind (TODO-155, Q16);
  (v) the human in another area (the office), with methods selected by area (B11);
  (vi) the robot and the human at the same bay while the robot has an alternative task;
  (vii) a human's script that depends on the robot (Q13b).
  The set does not claim full coverage of the decision paths on dock_loading. Kitting's coverage matrix
  (analysis/kitting/mpb/coverage.md) is not repeated.
  Reason: T-G tests that the chain stays domain-independent. The chain's code is shared, and its paths are verified on
  kitting. A second full matrix would test the same paths again.
  AMENDED (Hadi, 2 October 2026; T-G records 11; DISPOSITIONS, D4): cases (i) and (vii) are mixed scenarios with
  declared properties. Reason: the entry tick of the scan is the robot's delivery tick, which is not derivable before
  the run.
- MPB-DL2, a new setup kind per room, for the MPB's controlled scenarios.
  The setup: one full unscanned pallet already in each delivery bay, designated to the bay it stands in; one full pallet
  in the truck designated to each delivery bay; two empty pallets in the empties container, designated to the truck.
  The human scans only the pallets that stand in the bays at the start.
  A meeting at a bay is authored by a stand or a break at the bay. Its timing is computed from path lengths before any
  run.
  Reason: in setup kind 2 (B14) a scan becomes applicable only at the robot's delivery, so the human's script depends on
  the robot. A round trip to the truck (about 96 ticks) is longer than a scan (16 to 30 ticks), so the robot never
  arrives at a bay where the human stands (the second milestone scenario). Pallets already in the bays give a script
  that is independent of the robot.
  The kind recorded earlier as conditional (B14: all full pallets designated to one bay, added only if the first MPB run
  calls for it) keeps its condition.
  The names of the new kind and of the conditional kind are not ruled. The records step proposed names in its report
  (T-G records 10); nothing that exists is renamed.
  AMENDED (Hadi, 2 October 2026; T-G records 11; DISPOSITIONS, D2), a correction before any run: the new kind has two
  full unscanned pallets in each delivery bay at the start, not one, each designated to the bay it stands in. Reason:
  the same-motion case (MPB-DL1 (iii)) needs two scans in one bay; with one pallet per bay it cannot be a controlled
  scenario. A scenario that assigns one scan per bay is unaffected: the other pallet's scan is outside the support.
  CORRECTED (the same ruling; DISPOSITIONS, D3): "a break at the bay" is withdrawn; no break ends at a bay. The meeting
  at a bay has two forms. Form 1: the human walks to the bay on an admitted scan while a delivery of the robot goes to
  that bay. Form 2: the human stands at the bay after a scan (a `stand`, unmodelled behaviour), and the robot decides on
  the fallback projection.
  NAMED (the same ruling; DISPOSITIONS, D7): the new kind is kind 3, "pallets in the bays"; the conditional kind is kind
  4, "one bay". Two setups of kind 3, for env_layout_03 and env_layout_04 (D6).
- MPB-DL3, expected decisions. It answers, for stage 1, the third clause of C6: how the MPB's oracle derives an expected
  decision when the human's sequence depends on the robot's decisions.
  - Controlled scenarios: scripts independent of the robot only. Full expectations (trigger and cause, gate,
    projection) are committed before the run, as kitting's MPB rules (MPB-1, MPB-3).
  - Mixed scenarios: a script that depends on the robot is allowed. Properties are declared before the run and checked
    on the run. This is the weaker check. Those runs do not validate the recognizer's decisions, and no record may claim
    that they do.
  - Not taken: a check per decision derived from the logged state at the decision tick. Reason: it conditions on the run
    and needs new instrument code.
  AMENDED (Hadi, 2 October 2026; T-G records 11; DISPOSITIONS, D1 and D5): the controlled scenarios are also bound by
  the disjointness rule (MPB-DL7). A mixed scenario is either dependent on the robot, on kind 2, with declared
  properties, or independent of the robot, on kind 3, with full expectations committed before the run. Each scenario
  states its kind.
- MPB-DL4, the robot's last task.
  The proposal "an authoring convention that the robot's last assigned task is a return" (FINDINGS OF THE SECOND
  MILESTONE SCENARIO; TODO-135's fourth instance) is CLOSED, NOT TAKEN.
  Reason: the robot's pool is unordered and the meta-planner selects by cost, so an author cannot fix the last task
  without constraining the selection.
  In its place the MPB reports, per room, the ticks below the minimum separation with a standing robot, beside the
  violations with a moving robot. These counts serve Hadi's later ruling on whether to reopen TODO-135. Nothing is ruled
  on TODO-135 itself.
- MPB-DL5, office_break stays at 90 seconds for the MPB (B6's note).
  Reason: no value is changed for a test set.
- MPB-DL6, strategies and rooms.
  `single_task` is primary and `full_reorder` is the second run, as kitting's MPB rules (MPB-6).
  The set runs in two rooms, env_layout_03 and env_layout_04.
  env_layout_02 is excluded as a reduction of scope, not because it is irrelevant. Its condition of late admission (the
  coffee machine lies in the direction of the walk from the dry bay to the frozen bay; median delay 28 ticks in the IR
  test-bed) remains untested by the MPB.
  Reason for the two rooms: env_layout_03 has frequent admissions and env_layout_04 rare ones (in the IR test-bed's
  baseline, 40 and 20 of 49 stretches reach the threshold), so they give decisions on an admitted projection and on the
  fallback projection.
  Planned size: about 8 controlled and 4 mixed scenarios, 48 runs (two rooms, two strategies). The set is agreed with
  Hadi before it is authored.
  CORRECTED (Hadi, 2 October 2026; T-G records 11; DISPOSITIONS, D8): env_layout_04 also has the frozen bay and the
  coffee machine in one direction from the standby place. The late-admission condition is untested by the MPB only for
  the walk from the dry bay to the frozen bay in env_layout_02.
  SUPERSEDED (the same date; THE SET below): the planned size reads 9 controlled and 4 mixed scenarios, 52 runs.
- MPB-DL7, the disjointness rule (Hadi, 2 October 2026; T-G records 11; DISPOSITIONS, D1). An authoring constraint of
  the controlled scenarios, checked per scenario before its runs: no pallet is named both by the robot's pool and by an
  assigned scan of the human.
  Reason: under it, with the prior on, no act of the robot changes the live set, the belief or the adequacy of a
  hypothesis in the support (the records step's answer, T-G records 10: a scan reads `in_area` of the human and
  `obj_at` of its own pallet; the robot moves only the pallets of its pool; inadmissible hypotheses are skipped before
  the applicability check and stay pinned; the terminal facts, the boundary, the excess path, the standing and the
  warrant are the human's own). It is the dock_loading form of kitting's rule (MPB-3).
  It holds for controlled scenarios only. It is not generalised to mixed scenarios, where a delivery changes
  applicability.
DISPOSITIONS ON THE FLAGS OF T-G RECORDS 10 (Hadi, 2 October 2026; recorded in T-G records 11). D1 to D10 are Hadi's
numbers; each is recorded where it applies:
- D1, the disjointness rule: MPB-DL7.
- D2, kind 3 with two pallets in each delivery bay: MPB-DL2, AMENDED.
- D3, "a break at the bay" withdrawn, the two forms of the meeting at a bay: MPB-DL2, CORRECTED.
- D4, cases (i) and (vii) mixed: MPB-DL1, AMENDED.
- D5, a dependent mixed scenario on kind 2, an independent one on kind 3 with full expectations, each scenario stating
  its kind: MPB-DL3, AMENDED.
- D6, two setups of kind 3, for env_layout_03 and env_layout_04: MPB-DL2, NAMED.
- D7, the names, kind 3 "pallets in the bays" and kind 4 "one bay": MPB-DL2, NAMED; B14's "a third kind", READS.
- D8, the late-admission condition: MPB-DL6, CORRECTED.
- D9, kind 3 is a test condition. No record describes the runs on kind 3 as the domain's work cycle: the pallets the
  robot delivers there are never scanned (B1's reading is the work cycle; M1 below is the set's instance of it).
- D10, the glossary: controlled scenario, mixed scenario, setup kind, disjointness rule, declared property, each
  defined from its use in the records (`docs/glossary.md` §9).
THE SET (agreed by Hadi, 2 October 2026; recorded in T-G records 11). Records only; nothing is authored or run. 9
controlled scenarios (K1 to K9) and 4 mixed (M1 to M4; this set's, distinct from the IR test-bed's M1 to M4 above),
each in env_layout_03 and env_layout_04, prior on, `single_task` primary and `full_reorder` second: 52 runs.
Common to all: the human starts at the standby place and closes at the desk (B13); the robot starts on the truck side.
On kind 3, pallet_0 and pallet_1 stand in the dry bay and pallet_2 and pallet_3 in the frozen bay. "scan n" is
`confirm_delivered_pallet` of pallet_n. The robot's tasks on kind 3 are deliver-dry and deliver-frozen (the two truck
pallets), return-1 and return-2 (the two empty pallets). Where no assignment is named, the human's assigned tasks are
the script's scans. Every duration and cut point is derived from path lengths before any run, in the build's plan, and
approved by Hadi; the plan shows per room that the geometry gives the declared case.
Controlled (kind 3, a script independent of the robot, the disjointness rule, full expectations before the run):
- K1, the control. Human: scan 2. Robot: deliver-dry, return-1. Tests: no hold at any decision; completion equal to a
  comparison run with the same setup, pool and start and no human.
- K2, admission and the admitted projection (meeting form 1). Human: scan 0, scan 2. Robot: deliver-dry,
  deliver-frozen, return-1. Tests: the decision at the tick the gate clears, against the human's projected walk to the
  bay the robot delivers to.
- K3, the stand at a bay with an alternative task (meeting form 2). Human: scan 0, then a long `stand` at the dry bay.
  Robot: deliver-dry, deliver-frozen, return-1. Tests: decisions on the fallback projection of a standing human, the
  `projection_expired` cadence, the switch by cost.
- K4, the stand at a bay with no alternative. As K3; the robot's pool is deliver-dry only. Tests: the robot holds; the
  holds lengthen at each expiry.
- K5, the same motion. Human: scan 0, scan 1. Robot: deliver-dry, deliver-frozen, return-1. Tests: the gate refuses
  during the walk; the robot decides on the fallback projection of a walking human; scan 1 is admitted alone after
  scan 0.
- K6, a foreseeable task between scans. Human: scan 0, coffee_break, scan 2. Robot: all four tasks. Tests: admission
  on observation warrant during the break walk; the boundary and the re-admission after it.
- K7, the office. Human: scan 0, office_break, scan 2. Robot: all four tasks. Tests: the admitted projection through
  the office door; the robot's decisions while the human is in another area.
- K8, the change during an action. Human: scan 0 with coffee_break cut into its walk; scan 2. Robot: deliver-dry,
  deliver-frozen, return-1. Tests: retraction, the fallback projection after it, re-admission.
- K9, the admission that is wrong about the human. Human: assigned scan 0 only; script: scan 0, `go_to(standby_place)`
  as an ordinary entry, a `stand` there, the desk. Robot: deliver-frozen, return-1. Tests: the walk to the standby
  place admitted as a break (expected so, by the records), the robot's decision against it, the retraction when the
  human stands. The run agreeing with the expectation is not a disagreement; the wrong reading is a finding about the
  mind (MPB-DL1 (iv)). The script has no entry that waits for the robot. The repeatable standby entry is exercised in
  M1, M2 and M4.
Mixed (read only against the controlled ones):
- M1, the domain's work cycle. Kind 2, dependent. Human: the scans of the four delivered pallets, the standby entry.
  Robot: four deliveries, two returns. Declared properties: every robot task completes; every script entry closes; no
  violation with a moving robot; each scan enters the live set on its delivery tick.
- M2, pallets accumulate. Kind 2, dependent. As M1, with office_break after the first scan. Declared properties: as
  M1, plus two scans applicable at once in one bay, and the robot's decision at an occupied bay.
- M3, combined deviations. Kind 3, independent, full expectations. Human: scan 0 with coffee_break on arrival; scan 1;
  scan 2; a `stand` at the frozen bay. Robot: all four tasks. Combines K5, K6 and K3.
- M4, a dropped scan in the work cycle. Kind 2, dependent. Human: the first scan dropped during its walk;
  coffee_break; the other scans; the dropped scan as a second entry; the standby entry. Robot: as M1. Declared
  properties: as M1.
Rules of the set:
- The controlled scenarios run and are read first.
- Nothing is adjusted to a result.
- Findings are classified: kitting's five disagreement classes and the three readings of class 2 carry over (MPB-4).
- The mixed runs with declared properties do not validate the recognizer's decisions (MPB-DL3).
- Every run reports the separation counts: violations with a moving robot, and ticks below the minimum separation with
  a standing robot (MPB-DL4).
Not in the set: env_layout_02 (MPB-DL6); a dropped scan as a controlled scenario.
RULED ON THE SET (Hadi, 2 October 2026; recorded in T-G records 12): the flags of T-G records 11. Records only; nothing
is authored or run.
- The case per room, a principle of the set. A scenario runs in both rooms. Where the records predict that its case
  does not form in a room, the expectation for that room says so before the run. The case counts as tested only where
  it forms. Nothing is changed to make it form.
  Reason: a case engineered into existence tests the engineering, not the chain.
- K2: unchanged. On env_layout_03 it shows the decision at admission. On env_layout_04, where the records predict no
  admission, it shows a decision on the fallback projection.
- K5, AMENDED: the clause "scan 1 is admitted alone after scan 0" is withdrawn. K5 tests the refusing gate and the
  fallback projection.
  Reason: the second scan has no walk and never reaches the threshold in the IR test-bed.
- K8, AMENDED: the cut comes after the tick at which the oracle expects scan 0's admission, derived before the run. The
  retraction forms on env_layout_03 only.
- K9, AMENDED: the human's scan is scan 2 (pallet_2, the frozen bay); the robot's pool is deliver-dry and return-1.
  Reason: the IR test-bed admitted the walk from the frozen bay to the standby place as a break in every room.
- K1, AMENDED: the control requires that the human works away from every robot route. The build's plan selects, per
  room, the scan and the robot's pool that satisfy this and shows the derivation. If no pairing exists on
  env_layout_04, K1 runs on env_layout_03 only, and the record says so.
- K4: the lengthening holds are evidence for TODO-132 (a), not a verified rule.
- M2, AMENDED: office_break is an event on one named scan entry. "Two scans applicable at once in one bay" and "the
  robot's decision at an occupied bay" are not declared properties, because they depend on the order the robot chooses
  by cost. The report states whether each occurred.
- M4, AMENDED: one named scan is dropped during its walk; a second named scan has coffee_break on arrival; the dropped
  scan is a second entry; the standby entry closes the list.
THE BUILD'S PLAN, CONFIRMED (Hadi, 2 October 2026; recorded in T-G records 13): ccode's plan for the MPB set (its
sections a to i: the setups env_setup_08 and env_setup_09 of kind 3; the scenarios scenario_s08_01 to _10 and
scenario_s09_01 to _10 (K1 to K9, M3), scenario_s05_04 to _06 and scenario_s07_04 to _06 (M1, M2, M4); the authored
durations; the instrument's generalisation; the order of the build) with the dispositions below on its open points.
- DL-P1, K8's cut, by a rule: the cut falls on the last step of the walk to the pallet, in both rooms. The cause is
  whatever the oracle derives on kind 3; it is not inferred from the IR test-bed's rows on kind 1.
  Reason: it is the latest change that is still a change during the walk, so scan 0 has received all the walking
  evidence it can receive.
  Procedure, before any controlled run: K8's per-tick table is reported for both rooms, from scan 0's expected
  admission (or the walk's start if none) to 10 ticks after the cut: the leader, scan 0's share, scan 0's hypothesis
  adequacy, the gate's outcome and the expected cause of each decision. On env_layout_03, if the oracle expects the
  retraction, the build proceeds; if it expects "replaced" or no admission, the build stops before the controlled runs
  and reports; no other cut is tried; Hadi rules. On env_layout_04 there is no stop: K8 runs, and if the case does not
  form the expectation and the record say so for that room.
- DL-P2, K3's switch by cost is neither an expectation nor a declared property. K3's exact parts are the fallback
  decisions on the standing human and the expiry cadence. The report states whether the switch occurred and, if it
  did, checks the occupied-target condition (X1). The stand is not lengthened to force it.
  Reason: the selection depends on the robot's realized state; the records do not determine it.
- DL-P3, K1 on env_layout_04 runs with its one-task pool (the human's scan 0, the robot's deliver-frozen).
  Reason: a control needs no hold and an equal completion, not a selection between tasks.
- DL-P4, K9 on env_layout_04: if a `no_current_task` tick masks the retraction (D3's order on a shared tick), the case
  counts as not formed there. Nothing changes.
- DL-P5, the closing walk to the desk admitted as a break is expected by the oracle and is not a disagreement. Each
  instance is recorded as a finding about the mind, with TODO-155.
- DL-P6, admissions near the threshold: the oracle's computed table decides every tick. No hand-derived tick of the
  plan is binding.
- DL-P7, the step cap for a script that depends on the robot (an extension of MPB-5 for this set): the robot's plain
  chain, plus the human's replay on the state after that chain, plus 30 ticks. It bounds the run's length and is not
  an expectation. A run that reaches the cap is reported as such; the cap is not raised after a run.
- DL-P8, a condition on the instrument: dock_loading's horizon code may call the planner's decomposition for the cap
  only. The report shows that no module of the oracle (the per-tick tables, the chain assembly, the compare) imports it
  or anything of the planner, the recognizer, the projection or the robot's perception.
  READ (Hadi, 2 October 2026; recorded in T-G records 15): the condition reads as kitting's MPB-1 reads. The oracle may
  use the task model's decomposition. No module of the oracle imports the cap code (horizon.py). No stricter reading.
- DL-P9, the alteration E3 (every support key live whatever its applicability, T-G A4 switched off in the oracle): if
  undetected on the controlled set, it is recorded as a property of the set with its reason.

SCOPE REDUCED AND THE MPB ON DOCK_LOADING RUN (Hadi, 2 October 2026; recorded in T-G records 14). Hadi reduced the scope
of stage 1's MPB: it establishes that the recognizer and the recognition-to-planning chain run on dock_loading and
produce runs, logs and figures; the behavioural analysis belongs to stage 2. The stop for review between the controlled
and the mixed runs was withdrawn; a class-2 disagreement no longer stops the build (reported with its evidence); the
alteration test on dock_loading is not run in stage 1. Reason: stage 1's purpose is that the chain runs on the second
domain; the deeper analysis needs stage 2's room and tasks.
- What ran: the 26 scenarios of the set (K1 to K9 and M3 on kind 3, scenario_s08_01 to _10 and scenario_s09_01 to _10;
  M1, M2, M4 on kind 2, scenario_s05_04 to _06 and scenario_s07_04 to _06), in env_layout_03 and env_layout_04, prior
  on, single_task and full_reorder: 52 runs, every one completed within its cap; and K1's 4 comparison runs. The
  expectations and K8's table were committed before any run (8fb9981).
- Where: analysis/dock_loading/mpb/ (README.md, authoring.md, predictions.md, REPORT.md with every run's line and the
  md5s; per run the comparison, the properties, the figures and the separation counts; the logs and records in runs/,
  git-ignored); the run files in configs/dock_loading/mpb/; the instrument's shared code in analysis/instruments/mpb/.
- The comparison: the 40 runs with full expectations (K1 to K9, M3) agree with the oracle on parts 1 to 3 at exact
  equality, 0 disagreements; no class-2 disagreement. K1's properties hold against the comparison runs. The mixed
  runs M1, M2, M4 (declared properties only, MPB-DL3): (i), (ii) and (iv) hold in every run; (iii), no violation with a
  moving robot, does not hold in env_layout_04 under single_task (one violation at 387 in each; M2 also 224 to 226).
- Formed or not: K8's retraction formed on env_layout_03 (entered 14, retraction 34) and not on env_layout_04 (no
  admission of scan 0); K9's retraction formed on env_layout_03 (67) and on env_layout_04 under full_reorder (59);
  under single_task it was masked by the robot's no_current_task at 59 (DL-P4, not formed there); K2's admission of the
  scans did not form on env_layout_04; K3's switch by cost occurred on env_layout_04 (single_task at 104, full_reorder
  at 110), not on env_layout_03 (DL-P2: reported, not expected); K4's holds lengthened (13, 48, 96; 10, 48, 96); M2's
  two scans live at once in one bay did not occur; its decision at an occupied bay occurred in every M2 run.
- The walk to the desk (and K9's walk to the standby place) admitted as a break, a finding about the mind with TODO-155
  (DL-P5): coffee_break on env_layout_03 in K1, K2, K6, K7, K8, K9; office_break on env_layout_04 in K2, K6, K7, K8, K9.
- Not tested or not run: the alteration test on dock_loading (built, for stage 2); env_layout_02 (MPB-DL6); the cases
  listed above as not formed.
- Observations for stage 2, unanalysed: (1) M1, M2, M4 on env_layout_04, single_task: a hold of 6 decided at 382 on a
  moving fallback, scan 1 entered at 387 with hold 0, and a moving-robot violation at 387; (2) moving-robot violations
  in K8 full_reorder on env_layout_03 (2) and K9 single_task on env_layout_04 (2); (3) standing-robot ticks below
  min_separation (MPB-DL4, TODO-135's measure) in K3, K4, M3 and the mixed full_reorder runs, up to 15 with the human
  passing and 4 beside; (4) the switch while carrying in K3 on env_layout_04 returns the full pallet to the truck first
  (B8); (5) K9 on env_layout_04: the masking depends on the strategy; (6) the desk walk read as a break in most
  controlled runs; (7) M1 and M4 of one room end on the same terminal tick under each strategy.
- The instrument (no change of framework code): measures.py and the alteration engine shared; run.sh --expect and the
  control list per domain; a script that depends on the robot gets no oracle comparison and its human read from the
  run; dock_loading's horizon.py (DL-P7, DL-P8), properties.py, alteration.py, disjoint.py. Found on the way: HEAD's
  kitting alteration test failed since the IR oracle reads the layout's areas (its scratch copy's root); corrected in
  the shared engine, kitting's table reproduced exactly.
- The regression audit: byte-identical. Kitting's MPB (the sixteen, both strategies and prior off, after
  the generalisation; every committed output and md5; the alteration table), the reference set of stage 1 (the four
  maintained sweeps, the ten drop scenarios, kitting's IR test-bed and MPB; the stdout files differ in the run-file
  paths only, as since the sort), dock_loading's IR test-bed (54 runs, every output and md5); the suite 301 passed;
  every registered scenario of both domains loads (163).
T-G STAGE 1 CLOSED (Hadi, 2 October 2026; recorded in T-G records 15).
- Its purpose was an initial check that the recognizer and the recognition-to-planning chain run on dock_loading.
- Result: the 52 MPB runs completed; zero disagreements wherever full expectations exist; the regression audit
  byte-identical.
- This does not state that the scenarios are free of violations. The declared property "no violation with a moving
  robot" failed in three mixed runs (env_layout_04, `single_task`, tick 387), and controlled runs contain recorded
  separation violations. These are findings carried to stage 2, unanalysed. They do not reopen stage 1.
- Deferred to one housekeeping step, not done now: the sweep of old terms (TODO-153), the sizes of the files under
  docs/, and what of analysis/ stays in git.
- TODO-153, TODO-154, TODO-155 and TODO-156 are tagged [V1].

PROPOSALS (by the design chat, NOT RULED)
- An empty pallet's destination (the truck) as a designation in the setup, so that `load_return` reads `destination_of`
  and names no fixed object.
  RULED (Hadi and the design chat, 1 October 2026; recorded in T-G records 5), B14: the setup designates the truck as the destination of each empty pallet (one rule covers every
  pallet). How `load_return` reads it is for stage 1's plan.
- Two generic load checks in `shared/` that let malformed input through (TODO-151, recorded as a proposal, untagged).
- TODO-131 (the robot-mind object): A8's reduced form does not need it, so its landing in track 4 is no longer implied;
  its placement is open (TODO-131's note).
- Stage 1 may already use the room of B10, with the stores and the freezer present and unused.
  CLOSED, NOT TAKEN (Hadi and the design chat, 1 October 2026; recorded in T-G records 5), B14: B10's room moves to stage 2; stage 1 uses three rooms without stores.
- `pytest` over the whole repo stops on collection errors in `ros_sim/framework_HRI/test/` that predate build 1. Measured
  at 62ebc4e: three files (`test_copyright.py`, `test_flake8.py`, `test_pep257.py`; the `ament_*` modules are missing);
  the proposal named the first.

Reference: cchat, 30 September and 1 October 2026 (T-G); `docs/handoffs/handoff_T-G_onward.md`; ccode's dock_loading
survey (30 September 2026, not committed); "T-H: the human behaviour model"; "Layouts, setups and scenarios"; "An item's
destination table is a fact of the station"; "The successor state is derived from what the action schemas declare"; I2
("Targets, methods and completions are the planner's"); "T-D L" (L4); "T-D X" (X5); `docs/glossary.md` §6, §8, §9, §10;
`docs/assumptions.md` 2.3, 5.1 to 5.3; TODO-02, TODO-08, TODO-09, TODO-10, TODO-16, TODO-25, TODO-30, TODO-39, TODO-81,
TODO-96, TODO-97, TODO-104, TODO-131, TODO-140, TODO-143 to TODO-151; LIMIT-02 to LIMIT-05; DESIGN-01, DESIGN-02,
DESIGN-04, DESIGN-15; REFACTOR-03

Next: the layout and the setup of T-G's stage 1, agreed in the design chat; then stage 1's plan.
SUPERSEDED (T-G records 1, third follow-up, 1 October 2026): the order is the lifecycle question of the human's list
(A3, PARKED), then stage 1's layout and setup, then stage 1's plan.
SUPERSEDED (T-G records 2, 1 October 2026): the lifecycle question is ruled (A3, Q12 to Q15; B13). Next: stage 1's
layout and setup, agreed in the design chat, then stage 1's plan.
SUPERSEDED (Hadi and the design chat, 1 October 2026; recorded in T-G records 5): stage 1's rooms and setups are agreed (B14). Next: stage 1's plan.
SUPERSEDED (Hadi, 1 October 2026; recorded in T-G records 7): stage 1's plan is approved (STAGE 1 PLAN APPROVED above;
`docs/handoffs/plan_T-G_stage1.md`). Next: stage 1's build, step 0 then step 1 (the rename).
SUPERSEDED (records, 1 October 2026): steps 0 to 5 of stage 1 are built and accepted (STAGE 1, STEPS 0 TO 5 BUILT
above). Next: the domain steps, step 6 (the catch-up) and step 7 (the content), then the milestone (step 8).
SUPERSEDED (records, 1 October 2026): steps 6 to 8 of stage 1 are built and the milestone accepted (STAGE 1, STEPS 6
TO 8 BUILT above). Next: the second simple scenario per room; then the sorting of the earlier analyses and tests under
kitting, with the preparation of the instruments; then the IR test-bed scenarios, agreed with Hadi before they are
authored.
SUPERSEDED (records, 1 October 2026): the second milestone scenario is built and accepted, and stage 1's milestone is
complete (STAGE 1, THE SECOND MILESTONE SCENARIO BUILT above). Next: the design of the IR test-bed set with Hadi (first
question: TODO-155); then the sorting of the earlier analyses and tests under kitting, with the preparation of the
instruments; then the set's authoring and its runs.
SUPERSEDED (Hadi, 1 October 2026; recorded in T-G records 8): TODO-155 is ruled for now (T-G Q16: the walk stays without
a hypothesis) and the IR test-bed set on dock_loading is agreed (T-G Q16's block above, RULED). Next: the build step that
sorts the earlier analyses and tests under kitting and prepares the instruments for dock_loading; then the authoring of
the set, its expectations and its runs.
SUPERSEDED (records, 2 October 2026; T-G records 9): the sort, the instruments' preparation, office_break at 90 seconds,
the 54 scenarios, their expectations and the 54 runs are built and accepted, and the IR test-bed of stage 1 is closed
(STAGE 1, THE IR TEST-BED ON DOCK_LOADING BUILT, RUN AND ACCEPTED above). Next: the design of the MPB set with Hadi.
SUPERSEDED (Hadi, 2 October 2026; recorded in T-G records 10): the design of the MPB on dock_loading is ruled (THE MPB ON
DOCK_LOADING above, MPB-DL1 to MPB-DL6). Its three open points are answered: the setup with pallets already in the bays
(MPB-DL2); the robot's last task as a return, not taken (MPB-DL4); expected decisions when the human's sequence depends
on the robot (MPB-DL3). Next: the MPB set's scenarios, agreed with Hadi before they are authored.
SUPERSEDED (Hadi, 2 October 2026; recorded in T-G records 11): the dispositions on the flags are recorded and the MPB
set on dock_loading is agreed (THE MPB ON DOCK_LOADING above: MPB-DL7, DISPOSITIONS, THE SET; 13 scenarios, 52 runs).
Next: the build's plan (the two setups of kind 3, the scenarios, every duration and cut point derived from path lengths,
the per-room derivation that the geometry gives each declared case), approved by Hadi before the build.
SUPERSEDED (Hadi, 2 October 2026; recorded in T-G records 14): the build's plan was confirmed (DL-P1 to DL-P9), the
scope of stage 1's MPB reduced, and the MPB on dock_loading built and run (THE MPB ON DOCK_LOADING above, SCOPE REDUCED AND
THE MPB ON DOCK_LOADING RUN; 52 runs; the 40 with full expectations agree with the oracle). Next, as Hadi rules: the
close of stage 1 (handoff_T-G_stage1_MPB_onward.md, section 6).
SUPERSEDED (Hadi, 2 October 2026; recorded in T-G records 15): T-G stage 1 is closed (T-G STAGE 1 CLOSED above). Next:
to be named by Hadi.
