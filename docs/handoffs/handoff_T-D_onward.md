# TeamRob handoff: from the T-B1c / T-B3 / D3 / T-C chat to the T-D-and-upward chat

Written 23 September 2026 by cchat (the design chat), at the end of the chat that ran T-B1c, T-B1d,
T-B Q6, T-B3, the `task_committed` debate and its removal (D3), the TODO-90 check, T-C1 (design) and
T-C2a/b/c (build), the script play across nine layouts, and the recording of Phase 7. Everything in
it is committed and pushed; nothing is open in ccode.

## 0. How to use this document

- The repo on `main` at `528924d` (pushed after the authoring-convention records) is the base. The
  committed documents are authoritative over this handoff: `CLAUDE.md`, `docs/glossary.md`,
  `docs/roadmap.md`, `docs/design_decisions.md`, `docs/TODOS_AND_DEFERRED.md`,
  `docs/recognizer_handback.md`, `shared/io_contracts.md`, `docs/handoffs/phase7_interactive_deviations.md`,
  and the `analysis/*/README.md` files named below. Read them from project knowledge, which must be
  re-synced to that HEAD before use; ask Hadi to attach a file when a direct read is better.
- `docs/glossary.md` is authoritative for terms. Read it before the design record. Every term in this
  handoff has the meaning the glossary gives it.
- Read sections 1 to 5 fully before doing anything. Then go to section 6 (T-D), which is where the
  new chat starts.
- This chat ends when T-D's design is ruled and built, T-E is designed and built, and T-F's design is
  recorded; it writes the next handoff then. T-G and Phase 7 are recorded here as plan only. Phase 7
  gets its own chat and its own revised handoff when Hadi opens it; it is not this chat's work.

## 1. Working style (enforced strictly; all of it is also in memory)

Terms: **cchat** is this chat. **ccode** is Claude Code. Hadi now uses Opus 5.5 in ccode, which he
treats as equivalent to Fable; a prompt's model line still gives one clause of reason.

Division of work:
- cchat settles WHAT and WHY. ccode owns HOW. A ccode prompt states what the part is meant to achieve
  and why, the purpose behind each requirement, then the requirements; never an action list, never
  the mechanism. Where cchat and Hadi have DECIDED something (a name, a number, a set, a form), the
  prompt states it exactly; ccode is not left to choose what was decided. Hadi checks prompts for
  both. If a requirement forces an implementation ccode thinks wrong, ccode says so before building.
- Every ccode prompt is preceded by two lines: **model** (Opus 5.5 or Opus high, one clause of
  reason; for a borderline task give the cheaper choice as default) and **session** (new, or continue
  which one). Sessions run in **auto**, not plan mode.
- A follow-up prompt can be queued into a running ccode session. Two ccode sessions never run in
  parallel on the same working tree.
- ccode sometimes asks a multiple-choice question mid-task (a "Stay/wait_at" style card). cchat
  answers with the option and one or two lines of framing; Hadi relays.

