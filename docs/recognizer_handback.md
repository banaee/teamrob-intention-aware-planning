# The intention recognizer — current description
REWRITTEN TO HEAD at the T-D Stage 1 build (27 September 2026; design_decisions.md, "T-D R and E"): the `unknown`
hypothesis, u, the grade and the odds accounting are gone (R1); the recognizer reports an adequacy finding and a
lifecycle state beside the belief (R2 to R4, E1 to E7). The earlier text is in git history (before commit 367a3a7).

What `shared/recognizer.py` and `shared/likelihood_functions.py` do at HEAD (September 2026), for two readers:
later sessions of this project, and colleagues who last saw the recognizer before July 2026 (start with §9,
the revision since then, then §1). Every formula and constant below is read from those two files; where an
earlier text or a docstring says otherwise, the code wins and the difference is stated. The design history is
in `docs/design_decisions.md` (entries I2–I5, "θ has one home", F47b, D2, graded evidence, T-D R and E); open
items in `docs/TODOS_AND_DEFERRED.md`; the interface in `shared/io_contracts.md` §1.2 and §2.1.

Section numbers §1–§5 and §8 are cited from code and other docs; keep them stable. Terms are used as
`docs/glossary.md` defines them: the recognizer's unit of movement evidence is a STRETCH, the adequacy test's
unit is a DERIVED PHASE, a human's movement is a WALK ("leg" is not used, and the removed leg model keeps its
name in §8 only), a CROSSING is a θ crossing, and scenario_40's "segment 3" is a SCRIPT PART, not a `Segment`.

## 1. The model

### 1.1 Hypotheses and support

The hypothesis space is built once, at robot construction, from the domain schemas and the workspace objects
(`build_hypothesis_space`), never from the human's script:

$$
\mathcal{K} = \{ (\tau, b) : \tau \text{ a task schema},\ b \in \Pi_{v \in \mathrm{params}(\tau)} \mathrm{Objects}(\mathrm{type}(v)) \}
$$

one hypothesis per task and typed binding (`TaskSchema.parameter_types`). There is no residual hypothesis
(T-D R1): whether a behaviour is described by a hypothesis is its coverage, a world label the recognizer never
receives (glossary §7), and whether the best of the robot's models is wrong is the adequacy finding's question
(§1.10). Keys are `repr(HypothesisKey)` strings and are sorted at construction, so every order-dependent step
(ties, log order) depends on the space alone.

The SUPPORT is the whole space when nothing is known of the observed agent's assigned tasks (prior-off, the
default). With `--assignment_prior true` (prior-on) it is restricted: assigned tasks ∪ foreseeable tasks (every
hypothesis of a `PersonalTask`); every other hypothesis is pinned at the floor and never scored. The knowledge
restricts the support; it is not a weight.

The LIVE set H at tick t is the support minus the tasks completed by t (§1.6). One recognizer instance observes
one agent: the odometer and the standing clock are kept per agent, the phase state per hypothesis only.

### 1.2 Prior

Uniform over the live set: $\pi(k) = 1 / |H|$, at construction and again at every episode boundary (§1.6),
recomputed over what is still live. Nothing else is stored to restart from. A lone live hypothesis therefore
reads 1.0 on no evidence, and two rivals start at 0.5 (R1: expected, measured in Stage 1, not corrected). The
robot observes the human once before the clock starts (`RobotAgent.observe_initial`), so step 0 is already a
scored step.

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
 e = w + C(p, g) - C(o, g) \qquad \text{(the path wasted under the hypothesis; } \texttt{excess\_path}\text{)}
$$

$$
L = \frac{2}{1 + \exp(\beta \cdot e)} \qquad L(0)=1,\quad L(1/\beta)=\frac{2}{1+e}\approx 0.54,\quad L\to 0 \text{ as } e\text{ grows}
$$

