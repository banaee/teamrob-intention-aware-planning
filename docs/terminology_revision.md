# Terminology revision: human behaviour, model coverage and the robot's inference

Companion to `docs/glossary.md` §7. It explains, and the glossary decides: where the two differ, the glossary is
right and this file is to be corrected. Ruled by Hadi on 24 September 2026; recorded in `docs/design_decisions.md`,
"Terms for human behaviour, model coverage and the robot's inference".

REVISED BY T-H (25 September 2026; `docs/design_decisions.md`, "T-H: the human behaviour model"). Sections 1 to 7 are
the explanation as ruled on 24 September and are kept as written; section 8 states what T-H changes in them. Read
"work order" as "assigned tasks", and the WORLD labels as the queries of section 8. The ROBOT group is unchanged.

Why the terms exist. "Unknown" named two things:
- (a) a property of what the human does in the world: the behaviour is outside the robot's models;
- (b) the robot's belief: the mass on the residual hypothesis `unknown`.

The two diverge. A stand adds no evidence of its own, so (a) holds and (b) does not move. A
finished work order leaves `unknown` near 0.995 by normalisation while nothing is unexplained, so (b) is high with no
evidence behind it. The
next design decision, whether `unknown` stays in the Bayesian hypothesis space, has to be stated in terms that
keep them apart. This file fixes those terms. It does not prejudge that decision (section 6).

Numbers below are illustrations from the T-C play (`analysis/tc2c_scripts/`, code at feabe3d, prior on). They
show what the terms separate. They are not a reference for any design argument.

---

## 1. The two groups

Two groups, WORLD and ROBOT. A term from one group is never used for the other.

```
WORLD   ground truth about the observed human's behaviour
        computable from the scenario's script and the robot's hypothesis space
        never received by the robot's mind

ROBOT   what the robot's mind holds and decides
        computed from observations only
```

### 1.1 WORLD: three independent labels

```
WORLD
|
+-- label A: work order          (a behaviour compared with the human's assigned tasks)
|     |
|     +-- assigned task
|     +-- deviation              (any departure from the work order)
|            ^        ^        ^
|            |        |        |
|        produces  produces  produces        the script edits are OPERATIONS,
|            |        |        |             not kinds of deviation
|       interrupt   deviate   abandon        (free Stay / MoveTo(landmark) content
|                                             departs from the work order too)
|
+-- label B: model coverage      (a behaviour compared with the robot's hypothesis space)
|     |
|     +-- modelled behaviour     (a HypothesisKey describes it)
|     +-- unmodelled behaviour   (no HypothesisKey describes it)
|
+-- label C: experimental intent (a property of the SCENARIO, not of one behaviour)
      |
      +-- declared experimental condition   (written in the scenario's description,
                                             e.g. "unmodelled-behaviour condition")
```

Every behaviour has one value on label A and one on label B. The two are independent. The foreseeable task is
where a deviation meets a model: a task in the hypothesis space that is not assigned. It is a combination of the
two labels, not a third value of label A.

```
                        label B: modelled                 label B: unmodelled
                    +---------------------------------+---------------------------------+
 label A: assigned  | an assigned delivery            | (none in kitting: every         |
 task               |                                 |  assigned task has a hypothesis)|
                    +---------------------------------+---------------------------------+
 label A: deviation | FORESEEABLE TASK                | wrong-table delivery            |
                    | (a coffee_break interrupt       | walk to corner_NE               |
                    |  declared foreseeable)          | a stand of 5 minutes            |
                    +---------------------------------+---------------------------------+
 label A: no value  |                                 | the idle stand after the        |
 (work order        |                                 | finished work order             |
  finished)         |                                 |                                 |
                    +---------------------------------+---------------------------------+
```

Label A applies only while the work order has open tasks; once it is finished, label A has no value (the last row).

Coverage is judged at the hypothesis level: not at the schema level, and not by provenance.

```
                          provenance        schema in the domain   a HypothesisKey describes it   label B
coffee_break interrupt    coffee_break      yes                    yes                             modelled
wrong-table delivery      deliver_item      yes                    no (the hypothesis carries      unmodelled
(TODO-87)                                                           the designated table)
```

Coverage is judged against the full hypothesis space H (`build_hypothesis_space()`), not against the support that
`--assignment_prior` narrows: the prior is part of the belief, not of the model, so prior-on and prior-off runs of
the same script have the same ground truth. Under prior-on an unassigned, non-foreseeable task is therefore
modelled, and its hypothesis is suppressed by the prior; that is a belief-side matter.

