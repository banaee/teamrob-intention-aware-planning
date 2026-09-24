# Glossary

One term, one meaning — in the documents, in the code comments, and in the task prompts. When a
term below appears in prose it carries the meaning given here and no other. Identifiers are not
bound by it: a field or function may keep a name this glossary uses differently (`task_queue`,
`ProjectedPlan.entries`), and the glossary says so where it matters.

Every entry points at where the thing itself is defined. The pointer is the source of truth; this
file is the index. Where a pointer is a section of `shared/io_contracts.md` or a titled entry of
`docs/design_decisions.md`, the title is given rather than a line number, because line numbers rot.

Written after the B3.B design discussion, in which "task", "entry", "sequence", "ordering" and
"trajectory" were used as if they were one thing, and "walk" named both an agent's movement and a
loop in `realize()`.

---

## 1. Selection: what the meta-planner chooses between

**task** — one `TaskInstance` of the robot: a `TaskSchema` plus its bindings. Never an ordering,
never an entry, never a plan.
→ `shared/types.py`, `TaskInstance`; `shared/io_contracts.md` §1.6.

**pool** — the robot's remaining tasks at the trigger: `current_task` (if any) plus the queue,
minus every task whose terminal condition already holds in the `WorldState`, whoever made it hold.
The pool is not a candidate set; nothing competes at that level.
→ `shared/meta_planner.py`, `update()` block 0 and "TASK POOL vs. CANDIDATES";
`shared/io_contracts.md` §2.2.

