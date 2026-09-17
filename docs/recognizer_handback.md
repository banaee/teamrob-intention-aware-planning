# The intention recognizer — hand-back after I5

For whoever resumes the meta-planner work. State of `shared/recognizer.py` and `shared/likelihood_functions.py`
at the I5 commit, confirmed by the matrix in `analysis/i5_handback/` (eight conditions: s00, s20, s30,
scenario_40 × assignment prior off/on; scenario_10 dropped, TODO-52). The design history is in
`docs/design_decisions.md` (entries I1–I5); the open items in `docs/TODOS_AND_DEFERRED.md`.

## 1. What the recognizer is

A Bayesian recognizer over task hypotheses — one per (task, bindings) from the domain schemas and the workspace
objects — plus a constant `unknown`. Every tick, for every live hypothesis, the planner decomposes the task
against the current world for the observed agent (its guards select the method; what the agent holds decides
between `deliver_default`, `deliver_already_held` and `deliver_with_return`), the grounded actions are walked
from the start, and the EXPECTED action is the first whose completion condition does not hold: the phase is
derived, never stored. A task's likelihood is the likelihood of the action it expects now. A movement action
(`move_to`) is scored by the excess-path cost from the hypothesis's ORIGIN — where the agent was when it began
expecting that action — through a logistic: excess = walked + C(pos, g) − C(origin, g), L = 2/(1 + e^{β·excess}),
1 at zero excess. One stretch of movement toward one target is one observation however many ticks it spans;
its value is recomputed from the origin and replaces the previous tick's. A discrete completion signal in the
expected action's vocabulary (GRASP for `pick_up`, RELEASE for `place`) is scored by detection reliability: the
hit rate if the action's completion predicate holds, the false-alarm rate if not; an event multiplies into the
evidence once. An action with no graded signal (`pick_up`, `place`, `wait_at`) scores the perfect-fit value. An
EMPTY stretch — nothing walked since the origin — is not an observation and contributes no factor. `unknown` is
the reference: a hypothesis's evidence is its ODDS against `unknown`, the product over its own observations of
L/u; a stretch folds into the base as L/u when the expected action changes; `unknown` itself takes no factor.
The episode is local: when a completion retires a hypothesis whose expected action on the previous tick WAS
its terminal action (the observed agent's own phase reached the completing action), the belief re-initialises
to the uniform prior over the hypotheses still live and every origin moves to the agent's position — nothing
crosses an episode boundary. A completed task (its terminal predicate holds, whoever did it) is pinned at the
floor for the rest of the run: the pin and the boundary have different criteria and are not unified. With an
assignment known (prior-on), the support is restricted to the assigned tasks, the foreseeable tasks and
`unknown`; inadmissible hypotheses are pinned, never scored. The output is evidence × context weight,
normalised, floored at 10⁻³, with pins restored.

## 2. The four parameters

| constant | value | meaning |
|---|---|---|
| `BETA` | 0.01 /cm | detour tolerance: the excess at which a hypothesis's likelihood has fallen to ≈ 0.27 is 1/β = 100 cm. In centimetres, hence layout-scale dependent (TODO-58). |
| `UNKNOWN_LIKELIHOOD` (u) | 0.1 | the likelihood of any observation under `unknown` — the bar a hypothesis must clear per observation, and the unit of the ceiling: a lone fitting task reaches 1/(1 + uⁿ) over n observations. |
| `DETECTION_HIT_RATE` / `DETECTION_FALSE_ALARM_RATE` | 1.0 / 10⁻³ | the completion detector's reliability. In Mesa the simulator's report is ground truth; the false-alarm rate is non-zero only so a refuted hypothesis keeps a recoverable base. Set from a real cell's measured rates. |
| θ (`CONFIDENCE_THRESHOLD`, meta-planner) | 0.75 | the gate on the normalised posterior. Not a likelihood parameter; its meaning depends on the live set (§5, TODO-65). |

Not parameters but load-bearing: `BELIEF_FLOOR` = 10⁻³ (output only); `PROXIMITY_THRESHOLD` = 30 cm in
`mesa_sim/world_state_builder.py`, which decides when `at(agent, x)` holds and therefore when every phase
advances; the context weights (TEMPERATURE_BOOST 3.0, FATIGUE_BOOST 2.5 on literal task names — TODO-66,
output only, inert in every measured condition).

## 3. The guarantee statement (β = 0.01 /cm, u = 0.1, θ = 0.75)

Everything below is measured at these values on the four layouts, under the premises in §3.3. "Guarantee"
means: holds in every measured condition and follows from the model, not from a scenario.

**Figures superseded for scenario_40 (F47b, September 2026).** Every scenario_40 tick below was measured
with the segment-3 legs scripted as `ac_activation` bound to two `waypoint` objects — an ill-typed script
that gave the walks no hypothesis. F47b retyped the two targets as AC switches (`ac_switch_1`, `ac_switch_2`)
at the same coordinates, so `ac_activation` has three hypotheses and the s40 belief differs from tick 0.
On the regenerated baseline (`analysis/f47_fixtures/README.md`): the coffee crossing is at 153 under both
priors (peak 0.915 / 0.917, not 0.982 / 0.984; was 135 prior-on, 143 prior-off); the two AC legs ARE
recognised (205: ac_switch_1 0.784 / 0.878; 221: ac_switch_2 0.772 / 0.853) and pinned complete at 207 and
228, so their ends are boundaries; an item_6 crossing appears at 266 (off) / 250 (on). The s00 / s20 / s30
figures stand; scenario_10 was reinstated in the sweep at R1/T9 on the cleaned env_layout1 (its figures here
were never part of the I5 matrix). The model, its parameters and the guarantees' form are unchanged.

### 3.1 Prior-on (the observed agent's assignment is known)

The recognizer GUARANTEES:
- **The belief is over the assigned tasks, the foreseeable tasks and `unknown` only.** Everything else is
  pinned at 10⁻³ and never scored. The live set is small (3–4 tasks + `unknown` in these layouts).
- **A task the agent is executing is revealed above θ before its grasp** — first task: s00 11, s20 6, s30 21,
  s40 19; next task: s00 81, s20 57, s30 77 (all pre-grasp; grasps at 41, 22, 39, 60, 111, 89, 98) — and a
  deviation with no grasp (coffee) at 135, mid-walk. Conditional on β and u (I4b's fine grid: pre-grasp
  first-task reveals in 24 of 25 cells; coffee ≥ θ in all 25 — the region analysis is closed, do not reopen).
- **No wrong task crosses θ except on a walk geometrically indistinguishable from that task's approach**
  (s40 203–213: 20 ticks of zero-excess walk on the bearing to shelf_6; the turn retracts it, 0.790 → 0.083).
  That is the model's characterised limitation (§4 (a)), not an error the model can see.
- **One `theta_crossed` per recognition.** No repeated crossing in any prior-on condition.
- **After the agent's own task completion, the belief is the uniform prior over the live set** (0.25–0.5 each)
  until the agent moves; `most_likely` on those ticks is a key-order tie-break, and its confidence is 1/n.
- **Confidence on a fitting task is 0.905 on its first stretch, 0.986 after its first phase advance, 0.995
  after its second**, and it can legitimately FALL when the next expected action stops fitting (non-monotone by
  design; do not smooth).
- **A completed task is at the floor for the rest of the run**, whoever completed it.

### 3.2 Prior-off (no assignment known)

The recognizer GUARANTEES the same model over a larger live set — every task of every object in the workspace,
the robot's own undelivered items included — and therefore:
- **First-task reveals still precede the grasp in all four layouts** (39, 20, 28, 19; s20's 20 is the
  arrival's fold — before I4d it was 31, after the grasp — and depends on a phase advance at 30 cm from the
  shelf, not on the walk). Next-task reveals: 109, 87, 87 (pre-grasp). Coffee at 143 (later than 135: seven
  live rivals instead of three must be walked away from). **No wrong crossing** in any prior-off condition.
- **Repeated `theta_crossed` per recognition**: s00_off 109 / 113 / 115, s20_off 20 / 24 / 30 and 87 / 91 / 95.
  The rivals' `deliver_with_return` phases at the grasp lift them briefly (§5). The belief is correct; the
  event fires each time the trajectory crosses.
- **An idle human sits at the prior over the robot's undelivered items**: after the human's last task,
  `most_likely` is one of the robot's items at 1/n ≤ 0.5 (s00_off 0.5 until the robot's delivery, s20_off
  0.33, s30_off 0.33, s40_off 0.33 → 0.5 at 376). A robot completion shrinks the set (the pin) without
  re-initialising (no boundary). Never above θ; never a crossing.
