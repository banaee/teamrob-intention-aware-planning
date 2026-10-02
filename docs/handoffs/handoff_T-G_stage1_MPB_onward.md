# Handoff: T-G stage 1, the MPB on dock_loading and the close of stage 1

Written 2 October 2026 by the design chat that planned and built T-G stage 1 up to the close of its IR test-bed
(1 and 2 October 2026). Informative only. It decides nothing. The repo is authoritative; where this text and the
repo disagree, the repo wins. The rulings are in docs/design_decisions.md, entry "T-G: the second domain's
rulings". This handoff points to them and does not restate them in full.

## 1. Working style (binds every reply in the new chat)

- The design chat settles WHAT and WHY; Claude Code (ccode) owns HOW and runs everything. Design before
  implementation; rulings go into the records before code.
- Terms are docs/glossary.md's, used exactly; a missing term is flagged and proposed, never invented.
- Before the first design question, show the zoomed-out plan of the chat (scope, steps, the questions to come) and
  get Hadi's agreement.
- One question at a time: the problem in plain words, concrete cases, the alternatives, one recommendation, an
  explicit ask. Independent questions may share a message; chained ones never do. A clarification question is
  answered directly, without repeating the open question.
- Never write a ruling code alone (B10, C1, A4). Write the content in a few words and give the code beside it.
- Scientific, literal register; short sentences; no idioms; no em dashes. For the robot write "moves" or "goes".
- Engage critically. Every ruling, the dock_loading ones above all, is open to discussion on design grounds; a
  change passes through Hadi's ruling and a dated superseding note before the build relies on it.
- Scenarios and runs are tests. Nothing in the design, a parameter, a layout, a setup or a task is adjusted to a
  result. Findings are classified, never fitted.
- Hadi leads scenario design. The design chat drafts a whole set in one go: controlled scenarios first (each tests
  one thing; several, varied), then at most four or five mixed ones, read only against the controlled ones.
- ccode prompts: the model and the session line above each; the step in the first line (plan only, build, records
  only; ccode is in auto mode); what and why fixed, how left to ccode; the autonomy block; the reviewer role;
  headless; commit on main in logical groups; never push (Hadi pushes; pushing syncs the repo into the project).
  A records prompt states decisions by their content. One prompt at a time: wrap one, then the next.
- Every build prompt carries the core-algorithm rule (now also in CLAUDE.md): the recognizer's scoring and
  admission, the meta-planner's candidate evaluation and cost, the projection's semantics, the planner's method
  selection and the trigger set are not changed at the conceptual level without Hadi's ruling; a change to shared/
  or world/ is domain-agnostic and named in an approved plan; otherwise ccode stops and reports first.
- Expectations are derived from the records and committed before the runs, by an oracle that does not import the
  recognizer.
- The design chat cannot read the `analysis` folder or `ros_sim` (not in the project knowledge); `mesa_sim` is
  selected in part. The figures of a run come through ccode's reports and the records. Each run prompt asks for
  the figures needed; each records step puts a set's results into the design entry.
- Reviews of ccode reports show only what matters for decisions and the design logic.

## 2. State of the repo at handoff (verify each line before relying on it)

- Design rulings of this chat, recorded: the lifecycle of a script entry, the closing part, the load-time replay,
  the agent's area in computed states (commits e3feac0, 98076f5, ec2cc61, 665f70e, 139a60e, fb510cd, 9549b92,
  dc7bbce); the rooms and setups (f3d4125, adb6cf3, 5381491, eca9ae8); the plan's approval and the plan file
  docs/handoffs/plan_T-G_stage1.md (0d1c383, 8b1a4ed, 81aa154, 03b0ed4, 950d763).
- Artefacts: env_layout_02 to _04, env_setup_02 to _07 (cec8cc3). The old env_layout_01 with its setup and
  scenarios is removed.
