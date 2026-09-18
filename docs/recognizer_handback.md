# The intention recognizer — current description

What `shared/recognizer.py` and `shared/likelihood_functions.py` do at HEAD (September 2026), for two readers:
later sessions of this project, and colleagues who last saw the recognizer before July 2026 (start with §9,
the revision since then, then §1). Every formula and constant below is read from those two files; where an
earlier text or a docstring says otherwise, the code wins and the difference is stated. The design history is
in `docs/design_decisions.md` (entries I2–I5, "θ has one home", F47b, D2); open items in
`docs/TODOS_AND_DEFERRED.md`; the interface in `shared/io_contracts.md` §1.2 and §2.1.

Section numbers §1–§5 and §8 are cited from code and other docs; keep them stable.

## 1. The model

### 1.1 Hypotheses and support

The hypothesis space is built once, at robot construction, from the domain schemas and the workspace objects
(`build_hypothesis_space`), never from the human's script:

    H = { (τ, b) : τ a task schema, b ∈ Π_{v ∈ params(τ)} Objects(type(v)) } ∪ { unknown }

one hypothesis per task and typed binding (`TaskSchema.parameter_types`), plus `unknown`, the hypothesis that
the behaviour is none of them. Keys are `repr(HypothesisKey)` strings and are sorted at construction, so every
order-dependent step (ties, log order) depends on the space alone.

The SUPPORT S is H when nothing is known of the observed agent's work order (prior-off, the default). With
`--assignment_prior true` (prior-on) it is restricted: S = assigned tasks ∪ foreseeable tasks
(`TaskSchema.is_foreseeable`) ∪ {unknown}; every other hypothesis is pinned at the floor and never scored.
The knowledge restricts the support; it is not a weight.

The LIVE set at tick t is S minus the tasks completed by t (§1.6). One recognizer instance observes one agent:
the odometer is kept per agent, the phase state per hypothesis only.

### 1.2 Prior

Uniform over the live set, `unknown` included: π(k) = 1 / |Live|, at construction and again at every
episode boundary (§1.6), recomputed over what is still live. Nothing else is stored to restart from.
The robot observes the human once before the clock starts (`RobotAgent.observe_initial`), so step 0 is
already a scored step.

### 1.3 Phase: the expected action

Every tick, for every live hypothesis k = (τ, b), the planner decomposes τ against the current world for the
observed agent (`AdaptivePlanner.decompose`): the guards select the method (in kitting, what the agent holds
chooses between `deliver_default`, `deliver_already_held` and `deliver_with_return`), and the steps are
grounded. The EXPECTED action a_φ(k) is the first grounded action whose completion predicate does not hold in
the world. The phase is derived, never stored; what is stored per hypothesis is the action it expected on the
previous tick and its ORIGIN, the agent's position and odometer reading when it began expecting it. A change
of expected action (an advance, or a regress when `at()` flickers off at the proximity threshold) is a phase
change. Two actions are the same when their name and grounded bindings are.

A task's likelihood is the likelihood of the action it expects now: P(o_t | τ) = P(o_t | a_φ(τ)).

### 1.4 Likelihoods

MOVEMENT (actions with `progress_evaluator = "excess_path"`, in kitting `move_to`). Measured from the origin o,
with w the distance walked since o (per-agent odometer: the sum of straight-line steps between observed
positions), p the current position and g the target's current position (`shared/target_resolution.py`; a
carried object resolves through its holder):

    e = w + C(p, g) − C(o, g)                      (the path wasted under the hypothesis)
    L = 2 / (1 + exp(β · e))                         L(0) = 1,  L(1/β) = 2/(1+e) ≈ 0.54,  L → 0 as e grows

C is the path cost, straight-line by default and injectable (`IntentionRecognizer(path_cost=…)`). With a
static target and a metric C, e ≥ 0 and L ∈ (0, 1]; a moving target can make e negative, L ∈ (0, 2). One
stretch toward one target is ONE observation however many ticks it spans: its value is recomputed from the
origin every tick and replaces the previous tick's. A stationary tick mid-stretch leaves e where it was.

COMPLETION SIGNAL (an event). If the observed microaction is in the declared vocabulary of the action the
hypothesis expected on the PREVIOUS tick (`pick_up` → GRASP, `place` → RELEASE), the event factor is

    c = DETECTION_HIT_RATE         if that action's grounded completion predicate holds now
        DETECTION_FALSE_ALARM_RATE otherwise

It multiplies into the evidence once. It is judged on the previous tick's action because the world after a
grasp already satisfies `pick_up`'s completion, so the derived action has moved on. A terminal action's
signal never reaches this channel: the completion pin (§1.6) retires the hypothesis first.

