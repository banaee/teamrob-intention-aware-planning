# Handoff: T-D cycle 1 closed; cycle 2 (L) and the IR test-bed

Written 27 September 2026, at the close of the chat "T-D-cont-2" (the continuation of "T-D-cont"). For the next chat, which carries two tracks: the IR test-bed and cycle 2 of T-D (L). Informative. The repo is authoritative over this text. Nothing here is a task list; sections 6 to 8 say what is open.

Terms follow docs/glossary.md §7's prose rule: "the `unknown` hypothesis" (historical), "unmodelled behaviour", "unexplained", "admitted"; never "unknown behaviour". New terms from this chat: adequacy finding, adequate, unresolved, unexplained (as a finding value), exhausted, derived phase, projected completion delay (D), tail probability (S_k), test level (α), hypothesis adequacy.

---

## 0. Sources of truth, and what to verify first

The pushed repo is authoritative. At the close of this chat the last commits were (all on main, pushed by Hadi after the close):

- 1.1 record: 2deef92; 1.2 sweep: 6c9c374, 92a8fdb
- 1.3 build: 84309e9, 367a3a7, 039d2a5, 09423e3, 2d4d759
- 1.3b: 5c67d62, bfa756b, 8a04aa9, 7f4559a
- 1.4 analysis: b57f50a (analysis/td_stage1/)
- 1.5r records: f77bc36, 6608c3e, 6e1caa5, 7b9c760
- 1.5b: 732c354, fe483d8, 1ccabf3, dec0e87, 681bc1a, 4e13cc0 (analysis/td_stage1b/)
- 1.5c: 0bc1347, dd7a4fd, 3bfc293, 096408e, 32de7c6, a9d05c8

Verify from the repo before stating a fact:

1. docs/design_decisions.md, entry "T-D R and E": R1 to R6, E1 to E7 with E6 amended twice and the boundary-tick rule, the section "1.5 rulings" (E8, E9, E10, G1), the three plan-step rulings, the recorded readings, the staging.
2. docs/glossary.md §5 and §7: the new entries, "built (T-D Stage 1)".
3. docs/recognizer_handback.md at HEAD, especially §1.10 (the adequacy finding) and §3 (crossings, admissions).
4. docs/TODOS_AND_DEFERRED.md: TODO-113 to TODO-120 (new in this cycle), TODO-87, TODO-93, TODO-95, TODO-96, TODO-97, TODO-101, TODO-117.
5. analysis/td_stage1/REPORT.md (1.4) and analysis/td_stage1b/REPORT.md (1.5b and its 1.5c section): every number in this handoff comes from them.
6. CLAUDE.md: the prior-ON convention, the rewritten `unknown` lines, the status paragraph.
7. shared/io_contracts.md: the output contract (BeliefState with finding, lifecycle, tails, hypothesis_adequacy).

If this text and the repo disagree, the repo wins.

---

## 1. What this chat settled, and why

### 1.1 The root question R: Design B ruled

The `unknown` hypothesis carried four meanings in one number: evidence against every live task hypothesis, the prior share at every reset, the mass left by normalisation at exhaustion, and nothing for a stand. The meta-planner never read it. The relative test cannot express "the best of my models is wrong". Hadi ruled B on 27 September 2026.

- R1. The `unknown` hypothesis leaves the hypothesis space. The belief is normalised over live task hypotheses only. u, the grade f and `graded_unknown_likelihood` leave the belief (ruled separately: "u leaves"). A lone live hypothesis reads 1.0 at zero evidence.
- R2. A second output: the adequacy finding (unresolved, adequate, unexplained), plus per-hypothesis tail probabilities S_k for evaluation.
- R3. Belief and finding are independent outputs; the state is their product plus the lifecycle state; not a state machine.
- R4. Exhausted is a lifecycle state (no live task hypothesis); no finding in it; nothing is unexplained in it.
- R5. The recognizer decides nothing about action.
- R6. Unchanged: the excess-path likelihood, β, origins and folds, the terminal pin, the boundary rule, the support restriction. The primary arithmetic invariant: on every tick the probabilities sum to 1 over exactly the live set H (two levels: normalised evidence before the output floor; the floored output with pinned keys at BELIEF_FLOOR).

