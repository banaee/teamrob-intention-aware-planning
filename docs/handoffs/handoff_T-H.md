# TeamRob handoff: T-H, the human behaviour model

Written 25 September 2026 by ccode. It records Hadi's ruling of that day and the rulings on ccode's conceptual review
of it. It is for the sessions that build T-H (T-H1 to T-H4) and for cchat.

The committed documents are authoritative over this handoff:
- `docs/design_decisions.md`, "T-H: the human behaviour model": the design, items 1 to 11, and the facts left to the
  build;
- `docs/glossary.md` §6 and §7: the terms;
- `docs/terminology_revision.md` §8;
- `docs/roadmap.md`, "The plan from T-A", T-H;
- `docs/TODOS_AND_DEFERRED.md`: TODO-92, TODO-99 (closed), TODO-100, TODO-101.

Read the glossary first.

## Close-out (26 September 2026): T-H is closed

T-H1 to T-H4 are built and committed on `main` (not pushed at writing; Hadi reviews and pushes). Sections 0 to 5 below
are the record of the ruling and the plan as written on 25 September; where they say "to be built", read this section.

| subtask | commits | closed by |
|---|---|---|
| T-H1 the tree, the task model, the two knowledge objects | `c5cd1a0`, `99958c1`, `e571eed`, `a2c2a5b` | `shared/knowledge.py` (`Tree`, `TaskModel`); the schema classes; the stand action; `go_to` / `stand` |
| T-H2 the executor | `c1c1089`, `448f38a`, `1b6c83d` | `world/human_executor.py` (the stack machine, `check_script`), `world/record.py`, the `[rec]` stream, `Executor.suspend` / `resume` |
| T-H3 the migration | `39b59a5`, `60ab8dc`, `0af3c0a` | every scenario on the `Script` in the kitting call form; `go_to_and_stand`; the C1 layer deleted |
| T-H4 the record's queries | `da4c61f`, `e4fe110` | `world/queries.py`; task equality `same_task`; `Departure`; the `[coverage]` line |

ACCEPTANCE (section 4), as measured:
- T-H1: no baseline regenerated; T-H1's report (the session report to Hadi) found the 48 logs (the 40 maintained and
  tb3's 8 `single_task` runs) byte-identical to those before its commits; the T-C2b baselines stood through T-H1 and
  T-H2, and T-H2's check against them was byte-identical.
- T-H2: the 40 maintained logs and tb3's 8 unstored `single_task` runs byte-identical; the `.rec` files empty.
- T-H3: the 40 maintained logs byte-identical to the T-C2b baselines outside the `[human]` lines (the record's
  transitions replace the C1 primitive lines); the first non-empty `.rec` baselines; the four sets regenerated (T-H3
  md5 sections).
- T-H4: the 40 maintained logs and the 8 `single_task` runs byte-identical to T-H3's outside the new `[coverage]`
  lines; every `.rec` byte-identical; the four sets regenerated (T-H4 md5 sections, the `.rec` md5s unchanged). Every
  entry of the maintained fixtures is `covered`.
- Robot-side lines were byte-identical at every step: T-H changed nothing in the robot's mind.

DEFERRED, each recorded:
- TODO-100: nested interruptions; the stack stays one level deep until a scenario needs more.
- TODO-101: the oracle-IR evaluation; its seam is recorded (`truth_at`, then `coverage`, a `Covered` carries the
  hypothesis), the adapter is not built.
- TODO-102: a per-robot task model on the robot's `AgentConfig`; today every robot gets the use case's declared one.
- TODO-105: a resumed fetch walk goes to an item the robot has already delivered (the cut action finishes first).
- TODO-106: the load-time replay cannot see body-derived facts (`waited` retraction, `at` for a held object).
- TODO-109: the `[rec]` stream carries no agent id; two humans would interleave.
- The exporter (Phase 7): rewriting `Now` as `at` / `during` from the record, and the viewer's buttons; `inject` exists.
- The label-C check: a scenario's purpose is free text in its description (label C, glossary §7; was "declared
  condition"); the queries it would read are built, and so are the scenario's composition and scenario coverage (T-H
  follow-up, `world/composition.py`); the check is not.

## 0. Push state

- `origin/main` is at `19e7b8b` (the stand rule stated in full). Everything up to that commit is pushed.
- The T-H record commits sit on top of it, local and NOT pushed at writing:
  - the first recording;
  - its amendment by the rulings on the review;
  - this handoff, with CLAUDE.md and the living-doc renames.

  Hadi reviews and pushes. A session that starts after the push starts from the pushed HEAD.
