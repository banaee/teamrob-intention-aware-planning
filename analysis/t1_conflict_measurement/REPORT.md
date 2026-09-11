# T1 — Conflict-geometry measurement for MetaPlanner (measurement only)

> **Units note (added after T2, commit `2282c83`):** every cost, step count, T_r/T_h and pause
> delay δ in this report is in pre-T2 projection units (1 unit = 1 cm of motion, ≈ 20 units per
> Mesa tick; stationary actions 1 unit). Since T2 the projector runs in execution ticks.
> Distances (min d, s) are world units (cm) and are unchanged.

Code at HEAD `372d925` (main, clean tree). `shared/` untouched. Six runs, `PYTHONHASHSEED=0`.
No decision, default, threshold or cost was changed; nothing below proposes one.

## How to read this directory

| File | Content |
|---|---|
| `measure.py` | Drives the six conditions with instance-level wrappers on the robot's live `MetaPlanner`/`Projector`; writes `captures.json` (git-ignored, 1.3 MB) and byte-comparable instrumented logs (git-ignored). |
| `analyze.py` | `captures.json` → every table and plot below. |
| `spotcheck.py` | §6.4 hand arithmetic for s20 prior-on step 11, item_4. |
| `rows.csv` | §5.0 — one row per (condition, trigger, candidate), 93 rows, with tags and `min_d`, `T_r`, `T_h`, tail. |
| `a_conflict_profile.csv` | §5.1 — per row × s ∈ {10,25,50,100}. |
| `b_curves/*.png, *.csv` | §5.2 — the three required d(t) curves; `b_curves/all/*.png` the same plot for every other trigger with a projection. |
| `c_pause_delay.csv` | §5.3 — per primary row × s. |
| `d_min_d_sorted.csv`, `d_min_d_hist.png`, `d_scale_context.csv` | §5.4. |
| `e_pairs.csv` | §5.5 — candidate pairs within a trigger. |
| `f_theta_flips.csv`, `f_most_likely_changes.csv` | §5.6. |
| `g_tail.csv` | §5.7. |
| `summary.md` | all tables in markdown, auto-generated; quoted selectively below. |

**Units.** The projector runs at `assumed_speed = 1.0`, so one projection step is one world unit
(cm) of movement; a candidate's cost is its path length plus 1 per stationary action
(`costs.yaml` is empty, `default_action_cost = 1.0`). The executor moves 20 units per Mesa tick
and takes one full tick per grasp/release. So **t = 20 projection steps ≈ 1 Mesa tick** for
motion, and a stationary action is 20× shorter in the projection than in execution. All
distances and step counts below are in world units / projection steps unless a Mesa tick is
named explicitly.

**Row classes.** *Primary* = trigger with a built projection (43 rows, 24 triggers).
*Counterfactual* = trigger rejected `none(below_theta)`, profiled against a projection of that
tick's below-θ `most_likely` (44 rows; never pooled with primary). Of those, 8 are
*degenerate* (human finished its script, or the hypothesis projects an item already at the
table; the projected human never moves ≥ 30 units) and are kept out of (d) and (e). *None* = no
projection possible (6 rows: t=0 with the prior on, `most_likely = unknown`).
*Wrong-hypothesis* rows (`hypothesis_matches_actual = False`) stay in the tables and are
reported separately: 5 primary rows, all in s10 prior-on (steps 107, 142, 200 — the coffee
walk credited to item_6, TODO-46).

Primary rows per condition: s00_off 6, s00_on 8, s10_off 2, s10_on 7, s20_off 10, s20_on 10.
Seven of the 43 are exact duplicates across the prior on/off pair (s00 steps 41, 63, 131;
s10 steps 257, 262 — same tick, same positions, same belief), so there are 36 distinct
geometries.

---

## (a) Conflict profile (§5.1)

Data: `a_conflict_profile.csv`; per-row summary in `rows.csv`; full tables in `summary.md`.

Steps with d(t) < s, primary rows that have any step below 100 (the other 30 primary rows have
none at any s):

