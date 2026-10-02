# Record of planning and building: T-D, robustness in kitting (R and E, the cognitive loop, the IR test-bed, L, P, G, X, the MPB)

Moved verbatim from `docs/design_decisions.md` on 2 October 2026 (Hadi's ruling of that day: one record file per task;
the conceptual design stays in design_decisions.md). Each block is headed by the title of the entry it comes from
and its id; in design_decisions.md an index line with the same id stands where the block was.

**T-D R and E: the recognizer's output under a removed `unknown` hypothesis (ruled by Hadi, 26 to 27 September 2026)** — RECORD [T-D/1], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
- Dependencies to verify in the build, not design questions: the schema durations of `pick_up` and `place`; the body's speed and its duration-to-ticks conversion supplied to the adequacy computation (the Projector already receives both); β remains body-supplied as established in T-A1.

Staging (ruled).
- Stage 1: this record; then build the recognizer side and regenerate the baselines. The gate is left exactly as it is; its input changes meaning (the leader's share over H), so admissions are expected to shift; the shift is measured, not corrected. Verify: the arithmetic invariant of R6; recognizer outputs per ground-truth case against oracle IR (TODO-101); admissions before and after on the maintained baseline sets (`analysis/tb1a_destination/`, `analysis/tb1b_two_tables/`, `analysis/tb1c_realized_flip/`, `analysis/tb3_full_reorder/`: 48 logs, 36 distinct by md5); false-unexplained per phase and per run, missed findings, detection delay, at every α.
- Cycle 1.5 (ruled 27 September 2026, on Stage 1's verification): 1.5b builds E8, E9, E10 and G1 together; acceptance is 1.4's scripts rerun on the regenerated baselines ("1.5 rulings", below).
- Then L (boundary at a misdelivery, retraction, resumption), P (projection from observation; the moving human; the staleness trigger), G (consumption of belief, finding and lifecycle; TODO-97 on its own gate), X (WAIT against RECONSIDER; the occupied target; communication on a persistent finding). Each ruled on Stage 1's results, recorded before its build. The relation to Alternative 1 stays open. T-D Q1 (option 1) is unchanged and is P's building block.

For the Stage 1 build: the docstring of `UNKNOWN_LIKELIHOOD` ("the threshold separating unexplained from a real hypothesis") is false under R; the registry's reserved "duration" evaluator is not what E builds, since time enters adequacy and not the belief's likelihood. The log reason `none(unresolved)` is renamed in the Stage 1 build, since it collides with the finding's value unresolved; the string is chosen there.

**T-D R and E: the recognizer's output under a removed `unknown` hypothesis (ruled by Hadi, 26 to 27 September 2026)** — RECORD [T-D/2], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
  CYCLE 2 INPUT (1.5c; with 1.5b finding 3, TODO-119): under the second E6 amendment a lone hypothesis is admitted at
  b + 1, on a belief of 1.0 by normalisation and one priced standing tick (its latency tick is an observation with
  S = 1). The boundary admissions of 1.5b (at b + 2) move one tick earlier; they are expected and listed in
  `analysis/td_stage1b/REPORT.md`, section 1.5c.

**T-D R and E: the recognizer's output under a removed `unknown` hypothesis (ruled by Hadi, 26 to 27 September 2026)** — RECORD [T-D/3], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
Staging, cycle 1.5: session 1.5r records these rulings (records only). Cycle 1.5b builds E8, E9, E10 and G1 together;
acceptance is 1.4's scripts (`analysis/td_stage1/`) rerun on the regenerated baselines.

**The cognitive loop does not end with the task pool (TB, ruled by Hadi, 27 September 2026)** — RECORD [T-D/4], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
Consequences recorded.
- After the terminal return the body calls neither `evaluate_triggers` nor the executor. The existing baselines stay
  byte-identical once every `[IR*]` line is removed, and their `[IR*]` lines stay byte-identical up to and including
  the declared completion tick; the new lines begin the tick after it and include `[IR-complete]` and `[IR-boundary]`
  as well as `[IR]` and `[IR-dist]`. (Refined in TB.2b records, Hadi on the TB.1r report, 27 September 2026.)
- Within a tick, the robot's `[IR]` and `[IR-dist]` lines now precede its `[meta-trig]` line, on every tick (observation,
  recognition and their logging come before the guard, the guard before the trigger evaluation); before TB.2b the
  `[meta-trig]` line came first. Every log's md5 changes with it, a run whose robot never finishes included; the
  comparison above is unaffected. (TB.2b plan, confirmed by Hadi.)
- The 1.4 and 1.5b measurements (`analysis/td_stage1/`, `analysis/td_stage1b/`) were taken over the truncated
  interval. They are rerun over the newly exposed interval in TB.2b, with every change reported and no previous
  statistic preserved for comparability (TODO-121).
- With an empty pool, tick 0 still produces one `no_current_task`, one `[meta-proj]` line and one "all tasks complete"
  line.
- TODO-33 (the run loop does not stop when all agents are finished) is untouched: the run's length is the run file's
  steps.

**The IR test-bed (TB, ruled by Hadi, 27 September 2026)** — RECORD [T-D/5], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
Purpose. Test the recognizer in isolation on scenarios written for it, with expectations derived from the entry "T-D
R and E" before the run, so that a result can say "the recognizer disagrees with the design" rather than "the run looks
odd". The 48 maintained fixtures cannot: the robot acts in them, the layouts vary, and the cases Design B was ruled for
(the corner walk, a switch outside the support) are absent (TODO-101's note). Hadi's requirement: the simplest cases
first, to see whether the new design produces what we expect.

Rules.
- The layout is not designed to produce a desired IR result. Its geometric consequences are stated and feed the
  independently derived expectations; an unexpected recognizer behaviour on a resulting trajectory is evidence to
  investigate, never a reason to adjust the layout.
- A test-bed finding enters a cycle as a design question with its ticks, as 1.4's findings did; it never changes the
  mechanism on its own.
- Any result that contradicts E5's reference distribution or E10's unit is a cycle 1 reopening, put to Hadi as such.

The layout (the room). Deliberately simple, square, the proportions from Hadi's sketch, to be kept (a distance is
adjusted only if a derivation needs it; never rearranged):
- one kitting_table KT at the top centre;
- two shelves, west and east, at the same height, symmetric about KT's vertical axis;
- the coffee machine near the south wall, offset west of centre;
- one landmark, corner_SE, the exit walk's target; no other corner and no door (landmarks are optional under the layout
  rule);
- no AC switch, so no `ac_activation` hypothesis exists in this room.
Stated consequences:
- from KT the two delivery hypotheses have equal path cost, so the first walk separates them by excess alone;
- the coffee machine's bearing from KT differs from corner_SE's, so a walk to the machine and the exit walk are
  distinguishable;
- with the prior on, the hypothesis space is the two deliveries plus `coffee_break`. `coffee_break` is retired for the
  run once `waited` holds (the completion pin, `docs/recognizer_handback.md` §1.6), so in the three coffee scenarios no
  hypothesis is live after the second delivery: the lifecycle reads exhausted and the exit walk has no finding. Only
  in the two-deliveries scenario (`scenario_s08_01`) is `coffee_break` the lone live hypothesis after both deliveries,
  at 1.0 by normalisation, and the exit walk is charged against its walk to the machine (TODO-117's case by
  construction).
  SUPERSEDED (T-D L4, ruled 27 September 2026, built in L-build): `coffee_break` is retired while `waited` holds, not
  for the run; it is live again the tick `waited` clears, so after the work order it is the lone live hypothesis in
  every scenario and the exit walk reads unexplained. design_decisions.md, "T-D L: the belief lifecycle", L4.

