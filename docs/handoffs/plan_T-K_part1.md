# T-K part 1: the plan of the build of context knowledge

Written by ccode on 4 October 2026 (T-K part 1, step 2; BUILD DISCIPLINE, step 1: plan only, no code). For review by
Hadi in the design chat. Nothing in it is built or approved. Once approved, every build session of T-K part 1 reads this
file first, then `CLAUDE.md`, `docs/glossary.md`, `docs/context_knowledge_method.md` and the T-K entries
(`docs/design_decisions.md`, "T-K: context knowledge in the recognizer's belief"; `docs/design_records.md`, "T-K").
The rulings fix what and why; this file proposes how, the names and the build order. Where it proposes something the
records do not rule, it says so and names the decision (section 7, D1 to D10).

State at writing: HEAD 2602c7a (the records of AM40, AM41, KT13, KT14). Every layout of both domains holds at most one
A/C switch (step 1). Durations are in ticks (one tick is 2 seconds in both domains).

## 1. What the build contains, and what it leaves out

From the records (THE CUT AND THE QUEUE as amended; CONTENT POINTS 1 AND 2; AM30 to AM41; the method document):

- The prior of R2 to R4 with crisp facts and the three levels (AM36 to AM38): per foreseeable task a suppressing and a
  raising condition, each one fact or a conjunction of facts over three sources (a timeline fact, an object state, a
  recency fact); no "not", no "or".
- The timeline of context facts: the setup's default and a scenario's own, which replaces it whole (AM34, AM40); the
  run's header prints the timeline in force and its source.
- The declared context knowledge per domain (AM26, AM37, AM38): the facts that exist, the suppressed and the ordinary
  strength, per foreseeable task its conditions, its raised strength, the sources and its recency duration (declared in
  physical time, converted by the body). It replaces the class `ContextKnowledge` in `shared/knowledge.py`.
- The memory of observed completions, a component of the mind outside the recognizer (AM27, AM30, AM33).
- ac_on: the A/C switch's state and its setting by ac_activation (AM18); in dock_loading the object type `ac_switch`,
  the task ac_activation and the fact room_warm (no switch in its three rooms).
- The two run options `assignment_knowledge` (renamed from `assignment_prior`) and `context_knowledge`, both on by
  default (AM3, AM9); `docs/assumptions.md` 1.4 updated.
- The removal of the domain task names and constants from the recognizer, the long-shift rule with them, nothing in
  its place (AM22, TODO-66).
