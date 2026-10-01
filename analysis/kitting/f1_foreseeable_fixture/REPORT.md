# F1 — Foreseeable-task fixture: `env_layout4` / `scenario_40` (baseline on the current recognizer)

> Superseding note (T-L stage 3, 26 Sept 2026): the layout and scenario ids here are the old ones; `docs/rename_table.md` maps them to the serial ids. The scripts and records stay frozen at their commit.

Built on top of `819b44f` (I1 audit). `shared/` untouched. Files changed: `domains/kitting/env_layout4.json`
(new), `domains/kitting/scenarios.py` (`scenario_40` appended), `domains/kitting/registry.py`
(import + `layouts` entry). Two baseline runs, `PYTHONHASHSEED=0`, 400 steps, assignment_prior off and
on; both complete (`[meta] step=378 all tasks complete`), no exception. s00/s20/s30 regression logs
re-run after the registry change: byte-identical to their baselines, both prior settings.

```
PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python mesa_sim/run_mesa.py \
    --domain kitting --layout env_layout4 --scenario scenario_40 --steps 400 --assignment_prior false|true
```

## How to read this directory

| File | Content |
|---|---|
| `measure.py` | Runs both conditions, reads `robot.belief` after every tick (no wrappers, nothing patched), labels ticks with the human's actual script segment and executor action, writes everything below plus byte-comparable logs (git-ignored). |
| `trace_s40_off.csv`, `trace_s40_on.csv` | **The baselines I3/I4 are compared against.** One row per tick: segment, human task/action/microaction/position/holding, robot task/holding, `most_likely`, `confidence`, and the full distribution (`p_*`). |
| `segments_s40_off.csv`, `segments_s40_on.csv` | One row per (segment × human action): step range, belief at start/end/max, ticks at or above θ, which `deliver_item` was above θ, `coffee_break` max, `unknown` range, winner sequence. |
| `angles.csv` | Bearings and angular separations of every segment's heading from every task target, from the layout file. |
| `summary.md` | the segment and angle tables as markdown. |

---

## 1. The `AC_switch` type match — resolved by measurement

`ac_activation` has **never** had a hypothesis in scenario_10. The I1 capture at `819b44f`
(`analysis/i1_ir_audit/captures.json`, condition `s10_off`, field `hypotheses`) lists exactly nine
keys: eight `deliver_item(?item=item_k, …)` and one `coffee_break(?coffee_machine=coffee_machine_0)`.
`object_types` in the same capture records `AC_switch_0 → "AC_switch"`.

Mechanism (read, then confirmed by the count): `SimModel._init_objects` (`mesa_sim/sim_model.py:231`)
groups objects by `obj.type` verbatim; `build_hypothesis_space` (`shared/recognizer.py:204`) does
`known_objects_by_type.get(param_types[v], [])` with `param_types["?ac_switch"] == "ac_switch"`
(`domains/kitting/tasks.py:171`). A plain `dict.get` is case-sensitive, so `"ac_switch"` finds
nothing, the product over an empty list is empty, and the task is silently absent — I1's
fallback 3.8, exactly as suspected. Consequences: s10's scripted `ac_activation` (its fifth task)
was never recognisable, and every count in the I1 audit that says "coffee_break is the only
foreseeable hypothesis" is correct for that reason.

It is a bug (a layout/schema spelling mismatch), **not fixed here**. Two candidate fixes, for
whoever takes it: (a) rename the object type in `env_layout1.json` to `ac_switch` — consistent with
every other type string in the domain (`kitting_table`, `coffee_machine`, all lowercase); (b)
change `parameter_types` in `tasks.py`. Either changes scenario_10's hypothesis space (9 → 10 keys)
and its `[IR-dist]` lines, so it must be re-baselined, not diffed. It also means the audit's
s10 figures (t=0 prior 0.111, grasp 0.662) would move.

Consequence for this fixture: it could not rely on layout1's AC object. `env_layout4` declares
`ac_switch_0` with type `ac_switch`, so `ac_activation(?ac_switch=ac_switch_0)` **is** in the
hypothesis space here (7 hypotheses + `unknown`; prior-on admissible set: item_3, item_6,
coffee_break, ac_activation, unknown). See §5(b) for what that costs.

