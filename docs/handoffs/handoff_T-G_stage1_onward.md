# Handoff: T-G stage 1 onward (planning and building dock_loading, stage by stage)

Written 1 October 2026 by the design chat that settled T-G's design (30 September and 1 October 2026).
Informative only. It decides nothing. The repo is authoritative; where this text and the repo disagree,
the repo wins. The rulings themselves are in docs/design_decisions.md, entry "T-G: the second domain's
rulings" (sections A framework-wide, B dock_loading only, C staging, Proposals). This handoff points to
them and does not restate them in full.

## 1. Working style (binds every reply in the new chat)

- The design chat settles WHAT and WHY; Claude Code (ccode) owns HOW and runs everything. Design before
  implementation; rulings go into the records before code.
- Terms are docs/glossary.md's, used exactly; a missing term is flagged and proposed, never invented.
  New since this chat: mind, body, environment, simulator, container, area, monitored area, applicable.
  "Body" no longer names the simulator. For the robot write "moves" or "goes", never "drive".
- One question at a time: the problem in plain words, concrete cases, the alternatives, one
  recommendation, an explicit ask. Independent questions may share a message; chained ones never do.
- When Hadi asks a clarification question while a design question is open, answer it directly. Do not
  repeat the open question at the end of each reply.
- Scientific, literal register; short sentences; no idioms; no em dashes in text drafted for Hadi.
- Engage critically. A settled decision can be reopened on design grounds.
- Scenarios and runs are for testing; nothing in the design or a parameter is adjusted to fit one.
- ccode prompts: the model and session line above each; the step in its first line (plan only / build /
  records only; ccode is in auto mode); what and why fixed, how left to ccode; the reviewer paragraph;
  commit on main in logical groups; never push (Hadi pushes; pushing syncs the repo into the project).
  A records prompt is distilled: it states decisions by their content and names no discussion document.
  Reviews of ccode reports show only what matters for decisions and the design logic.
- V1 and FW: a TODO keeps its number; a tag [V1] or [FW] is added when the item is next touched, by
  Hadi's ruling. [FW] is for conceptual directions only. An alternative not taken is recorded inside
  its ruling.
- Before each stage's plan, the design chat and Hadi agree the layout and the setup for that stage.
- Findings are classified, never fitted (the assumptions' case classification and MPB-4's classes). A
  finding that the framework disagrees with the records stops a build and returns to the design chat.

## 2. State of the repo at handoff (verify each line before relying on it)

- Build 1 (30 September): commits 56e674e, 6e29c15, 62ebc4e. Form-only repairs in domains/dock_loading
  and scenario_s01_03, a viewing fixture that loads and initialises with no tick. scenario_s01_01 and
  scenario_s01_02 fail at load by intent.
- T-G records 1 (1 October): commits 2450a58, 3f705b7, 7da6da5, d43463b, 6dde414. The design entry,
  the glossary and assumptions (5.3 new), the TODO file (TODO-147 to TODO-151 new; tags on TODO-16,
  25, 39, 104, 140, 144, 145, REFACTOR-03, LIMIT-04; TODO-81 closed), the roadmap, CLAUDE.md, and
  superseding notes on docs/handoffs/handoff_T-G_onward.md.
- Verify that Hadi has pushed these commits, so that the project knowledge holds them.
- No code outside domains/dock_loading has changed in T-G so far.

## 3. What is ruled (read the design entry; this is an index)

Framework-wide (section A): V1 and its boundary; the terms; the human's script form (assignment static,
availability dynamic, execution order dynamic; the author's priority list; no interruption of a task in
progress); liveness by applicability in the recognizer; object states and designations declared by the
domain and held by the environment; the perception assumption 5.3; TODO-16 in V1; track 4 in V1 in a
reduced form (monitored areas); areas; the FW directions (TODO-147 to TODO-150, LIMIT-04).

dock_loading (section B): the robot replaces the driver, the observed human is the warehouse staff
member; the scan's condition; destinations by designation; is_empty as a state; the gate opened on
request and the office door; two foreseeable tasks; store_pallet; the held-object rule; one point per
container; the room; the gate passage as a plain step with one method per starting area; check-in and
check-out; the items not taken.

## 4. The stages (section C1 of the design entry; all in V1)

- Stage 1, the basic domain: the robot delivers and returns; the human scans, takes the two breaks and
  steps aside to the standby place; the gate is declared open; the office door has no state. The
  framework-wide mechanisms are first built here. The IR test-bed, then the MPB.
- Stage 2: store_pallet; the gate opened on request; the office door's state; after the MPB's first
  run, TODO-16 with the stepwise delivery.
