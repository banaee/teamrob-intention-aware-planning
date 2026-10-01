# I4c — episode semantics and the empty stretch

> Superseding note (T-L stage 3, 26 Sept 2026): the layout and scenario ids here are the old ones; `docs/rename_table.md` maps them to the serial ids. The scripts and records stay frozen at their commit.

> Superseding note (24 Sept 2026, the terminology ruling; `docs/glossary.md` §7, `docs/terminology_revision.md`): the harness (`analysis/i4_evidence_model/check_i4.py`, reused by I4c, I4d and I5) labels the human's ground truth `"unknown"` when the human's script is finished and for scenario_40's wander (`S40_TRUTH`: seg3a, seg3b, done). That is a WORLD fact written with the ROBOT's hypothesis name: read it as a finished work order, or unmodelled behaviour (the wander), respectively. So the "`!` = winner ≠ truth" marks and "wrong-θ" counts treat `unknown` leading as the correct reading of those ticks, and "unknown when idle" / `unknown_when_idle` is the `unknown` hypothesis's mass while the work order is finished (high by normalisation, not evidence of unmodelled behaviour).

Built on `d040e6d` (I4b). Sweep: s00 (300 steps), s20 (200), s30 (200), s40 (400) × assignment_prior off/on,
`PYTHONHASHSEED=0`, interpreter `~/python-envs/teamrob-sp4-env/bin/python`. scenario_10 stays dropped (TODO-52).
β = 0.01 /cm and u = 0.1 unchanged. Baseline = I4b's `run_mesa.py` logs at `d040e6d` (`baseline/`, the same files
as I4b's `new/`). No sweep was run; criterion 6 is answered in closed form from the logged excess (§6).

**The one-paragraph result.** Both decisions are implemented as specified and both do what the specification
says they do, with one interaction the spec did not name (§5) and one residue it invited (§4). Change 1 — an
empty stretch contributes no factor, and `unknown`'s constant applies only on a tick with an observation —
removes the 47 idle-tail wrong-task ticks on its own; change 2 — the belief re-initialises to the prior over the
live hypotheses at the observed agent's task boundary — removes the other 16 by giving `ac_activation` a live
competitor, and produces next-task reveals in every scenario (pre-grasp prior-on: s00 81, s20 57, s30 77) with
no wrong crossing and no crash. Coffee crosses θ at 135 prior-on and 143 prior-off, later than I4b's 125 for
the reason the spec predicted plus one it did not: the post-boundary zero-length stretch no longer scores as a
perfect fit, and item_6 — no longer buried under its previous-episode folds — is scored on segment 2's walk
from the prior and holds 0.32 at tick 118. Segment 3b's retraction is visible (item_6 0.790 → 0.083). Retention
across every boundary is uniform: at each of the 18 boundaries every live base equals 1/n on the boundary
tick, with 0 to 3 advances in the ended episode (§7). Eleven wrong-task ticks remain, all in s40_on
(item_6, 203–213), and they are produced by evidence — a 20-tick zero-excess walk on the bearing to shelf_6 —
not by either change; what they expose is that the likelihood's confirmation is length-blind (§4, TODO-61).
What change 1 exposes is that `unknown`'s u is charged per open observation and never folded, so "the belief
carries forward unchanged" holds for the base and not for the posterior: a lone live hypothesis dips from
0.905 to 0.498 on its grasp tick (§5, TODO-60). Neither is a reason to revisit the two decisions; both are
the likelihood form's, for I5. `neither` (both changes reverted) reproduces I4b byte-for-byte in all eight
conditions, so every difference from the baseline is one of the two changes or the meta-planner's response
to it (§9).

## How to read this directory

