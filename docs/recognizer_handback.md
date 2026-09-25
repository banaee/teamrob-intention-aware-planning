# The intention recognizer — current description

What `shared/recognizer.py` and `shared/likelihood_functions.py` do at HEAD (September 2026), for two readers:
later sessions of this project, and colleagues who last saw the recognizer before July 2026 (start with §9,
the revision since then, then §1). Every formula and constant below is read from those two files; where an
earlier text or a docstring says otherwise, the code wins and the difference is stated. The design history is
in `docs/design_decisions.md` (entries I2–I5, "θ has one home", F47b, D2, graded evidence); open items in
`docs/TODOS_AND_DEFERRED.md`; the interface in `shared/io_contracts.md` §1.2 and §2.1.

Section numbers §1–§5 and §8 are cited from code and other docs; keep them stable. Terms are used as
`docs/glossary.md` defines them: the recognizer's unit of movement evidence is a STRETCH, a human's
movement is a WALK ("leg" is not used, and the removed leg model keeps its name in §8 only), a
CROSSING is a θ crossing, and scenario_40's "segment 3" is a SCRIPT PART, not a `Segment`.

## 1. The model

### 1.1 Hypotheses and support

The hypothesis space is built once, at robot construction, from the domain schemas and the workspace objects
(`build_hypothesis_space`), never from the human's script:

$$
H = \{ (\tau, b) : \tau \text{ a task schema},\ b \in \Pi_{v \in \mathrm{params}(\tau)} \mathrm{Objects}(\mathrm{type}(v)) \} \cup \{ \mathrm{unknown} \}
$$

one hypothesis per task and typed binding (`TaskSchema.parameter_types`), plus `unknown`, the residual
hypothesis: the hypothesis that the behaviour is none of them (glossary §7; whether a behaviour is described by
a hypothesis is its coverage, a world label the recognizer never receives). Keys are `repr(HypothesisKey)` strings and are sorted at construction, so every
order-dependent step (ties, log order) depends on the space alone.

The SUPPORT S is H when nothing is known of the observed agent's work order (prior-off, the default). With
`--assignment_prior true` (prior-on) it is restricted: S = assigned tasks ∪ foreseeable tasks
(`TaskSchema.is_foreseeable`) ∪ {unknown}; every other hypothesis is pinned at the floor and never scored.
The knowledge restricts the support; it is not a weight.

The LIVE set at tick t is S minus the tasks completed by t (§1.6). One recognizer instance observes one agent:
the odometer is kept per agent, the phase state per hypothesis only.

### 1.2 Prior

Uniform over the live set, `unknown` included: $\pi(k) = 1 / |\mathrm{Live}|$, at construction and again at every
episode boundary (§1.6), recomputed over what is still live. Nothing else is stored to restart from.
The robot observes the human once before the clock starts (`RobotAgent.observe_initial`), so step 0 is
already a scored step.

### 1.3 Phase: the expected action

Every tick, for every live hypothesis $k = (\tau, b)$, the planner decomposes $\tau$ against the current world for the
observed agent (`AdaptivePlanner.decompose`): the guards select the method (in kitting, what the agent holds
chooses between `deliver_default`, `deliver_already_held` and `deliver_with_return`), and the steps are
grounded. The EXPECTED action $a_\phi(k)$ is the first grounded action whose completion predicate does not hold in
the world. The phase is derived, never stored; what is stored per hypothesis is the action it expected on the
previous tick and its ORIGIN, the agent's position and odometer reading when it began expecting it. A change
of expected action (an advance, or a regress when `at()` flickers off at the proximity threshold) is a phase
change. Two actions are the same when their name and grounded bindings are.

A task's likelihood is the likelihood of the action it expects now: $P(o_t \mid \tau) = P(o_t \mid a_\phi(\tau))$.

### 1.4 Likelihoods

MOVEMENT (actions with `progress_evaluator = "excess_path"`, in kitting `move_to`). Measured from the origin $o$,
with $w$ the distance walked since $o$ (per-agent odometer: the sum of straight-line steps between observed
positions), $p$ the current position and $g$ the target's current position (`shared/target_resolution.py`; a
carried object resolves through its holder):

$$
 e = w + C(p, g) - C(o, g) \qquad \text{(the path wasted under the hypothesis)}
$$

$$
L = \frac{2}{1 + \exp(\beta \cdot e)} \qquad L(0)=1,\quad L(1/\beta)=\frac{2}{1+e}\approx 0.54,\quad L\to 0 \text{ as } e\text{ grows}
$$

$C$ is the path cost, straight-line by default and injectable (`IntentionRecognizer(path_cost=…)`). With a
static target and a metric $C$, $e \ge 0$ and $L \in (0, 1]$; a moving target can make $e$ negative, $L \in (0, 2)$. One
stretch toward one target is ONE observation however many ticks it spans: its value is recomputed from the
origin every tick and replaces the previous tick's. A stationary tick mid-stretch leaves $e$ where it was.

THE GRADE (graded evidence, September 2026). A stretch is also graded by how much of the hypothesis's expected
path it has covered:

