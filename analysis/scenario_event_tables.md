# Scenario event tables — what happens in each run at HEAD

Reference material. One table per (scenario, assignment_prior) condition, rows in tick order, only ticks
where something happens. No model or code change is described here; the code is the source of truth.

**Source.** Rerun at HEAD `4d9b948` with `PYTHONHASHSEED=0` on 2026-09-14 (the I5 matrix in
`analysis/i5_handback/` holds recognizer-only per-tick data, not meta-planner or executor events, so a rerun
was needed). Step counts as in the I5 sweep: s00 300, s20 200, s30 200, s40 400. No code changed between the
I5 commit `a6d7d7a` and HEAD (only docs, analysis data and layout JSON files), and the rerun's `[IR]` lines
match `analysis/i5_handback/trace.csv` on every tick of all eight conditions (`most_likely` and confidence
to the logged precision). Logs: `logs/run_20260914_1246{56,59}` (s00 off/on), `_1247{00,02}` (s20),
`_1248{30,32}` (s30), `_1247{04,06}` (s40).

**Reading the tables.**
- `tick` is the simulator step. `most_likely (conf)` is that tick's `[IR]` line. θ = 0.75.
- "grasps" / "places" is the tick whose step line shows `micro=grasp` / `micro=release`. The recognizer's
  completion pin (`[IR-complete]`) for the human's own placement is on the release tick; for the robot's
  placement it is one tick later. A robot task completes (`_on_task_complete`) one tick after its release,
  and the `no_current_task` trigger fires the tick after that.
- `projection` is the `[meta-proj]` result on a trigger tick: `built`, `none(below_theta)`, or
  `none(unresolved)` (confidence ≥ θ but `most_likely` is `unknown`, so no human plan can be projected).
- `winner` is the `[meta]` winner on a trigger tick; "same" means the executing task was re-selected (the
  plan is still reloaded and the robot loses that tick, TODO-43). Candidate costs are in ticks, `min_dist`
  in cm; a candidate is excluded when `min_dist < min_safe_distance = 1.0` (TODO-28, TODO-30).
- `d(item_N)` = `deliver_item(?item=item_N, ?kitting_table=kitting_table_0)`; `coffee` = `coffee_break`;
  `ac` = `ac_activation`; KT = kitting_table_0.
- Every run keeps stepping as a no-op after the last agent finishes (TODO-33); the "run ends" tick is the
  robot's `all tasks complete` tick.
- Prior-on, the recognizer's support is the human's assigned tasks, the foreseeable tasks and `unknown`;
  the robot's own items are never hypotheses, so its deliveries produce no pin in those conditions.

---

## scenario_00 — env_layout0 (`layout0_phase4_collision_baseline`)

- **Layout.** KT (0, 350); shelf_3 (−300, −300), shelf_4 (300, −300), shelf_6 (−400, −100), shelf_7
  (−400, 100), shelf_2 (400, −100). No coffee machine or AC switch: all hypotheses are deliveries.
- **Human** starts (350, 200): d(item_3) then d(item_2), both assigned. **Robot** starts (−350, 200), pool
  {item_4, item_6, item_7}; picks item_7 (cheapest, 31 ticks) at t=0, then item_6, then item_4.
- **Built to exercise.** Symmetric starts whose first approaches cross near the centre, then both agents
  converging on KT after picking. No foreseeable tasks. Prior-off live set: 5 deliveries + `unknown`;
  prior-on: item_3, item_2 + `unknown`.
- **How it ends.** Both conditions: all five items delivered. Prior-off the robot finishes at 172 after
  re-picking and re-placing the already-delivered item_4 (166–169); prior-on it finishes at 168. Human done
  at 142 in both.

### scenario_00, assignment_prior off