| File | Content |
|---|---|
| `check_i4c.py` | The matrix on I4's harness: variants `base` (shipped), `empty_only` (change 1 alone), `episode_only` (change 2 alone), `neither` (cmp'd against `baseline/`); unit checks U1–U6 (I4's) and U7–U9; `retention.csv`, `chains.md`, `region.md`. |
| `summary.md`, `metrics.csv` | Per condition and variant: boundaries, completions, crossings, reveals, wrong-θ ticks with the wrong-task ranges, the s40 segment metrics. |
| `retention.csv` | Criterion 7: at every boundary, per live hypothesis, advances in the ended episode, base the tick before, base on the boundary tick. |
| `chains.md` | Per-tick causal chains: coffee 113–160, item_6 183–275, ac 183–215 and 329–380, for s40 × {off, on} × {base, empty_only, episode_only}. The `factor` column says `none (empty)` where no factor was applied; `u paid` says whether `unknown` took its constant. |
| `region.md` | Criterion 6, closed form on I4b's fine grid from the logged excess (no run). |
| `trace.csv`, `excess.csv`, `phase_advances.csv`, `completions.csv`, `completion_events.csv` | As in I4/I4b, all variants; `excess.csv` has a `walked_cm` column, `trace.csv` a `u_factor` column. |
| `baseline/`, `new/`, `logs_instrumented/<variant>/`, `diffs/` | Not in git (`*.log`); `stages.sh` regenerates them (~8 min). `diffs/` is committed. |

---

## 1. What changed and where

| what | where |
|---|---|
| `_progress_likelihood` returns `None` for an EMPTY stretch (`walked <= 0` with an evaluator and a resolvable target). In `update()`: no factor for it, on an advance tick and on every later tick alike; the fold of a closing stretch multiplies only if it had a value; the first-observation tick applies no factor; `unknown` takes `UNKNOWN_LIKELIHOOD` only if some live hypothesis was scored this tick (`observed`). Actions without a graded signal keep the perfect-fit value (I4's rule, unchanged). | `shared/recognizer.py` (`update`, `_progress_likelihood`) |
| `_prior(live)`: the uniform prior over the given keys + `unknown` — the one prior, used at construction (over the admissible set) and at every boundary (over the live set). `_begin_episode(pos, odo)`: bases ← `_prior(live)`, evidence ← bases (every stretch empty), every origin ← the agent's position. Called by `update()` after normalisation when a retirement satisfies I4b's `_task_boundary` (unchanged); the boundary tick reports the re-initialised belief. `[IR-boundary]` says so. | `shared/recognizer.py` (`__init__`, `_prior`, `_begin_episode`, `update`) |
| Docstrings: the module's evidence-model and episode paragraphs, `update()`, `_base`. | `shared/recognizer.py` |
| `design_decisions.md`: the I4b entry ("reset the geometry, keep the belief") REPLACED. `TODOS_AND_DEFERRED.md`: TODO-59 closed, TODO-55 (b) closed by decision / (d) reported / (e) open, TODO-57 note, TODO-60 and TODO-61 new. | `docs/` |

Nothing else. β, u, θ, the likelihood form, the phase model, the pin's criterion, the boundary's criterion,
the gate, the meta-planner, the context weights: untouched. Unit checks: I4's U1–U6 PASS unchanged (U5's
"a:unknown unchanged at the grasp" holds because the rival's new action — `place` under
`deliver_with_return` — has no graded signal and is an observation); U7 (t = 0 and a stationary tick report
the prior exactly; the first step scores everyone), U8 (the boundary: b with one flip and c with an advance,
a false alarm and a flip hold bases 8.9e-3 and 9.1e-4 the tick before, 1/3 each on the boundary tick, the
output is the pinned prior, a stationary tick keeps it, one step scores from the new origin), U9 (a
completion the agent's phase did not reach pins and is no boundary: origin stays, a:unknown stays 1/u) PASS.
Instrumented `base` equals `run_mesa.py`'s logs in all eight; `neither` equals `baseline/` in all eight.

One implementation detail decided on method, reported: on a phase-advance tick the new action's (empty)
stretch is scored by the same rule as on every later tick — `_progress_likelihood(current, pos, 0.0, …)` —
rather than by a special "no factor" branch. The first draft used the branch and made the advance tick differ
from the stationary tick after it (s00_on 109: 0.498, 110: 0.905, no observation between them), which
violates the stationary-tick clause. The rule as shipped: an empty engaged stretch → no factor; an action
with no graded signal → the perfect-fit value; identical on the advance tick and after.

The logged tick 0 is unchanged in every condition: the robot primes the recognizer at construction
(`sim_agents.py`, the unlogged first update, where the prior now shows), and the logged step 0 is the
second update, after the human's first step.

## 2. coffee_break — the chain (`chains.md`; `chain.py`'s L column is replaced by `factor`)

s40_on. Prior over the live set at 115: {coffee, ac, item_6} + unknown = 0.25 each (item_3 pinned).

| step | seg | human | coffee excess | factor | base | P(coffee) | strongest other | P(unknown) | u paid |
|---|---|---|---|---|---|---|---|---|---|
| 113–114 | 1 | carry | 2143.8 | 0.000 | 0.91 | 0.001 | item_3 0.904 | 0.090 | u |
| 115 | release — **boundary** | | 0.0 | none (empty) | 0.25 | 0.249 | ac 0.249 (tie) | 0.249 | — |
| 116–117 | stationary | | 0.0 | none (empty) | 0.25 | 0.249 | ac 0.249 | 0.249 | — |
| 118 | 2 | walk | 0.0 | 1.000 | 0.34 | 0.340 | item_6 0.323 | 0.034 | u |
| 120 | 2 | walk | 0.0 | 1.000 | 0.39 | 0.383 | item_6 0.327 | 0.038 | u |
| 125 | 2 | walk | 0.0 | 1.000 | 0.52 | 0.520 | item_6 0.314 | 0.052 | u |
| 130 | 2 | walk | 0.0 | 1.000 | 0.66 | 0.653 | item_6 0.246 | 0.065 | u |
| 135 | 2 | walk | 0.0 | 1.000 | 0.76 | **0.757** | item_6 0.156 | 0.076 | u |
| 140 | 2 | walk | 0.0 | 1.000 | 0.83 | 0.830 | unknown 0.083 | 0.083 | u |
| 150 | 2 | walk | 0.0 | 1.000 | 0.90 | 0.892 | unknown 0.089 | 0.089 | u |
| 153–183 | 2 | wait | — | 1 (no graded signal) | 0.90 | 0.898 | unknown 0.090 | 0.090 | u |

The chain: at 115 every live base is 0.25 and every stretch is empty; nothing is scored and the belief IS the
prior for three ticks (I4b reported 0.474 here — 1.0 for two tasks against u — on nothing). From 118 coffee's
excess stays at 0 for the whole walk; `ac_activation`'s grows at 1.8 cm per cm walked as in I4b (0.462 at
187 of segment 3 is a different episode); item_6's — shelf_6 is roughly on the way — grows slowly (0.323 →
0.156 by 135), and it is item_6's presence that moves the crossing from 125 to 135: at 125, coffee's
posterior is 1/(1 + u + L_ac + L_item6) = 0.52 with L_item6 ≈ 0.6, where I4b had item_6 at the floor. Ceiling
0.898 instead of 0.904: item_6 never falls to zero (its excess at 150 is ≈ 300 cm, L ≈ 0.1) — the
ceiling with one unrefuted rival at 0.01 of coffee's mass.

