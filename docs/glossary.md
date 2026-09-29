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
An empty pool prevents planning and execution only; the robot's observation and recognition go on every tick (ruled
27 September 2026, built in TB.2b; `docs/design_decisions.md`, "The cognitive loop does not end with the task pool").
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
The same derivation advances the human script's symbolic state at load (the load-time replay, `check_script`, §6).
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

**segment** — one `Segment` inside an entry: a straight-line motion, or a stationary interval (a stationary segment),
between two steps. An entry has several segments — one per action, plus the completion latencies.
Do not call a segment a "stretch of evidence"; that is the recognizer's.
→ `shared/types.py`, `Segment`; `shared/io_contracts.md` §1.7.
IN THE RECORD: scenario_40's (now scenario_s04_01) human script was described as four numbered "segments" (1, 2,
3a, 3b, 4). That is a SCRIPT PART, not a `Segment`. "Segment 3a" in `docs/design_decisions.md`,
`docs/TODOS_AND_DEFERRED.md` and the I4 / F47 reports means script part 3a. The living files
(`domains/kitting/layouts/env_layout_05.json`, `domains/kitting/scenarios/scenarios_s04.py`,
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
AMENDED (T-D P, 28 September 2026): when admission refuses and a human is observed, the **fallback projection**
takes its place.

**fallback projection** — the short-term physical projection of T-D P, built when admission refuses and a human is
observed: where to expect the human, from what was observed and for as long as it was observed, claiming nothing
about intention (P4). From the robot's perception facts (`WorldState.agent_displacements`, `agent_run_lengths`,
`agent_standing_counts`): MOVING, the last displacement continued for as many ticks as the current straight run has
lasted, ended earlier where the ray meets the workspace boundary or enters the first fixed object's arrival radius,
with no stand after it; STANDING, a stand at the observed position for as many ticks as the human has stood; no
previous observation, no fallback. From the observation offset; one per decision, the same for every candidate.
Beyond it the human is unassessed. `realize()` prices it as any projection (F1: a finite hold or none). Nothing is
admitted, so the recorded hypothesis stays empty; its end (T_h) is recorded, and reaching it fires
`projection_expired`. Logged `[meta-proj] … projection=fallback refused=<reason>`.
AMENDED (P4, 28 September 2026): the tail to the wall, the stand for the candidate's whole span, the refusal (rule 5)
and the wait of the earlier forms are superseded.
→ `docs/design_decisions.md`, "T-D P: the fallback projection" (P4, Q6); `shared/projection.py`,
`Projector.project_fallback()`; `shared/io_contracts.md` §2.2.

**run length** / **standing count** — the robot's perception facts of an observed agent's motion (T-D P4): the
number of consecutive ticks of the current straight run (unit directions equal within 1e-9, the body's numerical
resolution; a turn sets it to 1, a stop to 0), and of consecutive zero displacements (a step resets it). Written by
`RobotAgent` from its consecutive observations, beside the last displacement; a bounded memory, not a history.
→ `shared/types.py`, `WorldState`; `mesa_sim/sim_agents.py`, `RobotAgent._perceive()`.

**occupied target** — X's case (proposed as a term, T-D P-build, 28 September 2026): with nothing realizable under
the fallback, the robot waits because the human stands at the robot's target. What to do then is X's. ("Blocked
route", the human standing on the robot's walk to its target, has no instance in the fixtures and stays one of X's
categories in the design record, not a term here.)
→ `docs/design_decisions.md`, "T-D P", the deadlock.

