# I4d — fold `unknown` with the stretch (TODO-60)

> Superseding note (24 Sept 2026, the terminology ruling; `docs/glossary.md` §7, `docs/terminology_revision.md`): the harness (`analysis/i4_evidence_model/check_i4.py`, reused by I4c, I4d and I5) labels the human's ground truth `"unknown"` when the human's script is finished and for scenario_40's wander (`S40_TRUTH`: seg3a, seg3b, done). That is a WORLD fact written with the ROBOT's hypothesis name: read it as a finished work order, or unmodelled behaviour (the wander), respectively. So the "`!` = winner ≠ truth" marks and "wrong-θ" counts treat `unknown` leading as the correct reading of those ticks, and "unknown when idle" / `unknown_when_idle` is the `unknown` hypothesis's mass while the work order is finished (high by normalisation, not evidence of unmodelled behaviour). The same holds for this folder's `summary.md`.

Built on `ac240a8` (I4c). Same sweep, seed, interpreter and constants as I4c. Baseline = I4c's `run_mesa.py`
logs at `ac240a8` (`baseline/`, the same files as I4c's `new/`).

## 1. The accounting — written before the implementation

The recognizer reports a normalised set of odds against `unknown`. The invariant this correction establishes,
for every live hypothesis k and every tick t within an episode:

    E_t(k) / E_t(unknown)  =  [π(k) / π(unknown)]
                              × Π_{stretches s of k closed by t}   L_k(s) / u
                              × Π_{completion events e of k}       c_k(e)
                              × ( v_k(t) / u   if k's open stretch is an observation this tick, else 1 )

π is the prior at the episode start (uniform, so the first factor is 1); L_k(s) is the closing value of each
stretch of k — the excess-path value of a movement stretch, or the perfect-fit value of a phase whose action
has no graded signal (pick_up, place, wait_at); c_k(e) the detection factor of a completion event (hit 1.0,
false alarm 10⁻³); v_k(t) the open stretch's value; u = UNKNOWN_LIKELIHOOD. An empty stretch is not an
observation and contributes nothing to either side (TODO-59, unchanged).

What it says: `unknown` is the reference hypothesis. Each task's odds against it are the product, over that
task's own observations, of L/u. A fold moves one factor from the open term to the closed product and
changes nothing. That is the whole correction: the closed product held L alone, so u was lost at every fold,
and a task with only perfect folds stood at odds 1 against `unknown` the moment its stretch closed.

Representation chosen: the base of k holds k's closed odds (the second and third products); `unknown`'s
base is the reference and takes no factor; the open observation multiplies v/u onto k's base for this tick.
Nothing else is stored. The check: an independent accumulator in the harness, driven only by the recognizer's
per-tick phase state and the likelihood functions, must reproduce E_t(k)/E_t(unknown) on every tick of every
condition (`invariant.csv`).

What the invariant makes explicit, beyond removing the dip:

1. The ceiling for a lone fitting task is 1/(1 + uⁿ) over its n observations, no longer 1/(1 + u): after the
   first fold a fitting task reads 0.99, after the second 0.999.
2. Between two tasks with equal fit, one extra closed stretch is worth 1/u. A phase advance is evidence, and a
   hypothesis whose plan segments the same trajectory into more actions collects more factors
   (`deliver_with_return` has six actions to `deliver_default`'s four).
3. A regress folds too (I4: derived, so both happen), and a no-graded-signal phase folds its perfect-fit
   value — 1/u against `unknown` for having expected `place` or `pick_up` while the agent stood within reach.
4. On a tick where some hypotheses have an observation and one does not (the tick after its own advance,
   while rivals are mid-stretch), the empty one must pay nothing while the others pay L/u. `unknown`'s factor
   therefore becomes part of each hypothesis's odds, not a global per-tick factor on `unknown`; I4c's
   "u applies if some hypothesis was scored" was an approximation of this, exact only when every live
   stretch is in the same state.
5. Events are unchanged: the completion channel has no `unknown` counterpart (the gate's statement stands).
6. Nothing crosses an episode boundary: the bases are re-initialised to the prior there, closed odds included.

Consequences 1–3 are not side effects; they are what "u per observation" means once every observation is
counted. Point 2 is I4c's stated core property (prefix accumulation) made real against `unknown` and between
tasks. Whether point 3's 1/u for a `place` phase the agent never performed (a rival's flip under the carry:
item_6 at 60–62 in s40) is wanted is a phase-model question; it is measured below and left as it falls.

## How to read this directory

| File | Content |
|---|---|
| `check_i4d.py` | The matrix on I4's harness through I4c's helpers: variants `base` (shipped) and `nofold` (the reversion, cmp'd against `baseline/`); the invariant accumulator; unit checks (I4's U1–U3/U6, I4c's U7–U9, U5'' and U10 re-stated). |
| `invariant.csv` | One row per tick and live hypothesis: the accumulated odds, the recognizer's E(k)/E(unknown), |Δ log|. |
| `retrigger.md` | Criterion 2: the three windows, tick by tick, with the `[meta]` lines in them. |
| `summary.md`, `metrics.csv`, `retention.csv`, `chains.md`, `region.md` | As in I4c. In `chains.md` the `u paid` column now reads `—` everywhere: `unknown` takes no factor; the u is inside each hypothesis's odds. |
| `baseline/`, `new/`, `logs_instrumented/<variant>/`, `diffs/` | Not in git (`*.log`); `stages.sh` regenerates them (~5 min). `diffs/` is committed. |

## 2. What changed and where

`shared/recognizer.py`, `update()`: the fold multiplies `closing / u` into the base (was `closing`); the open
observation multiplies `value / u` (was `value`); `unnorm[unknown] = base[unknown]` always (was `× u` if some
hypothesis was scored — the `observed` flag is gone). Docstrings: the module's `unknown` paragraph (the
invariant), `_base`, `update()`. Nothing else: β, u, θ, the empty-stretch rule, the boundary and its
re-initialisation, the pin, the gate, the likelihood functions, the meta-planner are untouched.

Verification: instrumented `base` == `run_mesa.py`'s logs in all eight; `nofold` == I4c's logs (`baseline/`)
in all eight on the four greps, so the reversion is exact; the invariant holds to |Δ log odds| ≤ 7.1e-15 over
5,069 checks (every live hypothesis, every tick, eight conditions); retention at every boundary uniform (37 of
37 base rows). Unit checks: I4's U4 ("a:unknown unchanged across a zero-excess advance") and U5 ("evidence
ratio a:b exactly 1000 at the grasp") are false by design now and re-stated as U10 (a:unknown 1/u on the walk,
1/u² at the arrival, 1/u² on the grasp tick — no dip — 1/u³ one step into the carry) and U5'' (base ratio a:b
1000, evidence ratio 100: a's new stretch is empty, b's new `place` phase is an observation). All nine PASS.

## 3. The three re-trigger cases (criterion 2; `retrigger.md`)

| condition | ticks | I4c | I4d | `[meta]` in the window |
|---|---|---|---|---|
| s00_on | 108 → 109 (arrival) → 111–112 (grasp) → 113 | 0.905 → 0.905 → **0.498** → 0.905, `theta_crossed` 113 | 0.905 → 0.986 → 0.986 → 0.995 | none |
| s20_on | 86 → 87 → 89–90 → 91 | 0.905 → 0.905 → **0.498** → 0.905, `theta_crossed` 91 | 0.905 → 0.986 → 0.986 → 0.995 | none |
| s30_on | 95 → 96 → 98–99 → 100 | 0.905 → 0.905 → **0.498** → 0.905, `theta_crossed` 100 | 0.905 → 0.986 → 0.986 → 0.995 | none |

The chain, s00_on: the walk's stretch (81–108) is at odds 1/u; at the arrival (109) it folds as 1/u and the
`pick_up` phase opens at 1/u — odds 100, 0.986; at the grasp (111) `pick_up` folds as 1/u and the carry's
stretch is empty — odds 100, unchanged; at the first step (113) the carry pays its 1/u — odds 1000, 0.995.
Nothing crosses θ twice.

## 4. Attribution — every difference from I4c (`diffs/*_base_to_new.txt`)

One change; `nofold` reproduces I4c byte-for-byte, so every difference is this change or the meta-planner
reacting to it.

| condition | differences | mechanism |
|---|---|---|
| s00_on, s20_on, s30_on | after every first fold the true task reads 0.986–0.995 instead of 0.905 (s00_on 43–77, 109–141; s20_on 24–53, 87–121; s30_on 41–73, 96–120); the grasp dips gone; `theta_crossed` 113 / 91 / 100 gone. Reveals 11/81, 6/57, 21/77 unchanged. | the ceiling 1/(1+uⁿ); the fold keeps u |
| s30_off | same rise after each fold (item_3 0.895 → 0.995 from 41, item_7 from 100); reveals 28 / 87 unchanged; no `[meta]` change. | as above |
| s00_off | item_2's reveal **117 → 109** (pre-grasp, the arrival's fold); then **0.939 → 0.652 (111–112) → 0.947 (113) → 0.703 (114) → 0.754 (115)**: `theta_crossed` at 109, 113 and 115 (one in I4c, at 117). The robot's completions unchanged. | §6(a) |
| s20_off | item_3's first-task reveal **31 → 20** (pre-grasp; the arrival's fold separates it from the two collinear decoys: 0.363 → 0.850); crossings 20, 24, 30; item_2's **96 → 87** (pre-grasp), crossings 87, 91, 95. The meta-planner re-decides at 20/24/29/30 and 87–103; the robot's item_4 delivery **52 → 60**, item_6 **136 → 144**. | §6(a); the cascade is the meta-planner's |
| s40_off, s40_on | coffee's crossing 143 / 135 unchanged; from 153 (the `move_to` fold, `wait_at` open) coffee 0.898 → **0.984**; segment 3 identical through 269 (no fold); at 270 item_6 **0.083 → 0.474** (the 539 cm stretch folds as ×0.09, `pick_up` opens at ×10), 272 unchanged, 274 **0.896** — item_6 revealed post-grasp, new `theta_crossed` 274 (the robot re-decides item_5; its own deliveries unchanged). at_272: `unknown` 0.520 (item_6 0.474), was 0.911 (0.083). wrong-θ ticks incl. `unknown` 112 → 51 (on), 101 → 40 (off): item_6 wins segment 4 from 274. | §6(b) |