The commit gate (Hadi's rule):
- ccode does NOT commit a change to code until Hadi confirms the design is right: report and wait.
- Docs, records and regenerated baselines may be committed as ccode goes.
- A restatement check at the top of a prompt says "no commit until confirmed", not "no change".
- Push marks a checkpoint; project knowledge syncs on push.

Standing-rules block, on a prompt that opens a NEW session only (a same-session follow-up opens with
one line stating the push state):

    Standing rules: follow CLAUDE.md, and docs/glossary.md with it. Work on main. Do not commit a
    change to code until Hadi confirms: report and wait. Docs, records and regenerated baselines
    may be committed as you go. Do not push until told. PYTHONHASHSEED=0 on every run. Scenarios
    are experiments, not the specification; fixtures are debugging examples, not a settled
    reference. The design is settled: build it, do not explore alternatives. If it is structurally
    or experimentally deadlocked, say so and stop. Code wins over this prompt: report
    contradictions, do not silently resolve them. Flag scope, do not absorb it.

How cchat talks to Hadi (the two rules added in this chat are marked NEW):
- Whenever a decision is needed from Hadi, first restate in plain human words what the problem is,
  then give the options with their consequences, then ask explicitly.
- NEW: elaborate literally and clearly with concrete examples (numeric illustrations, labelled as
  illustrations); no figurative or abstract language; give clear alternative solutions and a
  recommendation; never present only a broad, vague issue. Hadi asked for this after a confusing
  round on T-B1c.
- NEW: when a term names different things at different points of the flow, say in parentheses which
  is meant at each use, e.g. `current_task` (the task the robot was executing at the trigger) against
  `current_task` (the decided new current task to be executed); "hold" (before the first entry,
  executed) against a hold before a later entry (priced only); "queue" (the pool without the
  executing task) against `UpdateResult.queue` (the winner's tail, information only).
- Itemised, exact, one meaning per term, the glossary's meaning. No em dashes. No praise.
- When relaying a ccode report, show only what matters for the decisions on the T-X tasks and their
  logic; not the obvious, not the non-conceptual implementation details.
- Do not justify an algorithmic design decision from a scenario; a fixture number is an illustration.
- Agreement is earned. Question assumptions; disagree when warranted; say when a previous cchat
  statement was wrong (this chat withdrew several: "close in plain cost", the R3 removal criterion of
  T-B1d, the Q6.3 defect rule, the "identical choices on one-table fixtures" expectation, the Phase 7
  boundary deferral).

Rules Hadi set, standing (added in this chat are marked NEW):
- Fixtures are experiments; they never supply a design decision or a parameter value. Safety
  parameters (`min_separation`) are set by standards; β is a fixed physical tolerance.
- Every mechanism must be defensible in one sentence without reference to a scenario. No per-scenario
  rules, no heuristic timing corrections in the executor.
- A settled decision can be questioned when there is a reason; debated on design grounds in cchat
  before anything changes (done for `task_committed`, section 4).
- NEW: layouts, scenarios and the saved logs are debugging examples, not a settled evaluation
  reference. Hadi may change or rearrange any of them at any time; when they change, the logs are
  regenerated; no design argument rests on them (CLAUDE.md, Methodology).
- NEW: fixture tasks are cheap: one run per candidate script, no sampling checks, no analysis
  scripts, no md5s, a budget of candidates in the prompt, "a fixture is disposable; the algorithm is
  what is fixed; approximate is fine". Evaluation-grade checks only where logs are kept as diff
  targets (T-B3 style). T-B1c spent far too much; do not repeat it.
- NEW: debugging and development runs use the assignment prior ON only, from T-B3 on; OFF/ON returns
  for the paper's evaluation.
- Fixtures are readable: hand-written literals in `scenarios.py` with ordinary registry entries.
  Scenario naming: a scenario on layout X is numbered X0, X1, X2 (layout9 owns 90 to 99).
- Hadi rules on every evaluation scenario; ccode may propose one within limits, reported as an
  existence case, not an evaluation.
- Design questions of a task are named "T-D Q1", never plain "Q1".
- The historical record is not rewritten for tidiness; a closed entry keeps its text, marked
  superseded.

## 2. The framework, state at handoff

One flow: the recognizer holds one hypothesis per human task and `unknown`, updated from the human's
trajectory by graded evidence (walked excess path; a tick with nothing walked is no evidence, I4c);
the meta-planner runs on TWO triggers (`recognition_changed`, `no_current_task`), admits the most
likely hypothesis at θ = 0.75, projects the human to T_h, and chooses the robot's next task
(`single_task` default, `full_reorder` under `--strategy`); `realize()` prices each candidate against
the human projection with one hold per entry; the Mesa body executes the plan and the hold; the
separation stop (off by default in debugging runs) refuses a robot step below `min_separation`.

What changed in this chat (details in sections 3 and 4):
- `task_committed` is gone (D3). Trigger set {`recognition_changed`, `no_current_task`}. No re-timing
  mechanism exists; none was needed on the corrected body.
- The human's scenario is an action script (T-C): `scheduled_tasks` is a flat list of primitives at
  run time (`MoveTo`, `PickUp`, `Place`, `Stay`); a `TaskInstance` in it is expanded at load by
  `expand()` (the planner's decomposition, sequential against the successor state left by the earlier
  elements, provenance recorded); the author vocabulary `interrupt`, `deviate`, `abandon` (deferred
  edits resolved at load, anchors by action name or index); landmarks (four corners and a door) as
  layout objects of type `landmark` that no task may type; the human executor is action-level
  (`HumanAgent` grounds one primitive when reached and hands it to the shared Executor as a one-action
  plan; no task tracking, no per-task completion tick; the human's per-task latency is 0 for the
  projector, `HUMAN_TASK_COMPLETION_LATENCY`). The robot's side is unchanged.
- Baselines: 40 logs at commit `06093ee` (tb1a 16, tb1b 4, tb1c 8, tb3 12; md5s in the READMEs),
  regenerated once for the dropped human per-task tick. `full_reorder` baselines exist (tb3, realized,
  both priors). scenario_83 is the existence case for a realized-cost head flip under B3.B (fragile:
  decided by 0.78 cm and a 3-tick timing window; recorded as such).
- Fixtures now: layouts 0 to 7 (one table), 8 and 9 (two tables); the Phase 4C and T-B fixtures
  unchanged; two T-C fixtures (scenario_11 interrupted delivery on layout1, scenario_01 declared stay
  on layout0); 22 script examples on nine layouts, registered, not measured (02, 03, 04, 12, 22, 23,
  24, 31, 32, 41, 42, 51, 52, 53, 72, 73, 84, 85, 91, 92, 93, 94), run by
  `analysis/tc2c_scripts/play.py <n>`, five-line observations in `analysis/tc2c_scripts/play.md`.
- Authoring convention: a script ends with the human leaving the workspace (`MoveTo("door")` or a
  corner) unless the scenario is about the terminal stand (TODO-80).
- Phase 7 (interactive deviations and a context stream) is recorded, not scheduled:
  `docs/handoffs/phase7_interactive_deviations.md`, roadmap section, one design_decisions entry.

## 3. What this chat did, in order (all committed and pushed)

- **T-B1c** (`38dd7f7` record, `8aec522` scenario_83 literal, `bcb338e` records): the existence case.
  scenario_83 on layout8, human `item_3 -> kitting_table_1, then item_0 -> kitting_table_0` from
  (-430, 400); at step 159 (`no_current_task`, projection of item_0 admitted) plain head item_6,
  realized head item_1, gap 1.44 < shift 3, both priors. Ruled a fixture (option i). TODO-89 opened
  (arrival-radius geometry decides conflicts at s with a margin of the order of the projected-vs-
  executed stop-point difference). `permutation_costs.py` prices only from the robot's start (known
  limit, not extended).
- **T-B1d** (record only): no scenario_84 as a designation fixture. The nine designation sets ccode
  priced showed that the greedy head and the ordering head differ in seven (gaps 14 to 78 ticks) and
  coincide in two, and every flip traces to the one designation that moves the cheapest single task:
  that is the mechanism (`single_task` takes the cheapest task from here; `full_reorder` takes the
  task whose delivery leaves the robot best placed for the remaining shelves), not a weakness. R1 of
  the prompt was wrong (a scenario cannot change a designation; the destination is a layout fact,
  T-B Q1). `analysis/tb1d_designations/README.md`; TODO-47 (f) corrected. (The number 84 was later
  reused for a play script on layout8; no conflict, T-B1d registered nothing.)
- **T-B Q6** (cchat): reduced to a table and a regression set; no claim sentences; see section 4.
- **T-B3** (`25ccb1b` CLAUDE.md fixtures rule, `58eb347` record, `e76f2d8` follow-up): 20 runs (s80,
  s81, s83, s20, s70 x strategy x prior, realized, gate none, stop off); the first `full_reorder`
  logs; s20 `full_reorder` finishes 16 ticks earlier with a different head order and no hold (the
  case (b) of the corrected one-table expectation, not investigated); roadmap line for a separate
  "two-table re-examination of the recognizer and B2" task. `analysis/tb3_full_reorder/`.
- **Ablation** (`142deaa`): the trigger set without `task_committed`; 26 pairs, world identical.
- **D3** (`dd880be` code, `36b3978` baselines, `c650ec3` records, plus cleanup `8b0af14`, `7f122fd`):
  `task_committed` deleted; `evaluate_triggers()` has two conditions; six 1-tick holds it had placed
  (s20 and s50 at 31, s30 at 47, both priors) were the owed acknowledgement tick; world lines
  byte-identical; records revised (D2 entry, DESIGN-07, TODO-77 closed, TODO-71, E2b, glossary).
- **TODO-90 check** (`1819ca3`): the two in-window approaches under gate `b2a` are standing ticks that
  realization itself projected (the human walks up to a standing robot; F1 allows it); one tick was an
  attribution error of the ablation's tool. TODO-90 closed; TODO-91 (the executor's `[stop]` label
  uses T_h alone where the glossary intersects the window with the plan's span; label only).
- **Phase 7 recorded** (`7c7e44d` and the rename): handoff file, roadmap section, design entry.
- **T-C1** (`1df2c42`, `7f38213`, `56ce95a`, `8c58d6a`): the design record; CLAUDE.md "about / not
  about"; TODO-86 closed; TODO-92 (observed history of the human's tasks, for T-D); glossary §6.
- **T-C2a** (code commit after Hadi's confirmation; `4f1e907` Stay ruling in the record): primitives,
  `expand()`, provenance, vocabulary as deferred edits, landmarks on layout0, `check_work_order`
  (presence by provenance), `decompose(method=)`, `tests/test_script_layer.py` (19 checks, pytest
  installed). Regression byte-identical.
- **T-C2b** (`c773d5c` records, `06093ee` code, `679fcb0` baselines): sequential expansion via
  `shared/projection.successor_state()`; action-level `HumanAgent`; human per-task latency 0; the
  compatibility path removed; identity check on five fixtures; all 40 baselines regenerated (human
  one tick earlier per completed task; holds one tick shorter where they depended on the human's
  arrival: s20 8 -> 7, s30 7 -> 6, s50 8 -> 7, s81 3 -> 2, s70's 1-tick hold gone, s83 `full_reorder`
  a new 2-tick hold at 190, s71 hold planned 31 instead of 32).
- **T-C2c** (`92cf519`, `feabe3d`): executor's unused `advance_script` branch removed; scenario_11
  (interrupted delivery) and scenario_01 (declared stay) as fixtures; `analysis/tc2c_scripts/`;
  TODO-85, TODO-80 observations; TODO-93 opened; T-C closed in the roadmap.
- **Play** (`b352e7c`, `f5719fe`): 22 scripts on nine layouts, landmarks added to those layouts,
  existing fixtures byte-identical; Phase 7 readiness lines in the handoff file.
- **Convention and T-D agenda** (`528924d`): the authoring convention; TODO-85 (b) generalised;
  TODO-94 opened; TODO-93, TODO-87 marked reproduced; TODO-80 fixture note.

## 4. Decisions settled in this chat (do not reopen; the record entries are authoritative)

T-B1c requirements (Hadi's rulings on the seven items):
1. Gap < hold, both reported; "close in plain cost" withdrawn.
2. The plain-cost head and the realized-cost head differ (a same-head flip changes only `ordering=`).
3. The conflict is in an entry after the head, inside [trigger, T_h], head realized alone hold 0
   (case (b), the case T-B2c exists for); case (a) is B3.A's own effect.
4. The decision is `recognition_changed` or `no_current_task`, gate `none`.
5. One variable: scenario_80's robot side, only the human's script differs; read per decision.
6. Layout8. 7. ccode proposes, Hadi rules.
Outcome: on layout8 any case (b) is a table convergence at the arrival-radius margin; a robust
crossing case belongs to T-F.

T-B Q6 (the acceptance of T-B3), as reduced by Hadi:
- No claim sentences; a table per fixture and prior (completion tick from the world fact, head
  sequence, admitted projections, holds executed). Generality is T-F's.
- Defect rule, corrected after TODO-90: a robot STEP (a moving tick) inside an assessed window that
  ends below `min_separation` is a defect; standing ticks are judged by whether realization projected
  them (F1: the robot answers for its own motion only). Violations outside the window are information.
- Runs: realized cost only, strategy x prior, subset of fixtures; `full_reorder` realized logs kept as
  diff targets. The two-table re-examination of recognizer and B2 is its own task after T-B.
- Corrected expectation on one-table fixtures (derived by the previous chat, verified in outline by
  s20): the heads coincide only at decisions taken FROM the table (all orderings tie up to the
  arrival point); at a decision away from the table `full_reorder` may legitimately differ by the
  differential walk(p, shelf_A) − walk(table, shelf_A); with realized cost a hold before a later
  entry may account for a difference. Record: design_decisions.md B3.B entry and T-B3 README.

D3, the trigger set:
- A trigger is a change in what the last decision rested on: the human's hypothesis or the robot's
  task set. The robot's own grasp is neither; it was in the plan the last decision priced. Set:
  {`recognition_changed`, `no_current_task`}. Ruled on the semantics before the ablation; the
  ablation decided only whether a re-timing mechanism was needed (it was not).
- Not reverted: T-B Q7's executor fix (the body spends the ticks it states); `deliver_already_held`
  stays (needed for mid-carry `recognition_changed` decisions under "plans are never resumed").
- E2b (stall/block) and TODO-71 (executor-extended hold) are not triggers; their home, if ever
  needed, is a body-side event (T-D's blocked event).
- The per-task completion tick (`TASK_COMPLETION_LATENCY`, from F1) is real, per agent, counted once
  per task by the projector; not a heuristic, not from Q7. The robot keeps it; the human no longer
  spends it (T-C2b). The robot's own per-task tick as an executor artefact is a later, separate
  question (one line in TODOS).

T-C1, the human action script (design_decisions.md "The human action script (T-C1, decided)" with
its AS BUILT notes is authoritative; summary):
- The script is an experimental instrument. The robot's mind receives nothing from it.
- Framework statement (Hadi, in CLAUDE.md): the framework shows how the robot reads and plans around
  the human; what the human produces is not the object; an abandoned delivery is in scope for what it
  does to the robot (retraction, `unknown`, re-planning), not for the human's output.
- Executed form: flat list of primitives; `TaskInstance` as sugar expanded at load, sequentially
  against the successor state (a change of mind after a pick-up expands the next delivery with the
  return, `deliver_with_return`); `expand()` returns one element per action the method contains
  (`wait_at` inside `coffee_break` stays an action with its `waited` fact); provenance automatic; no
  intent label, no boundary flag, no `Block` type, no `wait` primitive.
- `Stay` grounds to nothing: standing still is the absence of an action; `Stay()` idles to the run's
  end, `Stay(n)` n ticks, `Stay(0)` is a no-op; zero is never the encoding of open-ended.
- Vocabulary: `interrupt(task, after=|before=, with_=[...])`, `deviate(task, destination=)`,
  `abandon(task, after=|before=, then=[...])`; list helpers `insert_after`, `insert_before`,
  `retarget`, `truncate`; anchors by action name (must be unique in the expansion) or 0-based index;
  injected content mixes `TaskInstance`s and primitives. Deferred edits: the vocabulary returns a
  `Deviation` the loader resolves against the initial world (scenario literals are built at import
  with no world). All injections at action boundaries; no tick, fraction or position anchors in T-C.
  A coordinate-valued `MoveTo` is admitted by the form for Phase 7's exporter; authors never write
  waypoints.
- Landmarks: four corners and one door per layout (`corner_NE/NW/SE/SW`, `door`), type `landmark`;
  no `TaskSchema` may type a parameter as `landmark` (rejected at load); only a scripted `MoveTo`
  targets one.
- Work order: every assigned task appears exactly once in the script, by provenance; foreseeable
  tasks, unassigned non-foreseeable tasks and hand-written primitives are free; present is not
  completed (abandon passes); a change of mind needs both tasks assigned; empty `assigned_tasks`
  skips the check. The old key-equality check is gone (TODO-86 closed); TODO-87 stays.
- Human executor action-level; the human's task completions are known to the robot's mind from the
  world (a hypothesis retires on its terminal completion); nothing in `shared/` reads another agent's
  `current_task` (the human's is `None` now, checked by grep).
- Recorded for T-D: TODO-92, the robot's mind keeps an observed history of the human's tasks
  (completed / dropped / `unknown` episodes) for evaluation; the robot taking over an abandoned task is
  TODO-15, not now. TODO-85 half (a) (a stay as evidence, a duration term) is T-H if ever taken up.
- Authoring convention: a script ends with the human leaving the workspace unless the scenario is
  about the terminal stand.
- Author note (glossary): an injected task that returns the held item leaves the resumed `place`
  failing; write the return explicitly or use `abandon`.

Phase 7 (recorded, not decided): a run-time deviation is the same operation as a load-time edit; the
human executor's injection path serves both; the robot's mind receives nothing from either; the
replay rule is the phase's first decision (a fixed button set, every event logged with its tick, a
live run exports as a pre-loaded script; live runs demonstrate, pre-loaded scripts evaluate); events
may cut the current action at the tick they arrive (the export writes the human's position as the
split point). Readiness lines (a), (b), (c) are in section 4 of the Phase 7 handoff: (a) yes as is
(a splice into `HumanAgent.script` past `script_index`; `load_script()` restarts the index, so the
event path needs its own splice call); (b) mechanism exists, needs one small public `HumanAgent`
method; (c) `expand()` accepts any `WorldState`, run `check_script_bindings` on injected content.

## 5. The plan (roadmap "The plan from T-A", with this chat's changes)

Done: Phase 4C; T-A; T-B (T-B1a to T-B1d, T-B2a to T-B2d, T-B Q6, T-B Q7, T-B3); D3; TODO-90; T-C
(T-C1, T-C2a, T-C2b, T-C2c, play).

Next, in order, for the new chat:
1. **T-D**, robustness in kitting on the script: the opening agenda in section 6.
2. **T-E**, the viewer: shows belief, admitted projection, decision, hold, refusal, and now the
   script's events; check `mesa_sim/viz/` first.
3. **T-F**, evaluation (Phase 5): the randomised harness (TODO-47), factors `cost_strategy` x
   `gate_strategy` x `strategy` x `separation_stop` x prior, metrics on `recognition_changed`,
   completion from the world fact, blocked time, wrong-task ticks (TODO-92's history is the ground
   truth for the last); a robust crossing case for realized cost; TODO-84 (expected realized cost
   over the belief) as a later item.
4. **T-G**: second domain in Mesa (dock_loading, TODO-81), 4D detour, ROS (TODO-75, Phase 6 in the
   roadmap's numbering).
5. **Two-table re-examination of the recognizer and B2**: its own task after T-B, unscheduled
   (roadmap line, four points).
6. **Phase 7**: interactive deviations and a context stream; own chat, own revised handoff; not this
   chat's work beyond its agenda line.

The documentation pass for the paper comes before the paper, not before the demonstration.

## 6. T-D in detail: the first task of the new chat

T-D as recorded (design_decisions.md "Robustness is tested in kitting", TODO-80, D2): scenarios for a
change of mind mid-task, a walk to an empty corner (`unknown` as outcome), a declared stay at the
table (the blocked case); the blocked event in `ExecutorState`, the trigger routed past B2 as
`no_current_task` is, the response pair WAIT against RECONSIDER; measured on blocked time and
completion, and on whether retraction and re-recognition fire and whether `unknown` leads.

What the T-C play already showed (analysis/tc2c_scripts/play.md; the T-D agenda block at the end of
TODOS_AND_DEFERRED.md), so T-D starts from observations, not expectations:

1. **The robot is blind after every human task completion** (TODO-85 (b), general form). The
   episode boundary resets the belief to the prior, below θ; no projection is admitted; the human is
   standing at the table it just delivered to, which is where the robot delivers. scenario_72: the
   robot's carry passed 0.78 cm from the standing human mid-run; six other scripts show 1 to 15 cm at
   the end of the run with the stop off. The stop is the only guard. The recorded candidate: under
   `unknown` (or no admitted hypothesis) project the human as stationary at its current position for a
   bounded horizon, so that `realize()` prices holds against where the human is; how the horizon is
   bounded is part of it. This is T-D's first design question (T-D Q1) and is meta-planner-side.
2. **Re-recognition inside an episode depends on the length of the misleading walk** (TODO-94). The
   excess path a walk lays against the hypotheses it does not serve persists until a task completion
   resets legs and origins. A short misleading walk (12 to 22 ticks) lets the new task recover; a
   long one (77 ticks) never does and the robot sees `unknown` for the whole second delivery. The same
   mechanism hides a foreseeable task (scenario_41's `coffee_break`). This is the retraction case T-D
   was meant to test; the recognizer has no mechanism for it. Recognizer-side (T-D Q2). Note the
   anchors cannot express a turn mid-walk; "change of mind before the pick-up" means the human reaches
   the item first and then turns.
3. **TODO-93**: a foreseeable task finishing inside an assigned delivery ends the episode and resets
   the belief while the item is visibly in hand (scenarios 11, 12, 41, 72). Recognizer-side (T-D Q3).
4. **TODO-87**: a wrong-table delivery pins nothing and ends no episode; afterwards the assigned
   delivery leads again at about 0.9 and the robot projects a human carrying the item back to its
   designated table while the human stands (scenarios 85, 92). A stale projection under a frozen
   belief. Recognizer and meta-planner (T-D Q4).
5. **The stop's deadlock comes only from the end-of-script stand** (TODO-80); a stay that ends is
   waited out (scenario_94 stop on: refused 144 to 186, completed 413 against 370). T-D's blocked
   fixture uses a stay that ends; the authoring convention covers the rest. The blocked event and
   WAIT/RECONSIDER are then built on it (T-D Q5, the recorded design).
6. `unknown` with an exhausted hypothesis space (the human finished its work order) reads 0.995 and
   is indistinguishable from `unknown` as unmodelled behaviour (scenario_01, 06). T-D decides whether
   the distinction matters for `update()` (part of T-D Q1).
7. Smaller: a hold can put the robot at the human's projected destination (scenario_94: hold placed
   at kitting_table_1, the human walked up to the standing robot, 1.1 cm; consistent with F1, but
   matters for how the demonstration looks). Layout4's beliefs are diffuse (wide hypothesis space).

Proposed order for the new chat (Hadi rules): T-D Q1 (stationary human under no admitted
hypothesis) first, since it is the safety gap and every other item shows through it; then T-D Q5
(the blocked event and WAIT/RECONSIDER, the recorded design, on a stay-that-ends fixture); then the
recognizer items Q2, Q3, Q4 as one recognizer pass (they share the episode-boundary and evidence-
reset questions; docs/recognizer_handback.md is the recognizer's record); TODO-92's observed history
alongside. Fixtures for T-D: from the 22 play scripts and the two C2c fixtures, chosen by Hadi;
cheap form; prior on.

Things T-D must not do: add a hypothesis for a script action; read the script from the robot's
mind; set any constant from a scenario; add a heuristic timing correction to the executor.

## 7. Open flags and housekeeping (not blocking)

- TODO-89 (arrival-radius geometry decides conflicts at s with a margin of the order of the
  projected-vs-executed stop point, 10 to 15 cm), TODO-74 (placement positions): same subject, open.
- TODO-91: the executor's `[stop]` label window against the glossary's (plan-span intersection).
- `permutation_costs.py` prices only from the robot's start; `analysis/tb1c_realized_flip/check.py`'s
  `task_committed` test is vacuous; t6 and ablation READMEs note their `task_committed` column is 0.
- Older analysis folders (t6_ablation, d2, g1) are not maintained as baselines; frozen READMEs carry
  superseding notes where they were wrong (the ablation README).
- The robot's own per-task completion tick (an executor artefact a real body would not have): one
  line in TODOS, later.
- Undeclared effects the successor state does not need today (TODO-07); TODO-15; TODO-71; TODO-75;
  TODO-81; TODO-84; TODO-88 (with the prior off, a live hypothesis about the human whose item the
  robot is carrying away).
- pytest is installed in `teamrob-sp4-env`; `tests/test_script_layer.py` runs through it.
- The paper-facing documentation pass before the paper.