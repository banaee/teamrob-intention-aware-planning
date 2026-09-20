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

**candidate** — the unit the argmin ranges over. An individual task under `single_task`; one
ordering under `full_reorder`. Candidates exist only inside B3; forming them from the pool is B3's
private business.
→ `docs/design_decisions.md`, DESIGN-16, "Terminology, fixed"; `shared/io_contracts.md` §2.2,
"Strategy (DESIGN-16)".
COLLISION, not resolved: the older TODO entries use "candidate" as the ordinary adjective — "candidate
fix", "candidate formulas", "candidate remedy". That is the English word, not the term.

**head** / **tail** of an ordering — its first task, and everything after it. Under `full_reorder`
the head becomes `current_task` and the tail is lookahead only: it carries no order commitment and
is re-priced at the robot's next boundary.
→ `docs/design_decisions.md`, "B3.B (`full_reorder`) is lookahead for the choice of the next task,
built next", point 4. (Used in prose; not separately defined there.)

**single_task** / **full_reorder** — B3's two strategies (B3.A and B3.B). `single_task` is the
default and the implemented one; `full_reorder` is designed and is T-B's build.
→ `shared/meta_planner.py`, module docstring, STRATEGY; `docs/design_decisions.md`, DESIGN-16.

**B1 / B2 / B3** — the blocks of `MetaPlanner.update()`: B1 the human projection, B2 the mid-task
commitment gate (`b2a` built, `b2b` a stub), B3 selection on realized cost.
→ `shared/meta_planner.py`, module docstring, "BLOCK STRUCTURE OF update()".

---

## 2. Projection: what a plan looks like before the human is considered

**projection** — turning a task, or an ordering, plus a `WorldState` into a predicted trajectory.
Agent-agnostic: the same call projects a robot candidate and the human's predicted task.
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
Do not call a segment a "leg" or a "stretch of evidence"; those are the recognizer's.
→ `shared/types.py`, `Segment`; `shared/io_contracts.md` §1.7.
COLLISION, not resolved: scenario_40's human script is described as four numbered "segments" (1, 2,
3a, 3b, 4) in `domains/kitting/env_layout4.json`, `domains/kitting/scenarios.py` and every I4 / F47
report that cites them. That is a PART OF A SCRIPT, not a `Segment`. It was left alone because
renaming it would make the record's "segment 3b" unreadable. New text says "script part".

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
observed human at this trigger, projected exactly as a robot candidate is. It ends at **T_h**.
Admission is logged as `[meta-proj]`; there is at most one, and there may be none.
→ `shared/meta_planner.py`, `update_human_projection()`; `shared/io_contracts.md` §2.2.

**T_h** — the end of the human projection: its last segment's end step. Nothing past T_h is
assessed or charged.
→ `shared/io_contracts.md` §1.11, `RealizedPlan.horizon`.

---

## 3. Realization: what a plan costs once the human is in it

**realization** — what a projected trajectory actually is, given the human. It computes the hold the
robot must take to keep `min_separation` from the human projection, and the realized duration
T_r + δ is the candidate's cost. Conflict becomes cost by construction; there is no conflict weight
and no exclusion threshold. Since F1 realization is TOTAL: every plan realizes and every candidate
has a cost.
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

**minimal-shift search** — given a set of violating shift intervals and a lower bound b, the
smallest whole tick ≥ b that lies inside none of them. It is the loop inside `realize()` today, with
b = 0: δ starts at 0 and, whenever an interval strictly contains it, jumps to the first whole tick
at or after that interval's end, the intervals taken in order of their start. Not a bisection and
not a grid — feasibility in the shift is not monotone, so the whole-tick answer is NOT the
fractional minimum rounded up. The repo had no name for this; this one is new.
→ `shared/realization.py`, `realize()`; `shared/io_contracts.md` §2.2c.

**hold** — the shift that was chosen, as a number of ticks in which the robot stands still (δ,
`RealizedPlan.delta`). It is taken at the robot's position at the decision step, it is executed as
STAND ticks one per tick, and it is logged as `[hold]`. There is no hold cap.
→ `shared/io_contracts.md` §1.11; `mesa_sim/executor.py`, `hold()`.
NOTE: a stationary `Segment` that is NOT a chosen shift — a grasp, a wait, a completion latency — is
a "stationary stretch" or "stationary segment", not a hold.

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

**trigger** — the condition on which `MetaPlanner.update()` re-decides. Three, and only three:
- `no_current_task` — there is nothing running.
- `recognition_changed` — the belief no longer points at the hypothesis the last decision projected,
  or first clears the gate on one. Replaced `theta_crossed` at D2; older reports and logs still name
  `theta_crossed`.
- `task_committed` — the ROBOT's own grasp, not the human's commitment.
→ `shared/meta_planner.py`, `evaluate_triggers()`; `shared/io_contracts.md` §2.2.

**decision record** — one field: the hypothesis the last fired trigger's decision was projected
against. `recognition_changed` is read against it from both sides.
→ `shared/meta_planner.py`, `_projected_hypothesis`; `shared/io_contracts.md` §2.2.

**boundary** (robot) — a tick at which the robot re-decides freely: `task_committed` or
`no_current_task`. Distinct from the recognizer's **episode boundary** below; the two are unrelated.
(Used in prose; not separately defined.)

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

**leg** — the recognizer's older word for a human walk, still used in prose for a scripted walk of
the human's script ("the two AC-switch legs"). The leg MODEL — one global movement leg for all
hypotheses, closed by stillness — was removed and must not return; the unit is the stretch.
→ `CLAUDE.md`, "Conventions and terminology"; `docs/recognizer_handback.md` §8.

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

---

## 7. Sessions

**cchat** — the design chat with Hadi, where design is decided. **ccode** — the Claude Code session
in the repository, which builds and checks; older reports call it Fable.
→ `CLAUDE.md`, "Conventions and terminology".

**T-A … T-G** — the plan names task prompts and reports use.
→ `docs/roadmap.md`, "The plan from T-A".

---

## Not in this glossary

**trajectory** is used throughout (`realization.py`, `projection.py`, `io_contracts.md`) and is
defined nowhere. It is not given a meaning here, because inventing one is a design act.