**ordering** — one permutation of the pool. Under `full_reorder` one candidate is one ordering.
Say "ordering", not "sequence" and not "queue", whenever a permutation of the pool is meant.
→ `docs/design_decisions.md`, DESIGN-16 ("Single-task selection (receding horizon), not queue-wide
reordering") and its revision, "B3.B (`full_reorder`) is lookahead for the choice of the next task,
built next".
"Sequence" is not banned outright — it keeps its own two established uses, a **decision sequence**
(a run's decisions over time, `step:trigger:winner`, the key the analysis scripts diff on) and a
**grounded action sequence** (an `AbstractPlan`'s actions). Neither is a permutation of the pool.

**candidate** — the unit the argmin ranges over. An individual task under `single_task`; one
ordering under `full_reorder`. Candidates exist only inside B3; forming them from the pool is B3's
private business.
→ `docs/design_decisions.md`, DESIGN-16, "Terminology, fixed"; `shared/io_contracts.md` §2.2,
"Strategy (DESIGN-16)".
COLLISION, not resolved: the older TODO entries use "candidate" as the ordinary adjective — "candidate
fix", "candidate formulas", "candidate remedy". That is the English word, not the term.

**head** — the first task of an ordering. Under `full_reorder` the head of the argmin ordering
becomes `current_task`; that choice is what the ordering is priced for.

**tail** — the tasks of an ordering after the head. Lookahead only: it carries no order commitment
and is re-priced at the next robot trigger.
→ `docs/design_decisions.md`, "B3.B (`full_reorder`) is lookahead for the choice of the next task,
built next", point 4.

**queue** — the pool without the current task, as carried in `UpdateResult.queue`. It carries no
commitment under either strategy, and is re-decided at the next trigger. Under `full_reorder`
`UpdateResult.queue` lists the winning ordering's tail, as information only; the meta-planner's internal
queue stays in pool order, so the winning ordering is not stored.
→ `shared/types.py`, `UpdateResult`; `shared/meta_planner.py`, `update()` ("queue invariant").
NOTE: the field `ProjectedPlan.task_queue` is a different thing — the tasks of ONE projected
ordering, in the ordering's order. The identifier is not renamed.

**single_task** / **full_reorder** — B3's two strategies (B3.A and B3.B), selected by the run option
`--strategy`. `single_task` is the default. Under `full_reorder` (T-B2b, T-B2c) an ordering is realized
against the one human projection, one minimal-shift search per entry, and costs the sum of its entries' T_r
plus the cumulative shift of its last entry; the hold that goes out is the hold before the first entry,
which is the head's hold realized alone.
→ `shared/meta_planner.py`, module docstring, STRATEGY, and `_replan_orderings()`;
`docs/design_decisions.md`, DESIGN-16, "B3.B on plain cost: the internal queue stays in pool order" and
"One hold per entry".

**successor state** — the hypothetical `WorldState` entry k+1 of an ordering is decomposed against: the
previous one as entry k's action schemas declare they leave it (`ActionSchema.retracts`, `effects`,
`moved_object_key` / `moved_to_key`), with the agent where entry k's last segment ends. Built and dropped
inside one `Projector.project()` call; the live `WorldState` is never written.
The same derivation advances the human script's symbolic state at load (sequential expansion, T-C2b, §6).
→ `shared/projection.py`, `successor_state()`; `docs/design_decisions.md`, "The successor state is
derived from what the action schemas declare: a delete list and a declared relocation".

**B1 / B2 / B3** — the blocks of `MetaPlanner.update()`: B1 the human projection, B2 the mid-task
commitment gate (`b2a` built, `b2b` a stub), B3 selection on realized cost.
→ `shared/meta_planner.py`, module docstring, "BLOCK STRUCTURE OF update()".

---

## 2. Projection: what a plan looks like before the human is considered

**projection** — turning a task, or an ordering, plus a `WorldState` into a `ProjectedPlan`: where
the agent will be, and when. Agent-agnostic: the same call projects a robot candidate and the
human's predicted task.
→ `shared/projection.py`, `Projector`.

**entry** — one task's part of a `ProjectedPlan` (`ProjectedPlanEntry`). An ordering of n tasks is
projected to ONE `ProjectedPlan` with n entries, in the ordering's order. An entry is not a task and
not a plan. (Under `single_task` a `ProjectedPlan` always holds exactly one entry.)
→ `shared/types.py`, `ProjectedPlanEntry`; `shared/io_contracts.md` §1.7.
COLLISION, not resolved: "entry" is also the ordinary word for a titled section of
`docs/design_decisions.md` or `docs/TODOS_AND_DEFERRED.md` ("the B3.B entry"), and for an element of
a dict or a JSON list. Those are the English word; only the plan sense is a term. Where both could be
read, write "the design entry" or "the plan's entry".

**segment** — one `Segment` inside an entry: a straight-line motion, or a stationary stretch,
between two steps. An entry has several segments — one per action, plus the completion latencies.
Do not call a segment a "stretch of evidence"; that is the recognizer's.
→ `shared/types.py`, `Segment`; `shared/io_contracts.md` §1.7.
IN THE RECORD: scenario_40's human script was described as four numbered "segments" (1, 2, 3a, 3b,
4). That is a SCRIPT PART, not a `Segment`. "Segment 3a" in `docs/design_decisions.md`,
`docs/TODOS_AND_DEFERRED.md` and the I4 / F47 reports means script part 3a. The living files
(`domains/kitting/env_layout4.json`, `domains/kitting/scenarios.py`,
`docs/recognizer_handback.md`) say "script part"; the record is untouched.

**walk** — an agent's movement, and nothing else: a "fetch walk", a "carry walk", "the human's walk
to the coffee machine". It is NEVER used for a loop, a search, or an iteration in the code. Where
prose needs to say that an algorithm goes through a list, it says so literally, or names the search
(see **minimal-shift search**).

**T_r** — a projected plan's duration: the span of its segments, in fractional steps. Execution
quantises per walk (ceil per walk) and that is deliberately not compensated, so T_r is not an
integer and is not `ProjectedPlan.total_estimated_cost`.
→ `shared/io_contracts.md` §1.11, `RealizedPlan.projected_duration`; `docs/design_decisions.md`,
"Realization as built".

**human projection** — the human's `ProjectedPlan`: the one task the meta-planner admitted for the
observed human at this trigger, projected as a robot candidate is, with the human body's own per-task
completion tick (0 since T-C2b: its executor is action-level). It ends at **T_h**.
Admission is logged as `[meta-proj]`; there is at most one, and there may be none.
See TODO-97 (24 Sept 2026): belief-aware planning, one realization against the hypotheses covering 1 − ε of the mass, recorded for after the T-D recognizer pass, not decided.
→ `shared/meta_planner.py`, `update_human_projection()`; `shared/io_contracts.md` §2.2.

**T_h** — the end of the human projection: its last segment's end step. Nothing past T_h is
assessed or charged.
→ `shared/io_contracts.md` §1.11, `RealizedPlan.horizon`.

---

## 3. Realization: what a plan costs once the human is in it

**realization** — what the segments of a `ProjectedPlan` actually become, given the human. It
computes the hold the robot must take to keep `min_separation` from the human projection, and the
realized duration T_r + δ is the candidate's cost. Conflict becomes cost by construction; there is
no conflict weight and no exclusion threshold. Since F1 realization is TOTAL: every plan realizes
and every candidate has a cost.
→ `shared/realization.py`, `realize()`; `shared/io_contracts.md` §2.2c; `docs/design_decisions.md`,
"The robot can wait".

**shift** — a number of ticks added to the start step and the end step of a robot segment. The same
path, occupying a later interval.
→ `shared/trajectory_algorithms.py`, `shift_violation_interval()`.

**violating shift interval** — for ONE robot segment and ONE human segment, the set of shifts under
which the delayed robot segment comes within `min_separation` of the human segment without the
distance increasing. One open interval, or none. Computed in closed form by
`shift_violation_interval` — exact, no sampling in time and none in the shift. A stationary robot
segment has none: a standing robot never violates (F1).
→ `shared/trajectory_algorithms.py`, `shift_violation_interval()`; `shared/io_contracts.md` §2.2b.

**conflict** — an entry has a conflict when the shift it INHERITS — 0 for the first entry, the
cumulative shift of the previous entry otherwise — lies inside one of its violating shift intervals.
"Its" intervals are those of its own segments against the human projection's segments. Conflict is
not a separate cost term: it becomes cost because clearing it takes ticks. With one entry the
inherited shift is 0, so the entry has a conflict exactly when δ > 0 — that is the check `realize()`
performs today.
→ `shared/realization.py`, `realize()`; `docs/design_decisions.md`, "The robot can wait".

**cumulative shift of entry k** — the number of ticks by which entry k starts later than projected: the
result of entry k's own minimal-shift search. Never smaller than entry k−1's.
→ `shared/types.py`, `RealizedPlan.cumulative_shifts`; `shared/realization.py`, `realize()`.

**hold before entry k** — the cumulative shift of entry k minus the cumulative shift of entry k−1
(entry 0's cumulative shift being 0): the ticks the robot stands still at the boundary before entry
k. With ONE entry the two quantities are equal, which is why the glossary needed only one term for
them; they became two because T-B Q2 decided ONE HOLD PER ENTRY, placed at the boundary before the
entry it clears (built in T-B2c). `RealizedPlan.holds` carries the hold before each entry and
`RealizedPlan.cumulative_shifts` each entry's cumulative shift; `RealizedPlan.delta` is the hold before
the FIRST entry — with one entry both quantities, with several the only hold that is executed before the
next re-decision — and never the plan's total shift.
→ `shared/types.py`, `RealizedPlan`; `docs/design_decisions.md`, "One hold per entry".

**hold** — unqualified, the hold before the entry being spoken of. Where there is one entry that is
δ, `RealizedPlan.delta`: whole ticks, taken at the robot's position at the decision step, executed
as STAND ticks one per tick, logged as `[hold]`. A hold before a later entry is taken where the previous
entry ended; it is priced at the trigger and never executed as such, because the robot re-decides at its
own triggers first. There is no hold cap.
→ `shared/io_contracts.md` §1.11; `mesa_sim/executor.py`, `hold()`.
NOTE: a stationary `Segment` that is NOT a chosen shift — a grasp, a wait, a completion latency — is
a "stationary stretch" or "stationary segment", not a hold.

**whole-trajectory minimal shift** — the name of the R1 realization policy: the smallest whole-tick
shift under which the plan has no violation in the assessed window, the robot standing still until
it. Since T-B Q2 the policy is applied PER ENTRY (one hold before each entry) rather than once over
the whole plan; the name is kept for the policy. This is the one permitted use of the word
"trajectory" — see "Not in this glossary".
→ `docs/design_decisions.md`, "The robot can wait" (the R1 decisions), "Realization as built".

**minimal-shift search** — given a set of violating shift intervals and a lower bound b, the
smallest whole tick ≥ b that lies inside none of them. It is the loop inside `realize()`, run once per
entry: the shift starts at b and, whenever an interval strictly contains it, jumps to the first whole tick
at or after that interval's end, the intervals taken in order of their start. Not a bisection and
not a grid — feasibility in the shift is not monotone, so the whole-tick answer is NOT the
fractional minimum rounded up. b is the shift the entry inherits: 0 for the first entry, the previous
entry's cumulative shift otherwise (T-B Q2, T-B2c). The repo had no name for this; this one is new.
→ `shared/realization.py`, `realize()`; `shared/io_contracts.md` §2.2c.


**assessed window** — the steps at which both the realized plan and the human projection exist:
[decision step, T_h] intersected with the human projection's span and the realized plan's. Nothing
past T_h is assessed, and nothing before the human projection's span (it starts at the observation
offset) is assessed either.
→ `shared/realization.py`, `realize()`; `shared/io_contracts.md` §2.2c.

**unassessed share** — the share of the realized plan's span lying beyond T_h. Logged so the bias
can be reported, never priced.
→ `shared/io_contracts.md` §1.11.

**min_separation** — the distance realization must keep between the agents. Supplied by the body in
physical units (Mesa: 50 cm, `mesa_sim/mesa_configs.yaml`); `shared/` holds no value for it.
→ `shared/meta_planner.py`, the `min_separation` constructor argument.

**separation stop** — the execution-time refusal in the Mesa executor (run option, default off),
logged as `[stop]`. Distinct from a hold: the hold is decided, the stop is a body-side safety
refusal that decides nothing.
→ `mesa_sim/executor.py`; `docs/design_decisions.md`, the C entry.

---

## 4. Triggers and the decision record

**trigger** — the condition on which `MetaPlanner.update()` re-decides: a change in what the last decision
rested on, the human's hypothesis or the robot's task set. Two, and only two (D3):
- `no_current_task` — there is nothing running.
- `recognition_changed` — the belief no longer points at the hypothesis the last decision projected,
  or first clears the gate on one. Replaced `theta_crossed` at D2; older reports and logs still name
  `theta_crossed`.
- `task_committed` — the ROBOT's own grasp, not the human's commitment. REMOVED BY D3: the grasp was in the
  plan the last decision priced. Older reports and logs still name it.
→ `shared/meta_planner.py`, `evaluate_triggers()`; `shared/io_contracts.md` §2.2.

**decision record** — one field: the hypothesis the last fired trigger's decision was projected
against. `recognition_changed` is read against it from both sides.
→ `shared/meta_planner.py`, `_projected_hypothesis`; `shared/io_contracts.md` §2.2.

**crossing** — a θ crossing, and nothing else: the tick a hypothesis's normalised share first clears
the gate. For paths the word is **violation** (§3); for two paths meeting in space, say that they
intersect.
→ `shared/meta_planner.py`, `_clears_gate()`; `docs/recognizer_handback.md` §3.

**robot trigger** — a trigger raised by the ROBOT's own progress: `no_current_task` (since D3 the only one;
`task_committed` was the other). It replaces "the robot's boundary" everywhere in the living documents, so that
**boundary** keeps one meaning, the recognizer's episode boundary (§5).
The two are not interchangeable: `no_current_task` goes to B3 through B1.5 and BYPASSES the B2 gate,
while `task_committed` goes THROUGH B2, which may keep the current task and never reach B3. A
sentence about re-pricing therefore names the trigger it means, never "the next robot trigger" as if
both re-priced alike. Since D3 the same holds between the two triggers: `no_current_task` bypasses B2,
`recognition_changed` goes through it.
→ `shared/meta_planner.py`, `evaluate_triggers()` and `update()` block B1.5.