| condition | step | candidate | cost | min d | @t | <10 | <25 | <50 | <100 | intervals | robot phase in the close steps | human phase |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| s20_on  | 11  | item_4 (winner, current) | 812  | 15.3 | 812 (end) | 0 | 72 | 188 | 398 | 1 | carry_to_table (+1 placement) | carry_to_table |
| s20_on  | 11  | item_7 | 1841 | 41.3 | 336 | 0 | 0 | 36 | 118 | 1 | approach_shelf | carry_to_table |
| s20_on  | 23  | item_4 (winner, current) | 570  | 25.9 | 569 (end) | 0 | 0 | 124 | 294 | 1 | carry_to_table (+1 placement) | carry_to_table |
| s20_off | 22  | item_4 (winner, current) | 612  | 16.3 | 595 (end) | 0 | 61 | 164 | 350 | 1 | carry_to_table | carry_to_table (+1 placement) |
| s20_off | 22  | item_7 | 1687 | 93.7 | 109 | 0 | 0 | 0 | 47 | 1 | approach_shelf | carry_to_table |
| s20_off | 24  | item_4 (winner, current) | 570  | 5.9  | 569 (end) | 23 | 75 | 155 | 314 | 1 | carry_to_table (+1 placement) | carry_to_table |
| s10_off/on | 257 | item_5 (winner, current) | 1308 | 24.5 | 1308 (end) | 0 | 1 | 187 | 433 | 1 | carry_to_table (+1 placement) | carry_to_table |
| s10_off/on | 262 | item_5 (winner, current) | 1190 | 63.5 | 1189 (end) | 0 | 0 | 0 | 325 | 1 | carry_to_table (+1 placement) | carry_to_table |
| s10_on  | 107 | item_1 (winner, current) — wrong hyp | 1820 | 89.6 | 159 | 0 | 0 | 0 | 85 | 1 | approach_shelf | approach_shelf |
| s10_on  | 142 | item_1 (winner, current) — wrong hyp | 1110 | 7.0  | 146 | 12 | 42 | 86 | 174 | 1 | carry_to_table | approach_shelf |
| s10_on  | 142 | item_5 — wrong hyp | 3198 | 4.0 | 317 | 30 | 82 | 166 | 451 | 2 | approach_shelf | approach_shelf, then carry |

Observations.
- Every close episode in a correct-hypothesis row is **one interval that begins mid-carry and
  ends at the last step of the shared window**, with both agents in `carry_to_table` (the robot's
  single-step `placement` is the last step). None of these has a step below 10.
- The only correct-hypothesis rows whose minimum is interior (not at the window end) are the
  two item_7 rows in s20: the robot's approach to shelf_7 crosses the human's carry path
  (min 41.3 at t=336; min 93.7 at t=109). These are the only crossing geometries with a correct
  hypothesis.
- The three rows with any step below 10 are s20_off step 24 item_4 (23 steps, ≈1.2 Mesa ticks)
  and the two s10_on step 142 wrong-hypothesis rows (12 and 30 steps).
- Exposure durations at s=50 range from 36 steps (≈1.8 ticks, item_7 crossing) to 188 steps
  (≈9 ticks, item_4 convergence).

---

## (b) Distance-over-time curves (§5.2)

Data: `b_curves/s20_on_step011.{png,csv}`, `b_curves/s20_on_step023.{png,csv}`,
`b_curves/s20_off_step022.{png,csv}` (the first prior-off trigger with a built projection is
step 22). Columns: `t`, `d_<candidate>`, `robot_phase_<candidate>`, `human_phase`. Vertical
lines mark action boundaries (orange dashed robot, teal dotted human); grey shading is the part
of the robot's trajectory after the human projection ends.

Shapes (factual):
- **s20_on step 11, item_4** (cost 812, T_h 828): d falls monotonically from 438 to 15.3 with
  one kink at the pick-up (t=228, d=145). From the kink on, both agents carry toward the same
  table and d decreases linearly at ≈0.22 units per step. The curve ends at the robot's
  placement with the human 15.3 units from the table and still approaching.
- **s20_on step 11, item_6** (cost 1189): V-shape, minimum 292 at t=215 (robot arriving at
  shelf_6 while the human is at shelf_3), then rising to 420 at pick-up and drifting down to
  360 when the human projection ends at 828. The last 360 steps (30 % of cost) are unchecked.
- **s20_on step 11, item_7** (cost 1841): V-shape with minimum 41.3 at t=336 — the robot's
  approach to shelf_7 crosses the human's carry path — then diverging to 760 by t=828.
  55 % of cost unchecked.