"Model coverage" is unrelated to the covered fraction f of graded evidence (`covered_fraction`, the share of one
hypothesis's expected path a stretch has closed). f lives inside the robot's evidence; coverage is a world label.

"Scripted" is not a behaviour class: in the simulator every behaviour is scripted. The word only contrasts
simulation with a real deployment.

### 1.2 ROBOT

```
ROBOT
|
+-- recognizer: belief           a distribution; gates nothing
|     |
|     +-- task hypotheses        one per HypothesisKey in the live set
|     +-- `unknown`              the residual hypothesis: the behaviour is none of them
|
+-- recognizer: finding
|     |
|     +-- unexplained            evidence that no live task hypothesis explains the observations
|
+-- meta-planner: gate outcome   theta, asked in _clears_gate() only
      |
      +-- admitted               a task hypothesis cleared theta; its projection is built
                                 (`unknown` above theta is never admitted: none(unknown))
```

The recognizer has no separate output for "unexplained" today. How the finding is represented is part of the
pending decision on `unknown` (section 6). The term fixes what it means, not how it is computed.

### 1.3 The usage rule

```
you are writing about ...            write ...
the implementation                   "the `unknown` hypothesis"
the human's behaviour                "unmodelled behaviour"
the robot's inference result         "unexplained"
```

Not written: "unknown behaviour", "an unknown task", "`unknown` as unmodelled behaviour".

---

## 2. The cases

Label A and label B are the world. The belief column is what the current recognizer does, from the play or the
fixtures named. The finding column applies the definition of "unexplained" to that behaviour of the belief.

| case | label A | label B | belief (current recognizer) | finding |
|---|---|---|---|---|
| an assigned delivery (`deliver(item_3)`) | assigned task | modelled | its hypothesis rises along the walk and clears θ at about half of it; admitted | nothing unexplained |
| a `coffee_break` interrupt declared foreseeable (`interrupt(..., with_=[coffee_break])`) | deviation, produced by `interrupt` | modelled (a foreseeable task) | `coffee_break` rises on the walk to the machine (scenario_11: 0.345), unless an earlier misleading walk refuted it (scenario_41: `coffee_break` ≤ 0.001, `unknown` 0.453; TODO-94) | nothing unexplained in scenario_11; in scenario_41 (modelled, suppressed by earlier evidence): undecided, depends on the evidence window (pending decision, T-D Q2) |
| a wrong-table delivery (`deviate(deliver(item_0), destination=kitting_table_1)`, TODO-87) | deviation, produced by `deviate` | unmodelled | the item's delivery leads while the carry still fits it; `unknown` leads once the carry wastes path; no pin, no boundary at the place; after the next boundary the item's delivery leads again (scenario_85, section 3.3) | unexplained only in the middle stretch; not before, not after |
| a walk to corner_NE (`MoveTo("corner_NE")`) | deviation (free primitive) | unmodelled (a landmark: no hypothesis binds one) | `unknown` rises with walked excess path and leads (0.99 in the play's long detours); a walk that stays in line with a live hypothesis does not raise it (scenario_04's walk to the door: the one live hypothesis at 0.58 to 0.61) | unexplained (when the walk wastes path against every live hypothesis) |
| a human standing for 5 minutes (`Stay(n)`) | deviation (a stay the work order does not contain) | unmodelled (no hypothesis describes standing) | frozen where the last walk left it: mid-carry, the carried item's delivery on top (TODO-85); after a boundary, the uniform prior; `unknown` does not rise (I4c) | nothing unexplained: a stand adds no evidence of its own |
| a finished work order, idle human | none (work order finished) | unmodelled (no `HypothesisKey` describes a stand) | `unknown` about 0.995 by normalisation: no task hypothesis is left live (scenario_01, prior on); not admitted, `none(unknown)` | nothing unexplained |

The coffee row in scenario_41 is a pattern of its own: MODELLED, SUPPRESSED BY EARLIER EVIDENCE. The `coffee_break`
hypothesis is live and fits the walk to the machine, but the earlier walk to item_3 refuted it, and `unknown` rose
instead. Whether the robot's finding is "unexplained" depends on the evidence window, every observation since the
episode began or only the current ones. That window is the retraction question (T-D Q2) and belongs to the pending
decision on `unknown`; the definition of "unexplained" does not settle it.

---

## 3. Divergence diagrams

Time runs left to right. "B" is label B (the world), `unknown` is the belief's residual mass, "finding" is the
recognizer's finding.

### 3.1 Standing: unmodelled / nothing unexplained yet

```
the human    walks to shelf, picks up   |  stands still, 5 minutes ....................... |  walks on
B            modelled (the delivery)    |  unmodelled ..................................... |
belief       delivery rising, on top    |  unchanged (no stretch, no observation, I4c)       |
`unknown`    low                        |  low, unchanged                                    |
finding      nothing unexplained        |  nothing unexplained yet (no evidence arrives)     |
```

The world has changed and the robot has received nothing that says so. The rule: a stand adds no evidence of its
own (an empty stretch is no observation; a stretch that stops keeps its value). A live hypothesis in a
no-graded-signal phase (`wait_at`, `pick_up`, `place`) receives one fitting observation, 1/u, for that phase,
whether or not the human performs that task. So an unmodelled stand can support a hypothesis whose current phase
happens at that place, and it is not unexplained; otherwise it changes nothing. Mid-carry, as drawn, every live
hypothesis expects a walk, so nothing changes. (`shared/recognizer.py`: `_progress_likelihood` returns the perfect fit for a phase with no evaluator (lines 865-866) and `None` for an empty stretch (870-871); `_unknown_likelihood` returns the ungraded u for it (903-904); the open term (638-641) and the fold at a phase change (623-631).) After an episode boundary the same stand
leaves the belief at the uniform prior (0.498 each over one task and `unknown`), below θ, again with nothing
unexplained.

### 3.2 A walk to corner_NE: unmodelled / high `unknown` / unexplained

```
the human    at the table               |  walks to corner_NE ............................ |  at the corner
B            ...                        |  unmodelled ...................................... |
belief       prior over the live set    |  every live hypothesis's excess path grows         |
`unknown`    1/|Live|                   |  rises, leads (0.99 in the long detours)           |
finding      nothing unexplained        |  unexplained                                       |
```

The case where the two terms agree: unmodelled behaviour, and evidence that no live task hypothesis explains it.

### 3.3 A wrong-table delivery: unmodelled / high belief in a task hypothesis / not unexplained

scenario_85 (`deviate(deliver(item_0), destination=kitting_table_1)`, then `deliver(item_3)`), current recognizer:

```
tick         17 -------- 49 | 50 -------------------- 157 | 158   159 ----------------- 200 ...
the human    carries item_0 toward kitting_table_1        | places item_3, then stands at kitting_table_1
             (placed on the wrong table at 103)           |
B            unmodelled (the wrong-table delivery) .......| the stand: unmodelled
belief       deliver_item(item_0) leads | `unknown` leads | item_3 pinned, boundary; deliver_item(item_0)
             (gate cleared at 8)        |                 | leads again (0.905 at 200): item_0 lies on the
                                        |                 | wrong table, so its delivery is still open
finding      not unexplained            | unexplained     | not unexplained
```

At 17 to 49 and from 159 on the belief is high on a task hypothesis while the behaviour is unmodelled: the robot
is confidently wrong, and "unexplained" does not fire. From 159 the meta-planner admits it and projects a human
carrying item_0 back, while the human stands (TODO-87).

### 3.4 A finished work order: unmodelled / `unknown` high by normalisation / nothing unexplained

scenario_01, prior on:

```
the human    last assigned delivery      | release: pinned, episode boundary | stands idle
A            assigned task               |                                   | no value (work order finished)
B            modelled                    |                                   | unmodelled (no hypothesis describes a stand)
live set     {that task, `unknown`}      | {`unknown`} (the rest pinned)     |
`unknown`    0.498 at the prior, falls   | 0.995                             | 0.995
finding      nothing unexplained         | nothing unexplained               | nothing unexplained
```

`unknown` is high because nothing else is live, not because of evidence: the mass follows from normalisation. The
stand is unmodelled, as in 3.1, and a stand adds no evidence of its own, so nothing is unexplained. Here `unknown` is high; in 3.1,
mid-carry, it stays low. The belief differs because of what is live, not because of what the human does.

---

## 4. The label-C check

```
scenario description  ------------------------------->  declared experimental condition   (label C)
                                                                  |
script + robot's hypothesis space  -->  label B per behaviour ----+
                                                                  |
                                                                  v
                                   an unmodelled behaviour the declared condition does not cover
                                   ==> the run contains UNINTENDED unmodelled behaviour
```

Declared by convention, for every scenario: the authoring convention's terminal exit walk (`MoveTo` to the door or
a corner, glossary §6, **deviation vocabulary**). It is intended unmodelled behaviour, and the check excludes it by
that declaration.

