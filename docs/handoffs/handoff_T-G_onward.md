# Handoff: T-G onward (the second domain in Mesa: dock_loading)

Written 30 September 2026 by the design chat that closed T-D (the G, X and MPB chat). Informative only.
It decides nothing about T-G. The new chat starts with Hadi's own assumptions and intentions for the
domain, then puts T-G's design questions one at a time. The repo is authoritative; where this text and
the repo disagree, the repo wins. Statements marked "(verify)" were read from the repo during the previous
chat but must be re-verified by ccode before the new chat relies on them.

## 1. Working style (binds every reply in the new chat)

- The design chat settles WHAT and WHY; Claude Code (ccode) owns HOW and runs everything. Design before
  implementation; rulings go into the records before code.
- Terms are docs/glossary.md's, used exactly; a missing term is flagged and proposed, never invented.
  The world (what the human does) and the robot's mind (what it believes) keep separate vocabularies.
- One question at a time: the problem in plain words, concrete cases, the alternatives, one
  recommendation, an explicit ask. Independent questions may share a message; chained ones never do.
- Scientific, literal register; short sentences; no idioms; no em dashes in text drafted for Hadi.
- Scenarios and runs are for testing; nothing in the design or a parameter is adjusted to fit one. A
  rare or accidental case is parked (the fixture rule in docs/assumptions.md), never designed around.
- ccode prompts: the model and session line above each; the step in its first line (plan only / build /
  records only; auto mode); what and why fixed, how left to ccode with every open technical choice
  stated in its plan; the reviewer paragraph (objections on design grounds, built as given, objections
  to Hadi); commit on main in logical groups; never push (Hadi pushes; pushing syncs the repo into the
  project). Reviews of ccode reports show only what matters for decisions and the design logic.
- Findings are classified, never fitted: MPB-4's five classes (the oracle misread the records; the
  framework disagrees with the records; the records do not determine the value; an authoring artefact;
  a boundary case). Class 2 stops a build and returns to the design chat; its three readings are
  recorded under MPB-4.

## 2. State of the repo at handoff

- T-D is closed except its tail. Tracks 1 (the IR test-bed), L, P, 2.5, G, X and 3 (the MPB) are done.
- The MPB is CLOSED (design_decisions.md, "The meta-planner test-bed (MPB)"): sixteen scenarios on
  env_layout_12, 13 and 14, zero disagreements on parts 1 to 3 under both strategies prior on; the
  coverage matrix in analysis/mpb/coverage.md (36 verified paths, 5 unreachable with derivation, 4 out
  of coverage, P3 not claimed). Its closure sentence: the MPB establishes structural branch
  reachability and execution of the recognition-to-planning chain, not consequential activation under
  human-robot interaction conflict (track 3b, TODO-145).
- The plan-execution invariant was fixed this week (class 2 (a), recorded under MPB-4 and the
  realization entry): the trajectory realize() assesses is the trajectory the robot executes;
  ExecutorState.action_in_flight and owed_completion_ticks, Projector.project(resume_from, lead_in),
  owed ticks spent before a hold; T-B Q7 superseded in part; TODO-77 corrected; TODO-146 the P-side
  residual. The maintained sets were regenerated (one behavioural change, scenario_s02_01 prior on).
- The pipeline was revised on 30 September 2026 (roadmap, "The plan from T-A", the dated order block;
  commit 3d95214): T-D close, then T-G, T-F, T-V, the T-D tail (3b, 4, 4D), T-S. Letters are never
  reassigned; T-E means the viewer in older records and is T-V track 1.
- Commits to verify as landed before the new chat starts: the MPB close-out commit group (CLOSED, the
  closure criterion, TODO-145, TODO-144's during line, figure_ir.png per MPB scenario, the instrument
  saving the projected and planned segments, io_contracts §1.9) and the pipeline records (3d95214).

## 3. What T-G is (from the roadmap's T-G entry, as recorded)

The second domain in Mesa: domains/dock_loading/ against shared/ unchanged, executed by the Mesa body.
Its purpose is the generality claim: the recognizer, the gate, the projection and the meta-planner,
unchanged, on a second task model and room. Rules recorded with it:
- nothing domain-specific enters shared/, ever;
- findings are classified under the assumptions' case classification and MPB-4; a shared ruling is
  reopened on design grounds only;
- the artefacts follow T-L's rules (layouts, setups, scenarios by discovery; serial ids; the setup
  holds item placement and designations; positions, pools and scripts are the scenario's);