- No code has changed for T-H. The maintained baselines are still the T-C2b regeneration (`06093ee`).

## 1. Why T-H

The human's script (T-C1) holds the meaning of the human's behaviour in edits of task expansions. Recovering that
meaning needed provenance, string anchors, a kind-string `Deviation` class, key-based checks and two booleans on
`TaskSchema`. The terminology of 24 September named the resulting distinctions but could not remove their cause.

T-H replaces the representation. It changes nothing in the robot's mind. It changes what the human is, how a scenario
is written, and what ground truth is.

## 2. The design (summary; the design entry is authoritative)

1. **Deviation.** A deviation is a node of the human's realised plan tree that the robot's tree does not contain.
   There are two levels: the task schema is absent, or the binding is absent.

2. **One tree of task schemas per use case.** Every schema has the full HTN structure:
   - `WorkTask`: may be assigned (`deliver_item`); a robot's own assigned tasks are `WorkTask`s;
   - `PersonalTask`: never assigned (`coffee_break`, `ac_activation`);
   - `HumanOnlyTask`, a kind of `PersonalTask`: never given to a robot (`go_to(?landmark)`, `stand(?duration)`).

   `is_assigned` and `is_foreseeable` are removed. Only a `HumanOnlyTask` may type a parameter as a landmark.

3. **Task model and knowledge objects.** A robot's task model is chosen per experiment by whole schemas:
   - every `WorkTask` is in it;
   - a `PersonalTask` may be omitted;
   - a `HumanOnlyTask` is rejected.

   There are two knowledge objects: the world's tree, and one task model per robot, built from the tree in the
   embodiment loader, which is where the rejection runs. The human executor's planner uses the tree. The robot's
   recognizer, projector and planner use the task model only. Nothing in `shared/` reads human-only-ness.

   "Foreseeable" means a `PersonalTask` in the task model. The support restriction is the hypotheses of the assigned
   `WorkTask` instances, plus every `PersonalTask` hypothesis in the task model, plus `unknown`, compared as
   `HypothesisKey` values.

4. **Assigned tasks.** A set the robot is told ("work order" is renamed). The ordering lives only in the script.

5. **The script.** An ordered list of fully bound task instances, with typed events attached. An event is a
   `Trigger` plus a `Decision`:
   - `Trigger`: `AfterAction(action, occurrence)` (written with `at`), `DuringAction(action, time)` (written with
     `during`, built in T-H2; physical time in the form durations use, converted by the body, the exporter converting
     the recorded tick once), or `Now` (`inject`);
   - `Decision`: `Start(task)` or `Drop`.

   The authored forms are `.at(action, task_instance)`, `.at(action, drop)` and `.during(action, time, task_instance |
   drop)`: sugar that constructs `Event(AfterAction | DuringAction, Start | Drop)`. The types are fixed; T-H2's plan
   shows the sugar.

   Rules for `at`:
   - it fires after the action completes;
   - the boundary before a task's first action is the previous entry's last action;
   - an event fires once per script entry, then is consumed.

   At load, every anchor is checked against the load-time sequential expansion, which the executor must reproduce
   exactly. An anchor that is absent from a re-expansion is a load error. The script itself is checked for types only.
   `Stay`, `MoveTo`, `PickUp` and `Place` are removed.

6. **The stack.** It is one level deep. `Start` suspends the current task; `Drop` removes the top of the stack.
   On resumption the executor:
   - first completes the cut action with what remains of it;
   - then re-expands the task in the resulting state.

   Outcomes are completed, suspended, abandoned and infeasible, computed and never authored. One world behaviour can
   have two records; this is accepted, because the record is of decisions.

7. **The record.** Per tick it holds the stack (top first), the action and its progress. It is its own stream (a
   `[rec]` file beside the run log, diffed in the sweep).

   Its typed queries are `switches`, `resumptions`, `assigned(task)`, `unperformed(assigned_tasks)`,
   `coverage(task, robot)` and `truth_at(tick)`. Coverage takes the values `COVERED`, `TASK_ABSENT` and
   `BINDING_ABSENT`, and is judged per task instance on the stack.

   `world_state_builder` exposes nothing of the stack. The record exists in simulation only; a real human needs
   annotation of the same form.

8. **Live runs.** `inject(Start(task) | Drop())` creates an event with the trigger `Now`. On export, `Now` becomes
   `AfterAction` or `DuringAction`; an injection on an empty stack becomes a plain script entry. An exported run
   replays byte-identically.

