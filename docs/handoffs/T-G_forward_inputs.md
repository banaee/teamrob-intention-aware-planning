# T-G: forward inputs for the stages after stage 1

Written 2 October 2026 by the design chat that closed T-G stage 1. Place: docs/handoffs/.
Corrected 2 October 2026 by the next design chat, after its verification against the repo's records.

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

The next stage is not yet named by Hadi [open]. The records say stage 1.5 comes before stage 2. Hadi has spoken
of stage 2 as the next work. The design chat's recommendation was stage 1.5 first, because stage 2's tests would
otherwise be read twice, once with the present weak admissions and once after stage 1.5. The new chat asks Hadi
before anything else.

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

Not tested in stage 1: env_layout_02 in the MPB (the room with the latest admissions, median 28 ticks); the test
that alters one rule of the oracle to show that a zero result is a detection (built for dock_loading, not run); a
setup in which all pallets go to one bay (recorded as conditional, never needed).

---

## 5. Stage 1.5: context knowledge (framework-wide; nothing ruled)

NOTE (2 October 2026): the stage's design is ruled by Hadi (design_decisions.md, "T-G stage 1.5: context knowledge in
the recognizer's belief", R1 to R8; design_records.md, "T-G stage 1.5", R9, the cut, the open items). Hadi's earlier
idea of a context fact that triggers or interrupts a task of the human is superseded by R1 for this stage: context
knowledge acts in the robot's mind only, in the recognizer's belief.

Content, as recorded: the scenario holds a timeline of context facts. A context fact changes at an authored
point of a run, and the environment applies it. Foreseeable tasks of both domains can be conditioned on such
facts. The mechanism for object states built in stage 1 already admits a fact that no action changes, so
context facts need no second mechanism. [ruled: the requirement on the form; everything else open]

The central design question [open]: what sets a hypothesis's share at the start of an episode. Four determinants
are recorded, to be designed as one mechanism:
1. the assignment (exists today: assigned tasks are in the support);
2. context facts;
3. the task that just ended;
4. an enabling event, such as the robot's own delivery.
Stage 1's figures in section 4 are its measured baseline.

What exists in the code today [recorded, TODO-66, deferred]: the recognizer holds a context weight in the shared
core (`_context_weight`). It names two tasks literally (`ac_activation`, `coffee_break`). It carries four
constants (a temperature boost of 3.0, a fatigue boost of 2.5, the thresholds 26.0 and 500). It acts on the
recognizer's output only and is never fed back. No scenario sets the temperature or a long shift. It is the one
place in the shared core that names a domain task. Whether stage 1.5 closes this item is for the stage's design.

Also recorded: the pre-loaded context stream moved to stage 1.5 from the interactive simulator's track (T-V track
2), which keeps the live events.

Other open questions recorded for the stage [open]:
- the form of a context fact;
- whether a context fact only lets the human start a task, or also interrupts a task in progress (the present
  rule is: never interrupted). The record on future-work directions places the design of "an interruption of a
  busy human caused by a world fact, if wanted" in T-V track 2, as the same entry point as a live user's click;
- what happens to a hypothesis when its condition turns false while the human still executes the task
  ("applicable to start" against "valid to continue");
- how the prior uses context;
- how the robot perceives a context fact.

Hadi's ideas for the stage [idea]:
- A coffee break is taken in a time window (his example: 9:30 to 10:00), and the hypothesis has a higher
  probability inside the window. An air-conditioning task is triggered when the temperature in the context
  stream passes a threshold. He sees both as dynamic and as possibly interrupting a task in progress.
- "Applicable" can track context: a condition on a context fact makes the human take the task, and keeps the
  hypothesis live only while the condition holds.
- A transition prior between tasks, like a chain of tasks: after one task ends, some next tasks are more
  probable. His example: after putting the pan on the stove, adding oil most probably follows, without being
  part of the same task.
- The duration of a foreseeable task is not one fixed number. An office visit can last 20 to 30 seconds (to fetch
  something) or 90 to 120 seconds (office work).
- Temporal context as a fuzzy set with a degree of membership.
- In kitting, a human who leaves the room for a while can be a foreseeable task with a typical duration known
  from context. (chat only)

The walk to the standby place and the walk to the desk (TODO-155) [open]. The item is parked and tagged V1. No
stage is assigned to it. Its placement in stage 1.5 was a proposal of the previous design chat, not a ruling.
Ruled for now: these walks stay without a hypothesis. Two candidates are recorded, neither approved:
- a foreseeable task "step aside" that is always possible. Hadi's objection: the human steps aside only when no
  pallet waits; an always-possible task competes with the scans when a pallet waits. Also, as a walk alone it
  would make every arrival at any target count as the end of an episode. A wait at the end of the task avoids
  that.
- a hypothesis that is live only while no assigned task of the human is live. It matches the condition, and it
  changes the rule for which hypotheses are live.
Not taken: the walk as the last step of the scan task.

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
reappearance starts a new episode from the prior base (the belief with which an episode starts). The mind keeps
no last observed position. dock_loading's office is the one unmonitored area. This step is built before the
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

Not future work [ruled]: a type-to-destination rule in place of explicit designations is recorded as not taken.
By the rule on V1 and future work, an alternative not taken in a design question is never a future-work item.

Also planned inside V1, after T-G: the evaluation; the viewer; an interactive simulator in which deviations are
injected at run time; one further test track on adaptation under conflict.

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