s40_off: prior over 7 live (coffee, ac, item_4/5/6/7 + unknown) = 0.143 at 115–117; 0.174 at 118, 0.301 at
125, 0.588 at 135, crosses at **143** (0.762), 0.851 at 150, max 0.872 at 183. Same chain; four rivals
instead of one, all scored on the walk from the prior, item_5 the strongest (0.21 at 125). The reveal is later
because more of the prior mass has to be walked away from; nothing else differs.

The reveal moved later than 125 in both settings, for the reason the spec expected (the zero-length stretch
at 115–117 no longer scores 1.0 against u) and for one it did not name: change 2 re-primes every rival at the
prior, including the ones I4b had at the floor. A correct result, not a regression.

## 3. The 63 wrong-task ticks — the causal account

I4b's 63 (s40, both settings): `ac_activation` ≥ θ at 185–200 (16 ticks: 185–186 with the human standing at
the coffee machine, 187–200 walking toward wander_0) and at 332–378 (47 ticks, idle after item_6). In every
case ac was the lone surviving stuck hypothesis at zero excess, scored 1.0 against u = 0.1.

| ticks | I4b | `empty_only` (change 1) | `episode_only` (change 2) | shipped | removed by |
|---|---|---|---|---|---|
| 185–186 (standing) | ac 0.904 | gone (no observation → base ratio) | ac 0.474 = item_6 0.474 (I4b scoring on the re-initialised bases; tie, < θ) | prior 1/3 | change 1 |
| 187–200 (walking, 55° off the switch) | ac 0.90 → 0.76 | **ac 0.90 → 0.76 (14 ticks remain)** | gone: item_6 0.485 → 0.699 outcompetes ac from the first step | gone | change 2 |
| 332–378 (idle) | ac 0.904 | gone | **ac 0.904 (47 ticks remain; 48 with 331)** | prior 1/2 (on) / 1/3 → 1/2 (off, item_5 pinned at 376) | change 1 |

