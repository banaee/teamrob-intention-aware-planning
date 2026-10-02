# Record of planning and building: T-G, the second domain: rulings outside the shared core (A1, A10, A11; part B; part C)

Moved verbatim from `docs/design_decisions.md` on 2 October 2026 (Hadi's ruling of that day: one record file per task;
the conceptual design stays in design_decisions.md). Each block is headed by the title of the entry it comes from
and its id; in design_decisions.md an index line with the same id stands where the block was.

**T-G: the second domain's rulings (ruled by Hadi, 30 September and 1 October 2026)** — RECORD [T-G/1], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
- A1, V1 and FW.
  V1 is the first complete version of the framework, the package for TeamRob and the publications. In V1: T-G; T-F; T-V
  track 1 and track 2; the T-D tail's track 3b (TODO-145); track 4 in the reduced form of A8. FW (future work: not
  designed, ruled or built within V1): the 4D detour; T-S; the directions of A10.
  Tags. Each open TODO may carry a tag beside its status: [V1] or [FW]. A TODO keeps its number and identifier for good:
  no renumbering, no renaming. An untagged TODO is not yet ruled. There is no full pass now: a TODO gets its tag when it
  is next touched, by Hadi's ruling; a new item gets its tag when recorded.
  [FW] is for conceptual, higher-level directions only. An alternative not taken in a design question is recorded inside
  that question's ruling as "not taken", with its reason, and gets no FW item. FW must not hide a known wrong behaviour
  inside what V1 claims: such an item is fixed in V1 or stated as a limitation.

**T-G: the second domain's rulings (ruled by Hadi, 30 September and 1 October 2026)** — RECORD [T-G/2], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
- A10, FW directions (conceptual; each a TODO tagged [FW], or a tag on an existing item):
  - shared work between the human and the robot: TODO-147;
  - a human that chooses its own tasks (a human planner in place of the author's priority list): TODO-148;
  - the robot modelling a human who waits for the robot's own action (Q3's alternative M3): TODO-149;
  - several observed humans (`docs/assumptions.md` 5.2 allows one): TODO-150;
  - a container divided into positions, the position chosen when an object is put down: the [FW] tag on LIMIT-04, no new
    item;
  - communication acts stay under the existing records (T-D X5, TODO-96): the human assigning or changing a delivery
    location during the run; the robot informing a third party;
  - under T-V track 2 (roadmap, T-V): an interruption of a busy human caused by a world fact, if wanted, is designed there
    as the same entry point as the live user's click.

- A11, a note for T-F (TODO-144): a layout authored so that routes cross shows that the robot adapts when an interaction
  exists; it does not show how often interactions occur. T-F varies the placement and takes no interaction rate from
  crossing setups alone.

**T-G: the second domain's rulings (ruled by Hadi, 30 September and 1 October 2026)** — RECORD [T-G/3], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
PART B. DOCK_LOADING RULINGS (the domain only; nothing here enters `shared/` or `world/`)

- B1, the domain's reading. The robot replaces the driver: an automated forklift whose assigned tasks are to deliver full
  pallets from the truck to their containers and to return empty pallets to the truck. The truck stays parked for the
  whole run and is a container. The observed human is the warehouse staff member who receives the delivery. The human's
  assigned scans follow from the robot's assigned deliveries and are known at load.
  It corrects the roadmap's T-G entry and `docs/handoffs/handoff_T-G_onward.md` (§4, §5): "a driver unloading pallets"
  and "the driver's work order" are wrong under this reading; the foreseeable candidates recorded there (the phone call,
  talking to the dock worker) belong to the driver's role, which the robot holds, and do not apply to the observed human;
  "work order" was superseded by "assigned tasks" at T-H.
- B2, Q1 in dock_loading: `confirm_delivered_pallet` states its condition in the task model: the pallet is in its
  delivery container. (It answers LIMIT-02, TODO-10 and DESIGN-04 with A3.)
- B3, Q4 (D1): "In V1, each object's destination is explicitly designated in the setup. The resolved fact is
  destination_of(object, target), which the mind reads." The form of "An item's destination table is a fact of the
  station" (T-B1a, amended by T-L). Not taken: a setup rule from an object's property to a target (an authoring
  convenience, no component reasons with it); a destination decided at run time by the human.
- B4, Q5 (E2): "A pallet has one type, pallet, and its full/empty condition is represented by the state fact
  is_empty(pallet). Methods use that fact to determine which tasks are executable. In V1 the state remains constant
  during a run; actions that change it are future work." Not taken: two object types; one task for both movements.