$$
 f = \frac{C(o, g) - C(p, g)}{C(o, g)} \quad \text{clipped to } [0, 1];\qquad f = 0 \text{ when } C(o, g) = 0
$$

(`covered_fraction`: the share of the direct cost from the origin that the agent has closed; a step away from
the target covers nothing). At a fold whose closing action's completion predicate holds — an arrival — $f = 1$
by that fact: the world says the path is covered, so no arrival radius enters this layer. An observation with
no path (an action without evaluator or target, or an undecomposable hypothesis) is ungraded, $f = 1$. The
grade enters the stretch's likelihood under `unknown` (§1.5) and leaves $L$ untouched.

COMPLETION SIGNAL (an event). If the observed microaction is in the declared vocabulary of the action the
hypothesis expected on the PREVIOUS tick (`pick_up` → GRASP, `place` → RELEASE), the event factor is

$$
 c =
 \begin{cases}
 \mathrm{DETECTION\_HIT\_RATE}, & \text{if that action's grounded completion predicate holds now}\\
 \mathrm{DETECTION\_FALSE\_ALARM\_RATE}, & \text{otherwise}
 \end{cases}
$$

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
nothing while a rival with an open stretch pays its L/u^f (accepted, I4d point 4).

### 1.5 Evidence: odds against `unknown`

`unknown` is the reference, and it takes no factor of its own. Its likelihood for a stretch is graded,
$u^{f}$ with $u = \mathrm{UNKNOWN\_LIKELIHOOD}$ and $f$ the stretch's grade (§1.4, `graded_unknown_likelihood`):
$u$ for a stretch that covered a whole expected path, 1 for one that covered nothing, $u$ for an ungraded
observation. Each hypothesis's evidence is its odds against `unknown` over its OWN observations in the current
episode. For every live $k$ and tick $t$, the invariant is (update()'s docstring; checked to $7\times10^{-15}$
by an independent accumulator in `analysis/i4d_fold_unknown/` before the grade and again under it in
`analysis/g1_graded_evidence/`):

$$
O_t(k) = \frac{E_t(k)}{E_t(\mathrm{unknown})}
= \left[\frac{\pi(k)}{\pi(\mathrm{unknown})}\right]
\cdot \prod_{s \in \mathrm{stretches\ of\ } k \mathrm{\ closed\ by\ } t} \frac{L_k(s)}{u^{f_k(s)}}
\cdot \prod_{e \in \mathrm{events\ of\ } k} c_k(e)
\cdot \left(\frac{v_k(t)}{u^{f_k(t)}} \text{ if } k\text{'s open stretch is an observation, else }1\right)
$$

- The open stretch's current value v multiplies on top as v/u^f for this tick only, with f its grade now.
- A phase change FOLDS the closing stretch's final value into the base as L/u^f once — f = 1 if the closing
  action's completion holds — or nothing if that stretch was empty, and moves the origin to the agent's
  position and odometer reading. A fold moves a factor from the open term to the base without changing it.
  A regress folds too, and so does a no-graded-signal phase (as 1/u, ungraded).
- The grade meters confirmation only: L is charged in full whatever f, so a stretch walked away from its
  target (f = 0) pays L alone, and refutation by wasted path is as before. Log-linear in f, the odds of a
  walk accrue at a constant rate per unit of expected path, from 1 on its first step to 1/u at its arrival,
  and two stretches covering the halves of one path multiply to the whole.
- Events enter as c, not c/u.
- π(k)/π(unknown) = 1, since the prior is uniform.

The belief over the live set is $E_t(k) = O_t(k) / (1 + \sum_j O_t(j))$, with $E_t(\mathrm{unknown}) = 1 / (1 + \sum_j O_t(j))$.
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

$$
\tilde{P}(k) = E(k) \cdot \omega(k) \qquad \omega: \text{context weight, output only, never fed back};\ \omega(\mathrm{unknown})=1
$$

$$
P(k) = \mathrm{normalise}\big(\max(\mathrm{normalise}(\tilde{P})(k),\ \mathrm{BELIEF\_FLOOR})\big)
$$

$$
pinned\ keys\ (inadmissible \cup completed) = \mathrm{BELIEF\_FLOOR};\quad live\ keys\ scaled\ by\ 1 - \mathrm{BELIEF\_FLOOR}\cdot |pinned|
$$

`most_likely` is the argmax, and `confidence` is its value. Ties go to the first live key in sorted order,
and `unknown` sorts after every live task key, so it loses every tie. The recognizer owns its evidence:
`prev_belief` is accepted by `update()` and not consulted, because the reported distribution carries
output-only factors.

### 1.8 `update()` in pseudocode

Close enough to `IntentionRecognizer.update()` to check line by line; λ is `_progress_likelihood`, μ is
`_unknown_likelihood`, and ≡ is identity of name and bindings.

```python
# update(obs, world)
pos, mu = obs.position, upper(obs.microaction)
odo[agent] = odo[agent] + abs(pos - last_pos[agent])  # 0 on the agent's first observation
boundary = False
U = {}

for k in sorted(hypotheses):
    if k inadmissible or k completed:
        continue

    A = planner.decompose(k.task, k.bindings, agent, world)  # None on DecompositionError
    if A is not None and A[-1].completion in world.predicates:  # terminal pin
        if expected[k] == A[-1]:
            boundary = True  # the observed agent's own completion
        completed.add(k)
        del base[k], expected[k], origin[k], origin_odo[k]
        continue

    a = first action in A whose completion not in world.predicates  # None if A is None
    if k never observed:  # enters its action: empty stretch
        expected[k], origin[k], origin_odo[k] = a, pos, odo
        U[k] = base[k]
        continue

    a_prev = expected[k]
    if a_prev is not None and mu in vocabulary(a_prev):  # event
        base[k] *= HIT if a_prev.completion in world.predicates else FALSE_ALARM

    if a_prev != a:  # phase advance or regress
        L = lambda_(a_prev, origin[k], odo - origin_odo[k], pos)
        if L is not None:
            base[k] *= L / mu(a_prev, origin[k], pos, arrived=a_prev.completion in world.predicates)  # fold
        expected[k], origin[k], origin_odo[k] = a, pos, odo
        v = lambda_(a, pos, 0, pos)  # None if graded; 1 if not
    else:
        v = lambda_(a, origin[k], odo - origin_odo[k], pos)

    U[k] = base[k] * (v / mu(a, origin[k], pos) if v is not None else 1)

U[unknown] = base[unknown]  # the reference: no factor
Z = sum(U.values())
base = {k: v / Z for k, v in base.items()}
E = {k: v / Z for k, v in U.items()}

if boundary:  # episode ends
    base = uniform over (live keys ∪ {unknown})
    E = base.copy()
    for k in live_keys:
        origin[k], origin_odo[k] = pos, odo

P = output(E)  # §1.7
return BeliefState(distribution=P, most_likely=argmax(P), confidence=max(P))
```

The progress term used in the pseudocode is:

$$
\lambda(a, o, w, p)=
\begin{cases}
1, & \text{if } a = \mathrm{None} \text{ or } a \text{ has no progress\_evaluator or } a\text{'s target has no position},\\
\mathrm{none}, & \text{if } w \le 0,\\
\frac{2}{1 + \exp(\beta \cdot e)}, & \text{where } e = w + C(p,g) - C(o,g).
\end{cases}
$$

The graded reference under `unknown` is:

$$
\mu(a, o, p, \mathrm{arrived})=
\begin{cases}
u, & \text{if arrived, or } a = \mathrm{None}, \text{ or } a \text{ has no progress\_evaluator or no target position},\\
u^{f}, & \text{otherwise, with } f = \mathrm{clip}\big((C(o,g) - C(p,g)) / C(o,g),\ 0,\ 1\big).
\end{cases}
$$

Likelihoods are memoised per tick by their inputs: (evaluator, origin, walked, target) and the grounded
completion predicate. Two items on one shelf therefore receive identical values from the same origin.

### 1.9 Closed forms

- A lone live task on its first fitting stretch: $O = u^{-f}$, so confidence $= 1/(1 + u^{f})$ times the
  pinned-mass factor $(1 - 0.001 \cdot |pinned|)$: 0.5 at the first step, $\theta = 0.75$ at $f = \ln 3 / \ln 10 \approx 0.48$
  of the path (a little more with pins), 0.909 at the arrival. Measured, s00_on: 0.517 at 81 (first step),
  0.759 at 95, 0.894 at 108, 0.986 at 109 (`analysis/g1_graded_evidence/sweep/`).
- A lone live task with $n$ whole fitting observations: $O = u^{-n}$, confidence $1/(1 + u^n)$: 0.909 / 0.990 / 0.999
  unpinned, as before the grade.
- With rivals: $\mathrm{confidence}(k) = 1 / (1 + 1/O(k) + \sum_{j\neq k} O(j)/O(k))$ before floor and pins. $\theta = 0.75$ is
  reachable on a first fitting stretch ($O(k) = u^{-f}$) only if $\sum_j O(j)/O(k) < 1/\theta - 1 - u^{f}$; at the
  arrival ($f = 1$) that bound is 0.233; after one fold, $10 \times$ that (TODO-64).
- Two targets on one bearing at distances $d_1 < d_2$: equal excess, but after $x$ walked the nearer has odds
  $u^{-x(1/d_1 - 1/d_2)}$ over the farther (the grade is a distance term for collinear targets; TODO-38).
- $L = u$ at $e = \ln(2/u - 1)/\beta \approx 294\,\mathrm{cm}$: a stretch that wasted about $294\,\mathrm{cm}$ scores no better than `unknown`.
  $L(30\,\mathrm{cm}) = 0.85$, the slop at the proximity threshold (TODO-58).
- A step change of k's expected action, as at an arrival, is a fold of the closing stretch (at f = 1, L/u)
  plus, for a no-graded-signal next action, an open 1/u. An arrival at a shelf is therefore worth two
  observations at once (×10 on the odds from the tick before). This is TODO-61 (b)'s mechanism, open for
  the no-graded-signal phases.

## 2. Parameters

Four constants in `shared/likelihood_functions.py`, each with a physical meaning; `recognizer.py` reads them
through the module and never redefines them.

| constant | value | meaning |
|---|---|---|
| `BETA` (β) | 0.01 /cm | Detour tolerance. L at an excess of 1/β = 100 cm is 2/(1+e) ≈ 0.54 (the earlier text of this section said ≈ 0.27, which is the raw logistic's value; the logistic is normalised to 1 at zero excess, and the code comment on `BETA` is right). In centimetres, hence layout-scale dependent (TODO-58). REVISED (T-A1): a physical tolerance, fixed per embodiment, not per layout; supplied by the body (`IntentionRecognizer(beta=...)`, Mesa `mesa_configs.yaml`), no longer in `likelihood_functions.py`. |
| `UNKNOWN_LIKELIHOOD` (u) | 0.1 | The likelihood under `unknown` of an observation that covered one whole expected path; a stretch pays u^f for its grade f (§1.4). The bar a hypothesis must clear per whole observation, and the unit of the ceiling 1/(1 + uⁿ) over n whole observations. |
| `DETECTION_HIT_RATE` | 1.0 | P(signal \| the action completed). Mesa reports every completion. |
| `DETECTION_FALSE_ALARM_RATE` | 10⁻³ | P(signal \| not completed). Mesa has none; non-zero only so a refuted hypothesis keeps a recoverable base. Set both rates from a real detector's measured rates. |

β and u were chosen jointly (I4: the region where every first task is revealed before its grasp with no wrong
task at θ is β ∈ [0.005, 0.1] × u ∈ [0.01, 0.2]; the chosen point is its centre; `analysis/i4_evidence_model/`,
closed, not to be reopened by sweeping). The grade changed what u means (per whole path, not per stretch),
not its value; by decision, u, β and θ stayed as they were and nothing was re-swept.

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
conditions are the five regression fixtures and the three evaluation fixtures (s50, s70, s71) × assignment
prior off/on, PYTHONHASHSEED=0, at the graded-evidence HEAD. The figures are from
`analysis/g1_graded_evidence/` (`sweep/`, logs local; `summary.md`, committed). Where a figure moved with the
grade the pre-grade value (D2's sweep, `analysis/d2_recognition_trigger/`) is given as old → new; the pre-grade
figures differ from the I5 matrix because the fixtures and the robot changed (s40 retyped in F47b, s10 back in
the sweep, prior-off pins following the robot's deliveries). Ticks are `[IR] step=` values. A reveal is the
first tick the true task is `most_likely` with confidence ≥ θ; "done" is the human's boundary tick.

| fixture | task (human, in order) | reveal prior-on | reveal prior-off | grasp / completion |
|---|---|---|---|---|
| s00 | item_3 | 11 → 20 | 39 → 37 | grasp 41 |
|  | item_2 | 81 → 95 | 109 | grasp 111 |
| s10 | item_2 | 25 → 24 | 29 | grasp 31 |
|  | coffee_break | 123 | 123 | arrival 123, done 154 |
|  | item_5 | 163 → 202 | 247 → 245 | grasp 249 |
|  | ac_activation(ac_switch_0) | 314 → 339 | 334 → 341 | done 365 |
| s20 | item_3 | 6 → 11 | 20 | grasp 22 |
|  | item_2 | 57 → 72 | 87 | grasp 89 |
| s30 | item_3 | 21 → 23 | 28 → 27 | grasp 39 |
|  | item_7 | 77 → 87 | 86 → 88 | grasp 98 |
| s40 | item_3 | 21 → 30 | 21 → 30 | grasp 60 |
|  | coffee_break | 153 | 153 | arrival 153, done 184 |
|  | ac_activation(ac_switch_1) | 205 | 205 | arrival 205, done 207 |
|  | ac_activation(ac_switch_2) | 218 → 219 | 221 → 220 | done 228 |
|  | item_6 | 250 → 254 | 266 → 265 | grasp 272 |
| s50 | item_3 | 8 → 11 | 20 | grasp 22 |
|  | item_2 | 72 → 75 | 87 | grasp 89 |
|  | coffee_break | 125 → 136 | 139 | done 178 |
| s70 | coffee_break | 23 | 23 | done 54 |
|  | item_5 | 61 → 60 | 61 | grasp 63 |
|  | ac_activation(ac_switch_0) | 98 → 120 | 116 → 122 | done 143 |
| s71 | coffee_break | 23 | 23 | done 54 |
|  | item_5 | 61 → 60 | 61 | grasp 63 |
|  | ac_activation(ac_switch_0) | 98 → 120 | 108 → 120 | done 143 |

### 3.1 Prior-on (the observed agent's assignment is known)

The recognizer GUARANTEES:
- **The belief is over the assigned tasks, the foreseeable tasks and `unknown` only.** Everything else is
  pinned at 10⁻³ and never scored.
- **Every task the human executes is revealed above θ before its grasp, or before its completion for a task
  with no grasp.** See the table. Of the foreseeable tasks, coffee (s10 123, s40 153, s70 / s71 23) and
  ac_switch_1 (205) are revealed at their arrival fold; ac_switch_2 (219), s10's and s70 / s71's AC task (339,
  120) and s50's coffee (136) mid-walk.
- **HOW the one-task reveals happen: at about half the walk, not on the first step.** After the boundary the
  human's last assigned task is the only live task and the belief is the prior over {task, unknown} (0.498).
  Before the grade one fitting step took it to 0.905 (s00 81, s20 57, s30 77, s10 314, s70 / s71 98). Under the
  grade the walk lifts it as 1/(1 + u^f): θ at f ≈ 0.48 (s00 95, s20 72, s30 87, s10 339, s70 / s71 120, all
  at odds 3.1–3.4 against `unknown`; `analysis/g1_graded_evidence/crossings.md`). The gate is still cleared by
  the size of the live set plus half a walk: over two live keys the same walk needs more of the path (s10_on
  item_5 at 202, 46 ticks into a 91-tick walk), and over more, an arrival (TODO-64).
- **No wrong task reaches θ** in any prior-on condition.
- **One crossing of θ per recognition.** No task crosses twice within its episode.
- **After the human's own task completion, the belief is the uniform prior over the live set** until the
  human moves: 0.498 each over {task, unknown} in s00/s20/s30, 0.331 over three live keys in s40 at 228.
  `most_likely` on those ticks is the key-order tie-break, and its confidence is 1/|Live| (with pins).
- **Confidence on a fitting task rises along a walk and steps at its folds**: 1/(1 + u^f) on a lone
  stretch, then 1/(1 + uⁿ) over n whole observations, with pins: s00_on 0.517 (81, first step) → 0.759 (95)
  → 0.894 (108) → 0.986 (109, arrival fold plus the open pick_up phase). It can legitimately FALL when the
  next expected action stops fitting. Non-monotone by design; do not smooth.
- **A completed task is at the floor for the rest of the run**, whoever completed it.
- **Once every admissible task is complete, `unknown` holds all live mass** (0.995 in s00/s20/s30 from the
  last boundary, 0.990 in s10). In s40 the never-performed foreseeable `ac_activation(ac_switch_0)` stays
  live and ties with `unknown` at 0.496; it is `most_likely` by the tie-break.

### 3.2 Prior-off (no assignment known)

The same model over a larger live set: every task of every object, the robot's own undelivered items
included. Therefore:
- **Every reveal still precedes the grasp** (or the completion), and **no wrong task reaches θ**, in all eight
  fixtures. Several prior-off reveals are the arrival fold, two ticks before the grasp: s00 109, s10 29, s20 /
  s50 20 and 87, s70 / s71 61. There the walk alone did not separate the true task from its rivals; the
  arrival's two observations did (§1.9). The others are on the walk (s00 37, s10 245 and 341, s30 27 and 88,
  s40 30 / 220 / 265, s50 139, s70 122, s71 120), where the grade now separates the true task before its
  arrival — the pre-grade first reveals moved little (s00 39 → 37, s30 28 → 27, s10 / s20 / s50 / s70 / s71
  unchanged), except s40's item_3, 21 → 30 on the human's longest first walk (grasp 60): at 21 it had covered
  a third of its path, odds u^{−0.35} ≈ 2.2 rather than 10.
- **Repeated crossings within one recognition**: s20 / s50 20 / 27 and 87 / 92 (pre-grade also s00 109 / 113 /
  115, s10 29 / 33 / 35, s20 / s50 20 / 24 / 30 and 87 / 91 / 95, s70 / s71 61 / 65 / 72). At the grasp every
  rival's method flips to `deliver_with_return`. Its `place`-back-on-the-shelf phase is a no-graded-signal
  observation worth 1/u (ungraded), so the true task still dips under θ at the grasp (s20_off 0.927 at 21,
  0.595 at 22) and recovers along the carry (0.806 at 27). The second dip — on departure the rival regressed to
  a fresh zero-excess stretch worth 1/u on its first step — is gone: that stretch walks away from the shelf,
  f = 0, and pays its L alone. This is the model working as specified (TODO-61 (b), TODO-55 (e)). Since D2 the
  consumer tracks identity and these crossings do not re-decide (§5).
- **An idle human sits at the prior over what is still live**, meaning the robot's undelivered items and any
  foreseeable task never performed. After the human's last task: s00 item_4 at 0.498; s10 item_0 at 0.248,
  then 0.331 from 418; s20 item_6 at 0.332, then item_7 at 0.498 from 145; s30 item_2 at 0.332, then item_6
  at 0.498 from 160; s40 `ac_activation(ac_switch_0)` at 0.331, then 0.496 from 376. A robot delivery shrinks
  the set (the pin) without re-initialising (no boundary). Never at θ. When the robot delivers the last live
  item, `unknown` takes 0.995 (s00 166, s20 235).
- **Dilution**: more live rivals mean less confidence from the same evidence and later reveals. Examples:
  ac_switch_1 at its arrival (205), 0.959 prior-on against 0.934 prior-off; item_5 in s10, revealed at 202
  prior-on and 245 prior-off; item_6 in s40 at 254 against 265.

### 3.3 What every figure above is conditional on

- **Straight lines.** Mesa agents walk straight through obstacles and C is Euclidean, so the true
  hypothesis's excess is exactly 0. In a real cell with obstacles, every detour the path cost does not model
  is charged to the true hypothesis. Inject a path cost before reading any figure here as a guarantee there.
- **`PROXIMITY_THRESHOLD` = 30 cm.** Every arrival fold is taken 30 cm from the target; a different threshold
  moves every reveal tick and every ceiling step.
- **Kitting's decompositions and guards.** The prior-off repeated crossings are `deliver_with_return`'s
  phases. The arrival's double observation is `move_to` followed by a no-graded-signal action.
- **The layout's decoy geometry.** Targets on one bearing tie in excess for the whole walk; the grade
  separates them by distance covered, the nearer first, and the arrival fold finishes it (s40_on 187–204:
  ac_switch_1 and item_6 tied before the grade, 0.248 → 0.417; now 0.216 / 0.201 → 0.682 / 0.194, the switch
  being the nearer; at 205, 0.959 against 0.023. s20_off's collinear shelves lie behind item_3's: 0.506 /
  0.226 / 0.201 at 19, revealed at the arrival, 20). A decoy on the true bearing BEFORE the target gains
  mid-walk under the grade (TODO-38) and, within 30 cm of the path, folds first: it could cross θ wrongly. No
  fixture has one.
- **The live set's size**: it sets the prior and the dilution. Under the grade it no longer sets the crossing
  odds against `unknown`; unrefuted rivals raise the odds a crossing needs (§5, the gate ruling; TODO-64 / 65
  closed).
- **β, u**: they set every reveal tick (I4 / I4b / I4c region analysis, closed).
- **The human's script.** A human who hesitates, back-tracks or wanders mid-task is charged as a rival would
  be. An unmodelled stand is not evidence (TODO-59's deferred channel, not built); a stand inside a modelled
  `wait_at` phase is that hypothesis's no-graded-signal observation (§1.5). Every task in the script is one
  the domain describes (well typed, F47b); unmodelled behaviour in a run is either a declared experimental
  condition (TODO-80) or unintended (glossary §7, label C).

### 3.4 What the meta-planner may assume, and must not

MAY assume, either setting: a task at or above θ is the task being executed now. There is no wrong task at θ
in the measured conditions, but see §3.3 on a decoy before the target. A completed task never returns. After
the human's own completion the belief is the prior, and `most_likely` carries no information until the human
moves. Prior-on: one crossing per recognition. Prior-off: up to two crossings within the grasp stop, all on
the same task.

MUST NOT assume, either setting:
- that confidence is comparable across live-set sizes (0.75 is a different bar over 2 and over 8 keys);
- that confidence ≥ θ implies more than half a walk (a lone live task clears θ at f ≈ 0.48 of its first
  stretch, from a prior of 0.5);
- that `unknown` ≥ θ means the human is idle: it also means unmodelled behaviour (a task the space does not
  contain, a detour under way), or every task pinned, where the mass is `unknown`'s by normalisation (glossary §7);
- that a robot completion is a human boundary;
- that the ceiling is a constant (it is 1/(1 + uⁿ));
- that confidence is monotone within a task;
- that anything in the belief refers to a previous episode.

## 4. Characterised limitations, and the open design item

Properties of the chosen model, not defects (TODO-61). Both had one root, costdif1 with a constant `unknown`:
a fitting stretch scored L = 1 whatever its length, and every scored observation was worth L/u against a
constant reference. The grade (September 2026) changed that for walks and left it for everything else.

**(a) Confirmation was length-blind — closed for walks by the grade.** The excess discriminates by penalising
wrong hypotheses, not by rewarding right ones: the correct hypothesis sits at zero excess however far it walks.
Under the grade its odds against `unknown` rise with the path covered, u^{−f}, from 1 on the first step to 1/u
at the arrival (§1.5, §1.9); the pre-grade one-step reveals (§3.1) are gone, and collinear targets separate by
distance covered before the arrival (§3.3). L itself is unchanged: refutation is as it was.

**(b) Accumulation is observation-count and decomposition sensitive — open for the no-graded-signal phases.**
A stationary `pick_up`, `place` or `wait_at` phase and an undecomposable hypothesis are still one whole
observation, 1/u, whatever they observed; how a selected method cuts a walk into such phases
therefore still sets how much evidence a hypothesis can gather. Seen at HEAD:
- an arrival still counts twice (the fold at f = 1 plus the open no-graded-signal phase), which is what
  finishes the separation of collinear targets and produces the arrival-fold reveals (§3.2);
- the prior-off dip at the grasp comes from the rivals' `deliver_with_return` `place` phase; the second dip,
  at the departure, came from their fresh stretch and is gone (a walk away from the target pays L alone).
For walks the grade is TODO-61's "u per unit of evidence" (the unit being the hypothesis's own expected
path): two stretches covering the halves of one path are worth the whole, so a walk's value no longer
depends on where the phase machinery cuts it.

**GRADED EVIDENCE, built (September 2026; design_decisions.md, "A stretch's evidence against `unknown` is
graded by the share of the expected path it covers").** The form is L / u^f, f the covered fraction of the
expected path, 1 at an arrival by the completion fact (§1.4). u, β and θ were kept by decision. The
accounting invariant was re-checked (§1.5). What the grade did to the reveals and to the meta-planner's
decisions is in `analysis/g1_graded_evidence/summary.md` (consequences, not judged): the one-task reveals
follow the walk; the prior-off first-task reveals moved little except s40 (21 → 30); no wrong task at θ;
robot motion changed in six of sixteen conditions. Not built, by scope: grading of the no-graded-signal
phases ((b) above).

**DECIDED on the data this build reports: θ stays a fixed share (the gate ruling, September 2026; §5).**
`analysis/g1_graded_evidence/crossings.md` carries, at every crossing of θ and on the two ticks either
side, the top hypothesis's odds against `unknown`, the ratio of the top two and the live-set size. Read
from it: 25 of the 30 walk crossings sit at top odds 3.1–4.2 whatever the live set (1 to 9 keys), the other
five at 5.2–9.4 with one rival still live (top-two ratio 5.2–12.3); every arrival crossing at about 100. The
lowest top-two ratio at a walk crossing is 5.23 (s00_off 37); the 3.26 of s20_off / s50_off 92 is a
post-arrival re-crossing at odds 116. (This paragraph said "every walk crossing at 3.1–4.2" before the
ruling; corrected.) The live-set dependence was the likelihood's and the grade removed it, so the gate is
unchanged (TODO-64 / 65 closed). Grading changed what `unknown` means (per whole path); the
rationality-measure alternative (TODO-63) is still to be weighed against it, on the same ground.

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
- `_clears_gate(belief)`, the one place θ is applied, tests `confidence ≥ θ`, θ = `DEFAULT_THETA` = 0.75,
  on the normalised share. Under graded evidence the share is
  $O(k) / (1 + O(k) + \sum_{j \neq k} O(j))$ (§1.9), so θ reads "the top hypothesis at least about 3:1 over
  no model, and more while unrefuted rivals remain". A lone task clears at $f \approx 0.48$ of its expected
  path, a fraction, not a distance; a crossing that comes later under ambiguity is intended. The crossing
  odds do not depend on the live-set size, because the walk refutes the rivals (§4). This is the gate
  ruling (September 2026; `design_decisions.md`, "The gate stays a fixed share"), which closed TODO-64 / 65.
  Not taken: odds against `unknown` (drops the rivals' term), the ratio of the top two (infinite for a lone
  task), θ from the live-set size or the layout, a rate-of-growth gate. What reopens it: a walk crossing
  with a live rival at similar odds, which no current fixture shows (TODO-47 (g), the randomised fixtures).
- `evaluate_triggers()` fires `recognition_changed` (D2) when a decision record `_projected_hypothesis`
  exists and `most_likely` is no longer it. That covers a replacement, the human's boundary, or `unknown`
  after a pin. It also fires when no record exists and the belief clears the gate on a task, not `unknown`.
- `update_human_projection()` admits a projection only when the gate clears and `most_likely` is not
  `unknown`. It resolves the key through `recognizer.get_hypothesis()` (the same live instance, held by
  reference) to project the human's task, and records the hypothesis it projected.

Confidence is a gate, never a magnitude in any cost; `distribution` is logged and not read. (See TODO-97 (24 Sept 2026): belief-aware planning, one realization against the hypotheses covering 1 − ε of the mass, recorded for after the T-D recognizer pass, not decided.) The one-shot
question of the I5 hand-back (TODO-68, with TODO-48 and TODO-54) is closed by D2 on the consumer side. A
re-crossing of the recorded hypothesis fires nothing; a change of hypothesis or its end fires. No change was
made to the recognizer or to its event semantics (`design_decisions.md`, the D2 entry;
`analysis/d2_recognition_trigger/README.md`).

## 6. Open items

| item | where | one line |
|---|---|---|
| the no-graded-signal phases under the grade | TODO-61 (b) | §4; `pick_up`, `place`, `wait_at` still one whole observation each; (a) closed for walks |
| the gate's reopening condition | TODO-47 (g) | a walk crossing with a live rival at similar odds; none in the current fixtures; watched for in the randomised fixtures (§5) |
| collinear decoys under the grade | TODO-38 | the grade is a distance term for targets on one bearing; a decoy before the target gains mid-walk; no fixture has one |
| `deliver_with_return`'s guard | TODO-55 (e) | a stray item vs an assigned one; a domain question, the producer of the prior-off repeated crossings |
| β in centimetres | TODO-58 | layout-scale dependence |
| the stationarity channel | TODO-59 (deferred paragraph) | standing still as evidence against movement hypotheses; not built |
| declared unmodelled behaviour | TODO-80 | a human stay no hypothesis describes, declared as the scenario's experimental condition; not built |
| the context / knowledge-representation pass | TODO-66 | `_context_weight` names two tasks and carries four constants; output only, inert |
| the two analytical tools | TODO-62, TODO-63 | radius of maximum probability (diagnostic); rationality measure (competes with `unknown`) |
| hash-seed dependence | TODO-42 | resolved for the recognizer (sorted keys); runs still need `PYTHONHASHSEED=0` |

Closed since the I5 hand-back: TODO-48 / 54 / 68 (D2); TODO-64 / 65 (the gate ruling, §5); TODO-72 (io_contracts §1.3 / §2.1 aligned with this
document); TODO-52 (R1 / T10) and TODO-67 (T7), both meta-planner side; TODO-57's script-part-3 question (the record calls it segment 3), made
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
| the previous posterior as the prior (`prev_belief` fed back) | the output carries state-only factors; feeding it back counted them twice | Sept 10 session; I3 |
| the 10× assignment multiplier | knowledge of the assignment restricts the SUPPORT, not the magnitude | assignment-pool entry |
| the held-item rule (refute a hypothesis that binds a portable object the agent is not holding) | a domain shortcut the phase model subsumes; wrong in domains with no holding relation | I3 |
| `ZONE_BOOST` | a soft multiplier standing in for a hard fact; fired for the wrong hypothesis in 28 of 52 measured episodes (I1 §5.4) | I3 |
| the global leg (one movement leg for all hypotheses, closed by the body's `stand`) | a stretch is per hypothesis, from its own origin; no leg closed by stillness, no decay | I2–I4 |
| HIGH / LOW / NEUTRAL likelihoods (4.0 / 0.1 / 1.0) | four numbers with no stated meaning; replaced by the excess-path logistic, detection reliability and a stated u | I4 |
| the cosine trajectory kernel (`"directional"`) | multiplied identical headings tick after tick (4ⁿ from one straight walk); replaced by one observation per stretch | Sept 10 session, I4 |
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
| Sept 10 | per-tick multiplication of identical headings (4ⁿ from one walk) | one observation per movement leg (the leg model, removed since; §8); output-only state factors | consecutive steps are duplicates, not independent evidence; the retracted "early reveals" were duplicate counting |
| I1 audit | — | measurement only | 0 of 5,579 likelihood calls evaluated a completion; ZONE_BOOST wrong in 28 of 52 episodes |
| I2 foundations | the recognizer's own target lookup, `methods[0]`, `"?item"` | targets, methods and completions from the planner and `target_resolution`; `waited` observable; sorted keys; first step scored | one answer to "where is the target"; no domain literals |
| I3 phase model | a single `holding` check choosing "phase 1 / 2"; the held-item rule; ZONE_BOOST | the derived expected action per hypothesis with its own origin; the terminal-completion pin | a task's likelihood is its current action's; completion is a world fact |
| I4 evidence model | cosine kernel, HIGH / LOW / NEUTRAL | excess-path likelihood (normalised logistic), detection reliability, constant u; β and u from a joint sweep | four constants with physical meanings; wasted distance was never charged before (TODO-53) |
| I4b / I4c boundary | origins moved only at an action change (coffee entered its own walk with 2144 cm of excess); then I4b's "reset geometry, keep belief" | the observed agent's own completion ends the EPISODE: belief to the prior over the live set, origins reset | a task hypothesis means the task being executed now; keeping folds across the boundary depended on accidental phase history |
| I4c empty-stretch rule | an empty stretch scored as a perfect walk (a lone survivor at 0.909 on nothing; 63 wrong-task ticks) | an empty stretch is no observation, no factor | zero excess meant two things; no walk is not an efficient walk |
| I4d | u charged only while a stretch was open (fold tick 0.905 → 0.498, a false re-trigger) | u folds with the stretch: evidence is odds against `unknown` (§1.5), invariant checked to 7e-15 | the evidence a stretch gave against `unknown` was lost at its fold |
| I5 hand-back | — | confirmation matrix at HEAD, guarantee statement, limitations (`analysis/i5_handback/`) | — |
| Sept 15 (θ single source) | `CONFIDENCE_THRESHOLD` in `recognizer.py`, unread | `DEFAULT_THETA` in the meta-planner, applied in `_clears_gate` only | the recognizer emits a belief and gates nothing |
| Sept 17, F47b (fixture, not model) | scenario_40's script part 3 walks (the record calls it segment 3) scripted as `ac_activation` bound to two waypoints: ill-typed, so the space had no hypothesis for them | the targets retyped as `ac_switch_1` / `ac_switch_2` at the same coordinates; bindings type-checked at spawn (`check_task_bindings`) | a behaviour the domain does not describe can never be recognised. The I5 matrix's only wrong crossing (item_6, s40 203–213) was that walk: now the walk is its own task, tied with item_6 until its arrival fold (205). All s40 figures in §3 are from the corrected fixture. |
| Sept 17, D2 (consumer) | `theta_crossed` as the trigger | `recognition_changed` against the decision record (§5) | a trigger is a change in what the decision rested on; recognizer unchanged |
| Sept 19, graded evidence | a stretch's odds against `unknown` L/u whatever its length: one fitting step was a whole observation, and a lone task cleared θ on the human's first step | L / u^f, f the fraction of the expected path the stretch covered, 1 at an arrival by the completion fact (§1.4, §1.5); u, β, θ unchanged; invariant re-checked to 7e-15 | the model counted stretches and did not grade them by how much they revealed; a walk's evidence now accrues per unit of path and does not depend on how the phases cut it. Every figure in §3 is from this HEAD, with the pre-grade value where it moved. |

Superseded figures (the I5 matrix, and any s40 figure before F47b) are not carried here. Where they are cited
elsewhere they describe the fixture of their time.
