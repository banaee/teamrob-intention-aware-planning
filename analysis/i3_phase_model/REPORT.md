# I3 — the phase model: a task's likelihood is the likelihood of the action it expects now

Built on `5a8c480` (I2). Sweep: s00 (300 steps), s20 (200), s30 (200), s40 (400) × assignment_prior
off/on, `PYTHONHASHSEED=0`, interpreter `~/python-envs/teamrob-sp4-env/bin/python`. scenario_10 stays
dropped (TODO-52; run once, outside the sweep, for the `waited` check — §6). Baselines recorded at
`5a8c480` before any edit (`baseline/`), byte-identical on the four regression greps to I2's
`logs_instrumented/`.

## How to read this directory

| File | Content |
|---|---|
| `check_i3.py` | Unit checks U1–U5 and the instrumented sweep M1–M6 (wrappers on the robot's live recognizer; its `base` logs cmp equal to `run_mesa.py`'s on the regression greps, verified per condition). `--variants` adds the analysis-only monkeypatches `ungated` and `ownshelf` (§5). Writes `summary.md` and the CSVs. |
| `summary.md` | Unit-check results; per condition: kernel/completion call counts vs evaluations (criterion 5), phase advances, completions, θ crossings, `waited` ticks vs the executor's bound entity; the variants' crossings. |
| `sweep.sh` | `sweep.sh <repo_root> <out_dir>`: the eight conditions through `run_mesa.py`. Used for `baseline/`, `stage1_zone/`, `stage2_held/` (worktrees of `5a8c480` with one-line patches) and `new/` (HEAD). |
| `baseline/`, `stage1_zone/`, `stage2_held/`, `logs_instrumented/nopin/`, `new/` | The replay stages S0 → S1 (ZONE_BOOST = 1.0) → S2 (S1 + held-item rule returns ∅) → S3 (HEAD with `_terminal_complete` patched to False) → S4 (HEAD). |
| `diffs/` | `diff_ir.py` (I2's, unchanged) between consecutive stages and base → new, per condition. §3 is written from these. |
| `expected_actions.csv` | Per condition, tick, hypothesis: the expected action and its origin (step −1 is the priming observation). |
| `phase_advances.csv` | Every change of expected action (tick, hypothesis, from, to). |
| `completion_events.csv` | Every firing of the completion channel: tick, microaction, hypothesis, judged action, predicate, likelihood, output belief. |
| `completions.csv`, `rival_phase.csv`, `waited_ticks.csv` | Terminal completions; what every `deliver_item(Y≠X)` expected while the human held X; `waited(human_0, ·)` ticks against the entity the executor's own `wait_at` was bound to. |

---

## 1. What changed and where

One file in the cognitive layer: `shared/recognizer.py` (559 lines changed). Nothing in `mesa_sim/`,
`domains/`, `shared/planner.py`, `shared/likelihood_functions.py`, `shared/target_resolution.py`. Human
and robot per-step lines are byte-identical to baseline in all eight conditions (the simulation side,
including `wait_at` timing, is untouched).

| what | where |
|---|---|
| Per-hypothesis state: `_expected[key]` (the `GroundedAction` expected last tick, or None), `_origin[key]` (position when it became expected), `_base[key]` (evidence with closed phases and events folded in, one common scale), `_completed` (latched). No index into any action list. | `IntentionRecognizer.__init__` |
| `update()`: per live hypothesis — decompose (I2) → terminal completion? → retire; derive the expected action (first whose completion does not hold); completion channel on the action expected BEFORE the event when the microaction is in its vocabulary (multiplies into `_base`); on a change of expected action fold the closing action's final chord into `_base` and move the origin; the open action's chord from the origin multiplies on top for this tick only. One normalisation over live keys + `unknown`; `_base` rescaled by the same total. | `update` |
| `_expected_action`, `_terminal_complete`, `_same_action` (name + grounded bindings), `_in_vocabulary` (the schema's own list) | new, static |
| `_completion_likelihood`, `_progress_likelihood`: memoised per tick by inputs — the grounded predicate; (evaluator, origin, target position). | rewritten, static |
| `_output`: evidence × ω_context, pin inadmissible ∪ completed, floor. ω keeps the two context branches only. | `_output`, `_context_weight` |
| `[IR-complete] step=N <key> completed: <predicate> holds` — one line per retirement. | `update` |
| DELETED: `_refuted_by_holding`, `ZONE_BOOST`, `_target_zone`, `_leg_base`, `_leg_start_pos`, `_discrete_microactions`, `_weigh`, `_likelihood`, the stray `importlib.metadata` import (I1 O7, in the rewritten module). | |

Unchanged by instruction: the cosine kernel, HIGH 4.0 / LOW 0.1 / NEUTRAL 1.0, the assignment mask,
BELIEF_FLOOR = 1e-3, the two `_context_weight` task names, θ, the meta-planner, `_history`,
`CONFIDENCE_THRESHOLD` (unused), the commented-out old `build_hypothesis_space` (dead).

Three places where the algorithm as spelled out per tick was realised differently, each recorded in
`design_decisions.md`:

1. **The completion channel is judged on the action expected before the event.** The expected action
   is derived against the post-event world; after a grasp `holding` already holds, `pick_up` reads as
   complete and the derived action is `move_to(table)`. "HIGH if the derived action's completion
   holds" can never be true by construction. So at an event the check runs on `_expected[key]` from
   the previous tick. (Check U4.)
2. **`_base` is kept in one common scale, not as each hypothesis's normalised value at its own advance
   tick.** The latter carries that tick's normaliser into cross-hypothesis ratios: in s00 a rival whose
   phase flips at 43 (where item_3's chord is 4.0 and the tick total ≈ 3.6) would be charged ×3.6
   relative to item_3 for nothing. Rescaling every base by the tick total keeps Σ base·chord = 1 and
   makes the result exactly the product over each hypothesis's own segments.
3. **The floor is applied on output only.** Step 6 of the algorithm puts it there; the old code
   re-floored the evidence state at every leg base (a once-per-leg recovery clamp). With nothing
   feeding back, the evidence state is normalised but not floored.

No odometer (dropped per the follow-up instruction; I4 brings it with the term that reads it).

## 2. Verification

- Eight conditions, no traceback, no `not decomposable` warning. `check_i3.py`: all unit checks PASS;
  instrumented logs equal `run_mesa.py`'s on `[IR]`/`[IR-dist]`/`[meta]`/`[meta-cand]` in all eight.
- Hash-seed independence: s40_off byte-identical on the four greps under `PYTHONHASHSEED` 0/1/7;
  s40_on re-verified after the last edit.
- Wall time unchanged (s40, 400 steps: 2.6 s). dock_loading registry imports.
- Criterion 5 in the sweep (`summary.md`): progress calls / kernel evaluations = 510/426, 220/212,
  564/428, 176/168, 626/488, 195/187, 1773/1567, 1009/971 — every shared value is one evaluation;
  completion calls 2/2 in every condition (one per grasp).

## 3. Attribution of every difference, by stage

Stages: S1 = ZONE_BOOST off; S2 = S1 + held-item rule off (both one-line patches on `5a8c480`);
S3 = phase model without the terminal pin; S4 = HEAD. Columns give changed ticks (|Δ| > 5·10⁻⁴),
the ticks where `most_likely` differs, and the largest single change.

| condition | S0→S1 ZONE_BOOST | S1→S2 held-item rule | S2→S3 phase model (no pin) | S3→S4 terminal pin |
|---|---|---|---|---|
| s00_off | 75 ticks from 16; winner 16–21; max item_3 +0.126 @103 | 68 from 41; winner 111–112; item_2 0.796→0.120 @111 | 128 from 41; winner 113; item_3 0.106→0.745 @113 | 138 from 31; winner 78–113, 142–168; item_3 0.988→0.001 @78 |
| s00_on | 56 from 16; winner 16–21; item_2 −0.170 @16 | 68 from 41; winner 111–112; item_3 0.001→0.804 @111 | 128 from 41; winner 113; item_3 0.11→0.76 @113 | 91 from 78; winner 78–113, 142–168; item_3 0.991→0.001 @78 |
| s20_off | 49 from 4; winner 4–10; item_3 0.801→0.668 @54 | 175 from 22; winner 89–90; item_2 0.766→0.103 @89 | 178 from 22; winner 91 | 148 from 52; winner 54–91, 122–199; item_3 0.984→0.001 @54 |
| s20_on | 49 from 4; no winner change; item_3 0.770→0.627 @11 | 65 from 22; winner 89–90 | 178 from 22; winner 91 | 146 from 54; winner 54–91, 122–199 |
| s30_off | 133 from 19; winner 19–22 | 69 from 39; winner 98–99 | 130 from 39; winner 100 | 95 from 74; winner 74–100, 121–168 |
| s30_on | 129 from 23; none | 58 from 39; winner 98–99 | 129 from 39; winner 100 | 94 from 74; winner 74–100, 121–167 |
| s40_off | 314 from 0; winner 60–64; coffee 0.549→0.379 @60 | 114 from 60; none; coffee 0.962→0.799 @272 | 319 from 60; winner 118–378; item_3 0.049→0.972 @274 | 264 from 115; winner 115–378; item_3 0.986→0.001 @266 |
| s40_on | 314 from 0; winner 60–64 | 114 from 60; none | 319 from 60; winner 118–378 | 264 from 115; winner 115–378 |

**S1 — ZONE_BOOST.** Output-only, so every change is a ×2 appearing or vanishing with a quadrant
crossing: the t=16–23 winner flips in s00/s30 (the human crosses into the shelf's quadrant), s20_on's
step-11 crossing (0.770 → 0.627, the crossing is gone — as I1 predicted), s40's t=0 boosts (the human
starts in zone_NE with item_7's shelf) and the 142 coffee crossing (item_3 at the table losing ×2
when the human leaves zone_NW: coffee 0.811 → 0.550, no crossing). θ crossings after S1: s00_on loses
111, s20_on keeps only 22, s40 keeps only 210 (`summary` of `[meta]` lines).

**S2 — held-item rule.** Output-only. The rivals are no longer pinned during a carry, so they show
their evidence: during the carry ≈ 0.01–0.05 each (their I2 carry-leg evidence, `deliver_with_return`
against them), and at the grasp tick the held item no longer jumps (s00_on item_3 0.804 → 0.001 at
111 is the S1-stage pin of item_3 by the grasp of item_2 coming back as 0.804 without the pin). All
grasp-tick crossings vanish (41/22/39 → none); the carry tick crosses instead (43/24/41).

**S3 — phase model, no pin.** Every difference starts at the first grasp (41/22/39/60). Mechanisms,
each measured:

1. *Completion evidence fires* (`completion_events.csv`): at every grasp the grasped item's hypothesis
   expected `pick_up(item)`, GRASP is in its vocabulary, `holding(human_0, item)` holds → 4.0. Sixteen
   firings in the sweep (two per condition), all 4.0, none LOW. At the grasp tick the held item now
   moves ×4 against everyone: s00_off 0.261 → 0.586, s00_on 0.500 → 0.799, s20_off 0.245 → 0.565,
   s20_on 0.627 → 0.869, s30_off 0.213 → 0.520, s30_on 0.469 → 0.778, s40_off 0.304 → 0.636,
   s40_on 0.398 → 0.725. Before I3 the grasp tick was 1.0 for everyone (0.797 came from pinning
   rivals). Releases fire nothing: the terminal completion holds on the same tick and the pin
   preempts the channel (in S3, with the pin disabled, `place`'s check would fire but the human's
   task is over anyway).
2. *Rivals' phases flip through `deliver_with_return`* (`rival_phase.csv`, `phase_advances.csv`):
   at the grasp of X every `deliver_item(Y)` goes `move_to(item_Y)` → `place(X, shelf_X)` (the
   approach chord is folded; two NEUTRAL ticks while `at(human, shelf_X)` holds) → `move_to(shelf_X)`
   from an origin 30–50 cm on the table side of the shelf (chord ≈ 180° off, ≈ 0.1 for the carry,
   folded at the release) → `move_to(item_Y)` from the table. §5.
3. *The carried item's own chord* is measured from the grasp position toward the table (4.0) and
   the delivered item, in S3 (no pin), keeps 0.96–0.99 for the rest of the run — the I2 lead, now
   without the ZONE_BOOST half (0.975 vs 0.966 mid-carry).
4. *Origins are per hypothesis and never closed by a stop*: within a straight approach the values are
   flat to the third decimal as before; the priming leg is identical to I2's because nothing in it
   changes an expected action.

**S4 — terminal pin.** Every difference starts at a completion: the human's releases (78/54/74/115,
142/122/121/331) and, prior-off, the robot's deliveries (s00_off 31, 93, 166; s20_off 52, 136;
s30_off 96, 166; s40_off 145, 243, 376) and `coffee_break` at 184. The delivered item goes to 0.001
on the release tick and the live set renormalises; everything after a release in every condition is
a consequence (winner ranges in the table).

Downstream, θ crossings base → new (the human's task at the crossing in parentheses):

| condition | base (I2) | new | reading |
|---|---|---|---|
| s00_off | 41, 111 | **43**, **113** | grasp ×4 against five live items is 0.586 (< θ); the first carry tick crosses |
| s00_on | 41, 111 | 41, 111 | identical ticks; 0.799 / 0.880 instead of 0.797 / 0.796 — different mechanisms (completion ×4 vs pin) |
| s20_off | 22, 89 | **24**, **91**, **136** | as s00_off; 136 is `unknown` crossing θ (0.804) when the robot's delivery pins item_6 — TODO-54 |
| s20_on | 11, 89 | **22**, 89 | 11 was ZONE_BOOST; the grasp crosses (0.869) |
| s30_off | 39, 98 | **41**, **100** | as s00_off |
| s30_on | 39 only (TODO-48 flip at 98) | 39, **98** | item_3 pinned at 74, so item_7's grasp is a crossing (0.885) |
| s40_off | 142 coffee, 210 coffee | **62** item_3, **326** item_6 | 142/210 were ZONE_BOOST / foreseeable-attractor events; coffee never reaches θ (§4); item_6 crosses on its carry |
| s40_on | 142, 210 | **62**, **325** | same |

Robot behaviour: the `[meta]` winners and queues are unchanged in all eight conditions (`diffs/*`:
the meta diffs are trigger steps, `[meta-proj]` admissions and candidate conflict counts, never a
different winner). `projection=built` 5 → 4 (s00_off), 6 → 3 (s40_off).

## 4. scenario_40 after I3

`[IR-complete]`: item_3 at 115, coffee_break at 184, item_6 at 331 (and prior-off the robot's
item_4 145, item_7 243, item_5 376).

| tick | event | off | on |
|---|---|---|---|
| 60 | grasp item_3 | item_3 0.636 (coffee 0.131) | 0.725 (coffee 0.149) |
| 62–114 | carry | item_3 0.875 → 0.927 | 0.911 → 0.929 |
| 115 | release — item_3 pinned | **coffee 0.646** most_likely, unknown 0.200 | coffee 0.687 |
| 118–141 | coffee walk | coffee 0.551 → 0.508 (ac 0.07 → 0.20) | 0.645 → 0.569 |
| 154–183 | wait | coffee 0.514 (expects `wait_at`, NEUTRAL) | 0.559 |
| 184 | `waited` — coffee pinned | **ac 0.451**, unknown 0.264, item_5 0.145, item_6 0.111 | ac 0.544, unknown 0.318, item_6 0.133 |
| 187–229 | wander | ac 0.46 → 0.53 → 0.51 | 0.55 → 0.63 → 0.61 |
| 231–271 | approach shelf_6 | ac 0.51 → 0.615, item_6 0.105 → 0.094 | ac 0.61 → 0.69, item_6 0.125 → 0.106 |
| 272 | grasp item_6 | ac 0.479, **item_6 0.294** | ac 0.525, item_6 0.322 |
| 274 | first carry tick | item_6 0.623 | 0.654 |
| 325/326 | θ | item_6 0.746 → crossing | 0.751 |
| 331 | release — item_6 pinned | unknown 0.607, ac 0.329 | unknown 0.645, ac 0.349 |

Against I2's §9(b) success criterion:

- `coffee_break` ≥ θ during 118–186: **no** (max 0.551 off / 0.645 on, at 118, then falling). I2's
  0.81 at 142 was a ZONE_BOOST event on item_3. Under the cosine kernel the coffee walk from the
  table is 4.0 for coffee, but item_5 (bearing 50° off) and item_6 (58°) score 3.2 and 2.9 and
  `unknown` 1.0; coffee cannot exceed ≈ 0.55 here whatever the phase model does. The walk IS
  recognised (most_likely throughout, 0.51–0.65).
- At BELIEF_FLOOR from 187 on: **yes, from 184** — the pin on the first `waited` tick, never lifted
  (TODO-50 closed). Not a decay.
- No `deliver_item` ≥ θ during 187–229: **yes** (max item_5 0.134).
- item_6 `most_likely` by the grasp at 272: **no** — 0.294/0.322 at the grasp, `ac_activation` leads
  at 0.479/0.525; item_6 leads from the first carry tick (274). Cause (TODO-53): `ac_activation`'s
  expected action never changes, so its origin is still the start position (100, 550) and its whole
  history is one chord start → current position, replaced each tick — start → shelf_6 is 39° off the
  switch's bearing (L ≈ 3.5), and it was never charged for the 270 ticks of walking elsewhere.
  item_6's origin was reset to the table at 115 and its base carries the ×0.1–0.3 carry fold.
  The same asymmetry makes coffee `most_likely` at 115–117 before the coffee walk begins. This is
  the thing I4's path-cost term charges; it is not patched here.

## 5. Acceptance

| # | criterion | evidence |
|---|---|---|
| 1 | every difference attributed | §3 stage table, `diffs/` per condition, CSVs. No unexplained difference. |
| 2 | `deliver_with_return` rival-targeting effect GONE | **NOT MET — and not attainable under the design as specified.** `rival_phase.csv`: while the human holds X, `deliver_item(Y)`'s expected action is `place(X, shelf_X)` (2 ticks) then `move_to(shelf_X)` in every carry of every condition; criterion 2's "deliver_item(Y) at phase 0 must expect move_to(shelf_Y)" is false by construction, because the guard-selected method is `deliver_with_return` and its phase 0 is `move_to(home_container_of(X))`. The rival's carry evidence is ≈ 0.1 (s00_on item_2 0.148 → 0.007 from 41 to 44, while unknown goes 0.050 → 0.015). Crossings: s00_on 111 (I2 111, base 81), s20_on 89 (89, 82), s30_on 98 (none, 77) — the pin restores s30_on's crossing but none moves back, because after the release the rival fights `unknown` from a 1 : 3–8 deficit at ×4 per leg. The direct check I2 asked for — the rivals' evidence at the release — is that deficit, so the pin is not masking the effect; the effect is the method. Variant `ownshelf` (rivals decomposed as if nothing were held, analysis only) gives s00_on 97, s20_on 77, s40 item_6 ≥ θ at its grasp (272/274), and s30_on loses its crossing (item_7 at 0.795 at the release of item_3, 74 — shelf_7 is 39° off the carry, TODO-38's collinear decoy). Decision surfaced as TODO-55 with three readings. |
| 3 | `coffee_break` releases (TODO-50) | `[IR-complete] step=184 coffee_break … waited(human_0, coffee_machine_0) holds`; 0.001 from 184 to the end in both settings (was 0.96 at 272). No decay. Pinned on the first `waited` tick; the fact clears at 187 and the latch holds (check U3). |
| 4 | no domain predicate decides a phase | `holding` appears in `recognizer.py` only inside docstrings/comments (check U5 greps the code for `"holding"`, `"in_zone"`, `"at"`, `"obj_at"`, `"waited"`, `"?item"`, `"move_to"`, `ZONE_BOOST`, `_refuted_by_holding`: none). The only reads of the world are `predicate in world.predicates` on planner-grounded predicates, and the vocabulary test is against the action's own schema list. |
| 5 | identical expected action → identical likelihood, once | Check U1: two items on one shelf, P(a) = P(b) = 0.4444, one kernel evaluation. Sweep: the memo key is (evaluator, origin, target position) / (predicate), so sharing is by inputs, stronger than by action identity; 84 / 8 / 136 / 8 / 138 / 8 / 206 / 38 of the progress calls per condition were served from the memo (§2). |

## 6. `waited` attribution check

`waited_ticks.csv`: every `waited(human_0, X)` tick compared with the `?entity` binding of the
`wait_at` the human's executor was executing. s40 off/on: 184–186 coffee_machine_0, 207–209 wander_0,
228–230 wander_1 — all equal to the bound entity. s10_off (env_layout1: coffee machine (−975, −275)
and AC switch (−975, −350), 75 cm apart): 158–160 coffee_machine_0, equal to the bound entity. No
misattribution in any scenario, so the executor is not changed. The reason it holds: `at()` completes
the approach within 30 cm of the target, and 30 < 75/2; a layout with two fixed objects closer than
twice PROXIMITY_THRESHOLD would break it, and then the fix is the one the task names (record the
bound entity, not the nearest object). s10_off reached step 260 and then raised TODO-52's latent
`RuntimeError` (θ crossing on item_4 at its grasp at 257, 0.822; every candidate excluded on the
carry tick) — the crash the TODO said would return when the belief changed. Dropped scenario;
recorded in TODO-52.

## 7. What the first-ever firing of completion evidence did

Sixteen firings (`completion_events.csv`), all at grasp ticks, all HIGH (4.0), all for the hypothesis
that expected `pick_up(grasped item)`. Output at the grasp tick, I2 → I3: s00_off 0.797 (pin) → 0.586;
s00_on 0.797 → 0.799; s20_off 0.797 → 0.565; s20_on 0.797 → 0.869; s30_off 0.797 → 0.520; s30_on
0.797 → 0.778; s40_off 0.549 → 0.636; s40_on 0.549 → 0.725; second grasps: s00_off 0.970 → 0.707,
s00_on 0.796 → 0.880, s20_off 0.928 → 0.502, s20_on 0.766 → 0.860, s30_off 0.976 → 0.749, s30_on
0.876 → 0.885, s40 0.986/0.962 → 0.294/0.322. The value is ×4 against every live rival and `unknown`;
with one live rival (prior on) that is ≥ θ, with four or five (prior off) it is not and the carry tick
crosses two ticks later. No LOW was ever produced in the sweep — no two hypotheses expect a grasp at
the same tick in these layouts (check U4 shows the ×40 when they do). Releases never reached the
channel: the terminal pin fires first. The ungated reading of the channel (every expected action
judged at a discrete tick) was measured and rejected (§1 of `design_decisions.md`, TODO-56): `unknown`
0.96–0.99 after every release, no second crossing anywhere.

## 8. For I4, before it replaces the kernel

1. **The origin is where I4 plugs in, and it is per hypothesis.** `_origin[key]` is the position at
   which the hypothesis began expecting its current action; `_progress_likelihood(action, origin, pos,
   world, memo)` is the one place the kernel is called, with the memo key built from its inputs. A
   path-cost likelihood needs the distance walked since the origin: add an odometer per observed
   agent in `update()` and store `_origin_odo[key]` beside `_origin[key]`, reset at the same place.
2. **The stuck-origin asymmetry (TODO-53) is I4's to close, and it is load-bearing in s40.** A
   hypothesis whose expected action never completes is scored on one chord from t=0 and never pays
   for the detour; with the cosine kernel it wins s40 from 184 to 271 (`ac_activation` 0.45–0.69)
   and keeps item_6 below the lead at its grasp. The excess path since the origin is exactly the
   quantity that charges it. If I4 does not, the alternative is an origin reset on the observed
   agent's task boundary (the `[IR-complete]` event), which is a design decision, not a kernel.
3. **The carry refutation of rivals is ≈ ×0.1 per carry and it is the method's doing** (TODO-51/55).
   I4 changes its magnitude (a rival's path cost to shelf_X while the human walks to the table), not
   its sign. Whether the next task should be revealed before its grasp is therefore not a kernel
   question; the candidates are in TODO-55.
4. **`unknown` pays nothing.** Every asymmetry measured in the variants traces to `unknown`'s flat
   likelihood: it wins after every release (0.38–0.71 in the shipped code), it crosses θ when a pin
   shrinks the live set (TODO-54), and it would sweep everything under the ungated channel
   (TODO-56). If I4 gives `unknown` a likelihood of its own, the completion-channel gate should be
   revisited with it.
5. **The grasp tick is ×4 for exactly one hypothesis**; I4 need not touch the completion channel.
6. **No floor feedback remains in the evidence state.** A hypothesis can now be arbitrarily far
   below the floor in `_base`; only the output is floored. Under the cosine kernel the deepest value
   seen is ≈ 10⁻³ of the total (s00_on item_2 during the carry); a sharper kernel will go deeper and
   recovery then takes as many legs as it took to fall.
7. **Regression greps** at this commit are byte-identical across `PYTHONHASHSEED` 0/1/7 on s40.

## Flagged, not fixed (outside scope)

- `shared/recognizer.py`: `CONFIDENCE_THRESHOLD` unused (I1 O8); the commented-out old
  `build_hypothesis_space` block; `_history` grows without bound.
- `mesa_sim/executor.py` `_execute_stand`: the nearest-fixed-object rule for `waited_at` is correct in
  every current layout (§6) but is a proximity heuristic for a fact the executor holds (the
  `?entity` binding); it breaks for two fixed objects closer than 2 × PROXIMITY_THRESHOLD.
- `shared/meta_planner.py`: `theta_crossed` fires on `unknown` (TODO-54); TODO-52's crash returned in
  s10 at step 260.
- `docs/io_contracts.md` §2.1/2.2 not updated (the task named the two docs that were).
- `CLAUDE.md` still lists `--assignment_prior` and PYTHONHASHSEED guidance unchanged; the recognizer
  no longer depends on the seed (re-verified here) but other consumers were not checked.
