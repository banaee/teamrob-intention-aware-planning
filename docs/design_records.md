# Design records: the record of planning and building

Deleted 5 October 2026 (T-F part 1's close, part E; analysis/README.md): the frozen analyses td_stage1, td_stage1b, l_build, irb2b_exposed_interval (tb2b_exposed_interval before 3 October), ablation_task_committed, f47_fixtures, t1_conflict_measurement, todo90_b2a_window, tc2c_scripts, tb1d_designations, tb2c_per_entry_holds and big_picture under analysis/kitting/ (analysis/ before the sort); the runs and run files of T-K part 1's steps 5 and 5b (planning) and 5e and of T-F part 1's stage 2 check (configs/kitting/mpb/tk, mpb/tk5b, tk5e, tf1/check; their READMEs and reports stay). A path cited below under these names is held by commit 362af19 (`git checkout 362af19 -- <path>`).

Moved verbatim from `docs/design_decisions.md` on 2 October 2026 (Hadi's rulings of that day: the records split;
one record file beside design_decisions.md, one heading per task). Each block is headed by the title of the entry it
comes from and its id; in design_decisions.md an index line with the same id stands where the block was.

## Phase 4 (4A to 4C: the I-series, the T-series, F1, C, D2, D3)

**One leg is one observation — replace, do not multiply** — RECORD [phase4/1], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
Crossings after the change (PYTHONHASHSEED=0; runs 20260910_1552xx — superseded as regression
baselines by runs 20260911_0826xx after T2 rescaled projection time to execution ticks; the
`theta_crossed` steps below are unchanged in those runs, the built/selected columns are not —
see TODO-28 and TODO-30). `theta_crossed` = crossing events; "built" = admitted projections:

| run      | first ≥ θ            | theta_crossed | built projections  | note |
|----------|----------------------|---------------|--------------------|------|
| s20 off  | 22 (0.797), grasp    | 22, 89        | 22, 24, 89, 96     | late-reveal condition |
| s20 on   | **11 (0.780)**       | 11, 82        | 11, 23, 82, 95     | PRE-GRASP: human crosses x=0 into zone_SW at 11 (13.99 → −2.92) and ZONE_BOOST doubles item_3 (0.641 → 0.780); robot at (−393, 85), its move_to to shelf_4 completes at 21 — roughly half the approach; projection built, item_4 min_dist 14.98 at cost 812. This is the fixture condition B2 needs. It is a zone-state reveal on top of one honest chord (0.641), not an accumulation. |
| s00 off  | 41 (0.797), grasp    | 41, 111       | 41, 63, 111, 131   | |
| s00 on   | 41 (0.797), grasp    | 41, 81        | 41, 63, 81, 95, 131| leg-2 first chord 0.856 (carry-leg chord had already favoured shelf_2, 49° off, L 3.4) |
| s10 off  | 257 (0.769), grasp of item_4 | 257   | 257, 262           | grasp of item_2 at 31 gives 0.662: item_2 : coffee : unknown = 4 : 1 : 1 — coffee has no item binding and survives the pin |
| s10 on   | **107 (0.853) on item_6 — wrong** | 107, 257 | 107, 142, 200, 257, 262 | coffee-leg criterion FAILED, known consequence of TODO-46: `coffee_break` gets no chord evidence, so the walk to the coffee machine is credited to shelf_6 (27° off) and doubled on zone_SW entry |

Every belief change in all six runs is attributable to a leg start, a discrete event, a
quadrant crossing, or a world change (a robot-carried item's expected position moving with
the robot — switch-off only, since those hypotheses are inadmissible switch-on). No
per-step accumulation remains; within-leg values are flat to the third decimal.

**Projection time includes what the body spends finishing an action, and the human's projection starts when it was observed (L2)** — RECORD [phase4/2], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
MEASURED (L2, `analysis/l2_execution_lag/REPORT.md` (deleted in the analysis cleanup, September 2026; carried in the L2 entry of design_decisions.md and TODO-77), TODO-77's own terms). The systematic whole-tick lag
is gone: medians move from −1.46/−3.32 to −0.46/−0.32 for the robot (2- and 4-action plans) and from
−2.21/−5.32 to −0.21/−1.32 for the human. What remains is exactly the two things above: a discrete-step
forward model of the executor, using no execution data, predicts the actual release tick EXACTLY for all
68 human and robot 2-action rows, and exactly one tick early for all 35 robot 4-action rows. That last
+1 is not quantisation and is not compensated either: the robot re-plans at its own `task_committed`
trigger, which fires on the tick that would have acknowledged the `pick_up`; the fresh
`deliver_already_held` plan does not contain that `pick_up`, so `continue_plan()` loads from the start
and the carry begins on that very tick. One of the four charged latencies is never spent. Modelling it
would mean the projection predicting the robot's own future triggers, which are decided FROM the
projection — recorded in TODO-77, not fixed.

CONSEQUENCE, and a correction to the expectation this task was set with. "B3 is plain-cost argmin, so
any change comes from durations" is not what the code does: B3 is an argmin over candidates that
`_detect_interference()` has not excluded, and that filter is still live. Across the ten sweep
conditions the latency changed every cost (by one tick per action) and reordered NO candidate set at any
of the 93 triggers compared. The single decision change in the sweep comes from the offset instead:
with the two agents finally in phase, scenario_30's mirror crossing is projected as the near-coincidence
it is (`min_dist` 15.37 → 0.49 cm, the continuous-time minimum of two agents passing through each other
— `[sep]`'s 11.0 cm was the closest integer-tick sample), and the superseded `min_safe_distance = 1.0`
excludes the candidate. Ablation confirms it: latency alone changes no decision, offset alone produces
the whole change. That threshold is already superseded (R1; removed in T10), so the exclusion is a
vestigial mechanism firing on a newly-accurate number, not a new policy.

**B3 selects on realized cost: the argmin of T_r + δ over the realizable candidates, the winner's hold executed, plain cost when nothing realizes (T10)** — RECORD [phase4/3], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
MEASURED (T10; `analysis/t10_b3_realized/comparison.md` (deleted in the analysis cleanup, September 2026; carried in the T10 entry of design_decisions.md, TODO-36 and TODO-79); s00/s10/s20/s30 × prior off/on, run to
completion, PYTHONHASHSEED=0; `plain`+`none`, `realized`+`none`, `realized`+`b2a` with ρ = 0.5):
- PLAIN against L2: identical in every condition but s30_on, where at step 21 the superseded
  `min_safe_distance` exclusion no longer fires and item_4 stays selected (the L2 report predicted
  this). Plain is therefore the old B3 minus the vestigial filter, on the fractional T_r.
- REALIZED against PLAIN — realization's effect. s00 (both priors): identical; every δ is 0. s10, s20,
  s30: the same TASK ORDER except s20_on (below), reached later: the holds B2 executed under T4's
  `b2a` are now B3's, at the same triggers with the same δ (s10 29/33/35 → 6, 2, 0; s20_off 20/24/30
  → 7, 3, 1; s20_on 6/30 → 7, 1; s30_off 28/46 → 6, 1), plus s30_on 40/77 → 7, 1, which T4 did not
  have because its old B3 had switched to item_2 at 21. 12 holds, 43 ticks held, 2 interrupted
  (s10_off 29→33 and s20_off 20→24, the remainder re-decided as at T4). Completion slips by the held
  ticks: s10 +6, s20_off +8, s30 +7/+8. ONE all-unrealizable event, s30_on 21 (the mirror crossing,
  both candidates `hold_position_violated`): the fallback keeps item_4 on plain cost, which is what
  plain does too; its residual conflict is the 0.00 cm pass-through at tick 23, inside that window.
- REALIZED, `none` against `b2a`: IDENTICAL decision sequences, greps and holds in all eight
  conditions. B2 continued exactly where B3 keeps the current task, and both escalations reach a B3
  that decides as it would have without the gate. On these fixtures at ρ = 0.5 `b2a` is a computation
  saving (one realization per trigger instead of one per candidate) and nothing else (TODO-36).
- s40 (regression sweep only, `realized`+`none`): byte-identical to L2 on every grep — no δ > 0.
- ACTUAL SEPARATION (TODO-79, `dist` and the continuous `min`): every moment below 50 cm is past T_h,
  under no projection, after the robot finished, or inside the s30_on fallback's window, EXCEPT s10
  tick 75 at 49.15 cm (both priors, both realized configurations) — TODO-77's step-quantisation
  residual, inside the step-35 decision's window by 0.29 tick. The continuous minimum lowers the
  crossing minima (s30 tick 23: 11.03 → 0.00; s20_off crossing: 11.64 at tick 51 → 9.02 over tick 52) and extends episodes by
  one tick; it moves nothing from outside to inside.

FINDING (RESOLVED by F1, "Robot-responsible separation", which redefined the violation; the mechanism
below is corrected there: it was the robot's stationary placement, not its walk, that the joint-state
rule counted), recorded at T10: s20_on, step 57 (`theta_crossed`, the human's next
task admitted). The robot is carrying item_4, 3.95 projected ticks from placing it. The human has just
placed at the table and is walking away, and at the trigger stands 37.5 cm from the robot — already
inside `min_separation`. item_4's plan converges on the departing human at δ = 0 and its hold position
is violated at step 1, so it is UNREALIZABLE; item_6's plan (return item_4 to its shelf first, then
fetch item_6 — six actions) walks away from the human and realizes at δ = 0, cost 84.65. B3 selects
item_6. Under plain the robot had delivered item_4 at 54 (no holds earlier); under realized the
step-6 and step-30 holds placed the robot's arrival exactly where the human departs. Consequence:
completion 292 vs 228 ticks (+64), item_4 delivered third instead of first, and the human passed the
robot anyway (56–57: 35.1 cm, past T_h). RESOLVED (F1, next entry but one: the flag and the
hold-position check are gone; item_4 wins at 57 with δ = 2). Mechanism as it was: realizability is a HARD GATE inside B3 whenever
some candidate realizes — the argmin ranges over realizable candidates only, so an unrealizable
candidate cannot win however short its plan — and `hold_position_violated` fires here not on a
projected conflict but on the PRESENT state (the human already within `min_separation` of where the
robot stands), which no hold can change and which afflicts every candidate whose first step converges.
This is the over-reaction the wait revision set out to remove, returning through the realizability
flag: switching cost 64 ticks to avoid a 4-tick completion whose "conflict" was the human leaving.
The design as decided says this is what B3 does (the all-unrealizable fallback covers only the case
where NOTHING realizes), so it was built as decided and is reported here. Where it belongs: T6 (the
ablation will show it as the largest realized-vs-plain difference) and D2 / the R1 follow-up — whether
an unrealizable current task a few ticks from completion should compete on plain cost, whether a
present-state violation is a realization question at all, or whether this is `min_separation`'s value
(TODO-28) at the table. Nothing here was tuned.

**What a trigger is an event of: `recognition_changed` against the decision record replaces `theta_crossed`; the blocked event designed, not built (D2)** — RECORD [phase4/4], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
MEASURED (PYTHONHASHSEED=0; the sweep and the evaluation fixtures, prior off / on; baselines at the
pre-D2 HEAD agree byte-for-byte with F1's and F47b's on the decision grep):
- Fires of the replaced trigger, old `theta_crossed` → new `recognition_changed`: s00 5→4 / 2→4, s10 6→7 /
  4→7, s20 7→4 / 2→4, s30 2→4 / 2→4, s40 5→10 / 5→10, s50 8→6 / 3→6, s70 5→6 / 3→6, s71 5→7 / 3→6. The new
  count is two per human task everywhere (a recognition, then its end) except s71_off, where item_5 enters
  twice (61 and 72): the robot's own `task_committed` at 69 fell inside item_5's dip (0.572), its admission
  refused, the record was cleared, and item_5's next clearing of the gate is a new recognition. A property
  of the rule, stated here: the record is what the LAST decision projected, whichever trigger made it, so
  the guarantee is "no fire while a projection stands", not one fire per hypothesis. Every fire that retracts — admission `none(below_theta)` or
  `none(unknown)` — decided a CONTINUE in all 16 conditions.
- PRIOR-ON: decisions identical modulo the reason string and the added retraction continues in s00, s10,
  s20, s30, s40, s50, s70 (completion 168 / 420 / 239 / 162 / 378 / 237 / 187, unchanged; `[sep]`
  byte-identical). s71_on: the retraction at the human's boundary, step 54, replaces the last tick of the
  32-tick hold placed against the coffee stay that ended on that tick (executed 31, interrupted); the
  robot leaves one tick earlier, completion 204 → 203. Expected under T4's rule that a later decision
  replaces the hold in progress.
- PRIOR-OFF: the repeated crossings no longer decide (s00 113 / 115, s10 33 / 35, s20 and s50 24 / 30 /
  91 / 95, s70 and s71 65); s20 and s50's first hold runs its 8 ticks in one piece instead of 4 + 4
  (interrupted and re-realized at 24). Robot motion identical in s00, s10, s20, s30, s40, s50, s70
  (`[sep]` byte-identical). Completion DECLARED two ticks later in s00, s20, s50 (166 → 168, 235 → 237,
  235 → 237): the old `theta_crossed` on `unknown` at the robot's own last delivery (TODO-54) declared the
  empty pool on that tick; nothing enters on `unknown` now, so `no_current_task` declares it when the
  executor's bookkeeping learns of the completion, two ticks later. The run's behaviour is the same;
  two trailing `[IR]` lines are the only other difference. s71_off: the boundary retraction at 54
  interrupts the hold's last tick as prior-on, the switch to item_3 comes at 108 instead of 111,
  completion 204 → 201.
These are the meta-planner-side regression baselines from here on: `analysis/d2_recognition_trigger/`
(`sweep/` for s00–s40, `fixtures/` for s50 / s70 / s71; logs local, README committed).

## T-A, the pipeline revision

**The pipeline from T-A: what moved, and why (T-A1)** — RECORD [T-A/1], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
REVISED ORDER (Hadi, 30 September 2026; `docs/roadmap.md`, "The plan from T-A", its order block): T-G no longer
holds 4D or ROS (4D is in the T-D tail, ROS is T-S); T-E is superseded by T-V, track 1. The order stated below is
history; the four decisions stand.

DECIDED (cchat, September 2026, after reading the state in `analysis/big_picture/STATUS.md`). The plan from
here is T-A (records) → T-B (B3.B on two tables) → T-C (the human action script) → T-D (robustness in
kitting) → T-E (demonstration) → T-F (evaluation, Phase 5) → T-G (later: a second domain in Mesa, 4D,
ROS); `docs/roadmap.md` holds it. Four decisions shape that order.
1. B2 (`gate_strategy`) IS AN EVALUATION FACTOR, NOT A DESIGN STEP. STATUS.md named "does the commitment
   gate survive?" as the first question for generated fixtures. It is not a question to answer before
   other work: `none` and `b2a` are both built, nothing downstream depends on which one wins, and B3.B
   leaves `b2a` unchanged (it commits to a task). So it is one factor of T-F's factorial, and no step
   re-reads B2 first. TODO-36 closes on this.
2. THE RANDOMISED HARNESS (TODO-47) MOVES TO T-F. It was "the next step" because three questions (B2, the
   gate's reopening condition, the scale of `min_separation` and β) were said to be answerable only there.
   Of these, B2 is a factor (1), the gate's reopening condition (TODO-47 (g)) is a T-F condition, and the
   scale question is gone: `min_separation` is a distance the body supplies ("`min_separation` is supplied
   by the body", above) and β is a physical tolerance ("β is a physical tolerance", below). What was
   genuinely blocking is the ordering fixture, so TODO-47 (f) stays in T-B as hand-built two-table layouts,
   with programmatic registration built there as the first part of fixture generation.
3. THE DEMONSTRATION COMES AFTER T-B, T-C AND T-D. Built now it could show switch and hold (s70 / s71) only.
   After them it shows what the framework claims: a two-table ordering, a change of mind, `unknown` as an
   outcome, as well as switch and hold, plain against realized cost, the stop on, prior off.
   SUPERSEDED IN PART (T-D R1, 27 September 2026): the `unknown` route no longer exists; its replacement is G. Not closed: the downstream response is G and X. design_decisions.md, "T-D R and E".
4. THE DOCUMENTATION PASS FOR THE PAPER COMES BEFORE THE PAPER, NOT BEFORE THE DEMONSTRATION. The demo is
   an instrument for seeing behaviour, and it needs the viewer, not polished documents; the paper needs
   the record consolidated once the evaluation's content is known.
Reference: T-A1, September 2026; `analysis/big_picture/STATUS.md`; TODO-36; TODO-47

---

## T-B, B3.B on two tables

**B3.B (`full_reorder`) is lookahead for the choice of the next task, built next: geometry couples tasks in two-table kitting (DESIGN-16 revised)** — RECORD [T-B/1], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
"Do not implement piecemeal" is replaced by an order (PROPOSAL): the successor state and `project()` for
orderings first, checked alone (a length-1 ordering byte-identical; a later entry equal to the same task
projected alone from a world in which the earlier task has really been done); then B3.B on plain cost;
then on realized cost, once the hold placement is decided. This is also the order of the evaluation.

OPEN POINT 1: WHERE A HOLD THAT CLEARS A CONFLICT IN A LATER TASK IS PLACED. Two options:
  (A) one δ at the decision position, the whole sequence shifted, as T4 / `realize()` does today;
  (B) a hold at the boundary before the task it clears: δ_1 at the decision position for task 1 (today's
      realization of task 1, unchanged), δ_2 where task 1 ended (at the table) before task 2 starts, and
      so on. Each is still "a hold where the robot is", on a segment boundary: not a detour (4D) and not
      partway along a segment (TODO-70).
PROPOSAL (not decided): (B), for these reasons.
  - Point 4. Only the head's hold is executed before the next re-decision. Under (A) a conflict in task 2
    makes the robot stand NOW, before task 1, on the strength of a lookahead that is re-priced at the
    next boundary: the executed hold would commit to the order, which point 4 says the order is not.
    Under (B) `UpdateResult.hold` = δ_1 is exactly the hold `single_task` would execute for the same
    head, so B3.A and B3.B differ in WHICH task is chosen and in nothing else, which is also what makes
    the evaluation readable.
  - Cost. The per-boundary minimal shifts are optimal among boundary placements and never cost more than
    (A): with Δ_k the cumulative shift of task k, taking Δ_k = the smallest whole tick ≥ Δ_{k−1} outside
    task k's violating intervals gives, by induction, Δ_k ≤ any feasible non-decreasing sequence's, and
    (A)'s single δ is one such sequence. Task k's violating intervals do not depend on the earlier shifts
    (positions are unchanged; the human's projection is fixed), so this is `realize()`'s one-pass walk,
    once per entry. The cost of an ordering is Σ T_r + Δ_n.
  - A concrete case in the current baselines (an illustration, not a specification): s00_on, the
    `recognition_changed` decision with three candidates: item_7 costs 12.58 with δ = 0, T_h = 59.48,
    and item_6 alone has δ = 8. In (item_7, item_6) a conflict can only lie in item_6; (A) would stand
    the robot before item_7 for it, (B) at the table after item_7, if it is still there from the new
    start.
  AGAINST (B), to be weighed in cchat: the boundary is at a table, where the human converges. A standing
  robot never violates (F1), but it may be in the human's way there more than at the decision position;
  that is the team-level cost of TODO-15, not priced by either option. And (B) changes `RealizedPlan`
  (one `delta` / `hold_position` today) to per-entry holds, where (A) needs no type change.

OPEN POINT 2: WHAT B2 COMMITS TO UNDER B3.B, a task or an order. PROPOSAL (not decided): a task. B2 is a
mid-task commitment gate on the CURRENT task (`b2a`: realize it alone, continue iff δ ≤ ρ × (T_h − now));
under point 4 the order past the head was never committed to, so there is nothing of it to keep, and
`b2a` runs unchanged. Committing to an order would need the order stored as decision state, against the
one-field decision record (D2) and the unordered queue. Consequence to state in the build: `UpdateResult.queue`
is then the winning order's tail, informational only; `_queue` order carries no commitment, as today.

THE ONE-TABLE EXPECTATION, MEASURED. Point 1's "B3.A and B3.B cannot differ on any current fixture" is an
expectation, not an identity. Two mechanisms can separate them on one table:
  - the arrival point (T9): a delivery ends `arrival_radius` (30 cm in Mesa, 1.5 ticks) short of the
    table on the side it approached from, so the next walk's length depends on the previous task by up
    to that scale per boundary;
  - point 3 itself: where T_h reaches past the head, orderings with the same head differ in the
    conflicts of their later tasks. Measured on the graded-evidence baselines
    (`analysis/g1_graded_evidence/sweep/`, the five fixtures, both priors): of the B3 decisions with an
    admitted projection and more than one candidate, T_h exceeds the winner's cost in s00_on (1 of 3:
    12.58 against 59.48), s10_off (2 of 3: 45.81 / 48.29, 37.27 / 67.05) and s10_on (3 of 4: 50.81 /
    53.02, 80.09 / 110.05, 58.27 / 88.05), and in none of s20, s30, s40.
The candidate gaps at those decisions are tens of ticks, so identical choices are still expected; but a
difference there is to be traced to one of the two mechanisms, not presumed a bug. The byte-identity
check is the default run: with `strategy` left at `single_task`, the greps must not move.

THE EVALUATION (B3.A against B3.B, to be run when the build and the fixtures exist):
  1. plain cost first (`cost_strategy` plain: geometry only, no human consideration) on the two-table
     fixtures: does the head differ, and the completion tick (world fact, T6);
  2. then realized cost on the same fixtures, under the hold placement decided from open point 1;
  3. the current one-table fixtures under B3.B, expected identical in choice (above), as the check that
     the lookahead adds nothing where geometry does not couple tasks.
Needed for it and not present today: `strategy` has no run option (`gate_strategy` and `cost_strategy`
do); the build adds one. The fixtures set no parameter and select no value (as T6).
A consequence of two tables to MEASURE on those fixtures, outside B3.B: the recognizer's hypothesis space
is the product over typed parameters, so `deliver_item` has items × tables hypotheses, and the two table
hypotheses of one item share the fetch walk. With the assignment prior off, the belief is expected to
split between them until the carry walk discriminates, which would move the admission of the human
projection later than in one-table layouts. Expected from the code, not measured.

THE FIXTURE SIDE (T-A1, September 2026; T-B1). A kitting layout with a second table on the opposite side
of the room and each item assigned to one table. Example: items 4 and 6 go to the north table, item 7 to
the south table. From the north table item 7 is the far task, so the orderings (4, 6, 7) and (4, 7, 6)
differ in walking cost with no human present: that difference is what single-task selection cannot see,
and it is the first thing the evaluation looks for (plain cost). Hand-built, registered programmatically
(TODO-47 (a), built here as the first part of fixture generation).
ONE DESIGN QUESTION BEFORE THE LAYOUT IS WRITTEN, OPEN: what kind of fact is an item's destination table?
  - A DOMAIN fact: the domain model says where each item goes. One `deliver_item` hypothesis per item; the
    recognizer knows the table from the domain, and the belief is as in one-table kitting.
  - A WORK-ORDER fact: the table is a binding of the task instance, as `?kitting_table` is today. The
    hypothesis space is items × tables; the assignment prior (when on) restricts it to the assigned
    pairs. Expected recognizer effect with the prior off: the two table hypotheses of one item share the
    fetch walk, so the belief splits between them until the carry walk discriminates, and the human
    projection is admitted later than in one-table layouts. Expected from the code, not measured.
The two readings put the same layout to different uses (the first tests ordering with the recognizer as
it behaves now; the second also tests the recognizer on a split it has not met). The choice is cchat's.

**One hold per entry: an ordering is realized by one minimal-shift search per entry, and B2 commits to the current task (T-B Q2, T-B Q3; T-B2c)** — RECORD [T-B/2], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
AS BUILT. `shared/realization.py`: `realize()` runs the searches and `_realized_segments()` places each
entry at its cumulative shift, with the stationary stretch of each hold where it is taken.
`shared/types.py`: `RealizedPlan.holds`, `.cumulative_shifts`, `.delta` (property). `shared/meta_planner.py`:
`_replan_orderings()` realizes every ordering against the human projection (`cost_strategy realized`) or none
(`plain`) and ranks on `RealizedPlan.cost`. Orderings with a common prefix share no work (accepted at
review, ccode's reasoning): sharing the prefix's
projection would need a successor state that outlives a `project()` call, which T-B2a rules out; measured, one
B3 call with a pool of four costs about 32 ms with an admitted projection (8 ms without; `single_task` about
1 ms), and triggers are events. Log, `full_reorder` only: `[meta-ord]` as in T-B2b; `[meta-win]` for the
winning ordering (`holds` per entry, `shift` the cumulative shift of the last entry, `T_r`, `cost`, `share`);
`[meta-b3]` with `selection` as under `single_task` and `ordering=`.

CHECKED (`analysis/tb2c_per_entry_holds/`, scenario_81, both priors; the B3 calls of the `full_reorder` run and
of the `single_task` run, every ordering of the pool at every call: 402 orderings, 260 against an admitted
projection).
- DOMINANCE: 0 rows where the per-entry cost differs from the common-shift cost (computed in the script only),
  so none where it is higher. A null result, as R1 measured that more places for a hold seldom change the
  total. It is not vacuous: 12 orderings carry a hold, 8 of them before a LATER entry (item_1 after item_6,
  holds [0, 2, 0, 0] and [0, 3, 0, 0]); in those 8 the cost equals the common shift's and the hold is taken
  elsewhere (at the table after entry 1, not at the decision position). All 12 are on the `single_task` run's
  course; under `full_reorder` no ordering priced on scenario_81 carries any hold.
- THE HEAD'S HOLD: the hold before the first entry equals the head realized alone in all 402.
- VALIDITY, by F1's independent method (sampling at 0.001 tick inside [trigger, T_h], rules (a) and (b)): the
  14 winning orderings with an admitted projection and the 8 orderings with a later hold have no violating
  sample; each later hold is minimal (its entry at shift − 1 violates).
- A synthetic two-entry case (literal segments; a check of the code, not a finding): per entry [0, 14], cost
  34; one common shift 24, cost 44; both clear under sampling; entry 2 at shift − 1 violates.
- BEHAVIOUR: scenario_80 and scenario_81, both priors: `single_task` heads 6, 1, 7, 4 (completion 261 and 265
  from the world fact; one 4-tick hold in scenario_81), `full_reorder` heads 7, 4, 6, 1, completion 220, no
  hold. scenario_00, both priors: identical to `single_task`. The executed behaviour under `full_reorder` is
  the same as at T-B2b on these fixtures; the full comparison is T-B3.
- IDENTITY: the 20 baselines byte-identical under the default strategy; `b2a` runs (scenario_20 with executed
  holds, scenario_81; both priors) byte-identical between the commit before and the change.

A FINDING FOR T-B3. On every current fixture no winning ordering under `full_reorder` carries a hold, so
T-B2c changes nothing executed. scenario_81 does not exercise realized cost under `full_reorder`: its conflict
belongs to `single_task`'s course (6, 1, 7, 4), and the course `full_reorder` chooses (7, 4, 6, 1) never meets
the human, so its saving mixes two causes, the order of the tasks and not meeting the human. A fixture for
T-B3b must put a conflict into the orderings `full_reorder` would choose; Hadi designs it (TODO-47,
f-designations).

NOT PART OF THIS DECISION. Entries after the first are projected about one tick late per preceding entry with a
`pick_up` (TODO-77). It is an error in the input to `realize()`, present under `single_task` too, and is not
compensated here; cchat decides it. No `full_reorder` baselines are recorded until Hadi confirms T-B2c.

**A reload never cancels a completion tick the body states: the Mesa executor spends the acknowledgement after the robot's pick_up (T-B Q7)** — RECORD [T-B/3], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
WHAT REMAINS UNCOMPENSATED. STEP QUANTISATION only (L2's decision, unchanged): a walk of projected duration
`dur` executes as ceil(dur) steps and the walker stops on the first step inside the arrival radius, so it
finishes late and the next walk may start up to one step off its projected start. Measured per delivery on
scenario_80, executed minus projected, before → after: fetch part −0.89 → +0.11, −0.36 → +0.64, −0.60 → +0.40,
+0.41 → +1.41; carry part unchanged (+0.62, +0.67, +0.92, +0.48); total −0.27 → +0.73, +0.31 → +1.31,
+0.32 → +1.32, +0.89 → +1.89. The executed fetch gains EXACTLY one tick in all four deliveries. Before the
fix three of the four ran SHORTER than projected — the skipped acknowledgement masking quantisation; after
it every residual is positive, which ceil-per-walk alone produces. TODO-77's residual is closed with that.

MEASURED, the 20 baselines (both priors; `analysis/tb1a_destination/`, `analysis/tb1b_two_tables/`).
Completion from the world fact moves by one tick per robot delivery, less where a hold carried the tick:
s00 166 → 169, s10 418 → 422, s20 235 → 237, s30 160 → 161, s40 376 → 379, s50 235 → 237, s70 185 → 186,
s71 201 → 203, s80 261 → 265, s81 265 → 268. The three carried ticks: s20 / s50 and s30, where the post-grasp
decision already held for δ = 1; s70, where the hold at step 61 / 60 re-realized 2 → 1, and s81, where the
hold at step 39 → 40 re-realized 4 → 3 — the robot reaches those decisions one tick later, so one fewer tick
of shift clears the same human, minimal in both. THE DECISION SEQUENCES ARE OTHERWISE UNCHANGED, with two
exceptions, both traced to a trigger that used to land on a cancelled completion tick: s10 (both priors) and
s00_on, where the run now spends it; and one decision that was never separately raised before, s81_off's
`task_committed` at 132, because the grasp and a belief change no longer share a tick. Changed decisions are
explained, never adjusted. The human's lines are byte-identical in all 20 runs, and 17 of the 20 were
byte-identical between the grasp-only fix and the general rule — including the three whose post-grasp hold
carries the acknowledgement, so moving that absorption from `hold()` into `step()` preserves behaviour.

THE ACCEPTANCE CRITERION THAT WAS WRONG, CORRECTED. The task expected every `[IR]` line to be byte-identical,
on the ground that the robot does not touch the human and the recognizer observes the human only. The second
half does not follow: the recognizer reads the `WorldState`, and the robot writes into it (a) a carried
item's position, which IS the carrier's, so while the robot carries item X the hypothesis `deliver_item(X)`
is scored against a target that moves with the ROBOT, and (b) task completion as a WORLD FACT, so the pin
retiring that hypothesis falls on the tick the robot's release makes `obj_at` hold. Measured: with the prior
ON every `[IR]` line is identical (the support is the human's assigned pool and holds none of the robot's
items); with it OFF 1 to 29 steps per run differ, by at most 0.165 in confidence where `most_likely` is
unchanged and by up to 0.497 at the pin ticks. The human's own lines are byte-identical in all 20, so nothing
reaches the OBSERVATION. The criterion as corrected is met. The recognizer question this exposes — with the
prior off, a live hypothesis about the human whose item the robot is carrying away — is
`docs/TODOS_AND_DEFERRED.md`, TODO-88, for cchat; nothing was changed for it.

## T-C, the human action script

**The human action script (T-C1, decided)** — RECORD [T-C/1], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
RECORDED FOR T-D, not designed here: an observed history of the human's tasks in the robot's mind (completed,
dropped, `unknown` episodes), for evaluation (TODO-92). The robot taking over an abandoned task is TODO-15.
Not decided in T-C1 and left where they are: TODO-85 (a stationary human; half (b), the robot's action under
`unknown`, with T-D) and TODO-88 (its own item).

AS BUILT (T-C2b): SEQUENTIAL EXPANSION. `resolve_script()` resolves the script's elements in order, each
against the initial world advanced by every element before it: the primitives grounded and handed to
`shared.projection.successor_state()`, the successor state of T-B2a, made a module function so that the
projection of an ordering and the script share one derivation (no second successor state); the agent stands at
the target of its last walk; a `Stay` changes nothing. A deviation's injected content is resolved against the
state its task's expansion leaves at the anchor (after the kept part, for `abandon`); anchors are resolved
against the task's own expansion as before. Check: `abandon(deliver(item_3), after="pick_up",
then=[deliver(item_5)])` expands the second delivery with `deliver_with_return` (item_3 to its shelf first);
with `before="pick_up"` it expands with `deliver_default`.
AS BUILT (T-C2b): THE ACTION-LEVEL HUMAN EXECUTOR. `HumanAgent` holds the resolved list (`load_script()`, by the
loader); each `ScriptAction` is grounded when reached (`ground()`) and handed to the shared `Executor` as a
one-action plan; the executor is handed no plan before the next one, so it owes no per-task completion tick; the
next primitive's first microaction runs on the tick after the last one's acknowledgement. `Stay(n)` stands n
ticks, `Stay()` to the end, an empty list stands. `current_task` stays `None`. The C2a compatibility path is
removed. The shared `Executor` is unchanged: its `_on_task_complete()` is no longer reached by the human. The
human's body reports 0 for the per-task tick to the projector (`observed_task_completion_latency`,
`HUMAN_TASK_COMPLETION_LATENCY` in `mesa_sim/sim_agents.py`); the robot's candidates keep its own. CONSEQUENCE,
measured: the human projection ends one tick earlier, so a decision may move before any human task completes
(s20 `single_task`: the hold at step 11 is 7 ticks, was 8); with the human's latency set back to 1 the run is
identical up to the first dropped tick. RULING (Hadi, T-C2b): the decision working, not a defect — the human's
projection without the per-task tick ends one tick earlier and the human arrives one tick earlier, so the hold
that clears it is one tick shorter. Holds moved in the fixtures (prior on): s20 `single_task` 8 -> 7, s70 (both
strategies) 1 -> none, s83 `full_reorder` a new hold of 2 at step 190. Nothing in `shared/` reads another
agent's `current_task` (checked by grep: `WorldState.agent_states` is read nowhere in `shared/`), so the
human's `current_task = None` reaches no decision. Fixture results: every human line identical up to the dropped per-task
tick in all ten runs (s00, s20, s70, s80, s83; `single_task`, `full_reorder`; prior on).

AS BUILT (T-C2c): SCENARIO-AUTHORING CONVENTION (Hadi, cchat, 23 September 2026). A human's script ends with the
human leaving the workspace (`MoveTo("door")` or a corner, then the empty list's stand), unless the scenario is
about the terminal stand at a table (TODO-80's blocked case, stated in the scenario's description). Reason: a human
standing at a table after its script deadlocks the robot with the stop on; that is the scenario's artefact, not a
design result, and a stay that ends is waited out (scenario_94). The 22 play scripts and the two C2c fixtures
(scenario_11, scenario_01) are not edited: they are examples and TODO-80 fixtures. New scenarios follow the
convention.
SUPERSEDED IN PART (Track 2.5, ruled by Hadi 28 Sept 2026): "New scenarios follow the convention" is extended to the
existing regression fixtures where their terminal stand is not part of the fixture's purpose (docs/assumptions.md
1.1); the six scripts behind the occupied-target logs (scenario_s01_01, s01_06, s02_01, s03_01, s04_01, s06_03) end
with `go_to("corner_SE")` since 52295f7. The play scripts and the C2c fixtures are unchanged.

T-C2, THE BUILD: C2a the script layer (primitives, `expand`, the vocabulary, landmarks, the provenance check);
C2b the human executor, action-level (both built). Fixtures s00, s20, s70, s80, s83, prior on; the check is identity up to
the dropped per-task completion tick; the baselines are regenerated once. Then two literal scenarios, an
interrupt and a stay, one run each, observed and not judged. From here debugging runs use prior on only; off /
on returns for the paper.

## T-H, the human behaviour model

**T-H: the human behaviour model** — RECORD [T-H/1], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
   Format (ccode's choice): one line per tick in a file of its own beside the run log,
   `[rec] step=<n> stack=<top>;<suspended> action=<action>#<occurrence> progress=<done>/<total>`, tasks by their task
   instance key, `stack=-` when empty; the sweep diffs it as it diffs the greps.

**T-H: the human behaviour model** — RECORD [T-H/2], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
10. NOT PART OF T-H.
    - IR is not redesigned. T-D resumes on this structure; T-D Q1 stays "what the robot infers and does when no
      hypothesis explains the evidence, inside `unknown` or outside it", now with ground-truth cases: a switch to a
      modelled task, a switch to a modelled task outside the support, a switch to an unmodelled task, a binding-level
      deviation, no task on the stack, an episode's first ticks.

**T-H: the human behaviour model** — RECORD [T-H/3], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
    - Alternative 1 (a human mind that generates events; a stack-aware IR): recorded as the next architecture
      direction, not scheduled (roadmap).
    - Nested interruptions beyond one level: the stack allows them; the restriction is lifted only when a scenario
      needs it (TODO-100).

11. ACCEPTANCE ACROSS T-H: after each build, the 40 maintained baseline logs are rerun; robot-side lines (`[IR]`,
    `[IR-dist]`, `[meta-*]`, decisions) must be byte-identical; human-side differences are listed and each explained. At
    the end of T-H3 the new logs replace the stored baselines.

THE BUILD, one session each, each under CLAUDE.md's BUILD DISCIPLINE (a plan step confirmed by Hadi, then the build):
- T-H1 the tree, the task model and the two knowledge objects (items 2, 3, 9), and the destination check's move; the
  migration of `domains/dock_loading/` and `ros_sim/` to the tree begins here (finished in T-H3). Its planning step
  shows methods referencing `ActionSchema` objects and the support restriction comparing `HypothesisKey` values.
- T-H2 the executor: `Event`, `Decision` (`Start`, `Drop`), `Trigger` (`AfterAction`, `DuringAction`, `Now`), `at`,
  `during`, `inject`, the stack, the mid-action cut and the resumption rule, the record and its stream, the test that
  `world_state_builder` exposes nothing of the stack (items 5 to 8). Its planning step shows how the cut and the resume
  sit in the shared `Executor` without touching the robot's paths.
- T-H3 the migration of the scenarios; deletion of the C1 vocabulary, `Deviation`, `Provenance`, `expand` /
  `resolve_script` as a separate form, the key-based checks, `Stay`, `MoveTo` / `PickUp` / `Place`; `dock_loading`
  and `ros_sim` migrated.
- T-H4 the record's queries, `unperformed` and coverage (item 7); supersedes TODO-92.

RECORDED AT WRITING (ccode, 25 September 2026), facts and points the ruling leaves to the build:
- (T-H1) In the code at 19e7b8b `check_task_destinations` already runs on `assigned_tasks` only, for both agents, and
  not on the human's `scheduled_tasks` (`mesa_sim/sim_model.py`, the T-B1a block). The move is to where the task model
  and the robot's plans are checked.
- (T-H1) `is_foreseeable` is read in the robot's mind at one place (`IntentionRecognizer._build_admissible_keys`);
  `DomainKnowledge.get_assigned_intentions()` and `get_foreseeable_intentions()` read the two booleans and have no
  caller. The per-domain `DomainModel.intentions` set is the nearest existing thing to the task model; today one
  `DomainKnowledge` serves the robot and the human's script resolver alike.

**T-H: the human behaviour model** — RECORD [T-H/4], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
- (T-H1, as built) The destination check runs where each robot's task model is built, on the robot's own assigned
  tasks and those of the agent it observes; a human no robot observes is no longer checked (no scenario has one).

**T-H: the human behaviour model** — RECORD [T-H/5], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
- (T-H3, as built) THE MIGRATION. Every registered scenario's human script is a `Script` (the list form is refused
  by `AgentConfig`); `domains/kitting/scenarios.py` is written wholly in the kitting call form (`deliver_item("item_3",
  table="kitting_table_0")`, `coffee_break(...)`, `ac_activation(...)`, `go_to(...)`, `stand(...)`, `go_to_and_stand(...)`),
  explicit typed functions in `domains/kitting/script.py`, each building a `TaskInstance` of its schema with the
  `Var`s read from the schema's parameters. They are kitting's (its schemas, its word `table=`): `world/` holds no use
  case; the generic sugar (`Script`, `.at`, `.during`, `drop`) stays in `shared/types.py`. `table=` is written wherever
  the old instance bound it (every kitting instance), so every task instance key, and every robot-side line, is
  unchanged. The translation, per old edit: `interrupt(t, after=x, with_=[Y])` → `t.at(x, Y)`; `abandon(t, after=x,
  then=[...])` → `t.at(x, drop)` then plain entries; `abandon(t, before=pick_up)` → `t.at(move_to, drop,
  occurrence=0)` (the action before the anchor; `deliver_default` has two walks); `deviate(t, destination=k)` → the
  instance with `table=k`; `MoveTo(landmark)` → `go_to(landmark)`; `Stay(n)` → `stand("PT<2n>S")` (n standing ticks at
  the body's 2 s per step).

**T-H: the human behaviour model** — RECORD [T-H/6], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
  CHECKED: the 40 maintained logs and tb3's 8 unstored `single_task` runs are byte-identical to the T-C2b baselines
  outside the `[human]` lines, the human's step lines included; the C1 `[human] primitive k:` lines are replaced by the
  record's transitions (`entered:`, `completed:`); the `.rec` streams are the first non-empty baselines.
- (T-H4) `assigned(task)` for a binding-level deviation of an assigned task (`deliver_item("item_1",
  table="kitting_table_2")` against the assigned `deliver_item(item_1)`): whether the query compares the whole instance
  or its enumerated bindings is part of the query's type, settled in T-H4.

**T-H: the human behaviour model** — RECORD [T-H/7], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
  THE COVERAGE LINE: `[coverage] <human> <robot> entry=<i> <task>=<value> start:<task>=<value>`, one per script entry
  for each robot observing the human, printed by `SimModel._log_coverage` in the run log after the `[run]` headers
  (read against the `[IR]` lines; the `.rec` unchanged). Information only; the same with the prior on and off. Every
  entry of the maintained fixtures is `covered`.

**T-H: the human behaviour model** — RECORD [T-H/8], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
  CHECKED: the 40 maintained logs and tb3's 8 unstored `single_task` runs are byte-identical to the T-H3 baselines
  outside the new `[coverage]` lines, and every `.rec` is byte-identical.

**T-H: the human behaviour model** — RECORD [T-H/9], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
  CHECKED: the 40 maintained logs are byte-identical to the T-H4 baselines outside the new `[scenario-coverage]`
  lines, and every `.rec` is byte-identical.

## T-L, layouts, setups and scenarios

**Layouts, setups and scenarios: the three artefacts of a run (T-L, 26 September 2026)** — RECORD [T-L/1], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
   - THE STATED TABLE (ruling b): the stated table stays explicit in a scenario's assigned tasks and script, validated
     against the setup's designations as today. A readability choice: the HTN model does not require it ("T-H: the
     human behaviour model", item 5; the T-B1a precedence rule). Consequence: a scenario fits a setup whose
     designations agree with its stated tables, and that is what the check says.

**Layouts, setups and scenarios: the three artefacts of a run (T-L, 26 September 2026)** — RECORD [T-L/2], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
4. NAMING: descriptive ids, nothing encoded. One id per artefact, snake_case, unique within the domain and artefact
   kind; the Python variable of a `ScenarioConfig` equals its id; the `name` field is dropped; `description` holds the
   purpose. The same rule for layout and setup ids.
   FORM AMENDED (Hadi, 26 September 2026; the principle stands — the variable equals the id, `name` dropped,
   `description` holds the purpose, nothing about the script's content in an id): serial ids.
   - Layout ids `env_layout_KK`; setup ids `env_setup_NN`; scenario ids `scenario_sNN_MM`, NN the scenario's setup
     serial and MM a counter per setup. KK, NN, MM are independent serials with no meaning beyond order of writing.
     Example: `env_layout_07`, `env_setup_04`, `scenario_s04_01` (today's env_layout7, env_setup7, scenario_70);
     scenario_71 becomes `scenario_s04_02`.
     NOTE (Hadi, 26 September 2026, the stage-3 task): the example's serials were illustrative. The built numbering is
     the rule's: stage 2 numbered env_setup7 as `env_setup_05`, so scenario_70 is `scenario_s05_01` and scenario_71
     `scenario_s05_02`; env_layout7 is `env_layout_07`. `docs/rename_table.md` holds every id.
   - The setup serial in a scenario id repeats the validated `setup` field. The code does not check that they agree
     (a check that reads an id out of an id string is string matching, which BUILD DISCIPLINE forbids); the agreement
     is an authoring convention stated in CLAUDE.md, and an author who moves a scenario to another setup renames it.
   - A layout's serial is never in a scenario id (a scenario has one or more reference layouts).
   - Stage 3 merges the identical setups (env_setup0 = env_setup3, env_setup2 = env_setup5) before numbering, so
     numbering is done once. SUPERSEDED (Hadi, 26 Sept 2026, the stage-2 task): the merge and the setup ids
     `env_setup_NN` are stage 2's, because the module division (one module per setup, `scenarios_sNN.py`) keys on
     the setup serial and a stage-3 rename would touch every module twice; scenario and layout ids stay old until
     stage 3.
   - Baseline file names: `<layout id>_<scenario id>_<run options>.log`, as ruling 6 states.

5. REGISTRATION BY DISCOVERY: a `ScenarioConfig` is registered at import of the domain package (a decorator or a module
   scan; ccode chooses in stage 2), with no side effect beyond adding to a dict; a duplicate id is an error. Layouts
   and setups are registered by their files. BUILT (stage 2): a module scan (`domains/discovery.py`) — a decorator
   can be forgotten on a new scenario, which recreates the omission this ruling closes; registration runs at import
   of `domains.<domain>.registry`, the one entry every reader uses (importing the bare domain package registers
   nothing). Scenarios stay hand-written literals; T-B1b's ruling (TODO-47 (a))
   reversed a generator that produced fixtures, not a mechanism that lists them. That distinction is recorded under
   TODO-47 (a).

6. BASELINES ARE KEYED BY THE RUN. File names carry the layout id and the scenario id plus the run options already
   present (prior, strategy); the setup is omitted from names because ruling 3 gives a scenario exactly one setup.
   THE TRIPLE LINE: the `[run_mesa]` start line, where the layout and scenario ids are printed today, prints all three
   ids; stage 1 adds the setup to it. The four maintained sets are regenerated under the new names in stage 3, `.rec`
   streams byte-identical, a new md5 section in each README. Frozen records are not touched; one file
   `docs/rename_table.md` maps every old layout and scenario id to its new id, and says in one line that the frozen
   analysis scripts stay frozen at their commit; each frozen README gets one superseding line pointing to it.

**Layouts, setups and scenarios: the three artefacts of a run (T-L, 26 September 2026)** — RECORD [T-L/3], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
8. SEQUENCING: T-L precedes T-D. kitting and dock_loading migrate together (this task and its stages may touch
   `domains/dock_loading/`; it must still import). dock_loading's two scenarios fail at load before T-L (TODO-104);
   TODO-104 stands and T-L must not worsen it. ros_sim stays parked: TODO-111, with TODO-108, records that its layout
   readers move to the same sources when it resumes. The stages after this record task, each its own ccode task, each
   ending in the acceptance check below:
   - stage 1: types (`ScenarioConfig` gains `setup` and `reference_layouts`, loses `name`), loader, resolver,
     validator; every registered layout split into a layout file and a setup file with the object ids unchanged and the
     dead spawn entries deleted (`env_layout99.json` stays an unregistered file); scenarios unchanged in content and
     id; the tests' helpers move with the registry shape; the setup id added to the `[run_mesa]` line; the docs pass
     on the lines the survey listed (roadmap, T-L, stage 1).
   - stage 2: the scenarios package (one module per theme) and registration by discovery; `list_scenarios` and the
     tests' helpers on the declared pairs. AMENDED (Hadi, 26 Sept 2026, the stage-2 task): one module per SETUP,
     `scenarios_sNN.py`, and the setups finished here — the merge and the final ids `env_setup_NN` — because the
     module division keys on the setup serial.
   - stage 3: the rename to the serial ids (ruling 4 as amended), the identical setups merged before numbering
     [DONE IN STAGE 2, with the setup ids],
     `docs/rename_table.md`, the four maintained sets regenerated under the new names, sweep scripts and READMEs.
     BUILT (26 September 2026): the layouts and scenarios of both domains under their serial ids, `docs/rename_table.md`,
     the four maintained sets regenerated as `<layout id>_<scenario id>_<run options>.log` (tb1a gained its own
     `sweep.sh`; tb3 keeps all 20 runs), differing from the stage-2 logs in the `[run_mesa]` line alone, every `.rec`
     byte-identical; one superseding line in each frozen analysis README pointing to the rename table.
   - stage 4: the run file and the override mechanism, with the viewer reading it.
     BUILT (26 September 2026): `--run <path>` (replacing `--experiment`, no alias) and `--override
     <path>=<value>` (repeatable) in `mesa_sim/run_mesa.py`; a path is `<artefact>.<id>.<fact>`, the same in the run
     file's flat `overrides:` block (path: value) and on the command line, read once at the input boundary into one of
     three typed classes (`mesa_sim/overrides.py`: `StartPositionOverride` for `scenario.<agent>.start_position`,
     `FixedPositionOverride` for `layout.<object>.position`, `HomeContainerOverride` for
     `setup.<object>.initial_container`, the file keys), every other path refused with the path named; the value typed
     by the fact (two numbers, an id); a command-line override replaces the file's for the same path. `SimModel`
     applies them to the artefacts as read, before `_init_objects` and `_spawn_agents` (the registered scenario is
     copied, never changed); an unknown agent or object, or a layout position for a setup's object, is an error naming
     the path; bounds, container existence, destinations and the replay are the existing checks. Each override is
     printed after the start line as `[run_mesa] override <path>=<value>`, sorted by path, in the `--override` form.
     The viewer's `Page` reads the run file it is started from on every reload and shows the triple and the overrides
     (`mesa_sim/viz/run_file_panel.py`); its form, limited to the three kinds, builds the run first, writes the file's
     block only if it loads (a path the command line gives is refused: its value, not the file's, is run) (round-trip through `ruamel.yaml`, comments kept, a new dependency) and reloads. A run with
     no overrides is byte-identical to stage 3, and the four maintained sweeps are unchanged. NOT COVERED, as built: a
     fixed object moved out of the space or onto another object is not checked (ruling 7: the checks of any run); a
     moved fixed object keeps its declared `zone`, which nothing in the run reads; a duplicate path in the yaml block
     is PyYAML's last-one-wins; the viewer prints no `[run_mesa]` line (as before), so an override applied in the
     viewer is not in its log; a viewer started on `configs/experiment.yaml` writes its overrides there, where every
     run that takes the default file (the sweeps included) picks them up.

ACCEPTANCE, at every stage: the four maintained sweeps (tb1a, tb1b, tb1c, tb3) are run from scratch and diffed against
the previous stage's logs, with no difference outside the lines the stage names (the triple line, the ids); AND pytest
is green. Nothing is aligned to older analyses.

**Layouts, setups and scenarios: the three artefacts of a run (T-L, 26 September 2026)** — RECORD [T-L/4], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
MEASURED AT RECORD TIME, CLOSED BY RULING a (read-only, the registered scenarios against their registered layouts'
fixed objects, a footprint being the object's `size` centred on its `position`): an object check would have refused
scenario_40, scenario_41 and scenario_42 (robot_0 at (-950, -550), the centre of the landmark `corner_SW`), and left
undecided the starts on the edge of `kitting_table_0` (scenario_40 to 42's human_0, scenario_70 to 73's robot_0).
Every registered start lies inside its space's bounds.

## T-D, robustness in kitting (R and E, the cognitive loop, the IRB, L, P, G, X, the MPB)

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

**The cognitive loop does not end with the task pool (IRB, ruled by Hadi, 27 September 2026)** — RECORD [T-D/4], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
Consequences recorded.
- After the terminal return the body calls neither `evaluate_triggers` nor the executor. The existing baselines stay
  byte-identical once every `[IR*]` line is removed, and their `[IR*]` lines stay byte-identical up to and including
  the declared completion tick; the new lines begin the tick after it and include `[IR-complete]` and `[IR-boundary]`
  as well as `[IR]` and `[IR-dist]`. (Refined in IRB.2b records, Hadi on the IRB.1r report, 27 September 2026.)
- Within a tick, the robot's `[IR]` and `[IR-dist]` lines now precede its `[meta-trig]` line, on every tick (observation,
  recognition and their logging come before the guard, the guard before the trigger evaluation); before IRB.2b the
  `[meta-trig]` line came first. Every log's md5 changes with it, a run whose robot never finishes included; the
  comparison above is unaffected. (IRB.2b plan, confirmed by Hadi.)
- The 1.4 and 1.5b measurements (`analysis/td_stage1/`, `analysis/td_stage1b/`) were taken over the truncated
  interval. They are rerun over the newly exposed interval in IRB.2b, with every change reported and no previous
  statistic preserved for comparability (TODO-121).
- With an empty pool, tick 0 still produces one `no_current_task`, one `[meta-proj]` line and one "all tasks complete"
  line.
- TODO-33 (the run loop does not stop when all agents are finished) is untouched: the run's length is the run file's
  steps.

**The intention-recognition test-bed (IRB, ruled by Hadi, 27 September 2026)** — RECORD [T-D/5], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
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
proximity threshold, the action and task latencies). IRB.3b asserts per-tick equality of that trajectory with the run's
human lines; if the assertion fails, the generator reads the run's human lines instead and the report says so.
Independence boundary. The generator implements the belief from all recognizer records at HEAD, not from one entry:
this file's "T-D R and E" (e as the straight-line excess from the origin, s, s_exp by E9's attribution, D, L clipped
at 1, S, membership as amended twice with the boundary-tick rule, the finding) and `docs/recognizer_handback.md`
§§1.2 to 1.7 (the uniform prior, the proximity regress, the fold and prefix accumulation, the normalisation over H,
the completion signal, the pin, the boundary and the retirement, `BELIEF_FLOOR`, target resolution for a carried
item). The IRB.3b report lists each rule the generator implements with its source. It imports nothing from
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

Sessions (the IRB track; the IRB first, cycle 2 (L) second): IRB.1r records these rulings and the cognitive-loop
ruling (records only); IRB.2b builds the cognitive-loop correction ("The cognitive loop does not end with the task
pool", above), which the test-bed's runs need; IRB.3b builds the artefacts and the expectation generator, runs the
scenarios and writes the report.

CORRECTED IN PLACE (IRB.2b records; Hadi on the IRB.1r report, 27 September 2026): the landmarks (corner_SE only, no
door; IRB.1r had them required), the ids (serial; IRB.1r had descriptive ids), the generator's source (all recognizer
records at HEAD; IRB.1r had the one entry), the trajectory (the replay expanded per tick with the body's walker, and the
fallback to the run's human lines), and the third stated consequence (`coffee_break` is retired once `waited` holds, so
TODO-117's case arises in the two-deliveries scenario only; IRB.1r had it in every scenario).

Files: domains/kitting/ (the layout, setup and scenarios, hand-written literals registered by discovery), the run files
where T-L keeps them, analysis/irb/ (the generator, the log reader reusing `analysis/td_stage1b/tdlib.py`,
expected.csv, actual.csv and diff.md per scenario, REPORT.md). Built in IRB.2b and IRB.3b.
Reference: cchat, 27 September 2026 (IRB); "T-D R and E" (R1 to R6, E1 to E10, G1, the membership rule as amended
twice); "Layouts, setups and scenarios: the three artefacts of a run"; "T-H: the human behaviour model";
`docs/handoff_T-D_cycle2_and_IRB.md` §8 (the layered plan); TODO-101, TODO-117, TODO-122;
`docs/recognizer_handback.md` §1.10

TRACK COMPLETE (IRB close-out, 27 September 2026): IRB.2b, IRB.3b and IRB.4b are built; sixteen scenarios (scenario_s08_01
to _04 on env_layout_10, scenario_s09_01 to _12 on env_layout_11), zero disagreements at 1e-9 between the recognizer's
public outputs and the independent oracle; the instrument is independent of the layout, and its record is
`analysis/irb/README.md` (the results in `REPORT.md`). Two facts for cycle 2, stated without ruling: (1) E8's
member clause is covered by E6's second amendment whenever the action completion latency is 1 (every phase an advance
opens then has s_exp ≥ 1, so its entry tick is already a member; removing the clause changed no output in IRB.3b); (2) at
the current β (0.01 /cm) and v (20 cm/tick), two targets 10.4° apart as seen from the start are not separated by a
28-tick walk (the rival's S 0.765 at the arrival), while 30.4° separates them three ticks before the arrival (S < α at
tick 25 of 28; scenario_s09_10, shallow runs of IRB.4b).

---

**T-D L: the belief lifecycle (ruled by Hadi, 27 September 2026)** — RECORD [T-D/6], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
Staging for L-build. The recognizer (L1, L4) and the meta-planner (L2 ii) are built; the IRB's oracle is
updated by derivation from this entry (not fitted to the runs); the sixteen test-bed scenarios (scenario_s08_01 to _04,
scenario_s09_01 to _12) are recompared; the four maintained baseline sets are regenerated; the 1.5c and IRB.2b measures
are rerun; every moved number is reported.

BUILT (L-build, 28 September 2026): c4beb1d (records), 2c54c4a (L1, L4, the flag: `ProceduralKnowledge.
terminal_actions`, `AdaptivePlanner.enabled_groundings` / `completed_groundings`, `_observed_terminal_completion`,
`_retired`), 493c095 (L2 (ii), L5 B: `RecognitionChange`, `TriggerDecision.cause`), 5129d90 and 3d65ca6 (the re-entry
kept in hypothesis order, the tie-break; found by the IRB), 013cd35 (tests). Verified: `analysis/l_build/
REPORT.md` and `analysis/irb/REPORT.md`, "L-build" (the sixteen agree with the derived generator at 1e-9). Two
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
tests/test_p_build.py, and four tests re-derived by P), 15cb99f (IRB.2b's mid-run pool test moved to scenario_s03_06),
fa26176 (the four maintained sets, a "P-build" section each). Verified on the P-build baselines: `.rec` streams
byte-identical in all 48; the recognizer's lines byte-identical prior on; the first difference of every changed run at
tick 0, a decision under the fallback; the IRB's sixteen logs differ in the step-0 `[meta-proj]` line alone
(no oracle rerun: the recognizer is untouched and the robot is idle there). Measured, not examined: scenario_s06_01
`single_task` prior off does not finish in 340 steps, with no wait (TODO-133). P is closed; next is G.
SUPERSEDED: P was reopened by P4 and closed with it (BUILT (P4-build), below).

BUILT (P4-build, 28 September 2026): 57600e2 (records: P4, Q6, the superseding notes), 179a503 (the build: the
perception facts on `RobotAgent`, `Projector.project_fallback()` from the evidence, the record's second value and
`projection_expired`; the refusal, the wait, the body's wait branch, the executor's wait handling and the
`HumanProjection` types removed), f0ead6e (tests; tests/test_p_build.py re-derived, the three "refusal returns None"
tests back to None, the WorldState field set), d7c98b5 (the four maintained sets, a "P4-build" section each;
TODO-133 closed). Verified: `.rec` streams byte-identical in all 48; the recognizer's lines prior on byte-identical to
L-build's; the IRB's sixteen logs differ in the step-0 `[meta-proj]` line alone; the suite 170 passed.
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
scenario_s09_06, scenario_s05_01 prior on, one control scenario); the IRB's oracle extended by derivation from
this entry for the warrant output; the four maintained sets as md5 regression plus one completion table.

BUILT (G-build, 29 September 2026): 81a9f86 (the build: `ObservationWarrant` and `BeliefState.observation_warrant`;
the recognizer's `_entered_by_completion` and `_observation_warrant`; the meta-planner's `WarrantSource`,
`GateOutcome.LEADER_UNWARRANTED`, `observed_assigned_tasks` and `_warrant`, `_clears_gate` still the one home; the `[IR]`
line's `warrant=[...]` and `[meta-proj] projection=built warrant=...`; TODO-123's docstring), 0555af7 (tests:
tests/test_g_build.py, 21; three expectations of tests/test_td15_build.py re-derived from AD1, CLEARS to
LEADER_UNWARRANTED, the fixture being prior off), cbe3f00 (the IRB's oracle extended by derivation: the warrant
per hypothesis and the gate's outcome per tick), 5afa7f9 (the four maintained sets, a "G-build" section each).

**T-D G: admission (ruled by Hadi, 29 September 2026)** — RECORD [T-D/15], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
Verified. The suite 191 passed. The IRB: 0 disagreements in all seventeen scenarios (scenario_s08_01 to _04,
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
IRB (track 1) tested the recognizer with an idle robot; this instrument tests the decisions the
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
  IRB does (task and hypothesis definitions, not cost, realization or selection logic).
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
  leader's confidence, which moved scenario_s10_08's crossing from the IRB's 46 to 47. A spatial or structural
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
  and every declared part-4 property holds (prior off: MPB-6). Outputs as in the IRB: the expectation written
  before the run, the in-process and the log-derived actuals, the comparison with a classified diff.md, a figure, a
  summary, a REPORT with numbers and md5s.
  The oracle's own check: the single-rule alteration test of the IRB (one rule of the derivation altered in a
  scratch copy; the comparison must detect it). The derivations new to the MPB oracle are the expiry cadence and the
  projection identity; on the gate with warrant, derived by the IRB since G-build (its rule 23), only the
  alteration test is new. An undetected alteration is recorded as a property of the test set with its reason, as the
  IRB did (E8's member clause), unless it is an oracle defect.
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
  ended and the robot's pool is empty) plus the idle margin the IRB derives from E5 (30 ticks, covering E5's
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
E8); "The intention-recognition test-bed (IRB)" and its close-out; `analysis/irb/README.md` (rule 23, the run length) and `REPORT.md`
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
  entered at 47 (commitment and observation; the IRB's 46 moved by this setup's output floor); no retraction.
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
recognition (the IRB); track 2, semantics (T-D R, E, L, P, G, X); track 3, reachability (this test-bed); track
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

## T-G, the second domain: rulings outside the shared core (A1, A10, A11; part B; part C)

**T-G: the second domain's rulings (ruled by Hadi, 30 September and 1 October 2026)** — RECORD [T-G/1], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
- A1, V1 and FW.
  V1 is the first complete version of the framework, the package for TeamRob and the publications. In V1: T-G; T-F; T-V
  track 1 and track 2; the T-D tail's track 3b (TODO-145); track 4 in the reduced form of A8. FW (future work: not
  designed, ruled or built within V1): the 4D detour; T-S; the directions of A10.
  AMENDED (Hadi, 3 October 2026): T-K is in V1, T-K part 1 (crisp context knowledge) and T-K part 2 (degrees); T-K's
  later directions (the stream of context values with the world's dynamics, TODO-158 to TODO-161, TODO-163, TODO-164)
  are FW.
  Reason: whatever was agreed for V1 about knowledge stays in V1. This ruling was made before T-K existed as a task, so
  its restatements were incomplete.
  AMENDED (Hadi, 6 October 2026, for T-viz; preferred, in T-viz's status words; design_records.md, "T-viz, the web-ui",
  HADI'S ANSWERS): T-V is carried out as T-viz. "T-V track 1 and track 2" in V1 reads "T-viz stages 0 and 1" (track 1 is
  T-viz stage 1); track 2 is T-viz stage 3, which with stage 2 is FW for now, the default until Hadi draws the V1
  border inside the web-ui. ccode's note: the Tags paragraph below reserves [FW] for conceptual, higher-level directions;
  the web-ui's stages 2 and 3 and TODO-173 are tagged [FW] by Hadi's answer all the same.
  Tags. Each open TODO may carry a tag beside its status: [V1] or [FW]. A TODO keeps its number and identifier for good:
  no renumbering, no renaming. An untagged TODO is not yet ruled. There is no full pass now: a TODO gets its tag when it
  is next touched, by Hadi's ruling; a new item gets its tag when recorded.
  [FW] is for conceptual, higher-level directions only. An alternative not taken in a design question is recorded inside
  that question's ruling as "not taken", with its reason, and gets no FW item. FW must not hide a known wrong behaviour
  inside what V1 claims: such an item is fixed in V1 or stated as a limitation.

**T-G: the second domain's rulings (ruled by Hadi, 30 September and 1 October 2026)** — RECORD [T-G/2], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
- A10, FW directions (conceptual; each a TODO tagged [FW], or a tag on an existing item):
  - shared work between the human and the robot: TODO-147;
  - a human that chooses its own tasks (a human planner in place of the author's priority list): TODO-148;
  - the robot modelling a human who waits for the robot's own action (Q3's alternative M3): TODO-149;
  - several observed humans (`docs/assumptions.md` 5.2 allows one): TODO-150;
  - a container divided into positions, the position chosen when an object is put down: the [FW] tag on LIMIT-04, no new
    item;
  - communication acts stay under the existing records (T-D X5, TODO-96): the human assigning or changing a delivery
    location during the run; the robot informing a third party;
  - under T-V track 2 (roadmap, T-V): an interruption of a busy human caused by a world fact, if wanted, is designed there
    as the same entry point as the live user's click.

- A11, a note for T-F (TODO-144): a layout authored so that routes cross shows that the robot adapts when an interaction
  exists; it does not show how often interactions occur. T-F varies the placement and takes no interaction rate from
  crossing setups alone.

**T-G: the second domain's rulings (ruled by Hadi, 30 September and 1 October 2026)** — RECORD [T-G/3], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
PART B. DOCK_LOADING RULINGS (the domain only; nothing here enters `shared/` or `world/`)

- B1, the domain's reading. The robot replaces the driver: an automated forklift whose assigned tasks are to deliver full
  pallets from the truck to their containers and to return empty pallets to the truck. The truck stays parked for the
  whole run and is a container. The observed human is the warehouse staff member who receives the delivery. The human's
  assigned scans follow from the robot's assigned deliveries and are known at load.
  It corrects the roadmap's T-G entry and `docs/handoffs/handoff_T-G_onward.md` (§4, §5): "a driver unloading pallets"
  and "the driver's work order" are wrong under this reading; the foreseeable candidates recorded there (the phone call,
  talking to the dock worker) belong to the driver's role, which the robot holds, and do not apply to the observed human;
  "work order" was superseded by "assigned tasks" at T-H.
- B2, Q1 in dock_loading: `confirm_delivered_pallet` states its condition in the task model: the pallet is in its
  delivery container. (It answers LIMIT-02, TODO-10 and DESIGN-04 with A3.)
- B3, Q4 (D1): "In V1, each object's destination is explicitly designated in the setup. The resolved fact is
  destination_of(object, target), which the mind reads." The form of "An item's destination table is a fact of the
  station" (T-B1a, amended by T-L). Not taken: a setup rule from an object's property to a target (an authoring
  convenience, no component reasons with it); a destination decided at run time by the human.
- B4, Q5 (E2): "A pallet has one type, pallet, and its full/empty condition is represented by the state fact
  is_empty(pallet). Methods use that fact to determine which tasks are executable. In V1 the state remains constant
  during a run; actions that change it are future work." Not taken: two object types; one task for both movements.
- B5, Q6: the gate and the office door each have the state open or closed, declared in the setup. No action closes them
  in V1.
  - The gate, opened on request: the robot moves to the closed gate and honks; the honk is an action of the robot that
    sets the fact "opening requested". The human has the assigned task "open the gate", applicable when the gate is
    closed and the opening is requested: walk to the gate's button, press it. The button is a fixed object on the wall
    beside the gate, away from the passage. The robot's deliveries require the open gate; until then the robot has no
    applicable task and stands. The human is not interrupted and takes the task the next time it is free. Because the
    task is assigned, the robot knows it through the prior, and it is a live hypothesis after the honk. No information
    is exchanged. No deadline.
  - The office door: the agent that passes it opens it; the affected task has one method for the open state and one that
    opens first.
  This supersedes TODO-08 for the gate and answers LIMIT-03 (with them TODO-02, BUG-04 and DESIGN-15's point 2). Not
  taken: neither a state; constant states without an action; the robot opening the gate itself.
- B6, Q7 (F2): two foreseeable tasks, `coffee_break` and `office_break`. `office_break` ends at its chair with a wait,
  and the chair stands inside the office. Until track 4 is built the office is observed. (It answers DESIGN-15's point
  3.) Not taken: a third foreseeable task of the same structure (standing with a colleague); a variant in which the human
  scans all pallets only after every delivery; recognizing which variant of a task a human follows.
  ADDED (Hadi, 1 October 2026; T-G records 8): `office_break` lasts 90 seconds; `coffee_break` stays 60 (TODO-157,
  closed as ruled; the value is changed in the next build step). Reason: a long absence lets pallets accumulate in a bay,
  which gives two scans possible at once and the robot arriving at an occupied bay; it differs clearly from the coffee
  break. "T-G: the second domain's rulings", T-G Q16's block (RULED, T-G records 8).
  CORRECTED (records, 2 October 2026; T-G records 9): one tick is 2 seconds (PT60S is 30 ticks), so office_break's wait is
  45 ticks, and the human's absence is about 110 ticks (in the IRB's C6 on env_layout_02, from leaving the dry
  bay at 30 to the arrival at the frozen bay at 141), a little more than one round trip of the robot (about 96 ticks,
  B14's note). Whether the absence is long enough for pallets to accumulate in a bay is reviewed with the MPB's design.
  REVIEWED (Hadi, 2 October 2026; T-G records 10; THE MPB ON DOCK_LOADING, MPB-DL5): office_break stays at 90 seconds
  for the MPB. Reason: no value is changed for a test set.
- B7, Q8 (H2'): `store_pallet(?pallet)`, a work task of the human: it takes a delivered and scanned pallet from its
  delivery container to its onward container. Condition: the pallet is in its delivery container and is scanned, so the
  order per pallet is delivered, scanned, stored. Each full pallet has a second designation in the setup, its onward
  container. The human carries a pallet as the kitting human carries an item; no tool in V1. The human is never assigned
  `deliver_pallet` or `load_return` in V1. Not taken: the human delivering its own pallets from the truck (kitting's
  pattern).
- B8, Q8b (K1): kitting's rule for a held object, unchanged. Hadi's wording: "When an agent starts a new task while
  carrying an object, the carried object determines the applicable method. Continue with it if it is the new task's
  object; otherwise return it to its recorded origin before starting the new task." It applies to `deliver_pallet`,
  `load_return` and `store_pallet`. The origin is where the pallet was picked up: the truck, the empties area, the
  delivery container.
- B9, Q9a (S2): a container is one point, the centre of the container, with no constraint, and it may hold several
  pallets (as kitting's table does). Not taken: authored pallet places; a position chosen when the pallet is put down
  (FW on LIMIT-04, A10). Pallets drawn on top of each other are a drawing matter for T-V.
  NOTE (records, 2 October 2026; T-G records 9; the IRB on dock_loading), a property of "one point per
  container", not a ruling: two pallets in one container stand on one point, so the second scan has no walk (its
  move_to is acknowledged at once: C3, three stretches of 3 ticks that never reach the threshold), and no walk between
  the two exists that an event could cut (the set's M3 as written was not buildable; Hadi approved scan 2 in its
  place). LIMIT-04's FW direction (a position chosen when a pallet is put down) is the alternative.
- B10, Q9b, the room. Requirements (Hadi): goods flow forward (truck, delivery container, store) and never travel away
  from their store and back; the freezer lies near the dock; no bay stands in front of a store entrance; one place for
  empties that both stores can bring to. Arrangement: the delivery bays in a row on one side wall, the frozen bay nearest
  the gate; the freezer and the dry store on the opposite wall, the freezer nearest the gate; the empties in the top
  corner on the bay side; the office at the top centre. The coffee machine, the gate's button, the desk, the standby
  place and the landmarks are placed when the layout is drawn.
  Artefact constraint: by the setup's designations, the human's carrying route crosses or approaches a normal robot route
  in some setups and stays clear in others; the V1 scenarios include both.
  Catch-up requirements: every fixed object inside the space; the zones leave the layout and areas are declared (A9);
  landmarks for the exit walk; the revised room is a new layout and a new setup with the next serial ids; the present ones
  (env_layout_01, env_setup_01) stay for the viewing fixture.
  READS (B13, T-G records 2, 1 October 2026): "landmarks for the exit walk" reads: the desk landmark, which enters stage
  1's layout.
  MOVED TO STAGE 2 (Hadi and the design chat, 1 October 2026; recorded in T-G records 5); B14: the arrangement above (the freezer and the dry store on the opposite wall) is stage
  2's room, with its own layout, setup and scenarios; it is unchanged and can be revised when stage 2's layout is agreed.
  Reason: that arrangement serves `store_pallet`, which stage 1 does not have. Stage 1 uses the three rooms of B14.
  "The present ones (env_layout_01, env_setup_01) stay for the viewing fixture" is superseded: they are removed with
  their three scenarios, and the viewing fixtures of B14 replace build 1's. The other catch-up requirements hold for
  B14's rooms (every fixed object inside the space; the areas declared; the desk landmark).
- B11, Q11 (P2) in dock_loading: passing the gate is a plain step "move to the gate", whose target is the gate's centre
  point; no special action. The domain has three areas, divided by the gate and by the office door: the truck side (the
  truck and the dock platform, outside the gate), the hall, and the office (A9; names settled with stage 1's layout; the
  six zones of env_layout_01 are replaced). Each task has one method per starting area, selected by the condition on the agent's area. A
  method that crosses the gate keeps the condition that the gate is open. "Return the held pallet to its origin" may be a
  sub-task used as the first step. Not taken: always going by the gate; a sub-task with conditions for a later passage
  (A9's property defeats it); routing through openings as a property of movement (it changes the projection and the
  recognizer in `shared/`). Within V1 this is dock_loading's answer to TODO-09.
  AMENDED (Hadi, 1 October 2026, T-G stage 1's plan approved, answer 6; recorded in T-G records 7): "Each task has one
  method per starting area" reads: a task has a method for every area its agent can be in, not for every area. The
  robot can be on the truck side and in the hall; the human in the hall and in the office. With B8's four held-object
  cases (held, another empty pallet held, another full pallet held, nothing held) a robot task has 8 methods. An agent
  in another area is a defect: no method covers it, the absence of a method is the check, and no mechanism is added
  (for the robot the run stops, TODO-152). B11's optional sub-task for the return is not used: a sub-task schema must be
  in the robot's task model, and the hypothesis space is built from every schema there, so it would become a hypothesis
  about the human. The methods: `docs/handoffs/plan_T-G_stage1.md`, section 4.
- B12, further rulings on the domain's scope.
  - Check-in and check-out [V1], stage 3: separate from the gate mechanism and independent of it. A desk with a computer
    beside the gate's button is the human's place; the robot's place is a point just inside the gate, more than the
    minimum separation away. Check-in: the two agents exchange the list of deliveries at the start. Check-out: the human
    signs at the end to confirm that everything is delivered. Design open until stage 3, including what "exchanging the
    list" means when the robot holds the designations from the start.
    AMENDED (B13, T-G records 2, 1 October 2026): the desk enters stage 1's layout, as the target of the closing part;
    check-in and check-out stay in stage 3 and will use this desk.

**T-G: the second domain's rulings (ruled by Hadi, 30 September and 1 October 2026)** — RECORD [T-G/4], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
  - A deadline on the robot's waiting: the default is that the robot waits without limit. Optional in stage 3; not
    planned.
  - A pallet that blocks another in the truck: an optional sub-task in stage 3, if time in V1 allows.
  - Not taken: an action of unknown length inside a plan; a fixed order among the robot's tasks as its own mechanism
    (conditions cover it; deliveries and returns may be intertwined); the robot moving to wherever the human is (the
    target would be an agent, arrival contradicts `min_separation`, the prediction becomes circular); a check-in that is
    a meeting with no content.
- B13, the closing part in dock_loading (the domain side of T-G Q14; Hadi, 1 October 2026; recorded in T-G records 2).
  Stage 1's closing part is one entry: go to the desk. The desk is a landmark inside the hall, at the wall on the gate's
  side, beside the place of the gate's button. It enters stage 1's layout.
  The desk lies more than the minimum separation from the robot's routes through the gate. Reason: the robot still passes
  the gate after the human's list is finished, and the human then stands at the desk.
  No exit from the room is defined for dock_loading now. Check-in and check-out stay in stage 3 and will use this desk
  (B12).
  `docs/assumptions.md` 1.1 (a script ends with the human leaving the workspace) reads for dock_loading: the script ends
  with the walk to the desk. B10's "landmarks for the exit walk" reads: the desk landmark. Kitting is unchanged. T-F's
  scope line on the exit walk (TODO-144) is a kitting statement; dock_loading's ending is for T-F's own design.
  NOTE (T-G records 3, 1 October 2026; not a ruling): the desk is a landmark in stage 1, so no task of the robot's task
  model names it and the robot's mind holds no hypothesis for the walk to the desk, as for kitting's exit walk. Whether
  the desk becomes a fixed object is stage 3's question.
- B14, stage 1's rooms and setups (Hadi and the design chat, 1 October 2026; recorded in T-G records 5).
  Rooms. Stage 1 uses three rooms, env_layout_02, env_layout_03 and env_layout_04, derived from the present room. The old
  env_layout_01, env_setup_01 and the three scenarios on it are removed; the viewing fixture of build 1 is replaced by the
  fixtures written with these rooms. The room of B10 (the freezer and the dry store on the opposite wall) moves to stage 2
  (B10's note). More rooms and setups may be added in stage 1 later.
  Identical in the three rooms (centres in cm; origin and axes as before): the hall, x from -600 to 600, y from -300 to
  300; the office, x from -170 to 170, y from 300 to 415; the office door (0, 300); the chair (130, 365), inside the
  office; the gate (0, -300), width 300; the truck (0, -590), 250 by 300; the dock platform as before; the desk, a
  landmark, (300, -260); the standby place, a landmark, (0, 0); the delivery bays and the empties container 170 by 170;
  the coffee machine 50 by 50. The declared space contains every fixed object, the truck included.
  Differing:
  - env_layout_02: dry delivery bay (-515, 215); frozen delivery bay (515, 215); empties (-515, -35); coffee machine
    (505, 30).
  - env_layout_03: dry delivery bay (-515, 215); frozen delivery bay (515, 0); empties (-515, -35); coffee machine
    (-400, -230).
  - env_layout_04: dry delivery bay (-255, 215); frozen delivery bay (-515, -35); empties (515, -35); coffee machine
    (-400, -230).
  One container for empty pallets per room. The three areas (truck side, hall, office) are declared in each layout,
  written under the name the code has today (zones); stage 1's rename step converts them.
  Agents. The human starts at the standby place. IRB: the robot stands idle on the gate's centre point (0, -300)
  for the whole run. MPB: the robot starts on the truck side. Stage 1 keeps full observation: the robot observes every
  area, the office included, wherever it stands. A8's rule on monitored areas is reopened at stage 2 (A8's note).
  Setups, two kinds per room (six files):
  - Kind 1, for the IRB: two full unscanned pallets in the dry delivery bay and two in the frozen delivery bay,
    each designated to the bay it stands in; one full pallet in the truck, designated to the dry delivery bay; no empty
    pallets. Reason: one setup serves three cases by the scans a scenario assigns (one scan per bay; two scans in one
    bay, the same-motion case; the scan of the pallet in the truck, which never becomes applicable, so the human goes to
    the standby place).
  - Kind 2, for the MPB: four full pallets in the truck, two designated to each delivery bay; two empty pallets in the
    empties container. Reason: the robot's pool always holds a delivery to the other bay and a return.
  - RULED: the setup designates the truck as the destination of each empty pallet (the PROPOSAL of that name). Reason:
    one rule covers every pallet.
  - A third kind, all four full pallets designated to one bay, is added after the first MPB run if its results call for
    it.
    KEPT (Hadi, 2 October 2026; T-G records 10; THE MPB ON DOCK_LOADING, MPB-DL2): the condition stands. A new kind for
    the MPB's controlled scenarios is ruled there (one full pallet already in each delivery bay); the names of the kinds
    are not ruled.
    READS (Hadi, 2 October 2026; T-G records 11; THE MPB ON DOCK_LOADING, DISPOSITIONS, D7): "a third kind" reads "kind 4"
    ("one bay"). Kind 3, "pallets in the bays", is MPB-DL2's (two full pallets in each delivery bay, as amended).
  Staging: a milestone in stage 1's build, before the IRB: one simple scenario per room runs from start to end.
  Stage 1's "before the plan" points on the layout and the setup (C1's "before each stage's plan the design chat and
  Hadi agree the layout and the setup") are closed by this entry for stage 1.
  ANSWERS (Hadi, 1 October 2026, on the B14 build's flags; recorded in T-G records 6):
  - The six setups stay as written, though pairwise identical in content across the rooms. Merging identical setups
    belongs to the held refactor of scenarios and layouts, not to this stage.
  - Accepted as built (cec8cc3): the MPB robot's start point (0, -370), on the dock platform; the ids
    `empty_pallet_bay_0`, `desk`, `standby_place`; the area names `zone_hall`, `zone_office`, `zone_truck_side`.
  - A pallet's `subtype` stays out of the setups. Reason: destinations are by designation.
  - The pictures of the old room are kept, renamed with the suffix `_original` (C3's note).
  NOTES (the same answers; facts, not rulings):
  - An agent stops 10 to 30 cm before a target point (a walk steps 20 cm toward the centre and completes once
    `at(agent, object)` holds); the proximity threshold is 30 cm (`PROXIMITY_THRESHOLD`).
  - The scan and the next delivery to the same bay share one point (the bay's centre, B9), so with a minimum separation
    of 50 cm that conflict is certain whenever both concern the same bay. This is the expected main interaction of stage
    1, not a defect.
    CORRECTED (records, 1 October 2026; STAGE 1, THE SECOND MILESTONE SCENARIO BUILT): the conflict requires, in
    addition, that the human is still at the bay when the robot arrives. In stage 1's rooms a round trip to the truck
    takes about 96 ticks and a scan from the standby place 16 to 30, so the human finishes before the next pallet
    arrives, and the second milestone scenario did not reach it.

PART C. STAGING AND THE DOMAIN'S PRESENT STATE (statements, not design rulings)

- C1, the stages of T-G (all in V1). Before each stage's plan the design chat and Hadi agree the layout and the setup for
  that stage.
  - Stage 1, the basic domain: the robot delivers and returns (B11); the human scans, takes the two breaks, steps aside to
    the standby place; the gate is declared open; the office door has no state yet. The IRB, then the MPB.
  - Stage 2: `store_pallet` (B7); the gate opened on request (B5); the office door's state (B5); after the MPB's first
    run, TODO-16 with the stepwise delivery (A7).
  - After stage 2: track 4 (A8).
  - Stage 3: check-in and check-out (B12), with the two optional items.
  T-K PART 1 (Hadi, 1 October 2026; T-G records 2): context knowledge is framework-wide, so it is not a stage of T-G but
  T-K; T-K part 1 runs after T-G's stage 1 and before its stage 2. T-G's order is stage 1, stage 2, track 4, stage 3;
  T-G is paused between stage 1 and stage 2 while T-K part 1 runs. T-K part 1 starts from its own handoff.
  Its content (its design opens in T-K part 1; nothing is ruled yet): a context timeline in the scenario that changes a
  fact at an authored point of a run, applied by the environment; both domains' foreseeable tasks conditioned on such
  facts. Open questions recorded for it:
  - the form of a context fact;
  - whether the human only starts a task on it or a task in progress is interrupted (A3's "never interrupted" and A10's
    line on an interruption caused by a fact);
  - liveness under A4 when a condition turns false while the human still executes the task ("applicable to start"
    against "valid to continue");
  - the prior under context;
  - the perception assumption for context facts.
  The pre-loaded context stream moves from T-V track 2 to T-K part 1. T-V track 2 keeps the live events.
  ADDED (Hadi, 1 October 2026; T-G records 8; T-G Q16's block below, RULED), NOT RULED: one design question for T-K part
  1, what sets a hypothesis's share at the start of an episode. Four determinants are recorded for it: the assignment
  (exists); context facts; the task that just ended (a transition prior between tasks, Hadi's idea); an enabling event,
  such as the robot's own delivery (TODO-154). They are designed as one mechanism. Also Hadi's ideas for T-K part 1, NOT
  RULED: the duration of a foreseeable task is not one fixed number; temporal context can be a fuzzy set with a degree
  of membership.
  RULED (Hadi, 2 October 2026; design_decisions.md, "T-K: context knowledge in the recognizer's belief";
  the record in "T-K" below): the open questions above are answered there, except as stated. The form of a
  context fact: R5 (a degree in [0, 1]; T-K part 1 crisp only). Start or interruption: neither; context drives no task
  of the human (R1). The prior under context, and the share at the start of an episode: R2 to R4 (the assignment and
  context facts; the task that just ended is open, an item of T-K part 2 after T-G's stage 2, R4; an enabling event's preference not taken, R4). The
  duration: one declared duration (R6; its uncertainty is FW). The perception assumption: open (open item 2). Liveness
  when a condition turns false during execution ("applicable to start" against "valid to continue"): not answered by
  the rulings; R1 keeps the conditions of tasks in the task model and A4 as built stands.
  A requirement on stage 1's plan (the same ruling): the form built for A5 admits a fact that no action changes and that
  is not the state of a movable object. Reason: context knowledge then needs no second mechanism. Stage 1 authors no such
  fact.
  WHERE EACH RULING IS FIRST BUILT (Hadi, 1 October 2026, T-G records 1, continued). Content only; the order inside a
  stage is for that stage's plan.
  - Stage 1, the basic domain:
    - first, in its own commit with no change of behaviour: the zone mechanism renamed to "area" in the code (A2's
      ruling of 1 October 2026; the plan reports the extent first). This is the one rename in V1; A2's "no code is
      renamed" concerns the terms it introduces;
    - the catch-up of dock_loading's forms to kitting's (C3);
    - A3, the human's script form (`world/`), with the standby entry, once the entry lifecycle is ruled (A3, PARKED);
      RULED (1 October 2026): the lifecycle is A3's Q12 to Q15, with the closing part; dock_loading's closing part, the
      walk to the desk, and the desk landmark (B13);
    - A4, liveness by applicability (`shared/`);
    - A5, generic object states and designations, used here for the scanned state, `is_empty` and the destination;
    - A6, the perception assumption;
    - A9, the declared areas and the fact that an agent is in an area (the mechanism exists under the code name "zone":
      renamed by the first step, not built anew; dock_loading's three areas declared in stage 1's layout);
    - B1 to B4, B8, B9, B11;
    - B6, with `office_break` in a reduced form: the office door has no state yet, and the human passes it as a plain
      point on the way; the office is observed;
    - B10, the room; whether the stores and the freezer are already present in stage 1's layout is not ruled
      (PROPOSALS);
      SUPERSEDED (Hadi and the design chat, 1 October 2026; recorded in T-G records 5): stage 1 builds B14's three rooms and six setups; B10's room is stage 2's; the proposal is
      closed as not taken;
    - the IRB on dock_loading, then the MPB.
    - ADDED (Hadi and the design chat, 1 October 2026; recorded in T-G records 5): before the IRB, a milestone: one simple scenario per room of B14 runs from start to end;

**T-G: the second domain's rulings (ruled by Hadi, 30 September and 1 October 2026)** — RECORD [T-G/5], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
    A3, A4, A5 and A9 each change code outside the domain, and each carries its acceptance check on kitting: the
    maintained sets stay byte-identical.
    BUILT (1 October 2026): the rename, A9 with R2, A4, A5 and A3 (stage 1, steps 1 to 5). "T-G: the second domain's rulings", STAGE 1, STEPS 0 TO 5 BUILT.
    BUILT (1 October 2026): dock_loading's catch-up, its content and the milestone (stage 1, steps 6 to 8; the
    milestone's acceptance held in all three rooms). ADDED (Hadi, 1 October 2026): before the IRB, a second
    simple scenario per room, then the sorting of the earlier analyses and tests under kitting with the preparation of
    the instruments. "T-G: the second domain's rulings", STAGE 1, STEPS 6 TO 8 BUILT.
  - Stage 2:
    - B7, `store_pallet`, with the second designation (the onward container);
    - ADDED (Hadi and the design chat, 1 October 2026; recorded in T-G records 5): B10's room (the freezer and the dry store on the opposite wall), with its own layout, setup and
      scenarios;
    - ADDED (the same): A8's rule on monitored areas reopened (A8's note); its build inside stage 2 or its own
      increment, decided then;
    - B5, the gate opened on request, and the office door's state;
    - A7, TODO-16, after the MPB's first run on dock_loading.
  - After stage 2: A8, track 4.
  - Stage 3: B12, check-in and check-out, with its two optional items.
  ADDED (T-G records 2, 1 October 2026): T-G pauses between stage 1 and stage 2 (before track 4) while T-K part 1,
  context knowledge, runs (T-K PART 1 above); nothing in it is ruled yet.
  Rulings with no stage, because nothing is built for them: A1 (V1, FW and the tags: a records rule), A2 (terms; no code
  is renamed), A10 (FW directions, outside V1), A11 (a note for T-F), and B12's items "not taken". A6 is an assumption,
  recorded in `docs/assumptions.md` 5.3; stage 1 is where the robot first reads object states through it.
- C2, build 1 (30 September 2026; 56e674e, 6e29c15, 62ebc4e): the form-only repairs (the steps of `pick_up`, `place` and
  `scan_it` bind `?item`; `confirm_delivered_pallet` typed; the layout's `office_chair` typed `office_chair`; the robots'
  tasks in `assigned_tasks`) and scenario_s01_03, a viewing fixture that loads and initialises. scenario_s01_01 and
  scenario_s01_02 still fail at load by intent (`infeasible:office_break(...)` in the load-time replay: the door
  condition). Re-measured at 62ebc4e (1 October 2026): as stated.
  SUPERSEDED (Hadi and the design chat, 1 October 2026; recorded in T-G records 5); B14: env_layout_01, env_setup_01 and scenario_s01_01 to _03 are removed; B14's viewing fixtures
  replace scenario_s01_03.
- C3, the state of `domains/dock_loading/` after build 1 (the survey of 30 September; each line verified against the code
  at 62ebc4e, 1 October 2026). Stage 1's plan starts from this list.
  NOTE (Hadi and the design chat, 1 October 2026; recorded in T-G records 5): the lines on env_layout_01, env_setup_01 and their scenarios (the truck outside the space, the office
  chair in the hall, no landmarks, no assigned tasks for the human) describe artefacts B14 removes; B14's rooms have every
  fixed object inside the space, the chair inside the office and the two landmarks. The rest of the list stands.
  Still not in kitting's current form:
  - no `HumanOnlyTask` (`go_to`, `stand`, `go_to_and_stand`) and no `stand` action; no `script.py` with the call forms;
    the scenarios use raw `TaskInstance`s;
  - `pick_up` and `place` lack the successor-state declarations of T-B2a (`moved_object_key`, `moved_to_key`); `place`
    still has the effect `not_holding` instead of a retraction of `holding`;
  - `wait_at` completes on `ProcessCompletion`, not on the fact `waited`;
  - no landmarks; no exit walk; no purpose statement in the scenarios;
  - the layout has a `zones` block and a `zone` field per object (kitting's layouts too: A2);
  - stale docstrings in `tasks.py` (`?dest`, two gate methods per task, "Human assigned" / "Human foreseeable", no
    `office_break`) and `scenarios/scenarios_s01.py` ("scenario ids keep their old form until stage 3"); layout pictures
    inside the domain folder under an old id (`env_layout1.svg`, `env_layout1_present.svg`, `env_layout1_present.png`,
    `env_layout_original.jpg`; kitting keeps its pictures in `docs/env_layouts_png/`).
    NOTE (Hadi, 1 October 2026, on the B14 build's flags; recorded in T-G records 6): these pictures show the removed env_layout_01. They are kept, renamed with the suffix `_original`
    (`env_layout1_original.svg`, `env_layout1_present_original.svg`, `env_layout1_present_original.png`);
    `env_layout_original.jpg` keeps its name.
  Content that the rulings of part B replace:
  - `deliver_pallet` has a free `?delivery_bay` and one method (B3, B8, B11); `load_return` ranges over every pallet
    (B4); `confirm_delivered_pallet` has no condition (B2); `office_break` has a door condition no fact satisfies and ends
    with a walk to the gate (B5, B6); the human has no assigned tasks in scenario_s01_01 and scenario_s01_02 (B1);
  - the truck extends 40 cm outside the space (to y = −740; the space's y runs from −700); the office chair stands in the
    hall (its declared zone is `zone_hall_center`), 30 cm from the coffee machine (B10).
  In the simulator, written for this domain (A5 replaces them):
  - `mesa_sim/world_state_builder.py` emits `gate_is_open` for every object of type `gate` whose `is_open` is not False,
    and `is_open` is never loaded (always None); nothing emits a door fact;
  - the fields `is_empty`, `is_scanned`, `is_open` on `SimObject`, the `scanned` fact, and the touch handler reading the
    literal `"?item"` (`mesa_sim/action_decomposer.py`; the grasp handler, kitting's too, reads the same literal);
  - `mesa_sim/list_scenarios.py` lists kitting only; `SimModel.get_movable_objects` filters the type `"item"` and nothing
    reads it.
  In the viewer (for T-V, or the stage that first needs it): the colour table's keys (`delivery_area`, `empty_bay`) do
  not match the layout's types (`delivery_bay`, `empty_pallet_bay`; `office_chair` absent); the axis range clips what
  lies outside the space; the label offset is keyed on the type `"shelf"`.
  `domains/README.md` is stale throughout: rewritten with stage 1's build (REFACTOR-03).
- C4, points for the stage plans (not rulings; each returns to the design chat only if it produces a finding):
  - the load-time check for a script that depends on the robot, and the meaning of the outcome "infeasible" under A3;
    RULED (Hadi, 1 October 2026): A3, Q13b (and Q13a for an entry that ends INFEASIBLE);
  - how "completed" is judged for an entry of the human's list (the standby entry must be takable again after the human
    has left the place). PARKED (Hadi, 1 October 2026) as the first design question of the next design chat, the
    lifecycle of an entry: A3's PARKED block; A3 is not built before it is ruled. The byte-identical acceptance does not
    exercise the rule (no maintained kitting set has a dropped task): the ruled rule is also checked on the kitting
    scenarios with a drop event and on the test-bed sets with misdeliveries;
    RULED (Hadi, 1 October 2026): A3, Q12; the added check is A3's ACCEPTANCE;
  - where the exit walk stands relative to the priority list (a plain walk is always applicable);
    RULED (Hadi, 1 October 2026): A3, Q14 (the closing part); dock_loading's, B13;
  - how an event or a foreseeable task is placed relative to tasks whose order is not fixed;
    RULED (Hadi, 1 October 2026): A3, Q15;
  - how a pallet's origin is recorded (B8);
    SETTLED (T-G stage 1's plan, approved by Hadi, 1 October 2026; recorded in T-G records 7): in stage 1 a pallet's
    origin is the setup's initial container (`home_container_of`), which is where every stage-1 pick-up happens; stage 2
    (`store_pallet` picks up from a delivery bay) needs the origin recorded at the pick-up;
  - how the meta-planner behaves when the pool holds tasks and none is applicable (TODO-30);
    CORRECTED (T-G records 7, 1 October 2026): the citation of TODO-30 is wrong; TODO-30 is closed and concerns
    realizability (F1), not applicability. FINDING (T-G stage 1's plan, approved by Hadi, 1 October 2026): a robot task
    with no applicable method raises `DecompositionError` out of `MetaPlanner.update()` (through `_is_complete`), which
    nothing catches, and the run stops. Stage 1 cannot reach it (a method for every area the robot can be in, the gate
    open). Stage 2 (the robot at a closed gate, B5) needs a ruling first. TODO-152;
  - the forms in the setup and the registry for object states and the two designations (A5);
  - the smallest set of methods under B11 with B8;
    SETTLED (the same approval): B11 as amended (answer 6): 8 methods per robot task, the human's methods for the hall
    and the office;
  - how the existing machinery behaves when the live set holds foreseeable tasks only, at the start of a run and between
    deliveries (TODO-143 stays parked: it concerns an empty assigned list, which is a different state);
    SETTLED (the same approval): the existing machinery, nothing new. With the prior on the live set is {coffee_break,
    office_break}; the human waits or walks to the standby place; both hypotheses become inadequate, the finding is
    unexplained, admission refuses and the robot realizes against the fallback projection, as for kitting's exit walk.
    An empty live set is not reached with the prior on while the human is in an area; otherwise exhausted, below theta,
    the fallback;
  - for the IRB on dock_loading the robot is idle, so its setup places the pallets in their delivery containers
    from the start.
  - ADDED (Hadi, 1 October 2026, on the B14 build's flags; recorded in T-G records 6): the rule for a point on the boundary of two areas, which today is decided by the order of
    declaration (`SimModel.get_zone_of_position`: inclusive bounds, the first declared zone wins); and, since an agent
    stops 10 to 30 cm before its target, the area an agent is in after "move to the gate" from each side, in the
    environment and in the computed state alike (R2);
    SETTLED (the same approval): the rule stays the order of declaration, stated in one shared function (`area_of`).
    NOTE (T-G stage 1, step 2 as built, 1 October 2026): that shared function is `area_at`; `area_of` is the planner's
    lookup for an object's area.
    An agent stops 10 to 30 cm short of the gate on its side of approach and stays in the area it came from; the
    projection's arrival point and the replay's walk end (where the body stops, answer 5) give the same area; only the
    centres of the gate and the office door lie on an edge;
  - ADDED (the same): the scanned state of an empty pallet (B14's setups leave it out; the form defaults it to false);
    SETTLED (the same approval): it does not hold (the form's default: a declared state not listed does not hold);
    nothing reads it with the prior on;
  - ADDED (the same): the stale references to removed dock_loading scenarios in `mesa_sim/run_mesa.py` (its docstring
    and commented-out imports name scenario_s01_01 and _02), corrected in stage 1's first build step.
  - ADDED (Hadi, 1 October 2026, on the T-G records 3 flags; recorded in T-G records 4), R2 (C1, stage 1): the agent's area in a computed state after a movement action, one
    definition shared with the environment's state construction; the plan names the shared representation, every
    consumer of a computed state that decomposes a later task, and the form.
- C5, to watch in the test-beds: hypotheses that predict the same motion divide the belief, so none passes the admission
  threshold (two unscanned pallets in one container). If the IRB confirms it on dock_loading, it is a finding
  about the mind and returns to the design chat within V1.
  CONFIRMED (the IRB on dock_loading, 1 to 2 October 2026; records 2 October 2026, T-G records 9): in C3 and on
  C4's first two walks, in all three rooms, two scans of one bay share the belief and neither reaches the threshold (9
  stretches; none admitted). A finding about the mind, NOT RULED; it returns to the design chat. Linked to the recorded
  direction on acting on a set of hypotheses with the same projection: belief-aware planning, the covering set S_ε and
  one realization against its projections jointly (TODO-97). "T-G", STAGE 1, THE IRB ON DOCK_LOADING BUILT.
- C6, open at their stage: the design of check-in and check-out; the design of TODO-16; how the MPB's oracle derives an
  expected decision when the human's sequence depends on the robot's decisions.
  ANSWERED FOR STAGE 1 (Hadi, 2 October 2026; T-G records 10): the third clause, by THE MPB ON DOCK_LOADING, MPB-DL3.
  The first two clauses stay open at their stages.

**Stale passages, input for a later consolidation (records, 2 October 2026; Hadi's ruling of that day)**
Found in the records split's plan step and listed as reported there; not corrected now (the corrected ones are the two
area passages of design_decisions.md, CLAUDE.md's invariant and the docstring in `shared/types.py`, commit fbc8a55).
Line numbers are those of `docs/design_decisions.md` at 248a946, before the split; each passage is in design_decisions.md
or, where the split moved it, in the record file its index line names.
- 103–109 and 116–120: scenarios are YAML, `scenarios.yaml` → scenarios are Python literals
  (`domains/*/scenarios/scenarios_sNN.py`).
- 132–160: one unified `env_objects` list → split between the layout file and the setup file (T-L).
- 195–213: the progress evaluator "directional" → `excess_path` (`shared/likelihood_functions.py:184`).
- 361–371: `_project()` raises for orderings → `Projector.project` chains orderings (`shared/projection.py:216`).
- 1943: `realize()` not yet consumed → the meta-planner consumes it.
- 2035, 2181: min_separation as 2.5 × motion → a body-supplied distance (`shared/meta_planner.py:254`).
- 2038: no projection means δ = 0 → a fallback projection since T-D P (`shared/meta_planner.py:354–359`).
- 2383: `task_instance_key` equality → `same_task` (`mesa_sim/sim_agents.py:539–545`).
- 2619: `_clears_gate` tests confidence ≥ θ → it returns a `GateOutcome`, which also needs adequacy and warrant
  (`shared/meta_planner.py:202, 712`).
- 2964: a `BETA` constant → beta is a required constructor argument (`shared/recognizer.py:360`).
- 3146: `DomainKnowledgeBase` → `Tree` (`shared/knowledge.py:201`).
- 3150, 3272: `zone_of`, `in_zone`, `object_zones` → `area_of`, `in_area`, `object_areas`.
- 3227: `Projector._successor_state` → `successor_state` (`shared/projection.py:623`).
- 3869–3871 (T-H): the support includes `∪ {unknown}` → no `unknown` hypothesis.
- 3881, 3903 (T-H): the script is an ordered list → A3's priority form (`world/human_executor.py:31–40`).
- 3926: a coverage enum → the classes in `world/queries.py:143–169`.
- 4173: "zones" → areas.
- 4344–4346: R3 "to be built" → built (`shared/meta_planner.py:793`).
- 4723–4729 and 4749 (L4, L5): a live set from terminal facts only → A4's inapplicability as well
  (`shared/recognizer.py:490, 760–768`).
- 4856: "P adds no trigger" → `projection_expired` (`shared/meta_planner.py:466`).
- 4845, 4868: the decision record stays empty under a fallback → its expiry field is set
  (`shared/meta_planner.py:578–596`).
- 4875–4877: a stationary tail at the current position → `project_fallback` returns None (`shared/projection.py:415–418`).
- 4871: one stored field → also a run length and a standing count (`mesa_sim/sim_agents.py:404, 624–639`).
- Code docstrings: `mesa_sim/world_state_builder.py:54` repeats "in_area … context for IR"; `shared/types.py:479–490`
  (`goto_zone`, `?zone`); `shared/types.py:1142` (`FallbackProjection`); `world/human_executor.py:42` (`shared/record.py`).
CLAUDE.md's "Current phase and status" section and `docs/TODOS_AND_DEFERRED.md` show the same mix of conceptual design
and record; they are not treated in this step.

## T-G stage 1: the plan, the build, the test-beds, the close

**T-G: the second domain's rulings (ruled by Hadi, 30 September and 1 October 2026)** — RECORD [T-G_stage1/1], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
STAGE 1 PLAN APPROVED (Hadi, 1 October 2026; recorded in T-G records 7). The approved plan, with the answers merged in,
is `docs/handoffs/plan_T-G_stage1.md`; every build session of stage 1 reads it. The answers to the plan's nine questions:
1. `deliver_pallet` has no condition on the pallet being full. Reason: the designation and the load check (an assigned
   task's determined parameter, resolved from the station, must have its declared type) exclude an empty pallet, and the
   planner needs no negated condition. It answers B4 for `deliver_pallet`; `load_return`'s methods read `is_empty`.
2. A fixed object's area is derived from its position; the declared per-object field is dropped (A9 AMENDED).
3. dock_loading's area ids are `area_hall`, `area_office`, `area_truck_side`; kitting's ids stay.
4. The carriers of the area that nothing reads are removed (`AgentState`'s area, the observation's area,
   `SimObject`'s area and its query); the `in_area` fact stays.
5. The load-time replay ends a walk where the body stops. Reason: the replay and the run must select the same method at
   the gate and at the office door.
6. Not as recommended: a task has a method for every area the agent can be in, not for every area (B11 AMENDED).
7. The task model names `dock_gate`, `office_door` and the area ids, as this domain's convention.
8. The milestone scenarios as proposed, one per room (scenario_s03_02, s05_02, s07_02).
9. The build may edit `shared/io_contracts.md`, `README.md`, `domains/README.md` and the note in `docs/rename_table.md`;
   the glossary and this file stay with records steps.
Also approved: the names in the plan's section 6 as proposed; the build order, steps 0 to 8, with their acceptance and
stop conditions.
Notes (not rulings):
- A pallet's origin is the setup's initial container in stage 1; stage 2 needs it recorded at the pick-up (C4).
- The rename leaves `ros_sim/` passing the old field names (`current_zone`, `object_zones`); `ros_sim/` is not touched
  (TODO-111's note).
- The walk to the standby place has no hypothesis in the robot's task model, so a scenario with a standby entry is
  classed as containing unmodelled behaviour, and its purpose says so (`docs/assumptions.md` 1.2). PARKED for after the
  milestone, not ruled: whether the robot's mind holds a hypothesis for the human stepping aside.
- In the IRB setup (B14, kind 1) the case with the assigned scan of the pallet in the truck is declared
  dependent on the robot; its priority list never finishes, so that run has no walk to the desk (B13, assumptions 1.1).
- REQUIREMENT on the later preparation of the IRB and the MPB on dock_loading: the instruments obtain the human's
  run-time sequence from the executor's own selection rule; they do not implement that rule a second time. Reason: one
  definition. (Under R1 the load-time replay no longer gives that sequence for a script with a standby entry.)
- Finding: a robot task with no applicable method stops the run (C4, TODO-152).

STAGE 1, STEPS 0 TO 5 BUILT (1 October 2026; built and accepted, each against the plan's acceptance and stop conditions).
- Step 0: the HEAD runs of the extended set (the four maintained sets, the ten kitting drop scenarios, the IR and MPB
  test-bed sets), kept outside git as the reference set of every later step; no commit.
- Step 1, the rename "zone" to "area": 8d064ca; the stale references to removed dock_loading files: c21f001.
  ADDED (records, 1 October 2026): acceptance, 655 reference files byte-identical, 220 tests.
- Step 2, the declared areas and the agent's area in a computed state (A9, R2): b513b82; the layout's per-object area
  field dropped: 9bca721; `shared/io_contracts.md`: a76054f.
  ADDED (records, 1 October 2026): acceptance, 844 reference files byte-identical, 225 tests.
- Step 3, liveness by applicability (A4) and `AdaptivePlanner.is_applicable`: bd4bddc.
  ADDED (records, 1 October 2026): acceptance, 847 reference files byte-identical, 232 tests.
- Step 4, object states and designations (A5): b74485b; `shared/io_contracts.md`, `domains/README.md`: 50f2fb8.
  ADDED (records, 1 October 2026): acceptance, 847 reference files byte-identical, 241 tests.
- Step 5, the human's script form (A3): 048a36e; `shared/io_contracts.md`: 576f2b2.
Next: step 6 (dock_loading's catch-up, with the area ids), step 7 (the domain's content), then the milestone (step 8).
NOTES (records, 1 October 2026; facts of the build, not rulings):
- The shared function for a position's area is `area_at(position, areas)` (the plan's 3d named it `area_of`); the
  planner's lookup for an object's area keeps the name `area_of`.
- A setup entry that still carries the old per-object state fields (`is_empty`, `is_scanned`) is ignored for those
  fields, not refused. An authoring risk, parked under TODO-151; step 4 was not widened.
- A dock_loading grasp raises an explicit error (the action declares no `moved_object_key`) until step 6 gives `pick_up`
  its final form. Intended; no fixture grasps.
- Step 2 made the walks of kitting's load-time replay 1 to 3 ticks shorter (the replay's walk ends where the body stops,
  answer 5); no maintained output contains them.
- Step 3 removed two dead branches, in the adequacy test and in the warrant, with no change of output.
- A closing entry begun and not finished at the run's end counts as open. A dependent script always writes its end line
  (`[rec] end step=n open=-` when no entry is open).
- The log wording for a hypothesis that never enters the live set, `[IR-inapplicable] step=N <key> does not enter the
  live set: no applicable method`, is confirmed as built.
- Four frozen analysis scripts no longer run since the rename (step 1): `analysis/i4_evidence_model/check_i4.py`,
  `analysis/g1_graded_evidence/unit_checks.py`, `analysis/i4c_episode/check_i4c.py`,
  `analysis/i4d_fold_unknown/check_i4d.py`; they need the old field names. Frozen records: not edited.

STAGE 1, STEPS 6 TO 8 BUILT (1 October 2026; built and accepted, each against the plan's acceptance and stop
conditions; the milestone accepted by Hadi).
- Step 6, dock_loading's catch-up (the forms brought up to kitting's; the area ids `area_hall`, `area_office`,
  `area_truck_side`; `domains/dock_loading/script.py`; `domains/README.md` rewritten): 670cb78; `list_scenarios.py`
  lists every domain, `SimModel.get_movable_objects` removed (no reader): 610fed9.
- Step 7, the domain's content (the plan's section 4: 16 robot methods, 11 human methods, the declared states, the task
  model): 1492789; its tests, `tests/test_tg_dock_tasks.py`: 512a452.
- Step 8, the milestone: the two allowed one-line corrections (the stale note on `ProcessCompletion` in
  `shared/types.py`; the viewer's colour keys for the three area ids): 52b2aae; the three scenarios, scenario_s03_02
  (env_layout_02, env_setup_03), scenario_s05_02 (env_layout_03, env_setup_05), scenario_s07_02 (env_layout_04,
  env_setup_07), as the plan's answer 8 states them: 8b9d267. Prior on, 800 steps, headless. The acceptance held in all
  three rooms: the run ends with no error; the robot completes both tasks; every entry of the human's script is closed,
  the closing part included (`[rec] end step=800 open=-`). The maintained sets byte-identical, 301 tests.
  CAVEAT (Hadi, 3 October 2026): these runs pass step 500 and are potentially confounded by the undeclared context
  weight; SCOPE REDUCED AND THE MPB ON DOCK_LOADING RUN, its CAVEAT, below.
  Completion ticks (the world tick; the declared tick in brackets), env_layout_02 / env_layout_03 / env_layout_04:
  `deliver_pallet(pallet_0)` 64 / 64 / 57; `load_return(pallet_4)` 125 (127) / 125 (127) / 151 (153); the scan,
  `is_scanned` holds / the record closes the entry, 92, 94 / 92, 94 / 74, 76; `go_to(desk)` completes 140 / 140 / 112.
FINDINGS OF THE MILESTONE (Hadi and the design chat, 1 October 2026, on ccode's report; each with its classification):
- The walk to the standby place and the meeting at a shared bay (the plan's section 5, last point) were not exercised:
  the human starts at the standby place, where `go_to(standby_place)` is complete, so the machine waits there (the skip
  rule), and the robot's second task was a return. A gap of the scenario. A second simple scenario per room follows.
  The three descriptions state that the standby walk is not taken.
- env_layout_02 and env_layout_03 produced identical motion: the scenario uses neither of the two objects that differ
  between them (the frozen bay, the coffee machine). The recognition differs (the coffee machine), the motion does not.
- In env_layout_04 the human passes the standing robot at 22.5 cm (ticks 66 to 69). The robot had left the bay toward
  the empties, decided to hold at tick 63 before the scan was admitted (admitted at 69), and stood about 95 cm from the
  bay's point, on the human's straight line to the bay. Classified: the parked case of the human walking toward the
  robot (X3, TODO-135); a standing robot does not violate by definition (F1); the simulated human does not react to the
  robot. Note: in this domain the case is structural, because a scan becomes applicable at the moment of delivery, so
  the human walks to a bay when the robot leaves it. Whether to reopen the parked case is decided after the MPB, with
  counts from all rooms.
- A measure for the evaluation: the number of ticks in which the human passes a standing robot closer than the minimum
  separation, reported separately from violations by a moving robot. Reason: the hold turns a closeness that would
  count against a moving robot into one the present measure does not count. Nothing is added to the code for it now
  (TODO-144, TODO-135).
- In env_layout_02 the walk to the desk is admitted as coffee_break (tick 112). The recorded effect of an unmodelled
  walk read as the nearest modelled task ("T-D G", the movement source's half-plane test; TODO-140); no consequence in
  this run.
- Candidate finding about the mind, NOT RULED: the robot's own delivery makes the scan applicable, and the robot does
  not anticipate the human's walk to that bay; the scan hypothesis enters at an equal share and is admitted 8 to 12
  ticks after the human starts (TODO-154).
- Parked question, now with evidence, NOT RULED: whether the robot's mind holds hypotheses for the walks to the standby
  place and to the desk (TODO-155; it carries the approval's parked note on the human stepping aside).
- On a fixture with no assigned tasks for the human, every task of the robot's task model becomes a hypothesis: the
  parked case TODO-143. With the restriction off, two hypotheses about empty pallets become possible: artefacts of
  running without the prior (`docs/assumptions.md` 1.4).
NOTES FROM THE INDEPENDENT REVIEW of dock_loading's task file against kitting's (records, 1 October 2026). The file
follows kitting's building blocks and rules; no special case for dock_loading exists in shared code.
- The robot's methods use a pallet's emptiness as a proxy for the side of the gate on which its origin lies. True for
  every pallet the robot handles in stage 1. False in stage 2, when a full pallet has an origin in the hall (TODO-156).
- The method for "holding another full pallet" (return_full) has no condition of its own; it is correct through its
  position after the method for an empty one (return_empty) and through equal gate conditions.
- `stand` has one method with no area condition: over-broad, and the stated exception to "the absence of a method is
  the check" (the plan's section 4).
- `office_break` waits 60 seconds, copied from `coffee_break`; no record gives the value; Hadi's word is pending
  (TODO-157).
- One dictionary is shared by eight methods: a maintainability risk with no behavioural effect.
- A design question for stage 2, to rule before `store_pallet`: a route is selected from the areas of the agent and of
  the object, not from the kind of task and the pallet's state (TODO-156).
A STEP ADDED (Hadi, 1 October 2026), before the IRB and the MPB run on dock_loading: the earlier analyses in
`analysis/` and the tests are sorted under kitting, so that nothing of kitting is mixed with dock_loading's. The
instruments' code is shared; their run sets, expectations and reports are per domain. Its own commit, no change of
behaviour; the maintained sets and the reference set byte-identical; every path named in a record or a README updated.
Next: the second simple scenario per room; then the step added above, with the preparation of the instruments (the
plan's section 7, "After the milestone"); then the IRB scenarios, agreed with Hadi before they are authored.
STAGE 1, THE SECOND MILESTONE SCENARIO BUILT (1 October 2026; built and accepted, records 1 October 2026).
- Built: scenario_s03_03 (env_layout_02, env_setup_03), scenario_s05_03 (env_layout_03, env_setup_05), scenario_s07_03
  (env_layout_04, env_setup_07), one per room on the MPB setups, identical in content: the robot is assigned
  `deliver_pallet` of pallet_0 and pallet_1 (the dry bay) and of pallet_2 (the frozen bay) and `load_return(pallet_4)`;
  the human is assigned the three scans, with the script [the three scans, the dry bay's first,
  `RepeatableEntry(go_to("standby_place"))`], closing [`go_to("desk")`], `ScriptDependence.ON_ROBOT`. Each description
  states the purpose and the unmodelled behaviour (the walk to and the stay at the standby place, the walk to the desk).
  0371035. Prior on, `single_task`, 1000 steps, headless. The acceptance held in all three rooms: the run ends with no
  error; the robot completes its four tasks; every entry of the human's script is closed, the closing part included
  (`[rec] end step=1000 open=-`). The maintained sets byte-identical, 301 tests.
  CAVEAT (Hadi, 3 October 2026): these runs pass step 500 and are potentially confounded by the undeclared context
  weight; SCOPE REDUCED AND THE MPB ON DOCK_LOADING RUN, its CAVEAT, below.
  Completion ticks (the world tick; the declared tick of the last task in brackets), env_layout_02 / env_layout_03 /
  env_layout_04: `deliver_pallet(pallet_0)` 64 / 159 / 148; `deliver_pallet(pallet_1)` 182 / 276 (278) / 285 (287);
  `deliver_pallet(pallet_2)` 289 (291) / 58 / 57; `load_return(pallet_4)` 125 / 220 / 236; the scans, `is_scanned`
  holds / the record closes the entry: pallet_0 92, 94 / 188, 190 / 164, 166; pallet_1 209, 211 / 303, 305 / 301, 303;
  pallet_2 318, 320 / 84, 86 / 83, 85; `go_to(desk)` completes 346 / 351 / 339.
- Exercised:
  - The priority rule: the first applicable open entry is taken. In env_layout_03 and env_layout_04 the robot delivered
    pallet_2 first, and the human scanned it first, against the written order.
  - The walk to the standby place between scans: two per room (env_layout_02 94 to 121 and 211 to 238; env_layout_03 86
    to 111 and 190 to 217; env_layout_04 85 to 110 and 166 to 182).
  - The frozen bay, which makes the three rooms differ in motion and in recognition.
  - Each scan hypothesis enters the live set on the tick of its delivery (A4, `[IR-reentry] ... live again:
    applicable`).
- Not exercised: the robot arriving at a bay where the human stands, and two scans possible at once in one bay. Reason:
  a round trip to the truck takes about 96 ticks and a scan from the standby place 16 to 30, so the human finishes
  before the next pallet arrives; at every delivery the human was at the standby place, and the live intervals of the
  scans never overlap. The note on B14 ("that conflict is certain whenever both concern the same bay") is corrected
  there: it requires that the human is still at the bay when the robot arrives. Consequence recorded for the MPB's
  design on dock_loading, NOT RULED: a setup in which some pallets already stand in a bay while the robot delivers
  others.
FINDINGS OF THE SECOND MILESTONE SCENARIO (Hadi and the design chat, 1 October 2026, on ccode's report; each with its
classification):
- Five of the six walks to the standby place are admitted as coffee_break or office_break on the observation warrant,
  wrongly (env_layout_02 at 114 and 231, coffee_break; env_layout_03 at 109, coffee_break, and 206, office_break;
  env_layout_04 at 94, office_break; the sixth, env_layout_04 166 to 182, never clears theta). The finding turns
  unexplained once the human stands, and the gate refuses with `none(leader_inadequate)`. No consequence on a decision
  in these runs. The parked question TODO-155: the walk follows almost every scan in this domain, so the case is
  frequent. It becomes the first design question before the IRB set. NOT RULED.
- At the end of every run the human walks up to the standing robot: 8.69 cm (env_layout_02, at 320), 13.41 cm
  (env_layout_03, at 301), 8.11 cm (env_layout_04, at 299); 9 / 8 / 8 ticks below the minimum separation with a
  standing robot, 0 with a moving robot in all three. The robot's last task is a delivery, and a robot with an empty
  pool stays where it is, at the bay the last scan walks to. The parked case of the human walking toward the robot
  (X3, TODO-135). PROPOSAL for stage 1, NOT RULED: an authoring convention that the robot's last assigned task is a
  return.
  CLOSED, NOT TAKEN (Hadi, 2 October 2026; T-G records 10; THE MPB ON DOCK_LOADING, MPB-DL4): the robot's pool is
  unordered and the meta-planner selects by cost. In its place the MPB reports the separation counts per room.
- In env_layout_03 at tick 64 the robot changes its task on the fallback projection while the gate refuses (below
  theta): at 60 the three candidates lay within 0.6 and `load_return` won; at 64 the fallback, the human walking
  straight toward the robot, charged `load_return` a shift of 4 and `deliver_pallet(pallet_0)` won, 94.68 against
  97.46. The conflict enters the cost and decides the choice. Consistent with the design; noted for track 3b
  (TODO-145).
- The scan at the frozen bay is late because the coffee machine lies in the same direction from the standby place:
  in env_layout_04 it enters at 57 and is admitted at 76, 19 ticks after; in env_layout_02 it enters at 289, leads from
  308 (19 ticks after) and clears theta at 315 (it is the last scan, see the next point). TODO-154, with the room's
  geometry.
- The last scan is never admitted (env_layout_02 pallet_2, env_layout_03 and env_layout_04 pallet_1), because an empty
  pool gives no further decision. Noted, no action.
Next: the design of the IRB set with Hadi (first question: TODO-155); then the sorting of the earlier analyses
and tests under kitting, with the preparation of the instruments (the step added above); then the set's authoring and
its runs.
RULED (Hadi, 1 October 2026; recorded in T-G records 8, 1 October 2026): T-G Q16, the duration of office_break, and the
IRB set on dock_loading. Records only; nothing in this block is built.
- Q16, the walk to the standby place in the robot's mind (TODO-155).
  The walk stays without a hypothesis for now. The IRB set observes how the present recognizer explains it; that
  is the baseline.
  Two candidates are recorded on TODO-155, neither approved for building:
  - H1: a foreseeable task "the human steps aside to the standby place", always possible, with the standby place as a
    fixed object.
  - H2: a hypothesis that is live only while no assigned task of the human is applicable.
    CORRECTED (Hadi, at the approval of the IRB's build, 1 October 2026; recorded 2 October 2026, T-G records
    9): worded "a hypothesis that is live only while no assigned task of the human is live". Reason: a scanned pallet's
    scan stays applicable (its guards do not read is_scanned), so read as "applicable" H2 would never be live after a
    scan.
  The difference: the human steps aside only when no other pallet is applicable. H1 states an unconditional behaviour
  that the human does not perform, and competes with the scans when a pallet waits; H2 matches the condition and changes
  the rule for the live set (A4).
  Not taken: the walk as the tail of the scan task. Reasons: the human would step aside after every scan, also when a
  pallet waits; the condition "no other pallet waits" cannot be stated in a method; the scan's terminal fact would hold
  in the middle of the task.
  NOTE (records, 2 October 2026; T-G records 9), on H1: the always-possible standby task, as a walk only, would make
  move_to a terminal action of the task model (the last action of one of its methods), so under L1 every arrival at any
  target would be an episode boundary. A wait at its end would avoid that.
  For T-K part 1, one design question, NOT RULED: what sets a hypothesis's share at the start of an episode. Four
  determinants are recorded for it: the assignment (exists); context facts; the task that just ended (a transition prior
  between tasks, Hadi's idea); an enabling event, such as the robot's own delivery (TODO-154). They are designed as one
  mechanism. Recorded under C1, T-K PART 1.
  Also for T-K part 1, Hadi's ideas, NOT RULED: the duration of a foreseeable task is not one fixed number; temporal
  context can be a fuzzy set with a degree of membership. Recorded under C1, T-K PART 1.
- The duration of office_break (TODO-157, closed as ruled): `office_break` lasts 90 seconds; `coffee_break` stays 60.
  Reason: a long absence lets pallets accumulate in a bay, which gives two scans possible at once and the robot arriving
  at an occupied bay; it differs clearly from the coffee break. The change of the value is made in the next build step.
  B6's note.
- The IRB set for dock_loading, agreed: 14 controlled scenarios (C1 to C14) and 4 mixed (M1 to M4), each in all
  three rooms (env_layout_02, env_layout_03, env_layout_04), on the room's IR setup (kind 1 of B14: env_setup_02,
  env_setup_04, env_setup_06; pallet_0 and pallet_1 in the dry bay, pallet_2 and pallet_3 in the frozen bay, pallet_4 in
  the truck), the robot idle on the gate's centre, the human starting at the standby place, the closing part the walk to
  the desk (B13). "scan n" is `confirm_delivered_pallet` of pallet_n; where no assignment is named, the assigned tasks
  are the script's scans. The script of each, with its purpose:
  - C1: scan 0, scan 2 (assigned work, two bays).
  - C2: scan 2, scan 0 (order).
  - C3: scan 0, scan 1 (two scans with the same motion).
  - C4: scan 0, 2, 1, 3 (lifecycle over many episodes).
  - C5: scan 0, coffee_break, scan 2 (a foreseeable task between scans).
  - C6: scan 0, office_break, scan 2 (the office and its door).
  - C7: scan 0 with coffee_break started on arrival at the pallet; scan 2 (a foreseeable task inside a scan).
  - C8: scan 0 with coffee_break cut into the walk to the pallet; scan 2 (an interruption inside a walk).
  - C9: scan 0 dropped during its walk; scan 2 (a dropped scan).
  - C10: scan 0 dropped; scan 2; scan 0 as a second entry (an authored retry; Q12).
  - C11: scan 0; a stand in the hall; scan 2 (the long stand).
  - C12: assigned the scans of 0 and 2; script: scan 1, scan 2 (a scan outside the assigned set).
  - C13: assigned the scans of 0 and 4; script: scan 0, scan 4, the standby entry; dependent (the standby walk from the
    dry bay; a hypothesis never live).
  - C14: assigned the scans of 2 and 4; script: scan 2, scan 4, the standby entry; dependent (the standby walk from the
    frozen bay).
  - M1: scan 0 with coffee_break on arrival; office_break; scan 2.
  - M2: scan 0 dropped; coffee_break; scan 2; scan 0.
  - M3: scan 0; a stand; scan 1 with coffee_break cut into the walk.
  - M4: assigned 0, 2, 4; script: scan 1; office_break; scan 2; scan 4; the standby entry; dependent.
  Rules of the set:
  - The controlled scenarios run and are read first; a mixed scenario is read only against what the controlled ones have
    shown.
  - Expectations are derived from the records before the runs (as in "The intention-recognition test-bed (IRB)").
  - Nothing is adjusted to a result; findings are classified (`docs/assumptions.md`).
  - The standby walks (C13, C14, M4) are diagnostic observations. Beside the expectation under the present model, the
    predictions under H1 and under H2 (Q16) are written down before the run. Only the present model's expectation is
    compared with the run.
  NOTE (T-G records 8, not a ruling; a consequence of Q14 and B14 to be confirmed by Hadi): in C13, C14 and M4 the scan
  of pallet_4 never becomes applicable (the robot is idle, pallet_4 stays in the truck), so its entry stays open, the
  priority list is never finished and the closing part, the walk to the desk, is not taken; the record states the
  entries still open at the run's end (Q13b).
Next: the build step that sorts the earlier analyses and tests under kitting and prepares the instruments for dock_loading
(the step added above, with the plan's section 7, "After the milestone"); then the authoring of the set, its
expectations and its runs.

STAGE 1, THE IRB ON DOCK_LOADING BUILT, RUN AND ACCEPTED (1 to 2 October 2026; accepted by Hadi, 2 October
2026; records 2 October 2026, T-G records 9). The results are recorded here because the design chat cannot read
analysis/; the report is analysis/dock_loading/irb/REPORT.md.
BUILT, with the commits and the acceptance of each part:
- The sort of kitting's analyses and tests (746fae6, 9a35af1, ae77689): analysis/kitting/ (every earlier analysis,
  the four maintained sets, kitting's IRB and MPB sets), analysis/instruments/ (the shared code;
  run.sh <domain>), analysis/dock_loading/; the run files under configs/kitting/; the tests under tests/kitting/,
  tests/dock_loading/, tests/instruments/ (three two-domain tests stay at tests/). The path table:
  docs/rename_table.md, "Paths: the sort"; dated entries, frozen reports, descriptions and comments keep the old paths.
  Acceptance: the reference set regenerated from the sorted tree, 847 files, 844 byte-identical and the three stdout
  files differing in the run-file path token only; the four maintained sets byte-identical; 301 tests, the same ids;
  the moves pure renames apart from 14 path-edited scripts and 33 run-file headers; 83 scenarios load.
- The instruments prepared for dock_loading (65273e8, cbeefe4, e573e9e; then 3ea4b60, 736eb01, e4fc88c):
  - the human's run-time sequence from the executor's own selection rule: the trajectory drives a StackMachine on the
    whole script (repeatable entries and the closing part included) as the body drives it, against the world the
    environment's builder makes; the load-time replay is no longer the source (R1 skips the standby entry);
  - the oracle brought to liveness by applicability (A4), the agent's area (A9, R2) and the boundary through each
    terminal action's preconditions and completion (L1's as-built reading; adds scan_it), the domain from the run file;
  - the log reader: the pool read without kitting's words, the [IR-inapplicable] lines;
  - the separation counts per run (separation.md): a moving robot violating or receding, and a standing robot with
    the human passing (moved on the tick) or standing beside it (did not);
  - the figure: a fourth colour and a facet beyond four hypotheses; the summary's open entries; baseline.py (reporting).
  Acceptance: kitting's 17 IR and 16 MPB trajectories and 17 expectation tables byte-identical before any run; the 17
  IR runs and the 16 MPB scenarios under each strategy byte-identical in every output apart from the new separation
  files (17 and 32); 301 tests.
- office_break at 90 seconds (edbe34f). Acceptance: the four maintained sets byte-identical (96 files); the milestone
  reruns identical except scenario_s05_03 at tick 206 and scenario_s07_03 at tick 94, the decision admitting
  office_break (T_h 15 ticks longer, one candidate's share; winner, cost and hold unchanged, the .rec identical).
- The 54 scenarios (51e5e1c): scenario_s02_02 to _19 (env_layout_02, env_setup_02), s04_02 to _19 (env_layout_03,
  env_setup_04), s06_02 to _19 (env_layout_04, env_setup_06), in domains/dock_loading/scenarios/scenarios_s02.py,
  _s04.py, _s06.py; _02 to _15 the controlled rows C1 to C14, _16 to _19 the mixed M1 to M4; run files in
  configs/dock_loading/irb/. Authoring values approved by Hadi: a cut or a drop during a walk at PT28S; the
  stand at the bay just scanned, stand(PT80S); M3 with scan 2 in place of scan 1; C13, C14, M4 dependent on the robot.
  Acceptance: 137 scenarios load; the three dependent scripts report the entries not replayed.
- The expectations committed before the runs (54edb71): per scenario the trajectory, expected.csv and phases.json (θ =
  0.75, the value of record) and predictions.md (C13, C14, M4: the present model beside H1 and H2); every run's own
  oracle call reproduced them byte for byte.
RESULT: 42 controlled runs (4d9011d) and 12 mixed runs (b20a67f), zero disagreements, zero unmatched rows; every
trajectory equal to the run's human lines on every tick; separation counts 0 (the closest approach 115.85 cm). What it
establishes: the recognizer behaves on dock_loading as the records specify (rules 1 to 27 of the instrument). It does
not establish the quality of the recognition.
THE BASELINE (all 54 runs; one tick is 2 seconds): of 153 true stretches, 147 lie in the support (6 outside: the scan
of pallet_1 in C12 and M4). 98 of the 147 reach the threshold within the stretch (38, 40 and 20 of 49 on env_layout_02,
_03, _04); the median delay is 20 ticks (range 6 to 50; 28, 16 and 17 by room). 49 never reach it, all scans: 34
stretches of 26 ticks or fewer, 9 same-motion pairs, 3 second scans with no walk, 3 scans leaving the office in
env_layout_02. Every coffee_break and office_break stretch reaches it. Ticks from each true stretch's start to the
threshold, per row and room ("never": not within the stretch; "out": outside the support):
| row | env_layout_02 | env_layout_03 | env_layout_04 |
|---|---|---|---|
| C1 | scan 0 10, scan 2 50 | scan 0 14, scan 2 24 | scan 0 never, scan 2 never |
| C2 | scan 2 25, scan 0 28 | scan 2 8, scan 0 34 | scan 2 21, scan 0 never |
| C3 | scan 0 never, scan 1 never | scan 0 never, scan 1 never | scan 0 never, scan 1 never |
| C4 | scan 0 never, scan 2 never, scan 1 28, scan 3 50 | scan 0 never, scan 2 never, scan 1 34, scan 3 24 | scan 0 never, scan 2 never, scan 1 never, scan 3 never |
| C5 | scan 0 10, coffee 49, scan 2 never | scan 0 14, coffee 13, scan 2 19 | scan 0 never, coffee 17, scan 2 10 |
| C6 | scan 0 10, office 33, scan 2 never | scan 0 14, office 30, scan 2 14 | scan 0 never, office 6, scan 2 37 |
| C7 | scan 0 10, coffee 50, scan 0 27, scan 2 50 | scan 0 14, coffee 17, scan 0 15, scan 2 24 | scan 0 never, coffee 21, scan 0 never, scan 2 never |
| C8 | scan 0 10, coffee 37, scan 0 26, scan 2 49 | scan 0 never, coffee 11, scan 0 15, scan 2 24 | scan 0 never, coffee 20, scan 0 never, scan 2 never |
| C9 | scan 0 10, scan 2 31 | scan 0 never, scan 2 21 | scan 0 never, scan 2 10 |
| C10 | scan 0 10, scan 2 31, scan 0 28 | scan 0 never, scan 2 21, scan 0 34 | scan 0 never, scan 2 10, scan 0 never |
| C11 | scan 0 10, scan 2 46 | scan 0 14, scan 2 21 | scan 0 never, scan 2 17 |
| C12 | scan 1 out, scan 2 50 | scan 1 out, scan 2 24 | scan 1 out, scan 2 never |
| C13 | scan 0 9 | scan 0 14 | scan 0 14 |
| C14 | scan 2 25 | scan 2 8 | scan 2 21 |
| M1 | scan 0 10, coffee 50, scan 0 27, office 34, scan 2 never | scan 0 14, coffee 17, scan 0 15, office 30, scan 2 13 | scan 0 never, coffee 21, scan 0 never, office 6, scan 2 36 |
| M2 | scan 0 10, coffee 37, scan 2 never, scan 0 28 | scan 0 never, coffee 11, scan 2 19, scan 0 33 | scan 0 never, coffee 20, scan 2 never, scan 0 never |
| M3 | scan 0 10, scan 2 never, coffee 33, scan 2 never | scan 0 14, scan 2 never, coffee 13, scan 2 19 | scan 0 never, scan 2 never, coffee 7, scan 2 11 |
| M4 | scan 1 out, office 33, scan 2 never | scan 1 out, office 30, scan 2 15 | scan 1 out, office 8, scan 2 37 |
FINDINGS (classified as findings about the mind; none ruled):
- Hypotheses that predict the same motion divide the belief and are not admitted: the watched item C5, confirmed (C5's
  note). Linked to the recorded direction on acting on a set of hypotheses with the same projection (TODO-97).
- A short walk gives too little evidence under equal shares at the start of an episode (34 of the 49 stretches that
  never reach the threshold last 26 ticks or fewer; on env_layout_04, 16 steps from the standby place to the dry bay,
  scan 0's first walk never reaches it with three or more rivals live). It joins T-K part 1's question on what sets a
  hypothesis's share at the start of an episode, as its measured baseline (C1, T-K PART 1; TODO-154).
- The walk to the standby place: admitted as a break in five of six controlled runs (C13 and C14: coffee_break or
  office_break by the room's bearings, cleared 8 to 23 ticks into the walk; never above θ in scenario_s06_14); in M4
  admitted on env_layout_02 as the scan of pallet_0 (from 167), an assigned task the human never performs and that stays
  live with its commitment warrant. The finding turns unexplained once the human stands. On TODO-155, with the written
  predictions: C13 and C14 separate the conditional candidate (H2) from the present model, M4 does not (H2 is never live
  there, scan 0 being live).
- Two pallets in one container stand on one point: the second scan has no walk and a walk between them cannot be cut;
  a property of "one point per container" (B9's note).
CORRECTIONS of earlier notes: one tick is 2 seconds (B6's note: office_break's wait 45 ticks, the absence about 110
ticks, reviewed with the MPB's design); H2 worded "no assigned task is live" (Q16's block); the always-possible standby
task as a walk only would make every arrival an episode boundary (Q16's block).
The IRB of stage 1 is CLOSED. Next: the design of the MPB set with Hadi. Open for it: a setup with pallets
already in a bay while the robot delivers others; the robot's last task as a return (the PROPOSAL of the second
milestone's findings); how expected decisions are derived when the human's sequence depends on the robot's decisions
(C6).

RULED (Hadi, 2 October 2026; recorded in T-G records 10, 2 October 2026): THE MPB ON DOCK_LOADING, its design, ruled as
one package (MPB-DL1 to MPB-DL6; the labels are this block's, distinct from kitting's MPB-1 to MPB-6). Records only;
nothing in this block is built. The MPB of stage 1 is a test and an analysis; it changes nothing in the framework. The
scenario set itself is not yet agreed and is not recorded here. "As kitting's MPB rules" refers to "The meta-planner
test-bed (MPB)".
- MPB-DL1, the claim.
  The MPB on dock_loading has two parts.
  Part 1: a few of kitting's decision paths re-instantiated on dock_loading.
  Part 2: one scenario for each case that dock_loading adds:
  (i) a hypothesis that enters the live set during the run through the robot's own act (a scan becomes live when the
      robot puts the pallet down; liveness by applicability, A4);
  (ii) decisions on the fallback projection as the frequent case;
  (iii) two hypotheses with the same motion waiting in one bay, so that the gate refuses during the walk;
  (iv) an admission that is correct by the records and wrong about the human (the walk to the standby place admitted as
       a break). The expectation states that admission before the run. The run agreeing with it is not a disagreement;
       the wrong reading is a finding about the mind (TODO-155, Q16);
  (v) the human in another area (the office), with methods selected by area (B11);
  (vi) the robot and the human at the same bay while the robot has an alternative task;
  (vii) a human's script that depends on the robot (Q13b).
  The set does not claim full coverage of the decision paths on dock_loading. Kitting's coverage matrix
  (analysis/kitting/mpb/coverage.md) is not repeated.
  Reason: T-G tests that the chain stays domain-independent. The chain's code is shared, and its paths are verified on
  kitting. A second full matrix would test the same paths again.
  AMENDED (Hadi, 2 October 2026; T-G records 11; DISPOSITIONS, D4): cases (i) and (vii) are mixed scenarios with
  declared properties. Reason: the entry tick of the scan is the robot's delivery tick, which is not derivable before
  the run.
- MPB-DL2, a new setup kind per room, for the MPB's controlled scenarios.
  The setup: one full unscanned pallet already in each delivery bay, designated to the bay it stands in; one full pallet
  in the truck designated to each delivery bay; two empty pallets in the empties container, designated to the truck.
  The human scans only the pallets that stand in the bays at the start.
  A meeting at a bay is authored by a stand or a break at the bay. Its timing is computed from path lengths before any
  run.
  Reason: in setup kind 2 (B14) a scan becomes applicable only at the robot's delivery, so the human's script depends on
  the robot. A round trip to the truck (about 96 ticks) is longer than a scan (16 to 30 ticks), so the robot never
  arrives at a bay where the human stands (the second milestone scenario). Pallets already in the bays give a script
  that is independent of the robot.
  The kind recorded earlier as conditional (B14: all full pallets designated to one bay, added only if the first MPB run
  calls for it) keeps its condition.
  The names of the new kind and of the conditional kind are not ruled. The records step proposed names in its report
  (T-G records 10); nothing that exists is renamed.
  AMENDED (Hadi, 2 October 2026; T-G records 11; DISPOSITIONS, D2), a correction before any run: the new kind has two
  full unscanned pallets in each delivery bay at the start, not one, each designated to the bay it stands in. Reason:
  the same-motion case (MPB-DL1 (iii)) needs two scans in one bay; with one pallet per bay it cannot be a controlled
  scenario. A scenario that assigns one scan per bay is unaffected: the other pallet's scan is outside the support.
  CORRECTED (the same ruling; DISPOSITIONS, D3): "a break at the bay" is withdrawn; no break ends at a bay. The meeting
  at a bay has two forms. Form 1: the human walks to the bay on an admitted scan while a delivery of the robot goes to
  that bay. Form 2: the human stands at the bay after a scan (a `stand`, unmodelled behaviour), and the robot decides on
  the fallback projection.
  NAMED (the same ruling; DISPOSITIONS, D7): the new kind is kind 3, "pallets in the bays"; the conditional kind is kind
  4, "one bay". Two setups of kind 3, for env_layout_03 and env_layout_04 (D6).
- MPB-DL3, expected decisions. It answers, for stage 1, the third clause of C6: how the MPB's oracle derives an expected
  decision when the human's sequence depends on the robot's decisions.
  - Controlled scenarios: scripts independent of the robot only. Full expectations (trigger and cause, gate,
    projection) are committed before the run, as kitting's MPB rules (MPB-1, MPB-3).
  - Mixed scenarios: a script that depends on the robot is allowed. Properties are declared before the run and checked
    on the run. This is the weaker check. Those runs do not validate the recognizer's decisions, and no record may claim
    that they do.
  - Not taken: a check per decision derived from the logged state at the decision tick. Reason: it conditions on the run
    and needs new instrument code.
  AMENDED (Hadi, 2 October 2026; T-G records 11; DISPOSITIONS, D1 and D5): the controlled scenarios are also bound by
  the disjointness rule (MPB-DL7). A mixed scenario is either dependent on the robot, on kind 2, with declared
  properties, or independent of the robot, on kind 3, with full expectations committed before the run. Each scenario
  states its kind.
- MPB-DL4, the robot's last task.
  The proposal "an authoring convention that the robot's last assigned task is a return" (FINDINGS OF THE SECOND
  MILESTONE SCENARIO; TODO-135's fourth instance) is CLOSED, NOT TAKEN.
  Reason: the robot's pool is unordered and the meta-planner selects by cost, so an author cannot fix the last task
  without constraining the selection.
  In its place the MPB reports, per room, the ticks below the minimum separation with a standing robot, beside the
  violations with a moving robot. These counts serve Hadi's later ruling on whether to reopen TODO-135. Nothing is ruled
  on TODO-135 itself.
- MPB-DL5, office_break stays at 90 seconds for the MPB (B6's note).
  Reason: no value is changed for a test set.
- MPB-DL6, strategies and rooms.
  `single_task` is primary and `full_reorder` is the second run, as kitting's MPB rules (MPB-6).
  The set runs in two rooms, env_layout_03 and env_layout_04.
  env_layout_02 is excluded as a reduction of scope, not because it is irrelevant. Its condition of late admission (the
  coffee machine lies in the direction of the walk from the dry bay to the frozen bay; median delay 28 ticks in the IRB) remains untested by the MPB.
  Reason for the two rooms: env_layout_03 has frequent admissions and env_layout_04 rare ones (in the IRB's
  baseline, 40 and 20 of 49 stretches reach the threshold), so they give decisions on an admitted projection and on the
  fallback projection.
  Planned size: about 8 controlled and 4 mixed scenarios, 48 runs (two rooms, two strategies). The set is agreed with
  Hadi before it is authored.
  CORRECTED (Hadi, 2 October 2026; T-G records 11; DISPOSITIONS, D8): env_layout_04 also has the frozen bay and the
  coffee machine in one direction from the standby place. The late-admission condition is untested by the MPB only for
  the walk from the dry bay to the frozen bay in env_layout_02.
  SUPERSEDED (the same date; THE SET below): the planned size reads 9 controlled and 4 mixed scenarios, 52 runs.
- MPB-DL7, the disjointness rule (Hadi, 2 October 2026; T-G records 11; DISPOSITIONS, D1). An authoring constraint of
  the controlled scenarios, checked per scenario before its runs: no pallet is named both by the robot's pool and by an
  assigned scan of the human.
  Reason: under it, with the prior on, no act of the robot changes the live set, the belief or the adequacy of a
  hypothesis in the support (the records step's answer, T-G records 10: a scan reads `in_area` of the human and
  `obj_at` of its own pallet; the robot moves only the pallets of its pool; inadmissible hypotheses are skipped before
  the applicability check and stay pinned; the terminal facts, the boundary, the excess path, the standing and the
  warrant are the human's own). It is the dock_loading form of kitting's rule (MPB-3).
  It holds for controlled scenarios only. It is not generalised to mixed scenarios, where a delivery changes
  applicability.
DISPOSITIONS ON THE FLAGS OF T-G RECORDS 10 (Hadi, 2 October 2026; recorded in T-G records 11). D1 to D10 are Hadi's
numbers; each is recorded where it applies:
- D1, the disjointness rule: MPB-DL7.
- D2, kind 3 with two pallets in each delivery bay: MPB-DL2, AMENDED.
- D3, "a break at the bay" withdrawn, the two forms of the meeting at a bay: MPB-DL2, CORRECTED.
- D4, cases (i) and (vii) mixed: MPB-DL1, AMENDED.
- D5, a dependent mixed scenario on kind 2, an independent one on kind 3 with full expectations, each scenario stating
  its kind: MPB-DL3, AMENDED.
- D6, two setups of kind 3, for env_layout_03 and env_layout_04: MPB-DL2, NAMED.
- D7, the names, kind 3 "pallets in the bays" and kind 4 "one bay": MPB-DL2, NAMED; B14's "a third kind", READS.
- D8, the late-admission condition: MPB-DL6, CORRECTED.
- D9, kind 3 is a test condition. No record describes the runs on kind 3 as the domain's work cycle: the pallets the
  robot delivers there are never scanned (B1's reading is the work cycle; M1 below is the set's instance of it).
- D10, the glossary: controlled scenario, mixed scenario, setup kind, disjointness rule, declared property, each
  defined from its use in the records (`docs/glossary.md` §9).
THE SET (agreed by Hadi, 2 October 2026; recorded in T-G records 11). Records only; nothing is authored or run. 9
controlled scenarios (K1 to K9) and 4 mixed (M1 to M4; this set's, distinct from the IRB's M1 to M4 above),
each in env_layout_03 and env_layout_04, prior on, `single_task` primary and `full_reorder` second: 52 runs.
Common to all: the human starts at the standby place and closes at the desk (B13); the robot starts on the truck side.
On kind 3, pallet_0 and pallet_1 stand in the dry bay and pallet_2 and pallet_3 in the frozen bay. "scan n" is
`confirm_delivered_pallet` of pallet_n. The robot's tasks on kind 3 are deliver-dry and deliver-frozen (the two truck
pallets), return-1 and return-2 (the two empty pallets). Where no assignment is named, the human's assigned tasks are
the script's scans. Every duration and cut point is derived from path lengths before any run, in the build's plan, and
approved by Hadi; the plan shows per room that the geometry gives the declared case.
Controlled (kind 3, a script independent of the robot, the disjointness rule, full expectations before the run):
- K1, the control. Human: scan 2. Robot: deliver-dry, return-1. Tests: no hold at any decision; completion equal to a
  comparison run with the same setup, pool and start and no human.
- K2, admission and the admitted projection (meeting form 1). Human: scan 0, scan 2. Robot: deliver-dry,
  deliver-frozen, return-1. Tests: the decision at the tick the gate clears, against the human's projected walk to the
  bay the robot delivers to.
- K3, the stand at a bay with an alternative task (meeting form 2). Human: scan 0, then a long `stand` at the dry bay.
  Robot: deliver-dry, deliver-frozen, return-1. Tests: decisions on the fallback projection of a standing human, the
  `projection_expired` cadence, the switch by cost.
- K4, the stand at a bay with no alternative. As K3; the robot's pool is deliver-dry only. Tests: the robot holds; the
  holds lengthen at each expiry.
- K5, the same motion. Human: scan 0, scan 1. Robot: deliver-dry, deliver-frozen, return-1. Tests: the gate refuses
  during the walk; the robot decides on the fallback projection of a walking human; scan 1 is admitted alone after
  scan 0.
- K6, a foreseeable task between scans. Human: scan 0, coffee_break, scan 2. Robot: all four tasks. Tests: admission
  on observation warrant during the break walk; the boundary and the re-admission after it.
- K7, the office. Human: scan 0, office_break, scan 2. Robot: all four tasks. Tests: the admitted projection through
  the office door; the robot's decisions while the human is in another area.
- K8, the change during an action. Human: scan 0 with coffee_break cut into its walk; scan 2. Robot: deliver-dry,
  deliver-frozen, return-1. Tests: retraction, the fallback projection after it, re-admission.
- K9, the admission that is wrong about the human. Human: assigned scan 0 only; script: scan 0, `go_to(standby_place)`
  as an ordinary entry, a `stand` there, the desk. Robot: deliver-frozen, return-1. Tests: the walk to the standby
  place admitted as a break (expected so, by the records), the robot's decision against it, the retraction when the
  human stands. The run agreeing with the expectation is not a disagreement; the wrong reading is a finding about the
  mind (MPB-DL1 (iv)). The script has no entry that waits for the robot. The repeatable standby entry is exercised in
  M1, M2 and M4.
Mixed (read only against the controlled ones):
- M1, the domain's work cycle. Kind 2, dependent. Human: the scans of the four delivered pallets, the standby entry.
  Robot: four deliveries, two returns. Declared properties: every robot task completes; every script entry closes; no
  violation with a moving robot; each scan enters the live set on its delivery tick.
- M2, pallets accumulate. Kind 2, dependent. As M1, with office_break after the first scan. Declared properties: as
  M1, plus two scans applicable at once in one bay, and the robot's decision at an occupied bay.
- M3, combined deviations. Kind 3, independent, full expectations. Human: scan 0 with coffee_break on arrival; scan 1;
  scan 2; a `stand` at the frozen bay. Robot: all four tasks. Combines K5, K6 and K3.
- M4, a dropped scan in the work cycle. Kind 2, dependent. Human: the first scan dropped during its walk;
  coffee_break; the other scans; the dropped scan as a second entry; the standby entry. Robot: as M1. Declared
  properties: as M1.
Rules of the set:
- The controlled scenarios run and are read first.
- Nothing is adjusted to a result.
- Findings are classified: kitting's five disagreement classes and the three readings of class 2 carry over (MPB-4).
- The mixed runs with declared properties do not validate the recognizer's decisions (MPB-DL3).
- Every run reports the separation counts: violations with a moving robot, and ticks below the minimum separation with
  a standing robot (MPB-DL4).
Not in the set: env_layout_02 (MPB-DL6); a dropped scan as a controlled scenario.
RULED ON THE SET (Hadi, 2 October 2026; recorded in T-G records 12): the flags of T-G records 11. Records only; nothing
is authored or run.
- The case per room, a principle of the set. A scenario runs in both rooms. Where the records predict that its case
  does not form in a room, the expectation for that room says so before the run. The case counts as tested only where
  it forms. Nothing is changed to make it form.
  Reason: a case engineered into existence tests the engineering, not the chain.
- K2: unchanged. On env_layout_03 it shows the decision at admission. On env_layout_04, where the records predict no
  admission, it shows a decision on the fallback projection.
- K5, AMENDED: the clause "scan 1 is admitted alone after scan 0" is withdrawn. K5 tests the refusing gate and the
  fallback projection.
  Reason: the second scan has no walk and never reaches the threshold in the IRB.
- K8, AMENDED: the cut comes after the tick at which the oracle expects scan 0's admission, derived before the run. The
  retraction forms on env_layout_03 only.
- K9, AMENDED: the human's scan is scan 2 (pallet_2, the frozen bay); the robot's pool is deliver-dry and return-1.
  Reason: the IRB admitted the walk from the frozen bay to the standby place as a break in every room.
- K1, AMENDED: the control requires that the human works away from every robot route. The build's plan selects, per
  room, the scan and the robot's pool that satisfy this and shows the derivation. If no pairing exists on
  env_layout_04, K1 runs on env_layout_03 only, and the record says so.
- K4: the lengthening holds are evidence for TODO-132 (a), not a verified rule.
- M2, AMENDED: office_break is an event on one named scan entry. "Two scans applicable at once in one bay" and "the
  robot's decision at an occupied bay" are not declared properties, because they depend on the order the robot chooses
  by cost. The report states whether each occurred.
- M4, AMENDED: one named scan is dropped during its walk; a second named scan has coffee_break on arrival; the dropped
  scan is a second entry; the standby entry closes the list.
THE BUILD'S PLAN, CONFIRMED (Hadi, 2 October 2026; recorded in T-G records 13): ccode's plan for the MPB set (its
sections a to i: the setups env_setup_08 and env_setup_09 of kind 3; the scenarios scenario_s08_01 to _10 and
scenario_s09_01 to _10 (K1 to K9, M3), scenario_s05_04 to _06 and scenario_s07_04 to _06 (M1, M2, M4); the authored
durations; the instrument's generalisation; the order of the build) with the dispositions below on its open points.
- DL-P1, K8's cut, by a rule: the cut falls on the last step of the walk to the pallet, in both rooms. The cause is
  whatever the oracle derives on kind 3; it is not inferred from the IRB's rows on kind 1.
  Reason: it is the latest change that is still a change during the walk, so scan 0 has received all the walking
  evidence it can receive.
  Procedure, before any controlled run: K8's per-tick table is reported for both rooms, from scan 0's expected
  admission (or the walk's start if none) to 10 ticks after the cut: the leader, scan 0's share, scan 0's hypothesis
  adequacy, the gate's outcome and the expected cause of each decision. On env_layout_03, if the oracle expects the
  retraction, the build proceeds; if it expects "replaced" or no admission, the build stops before the controlled runs
  and reports; no other cut is tried; Hadi rules. On env_layout_04 there is no stop: K8 runs, and if the case does not
  form the expectation and the record say so for that room.
- DL-P2, K3's switch by cost is neither an expectation nor a declared property. K3's exact parts are the fallback
  decisions on the standing human and the expiry cadence. The report states whether the switch occurred and, if it
  did, checks the occupied-target condition (X1). The stand is not lengthened to force it.
  Reason: the selection depends on the robot's realized state; the records do not determine it.
- DL-P3, K1 on env_layout_04 runs with its one-task pool (the human's scan 0, the robot's deliver-frozen).
  Reason: a control needs no hold and an equal completion, not a selection between tasks.
- DL-P4, K9 on env_layout_04: if a `no_current_task` tick masks the retraction (D3's order on a shared tick), the case
  counts as not formed there. Nothing changes.
- DL-P5, the closing walk to the desk admitted as a break is expected by the oracle and is not a disagreement. Each
  instance is recorded as a finding about the mind, with TODO-155.
- DL-P6, admissions near the threshold: the oracle's computed table decides every tick. No hand-derived tick of the
  plan is binding.
- DL-P7, the step cap for a script that depends on the robot (an extension of MPB-5 for this set): the robot's plain
  chain, plus the human's replay on the state after that chain, plus 30 ticks. It bounds the run's length and is not
  an expectation. A run that reaches the cap is reported as such; the cap is not raised after a run.
- DL-P8, a condition on the instrument: dock_loading's horizon code may call the planner's decomposition for the cap
  only. The report shows that no module of the oracle (the per-tick tables, the chain assembly, the compare) imports it
  or anything of the planner, the recognizer, the projection or the robot's perception.
  READ (Hadi, 2 October 2026; recorded in T-G records 15): the condition reads as kitting's MPB-1 reads. The oracle may
  use the task model's decomposition. No module of the oracle imports the cap code (horizon.py). No stricter reading.
- DL-P9, the alteration E3 (every support key live whatever its applicability, T-G A4 switched off in the oracle): if
  undetected on the controlled set, it is recorded as a property of the set with its reason.

SCOPE REDUCED AND THE MPB ON DOCK_LOADING RUN (Hadi, 2 October 2026; recorded in T-G records 14). Hadi reduced the scope
of stage 1's MPB: it establishes that the recognizer and the recognition-to-planning chain run on dock_loading and
produce runs, logs and figures; the behavioural analysis belongs to stage 2. The stop for review between the controlled
and the mixed runs was withdrawn; a class-2 disagreement no longer stops the build (reported with its evidence); the
alteration test on dock_loading is not run in stage 1. Reason: stage 1's purpose is that the chain runs on the second
domain; the deeper analysis needs stage 2's room and tasks.
- What ran: the 26 scenarios of the set (K1 to K9 and M3 on kind 3, scenario_s08_01 to _10 and scenario_s09_01 to _10;
  M1, M2, M4 on kind 2, scenario_s05_04 to _06 and scenario_s07_04 to _06), in env_layout_03 and env_layout_04, prior
  on, single_task and full_reorder: 52 runs, every one completed within its cap; and K1's 4 comparison runs. The
  expectations and K8's table were committed before any run (8fb9981).
- Where: analysis/dock_loading/mpb/ (README.md, authoring.md, predictions.md, REPORT.md with every run's line and the
  md5s; per run the comparison, the properties, the figures and the separation counts; the logs and records in runs/,
  git-ignored); the run files in configs/dock_loading/mpb/; the instrument's shared code in analysis/instruments/mpb/.
- The comparison: the 40 runs with full expectations (K1 to K9, M3) agree with the oracle on parts 1 to 3 at exact
  equality, 0 disagreements; no class-2 disagreement. K1's properties hold against the comparison runs. The mixed
  runs M1, M2, M4 (declared properties only, MPB-DL3): (i), (ii) and (iv) hold in every run; (iii), no violation with a
  moving robot, does not hold in env_layout_04 under single_task (one violation at 387 in each; M2 also 224 to 226).
- Formed or not: K8's retraction formed on env_layout_03 (entered 14, retraction 34) and not on env_layout_04 (no
  admission of scan 0); K9's retraction formed on env_layout_03 (67) and on env_layout_04 under full_reorder (59);
  under single_task it was masked by the robot's no_current_task at 59 (DL-P4, not formed there); K2's admission of the
  scans did not form on env_layout_04; K3's switch by cost occurred on env_layout_04 (single_task at 104, full_reorder
  at 110), not on env_layout_03 (DL-P2: reported, not expected); K4's holds lengthened (13, 48, 96; 10, 48, 96); M2's
  two scans live at once in one bay did not occur; its decision at an occupied bay occurred in every M2 run.
- The walk to the desk (and K9's walk to the standby place) admitted as a break, a finding about the mind with TODO-155
  (DL-P5): coffee_break on env_layout_03 in K1, K2, K6, K7, K8, K9; office_break on env_layout_04 in K2, K6, K7, K8, K9.
- Not tested or not run: the alteration test on dock_loading (built, for stage 2); env_layout_02 (MPB-DL6); the cases
  listed above as not formed.
- Observations for stage 2, unanalysed: (1) M1, M2, M4 on env_layout_04, single_task: a hold of 6 decided at 382 on a
  moving fallback, scan 1 entered at 387 with hold 0, and a moving-robot violation at 387; (2) moving-robot violations
  in K8 full_reorder on env_layout_03 (2) and K9 single_task on env_layout_04 (2); (3) standing-robot ticks below
  min_separation (MPB-DL4, TODO-135's measure) in K3, K4, M3 and the mixed full_reorder runs, up to 15 with the human
  passing and 4 beside; (4) the switch while carrying in K3 on env_layout_04 returns the full pallet to the truck first
  (B8); (5) K9 on env_layout_04: the masking depends on the strategy; (6) the desk walk read as a break in most
  controlled runs; (7) M1 and M4 of one room end on the same terminal tick under each strategy.
- The instrument (no change of framework code): measures.py and the alteration engine shared; run.sh --expect and the
  control list per domain; a script that depends on the robot gets no oracle comparison and its human read from the
  run; dock_loading's horizon.py (DL-P7, DL-P8), properties.py, alteration.py, disjoint.py. Found on the way: HEAD's
  kitting alteration test failed since the IR oracle reads the layout's areas (its scratch copy's root); corrected in
  the shared engine, kitting's table reproduced exactly.
- The regression audit: byte-identical. Kitting's MPB (the sixteen, both strategies and prior off, after
  the generalisation; every committed output and md5; the alteration table), the reference set of stage 1 (the four
  maintained sweeps, the ten drop scenarios, kitting's IRB and MPB; the stdout files differ in the run-file
  paths only, as since the sort), dock_loading's IRB (54 runs, every output and md5); the suite 301 passed;
  every registered scenario of both domains loads (163).
CAVEAT (Hadi, 3 October 2026; design_decisions.md, "T-K: context knowledge in the recognizer's belief", AM3's C1; TODO-66). The results of the run files that last 500 steps or more,
and of the milestone runs, are potentially confounded by an undeclared weight: the present hardcoded context weight
(`_context_weight`) multiplies coffee_break by 2.5 from step 500 in every run, because the shift starts at step 0 and
the step count serves as the clock. They are not declared invalid. Identified by duration:
- the MPB on dock_loading: 11 run files in configs/dock_loading/mpb/, each run under both strategies (22 runs; every
  one reaches step 500): on env_layout_03, scenario_s08_06 (K6, 531 steps), scenario_s08_07 (K7, 548), scenario_s08_10
  (M3, 658), scenario_s05_04 (M1, 686), scenario_s05_05 (M2, 803), scenario_s05_06 (M4, 858); on env_layout_04,
  scenario_s09_07 (K7, 538), scenario_s09_10 (M3, 626), scenario_s07_04 (M1, 639), scenario_s07_06 (M4, 716),
  scenario_s07_05 (M2, 760);
- the milestone runs (headless, prior on): scenario_s03_02, scenario_s05_02, scenario_s07_02 (800 steps) and
  scenario_s03_03, scenario_s05_03, scenario_s07_03 (1000 steps), on env_layout_02, env_layout_03, env_layout_04.
One effect is demonstrated, as one case: in scenario_s03_03 (env_layout_02) the hypothesis with the highest belief
changes from office_break (0.602) to coffee_break (0.601) at step 500 with no new observation.
Not affected: kitting's maintained sets (they end by step 449) and every run of the IRB (kitting's and
dock_loading's run files end by step 331), so the recognition figures of the IRB stand.
T-G STAGE 1 CLOSED (Hadi, 2 October 2026; recorded in T-G records 15).
- Its purpose was an initial check that the recognizer and the recognition-to-planning chain run on dock_loading.
- Result: the 52 MPB runs completed; zero disagreements wherever full expectations exist; the regression audit
  byte-identical.
- This does not state that the scenarios are free of violations. The declared property "no violation with a moving
  robot" failed in three mixed runs (env_layout_04, `single_task`, tick 387), and controlled runs contain recorded
  separation violations. These are findings carried to stage 2, unanalysed. They do not reopen stage 1.
- Deferred to one housekeeping step, not done now: the sweep of old terms (TODO-153), the sizes of the files under
  docs/, and what of analysis/ stays in git.
  DONE (2 October 2026), the housekeeping step: the sweep of old terms ("zone" to "area" in wording; TODO-153 closed,
  1551d1c); the split of the records (docs/design_decisions.md holds the conceptual design of the shared core,
  docs/design_records.md everything else, one heading per task); the rule for analysis/ (git tracks reports and code
  only; data and figures stay on Hadi's disk; 7d00f43, 248a946). Open: the rewriting of each conceptual entry into one
  current rule (input: "Stale passages, input for a later consolidation" in this file); the destination of two old
  items under docs/ (the old ROS planner reference text, the folder of old layout pictures), deferred until Hadi names
  one.
- TODO-153, TODO-154, TODO-155 and TODO-156 are tagged [V1].

PROPOSALS (by the design chat, NOT RULED)
- An empty pallet's destination (the truck) as a designation in the setup, so that `load_return` reads `destination_of`
  and names no fixed object.
  RULED (Hadi and the design chat, 1 October 2026; recorded in T-G records 5), B14: the setup designates the truck as the destination of each empty pallet (one rule covers every
  pallet). How `load_return` reads it is for stage 1's plan.
- Two generic load checks in `shared/` that let malformed input through (TODO-151, recorded as a proposal, untagged).
- TODO-131 (the robot-mind object): A8's reduced form does not need it, so its landing in track 4 is no longer implied;
  its placement is open (TODO-131's note).
- Stage 1 may already use the room of B10, with the stores and the freezer present and unused.
  CLOSED, NOT TAKEN (Hadi and the design chat, 1 October 2026; recorded in T-G records 5), B14: B10's room moves to stage 2; stage 1 uses three rooms without stores.
- `pytest` over the whole repo stops on collection errors in `ros_sim/framework_HRI/test/` that predate build 1. Measured
  at 62ebc4e: three files (`test_copyright.py`, `test_flake8.py`, `test_pep257.py`; the `ament_*` modules are missing);
  the proposal named the first.

Reference: cchat, 30 September and 1 October 2026 (T-G); `docs/handoffs/handoff_T-G_onward.md`; ccode's dock_loading
survey (30 September 2026, not committed); "T-H: the human behaviour model"; "Layouts, setups and scenarios"; "An item's
destination table is a fact of the station"; "The successor state is derived from what the action schemas declare"; I2
("Targets, methods and completions are the planner's"); "T-D L" (L4); "T-D X" (X5); `docs/glossary.md` §6, §8, §9, §10;
`docs/assumptions.md` 2.3, 5.1 to 5.3; TODO-02, TODO-08, TODO-09, TODO-10, TODO-16, TODO-25, TODO-30, TODO-39, TODO-81,
TODO-96, TODO-97, TODO-104, TODO-131, TODO-140, TODO-143 to TODO-151; LIMIT-02 to LIMIT-05; DESIGN-01, DESIGN-02,
DESIGN-04, DESIGN-15; REFACTOR-03

Next: the layout and the setup of T-G's stage 1, agreed in the design chat; then stage 1's plan.
SUPERSEDED (T-G records 1, third follow-up, 1 October 2026): the order is the lifecycle question of the human's list
(A3, PARKED), then stage 1's layout and setup, then stage 1's plan.
SUPERSEDED (T-G records 2, 1 October 2026): the lifecycle question is ruled (A3, Q12 to Q15; B13). Next: stage 1's
layout and setup, agreed in the design chat, then stage 1's plan.
SUPERSEDED (Hadi and the design chat, 1 October 2026; recorded in T-G records 5): stage 1's rooms and setups are agreed (B14). Next: stage 1's plan.
SUPERSEDED (Hadi, 1 October 2026; recorded in T-G records 7): stage 1's plan is approved (STAGE 1 PLAN APPROVED above;
`docs/handoffs/plan_T-G_stage1.md`). Next: stage 1's build, step 0 then step 1 (the rename).
SUPERSEDED (records, 1 October 2026): steps 0 to 5 of stage 1 are built and accepted (STAGE 1, STEPS 0 TO 5 BUILT
above). Next: the domain steps, step 6 (the catch-up) and step 7 (the content), then the milestone (step 8).
SUPERSEDED (records, 1 October 2026): steps 6 to 8 of stage 1 are built and the milestone accepted (STAGE 1, STEPS 6
TO 8 BUILT above). Next: the second simple scenario per room; then the sorting of the earlier analyses and tests under
kitting, with the preparation of the instruments; then the IRB scenarios, agreed with Hadi before they are
authored.
SUPERSEDED (records, 1 October 2026): the second milestone scenario is built and accepted, and stage 1's milestone is
complete (STAGE 1, THE SECOND MILESTONE SCENARIO BUILT above). Next: the design of the IRB set with Hadi (first
question: TODO-155); then the sorting of the earlier analyses and tests under kitting, with the preparation of the
instruments; then the set's authoring and its runs.
SUPERSEDED (Hadi, 1 October 2026; recorded in T-G records 8): TODO-155 is ruled for now (T-G Q16: the walk stays without
a hypothesis) and the IRB set on dock_loading is agreed (T-G Q16's block above, RULED). Next: the build step that
sorts the earlier analyses and tests under kitting and prepares the instruments for dock_loading; then the authoring of
the set, its expectations and its runs.
SUPERSEDED (records, 2 October 2026; T-G records 9): the sort, the instruments' preparation, office_break at 90 seconds,
the 54 scenarios, their expectations and the 54 runs are built and accepted, and the IRB of stage 1 is closed
(STAGE 1, THE IRB ON DOCK_LOADING BUILT, RUN AND ACCEPTED above). Next: the design of the MPB set with Hadi.
SUPERSEDED (Hadi, 2 October 2026; recorded in T-G records 10): the design of the MPB on dock_loading is ruled (THE MPB ON
DOCK_LOADING above, MPB-DL1 to MPB-DL6). Its three open points are answered: the setup with pallets already in the bays
(MPB-DL2); the robot's last task as a return, not taken (MPB-DL4); expected decisions when the human's sequence depends
on the robot (MPB-DL3). Next: the MPB set's scenarios, agreed with Hadi before they are authored.
SUPERSEDED (Hadi, 2 October 2026; recorded in T-G records 11): the dispositions on the flags are recorded and the MPB
set on dock_loading is agreed (THE MPB ON DOCK_LOADING above: MPB-DL7, DISPOSITIONS, THE SET; 13 scenarios, 52 runs).
Next: the build's plan (the two setups of kind 3, the scenarios, every duration and cut point derived from path lengths,
the per-room derivation that the geometry gives each declared case), approved by Hadi before the build.
SUPERSEDED (Hadi, 2 October 2026; recorded in T-G records 14): the build's plan was confirmed (DL-P1 to DL-P9), the
scope of stage 1's MPB reduced, and the MPB on dock_loading built and run (THE MPB ON DOCK_LOADING above, SCOPE REDUCED AND
THE MPB ON DOCK_LOADING RUN; 52 runs; the 40 with full expectations agree with the oracle). Next, as Hadi rules: the
close of stage 1 (handoff_T-G_stage1_MPB_onward.md, section 6).
SUPERSEDED (Hadi, 2 October 2026; recorded in T-G records 15): T-G stage 1 is closed (T-G STAGE 1 CLOSED above). Next:
to be named by Hadi.
SUPERSEDED (Hadi, 2 October 2026; the heading "T-K" below): the task named is T-K, part 1 next, and its design is
ruled. Next: its three open items, then its build's plan.

## T-K: context knowledge

**T-K: context knowledge in the recognizer's belief (ruled by Hadi, 2 October 2026)** — RECORD [T-K/1], written 2 October 2026; the conceptual part (R1 to R8, the assumptions A1 to A7) is in docs/design_decisions.md under this title.
Ruled in cchat, 2 October 2026; recorded before any build. Nothing is built.
AMENDED (Hadi, 3 October 2026, on the review of the records): AM1 to AM9 in design_decisions.md under this title; here
R9 superseded by AM3, AM3's consequences and AM8.
AMENDED (Hadi, 3 October 2026, the design chat on content points 1 and 2): AM10 to AM29. Their conceptual part is in
design_decisions.md under this title; here the record part (CONTENT POINTS 1 AND 2, below), the cut and T-K part 2's open
items as amended, and the open items' state.
AMENDED (Hadi, 3 October 2026, content point 3, the tests): CONTENT POINT 3, THE TESTS (below), KT1 to KT7. Its
conceptual part, AM34 (the setup holds the timeline of context facts), is in design_decisions.md under this title,
under AM11.
AMENDED (Hadi, 3 October 2026, the design chat on the rest of T-K part 1, the form and the values of the strengths;
recorded 4 October 2026): AM35 to AM39. Their conceptual part (AM35 the name, AM36 the three levels, AM39 the reading
of a strength) is in design_decisions.md under this title, under R3; here AM37 the declarations (under AM13), AM38 the
values and their sources (under AM17), and the block THE STRENGTHS REVISED (below).
AMENDED (Hadi, 4 October 2026, the design chat; AM40, AM41): where the timeline of context facts is stated. Their
conceptual part is in design_decisions.md under this title, under AM11's AM34; here KT13 and KT14, in the block THE
TIMELINE IN THE SCENARIO (after KT12).
AMENDED (Hadi, 4 October 2026, on ccode's plan of the build; AM42 to AM53): the plan's decisions. The conceptual part
(AM42, AM44, AM46, AM47, AM50, AM52) is in design_decisions.md under this title; here the block THE BUILD'S PLAN, RULED
(after THE TIMELINE IN THE SCENARIO).
AMENDED (Hadi, 4 October 2026, on ccode's cross-check of the plan's rulings; AM54 to AM58): AM54 is in
design_decisions.md under this title, under R1; here the block THE CROSS-CHECK, RULED (after THE BUILD'S PLAN, RULED).
AMENDED (Hadi, 4 October 2026, step 5; AM66, KT15): question G ruled, its conceptual part in design_decisions.md
under this title, under R7; here QUESTION G, RULED, THE PLANNING CASES, RULED (KT15), STEP 5B, PLANNED and STEP 5,
STAGE 1: THE PROPOSAL (at the end of this heading); STEP 5B's result: STEP 5B, KITTING, THE EXISTING SETS WITH
CONTEXT KNOWLEDGE ON: DONE (the heading's last entry).

R9. The support restriction (the switch named `assignment_prior`) is on by default for every further analysis and test
in V1. The robot without knowledge of the assignment is future work (TODO-162). Recorded only: the run option's default
(`configs/experiment.yaml`, false; TODO-139) is not changed now.
SUPERSEDED (AM3, Hadi, 3 October 2026; design_decisions.md, this title, R3's AM3): R9 is replaced by two independent run
options, both on by default, assignment knowledge (the support restriction, today's switch `assignment_prior`) and
context knowledge; their names are `assignment_knowledge` and `context_knowledge` (AM9). Each "off" setting is an
ablation or a diagnostic; the default configuration is the framework as designed. The robot without knowledge of the
assignment is no future-work direction any more: R3's formula covers the case (TODO-162, superseded).
AM3's CONSEQUENCES, recorded, not acted on:
- the default change of both options belongs to the build (today `assignment_prior` defaults to false, TODO-139;
  `context_knowledge` does not exist);
- at the build, every existing baseline set and test either states "context knowledge off" to stay identical, or is
  regenerated with the reason stated, with the regression audit CLAUDE.md requires;
- the rename of `assignment_prior` to `assignment_knowledge` in code, configuration and commands belongs to the build,
  with the regression audit (AM9); older records keep the old name.
- CORRECTED (C1, Hadi, 3 October 2026): "context knowledge off" differs from today's behaviour in runs of 500 steps or
  more (the hardcoded context weight's long-shift rule, reached by step count); the second consequence above covers
  them. The runs concerned: the heading "T-G stage 1", SCOPE REDUCED AND THE MPB ON DOCK_LOADING RUN,
  its CAVEAT.
TO UPDATE AT THE BUILD (Hadi, 3 October 2026; NOT NOW): `docs/assumptions.md` 1.4 (the option's default, still off,
and the maintained sets running both settings) stays as it is until the build changes the default.

THE CUT AND THE QUEUE.
- T-K part 1 builds: R1 to R4, R6, R7, crisp context facts, the scenario's timeline of context facts, and the
  removal of the domain task names and constants from the recognizer (TODO-66; T-K part 1's build closes it).
  AMENDED (AM34, Hadi, 3 October 2026; content point 3): "the scenario's timeline of context facts" reads "the setup's
  timeline of context facts" (CONTENT POINT 3, THE TESTS, KT4, below).
  AMENDED (AM40, Hadi, 4 October 2026): the setup's timeline is the default; a scenario may state its own, which
  replaces it whole (design_decisions.md, this title, AM11's AM40; THE TIMELINE IN THE SCENARIO, below).
  AMENDED (Hadi, 3 October 2026; AM10 to AM29): the build also contains "not" in an occurrence condition and its three
  sources (AM11: timeline facts, object states, recency facts); the recency facts and their memory of observed
  completions (AM14, AM27); the A/C switch's object state ac_on, and ac_activation with room_warm in both domains
  (AM18); the timeline's facts carried by the world state (AM25); the declared context knowledge from the knowledge
  component (AM26), which replaces the class `ContextKnowledge` in `shared/knowledge.py` (glossary §5, context
  knowledge); the removal of the long-shift rule with nothing in its place (AM22). Before the build, in its own step:
  the layouts with more than one A/C switch (AM19).
  SUPERSEDED IN PART (AM36, Hadi, 3 October 2026): the build contains no "not". It contains the suppressing condition
  and the raising condition of each foreseeable task, each one fact or a conjunction of facts over the three sources,
  and the three levels of a strength.
  AMENDED (Hadi, 3 October 2026; AM30, AM33): the memory of observed completions is its own component of the robot's
  mind, outside the recognizer, and records the tick of an observed completion; an observed completion is the task's
  terminal fact in the robot's world state (design_decisions.md, this title, AM27's AM30 and AM33).
- T-K part 2 holds the build of R5 (degrees: membership functions, the operators, the linear rule for a
  strength). Its place: the end of the V1 queue, after track 3b (roadmap, "The plan from T-A", the order block;
  CLAUDE.md's state). The letter T-K was verified unused in the repository before it was taken (2 October 2026).
  T-K part 2's operators include "or" and "not" in an occurrence condition; T-K part 1's occurrence condition is a conjunction
  (AM7).
  SUPERSEDED IN PART (AM11, Hadi, 3 October 2026): "not" is in T-K part 1; T-K part 2's operators keep "or" (and the degrees).
  SUPERSEDED IN PART (AM36, Hadi, 3 October 2026): "not" is T-K part 2's again; T-K part 2's operators hold "or" and
  "not" (and the degrees).
  T-K part 2's OPEN ITEMS (AM8, Hadi, 3 October 2026): the representation of a context value and of a degree. The fact form of
  T-G A5 holds crisp facts only.
  ADDED (Hadi's ideas and open items, the design chat of 3 October 2026; NOT RULED):
  - Soft edges of a window; a gradual return of the strength after a task (a membership function over the time since
    the last observed completion). T-K part 1's facts are crisp (AM10).
  - "Or" in an occurrence condition, with "long work without a break". Open with it: what counts as a break, when the
    count starts, its limit and its source, the unobserved human. T-K part 1 has no replacement for the long-shift rule
    (AM22).
  Open, also part 2's: whether succession between tasks affects the division inside work as a whole (R4), after T-G
  stage 2, to be argued with `store_pallet` present.
  OPEN (AM36, Hadi, 3 October 2026): the linear rule "strength = low + degree × (high − low)" (R5) was stated for the
  pair of a low and a high strength. It is restated for two conditions (the suppressing condition and the raising
  condition).
- Future work, each a TODO tagged [FW]: duration uncertainty and a projection that depends on context (TODO-158);
  unobservable states of the human as context (TODO-159); scopes of knowledge (general, sector, domain) and norms
  (TODO-160); validation of the strengths on site data (TODO-161); the robot without knowledge of the assignment
  (TODO-162).
  SUPERSEDED IN PART (AM3, Hadi, 3 October 2026): the last item; TODO-162 is marked superseded (R3's formula covers the
  case with assignment knowledge off).
  ADDED (Hadi, 3 October 2026; the design chat on content points 1 and 2): A/C deactivation (TODO-163); several A/C
  switches in one layout (TODO-164).
  Also future work: the stream of context values as the world's evolving state at each tick. The environment updates a
  value through its dynamics (the A/C lowers the temperature); the robot derives graded facts from the values. A sketch
  from the chat, not ruled: a crisp condition as an interval on one value. It needs a model of the world's physics, and
  nothing that V1 claims depends on it. T-K part 1 did not take the stream in place of the timeline of facts (AM11's
  "Not taken").

OPEN ITEMS OF T-K PART 1 (recorded as open; nothing decided):
1. The values for the two domains: the context facts, each foreseeable task's occurrence condition, its strengths and
   their source. Hadi states them.
   RULED (Hadi, 3 October 2026): AM10 to AM24 (design_decisions.md, this title, CONTENT POINTS 1 AND 2; the values in
   CONTENT POINTS 1 AND 2 below).
2. The perception assumption: how the robot obtains a context value.
   RULED (Hadi, 3 October 2026): AM25 to AM28 (the timeline's facts known exactly and at once, through the world state;
   the declared knowledge from the knowledge component; a recency fact from the mind's memory of an observed
   completion; the placement in `docs/assumptions.md`). Same places.
3. The tests of T-K part 1: a script that agrees with an occurrence condition, a human who acts against it, a duration
   mismatch.
   OPEN (3 October 2026). ccode's check of the authorable waits is recorded with it (AM29, below).
   HADI'S DIRECTION (3 October 2026; NOT RULED): the tests start on kitting, then cover dock_loading's stage 1
   scenarios, with what dock_loading's layouts and scenarios need for context knowledge. The re-measurement of stage
   1's baseline is that dock_loading part.
   RULED (Hadi, 3 October 2026): CONTENT POINT 3, THE TESTS, below (KT1 to KT7). Of the three cases above, the script
   that agrees with an occurrence condition and the human who acts against it are tested through where a foreseeable
   task is placed against the setup's timeline (KT3, KT4); the duration mismatch waits for a later set (KT3).

NOTES FOR THE BUILD'S PLAN (Hadi, 3 October 2026; confirmed on ccode's report of the records of content points 1 and 2;
not rulings of design):
- "not" in an occurrence condition (AM11) needs a condition form of its own; ccode proposes it in the build's plan.
  (The code's `ConditionSchema` has no negation flag, by its own comment.)
  SUPERSEDED (AM36, Hadi, 3 October 2026): T-K part 1 builds no "not"; no form for "not" is needed.
- ac_on (AM18) needs a declared state and a declared effect of the action; dock_loading needs the object type and the
  task ac_activation.
- Recency durations (AM16) are declared in physical time and converted by the body.
- ADDED (the design chat, 3 October 2026): the instruments are part of the build's plan. The IRB's expectations must
  be computed with the new prior (the oracle assumes the equal prior and ω = 1 today); its report must read the three
  conditions A, B and C (KT11); the A/C's measure is its belief at its arrival (KT10). The plan states what this costs.
- OPEN (Hadi, 3 October 2026; THE STRENGTHS REVISED, below): which value the gate compares with the threshold, the
  belief over the live hypotheses or the output after its scaling by the pinned hypotheses. It is a design question,
  argued from what each value means. The plan reports the facts of the code. It is not settled by whether a given
  value passes.
  RULED (AM42, Hadi, 4 October 2026): the belief over the live hypotheses (design_decisions.md, this title, under R7).
- ADDED (Hadi, 4 October 2026): the statement of the prior that the plan reads is `docs/context_knowledge_method.md`
  (THE STRENGTHS REVISED, below, F).

Also recorded: the open questions of C1, T-K PART 1 (the T-G heading above) are answered by the rulings, except the
liveness of a hypothesis whose condition turns false while the human executes its task, which is not answered (C1,
T-K PART 1, its RULED line). Hadi's earlier idea of a context fact that triggers or interrupts a task of the human is
superseded by R1 for T-K part 1 (`docs/handoffs/T-G_forward_inputs.md`, section 5, its dated note).

CONTENT POINTS 1 AND 2, RULED (Hadi, 3 October 2026; the design chat on T-K part 1's open items 1 and 2). Records only:
nothing is built, and no layout, scenario, test or analysis is changed. The conceptual part (AM10 every fact crisp;
AM11 the occurrence condition's three sources with "and" and "not"; AM12 context removes no hypothesis; AM14 recency
facts per task; AM20 no action changes a context fact; AM21 a fact is a state and its change no trigger; AM22 the
long-shift rule leaves with no replacement; AM25 to AM27 perception) is in design_decisions.md under this title,
CONTENT POINTS 1 AND 2. The chat's labels map in order: its A1 to A15 are AM10 to AM24, its B1 to B5 are AM25 to AM29.

- AM13, the occurrence conditions (the chat's A4). "recent" is the task's own recency fact (AM14):
  - coffee_break (kitting, dock_loading): break_time and not recent.
  - ac_activation (kitting, dock_loading): room_warm and not ac_on.
  - office_break (dock_loading): not recent. It has no timeline fact.
  break_time and room_warm are timeline facts (AM11); ac_on is the A/C switch's object state (AM18).
  SUPERSEDED (AM37, Hadi, 3 October 2026; the design chat on the rest of T-K part 1): the declarations under the three
  levels (design_decisions.md, this title, R3's AM36), the same in both domains where the task exists:
  - Suppressed strength 0.005. Ordinary strength 0.02. Each declared once per domain, for every foreseeable task.
  - coffee_break: suppressing condition, its recency fact. Raising condition, break_time, with the raised strength 2.
  - ac_activation: suppressing condition, ac_on. Raising condition, room_warm, with the raised strength 0.5.
  - office_break: suppressing condition, its recency fact. No raising condition.
  - The recency durations are unchanged (AM16): 90 ticks and 135 ticks.

- AM14, record part (the chat's A5): coffee_break and office_break each declare a recency fact, with its own recency
  duration. ac_activation declares none (ac_on covers it).

- AM15, the glossary (the chat's A6): new entries recency fact and recency duration; occurrence condition amended (a
  condition over context facts and object states, using "and" and "not"). The wordings are in `docs/glossary.md` §5.

- AM16, the recency durations (the chat's A7). The recency duration is 3 times the task's declared wait: 3 minutes (90
  ticks) for coffee_break, 4.5 minutes (135 ticks) for office_break. It is counted from the observed completion.
  Reason: the motivation is the real ratio (a break of about 10 minutes; a second one within 30 minutes is rare),
  applied at the scale the task durations already use.

- AM17, the strengths (the chat's A8), the same in both domains:
  - coffee_break: low 0.02, high 3.
  - ac_activation: low 0.005, high 0.2.
  - office_break: low 0.005 (recent), high 0.02 (not recent).
  The source of each, in these words: "Modelling assumption, Hadi, 3 October 2026. A relative strength. Its order of
  magnitude is motivated by the proposed meaning of a strength (a ratio of counted task starts), which is not
  validated."
  MOTIVATION ONLY, not in the declarations: the frequency readings of the design chat, for example "about 4
  unscheduled coffees per shift".
  Stated consequence, not a criterion: the values decide whether an assigned task is at or above the threshold before
  any distinguishing movement. No value was chosen from the threshold or from a scenario.
  SUPERSEDED (AM38, Hadi, 3 October 2026; the design chat on the rest of T-K part 1): the values and their sources,
  under the three levels (AM36; the declarations, AM37 under AM13).
  - 0.005 and 0.02 keep the recorded source sentence above.
  - coffee_break raised, 2 in place of 3. Source, Hadi, 3 October 2026: break time favours the coffee break; it is more
    probable than an assigned task, and not as strongly as 3 stated. Reason for leaving 3: held over a whole period, 3
    asserts that 3 of 4 task starts are the coffee break, so that the human almost never starts an assigned task in
    break time.
  - ac_activation raised, 0.5 in place of 0.2. Source, Hadi, 3 October 2026: a warm room is a matter of comfort with no
    stated time, so the human more often starts an assigned task first, and the activation follows within about 3 task
    starts. 0.2 asserted 6 task starts.
  - ADDED (Hadi, 4 October 2026, on ccode's flag 2), beside the two sources: the two raised strengths lie on opposite
    sides of 1, because break time is a scheduled norm of the site and a warm room is a weaker call.
  - ac_activation with the room not warm and the A/C off: the ordinary strength 0.02, in place of 0.005. Nothing states
    that the task is pointless there.
  - A coffee break just completed has the suppressed strength in every situation, inside break time too.
  - No value was chosen from the threshold or from a scenario.
  NOT TAKEN (Hadi, 4 October 2026, on ccode's flag 2):
  - The raised strength 1 for coffee_break. It asserts no direction. Hadi stated one: break time favours the coffee
    break.
  - One raised strength shared by all foreseeable tasks. Hadi stated different directions for coffee_break and
    ac_activation, which is knowledge that the two differ.
  Each value rests on an argument about what it states about the human; none rests on a run or on the threshold. The
  reading per value: design_decisions.md, this title, R3's AM39.

- AM18, the A/C switch (the chat's A9). An A/C switch is an object in the layout with a state, on or off (ac_on).
  ac_activation sets it to on. A setup may state its initial state. The state is read by the occurrence condition, not
  by a condition of the task.
  V1 rule: at most one A/C switch per layout, in every domain. A layout may have none.
  ac_activation and the context fact room_warm are in the task model and the context knowledge of both domains.
  dock_loading's three existing rooms get no A/C switch; stage 2's layouts may have one.
  Reason for no switch in the existing rooms: the re-measurement of stage 1's baseline then shows the effect of context
  knowledge alone.
  ADDED (the design chat, 3 October 2026): the reason for the V1 rule. An occurrence condition is evaluated per
  foreseeable task, not per hypothesis (design_decisions.md, this title, R3's AM2, its CLARIFIED line), so the state of
  one switch cannot select the strength of one hypothesis of ac_activation; a condition per hypothesis is TODO-164.
  Not taken: the state of the A/C as a condition of the task (context only lowers the strength).
  AMENDED (AM43, AM45, Hadi, 4 October 2026; THE BUILD'S PLAN, RULED, below): ac_activation sets ac_on through its
  own action switch_on; in dock_loading the switch stands only in the delivery hall, and ac_activation has one method,
  from the hall.
  SUPERSEDED IN PART (AM36, AM37, Hadi, 3 October 2026), the wording: "the occurrence condition" reads "the suppressing
  condition of ac_activation"; "an occurrence condition is evaluated per foreseeable task" reads "the suppressing and
  the raising condition are evaluated per foreseeable task".

- AM19, the layouts with more than one A/C switch (the chat's A10). They are changed to the V1 rule (AM18), in their own
  step before the build of T-K part 1. First ccode lists every such layout and every scenario, test and analysis that
  rests on it; Hadi decides on that list. Affected analyses and tests are deleted or regenerated. Hadi's statement: the
  existing layouts, setups and their analyses are not an evaluation reference and need not be kept.
  Order, for the regression check: the list, the layout change, the regeneration of the baselines that remain, then
  the build.
  KNOWN INPUT (the design chat, 3 October 2026; ccode, the same day): env_layout_05 holds three A/C switches
  (ac_switch_0 at (400, 550), ac_switch_1 at (356, -210), ac_switch_2 at (230, -550)). Its scenarios are
  scenario_s04_01 to _03 (env_setup_04); scenario_s04_01, a fixture of the regression sweep (analysis/kitting/
  tb1a_destination/, both priors), scripts two activations, at ac_switch_1 and then ac_switch_2. Tests that name
  env_layout_05 or the s04 scenarios: tests/kitting/test_th1_tree.py, test_td15_build.py, test_td1_adequacy.py,
  test_g_build.py. The full list, over every layout of both domains, is the step's own work.

- AM23, the scale of the durations (the chat's A14). A simulator convention: the durations declared in the domains (the
  waits of the foreseeable tasks, the recency durations) are at a compressed demonstration scale and are not
  calibrated. In `docs/assumptions.md` as 6.3.

- AM24, the build's acceptance (the chat's A15; Hadi's clarification): "identical except for the lines the build
  names", with the regression audit. Reason: the rename of the run option changes the run header in every log. Also:
  with context_knowledge on, runs with assignment_knowledge off change too.

- AM28, the assumptions placed in `docs/assumptions.md` (the chat's B4): the perception entry (AM25, AM27) as 5.4; the
  entry's assumption A1 (given the task, the movement does not depend on the context) as 6.1; its A5 (the declared and
  the actual duration match) as 6.2, stated as a baseline whose violation is a deviation that the existing chain
  handles. A4 (no claim that a strength measured at one real site holds at another) stays in the design record only.
  A4 is about strength values at real sites; it does not concern the per-domain declaration.

- AM29, ccode's check, 3 October 2026, recorded with open item 3 (the tests; the chat's B5). A shorter wait is
  authorable (during wait_at, drop; 46 seconds, since 45 cannot be written at 2 seconds per tick; the entry closes as
  abandoned). A longer wait is authorable (during wait_at, a Start of stand). Neither is authorable when the coffee
  break is itself the task of another entry's event (the stack is one level deep, TODO-100): that case is recorded as
  absent.

NOT RULED, the chat's ideas and open items, each to its place:
- T-K part 2: soft edges and a gradual return, "or" with "long work without a break" (THE CUT AND THE QUEUE above, T-K
  part 2's OPEN ITEMS, ADDED; the roadmap's T-K entry, part 2). T-K's future work: the stream of context values (THE CUT
  AND THE QUEUE above, the future work).
- T-F: the time-scale convention for the evaluation (TODO-144, its open item of 3 October 2026).
- Future work [FW], by Hadi's ruling: A/C deactivation (TODO-163); several A/C switches in one layout (TODO-164).
- Open in T-K part 1: content point 3, the tests (OPEN ITEMS, item 3). Open at the re-measurement step: whether the 22
  potentially confounded MPB runs (the heading "T-G stage 1", SCOPE REDUCED AND THE MPB ON DOCK_LOADING RUN, its CAVEAT)
  are rerun then or in stage 2.
  RULED IN PART (Hadi, 3 October 2026): content point 3 (CONTENT POINT 3, THE TESTS, below). The question of the 22 MPB
  runs stays open.

CONTENT POINT 3, THE TESTS, RULED (Hadi, 3 October 2026; T-K part 1's open item 3). Records only: nothing is built,
and no layout, setup, scenario, test or analysis is changed. Hadi's points 1 to 7 are KT1 to KT7, in order. KT4 is
conceptual: AM34 in design_decisions.md under this title (under AM11); its record part is here.

- KT1, the order of the tests. First kitting, then dock_loading's stage 1 scenarios. In each domain first the IRB with
  an idle robot, then the MPB with a working robot.
  Reason: T-K changes the belief, so the recognition is examined first; the two MPB cases (KT3) then show whether a
  changed admission changes the robot's decision.

- KT2, the rooms on kitting. Layouts env_layout_12 to _14 are unfit for a controlled test: they carry the MPB's many
  tables. Hadi designed env_layout_15, _16 and _17 (6354a90, 1efe382, 014538a): the kitting table at the middle of the
  north wall, the exit place corner_NE.
  - env_layout_15 has no A/C switch; it is the first, basic room.
  - env_layout_17 is env_layout_15 plus an A/C switch between two deliveries.
  - env_layout_16 has a dense cluster with the coffee machine and the A/C switch inside it.
  - In env_layout_15 and _16 the human does all items and the robot is idle. env_layout_17 serves the MPB or a mix.
  - env_layout_10, _11 and _02 stay unchanged, as a comparison.
  - A further layout by Hadi, with more shelves and items, is to come for the second coffee break and the recency
    fact; that case waits for it.
  AMENDED (Hadi, 3 October 2026; ROUND 1, KT9, below): the rooms as they are. The kitting table stands at the middle of
  the north wall in all three (014538a). env_layout_16 lost its two south-east shelves, shelf_3 and shelf_4, outside
  the cluster (4cd7bca), so that its runs end before step 500; the cluster is unchanged. ccode may adjust these rooms
  where it makes a better basic test, decided before the runs and never after seeing a result.
  CORRECTED (recorded 4 October 2026; Hadi's correction in the layout tool's chat, 3 October 2026): "env_layout_10, _11 and _02 stay unchanged" reads "stay
  as they are", env_layout_02 as it is after Hadi's correction of its object sizes (4191202, 3 October 2026: the
  coffee machine 50 × 50, the A/C switch 20 × 20, the sizes of every other kitting layout; nothing else changed).
  ccode's check, 4 October 2026: the correction is committed; only the viewer reads an object's size
  (`mesa_sim/viz/space_drawer.py`), so no run's behaviour depends on it.

- KT3, the basic set. The only variation is where a foreseeable task is placed: between tasks (after the first
  delivery, after the second, and so on) and inside a task, between its actions. No other kind of deviation.
  Reason: this set tests the implementation of context knowledge, and other deviations would mix causes. So the
  duration mismatch (a coffee break cut short or prolonged, which needs a deviation event; AM29 above) waits for a
  later set.
  - Size: two setups per layout, five or more scenarios each; every scenario run with context knowledge on and off.
    SUPERSEDED IN PART (KT13, Hadi, 4 October 2026): "two setups per layout"; one setup per room, and a scenario that
    states its own timeline where the window is to differ.
  - Two cases also run in the MPB: a coffee break inside the break time, and deliveries through the whole break time.
  - The measure: the tick at which the true task reaches the threshold and is admitted, and whether a retraction
    follows.
    AMENDED (Hadi, 3 October 2026; ROUND 1, KT10, below): for ac_activation the measure is its belief at its arrival,
    not its admission.
  - Expectations are stated before the runs.

- KT4, the setup holds the timeline of context facts (AM34; amends "the scenario's timeline" of THE CUT AND THE QUEUE
  above and of AM11).
  Reason: the timeline is the world's course and does not depend on what the human does; the scenario holds the
  agents' behaviour; one timeline is then shared by several scenarios. The two setups of a layout differ in their
  timeline, and this is also how the effect of a different window on the same activity is tested.
  ADDED (Hadi, 3 October 2026, in the design chat): the same activity under a window whose edge falls before the human
  leaves for the foreseeable task, during the walk to it, or after the arrival. The middle case is the recorded cost
  of crisp facts (design_decisions.md, this title, R5: the prior changes at one tick, where the approximation of A2 has
  its largest error): the prior changes inside the episode at one tick. It is part of authoring the windows.
  SUPERSEDED IN PART (AM40, KT13, Hadi, 4 October 2026): the setup holds the default timeline, and a scenario may state
  its own, which replaces it whole; "the two setups of a layout differ in their timeline" is dropped (KT13). The ADDED
  line stands: the three edges are authored as scenarios' own timelines.

- KT5, a round without context knowledge comes first, before the mechanism is built: the setups and the human's
  scripts in env_layout_15, _16 and _17, run in the IRB with the present equal prior.
  Reason: it gives the "off" side of every case and shows how well the movement alone separates the tasks in these
  rooms.
  BUILT AND RUN (3 October 2026; 4cd7bca, 4c71b44): ROUND 1, KT8, below.

- KT6, findings recorded; none changes a value.
  - The strength 3 of coffee_break gives, with one delivery live and no other foreseeable task, a prior of exactly
    0.75 (3 / (1 + 3)), the threshold. The value stays, because moving it would choose a value from the threshold
    (AM17's stated consequence).
    AMENDED (Hadi, 3 October 2026; ROUND 1, KT11, below): work as a whole contributes 1 however many deliveries are
    live, so in env_layout_15 the coffee break's prior inside the break time is 0.75 in every scenario.
    SUPERSEDED (AM36, AM38, Hadi, 3 October 2026; THE STRENGTHS REVISED, below): the coffee break's raised strength is
    2. With one coffee machine and no A/C switch, its prior inside the break time is now 2/3 for any number of live
    deliveries, and each of n live deliveries has 1/(3n). The finding that it equals the threshold no longer holds.
  - The recency duration of 90 ticks (AM16) was derived from the wait, which is compressed, while walking is not. In
    these rooms the walk from the coffee machine to the table and back takes about 84 to 94 ticks. It joins T-F's open
    item on the time scale (TODO-144, its open item of 3 October 2026).
  - In env_layout_15 the prior has no effect once no delivery is live.
  - In env_layout_17 the robot must not hold item_1 or item_4, or the A/C switch no longer stands between two of the
    human's hypotheses; and two deliveries that finish together at the shared table stop closer than min_separation.
    CORRECTED (Hadi, 3 October 2026; ROUND 1, KT9, below), by role: the robot must not hold the items of the two
    shelves beside the A/C switch (in env_setup_15, item_1 on shelf_1 and item_4 on shelf_4).

- KT7, the state. Open item 3 (the tests) is ruled (OPEN ITEMS above). Next: the round without context knowledge
  (KT5). Then a new design chat takes the build of T-K part 1: the list of the layouts with more than one A/C switch
  (AM19), the build's plan, the build, the runs with context knowledge on, dock_loading, the close. A later chat
  returns to T-G's stage 2.

ROUND 1, THE ROUND WITHOUT CONTEXT KNOWLEDGE: BUILT, RUN AND ACCEPTED; HADI'S DECISIONS ON ITS REPORT (3 October
2026). Records only in this block; the round's artefacts and outputs are named in KT8. Hadi's points 1 to 4 are KT8 to
KT11, in order; KT12 is the state. Each states its reason. Nothing of the mechanism is built.

- KT8, the round is done (KT5). 31 scenarios in env_layout_15, _16 and _17 (scenario_s13_01 to _07, s14_01 to _11,
  s15_01 to _13, on env_setup_13, _14 and _15; one setup per room; run files in configs/kitting/irb/tk1/), the robot
  idle, the human doing every delivery, the only variation where one foreseeable task is placed (KT3). The
  expectations were committed before any run (4cd7bca); the runs and the report followed (4c71b44):
  analysis/kitting/irb/tk1/README.md (the set, the foreseeable tasks' ticks for authoring the timelines, the
  expectations and their md5s) and REPORT.md (the comparison, the measure per scenario, the rooms).
  - Every run agrees with its expectations: 0 disagreements at 1e-9 in all 31; at print precision one, s14_02 tick 181
    (S = 0.049970 printed as 0.0500), the IRB's known print-precision flag.
  - No run is touched by the undeclared weight (TODO-66): every run ends before step 500 (the last observed tick is
    480).
  - No retraction follows any admission.
  What the rooms show, in plain words:
  - env_layout_15, the basic room: the movement recognises every task, but late: a delivery reaches the threshold at
    about 70 to 85 percent of its walk to the shelf, the coffee break from the table at 32 to 34 ticks of a 43-tick
    walk. (The only stretches that never reach it are the short first parts of a delivery cut by the coffee break.)
  - env_layout_17, the A/C switch between two shelves: the A/C hypothesis delays the two deliveries beside it (item_1
    reaches the threshold at 47 ticks against 37 in env_layout_15, item_4 at 45 against 31); the other two are nearly
    unchanged.
  - env_layout_16, the dense room: the movement recognises nothing in the cluster before the arrival. A delivery
    reaches the threshold only on the carry back, the coffee break only during its wait, the A/C activation never.
  Reason: KT5 asked for the "off" side of every case and for how well the movement alone separates the tasks.

- KT9, the rooms as they are (by Hadi's decision or with his acceptance). The kitting table stands at the middle of
  the north wall in all three. env_layout_16 lost its two south-east shelves (shelf_3 and shelf_4, outside the
  cluster), removed before the runs so that its runs end before step 500; the cluster is unchanged. ccode has Hadi's
  permission to adjust these rooms where it makes a better basic test, decided before the runs and never after seeing
  a result. The caution for env_layout_17 (KT6) reads by role: the robot must not hold the items of the two shelves
  beside the A/C switch.
  Reason: the shelves of env_layout_16 were removed so that its runs end before step 500, where the undeclared weight
  acts (TODO-66). The permission is bounded by its condition: a change is decided before the runs, never after a
  result.
  ADDED (Hadi, 3 October 2026, on ccode's report): the reasons for the other two. ccode may adjust the three rooms
  because they are test instruments and not an evaluation reference (Hadi's statement on the layouts, AM19). The
  caution for env_layout_17 reads by role because objects in these rooms may move or be renumbered.
  ADDED (the design chat, 3 October 2026): env_layout_16 lost its two south-east shelves only because its runs had to
  end before step 500. The build removes that limit (AM22, TODO-66). Hadi accepted the room as it is; whether the
  shelves return is not ruled.

- KT10, findings of the round; none changes a value.
  - The A/C activation is almost never recognised by movement, since its wait is one tick (it reaches the threshold
    only in s15_12 and s15_13, with an item in hand; never in env_layout_16). The wait stays; it is a domain value. For
    the A/C the measure is its belief at its arrival, not its admission (amends KT3's measure).
  - A coffee break begun inside a delivery after the carry (before the place) leads but stays inadequate until the
    human reaches the machine, because its evidence counts from the start of the delivery (s13_07, s15_07: the
    threshold at 153, admitted at 163; the same for the A/C in s15_13). This is the episode's existing behaviour, and
    the prior does not change it.
  - Two A/C cases in env_layout_17 peak just under the threshold with the equal prior (s15_10 at 0.746, s15_11 at
    0.745), so a later crossing there must not be read as the effect of the A/C's strength.
    MOVED (4 October 2026, T-K part 1's gate stage, AM42): read over the live hypotheses, the gate's value, the two
    peaks are 0.7487 and 0.7468, still below the threshold (analysis/kitting/irb/tk1/REPORT.md, its last section).
    Four of round 1's admissions fall one tick earlier (s15_02, s15_05, s15_10, s15_12), no retraction; KT8's other
    numbers stand.

- KT11, the method of the comparison (ruled by Hadi). The run with context knowledge off is not a neutral baseline: the
  equal prior gives a foreseeable task the share of one delivery. So the tests read three conditions:
  - A: context knowledge off;
  - B: context knowledge on, with the context fact not holding (the low strengths);
  - C: context knowledge on, with the context fact holding.
  A to B shows the effect of the declared strengths; B to C shows the effect of the context fact. One window in a
  setup puts some scenarios in B and others in C, since the foreseeable task falls at a different tick in each.
  The directions expected before the runs:
  - deliveries earlier in B and C than in A;
  - a coffee break outside the break time later in B than in A;
  - a coffee break inside the break time earlier in C;
  - the A/C lower than A in both B and C, and higher in C than in B.
  CORRECTED (Hadi, 3 October 2026, on ccode's report of these records): the first direction, "deliveries earlier in B
  and C than in A", was the design chat's own sentence and contradicts the prior's arithmetic. When break_time holds,
  coffee_break's high strength 3 takes most of the prior, and each live delivery's prior falls below its share in A
  (in env_layout_15, with n deliveries live, from 1/(n + 1) to 1/(4n): 0.25 against 0.5 for one, 0.0625 against 0.2
  for four). The directions, as corrected:
  - deliveries are earlier in B than in A;
  - in C, deliveries are later than in A when the fact that holds is break_time, and earlier when it is room_warm;
  - a coffee break outside the break time is later in B than in A; inside the break time it is earlier in C;
  - the A/C is lower than A in both B and C, and higher in C than in B; with several deliveries live the difference
    between A and C is small (in env_layout_17 with four deliveries live, 0.164 in C against 0.167 in A).
  The "later in C" case is the cost of context knowledge when the human works through a break time: the robot expects
  the break and recognises the work later.
  Also recorded: work as a whole contributes 1 however many deliveries are live, so in env_layout_15 the coffee
  break's prior inside the break time is 0.75 in every scenario.
  ADDED (the design chat, 3 October 2026), for the expectations with context knowledge on: the gate refuses only
  below the threshold (`MetaPlanner._clears_gate`, confidence < θ). Where the prior alone is exactly 0.75, as for the
  coffee break inside the break time in env_layout_15, the outcome at the first observed movement depends on
  floating-point rounding. The runs are deterministic, so the result is stable, and it is arbitrary.
  Reason: the run with context knowledge off is not a neutral baseline, since the equal prior gives a foreseeable task
  the share of one delivery; A to C alone would mix the effect of the strengths with that of the fact.
  SUPERSEDED (AM36 to AM38, Hadi, 3 October 2026; THE STRENGTHS REVISED, below): the expected directions for the runs
  with context knowledge on, and their arithmetic (the first directions, the CORRECTED directions with their numbers,
  the "Also recorded" line on 0.75, and the case of a prior of exactly 0.75 in the ADDED line; that line's statement of
  the gate, which refuses only below the threshold, stands). The design chat restates them before those runs. The
  three conditions A, B and C stand; in B, "(the low strengths)" reads "(no raising condition satisfied)".
  RULED (Hadi, 3 October 2026), for that restatement: with context knowledge on and no raising fact holding, a lone
  live assigned task is admitted on its commitment warrant from its prior, and a retraction follows if the human then
  takes a foreseeable task.
  SUPERSEDED (AM67, Hadi, 4 October 2026; THE GATE AFTER STEP 5B, RULED, below): the RULED line above. Commitment
  warrant alone no longer admits; a lone live assigned task needs observation warrant (the human's first step toward
  it, or the observed completion that enters its phase), and the gate refuses it while the evidence alone ranks another
  live hypothesis above it (AM68). A retraction still follows if the human then takes a foreseeable task.
  SUPERSEDED IN PART (KT14, Hadi, 4 October 2026; THE TIMELINE IN THE SCENARIO, below): the three conditions read
  context knowledge off against on, each case labelled by the state that the script meets.

- KT12, the state. The round without context knowledge is done; it is condition A. Next: a new design chat takes the
  rest of T-K part 1: the list of the layouts with more than one A/C switch and their change (AM19); the build's plan;
  the build; the timelines in the setups and the runs in conditions B and C; the two MPB cases (KT3); dock_loading's
  part, with the re-measurement of T-G stage 1's baseline; the close. Waiting: the further layout for the second
  coffee break and the recency fact (KT2); the duration mismatch (KT3). The entry point:
  docs/handoffs/T-G_forward_inputs.md, section 5. A later chat returns to T-G's stage 2.
  AMENDED (Hadi, 4 October 2026; KT13, below): "the timelines in the setups" reads "the timelines in the setups and in
  the scenarios that state their own".

THE TIMELINE IN THE SCENARIO, RULED (Hadi, 4 October 2026, the design chat; recorded the same day, before the build's
plan). Records only: nothing is built, and no layout, setup, scenario, test or analysis is changed. The conceptual part,
AM40 (the setup states the default timeline; a scenario may state its own, which replaces it whole) and AM41 (the
override of the timeline, later work), is in design_decisions.md under this title, under AM11's AM34. The record part
continues the numbering of the tests:

- KT13, the second setup per room is dropped. KT3's "two setups per layout" and KT4's "the two setups of a layout
  differ in their timeline" are superseded: the same script under another timeline is a scenario that states its own
  timeline on the room's one setup. `docs/handoffs/T-G_forward_inputs.md` 5.10 item 2 (how the same scenarios run on a
  second setup) is answered by it.
  Reason: AM40. A test case is a script, a window and an expectation, held together in the scenario; a second setup
  that differs only in its timeline is no longer needed to vary the window.

- KT14, the conditions of the tests restated. KT11's three conditions A, B and C read: context knowledge off against
  context knowledge on, with each case labelled by the state that the script meets (for example, the foreseeable task
  begun while its raising condition holds, while its suppressing condition holds, or while neither holds). The
  design chat restates the expected directions before the runs (KT11's SUPERSEDED line stands).
  Reason: with a scenario's own timeline, the state a case meets is a property of the case, stated with it; the
  comparison is between the two settings of the run option on the same case.

THE BUILD'S PLAN, RULED (Hadi, 4 October 2026, on ccode's plan, `docs/handoffs/plan_T-K_part1.md`, 41efa76; recorded
the same day). Records and the plan only; nothing is built. The plan's decisions D1 to D10 and two additions of the
review are AM42 to AM53, in this order: D1 AM42, D2 AM43, D3 AM44, D4 AM45, D5 AM46, D6 AM47, D7 AM48, D8 AM49, D9 AM50,
D10 AM51, the review's addition 1 AM52, its addition 2 AM53. Conceptual (design_decisions.md, this title): AM42 under
R7, AM44 under R3, AM46 and AM50 under AM11's AM40, AM47 under AM27, AM52 under R1. The plan is amended to these
rulings.

- ccode's proposals P1 to P5 are accepted (the plan, section 7): the prior with context knowledge off as exact unit
  weights; the timeline as a function of the tick read by the world-state builder; timeline facts in the A5 form; the
  level per task read in the knowledge component; the recency facts passed to the recognizer on each run.

- AM43, the A/C's action (D2). A new action schema switch_on, of the same form as wait_at (standing for a stated
  duration, completion waited(agent, entity)), with the declared effect that the switch is on (ac_on). Only
  ac_activation uses it, in both domains.
  Reason: a state of the world changes through a declared effect of an action (T-G A5); an effect on wait_at would also
  apply at the coffee machine.
  Not taken: a rule inside the environment (an effect applied only to objects of the state's type); the robot inferring
  the state from an observed wait at the switch ("not taken" in T-G A5).

- AM45, dock_loading's ac_activation (D4). One method, from the hall. In dock_loading an A/C switch stands only in the
  delivery hall. A choice of scope for V1, not forced by the design.
  Consequence: when a dock_loading room gets a switch, the method from the office is added in the same step; without it
  the task is not a live hypothesis while the human is in the office.

- AM48, the build's regression scope (D7): the four maintained sets, round 1's 31 runs with context knowledge off, and
  dock_loading's milestone runs, as the plan states (its D7 named three, its stage 0 six: scenario_s03_02, s05_02,
  s07_02, s03_03, s05_03, s07_03; the amended plan runs the six, its section 11, X6). The 22
  dock_loading MPB runs stay with dock_loading's step (the recorded open question).
  Consequence: dock_loading's recognition and planning runs (its IRB and MPB sets) are not rerun in the build; a
  regression that affects only them is found at dock_loading's step.
  CONFIRMED (AM55, Hadi, 4 October 2026; THE CROSS-CHECK, RULED, below): the six milestone runs are run; the IRB and the
  MPB sets are not.

- AM49, the instruments' check with context knowledge on (D8): round 1's 31 scenarios run with context knowledge on and
  compared with the oracle for agreement only; their results are not read (the reading belongs to the step with the
  authored windows).
  Consequence: no run of the build exercises a raised strength; the unit tests against the method document cover it
  until the step with the authored windows.

- AM51, the run options at every caller (D10): `SimModel` takes `assignment_knowledge` and `context_knowledge` with no
  default; every caller states both. The defaults (both on) live in the run file and the loader's fallback.
  Consequence: a caller that does not state both options fails with an error.

- AM53, the gate's change in the build (the review's addition 2): AM42 has its own commit and its own regenerated
  baseline. The plan places it and states which baseline each later stage's check compares against.

- Recorded beside them: CLAUDE.md and the roadmap brought in line with AM40; TODO-177 (the override of the timeline,
  AM41) and TODO-178 (the removal of the floor and the scaling from the reported distribution, AM42's later work)
  opened.

THE CROSS-CHECK, RULED (Hadi, 4 October 2026, on ccode's cross-check of the plan's rulings, the plan's section 11, X1
to X10; recorded the same day). Records and the plan only; nothing is built. Ruled: X4 (AM54, design_decisions.md,
this title, under R1), X6 (AM55), X3 (AM56), X1 (AM57), X2 (AM58). X5, X7, X8, X9 and X10 need no ruling and stay
recorded as stated in the plan's section 11.

- AM55, dock_loading's runs in the build (X6). ccode's reading of AM48 is confirmed: the build does not rerun
  dock_loading's recognition set (its IRB) and its planning set (its MPB); it runs dock_loading's six milestone runs
  (scenario_s03_02, s05_02, s07_02, s03_03, s05_03, s07_03).

- AM56, the label of the episode-boundary line for a completed switch_on (X3). A log names what happened: corrected
  in the build if the change is small, otherwise recorded as deferred work with the reason.
  ccode's judgement (4 October 2026): not small; deferred, TODO-179. Reason: the boundary's observable reads facts only
  (T-D L1 as built). wait_at and switch_on have the same precondition, at(agent, entity), and the same completion,
  waited(agent, entity), and wait_at's ?entity has no type in its schema (the types come from the task that calls it),
  so at the switch both are enabled and both complete on the same fact; the world state carries no object types.
  switch_on's effect ac_on distinguishes the two only when the A/C was off. A correct label needs the terminal actions'
  parameter types derived from the methods that call them and the objects' types in the robot's world state: a change
  to the boundary's as-built reading, which is the recognizer's and needs a ruling. Reordering the terminal actions
  only moves the wrong label to the coffee break (switch_on(coffee machine)). The boundary's tick is right; only its
  label is wrong.

- AM57, the test-bed sets and the new gate (X1).
  - Round 1 is rerun in the build with the new gate (AM42) and its outputs are replaced. Its README states what changed
    and names the last commit that holds the old results. Findings in the design records that move are marked, not
    rewritten.
    Reason: the comparison needs an "off" side made with the same gate as the "on" side, and one current baseline is
    kept, not two. Not taken: a second folder beside the old one; a rerun only at the later step.
  - The gate's stage also reruns kitting's planning set (the MPB) and checks its declared properties, and reruns
    kitting's recognition set (the IRB, scenario_s08 and s09). Their outputs are replaced in the same way. If a declared
    property no longer holds, that is a finding: the build stops and reports it with its cause, and does not continue;
    it is no reason to change a ruling or a scenario.
    Reason: the planning set is the test-bed of the meta-planner, and the gate's change is a change of the
    meta-planner's behaviour; it is checked where expectations are declared.
  - dock_loading's recognition set and planning set (T-G stage 1's IRB and MPB outputs, `analysis/dock_loading/irb/`,
    `analysis/dock_loading/mpb/`) are stale from the gate's stage of the build until dock_loading's step of T-K part 1,
    which measures them again.

- AM58, the viewer's confidence (X2): deferred work, TODO-180. The viewer is not checked for which value it shows as
  the confidence.

THE CROSS-CHECK'S CONSEQUENCES, RULED (Hadi, 4 October 2026, on the plan's section 11, X11 to X14, and on ccode's
judgement of X3; recorded the same day). Records and the plan only; nothing is built. X11 is AM59, X12 AM60, X13 AM61,
X14 AM62, X3's acceptance AM63; AM64, on ccode's flag on AM61, below.

- AM59, the old data (X11). Before the gate's stage replaces the outputs of the three kitting sets (round 1, the IRB,
  the MPB), their untracked data (per-tick data and figures) are copied outside the repository: one external copy;
  nothing of it is added to the repository. Each set's README names the copy.
  Reason: round 1's per-tick data and figures are in no commit; kitting's IRB and MPB data are restorable from 7d00f43.

- AM60, the gate's stage and its commits (X12). The gate's stage is committed only after its checks pass. If it stops
  before, the committed state stays on the old gate.

- AM61, the stop conditions in the planning set (X13). Two: a disagreement with the independent computation (the
  oracle's parts 1 to 3), and a scenario that no longer reaches its authored coverage case. A stop means that its cause
  is examined; it does not mean that the ruling on the gate is rejected.

- AM62, the run without assignment knowledge (X14). A diagnostic: its changes are reported and never stop the build.

- AM63, the label of the episode boundary for a switch_on (X3). Accepted as ccode reported it (AM56): the label stays
  deferred (TODO-179); the tick of the episode boundary is not changed.

- AM64, the stop conditions of the gate's stage, confirmed (Hadi, 4 October 2026, on ccode's flag). AM61 adds
  specificity to AM57 and does not replace it. Three conditions stop the build in the planning set: a declared
  property no longer holds; the run disagrees with the independent computation; a scenario no longer reaches its
  authored coverage case.

Next: the three open items, then T-K part 1's build plan (BUILD DISCIPLINE, step 1).
AMENDED (Hadi, 3 October 2026): the design is ruled and amended (AM1 to AM9); the three open items are unchanged (the
values for kitting and dock_loading, the perception assumption, the tests). T-K is framework-wide: it concerns
kitting and dock_loading alike. Next: unchanged.
SUPERSEDED (Hadi, 3 October 2026; CONTENT POINTS 1 AND 2 above): content points 1 and 2 are ruled (AM10 to AM29).
Next: content point 3 (the tests), then ccode's list of the layouts with more than one A/C switch (AM19), then the
build's plan (BUILD DISCIPLINE, step 1).
AMENDED (Hadi, 3 October 2026, on ccode's report of these records): AM30 to AM33 (design_decisions.md, this title: the
memory of observed completions outside the recognizer, AM30; a context value measured from the robot's own
observation, AM31; the wording of "no action changes a context fact", AM32; an observed completion is the task's
terminal fact, AM33) and the NOTES FOR THE BUILD'S PLAN above. Next: unchanged.
SUPERSEDED (Hadi, 3 October 2026; CONTENT POINT 3, THE TESTS above, KT7): content point 3 is ruled. Next: the round
without context knowledge (KT5); then a new design chat takes the build of T-K part 1 (the list of the layouts with
more than one A/C switch, AM19; the build's plan, BUILD DISCIPLINE step 1; the build; the runs with context knowledge
on; dock_loading; the close); a later chat returns to T-G's stage 2.
SUPERSEDED (Hadi, 3 October 2026; ROUND 1 above, KT12): the round without context knowledge is done. Next: KT12.
AMENDED (Hadi, 3 October 2026, recorded 4 October 2026; THE STRENGTHS REVISED, below): the form and the values of the
strengths are revised (AM35 to AM39) before the build's plan. Next: KT12's steps, unchanged; the build's plan reads
`docs/context_knowledge_method.md` as the statement of the prior, and the design chat restates the expected directions
before the runs with context knowledge on.

THE TASK RENAMED: T-K AND ITS PARTS (Hadi, 3 October 2026). Records only: a reorganisation of task names; no change of
behaviour. The old name and the new are mapped in one line each in CLAUDE.md and docs/design_decisions.md (this
entry's head); git commit messages use the old name.
1. T-K names context knowledge as a whole (K for knowledge). T-K part 1 is the crisp context knowledge.
   Reason: context knowledge is framework-wide. It concerns kitting and dock_loading alike, so it is a task of the pipeline,
   not a stage of the dock_loading task.
   The rule on task letters, clarified: a letter is never given to a different task; a task may be paused, resumed and
   revisited, and may hold a V1 part and a later part. T-G is paused after its stage 1. T-K part 1 runs now. T-G
   resumes at its stage 2 when T-K part 1 is closed.
2. The parts of T-K:
   - Part 1, V1, ongoing: crisp context knowledge (R1 to R8, AM1 to AM33).
   - Part 2, V1, at the end of the V1 queue after track 3b: degrees, as ruled (R5): membership functions, soft edges of
     a window, the gradual return after a task, "or", with "long work without a break" as its open item.
   - Later, future work: the stream of context values with the world's dynamics; A/C deactivation (TODO-163); several
     A/C switches in one layout (TODO-164); TODO-158 to TODO-161.
   Reason for the stream as future work: it needs a model of the world's physics, and nothing that V1 claims depends
   on it.
3. Everything related to context knowledge is T-K's. The open question of the prior, whether succession between tasks
   affects the division inside work as a whole (R4), is an item of T-K part 2: after T-G stage 2, to be argued with
   store_pallet present.
   Not moved: framework-wide work inside T-G (the choice between two applicable methods by cost, the robot with no
   applicable task, the observation rule, track 4). Hadi's principle: building a new domain includes revisiting its
   effect on the other domains, assessed framework-wide inside the domain's task.
4. The rename, everywhere in the repository's documents, older handoff files and frozen analysis reports included.
   Exception recorded: CLAUDE.md's rule that a frozen record is edited only by a superseding note does not apply to
   this rename. The entry's title is "T-K: context knowledge in the recognizer's belief"; this heading and the record
   identifier ([T-K/1]) follow it. docs/handoffs/T-G_forward_inputs.md keeps its name; its section 5 is T-K part 1's.
   Git commit messages are not changed.
5. Track 4's open points gain one line (docs/handoffs/T-G_forward_inputs.md, section 7; TODO-140): whether the robot's
   world state still holds the terminal fact of a task that the human completed outside the monitored areas. If it
   does, the robot gets a recency fact for a completion it did not observe, against AM27 and AM33.
6. Hadi's direction for T-K part 1's tests (content point 3, OPEN ITEMS item 3; still open, not ruled): recorded there.
   RULED (Hadi, 3 October 2026): CONTENT POINT 3, THE TESTS above (KT1 to KT7).

THE STRENGTHS REVISED, RULED (Hadi, 3 October 2026; the design chat on the rest of T-K part 1, on the form and the
values of the strengths; recorded 4 October 2026). Records only: no code, layout, setup, scenario, test or run is
changed. The design of context knowledge was reviewed before its build. Each revision rests on an argument about what
a value or the form states about the human; none rests on a run or on the threshold. The rulings are in the records
before the build's plan is written.

A. The rulings. The chat's A.1 to A.5 are AM35 to AM39, in order.
- AM35, the name "the assigned tasks as a whole" (wording only); AM36, three levels per foreseeable task, with a
  suppressing condition and a raising condition; AM39, the reading of a strength per value: design_decisions.md, this
  title, under R3, each with its reason.
- AM37, the declarations: under AM13 above. AM38, the values and their sources: under AM17 above.
- The marks they set, each with a pointer: in design_decisions.md, R3's bullet on the low and the high strength, the
  CLARIFIED line under AM2, AM7's line, R5, AM11, AM12, AM20, AM26; here, THE CUT (no "not"), T-K part 2's OPEN ITEMS,
  AM18's wording, NOTES FOR THE BUILD'S PLAN.

B. The glossary (`docs/glossary.md` §5). New entries: suppressing condition; raising condition; suppressed strength,
ordinary strength, raised strength; the assigned tasks as a whole; timeline of context facts; timeline fact; observed
completion; memory of observed completions. Amended: strength, prior, context knowledge, assignment knowledge, and §8's
T-K and T-K part 2. Retired, with a pointer: occurrence condition, the older records' term for the single condition,
replaced by the suppressing condition and the raising condition.

C. What becomes stale, marked superseded with a pointer here; the expected directions are not restated in this record.
- The finding that the coffee break's prior in break time equals the threshold (KT6, its first finding and its
  AMENDED line; KT11's "Also recorded"). With one coffee machine and no A/C switch it is now 2/3 for any number of live
  deliveries, and each of n live deliveries has 1/(3n).
- The expected directions for the runs with context knowledge on, and their arithmetic (KT11). The design chat
  restates them before those runs. RULED by Hadi for that restatement: with context knowledge on and no raising fact
  holding, a lone live assigned task is admitted on its commitment warrant from its prior, and a retraction follows if
  the human then takes a foreseeable task (KT11's RULED line).
  SUPERSEDED (AM67, Hadi, 4 October 2026): that RULED line, as KT11's SUPERSEDED line above states.
- T-K part 2's formula, strength = low + degree × (high − low), was stated for the pair of values: an open item of T-K
  part 2 that it is restated for two conditions (T-K part 2's OPEN ITEMS, above).
- The notes for the build's plan: no form for "not" is needed (NOTES FOR THE BUILD'S PLAN, above).
- OPEN, for the build's plan: which value the gate compares with the threshold, the belief over the live hypotheses or
  the output after its scaling by the pinned hypotheses (NOTES FOR THE BUILD'S PLAN, above).
  RULED (AM42, Hadi, 4 October 2026): the belief over the live hypotheses.
- The same marks in `docs/handoffs/T-G_forward_inputs.md`, section 5.

D. Records from the layout tool's chat (3 October 2026).
- KT2's line "env_layout_10, _11 and _02 stay unchanged, as a comparison" is brought in line with Hadi's correction of
  env_layout_02's object sizes (KT2's CORRECTED line). The correction is committed (4191202).
- `docs/handoffs/T-G_forward_inputs.md` (5.11) names the two entries of 3 October 2026 in design_decisions.md, "An
  object id is an opaque name" and "`subtype` is a stated fact of an object", with their bearing: the build identifies
  no object by the text of its id; dock_loading's layouts and setups changed after stage 1's baseline was measured
  (5d19859: `subtype` on the delivery bays and the pallets that touch them).

F. The method document. Hadi added `docs/context_knowledge_method.md` (812283c, 4 October 2026): the method of
context knowledge at the state of these rulings, the concept, the formulas and worked examples, written for Hadi's
reading and for a later paper; it serves the build's plan as the statement of the prior.
- Its place and name are kept (ccode's choice): `docs/` at the top level, beside `glossary.md`, `assumptions.md` and
  `terminology_revision.md`, the living documents of the design, which carry snake_case names. It is not a handoff (a
  handoff is written for one chat) and not an analysis.
- Its status, in its first lines: the design records hold the rulings and their reasons and are authoritative; the
  document states the result of the rulings; if the two disagree, the records win and the document is corrected.
- Its terms are brought in line with the glossary as amended in B. No formula, value or example is changed. The
  sentence of its section 3 on the half-open window edges is left; the build's plan confirms it.
- The standing rule, in CLAUDE.md beside the rule on where a ruling is recorded: a ruling that changes the method of
  context knowledge updates this document in the same records step. ccode does not change the method itself; ccode
  flags a contradiction with its evidence, and Hadi rules.
- Named in `docs/handoffs/T-G_forward_inputs.md` (5.1, 5.3, 5.7) as the statement of the prior that the build's plan
  reads.
- FLAGGED by ccode (4 October 2026), not resolved:
  1. Its status line named "the question of 4 October 2026 on the equal prior" (its section 13); no record holds a
     ruling or a question of that date. The phrase is kept in the new status line.
  2. Its section 14 states three things that A and the records do not hold: the value 1 not taken because it asserts
     no direction; the two raised strengths on opposite sides of 1 (break time a scheduled norm of the site, a warm room
     a weaker call); "one raised strength shared by all tasks" among the alternatives not taken.
  3. Its section 8 states a foreseeable task's warrant as supporting movement only (the path cost to the task's target
     decreased since the start of the present phase). Observation warrant has a second source, the phase entered by
     the observed completion of the hypothesis's previous step, the only source in a phase without a movement target
     (glossary §7, observation warrant; design_decisions.md, "T-D G: admission", AD1, AD2).
  RESOLVED (Hadi, 4 October 2026; follow-up records step):
  1. The question of 4 October 2026 was Hadi's question in the design chat on the equal prior; its answer is the
     derivation in section 13, no ruling. The status line names no question and says that section 13 is a derivation.
  2. Recorded under AM38 (above): the raised strength 1 and one raised strength shared by all foreseeable tasks as
     alternatives not taken, each with its reason; beside the two sources, why the raised strengths lie on opposite
     sides of 1.
  3. Section 8 corrected to the records: observation warrant has two sources, the path-cost gain toward the target and
     the observed completion of the hypothesis's previous step, the only source in a phase without a movement target.
  FLAGGED by ccode (4 October 2026), not resolved: section 12's three cases hold for kitting's coffee_break, whose
  walking phase is its first step (`coffee_break_default`: move_to, wait_at), so only the gain source applies there.
  They do not hold for dock_loading's coffee_break from the office (`coffee_break_office`: go to the office door, go to
  the coffee machine, wait_at). Its walk to the machine is entered by the observed completion of the walk to the door,
  and the recognizer gives the entry source before the gain (`shared/recognizer.py`, the observation warrant). A human
  who passes the office door on an unmodelled walk then makes that phase warranted, also when the human then stands
  (case 1) or walks away from the machine (case 2), until the phase is left or turns inadequate.
  CHECKED by ccode (4 October 2026): every number in the tables of sections 5, 10, 11, 12 and 13 was recomputed from the
  document's formulas and the declared values; none differs beyond the document's rounding.

STEP 1, THE LAYOUTS WITH MORE THAN ONE A/C SWITCH (AM19): LISTED, RULED AND BUILT (4 October 2026).
- The list (ccode, 4 October 2026; read only): over every layout file of both domains, registered or not, counted by
  the object type `ac_switch` (ac_activation's `parameter_types`), only kitting's env_layout_05 holds more than one:
  ac_switch_0 (400, 550), ac_switch_1 (356, -210), ac_switch_2 (230, -550). One each in kitting's env_layout_02, _07,
  _16, _17 and the unregistered env_layout99.json; none in the other kitting layouts and none in dock_loading. On
  env_layout_05 rest env_setup_04, scenario_s04_01 to _03 (only s04_01 scripts an activation: ac_switch_1, then
  ac_switch_2; ac_switch_0 never visited), tb1a_destination's two s04_01 logs, five tests, and twenty frozen analyses.
- RULED (Hadi, 4 October 2026, on the list): env_layout_05 keeps ac_switch_1 and no other A/C switch; ac_switch_0 and
  ac_switch_2 are removed, nothing takes their place. scenario_s04_01's script keeps one ac_activation, at ac_switch_1;
  the walk to ac_switch_2 and its activation are removed; the rest of the script keeps its order and purpose.
  env_setup_04 and scenario_s04_02, _03 are brought in line where they need it. The earlier logs, runs and analyses of
  this layout are no evaluation reference. Reason: the V1 rule (AM18), at most one A/C switch per layout, in every
  domain, before the build of context knowledge, so that the build's regression check starts from baselines that
  already follow the rule; a foreseeable task's conditions are evaluated per task, not per hypothesis, so the state of
  one switch cannot select the strength of one hypothesis of ac_activation (TODO-164).
- RULED (Hadi, 4 October 2026), the frozen analyses: the 14 early folders (runs of early tests, no systematic
  evaluation) are deleted whole: c_separation_stop, d2_recognition_trigger, f1_foreseeable_fixture,
  f1_robot_responsible, g1_graded_evidence, i2_ir_foundations, i3_phase_model, i4_evidence_model, i4c_episode,
  i4d_fold_unknown, i5_handback, t1b_realization, t6_ablation, t9_arrival_radius. In the other six (l_build, td_stage1,
  td_stage1b, irb2b_exposed_interval, tc2c_scripts, f47_fixtures) only scenario_s04_01's logs and the scripts that read
  only them are deleted, with one note per report that its case on the scenario is no longer reproducible. Citations
  in the records stay.
- BUILT: 32029d3 (the layout, the script, the notes, the test, tb1a's regeneration, CLAUDE.md's regression table),
  098b1a8 (the analyses; the deleted folders named in analysis/README.md, last held by 32029d3; CLAUDE.md and the
  roadmap mark them), and this records step. env_setup_04 and scenario_s04_02, _03 needed no change (they name no
  switch). The layout's stale note on env_layout_02's spelling of the type is dropped (it spells `ac_switch`).
- Acceptance: the four maintained sets rerun whole. Byte-identical: every log and `.rec` of tb1b, tb1c and tb3 and the
  other 14 logs of tb1a (92 of 96 files). scenario_s04_01's two logs and `.rec` streams differ, both priors: the
  `[coverage]` lines at load, every `[IR*]` line from tick 0 (two hypotheses fewer), the human's record from tick 207
  (on from ac_switch_1 to shelf_6); completion 384 → 379 prior on, 384 → 392 prior off (the world tick), no F1
  violation (tb1a README, its new section). 307 tests pass.
- Tests: one adapted, none removed. test_td15_build's two grasp tests (E8, E9 with E6's second amendment) took
  ac_activation(ac_switch_0) as the refuted foreseeable rival; it is now ac_activation(ac_switch_1), still refuted by
  the hand-walked delivery (tail < 0.05, inadequate), so both still check that the true hypothesis is the member that
  keeps the finding adequate. The other tests on the layout (test_g_build, test_td1_adequacy, test_th1_tree,
  test_th3_scenarios) read no removed switch and pass unchanged.
- Deleted beside the 14 folders: 20 local, git-ignored logs of scenario_s04_01 in the `pre*/tb1a_destination/` folders
  of l_build, td_stage1, td_stage1b (two sets) and irb2b_exposed_interval, in no commit; all 20 are in the copy at
  /home/hadi/teamrob_analysis_2026-10-02/ (irb2b's under its earlier name tb2b_exposed_interval). No script in the six
  reads only them; tc2c_scripts and f47_fixtures held none.

THE BUILD, STAGES 1 AND 2 (T-K part 1, step 3; ccode, 4 October 2026, by the approved plan,
`docs/handoffs/plan_T-K_part1.md`, section 8). Records only what was built and what moved.
- Stage 0: the baselines B0 at 93f9083 (the four maintained sets, round 1's 31 runs through the IRB pipeline,
  dock_loading's six milestone runs); local, not committed. One pass of the scope takes about 8 minutes.
- Stage 1, b85494d: the run option `assignment_prior` renamed `assignment_knowledge` (AM9), in code, every run file,
  the sweeps, the instruments and the tests; the log line `[IR-prior] switch=` reads `[IR-assignment] knowledge=`.
  Against B0: identical except those two lines, every `.rec` byte-identical.
- Stage 2, the gate (AM42, AM53): 91774ce (BeliefState.belief, the belief over the live hypotheses; `confidence` its
  leader's value; `_clears_gate` unchanged), 3b05a8a (the instruments: the IRB's rule 28 and the column `belief_h`),
  and the records commit with the regenerated sets (B2).
  - The three stop conditions (AM57, AM61, AM64) checked, none met: 0 disagreements with the oracle in round 1 (31),
    kitting's IRB (17) and MPB (16, both strategies); every declared property of the MPB reads as before; every
    claimed coverage cell is still reached (C2 and D8 one tick earlier, at 75 and 25).
  - What moved: the printed confidence wherever a key is pinned or floored. Decisions only where the leader sits
    within the pin scaling of θ (0.747 to 0.750): one admission one tick earlier in four of the 48 maintained logs
    (no motion, completion or separation moved), in five MPB scenarios (motion only in s12_02), in four rows of round
    1's measure; no retraction anywhere. The run without assignment knowledge: one MPB admission one tick earlier
    (s12_01 at 95), a diagnostic (AM62).
  - dock_loading's milestone runs (not a stop condition): an admission one tick earlier in five of six; in
    scenario_s07_02 it interrupts the robot's hold at 68 (5 of 6 ticks), the robot moves off at 26 cm from the human,
    and F1 counts one moving-robot violation where it stood at 22.5 cm before. A finding for dock_loading's step.
  - The old untracked data: /home/hadi/teamrob_analysis_2026-10-04/ (AM59). dock_loading's IRB and MPB sets marked
    stale in their READMEs (AM57).


THE BUILD, STAGES 3 TO 7 (T-K part 1, step 3; ccode, 4 October 2026, by the approved plan, section 8; the session's
state file `docs/handoffs/build_T-K_part1_state.md`). Records only what was built and what moved. Every stage's check
ran on a snapshot of that stage's files while the next was edited (Hadi's rule of parallel work), and each stage was
committed from its own files after its check passed. Each check compared with B2 (stage 2's regenerated outputs) with
the lines the earlier stages named set aside, so every stage's outputs are "B2 except the named lines".
- Stage 3, bbb7227 and 67b899e (the sweeps' executable bit): the run option `context_knowledge` (the CLI flag, the run
  file key, `SimModel`'s keyword with no default beside `assignment_knowledge`, AM51; every run file and sweep states
  `context_knowledge: false`, the tests both); the context weight `_context_weight`, its four constants and the old
  `ContextKnowledge` removed, nothing in their place (AM22, TODO-66); `_output` multiplies by unit weights (P1).
  Against B2: the four sets and round 1 identical except the `[run]` field; dock_loading's six milestone runs identical
  up to step 499 and differing from step 500 in the recognizer's lines only (the long-shift rule gone).
- Stage 4, f70f72f (4a) and 2393935 (4b). 4a: `Timeline`, `Window` and `TimelineSource` (`shared/types.py`; the mind
  never reads them), `ScenarioConfig.timeline`; the registry list `"timeline_facts"` (the A5 form, P3); the setup's
  optional `"timeline"` list and the scenario's `window(fact, start, end)` form; the resolution at load in `SimModel`
  (the scenario's, else the setup's, else none; AM40) and the header line `[run_mesa] timeline source=... windows=[...]`;
  the world-state builder adds the facts in force at the tick (P2); the load checks (AM20, AM46, AM50, AM52, AM54: no
  effect, retraction, precondition, guard or completion condition of any schema names a timeline fact, the `"states"`
  block refuses one, windows in ticks, half-open, no overlap). 4b: break_time and room_warm (timeline facts), ac_on (a
  state of `ac_switch`), the action `switch_on` with the effects waited and ac_on, called by ac_activation's method, in
  both domains (AM18, AM43); dock_loading's ac_activation with one method from the hall and its object type (AM45).
  Against stage 3: the timeline line (`source=none windows=[]` everywhere: no setup or scenario states one) and
  `switch_on` in `[rec]`, `[human]`, the human's step lines and the executor's `_load_plan` line where an A/C
  activation runs; every registered scenario of both domains loads; 329 tests.
- Stage 5, e589731 (the mind): `ContextKnowledge` rebuilt as the domain's declared context knowledge (`Strength`,
  `RecencyDuration`, the typed facts `TimelineFact` | `ObjectState` | `RecencyFact`, `Condition`,
  `ForeseeableKnowledge`; `level` and `strength`; validated at construction and against the robot's task model, AM4),
  declared once per registry under `"context_knowledge"` with the values of AM37 and AM38 and a source per value;
  `shared/completion_memory.py`, `ObservedCompletions` (AM30, AM33, AM47), built by the body with context knowledge on
  and read before the recognizer; the recognizer's constructor takes `context` (None: off), `update()` takes
  `recent` (P5), `_prior_weights` groups the live hypotheses by their schema's class and the pure function
  `context_prior` divides (R3, R4, AM35, AM36); `BeliefState.prior` and `levels`; the `[IR-context]` line per tick;
  `_prior` and `_initial_prior` renamed `_equal_evidence`, `_initial_evidence` (AM1); both run options on by default
  (AM3, TODO-139). Against stage 4, context knowledge off: identical (85 logs and `.rec`, round 1's 248 instrument
  files, the `[run]` header's field aside); with it on, all 85 runs of the scope complete (not read). 352 tests, among
  them section 10's eight rows, sections 11 to 13 of the method document, the memory on a recorded run (the recency
  fact holds on exactly 90 ticks), every registered scenario of both domains loading with context knowledge on, and the
  three shared modules naming no task, fact, object or domain in their code strings.
- Stage 6, 766f7d3 (the instruments): the IRB's oracle computes the prior on its own (rules 29 to 33 in
  `analysis/kitting/irb/README.md`: the facts, its own memory of observed completions from the rows, the level, the
  weights, the belief), from the domain's declared values (`ContextKnowledge.entries()`, `suppressed`, `ordinary`) and
  the method document; it calls no function of the recognizer or of the knowledge component for the level, the groups
  or the division, and asserts as before that neither recognizer module was loaded; the trajectory carries the timeline
  facts in force per tick and `params.recency_ticks`; the columns `prior`, `levels`, `recent` in expected and actual,
  compared; `run.sh --context on|off`; `admission.py` labels each true stretch by the state the script meets (KT14) and
  gives the A/C's belief over H at its arrival (KT10); `summary.py` prints the levels and the recency facts as
  stretches; `tdlib.py` reads `[IR-context]` and the timeline line; the MPB instrument follows (the oracle's context
  from the run file; `declared_context` at every instrument `SimModel` call). Check: round 1 (31), kitting's IRB (17)
  and MPB (16, both strategies and the prior-off diagnostic) with context knowledge off, every instrument output
  identical to B2 after the named additions (the three columns and their rows in `diff.md`, `recency_ticks`, switch_on's
  name and its effect ac_on in the trajectory's facts); round 1 with it on, 0 disagreements at 1e-9 in all 31 (the known
  print-precision flag at s14_02 tick 181 as before), results not read (AM49); 352 tests. Two defects found by the
  check and repaired (small, obvious): the MPB's `actual.py` compared the in-process lines unfiltered against the
  filtered log, so the model's own `[run_mesa] timeline` line failed its identity assertion in every MPB run (the
  same prefixes are now set aside on both sides); a stray indentation in `mesa_sim/list_scenarios.py`.
- Stage 7 (this commit): this block; the docs (`docs/assumptions.md` 1.4, 5.4 and 6; `shared/io_contracts.md`
  `BeliefState`, the constructor, `update()`, the companion class; `docs/recognizer_handback.md` §1.2, §1.6, §1.7 and
  §2; the glossary's BUILT lines in §5 and at θ, switch_on, setup and scenario; CLAUDE.md's options, greps and state;
  the roadmap; TODO-66 and TODO-139 closed; `docs/handoffs/T-G_forward_inputs.md` 5.5 to 5.7); the final regeneration
  of the four maintained sets, kitting's IRB, round 1 and the MPB in the repository at the stage 6 commit, with new
  README sections (md5s; every named line since B2) in the four sets and round 1.
- What the build did not exercise: no setup or scenario states a timeline and no run with context knowledge on is read,
  so no run of the build exercises a raised strength or the gate under the new prior; the unit tests against the
  method document cover the arithmetic until the windows are authored (AM49, D8). dock_loading's IRB and MPB sets stay
  stale (AM57).
- For the authoring of the windows (step 4): the foreseeable tasks' start and completion ticks in round 1's README
  stand, confirmed from stage 6's rerun with context knowledge on (31 of 31 trajectories equal in those columns); the
  recency fact of each coffee_break first holds on the README's completion tick and holds for 90 ticks in all 17
  coffee_break scripts.

STEP 4, KITTING, THE IDLE ROBOT: DONE (T-K part 1; ccode, 4 October 2026, three stages with a pause after each, as
Hadi ruled; `analysis/kitting/irb/tk2/README.md` and `REPORT.md`).
- Ruled by Hadi for the step: env_layout_16 as it is; the setups' default timeline break_time 178 to 300 (no room_warm);
  the eleven A/C scripts with their own timeline room_warm 150 to the end (3A); the windows of 3B to 3F; ccode's
  proposals P1 to P9 all taken (stage 1), P8 part of the measure; the direction "never on the prior alone" restated:
  while a delivery is live the coffee break does not reach θ on the prior alone, with none live it does and only the
  observation rule delays its admission; each direction read on three sides (off, on without the raising fact, on with
  it) with the deliveries live, each comparison marked within one script or across scripts, verdicts from within.
- Built: the timelines (setups; 3A in place in the eleven scenarios; 26 new scenarios, scenario_s13_08 to _15,
  s14_12 to _21, s15_14 to _21); `configs/kitting/irb/tk2/` (57, context knowledge on); the instrument (32ce7ed):
  `trajectory.py` carries a scenario's own timeline (a plain defect, found by the first expectations), `admission.py`
  reads the A/C's arrival on the tick before its switch_on and lists every admission of a hypothesis not the true task,
  `offon.py`; the expectations committed before any run (fffcffb). Audit: round 1 rerun, identical except the timeline
  line and the trajectories' timeline facts; the four maintained sets byte-identical; three tests updated (none for a
  change of behaviour).
- Result: 59 runs, 0 disagreements with the oracle at 1e-9. Directions (REPORT.md): 1, 2, 4 and 5 confirmed within one
  script on every side the set has; 2's delivery direction contradicted against off in 5 of 22 stretches and 3
  contradicted against off in one script at 1 live (s15_10), both where off gives the A/C, whose switch stands beside
  shelf_1 and shelf_4, the share of a delivery; 3 confirmed against on without the fact in every script. Findings, none
  ruled: the belief at a tick depends only on the facts at that tick (a window's edge before the arrival leaves the
  belief at arrival unchanged); with the A/C as the foreseeable task beside the lone delivery's shelf (P4), the early
  admission of the delivery lasts the whole A/C activation; admitted deliveries lose θ where a recency fact ends inside
  break_time, never where a window opens; the early admission also reaches a delivery with three live before a break
  begun inside it. Flags: the MPB instrument's `reference.py` drops a scenario's own timeline (no MPB scenario states
  one). Next: step 5, the planning cases (5.7 of the forward inputs).

QUESTION S, RULED (Hadi, 4 October 2026; AM65, its conceptual part in design_decisions.md under R3).
- The finding that led to the question, from step 4: within one walk the prior outweighs the movement evidence. In the
  reading for question G (below) the evidence alone ranked another hypothesis first on the tick the gate admitted, in 7
  of its 32 rows: the coffee break raised by break_time while the human walks to its neighbour, shelf_2 or the A/C
  switch (×1.18 to ×1.22), and item_4 while the human walks to the coffee machine with no fact holding (×1.90 to
  ×2.01).
- Ruled: the four strengths stay as ruled (AM38). They state the designer's knowledge and are not tuned to the movement
  evidence.
- A table of step 4's cases under compressed values is a sensitivity analysis for the close of T-K part 1, not a
  candidate design. Not built; it belongs to the close.
- UNDER DISCUSSION AGAIN since 4 October 2026 (the note in design_decisions.md under R3's AM65; THE DESIGN DISCUSSION
  AFTER STEP 5B, below). The ruling stands until Hadi rules.
- RESOLVED (AM70, Hadi, 4 October 2026; THE GATE AFTER STEP 5B, RULED, below): the strengths stay as ruled; the table
  of the cases at other values stays the sensitivity analysis for the close.

THE READING FOR QUESTION G (ccode, 4 October 2026; `analysis/kitting/irb/tk2/REPORT.md`, "The reading for question G",
and Appendix C; `analysis/kitting/irb/tk2/g_reading.py`). A reading of step 4's outputs, nothing run, nothing ruled.
Question G: admission and retraction under context knowledge; T-D G admits an assigned task on commitment warrant and
relies on retraction for a deviation.
- For every admission of a hypothesis not the true task with context knowledge on (32 rows, the exit walk apart): the
  belief, prior, hypothesis adequacy and warrant source at the admission; observation warrant and adequacy over the
  admitted ticks; from the off run of the same script, the first tick on which a rival is strictly above the admitted
  hypothesis and on which the true task is strictly first, with the two leading values' difference and ratio (ties
  reported, never given a first tick); the gate's ending and what the trigger rule would read against a record.
- Counts: 43 of 256 admissions of the true task rest on commitment warrant with no observation warrant on the
  admission tick, all 43 lone deliveries admitted on the previous task's pin tick (off: 0 of 148); in the 32 rows, 14,
  4 of them lone deliveries.
- What it shows: adequacy and warrant held on every admitted tick (the per-tick gate requires both; neither reads
  context knowledge); the evidence alone turns against an interrupted delivery 3 to 9 ticks after the human left, by
  small margins (×1.009 to ×1.25), and the trigger rule fires 3 to 8 ticks after that; a carried delivery is retracted
  on inadequacy 8 ticks after the break begins, before the evidence alone turns; the lone delivery admitted early
  lasts 43 to 60 ticks, the evidence alone near a tie (×1.0006 to ×1.009), with observation warrant held because the
  walk to the machine or the switch gains path toward its shelf; the trigger rule ends an admission later than the
  per-tick gate in 18 of 32 rows. Next: question G in the design chat.

QUESTION G, RULED (Hadi, 4 October 2026; AM66, its conceptual part in design_decisions.md under R7). The gate and the
retraction stay as ruled under context knowledge. The reasons and the consequences are stated there; the consequences
rest on THE READING FOR QUESTION G above (the late catch: the evidence alone turns 3 to 9 ticks after the human left,
the trigger rule 3 to 8 ticks later; the A/C beside the delivery's shelf: s15_19; the record kept 1 to 9 ticks past the
per-tick gate in 18 of 32 rows). Question G is closed.
UNDER DISCUSSION AGAIN since 4 October 2026 (the note in design_decisions.md under R7's AM66; THE DESIGN DISCUSSION
AFTER STEP 5B, below). The ruling stands until Hadi rules.
RESOLVED (AM67 to AM69, Hadi, 4 October 2026; THE GATE AFTER STEP 5B, RULED, below): question G reopened and ruled.
Observation warrant is required at admission for every hypothesis (AM67); the gate refuses a leader that the evidence
alone ranks below another live hypothesis (AM68); the end of an admission is unchanged (AM69). AM66 is superseded in
part (design_decisions.md, "T-K", under R7).

THE PLANNING CASES, RULED (KT15, Hadi, 4 October 2026; step 5 of T-K part 1). Amends KT3's "two cases also run in the
MPB".
- The planning cases are five, on env_layout_17. The case of the early admission is added; it replaces neither of
  KT3's two.
  1. The human takes a coffee break inside break_time (raised, in accord).
  2. The human delivers through the whole break_time (raised, against).
  3. No fact holds, and the human does the last delivery (ordinary, in accord: the early admission, correct).
  4. No fact holds, and the human takes a coffee break instead of the last delivery (ordinary, against: the early
     admission and its retraction).
  5. No fact holds, and the human activates the A/C instead of the last delivery (ordinary, against: the admission
     that the movement does not correct).
- Purpose: step 4 showed what the prior does to recognition; step 5 shows whether a changed admission changes the
  robot's decision, when the human acts in accord with the context and when not.
- Each case: the same script and the same robot task on up to three sides (context knowledge off; on without the
  raising fact for the true task; on with it), every verdict within one script; the robot's task conflicts with the
  human at the place and time where the admission differs between the sides; KT3's condition stands (the robot does
  not hold the items of the two shelves beside the A/C switch). Measures per side: each decision of the robot with its
  tick and the projection it rests on; the admissions and retractions as the meta-planner holds them, not the gate's
  tick-by-tick answer; the completion ticks; the separation.
- The step's rules: no script, window, robot task or expectation changes after a run with context knowledge on (a
  surprising result is a finding); it stops on a disagreement with the oracle that is not a plain defect, on a ruled
  case that cannot be given a conflict, and on anything that would need a change to a core algorithm. No change to the
  recognizer, the gate, the projection, the meta-planner or any ruled value. Three stages, a pause after each.

STEP 5B, PLANNED (Hadi, 4 October 2026). After step 5 and before dock_loading's part (step 6): the existing sets of
kitting run with context knowledge on, with no new authoring. First the recognition set (17 scenarios on
env_layout_10 and _11, the robot idle), then the planning set (16 scenarios on env_layout_12 to _14), read against its
coverage matrix (analysis/kitting/mpb/coverage.md). Purpose: to see what the prior does to the human's deviations,
which the context rooms exclude, and which authored decision paths remain when the prior changes the admissions. The
run files with context knowledge off stay each set's reference. Not part of step 5's session.

STEP 5, STAGE 1: THE PROPOSAL (ccode, 4 October 2026; not ruled, Hadi rules at the pause). Authoring runs with
context knowledge off only. The on sides' admissions are the IRB oracle's previews on the drafted scripts (no run with
context knowledge on); they equal step 4's ticks once shifted to the stretch's start.
- The disjointness rule (the robot's items and shelves disjoint from the human's; Hadi's question at stage 1).
  - With step 4's assignment (item_1 to item_4 on shelf_1 to shelf_4) it cannot hold: every shelf holds a human item,
    and KT3 excludes the two shelves beside the switch for the robot.
  - It holds with a reduced assignment: the human is assigned item_4 alone, the robot item_2 on shelf_2. The human then
    starts in the state of step 4's last delivery (live: item_4, coffee_break, ac_activation; the same walk from the
    table). With it every ruled case gets a conflict, all on the robot's first walk. With one kitting table, every
    later robot route is a ray from the table, as every human walk is, and two such rays come within min_separation
    only 60 to 130 cm from the table. A first walk from inside the room meets a human walk no later than tick 28 (a
    search over starts).
  - Alternative (a), the full assignment and a shared shelf (the robot's item in shelf_2's second slot): step 4's
    scripts run verbatim, but the human's 216-tick prefix with a working robot makes earlier admissions differ between
    the sides (a confound), the robot meets the human at shelf_2, and its routes stay rays from the table, so no
    conflict reaches the last delivery. No gain.
  - Alternative (b), a robot-side addition: a robot table and a robot shelf in a copy of env_layout_17 under a new id,
    off every human walk and its continuation. The robot's routes then cross the human's walks away from the table at
    times its chain of tasks sets, so a case can reach the human's turn at shelf_4 (ticks 44 to 48), the wait at the
    machine (42 to 71) and the walk after the break (from 73), where an admitted projection knows what the fallback
    does not; the table event below goes. Cost: a new room, "on env_layout_17" read as env_layout_17 plus robot-only
    objects (Hadi rules); no assigned task names the added objects, so the human's hypotheses are unchanged.
  - Recommended: the reduced assignment on env_layout_17 as it is; (b) only if the correct early admission is to be
    tested where the projection differs from a straight walk.
- What shapes the predictions (the authoring runs, off): on a straight walk the fallback projection (T-D P4)
  anticipates the conflict. Its expiries fall at 2, 6, 14 and 30, each projecting to the next, so a conflict from tick
  15 is seen at 14, and a hold of 2 to 6 ticks clears it (separation above 50 cm in every crossing tried). A correct
  early admission then moves the decision earlier and is not expected to change the hold's effect. A wrong one either
  displaces the fallback (no fallback is built while an admission stands) or holds the robot for a walk that does not
  come.
- The set. env_setup_16 on env_layout_17: item_4 on shelf_4 (the human's), item_2 on shelf_2 (the robot's), both to
  kitting_table_0; no default timeline. The human starts at (0, 450), is assigned deliver_item(item_4), and every script
  ends with the exit walk to corner_NE. The robot has one task, deliver_item(item_2), from a start per family.
  single_task only (with one task full_reorder has one ordering). Per family, off and on without the fact on a scenario
  with no timeline, on with the fact on a scenario stating its own timeline, the fact from tick 0 to the run's end (no
  edge inside an episode). scenario_s16_01 to _08, run files in configs/kitting/mpb/tk/, 12 runs.
  - F1 (s16_01; s16_02 break_time): deliver item_4. Robot from (-310, 90); its walk to shelf_2 meets the walk to shelf_4
    from tick 15 (8 cm unheld). item_4 admitted: off 47 (step 4: s15_01, +45), on without 0 (38 of 38 lone deliveries
    at their first observation), on with break_time 38 (s15_01, s15_18: +37, +39). Expected: off holds 2 at 14 on the
    fallback (the authoring run); on without decides its hold at 0 against the admitted plan; on with is off's up to
    38. Cases 3 and 2: nothing expected in ticks or separation; the decision's tick and place differ.
  - F2 (s16_03; s16_04 break_time): coffee_break, then deliver item_4. Robot from (-60, -480); meets the walk to the
    machine from 27 (17 cm unheld), 169 cm from the walk to shelf_4. coffee_break admitted: off 36 (s15_04, +36), on
    with break_time 22 (s15_04, +22); on without, item_4 0 to 42 (s15_19: 216 to 261; s13_13: 216 to 258), its
    retraction at 43, coffee_break from 55. Expected: off and on with hold 3 at 14 on the fallback (on with is below the
    threshold until 22), and on with re-decides at 22 with no further hold: case 1, nothing expected. On without: no
    hold, the robot passes the human at about 17 cm at 27 (the wrong admission displaced the fallback; a case 4
    consequence, read beside F3).
  - F3 (s16_05; s16_06 break_time): F2's script. Robot from (-310, 90); meets the walk to shelf_4 at 15, where on
    without's projection puts the human, 103 cm from the walk to the machine. Expected: off and on with, no hold (the
    authoring run: none); on without, a hold of a few ticks at 0 for a walk that does not come (case 4, a cost in
    ticks). The retraction at 43 comes after the robot has passed.
  - F4 (s16_07; s16_08 room_warm): ac_activation, then deliver item_4. Robot from (-475, -408); meets the walk to the
    switch from 27 (8 cm unheld), 63 to 85 cm from the walk to shelf_4. Admitted: off nothing until 63; on without
    item_4 0 to 45 (s15_19: 216 to 261); on with room_warm nothing until 47 (the A/C below the threshold, s15_10: 0.60
    at its arrival). Expected: off and on with hold 6 at 14 on the fallback; on without, no hold, the robot passes the
    human at about 8 cm at 27 (case 5, a cost in separation, the robot moving).
- The shared table. In every authoring run the robot completes (declared 69 to 92) before the human returns to place
  item_4 (89, 135, 135, 99), then stands at the table with an empty pool, 3 to 22 cm from the human's placement: a
  standing robot, not robot-responsible under F1, the same on every side while the robot completes first, which the
  expectations check. It confounds no verdict; the separation is reported per conflict window and over the run with
  F1's class. No two deliveries finish together in this set.
- Not shown on env_layout_17 as it is: the correct early admission where the projection differs from a straight walk
  (a turn, a stand); any planning consequence of case 4's retraction (at 43, after every reachable conflict). Further
  cases proposed, both needing (b): E1, a correct early admission at a turn (the robot meets the human's carry back
  from shelf_4 or the human at the shelf); E2, the lone delivery admitted early after an observed break (the recency
  fact: item_4 at 73 on both on sides against 97 off, on the walk from the machine), direction 4 reaching planning.

THE ROOM, RULED (Hadi, 4 October 2026, on stage 1's proposal): option (b). A copy of env_layout_17 under a new id with
additions for the robot only; the human's side unchanged; the disjointness rule holds. It serves KT3's "on
env_layout_17". Reason: in the room as it is, a conflict exists only on a straight walk, where the fallback projection
already holds the robot, so the set could show a cost of context knowledge and never a gain. Conditions: each case's
conflict placed where the projection of the admitted task differs from the fallback projection (a turn, a stand, the
walk back); case 4 reaches the retraction (a conflict that the retraction and the decision after it can change).
THE STEP'S MODE AND SIZE (Hadi, 4 October 2026). ccode decides the room's additions, the scripts, the robot's tasks, the
windows and the further cases by the conditions given, without approval, and does not wait at the stage boundaries
(commit, the result in a few lines, the next stage); it stops only on a blocking condition (a disagreement with the
oracle that is not a plain defect; a ruled case with no conflict; a change to a core algorithm or a ruling). The step
is a basic check that context knowledge works through the planning chain, not a coverage set. In order: (1) the chain
works (the held admission, the projection and the decision follow as the oracle and the reference state); (2) a gain
where the human acts in accord with the context, one instance for the raised state (the coffee break inside
break_time, the stand at the machine) and one with no fact (the last delivery, at a turn or on the walk back); (3) a
cost where the human acts against it (cases 4 and 5; in case 4 what the retraction and the decision after it change).
One script and one robot task per case; E1 and E2 only as the form a ruled case takes; at most about 8 scenarios and
20 runs; one strategy; no variants of a window's position and no second room; the clearest instance of each point.
The report leads with the three points.

STEP 5, STAGE 1, REVISED: THE SET (ccode, 4 October 2026, by the rulings above; supersedes the set and the predictions
of STEP 5, STAGE 1: THE PROPOSAL, whose disjointness reading and fallback finding stand). Authoring runs with context
knowledge off; the on sides' admissions are the IRB oracle's previews (no run with context knowledge on).
- The room env_layout_18: env_layout_17 and three robot-only objects. kitting_table_1 at (440, -450), the robot's table
  in the south-east corner, so no robot delivery ends at the human's table (the table event of the first proposal goes)
  and the robot's routes cross the human's walks away from kitting_table_0. shelf_5 at (-470, -400), on the west wall:
  its carry to kitting_table_1 runs along the south wall and passes 4 cm from the point where the human stands at
  shelf_4 (148, -438) and turns north. shelf_6 at (480, -60), on the east wall between the coffee machine and shelf_2:
  its carry to kitting_table_1 passes the point where the human stands at the machine (460, -253). None lies on a human
  walk or on its straight continuation, so the fallback's cut is env_layout_17's.
- The human keeps a reduced assignment: deliver_item(item_4) alone, from the table at (0, 450), every script ending
  with the exit walk to corner_NE. Its state is step 4's last delivery (live: item_4, coffee_break, ac_activation; the
  same walk); step 4's ticks hold shifted to the stretch's start (item_4 at 0 / 38 / 47; coffee_break at 22 / 36;
  item_4 wrongly 0 to 45 before the A/C, as s15_19). Cost: the scripts are not step 4's verbatim, and a lone
  delivery starts with no previous task's pin tick, so its early admission comes on the first tick, not the pin tick.
  Step 4's full scripts would put a 216-tick prefix with a working robot before every case.
- env_setup_16: item_4 on shelf_4 to kitting_table_0 (the human's); item_5 on shelf_5 and item_6 on shelf_6 to
  kitting_table_1 (the robot's). No default timeline; a fact from tick 0 to the run's end where a side needs it.
- Three scripts, six scenarios, nine runs, single_task, one robot task each:
  - scenario_s16_01 (no timeline; off, on) and _02 (break_time): the delivery. Robot from (-470, -120), item_5. Cases 3
    and 2: the turn at shelf_4 (the human stands 45 to 47, steps north at 48). Off has no projection past the arrival:
    its robot is moving 42 cm from the human at 44 and then stands 42 cm from it through the turn (holds at 45 and
    47; the authoring run). Expected: on without the fact holds at 0 against the admitted plan, its separation stays
    above 50 cm (case 3, the gain with no fact; E1 is this case's form); on with break_time behaves as off until 38,
    then holds at 38, 7 ticks before the turn (case 2).
  - scenario_s16_03 (no timeline; off, on) and _04 (break_time): coffee_break, then the delivery. Robot from (-200, 0),
    item_6, unheld 36 cm from the machine point at 43 and 12 cm at 45, 144 to 191 cm from the item_4 projection. Off
    holds at 36 (coffee_break admitted) at shelf_6, and at 72, when the break ends, rests on the observed stand of 30
    ticks and holds to 97 while the human left at 74. Expected: on with break_time decides the same hold at 22 (case 1,
    the gain in the raised state: the stand known 14 ticks earlier); on without rests on item_4 until 43, with no
    hold, and the retraction at 43 is the decision that stops the robot short of the standing human (case 4: the cost,
    and what the retraction changes); both on sides admit item_4 at 73 after the observed break and need no stale
    hold (E2's form; an observation of this script, not a further case).
  - scenario_s16_05 (no timeline; off, on) and _06 (room_warm): ac_activation, then the delivery. Robot from
    (400, 210), item_5, crossing the walk to the switch westward at about 24 (29 cm unheld), 67 to 84 cm from the
    item_4 projection. Off holds 5 at 14 on the fallback. Expected: on without the fact makes no hold and passes the
    human at about 29 cm, the robot moving (case 5: the admission the movement does not correct); on with room_warm
    admits nothing on the walk and holds as off.
- Not taken (the flags of the final report): the needless hold for a walk that never comes (case 4's other form, from
  the first proposal); case 5 at the human's turn east at the switch; E2 as a separate case.
STEP 5, STAGE 2: AUTHORED (ccode, 4 October 2026). env_layout_18, env_setup_16, scenario_s16_01 to _06, the run files
in configs/kitting/mpb/tk/ (on) and configs/kitting/mpb/tk/off/ (off); the expectations committed before any run with
context knowledge on (the oracle's tables, md5s and the expected chains in analysis/kitting/mpb/tk/README.md; the
declared properties PK1 to PK5 in analysis/kitting/mpb/properties.py). The instrument: reference.py carries a
scenario's own timeline (the flag of step 4, a plain defect); the six scenarios have their reference run (CONTROLS);
tk5.py reads the set. Audit: the existing control scenario_s10_06 rerun through the instrument is byte-identical
(properties, diff, separation, reference, decisions, expectations; the log but for its header lines); the tests pass
with the registry's counts updated (134 scenarios, setups 01 to 16).
STEP 5, KITTING, THE PLANNING CASES: DONE (ccode, 4 October 2026; analysis/kitting/mpb/tk/REPORT.md). Nine runs, 0
disagreements with the oracle; in every run the completion is the robot-alone reference plus the executed holds.
Gain in accord: case 1, the stand's hold decided at 22 against 36, the same outcome; case 3, the hold decided at 0
against 45 and 47, 1 tick and 4.7 cm in the minimum, min_separation not kept (41.7 cm). Cost against: case 5, a pass at
28.3 cm with the robot moving (4 violation ticks), room_warm restoring off's decision; case 4, no decision until the
retraction at 43, whose decision held the robot at 55.5 cm (off 95.0). Case 2: break_time delays the correct admission
to 38, the pass 29.3 cm. Findings, none ruled: at the turn the admitted plan runs about one tick and 18 cm ahead of the
executed human (TODO-146), so a planned 54.8 cm became 41.7; off's stand fallback after the coffee break holds 25 ticks
while the human walks away (TODO-132 (a)), the largest difference in ticks (113 against 89 and 90), ended on the on
sides by the lone delivery's admission at 73. Next: step 5b.
STEP 5B, KITTING, THE EXISTING SETS WITH CONTEXT KNOWLEDGE ON: DONE (ccode, 4 October 2026; three stages with no pause,
as Hadi ruled; analysis/kitting/mpb/tk5b/REPORT.md, one report for both sets; the READMEs of analysis/kitting/irb/tk5b/
and analysis/kitting/mpb/tk5b/). No authoring: the recognition set (17 scenarios, env_layout_10 and _11, the robot
idle) and the planning set (16, env_layout_12 to _14, single_task) run with context knowledge on from copies of their
run files (configs/kitting/{irb,mpb}/tk5b/); the run files with it off stay the reference, rerun at HEAD first and
byte-identical. No timeline in these setups: only the state with no raising fact occurs. Expectations committed before
any run (398d890); runs 613803b. First, step 5's two accepted suggestions recorded in TODO-146 and TODO-132 (a)
(aa73ce3).
- The chain: 33 runs, 0 disagreements with the oracle; the control equals its reference; scenario_s10_11 (no
  foreseeable task in the room) identical to off but for the [run] field and the [IR-context] lines.
- Recognition: every delivery admitted earlier or at the same tick (the first of two at 8 against 25; a lone one on
  its stretch's first tick); the coffee break 18 to 30 ticks into its stretch against 10 to 12. New wrong admissions:
  the lone delivery while the human walks to a coffee break between deliveries (22, 22, 18 ticks); the interrupted
  delivery kept longer by the gate (11 against 5, 8 against 2, 16 against 11), by the trigger rule about as long as
  off's; the misdelivered item and the assigned delivery beside an unassigned one admitted as the lone assigned task
  (17 and 11 ticks).
- Planning: 12 of 16 authored cases reached; not reached: scenario_s10_08 (the cause boundary at 33 in place of
  replaced through coffee_break), s10_10 (no dip below θ: E6), s11_01 (the switch at the retraction of 16, not at an
  expiry: P6.1), s11_03 (no switch while carrying: D9; item_8 released 11.3 cm from the standing human, 2 F1 violation
  ticks, completion 35 against 113). In the s11 scenarios the assigned delivery the human never performs is admitted
  at tick 0 on its prior of 0.98 and retracted at 10 or 16; the evidence cannot separate it from coffee_break while the
  human stands. The lone foreseeable hypothesis (s10_05) and the hold at the coffee machine (s12_02, hold 18 at 93
  against 75) are reached.
- Findings, none ruled: with context knowledge on, the coverage matrix's E6, D9 and A8 have no instance in the set and
  A4 has a second (s10_08; coverage.md's A4 derivation assumes the equal prior's tie order); P6.1, P10.10 and P11.3a to
  c fail; the trigger rule and the gate agree more often (the record outlives the gate in 2 rows against 7).
  Suggested: scenario_s11_03's 11.3 cm as a measurement under the KT11 consequence or TODO-132 (a). Next: dock_loading's
  part (step 6).
CONTEXT KNOWLEDGE ON AGAINST OFF, AN OVERVIEW (ccode, 4 October 2026, at Hadi's request; analysis/kitting/mpb/tk5b/
COMPARISON.md and comparison.py; existing outputs of steps 4, 5 and 5b only, no run, no ruling): the true task admitted
earlier in 206 of 325 true stretches (3005 ticks) and later in 42 (365 ticks; the coffee break with no raising fact 24
of 28); admissions of a hypothesis that is not the true task during modelled tasks 17 off, 47 on (gate ticks 114, 504),
by the evidence alone 0 near-ties, 17 the true task first with the prior overruling, 26 the evidence itself ranking the
admitted one first, 4 with no true hypothesis; planning completion better in 7 of 22 runs, worse in 2 (134 ticks gained,
3 lost); cases below min_separation 2 off, 5 on (2 wrong admissions, 2 TODO-146 at a turn, 1 other). The scenarios are
authored: the counts compare the settings and are no rate of occurrence.
THE LIMITATION OF ADMISSION FROM CONTEXT AND MOVEMENT (Hadi, 4 October 2026; recorded by ccode the same day;
CORRECTED the same day by Hadi, the first wording being the design chat's and wrong). Recorded in docs/assumptions.md,
6.4. An admission of a hypothesis that is not the true task, read against the evidence alone (the run with context
knowledge off), has two parts. In the first ticks of a walk the evidence for two targets is nearly equal (18 ticks, the
ratio within ×1.01 of 1, the smallest ×1.0008; no tick an exact tie); only this part is a limit of the situation. After
it the evidence ranks the true task first, weakly at first and by about ×3 to ×14 at the end of the walk (×3.05 to
×14.2), and the prior overrules it (293 ticks); this part follows from the declared strengths and the gate (questions S
and G). 141 further wrong ticks have the evidence alone ranking the admitted hypothesis first (the off run admits most
of them too). The ratios are reported with no cut between separating and not separating; ×1.01 is COMPARISON.md's
reporting threshold. The largest gain and the largest costs come from one mechanism, a lone assigned task admitted
before the human starts it (59 correct, 9 not; both new planning cases below min_separation). Not settled there: how
the meta-planner acts on an admitted hypothesis that can be wrong (THE DESIGN DISCUSSION AFTER STEP 5B, below, not
ruled); communication (T-D X). Numbers: analysis/kitting/mpb/tk5b/COMPARISON.md and WHATIF.md.
TWO WHAT-IF READINGS, X AND Y (ccode, 4 October 2026, at Hadi's request; analysis/kitting/mpb/tk5b/WHATIF.md and
whatif.py; filters on the recorded gate answers with context knowledge on of step 4 and step 5b's recognition set, not
runs; no ruling). X: admissible only where the evidence alone ranks no other live hypothesis strictly above; Y:
observation warrant required. The true task's 216 earlier admissions: X keeps all; Y delays the 59 lone assigned tasks
admitted on a completion tick by 1 tick. Wrong admissions of kind (ii) (17 rows, 310 ticks): X leaves 18 ticks, Y 302,
both 11; of kind (iii) (26, 149): X 122, Y 72, both 55. scenario_s16_05's admission is refused by X (not by Y),
scenario_s11_03's by Y (not by X), both by X and Y together. Changes of the answer within a true stretch: 673 recorded,
653 X, 579 Y, 560 both.
THE DESIGN DISCUSSION AFTER STEP 5B (the design chat with Hadi, 4 October 2026; recorded by ccode the same day). A
DISCUSSION, NOT RULED. Hadi continues it in the next design chat and rules there. CLOSED (Hadi, 4 October 2026):
ruled the same day, THE GATE AFTER STEP 5B, RULED, below (AM67 to AM72). Nothing below carries a ruling
number; each point is attributed. Rulings S (AM65) and G (AM66) stand as recorded until Hadi rules (their notes of
4 October 2026, design_decisions.md, "T-K", under R3 and R7). No order of the remaining work is decided.
- The problem as discussed. After an admission the meta-planner uses the projection of the admitted task alone. The
  projection is the same for a belief of 0.76 and of 1.0, and the same with and without observation warrant. Context
  knowledge makes the belief high earlier, also before any movement.
- The changes discussed, with their labels:
  - 1.A (prior): a larger ordinary strength only; 0.1 and 0.2 were named as values to compare; the raised and the
    suppressed strengths stay.
  - 2.A (gate): commitment warrant alone does not admit; observation warrant is required.
  - 2.B (gate): the leader is admitted only if the evidence alone ranks no other hypothesis above it.
  - 3.A (projection): an admitted task without observation warrant is projected as the human staying at the observed
    position until the human moves.
  - 3.B (meta-planner): the robot's plan is checked against the admitted task's projection and the fallback projection
    together.
  - 4.A (response): communication or slowing down when the admission is weak (T-D X).
- Hadi's positions in the discussion (not rulings):
  - Hadi does not want 3.B in this framework: it changes the meta-planner and mixes high-level planning with a lower
    level; the framework's objective is IR → AP, to show what recognition contributes, not to run a perfect
    simulation. Hadi sees 3.B as possibly part of future work on planning that uses the belief.
  - A ruled decision can be reopened if there is a good reason. Hadi asked why 1.A is not reopened.
  - Some admissions of a hypothesis that is not the true task are sound reasoning: the human did the less probable
    thing.
- The design chat's suggestions (not confirmed by Hadi):
  - A principle for the gate: context knowledge may make an admission earlier; it may not admit a task that the
    observation does not show.
  - 2.A as necessary. With context knowledge on, the admission before movement gains 1 tick in the 59 correct cases and
    produces the 11.3 cm case (scenario_s11_03). It would reverse the part of T-D G that admits an assigned task before
    any movement.
  - 1.A and 2.B as two candidates for the same problem (the prior overruling the evidence), to be decided from numbers.
    Unknown for 2.B: how much gain it keeps, and whether the admission switches on and off at ratios near 1. For 1.A: a
    new value needs an argument about its meaning from Hadi (by the proposed reading of a strength, AM39: 0.02, 1 of 51
    task starts; 0.1, 1 of 11; 0.2, 1 of 6).
  - 3.A not needed if 2.A is taken. 4.A as future work.
  - The reasons it gave for looking at S and G again: its argument for S used an estimate (one walk shifts the belief
    by a factor of 3 to 4) that the data corrected (12 to 14); its argument for G (a), that an evidence condition acts
    on differences of 0.0002, holds only in the first ticks of a walk.
  - Which measured case each change would cover. The standing human (scenario_s11_03, 11.3 cm): 2.A yes, 2.B no. The
    walk to the A/C switch (scenario_s16_05, 28.3 cm): 2.A no; 2.B on a ratio of 1.003 to 1.09; 1.A at 0.2 yes (the
    lone delivery's prior is 0.71, below the threshold, in a room with two foreseeable tasks). The wrong admissions of
    43 to 60 ticks: 2.B after the first ticks; 1.A shortens them. The gap between plan and execution at a turn
    (TODO-146) is a separate defect that none covers.
  - A table that could inform the ruling, from existing outputs with no simulation run: the recognition sets under
    2.A, under 2.B, under 1.A at 0.1 and at 0.2, and their combinations, each as gains kept, wrong admissions removed,
    and switches within a stretch. For the strengths the oracle recomputes the belief, since the human's trajectories
    do not depend on them. It would also serve as the sensitivity table that question S planned for the close.
- Questions put to Hadi, unanswered: the direction for the gate and the prior; whether that table is wanted; whether
  the coverage matrix of the planning set stays the matrix of the off setting with one added column for context
  knowledge on, or new scenarios are authored; the order of the remaining work.
- ccode's notes, facts from the repository for the next chat (no position):
  - WHATIF.md (6f11c13) already holds part of that table. Its filter Y is 2.A and its filter X is 2.B (the evidence
    alone ranks no other live hypothesis strictly above the leader, by more than 1e-9), each alone and together, on
    step 4's 57 runs and step 5b's 17 recognition runs with context knowledge on. X keeps all 216 earlier admissions of
    the true task; Y delays the 59 lone assigned tasks by 1 tick. Changes of the answer within a true stretch: 673
    recorded, 653 under X, 579 under Y, 560 under both. Missing: 1.A and its combinations. With the robot idle the
    belief, adequacy and warrant do not depend on the gate, so the filter's per-tick answer is the answer a run would
    give; the decision record and the trigger rule are not recomputed.
  - 2.A also reverses T-K's R7 as amended by AM5 (an assigned task may be admitted before any distinguishing movement,
    on its commitment warrant) and KT11's RULED line for the expected directions (a lone live assigned task admitted
    early on its commitment warrant).
  - scenario_s16_05, the off run, the ratio of the A/C activation over deliver_item(item_4): ×1.0014 at tick 0 (the
    admission), ×1.0029 at 1, ×1.09 at 25 and 26; the discussion's "1.003 to 1.09" starts at tick 1.
THE GATE AFTER STEP 5B, RULED (Hadi, 4 October 2026, in the design chat; recorded by ccode the same day; AM67 to AM72).
The conceptual part is in design_decisions.md, "T-K": Hadi's principle, AM67, AM68, AM69, AM71 and AM72 under R7; AM70
under R3. It closes THE DESIGN DISCUSSION AFTER STEP 5B above and resolves the notes on questions S and G. Records only;
nothing built.
- The rulings in brief. AM67: observation warrant is required at admission, for every hypothesis; commitment warrant
  alone no longer admits; a lost observation warrant still ends nothing. AM68: the gate refuses a leader that the
  evidence alone ranks below another live hypothesis; rank only, a tie passes, no constant, no margin; a condition of
  admission only. AM69: the rule on when an admission ends (T-D L) is unchanged; a stated limitation. AM70: all
  strengths stay as ruled. AM71: 3.A, 3.B and 4.A not taken; 3.B and 4.A possible future work. AM72: the cases that
  remain are limitations, not defects (docs/assumptions.md 6.4).
- The discussion's labels: 2.A is AM67; 2.B is AM68, as a condition of admission only; 1.A is not taken (AM70); 3.A,
  3.B and 4.A are not taken (AM71; TODO-97 for 3.B, TODO-96 for 4.A).
- The measured basis (analysis/kitting/mpb/tk5b/WHATIF.md; filters on recorded answers, not runs; the robot idle,
  except the two planning rows). Y, the reading of AM67: the 59 lone assigned tasks admitted on the previous task's
  completion tick come 1 tick later, still earlier than with context knowledge off; scenario_s11_03's admission (0 to
  10) is refused. X, the reading of AM68: all 216 earlier admissions of the true task keep their tick; scenario_s16_05's
  admission (0 to 21) is refused. Both together leave 11 of the 310 wrong gate ticks of kind (ii) and 55 of the 149 of
  kind (iii). In a run with the rules built the later ticks change too; a filter does not show it.
- The strengths (AM70): the table of the cases at other values stays the sensitivity analysis for the close of T-K
  part 1 (QUESTION S, RULED, above).
- What becomes stale, each marked with a pointer: here, KT11's RULED line and THE STRENGTHS REVISED, C, its RULED
  sentence; QUESTION S's and QUESTION G's notes (resolved). In design_decisions.md: R7's first sentence and AM5, AM6's
  gate policy, AM66 in part (under R7); "T-D G: admission", AD1's commitment source and its consequences, AD2 (a note),
  AD3's derivation in its delivery case; "T-D L", L2 (a line: unchanged). docs/assumptions.md 6.4; docs/
  context_knowledge_method.md, sections 8, 12 and 15; docs/glossary.md §5 (θ) and §7 (warrant, observation warrant,
  commitment warrant, warranted / unwarranted, admitted).
- The term, PROPOSED, NOT RULED (ccode, 4 October 2026; Hadi rules). AM68's condition has no glossary term. Proposed:
  "outranked": a live hypothesis is outranked when the evidence alone ranks another live hypothesis strictly above it;
  the refusal reason `none(leader_outranked)`. Recorded as proposed in docs/glossary.md §7.
  RULED (AM73, Hadi, 4 October 2026): the term and the refusal reason are accepted; the proposed marks are removed.
- Open, not ruled: the order of the remaining work; whether the planning set's coverage matrix stays the matrix of the
  off setting with one added column for context knowledge on, or new scenarios are authored; the build of AM67 and
  AM68, which starts with a plan step in its own session (BUILD DISCIPLINE).
- ccode's facts for the build's plan (the review of these records, 4 October 2026; read from the existing logs and the
  code, nothing run; no position):
  - Commitment warrant in the maintained sets. 17 of the 48 logs hold one admission each on commitment warrant alone
    (`[meta-proj] ... projection=built warrant=commitment`): the lone last delivery at b + 1, at confidence 1.000, all
    with assignment knowledge on (tb1a 3, tb1b 2, tb1c 4, tb3 8). 65 admissions name both sources, 113 observation
    alone. Under AM67 the 17 are refused and come on a later tick, so AM67 changes behaviour and the maintained sets
    are regenerated with it. After AM67 no admission can depend on commitment warrant: in the code it is read only by
    the gate (`MetaPlanner._warrant`, `_clears_gate`) and by admission's log line.
  - The test-bed sets. The MPB holds 7 commitment-only admissions in 6 of its 50 log files, step 5's set 4 in 4 of its
    18 (scenario_s16_03 to _06, context knowledge on), step 5b's 18 in 15 of its 17; the IRB (robot idle) logs none, but its oracle computes the gate per tick with commitment
    warrant (analysis/instruments/irb/oracle.py), as the MPB's does (analysis/instruments/mpb/mpb_oracle.py). The MPB's
    coverage cell B5, "clears by commitment only" (scenario_s10_04 at 134; analysis/kitting/mpb/coverage.md), becomes
    unreachable by construction, and the MPB alteration C1, "commitment warrant ignored"
    (analysis/instruments/mpb/alteration.py), becomes the rule.
  - What AM68 requires the recognizer to report. `BeliefState` carries the belief over H (`belief`) and the prior
    (`prior`, empty with context knowledge off), not the evidence; the recognizer holds the normalised evidence over H
    internally (`Recognizer._evidence`). The gate reconstructs no recognizer quantity (T-D G, AD2), so dividing the
    belief by the prior in the gate is excluded, and with context knowledge off there is no prior to divide by. A new
    recognizer output is needed: either the evidence over H, which the gate compares by rank for the leader, or a
    categorical value per live hypothesis that the gate reads for the leader only, as it reads hypothesis adequacy and
    observation warrant. Which one, its line in `[IR]`, and the place of the check in the gate's order (it decides
    only the printed refusal reason) are the plan's.
  - With context knowledge off the belief is the normalised evidence bit for bit (`Recognizer._belief`), so AM68
    refuses nothing there: its build can leave the maintained sets identical except the lines it adds. AM67 changes
    them (above).
  - Rank only, with no constant, makes the comparison exact. WHATIF's filter X counted "strictly above by more than
    1e-9"; the built rule may differ from X where two evidence values differ by less than 1e-9 (none on the 453 wrong
    ticks with a true hypothesis; no tie within 1e-9 there). An exact tie occurs on a boundary tick, where the evidence
    restarts equal (scenario_s14_19 at 180, 1/3 each); there AM67 refuses (no observation warrant).
  - AM68 acts where `_clears_gate` is asked: at admission and on the entering side of `recognition_changed`, as warrant
    does (AD3); not on retention.
  - AM72's first case, the first ticks of a walk with equal evidence. The 18 measured ticks of 6.4's first part rank
    the true task first by ×1.0008 to ×1.01; AM68 refuses them, and the boundary tick before them is refused by AM67.
    In the measured sets none of them remains under both; what remains of the case is an exact tie with observation
    warrant, or near-equal evidence that ranks the admitted hypothesis first.
  - AM70's reason. Under AM68 which hypothesis is admitted no longer depends on the strength values (the evidence must
    rank it first or tie). Whether and how long a leader the evidence ranks first stays at the threshold still does:
    the 55 ticks of kind (iii) left under X and Y are such admissions.
- RULED ON THIS RECORD (Hadi, 4 October 2026; AM73 to AM76, the conceptual part in design_decisions.md, "T-K", under
  R7 and R3). AM73: the term "outranked" and `none(leader_outranked)` accepted. AM74: AM72's first case reads "a
  near-tie in the evidence that favours a hypothesis the human is not doing" (as first worded it does not occur: AM67
  and AM68 refuse those ticks in the measured sets). AM75: "a tie passes" is an exact comparison, with no tolerance (no
  number in the rule); the 1e-9 of WHATIF's filter X is a reading's agreement level, not the rule. AM76: for the
  outranked condition the recognizer reports one category per live hypothesis, read by the gate for the leader only
  (the gate reconstructs no recognizer quantity and receives no raw value); of the two options in ccode's facts above,
  the second. ccode's correction of AM70's reason (the fact above) is accepted as recorded (design_decisions.md, under
  R3's AM70, CORRECTED). The plan of the build: docs/handoffs/plan_T-K_gate.md.
THE GATE'S BUILD PLAN, RULED (Hadi, 4 October 2026, on ccode's plan, docs/handoffs/plan_T-K_gate.md, e4147bf). The plan
is approved with these rulings on its decisions D1 to D7; the plan is amended to them.
- D1 (a): the outranked check stands last among the gate's refusals, after `none(leader_unwarranted)`. Reason: every
  tick refused today keeps its printed reason, so a log difference shows this ruling's effect alone.
- D2 (a): commitment warrant's parts are removed from the meta-planner (the constructor argument
  `observed_assigned_tasks`, the matching by `same_task` in `_warrant`, `WarrantSource.COMMITMENT`); the admission
  line keeps its warrant field (`[meta-proj] projection=built warrant=observation`, AD4 unchanged). Reason: an input
  that decides nothing invites a later role the rulings removed. The recognizer's support restriction is untouched.
- D3 (a): the IRB oracle marks the rank undetermined where its own two evidence values lie within its agreement level
  (1e-9); the comparison skips and counts those ticks. Reason: the rule stays exact (AM75); the tolerance is the
  instrument's.
  AMENDED (Hadi, 5 October 2026, in step 5d): the oracle treats exactly equal evidence as a tie, not outranked;
  "undetermined" stays for values that are close but not equal. Reason: the oracle stays independent of the run and
  now checks that a tie passes. Occasion: step 5d stopped on the gate's answer at 135 in scenario_s10_04 and s12_02,
  which the oracle could not determine (coffee_break's re-entry with one delivery live: the evidence exactly 1/2 each by
  the re-entry rule). Built in oracle.py's rank() and rule 34 (analysis/kitting/irb/README.md); C5 retargeted to an
  exact tie counted outranked.
- D4 (a): the planning set's coverage matrix stays the matrix of the setting with context knowledge off, with one added
  row for the outranked refusal, claimed with context knowledge on, its instance from step 5's existing scenarios. No
  new scenario. This closes the open question on the coverage matrix (THE DESIGN DISCUSSION AFTER STEP 5B, question 3).
- D5 (a): step 5's properties that the rulings move (PK4a, PK4b, PK4c, PK4e, PK1b, PK5a, PK5b) are re-declared before
  the measurement runs; the old ones stay in the record, marked superseded; the separation stays a measure, not a
  property.
- D6 (a), narrowed: the three new alterations (C4 the outranked condition not asked, C5 a tie refused, C6 the rank read
  from the belief instead of the evidence) run on step 5's six scenarios only. On the planning set's sixteen, with
  context knowledge off, they cannot be detected by construction: stated as a property of that set, not run there.
  C1 (commitment warrant ignored) is retired by AM67.
- D7 (a): a mathematical tie decided by float rounding is accepted and recorded as a consequence of the exact
  comparison (design_decisions.md, "T-K", R7's AM75, its consequence line).
Open after it: the order of the remaining work. Next: the build, stages 0 to 5 of the plan, each committed after its
check, with a pause at each stage boundary; the measurements with context knowledge on are a separate step after it.
THE GATE RULINGS, BUILT (ccode, 4 October 2026; by the approved plan, docs/handoffs/plan_T-K_gate.md, with D1 to D7;
the session's state file docs/handoffs/build_T-K_gate_state.md). Six commits, each after its check, a pause at each
stage boundary.
- Rulings on the plan: 3a4f00b. Stage 0, B0 at 3a4f00b (no commit): the scope (the four maintained sets, the IRB's s08
  and s09, round 1, the MPB under both strategies and prior off, dock_loading's six milestones with context knowledge
  off, pytest) byte-identical to the repository's outputs; one external copy of the untracked data,
  /home/hadi/teamrob_analysis_2026-10-04_gate/.
- Stage 1, 2c939a5 (AM76): `EvidenceRank`, `BeliefState.evidence_rank`, `Recognizer._evidence_rank()` from the
  normalised evidence by exact comparison (AM75); logged on its own line `[IR-rank]` (the plan amended: a field of
  `[IR]` would have broken the IRB instrument's parsers before stage 4). Check: 1298 outputs identical to B0 after
  dropping the `[IR-rank]` lines; the leader never outranked on 50,734 ticks with context knowledge off.
- Stage 2, 02956ba (AM68, D1): `none(leader_outranked)`, asked last in `_clears_gate`. Check: 1298 outputs
  byte-identical to stage 1 (context knowledge off: nothing outranked).
- Stage 3, 725d673 (AM67, D2): observation warrant required for every hypothesis; `WarrantSource`, `_warrant` and
  `observed_assigned_tasks` removed from the meta-planner; `[meta-proj] projection=built warrant=observation`. Check:
  the 17 maintained logs and the MPB's s10_04, s10_11, s12_02 (both strategies) first differ on their commitment-only
  admission's tick, every other log identical after the warrant text; every `.rec` identical; the IRB's gate column 7
  ticks in 5 runs, round 1's 41 in 6; no maintained completion moved; MPB full_reorder completion s10_04 137 to 139,
  s10_11 139 to 138.
- Stage 4, 8357b74 (the instruments): the IRB oracle's `rank` column and gate (no commitment; outranked last;
  undetermined within its agreement level, D3), rules 23 (amended) and 34 to 36; the MPB's oracle, chain, compare and
  Gate; the alteration test (C1 retired, C4 to C6 for step 5 only, D6). Check: every log identical to stage 3; 0
  disagreements in the IRB's 17 and round 1's 31 (s14_02's known flag apart), 972 rank cells undetermined (exact
  ties), no gate undetermined; 0 on parts 1 to 3 in the MPB's 32 prior-on runs; every declared property holds.
- Stage 5, the records commit: the regenerated outputs in the repository; the maintained sets' and the test-beds'
  README sections; coverage.md (B5 unreachable by ruling, B7 not a distinct path, B12 claimed with context knowledge
  on); the BUILT lines in design_decisions.md, the glossary, the method document, docs/assumptions.md and the handoff.
- Not in the build, the measurement step's (the plan's section 8): the runs with context knowledge on (steps 4, 5, 5b);
  step 5's re-declared properties before them (D5); C4 to C6 on step 5's six (their actual files are the pre-build
  runs until then); B12's instance.
- ccode's decisions in the build: the `[IR-rank]` line; the MPB instrument's warrant hook at stage 3; the oracle's band
  marks an exact tie undetermined (D3 as worded), so the exact-tie side of the rule is checked by the unit tests only;
  the alteration engine finds a run file below configs/<domain>/mpb/; unused imports removed.
STEP 5C AND STEP 5D NAMED (Hadi, 5 October 2026): step 5c is the gate after step 5b (the discussion, the records, the
plan, the build above); step 5d the measurements after the gate change. Steps 6 and 7 keep their numbers. The steps
of T-K part 1 stand as one tree at the top of docs/handoffs/T-G_forward_inputs.md, section 5, kept current at each
step's close.
STEP 5D, THE MEASUREMENTS AFTER THE GATE CHANGE: DONE (ccode, 5 October 2026; analysis/kitting/tk5d/REPORT.md, the
step's one document). With context knowledge on, no new authoring: step 4's recognition runs (57 and its 2 off runs),
step 5's planning cases (6 and 3 off), step 5b's recognition (17) and planning runs (16), against the updated oracles.
- Before the runs (f02b04c): the expectations from the updated oracles; step 5's moved properties re-declared (D5):
  PK4a.r, PK4b.r, PK4e.r, PK1b.r, PK5a.r, the old ones kept in properties.py's docstring, marked superseded; PK4c and
  PK5b without successor, the separation a measure.
- A stop on the step's blocking condition (a gate answer the oracle cannot determine: s10_04 and s12_02 at 135), then
  D3 AMENDED (above); the oracle and the comparison rerun on every kitting test-bed output (no simulation): every change
  a cell marked undetermined before (3241 rank cells, 6 gate ticks, the two chains at 135).
- Results: 0 disagreements with the oracles in all 76 recognition and 25 planning runs, and in the context-off sets
  rerun under the amendment (IRB s08, s09; round 1; the planning set under both strategies); undetermined left: 2 rank
  cells (scenario_s09_07 at 35, D7). Every re-declared property holds; PK3c, PK2b (the turn, TODO-146) and P10.10 fail
  as before. B12 verified (s16_03, s16_05 at 0, D4). C4 and C6 detected on step 5's six, C5 undetected there (no tie at
  a gate-relevant tick: a property of the set; D6).
- The comparison (off / on before / on after, the report's section 1): the admissions of the true task unchanged (206
  earlier, 48 equal, 42 later of 325; 3005 ticks earlier, 365 later); wrong admissions during modelled tasks 17 → 9 off,
  47 → 19 on (504 → 99 gate ticks); the pin-tick and lone-early admissions removed; planning completion better / equal
  / worse against off 7 / 13 / 2 → 5 / 16 / 1 (134 → 50 ticks gained); cases below min_separation 5 → 3 on, the two from
  a wrong admission (s16_05, s11_03) gone, no new case. Every case that moved is as expected by ruling (AM67 or AM68);
  no defect in the framework. The cost: s11_03's completion 35 → 113 (its gain rested on admitting a delivery never
  performed), s16_05 +5, s16_04 +1; no admission of the true task later than its first tick.
- Decided by ccode, confirmed by Hadi (5 October 2026): the report's place (analysis/kitting/tk5d/, with
  moved5d.py); the off column of the comparison is the off setting after the gate change (its earlier values in
  brackets); "wrong hypothesis held by the meta-planner" counted only before the robot's completion; C5 retargeted to
  the amended tie rule; the class "as expected by ruling" given where every lost tick is refused by AM67 or AM68.
Next: step 6 (dock_loading's part).
STEP 5E NAMED AND RULED (Hadi, 5 October 2026): context knowledge on kitting's rooms 02, 05, 06 and 07 (the rooms of
layouts 1 to 9 that hold a coffee machine or an A/C switch) with new scenarios, then the test off against on on all of
them. Steps 6 and 7 on hold. Ruled with it: new files only (no existing layout, setup, scenario, test or output changed
or deleted; no framework code, strength or ruled value changed); a behaviour the human model cannot express is left out
and named; about 2 setups and 4 to 6 scenarios per setup; the existing scenarios on these rooms that hold a measured
script join as they are; the settings off, on with no timeline fact, accord (the foreseeable task's raising fact over
the ticks where the human does it), through (a raising fact over a delivery); a window as a copy of the scenario with
its own timeline, placed from the scripts and never moved after a result; each script once with the idle robot through
the IRB and once with a working robot through the MPB, the idle robot first, the oracles' expectations committed before
the runs; declared properties and coverage rows not required; the report's five questions. ADDITIONS (Hadi, the same
day): layouts 08 and 09 join as two new layouts, copies with one coffee machine each, placed by a stated reason from
the room's arrangement, no A/C switch; on them 3 or more setups and 10 or more scenarios per setup, each scenario
differing from the others in a stated respect (the deliveries' number, order and tables; the place and number of the
foreseeable tasks; the kind, place and length of the unmodelled behaviour; the start and the first walk's direction
against the coffee machine; the robot's side).
STEP 5E, THE AUTHORING (ccode, 5 October 2026; analysis/kitting/tk5e/README.md): env_layout_19 (env_layout_08 with
coffee_machine_0 at (0, 450), the north wall's free middle) and env_layout_20 (env_layout_09 with it at (125, 450),
the free stretch of the north wall between kitting_table_0 and shelf_3); env_setup_17 to _30 (two per room on 02, 05,
06, 07, the first repeating the existing setup's shift; three per new room); 100 new scripts (10 per room on 02, 05,
06, 07; 30 per new room) and the 5 existing measured scripts (scenario_s02_01, s02_02, s04_01, s03_06, the one script of
s05_01 and s05_02), in 555 new scenario literals (scenarios_s17.py to _s30.py: each script's idle and working form, and
its window copies); run files in configs/kitting/tk5e/ (772 runs). Every behaviour the prompt names was expressible.
Decided by ccode, confirmed by Hadi (5 October 2026): the window rules (accord per instance over the task's ticks;
through with break_time over the first plain delivery, in every room; through_rw with room_warm for the deliveries-only
scripts of the rooms with an A/C switch); the idle robot's place per room; the literals written by ccode's generator,
which stays outside the repository (the literals are the source); the outputs under analysis/kitting/tk5e/{irb,mpb}/
{on,off}/.
STEP 5E, DONE (ccode, 5 October 2026; analysis/kitting/tk5e/REPORT.md, the step's one document; the comparison
comp5e.py). The runs: 384 recognition (idle robot) and 388 planning (working robot), the recognition runs first, through
repository copies in parallel; 0 disagreements with the oracles in all 772. Every planning expectation as committed;
33 recognition expectations changed by an instrument fix during the runs (the oracle's `recent` column on ticks with no
live hypothesis: the committed oracle reproduces the committed tables, the fixed one changes only that column there;
the new md5s in the README). Undetermined (D3): rank cells in 6 runs, one gate tick in each of 3.
- Recognition, on against off (no fact): deliveries earlier (four rooms 81 / 11 / 0, median −6; new rooms 102 / 24 /
  0, median −3); the coffee break outside break_time later (median +10, +13); inside it (accord) earlier (median −7,
  −3: less than step 5d's −14, off already early and AM68's refusals); wrong admissions during modelled tasks 7 / 5
  and 9 / 8 against off, all of kind (iii) or (i).
- The work-through cost: a delivery under break_time later than with no fact by a median 12 and 6 ticks (at most 61),
  later than off by 4 and 3; 2 never admitted (env_layout_20, the carry along the north wall at the machine); in
  env_layout_07 the raised coffee break admitted wrongly during a delivery toward the machine (17, 40 ticks).
- The A/C admitted more often than in step 5d (no fact 3 of 10, room_warm 8 of 10): env_layout_07's switch stands
  apart from every other target; where it follows the last delivery the foreseeable tasks share the whole prior.
- The gate: AM68 refuses the true task on 1 to 9 ticks (11 accord coffee breaks delayed 1 to 6 ticks; two deliveries
  interrupted), which step 5d did not meet; AM67 never refuses the true task.
- Planning: four rooms completion better / equal / worse 1 / 39 / 6 (16 ticks gained, 32 lost: longer holds against
  earlier admissions); new rooms 2 / 58 / 0. Cases below min_separation 58 on and 58 off (17 with the robot moving),
  mostly the same on both sides; added on: script 035 (env_layout_07, a near-tie of the coffee machine and shelf_5
  on one bearing resolved for the delivery, 30.0 cm, a limitation, docs/assumptions.md 6.4) and 038 (an admitted
  delivery cut by a coffee break inside it, 19.3 cm, a limitation); gone on: 024, 025, 043.
- No defect in the framework. Flag: tests/test_tl2_discovery.py's count of the registry (134) fails with the step's
  555 new scenarios (689); left unchanged (new files only), its one-line update for Hadi.
- Decided by ccode, confirmed by Hadi (5 October 2026): the authoring rules and the window rules (above); the
  classes of a wrong admission (main, unmodelled, exit, pin); the rule "the same case on both sides" for a case below
  min_separation with the same ticks and minimum on both sides; the oracle's `recent` fix; the per-run outputs kept
  untracked under analysis/kitting/tk5e/{irb,mpb}/{on,off}/ (Hadi, 5 October 2026: the convention of steps 5b and 5d).
Next: steps 6 and 7 on hold until Hadi rules.
STEPS 5D AND 5E: THE DECISIONS CONFIRMED; THE DISCOVERY TEST UPDATED (Hadi, 5 October 2026):
- The decisions ccode took provisionally in step 5d and in step 5e are confirmed, all of them (their lists above, now
  marked "confirmed by Hadi"; the same in analysis/kitting/tk5e/README.md and REPORT.md).
- tests/test_tl2_discovery.py: the registry's count updated to the present number, 689 scenarios (step 5e's 555
  added), and with it the same test's set of setups, env_setup_01 to _30 (step 5e's env_setup_17 to _30). The test
  suite: 365 passed.
Next: steps 6 and 7 on hold until Hadi rules.
A FINDING OF T-F PART 1 THAT BEARS ON T-K (5 October 2026; not ruled): with context knowledge on and no timeline fact in
force, an admission at tick 0 of a task the human is not doing (scenario_s05_01, s05_02; s16_01, s16_02); recorded
under "T-F part 1", THE CLOSE, FINDINGS. A second (5 October 2026; not ruled): with a timeline fact in force, a fact in
accord with the human's task speeds its admission, a fact not in accord delays it (design_records.md, "T-F part 1",
PART 1 OF THE LAST STEP; COMPARISON.md).
STEP 6 NAMED AND RULED (Hadi, 6 October 2026): dock_loading's stage 1 measured in full, before T-G's stage 2 opens (the
older ruling on the order reopened by Hadi on 5 October; reason: the instruments, the gate and the run conditions
changed since stage 1's tests). Debugging, not the evaluation: the set covers various situations roughly and need not be
complete; nothing is adjusted to a result; a case that does not occur is recorded as absent. The form is kitting's: step
5e's authoring (added scripts, scenarios that differ only in their timeline, expectations committed before the runs)
and T-F part 1's measurement (run files per scenario by serial, no setting in a name, the result table, one figure per
run, a comparison report generated from the table). No A/C switch in stage 1's rooms (stage 2's room). Four conditions:
human-unaware, intention-unaware, intention-aware with context knowledge off, with it on; assignment knowledge on;
`single_task` in every run. The old stage 1 outputs, expectation files and run files of both test-beds and the milestone
runs deleted as at T-F part 1's close (the tracked part reachable by a commit hash, the untracked outputs copied outside
the repository); the layouts, setups, scenarios and recorded findings stay; the old reports stay, marked stale. The
existing scenarios stay unchanged; their intention-aware runs with context knowledge off are the re-measurement of stage
1 under the present gate. A new setup on env_layout_02 with the pallets already in the bays. New scripts: one of each of
the survey's kinds (a) to (f) per room, more where they may show something about context knowledge; no expectation
derived by hand per scenario. Timelines: two or three scenarios per script that differ only in where break_time lies,
placed roughly, written before the runs and not moved; no window over the whole run; a scenario may hold two windows;
the scripts that depend on the robot get such variants too. The tag per task (THE TAG PER TASK, "T-F part 1") computed
by a reader that takes the raised task from the declared context knowledge, not from names; TODO-185 decided
provisionally by ccode and reported for Hadi's confirmation. The tag's measures report "admitted" in both readings, two
columns: the gate's answer per tick and the meta-planner's decision record. ADDITION (Hadi, the same day): ccode may add
a few new layouts (a new file with the next serial id; the three existing rooms unchanged; no A/C switch) and new setups
where more tests need them, each with one line stating why and what it makes testable.
STEP 6, DONE (ccode, 6 October 2026; analysis/dock_loading/tk6/: README.md the set and its rules, COMPARISON.md the
report generated from the table). Points 1 and 2 confirmed before the authoring: the recognizer's lines are identical
with an idle and a working robot on the 20 independent kind-3 scripts; a human-unaware robot moves as the robot alone
on the 12 scripts that depend on the robot (the reference check applied there). Added: env_layout_05 (env_layout_03 with
the coffee machine beside the office door: the coffee break and the office break on one shared walk), env_setup_10 and
_11 (kind 3 on rooms 02 and 05); 52 planning scenarios (the ten planning scripts on room 02; scripts a to g in four
rooms) and 164 copies with break_time; 568 runs (74 planning scripts in the four conditions, the copies with context
knowledge on, the 54 recognition scenarios intention-aware off and on), every run finished, 0 disagreements with the
oracle on 478, the 956 expectation files as committed, the reference check equal on 74. Instruments fixed for
dock_loading: logparse, admission.py, offon.py, the reference check, actual.py's end of run (end_run), tag.py new.
Decided by ccode, provisional, for Hadi's confirmation:
- TODO-185: a fact that lowers a task gives no tag (the tag reads the raised level of the declared context knowledge);
  the tasks at the suppressed level at a task's start are listed beside it (`lowered`).
- The tag is read from the world (the timeline's windows, the recency facts of the human's actual completions in the
  run's record), every top-of-stack stretch tagged, a task resumed after a cut tagged again at its resumption; the
  gate's reading over the whole stretch, the decision record's before the robot's terminal decision.
- The recognition set gets no copies with break_time (its scripts are the planning set's; point 1).
- The windows' rules V1 to V3, KT4's edges for script f, and the dependent scripts' windows from the plain chain.
Findings, none ruled: COMPARISON.md; the main ones in the chat report of the same day.
Next: Hadi's confirmation of the provisional decisions; step 7 (the close of T-K part 1).
STEP 6, FULL_REORDER (Hadi, 6 October 2026): the 74 planning scripts of step 6 are also run under `full_reorder`, in the
same four conditions. Reason: under `single_task` an admission can change only the hold, so the set cannot show whether
recognition changes the robot's choice or order of tasks. The ruling "single_task in every run" is extended, not
replaced: every comparison of conditions stays inside one strategy. The same scripts, setups and layouts; no window
copies and no recognition set; the same form (run files by serial, strategy a column of the one result table, one
figure per run, the oracle's expectations committed before the runs, the human-unaware reference run per strategy);
COMPARISON.md gains the three steps under `full_reorder` and a table of `full_reorder` against `single_task` per
condition. TODO-141 applies (no per-candidate hold under `full_reorder`).
STEP 6, FULL_REORDER, DONE (ccode, 6 October 2026; analysis/dock_loading/tk6/COMPARISON.md, its sections on the two
strategies): 296 runs (run_569 to run_864), every run finished, 0 disagreements with the oracle on 248, the 496
expectation files as committed, the reference check equal on 74. The single_task sections of COMPARISON.md are unchanged.
A measured premise: under single_task an admission can change the robot's order too (context knowledge off → on: 3
scripts that depend on the robot, scenario_s05_03, _04, _06); under full_reorder recognition changed the order in 1
script (intention-unaware → off, scenario_s09_03) and context knowledge in 3 (scenario_s07_04 to _06); in no script the
first task. Findings, none ruled: the comparison report.


## T-F part 1: the conditions human-unaware and intention-unaware

THE RULINGS (Hadi, 5 October 2026; recorded by ccode the same day). Made after ccode's read-only verification of the
same day (chat only, no file). The conceptual part (R2, R4, R5's premise, R6, R7) is in design_decisions.md, the entry
of this title. Records only, nothing built.
- R1. The name: "T-F part 1: the conditions human-unaware and intention-unaware", taken now, while T-K part 1's steps 6
  and 7 are on hold. The rest of T-F keeps its place after T-G. Reason: its only purpose is the evaluation's comparison,
  and TODO-144 names TODO-137 as a prerequisite.
- R3. Two run options, `human_aware` and `intention_aware`, both on by default, in the form of `assignment_knowledge`
  and `context_knowledge`: `--human_aware true|false`, `--intention_aware true|false`, the run file's keys of the same
  names, `human_aware=on|off intention_aware=on|off` in the `[run]` header. Reason: each names its condition directly
  (`human_aware` off is the human-unaware robot, `intention_aware` off the intention-unaware robot).
- R5, its form. An option that is off sets every option above it to off, whatever the default, the run file or the
  command states: `human_aware` off sets `intention_aware`, `assignment_knowledge`, `context_knowledge` and the
  separation stop to off; `intention_aware` off sets `assignment_knowledge` and `context_knowledge` to off. The run
  prints a message naming what it set to off, then runs; the `[run]` header prints the effective values; nothing stops
  at load. Reason: design_decisions.md, R5's premise.
- R8. `--cost_strategy plain` stays untouched and is not a column of the measurement. Reason: the verification showed
  the same behaviour as human-unaware in both runs, and plain differs by construction (re-decisions at triggers whose
  results it ignores); removing it is a cleanup outside this work, ruled with T-F (TODO-144's note).
- R9. The planning test-bed's oracle is extended to both conditions, as instrument work, in the build's second stage.
  Intention-unaware: the recognition columns as today; the gate refuses on every tick with `none(intention_off)`;
  decisions only at `no_current_task` and `projection_expired`; every projection a fallback projection. Human-unaware:
  no recognition lines; decisions only at `no_current_task`, no projection, hold 0; the robot's positions equal the
  reference run's where the human's script is independent of the robot. Not included: the declared properties per
  scenario (authored for the intention-aware run). Reason: the oracle checks the mechanism, not a scenario's design;
  without it these two columns would be the only unverified columns of the measurement.
- R10. The measurement, a separate step after the build, not planned now: the existing planning scenarios in four
  columns (human-unaware; intention-unaware; intention-aware with context knowledge off; intention-aware with it on).
  Measures from the log: completion, held ticks, the ticks below `min_separation` with F1's classes, the passes by a
  standing robot. Which sets: decided at that step.
State: nothing built. The build's plan: docs/handoffs/plan_T-F_part1.md, written by ccode, not approved. Next: Hadi's
rulings on the plan's open points, then the build's stage 1.
THE PLAN APPROVED, A TO G (Hadi, 5 October 2026; on ccode's flags 1 to 4 and Q1 to Q7 of the plan). A, B, C, E and
F's Q4 are conceptual: design_decisions.md, the same title, AMENDED. Here:
- D (Q1). The loader gives the robot no observed human; the scenario stays as written. Future work, Hadi's alternative
  (TODO-182): the robot keeps the observed human and each component skips its computation; its reason: an
  execution-time avoidance (C, TODO-181) could then still use the human.
- F, Q3. A run in which the recognizer does not run (human-unaware, intention-unaware) prints no `[coverage]` and
  `[scenario-coverage]` lines. Reason: they describe what recognition can explain. (ccode's check: only the IRB's
  instruments read them, and the IRB is not run in these conditions.)
- G (Q5, Q6). dock_loading's six scripts that depend on the robot get no oracle in the new conditions, measures only.
  The check that a human-unaware robot moves as the robot alone applies only where the robot's and the human's objects
  are separate; elsewhere a difference is a recorded finding, not a disagreement. The measurement of T-F part 1 (R10)
  runs on kitting only. Open for T-G's next stage, not ruled (TODO-183): may a domain forbid a run condition?
- The oracle's scope (R9 as amended by A): for the intention-unaware run it checks the decisions and the fallback
  projections only; "the recognition columns as today" is superseded.
- The plan: APPROVED with A to G (docs/handoffs/plan_T-F_part1.md, its status line and the sections A to G change).
Next: the build's stage 1, then a pause.
STAGE 1 BUILT (ccode, 5 October 2026; the plan's section 2, with A to F):
- The options: `--human_aware`, `--intention_aware` and the run file's keys (`mesa_sim/run_mesa.py`,
  `configs/experiment.yaml`, its stale commitment-warrant comment corrected); `SimModel` takes both with no default and
  applies the override (R5) in its one home, so the headless run, the viewer and the instruments get the same effective
  values; the line `[run_mesa] options <option>=off sets off: ...` after the timeline line, naming only the options
  whose stated or default value was on (none: no line); the `[run]` header's `human_aware=on|off intention_aware=on|off`
  before `assignment_knowledge`. Human-unaware: the robot is given no observed human (D). Intention-unaware: the
  recognizer is not called (`RobotAgent.step`, `observe_initial`), `_perceive` still runs (A). No `[coverage]` and
  `[scenario-coverage]` lines with `intention_aware` off (F).
- `shared/meta_planner.py`: `intention_aware: bool = True`; `GateOutcome.INTENTION_OFF` (`none(intention_off)`), asked
  first in `_clears_gate` (R6, A); admission asks `none(no_human)` before the gate (E); docstrings, `evaluate_triggers`'
  "Two real triggers" corrected. Unchanged: the recognizer, the gate's rule for the intention-aware run, the trigger
  rule, the fallback projection, the candidates and the cost.
- The other `SimModel` call sites pass `human_aware=True, intention_aware=True` (17 test files, list_scenarios.py, the
  IRB's and the MPB's instruments, the two frozen scripts as at AM51). Tests: tests/kitting/test_tf1_conditions.py (13:
  the override on six combinations, the header, the gate's two callers, `none(no_human)` before the gate, one run per
  condition on scenario_s10_02); the suite 378 passed (365 before).
- The identity check (B0 at 6cc69fb, no code change since db99f74, against the build; both in the session's scratchpad,
  each job in its own copy of the tree): the four maintained sets (48 logs), the kitting MPB under single_task,
  full_reorder and the prior-off appendix (16 scenarios each, every instrument output), the IRB's s08 and s09 (17),
  dock_loading's six milestone runs: 1082 outputs identical (logs after removing ` human_aware=on intention_aware=on`
  from `[run]`; every `.rec` and instrument output by bytes); 3 differ, the robot-alone reference logs of
  scenario_s10_06 (one per run variant), in 5 `[meta-proj]` lines each, `none(below_theta)` → `none(no_human)` (E).
- The conditions on scenario_s10_02, headless: human-unaware completes at 61 with no hold and the [sep] minimum 18.54
  cm (3 violations by the moving robot, 1 recede), as the robot alone; intention-unaware decides at
  `no_current_task` and 11 `projection_expired` ticks, holds 5 at 40 on a fallback, completes at 66 with the minimum
  52.20 cm (the intention-aware run: the hold 5 at 25 on the admitted plan, 66, 52.20 cm).
Next: stage 2 (the instruments), after Hadi's go.
STAGE 1 ACCEPTED; H TO J (Hadi, 5 October 2026). Stage 1 accepted; ccode's two decisions in it (`[IR-assignment]`
printed with the effective value; the two stale texts corrected) accepted; B's second corner case recorded
(design_decisions.md); stage 2's check on `single_task` only.
- H. The measurement of T-F part 1 (R10; the step after the build): the kitting scenarios in which the robot has
  assigned tasks: the planning test-bed's 16, step 5's 6 planning cases, step 5e's 106 planning scripts; all four
  conditions run anew into one new folder, under `single_task`. Reason: where the robot is idle the conditions give the
  same robot; one folder complete on its own does not depend on the folders of steps 5 to 5e.
- I. Naming: no file or folder of runs carries a parameter, an argument or a variable in its name. A run's settings are
  stated in its run file, in its `[run]` header and as columns of the instrument's result (`human_aware`,
  `intention_aware`, `assignment_knowledge`, `context_knowledge`, `strategy`). It applies to the new outputs of T-F
  part 1; the older folders are handled after the measurement, from a list Hadi rules on. Reason: a folder per setting
  multiplies files and archives; with the settings as columns, a later condition or strategy adds rows to the same table
  and renames nothing. In part 1 the column `strategy` holds `single_task` in every row.
- J. Notes for T-F part 2, recorded, not built: `full_reorder` becomes the default strategy of the runs of the actual
  evaluation (under it an early admission can change the next task and the whole remaining order, so recognition has
  more ways to change the result; a different choice rule from `single_task`, not a superset of it). Strategy is then a
  second dimension of the same result table; the human-unaware condition needs its own reference run per strategy;
  TODO-141 applies.
STAGE 2 BUILT (ccode, 5 October 2026; the plan's section 3 as amended by I; analysis/kitting/mpb/README.md, the T-F
part 1 section):
- `analysis/instruments/mpb/run_set.sh` (new): a set whose settings live in its run files; a run named by its run file
  (I); `table.py` (new) writes `results.csv` and `results.md`, one row per run, the effective settings (the `[run]`
  header) as columns, then completion, terminal, decisions, held ticks, near-encounters, F1's classes, the passes by a
  standing robot (passing, beside), the [sep] minimum, the oracle's check. `run.sh` stays the runner of the maintained
  outputs, its names unchanged.
- `conditions.py` (new): R5 as the instrument reads it (its own reading of the records), the header's settings, their
  agreement, the condition, objects separate (G: no movable object of the setup bound by both the robot's pool and the
  human's script; a shared shelf or table counts as separate), the script's dependence.
- The oracle and the comparison in the recorded scope: intention-unaware, no recognition columns, `none(intention_off)`
  on every tick, the decisions and the fallback projections; human-unaware, `none(no_human)` (asked before the gate, E;
  the gate is not asked, so the oracle and `mpblib.Gate` carry it as the decision's refusal), decisions at
  `no_current_task` only, no projection, hold 0, the robot's position against the reference run's on every tick within
  the horizon. No declared property in `run_set.sh` (`measures.py`: the measures alone). `actual.py` reads the
  meta-planner's belief where the recognizer does not run and `none(no_human)` as admission printed it.
- The check (the planning test-bed's 16 in each new condition and intention-aware, `single_task`;
  configs/kitting/tf1/check/run_001 to _048, named by serial, the scenario a column; outputs in
  analysis/kitting/tf1/check/, its results.md): 0 disagreements in all 48; every row's header settings agree with R5's
  reading; human-unaware equal to the reference run on every compared tick in all 16 (objects separate in all 16); the
  intention-aware rows through `run_set.sh` identical to `run.sh`'s runs and outputs (but for the run's name in
  separation.md's title); `run.sh`'s outputs (single_task, full_reorder, the prior-off appendix) identical to stage 1's
  (790 files). Tests: 385 passed.
- Read from the table, not analysed (the measurement is H's): human-unaware completes as the robot alone and comes
  closest to the human (s11_01 and s11_03 11.33 cm, s10_02 18.54 cm); intention-unaware never below min_separation in
  the s10 scripts, holds on fallbacks (s11_02 66 ticks, s11_03 62); intention-aware equal to intention-unaware on most
  s10 rows.
THE FIGURES, A STANDING RULE (Hadi, 5 October 2026; CLAUDE.md, "Methodology"): every run made through a test or
analysis instrument produces its per-tick figure (png, ignored by git). A run in which the recognizer runs: the belief,
the adequacy, the gate and the decisions per tick; with context knowledge on, beneath the belief, the timeline facts in
force per tick (they are what changes the prior). A human-unaware or intention-unaware run: the decisions, the kind of
projection (none or the fallback), the holds, the robot–human distance against min_separation; no belief. A set gets
its figures when it is next run; no old set is rerun only to make figures. Reason: Hadi reads a run from its figure.
Follow-up (Hadi, the same day): a decision panel on the belief's tick axis (the decision ticks with trigger and cause,
the projection each used, the robot's task over the ticks, the decided holds), the same panel in the two new
conditions' figures, the run's settings, the strategy included, in the title. Reason: the belief shows what the robot
believed; the panel shows what it did with it.
BUILT (ccode, 5 October 2026): `irb/plot.py` (the context panel under the belief from the run's `[IR-context]` lines:
the context facts in force, a timeline fact labelled `timeline` when the run's timeline line names it, an object state
`state`, and the recency facts `recent`; with no oracle table the actual alone; a caller's last panel and settings
line); `mpb/decision_panel.py` (new); `mpb/plot_ir.py` (every run in which the recognizer runs, the decision panel,
every faceted part kept: it had kept only the first, losing hypotheses 5 on); `mpb/plot.py` (the new conditions' figure:
the decision panel and the distance); `run.sh` and `run_set.sh` draw them. The IRB's figures of runs with context
knowledge off and of runs with an oracle table are byte-identical to before (checked by redrawing). ccode's choices:
the context panel shows all three sources the prior reads (timeline facts, object states, recency facts), the timeline
facts dark; the decision panel's rows are robot task (with the holds hatched), projection, decision; an admitted task is
named where it differs from the last named. Not covered by the rule as built: the regression sweeps of the four
maintained sets and the dock_loading milestone runs (run_mesa.py directly, logs only), and the robot-alone reference
run; a question for Hadi.
THE MEASUREMENT, RULINGS K TO O (Hadi, 5 October 2026; recorded by ccode the same day, as given). The measurement of
R10 and H: what recognition adds to planning, four conditions on the same scenarios (human-unaware, intention-unaware,
intention-aware with context knowledge off and on), all under `single_task`. Steps 4 to 5e of T-K part 1 compared
context knowledge off against on, both sides recognising intentions; this adds the missing side.
- K. Names. One folder per scenario, named by the scenario id; inside it the runs of the conditions by serial; no
  setting in any file or folder name. Supersedes naming every run by serial alone (I's form for the outputs). Reason:
  the scenario is what a run is about, not a setting the measurement varies; the runs of one scenario then lie side by
  side, and a reader finds a figure without opening the table.
- L. The scenarios: the planning test-bed's 16, step 5's 6 planning cases and step 5e's 106 planning scenarios in the
  form with no timeline fact, 128 in all four conditions (512 runs); step 5e's 176 copies with timeline facts,
  intention-aware with context knowledge on only; 688 runs in total. Reason: the four conditions must run identical
  scenarios; a timeline acts only through context knowledge, so the 176 copies add rows in that one condition only;
  they are the runs in which the context panel shows timeline facts, and their old folders are to be deleted.
- M. Declared properties are not checked in the measurement; the oracle check runs on every row where it applies.
  Reason: they were written for one condition; the planning test-bed keeps checking them in its own maintained outputs.
- N. The figure, completing what the last session built: one figure file per run, every panel on one shared tick axis:
  the belief; the tail probability S; the adequacy finding; the context panel (context knowledge on); the observation
  warrant and the gate's answer per tick with its refusal reason; the decision panel; the robot-to-human distance,
  readable near min_separation. A human-unaware or intention-unaware run keeps the panels that apply. Reason: the reader
  lines up belief, gate, decision and distance on one tick by eye; two files with different axes do not allow it; the
  ticks below min_separation are the measure, and a scale of 0 to 1600 cm hides them.
- O. Figures for the sets the measurement does not run: run them once more so that each has its figures; every other
  output must come out identical to the existing one, and any that does not is reported. Not the robot-alone reference
  run. Reason: the standing rule (every test and analysis run has its per-tick figure) should hold for what exists now.
  NARROWED (Hadi, the same day): of the recognition runs of steps 4 to 5e only those of steps 4 to 5b (irb/tk1, tk2,
  tk5b), which stay as sets until T-F part 2; step 5e's recognition runs are not rerun (the measurement runs the same
  human scripts with a working robot; Hadi intends to delete them). CORRECTED (Hadi, the same day): dock_loading's two
  test-beds and its milestone runs are not rerun; they are stale since the gate rulings, until dock_loading's own step,
  which brings their figures.
- E (the step's part E; widened by Hadi the same day): a table, not executed, of every folder under analysis/ and the run
  files under configs/: what it is, whether a record cites it (by its present path or its path before the sort of 1
  October), and a judgement: maintained (stays, and takes K's names on its next run), replaced (runs deleted, report
  kept), old record (data deleted, reports and scripts kept), or keep. Hadi's intentions: step 5e, steps 5 and 5b's
  planning runs, stage 2's check and their run files are replaced; the recognition runs' run files deleted, each
  step's report kept, every record citing a deleted path given one line; the old frozen analyses under analysis/kitting
  (td_stage1, td_stage1b, l_build, irb2b_exposed_interval, ablation_task_committed, f47_fixtures,
  t1_conflict_measurement, todo90_b2a_window, tc2c_scripts, tb1d_designations, tb2c_per_entry_holds, big_picture)
  deleted completely, as on 4 October (one note in analysis/README.md naming the last commit that holds them; the
  records' citations stay), unless something in one is still used. Reason: analysis/ holds about 18,000 files and
  2.5 GB (step 5e alone 12,001 and 1.7 GB), which Hadi cannot read; the frozen analyses were made on a recognizer that
  no longer exists, their conclusions are in the records, and git history and the outside copy of 2 October hold them.
  Nothing is deleted or untracked before Hadi rules on the table.
BUILT AND RUN (ccode, 5 October 2026):
- A (f849db9, edae0e4): `analysis/instruments/irb/plot.py` `draw`, the one figure's builder, the panels from the top:
  the belief over H (one panel per four hypotheses, all in the file), the context panel directly under the belief (the
  earlier figures ruling's place), S (one panel per four), the finding, the warrant per hypothesis and the gate's answer
  per tick (one row per answer: clears or the refusal's reason), the decision panel (with the oracle's expected
  decisions), the distance (the `[sep]` line's continuous minimum on 0 to 4 × min_separation, larger values at the top
  edge, the ticks below min_separation shaded by F1's class, the closest approach written); `mpb/plot.py` draws it for
  every planning run (figure_ir.png no longer drawn; `plot_ir.py` keeps the rows helper); `mpb/figure_of_log.py` draws
  it for a run made by run_mesa.py directly, from its log (the four maintained sets' sweep.sh call it). K:
  `run_set.sh` writes `<out_root>/<scenario>/<run>/`, the log and `.rec` inside; `table.py` reads that layout.
- B (3d7a26a, efb16fe): 688 run files, `configs/kitting/tf1/measurement/<scenario>/run_NNN.yaml` (written by
  `analysis/kitting/tf1/make_runs.py`; the four conditions of a scenario consecutive); outputs in
  `analysis/kitting/tf1/measurement/`, `results.csv` and `results.md`. The oracle compared on all 688 rows, 0
  disagreements; every row's header settings agree with R5's reading; the 128 human-unaware rows equal the robot-alone
  reference run on every compared tick (objects separate in all 128).
- D (efb16fe): `analysis/kitting/tf1/REPORT.md` (tables per set and condition, the pair counts, findings 1 to 7, none
  ruled; `tables.py`). ccode's correction: the result table's `completion` is the tick after the robot's last release
  even when its pool did not complete; the report counts completion only with a terminal decision (five runs do not
  complete within the cap: scenario_s02_02 intention-unaware and intention-aware, and its copies s17_08, s17_10).
- O (edae0e4, 26ca369, and the copy-in of this record's commit): rerun with their figures, every other output compared
  with the existing one: the four maintained sets (48 runs; every `.rec` byte-identical, every log identical but the
  `[run]` line's ` human_aware=on intention_aware=on`, which the logs on disk predated; new md5 sections in their
  READMEs); kitting's IRB s08/s09 (17), irb/tk1 (31), irb/tk2 (57 and tk2/off 2), irb/tk5b (17): 1116 files identical,
  124 logs identical but those two fields, none differing; kitting's MPB set under single_task, full_reorder and the
  prior-off appendix: 659 identical, 48 logs but the two fields, 2 differing, the robot-alone reference logs of
  scenario_s10_06 in their 5 `[meta-proj]` lines (`none(below_theta)` → `none(no_human)`: stage 1's named exception
  E). No tracked file changed. Not rerun (O as narrowed and corrected): step 5e's recognition runs, dock_loading's IRB,
  MPB and milestone runs (the milestone sweep added in edae0e4 withdrawn, 8da7b2a). The old `figure_N.png` (88, the
  IRB's faceted parts) and `figure_ir*.png` (32) stay beside the new `figure.png` until Hadi's ruling on part E.
- ccode's flags on the rulings (the step's report): L runs step 5's three timeline copies (scenario_s16_02, _04, _06)
  in all four conditions, against L's own reason (they equal their bases in HU, IU and IA-off); N's list puts the
  context panel after the finding, the figure keeps it under the belief (the earlier figures ruling's place); deleting
  the recognition runs' run files would leave their outputs with no way to rerun them.
State: the measurement run and reported; part E's table with Hadi. Next: Hadi's ruling on part E.
THE CLOSE (Hadi, 5 October 2026; recorded by ccode the same day). The statistics report (analysis/kitting/tf1/
COMPARISON.md, comparison.html, comparison.py) is accepted; part E's table and the untrack step are accepted as ccode
proposed them (reason: analysis/ held 18,071 files and 2.5 GB; the deleted runs are replaced by the measurement or were
made on a recognizer that no longer exists; their conclusions are in the records, and git history, the copy of 2
October and ccode's backup hold them). T-F part 1 is CLOSED. T-F part 2 is parked. Hadi's next chat is T-G's next stage
with T-K part 1's steps on dock_loading.
- What T-F part 1 built: the run options `human_aware` and `intention_aware` (R3), the override (R5) in `SimModel`, the
  refusals `none(intention_off)` and `none(no_human)` (R6, R7, E); the planning test-bed's runner of a set whose settings
  live in its run files (`run_set.sh`), its result table with the settings as columns (`table.py`), the oracle in both
  new conditions (R9); one figure per run on one tick axis (N). What it measured: 128 kitting scenarios in the four
  conditions and 176 timeline copies, 688 runs, `single_task`, 0 disagreements with the oracle (REPORT.md; for a reader
  outside the repository, COMPARISON.md).
- PART E EXECUTED (a63e11b, 02c8e5c): analysis/ from 30,771 files and 3.9 GB (the measurement's 688 runs included) to
  16,488 files and 2.0 GB; configs/ from 1,757 to 912 files; tracked files under analysis/ from 1,056 to 95. Deleted:
  the 12 frozen kitting folders, the runs and run files of T-K part 1's steps 5, 5b (planning) and 5e and of stage 2's
  check (their READMEs and reports kept), tf1/figure_examples, the 120 superseded figure files; untracked: 806 per-run
  detail files .gitignore names (kept on disk). The last commit holding the deleted tracked files is 362af19; everything
  deleted is also in /home/hadi/teamrob_tf1_handoff/deleted_2026-10-05_part_E.tgz. Nothing deleted was in use (no import
  or read by code, a test or a maintained set); after it the tests pass (385) and the IRB, the MPB's run.sh and
  run_set.sh and a maintained sweep run, their outputs identical to those on disk. analysis/README.md holds the note;
  each record citing a deleted path has one line.
- FINDINGS (none ruled):
  - A stand that does not end (X1's case with no alternative task, measured). scenario_s02_02 (env_layout_02; T-C2c's
    scenario A, whose script ends with the delivery of item_5 at kitting_table_0 and no exit walk, docs/assumptions.md
    1.1): from tick 250 the human stands at kitting_table_0, the robot's remaining target (item_1). The three conditions
    that observe the human do not finish within the cap of 704 ticks: the robot holds on fallback projections of the
    stand, each as long as the stand observed so far (P4); intention-unaware 30 ticks at 278, 64 at 310, 128 at 374, 256
    at 502 (478 held ticks); intention-aware, context knowledge off and on, 14 at 270, 48 at 294, 96 at 342, 192 at 438,
    384 at 630 (734). Human-unaware completes at 422, as the robot alone. The same in its timeline copies scenario_s17_08
    and s17_10 (intention-aware, context knowledge on). Open question, not ruled: what the robot does when a stand at its
    target does not end (TODO-184; X1 set aside a give-up threshold and pointed to communication, X5).
  - An admission at tick 0 with context knowledge on. In scenario_s05_01 and s05_02 (env_layout_07) the human's first
    task is coffee_break; at tick 0 no timeline fact holds, coffee_break has the ordinary strength, and the belief over H
    puts deliver_item(item_5) at about 0.97 (the oracle's value as well); the gate clears on it from tick 0 to 23, the
    robot admits it at tick 0 (hold 2) and violates at ticks 27 to 29 (minimum 30.0 cm) before its next decision at 40.
    With context knowledge off the same ticks rest on fallback decisions and no tick lies below min_separation. The same
    form in scenario_s16_01 (admission at 0, violations at 49 and 50) and s16_02 (admission at 38, violations 48 and 49).
    It bears on T-K (the strengths as ruled, AM65; the gate, AM66).
  - Steps 2 and 3 show no difference this set can distinguish from zero (COMPARISON.md): recognition over the fallback
    alone, completion 15 earlier, 101 equal, 11 later of 127 scenarios, mean -0.84 ticks, violation ticks 14 → 17;
    context knowledge, completion 8 earlier, 112 equal, 7 later, mean -0.28, violation ticks 17 → 23; for both the 95%
    interval of the mean change, resampling the 10 rooms, includes zero. Step 1 (planning against the observed human):
    violation ticks 137 → 14, completion later in 36 of 127 scenarios, mean +5.83 ticks.
    AMENDED (5 October 2026, with the last step's part 1): step 3 is context knowledge with no timeline fact in force
    (125 of 128 scenarios), so it measures the prior alone; COMPARISON.md names it step 3a. Context knowledge with a
    fact in force is step 3b (PART 1 OF THE LAST STEP, below).
- TODOs: TODO-137 closed (built and measured); TODO-144 part 1's result recorded, part 2 parked; TODO-183 forwarded to
  T-G's next stage (docs/handoffs/T-G_forward_inputs.md); TODO-184 recorded (the stand that does not end); TODO-181 and
  TODO-182 unchanged.
- The handoff: docs/handoffs/handoff_T-F_part1.md (the options, the instruments, the result, the findings, the parked
  notes for T-F part 2).
PART 1 OF THE LAST STEP: CONTEXT KNOWLEDGE WITH A FACT IN FORCE (Hadi, 5 October 2026; recorded by ccode the same day).
Ruling: step 3 of COMPARISON.md compares context knowledge off and on almost only where no timeline fact is in force
(125 of 128 scenarios), so it measures the prior alone; pair each copy with a timeline (context knowledge on) with its
base's run with context knowledge off, by class (the human's behaviour in accord with the fact in force, or not);
complete the set by new copies where a class is missing (both classes for every script that allows them; reason: a set
with facts only in accord would show a benefit by construction), one rule written down before the runs; two
recognition measures beside the others (how many ticks after its start each of the human's tasks is admitted; how many
ticks a task other than the one the human performs is admitted), because context knowledge acts on recognition first.
BUILT AND RUN (05b4dd3, 673d1b6): the rule in analysis/kitting/tf1/REPORT.md ("Part 1"), committed before the runs;
`make_copies.py` (the classes, the windows, the new copies); 32 new copies (7 in accord, 25 not in accord, on 25 bases;
new scenario literals only, tests/test_tl2_discovery.py's count 689 → 721), run_689 to run_720, 0 disagreements with the
oracle; the classes: 73 copies in accord, 135 not in accord, step 5's 3 whole-run copies apart. Results: COMPARISON.md,
"Step 3b: context knowledge with a timeline fact in force". FINDING (not ruled): with the fact in accord, of 66 stretches of the human's
tasks starting while the fact holds, 52 are admitted earlier than with context knowledge off and 2 later; with the fact
not in accord, of 119 such stretches, 31 earlier and 70 later. Wrong-admission ticks 633 → 613 (in accord) and 999 →
1175 (not in accord). Completion and violations change little: completion 5 earlier, 62 equal, 5 later of 72 (in
accord) and 5 / 119 / 10 of 134 (not in accord); violation ticks 10 → 5 and 18 → 24.
THE TAG PER TASK (Hadi, 5 October 2026; recorded by ccode the same day; records only, nothing built). For the next
analyses (T-K part 1's step on dock_loading, T-F part 2). Each task the human performs gets one tag in the analysis, by
the facts in force when the task starts:
- in accord: a fact holds, and the human performs the task that the fact makes more likely;
- not in accord: a fact holds, and the human performs another task;
- no fact: no fact holds.
Reported per tag: how many ticks until the task is admitted, how many ticks a wrong task is admitted, and the violation
ticks that fall inside the task. Completion stays per run.
Reason: a run has several tasks, and a fact holds for only some of them, so a class per scenario copy mixes them; step
3b already had to split inside each class. A tag per task works for any scenario, with no special copy.
Points that belong to the ruling:
- The tag is a label of the analysis. It compares what the human does with what the fact suggests; the robot never has
  it. It is a term of the world, not of the robot's mind.
- "in accord" and "not in accord" are new terms (glossary §7).
- OPEN, not ruled, for Hadi's next chat (TODO-185): the definition covers facts that raise a task. For a fact that lowers
  a task (the human just had a break), what "in accord" means is not decided.
State: T-F part 1 CLOSED; T-F part 2 parked. Next: T-G's next stage with T-K part 1's steps on dock_loading.
THE MEASUREMENT EXTENDED BY FULL_REORDER (Hadi, 6 October 2026; debugging, not T-F part 2's evaluation): the 128 kitting
scenarios of the measurement run under `full_reorder` in the same four conditions. Reason: as on dock_loading, under
`single_task` an admission can change only the hold. The same scenarios, no window copies; the single_task runs not
rerun unless a check requires it; the same form (run files by serial, strategy a column of the one result table, one
figure per run, the oracle's expectations committed before the runs, the human-unaware reference run per strategy);
COMPARISON.md gains the three steps under `full_reorder` and a table of `full_reorder` against `single_task` per
condition, its single_task numbers unchanged. TODO-141 applies.
THE MEASUREMENT EXTENDED BY FULL_REORDER, DONE (ccode, 6 October 2026; analysis/kitting/tf1/COMPARISON.md, "The
measurement under full_reorder"): 512 runs (run_721 to run_1232), 0 disagreements with the oracle, the 1024 expectation
files as committed (each oracle table byte-identical to its single_task counterpart's), the 720 single_task rows of the
result table byte-identical, every earlier line of COMPARISON.md unchanged. Not finished: scenario_s02_02 in the three
conditions that observe the human, as under single_task (TODO-184). A measured premise: under single_task recognition
changed the robot's order in 3 scenarios (intention-unaware → context knowledge off) and context knowledge in 1;
under full_reorder in 1 and 3. Findings, none ruled: the report.

## T-viz, the web-ui

WHAT IT IS (Hadi and the design chat, 4 to 6 October 2026; recorded by ccode, 6 October 2026, T-viz 0.1). A web user
interface for the framework, the web-ui: its own page in the browser and a small Python server, without Solara. The
source is `docs/handoffs/handoff_T-viz.md` (written in the design chat, placed in the repo by Hadi, 069282b), which every
T-viz session reads first; it holds the course of the discussion, Hadi's taste and references (section 10, the images
in `docs/handoffs/tviz_refs/`), the proposed architecture and messages, and the open questions. This heading records
the status of each item and the steps done; it does not repeat the handoff.

THE STATUS WORDS. T-viz records do not use "ruling" or "ruled" (Hadi, so that its choices stay changeable in later
design stages): open (not chosen; every item until Hadi says otherwise), preferred (Hadi said so; the default for now),
preferred, replaceable (a default defined from the start as exchangeable for a named later alternative), proposed by
cchat (a recommendation of the design chat, treated as open), verified and not verified (facts). Proposals of ccode are
marked "proposed by ccode" and are open. "sim-run" (one simulation, from a built model at step 0 to its end) is a word
of the T-viz records only; the glossary's run, run file and run options are unchanged.

PREFERRED BY HADI (handoff, 6.1 to 6.3, 7.2, 7.5, 12.4):
- The framework gets a web-ui, its own page with a small Python server, without Solara; it is domain-independent (the
  same for kitting and dock_loading); the scene is drawn by a JavaScript drawer, not Plotly, a tick moving existing
  shapes.
- Run options are fixed for a sim-run: editing happens before the model is built, nothing is edited while a sim-run is
  in progress (within stages 0 to 2). The time of a sim-run is its number of ticks.
- The technologies are chosen for the full target, not for the first increment; only stage 1's visual design may be a
  simple first round; the backend is not provisional. The work is incremental.
- The reading of the run configuration and the building of the `SimModel` move into a module of their own (0.2).
- The visual design is ccode's, within Hadi's described taste (handoff, section 10: sketch J the reference style, the
  background and static objects toward the line drawing of sketch A; a tilted view with height, "minimal 3d"; agents a
  bit illustrative; active objects given more presence); a per-domain visualisation configuration read only by the
  web-ui, its form and place ccode's.
- What the env-pane shows before the first step: alternative B, every change of a choice or a toggle builds the model
  and the env-pane shows its step 0; the choices lock after the first step, reset unlocks them. Its condition, a build
  of about a second or less, is measured (fact 5 below): met.
- Stage 1 split into 1a, 1b, 1c; the toggles cover all run options; sim-runs side by side belong to stage 2.
- Preferred, replaceable: an agent's path is a straight line now, another path method later (see fact 3 below).
- The solara-ui stays in the repo as archived (not updated with core and model changes, not guaranteed to run, not
  deleted); the archived status begins when Hadi accepts stage 1a; until then it is kept working.
  CHANGED (Hadi, 6 October 2026, preferred; design_records.md, "T-viz, the web-ui", 1a, STAGE 1a CLOSED): the solara-ui is not archived; it stays as an alternative start, kept running with a light check.
Everything else in the handoff is open or proposed by cchat (collected in its section 15).

THE STAGES: `docs/roadmap.md`, "The plan from T-A", the T-viz bullet (stages 0 to 3 and the unassigned items); the
open questions of stages 2 and 3 and the unassigned items are TODO-186 to TODO-189. Hadi did not explicitly confirm the
consolidated list of the handoff's 12.1; he raised no objection to it.

RELATIONS (ccode's reading of the records, 6 October 2026; how the records join T-viz and T-V is open, for Hadi):
- T-E (the demonstration's viewer) is not an open task: superseded by T-V track 1 on 30 September 2026 (roadmap.md,
  "T-E — Demonstration", its SUPERSEDED line; glossary §8, **T-E**; `docs/handoffs/handoff_T-D_onward.md`, the header
  that marks its order as history). Its list (belief, admitted projection, decision, hold, refusal, the script's events)
  lives on in T-V track 1.
- T-V track 1, "the viewer for pre-loaded scripts" (demonstration only, nothing enters the mind), has the content that
  T-viz's panels 4b and 4c (stages 1b and 1c) show, on the program T-viz builds. T-V track 2 (Phase 7: live events
  through `inject`, the export as a script, the replay rule) has its page's side in T-viz's stage 3 (proposed by cchat);
  the mechanism stays T-V's. Proposed by ccode: T-V keeps what is shown and the live-event mechanism, T-viz is the
  program; T-V track 1 is carried out on the web-ui as T-viz's stage 1, so that the two never hold two copies of one
  item. T-V's place in the order (after T-F) and T-viz's (taken now) differ; the order block states only that T-viz is
  taken now.
- T-L's run-file panel (`mesa_sim/viz/run_file_panel.py`) is the solara-ui's built form of T-L ruling 7 ("The viewer
  reads and edits the same file"): it shows the run file, edits the three override kinds and writes them into the run
  file. The web-ui has no run-file panel; whether it offers the override kinds in stage 1 or 2 is open (TODO-186);
  saving the page's choice as a run file is unassigned (TODO-189). `mesa_sim/overrides.py` holds the reusable logic.
- TODO-110 (selection by composition or scenario coverage, not built): "the viewer" it names would be the web-ui's
  selection panel; it is among stage 2's open questions (TODO-186). `mesa_sim/list_scenarios.py` is its one reader
  over the registry today; the web-ui's catalogue of what the registry holds (handoff, 7.3, proposed by cchat) would be
  a second reader of the same registry.

HADI'S ANSWERS (6 October 2026, to the 0.1 report's questions 2 and 3; preferred; recorded by ccode the same day). They
settle the open point of RELATIONS above.
- T-viz and T-V. T-viz is the name for all web-ui work. T-V track 1 (the viewer task: what is shown) is carried out as
  T-viz stage 1 (1a, 1b, 1c). T-V track 2 (Phase 7, live events on the human's script) is T-viz stage 3: stage 3 means
  T-V, the live-event mechanism with the page's side. The mapping: docs/rename_table.md, "Task names". Dated entries
  that say T-V, T-E or "the viewer" stay as written.
- V1 and FW. T-viz stages 0 and 1 are in V1. Stages 2 and 3 are after V1, [FW], the default until Hadi draws the V1
  border inside the web-ui; with stage 3 the live-event task (T-V track 2) is [FW]. TODO-173 (slots in containers) is
  [FW]; TODO-186, TODO-187 and TODO-188 are tagged [FW]. Stage 0's choice of technology still considers stages 2 and 3
  (handoff, 6.1, item 6), unchanged.
- The place in the order (proposed by ccode; the answers move T-V's content, not its place): T-viz stage 0 runs now;
  T-viz stage 1 stands in T-V's place in the present order, after T-F and before track 3b; stages 2 and 3 leave the V1
  queue. Hadi may place stage 1 elsewhere.
- What the answers contradict, recorded and left for Hadi:
  - A1's tag rule (T-G records, "Tags"; glossary, **FW**): [FW] is for "conceptual, higher-level directions only"; the
    web-ui's stages 2 and 3 and TODO-173 are build work, tagged [FW] by this answer.
  - design_decisions.md, "T-G: the second domain's rulings", A3's paragraph: the human's choice among applicable tasks
    is one isolated point of its executor "so that a live user (T-V track 2, in V1) ... can supply the choice. This
    isolation is a V1 requirement." The live user is now FW; whether the isolation stays a V1 requirement (it is built,
    A3, 048a36e) is Hadi's. Also the roadmap's T-V bullet, its T-G line.
  - Track 3b and track 4 placed "after T-V" (roadmap.md, T-D's CLOSED EXCEPT ITS TAIL line and its amendment; glossary,
    **T-D tail**; TODO-140's and TODO-145's PLACEMENT REVISED lines): with T-V split, "after T-V" reads "after T-viz
    stage 1" under ccode's proposal; dated, left as written.
  - design_decisions.md, Phase 7's entry, SCHEDULED: "Phase 7 is T-V, track 2", still true; that it is now FW is
    recorded in the roadmap's Phase 7 section, not in the entry.
HADI'S ANSWER ON THE CONTRADICTIONS AND THE PLACE (6 October 2026, preferred for now): "Put everything in FW, I decide
later." The [FW] tags on T-viz stages 2 and 3, TODO-173 and TODO-186 to TODO-188 stay. No ruling is amended by this:
A1's tag rule, the glossary's **FW** entry and A3's text on the live user as a V1 requirement stay as written. Open,
each with "Hadi decides later", collected in TODO-190 for when Hadi draws the V1 border inside the web-ui:
- the [FW] tags against A1's tag rule (conceptual, higher-level directions only);
- A3's isolation of the human's choice as a V1 requirement, its live user now FW;
- "after T-V" in the placements of track 3b and track 4;
- the place of T-viz stage 1 in the order (ccode's proposal: in T-V's place, after T-F, before track 3b).

0.1, RECORDING, DONE (ccode, 6 October 2026; no code changed). THE VERIFICATIONS of the handoff's 16.2, read at
069282b (line numbers at that commit):
1. T-E: superseded by T-V track 1 (roadmap.md 600 to 605; glossary.md 1373 to 1374; handoff_T-D_onward.md 10 to 12),
   not an open task. CLAUDE.md 292 to 293 and 892 say the same.
2. The dependencies between run options: `SimModel.__init__` applies them (mesa_sim/sim_model.py 136 to 149):
   `intention_aware = intention_aware and human_aware`, the two knowledge options `and intention_aware`, the separation
   stop `and human_aware`; the options set off are logged as `[run_mesa] options <cause>=off sets off: ...` (265 to 266).
   The model exposes the effective values as attributes: `human_aware`, `intention_aware`, `assignment_knowledge`,
   `context_knowledge`, `separation_stop`, `strategy`, `gate_strategy`, `cost_strategy`, `test_level` (136 to 170). The
   stated values are not kept. No refusal at load, as Hadi said.
3. `planned_path`: no module writes it, for the human or the robot. Its only reader is the drawer, behind a `hasattr`
   guard (mesa_sim/viz/space_drawer.py 223 to 228); `git log -S planned_path -- mesa_sim` finds only the drawer's own
   commit (6881369). The solara-ui draws no planned path today. What the model holds that a path could be copied from
   (the executor's current walk target, the meta-planner's projected segments, the human executor's current `MoveTo`)
   is for 0.4.
4. Heading: no agent holds a heading or facing. The robot's mind keeps `_previous_human_direction`, the unit direction
   of the observed human's last step (mesa_sim/sim_agents.py 420, 680 to 690), a perception fact of the robot, not the
   human's facing.
5. The time to build a `SimModel` (`SimModel(**resolve_model_params(...))`, the layout and setup read, the agents
   spawned, the load-time replay `check_script` included; PYTHONHASHSEED=0, measured over every registered scenario on
   its first reference layout, one build each): kitting 721 scenarios, 0.002 to 0.068 s, median 0.003 s; dock_loading
   298 scenarios, 0.001 to 0.005 s, median 0.003 s. The one-time import of `mesa_sim/run_mesa.py` takes about 1.7 s.
   Alternative B's condition holds by two orders of magnitude.
6. The roadmap's Phase 2.2 line "Live agent positions, task progress, belief state display" (roadmap.md 49) does not
   match the code: no file under mesa_sim/viz/ or mesa_sim/mesa_fork/visualization/ shows task progress or a belief
   (TODO-180's check of 4 October 2026 found the same for `confidence` and `distribution`). Left for the records
   cleaning.
7. A headless run is stopped by an import fault in the Solara modules: `import solara` and the viz imports are at module
   level (mesa_sim/run_mesa.py 420 to 424), before `run_headless()` is called (473). Checked: with `solara` made
   unimportable (`sys.modules['solara'] = None`), `mesa_sim/run_mesa.py --steps 1` stops with `ModuleNotFoundError` at
   line 420.
8. The glossary has no entry for "tick", "step", "author" or "viewer" (nor for "run options"; the words are used
   throughout). It does not distinguish "tick" and "step"; the code uses both (Mesa's `step()`, one tick per step).
9. No automatic pause at a cognitive event exists: the fork's `ModelController` (mesa_sim/mesa_fork/visualization/
   solara_viz.py 255 to 320) has step, play, pause and reset only; nothing in mesa_sim/viz/ or run_mesa.py pauses on an
   event. The two triggers that earlier design named, `theta_crossed` and `task_committed`, no longer exist (D2, D3).
10. Shared changing state outside the model object (reading only; the decisive two-model check belongs to stage 2):
    no global random source is used (no `random.*` or `np.random.*` call in shared/, world/, mesa_sim/ or domains/; the
    fork draws a seed from Python's global `random` when none is given, mesa_sim/mesa_fork/model.py 55 to 60, and no
    framework code reads `model.random`); domain registration returns a new `Tree` per build (domains/kitting/registry.py
    19 to 24); no mutation of the registry's scenario objects was found (overrides use `dataclasses.replace`,
    mesa_sim/overrides.py 220 to 223); one module-level cache, `_mesa_config_cache` (mesa_sim/action_decomposer.py 314 to
    323), holds the constant `mesa_configs.yaml`. Shared: the logging set-up. The run log and the `.rec` stream are one
    file pair per process, opened at import of mesa_sim/run_mesa.py (69 to 89); two models in one process write into the
    same pair.
11. The vendored Mesa fork is 3.0.0a1 (`mesa_sim/mesa_fork/__init__.py` 27). Python 3.10.12; solara 1.57.3, starlette
    0.48.0, reacton 1.9.1, plotly 5.23.0 (requirements.txt 13 to 16).
12. What a sim-run writes, and from where:
    - `logs/run_<timestamp>.log` (the root logger, also echoed to the terminal) and `logs/run_<timestamp>.rec` (the
      logger `rec`), both relative to the working directory and opened at import of mesa_sim/run_mesa.py (69 to 89),
      once per process. The layout and setup paths in the registry are also relative to the repository root.
    - Written by the model and its agents: the `[run_mesa] timeline` and `[run_mesa] options` lines
      (mesa_sim/sim_model.py 263 to 266), the `[run]` header (mesa_sim/sim_agents.py 393), `[coverage]`,
      `[scenario-coverage]`, `[IR...]`, `[meta...]`, `[hold]`, `[stop]`, `[human]` and the `[rec]` stream
      (sim_agents.py 71).
    - Written by `run_headless()` only (mesa_sim/run_mesa.py 343 to 411): the start line `[run_mesa] Starting headless
      run — ...`, the `[run_mesa] override` lines, the per-step agent lines, `[sep]`, the run's end (`end_run`: the
      still-open entries of a robot-dependent script, a `[human]` line and a `[rec] end` line) and `[run_mesa] Headless
      run complete.`. The solara-ui writes none of these.
    - No run file is written by a sim-run. Only the solara-ui's run-file panel writes one (`write_overrides`,
      mesa_sim/overrides.py 234 to 256). No figure is written by a sim-run (`analysis/instruments/mpb/figure_of_log.py`
      draws it from the log).
THE DIFFERENCES between the handoff and the repo (the repo wins; a dated correction note stands at the end of the
handoff):
- Reference images: the handoff places them in `docs/handoffs/tviz_refs/`; commit 069282b held them in
  `docs/handoffs/`, and Hadi's 4e71335 moved them to `tviz_refs/` during this step, so the place now agrees. The
  handoff (10.3) says the folder should stay out of version control if the repository is public; the repository is
  public, and both commits, with the thirteen third-party images, are pushed.
  RESOLVED (Hadi, 6 October 2026): `docs/handoffs/tviz_refs/` is git-ignored and untracked from ef0726d on, its 14
  files (the 13 images and `sketch_A_and_J.svg`) kept on disk; no copy of 069282b's image blobs is tracked at another
  path. They remain in the public history of 069282b and 4e71335; history is not rewritten.
- 4.4 lists T-E as a task and names T-V for track 2 only; T-E is superseded and T-V track 1 is the existing record of
  the viewer as a task (fact 1).
- 5.4, 8.4 and 12.1: "the model already holds a path per agent (`agent.planned_path`) ... Today that path is a straight
  line": no module writes `planned_path`; the solara-ui draws none (fact 3).
- 4.1: "Play stops when `model.running` is false": true of the fork, but no framework code sets `running`, which the
  fork initialises to True (mesa_sim/mesa_fork/model.py 72); the solara-ui's play does not stop at a run's end.
- 4.4: Phase 7's deviation "applied at the next action boundary": superseded in part by T-H (25 September 2026): events
  may cut mid-action (`DuringAction`) (design_decisions.md, the entry's SUPERSEDED IN PART line).
- 4.2 lists the reading (A), the building (B) and two uses (C); it does not list the logging set-up at module level,
  nor that the start line, the override lines, `[sep]`, the per-step lines and the run's end are written by the
  headless loop and not by the model (fact 12). "The same logs" for the web-ui (12.3) depends on this; it bears on 0.2.
- 2.2: "viewer" is verified "in three places"; the repo has about 110 occurrences meaning a program (below).
- 13.4: the earlier chat's pause events `theta_crossed` and `task_committed` no longer exist (fact 9).
- 4.3: the drawer's dock_loading object colours also do not match the layouts' types (TODO-171, `delivery_area` and
  `empty_bay` against `delivery_bay` and `empty_pallet_bay`); kitting's area ids (`zone_NW` ...) still match.
THE WORD "VIEWER" FOR THE PROGRAM (item 5 of the task; nothing renamed; line numbers at 069282b; "reviewer" excluded:
handoff_G_X_onward.md 51, 74, 77; handoff_T-G_onward.md 32; handoff_T-G_stage1_MPB_onward.md 27;
handoff_T-G_stage1_onward.md 24):
- The present Solara program (the solara-ui): CLAUDE.md 439, 503, 702, 742, 745, 861; README of
  analysis/kitting/tb1b_two_tables 6; docs/artefacts_user_guide.md 111, 114; design_decisions.md 3870, 5017;
  design_records.md 556, 568, 574, 575 (twice), 1805, 2762, 3042, 4073; glossary.md 1529; roadmap.md 569, 573;
  TODOS_AND_DEFERRED.md 4459, 4462, 4477, 4824, 4827, 4828; handoffs: continue_T-F_part1_measurement.md 98,
  handoff_T-D_onward.md 61, handoff_T-F_part1.md 36, plan_T-F_part1.md 26, 39, plan_T-G_stage1.md 25, 54,
  plan_T-K_part1.md 360, 487, 489, 490, T-G_forward_inputs.md 509, 529. Code and data: mesa_sim/run_mesa.py 430 (the
  `Page` docstring); mesa_sim/viz/run_file_panel.py 5, 6; mesa_sim/overrides.py 24, 234; requirements.txt 9;
  tests/kitting/test_tl4_overrides.py 7, 157, 159 (159 is a test function's name,
  `test_the_viewers_write_keeps_the_run_files_comments`); domains/kitting/scenarios/scenarios_s06.py 156, 163;
  domains/kitting/layouts/env_layout_18.json 7 (its description).
- A planned program (T-E, T-V, Phase 7, a selector, later work): CLAUDE.md 292, 293, 582, 892 (twice), 894;
  design_decisions.md 3375, 3379, 3605, 3715, 3764, 4896, 5002, 5419; design_records.md 167, 1622; glossary.md 539, 931,
  1017, 1093, 1373, 1374, 1383, 1384; roadmap.md 381, 600, 605, 803, 804, 1055, 1058; TODOS_AND_DEFERRED.md 3628, 3633,
  4165, 4789; handoffs: handoff_G_X_onward.md 99, handoff_T-D_onward.md 11, 364, handoff_T-G_onward.md 56,
  handoff_T-H.md 49, phase7_interactive_deviations.md 11, 13, 16, 17, 24, 52, 62, 64, 65, 83, 104, 111,
  T-G_forward_inputs.md 775, 1108. Code: world/composition.py 32.
Whether any of these is renamed is open (handoff, 2.2).
GLOSSARY ENTRIES PROPOSED BY CCODE (not in the glossary; Hadi decides which are added): the 0.1 report of 6 October
2026 lists them (web-ui, solara-ui, screen-user, env-pane, scene, display place, author, and a §8 entry T-viz; no entry
proposed now for sim-run, start, preview, draft, run description, tick update, active and passive object, scene
appearance, shape kind, each with its reason).
FLAGS, outside T-viz's scope, not fixed: the solara-ui's hardcoded agent ids `robot_0` and `human_0`
(mesa_sim/mesa_fork/visualization/solara_viz.py 215 to 216); the drawer's per-domain colour tables (TODO-171); the
roadmap's Phase 2.2 line (fact 6); the README's "Mesa visualization (Solara) | Running" (README.md 190), to change when
the solara-ui becomes archived; `model.running` never set (above).

0.2, CODE STRUCTURE, DONE (ccode, 6 October 2026; the plan agreed by Hadi the same day, with his answers to Q1 to Q3
and three conditions). Handoff 7.2 built: the reading of the run configuration and the building of the model, and the
log pair with the run-level lines, are each one definition that every start uses; the log pair belongs to a sim-run,
not to a process (alternative B, Hadi's preference). Behaviour of the headless start unchanged (verified, below).
- `mesa_sim/run_config.py` (new): A and B of handoff 4.2, moved from `mesa_sim/run_mesa.py`: `DOMAIN_REGISTRY`, the
  choices, `RUN_OPTIONS` (the keys a run configuration may state, equal to the flags, a test holds them equal),
  `run_configuration(config, source, flags, cli_overrides)` (the checks of a run file applied to any mapping: a caller
  whose configuration did not come from the command line gets the same validation), `load_experiment` (the run file
  read, then `run_configuration`), the parser and `load_user_config(argv)` (with `UNDER_SOLARA` and `script_argv()`,
  needed by both starts), `resolve_triple`, `resolve_model_params`, `build_model`. It opens no file at import and
  imports nothing of Solara.
- `mesa_sim/sim_run.py` (new): `RunLog`, the log pair of one sim-run (`logs/run_<timestamp>.log` and `.rec`, relative to
  the working directory as before; a name already taken gets `_2`, `_3`); `SimRun(config, log)`, the start line and the
  override lines, the model (`build_model`), `step()` (the per-step agent lines and `[sep]`), `end()` (`end_run`, the end
  line, the pair closed), `close()` (the pair left without the end); `start_sim_run(read_config)`.
  - Point 6: the pair's lines are held in memory until the sim-run's first step or its end, which create the files; a
    model built and never stepped leaves no file. Cost: the lines of the build (about 11 lines, 1.7 KB, measured on
    scenario_s01_01) held in memory until the first step, one handler swap at the first step; the terminal echo is
    immediate as before. A headless start of 0 steps still writes its pair, since its end opens it.
  - Logging stays process-wide (the model, its agents and `shared/` log through the root logger and the logger `rec`):
    one pair is attached at a time, and a new sim-run closes the one attached before it, its files ending where they
    stand, or none if never stepped. Two sim-runs stepped alternately in one process do not get their own logs; how they
    could later: TODO-187, LOGGING SINCE T-VIZ 0.2.
  - Q2 (Hadi: a failed build writes its log pair, and the same reasoning for flag errors, unless every sweep script
    stops on a non-zero exit). The four maintained sweeps do not stop (`|| echo "$tag: exit $?"`, then the newest
    `logs/run_*.log` is copied); the instruments' `run.sh` and `run_set.sh` stop (`set -eo pipefail`). Chosen:
    `start_sim_run` creates the pair before the configuration is read, and on any failure before the sim-run exists
    (a flag error, a configuration error, a failed resolution or build, SystemExit included) opens it, so the start
    writes its pair: empty on a flag or configuration error, the lines before the error on a failed build, as before
    0.2. The policy is the start's: a later start (the web-ui) that treats a failed build otherwise creates its
    `RunLog` and `SimRun` itself and closes the log unopened, with no second copy of the logic.
  - Q1 (the end of a sim-run for a start that steps on request): not decided; it goes to the message round (stage 0.4).
    `SimRun.end()` exists; the headless start calls it after its N steps; the solara-ui never calls it, as before.
  - Q3 (agreed): the start line `[run_mesa] Starting headless run — ...` and the end line `[run_mesa] Headless run
    complete.` keep their text for byte-identity; every start writes them; TODO-191.
- `mesa_sim/run_mesa.py`: the starts only. `run_headless()` is `start_sim_run(load_user_config)` stepped `steps` times
  and ended; it re-exports the names of `run_config` its callers used. Under solara only, it imports `Page` from
  `mesa_sim/viz/solara_page.py` (new; the page moved unchanged but for its model), so a headless start imports neither
  Solara nor anything of `mesa_sim/viz/` or the fork's `visualization`.
- The solara-ui: start command unchanged, `solara run mesa_sim/run_mesa.py [-- <flags>]`. SolaraViz (vendored, not
  touched) builds its model by `model_class.__new__` and `__init__`; the page passes `SolaraSimRun`, which starts a
  sim-run of the run configuration, steps it, and hands every other attribute to its `SimModel`.
  THE SOLARA-UI'S LOGS CHANGE (condition 1): before 0.2 one pair per process, opened at import, holding the model's own
  lines only (every model the page built, stepped or not); since 0.2 one pair per stepped sim-run, holding also the
  start line, the override lines, the per-step agent lines and `[sep]`, as the headless start writes them; a reset or a
  reload starts a new pair at its first step; a model never stepped writes none; no end lines (Q1). Verified in both
  domains: its first pair equals a headless run of the same steps but for the start line's `steps=` (the run file's,
  50) and the end lines.
  THE LEAK, NOT FIXED (condition 1): the run-file panel's trial build of the overrides
  (`mesa_sim/viz/run_file_panel.py`, `SimModel(**{**model_params, "overrides": trial})`) is built outside any sim-run,
  so its build lines go to the sim-run attached at that moment: into its open file, or held for its first step. Before
  0.2 they went into the process's pair.
- `mesa_sim/list_scenarios.py` imports `DOMAIN_REGISTRY` from `run_config` (its own copy removed; its reason, that
  importing `run_mesa` opened a run's log files, is gone). Comments updated: `sim_agents.py` (the `rec` logger),
  `viz/portrayal.py`, `viz/space_drawer.py`.
- FLAG, not touched (agreed): `analysis/instruments/mpb/actual.py` builds the `SimModel` and states the run's end with
  its own code (a copy of reading, building and `end_run`); since 0.2 it could use `run_config` and `SimRun`.
HOW THE EIGHT POINTS WERE CHECKED (B0 at 5d6eb50, after the records session's ff23cef and 5d6eb50; B1 on the change):
1. Headless unchanged: B0 and B1 byte-identical in all 114 files: the four maintained sets (48 logs and their `.rec`,
   every md5 equal to the READMEs'), dock_loading's scenario_s03_02, s05_02, s07_02 (800 steps), a run with the three
   override kinds, a run of 0 steps, and four failed starts (a bad flag value, an unknown run-file key, an unknown
   scenario, an override out of bounds): the same exit codes, the same last line on stderr, the same log pair (three
   empty, one with the lines before the error). `mesa_sim/list_scenarios.py`: the same output (1019 lines). The test
   suite: 385 passed before, 398 after (13 new, tests/test_tviz_sim_run.py).
2. A headless start imports no Solara: a test runs `mesa_sim/run_mesa.py --steps 1` in a subprocess that refuses any
   import of `solara`, `reacton`, `mesa_sim.viz` or the fork's `visualization`; it completes.
3. The solara-ui works: `solara run` per domain serves the page (HTTP 200, no error); the page rendered in process per
   domain (`solara.render`, the loggers `solara` and `reacton` at ERROR as `solara run` sets them), Step three times,
   Reset, Step once: no file after the build, one pair per stepped sim-run, the first equal to the headless run as
   above. Hadi opens it in a browser once per domain before accepting 0.2 (condition 3).
4. A configuration not from the command line: tests give the same mappings to `run_configuration` and, as a yaml file,
   to `load_experiment`: the same refusal (unknown key, strategy, switch, test level, an override of an unknown object)
   and, for a valid one, the same configuration and a model.
5. Two sim-runs in one process, one after the other: tests: two pairs, each with its own start line; a sim-run left
   unended keeps its pair as it stood when the next began.
6. A model never stepped leaves no file: a test (three builds, none stepped: no file); the cost under point 6 above.
7. No second copy: `run_mesa.py` holds no reading, building or logging logic; the solara page calls `run_config` and
   `start_sim_run`; `list_scenarios.py`'s copy of the domain map removed. Outside 0.2: `actual.py` (flag above).
8. Callers of `run_mesa`: tests/kitting/test_tl1_artefacts.py and test_tl4_overrides.py use `resolve_triple`,
   `load_user_config` and `run_headless` from it unchanged and pass.

0.4, THE MESSAGES, BUILT (ccode, 6 October 2026; the plan confirmed by Hadi the same day, Q1 to Q9 each answered (a),
with six conditions). The messages between the web-ui and a simulator, and Mesa's piece that produces them; no server,
no page, no transport.
- What Hadi preferred for 0.4 (6 October 2026): the web-ui independent of the simulator (its page, its message
  definitions and the part of its server that answers the page in a folder of its own; only the piece that reads one
  simulator lives with that simulator) and of the domain (no domain name, object type or area id in its code or a
  message definition); a sim-run in the web-ui ends at the configured steps (further steps refused) and at the tick
  reached when the screen-user resets or changes a choice after the first step, its end lines written in both; every
  change of a choice builds the model, the page shows the start, the choices lock after the first step; all run
  options offered, the rules between them in the simulator's code, the page showing the values in effect the model
  reports; stage 1a shows no planned path (a question for 1b) and the actual world (the scene, what the human is
  doing), the robot's mind in 1b, plots in 1c. Taken from cchat's proposals (handoff, 7.4, 8.1 to 8.4): the page
  requests each step; three messages (a catalogue, a run description, a tick update with the complete changing state);
  each message names its sim-run (TODO-187); the order of arrival per container supplied by the simulator's side;
  typed classes defined once in Python; plain request and response.
  CHANGED (Hadi, 6 October 2026, preferred, at the plan of 1a; reason: a stopping point is needed for headless, not for
  a screen-user who can stop): the web-ui has no step limit by default; a sim-run ends at a limit only when one is set
  (`--steps` at the web-ui's start, or a number entered in the page), and otherwise by reset, by a change of choice or
  at the server's stop. Also changed: every change that completes a triple builds the model (a layout, or a layout and
  a setup, is shown without a model). Below, 1a, HADI'S PREFERENCES, item 3, and 1a, HADI'S ANSWERS ON THE PLAN.
- `webui/` (new, at the repo root): `messages.py`, the message definitions (pydantic v2, frozen, no extra field, strict;
  their JSON Schema for the page's types later); `simulator.py`, the interface a simulator's piece implements
  (`Simulator`: `catalogue()`, `build(choice, sim_run)`; `SimRunSide`: `description`, `state()`, `step()`,
  `end(reason)`, `discard()`; `BuildFailed`). Only message types cross it; the server (later) holds the rules (which
  sim-run is current, the end at the configured steps, the lock). Nothing in `webui/` imports `mesa`, `mesa_sim`,
  `domains`, `shared`, `world`, `ros_sim` or `solara`; the start that hands Mesa's piece to the server will live in
  `mesa_sim/`.
- `mesa_sim/webui_adapter.py` (new): `MesaSimulator` (the catalogue from `DOMAIN_REGISTRY` and the run file, default
  `configs/experiment.yaml`; the build of a `SimRun` from the choice) and `MesaSimRun` (per step its tick update, its end
  and its discard). It only reads the model.
- `mesa_sim/run_config.py`, two edits with no change of behaviour: `OPTION_DEFAULTS` (the fallbacks
  `resolve_model_params` wrote inline) and `ONE_OF_OPTIONS` (the three strategies and their values, which
  `run_configuration` checks in the same order), and the parser in its own function `user_args_parser()`, whose help
  texts are the catalogue's descriptions of the run options.
- `requirements.txt`: `pydantic==2.13.5` (Q2).
THE MESSAGES (fields, terms and sources as in the plan; the definitions are `webui/messages.py`):
- Catalogue: per domain its layouts (id, title: the file's `space.name`), setups, scenarios (id, setup, reference
  layouts, description); the run options, each declared by kind, `SwitchOption`, `OneOfOption` (a closed list of
  values), `LevelOption` (strictly between 0 and 1), `CountOption` (steps, at least 1), with its default (the run
  file's value, else `OPTION_DEFAULTS`) and its description; the default choice of a sim-run (the run file's triple and
  options).
- `SimRunChoice` (condition 2: the screen-user's choice of a sim-run; the kind of run option with a closed list is
  `OneOfOption`, its value `OneOfValue`): domain, layout, scenario, one value per declared run option.
- Run description: the sim-run's id; the triple; the choice as stated; the run options in effect (the model's
  attributes, the steps the configuration's); the world: the space (title, bounds), the areas, the fixed objects (id,
  type, subtype, position after an override, size), the movable objects (id, type, subtype, size, home container,
  designated destination), the humans, the robots, each human's script (its ordinary, repeatable and closing entries,
  each entry's task and typed events, its dependence), the timeline of context facts in force with its source.
- Tick update: the sim-run's id; the tick (Q1: the run log's number of the step executed, none at the start); the world:
  per agent its position and `last_motion`, the unit direction of its most recent step that moved it, computed in the
  piece from the agent's own positions (Q6, condition 3; the robot's perception memory of the human's last step is not
  read); `fixed_object_contents` and `carried` (below); the object states that hold; the timeline facts in force (the
  start's those of tick 0, as the robot's first observation has them); per human its `HumanActivity` (below); and, at
  the end, why the sim-run ended (steps reached, reset, choice changed, server stopped) and the entries still open.
- Refusals: `BuildFailure` (a choice that cannot be built) and `StepRefusal` (not current, ended, busy), for the server.
- Sections: the run description and the tick update hold the world under `world`; 1b adds the robot's mind beside it,
  1c the plots, each a new field with an empty default, so nothing 0.4 defines changes.
CONTAINERS (condition 1). The glossary's container (§10) is a fixed object of the layout that holds movable objects (a
shelf, a table, a bay, the truck), a kind of fixed object, not a state of one at a tick. The tick update does not use
the word for a field: `fixed_object_contents` lists the fixed objects that hold movable objects at that tick, each with
them in their order of arrival (at the start the setup's order; two arriving on one tick, the setup's order); `carried`
the movable objects held by an agent; every movable object is in exactly one of the two. A misdelivery (a release lands
on the nearest fixed object that is not movable, `mesa_sim/executor.py`) appears as such. Whether a page can know that
a fixed object is a container while it is empty: in stage 1a it cannot in general. The domains declare no container
types in code (the glossary's examples are prose), and the messages carry none. A page can know only the fixed objects
the run description names as a movable object's home container or designated destination, which are containers by §9
and §10; a container named by neither (a store no movable object starts in or is designated to) is known only once it
holds one. Knowing every container would need the domain to declare its container types and the run description to
carry them, open.
THE HUMAN'S ACTIVITY (panel 4a; condition 6: the messages carry all of it, which part panel 4a shows is a page design
matter of stage 1a). The world's side only: the human executor's record (`world/record.py`, `HumanAgent.record`) and its
stack machine (`world/human_executor.py`, `HumanAgent.machine`), nothing of the robot. Per human and tick: the stack,
top first (`truth_at`); the action in hand with its occurrence and its progress in ticks; the tick's typed transitions
(entered, started with its trigger and where, resumed, left with its outcome, refused, unfired, still open); the
script's entries still open (`open_entries`). Coverage and label A stay out: coverage is judged against the robot's task
model.
THE ORDER OF ARRIVAL AND THE LAST MOTION are kept by the piece per sim-run, so that a page reload keeps them; neither is
a world fact, neither is written anywhere. A display place is derived on the page from the order of arrival.
THE REQUESTS (for the server, not built): catalogue (no effect); choose (the current sim-run discarded if never stepped,
no file, or ended with `choice_changed` and its end lines if stepped; then the build: the start and override lines held,
no file yet; a failed build writes no log pair, Q4, and leaves no current sim-run); step (refused when not current,
ended or busy; the first step opens the pair; the step that reaches the configured steps ends the sim-run in the same
reply, `steps_reached`); reset (if stepped, ended with `reset` at the tick reached; then the same choice built again);
current (the current run description and latest tick update, for a page reload; no effect); at the server's stop a
stepped sim-run is ended with `server_stopped` (Q5).
RUN OPTIONS BY NAME, A DELIBERATE EXCEPTION AT THE INPUT BOUNDARY (Q3, condition 4). BUILD DISCIPLINE refuses
identification by string or key matching. Here the web-ui knows the run options only as the catalogue declares them,
each identified by its name: with a fixed typed class of the nine options the web-ui would name Mesa's run options and
change for a simulator with others, against its independence of the simulator. The name is matched once, in the piece
(`MesaSimulator._configuration`): a value of another kind, a missing, repeated or undeclared option, or a count below its
minimum is refused, and the mapping goes to `run_configuration`, which checks it as it checks a run file (whose own keys
are the same names). Inside the piece the values in effect are read by an explicit table per option (`_EFFECTIVE`), held
equal to the run options by a test.
THE OTHER ANSWERS: Q2 pydantic v2, pinned; Q7 the orientation of fixed objects left out (TODO-192, open, for the scene's
look; condition 5); Q8 the run file's overrides block is not part of a stage-1a choice (TODO-186), and the run
description gets an overrides field when that is decided; Q9 the object states and the timeline facts are in the tick
update.
GLOSSARY (Hadi approved the entries, 6 October 2026, preferred in the T-viz status words): §11 "The web-ui (T-viz)", web-ui,
solara-ui (tentative), screen-user, env-pane, scene, display place, author (the existing use described), catalogue, run
description, tick update. No entry for sim-run, start, preview, draft, active and passive object, scene appearance or
shape kind; "viewer" is renamed nowhere.
HOW IT WAS CHECKED:
1. The messages validate: for scenario_s01_01 (kitting, env_layout_01) and scenario_s03_02 (dock_loading,
   env_layout_02) the catalogue, the run description, the start and the tick updates after each of the first 20 steps
   and at the end, each written as JSON and read back against its definition, equal; every movable object in exactly
   one fixed object or held; at the start the setup's order; an object that stays keeps its place in the order; an
   agent that moved has its own step's direction as its last motion (tests/test_tviz_messages.py).
2. `webui/` imports nothing forbidden: its imports read from the source of every module, and `webui` imported in a
   subprocess that refuses `mesa`, `mesa_sim`, `mesa_fork`, `domains`, `shared`, `world`, `ros_sim` and `solara`.
   Proposed by ccode and added: no domain name, object type or area id of the registered layouts and setups appears in
   an identifier or string of `webui/`.
3. Producing messages changes no sim-run: the log pair of the headless sim-run and of the same sim-run with a tick
   update produced at every step, byte-identical, scenario_s01_01 for 300 steps and scenario_s03_02 for 800, to their
   end. A choice that cannot be built (seven cases) raises `BuildFailed` and writes no file; a sim-run discarded
   unstepped writes none.
4. The test suite: 398 passed before, 416 after (18 new). The four maintained sets (48 logs and their `.rec`) rerun on
   the change (`run_config`'s two edits) into a scratch folder: all 96 files byte-identical to the baselines on disk,
   whose `.log` md5s are those of each README's latest section (checked on tb1a).

0.2'S FAULT IN THE SOLARA-UI, FIXED (ccode, 6 October 2026; found in Hadi's browser check of 0.2; scope narrowed by Hadi
to one tab). The fault: a step raised `RuntimeError: a closed log pair is not opened again` (`mesa_sim/sim_run.py`,
`RunLog.open`, from `SolaraSimRun.step`). Reproduced under `solara run` with headless Chrome: two tabs on one server,
the first tab's Step after the second tab opened.
- The cause: since 0.2 one log pair is attached at a time, and a new `RunLog` closed the pair attached before it, so
  displacing a sim-run was treated as ending it. The solara server holds more than one sim-run in its process (a model
  per page session, and the one a Reset or reload leaves behind), and a page that steps a sim-run another one displaced
  reopens a closed pair.
- The fix (`mesa_sim/sim_run.py`): a new pair detaches the pair attached before it instead of closing it; a sim-run's
  step and end attach its own pair again (`RunLog.attach`, `RunLog.detach`). Only `close()` (a sim-run's end, or its
  owner leaving it) ends a pair. What happens to the log of a displaced sim-run: its files, if opened, stay open and
  stop growing while it is displaced; its next step or end attaches it again and its lines go on in its own files; if
  it is never stepped again, its files end where they stand (and a pair never opened leaves no file, as before).
  Steps of two sim-runs taken one after the other each go to their own pair. Headless is unchanged (one sim-run per
  start): the four maintained sets rerun, all 96 files byte-identical; the test suite 417 passed.
- The test: tests/test_tviz_sim_run.py, `test_a_displaced_sim_run_steps_again_into_its_own_pair` (two sim-runs
  stepped alternately in one process: no error, each one's lines in its own pair); it fails on the code before the fix
  with the same RuntimeError.
- Checked by Hadi, not by ccode after the fix: the one-tab sequence Step, Play, pause, Reset, then Step and Play again,
  on both domains. Before the fix, in one tab, Play then Reset and a reload during Play did not raise (headless Chrome).
- Known limits of the solara-ui, not fixed (it is archived after stage 1a), not tested after the fix, by reading:
  - Two tabs on one server: no error; two steps at the same moment in two tabs could write a line into the other
    tab's log pair (logging is process-wide).
  - A tab left open from an earlier server on the same port: the same as two tabs once it reconnects.
  - A reload during Play: the sim-run left behind is no longer stepped; its pair ends where it stands.
- The web-ui's piece (`mesa_sim/webui_adapter.py`), by reading: the same cause could occur there before the fix, since
  `MesaSimulator.build` creates a `RunLog`, which closed the current sim-run's pair, and a `MesaSimRun` stepped
  afterwards would have raised. The server's rules (the current sim-run ended or discarded before a build; a step on a
  sim-run that is not current refused) keep it from being stepped; since the fix it would attach its own pair again.

0.3, THE STYLE TRIAL, BUILT (ccode, 6 October 2026; the plan, P1 to P8, confirmed by Hadi the same day, "Go, with (a) on
Q1, Q2 and Q3", with six notes). The env-pane of the web-ui's page, drawing the start of one real sim-run per domain
from saved messages, tilted and from above. Two things are decided by it: the page framework and the drawing library
for every stage (handoff, 6.1 item 6; 10.8), and whether Hadi's style direction (handoff, 10.2, 10.5) can be produced.
Hadi's review of the picture is open; nothing below is preferred until he says so.
- The technology (proposed by ccode, the plan confirmed by Hadi for the trial): React 19 and TypeScript on Vite, the
  scene in three.js through React Three Fiber and drei, every dependency pinned exactly (`webui/page/package.json` and
  its lock file; Node.js 22.12 or later). The reasons per need, as the plan gave them: the tilted and the top view are
  one scene and one orthographic camera in two poses; the look (flat pale faces without lights, the shaded side hatched,
  thick outlines) is one shader material and drei's fat-line edges; a tick moves existing meshes; panels are React
  components on the theme, no UI kit; growing plots in 1c with uPlot (named, not installed); clicking through R3F's
  pointer events, dragging by projection onto the floor; two env-panes as two canvases or drei's `View`; the most
  common, best-typed stack for this page. Rejected: three.js without React (panels and state by hand), Babylon.js
  (heavier, game-oriented, no easier for this look), 2D drawing in SVG, PixiJS or Konva (two drawings, not one camera;
  depth and height faked), Svelte or Vue with their three.js bindings (smaller ecosystems), Plotly or Solara (6.1),
  deck.gl (maps and data layers). The page's types are generated from the Python definitions: `webui/schema.py` writes
  the JSON Schema of the page's messages, `npm run gen:types` the TypeScript (`webui/page/src/gen/`, committed).
- The sim-runs (P3): kitting scenario_s02_01 on env_layout_02 (every kind of kitting object, 8 items on 8 shelves);
  dock_loading scenario_s08_01 on env_layout_03 (pallets in the truck and in every bay at the start: the display places
  in four containers). `mesa_sim/webui_export.py` builds each through Mesa's piece, writes its run description, its
  start tick update and its domain's scene appearance to `webui/page/public/samples/` (git-ignored), and discards the
  sim-run unstepped (no log pair). Stage 1a's server replaces it.
- The scene appearance (P4; Q1 to Q3 each (a); handoff, 10.6 items 1 to 3): `webui/appearance.py` defines it, a domain
  states its values in `domains/<domain>/appearance.json` (kitting, dock_loading; not in a layout or a setup file, not a
  world fact; the simulation never reads it). Per object type a form, a height in the layout's unit and a presence; per
  movable type a form and a height; the human's and the robot's figure and height; a default for a type with no entry
  and for a domain with no file.
  - THE LIMIT OF THE SHAPE VOCABULARY (Hadi's note 3): a new domain is drawn without a code change, from defaults (every
    fixed object a hatched block, every movable object a crate; checked: the kitting sample drawn with the default
    appearance). A new form is web-ui code. The vocabulary names forms, never a domain's object types: block, rack,
    counter, pad, enclosure, appliance, panel, seat, marker, barrier; crate, skid; person, cube-head robot, lift vehicle.
    No form has a front, since the messages carry no orientation (TODO-192); the lift vehicle faces the agent's
    `last_motion`, north before the agent has moved (a display convention).
  - PRESENCE (Hadi's note 2): a property of the look, declared per object type in the appearance data (background or
    active); not a world fact. Deriving it from a run's bindings (handoff, 10.6 item 4) was measured and found unstable:
    in scenario_s08_01 the human's script binds no coffee machine (its entries are confirm_delivered_pallet(pallet_2)
    and the closing go_to(desk)), so the coffee machine, Hadi's example of an active object, would be drawn passive,
    while every landmark a go_to binds (desk; kitting's corner_SE) would be drawn active; and the same object type would
    change its look from one scenario of a room to the next.
  - Q1, how the appearance reaches the page in stage 1a, stays open (Hadi's note 1). ccode's recommendation: the
    catalogue's per-domain entry carries it, read by the simulator's piece. In the trial it is a file beside the samples.
- The look as built (one treatment, P6). Three levels of presence: the space, the areas and the background objects as
  lines and pale faces (toward sketch A: thin members drawn as single strokes, open racks, see-through panes); active
  objects in a warm neutral tone with a representative form; the agents as figures in their semantic colours (robot
  blue, human orange), each on a faint ring of its colour. Movable objects are solid ink (image 4's cargo): what can
  change stands out. The side away from the light is hatched in screen space; soft floor shadows. Labels: the agents in
  white pills with a dot of their colour (sketch J, image 13); fixed objects and areas by their ids written on the floor
  (image 4), small and light for passive things (Hadi, during the session: "they are not informative"), in the active
  tone for active objects; an area's id in the first of its corners, farthest from the room's centre first, where it
  covers no fixed object. One theme file, `webui/page/src/theme.ts`, holds the colours, line weights, spacing and type
  sizes; the page's CSS reads them as variables and the scene takes its colours only from it. Light only.
- Display places (handoff, section 9): a grid over the footprint in the order of arrival, the grid that holds the
  objects at their own size and whose shape is nearest the footprint's, the gap shrinking to what the footprint leaves,
  overlap only when no grid fits; contents at the form's rest height (a rack's upper board, a counter's top, the floor
  of an enclosure or a pad). The rule and the statement that a display place is a display convention, written nowhere,
  are in `webui/page/src/env-pane/displayPlaces.ts` and the page's README. Requirement 2 (a place kept while the object
  stays) is stage 1a's: the trial draws one tick.
- The checks: the screenshots of both domains in both views, in Google Chrome through `npm run shots`, at
  `docs/handoffs/tviz_trial/` (untracked, Q3), compared with images 4 and 12 and sketch J and revised five times before
  the report; `npm run build` passes (one script of 1.30 MB, 367 kB compressed: three.js and drei); the test suite 418
  passed (417 before, one test added; the existing domain-word test reads string literals with `literal_eval` and
  cannot read an f-string, so `webui/schema.py` uses none). The added test, `test_the_page_names_no_domain_object_type_or_area_id`, scans the page's own files
  (code, styles, configuration, the generated types; not `node_modules`, `dist`, the samples or the lock file) for the
  domain names, object types and area ids of every registered layout and setup.
- What the library made easy: the two views by the camera alone; outlines of a set pixel width (drei's `Edges`, fat
  lines); text lying on the floor from a bundled font; HTML labels pinned to a point of the scene. What it made hard: the
  illustration look needed its own shader (the tones by the face's direction, the screen-space hatching); `Edges` draws
  creases, not silhouettes, so a sphere or a cylinder's side has no outline; a thin box outlined on every edge reads as
  a double line, so thin members became strokes; see-through faces depend on draw order; labels have no layout engine,
  so placement is by hand.
- Found while drawing from the messages (for the message round of 1a, nothing changed):
  - Agents have no size in the messages; a figure's height and its ring are the appearance's.
  - An object state cannot change a form unless the appearance maps a state to a variant (an empty pallet looks like a
    full one; the gate's `is_open` is not drawn).
  - An area's `label` in the layout (kitting's "southwest_storage") is not carried; the page shows the area's id.
  - The layout's `space.name`, the env-pane's title, is stale in older layouts (env_layout_02 is titled "Kitting Domain
    Layout 1"); a layout file question, not a message one.

STAGE 0 CLOSED (Hadi's answers on the trial, 6 October 2026, preferred, not ruled; recorded by ccode the same day,
records only, no code changed). T-viz stage 0 is done: 0.1 recording, 0.2 code structure, 0.4 the messages, 0.3 the
style trial. Next within T-viz: stage 1a, when Hadi asks for it; the place of T-viz stage 1 in the order of the tasks
stays open (TODO-190, point 4).
- HADI'S ANSWERS ON THE TRIAL:
  - The trial's look is accepted "for now and for stage 0". It is the starting point of stage 1a, not a final design.
  - The technology of the trial is the web-ui's technology: React, TypeScript, Vite, three.js through React Three Fiber
    and drei. uPlot is planned for the plots of stage 1c. No UI kit.
  - The 0.3 report's questions: (1) how the scene appearance reaches the page is settled in stage 1a; (2) the tilted
    view at 35° and the view from above stay as presets, and in stage 1a the screen-user can change the camera freely
    during a sim-run, rotating, tilting, zooming and moving it (TODO-195); (3) an object's state may change its shape (an
    empty pallet, an open gate), with minimal effort, in stage 1a (TODO-194); (4) a figure turns at once to its last
    direction of movement, with no rotate action in the world, and before its first move it faces a default, as a
    display convention; (5) labels show the ids; (6) no dark mode in stage 1, recorded for stage 2 or 3 (TODO-193).
- HADI'S OTHER PREFERENCES SINCE THE HANDOFF, checked against the records:
  - No single "mother" start command now; the README states the command of each start. The question of one command with
    subcommands returns in stage 1a, when the web-ui's start command is defined (TODO-196). Not recorded before; added.
  - The web-ui is independent of the simulator and lives at the repository's root; only one piece per simulator lives
    with that simulator. Recorded in 0.4 ("What Hadi preferred for 0.4"); Hadi's reason, added here: a later simulator or
    ROS may replace Mesa, and the web-ui stands above any one of them.
  - Stage 1a shows no planned path; whether and which paths the scene shows is a question for stage 1b. Recorded in 0.4;
    TODO-197 added. The item "Preferred, replaceable: an agent's path is a straight line now" under PREFERRED BY HADI
    above is superseded in part: the model holds no path per agent (0.1, fact 3), and stage 1a shows none.
  - Everything of stages 2 and 3 stays [FW] until Hadi draws the V1 border for the web-ui. Recorded (HADI'S ANSWERS,
    TODO-190); unchanged.
- MEASURED for the state after stage 0 (ccode, 6 October 2026): the catalogue is 645 KB as JSON, 40 KB compressed
  (`MesaSimulator().catalogue()`, the run file `configs/experiment.yaml`), mostly the descriptions of 1019 scenarios (721
  in kitting, 298 in dock_loading). The log pair's handlers sit on the root logger at the INFO level
  (`mesa_sim/sim_run.py`, `RunLog`), so any library logger that propagates to the root logger, a web server's for
  example, writes into the open sim-run's log; stage 1a's server must keep such lines out (open how).
- THE RECORDS OF THE CLOSE: `docs/handoffs/handoff_T-viz.md` gained the section "State after stage 0" at its top (what
  exists in the code, what Hadi prefers now, what stage 1a starts from, what is still open with the stage of each); its
  body is corrected where stage 0 showed it wrong, each passage kept and a dated line with its reason beside it
  (among them T-E and T-V, `planned_path`, the logging at import, the places of "viewer"); its correction note is
  shortened to a pointer. The roadmap's T-viz bullet, CLAUDE.md's status block and the README (the commands of the
  starts and the trial page) are updated; TODO-193 to TODO-197 are added. The solara-ui is not marked archived: that
  begins when Hadi accepts stage 1a. "Viewer" is renamed nowhere.

1a, HADI'S PREFERENCES (Hadi, 6 October 2026, preferred; recorded by ccode the same day, records only, no code
changed). Six preferences for stage 1a, given with the task of its plan:
1. The size of 1a. One plan covers the whole of 1a; ccode builds it in increments and pauses after each for Hadi's
   review. Reason: the technology and the page layout are designed for the whole stage, and Hadi sees agents move in
   the browser after the first increment.
2. The order of the selection: domain, layout, setup, scenario. Reason: Hadi wants to look at a room first, compare
   several, then go to its setups. The setups offered for a layout X are the setups that have at least one scenario
   with X among its reference layouts; the scenarios offered are the scenarios of the chosen setup.
   Proposed by cchat, not marked by Hadi: the web-ui therefore offers only these combinations; a sim-run on a layout
   outside a scenario's reference layouts stays possible headless and is not offered in the page.
3. After a layout is chosen and before a triple is complete, the env-pane shows the layout alone: the space, the areas,
   the fixed objects, no model. The handoff's 7.5 changes accordingly: every change that completes a triple builds the
   model. Reason: item 2's way of choosing, a room seen before its setups. Condition: the layout-only description is
   read through the same loader that the model uses, so that a layout's picture cannot differ from the picture of a
   sim-run on it. cchat told Hadi that this is a small amount of work (a subset of the run description, one request,
   one more page state); ccode confirms the cost in the plan (below: the loader reads the layout inline in
   `SimModel.__init__`, so its layout part moves into a function of its own first).
4. The scenario list of 1a shows each scenario's description beside its id and offers a plain text filter over id and
   description. Reason: Hadi cannot select a scenario from its id alone. The structured filter by composition
   (TODO-110) is stage 2, [FW].
5. Panel 4a shows the action in hand with its progress and the task it belongs to; the human executor's stack (the
   task in hand and the interrupted ones below it); the last few switches and resumptions with their ticks. Hadi
   adjusts it after he sees it. Reason: what the human is doing, and how it changed, is what panel 4a is for (the
   handoff's 12.3, part a); the right amount is seen only on the page.
6. The start: one command per start. The web-ui's start command is a file in `mesa_sim/`; it accepts the same run file
   and flags as the headless start, so that the page can open with a sim-run already chosen. `webui/` stays at the
   repository's root and imports no simulator. Reason: the web-ui stands above any one simulator (0.4), and its start,
   which hands Mesa's piece to the server, belongs with the simulator. TODO-196 is answered for now; it returns when a
   second simulator exists.

1a, THE PLAN, WRITTEN (ccode, 6 October 2026; for Hadi's review; every item proposed by ccode and open until Hadi says
"I prefer"; nothing built). `docs/handoffs/plan_T-viz_1a.md`, which every build session of 1a reads first. It holds:
four increments, each with its scope, what Hadi sees at its end, and its checks: (i) the server, the start, the page's
frame, a minimal choice, the moving env-pane; (ii) the full selection, all run options, lock and unlock; (iii) the
env-pane additions (free camera, a look by state, display places kept, a reload keeping the picture); (iv) panel 4a,
test 2, the close. Two changes from cchat's proposal, with reasons: the page layout is built in (i), test 1 is run
in (i). The message round of 1a (the catalogue carrying each domain's scene appearance and the notes of layouts and
setups; the view of a layout; the request `view`, and `current` returning every tick update of the sim-run; looks by
state in the appearance; agents without size and areas labelled by their id); ccode's proposals on the open items 1, 2,
3, 5, 7, 9 and 10 of the handoff's "State after stage 0"; the page layout for the whole of stage 1; the two tests and
how a web-ui sim-run writes the same log pair as headless; three questions to Hadi (Q1 what the env-pane shows with a
layout and a setup and no scenario; Q2 the key of dock_loading's layout notes; Q3 what the page opens on without a run
file).
VERIFIED for the plan (at e5de942; the plan's section 1 has the detail):
- Every one of the 1019 scenarios names exactly one reference layout, so the page offers exactly 1019 triples.
- Scenarios per pair of layout and setup: kitting 33 pairs, 1 to 52 scenarios, median 21; dock_loading 10 pairs, 7 to
  58, median 19; 1 to 3 setups per layout; three kitting setups are offered under two layouts each.
- Layouts and setups carry no description field. Free-text notes that nothing reads: `space.notes` in 19 of kitting's
  20 layouts, `space.note` (singular) in dock_loading's 4; a top-level `notes` in kitting's env_setup_17 to _30 and in
  all 10 of dock_loading's setups.
- The loader reads the layout inline in `SimModel.__init__` (the space, the areas, the first pass of `_init_objects`);
  no function reads a layout alone. Item 3's condition needs that part moved into a function, with headless
  byte-identity as its check; otherwise the cost is as cchat stated.
- Agents are points in the model; an area's `label` is in 22 of the 24 registered layouts and read only by `ros_sim/`.
- Starlette 0.48.0 and uvicorn 0.30.5 are installed (Solara's dependencies); FastAPI and httpx are not.
- A tick update is about 1.3 KB as JSON (1.0 to 1.8 KB over scenario_s02_01 and scenario_s08_01).
- In all ten of dock_loading's setups the gate is open from the start (`is_open`).
- The terms of panel 4a: "action in hand", "switch", "resumption" and "progress" have no glossary entry of their own
  (the entry **record** names the queries `switches` and `resumptions` and "the action and its progress"); **stack**,
  **record** and **outcome** have entries. The plan uses "suspended" (an outcome) for item 5's "interrupted ones".

1a, HADI'S ANSWERS ON THE PLAN (Hadi, 6 October 2026, preferred; recorded by ccode the same day, records and the plan
only, no code changed). `docs/handoffs/plan_T-viz_1a.md` is amended to match (its P7 to P16). Every other proposal of
the plan stays proposed by ccode; Hadi reviews each at the pause after its increment.
1. Q1 (b). With a layout and a setup chosen and no scenario, the env-pane shows the layout with the setup's movable
   objects in their home containers and the setup's object states, no agents. Reason (the plan's): what distinguishes
   two setups of one room is which objects lie where. The setup's part of the loader moves into a function as the
   layout's does.
2. Q2 (a). The key `space.note` of dock_loading's four layout files is renamed `notes`, in increment (ii).
   Reason (ccode's reading; Hadi stated none): one key for the notes of every layout; nothing reads it, no sim-run changes.
3. Q3 (a). Started without a run file, the page opens on the default run file's sim-run at its start. Reason (the
   plan's): one rule for every start, as the headless start runs the default run file, and the page is never empty.
4. The page's choice mirrored in the address is kept, with one rule: the server's state wins. If a stepped sim-run is
   current, the page shows it and ignores the address; otherwise the page requests the address's choice. Reasons: a
   bookmark per scenario for a demonstration; a link that can be embedded in web-based slides, a later task Hadi will
   open (no name and no letter yet). Limits: the link is not a run file (TODO-189); it reopens a choice at its start,
   not at a tick; one server holds one current sim-run (TODO-187).
5. The web-ui has no step limit by default. This changes 0.4's preference "a sim-run in the web-ui ends at the
   configured steps" (0.4's dated line above). Reason: the solara-ui runs without an end; a stopping point is needed for
   headless, not for a screen-user who can stop. Proposed by cchat and worked out in the plan (its M8 and section 4,
   item 11): the web-ui does not use the run file's `steps`; a limit applies only with `--steps` at the start or a
   number entered in the page; the steps option becomes optional in the messages; without a limit a sim-run ends by
   reset, by a change of choice or at the server's stop; test 1 states its steps; the control bar shows the steps done
   without a bar when there is no limit.
6. Play pauses by itself at the tick where the human's script has ended and the robot's pool is empty (the point MPB-5
   names); the page states that all agents have finished. The sim-run is not ended; step and play continue to work. A
   sim-run that never reaches the point is not paused. Reason (ccode's reading; Hadi stated none): the screen-user
   sees where the work ends without the sim-run ending there. The value's place proposed in the plan (M7): a third section `run` of the tick update, beside
   `world`, holding `finished_at`.
7. TODO-33 gets Hadi's idea, not decided: every start stops when no agent has anything left scheduled or scripted;
   with three facts (TODO-33). The first, "every maintained baseline log runs past that point", was measured: 46 of 48
   run past it; the two logs of scenario_s02_01 end five ticks before it, the human still on its closing walk.
8. The run options stay as set when the layout, the setup or the scenario changes. Reason (ccode's
   reading; Hadi stated none): a screen-user comparing scenarios under one set of options does not set them again.
9. Panel 4a's words "action in hand", "progress", "switch" and "resumption" get glossary entries describing their
   existing use, as "author" did in 0.4; ccode words them, Hadi does not review them (glossary §6, after **record**).
   "Suspended" stays the word for the task below the top of the stack.
10. Test 2's limit is stated in the plan: a copy of dock_loading under a new name shows that a domain without its own
    look is drawn; it does not show new object types or area ids, which the code scan covers.
cchat's note on the display places (visual design, ccode's to decide): the plan placed a container's objects from its
north-west corner, so a container with one object no longer showed it centred, as the trial Hadi accepted did.
DECIDED BY CCODE (proposed, in the plan's section 4, item 10): the places are taken from the centre outward, numbered by
their distance from the footprint's centre, so a lone object sits in the middle while no place moves; where the grid
has an even count along an axis, a lone object sits half a place off the centre.
WHAT THE ANSWERS MEET IN THE CODE AND IN 0.4 (ccode, 6 October 2026; worked out in the plan, nothing built):
- Item 5 against 0.4: `steps` is declared as a `CountOption` (minimum 1) whose default is the run file's, and the
  catalogue refuses a run file that states none (`mesa_sim/webui_adapter.py`, `_declarations`); a `SimRunChoice` must
  give every declared option a value. Proposed: `CountOption` and `CountValue`, used only for steps, become
  `LimitOption` and `LimitValue`, whose value may be none.
- Item 5 against the code: `SimRun` reads `config["steps"]` for the start line's `steps=` field, which has no value
  without a limit. Proposed: `steps=none` for a web-ui sim-run without a limit; headless and a sim-run with a limit
  write the number as now. Such a log pair differs from every headless pair in that field only.
- Item 5, a consequence: without a limit a sim-run's tick updates grow with it (about 1.3 KB per tick; 13 MB at 10 000
  ticks), all held by the server for `current` and by the page. Noted, no limit set.
- Item 6 against 0.4: the tick update holds the world only, and the point is not a world fact: the robot's pool is the
  robot's side (`RobotAgent.finished`, set on the tick of its `[meta] ... all tasks complete` line, the declared tick,
  TODO-127; the tick the test-beds read as MPB-5's point). The human's script has ended when every ordinary and
  closing entry is closed and the stack is empty (`HumanStackMachine.all_closed()`). Hence the plan's third section.
- Item 4: no conflict with the code or with 0.4. The page tells a stepped sim-run from the tick updates `current`
  returns (the plan's M3). Two tabs on one server share the current sim-run (TODO-187): a second tab opened while one
  is stepped shows it, whatever its address says.

1a, INCREMENT (i), BUILT (ccode, 6 October 2026; `docs/handoffs/plan_T-viz_1a.md`, section 2 (i), as amended at
a7ffcb0; every item proposed by ccode unless marked preferred; Hadi's review at the pause after it is open). The server,
the start, the page's frame, a minimal choice, the moving env-pane; nothing of increments (ii) to (iv).
- `webui/server.py` (new): the web-ui's server on Starlette and uvicorn (both already installed; uvicorn pinned in
  `requirements.txt`, starlette moved to the web-ui's block). Its rules: one current sim-run; a choice ends a stepped
  one (`choice_changed`) or discards an unstepped one; the step limit, when set, ends the sim-run in the answer of the
  step that reaches it (`steps_reached`), and a later step is refused (`ended`); a reset ends or discards the current
  one and builds the same choice again; a second step while one runs is refused (`busy`); at its stop (Ctrl+C) a stepped
  sim-run is ended (`server_stopped`). Every call into the simulator's side runs on one worker thread. The requests:
  GET catalogue, POST choose, POST step, POST reset, GET current (the current sim-run with its latest tick update, as in
  0.4; every tick update is (iii)'s M3); answers over 1000 bytes compressed; 127.0.0.1 only; the built page served at /.
  It imports no simulator and names no domain word.
- `mesa_sim/run_webui.py` (new): the web-ui's start (P6): the headless start's parser, as strict, plus `--port`;
  `--steps` the default step limit, the run file's steps not used and said so on the terminal (P11); a run with an
  override, or a layout outside the scenario's reference layouts, stops the start; the built page (`webui/page/dist`)
  missing or older than its sources stops the start, naming the build command.
- `mesa_sim/sim_run.py`: `RunLog(echo, own_thread_only)`, both as before by default (headless and the solara-ui
  unchanged); a web-ui sim-run's pair takes only the lines logged on the thread that created it and does not echo
  (section 4, item 9); `SimRun` writes `steps=none` on the start line for a sim-run without a step limit (item 11).
- `mesa_sim/webui_adapter.py`: `MesaSimulator(config, step_limit)` (the start's run configuration and default limit;
  by default the run file configs/experiment.yaml and no limit); the catalogue's per-domain `appearance` (item 1;
  `appearance()` moved here from `mesa_sim/webui_export.py`); the step limit as `LimitOption` and `LimitValue`, value
  None for no limit (M8); `finished_at` (M7) from `HumanStackMachine.all_closed()` with an empty stack for every human
  and `RobotAgent.finished` for every robot.
- `webui/messages.py`: `CountOption` and `CountValue` became `LimitOption` and `LimitValue`; `DomainEntry.appearance`;
  `RunTick` (`finished_at`) as the tick update's section `run`; the server's bodies and answers `SimRunRef`,
  `SimRunState`, `Current`; the base class `Message` moved to `webui/message_base.py` (item 1's change of form).
  `webui/simulator.py`: the one-thread contract. `webui/schema.py`: the new answers among the page's types.
- The page: `src/App.tsx` (the frame of section 5 and the play loop), `src/api.ts` (the requests; `src/data.ts`, the
  samples' reader, removed), `src/frame/SelectionPanel.tsx` (five columns; in (i) the domain and a scenario from the
  domain's whole list, the layout and the setup the scenario binds, the run options as stated and in effect, read
  only), `src/frame/ControlBar.tsx` (reset, step, play and pause, the speed 1 to 20 ticks per second or as fast as the
  server answers, default 5; the tick and the steps done, of the limit with a bar when one is set; "All agents have
  finished at tick N"; the end and its reason), `src/env-pane/Scene.tsx` (what is constant drawn once per sim-run; each
  agent drawn in a group that glides to the tick's position over the tick's display time during play, at once when
  paused or stepped), `src/env-pane/EnvPane.tsx` (the control bar at its foot), `src/styles.css`, `vite.config.ts` (the
  dev server passes /api/ to port 8000), `scripts/shots.mjs` (rewritten to drive a running web-ui). Panel 4a is its
  titled place, filled in (iv); 4b a rail, 4c a strip, each with its title.
- README: the web-ui's start replaces the trial page's commands; `webui/page/README.md` rewritten. `.gitignore`:
  `docs/handoffs/tviz_1a/`.
THE CHECKS (each run on the change; B0 the baselines on disk and dock_loading's three runs taken before the change):
1. Test 1, in both domains (`tests/test_tviz_server.py`): the server as its own process, driven over HTTP to its step
   limit (scenario_s01_01, 300 steps; scenario_s03_02, 800), writes a log pair byte-identical to the headless start's
   with the same flags; a step after the limit is refused. A sim-run without a limit reset at tick 37 equals the
   headless run of 37 steps but for `steps=none` on the start line. Passed.
2. The thread filter's test: a line logged on another thread stays out of a web-ui pair, the pair's own thread's lines
   go in. Passed. Also read: the 20 log pairs the web-ui wrote during this session's browser checks hold no line of the
   server or a library.
3. The point where all agents have finished: a test on tb1a's eight sim-runs (assignment knowledge on) and a one-off
   check on all 48 of the four maintained sets, each built and stepped through the piece: `finished_at` equals the
   point read from the log pair (the robot's empty-pool tick, or the human's first tick with the stack empty for good,
   whichever is later), None before it; 46 of 48 reach it (scenario_s02_01 reaches it at 455, after its 450 steps); and
   the piece's own log pair of each of the 48 is byte-identical to its baseline.
4. Headless byte-identical: the four maintained sets (48 logs and their `.rec`) and dock_loading's scenario_s03_02,
   s05_02, s07_02 (800 steps), rerun into a scratch folder: 102 files, 0 differ.
5. The test suite: 418 passed before, 432 after (14 new).
6. The solara-ui: `solara run` serves per domain (HTTP 200); its sim-run, built from the command line's configuration
   as under solara, steps three times in each domain, each into its own log pair.
7. The page: `npm run build` (the type check and the bundle) passes; the bundle is 1.30 MB, 370 kB compressed, the same
   warning on its size as in 0.3.
8. Screenshots in Google Chrome (`npm run shots`, `docs/handoffs/tviz_1a/`, untracked): kitting scenario_s02_01 and
   dock_loading scenario_s08_01, each chosen in the page; a moment after 60 steps, tilted and from above, at 1440 and
   1920 wide; play as fast as possible from the start, pausing by itself where all agents have finished (kitting at
   455, dock_loading at 127); an end at a step limit of 40; and the run options with `--human_aware false`, the three
   options it sets off marked "off in effect". The server's stop by Ctrl+C ended a stepped sim-run (`server_stopped`).
DEVIATIONS FROM THE PLAN, each with its reason:
- Test 1 starts the server with the start's own reading of the command line (`run_webui.read_start`) and `serve` without
  the page, in its own process, not `mesa_sim/run_webui.py` itself: the start's page check would make the test depend on
  a build of the page with Node.js. The start's checks are tested in process.
- The point of P12 is tested on tb1a's eight sim-runs in the test suite and on all 48 in a one-off check whose result
  is above: the 48 take minutes and are a check of the build, not of every later change.
- A reset of a sim-run that is not the current one is refused with `StepRefusal` (`not_current`), the refusal 0.4
  defined for steps; no reset refusal of its own.
- Item 1's check that every state an appearance names is a state the domain declares is not built: the appearance
  names no state before item 2 (iii).
- The `--steps` flag's help text, which is also the step limit's description in the catalogue, now names both uses
  (the headless start's `--help` changes, no log).
FLAGS (outside (i), not done): `mesa_sim/webui_export.py` and the samples under `webui/page/public/samples/` are no
longer read by the page; whether they are removed is Hadi's. In the tilted view an agent at a kitting table is partly
hidden under the table's top (the handoff's 10.6, item 5), seen in the screenshots; a question for the review.

1a, HADI'S REVIEW OF INCREMENT (i) (Hadi, 6 October 2026, preferred; recorded by ccode the same day, before any code
of increments (ii) and (iii)). Hadi tried increment (i) in the browser in both domains. It works for him as a first
stage; he will ask for tuning later. `docs/handoffs/plan_T-viz_1a.md` is amended to match (its P17 to P24, and the
increments of its section 2). Every proposal of the plan not named here stays proposed by ccode.
1. The selection panel folds at the first step and reopens from the header's button: kept.
2. Panel 4a is 300 px wide for now and may grow to 400 px; its width is adjusted in increment (iv). Panel 4b stays a
   thin rail until stage 1b.
3. The control bar stays under the env-pane, for now.
4. The env-pane's header shows the layout's id only, not its title, for now, until the stale titles are corrected. The
   open item on the stale titles (the handoff's "State after stage 0", open item 12) stays open.
5. Table tops are drawn see-through in increment (iii), so that an agent at a table is not hidden (the flag of
   increment (i)). Hadi judges it when he sees it.
6. The default play speed stays 5 ticks per second.
7. `mesa_sim/webui_export.py` and the saved sample messages of the 0.3 trial (`webui/page/public/samples/`) are removed
   in increment (ii), after verifying that nothing else reads them; the README is updated where it names them.
8. The order of the rest of 1a: increments (ii) and (iii) are built together, with no pause between them; then one
   pause for Hadi's review; then increment (iv) in a new session; then a new increment (v), polishing. For (v) Hadi
   gives a written list, and ccode works that list and nothing else. Whether a second polishing round follows after
   stage 1c is open.

1a, THE MODE OF CHECKS FOR THE REST OF STAGE 1 (Hadi, 6 October 2026, preferred; given during the build of (ii) and
(iii) and applied to it). Stage 1 is a prototype: Hadi will change the page layout and the design soon, so product-level
checks of the page cost more time than they save. Kept: headless logs byte-identical whenever code under `mesa_sim/`,
`shared/`, `world/` or `domains/` changes (a difference stops the work); the test suite once at the end of each
increment; the page's build and type check; one look in a real browser per new feature, at one window size, to confirm
it renders and works (what is broken is fixed, the look not refined). Dropped or deferred: screenshot sets of every
page state, the second window size and saved screenshot folders; rounds of visual comparison and refinement (they
belong to (v), from Hadi's list); page-side unit tests (deferred); the solara-ui check per increment (once, before
Hadi's acceptance of 1a); long record entries (per increment: what was built, the deviations, the commit ids).
`docs/handoffs/plan_T-viz_1a.md` is amended to match (P25, sections 2 and 8).

1a, INCREMENTS (ii) AND (iii), BUILT (ccode, 6 October 2026; plan sections 2 (ii) and (iii); proposals of ccode unless
marked preferred; Hadi's review at the pause after (iii) is open; the session's state file
`docs/handoffs/build_T-viz_1a_state.md`).
- (ii), commits 5f578dc, db28f6f, 0038743, e55c066, 986ded6: the loader's layout and setup parts as functions of
  `mesa_sim/sim_model.py`; dock_loading's `space.note` renamed `notes`; the view of a layout, and of a layout and a
  setup (`LayoutView`, `POST /api/view`, refused while a stepped sim-run is current); the notes in the catalogue; the
  page's full selection, the run options edited by kind, lock and unlock, the address; the env-pane's header by the
  layout's id (P20); `mesa_sim/webui_export.py` and the samples removed (P23).
- (iii), commits 9e1bef1, e42bd2b: the free camera beside the presets; looks by state (the loaded and empty pallet, the
  open gate) with the piece's check of the named states; display places kept, folded over every tick update, which
  `current` now returns; the counter form's top see-through (P21).
- Checks: headless byte-identical after each change of `mesa_sim/` and `domains/` (102 files); every offered triple
  (1020) builds and its view equals its start; the page's offer equals P2's rule on the real catalogue; the suite 436
  passed, 1 failed (`tests/test_tl2_discovery.py` counts 721 kitting scenarios, 722 since Hadi's 0536293; not
  touched); the build and type check; in Chrome: the views, an option set off, the address's three cases, a reload
  giving the same picture as the steps before it, a free angle.
- Deviations: vitest came in (ii), not (iii), for the selection rule and the address (15 page-side tests in all,
  written before the change of mode, kept); the deletion of `webui_export.py` landed in 0038743 with the view's
  commit; a refusal's message is shown in at most three lines (the unknown-scenario message lists every scenario).

1a, HADI'S REVIEW OF INCREMENTS (ii) AND (iii) (Hadi, 6 October 2026, preferred; recorded by ccode the same day). The
plan is amended to match (P25 corrected, P26).
1. The mode of checks, corrected: the message on the mode went further than Hadi meant. Tested: the flow, the functions
   and the logic of the web-ui (the server's rules, which setups and scenarios a layout offers, the lock after the first
   step, the same log pair as headless, display places kept, the messages). Not tested: details of appearance and how
   good the page looks (no screenshot sets, no second window size, no rounds of visual refinement). Page-side tests of
   logic are written, not deferred; logic of (ii) and (iii) without a test gets one now. Unchanged: one look in a real
   browser per new feature; headless byte-identical when simulator code changes; short record entries.
2. The 15 page tests stay.
3. `tests/test_tl2_discovery.py` updated for scenario_s31_01 (722 scenarios, setups to env_setup_31; 0edd3dc).
4. A choice that cannot be built keeps the env-pane's last picture, the controls disabled, the error in at most three
   lines: kept.
5. The address carries every run option: kept.
6. The see-through table top keeps its opacity (0.4) for now.
7. dock_loading's four layout notes rewritten, shorter, the purpose first, every fact kept (cchat's assumption, not
   confirmed by Hadi: these four only; whether other layouts' notes are rewritten is open). Headless byte-identical.

1a, INCREMENT (iv), BUILT (ccode, 6 October 2026; plan section 2 (iv) without the close; proposals of ccode; Hadi's
review open). Before it, the review's items: 0edd3dc (the discovery test), 1fef671 (dock_loading's notes, headless
byte-identical), 7e9716e (the page logic of (ii) and (iii) tested: `src/opening.ts`, `withOption`, `foldBook`, moved out
of `App.tsx` unchanged).
- Panel 4a (8f05287): per human the action in hand with its progress and its task, the stack with the task below the
  top suspended, the last five switches of the stack and resumptions with their ticks and, for a switch, the task it
  suspended and where it cut it; 340 px wide (P18). Test 2 (795fc34): dock_loading's content under a new name, no
  appearance file, listed with the default appearance, built and stepped through the server.
- Checks: the suite 438 passed; vitest 27 passed; the build and type check; one look in Chrome at 1440 wide (kitting
  scenario_s02_02, dock_loading scenario_s06_09, the new domain drawn from the defaults, no console error).
- Deviations: an action is written with all its bindings' values, the agent included (`move_to(human_0, pallet_0)`), as
  the logs write it, not the plan's example without the agent; test 2's screenshot is a look, not a saved file (P25).

1a, THE PANELS' CONTENT (Hadi, 6 October 2026, preferred; after trying increment (iv) and discussing the panels with
cchat; recorded by ccode the same day). The plan is amended to match (P27 to P33).
1. The roles of the three panels: the left panel (4a) shows the human and the world's context as they are at the tick;
   the right panel (4b, stage 1b) shows the robot in two parts, its body (its action, what it carries) and its mind; the
   bottom panel (4c, stage 1c) shows both over time.
2. Panel 4a's content: (A) the human now and (B) the recent switches of the stack and resumptions, as built in (iv);
   (C) the human's script; (D) the world's context now. C and D are built in (iv)'s second part.
3. Not in panel 4a: the distance between robot and human (panel 4c, stage 1c). The timeline facts also get their own
   subplot in panel 4c.
4. The tag per task ("in accord", "not in accord", "no fact"; THE TAG PER TASK, under "T-F part 1") is wanted in panel
   4a. Open: Hadi and cchat first settle which definition the panel shows. Nothing is built for it.
5. Task names in the panel show values only, as actions do: `deliver_item(item_2, kitting_table_0)`.
6. Panel 4a's reference cases (the scenarios of the increment (iv) report): a task in progress, kitting
   scenario_s02_02 from its start; an interruption after an action, scenario_s02_02 at tick 33 (a coffee break after
   `pick_up`); an interruption inside an action, kitting scenario_s09_13 at tick 46 and dock_loading scenario_s06_09
   (env_layout_04) at tick 14; a resumption, scenario_s02_02 at tick 77, scenario_s06_09 at tick 68, and dock_loading
   scenario_s11_03 (env_layout_05), an office break at 28 resumed at 108.
7. The notes of every layout of both domains are rewritten to be readable for a screen-user (supersedes the review of
   (ii) and (iii), item 7's assumption "these four only").

1a, THE TAG PER TASK IN PANEL 4a (Hadi, 6 October 2026, preferred). Panel 4a shows the tag per task as the records
define it (THE TAG PER TASK, under "T-F part 1"): "in accord", "not in accord", "no fact", on every task the human
performs. Reason: the page and the analyses then use one meaning. The provisional rule of T-K step 6 is followed
(TODO-185: a fact that lowers a task gives no tag), provisional until Hadi confirms or changes it. Increment (iv) is
accepted in advance; its open details are decided by ccode (below). The plan's P34.

1a, INCREMENT (iv), SECOND PART, BUILT (ccode, 6 October 2026). Increment (iv) is complete.
- Records: 512a167 (the panels' content, P27 to P33). Outside the web-ui: 33c9394 (the discovery test pins no
  inventory and runs alone; TODO-126 closed); a48b1b3 (every layout's notes rewritten, headless byte-identical).
- The tag's one definition: e50cb81, `world/tag.py` (the tag, the recency facts, the stretches), read by
  `analysis/instruments/mpb/tag.py` and by Mesa's piece. Unchanged analyses: 120 sampled dock_loading runs equal tk6's
  `tags.csv`, 150 sampled kitting runs (tf1) equal the reader before the move.
- The messages and the piece: fddcf7b (`HumanActivity.stack_entries` and `.tag`; `Left.entry`, `Started.event`,
  `Unfired.position`). Tests: 705653e (the script lines' fixtures of the four reference cases; the tag the page
  receives equals the reader's on four scenarios with a timeline fact, all three values). The page: 3cb88e5 (block C
  the script, block D the world's context, the tag beside the task in progress and on its script line).
- Checks: headless byte-identical (102 files) after each change of `mesa_sim/`, `world/`, `domains/`; the suite 444
  passed; vitest 32 passed; the build and type check; one look in Chrome (kitting scenario_s10_14, dock_loading
  scenario_s03_02 and scenario_s03_04, no console error). The tag is computed under every run option (all on; context
  knowledge, assignment knowledge, intention-aware, human-aware each off: the same tags).
- Decided by ccode: the one definition in `world/tag.py` (a term of the world; `mesa_sim/` may import `world/`, not
  `analysis/`), the reader keeping only its parsing. The tag sent as the top's (`HumanActivity.tag`: the value, its
  stretch's first tick, the raised and lowered tasks); a script line shows the tag its task last had on top.
  Entries and events named in the piece by object identity (a frame's task is its entry's task object; an event's
  trigger and object are the record's); a task entered and left within one tick whose task object belongs to two
  entries gets no entry. A Drop event counts as fired when its entry was abandoned. With a domain that declares no
  context knowledge the tag is none (no domain of today; no run option removes the declaration). The script test's
  fixtures live outside `webui/` (`tests/fixtures/tviz_panel/`, they name a domain's tasks), the truth from the
  executor's own state, ticks with no change dropped. Panel 4a 360 px; its blocks in the order A, C, B, D; a repeatable
  entry shows how often its task was completed. The layout notes keep every measured fact, so the measured rooms' notes
  stay long, their first sentence the purpose; env_layout_02 got its first note; a description copied from another
  room replaced by a reference to it.
- Found for Part 2b: the stale titles are kitting env_layout_01 to _06 ("Kitting Domain Layout 0" to "5", from the old
  ids) and env_layout_30 ("env_layout_18", a copy of env_layout_18); a layout's title is written into no log line (it
  reaches only the web-ui's run description and `scripts/layout_tool.py`).

1a, STAGE 1a CLOSED (Hadi, 6 October 2026, preferred; recorded by ccode the same day; records only, no code changed).
1. Hadi tried increments (i) to (iv) in both domains and accepts stage 1a.
2. Increment (v), polishing, is not done in stage 1a. One polishing round follows after stage 1c, from Hadi's written
   list. Candidates known so far, all open: the seven stale layout titles (kitting env_layout_01 to _06, env_layout_30),
   and showing the title beside the id again once they are correct; the width of panel 4a; the tuning Hadi mentioned
   after increment (i), not yet specified; the see-through table top.
3. The solara-ui is not archived: it stays in the repository as an alternative start, as it is. This replaces the
   preference that it becomes archived when Hadi accepts stage 1a (the handoff's 6.3; the earlier passages carry a
   dated line). The README and the roadmap carry no "archived" line.
4. The roles of the three panels and the content of panel 4a, as recorded (THE PANELS' CONTENT; THE TAG PER TASK IN
   PANEL 4a), are what stage 1b starts from. The right panel shows the robot in two parts, its body and its mind; its
   content is decided with Hadi before stage 1b is planned.
5. The solara-ui's light check (Hadi, 6 October 2026, preferred; it answers the open point of item 3): after a change to
   code the solara-ui uses, check only that it starts and that one sim-run takes a few steps without an error, in one
   domain. No check after a change to the web-ui's page alone, no check of its look, no second domain unless the change
   is specific to that domain. A failed light check is reported, and fixed only when the fix is small; otherwise
   reported, and the work waits. The rule stands in the handoff's "State after stage 1a" and in the plan's section 8.
THE CHECK (ccode, 6 October 2026): `solara run mesa_sim/run_mesa.py` serves in kitting (scenario_s01_01) and
dock_loading (scenario_s03_02), HTTP 200; a sim-run of each, built from the command line's configuration as under
solara, takes three steps without an error.
The state for the next design chat: `docs/handoffs/handoff_T-viz.md`, "State after stage 1a".

1b, THE RIGHT PANEL'S CONTENT AND STAGES 1d AND 1e (Hadi, 6 October 2026, preferred; recorded by ccode the same day,
with the task of stage 1b; records only, no code changed).
1. Panel 4b, the right panel, shows the robot at the tick in five blocks, in this order: (1) Body: the robot's action
   and its progress, what it carries, a hold in progress, its current task. (2) Belief: the robot's belief over the
   tasks the human may be doing. (3) Admission: whether the leading hypothesis passes the gate, or why it is refused.
   (4) Projection: what the robot expects the human to do, and its kind: the plan of the admitted task, the fallback
   projection, or none. (5) Decision: the last decision: its tick, its trigger and cause, the chosen task, the hold.
   Reason: the order is the framework's chain from intention recognition to adaptive planning, and it matches the
   per-run figure Hadi reads (analysis/instruments/irb/plot.py, mpb/decision_panel.py); the panel is that figure at one
   tick. The content of each block is ccode's (`docs/handoffs/plan_T-viz_1b.md`).
2. Two stages are added to stage 1, after 1c; stage 1's order is 1b, 1c, 1d, 1e.
   - 1d: the env-pane draws the movement of the current task of the human and of the robot as wide, semi-transparent
     stripes on the floor (the walk segments). A first try; the form is open.
   - 1e: the env-pane draws the robot's projection of the human (the plan of the admitted task, or the fallback
     projection) in the same way.
   Proposed by cchat, recorded with them: 1d against 1e shows where the robot's expectation differs from what the human
   does; the model holds no path per agent (0.1, fact 3), so the simulator's side derives the segments and the page
   computes none; the human's real movement is a world fact, the robot's plan and its projection belong to the robot's
   section of the messages.
   TODO-197 (whether and which paths the scene shows) is answered by 1d and 1e. Open: whether the polishing round
   comes after 1c or after 1e.

1b, THE RIGHT PANEL, BUILT (ccode, 6 October 2026; `docs/handoffs/plan_T-viz_1b.md`, planned and built in one session
without a pause, as the task asked; Hadi's mode for 1b: web design details are ccode's, recorded as "decided by ccode";
a conceptual reading of the robot's mind that the records do not settle is built as judged closest to the records,
marked "provisional, raised to Hadi" below; nothing marked preferred is Hadi's review yet).
- The model: `RobotAgent.last_decision` (`DecisionTaken`: the tick, the trigger decision, the human projection and the
  meta-planner's result step() already holds), for readers; nothing in the loop reads it (b69d9b6). No change to the
  recognizer, the gate, the projection, the meta-planner or the executor.
- The messages: the run description's and the tick update's `robots` (`RobotDescription`, `RobotTick`: the body, the
  belief, the gate's answer at the tick, the last decision with the projection it rested on), beside `world`, each
  with an empty default; every value typed (enums for the trigger, the cause, the gate's answer, adequacy, warrant,
  rank, level, lifecycle, finding, the fallback's form, the change of task).
- Mesa's piece reads the robot after each step: the belief (`RobotAgent.belief`), the gate's answer from its one home
  (`MetaPlanner._clears_gate`, as the test-beds ask it), after `none(no_human)` asked first; the last decision; the
  executor's cursor, progress and hold; the memory's recency facts. The trigger's reason, a string in shared/types.py,
  is translated by a closed table; an unknown one stops the piece.
- The page: panel 4b (`src/frame/RobotPanel.tsx`, its reading `src/frame/robot.ts`) in the rail's place.
- Checks: headless byte-identical after the model change (the four maintained sets and dock_loading's three runs, 102
  files); `tests/test_tviz_robot.py`, the values the panel receives equal the run log's at every tick on kitting
  scenario_s05_02 and dock_loading scenario_s07_07 (each an admission, refusals, fallback projections, holds, a
  retraction), kitting scenario_s10_14 (a timeline fact, a raised level), scenario_s05_02 intention-unaware and
  scenario_s07_07 human-unaware: the recognizer's lines, the gate derived from the logged values in the gate's order,
  every decision's trigger, cause, admission, projection's kind, winner, queue and hold, a fallback's end where
  projection_expired fires, `[meta-b3]`'s T_h, the hold against the `[hold]` lines, the body against the step lines;
  vitest 38 (6 new); the page's build and type check; the suite; one look in Chrome at 1440 wide (env-pane 684 px,
  no console error); the solara-ui's light check (it serves; a sim-run steps).
DECIDED BY CCODE (web design and naming):
- Panel 4b is 340 px wide (260 px under 1200 px); panel 4a keeps 360 px; the rail and its styles are gone.
- The robot's id heads the panel with the robot's colour; the five blocks under the headings Body, Belief, Admission,
  Projection, Decision, in Hadi's order.
- Body: the task, the action at the plan's cursor with a progress bar ("not begun" at 0 of 0), then "this tick" (the
  microaction), "carries" (from the world's `carried`), "hold" (stood of planned ticks, the deciding tick).
- Belief: one row per live hypothesis, highest belief first, ties by key; a bar with θ as a thin mark; the value to 3
  decimals; under it adequacy, warrant ("warranted", "no warrant"), "outranked" only when outranked, S and the prior to 3
  decimals; the leader in the robot's colour; then the levels, the memory's recent tasks, the count of hypotheses not
  live and the assigned tasks it is told.
- A hypothesis is written by its values, as panel 4a writes a task (`deliver_item(item_5)`); its key travels as data.
- Admission: "passes" or "refused" with a short phrase, the leader and its belief, the log's code small beside it; a
  note that the gate is asked at a decision and which hypothesis the last decision rests on.
- Projection: a pill "admitted" or "fallback"; an admitted projection lists its plan's actions; a fallback reads "the
  human stays where it was seen" or "walks straight on", for its span, to its end tick; ticks past the projection's end
  say it ran out; a fractional tick to one decimal.
- Decision: the last decision's tick, trigger in words and cause, the log's codes small; task (starts, continues,
  switches to, all its tasks are complete), hold, queue, admission; then the five before it, newest first.
- Conditions: a grey note under the robot's id for intention-unaware and human-unaware; a block that does not apply
  says "does not apply".
- The message fields for the gate's answer are named `gate_answer`, and the scan for domain words (tests/
  test_tviz_messages.py) admits "gate" as a framework term (the confidence gate; also dock_loading's object type) in a
  name or in prose, still refusing it as a string literal on its own, the form a dependence on the object type takes.
- The tick update grows from about 1.3 KB to about 3.5 KB (kitting scenario_s01_06): noted, with open item 10.
PROVISIONAL, RAISED TO HADI (conceptual readings the records do not settle; each built as judged closest to them):
ANSWERED (Hadi, 7 October 2026, preferred; 1b, HADI'S REVIEW, below): 1, 3, 4 and 5 kept, no longer provisional; 2
changed.
1. The belief block shows the belief over the live hypotheses (`BeliefState.belief`, the value the gate compares with
   θ, AM42), not the reported distribution with the floor and the pins (`distribution`, the `[IR-dist]` line).
   Example: kitting scenario_s05_02, tick 71: deliver_item(item_5) 0.999 shown, 0.995 in `[IR-dist]`.
2. The admission block states the gate's answer at every tick, though the gate is asked only at a decision and on the
   entering side of recognition_changed; it can read "refused" while the decision still rests on an admitted hypothesis
   (retention by identity, D2). Example: kitting scenario_s05_02, tick 24: refused, the leader outranked, while the
   decision of tick 0 rests on deliver_item(item_5).
3. "The projection in use" is the last decision's projection, kept until the next decision, also past its end (an
   admitted projection past T_h, P3) and after the robot's pool is empty (no trigger is evaluated then). Example:
   kitting scenario_s01_06, tick 119: the admitted projection of tick 84 ended at 118.6; the panel shows it, "ran out".
4. The body's action is the action at the plan's cursor; on an acknowledgement tick the executor's `current_action`
   (the step line's) still names the action just completed. Example: kitting scenario_s05_02, tick 38: the step line
   says move_to, the panel pick_up, not begun.
   THE CONVENTION (Hadi, 7 October 2026, preferred): the body shows the action at the plan's cursor; on the tick
   between two actions it may name the next action one tick before the step line does.
5. The fallback's form (standing, moving) is read from the projection's segment (it moves or not), not from the
   perceived displacement; a moving human whose ray is blocked at once would read "stays where it was seen". No instance
   in kitting scenario_s05_02, s01_06, s04_01 or dock_loading scenario_s07_07, s03_02.

1b, HADI'S REVIEW (Hadi, 7 October 2026, preferred; recorded by ccode the same day, then built).
1. The check for domain words names one exception and only that one: "gate", the framework's own term for the
   admission gate, which collides with dock_loading's object type `gate`; a string literal that is the word alone is
   still refused. Not a general loosening (tests/test_tviz_messages.py, `GATE`).
2. The belief block keeps the belief over the live hypotheses, the value the gate compares with θ (point 1 kept).
3. The admission block shows two named parts, the first first: (a) what the robot holds since its last decision, with
   that decision's tick ("held"); (b) what the gate would answer if asked at this tick ("gate now"). Reason: the robot
   asks the gate only when it decides and keeps what it admitted in between; a single "refused" beside a decision that
   rests on an admitted task reads as a fault. These are the two readings of "admitted" the analyses already report
   (point 2 changed).
4. The projection after its end: kept (point 3). The robot's action on the tick between two actions: a difference of
   one tick is acceptable, kept as built, the convention stated under point 4 above. The fallback's form read from the
   projection: kept (point 5).
5. Three requirements for the panel: (i) not crowded: no full sentences, short labels and values, read at a glance
   during play; (ii) what intention recognition provides is clear and explicit: the panel shows visibly which part is
   the recognizer's output and which is what the planner does with it (admission, projection, decision), the
   recognizer's part naming its outputs one by one; reason: the framework's claim is the step from intention
   recognition to adaptive planning, and an audience must see where one ends and the other begins; (iii) the live
   hypotheses as a small, simple bar chart, one bar per live hypothesis with its value at the tick and the threshold
   marked, each bar keeping its position from tick to tick; reason: it is the snapshot at one tick of what panel 4c
   (stage 1c) shows over time.
BUILT (ccode, 7 October 2026; commits below):
- Panel 4b in three parts: Body; "Intention recognition, the recognizer's outputs" (leader, finding, lifecycle, an
  episode boundary; the belief chart with, per hypothesis, hypothesis adequacy, observation warrant, evidence rank, S
  and, with context knowledge on, the prior; the levels); "Planning, what the meta-planner does with them" (admission:
  held, gate now; projection; decision). The recognizer's outputs are the fields of `BeliefState` (its docstring:
  the belief, the adequacy finding and the lifecycle, then G1's adequacy, AD's warrant, AM76's rank, L's boundary,
  T-K's prior and levels). The gate, the projection (it only looks the admitted hypothesis up in the recognizer,
  `get_hypothesis`) and the decision are the meta-planner's.
- Checks: tests/test_tviz_robot.py also tests "held" at every tick against the decision record the log's last
  [meta-proj] states (the gate now was tested already); the suite 449 passed; vitest 39; the build and type check; one
  look in Chrome at 1440 wide (kitting scenario_s05_02 tick 24, scenario_s10_14 tick 59, scenario_s05_02
  intention-unaware, dock_loading scenario_s07_07 tick 92). No simulator code changed.
DECIDED BY CCODE:
- The two parts framed side by side in colour: the recognizer's in the robot's light tone, the planning's in the
  robot's colour, each with its title and a short subtitle.
- Labels: "held … · since N" or "nothing admitted · since N"; "gate now" with a short label and the log's code small;
  the gate's answers "passes", "below θ", "leader not observed", "leader inadequate", "leader unwarranted", "leader
  outranked", "intention off", "no human"; triggers and causes by their glossary words; a decision's task "starts",
  "continues", "switches to", "all done"; "–" for nothing; a part that does not apply says "off"; the condition as a
  chip beside the robot's id.
- The chart: horizontal bars, one row per hypothesis that has been live at some tick so far, in the order first live
  (those first live on one tick by key); a row whose hypothesis is not live at the tick stays, greyed, with no bar; the
  label on its own line, under it the bar (θ a thin mark), the value to 2 decimals, then the columns adeq (✓ ✗ ·), warr
  (✓ ·), rank (↓ when outranked), S and prior to 2 decimals; column names spelled out on hover; the leader in the
  robot's colour.
- The memory's recency facts are shown in the recognition part as "memory … (input)": the memory of observed
  completions is a component of its own (AM30) that hands the recognizer its recency facts, an input, not an output.
- The last decision and the three before it (five before the review).

1c, THE BOTTOM PANEL (Hadi, 7 October 2026, preferred; recorded by ccode the same day, with the task of stage 1c,
before any code of it).
1. Panel 4c, the bottom panel, shows five lanes on one tick axis, in this order: (1) the human's task: a band per task
   the human performs (the truth), with the tag per task (in accord, not in accord, no fact) where it applies; (2) the
   robot's belief: one line per hypothesis, the threshold, and a marked span where the robot holds an admitted task;
   (3) context: a band per timeline fact while it holds, hidden when the sim-run has none; (4) the robot's task: a band
   per task, with holds marked and a mark at each decision; (5) distance: the distance between robot and human, the
   minimum separation, and the ticks below it marked. Reason: a viewer of a demonstration asks what the human was
   really doing, what the robot believed and when it became sure, and what the robot did about it and whether it was
   safe.
2. Left out for now: the tail probability S, the finding, the warrant rows, the gate's answer per tick. Reason: they
   serve the developer, and the per-run figures of the analyses keep them.
3. The plots are drawn from the tick updates the page already holds and grow by one tick per step. Nothing is read
   from logs. A reload restores them.
4. One colour per task across the whole page: the same task has the same colour in lanes 1 and 2, in the belief chart
   of the right panel and in the script list of the left panel. Reason: the viewer sees without reading whether the
   highest belief line has the colour of the truth band.
5. A vertical line marks the current tick through all lanes.
6. A click on the plot shows an earlier tick: the click pauses play, and the scene and both side panels show the
   clicked tick; the page states clearly that it shows the past (for example "viewing tick 24, the sim-run is at tick
   211"); play or step returns to the latest tick and continues; the sim-run never goes back and its log is not
   affected. This takes "moving back along the ticks" out of TODO-189's items without a stage, for display only.
7. Proposed by cchat, ccode's to decide as design: the tick axis extends in fixed portions and is not rescaled at every
   tick; the distance is sent by the simulator's side as the value the run log prints, and the page computes none.
The mode of 1c (as for 1b): a short plan (`docs/handoffs/plan_T-viz_1c.md`), then the build without a pause; web
design details are ccode's, recorded as "decided by ccode"; a conceptual reading of the core algorithm the records do
not settle is built as judged closest to them and marked "provisional, raised to Hadi".

1c, THE BOTTOM PANEL, BUILT (ccode, 7 October 2026; `docs/handoffs/plan_T-viz_1c.md`, planned and built in one session
without a pause, as the task asked; Hadi's review open).
- The messages (a859c55): `WorldTick.separations`, per robot and human the two values the `[sep]` line prints
  (`SimRun.separation` keeps them; the piece reads them, nothing is computed twice) and `below`, the minimum under the
  robot's min_separation as the analyses count it; `TaskRef.identity`, the task's identity by task equality (its schema
  and goal bindings, `goal_bindings`), the form of a hypothesis key. No change to the recognizer, the gate, the
  projection, the meta-planner or the executor.
- The page (07bf71f): panel 4c (`src/plots/PlotPanel.tsx`, its reading `src/plots/lanes.ts`), the past view
  (`src/plots/past.ts`, App.tsx, the control bar), one colour per task (`src/frame/colours.ts`) in the lanes, the right
  panel's belief chart and the left panel's script, stack and action in hand.
- Checks (56c7e2c): headless byte-identical, B1 equals B0 on 102 files (the four maintained sets, which equal the
  baselines on disk, and dock_loading's scenario_s03_02, s05_02, s07_02); `tests/test_tviz_plots.py`: the distance and
  the identity the page receives equal the log and task equality, and the page's own lane reading, run under vitest on
  each sim-run's tick updates, equals the run log's values at every tick (kitting scenario_s05_02, scenario_s10_14,
  scenario_s05_02 intention-unaware; dock_loading scenario_s07_07, scenario_s07_07 human-unaware), the lanes folded one
  tick at a time equal the lanes folded at once, and the view of tick k equals what the page held at tick k (the tick
  updates and the place book); a wrong log value makes it fail (tried). The suite 450 passed; vitest 44 (5 more under
  the Python test); the page's build and type check; one look in Chrome at 1440 wide (kitting scenario_s05_02 and
  scenario_s10_14, dock_loading scenario_s07_07 human-unaware): a click in the past sends no request and leaves the log
  pair's checksums unchanged, a step returns to the latest tick, no console error; play at 5 ticks per second with 2000
  ticks held kept 5.2 ticks per second with no long task on the main thread (headless Chrome, software rendering); the
  solara-ui's light check (it serves; a sim-run steps).
- The per-hypothesis belief over the live hypotheses is not in the run log (only the leader's confidence, the live set
  and `[IR-dist]`, the reported distribution with the floor and the pins): the test compares what the log holds (the
  live set, the leader, its confidence, the values summing to 1).
DECIDED BY CCODE:
- What draws the plots: the page's own canvas drawing, no plotting library; uPlot, planned for 1c in stage 0, is not
  taken. Reason: the lanes are mostly bands and marks on one shared axis with one hairline, one click and the past view
  across all five; one canvas does that without syncing five charts, and draws with the theme's colours, line weights,
  opacities and type (`src/theme.ts`: `task`, `taskOther`, `past`, `below`, `separation`, `line.plot*`,
  `opacity.plot*`). Nothing is rendered by Python; no Plotly (Hadi's double check, 7 October 2026).
- Lane order and content as Hadi's items 1 and 2; lane titles "human's task", "robot's belief", "context", "robot's
  task", "distance" in a 156 px gutter with the agent's or the fact's id; the panel's height is its lanes' (236 px with
  one human, one robot and no timeline fact).
- Lane 1: a band per stretch of the stack's top (a new band where the tag's stretch begins anew), the task's text
  inside where it fits; the tag as a 3 px strip under the band in the tag's colour. Lane 2: lines in the task's colour,
  a hypothesis that has led at some tick 2 px, the others 1 px at 0.45; θ dashed; the held admission as a 3 px strip
  along the lane's top in the held hypothesis's colour; the latest leader named at its line's end. Lane 3: a grey band
  per fact with its name. Lane 4: a band per task, a hold (`body.hold`, panel 4b's) as a dark 4 px strip under it, a
  ▾ at each decision. Lane 5: the continuous minimum over the tick, 0 to 4 × min_separation (above drawn at the top),
  min_separation dashed, the ticks below shaded.
- The axis from 0 to the next multiple of 100 ticks past the latest (cchat's fixed portions, taken). The latest tick a
  1 px line through all lanes; the viewed tick a 2 px line in the past colour, "viewing k" on the axis. A hairline and a
  tooltip (tick, the human's task and tag, the top three hypotheses, held, context, the robot's task and hold, a
  decision's trigger and cause, the distance) follow the pointer.
- The colours: fixed from the run description, the human's script first (entries in written order with the tasks
  their events start, the repeatable entries, the closing part), then the robot's assigned tasks, then the hypotheses
  in the recognizer's order; ten hues (validated with the dataviz validator: adjacent CVD ΔE 6.4, legal with the labels
  and tooltips), every further task one neutral grey. A robot's own task has the colour of that task wherever it shows,
  also where a hypothesis names the same task (one colour per task, read literally).
- The past view: a click on the latest tick returns to it; the control bar shows "viewing tick k · sim-run at tick n"
  with a "latest" button in place of its other notes; the scene does not glide in the past view; reset or a new choice
  clears it.
- Conditions: lane 2 a short row "off · intention-unaware" or "off · human-unaware"; lane 5's line labelled "min sep 50 ·
  not kept" when human-unaware.
PROVISIONAL, RAISED TO HADI (conceptual readings the records do not settle; each built as judged closest to them):
1. Lane 5 draws the continuous minimum over the tick (`[sep]`'s `min`), not the distance at the tick's end (`dist`),
   and marks a tick below min_separation by that minimum, as the analyses' figures and counts do; the tooltip gives
   both. Example: kitting scenario_s05_02, tick 30: min 31.62 (drawn, below), dist 42.43.
2. In a human-unaware sim-run lane 5 still draws min_separation, labelled "not kept": the human-unaware robot neither
   plans around the human nor stops for it (T-F part 1: the condition covers the mind and the separation stop), so the
   line is a reference, not the robot's. Example: dock_loading scenario_s07_07 human-unaware, tick 60.
FOUND (for the polishing round): with the note "all agents have finished" the control bar's tick text is cut at four
digits at 1440 wide (kitting scenario_s05_02 past tick 2000); a task's text in a light band (pink, aqua) is white on a
light hue.

1c, HADI'S REVIEW AND TWO VERSIONS OF THE BOTTOM PANEL (Hadi, 7 October 2026, preferred; recorded by ccode the same
day, before any code of it).
1. Point 1 of 1c's provisional readings (lane 5 shows the smallest distance within the tick) stays as built, with no
   extra label. No longer provisional.
2. Point 2 (the human-unaware sim-run): the dotted minimum separation line stays; the label "not kept" is removed. No
   longer provisional.
3. A principle from Hadi: the web-ui is for users, not a tool for the developer to debug the algorithms. Few labels and
   explanations; more would crowd it.
4. Hadi finds the bottom panel as built not modern; he asked twice why no JavaScript chart library is used. He likes the
   light colouring and the soft boxes of the right panel as it is now (the tinted blocks for intention recognition and
   planning). The ten strong task colours and the flat default look of the panel are what he objects to.
5. Hadi chooses between two versions of the bottom panel from screenshots: version A, ccode's own drawing restyled;
   version B, drawn with a JavaScript chart library of ccode's choice. Both show the same five lanes for the same
   sim-run, with the click on an earlier tick working; modern, minimal, abstract and still elegant; few colours; few
   labels; in the page's theme, so that the panel belongs to the scene and to the right panel's tinted boxes (Hadi's
   taste: the handoff, section 10). Screenshots at 1920 x 1080, the size of Hadi's projector; the page's size and
   layout unchanged; the screenshot folder untracked.
6. Not in this step: the left panel, the right panel, the scene, the selection, the page's size, the messages, the
   lanes' content. A change of the tasks' colours applies to the bottom panel only for now; the side panels follow after
   Hadi's choice.

1c, THE TWO VERSIONS OF THE BOTTOM PANEL, BUILT (ccode, 7 October 2026; 19d62e1; for Hadi's choice, open).
- Version A: the page's own drawing on a canvas (`src/plots/drawA.ts`), restyled: each lane a tinted box as the right
  panel's blocks (the human's warm tint, the recognition tint, the planning tone, neutral), small-capital titles, a faint
  dashed grid, the tasks as soft tints of dusty colours, lines only for hypotheses that have led, a gradient under the
  leading belief and under the distance, a dot at the shown tick and a large number at the box's right.
- Version B: the look of the ReUI chart components (reui.io, MIT) in a light scheme, on their chart base, Recharts 3.10.1
  (MIT), with ReUI's styling written in the page's CSS (`src/plots/PlotsB.tsx`): each lane a white card with a fine ring
  and a faint shadow, a header column in the matching tint with the title, a large number (the leading belief, the
  present distance), a badge and a muted line; areas with a gradient fading under the line; a faint dashed horizontal
  grid; no axes; the task lanes as rounded shapes in soft tints on the same axis; a hold as ReUI's stripe texture.
- Shared (`src/plots/look.ts`): one geometry per version's proportions, one click mapping (`tickOf`, tested for both), the
  tooltip (a header line, rows with a colour square, a muted label and a value), the soft task colours
  (`theme.taskSoft`, the bottom panel only until Hadi chooses). The label "not kept" is gone (HADI'S REVIEW, item 2).
- The switch: a small A/B control at the panel's foot, remembered in the browser. Screenshots at 1920 x 1080, kitting
  scenario_s05_02 at tick 120 (a hold, ticks below min_separation): `docs/handoffs/tviz_1c/`, untracked (.gitignore).
- The libraries considered for B (Hadi's three, 7 October 2026): FusionCharts is commercial and watermarks its free
  version, and its plain style reads as a paper figure (Hadi): out. ReUI's components are MIT but are Tailwind and shadcn
  code, which the page does not use: their look is rebuilt on their base instead. Recharts in its usual look: not
  delivered (Hadi). Apache ECharts and visx were started and removed on Hadi's word; Motion, ReUI's animation library,
  was tried and removed: in a 2000-tick sim-run it lengthened every step (the longest task 192 ms against 77 ms), and
  CSS transitions give the shapes' growth.
- Found and avoided: Recharts' own animation and an SVG glow filter on its areas each drew a stale copy of a curve across
  a gap of the line in Chrome; the line grows by a short reveal of the chart's right edge, and no line glows (Hadi: no
  glow on lines).
- Checks: vitest 46 (the click mapping for both versions); the lanes against the run log (tests/test_tviz_plots.py,
  unchanged lanes); the suite 450 passed; the page's build and type check; the click on an earlier tick in both versions
  in Chrome (no request sent); 2000 ticks held, play at 5 ticks per second: A 5.1 ticks per second, no long task; B 5.2
  ticks per second, four tasks over 50 ms (the longest 80 ms; B draws its lines through at most one point per 6 px).
  No simulator code changed.
DECIDED BY CCODE: the soft palette (eight dusty tones, theme.taskSoft); the gradient only under the leader at the shown
tick (two fills mixed muddily); the large numbers' tick is the shown one (the viewed tick in the past view).
