# Framework assumptions and authoring conventions

Ruled by Hadi, 28 September 2026 (cchat, Track 2.5); recorded 29 September 2026. The terms are the glossary's
(`docs/glossary.md`); where one is used, its plain meaning is written beside it once.

Why. The maintained baseline logs held situations the framework does not mean to cover (a human standing at the shared
table to the run's end, prior-off artefacts, fixed step counts), and effort went into them. A case met in a run is
first classified, then handled by its class:
- an **intended phenomenon** (the framework means to cover it): design it;
- a **boundary** (outside what the framework claims): record it;
- an **authoring artefact** (the fixture produces a situation its purpose does not include): correct the fixture;
- a **prior-off artefact** (it arises only with the assignment prior off): never framework semantics, never a rule.

A boundary case's fixture is parked (kept out of the maintained sets, or moved to a reserved id range: layouts and
setups numbered 100 and above), never designed around. Ruled by Hadi, 29 Sept 2026 (design_decisions.md, "T-D G:
admission").

Simplification comes from general semantics, never from excluding difficult cases.

Each item: the statement; then kind · source · what it affects; at most two lines of detail. Kinds: authoring
convention, framework scope, simulator convention, perception.

## 1. Authoring

**1.1** Baseline human scripts end with the human leaving the shared workspace after completing its assigned tasks
(the **exit walk**: the script's last entry, a `go_to` to a landmark, the layout's symbolic place), unless the
scenario explicitly studies post-completion behaviour and its description says so (label C, the scenario's
**purpose**: what the scenario is for, stated in its description). Existing regression fixtures are corrected likewise
where their terminal stand is not part of the fixture's purpose.
Authoring convention · T-C2c, extended (Hadi, 28 Sept 2026) · every human script; the six fixtures corrected in
Track 2.5 (scenario_s01_01, s01_06, s02_01, s03_01, s04_01, s06_03), each ending with `go_to("corner_SE")`.
Supersedes T-C2c's "new scenarios follow the convention" and T-D P's "the scripts are not edited". In Mesa leaving is a
walk to a landmark inside the workspace, the human still observed (2.3).
READS FOR DOCK_LOADING (T-G B13, Hadi, 1 October 2026): the script ends with the walk to the desk, the one entry of its
closing part (A3, Q14); no exit from the room is defined for dock_loading now. Kitting is unchanged.
design_decisions.md, "T-G: the second domain's rulings", A3, B13.
NOTE (T-G records 3, 1 October 2026; not a ruling): the exit walk is defined as "the script's last entry"; where a
script has a closing part it reads "the last closing entry". Stage 1's plan carries the consequence for the code.
NOTE (T-G stage 1's plan, approved by Hadi, 1 October 2026; design_decisions.md, "T-G: the second domain's rulings",
STAGE 1 PLAN APPROVED): in the IRB setup (B14, kind 1) the case with the assigned scan of the pallet in the truck
is declared dependent on the robot; its priority list never finishes, so that run has no walk to the desk.

**1.2** Every baseline script declares its experimental intent (label C, purpose); **unmodelled behaviour** (behaviour
no hypothesis of the robot's hypothesis space describes, label B) appears only where the description says so.
Authoring convention · the terms ruling of 24 Sept 2026 (labels A, B, C), TODO-80 · scenario descriptions; the
label-C check (the exit walk is exempt, glossary §7).
NOTE (T-G stage 1's plan, approved by Hadi, 1 October 2026; design_decisions.md, "T-G: the second domain's rulings",
STAGE 1 PLAN APPROVED): the walk to the standby place has no hypothesis in the robot's task model, so a dock_loading
scenario with a standby entry contains unmodelled behaviour, and its purpose says so. Parked for after the milestone, not
ruled: whether the robot's mind holds a hypothesis for the human stepping aside.

**1.3** For human-script and test-bed runs (the robot has no work of its own), a run's step count is derived from the
human's load-time replay plus the idle margin (the replay's last acknowledgement tick + 1 + 30 ticks of the idle
human), not a literal. The horizon of runs where the robot has work is open; the maintained baseline sets keep their
step counts.
Authoring convention · IRB.3b's rule (`analysis/irb/run.sh`) · run files, sweep scripts.
The replay has no term for the robot's work, which in the maintained sets ends after the human's (TODO-138).
Ruled for MPB runs (Hadi, 29 Sept 2026; design_decisions.md, "The meta-planner test-bed (MPB)", MPB-5): the comparison
horizon is the first observed completion point plus the idle margin, under a derived plain-cost safety cap; the
maintained sets keep their literal step counts.

**1.4** The framework's experiments use the prior-on configuration (the robot knows the human's assigned tasks,
`--assignment_prior true`). Prior off is a recognizer diagnostic and ablation configuration, not a human-behaviour
scenario; an artefact produced only under prior off is not a framework scope case and never produces a rule.
Framework scope · CLAUDE.md's prior convention, revised (Hadi, 28 Sept 2026) · where findings are drawn from; the
maintained sets still run both priors.
The run option's default is still off (`configs/experiment.yaml`); not changed here (TODO-139).
BUILT (T-K part 1's build, 4 October 2026; AM3, AM9; design_records.md, "T-K", THE BUILD): the option is
`assignment_knowledge` (`--assignment_knowledge`; `assignment_prior` was its old name) and is on by default, beside the
new option `context_knowledge`, also on by default; each "off" is an ablation or a diagnostic (glossary §5, the run
options). "Prior on" and "prior off" in the older records mean assignment knowledge on and off. TODO-139 closed.

## 2. The team and the task world

**2.2** All agents know the full set of tasks and the initial allocation (which agent is assigned which tasks). A
delivery of an unassigned item is a boundary case.
Framework scope · the AAAI paper · the hypothesis space and the support restriction (the assigned tasks plus the
foreseeable tasks); scenario_s09_09 is the boundary case.
The allocation is not the order: the robot never reads the human's script.

**2.3** Humans may enter or leave the shared workspace; robots stay. "No human observed" is a normal state; a
returning human is a new observation.
Framework scope · the AAAI paper · perception; the fallback projection.
Not in the Mesa body: the human never leaves (the exit walk ends inside the workspace, the human observed). The one
place the code handles no observed human is T-D P's boundary condition (no fallback); the recognizer has no path for it.
Ruled, not built (T-G A8, Hadi, 1 Oct 2026; track 4's reduced form, after T-G's stage 2): the layout declares monitored
areas; outside every one the robot's WorldState holds no human, the recognizer does not update, no human projection
exists; disappearance and reappearance each cause a new decision, the reappearance a new episode from the prior base.

**2.4** The human executes one task at a time; a switch (a `Start` event) suspends the current task, a `Drop` ends it.
Framework scope · T-H's stack (one level deep) · the human executor and its record.

**2.5** The human carries one item at a time.
Framework scope · the executor's holding · the decompositions (`deliver_with_return` returns the held item first).

**2.6** In baseline the human does not repeat a completed assigned task and does not move an item after delivering it.
A delivery hypothesis re-entering the live set because its item moved (T-D L4) is a boundary case.
Framework scope · Hadi, 28 Sept 2026 · L4's re-entry; TODO-128.

## 3. Changes of intention

**3.2** A change of mind between two assigned deliveries is a normal in-scope case.
Framework scope · T-C1, T-H · scenario_s09_07.

**3.3** In baseline the human makes at most one **deviation** (a node of the human's realised plan tree that the
robot's tree does not contain: here, a departure from the task as the robot's model decomposes it) per task instance,
and resumes the task afterwards; chains of deviations are boundary cases.
Framework scope · Hadi, 28 Sept 2026 · human scripts.

**3.4** A stand inside a task is a pause while it lies within the standing the task's current **derived phase** (the
action the hypothesis expects now) prices (s_exp; T-D R and E, E9, E10). Beyond that the phase does not fit, and if no
other live hypothesis fits, the **adequacy finding** is **unexplained** (evidence that no live task hypothesis explains
the observations). Standing contributes no hypothesis-specific evidence while the live hypotheses price the standing
equally; any movement of the probabilities is a consequence of the evidence function and the normalisation, not
evidence that one hypothesis explains the stand better than another; the probabilities are not claimed invariant. No
stay hypothesis is introduced; P4's **fallback projection** (the short-term physical projection from what was observed)
carries an observed stand.
General semantics · Hadi, 28 Sept 2026 · the recognizer (no change); TODO-95 closed, its open levels to X and
TODO-132 (b).
Measured, scenario_s09_06 over its stand (ticks 30 to 69): deliver_item(item_1) 0.8608 to 0.9184, coffee_break 0.1373
to 0.0796 (the evidence L(v·D) is logistic in D, so an equal added standing moves the ratios until its tail).