- **s20_on step 23** (robot holding item_4): item_4 is a straight line from 186 to 25.9 over
  570 steps (both carrying; the human is 26 units behind at the robot's placement).
  item_6/item_7 begin with the 28-step return of item_4 to shelf_4 (`deliver_with_return`);
  item_6's minimum 159 is at that return placement (t=28); item_7's minimum 112 at t=106.
- **s20_off step 22**: item_4 falls from 186 to 16.3 at t=595, which is the human's placement
  (here T_h < T_r: the robot is 16 units short of the table when the human projection ends).
  item_6 min 185 at t=2; item_7 min 93.7 at t=109 (crossing).

---

## (c) Pause delay (§5.3)

Data: `c_pause_delay.csv` (172 = 43 rows × 4 s). Definition as specified: robot holds its start
position for δ steps (the hold counts), then runs its projected trajectory unshifted against the
unshifted human projection; smallest integer δ ≥ 0 with d_δ(t) ≥ s wherever both exist;
search δ ∈ [0, T_h). Two extra columns: `clears_via_tail` (some violation of δ−1 was pushed past
T_h rather than separated), `clears_via_tail_only` (all of them were), and
`delta_ext_human_held_at_end` (same search with the human held at its final position after
T_h, so the whole robot trajectory is checked — only there to make the tail flag readable).

Rows with δ > 0 (all others are δ = 0 at every s):

| condition | step | candidate | s | δ | δ/cost | clears via tail | tail only | δ with human held at end |
|---|---|---|---|---|---|---|---|---|
| s20_on  | 11 | item_4 | 25 / 50 / 100 | 42 / 67 / 117 | .052 / .083 / .144 | yes | yes | unresolvable |
| s20_on  | 11 | item_7 | 50 / 100 | 144 / 223 | .078 / .121 | no | no | unresolvable |
| s20_on  | 23 | item_4 | 50 / 100 | 77 / 127 | .135 / .223 | yes | yes | unresolvable |
| s20_off | 22 | item_4 | 25 / 50 / 100 | 9 / 34 / 84 | .015 / .056 / .137 | yes | partly | unresolvable |
| s20_off | 22 | item_7 | 100 | 10 | .006 | no | no | unresolvable |
| s20_off | 24 | item_4 | 10 / 25 / 50 / 100 | 17 / 32 / 57 / 107 | .030 / .056 / .100 / .188 | yes | yes | unresolvable |
| s10_off/on | 257 | item_5 | 25 / 50 / 100 | 51 / 76 / 126 | .039 / .058 / .096 | yes | partly | unresolvable |
| s10_off/on | 262 | item_5 | 100 | 165 | .139 | yes | yes | unresolvable |
| s10_on | 107 | item_1 (wrong hyp) | 100 | 13 | .007 | no | no | unresolvable |
| s10_on | 142 | item_1 (wrong hyp) | 10 / 25 / 50 / 100 | 4 / 23 / 53 / 114 | .004 / .021 / .048 / .103 | no | no | 4 / 23 / 53 / 114 |
| s10_on | 142 | item_5 (wrong hyp) | 10 / 25 / 50 / 100 | 15 / 31 / 152 / 209 | .005 / .010 / .048 / .065 | no | no | unresolvable |

Observations.
- 140 of 172 (row, s) combinations need no pause (δ = 0). 32 need one; **0 are unresolvable**
  under the specified search. No hold position was within s of the human at a tick that
  mattered (`hold_first_conflict_t` is set in 10 combinations, all with δ = 0).
- Of the 32 non-zero δ, **20 clear via the tail** (11 entirely, 9 partly): the delayed robot
  motion lands after T_h and is never checked. These are exactly the correct-hypothesis
  convergence rows (item_4 in s20, item_5 in s10). For them δ is arithmetic on the arrival gap:
  s20_on 11 item_4 has T_h − T_r = 16, and δ(s) = s + 16 + 1 (42, 67, 117). With the human held
  at the table after T_h, every one of these is unresolvable — the robot's destination is the
  human's final position.
- The 12 genuine separations are all crossing geometries: the s20 item_7 rows and the s10_on
  coffee-walk rows (wrong hypothesis). For s10_on 142 item_1, δ is identical with and without
  the human held at its end (4/23/53/114), i.e. a real clearance.
- **Exposure and pause disagree in the direction §2 anticipated.** At s20_on step 11, s=50:
  item_4 is close for 188 steps and needs δ = 67 (and only via the tail); item_7 is close for
  36 steps and needs δ = 144 (genuine). Ranking by exposure and ranking by pause invert.
- Only a whole-trajectory shift from t=0 was measured; a pause inserted mid-trajectory (e.g. at
  pick-up) could need less. Not computed.

---

## (d) Distribution of min d(t) (§5.4)

Data: `d_min_d_sorted.csv`, `d_min_d_hist.png`, `d_scale_context.csv`. Primary rows only (43;
36 distinct). Degenerate counterfactual rows are excluded by construction (not primary).

Sorted min d, correct hypothesis (38 rows; winners in bold):
**5.9**, **15.3**, **16.3**, **24.5**, **24.5**, **25.9**, 41.3, **63.5**, **63.5**, 93.7, 111.9,
125.6, **136.4**, **136.4**, **139.7**, **140.7**, **154.8**, 159.4, 159.9, 185.4, 203.2, 226.3,
226.3, **279.9**, 292.3, **299.3**, **299.9**, **301.7**, **301.7**, **303.3**, 326.7, 326.7, 380.5,
**480.0**, **480.0**, 493.6, 611.1, 618.8.
Wrong hypothesis (5 rows): 4.0, **7.0**, **89.6**, 189.1, **661.3**.

Per condition (correct hypothesis): s00 (14 rows) 136–480, nothing below 136; s10 (4 rows)
24.5, 24.5, 63.5, 63.5; s20 (20 rows) 5.9–619 with the six values below 30 all item_4.

Observations.
- The previously observed "conflicted 4.9–29, clear 93–819, nothing between 30 and 93" is
  **not confirmed**: 41.3 (s20_on 11 item_7), 63.5 (s10 262 item_5, twice) and 89.6 (wrong hyp)
  fall in the gap, and the largest value is 661 (819 was pre-fix). The value 4.9 in the task
  prompt is the logged fractional-endpoint sample of a row whose integer-step minimum is 5.9.
- **All six correct-hypothesis values below 30 occur at the last step of the shared window**
  (`min_at_window_end = True`) and equal the projected arrival-time gap between the two agents at
  the kitting table, in world units. They are truncation values, not closest approaches — see
  Anomalies.
- Every winner with min d < 30 is the current task continuing into the shared table.
- Sample size: 24 triggers, 43 rows, 36 distinct geometries, three layouts, one human script
  per layout run twice (prior off/on). Twenty of the 36 distinct geometries come from a single
  fixture (scenario_20) built to produce convergence.

Scale context (from `d_scale_context.csv`):

| | env_layout0 (s00) | env_layout1 (s10) | env_layout2 (s20) |
|---|---|---|---|
| space (w × h), diagonal | 1000 × 800, 1281 | 2000 × 1000, 2236 | 1200 × 900, 1500 |
| task-object bounding box | x[−400,400] y[−300,350] | x[−975,950] y[−450,400] | x[−500,450] y[−350,400] |
| projected leg length min / median / max | 0 / 602 / 820 | 18 / 1125 / 1953 | 0 / 612–629 / 1151 |
| median approach leg / carry leg | 581 / 602–645 | 776–783 / 1134 | 447–526 / 820 |
| full task costs at t=0 | 586, 908, 1538 | 1646, 1996, 2457 | 1032, 1372, 2028 |
| candidate cost min / median / max over all triggers | 222 / 1105 / 1828 | 971 / 2029 / 3198 | 570 / 1372 / 2028 |
| `assumed_speed`, `default_action_cost`, `min_safe_distance`, θ | 1.0, 1.0, 1.0, 0.75 | same | same |
| Mesa step size (units per tick), executor "at" proximity | 20, 30 | 20, 30 | 20, 30 |

The executor's `PROXIMITY_THRESHOLD` (30 units) is the distance at which a `move_to` is
considered complete; it is of the same magnitude as the six smallest min d values.

---

## (e) Cost vs. conflict disagreements (§5.5)

Data: `e_pairs.csv` — 23 primary pairs (within-trigger, A = cheaper), 29 non-degenerate
counterfactual pairs listed separately in the file and in `summary.md`. Δ = B − A. Cost prefers
A; "disagree" means the conflict measure prefers B.

Primary pairs with any step below 100 in either candidate (the other 11 pairs have both
candidates ≥ 100 at every step and disagree on min d only in the sense that both are far):

| condition | step | A (cheaper) | B | Δcost | min d A / B | Δ<50 steps | Δ<100 steps | δ50 A / B | δ100 A / B |
|---|---|---|---|---|---|---|---|---|---|
| s20_on  | 11 | item_4 (winner) | item_6 | 377 | 15.3 / 292.3 | −188 | −398 | 67 / 0 | 117 / 0 |
| s20_on  | 11 | item_4 (winner) | item_7 | 1029 | 15.3 / 41.3 | −152 | −280 | 67 / 144 | 117 / 223 |
| s20_on  | 11 | item_6 | item_7 | 652 | 292.3 / 41.3 | +36 | +118 | 0 / 144 | 0 / 223 |
| s20_on  | 23 | item_4 (winner) | item_6 | 530 | 25.9 / 159.4 | −124 | −294 | 77 / 0 | 127 / 0 |
| s20_on  | 23 | item_4 (winner) | item_7 | 1125 | 25.9 / 111.9 | −124 | −294 | 77 / 0 | 127 / 0 |
| s20_off | 22 | item_4 (winner) | item_6 | 466 | 16.3 / 185.4 | −164 | −350 | 34 / 0 | 84 / 0 |
| s20_off | 22 | item_4 (winner) | item_7 | 1075 | 16.3 / 93.7 | −164 | −303 | 34 / 0 | 84 / 10 |
| s20_off | 22 | item_6 | item_7 | 609 | 185.4 / 93.7 | 0 | +47 | 0 / 0 | 0 / 10 |
| s20_off | 24 | item_4 (winner) | item_6 | 530 | 5.9 / 159.9 | −155 | −314 | 57 / 0 | 107 / 0 |
| s20_off | 24 | item_4 (winner) | item_7 | 1125 | 5.9 / 125.6 | −155 | −314 | 57 / 0 | 107 / 0 |
| s10_on  | 107 | item_1 (winner, wrong hyp) | item_5 | 835 | 89.6 / 189.1 | 0 | −85 | 0 / 0 | 13 / 0 |
| s10_on  | 142 | item_1 (winner, wrong hyp) | item_5 | 2088 | 7.0 / 4.0 | +80 | +277 | 53 / 152 | 114 / 209 |

Observations.
- Cost and min d disagree in 18 of 23 primary pairs; in 11 of those both candidates have no
  step below 100, so the disagreement is between two clear candidates. Cost and
  steps-below-50 disagree in 8 pairs, all of them s20 item_4 (winner) against item_6 or item_7;
  cost and δ50 disagree in 7 of those 8.
- The exception is s20_on 11 item_4 vs item_7: min d (15 vs 41) and exposure (188 vs 36 steps
  below 50) prefer item_7, δ50 prefers item_4 (67 vs 144). The two conflict measures order this
  pair oppositely; the "cheaper" δ is the tail-cleared one.
- Close on cost, far on conflict: s20_on 11 item_4 vs item_6 — Δcost 377 (46 % of A) against
  Δmin d 277, Δ<50 188 steps, Δδ50 67. Far on cost, close on conflict: s20_on 11 item_6 vs
  item_7 — Δcost 652 against Δmin d −251 and Δδ50 +144, i.e. the expensive one is also the
  conflicted one; and s00 pairs (Δcost 362–1606) whose min d differ by 25–90 while both stay
  ≥ 136.
- s10_on 142 (wrong hypothesis): item_1 and item_5 have min d 7.0 and 4.0 — indistinguishable
  on min d — while cost (1110 vs 3198), exposure (86 vs 166 steps below 50) and δ (53 vs 152)
  all order them the same way.
- Counterfactual pairs (29): cost vs min d disagree in 13, cost vs steps-below-50 in 4
  (s20_off step 0 item_4 vs item_6/item_7 against the t=0 tie-break hypothesis, and s10_off step
  0 item_7 vs item_5/item_1 against a wrong hypothesis).

---

## θ-flip scan (§5.6, TODO-48)

Data: `f_theta_flips.csv` (empty), `f_most_likely_changes.csv` (25 changes). Scanned every
`[IR] step=` line of all six runs.

**Result: no tick in any run changes `most_likely` while confidence is ≥ θ at both that tick
and the previous one.** The 25 `most_likely` changes all have at least one side below θ:

- 16 are swaps with both sides below θ (confidence 0.15–0.74), mostly early in a run or
  between human tasks.
- 6 are a collapse after the human's task completes, from ≥ θ to well below (s00_off 78:
  0.797→0.351; s00_off 142: 0.970→0.366; s00_on 78: 0.797→0.510; s20_off 54: 0.797→0.599;
  s20_off 122: 0.928→0.432; s20_on 122: 0.928→0.500). None of these fires a trigger; the next
  trigger is the robot's own `no_current_task` or `task_committed`, 1–26 ticks later.
