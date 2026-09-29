# TeamRob handoff: from the test-bed / L / P / track 2.5 chat to the G-and-X chat

Written 29 September 2026 by cchat (the design chat) at the end of the chat that ran the IR test-bed
(track 1), cycle 2's L and P (with P4), the framework assumptions round and track 2.5. Everything named
here is committed on `main`; Hadi pushes before the new chat starts. Nothing is open in ccode.

## 0. How to use this document

- The repo is authoritative over this document. Before opening any question, the new chat verifies
  section 2 (state) and section 9 (open items) from the repo and reports every disagreement to Hadi.
  Files: `CLAUDE.md`, `docs/glossary.md`, `docs/design_decisions.md` (entries "T-D R and E", "The
  cognitive loop does not end with the task pool", "The IR test-bed", "T-D L: the belief lifecycle",
  "T-D P" with P4), `docs/assumptions.md`, `docs/TODOS_AND_DEFERRED.md` (TODO-119, 131 to 139, 95
  closed, 97, 96, 134), `docs/recognizer_handback.md`, `shared/io_contracts.md`,
  `analysis/ir_testbed/README.md` and `REPORT.md`, `analysis/l_build/REPORT.md`, the four maintained
  READMEs (`analysis/tb1a_destination`, `tb1b_two_tables`, `tb1c_realized_flip`, `tb3_full_reorder`).
- Terms come from `docs/glossary.md`. Beside every repo term, write its plain meaning once (section 1).
- This document carries what the repo does not: the reasoning state, candidate rules marked as
  candidates, parked items with their status, the process rules learned in this chat, and the pipeline.
- The previous handoff (`docs/handoffs/handoff_T-D_cycle2_and_IR_testbed.md`) is superseded by this one
  where they differ.

## 1. Working style, enforced in every reply (learned or confirmed in this chat)

- Scientific, literal, exact. Short sentences, one clause, the actor named. Itemised. No idioms. No
  em dashes in text drafted for Hadi.
- Every repo or glossary term gets its plain meaning beside it once ("the hypothesis with the highest
  probability (the leader)", "no hypothesis live (exhausted)", "fits / does not fit (adequate /
  inadequate)"). Hadi does not remember every term; a reminder written in codes (L2, G1, E7) is
  rejected. Never swap in an English synonym for an established term; if a concept has no term, flag
  it and propose one, recorded when its question is ruled.
- A design question is put one at a time: restate the problem in plain words, give the case with its
  ticks, list the alternatives, recommend one, ask explicitly. Independent questions may share one
  message; chained ones never.
- When Hadi asks for a table or a diagram, deliver a rendered one (the Visualizer or a PDF), never an
  ASCII or markdown table and never prose.
- Ruling sheets (a list of items to rule): numbered categories with items x.y, one row per item with
  a) keep, b) drop, c) short alternative, and cchat's recommendation letter; plain English; a rendered
  PDF table.
- Reflections Hadi pastes from another chat: take what clarifies or improves the decision, do not
  argue with them. Say which of its points changes something and which restates what is ruled.
- Reviewing a ccode report: show only what matters for the decisions and the design logic; read the
  behaviour in the picked runs, not only the test suite.
- Process per item: ccode report, cchat review, Hadi confirms, then the next session's prompt on its
  own. Never a review and a prompt in one message.
- Prompts: model and session line above a plain-text copiable snippet; the snippet holds only the
  prompt. From 29 September Hadi keeps ccode in auto mode: every prompt states its step in its first
  lines, "plan only, no code, wait for confirmation" or "build".
- Every records, plan and build prompt carries the why per ruling and the reviewer paragraph (below).
  Rulings are recorded and built as given; objections go to Hadi in the report.
- Verification scope: a few picked scenarios that exercise the rulings, at the oracle / CSV / figure /
  compare level; while the work is on the recognizer, picked from the test-bed rooms (layouts 10 and
  11); the maintained sets of layouts 1 to 9 stay a byte-level md5 regression check; the full pass only
  when a ruling touches the recognizer's evidence path. Two or three baseline runs where the
  meta-planner is the subject, not 48.
- Any prompt that edits shared fixtures or regenerates baselines includes the regression audit: every
  test, hash, manifest, snapshot and script that refers to the affected fixtures, verified identical or
  updated with a reason, every item's disposition reported.
