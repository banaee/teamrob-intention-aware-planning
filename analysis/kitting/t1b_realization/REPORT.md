# T1b — What realization would produce (measurement only)

> Superseding note (T-L stage 3, 26 Sept 2026): the layout and scenario ids here are the old ones; `docs/rename_table.md` maps them to the serial ids. The scripts and records stay frozen at their commit.

Code at HEAD `51b7cee` (main). `shared/` untouched. Eight runs, `PYTHONHASHSEED=0`, the T5
sweep conditions (s00, s20, s30, s40 × assignment prior off/on; scenario_10 dropped, TODO-52).
No decision, default, threshold or cost was changed; nothing below proposes a value.

Units: durations in ticks (1 tick = 20 cm of motion, stationary action 1 tick), distances in cm.
δ = total hold. T_r = the candidate's projected duration, T_h = the human projection's end (both
from the trigger tick). s = separation, the free parameter.

## How to read this directory

| File | Content |
|---|---|
| `measure.py` | Runs the eight conditions with T1's instance-level wrappers on the live `MetaPlanner`/`Projector`; writes `captures.json` (git-ignored) and byte-comparable instrumented logs (git-ignored). |
| `realize.py` | The throwaway realizer: closed-form `earliest_violation`, the design loop (`greedy`, with a `literal` mode), the same policy at its minimal hold (`exact`), T1's whole-trajectory shift (`whole`), and sampled cross-checks. Not the implementation. |
| `analyze.py` | `captures.json` → every table. `--summary-only` re-renders `summary.md` from the CSVs. |
| `spotcheck.py` | Hand arithmetic for s20 prior-on step 6, item_4, s = 30 (§Verification). |
| `rows.csv` | One row per (condition, trigger, candidate): 141 rows, with tags. |
| `a_realization.csv` | Row × separation (13 values): status, δ, holds, first violation, unassessed share, tail, all four realizers. 1716 rows. |
| `b_triggers_argmin.csv` | Per (condition, trigger, s): cost-only winner, realized winners, all-unrealizable flags, B2 reference columns. |
| `f_scale.csv` | Scale context per layout. |
| `checks.json` | The verification numbers. |
| `summary.md` | All tables, auto-generated; quoted selectively below. |

## Method