- 3 coincide with a `theta_crossed` trigger on the same tick (s10_off 257, s10_on 257
  0.738→0.769, s20_off 89 0.353→0.928): the hypothesis changes and crosses θ in one tick, so the
  trigger already covers them.
- Among the 16, s10_on 78 (0.399→0.730, item_2→item_6, human actually on the coffee walk) is
  the largest change that stays below θ; it becomes the wrong-hypothesis admission at 107.

---

## Tail beyond the human projection (§5.7)

Data: `g_tail.csv`.

- 34 of 43 primary rows have T_r > T_h. The unchecked share of the candidate's cost ranges from
  0.027 (s20_off 22 item_4, 16 steps) to 0.81 (s00 63 item_4, 1189 steps); median 0.49.
  15 of the 24 winners have an unchecked tail (winners' shares 0.027–0.70).
- For every non-current candidate the unchecked part contains the whole carry leg and
  placement, and for the `deliver_with_return`/fresh-approach candidates the pick-up as well.
- The other 9 rows have T_h > T_r (robot finishes first; all are current-task winners
  converging on the table, plus s00_on 81 item_6 with 957 steps of human projection left). In 6
  of these the minimum sits at T_r: the human is still converging on the robot's final position
  when the check stops. Nothing in the projection represents either agent after its last action.

---

## Interpretation (labelled; not part of the measurements)

- The six smallest correct-hypothesis min d values measure how far apart the two agents are at
  the instant the first of them finishes at the shared table, i.e. the arrival gap × speed.
  With the human's projection ending at its placement, the geometry that follows (both at the
  table) is invisible to both `min_dist` and the pause delay; a design step that reads these
  values as closest approaches would be reading the truncation.