---

## 5. The recognizer

**hypothesis** — one candidate task of the observed agent, keyed by `HypothesisKey` (schema plus its
ENUMERATED bindings; determined parameters are not enumerated). The live set is the hypotheses not
yet retired, plus `unknown`.
→ `shared/io_contracts.md` §1.8; `docs/recognizer_handback.md` §1.1.

**stretch** — the recognizer's unit of movement evidence: one continuous run toward one target,
measured from its origin, per hypothesis. ONE observation however many ticks it spans. It is not a
`Segment` and not a walk: a walk may be cut into several stretches by phase changes.
→ `docs/recognizer_handback.md` §1.4.

**graded evidence** — a stretch's evidence against `unknown` is graded by f, the share of the
hypothesis's expected path the stretch covered: `unknown`'s likelihood for the stretch is u^f. A
walk's odds accrue per unit of expected path and do not depend on how the phases cut it. The grade
meters confirmation only; refutation by wasted path is unchanged.
→ `docs/recognizer_handback.md` §1.4 (THE GRADE) and §1.5; `docs/design_decisions.md`, "A stretch's
evidence against `unknown` is graded by the share of the expected path it covers".

**fold** — a phase change charging the closing stretch's final value into the hypothesis's stored
base once, and moving the origin. A fold moves a factor without changing it.
→ `docs/recognizer_handback.md` §1.5.