## 5. I4c's results (criterion 4) and the working region (criterion 5)

| result | I4c | I4d |
|---|---|---|
| next-task reveals prior-on | s00 81, s20 57, s30 77 (pre-grasp) | **unchanged** |
| next-task reveals prior-off | s00 117, s20 96, s30 87 | s30 87 unchanged; **s00 109, s20 87** — earlier, pre-grasp, by the arrival's fold (§6(a)) |
| coffee crossing | 135 / 143 | **unchanged** (no fold in segment 2 before 153) |
| the 63 wrong-task ticks | gone | **still gone**; the 11 of item_6 at 203–213 unchanged (no fold in 3a) |
| 3b retraction | 0.790 → 0.083 | **unchanged** |
| s30 first reveal | 28 / 21 pre-grasp | **unchanged** |
| TODO-53 | ac 0.001 at 272, `most_likely` 3 ticks in 184–271 | **unchanged**; item_6 itself now 0.474 at 272 and 0.896 at 274 (§6(b)) |

Working region: `region.md` is byte-identical to I4c's. The closed form evaluates windows with no fold
(segment 2 to 153, segment 3 to 270) from the uniform base, and the correction changes nothing there: coffee
prior-on crosses in all 25 cells, prior-off fails in the same 6 cells at β ≤ 0.007; the segment-3 counts are
the same. First-task reveals at the shipped constants prior-on unchanged (I4b's grid was prior-on). The
region moves neither way. What the closed form does not cover — every tick after a fold — is where the
correction acts, and there it raises the true task (0.986, 0.995) and, prior-off, produces §6(a).

## 6. Unexpected — reported, not fixed

**(a) Prior-off, three `theta_crossed` per recognition.** s00_off 109 / 113 / 115; s20_off 20 / 24 / 30 and
87 / 91 / 95. The producer is the rivals' phase structure under the carry, not the true task's fold:

| tick (s00_off) | human | item_2 | item_4 (rival) | what happened |
|---|---|---|---|---|
| 108 | walk | 0.600 | 0.337 | item_4's excess growing |
| 109 | arrival | **0.939** ↑θ | 0.049 | item_2's `move_to` folds as 1/u, `pick_up` opens at 1/u |
| 111–112 | grasp | **0.652** ↓ | 0.338 | item_4 flips to `deliver_with_return`: `move_to(shelf_2)` already holds, `place(item_2, shelf_2)` opens — no graded signal, an observation, 1/u; item_2's carry stretch is empty |
| 113 | first step | **0.947** ↑θ | 0.049 | item_2 pays 1/u; item_4 regresses to `move_to(shelf_2)` (`place` folds as 1/u, kept), its new stretch empty |
| 114 | second step | **0.703** ↓ | 0.293 | item_4's fresh stretch is non-empty at L ≈ 0.85 — 15 cm from shelf_2, a zero-excess start (TODO-61) |
| 115– | walk | 0.754 ↑θ … 0.887 | 0.242 … 0.109 | item_4's excess grows |

In I4c the same two bumps existed but item_2 was below θ until 117, so they were invisible at the interface.
The correction lifts the true task above θ at its arrival, and the bumps become crossings. Two ingredients,
both outside this task: a rival's `deliver_with_return` phases (`place` back on the shelf, then a regress) are
scored as observations the human never made — TODO-55 (e)'s question whether that method is the right
prediction for a rival at all; and the fresh stretch's L ≈ 1 from its first step — TODO-61. Prior-on there is
no live rival with a flip, and no such crossing. Not a reason to touch the correction: the invariant is
exactly what it says, and the rival's 1/u for `place` is point 3 of the accounting.

**(b) A refuted approach is forgiven after one action's worth of observations.** s40, item_6: the 539 cm
detour of 3b is ×0.09 (L/u = 0.009/0.1); the `pick_up` phase at shelf_6 is ×10, the first step of the carry
×10 — odds 0.09 → 0.9 → 9, and item_6 is `most_likely` at 0.896 from 274. Point 2 of the accounting, in
action; it also means the unmodelled segment 3 → 4 boundary (I4b §8(c)) now costs two observations rather
than the rest of the episode. Note that the grasp event itself (hit, ×1.0) is worth nothing here; the two
no-graded-signal / zero-excess observations around it are worth ×100.

**(c) s20_off's first-task reveal moves from 31 (post-grasp) to 20 (pre-grasp).** The arrival's fold separates
item_3 from the two collinear decoys (0.363 → 0.850) — the movement channel now does at the arrival what
I4b §6 said only an ungated completion charge could do at the grasp. A first-task result changed by a
correction aimed at the fold; recorded.

**(d) Cascade.** s20_off's meta-planner re-decides at every new crossing; the robot's item_4 delivery moves
52 → 60 and item_6's 136 → 144. The recognizer's completions list changes accordingly (60, 144). Meta-planner
behaviour, not touched.

## 7. Open

TODO-61, untouched by decision, now with two more instances (§6(a) tick 114, §6(b)). TODO-55 (e), the
domain question, now with an interface consequence (§6(a)). TODO-48's crossing rule meets the prior-off
triple crossings. The unmodelled segment 3 → 4 boundary. The stationarity channel (deferred).

SUPERSEDING NOTE (T-H1, 25 Sept 2026): the script here predates T-H1 and no longer imports (`DomainModel`, `DomainKnowledgeBase`, `StepCall`, a directly constructed `TaskSchema` were replaced by `shared/knowledge.py` and the typed tree); the record stands at its commit.