- **Dilution**: with more live rivals the same evidence yields lower confidence (item_6's aligned walk peaks
  at 0.462 prior-off against 0.790 prior-on; coffee's ceiling in segment 2 0.87 against 0.90).

### 3.3 What every figure above is conditional on

- **Straight lines.** Mesa agents walk straight through obstacles, and C is Euclidean, so the true hypothesis's
  excess is exactly 0 and every rival's excess is exactly its wasted distance. In a real cell with obstacles
  the true hypothesis is CHARGED for every detour the path cost does not model; inject a path cost
  (`IntentionRecognizer(path_cost=…)`) before reading any confidence figure as a guarantee there.
- **`PROXIMITY_THRESHOLD` = 30 cm.** Decides when `at()` holds, hence when a stretch closes and folds (×10
  against `unknown`) and when the next phase's observation begins. Every "pre-grasp" figure is a fold at 30 cm
  from the target; a different threshold moves every reveal tick and every ceiling step.
- **Kitting's guards.** Prior-off's repeated crossings and every rival's flip are `deliver_with_return`'s
  phases (TODO-55 (e)); a domain without a holding-driven method change has neither.
- **The layout's decoy geometry.** Collinear decoys (s20) are not separated by the walk; they are separated
  by the arrival's fold. A layout with a decoy beyond the target on the same bearing AND within 30 cm of it
  would not separate them before the grasp.
- **The live set's size** sets the prior, the dilution and what θ means (TODO-64, TODO-65).
- **β, u** set every reveal tick (the closed-form and fine-grid results of I4b/I4c, closed).
- **The scripted human.** Every scenario's human follows a script; a human who hesitates, back-tracks or
  wanders mid-task is charged like a rival would be — the stationarity channel that could read a pause as
  evidence is not built (TODO-59).

### 3.4 What the meta-planner may assume, and must not

MAY assume, prior-on: a `theta_crossed` whose winner is a task is that task being executed now (no wrong
crossing except the aligned-walk case, which the meta-planner cannot distinguish either); one crossing per
recognition; confidence ≥ θ persists while the task's actions keep fitting and ends at the task's completion
(the pin) or at a detour; a completed task never returns; after the human's own completion the belief is the
prior and `most_likely` carries no information until the human moves.

MAY assume, prior-off: the same except one crossing per recognition — expect up to three within the grasp
stop, all on the same winner; and that `most_likely` on an idle human is the robot's own item at ≤ 0.5.

MUST NOT assume, either setting: that confidence is comparable across live-set sizes (0.75 is a different
bar with 3 and with 8 hypotheses); that `unknown` ≥ θ means the human is idle (it also means a task the space
does not contain, or a detour under way); that a robot completion is a human boundary; that the ceiling is
0.909 (it is 1/(1 + uⁿ)); that confidence is monotone within a task; that a `theta_crossed` on `unknown`
(TODO-54) or a `most_likely` change without a crossing (TODO-48) carries any recognition; that anything in the
belief refers to a previous episode; that the segment-3 wander's end is a boundary (nothing fired there;
since F47b the legs are AC-switch tasks and their completions ARE boundaries — see the note above §3.1).