## 4. Interaction and execution

**4.2** The scripted human is open-loop: it does not react to the robot's motion.
Framework scope · T-C1; the Mesa human has no avoidance · the human executor.
It reads what the robot does to objects (T-H2 D3, TODO-105: a resumed fetch walk goes to where the item now is).
Future work: a reactive human that gives the robot space (TODO-136).

**4.4** Execution-time residuals (the robot's motion past the human projection's end T_h, or under a projection built
on little evidence, P4's recorded error) are not the planner's to remove. Evaluation measures their outcome as
near-encounters (4.6); the body's separation stop is the demonstration and safety mechanism against them.
Framework scope · "Assumption: execution-time avoidance past T_h" (R1); C, the separation stop · realization's
assessed window; the stop, a run option.

**4.5** In Mesa agents are points and may overlap; an overlap is a simulator representation, not a framework
collision event.
Simulator convention · Hadi, 28 Sept 2026 · `[sep]`; F1's classes.

**4.6** Near-encounters (ticks at which the robot–human distance is below `min_separation`; not a glossary term) are an
evaluation measure of the planner, classified per F1 (a robot violation, a stand, a recede;
`analysis/f1_robot_responsible/evaluate.py`), compared between the IR planner (realized cost) and the no-IR planner
(plain cost, and the fallback-only control), not a condition the simulator must prevent. The execution stop is a run
option for demonstrations, off for evaluation. Scenarios in which the human walks toward the robot stay in scope as
evaluation cases for the communication question (X).
Framework scope · Hadi, 28 Sept 2026, reframing F1's stance (F1 stays the safety record) · the maintained sets'
"2.5" sections (the `[sep]` minimum and F1's class counts per run).
The fallback-only control is no run option today (TODO-137); the evaluation scenario is TODO-135 (its first
instance: scenario_s01_06, the exit walk through the holding robot, 5.23 cm at 147, stands and a recede).
The evaluation's framing (the conditions, the measures, the scenario dimension; not ruled): TODO-144.

## 5. Perception

**5.1** The robot senses the human's position, grasps, releases and standing exactly and on every tick, with one tick
of latency: the human projection starts at the observation offset ("Projection time includes what the body spends
finishing an action, and the human's projection starts when it was observed", L2 of the Phase 4 records; not T-D L's
L2). Numerical resolution is the body's (P4's "same direction" within 1e-9).
Perception · the AAAI paper; L2 · the recognizer's input; the projection's start.

**5.2** One observed human, for the current contribution.
Perception · the world-state builder (one observed human per robot) · the recognizer; the fallback projection.
Several observed humans (a passing colleague, a colleague talking to the observed human) are an FW direction (T-G A10;
TODO-150).

**5.3** The robot knows the states of objects, including which pallets are scanned, through the site's system: a scan is
a digital act written to that system at once. Its knowledge of objects does not depend on where the human is (T-G A8).
Perception · Hadi, 1 Oct 2026 (T-G A6) · the robot's WorldState (object states, T-G A5); dock_loading's scan.
The simulated robot reads the environment's true states through its body; no observation of the scan is modelled.

**5.4** The robot knows which facts of the scenario's timeline of context facts hold, exactly and at once; no sensing
is modelled. The justification is the site's system (clock, schedule, temperature sensor), as for object states (5.3).
The facts reach the robot's mind through the world state: the environment applies the timeline, the world state
carries the facts, the recognizer reads them there. A **recency fact** (glossary §5) rests on the mind's own memory of
an observed completion: the world state holds no history, and the mind does not read the simulator's record of the
human. A completion the robot does not observe produces no recency fact (a limit once the human can be outside the
monitored areas, 2.3); a task cut before its completion produces none.
Perception · Hadi, 3 Oct 2026 (T-K part 1, AM25, AM27; placed here by AM28) · the robot's WorldState; the
recognizer's prior. Ruled, not built.
BUILT (T-K part 1's build, 4 October 2026; design_records.md, "T-K", THE BUILD): the timeline in force is resolved at
load (the scenario's, else the setup's, else none) and read as a function of the tick by the world-state builder; the
memory of observed completions is `shared/completion_memory.py`, read by the robot's body before the recognizer runs.
AMENDED (AM30, AM33, Hadi, 3 Oct 2026): the memory is its own component of the robot's mind, outside the recognizer,
and records the tick of an observed completion; an observed completion is the task's terminal fact in the robot's
WorldState (for example waited(agent, machine)), not the episode boundary.
AMENDED (AM34, Hadi, 3 Oct 2026): the timeline of context facts is the setup's, not the scenario's.

## 6. Context knowledge

Ruled by Hadi, 3 October 2026 (T-K part 1, AM28; design_decisions.md, "T-K: context knowledge in the
recognizer's belief"). Not built.
BUILT (T-K part 1's build, 4 October 2026; design_records.md, "T-K", THE BUILD): the mechanism these assumptions
stand under is built; the assumptions themselves are unchanged.

**6.1** Given the task, the human's movement does not depend on the context.
Framework scope · T-K part 1, its assumption A1 (placed here by AM28) · the recognizer's evidence, which contains no
context (R2).

**6.2** The robot's declared duration of a task and the human's actual duration match. This is a baseline: a violation
is a deviation that the existing chain handles.
Framework scope · T-K part 1, its assumption A5 (placed here by AM28); "The human's wait duration in the projection
is the schema's, converted by the body (TODO-32, R2)" · the projection; the stage's tests (a duration mismatch).

**6.3** The durations declared in the domains (the waits of the foreseeable tasks, the recency durations) are at a
compressed demonstration scale and are not calibrated.
Simulator convention · Hadi, 3 Oct 2026 (T-K part 1, AM23) · the domains' task schemas and context knowledge.

**6.4** An admission of a hypothesis that is not the true task, read against the evidence alone. The evidence alone is
the belief of the run with context knowledge off of the same script (the equal prior); the ratio is the true task's
belief over the admitted hypothesis's belief in that run. Such an admission has two parts.
- First part. In the first ticks of a walk the evidence for two targets is nearly equal. Where two targets lie close
  (the coffee machine beside a shelf; the A/C switch beside shelf_4), the movement of these ticks hardly separates
  them, and the declared context makes one of them probable: the robot admits that one, and the human may do the
  other. Measured: 18 ticks, the ratio within ×1.01 of 1, the smallest ×1.0008; no tick is an exact tie (equal within
  1e-9). Only this part is a limit of the situation. A careful observer with the same knowledge could make the same
  guess, and no rule inside recognition removes it, because the information that would separate the two tasks does
  not exist yet. It is the stated meaning of the threshold: at θ = 0.75 the robot accepts that an admitted hypothesis
  can be other than what the human does.
- Second part. After the first ticks the evidence ranks the true task first, weakly at first and by a ratio of about
  3 to 14 at the end of the walk, and the prior overrules it while the admission stands. Measured: 293 ticks. In the
  long admissions (a lone delivery admitted while the human walks to a coffee break or to the A/C switch) the ratio on
  the first wrong tick and on the last: ×1.0008 and ×13.7 (scenario_s14_19), ×1.0092 and ×12.7 (s13_13), ×1.0015 and
  ×3.05 (s15_19, the A/C beside shelf_4), ×1.048 and ×13.6 (s08_02), ×1.06 and ×14.2 (s09_11). In a short one, the
  coffee break under break_time during the walk to the neighbouring shelf: ×1.22 and ×1.71 (s13_11, _12, _14). This
  part follows from the declared strengths and the gate as ruled (question S, AM65; question G, AM66), not from the
  situation.
  RULED (Hadi, 4 October 2026; AM68, not built): the gate refuses a leader that the evidence alone ranks below another
  live hypothesis. Once built, this part leaves the gate's admissions: in the what-if reading X (WHATIF.md) 18 of the
  310 wrong gate ticks of kind (ii) remain (ticks on which the evidence ties or ranks the admitted hypothesis first; not
  the first part's 18), 11 with AM67 as well.
Boundary (framework scope), the first part only · Hadi, 4 Oct 2026, corrected the same day (T-K part 1, after step 5b;
design_records.md, "T-K", THE LIMITATION OF ADMISSION FROM CONTEXT AND MOVEMENT) · the recognizer's belief and the
gate; how they are read in an evaluation.
- "An admission of a hypothesis that is not the true task" names the outcome. It does not say the reasoning was wrong.
- The numbers: analysis/kitting/mpb/tk5b/COMPARISON.md (A2, the kinds) and WHATIF.md (the ratios), existing outputs of
  steps 4 and 5b, the robot idle. The two parts are reported as ratios. The ×1.01 that counts the 18 ticks is
  COMPARISON.md's reporting threshold for its kind (i); it is no design value and no cut between "separates" and "does
  not separate". With context knowledge on there are 47 such admissions during modelled tasks (504 gate ticks); 43 of
  them (453 ticks) have a true hypothesis: 311 ticks the true task first (the 18 and the 293), 141 ticks the admitted
  hypothesis first, 1 tick a third hypothesis first.
- The 141 ticks with the evidence alone ranking the admitted hypothesis above the true task (×0.93 down to near 0)
  belong to neither part: mostly the first ticks after the human leaves a delivery for a coffee break or the A/C,
  where the delivery still fits. The run with context knowledge off makes most of these admissions too.
- Step 5's case 5 (scenario_s16_05, the pass at 28.3 cm from 22): the evidence ranks the A/C activation above the
  admitted deliver_item(item_4) by ×1.0014 at tick 0, ×1.0029 at 1, ×1.09 at 25.
- The largest gain and the largest costs come from one mechanism: a lone assigned task admitted before the human starts
  it, on its commitment warrant and its prior. Correct 59 times (admitted on the previous task's completion tick, the
  human starting it on the next): 1773 of the 3005 ticks by which the true task's admissions come earlier, and in
  planning the gain of 24 and 23 ticks in scenario_s16_03 and _04 (admitted at 73, the human starting at 74). Not
  correct 9 times (retracted after 8 to 60 ticks): 230 of the 504 wrong gate ticks during modelled tasks, and both new
  cases below min_separation in planning (scenario_s16_05, 28.3 cm; scenario_s11_03, 11.3 cm, whose 78 ticks gained
  come from the same wrong admission).
  RULED (Hadi, 4 October 2026; AM67, not built): this admission waits for observation warrant. In the what-if reading
  Y the 59 correct cases come 1 tick later and scenario_s11_03's admission is refused; scenario_s16_05's stays (observation
  warrant held, WHATIF.md) and is refused by AM68.
- Not settled here: how the robot acts on an admitted hypothesis that can be wrong. Today it plans on the admitted task
  alone and does not use the fallback projection while the admission stands. The design discussion of 4 October 2026
  after step 5b takes this up, with the gate and the prior; nothing in it is ruled (design_records.md, "T-K", THE
  DESIGN DISCUSSION AFTER STEP 5B). Communication with the human is the other place where such a case can be resolved
  (T-D X, X5).
  RULED (Hadi, 4 October 2026; design_decisions.md, "T-K", R7's AM69, AM71): the robot keeps planning on the admitted
  task alone; an admission that was correct when made stays until the retraction (the end of an admission, T-D L, is
  unchanged). Not taken: projecting an admission without observation warrant as the human staying, checking the plan
  against two projections together, communication on a weak admission (the last two possible future work, TODO-97,
  TODO-96).
- The cases that remain are limitations, not defects (Hadi, 4 October 2026; AM72, its first case reworded by AM74): a
  near-tie in the evidence that favours a hypothesis the human is not doing; the evidence itself ranking another task first after the human interrupts a task (the 141 ticks above, in
  part); the human doing the less probable task after a correct admission. Kind: boundary (framework scope). Hadi's
  principle: if the robot admits task X and the human does Y, the recognizer was not wrong for that reason; either the
  human did something unexpected given the modelled knowledge and the evidence, or the recognizer is limited. The
  framework shows what recognition contributes to adaptive planning and is not changed to make every run flawless.
  Why the rewording (AM74): the first part's 18 measured ticks rank the true task first by ×1.0008 to ×1.01, so AM68
  refuses them, and AM67 refuses the boundary tick before them; as first worded ("the first ticks of a walk with equal
  evidence") the case does not occur in the measured sets.

## Rejected or dropped

- **2.1** "The human acts rationally": too strong; nothing depends on it.
- **3.1** "Switches only at action boundaries": rejected. Mid-action changes stay in scope and are handled by the
  general machinery: the current derived phase's hypothesis adequacy turns inadequate, the admitted projection is
  retracted, the fallback projection takes over, and the new task is admitted at its next fitting phase.
  scenario_s09_13 demonstrates the recognition side, not the recognition-to-planning chain (the robot is idle).
- **3.5** The re-admission delay after a switch: a consequence of T-D L5, recorded there (with the test-bed's numbers
  at HEAD), and an evaluation measure; not an assumption.
- **4.1** Reframed as 4.6.
- **4.3** Approach-and-hold at the separation boundary: an observed consequence of P4, recorded in the T-D P entry; what
  else the robot may do is X's.
- **A2** A second behavioural claim, redundant with 1.1.
