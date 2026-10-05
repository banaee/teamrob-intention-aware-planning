# T-K part 1: the plan of the build of the two gate rulings (AM67, AM68)

Deleted 5 October 2026 (T-F part 1's close, part E; analysis/README.md): the frozen analyses td_stage1, td_stage1b, l_build, irb2b_exposed_interval (tb2b_exposed_interval before 3 October), ablation_task_committed, f47_fixtures, t1_conflict_measurement, todo90_b2a_window, tc2c_scripts, tb1d_designations, tb2c_per_entry_holds and big_picture under analysis/kitting/ (analysis/ before the sort); the runs and run files of T-K part 1's steps 5 and 5b (planning) and 5e and of T-F part 1's stage 2 check (configs/kitting/mpb/tk, mpb/tk5b, tk5e, tf1/check; their READMEs and reports stay). A path cited below under these names is held by commit 362af19 (`git checkout 362af19 -- <path>`).

Written by ccode, 4 October 2026 (BUILD DISCIPLINE, step 1: plan only, no code). Status: APPROVED (Hadi, 4 October
2026), with the rulings on D1 to D7 (section 7, each marked RULED; design_records.md, "T-K", THE GATE'S BUILD PLAN,
RULED). Every build session reads this file first. BUILT (4 October 2026; design_records.md, "T-K", THE GATE
RULINGS, BUILT; the state file docs/handoffs/build_T-K_gate_state.md).

What is built: AM67 (observation warrant is required at admission, for every hypothesis; commitment warrant alone no
longer admits) and AM68 (the gate refuses an outranked leader, as a condition of admission only), with AM73 (the term
and `none(leader_outranked)`), AM75 (the tie an exact comparison) and AM76 (the recognizer reports one category per
live hypothesis, read by the gate for the leader only). The rulings and their reasons: design_decisions.md, "T-K",
under R7 (AM67 to AM69, AM71 to AM76); design_records.md, "T-K", THE GATE AFTER STEP 5B, RULED.

What does not change, and is not touched at the conceptual level: the end of an admission (T-D L, D2; AM69), the
trigger rule, the projection and the fallback projection, the strengths and the prior, the meta-planner's candidate
evaluation and cost, the recognizer's belief, adequacy and observation warrant. dock_loading's IRB and MPB sets stay
stale for dock_loading's step (AM57).

Every number below marked "predicted" is read from existing outputs (filters on recorded answers, as WHATIF.md), not
from a run. It names what the build's checks expect; a run decides.

---

## 1. Facts from the code and the outputs (the plan rests on these)

- F1. `BeliefState` (`shared/types.py`) carries the belief over H (`belief`), the prior (`prior`, empty with context
  knowledge off), and per live hypothesis `hypothesis_adequacy` and `observation_warrant`. It carries no evidence. The
  recognizer holds the normalised evidence over exactly H in `Recognizer._evidence`, after the tick's update and, on a
  boundary tick, after `_begin_episode` has reset it equal (`shared/recognizer.py`, `update`, around the
  `self._evidence = {k: v / total ...}` line and the boundary block). `_belief()` multiplies it by the prior's weights;
  with context knowledge off it returns `dict(self._evidence)`, bit for bit.
- F2. The gate (`MetaPlanner._clears_gate`) asks, in order: θ (`none(below_theta)`), the leader's adequacy
  (`none(leader_inadequate)`, then `none(leader_no_observation)`), warrant (`none(leader_unwarranted)`). Warrant is
  `_warrant(belief)`: COMMITMENT (the leader matched by `same_task` to `self._observed_assigned_tasks`) or OBSERVATION
  (`belief.observation_warrant[leader]`). `_warrant` is read by the gate and by admission's log line
  (`[meta-proj] projection=built warrant=<sources>`) only. `_clears_gate` is asked at admission
  (`update_human_projection`) and on the entering side of `recognition_changed` (`evaluate_triggers`); never for
  retention.
- F3. The assigned tasks reach the meta-planner as the constructor argument `observed_assigned_tasks`
  (`mesa_sim/sim_agents.py`, `RobotAgent.__init__`); its only reader is `_warrant`. The recognizer receives the same
  list as its support restriction, which AM67 does not touch. `same_task` stays in use elsewhere in the meta-planner
  (`_replan_orderings`, the continued head).
- F4. The `[IR]` line (`mesa_sim/sim_agents.py`) ends with `warrant=[...]`, every live hypothesis in order. The IRB
  instrument parses that field with a regex anchored at the line's end (`analysis/instruments/irb/actual.py`,
  `WARRANT`) and strips it before `tdlib` reads the line.
