# Record of planning and building: T-H, the human behaviour model

Moved verbatim from `docs/design_decisions.md` on 2 October 2026 (Hadi's ruling of that day: one record file per task;
the conceptual design stays in design_decisions.md). Each block is headed by the title of the entry it comes from
and its id; in design_decisions.md an index line with the same id stands where the block was.

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