---

## 2. Why a new layout, not a scenario on `env_layout1`

Measured on `env_layout1.json`: the coffee machine (−975, −275) sits 177 cm from shelf_1 and 276 cm
from shelf_2. From the kitting table (−200, 400), where every segment 2 has to start, the coffee
bearing is −139.0°; shelf_1 is at −131.4° (7.6° off), shelf_2 at −152.0° (13.0° off), shelf_6 at
−109.5° (29.5°). From any other plausible start the same three shelves stay within 5–15° of the
coffee bearing, because they surround it. The 45° constraint can be met on layout1 only against
*assigned* targets (by assigning east-side shelves), but with the prior off shelf_1/shelf_2 are
live decoys 8–13° off — the s10 failure mode again, testing the layout not the recognizer. So:
new layout, geometry chosen so that every constraint holds against **every** target, under both
prior settings.

---

## 3. Geometry (`env_layout4.json`, 2000 × 1200 cm, quadrant zones)

| object | position | role |
|---|---|---|
| kitting_table_0 | (0, 500) | sink; segment 2 starts here |
| shelf_3 / item_3 | (−950, −50) | human, segment 1 |
| shelf_6 / item_6 | (950, −150) | human, segment 4; segment 3a heads toward it |
| shelf_4 / item_4 | (850, 150) | robot task 1 |
| shelf_7 / item_7 | (950, 450) | robot task 2 |
| shelf_5 / item_5 | (950, −400) | robot task 3 (last, keeps the robot busy to step 378) |
| coffee_machine_0 | (−40, −250) | segment 2 target; x = −40 keeps the walk off the x = 0 zone boundary |
| ac_switch_0 | (400, 550) | second foreseeable target, never visited |
| wander_0 | (356, −210) | segment 3a end: exactly on the coffee → shelf_6 line at t = 0.40 (cross product 0) |
| wander_1 | (230, −550) | segment 3b end |
| human_0 start | (100, 550) | |
| robot_0 start | (−950, −550) | far corner so its first approach is long |

Human script (`scheduled_tasks`): deliver item_3 · coffee_break(coffee_machine_0) ·
ac_activation(wander_0) · ac_activation(wander_1) · deliver item_6. `assigned_tasks`: item_3, item_6.
Robot pool: item_4, item_7, item_5 (measured order of selection: 4 at step 0, 7 at 147, 5 at 245).

