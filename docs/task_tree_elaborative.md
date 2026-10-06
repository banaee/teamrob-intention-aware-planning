# Task tree

The status of every task of "The plan from T-A", its parts and their sub-tasks, as the records state them. This
document reports the records. It decides nothing and changes no record. Where two sources disagree on a status, both
are shown with their sources; the disagreement is not resolved here.

- Date: 6 October 2026.
- Commit read: `be3c200` on `main` ("T-viz 1a: Hadi's review of increment (i) recorded; the plan amended"). Each source
  was read once, from one copy taken at 20:14.
- Working tree when read: no tracked source file modified. One untracked file among the sources:
  `docs/handoffs/build_T-viz_1a_state.md` (the state file of the session that builds T-viz 1a's increments (ii) and
  (iii)). It was read; where it differs from the committed records, the node says so.
- Sources: `docs/roadmap.md`, "The plan from T-A" (the order block, V1 AND FW, the task bullets); `docs/design_records.md`;
  `docs/design_decisions.md`; `docs/TODOS_AND_DEFERRED.md`; the current handoffs: `docs/handoffs/T-G_forward_inputs.md`
  (T-G and T-K), `docs/handoffs/handoff_T-viz.md` and `docs/handoffs/plan_T-viz_1a.md` (T-viz),
  `docs/handoffs/handoff_T-F_part1.md` (T-F), `docs/handoffs/handoff_T-H.md` (T-H); `docs/glossary.md` for the terms.
  No file named `SUPERSEDED_*` exists.
- Depth: level 1 the task; level 2 its parts as the records name them (stage, step, part, track); level 3 the
  sub-tasks of a part, only where the records define them. No TODOs, open questions or items below that.