The setup (the shift). item_1 on the west shelf, item_2 on the east shelf, both designated to KT.

The scenarios. Prior ON in every run. The robot at the top left with an empty task pool (`assigned_tasks` empty),
observing the human. The human starts at KT, assigned `deliver_item(item_1)` and `deliver_item(item_2)`, never in an
order. Every script ends with the exit walk to corner_SE (the authoring convention), which is itself an unmodelled walk
and part of every expectation.
1. `scenario_s08_01` (two deliveries): deliver item_1, deliver item_2, exit.
2. `scenario_s08_02` (coffee between): deliver item_1, `coffee_break`, deliver item_2, exit.
3a. `scenario_s08_03` (coffee after the pick-up): `coffee_break` started after the `pick_up` of item_1 (the item in
   hand during the break; resumption re-expands the carry), then deliver item_2, exit.
3b. `scenario_s08_04` (coffee before the pick-up): `coffee_break` started after the first `move_to` of item_1's
   delivery, before its `pick_up` (empty-handed at the shelf; resumption re-expands the walk back to the shelf, then
   the pick-up), then deliver item_2, exit.
3a and 3b are separate scenarios because they test different suspended task states, not parameter variations of one
scenario. Both are L's subject; their expectations are generated mechanically from the current entry, and the test-bed
does not resolve L. The deviations (the corner walk, a switch outside the support, the wrong table, the long stand,
the finished assigned tasks) are authored later with P and X (TODO-122).
Ids: serial, as every existing artefact: the layout `env_layout_10`, the setup `env_setup_08`, and the scenario ids
above (`scenario_s08_01` to `scenario_s08_04`, in the order listed); each scenario's purpose is stated in its
`description` field. The
coffee break's duration is the schema's; no scenario constant. One run file per scenario: steps enough to include the
exit walk, `separation_stop` off, `test_level` 0.05, `assignment_prior` on.

The expectations. Per scenario one CSV:
- per tick, per live hypothesis: the expected action (derived phase), the origin, e, s, s_exp, D, L, the normalised
  belief value, S, member, hypothesis adequacy;
- per tick: the human's position, the world facts the phase rule reads, the finding, the lifecycle state, the pin and
  boundary ticks.
Two files per scenario, expected and actual, and a diff. The source of the human's trajectory and world facts is the
load-time replay (`check_script`), expanded per tick with the body's walker (`steps_toward`, the step size, the
proximity threshold, the action and task latencies). TB.3b asserts per-tick equality of that trajectory with the run's
human lines; if the assertion fails, the generator reads the run's human lines instead and the report says so.
Independence boundary. The generator implements the belief from all recognizer records at HEAD, not from one entry:
this file's "T-D R and E" (e as the straight-line excess from the origin, s, s_exp by E9's attribution, D, L clipped
at 1, S, membership as amended twice with the boundary-tick rule, the finding) and `docs/recognizer_handback.md`
§§1.2 to 1.7 (the uniform prior, the proximity regress, the fold and prefix accumulation, the normalisation over H,
the completion signal, the pin, the boundary and the retirement, `BELIEF_FLOOR`, target resolution for a carried
item). The TB.3b report lists each rule the generator implements with its source. It imports nothing from
`shared/recognizer.py` or `shared/likelihood_functions.py`. It may use the planner's decomposition and the domain's method guards to obtain each hypothesis's expected action sequence, which is
the domain's structure, not the recognizer's. The expected-action table per hypothesis per scenario is written out in
the report, so the oracle is inspectable.

The comparison.
- Categorical values (expected action, member, hypothesis adequacy, finding, lifecycle, most_likely, pin and boundary
  ticks) exactly; numeric values at relative tolerance 1e-9.
- Every disagreement is listed with its tick and classified as one of: the generator misread the entry; the recognizer
  disagrees with the entry; the entry does not determine the expected value for that case. "The entry is silent" is
  used only when the entry genuinely does not determine the value, never for a case the generator finds unspecified or
  inconvenient.
- No same-session adjustment of the generator or the recognizer to make the comparison pass; the standing rule
  applies (the entry's mechanism stands over runs, baselines and tests; a disagreement is reported, not fitted).
- The report distinguishes "the recognizer currently behaves this way" from "this behaviour is correct by the current
  design".

Sessions (the TB track; the IR test-bed first, cycle 2 (L) second): TB.1r records these rulings and the cognitive-loop
ruling (records only); TB.2b builds the cognitive-loop correction ("The cognitive loop does not end with the task
pool", above), which the test-bed's runs need; TB.3b builds the artefacts and the expectation generator, runs the
scenarios and writes the report.

CORRECTED IN PLACE (TB.2b records; Hadi on the TB.1r report, 27 September 2026): the landmarks (corner_SE only, no
door; TB.1r had them required), the ids (serial; TB.1r had descriptive ids), the generator's source (all recognizer
records at HEAD; TB.1r had the one entry), the trajectory (the replay expanded per tick with the body's walker, and the
fallback to the run's human lines), and the third stated consequence (`coffee_break` is retired once `waited` holds, so
TODO-117's case arises in the two-deliveries scenario only; TB.1r had it in every scenario).

Files: domains/kitting/ (the layout, setup and scenarios, hand-written literals registered by discovery), the run files
where T-L keeps them, analysis/ir_testbed/ (the generator, the log reader reusing `analysis/td_stage1b/tdlib.py`,
expected.csv, actual.csv and diff.md per scenario, REPORT.md). Built in TB.2b and TB.3b.
Reference: cchat, 27 September 2026 (TB); "T-D R and E" (R1 to R6, E1 to E10, G1, the membership rule as amended
twice); "Layouts, setups and scenarios: the three artefacts of a run"; "T-H: the human behaviour model";
`docs/handoff_T-D_cycle2_and_IR_testbed.md` §8 (the layered plan); TODO-101, TODO-117, TODO-122;
`docs/recognizer_handback.md` §1.10

TRACK COMPLETE (TB close-out, 27 September 2026): TB.2b, TB.3b and TB.4b are built; sixteen scenarios (scenario_s08_01
to _04 on env_layout_10, scenario_s09_01 to _12 on env_layout_11), zero disagreements at 1e-9 between the recognizer's
public outputs and the independent oracle; the instrument is independent of the layout, and its record is
`analysis/ir_testbed/README.md` (the results in `REPORT.md`). Two facts for cycle 2, stated without ruling: (1) E8's
member clause is covered by E6's second amendment whenever the action completion latency is 1 (every phase an advance
opens then has s_exp ≥ 1, so its entry tick is already a member; removing the clause changed no output in TB.3b); (2) at
the current β (0.01 /cm) and v (20 cm/tick), two targets 10.4° apart as seen from the start are not separated by a
28-tick walk (the rival's S 0.765 at the arrival), while 30.4° separates them three ticks before the arrival (S < α at
tick 25 of 28; scenario_s09_10, shallow runs of TB.4b).

---

**T-D L: the belief lifecycle (ruled by Hadi, 27 September 2026)** — RECORD [T-D/6], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
Staging for L-build. The recognizer (L1, L4) and the meta-planner (L2 ii) are built; the IR test-bed's oracle is
updated by derivation from this entry (not fitted to the runs); the sixteen test-bed scenarios (scenario_s08_01 to _04,
scenario_s09_01 to _12) are recompared; the four maintained baseline sets are regenerated; the 1.5c and TB.2b measures
are rerun; every moved number is reported.

BUILT (L-build, 28 September 2026): c4beb1d (records), 2c54c4a (L1, L4, the flag: `ProceduralKnowledge.
terminal_actions`, `AdaptivePlanner.enabled_groundings` / `completed_groundings`, `_observed_terminal_completion`,
`_retired`), 493c095 (L2 (ii), L5 B: `RecognitionChange`, `TriggerDecision.cause`), 5129d90 and 3d65ca6 (the re-entry
kept in hypothesis order, the tie-break; found by the IR test-bed), 013cd35 (tests). Verified: `analysis/l_build/
REPORT.md` and `analysis/ir_testbed/REPORT.md`, "L-build" (the sixteen agree with the derived generator at 1e-9). Two
readings stated there: a retired hypothesis the planner cannot decompose stays retired (its fact cannot be read); L5 B
fired in no baseline run (at every boundary that met a record, most_likely changed). Measured wording: `coffee_break`
re-enters on the tick `waited` clears, the human's first step after the break, two ticks after its pin (133 → 135 in
scenario_s09_02); "one tick after its break" above reads so.

