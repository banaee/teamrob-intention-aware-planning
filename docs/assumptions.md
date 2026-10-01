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

**1.2** Every baseline script declares its experimental intent (label C, purpose); **unmodelled behaviour** (behaviour
no hypothesis of the robot's hypothesis space describes, label B) appears only where the description says so.
Authoring convention · the terms ruling of 24 Sept 2026 (labels A, B, C), TODO-80 · scenario descriptions; the
label-C check (the exit walk is exempt, glossary §7).

**1.3** For human-script and test-bed runs (the robot has no work of its own), a run's step count is derived from the
human's load-time replay plus the idle margin (the replay's last acknowledgement tick + 1 + 30 ticks of the idle
human), not a literal. The horizon of runs where the robot has work is open; the maintained baseline sets keep their
step counts.
Authoring convention · TB.3b's rule (`analysis/ir_testbed/run.sh`) · run files, sweep scripts.
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