- Case classification before mechanism: an intended phenomenon is designed; a boundary case is
  recorded (X keeps it as a study); an authoring artefact of an old fixture is corrected under the
  existing convention; a prior-off artefact never becomes framework semantics.
- Simplify by general semantics, never by excluding difficult cases (Hadi, closing the assumptions
  round): mid-action changes, a human walking toward the robot, and the pressure to communicate stay
  in scope; a scenario is added to demonstrate each.
- Test-beds are instruments: a README in `analysis/`, no design entries beyond rulings that change the
  framework, their rulings put to Hadi as a few one-line rules.
- Framework assumptions are Hadi's: cchat extracts candidates from the documents with their source and
  marks its own as proposals; nothing goes to ccode as a ruling until Hadi rules it.
- Handoff rule: a long chat finishes its bounded step, then hands off; the handoff is committed by
  ccode to `docs/handoffs/` and checked against the repo; the new chat verifies it before any question.

The reviewer paragraph, in every new-session prompt (a same-session follow-up opens with one line on
the push state instead):

> Every ruling below carries its reason. You are also its reviewer: before building, flag any ruling
> that is conceptually or logically wrong against its reason, or that conflicts with another ruling or
> a settled decision not marked superseded, one line each with the code lines; then build unless Hadi
> stops you. Disagreement on design grounds is wanted; the rulings are recorded and built as given, and
> objections go to Hadi in the plan and the report, not into the code. No hidden assumptions; no
> shortcut to reach a running state; nothing left untyped; no new string-level or key-matching checks
> or patches around the design; where the design does not cover a case, stop and ask. The entry's
> mechanism stands over runs, baselines and tests; a test expectation and the oracle change only by
> derivation from the entry; a disagreement is reported, not fitted. Prior ON is the primary set;
> prior OFF an appendix; no ruling rests on prior-OFF numbers alone. Headless, in the working
> environment CLAUDE.md names. Commit on main in logical groups; never push.