- Under the specified pause definition, "unresolvable" cannot occur for a candidate whose
  conflict lies late in the human projection, because a δ near T_h always clears by waiting the
  projection out. The `clears_via_tail` flag and the held-human variant separate the two
  outcomes; 20 of the 32 non-zero pauses are of the tail kind.
- Exposure (steps below s) and pause (δ) rank the two s20 conflict geometries oppositely:
  co-directional convergence is long-exposed but cheap to shift (if the shift were real),
  crossing is briefly exposed but expensive to shift. They are not proxies for each other.

---

## Anomalies

1. **Truncation minima.** All six correct-hypothesis rows with min d < 30, and 16 of 43 primary
   rows overall, have their minimum at the last step of the shared window. For the item_4/item_5
   convergence rows the logged `min_dist` is exactly the projected arrival gap at the kitting
   table (e.g. s20_on 11: T_h − T_r = 16.0, min d 15.3 with the robot at the table and the human
   15.3 units away). The realized run confirms the convergence: at s20 step 54/55 the robot and
   the human are 15.5 units apart at the table, the human placing item_3.
2. **Pause search cannot fail.** δ ∈ [0, T_h) with a human projection that simply ends means a
   large δ always "clears" unless the hold position itself is within s. 0 of 172 combinations
   are unresolvable; 20 of 32 non-zero δ clear via the tail; with the human held at its end
   position 153 of 172 combinations are unresolvable.