NO GRADED SIGNAL. An action with no evaluator (`pick_up`, `place`, `wait_at`), a target with no resolvable
position, or a hypothesis the planner cannot decompose in this world (`DecompositionError`, logged once)
scores the perfect-fit value L = 1: nothing to charge. An undecomposable hypothesis is therefore not refuted;
it is treated as fitting.

EMPTY STRETCH. A graded action whose stretch is empty (w ≤ 0: the tick a hypothesis enters the action, the
ticks after a boundary before the agent moves) is not an observation. It contributes no factor. That is not
the value 1: 1 is a perfectly efficient walk, and here there is no walk. On such a tick the hypothesis pays
nothing while a rival with an open stretch pays its L/u (accepted, I4d point 4).

### 1.5 Evidence: odds against `unknown`

`unknown` is the reference. Its likelihood is the constant u = `UNKNOWN_LIKELIHOOD` for every observation,
and it takes no factor of its own. Each hypothesis's evidence is its odds against `unknown` over its OWN
observations in the current episode. For every live k and tick t, the invariant is (update()'s docstring,
checked to 7e-15 by an independent accumulator in `analysis/i4d_fold_unknown/`):

    O_t(k) = E_t(k) / E_t(unknown)
           = [π(k)/π(unknown)] · Π_{stretches s of k closed by t} L_k(s)/u · Π_{events e of k} c_k(e)
             · ( v_k(t)/u   if k's open stretch is an observation,  else 1 )

- The open stretch's current value v multiplies on top as v/u for this tick only.
- A phase change FOLDS the closing stretch's final value into the base as L/u once, or nothing if that
  stretch was empty, and moves the origin to the agent's position and odometer reading. A fold moves a
  factor from the open term to the base without changing it. A regress folds too, and so does a
  no-graded-signal phase (as 1/u).
- Events enter as c, not c/u.
- π(k)/π(unknown) = 1, since the prior is uniform.

The belief over the live set is E_t(k) = O_t(k) / (1 + Σ_j O_t(j)), with E_t(unknown) = 1 / (1 + Σ_j O_t(j)).
One normalisation, over every live hypothesis and `unknown` together. The stored bases are rescaled by the
same total each tick, so they stay in one scale.

### 1.6 Completion pin and episode boundary

PIN. A hypothesis whose TERMINAL action's completion predicate holds (`obj_at(item, table)`,
`waited(agent, machine)`) is complete, whoever did it. It is retired, never scored again, and pinned at the
floor on output for the rest of the run (`[IR-complete]`). The live set shrinks and nothing re-initialises.

BOUNDARY. If a hypothesis retired this tick expected its terminal action on the previous tick, the observed
agent's own derived phase had reached the completing action, so the observed agent finished a task. The
episode ends (`[IR-boundary]`): every live base becomes the uniform prior over the live set, every origin
moves to the agent's position and odometer reading, and this tick already reports the prior. Nothing crosses
the boundary. A task hypothesis means "the task being executed now"; there is no representation of
dispositions or future tasks, and none may be smuggled in. The pin and the boundary deliberately have
different criteria. A robot completion pins (prior-off) but is not the human's boundary. The attribution
assumes that an agent whose phase reached the terminal action is the one that completed it; the world carries
no authorship.

### 1.7 Output

    P̃(k) = E(k) · ω(k)                  ω: context weight, output only, never fed back; ω(unknown) = 1
    P(k)  = normalise( max( normalise(P̃)(k), BELIEF_FLOOR ) )
    pinned keys (inadmissible ∪ completed) = BELIEF_FLOOR;  live keys scaled by 1 − BELIEF_FLOOR · |pinned|

`most_likely` is the argmax, and `confidence` is its value. Ties go to the first live key in sorted order,
and `unknown` sorts after every live task key, so it loses every tie. The recognizer owns its evidence:
`prev_belief` is accepted by `update()` and not consulted, because the reported distribution carries
output-only factors.

### 1.8 `update()` in pseudocode

Close enough to `IntentionRecognizer.update()` to check line by line; λ is `_progress_likelihood`, and ≡ is
identity of name and bindings.