Environment note: ccode's auto-mode permission check has timed out twice ("no verdict"); it recovers by
retrying later. An allow rule for the interpreter in `.claude/settings.json` reduces how often the
check is needed (ccode's suggestion, not yet applied).

## 2. Where the work stands (verify from the repo)

Pipeline of tracks: 1 (done) → 2: L (done), P (done with P4) → 2.5 (done) → 2: G, X (next) → 3 → 4 →
demonstration and evaluation (T-E, T-F). Track 4 may move before track 3 if the evaluation scenarios
need a genuine departure from the workspace.

### 2.1 Track 1, the IR test-bed (closed)

Purpose: test the recognizer alone, robot idle, on scenarios written for it, with expectations derived
from the records before the run by an oracle that imports nothing from `shared/recognizer.py` or
`shared/likelihood_functions.py` (it may use the planner's decomposition; the expected-action table is
in the report). Comparison at 1e-9 against the public `BeliefState` read in-process; disagreements
classified as: the generator misread the records; the recognizer disagrees; the records do not
determine the value (only when they genuinely do not).

Artefacts (serial ids, per T-L ruling 4): `env_layout_10` (1000 × 1000, one table top centre, two
shelves symmetric, coffee machine bottom offset west, `corner_SE` only), `env_setup_08`,
`scenario_s08_01` to `_04`; `env_layout_11` (the same plus `kitting_table_1` and `shelf_3` at
(-420, 300), 30.4° from shelf_1 after a shallow run showed 10.4° does not separate), `env_setup_09`,
`scenario_s09_01` to `_13`. Run files in `configs/ir_testbed/`. The instrument is layout-independent:
`trajectory.py` (the human's per-tick path from the load-time replay expanded with the body's walker),
`oracle.py`, `actual.py`, `compare.py`, `plot.py`, `run.sh` (the run length from the replay plus a
30-tick idle margin derived from E5). Sessions: TB.1r records, TB.2b the cognitive-loop correction,
TB.3b layers 1 to 3, TB.4b layer 4 and the alternates, close-out.

Scenarios and what they hold: _01 two deliveries; _02 coffee between; _03 coffee after the pick-up;
_04 coffee after the first walk (empty-handed); _05 corner walk mid-carry (TODO-94); _06 the long
stand (TODO-95, now 3.4); _07 change of mind; _08 misdelivery to `kitting_table_1` (TODO-87);
_09 a delivery of an unassigned item (outside the support); _10 two west shelves (item_1 and item_3);
_11 the same with coffee between; _12 reversed order; _13 (track 2.5) the coffee break cut into the carry mid-walk
(T-H's `during` cut, PT28S, cut at 46).

Results: zero disagreements at every oracle comparison: 16 scenarios at TB and at L-build, 17 at track
2.5 (with s09_13); at P and P4 the test-bed logs were diffed, not compared (only the step-0 `[meta-proj]`
line differs). The oracle detects 7 of 8
single-rule alterations; E8's member clause is covered by E6's second amendment whenever the completion
latency is 1, so E8 is not exercised on its own (a body property, recorded).

Cognitive-loop correction (TB.2b, ruled (c)): observation and recognition run on every tick
unconditionally; `finished` (the robot's task pool is empty) guards only triggers, decision and
execution; no_current_task does not refire on a permanently empty pool. Consequence: `[IR]` lines
before `[meta-trig]` on every tick; the idle interval after the robot's completion was invisible in
every baseline before.

### 2.2 Cycle 2, L: the belief lifecycle (closed; entry "T-D L")

- L1, the boundary: fires when a terminal action's own completion condition becomes true for the
  observed agent (place: the released object rests at a container; wait_at: `waited(agent, ·)` starts
  holding). Read through the action's preconditions on the previous tick (one tick of derived state).
  A bare RELEASE is not a boundary. A terminal place is a boundary wherever it sits in a decomposition
  (the return of a change of mind, s09_07 at 33). The pin stays the world's terminal fact of a live
  hypothesis.
- L2, retraction: (i) recognizer unchanged, inadequacy attaches to the phase and is not retracted when
  behaviour becomes consistent again; (ii) `recognition_changed` fires when the recorded hypothesis's
  adequacy is INADEQUATE (state reading; never a rival's transition, never "no observation");
  (iii) "consistent again" is the next phase change, advance or regress.
- L3, resumption: no class exception; every terminal action is a boundary; the world carries the
  suspension (the held item re-derives both hypotheses); the belief near 0.5 after a break is genuine.
- L4, liveness: retirement lasts exactly as long as the terminal fact holds, read every tick; a
  returning hypothesis takes 1/|H|, the incumbents keep their proportions, origin at the current
  position, entry latency as a first observation; coffee is recognisable again once `waited` clears.
- L5, persistence: the world persists, the recognizer does not; the live set is a world function; a
  boundary re-initialisation fires `recognition_changed` (cause BOUNDARY, a flag on `BeliefState`).
- Trigger causes: ENTERED, REPLACED, BOUNDARY, RETRACTION; `[meta-trig]` prints `cause=`.
- Results (l_build): 16 agree; invariant 0 violations on 16,860 ticks; 0 false unexplained on modelled
  ticks; 23 retractions; TODO-118's frozen holds end (s01_01 off 201 → 186; s03_01 full_reorder off
  completes at 227); exhausted disappears on the coffee exit walks (unexplained instead).
- Consequence lines recorded: re-admission after a switch needs fresh evidence, about 15 ticks after
  a boundary (s09_01) and 14 after the change of mind (s09_07) at HEAD; a foreseeable hypothesis
  returns two ticks after its pin (the human's first step after the break) as a third rival. The
  boundary cause (`cause=boundary`) fired in none of the 52 L-build runs; the leader changed anyway at
  every boundary that met a recorded decision.

### 2.3 Cycle 2, P: the fallback projection (closed with P4; entry "T-D P")

- P1: when the gate refuses and a human is observed, a fallback projection (a `ProjectedPlan`,
  `Projector.project_fallback()`) exists; no human observed means none; the decision record stays
  empty; `[meta-proj] projection=fallback refused=<reason>`. First form ruled (b): stationary for the
  candidate's own duration, corrected to (2): a candidate needing a hold under a stand is refused
  (a shift only moves the violation to the projection's end; ccode's table with realize() unchanged).
- P2 (first): no motion extrapolation. Reopened by Hadi as a physical occupancy projection, then
  superseded by P4.
- P4, persistence-mirrored (rulings A to E in the P4 prompt): the robot's world model keeps per
  observed agent the last position, the last displacement, the current straight-run length
  (direction equality at the body's numerical resolution, slack 1e-9, not a margin) and the standing
  count, computed on `RobotAgent` from consecutive observations and written into the `WorldState`
  (`agent_displacements`, `agent_run_lengths`, `agent_standing_counts`; absent before a second
  observation); `WorldState.workspace` and `fixed_object_positions` from the builder (static layout
  facts). Moving: project the straight motion for as long as it has been maintained, cut where the
  ray meets the workspace boundary or enters the first fixed object's arrival radius (landmarks count
  as fixed objects: a code fact, `world_state_builder.py` puts every non-portable object in
  `fixed_object_positions`; recorded by the records step of section 11), no stand inferred after a cut. Standing: project standing for as long as it has
  stood. Beyond the projection the human is unassessed. realize() unchanged; every candidate gets a
  finite hold; the refusal rule, the wait state, the body's wait branch and the `HumanProjection`
  classes are removed. Q6: `projection_expired` is a third trigger (after `recognition_changed`), the
  expiry of the assessed span of the fallback the decision rested on (D3's "only two triggers" and
  D2's "one field" superseded). Q5 dissolved (no wait state). The doubling of holds against a standing
  human is emergent, never a rule.
- Results (P4): s05_01 back to 194 with the closest approach 58 cm (7 cm under the first P build);
  the occupied table (s01_06: the human's last delivery completes at 122; the first hold on the final
  stand at 141): the robot approaches, holds at 63 cm with lengthening holds
  48, 96, 192, 384 (800-step run), never completes while the human stands: X's occupied target,
  emerging as "approach and hold at the separation boundary" (recorded as a P4 consequence, not a
  rule). s03_01's 30 cm was the observation offset (the first step after a decision is unassessed,
  T3b/L2 entry), pre-existing; TODO-134 asks whether that offset applies to a fallback stand.
- P3 open: what the meta-planner projects when an admitted projection reaches its horizon at a
  non-terminal action (terminal endings are covered by L1's boundary within the completion latency;
  s05_01 tick 92, T_h 4, 6.96 cm, was the case). Not P's to build; parked.
- Ownership ruled: P is a short-term physical projection layer; G answers whether to reconsider;
  X answers what to do when nothing is realizable. Priority: admitted projection > (parked) union of
  adequate hypotheses > physical fallback.

### 2.4 Conceptual clarifications made in this chat (not all in the records; verify)

- IR's output channels every tick: the live set (non-empty / exhausted), the belief over it (relative;
  a lone hypothesis reads 1.0 on no evidence), the leader's adequacy (adequate / inadequate / no
  observation), the finding (adequate / unexplained / unresolved), the boundary flag. Plus the world
  channel (position, displacement, run, standing). "Admitted" is the gate's word, not IR's.
- The eight cases the gate meets and the alternatives per case were tabled (rendered table, 28 Sept);
  rows 1 to 8 are ruled; the open alternatives moved to G, X and TODO-97.
- Layers as they should be: the world (Mesa or reality; the human acts from its script); the robot
  body (sensors, actuators, the executor, the separation stop); the robot mind with perception (the
  robot's world model, a short record of change) and cognition (IR, meta-planner, projection,
  realization); shared domain knowledge. Today `world_state_builder.py` in `mesa_sim/` reads Mesa's
  ground truth and hands the mind a finished `WorldState`; there is no perception module and no
  robot-mind object; the mind's components are attributes of the Mesa `RobotAgent`. Ruled: the
  `WorldState` is understood as the robot's world model; perception facts (displacement, run, standing
  count) are the robot's, held on `RobotAgent` until a mind object exists (TODO-131, see 9.4); the
  mind keeps a bounded record (four numbers), never a history. Track 4 is where the perception layer
  lands (the observable area is its first rule).
- Union projection (plan against every adequate hypothesis's plan when none is above θ) is a
  belief-aware planning move, parked under TODO-97 (which today records only the covering-set union;
  the two variants are a chat decision, recorded by the records step of section 11):
  the fit-set variant (all adequate) and the belief-weighted variant; the case that decides between
  them is a hypothesis adequate for one tick with almost no probability.

### 2.5 Track 2.5: assumptions and fixtures (closed)

- `docs/assumptions.md`: accepted 1.1 to 1.4, 2.2 to 2.6, 3.2 to 3.4, 4.2, 4.4 to 4.6, 5.1, 5.2, each
  with kind, source, effect; rejected or dropped: 2.1, 3.1, 3.5, 4.1 (reframed as 4.6), 4.3
  (a P4 consequence), A2. Read it before G and X.
- 1.1: baseline scripts end with the human leaving the shared workspace (implemented as
  `go_to("corner_SE")`; the human stays observed at the corner); the six regression scripts corrected
  (s01_01, s02_01, s03_01, s01_06, s04_01, s06_03), `corner_SE` added to layouts 02 and 08, baselines
  regenerated once ("2.5" README sections, F1 classes per run via
  `analysis/tb1a_destination/sep_classes.py`). All twelve former occupied-target logs complete
  (174 to 384). Unedited scenarios byte-identical.
- 3.4: a stand inside a task is a pause while within the standing its derived phase (the task's
  current step) prices (E9, E10); beyond that the derived phase does not fit and, with no other fit,
  the finding is unexplained; standing
  contributes no hypothesis-specific evidence while the hypotheses price it equally; any movement of
  the probabilities comes from the evidence function, not from one hypothesis explaining the stand
  better. No stay hypothesis. TODO-95 closed; its levels moved (level 1 built as P; 2 and 3 to X; the
  sustained stand to TODO-132 (b)). G's former question 7 is gone.
- 4.6: near-encounters are an evaluation measure (F1's viol / stand / recede), IR planner (realized)
  against no-IR (plain; the fallback-only control does not exist yet, TODO-137); the execution stop is
  for demonstrations, off for evaluation. First instance recorded: s01_06 tick 147, 5.23 cm, the exit
  walk through a holding robot, no robot violation (TODO-135).
- s09_13 built and compared: the cut at 46; the delivery inadequate at 55, unexplained; the coffee
  break at θ at 67 but not fitting until its wait at 74; the resumed delivery at θ 14 ticks after it
  resumes at 107. Recognition side only; the planning side is track 3.
- New TODOs: 135 (near-encounter scenario, with X), 136 (the reactive human), 137 (fallback-only
  control), 138 (the horizon of runs where the robot has work; s04_01's 16-tick margin), 139 (align
  the default prior with 1.4; `configs/experiment.yaml` still has `assignment_prior: false`).

## 3. What G is about, in plain words

The recognizer gives the meta-planner, every tick, the probabilities of the human's possible tasks and,
per task, whether the human's current movement fits it. The meta-planner accepts (admits) the most
probable task only if its probability is at least θ and it fits; it re-decides when that task is
replaced, when the human finishes a task (a boundary), when the accepted task stops fitting
(retraction), and when the fallback it planned against runs out (expiry). When it accepts nothing it
plans against the physical fallback (P4). G settles what should count as evidence for accepting, and
whether any further re-decision is needed.

## 4. G's questions (two remain; take them in this order)

G Q1, admission on no evidence. When one task is left live, its probability reads 1.0 because nothing
else is live; at the start of any phase, "fits" is vacuous (S = 1 with nothing to contradict it). So the
gate admits on a probability that is 1.0 by bookkeeping and a fit that is true by absence of evidence.
Cases: s09_01 after 124 (coffee lone at 0.997, admitted at once; unexplained from 157); the baselines
after the work order (P report: s05_01's coffee admitted on the tick after the boundary, then retracted);
every reset tick + 1 with a lone hypothesis.
Alternatives Hadi listed as initial: (a) admit as now; (b) require some positive observation before
admission; (c) distinguish "adequate because evidence supports it" from "not yet contradicted", and only
the former permits admission. Hadi favoured (c) initially.
cchat's candidate rule (a candidate, not ruled): "adequate by evidence" = the human has made progress in
the task's current step (walked toward its target, i.e. C(o,g) − C(p,g) > 0 within the phase, or
completed the step); progress is already computed inside the excess-path test, so no constant. Under it
the lone coffee after the work order is not admitted (no progress toward the machine) and the grasp
flicker is not either (a rival's stationary step gets no progress from someone else's grasp). Check
first whether the existing D / S / L machinery already gives the distinction (Hadi's instruction) before
adding anything; state what "progress" is for a stationary step (its completion event) and for a walk.

G Q2, short-lived fit. A task can fit for one or two ticks by accident: after a grasp, a rival delivery's
next step is `place(held item, its shelf)`, a stationary step satisfied by the grasp's own stationary
ticks (S = 1). Cases: s09_09 flicker (unexplained 83, adequate 84, unexplained 86, adequate 87);
coffee re-entering within 30 cm of the machine as an adequate member for a tick or two (P4 flag).
Whether such a fit should count for admission, for retraction, or for the finding, without a count
constant. Hadi's alternatives: any phase-consistent observation contributes evidence immediately;
admission requires evidence that crosses an existing criterion, no persistence count; distinguish
structural fit at phase entry from discriminating evidence. The candidate rule of Q1 covers Q2 if it
holds; test it on both cases.

Withdrawn or answered before G: the reset tick as a separate question (adequacy already refuses on the
boundary tick; the two decisions per boundary are Q1's churn); staleness of a fallback and the wait
(P4's expiry trigger; TODO-132 (a) ruled for fallbacks); a projection ending at a non-terminal action
(P3, parked); the long stand (3.4, closed).

Open under G's track but not G's rulings: TODO-132 (b) the sustained stand (now: the fallback carries
it; revisit only if a case needs more); TODO-119's G part (the lone-hypothesis admission at b + 1 is
Q1); TODO-134 (the observation offset on a fallback stand); TODO-97 belief-aware planning with the
union variants (parked).

G's sessions: G-records, G-build, G-review; the build's verification on picked scenarios only
(s09_01 tail, s09_09, s09_06, s05_01 prior on, one control scenario), with the oracle unchanged unless
a ruling touches the recognizer; the maintained sets as md5 regression plus one completion table.

## 5. X's questions (after G)

X is response policy: what the robot does when the projection leaves it nothing to do or when
execution meets the human.
- The occupied target: a human standing where the robot must work. P4 gives "approach and hold at the
  separation boundary with lengthening holds" (s01_06). X decides the alternatives: switch to another
  task; communicate (TODO-96, no channel exists); keep holding. TODO-95's levels 2 and 3 live here.
- The blocked route: a category (a human standing on the robot's only route with the target free);
  no current instance since P2 (s02_01 completes); not a glossary term.
- The human walking toward the robot (assumption 4.6; TODO-135; the s01_06 5.23 cm instance): kept as
  an evaluation case that forces the communication question; near-encounters counted per F1.
- The blocked event: the recorded design (WAIT against RECONSIDER when the separation stop refuses a
  step) applies to stop-on runs only; evaluation runs with the stop off.
- What the robot does after a retraction beyond the fallback (today: the fallback and its holds).
- The reactive human (TODO-136) is future work, not X.

## 6. Track 3: the meta-planner test-bed (after X)

Rooms like layouts 10 and 11 with the robot given its own deliveries; layers in the same order (assigned
only, a foreseeable task between, the deviations); one scenario per decision to expose (an admission, a
hold, a retraction, a boundary re-admission, a lone-hypothesis projection after the work order, a
blocked target, the planning side of the mid-action change). Its oracle is the decision rule from the
human's trajectory and the belief; it needs the oracle extension that reads a run log's world with the
robot's acts (the existing oracle's world holds only the human's facts). Recorded as a TODO (the
number to verify).

## 7. Track 4: the workspace boundary and human departure (after 3, or before if evaluation needs it)

Hadi's framing: extend the environment so the shared work area has a boundary and the human can pass
through a door into an outside area (a corridor or rest area); the script's terminal primitive becomes
`leave()`; whether the outside area is observable is a track 4 design question (observable: the human
is seen but outside the robot's operational area; unobservable: the first genuine "no human observed").
Principle ruled: the robot's observation is restricted to what it can sense from its area; a human
outside is an absence of observation, never a message; departure and re-entry are emergent (observed,
not observed, observed again; a returning human has no memory in the mind). Consequences: this is the
first case where the robot's world model must differ from the simulator's state, so track 4 builds the
perception layer (the robot's own world model, the mind object); P4's fallback then uses the shared
work area's boundary; the six corrected scripts and the test-bed scripts switch to `leave()` then, with
one regeneration. Until then 1.1's corner walk stands.

## 8. Insights to carry (from the reports, for the paper and for design)

- The implementation is faithful to the records: zero disagreements at 1e-9 at every oracle
  comparison (16 scenarios at TB and L-build, 17 at track 2.5); a
  disagreement between what we want and what we see is a design question, not a bug hunt.
- Belief and adequacy are independent as R3 intended: the stand moves the finding and not the belief
  (s09_06); a confidently wrong belief with an unexplained finding (s09_09, coffee at 0.97 with no walk
  to the machine); θ cleared while inadequate (s09_05 at 87), the case G1 exists for.
- The belief's resolution is bounded by geometry: two targets 10.4° apart are not separated by a
  28-tick walk; 30.4° separates them three ticks before arrival; nearby targets are decided by the
  grasp, not the walk.
- A detour is a permanent charge within a phase (e stays constant on the way back); L2 accepted that
  cost: a resumed carry is unprojected until its advance (46 ticks in s09_05).
- Every grasp gives the rivals a free adequate tick (the `deliver_with_return` expansion meets E6's
  amendment); adequacy is local to the current phase.
- Little evidence protects little (P4): a human one step into a walk is projected 20 cm; the body's
  stop and X cover the residual; the evaluation counts it.
- After the work order the honest reading is unexplained (a foreseeable task live, no walk to it),
  the same in every scenario since L4.

## 9. Open items and parked items, with status (verify the TODO numbers in the repo)

9.1 G Q1 and Q2 (section 4), with the candidate rule.
9.2 X (section 5).
9.3 P3 (an admitted projection ending at a non-terminal action), parked, recorded in the P entry.
9.4 TODO-131, the robot-mind object and perception layer in `shared/`. "Lands in track 4" is this
    chat's decision, not yet in the TODO's text; recorded by the records step of section 11.
9.5 TODO-134, the observation offset on a fallback stand; its case (s03_01, 30.12 cm) no longer
    occurs in the maintained sets after the exit walks (track 2.5 note); the question stays open.
9.6 TODO-97 belief-aware planning with the union's two variants (fit-set, belief-weighted), parked;
    the variants recorded by the records step of section 11.
9.7 TODO-137 fallback-only control; TODO-138 the horizon with a working robot; TODO-139 the default
    prior (change it in its own step, since every hand run and test expectation moves).
9.8 TODO-129: a retired hypothesis whose terminal fact cannot be read stays retired (from L-build's
    BUILT paragraph, recorded in the P records).
9.9 The "leave the workspace" foreseeable task as a domain addition: proposed and declined for now
    (option (a), keep unmodelled); revisit with track 4 or the demonstration. A chat decision, in no
    record until the records step of section 11.
9.10 `docs/env_layouts_png/` screenshots are stale (old ids, no `corner_SE` on 02 and 08); cosmetic.
9.11 E8 not exercisable on its own with completion latency 1; a design note, no action.
9.12 The IR test-bed README has no P4 md5 section and no track 2.5 md5s for the 16 earlier runs (only
    s09_13's are recorded); the local logs differ from L-build's only in the step-0 line.

## 10. Provenance of what this document says

Three kinds of statement appear here: repo facts (verified by ccode at commit e0028dd), recorded
decisions (in the entries and TODOs named), and decisions made in the preceding chat that were in no
record when this document was first written. The third kind is marked "chat decision" and is recorded
by the records step of section 11, after which the repo holds them too.

## 11. Records step at the handoff (ccode, one commit, before the new chat starts)

- TODO-97: add the union projection's two variants (the fit-set variant over all adequate hypotheses;
  the belief-weighted variant) and the case that decides between them (a hypothesis adequate for one
  tick with almost no probability); parked.
- TODO-131: add that the perception layer and the mind object land in track 4, whose observable-area
  rule is their first case.
- The track 4 TODO: add that a "leave the workspace" foreseeable task was proposed and declined for
  now (the exit walk stays unmodelled; option (a)); revisit with track 4 or the demonstration.
- The P entry (P4): one line that landmarks count as fixed objects for the fallback's tail
  (`world_state_builder.py` puts every non-portable object in `fixed_object_positions`).
- Then verify sections 2 and 9 of this document against the repo once more and report.

## 12. First message of the new chat (what Hadi asked for)

Show, itemised and in plain words: the pipeline zoomed out (section 2's first paragraph), then where
each track stands, then G's two questions with their cases, then the verification of this handoff
against the repo with every disagreement, then stop and wait. Open G Q1 only when Hadi says so, one
question at a time, alternatives and a recommendation, no ccode prompt until Hadi says so.