- Build, each step with kitting's outputs byte-identical: the rename of "zone" to "area" (8d064ca, c21f001); the
  agent's area in computed states (b513b82, 9bca721); liveness by applicability (bd4bddc, a76054f); object states
  and designations (b74485b, 50f2fb8); the human's script form (048a36e, 576f2b2); dock_loading's forms and tasks
  (670cb78, 610fed9, 1492789, 512a452); the milestone scenarios (52b2aae, 8b9d267, 0371035).
- Records of the build and the milestones (772e422, 63fd2f9, bea5930, 1968e0d, bd65b49, 60c9193, 8ee9e87, e5e4c6a,
  and the records of the second milestone scenario).
- The IR test-bed on dock_loading: the sorting under kitting, the instruments, office_break at 90 seconds, the 54
  scenarios, the expectations, the runs, the report (746fae6, 9a35af1, ae77689, 65273e8, cbeefe4, e573e9e, edbe34f,
  51e5e1c, 54edb71, 3ea4b60, 736eb01, 4d9011d, e4fc88c, b20a67f); its records (cc516f9, e1c4a54, 16ad4b7).
- Verify that Hadi has pushed the last commits.
- The reference set for byte comparisons lies outside git: /home/hadi/teamrob_refs/tg_stage1/ (ref/, refrun.sh).
- The analysis folder is sorted: analysis/instruments/ (shared code), analysis/kitting/, analysis/dock_loading/;
  the run files under configs/<domain>/; the tests under tests/kitting, tests/dock_loading, tests/instruments.
  docs/rename_table.md maps the old paths.

## 3. What was ruled in this chat (an index; read the entry)

- The human's script (framework-wide, extends A3): an ordinary entry is taken at most once and is closed on
  COMPLETED, ABANDONED or INFEASIBLE (Q12, Q13a); a repeatable entry stands below every ordinary entry, carries no
  events, is skipped at run time while its task's completion condition holds, and is not executed by the load-time
  replay (Q12, R1); the author declares a script that depends on the robot (Q13b); the closing part is taken once
  every ordinary entry is closed, and its content is each domain's convention (Q14); a foreseeable task written as
  an entry is an ordinary entry, and events stay attached to their entry (Q15).
- The agent's area in a computed state (R2), with one definition for the environment and the computed state.
- dock_loading: stage 1's closing part is "go to the desk"; three rooms from the present room; two setup kinds per
  room; the truck designated as the destination of an empty pallet; a task has a method for every area the agent
  can be in (the robot: truck side and hall; the human: hall and office); office_break lasts 90 seconds.
- Staging: stage 1, then stage 1.5 (context knowledge), stage 2, stage 3. The room with the freezer and the dry
  store moved to stage 2 with its own setup and scenarios. Stage 1 keeps full observation; the rule that monitored
  areas are fixed per layout (A8) is reopened at stage 2.
- The walk to the standby place stays without a hypothesis for now (Q16). Two candidates are recorded on TODO-155,
  neither approved.

## 4. Results so far

- The five mechanisms are built with kitting unchanged. dock_loading runs from start to end in all three rooms.
- The IR test-bed: 42 controlled and 12 mixed runs, zero disagreements with the expectations committed beforehand.
  This establishes that the recognizer behaves on dock_loading as the records specify. It does not establish the
  quality of the recognition.
- The baseline: 98 of 147 stretches reach the admission threshold (38, 40 and 20 of 49 by room); the median delay is
  20 ticks; 49 stretches never reach it, all scans (34 short walks of 26 ticks or fewer, 9 same-motion pairs, 3
  second scans with no walk, 3 scans leaving the office in env_layout_02). One tick is 2 seconds.
- Findings about the mind, none ruled: hypotheses with the same motion divide the belief (TODO-97); a short walk
  gives too little evidence under equal shares at an episode's start (TODO-154); the walk to the standby place is
  admitted as a break, or as a skipped assigned scan (TODO-155); the robot does not anticipate the scan that its
  own delivery makes possible (TODO-154).
