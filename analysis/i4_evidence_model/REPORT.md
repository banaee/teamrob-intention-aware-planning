# I4 — the evidence model: excess-path likelihood, detection reliability, a stated `unknown`

Built on `1669011` (I3). Sweep: s00 (300 steps), s20 (200), s30 (200), s40 (400) × assignment_prior
off/on, `PYTHONHASHSEED=0`, interpreter `~/python-envs/teamrob-sp4-env/bin/python`. scenario_10 stays
dropped (TODO-52). Baselines recorded at `1669011` before any edit (`baseline/`), byte-identical on the
four regression greps to I3's `new/` in all eight conditions.

**The one-paragraph result.** The excess-path likelihood does what the design says on every stretch it
is given: a hypothesis whose expected action the agent walks straight at keeps likelihood 1, every
other hypothesis is charged by the distance it has wasted, and the first task of every scenario is
revealed mid-approach, before the grasp, in seven of eight conditions (the eighth, s20_off, has two
decoys on the far side of the target that the approach cannot separate). The `unknown` constant works
as designed: it caps confidence at 1/(1+u) and wins every stretch that fits no task. What the design
as specified does NOT do is recognise any task after the observed agent's first one — not `coffee_break`
in s40 (criterion 1), not the retraction in segment 3b (criterion 3, trivially met at the floor), not
item_6 in segment 4 — because a hypothesis's origin is where it began expecting its current action
(t = 0 for every task the agent has not yet started) and every closed phase is folded permanently, so
by the first release every remaining hypothesis carries the whole first task as wasted path. The
diagnostic answer to "which part failed" is therefore **the phase state across a task boundary**: not
the trajectory evidence (coffee's incremental excess during its own walk is exactly 0 cm), not the
`unknown` constant (no value rescues it; §4.2), not the hypothesis space. Two analysis-only what-ifs
that move every origin — and, in the second, the prior — to the observed agent's task boundary put
`coffee_break` at 0.90 in both prior settings by the mechanism the design intends (§6), and they are
TODO-53's named alternative and TODO-55's reading (b), both deferred by decision, so they are measured
here and not shipped.

## How to read this directory

| File | Content |
|---|---|
| `check_i4.py` | The harness. `--unit`: U1–U6. `--sweep abs` / `--sweep frac` / `--sweep abs fine`: the joint grids on the prior-on subset (s40, s30, s00), 4 processes. `--final --variants`: the eight conditions at the shipped constants (instrumented logs cmp'd against `run_mesa.py`'s) plus the six analysis-only variants; writes `summary.md`, `metrics.csv` and the CSVs. |
| `sweep_abs.csv`, `sweep_frac.csv`, `sweep_abs_fine.csv` | One row per (β, u, condition) with every derived metric. `pivot.py <csv> [s40 s30 s00 max]` prints them as β × u grids (§4). |
| `summary.md`, `metrics.csv` | The final matrix: per condition and variant, θ crossings (`!` = winner ≠ truth), first reveal per human task (pre-/post-grasp), wrong-θ ticks, the s40 segment metrics. |
| `trace.csv` | Per condition/variant/tick: segment, truth, human state, `most_likely`, confidence, the distribution. |
| `excess.csv` | Per condition/variant/tick/hypothesis: expected action, **excess path (cm)**, evidence base, belief. Pure geometry for the excess column (independent of β and u). |
| `chain.py` | `chain.py <tag> <hyp> <from> <to>`: the causal chain from `excess.csv` + `trace.csv` — excess, the likelihood it produced, base, posterior, strongest competitor, P(unknown) per tick (§6). |
| `expected_actions.csv`, `phase_advances.csv`, `completion_events.csv`, `completions.csv` | As in I3, with the origin's odometer reading added. |
| `baseline/`, `new/`, `logs_instrumented/<variant>/` | S0 = I3 (`run_mesa.py` at `1669011`); new = HEAD (`run_mesa.py`); the harness's logs per variant. **Not in git** (`*.log`); `stages.sh` regenerates all of them in about five minutes. |
| `diffs/` | `diff_ir.py` (I2's): base → S1 (`rawlogistic`, the spec's literal logistic) → new, base → new, and new → each what-if, per condition. |

Variants (monkeypatches in `check_i4.py`, none shipped): `rawlogistic` (S1: the logistic as literally
specified, 0.5 at zero excess), `costdif2` (the `walked` term dropped), `ungated` (TODO-56),
`ownshelf` (TODO-55 (c)), `reset_origin` (every live origin moves to the agent at a retirement —
TODO-53's alternative), `reset_boundary` (`reset_origin` plus the evidence state reset to uniform over
the live keys and `unknown` — TODO-55 (b)).

---

## 1. What changed and where

| what | where |
|---|---|
| The parameter set, each with a stated meaning: `BETA` (detour tolerance, 1/cm), `UNKNOWN_LIKELIHOOD` (the constant likelihood under `unknown`; the confidence ceiling 1/(1+u)), `DETECTION_HIT_RATE` / `DETECTION_FALSE_ALARM_RATE` (the completion detector), `PERFECT_FIT_LIKELIHOOD` (= 1.0, derived: the value at zero excess). `straight_line_cost` (the default C), `logistic_of_excess`, `excess_path_likelihood(walked, origin, pos, target, cost)` registered as `"excess_path"`. DELETED: `HIGH_LIKELIHOOD`, `LOW_LIKELIHOOD`, `NEUTRAL_LIKELIHOOD`, `direction_consistency_likelihood`, `"directional"`. | `shared/likelihood_functions.py` (rewritten) |
| A per-observed-agent odometer (`_odometer`, `_last_pos`: Σ straight-line steps between consecutive observed positions, from the priming observation) and `_origin_odo[key]` beside `_origin[key]`, set and reset at the same two places; `walked = odometer − _origin_odo[key]`. `_progress_likelihood` takes `walked`, memoises by (evaluator, origin, walked, target) and calls the evaluator with the injected `path_cost`. `unnorm[UNKNOWN] = base × UNKNOWN_LIKELIHOOD`. The first-observation tick and the advance tick score the perfect-fit value (zero excess by construction). No-evaluator actions score the perfect-fit value. `IntentionRecognizer(..., path_cost=None)`. Docstrings. | `shared/recognizer.py` (`__init__`, `update`, `_completion_likelihood`, `_progress_likelihood`) |
| `move_to.progress_evaluator = "excess_path"` (was `"directional"`). | `domains/kitting/actions.py` (one word) |

Nothing in `mesa_sim/`, `shared/planner.py`, `shared/target_resolution.py`, `shared/meta_planner.py`.
Human and robot per-step lines are byte-identical to baseline in all eight conditions. Unchanged by
instruction: the phase model, the terminal pin, the assignment mask, BELIEF_FLOOR, θ, the meta-planner,
the context weights, the fixture, the completion-channel gate (§8).

**Two departures from the spec as written, each measured before being taken:**

1. **The logistic is normalised to 1 at zero excess** (`L = 2/(1+e^{βΔC})`, not `1/(1+e^{βΔC})`). With
   the literal form a phase with nothing wrong folds 0.5 into the evidence when it closes, and every
   phase advance halves the hypothesis against `unknown` (whose value is never folded): measured as
   s40's positive control dropping 0.83 → 0.71 at its own grasp tick with the raw form (u = 0.05),
   and in the staged replay (`rawlogistic` → new, §3) as s30_on's item_3 at 0.550 vs 0.902 at tick 39
   and s00_off / s20_off never reaching θ at all (max 0.68 / 0.55). The factor 2 is a constant and
   cancels everywhere except against `unknown` (where it is absorbed by the u sweep) and in the fold,
   where it is the difference between "a completed phase costs nothing" and "a completed phase costs
   ×0.5". The normalised form makes the fold continuous: U4 checks that an advance whose closing phase
   had zero excess leaves the evidence against `unknown` unchanged.
2. **Hypotheses with no graded signal score the perfect-fit value, not a separate NEUTRAL.** With the
   likelihood in (0, 1] there is no middle to put a NEUTRAL in; a hypothesis expecting `pick_up`, `place`
   or `wait_at` is one whose agent is within reach of where that action happens (otherwise the walk
   would have regressed to the approach, a derived phase change), and standing there fits perfectly.
   The stationary-tick NEUTRAL of the cosine kernel is gone too: a tick with no movement leaves the
   excess where it was, which is exactly "replace, do not multiply".

The completion channel: `DETECTION_HIT_RATE = 1.0`, `DETECTION_FALSE_ALARM_RATE = 1e-3`. In Mesa the
simulator's report is the ground truth, so these are stated, not tuned: every completion is reported,
none is invented; the false-alarm rate is non-zero only so that a refuted hypothesis keeps a
recoverable base (the floor's rationale), and it is not load-bearing anywhere in the sweep — no two
hypotheses expect a grasp on the same tick in any current layout (`completion_events.csv`: 16 firings,
all hits, as in I3). A consequence worth stating plainly: under the gate, a grasp is no longer
evidence. The grasped item's hypothesis is multiplied by 1.0 and the rivals, being movement
expectants, are not judged; I3's ×4 at the grasp tick is gone, and the approach has to carry the
reveal (it does — §5, criterion 5; and see §8 for what the ungated reading now gives).

## 2. Verification

- Eight conditions, no traceback, no `not decomposable` warning. `check_i4.py --unit`: U1–U6 PASS
  (`summary.md`). Instrumented logs equal `run_mesa.py`'s on `[IR]`/`[IR-dist]`/`[meta]`/`[meta-cand]`
  in all eight.
- Hash-seed independence: s40_on byte-identical on the four greps under `PYTHONHASHSEED` 0/1/7.
- Wall time unchanged (s40, 400 steps: 2.6 s). dock_loading registry imports.
- Likelihood sharing: progress calls / evaluations 510/426, 220/212, 564/428, 176/168, 596/458,
  195/187, 1773/1567, 1009/971 — the same counts as I3 except s30_off (626/488 → 596/458: the robot's
  schedule changed, §3), so the cost per tick is the cosine kernel's. Completion calls 2/2 everywhere.

## 3. Attribution of every difference, by stage

Stages: S0 = I3 (`baseline/`); S1 = I4 with the raw logistic (`logs_instrumented/rawlogistic/`);
new = HEAD. `diffs/*_base_to_s1raw.txt`, `*_s1raw_to_new.txt`, `*_base_to_new.txt`.

**S0 → S1 — the evidence model (kernel + constants).** Every tick of every condition changes (a
different likelihood), so the attribution is by mechanism, each read off `excess.csv`:

1. *First approach.* Under the cosine kernel a decoy 42° off the heading scored 3.0 against 4.0; under
   excess path it is charged by its wasted distance, which grows with every step (s30_on item_7: 76 cm
   at tick 10, 198 at 20, 582 at the grasp; s00_on item_2: 221 cm at tick 11, 1205 at the grasp).
   The first-task reveal therefore moves from the grasp/carry to mid-approach: s00 43/41 → 39/11,
   s20 24/22 → 31/6, s30 41/39 → 28/21, s40 62/62 → 19/19 (off/on). Prior-off is later than prior-on
   in every layout because it has more live decoys, some of them on the path.
2. *The grasp tick.* I3's ×4 is gone (hit rate 1.0 against gated rivals at 1.0): the grasped item's
   belief does not move at the grasp (s30_on 0.9015 at 38 and 39). In s20_off this is the one condition
   where the reveal now comes AFTER the grasp: item_6 and item_4 lie beyond item_3 on the same bearing
   (excess 11 and 61 cm at the grasp, belief 0.34 and 0.26 against item_3's 0.36), the grasp does not
   separate them, and the carry does (their excess 78 cm at 26, 277 cm at 31 → 0.086/0.064; item_3
   0.771 at 31; base 24).
3. *The carry.* Every rival's method flips to `deliver_with_return` at the grasp (unchanged) and its
   approach phase is folded at its final excess — 582 cm → ×0.006 (s30_on item_7), 1205 cm → ×1e-5
   (s00_on item_2), 1957 cm → ×3e-9 (s40 item_6) — where I3 folded a chord at ≥ ×0.1. During the carry
   the rival's expected `move_to(shelf_X)` is charged again (s30_on item_7 1239 cm at 73). TODO-55's
   ≈ ×0.1 per carry is now ≈ ×1e-8 per task (§8).
4. *After the release.* With every rival folded to ≈ 0 and the delivered item pinned, `unknown` holds
   0.993–0.995 for the rest of every run (`unknown_when_idle` = 0.995). The "wrong-θ ticks" column of
   `summary.md` (66 / 70 / 49 / 174) is this: `unknown` ≥ θ while the human does its second task,
   never a wrong task above θ (the parenthesised task count is 0 in all eight). I3's second crossings
   (113 / 111 / 91 / 100 / 98) are all gone, and `unknown`'s 136 crossing in s20_off (TODO-54) is gone
   with them, only because `unknown` is already at 0.995 from 91.
5. *s40.* Segment 1 as above (item_3 0.904 from tick 19). From 115 on, everything is `unknown` (0.993):
   coffee's excess is 2144 cm before its walk begins and stays 2144 cm throughout it (its origin is
   t = 0 and its walk is efficient, so no increment); `ac_activation`'s is 2373 → 5664 cm; item_6's base
   carries the two folds above. §6 has the chains. TODO-53's asymmetry is closed and inverted: the
   stuck origin now over-charges instead of under-charging.

**S1 → new — the normalisation.** Output-only in effect: every difference is at a phase advance or in
its aftermath. First-task reveals move earlier by 2–3 ticks (s00_on 13 → 11, s30_on 24 → 21,
s40 22 → 19) and s00_off / s20_off, which never reached θ under S1 (item_3 max 0.68 / 0.55: three
advances, ×0.125), reach it at 39 / 31. The largest single change is the pick_up phase closing at the
grasp (s30_on t=39: item_3 0.550 → 0.902; s40_on t=113: `unknown` 0.612 → item_3 0.904).

**Robot behaviour** (`[meta]` diffs): the first `theta_crossed` moves with the reveal in every
condition (the robot's winner at the trigger is unchanged: item_6 / item_4 / item_2 / item_4 as before);
the second `theta_crossed` (on the human's second task) disappears in all eight; because the
projections are built earlier, `task_committed` / `no_current_task` triggers and the robot's own
completions shift by up to 10 ticks (s30: "all tasks complete" 168/167 → 158/159; s20_on 144 → 132).
No `[meta]` winner differs. `[meta-cand]` conflict counts differ where the timing does.

## 4. The joint sweep

Subset: s40_on, s30_on, s00_on (the fixture, the mid-approach case, the no-wrong-reveal case),
coarse grid first, fine grid inside the region it located; the full matrix once at the chosen values
(§5). Grids: `pivot.py sweep_abs.csv`, `pivot.py sweep_frac.csv`, `pivot.py sweep_abs_fine.csv`.

### 4.1 Absolute β (1/cm) × u — coarse

First-task reveal tick (s40 / s30 / s00; grasp at 60 / 39 / 41; "—" = never):

| β \ u | 0.01 | 0.02 | 0.05 | 0.1 | 0.2 | 0.35 | 0.5 |
|---|---|---|---|---|---|---|---|
| 0.001 | — / — / 59† | — / — / 61† | — / — / 64† | — / — / 71† | — / — / — | — / — / — | — / — / — |
| 0.002 | 51 / 50† / 30 | 52 / 51† / 30 | 54 / 53† / 32 | 57 / 56† / 35 | 84† / 65† / 49† | — / — / — | — / — / — |
| 0.005 | 27 / 28 / 15 | 27 / 28 / 16 | 28 / 29 / 16 | 30 / 31 / 18 | 35 / 36 / 21 | — / — / — | — / — / — |
| 0.01 | 16 / 18 / 9 | 16 / 19 / 9 | 17 / 19 / 10 | **19 / 21 / 11** | 22 / 24 / 13 | — | — |
| 0.02 | 9 / 11 / 5 | 9 / 11 / 5 | 10 / 12 / 6 | 11 / 13 / 6 | 13 / 16 / 8 | — | — |
| 0.05 | 4 / 5 / 2 | 4 / 5 / 2 | 4 / 6 / 2 | 5 / 6 / 3 | 6 / 8 / 4 | — | — |
| 0.1 | 2 / 2 / 1 | 2 / 3 / 1 | 2 / 3 / 1 | 2 / 3 / 1 | 3 / 4 / 2 | — | — |

† post-grasp. u ≥ 0.35: the ceiling 1/(1+u) ≤ 0.74 < θ, nothing ever crosses (max 0.74 / 0.66).

s40_on, the fixture's own criteria (coffee max in segment 2; item_6 through 3b; `ac_activation`
`most_likely` ticks in 184–271; belief at item_6's grasp, 272):

| β \ u | 0.01 | 0.02 | 0.05 | 0.1 | 0.2 |
|---|---|---|---|---|---|
| 0.001 | coffee 0.66; item_6 0.43→0.46; ac 29 ticks; 272: item_6 0.56 | 0.64; 0.39→0.40; 29; item_6 0.47 | 0.58; 0.31→0.28; 14; unknown 0.54 | 0.51; 0.22→0.19; 0; unknown 0.70 | 0.41; 0.15→0.11; 0; unknown 0.82 |
| 0.002 | 0.68; 0.06→0.03; 0; unknown 0.96 | 0.55; 0.03→0.01; 0; 0.98 | 0.34; 0.01→0.01; 0; 0.99 | 0.21; 0.01→0.00; 0; 0.99 | 0.12; 0.00; 0; 0.99 |
| ≥ 0.005 | coffee ≤ 0.004; item_6 0.001→0.001; ac 0 ticks; 272: unknown 0.993 (all cells) | | | | |

No cell has `coffee_break` ≥ θ; no cell has a wrong task ≥ θ in s40; the two cells with coffee > 0.6
(β ≤ 0.002, u ≤ 0.02) have `ac_activation` `most_likely` for 29 ticks and s30's first task revealed
after its grasp. Wrong task crossings anywhere in the subset: only β = 0.001–0.002 with u ≤ 0.02
(s30: item_7 at 74, the tick of item_3's release; s00: none).

### 4.2 Why no absolute β works for both, in numbers

Two scale requirements pull apart. (i) The first-task decoy must be refuted before the grasp: s30's
item_7 has 200 cm of excess at tick 20 and 582 at the grasp, so β·200 ≳ 2.5 (β ≳ 0.005) for a reveal
by mid-approach. (ii) A task the agent does LATER must survive the first task: coffee enters segment 2
with 2144 cm of excess from a t = 0 origin, `ac_activation` with 2373, and item_6 with two folds
totalling 3997 cm; for coffee to beat `unknown` 3 : 1 it needs L(2144) ≥ 3u, i.e. β ≲ 0.001 even at
u = 0.01 — and then `ac_activation` (L(2373)) is within a factor 1.6 of it and wins segment 3 for
29 ticks. The two regions are a factor ≥ 5 apart in β and do not meet; lowering u does not help
because the competitor of a stuck-origin task is another stuck-origin task, not `unknown`. This is
the phase state, not the kernel: the same kernel with the origins moved to the release tick reveals
coffee in 10 ticks (§6).

### 4.3 Fractional β (excess as a fraction of C(origin, target))

| β_f \ u | 0.01 | 0.02 | 0.05 | 0.1 | 0.2 |
|---|---|---|---|---|---|
| 0.2 | coffee **0.80**; s30 49†; s00 49†; ac 88 ticks | 0.79; 50†; 49†; 88 | **0.77**; 50†; 50†; 88 | 0.73; 51†; 51†; 41 | 0.66; 54†; 54†; 0 |
| 0.5 | **0.96**; 44†; 34; 0 | **0.94**; 44†; 35; 0 | **0.88**; 45†; 37; 0 | **0.80**; 45†; 44†; 0 | 0.67; 46†; 45†; 0 |
| 1 | **0.93**; 43†; 21; 0 | **0.86**; 43†; 21; 0 | 0.72; 43†; 22; 0 | 0.57; 43†; 24; 0 | 0.40; 44†; 29; 0 |
| 2 | 0.50; 42†; 13 | 0.33; 42†; 13 | 0.17; 42†; 13 | 0.09; 42†; 15 | 0.05; 42†; 18 |
| 5 | 0.00; 23; 6 | 0.00; 23; 6 | 0.00; 24; 7 | 0.00; 26; 7 | 0.00; 30; 9 |
| 10, 20 | 0.00; 15 / 8; 3 / 2 (pre-grasp) | | | | |

The fractional form DOES produce coffee crossings (bold), in a band β_f ∈ [0.2, 1] × u ≤ 0.1, and the
reason is worth stating because it is not the mechanism the design intends: coffee's reference length
is C(start, coffee) = 812 cm, so its 2144 cm of excess is a 2.6× detour, while `ac_activation`'s
reference is 300 cm (its 2373 cm is 7.9×) and item_6's carry-phase reference is the 30–50 cm between
the grasp position and shelf_3 (its 2040 cm of carry excess is a 50× detour and buries it outright).
Coffee wins by having the longest direct distance among the stuck-origin hypotheses — a fact about the
layout, not about the walk. The same band puts s30's first-task reveal after its grasp (43–45 vs 39)
and makes `ac_activation` `most_likely` for 88 ticks of segment 3 at β_f = 0.2. The band where the
first-task criteria hold (β_f ≥ 5) has coffee at 0.00. So the fractional reading has no working
region either, and it has a defect the absolute reading does not: the reference length goes to zero
whenever an origin sits near the target (every `deliver_with_return` carry phase, every `place` /
`pick_up` regress at 30 cm), and a 100 cm excess there is an infinite detour. **Verdict: absolute**,
with the scale dependence recorded (TODO-28's class): β is in cm and a layout twice as large needs
half the β. A scale-invariant form would have to normalise by a layout-level length (the workspace
diagonal, the mean inter-target distance), not by the per-hypothesis direct cost.

### 4.4 The working region and its width

For the criteria the design CAN meet — first task revealed pre-grasp in all three subset conditions,
no wrong task at θ anywhere — the region is β ∈ [0.005, 0.1] × u ∈ [0.01, 0.2] on the coarse grid
(25 of 49 cells), and every cell of the fine grid β ∈ {0.005, 0.007, 0.01, 0.014, 0.02} ×
u ∈ {0.05, 0.07, 0.1, 0.14, 0.2}. Inside it the only thing that moves is the reveal tick, smoothly:
about one tick per 0.05 of u and about 3–6 ticks per grid step of β (s30: 29/24/19/16/12 at
u = 0.05 for the five fine βs; 19/20/21/22/24 across the five us at β = 0.01). No cliff, no cell
where a neighbour differs in kind. **Chosen: β = 0.01 /cm, u = 0.1**, the centre of the region, with
these meanings: 100 cm of wasted path costs ×0.54 and 300 cm ×0.095; a target for which the agent has
wasted ≈ 294 cm is no better than unexplained (L = u); the confidence ceiling is 0.909. β = 0.01 is the
lowest fine-grid value that reveals s40's positive control in the first third of its 1209 cm approach
(tick 19) while tolerating the geometric slop of a 30 cm proximity threshold and shelf slots (a
100 cm excess is still 0.54). Higher β (0.05–0.1) reveals in 2–5 ticks, i.e. after 40–100 cm of
walking, which is the slop itself. For the coffee criterion the working region is **empty** under
absolute β and a **narrow, layout-shaped band** under fractional β (§4.3) — both are findings about the
phase state, §4.2, not results to report around.

## 5. Acceptance (the eight criteria), at β = 0.01, u = 0.1, full matrix

| # | criterion | outcome | evidence |
|---|---|---|---|
| 1 | `coffee_break` crosses θ on s40 | **NO — and not reachable under any β, u** | max 0.001 in both settings at the shipped values; sweep max 0.68 (β = 0.002, u = 0.01, with ac `most_likely` for 29 ticks elsewhere). Coffee's excess is 2144 cm at 118 and 2144 cm at 154: its walk adds nothing, and nothing it does can remove what its t = 0 origin charged. §4.2, §6. Under the what-ifs (origins at the boundary) it is 0.904 / 0.898 (on) and 0.904 / 0.779 (off), crossing at 125 / 135 / 143 — by the intended chain. |
| 2 | no `deliver_item` ≥ θ in segment 2 | yes | `deliver_max_seg2` 0.001 / 0.001; also true in every sweep cell (max 0.38 at β = 0.001). |
| 3 | item_6 FALLS through 3b | trivially (0.001 → 0.001) | item_6's excess grows 550 → 1088 cm through 3b (L 0.008 → 0.000) exactly as the design says, but its base is ≈ 0 from the two folds of segment 1, so the fall is invisible at the floor. With the base restored (`reset_boundary`) the rise-and-fall is the fixture's: 0.47 → 0.79 in 3a (excess 0 — the walk IS a walk to shelf_6), 0.80 → 0.083 in 3b as the excess goes 28 → 539 cm (§6). Not a defect; the shape the fixture was built for. |
| 4 | TODO-53 closed | **yes** | `ac_activation`: excess 2373 cm at 118, 3539 at 154, 5048 at 272; `most_likely` for 0 ticks in 184–271 (I3: 88 ticks at 0.45–0.69); 0.001 at item_6's grasp (I3: 0.48–0.53). The stuck origin is charged for the whole path — and so is every other never-advanced hypothesis, which is criterion 1's failure. |
| 5 | s30 reveals mid-approach | **yes** | s30_on item_3 crosses at 21 (grasp 39; 0.761), s30_off at 28 (0.75+); item_7's excess 214 cm at 21. Every first task is pre-grasp except s20_off (31, grasp 22: the on-path decoys, §3.2). |
| 6 | no new confidently wrong reveals in s00 / s20 | **yes** | wrong-task θ ticks 0 in all eight conditions; the only new ≥ θ stretches are `unknown` after the first release (§3.4). |
| 7 | every difference attributed | §3, `diffs/`, `excess.csv`, `chain.py`. | |
| 8 | θ = 0.75 reachable? | **yes, for a first task: ceiling 1/(1+u) = 0.909**, reached: s40 0.904 with two foreseeable hypotheses in the space (F1's 0.569 came from pinning, which is gone — the foreseeable rivals are now refuted by their own excess, 1278 and 2328 cm at the grasp); s00/s20/s30 0.905. `unknown` reaches 0.993–0.995. For any later task: **no**, at any β, u (§4.2). θ itself untouched. Reachability under the what-if: 0.90 (coffee, both), 0.82 (item_6 at 268, s40_off). |

TODO-54 (`unknown` crossing θ on a pin) does not occur in the sweep because `unknown` is already
above θ from the first release; it would return the moment later tasks become recognisable.

## 6. The causal chains (`chain.py`)

Excess in cm; L = 2/(1+e^{0.01·excess}); the base is the evidence with folds in; "other" is the
strongest live competitor. s40_on unless stated.

**coffee_break over segment 2, shipped code.** Origin (100, 550) from the priming tick.

| step | segment | excess | L | base | P(coffee) | strongest other | P(unknown) |
|---|---|---|---|---|---|---|---|
| 114 | 1 (carry) | 2143.8 | 0.000 | 0.91 | 0.001 | item_3 0.904 | 0.093 |
| 115 | release | 2143.8 | 0.000 | 10 | 0.001 | unknown 0.997 | 0.997 |
| 118–150 | 2 (walk) | 2143.8 (constant) | 0.000 | 10 | 0.001 | unknown 0.997 | 0.997 |
| 154–183 | 2 (wait) | — (`wait_at`, no graded signal) | 1 | 0 (fold ×0.000) | 0.001 | unknown 0.997 | 0.997 |

The excess does not move during the walk: `walked` grows by exactly what C(pos, coffee) shrinks. The
claim "coffee gains support because its excess falls relative to the alternatives" is refuted for the
shipped code — nothing's excess falls; every alternative's grows (item_6 10 → 550 cm, ac 2373 → 3539),
which would lift coffee if coffee's own value were not 0.000. Prior-off identical (`unknown` 0.994).

**coffee_break over segment 2, `reset_origin` (what-if).** Every origin moved to the table at 115.

| step | excess | L | base | P(coffee) | strongest other | P(unknown) |
|---|---|---|---|---|---|---|
| 116 | 0.0 | 1.000 | 0.48 | 0.474 | ac 0.474 | 0.051 |
| 120 | 0.0 | 1.000 | 0.57 | 0.570 | ac 0.368 | 0.061 |
| 125 | 0.0 | 1.000 | 0.76 | **0.759** | ac 0.160 | 0.080 |
| 130 | 0.0 | 1.000 | 0.87 | 0.866 | unknown 0.091 | 0.091 |
| 145–183 | 0.0 / wait | 1 | 0.91 | 0.904 | unknown 0.094 | 0.094 |

Here the chain is the intended one: coffee's excess stays 0, `ac_activation`'s grows from 0 at the
table at 1.8 cm per cm walked (the switch is 100° off the coffee bearing), item_6 is at the floor
(its base is still the two folds), and coffee rises to the ceiling. `reset_boundary` (base also reset)
is the same shape from a lower start (0.32 → 0.757 at 135 → 0.898); prior-off it reaches 0.762 at 143
and is knocked back to 0.34 at 145 because the ROBOT's delivery of item_4 retires a hypothesis and the
what-if resets the prior on every retirement — the prior-off caveat of any boundary mechanism that
cannot tell whose completion it saw.

**item_6 over segment 3, shipped code.** Origin at the table (115).

| step | segment | excess | L | base | P(item_6) | P(unknown) |
|---|---|---|---|---|---|---|
| 187–206 | 3a (toward shelf_6) | 549.6 → 549.8 | 0.008 | ≈ 0 | 0.001 | 0.998 |
| 210 | 3b (turn) | 578.1 | 0.006 | ≈ 0 | 0.001 | 0.998 |
| 216 | 3b | 758.1 | 0.001 | ≈ 0 | 0.001 | 0.998 |
| 227 | 3b end | 1088.2 | 0.000 | ≈ 0 | 0.001 | 0.998 |

The excess is flat through 3a (the human walks exactly toward shelf_6 — no waste) and rises through
3b, so L retracts as designed; the posterior cannot show it from a base of 3e-9 × 1e-9.

**item_6 over segment 3, `reset_boundary` (what-if).** Origins and prior reset at 184 (coffee retires).

| step | segment | excess | L | base | P(item_6) | strongest other | P(unknown) |
|---|---|---|---|---|---|---|---|
| 187 | 3a | 0.0 | 1.000 | 0.49 | 0.485 | ac 0.462 | 0.053 |
| 200 | 3a | 0.1 | 1.000 | 0.70 | 0.699 | ac 0.226 | 0.075 |
| 206 | 3a end | 0.2 | 0.999 | 0.79 | **0.790** | ac 0.126 | 0.084 |
| 210 | 3b | 28.5 | 0.858 | 0.94 | 0.799 | ac 0.103 | 0.098 |
| 213 | 3b | 116.4 | 0.476 | 1.64 | 0.775 | unknown 0.168 | 0.168 |
| 216 | 3b | 208.5 | 0.221 | 3.0 | 0.663 | unknown 0.305 | 0.305 |
| 220 | 3b | 336.7 | 0.067 | 5.9 | 0.393 | unknown 0.594 | 0.594 |
| 227 | 3b end | 538.6 | 0.009 | 9.2 | 0.083 | unknown 0.915 | 0.915 |

Rise while the expected action fits (3a, θ crossed at 203 — the fixture is built to produce this:
a walk toward shelf_6 is a walk toward shelf_6), retraction as soon as the excess grows (3b), `unknown`
winning by the end of the turn. Non-monotonic and correct. Prior-off the same shape with item_5
(14° off) tracking item_6 through 3a (0.35 vs 0.33 at 203) and outlasting it into 3b (0.46 at 216),
`unknown` at 0.754 by 227. And item_6 in segment 4 under this what-if: prior-off it crosses at 268
(pre-grasp, 0.82); prior-on it stays at 0.08 because its segment-3 excess (539 cm) is not reset
(no hypothesis retires at the wander waypoints — there is no boundary the recognizer can see between
segment 3 and segment 4).

## 7. TODO-56 — the completion-channel gate, re-checked under the new constants

Variant `ungated` (every expected action judged at a discrete tick): crossings identical to the shipped
code in seven of eight conditions; s20_off's reveal moves from 31 to **22, the grasp tick** (the two
on-path decoys that the approach could not separate are charged the false-alarm rate, ×1e-3, at the
grasp). Completion calls 10/8, 4/4, 14/10, 4/4, 14/10, 4/4, 18/15, 10/10 (vs 2/2 gated). I3's
pathology — `unknown` taking ×10 against every task at every event and ending at 0.96–0.99 — does not
occur, because `unknown`'s likelihood is a per-tick constant that is never multiplied into its base
while the false-alarm rate multiplies into the rivals'. `unknown` is at 0.995 after every release in
both readings, for the reason in §3.4, not because of the gate. The measurement no longer rejects the
ungated reading; it favours it slightly (one earlier reveal, no cost). The gate stays as instructed;
the decision is now open on its merits (the generative argument: a walker does not emit GRASP) rather
than blocked by the `unknown` asymmetry. Recorded in TODO-56.

## 8. TODO-55 — re-measured, not settled

Under reading (a), the shipped code: the rival's charge per task is no longer the ≈ ×0.1 cliff but the
product of two folds — the first approach at its final excess and the carry phase's `move_to(shelf_X)`
at its final excess: s00_on item_2 ×1.1e-5 (1205 cm) then ×≈ 3e-6 (1319 cm); s30_on item_7 ×0.006
(582 cm) then ×≈ 8e-6 (1239 cm); s40 item_6 ×3e-9 then ×1e-9. Next-task reveal ticks under (a): **never,
in all eight conditions** (I3: at the grasp, 111 / 89 / 98). Variant `ownshelf` (reading (c), rivals
decomposed as if nothing were held): identical — never in all eight; s20_off 32 vs 31 — because the
rival's t = 0 origin then accumulates the whole first task as one excess (2358 cm at the release for
s40's item_6) instead of two folds; the carry-method charge (TODO-51) is no longer the binding one.
Reading (b), the what-if `reset_boundary`: next-task reveals s00_on **80** (pre-grasp, grasp 111),
s20_on **56** (89), s30_on **76** (98); prior-off 117† / 96† / 96 (post-grasp for s00/s20 — the
reset fires at the robot's completions too, and the human's second approach in s00_off starts while
the robot's delivery has just re-flattened the prior), with three wrong crossings prior-off (s20_off
item_7 at 136, s30_off item_6 at 156, s40_off ac at 376 — all on a robot-triggered reset while the
human idles) and TODO-52's crash in s20_off at 142. Readings (d) and (e) not measured (both need
changes outside the recognizer). Evidence that settles it, from the task's own criterion: the approach
after a release is NOT decisive before the grasp under (a) — it is not decisive at all — so (a) does not
stand, and the candidates are (b) (measured: works prior-on, needs a boundary the recognizer can
attribute to the observed agent for prior-off), (d) and (e). (c) is out. No reading chosen.

## 9. Sensitivity of the chosen constants

- β: ±40% (0.007–0.014) moves every first-task reveal by ≤ 5 ticks and changes no crossing's winner.
  Below 0.005 s30's first task is post-grasp; above 0.05 a reveal follows 40–100 cm of walking.
- u: 0.05–0.2 moves the reveals by ≤ 3 ticks; u ≥ 1/3 makes θ unreachable by construction
  (ceiling 1/(1+u)).
- Detection rates: not load-bearing (no simultaneous grasp expectations in any layout; U5 shows the
  ×1000 when there are).
- PROXIMITY_THRESHOLD (30 cm, world-state builder): decides when `at` holds, hence every phase
  advance and every origin; a hypothesis regresses to its approach when the agent leaves the 30 cm
  disc. It sets the geometric slop β must tolerate (a 30 cm excess at β = 0.01 is ×0.85).

## Flagged, not fixed (outside scope)

- `domains/dock_loading/actions.py` still names `progress_evaluator="directional"`, which no longer
  exists in the registry; the domain imports (the lookup is at call time) and would score its movement
  actions at the perfect-fit value if run. One-word fix when the domain is revived.
- `shared/recognizer.py`: `CONFIDENCE_THRESHOLD` unused (I1 O8); the commented-out old
  `build_hypothesis_space`; `_history` unbounded — as before.
- `shared/meta_planner.py`: TODO-52's crash reproduced in the `reset_boundary` what-if (s20_off, 142).
- `CLAUDE.md`'s regression note still says tie order flaps without `PYTHONHASHSEED`; the recognizer
  has been seed-independent since I2 (re-verified here); other consumers unchecked.
- `docs/io_contracts.md` §2.1/2.2 not updated (the task named the two docs that were).

## 10. Hand-off (what the commit history does not say)

**(a) The kernel is not the open problem; the boundary is.** Every number in §4–6 says the same
thing: the excess-path likelihood ranks and values hypotheses correctly within a task, and the
recognizer has no notion of the observed agent's task ENDING and the next one STARTING. A never-advanced
hypothesis's origin is the priming tick; a rival's evidence is the product of every phase it ever
lost. Both are correct for a fixed intention and both are wrong for a human who does one task after
another. The two what-ifs isolate the two halves: `reset_origin` fixes the origins (coffee 0.90) and
leaves the folds (item_6 stays buried); `reset_boundary` fixes both (item_6 0.79 → 0.08 → 0.82 at its
own grasp). Whatever is shipped next is a decision about what a task boundary IS to the recognizer
(TODO-53's alternative, TODO-55 (b)/(d)/(e), TODO-57), not a kernel or a constant.

**(b) The boundary the recognizer can see is not the human's.** A retirement fires on the robot's
completions too (prior-off: s40 145 / 243 / 376, s20 52 / 136, s30 86 / 156, s00 31 / 93 / 166), and
segment 3's waypoints retire nothing. Any shipped mechanism needs the completion attributed to the
observed agent — the terminal action's completion held on a tick where that agent's microaction was
in the terminal action's vocabulary is the recognizer-side signal (RELEASE → `place`; `waited(human, ·)`
carries the agent in the predicate) — and a decision about what to do at an unmodelled boundary.

**(c) Numbers to reuse.** Excess in cm is geometry (`excess.csv` is identical for every β, u and for
every variant that does not move origins). First-approach decoy excess at the grasp: s00 1205 / 882 /
213 (item_2 / item_4 / item_6, prior-off), s20 730 / 61 / 12 / 578, s30 739 / 539 / 962 / 582,
s40 2328 (ac) / 1278 (coffee) / 1957 (item_6). Cross-task excess: 2144 (coffee, s40), 1821 (s30 item_7,
two folds), 2524 (s00 item_2, two folds).

**(d) The grasp is no longer a reveal.** Under the gate a hit multiplies by 1.0 and rivals are not
judged; the approach carries every reveal. If a grasp-tick reveal is wanted back, it is the ungated
reading (§7), not a constant.
