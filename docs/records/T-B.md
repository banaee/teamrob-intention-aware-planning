# Record of planning and building: T-B, B3.B on two tables

Moved verbatim from `docs/design_decisions.md` on 2 October 2026 (Hadi's ruling of that day: one record file per task;
the conceptual design stays in design_decisions.md). Each block is headed by the title of the entry it comes from
and its id; in design_decisions.md an index line with the same id stands where the block was.

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