**pin** / **episode boundary** — a hypothesis whose terminal condition holds is retired and pinned at
the floor (`[IR-complete]`). If the retiring hypothesis expected its terminal action on the previous
tick, the OBSERVED AGENT finished a task and the episode ends (`[IR-boundary]`): every base becomes
the uniform prior and every origin moves. The two criteria are deliberately different.
→ `docs/recognizer_handback.md` §1.6.

**θ (theta)** — the confidence gate. It belongs to the meta-planner, not the recognizer, and is
asked in exactly one place. The recognizer emits a belief distribution and gates nothing.
→ `shared/meta_planner.py`, `DEFAULT_THETA` and `_clears_gate()`; `docs/design_decisions.md`, "θ has
one home", "The gate stays a fixed share".

**β, u, ρ** — β the tolerance on wasted path in the movement likelihood (0.01 /cm, supplied by the
body); u `UNKNOWN_LIKELIHOOD`; ρ B2 `b2a`'s policy parameter.
→ `docs/recognizer_handback.md` §2; `shared/meta_planner.py`, the `rho` constructor argument.

---

## 6. Tasks, schemas and the world

**task instance key** — a `TaskInstance`'s derived identity string: schema name plus its sorted
bindings, e.g. `deliver_item(?item=item_3,?kitting_table=kitting_table_0)`. It carries ALL bindings,
including determined ones; a `HypothesisKey` carries the enumerated ones only.
→ `shared/types.py`, `task_instance_key()`; `shared/io_contracts.md` §1.10.