- After stage 2: track 4. It now comes before T-F, and T-F may use the unmonitored office on
  dock_loading.
- Stage 3: check-in and check-out, with two optional items.

## 5. The first design question of the new chat (parked, not ruled)

The lifecycle of an entry of the human's list. Q2 says the free human takes the first applicable entry
that is "not yet completed". That is not sufficient: a dropped or misdelivered task is not completed,
and Q2 as worded selects it again (evidence: ten kitting scenarios with a drop event, and the
misdeliveries in the test-bed sets). "Completed", "ended", "abandoned" and "available again" are
distinct. For an abandoned entry three readings are open: finished for good for that entry;
unavailable for now and retryable; a state of its own that depends on the authored event. Two cases
any rule must satisfy: the standby entry is takable again after the human has left the place; a
dropped work task does not restart at once. A candidate, not ruled: an entry is skipped when its
terminal fact holds or when the human has ended it by an authored event.
The human's script form is not built before this is ruled.

## 6. Before stage 1's plan: the layout and the setup (to agree with Hadi)

- The room's arrangement is ruled (design entry, B10). Not ruled: whether stage 1's layout already
  holds the stores and the freezer, unused (a proposal).
- To place when the layout is drawn: the coffee machine, the standby place, the landmarks for the exit
  walk. The gate's button and the desk belong to stages 2 and 3.
- The areas of the room (truck side, hall, office) are declared in the layout.
- For the IR test-bed the robot is idle, so that setup places the pallets in their delivery containers
  from the start.

## 7. What stage 1's plan must contain or settle (design entry, C3 and C4)

- First step, in its own commit, no change of behaviour: the code name "zone" becomes "area". The
  plan first reports every place the name occurs and whether the maintained sets' logs print it.
- The catch-up of dock_loading's forms to kitting's (the state list in C3).
- The mechanisms outside the domain, each with its acceptance on kitting (the maintained sets stay
  byte-identical): the human's script form (after section 5 is ruled), liveness by applicability, the
  generic object states and designations.
- Points for the plan, each returning to the design chat only as a finding: the load-time check for a
  script that depends on the robot and the meaning of the outcome "infeasible"; where the exit walk
  stands relative to the priority list; how an event or a foreseeable task is placed relative to tasks
  whose order is not fixed; how a pallet's origin is recorded; how the meta-planner behaves when the
  pool holds tasks and none is applicable (TODO-30); the forms for states and designations; the
  smallest set of methods for the gate passage with the held-object rule; how the existing machinery
  behaves when the live set holds foreseeable tasks only.
- Names not yet given are proposed by the plan and approved by Hadi.
- To watch in the test-beds: hypotheses that predict the same motion divide the belief, so none passes
  the admission threshold. If confirmed on dock_loading, it is a finding about the mind within V1.

## 8. Open at their stage (do not open before)

- Stage 2: the design of TODO-16 (how the candidates are formed; whether the recognizer also considers
  several applicable methods).
- The MPB on dock_loading: how its oracle derives an expected decision when the human's sequence
  depends on the robot's decisions.
- Track 4: which trigger carries the human's disappearance and reappearance (one conflict mark remains
  under A8); the rest of TODO-140 (the exit through a door).
- Stage 3: the design of check-in and check-out, including what "exchanging the list" means when the
  robot holds the designations from the start.

## 9. Proposals, not ruled (design entry, Proposals section)

An empty pallet's destination as a designation in the setup; TODO-151 (two generic load checks in
shared/), untagged; the placement of TODO-131 (the robot-mind object), no longer implied by track 4;
stage 1's layout already holding the stores.

## 10. Parked items that a finding may touch (do not open unasked)

TODO-132 (a), TODO-134, TODO-142, TODO-143, TODO-146, P3, TODO-97. A dock_loading case that lands on
one of these is classified and recorded; the item reopens only by Hadi's ruling. A sweep of the old
terms ("body" for the simulator, "embodiment layer") can go with stage 1's records.

## 11. Where things are

- Records: docs/design_decisions.md ("T-G: the second domain's rulings"), docs/glossary.md (sections 6,
  8, 9, 10), docs/assumptions.md (5.3; the note on 2.3), docs/TODOS_AND_DEFERRED.md, docs/roadmap.md
  ("The plan from T-A", the T-G stages), CLAUDE.md (the state paragraph).
- Domain: domains/dock_loading/ (build 1's state), domains/kitting/ (the reference for every form).
- Instruments: analysis/ir_testbed/, analysis/mpb/.
- Handoffs: docs/handoffs/ (this file belongs there).