9. **Actions.** `wait_at(?entity, ?duration)` is unchanged. T-H adds `stand(?duration)`:
   - no entity;
   - process completion only;
   - no world fact.

   Durations take the physical form and are typed through `duration_key`. The projector takes a stand's duration from
   the instance's binding.

10. **Not part of T-H.**
    - The IR redesign. T-D Q1 gets ground-truth cases: a switch to a modelled task, one outside the support, one to
      an unmodelled task, a binding-level deviation, no task on the stack, and an episode's first ticks.
    - Oracle IR (TODO-101). `truth_at` enters the robot's mind only through that condition's explicit adapter.
    - Alternative 1.
    - Nested interruptions (TODO-100).

## 3. The build plan

Each subtask is one session. Each follows CLAUDE.md's **BUILD DISCIPLINE**, in two steps:
- **Step 1, plan only.** Report the intended structure (classes, fields, what is removed, which files), the cases the
  design does not cover, and the tests to run. No code and no commit; wait for Hadi's confirmation.
- **Step 2.** Build what was confirmed.

The rules for both steps:
- No hidden assumptions: where the design is silent, ask.
- No shortcut to a running state.
- Nothing left untyped: no `List[Any]`, no `Union` of unrelated types, no kind strings, and no booleans standing for
  a class.
- No new check that works by string or key matching, and no patch around the conceptual design. Identity is object
  identity, or value equality of typed objects.
- If a rule blocks progress, stop and report why. That report is the deliverable.

The subtasks:

- **T-H1: the tree, the task model and the two knowledge objects.** CLOSED (`c5cd1a0` to `a2c2a5b`). It covers the `stand` action, the destination
  check's move, and the start of the `dock_loading` / `ros_sim` migration. Its planning step shows:
  - methods referencing `ActionSchema` objects (today `StepCall.action_name` is a string);
  - the support restriction comparing `HypothesisKey` values (today it matches `repr` strings).

  Facts for step 1, recorded in the design entry:
  - `check_task_destinations` already runs on `assigned_tasks` only;
  - `is_foreseeable` is read in the mind only in `_build_admissible_keys`;
  - the `DomainKnowledge` getters for the two booleans have no caller;
  - one `DomainKnowledge` serves the robot and the script resolver today.
- **T-H2: the executor.** CLOSED (`c1c1089` to `1b6c83d`). It builds:
  - `Event`, `Decision` (`Start`, `Drop`) and `Trigger` (`AfterAction`, `DuringAction`, `Now`);
  - `at`, `during` and `inject`;
  - the stack, the mid-action cut and the resumption rule;
  - the load-time anchor check against the sequential expansion;
  - the record and its `[rec]` stream;
  - the test that `world_state_builder` exposes nothing of the stack.

  Its planning step shows how the cut and the resume sit in the shared `Executor` without touching the robot's paths
  (reload and completion-tick bookkeeping, hold, separation stop).
- **T-H3: the migration.** CLOSED (`39b59a5` to `0af3c0a`). The scenarios are rewritten in the new script, and `dock_loading` and `ros_sim` are
  migrated. It deletes:
  - the C1 vocabulary: `interrupt`, `deviate` and `abandon`;
  - `Deviation` and `Provenance`;
  - `expand` / `resolve_script` as a separate form;
  - the key-based checks (`check_work_order`);
  - `Stay`, `MoveTo`, `PickUp` and `Place`.

  The glossary's T-C1 entries go with the code.
- **T-H4: the record's queries, `unperformed` and coverage.** CLOSED (`da4c61f`, `e4fe110`). This supersedes TODO-92's ground-truth half. The type of
  `assigned(task)` for a binding-level deviation of an assigned task is settled here.

## 4. Acceptance across T-H

After each build, rerun the 40 maintained baseline logs (tb1a 16, tb1b 4, tb1c 8, tb3 12; the commands are in their
READMEs). Then:
- Robot-side lines (`[IR]`, `[IR-dist]`, `[meta-*]`, the decisions) must be byte-identical. There is no rename
  exception, since `wait_at` stays.
- Human-side differences are listed, and each one is explained.
- From T-H2 on, the `[rec]` stream is diffed as well.

At the end of T-H3 the new logs replace the stored baselines, with a new md5 section in each README.

## 5. After T-H

- T-D resumes on this structure. Read `docs/handoffs/handoff_T-D_onward.md`, section 6, with the T-H terms.
- The oracle-IR evaluation (TODO-101) runs no IR, IR and oracle IR on the same scenario. Its interface is recorded
  there.
- Alternative 1 is recorded in the roadmap and not scheduled.
- The name T-H was earlier reserved for the recognizer's duration term for a stay (TODO-85 (a)). That item is TODO-95.