**T-D P: the fallback projection (ruled by Hadi, 28 September 2026)** — RECORD [T-D/7], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
  As first ruled: the wait, a mechanical consequence of P1: a planner outcome, not a terminal state. `update()` returns no current task
  with the whole pool as the queue; the terminal return is no current task AND an empty queue, and the body tests both.
  The body executes the wait by running no plan that tick. Completion ticks the body already owes (T-B Q7) are kept:
  the wait carries them as a hold carries them (the robot standing where the decision found it), and what a wait does
  not spend passes to the next plan loaded.

**T-D P: the fallback projection (ruled by Hadi, 28 September 2026)** — RECORD [T-D/8], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
- Confirmed at the P plan step: the types (`HumanProjection`: `AdmittedProjection`, `FallbackProjection`);
  `ProjectedPlanEntry.abstract_plan` Optional, None only for the fallback's entry; "a human observed" = a
  `human_agent_id` and a position for it in the world; unprojectable → the fallback, the record empty; the logs
  (`[meta-proj] … projection=fallback refused=<reason>`, `[meta-b2]` the admission's reason, `[meta-b3]`'s T_h the
  winner's).

**T-D P: the fallback projection (ruled by Hadi, 28 September 2026)** — RECORD [T-D/9], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
The deadlock (ruled (b); measured on the P-build baselines, under P2 as ruled). 16 of the 48 maintained logs end in a
wait that never ends, all an OCCUPIED TARGET: five scripts end with the human standing at the robot's delivery table
while the robot's last task delivers there (scenario_s01_01, s03_01, s01_06, s04_01, s06_03). T-C2c's authoring
convention covers new scenarios only, and these predate it: no retroactive scope change, the scripts are not edited.
The READMEs record "waits: occupied target (X)" in place of a completion tick; the case carries into X. Under the first
P2 (stationary only) scenario_s02_01 waited too, at a BLOCKED ROUTE (the human standing at ac_switch_0, 145 cm from
shelf_1, the robot's walk there within `min_separation` of it); under P2 as ruled it completes in both priors (425 /
428), the robot's earlier decisions having moved. The blocked route has no instance in the fixtures; it stays one of
X's categories beside the occupied target, not a glossary term.
SUPERSEDED IN PART (Track 2.5, ruled by Hadi 28 Sept 2026): "no retroactive scope change, the scripts are not edited" no
longer holds. docs/assumptions.md 1.1 extends the authoring convention to the regression fixtures whose terminal stand
is not their purpose; the six scripts end with the exit walk (52295f7), and the twelve occupied-target logs of P4 now
complete (the maintained READMEs, "2.5"). The occupied target stays X's case, now with no instance in the fixtures.

**T-D P: the fallback projection (ruled by Hadi, 28 September 2026)** — RECORD [T-D/10], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
Consequence of ruling 3 (the candidate's own horizon), recorded: a fallback can refuse every candidate at a decision
while the human walks, and the robot then waits by polling until the tail frees one. scenario_s05_01 under
`full_reorder` waits 23 ticks from tick 0 in both priors (every ordering refused under the human's moving tail). It is
evidence for G's staleness question (TODO-132), not a defect of P.

**T-D P: the fallback projection (ruled by Hadi, 28 September 2026)** — RECORD [T-D/11], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
MEASURED AT (recorded at G-records, 29 Sept 2026; design_decisions.md, "T-D G: admission"): the cited case was
measured on the P-build baselines (fa26176) and does not occur under P4 and Track 2.5 (verified 29 Sept 2026 at
a412b39: tick 92 has no decision; the run's minimum `[sep]` is 58.31 cm at tick 25). P3 stays parked, with no instance
in the maintained sets.

**T-D P: the fallback projection (ruled by Hadi, 28 September 2026)** — RECORD [T-D/12], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
BUILT (P-build, 28 September 2026): b19b5e2 and 4470708 (records), e93cbd9 (the build), 5e853a0 (tests;
tests/test_p_build.py, and four tests re-derived by P), 15cb99f (TB.2b's mid-run pool test moved to scenario_s03_06),
fa26176 (the four maintained sets, a "P-build" section each). Verified on the P-build baselines: `.rec` streams
byte-identical in all 48; the recognizer's lines byte-identical prior on; the first difference of every changed run at
tick 0, a decision under the fallback; the IR test-bed's sixteen logs differ in the step-0 `[meta-proj]` line alone
(no oracle rerun: the recognizer is untouched and the robot is idle there). Measured, not examined: scenario_s06_01
`single_task` prior off does not finish in 340 steps, with no wait (TODO-133). P is closed; next is G.
SUPERSEDED: P was reopened by P4 and closed with it (BUILT (P4-build), below).

BUILT (P4-build, 28 September 2026): 57600e2 (records: P4, Q6, the superseding notes), 179a503 (the build: the
perception facts on `RobotAgent`, `Projector.project_fallback()` from the evidence, the record's second value and
`projection_expired`; the refusal, the wait, the body's wait branch, the executor's wait handling and the
`HumanProjection` types removed), f0ead6e (tests; tests/test_p_build.py re-derived, the three "refusal returns None"
tests back to None, the WorldState field set), d7c98b5 (the four maintained sets, a "P4-build" section each;
TODO-133 closed). Verified: `.rec` streams byte-identical in all 48; the recognizer's lines prior on byte-identical to
L-build's; the IR test-bed's sixteen logs differ in the step-0 `[meta-proj]` line alone; the suite 170 passed.
Accepted on scenario_s05_01 (the 23-tick wait gone under both strategies; complete at 194 as before P),
scenario_s01_06 and scenario_s06_06 (complete at 265, `[sep]` 26.0 cm, as before P).
- The occupied target, under P4: six prior-on logs do not complete (and the same six prior off): scenario_s01_01,
  scenario_s03_01 (`single_task` and `full_reorder`, in `analysis/tb1a_destination/` and `analysis/tb3_full_reorder/`),
  scenario_s01_06 and scenario_s04_01. The human's script ends standing at the robot's delivery table; the robot holds
  and reconsiders at each expiry of a longer stand (scenario_s01_06 prior on, 800 steps: expiries at 165, 213, 309,
  501, holds 48, 96, 192, 384, 63.42 cm from the human, never complete). The READMEs record "does not complete:
  occupied target (X), holds lengthening, from <first hold on the final stand>". The case is X's.

**T-D P: the fallback projection (ruled by Hadi, 28 September 2026)** — RECORD [T-D/13], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
- The observation-offset gap, recorded (scenario_s03_01 `single_task`, both priors, `[sep]` 30.12 cm at tick 171).
  The decision at 171 (`no_current_task`) rested on a fallback stand (count 52, [1, 53] on the decision clock) and
  chose item_7 with δ = 0; its first step, from 35.5 cm of the standing human, passes 30.12 cm from it (rule (b):
  moving within `min_separation`, the distance falling) entirely inside the robot's first tick, [0, 1), before the
  human projection begins at the observation offset (L2); its violating shifts are (0.06, 53), so δ = 0 is clear, where
  a stand known from step 0 gives (−0.94, 53). Not P4's recorded error, not P3, not a defect: the gap predates P (T3b,
  L2: the robot's first tick after a decision is unassessed against the human), made visible by a decision taken
  within reach of a standing human. TODO-134: whether L2's offset applies to a fallback stand, whose position at the
  decision tick is the observation itself.
- P4's separation cost, recorded (scenario_s05_02 prior on, completion 195 before P, 214 under P4). The human reaches
  its stay beside the robot's route at tick 24; before P, unprojected, the robot walked on and passed about 30 cm from
  the standing human (ticks 26 to 27); under P4 the first standing tick is evidence, the robot holds before the human
  and waits out the stay (42 ticks held against 23). The 19 ticks buy the separation: `[sep]` minimum 28.16 cm before
  P, 50.99 cm under P4.
P is closed with P4; P3 stays open; next is G.

**T-D G: admission (ruled by Hadi, 29 September 2026)** — RECORD [T-D/14], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
Staging. G-build follows in its own session. Verification on picked scenarios (scenario_s09_01's tail, scenario_s09_09,
scenario_s09_06, scenario_s05_01 prior on, one control scenario); the IR test-bed's oracle extended by derivation from
this entry for the warrant output; the four maintained sets as md5 regression plus one completion table.

BUILT (G-build, 29 September 2026): 81a9f86 (the build: `ObservationWarrant` and `BeliefState.observation_warrant`;
the recognizer's `_entered_by_completion` and `_observation_warrant`; the meta-planner's `WarrantSource`,
`GateOutcome.LEADER_UNWARRANTED`, `observed_assigned_tasks` and `_warrant`, `_clears_gate` still the one home; the `[IR]`
line's `warrant=[...]` and `[meta-proj] projection=built warrant=...`; TODO-123's docstring), 0555af7 (tests:
tests/test_g_build.py, 21; three expectations of tests/test_td15_build.py re-derived from AD1, CLEARS to
LEADER_UNWARRANTED, the fixture being prior off), cbe3f00 (the IR test-bed's oracle extended by derivation: the warrant
per hypothesis and the gate's outcome per tick), 5afa7f9 (the four maintained sets, a "G-build" section each).

**T-D G: admission (ruled by Hadi, 29 September 2026)** — RECORD [T-D/15], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
Verified. The suite 191 passed. The IR test-bed: 0 disagreements in all seventeen scenarios (scenario_s08_01 to _04,
scenario_s09_01 to _13), the warrant and the gate compared exactly; every expected.csv, actual.csv and actual_log.csv
equals the committed one once the two new columns are removed (the belief and the adequacy unchanged). The maintained
sets: the `.rec` streams byte-identical in all 48; prior on, every `[IR*]` line byte-identical to 2.5 once the `[IR]`
warrant field is removed, and every other line once `[meta-proj]`'s warrant field is removed, except where a
foreseeable admission moved. Prior on, commitment warrant covers every assigned task; the moves are all the lone
`coffee_break` after a boundary: no longer admitted at b + 1 on a standing tick (scenario_s02_01 at 363,
scenario_s05_01 and scenario_s05_02 at 142, both strategies) or admitted one tick later on its first step's gain
(scenario_s03_06, 123 for 122). No prior-on completion tick, `[sep]` minimum or F1 class moved. The control,
scenario_s01_01 prior on (two assigned deliveries), changed in the log fields alone. Picked cases:
scenario_s05_01 prior on, `coffee_break` after the boundary at 141 refused `none(leader_unwarranted)` from 142 (at the
`projection_expired` decisions of 144 and 150, against the fallback, no hold) and inadequate from 159; completion 194
as before. scenario_s09_09, 83 to 87: no admission (`none(leader_inadequate)`, 83 to 106). scenario_s09_06, the stand:
`deliver_item(item_1)`'s `pick_up` is warranted through its entry (the walk's completion at 28) for the whole stand,
refused as inadequate 47 to 71. Prior off (appendix, no ruling): the admissions of the robot's own items move;
completion scenario_s01_01 201 → 199, scenario_s06_03 realized 236 → 226 (tb1c, and tb3 full_reorder), single_task
316 → 314.

**T-D X: response (ruled by Hadi, 29 September 2026)** — RECORD [T-D/16], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
  Verification. One authored scenario, a declared persistent stand at the robot's target with at least one alternative
  task in the robot's pool, placed in the meta-planner test-bed (TODO-130), not a new maintained fixture. The expected
  property: the switch by cost. A derived verification condition, not a parameter: the occupied task's hold is at most
  the observed standing count (P4), so the authored stand must be long enough for that hold to exceed the relevant cost
  difference between the occupied task and the alternative, the return walk included when the robot carries the
  occupied task's item (`deliver_with_return`).

**T-D X: response (ruled by Hadi, 29 September 2026)** — RECORD [T-D/17], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
Next: track 3 (TODO-130); track 4 (TODO-140) may move first if the evaluation needs a genuine departure.

**The meta-planner test-bed (MPB) (ruled by Hadi, 29 September 2026)** — RECORD [T-D/18], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
Track 3 (TODO-130), after X. Ruled in cchat; records only (session MPB-records); nothing is built in this step. The
rulings are labelled MPB-1 to MPB-6 (not T3 or T3b, the Phase 4C realization tasks). The corrections and rulings Hadi
made on the records plan (29 September 2026) are written into the rulings below.

Purpose. To test the recognition-to-planning chain (the recognizer, the gate, the projection, the meta-planner) with a
working robot, one authored scenario per decision. The oracle (the instrument's own derivation of the expected
decision from the records) states the expected decision before the run; a disagreement is classified, never fitted. The
IR test-bed (track 1, TB) tested the recognizer with an idle robot; this instrument tests the decisions the
contribution claims. It is the last instrument before the evaluation and the demonstration.

- MPB-1, the oracle's expected decision.
  Ruling. A meta-planner decision has four parts with different epistemic status.
  (1) The trigger tick and its cause (a trigger: the condition on which the meta-planner re-decides). The causes
  compared are the four of `recognition_changed` — entered (no decision is recorded and the gate clears), replaced
  (the belief no longer points at the recorded hypothesis), boundary (the belief was re-initialised at an episode
  boundary, the observed human's completion of a terminal action; L1, L5 B), retraction (the recorded hypothesis's
  hypothesis adequacy, whether it explains its own derived phase, turned inadequate; L2 (ii)) — and
  `projection_expired` (the fallback projection the last decision rested on has reached its end; Q6). What they read
  of the human is derivable pre-run from the human's script, the layout and the records (the completions, the
  adequacy, the persistence rule); `no_current_task` depends on the robot's own progress and is read from the run as
  an observed fact.
  (2) The gate's outcome at the trigger (belief, hypothesis adequacy, warrant, the assigned tasks, θ), pre-run.
  (3) The projection the decision rests on (the admitted task's plan from the task model, or the fallback projection,
  the short-term physical projection from the observed persistence), pre-run.
  (4) The selection (the winner and its hold), which depends on the robot's realized state.
  The oracle derives per-tick tables pre-run: the boundary ticks, the ticks at which a hypothesis turns inadequate, the
  gate's outcome and leader, and the fallback a decision on that tick would rest on, with its end per the observed
  persistence. The (tick, cause) chain is assembled at the compare step from those tables and the run's observed
  `no_current_task` ticks, with D3's order on a shared tick (`no_current_task`, then `recognition_changed`, then
  `projection_expired`: a `no_current_task` tick masks the others); the decision record (the hypothesis the last
  decision was projected against, and the tick its fallback ends) follows from the chain, since a record is set at
  every decision, the robot's included. The assembly imports nothing from the planner. Part 4 is checked as
  properties the scenario declares, derivable from the layout by the author (for the occupied target: the alternative
  wins at the first expiry whose hold exceeds the layout's cost difference). The oracle states what the decision rule
  should conclude from the world's facts, never how the planner scores.
  The independence boundary. The oracle imports nothing from `shared/meta_planner.py` (the triggers, the gate, the
  cost strategy, selection), `shared/realization.py`, `shared/projection.py` (the projected durations,
  `Projector.project_fallback`), `shared/recognizer.py` or `shared/likelihood_functions.py`, nor
  `RobotAgent._perceive` (`mesa_sim/sim_agents.py`). It derives P4's perception facts (the run length and the standing
  count, the same direction within 1e-9) and the fallback's tail itself. It may use the planner's decomposition as the
  IR test-bed does (task and hypothesis definitions, not cost, realization or selection logic).
  Why. An oracle that reconstructs part 4 is a second planner, and a disagreement between two planners says nothing
  about which is wrong. The chain is assembled at the compare step because the record it reads is set at the robot's
  decisions too.
  Set aside. Full per-tick reconstruction; a single expected property per scenario without the per-tick parts.

- MPB-2, the scenarios.
  Ruling. Eight, each exposing one decision.
  (1) Admission after θ: two assigned deliveries, the first walk discriminates. The admission comes on the tick the
  gate clears, through `recognition_changed` with cause entered (D2): the expected tick is the crossing (the tick the
  leader's share first clears the gate).
  (2) The hold against an admitted projection (the hold: the ticks the robot stands still before its entry so that the
  realized plan keeps `min_separation`): the admitted human plan crosses the robot's route.
  (3) The planning side of the mid-action change (scenario_s09_13's chain): retraction, the fallback, re-admission at
  the next fitting phase.
  (4) Boundary re-admission: b refused, b + 1 admitted on commitment (commitment warrant: the hypothesis is one of the
  observed human's assigned tasks).
  (5) The lone foreseeable hypothesis after the work order: unwarranted on standing, warranted on the first step
  toward the machine, admitted through `recognition_changed` with cause entered on the first warranted tick.
  (6) The occupied target with an alternative task (X1): a declared stand at the robot's table, long enough by the
  derived condition (the hold, at most the observed standing count, must exceed the cost difference, the return walk
  included when carrying), a second delivery elsewhere; the switch by cost.
  (7) The fallback against a walker and against a stander: a straight run across the route, later a stand beside the
  route that ends before its projection; the expiry cadence. The stand is evidence for TODO-132 (a) (re-decision at
  the expiry only, holds outlasting the stay), recorded, not a verification of a rule.
  (8) The control: the human works away from every robot route; no hold at any decision, and completion identical to
  the same setup run without the human (a reference run, not a scenario).
  Recorded for scenarios 4 and 5: with the coffee machine in the room, `coffee_break` is live after every delivery
  boundary (L4), so at b + 1 the prior gives each live hypothesis 1/2 and θ is not cleared; b + 1 admission on
  commitment requires a single live hypothesis (after the coffee break's own boundary with one delivery left,
  `coffee_break` retired while `waited` holds) or the second-layout allowance below. Step 2's derivation shows which.
  Environments. One newly authored controlled layout, env_layout_12, as the default, authored for the physical facts
  the scenarios need (a crossing, an occupied table with a second free, a run and a stand on a route, clear routes),
  not for any expected number. Setups vary within it (env_setup_10, env_setup_11, ...): a setup holds the item
  placement and designations; the positions, the pools and the scripts are the scenario's. A second controlled layout
  only where the geometry itself must change, reported as such. Ids on the serial rule (T-L, ruling 4 as amended): a
  scenario's id repeats its setup's serial (scenario_s10_MM on env_setup_10, scenario_s11_MM on env_setup_11).
  Why. The existing layouts (1 to 9 for development, 10 and 11 for the recognizer) were not authored to isolate a
  planning decision, so a disagreement in them could not be attributed; a controlled room makes the property
  derivable beforehand; varying the setup rather than the room keeps the control scenario meaningful.
  Set aside. Reusing env_layout_11; one layout per scenario; authored parameter variants (the test-bed is not a sweep).
  AMENDED (Hadi, 29 September 2026, the post-(iv) records): THE LAYOUT-AND-SETUP RULE. The existing geometry is reused
  only when it naturally instantiates the case. One placement change is a setup fix. A second change, or any move of
  unrelated geometry to make a case come out, means a new setup or a new layout. The criterion is conceptual, not
  timing: a timing accident is a class-4 re-authoring of the same case (MPB-4). A placement or setup change is
  acceptable only if it alters no already-verified scenario on that setup; otherwise a new setup. The output floor
  couples every scenario on a setup: the setup's robot items inadmissible for the human sit at the floor and lower the
  leader's confidence, which moved scenario_s10_08's crossing from the IR test-bed's 46 to 47. A spatial or structural
  requirement (a relation between a robot route and a human station; the absence of a hypothesis) may need a new
  layout. First instance: scenario_s11_02's shelf_2 case (part (iv); analysis/mpb/authoring.md): item_12 on shelf_2
  put the exit walk within 2.3 cm of its shelf and admitted the delivery at 97, class 4 found before any run; moved to
  shelf_1, one placement change on env_setup_11, whose two scenarios were re-authored together.
  Why. A room or setup bent to make one case come out would make the other scenarios' properties depend on it, and a
  disagreement could no longer be attributed.
  THE COVERAGE PRINCIPLE EXTENDED (same date): every materially distinct in-scope decision path is one of three kinds of
  cell: verified (an instance in a verified run), unreachable (no instance, with a derivation from the records that the
  framework cannot reach it in scope), or out of coverage (no instance, with a recorded reason why it is not part of the
  mechanism the MPB claims). The matrix is analysis/mpb/coverage.md. A reachable cell the contribution claims gets one
  authored instance (part (v)).

- MPB-3, the robot's acts and the compare level.
  Ruling. The oracle's world holds the human's facts. The per-tick tables of parts 1 to 3 stay pre-run derivable
  because every scenario keeps the robot's items and shelves disjoint from the human's, so the robot's acts touch no
  fact a human hypothesis reads (L4's live set) and the human's trajectory does not depend on the robot
  (`docs/assumptions.md` 4.2). The disjointness rule is an authoring constraint of this test-bed, checked per scenario
  (its pools, its setup's item placement) before its runs, not a framework assumption; it gives the independence with
  the prior on only (MPB-6). The robot enters at the compare step only, from the run's own record: its logged
  positions, decisions and `no_current_task` ticks.
  Compare levels. Part 1: the set of (tick, cause) for entered, replaced, boundary, retraction and
  `projection_expired`, exact, with the `no_current_task` ticks listed. Part 2: the outcome name and the leader at
  every decision tick, exact. Part 3: the projection's identity (the admitted hypothesis key, or the fallback with its
  mode, k and end), exact. Part 4: the declared properties as booleans over the logged robot state.
  Part 4's inputs. The planner's logged decision values (the winner, its hold on `[meta-win]`, `[meta-cand] delta`) are
  observed inputs to a declared property, never inputs to the oracle's derivation of what should hold. The
  instrument's own computation is the F1 check (the separation classes) over the executed positions, and the layout's
  path lengths; never a hold.
  The in-process read of `BeliefState` and the meta-planner's outputs is the primary source, the log the check.
  Why (part 4's inputs). A hold the instrument computed would be MPB-1's second planner.
  Set aside. The oracle simulating the robot; everything read from the log after the run.

- MPB-4, verification and disagreements.
  Ruling. A scenario is verified when parts 1 to 3 show zero disagreements at exact equality on every tick, prior on,
  and every declared part-4 property holds (prior off: MPB-6). Outputs as in the IR test-bed: the expectation written
  before the run, the in-process and the log-derived actuals, the comparison with a classified diff.md, a figure, a
  summary, a REPORT with numbers and md5s.
  The oracle's own check: the single-rule alteration test of the IR test-bed (one rule of the derivation altered in a
  scratch copy; the comparison must detect it). The derivations new to the MPB oracle are the expiry cadence and the
  projection identity; on the gate with warrant, derived by the IR test-bed since G-build (its rule 23), only the
  alteration test is new. An undetected alteration is recorded as a property of the test set with its reason, as the
  IR test-bed did (E8's member clause), unless it is an oracle defect.
  Disagreement classes: (1) the oracle misread the records: fix the oracle; (2) the framework disagrees with the
  records: a defect, reported with the entry and the ticks, a ruling before any code, never a local fix; (3) the
  records do not determine the value: a design gap, a question to the design chat, never a choice made in the
  instrument or the code; (4) an authoring artefact: the scenario breaks the disjointness rule or the geometry does not
  give the declared property; it is re-authored or parked under the fixture rule; (5) a boundary case
  (`docs/assumptions.md` 2.2 to 2.6, 3.3): recorded, not designed for. A class-2 disagreement stops the build at that
  scenario.
  Why. Exact verification where the records determine the answer, property verification where they do not; classes
  3 to 5 keep the instrument from turning an accident into a rule; the alteration test shows that a zero result is a
  detection.
  AMENDED (Hadi, 29 September 2026, the post-(iv) records): THE THREE READINGS OF A CLASS-2 FINDING. When the framework
  disagrees with the records, the finding is read as one of three:
  (a) the implementation departs from the ruling: a defect under the ruling, reported with the entry and the ticks,
      and corrected to the ruling after Hadi's ruling (class 2 as above: never a local fix);
  (b) the ruling is followed, but its stated reason predicted otherwise: a redesign, returned to the design chat;
  (c) the ruling can be read two ways: class 3, a question to the design chat.
  THE LOOP: ruling, build, MPB evidence, interpretation, a possible redesign, build, re-test. The scenario is never
  modified to make a finding pass; it changes only under class 4, with its case unchanged.
  Why. A scenario changed until the framework passes it tests nothing; the instrument's worth is that a disagreement
  is attributed to the ruling, the build or the scenario before anything changes.
  CLASS-2 FINDING, READING (a) (Hadi, 30 September 2026; the first under MPB-4). THE INVARIANT: the trajectory realize()
  assesses is the trajectory the robot executes from the decision tick onward. THE EVIDENCE: scenario_s12_01,
  full_reorder, prior on, ticks 45 to 47, the cross-pairing of the decision at 26 (item_7, hold 4) on the re-executed
  realization: the planned robot against the projected human keeps F1 (54.64 cm minimum); the planned robot against the
  actual human, no violation; the executed robot against either, the three violations; the executed robot one step
  (20 cm) ahead of its plan on every tick, by the stationary accounting after the hold. A defect under the existing
  ruling, not a design question: F1, min_separation, the hold's meaning and the realization semantics unchanged; not
  acceptable quantisation. THE FAMILY, measured on the saved segments (the lag of the executed robot against its plan at
  its first move after each admitted decision, 32 prior-on runs): (a) after a walk's acknowledgement, +1 (one decision);
  (b) on a pick_up's acknowledgement tick, −1 (three); (c) on a task's completion tick, −1, or after a release, −2 (three).
  Corrected ("Realization as built", the dated correction; T-B Q7, superseded in part); re-verified (analysis/mpb/
  REPORT.md, "The class-2 correction"). THE P-SIDE RESIDUAL, recorded apart, out of scope of the correction: the human
  projection is 3.4 cm off the actual human on every tick of that carry (projection rounding: the projected walk ends
  1.7 cm short of the body's last step, and the projected carry starts 0.086 tick early), and one tick early at a decision
  falling on the human's own walk-acknowledgement tick (+1, five decisions: scenario_s10_01, _04, _05, _06 at 29, ...);
  −0.17 to −0.25 tick at walk starts generally. Not the cause of the violations. TODO-146.

- MPB-5, scope for the parked items.
  Ruling. TODO-132 (a): scenario 7's stand records the re-decision ticks, the holds and the tick the persistence broke,
  as evidence; nothing is built; the question returns to the design chat after the runs. TODO-134: no scenario is
  authored for it; a decision inside the observation-offset gap against a fallback stand, if one occurs in scenario 6
  or 7, is classified and recorded. TODO-137 and TODO-141: evaluation items, not built here.
  TODO-138, ruled for MPB runs. The comparison horizon is the first observed completion point (the human's script has
  ended and the robot's pool is empty) plus the idle margin the IR test-bed derives from E5 (30 ticks, covering E5's
  standing threshold at α = 0.01, 25 ticks). A derived plain-cost horizon (the robot's pool chained along its authored
  order from the robot's start, plus the human's replay length, plus the margin) is a safety cap for the run, not a
  behavioural timeout: a run that does not complete within it is classified (class 2 or 4), never given a longer cap.
  No change to the run loop or the body (TODO-33 stays as it is). The maintained sets keep their literal step counts.
  Why. Derived, no scenario constant.

- MPB-6, sets and strategies.
  Ruling. Prior on is primary. Prior off is run as a diagnostic appendix only, reported by completion, holds and
  near-encounters (ticks with the robot–human distance below `min_separation`), with no exact oracle comparison: with
  the prior off every hypothesis is admissible, including deliveries of the robot's own items, so the robot's acts
  change human-side hypothesis state and MPB-3's pre-run independence does not hold. Prior off has a different
  verification status from prior on. The same scripts in both.
  `single_task` is primary (its decisions, B2 and B3, are the ones scenarios 1 to 8 name; its `[meta-cand]` lines carry
  the per-candidate hold). `full_reorder` is a second run of the same scripts: identical per-tick tables of parts 1 to
  3 (the human side does not depend on the strategy; an invariant the comparison shows), not identical chains (the
  `no_current_task` ticks differ by strategy), and part-4 properties where defined for it; it is not required to
  reproduce every part-4 property (TODO-141).
  Why. The same scripts across strategies keep a difference attributable to the strategy, not to the human's
  trajectory.

Staging. Step 2: authoring and build in one plan-then-build session. The plan shows the layout's geometry, each
scenario's derivation of its declared property (on its setup) and the oracle's derivations (the expiry cadence, the
projection identity, the gate with warrant) before any run; the independence boundary is demonstrated in the build
report, not stated.

Unchanged: nothing in the framework (the trigger set, `_clears_gate`, `realize()`, P4's fallback projection,
retraction as L2 (ii) rules it, the recognizer, the run loop).

Reference: cchat, 29 September 2026 (MPB); `docs/handoffs/handoff_G_X_onward.md` §6; "T-D X" (X1, X5); "T-D G" (AD1
to AD4); "T-D P" (P4, Q6, P3, the observation-offset gap); "T-D L" (L1, L2 (ii), L4, L5 B); "T-D R and E" (E5, E6,
E8); "The IR test-bed" and its close-out; `analysis/ir_testbed/README.md` (rule 23, the run length) and `REPORT.md`
(the alteration test, the disagreement classes); "Layouts, setups and scenarios: the three artefacts of a run"
(ruling 4 as amended); D2; D3; F1; `docs/assumptions.md` 1.3, 1.4, 2.2 to 2.6, 3.3, 4.2, 4.6 and the case
classification; TODO-33, TODO-130, TODO-132, TODO-134, TODO-137, TODO-138, TODO-141

Next: step 2.

BUILT (MPB step 2, 29 September 2026; parts (i) to (iv)): e9f33ce (part (i), authoring), 787cee1 (part (ii), the
instrument and its tests), b5c7387 (part (iii), the runs, the classification, the records, then "built in part"),
8149f1d (part (iv), authoring: scenarios 6 and 7 re-authored, three scenarios added), and the part (iv) runs-and-records
commit.

The artefacts:
- env_layout_12: the 10/11 pattern translated by (0, -200), plus the robot's work areas.
- env_setup_10, env_setup_11.
- Eleven scenarios:
  - scenario_s10_01 to _05: MPB scenarios 1 to 5;
  - scenario_s10_06: the control (8);
  - scenario_s11_01, _02: 6 and 7, re-authored;
  - scenario_s10_07: the sudden stand mid-carry; scenario_s10_08: the change of mind; scenario_s10_09: the misdelivery.
- configs/mpb/, whose steps are MPB-5's safety cap.
- analysis/mpb/: authoring.md, README.md, REPORT.md, the md5s of every run.

The control's fact: a robot-only scenario is representable and loads and runs with no code change. The reference is
built in-process and not registered; completion 161 (single_task), 137 (full_reorder).

Verified, prior on, both strategies: all eleven, with zero disagreements on parts 1 to 3 at exact equality (every
tick's leader, boundary, adequacy finding, gate, hypothesis adequacy, observation warrant and perception facts; every
decision's trigger and cause, gate, leader, warrant and projection), against the in-process run and the log. Every
declared part-4 property holds under single_task. The expected per-tick tables are byte-identical across strategies.
- Scenario 1: entered at 25 and 76.
- Scenario 2: the hold 5 at the admission at 25; no F1 violation in its window.
- Scenario 3: retraction 55, expiry 66, entered 74.
- Scenario 4: replaced and refused at the coffee break's boundary 133; entered on commitment at 134.
- Scenario 5: `none(leader_unwarranted)` at the expiry of 127, on standing; entered at 132.
- Scenario 6: the switch by cost at the expiry of 14. item_8's hold, 7, exceeds the layout's cost difference, 3.5; the
  fallback stand ends at 1 + k, so the hold is at most k + 1.
- Scenario 7: the walk's and the stand's expiry cadence.
- The control: no hold; completion and every position equal to the reference.
- scenario_s10_07: retraction at 62, 17 standing ticks into the stand; the standing fallback's doubling at the expiry
  of 90 (k = 22 → 45); the resumed walk as a moving fallback at 110 and 115; re-admission only at the carry's advance to
  `place`, 120; replaced at the boundary, 123; item_2 entered at b + 15, 138 (coffee_break live after the boundary: 1/2
  each).
- scenario_s10_08: replaced at 33 (the return's place, a boundary; coffee_break leads on the prior's tie order, so the
  human's change from delivery 1 to delivery 2 passes through the coffee hypothesis in the recognizer's chain);
  entered at 47 (commitment and observation; the IR test-bed's 46 moved by this setup's output floor); no retraction.
- scenario_s10_09: retraction at 60; no re-admission of the misdelivered item; X5's ground (1) measured, the finding
  unexplained from 60 to 72 and outliving a refused re-decision from 61.

Classified:
- Part (iii): scenarios 6 and 7 as first authored (a human with no assigned tasks), class 1 (the oracle's support rule
  lacked io_contracts §2.1's empty-list clause; rule M0) and class 4 (MPB-3's precondition); re-authored in part (iv).
- Part (iv), before any run: item_12 on shelf_2, class 4 (scenario 7's exit walk within 2.3 cm of it, admitted at 97);
  moved to shelf_1.
- scenario_s10_03's P3 under full_reorder: not a disagreement; P3 is declared for single_task.

The alteration test detects every altered rule in some scenario except the skip rule (B2), class 3 (P4's dated line;
TODO-142). AD3 is not exercisable in the MPB set (the AD3 line in "T-D G"). TODO-134: no instance.

TODO-132 (a) evidence (scenario 7, single_task): the stand's holds double, 4, 8, 16, 32, and the last runs 30 ticks past
the stay.

The primary set's run logs at part (iv) (prior on, single_task; SUPERSEDED by the final list under CLOSED, below):
9a35a1b15f37d877e865c301494d604c scenario_s10_01, 261221bbaaf4639801652a2b8003b69e scenario_s10_02,
a9901a7af59ad78a65afc3179434a2e9 scenario_s10_03, 751eedb2c3ad3dbdeccf2b6abbdb3151 scenario_s10_04,
bacc21befccd638cfcd0f1101f805443 scenario_s10_05, 65a9facce7cdd1621a081aa1f7980890 scenario_s10_06,
86a511f42b9eb6756cdcd6fb6e8d65fe scenario_s10_07, 3edb658f33a62c60ecb8296c14b9c8c4 scenario_s10_08,
5728f8b4f018b256af74c47aa3de9744 scenario_s10_09, 60987425011281575480cc73a7c093ab scenario_s11_01,
580ae9fd3ae2455d251086223a6c5867 scenario_s11_02.

The suite: 211 passed. The 48 maintained logs and their .rec streams are byte-identical to G-build's.

COVERAGE PRINCIPLE (Hadi, 29 September 2026): each materially distinct mapping from a deviation kind to a decision chain
that the MPB claims to verify has one authored instance; a different location of the same chain is covered by type.
Provenance: scenario_s10_07 to _09 were added for a coverage gap found in review, not because a run failed.
RECORD LINE (part (iv)): the framework has no representation of an observed human with no work under the prior on, since
an empty assigned list is the diagnostic mode (shared/io_contracts.md §2.1). TODO-143, recorded only.

NOT CLOSED (Hadi, 29 September 2026, the post-(iv) records; SUPERSEDED by CLOSED, part (v), below): "BUILT" above is step 2, parts (i) to (iv). The coverage
matrix (analysis/mpb/coverage.md; the extended coverage principle under MPB-2) sorts every materially distinct decision
path of the eleven runs: 31 verified, 5 unreachable with a derivation, 4 out of coverage with a reason, 1 reachable and
not claimed (P3), 1 not a distinct path, and 5 reachable and claimed with no instance. Three facts of the whole set: the
cause boundary fired in no run; every admitted record ended before its T_h; no record was kept through a dip below θ.
X5's ground (2) is measured in scenario_s11_02 (single_task; every candidate holds at 25, 27, 31, 39 and 55).
The five claimed cells are authored in part (v), one instance each, in the order ruled: the switch against an admitted
projection (a new setup on env_layout_12); the hold against an admitted standing segment (a new scenario on
env_setup_10); the switch while carrying (a new scenario on env_setup_11); a record kept through a dip below θ (a new
scenario on env_setup_10); the cause boundary (a new layout without the coffee machine: the mechanism requires the
absence of the `coffee_break` hypothesis, which wins the tie order at every reset). Rulings kept apart: P3 is reachable
and not claimed; the wall cut is out of coverage until TODO-142 is ruled; "none" (no projection) is track 4's; AD3 stays
out of coverage, conceptually apart from the boundary cause (both without instance; the boundary is claimed and
reachable under a changed hypothesis space, AD3 is not exercisable here).
CLOSURE CRITERION: the MPB closes when every materially distinct in-scope decision path is verified, unreachable with a
recorded derivation, or outside the claimed mechanism with a recorded reason.

PART (v), BUILT (30 September 2026; analysis/mpb/authoring.md and REPORT.md, "Part (v)"; coverage.md): the five claimed
cells, one authored instance each, all verified (zero disagreements on parts 1 to 3 under both strategies, prior on;
every declared part-4 property under single_task).
- D8, the switch against an admitted projection: scenario_s12_01 on env_layout_14 and env_setup_12. At the admission
  (entered, 26) item_7's hold through the crossing is 4, above the authored cost difference of 2.5 ticks (the midpoint of
  (0, hold), fixed before any run), and the winner switches to item_13 with hold 0 before item_7 is grasped. The ruled
  "new setup on env_layout_12" was not expressible: from shelf_5 every other robot task of that room is at least 11.2
  ticks dearer, above a crossing's hold; Hadi ruled env_layout_14 (plus a shelf beside shelf_5 and a table), no two items
  on one shelf. The admission moved from 25 to 26 on env_setup_12 (the output floor, seven keys), found before the run,
  the cost relation unchanged.
- C2, the hold against an admitted standing segment: scenario_s12_02 on the same room and setup (shelf_10 and
  kitting_table_6, whose carry passes the human's waiting point at the coffee machine). At coffee_break's admission (76)
  item_14's hold is 18, against the admitted wait (104 to 134); the robot comes within min_separation of the waiting
  point only after the human has left it. env_layout_12 could not express it: every robot station lies at y >= -220, so
  only a walk from the start passes the waiting point, before any admission of coffee_break is possible. The fallback
  stand after the coffee break's boundary sends a hold of 30 as the human leaves (TODO-132 (a), recorded, not the
  property).
- D9, the switch while carrying: scenario_s11_03 on env_setup_11, the stand from tick 0 and the robot grasping item_8 at
  4, before the decisive expiry (Hadi: the experimental variable is the carrying state at the decision, the return walk
  in the cost difference, not when the stand began). At the expiry of 30 (k = 31) item_8's hold, 32, exceeds the return
  difference, 16.4 (X1's condition with deliver_with_return); the robot switches while carrying, under both strategies,
  and returns item_8 to shelf_3 before item_9's grasp.
- E6, a record kept through a dip below theta: scenario_s10_10 on env_setup_10, scenario_s09_04's script (the planned
  drop-cut detour cannot be expanded by the oracle's trajectory, which reads a cut from a Start only). Admitted at 25; the
  record kept with no trigger through a proximity regress at 31 and the dip at 34 to 36 (item_1 leading below theta,
  adequate); replaced at 37.
- A4, the cause boundary: scenario_s10_11 on env_layout_13 (env_layout_12 without the coffee machine: the mechanism
  requires the absence of the coffee_break hypothesis, which wins the tie order at every reset) with env_setup_10. item_1
  misdelivered to kitting_table_3, adequate to the place (margin 55.5 cm at alpha = 0.05; the case would not form at
  0.1); at the place (53) the reset leaves item_1 the leader: recognition_changed with cause boundary, its first instance.
Classified, no class 2: scenario_s12_01 under full_reorder keeps item_7 (the ordering's cost includes its tail's return
walks; MPB-6); three F1 robot violations inside that admission's window under full_reorder (hold 4 from 26), the pattern
of scenario_s10_02 prior off; checked on the re-executed realization (REPORT.md, part (v)): the plan keeps 54.64 cm, the
executed robot runs one step (one priced stationary tick) ahead of it and the projected human is 3.4 cm off the actual
one, the robot's lead producing the violations; reading (c) by the check's rule, no class assigned;
Hadi then read it as class 2, reading (a), and it was corrected (MPB-4's class-2 record); a near-encounter in scenario_s12_02 at 139 as the human
walks toward the robot on moving fallbacks of k = 1 and 3 (P4's recorded error; X3; TODO-135). The alteration test on
the sixteen: every rule detected except the skip rule (B2), as before. The eleven verified scenarios rerun byte-identical
(68 of 68 logs and streams); the suite 211 passed; the four maintained sets 96 of 96 byte-identical.
CLOSED (the close-out, Hadi, 30 September 2026; no longer provisional: objection 1 was read as class 2, reading (a),
and corrected the same day, MPB-4's class-2 record). THE CLOSURE CRITERION: every materially distinct in-scope decision
path is verified, unreachable with a recorded derivation, or outside the claimed mechanism with a recorded reason. Met:
36 verified, 5 unreachable with a derivation, 4 out of coverage with a reason, P3 reachable and not claimed, one not a
distinct path (analysis/mpb/coverage.md). The NOT CLOSED paragraph above is superseded.
WHAT THE MPB ESTABLISHES. The MPB establishes structural branch reachability and execution of the recognition-to-planning
chain, not consequential activation of those branches under human-robot interaction conflict. The progression: track 1,
recognition (the IR test-bed); track 2, semantics (T-D R, E, L, P, G, X); track 3, reachability (this test-bed); track
3b, consequence under conflict (TODO-145); T-F, benefit (TODO-144).
FINAL NUMBERS (after the class-2 correction; analysis/mpb/REPORT.md): sixteen scenarios (scenario_s10_01 to _11,
scenario_s11_01 to _03, scenario_s12_01, _02) on env_layout_12, _13 and _14 with env_setup_10, _11 and _12; zero
disagreements on parts 1 to 3 in all 32 prior-on runs (both strategies), against the in-process run and the log; every
declared part-4 property holds under single_task; the alteration test detects every rule except the skip rule (B2,
TODO-142); the suite 220 passed; the four maintained sets regenerated at the correction (their "class-2 correction"
sections). The primary set's run logs (prior on, single_task; every run's md5 in analysis/mpb/REPORT.md):
ad1a4020ff0da1eb5d4dbfcafe60361e scenario_s10_01, ed061081de759217002890ab9ba36c5e scenario_s10_02,
0ac37ed728ba00ccfa741a444da20206 scenario_s10_03, a46a710d3cf5115481c6563179432a7c scenario_s10_04,
9f2cf65204ed963e1fcd030cff3d95a5 scenario_s10_05, f15ebb8578b481f7365cc78fc819394d scenario_s10_06,
f58c4f4a9f50a495b5e5081869f4a83c scenario_s10_07, b10ca58e31510b196d1ca86344049c6d scenario_s10_08,
eaa8e01774b9e925254c2fcbb96027b6 scenario_s10_09, f3299d52a633692e539ad0f0c9310f53 scenario_s10_10,
f7f275edfcc056ca12dd9ce67554675b scenario_s10_11, 9b673e2bf65bd1d41cb1fa7e92215173 scenario_s11_01,
580ae9fd3ae2455d251086223a6c5867 scenario_s11_02, 31d5f0f5e16cdd71e301cf77182aa311 scenario_s11_03,
e1e9a758799a488b3bf022fe8c8b92ae scenario_s12_01, 93053e69c0d69ae637fb82b0c9399eb2 scenario_s12_02.
Next, as Hadi rules: track 3b (TODO-145) before the evaluation (T-F, TODO-144), or track 4 (TODO-140).
RULED (Hadi, 30 September 2026; `docs/roadmap.md`, "The plan from T-A", its order block): neither; T-G is next, then
T-F and T-V, and track 3b and track 4 in the T-D tail after them.
AUDIT TRAIL (Hadi, 2 October 2026; recorded in T-G records 15): the alteration test was broken at HEAD since the IR
oracle began to read the layout's areas (T-G A9): its scratch copy looked for the layout under the scratch directory. It
was corrected in the shared instrument code (analysis/instruments/mpb/alteration.py, c6469db). The table of
analysis/kitting/mpb/REPORT.md reproduces exactly. An instrument correction, no change of behaviour.

---
