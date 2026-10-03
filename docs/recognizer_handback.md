# The intention recognizer — current description
REWRITTEN TO HEAD at the T-D Stage 1 build (27 September 2026; design_decisions.md, "T-D R and E"): the `unknown`
hypothesis, u, the grade and the odds accounting are gone (R1); the recognizer reports an adequacy finding and a
lifecycle state beside the belief (R2 to R4, E1 to E7). The earlier text is in git history (before commit 367a3a7).
REWRITTEN TO HEAD at the cycle 1.5b build (27 September 2026; design_decisions.md, "T-D R and E", "1.5 rulings"):
E8 (the advance tick), E9 (s_exp by the Projector's attribution), E10 (the belief's evidence per phase is L(v·D))
and G1 (the guard on admission, the meta-planner's side, §5). UPDATED at 1.5c (27 September 2026): E6's second
amendment (a stationary tick within the priced standing of any phase with s_exp > 0 is an observation) and the
boundary tick (no member on it), §1.10. Figures in §3 are from the 1.5c regeneration, with earlier values where they
moved; acceptance in `analysis/td_stage1b/REPORT.md` (sections 1.5b and 1.5c).
UPDATED at T-G stage 1, step 3 (1 October 2026; bd4bddc): liveness by applicability (T-G A4), §1.1; the perfect-fit
score of an undecomposable hypothesis is removed (the superseding notes in §1.4, §1.10 and §4).

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

SUPERSEDED IN PART (T-D L4, ruled 27 September 2026, built in L-build): H at tick t is the support minus the hypotheses
whose terminal fact holds AT t, read from the world on every tick; "completed by t" (once, for the rest of the run)
no longer. A hypothesis whose terminal fact stops holding re-enters H with the prior base and the current position as
origin, the others renormalised (R6): a moved item makes its delivery live again, `coffee_break` is live again when
`waited` clears. design_decisions.md, "T-D L: the belief lifecycle", L4.
AMENDED (Hadi, on the L-records report, 27 September 2026): re-entry takes exactly 1/|H| (H with the returning hypothesis; k
returning on one tick take 1/|H| each), the incumbents share the rest in this tick's proportions; origin the current
position, entry latency 0 (a first observation), the derived action the world's; a re-entry on a boundary tick is
governed by the boundary. Logged `[IR-reentry]`. BUILT IN L-BUILD (28 September 2026; 2c54c4a, 493c095, 5129d90, 3d65ca6).
AMENDED (T-G A4, built in T-G stage 1, step 3, 1 October 2026; bd4bddc): a second condition of H, liveness by
applicability. A hypothesis whose task has no applicable method in this world (`decompose` raises `DecompositionError`;
the one definition is `AdaptivePlanner.is_applicable`) is not live: it leaves H, is pinned at `BELIEF_FLOOR` on output and
is never a member, logged `[IR-inapplicable] step=N <key> leaves the live set: no applicable method` (on the first tick
`does not enter the live set`). When it is applicable again: retired if its terminal fact holds (L4), else it re-enters
at 1/|H| through L4's returning path, logged `[IR-reentry] step=N <key> live again: applicable`. A retired hypothesis
that becomes inapplicable stays retired. No kitting hypothesis is ever undecomposable: the maintained outputs are
unchanged.
AMENDED (T-K part 1, AM1, Hadi, 3 October 2026; not built): the re-entry share (1/|H|, the incumbents sharing the rest)
is a share of the evidence, not of the belief; the belief is prior × evidence, normalised. The rule's content does not
change. design_decisions.md, "T-K: context knowledge in the recognizer's belief", R2, AM1.

### 1.2 Prior

Uniform over the live set: $\pi(k) = 1 / |H|$, at construction and again at every episode boundary (§1.6),
recomputed over what is still live. Nothing else is stored to restart from. A lone live hypothesis therefore
reads 1.0 on no evidence, and two rivals start at 0.5 (R1: expected, measured in Stage 1, not corrected). The
robot observes the human once before the clock starts (`RobotAgent.observe_initial`), so step 0 is already a
scored step.
RULED, NOT BUILT (T-K part 1, Hadi, 2 and 3 October 2026): the uniform start above becomes the EVIDENCE's (AM1); the
belief is normalise(prior × evidence), the prior computed at each run from the present context facts, the strengths of
the live foreseeable tasks (each divided among its live hypotheses) and the equal division of work as a whole (R2 to
R4, AM2, AM3). With context knowledge off the prior is equal over the live hypotheses, as here.
design_decisions.md, "T-K: context knowledge in the recognizer's belief".

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

THE PHASE (T-D E10, 1.5 rulings). Every live hypothesis's derived phase is scored by one statistic, its projected
completion delay in ticks, measured from the phase's origin $o$:

$$
D = e / v + (s - s_{\mathrm{exp}}), \qquad e = w + C(p, g) - C(o, g) \quad \text{(the path wasted under the hypothesis; } \texttt{excess\_path}\text{)}
$$

$w$ the distance walked since $o$ (per-agent odometer: the sum of straight-line steps between observed positions),
$p$ the current position, $g$ the target's current position (`shared/target_resolution.py`; a carried object
resolves through its holder); $e = 0$ for an action with no `progress_evaluator` (`pick_up`, `place`, `wait_at`) or
no resolvable target. $s$ the ticks the agent stood since $o$ (per-agent standing clock), $s_{\mathrm{exp}}$ the
Projector's priced stationary ticks within the phase (§1.10, E9), $v$ the body's speed. The belief's evidence for
the phase is the logistic of $v \cdot D$, clipped at 1:

$$
L = \frac{2}{1 + \exp(\beta \cdot v D)} \text{ for } vD > 0, \qquad L = 1 \text{ for } vD \le 0
\qquad L(1/\beta)=\frac{2}{1+e}\approx 0.54,\quad L\to 0 \text{ as } vD\text{ grows}
$$