```text
update(obs, world):
    pos, mu ← obs.position, upper(obs.microaction)
    odo[agent] ← odo[agent] + |pos − last_pos[agent]|        (0 on the agent's first observation)
    boundary ← false;  U ← {}
    for k in sorted hypotheses:
        if k inadmissible or k completed: continue
        A ← planner.decompose(k.task, k.bindings, agent, world)          (None on DecompositionError)
        if A ≠ None and A[-1].completion ∈ world.predicates:            # terminal pin
            if expected[k] ≡ A[-1]: boundary ← true                      # the observed agent's own completion
            completed ∪= {k};  drop base[k], expected[k], origin[k], origin_odo[k]
            continue
        a ← first action of A whose completion ∉ world.predicates         (None if A = None)
        if k never observed:                                             # enters its action: empty stretch
            expected[k], origin[k], origin_odo[k] ← a, pos, odo
            U[k] ← base[k];  continue
        a_prev ← expected[k]
        if a_prev ≠ None and mu ∈ vocabulary(a_prev):                     # event
            base[k] ← base[k] · (HIT if a_prev.completion ∈ world.predicates else FALSE_ALARM)
        if not a_prev ≡ a:                                               # phase advance or regress
            L ← λ(a_prev, origin[k], odo − origin_odo[k], pos)
            if L ≠ none: base[k] ← base[k] · L / u                        # fold
            expected[k], origin[k], origin_odo[k] ← a, pos, odo
            v ← λ(a, pos, 0, pos)                                         # none if graded; 1 if not
        else:
            v ← λ(a, origin[k], odo − origin_odo[k], pos)
        U[k] ← base[k] · (v / u if v ≠ none else 1)
    U[unknown] ← base[unknown]                                           # the reference: no factor
    Z ← Σ U;  base ← base / Z;  E ← U / Z
    if boundary:                                                         # episode ends
        base ← uniform over (live keys ∪ {unknown});  E ← base
        origin[k], origin_odo[k] ← pos, odo  for every live k
    P ← output(E)                                                        # §1.7
    return BeliefState(distribution=P, most_likely=argmax P, confidence=max P)

λ(a, o, w, p):
    if a = None or a has no progress_evaluator or a's target has no position: return 1   # perfect fit
    if w ≤ 0: return none                                                               # empty stretch
    e ← w + C(p, g) − C(o, g);  return 2 / (1 + exp(β · e))
```

Likelihoods are memoised per tick by their inputs: (evaluator, origin, walked, target) and the grounded
completion predicate. Two items on one shelf therefore receive identical values from the same origin.

### 1.9 Closed forms

- A lone live task with n fitting observations: O = u^{−n}, so confidence = 1/(1 + uⁿ) times the pinned-mass
  factor (1 − 0.001 · |pinned|). That is 0.909 / 0.990 / 0.999 unpinned; measured 0.905 / 0.986 / 0.995 with
  four keys pinned (s00_on 81 / 109 / 113, `analysis/d2_recognition_trigger/sweep/`).
- With rivals: confidence(k) = 1 / (1 + 1/O(k) + Σ_{j≠k} O(j)/O(k)) before floor and pins. θ = 0.75 is
  reachable on a first fitting stretch (O(k) = 1/u) only if Σ_j O(j)/O(k) < 1/θ − 1 − u = 0.233; after one
  fold, only if that sum is below 10 × that (TODO-64).
- L = u at e = ln(2/u − 1)/β ≈ 294 cm: a stretch that wasted about 294 cm is no better than unexplained.
  L(30 cm) = 0.85, the slop at the proximity threshold (TODO-58).
- A step change of k's expected action, as at an arrival, is a fold of the closing stretch plus, for a
  no-graded-signal next action, an open 1/u. An arrival at a shelf is therefore worth two observations at
  once (×10 on the confidence odds). This is TODO-61 (b)'s mechanism.

## 2. Parameters

Four constants in `shared/likelihood_functions.py`, each with a physical meaning; `recognizer.py` reads them
through the module and never redefines them.