Alternatives considered and set aside: Design A (patch the four meanings one by one; leaves the number the planner cannot read); "A now, B later" (the patches would be thrown away); Alternative 1 (a stack-aware recognizer) left open, not a third option on R's line. B keeps the door to Alternative 1 open; whether A could is not established.

### 1.2 E, time as evidence: the adequacy criterion

Ruled E1 to E7 in this chat, E5 in a separate chat ("E5 adequacy criterion"), then E8 to E10 on measurements.

- E1. Unit: each live hypothesis's derived phase, from its existing origin to its phase advance.
- E2. One statistic per hypothesis per phase, the projected completion delay D = e/v + (s − s_exp). e the excess path from the origin; v the body's speed; s ticks without movement since the origin; s_exp the Projector's priced standing for the phase (E9 revised its attribution).
- E3. Originally "time enters adequacy only". Superseded by E10.
- E4. Every live hypothesis assessed against its own phase; the finding is unexplained only when every member has S_k < α (intersection-union test).
- E5. Reference distribution: the belief's own likelihood shape read as a density, p(x) = βL(x)/(2 ln 2) on x ≥ 0, applied to v·D; tail S(x) = ln(1 + e^(−βx))/ln 2, S = 1 for x ≤ 0. A modelling assumption, stated as one. α is a per-phase test level, a run option (`test_level`, default 0.05, reported at 0.01, 0.05, 0.1), never chosen from a scenario, not a meta-planner threshold (DESIGN-07 untouched). At v = 20 cm/tick, β = 0.01/cm: threshold 334 cm at α = 0.05 (17 standing ticks; 167 cm walked straight away), 497 cm at 0.01. β gains a second meaning (the scale of the reference distribution) and is not retuned.
- E6, with two amendments and the boundary-tick rule (final form): a live hypothesis is a member of the test on a tick iff it has a derived phase this tick (an expected action) and that phase holds an observation. An observation exists once the phase holds walked path since its origin, or standing beyond s_exp, or a stationary tick with s ≤ s_exp in any phase whose s_exp > 0 (an observation with D ≤ 0, S = 1, L = 1). The initial walk at step 0 (s_exp = 0) holds no observation until walking. No hypothesis is a member on a boundary tick, including a stationary phase the boundary opens (E8's boundary clause applied generally). A hypothesis with no expected action this tick is never a member. Unresolved iff no member; unexplained iff every member has S_k < α; adequate otherwise. Non-members contribute no S_k.
- E7. The finding has no memory beyond each live hypothesis's current phase; computed fresh every tick; it clears when a member reaches S_k ≥ α or a boundary empties the membership. (Earlier wording "when every live hypothesis advances" was loose; the mechanism is per-tick recomputation.)
- E8 (1.5). On the tick a hypothesis's expected action completes, the completing hypothesis remains a member with S = 1 regardless of the phase it advances into. The completion is an observation consistent with the hypothesis.
- E9 (1.5). s_exp for a phase equals the Projector's priced stationary ticks that fall within the phase's span, derived from the Projector's own sequence (walk latency, action or bound duration, action latency). Kitting: 2 for `pick_up` and `place`; 1 for a walk entered from a completion (including the first walk after a boundary); 0 for the initial walk; 31 for `wait_at` (coffee); a stationary phase first observed gets its own duration only. Source: the body's `ACTION_COMPLETION_LATENCY` (1), `HUMAN_TASK_COMPLETION_LATENCY` (0), `default_action_cost` (1.0) and `duration_to_steps`, the same values the Projector receives. I3's phase rule unchanged.
- E10 (1.5). Belief and adequacy use the same D through two functions: the belief's evidence per phase is L(v·D) (clipped to 1 for D ≤ 0), adequacy's is S(v·D). On walking ticks without standing L(v·D) = L(e), so walking evidence is unchanged. Standing beyond the priced duration charges the hypothesis in the belief as a detour does. I4c narrows to "a stationary tick within a phase's priced standing is not a charge".
- Limitations recorded, not built: (a) sub-threshold waste is not summed across phases (an episode-level test by convolution is the form if a case demands it); (b) a regress at the proximity threshold (30 cm) resets that hypothesis's test; (c) the aggregate false-unexplained count per run grows with the number of phases; reopening condition: data establishing a null whose spread depends on phase duration.

### 1.3 G1, the guard on admission (the first ruling of G, ahead of the cycle order)

Admission requires the leader to be adequate in its own phase: the leader is a member and S_leader ≥ α. The recognizer reports hypothesis adequacy per live hypothesis (adequate, inadequate, no observation); the meta-planner receives no α and no S_k. `_clears_gate` is the one home of the rule; it checks θ first (so `none(below_theta)` lines are unchanged), then returns CLEARS, LEADER_INADEQUATE or LEADER_NO_OBSERVATION; `recognition_changed` fires on CLEARS. Reason strings: `none(leader_inadequate)`, `none(leader_no_observation)`. Why not the aggregate finding: it is existential over live hypotheses, while admission concerns the one hypothesis the planner acts on; the aggregate would admit a stale leader whenever a weaker hypothesis is adequate. TODO-97 (belief-aware planning) unchanged, on its own gate.

### 1.4 Rulings made at plan steps (recorded in the entry)

- s_exp's source: the body's `default_action_cost` through the Projector's rule, one source; TODO-113 records the schema-fact form (a duration on `pick_up` and `place` read by both the Projector and the recognizer) for when the Projector is in scope.
- The exhausted belief: the output distribution holds only the pins (retired keys at BELIEF_FLOOR), `most_likely` None, confidence 0.0; the lifecycle state is authoritative; the pins are an output convention, not belief mass.
- The two-level R6 invariant (above).
- Membership: as in E6's final form; the original per-plan ruling and both amendments are in the entry.
- The entry tick of a stationary phase is its first stationary tick (s = 0), since the odometer credits the step to the closing walk.
- "At the phase's location" follows from the phase derivation (every stationary action follows a walk whose `at()` completion holds): a kitting domain assumption the recognizer does not check.
- Reading 3 of 1.3b (a stationary phase directly after a boundary would be a member) is superseded by the boundary-tick rule.

### 1.5 Staging ruled

Cycles, one per open item, in the order L, P, G, X. Each cycle: design here (one question at a time), record (a ccode session, records only), build (a ccode session), verify, review. No build on an unrecorded ruling. Each cycle's rulings rest on the previous cycle's measurements. The relation to Alternative 1 stays open. T-D Q1 (option 1, the observation-based projection: the human at its observed position over each candidate's own plan duration, no horizon constant) is unchanged and is P's building block; it is recorded in TODO-95, not yet in design_decisions.md (P records it), and not built.

---

## 2. The mechanism as built at HEAD (after 1.5c)

```
observations
     |
     v
recognizer (per tick)
  lifecycle: retire hypotheses whose terminal completion holds; boundary -> prior over live H,
             origins moved; H empty -> exhausted (pins only in the output, no finding)
  per live hypothesis h with an expected action (derived phase):
      e   = excess path from the phase origin (EXCESS_MEASURES, same computation as the likelihood)
      s   = standing ticks since the origin (a standing clock mirroring the odometer)
      s_exp = entry latency (E9) + the phase's own priced standing
      D   = e/v + (s - s_exp)
      member iff (walked > 0) or (s > s_exp) or ((stationary phase or s_exp > 0) and s <= s_exp);
             never on a boundary tick; never without an expected action
      belief:   open value L(v*D) (1 for D <= 0), replaces the previous value within the phase,
                folds at the advance; normalised over H
      adequacy: S_k = S(v*D) for members; hypothesis adequacy = adequate if S_k >= alpha,
                inadequate if S_k < alpha, no observation if non-member
  finding: unresolved iff no member; unexplained iff every member S_k < alpha; adequate otherwise
  output: BeliefState(distribution, most_likely, confidence, finding, lifecycle, tails,
                      hypothesis_adequacy)
     |
     v
meta-planner
  _clears_gate: confidence >= theta, then leader's hypothesis adequacy == adequate
                -> CLEARS | BELOW_THETA | LEADER_INADEQUATE | LEADER_NO_OBSERVATION
  recognition_changed fires on CLEARS; admission on CLEARS; else today's below-theta behaviour
  (no observation-based projection yet: that is P)
```

Log line: `[IR] step=N most_likely=K confidence=C lifecycle=live finding=adequate tails=[K=S ...] leader_adequacy=<value>`; exhausted lines have no finding. `[run]` header names `test_level` and `speed`. The log reason `none(unresolved)` was renamed `none(unprojectable)` (the projector could not resolve the admitted hypothesis's task).

What the meta-planner does NOT do yet: read the finding beyond the guard; drop an admitted projection when its leader becomes inadequate (D2 retains a projection by identity); project a human with no admitted hypothesis (P).

---

## 3. What was done and measured in cycle 1

### 3.1 Sessions

- 1.1 record (Opus): the entry, the TODOs, the glossary, the handoff.
- 1.2 sweep (Opus): marks on every older record that assumed `unknown`, u, the grade, the odds invariant; Hadi ruled the unclear list (11 points, two amendments: TODO-61(b)/62 keep their independent measurements; the baseline description is "the four maintained sets, 48 logs, 36 distinct by md5").
- 1.3 build (Fable, plan mode then auto): R1 to R6, E1 to E7, the contract, `test_level`, the guard untouched, 12 new tests, baselines regenerated.
- 1.3b (Fable): the first E6 amendment (a stationary phase within its priced duration is a member with S = 1).
- 1.4 analysis (Opus): eight sections against the record's ground truth and the pre-build baselines.
- 1.5 design (here): E8, E9, E10, G1 ruled.
- 1.5r records (Opus). 1.5b build (Fable, plan mode). 1.5c (Fable): the second E6 amendment and the boundary-tick rule.

### 3.2 Numbers that matter (from the reports)

- Arithmetic: the R6 invariant holds on every tick (12,843 in 1.4; 12,923 in 1.5b; 12,929 in 1.5c). Walking-only spans give a belief byte-identical to the pre-E10 build.
- False unexplained on modelled ticks (prior on, 4,352 ticks, 204 phase instances): 3 after 1.3b (all on grasp ticks), 3 moved one tick after 1.5b, 0 after 1.5c, at every α, both priors.
- Boundaries: all 65 live boundaries read unresolved, adequate, adequate (the latency tick after a release is priced standing, a member with S = 1).
- Wrong table (scenario_s06_06, scenario_s07_03, BINDING_ABSENT): adequate during the shared prefix, then unexplained; detection delay after the prefix 21 ticks at α = 0.05 (28 at 0.01, 18 at 0.10); the admissions at 76 and 79 refused `none(leader_inadequate)` under G1.
- The foreseeable coffee break: after 1.3 the coffee walk tied with item_5 at 0.498 and the stand moved only the finding, so coffee_break was never revealed (s02_01, s04_01, s05_01, s05_02) and s05_02's 31-tick hold was lost. After E10, coffee_break is revealed during its stand (s05 at 32, s02 at 130, s04 at 158) and the hold returns (20 ticks at 32). A stay is revealed about 9 standing ticks after arrival, not on arrival: a recorded property, the price of the gradient.
- ac_switch_1 is not revealed (peaks 0.475 at 204, completes 205): unresolved case, see §7.
- Exhausted: scenario_s01_01 prior on at 141; the meta-planner refuses `none(below_theta)` at confidence 0. scenario_s04_01 prior on does not read exhausted: ac_switch_0 (a foreseeable task never performed) stays live and the finding turns unexplained from 344 (TODO-117, L).
- Prior off (appendix only, by the CLAUDE.md convention): after the human's last task, the robot's own remaining item becomes the lone live hypothesis at 0.996 (TODO-88's channel). After G1: refused on the boundary tick, admitted at b + 1 on "consistent so far" (one priced standing tick, belief 1.0 by normalisation); s01_01 off holds 32 ticks from 142 (the leader turns inadequate at 159 but the projection persists to 173, D2); s03_01 off: the hold is gone (refused inadequate at 147) and the run completes at 236 where it did not complete before.
- The 48 fixtures contain no TASK_ABSENT and no switch outside the support. Missed findings and detection delay for those cases are unmeasured. Oracle IR (TODO-101) is unbuilt; comparisons were against the record's `[coverage]` labels directly.
- Record lag: the record's task transitions land 2 ticks after the world fact the recognizer reads, in all 48 switches. The analyses use lag-corrected truth and say so.
- Non-member ticks per run after 1.3b: 3 to 9, all `move_to` phases with nothing walked and no standing.
- Adequate-below-θ (a member with S = 1 while its belief is below θ): 174 ticks after 1.3b (coffee `wait_at`), 38 after E10 (the ~9 ticks a rival needs to be charged).

### 3.3 What is tested (tests/)

- test_td1_adequacy.py: the R6 invariant (two levels), S at β = 0.01 and v = 20 (334 cm at 0.05, 497 at 0.01, S = 1 at x ≤ 0), D non-decreasing along a walk, unresolved on the first tick and after a boundary, the finding at a phase advance, exhausted (lifecycle, no finding, empty tails), a lone hypothesis at 1.0 with finding unresolved, a stand of 18 ticks in a `move_to` phase unexplained at 0.05 and adequate at 0.01, the stationary-phase member at S = 1, the s01_01 case now adequate, non-members.
- test_td15_build.py: the grasp tick as a member (E8), s_exp 2/1/0/31 as derived from the Projector's segments (E9), the walking-only regression (E10), a coffee-versus-walk tie breaking past θ after 9 standing ticks (E10), the guard refusing a lone hypothesis at a boundary and an inadequate leader, admitting the coffee leader in its stand (G1), the boundary sequence U, A, A, the latency tick after a grasp as a member (1.5c).
- 133 tests pass at HEAD.

---

## 4. Process rules established in this chat

- Sessions and cycles are numbered (cycle.session: 1.1, 1.2, 1.3, 1.3b, 1.4, 1.5r, 1.5b, 1.5c). Each session has one meaningful task.
- The loop: ccode report, cchat review showing only what matters for decisions, Hadi confirms, then the next session's prompt on its own. Reports and prompts are never mixed in one message.
- Prompts are given as a plain copiable snippet. The model and the session choice (new or continue) go in a line above the snippet, never inside it. Fable for sessions that build inside the recognizer or decide where the entry and the code disagree; Opus for records and analysis. Plan mode first for builds; auto after the plan is checked.
- The standing rule (added to every build prompt): the entry's mechanism stands over runs, baselines and tests; a test expectation changes only by derivation from the entry; a disagreement is reported, not fitted. Reports carry a section "Runs and tests that disagree with the mechanism".
- A build commit carries the test updates its ruling derives; only new tests get their own commit (learned at 1.5c, where a build commit was left with two tests failing).
- Prior ON is the primary set for runs, tests, debugging and reports; prior OFF is an appendix; no ruling on prior-OFF numbers alone (CLAUDE.md).
- ChatGPT reflections: Hadi shares them as points of view; the cchat consumes them for anything that improves a decision and does not argue about them. Two things worth carrying: the distinction between intention-conditioned projection and behaviour-based projection (for P); Alternative 1's three roles (operational recognizer, diagnostic layer, oracle) as separate from its four proposed states.
- Terminology: no new term is used until Hadi confirms it; "hypothesis adequacy" was confirmed; "realizer" was rejected (the projector; "realization" already means the meta-planner's costing); "recognised" is not a term.

---

## 5. Claims withdrawn in this chat (do not repeat them)

- "The handoff's 'four states' for Alternative 1 are in the repo": no; they came from the T-H design discussion (not enough evidence; outside vocabulary; plan departure; empty stack) and the repo records Alternative 1 in one clause.
- "The T-D Q1 entry is marked reopened": no such marking; Q1 lives in TODO-95, ruled, unbuilt.
- "Commit to belief-aware planning before R": withdrawn; adequacy has consumers without TODO-97 (the guard, the projection choice).
- "B gives no stale projection on the wrong table": withdrawn; B represents "delivery leads and is unexplained"; the boundary at a misdelivery is L, the stand is E.
- "One principle covers the four cases": B provides the representation; E, L, P do detection and handling.
- "Time enters adequacy only" (E3): superseded by E10 on measurement.
- "The finding clears when every live hypothesis advances" (E7 wording): per-tick recomputation; one member at S ≥ α clears it.
- "A stationary tick within the priced duration is not an observation" (E6 original): amended twice.
- "The tick after a boundary is unresolved; the sequence is U, U, A": derived U, A, A once E9 prices the release's latency tick to the first walk.
- "The prior-off lone-item holds will be gone after G1": one remained (s01_01), bounded; the other vanished.
- "The three false unexplained will disappear after E8": they moved one tick, until 1.5c.

---

## 6. Open for cycle 2: L, the belief lifecycle

Order for cycle 2 as ruled: L first. Its sub-questions, each with the measured case:

1. The boundary at a misdelivery (TODO-87, 1.4 finding 5). The terminal completion `obj_at(item, designated_table)` never holds, so no pin and no boundary; the item's hypothesis keeps leading at 0.995 into the human's next task; after the release it sits at S = 1 in its new phase and is re-admitted (s06_06 at 103, s07_03 at 94). The design question: what ends an episode when the world fact the hypothesis waits for will never come, without a scenario constant.
2. Retraction (TODO-118, TODO-94). An admitted projection outlives its leader's adequacy: D2 retains a projection by identity; the recognizer already reports inadequate; the meta-planner has no event for it (s01_01 off: inadequate at 159, hold to 173; s03_01 full_reorder off: inadequate from 139, hold to 219). The long misleading walk (TODO-94): the belief accumulates over the episode, adequacy is per phase; the gate now refuses a stale leader at admission but does not retract one already admitted. Design question: is retraction a trigger of the meta-planner (the gate stops clearing), a rule of the recognizer (the belief drops), or both; and what the robot does after retraction (P).
3. Resumption (TODO-93). A foreseeable task finishing inside an assigned delivery ends the episode and resets the belief while the item is visibly in hand (scenarios 11, 12, 41, 72 in old ids; verify current ids through docs/rename_table.md). T-H gives the human a task stack; the robot's belief is flat. Design question: whether the belief remembers a suspended task after a break, the first genuinely stack-aware question; the world fact "holding item" is what a stack-aware recognizer would use.
4. What is live after the work order (TODO-117). A foreseeable hypothesis (ac_switch_0) never performed keeps the human from reading exhausted and turns the finding unexplained (s04_01 from 344). Design question: whether foreseeable hypotheses are live after the assigned tasks are done, and what "exhausted" means with only foreseeable hypotheses.
5. What resets and what persists at a boundary (from the handoff of T-D-cont): the position, the standing clock, the origins move; the finding empties; whether anything else should persist.

Then P (the observation-based projection: T-D Q1 as building block, TODO-85 (b), TODO-119 the lone hypothesis at b + 1, the moving human, the staleness trigger, the two projection bases), then G (TODO-97 on its own gate; the lone hypothesis's 1.0 as no evidence), then X (WAIT against RECONSIDER, the occupied target, TODO-80's stop, communication on a persistent finding, TODO-96).

---

## 7. What could send us back to cycle 1

- The reference distribution (E5) is the belief's likelihood shape read as a density, a modelling assumption; its empirical adequacy is open and cannot be tested on the scripted human (D near zero). A test-bed case with controlled detours or stands could show it wrong.
- β carries two meanings (reveal timing, the adequacy scale). Over I4's region [0.005, 0.1] the α = 0.05 threshold runs from 33 cm to 669 cm. If the test-bed shows the two meanings pulling apart, E5's form is the place to look, not β's value.
- E1's limitation (a): sub-threshold waste is never summed across phases. A case of small waste in every phase would pass every test; the convolution form is recorded.
- E1's limitation (b): a regress at the proximity threshold resets the test; a human hovering at 30 cm never becomes unexplained.
- E10's unit assumption: one tick of standing is as surprising as v·1 tick of detour. It is E5's assumption applied to the belief; the coffee case validated it on one geometry only.
- TASK_ABSENT and outside-support switches were never measured. The corner walk is the case B was chosen for; the fixtures do not contain it. The test-bed's first job.
- The lone hypothesis: 1.0 by normalisation, admitted at b + 1 on one priced standing tick. If P and G cannot handle it, R1's "no reference term" is the place it comes from.
- Completion as evidence: E10 restored standing; completion itself still adds nothing beyond E8's membership. The detection channel (hit rate 1.0, false alarm 10⁻³) was rejected as a cliff for charging rivals on an arrival. If a case shows a reveal that only a completion can give (ac_switch_1 peaking at 0.475 one tick before completing may be one), this reopens.
- The record lag (2 ticks) and the Projector's latency (1 tick per action) are now both in the design; a change on the body side changes s_exp.

---

## 8. The IR test-bed (Hadi's proposal, agreed; the mid-step before cycle 2's design)

Purpose: test the recognizer in isolation, on scenarios written for it, with expectations derived from the design before the run, so that the result can say "IR is wrong" and not "the run looks odd". The 48 fixtures cannot: the robot acts, the layouts vary, and the cases B was ruled for (the corner walk) are absent.

Hadi's layered plan (the layout: a table KT at the top, two items 1 and 2 left and right, a coffee machine at the bottom, a corner_SE; the robot idle at the top left, observing only; the human assigned tasks 1 and 2):

1. Assigned tasks only: the human delivers 1 then 2; observe the belief and the finding tick by tick against derived expectations.
2. Assigned with a foreseeable task between tasks: deliver 1, coffee, deliver 2.
3. The foreseeable task inside the first task, after the human picked item 1 (resumption, L's case).
4. The deviations of the record: the corner walk (TASK_ABSENT), a switch outside the support, the wrong table (BINDING_ABSENT), the long stand, a finished work order.

What the test-bed chat must settle before any build, all design, none new mechanism:

- A run mode in which the robot has no task and only observes (whether the framework allows an empty robot pool today, or needs a switch; the meta-planner must not act).
- The layout and setup as T-L artefacts (layouts, setups, scenarios: the three artefacts of a run), authored with T-H's behaviour model (plain instances, the stand action, an Activity goal for the corner walk).
- The expectation format: per tick and per hypothesis, derived from the entry (the belief's trajectory from the geometry and β; D and S from the stand and s_exp; the members and the finding), so that the test-bed obeys the standing rule and cannot become a place where IR is tuned to pass.
- Reuse analysis/td_stage1b/tdlib.py and the per-section scripts as the harness for reading logs and comparing to truth.

Rule for both tracks: a test-bed finding enters a cycle as a design question with its ticks, the same way 1.4's findings do; it never changes the mechanism on its own.

Sequencing agreed: layers 1 and 2 first, their results are input to cycle 2's design; layer 3 when L opens (it is L's subject); layer 4 with the later cycles (P for the corner walk's projection, X for the response).

---

## 9. Suggested first steps for the new chat

1. Verify §0 from the repo. Report any disagreement with this handoff.
2. Confirm the terms in use and the process rules of §4.
3. Open the test-bed track: put the three design questions of §8 to Hadi one at a time (the idle-robot run mode; the artefacts; the expectation format), then a records session, then a build session for the layout, setup, scenarios and expectations of layers 1 and 2, then a run and a report.
4. With layers 1 and 2 reported, open cycle 2 (L) with §6's questions in order: the misdelivery boundary, retraction, resumption, live-after-work-order, what persists.
5. Keep §7 in view: any test-bed result that contradicts E5's assumption or E10's unit is a cycle 1 reopening, put to Hadi as such.
