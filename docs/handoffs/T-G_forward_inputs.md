# T-G: forward inputs for the stages after stage 1

Written 2 October 2026 by the design chat that closed T-G stage 1. Place: docs/handoffs/.
Corrected 2 October 2026 by the next design chat, after its verification against the repo's records.
Updated 3 October 2026 at the close of the design chat of stage 1.5 (section 5 rewritten; sections 2, 7, 9 and 11 amended).
Updated 3 October 2026 after the design chat on stage 1.5's content points 1 and 2 (section 5 brought to that state;
5.1, 5.2 and 5.5 corrected; section 2's last paragraph amended).
Updated 3 October 2026 after Hadi's rulings on ccode's report (AM30 to AM33: section 5 in line; section 9 gains
TODO-163 and TODO-164).

Purpose. This file is the single place a new design chat reads to know what lies ahead in T-G. It collects, per
stage, what is already ruled, what is open, what is parked, and the ideas Hadi stated. It replaces the reading of
the chain of earlier T-G handoffs. Those stay in the repo as history.

Status of this file. Informative. It decides nothing. Where it and the repo's records disagree, the records win.
Each item carries one of three marks:
- [ruled]: a ruling by Hadi that is recorded in the repo.
- [open]: a question recorded as open, or a proposal not ruled.
- [idea]: something Hadi said in a design chat. Some ideas are also in the records; those marked "chat only" are
  not, and no ruling rests on them.

Maintenance. The chat that closes a stage updates this file: it removes what the stage settled and adds what the
stage produced for later stages.

---

## 1. The project and the domain, in brief

TeamRob's framework is a robot cognitive architecture for working beside a human. The robot observes the human,
keeps a belief over what the human is doing (intention recognition), and chooses and times its own tasks so that
it does not come closer to the human than a minimum separation (adaptive planning). The framework's core is
domain-independent. Kitting was the first domain. T-G adds a second domain, dock_loading, to test that the core
stays domain-independent.

The chain of the robot's mind, in four parts:
1. The recognizer keeps a belief over hypotheses. A hypothesis is a task the human may be doing: one of the
   human's assigned tasks, or a foreseeable task (a break).
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
robot has delivered it. The human's foreseeable tasks: a coffee break (60 seconds) and an office break (90
seconds, at a chair inside the office). When no task is applicable, the human goes to a standby place in the
middle of the hall. At the end the human goes to a desk beside the gate.

The room has three areas: the truck side, the hall, the office. The gate separates the truck side from the hall.
The office door separates the hall from the office.

---

## 2. Where T-G stands

The staging, as recorded: stage 1, stage 1.5, stage 2, then "track 4", then stage 3. All are inside V1, the first
complete version of the framework.

Stage 1 is closed (2 October 2026). What it delivered:
- Five framework-wide mechanisms, each built with kitting's outputs unchanged byte for byte:
  the rename of "zone" to "area"; the agent's area carried in computed states; a hypothesis is live only while one
  of its methods is applicable; object states and designations declared by the domain; the human's script as a
  priority list.
- dock_loading's tasks, three rooms without stores, and three kinds of setup (a fourth, "one bay", is named as conditional and not built).
- An intention-recognition test set (the IR test-bed): 54 runs with an idle robot, zero disagreements with the
  expectations written before the runs.
- A recognition-to-planning test set (the MPB, the meta-planner test-bed): 52 runs with a working robot in two
  rooms, all completed, zero disagreements where full expectations existed (40 runs). This result does not state
  that the runs are free of violations of the minimum separation (section 4).

Scope of stage 1's tests, as Hadi set it [ruled]: they are an initial check that dock_loading works. The deeper
behavioural analysis belongs to stage 2. Hadi wants stage 2's questions, rulings and discussion taken in full
depth, one at a time.