- Legend (each word as its task's records use it): **done**, **closed**, **built**, **ongoing**, **asked for**,
  **paused**, **on hold**, **parked**, **stale**, **open**, **ruled**, **ruled in outline**, **not started**,
  **not scheduled**, **superseded**, **carried out as T-viz**, **V1** (in the first complete version), **FW** (future
  work). T-viz nodes use T-viz's own words: **done**, **built**, **open**, **preferred**, **proposed by ccode**.
  **▶ NOW** marks what the roadmap states as running now; **⏭ NEXT** what it states as next.

## The order, as the roadmap states it

Source: roadmap.md, The plan from T-A, the order block (THE PRESENT ORDER of 3 October 2026 and its dated lines of 5
and 6 October 2026), and V1 AND FW.

1. Done: T-A, T-B, T-C, T-H, T-L.
2. T-D: closed except its tail.
3. T-G's stage 1: closed; T-G paused.
4. T-K part 1: "Now" in THE PRESENT ORDER (3 October 2026).
5. T-F part 1: taken while T-K part 1's steps 6 and 7 were on hold, then closed (5 October 2026).
6. T-viz stage 0: done (6 October 2026). **▶ NOW: T-viz stage 1a**, asked for (6 October 2026).
7. **⏭ NEXT**: "T-G's next stage with T-K part 1's steps on dock_loading" (the CLOSED line of 5 October 2026).
   Disagreement: design_records.md, T-K, STEP 6, DONE records step 6 (dock_loading) as done and states "Next: Hadi's
   confirmation of the provisional decisions; step 7 (the close of T-K part 1)".
8. Then: T-G's stage 2, track 4 (its reduced form) and T-G's stage 3; T-F; T-V, which reads "T-viz stage 1" in T-V's
   place (proposed by ccode; the place is open); track 3b; T-K part 2 at the end of the V1 queue.
9. FW: the 4D detour, T-S, T-K's later directions; T-viz stages 2 and 3 (preferred, for now).

The roadmap's "Now: T-K part 1" (3 October 2026) and its later dated lines ("T-viz stage 0 starts now", then "ASKED
FOR: T-viz stage 1a") are both in the order block; the later lines are newer.

## T-A — Records

**done** (roadmap.md, The plan from T-A, the order block, "Done"; the T-A bullet).

## T-B — B3.B (`full_reorder`): a candidate is an ordering of the pool

**done** (roadmap.md, The plan from T-A, the order block, "Done"; the T-B bullet: T-B1 complete, T-B2a to T-B2d and T-B3
✅).

## T-C — The human action script

**closed** (roadmap.md, The plan from T-A, the T-C bullet: "T-C closed"; the order block, "Done").

## T-H — The human behaviour model

**closed** (26 September 2026) (roadmap.md, The plan from T-A, the T-H bullet: CLOSED; handoff_T-H.md, "Close-out (26
September 2026): T-H is closed").

## T-L — Layouts, setups and scenarios: the three artefacts of a run

**built** (26 September 2026, stages 1 to 4); **done** in the order block (roadmap.md, The plan from T-A, the T-L
bullet: BUILT; the order block, "Done").

## T-D — Robustness in kitting

**closed except its tail** (30 September 2026) (roadmap.md, The plan from T-A, the order block, item (1) and THE
PRESENT ORDER; the T-D bullet: CLOSED EXCEPT ITS TAIL). The T-D tail is track 3b, track 4 and the 4D detour strategy
(glossary.md §8, **T-D tail**, as amended).

- **Tracks 1 (the IRB), L, P, 2.5, G, X and 3 (the MPB)**: **done**; the MPB **closed** at its close-out (30 September
  2026) (roadmap.md, The plan from T-A, the order block, item (1); the T-D bullet).
- **Track 3b, consequential activation under conflict** (T-D tail): **V1**; **open**; after T-V (roadmap.md, The plan
  from T-A, the T-D bullet: "Track 3b stays after T-V, in V1"; the order block, THE PRESENT ORDER; TODOS_AND_DEFERRED.md,
  TODO-145: [OPEN] [V1], PLACEMENT REVISED). Its place against T-V's split into T-viz stages 1 and 3 is open
  (TODOS_AND_DEFERRED.md, TODO-190, point 3).
- **Track 4, the workspace boundary and departure** (T-D tail): moved into T-G, after T-G's stage 2, in its reduced
  form; **V1** (roadmap.md, The plan from T-A, the T-D bullet, SUPERSEDED IN PART (T-G A1, A8); the T-G bullet, "After
  stage 2"; TODOS_AND_DEFERRED.md, TODO-140: [OPEN] [V1, reduced form]). Shown under T-G.
- **The 4D detour strategy** (T-D tail; Phase 4D): **FW** (1 October 2026) (roadmap.md, The plan from T-A, the T-D
  bullet, SUPERSEDED IN PART; roadmap.md, Phase 4D, "1 October 2026: both are FW"; glossary.md §8, **T-D tail**).

## T-G — The second domain in Mesa: dock_loading

**open**; **paused** after its stage 1; it resumes at its stage 2 when T-K part 1 is closed; all stages **V1**
(roadmap.md, The plan from T-A, the T-G bullet, "Paused after stage 1"; T-G_forward_inputs.md, section 2;
design_records.md, T-G, PART C, C1 and its T-K PART 1 line).

- **Stage 1, the basic domain**: **closed** (2 October 2026) (roadmap.md, The plan from T-A, the T-G bullet, CLOSED, T-G
  STAGE 1; design_records.md, T-G stage 1, T-G STAGE 1 CLOSED). Its IRB and MPB outputs: **stale** since the gate
  rulings, until T-K part 1's step on dock_loading (design_records.md, T-K, THE CROSS-CHECK, RULED, AM57;
  design_records.md, T-F part 1, THE MEASUREMENT, O as corrected; T-G_forward_inputs.md, section 12). Stage 1 is
  measured again in full by T-K part 1's step 6 (done, 6 October 2026); the old reports stay, marked stale
  (design_records.md, T-K, STEP 6 NAMED AND RULED and STEP 6, DONE).
- **Stage 2, the full domain** (`store_pallet`, the gate opened on request, the office door's state, A7): its content
  **ruled**; points to rule before its build **open**; T-G resumes here when T-K part 1 is closed; **⏭ NEXT** in the
  roadmap's line of 5 October 2026 (T-G_forward_inputs.md, section 6: "[ruled unless marked]", "To rule before the build
  [open]"; roadmap.md, The plan from T-A, the T-G bullet, Stage 2 and "Paused after stage 1"; the order block, the
  CLOSED line of 5 October 2026). No record states "not started" for it.
- **Track 4, the human outside the monitored areas** (reduced form): after stage 2; **V1**; **ruled**, with the
  observation rule reopened (roadmap.md, The plan from T-A, the T-G bullet, "After stage 2"; T-G_forward_inputs.md,
  section 7: "[ruled, with the observation rule reopened]"; TODOS_AND_DEFERRED.md, TODO-140: [OPEN] [V1, reduced form]).
- **Stage 3, check-in and check-out**: **ruled in outline**, design **open** (T-G_forward_inputs.md, section 8: "[ruled
  in outline, design open]"; roadmap.md, The plan from T-A, the T-G bullet, Stage 3; design_records.md, T-G, PART C, C1).

## T-K — Context knowledge

**ruled** (2 October 2026); framework-wide (roadmap.md, The plan from T-A, the T-K bullet; design_records.md, T-K).

- **Part 1, crisp context knowledge**: **V1**, **ongoing** (roadmap.md, The plan from T-A, the T-K bullet, Part 1;
  glossary.md §8, **T-K part 1**). The steps are those of T-G_forward_inputs.md, section 5 (the tree) and 5.7.
  Disagreement for steps 4 to 7: roadmap.md's T-K bullet records steps 1 to 3 and ends with STEP 3 DONE, "Next: step 4
  of `docs/handoffs/T-G_forward_inputs.md`, section 5.7"; it does not record steps 4 to 7.
  - **Step 1, the layouts with more than one A/C switch**: **done** (4 October 2026) (T-G_forward_inputs.md, section 5,
    the tree, and 5.7, item 1; design_records.md, T-K, STEP 1; roadmap.md, the T-K bullet, STEP 1 DONE).
  - **Step 2, the plan of the build**: **done** (4 October 2026) (T-G_forward_inputs.md, section 5, the tree, and 5.7,
    item 2; design_records.md, T-K, THE BUILD'S PLAN, RULED; roadmap.md, the T-K bullet, STEP 2 DONE).
  - **Step 3, the build of context knowledge**: **done** (4 October 2026) (T-G_forward_inputs.md, section 5, the tree,
    and 5.7, item 3; design_records.md, T-K, THE BUILD, STAGES 1 AND 2 and STAGES 3 TO 7; roadmap.md, the T-K bullet,
    STEP 3 DONE; build_T-K_part1_state.md, Status).
  - **Step 4, kitting, idle robot, context knowledge on**: **done** (4 October 2026) (T-G_forward_inputs.md, section 5,
    the tree, and 5.7, item 4; design_records.md, T-K, STEP 4, KITTING, THE IDLE ROBOT: DONE).
  - **Step 5, kitting, the planning cases**: **done** (4 October 2026) (T-G_forward_inputs.md, section 5, the tree, and
    5.7, item 5; design_records.md, T-K, STEP 5, KITTING, THE PLANNING CASES: DONE).
  - **Step 5b, the existing kitting sets with context knowledge on**: **done** (4 October 2026) (T-G_forward_inputs.md,
    section 5, the tree, and 5.7, item 5b; design_records.md, T-K, STEP 5B, KITTING, THE EXISTING SETS WITH CONTEXT
    KNOWLEDGE ON: DONE).
  - **Step 5c, the gate after step 5b**: **done**; its design discussion **ruled** (AM67 to AM72) (T-G_forward_inputs.md,
    section 5, the tree, and 5.7, item 5c; design_records.md, T-K, THE GATE AFTER STEP 5B, RULED and THE GATE RULINGS,
    BUILT; build_T-K_gate_state.md, Status: "THE BUILD IS COMPLETE").
  - **Step 5d, the measurements after the gate change**: **done** (5 October 2026) (T-G_forward_inputs.md, section 5,
    the tree, and 5.7, item 5d; design_records.md, T-K, STEP 5D, THE MEASUREMENTS AFTER THE GATE CHANGE: DONE).
  - **Step 5e, kitting's rooms 02, 05, 06, 07 and copies of 08, 09**: **done** (5 October 2026) (T-G_forward_inputs.md,
    section 5, the tree, and 5.7, item 5e; design_records.md, T-K, STEP 5E, DONE and STEPS 5D AND 5E: THE DECISIONS
    CONFIRMED).
  - **Step 6, dock_loading's stage 1 measured in full**: sources disagree:
    - **done** (6 October 2026), ccode's provisional decisions waiting for Hadi's confirmation (design_records.md, T-K,
      STEP 6, DONE and STEP 6, FULL_REORDER, DONE; T-G_forward_inputs.md, section 5, the tree: "done (6 Oct;
      provisional decisions to confirm)");
    - **on hold** (T-G_forward_inputs.md, 5.7, item 6: "ON HOLD (Hadi, 5 October 2026, with step 7; step 5e done, the
      hold stands until Hadi rules)"; roadmap.md, The plan from T-A, the order block, the ADDED line of 5 October 2026:
      "T-K part 1's steps 6 and 7 are on hold");
    - remaining (T-G_forward_inputs.md, section 2: "dock_loading's part (step 6) and the close (step 7) remain").
  - **Step 7, the close of T-K part 1**: sources disagree:
    - **on hold** (T-G_forward_inputs.md, section 5, the tree: "on hold"; 5.7, item 6; roadmap.md, The plan from T-A,
      the order block, the ADDED line of 5 October 2026);
    - next, after Hadi's confirmation of step 6's provisional decisions (design_records.md, T-K, STEP 6, DONE: "Next:
      Hadi's confirmation of the provisional decisions; step 7 (the close of T-K part 1)").
- **Part 2, degrees of context facts (R5)**: **V1**, at the end of the V1 queue, after track 3b; **not started**
  (roadmap.md, The plan from T-A, the T-K bullet, Part 2: "Not started"; glossary.md §8, **T-K part 2**;
  T-G_forward_inputs.md, 5.8: "[ruled as design, not built]").
- **Later directions: the stream of context values with the world's dynamics**: **FW** (roadmap.md, The plan from T-A,
  the T-K bullet, "Later, future work"; V1 AND FW; glossary.md §8, **FW**).