**determined parameter** — a task parameter that follows from another by a declared lookup
(`TaskSchema.determined_parameters`, e.g. an item's destination table through `destination_of`). The
planner fills it before method selection; the recognizer does not enumerate it.
→ `shared/types.py`, `TaskSchema.determined_parameters`; `shared/io_contracts.md` §1.6;
`docs/design_decisions.md`, "An item's destination table is a fact of the station".

**foreseeable task** — a task the domain declares as a deviation the robot can anticipate
(`schema.is_foreseeable`). Foreseeable tasks sit inline in the human's `scheduled_tasks` and never in
`assigned_tasks`.
→ `shared/types.py`, `TaskSchema` and `AgentConfig`.

**task completion** — a fact about the world: the task's terminal condition holds, whoever made it
hold (`planner.is_complete()`). Not a fact about who performed it. Measured from the world tick, the
tick after the robot's last release; the empty-pool `[meta]` line is the DECLARED tick, two later.
→ `shared/planner.py`, `is_complete()`; `CLAUDE.md`, "Regression checking".

**assigned_tasks / scheduled_tasks** — for the human, the work order (which tasks) and the
developer's execution script (which order). The robot never reads `scheduled_tasks`. For the robot,
`assigned_tasks` is its task pool and `scheduled_tasks` is unread.
→ `shared/types.py`, `AgentConfig`.

The five entries below are decided (T-C1) and built: the scenario layer (T-C2a), the script written, expanded,
edited and checked at load; sequential expansion and the action-level human executor (T-C2b), which runs the
primitives one by one, tracks no task and spends no per-task completion tick.

**primitive** — one entry of the human's executed script: a `ScriptAction` (an action of the domain by schema
name, one element type per action schema) or a `Stay`. Authors write four: `MoveTo`, `PickUp`, `Place` (kitting:
`move_to`, `pick_up`, `place`) and `Stay`, which grounds to nothing (the executor idles). `expand` yields one
element per action of the method, so a `coffee_break` gives a `wait_at` element, which grounds to `wait_at` as
before; `wait_at` is never a `Stay`. The executed `scheduled_tasks` is a flat list of primitives, with no intent
label and no task-boundary marker. A coordinate-valued `MoveTo` exists for Phase 7's exporter; authors never
write one.
→ `shared/types.py`, `ScriptAction`, `Stay`; `domains/kitting/script.py`; `shared/io_contracts.md` §1.12;
`docs/design_decisions.md`, "The human action script (T-C1, decided)".

