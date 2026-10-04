# T-G and T-K: forward inputs (T-G after its stage 1; T-K)

Written 2 October 2026 by the design chat that closed T-G stage 1. Place: docs/handoffs/.
Corrected 2 October 2026 by the next design chat, after its verification against the repo's records.
Updated 3 October 2026 at the close of the design chat of T-K part 1 (section 5 rewritten; sections 2, 7, 9 and 11 amended).
Updated 3 October 2026 after the design chat on T-K part 1's content points 1 and 2 (section 5 brought to that state;
5.1, 5.2 and 5.5 corrected; section 2's last paragraph amended).
Updated 3 October 2026 after Hadi's rulings on ccode's report (AM30 to AM33: section 5 in line; section 9 gains
TODO-163 and TODO-164).
Updated 3 October 2026 after Hadi's rulings on content point 3, the tests (KT1 to KT7, AM34: section 5 brought to that
state; 5.4 item 3 and 5.6 rewritten).
Updated 3 October 2026 at the close of the design chat on T-K part 1's tests, after the first round and Hadi's
decisions on its report (KT8 to KT12): section 5 rewritten as the handoff for the next design chat, which takes the
rest of T-K part 1; sections 1, 2 and 9 brought in line.
Completed 3 October 2026 from the design chat's scan of its conversation: section 5 (the occurrence condition per
task, the instruments in the build's plan, env_layout_05, the gate at exactly θ, the window edges, env_layout_16's
shelves) and section 11 (Hadi's rules of 3 October 2026); durations shown in ticks.
Updated 4 October 2026 after Hadi's rulings of 3 October 2026 on the form and the values of the strengths (AM35 to
AM39): section 5 in line (5.1 to 5.4 and 5.7 to 5.11); the method document named as the statement of the prior; the
entries on object ids and on subtype named (5.11).
Updated 4 October 2026 after Hadi's ruling on where the timeline of context facts is stated (AM40, AM41, KT13, KT14):
section 5 in line (5.1 to 5.4, 5.6 to 5.8, 5.10).
Updated 4 October 2026 after Hadi's rulings on the build's plan (AM42 to AM53; docs/handoffs/plan_T-K_part1.md): 5.2,
5.3, 5.7 and 5.10 in line.
Updated 4 October 2026 at the close of the design chat on T-K part 1's build plan (rulings AM40 to AM63): section 5
brought to the state the next design chat starts from (its opening, 5.6, 5.7 and 5.10 rewritten); section 2's T-K
paragraph; section 11 gains the rules Hadi set for the design chat on 4 October 2026.
Updated 4 October 2026 after step 5b and the design discussion that followed it (the design chat with Hadi, not ruled):
section 5's state rewritten (the build, steps 4, 5 and 5b, the reading for question G, the comparison, what remains
with no order decided); 5.5, 5.6, 5.7 and 5.10 in line; 5.13 added (the discussion); section 2's T-K paragraph;
section 11 gains the working rules Hadi set in that chat.
Updated 4 October 2026 after Hadi's rulings that closed the design discussion after step 5b (AM67 to AM72): section 5's
state, 5.1, 5.2, 5.4, 5.6, 5.7, 5.10 and 5.13 in line; section 2's T-K paragraph.
Updated 4 October 2026 after Hadi's rulings on ccode's report of those records (AM73 to AM76: the term "outranked",
the first limitation reworded, the exact tie, the recognizer's category; AM70's reason as corrected): 5.1 and 5.13.

Purpose. This file is the single place a new design chat reads to know what lies ahead in T-G and in T-K. It
collects, per stage of T-G and per part of T-K, what is already ruled, what is open, what is parked, and the ideas Hadi
stated. It replaces the reading of
the chain of earlier T-G handoffs. Those stay in the repo as history.

Status of this file. Informative. It decides nothing. Where it and the repo's records disagree, the records win.
Each item carries one of three marks:
- [ruled]: a ruling by Hadi that is recorded in the repo.
- [open]: a question recorded as open, or a proposal not ruled.
- [idea]: something Hadi said in a design chat. Some ideas are also in the records; those marked "chat only" are
  not, and no ruling rests on them.

Maintenance. The chat that closes a stage of T-G or a part of T-K updates this file: it removes what it settled and
adds what it produced for what follows.

---

## 1. The project and the domain, in brief

TeamRob's framework is a robot cognitive architecture for working beside a human. The robot observes the human,
keeps a belief over what the human is doing (intention recognition), and chooses and times its own tasks so that
it does not come closer to the human than a minimum separation (adaptive planning). The framework's core is
domain-independent. Kitting was the first domain. T-G adds a second domain, dock_loading, to test that the core
stays domain-independent.

The chain of the robot's mind, in four parts:
1. The recognizer keeps a belief over hypotheses. A hypothesis is a task the human may be doing: one of the
   human's assigned tasks, or a foreseeable task (a break; in kitting also the A/C activation).
2. The gate decides whether the meta-planner plans against the hypothesis with the highest probability. The gate
   requires three things. The belief is at least the threshold θ = 0.75. The hypothesis is adequate (what was
   observed in its current phase does not contradict it). The hypothesis is warranted (it is an assigned task, or
   the observed movement supports it). A hypothesis that passes is admitted. A retraction is the meta-planner's
   act of withdrawing an admitted projection when the admitted hypothesis becomes inadequate.
3. The projection states where the human is expected to be. If a hypothesis is admitted, the projection is that
   task's plan. If none is admitted, the robot uses the fallback projection: the human's observed motion continued
   for as long as it has been observed.
4. The meta-planner chooses the robot's next task and a hold before it, by cost, against that projection.

dock_loading. A truck stands parked at a dock gate. The robot is an automated forklift that replaces the driver.
Its assigned tasks: deliver full pallets from the truck to their delivery bay (dry or frozen), and return empty
pallets to the truck. The observed human is the warehouse staff member who receives the delivery. The human's
assigned task in stage 1: go to each delivered pallet and scan it. The human can scan a pallet only after the
robot has delivered it. The human's foreseeable tasks: a coffee break (a wait of 30 ticks) and an office
break (45 ticks, at a chair inside the office). T-K part 1's build adds ac_activation and room_warm to dock_loading's task
model and context knowledge; its three rooms get no A/C switch (AM18). When no task is applicable, the human goes to a standby place in the
middle of the hall. At the end the human goes to a desk beside the gate.

The room has three areas: the truck side, the hall, the office. The gate separates the truck side from the hall.
The office door separates the hall from the office.

---

## 2. Where T-G stands

T-G's staging, as recorded: stage 1, stage 2, then "track 4", then stage 3. All are inside V1, the first complete
version of the framework. T-G is paused after its stage 1 while T-K part 1, context knowledge, runs (section 5); T-G
resumes at its stage 2 when T-K part 1 is closed.

Stage 1 is closed (2 October 2026). What it delivered:
- Five framework-wide mechanisms, each built with kitting's outputs unchanged byte for byte:
  the rename of "zone" to "area"; the agent's area carried in computed states; a hypothesis is live only while one
  of its methods is applicable; object states and designations declared by the domain; the human's script as a
  priority list.
- dock_loading's tasks, three rooms without stores, and three kinds of setup (a fourth, "one bay", is named as conditional and not built).
- An intention-recognition test set (the IRB): 54 runs with an idle robot, zero disagreements with the
  expectations written before the runs.
- A recognition-to-planning test set (the MPB, the meta-planner test-bed): 52 runs with a working robot in two
  rooms, all completed, zero disagreements where full expectations existed (40 runs). This result does not state
  that the runs are free of violations of the minimum separation (section 4).

Scope of stage 1's tests, as Hadi set it [ruled]: they are an initial check that dock_loading works. The deeper
behavioural analysis belongs to stage 2. Hadi wants stage 2's questions, rulings and discussion taken in full
depth, one at a time.

T-K part 1 runs now. Its design is ruled and recorded (2 to 4 October 2026), the build's plan included and approved
(docs/handoffs/plan_T-K_part1.md). The mechanism is built, and kitting's tests with context knowledge on are run
(steps 4, 5 and 5b). The design discussion that followed them is closed: Hadi ruled on the gate and the strengths
(4 October 2026, AM67 to AM72; not built). The build of the two rulings on the gate, dock_loading's part and the close
remain, in no decided order. Section 5 holds its state.

---

## 3. The human's script, as ruled in stage 1 (binds every later stage)

- The human's assigned tasks are a fixed set known at the start. Which of them is applicable changes with the
  state of the room. The order of execution is not authored. [ruled]
- The author writes a priority list. Each time the human is free, it takes the first entry that is applicable and
  still open. A task in progress is never interrupted by a newly applicable entry. [ruled]
- An ordinary entry is taken at most once. It is closed when its task ends as completed, abandoned or infeasible.
  Closing an entry does not mean the assigned task is fulfilled; the robot may still regard it as unfulfilled.
  [ruled]
- A repeatable entry stands below every ordinary entry and carries no events. V1 has one: the standby entry. It
  is skipped while the human already is at the standby place. [ruled]
- The author declares a script that depends on the robot (an entry that waits for a delivery). [ruled]
- A closing part is taken once every ordinary entry is closed. Its content is each domain's convention. In
  dock_loading it is "go to the desk". [ruled]
- A foreseeable task written as an entry is an ordinary entry. A deviation (a break cut into a walk, a dropped
  task) is an event attached to its entry. [ruled]