## 4. The characterised limitations (TODO-61 — properties of the chosen model, not defects)

Both follow from costdif1 with a constant `unknown`, and both were visible in I4d's accounting invariant
before they were measured. Kept under one item because they share that root and any remedy for one changes the
other's currency; kept as two sharp statements because they are distinct mechanisms.

**(a) Confirmation is length-blind.** dC discriminates by penalising wrong hypotheses, not by rewarding right
ones: the correct hypothesis sits at zero excess however far it walks — L(0) = 1 after 15 cm as after 300 cm.
Evidence is one-sided, strong at refutation and weak at confirmation. Seen: one 15 cm step on the bearing to
shelf_6 takes item_6 from 0.333 to 0.485 (s40_on 187); a rival's regress after the grasp opens a fresh stretch
at L ≈ 1 (s00_off 114).

**(b) Accumulation is observation-count and decomposition sensitive.** Each scored observation is worth its
likelihood relative to the constant `unknown` — 1/u for any fitting observation, whatever it observed: a
300 cm walk straight at the target, a stationary `pick_up` phase, a regress-generated zero-excess stretch. A
hypothesis's decomposition (how many phases its selected method has, where its steps sit) therefore sets how
much evidence it can accumulate. Seen: item_6 recognised at 274 in s40 despite a 539 cm detour worth ×0.09,
because two fitting observations at ×10 each outweigh it; s20_off's first reveal moving 31 → 20 because the
arrival's fold separates item_3 from its collinear decoys before the grasp; the prior-off repeated crossings
(§5).