**expand** — `expand(task)`: turning a `TaskInstance` in the script into primitives at load, by the planner's own
decomposition (optional `method=`). Sequential (T-C2b): each task against the symbolic state the script's
elements before it leave behind, the initial world advanced by the **successor state** (§1). Sets provenance on
each primitive. It needs a world, so it runs where one exists (the loader, tests, a later generator), not in a
scenario file.
→ `domains/script.py`, `expand()`; `docs/design_decisions.md`, "The human action script (T-C1, decided)".

**provenance** — the task a primitive came from, recorded automatically by `expand`, one per expansion. The script
layer's own bookkeeping: the work-order check reads it (every assigned task exactly once); nothing in the robot's
mind does.
→ `shared/types.py`, `Provenance`, `check_work_order()`; `docs/design_decisions.md`, "The human action script
(T-C1, decided)".

**landmark** — a symbolic place a layout may declare (`corner_NE`, `door`), an object of a type of its own that
no `TaskSchema` types a parameter as (rejected at load). So no hypothesis binds one and no robot action grounds
to one; the human's script may walk to it (`MoveTo(landmark)`). The type is `landmark`; env_layout0 declares
`corner_NE`, `corner_NW`, `corner_SE`, `corner_SW` and `door`.
→ `shared/types.py`, `LANDMARK_TYPE`, `check_no_landmark_parameters()`; `docs/design_decisions.md`, "The human
action script (T-C1, decided)".

**deviation vocabulary** — the author's edits of the work order: `interrupt(task, after=|before=, with_=[...])`,
`deviate(task, destination=)`, `abandon(task, after=|before=, then=[...])`, plus free `Stay(n)` (n omitted:
until the run ends) and `MoveTo(landmark)`. Anchors name an action by name or index; injected content may mix
tasks and primitives; in T-C every injection sits at an action boundary. A deviation is an edit of the
expanded work order, not a task of its own. Written at import, where there is no world, each returns a deferred
edit (`[Deviation]`) that the loader applies to the task's expansion with the list helpers (`insert_after`,
`insert_before`, `retarget`, `truncate`).
AUTHOR CONVENTION (T-C2c, Hadi): a script ends with the human leaving the workspace (`MoveTo("door")` or a corner),
unless the scenario is about the terminal stand at a table (TODO-80's blocked case, said in its description): a
human left standing at a table deadlocks the robot with the stop on, an artefact of the scenario.
AUTHOR NOTE (T-C2b): content injected by `interrupt` is expanded sequentially, but the interrupted task's
remaining actions are not: a task injected after a pick-up that returns the held item (`deliver_with_return`)
leaves the resumed `place` failing at run time. Write the return explicitly, or use `abandon`.
→ `domains/script.py`; `docs/design_decisions.md`, "The human action script (T-C1, decided)".

---

## 7. Sessions

**cchat** — the design chat with Hadi, where design is decided. **ccode** — the Claude Code session
in the repository, which builds and checks; older reports call it Fable.
→ `CLAUDE.md`, "Conventions and terminology".

**T-A … T-G** — the plan names task prompts and reports use.
→ `docs/roadmap.md`, "The plan from T-A".

---

## Not in this glossary

**trajectory** has no definition and gets none: inventing one is a design act. In the living
documents and comments it is replaced by what is actually meant — "the segments of a
`ProjectedPlan`" or "the segments of a `RealizedPlan`". The ONE permitted use is the name of the R1
policy, **the whole-trajectory minimal shift** (§3). The module name `trajectory_algorithms.py` is
an identifier and is not renamed, and the removed "cosine trajectory kernel" keeps its name in the
record because that is what was removed (`docs/recognizer_handback.md` §8).

**leg** has no definition and is not used. The recognizer has no leg concept — the leg model was
removed and must not return (`docs/recognizer_handback.md` §8), and its unit is the **stretch**. A
human's movement is a **walk**.