(`likelihood_functions.delay_likelihood`). For a walk with no standing beyond its $s_{\mathrm{exp}}$, $vD = e$ and
$L = L(e)$: walking evidence is the excess-path likelihood, unchanged (asserted on a walking-only span in
`tests/test_td15_build.py`; the maintained baselines' walking-only `[IR-dist]` lines are byte-identical). Standing
beyond $s_{\mathrm{exp}}$ is charged $v$ per tick, as excess path is. Standing within it is no charge (I4c
narrowed). The clip: a moving target's negative excess ($e < 0$, which gave $L \in (1, 2)$ before 1.5b) reads 1, the
moving target being outside the model; in the maintained baselines, prior off, $e < 0$ occurs only at rounding
($|e| \le 7 \cdot 10^{-13}$ cm; `analysis/td_stage1b/clip_ticks.txt`). $C$ is the path cost, straight-line by default
and injectable (`IntentionRecognizer(path_cost=…)`). One phase is ONE observation however many ticks it spans: its
value is recomputed from the origin every tick and replaces the previous tick's. The excess $e$ is computed once
(`likelihood_functions.excess_path`, registered in `EXCESS_MEASURES` under the evaluator's name) and $vD$ once
(`_delay_length`), read by both the belief (L) and the adequacy test (S, §1.10).

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

NO DERIVED PHASE. A hypothesis the planner cannot decompose in this world (`DecompositionError`, logged once) has
no phase and scores the perfect-fit value L = 1: nothing to charge. It is therefore not refuted; it is treated as
fitting (and it is never a member of the adequacy test).
SUPERSEDED (T-G A4, built in T-G stage 1, step 3, 1 October 2026; bd4bddc): a hypothesis the planner cannot decompose
is not applicable and is not live: it leaves H and is pinned at the floor (§1.1); no perfect-fit score is given.

AN EMPTY PHASE. A phase with nothing walked and no standing beyond its $s_{\mathrm{exp}}$ (the tick a hypothesis
enters an action, the ticks after a boundary before the agent moves) has $vD \le 0$ and pays L = 1: no charge,
the belief carries forward. Before 1.5b this was "no factor" (I4c: an empty stretch is not an observation);
the value is the same. On such a tick the hypothesis pays nothing while a rival with an open, charged phase
pays its L (accepted, I4d point 4). Standing now enters the belief (E10, superseding E3's "time enters adequacy
only"), through D and only beyond the priced standing.

### 1.5 Evidence: normalised likelihood over H

Each live hypothesis's evidence is the product of its OWN observations in the current episode, normalised over
H. For every live $k$ and tick $t$:

$$
E_t(k) \propto \pi(k)
\cdot \prod_{\phi \in \mathrm{phases\ of\ } k \mathrm{\ closed\ by\ } t} L(v D_k(\phi))
\cdot \prod_{e \in \mathrm{events\ of\ } k} c_k(e)
\cdot L(v D_k(t)),
\qquad \sum_{k \in H} E_t(k) = 1
$$

- The open phase's current value L(v·D) multiplies on top for this tick only.
- A phase change FOLDS the closing phase's final value L(v·D) into the base once (1 if its delay was not
  positive) and moves the origin to the agent's position, odometer and standing-clock readings. The final value
  is computed with the tick of the change included (the grasp tick's standing belongs to the closing `pick_up`,
  s = 2 = s_exp). A fold moves a factor from the open term to the base without changing it. A regress folds too.
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

SUPERSEDED (T-D L1 and L4, ruled 27 September 2026, built in L-build). BOUNDARY (L1): the episode boundary fires when
the observed agent completes an action that is terminal in the task model (`place`, `wait_at`), read from the
completion channel, whatever its binding; it no longer requires a retirement. PIN: unchanged as the world's terminal
fact of a live hypothesis; a boundary at a pin is the special case where the terminal action also produces that fact.
A task whose execution ends without its terminal fact (the misdelivery, scenario_s09_08 at 75) stays live and starts
the next episode at the prior. RETIREMENT (L4): "for the rest of the run" no longer; a hypothesis is retired while its
terminal fact holds and re-enters when it stops holding (§1.1). What a boundary does is unchanged (L5).
design_decisions.md, "T-D L: the belief lifecycle", L1, L4, L5.
AMENDED (Hadi, on the L-records report, 27 September 2026): "read from the completion channel" no longer: the boundary fires
when a terminal action's own completion condition becomes true for the observed agent — its preconditions held for
that agent on the previous tick and a grounding of its completion condition under that binding holds now and did not
then (`place`: `holding(agent, x)` then `obj_at(x, c)`; `wait_at`: `at(agent, e)` then `waited(agent, e)`). No
microaction is read. A terminal `place` inside a decomposition (the return of `deliver_with_return`, scenario_s09_07 at
33) is a boundary. The boundary tick is flagged on the belief (`episode_boundary`, L5 B). BUILT IN L-BUILD (28 September 2026; 2c54c4a, 493c095, 5129d90, 3d65ca6);
`[IR-boundary]` names the action (`completed place(item_1,shelf_1):`).
AMENDED (T-K part 1, AM1, Hadi, 3 October 2026; not built): "every live base becomes the uniform prior" and "this tick
already reports the prior" describe the evidence: at a boundary the evidence restarts equal over the live hypotheses,
and the belief is prior × evidence, normalised (R2). The rule's content does not change. design_decisions.md, "T-K: context knowledge in the recognizer's belief", R2, AM1.

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

Beside the belief, `BeliefState` carries the adequacy finding, the lifecycle state, the members' tail
probabilities and every live hypothesis's hypothesis adequacy (§1.10). Belief and finding are independent outputs
(R3); since E10 they read one statistic, D, through two functions (L and S).

### 1.8 `update()` in pseudocode

Close enough to `IntentionRecognizer.update()` to check line by line; λ is `_progress_likelihood`, and ≡ is
identity of name and bindings.

SUPERSEDED IN PART (T-D L1 and L4, ruled 27 September 2026, built in L-build): the pseudocode below is the recognizer
before L-build. Under L4 the `k completed` skip and `completed.add(k)` become a per-tick test of the terminal fact (a
retired key whose fact no longer holds re-enters H with the prior base and the current position as origin); under L1
`boundary` is set by the observed agent's completion of a terminal action read from the completion channel, not
inside the retirement branch by `expected[k] == A[-1]`. design_decisions.md, "T-D L: the belief lifecycle", L1, L4.
AMENDED (Hadi, on the L-records report, 27 September 2026): `boundary` is set from the world's completion conditions for the
observed agent (above, §1.6), not from the completion channel.

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
    if k never observed:  # enters its action from no completion: an empty phase
        expected[k], origin[k], origin_odo[k], origin_still[k] = a, pos, odo, still
        entry_latency[k] = 0
        U[k] = base[k]
        continue

    a_prev = expected[k]
    if a_prev is not None and mu in vocabulary(a_prev):  # event
        base[k] *= HIT if a_prev.completion in world.predicates else FALSE_ALARM

    if a_prev != a:  # phase advance or regress
        base[k] *= lambda_(k, a_prev)  # fold: the closing phase's L(v·D), this tick included
        expected[k], origin[k], origin_odo[k], origin_still[k] = a, pos, odo, still
        completed = a_prev is not None and a_prev.completion in world.predicates
        entry_latency[k] = ACTION_LATENCY if completed else 0  # E9
        if completed:
            advanced.add(k)  # E8
    U[k] = base[k] * lambda_(k, a)  # the open phase's L(v·D)

Z = sum(U.values())                               # over H only
base = {k: v / Z for k, v in base.items()}
E = {k: v / Z for k, v in U.items()}

if boundary:  # episode ends
    base = uniform over live keys
    E = base.copy()
    for k in live_keys:
        origin[k], origin_odo[k], origin_still[k] = pos, odo, still
        entry_latency[k] = ACTION_LATENCY + OBSERVED_TASK_LATENCY  # E9
    advanced = {}  # E8: no observation on the boundary tick

P = output(E)  # §1.7
most_likely, confidence = (argmax over H of P, its value) if E else (None, 0.0)
finding, lifecycle, tails, hypothesis_adequacy = adequacy(pos, odo, still, advanced)  # §1.10
return BeliefState(P, most_likely, confidence, finding, lifecycle, tails, hypothesis_adequacy)
```

The phase term used in the pseudocode (`_phase_likelihood`) is, from $k$'s origin $o$, walked $w$ and standing $s$:

$$
\lambda(k, a)=
\begin{cases}
1, & \text{if } a = \mathrm{None} \text{ (no derived phase)},\\
\mathrm{delay\_likelihood}(e + v\,(s - s_{\mathrm{exp}}(k, a)),\ \beta), & \text{otherwise, } e = w + C(p,g) - C(o,g) \text{ (0 without evaluator or target, or if } w \le 0\text{)},
\end{cases}
$$

with $s_{\mathrm{exp}}(k, a)$ = entry_latency[k] + the action's own stationary duration (§1.10). The excess is
memoised per tick by (evaluator, origin, walked, target), and the completion likelihood by the grounded
predicate. Two items on one shelf therefore share one excess from the same origin.

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
- Standing (E10): one tick beyond $s_{\mathrm{exp}}$ is worth $L(v) = L(20\,\mathrm{cm}) = 0.90$. A hypothesis within its
  priced standing (coffee_break's `wait_at`, 31 ticks after its walk) against a walk rival at an even tie clears θ
  when the rival's $L \le 1/3$: $v\,(s - s_{\mathrm{exp}}) \ge \ln 5 / \beta = 160.9$ cm, 9 standing ticks
  (scenario_s05_01 / _02 prior on: arrival 23, crossing 32).
- There is no ceiling below 1 (the ceiling $1/(1 + u^n)$ went with u).

### 1.10 The adequacy finding (T-D E1 to E9, G1)

The recognizer's second output, computed after the belief, from scratch every tick (`_adequacy`).

UNIT (E1). Each live hypothesis's DERIVED PHASE: from its existing origin to its phase advance. No window, no
episode constant. A regress at the proximity threshold is a phase change and restarts that hypothesis's test
(limitation (b) of the entry).

STATISTIC (E2, E9). Per live hypothesis $k$ in its derived phase, the projected completion delay of §1.4, in ticks:

$$
D_k = e_k / v + (s_k - s_{\mathrm{exp}})
$$

the same statistic the belief reads (E10). $s_{\mathrm{exp}}$ is the Projector's priced stationary ticks that fall
within the phase's span (E9, `_priced_standing(key, action)`), read from the Projector's own sequence and source:
per action its own segment, then the body's `action_completion_latency`; the latency falls in the phase the
completion opens. So $s_{\mathrm{exp}}$ = the latency priced after the completion that opened the phase
(`_entry_latency`: `action_completion_latency` when the previous expected action's completion predicate holds on
the tick the phase is entered; that plus the observed agent's `observed_task_completion_latency` for every phase a
boundary opens; 0 for the phase a hypothesis is first observed in, and after a regress or a method flip that
completed nothing) + the action's own stationary duration (`_action_duration`: 0 for a walk; the bound duration
through the body's `duration_to_steps` for an action whose schema names a duration binding, `wait_at`: PT60S → 30
ticks, PT2S → 1 tick; otherwise `task_model.get_cost(action)`, no costs in kitting; failing that the body's
`default_action_cost`, 1 tick, `pick_up`, `place`). The derived values in kitting (Mesa: latency 1, the human's
task latency 0):

| phase | s_exp |
|---|---|
| the initial walk (first observed, no completion before it) | 0 |
| `pick_up` / `place` after its walk | 1 + 1 = 2 |
| a walk entered from a completion (the carry after a grasp; the first walk after a boundary) | 1 |
| `wait_at` after its walk | 1 + 30 = 31 |
| a stationary phase first observed (the agent starts there) | its own duration only (1; 30) |

The body stands 3 ticks at a shelf or table (the walk's latency, the action, the action's latency); the recognizer
now charges the same ticks to the same phases as the Projector (`analysis/td_stage1b/g_priced_standing.txt`): the
true hypothesis's D on its walking ticks is exactly 0 on every tick (3891 of 3891 per prior), where under Stage 1
it was 1 on 77.5% (the latency tick charged to the walk). $D$ is non-decreasing within a phase.

TAIL (E5). $S_k = S(v D_k)$ with $S(x) = \ln(1 + e^{-\beta x}) / \ln 2$ for $x > 0$ and $S = 1$ for $x \le 0$
(`tail_probability`): the tail of the belief's own likelihood shape read as a density on $x \ge 0$,
$p(x) = \beta L(x) / (2\ln 2)$. A modelling assumption, stated as one; its empirical adequacy is open. β is the
movement likelihood's β, not retuned (its second meaning). At $v = 20$ cm/tick and β = 0.01 /cm: $S < 0.05$ from
$vD = 334.5$ cm (17 ticks of standing in a walk; 167 cm walked straight away from the target), $S < 0.01$ from
496.8 cm (25 ticks).

MEMBERSHIP (E4, E6 as amended twice, E8; the complete rule recorded in the entry). A live hypothesis is a MEMBER of
the test on a tick iff it has a derived phase this tick (an expected action), the tick is not a boundary tick, and
that phase holds an observation: walked path since its origin; or standing beyond $s_{\mathrm{exp}}$; or a stationary
tick within the priced standing ($s \le s_{\mathrm{exp}}$) in a stationary phase (`pick_up`, `place`, `wait_at`: no
movement target) or in ANY phase with $s_{\mathrm{exp}} > 0$ (E6's second amendment, 1.5c), which is an observation with
$D \le 0$ and $S_k = 1$: a hypothesis whose priced standing has not ended explains the behaviour exactly. The second
amendment covers the latency tick E9 prices to a walk entered from a completion. And (E8) on the tick a hypothesis's
expected action completes (the phase change where the previous expected action's completion predicate holds), that
hypothesis is a member with $S_k = 1$, whatever phase it advances into: the completion is an observation
consistent with it. On a boundary tick no hypothesis is a member, a stationary phase the boundary opens included
(E8's boundary clause applied generally, 1.5c; it supersedes reading 3 of 1.3b). A stationary phase is
derived only once its location is reached (the preceding walk's `at()` holds), so the agent is at the phase's
location. The entry tick of a stationary phase counts as its first stationary tick ($s = 0$): the arrival step
of that tick belongs to the closing walk's stretch, and nothing has been walked since the new origin. A
walk with $s_{\mathrm{exp}} = 0$ (the initial walk at step 0, or one entered by a regress) with nothing walked holds no
observation; the initial walk stays unresolved until walking evidence occurs. At a boundary the derived sequence is
unresolved (b), adequate (b + 1, the latency tick: s = 1 = s_exp, S = 1), adequate (65 of 65 live boundaries in the
maintained baselines); under 1.5b it was unresolved, unresolved, adequate. On the latency tick after a grasp the true
hypothesis's carry walk is a member at S = 1 (under 1.5b it held no observation there and a refuted rival alone made
the finding unexplained: scenario_s02_01 on 248, scenario_s04_01 on 269, scenario_s03_06 on 89). False unexplained
on modelled ticks: 0 at every α, both priors (`analysis/td_stage1b/REPORT.md`, 1.5c). An observation whose D is not
surprising is still one. A non-member contributes no $S_k$ (absent from `tails`); a hypothesis with no expected action
(undecomposable) is never a member.
SUPERSEDED IN PART (T-G A4, built in T-G stage 1, step 3; bd4bddc): an undecomposable hypothesis is not live at all
(§1.1).

FINDING. UNRESOLVED iff there is no member; UNEXPLAINED iff every member has $S_k < \alpha$
(intersection-union); ADEQUATE otherwise. HYPOTHESIS ADEQUACY (G1), per live hypothesis: ADEQUATE (a member with
$S_k \ge \alpha$), INADEQUATE (a member with $S_k < \alpha$), NO_OBSERVATION (not a member); the finding is adequate
exactly when some live hypothesis's is. No memory beyond each live hypothesis's current phase (E7): an
unexplained finding clears when a member reaches $S_k \ge \alpha$, or when a phase advance or an episode boundary
empties the membership. SUPERSEDED IN PART (TB.2b records, 27 September 2026): "a phase advance ... empties the membership"
is wrong under E8: on the tick a hypothesis's expected action completes, the completing hypothesis is a member with
$S_k = 1$ whatever phase it advances into, so an advance never empties the membership on its tick; only a boundary
tick does (no hypothesis is a member on it, 1.5c). The finding is recomputed every tick (E7 as worded in TB.1r). α is the run option `test_level`, default 0.05, never chosen from a scenario; it is not
a meta-planner threshold. LIFECYCLE: EXHAUSTED iff H is empty, and then no finding (R4).

What reads it: the meta-planner reads the leader's hypothesis adequacy at its gate (G1, §5), never α or $S_k$;
the finding itself, the lifecycle and the tails are for evaluation and for the rest of G. The `[IR]` log line
carries `lifecycle=`, `finding=` and `leader_adequacy=` (both absent when exhausted) and `tails=[key=S …]` over the
members, to four decimals; every other hypothesis's adequacy follows from the tails and α.

WARRANT (T-D G, AD1 to AD4, ruled by Hadi, 29 September 2026; built in G-build, 81a9f86). A third independent output
beside the belief and the finding (R3 as amended, AD2), not a kind of adequacy: per live hypothesis, OBSERVATION
WARRANT (none | observation) on `BeliefState`. A hypothesis's current derived phase holds observation warrant when,
for a phase with a movement target (`move_to`), the path-cost gain toward the target since the phase origin is
positive, $C(o, g) - C(p, g) = w - e > 0$ (the quantities of the excess-path statistic above; no new statistic, no
constant); or, for any phase, when the phase was entered by the observed completion of the hypothesis's previous step
in this episode (the completion E8 reads). A phase without a movement target (`pick_up`, `place`, `wait_at`, where
$e = 0$ and $w - e$ would be the path walked) has observation warrant through that entry only. It resets with the
origins, at a boundary and at a phase change. Commitment warrant (the hypothesis is one of the observed human's
assigned tasks) is the gate's knowledge, never computed or printed here. The meta-planner's gate reads observation
warrant, adds commitment warrant and refuses an unwarranted leader (`none(leader_unwarranted)`, after
`none(leader_inadequate)`); it reconstructs no recognizer quantity. The `[IR]` line prints `warrant=none|observation`
per live hypothesis, its exact form settled at G-build's plan step. design_decisions.md, "T-D G: admission".
AS BUILT (G-build, 29 September 2026). `BeliefState.observation_warrant: Dict[str, ObservationWarrant]` (NONE |
OBSERVATION), keys exactly H, empty when exhausted, computed after `_adequacy` by `_observation_warrant(pos, world)`,
which reads neither the belief nor the adequacy. Per live key: NONE with no derived phase; OBSERVATION if the key is in
`_entered_by_completion` (the ENTRY source: set when the phase change's previous expected action has its completion
predicate holding, the completion E8 reads; cleared at a phase change without it, at a first observation or re-entry
and at a pin; emptied by `_begin_episode`, so nothing crosses a boundary and no phase a boundary opens has it); else
NONE for a stationary phase (no movement target, by definition); else NONE for a `move_to` whose target position
`movement_target_position` cannot resolve (a movement target that cannot currently be resolved: no gain computable;
ruled by Hadi at the G-build plan step, occurring on no tick of the 48 maintained logs or the 17 test-bed runs); else
OBSERVATION iff C(o, g) − C(p, g) > 0 (the MOVEMENT source), with the injected path cost, computed as the difference of
the two costs (algebraically w − e; p = o gives exactly 0). The `[IR]` line ends with `warrant=[<key>=none|observation
...]` over every live hypothesis in hypothesis order (`warrant=[]` when exhausted), after `tails=[...]`; the existing
fields and their order are unchanged. Verified: the IR test-bed's oracle, extended by derivation, agrees on every tick
of the seventeen scenarios; the belief and the adequacy are unchanged (prior on, every `[IR*]` line of the 48 maintained
logs byte-identical to 2.5 once the field is removed). A consequence recorded in the entry's BUILT paragraph: the
movement source is a half-plane test, so a lone foreseeable task is warranted by any walk within 90° of its target's
bearing (the exit walk in scenario_s09_01 from 126).

## 2. Parameters

Two constants in `shared/likelihood_functions.py`, each with a physical meaning, read through the module; the
rest are the body's or the run's, passed to the constructor. `shared/` holds no default for any of them.

| parameter | value (Mesa) | source | meaning |
|---|---|---|---|
| β | 0.01 /cm | body, `mesa_configs.yaml` `simulation.beta` | Detour tolerance: L at v·D = 1/β = 100 cm is 2/(1+e) ≈ 0.54. Since T-D E5 also the scale of the adequacy test's reference distribution. A physical tolerance per embodiment, not per layout (T-A1). |
| v (`speed`) | 20 cm/tick | body, `mesa_configs.yaml` `simulation.step_size` (the Projector's `assumed_speed`) | converts between excess and ticks in D; one standing tick beyond s_exp is v·1 = 20 cm |
| `duration_to_steps` | seconds / 2.0, at least 1 | body, `_parse_duration_to_steps` over `simulation.seconds_per_step` (the Projector's) | a duration binding in ticks, for s_exp |
| `default_action_cost` | 1 tick | body, `RobotAgent` (the Projector's) | the own stationary duration of `pick_up` and `place` in s_exp (TODO-113: a schema fact later) |
| `action_completion_latency` | 1 tick | body, `mesa_sim/executor.ACTION_COMPLETION_LATENCY` (the Projector's) | E9: priced to the phase a completion opens |
| `observed_task_completion_latency` | 0 ticks | body, `mesa_sim/sim_agents.HUMAN_TASK_COMPLETION_LATENCY` (the Projector's, for the observed agent) | E9: priced, with the action latency, to the phases a boundary opens |
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

## 3. The guarantee statement (β = 0.01 /cm, θ = 0.75, T-D cycle 1.5b)

"Guarantee" means: holds in every measured condition and follows from the model, not from a scenario. The
conditions are the `analysis/tb1a_destination/` set at the cycle 1.5b regeneration (the five regression
fixtures and the three evaluation fixtures × assignment prior off/on, `single_task`, stop off,
PYTHONHASHSEED=0; logs local, md5s in its README). The reveal columns give the value before R1 (the T-L stage 3
logs), at Stage 1 / 1.3b, and at 1.5b, as old → 1.3b → 1.5b where the last moved; old → new where only R1 moved it. Ticks are `[IR] step=` values. A reveal is the first tick the task the
human is executing is `most_likely` with confidence ≥ θ; the human's task is read from the record's
transitions, which land 2 ticks after the world fact the recognizer's boundary reads (all 48 runs). The
adequacy finding's figures (false-unexplained, missed findings, detection delay) are session 1.4's
measurement, not stated here.

| fixture | task (human, in order) | reveal prior-on | reveal prior-off | grasp / done |
|---|---|---|---|---|
| scenario_s01_01 | item_3 | 20 → 9 | 37 | grasp 41 |
|  | item_2 | 94 → 78 | 108 → 114 → 113 | grasp 110 |
| scenario_s02_01 | item_2 | 24 → 23 | 29 → 35 → 34 | grasp 31 |
|  | coffee_break | 122 → none → 130 | 122 → none → 134 | done 155 |
|  | item_5 | 200 → 160 | 243 → 242 | grasp 247 |
|  | ac_activation(ac_switch_0) | 336 → 309 | 338 → 328 | done 364 |
| scenario_s03_01 | item_3 | 11 → 5 | 20 → 30 → 29 | grasp 22 |
|  | item_2 | 71 → 54 | 86 → 94 → 93 | grasp 88 |
| scenario_s01_06 | item_3 | 23 → 18 | 27 → 26 | grasp 39 |
|  | item_7 | 86 → 74 | 87 → 84 | grasp 97 |
| scenario_s04_01 | item_3 | 30 → 19 | 30 → 19 | grasp 60 |
|  | coffee_break | 152 → none → 158 | 152 → none → 158 | done 185 |
|  | ac_activation(ac_switch_1) | 203 → none | 203 → none | done 207 |
|  | ac_activation(ac_switch_2) | 216 → 214 | 217 | done 227 |
|  | item_6 | 250 → 243 | 261 → 260 | grasp 268 |
| scenario_s03_06 | item_3 | 11 → 6 | 20 → 30 → 29 | grasp 22 |
|  | item_2 | 74 → 69 | 86 → 94 → 93 | grasp 88 |
|  | coffee_break | 134 → 121 | 137 → 135 | done 178 |
| scenario_s05_01 / _02 | coffee_break | 23 → none → 32 | 23 → none → 36 | done 56 |
|  | item_5 | 59 → 60 | 60 → 71 → 70 | grasp 62 |
|  | ac_activation(ac_switch_0) | 118 → 94 | 120 / 118 → 104 | done 143 |

### 3.1 Prior-on (the observed agent's assignment is known)

The recognizer GUARANTEES:
- **The belief is over the assigned and foreseeable tasks only.** Everything else is pinned at 10⁻³ and never
  scored.
- **At a boundary with one live task left, that task is at θ on the boundary tick**, by normalisation (R1):
  scenario_s01_01 item_2 at 78, scenario_s03_01 item_2 at 54, scenario_s01_06 item_7 at 74, scenario_s05_01 /
  _02 ac_switch_0 at 94. Its confidence is $1 - 0.001\cdot|pinned|$ (0.996) on no evidence, and its hypothesis
  adequacy is NO_OBSERVATION on the boundary tick: the meta-planner's gate refuses it there (G1) and admits it on
  the latency tick b + 1, on a belief of 1.0 by normalisation and one priced standing tick (79, 55, 75, 95; at 1.5b
  the first walking tick b + 2; TODO-119).
- **The first task, and a task among several live ones, is revealed on the walk**: every walk reveal precedes
  the grasp (the table). With R1 an even prior over two or three keys needs only the rivals refuted, so first
  reveals moved earlier (scenario_s01_01 item_3 20 → 9, scenario_s03_01 11 → 5).
- **A foreseen stay is revealed during its stand** (E10): `coffee_break` clears θ in scenario_s02_01 at 130,
  scenario_s04_01 at 158 and scenario_s05_01 / _02 at 32, each during its priced `wait_at`, when the rival on its
  bearing has stood about 9 ticks beyond its own priced standing (§1.9). Under Stage 1 it was never at θ (the stand
  moved only the finding). `ac_activation(ac_switch_1)` in scenario_s04_01 is still never at θ: its stand is one tick
  (PT2S), and it peaks at 0.475 (204) before completing (205).
- **After every admissible task is complete**, the recognizer is EXHAUSTED (scenario_s01_01 from 141,
  scenario_s02_01 from 362, scenario_s03_01 from 121, scenario_s01_06 from 120, scenario_s03_06 from 176,
  scenario_s05_01 / _02 from 141), unless a foreseeable task
  never performed stays live: in scenario_s04_01 `ac_activation(ac_switch_0)` is then the lone live task and
  at θ from 327, with the human idle — a crossing of a task the human is not executing. It is refused on 327
  (the boundary tick), admitted at 328 (the priced latency tick, S = 1), and inadequate from 345.
- **A completed task is at the floor for the rest of the run**, whoever completed it.

### 3.2 Prior-off (no assignment known)

The same model over a larger live set: every task of every object, the robot's own undelivered items
included. Therefore:
- **Reveals are later, and several now follow the grasp**: scenario_s01_01 item_2 at 113 (grasp 110),
  scenario_s02_01 item_2 at 34 (31), scenario_s03_01 / _06 item_3 at 29 (22) and item_2 at 93 (88),
  scenario_s05_01 / _02 item_5 at 70 (62) — each one tick earlier than at Stage 1, the rivals now charged the
  standing tick they are not priced for (E10). Before R1 these were the arrival-fold reveals (an arrival counted
  two observations against `unknown`); an arrival folds L = 1, so the true task is separated when the rivals'
  carry phases are refuted or their standing is charged.
- **After the human's last task, the robot's own remaining item is at θ** once it is the lone live task, with
  the human idle: scenario_s01_01 item_4 at 141, scenario_s03_01 item_7 at 145, scenario_s01_06 item_6 at 160,
  scenario_s03_06 item_7 at 176, scenario_s05_01 item_3 at 171, scenario_s05_02 item_2 at 172, scenario_s04_01
  `ac_activation(ac_switch_0)` at 379. Before R1, `unknown` held half the mass there and nothing crossed. Its
  hypothesis adequacy follows the idle stand: no observation on the boundary tick, adequate on the latency tick and
  the next 16 ticks (standing charged beyond s_exp = 1), inadequate after. The gate (G1) therefore admits it where
  it is still adequate (scenario_s01_01 at 142, hold 32, which runs to 173 though the leader is inadequate from 159:
  a projection is retained by identity, D2; TODO-118, TODO-119) and refuses it where it is already inadequate (scenario_s03_01 at 147,
  `none(leader_inadequate)`: no hold, the run completes at 236). See §5.
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
  be. A stand beyond the phase's priced standing is charged in the belief and in the adequacy test alike (E10,
  §1.4, §1.10); a real human's pauses would refute the true task as they refute a rival. Every task in the script is one the domain describes (well typed, F47b).

### 3.4 What the meta-planner may assume, and must not

MAY assume, either setting: a completed task never returns. After the human's own completion the belief is
the uniform prior over what is live, and `most_likely` carries no information until the human moves unless one
task is live. When nothing is live the recognizer says so (EXHAUSTED, `most_likely` `None`, confidence 0).

MUST NOT assume, either setting:
- that a task at θ is the task being executed now: a lone live task is at θ by normalisation, whatever the
  human does (§3.1, §3.2);
- that confidence is comparable across live-set sizes (0.75 is a different bar over 1, 2 and 8 keys);
- that confidence says anything absolute: the belief is relative over the robot's models; whether the best of
  them is wrong is the adequacy finding (§1.10); the meta-planner reads the leader's hypothesis adequacy at its
  gate (G1), not the finding;
- that an admitted hypothesis stays adequate: the gate is asked at admission only (D2), and a projection is kept
  while the leader turns inadequate (scenario_s01_01 prior off, 159–173);
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
refuting. A stationary phase (`pick_up`, `place`, `wait_at`) is evidence in the belief only through standing
beyond its priced duration (E10), and for a rival only through its own charges; a stay is revealed as the rivals on
its bearing are charged their standing (§1.9).

**(c) The adequacy test's limitations, recorded in the entry and not built**: sub-threshold waste is not
summed across phases; a regress at the proximity threshold restarts a hypothesis's test; the false-unexplained
count per run grows with the number of phases of the true hypothesis. Under the membership rule as first
ruled, a finding could be unexplained while the true hypothesis was a non-member (standing within its priced
duration) and only a refuted rival a member (scenario_s01_01 prior-on, steps 76–77, the human placing item_3);
the E6 amendment of 27 September 2026 makes that hypothesis a member with S = 1, and the finding there reads
adequate. E8 does the same for the advance tick (the grasp), and E6's second amendment for the latency tick after
it (1.5c): no false unexplained remains on modelled ticks (§1.10).

Also stated, lower in consequence:
- An undecomposable hypothesis scores the perfect fit in the belief and is never a member of the adequacy
  test; no case occurs in the maintained baselines (§1.10).
  SUPERSEDED (T-G A4, built in T-G stage 1, step 3, 1 October 2026; bd4bddc): it leaves the live set (§1.1).
- The boundary infers authorship from the phase. A domain where another agent satisfies a terminal condition
  while the observed agent stands in its terminal phase would attribute wrongly.
- Evidence accumulated under one method is reused when the guard re-selects another. Dormant in kitting (every
  within-episode flip is the observed agent's own grasp or release, TODO-55 (d)).

## 5. The interface to the meta-planner

`update()` returns a `BeliefState` (`shared/io_contracts.md` §1.2; contract §2.1): `timestamp`, `agent_id`,
`distribution` (every hypothesis key, pinned ones at 10⁻³), `most_likely` (the argmax over H, `None` when
exhausted), `confidence` (its value, 0.0 when exhausted), `finding`, `lifecycle`, `tails`,
`hypothesis_adequacy` and, since G-build, `observation_warrant` (§1.10). The meta-planner reads `most_likely`,
`confidence`, the leader's `hypothesis_adequacy` and the leader's `observation_warrant` (io_contracts §2.2), never α or
the tails; the finding and the lifecycle are for the rest of G and X (R5):
- `_clears_gate(belief) -> GateOutcome`, the one place θ is applied and the one home of the guard on admission
  (G1): CLEARS iff `confidence ≥ θ` (θ = `DEFAULT_THETA` = 0.75, unchanged) and the leader's hypothesis adequacy
  is ADEQUATE; otherwise, in this order, BELOW_THETA, LEADER_NO_OBSERVATION, LEADER_INADEQUATE. A guard refusal
  behaves as below θ.
  SINCE G-BUILD (T-D G, AD1, AD4; 81a9f86): CLEARS also requires the leader to be WARRANTED, and a third refusal,
  LEADER_UNWARRANTED (`none(leader_unwarranted)`), is asked after LEADER_INADEQUATE. Warrant is commitment (the leader is
  one of the observed human's assigned tasks, `same_task`, the meta-planner's new input `observed_assigned_tasks`, prior
  on only) or observation (`belief.observation_warrant`), read by `_warrant(belief)`; the gate reconstructs no
  recognizer quantity. `[meta-proj] projection=built` names the source (`warrant=commitment`, `observation`, or
  `commitment,observation`). Loss of observation warrant fires nothing (AD3): retention stays by identity and retraction
  on inadequacy. Measured at the G-build regeneration: prior on, the lone coffee_break at b + 1 on a standing tick is no
  longer admitted (scenario_s02_01 at 363, scenario_s05_01 / _02 at 142) or is admitted one tick later on its first
  step's gain (scenario_s03_06, 123 for 122); no prior-on completion moved.
  The gate's input changed meaning with R1 (the leader's share over H); the gate ruling
  (September 2026) stands and its justification is G's. Measured at the 1.5b and 1.5c regenerations
  (`analysis/td_stage1b/REPORT.md`): every boundary admission of a lone live task moves from the boundary tick to
  the latency tick after it (b + 1; b + 2 at 1.5b); the wrong-table delivery is refused at 76 / 79
  (`none(leader_inadequate)`); coffee_break is admitted during its stand; prior off the robot's own remaining item is
  admitted where the idle human's stand has not yet made it inadequate (scenario_s01_01 at 142, hold 32, completion
  201) and refused where it has (scenario_s03_01: completes at 236).
- `evaluate_triggers()` fires `recognition_changed` (D2) when a decision record `_projected_hypothesis`
  exists and `most_likely` is no longer it: a replacement, the human's boundary, or no hypothesis live. It also
  fires when no record exists and the belief clears the gate (θ and the guard, one condition).
  SUPERSEDED IN PART (T-D L2 (ii), ruled 27 September 2026, built in L-build): it also fires when the recorded
  hypothesis leaves adequate (its `hypothesis_adequacy`), that hypothesis only, never a rival's transition: RETRACTION,
  the meta-planner's act. Admission is re-asked and G1 refuses; re-admission through the entering side. The recognizer
  retracts nothing (L2 (i)). design_decisions.md, "T-D L: the belief lifecycle", L2.
  AMENDED (Hadi, on the L-records report, 27 September 2026): "leaves adequate" is adequate to inadequate
  (built as the state: the recorded hypothesis is inadequate); no P fallback. It also fires on a belief re-initialised
  at an episode boundary (`belief.episode_boundary`), whether or not most_likely changed (L5 B).
- `update_human_projection()` admits a projection only when the gate clears. It resolves the key through
  `recognizer.get_hypothesis()` (the same live instance, held by reference) to project the human's task, and
  records the hypothesis it projected. Its refusal reasons are `none(below_theta)`, `none(leader_no_observation)`,
  `none(leader_inadequate)` (G1), `none(leader_unwarranted)` (T-D G), `none(no_human)` and `none(unprojectable)` (the projector could not resolve the
  task; `none(unresolved)` before the Stage 1 build). When the recognizer is exhausted it refuses as
  `none(below_theta)`.

Confidence is a gate, never a magnitude in any cost; `distribution` is logged and not read. (See TODO-97 (24 Sept 2026): belief-aware planning, one realization against the hypotheses covering 1 − ε of the mass, recorded for after the T-D recognizer pass, not decided.) A
re-crossing of the recorded hypothesis fires nothing; a change of hypothesis or its end fires
(`design_decisions.md`, the D2 entry).

## 6. Open items

| item | where | one line |
|---|---|---|
| an admitted projection retained while its leader turns inadequate | TODO-118 (L); D2 | the gate is asked at admission only (scenario_s01_01 prior off, 159–173) |
| a lone hypothesis admitted at b + 1 on a belief of 1.0 and one priced standing tick | TODO-119 (P, G) | prior off the idle lone item is adequate for about 16 ticks after the boundary |
| a misdelivered item's hypothesis admitted after the release | TODO-87 (L) | scenario_s06_06 at 103, scenario_s07_03 at 94: S = 1 in a stationary phase at the item's new place |
| what the meta-planner does with the finding and lifecycle | G, X (T-D) | R5; TODO-97 on its own gate; G1 built |
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
channel (closed by decision, T-D R and E: time enters adequacy only; superseded in part by E10 at 1.5b: standing
beyond the priced standing is belief evidence through D, not a channel of its own); TODO-61 (b) (reason superseded
by R1).

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
| a reserved "duration" progress evaluator | standing enters through D beside the excess (E10), not as an evaluator of its own | T-D R and E (E3, E10) |
| `PROGRESS_EVALUATORS` and `excess_path_likelihood` | the belief reads the excess through D (`delay_likelihood`), not through a likelihood of the excess alone; no reader was left | T-D R and E (E10), cycle 1.5b |

Also gone and not to be re-added:
- any persistence of belief across an episode boundary (I4c; I4b's "reset the geometry, keep the belief" was
  measured and found wrong);
- any charge for an empty phase or for standing within the priced standing (I4c, narrowed by E10);
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

| Sept 27, T-D R and E Stage 1 | the `unknown` hypothesis, u, the grade and the odds accounting; one number carrying four meanings | the belief normalised over the live set H only (§1.5); beside it the adequacy finding, per live hypothesis per derived phase, D and its tail S at the test level α (§1.10), and the lifecycle state (EXHAUSTED when H is empty) | the relative test could not express "the best of my models is wrong"; `unknown` at 0.995 was normalisation, not evidence. |
| Sept 27, T-D cycle 1.5b | the stand counted in adequacy only; s_exp the action's own segment; the completing hypothesis out of the test on its advance tick; admission on the leader's share alone | E10: the belief's evidence per phase is L(v·D) (§1.4); E9: s_exp the Projector's priced stationary ticks within the phase (§1.10); E8: the advance tick a member at S = 1; G1: per-hypothesis adequacy, read by the meta-planner's gate for the leader (§5) | the foreseen stay was no longer foreseen (1.4 finding 4); the latency tick was charged to the walk (finding 2); grasp-tick false unexplained (finding 1); a lone hypothesis admitted on no evidence and the wrong table admitted while unexplained (finding 3). Every figure in §3 is from this HEAD, with earlier values where they moved. |
| Sept 27, T-D cycle 1.5c | the latency tick after a completion holding no observation (the three false unexplained of 1.5b, at grasp + 1) | E6's second amendment: a stationary tick within the priced standing of any phase with s_exp > 0 is an observation at S = 1; no member on a boundary tick (§1.10) | zero false unexplained on modelled ticks; the boundary reads unresolved, adequate, adequate |

Superseded figures (the I5 matrix, any s40 figure before F47b, and the graded-evidence figures before the T-D
Stage 1 build) are not carried here. Where they are cited
elsewhere they describe the fixture of their time.