| tick | event | who | human task | most_likely (conf) | projection | winner | note |
|---|---|---|---|---|---|---|---|
| 0 | run start; trigger `no_current_task`; cands item_4 79 / item_6 47 / item_7 31 | robot | d(item_3): walk to shelf_3 | d(item_3) (0.200) | none(below_theta) | d(item_7) | 5-way uniform prior; `most_likely` is a key-order tie (TODO-42). |
| 6 | grasps item_7 at shelf_7 | robot | d(item_3): walk | d(item_3) (0.238) | — | — | |
| 7 | trigger `task_committed`; cands item_7 24 / item_4 80 / item_6 44 | robot | d(item_3): walk | d(item_3) (0.247) | none(below_theta) | same | Plan reloaded (TODO-43). |
| 30 | places item_7 at KT | robot | d(item_3): walk | d(item_3) (0.581) | — | — | |
| 31 | pin d(item_7) | recognizer | d(item_3): walk | d(item_3) (0.595) | — | — | Robot's own delivery: pin, no boundary. |
| 33 | trigger `no_current_task`; cands item_4 73 / item_6 61 | robot | d(item_3): walk | d(item_3) (0.626) | none(below_theta) | d(item_6) | |
| 39 | confidence crosses θ ↑; trigger `theta_crossed`; cands item_6 55 (min_dist 133) / item_4 72 (275) | recognizer, robot | d(item_3): walk, 2 ticks from shelf_3 | d(item_3) (0.967) | built | same | First reveal, pre-grasp: the arrival fold at 30 cm. |
| 41 | grasps item_3 at shelf_3 | human | d(item_3): grasp | d(item_3) (0.815) | — | — | Dip at the grasp (rivals' method flips, TODO-68 (a)); stays ≥ θ. |
| 43 | starts carry to KT | human | d(item_3): carry | d(item_3) (0.975) | — | — | |
| 62 | grasps item_6 at shelf_6 | robot | d(item_3): carry | d(item_3) (0.995) | — | — | |
| 63 | trigger `task_committed`; cands item_6 30 (282) / item_4 76 (327) | robot | d(item_3): carry | d(item_3) (0.995) | built | same | |
| 78 | places item_3 at KT; pin d(item_3); **episode boundary** (re-init over item_2, item_4, item_6 + `unknown`); `most_likely` → d(item_2); confidence crosses θ ↓ | human, recognizer | d(item_3): place → done | d(item_2) (0.249) | — | — | Post-boundary `most_likely` is a key-order tie; no information until the human moves. |
| 81 | starts d(item_2): walk to shelf_2 | human | d(item_2): walk | d(item_2) (0.333) | — | — | Idle 79–80. |
| 92 | places item_6 at KT | robot | d(item_2): walk | d(item_2) (0.490) | — | — | |
| 93 | pin d(item_6) | recognizer | d(item_2): walk | d(item_2) (0.496) | — | — | Live set shrinks to item_2, item_4 + `unknown`; no boundary. |
| 95 | trigger `no_current_task`; cand item_4 73 | robot | d(item_2): walk | d(item_2) (0.502) | none(below_theta) | d(item_4) | Last pool item. |
| 109 | confidence crosses θ ↑; trigger `theta_crossed`; cand item_4 59 (142) | recognizer, robot | d(item_2): walk, 2 ticks from shelf_2 | d(item_2) (0.939) | built | same | Next-task reveal, pre-grasp. |
| 111 | grasps item_2; confidence crosses θ ↓ | human, recognizer | d(item_2): grasp | d(item_2) (0.652) | — | — | item_4 lifts to 0.338 (its `deliver_with_return` place phase, TODO-68 (a)). No trigger fires on a downward crossing. |
| 113 | starts carry; confidence crosses θ ↑; trigger `theta_crossed`; cand item_4 55 (143) | human, recognizer, robot | d(item_2): carry | d(item_2) (0.947) | built | same | Second crossing of the same recognition (TODO-68). Plan reloaded (TODO-43). |
| 114 | confidence crosses θ ↓ | recognizer | d(item_2): carry | d(item_2) (0.703) | — | — | Rival regresses to a fresh zero-excess stretch (TODO-61 (a)). |
| 115 | confidence crosses θ ↑; trigger `theta_crossed`; cand item_4 53 (143) | recognizer, robot | d(item_2): carry | d(item_2) (0.754) | built | same | Third crossing (TODO-68). Plan reloaded again (TODO-43). |
| 130 | grasps item_4 at shelf_4 | robot | d(item_2): carry | d(item_2) (0.995) | — | — | |
| 131 | trigger `task_committed`; cand item_4 35 (461) | robot | d(item_2): carry | d(item_2) (0.995) | built | same | |
| 142 | places item_2 at KT; pin d(item_2); **episode boundary** (item_4 + `unknown`); `most_likely` → d(item_4); confidence crosses θ ↓ | human, recognizer | d(item_2): place → done | d(item_4) (0.498) | — | — | Human's script ends; idle from 144. Idle human sits at the prior over the robot's undelivered item. |
| 165 | places item_4 at KT | robot | idle | d(item_4) (0.498) | — | — | Last delivery. |
| 166 | pin d(item_4); `most_likely` → `unknown`; confidence crosses θ ↑; trigger `theta_crossed`; cand item_4 3 | recognizer, robot | idle | unknown (0.995) | none(unresolved) | d(item_4) | `theta_crossed` on `unknown` after a pin (TODO-54); the already-delivered item_4 is still in the pool and is re-selected (TODO-67 class); a fresh 4-action plan is loaded. |
| 167 | grasps item_4 again, at KT | robot | idle | unknown (0.995) | — | — | Run-visible consequence of 166: a delivered item is lifted off the table. |
| 168 | trigger `task_committed`; cand item_4 2 | robot | idle | unknown (0.995) | none(unresolved) | same | |
| 169 | places item_4 at KT again | robot | idle | unknown (0.995) | — | — | Three robot ticks spent re-delivering item_4. |
| 172 | trigger `no_current_task` → all tasks complete | robot | idle | unknown (0.995) | none(unresolved) | — | Run ends (steps continue as no-ops to 300, TODO-33). |

### scenario_00, assignment_prior on

| tick | event | who | human task | most_likely (conf) | projection | winner | note |
|---|---|---|---|---|---|---|---|
| 0 | run start; trigger `no_current_task`; cands item_4 79 / item_6 47 / item_7 31 | robot | d(item_3): walk to shelf_3 | d(item_3) (0.488) | none(below_theta) | d(item_7) | Support restricted to item_3, item_2 + `unknown` (item_2 0.461). |
| 6 | grasps item_7 at shelf_7 | robot | d(item_3): walk | d(item_3) (0.615) | — | — | |
| 7 | trigger `task_committed`; cands item_7 24 / item_4 80 / item_6 44 | robot | d(item_3): walk | d(item_3) (0.645) | none(below_theta) | same | Plan reloaded (TODO-43). |
| 11 | confidence crosses θ ↑; trigger `theta_crossed`; cands item_7 20 (356) / item_4 84 (145) / item_6 48 (238) | recognizer, robot | d(item_3): walk | d(item_3) (0.768) | built | same | First reveal, 30 ticks pre-grasp, mid-approach. |
| 30 | places item_7 at KT | robot | d(item_3): walk | d(item_3) (0.905) | — | — | No pin: item_7 is not a hypothesis prior-on. |
| 33 | trigger `no_current_task`; cands item_4 73 (360) / item_6 61 (133) | robot | d(item_3): walk | d(item_3) (0.905) | built | d(item_6) | |
| 41 | grasps item_3 at shelf_3 | human | d(item_3): grasp | d(item_3) (0.986) | — | — | No dip: no live rival to flip. |
| 43 | starts carry to KT | human | d(item_3): carry | d(item_3) (0.995) | — | — | |
| 62 | grasps item_6 at shelf_6 | robot | d(item_3): carry | d(item_3) (0.995) | — | — | |
| 63 | trigger `task_committed`; cands item_6 30 (282) / item_4 76 (327) | robot | d(item_3): carry | d(item_3) (0.995) | built | same | |
| 78 | places item_3 at KT; pin d(item_3); **episode boundary** (item_2 + `unknown`); `most_likely` → d(item_2); confidence crosses θ ↓ | human, recognizer | d(item_3): place → done | d(item_2) (0.498) | — | — | |
| 81 | starts d(item_2); confidence crosses θ ↑; trigger `theta_crossed`; cands item_6 12 (155) / item_4 94 (203) | human, recognizer, robot | d(item_2): walk to shelf_2 | d(item_2) (0.905) | built | same | Next-task reveal on the human's first step (one observation against `unknown` alone: 1/(1+u)). |
| 92 | places item_6 at KT | robot | d(item_2): walk | d(item_2) (0.905) | — | — | No pin prior-on. |
| 95 | trigger `no_current_task`; cand item_4 73 (142) | robot | d(item_2): walk | d(item_2) (0.905) | built | d(item_4) | |
| 111 | grasps item_2 at shelf_2 | human | d(item_2): grasp | d(item_2) (0.986) | — | — | No dip. |
| 113 | starts carry | human | d(item_2): carry | d(item_2) (0.995) | — | — | |
| 130 | grasps item_4 at shelf_4 | robot | d(item_2): carry | d(item_2) (0.995) | — | — | |
| 131 | trigger `task_committed`; cand item_4 35 (461) | robot | d(item_2): carry | d(item_2) (0.995) | built | same | |
| 142 | places item_2 at KT; pin d(item_2); **episode boundary** (`unknown` only); `most_likely` → `unknown` | human, recognizer | d(item_2): place → done | unknown (0.995) | — | — | Confidence stays ≥ θ (0.995 → 0.995): no crossing, no trigger. Human done; idle from 144. |
| 165 | places item_4 at KT | robot | idle | unknown (0.995) | — | — | No pin, no trigger: `unknown` was already above θ, so the prior-off re-pick at 166 does not occur here. |
| 168 | trigger `no_current_task` → all tasks complete | robot | idle | unknown (0.995) | none(unresolved) | — | Run ends (no-ops to 300, TODO-33). |

---

## scenario_20 — env_layout2 (`layout2_midapproach_sustained_conflict`)

- **Layout.** KT (0, 400); shelf_4 (−300, −100), shelf_3 (−180, −190), shelf_6 (−500, −250), shelf_7
  (450, −350), shelf_2 (400, −100). Deliveries only.
- **Human** starts (200, 50): d(item_3) then d(item_2), both assigned. **Robot** starts (−500, 300), pool
  {item_4, item_6, item_7}; item_4 is cheapest (54 ticks) and is the t=0 pick by construction.
- **Built to exercise.** B2/B3: the robot's cheapest task (item_4) has an arrival at KT within a tick of the
  human's, so both placements overlap at the table and item_4 is excluded by `min_safe_distance` once a
  projection exists; item_6 is the clean alternative; item_7 never competes. Prior-off live set: 5
  deliveries + `unknown`; prior-on: item_3, item_2 + `unknown`.
- **How it ends.** Both conditions run out of steps at 200 with the robot carrying item_7 toward KT
  (grasped at 189 prior-off, 175 prior-on). Human done at 122 in both. Delivered: item_4 and item_6
  (prior-off 59, 143; prior-on item_6 69, item_4 129), item_3 and item_2 by the human.

### scenario_20, assignment_prior off

| tick | event | who | human task | most_likely (conf) | projection | winner | note |
|---|---|---|---|---|---|---|---|
| 0 | run start; trigger `no_current_task`; cands item_4 54 / item_6 71 / item_7 103 | robot | d(item_3): walk to shelf_3 | d(item_3) (0.206) | none(below_theta) | d(item_4) | item_3 / item_6 / item_4 within 0.001 at t=0: key-order tie (TODO-42). |
| 20 | confidence crosses θ ↑; trigger `theta_crossed`; cands **item_4 34 excluded (min_dist 0.0)** / item_6 56 (196) / item_7 87 (35) | recognizer, robot | d(item_3): walk, 2 ticks from shelf_3 | d(item_3) (0.850) | built | **d(item_6)** | First reveal pre-grasp (arrival fold). Exclusion branch exercised (TODO-30); whether a 0.0 placement overlap at a point-modelled table is a legitimate exclusion is TODO-28. **Task switched**: robot abandons item_4 at tick 20 of its 22-tick approach to shelf_4. |
| 22 | grasps item_3; confidence crosses θ ↓ | human, recognizer | d(item_3): grasp | d(item_3) (0.375) | — | — | item_6 0.353, item_4 0.264: rivals' `deliver_with_return` flip (TODO-68 (a)). |
| 24 | starts carry; confidence crosses θ ↑; trigger `theta_crossed`; cands item_6 52 (229) / item_4 35 (86) / item_7 89 (177) | human, recognizer, robot | d(item_3): carry | d(item_3) (0.856) | built | **d(item_4)** | Second crossing (TODO-68). item_4 no longer excluded (the projected arrival gap moved), so the argmin **switches back** to item_4: two switches in four ticks. |
| 25 | confidence crosses θ ↓ | recognizer | d(item_3): carry | d(item_3) (0.427) | — | — | Rival regress (TODO-61 (a)). |
| 28 | grasps item_4 at shelf_4 | robot | d(item_3): carry | d(item_3) (0.636) | — | — | |
| 29 | trigger `task_committed`; cands item_4 31 / item_6 57 / item_7 87 | robot | d(item_3): carry | d(item_3) (0.710) | none(below_theta) | same | Below θ on this tick, so no interference check. |
| 30 | confidence crosses θ ↑; trigger `theta_crossed`; cands item_4 30 (100) / item_6 57 (194) / item_7 87 (194) | recognizer, robot | d(item_3): carry | d(item_3) (0.777) | built | same | Third crossing (TODO-68). Plan reloaded (TODO-43). Re-decisions at 20/24/29/30 move the robot's item_4 delivery from 52 to 59 (TODO-68 (c)). |
| 54 | places item_3 at KT; pin d(item_3); **episode boundary** (item_2, item_4, item_6, item_7 + `unknown`); `most_likely` → d(item_2); confidence crosses θ ↓ | human, recognizer | d(item_3): place → done | d(item_2) (0.200) | — | — | Key-order tie after re-init. |
| 57 | starts d(item_2): walk to shelf_2 | human | d(item_2): walk | d(item_2) (0.257) | — | — | Idle 55–56. item_7 also 0.257: same bearing from KT. |
| 59 | places item_4 at KT | robot | d(item_2): walk | d(item_2) (0.301) | — | — | |
| 60 | pin d(item_4) | recognizer | d(item_2): walk | d(item_2) (0.360) | — | — | |
| 62 | trigger `no_current_task`; cands item_6 83 / item_7 89 | robot | d(item_2): walk | d(item_2) (0.381) | none(below_theta) | d(item_6) | |
| 87 | confidence crosses θ ↑; trigger `theta_crossed`; cands item_6 58 (453) / item_7 88 (357) | recognizer, robot | d(item_2): walk, 2 ticks from shelf_2 | d(item_2) (0.907) | built | same | Next-task reveal, pre-grasp. |
| 89 | grasps item_2; confidence crosses θ ↓ | human, recognizer | d(item_2): grasp | d(item_2) (0.523) | — | — | item_7 lifts to 0.469 (TODO-68 (a)). |
| 91 | starts carry; confidence crosses θ ↑; trigger `theta_crossed`; cands item_6 54 (436) / item_7 89 (424) | human, recognizer, robot | d(item_2): carry | d(item_2) (0.914) | built | same | Second crossing (TODO-68); reload (TODO-43). |
| 92 | confidence crosses θ ↓ | recognizer | d(item_2): carry | d(item_2) (0.579) | — | — | |
| 95 | confidence crosses θ ↑; trigger `theta_crossed`; cands item_6 50 (436) / item_7 90 (503) | recognizer, robot | d(item_2): carry | d(item_2) (0.766) | built | same | Third crossing (TODO-68); reload (TODO-43). |
| 102 | grasps item_6 at shelf_6 | robot | d(item_2): carry | d(item_2) (0.975) | — | — | |
| 103 | trigger `task_committed`; cands item_6 41 (406) / item_7 96 (685) | robot | d(item_2): carry | d(item_2) (0.982) | built | same | |
| 122 | places item_2 at KT; pin d(item_2); **episode boundary** (item_6, item_7 + `unknown`); `most_likely` → d(item_6); confidence crosses θ ↓ | human, recognizer | d(item_2): place → done | d(item_6) (0.332) | — | — | Human's script ends; idle from 124. |
| 143 | places item_6 at KT | robot | idle | d(item_6) (0.332) | — | — | Re-decisions at 87–103 moved this from 136 to 143 (TODO-68 (c)). |
| 144 | pin d(item_6); `most_likely` → d(item_7) | recognizer | idle | d(item_7) (0.498) | — | — | Tie with `unknown` at 0.498; below θ, so unlike s00_off 166 no trigger fires. |
| 146 | trigger `no_current_task`; cand item_7 89 | robot | idle | d(item_7) (0.498) | none(below_theta) | d(item_7) | |
| 189 | grasps item_7 at shelf_7 | robot | idle | d(item_7) (0.498) | — | — | |
| 190 | trigger `task_committed`; cand item_7 43 | robot | idle | d(item_7) (0.498) | none(below_theta) | same | |
| 199 | run out of steps | — | idle | d(item_7) (0.498) | — | — | Robot still carrying item_7, about 34 ticks from KT: item_7 undelivered. |

### scenario_20, assignment_prior on

| tick | event | who | human task | most_likely (conf) | projection | winner | note |
|---|---|---|---|---|---|---|---|
| 0 | run start; trigger `no_current_task`; cands item_4 54 / item_6 71 / item_7 103 | robot | d(item_3): walk to shelf_3 | d(item_3) (0.508) | none(below_theta) | d(item_4) | Support item_3, item_2 + `unknown`. |
| 6 | confidence crosses θ ↑; trigger `theta_crossed`; cands **item_4 48 excluded (0.0)** / item_6 65 (311) / item_7 98 (90) | recognizer, robot | d(item_3): walk | d(item_3) (0.764) | built | **d(item_6)** | Mid-approach reveal, 16 ticks pre-grasp. Exclusion (TODO-30 / TODO-28). **Task switched** at tick 6 of the 22-tick approach to shelf_4; the fixture's mid-approach condition. |
| 22 | grasps item_3 at shelf_3 | human | d(item_3): grasp | d(item_3) (0.986) | — | — | No dip prior-on. |
| 24 | starts carry | human | d(item_3): carry | d(item_3) (0.995) | — | — | |
| 28 | grasps item_6 at shelf_6 | robot | d(item_3): carry | d(item_3) (0.995) | — | — | |
| 29 | trigger `task_committed`; cands item_6 41 (303) / item_4 46 (404) / item_7 96 (408) | robot | d(item_3): carry | d(item_3) (0.995) | built | same | |
| 54 | places item_3 at KT; pin d(item_3); **episode boundary** (item_2 + `unknown`); `most_likely` → d(item_2); confidence crosses θ ↓ | human, recognizer | d(item_3): place → done | d(item_2) (0.498) | — | — | |
| 57 | starts d(item_2); confidence crosses θ ↑; trigger `theta_crossed`; cands item_6 13 (159) / item_4 74 (163) / item_7 124 (222) | human, recognizer, robot | d(item_2): walk to shelf_2 | d(item_2) (0.905) | built | same | Reveal on the first step. Reload (TODO-43). |
| 69 | places item_6 at KT | robot | d(item_2): walk | d(item_2) (0.905) | — | — | No pin prior-on. |
| 72 | trigger `no_current_task`; cands item_4 59 (177) / item_7 89 (73) | robot | d(item_2): walk | d(item_2) (0.905) | built | d(item_4) | item_4 now clear of the human: feasible. |
| 89 | grasps item_2 at shelf_2 | human | d(item_2): grasp | d(item_2) (0.986) | — | — | |
| 91 | starts carry | human | d(item_2): carry | d(item_2) (0.995) | — | — | |
| 100 | grasps item_4 at shelf_4 | robot | d(item_2): carry | d(item_2) (0.995) | — | — | |
| 101 | trigger `task_committed`; cands item_4 29 (129) / item_7 88 (479) | robot | d(item_2): carry | d(item_2) (0.995) | built | same | |
| 122 | places item_2 at KT; pin d(item_2); **episode boundary** (`unknown` only); `most_likely` → `unknown` | human, recognizer | d(item_2): place → done | unknown (0.995) | — | — | No crossing (stays ≥ θ). Human done; idle from 124. |
| 129 | places item_4 at KT | robot | idle | unknown (0.995) | — | — | No pin. |
| 132 | trigger `no_current_task`; cand item_7 89 | robot | idle | unknown (0.995) | none(unresolved) | d(item_7) | Confidence ≥ θ but `most_likely` is `unknown`: nothing to project. |
| 175 | grasps item_7 at shelf_7 | robot | idle | unknown (0.995) | — | — | |
| 176 | trigger `task_committed`; cand item_7 43 | robot | idle | unknown (0.995) | none(unresolved) | same | |
| 199 | run out of steps | — | idle | unknown (0.995) | — | — | Robot carrying item_7, about 20 ticks from KT: item_7 undelivered. |

---

## scenario_30 — env_layout3 (`layout3_midpath_crossing`)

- **Layout.** KT (0, 350); shelf_3 (−200, −300), shelf_4 (200, −300), shelf_6 (400, −100), shelf_7
  (−400, 200), shelf_2 (400, −300). Deliveries only.
- **Human** starts (300, 300): d(item_3) then d(item_7), both assigned. **Robot** starts (−300, 300), pool
  {item_2, item_4}; item_4 is cheapest (75 ticks) and is the t=0 pick.
- **Built to exercise.** A mid-path crossing on the robot's current task: the two first approaches are
  mirror images across x = 0 and pass through each other at the centre line at step 22 (11 cm apart) while
  both agents are in `move_to`. The human hypothesis is correct throughout. Prior-off live set: 5 deliveries
  + `unknown` (item_6 is never delivered by anyone); prior-on: item_3, item_7 + `unknown`.
- **How it ends.** Both conditions: all four items delivered; robot finishes at 163 (prior-off, after
  re-picking the already-delivered item_2 at 87–90, TODO-67) / 159 (prior-on). Human done at 121 in both.

### scenario_30, assignment_prior off

| tick | event | who | human task | most_likely (conf) | projection | winner | note |
|---|---|---|---|---|---|---|---|
| 0 | run start; trigger `no_current_task`; cands item_2 86 / item_4 75 | robot | d(item_3): walk to shelf_3 | d(item_3) (0.201) | none(below_theta) | d(item_4) | Key-order tie at the uniform prior (TODO-42). |
| 28 | confidence crosses θ ↑; trigger `theta_crossed`; cands **item_4 47 excluded (0.0)** / item_2 59 (131) | recognizer, robot | d(item_3): walk | d(item_3) (0.775) | built | **d(item_2)** | First reveal, 11 ticks pre-grasp. The designed crossing at 22 was below θ and is never seen by the meta-planner. **Task switched**: the robot leaves the shelf_4 approach for shelf_2 (200 cm east). Exclusion is the placement overlap at KT (TODO-28 / TODO-30), not the crossing. |
| 39 | grasps item_3 at shelf_3 | human | d(item_3): grasp | d(item_3) (0.973) | — | — | Small dip, no crossing. |
| 41 | starts carry to KT | human | d(item_3): carry | d(item_3) (0.995) | — | — | |
| 47 | grasps item_2 at shelf_2 | robot | d(item_3): carry | d(item_3) (0.994) | — | — | |
| 48 | trigger `task_committed`; cands item_2 38 (224) / item_4 48 (421) | robot | d(item_3): carry | d(item_3) (0.995) | built | same | |
| 74 | places item_3 at KT; pin d(item_3); **episode boundary** (item_2, item_4, item_6, item_7 + `unknown`); `most_likely` → d(item_2); confidence crosses θ ↓ | human, recognizer | d(item_3): place → done | d(item_2) (0.200) | — | — | |
| 77 | starts d(item_7): walk to shelf_7; `most_likely` → d(item_7) | human, recognizer | d(item_7): walk | d(item_7) (0.269) | — | — | Idle 75–76. |
| 85 | places item_2 at KT | robot | d(item_7): walk | d(item_7) (0.664) | — | — | |
| 86 | pin d(item_2) | recognizer | d(item_7): walk | d(item_7) (0.728) | — | — | Robot's delivery: pin, no boundary. |
| 87 | confidence crosses θ ↑; trigger `theta_crossed`; cands item_2 3 (237) / item_4 69 (237) | recognizer, robot | d(item_7): walk | d(item_7) (0.763) | built | **d(item_2)** | Next-task reveal, 11 ticks pre-grasp. The **already-delivered item_2** is still in the pool and wins on cost (TODO-67); a 4-action plan is loaded. |
| 88 | grasps item_2 again, at KT | robot | d(item_7): walk | d(item_7) (0.793) | — | — | Run-visible consequence of 87. |
| 89 | trigger `task_committed`; cands item_2 2 (277) / item_4 84 (277) | robot | d(item_7): walk | d(item_7) (0.818) | built | same | |
| 90 | places item_2 at KT again | robot | d(item_7): walk | d(item_7) (0.838) | — | — | |
| 93 | trigger `no_current_task`; cand item_4 69 (357) | robot | d(item_7): walk | d(item_7) (0.877) | built | d(item_4) | The robot's item_4 delivery starts 6 ticks later than in the prior-on run (89). |
| 98 | grasps item_7 at shelf_7 | human | d(item_7): grasp | d(item_7) (0.974) | — | — | |
| 100 | starts carry | human | d(item_7): carry | d(item_7) (0.995) | — | — | |
| 121 | places item_7 at KT; pin d(item_7); **episode boundary** (item_4, item_6 + `unknown`); `most_likely` → d(item_4); confidence crosses θ ↓ | human, recognizer | d(item_7): place → done | d(item_4) (0.332) | — | — | Human done; idle from 123. |
| 126 | grasps item_4 at shelf_4 | robot | idle | d(item_4) (0.332) | — | — | |
| 127 | trigger `task_committed`; cand item_4 34 | robot | idle | d(item_4) (0.332) | none(below_theta) | same | |
| 160 | places item_4 at KT | robot | idle | d(item_4) (0.332) | — | — | |
| 161 | pin d(item_4); `most_likely` → d(item_6) | recognizer | idle | d(item_6) (0.498) | — | — | Tie with `unknown`; below θ, no trigger. |
| 163 | trigger `no_current_task` → all tasks complete | robot | idle | d(item_6) (0.498) | none(below_theta) | — | Run ends (no-ops to 200, TODO-33). |

### scenario_30, assignment_prior on

| tick | event | who | human task | most_likely (conf) | projection | winner | note |
|---|---|---|---|---|---|---|---|
| 0 | run start; trigger `no_current_task`; cands item_2 86 / item_4 75 | robot | d(item_3): walk to shelf_3 | d(item_3) (0.481) | none(below_theta) | d(item_4) | Support item_3, item_7 + `unknown`. |
| 21 | confidence crosses θ ↑; trigger `theta_crossed`; cands **item_4 54 excluded (0.0)** / item_2 66 (22.7) | recognizer, robot | d(item_3): walk | d(item_3) (0.761) | built | **d(item_2)** | Reveal one tick before the designed crossing at 22. **Task switched** to item_2. item_2's own min_dist is 22.7 cm: clears `min_safe_distance = 1.0` (TODO-28). |
| 39 | grasps item_3 at shelf_3 | human | d(item_3): grasp | d(item_3) (0.981) | — | — | |
| 41 | starts carry | human | d(item_3): carry | d(item_3) (0.995) | — | — | |
| 47 | grasps item_2 at shelf_2 | robot | d(item_3): carry | d(item_3) (0.995) | — | — | |
| 48 | trigger `task_committed`; cands item_2 39 (231) / item_4 48 (412) | robot | d(item_3): carry | d(item_3) (0.995) | built | same | |
| 74 | places item_3 at KT; pin d(item_3); **episode boundary** (item_7 + `unknown`); `most_likely` → d(item_7); confidence crosses θ ↓ | human, recognizer | d(item_3): place → done | d(item_7) (0.498) | — | — | |
| 77 | starts d(item_7); confidence crosses θ ↑; trigger `theta_crossed`; cands item_2 10 (149) / item_4 77 (166) | human, recognizer, robot | d(item_7): walk to shelf_7 | d(item_7) (0.905) | built | same | Reveal on the first step. Reload (TODO-43). |
| 86 | places item_2 at KT | robot | d(item_7): walk | d(item_7) (0.905) | — | — | No pin prior-on; no trigger at 87, so no re-pick (contrast prior-off). |
| 89 | trigger `no_current_task`; cand item_4 69 (274) | robot | d(item_7): walk | d(item_7) (0.905) | built | d(item_4) | |
| 98 | grasps item_7 at shelf_7 | human | d(item_7): grasp | d(item_7) (0.986) | — | — | |
| 100 | starts carry | human | d(item_7): carry | d(item_7) (0.995) | — | — | |
| 121 | places item_7 at KT; pin d(item_7); **episode boundary** (`unknown` only); `most_likely` → `unknown` | human, recognizer | d(item_7): place → done | unknown (0.995) | — | — | No crossing. Human done. Robot arrives at shelf_4 the same tick. |
| 122 | grasps item_4 at shelf_4 | robot | idle | unknown (0.995) | — | — | |
| 123 | trigger `task_committed`; cand item_4 34 | robot | idle | unknown (0.995) | none(unresolved) | same | |
| 156 | places item_4 at KT | robot | idle | unknown (0.995) | — | — | |
| 159 | trigger `no_current_task` → all tasks complete | robot | idle | unknown (0.995) | none(unresolved) | — | Run ends (no-ops to 200, TODO-33). |

---

## scenario_40 — env_layout4 (`layout4_foreseeable_and_unmodelled`)

- **Layout.** KT (0, 500); shelf_3 (−950, −50), shelf_6 (950, −150), shelf_4 (850, 150), shelf_7
  (950, 450), shelf_5 (950, −400); coffee_machine_0 (−40, −250); ac_switch_0 (400, 550), never visited;
  waypoints wander_0 (356, −210) and wander_1 (230, −550).
- **Human** starts (100, 550). Script in four segments: (1) d(item_3); (2) `coffee_break` at
  coffee_machine_0 (scheduled, not assigned: a foreseeable task); (3) two walks scripted as `ac_activation`
  bound to wander_0 then wander_1 (`move_to` + a one-tick `wait_at`; not tasks the recognizer enumerates);
  (4) d(item_6). Assigned: item_3, item_6. **Robot** starts (−950, −550), pool {item_4, item_7, item_5},
  taken in that order.
- **Built to exercise.** A positive control (segment 1: every other target ≥ 50° off the heading), a
  foreseeable deviation with no grasp (coffee), an unmodelled wander whose first leg points at shelf_6 and
  whose second leg turns away (the retraction case), and a final delivery approached from the wander with
  shelf_5 (the robot's undelivered item) as a prior-off decoy. Prior-off live set: 5 deliveries + coffee +
  ac + `unknown`; prior-on: item_3, item_6, coffee, ac + `unknown`.
- **How it ends.** Both conditions: all three robot items and both human items delivered, coffee completed;
  robot finishes at 378, human script ends at 331 (idle to 400).

### scenario_40, assignment_prior off

| tick | event | who | human task | most_likely (conf) | projection | winner | note |
|---|---|---|---|---|---|---|---|
| 0 | run start; trigger `no_current_task`; cands item_4 145 / item_7 157 / item_5 163 | robot | d(item_3): walk to shelf_3 | d(item_3) (0.159) | none(below_theta) | d(item_4) | 7 hypotheses + `unknown`. |
| 19 | confidence crosses θ ↑; trigger `theta_crossed`; cands item_4 126 (539) / item_7 138 (494) / item_5 145 (647) | recognizer, robot | d(item_3): walk | d(item_3) (0.762) | built | same | Positive control: reveal at 19 of a 60-tick approach. Reload (TODO-43). |
| 60 | grasps item_3 at shelf_3 | human | d(item_3): grasp | d(item_3) (0.984) | — | — | |
| 62 | starts carry to KT | human | d(item_3): carry | d(item_3) (0.993) | — | — | |
| 97 | grasps item_4 at shelf_4 | robot | d(item_3): carry | d(item_3) (0.993) | — | — | |
| 98 | trigger `task_committed`; cands item_4 47 (563) / item_7 67 (946) / item_5 97 (1089) | robot | d(item_3): carry | d(item_3) (0.993) | built | same | |
| 115 | places item_3 at KT; pin d(item_3); **episode boundary** (item_4, item_5, item_6, item_7, coffee, ac + `unknown`); `most_likely` → ac; confidence crosses θ ↓ | human, recognizer | d(item_3): place → done | ac (0.143) | — | — | Key-order tie after re-init. |
| 118 | starts coffee_break: walk to coffee_machine_0; `most_likely` → coffee | human, recognizer | coffee: walk | coffee (0.174) | — | — | Idle 116–117. |
| 143 | confidence crosses θ ↑; trigger `theta_crossed`; cands item_4 2 (532) / item_7 112 (532) / item_5 142 (532) | recognizer, robot | coffee: walk | coffee (0.762) | built | same | Foreseeable task recognised mid-walk, 11 ticks before the machine. Fires as the robot reaches KT; reload (TODO-43). |
| 144 | places item_4 at KT | robot | coffee: walk | coffee (0.779) | — | — | |
| 145 | pin d(item_4) | recognizer | coffee: walk | coffee (0.794) | — | — | |
| 147 | trigger `no_current_task`; cands item_7 97 (612) / item_5 132 (612) | robot | coffee: walk | coffee (0.820) | built | d(item_7) | |
| 155 | waits at coffee_machine_0 (stand, 155–184) | human | coffee: wait | coffee (0.982) | — | — | |
| 184 | coffee_break completes (waited); pin coffee; **episode boundary** (item_5, item_6, item_7, ac + `unknown`); `most_likely` → ac; confidence crosses θ ↓ | human, recognizer | coffee: done | ac (0.199) | — | — | |
| 187 | starts wander leg 1: walk to wander_0; `most_likely` → d(item_6) | human, recognizer | ac_activation@wander_0: walk | d(item_6) (0.247) | — | — | The leg lies on the bearing to shelf_6. |
| 194 | grasps item_7 at shelf_7 | robot | wander_0: walk | d(item_6) (0.281) | — | — | |
| 195 | trigger `task_committed`; cands item_7 48 / item_5 112 | robot | wander_0: walk | d(item_6) (0.287) | none(below_theta) | same | |
| 207 | waits at wander_0 (one tick) | human | wander_0: wait | d(item_6) (0.382) | — | — | Leg 1 ends at 209; no pin, no boundary: not a task the recognizer enumerates (TODO-57, question 3). item_6 peaks at 0.397 (210) prior-off: diluted by 7 rivals. |
| 210 | starts wander leg 2: walk to wander_1 | human | ac_activation@wander_1: walk | d(item_6) (0.397) | — | — | The turn away from shelf_6. |
| 211 | `most_likely` → d(item_5) | recognizer | wander_1: walk | d(item_5) (0.401) | — | — | shelf_5 is the nearest bearing to the new heading; stays below θ. |
| 221 | `most_likely` → `unknown` | recognizer | wander_1: walk | unknown (0.407) | — | — | |
| 226 | confidence crosses θ ↑ on `unknown`; trigger `theta_crossed`; cands item_7 17 / item_5 143 | recognizer, robot | wander_1: walk | unknown (0.751) | none(unresolved) | same | `theta_crossed` on `unknown` (TODO-54). Reload (TODO-43). |
| 228 | waits at wander_1 (one tick) | human | wander_1: wait | unknown (0.751) | — | — | Leg 2 ends at 230; no boundary. |
| 231 | starts d(item_6): walk from wander_1 to shelf_6 | human | d(item_6): walk | unknown (0.752) | — | — | |
| 242 | places item_7 at KT | robot | d(item_6): walk | unknown (0.772) | — | — | |
| 243 | pin d(item_7) | recognizer | d(item_6): walk | unknown (0.774) | — | — | |
| 245 | trigger `no_current_task`; cand item_5 132 | robot | d(item_6): walk | unknown (0.780) | none(unresolved) | d(item_5) | |
| 270 | confidence crosses θ ↓ | recognizer | d(item_6): walk, 1 tick from shelf_6 | unknown (0.518) | — | — | item_6's arrival fold lifts it (0.451 at 272) but not yet above `unknown`. |
| 272 | grasps item_6 at shelf_6 | human | d(item_6): grasp | unknown (0.495) | — | — | Not recognised at the grasp: item_6 carries its segment-3 excess into its own approach (TODO-57 question 3, TODO-61 (b)). |
| 274 | starts carry; `most_likely` → d(item_6); confidence crosses θ ↑; trigger `theta_crossed`; cand item_5 103 (125) | human, recognizer, robot | d(item_6): carry | d(item_6) (0.888) | built | same | Post-grasp reveal (2 ticks after). |
| 310 | grasps item_5 at shelf_5 | robot | d(item_6): carry | d(item_6) (0.896) | — | — | |
| 311 | trigger `task_committed`; cand item_5 65 (882) | robot | d(item_6): carry | d(item_6) (0.896) | built | same | |
| 331 | places item_6 at KT; pin d(item_6); **episode boundary** (item_5, ac + `unknown`); `most_likely` → ac; confidence crosses θ ↓ | human, recognizer | d(item_6): place → done | ac (0.332) | — | — | Human's script ends; idle from 333. |
| 375 | places item_5 at KT | robot | idle | ac (0.332) | — | — | |
| 376 | pin d(item_5) | recognizer | idle | ac (0.497) | — | — | ac / `unknown` tie at 0.497; below θ, no trigger. |
| 378 | trigger `no_current_task` → all tasks complete | robot | idle | ac (0.497) | none(below_theta) | — | Run ends (no-ops to 400, TODO-33). |

### scenario_40, assignment_prior on

| tick | event | who | human task | most_likely (conf) | projection | winner | note |
|---|---|---|---|---|---|---|---|
| 0 | run start; trigger `no_current_task`; cands item_4 145 / item_7 157 / item_5 163 | robot | d(item_3): walk to shelf_3 | d(item_3) (0.266) | none(below_theta) | d(item_4) | Support item_3, item_6, coffee, ac + `unknown`. |
| 19 | confidence crosses θ ↑; trigger `theta_crossed`; cands item_4 126 (539) / item_7 138 (494) / item_5 145 (647) | recognizer, robot | d(item_3): walk | d(item_3) (0.768) | built | same | 0.7495 at 18 (just under θ). Reload (TODO-43). |
| 60 | grasps item_3 at shelf_3 | human | d(item_3): grasp | d(item_3) (0.984) | — | — | |
| 62 | starts carry to KT | human | d(item_3): carry | d(item_3) (0.993) | — | — | |
| 97 | grasps item_4 at shelf_4 | robot | d(item_3): carry | d(item_3) (0.993) | — | — | |
| 98 | trigger `task_committed`; cands item_4 47 (563) / item_7 67 (946) / item_5 97 (1089) | robot | d(item_3): carry | d(item_3) (0.993) | built | same | |
| 115 | places item_3 at KT; pin d(item_3); **episode boundary** (item_6, coffee, ac + `unknown`); `most_likely` → ac; confidence crosses θ ↓ | human, recognizer | d(item_3): place → done | ac (0.249) | — | — | |
| 118 | starts coffee_break; `most_likely` → coffee | human, recognizer | coffee: walk | coffee (0.340) | — | — | |
| 135 | confidence crosses θ ↑; trigger `theta_crossed`; cands item_4 10 (361) / item_7 104 (361) / item_5 134 (361) | recognizer, robot | coffee: walk | coffee (0.757) | built | same | Coffee recognised 19 ticks before the machine (8 earlier than prior-off: 3 live rivals instead of 7). Reload (TODO-43). |
| 144 | places item_4 at KT | robot | coffee: walk | coffee (0.865) | — | — | No pin prior-on. |
| 147 | trigger `no_current_task`; cands item_7 97 (612) / item_5 132 (612) | robot | coffee: walk | coffee (0.882) | built | d(item_7) | |
| 155 | waits at coffee_machine_0 (155–184) | human | coffee: wait | coffee (0.984) | — | — | |
| 184 | coffee_break completes; pin coffee; **episode boundary** (item_6, ac + `unknown`); `most_likely` → ac; confidence crosses θ ↓ | human, recognizer | coffee: done | ac (0.332) | — | — | |
| 187 | starts wander leg 1: walk to wander_0; `most_likely` → d(item_6) | human, recognizer | ac_activation@wander_0: walk | d(item_6) (0.485) | — | — | One 15 cm step on the shelf_6 bearing: 0.333 → 0.485 (length-blind confirmation, TODO-61 (a)). |
| 194 | grasps item_7 at shelf_7 | robot | wander_0: walk | d(item_6) (0.585) | — | — | |
| 195 | trigger `task_committed`; cands item_7 48 / item_5 112 | robot | wander_0: walk | d(item_6) (0.603) | none(below_theta) | same | |
| 203 | confidence crosses θ ↑ on d(item_6); trigger `theta_crossed`; cands item_7 40 (662) / item_5 120 (59.4) | recognizer, robot | wander_0: walk | d(item_6) (0.756) | built | same | **Wrong crossing**: the human is on the wander, not delivering item_6. The only wrong crossing in the matrix; a walk geometrically indistinguishable from item_6's approach (the characterised limitation, TODO-61 (a)). A projection of d(item_6) is built and item_5 is assessed against it (59 cm); the argmin is unchanged. |
| 207 | waits at wander_0 (one tick) | human | wander_0: wait | d(item_6) (0.790) | — | — | Peak. Leg 1 ends 209; no boundary. Wrong-task ticks 203–213. |
| 210 | starts wander leg 2: walk to wander_1 | human | ac_activation@wander_1: walk | d(item_6) (0.799) | — | — | |
| 214 | confidence crosses θ ↓ | recognizer | wander_1: walk | d(item_6) (0.748) | — | — | The turn retracts item_6 (0.790 → 0.083 over the leg). |
| 219 | `most_likely` → `unknown` | recognizer | wander_1: walk | unknown (0.512) | — | — | |
| 223 | confidence crosses θ ↑ on `unknown`; trigger `theta_crossed`; cands item_7 20 / item_5 140 | recognizer, robot | wander_1: walk | unknown (0.791) | none(unresolved) | same | TODO-54. Reload (TODO-43). |
| 228 | waits at wander_1 (one tick) | human | wander_1: wait | unknown (0.910) | — | — | Leg 2 ends 230; no boundary. |
| 231 | starts d(item_6): walk from wander_1 to shelf_6 | human | d(item_6): walk | unknown (0.910) | — | — | |
| 242 | places item_7 at KT | robot | d(item_6): walk | unknown (0.911) | — | — | No pin. |
| 245 | trigger `no_current_task`; cand item_5 132 | robot | d(item_6): walk | unknown (0.911) | none(unresolved) | d(item_5) | |
| 270 | confidence crosses θ ↓ | recognizer | d(item_6): walk, 1 tick from shelf_6 | unknown (0.520) | — | — | item_6's arrival fold (0.474 at 272). |
| 272 | grasps item_6 at shelf_6 | human | d(item_6): grasp | unknown (0.520) | — | — | Not recognised at the grasp (TODO-57 question 3, TODO-61 (b)). |
| 274 | starts carry; `most_likely` → d(item_6); confidence crosses θ ↑; trigger `theta_crossed`; cand item_5 103 (125) | human, recognizer, robot | d(item_6): carry | d(item_6) (0.896) | built | same | Post-grasp reveal. |
| 310 | grasps item_5 at shelf_5 | robot | d(item_6): carry | d(item_6) (0.896) | — | — | |
| 311 | trigger `task_committed`; cand item_5 65 (882) | robot | d(item_6): carry | d(item_6) (0.896) | built | same | |
| 331 | places item_6 at KT; pin d(item_6); **episode boundary** (ac + `unknown`); `most_likely` → ac; confidence crosses θ ↓ | human, recognizer | d(item_6): place → done | ac (0.497) | — | — | Human's script ends; idle from 333. |
| 375 | places item_5 at KT | robot | idle | ac (0.497) | — | — | No pin. |
| 378 | trigger `no_current_task` → all tasks complete | robot | idle | ac (0.497) | none(below_theta) | — | Run ends (no-ops to 400, TODO-33). |

---

## Cross-condition facts visible in the tables

- **Exclusions by `min_safe_distance`** (all at `min_dist = 0.0`, the placement overlap at KT): s20_off 20
  (item_4), s20_on 6 (item_4), s30_off 28 (item_4), s30_on 21 (item_4). None in s00 or s40. No
  `RuntimeError` (every-candidate-excluded) in any of the eight runs; that case is scenario_10's, TODO-52.
- **Task switches caused by a projection**: s20_off 20 (item_4 → item_6) and 24 (back to item_4);
  s20_on 6 (item_4 → item_6); s30_off 28 and s30_on 21 (item_4 → item_2). Every other winner is either
  the executing task or the cheapest remaining one after a completion.
- **Already-delivered item re-picked from the table**: s00_off 166–169 (item_4, via a `theta_crossed` on
  `unknown`, TODO-54 / TODO-67 class) and s30_off 87–90 (item_2, TODO-67). Prior-on neither occurs.
- **Repeated `theta_crossed` per recognition** (prior-off only): s00_off 109 / 113 / 115, s20_off
  20 / 24 / 30 and 87 / 91 / 95 (TODO-68). One crossing per recognition in every prior-on condition.
- **`theta_crossed` on `unknown`**: s00_off 166, s40_off 226, s40_on 223 (TODO-54); the projection is
  `none(unresolved)` each time.
- **Wrong crossing**: s40_on 203 only (item_6 during the aligned wander leg).
- **Runs that do not finish**: s20 both conditions (item_7 in hand at 200). All other runs deliver
  everything and idle to the step limit (TODO-33).