- Findings from the milestone runs: the human passes a standing robot closer than the minimum separation (the
  parked case TODO-135; structural in this domain; reported as its own measure beside the violations by a moving
  robot); the robot never arrived at a bay where the human stood, because a round trip to the truck (about 96
  ticks) is longer than a scan from the standby place; a robot with an empty pool stays at the bay after its last
  delivery, and the human walks up to it.

## 5. The first task of the new chat: the MPB set on dock_loading

Read first: the MPB entry of kitting in docs/design_decisions.md (its rules, its oracle, its disagreement classes),
and the rulings on the admission gate (T-D G), the fallback projection (T-D P) and the boundary cases (T-D X).

Open points, to put to Hadi one at a time:
1. A setup in which some pallets already stand in a bay while the robot delivers others, so that the robot meets
   the human at a bay.
2. A convention that the robot's last assigned task is a return, so that it does not end standing at a bay.
3. How expected decisions are derived when the human's sequence depends on the robot's decisions (C6 of the entry).
   The MPB instrument is prepared only as far as reading its domain from the run file; its chain, property and
   alteration code is kitting's.
4. The value of office_break, reviewed for the MPB: at 90 seconds the human is away for about 110 ticks, a little
   more than one round trip of the robot.
5. A third setup kind (all full pallets designated to one bay), to add only if the first MPB run calls for it.

Design inputs: admissions are not the normal case on dock_loading (one third of the stretches are never admitted),
so the MPB must show how the robot decides on the fallback projection; in env_layout_03 the robot already changed
its task on the fallback alone (noted for track 3b, TODO-145); the return of an empty pallet is the robot's task
that conflicts with nothing; a break walk crosses a robot route in some rooms and not in others.

## 6. After the MPB: the close of stage 1

- Records: the MPB's results and classified findings; the tags of TODO-153 to TODO-156 (Hadi rules); the sweep of
  old terms ("zone" in records and comments, "body" for the simulator); the sizes of the files under docs/, since
  docs/ takes about a third of the project knowledge's capacity.
- The handoff for stage 1.5.

## 7. Inputs recorded for later stages (do not open before their stage)

- Stage 1.5, context knowledge. One design question for it: what sets a hypothesis's share at the start of an
  episode. Four determinants, to design as one mechanism: the assignment (exists), context facts, the task that
  just ended (Hadi's transition prior), an enabling event such as the robot's own delivery. Also Hadi's ideas: a
  foreseeable task's duration is not one fixed number; temporal context as a fuzzy set. Its other questions: the
  form of a context fact; start only or interruption; "applicable to start" against "valid to continue".
- Stage 2. To rule before store_pallet: a route is selected from the areas of the agent and of the object, not
  from the kind of task and the pallet's state (TODO-156; today a pallet's emptiness stands in for the side of the
  gate of its origin). What the robot does when no method of a task is applicable (TODO-152, V1). The origin of a
  pallet recorded at the pick-up. The observation rule reopened (the robot's own area, or its area and the areas
  behind open passages) with the trigger at disappearance and reappearance.
- Hadi's wish, not scheduled: a task file that reads as human-written (the knowledge stated once, the flat methods
  generated from it); the abstraction of passages between areas as domain-independent knowledge.

## 8. Parked items that a finding may touch (do not open unasked)

TODO-132 (a), TODO-134, TODO-135, TODO-140, TODO-142, TODO-143, TODO-146, TODO-151, P3, TODO-97. A dock_loading case
that lands on one of these is classified and recorded; the item reopens only by Hadi's ruling.

## 9. Where things are

- Records: docs/design_decisions.md (the T-G entry, with the blocks on the approved plan, the milestone, Q16 and
  the IR test-bed), docs/glossary.md, docs/assumptions.md, docs/TODOS_AND_DEFERRED.md, docs/roadmap.md, CLAUDE.md.
- The plan of stage 1: docs/handoffs/plan_T-G_stage1.md.
- Domain: domains/dock_loading/ (layouts, setups, scenarios, tasks, actions, script call forms).
- Instruments and results (not readable by the design chat): analysis/instruments/, analysis/dock_loading/ir_testbed/.
- Handoffs: docs/handoffs/ (this file belongs there).
