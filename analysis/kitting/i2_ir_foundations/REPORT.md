# I2 — IR foundations: term → location resolution, guard-selected methods, observable wait_at

> Superseding note (T-L stage 3, 26 Sept 2026): the layout and scenario ids here are the old ones; `docs/rename_table.md` maps them to the serial ids. The scripts and records stay frozen at their commit.

> Superseding note (24 Sept 2026, the terminology ruling; `docs/glossary.md` §7, `docs/terminology_revision.md`): "The coffee walk is recognised" → `coffee_break`'s hypothesis clears θ (ROBOT). "A human about to execute a task the robot cannot recognise" → a task no hypothesis describes: unmodelled behaviour (WORLD); "declared as such" → a declared experimental condition (label C).

Built on `ff78636` (F1). Sweep: s00 (300 steps), s20 (200), s30 (200), s40 (400) × assignment_prior
off/on, `PYTHONHASHSEED=0`, interpreter `~/python-envs/teamrob-sp4-env/bin/python`. scenario_10 is
dropped (I1 O1; see §7 for what happened to it anyway). Baselines were recorded at `ff78636` before any
edit and are byte-identical on `[meta]`, `[IR]`, `[IR-dist]`, `[meta-cand]` to the I1/F1 logs.

## How to read this directory

| File | Content |
|---|---|
| `check_i2.py` | Unit checks U1–U3 (synthetic domains) and the instrumented sweep M1–M6 (wrappers on the robot's live recognizer, I1's technique). Writes `summary.md` and the CSVs below; its logs are byte-identical to `run_mesa.py`'s for the same conditions (whole file minus the start banner). |
| `summary.md` | Auto-generated: unit-check results, per-condition counts (progress calls, unresolved targets, at-target branch, methods selected, zone firings by kind, refutation equivalence, `waited` ticks). |
| `diff_ir.py` | `diff_ir.py BASE.log NEW.log` — tick-level attribution of belief differences between two logs (t=0, `most_likely` changes, changed-key episodes with the human's action, meta-line diff). What §4 was written from. |
| `zone_boost_episodes.csv` | Every ZONE_BOOST episode per condition, labelled `phase1` (as before), `phase2_table` (new: the carried item's hypothesis, target = table) or `robot_carried` (new: a robot-carried item resolving to the robot's zone). |
| `method_selection.csv` | Per condition, how many (hypothesis × tick) decompositions selected each method (by action count: 4 = `deliver_default`, 2 = `deliver_already_held`, 6 = `deliver_with_return`). |
| `waited_ticks.csv`, `at_target_firings.csv` | The ticks `waited(human_0, X)` was in the world; firings of the kernel's "already at target" branch (none). |
| `f1_traces/` | `trace_s40_off/on.csv`, `segments_s40_*.csv`, `summary.md` in F1's exact format, regenerated with F1's `measure.py` at this commit. **These replace F1's tables as the reference I3/I4 are compared against**; F1's own files are left as the pre-I2 record. |

---

## 1. What changed and where

| # | task item | change | files |
|---|---|---|---|
| 1 | term → location | `shared/target_resolution.py` (new): `object_position` (current location; a carried object through its holder — its `object_locations` entry is an agent id, a key of `agent_positions`), `movement_target_id` (`schema.movement_target_key` → binding), `movement_target_position`. The projector's inline lookup replaced by it. The recognizer grounds each hypothesis through `AdaptivePlanner.decompose()` (new public entry point; `plan()` wraps it) and scores the first movement action's target. `_get_expected_position`, `_get_target_zone`, `_get_relevant_action_schemas`, `_resolve_completion_predicate`, `_resolve_term_value` deleted; completion predicates are the planner-grounded ones. | shared/target_resolution.py, shared/planner.py, shared/projection.py, shared/recognizer.py |
| 2 | methods by guards | Selection = the planner's `_select_method`, per hypothesis per tick, with `?agent` = the observed agent. `DecompositionError(ValueError)` for world-dependent failure (no applicable method, derived var without a value); the recognizer catches it → NEUTRAL + one warning per episode. Schema errors (unbound var, unknown lookup) still raise. | shared/planner.py, shared/recognizer.py |
| 3 | wait_at | kitting `wait_at.completion = waited(?agent, ?entity)` (was `ProcessCompletion`). Executor: on the last STAND (`remaining == 1`, the decomposer now counts down) records `agent.waited_at = nearest fixed object`; cleared by the next step/grasp/release/touch. `world_state_builder` emits `waited(agent, obj)`. Executor's `ProcessCompletion` branch kept for dock_loading. | domains/kitting/actions.py, mesa_sim/executor.py, mesa_sim/action_decomposer.py, mesa_sim/world_state_builder.py, mesa_sim/sim_agents.py (attribute), shared/types.py (docstring) |
| 4 | sorted hypotheses | `self._hypotheses = sorted(hypotheses, key=repr)`; initial prior built in that order (was the admissible *set*'s order); `_pin` emits pinned keys sorted. | shared/recognizer.py |
| 5 | first observation | `RobotAgent.observe_initial()` — one `recognizer.update()` on the human's start position, called by `SimModel.__init__` after spawning; belief not stored. | mesa_sim/sim_agents.py, mesa_sim/sim_model.py |
| 6 | AC_switch | `env_layout1.json`: `AC_switch_0`/`AC_switch` → `ac_switch_0`/`ac_switch` (id too: scenario_10's script already bound `ac_switch_0`). | domains/kitting/env_layout1.json |
| — | literals | `"?item"` ×3, `"move_to"` ×3, `"holding"` ×2, `"in_zone"`, `"?agent"` removed from the recognizer. The held-item rule reads `AgentState.holding` and refutes a hypothesis binding a *portable* object (one with an `object_locations` entry) other than the held one — measured identical to the old rule on every refutation tick of every condition (M6, 0 mismatches). The zone comes from `obs.spatial_context.zone`. | shared/recognizer.py |

Left as the task specified: the kernel, HIGH/LOW/NEUTRAL, ZONE_BOOST's constant and rule, the held-item
rule, the assignment mask, the `ac_activation` / `coffee_break` branches of `_context_weight` (they still
name two kitting tasks in `shared/` — the one acceptance exception, by instruction), `"STEP*"` as the
continuous-vocabulary marker, `"?agent"` in `planner.py` (the injection convention, pl:110/297).
Remaining `?item` strings in `shared/` are docstring examples and a commented-out old
`build_hypothesis_space` in recognizer.py (dead code, flagged §8).

Decision on the two conflated questions (audit 4.3): the recognizer needs the object's **current**
location (where a fetcher walks to — a shelf, the table it was delivered to, or someone's hands); the
planner's `home_container_of` is a symbolic **return destination** and stays a derived var resolved at
decomposition. They are different questions and are kept apart; the movement target of the returned
item's `move_to` is then "position of that container", through the same function.

## 2. Verification

- Eight conditions run to completion, no traceback, no `not decomposable` warning (every kitting task has
  an unguarded fallback). Human and robot per-step lines byte-identical to baseline in all eight → the
  simulation side, including `wait_at` timing, is unchanged.
- `check_i2.py`: all unit checks PASS; **0 unresolved targets** over 675/270/575/230/570/228/1981/1132
  progress calls (I1: 64/261/61/54 per scenario); 0 undecomposable; 0 refutation mismatches; at-target
  branch 0 firings; `waited(human_0, ·)` at 184–186 (coffee_machine_0), 207–209 (wander_0), 228–230
  (wander_1) in s40 — visible for three ticks each.
- Hash-seed independence: s40 off/on byte-identical on the four greps under `PYTHONHASHSEED=0`, `1`, `2`.
- Wall time unchanged (s40, 400 steps: 2.6 s before and after).
- dock_loading registry imports.
- Stage attribution (§3): the work was replayed in a worktree in four stages — A = sorting only,
  B = A + priming, C = B + resolution/guards, D = C + wait_at/layout/executor (= HEAD) — and each stage
  diffed against the previous one with `diff_ir.py`.

## 3. Attribution of every difference, by stage

| condition | A sorting (base→A) | B priming (A→B) | C resolution (B→C) | D wait_at+layout (C→D) |
|---|---|---|---|---|
| s00_off | 0 numeric; key order only (69 ticks); t=0 winner item_3→… (tie) | 132 ticks, max Δ 0.114, first tick 0; winner differs t=0 only | 126 ticks from 43, max Δ 0.687; winner differs 78–110, 142–168 | none |
| s00_on | 0 numeric; order 169 ticks; t=0 winner | 132 ticks, max 0.207 | 126 ticks from 43, max 0.707; winner 78–110 | none |
| s20_off | 0 numeric; order 66; t=0 | 168 ticks, max 0.106; winner 0, 4–10 | 176 ticks from 24, max 0.683; winner 54–88, 122–199 | none |
| s20_on | 0 numeric; order 200; t=0 | 168 ticks, max 0.295; winner 0, 122–199 | 176 ticks from 24, max 0.588; winner 57–88 | none |
| s30_off | 0 numeric; order 59; t=0 | 110 ticks, max 0.114 | 127 ticks from 41, max 0.730; winner 74–97, 165–167 | none |
| s30_on | 0 numeric; order 168; t=0 | 110 ticks, max 0.215 | 127 ticks from 41, max 0.729; winner 74–97 | none |
| s40_off | 0 numeric; order 115 | 305 ticks, max 0.208 | 379 ticks from 0, max 0.965; winner 60–64, 118–378 | none |
| s40_on | 0 numeric; order 379; t=0 | 283 ticks, max 0.278 | 379 ticks from 0, max 0.965; winner 60–64, 118–378 | none |

**A — sorting.** No value changes anywhere. `[IR-dist]` lists tied entries in key order, and the t=0
`most_likely` under a uniform prior is the alphabetically first tied key instead of the layout's or
the admissible set's first: s00_off/s20_off/s30_off item_2 (was item_3/item_4/item_3); s00_on/s20_on
item_2 and s30_on item_3 (was `unknown`, the set's first); s40_on ac_activation (was coffee_break);
s40_off unchanged (item_4 is ×2-boosted at t=0 and first among the boosted pair either way).
Reproducible, not meaningful (TODO-42).

**B — priming.** Tick 0 is now a scored chord (start → first position, 20 cm): s00_off t=0 item_3 0.210
instead of the 0.167 prior, unknown 0.053. Every later value in the first leg differs in the third
decimal because the leg's origin moved 20 cm back to the start position (bearings to far targets change
by < 1°), and the difference propagates through the evidence state at the 10⁻³ level for the rest of the
run. Two winner changes come from near-ties this shifts: s20_off steps 4–10 (item_3 0.207 vs item_7
0.209) and s20_on 122–199 (the post-completion plateau, TODO-21: item_3 0.500 / item_2 0.463 becomes
item_2 0.488 / item_3 0.477). Priming changes no θ crossing.

**C — resolution and guard selection.** Every large difference is here, and all of it starts at the first
grasp (s00 41→43, s20 22→24, s30 39→41) or, in s40, at tick 0 (the foreseeable hypotheses resolve from
the start). Four mechanisms, each measured:

1. *The carry leg scores.* The held item's hypothesis targets the table (`deliver_already_held`), chord
   L = 4.0 → 0.797 at the grasp (unchanged: the grasp tick itself is a zero chord) rises to 0.94 on the
   first carry tick and **0.966** once the human enters the table's zone (mechanism 2). Base: frozen at
   0.797 (NEUTRAL). s00/s20/s30, both settings, every carry.
2. *ZONE_BOOST phase-2 branch.* The target zone is the chord target's zone, so the carried item's
   hypothesis gets ×2 in the table's zone: 20/20/21/21/42/42/50/50 new (tick × hyp) firings per
   condition (`zone_boost_episodes.csv`, kind `phase2_table`) — TODO-37(b)'s "correct phase-2 branch".
   Prior-off only, a robot-carried item now resolves to the robot's zone (kind `robot_carried`: s00_off
   item_6 78–80, item_4 147–165; s40_off item_5 340–375 — 22/0/0/0/0/0/36/0 firings). Old counts
   (I1 §5.4) plus these equal the new totals exactly.
3. *`deliver_with_return` for every other item during a carry.* While the human holds X, every
   `deliver_item(Y≠X)` hypothesis decomposes to `deliver_with_return` (256/64/244/61/216/54/440/110
   hypothesis-ticks per condition, `method_selection.csv`), whose first movement is to X's home shelf —
   behind the human on every carry — so under the pin they collect L ≈ 0.1 per carry leg (base: scored
   against their own shelves, L 1–3). At the release the pin lifts and they return crushed:
   s00_off step 78 item_3 **0.805** (base 0.120; base winner item_7 0.351), item_7 0.051 (0.351),
   item_4 0.138 (0.356); s20_off 54: item_3 0.801 (0.222); s30_off 74: item_3 0.853 (0.124). The
   delivered item then stays `most_likely` through the next approach until the grasp (s00 78–110,
   s20 54–88, s30 74–97) — TODO-37(a) sharper (TODO-51).
4. *Foreseeable targets resolve* (s40 only): `coffee_break` and `ac_activation` receive chords from
   tick 0. §4.

Downstream (meta lines, all from C): θ-crossing steps and winners, base → new:

| condition | base crossings | new crossings | reading |
|---|---|---|---|
| s00_off | 41 item_3 (0.797), 111 item_2 (0.970) | 41 (0.797), 111 (0.796) | same steps; 111 lower because item_3 (delivered) still holds 0.11 |
| s00_on | 41, **81** item_2 (0.856, mid-approach) | 41, **111** item_2 (0.796, grasp) | second reveal 30 ticks later — mechanism 3 |
| s20_off | 22 item_3, 89 item_2 (0.928) | 22, 89 (0.766) | same steps |
| s20_on | **11** item_3 (0.780, zone reveal), **82** item_2 (0.851) | 11 (0.770), **89** (0.766) | 11 stands (0.770: the leg-1 chord under priming); second reveal 7 ticks later |
| s30_off | 39 item_3, 98 item_7 (0.976) | 39, 98 (0.876) | same steps |
| s30_on | 39, **77** item_7 (0.917) | 39 only | at 98 `most_likely` flips item_3 (0.782, ≥ θ) → item_7 (0.876) with no crossing: **the TODO-48 case, first measured occurrence**; the robot keeps the projection from step 39 |
| s40_off | 272 item_6 (0.986, grasp) | **142 coffee_break** (0.811), 210 coffee_break (0.860) | §4 |
| s40_on | **187 item_6 (0.826, wrong)** | 142 coffee_break (0.814), 210 (0.887) | wrong reveal gone; §4 |

Robot behaviour (its per-step lines and `[meta]` winners/queues) is identical in all eight conditions:
the changed triggers only rebuilt the human projection; no candidate was excluded (`feasible=False`
never appears).

**D — wait_at, executor, layout.** No difference on any grep in any condition (`stand` ticks are not
scored in I2; the executor's completion timing is the same tick as before).

## 4. scenario_40 (the F1 fixture) after I2

`f1_traces/summary.md` is the full segment table. Against F1's acceptance facts:

| criterion | F1 off | I2 off | F1 on | I2 on |
|---|---|---|---|---|
| segment 1 reveal ≥ θ | never (max 0.520; grasp 0.569) | never (0.391 at 55; grasp **coffee_break 0.549**; 0.696 at the end of the carry) | never (0.647; 0.569) | never (0.461; 0.549; 0.696) |
| segment 2: any `deliver_item` ≥ θ | no (0.387 item_5) | no (item_3 0.400, the delivered item, until it loses ZONE_BOOST at 142) | no (0.676 item_6) | no |
| segment 2: `coffee_break` max | 0.021 | **0.811 (θ at 142)** | 0.045 | **0.814 (θ at 142)** |
| segment 3a: wrong reveal ≥ θ | no | no (coffee_break stays winner, 0.77 → 0.61) | **yes, item_6 0.826 at 187** | **no** |
| segment 3b: retraction | no (item_5 0.49 → 0.64) | no — `coffee_break` 0.61 → **0.86** (64° off it; every shelf ≥ 77°) | no (item_6 0.90 → 0.94) | no — coffee_break 0.63 → 0.89 |
| `unknown` at end of segment 3 | 0.002 | 0.0035 | 0.006 | 0.0036 |
| segment 4: winner at the grasp of item_6 | item_6 0.986 (correct) | **coffee_break 0.962** | item_6 0.986 | **coffee_break 0.962** |
| first θ crossing | 272 (correct grasp) | 142 (coffee_break, correct) | 187 (item_6, wrong) | 142 (coffee_break, correct) |

Three things to read off this, stated with both readings where there are two:

- *The coffee walk is recognised* — the segment-2 criterion F1 could not meet is met, at the honest
  chord (L = 4.0 dead on, 0.550 from step 118) plus a zone-state event at 142 (item_3, delivered and at
  the table in zone_NW, loses its ×2 when the human leaves the zone; 0.550 → 0.811). The crossing is
  therefore half evidence, half ZONE_BOOST, the same shape as s20_on's step 11; when ZONE_BOOST goes
  (I3) expect the crossing to move later or vanish at this kernel.
- *The grasp of item_3 makes `coffee_break` the winner (60–64, 0.549).* The pin refutes the other four
  items; `coffee_break` had collected 0.32 during the 1209 cm approach (50° off it, L = 3.0) and is not
  refuted, so with item_3 at 4 : coffee 3 : ac 1 : unknown 1 on that tick's evidence — the positive
  control's grasp is credited to a foreseeable task. Reading (a): correct under the current model — a
  hypothesis that predicts nothing at a grasp should not be refuted by it; the fix is completion
  evidence for `pick_up` (I3), which today is unreachable (I1 2.2). Reading (b): the held-item rule is
  wrong to spare hypotheses with no portable object. Either way it is I3's evidence model, not I2's
  plumbing; the number to beat is 0.549.
- *`coffee_break` never lets go* (TODO-50): winner from 118 to the end, 0.96 at the grasp of item_6,
  0.89–0.90 while the human is idle. Never refuted by a grasp, never completed, and every later leg still
  scores it moderately (3b: 64° off → 2.9; 4: 103° off → 1.6). This is I1's C5 in its clearest form and
  the reason `wait_at` had to become observable: `waited(human_0, coffee_machine_0)` is in the world at
  184–186, and a phase model that completes `coffee_break` on it has exactly what it needs. Do not
  patch this with a decay: the fixture now measures the missing completion, which is the point.

The wander is still unmodelled from the recognizer's side: the `ac_activation(wander_*)` script entries
bind objects of type `waypoint`, which no `parameter_types` names, so there is no hypothesis for them;
`ac_activation(ac_switch_0)`'s chord target is the switch at (400, 550) and it receives 0.03–0.07
throughout segment 3. Guard checking did not change this (the schema has no guards); term resolution
did make `ac_activation`'s own target resolve, which it never had (F1 §5(b) measured it NEUTRAL). The
`waited(human_0, wander_0/1)` facts at 207–209 / 228–230 are emitted by the body as for any wait; no
hypothesis reads them.

## 5. Acceptance

| criterion | evidence |
|---|---|
| every difference attributed | §3 stage table; `diff_ir.py` per condition; the four mechanisms of stage C each measured in `summary.md` / the CSVs |
| no kitting object/parameter/action/task named in `shared/` | grep §1: recognizer has none; `_context_weight`'s two task names kept by instruction; `"?agent"` stays in planner.py; audit's 1.7–1.9 predicate names all removed from the recognizer |
| no `methods[0]` | grep: none in code (one rewritten comment) |
| coffee_break's and every carry leg's target resolves | M1: 0 unresolved targets in all eight conditions |
| no crash on unsatisfiable guards | U1: NEUTRAL, one warning, scores again when the guard holds; an unbound variable raises (U2, by design) |

## 6. Proposal — how a type-name mismatch should surface (audit 3.8)

The `AC_switch` case was a spelling error that looked like a recognizer merely uncertain for the whole
life of scenario_10. Two facts distinguish an error from a layout that legitimately lacks an object:
the *scenario scripts a task* the hypothesis space cannot contain, and/or the layout has a type that
matches the schema's *except for case*. Proposal (TODO-49), three small pieces, none a framework:

1. `build_hypothesis_space()` logs one `[IR-space]` line per intention with its hypothesis count. The
   log then states which tasks are recognisable in this layout; "coffee_break is the only foreseeable
   hypothesis" would have been a line to read, not a count to infer.
2. At spawn, every scripted task of every human must have its key in the robot's hypothesis space and
   every bound object id must exist in the layout — raise, do not warn. A human about to execute a task
   the robot cannot recognise is never a fixture's intent (the wander in s40 is the one deliberate
   exception and it would have to be declared as such — e.g. a `walk_to` schema, F1 §6(a)).
3. At hypothesis-space construction, a parameter type with a case-insensitive but not exact match among
   the layout's types is an error.

The same principle drove one I2 decision already: an unbound variable in a hypothesis raises instead of
scoring NEUTRAL.

## 7. Outside the sweep

- **scenario_10** now runs 300 steps in both prior settings without the step-257 `RuntimeError`. Not a
  fix: the belief at 257 is `ac_activation` at 0.69 (the hypothesis exists since the layout fix), so no
  `theta_crossed` fires there and the meta-planner branch that raised is not reached (TODO-52). The
  hypothesis space is 10 keys (was 9).
- dock_loading: `wait_at` still `ProcessCompletion` (deferred domain, not modified); `office_break`
  would be handled by U1's path; `confirm_delivered_pallet` would raise on the first tick (TODO-25).

## 8. For I3, before it builds the phase model

1. **Method re-selection per tick is now the mechanism, and it has teeth** (§3 C.3, TODO-51). "Phase k"
   under `deliver_with_return` is a different action list from phase k under `deliver_default`; the
   audit's open question (§9) is now concrete: when the held item changes, the six-step method's index
   0 is "walk to the other item's shelf". I3's "last completed action" must be robust to the method
   changing under it — store the action (name + bindings), never an index (already decided).
2. **The delivered item's lead after a release is 0.8** (was 0.35). The completion pin is load-bearing
   for every next-task reveal time; the s00_on 81 → 111 and s30_on no-crossing figures are the
   reference. The pin needs "completed by the observed agent", which the world does not say (I1 §8
   note, O10): `obj_at(item_7, kitting_table_0)` is true for the robot's deliveries too.
3. **A foreseeable task needs a completion or it is permanent** (TODO-50). `waited(agent, entity)` is
   the only observable end of `coffee_break` / `ac_activation`; it is visible for three ticks after the
   last STAND (body-side persistence until the next microaction). If I3 checks completion every tick that
   is enough; if it checks only on events, `stand` is still not an event (STAND* is a string, I1 2.8).
4. **The grasp tick itself is unchanged** (0.797 in s00/s20/s30, 0.549 in s40): dispatch still returns
   from `move_to` for every observation, so `pick_up`/`place` completion predicates are never evaluated.
   They are now correctly grounded on every `GroundedAction` (`completion_predicate`), so the phase
   model gets them for free once it dispatches on the current action instead of the first one.
5. **The kernel's "already at target" branch never fired** (0 in all conditions): the human stops up to
   one step short of a target (PROXIMITY_THRESHOLD 30 cm), so a leg never starts exactly on it. Not a
   safe assumption for ROS.
6. **`DecompositionError` vs `ValueError`**: a hypothesis with no applicable method is NEUTRAL and
   logged once per episode; a schema that cannot be grounded raises on the first tick. If I3 wants a
   third outcome (e.g. "completed, hence no method"), it is a new class, not a widening of the catch.
7. **`ZONE_BOOST` now fires during carries** (phase-2 branch) and for robot-carried items. Its removal
   (I3) therefore moves the mid-carry 0.966, s40's step-142 coffee crossing (half of it is item_3 losing
   ×2) and s20_on's step-11 crossing (as I1 predicted).
8. **`[IR-dist]` and tie-breaks are alphabetical by key** now. A t=0 winner is still a tie, not
   evidence.

## Flagged, not fixed (outside scope)

- `shared/recognizer.py`: stray `from importlib.metadata import distribution` (I1 O7); dead
  commented-out `build_hypothesis_space` block; `CONFIDENCE_THRESHOLD` unused (O8); module docstring
  lines 12–13 still describe a grasp → HIGH/LOW rule that never fires (I1 10.6) — evidence-model text, I3's.
- `mesa_sim/action_decomposer.py` still resolves movement targets from the model with its own
  `_resolve_movement_target` (embodiment side; not one of the three callers the task named) and reads
  `"?item"`/`"?duration"` (O5, TODO-01).
- `docs/io_contracts.md` §2.1/§2.2 not updated (drift 10.9–10.11 remain; the task named the two docs
  that were updated).
- `CLAUDE.md`'s "prefix with PYTHONHASHSEED=0 until TODO-42 is fixed": the recognizer no longer needs
  it (measured on s40 only); other consumers of `get_all_intentions()` order were not checked.

## 9. Hand-off for I3 (what the commit history does not say)

Reproduce any number below with, at `dd680ea` or later:

```
PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python mesa_sim/run_mesa.py \
    --domain kitting --layout env_layout<N> --scenario scenario_<N>0 --steps <300|200|200|400> --assignment_prior <false|true>
PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python analysis/i2_ir_foundations/check_i2.py     # summary.md + CSVs
python3 analysis/i2_ir_foundations/diff_ir.py <before.log> <after.log>                              # per-tick attribution
```
Steps per scenario: s00 300, s20 200, s30 200, s40 400. `[IR]`, `[IR-dist]`, `[meta]`, `[meta-cand]`
are the regression greps; at this commit they are byte-identical across PYTHONHASHSEED 0/1/2/7 on s40.

**(a) The `deliver_with_return` rival-targeting effect.** What it is: while the observed human holds X,
`AdaptivePlanner.decompose()` selects `deliver_with_return` for every `deliver_item(Y≠X)` hypothesis
(guards `holding(?agent, ?other)` ∧ `not_equal(?other, ?item)` hold with `?other = X`), whose first
action is `move_to(?target = home_container_of(X))` — X's shelf, which the human has just left. The
carry chord toward the table is therefore ≈180° off every rival's target: L ≈ 0.1 per rival per carry
leg, against 4.0 for `deliver_item(X)`. The rivals are pinned on output during the carry (held-item
rule), so nothing shows until the release; then they return with that evidence. Counts:
`method_selection.csv`, `deliver_item:6` = 256/64/244/61/216/54/440/110 hypothesis-ticks per
condition (off/on for s00, s20, s30, s40).

Release-tick distributions it produced (base → I2; base logs are the I1/F1 baselines at `ff78636`):

| condition | release tick | delivered item | best rival |
|---|---|---|---|
| s00_off | 78 | item_3 0.120 → **0.805** | item_7 0.351 → 0.051; item_4 0.356 → 0.138 |
| s00_on | 81 | item_3 0.118 → **0.804** | item_2 0.856 → 0.154 |
| s20_off | 54 | item_3 0.222 → **0.801** | item_6 0.277 → 0.061; item_4 0.267 → 0.060 |
| s30_off | 74 | item_3 0.124 → **0.853** | item_7 (next task) reaches only 0.176 at 93 (was 0.704) |

θ crossings it moved (the human's next assigned task): s00_on 81 → 111 (mid-approach → grasp, 0.856 →
0.796); s20_on 82 → 89 (0.851 → 0.766); s30_on 77 → none (item_7's grasp at 98 flips the winner
item_3 0.782 → item_7 0.876 with both sides ≥ θ, so `theta_crossed` never fires: TODO-48's first
occurrence). What would show it is gone: with a completion pin on the delivered task, the release
tick should put the delivered item at BELIEF_FLOOR and the next-task crossing at ≤ 81 (s00_on), ≤ 82
(s20_on) and a crossing on item_7 in s30_on at ≤ 77 — i.e. back to or better than baseline. If the
crossings return but the rivals still come back near-uniform at the release (all ≈ 0.02–0.14 as now),
the pin is masking the effect rather than removing it; the direct check is the rivals' evidence at the
release tick (`_evidence`, not the output) — under reading (b) of TODO-51 (freeze evidence under a
hard refutation) it would equal their pre-grasp evidence.

**(b) TODO-50, `coffee_break` never releasing (s40).** Trace (`f1_traces/trace_s40_*.csv`, column
`p_coffee_break`; off / on): 0.550 / 0.550 from step 118 (first coffee-walk chord, L = 4.0 dead on);
**0.811 / 0.814 at 142** — the θ crossing, which is a ZONE_BOOST event (the delivered item_3 at the
table in zone_NW loses ×2 when the human leaves the zone), not new chord evidence; flat through the
wait 155–185; 0.772 / 0.780 at 187 falling to 0.612 / 0.633 by 206 (segment 3a: shelf_6 dead ahead
scores 4.0, coffee 50°+ off); **0.860 / 0.887 at 210** (segment 3b: coffee 63.9° off → L ≈ 2.9, every
shelf ≥ 77°) — a second `theta_crossed`; 0.758 / 0.815 through the approach to shelf_6 (231–271,
coffee 103° off → L ≈ 1.6, but the lead holds); **0.962 at 272**, the grasp of item_6 (the pin removes
items 3/4/5/7; coffee is not refuted; item_6 is at 0.022); 0.959 → 0.949 through the carry (coffee is
29° off the carry direction, L ≈ 3.5); 0.892 / 0.903 from 331 to the end. `unknown` ends segment 3 at
0.0035 / 0.0036. The completion fact I3 can use: `waited(human_0, coffee_machine_0)` is in
`world.predicates` at steps 184, 185, 186 (`waited_ticks.csv`); `at(human_0, coffee_machine_0)` holds
from 154. Success criterion for I3 on this fixture: `coffee_break` ≥ θ during 118–186 and at
BELIEF_FLOOR (or no longer `most_likely`) from 187 on; item_6 `most_likely` by the grasp at 272 (base
prior-off: 0.986 there), and no `deliver_item` ≥ θ during 187–229.

**(c) TODO-51, last-completed-action versus method re-selection.** Concrete case, s00: the human
holds item_3 from 41 to 77. On every one of those ticks `deliver_item(item_2)` decomposes to six
actions [`move_to(shelf_3)`, `place(item_3, shelf_3)`, `move_to(item_2)`, `pick_up(item_2)`,
`move_to(kitting_table_0)`, `place(item_2, kitting_table_0)`]; at 78 (release) it decomposes to four
[`move_to(item_2)`, `pick_up(item_2)`, `move_to(kitting_table_0)`, `place(…)`]; `deliver_item(item_3)`
meanwhile is two actions [`move_to(kitting_table_0)`, `place(…)`]. An index into the list is meaningless
across a re-selection (index 0 is "return item_3" in one and "fetch item_2" in the other). A stored
`(action_name, bindings)` — the decision already taken — must be *searched for* in the newly selected
list each tick, and may be absent (a completed `move_to(item_2)` does not appear in
`deliver_already_held`), so I3 needs a rule for "last completed action not in the current method":
the candidates are "restart at index 0 of the new method" and "treat as completed past the end".
`GroundedAction` has no method name; if I3 needs it, add it to the planner's output rather than
inferring it from the action count as `check_i2.py` does for analysis.

**(d) Two more numbers I3 will be measured against.** The grasp tick is unchanged by I2 (0.797 in
s00/s20/s30, 0.549 in s40 where `coffee_break` and `ac_activation` survive the pin); the mid-carry
0.966 includes the phase-2 ZONE_BOOST ×2 and will drop to ≈ 0.94 when ZONE_BOOST goes.
