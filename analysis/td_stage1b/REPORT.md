# T-D cycle 1.5b: acceptance of E8, E9, E10 and G1 (cycle 1, session 1.5b)

27 September 2026, at the 1.5b build (fe483d8 recognizer, 1ccabf3 meta-planner, dec0e87 baselines). 1.4's scripts
(`analysis/td_stage1/`) rerun on the regenerated baselines, adapted to the new log field only; every expectation of
the task is checked against the mechanism, and where one is not met it is stated as a finding, not adjusted.

## Material and conventions

- POST: the four maintained sets regenerated at 1.5b (`analysis/{tb1a_destination,tb1b_two_tables,tb1c_realized_flip,tb3_full_reorder}/sweep/`,
  48 logs; md5s in the READMEs' "T-D cycle 1.5b" sections).
- PRE: the 1.3b baselines (7f4559a), md5-checked against the READMEs' "E6 amended" sections (48 of 48 match) and
  copied to `pre/<set>/` before any code changed. The 52 `.rec` streams (48 + 4 supplementary) are byte-identical
  PRE and POST: the ground truth is the same on both sides.
- SUPPLEMENTARY: scenario_s06_06 (env_layout_08) and scenario_s07_03 (env_layout_09), prior off and on, the tb1a
  options, 300 steps (`supp_sweep.sh`): `pre/supp/` at 732c354, before any code changed (md5 identical to 1.4's
  HEAD logs: 06504fdc…, e680b94b…, 4ecc3614…, f39e633e…) and `post/supp/` after (s06_06 off dbfc8280…, on 1d11e424…;
  s07_03 off 0a38e5c5…, on 7a7f3b2f…). All logs git-ignored.
- ADAPTATION (the only changes to 1.4's logic): `tdlib.py` parses `leader_adequacy=` in the `[IR]` line (without
  it 1.4's regex would drop the tails) and reads the new paths; `a_invariant.py` adds A8 for the new field;
  `d_decisions.py` prints the leader's hypothesis adequacy (POST) and the finding (PRE) in its state strings;
  `g_priced_standing.py` reads s_exp per phase from the recognizer during the run (the E9 signature) and prints
  the Projector's attribution beside it. New: `baseline_diff.py` (item 1g), `clip_ticks.py` (decision 3).
- Truth, alignment (record task transitions 2 ticks after the world fact), α levels and grouping as in 1.4.
  Prior ON is the primary set; prior OFF an appendix to each section.

Run from this directory with `~/python-envs/ir-nomesa-env/bin/python <script>.py > <script>.txt`; G and
`clip_ticks.py` from the repo root with `PYTHONHASHSEED=0` (commands in their docstrings).

---

## The baseline regeneration (item 1g; `baseline_diff.py` → `baseline_diff.txt`)

`.rec` streams byte-identical in all 48 runs. Every run's `[IR]` lines changed (the new field on every live tick).
The walking-only span of scenario_s01_01 prior on (0–38): `[IR-dist]` byte-identical PRE and POST (E10 leaves
walking evidence unchanged).

| set | prior | runs | [IR] changed | world changed | completion, world tick (T6), where it moved |
|---|---|---|---|---|---|
| tb1a_destination | on | 8 | 8 | 3 | s03_01 237→238; s05_01 171→197; s05_02 172→198 |
| tb1a_destination | off | 8 | 8 | 7 | s01_01 202→200; s03_01 incomplete (last release 144)→236; s05_01 171→194; s05_02 172→195 |
| tb1b_two_tables | on | 2 | 2 | 0 | — |
| tb1b_two_tables | off | 2 | 2 | 0 | — |
| tb1c_realized_flip | on | 4 | 4 | 0 | — |
| tb1c_realized_flip | off | 4 | 4 | 1 | s06_03 realized 239→236 |
| tb3_full_reorder | on | 10 | 10 | 3 | s03_01 single_task 237→238; s05_01 both strategies 171→197 |
| tb3_full_reorder | off | 10 | 10 | 5 | s03_01 single_task incomplete→236; s05_01 both 171→194; s06_03 full_reorder 239→236, single_task 317→315 |

"World changed" = the agents' per-tick lines differ; the first differing tick per run is in `baseline_diff.txt`
(prior on: s03_01 at 54, s05_01 / _02 at 32).

## A. The R6 invariant (`a_invariant.py` → `a_invariant.txt`) — expected: holds. MET.

12,923 ticks (48 + 4 supplementary): 0 violations of A1–A7 (1.4's checks), and 0 of A8: the logged
`leader_adequacy` equals the value recomputed from the logged tails at α = 0.05 on every live tick, and is absent
exactly when exhausted.

## C. False unexplained (`c_findings.py` → `c_findings.txt`) — expected: the three grasp ticks gone. MET AS STATED; THE THREE MOVED ONE TICK.

| | α = 0.01 | α = 0.05 | α = 0.1 |
|---|---|---|---|
| prior ON, lag-corrected (4352 ticks, 204 instances) | 3 / 3 | 3 / 3 | 3 / 3 |
| prior ON, raw | 3 / 3 | 3 / 3 | 3 / 3 |
| prior OFF | 0 / 0 | 0 / 0 | 0 / 0 |

The grasp ticks (s02_01 on 247, s04_01 on 268, s03_06 on 88) now read adequate: the true hypothesis is a member at
S = 1 (E8). The three false unexplained ticks are now the NEXT tick, the pick_up's latency tick: s02_01 on 248,
s04_01 on 269, s03_06 on 89, at every α. On that tick the true hypothesis's carry walk has s = 1 = s_exp (E9) and
nothing walked, so it holds no observation (E6 (2)); the only member is the refuted foreseeable rival
(`ac_switch_0` S = 0.0000 / 0.0021, `coffee_break` 0.0016). The next tick (the first carry step) the true
hypothesis is a member at S = 1. Derived from the entry and asserted in
`tests/test_td15_build.py::test_the_grasps_latency_tick_holds_no_observation_for_the_carry_walk`. By phase, prior
on: `move_to#1` 3/44 instances (lag-corrected; raw `pick_up#0`), every other phase 0.

MISSED UNEXPLAINED, BINDING_ABSENT (the wrong table; TASK_ABSENT and outside-support: none exist, as in 1.4): first
unexplained one tick later than 1.4 at every α (s06_06: 48 / 41 / 38 at α .01 / .05 / .10, was 47 / 40 / 37;
s07_03: 39 / 34 / 31, was 39 / 33 / 31) — the carry walk entered from the grasp is priced its latency tick (E9),
so D is one tick smaller.

## D. Decisions (`d_decisions.py` → `d_decisions.txt`, `d_extras.txt`)

PRIOR ON (primary). Every admission, refusal and hold that differs from 1.3b; belief, finding, the leader's
hypothesis adequacy and the reason at that tick (`d_decisions.txt` has every line):

| run | tick | 1.3b | 1.5b | recognizer at the tick |
|---|---|---|---|---|
| s01_01 | 78 | built | `none(leader_no_observation)` | item_2 0.996, U, no_observation (boundary) |
| s01_01 | 80 | — | built (hold 0) | item_2 0.996, A, adequate |
| s02_01 | 130 | — | built (hold 0) | coffee_break 0.766, A, adequate |
| s02_01 | 153 | — | `none(below_theta)` | ac_switch_0 0.496, U (boundary; record replaced) |
| s02_01 | 309 → 311 | built at 309 | `none(leader_no_observation)` at 309, built at 311 | ac_switch_0 0.991 |
| s03_01 (×2) | 54 → 56 | built, hold 1 at 54 | `none(leader_no_observation)` at 54, built hold 2 at 56 | item_2 0.996 |
| s03_01 (×2) | 63 → 64, 148 → 149 | no_current_task | the same one tick later (the robot's schedule after the hold) | |
| s01_06 | 74 → 76 | built at 74 | `none(leader_no_observation)` at 74, built at 76 | item_7 0.996 |
| s04_01 | 158 | — | built (hold 0) | coffee_break 0.772, A, adequate |
| s04_01 | 183 | — | `none(below_theta)` | ac_switch_0 0.249, U |
| s04_01 | 327 → 329 | built at 327 | `none(leader_no_observation)` at 327, built at 329 | ac_switch_0 0.992 (idle human) |
| s03_06 | 121 → 123 | built at 121 | `none(leader_no_observation)` at 121, built at 123 | coffee_break 0.995 |
| s05_01 / _02 (×4) | 32 | — | built, HOLD 20 | coffee_break 0.776, A, adequate |
| s05_01 / _02 | 54 | — | `none(below_theta)` | ac_switch_0 0.498, U |
| s05_01 / _02 | 60 | built hold 0 | built HOLD 3 | item_5 0.804, A, adequate |
| s05_01 / _02 | 94 → 96 | built at 94 | `none(leader_no_observation)` at 94, built HOLD 3 at 96 | ac_switch_0 0.995 |
| s06_01, s06_02, s06_03 (all strategies) | b → b + 2 | built at the lone-task boundary | `none(leader_no_observation)`, built two ticks later, hold unchanged | |

Pattern: every boundary admission of a lone live task moves from the boundary tick to the first walking tick
(b + 2); coffee_break is admitted during its stand (below). One admission is refused as inadequate prior on:
s04_01 at 381, the last `no_current_task` with the pool already empty (`[meta] all tasks complete`; 1.3b built a
projection there; no decision follows either way; ac_switch_0 lone and idle, inadequate from 345). The
two new `none(below_theta)` lines are `recognition_changed` firing at a boundary because a record now exists (the
coffee admission).

Completion (world tick T6), prior on: 18 of 24 runs unchanged; s03_01 (×2) 237 → 238 (hold 2 instead of 1);
s05_01 (×3) 171 → 197 and s05_02 172 → 198 (the coffee hold of 20 at 32, and holds of 3 at 60 and 96). Minimum
separation unchanged in every prior-on run (s05_01 / _02 30.00, s03_01 3.85, s01_06 25.28).

APPENDIX, PRIOR OFF. Expected: the lone-item holds of 33 to 89 ticks gone. MET FOR scenario_s03_01, NOT FOR
scenario_s01_01 (derived at the plan step; your addition answered below):

| run | 1.3b | 1.5b |
|---|---|---|
| s01_01 off | built at 141, hold 33 (item_4 0.996, U); completion 202 | `none(leader_no_observation)` at 141; built at 143, HOLD 31 (item_4 0.996, A, adequate); completion 200 |
| s03_01 off (×2) | built at 145, hold 89 (item_7 0.996, X); incomplete in 300 steps | no trigger at 145 (the gate refuses, so `recognition_changed` does not fire); `no_current_task` at 147 `none(leader_inadequate)`; no hold; completion 236 |
| s03_01 full_reorder off | built at 131, hold 89; incomplete | unchanged: built at 131 (item_7 0.996, A, adequate), hold 89; incomplete |
| s06_03 realized / full_reorder off | built at 220, hold 13; completion 239 | `none(leader_no_observation)` at 220; built at 222, hold 10; completion 236 |
| s06_03 single_task off | hold 52 at 220; 317 | the same pattern at 222; 315 |

THE HOLD AND THE GUARD (your addition), s01_01 off and s03_01 off:
- scenario_s01_01 off: admitted at 143 (lead adequate: the idle stand is charged one tick beyond s_exp = 1,
  S = 0.8629). The leader turns `inadequate` at 159 (α = 0.05). The hold does NOT end there: it runs its planned 31
  ticks to 173 (`[hold] end executed=31 interrupted=False`); no trigger fires between 143 and 174. The admitted
  projection persists 14 ticks past the tick the guard turns: the gate is asked at admission only, and the record
  is retained by identity (D2).
- scenario_s03_01 off: the guard is already `inadequate` when the lone item becomes the leader (X since 139 at
  α = 0.05; item_7 lone from 145), so there is no admission and no hold to end.
- (the same persistence, prior off, s03_01 full_reorder: admitted at 131 while adequate, inadequate from 139, the
  89-tick hold runs to 219; the run does not complete, as before.)

Other prior-off moves: item_2 / item_3 reveals and their admissions one tick earlier (s01_01 113, s02_01 34,
s03_01 / _06 29 and 93); coffee_break admitted during its stand (s02_01 134, s04_01 158, s05 36 with hold 24);
s03_01 off minimum separation 30.12 → 3.85 cm (the 89-tick hold gone; the value before Stage 1), s05 off 30.00 →
25.75.

## E. Reveals (`e_reveals.py` → `e_reveals.txt`) — expected: coffee_break revealed during its stand in s02_01, s04_01, s05_01, s05_02; ac_switch_1 reported. MET.

| prior | task | 1.3b → 1.5b | the stand |
|---|---|---|---|
| on | coffee_break s02_01 | none → 130 | arrival 122, stand from 124 |
| on | coffee_break s04_01 | none → 158 | arrival 152, stand from 154 |
| on | coffee_break s05_01 / _02 | none → 32 | arrival 23, acknowledgement 24, stand 25–53 |
| off | coffee_break s02_01 / s04_01 / s05 | none → 134 / 158 / 36 | as above |
| on/off | ac_activation(ac_switch_1) s04_01 | none → none | peaks at 0.475 on 204 (the one-tick stand), completes 205 |

In s05 (prior on) the tie at 0.498 from 16 breaks as derived: coffee_break's `wait_at` is within its priced 31 ticks
(L = 1) while item_5's walk is charged v per standing tick from 24; coffee_break 0.524 at 24, crosses θ at 32
(0.776), the ninth tick of item_5's standing (L ≤ 1/3 at v·s ≥ 160.9 cm). Every other reveal is equal (prior on) or
one tick earlier (prior off: item_2 / item_3 / item_5, the rivals charged their unpriced standing).

## F. Adequate-below-θ (`f_adequate_below_theta.py` → `f_adequate_below_theta.txt`) — expected: the coffee wait_at ticks gone. NOT MET: REDUCED.

| | wait_at | pick_up | place | move_to |
|---|---|---|---|---|
| prior ON | 174 → 38 | 0 | 0 | 244 → 399 |
| prior OFF | 174 → 58 | 0 → 14 | 0 | 607 → 1626 |

The coffee stands keep their first ticks below θ, until the rival has stood the ~9 ticks that break the tie: s02_01
124–129 (6), s04_01 154–157 (4), s05_01 / _02 25–31 (7 each). The mechanism reveals the stay after 9 ticks of
charged standing, not on arrival; "gone" is not what E10 derives. The `move_to` count rises because the true walk
after a completion now has D = 0 exactly (S = 1; under Stage 1 S = 0.8629), so walks after a boundary before the
reveal enter the pattern (e.g. s02_01 77–123).

## G. The priced standing (`g_priced_standing.py` → `g_priced_standing.txt`)

The recognizer's s_exp equals the E9 attribution from the Projector's own segments on every phase read: move_to 0,
pick_up 2, carry move_to 1, place 2 (scenario_s01_01 on, item_3). The true hypothesis's D on the human's walking
ticks where it is a member: exactly 0 on 3891 of 3891 ticks per prior (Stage 1: D = 1 on 77.5%). (For item_2,
projected from step 80, the table's first recognizer value is the one first seen in the run, the initial walk's 0,
not the post-boundary 1: a reading limit of the script.)

## H. The boundary (`h_cases.py` → `h_cases.txt`, `b_cases.txt` B6) — expected: unresolved on the boundary tick and the latency tick, adequate from the first walking tick. MET.

Every boundary that leaves a task live reads U, U, then A (64 of 64 printed boundary groups `UUAAAA`, one `UUAAE`
cut by exhaustion; 15 exhaust). s01_01 on: 78 U, 79 U, 80 A (the first step). s02_01 on: 75 U, 76 U, 77 A. With an
idle human and no next task (s04_01 on 327, prior-off lone items), the finding resolves at b + 2 on standing charged
beyond s_exp = 1, not on a walk (the same rule).

THE WRONG TABLE (supplementary, default options) — expected: the admissions at 76 and 79 refused. MET, both priors:
s06_06 at 76 `none(leader_inadequate)` (the leader item_0 at 0.995, its carry walk to its designated table
inadequate, finding X since 41 at α = 0.05), s07_03 at 79 `none(leader_inadequate)` (item_2 at 0.995, X since 34). After the misdelivery release
(s06_06 103, s07_03 94) the stale item hypothesis is admitted again (0.995, `built`): no boundary at a misdelivery
(1.4 finding 5), and in its new derived phase (pick the item up where it now lies) it is a member at S = 1.
Completion unchanged (265, 243).

---

## Runs and tests that disagree with the mechanism

None. Every run and every test agrees with the mechanism as ruled; the three expectations above that are not met
as worded (C moved, F reduced, prior-off s01_01) are consequences the entry derives, listed below.

## Findings (numbers the design may not want, with the ticks)

1. THE LATENCY TICK AFTER A GRASP (E8 + E9 + E6 (2)): the false unexplained moved from the grasp tick to the next
   tick (s02_01 on 248, s04_01 on 269, s03_06 on 89; every α). E8 covers the advance tick; E9 prices the latency tick
   to the carry walk, where s = s_exp and nothing is walked, so the true hypothesis holds no observation for exactly
   one tick and a refuted rival alone decides.
2. THE GUARD ONLY AT ADMISSION: an admitted projection outlives its leader's adequacy (s01_01 prior off: inadequate
   from 159, the hold runs to 173; s03_01 full_reorder off: 139 → 219). D2 retains by identity; G1 does not
   reopen it.
3. THE IDLE LONE ITEM IS ADMITTED BEFORE IT IS INADEQUATE: prior off, the idle stand makes the lone item's walk
   adequate for 16 ticks after b + 1 (S from 0.86 down to 0.05); the gate admits it there (s01_01 off at 143,
   hold 31). Where the lone item arrives after 17 standing ticks it is refused (s03_01 off).
4. THE STAY IS REVEALED AFTER ~9 STANDING TICKS, not on arrival (F): the arrival adds nothing to a rival on the
   same bearing; the robot waits for the rival's standing to cost L ≤ 1/3.
5. THE MISDELIVERED ITEM IS ADMITTED AGAIN (s06_06 103, s07_03 94): the guard refuses the wrong-table carry (X) but
   admits the stale hypothesis after the release, adequate in its new phase (L's question, as 1.4 finding 5).

Flags: the `unknown` column in `e_reveals.txt` is 1.4's and reads 0.000 on the PRE side (no such key since
Stage 1); G's item_2 table reads the first s_exp seen in the run (above).

---

# 1.5c: the second E6 amendment (cycle 1, session 1.5c; closes cycle 1)

27 September 2026, at dd7a4fd (the membership condition), 3bfc293 (tests), 096408e (baselines).

THE RULING, AS RECORDED (design_decisions.md, "T-D R and E", E6, "AMENDED A SECOND TIME" and "THE BOUNDARY TICK"): a
stationary tick with s ≤ s_exp in any phase whose s_exp > 0 is an observation with D ≤ 0, the hypothesis a member with
S = 1 (and L = 1); it covers the latency tick E9 prices to a walk entered from a completion; the initial walk at
step 0 (s_exp = 0) is unchanged and stays unresolved until walking evidence occurs; no exception for phases opened by
a boundary. No hypothesis is a member on a boundary tick, a stationary phase the boundary opens included (E8's
boundary clause applied generally; reading 3 of 1.3b superseded).

THE CHANGED CONDITION (`IntentionRecognizer._adequacy`):
`walked > 0.0 or s > s_exp or (stationary_phase and s <= s_exp)` became
`walked > 0.0 or s > s_exp or ((stationary_phase or s_exp > 0.0) and s <= s_exp)`, and no hypothesis is a member when
the tick is a boundary tick (`if action is None or boundary: continue`). Nothing else changed; the belief is untouched
(L = 1 on these ticks before and after).

MATERIAL: PRE = the 1.5b logs (copied to `pre15b/` before the regeneration; `TD_PRE=pre15b` selects them in
`tdlib.py`, the only script change), POST = the regenerated sets and `post/supp/`. Outputs `*_15c.txt`. The 52 `.rec`
streams are byte-identical to 1.5b's.

## The boundary sequence (asked at the plan step)
Derived: b unresolved (no member on a boundary tick), b + 1 adequate (the latency tick: s = 1 = s_exp by E9, S = 1),
b + 2 adequate. This conflicted with 1.5b's expectation "unresolved, unresolved, adequate" and with the ruling's first
closing sentence; Hadi corrected the sentence to the initial walk at step 0 and superseded the expectation by
derivation. MEASURED (`b_cases_15c.txt`, B6): every boundary that leaves a task live reads U, A, A (64 groups `UAAAAA`,
one `UAAAE` cut by exhaustion; 15 exhaust); step 0 reads A in all 32 groups. `h_cases_15c.txt`, H5: s01_01 on 78 U,
79 A (item_2 S = 1, the place's latency), 80 A.

## C. False unexplained (`c_findings_15c.txt`) — expected 0 at every α. MET.
0 / 4352 modelled ticks and 0 / 204 phase instances, prior on and prior off, at α = 0.01, 0.05 and 0.1, raw and
lag-corrected; every phase 0. The 1.5b ticks (s02_01 on 248, s04_01 on 269, s03_06 on 89) read adequate, the true
carry walk a member at S = 1. BINDING_ABSENT (the wrong table) unchanged from 1.5b: first unexplained s06_06 48 / 41 /
38, s07_03 39 / 34 / 31 (α .01 / .05 / .10).

A (`a_invariant_15c.txt`): 12,929 ticks, 0 violations (A1–A8).

## D. Decisions against 1.5b (`d_decisions_15c.txt`, `baseline_diff_15c.txt`) — expected: only one-tick-earlier admissions.
Every differing decision is an admission (`built`) that moves from b + 2 to b + 1, the latency tick after a boundary
([IR-boundary] at b checked for each), the leader adequate there on a belief of 0.99x by normalisation and one priced
standing tick. No refusal, trigger kind, winner or selection changed otherwise. Prior ON (all completion ticks
unchanged):

| run | admission 1.5b → 1.5c | hold |
|---|---|---|
| s01_01 | 80 → 79 | 0 |
| s02_01 | 311 → 310 | 0 |
| s03_01 (single_task ×2) | 56 → 55 | 2 (the same hold, one tick earlier; completion 238) |
| s03_01 full_reorder | 56 → 55 | 0 |
| s01_06 | 76 → 75 | 0 |
| s04_01 | 329 → 328 | 0 |
| s03_06 | 123 → 122 | 0 |
| s05_01 (×3), s05_02 | 96 → 95 | 3 (one tick earlier) |
| s06_01 (tb1b, tb1c ×2, tb3 ×2) | 55 → 54 | 0 |
| s06_02 (tb1b, tb3 ×2) | 72 → 71 | 0 |
| s06_03 (tb1c ×2, tb3 ×2) | 98 → 97 | 0 |

APPENDIX, PRIOR OFF: the same move at s03_06 178 → 177, s06_01 173 → 172, s06_02 190 → 189, s06_03 plain 222 → 221
(hold 0), and three admissions whose hold grows as it starts a tick earlier, with the robot's completion later:

| run | admission | hold | completion (world tick) |
|---|---|---|---|
| s01_01 off | 143 → 142 | 31 → 32 (still ends at 173; leader inadequate from 159) | 200 → 201 |
| s06_03 realized / full_reorder off | 222 → 221 | 10 → 12 | 236 → 238 |
| s06_03 single_task off | 222 → 221 | 50 → 51 | 315 → 316 |

The holds are the realization's answer to a projection made one tick earlier (not analysed further). `[IR-dist]` is
identical on every common tick of all 48 runs; four runs end later and add exhausted ticks.

## Runs and tests that disagree with the mechanism
None. Two tests of 1.5b encoded the superseded expectations and were updated by derivation in 3bfc293 (the grasp's
latency tick now a member at S = 1; the boundary sequence U, A, A); dd7a4fd, the condition alone, was committed with
those two failing, as the task staged build and tests in separate commits.

## Cycle 2 inputs recorded (Step 0, 0bc1347)
1.5b finding 2 → TODO-118 (retraction under L); finding 3 → TODO-119 (P, G), with the b + 1 admission above; finding 4
→ the entry's properties; finding 5 → TODO-87; the three flags → TODO-120.