$C$ is the path cost, straight-line by default and injectable (`IntentionRecognizer(path_cost=…)`). With a
static target and a metric $C$, $e \ge 0$ and $L \in (0, 1]$; a moving target can make $e$ negative, $L \in (0, 2)$. One
stretch toward one target is ONE observation however many ticks it spans: its value is recomputed from the
origin every tick and replaces the previous tick's. A stationary tick mid-stretch leaves $e$ where it was. The
excess $e$ is computed once (`likelihood_functions.excess_path`, registered in `EXCESS_MEASURES` under the
evaluator's name) and read by both the likelihood and the adequacy test (§1.10).

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
nothing while a rival with an open stretch pays its L (accepted, I4d point 4). Time never enters the belief:
a stand is charged in the adequacy test only (§1.10; E3).

### 1.5 Evidence: normalised likelihood over H

Each live hypothesis's evidence is the product of its OWN observations in the current episode, normalised over
H. For every live $k$ and tick $t$:

$$
E_t(k) \propto \pi(k)
\cdot \prod_{s \in \mathrm{stretches\ of\ } k \mathrm{\ closed\ by\ } t} L_k(s)
\cdot \prod_{e \in \mathrm{events\ of\ } k} c_k(e)
\cdot \left(v_k(t) \text{ if } k\text{'s open stretch is an observation, else }1\right),
\qquad \sum_{k \in H} E_t(k) = 1
$$

- The open stretch's current value v multiplies on top for this tick only.
- A phase change FOLDS the closing stretch's final value into the base once — or nothing if that stretch was
  empty — and moves the origin to the agent's position, odometer and standing-clock readings. A fold moves a
  factor from the open term to the base without changing it. A regress folds too; a no-graded-signal phase
  folds 1.
- Events enter as c.

One normalisation, over H. The stored bases are rescaled by the same total each tick, so they stay in one
scale and evidence = base × open value exactly.

THE INVARIANT (R6), at two levels (read by Hadi on the Stage 1 plan, 27 September 2026, so that the entry's
wording is not read as a claim about the floored output): (1) the normalised evidence (`_evidence`) sums to 1
over exactly H before the output floor, and a retired or inadmissible hypothesis is never in H; (2) the returned
distribution sums to 1 with every pinned key at exactly `BELIEF_FLOOR` and the live keys carrying the rest
(§1.7). Checked every tick in `tests/test_td1_adequacy.py`. The earlier invariant "belief equals odds against
`unknown`" no longer exists.

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
\tilde{P}(k) = E(k) \cdot \omega(k) \qquad \omega: \text{context weight, output only, never fed back}
$$

$$
P(k) = \mathrm{normalise}\big(\max(\mathrm{normalise}(\tilde{P})(k),\ \mathrm{BELIEF\_FLOOR})\big)
$$

$$
pinned\ keys\ (inadmissible \cup completed) = \mathrm{BELIEF\_FLOOR};\quad live\ keys\ scaled\ by\ 1 - \mathrm{BELIEF\_FLOOR}\cdot |pinned|
$$

`most_likely` is the argmax over H, and `confidence` is its value. Ties go to the first live key in sorted
order. A lone live hypothesis reads 1.0 in the evidence and $1 - \mathrm{BELIEF\_FLOOR}\cdot|pinned|$ in the
output (0.996 with four pins). The recognizer owns its evidence: `prev_belief` is accepted by `update()` and not
consulted, because the reported distribution carries output-only factors.

EXHAUSTED (R4; read by Hadi on the Stage 1 plan, 27 September 2026). When H is empty the belief over H has no
members: `distribution` holds the retired and inadmissible keys at `BELIEF_FLOOR` — the output convention, not
belief mass, so it does not sum to 1 — `most_likely` is `None` and `confidence` 0.0. The authoritative signal is
the lifecycle state EXHAUSTED. The meta-planner's gate reads 0.0 and refuses admission as `none(below_theta)`:
the expected, measured behaviour in this cycle, not a design (G).

Beside the belief, `BeliefState` carries the adequacy finding, the lifecycle state and the members' tail
probabilities (§1.10). Belief and finding are independent outputs (R3).

### 1.8 `update()` in pseudocode

Close enough to `IntentionRecognizer.update()` to check line by line; λ is `_progress_likelihood`, and ≡ is
identity of name and bindings.

```python
# update(obs, world)
pos, mu = obs.position, upper(obs.microaction)
step = abs(pos - last_pos[agent])                 # 0 on the agent's first observation
odo[agent] += step; still[agent] += (step == 0)   # the walking and the standing clocks
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
        del base[k], expected[k], origin[k], origin_odo[k], origin_still[k]
        continue

    a = first action in A whose completion not in world.predicates  # None if A is None
    if k never observed:  # enters its action: empty stretch
        expected[k], origin[k], origin_odo[k], origin_still[k] = a, pos, odo, still
        U[k] = base[k]
        continue

    a_prev = expected[k]
    if a_prev is not None and mu in vocabulary(a_prev):  # event
        base[k] *= HIT if a_prev.completion in world.predicates else FALSE_ALARM

    if a_prev != a:  # phase advance or regress
        L = lambda_(a_prev, origin[k], odo - origin_odo[k], pos)
        if L is not None:
            base[k] *= L  # fold
        expected[k], origin[k], origin_odo[k], origin_still[k] = a, pos, odo, still
        v = lambda_(a, pos, 0, pos)  # None if graded; 1 if not
    else:
        v = lambda_(a, origin[k], odo - origin_odo[k], pos)

    U[k] = base[k] * (v if v is not None else 1)

Z = sum(U.values())                               # over H only
base = {k: v / Z for k, v in base.items()}
E = {k: v / Z for k, v in U.items()}

if boundary:  # episode ends
    base = uniform over live keys
    E = base.copy()
    for k in live_keys:
        origin[k], origin_odo[k], origin_still[k] = pos, odo, still

P = output(E)  # §1.7
most_likely, confidence = (argmax over H of P, its value) if E else (None, 0.0)
finding, lifecycle, tails = adequacy(pos, odo, still)  # §1.10
return BeliefState(P, most_likely, confidence, finding, lifecycle, tails)
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

Likelihoods are memoised per tick by their inputs: (evaluator, origin, walked, target) and the grounded
completion predicate. Two items on one shelf therefore receive identical values from the same origin.

### 1.9 Closed forms

- A lone live task: 1.0 in the evidence whatever it observes (a relative belief over one member), in the
  output $1 - 0.001 \cdot |pinned|$. It clears θ = 0.75 the tick it becomes the lone live task — by
  normalisation, at a boundary or a pin, on no evidence (R1).
- Two rivals $j, k$ with no events: $E(k) = \prod L_k / (\prod L_k + \prod L_j)$. From an even prior, θ needs a
  likelihood ratio of 3 in $k$'s favour; one fitting stretch against a rival stretch of excess $e$ gives
  $1/L(e) = (1 + e^{\beta e})/2$, which is 3 at $e = \ln 5/\beta \approx 161\,\mathrm{cm}$.
- With $n$ live keys and an even prior, confidence $= 1/(1 + \sum_{j \ne k} R_j)$ with $R_j$ the rivals' likelihood
  ratios against $k$: θ needs $\sum_j R_j \le 1/3$. Confirmation is by refutation of the rivals alone: the true
  hypothesis on a straight walk has L = 1 and gains nothing on its own; an arrival fold adds nothing (L = 1).
- $L(30\,\mathrm{cm}) = 0.85$, the slop at the proximity threshold (TODO-58).
- There is no ceiling below 1 (the ceiling $1/(1 + u^n)$ went with u).

### 1.10 The adequacy finding (T-D E1 to E7)

The recognizer's second output, computed after the belief, from scratch every tick (`_adequacy`).

UNIT (E1). Each live hypothesis's DERIVED PHASE: from its existing origin to its phase advance. No window, no
episode constant. A regress at the proximity threshold is a phase change and restarts that hypothesis's test
(limitation (b) of the entry).

STATISTIC (E2, E3). Per live hypothesis $k$ in its derived phase, the projected completion delay, in ticks:

$$
D_k = e_k / v + (s_k - s_{\mathrm{exp}})
$$

$e_k$ the excess path from the origin exactly as the movement likelihood computes it (0 for a phase with no
evaluator or no resolvable target: `pick_up`, `place`, `wait_at`); $v$ the body's speed; $s_k$ the ticks without
movement since the origin; $s_{\mathrm{exp}}$ the standing the Projector prices for the phase, by the Projector's own
rule and source (`_priced_standing`; ruled on the Stage 1 plan, 27 September 2026: one source): 0 for a walk (the
schema names a movement target), the bound duration through the body's `duration_to_steps` for an action whose
schema names a duration binding (`wait_at`: PT60S → 30 ticks, PT2S → 1 tick), otherwise
`task_model.get_cost(action)` (no costs in kitting), and failing that the body's `default_action_cost`, 1 tick
(`pick_up`, `place`). A stand in a `move_to` phase is charged against $s_{\mathrm{exp}} = 0$. $D$ is non-decreasing within a
phase (e and s only grow for a static target). Time enters here only, never the belief's likelihood.

TAIL (E5). $S_k = S(v D_k)$ with $S(x) = \ln(1 + e^{-\beta x}) / \ln 2$ for $x > 0$ and $S = 1$ for $x \le 0$
(`tail_probability`): the tail of the belief's own likelihood shape read as a density on $x \ge 0$,
$p(x) = \beta L(x) / (2\ln 2)$. A modelling assumption, stated as one; its empirical adequacy is open. β is the
movement likelihood's β, not retuned (its second meaning). At $v = 20$ cm/tick and β = 0.01 /cm: $S < 0.05$ from
$vD = 334.5$ cm (17 ticks of standing in a walk; 167 cm walked straight away from the target), $S < 0.01$ from
496.8 cm (25 ticks).

MEMBERSHIP (E4, E6; ruled by Hadi, 27 September 2026, the precise form, to be recorded in the entry at 1.5). A
live hypothesis is a MEMBER of the test on a tick iff it has a derived phase this tick (an expected action) and
that phase holds an observation: walked path since its origin, or standing beyond $s_{\mathrm{exp}}$. A stationary tick
within the priced duration is not an observation; an observation whose D is not surprising is still one. A
non-member contributes no $S_k$ (absent from `tails`); a hypothesis with no expected action (undecomposable) is
never a member.

FINDING. UNRESOLVED iff there is no member; UNEXPLAINED iff every member has $S_k < \alpha$
(intersection-union); ADEQUATE otherwise. No memory beyond each live hypothesis's current phase (E7): an
unexplained finding clears when a member reaches $S_k \ge \alpha$, or when a phase advance or an episode boundary
empties the membership. α is the run option `test_level`, default 0.05, never chosen from a scenario; it is not
a meta-planner threshold. LIFECYCLE: EXHAUSTED iff H is empty, and then no finding (R4).

What nothing does with it yet: the meta-planner reads `confidence` and `most_likely` only; the finding is for
Stage 1's measurement (session 1.4) and for G. The `[IR]` log line carries `lifecycle=`, `finding=` (absent when
exhausted) and `tails=[key=S …]` over the members, to four decimals.

## 2. Parameters

Two constants in `shared/likelihood_functions.py`, each with a physical meaning, read through the module; the
rest are the body's or the run's, passed to the constructor. `shared/` holds no default for any of them.

| parameter | value (Mesa) | source | meaning |
|---|---|---|---|
| β | 0.01 /cm | body, `mesa_configs.yaml` `simulation.beta` | Detour tolerance: L at an excess of 1/β = 100 cm is 2/(1+e) ≈ 0.54. Since T-D E5 also the scale of the adequacy test's reference distribution. A physical tolerance per embodiment, not per layout (T-A1). |
| v (`speed`) | 20 cm/tick | body, `mesa_configs.yaml` `simulation.step_size` (the Projector's `assumed_speed`) | converts the excess to ticks in D |
| `duration_to_steps` | seconds / 2.0, at least 1 | body, `_parse_duration_to_steps` over `simulation.seconds_per_step` (the Projector's) | a duration binding in ticks, for s_exp |
| `default_action_cost` | 1 tick | body, `RobotAgent` (the Projector's) | s_exp of `pick_up` and `place` (TODO-113: a schema fact later) |
| α (`alpha`) | 0.05 | run option `test_level` (`configs/experiment.yaml`, `--test_level`) | the adequacy test's level per derived phase; reported at 0.01, 0.05 and 0.1 |
| `DETECTION_HIT_RATE` | 1.0 | `likelihood_functions.py` | P(signal \| the action completed). Mesa reports every completion. |
| `DETECTION_FALSE_ALARM_RATE` | 10⁻³ | `likelihood_functions.py` | P(signal \| not completed). Mesa has none; non-zero only so a refuted hypothesis keeps a recoverable base. Set both rates from a real detector's measured rates. |

β was chosen jointly with the removed u (I4: `analysis/i4_evidence_model/`, closed). R1 removed u and kept β;
nothing was re-swept, and β is not retuned for adequacy (the I4 rule stands).

LOAD-BEARING, NOT PARAMETERS:
- θ is NOT a recognizer parameter. The recognizer emits a distribution and gates nothing. The gate is the
  meta-planner's: `DEFAULT_THETA = 0.75` in `shared/meta_planner.py`, applied only in
  `MetaPlanner._clears_gate`. A `CONFIDENCE_THRESHOLD` sat in `recognizer.py` until September 2026 with no
  reader; it is gone (§8).
- `BELIEF_FLOOR` = 10⁻³ (`recognizer.py`): applied to the output only. The evidence is normalised but never
  floored.
- `PROXIMITY_THRESHOLD` = 30 cm (`mesa_sim/world_state_builder.py`): decides when `at(agent, x)` holds, hence
  every phase advance, every fold, every origin and so every derived phase of the adequacy test.
- The path cost: straight-line, exact only because Mesa agents walk straight through obstacles.
- The domain's decompositions: how a selected method cuts a task into phases sets when a rival's excess is
  folded and what the adequacy test's unit is. `deliver_with_return` has six actions to `deliver_default`'s four.
- The context weights (`_context_weight`, output only): TEMPERATURE_BOOST 3.0 on `ac_activation` at room
  temperature ≥ 26.0, FATIGUE_BOOST 2.5 on `coffee_break` after a shift of ≥ 500 steps, on literal task names
  (TODO-66). Inert in every run: Mesa builds `ContextKnowledge.default()` (21.0 °C, shift from step 0) and no
  run reaches 500 steps.

## 3. The guarantee statement (β = 0.01 /cm, θ = 0.75, T-D Stage 1)

"Guarantee" means: holds in every measured condition and follows from the model, not from a scenario. The
conditions are the `analysis/tb1a_destination/` set at the T-D Stage 1 regeneration (the five regression
fixtures and the three evaluation fixtures × assignment prior off/on, `single_task`, stop off,
PYTHONHASHSEED=0; logs local, md5s in its README). Where a figure moved with R1 the value before the build (the
T-L stage 3 logs) is given as old → new. Ticks are `[IR] step=` values. A reveal is the first tick the task the
human is executing is `most_likely` with confidence ≥ θ; the human's task is read from the record's
transitions, which land 2 ticks after the world fact the recognizer's boundary reads (all 48 runs). The
adequacy finding's figures (false-unexplained, missed findings, detection delay) are session 1.4's
measurement, not stated here.

| fixture | task (human, in order) | reveal prior-on | reveal prior-off | grasp / done |
|---|---|---|---|---|
| scenario_s01_01 | item_3 | 20 → 9 | 37 | grasp 41 |
|  | item_2 | 94 → 78 | 108 → 114 | grasp 110 |
| scenario_s02_01 | item_2 | 24 → 23 | 29 → 35 | grasp 31 |
|  | coffee_break | 122 → none | 122 → none | done 155 |
|  | item_5 | 200 → 160 | 243 → 242 | grasp 247 |
|  | ac_activation(ac_switch_0) | 336 → 309 | 338 → 328 | done 364 |
| scenario_s03_01 | item_3 | 11 → 5 | 20 → 30 | grasp 22 |
|  | item_2 | 71 → 54 | 86 → 94 | grasp 88 |
| scenario_s01_06 | item_3 | 23 → 18 | 27 → 26 | grasp 39 |
|  | item_7 | 86 → 74 | 87 → 84 | grasp 97 |
| scenario_s04_01 | item_3 | 30 → 19 | 30 → 19 | grasp 60 |
|  | coffee_break | 152 → none | 152 → none | done 185 |
|  | ac_activation(ac_switch_1) | 203 → none | 203 → none | done 207 |
|  | ac_activation(ac_switch_2) | 216 → 214 | 217 | done 227 |
|  | item_6 | 250 → 243 | 261 → 260 | grasp 268 |
| scenario_s03_06 | item_3 | 11 → 6 | 20 → 30 | grasp 22 |
|  | item_2 | 74 → 69 | 86 → 94 | grasp 88 |
|  | coffee_break | 134 → 121 | 137 → 135 | done 178 |
| scenario_s05_01 / _02 | coffee_break | 23 → none | 23 → none | done 56 |
|  | item_5 | 59 → 60 | 60 → 71 | grasp 62 |
|  | ac_activation(ac_switch_0) | 118 → 94 | 120 / 118 → 104 | done 143 |

### 3.1 Prior-on (the observed agent's assignment is known)

The recognizer GUARANTEES:
- **The belief is over the assigned and foreseeable tasks only.** Everything else is pinned at 10⁻³ and never
  scored.
- **At a boundary with one live task left, that task is at θ on the boundary tick**, by normalisation (R1):
  scenario_s01_01 item_2 at 78, scenario_s03_01 item_2 at 54, scenario_s01_06 item_7 at 74, scenario_s05_01 /
  _02 ac_switch_0 at 94. Its confidence is $1 - 0.001\cdot|pinned|$ (0.996) on no evidence.
- **The first task, and a task among several live ones, is revealed on the walk**: every walk reveal precedes
  the grasp (the table). With R1 an even prior over two or three keys needs only the rivals refuted, so first
  reveals moved earlier (scenario_s01_01 item_3 20 → 9, scenario_s03_01 11 → 5).
- **Not every foreseeable task is revealed**: `coffee_break` is never at θ in scenario_s02_01, scenario_s04_01
  or scenario_s05_01 / _02 (it was, at its arrival fold, before R1: the fold was worth 1/u against `unknown`,
  and at L = 1 it is worth nothing against rivals no longer refuted), nor is ac_switch_1 in scenario_s04_01.
- **After every admissible task is complete**, the recognizer is EXHAUSTED (scenario_s01_01 from 141,
  scenario_s02_01 from 362, scenario_s03_01 from 121, scenario_s01_06 from 120, scenario_s03_06 from 176,
  scenario_s05_01 / _02 from 141), unless a foreseeable task
  never performed stays live: in scenario_s04_01 `ac_activation(ac_switch_0)` is then the lone live task and
  at θ from 327, with the human idle — a crossing of a task the human is not executing.
- **A completed task is at the floor for the rest of the run**, whoever completed it.

### 3.2 Prior-off (no assignment known)

The same model over a larger live set: every task of every object, the robot's own undelivered items
included. Therefore:
- **Reveals are later, and several now follow the grasp**: scenario_s01_01 item_2 at 114 (grasp 110),
  scenario_s02_01 item_2 at 35 (31), scenario_s03_01 / _06 item_3 at 30 (22) and item_2 at 94 (88),
  scenario_s05_01 / _02 item_5 at 71 (62). Before R1 these were the arrival-fold reveals (§1.9 of the earlier
  text: an arrival counted two observations against `unknown`); now an arrival folds L = 1 and adds nothing, so
  the true task is separated only when the rivals' carry phases are refuted.
- **After the human's last task, the robot's own remaining item is at θ** once it is the lone live task, with
  the human idle: scenario_s01_01 item_4 at 141, scenario_s03_01 item_7 at 145, scenario_s01_06 item_6 at 160,
  scenario_s03_06 item_7 at 176, scenario_s05_01 item_3 at 171, scenario_s05_02 item_2 at 172, scenario_s04_01
  `ac_activation(ac_switch_0)` at 379. Before R1, `unknown` held half the mass there and nothing crossed. The
  meta-planner admits these (R1's admission shift, measured in 1.4, not corrected): see §5.
- **An idle human sits at the uniform prior over what is still live** until a pin or exhaustion; the robot's
  deliveries shrink the set without re-initialising it.
- **Dilution**: more live rivals mean less confidence from the same evidence and later reveals (item_5 in
  scenario_s02_01: 160 prior-on, 242 prior-off).

### 3.3 What every figure above is conditional on

- **Straight lines.** Mesa agents walk straight through obstacles and C is Euclidean, so the true
  hypothesis's excess is exactly 0. In a real cell with obstacles, every detour the path cost does not model
  is charged to the true hypothesis, in the belief and in the adequacy test alike. Inject a path cost before
  reading any figure here as a guarantee there.
- **`PROXIMITY_THRESHOLD` = 30 cm.** Every phase advance is taken 30 cm from the target.
- **Kitting's decompositions and guards** (`deliver_with_return`'s phases refute the rivals at the grasp).
- **The layout's decoy geometry**: targets on one bearing tie in excess for the whole walk and are separated
  only when one is refuted; without the grade there is no distance term (TODO-38).
- **The live set's size**: it sets the prior, the dilution and, with R1, whether a lone task is at θ by
  normalisation.
- **β**: it sets every reveal tick and the scale of the adequacy test.
- **The human's script.** A human who hesitates, back-tracks or wanders mid-task is charged as a rival would
  be. A stand adds no evidence to the belief (I4c); it is charged in the adequacy test against the phase's
  priced standing (§1.10). Every task in the script is one the domain describes (well typed, F47b).

### 3.4 What the meta-planner may assume, and must not

MAY assume, either setting: a completed task never returns. After the human's own completion the belief is
the uniform prior over what is live, and `most_likely` carries no information until the human moves unless one
task is live. When nothing is live the recognizer says so (EXHAUSTED, `most_likely` `None`, confidence 0).

MUST NOT assume, either setting:
- that a task at θ is the task being executed now: a lone live task is at θ by normalisation, whatever the
  human does (§3.1, §3.2);
- that confidence is comparable across live-set sizes (0.75 is a different bar over 1, 2 and 8 keys);
- that confidence says anything absolute: the belief is relative over the robot's models; whether the best of
  them is wrong is the adequacy finding (§1.10), which the meta-planner does not read in this cycle;
- that a robot completion is a human boundary;
- that confidence is monotone within a task;
- that anything in the belief refers to a previous episode.

## 4. Characterised limitations, and the open design item

Properties of the chosen model, not defects.

**(a) Confirmation is by refutation.** The excess discriminates by penalising wrong hypotheses, not by rewarding
right ones: the correct hypothesis sits at zero excess however far it walks, and with no reference hypothesis
it gains share only as its rivals lose it. A lone live task needs nothing (§1.9). The grade, which made a
walk's odds against `unknown` grow with the path covered, went with u (R1).

**(b) Accumulation is decomposition sensitive.** How a selected method cuts a walk into phases sets when a
rival's excess is folded; the prior-off reveals after the grasp (§3.2) are the rivals' carry phases doing the
refuting. A no-graded-signal phase (`pick_up`, `place`, `wait_at`) folds L = 1 and is evidence for nothing in
the belief; it is assessed in the adequacy test against its priced standing.

**(c) The adequacy test's limitations, recorded in the entry and not built**: sub-threshold waste is not
summed across phases; a regress at the proximity threshold restarts a hypothesis's test; the false-unexplained
count per run grows with the number of phases of the true hypothesis. Under the membership ruling a finding can
be unexplained while the true hypothesis is a non-member (standing within its priced duration) and only a
refuted rival is a member (scenario_s01_01 prior-on, steps 76–77, the human placing item_3); measured in 1.4.

Also stated, lower in consequence:
- An undecomposable hypothesis scores the perfect fit in the belief and is never a member of the adequacy
  test; no case occurs in the maintained baselines (§1.10).
- The boundary infers authorship from the phase. A domain where another agent satisfies a terminal condition
  while the observed agent stands in its terminal phase would attribute wrongly.
- Evidence accumulated under one method is reused when the guard re-selects another. Dormant in kitting (every
  within-episode flip is the observed agent's own grasp or release, TODO-55 (d)).

## 5. The interface to the meta-planner

`update()` returns a `BeliefState` (`shared/io_contracts.md` §1.2; contract §2.1): `timestamp`, `agent_id`,
`distribution` (every hypothesis key, pinned ones at 10⁻³), `most_likely` (the argmax over H, `None` when
exhausted), `confidence` (its value, 0.0 when exhausted), `finding`, `lifecycle` and `tails`. The meta-planner
reads only `most_likely` and `confidence` (io_contracts §2.2); it does not read the finding, the lifecycle or
the tails in this cycle (R5: what it does with them is G and X, open):
- `_clears_gate(belief)`, the one place θ is applied, tests `confidence ≥ θ`, θ = `DEFAULT_THETA` = 0.75,
  unchanged. Its input changed meaning with R1: the leader's share over H. The gate ruling (September 2026)
  stands; its reason, the crossing odds against `unknown`, is superseded by R1, and its justification is
  re-derived from Stage 1's admission measurement (G). Measured at the regeneration: no admission at tick 0 in
  any of the 48 baseline logs (no fixture starts with one live task); the admission shift occurs at the boundary
  that leaves one task live, and prior-off it admits the robot's own remaining item with the human idle
  (§3.2), which delays the robot (scenario_s01_01 prior-off completes at 202 instead of 169; scenario_s03_01
  prior-off does not complete in 300 steps).
- `evaluate_triggers()` fires `recognition_changed` (D2) when a decision record `_projected_hypothesis`
  exists and `most_likely` is no longer it: a replacement, the human's boundary, or no hypothesis live. It also
  fires when no record exists and the belief clears the gate.
- `update_human_projection()` admits a projection only when the gate clears. It resolves the key through
  `recognizer.get_hypothesis()` (the same live instance, held by reference) to project the human's task, and
  records the hypothesis it projected. Its refusal reasons are `none(below_theta)`, `none(no_human)` and
  `none(unprojectable)` (the projector could not resolve the task; `none(unresolved)` before the Stage 1 build).
  When the recognizer is exhausted it refuses as `none(below_theta)`.

Confidence is a gate, never a magnitude in any cost; `distribution` is logged and not read. (See TODO-97 (24 Sept 2026): belief-aware planning, one realization against the hypotheses covering 1 − ε of the mass, recorded for after the T-D recognizer pass, not decided.) A
re-crossing of the recorded hypothesis fires nothing; a change of hypothesis or its end fires
(`design_decisions.md`, the D2 entry).

## 6. Open items

| item | where | one line |
|---|---|---|
| Stage 1 verification | TODO-101; session 1.4 | the R6 invariant, recognizer outputs per ground-truth case against oracle IR, admissions before and after, false-unexplained / missed findings / detection delay at every α |
| what the meta-planner does with belief, finding and lifecycle | G, X (T-D) | R5; TODO-97 on its own gate |
| the gate's justification after R1 | G | the gate stands; its reason is re-derived from Stage 1's admissions (§5) |
| s_exp of `pick_up` / `place` as a schema fact | TODO-113 | one source for the Projector and the recognizer, when the Projector is in scope |
| collinear decoys | TODO-38 | targets on one bearing tie until one is refuted; no distance term since the grade went |
| `deliver_with_return`'s guard | TODO-55 (e) | a stray item vs an assigned one; a domain question |
| β in centimetres | TODO-58 | layout-scale dependence |
| declared unmodelled behaviour | TODO-80 | a human stay no hypothesis describes, stated by the scenario's purpose (label C) |
| the context / knowledge-representation pass | TODO-66 | `_context_weight` names two tasks and carries four constants; output only, inert |
| the two analytical tools | TODO-62, TODO-63 | radius of maximum probability (diagnostic); rationality measure |
| hash-seed dependence | TODO-42 | resolved for the recognizer (sorted keys); runs still need `PYTHONHASHSEED=0` |

Closed since the I5 hand-back: TODO-48 / 54 / 68 (D2); TODO-64 / 65 (the gate ruling, §5); TODO-72 (io_contracts
§1.3 / §2.1 aligned with this document); TODO-52 (R1 / T10) and TODO-67 (T7), both meta-planner side; TODO-57's
script-part-3 question, made moot by F47b; TODO-95's recognition level and TODO-59's deferred stationarity
channel (closed by decision, T-D R and E: time enters adequacy only); TODO-61 (b) (reason superseded by R1).

## 7. The paper-facing divergence

The HCM paper writes P(task | O) with O a sequence of ACTIONS. The recognizer never observes an action: it
observes a microaction and a position, and the action is LATENT. P(o | τ) = P(o | a_φ(τ)) is a
marginalisation over that latent action, collapsed because the phase is derived deterministically from the
world (design_decisions.md, the I3 entry). The paper is a position paper, outdated relative to this design,
and not a specification. It will need rewriting on this point, and also on:
- the episode-local semantics (I4c);
- the belief as relative over the robot's models, with the adequacy finding as a separate output (T-D R and E);
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
| the `unknown` hypothesis, u (`UNKNOWN_LIKELIHOOD`), the odds accounting against it and its invariant | one number carried four meanings (evidence against every hypothesis, the prior share, the mass left at exhaustion, nothing for a stand); the relative test could not say "the best of my models is wrong" | T-D R and E (R1, R6) |
| the grade (`covered_fraction`, `graded_unknown_likelihood`) | it graded evidence against `unknown`, which is gone | T-D R and E (R1) |
| a reserved "duration" progress evaluator | time enters the adequacy test, never the belief's likelihood | T-D R and E (E3) |

Also gone and not to be re-added:
- any persistence of belief across an episode boundary (I4c; I4b's "reset the geometry, keep the belief" was
  measured and found wrong);
- any scoring of an empty stretch (I4c);
- a residual hypothesis in the belief, or any reference likelihood the live hypotheses are scored against (T-D R1);
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
| Sept 10 (assignment pool) | a 10× prior weight on assigned tasks | the support restriction (§1.1) | knowledge of the assigned tasks is a fact about the support, not a magnitude |
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

| Sept 27, T-D R and E Stage 1 | the `unknown` hypothesis, u, the grade and the odds accounting; one number carrying four meanings | the belief normalised over the live set H only (§1.5); beside it the adequacy finding, per live hypothesis per derived phase, D and its tail S at the test level α (§1.10), and the lifecycle state (EXHAUSTED when H is empty) | the relative test could not express "the best of my models is wrong"; `unknown` at 0.995 was normalisation, not evidence. Every figure in §3 is from this HEAD, with the pre-build value where it moved. |

Superseded figures (the I5 matrix, any s40 figure before F47b, and the graded-evidence figures before the T-D
Stage 1 build) are not carried here. Where they are cited
elsewhere they describe the fixture of their time.