Neither is a reason to touch β, u or the likelihood form. Candidate remedies are recorded in TODO-61 with the
decision each would require (a confirmation term graded by covered fraction for (a); u per unit of evidence
or decomposition-normalised odds for (b), which change what `unknown` means and must be decided with the
rationality-measure alternative, TODO-63).

## 5. The `theta_crossed` question — three things, kept apart (TODO-68)

DECIDED (D2, September 2026): (c) was decided as the design chat's question, and the answer changed the consumer,
not the event or the model — `recognition_changed` replaces `theta_crossed` in `evaluate_triggers()`, tracking the
identity of the projected hypothesis (design_decisions.md, D2 entry). The measurements below stand as recorded.

Measured prior-off: the true task crosses θ three times per recognition (s00_off 109 / 113 / 115; s20_off
20 / 24 / 30 and 87 / 91 / 95). The bumps existed in I4c below θ; I4d's ceiling made them cross; the
correction did not create them.

**(a) Recognizer belief behaviour.** The trajectory is exactly what the stated model implies: the I4d
invariant holds to 7e-15 on every one of these ticks. The true task rises above θ at its arrival (its
`move_to` folds, ×10). At the grasp each live rival's method flips to `deliver_with_return`, whose `place`
phase back on the shelf is a no-graded-signal observation worth 1/u — the rival lifts, the true task dips.
On departure the rival regresses to a fresh zero-excess stretch at L ≈ 1 and lifts again; the walk away then
refutes it. **The recognizer is correctly implementing its model.** The producer is the rivals' phase structure
under the carry (§4 (b) and (a); TODO-55 (e)), not the true task's fold.

**(b) The semantics of `theta_crossed` as an interface event.** `shared/io_contracts.md` defines it as
"confidence crosses θ from below to at-or-above (prev < θ ≤ current) — a crossing event, not confidence ≥ θ
per tick". The contract promises an event whenever the trajectory crosses; it does NOT promise one crossing
per task. Repeated crossings are consistent with it. What the meta-planner reads the event as — "a task has
just become recognised" — is a stronger claim than the contract makes. If a one-shot semantics is wanted (one
event per task per episode), that is an INTERFACE / DESIGN decision — a change to the event's definition or
to the consumer (a per-episode latch, a gate on odds against `unknown` — TODO-65) — and not a reason to change
the evidence model.

**(c) The meta-planner's handling.** Out of scope here, handed over: each crossing re-runs B2/B3 (s20_off
re-decides at 20, 24, 29, 30 and again at 87–103, moving the robot's item_4 delivery from 52 to 60 and
item_6's from 136 to 144). Decide together with TODO-48 (no trigger on a `most_likely` change above θ) and
TODO-54 (`theta_crossed` on `unknown` after a pin): the three are one question — what a trigger is an event OF.