## T-F — Evaluation (Phase 5)

**V1**; it follows T-G and is framed in TODO-144; the rest of T-F keeps its place after T-G (roadmap.md, The plan from
T-A, V1 AND FW; the T-F bullet, REVISED; the order block, the ADDED line of 5 October 2026; TODOS_AND_DEFERRED.md,
TODO-144: [OPEN] [V1]).

- **Part 1, the conditions human-unaware and intention-unaware**: **closed** (5 October 2026); its measurement extended
  by `full_reorder`, done (6 October 2026) (roadmap.md, The plan from T-A, the order block, the CLOSED line of 5 October
  2026; design_records.md, T-F part 1, THE CLOSE and THE MEASUREMENT EXTENDED BY FULL_REORDER, DONE; handoff_T-F_part1.md,
  its title).
- **Part 2**: **parked** (roadmap.md, The plan from T-A, the order block, the CLOSED line of 5 October 2026;
  handoff_T-F_part1.md, its title and section 5; design_records.md, T-F part 1, THE CLOSE).

## T-viz — The web-ui (T-V carried out as T-viz)

A name, not a task letter; **asked for** by Hadi (6 October 2026) (roadmap.md, The plan from T-A, the order block, the
ADDED and ASKED FOR lines of 6 October 2026; the T-viz bullet; glossary.md §8, **T-viz**). T-viz records use the status
words open, preferred, preferred, replaceable, proposed by cchat, verified, not verified (handoff_T-viz.md, 1.1).