- The simulated human does not react to the robot (docs/assumptions.md, the human's trajectory). A human that
  gives the robot space is future work. [ruled]

---

## 4. What stage 1 found (inputs for the next stages; none is ruled)

Recognition on dock_loading (the IRB, 54 runs):
- A true stretch is a run of consecutive ticks in which the human does one modelled task. The runs hold 153 true
  stretches. 147 lie in the support (the hypotheses allowed under the assignment prior: the human's assigned tasks
  and the foreseeable tasks). 6 lie outside the support (the scan of pallet_1 in two scenarios).
- Of the 147, 98 reached θ within the stretch, after a median of 20 ticks (range 6 to 50; one tick is 2 seconds).
  Each room has 49 of the 147. Reached θ: 38, 40 and 20 (env_layout_02, _03, _04; medians 28, 16 and 17 ticks).
- 49 never reached θ: 11, 9 and 29 by room. All 49 are scans. Every break stretch reached θ.
- The 49 fall in four classes:
  - Class 1, a short walk: 34 stretches of 26 ticks or fewer. At the start of an episode every live hypothesis has
    an equal share. A short walk gives too little evidence to lift one share above 0.75 when three or more
    hypotheses are live.
  - Class 2, the same motion: 9 stretches. Two unscanned pallets in one bay give two hypotheses that predict the
    same walk. They divide the belief, and neither is admitted. Hadi's recorded direction for this: planning
    against a set of hypotheses with the same projection instead of one dominant hypothesis (belief-aware
    planning, TODO-97). He wants this kept as a possible contribution of a paper.
  - Class 3, no walk: 3 stretches. Two pallets in one bay stand on one point, so the second scan has no walk.
  - Class 4: 3 scans that start as the human leaves the office in env_layout_02 (33 to 35 ticks). The short-walk
    cause does not explain them. No cause is recorded.
- The robot does not anticipate the scan that its own delivery makes possible (TODO-154). The scan hypothesis
  becomes live on the tick of the delivery and starts with an equal share.
- The walk to the standby place and the walk to the desk have no hypothesis (TODO-155). The robot reads them as
  the nearest modelled task. In most runs the walk is admitted as a coffee break or an office break. When the
  human then stands, the admitted hypothesis becomes inadequate and the retraction follows. This is correct by
  the present rules and wrong about the human.
- A fact of the task model: a scanned pallet's scan stays applicable, because the scan's conditions do not read
  the scanned state. This bears on "live only while applicable" and on store_pallet's condition.

Planning on dock_loading (the MPB, 52 runs):
- Many decisions rest on the fallback projection, because admissions are late or absent.
- A round trip of the robot to the truck takes about 96 ticks. A scan from the standby place takes 16 to 30. So
  in the domain's normal work cycle the robot never arrives at a bay while the human is there.
- A scan becomes applicable when the robot puts the pallet down. The human then walks to the bay the robot is
  leaving. The human passes the standing robot closer than the minimum separation. A standing robot does not
  count as violating by the present measure. Stage 1 counted these ticks separately (up to 15 with the human
  passing, 4 with the human standing beside). Whether to reopen the parked case "the human walks toward the
  robot" (TODO-135) is Hadi's decision, to take with these counts. [open]
- Violations of the minimum separation by a moving robot, all unanalysed:
  - The case to look at first in stage 2: the mixed runs M1, M2 and M4 in env_layout_04 (the room with opposed
    paths) under single_task (the strategy that selects one task at a time). Each has a violation at tick 387.
    The robot had decided a hold of 6 ticks at tick 382, against the fallback projection of a moving human. At
    tick 387 a scan was admitted, the new decision gave a hold of 0, and the violation fell on that tick. The
    declared property "no violation with a moving robot" failed in these three runs.
  - M2 in the same room and strategy also has violations at ticks 224 to 226.
  - Two controlled runs have two violations each: K8 in env_layout_03 under full_reorder (the strategy that
    orders the whole pool), and K9 in env_layout_04 under single_task.
- Other observations, unanalysed:
  - The robot's switch of task while carrying returns the pallet to the truck first.
  - In K9 on env_layout_04 the robot's own completion masks the retraction under single_task and not under
    full_reorder.
  - K4's holds lengthen at each expiry (13, 48, 96 ticks in env_layout_03; 10, 48, 96 in env_layout_04). The
    record cites this as evidence for the parked TODO-132 (a).
  - The mixed runs M1 and M4 of one room end on the same tick under each strategy.
  - The robot with nothing left to do stays standing at the bay of its last delivery (recorded in the findings
    of the second milestone scenario).
- CAVEAT (3 October 2026): the MPB run files of 500 steps or more and the milestone runs are potentially confounded
  by an undeclared weight (the hardcoded context weight multiplies coffee_break by 2.5 from step 500); the IRB's figures are not affected. design_records.md, "T-G stage 1", SCOPE REDUCED AND THE MPB ON DOCK_LOADING RUN,
  its CAVEAT.

Not tested in stage 1: env_layout_02 in the MPB (the room with the latest admissions, median 28 ticks); the test
that alters one rule of the oracle to show that a zero result is a detection (built for dock_loading, not run); a
setup in which all pallets go to one bay (recorded as conditional, never needed).

---

## 5. T-K part 1: context knowledge (framework-wide: kitting and dock_loading)

State at the close of 4 October 2026, after step 5b and the design discussion that followed it; written for a design
chat that has read nothing else. [ruled unless marked]
- The build (step 3 of 5.7) is done: b85494d to c62e7ea, eight stages by the approved plan, each checked against the
  previous stage's outputs (design_records.md, "T-K", THE BUILD). Both run options, assignment_knowledge and
  context_knowledge, are on by default. With context knowledge off every maintained log and instrument output is the
  gate stage's except the named lines. Where it lives: 5.5.
- Step 4, kitting with the idle robot, is done (a271c72, 32ce7ed, fffcffb, eec1903, f1ea2c4, caa708e;
  analysis/kitting/irb/tk2/REPORT.md). The setups' default timeline break_time 178 to 300, the A/C scripts room_warm
  from 150, and a scenario that is to meet another window states its own timeline. 59 runs, 0 disagreements with the
  oracle. The deliveries are admitted earlier; the coffee break earlier inside break_time and later outside it.
- Question S is ruled (AM65, 2daef04): the four strengths stay as ruled, not tuned to the movement evidence. Under
  discussion again since 4 October 2026 (5.13); no change until Hadi rules. RESOLVED (AM70, 4 October 2026): all
  strengths stay as ruled; a larger ordinary strength was not taken.
- The reading for question G (002e1ce; analysis/kitting/irb/tk2/REPORT.md, "The reading for question G"): the evidence
  alone turns against an interrupted delivery 3 to 9 ticks after the human left, the trigger rule 3 to 8 ticks later;
  a lone delivery admitted early lasts 43 to 60 ticks. Question G is ruled (AM66, 1fad437): the gate and the
  retraction stay as ruled. Under discussion again since 4 October 2026 (5.13); no change until Hadi rules. REOPENED
  AND RULED (AM67 to AM69, 4 October 2026): observation warrant is required at admission for every hypothesis; the gate
  refuses a leader that the evidence alone ranks below another live hypothesis; the end of an admission is unchanged.
  AM66 is superseded in part.
- Step 5, the planning cases, is done (1fad437, 450dad5, cfbf778, 17cadf0; analysis/kitting/mpb/tk/REPORT.md). Five
  cases on env_layout_18, 9 runs, 0 disagreements with the oracle. A gain as an earlier decision when the human acts
  as the context makes probable (cases 1 and 3); a cost when the human acts against it (case 5: a pass at 28.3 cm with
  the robot moving; case 4: no decision until the retraction at 43). Findings for TODO-146 and TODO-132 (a).
- Step 5b, the existing kitting sets with context knowledge on, is done (aa73ce3, 398d890, 613803b, a519475;
  analysis/kitting/mpb/tk5b/REPORT.md). 33 runs, 0 disagreements with the oracle; only the state with no raising fact
  occurs. 12 of the planning set's 16 authored cases reached. In scenario_s11_03 the robot releases item_8 11.3 cm from
  a standing human who never performs the assigned delivery admitted at tick 0.
- The comparison of context knowledge on against off (374283c; analysis/kitting/mpb/tk5b/COMPARISON.md), from existing
  outputs, no run. Three main numbers: the true task is admitted earlier in 206 of 325 true stretches (3005 ticks
  earlier, 365 later); admissions of a hypothesis that is not the true task during modelled tasks, 17 off and 47 on
  (114 and 504 gate ticks); in planning, completion better in 7 of 22 runs and worse in 2, and cases below
  min_separation 2 off and 5 on. The scenarios are authored: the counts compare the settings and are no rate of
  occurrence.
- The limitation of admission from context and movement (docs/assumptions.md 6.4; 298b22e, 479c3c7, restated in two
  parts in the records step after the discussion). In the first ticks of a walk the evidence for two targets is
  nearly equal (18 ticks); only this part is a limit of the situation. After it the evidence ranks the true task
  first, weakly at first and by about ×3 to ×14 at the end of the walk, and the prior overrules it (293 ticks); this
  part follows from the declared strengths and the gate. The largest gain and the largest costs come from one
  mechanism, a lone assigned task admitted before the human starts it (59 correct, 9 not; both new planning cases
  below min_separation).
- Two what-if readings, X and Y (6f11c13; analysis/kitting/mpb/tk5b/WHATIF.md): filters on the recorded gate answers,
  not runs. X is the discussion's 2.B, Y its 2.A (5.13).
- The design discussion that followed step 5b: 5.13. CLOSED AND RULED (Hadi, 4 October 2026; AM67 to AM72; 5.13's
  head). [ruled; AM67 and AM68 not built]

What remains of T-K part 1. A list; no order is decided. [open]
- The open design question of 5.13: the gate and the prior after an admission (Hadi rules). RULED (AM67 to AM72).
- The table of 5.13, from existing outputs, if Hadi wants it. RULED (AM70): the table at other values is the
  sensitivity analysis for the close.
- The build of AM67 and AM68, starting with a plan step in its own session (BUILD DISCIPLINE), and new measurements.
  BUILT (4 October 2026; docs/handoffs/plan_T-K_gate.md, approved with D1 to D7; design_records.md, "T-K", THE GATE
  RULINGS, BUILT; 2c939a5 to 8357b74 and the records commit). Next: the measurements with context knowledge on (the
  plan's section 8), a separate step: step 5's moved properties re-declared before its runs (D5), C4 to C6 on step 5's
  six (D6), B12's instance (D4).
- The question on the planning set's coverage matrix (5.13, question 3). [open]
- dock_loading's part (5.7, step 6).
- The close (5.7, step 7), with this file updated.
The design chat suggested settling the design question before dock_loading's part. Hadi has not confirmed it.
Where this section and the records disagree, the records win.

T-K is context knowledge as a whole: a task of the pipeline, framework-wide (it concerns kitting and dock_loading
alike), not a stage of T-G. Part 1 (V1, now): crisp context knowledge. Part 2 (V1, at the end of the V1 queue, after
track 3b): degrees (5.8). T-G stage 1.5 was renamed T-K part 1 on 3 October 2026; git commit messages use the old
name. T-G is paused after its stage 1 and resumes at its stage 2 when T-K part 1 is closed. [ruled]

### 5.1 Where it is recorded

- docs/design_decisions.md, the entry "T-K: context knowledge in the recognizer's belief": the conceptual part. R1 to
  R8 (the rulings), A1 to A7 (the assumptions), AM1 to AM66 (the amendments, each under the ruling it amends, the
  record parts in design_records.md; AM40 to AM64 are of 4 October 2026: the timeline, the plan, the cross-check; AM65
  question S under R3 and AM66 question G under R7, each with a NOTE of 4 October 2026 that it is under discussion
  again, resolved by AM67 to AM72: under R7 Hadi's principle, AM67 to AM69, AM71, AM72; under R3 AM70), the
  corrections C1, C3 and C4. AM1 to AM9 come from the review of the records; AM10 to AM29 from content points 1 and 2
  (the block CONTENT POINTS 1 AND 2, after R8; that chat's A1 to A15 are AM10 to AM24, its B1 to B5 are AM25 to AM29);
  AM30 to AM33 from Hadi's rulings on ccode's report; AM34 from content point 3 (under AM11); a CLARIFIED line under
  R3's AM2 (the occurrence condition evaluated per task); AM35, AM36 and AM39 under R3, from the design chat on the
  rest of T-K part 1 (the name, the three levels, the reading of a strength); AM40 and AM41 under AM11's AM34 (the
  setup's timeline the default, a scenario's own timeline replacing it whole; the override of the timeline, later work).
- docs/design_records.md, the heading "T-K": the record part. R9, superseded by AM3, and AM3's consequences; THE CUT
  AND THE QUEUE (what part 1 builds, part 2, the future work); OPEN ITEMS OF T-K PART 1 (all three ruled); NOTES FOR
  THE BUILD'S PLAN; CONTENT POINTS 1 AND 2 (the values: AM13, AM14's record part, AM16 to AM19, AM23, AM24, AM28,
  AM29); CONTENT POINT 3, THE TESTS (KT1 to KT7); ROUND 1 (KT8 to KT12); THE TASK RENAMED: T-K AND ITS PARTS; AM37
  under AM13 (the declarations) and AM38 under AM17 (the values and their sources); THE STRENGTHS REVISED (what became
  stale, the open item on the value the gate compares with θ, the method document, ccode's flags on it).
  Correction C2, the caveat on the long runs, stands under "T-G stage 1", in TODO-66 and in the MPB report.
- docs/glossary.md §5 (context knowledge, context value, context fact, timeline of context facts, timeline fact,
  membership function, suppressing condition, raising condition, suppressed / ordinary / raised strength, recency fact,
  observed completion, memory of observed completions, recency duration, the assigned tasks as a whole, strength,
  prior; occurrence condition retired); §8 (T-K part 1, T-K part 2); §9, setup (AM34).
- docs/context_knowledge_method.md: the method of context knowledge at the state of AM35 to AM39, the concept, the
  formulas of the prior and worked examples. It is the statement of the prior that the build's plan reads. The records
  win where the two disagree; a ruling that changes the method updates it in the same records step (CLAUDE.md).
- docs/design_records.md, "T-K", after the build: STEP 4, KITTING, THE IDLE ROBOT; QUESTION S, RULED; THE READING FOR
  QUESTION G; QUESTION G, RULED; THE PLANNING CASES, RULED (KT15); STEP 5 (its stages and its result); STEP 5B; CONTEXT
  KNOWLEDGE ON AGAINST OFF, AN OVERVIEW; THE LIMITATION OF ADMISSION FROM CONTEXT AND MOVEMENT; TWO WHAT-IF READINGS, X
  AND Y; THE DESIGN DISCUSSION AFTER STEP 5B (closed); THE GATE AFTER STEP 5B, RULED (AM67 to AM72: the measured
  basis, what becomes stale, the term "outranked", ccode's facts for the build's plan, what stays open; the rulings
  on it, AM73 to AM76).
- docs/assumptions.md 5.4 (the timeline's facts known exactly and at once; the source of a recency fact), 6.1 (given
  the task, the movement does not depend on the context), 6.2 (the declared and the actual duration match, a baseline
  whose violation is a deviation), 6.3 (the declared durations are at a compressed demonstration scale), 6.4 (an
  admission of a hypothesis that is not the true task, read against the evidence alone: the first part a boundary,
  the second part a consequence of the strengths and the gate).
- TODOs: TODO-66 (the hardcoded context weight; the build closes it); TODO-144 (T-F; its time-scale item holds the
  recency finding); TODO-154 and TODO-155 [V1]; TODO-158 to TODO-161, TODO-163, TODO-164 [FW]; TODO-162 superseded
  (AM3).
- The first round: analysis/kitting/irb/tk1/README.md and REPORT.md.

### 5.2 The design in plain words [ruled]

- Scope (R1). Context knowledge acts in the robot's mind only, in the recognizer's belief. It does not drive the
  human: it starts no task and interrupts no task of the human. A script may be authored to agree with it for a
  test; that is test authoring. Conditions of tasks stay in the task model. They decide which hypotheses are live;
  they are not context knowledge.
- The belief (R2, AM1). At each run of the recognizer, belief = normalise(prior × evidence) over the live hypotheses.
  The prior is evaluated on the context facts that hold at the present tick. The evidence is the likelihood
  accumulated in the present episode, with no context in it. The prior enters once and is never folded into the
  evidence. Adequacy and warrant do not read the prior. The rules on the episode boundary and on re-entry describe the
  evidence: at a boundary it restarts equal over the live hypotheses; a hypothesis that returns to the live set takes
  1/|H| of it.
- The prior (R3, R4, AM2 to AM4, C3). It is the normalisation of the strengths of what is live.
  - The assigned tasks as a whole (AM35; "work as a whole" in older records) contribute 1 while at least one of them
    is live, however many are live. Its share is divided equally among them. With assignment knowledge off (an
    ablation), every work task of the task model takes the place of the assigned tasks.
  - Each live foreseeable task contributes its declared strength, divided equally among that task's live hypotheses.
  - With no work hypothesis live, the normalisation runs over the live foreseeable tasks alone.
  - Every strength is greater than zero. With context knowledge on, every foreseeable task in the task model declares
    a strength. A declaration that violates either is rejected when the knowledge is loaded.
- A strength (AM36). The declared relative weight of a foreseeable task against the assigned tasks as a whole. Three
  levels per foreseeable task, in place of the low strength, the high strength and the occurrence condition. A
  foreseeable task declares a suppressing condition and a raising condition, each optional. If the suppressing
  condition is satisfied, the task has the suppressed strength; otherwise, if the raising condition is satisfied, its
  raised strength; otherwise the ordinary strength. The suppressed and the ordinary strength are declared once per
  domain, for every foreseeable task; the raised strength per task, with its raising condition. Each carries its
  source and is a modelling assumption until a site measures it. Reason: a number must not decide between hypotheses
  that the robot has no knowledge to tell apart; one low and one high value cannot state three situations (suppressed,
  ordinary, raised).
- The reading of a strength (AM39), proposed, not validated: at a task start, with only this foreseeable task and the
  assigned tasks live, the probability that the start is the foreseeable task is s / (1 + s). 0.005: 1 of 201 task
  starts; 0.02: 1 of 51; 0.5: 1 of 3; 2: 2 of 3.
- A condition (AM11, AM12, AM36). One fact or a conjunction of facts from three sources: a timeline fact (a window on
  the setup's timeline of context facts), an object state (T-G A5), a recency fact. T-K part 1 builds no "not"; "not"
  and "or" are T-K part 2's. At every level the foreseeable task stays live: context removes no hypothesis.
- The conditions are evaluated per foreseeable task, not per hypothesis (R3's AM2, its CLARIFIED line): one selection
  of the level per task, which is then divided among the task's live hypotheses. This is why V1 has at most one A/C
  switch per layout, and why a condition that differs per hypothesis is future work (TODO-164).
- Facts (AM10, AM14, AM20, AM21, AM30 to AM34).
  - Every fact of T-K part 1 is crisp: it holds or it does not hold.
  - A timeline fact is a state. An entry of the timeline is the change; the fact holds until the next change. The
    change is no trigger of the meta-planner; it acts only through the belief.
  - The setup holds the timeline of context facts, not the scenario (AM34): the timeline is the world's course and
    does not depend on what the human does, so one timeline is shared by the scenarios that bind the setup.
    AMENDED (AM40, Hadi, 4 October 2026): the setup states the default timeline (the site's break regulation belongs to
    the shift; a condition of the day, such as a warm room, is the designer's default). A scenario may state its own
    timeline, which replaces the setup's whole, with no merge per fact (a test case is a script, a window and an
    expectation, and the expectation is valid under one timeline only). Not stated in the scenario: the setup's
    applies; stated empty, or a setup with none: no timeline fact holds. Every timeline fact follows the same rules.
    The run's header prints the timeline in force and its source. The independence the design requires is causal (no
    action sets or removes a timeline fact) and holds wherever the windows are written. [ruled]
  - No action's declared effect sets or removes a context fact in the world.
  - A recency fact is a context fact derived from the time since the robot observed the completion of a named task.
    It holds for that task's recency duration after the observation. It is declared per task.
  - An observed completion is the task's terminal fact in the robot's world state, for example waited(agent,
    machine), not the episode boundary. Completion counts, not admission. A completion the robot does not observe,
    and a task cut before its completion, produce no recency fact.
  - The memory of observed completions is its own component of the robot's mind, outside the recognizer. It records
    the tick of an observed completion. The recognizer reads the recency facts as an input on each run and stores
    nothing across episodes.
- Perception (AM25, AM26). The robot knows which timeline facts hold, exactly and at once; no sensing is modelled
  (justified by the site's system, as for object states). The environment applies the timeline, the world state
  carries the facts, the recognizer reads them there. The declared context knowledge (the facts that exist, the
  suppressing and the raising conditions, the strengths, the recency durations) reaches the mind directly from the
  knowledge component, as the task model does.
- The values (AM16, AM37, AM38), the same in both domains where the task exists. Suppressed strength 0.005, ordinary
  strength 0.02, for every foreseeable task:

  | foreseeable task | suppressing condition | raising condition | raised strength | recency duration |
  |---|---|---|---|---|
  | coffee_break (kitting, dock_loading) | its recency fact | break_time | 2 | 90 ticks |
  | ac_activation (kitting, dock_loading) | ac_on | room_warm | 0.5 | none (ac_on covers it) |
  | office_break (dock_loading) | its recency fact | none | none | 135 ticks |

  break_time and room_warm are timeline facts; ac_on is the A/C switch's object state. A recency duration is 3 times
  the task's declared wait, counted from the observed completion. A coffee break just completed has the suppressed
  strength in every situation, inside break time too; ac_activation in a room not warm, with the A/C off, has the
  ordinary strength. Sources: 0.005 and 0.02 keep the sentence "Modelling assumption, Hadi, 3 October 2026. A relative
  strength. Its order of magnitude is motivated by the proposed meaning of a strength (a ratio of counted task
  starts), which is not validated." The raised strength 2 (in place of 3): break time favours the coffee break, more
  probable than an assigned task, not as strongly as 3 stated (3 asserted 3 of 4 task starts). The raised strength
  0.5 (in place of 0.2): a warm room is a matter of comfort with no stated time; the activation follows within about 3
  task starts (0.2 asserted 6). No value was chosen from the threshold or from a scenario.
- The A/C switch (AM18). An object in the layout with the state ac_on, which ac_activation sets. A setup may state its
  initial state. At most one per layout in V1, in every domain; a layout may have none. ac_activation and room_warm are
  in the task model and the context knowledge of both domains. dock_loading's three existing rooms get no A/C switch,
  so the re-measurement of stage 1's baseline shows the effect of context knowledge alone.
- The long-shift rule (AM22). The hardcoded rule (the step count since the shift's start) leaves at the build, with
  nothing in its place: the robot's expectation of coffee_break does not rise with the duration of work. A stated
  limitation until T-K part 2.
- Two independent run options (AM3, AM9): assignment_knowledge (today's assignment_prior) and context_knowledge (new),
  both on by default from the build (today assignment_prior defaults to off, TODO-139). Each "off" is an ablation or a
  diagnostic. With context_knowledge off, the prior is equal over the live hypotheses.
- The gate (R7, AM5), unchanged. An assigned task may be admitted before any distinguishing movement, on its
  commitment warrant, when its belief reaches θ on the prior. The prior is the robot's expectation, not evidence that
  the human has started; adequacy tests the hypothesis afterwards and can cause the retraction. A foreseeable task
  still needs observation warrant. The refusal of a leader with no observation (none(leader_no_observation)) stands.
  AMENDED (AM42, Hadi, 4 October 2026): the gate compares θ with the belief over the live hypotheses, with context
  knowledge on or off; the floor and the scaling by the pinned hypotheses stay in the reported distribution only (their
  removal there is TODO-178); the log prints the value the gate read. [ruled]
  RULED (AM67, AM68, Hadi, 4 October 2026; not built): observation warrant is required at admission for every
  hypothesis; commitment warrant alone no longer admits, so an assigned task is no longer admitted before movement. The
  gate refuses a leader that the evidence alone (E_t, without the prior) ranks below another live hypothesis: rank only,
  a tie passes, no constant, no margin, at admission only. The end of an admission is unchanged (AM69). Hadi's
  principle: an admission of X while the human does Y is not, for that reason, an error of the recognizer; the
  framework shows what recognition contributes to adaptive planning, and the core changes minimally. [ruled]
- One declared duration (R6). Context does not change the content of a projection. The only path from context to the
  projection is: prior, belief, gate, projection of the admitted task.
- The earlier entry "Assigned-task pool is a support restriction, not a prior" is superseded in part (R8, AM6): the
  assignment still restricts the support and sets no weight; declared strengths replace unit weight between the
  assigned tasks as a whole and the foreseeable tasks. The surviving concern: a number must not decide between hypotheses that the robot
  has no knowledge to tell apart.
- The assumptions A1 to A7 stand in the entry; A1 and A5 are also docs/assumptions.md 6.1 and 6.2.

### 5.3 What the build of T-K part 1 contains [ruled]

- The prior of 5.2, with crisp facts, and the three levels: per foreseeable task a suppressing and a raising
  condition, each one fact or a conjunction of facts over the three sources. No "not" (AM36): no form for "not" is
  needed. The statement of the prior that the plan reads: docs/context_knowledge_method.md.
- The setup's timeline of context facts (AM34), the default, and a scenario's own timeline, which replaces it whole
  (AM40); the run's header prints the timeline in force and its source. Today neither has a form for it; the build adds
  both.
- The declarations per domain: the context facts, the suppressed and the ordinary strength, and per foreseeable task
  its suppressing condition, its raising condition with its raised strength, the sources and its recency duration. Recency durations are declared in physical time and converted by the
  body. The declared knowledge replaces the class ContextKnowledge in shared/knowledge.py.
- The memory of observed completions, its own component of the mind (AM30).
- ac_on: a declared state and a declared effect of ac_activation. dock_loading needs the object type, the task
  ac_activation and the fact room_warm.
  RULED (AM43, AM45, Hadi, 4 October 2026): the effect is declared on a new action switch_on (wait_at's form), used by
  ac_activation only, in both domains; dock_loading's ac_activation has one method, from the hall, where its A/C
  switch would stand (the office method is added when a room gets a switch).
- Ruled on the plan (AM44, AM46, AM47, AM50, AM52; Hadi, 4 October 2026): an object-state condition holds for any
  object of its type; windows in ticks, half-open; the memory records a completion at the tick the terminal fact first
  holds, and an unobserved completion is not remembered; a timeline fact is stated by a timeline only (from the start:
  a window from tick 0); no condition of any schema (precondition, guard, completion condition, effect) names a
  timeline fact (AM52, AM54). The plan: docs/handoffs/plan_T-K_part1.md. [ruled]
- Ruled on ccode's cross-check (AM55 to AM58; Hadi, 4 October 2026): the build reruns round 1 and kitting's IRB and MPB
  sets with the new gate in the gate's stage, replacing their outputs, and stops if a declared property of the MPB no
  longer holds; dock_loading's IRB and MPB sets are stale from that stage until dock_loading's step; the
  episode-boundary label for a switch_on is deferred (TODO-179); the viewer's confidence is TODO-180. [ruled]
- The two run options, their names and their defaults; the rename of assignment_prior to assignment_knowledge in
  code, configuration and commands. Also flagged for renaming at the build: the context weight (ω_context,
  _context_weight) and the prior base. docs/assumptions.md 1.4 is updated at the build.
- The removal of the domain task names and constants from the recognizer, the long-shift rule with them (TODO-66).
- The instruments (NOTES FOR THE BUILD'S PLAN, the design chat's addition): the IRB's expectations must be computed
  with the new prior (its oracle assumes the equal prior and no context weight today); its report must read the three
  conditions A, B and C (5.4); the A/C's measure is its belief at its arrival. The plan states what this costs.
- Before the build, in its own step (AM19): the layouts with more than one A/C switch (5.7, step 1). Done, 4 October
  2026.

### 5.4 The tests [ruled]

Recorded: design_records.md, "T-K", CONTENT POINT 3, THE TESTS (KT1 to KT7) and ROUND 1 (KT8 to KT12).
- Order (KT1). Kitting first, then dock_loading's stage 1 scenarios. In each domain first the IRB with an idle robot,
  then the MPB with a working robot. Reason: T-K changes the belief, so the recognition is examined first; the two MPB
  cases then show whether a changed admission changes the robot's decision.
- Rooms on kitting (KT2, KT9). env_layout_15, _16 and _17, Hadi's design, as they are in 5.5. env_layout_12 to _14
  are unfit for a controlled test (they carry the MPB's many tables). env_layout_10, _11 and _02 stay as they are, as a
  comparison; env_layout_02 as it is after Hadi's correction of its object sizes (4191202; KT2's CORRECTED line; only
  the viewer reads a size). ccode may adjust the three rooms where it makes a better basic test, decided before the runs and never
  after seeing a result, because they are test instruments and not an evaluation reference.
- The basic set (KT3). The only variation is where a foreseeable task is placed: between tasks (after the first
  delivery, after the second, and so on) and inside a task, between its actions. No other kind of deviation, since
  this set tests the implementation of context knowledge and other deviations would mix causes. Size: five or more
  scenarios per room, every scenario run with context knowledge on and off. Expectations are stated before the runs.
  The second setup per room is dropped (KT13, Hadi, 4 October 2026).
- The timeline (KT4, AM34, as amended by AM40 and KT13). The setup states the default; a scenario that is to meet
  another window states its own timeline, on the room's one setup. The same activity under a window whose edge falls
  before the human leaves, during the walk, or after the arrival is authored this way.
- The conditions (KT14, Hadi, 4 October 2026): context knowledge off against on, each case labelled by the state that
  the script meets. The design chat restates the expected directions before the runs. [ruled] KT11's text, which
  the restatement replaces:
- The three conditions (KT11, ruled by Hadi). The run with context knowledge off is not a neutral baseline: the equal
  prior gives a foreseeable task the share of one delivery. So the tests read:
  - A: context knowledge off (round 1 is A);
  - B: context knowledge on, the context fact not holding (no raising condition satisfied);
  - C: context knowledge on, the context fact holding.
  A to B shows the effect of the declared strengths; B to C the effect of the context fact. One window in a setup
  puts some scenarios in B and others in C, since the foreseeable task falls at a different tick in each.
  The expected directions with context knowledge on, and their arithmetic, were stated for the old values; they are
  superseded (KT11's SUPERSEDED line; AM36 to AM38). The design chat restates them before the runs in B and C. Ruled
  by Hadi for that restatement: with context knowledge on and no raising fact holding, a lone live assigned task is
  admitted on its commitment warrant from its prior, and a retraction follows if the human then takes a foreseeable
  task. [ruled] SUPERSEDED (AM67, 4 October 2026): commitment warrant alone no longer admits; the lone assigned task
  needs observation warrant, and the gate refuses it while the evidence alone ranks another live hypothesis above it
  (AM68).
- The measure (KT3, KT10). Per true stretch: the tick at which the true task reaches the threshold and is admitted,
  and whether a retraction follows. For the A/C the measure is its belief at its arrival, not its admission.
- The two MPB cases (KT3): a coffee break inside the break time; deliveries through the whole break time.
  env_layout_17 serves the MPB or a mix.

### 5.5 What is built

Rooms (kitting; 6354a90, 1efe382, 014538a; env_layout_16's change in 4cd7bca). Square, 1000 x 1000; kitting_table_0
at (0, 450), the middle of the north wall, in all three; the exit walk's target corner_NE (450, 450); no door, no
obstacles. Each file's notes give bearings and distances from the table.
- env_layout_15, the basic room: five targets fanned out from the table to the south-west, south and south-east
  (shelf_1 to shelf_4, the coffee machine); no A/C switch.
- env_layout_17: env_layout_15 plus the A/C switch on the south wall, straight south of the table, between the two
  shelves shelf_1 and shelf_4.
- env_layout_16, the dense room: one cluster in the south-west with three shelves (shelf_0, shelf_1, shelf_2), the
  coffee machine and the A/C switch. Its two south-east shelves were removed before the runs only because its runs
  had to end before step 500 (KT9). The build removes that limit. Hadi accepted the room as it is; whether the shelves
  return is not ruled [open; 5.10].

Setups, one per room for now, with no timeline (no form exists yet): env_setup_13 (env_layout_15: item_1 to item_4,
item_i on shelf_i), env_setup_14 (env_layout_16: item_0 to item_2), env_setup_15 (env_layout_17: item_1 to item_4).
Every item is designated to the one kitting table.

Scenarios: scenario_s13_01 to _07 (env_layout_15), s14_01 to _11 (env_layout_16), s15_01 to _13 (env_layout_17),
in domains/kitting/scenarios/scenarios_s13.py, _s14.py, _s15.py; run files in configs/kitting/irb/tk1/. The robot
idle (an empty pool, observing only); the human assigned every delivery, delivering them in one order per room,
returning to the table and ending with the exit walk. _01 is the control; the others place one coffee_break or
ac_activation after a delivery or inside the second delivery (after the walk to the shelf, after the grasp, after the
carry). The placement table is in the round's README.

Round 1, the round without context knowledge, is condition A (KT8; 4cd7bca, 4c71b44). Rerun in the build with the new
gate and its outputs replaced (AM42, AM57); the numbers below are the old gate's, marked where they move. 31 runs, prior on (assignment
knowledge), test level 0.05, θ = 0.75. Every run agrees with the expectations committed before it (0 disagreements at
1e-9; one at print precision, s14_02 tick 181, the IRB's known flag). Every run ends before step 500, so TODO-66's
weight never acts. No retraction follows any admission. Where the numbers are:
- analysis/kitting/irb/tk1/REPORT.md: the measure per scenario (first tick at θ, admission, other admissions), the
  per-room table, what the rooms show, the observations;
- analysis/kitting/irb/tk1/README.md: the set, the placements, the foreseeable tasks' start and completion ticks per
  scenario (for authoring the timelines), the expectations and their md5s.
What the rooms show:
- env_layout_15: the movement recognises every task, late (a delivery reaches θ at about 70 to 85 percent of its walk
  to the shelf; the coffee break from the table at 32 to 34 ticks of a 43-tick walk).
- env_layout_17: the A/C hypothesis delays the two deliveries beside it (item_1 at 47 ticks against 37, item_4 at 45
  against 31).
- env_layout_16: the movement recognises nothing in the cluster before the arrival (deliveries reach θ only on the
  carry back, the coffee break only during its wait, the A/C never).

Nothing of the mechanism is built. Nothing on dock_loading is changed for T-K. (The state before the build; superseded
by the paragraph below.)

THE MECHANISM IS BUILT (step 3, 4 October 2026; design_records.md, "T-K", THE BUILD, STAGES 1 AND 2 and THE BUILD,
STAGES 3 TO 7; the state file `docs/handoffs/build_T-K_part1_state.md`): everything in 5.3, by the approved plan, in
eight stages, each checked against the previous one's outputs. Where it lives: the run options `assignment_knowledge`
and `context_knowledge` (both on by default; `configs/experiment.yaml`, `mesa_sim/run_mesa.py`); the gate on the
belief over the live hypotheses (`BeliefState.belief`, `confidence`); `Timeline`, `Window` and the resolution at load
(`shared/types.py`, `mesa_sim/sim_model.py`; the header line `[run_mesa] timeline`); break_time, room_warm, ac_on and
switch_on in both domains' `facts.py` and `actions.py`; dock_loading's ac_activation (one method, from the hall); the
declared context knowledge in each registry's `"context_knowledge"` (`shared/knowledge.py`, `ContextKnowledge`); the
memory of observed completions (`shared/completion_memory.py`); the prior in the recognizer (`context_prior`,
`_prior_weights`; the `[IR-context]` line); the IRB's oracle computing the prior on its own (rules 29 to 33 in
`analysis/kitting/irb/README.md`) and the readers labelling each case by the state the script meets (KT14) and
giving the A/C's belief at arrival (KT10). Checks: with context knowledge off every maintained log and every
instrument output is the gate stage's (B2) except the named lines; round 1 with it on agrees with the oracle in all
31 runs. No setup or scenario states a timeline yet, so no run of the build exercises a raised strength; the unit
tests against the method document cover it (AM49). dock_loading's IRB and MPB sets stay stale (AM57; step 6).

### 5.6 What is not built

- The mechanism: everything in 5.3, built by the approved plan (step 3). BUILT (4 October 2026; 5.5).
- The timelines of the setups and of the scenarios that state their own; the runs with context knowledge on (step 4).
  DONE for kitting (4 October 2026).
- The planning cases (step 5). DONE (4 October 2026), with step 5b.
- dock_loading's part (step 6). Not built.
- Any change the discussion of 5.13 may lead to: nothing ruled, nothing built. RULED (4 October 2026): AM67 and AM68
  change the gate; not built; their build starts with a plan step in its own session.

### 5.7 The steps from here

1. The layouts with more than one A/C switch (AM19). DONE (4 October 2026; design_records.md, "T-K", STEP 1; 32029d3,
   098b1a8): env_layout_05 keeps one A/C switch, ac_switch_1, and scenario_s04_01 one ac_activation; every layout of
   both domains holds at most one A/C switch. [ruled]
2. The build's plan. DONE (4 October 2026; docs/handoffs/plan_T-K_part1.md, 41efa76, amended to the rulings): its
   decisions ruled (AM42 to AM53), ccode's cross-check ruled (AM54 to AM63), ccode's proposals P1 to P5 accepted. The
   plan is approved. [ruled]
3. The build (BUILD DISCIPLINE, step 2), stage by stage as the plan states, each stage checked before the next. The
   first act of the next design chat is its prompt (the state above). The gate's stage is committed only after its
   checks pass; it stops on a disagreement with the oracle, on a declared property of the planning set that no longer
   holds, or on a scenario that no longer reaches its authored coverage case (three conditions, AM57 with AM61, as
   Hadi confirmed on 4 October 2026); a stop means its cause is examined, not
   that the ruling on the gate is rejected. The run without assignment knowledge is a diagnostic and never stops the
   build. [ruled]
   DONE (4 October 2026; design_records.md, "T-K", THE BUILD; 5.5). No stop condition was met. The foreseeable tasks'
   start and completion ticks of round 1's README stand, confirmed from the build's rerun with context knowledge on
   (31 of 31 trajectories; the recency fact of each coffee_break first holds on the README's completion tick and lasts
   90 ticks, in all 17 coffee_break scripts).
4. The timelines and the runs with context knowledge on. [ruled unless marked]
   - One setup per room with its default timeline; a scenario may state its own, which replaces the setup's whole
     (AM40, KT13).
   - The windows are authored only after ccode supplies the start and completion ticks of the foreseeable tasks in the
     existing scripts. A case that no existing script covers needs a new script. (ccode, a fact: round 1's README
     already lists these ticks for its 31 scripts; the robot is idle there, so the gate's change does not move the
     human's ticks; ccode confirms them after the build's rerun, as Hadi accepted on 4 October 2026.)
   - The design chat restates the expected directions before the runs: context knowledge off against on, each case
     labelled by the state the script meets (KT14), with the revised strengths (5.2).
   - To add to them, as Hadi ruled (KT11's RULED line): with no raising fact holding, a lone live assigned task is
     admitted early on its commitment warrant, and a retraction follows if the human then takes a foreseeable task.
     SUPERSEDED (AM67, 4 October 2026): no admission on commitment warrant alone (5.4).
     Its admission still waits for its first observation (the gate refuses a leader with no observation).
   - With no assigned task live, the foreseeable tasks share the whole prior (the method document, section 12). Hadi's
     caution: this state is no argument for or against any strength value.
   - At a foreseeable task's completion (the plan, section 11, X9): on the completion tick the task's hypothesis is
     retired and takes no share; it re-enters with 1/|H| of the evidence, under its suppressed strength, on the tick its
     terminal fact stops holding (the human's next step); while the human stands at the machine, it stays retired.
   - The expectations are stated before the runs; every expectation near a window's edge depends on the half-open
     reading by one tick (AM46).
   DONE for kitting with the idle robot (4 October 2026; design_records.md, "T-K", STEP 4, KITTING, THE IDLE ROBOT;
   analysis/kitting/irb/tk2/REPORT.md): 59 runs, 0 disagreements with the oracle; the directions read per side.
5. The planning cases, with a working robot. KT3 rules two: a coffee break inside the break time, and deliveries
   through the whole break time (env_layout_17 serves; the robot must not hold the items of the two shelves beside
   the A/C switch). Hadi wants a recommendation on one case for the early admission and its retraction, since it is
   the consequence of the new prior that reaches planning most directly. [open] (Whether this case is a third
   planning case or takes the place of one of KT3's two stays open for this step; Hadi, 4 October 2026.)
   - Question S is ruled (AM65, 4 October 2026): the four strengths stay as ruled; a table of step 4's cases under
     compressed values is a sensitivity analysis for the close, not a candidate design. [ruled]
   - Question G, admission and retraction under context knowledge: ccode's reading of step 4's outputs is in
     analysis/kitting/irb/tk2/REPORT.md, "The reading for question G" (design_records.md, "T-K", THE READING FOR
     QUESTION G). RULED (AM66, Hadi, 4 October 2026): the gate and the retraction stay as ruled; a deviation from what
     the context makes probable is caught late, the A/C case is not corrected by the movement, the meta-planner keeps
     an admission 1 to 9 ticks past the gate's answer. [ruled]
   - The planning cases are five (KT15, Hadi, 4 October 2026; design_records.md, "T-K", THE PLANNING CASES, RULED):
     KT3's two, the early admission correct, and the early admission against the context with a coffee break and with
     the A/C. Stage 1's proposal (the set, the disjointness rule on env_layout_17, the predictions): design_records.md,
     "T-K", STEP 5, STAGE 1: THE PROPOSAL; the room ruled, option (b), env_layout_18 (THE ROOM, RULED); the set:
     STEP 5, STAGE 1, REVISED: THE SET. [ruled]
     DONE (4 October 2026; analysis/kitting/mpb/tk/REPORT.md; design_records.md, "T-K", STEP 5, KITTING, THE PLANNING
     CASES: DONE): 9 runs, 0 disagreements; a gain as an earlier decision (cases 1, 3), a cost when the human acts
     against the context (cases 4, 5); findings for TODO-146 and TODO-132 (a). [done]
5b. The existing sets of kitting with context knowledge on, no new authoring (Hadi, 4 October 2026; design_records.md,
   "T-K", STEP 5B, PLANNED): first the recognition set (17 scenarios on env_layout_10 and _11, the robot idle), then the
   planning set (16 scenarios on env_layout_12 to _14), read against its coverage matrix. The run files with context
   knowledge off stay each set's reference. [ruled, planned]
   DONE (4 October 2026; analysis/kitting/mpb/tk5b/REPORT.md; design_records.md, "T-K", STEP 5B, KITTING, THE
   EXISTING SETS WITH CONTEXT KNOWLEDGE ON: DONE): 33 runs, 0 disagreements with the oracle; only the state with no
   raising fact occurs (no timeline). Recognition: the deliveries admitted earlier, the coffee break later, new wrong
   admissions of a lone delivery during a coffee break between deliveries (18 to 22 ticks). Planning: 12 of 16 authored
   cases reached; not reached: s10_08 (the cause boundary in place of replaced), s10_10 (E6), s11_01 (P6.1's trigger),
   s11_03 (D9; the robot delivers 11.3 cm from a standing human who never performs the assigned delivery admitted at
   tick 0). [done]
   After step 5b: the comparison, the limitation (docs/assumptions.md 6.4), the what-if readings and the design
   discussion (section 5's opening, 5.13). Steps 6 and 7 keep their numbers; their order against the open design
   question of 5.13 is not decided. [open]
   The design question is RULED (AM67 to AM72, 4 October 2026). Open: the order of what remains (the build of AM67 and
   AM68, dock_loading's part, the close) and the question on the planning set's coverage matrix. [open]
6. dock_loading's part. [open unless marked]
   - Its layouts and setups changed after stage 1's baseline was measured (`subtype` on the delivery bays and the
     pallets, 5d19859). [ruled as a fact]
   - Its two test sets (the recognition set and the planning set of stage 1) are stale since the gate's change; the
     build does not rerun them; this step measures them again (AM55, AM57). [ruled]
   - The removal of the long-shift rule changes its runs of 500 steps or more (the 22 MPB runs of section 4's caveat,
     the milestone runs). [ruled as a fact]
   - Whether T-K part 1 answers the open item on the scan the robot does not anticipate (TODO-154: the robot's own
     delivery makes a scan applicable, and the share at the episode's start) is not decided.
   - The open flag on the coffee break from the office (the method document, section 12): its walk to the machine is
     warranted on its entry from the walk to the office door, so the method document's cases of the gate with no
     assigned task live do not hold there.
   - What its layouts and scenarios need for context knowledge (the timelines in its setups; no A/C switch in its three
     rooms; its ac_activation has one method, from the hall, AM45).
7. The close of T-K part 1, with this file updated. Then a later design chat returns to T-G's stage 2 (section 6).

### 5.8 What waits

- The second coffee break and the recency fact: they wait for a further layout by Hadi, with more shelves and items
  (KT2). [ruled]
- The duration mismatch (a coffee break cut short or prolonged): a later set, since it needs a deviation event (KT3).
  Authorable (AM29): a shorter wait (during wait_at, drop; at 23 ticks, written as 46 seconds, since a half tick
  cannot be written; the entry closes as abandoned); a longer wait (during wait_at, a Start of stand). Neither when the coffee
  break is itself the task of another entry's event (the stack is one level deep, TODO-100): recorded as absent.
  [ruled]
- T-K part 2 [ruled as design, not built]: degrees (R5): a context fact satisfied to a degree in [0, 1], a membership
  function from a context value, minimum for "and", maximum for "or", 1 minus the degree for "not" ("not" is part 2's
  again, AM36). Open with it: the representation of a context value and of a degree (AM8); the linear rule, strength =
  low + degree × (high − low), was stated for the pair of a low and a high strength and is restated for two conditions
  (AM36). Hadi's ideas
  [idea, not ruled]: soft edges of a window; a gradual return of the strength after a task; "or" with "long work
  without a break" (open: what counts as a break, when the count starts, its limit and source, the unobserved human).
  After T-G stage 2 [open]: whether succession between tasks affects the division inside the assigned tasks as a whole (R4), with
  store_pallet present. Not taken, and not future work [ruled]: a preference for a task that has just become
  applicable.
- Future work [FW]: section 9.
- The override of the timeline from the run file and from the viewer, taking precedence over the setup and the
  scenario (AM41): later work, recorded, not built in T-K part 1. A change of a fact during a run belongs to the
  interactive phase (T-V track 2). [ruled]
- Under TODO-155 [open, parked]: no share for "none of the modelled tasks" (it would reopen the decision that the
  belief has no residual hypothesis).
- Outside T-K part 1 [open]: whether a hypothesis stays live when its method's condition turns false while the human
  does the task.

### 5.9 Findings to carry into the next runs (none changes a value) [ruled as findings]

- SUPERSEDED (AM38; KT6's SUPERSEDED line): the finding that the coffee break's prior in break time equals the
  threshold. With the raised strength 2, one coffee machine and no A/C switch, the coffee break's prior inside the
  break time is 2/3 for any number of live deliveries, and each of n live deliveries has 1/(3n).
- The recency duration of 90 ticks was derived from the wait, which is compressed, while walking is not; in these
  rooms the walk from the coffee machine to the table and back takes about 84 to 94 ticks. It joins T-F's open item on
  the time scale (TODO-144). (KT6)
- In env_layout_15 the prior has no effect once no delivery is live (only one foreseeable task is live there). (KT6)
- In env_layout_17 the robot must not hold the items of the two shelves beside the A/C switch, or the switch no longer
  stands between two of the human's hypotheses; and two deliveries that finish together at the shared table stop
  closer than min_separation. The caution reads by role because objects in these rooms may move or be renumbered.
  (KT6, KT9)
- The A/C activation is almost never recognised by movement, since its wait is one tick. The wait stays; it is a
  domain value. Hence the A/C's measure is its belief at arrival. (KT10)
- A coffee break begun inside a delivery after the carry leads but stays inadequate until the human reaches the
  machine, because its evidence counts from the start of the delivery: the episode's existing behaviour, which the
  prior does not change. (KT10)
- Two A/C cases in env_layout_17 (s15_10, s15_11) peak just under θ with the equal prior (0.746, 0.745): a later
  crossing there must not be read as the effect of the A/C's strength. (KT10)
  MOVED (4 October 2026, the gate's stage, AM42): over the live hypotheses 0.7487 and 0.7468, still below θ.
- The gate refuses only below the threshold. Where the prior alone is exactly θ, the outcome at the first observed
  movement depends on floating-point rounding; the runs are deterministic, so the result is stable, and it is
  arbitrary. (KT11, its ADDED line; its case, the coffee break inside the break time in env_layout_15 at 0.75, no longer
  arises with the raised strength 2.)

### 5.10 Open points the next chat must put to Hadi [open]

ANSWERED on 4 October 2026 (steps 4 and 5): points 1, 2 and 3 below. Open: points 4, 5 and 6, and the questions of
5.13. Of 5.13's questions, 1 (the direction for the gate and the prior) and 2 (the table) are answered by AM67 to AM72
(4 October 2026); 3 (the planning set's coverage matrix) and 4 (the order of the remaining work) stay open.
1. The expected directions for the runs with context knowledge on, restated before those runs (5.7, step 4).
2. The windows of break_time and room_warm: the setups' defaults and the scenarios that state their own, authored from
   the foreseeable tasks' ticks ccode supplies. Hadi's addition (KT4, its ADDED line): the same activity under a window
   whose edge falls before the human leaves for the foreseeable task, during the walk to it, or after the arrival. The
   middle case is the recorded cost of crisp facts: the prior changes inside the episode at one tick.
3. The planning cases (5.7, step 5): the recommendation on one case for the early admission and its retraction; their
   scenarios on env_layout_17; the separation when two deliveries finish together at the shared table.
4. dock_loading's part (5.7, step 6): what its layouts and scenarios need; whether TODO-154 is answered; the 22
   potentially confounded MPB runs, measured again in this step.
5. Whether env_layout_16's two south-east shelves return once the build removes the step-500 limit (KT9, its ADDED
   line; Hadi accepted the room as it is).
6. The open flag on dock_loading's coffee break from the office (5.7, step 6).
Answered on 4 October 2026 and no longer open: the second setup per room (dropped, a scenario may state its own
timeline); the items of the build's plan (ruled); which value the gate compares with the threshold (the belief over
the live hypotheses).

### 5.11 What the build must respect [recorded]

- T-K is framework-wide: it concerns kitting and dock_loading alike [recorded]. The build's acceptance includes
  kitting [chat only].
- The build's acceptance (AM24) [ruled]: "identical except for the lines the build names", with the regression audit.
  The rename of the run option changes the run header in every log. With context_knowledge on, runs with
  assignment_knowledge off change too. With assignment knowledge on, each foreseeable task has its declared strength
  in place of an equal share [chat only: the design chat's statement of this consequence]. Runs of 500 steps or more
  change even with context_knowledge off, because the hardcoded weight leaves.
- Every existing baseline set and test either states context_knowledge off to stay identical, or is regenerated with
  the reason stated, with the regression audit CLAUDE.md requires.
- The recognizer is a core algorithm. The change is domain-independent and ruled. The build touches nothing else of
  the core at the conceptual level without asking.
- ccode works in two steps: a plan with no code, confirmed in the design chat, then the build.
- Two entries of 3 October 2026 in design_decisions.md bear on the build [ruled]: "An object id is an opaque name" (no
  code reads meaning from the text of an id) and "`subtype` is a stated fact of an object" (dock_loading's bays and
  pallets carry dry or frozen; the loader checks the setup; the robot does not read it). Their bearing: the build
  identifies no object by the text of its id; dock_loading's layouts and setups changed after stage 1's baseline was
  measured (5d19859, subtype added), which the re-measurement (5.7, step 6) starts from.

### 5.12 Background from the design chat [chat only]

- The reason for the form of the prior: the literature puts context in the prior (Pynadath and Wellman
  1995; Kelley et al. 2012; CoBaIR, Lubitz et al. 2023). The hierarchy follows the idea of a nested
  choice model; the form is a hierarchical prior with declared relative strengths and inherits none of
  that model's further assumptions. These references may serve the paper.
- Discussed and not held: kinds of knowledge by force (a strict constraint, a norm, a habit) and by
  scope (general, sector or organisation, domain or site). The principle that was held and ruled: only
  a condition of the task model removes a hypothesis; context only changes how probable a live
  hypothesis is.
- A consequence of the ruled prior, stated as a consequence and not as its reason: with one assigned
  task live and no raising condition satisfied (AM36: the foreseeable tasks at the ordinary or the
  suppressed strength), the assigned task starts near the threshold or
  above it. This bears on the finding that the robot does not anticipate the scan its own delivery
  enables (TODO-154).
- Superseded for T-K part 1 by R1: Hadi's earlier sketch in which a context fact triggers a foreseeable task of the
  human or interrupts a task in progress.


### 5.13 The design discussion of 4 October 2026 after step 5b [closed: ruled 4 October 2026, AM67 to AM72]

RULED (Hadi, 4 October 2026, in the design chat; design_decisions.md, "T-K", under R7 and R3; design_records.md, "T-K",
THE GATE AFTER STEP 5B, RULED). Ruling n is AM(66 + n). [ruled; AM67 and AM68 not built]
Hadi's principle: if the robot admits task X and the human does Y, the recognizer was not wrong for that reason. Either
the human did something unexpected given the modelled knowledge and the evidence, or the recognizer is limited. The
framework is about what recognition contributes to adaptive planning; it is not changed to make every run flawless.
Changes to the core stay minimal.
1. AM67 (the discussion's 2.A). Observation warrant is required at admission, for every hypothesis. Commitment warrant
   alone no longer admits. A lost observation warrant still ends nothing. Reason: the prior states which task is
   probable; nothing states when the human starts; a projection built before the first movement assumes a start tick
   the robot has not observed. Measured cost (what-if Y): the 59 lone assigned tasks admitted 1 tick later. It reverses
   the part of T-D G that admits an assigned task before movement, the same part of R7 (with AM5), and KT11's RULED
   line.
2. AM68 (2.B, as a condition of admission). The gate refuses a leader (the hypothesis with the highest belief) that the
   evidence alone ranks below another live hypothesis. Rank only; a tie passes; no constant, no margin; a condition of
   admission only. Reason: context knowledge may make an admission earlier; it may not admit a task against the rank of
   the observed evidence; a margin would be a new constant. Not taken: the same condition as a ground for ending an
   admission (it changes T-D L). The term (AM73): such a leader is outranked; the refusal reason
   none(leader_outranked). The tie is an exact comparison, with no tolerance (AM75). The recognizer reports one
   category per live hypothesis; the gate reads the leader's (AM76).
3. AM69. The rule on when an admission ends (T-D L) is unchanged: an admission that was correct when made stays until
   the retraction. A stated limitation.
4. AM70. All strengths stay as ruled: raised 2 (coffee_break) and 0.5 (ac_activation), ordinary 0.02, suppressed
   0.005; 1.A not taken. Reason: a strength is the designer's statement about a site, not chosen from test results;
   with 1 and 2 which hypothesis is admitted no longer depends on the value; whether and how long a leader the
   evidence ranks first stays at the threshold still does (the reason as ccode corrected it, accepted). The table at
   other values stays a sensitivity analysis for the close.
5. AM71. Not taken: 3.A, 3.B, 4.A. 3.B and 4.A are possible future work (TODO-97, TODO-96).
6. AM72. The cases that remain are limitations, not defects: a near-tie in the evidence that favours a hypothesis the
   human is not doing (AM74's wording); the
   evidence itself ranking another task first after the human interrupts a task; the human doing the less probable task
   after a correct admission (docs/assumptions.md 6.4).
Open: the order of the remaining work; question 3 below (the planning set's coverage matrix); the build of AM67 and
AM68, which starts with a plan step in its own session. ccode's facts for that plan: design_records.md, "T-K", THE GATE
AFTER STEP 5B, RULED. BUILT (4 October 2026; THE GATE RULINGS, BUILT). The plan: docs/handoffs/plan_T-K_gate.md, APPROVED (Hadi, 4 October 2026, with D1 to D7;
design_records.md, "T-K", THE GATE'S BUILD PLAN, RULED). D4 closes question 3 (the coverage matrix).
What follows is the discussion as recorded before the ruling.

The design chat discussed the results of steps 4, 5 and 5b with Hadi. Nothing was ruled. Hadi continues the
discussion in the next design chat and rules there. No point below carries a ruling number. Each point is attributed:
Hadi's position in the discussion, or the design chat's suggestion, not confirmed by Hadi. The rulings S (AM65, the
strengths stay) and G (AM66, the gate and the retraction stay) stand as recorded until Hadi rules; each carries a note
that it is under discussion again (design_decisions.md, "T-K", under R3 and R7). The record: design_records.md, "T-K",
THE DESIGN DISCUSSION AFTER STEP 5B.

The problem as discussed. After an admission the meta-planner uses the projection of the admitted task alone. The
projection is the same for a belief of 0.76 and of 1.0, and the same with and without observation warrant. Context
knowledge makes the belief high earlier, also before any movement.

The changes discussed, with their labels:
- 1.A (prior): a larger ordinary strength only. 0.1 and 0.2 were named as values to compare. The raised and the
  suppressed strengths stay.
- 2.A (gate): commitment warrant alone does not admit; observation warrant is required.
- 2.B (gate): the leader is admitted only if the evidence alone ranks no other hypothesis above it.
- 3.A (projection): an admitted task without observation warrant is projected as the human staying at the observed
  position until the human moves.
- 3.B (meta-planner): the robot's plan is checked against the admitted task's projection and the fallback projection
  together.
- 4.A (response): communication or slowing down when the admission is weak (T-D X).

Hadi's positions in the discussion (not rulings):
- Hadi does not want 3.B in this framework. It changes the meta-planner and mixes high-level planning with a lower
  level. The framework's objective is IR → AP: to show what recognition contributes, not to run a perfect simulation.
  Hadi sees 3.B as possibly part of future work on planning that uses the belief.
- A ruled decision can be reopened if there is a good reason. Hadi asked why 1.A is not reopened.
- Some admissions of a hypothesis that is not the true task are sound reasoning: the human did the less probable
  thing.

The design chat's suggestions (not confirmed by Hadi):
- A principle for the gate: context knowledge may make an admission earlier; it may not admit a task that the
  observation does not show.
- 2.A as necessary. With context knowledge on, the admission before movement gains 1 tick in the 59 correct cases and
  produces the 11.3 cm case (scenario_s11_03). It would reverse the part of T-D G that admits an assigned task before
  any movement.
- 1.A and 2.B as two candidates for the same problem (the prior overruling the evidence), to be decided from numbers.
  Unknown for 2.B: how much gain it keeps, and whether the admission switches on and off at ratios near 1. For 1.A: a
  new value needs an argument about its meaning from Hadi. By the proposed reading of a strength (AM39): 0.02 is 1 of
  51 task starts; 0.1 is 1 of 11; 0.2 is 1 of 6.
- 3.A is not needed if 2.A is taken. 4.A as future work.
- The reasons it gave for looking at S and G again. Its argument for S used an estimate (one walk shifts the belief by
  a factor of 3 to 4) that the data corrected (12 to 14). Its argument for G (a), that an evidence condition acts on
  differences of 0.0002, holds only in the first ticks of a walk.
- Which measured case each change would cover:
  - the standing human (scenario_s11_03, 11.3 cm): 2.A yes, 2.B no;
  - the walk to the A/C switch (scenario_s16_05, 28.3 cm): 2.A no; 2.B on a ratio of 1.003 to 1.09; 1.A at 0.2 yes
    (the lone delivery's prior is 0.71, below the threshold, in a room with two foreseeable tasks);
  - the wrong admissions of 43 to 60 ticks: 2.B after the first ticks; 1.A shortens them;
  - the gap between plan and execution at a turn (TODO-146) is a separate defect that none covers.
- A table that could inform the ruling, from existing outputs with no simulation run: the recognition sets under 2.A,
  under 2.B, under 1.A at 0.1 and at 0.2, and their combinations, each as gains kept, wrong admissions removed, and
  switches within a stretch. For the strengths the oracle recomputes the belief, since the human's trajectories do not
  depend on them. It would also serve as the sensitivity table that question S planned for the close.

Questions put to Hadi, unanswered:
1. The direction for the gate and the prior.
2. Whether that table is wanted.
3. Whether the coverage matrix of the planning set stays the matrix of the off setting with one added column for
   context knowledge on, or new scenarios are authored.
4. The order of the remaining work.

Facts from the repository for this discussion (ccode, the records step of 4 October 2026; no position):
- WHATIF.md already holds part of that table. Its filter Y is 2.A and its filter X is 2.B (the evidence alone ranks no
  other live hypothesis strictly above the leader, by more than 1e-9), each alone and together, on step 4's 57 runs
  and step 5b's 17 recognition runs with context knowledge on. X keeps all 216 earlier admissions of the true task; Y
  delays the 59 lone assigned tasks by 1 tick. Changes of the answer within a true stretch: 673 recorded, 653 under X,
  579 under Y, 560 under both. Missing: 1.A and its combinations. With the robot idle, the belief, adequacy and warrant
  do not depend on the gate, so a filter's per-tick answer is the answer a run would give; the decision record and the
  trigger rule are not recomputed.
- 2.A would also reverse T-K's R7 as amended by AM5 (an assigned task may be admitted before any distinguishing
  movement, on its commitment warrant) and KT11's RULED line (a lone live assigned task admitted early on its
  commitment warrant; 5.4).
- scenario_s16_05, the run with context knowledge off: the ratio of the A/C activation over deliver_item(item_4) is
  ×1.0014 at tick 0 (the admission), ×1.0029 at 1 and ×1.09 at 25 and 26.

---

## 6. Stage 2: the full domain

Content, as recorded [ruled unless marked]:
- A second assigned task of the human, store_pallet: the human takes a delivered and scanned pallet from its
  delivery bay to its onward container (the dry store or the freezer). The order per pallet is delivered,
  scanned, stored. Each full pallet gets a second designation in the setup, its onward container. The human
  carries a pallet as the kitting human carries an item. The human never delivers from the truck and never
  returns empties.
  Hadi's reasons: the human then has two kinds of assigned task; the robot must hold the onward movements as
  possible intentions; the task depends on the robot's delivery.
- The room with the stores: delivery bays in a row on one side wall, the frozen bay nearest the gate; the freezer
  and the dry store on the opposite wall, the freezer nearest the gate; the empties in the top corner on the bay
  side; the office at the top centre. Requirements: goods flow forward and never travel away from their store and
  back; the freezer lies near the dock; no bay stands in front of a store entrance; one place for empties that
  both stores can bring to. The arrangement can be revised when stage 2's layout is agreed.
  Constraint on the setups: the human's carrying route crosses or approaches a normal robot route in some setups
  and stays clear in others, and the scenarios include both.
- Stage 2 has its own layout, setups and several scenarios. It is not a rerun of stage 1's scenarios.
- The gate opened on request: the gate has the state open or closed. The robot moves to the closed gate and
  honks. The honk makes the human's assigned task "open the gate" applicable: walk to a button on the wall
  beside the gate, press it. The human is not interrupted; it takes the task the next time it is free. While
  the gate is closed the robot has no applicable task and stands. No action closes the gate. The robot never
  opens it itself.
- The office door has a state. The agent that passes it opens it: one method for the open door, one that opens
  first.
- When a carried object does not belong to the new task, the agent first returns it to where it was picked up
  (kitting's rule, unchanged).

To rule before the build [open]:
- What the robot does when none of its tasks has an applicable method. Today the run stops with an error. Stage
  2 reaches this case at the closed gate.
- How a route is selected. Today a task's method is chosen by the kind of task and the pallet's state (a pallet's
  emptiness stands in for which side of the gate it comes from). The candidate: select the route from the area of
  the agent and the area of the object. store_pallet needs this settled.
- Where a pallet's origin is recorded when it is picked up.
- The observation rule. Stage 1 lets the robot observe every area from anywhere. The recorded rule for later is
  "monitored areas fixed per layout". Hadi reopened it: for him observation depends on where the robot is, and a
  robot that observes the whole hall from inside the truck is not realistic. Candidates: the robot observes its
  own area only, or its own area and every area behind an open passage. With it comes the decision on the human's
  disappearance and reappearance. Whether this is built inside stage 2 or as its own step after it is not
  decided.
- Choosing between two applicable methods by cost (TODO-16; the planner takes the first applicable method
  today). Ruled to be designed and built inside stage 2, "after the MPB's first run on dock_loading". That run
  took place in stage 1, so the recorded condition is already met. Where the work stands inside stage 2 is for
  Hadi to say when stage 2 opens. [open] Its case here: a delivery in one go
  (truck to bay) against a delivery in two steps (truck to gate, gate to bay). It changes the shared core and
  needs its own design question: how the candidates are formed, and whether the recognizer also considers
  several applicable methods.

Hadi's ideas and wishes for the stage [idea]:
- He wants the robot inside the truck to still know what the human does in the hall, to show intention
  recognition, and he also finds full observation unrealistic. He has said he does not know how to reconcile
  the two. (chat only)
- The task file of dock_loading looks very large and machine-written to him. He wants a task file that reads as
  written by a human: the knowledge stated once, the flat methods generated from it. Also: passages between
  areas as domain-independent knowledge. Not scheduled.
- Stage 2 is where the test sets go deep: controlled scenarios that each test one thing (seven to ten or more),
  then at most four or five mixed ones, drafted in one go by the design chat; the full instruments (expectations
  before the runs, declared properties, the alteration test).

---

## 7. After stage 2: the human outside the monitored areas ("track 4")

As recorded [ruled, with the observation rule reopened, see section 6]: the layout declares monitored areas (the
areas in which the robot observes the human). The robot's state of the world holds the human only while the human
is inside a monitored area. While no human is observed, the recognizer does not update, no projection exists, and
the planner plans as with no human. The disappearance and the reappearance each cause a new decision. The
reappearance starts a new episode from the prior base (the value with which the evidence restarts; the belief is
the prior multiplied by the evidence). The mind keeps no last observed position. dock_loading's office is the one unmonitored area. This step is built before the
evaluation, and the evaluation may use the office.

Open [open]: which trigger makes the decision at disappearance and reappearance (the trigger set has three
members today); the human leaving through a door.
Open [open] (3 October 2026): whether the robot's world state still holds the terminal fact of a task that the human
completed outside the monitored areas. If it does, the robot gets a recency fact for a completion it did not observe,
against AM27 and AM33.

Hadi's idea [idea]: the human vanishes into the office; the robot knows that the human is there and will appear
at the office door at some moment, without knowing when. A robot that expects the return and plans around it
belongs to belief-aware planning (TODO-97), outside this step.

---

## 8. Stage 3: check-in and check-out

As recorded [ruled in outline, design open]: separate from the gate mechanism. The human's place is the desk
beside the gate's button. The robot's place is a point just inside the gate, more than the minimum separation
away. Check-in: the two agents exchange the list of deliveries at the start. Check-out: the human signs at the
end to confirm that everything is delivered. Open: what "exchanging the list" means when the robot holds the
designations from the start.

Two optional items [open]: a deadline on the robot's waiting (the default is that the robot waits without
limit); a pallet in the truck that blocks another.

Not taken [ruled]: the robot moving to wherever the human is; a fixed order among the robot's tasks as its own
mechanism; an action of unknown length inside a plan; a rule that keeps the robot out of the delivery area
(Hadi: it contradicts the framework's claim of collaboration).

---

## 9. Outside V1 (future work; do not open)

- Tasks assigned to both agents, where each adjusts when the other has taken the object.
- A human that chooses its own tasks by a planner, in place of the author's priority list.
- The robot modelling a human who waits for the robot's own action.
- Several observed humans. Hadi's sketch: a second human with its own script that the robot has no model of,
  handled by the fallback projection.
- A position chosen when a pallet is put down (places inside a bay).
- A detour as the robot's response; execution in ROS.
- Communication acts stay under their existing records (TODO-96): the human assigning or changing a delivery
  location during the run; the robot informing a third party.
- Duration uncertainty and a projection that depends on context; unobservable states of the human as context; scopes of
  knowledge and norms; validation of the strengths on site data.
- A/C deactivation (TODO-163); several A/C switches in one layout (TODO-164). Added 3 October 2026 (T-K part 1's
  content points 1 and 2).
- The stream of context values with the world's dynamics [ruled]: T-K's later part, future work. It
  needs a model of the world's physics, and nothing that V1 claims depends on it.

Not future work [ruled]: a type-to-destination rule in place of explicit designations is recorded as not taken.
By the rule on V1 and future work, an alternative not taken in a design question is never a future-work item.

Also planned inside V1: T-K part 1 now (section 5), before T-G's stage 2; after T-G: the evaluation; the viewer; an interactive simulator in which deviations are
injected at run time; one further test track on adaptation under conflict. T-K part 2, the degrees of context facts (section
5.8), at the end of the V1 queue.

---

## 10. Housekeeping state and deferred items

- The records are split in two: docs/design_decisions.md holds the conceptual design of the shared core;
  docs/design_records.md holds everything else, one heading per task. New rulings go by their content. [ruled]
- Not done: rewriting each conceptual entry into one current rule. The conceptual file is still long because
  each entry carries its amendments. A list of passages that are false against the present code is kept in the
  record file as input. [open]
- Under analysis/, git tracks reports and code only. Data and figures stay on Hadi's disk, with a full copy
  outside the repo. [ruled]
- The housekeeping step after stage 1's close is done (2 October 2026): the sweep of old terms ("zone" to
  "area" in wording), the split of the records, and the rule for analysis/. The reports under analysis/ are
  readable in the design chat's project knowledge.
- Two large old items under docs/ wait for a destination that Hadi names: the old ROS planner reference text and
  the folder of old layout pictures. Deferred. [open]

---

## 11. How Hadi wants the work done (binds every reply)

- The design chat settles what and why. Claude Code builds and runs everything. Design before implementation;
  rulings are recorded before code.
- At the start of a chat: verify this file against the repo, report disagreements, show the zoomed-out plan
  (scope, steps, the questions to come) and wait for agreement.
- Design questions: one at a time. The problem in plain words, concrete cases, the alternatives, one
  recommendation, an explicit ask. Independent questions may share a message. A clarification is answered
  directly.
- Depth follows the kind of work. Design of the framework and of stage 2: full depth. Tests and housekeeping:
  light, one bounded prompt, a short report. Do not turn housekeeping into plan-then-build cycles.
- Language: the glossary's terms exactly; a missing term is proposed, not invented. Literal, short sentences. No
  figurative wording, no em dashes. A ruling's code is never written alone; its content is stated beside it.
- Engage critically. A settled decision can be reopened on design grounds, by Hadi's ruling.
- Scenarios and runs are tests. Nothing is adjusted to a result. A case that does not form in a scenario is
  recorded as absent, never engineered into existence. Findings are classified, not fitted.
- The core algorithms (the recognizer's scoring and admission, the meta-planner's evaluation and cost, the
  projection, the planner's method selection, the triggers) are not changed without Hadi's ruling.
- Prompts for Claude Code: the model and the session stated above the prompt; the step in the first line; what
  and why fixed, how left open; plain copiable text; one prompt at a time; commits on main, never a push.
  SUPERSEDED IN PART (Hadi, 4 October 2026, below): the model to use stands as the first line inside each prompt.
- Hadi reads recommendations quickly. A package ruled with one "ok" must state its consequential items
  separately and plainly.
- A stage whose subject is conceptual is first discussed as research: the concept, its terms and its
  alternatives, with no build steps, until Hadi rules. Hadi may bring reflections from another chat; the
  design chat takes from them what improves the decision and does not defend against them.
- Logic and knowledge-representation terms are used exactly: a fact holds, a condition is satisfied.
- Rules Hadi set on 3 October 2026 (also in CLAUDE.md, "How sessions work"):
  - Durations are shown in ticks, not in seconds or minutes.
  - A prompt for ccode states what is decided, its purpose and why it was ruled, and leaves to ccode which files and
    names are affected and how it checks its work. No micro-level instructions. SUPERSEDED IN PART (Hadi, 4 October
    2026; ccode's part, above): "ccode stays the worker: the decisions are fixed, and it is not asked for alternatives
    or opinions on them; it flags what the code contradicts" is replaced by ccode's part.
  - One ccode session, one concern. A follow-up goes to the session it belongs to.
  - Once a plan with numbered steps is agreed, replies keep those step numbers.
  - ccode's chat reports stay short: what was built, what it shows in plain words, what surprised, what it suggests.
    Detail goes into the repository's files.
- Rules Hadi set for the design chat on 4 October 2026 (the design chat on T-K part 1's build plan):
  - A decision is put in plain wording: what it is about, what the design says, the issue, what each option means,
    "in simple terms", one example, what the option does not change, a recommendation, an explicit question.
  - Simple decisions that match the design may be grouped in one reply, each with its kind and its consequence. A
    decision already ruled is not asked again. A decision where the design chat differs from ccode stays separate.
  - When explaining to Hadi, no document codes or numbering unless the content is beside them.
  - One ccode prompt per reply. The next prompt comes after the report of the previous one is reviewed and closed.
  - A ccode prompt states what is ruled and why as the fixed part, and invites ccode to check consequences, to
    cross-check, and to propose better ways. It lists no files and no sections.
  - ccode's part (Hadi, 4 October 2026; one wording replaces the rule of 3 October 2026 that ccode "is not asked for
    alternatives or opinions" and the invitation above to "propose better ways"): ccode decides how the approved design
    is built. On what is built and why, ccode may propose alternatives and raise objections, with reasons. ccode does
    not resolve a design question. Hadi rules what is built and why. Reason: Hadi decides the design, and ccode knows
    the code best, so its proposals and its doubts are wanted. (Also in CLAUDE.md, "How sessions work".)
  - The design chat states a fact about the repo only with the material in front of it, and says so when it has none.
  - The design is revised on arguments, never on a run's result. A surprising result is a finding to examine.
- Rule Hadi set on 4 October 2026 (also in CLAUDE.md, "Where to look"): a ruling that changes the method of context
  knowledge updates docs/context_knowledge_method.md in the same records step. ccode does not change the method itself;
  it flags a contradiction with its evidence, and Hadi rules. The records win where the two disagree.
- Rules Hadi set on 4 October 2026 (the design chat after step 5b):
  - A test or observation step needs no approval from Hadi. It runs on one model, with no pause between its stages.
  - A new ccode session per step.
  - When Hadi switches the model between stages, there is a pause at each stage boundary.
  - A test step is told what is of most interest. When it is a basic check, it is kept to a few scenarios.
  - The model to use stands as the first line inside each prompt.
  - An overview of parts, steps and stages is one nested tree. "Step" is the handoff's numbering; "stage" is the
    numbering inside a step.
  - In a design discussion the design chat writes literally, in the framework's terms, in short sentences with short
    examples. It gives no prompt and no task list unless asked.
  - A suggestion of the design chat is not a ruling. The design chat does not treat it as one until Hadi confirms it.