- The instruments: the IRB's oracle computes the new prior; its reports label each case by the state the script meets
  (KT14, replacing KT11's A, B, C); the A/C's measure is its belief at arrival (KT10) (NOTES FOR THE BUILD'S PLAN).

Left out (records): degrees, "not", "or", the long-shift replacement (T-K part 2); the override of the timeline
(AM41, later work); a change of a fact during a run (interactive phase); a condition per hypothesis (TODO-164); A/C
deactivation (TODO-163); a share for "none of the modelled tasks" (TODO-155). Not in the build, but after it (5.7 of
the forward inputs): the authoring of the timelines and the runs with context knowledge on (step 4), the two MPB cases
(step 5), dock_loading's re-measurement (step 6).

## 2. The three parts of context knowledge, and what an artefact may state

Held in three places, kept separate in the code:

| part | what | held in | reaches the mind |
|---|---|---|---|
| declared context knowledge | which facts exist; per foreseeable task its suppressing and raising condition, raised strength, recency duration; the suppressed and the ordinary strength; each with its source | the knowledge component (`shared/knowledge.py`), declared once per domain in its registry beside the task model | directly, as the task model does (AM26) |
| the facts that hold at a tick | the timeline facts in force, the A/C switch's state | the world: the run's timeline and the environment's object states | through the world state, `WorldState.predicates` (AM25) |
| the memory of observed completions | the tick of each observed completion | the robot's mind, its own component outside the recognizer | the recognizer reads the recency facts derived from it, as an input on each run (AM30) |

The timeline is not stored in the knowledge component: it is an artefact of the run (the setup's or the scenario's),
resolved at load by the simulator and read through the world state only.

A setup and a scenario state only when facts hold (a timeline) and the initial state of an object (the setup's
`"states"` block). Neither can state a condition, a strength or a recency duration: the loader's form for a timeline
has no field for them, and the declarations exist only in the domain's registry. Reason (Hadi, 4 October 2026): a rule
is knowledge about the human at this kind of site and is shared by every setup and scenario of the domain; a value
stated per setup could be chosen per test.

Contradictions found, not resolved:
- The present code holds facts in the knowledge component: `ContextKnowledge` (`shared/knowledge.py:258`) carries
  `room_temperature` and `shift_start_step`, and the recognizer holds the thresholds and boosts
  (`shared/recognizer.py:246-250`). The build removes both as ruled (TODO-66); the plan does not keep them in any form.
- The A5 form of the setup's `"states"` block admits a fact about no object (`SimModel._init_states`: "object" omitted).
  If the timeline facts take that form (section 3.2), a setup could state a timeline fact as holding from the start
  through `"states"`, a second way beside the timeline. Not a contradiction of the point above (it still states only
  when a fact holds), but two ways to state one thing: D9 proposes refusing it.
- No record contradicts either point. AM18 ("a setup may state its initial state") is the second kind of statement.

## 3. The structure

### 3.1 The mind (`shared/`)

`shared/knowledge.py`, the declared context knowledge (replaces `ContextKnowledge`; the class keeps the name, since the
glossary's term is "context knowledge" and the old class goes whole):
- `Strength(value: float, source: str)`: value > 0, checked at construction (AM4).
- A condition fact, one base class `ConditionFact` with three subclasses (a closed family, not a Union of unrelated
  types):
  - `TimelineFact(state: StateDeclaration)`: a fact about no object (`object_type` None); holds iff its predicate
    `Predicate(name, ())` is in the world state's predicates;
  - `ObjectState(state: StateDeclaration)`: a state about an object type; holds iff the state holds for an object of
    that type in the world state (D3);
  - `RecencyFact(task: PersonalTask)`: holds iff the task is among the recency facts the recognizer is given.
- `Condition(facts: Tuple[ConditionFact, ...])`: a conjunction, at least one fact.
- `ForeseeableKnowledge(task: PersonalTask, suppressing: Optional[Condition], raising: Optional[Condition],
  raised: Optional[Strength], recency: Optional[RecencyDuration])`; `raised` present iff `raising` is;
  `RecencyDuration(duration: str, source: str)`, an ISO-8601 duration in the form wait_at's binding uses, converted by
  the body.
- `ContextKnowledge(suppressed: Strength, ordinary: Strength, tasks: Sequence[ForeseeableKnowledge])`, with
  `strength(task, predicates, recent) -> Strength`: the suppressing condition first, then the raising, else the
  ordinary (AM36). Validated at construction: one entry per task; a `RecencyFact` names a task that declares a recency
  duration. Validated against a robot's `TaskModel` when the robot is built with context knowledge on: every
  `PersonalTask` of the task model has an entry, and no entry names a task outside it (AM4).
Identity throughout: tasks by schema object, states by their `StateDeclaration` object. No name is compared except the
predicate's name against its declaration's, which is how every condition already reads the world (the planner's
`ConditionSchema`).

`shared/completion_memory.py` (new), `ObservedCompletions`, the memory of observed completions (AM30): built per robot
for its observed agent, with the task model and the hypotheses of the foreseeable tasks that declare a recency
duration. `observe(agent, world)` decomposes each of them for the observed agent with the planner (`decompose`, the
query the recognizer's pin uses) and records, per task, the tick at which its terminal action's completion predicate
first holds after a tick on which it did not (AM33; D6). `recent(tick, durations) -> FrozenSet[PersonalTask]`: the
tasks with a completion at t_obs and 0 ≤ tick − t_obs < d, d in ticks. It stores nothing else.

`shared/recognizer.py`:
- Removed: `TEMPERATURE_BOOST`, `FATIGUE_BOOST`, `HIGH_TEMP_THRESHOLD`, `LONG_SHIFT_THRESHOLD`, `_context_weight`, the
  `ContextKnowledge` import as used today, the ω lines of the module docstring.
- The constructor takes `context: Optional[ContextKnowledge]` (None: context knowledge off) in place of today's
  `context`.
- `update(obs, world, prev_belief=None, recent=None)`: `recent` is the recency facts of this tick (a frozenset of
  tasks), required when context knowledge is on (an error if missing), ignored when off.
- `_output` multiplies the evidence by the prior's weights in place of ω (section 4). Nothing is fed back; `_evidence`,
  `_base`, the boundary and the re-entry are unchanged in arithmetic.
- Renamed (the prior base, AM1): `_prior()` to `_equal_evidence()`, `_initial_prior` to `_initial_evidence`; the
  docstrings say "evidence" where they say "prior" for the boundary and the re-entry.
- A module-level pure function `context_prior(groups, strengths)` (section 4), so the tests check it without a
  recognizer.

`shared/types.py`: `BeliefState` gains `prior: Dict[str, float]` (the prior over the live hypotheses, normalised;
empty when context knowledge is off) and `levels` (per foreseeable task with a live hypothesis, its level: a small enum
`StrengthLevel` SUPPRESSED | ORDINARY | RAISED); both with empty defaults, so existing constructions stay valid.
`Timeline` and `Window` (3.2) live here beside `ScenarioConfig`, which holds one; the mind never reads them.

### 3.2 The world and the artefacts

- Timeline facts take the A5 form, as the requirement on stage 1's plan intended ("context knowledge then needs no
  second mechanism", records "T-G", C1, T-K PART 1): each is a `StateDeclaration(name, None)` in the domain's
  `"states"`. Checked at load: no action's effect or retraction names a timeline fact (AM20, AM32).
- `Window(fact: StateDeclaration, start: int, end: Optional[int])` in ticks, half-open [start, end), `end` None to the
  run's end; `Timeline(windows: Tuple[Window, ...])` with `facts_at(tick) -> FrozenSet[Predicate]`. Checked at load:
  the fact is a declared state about no object, start ≥ 0, start < end, no two windows of one fact overlap.
- The setup's JSON gains an optional `"timeline"` list of `{"fact": <declared name>, "from": <tick>, "until": <tick>}`
  (`until` optional), resolved at load against the declarations as the `"states"` block is. Absent: the setup has no
  timeline. `[]`: an empty timeline.
- `ScenarioConfig.timeline: Optional[Timeline] = None` (None: not stated; `Timeline(())`: stated empty). The domains'
  `script.py` gain a call form `window(fact, start, end)` with the domain's declaration objects (no string).
- One resolution at load, `SimModel._timeline_in_force()` (or a pure function beside the overrides): the scenario's if
  stated, else the setup's if it has one, else none; returns `(Timeline, TimelineSource)`, `TimelineSource` SCENARIO |
  SETUP | NONE. AM41's override later becomes a third branch here, before the other two; nothing else changes.
- The environment applies it as a function of the tick: `build_world_state` adds `model.timeline.facts_at(t)` to the
  predicates, t = `schedule.steps` (the world state's own timestamp). No per-tick mutation of `state_facts`.
- One new line after the `[run_mesa]` start line, in every log: `[run_mesa] timeline source=<scenario|setup|none>
  windows=[<fact> <start>..<end> ...]`.
- ac_on: a `StateDeclaration("ac_on", "ac_switch")` in both domains' `"states"`, set by ac_activation's last action
  (D2). The setup may state it in `"states"` (AM18).

### 3.3 The domains

- Kitting `registry.py`: `"states"` gains break_time, room_warm (timeline facts) and ac_on; a new key
  `"context_knowledge"`: suppressed 0.005, ordinary 0.02 (source: AM17's sentence); coffee_break: suppressing its
  recency fact, raising break_time, raised 2 (AM38's source), recency PT180S (90 ticks); ac_activation: suppressing
  ac_on, raising room_warm, raised 0.5 (AM38's source), no recency.
- dock_loading: the same states; ac_activation added to the tree and the task model (methods: D4) with the action of
  D2; the object type `ac_switch`; `"context_knowledge"`: coffee_break as kitting, ac_activation as kitting,
  office_break: suppressing its recency fact, no raising, recency PT270S (135 ticks). No layout gains a switch.
- No layout, setup or scenario changes in the build except: none. (The timelines are authored in step 4.)

### 3.4 The body and the run options (`mesa_sim/`)

- `assignment_prior` renamed `assignment_knowledge` everywhere (section 6); `context_knowledge` added: the CLI flag, the
  run file key, `BOOL_OPTIONS`, `resolve_model_params`, `SimModel`. Both default on in `configs/experiment.yaml` and in
  the loader's fallback (AM3; TODO-139). `SimModel` takes both without a default (D10).
- `RobotAgent`: builds `ObservedCompletions` when context knowledge is on; per tick (and in `observe_initial`):
  world → `memory.observe` → `recent` → `recognizer.update(..., recent=recent)`. The recency durations are converted by
  the body's `_parse_duration_to_steps`, as wait durations are.
- One new line per tick when context knowledge is on, after `[IR-dist]`: `[IR-context] step=N facts=[...]
  recent=[...] levels=[<task>=<level> ...] prior=[<key>=<p> ...]` (prior to 4 decimals). Nothing when off.
- `[run]` header: `assignment_knowledge=on|off context_knowledge=on|off` in place of `assignment_prior=on|off`.

## 4. The prior, the belief, and the check against the method

The recognizer groups the live hypotheses (the keys of `_evidence`, H): a `WorkTask` hypothesis belongs to the
assigned tasks as a whole (with assignment knowledge on only the assigned ones are live; with it off every work task's,
as AM3/AM35 rule); a `PersonalTask` hypothesis to its task f. This reads the schema's class, as `_build_admissible`
already does, and no name. Strengths come from `context.strength(f, world.predicates, recent)`.

`context_prior(groups, strengths)` returns the weights w(h) = 1/|A| for h in A, s_f/|H^f| for h in H^f (section 6 of
the method). The normaliser Z cancels in the belief's normalisation, so `_output` multiplies the evidence by w and the
existing normalisation does the rest; π = w / Σw is computed for `BeliefState.prior` and the log.

Proposal P1 (not a design change): with context knowledge off, w(h) = 1.0 exactly, not 1/|H|. Multiplying by 1.0 is
exact in floating point, so every off run is identical by construction, not up to rounding; 1/|H| would be the same
belief mathematically and could flip a printed third decimal.

The check against the method document (requirement 5), as unit tests in `tests/test_tk_prior.py` (framework-wide):
- Section 10's eight rows: a `ContextKnowledge` with kitting's declared values; per row the predicates (break_time,
  room_warm, ac_on(switch)), the recent set and the live groups (n deliveries, one coffee machine, one switch); π per
  hypothesis against the table at its rounding (tolerance 5e-4); Σπ = 1 to 1e-12.
- Section 4's order: the suppressing condition wins over the raising (row 3, row 5).
- Section 11: the invented evidence gives 0.825 in state 2 and 0.926 in state 1.
- Section 12: state 7's 0.8 against 0.2, and the 0.77 example.
- Section 13: with context knowledge off the belief equals the normalised evidence exactly.
- AM4: a zero or negative strength, a foreseeable task without an entry, are refused at load.
Plus a test that the recognizer with context knowledge off returns the same `BeliefState` as before on a recorded run
(`test_td1_adequacy`'s fixture), and that `shared/recognizer.py`, `shared/knowledge.py` and
`shared/completion_memory.py` hold no string literal naming a task, a fact, an object or a domain (a grep in the test).

## 5. Facts from the code (a to g), reported without resolving them

**(a) Which value the gate compares with θ.** `MetaPlanner._clears_gate` compares `belief.confidence`
(`shared/meta_planner.py:758`). `confidence` is `distribution[most_likely]` (`shared/recognizer.py:879`), and
`distribution` is the output (`_output` → `_finalize`, `:1159-1186`; `docs/recognizer_handback.md` §1.7): the evidence
× ω normalised over H, then each live value floored at `BELIEF_FLOOR` = 0.001 and renormalised, then the live mass
scaled by 1 − 0.001·|pinned|, |pinned| the inadmissible, retired and inapplicable keys. So the gate reads the output
after the floor and the pin scaling, not the belief over H.
- What the scaling is for, from the code: the pin makes the reported distribution span the whole hypothesis space and
  sum to 1 (`_pin`, `:640`); the floor's stated reason is that a value at exact zero cannot recover through a
  multiplicative update (`:1177`). The output is no longer fed back (`prev_belief` is not consulted, `:720-723`; the
  evidence carries no floor), so in the present structure neither reason acts on the inference: both are an output
  convention that the gate inherits.
- What each value means. The belief over H (the method's P_t, R2) depends only on the live hypotheses, the evidence and
  the prior. The output also depends on how many keys of the space are not live (unassigned items, completed tasks,
  inapplicable ones): with k pins a belief of 0.75 over H reads 0.75·(1 − 0.001k), 0.746 with k = 5. That number of
  pins says nothing about the human's intention.
- Where the prior meets it: prior × evidence is normalised, then floored. Small priors make the floor bind more often:
  a suppressed task (prior about 0.005) with an evidence share below about 0.2 falls below 0.001 and is lifted, which
  lowers every other live value slightly. The reported belief then differs from the method's P_t.
- Bearing on the regression: moving the gate to the belief over H changes gate outcomes near θ with context knowledge
  off too (requirement 1 would then name gate lines); KT10's two A/C cases peaking at 0.746 and 0.745 are of this
  size. Not measured here. D1.

**(b) The edges of a window and of a recency duration.** The world state the robot reads at tick t is built during
the model's step t (`build_world_state`, timestamp `schedule.steps`, `mesa_sim/world_state_builder.py:97`); the
scheduler increments the step after every agent has acted (`mesa_sim/mesa_fork/time.py:112-113`); the human acts
before the robot within a tick, and the observation carries the same t (`sim_agents.py:435`). The pre-clock
observation (`observe_initial`) also reads t = 0. So every fact the robot reads carries one tick, and the half-open
window [a, b) means: the fact holds in every world state with timestamp t, a ≤ t < b (b − a ticks). A recency fact with
t_obs the first tick the terminal fact holds holds on t_obs … t_obs + d − 1 (d ticks). The human reads no timeline fact
(R1), so its being one step ahead within the tick does not matter. The half-open reading of the method's section 3
fits; nothing in the code reads a fact between ticks.

**(c) When the robot observes a completion.** The recognizer runs on every tick on which the robot has an observed
human, before the empty pool's return (`sim_agents.py:428-443`, `:483-484`; the cognitive-loop ruling): with no task,
while holding, after its pool is empty. An observed completion is the terminal fact in the world state (AM33):
waited(agent, machine) is set on the wait's last STAND and cleared on the agent's next step
(`world_state_builder.py:131`; `executor.py:441`), so it typically holds on one tick, the tick the human completes
the wait (it acts first). The robot reads that tick, so the memory can record at the completion tick with no lag,
provided it reads before the recognizer (3.4). A robot with no observed agent observes nothing (`_get_observed_human`).

**(d) The prior multiplying the evidence without being folded in.** It can, in the present structure. The recognizer
keeps the normalised evidence `_evidence` separate from the output; ω is applied in `_output` only and never fed back
(`:1159-1168`, `:720-723`). The prior takes ω's place there. The boundary (`_begin_episode`) and the re-entry
(`:838-848`) already act on the evidence, as AM1 rules; only their names say "prior". One consequence to note: a change
of the prior alone (a window edge, a recency fact ending) can change the leader, so `recognition_changed` may fire on
it; AM21's "no trigger" holds (the change acts only through the belief).

**(e) The renames the records assign to the build, and the lines each changes.** Section 6.

**(f) The cost of the instruments.** Section 9.

**(g) What cannot be built as ruled, with the evidence.**
1. "ac_activation sets ac_on" (AM18) and "a declared effect of ac_activation" (5.3 of the forward inputs): effects are
   declared on action schemas (T-G A5), and ac_activation's terminal action is `wait_at` (`domains/kitting/tasks.py:110`),
   shared with coffee_break. An effect ac_on(?entity) on `wait_at` would ground to the coffee machine, which the
   environment refuses (`SimModel._state_fact`, a type mismatch raises). It needs a decision: D2.
2. An object-state condition is evaluated per task (AM2's CLARIFIED line, AM36), but ac_on is a state of one object.
   The records do not say how the per-task condition grounds it. With at most one switch per layout (AM18) every
   reading gives the same value; the form must still pick one: D3.
3. dock_loading's ac_activation needs methods; dock_loading's human tasks have one method per area the human can be in
   (T-G B content, the hall and the office). The records do not say where a switch would stand. D4.
4. Nothing else found. The floor's interaction with the prior is a fact of (a), not a block.

## 6. Renames, and every log line the build changes

With context knowledge off, the lines that differ from today, all named:

| line | change | where | cause |
|---|---|---|---|
| `[run]` | `assignment_prior=on` → `assignment_knowledge=on context_knowledge=off` | every log, once per robot | rename (AM9), new option (AM3) |
| `[IR-prior] switch=on known=[...]` | → `[IR-assignment] knowledge=on known=[...]` | every log with an observing robot | rename (AM9; glossary names `[IR-prior]` as the old name) |
| `[run_mesa] timeline ...` | new, after the start line | every log | AM40 |
| `[rec]`, `[human]` | the action name of the A/C activation (if D2 takes a new action) | runs whose script holds ac_activation (maintained: scenario_s02_01, scenario_s04_01) | D2 |
| everything from step 500 | the long-shift rule's ×2.5 on coffee_break gone | runs of 500 steps or more with a coffee_break hypothesis live: none of the four maintained sets (450 the longest), none of kitting's IRB, MPB or round 1 run files (481 the longest); dock_loading's 11 MPB run files of 531 to 858 steps (22 runs, the recorded caveat) and the milestone runs (800, 1000 steps) | AM22, TODO-66 (C1's correction) |

Unchanged with context knowledge off: `[IR]`, `[IR-dist]` (bit-identical by P1), `[IR-boundary]` (its words "belief
re-initialised to the prior" stay true: at a boundary the evidence is equal, so the belief is the prior), every
`[meta*]`, `[hold]`, `[sep]`, `[coverage]` and `[scenario-coverage]` (dock_loading's task model gains ac_activation but
no script names it; checked in the diff). If D2 takes a new action, the `[IR-boundary]` label stays `wait_at(...)` for
an A/C completion (terminal actions in declaration order: `_observed_terminal_completion` returns the first), to be
confirmed by the diff.

Renamed in code, configuration and commands (assigned by the records):
- `assignment_prior` → `assignment_knowledge` (AM9): the CLI flag, `configs/experiment.yaml` and every run file under
  `configs/` (145 files: kitting irb 17, tk1 31, mpb 16; dock_loading irb 54, mpb 26; one shared), `SimModel`'s keyword
  and attribute, `resolve_model_params`, `BOOL_OPTIONS`, the four maintained `sweep.sh`, the instruments
  (`irb/actual.py`, `mpb/actual.py`, `mpb/reference.py`, `mpb/run.sh`, `common/tdlib.py`'s `[IR-prior]` and header
  parsing), three tests, two scenario descriptions that quote the flag (left: descriptions are history). Strict parsing
  refuses the old key, so the rename and every run file go in one commit. Frozen folders' scripts
  (`f47_fixtures`, `ablation_task_committed`, …) are not edited and no longer run as written; their READMEs say which
  commit they ran at.
- The context weight (ω_context, `_context_weight`) and its constants: removed, not renamed.
- The prior base (`_prior`, `_initial_prior`): renamed to say evidence (3.1). No log line names it.
- `ContextKnowledge`: replaced whole (3.1); its two test call sites (`test_td1_adequacy`, `test_th1_tree`) pass None.
- Docs at the build: `docs/assumptions.md` 1.4 (the default on, both settings), `shared/io_contracts.md`
  (`BeliefState`), `docs/recognizer_handback.md` §1.7 and §2 (ω gone, the prior), the glossary's BUILT lines, CLAUDE.md
  (its commands name `--assignment_prior`; its state), the roadmap, TODO-66 closed, TODO-139.

## 7. Proposals and decisions for Hadi

Proposals that change no design (taken unless Hadi objects):
- P1 the off prior as exact unit weights (section 4).
- P2 the timeline as a pure function of the tick read by the world-state builder, not a mutation of the environment's
  facts each tick: one object resolved once at load, which AM41's override can replace in the same place; the IRB's
  mirror model gets it with no code of its own. AM25's "the environment applies the timeline" holds: the builder is
  the environment's.
- P3 timeline facts in the A5 form (`StateDeclaration` about no object), as the stage-1 requirement intended.
- P4 the level per task and the facts read in the knowledge component (`ContextKnowledge.strength`); the recognizer
  only groups and divides. It keeps every fact, name and value out of the recognizer (requirement 2) and makes the
  three levels testable alone.
- P5 `recent` passed to `update()` explicitly, not through the world state. Alternative: a field of the robot's world
  model, as P4 (T-D) does with the perceived motion; not taken, because AM27 says the world state holds no history.

Decisions:
- D1 (open item, a design question). Which value the gate compares with θ: (i) the output, as today, after the floor
  and the pin scaling; (ii) the belief over H, P_t of the method. My reading of what each means (section 5 a): (ii) is
  the quantity R2 defines; (i) adds the count of non-live keys and the floor, which say nothing about the human. If
  (ii), the floor and the pin stay for the reported distribution only, and the change is its own stage with its own
  regeneration, since it moves gate outcomes near θ with context knowledge off. Alternative (iii): (ii) only when
  context knowledge is on; not recommended, as the gate would then read two quantities by a run option.
- D2. How ac_activation sets ac_on: (i) recommended, a new action schema in both domains for the A/C's activation (for
  example `switch_on(?entity)`), the same form as `wait_at` (STAND*, a duration, completion waited(agent, entity)) with
  the effect ac_on(?entity); the body executes it by its fields as it does `wait_at`, so nothing in the simulator
  changes; the action's name changes in `[rec]` and `[human]` (section 6). (ii) an effect on `wait_at` applied only when
  the object has the state's type: a hidden rule in the environment, and the projector's successor state would carry
  ac_on(coffee machine). (iii) the robot inferring ac_on from waited(agent, switch): the robot deriving a state from an
  observed action, "not taken" in T-G A5.
- D3. An object-state condition per task holds iff the state holds for some object of its declared type in the world
  state. With at most one switch per layout it is that switch's state. Alternative: grounding through the task's own
  parameter (per hypothesis, TODO-164's direction); not taken in V1.
- D4. dock_loading's ac_activation: two methods mirroring coffee_break's (from the hall: walk to the switch, activate;
  from the office: walk to the office door, then to the switch, activate), so a switch stands in the hall. Unexercised
  in V1 (no switch in its rooms); it must exist for the tree and the task model (AM18).
- D5. The windows: in ticks (AM11's "from one authored tick to another"), half-open (5 b), `until` optional (to the
  run's end), overlapping windows of one fact refused.
- D6. The memory records a completion when the terminal fact holds on a tick after one on which it did not; a fact
  already holding at the first observation is not recorded (not observed completing). It records only the tasks that
  declare a recency duration (nothing else reads it).
- D7. The build's regression scope beyond the four maintained sets (section 8): round 1's 31 runs with context
  knowledge off, and dock_loading's three milestone runs; the 22 dock_loading MPB runs stay with step 6 (the recorded
  open question).
- D8. The instruments' check under context knowledge on (section 9): round 1's 31 scenarios run on, compared with the
  oracle for agreement only, no reading of the results (their timelines are empty, so every case meets the ordinary or
  the suppressed state). The reading belongs to step 4.
- D9. The setup's `"states"` block refuses a timeline fact: a timeline fact is stated by a timeline only.
- D10. `SimModel` takes `assignment_knowledge` and `context_knowledge` with no default; every caller states both. The
  defaults (on, on) live in the run file and the loader's fallback, the one place a run's defaults are set. Today 15 of
  the 18 `SimModel` constructions in `tests/` rely on its default (off); with a code default flipped to on they would change silently.

## 8. Stages, commits and verification

Each stage is one or two commits; the next starts only when its check passes. Baselines are recorded before any code
(stage 0) and every later stage diffs against them. "Named lines" means section 6's table.

0. Baselines at HEAD, no code. The four maintained sets (`sweep.sh` of tb1a, tb1b, tb1c, tb3: 48 logs and their
   `.rec`), round 1's 31 runs (`analysis/instruments/irb/run.sh kitting` on `configs/kitting/irb/tk1/`), dock_loading's
   milestone runs (scenario_s03_02, s05_02, s07_02, 800 steps; s03_03, s05_03, s07_03, 1000 steps), `pytest` (307).
   Outputs in a local folder outside git; md5s noted in the stage report. No commit.
1. The rename `assignment_prior` → `assignment_knowledge` (one commit: code, every run file, sweeps, instruments, tests).
   Check: every baseline differs in the `[run]` field and the `[IR-assignment]` line only (a diff after replacing
   those two lines is empty), `.rec` byte-identical, pytest passes.
2. The option `context_knowledge` and the removal of ω (TODO-66), off only (one commit): the flag, `SimModel` without
   defaults (D10), the run files and sweeps state `context_knowledge: false`, tests state both; `ContextKnowledge`'s old
   class and the recognizer's constants removed; `_output` multiplies by unit weights. Check: the four sets and round
   1 identical except the `[run]` field; dock_loading's milestone runs identical up to step 499 and the first differing
   step at 500 or later (one line each, not analysed); pytest passes.
3. The world's side (two commits). 3a: `Timeline`, `Window`, the setup's and the scenario's forms, the resolution at
   load, the builder, the `[run_mesa] timeline` line, the load checks (D5, D9, AM20), with tests of the resolution's
   four cases (scenario stated, stated empty, not stated with a setup timeline, setup with none). 3b: the domains'
   states (break_time, room_warm, ac_on), the A/C's action (D2) in both domains, dock_loading's ac_activation (D4) and
   object type. Check: every baseline identical except the named lines (the timeline line; the action name in
   scenario_s02_01's and scenario_s04_01's `[rec]` and `[human]`); every registered scenario of both domains loads;
   pytest passes.
4. The mind (one or two commits): `ContextKnowledge` and the domains' declarations, `ObservedCompletions`, the prior in
   the recognizer, `BeliefState.prior` and `levels`, `[IR-context]`, the run options' defaults on. Tests: section 4's
   table tests; the memory on a recorded run (a coffee_break in round 1: the recency fact holds for exactly 90 ticks
   from the tick waited(human, coffee_machine_0) first holds); the robot loads with context knowledge on in every
   registered scenario of both domains. Check: with context knowledge off, every baseline identical to stage 3's;
   with it on, the four sets and round 1 run to completion (a smoke run, not read). If D1 takes (ii), it is stage 4b,
   its own commit, with the four sets regenerated and the gate lines that move listed one line each.
5. The instruments (one commit, section 9). Check: kitting's IRB (17), round 1 (31) and MPB (16 × 2 strategies)
   outputs with context knowledge off byte-identical to the outputs before the change; under D8, round 1 on agrees
   with the oracle (0 disagreements at 1e-9).
6. Records and docs (one commit): the BUILT block under "T-K" with commits and acceptance, the docs of section 6, the
   regenerated md5s in each maintained set's README (a new section naming the lines that changed and why).

## 9. The instruments and their cost

What changes, and roughly how much:
- `irb/trajectory.py`: the row's facts include the timeline facts (from the model's timeline at the tick) beside the
  state facts. About 10 lines.
- `irb/oracle.py`: its own prior from the method document, independent of `shared/recognizer.py` (it reads the
  domain's declared values from the registry, as it reads the task model, and computes the levels, the groups and the
  division itself); its own memory of observed completions from the rows (the terminal fact newly holding for the
  observed human, D6); `output()` multiplies by the prior before the floor and the pin, as the recognizer does; new
  columns `prior` per key and `levels`. About 80 to 120 lines, with new rules in the IRB README (28 onward, each with
  its source).
- `irb/compare.py`: the new columns compared. About 10 lines.
- `irb/summary.py`, `irb/admission.py`, `irb/baseline.py`: each case labelled by the state the script meets (KT14):
  the level of the true foreseeable task at its start, and of the assigned tasks' rivals; the A/C's belief at arrival
  (KT10). About 40 to 60 lines.
- `common/tdlib.py`: the `[IR-assignment]`, `[IR-context]` and `[run_mesa] timeline` lines. About 20 lines.
- The MPB instrument: its oracle imports the IRB's unchanged, so the gate's expected outcome follows the new belief;
  only the rename in `mpb/actual.py`, `mpb/reference.py`, `mpb/run.sh`. Part 4's measures are unchanged.
Cost: one build session for the code and the README rules; the verification reruns of stage 5 (kitting's 17 + 31 IRB
runs, the MPB's 32), each through the run, the trajectory, the oracle and the comparison, as the sort's preparation
did; their wall time is measured at stage 0 and stated in the stage report. dock_loading's 54 IRB and 52 MPB runs are
not rerun in the build (step 6 re-measures them).

## 10. Cases the design does not cover

Each is either a decision of section 7 or recorded here for Hadi:
- D2, D3, D4, D6 above.
- A timeline fact whose window opens while the robot's decision rests on a projection: the prior changes, possibly the
  leader, and `recognition_changed` may fire (5 d). Ruled behaviour (AM21), stated so the runs are not surprised.
- A foreseeable task with no live hypothesis contributes nothing to Z (method section 6); a task whose only hypothesis
  is retired (just completed) therefore takes no share on that tick, and the recency fact first matters when it
  re-enters on the next. As ruled.
- TODO-154 (the share at an episode's start) stays as recorded: the build answers nothing beyond R4.
- dock_loading's coffee_break from the office (the method document's open flag on section 12): unchanged by the build;
  observed in step 6.