3. **The 30–93 gap does not exist** in the current data (41.3, 63.5, 63.5, 89.6). The largest
   clear value is 661, not 819. The prompt's 4.9 is the fractional-endpoint sample of an
   integer-step 5.9.
4. **Sampling vs integer steps.** The logged `min_dist` includes each overlap window's exact
   (fractional) end point; the integer-step minimum is larger by up to 0.96 in 27 rows and
   identical in 16. The argmin of the logged value is a fractional segment boundary in every
   differing row (e.g. 812.31, 595.85, 279.18).
5. **Projection time scale.** Stationary actions cost 1 projection step (≈ 0.05 tick) but 1
   tick in execution; the executor also ends a `move_to` 30 units early (proximity threshold).
   Spot check (§6.4): projected robot grasp at step 22.4 vs actual 22; projected release at
   53.5 vs actual 51. TODO-28 territory; reported, not changed.
6. **TODO-37 decoys in below-θ hypotheses.** After the human's script ends (s20 steps 138/139,
   182/183), `most_likely` is a delivered item (item_3 / item_4) at 0.43–0.50 and its projection
   is a 30-step walk to the table. Flagged degenerate; excluded from (d)/(e).
7. **Baseline step counts.** The reference logs `run_20260910_1552{03,04}.log` for scenario_00
   are 200-step runs; the task lists 300. The 300-step regeneration is byte-identical over the
   first 200 steps and adds nothing (all tasks complete at step 168 in both conditions).