Under `episode_only` the 185–186 ticks read ac 0.474 = item_6 0.474 (two tasks at 1.0 against u after the
re-initialisation, I4b's scoring on the boundary tick); not a wrong-task tick by the metric because the tie
resolves to ac at 0.474 < θ, but the same defect. Under the shipped code all 63 are gone: 49 by change 1 and
14 by change 2, with 185–186 needing either.

**What remains: 11 ticks, s40_on only — d(item_6) 203–213 (crossing at 203, 0.756, peak 0.800 at 211).**
Produced by change 2 and by real evidence. From the prior at 184 (1/3 each), the human's walk to wander_0 lies
on the bearing to shelf_6: item_6's excess is 0.0 through 3a (0.2 cm at 206), ac's grows (9 cm at 187, 165 at
200, 245 at 206), so item_6 rises exactly as coffee did in segment 2 — 0.485 after ONE step (187), 0.603 at
195, 0.699 at 200, 0.756 at 203 — holds through the waypoint pause (206–209, the stretch is non-empty, the
value is what it was), and is undone by the turn: 28.5 cm at 210 (0.799), 116 cm at 213 (0.775), 209 at 216
(0.663), 337 at 220 (0.393), 436 at 223 (0.199, `unknown` crosses), 539 at 227 (0.083). Prior-off the same walk
peaks at 0.462 (no crossing): item_5 and item_7 are live at the prior and their excess grows only a little
faster than item_6's (item_5 0.348 at 205), so the mass is split. That is dilution, not evidence.

This is not the lone-survivor defect (item_6 has a competitor and `unknown` pays u on a real observation)
and not the fold asymmetry (every base was 1/3 at 184). It is what the excess-path likelihood says about a
walk that happens to point at a shelf: L = 1 from the first step, whether 15 cm or 300 cm of a 1,000 cm
approach has been covered. Confirmation is length-blind; only disconfirmation accumulates. Recorded as
TODO-61 — a candidate third defect, in the likelihood form (out of scope), not in either change. The
fixture's segment 3a is the ambiguous case the model accepts, and the 3b retraction is the model correcting
itself in 20 ticks; "approximately zero" was not pursued.

## 4. Segment 3b retraction (criterion 4)

Visible now, both settings: s40_on item_6 **0.790 → 0.083** (3b start → end), s40_off 0.388 → 0.068. I4b had
0.001 → 0.001 because item_6's base carried its segment-1 folds (×3e-9 × 1e-9) across both boundaries; under
episode-local those folds are discarded at 115 (and whatever segment 2 charged, at 184), so item_6 enters
segment 3 at the prior and the 539 cm of 3b excess is what moves it. Nothing carries it any more; the retraction
is carried by the open stretch alone. What still is not reset is the segment 3 → 4 boundary (no completion,
no boundary — I4b §8(c)): item_6 keeps its 539 cm into its own approach and sits at 0.083 through segment 4
and its own grasp (272: `unknown` 0.911, item_6 0.083), as in I4b. Unchanged, named.

## 5. Uniform retention (criterion 7) — and what the no-observation belief is

`retention.csv`, `base` rows: at each of the 18 boundaries every live hypothesis's base on the boundary tick
is 1/n (n = live + 1), whatever it held the tick before and however many times it advanced in the ended
episode:

| boundary | live hypotheses: advances in the ended episode → base the tick before → base at the boundary |
|---|---|
| s40_on 115 | ac 0 → 0.909 → 0.250; coffee 0 → 0.909 → 0.250; item_6 3 (60, 62, 115) → 0.000 → 0.250 |
| s40_on 184 | ac 0 → 0.902 → 0.333; item_6 0 → 0.902 → 0.333 |
| s40_off 115 | ac, coffee 0 → 0.909; item_4/5/6/7 3 each → 0.000; all → 0.143 |
| s00_off 78 | item_2 3 → 1.1e-5; item_4 3 → 2.7e-4; item_6 3 → 0.193; all → 0.250 |
| s30_off 74 | item_2/4/6/7 3 each → 1.1e-3 / 8.3e-3 / 1.2e-4 / 5.4e-3; all → 0.200 |

The `all_live_bases_equal` column is True in every `base` and `episode_only` row and False in 50 rows, all of
them `empty_only` / `neither` (I4b's mechanism keeps the bases). The base "the tick before" is in the
recognizer's common scale (Σ base·value = 1), which is why a never-advanced hypothesis with its whole charge
open reads 0.909 and a hypothesis with two folds reads 0.000 — the asymmetry I4b measured, now erased at the
boundary and only there.

**What the no-observation belief is.** On a tick with no observation the reported belief is the normalised
bases. After a boundary that is the prior. After a phase advance mid-episode it is the base ratio, and the
base ratio of a task with only perfect folds to `unknown` is 1:1, because `unknown`'s u is charged on the
open observation and never folded (I4's design: that is what makes 1/(1+u) a ceiling). So where the only
live hypothesis advances to an empty engaged stretch it dips: s00_on item_2 0.905 (110) → 0.498 (111, the
grasp; 112) → 0.905 (113, first step); s20_on 89–90; s30_on 98–99. Prior-off the rivals are mid-stretch, u is
paid, no dip. The dips are ticks 111–112 in the table below (`u_factor` 1.0 = `unknown` paid nothing):

| s00_on tick | 109 | 110 | 111 (grasp) | 112 | 113 |
|---|---|---|---|---|---|
| item_2 expects | pick_up (no graded signal) | pick_up | move_to(table), empty | empty | move_to, 15 cm |
| P(item_2) | 0.905 | 0.905 | 0.498 | 0.498 | 0.905 |

The spec's "the belief carries forward unchanged" therefore holds for the base — every fold and event
retained — and not for the previous tick's posterior, which contained a u that I4's model does not fold.
Change 1 is right (an empty stretch is not an observation); what it makes visible is TODO-60, in the
likelihood form. The recovery fires a second `theta_crossed` per reveal (s00_on 113, s20_on 91, s30_on 100)
and the meta-planner re-decides, without changing its winners (§9).

No-observation ticks per condition (`trace.csv`, `u_factor` = 1): s00_off 78–80, 142–172; s00_on 78–80,
111–112, 142–168; s20_off 54–56, 122–199; s20_on 54–56, 89–90, 122–199; s30_off 74–76, 121–163; s30_on 74–76,
98–99, 121–159; s40 115–117, 184–186, 331–378 (both). Every one is a boundary's stationary ticks, an idle tail,
or a lone-hypothesis advance.

## 6. Criteria 5 and 6 — I4's results, and the working region

**Criterion 5.** s30's mid-approach reveal: 28 prior-off / 21 prior-on, pre-grasp (grasp 39) — identical to
I4/I4b, as is every first-task reveal (s00 39/11, s20 31/6, s40 19/19): nothing before the first boundary
changes but the unlogged priming tick. TODO-53 closed: `ac_activation` is `most_likely` on 3 ticks in
184–271 (184–186, the prior at 1/3 with ac first in key order; 0.332 < θ), max 0.462 (187, one step), 0.001
at 272 (`unknown` 0.911). No delivery above θ in segment 2: deliver_max_seg2 = 0.332 prior-on (item_6 at
118), 0.230 prior-off.

**Criterion 6** (`region.md`; closed form: within a window with no advance and no event, P_t(k) =
L_β(e_k)/(Σ_j L_β(e_j) + u) from the uniform base, over the logged excess, which does not depend on β or u).
First-task criteria: unchanged from I4b's grid by construction (identical to the first boundary). Coffee
prior-on crosses θ in all 25 cells (126 at β = 0.02 to 153 at β = 0.005, u = 0.2; peak 0.75–0.95). Coffee
prior-off crosses in 19 of 25: not at β = 0.005 (peak 0.64–0.70) nor at (0.007, 0.2) — the four robot items
at the prior 1/7 are not walked away from fast enough under a tolerant β. **The region narrowed there**, and
the cause is change 2's prior over the whole live set: prior-off the robot's undelivered items are, for the
human's belief, legitimate candidates at the same prior as coffee, and a tolerant β keeps them alive. I4b's
cells had those items at the floor from their segment-1 folds — a wrong reason for a better number. Segment 3
wrong-task ticks (item_6 in 3a, prior-on): 2–21 per cell, monotone in β and u (the shipped cell 14, of which 2
are the closed form's own artefact at 270–271, where the run has item_6's 3b fold and the truth is item_6);
prior-off 0 everywhere (the artefact 2). The idle-tail and post-boundary ticks are at the prior in every cell
(no factor, no u), so the lone-survivor stretch I4b found in every cell is gone in every cell.

## 7. The boundary and the pin, seen apart

s40_off, idle after item_6 (331): prior over {ac, item_5} + unknown = 0.332 each, no observation; the robot
delivers item_5 at 376 → item_5 pinned, live set {ac} + unknown → 0.497 each, still no observation, no
re-initialisation, no boundary line. s00_off 142–172: {item_4} + unknown at 0.5 until the robot's 166
delivery, then `unknown` 0.999. s20_off 122–199 and s30_off 121–163 the same shape (`unknown when idle` 0.47,
0.34). Each looks odd in a log and is what the two criteria say: the world's completion shrinks the support,
only the observed agent's changes the episode. Not unified.

## 8. TODO-55

(b) adopted — it is §1's change 2. (d): within an episode a rival's method still flips under the carry and
its fold history differs from a never-advanced hypothesis's: s40 episode 1, item_6 advances at 60 (move_to
(item_6) → place(item_3, shelf_3)), 62 (→ move_to(shelf_3)) and 115 (→ move_to(item_6), the boundary tick),
and holds its two folds in its base (0.000 at 114) while coffee and ac hold 2144 and 2349 cm open (base 0.909,
value 0.000). Posterior consequence within the episode: none (all three 0.001 at 114); across the boundary:
none (0.25 each at 115). Every within-episode flip in the four scenarios (`phase_advances.csv`: 3 per rival
per episode, at the grasp, the departure from the shelf, and the release) is driven by the observed agent's
own `holding`, which ends at the boundary. In kitting the unevenness therefore never outlives the episode.
That is domain-specific and is recorded as such; the general question stays as stated in TODO-55 (d), with no
case in the current domain. (e) open, unchanged, a domain-model question.

## 9. Attribution of every difference from I4b (`diffs/*_base_to_new.txt`)

Checked mechanically: `neither` == `baseline/` on `[IR]`, `[IR-dist]`, `[meta]`, `[meta-cand]` in all eight,
so everything below is one of the two changes or the meta-planner reacting to a belief they changed.

| condition | differences | change |
|---|---|---|
| s00_off | 78–80 prior over {item_2, item_4, item_6} + u (0.25) instead of `unknown` 0.995; item_2 0.905 from 81, reveal **117** (post-grasp, grasp 111); 142–165 {item_4} + u at 0.5, 166– `unknown` 0.999 (the pin). `[meta]`: new `theta_crossed` 117 (item_4) and 166; all complete 168 → 172 (the robot's last delivery, item_4, 166 in both). | 2 (78–80 and 142–172 also 1: no u) |
| s00_on | 78–80 {item_2} + u at 0.498; item_2 0.905 from 81, reveal **81** (pre-grasp); dips 111–112 (0.498); 142–143 `unknown` 0.995 with the truth still labelled item_2 (harness labelling of the last boundary tick, 2 "wrong-θ" ticks). `[meta]`: new `theta_crossed` 81 (item_6) and 113 (item_4). | 2; the dips 1 (§5) |
| s20_off | 54–56 0.249; item_2 rises 0.331 → 0.499 (57–88), reveal **96** (post-grasp, grasp 89); 122–199 {item_6, item_7,…} + u. `[meta]`: new `theta_crossed` 96. | 2 (+1) |
| s20_on | 54–56 0.498; reveal **57** (pre-grasp); dips 89–90. `[meta]`: new `theta_crossed` 57, 91. | 2; dips 1 |
| s30_off | 74–76 0.200 over four robot items + item_7; item_7 reveal **87** (pre-grasp, grasp 98); 121–163 idle at the prior. `[meta]`: new `theta_crossed` 87 (winner item_2 — one tick after the robot's own item_2 completion at 86; flagged below), `task_committed` 89, `no_current_task` 88 → 93; the robot's item_4 delivery **156 → 161**, all complete 158 → 163. | 2 (+1); the robot's 5-tick delay is the meta-planner's re-decision at 87–93 |
| s30_on | 74–76 0.498; reveal **77** (pre-grasp); dips 98–99. `[meta]`: new `theta_crossed` 77, 100. | 2; dips 1 |
| s40_off | 115–117 0.143; coffee reveal 125 → **143**; 184–186 0.2; item_6 0.25 → 0.46 → 0.068 through segment 3 (no crossing); `unknown` crosses 214 → 226; 331–375 0.332, 376– 0.497. ac's 63 ticks gone. `[meta]`: `theta_crossed` 125 → 143, 214 → 226. | 2 (the reveal, the competitors), 1 (the prior ticks, the tail) |
| s40_on | 115–117 0.249; coffee 125 → **135**, ceiling 0.898; 184–186 0.332; item_6 0.485 → 0.800 → 0.083, crossing **203 (wrong, 11 ticks)**; `unknown` crosses 223; 331–378 0.497. `[meta]`: 125 → 135, 214 → 203 + 223. | 2, 1 as above; the 11 ticks: 2 + the evidence (§3) |

## 10. What remains open — for I5

- **TODO-60** — `unknown`'s u is per open observation and never folded; the no-observation belief is the base
  ratio, and a lone live hypothesis dips to 0.5 on its grasp tick (§5). Likelihood form.
- **TODO-61** — confirmation is length-blind: L(0) = 1 after one step; a walk that happens to point at a shelf
  is a reveal (§3). Likelihood form.
- The unmodelled boundary (segment 3 → 4; I4b §8(c)): item_6 carries its 539 cm into its own approach.
- The stationarity channel — deferred by the spec, not built: standing still as evidence against hypotheses
  that predict movement.
- TODO-55 (e), the domain question.
- The gate statement (I4b §6) now reads "unresettable within an episode": events are discarded with the base
  at a boundary. The gate decision stands; the statement's scope changed.

## Flagged, not fixed

- s30_off `[meta]` step 87: `theta_crossed` names `deliver_item(item_2)` as the robot's winner one tick after
  the robot's own delivery of item_2 (86); `no_current_task` re-selects item_4 at 93. Meta-planner; out of scope.
- `theta_crossed` re-fires on the recovery from a lone-hypothesis dip (s00_on 113, s20_on 91, s30_on 100):
  TODO-48's crossing rule meets TODO-60.
- TODO-52's crash returned under `episode_only` (s20_off 142) — the lone-survivor wrong crossing at 136 feeds
  it. Not reachable under the shipped code in these scenarios; still latent.
- The harness labels the last boundary tick and the one after with the human's finished task (2 "wrong-θ"
  ticks prior-on in s00/s20/s30, `unknown` 0.995 vs a truth of the just-completed task). A labelling artefact.

SUPERSEDING NOTE (T-H1, 25 Sept 2026): the script here predates T-H1 and no longer imports (`DomainModel`, `DomainKnowledgeBase`, `StepCall`, a directly constructed `TaskSchema` were replaced by `shared/knowledge.py` and the typed tree); the record stands at its commit.