- the instruments are reused in order: the IR test-bed (the oracle imports nothing from the recognizer
  or the likelihood functions; the trajectory replay from the script), then the MPB (parts 1 to 3
  exact; part 4 as declared properties; MPB-2's layout-and-setup rule; the placement rule that a setup
  change may not alter a verified scenario on that setup).
- T-G no longer holds the 4D detour (T-D tail) or ROS/PRIEST (T-S).

## 4. What the records say about dock_loading (verify each line from the repo)

- The domain skeleton: HITS3 scenario 2, a driver unloading pallets at a dock (docs: the HITS3
  scenarios document in the project files). Task schemas recorded: deliver_pallet, load_return,
  confirm_delivered_pallet, coffee_break, office_break (verify the exact names and their parameters).
- Deferred since Phase 2.1; migrated with kitting through T-L's stages, so it imports and the registry
  discovers it (verify).
- TODO-25 open: confirm_delivered_pallet lacks parameter_types and its parameters do not match the
  scenario's bindings; since I2 that raises on the first tick of any dock_loading run, by design. TODO-81
  points to T-G, with duration_key on dock_loading's wait_at in the same change (verify).
- LIMIT-02 and LIMIT-03 (verify their text): the gate is always open; the human's scan does not wait
  for the delivery.
- Nothing after Phase 2.1 was exercised on it: no T-H script vocabulary (script.py exists for kitting
  only), no IR test-bed, no assumptions check, no P4 landmarks, no MPB. Every ruling since T-D was
  verified on kitting only.
- CLAUDE.md still marks domains/dock_loading/ as deferred until T-G's first build.

## 5. Design questions T-G will meet (a list, not proposals; Hadi's assumptions come first)

1. The domain's task model: which of the driver's activities are assigned tasks (the work order),
   which are foreseeable tasks (recorded candidates: the phone call, talking to the dock worker; the
   coffee and office breaks exist in the skeleton), and what stays unmodelled behaviour.
2. The driver's work order and its representation (assumptions 1.4, 2.2, 2.6 apply as they stand;
   whether they hold for a driver is Hadi's to say).
3. What the domain adds that kitting did not: the truck as a container (objects inside a movable
   object), the dock gate as a method guard or a world fact, the forklift or pallet jack as the
   human's tool, the scan or confirmation as a terminal action. Each is a possible design question for
   the task model or the world state; each is checked against shared/ for domain-independence.
4. TODO-25's schema fixes, before any run.
5. The human action script vocabulary for the domain (T-C's and T-H's forms; the during form is
   absolute, TODO-144 notes the relative form as an authoring question).
6. The room: one controlled layout for the IR test-bed, then setups and scenarios by discovery; whether
   the IR test-bed's oracle needs anything beyond its current derivations (verify: it uses the
   planner's decomposition and the task model, nothing domain-specific).
7. The MPB on the domain: the same instrument; the coverage matrix's rows are the framework's, not the
   domain's; which rows the domain can reach is derived, not assumed.
8. The relation to T-F: T-F evaluates kitting, dock_loading and cross-domain as tracks; T-G's
   artefacts are what T-F's dock_loading track will use.

## 6. Parked items that a T-G finding may touch (do not open unasked)

TODO-132 (a) (the fallback's persistence break; evidence in scenario_s11_02), TODO-134 (the offset
gap), TODO-142 (the skip rule on an arrival tick), TODO-143 (an observed human with no work under the
prior on), TODO-146 (the P-side projection residuals), P3, TODO-97 (belief-aware planning). A
dock_loading case that lands on one of these is classified and recorded; the item reopens only by
Hadi's ruling.

## 7. Where things are

- Records: docs/roadmap.md ("The plan from T-A"), CLAUDE.md (the state paragraph; ccode's standing
  conventions), design_decisions.md (the entries named above; "T-D X", "T-D G", "T-D P", "T-D L",
  "T-D R and E", the MPB), docs/assumptions.md, docs/glossary.md, docs/TODOS_AND_DEFERRED.md.
- Instruments: analysis/ir_testbed/ (README, REPORT, the scripts), analysis/mpb/ (README, REPORT,
  coverage.md, authoring.md, the scripts).
- Domain: domains/dock_loading/ (skeleton), domains/kitting/ (the reference for every artefact form).
- Handoffs: docs/handoffs/ (T-D onward; G and X onward; Phase 7).