Stage 1.5 was taken next. Its design is ruled and recorded (2 and 3 October 2026). Its build has not
started. Section 5 holds its state. Its content points 1 (the values) and 2 (the perception assumption) are ruled
(3 October 2026); content point 3 (the tests) is open.

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

Recognition on dock_loading (the IR test-bed, 54 runs):
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
  by an undeclared weight (the hardcoded context weight multiplies coffee_break by 2.5 from step 500); the IR
  test-bed's figures are not affected. design_records.md, "T-G stage 1", SCOPE REDUCED AND THE MPB ON DOCK_LOADING RUN,
  its CAVEAT.

Not tested in stage 1: env_layout_02 in the MPB (the room with the latest admissions, median 28 ticks); the test
that alters one rule of the oracle to show that a zero result is a detection (built for dock_loading, not run); a
setup in which all pallets go to one bay (recorded as conditional, never needed).

---

## 5. Stage 1.5: context knowledge (framework-wide: kitting and dock_loading)

State on 3 October 2026: the design is ruled and recorded. Nothing is built. Three content points are
open and come before the build (5.4).
UPDATED (3 October 2026, after the design chat on content points 1 and 2): content points 1 (the values) and 2 (the
perception assumption) are ruled and recorded, AM10 to AM29 (the chat's A1 to A15 are AM10 to AM24, its B1 to B5 are
AM25 to AM29). Content point 3 (the tests) is open. Nothing is built. Records: the entry below, its block CONTENT
POINTS 1 AND 2; docs/design_records.md, "T-G stage 1.5", CONTENT POINTS 1 AND 2; docs/glossary.md §5 (recency fact,
recency duration, occurrence condition as amended); docs/assumptions.md 5.4, 6.1 to 6.3; TODO-163, TODO-164 [FW].
UPDATED (3 October 2026, Hadi's rulings on ccode's report): AM30 to AM33 (5.1 and 5.2 below) and three notes for the
build's plan (5.2).
Records: docs/design_decisions.md, the entry "T-G stage 1.5: context knowledge in the recognizer's
belief" (rulings R1 to R8, assumptions A1 to A7, amendments AM1 to AM9, corrections C1, C3 and C4). Correction
C2, the caveat on the long runs, stands in docs/design_records.md under "T-G stage 1", in TODO-66 and in the MPB
report. docs/design_records.md, the heading "T-G stage 1.5" (the cut, T-K, the open items, the build's list).
Where this section and those records disagree, the records win.

### 5.1 The design in plain words [ruled]

- Context knowledge acts in the robot's mind only, in the recognizer's belief. It does not drive the
  human. It starts no task and interrupts no task of the human. A script may be authored to agree with
  it for a test; that is test authoring.
- Conditions of tasks stay in the task model. They decide which hypotheses are live. They are not
  context knowledge.
- The belief. At each run of the recognizer, the belief is the prior multiplied by the evidence, then
  normalised over the live hypotheses. The prior is evaluated on the context facts that hold at the
  present tick. The evidence is the likelihood accumulated in the present episode (movement, standing and
  completion events), with no context in it. The prior enters once and is never folded into the evidence. Adequacy and warrant do not read
  the prior. The rules on re-entry and on the episode boundary describe the evidence (it restarts equal;
  a returning hypothesis takes 1/|H| of it).
  CORRECTED (3 October 2026): the parenthesis "(movement, standing and completion events)" is confirmed in the code
  (`shared/recognizer.py`: the walking and standing evidence per phase and the completion events of an episode) and is
  not in the ruling's text (R2 says "the likelihood accumulated in the present episode").
- The prior. It is the normalisation of the strengths of what is live. The human's work as a whole
  contributes 1 while a work-task hypothesis is live. Work as a whole is the live hypotheses of work
  tasks in the support; with assignment knowledge on, these are the live assigned tasks. Its share is
  divided equally among those hypotheses. Each live foreseeable task contributes its declared strength,
  divided equally among that task's live hypotheses.
- A strength is the declared relative weight of a foreseeable task against the human's work as a whole.
  A foreseeable task declares a low strength (its occurrence condition is not satisfied) and a high
  strength (it is satisfied). A foreseeable task with no occurrence condition declares one strength.
  Every strength is greater than zero and carries its source. It is a modelling assumption until a site
  measures it. Proposed meaning, not claimed: a ratio of counted task starts.
- An occurrence condition is the condition over context facts attached to a foreseeable task. In stage
  1.5 it is one context fact or a conjunction of context facts.
  SUPERSEDED IN PART (AM11, 3 October 2026): it reads facts from three sources (a context fact authored as a window
  on the scenario's timeline, an object state, a recency fact) and uses "and" and "not". "Or" stays in T-K. With it
  not satisfied, the foreseeable task has its low strength and stays live (AM12).
- A context fact is a declared fact derived from context values (the clock time, the temperature). In
  stage 1.5 it is crisp: it holds or it does not hold.
  ADDED (AM10, AM14, AM20, AM21, 3 October 2026): every fact of stage 1.5 is crisp (AM10). A timeline fact is a
  state: an entry of the timeline is the change, the fact holds until the next change, and the change is no trigger
  of the meta-planner (AM21). No action sets or removes a context fact (AM20). A recency fact is a context fact
  derived from the time since the robot observed completion of a named task; it holds for the task's recency
  duration after that observation; it is declared per task (AM14).
  AMENDED (AM30 to AM33, 3 October 2026): the robot may measure a context value from its own observation, for example
  the time since an observed completion, so a recency fact is a context fact by the existing definition (AM31). The
  rule on actions reads: no action's declared effect sets or removes a context fact in the world; a recency fact
  changes through the robot's observation of a completion, in the mind (AM32). An observed completion is the task's
  terminal fact in the robot's world state, for example waited(agent, machine), not the episode boundary (AM33). The
  memory of observed completions is its own component of the robot's mind, outside the recognizer; it records the
  tick of an observed completion; the recognizer reads the recency facts as an input on each run and stores nothing
  across episodes (AM30).
- The values [ruled, 3 October 2026; AM13 to AM18]: coffee_break (both domains): break_time and not recent, strengths
  low 0.02, high 3, recency duration 3 minutes (90 ticks). ac_activation (both domains): room_warm and not ac_on,
  strengths low 0.005, high 0.2, no recency fact. office_break (dock_loading): not recent, strengths low 0.005, high
  0.02, recency duration 4.5 minutes (135 ticks). Each strength's source: "Modelling assumption, Hadi, 3 October 2026.
  A relative strength. Its order of magnitude is motivated by the proposed meaning of a strength (a ratio of counted
  task starts), which is not validated." An A/C switch is an object with the state ac_on, which ac_activation sets;
  at most one per layout in V1; none in dock_loading's three existing rooms.
- The long-shift rule leaves at the build with no replacement in stage 1.5: the robot's expectation of coffee_break
  does not rise with the duration of work, a stated limitation until T-K [ruled, AM22].
- Two independent run options, both on by default from the build (today assignment_prior defaults to off):
  assignment_knowledge (today's assignment_prior) and context_knowledge (new). With context_knowledge off the prior is equal over the live hypotheses. Each
  "off" is an ablation or a diagnostic.
- Gate policy, no change to the gate: an assigned task may be admitted before any distinguishing
  movement, on its commitment warrant. The prior is the robot's expectation, not evidence that the human
  has started. Adequacy tests the hypothesis afterwards and can cause the retraction. A foreseeable task
  still needs observation warrant.
- A task keeps one declared duration. Context does not change the content of a projection. The only
  path from context to the projection is: prior, belief, gate, projection of the admitted task.
- The earlier decision "Assigned-task pool is a support restriction, not a prior" is revised in part:
  the assignment still restricts the support and sets no weight; declared strengths replace unit weight
  between work as a whole and the foreseeable tasks.
- Superseded for this stage by these rulings: Hadi's earlier sketch in which a context fact triggers a foreseeable task
  of the human or interrupts a task in progress.

### 5.2 What the build of stage 1.5 contains [ruled]

- The prior as in 5.1, with crisp context facts.
- A timeline of context facts in the scenario: a fact changes at an authored tick [ruled]. How the
  fact reaches the recognizer is not ruled; it depends on open item 2. The design chat's sketch
  [chat only]: the environment applies it, the robot's world state carries it, the recognizer reads
  it there.
- The declarations of context knowledge per domain: the context facts, and per foreseeable task its
  occurrence condition and its strengths. [implied by the rulings on the strengths; the values are open item 1]
- The two run options, their names and their defaults.
- The removal of the two domain task names and the four constants from the recognizer (TODO-66). The
  present hardcoded weight multiplies coffee_break by 2.5 from step 500 in every run (found on 3 October
  2026; see the caveat in section 4).
CORRECTED AND ADDED (3 October 2026, after the design chat on content points 1 and 2) [ruled]:
- The path of a timeline fact is ruled (AM25): the environment applies the timeline, the robot's world state carries
  the facts, the recognizer reads them there. The robot knows which timeline facts hold, exactly and at once; no
  sensing is modelled. The "[chat only]" sketch above is now the ruling.
- The declared context knowledge (the facts that exist, the occurrence conditions, the strengths, the recency
  durations) reaches the mind directly from the knowledge component, as the task model does (AM26). The build also
  replaces the class `ContextKnowledge` in `shared/knowledge.py`, as the glossary says (§5, context knowledge).
- The declarations' values are ruled (5.1, the values; AM13 to AM18).
- "Not" in an occurrence condition and its three sources: timeline facts, object states, recency facts (AM11).
- The recency facts: per task, each from the mind's own memory of an observed completion; completion counts, not
  admission; a completion the robot does not observe, or a task cut before its completion, produces none (AM14, AM27).
  AMENDED (AM30, AM33, 3 October 2026): the memory is its own component of the robot's mind, outside the recognizer,
  recording the tick of an observed completion; an observed completion is the task's terminal fact in the robot's
  world state.
- The A/C switch's object state ac_on, set by ac_activation; ac_activation and room_warm in the task model and the
  context knowledge of both domains (AM18).
- Before the build, in its own step: the layouts with more than one A/C switch are changed to the V1 rule (at most
  one per layout). ccode first lists every such layout and every scenario, test and analysis that rests on it; Hadi
  decides on that list. Order: the list, the layout change, the regeneration of the baselines that remain, then the
  build (AM19).
- Notes for the build's plan [confirmed by Hadi, 3 October 2026; design_records.md, "T-G stage 1.5", NOTES FOR THE
  BUILD'S PLAN]: "not" needs a condition form of its own, which ccode proposes in the plan; ac_on needs a declared
  state and a declared effect of the action, and dock_loading needs the object type and the task ac_activation; the
  recency durations are declared in physical time and converted by the body.

### 5.3 What is not in stage 1.5

- T-K, a new task at the end of the V1 queue [ruled]: degrees. A context fact satisfied to a degree
  between 0 and 1; a membership function that gives the degree from a context value; minimum for "and",
  maximum for "or", 1 minus the degree for "not"; the strength linear in the degree between low and
  high. The design is ruled; the representation of a context value and of a degree is open.
- T-G stage 2 [open]: whether succession between tasks affects the division inside work as a whole, to
  be argued with store_pallet present.
- Not taken, and not future work [ruled]: a preference for a task that has just become applicable.
- Under TODO-155 [open, parked, V1, no stage]: the walk to the standby place and the walk to the desk
  have no hypothesis. Recorded there as not taken for this stage: a share for "none of the modelled
  tasks"; it would reopen the decision that the belief has no residual hypothesis. With no work-task
  hypothesis live, the prior is conditional on one of the modelled foreseeable tasks.
- Future work [ruled]: see section 9.
- Still open and outside this stage: whether a hypothesis stays live when its method's condition turns
  false while the human is doing the task.

### 5.4 Open before the build: three content points [open]

Each is put to Hadi one at a time. None is decided.
UPDATED (3 October 2026): items 1 and 2 are RULED (AM10 to AM29); item 3 stays open.

1. RULED (3 October 2026; AM10 to AM24; 5.1, the values; design_records.md, "T-G stage 1.5", CONTENT POINTS 1 AND
   2). The text below is the question as it stood.
   The values for kitting and dock_loading: which context facts exist; the occurrence condition of each
   foreseeable task; its low and high strength; the source of each value.
   Hadi's examples from the design chat [chat only, not values]:
   - Coffee break: the human takes it at the fixed break time, or after long work without a break.
     "Tired" is not a fact, because the robot cannot observe it; "long work without a break" is,
     because it rests on values. The "or" needs T-K, or the two are authored as one fact.
   - Break time with soft edges: 9:15 to 9:30 partly, 9:30 to 10:00 fully, 10:00 to 10:15 partly. The
     soft edges need T-K; in stage 1.5 the fact is crisp.
   - A/C: the temperature rises near 25 degrees, the room is warmer than it should be, and turning on
     the A/C is likely. Turning on the A/C changes the temperature: in this stage an action may
     change a context value and never sets or removes a context fact directly.
   - The numbers used in the design chat's examples (coffee break 0.05 and 3, office break 0.05, A/C
     0.01 and 0.5) were illustrations only.
   SUPERSEDED (3 October 2026): the examples above are history. The ruled values are in 5.1. "Or" and "long work
   without a break" are T-K's open items (not ruled); the soft edges are T-K's (AM10); in stage 1.5 no action sets or
   removes a context fact (AM20), and the A/C's activation acts through the object state ac_on (AM18).
2. RULED (3 October 2026; AM25 to AM27; 5.2, the path of a fact; docs/assumptions.md 5.4). The text below is the
   question as it stood.
   The perception assumption: how the robot obtains a context value. The existing assumption for object
   states (the robot knows them through the site's system) is the likely model. Nothing is written.
3. OPEN. The tests of the stage: a script that agrees with an occurrence condition; a human who acts against
   it; a duration mismatch (the human's actual duration differs from the robot's declared one).
   Recorded with it (AM29, ccode's check, 3 October 2026): a shorter wait is authorable (during wait_at, drop; 46
   seconds, since 45 cannot be written at 2 seconds per tick; the entry closes as abandoned); a longer wait is
   authorable (during wait_at, a Start of stand). Neither is authorable when the coffee break is itself the task of
   another entry's event (the stack is one level deep, TODO-100): that case is recorded as absent.

Also open, Hadi's choice [chat only; the records say only that A1 to A7 are not added to
docs/assumptions.md]: whether A1 (given the task, the movement does not depend on the context), A5
(the declared and the actual duration match) and possibly A4 go into that file. ccode's view, stated
in a report and not recorded: A1 and A5 belong there.
RULED (AM28, 3 October 2026): A1 and A5 are in docs/assumptions.md (6.1 and 6.2; A5 as a baseline whose violation is
a deviation that the existing chain handles); A4 stays in the design record only (it is about strength values at real
sites, not about the per-domain declaration). Also added: 5.4, the perception entry (AM25, AM27), and 6.3, the
declared durations at a compressed demonstration scale, not calibrated (AM23).

### 5.5 What the build must respect [recorded, with two chat-only items]

- The stage is framework-wide: it concerns kitting and dock_loading alike [recorded]. The build's
  acceptance includes kitting [chat only].
- With both options on, every existing run with assignment knowledge on changes, also with no context
  fact declared: each foreseeable task has its declared strength (its low strength, or its one strength
  when it has no occurrence condition) in place of an equal share [chat only: the design chat's statement
  of this consequence].
  CORRECTED (3 October 2026; AM24, ruled): with context_knowledge on, runs with assignment_knowledge off change too.
- The build's acceptance [ruled, AM24]: "identical except for the lines the build names", with the regression audit.
  Reason: the rename of the run option changes the run header in every log.
- Every existing baseline set and test either states context_knowledge off to stay identical, or is
  regenerated with the reason stated, with the regression audit CLAUDE.md requires. Runs of 500 steps or
  more change even with context_knowledge off, because the hardcoded weight leaves.
- The renames (assignment_prior to assignment_knowledge; the context weight; prior base) and the default
  changes belong to the build. docs/assumptions.md 1.4 is updated there.
- The recognizer is a core algorithm. The change is domain-independent and ruled. The build touches
  nothing else of the core at the conceptual level without asking.
- ccode works in two steps: a plan with no code, confirmed in the design chat, then the build.

### 5.6 The steps from here

1. The three content points, one at a time.
2. The records of their rulings.
3. ccode's plan for the build, reviewed in the design chat.
4. The build, its verification, and the review.
5. The re-measurement of stage 1's baseline with context knowledge on (section 4's figures were measured
   with the equal prior).
6. The close of stage 1.5, with this file updated. Then stage 2 (section 6).

UPDATED (3 October 2026): steps 1 and 2 are done for content points 1 and 2. From here:

1. Content point 3 (the tests), then the records of its ruling.
2. ccode's list of the layouts with more than one A/C switch and of every scenario, test and analysis that rests on
   them (AM19); Hadi decides on the list.
3. The layout change, then the regeneration of the baselines that remain (AM19).
4. ccode's plan for the build, reviewed in the design chat.
5. The build, its verification (AM24) and the review.
6. The re-measurement of stage 1's baseline with context knowledge on. Open at this step: whether the 22 potentially
   confounded MPB runs (section 4's caveat) are rerun then or in stage 2.
7. The close of stage 1.5, with this file updated. Then stage 2 (section 6).

### 5.7 Background from the design chat [chat only]

- The reason for the form of the prior: the literature puts context in the prior (Pynadath and Wellman
  1995; Kelley et al. 2012; CoBaIR, Lubitz et al. 2023). The hierarchy follows the idea of a nested
  choice model; the form is a hierarchical prior with declared relative strengths and inherits none of
  that model's further assumptions. These references may serve the paper.
- Discussed and not held: kinds of knowledge by force (a strict constraint, a norm, a habit) and by
  scope (general, sector or organisation, domain or site). The principle that was held and ruled: only
  a condition of the task model removes a hypothesis; context only changes how probable a live
  hypothesis is.
- A consequence of the ruled prior, stated as a consequence and not as its reason: with one assigned
  task live and the foreseeable tasks at low strength, the assigned task starts near the threshold or
  above it. This bears on the finding that the robot does not anticipate the scan its own delivery
  enables (TODO-154).

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
- A/C deactivation (TODO-163); several A/C switches in one layout (TODO-164). Added 3 October 2026 (stage 1.5's
  content points 1 and 2).

Not future work [ruled]: a type-to-destination rule in place of explicit designations is recorded as not taken.
By the rule on V1 and future work, an alternative not taken in a design question is never a future-work item.

Also planned inside V1, after T-G: the evaluation; the viewer; an interactive simulator in which deviations are
injected at run time; one further test track on adaptation under conflict. T-K, the degrees of context facts (section
5.3), at the end of the V1 queue.

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
- Hadi reads recommendations quickly. A package ruled with one "ok" must state its consequential items
  separately and plainly.
- A stage whose subject is conceptual is first discussed as research: the concept, its terms and its
  alternatives, with no build steps, until Hadi rules. Hadi may bring reflections from another chat; the
  design chat takes from them what improves the decision and does not defend against them.
- Logic and knowledge-representation terms are used exactly: a fact holds, a condition is satisfied.
