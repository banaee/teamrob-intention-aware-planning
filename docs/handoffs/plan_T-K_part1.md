# T-K part 1: the plan of the build of context knowledge

Written by ccode on 4 October 2026 (T-K part 1, step 2; BUILD DISCIPLINE, step 1: plan only, no code; 41efa76).
Amended the same day to Hadi's rulings on it: the decisions D1 to D10 and two additions of the review are AM42 to AM53
(`docs/design_decisions.md` and `docs/design_records.md`, "T-K", THE BUILD'S PLAN, RULED); the proposals P1 to P5 are
accepted. Amended again the same day to Hadi's rulings on section 11 (AM54 to AM58; THE CROSS-CHECK, RULED) and on its
consequences (AM59 to AM63; THE CROSS-CHECK'S CONSEQUENCES, RULED). The plan is approved; the build has not started. Nothing in it is built. BUILT (step 3, 4 October 2026; design_records.md, "T-K", THE BUILD, STAGES 1 AND 2 and THE BUILD, STAGES 3 TO 7; the
session's state file `docs/handoffs/build_T-K_part1_state.md`): every stage of section 8 is built and checked; this
file is the plan as approved and is not rewritten to the build. Every build session of T-K part 1 reads this file first, then `CLAUDE.md`, `docs/glossary.md`, `docs/context_knowledge_method.md` and the T-K entries
(`docs/design_decisions.md`, "T-K: context knowledge in the recognizer's belief"; `docs/design_records.md`, "T-K").
The rulings fix what and why; this file fixes how, the names and the build order. Section 7 lists the decisions as
ruled; section 11 is ccode's cross-check of the rulings, with the points Hadi has not ruled on.

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
  through `"states"`, a second way beside the timeline. RULED (AM50): the `"states"` block refuses a timeline fact; a
  fact that holds from the start is a window from tick 0.
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
    that type in the world state (AM44);
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
first holds after a tick on which it did not (AM33, AM47). `recent(tick, durations) -> FrozenSet[PersonalTask]`: the
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

`shared/types.py`: `BeliefState.confidence` becomes the leader's belief over the live hypotheses (the evidence × the
prior, normalised over H, before the floor and the pin scaling): the value the gate reads (AM42); `_clears_gate` keeps
reading `belief.confidence` and does not change. `distribution` stays the reported distribution (floor, pins).
`BeliefState` gains `belief: Dict[str, float]` (the belief over H, the keys of H only; what a margin gate, TODO-65,
would read), `prior: Dict[str, float]` (the prior over the live hypotheses, normalised;
empty when context knowledge is off) and `levels` (per foreseeable task with a live hypothesis, its level: a small enum
`StrengthLevel` SUPPRESSED | ORDINARY | RAISED); both with empty defaults, so existing constructions stay valid.
`Timeline` and `Window` (3.2) live here beside `ScenarioConfig`, which holds one; the mind never reads them.

### 3.2 The world and the artefacts

- Timeline facts take the A5 form, as the requirement on stage 1's plan intended ("context knowledge then needs no
  second mechanism", records "T-G", C1, T-K PART 1): each is a `StateDeclaration(name, None)`, listed in a registry
  list of its own, `"timeline_facts"`, beside `"states"`. The loader needs to know which declared facts are timeline
  facts to refuse them where AM20, AM50 and AM52 forbid them; the A5 form alone (a state about no object) does not say
  (section 11, X5). The environment emits them as it emits states.
- Checked at load (`SimModel`, beside `_check_declared_effects`, over the world's tree, which holds every schema of
  the robot's task model too): no effect or retraction of an action schema (AM20, AM32), no precondition of an action
  schema and no guard of a method (AM52) names a timeline fact, by the condition's name against the declaration's, as
  `_check_declared_effects` reads it; a failure names the schema and the fact. The setup's `"states"` block refuses a
  timeline fact (AM50). The completion condition of an action schema is refused too (AM54): no condition of any
  schema names a timeline fact.
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
- ac_on: a `StateDeclaration("ac_on", "ac_switch")` in both domains' `"states"`, set by the action switch_on
  (AM43). The setup may state it in `"states"` (AM18).

### 3.3 The domains

- Both domains' `actions.py`: `switch_on(?entity, ?duration)`, wait_at's form (precondition at(agent, entity),
  STAND*, `duration_key`, completion waited(agent, entity)) with the effects waited(agent, entity) and ac_on(entity)
  (AM43). ac_activation's method calls it in place of `wait_at`; nothing else does.
- Kitting `registry.py`: `"timeline_facts"` holds break_time and room_warm, `"states"` gains ac_on; a new key
  `"context_knowledge"`: suppressed 0.005, ordinary 0.02 (source: AM17's sentence); coffee_break: suppressing its
  recency fact, raising break_time, raised 2 (AM38's source), recency PT180S (90 ticks); ac_activation: suppressing
  ac_on, raising room_warm, raised 0.5 (AM38's source), no recency.
- dock_loading: the same facts and states; ac_activation added to the tree and the task model with one method, from
  the hall (move_to the switch, switch_on; AM45), and switch_on in its actions; the object type `ac_switch`; `"context_knowledge"`: coffee_break as kitting, ac_activation as kitting,
  office_break: suppressing its recency fact, no raising, recency PT270S (135 ticks). No layout gains a switch.
- No layout, setup or scenario changes in the build. (The timelines are authored in step 4.)

### 3.4 The body and the run options (`mesa_sim/`)

- `assignment_prior` renamed `assignment_knowledge` everywhere (section 6); `context_knowledge` added: the CLI flag, the
  run file key, `BOOL_OPTIONS`, `resolve_model_params`, `SimModel`. Both default on in `configs/experiment.yaml` and in
  the loader's fallback (AM3; TODO-139). `SimModel` takes both without a default; a caller that states neither fails
  (AM51).
- `RobotAgent`: builds `ObservedCompletions` when context knowledge is on; per tick (and in `observe_initial`):
  world → `memory.observe` → `recent` → `recognizer.update(..., recent=recent)`. The recency durations are converted by
  the body's `_parse_duration_to_steps`, as wait durations are.
- One new line per tick when context knowledge is on, after `[IR-dist]`: `[IR-context] step=N facts=[...]
  recent=[...] levels=[<task>=<level> ...] prior=[<key>=<p> ...]` (prior to 4 decimals). Nothing when off.
- `[run]` header: `assignment_knowledge=on|off context_knowledge=on|off` in place of `assignment_prior=on|off`.
- The value the gate read is printed where it is today (AM42's requirement): `[IR] confidence=` and `[meta-proj]
  confidence=` print `belief.confidence`, now the belief over H. `[IR-dist]` keeps printing the reported distribution,
  so its leader's value can differ from `confidence` by the floor and the pin scaling; the log readers take θ crossings
  from `confidence` (section 9).

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
  size. Not measured here.
- RULED (AM42): the belief over the live hypotheses, with context knowledge on or off; the floor and the pin scaling
  stay in the reported distribution only (their removal there, TODO-178).

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
   environment refuses (`SimModel._state_fact`, a type mismatch raises). RULED (AM43): a new action switch_on.
2. An object-state condition is evaluated per task (AM2's CLARIFIED line, AM36), but ac_on is a state of one object.
   The records do not say how the per-task condition grounds it. With at most one switch per layout (AM18) every
   reading gives the same value; the form must still pick one. RULED (AM44): any object of the state's type.
3. dock_loading's ac_activation needs methods; dock_loading's human tasks have one method per area the human can be in
   (T-G B content, the hall and the office). The records do not say where a switch would stand. RULED (AM45): one
   method, from the hall; the switch stands only in the delivery hall.
4. Nothing else found. The floor's interaction with the prior is a fact of (a), not a block.

## 6. Renames, and every log line the build changes

With context knowledge off, the lines that differ from today, all named. The gate's change (AM42) is not among them:
it changes behaviour, has its own stage and its own regenerated baseline (stage 2, AM53), and every later stage is
compared with that baseline.

| line | change | where | cause |
|---|---|---|---|
| `[run]` | `assignment_prior=on` → `assignment_knowledge=on context_knowledge=off` | every log, once per robot | rename (AM9), new option (AM3) |
| `[IR-prior] switch=on known=[...]` | → `[IR-assignment] knowledge=on known=[...]` | every log with an observing robot | rename (AM9; glossary names `[IR-prior]` as the old name) |
| `[run_mesa] timeline ...` | new, after the start line | every log | AM40 |
| `[rec]`, `[human]` | `wait_at` → `switch_on` in an A/C activation | runs whose script holds ac_activation (maintained: scenario_s02_01, scenario_s04_01; round 1: the s14 and s15 scenarios with an A/C activation) | AM43 |
| everything from step 500 | the long-shift rule's ×2.5 on coffee_break gone | runs of 500 steps or more with a coffee_break hypothesis live: none of the four maintained sets (450 the longest), none of kitting's IRB, MPB or round 1 run files (481 the longest); dock_loading's 11 MPB run files of 531 to 858 steps (22 runs, the recorded caveat) and the milestone runs (800, 1000 steps) | AM22, TODO-66 (C1's correction) |

Unchanged with context knowledge off: `[IR]`, `[IR-dist]` (bit-identical by P1), `[IR-boundary]` (its words "belief
re-initialised to the prior" stay true: at a boundary the evidence is equal, so the belief is the prior), every
`[meta*]`, `[hold]`, `[sep]`, `[coverage]` and `[scenario-coverage]` (dock_loading's task model gains ac_activation but
no script names it; checked in the diff). The `[IR-boundary]` label of an A/C completion stays `wait_at(...)`: its
correction is not small and is deferred (AM56, TODO-179; section 11, X3).

The gate's stage (stage 2) changes, with context knowledge off: the value of `confidence` in `[IR]` and `[meta-proj]`
wherever a hypothesis is pinned or a live value is floored; where that moves the leader across θ, the gate's outcome
(`[meta-proj]` reason, `[meta-trig]`, `[meta]`, `[hold]`, the robot's motion and the `.rec`). Each such difference is
listed one line each in the stage's report (condition, first differing step, grep), not analysed.

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

## 7. Proposals and decisions, as ruled (Hadi, 4 October 2026)

Accepted proposals, no design change:
- P1 the prior with context knowledge off as exact unit weights (section 4).
- P2 the timeline as a function of the tick read by the world-state builder (3.2); one object resolved at load, which
  TODO-177's override replaces in the same place.
- P3 timeline facts in the A5 form (3.2), in a registry list of their own (section 11, X5).
- P4 the level per task and the facts read in the knowledge component (`ContextKnowledge.strength`); the recognizer
  only groups and divides.
- P5 the recency facts passed to `update()` explicitly.

The decisions (the plan's D1 to D10 and the review's two additions are AM42 to AM53):

| plan | ruling | what the build does | stated consequence |
|---|---|---|---|
| D1 | AM42 | the gate compares θ with the belief over H, context knowledge on or off; `confidence` is that value; the floor and the pins stay in `distribution` only | gate outcomes near θ move with context knowledge off too; the floor's and the pins' removal from the report is TODO-178 |
| D2 | AM43 | the action switch_on (wait_at's form, effect ac_on), used by ac_activation only, both domains | the action's name changes in `[rec]` and `[human]` |
| D3 | AM44 | an object-state condition holds if the state holds for any object of its type | with one switch per layout, the switch's state |
| D4 | AM45 | dock_loading's ac_activation: one method, from the hall | when a dock_loading room gets a switch, the office method is added in the same step; without it the task is not live while the human is in the office |
| D5 | AM46 | windows in ticks, half-open, the end optional, no overlap of one fact's windows | every expectation near a window's edge depends on the half-open reading by one tick |
| D6 | AM47 | the memory records the tick the terminal fact first holds after a tick it did not; not at the first observation; only tasks with a recency duration | an unobserved completion is not remembered and does not suppress; the duration counts from the completion tick, included |
| D7 | AM48, AM55 | the build's regression scope: the four maintained sets, round 1 (31, off), dock_loading's six milestone runs | dock_loading's IRB and MPB sets are not rerun in the build; a regression only they show is found at dock_loading's step |
| D8 | AM49 | round 1 run with context knowledge on, against the oracle, agreement only | no run of the build exercises a raised strength; the unit tests against the method cover it until the authored windows |
| D9 | AM50 | the setup's `"states"` block refuses a timeline fact | a fact that holds from the start is a window from tick 0 |
| D10 | AM51 | `SimModel` takes both run options with no default | a caller that does not state both fails with an error |
| review 1, X4 | AM52, AM54 | the loader refuses a timeline fact in any precondition, guard or completion condition (3.2) | context never drives the human |
| review 2 | AM53 | the gate's change in its own commit, with its own regenerated baseline (stage 2) | each later stage compares with it (section 8) |
| X3 | AM56 | the boundary label for a switch_on: not small, deferred (TODO-179) | `[IR-boundary]` names `wait_at(...)` at an A/C completion until then |
| X1 | AM57 | stage 2 reruns round 1 and kitting's IRB and MPB sets with the new gate, outputs replaced; it checks the MPB's declared properties | a declared property that no longer holds stops the build (a finding); dock_loading's IRB and MPB sets stale until its step |
| X2 | AM58 | nothing in the build (TODO-180) | the viewer is not checked for the confidence it shows |

## 8. Stages, commits and verification

Each stage is one or more commits; the next starts only when its check passes. The regression scope is AM48's: the four
maintained sets (`sweep.sh` of tb1a, tb1b, tb1c, tb3: 48 logs and their `.rec`), round 1's 31 runs with context
knowledge off (`analysis/instruments/irb/run.sh kitting`, `configs/kitting/irb/tk1/`), and dock_loading's six milestone
runs (scenario_s03_02, s05_02, s07_02 at 800 steps; s03_03, s05_03, s07_03 at 1000), plus `pytest`. "Named lines" are
section 6's table. Outputs of the checks stay local (logs are git-ignored); md5s go into the reports.

| stage | compared with | expected difference |
|---|---|---|
| 0 | (records B0) | none |
| 1 | B0 | the rename's lines |
| 2 | stage 1's outputs; the test-bed sets against their oracle | the gate's change, listed; every MPB declared property holds, else stop; then B2 and the sets' new outputs are recorded |
| 3 | B2 | the `[run]` field; dock_loading's milestones from step 500 |
| 4 | stage 3's outputs | the timeline line; switch_on in `[rec]`, `[human]` |
| 5 | stage 4's outputs, off | none |
| 6 | stage 2's test-bed outputs (off; round 1 and kitting's IRB and MPB) | none (instrument outputs byte-identical); round 1 on: 0 disagreements |

Since stages 3 to 6 differ from B2 only by named lines, each check is also "B2 except the named lines of the stages
since", which the final README sections state.

0. Baselines B0 at HEAD, no code: the regression scope above, and its wall time noted. No commit.
1. The rename `assignment_prior` → `assignment_knowledge` (one commit: code, every run file, sweeps, instruments,
   tests; `SimModel` states it at every caller). Check against B0: the `[run]` field and the `[IR-assignment]` line
   only (a diff after replacing them is empty), `.rec` byte-identical, pytest passes.
2. The gate (AM42, AM53). 2a, its own commit: the recognizer's `confidence` is the leader's belief over H, before the
   floor and the pins; `BeliefState.belief`; `_clears_gate` unchanged (it reads `confidence`); a unit test that a
   belief with pinned keys clears θ on its value over H. 2b: the instruments follow (the IRB oracle's `confidence` and
   gate columns from the belief over H; `tdlib`, `summary.py`, `baseline.py` take θ crossings from `confidence`).
   Check against stage 1: every difference is in the lines section 6 names for this stage, each listed. Before the
   reruns, the untracked data of round 1, the IRB and the MPB are copied outside the repository, one copy, named in
   each README (AM59). Then the test-bed sets, rerun with the new gate (AM57), each through its own pipeline (`analysis/instruments/irb/run.sh
   kitting` for round 1 and for the IRB's scenario_s08 and s09; `analysis/instruments/mpb/run.sh` for the MPB set, its
   variants as its README states, the prior-off appendix included as a diagnostic): the IRB sets and the MPB's parts 1
   to 3 agree with the oracle (0 disagreements at 1e-9), every declared property of the MPB's part 4 holds, and every
   scenario of the coverage matrix still reaches its authored case. A disagreement, a declared property that no
   longer holds, or a scenario that no longer reaches its case stops the build (AM57, AM61, confirmed as three by AM64): its cause is examined and
   reported; no ruling and no scenario is changed for it. The run without assignment knowledge is a diagnostic: its
   changes are listed and never stop (AM62). 2c, its own commit: B2 recorded, a new README section in
   each maintained set (md5s, the lines that moved and why); in round 1's, the IRB's and the MPB's README a section
   that states what changed and names the last commit that holds the old results (section 11, X11); their reports'
   moved numbers and the moved findings in the design records (KT8, KT10; the IRB's and the MPB's T-D records) marked
   with a dated line, not rewritten; a stale note in dock_loading's IRB and MPB READMEs (until dock_loading's step).
   The commits of stage 2 are made only after its checks pass; a stop leaves the committed state on the old gate
   (AM60).
3. The run option `context_knowledge` and the removal of ω (TODO-66), off only (one commit): the flag, the run files
   and sweeps state `context_knowledge: false`, tests state both (AM51); the old `ContextKnowledge` and the
   recognizer's constants removed; `_output` multiplies by unit weights (P1). Check against B2: the four sets and round
   1 identical except the `[run]` field; the dock_loading milestones identical up to step 499, the first differing step
   at 500 or later (one line each); pytest passes.
4. The world's side (two commits). 4a: `Timeline`, `Window`, the setup's and the scenario's forms, the resolution at
   load, the builder, the `[run_mesa] timeline` line, `"timeline_facts"`, the load checks (AM20, AM46, AM50, AM52),
   with tests: the resolution's four cases (scenario stated, stated empty, not stated with a setup timeline, setup with
   none); each refusal (a timeline fact in a precondition, a guard, a completion condition, an effect, the `"states"`
   block; overlapping windows). 4b: break_time, room_warm, ac_on; switch_on (AM43) in both domains; dock_loading's ac_activation (AM45)
   and its object type. Check against stage 3: the named lines only; every registered scenario of both domains loads;
   pytest passes.
5. The mind (one or two commits): `ContextKnowledge` and the domains' declarations, `ObservedCompletions`, the prior in
   the recognizer, `BeliefState.prior` and `levels`, `[IR-context]`, the run options' defaults on. Tests: section 4's
   table tests; the memory on a recorded run (in a round 1 scenario with a coffee_break, the recency fact holds on
   exactly 90 ticks, from the tick waited(human, coffee_machine_0) first holds, AM47); a robot with context knowledge
   on loads in every registered scenario of both domains. Check against stage 4, context knowledge off: identical;
   with it on, the four sets and round 1 run to completion (not read).
6. The instruments (one commit, section 9). Check: round 1 and kitting's IRB and MPB sets with context knowledge off,
   every instrument output byte-identical to stage 2's (no named line of stages 3 to 5 reaches an instrument output
   except the A/C action's name in the IRB's record columns, if any: listed); round 1 with it on, 0 disagreements with
   the oracle (AM49), results not read.
7. Records and docs (one commit): the BUILT block under "T-K" with commits and acceptance, the docs of section 6, the
   maintained sets' and round 1's README sections stating the final md5s and every named line since B2.

## 9. The instruments and their cost

What changes, and roughly how much:
- `irb/trajectory.py`: the row's facts include the timeline facts (from the model's timeline at the tick) beside the
  state facts. About 10 lines.
- `irb/oracle.py`: its own prior from the method document, independent of `shared/recognizer.py` (it reads the
  domain's declared values from the registry, as it reads the task model, and computes the levels, the groups and the
  division itself); its own memory of observed completions from the rows (the terminal fact newly holding for the
  observed human, AM47); `output()` multiplies by the prior before the floor and the pin, as the recognizer does; new
  columns `prior` per key and `levels`. About 80 to 120 lines, with new rules in the IRB README (28 onward, each with
  its source).
- `irb/compare.py`: the new columns compared. About 10 lines.
- `irb/summary.py`, `irb/admission.py`, `irb/baseline.py`: each case labelled by the state the script meets (KT14):
  the level of the true foreseeable task at its start, and of the assigned tasks' rivals; the A/C's belief at arrival
  (KT10). About 40 to 60 lines.
- `common/tdlib.py`: the `[IR-assignment]`, `[IR-context]` and `[run_mesa] timeline` lines. About 20 lines.
- The MPB instrument: its oracle imports the IRB's unchanged, so the gate's expected outcome follows the new belief;
  only the rename in `mpb/actual.py`, `mpb/reference.py`, `mpb/run.sh`. Part 4's measures are unchanged.
- The gate's part (AM42) comes first, in stage 2b: the oracle's `confidence` from the belief over H (its `output()`
  keeps the floor and the pins for the reported distribution), the gate column from it, the log readers' θ crossings
  from `confidence`. About 15 lines.
Cost: one build session for the code and the README rules. The verification reruns: in stage 2, round 1's 31 runs,
the IRB's 17 and the MPB set (its variants as its README states); in stage 6, the same with context knowledge off, and
round 1 once more with it on. Each goes through the run, the trajectory, the oracle and the comparison, as the sort's
preparation did; the wall time of one pass is measured at stage 0 and stated in the stage report. dock_loading's 54 IRB
and 52 MPB runs are not rerun in the build (AM55); they are stale from stage 2 until dock_loading's step (AM57).

## 10. Cases the design does not cover

Each is ruled in section 7, or recorded here for Hadi:
- AM43 to AM45 and AM47 settle the cases the first version listed.
- A timeline fact whose window opens while the robot's decision rests on a projection: the prior changes, possibly the
  leader, and `recognition_changed` may fire (5 d). Ruled behaviour (AM21), stated so the runs are not surprised.
- A foreseeable task with no live hypothesis contributes nothing to Z (method section 6); a task whose only hypothesis
  is retired (just completed) therefore takes no share on that tick, and the recency fact first matters when it
  re-enters on the next. As ruled.
- TODO-154 (the share at an episode's start) stays as recorded: the build answers nothing beyond R4.
- dock_loading's coffee_break from the office (the method document's open flag on section 12): unchanged by the build;
  observed in step 6.

## 11. Cross-check of the rulings (ccode, 4 October 2026)

The ten rulings and the two additions, checked against each other, against the earlier rulings of the T-K entry and
against the code. None of them conflicts with another. The points below are consequences nobody stated, or places
where a ruling looks incomplete from the code's side. Hadi rules on each; the plan does not resolve them.

- X1. RULED (AM57): round 1 and kitting's IRB and MPB sets are rerun in stage 2 with the new gate, their outputs
  replaced; dock_loading's sets stay stale until its step. The point as raised: AM42 with AM48: round 1 and the
  test-bed sets go stale. Round 1 (KT8) is the "off" side of KT14's comparison,
  and its expectations, outputs and report were made with the old gate. After AM42 they no longer describe HEAD. The
  same holds for kitting's other IRB (s08, s09) and MPB sets and for dock_loading's stage-1 IRB and MPB outputs, which
  AM48 does not rerun. The plan reruns round 1 in stage 2 and records it as a new section of its README, with a
  superseding note in its REPORT.md that points to it. Round 1 is a frozen folder under CLAUDE.md, so this needs
  Hadi's ruling; the alternative is a new folder for the regenerated off side. The other kitting test-bed sets stay
  stale until a task reruns them.
- X2. RULED (AM58): the viewer's confidence is TODO-180. The point as raised: AM42 and the log. `[IR] confidence` (the value the gate read) and the leader's value in `[IR-dist]` (the reported
  distribution) will differ wherever pins or the floor act. A reader that takes a θ crossing from `[IR-dist]` reads the
  wrong value. The instruments are changed in stage 2b. Any other reader of the logs (a report, the viewer) is also
  affected; the viewer is not checked in this build.
- X3. RULED (AM56): corrected if small; it is not small (no object types in the world state; the fix changes the
  boundary's as-built reading), so it is deferred, TODO-179. The point as raised: AM43 and the episode boundary (T-D
  L1 as built). At an A/C completion, waited(human, switch) newly holds. Both
  `wait_at` (still a terminal action, through coffee_break) and `switch_on` have an enabled grounding at the switch.
  `_observed_terminal_completion` returns the first in declaration order, so the `[IR-boundary]` line names
  `wait_at(ac_switch_…)` for a switch_on completion. The boundary itself is correct (one boundary at the right tick);
  only the label is misleading. Not fixed by the plan, since it changes no decision; flagged.
- X4. RULED (AM54): the completion condition is refused too. The point as raised: AM52 looks incomplete. A schema names a fact in four places: a precondition, a method's guard, an effect or
  retraction (AM20), and the completion condition. AM52 names the first two. A completion condition that named a
  timeline fact would let the timeline end the human's action: the body's executor and the recognizer's phase model
  both read completion conditions. Proposal: the loader also refuses a timeline fact in a completion condition.
  Alternative: leave it to authoring.
- X5. AM50 and AM52 with P3. To refuse a timeline fact in the `"states"` block and in schemas, the loader must know
  which declared facts are timeline facts. The A5 form (a state about no object) does not say this, since A5 admits a
  state about no object that an action sets. The plan therefore lists timeline facts in a registry list of their own,
  `"timeline_facts"`, with the same class. This refines P3 and is not a design change; flagged because P3 said
  `"states"`.
- X6. RULED (AM55): the reading confirmed; the six milestone runs. The point as raised: AM48's consequence and the
  plan's scope. The consequence says "dock_loading's recognition and planning runs are
  not rerun in the build". The scope Hadi accepted runs dock_loading's six milestone runs, which are recognition and
  planning runs, though not test-bed sets. The plan reads the consequence as dock_loading's IRB and MPB sets and keeps
  the milestone runs, as the only check of dock_loading's new task, action and declarations. Also: the first version
  named three milestone runs in D7 and six in stage 0; the amended plan runs the six (scenario_s03_02, s05_02, s07_02,
  s03_03, s05_03, s07_03). To confirm.
- X7. AM45 and the human's script. With no office method, the load-time replay refuses a dock_loading script that
  starts ac_activation while the human is in the office, because the task is not applicable there. Consistent with
  AM45's consequence; stated so that an author is not surprised. Unexercised in V1, since no dock_loading room has a
  switch.
- X8. AM46 and the recency durations. Windows are written in ticks (AM11, AM46). Recency durations are declared in
  physical time and converted by the body (NOTES FOR THE BUILD'S PLAN). A change of the tick length would move every
  window in physical time but no recency duration. Harmless in V1, where the tick length is 2 seconds in both domains.
- X9. AM47 and L4. On the completion tick the foreseeable task's hypothesis is retired and takes no share. On the next
  tick it re-enters with 1/|H| of the evidence, under the suppressed prior. If the human stays standing at the machine,
  waited holds and the hypothesis stays retired until the human moves. Consistent with the rulings; stated for the
  expectations.
- X10. AM44 and AM18. AM18's "not taken: ac_on as a condition of the task" is a decision, not a load check. Nothing
  refuses ac_on in a guard, as AM52 refuses a timeline fact. No schema does this today. Flagged only.

Consequences of the rulings on section 11 (ccode, 4 October 2026). RULED (Hadi, 4 October 2026): X11 as AM59 (one
external copy), X12 as AM60, X13 as AM61 (two stop conditions: a disagreement with the oracle, a scenario that no
longer reaches its coverage case; a stop means its cause is examined), X14 as AM62; X3 accepted as AM63. As raised:

- X11. "The last commit that holds the old results" (AM57) holds only what git tracks. Under the rule for analysis/
  (2 October 2026) the per-tick data (csv, json) and the figures are untracked. For kitting's IRB and MPB sets they
  are restorable from 7d00f43 (`analysis/README.md`). For round 1 the summaries, diffs and reports are in 4c71b44, but
  its per-tick data and figures are in no commit; replacing them on disk loses them. Proposal: before stage 2 replaces
  them, copy the three sets' untracked files outside the repository (as the copy of 2 October 2026,
  /home/hadi/teamrob_analysis_2026-10-02/) and name the copy in each README. This is not a second folder in the
  repository. Hadi decides.
- X12. The stop rule and the commits. Stage 2's reruns come after its code change. Its commits are made only after the
  checks pass, so a stop leaves the gate's change uncommitted in the working tree, HEAD at stage 1, and the finding
  reported.
- X13. What counts as declared in the MPB. Part 4's properties are declared. Parts 1 to 3 are full per-tick
  expectations from the oracle, which follows the new gate in stage 2b; a disagreement there is a fault of the code or
  of the instrument, and stops the build as well. The coverage matrix (`analysis/kitting/mpb/coverage.md`) claims
  cells, each verified by one authored instance. Under the new gate an instance can stop reaching its cell (for
  example, an admission one tick later that no longer meets the authored conflict). The plan treats a claimed cell
  that its instance no longer reaches as a declared property that no longer holds: stop and report. To confirm.
- X14. The prior-off appendix of the MPB (MPB-6) is rerun as its pipeline runs it. It is a diagnostic: a change there is
  listed, never a stop (CLAUDE.md, Methodology, the prior; `docs/assumptions.md` 1.4).