| constant | value | meaning |
|---|---|---|
| `BETA` (β) | 0.01 /cm | Detour tolerance. L at an excess of 1/β = 100 cm is 2/(1+e) ≈ 0.54 (the earlier text of this section said ≈ 0.27, which is the raw logistic's value; the logistic is normalised to 1 at zero excess, and the code comment on `BETA` is right). In centimetres, hence layout-scale dependent (TODO-58). |
| `UNKNOWN_LIKELIHOOD` (u) | 0.1 | The likelihood of any observation under `unknown`: the bar a hypothesis must clear per observation, and the unit of the ceiling 1/(1 + uⁿ) over n observations. |
| `DETECTION_HIT_RATE` | 1.0 | P(signal \| the action completed). Mesa reports every completion. |
| `DETECTION_FALSE_ALARM_RATE` | 10⁻³ | P(signal \| not completed). Mesa has none; non-zero only so a refuted hypothesis keeps a recoverable base. Set both rates from a real detector's measured rates. |

β and u were chosen jointly (I4: the region where every first task is revealed before its grasp with no wrong
task at θ is β ∈ [0.005, 0.1] × u ∈ [0.01, 0.2]; the chosen point is its centre; `analysis/i4_evidence_model/`,
closed, not to be reopened by sweeping).

LOAD-BEARING, NOT PARAMETERS:
- θ is NOT a recognizer parameter. The recognizer emits a distribution and gates nothing. The gate is the
  meta-planner's: `DEFAULT_THETA = 0.75` in `shared/meta_planner.py`, applied only in
  `MetaPlanner._clears_gate`. A `CONFIDENCE_THRESHOLD` sat in `recognizer.py` until September 2026 with no
  reader; it is gone (§8).
- `BELIEF_FLOOR` = 10⁻³ (`recognizer.py`): applied to the output only. The evidence is normalised but never
  floored.
- `PROXIMITY_THRESHOLD` = 30 cm (`mesa_sim/world_state_builder.py`): decides when `at(agent, x)` holds, hence
  every phase advance, every fold and every origin.
- The path cost: straight-line, exact only because Mesa agents walk straight through obstacles.
- The domain's decompositions: how many actions a selected method has sets how many observations a hypothesis
  can accumulate (TODO-61 (b)). `deliver_with_return` has six actions to `deliver_default`'s four.
- The context weights (`_context_weight`, output only): TEMPERATURE_BOOST 3.0 on `ac_activation` at room
  temperature ≥ 26.0, FATIGUE_BOOST 2.5 on `coffee_break` after a shift of ≥ 500 steps, on literal task names
  (TODO-66). Inert in every run: Mesa builds `ContextKnowledge.default()` (21.0 °C, shift from step 0) and no
  run reaches 500 steps.

## 3. The guarantee statement (β = 0.01 /cm, u = 0.1, θ = 0.75)

"Guarantee" means: holds in every measured condition and follows from the model, not from a scenario. The
conditions are the five regression fixtures × assignment prior off/on, PYTHONHASHSEED=0. The figures are from
`analysis/d2_recognition_trigger/sweep/` (logs local). Their `[IR*]` lines equal F1's
`analysis/f1_robot_responsible/realized_none/` and F47b's `analysis/f47_fixtures/baselines_s40/` except for
two trailing ticks in s00_off and s20_off. The recognizer is unchanged since I5 (θ's removal changed no
behaviour). The figures differ from the I5 matrix because the fixtures and the robot changed: s40 was retyped
(F47b), s10 is back in the sweep, and prior-off pins follow the robot's deliveries. Ticks are `[IR] step=`
values. A reveal is the first tick the true task is `most_likely` with confidence ≥ θ.

| fixture | task (human, in order) | reveal prior-on | reveal prior-off | grasp / completion |
|---|---|---|---|---|
| s00 | item_3 | 11 | 39 | grasp 41 |
|  | item_2 | 81 | 109 | grasp 111 |
| s10 | item_2 | 25 | 29 | grasp 31 |
|  | coffee_break | 123 | 123 | arrival 123, done 154 |
|  | item_5 | 163 | 247 | grasp 249 |
|  | ac_activation(ac_switch_0) | 314 | 334 | done 365 |
| s20 | item_3 | 6 | 20 | grasp 22 |
|  | item_2 | 57 | 87 | grasp 89 |
| s30 | item_3 | 21 | 28 | grasp 39 |
|  | item_7 | 77 | 86 | grasp 98 |
| s40 | item_3 | 21 | 21 | grasp 60 |
|  | coffee_break | 153 | 153 | arrival 153, done 184 |
|  | ac_activation(ac_switch_1) | 205 | 205 | arrival 205, done 207 |
|  | ac_activation(ac_switch_2) | 218 | 221 | done 228 |
|  | item_6 | 250 | 266 | grasp 272 |

### 3.1 Prior-on (the observed agent's assignment is known)

The recognizer GUARANTEES:
- **The belief is over the assigned tasks, the foreseeable tasks and `unknown` only.** Everything else is
  pinned at 10⁻³ and never scored.
- **Every task the human executes is revealed above θ before its grasp, or before its completion for a task
  with no grasp.** See the table. Of the foreseeable tasks, coffee (123 / 153) and ac_switch_1 (205) are
  revealed at their arrival fold, ac_switch_2 mid-walk (218), and s10's AC task on the first step.
- **HOW several reveals happen matters: the next-task reveals in s00, s20 and s30 (81, 57, 77) and s10's AC
  task (314) come on the human's FIRST STEP after the boundary.** The human's last assigned task is then the
  only live task, the belief is the prior over {task, unknown} (0.498), and one fitting step takes it to 0.905
  (1/(1 + u) with pins). The gate is cleared by the size of the live set plus one short stretch, not by
  trajectory evidence (§4, the graded-evidence question; TODO-64's note on one-task pools).
- **No wrong task reaches θ** in any prior-on condition.
- **One crossing of θ per recognition.** No task crosses twice within its episode.
- **After the human's own task completion, the belief is the uniform prior over the live set** until the
  human moves: 0.498 each over {task, unknown} in s00/s20/s30, 0.331 over three live keys in s40 at 228.
  `most_likely` on those ticks is the key-order tie-break, and its confidence is 1/|Live| (with pins).
- **Confidence on a fitting task steps with its observations**: 1/(1 + uⁿ) with pins, 0.905 → 0.986 → 0.995
  in s00_on (first step, arrival fold, first carry step). It can legitimately FALL when the next expected
  action stops fitting. Non-monotone by design; do not smooth.
- **A completed task is at the floor for the rest of the run**, whoever completed it.
- **Once every admissible task is complete, `unknown` holds all live mass** (0.995 in s00/s20/s30 from the
  last boundary, 0.990 in s10). In s40 the never-performed foreseeable `ac_activation(ac_switch_0)` stays
  live and ties with `unknown` at 0.496; it is `most_likely` by the tie-break.

### 3.2 Prior-off (no assignment known)

The same model over a larger live set: every task of every object, the robot's own undelivered items
included. Therefore:
- **Every reveal still precedes the grasp** (or the completion), and **no wrong task reaches θ**, in all five
  fixtures. Several prior-off reveals are the arrival fold, two ticks before the grasp: s00 39 and 109, s10 29
  and 247, s20 20 and 87. The walk alone did not separate the true task from its rivals; the arrival's two
  observations did (§1.9).
- **Repeated crossings within one recognition**: s00 109 / 113 / 115, s10 29 / 33 / 35, s20 20 / 24 / 30 and
  87 / 91 / 95. At the grasp every rival's method flips to `deliver_with_return`. Its `place`-back-on-the-shelf
  phase is a no-graded-signal observation worth 1/u, and on departure the rival regresses to a fresh
  zero-excess stretch. The rival lifts twice, and the true task dips under θ twice. This is the model working
  as specified (TODO-61, TODO-55 (e)). Since D2 the consumer tracks identity and these crossings no longer
  re-decide (§5).
- **An idle human sits at the prior over what is still live**, meaning the robot's undelivered items and any
  foreseeable task never performed. After the human's last task: s00 item_4 at 0.498; s10 item_0 at 0.248,
  then 0.331 from 418; s20 item_6 at 0.332, then item_7 at 0.498 from 145; s30 item_2 at 0.332, then item_6
  at 0.498 from 160; s40 `ac_activation(ac_switch_0)` at 0.331, then 0.496 from 376. A robot delivery shrinks
  the set (the pin) without re-initialising (no boundary). Never at θ. When the robot delivers the last live
  item, `unknown` takes 0.995 (s00 166, s20 235).
- **Dilution**: more live rivals mean less confidence from the same evidence and later reveals. Examples:
  item_6 at 249 in s40, 0.746 prior-on against 0.461 prior-off; ac_switch_1 at its arrival, 0.878 against
  0.784; item_5 in s10, revealed at 163 prior-on and 247 prior-off.

### 3.3 What every figure above is conditional on

- **Straight lines.** Mesa agents walk straight through obstacles and C is Euclidean, so the true
  hypothesis's excess is exactly 0. In a real cell with obstacles, every detour the path cost does not model
  is charged to the true hypothesis. Inject a path cost before reading any figure here as a guarantee there.
- **`PROXIMITY_THRESHOLD` = 30 cm.** Every arrival fold is taken 30 cm from the target; a different threshold
  moves every reveal tick and every ceiling step.
- **Kitting's decompositions and guards.** The prior-off repeated crossings are `deliver_with_return`'s
  phases. The arrival's double observation is `move_to` followed by a no-graded-signal action.
- **The layout's decoy geometry.** Targets on one bearing tie for the whole walk and are separated by the
  arrival fold (s40 187–204: ac_switch_1 and item_6 equal throughout, 0.248 → 0.417; at 205, 0.878 against
  0.088; s20_off's collinear shelves likewise, revealed at the arrival, 20). A decoy on the true bearing BEFORE the target, within 30 cm of the
  path, would fold first and could cross θ wrongly. No fixture has one.
- **The live set's size**: it sets the prior, the dilution, what θ means, and whether one step clears it
  (TODO-64, TODO-65).
- **β, u**: they set every reveal tick (I4 / I4b / I4c region analysis, closed).
- **The scripted human.** A human who hesitates, back-tracks or wanders mid-task is charged as a rival would
  be. Standing still is not evidence (TODO-59's deferred channel, not built). Only behaviour the robot's
  domain describes is scripted (F47b); an undeclared behaviour is TODO-80.

### 3.4 What the meta-planner may assume, and must not

MAY assume, either setting: a task at or above θ is the task being executed now. There is no wrong task at θ
in the measured conditions, but see §3.3 on a decoy before the target. A completed task never returns. After
the human's own completion the belief is the prior, and `most_likely` carries no information until the human
moves. Prior-on: one crossing per recognition. Prior-off: up to three crossings within the grasp stop, all on
the same task.

MUST NOT assume, either setting:
- that confidence is comparable across live-set sizes (0.75 is a different bar over 2 and over 8 keys);
- that confidence ≥ θ implies trajectory evidence (a lone live task clears θ on one step);
- that `unknown` ≥ θ means the human is idle: it also means a task the space does not contain, a detour under
  way, or every task pinned;
- that a robot completion is a human boundary;
- that the ceiling is a constant (it is 1/(1 + uⁿ));
- that confidence is monotone within a task;
- that anything in the belief refers to a previous episode.

## 4. Characterised limitations, and the open design item

Properties of the chosen model, not defects (TODO-61). Both have one root, costdif1 with a constant
`unknown`: a fitting stretch scores L = 1 whatever its length, and every scored observation is worth L/u
against a constant reference. Any remedy for one changes the other's currency.

**(a) Confirmation is length-blind.** The excess discriminates by penalising wrong hypotheses, not by
rewarding right ones. The correct hypothesis sits at zero excess however far it walks: L(0) = 1 after one
step as after 300 cm. Evidence is strong at refutation and weak at confirmation. Seen at HEAD: two targets on
one bearing tie for the whole walk (s40 187–204, above). The walk rises only as off-bearing rivals are
refuted, and it separates nothing that lies on the line.

**(b) Accumulation is observation-count and decomposition sensitive.** Every fitting observation is worth 1/u
whatever it observed: a 300 cm walk straight at the target, a stationary `pick_up` phase, a one-step stretch,
a regress-generated zero-excess stretch. How a selected method segments the trajectory therefore sets how much
evidence a hypothesis can gather. Seen at HEAD:
- an arrival counts twice (fold plus open no-graded-signal phase), which is what separates collinear targets
  and produces most prior-off reveals (§3.2);
- the prior-off repeated crossings come from the rivals' `deliver_with_return` phases.

**THE OPEN DESIGN ITEM: graded evidence.** One short stretch counts as a full observation against `unknown`.
A single step (about 20 cm in these fixtures) with zero excess is worth ×10, the same as a completed walk. Its sharpest consequence is
in the baseline: prior-on, every next task in s00, s20 and s30 and s10's AC task clears θ on the human's first
step after the boundary (0.498 → 0.905, §3.1). Whether evidence should be graded (a confirmation term by the
fraction of C(origin, g) covered for (a); u per unit of evidence, or decomposition-normalised odds, for (b)) is
undecided. Grading changes what `unknown` means, so it must be decided together with the rationality-measure
alternative (TODO-63) and with what θ is meant to bar (TODO-64 / 65). Neither (a) nor (b) is a reason to
touch β, u or the likelihood form without a decision naming which it addresses.

Also stated, lower in consequence:
- An undecomposable hypothesis scores the perfect fit and is not refuted; no case is logged in the sweep.
- The boundary infers authorship from the phase. A domain where another agent satisfies a terminal condition
  while the observed agent stands in its terminal phase would attribute wrongly.
- Evidence accumulated under one method is reused when the guard re-selects another. Dormant in kitting (every
  within-episode flip is the observed agent's own grasp or release, TODO-55 (d)).

## 5. The interface to the meta-planner

`update()` returns a `BeliefState` (`shared/io_contracts.md` §1.2; contract §2.1): `timestamp`, `agent_id`,
`distribution` (every hypothesis key, pinned ones at 10⁻³, summing to 1), `most_likely` (the argmax key) and
`confidence` (its value). The meta-planner reads only `most_likely` and `confidence` (io_contracts §2.2):
- `_clears_gate(belief)`, the one place θ is applied, tests `confidence ≥ θ`.
- `evaluate_triggers()` fires `recognition_changed` (D2) when a decision record `_projected_hypothesis`
  exists and `most_likely` is no longer it. That covers a replacement, the human's boundary, or `unknown`
  after a pin. It also fires when no record exists and the belief clears the gate on a task, not `unknown`.
- `update_human_projection()` admits a projection only when the gate clears and `most_likely` is not
  `unknown`. It resolves the key through `recognizer.get_hypothesis()` (the same live instance, held by
  reference) to project the human's task, and records the hypothesis it projected.

Confidence is a gate, never a magnitude in any cost; `distribution` is logged and not read. The one-shot
question of the I5 hand-back (TODO-68, with TODO-48 and TODO-54) is closed by D2 on the consumer side. A
re-crossing of the recorded hypothesis fires nothing; a change of hypothesis or its end fires. No change was
made to the recognizer or to its event semantics (`design_decisions.md`, the D2 entry;
`analysis/d2_recognition_trigger/README.md`).

## 6. Open items

| item | where | one line |
|---|---|---|
| graded evidence: the model's two properties | TODO-61 (a), (b) | §4; the open design item |
| θ's meaning and reachability | TODO-64, TODO-65 | ceiling 1/(1 + uⁿ); a live-set-dependent bar; derived θ or a margin gate, nothing chosen (meta-planner side) |
| `deliver_with_return`'s guard | TODO-55 (e) | a stray item vs an assigned one; a domain question, the producer of the prior-off repeated crossings |
| β in centimetres | TODO-58 | layout-scale dependence |
| the stationarity channel | TODO-59 (deferred paragraph) | standing still as evidence against movement hypotheses; not built |
| declared behaviour outside the domain | TODO-80 | a human stay the robot's knowledge does not cover, declared as such; not built |
| the context / knowledge-representation pass | TODO-66 | `_context_weight` names two tasks and carries four constants; output only, inert |
| the two analytical tools | TODO-62, TODO-63 | radius of maximum probability (diagnostic); rationality measure (competes with `unknown`) |
| hash-seed dependence | TODO-42 | resolved for the recognizer (sorted keys); runs still need `PYTHONHASHSEED=0` |

Closed since the I5 hand-back: TODO-48 / 54 / 68 (D2); TODO-72 (io_contracts §1.3 / §2.1 aligned with this
document); TODO-52 (R1 / T10) and TODO-67 (T7), both meta-planner side; TODO-57's segment-3 question, made
moot by F47b.

## 7. The paper-facing divergence

The HCM paper writes P(task | O) with O a sequence of ACTIONS. The recognizer never observes an action: it
observes a microaction and a position, and the action is LATENT. P(o | τ) = P(o | a_φ(τ)) is a
marginalisation over that latent action, collapsed because the phase is derived deterministically from the
world (design_decisions.md, the I3 entry). The paper is a position paper, outdated relative to this design,
and not a specification. It will need rewriting on this point, and also on:
- the episode-local semantics (I4c);
- the constant `unknown` and the odds accounting (I4, I4d);
- the assignment knowledge as a support restriction, not a prior weight;
- the gate's placement: the recognizer gates nothing, and θ and what a trigger is an event of belong to the
  meta-planner (D2).

## 8. Removed, and must not return

| mechanism | why it went | where recorded |
|---|---|---|
| hypotheses from the human's `scheduled_tasks` | the robot never reads the human's script; hypotheses come from schemas and workspace objects | July 2026 (typed enumeration) |
| the previous posterior as the prior (`prev_belief` fed back) | the output carries state-only factors; feeding it back counted them twice | leg-level session; I3 |
| the 10× assignment multiplier | knowledge of the assignment restricts the SUPPORT, not the magnitude | assignment-pool entry |
| the held-item rule (refute a hypothesis that binds a portable object the agent is not holding) | a domain shortcut the phase model subsumes; wrong in domains with no holding relation | I3 |
| `ZONE_BOOST` | a soft multiplier standing in for a hard fact; fired for the wrong hypothesis in 28 of 52 measured episodes (I1 §5.4) | I3 |
| the global leg (one movement leg for all hypotheses, closed by the body's `stand`) | a stretch is per hypothesis, from its own origin; no leg closed by stillness, no decay | I2–I4 |
| HIGH / LOW / NEUTRAL likelihoods (4.0 / 0.1 / 1.0) | four numbers with no stated meaning; replaced by the excess-path logistic, detection reliability and a stated u | I4 |
| the cosine trajectory kernel (`"directional"`) | multiplied identical headings tick after tick (4ⁿ from one straight walk); replaced by one observation per stretch | leg session, I4 |
| `methods[0]` and string-parsed bindings | the planner selects the method by guards; bindings are typed | I2 |
| `CONFIDENCE_THRESHOLD` in the recognizer | θ has one home, the meta-planner's `_clears_gate`; the copy here had no reader | "θ has one home" |

Also gone and not to be re-added:
- any persistence of belief across an episode boundary (I4c; I4b's "reset the geometry, keep the belief" was
  measured and found wrong);
- any scoring of an empty stretch (I4c);
- `unknown` paying only on the open stretch (I4d);
- a raw, unnormalised logistic (I4: every advance halved a hypothesis that had done nothing wrong).

## 9. What changed since July 2026

What colleagues saw (June, commit de5f7ad) was a per-tick Bayes filter:
- hypotheses from the human's scheduled tasks;
- a STEP scored by the cosine between the step and the bearing to the target, mapped linearly to
  [0.1, 4.0] and multiplied every tick;
- a GRASP scored 4.0 / 0.1 on whether the agent holds the target item;
- RELEASE and STAND scored 1.0, and `unknown` always 1.0;
- `ZONE_BOOST` × 2 plus the temperature and fatigue boosts, multiplied into the posterior;
- the previous posterior as the prior;
- θ = 0.75 defined in the recognizer.

Every element of that has been replaced. In order:

| when | what it replaced | by | why |
|---|---|---|---|
| July (TODO-19; typed params) | literal microaction strings; hypotheses from the human's script | dispatch by schema-declared vocabulary and evaluator name; the typed cartesian space over workspace objects; the belief floor | no simulator strings in `shared/`; the robot must not know the script |
| Sept 10 (assignment pool) | a 10× prior weight on assigned tasks | the support restriction (§1.1) | knowledge of the work order is a fact about the support, not a magnitude |
| Sept 10 (leg session) | per-tick multiplication of identical headings (4ⁿ from one walk) | one observation per movement leg; output-only state factors | consecutive steps are duplicates, not independent evidence; the retracted "early reveals" were duplicate counting |
| I1 audit | — | measurement only | 0 of 5,579 likelihood calls evaluated a completion; ZONE_BOOST wrong in 28 of 52 episodes |
| I2 foundations | the recognizer's own target lookup, `methods[0]`, `"?item"` | targets, methods and completions from the planner and `target_resolution`; `waited` observable; sorted keys; first step scored | one answer to "where is the target"; no domain literals |
| I3 phase model | a single `holding` check choosing "phase 1 / 2"; the held-item rule; ZONE_BOOST | the derived expected action per hypothesis with its own origin; the terminal-completion pin | a task's likelihood is its current action's; completion is a world fact |
| I4 evidence model | cosine kernel, HIGH / LOW / NEUTRAL | excess-path likelihood (normalised logistic), detection reliability, constant u; β and u from a joint sweep | four constants with physical meanings; wasted distance was never charged before (TODO-53) |
| I4b / I4c boundary | origins moved only at an action change (coffee entered its own walk with 2144 cm of excess); then I4b's "reset geometry, keep belief" | the observed agent's own completion ends the EPISODE: belief to the prior over the live set, origins reset | a task hypothesis means the task being executed now; keeping folds across the boundary depended on accidental phase history |
| I4c empty-stretch rule | an empty stretch scored as a perfect walk (a lone survivor at 0.909 on nothing; 63 wrong-task ticks) | an empty stretch is no observation, no factor | zero excess meant two things; no walk is not an efficient walk |
| I4d | u charged only while a stretch was open (fold tick 0.905 → 0.498, a false re-trigger) | u folds with the stretch: evidence is odds against `unknown` (§1.5), invariant checked to 7e-15 | the evidence a stretch gave against `unknown` was lost at its fold |
| I5 hand-back | — | confirmation matrix at HEAD, guarantee statement, limitations (`analysis/i5_handback/`) | — |
| Sept 15 (θ single source) | `CONFIDENCE_THRESHOLD` in `recognizer.py`, unread | `DEFAULT_THETA` in the meta-planner, applied in `_clears_gate` only | the recognizer emits a belief and gates nothing |
| Sept 17, F47b (fixture, not model) | scenario_40's segment-3 legs scripted as `ac_activation` bound to two waypoints: ill-typed, so the space had no hypothesis for them | the targets retyped as `ac_switch_1` / `ac_switch_2` at the same coordinates; bindings type-checked at spawn (`check_task_bindings`) | a behaviour the domain does not describe can never be recognised. The I5 matrix's only wrong crossing (item_6, s40 203–213) was that walk: now the leg is its own task, tied with item_6 until its arrival fold (205). All s40 figures in §3 are from the corrected fixture. |
| Sept 17, D2 (consumer) | `theta_crossed` as the trigger | `recognition_changed` against the decision record (§5) | a trigger is a change in what the decision rested on; recognizer unchanged |

Superseded figures (the I5 matrix, and any s40 figure before F47b) are not carried here. Where they are cited
elsewhere they describe the fixture of their time.
