# T9 — Projection ends where the executor stops; new baselines over ten conditions

> Superseding note (T-L stage 3, 26 Sept 2026): the layout and scenario ids here are the old ones; `docs/rename_table.md` maps them to the serial ids. The scripts and records stay frozen at their commit.

> Superseding note (24 Sept 2026, the terminology ruling; `docs/glossary.md` §7, `docs/terminology_revision.md`): "the coffee break is recognised at 123", "recognised at 334 / 314" → the hypothesis clears θ at that tick (ROBOT).

Code before: `aefebc7` (R1 docs; projection walks to the target point). Code after: HEAD (this
directory's commit). Ten runs per side, `PYTHONHASHSEED=0`: s00 (`env_layout0`, 300 steps), s10
(`env_layout1` as cleaned at R1, 450 steps), s20 (200), s30 (200), s40 (400) × assignment prior
off/on. Nothing in the meta-planner changed: `min_safe_distance = 1.0` is still live and the
all-candidates `RuntimeError` is still in the code. No condition raised.

Units: ticks (1 tick = 20 cm of motion; a stationary action 1 tick), distances in cm. "Lead" of a
placement = (trigger + projected start of the `place` segment) − the tick on which the executor
executed the release; positive = execution ahead of projection.

## How to read this directory

| File | Content |
|---|---|
| `sweep.sh` | The ten conditions → `<out>/<cond>.log` (logs are git-ignored; regenerate with it). |
| `compare.py` | `baseline/` vs `new/`: decision sequence, first `[IR]` difference, `[meta-cand]` differences, full-log identity minus `[meta-cand]`/`[sep]`, actual separation. Writes `comparison.md`. |
| `timing.py` | Projection vs execution per placement, from a T1b-style `captures.json` and the logs. `timing_baseline.md` (T1b's captures + `baseline/`), `timing_new.md` (`captures_new/` + `new/`). |
| `stop_distance.py` | The executor's real stopping distance per completed walk, per agent, from a log. |
| `baseline/`, `new/` | The logs (git-ignored). `new/` are the baselines for T3, T4 and T10. md5s below. |
| `captures_new/` | T1b's `measure.py --out` re-run on the new code (git-ignored). |

## What changed in the code

- `shared/trajectory_algorithms.py`: `arrival_point(start, end, radius)` — the point `radius` short
  of `end` along the line, or `start` when already inside the radius. Pure geometry.
- `shared/projection.py`: `Projector(arrival_radius=0.0)`; `build_segments()` ends every walk at
  `arrival_point(current, target, arrival_radius)` and projects the next action from there. The 0.0
  default is a unit-less placeholder (walk to the point), as `assumed_speed = 1.0` is.
- `mesa_sim/sim_agents.py`: the body passes `arrival_radius=PROXIMITY_THRESHOLD` (imported from
  `world_state_builder.py`, the constant that makes `at(agent, object)` true — one constant, one
  source). The human's projection goes through the same `Projector` instance, so it gets the same
  treatment automatically.
- `mesa_sim/run_mesa.py`: one `[sep] step=<n> robot_0-human_0 dist=<cm>` line per tick in the
  headless run (end-of-tick positions). Measurement only.

## The premise, measured (T1b's "not measured" item)

Does the human's execution stop short? Yes: the human runs the same `Executor` and completes a
`move_to` on the same `at` predicate. Real stopping distances over the baseline logs
(`stop_distance.py`, distance from the stop position to the nearest object):

| layout | robot: walks, min / median / max | human: walks, min / median / max |
|---|---|---|
| env_layout0 | 12: 11.8 / 21.5 / 28.0 | 8: 14.8 / 19.1 / 27.3 |
| env_layout1 | 16: 15.3 / 19.6 / 29.1 | 12: 10.1 / 19.9 / 28.7 |
| env_layout2 | 10: 15.0 / 21.5 / 29.3 | 8: 11.7 / 21.8 / 29.4 |
| env_layout3 | 8: 11.5 / 18.5 / 28.6 | 8: 12.1 / 17.9 / 21.0 |
| env_layout4 | 12: 10.4 / 16.0 / 27.9 | 14: 11.8 / 16.4 / 29.3 |

Every walk ends inside 30 cm; the stop is the last discrete 20 cm step that lands inside the radius,
so it sits 10–29 cm from the target, not at 30. The projection now stops at exactly 30; the executor
walks on average ~0.5 tick further.

Was execution "1 to 2 ticks ahead of projection"? Only for the robot's full-task rows, and only as
the net of opposing errors. Placement lead before the change (`timing_baseline.md`):

| rows | n | lead min / median / max |
|---|---|---|
| robot, 4-segment plan (trigger before the grasp) | 31 | −0.98 / +1.25 / +2.19 |
| robot, 2-segment plan (trigger after the grasp) | 30 | −0.48 / −0.17 / +0.40 |
| human, 4-segment projection | 18 | −1.89 / −1.18 / +0.35 |
| human, 2-segment projection | 21 | −1.26 / −0.71 / −0.57 |

The human was already BEHIND the projection by about a tick. The reason is in the executor, not the
geometry: it spends one tick ACKNOWLEDGING each completed action (the tick on which `at`/`holding`
is seen true and the cursor advances, `micro=None` in the log), so a delivery pays three
acknowledgement ticks before its release (move_to, pick_up, move_to). The robot pays two: its
`task_committed` trigger fires on the grasp's acknowledgement tick and the continue loads a
`deliver_already_held` plan whose first action starts at once (T5, design_decisions.md). The
target-point projection over-estimated each walk by 1.5 ticks (30 cm), which cancelled most of
that for the robot and left the human a tick behind.

After the change (`timing_new.md`), no row has execution ahead:

| rows | n | lead min / median / max |
|---|---|---|
| robot, 4-segment | 37 | −4.55 / −3.32 / −2.26 |
| robot, 2-segment | 29 | −1.98 / −1.46 / −1.00 |
| human, 4-segment | 16 | −6.39 / −5.32 / −4.07 |
| human, 2-segment | 22 | −2.89 / −2.21 / −2.07 |

The remaining offset is fully accounted for by three things the projection does not model, all on
the body side: (a) the acknowledgement tick per completed action — robot 1 (2-segment) / 2
(4-segment), human 1 / 3; (b) per walk, the executor's discrete steps (`ceil`) and its real stop
10–29 cm from the target rather than at 30 — together 0 to ~1 tick per walk, later; (c) for the
human only, one more tick: within a tick the human moves before the robot observes, so the human's
projection starts from its position AFTER the trigger tick's step while the robot's own projection
still includes the trigger tick. The row medians match this decomposition (robot 2-seg −1 − 0.5;
4-seg −2 − 1.3; human 2-seg −2 − 0.2; 4-seg −4 − 1.3). None of these is the arrival radius;
all three are flagged, not fixed (TODO-77 below).

## Decision-sequence changes and their mechanisms (`comparison.md`)

Unchanged in s00, s10, s40 (both priors): every `[meta-cand]` line changes (costs fall by ~1.5 ticks
per remaining walk — 4 for a full delivery, 1–2 after the grasp — and `min_dist` values move), the
argmin does not. Everything else in those six logs is byte-identical apart from `[meta-cand]` and
`[sep]`.

Changed at exactly the four triggers T1b's Anomaly 3 identified — the T2 exclusions:

| condition, step | before | after | why |
|---|---|---|---|
| s20_off 20 | item_4 `feasible=False min_dist=0.0` → item_6 wins (56) | item_4 `feasible=True min_dist=9.6`, wins (30) | see below |
| s20_on 6 | item_4 excluded (0.0) → item_6 (65) | item_4 9.6, wins (44) | same |
| s30_off 28 | item_4 excluded (0.0) → item_2 (59) | item_4 16.6, wins (43) | same |
| s30_on 21 | item_4 excluded (0.0) → item_2 (66) | item_4 15.4, wins (50) | same |

Mechanism: `min_dist = 0.0` was an artefact of projecting every walk to the table's one point. Both
agents' `place` segments sat at the identical point in overlapping ticks whenever their arrivals were
within a tick, so `min_safe_distance = 1.0` excluded the candidate (T2's consequence, TODO-30). With
each walk ending 30 cm short of the table along its OWN approach line, two agents converging from
different directions are projected ~2·30·sin(θ/2) apart at their placements (9.6 cm in s20, 15–17 in
s30) — above 1.0, so nothing is excluded, and item_4, the cheapest, wins as the pure cost argmin
always did. T1b's `cost_winner` column already predicted these four flips. The exclusion is gone from
all ten conditions: no `feasible=False` anywhere in `new/`.

Downstream of those flips (same conditions): the robot delivers item_4 first, so every later trigger
step, pool and winner shifts — s20_off ends at 182 instead of 190; s20_on at 182 instead of 176 (the
prior-on run had picked the short item_6 first); s30 both at 154 instead of 157/159; s30_off's
`[meta-pool]` drop of item_2 at 87 (TODO-67's case) no longer occurs because item_2 is still the
robot's own queued task there. The comparison lists every added/removed decision.

`[IR]`/`[IR-dist]`: byte-identical in s00, s10, s40 (both) and s20_on. They differ in s20_off from
step 52 and in s30_off from 74, and s30_on's are a prefix (155 vs 160 lines). None of this is the
recognizer reading projected positions — it reads none. The differences follow the changed
decisions through WORLD facts: the robot now delivers item_4 at 51 (s20_off) / 73 (s30_off) instead
of item_6 at 59 / item_2 at 85, and the completion pin (I3) retires the human's item_4 hypothesis on
the following tick, redistributing the belief. Prior-on the human's live set does not contain item_4
(support restriction), so s20_on's belief is untouched and s30_on's only ends five ticks earlier
with the robot.

## scenario_10 on the cleaned layout (fresh description; no previous comparable baseline)

Robot pool item_4 / item_1 / item_7 / item_6 from (200, 0); human item_2 → coffee_break → item_5 →
ac_activation, the human's tasks completing before ticks 77, 156, 313 and 367. Both priors, before
and after T9, give the SAME decision sequence: item_7 (70 ticks, the cheapest) at 0 → item_6 at 75 →
item_1 at 167 → item_4 at 283 → all tasks complete at 420. No trigger excludes anything (min
`min_dist` at an admitted trigger 42.8 cm, s10_off 29, item_7's carry against the human's item_2
carry), no `RuntimeError`, no `[meta-pool]` drop. Prior-off the human's item_2 crosses θ three times
during its grasp stop (29 / 33 / 35, TODO-68's shape) and the coffee break is recognised at 123
(0.83) while the robot carries item_6, prior-on once each (25, 123); the ac_activation walk is
recognised at 334 / 314. `theta_crossed` at 163 (prior-on) fires with the robot one tick from its
release (item_6 cost 1). scenario_10 no longer has the property TODO-52 recorded (an
every-candidate exclusion at the human's item_4 grasp): item_4 is not in the human's script any
more and the robot's item_4 delivery, last in its sequence, runs against the human's ac_activation
projection at 1150–1575 cm.

## Actual robot–human separation (`[sep]`, new logs) against 50 cm

| condition | robot done | min during execution (tick) | ticks < 50 cm during execution | min after both idle |
|---|---|---|---|---|
| s00_off / s00_on | 166 / 168 | 8.2 (163) | 5 / 7 (161–165 / 167) | 8.2 |
| s10_off / s10_on | 420 | 30.9 (73) | 4 (72–75) | 992 |
| s20_off / s20_on | not within 200 | 11.6 (51) | 13 (49–54, 133–139) | – |
| s30_off / s30_on | 154 | 11.0 (22) | 18 (21–24, 69–76, 148–153) | 25.3 |
| s40_off / s40_on | 378 | 4.6 (373) | 7 (371–377) | 4.6 |

Every condition goes below 50 cm during execution; the minima are 4.6–30.9 cm. Where: the s30 mirror
crossing at 21–24 (the two agents pass 11 cm apart, mid-walk — T1b's "approach/approach" case); the
table convergences (s20 49–54: the robot releases at 51 while the human arrives; s30 69–76; s10
72–75, the human walking in as the robot releases); and the END of each run, where whoever finishes
last places at the table next to an agent already standing there (s00 161–165, s20 133–139, s40
371–377). After both are idle the agents stand 4.6–25 cm apart for the rest of the run (s00, s40),
which is a fixture property (everyone ends at the table, TODO-74), not an execution event. Before
the change the numbers are the same in s00 / s10 / s40 and differ in s20 / s30 only through the
changed decisions (`comparison.md`). Mesa has no avoidance; these are the overlaps the assumption
"execution-time avoidance past T_h" leaves to a later layer (TODO-73).

## Verification

1. `baseline/`: the eight previous conditions are byte-identical to `analysis/t5_continue/new/` (md5
   7897fe99, 5ceb40dc, 395897bc, 1713f90e, d76ceeab, dc6e183b, 6b3e75ae, 07ecdc0f); s10 baseline
   c45116fd (off) / 3fe133e6 (on).
2. `new/` (the T3/T4/T10 baselines): s00 c60aeac6 / 994d8a5b, s10 bff8b468 / b1101e98, s20 522c3772 /
   aff89ddb, s30 f74121c2 / 3f40a04e, s40 608b5346 / 05bf6dbe (off / on).
3. Instrumentation is neutral: T1b's `measure.py` re-run on the new code writes logs byte-identical to
   `new/` minus the `[sep]` lines in all eight conditions it covers.
4. `arrival_point` with radius 0 returns the target point exactly, so a `Projector` constructed with
   the default reproduces the old geometry (checked by hand on three cases).
5. `domains/dock_loading` still imports (run_mesa.py imports its registry; every run above went through it).
6. R1 changed no behaviour: the ten baseline logs were generated after the R1 edits and match T5.

## Flagged, not fixed

- **TODO-77 (new): projection still runs ahead of execution by the executor's acknowledgement ticks**
  — one tick per completed action, plus step quantization and the human's one-tick observation
  offset (above). With the arrival radius in place the placement lead is −1.0 to −6.4 ticks, never
  positive. Whether to model the acknowledgement tick in the projection (a body-supplied per-action
  overhead, like `default_action_cost`), remove it from the executor, or accept it, is a decision;
  it changes every cost and every T_h by 1–4 ticks and therefore belongs before T3's validation
  numbers are read as exact.
- The `min_safe_distance = 1.0` exclusion is now inert on all ten conditions (no candidate below 1 cm
  anywhere); it is superseded anyway (T10).
- s20 (both priors) does not finish within 200 steps after the change either (the robot's item_7 is
  in flight at 199); unchanged from before.

## Contradictions with the task text

- Item 21 (T2 has no `design_decisions.md` entry): it has one — "Projection steps are execution
  ticks; the body supplies the rate, and the sampling resolution has no default in `shared/` (T2)",
  which already states both points. Not duplicated; the T9 entry cross-references it.
- The task cites the loop finding as "T1b Finding 1"; in T1b's report the loop is Finding 2
  (Finding 1 is the separation regimes). The docs cite the report's numbering.
- "Execution runs ahead of projection (placements finish 1 to 2 ticks early)": true only for the
  robot's full-task rows (+1.25 median), and as a net of two errors; after-grasp rows were within
  ±0.5 and the human was a tick behind. The decided change is right about the radius and was
  applied; what it uncovers is TODO-77.