Not declared by the convention: the terminal stand at a table (TODO-80). A script that ends with the human standing
at a table has unmodelled behaviour; unless the scenario's description declares the blocked case, the stand is
unintended, it is a label-C mismatch, and the run's results carry it. The convention exists to avoid exactly this.

The check reads the script and the hypothesis space only. Computing the labels is not built; it is recorded under
TODO-92, since the evaluation will need it.

---

## 5. What the terms do not change

- No identifier, constant, log tag or log text: the constant `UNKNOWN`, `UNKNOWN_LIKELIHOOD`,
  `none(unknown)`, `none(unresolved)`, `[IR]` lines and the class `Deviation` keep their names.
- No behaviour: the recognizer, the gate and the planner are unchanged.
- The robot's mind: it receives none of the WORLD labels.

---

## 6. Terms deliberately not introduced

| word | why not now |
|---|---|
| unresolved | a candidate name for a belief that points at no task hypothesis; which states the belief distinguishes is the pending decision on `unknown`. (`none(unresolved)` is existing log text with a different meaning: the projector could not resolve the admitted hypothesis's task.) |
| recognised | would name a recognizer outcome; it would also suggest that the recognizer performs the θ gate, which contradicts the architecture: the gate is the meta-planner's, and its outcome is "admitted" |
| exhausted | a candidate name for a live set with no task hypothesis left (the finished work order); whether that state is represented apart from `unknown` is the pending decision |

All three wait for the architecture decision on whether `unknown` stays in the Bayesian hypothesis space. Where
older records use them as ordinary words, they are not terms.

---

## 7. Phrase corrections made in the repo (24 September 2026)

LIVING: corrected in place. FROZEN: text kept; a superseding note at the top of the file (or next to the entry)
gives the precise term.

| file | old phrase | new phrase | kind |
|---|---|---|---|
| `CLAUDE.md` (plan names) | T-D robustness (change of mind, `unknown`, the blocked case) | … change of mind, unmodelled behaviour, the blocked case | living |
| `docs/roadmap.md` (T-E) | the run set covers … a change of mind, `unknown` | … a change of mind, unmodelled behaviour | living |
| `docs/roadmap.md` (T-E) | shows ordering, change of mind and `unknown` | … and unmodelled behaviour (and the belief's `unknown` leading) | living |
| `docs/roadmap.md` (later items) | declared out-of-domain human behaviour, the principled unforeseen stay | a declared unmodelled-behaviour condition: a stay no hypothesis describes | living |
| `docs/roadmap.md` (C) | the stop fires only past T_h and on deviations | … and where the human departs from its projection | living |
| `docs/handoffs/handoff_T-D_onward.md` item 6 | `unknown` with an exhausted hypothesis space … indistinguishable from `unknown` as unmodelled behaviour | `unknown` with no task hypothesis left live … by normalisation … indistinguishable from the high `unknown` that unmodelled behaviour produces | living |
| `docs/recognizer_handback.md` §1.1 | `unknown`, the hypothesis that the behaviour is none of them | `unknown`, the residual hypothesis: … (coverage is a world label the recognizer never receives) | living |
| `docs/recognizer_handback.md` §1.4 | no better than unexplained | scores no better than `unknown` | living |
| `docs/recognizer_handback.md` §3 | `unknown` ≥ θ … also means a task the space does not contain, a detour under way, or every task pinned | … also means unmodelled behaviour (…), or every task pinned, where the mass is `unknown`'s by normalisation | living |
| `docs/recognizer_handback.md` §4 | The scripted human. … Only behaviour the robot's domain describes is scripted; an undeclared behaviour is TODO-80 | The human's script. … Every task in the script is one the domain describes; unmodelled behaviour in a run is a declared experimental condition (TODO-80) or unintended | living |
| `docs/recognizer_handback.md` §7 | declared behaviour outside the domain; a human stay the robot's knowledge does not cover | declared unmodelled behaviour; a human stay no hypothesis describes, declared as the scenario's experimental condition | living |
| `shared/io_contracts.md` §1.9 | The human may deviate within a few ticks | The human may depart from its projection within a few ticks | living |
| `shared/io_contracts.md` §2.2 | The first recognition of a task | The first time a task hypothesis clears the gate | living |
| `shared/io_contracts.md` §2.2 | Mass on `unknown` above θ is not a recognition | … is not admitted | living |
| `shared/io_contracts.md` §4 | a declared out-of-domain behaviour is TODO-80 | declared unmodelled behaviour is TODO-80 | living |
| `shared/meta_planner.py` (`evaluate_triggers`) | not `unknown`, which is no hypothesis | not `unknown`, which is no task hypothesis | living |
| `shared/meta_planner.py` (`evaluate_triggers`) | The first recognition of a task | The first time a task hypothesis clears the gate | living |
| `shared/meta_planner.py` (`update_human_projection`) | not a recognition — the human is doing something outside the hypothesis space, is between tasks, or is deviating | not admitted — the human's behaviour is unmodelled, or no task hypothesis is left live and the mass is `unknown`'s by normalisation | living |
| `shared/recognizer.py` (`_build_admissible_keys`) | 'unknown' is the escape hatch for behaviour outside the model | 'unknown' is the residual hypothesis, which takes the mass when no task hypothesis explains the observations | living |
| `shared/types.py` (`check_task_bindings`) | which … the robot could never recognise | which … no hypothesis could describe: unmodelled behaviour by accident | living |
| `domains/kitting/scenarios.py` (scenario_50) | the coffee walk recognised | coffee_break clears theta on the walk | living |
| `domains/kitting/scenarios.py` (scenario_70/71) | whether the stay is recognised before the robot reaches it; the stay is recognised before it begins | the stay's hypothesis is admitted … | living |
| `docs/design_decisions.md` | escape hatch for behaviour outside the model; no better than unexplained; unexplained behaviour; recognises no task / is recognised at 274; not a recognition (outside the hypothesis space, between tasks, or a deviation); deviate / deviations from the projection; which the robot can never recognise; `unknown` are untouched | see the note at the top of the file | frozen |
| `docs/TODOS_AND_DEFERRED.md` | unknown behaviour; assigned, foreseeable and unknown behaviour; unmodelled behaviour (`unknown`); hypothesis space is exhausted; recognised (θ); a task the robot cannot recognise; by deviations / the human deviated; behaviour outside the robot's domain knowledge, unforeseen stay | see the note at the top of the file (and the pointers on TODO-95, 96, 97) | frozen |
| `analysis/i4_evidence_model`, `i4c_episode`, `i4d_fold_unknown`, `i5_handback` REPORT.md | ground truth `"unknown"` (finished script, s40 wander); winner ≠ truth; unknown when idle | a finished work order / unmodelled behaviour (WORLD); `unknown` leading counted as correct; the `unknown` hypothesis's mass while the work order is finished | frozen |
| `analysis/i2_ir_foundations/REPORT.md` | the coffee walk is recognised; a task the robot cannot recognise | the hypothesis clears θ; a task no hypothesis describes (unmodelled) | frozen |
| `analysis/f47_fixtures/README.md`, `analysis/t9_arrival_radius/REPORT.md` | recognised (at a tick) | the hypothesis clears θ | frozen |
| `analysis/tc2c_scripts/README.md` | a human who departs from the model mid-task; recognised again | a deviation (label A) by a modelled foreseeable task; clears θ again | frozen |
| `analysis/tc2c_scripts/play.md` | (not) recognised, re-recognised; hypothesis space exhausted | the hypothesis (never) leads / clears θ; no task hypothesis left live | frozen |
| `analysis/t6_ablation/README.md`, `analysis/big_picture/STATUS.md` | a deviation from the projection; on deviations | a departure from the projection | frozen |
| `CLAUDE.md`, `shared/io_contracts.md`, `shared/projection.py`, `shared/realization.py`, `shared/types.py`, `analysis/tb1c_realized_flip/README.md` | stationary stretch (a `Segment`) | stationary segment | living (follow-up, 24 Sept 2026) |
| `docs/handoffs/handoff_T-D_onward.md` item 6 (second revision) | indistinguishable from the high `unknown` that unmodelled behaviour produces | the idle stand is itself unmodelled; nothing is unexplained; indistinguishable to `update()` from a high `unknown` raised by evidence | living (follow-up, 24 Sept 2026) |

---

## 8. What T-H changes here (25 September 2026)

T-H replaces the representation the WORLD labels were read from: the script of primitives with provenance and edits
(T-C1) becomes an ordered list of task instances of one tree of task schemas, with events, run by a human executor
with a stack that writes a record per tick. The terms of the ROBOT group (section 1.2), the usage rule (1.3), the
divergence diagrams as statements about the belief (section 3) and the terms not introduced (section 6) are unchanged.

### 8.1 The labels become queries on the record

```
24 September (sections 1.1, 2, 4)             T-H (glossary §6, §7)
label A, work order: assigned task |           assigned(task): the assigned task and its departures | None;
  deviation                                      no value on an empty stack; unperformed(assigned_tasks): the
                                                 assigned tasks never completed without a departure (T-H4)
label B: modelled | unmodelled                 coverage(task, robot): COVERED | TASK_ABSENT |
  (a HypothesisKey describes it, or not)         BINDING_ABSENT, per task instance on the stack
label C: declared experimental condition       unchanged; the check reads coverage from the record
computed from script + provenance +            read from the executor's record: the stack (top first),
  hypothesis space (TODO-92, not built)          the action, its progress; built T-H2, queried T-H4
```

### 8.2 "Deviation" moves

On 24 September a deviation was any departure from the work order (label A), and a foreseeable task was "a deviation
that is modelled". Under T-H a deviation is a node of the human's realised plan tree that the robot's tree does not
contain, at one of two levels (task schema, binding). So:
- the foreseeable-task cell of the 1.1 table (label A deviation, label B modelled) is, under T-H, a switch to a
  `PersonalTask` in the robot's task model: `assigned` false, `coverage` `COVERED`, and no deviation;
- "foreseeable" is defined, not declared: a `PersonalTask` in the task model (the `is_foreseeable` flag goes, T-H1);
- `interrupt`, `deviate`, `abandon` (the operations of the 1.1 diagram) are replaced by an event (`task.at(action,
  Start(task))`), a plain instance with the other binding, and `Drop`.

### 8.3 The cases of section 2 under T-H

| case (section 2) | written under T-H | `assigned` | `coverage` |
|---|---|---|---|
| an assigned delivery | `deliver_item("item_3")` | the assigned task, no departure | `COVERED` |
| a `coffee_break` interrupt | `deliver_item("item_3").at(pick_up, coffee_break("coffee_machine_0"))`; the delivery suspended, then resumed | `None` (the coffee break, on top of the stack) | the coffee break: `COVERED` if the task model holds `coffee_break`, else `TASK_ABSENT`; the interrupted delivery, judged on its own instance: `COVERED` |
| a wrong-table delivery (TODO-87) | `deliver_item("item_0", table="kitting_table_1")`, a plain instance | the assigned task with a departure, `?kitting_table=kitting_table_1` (T-H4) | `BINDING_ABSENT` |
| a walk to corner_NE | `go_to("corner_NE")` | `None` | `TASK_ABSENT` (a `HumanOnlyTask`) |
| a stand of 5 minutes | `stand("PT5M")` (the stand task, its stand action emits no world fact) | `None` | `TASK_ABSENT` |
| the idle human after the script | nothing on the stack | no value | no value |

The belief and finding columns of section 2 are unchanged: T-H does not touch the robot's mind.

The last row differs from the 24 September follow-up ruling, which called the idle stand unmodelled. Under T-H coverage
is a query on a task, and after the script there is none: the empty stack is its own ground-truth case (T-D Q1's "no
task on the stack"). A stand the script writes is the `stand` task, `TASK_ABSENT`.

### 8.4 The label-C check (section 4)

It reads the record (in simulation only; a real human needs annotation of the same form) instead of the script and
the hypothesis space: every task on the record whose coverage is not
`COVERED` must be covered by the scenario's declared condition. The convention's terminal exit walk is now
`go_to("door")` or a corner, declared for every scenario as before; the terminal stand at a table (TODO-80) stays a
mismatch unless declared. The queries it reads are built (T-H4; TODO-92 superseded); the check itself is not: a
scenario's declared condition is free text in its description.

### 8.5 Identifiers and wording

- Removed by T-H3, kept in sections 1 to 7 as the vocabulary of their date: `Stay`, `MoveTo`, `PickUp`, `Place`,
  `expand` / `resolve_script` as a separate form, provenance, the class `Deviation`, string anchors,
  `check_work_order`.
- `wait_at` is unchanged (located; it completes `waited(agent, entity)`; the expected action of `coffee_break` and
  `ac_activation`). T-H1 adds a second action, `stand(?duration)`: no entity, process completion only, no world fact;
  the human-only task `stand` uses it. Sections 1 to 7 say "a stand" for a human standing still, which the record now
  splits into a `wait_at` inside a task, the `stand` task, or an empty stack.
- "work order" → "assigned tasks" (a set the robot is told; the ordering lives only in the human's script).