Measured angular separations (`angles.csv`; separation of the segment heading from the bearing to
each target, from the segment's origin):

| segment | origin → destination | bearing | length | nearest target (sep) | all other targets |
|---|---|---|---|---|---|
| 1 | (100, 550) → shelf_3 | −150.3° | 1209 cm | coffee 50.3° | shelf_5 102°, shelf_6 111°, shelf_4 122°, shelf_7 144°, ac 150° (table 3.2°, 112 cm behind — not a phase-1 target at t = 0) |
| 2 | table → coffee | −93.1° | 751 cm | shelf_5 49.6° | shelf_3 56.9°, shelf_6 58.7°, shelf_4 70.7°, shelf_7 90.0°, ac 100.2° |
| 3a | coffee → wander_0 | 5.8° | 398 cm | **shelf_6 0.0°** (by construction), shelf_5 14.4°, shelf_4 18.4°, shelf_7 29.5° | ac 55°, table 81°, shelf_3 162° |
| 3b | wander_0 → wander_1 | −110.3° | 363 cm | coffee 63.9° | shelf_3 76.7°, shelf_5 92.6°, shelf_6 116.1°, table 133°, shelf_4 146°, shelf_7 158°, ac 163° |
| 4 | wander_1 → shelf_6 | 29.1° | 824 cm | shelf_5 17.3°, shelf_4 19.4°, shelf_7 25.2° | ac 52°, table 73°, coffee 103°, shelf_3 128° |

Constraint check: segment 2 ≥ 45° off every target (min 49.6°, assigned min 56.9°) ✓; segment 3b
≥ 45° off every target from the turn point (min 63.9°) ✓; segment 1 ≥ 50° off everything ✓
(spec had no angular requirement here; s30's positive control had a 42° decoy). Segment 3a
deliberately points at shelf_6, with shelf_5/shelf_4 14–18° beside it: the robot delivers item_4
at step 147 (before 3a), so at 3a its target is the table; item_5 is undelivered until 378, so
prior-off it is a live 14° decoy in 3a — noted, not a constraint. Segment 4 (an addition, §5(c))
has the robot's undelivered item_5 17° off its heading — a prior-off decoy, inadmissible prior-on.
No segment ends within 30 cm of another task's target (closest: wander_1 to shelf_5, 735 cm;
wander_0 to shelf_6, 597 cm).

Robot/human separation: the robot's carries reach the table at steps ≈146, 244, 377; the human is at
the table at 115 and 331. No candidate was ever excluded (`feasible=True` on every `[meta-cand]`
line, both conditions); no exception.

## 4. Timeline (identical in both conditions — the human's script does not depend on the robot)

| segment | human action | steps | ticks | note |
|---|---|---|---|---|
| 1 | move_to shelf_3 | 0–59 | 60 | 1209 cm approach |
| 1 | pick_up | 60–61 | 2 | `holding(human_0, item_3)` from 60 |
| 1 | move_to table | 62–114 | 53 | |
| 1 | place | 115–116 | 2 | |
| 2 | move_to coffee | 118–154 | 37 | |
| 2 | wait_at coffee | 155–185 | 31 | 30 `stand` + advance |
| 3a | move_to wander_0 | 187–206 | 20 | toward shelf_6 |
| 3a/3b | wait + advance | 207–209 | 3 | the turn |
| 3b | move_to wander_1 | 210–227 | 18 | away from everything |
| 4 | move_to shelf_6 | 231–271 | 41 | |
| 4 | pick_up / carry / place | 272 / 274–330 / 331 | | |
| done | human idle | 333–378 | 46 | robot finishes at 378; IR called on every step 0–378 |

---

## 5. What the recognizer currently does in each segment (measured, `trace_*.csv`)

θ = 0.75. "L" is the chord likelihood of the linear cosine kernel (I1 §5).

**t = 0.** Prior-off: 8 keys uniform (0.125) with ZONE_BOOST ×2 on item_4 and item_7 (their shelves
are in zone_NE where the human starts) → `most_likely` item_4 at 0.200. Prior-on: 5 admissible keys
at 0.200; `most_likely` is **coffee_break** — an exact tie broken by the iteration order of the
`_admissible` set (I1 3.14 / TODO-42), not by evidence.

**Segment 1 — positive control.** One chord for the whole approach (I1's replace rule).
Prior-off: item_3 0.312 at step 1, 0.351 at step 5 (a robot-carried decoy moves), **0.520** from
step 55 when the human crosses y = 0 into zone_SW and item_3 gets ZONE_BOOST; prior-on: 0.479 at
step 1, **0.647** from step 55 for the same reason. At the grasp (step 60) the held-item refutation
pins the four other items, but coffee_break, ac_activation and unknown are not refuted, so the
belief is 4 : 1 : 1 : 1 → **0.569 in both conditions** — below θ. **The positive control never
crosses θ on the current code**: not mid-approach and not at the grasp. In s00/s20/s30 the same
grasp gave 0.797 because those layouts have no foreseeable hypothesis at all (4 : 1); in s10 it gave
0.662 (4 : 1 : 1, coffee only). With two foreseeable hypotheses it is 4/7. During the carry the
belief is frozen at 0.569 (phase-2 target is Var-bound → NEUTRAL, I1 3.1; the pin holds the rest).
At the release (115) the pin lifts and the other items return at the evidence they accumulated
underneath: prior-off item_3 0.294 with item_5 0.209 / item_6 0.179; prior-on item_3 0.502,
item_6 0.306.

**Segment 2 — coffee walk (the "can coffee_break win / must nothing cross θ" segment).**
coffee_break's target is Var-bound, so it receives NEUTRAL on every tick (I1 3.1); it cannot win.
Prior-off: the walk is credited to **item_5** (shelf_5 49.6° off; L = 3.0), 0.319 → 0.362 at step 142
(the human leaves zone_NW, and item_3 — whose "container" is now the table in zone_NW — loses its
×2) → 0.387; coffee_break peaks at **0.0205**, unknown at 0.0205. Prior-on: credited to **item_6**
(shelf_6 58.7° off, L = 2.9), 0.569 → **0.676** at step 142 for the same zone reason; coffee_break
max **0.045**. No `deliver_item` crosses θ in either condition (0 ticks ≥ θ) — but only by a margin
of 0.07 prior-on, and because of the kernel's value at 58.7°, not because the recognizer knows
where the human is going. The 30-tick wait changes nothing (stationary ticks are not scored).

**Segment 3a — heading toward shelf_6 (398 cm, 40% of the way).**
Prior-on: item_6 goes **0.676 → 0.826 at step 187 → 0.903 at step 188** and `theta_crossed` fires
at 187 — the robot builds a human projection for a delivery the human is not doing. Prior-off:
item_5 keeps winning (0.387 → 0.438 → 0.489) although shelf_6 is dead ahead (L 4.0) and shelf_5
14.4° off (L 3.88): the evidence carried over from segment 2 decides, not the chord. unknown
falls to 0.003–0.007.

**Segment 3b — the turn away (363 cm, ≥ 64° off everything).**
This is the retraction case and it does **not retract**. Prior-on: item_6 rises **0.903 → 0.942**
at step 210 and stays there; prior-off: item_5 rises **0.490 → 0.642**. Reason, read off the
kernel: at 116° off shelf_6 the chord scores L = 1.19, at 92.6° off shelf_5 L = 1.96, while
coffee_break, ac_activation and unknown get exactly 1.0 — walking away from a shelf is still
better evidence *for* that shelf than for `unknown`, because the linear kernel equals NEUTRAL at
cos = −0.54 (123° off) and exceeds it everywhere closer (I1 5.3: kernel mean 2.05 > NEUTRAL).
unknown ends segment 3 at **0.002 (off) / 0.006 (on)**: a walk that fits no task drives `unknown`
to the floor. This segment is the calibration case for I4's `unknown` mass and it currently
measures the opposite of the intended sign.

**Segment 4 — delivery of item_6 (bonus, §5(c)).** Prior-off: item_5 (17° off, undelivered)
stays `most_likely` through the whole approach at 0.644; the grasp at 272 gives item_6 **0.986**
(first θ crossing of the run, prior-off) — the pin plus the three NEUTRAL hypotheses already at
0.003. Prior-on: item_6 is already above θ since 187 and reaches 0.968 on the approach, 0.986 at
the grasp. At the release (331) the belief moves to **item_5 at 0.826 (prior-off)** — the robot's
own undelivered item, above θ, and stays there for the 46 idle ticks; prior-on item_6 0.823 (the
delivered item, table decoy).

Summary of the acceptance-relevant facts on the current code:

| criterion | prior off | prior on |
|---|---|---|
| segment 1 reveal ≥ θ | never (max 0.520; grasp 0.569) | never (max 0.647; grasp 0.569) |
| segment 2: any `deliver_item` ≥ θ | no (max 0.387, item_5) | no (max 0.676, item_6) |
| segment 2: `coffee_break` max | 0.021 | 0.045 |
| segment 3a: wrong reveal ≥ θ | no (item_5 0.489) | **yes**, item_6 0.826 at 187 → 0.903 |
| segment 3b: retraction | no — item_5 0.490 → 0.642 | no — item_6 0.903 → 0.942 |
| `unknown` at end of segment 3 | 0.002 | 0.006 |
| first θ crossing | 272 (grasp of item_6, correct) | 187 (item_6 while walking to wander_0, wrong) |

---

## 6. Decisions taken and surfaced

(a) **How the "fits nothing" walk is scripted.** The human can only execute `TaskInstance`s of
domain schemas, and every movement is a `move_to(object)`. Segment 3 is therefore scripted as two
`ac_activation` instances bound to objects of type `waypoint` (`wander_0`, `wander_1`), a type no
task's `parameter_types` names, so no hypothesis targets them; `ac_activation`'s method gives
`move_to` + a one-tick `wait_at`, i.e. a walk with a 3-tick pause at the turn. `coffee_break`
would have inserted a 30-tick stop. Costs: the per-step log and `trace_*.csv` label these ticks
`task=ac_activation`; the trace's `segment` column (from the script index) is the ground truth to
use. Alternative not taken: a dedicated non-intention `walk_to` schema in `domains/kitting/tasks.py`
— cleaner, but outside the allowlist (scenario, layout, registry). Whoever prefers it can swap the
two script entries; nothing else changes.

(b) **A live `ac_activation` hypothesis.** Because the new layout spells the type correctly, the
space has two foreseeable hypotheses. Effect on the current code: the segment-1 grasp reveal is
4/7 = 0.571 instead of 4/6 = 0.662 (coffee only) or 0.797 (none). Either way it is below θ, so
the positive control's behaviour does not hinge on this choice; what does is whether I3's
completion evidence is expected to refute foreseeable hypotheses at a grasp — this fixture will
show it. Omitting the AC object would reproduce s10's shape instead.

(c) **Segment 4 (deliver item_6) was added** so that `assigned_tasks` can contain item_6, which
makes shelf_6 an *admissible* target prior-on and lets segment 3a's "toward a shelf" fire under
both settings (it did: 187, prior-on). Without it, prior-on has no undelivered shelf hypothesis
during segment 3 and the retraction case exists only prior-off. Costs: a longer script, a third
robot task, and a 17° robot decoy on the segment-4 approach (prior-off). If segment 4 is unwanted,
drop the last script entry and item_6 from `assigned_tasks`; segments 1–3 are unaffected.

(d) **The robot has three tasks** (≈378 ticks) because the IR is only called while the robot is
unfinished (I1 7.12); the human ends at 333. Order relies on the meta-planner's cost ranking
(measured: item_4, item_7, item_5) — if `_cost()` changes, item_5 may stop being last and be
delivered before segment 4, which only removes the 17° decoy.

(e) **Prior-on t = 0 `most_likely` is coffee_break** by set-order tie-break. It affects nothing
downstream (no projection below θ) but will appear in any "first winner" comparison.

(f) **Segment 2's origin is the table**, where item_3 has just been delivered (I1 2.7 decoy): the
delivered item's target coincides with the leg origin up to the ≤ 30 cm placement offset, so its
chord value is arbitrary (here 0.14–0.31). Inherent to any delivery-then-deviation script; same in
s10.

## 7. What argues for a different shape

- Nothing in the measurements argues against the geometry: every constraint holds with margin
  (min 49.6°) and the intended failure modes appear exactly where predicted (3a reveal, 3b
  non-retraction, coffee NEUTRAL, unknown crushed).
- The positive control cannot cross θ on the current code as long as any foreseeable hypothesis
  exists (§5, segment 1). That is a property of the held-item refutation, which I3 deletes, not of
  the fixture; but it means "I3 improves the positive control" will be measured against 0.569, not
  0.797. If a θ crossing in segment 1 is wanted *today* as a reference point, the only way is a
  layout with no foreseeable hypothesis, which defeats the fixture.
- Segment 3a's 14° robot decoy (shelf_5, prior-off) is the one place where the fixture tests the
  layout as much as the recognizer; delivering item_5 earlier (robot order) would remove it but
  shorten the robot's work below the human's script.

## Verification

1. `measure.py`'s logs are byte-identical (`cmp`) to `run_mesa.py`'s own logs for the same
   conditions (`logs/run_20260913_094310.log` off, `run_20260913_094314.log` on).
2. s00/s20/s30 × off/on re-run after the registry edit: byte-identical to the I1 baselines
   (the layout file added later is not read by those scenarios).
3. `[meta-cand]` lines: `feasible=True` on every candidate evaluation (13 off, 14 on), `feasible=False` never; run ends
   with `all tasks complete`, no traceback.
4. Hypothesis space from the log: 7 keys + unknown; `[IR-prior] switch=on known=[item_3, item_6]`.