**T-V — Viewer, interface and interactive simulator**: **carried out as T-viz** (Hadi, 6 October 2026, preferred):
track 1 is T-viz stage 1, track 2 is T-viz stage 3 (roadmap.md, The plan from T-A, the T-V bullet, CARRIED OUT AS
T-VIZ; glossary.md §8, **T-V**).

- **Stage 0, foundation**: **done**, closed (6 October 2026); **V1** (preferred) (roadmap.md, The plan from T-A, the
  T-viz bullet, DONE; the order block, the DONE line of 6 October 2026; design_records.md, T-viz, STAGE 0 CLOSED).
  - **0.1 recording**: **done** (6 October 2026) (roadmap.md, the T-viz bullet, Stage 0; design_records.md, T-viz,
    0.1, RECORDING, DONE).
  - **0.2 code structure**: **done** (6 October 2026); preferred (roadmap.md, the T-viz bullet, Stage 0;
    design_records.md, T-viz, 0.2, CODE STRUCTURE, DONE).
  - **0.3 the style trial**: **built**; its look accepted by Hadi "for now and for stage 0", its technology preferred
    (roadmap.md, the T-viz bullet, DONE; design_records.md, T-viz, 0.3, THE STYLE TRIAL, BUILT and STAGE 0 CLOSED).
  - **0.4 the messages between server and page**: **built** (roadmap.md, the T-viz bullet, DONE; design_records.md,
    T-viz, 0.4, THE MESSAGES, BUILT).