- F5. `BeliefState(` is constructed in `shared/recognizer.py`, `mesa_sim/sim_agents.py` (`_make_dummy_belief`) and four
  test files (`tests/kitting/test_g_build.py`, `test_l_build.py`, `test_p_build.py`, `test_tk_gate.py`). Commitment
  warrant is tested in `tests/kitting/test_g_build.py` (the gate's order, task equality, prior off, the log text) and
  `tests/kitting/test_td15_build.py` (refusals as unwarranted, prior off); `tests/instruments/test_mpb_instrument.py`
  builds decisions with `("commitment",)`.
- F6. Ties in the evidence. Over the 15,175 ticks with two or more live hypotheses in the IRB's context-off outputs
  (scenario_s08, s09 and round 1), the top two values of the evidence are exactly equal on 321 ticks (boundary ticks,
  reset by `_equal_evidence`; symmetric stands such as scenario_s11_03's 0.5 / 0.5) and differ by less than 1e-9 but not
  by zero on one: scenario_s09_07, tick 35, by 1.7e-16.
- F7. AM68 with context knowledge off: the prior is equal, the belief's leader is the evidence's leader (a tie keeps
  it), so no leader is ever outranked. Every context-off gate answer is unchanged by AM68 (by construction; stage 2
  checks it).
- F8. Commitment-only admissions today (`warrant=commitment`), context knowledge off: 17 of the 48 maintained logs, one
  each, all with assignment knowledge on (tb1a 3, tb1b 2, tb1c 4, tb3 8): the lone last delivery at b + 1. In the MPB
  set: scenario_s10_04 and scenario_s12_02 at 134 (predicted under AM67: 140, when the human starts), scenario_s10_11
  at 136 (and 139 under full_reorder; predicted: no clearing tick with observation warrant while that delivery leads).
  In the IRB outputs the per-tick gate clears without observation warrant on 7 ticks in 5 of the 17 runs of
  scenario_s08 and s09, and on 41 ticks in 6 of round 1's 31 runs; with context knowledge on, 109 ticks in 44 of step
  4's 57 runs, 8 in 1 of its 2 off runs, 49 in all 17 of step 5b's recognition runs.

## 2. The structure

### 2.1 The recognizer's new output (AM76)

- A new enum in `shared/types.py`, beside `HypothesisAdequacy` and `ObservationWarrant`: `EvidenceRank`, two values,
  `OUTRANKED = "outranked"` (the evidence alone ranks another live hypothesis strictly above it) and
  `NOT_OUTRANKED = "not_outranked"` (no live hypothesis's evidence is strictly above it; a tie included). Its docstring
  states AM68, AM73, AM75 and that the meta-planner reads the leader's value only.
- A new field `BeliefState.evidence_rank: Dict[str, EvidenceRank]`, keys exactly H, empty exactly when EXHAUSTED.
  Required (no default), as `observation_warrant` is, so every constructor states it (F5); `_make_dummy_belief` states
  `{}`.
- Computed in `Recognizer.update` by a new method `_evidence_rank()`, from `self._evidence` after the tick's update and
  the boundary (the evidence the belief of the same tick multiplies): a key is OUTRANKED when some other key's value is
  strictly greater, by Python's float `>` and nothing else (AM75). It reads neither the prior nor the belief, the
  adequacy nor the warrant, and nothing reads it inside the recognizer. On a boundary tick every value is equal, so no
  hypothesis is outranked.
- The `[IR]` line gains a last field, `rank=[<key>=outranked|not_outranked ...]`, every live hypothesis in hypothesis
  order, as `warrant=[...]`; empty when exhausted. (ccode's choice of form; it follows AD4's placement of warrant. The
  alternative, a separate `[IR-rank]` line, would leave `[IR]` byte-identical; either costs the instruments one parser
  change.)
  AMENDED (ccode, the build's stage 1, 4 October 2026): the separate line is built, `[IR-rank] step=N
  rank=[<key>=outranked|not_outranked ...]`, printed after `[IR]`. Reason, found at stage 0: the IRB instrument's
  parsers (`irb/actual.py`'s warrant regex, anchored at the line's end, and `tdlib`'s greedy `tails=[...]`) would
  misread an `[IR]` line with a new last field before stage 4 updates them; with a line of its own, `[IR]` and every
  instrument output stay byte-identical through stages 1 to 3, a stronger check. Wherever this plan says "the `rank`
  field" it reads "the `[IR-rank]` line".
- Docs updated in the same commit: `shared/io_contracts.md` (BeliefState, its invariants, the gate's reading),
  `docs/recognizer_handback.md` (the outputs, §1.10's neighbourhood, the gate's paragraph).

### 2.2 The gate (AM67, AM68)

- `_clears_gate` asks, in order: θ; the leader's adequacy (inadequate, then no observation); the leader's observation
  warrant (`belief.observation_warrant[leader] is OBSERVATION`, else `none(leader_unwarranted)`); the leader's evidence
  rank (`belief.evidence_rank[leader] is OUTRANKED` gives `none(leader_outranked)`); else it clears. A new
  `GateOutcome.LEADER_OUTRANKED = "none(leader_outranked)"`. The place of the new check is decision D1 (section 7).
- `none(leader_unwarranted)` keeps its name: under AM67 a leader without observation warrant has no warrant.
- Both callers are unchanged: admission and the entering side of `recognition_changed` read the same predicate, as
  they read warrant; retention by identity is untouched (AM69).

### 2.3 What commitment warrant leaves without a function (ccode's proposal, decision D2)

Proposed: remove it from the meta-planner. `WarrantSource.COMMITMENT`, the `same_task` match in `_warrant`, the
constructor argument `observed_assigned_tasks` and `self._observed_assigned_tasks`, and the argument in
`RobotAgent.__init__`'s `MetaPlanner(...)` call. The recognizer's support restriction (the same list) is untouched.
`_warrant` and `WarrantSource` go with it: the gate reads `belief.observation_warrant[leader]` directly.
Reason: after AM67 the input decides nothing; an input that decides nothing invites a later reader to give it a role
the rulings removed, and keeping a matching that no decision reads is code built around the design. The assignment
then reaches the robot's mind through the support restriction (and the prior) only.
The log: `[meta-proj] projection=built warrant=observation` stays, as AD4 rules the admission's warrant source is
named; it now has one value. (D2 asks whether that field stays.)

### 2.4 Every log line that changes

| line | change | where |
|---|---|---|
| `[IR]` | new last field `rank=[...]` | every log, both settings |
| `[meta-proj] ... projection=built warrant=...` | `commitment` and `commitment,observation` no longer occur; `observation` only (under D2 (a)) | logs with such admissions |
| `[meta-proj] ... fallback refused=...` and the bare refusal | new value `none(leader_outranked)`; ticks that cleared on commitment alone now `none(leader_unwarranted)` | context on (outranked); assignment knowledge on (unwarranted) |
| `[meta-trig] ... cause=entered` and every decision line after it | moved where an admission on commitment alone moves (AM67) or an outranked leader is refused (AM68) | the runs of F8; context-on runs |
| `[run]` | none | |

## 3. The instruments (the oracles compute both conditions on their own)

- The IRB oracle (`analysis/instruments/irb/oracle.py`). It already computes the evidence per hypothesis on its own
  (the `evidence` column, from its rules, never read from the recognizer). New: a per-hypothesis column `rank`,
  OUTRANKED when another live hypothesis's oracle evidence is strictly greater; the gate (`Oracle.gate`) loses the
  commitment branch (`self.committed`), requires observation warrant, and adds `none(leader_outranked)` in the place D1
  rules. The README gains rules for both (numbered after rule 33), with their sources (AM67, AM68, AM73, AM75, AM76).
- The IRB's readers: `actual.py` takes `rank` from `BeliefState.evidence_rank` and from the `[IR]` line (its regex and
  the stripping before `tdlib`); `compare.py` compares `rank` as a categorical column against both files, and `gate`
  as now. How `rank` is compared where the oracle's own two evidence values lie within its 1e-9 agreement level (F6) is
  decision D3.
- The MPB oracle (`analysis/instruments/mpb/mpb_oracle.py`) imports the IRB oracle's gate unchanged; it loses
  `committed` and computes the admission's warrant tuple as `("observation",)`. `mpblib.Gate` gains
  `LEADER_OUTRANKED`. `actual.py` and `compare.py` follow (`built warrant=...` per D2). The MPB oracle's independence
  boundary (it imports nothing of `shared/meta_planner.py` or `shared/recognizer.py`) is kept.
- The alteration test (`analysis/instruments/mpb/alteration.py`): C1 ("commitment warrant ignored") becomes the rule
  and is retired; its anchor no longer exists. Proposed new shared alterations: C4, the outranked condition not asked;
  C5, a tie refused (`>=` for `>`); C6, the rank read from the belief instead of the evidence. Where they run is
  decision D6.
- `analysis/kitting/mpb/properties.py`: P3c's wording ("an assigned task (commitment warrant)") is corrected to "an
  assigned task"; its test (the leader's identity and the assignment) is unchanged. The step-5 properties moved by the
  rulings: section 4 and decision D5.
- Tests: `tests/instruments/test_mpb_instrument.py` (the `("commitment",)` decisions and the log text) follows D2.

## 4. What the rulings remove or move in the test sets

The MPB's coverage matrix (analysis/kitting/mpb/coverage.md; context knowledge off, assignment knowledge on):
- B5, "clears by commitment only" (scenario_s10_04 at 134): unreachable by ruling (AM67). Its scenario stays; from 134
  its decisions move (predicted: admission at 140).
- B7, "clears by both": commitment decides nothing, so it is no longer a distinct path from B6 ("clears by
  observation"); marked "not a distinct path", its instance kept.
- A new row of the gate dimension, "θ, adequacy and warrant passed, outranked": unreachable with context knowledge off,
  by construction (F7). With context knowledge on it is reachable; whether it is claimed, and where its instance comes
  from, is open question 3 of the discussion (decision D4).
- E7 (AD3, the loss of observation warrant): stays out of coverage; its derivation's delivery case reads "a lone
  delivery admitted on its first step" (AD3's AMENDED line).
- Every other verified row's instance lies before 134 or in a scenario without a commitment-only admission (A4 is
  scenario_s10_11 at 53; C2 scenario_s12_02 at 75; D8 scenario_s12_01 at 25; D9 scenario_s11_03 at 30; E6 scenario_s10_10
  34 to 36): predicted unchanged.
- Declared properties of the MPB set (context knowledge off): none predicted to move (scenario_s12_02's P12.2a to c
  concern the coffee break before 134; scenario_s10_04 and s10_11 declare none). P3c as section 3.

Step 5's planning cases (analysis/kitting/mpb/tk/; context knowledge on). Predicted from the recorded tables, the
evidence alone read from the off runs of the same scripts (the human is open-loop; s16_01 and _02, _03 and _04, _05
and _06 share a script):

| scenario (case) | recorded admission | under AM67 and AM68 (predicted) | declared properties that move |
|---|---|---|---|
| s16_01 (3, the early admission correct) | item_4 at 0 (observation warrant; not outranked, 0.3345 the top) | unchanged at 0 | none |
| s16_02 (2) | item_4 at 38 | unchanged | none |
| s16_03 (4, against the context, coffee break) | item_4 at 0 | refused at 0, outranked (coffee_break 0.3362 above 0.3333); item_4's first admission 74 | PK4a, PK4b (the admission and its retraction at 43 do not occur); PK4c (its window rests on them); PK4e (73 becomes 74) |
| s16_04 (1) | coffee_break at 22; item_4 at 73 (commitment only) | 22 unchanged; item_4 at 74 | PK1b (as PK4e) |
| s16_05 (5, against the context, the A/C; the pass at 28.3 cm) | item_4 at 0; again at 47 (commitment only) | refused at 0, outranked (ac_activation 0.3354 above 0.3349); item_4 first admitted at 48 | PK5a (no admission at 0); PK5b (the violation rested on that admission) |
| s16_06 (the A/C raised) | item_4 at 47 (commitment only) | 48 | none (PK5rw: "no admitted projection before 47" still holds) |

Step 5b's sets (context knowledge on): 15 of its 16 MPB runs hold a commitment-only admission (18 admissions); 12 are
predicted 1 tick later, and the other 6, scenario_s10_09 (160, 163), s10_11 (136), s11_01, s11_02 and s11_03 (0,
item_12, the standing human), have no clearing tick with observation warrant while that delivery leads (predicted: not
admitted). Of its 80 admissions, AM68 refuses 2 (the evidence alone from the MPB set's off run of the same script):
scenario_s10_04 at 67 (item_2, 0.4285 against 0.5715) and scenario_s10_09 at 163 (also commitment-only). Step 5b
declared nothing; its 12 reached cases are re-read after the runs.

## 5. Regression scope, what stays identical, what changes

The scope (as AM48 and the T-K build): the four maintained sets (`sweep.sh` of tb1a, tb1b, tb1c, tb3: 48 logs and
their `.rec`; context knowledge off, both assignment settings), the IRB's scenario_s08 and s09 (17) and round 1 (31)
through `analysis/instruments/irb/run.sh kitting`, the MPB set (16 scenarios, both strategies, assignment knowledge on;
the off appendix as a diagnostic) through `analysis/instruments/mpb/run.sh`, dock_loading's six milestone runs
(scenario_s03_02, s05_02, s07_02 at 800 steps; s03_03, s05_03, s07_03 at 1000), and `pytest`.

Predicted, context knowledge off:
- The recognizer's outputs (belief, adequacy, warrant, the reported distribution) and every `.rec` stream:
  byte-identical throughout.
- After stages 1 and 2: every log identical except the `[IR]` line's `rank` field (a diff after stripping it is
  empty).
- After stage 3 (AM67): the 31 maintained logs without a commitment-only admission identical except the `rank` field;
  the 17 with one identical up to the tick before that admission, then changed (each listed: condition, first differing
  step, grep). In the IRB sets only the per-tick `gate` column changes, on the 7 + 41 ticks of F8, plus the new `rank`
  column. In the MPB set scenario_s10_04, s10_11 and s12_02 change from 134 / 136; the others identical except the
  `rank` field. dock_loading's milestones: listed one line each (first differing step), not analysed; dock_loading's
  sets stay stale.
- Assignment knowledge off (the 24 prior-off maintained logs, the MPB's appendix): no commitment warrant existed, so
  identical except the `rank` field.
- AMENDED (ccode, stage 3, 4 October 2026): stage 3 also changes, in every log with such an admission, the text of the
  `[meta-proj] projection=built warrant=commitment,observation` line to `warrant=observation` (a named line of section
  2.4, left out of this list); the logs are compared with that text normalised.

Context knowledge on: no maintained set runs with it. Its sets (steps 4, 5, 5b) are the measurement of section 8.

## 6. Stages, checks, stop conditions

A pause at each stage boundary (Hadi, 4 October 2026, the rule for this prompt). Each stage is its own commit, made
only after its check passes. Outputs of the checks stay local; md5s go into the READMEs.

| stage | content | compared with | expected difference |
|---|---|---|---|
| 0 | baselines B0 at HEAD; one copy of the untracked test-bed data outside the repository (as AM59) | (records B0) | none |
| 1 | AM76: `EvidenceRank`, `BeliefState.evidence_rank`, `_evidence_rank()`, the `[IR]` field, io_contracts and the handback | B0 | the `rank` field only |
| 2 | AM68: `GateOutcome.LEADER_OUTRANKED`, the check in `_clears_gate` | stage 1 | none, context knowledge off (F7) |
| 3 | AM67: commitment warrant out of the gate; D2's removals | stage 2 | section 5, the AM67 lines, each listed |
| 4 | the instruments (section 3); the context-off test-bed sets rerun against the oracles | stage 3's runs | the oracles agree; section 4's moves only |
| 5 | records: the maintained sets' README sections (md5s, every moved line and why), the test-bed READMEs (what changed, the last commit holding the old results), coverage.md's rows, the BUILT lines | | |

Unit tests, by stage:
- 1: keys exactly H and empty when exhausted; nothing outranked on a boundary tick; a one-ulp difference outranks
  (AM75); a tie does not; with context knowledge off the leader is NOT_OUTRANKED on every tick of one recorded run;
  every `BeliefState(` constructor states the field.
- 2: the order of refusals; an outranked leader refused `none(leader_outranked)` at θ, adequate and warranted; a tied
  leader clears; the log text of the refusal.
- 3: an assigned leader without observation warrant is refused `none(leader_unwarranted)` (AM67), with assignment
  knowledge on and off alike; the commitment tests of `test_g_build.py` and `test_td15_build.py` rewritten to the rule,
  each named in the commit; `[meta-proj] built warrant=observation`.

Stop conditions (as the T-K build's, AM57, AM61, AM64). The build stops, and the cause is examined and reported, with
no ruling and no scenario changed for it, on:
1. a disagreement with an oracle on any test-bed run;
2. a declared property that no longer holds, other than those section 4 lists as moved by ruling;
3. a scenario that no longer reaches its authored coverage case, other than B5 (unreachable by ruling);
4. a context-off difference outside section 5's predictions: in stages 1 and 2 anything but the `rank` field; in stage
   3 a change in a log with no commitment-only admission, or before that admission's tick.
The run without assignment knowledge is a diagnostic: its differences are listed and never stop the build. A stop
leaves the committed state at the last stage that passed.

## 7. Decisions that need Hadi

D1. Where the outranked check stands among the gate's refusals. The order decides only which reason a refused tick
prints; the gate's answer (clears or not) is the same.
- (a) Last, after `none(leader_unwarranted)`. Every tick refused today keeps its printed reason, and
  `none(leader_outranked)` appears only where AM68 alone refuses, so a log diff shows exactly AM68's effect.
- (b) Before warrant, after adequacy (the evidence before the warrant).
Recommendation: (a). It follows how G1 and warrant were added, each after the existing checks.
RULED (a): last, after `none(leader_unwarranted)`. Reason: every tick refused today keeps its printed reason, so a log
difference shows this ruling's effect alone.

D2. What happens to commitment warrant's parts (section 2.3).
- (a) Remove the input and the matching from the meta-planner; keep `[meta-proj] projection=built warrant=observation`
  (AD4 unchanged; the field now has one value).
- (b) As (a), and drop the `warrant=` field from the admission line (AD4 amended: the field can no longer tell anything
  apart).
- (c) Keep the matching for the log only, printing whether the admitted leader is assigned.
Recommendation: (a). It removes what decides nothing, keeps AD4 as ruled, and leaves the instruments' parser of that
line unchanged; (c) prints a field that suggests a role the rulings removed.
RULED (a): the parts removed from the meta-planner; the admission line keeps its warrant field. Reason: an input that
decides nothing invites a later role the rulings removed.

D3. How the oracle checks an exact rule it can reproduce only to 1e-9. The recognizer compares its floats exactly
(AM75). The oracle computes its own evidence, which agrees with the recognizer's to 1e-9, not bit for bit; where two
hypotheses' evidence differ by less than that (F6: one tick in 15,175, scenario_s09_07 at 35), the two can rank them
differently.
- (a) The oracle marks `rank` undetermined on such a tick, the comparison skips it and counts the skipped ticks; the
  rule stays exact, the tolerance is the instrument's agreement level, as for its numeric columns.
- (b) The oracle compares exactly and every disagreement is examined by hand.
Recommendation: (a).
RULED (a): undetermined within the oracle's agreement level, skipped and counted. Reason: the rule stays exact; the
tolerance is the instrument's.
AMENDED (Hadi, 5 October 2026, step 5d): exactly equal evidence in the oracle is a tie, not outranked; "undetermined"
stays for values close but not equal. Reason: the oracle stays independent of the run and now checks that a tie passes
(design_records.md, "T-K", D3's AMENDED line).

D4. The coverage matrix (open question 3 of the discussion). With context knowledge off the outranked refusal is
unreachable by construction, so the off matrix cannot cover it.
- (a) The matrix stays the off setting's, with one added row for the outranked refusal, claimed with context knowledge
  on, its instance taken from step 5's existing scenarios (predicted: scenario_s16_03 and s16_05 at tick 0, a
  `no_current_task` decision that refuses `none(leader_outranked)`), no new scenario.
- (b) A full context-on column for every row.
- (c) New scenarios authored for it.
Recommendation: (a).
RULED (a): the off setting's matrix, one added row for the outranked refusal, claimed with context knowledge on from
step 5's existing scenarios; no new scenario. It closes the open question on the coverage matrix.

D5. Step 5's declared properties that the rulings move (section 4: PK4a, PK4b, PK4c, PK4e, PK1b, PK5a, PK5b). Cases 4
and 5 lose their premise: the early admission against the context no longer happens at 0.
- (a) Before the measurement runs, re-declare what the rulings determine (the admission ticks and the gate's answers,
  as section 4 predicts), keep the old properties in the record marked superseded, and leave the separation in those
  windows a measure, not a property.
- (b) Keep the old properties and report them as failed by ruling.
Recommendation: (a). The separation is what the measurement is for; declaring it in advance would state the hoped
result as an expectation.
RULED (a): re-declared before the measurement runs; the old ones kept, marked superseded; the separation a measure,
not a property.

D6. The alteration test. C1 is retired by AM67.
- (a) Add C4 to C6 (section 3) and run the C group on step 5's six scenarios (context on, where the outranked condition
  acts) and on the MPB's sixteen (context off, where C4 to C6 are undetectable by construction, recorded as a property
  of that set).
- (b) Retire C1 and add nothing now.
Recommendation: (a); the gate's rule changed, and the test exists to show the comparison would catch a wrong gate.
RULED (a), narrowed: C4 to C6 run on step 5's six scenarios only. On the planning set's sixteen, with context
knowledge off, they cannot be detected by construction; stated as a property of that set, not run there.

D7. Exact ties decided by rounding (F6, AM75). A mathematical tie computed as two floats that differ in the last bit is
ranked by the rounding: deterministic, stable, arbitrary. One tick in the context-off outputs (scenario_s09_07 at 35,
1.7e-16); with context knowledge off it moves no gate answer (F7).
- (a) Accept it and record it as a consequence of AM75 (as KT11's ADDED line recorded the same for θ).
- (b) Ask for a different rule.
Recommendation: (a). AM75's reason ("no number in the rule") already accepts it; this asks only that it be recorded.
RULED (a): accepted and recorded as a consequence of the exact comparison (AM75).

## 8. The measurements after the build (a separate step and session)

They replace the what-if readings X and Y by runs. Kept apart from the build (CLAUDE.md, "Keep measurement tasks and
build tasks apart"); the model and the session as Hadi rules. Expectations from the updated oracles, and step 5's
re-declared properties (D5), are written before the runs.
- Step 4's recognition runs (57 on and 2 off, analysis/kitting/irb/tk2/) and step 5b's recognition runs (17): rerun
  against the oracle; the gate's answer per tick, read as WHATIF.md read it (the true task's earlier admissions kept or
  delayed; wrong admissions by kind; changes of the answer within a true stretch), now from runs.
- Step 5's planning cases (analysis/kitting/mpb/tk/, 6 on, 3 off, their references) and step 5b's planning runs (16):
  rerun against the oracle and the declared properties. The main interest: the two cases below min_separation that came
  from a wrong admission, scenario_s16_05 (28.3 cm, case 5) and scenario_s11_03 (11.3 cm): their decisions, holds, the
  `[sep]` minimum and F1's classes. The planning set's 16 authored cases re-read (12 reached in step 5b).
- COMPARISON.md's three numbers recomputed from the runs (the true task admitted earlier; admissions of a hypothesis
  that is not the true task; completion and the cases below min_separation).

## 9. Cases the rulings do not cover

None found that changes what is built. Checked and covered by the rulings or by existing rules:
- A belief tie at the leader cannot reach θ = 0.75 (two hypotheses at 0.75 or more cannot share a distribution), so
  which tied hypothesis is the leader never reaches the outranked check.
- An outranked leader at a `no_current_task` or `projection_expired` decision: refused like any refusal; the decision
  rests on the fallback projection (T-D P4).
- An admitted record whose hypothesis becomes outranked: kept (AM68 is a condition of admission only; AM69).
- A lone delivery that never gains observation warrant while it leads (scenario_s10_11 at 136; the standing human of
  scenario_s11_01 to _03): never admitted; the decisions rest on fallbacks. This is AM67's intended effect.
- Assignment knowledge off: commitment warrant never existed; AM67 changes nothing there.
D7 is the one place where a ruling's consequence is to be recorded rather than built around.

## 10. ccode's review (flags and objections)

- The rulings and the code agree on every point checked: the evidence AM68 ranks exists in the recognizer (F1), the gate
  is the one place both callers ask (F2), and the support restriction does not depend on commitment warrant (F3).
- AM67's cost is not always 1 tick. The 1 tick of the what-if reading Y holds where the human starts the next delivery
  on the tick after the previous one's completion (step 4's and 5b's scripts). In the context-off MPB set the
  commitment-only admissions move by the human's stand before starting: 6 ticks in scenario_s10_04 and s12_02 (134 to
  140), and no admission in scenario_s10_11 (predicted). This agrees with AM67's reason (the start tick is not known);
  it is a fact for the measurement, not an objection.
- AM68 removes step 5's cases 4 and 5 as authored: both rest on an admission at tick 0 that the evidence, by ×1.009 and
  ×1.0014, ranks below another hypothesis. The two planning cases below min_separation that came from a wrong
  admission (s16_05; s11_03, removed by AM67) are therefore predicted not to recur in their recorded form; whether a
  violation recurs later in those runs is the measurement's question.
- No objection to the rulings.