- B5, Q6: the gate and the office door each have the state open or closed, declared in the setup. No action closes them
  in V1.
  - The gate, opened on request: the robot moves to the closed gate and honks; the honk is an action of the robot that
    sets the fact "opening requested". The human has the assigned task "open the gate", applicable when the gate is
    closed and the opening is requested: walk to the gate's button, press it. The button is a fixed object on the wall
    beside the gate, away from the passage. The robot's deliveries require the open gate; until then the robot has no
    applicable task and stands. The human is not interrupted and takes the task the next time it is free. Because the
    task is assigned, the robot knows it through the prior, and it is a live hypothesis after the honk. No information
    is exchanged. No deadline.
  - The office door: the agent that passes it opens it; the affected task has one method for the open state and one that
    opens first.
  This supersedes TODO-08 for the gate and answers LIMIT-03 (with them TODO-02, BUG-04 and DESIGN-15's point 2). Not
  taken: neither a state; constant states without an action; the robot opening the gate itself.
- B6, Q7 (F2): two foreseeable tasks, `coffee_break` and `office_break`. `office_break` ends at its chair with a wait,
  and the chair stands inside the office. Until track 4 is built the office is observed. (It answers DESIGN-15's point
  3.) Not taken: a third foreseeable task of the same structure (standing with a colleague); a variant in which the human
  scans all pallets only after every delivery; recognizing which variant of a task a human follows.
  ADDED (Hadi, 1 October 2026; T-G records 8): `office_break` lasts 90 seconds; `coffee_break` stays 60 (TODO-157,
  closed as ruled; the value is changed in the next build step). Reason: a long absence lets pallets accumulate in a bay,
  which gives two scans possible at once and the robot arriving at an occupied bay; it differs clearly from the coffee
  break. "T-G: the second domain's rulings", T-G Q16's block (RULED, T-G records 8).
  CORRECTED (records, 2 October 2026; T-G records 9): one tick is 2 seconds (PT60S is 30 ticks), so office_break's wait is
  45 ticks, and the human's absence is about 110 ticks (in the IR test-bed's C6 on env_layout_02, from leaving the dry
  bay at 30 to the arrival at the frozen bay at 141), a little more than one round trip of the robot (about 96 ticks,
  B14's note). Whether the absence is long enough for pallets to accumulate in a bay is reviewed with the MPB's design.
  REVIEWED (Hadi, 2 October 2026; T-G records 10; THE MPB ON DOCK_LOADING, MPB-DL5): office_break stays at 90 seconds
  for the MPB. Reason: no value is changed for a test set.
- B7, Q8 (H2'): `store_pallet(?pallet)`, a work task of the human: it takes a delivered and scanned pallet from its
  delivery container to its onward container. Condition: the pallet is in its delivery container and is scanned, so the
  order per pallet is delivered, scanned, stored. Each full pallet has a second designation in the setup, its onward
  container. The human carries a pallet as the kitting human carries an item; no tool in V1. The human is never assigned
  `deliver_pallet` or `load_return` in V1. Not taken: the human delivering its own pallets from the truck (kitting's
  pattern).
- B8, Q8b (K1): kitting's rule for a held object, unchanged. Hadi's wording: "When an agent starts a new task while
  carrying an object, the carried object determines the applicable method. Continue with it if it is the new task's
  object; otherwise return it to its recorded origin before starting the new task." It applies to `deliver_pallet`,
  `load_return` and `store_pallet`. The origin is where the pallet was picked up: the truck, the empties area, the
  delivery container.
- B9, Q9a (S2): a container is one point, the centre of the container, with no constraint, and it may hold several
  pallets (as kitting's table does). Not taken: authored pallet places; a position chosen when the pallet is put down
  (FW on LIMIT-04, A10). Pallets drawn on top of each other are a drawing matter for T-V.
  NOTE (records, 2 October 2026; T-G records 9; the IR test-bed on dock_loading), a property of "one point per
  container", not a ruling: two pallets in one container stand on one point, so the second scan has no walk (its
  move_to is acknowledged at once: C3, three stretches of 3 ticks that never reach the threshold), and no walk between
  the two exists that an event could cut (the set's M3 as written was not buildable; Hadi approved scan 2 in its
  place). LIMIT-04's FW direction (a position chosen when a pallet is put down) is the alternative.
- B10, Q9b, the room. Requirements (Hadi): goods flow forward (truck, delivery container, store) and never travel away
  from their store and back; the freezer lies near the dock; no bay stands in front of a store entrance; one place for
  empties that both stores can bring to. Arrangement: the delivery bays in a row on one side wall, the frozen bay nearest
  the gate; the freezer and the dry store on the opposite wall, the freezer nearest the gate; the empties in the top
  corner on the bay side; the office at the top centre. The coffee machine, the gate's button, the desk, the standby
  place and the landmarks are placed when the layout is drawn.
  Artefact constraint: by the setup's designations, the human's carrying route crosses or approaches a normal robot route
  in some setups and stays clear in others; the V1 scenarios include both.
  Catch-up requirements: every fixed object inside the space; the zones leave the layout and areas are declared (A9);
  landmarks for the exit walk; the revised room is a new layout and a new setup with the next serial ids; the present ones
  (env_layout_01, env_setup_01) stay for the viewing fixture.
  READS (B13, T-G records 2, 1 October 2026): "landmarks for the exit walk" reads: the desk landmark, which enters stage
  1's layout.
  MOVED TO STAGE 2 (Hadi and the design chat, 1 October 2026; recorded in T-G records 5); B14: the arrangement above (the freezer and the dry store on the opposite wall) is stage
  2's room, with its own layout, setup and scenarios; it is unchanged and can be revised when stage 2's layout is agreed.
  Reason: that arrangement serves `store_pallet`, which stage 1 does not have. Stage 1 uses the three rooms of B14.
  "The present ones (env_layout_01, env_setup_01) stay for the viewing fixture" is superseded: they are removed with
  their three scenarios, and the viewing fixtures of B14 replace build 1's. The other catch-up requirements hold for
  B14's rooms (every fixed object inside the space; the areas declared; the desk landmark).
- B11, Q11 (P2) in dock_loading: passing the gate is a plain step "move to the gate", whose target is the gate's centre
  point; no special action. The domain has three areas, divided by the gate and by the office door: the truck side (the
  truck and the dock platform, outside the gate), the hall, and the office (A9; names settled with stage 1's layout; the
  six zones of env_layout_01 are replaced). Each task has one method per starting area, selected by the condition on the agent's area. A
  method that crosses the gate keeps the condition that the gate is open. "Return the held pallet to its origin" may be a
  sub-task used as the first step. Not taken: always going by the gate; a sub-task with conditions for a later passage
  (A9's property defeats it); routing through openings as a property of movement (it changes the projection and the
  recognizer in `shared/`). Within V1 this is dock_loading's answer to TODO-09.
  AMENDED (Hadi, 1 October 2026, T-G stage 1's plan approved, answer 6; recorded in T-G records 7): "Each task has one
  method per starting area" reads: a task has a method for every area its agent can be in, not for every area. The
  robot can be on the truck side and in the hall; the human in the hall and in the office. With B8's four held-object
  cases (held, another empty pallet held, another full pallet held, nothing held) a robot task has 8 methods. An agent
  in another area is a defect: no method covers it, the absence of a method is the check, and no mechanism is added
  (for the robot the run stops, TODO-152). B11's optional sub-task for the return is not used: a sub-task schema must be
  in the robot's task model, and the hypothesis space is built from every schema there, so it would become a hypothesis
  about the human. The methods: `docs/handoffs/plan_T-G_stage1.md`, section 4.
- B12, further rulings on the domain's scope.
  - Check-in and check-out [V1], stage 3: separate from the gate mechanism and independent of it. A desk with a computer
    beside the gate's button is the human's place; the robot's place is a point just inside the gate, more than the
    minimum separation away. Check-in: the two agents exchange the list of deliveries at the start. Check-out: the human
    signs at the end to confirm that everything is delivered. Design open until stage 3, including what "exchanging the
    list" means when the robot holds the designations from the start.
    AMENDED (B13, T-G records 2, 1 October 2026): the desk enters stage 1's layout, as the target of the closing part;
    check-in and check-out stay in stage 3 and will use this desk.

**T-G: the second domain's rulings (ruled by Hadi, 30 September and 1 October 2026)** — RECORD [T-G/4], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
  - A deadline on the robot's waiting: the default is that the robot waits without limit. Optional in stage 3; not
    planned.
  - A pallet that blocks another in the truck: an optional sub-task in stage 3, if time in V1 allows.
  - Not taken: an action of unknown length inside a plan; a fixed order among the robot's tasks as its own mechanism
    (conditions cover it; deliveries and returns may be intertwined); the robot moving to wherever the human is (the
    target would be an agent, arrival contradicts `min_separation`, the prediction becomes circular); a check-in that is
    a meeting with no content.
- B13, the closing part in dock_loading (the domain side of T-G Q14; Hadi, 1 October 2026; recorded in T-G records 2).
  Stage 1's closing part is one entry: go to the desk. The desk is a landmark inside the hall, at the wall on the gate's
  side, beside the place of the gate's button. It enters stage 1's layout.
  The desk lies more than the minimum separation from the robot's routes through the gate. Reason: the robot still passes
  the gate after the human's list is finished, and the human then stands at the desk.
  No exit from the room is defined for dock_loading now. Check-in and check-out stay in stage 3 and will use this desk
  (B12).
  `docs/assumptions.md` 1.1 (a script ends with the human leaving the workspace) reads for dock_loading: the script ends
  with the walk to the desk. B10's "landmarks for the exit walk" reads: the desk landmark. Kitting is unchanged. T-F's
  scope line on the exit walk (TODO-144) is a kitting statement; dock_loading's ending is for T-F's own design.
  NOTE (T-G records 3, 1 October 2026; not a ruling): the desk is a landmark in stage 1, so no task of the robot's task
  model names it and the robot's mind holds no hypothesis for the walk to the desk, as for kitting's exit walk. Whether
  the desk becomes a fixed object is stage 3's question.
- B14, stage 1's rooms and setups (Hadi and the design chat, 1 October 2026; recorded in T-G records 5).
  Rooms. Stage 1 uses three rooms, env_layout_02, env_layout_03 and env_layout_04, derived from the present room. The old
  env_layout_01, env_setup_01 and the three scenarios on it are removed; the viewing fixture of build 1 is replaced by the
  fixtures written with these rooms. The room of B10 (the freezer and the dry store on the opposite wall) moves to stage 2
  (B10's note). More rooms and setups may be added in stage 1 later.
  Identical in the three rooms (centres in cm; origin and axes as before): the hall, x from -600 to 600, y from -300 to
  300; the office, x from -170 to 170, y from 300 to 415; the office door (0, 300); the chair (130, 365), inside the
  office; the gate (0, -300), width 300; the truck (0, -590), 250 by 300; the dock platform as before; the desk, a
  landmark, (300, -260); the standby place, a landmark, (0, 0); the delivery bays and the empties container 170 by 170;
  the coffee machine 50 by 50. The declared space contains every fixed object, the truck included.
  Differing:
  - env_layout_02: dry delivery bay (-515, 215); frozen delivery bay (515, 215); empties (-515, -35); coffee machine
    (505, 30).
  - env_layout_03: dry delivery bay (-515, 215); frozen delivery bay (515, 0); empties (-515, -35); coffee machine
    (-400, -230).
  - env_layout_04: dry delivery bay (-255, 215); frozen delivery bay (-515, -35); empties (515, -35); coffee machine
    (-400, -230).
  One container for empty pallets per room. The three areas (truck side, hall, office) are declared in each layout,
  written under the name the code has today (zones); stage 1's rename step converts them.
  Agents. The human starts at the standby place. IR test-bed: the robot stands idle on the gate's centre point (0, -300)
  for the whole run. MPB: the robot starts on the truck side. Stage 1 keeps full observation: the robot observes every
  area, the office included, wherever it stands. A8's rule on monitored areas is reopened at stage 2 (A8's note).
  Setups, two kinds per room (six files):
  - Kind 1, for the IR test-bed: two full unscanned pallets in the dry delivery bay and two in the frozen delivery bay,
    each designated to the bay it stands in; one full pallet in the truck, designated to the dry delivery bay; no empty
    pallets. Reason: one setup serves three cases by the scans a scenario assigns (one scan per bay; two scans in one
    bay, the same-motion case; the scan of the pallet in the truck, which never becomes applicable, so the human goes to
    the standby place).
  - Kind 2, for the MPB: four full pallets in the truck, two designated to each delivery bay; two empty pallets in the
    empties container. Reason: the robot's pool always holds a delivery to the other bay and a return.
  - RULED: the setup designates the truck as the destination of each empty pallet (the PROPOSAL of that name). Reason:
    one rule covers every pallet.
  - A third kind, all four full pallets designated to one bay, is added after the first MPB run if its results call for
    it.
    KEPT (Hadi, 2 October 2026; T-G records 10; THE MPB ON DOCK_LOADING, MPB-DL2): the condition stands. A new kind for
    the MPB's controlled scenarios is ruled there (one full pallet already in each delivery bay); the names of the kinds
    are not ruled.
    READS (Hadi, 2 October 2026; T-G records 11; THE MPB ON DOCK_LOADING, DISPOSITIONS, D7): "a third kind" reads "kind 4"
    ("one bay"). Kind 3, "pallets in the bays", is MPB-DL2's (two full pallets in each delivery bay, as amended).
  Staging: a milestone in stage 1's build, before the IR test-bed: one simple scenario per room runs from start to end.
  Stage 1's "before the plan" points on the layout and the setup (C1's "before each stage's plan the design chat and
  Hadi agree the layout and the setup") are closed by this entry for stage 1.
  ANSWERS (Hadi, 1 October 2026, on the B14 build's flags; recorded in T-G records 6):
  - The six setups stay as written, though pairwise identical in content across the rooms. Merging identical setups
    belongs to the held refactor of scenarios and layouts, not to this stage.
  - Accepted as built (cec8cc3): the MPB robot's start point (0, -370), on the dock platform; the ids
    `empty_pallet_bay_0`, `desk`, `standby_place`; the area names `zone_hall`, `zone_office`, `zone_truck_side`.
  - A pallet's `subtype` stays out of the setups. Reason: destinations are by designation.
  - The pictures of the old room are kept, renamed with the suffix `_original` (C3's note).
  NOTES (the same answers; facts, not rulings):
  - An agent stops 10 to 30 cm before a target point (a walk steps 20 cm toward the centre and completes once
    `at(agent, object)` holds); the proximity threshold is 30 cm (`PROXIMITY_THRESHOLD`).
  - The scan and the next delivery to the same bay share one point (the bay's centre, B9), so with a minimum separation
    of 50 cm that conflict is certain whenever both concern the same bay. This is the expected main interaction of stage
    1, not a defect.
    CORRECTED (records, 1 October 2026; STAGE 1, THE SECOND MILESTONE SCENARIO BUILT): the conflict requires, in
    addition, that the human is still at the bay when the robot arrives. In stage 1's rooms a round trip to the truck
    takes about 96 ticks and a scan from the standby place 16 to 30, so the human finishes before the next pallet
    arrives, and the second milestone scenario did not reach it.

PART C. STAGING AND THE DOMAIN'S PRESENT STATE (statements, not design rulings)

- C1, the stages of T-G (all in V1). Before each stage's plan the design chat and Hadi agree the layout and the setup for
  that stage.
  - Stage 1, the basic domain: the robot delivers and returns (B11); the human scans, takes the two breaks, steps aside to
    the standby place; the gate is declared open; the office door has no state yet. The IR test-bed, then the MPB.
  - Stage 2: `store_pallet` (B7); the gate opened on request (B5); the office door's state (B5); after the MPB's first
    run, TODO-16 with the stepwise delivery (A7).
  - After stage 2: track 4 (A8).
  - Stage 3: check-in and check-out (B12), with the two optional items.
  STAGE 1.5 (Hadi, 1 October 2026; T-G records 2): context knowledge, framework-wide, after stage 1's close and before
  stage 2. The order is stage 1, stage 1.5, stage 2, track 4, stage 3. Stage 1.5 starts from its own handoff.
  Its content (its design opens at its stage; nothing is ruled yet): a context timeline in the scenario that changes a
  fact at an authored point of a run, applied by the environment; both domains' foreseeable tasks conditioned on such
  facts. Open questions recorded for it:
  - the form of a context fact;
  - whether the human only starts a task on it or a task in progress is interrupted (A3's "never interrupted" and A10's
    line on an interruption caused by a fact);
  - liveness under A4 when a condition turns false while the human still executes the task ("applicable to start"
    against "valid to continue");
  - the prior under context;
  - the perception assumption for context facts.
  The pre-loaded context stream moves from T-V track 2 to stage 1.5. T-V track 2 keeps the live events.
  ADDED (Hadi, 1 October 2026; T-G records 8; T-G Q16's block below, RULED), NOT RULED: one design question for stage
  1.5, what sets a hypothesis's share at the start of an episode. Four determinants are recorded for it: the assignment
  (exists); context facts; the task that just ended (a transition prior between tasks, Hadi's idea); an enabling event,
  such as the robot's own delivery (TODO-154). They are designed as one mechanism. Also Hadi's ideas for stage 1.5, NOT
  RULED: the duration of a foreseeable task is not one fixed number; temporal context can be a fuzzy set with a degree
  of membership.
  A requirement on stage 1's plan (the same ruling): the form built for A5 admits a fact that no action changes and that
  is not the state of a movable object. Reason: context knowledge then needs no second mechanism. Stage 1 authors no such
  fact.
  WHERE EACH RULING IS FIRST BUILT (Hadi, 1 October 2026, T-G records 1, continued). Content only; the order inside a
  stage is for that stage's plan.
  - Stage 1, the basic domain:
    - first, in its own commit with no change of behaviour: the zone mechanism renamed to "area" in the code (A2's
      ruling of 1 October 2026; the plan reports the extent first). This is the one rename in V1; A2's "no code is
      renamed" concerns the terms it introduces;
    - the catch-up of dock_loading's forms to kitting's (C3);
    - A3, the human's script form (`world/`), with the standby entry, once the entry lifecycle is ruled (A3, PARKED);
      RULED (1 October 2026): the lifecycle is A3's Q12 to Q15, with the closing part; dock_loading's closing part, the
      walk to the desk, and the desk landmark (B13);
    - A4, liveness by applicability (`shared/`);
    - A5, generic object states and designations, used here for the scanned state, `is_empty` and the destination;
    - A6, the perception assumption;
    - A9, the declared areas and the fact that an agent is in an area (the mechanism exists under the code name "zone":
      renamed by the first step, not built anew; dock_loading's three areas declared in stage 1's layout);
    - B1 to B4, B8, B9, B11;
    - B6, with `office_break` in a reduced form: the office door has no state yet, and the human passes it as a plain
      point on the way; the office is observed;
    - B10, the room; whether the stores and the freezer are already present in stage 1's layout is not ruled
      (PROPOSALS);
      SUPERSEDED (Hadi and the design chat, 1 October 2026; recorded in T-G records 5): stage 1 builds B14's three rooms and six setups; B10's room is stage 2's; the proposal is
      closed as not taken;
    - the IR test-bed on dock_loading, then the MPB.
    - ADDED (Hadi and the design chat, 1 October 2026; recorded in T-G records 5): before the IR test-bed, a milestone: one simple scenario per room of B14 runs from start to end;

**T-G: the second domain's rulings (ruled by Hadi, 30 September and 1 October 2026)** — RECORD [T-G/5], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
    A3, A4, A5 and A9 each change code outside the domain, and each carries its acceptance check on kitting: the
    maintained sets stay byte-identical.
    BUILT (1 October 2026): the rename, A9 with R2, A4, A5 and A3 (stage 1, steps 1 to 5). "T-G: the second domain's rulings", STAGE 1, STEPS 0 TO 5 BUILT.
    BUILT (1 October 2026): dock_loading's catch-up, its content and the milestone (stage 1, steps 6 to 8; the
    milestone's acceptance held in all three rooms). ADDED (Hadi, 1 October 2026): before the IR test-bed, a second
    simple scenario per room, then the sorting of the earlier analyses and tests under kitting with the preparation of
    the instruments. "T-G: the second domain's rulings", STAGE 1, STEPS 6 TO 8 BUILT.
  - Stage 2:
    - B7, `store_pallet`, with the second designation (the onward container);
    - ADDED (Hadi and the design chat, 1 October 2026; recorded in T-G records 5): B10's room (the freezer and the dry store on the opposite wall), with its own layout, setup and
      scenarios;
    - ADDED (the same): A8's rule on monitored areas reopened (A8's note); its build inside stage 2 or its own
      increment, decided then;
    - B5, the gate opened on request, and the office door's state;
    - A7, TODO-16, after the MPB's first run on dock_loading.
  - After stage 2: A8, track 4.
  - Stage 3: B12, check-in and check-out, with its two optional items.
  ADDED (T-G records 2, 1 October 2026): stage 1.5, between stage 1 and stage 2 (before track 4): context knowledge
  (STAGE 1.5 above); nothing in it is ruled yet.
  Rulings with no stage, because nothing is built for them: A1 (V1, FW and the tags: a records rule), A2 (terms; no code
  is renamed), A10 (FW directions, outside V1), A11 (a note for T-F), and B12's items "not taken". A6 is an assumption,
  recorded in `docs/assumptions.md` 5.3; stage 1 is where the robot first reads object states through it.
- C2, build 1 (30 September 2026; 56e674e, 6e29c15, 62ebc4e): the form-only repairs (the steps of `pick_up`, `place` and
  `scan_it` bind `?item`; `confirm_delivered_pallet` typed; the layout's `office_chair` typed `office_chair`; the robots'
  tasks in `assigned_tasks`) and scenario_s01_03, a viewing fixture that loads and initialises. scenario_s01_01 and
  scenario_s01_02 still fail at load by intent (`infeasible:office_break(...)` in the load-time replay: the door
  condition). Re-measured at 62ebc4e (1 October 2026): as stated.
  SUPERSEDED (Hadi and the design chat, 1 October 2026; recorded in T-G records 5); B14: env_layout_01, env_setup_01 and scenario_s01_01 to _03 are removed; B14's viewing fixtures
  replace scenario_s01_03.
- C3, the state of `domains/dock_loading/` after build 1 (the survey of 30 September; each line verified against the code
  at 62ebc4e, 1 October 2026). Stage 1's plan starts from this list.
  NOTE (Hadi and the design chat, 1 October 2026; recorded in T-G records 5): the lines on env_layout_01, env_setup_01 and their scenarios (the truck outside the space, the office
  chair in the hall, no landmarks, no assigned tasks for the human) describe artefacts B14 removes; B14's rooms have every
  fixed object inside the space, the chair inside the office and the two landmarks. The rest of the list stands.
  Still not in kitting's current form:
  - no `HumanOnlyTask` (`go_to`, `stand`, `go_to_and_stand`) and no `stand` action; no `script.py` with the call forms;
    the scenarios use raw `TaskInstance`s;
  - `pick_up` and `place` lack the successor-state declarations of T-B2a (`moved_object_key`, `moved_to_key`); `place`
    still has the effect `not_holding` instead of a retraction of `holding`;
  - `wait_at` completes on `ProcessCompletion`, not on the fact `waited`;
  - no landmarks; no exit walk; no purpose statement in the scenarios;
  - the layout has a `zones` block and a `zone` field per object (kitting's layouts too: A2);
  - stale docstrings in `tasks.py` (`?dest`, two gate methods per task, "Human assigned" / "Human foreseeable", no
    `office_break`) and `scenarios/scenarios_s01.py` ("scenario ids keep their old form until stage 3"); layout pictures
    inside the domain folder under an old id (`env_layout1.svg`, `env_layout1_present.svg`, `env_layout1_present.png`,
    `env_layout_original.jpg`; kitting keeps its pictures in `docs/env_layouts_png/`).
    NOTE (Hadi, 1 October 2026, on the B14 build's flags; recorded in T-G records 6): these pictures show the removed env_layout_01. They are kept, renamed with the suffix `_original`
    (`env_layout1_original.svg`, `env_layout1_present_original.svg`, `env_layout1_present_original.png`);
    `env_layout_original.jpg` keeps its name.
  Content that the rulings of part B replace:
  - `deliver_pallet` has a free `?delivery_bay` and one method (B3, B8, B11); `load_return` ranges over every pallet
    (B4); `confirm_delivered_pallet` has no condition (B2); `office_break` has a door condition no fact satisfies and ends
    with a walk to the gate (B5, B6); the human has no assigned tasks in scenario_s01_01 and scenario_s01_02 (B1);
  - the truck extends 40 cm outside the space (to y = −740; the space's y runs from −700); the office chair stands in the
    hall (its declared zone is `zone_hall_center`), 30 cm from the coffee machine (B10).
  In the simulator, written for this domain (A5 replaces them):
  - `mesa_sim/world_state_builder.py` emits `gate_is_open` for every object of type `gate` whose `is_open` is not False,
    and `is_open` is never loaded (always None); nothing emits a door fact;
  - the fields `is_empty`, `is_scanned`, `is_open` on `SimObject`, the `scanned` fact, and the touch handler reading the
    literal `"?item"` (`mesa_sim/action_decomposer.py`; the grasp handler, kitting's too, reads the same literal);
  - `mesa_sim/list_scenarios.py` lists kitting only; `SimModel.get_movable_objects` filters the type `"item"` and nothing
    reads it.
  In the viewer (for T-V, or the stage that first needs it): the colour table's keys (`delivery_area`, `empty_bay`) do
  not match the layout's types (`delivery_bay`, `empty_pallet_bay`; `office_chair` absent); the axis range clips what
  lies outside the space; the label offset is keyed on the type `"shelf"`.
  `domains/README.md` is stale throughout: rewritten with stage 1's build (REFACTOR-03).
- C4, points for the stage plans (not rulings; each returns to the design chat only if it produces a finding):
  - the load-time check for a script that depends on the robot, and the meaning of the outcome "infeasible" under A3;
    RULED (Hadi, 1 October 2026): A3, Q13b (and Q13a for an entry that ends INFEASIBLE);
  - how "completed" is judged for an entry of the human's list (the standby entry must be takable again after the human
    has left the place). PARKED (Hadi, 1 October 2026) as the first design question of the next design chat, the
    lifecycle of an entry: A3's PARKED block; A3 is not built before it is ruled. The byte-identical acceptance does not
    exercise the rule (no maintained kitting set has a dropped task): the ruled rule is also checked on the kitting
    scenarios with a drop event and on the test-bed sets with misdeliveries;
    RULED (Hadi, 1 October 2026): A3, Q12; the added check is A3's ACCEPTANCE;
  - where the exit walk stands relative to the priority list (a plain walk is always applicable);
    RULED (Hadi, 1 October 2026): A3, Q14 (the closing part); dock_loading's, B13;
  - how an event or a foreseeable task is placed relative to tasks whose order is not fixed;
    RULED (Hadi, 1 October 2026): A3, Q15;
  - how a pallet's origin is recorded (B8);
    SETTLED (T-G stage 1's plan, approved by Hadi, 1 October 2026; recorded in T-G records 7): in stage 1 a pallet's
    origin is the setup's initial container (`home_container_of`), which is where every stage-1 pick-up happens; stage 2
    (`store_pallet` picks up from a delivery bay) needs the origin recorded at the pick-up;
  - how the meta-planner behaves when the pool holds tasks and none is applicable (TODO-30);
    CORRECTED (T-G records 7, 1 October 2026): the citation of TODO-30 is wrong; TODO-30 is closed and concerns
    realizability (F1), not applicability. FINDING (T-G stage 1's plan, approved by Hadi, 1 October 2026): a robot task
    with no applicable method raises `DecompositionError` out of `MetaPlanner.update()` (through `_is_complete`), which
    nothing catches, and the run stops. Stage 1 cannot reach it (a method for every area the robot can be in, the gate
    open). Stage 2 (the robot at a closed gate, B5) needs a ruling first. TODO-152;
  - the forms in the setup and the registry for object states and the two designations (A5);
  - the smallest set of methods under B11 with B8;
    SETTLED (the same approval): B11 as amended (answer 6): 8 methods per robot task, the human's methods for the hall
    and the office;
  - how the existing machinery behaves when the live set holds foreseeable tasks only, at the start of a run and between
    deliveries (TODO-143 stays parked: it concerns an empty assigned list, which is a different state);
    SETTLED (the same approval): the existing machinery, nothing new. With the prior on the live set is {coffee_break,
    office_break}; the human waits or walks to the standby place; both hypotheses become inadequate, the finding is
    unexplained, admission refuses and the robot realizes against the fallback projection, as for kitting's exit walk.
    An empty live set is not reached with the prior on while the human is in an area; otherwise exhausted, below theta,
    the fallback;
  - for the IR test-bed on dock_loading the robot is idle, so its setup places the pallets in their delivery containers
    from the start.
  - ADDED (Hadi, 1 October 2026, on the B14 build's flags; recorded in T-G records 6): the rule for a point on the boundary of two areas, which today is decided by the order of
    declaration (`SimModel.get_zone_of_position`: inclusive bounds, the first declared zone wins); and, since an agent
    stops 10 to 30 cm before its target, the area an agent is in after "move to the gate" from each side, in the
    environment and in the computed state alike (R2);
    SETTLED (the same approval): the rule stays the order of declaration, stated in one shared function (`area_of`).
    NOTE (T-G stage 1, step 2 as built, 1 October 2026): that shared function is `area_at`; `area_of` is the planner's
    lookup for an object's area.
    An agent stops 10 to 30 cm short of the gate on its side of approach and stays in the area it came from; the
    projection's arrival point and the replay's walk end (where the body stops, answer 5) give the same area; only the
    centres of the gate and the office door lie on an edge;
  - ADDED (the same): the scanned state of an empty pallet (B14's setups leave it out; the form defaults it to false);
    SETTLED (the same approval): it does not hold (the form's default: a declared state not listed does not hold);
    nothing reads it with the prior on;
  - ADDED (the same): the stale references to removed dock_loading scenarios in `mesa_sim/run_mesa.py` (its docstring
    and commented-out imports name scenario_s01_01 and _02), corrected in stage 1's first build step.
  - ADDED (Hadi, 1 October 2026, on the T-G records 3 flags; recorded in T-G records 4), R2 (C1, stage 1): the agent's area in a computed state after a movement action, one
    definition shared with the environment's state construction; the plan names the shared representation, every
    consumer of a computed state that decomposes a later task, and the form.
- C5, to watch in the test-beds: hypotheses that predict the same motion divide the belief, so none passes the admission
  threshold (two unscanned pallets in one container). If the IR test-bed confirms it on dock_loading, it is a finding
  about the mind and returns to the design chat within V1.
  CONFIRMED (the IR test-bed on dock_loading, 1 to 2 October 2026; records 2 October 2026, T-G records 9): in C3 and on
  C4's first two walks, in all three rooms, two scans of one bay share the belief and neither reaches the threshold (9
  stretches; none admitted). A finding about the mind, NOT RULED; it returns to the design chat. Linked to the recorded
  direction on acting on a set of hypotheses with the same projection: belief-aware planning, the covering set S_ε and
  one realization against its projections jointly (TODO-97). "T-G", STAGE 1, THE IR TEST-BED ON DOCK_LOADING BUILT.
- C6, open at their stage: the design of check-in and check-out; the design of TODO-16; how the MPB's oracle derives an
  expected decision when the human's sequence depends on the robot's decisions.
  ANSWERED FOR STAGE 1 (Hadi, 2 October 2026; T-G records 10): the third clause, by THE MPB ON DOCK_LOADING, MPB-DL3.
  The first two clauses stay open at their stages.