- **Stage 1, the first web-ui** (T-V track 1): **V1** (preferred); its place in the order of the tasks **open** (ccode's
  proposal: in T-V's place, after T-F and before track 3b) (roadmap.md, The plan from T-A, the T-viz bullet, V1 and FW;
  the order block, the AMENDED line of 6 October 2026; TODOS_AND_DEFERRED.md, TODO-190, point 4).
  - **1a, a sim-run in the browser**: **▶ NOW**, **asked for** (6 October 2026). Increment (i) **built** and reviewed
    (preferred); (ii) and (iii) next, built together; then (iv); then (v), polishing (roadmap.md, The plan from T-A, the
    order block, the ASKED FOR line; the T-viz bullet, AMENDED (HADI'S REVIEW OF INCREMENT (i)); design_records.md,
    T-viz, 1a, INCREMENT (i), BUILT and 1a, HADI'S REVIEW OF INCREMENT (i); plan_T-viz_1a.md, Progress: "Increments (ii)
    to (v) not started"). Disagreements:
    - roadmap.md's ASKED FOR line (order block) says "Nothing built; increment (i) after Hadi's review and his answers to
      the plan's questions"; the T-viz bullet of the same file, design_records.md and plan_T-viz_1a.md record increment
      (i) as built and reviewed.
    - Working tree: the untracked `docs/handoffs/build_T-viz_1a_state.md` states "In progress: Increment (ii)";
      plan_T-viz_1a.md (committed) states "(ii) to (v) not started".
  - **1b, the robot's mind (panel 4b)**: **open**; its contents decided later (roadmap.md, the T-viz bullet, Stage 1;
    handoff_T-viz.md, "What is still open", item 16).
  - **1c, plots over ticks (panel 4c)**: **open**; uPlot planned for it (preferred) (roadmap.md, the T-viz bullet, Stage
    1 and DONE; handoff_T-viz.md, "What Hadi prefers now" and "What is still open", item 18).
- **Stage 2, editing and comparison**: **FW** for now (preferred), until Hadi draws the V1 border inside the web-ui;
  questions recorded, decided when reached (roadmap.md, the T-viz bullet, Stage 2 and V1 and FW; TODOS_AND_DEFERRED.md,
  TODO-186, TODO-187, TODO-190).
  - **2.1 editing layouts**: **FW**, with stage 2 (roadmap.md, the T-viz bullet, Stage 2; handoff_T-viz.md, 12.1).
  - **2.2 editing setups**: **FW**, with stage 2 (same sources).
  - **2.3 editing scenarios** (the human's script, the timeline of context facts): **FW**, with stage 2 (same sources).
  - **2.4 sim-runs side by side**: **FW**, with stage 2 (same sources; TODOS_AND_DEFERRED.md, TODO-187).
- **Stage 3, changes during a sim-run** (T-V track 2, Phase 7): **FW** for now (preferred) (roadmap.md, the T-viz
  bullet, Stage 3 and V1 and FW; TODOS_AND_DEFERRED.md, TODO-188; glossary.md §8, **FW**, as amended).
  - **3.1 events, interruptions and deviations of the human's script**: **FW**, with stage 3 (roadmap.md, the T-viz
    bullet, Stage 3; handoff_T-viz.md, 12.1).
- **Items with no stage**: **open**, no stage yet (roadmap.md, the T-viz bullet, "Unassigned (TODO-189)";
  TODOS_AND_DEFERRED.md, TODO-189: "open").

## T-S — ROS/PRIEST

**FW** (1 October 2026), at the end of the queue (roadmap.md, The plan from T-A, the T-S bullet; V1 AND FW; glossary.md
§8, **T-S**).

## Other named items of the plan (outside the present order)

In the order of the roadmap's bullets.

- **D3 — `task_committed` is not a trigger**: **done** (September 2026) (roadmap.md, The plan from T-A, the D3 bullet).
- **Two-table re-examination of the recognizer and B2**: **not scheduled** (roadmap.md, The plan from T-A, its bullet:
  "a separate task, not scheduled"; the order block, "Unscheduled").
- **Oracle-IR evaluation**: its own pipeline task after T-H; **open** (roadmap.md, The plan from T-A, its bullet;
  TODOS_AND_DEFERRED.md, TODO-101: [OPEN]). No record states its place in the present order.
- **Alternative 1** (a human mind that generates the events, and a stack-aware IR): recorded as the next architecture
  direction, **not scheduled** (roadmap.md, The plan from T-A, its bullet).
- **T-E — Demonstration**: **superseded** by T-V, track 1 (30 September 2026) (roadmap.md, The plan from T-A, the T-E
  bullet; glossary.md §8, **T-E**).
- **Belief-aware planning**: unscheduled; recorded only (roadmap.md, The plan from T-A, the order block, "Unscheduled";
  TODOS_AND_DEFERRED.md, TODO-97: [OPEN, recorded only]).