**Rows.** 76 fired triggers, 141 candidate projections (rows). Row classes, never pooled:
*primary* — the trigger's human projection was admitted (`projection=built`): 89 rows at 44
triggers; *counterfactual* — not admitted (`none(below_theta)`), realized against a projection of
that tick's below-θ `most_likely` built after `update()` returned: 43 rows at 19 triggers; *none* —
`most_likely = unknown`, no projection possible: 9 rows at 7 triggers. Tags: `hyp_matches_actual`
(the projected hypothesis is the human's actual scripted task at that tick; False when the human
has finished its script), `degenerate` (projected human path < 30 cm, T1's rule; none this time),
`is_current_task`, `robot_holding`, trigger reason. **Primary, correct-hypothesis rows: 87 at 43
triggers**, 74 distinct geometries (13 rows repeat across the prior on/off pair). The one
wrong-hypothesis primary trigger (s40_on 203: item_6 projected, human on the wander walk) and the
7 wrong-hypothesis counterfactual rows are reported separately.

**Separations.** s ∈ {5, 10, 20, 30, 40, 50, 75, 100, 150, 200, 300, 400, 600} cm. 5 is below the
executor's 30 cm "at" proximity; 600 is half a layout width and excludes most of the pool.

**Geometry.** `earliest_violation` is closed form: robot segment placed at t and human segment on
their overlap window have relative position A + Bτ; d²(τ) is a quadratic, no real root below s²
means no violation, the roots bound the violation interval. Intervals are merged across abutting
human segments. No sampling in any realizer. Sampling (0.01 tick) is used only to cross-check.

**Four realizations per row, same hold-only policy:**

- `greedy` — the design entry's loop, literally: `v = earliest_violation(segment at t)`; `None` →
  place; clear time past the horizon → **unresolved** (`none:beyond_horizon`, the task's rule,
  never counted as cleared); else `hold += clear − t; t = clear`. `clear` is the end of the merged
  violation interval of the segment *as placed*. When that interval is cut by the robot segment's
  own end while still open (the robot arrives inside s), `clear` is the segment end: the loop holds
  one segment duration and re-checks (flagged `segment_end_truncation`; extrapolating the root
  past the segment end would describe motion the robot never makes). **A hold is a position**: the
  stationary stretch at the segment's start is checked like any segment; a violation there is
  `none:hold_position_violated`.
- `literal` — the same loop, but on "clear time past the horizon" it breaks *and places* the
  segment (the pseudo-code's `# no human left`). The design text read without the task's rule.
- `exact` — the same per-segment policy (hold at the segment's start, then go) at its **minimal**
  hold: the earliest start t' on a 0.01-tick grid such that the hold [t, t'] at the start position
  is clear and the segment is clear over all of its part inside the horizon. This is the check on
  the greedy: same policy, no clear-time jump.
- `whole` — T1's single shift: hold δ at the trigger position (checked), then the whole trajectory
  unshifted; smallest δ on a 0.01-tick grid.

**Strict horizon rule, all four:** only [0, T_h] is assessed. A violation anywhere in it, including
one cut off by T_h, is a violation. Nothing after T_h is assessed. "Realizable" = no violation in
[0, T_h] after the holds.

**Tail.** T1's `human held at its end` variant, re-measured properly: the human is extended at its
final position and holds are capped at the original T_h (a hold ending after T_h is clearing by
outlasting). `clears_via_tail` = realizable within the horizon with δ > 0, but not realizable with
the human held at its end. `tail_lead` = ticks after T_h until the realized trajectory first comes
within s of the human's final position (None if the robot finishes first or never does).

**Cost.** Realized cost = T_r + δ (fractional ticks). The cost-only winner is the pure argmin of
projected cost over the pool in pool order (what B3 picks with no interference term). The *logged*
winner differs from it at 4 triggers (s20_off 20, s20_on 6, s30_off 28, s30_on 21), where the
superseded `min_safe_distance = 1.0` exclusion removed item_4 (T2's `min_dist = 0.0` cases); both
are in `b_triggers_argmin.csv`.

---

# DATA

## 1. Hold δ and realization status (primary, correct hypothesis, 87 rows per s)

`greedy` (design loop, strict horizon):

| s | realized | δ=0 | δ>0 | δ>0 min / med / max | max δ/T_r | clears via tail | hold position violated | beyond horizon |
|---|---|---|---|---|---|---|---|---|
| 5 | 83 | 83 | 0 | – | 0 | 0 | 2 | 2 |
| 10 | 83 | 83 | 0 | – | 0 | 0 | 2 | 2 |
| 20 | 86 | 83 | 3 | 2.43 / 29.15 / 29.15 | 0.87 | 3 | 0 | 1 |
| 30 | 86 | 82 | 4 | 2.21 / 16.05 / 29.15 | 0.87 | 4 | 0 | 1 |
| 40 | 86 | 81 | 5 | 2.65 / 8.11 / 29.15 | 0.87 | 5 | 0 | 1 |
| 50 | 84 | 81 | 3 | 8.66 / 29.15 / 29.15 | 0.87 | 3 | 2 | 1 |
| 75 | 83 | 80 | 3 | 9.71 / 29.15 / 29.15 | 0.87 | 3 | 3 | 1 |
| 100 | 82 | 78 | 4 | 10.64 / 26.55 / 29.15 | 0.87 | 4 | 3 | 2 |
| 150 | 69 | 65 | 4 | 3.77 / 13.72 / 26.37 | 0.39 | 3 | 15 | 3 |
| 200 | 62 | 56 | 6 | 8.34 / 12.63 / 48.28 | 0.73 | 4 | 20 | 5 |
| 300 | 47 | 45 | 2 | 32.38 / 35.88 / 39.38 | 0.68 | 2 | 33 | 7 |
| 400 | 36 | 35 | 1 | 21.40 | 0.24 | 1 | 44 | 7 |
| 600 | 14 | 13 | 1 | 23.35 | 0.26 | 1 | 58 | 15 |

`exact` (same policy, minimal hold) and `whole` (T1 shift):

| s | exact realized | exact δ>0 | exact δ>0 min / med / max | max δ/T_r | whole realized | whole δ>0 | whole δ>0 min / med / max |
|---|---|---|---|---|---|---|---|
| 5 | 85 | 2 | 0.25 / 0.25 / 0.25 | 0.005 | 87 | 4 | 0.25 / 1.15 / 2.05 |
| 10 | 85 | 2 | 0.50 / 0.50 / 0.50 | 0.011 | 87 | 4 | 0.50 / 1.40 / 2.30 |
| 20 | 87 | 4 | 1.00 / 1.90 / 2.80 | 0.084 | 87 | 4 | 1.00 / 1.90 / 2.80 |
| 30 | 87 | 5 | 0.56 / 1.50 / 3.30 | 0.098 | 87 | 5 | 0.56 / 1.50 / 3.30 |
| 40 | 87 | 6 | 0.40 / 2.00 / 3.80 | 0.113 | 87 | 6 | 0.40 / 2.00 / 3.80 |
| 50 | 85 | 4 | 1.13 / 3.40 / 4.30 | 0.128 | 85 | 4 | 1.13 / 3.40 / 4.30 |
| 75 | 84 | 4 | 2.96 / 4.65 / 5.55 | 0.166 | 84 | 4 | same |
| 100 | 84 | 6 | 0.73 / 5.90 / 15.49 | 0.203 | 84 | 6 | same |
| 150 | 72 | 7 | 0.09 / 2.49 / 19.56 | 0.199 | 74 | 9 | 0.09 / 3.23 / 19.56 |
| 200 | 66 | 10 | 1.18 / 3.45 / 23.63 | 0.278 | 66 | 10 | same |
| 300 | 53 | 8 | 0.88 / 4.98 / 31.77 | 0.536 | 53 | 8 | same |
| 400 | 40 | 5 | 4.85 / 8.78 / 13.55 | 0.469 | 40 | 5 | same |
| 600 | 20 | 7 | 1.87 / 8.18 / 15.10 | 0.238 | 20 | 7 | same |

`literal` differs from `greedy` only on the beyond-horizon rows: 2 / 2 / 1 / 1 / 1 / 1 / 1 / 2 / 3 /
5 / 7 / 7 / 15 rows (s = 5 … 600) are placed with an open violation at T_h and counted "realized"
with δ = 0 by the pseudo-code.

**Every row with a hold or a failure at s ≤ 100** (from `a_realization.csv`; the other 78 rows
have δ = 0 in all four realizers at every s ≤ 100):

| condition, step | candidate | current? | T_r / T_h | s | greedy | exact δ | whole δ | first violation: robot phase / human phase |
|---|---|---|---|---|---|---|---|---|
| s20_off 20, s20_on 6 | item_4 | yes | 33.5 / 34.3, 47.5 / 48.3 | 5, 10 | hold position violated at the placement | none (dead end at the placement) | 2.05, 2.30 | placement / carry |
| same | item_4 | yes | same | 20 – 100 | realized, δ = 29.15 (one carry duration; via tail) | 2.80 – 6.80 | = exact | carry / carry |
| s20_off 20 | item_7 | no | 87.0 / 34.3 | 40 – 100 | δ = 8.1 – 10.6 | 0.40 – 4.79 | = exact | approach / carry (crossing) |
| s20_on 6 | item_7 | no | 98.1 / 48.3 | 100 | δ = 23.94 | 15.49 | = exact | approach / carry (crossing) |
| s20_off 24 | item_4 | no | 35.0 / 29.7 | 100 | beyond horizon | 0.73 | 0.73 | carry / placement |
| s20_on 72 | item_7 | no | 89.0 / 49.6 | 100 | 3 holds (25.9 + 13.5 + 6.9), then hold position violated | none | none | approach from the table / carry |
| s30_off 28 | item_4 | yes | 47.1 / 46.1 | 5 – 100 | beyond horizon at every s | 0.25 – 5.00 (= s/20) | = exact | carry / carry (arrives at T_h) |
| s30_on 21 | item_4 | yes | 54.1 / 53.1 | 5, 10 | beyond horizon | 0.25, 0.50 | = exact | carry / placement |
| same | item_4 | yes | same | 20 – 40 | δ = 2.43 – 3.37 | 1.00 – 2.00 | = exact | approach / approach (mirror crossing) |
| same | item_4 and item_2 | – | – | 50, 100 | hold position violated at the start | none | none | the human passes the standing robot |
| s30_on 21 | item_2 | no | 65.8 / 53.1 | 30, 40 | δ = 2.21, 2.65 | 0.56, 1.31 | = exact | approach / approach |

Counterfactual rows (not admitted, correct hypothesis, 36 rows): greedy realizes 30 – 36 of 36 at
s ≤ 100 with 0 – 10 held rows; the held ones are the t = 0 item_4 rows in s00 / s20 / s30 (greedy
δ 22 – 29, exact 1.5 – 3.3). Wrong-hypothesis primary rows (2, s40_on 203): realized with δ = 0 up
to s = 50, one hold from 75. Counterfactual wrong-hypothesis rows (7): in `a_realization.csv`, not
summarised.

## 2. Where the holds sit

Greedy holds by phase of the held robot segment × the human's phase when the hold starts (primary,
correct; counts of holds, not rows):

| s | approach_shelf while human approaches | approach_shelf while human carries | carry_to_table while human carries | placement while human carries | pick_up | return_held_item | carry while human approaches / walks to coffee |
|---|---|---|---|---|---|---|---|
| 5, 10 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| 20 | 1 | 0 | 2 | 0 | 0 | 0 | 0 |
| 30 – 50 | 2 – 3 | 0 | 2 | 0 | 0 | 0 | 0 |
| 75, 100 | 4 – 5 | 2 | 2 | 0 | 0 | 0 | 0 |
| 150 | 12 | 12 | 0 | 0 | 2 | 0 | 1 |
| 200 | 16 | 13 | 0 | 0 | 0 | 3 | 3 |
| 300 – 600 | 19 – 25 | 8 – 10 | 0 | 0 | ≤ 1 | 6 – 19 | 4 – 6 |

First violation of the unheld projection (robot phase / human phase), s = 30: approach/approach 2
rows, carry/carry 3. s = 100: approach/approach 2, approach/carry 3, carry/carry 3,
carry/placement 1. Every carry/carry violation is a convergence into the kitting table; every
approach/carry one is the robot's approach crossing the human's carry path (item_7 in s20);
approach/approach is the s30 mirror crossing.

## 3. Why no realization

Greedy, primary correct, by the failing segment's phase: at s ≤ 100 the failures are
`beyond_horizon` on a carry (1 – 2 rows: s30_off 28 item_4 at every s, s20_off 24 item_4 at 100;
plus the two s20 item_4 rows at s = 5, 10) and `hold_position_violated` on a placement (s = 5, 10:
the two s20 item_4 rows, the human reaches the table during the robot's placement tick) or on an
approach (s = 50 – 100: the s30_on 21 crossing rows, s20_on 72 item_7). From s = 150 the failures
are dominated by `hold_position_violated` on approach_shelf (13, 16, 23, 29, 33 rows at 150 … 600)
and, from 200, on return_held_item and carry_to_table: the human's path passes within s of where
the robot stands at the trigger. `exact` fails on the same segments, minus the `beyond_horizon`
rows, which it realizes with small holds (0.25 – 13.55 ticks; table in §7).

## 4. Unassessed share, and what the hold does to it

Primary correct, greedy-realized rows. Share = (T_r + δ − T_h)⁺ / (T_r + δ).

| s | realized | share before, min / med / max | share after | held rows | widening (ticks), held rows, min / med / max |
|---|---|---|---|---|---|
| 5 – 10 | 83 | 0.00 / 0.46 / 0.94 | same | 0 | – |
| 20 – 100 | 82 – 86 | 0.00 / 0.45 / 0.94 | same medians | 3 – 5 | 2.2 – 10.6 / 8.1 – 28.4 / 28.4 |
| 150 – 200 | 62 – 69 | 0.00 / 0.50 / 0.94 | 0.50 – 0.51 | 4 – 6 | 0 / 12 – 14 / 26 – 48 |
| 300 – 600 | 14 – 47 | 0.00 – 0.33 / 0.63 – 0.77 / 0.94 | 0.65 – 0.78 | 1 – 2 | 21 – 39 |

At s = 30 the current-task rows have an unassessed share of 0.00 / 0.40 / 0.69 (min / med / max, 36
rows) and the alternatives 0.00 / 0.52 / 0.94 (51 rows).

Tail (human held at its final position, holds capped at T_h):

- **Every held row clears via the tail.** At every s ≤ 100, 0 of the 3 – 5 greedy-held rows, 0 of
  the exact-held rows and 0 of the whole-shifted rows remain realizable with the human held at its
  end. The same holds at 150 – 600 except 1 – 2 rows at 150 / 200 (whose hold is not at the table).
- Of the δ = 0 rows, 15 remain realizable with the human held at its end at every s ≤ 100 (14 at
  150, 12 at 200, 11, 7, 2 beyond): these are the rows where the robot finishes before T_h (s00_on
  11 / 81, s20_on 57, s30_on 77, s40 143 / 147 / 135) or the human's final position is not the
  table (s40 coffee-break projections). The other 63 – 68 δ = 0 rows come within s of the human's
  final position 0.01 – 78 ticks after T_h (median 22 – 28 ticks).
- For the s20 item_4 convergence rows at s = 30: greedy δ = 29.15 gives a tail lead of 25.9 ticks
  (the whole carry is pushed past T_h); exact and whole δ = 3.30 give a tail lead of 0.00 (the
  robot reaches s of the table exactly at T_h). All three "clear via tail".

## 5. Argmin over the pool

Admitted, correct-hypothesis triggers (43 per s). "≠ cost" = the realized winner differs from the
pure cost argmin.

| s | greedy ≠ cost | exact ≠ cost | whole ≠ cost | literal ≠ cost | greedy all-unrealizable | exact | whole | literal |
|---|---|---|---|---|---|---|---|---|
| 5, 10 | 4 | 2 | 0 | 2 | 0 | 0 | 0 | 0 |
| 20 – 75 | 3 | 0 | 0 | 2 | 0 (1 from 50) | 0 (1 from 50) | same | same |
| 100 | 4 | 0 | 0 | 2 | 1 | 1 | 1 | 1 |
| 150 | 7 | 4 | 2 | 4 | 8 | 8 | 8 | 8 |
| 200 | 4 | 2 | 2 | 2 | 12 | 11 | 11 | 10 |
| 300 | 7 | 2 | 2 | 2 | 18 | 17 | 17 | 16 |
| 400 | 4 | 0 | 0 | 0 | 24 | 24 | 24 | 21 |
| 600 | 6 | 2 | 2 | 2 | 33 | 31 | 31 | 22 |

Which triggers, at s ≤ 100:

- s = 5, 10 — greedy: s20_off 20 and s20_on 6 (item_4 → item_6: item_4's placement is violated;
  the current task loses), s30_off 28 and s30_on 21 (item_4 → item_2: item_4 beyond horizon). exact:
  only the two s20 triggers (item_4 has no feasible start; its carry can start at once, and then
  the placement at the table cannot be held). whole: none (item_4 realizes with δ = 2.05 / 2.30 and
  keeps winning). literal: the two s20 triggers (the placement hold, not a horizon break).
- s = 20 – 75 — greedy: s20_off 20 and s20_on 6 (item_4 realized cost 62.7 / 76.7 with δ = 29.15
  against item_6 at 56.1 / 65.3 → item_6), s30_off 28 (item_4 beyond horizon → item_2). At s30_on 21
  the greedy realizes item_4 with δ = 2.4 – 3.4 and item_4 keeps winning. exact and whole: **no
  winner changes** — item_4's minimal hold (2.8 – 5.6 ticks) never costs more than the 22.6 / 17.8 /
  12.2-tick margin to item_6 / item_2.
- s = 100 — greedy adds s20_off 24 (item_4 beyond horizon).
- From s = 150 the changes are mostly forced: the winner is the only realizable candidate (pool of
  2 – 3 with 1 – 2 realizable) — e.g. s00_off 39, s00_on 33 (item_6 unrealizable, item_4 wins) and
  s20_on 101 (item_4 → item_7).

Per-trigger first s at which the greedy winner changes: s20_off 20 and s20_on 6 → 5 (and at every
s up to 150 / 300); s30_off 28 → 5 (up to 100); s30_on 21 → 5 (at 5 and 10 only: item_4 realizes
at 20 – 40 and keeps winning, and the trigger is all-unrealizable from 50); s20_off 24 → 100;
s20_off 30, s00_off 39, s00_on 33, s20_on 101 → 150; s00 63, s30 48 → 300; s20_on 29 → 400;
s20_off 95 / 103, s40 19 / 98 → 600. 23 of 43 triggers never change winner before nothing
realizes, or never (`summary.md` §5).

Counterfactual triggers (14, correct hypothesis): greedy winner ≠ cost at 4 triggers at s ≤ 50 — the
t = 0 triggers of s20 and s30 in both prior settings, where item_4 (cost winner) is held 22 – 29
ticks by the greedy (exact 1.5 – 3.3) or fails at the placement; exact ≠ cost at 2 (s20 t = 0, s = 5,
10). No all-unrealizable case below s = 150.

## 6. All-unrealizable (condition, trigger)

Primary, correct hypothesis, 43 triggers per s. Greedy:

| s | all-unrealizable | of which pool size 1 | of which current task in pool | exact | whole |
|---|---|---|---|---|---|
| 5 – 40 | 0 | 0 | 0 | 0 | 0 |
| 50 – 100 | 1 (s30_on 21) | 0 | 1 | 1 | 1 |
| 150 | 8 | 6 | 7 | 8 | 8 |
| 200 | 12 | 6 | 10 | 11 | 11 |
| 300 | 18 | 8 | 14 | 17 | 17 |
| 400 | 24 | 8 | 19 | 24 | 24 |
| 600 | 33 | 10 | 28 | 31 | 31 |

The s ≤ 100 case is the s30_on 21 mirror crossing at s ≥ 50: the human's approach passes within s of
the robot's trigger position, so neither candidate's first segment can be held (hold position
violated) and no start on the grid is clear either. From 150 the cases are pools whose every
candidate starts with a walk past the human, or single-task pools (`theta_crossed` mid-task with an
empty queue: s00 109 / 113 / 115, s00_on 95, s40 274, s30 87 / 89).

## 7. Per-segment vs whole-trajectory (TODO-70)

Primary correct rows, per s:

| s | greedy realized, whole not | greedy not, whole realized | both realized and δ differ | greedy − whole, max | exact not, whole realized | exact vs whole δ differ |
|---|---|---|---|---|---|---|
| 5, 10 | 0 | 4 | 0 | – | 2 | 0 |
| 20 – 75 | 0 | 1 | 3 – 5 (all greedy > whole) | 23.6 – 26.4 | 0 | 0 |
| 100 | 0 | 2 | 4 | 22.4 | 0 | 0 |
| 150 | 0 | 5 | 4 | 14.6 | 2 | 0 |
| 200 – 600 | 0 | 4 – 6 | 1 – 6 | 7.6 – 43.4 | 0 | 0 |

- **exact and whole agree on δ in every row where both realize** (0 rows differ at any s, to the
  0.01 grid). exact fails where whole succeeds in 2 rows at s = 5, 10 and 2 at 150: the s20 item_4
  rows, whose per-segment policy places the carry at once and then finds the placement (s = 5, 10)
  or the pick-up (150) unholdable — a dead end the single shift avoids by shifting the whole plan
  (δ 2.05 / 2.30 / 9.30). Never the reverse.
- **greedy vs exact** (same policy): where both realize and differ, greedy > exact in every row
  (3 – 6 rows per s; median excess 5.4 – 24.9 ticks, max 43.4). greedy fails where exact realizes in
  1 – 6 rows per s (the beyond-horizon rows; exact δ 0.25 – 13.55). Never the reverse. The excess
  has two sources: (i) the hold is `clear − t`, the time from the segment's *start* to the end of
  the violation, not the length of the violation or the minimal shift — item_7's crossing at s = 100
  needs 15.49 ticks, the greedy holds 23.94 (violation at 21.2 – 23.9 from a start at 0); (ii) when
  the violation runs to the robot's arrival, the loop holds a full segment duration: item_4's carry,
  D = 29.15, needs 2.8 – 6.8 (segment-end truncations: 2 iterations per s up to 150, 5 – 33 beyond).

## 8. B2's reference (TODO-36): current-task rows at admitted, correct-hypothesis triggers

36 current-task rows per s (`b_triggers_argmin.csv`, `cur_*` columns; `summary.md` §8 lists s ∈
{10, 30, 50, 100, 200}). At every s ≤ 100:

- δ = 0 for 32 of the 36 (greedy) at every s ≤ 100 — the current task is not held at all; the
  realized winner keeps it in 31 of the 32, the exception being an alternative that is cheaper on
  plain cost anyway (s20_off 24: item_6 current at 52.1, item_4 at 35.0 → B3 switches without any
  hold, as the log did; at s = 100 item_4 is beyond the horizon there and item_6 is kept).
- The held / failed current-task rows and their references:

| condition, step | s | greedy δ (status) | exact δ | δ / T_r | δ / T_h | best alternative realized cost − current realized cost | T_h remaining |
|---|---|---|---|---|---|---|---|
| s20_off 20 item_4 (T_r 33.5) | 10 | hold position violated | none | – | – | item_6 56.1 vs – | 34.3 |
| | 30 – 100 | 29.15 | 3.3 – 6.8 | 0.87 (exact 0.10 – 0.20) | 0.85 (exact 0.10 – 0.20) | −6.5 (greedy); +19.3 … +15.8 (exact) | 34.3 |
| s20_on 6 item_4 (T_r 47.5) | 10 | hold position violated | none | – | – | item_6 65.3 vs – | 48.3 |
| | 30 – 100 | 29.15 | 3.3 – 6.8 | 0.61 (exact 0.07 – 0.14) | 0.60 (exact 0.07 – 0.14) | −11.4 (greedy); +14.5 … +11.0 (exact) | 48.3 |
| s30_off 28 item_4 (T_r 47.1) | 10 – 100 | beyond horizon | 0.5 – 5.0 | – (exact 0.01 – 0.11) | – (exact 0.01 – 0.11) | item_2 59.2 vs – (greedy); +11.7 … +7.2 (exact) | 46.1 |
| s30_on 21 item_4 (T_r 54.1) | 10 | beyond horizon | 0.5 | – | – | item_2 66.3 vs – | 53.1 |
| | 30 | 2.94 | 1.5 | 0.05 | 0.06 | +11.0 (item_2 held 2.2) | 53.1 |
| | 50 – 100 | hold position violated | none | – | – | none realizable | 53.1 |
| s00_on 81 item_6 (T_r 12.0) | 200 | 8.75 | 3.35 | 0.73 | 0.14 | +73.5 | 60.8 |
| s20_on 57 item_6 (T_r 12.9) | 200 | 8.91 | 3.28 | 0.69 | 0.14 | +101.8 | 64.6 |

The two references behave differently: δ / T_r is large when the task is nearly done (0.7 for a
12-tick remainder held 9 ticks) and small for the same hold on a long task; δ / T_h is 0.14 for both
of those rows because the human's horizon is long. Under exact holds every current-task δ at s ≤ 100
is ≤ 0.20 of T_r and ≤ 0.20 of T_h.

## 9. Scale (TODO-47)

| | env_layout0 (s00) | env_layout2 (s20) | env_layout3 (s30) | env_layout4 (s40) |
|---|---|---|---|---|
| space w × h, diagonal | 1000 × 800, 1281 | 1200 × 900, 1500 | 1000 × 800, 1281 | 2000 × 1200, 2332 |
| task-object bounding box | x[−400, 400] y[−300, 350] | x[−500, 450] y[−350, 400] | x[−400, 400] y[−300, 350] | x[−950, 950] y[−550, 550] |
| motion per tick / executor "at" proximity / sampler resolution | 20 / 30 / 1 | same | same | same |
| robot approach leg (cm) min / med / max | 112 / 521 / 820 | 47 / 791 / 1151 | 200 / 519 / 922 | 316 / 1120 / 2147 |
| robot carry leg | 462 / 716 / 716 | 575 / 820 / 875 | 664 / 680 / 763 | 11 / 951 / 1309 |
| human approach leg | 15 / 217 / 800 | 12 / 471 / 846 | 195 / 607 / 761 | 809 / 813 / 1189 |
| human carry leg | 207 / 602 / 716 | 369 / 613 / 875 | 427 / 633 / 680 | 328 / 1098 / 1151 |
| candidate duration T_r (ticks) | 24 / 55 / 80 | 30 / 58 / 103 | 34 / 54 / 86 | 2 / 112 / 163 |
| human horizon T_h (ticks) | 11 / 36 / 78 | 19 / 33 / 88 | 26 / 54 / 74 | 8 / 20 / 116 |
| robot–human distance at the trigger | 8 / 329 / 684 | 29 / 470 / 817 | 27 / 392 / 664 | 5 / 908 / 1502 |

In ticks of motion, s = 20 / 30 / 50 / 100 / 150 / 300 is 1 / 1.5 / 2.5 / 5 / 7.5 / 15 ticks; as a
fraction of the diagonal, s = 30 is 0.013 – 0.023 and s = 150 is 0.064 – 0.117. The exact hold for a
table convergence is (T_h − robot arrival) + s / 20 (spot check): s enters as s / speed.

---

# INTERPRETATION (labelled; not part of the measurements)

- **Where behaviour changes with s.** Below 20 cm nothing is held; the only failures are the two
  s20 convergence rows at the placement tick (arrival gap 0.8 ticks = 16 cm) and the s30 carry that
  ends exactly at T_h. Between 20 and 100 cm, 3 – 6 of 87 rows are held, all four realizers agree on
  *which* rows (the s20 convergence, the item_7 crossings, the s30 mirror crossing), and the exact
  hold is 0.4 – 6.8 ticks except item_7's crossing at 100 (15.5). At 150 cm the picture changes
  kind: failures become "the human walks past where the robot stands" (13 → 33 rows), and the
  all-unrealizable count goes from 1 to 8 → 33 of 43 triggers. In ticks, the transition sits between
  5 and 7.5 ticks of motion; in layout terms between ~0.07 and 0.1 of a diagonal.
- **The greedy as stated is not the policy it describes.** Its hold is measured from the segment
  start, and when the violation reaches the arrival it holds a full segment. On this data that
  makes the current task's hold 4 – 10× the minimal one and flips two argmins the minimal hold would
  not flip (s20_off 20, s20_on 6: exact keeps item_4 by 11 – 19 ticks; greedy drops it by 6 – 11).
  Whether the arrival lands before or after T_h decides between "hold a whole carry" (s20) and
  "unrealizable" (s30_off 28) for what is the same geometry (0.8 vs −0.0 tick gap). exact and whole,
  which do not have this artefact, agree with each other in every row they both realize.
- **Every hold in this data is a hold into the tail.** With the human held at its final position
  no held row realizes, at any s, under any of the three realizers, because every hold is at a
  table convergence or a crossing en route to the table, and the human's projection ends at the
  table. What a hold buys, as measured, is "be s short of the table when the assessment stops"; the
  0.00-tick tail lead of the exact hold says so literally. The design's "a hold WIDENS the
  unassessed share" is visible but small for exact (a 3-tick hold on a 33 – 48-tick task) and large
  for greedy (29 ticks, share 0.45 → 0.65).
- **The literal pseudo-code and the task's rule give opposite argmins** on the beyond-horizon rows
  (s30_off 28: literal keeps item_4 at δ = 0, strict switches to item_2). The row count is small
  (1 – 2 at s ≤ 100) but it is the current-task convergence case the design was written for.
- **B2.** With exact holds, every current-task δ at s ≤ 100 is ≤ 0.2 of T_r and of T_h, and B3's
  argmin keeps the current task in every held row where it was cheaper to begin with. The one row
  where the current task is dropped for a conflict reason at s ≤ 100 (s20_off 24 → item_4) is
  dropped on plain cost, as the log already does. On this data a δ-only gate would have nothing to
  escalate that B3 does not already decide the same way — but only 5 of 36 current-task rows are
  ever held, all in two fixtures.

# Anomalies

1. **Non-monotone in s (per-segment policy).** The s20 convergence rows (item_4, s20_off 20 / s20_on
   6) are unrealizable at s = 5, 10, realizable at 20 – 100, unrealizable again at 150 (pick-up). At
   small s the carry is clear, so it is placed at once and the placement tick at the table is then
   within s of the arriving human with nowhere to hold; at s ≥ 20 the carry itself is violated first
   and the hold sits at the shelf. The whole-trajectory shift is monotone (2.05, 2.30, 2.80 …).
2. **Arrival order decides the greedy's outcome.** Same geometry class, opposite results: s20 (robot
   arrives 0.8 ticks before T_h) → hold a whole carry; s30_off 28 (arrival at T_h) → beyond horizon,
   unrealizable at every s. The exact hold is s / 20 ticks in both.
3. **Logged winner ≠ cost argmin at 4 admitted triggers** (s20_off 20, s20_on 6, s30_off 28, s30_on
   21): the superseded `min_safe_distance = 1.0` exclusion is live in the baselines and already
   removes item_4 there. The report's "cost-only winner" is the pure argmin; the logged one is also
   in the CSV. The four are exactly the triggers where realization holds or fails the current task.
4. **Only two fixtures produce holds** at s ≤ 100 (scenario_20's convergence and item_7 crossing;
   scenario_30's mirror crossing); s00 and s40 rows are δ = 0 in every realizer until s = 150 – 200.
   TODO-47 (c)'s fixture gap stands: the only correct-hypothesis crossing on a *current* task is
   s30_on 21 (item_4 at s = 20 – 40), and it is all-unrealizable from 50.
5. **`hold_position_violated` on an approach at s ≥ 150 is the robot's trigger position, not a
   waiting choice.** The robot did not choose to stand there; the human's projected path passes
   within s of it. Hold-only has no answer; T1's "no hold position was within s at a tick that
   mattered" was a small-s statement.
6. **The counterfactual t = 0 rows carry the largest greedy holds in the data** (22 – 29 ticks for
   item_4 in s00, s20, s30) against projections the robot does not admit (confidence 0.16 – 0.51).
   Reported separately; not pooled.
7. **Nothing was found structurally or experimentally deadlocked.** The one structural limit: with the human's projection ending at the table and every candidate ending
   there, "realizable with the human held at its end" is false for all 87 rows at every s, so the
   tail question cannot be separated from the fixture design on this data.
8. **`shared/meta_planner.py` changed on disk during the session** (`theta` default 0.75 → 0.65 at
   17:02, after the captures at 16:49; reverted at 17:08; not made by this task). All runs and all
   logs here are at the committed default (`[meta-proj] theta=0.750`); the tree was clean at the
   commit. Since `sim_agents.py` does not pass `theta`, the default governs the run; a regeneration
   with such an edit in place will not reproduce these baselines.

# Not measured

- A hold placed mid-segment, or waiting somewhere other than where the robot is (detour) — out of
  scope by decision (TODO-70).
- Anything after the human's last projected action: the tail numbers use the human's final position
  held indefinitely, which is T1's proxy, not a prediction.
- Rows with no projection at all (`most_likely = unknown`, 9 rows): no realization exists to
  measure; the design's rule (plain projected cost) applies.
- The executor's actual arrival time vs the projection (T1's Anomaly 5): the projection's timing is
  taken as given.
- Obstacle-aware paths (no obstacles in these four layouts).
- s between 100 and 150, where the all-unrealizable count jumps from 1 to 8: not resolved further.

# The three findings most consequential for the open decisions

1. **Separation (TODO-28).** On these fixtures s acts in three regimes, and they are set by
   geometry the robot does not choose: ≤ 10 cm (below the executor's own 30 cm arrival radius)
   nothing is held and the only failures are the arrival-tick cases; 20 – 100 cm (1 – 5 ticks of
   motion) holds are rare (3 – 6 of 87 rows), short under the minimal-hold policy (0.4 – 6.8 ticks,
   ≤ 0.2 of the task), always at a table convergence or a crossing, and every one of them is a hold
   *into the unassessed tail*; ≥ 150 cm the dominant event is the human's path passing the robot's
   standing position, which hold-only cannot resolve, and 8 → 33 of 43 triggers have nothing
   realizable. The value is therefore bounded above by the standing-position failures (~7 ticks of
   motion, ~0.1 of a diagonal here) and below by the arrival radius, not read off any conflict
   distribution.
2. **Per-segment vs whole (TODO-70), and the loop as written.** The per-segment policy at its
   minimal hold and the whole-trajectory shift agree on δ in every row both realize; they differ
   only where per-segment dead-ends at the table (4 rows) — the myopia of committing an early
   segment. The design's loop as written is a third thing: its hold runs from the segment start to
   the clear time, and when the violation runs to the arrival it holds a full segment, so it
   overshoots the minimal hold by 5 – 25 ticks (median) in every differing row, reverses two argmins
   the minimal hold keeps, and turns the same convergence into "hold a carry" or "unrealizable"
   depending on which agent arrives first. If the loop is kept, its clear-time semantics need to be
   decided against these rows.
3. **All-unrealizable (TODO-30) and B2 (TODO-36).** All-unrealizable does not occur below 50 cm
   and occurs once at 50 – 100 (a correct-hypothesis crossing on the current task, 1 of 43 admitted
   triggers), so at the separations where holds are short the outcome matters rarely; from 150 cm it
   is the majority case and it is mostly "the human walks past the robot" with single-task pools,
   i.e. reading (1) "hold and re-decide" would have to hold in a violated position. For B2: under
   minimal holds no current-task δ at s ≤ 100 exceeds 0.2 of either candidate reference, and B3's
   realized argmin keeps every held current task that was cheaper on cost; the two references (T_r,
   T_h) disagree by a factor of 5 on the same row (0.7 vs 0.14) only when the task is nearly done.
   The data contain 5 held current-task rows in two fixtures — enough to show the gate would not
   fire, not enough to show when it should.

# Verification

1. **Baselines regenerated at HEAD `51b7cee`** (`analysis/i3_phase_model/sweep.sh`, before any
   analysis code existed): all eight are byte-identical to `analysis/t5_continue/new/*.log`,
   including every `[meta-cand] min_dist` digit (no last-digit differences this time; the T5 note
   concerned T7/T8 → T5).
2. **Instrumentation changes nothing.** The eight instrumented logs written by `measure.py` are
   byte-identical to the T5 baselines (md5 7897fe99, 5ceb40dc, 395897bc, 1713f90e, d76ceeab,
   dc6e183b, 6b3e75ae, 07ecdc0f for s00_off … s40_on). The wrappers' "projections outside update"
   count equals admitted human projections + counterfactuals in every condition (the human
   projection is built before `update()` by design). The counterfactual re-projections run after
   `update()` returns and produce no log line and no state change.
3. **Closed form vs sampling.** For all 641 greedy iterations, the sampled first violation
   (0.01-tick samples) is within 0.0100 of the closed-form start (max 0.00999; 0 disagreements). For
   all 4129 realized trajectories (greedy, exact, whole), the sampled minimum distance over [0, T_h]
   is ≥ s (worst margin +0.0013 cm; 0 below).
4. **Grid resolution.** exact and whole re-run at 0.05 and 0.002 ticks for every row and s (3432
   pairs): status identical in all; δ differs by ≤ 0.04 (the 0.05 grid's spacing); 0 mismatches.
   Reported δ values are therefore accurate to 0.01 tick and do not depend on the resolution.
5. **Structure.** One Segment per action in all 141 candidate and 63 human projections. The
   pool-order argmin of logged int cost reproduces the logged winner at 66 of 70 triggers; the 4
   exceptions are the `feasible=False` exclusions (Anomaly 3).
6. **Hand spot check** (`spotcheck.py`), s20 prior-on step 6, item_4, s = 30. Robot (−446.3, 192.7),
   human (81.6, −24.8); robot legs 327.2 cm + 1 + 583.1 + 1 → T_r 47.515 (logged cost 48); human
   309.4 + 1 + 616.9 + 1 → T_h 48.315. Carry placed at t₀ = 17.361, D = 29.155: relative motion
   A + Bτ with A = (−202.5, 107.4), B = (4.454, −1.980); d² = 23.755 τ² − 2229.0 τ + 52537.5 < 900
   between the roots 41.691 and 52.139; overlap window ends at the robot's arrival 46.515 < 52.139,
   so the violation is open at the arrival. greedy: clear = 46.515, hold = 29.155 (one carry), the
   re-placed carry has walked 36 cm at T_h and is 566.5 cm from the human → clear; realized cost
   76.67. exact: the robot must be ≥ 30 cm short of the table at T_h: t' = 48.315 − (583.1 − 30)/20
   = 20.660, hold = 3.299 = (T_h − arrival) + s/speed = 1.799 + 1.5. `realize.py`: greedy 29.155,
   exact 3.300, whole 3.300.