**T_h** — the end of the human projection: its last segment's end step. Nothing past T_h is
assessed or charged. Under a fallback projection T_h is the candidate's own end, so it differs per candidate;
`UpdateResult.horizon` carries the winner's (T-D P).
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
a "stationary segment", not a hold ("stationary stretch" is not used: **stretch** is the recognizer's).

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
rested on, the human's hypothesis, the robot's task set, or the fallback projection it was realized against. Three
since T-D P4 / Q6 (two, and only two, from D3 to P4):
- `no_current_task` — there is nothing running.
- `recognition_changed` — the belief no longer points at the hypothesis the last decision projected,
  or first clears the gate on one. Replaced `theta_crossed` at D2; older reports and logs still name
  `theta_crossed`.
- `projection_expired` — the fallback projection the last decision rested on has reached its end (its T_h, where the
  projection is truncated, not where its evidence would have taken it); after `recognition_changed` on a shared tick,
  through B2. Scoped to fallbacks: an admitted projection's end is P3's question (T-D P, Q6).
- `task_committed` — the ROBOT's own grasp, not the human's commitment. REMOVED BY D3: the grasp was in the
  plan the last decision priced. Older reports and logs still name it.
→ `shared/meta_planner.py`, `evaluate_triggers()`; `shared/io_contracts.md` §2.2.

**decision record** — one field: the hypothesis the last fired trigger's decision was projected
against. `recognition_changed` is read against it from both sides.
AMENDED (T-D P4 / Q6, 28 September 2026): a second value, the tick at which the fallback projection the last decision
rested on reaches its T_h, read by `projection_expired`; set when admission returns a fallback, cleared otherwise.
→ `shared/meta_planner.py`, `_projected_hypothesis`; `shared/io_contracts.md` §2.2.

**retraction** — the meta-planner's act of withdrawing an admitted projection when the hypothesis the decision was
projected against leaves adequate (its **hypothesis adequacy**, §7): `recognition_changed` fires on that hypothesis
only, never on a rival's transition; admission is re-asked and G1 refuses, so the decision realizes against no human
plan; re-admission is through the entering side of `recognition_changed` when the leader clears the gate again. The
recognizer retracts nothing: inadequacy attaches to the derived phase and stays until its advance (L2 (i)), and the
recognizer's side has no term. Older texts use the word for the recognizer's side (T-D Q2; E7's "retraction and
resumption are L"; the **unexplained** entry, §7); L2 (i) rules that side out. Ruled in L2 (ii), built in L-build.
→ `docs/design_decisions.md`, "T-D L: the belief lifecycle", L2; `shared/io_contracts.md` §2.2.
AMENDED (Hadi, on the L-records report, 27 September 2026): "leaves adequate" is ADEQUATE to INADEQUATE, never to
no observation (which every boundary and every proximity regress would produce). Built as the state "the recorded
hypothesis is inadequate": a record is set only while its hypothesis is adequate (G1) and the fire clears it. There is
no P fallback: the decision realizes against no human plan, as below θ. Logged `[meta-trig] … cause=retraction`.
SUPERSEDED IN PART (T-D P, 28 September 2026): "there is no P fallback" no longer holds; with a human observed the
decision after a retraction realizes against the **fallback projection**. The retraction itself is unchanged.

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
yet retired, plus `unknown`, the residual hypothesis (§7). A hypothesis belongs to the robot's belief; whether a
behaviour of the human is described by one is its coverage (label B, §7).
→ `shared/io_contracts.md` §1.8; `docs/recognizer_handback.md` §1.1.
SUPERSEDED IN PART (T-D R, 27 September 2026): "plus `unknown`": the `unknown` hypothesis leaves the hypothesis space (R1). design_decisions.md, "T-D R and E".
SUPERSEDED IN PART (T-D L4, ruled 27 September 2026, built in L-build): the LIVE SET is the support minus the
hypotheses whose terminal fact holds on this tick, read from the world on every tick: retirement lasts exactly as long
as the fact holds, and a hypothesis whose fact stops holding re-enters with the prior base and the current position as
origin (the others renormalised). "Not yet retired" no longer means "never completed". design_decisions.md, "T-D L:
the belief lifecycle", L4.
AMENDED (Hadi, on the L-records report, 27 September 2026): RE-ENTRY takes exactly 1/|H| (H the live set with the
returning hypothesis; k returning on one tick take 1/|H| each), the incumbents share the rest in this tick's
proportions; the origin is the current position, the entry latency that of a first observation (0), the derived action
the world's. Logged `[IR-reentry]`. A re-entry on a boundary tick is governed by the boundary.

**stretch** — the recognizer's unit of movement evidence: one continuous run toward one target,
measured from its origin, per hypothesis. ONE observation however many ticks it spans. It is not a
`Segment` and not a walk: a walk may be cut into several stretches by phase changes.
→ `docs/recognizer_handback.md` §1.4.

**graded evidence** — a stretch's evidence against `unknown` is graded by f, the share of the
hypothesis's expected path the stretch covered: `unknown`'s likelihood for the stretch is u^f. A
walk's odds accrue per unit of expected path and do not depend on how the phases cut it. f is the covered
fraction (`covered_fraction`), unrelated to model coverage (label B, §7). The grade
meters confirmation only; refutation by wasted path is unchanged.
→ `docs/recognizer_handback.md` §1.4 (THE GRADE) and §1.5; `docs/design_decisions.md`, "A stretch's
evidence against `unknown` is graded by the share of the expected path it covers".

**fold** — a phase change charging the closing stretch's final value into the hypothesis's stored
base once, and moving the origin. A fold moves a factor without changing it.
→ `docs/recognizer_handback.md` §1.5.

**pin** / **episode boundary** — a hypothesis whose terminal condition holds is retired and pinned at
the floor (`[IR-complete]`). If the retiring hypothesis expected its terminal action on the previous
tick, the OBSERVED AGENT finished a task and the episode ends (`[IR-boundary]`): every base becomes
the uniform prior and every origin moves. The two criteria are deliberately different. After a boundary `unknown`
holds 1/|Live| by normalisation, not from evidence (§7).
→ `docs/recognizer_handback.md` §1.6.
SUPERSEDED IN PART (T-D R, 27 September 2026): "`unknown` holds 1/|Live|": the `unknown` hypothesis leaves the hypothesis space (R1). design_decisions.md, "T-D R and E".
SUPERSEDED IN PART (T-D L1 and L4, ruled 27 September 2026, built in L-build). EPISODE BOUNDARY (L1): it fires when the
observed agent completes an action that is terminal in the task model (`place`, `wait_at`), read from the completion
channel, whatever its binding; it no longer needs a pin. TERMINAL PIN: it stays the world's terminal fact of a live
hypothesis; a boundary at a pin is the special case where the terminal action also produces that fact. A task whose
execution ends without its terminal fact (a misdelivery) stays live and starts the next episode at the prior: "live"
and "being executed" are separate. The pin retires "for the rest of the run" no longer (L4): a pinned hypothesis
stays retired while its terminal fact holds and re-enters the live set when it stops holding (**hypothesis**, above).
design_decisions.md, "T-D L: the belief lifecycle", L1, L4.
AMENDED (Hadi, on the L-records report, 27 September 2026; supersedes "read from the completion channel"): the
boundary fires when a terminal action's own completion condition becomes true for the observed agent: the action's
preconditions held for that agent on the previous tick (`holding(agent, x)`; `at(agent, e)`) and a grounding of its
completion condition under that binding holds now and did not then (`obj_at(x, c)`: the release leaves the object
placed at a container; `waited(agent, e)` starts holding). No microaction is read: a bare RELEASE is no boundary. A
terminal `place` is a boundary wherever it sits in a decomposition (a return inside `deliver_with_return`). The
boundary tick is flagged on the belief (`BeliefState.episode_boundary`), and `recognition_changed` fires on it for any
recorded decision (L5 B). `[IR-boundary]` names the completed action.

**θ (theta)** — the confidence gate. It belongs to the meta-planner, not the recognizer, and is
asked in exactly one place. The recognizer emits a belief distribution and gates nothing. The gate's outcome is
**admitted** (§7); the recognizer's own finding is **unexplained** (§7), never a gate outcome.
→ `shared/meta_planner.py`, `DEFAULT_THETA` and `_clears_gate()`; `docs/design_decisions.md`, "θ has
one home", "The gate stays a fixed share".
AMENDED (T-D G, AD1, built in G-build, 29 September 2026): θ is the gate's first condition, not its only one: the gate
(`_clears_gate()`, still its one home) admits when the leader's share is at least θ, its **hypothesis adequacy** (§7) is
adequate, and it is **warranted** (§7), asked in that order; clearing θ alone admits nothing. design_decisions.md, "T-D
G: admission".

**β, u, ρ** — β the tolerance on wasted path in the movement likelihood (0.01 /cm, supplied by the
body); u `UNKNOWN_LIKELIHOOD`, the `unknown` hypothesis's reference likelihood, not a measure of unmodelled
behaviour (§7); ρ B2 `b2a`'s policy parameter.
→ `docs/recognizer_handback.md` §2; `shared/meta_planner.py`, the `rho` constructor argument.
SUPERSEDED IN PART (T-D R, 27 September 2026): u leaves the belief (R1); β gains a second meaning, the scale of the reference distribution (E5, **tail probability**). design_decisions.md, "T-D R and E".

The four entries below are ruled (T-D R and E, 27 September 2026) and built (T-D Stage 1, 27 September 2026). They
belong to the **adequacy finding** (§7).

**derived phase** — the unit of the adequacy test: one live hypothesis's current phase, from its existing origin to its
phase advance (E1). One per live hypothesis at a time; no window, no episode constant. It is bounded as the hypothesis's
**stretch** is (the origin moves at a **fold** and at an **episode boundary**), but a stretch is the belief's unit of
movement evidence, and a derived phase holds standing as well as walked path. A regress at the proximity threshold is a
phase change and restarts it (limitation (b)). Not a `Segment`, not an entry.
→ `docs/design_decisions.md`, "T-D R and E: the recognizer's output under a removed `unknown` hypothesis", E1.

**projected completion delay** (D) — the adequacy test's one statistic per live hypothesis per **derived phase**:
D = e/v + (s − s_exp), with e the excess path from the origin as the movement likelihood computes it, v the body's
speed, s the ticks without movement since the origin and s_exp the standing the Projector prices for the phase (0 for
`move_to`, 1 tick for `pick_up` and `place`, the bound duration for `wait_at`). In ticks. Path and standing are two
components of one statistic, not two tests; a detour is counted once. A stand in a `move_to` phase is charged against
s_exp = 0 (E3). Non-decreasing within a phase. Time enters here only, never the belief's likelihood.
→ the same entry, E2, E3.
RULED (1.5 rulings, 27 September 2026; to be built in cycle 1.5b): also the belief's evidence per phase through L(v·D) (E10),
beside adequacy's S(v·D); "time enters here only, never the belief's likelihood" is superseded by it. For a walk
without standing L(v·D) = L(e), walking evidence unchanged; standing within the priced duration gives D ≤ 0 and L = 1.
s_exp is the Projector's priced stationary ticks within the phase's span (E9): 2 for `pick_up` and `place` in kitting;
a walk entered from a completion receives that completion's latency tick, the initial walk 0.
→ the same entry, "1.5 rulings", E9, E10.

**tail probability** (S_k) — hypothesis k's tail of the reference distribution at v·D:
S(x) = ln(1 + e^(−βx)) / ln 2, and S = 1 for x ≤ 0. The reference distribution is the belief's own likelihood shape
read as a density, p(x) = βL(x) / (2 ln 2) on x ≥ 0: a modelling assumption, stated as one, whose empirical adequacy is
open. β is the movement likelihood's tolerance (above), not retuned for adequacy; this is its second meaning, the
scale of the reference distribution. The recognizer reports S_k per live hypothesis beside the finding, for
evaluation; it is not a belief and not a share.
→ the same entry, R2, E5.

**test level** (α) — the level the tail probabilities are tested at, per derived phase: a live hypothesis is
inadequate in its phase when S_k < α. Recognizer configuration (a run option), default 0.05 as a convention, reported
at every level (0.01, 0.05, 0.1), never chosen from a scenario. Not a meta-planner threshold and not θ: it does not
touch DESIGN-07, and the meta-planner receives the categorical finding and, since G1 (1.5 rulings, 27 September 2026;
to be built in cycle 1.5b), the categorical per-hypothesis adequacy of the leader (**adequacy finding**, §7), never α or
S_k: the rule is unchanged, restated. At v = 20 cm/tick and
β = 0.01 /cm the threshold is v·D = 334 cm at α = 0.05 (17 ticks of standing, or 167 cm walked straight away from every
live target), 497 cm at α = 0.01.
→ the same entry, E4, E5.

---

## 6. Tasks, schemas and the world

**task instance key** — a `TaskInstance`'s derived label string: schema name plus its sorted
bindings, e.g. `deliver_item(?item=item_3,?kitting_table=kitting_table_0)`. It carries ALL bindings,
including determined ones; a `HypothesisKey` carries the enumerated ones only. A label for logs and the `[rec]`
stream since T-H4, not an identity: whether two instances are the same task is **task equality**.
→ `shared/types.py`, `task_instance_key()`; `shared/io_contracts.md` §1.10.

**task equality** (T-H4) — `same_task(a, b)`: the same schema by identity and equal **goal bindings**, a task's
bindings minus its determined parameters (they follow from the station) and its duration parameters (how long is
not what: `stand("PT10S")` and `stand("PT50S")` are one task). The one definition, read by the duplicate check on
assigned tasks, the recognizer's support restriction, the robot's continue decision and the record's queries. A
`TaskInstance`'s `==` is object identity. A stated determined binding is not part of a task's identity: it is the
station's, or a **departure**. Replaces the `task_instance_key` comparisons (TODO-107).
→ `shared/types.py`, `same_task()`, `goal_bindings()`.

**departure** (T-H4) — `Departure(var, designated, stated)`: a stated determined binding that is not the station's
(`deliver_item("item_1", table="kitting_table_2")` where the setup designates `kitting_table_0`; the layout stored the
designation until T-L's stage 1). The binding-level
deviation of a delivery to another table; `assigned` reports it, and it makes coverage `BINDING_ABSENT`.
`check_task_destinations` refuses an assigned task with one.
→ `shared/types.py`, `destination_departures()`.

**determined parameter** — a task parameter that follows from another by a declared lookup
(`TaskSchema.determined_parameters`, e.g. an item's destination table through `destination_of`). The
planner fills it before method selection; the recognizer does not enumerate it.
→ `shared/types.py`, `TaskSchema.determined_parameters`; `shared/io_contracts.md` §1.6;
`docs/design_decisions.md`, "An item's destination table is a fact of the station".

**foreseeable task** — defined, not declared (T-H): a `PersonalTask` in the robot's **task model**. It is never
assigned. The support restriction keeps every hypothesis of it admissible under the assignment prior. On the queries
of §7: a switch to it is not a deviation, since the robot's tree contains it (`assigned` false, `coverage` `COVERED`).
AS BUILT until T-H1: declared on the schema (`schema.is_foreseeable`), read in the robot's mind at one place
(`_build_admissible_keys`); kept out of `assigned_tasks` by convention only (TODO-98).
→ `docs/design_decisions.md`, "T-H: the human behaviour model", item 3; `shared/recognizer.py`,
`_build_admissible_keys()`.

**task completion** — a fact about the world: the task's terminal condition holds, whoever made it
hold (`planner.is_complete()`). Not a fact about who performed it. Measured from the world tick, the
tick after the robot's last release; the empty-pool `[meta]` line is the DECLARED tick, two later.
→ `shared/planner.py`, `is_complete()`; `CLAUDE.md`, "Regression checking".

**assigned tasks** — a set the robot is told: for the human, which tasks it was assigned (every one a `WorkTask`
instance, T-H), never in which order; the ordering lives only in the human's script. Replaces "work order" (T-H,
25 Sept 2026; older records say "work order"). For the robot, `assigned_tasks` is its task pool.

**assigned_tasks / scheduled_tasks** — the `AgentConfig` fields: the assigned tasks, and the human's script. The robot
never reads `scheduled_tasks`; for the robot it is unread.
→ `shared/types.py`, `AgentConfig`; `docs/design_decisions.md`, "T-H: the human behaviour model", item 4.

THE HUMAN BEHAVIOUR MODEL (T-H). Ruled by Hadi, 25 September 2026 (with the rulings on the review); T-H1 to T-H3
built (T-H3 migrated every scenario and deleted the T-C1 script layer: primitives, `Stay`, `expand`, provenance, the
deviation vocabulary), T-H4 built the record's queries (`world/queries.py`). The entries below are the meaning
from here.
→ `docs/design_decisions.md`, "T-H: the human behaviour model"; `docs/handoffs/handoff_T-H.md`. Code (T-H2): the
script types in `shared/types.py` (`Trigger`, `Decision`, `Event`, `ScriptEntry`, `Script`, the `at` / `during`
sugar); the stack machine and the load-time replay in `world/human_executor.py`; the record in `world/record.py`;
the body-side driver `HumanAgent._step_stack` and `HumanAgent.inject` in `mesa_sim/sim_agents.py`; the cut in
`mesa_sim/executor.py` (`suspend`, `resume`, `progress`); the kitting call forms (`deliver_item("item_3")`,
`coffee_break(...)`, `go_to(...)`, `stand(...)`, `go_to_and_stand(...)`, T-H3) in `domains/kitting/script.py`. `world/` is the world's side (CLAUDE.md, "Layering: four
homes"): it imports `shared/` only.

**WorkTask / PersonalTask / HumanOnlyTask** — the three classes of the one tree of task schemas per use case, each
with the full HTN structure. A `WorkTask` may appear in a human's assigned tasks (`deliver_item`); a robot's own
assigned tasks are `WorkTask`s. A `PersonalTask` is never assigned (`coffee_break`, `ac_activation`). A
`HumanOnlyTask` is a `PersonalTask` never given to any robot (`go_to(?landmark)`, `stand(?duration)`,
`go_to_and_stand(?landmark, ?duration)`); it is the only
class that may type a parameter as a landmark. Replace `TaskSchema.is_assigned` and `is_foreseeable`.

**tree** — the world's tree of task schemas, one per use case: one of the two knowledge objects. The human executor's
planner uses it.

**task model** — a robot's task model: the subset of the tree the robot is given, chosen per experiment by whole
schemas; the other knowledge object, one per robot, built from the tree in the embodiment loader. A `WorkTask` is never
left out (the robot plans its own tasks with it); a `PersonalTask` may be omitted per experiment; a `HumanOnlyTask` is
rejected when a task model is built (`TaskModel`'s constructor, T-H1 ruling). The robot's recognizer, projector and
planner use the task model only; the robot's inference reads no human-only-ness, only the construction-time
validation of the knowledge objects does. The hypothesis space is built from the task model and the run's layout and
setup (until T-L's stage 1, one layout file held both). The
class of a schema is read in one place in the robot's mind, the support restriction: admissible = the hypotheses of
the `WorkTask` instances in the assigned tasks, every hypothesis of a `PersonalTask` in the task model, and `unknown`,
compared as `HypothesisKey` values.
SUPERSEDED IN PART (T-D R, 27 September 2026): "and `unknown`": the `unknown` hypothesis leaves the hypothesis space (R1). design_decisions.md, "T-D R and E".

**ProceduralKnowledge** — how things are done: task schemas with their methods, action schemas, microactions and
costs. The base class of the two knowledge objects, **tree** and **task model**, which are its two forms (`Tree`,
`TaskModel`); never constructed directly. Validated at construction (every method step calls a schema of the object,
by identity; the landmark rule in `Tree`; the `HumanOnlyTask` rejection and the every-`WorkTask` requirement in
`TaskModel`). Not "domain knowledge": "domain" names the use case. Beside it, `ContextKnowledge` holds background
facts for the recognizer's context weight.
→ `shared/knowledge.py` (was `shared/domain_knowledge.py`, `DomainKnowledgeBase`; T-H1)

**human's script** (T-H) — an ordered list of fully bound `TaskInstance`s of the tree (the author writes the machine;
a determined parameter follows from its lookup unless the author states it), with **events** attached to a task. A
binding-level deviation is a plain instance (`deliver_item("item_1", table="kitting_table_2")`); a `HumanOnlyTask`
instance is a plain entry (`stand("PT50S")`, `go_to("door")`). Checked at load for types, and every anchor against the
load-time sequential expansion (events and resumptions included), which the executor must reproduce exactly; the
check that a stated table agrees with the station (`check_task_destinations`) applies to the assigned tasks and the
robot's plans. A free placement or a handover, if ever wanted, is a task of the tree.
AUTHOR CONVENTION (T-C2c, carried over): a script ends with the human leaving the workspace (`go_to("door")` or a
corner), unless the scenario is about the terminal stand at a table (TODO-80), said in its description. Extended to the
regression fixtures whose terminal stand is not their purpose (Track 2.5): `docs/assumptions.md` 1.1.

**event** — a `Trigger` and a `Decision` attached to a task of the script, or built live by `inject`. Typed, no unions
and no sentinels. An event fires once per script entry and is then consumed.
COLLISION: T-D's "blocked event" (the body's report that the robot cannot proceed, `ExecutorState`) is not an event
in this sense.

**decision** — what an event does: `Start(task)` (suspend the current task and run `task`, any `TaskInstance` of the
tree) or `Drop`.

**event trigger** — what fires an event: `AfterAction(action, occurrence)` (written with `at`), `DuringAction(action,
time)` (written with `during`), or `Now` (`inject`). The ruling calls it "trigger"; in prose write "event trigger",
because **trigger** (§4) is the meta-planner's re-decision condition.

**at** — `.at(action, task_instance)` / `.at(action, drop)`: sugar for an event with an `AfterAction` event trigger
and a `Start` / `Drop` decision; the trigger which fires AFTER the action completes. `action` is a
reference to an `ActionSchema` object of the task's decomposition (an occurrence index when the method repeats it),
never a name string. The boundary before a task's first action is the previous entry's last action; before the whole
script, a plain entry. An anchor absent from a re-expansion is a load error.
COLLISION: the world predicate `at(agent, object)` (executor completion) is a different thing; say "the `at` event
trigger" where both could be read.

**during** — `.during(action, time, task_instance | drop)`: sugar for an event with a `DuringAction` event trigger, a
cut a stated physical time into the action (ISO-8601, the form durations use; the body converts it, the exporter
converts the recorded tick once), and a `Start` / `Drop` decision. No fraction or position forms. Built in T-H2.
The authored forms (`at`, `during`) are sugar that constructs `Event(AfterAction | DuringAction, Start | Drop)`; the
types are fixed, T-H2's plan shows the sugar.

**drop** — the decision `Drop`: it removes the top of the stack, authored or injected (`task.at(pick_up, drop)`
abandons `task`). Replaces `abandon`.

**inject** — `executor.inject(Start(task) | Drop())`: a live event with the event trigger `Now`; the viewer's buttons
are a fixed set of inject calls. Export rewrites `Now` as `AfterAction` or `DuringAction` from the record; an
injection on an empty stack is exported as a plain script entry; an exported run replays byte-identically.

**stack** — the human executor's stack of tasks, one level deep in T-H (nesting is allowed by the structure and
lifted only when a scenario needs it, TODO-100). On `Start` the executor suspends the current task and runs the
decision's task; it can stop an action mid-way. On resumption it first completes the cut action with what remains of
it (the rest of the walk from the current position, the remaining duration of a stand), then re-expands the task in
the resulting state (sequential expansion through the **successor state**, §1). One rule for every action type.
**outcome** — of a task on the stack, computed from what the stack did and the world, never authored: completed,
suspended, abandoned, infeasible. Completion is a world fact whoever caused it (**task completion**); a resumption with
nothing left to do is completed; a task with no applicable method is infeasible, recorded, and the executor moves on.

**record** — the human executor's record: per tick, the stack (top first), the action and its progress. The ground
truth, written as its own stream (a file beside the run log, one `[rec]` line per tick) and diffed in the sweep. Its
typed queries are `switches`, `resumptions`, `assigned(task)`, `unperformed(assigned_tasks)`, `coverage(task, robot)`
and `truth_at(tick)`; they replace labels A and B, provenance, `Deviation`, string anchors and the key-counting
`check_work_order` (`unperformed` replaces it). Built in T-H2, queried in T-H4 (`world/queries.py`, pure functions on
the in-memory `Record`; the `[rec]` stream is never read back): `truth_at(record, tick)` is the tick's `Snapshot`;
`switches` every applied `Start` (authored or injected, on a task or on the empty stack; a `Drop` is not a switch, it
is `Left(ABANDONED)`); `resumptions` every `Resumed`; `assigned` and `unperformed` are label A (§7), `coverage`
label B. `world_state_builder` exposes nothing
of the stack; `truth_at` enters the robot's mind only through the oracle condition's explicit adapter (TODO-101).
SIMULATION ONLY: the record, coverage and the oracle IR exist in simulation; a real human needs annotation of the same
form.
One world behaviour may have two records (`A.at(x, B)` against `A.at(x, drop), B, A`): accepted, the record
is of the human's decisions, not of the body.
COLLISION: the **decision record** (§4) is the meta-planner's one field; "the design record" is the documents. Write
"the executor's record" where either could be read.

**deviation** (T-H) — a node of the human's realised plan tree that the robot's tree does not contain, at one of two
levels: the task schema is absent, or the binding is absent (the **coverage** value). Supersedes the 24 September
meaning (any departure from the work order, label A): a switch to a `PersonalTask` in the task model is not a
deviation.

**coverage** — `coverage(task, robot)`, a query on the record, judged per task instance on the stack against the
robot's task model and the run's layout and setup (not against the support the assignment prior narrows). Values: `COVERED`;
`TASK_ABSENT` (the schema is not in the task model: every `HumanOnlyTask`, and a `PersonalTask` omitted per
experiment); `BINDING_ABSENT` (the schema is, the binding is not: a wrong-table delivery, since a hypothesis carries the
item's designated table). An interrupted task is `COVERED` when its own instance is; its interruption is judged on its
own. Unrelated to the covered fraction f of **graded evidence** (§5).
AS BUILT (T-H4): typed results `Covered(hypothesis)`, `TaskAbsent(schema)`, `BindingAbsent(var, value)` (the binding
no hypothesis carries), judged against an `ObservingRobot` (the robot's task model, its hypothesis space, the
station's destinations) the body builds at spawn. In order: the schema not in the task model, `TASK_ABSENT`; no
hypothesis the same task (**task equality**), `BINDING_ABSENT` with the first goal binding, in parameter order, no
hypothesis of the schema carries; a **departure**, `BINDING_ABSENT` with its stated binding; else `COVERED` with the
hypothesis. The loader prints one `[coverage]` line per script entry for each observing robot, in the run log: the
entry's task and each event's started task, each with its value. Information for the reader, the same with the prior
on and off.
→ `world/queries.py`; `mesa_sim/sim_model.py`, `_log_coverage()`.

**wait_at / stand** — two actions. `wait_at(?entity, ?duration)`, unchanged: located, it completes `waited(agent,
entity)` and is the expected action of `coffee_break` and `ac_activation`. `stand(?duration)`, added by T-H: no
entity, process completion only, it emits no world fact; the `HumanOnlyTask` `stand(?duration)` uses it as its single
action. Durations in the physical form `wait_at` uses (ISO-8601, converted by the body), the parameter's type declared
through `duration_key`, not `parameter_types`; the projector takes a stand's duration from the instance's binding.
Where the action and the task could both be read, write "the stand action" or "the stand task".
COLLISION: "a stand" in §7 and the older records is the ordinary word for a human standing still (in the record, a
`stand` task, a `wait_at` inside a task, or an empty stack); the hold's STAND ticks are a microaction.

**landmark** — a symbolic place a layout may declare (`corner_NE`, `door`), an object of the type `landmark`. Only a
`HumanOnlyTask` may type a parameter as one (`go_to(?landmark)`, `go_to_and_stand(?landmark, ?duration)`; `Tree`'s
constructor rejects any other), so no hypothesis binds one and no robot action grounds to one. env_layout_01 declares
`corner_NE`, `corner_NW`, `corner_SE`, `corner_SW` and `door`.
→ `shared/types.py`, `LANDMARK_TYPE`; `shared/knowledge.py`, `Tree`.

**go_to** — the `HumanOnlyTask` `go_to(?landmark)`: walking to a landmark (`move_to` the landmark). Replaces
`MoveTo(landmark)`. Walks from the viewer go to landmarks only.

**go_to_and_stand** — the `HumanOnlyTask` `go_to_and_stand(?landmark, ?duration)`: walking to a landmark and standing there
(`move_to` the landmark, then the stand action), one decision (T-H3). Started by an event, it is the interruption in
which the human steps away to a place and stays, and the suspended task resumes after it.

---

## 7. Human behaviour, model coverage and the robot's inference

Ruled by Hadi, 24 September 2026; the WORLD half revised by T-H (25 September 2026). "Unknown" used to name two
different things: what the human does (behaviour outside the robot's models) and what the robot believes (the mass on
the residual hypothesis `unknown`). The two diverge: a stand adds no evidence of its own, and a finished set of
assigned tasks leaves `unknown` near 0.995 while nothing is unexplained. The terms below keep four things apart: what
behaviour occurs in the world, whether the robot's models cover it, whether the scenario's author intended it (its
purpose), and what the robot believes. They form two groups, WORLD and ROBOT. A term from one group is
never used for the other. Diagrams, a table of cases and the divergences: `docs/terminology_revision.md`
(explanatory; this section is authoritative; its section 8 states what T-H changed).
→ `docs/design_decisions.md`, "Terms for human behaviour, model coverage and the robot's inference" and "T-H: the
human behaviour model".

WORLD: ground truth, read from the human executor's **record** (§6) by typed queries, in simulation only (T-H4; before T-H, labels A and
B, computed from the script and the hypothesis space, never built: TODO-92, superseded by T-H4). The robot's mind never
receives them. The query `truth_at(tick)` gives the stack at a tick; the behaviour at a tick is the task on top of the
stack, or no task.

**label A, assigned** — the query `assigned(task)`: whether the task on the stack is one of the human's **assigned
tasks** (§6); with `unperformed(assigned_tasks)`, the assigned tasks never performed: no task left the stack
`COMPLETED` that is that assigned task with no **departure** (an abandoned one, one delivered to another table, one
never begun and one the run ended in are unperformed). Replaces "label A, work order", whose values were "assigned task" and "deviation". A task that is not
assigned is a `PersonalTask` (a **foreseeable task** when the robot's task model holds it), a `HumanOnlyTask`, or a
`WorkTask` instance the assigned tasks do not contain. With no task on the stack (the script finished, the human idle)
the query has no value. The word "deviation" no longer names a value of label A (§6, **deviation**).
AS BUILT (T-H4): `assigned` returns `Assignment(assigned, departures)` or `None` (not assigned): the assigned task that
is the same task (**task equality**, §6), and the bindings the assignment did not give. A binding-level deviation of
an assigned task is the assigned task with a departure: `deliver_item("item_1", table="kitting_table_2")` against the
assigned `deliver_item("item_1")` gives that assigned task and `?kitting_table=kitting_table_2(designated
kitting_table_0)`. Neither a boolean nor a separate value.

**label B, coverage** — the query `coverage(task, robot)` (§6, **coverage**): whether the robot's tree contains the
task's nodes, and if not, at which level. Two classes of behaviour, in prose:
- **modelled behaviour** — the task on the stack has coverage `COVERED`: a hypothesis of the robot's hypothesis space
  describes it.
- **unmodelled behaviour** — coverage `TASK_ABSENT` or `BINDING_ABSENT`; the node the robot's tree lacks is a
  **deviation** (§6). Examples: a walk to a corner (`go_to`, `TASK_ABSENT`), a stand of five minutes
  (`stand("PT5M")`, `TASK_ABSENT`), a `coffee_break` the experiment omitted from the task model (`TASK_ABSENT`), a wrong-table delivery (`BINDING_ABSENT`, TODO-87: the schema and method are modelled,
  but a hypothesis carries the item's designated table, a **determined parameter**, §6).
With no task on the stack there is no task to judge: the idle human after the script is its own case (T-D Q1's "no
task on the stack"), neither modelled nor unmodelled. (The 24 September follow-up ruling called the idle stand
unmodelled; under T-H a stand the script writes is the `stand` task, `TASK_ABSENT`, and the empty stack has no
coverage.) Coverage is judged per task instance on the stack: an interrupted delivery is `COVERED`, its interruption is
judged on its own.
Coverage is judged against the robot's task model and the run's layout and setup, not against the support that `--assignment_prior`
narrows. The prior is part of the belief, not of the model, so a prior-on and a prior-off run of the same script have
the same ground truth. Consequence: under prior-on, an unassigned `WorkTask` instance is modelled, and its hypothesis
is suppressed by the prior; a belief-side matter.
"Model coverage" is unrelated to the covered fraction f of **graded evidence** (§5, `covered_fraction`). Say
"coverage" for label B and "covered fraction" (or "the grade", f) for the evidence, never one for the other.

**label C, purpose** — a property of the scenario, not of one behaviour: what the scenario's description says it is
for, as text (e.g. "an unmodelled walk mid-delivery"). The author declares the purpose and the scenario's two
bindings, its setup and its reference layouts (§9, T-L); what the script contains is still computed (**scenario
composition**, **scenario coverage**, below), never declared, so no tag can drift from the script. CHANGED (T-H follow-up, 26 September 2026): label C was "experimental intent", with the value "declared
experimental condition"; it is now the purpose alone, and "condition" no longer names it (the word keeps its other
meanings: an evaluation condition such as the prior or the oracle, and a predicate condition of a schema).
An unmodelled behaviour in the record that the purpose does not cover means that the run contains unintended
unmodelled behaviour. The check excludes the **exit walk** (below; the authoring convention's terminal `go_to` to the
door or a corner, §6, **human's script**): the convention declares it for every scenario. The terminal stand at a
table (TODO-80) is not declared by the convention and stays a label-C mismatch unless the scenario's purpose states
it.

**scenario composition** — what a scenario's script is made of, against one observing robot: four sets of existing
types, no new words. The task classes it names (`WorkTask`, `PersonalTask`, `HumanOnlyTask`), over `Script.tasks()`
(each entry's task and each `Start`'s); its decisions (`Start`, `Drop`) and its triggers (`AfterAction`,
`DuringAction`; `Now` never appears in a script), over the entries' events; and the coverage results of its tasks
(`Covered`, `TaskAbsent`, `BindingAbsent`; label B), over `Script.tasks()`. Computed at load, never stored on the
`ScenarioConfig`. What a selector for batch runs or the viewer reads (TODO-110, not built).

**scenario coverage** — label B lifted from one task to the scenario: `MODELLED_ONLY`, `TASK_ABSENT`,
`BINDING_ABSENT` or `BOTH`, by which non-covered results its tasks have (the composition's coverage set, less the exit
walk). It depends on the robot's task model, so it is a property of the run configuration, not of the script: a task
model without `coffee_break` moves scenario_s02_02 from `MODELLED_ONLY` to `TASK_ABSENT`. The same with the prior on and off. It
states what the script contains, never what the scenario is for (that is the purpose).
ONE EXEMPTION, stated here only: the **exit walk**, the script's last entry when its task is a `HumanOnlyTask` whose
only goal binding (§6, **task equality**) is a landmark, that decomposes to exactly one movement action to that
landmark (every method of its schema: one action step, whose action declares a movement target bound to the
landmark), and that carries no events, is not counted. A rule on type, structure and position, never on a schema's
name: `go_to("door")` or `go_to("corner_SE")` last is the exit walk; the same walk earlier in the script, or carrying
an event, is counted, and so are a terminal `stand` (no landmark; TODO-80) and a terminal `go_to_and_stand` (a walk
and a stand: `TASK_ABSENT`).
AS BUILT: `world/composition.py`, `scenario_composition(script, robot) -> (Composition, ScenarioCoverage)`; the
`[scenario-coverage]` line at load, one per observing robot, after its `[coverage]` lines; the listing
`mesa_sim/list_scenarios.py`.

"Scripted" is not a behaviour class: every behaviour in the simulator is scripted. Use "scripted" only to
contrast simulation with a real deployment.

ROBOT: what the robot's mind holds and decides. Unchanged by T-H.

**recognizer belief** — a distribution over the live **task hypotheses** (one per `HypothesisKey`, §5) and
`unknown`. The recognizer emits it and gates nothing.
SUPERSEDED IN PART (T-D R, 27 September 2026): "and `unknown`": the belief is normalised over the live task hypotheses only (R1); the adequacy finding is a separate output (R2, R3). design_decisions.md, "T-D R and E".

**`unknown`** — HISTORICAL (T-D R1, ruled by Hadi, 26 to 27 September 2026): the `unknown` hypothesis leaves the
hypothesis space; the belief is normalised over the live task hypotheses only, and u, `graded_unknown_likelihood` and
the grade f leave the belief. Of the four readings its share carried, evidence against every live task hypothesis goes
to the **adequacy finding** (below), the mass left at exhaustion to the lifecycle state **exhausted** (below), and a
stand enters adequacy only (E3). The text below describes the recognizer as built until the T-D Stage 1 build; so do
the mentions of `unknown` and u in §5 (**hypothesis**, **graded evidence**, **pin** / **episode boundary**, **β, u, ρ**)
and in **recognizer belief** above. → `docs/design_decisions.md`, "T-D R and E: the recognizer's output under a
removed `unknown` hypothesis".
The residual hypothesis: the hypothesis that the behaviour is none of the task hypotheses. Always
live; its likelihood is the reference u (`UNKNOWN_LIKELIHOOD`, §5), and it takes no factor of its own. Written in
code font. The constant `UNKNOWN` and the identifiers keep their names. Its mass is a quantity of the belief, not
a label of the world. It rises from walked excess path, and it is also high BY NORMALISATION when few task
hypotheses are live: it holds 1/|Live| after every **episode boundary** (§5), and 0.995 once every assigned task is
done (prior on).
→ `docs/recognizer_handback.md` §1.1, §1.5.
SUPERSEDED IN PART (E10, 1.5 rulings, 27 September 2026): "a stand enters adequacy only (E3)": standing beyond a phase's
priced duration enters the belief through L(v·D) as well as adequacy through S(v·D). design_decisions.md, "T-D R and E",
"1.5 rulings".

The entries below are ruled (T-D R and E, 27 September 2026) and built (T-D Stage 1, 27 September 2026); **hypothesis
adequacy** is ruled in the 1.5 rulings (G1) and built in cycle 1.5b.

**adequacy finding** — the recognizer's second output, beside the **recognizer belief** (R2): one of three values,
**unresolved**, **adequate** or **unexplained**, with the **tail probabilities** S_k (§5) of the live hypotheses beside
it, for evaluation. It answers what the belief's relative test cannot express: whether the best of the robot's models
is wrong. Belief and finding are independent outputs (R3); the recognizer's state is their product plus the lifecycle
state (**exhausted**, below); their combinations are examples of what the outputs jointly express, not a state machine,
and no transitions are defined. Each live hypothesis is assessed against its own **derived phase** (§5) by its
**projected completion delay** (§5), at the **test level** α (§5). The finding has no memory beyond each live
hypothesis's current derived phase: it clears when every live hypothesis advances its phase or an episode boundary
moves every origin (E7). The recognizer decides nothing about action with it (R5); the meta-planner receives the
categorical finding, and what it does with it is G and X, open. A ROBOT term: it is not model coverage (label B), and
the two can disagree.
→ `docs/design_decisions.md`, "T-D R and E: the recognizer's output under a removed `unknown` hypothesis", R2 to R5,
E1 to E7.
RULED (1.5 rulings, 27 September 2026; built in cycle 1.5b, amended in 1.5c). MEMBERSHIP (E6 as amended twice, E8): a
live hypothesis is a member on a tick iff its derived phase holds an observation — walked path since its origin;
standing beyond s_exp; a stationary tick with s ≤ s_exp in a stationary phase or in any phase with s_exp > 0 (D ≤ 0,
S_k = 1; this covers the latency tick E9 prices to a walk entered from a completion); or, on the tick at which its
expected action completes, the completion (E8: S_k = 1, whatever phase it advances into) — and the tick is not a
boundary tick: no hypothesis is a member on a boundary tick (E8's boundary clause applied generally). At a boundary the
sequence is unresolved (b), adequate (b + 1, the latency tick), adequate; only the initial walk at step 0
(s_exp = 0) stays unresolved until walking evidence occurs. PER-HYPOTHESIS ADEQUACY (G1): beside the finding the recognizer reports, per live
hypothesis, a categorical value: adequate (a member with S_k ≥ α), inadequate (a member with S_k < α) or no
observation (not a member). The finding is existential over the live hypotheses; the per-hypothesis value answers
whether one hypothesis explains its own phase, and the meta-planner reads it for the leader at admission
(**admitted**), never α or S_k. Its term is **hypothesis adequacy** (below).
→ the same entry, "1.5 rulings", E8, G1.
RELATION TO HYPOTHESIS ADEQUACY (ruled by Hadi, 27 September 2026): the aggregate adequacy finding is **adequate** when
at least one live hypothesis has hypothesis adequacy adequate; otherwise it is **unresolved** (no live hypothesis is a
member) or **unexplained** (every member is inadequate), by the aggregate rule (E4, E6).
SUPERSEDED IN PART (wording; TB.1r, Hadi, 27 September 2026): "it clears when every live hypothesis advances its phase
or an episode boundary moves every origin (E7)" was loose. The finding has no memory beyond each live hypothesis's
current derived phase; it is recomputed every tick; one member with S_k ≥ α makes it adequate; a boundary empties the
membership. No change to the mechanism.
→ `docs/design_decisions.md`, "T-D R and E", E7 (its superseding note); `docs/recognizer_handback.md` §1.10.
AMENDED (T-D G, AD2, ruled 29 September 2026; to be built in G-build): **warrant** (below) is a third independent
output beside the belief and the finding (R3 as amended); it is not a kind of adequacy. design_decisions.md, "T-D G:
admission".

**hypothesis adequacy** — per live hypothesis, a categorical value the recognizer reports beside the **adequacy
finding** (G1): **adequate** (a member of the test with S_k ≥ α), **inadequate** (a member with S_k < α) or **no
observation** (not a member: its derived phase holds no observation this tick, or it has no derived phase). It answers
whether one hypothesis explains its own derived phase; the finding is its existential aggregate over the live
hypotheses (above). The meta-planner reads it for the leader only, at admission (**admitted**), and never receives α
or S_k. Membership is the complete rule of E6 (as amended twice, with E8; **adequacy finding**, above).
→ `docs/design_decisions.md`, "T-D R and E", E6, "1.5 rulings", E8, G1.

The four entries below are ruled (T-D G, 29 September 2026) and built in G-build (29 September 2026).

**warrant** — commitment or observation that justifies admission: the third condition of the gate (AD1), beside θ and
the leader's **hypothesis adequacy**. Two sources, **commitment warrant** and **observation warrant** (below). A third
independent dimension beside the **recognizer belief** and the **adequacy finding** (AD2, R3 as amended): not a kind
of adequacy. Adequacy says a hypothesis is not contradicted in its derived phase; warrant says it has earned
admission. Warrant is not the support restriction: "the support" keeps its meaning, the hypotheses admissible under
the assignment prior (the observed human's assigned tasks plus the foreseeable tasks).
→ `docs/design_decisions.md`, "T-D G: admission", AD1, AD2.

**warranted** / **unwarranted** — a hypothesis has warrant, from either source, or has none. The gate refuses an
unwarranted leader (`none(leader_unwarranted)`, checked after `none(leader_inadequate)`, AD4). Loss of observation
warrant fires nothing and clears no admitted projection; retraction stays on inadequacy (AD3, L2 (ii)).
→ the same entry, AD3, AD4.

**observation warrant** — a hypothesis's current derived phase (§5) holds evidence for it: for a phase with a movement
target (`move_to`), the path-cost gain toward the target since the phase origin is positive, C(o, g) − C(p, g) =
w − e > 0 (the quantities of the excess-path statistic); for any phase, the phase was entered by the observed
completion of the hypothesis's previous step in this episode (the completion E8 reads), the only source for a phase
without a movement target (`pick_up`, `place`, `wait_at`). Reset with the origins, at a boundary and at a phase change.
Reported by the recognizer per live hypothesis on `BeliefState`, printed `warrant=none|observation` on `[IR]`.
→ the same entry, AD1, AD2, AD4.

**commitment warrant** — the hypothesis is one of the observed human's assigned tasks (prior on), matched by task
equality (`same_task`) as the support restriction matches them. Not reset: it derives from the assigned tasks, which
the meta-planner receives as an input; the recognizer never prints it. Prior off there is none. An assigned task is a
known commitment (`docs/assumptions.md` 2.2, 2.6) that warrants projecting it before movement; a deviation is handled
by retraction.
→ the same entry, AD1, AD2.

**unresolved** — the value of the **adequacy finding** while no live hypothesis is a member of the test: no live
hypothesis's current derived phase holds an observation (E6, as amended twice). A phase holds an observation once it
holds walked path since its origin, or standing beyond the priced standing s_exp, or a stationary tick with s ≤ s_exp
in a stationary phase (`pick_up`, `place`, `wait_at`) or in any phase with s_exp > 0 (D ≤ 0, S_k = 1: the latency tick
a walk entered from a completion is priced); and, on the tick a hypothesis's expected action completes, that
hypothesis is a member with S_k = 1 (E8). No hypothesis is a member on a boundary tick (E8's boundary clause applied
generally), so the boundary tick is unresolved and the latency tick after it adequate; the initial walk at step 0
(s_exp = 0) with nothing walked holds no observation and stays unresolved until walking evidence occurs; a hypothesis
with no derived phase is never a member. An observation whose projected completion delay is not surprising is still an
observation. No band, no constant. The log reason `none(unprojectable)` (the projector could not resolve the admitted
hypothesis's task; `none(unresolved)` before the Stage 1 build) is log text with its own meaning, not this word.
→ the same entry, E6 (amended twice, and the complete membership rule), "1.5 rulings", E8.

**adequate** — the value of the **adequacy finding** when some live hypothesis's current derived phase holds an
observation and not every live hypothesis has S_k < α: at least one live hypothesis explains its phase at the test
level (E4). It says nothing about which hypothesis leads (that is the belief) and is not admission (that is the
meta-planner's gate, **admitted**).
→ the same entry, E4.
AMENDED (T-D G, 29 September 2026): adequate is not **warrant** (above): a hypothesis can be adequate (not
contradicted) with nothing observed for it, and admission also requires warrant (AD1). design_decisions.md, "T-D G:
admission".

**exhausted** — the recognizer's lifecycle state when no task hypothesis is live (R4): every hypothesis retired. No
finding is reported in it, and nothing is unexplained in it. It replaces the reading "`unknown` at 0.995" (a finished
set of assigned tasks, prior on). A ROBOT term: the world's counterparts (every assigned task done, the empty stack)
are ground truth read from the record and can differ from it.
→ the same entry, R3, R4.
AMENDED (T-D L4, ruled 27 September 2026, built in L-build): exhausted is about the current world — no hypothesis of
the support whose terminal fact does not hold on this tick — and becomes rare: a foreseeable task is live again once its
fact clears, so after the work order the live set is the foreseeable tasks and the exit walk reads **unexplained**.
design_decisions.md, "T-D L: the belief lifecycle", L4.

**unexplained** — the recognizer's finding that it has evidence that no live task hypothesis explains the
observations. A finding about evidence, not a value of the belief. `unknown` can be high with nothing unexplained
(every assigned task done, by normalisation). A stand adds no evidence of its own (I4c: an empty stretch is no
observation). A live hypothesis in a no-graded-signal phase (`wait_at`, `pick_up`, `place`) receives one fitting
observation, 1/u, for that phase, whether or not the human performs that task. So an unmodelled stand can support a
hypothesis whose current phase happens at that place, and it is not unexplained; otherwise it changes nothing,
however long it lasts. (`shared/recognizer.py`: `_progress_likelihood` returns the perfect fit for a phase with no evaluator (lines 865-866) and `None` for an empty stretch (870-871); `_unknown_likelihood` returns the ungraded u for it (903-904); the open term (638-641) and the fold at a phase change (623-631).) The recognizer has no separate output for it today; how it is represented belongs to the
pending decision on `unknown`. The evidence window the finding is judged over (every observation since the episode
began, or only the current ones) is not yet defined; it is the retraction question (T-D Q2) and part of that
decision.
RULED (T-D R and E, 27 September 2026): unexplained is a value of the **adequacy finding** (above), reported only
when every live hypothesis has S_k < α in its own derived phase (E4), and never in the lifecycle state **exhausted**
(R4). The "pending decision" and the evidence window named in this entry are settled by it: the window is each live
hypothesis's current derived phase (E1, E7); retraction and resumption are L. The mechanism described in this entry
(1/u for a no-graded-signal phase, a stand adding nothing) is the recognizer as built until the Stage 1 build; under E a
stand in a `move_to` phase counts for adequacy beyond s_exp = 0 (E3, E6).
→ `docs/design_decisions.md`, "T-D R and E: the recognizer's output under a removed `unknown` hypothesis".
SUPERSEDED IN PART (E10, 1.5 rulings, 27 September 2026): "a stand adds no evidence of its own" and a stand counting
"for adequacy" only: standing beyond a phase's priced duration enters the belief through L(v·D) as well as adequacy
through S(v·D); a stationary tick within the priced standing is not a charge (I4c narrowed). design_decisions.md,
"T-D R and E", "1.5 rulings".

**admitted** — the meta-planner's gate outcome: a task hypothesis cleared θ at admission and its projection was
built (`[meta-proj] projection=built`). `unknown` above θ is never admitted (`none(unknown)`). The gate is the
meta-planner's, not the recognizer's (**θ**, §5).
→ `shared/meta_planner.py`, `update_human_projection()`.
SUPERSEDED IN PART (T-D R1, 27 September 2026): the `unknown` route no longer exists; its replacement is G. Not closed: the downstream response is G and X. design_decisions.md, "T-D R and E".
RULED (G1, 1.5 rulings, 27 September 2026; to be built in cycle 1.5b): admission also requires the leader to be adequate in
its own derived phase: the leader is a member and S_leader ≥ α, read by the meta-planner as the categorical
per-hypothesis adequacy (**adequacy finding**), never α or S_k. `_clears_gate` stays the one home of the rule, so
`recognition_changed` fires and refuses on the same condition; a refusal behaves as below θ. The first ruling of G.
design_decisions.md, "T-D R and E", "1.5 rulings".
AMENDED (T-D G, AD1, AD4, built in G-build, 29 September 2026): admitted means the leader cleared θ, was adequate in its
own derived phase and was **warranted** (commitment or observation, above), and its projection was built
(`[meta-proj] projection=built warrant=<commitment|observation|commitment,observation>`). An unwarranted leader is
refused (`none(leader_unwarranted)`, after `none(leader_inadequate)`); losing warrant after admission changes nothing
(AD3). design_decisions.md, "T-D G: admission".

USAGE RULE, in prose:
- about the implementation: "the `unknown` hypothesis";
- about the human's behaviour: "unmodelled behaviour";
- about the robot's inference result: "unexplained".
Unmodelled (ground truth) and unexplained (the robot's finding) can disagree at a given time; that disagreement
is why both terms exist. Not written: "unknown behaviour", "an unknown task", "`unknown` as unmodelled behaviour".
INTRODUCED BY T-D R AND E (27 September 2026), replacing the "not introduced" note of 24 September: "unresolved" and
"exhausted" are terms (**unresolved**, **exhausted**, above), with **adequacy finding** and **adequate**. "Recognised"
stays not a term: it would suggest that the recognizer performs the θ gate. The log reason `none(unprojectable)`
(`none(unresolved)` before the Stage 1 build) is log text with its own meaning (the projector could not resolve the admitted hypothesis's task), not the finding's value
**unresolved**.

---

## 8. Sessions

**cchat** — the design chat with Hadi, where design is decided. **ccode** — the Claude Code session
in the repository, which builds and checks; older reports call it Fable.
→ `CLAUDE.md`, "Conventions and terminology".

**T-A … T-H** — the plan names task prompts and reports use (T-H, the human behaviour model, runs before T-D; T-H1 to
T-H4 its build).
→ `docs/roadmap.md`, "The plan from T-A".
**T-L** — the refactor of layouts and scenarios into three artefacts (§9), before T-D; stages 1 to 4.
→ `docs/design_decisions.md`, "Layouts, setups and scenarios: the three artefacts of a run".
**TB** — the IR test-bed track (ruled 27 September 2026), before cycle 2 of T-D: the recognizer tested in isolation,
on a layout, setup and scenarios written for it, against expectations derived from the entry "T-D R and E" before the
run. Sessions TB.1r (records), TB.2b (the cognitive-loop correction), TB.3b (the artefacts, the expectation generator,
the runs, the report).
→ `docs/design_decisions.md`, "The IR test-bed" and "The cognitive loop does not end with the task pool".

---

## 9. Runs: what a run is made of

Ruled by Hadi, 26 September 2026 (T-L). Built in T-L's stages 1 to 4 (26 September 2026); before them the code held
one layout JSON per room and shift, and a registry that bound each scenario to one layout. The definitions are domain-neutral; kitting and
dock_loading appear as examples only.
→ `docs/design_decisions.md`, "Layouts, setups and scenarios: the three artefacts of a run".

**layout** — the room: the space, its zones, and the fixed objects with their positions, a fixed container
included. No movable object and no agent. Static. One file per layout, with a serial id (`env_layout_KK`, KK a serial
with no meaning beyond order of writing; ruling 4 as amended, 26 September 2026). (Kitting: tables,
shelves, machines, switches, landmarks; dock_loading: bays, the gate, and the truck, a fixed container of the room as a
shelf is.)
Until T-L's stage 1 the layout JSON also held the setup's objects and dead agent spawn entries.

**setup** — the shift: the movable objects that exist, each with its home container and, where the domain determines
one through `destination_of`, its designated destination, and any other initial state the domain declares per movable
object. Its container and destination ids name objects of a layout: a home container must exist in the layout; a
designated destination must also have the type the schema declares for it. A different designation set is a different
setup. One file per setup, with a serial id (`env_setup_NN`; ruling 4 as amended).
(Kitting: the items, each on a shelf with its designated table; dock_loading: the pallets, with `subtype`, `is_empty`,
`is_scanned`.) A new term.
COLLISION, not resolved: DESIGN-16 (`docs/design_decisions.md`) says "travel/setup costs between tasks", the
scheduling sense (a cost of switching between tasks). That is the English word, not the term.

**scenario** — the episode: per agent its `start_position`, `assigned_tasks`, `observes` and, for a human, the
human's script; the purpose, as description text (label C, §7); the one setup it binds (`setup`, required); and its
reference layouts. A hand-written `ScenarioConfig` literal, registered by discovery at import of the domain package.
Its id equals its Python variable: `scenario_sNN_MM` (ruling 4 as amended), NN its setup's serial — a repetition of the
validated `setup` field, an authoring convention the code does not check; an author who moves a scenario to another
setup renames it — and MM a counter per setup. No layout serial is in it (a scenario has one or more reference
layouts), and nothing about the script's content. Its assigned tasks and script state the
table explicitly (a readability choice, not required by the model), checked against the setup's designations: a
scenario fits a setup whose designations agree with its stated tables.
→ `shared/types.py`, `ScenarioConfig`.

**reference layout** — a layout a scenario declares it runs on (`reference_layouts`, one or more). A binding the
author makes, validated at load. A run whose run file names no layout runs the scenario's first reference layout;
`--layout` selects another registered layout (selection, not an override). A run on a layout outside the reference
layouts is valid and is never a baseline; to make it one, the author adds the id. The listing and batch runs enumerate
the declared (layout, scenario) pairs, never the product of artefacts.

**run** — a triple (layout, setup, scenario) plus the run facts: gate, cost strategy, strategy, prior, separation
stop, and the robot's task model (an evaluation condition chosen by whole schemas, §6; its default in the domain
registry). θ is a constant, not a run fact. Validated at load before anything is built; the load-time replay follows.
The triple is printed on the `[run_mesa]` start line. Baselines are keyed by the run: the layout id and the scenario
id, plus the run options present; the setup is implied by the scenario (one setup per scenario).

**run file** — a yaml (`configs/experiment.yaml`, or any yaml given by path) that states a run: the triple, the run
options and an overrides block. It may name all three artefacts; when it omits the layout, the scenario's first
reference layout is run. The viewer reads and edits the same file. `--run <path>` names another.
→ `mesa_sim/run_mesa.py`, `load_experiment()`; `mesa_sim/viz/run_file_panel.py`.

**override** — a change to one fact of a run's artefacts, applied at load before validation, from the run file's
overrides block or `--override <path>=<value>`. A closed list of three: an agent's `start_position`; a fixed
object's position (a movable object's position is its container's); a movable object's home container. Not
overridable: `assigned_tasks` (a variant is a new scenario), a designated destination (a different designation set is
a different setup), the script, and every id inside an artefact: an object's own id, its identity. A reference held
as a value (the container id in a movable object's home container) may be overridden; the override changes which
object is referenced, not what any object is. Choosing the layout is selection, not an override. Each override is printed as one line next to the triple in
the run log. A run with an override is never a fixture or a baseline. Not an injection: a change during a run is Phase
7's injection path (**inject**, §6). A path is `<artefact>.<id>.<fact>` (`scenario.<agent>.start_position`,
`layout.<object>.position`, `setup.<object>.initial_container`), read into a typed class at the input boundary.
→ `mesa_sim/overrides.py`; `mesa_sim/sim_model.py`, `SimModel.__init__` (where they are applied).

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