## 6. Open items travelling with this hand-back

| item | where | one line |
|---|---|---|
| θ's reachability | TODO-64 | ceiling 1/(1 + uⁿ); first-stretch reachability needs the rivals' summed odds < 0.233; is θ a fit bar or a prefix-length bar? |
| gate as a likelihood ratio | TODO-65 | the posterior gate is live-set dependent; the evidence state already is odds against `unknown` |
| `deliver_with_return`'s guard | TODO-55 (e) | a stray item vs an assigned one; a domain question, implicated in the prior-off crossings |
| the evidence model's two properties | TODO-61 (a), (b) | §4 |
| `theta_crossed` one-shot vs crossing | TODO-68, with TODO-48, TODO-54 — closed by D2 | §5 |
| the context / knowledge-representation pass | TODO-66 | `_context_weight` names two tasks and carries four constants; output only |
| the stationarity channel | TODO-59 (deferred paragraph) | standing still as evidence against movement hypotheses; outside dC, not built |
| the unmodelled segment 3 → 4 boundary | TODO-57 (question 3) | superseded by F47b: the legs are `ac_activation` tasks, their completions pin and re-initialise; a declared unmodelled behaviour is TODO-80 |
| the two analytical tools | TODO-62 (radius of maximum probability), TODO-63 (rationality measure) | filed, not built, with their triggers |
| TODO-52's latent crash; s30_off's item_2 at 87 | TODO-52, TODO-67 | meta-planner side |
| scenario_10 | TODO-52 (and TODO-42) | dropped from the sweep in I2; reinstated at R1/T9 on the cleaned env_layout1 (the RuntimeError path is gone since T10/F1); `PYTHONHASHSEED=0` still required |
| β in centimetres | TODO-58 | layout-scale dependence |
| `io_contracts.md` §1.3 / §2.1 describe the pre-I2 recognizer | TODO-72 | leg model, cosine kernel, held-item rule; align against §1–§2 here (found Sept 2026, meta-planner side, not edited) |

## 7. The paper-facing divergence

The HCM paper writes P(task | O) with O a sequence of ACTIONS. The recognizer never observes an action: it
observes a microaction and a position, and the action is LATENT. P(o | τ) = P(o | a_φ(τ)) is a
marginalisation over that latent action, collapsed because the phase is derived deterministically from the
world (design_decisions.md, the I3 entry). The paper is a position paper, outdated relative to this design,
and is not a specification; it will need rewriting on this point, and on the episode-local semantics (I4c),
the constant `unknown` (I4) and the odds accounting (I4d).

## 8. Removed, and must not return

| mechanism | why it went | where recorded |
|---|---|---|
| the held-item rule (refute a hypothesis that binds a portable object the agent is not holding) | a domain shortcut the phase model subsumes; wrong in domains with no holding relation | I3 |
| `ZONE_BOOST` | a soft multiplier standing in for a hard fact; fired for the wrong hypothesis in 28 of 52 measured episodes (I1 §5.4) | I3 |
| the global leg (one movement leg for all hypotheses, closed by the body's `stand`) | a stretch is per hypothesis, from its own origin; no leg closed by stillness, no decay, no factor | I2–I4 |
| HIGH / LOW / NEUTRAL likelihoods (4.0 / 0.1 / 1.0) | four numbers with no stated meaning; replaced by the excess-path logistic, detection reliability and a stated u | I4 |
| the cosine trajectory kernel (`"directional"`) | multiplied identical headings tick after tick (4ⁿ from one straight walk); replaced by one observation per stretch | I2, I4 |
| `methods[0]` and string-parsed bindings | the planner selects the method by guards; bindings are typed | I2 |
| the 10× assignment multiplier | knowledge of the assignment restricts the SUPPORT, not the magnitude | I1/T1 |

Also gone and not to be re-added: any persistence of belief across an episode boundary (I4c), any special
scoring of a zero-length stretch (I4c), `unknown` paying per tick (I4d).