8. **t=0 with the prior on** has `most_likely = unknown` (0.332), so no counterfactual can be
   built (the 6 "none" rows). With the prior off, t=0 `most_likely` is the layout-order
   tie-break (TODO-42): item_3 in s00 (happens to be right), item_1 in s10 and item_4 in s20
   (wrong; item_4 is a robot task).

## Verification (§6)

1. **Baselines regenerated at HEAD** (`372d925`, before any analysis code existed). All six runs
   are byte-identical to `logs/run_20260910_1552{03,04,06,08,10,11}.log` on `[meta]`,
   `meta-cand`, `[meta-proj]` and `[IR] step=` lines, and on the whole file over the reference
   step range (scenario_00 references are 200-step runs; see Anomaly 7).
2. **Instrumentation changes nothing.** The instrumented logs written by `measure.py` (same
   format as `run_mesa.py`, including per-step position lines) are byte-identical to the
   regenerated baselines for all six conditions (md5: s00_off bd36b532, s00_on 352b6769,
   s10_off 1a213add, s10_on a4cd5e7a, s20_off a7323c7a, s20_on 4afa6190). The counterfactual
   re-projections run after `update()` returns and produce no log lines and no state change
   (`Projector.project` reads `world`/`belief` only; `AdaptivePlanner` is stateless).
3. **Cross-check of distances.** For all 43 primary rows, the analysis-side d evaluated at every
   ConflictPoint's own sample step reproduces the ConflictPoint distance to within 2.3 × 10⁻¹³.
   `min_t d(t)` over integer steps equals the logged `min_dist` in 16 rows and exceeds it by
   0.18–0.96 in 27, always because the logged argmin is a fractional window end point (Anomaly
   4). One Segment per AbstractPlan action holds in every projection captured (93 candidate
   projections, 24 human projections, 23 counterfactual projections).
4. **Hand spot check** (`spotcheck.py`), s20 prior-on step 11, item_4. Live positions: robot
   (−401.6, 103.2), human (−2.9, −78.2); shelf_4 (−300, −100), shelf_3 (−180, −190), table
   (0, 400). Robot legs 227.2 + 1 + 583.1 + 1 = 812.3 (logged cost 812); human 209.4 + 1 +
   616.9 + 1 = 828.3. Robot progress at the trigger: 220 of 447 units of the approach done
   (49 %; "about half-way"). By-hand d at t = 0, 100, 227, 300, 500, 700, 812: 438.02, 306.13,
   145.38, 127.54, 79.41, 33.12, 15.29 — identical to the exported curve at all seven steps.
   The prompt's step-11 figures (0.780, item_4 cost 812 / 14.98, item_6 1189 / 292.3) are all
   reproduced in the log.

## Not measured

- A pause inserted mid-trajectory (e.g. at pick-up) rather than a whole-trajectory shift.
- Any geometry after an agent's last projected action (no post-completion position exists in
  the projection; see §5.7).
- Sub-step closest approach between integer samples (bounded by half the relative speed,
  ≤ 1 unit per step).
- Obstacle-aware paths: env_layout1 has 14 obstacles that both the projector and the executor
  ignore (straight lines).
- Rows with no resolvable hypothesis (the 6 "none" rows) have no conflict fields.
- ROS side and dock_loading domain — out of scope.
