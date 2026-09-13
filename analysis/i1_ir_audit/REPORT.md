# I1 — IR audit (report only, no fixes)

Code at HEAD `89b998d` (main, clean tree). `shared/`, `domains/`, `configs/` untouched. Eight runs
(s00/s10/s20/s30 × assignment_prior off/on), `PYTHONHASHSEED=0`, interpreter
`~/python-envs/teamrob-sp4-env/bin/python` (3.10). Every instrumented log is byte-identical to its
baseline (§Verification). Nothing below proposes a design; where a finding is ambiguous both
readings are recorded and the evidence that would settle it is named.

Line numbers refer to the files at `89b998d`. `rec:` = `shared/recognizer.py`,
`lf:` = `shared/likelihood_functions.py`, `pl:` = `shared/planner.py`.

## How to read this directory

| File | Content |
|---|---|
| `measure.py` | Drives the eight conditions with instance-level wrappers on the robot's live `IntentionRecognizer` (every helper: `_likelihood`, `_progress_likelihood`, `_get_expected_position`, `_get_target_zone`, `_context_weight`, `_refuted_by_holding`, `_resolve_completion_predicate`, `_resolve_term_value`, `_weigh`, `_output`, `_finalize`). Records inputs, branch taken and result per (tick × hypothesis), plus the human's actual executor state and an external evaluation of every declared completion condition. Writes `captures.json` (git-ignored, 12 MB) and byte-comparable logs (git-ignored). |
| `analyze.py` | `captures.json` → every table below. |
| `a_evidence_paths.csv` | §6 — per condition, counts of every evidence path over all likelihood calls. |
| `b_target_resolution.csv` | §3/§6 — per hypothesis, which branch of `_get_expected_position` answered. |
| `c_zone_boost_episodes.csv` | §6 — every maximal step range in which ZONE_BOOST carried ×2 for a hypothesis. |
| `d_held_item_refutation_episodes.csv` | §6 — every held-item refutation episode, with belief before/at/after. |
| `e_legs.csv` | §7 — every movement leg against the human's actual action boundaries. |
| `f_completion_reachability_human_plan.csv` | §8 — the human's live plan's completion predicates, evaluated externally per tick. |
| `f2_completion_groundable_from_hypothesis.csv` | §8/§9 — every action of every method, grounded from hypothesis bindings only. |
| `g_belief_events.csv` | §6 — every `most_likely` change and θ crossing with the state factors active at that tick. |
| `h_kernel_values.csv` | §5 — the chord likelihood values the kernel actually produced. |
| `j_discrete_ticks.csv` | §6 — the likelihood every hypothesis received from each discrete event. |
| `summary.md` | all tables as markdown, auto-generated. |

Counts per category: 1: 9 · 2: 17 · 3: 14 · 4: 9 · 5: 15 · 6: 9 evidence paths measured ·
7: 12 state items + 7 conflicts · 8: 6 schemas, 16 (task, method, step) sites · 9: 6 sites ·
10: 14 drift items. Outside-IR: 10.

---

## Run facts the rest of the report relies on

| condition | IR ticks | hypotheses | inadmissible | moving / discrete / stationary ticks | likelihood calls | note |
|---|---|---|---|---|---|---|
| s00_off / on | 169 | 5 | 0 / 3 | 130 / 4 / 35 | 670 / 268 | robot finishes at step 169; the IR is not called after that (`sim_agents.py:250`) although the run is 300 steps |
| s10_off / on | 258 | 9 | 0 / 4 | 215 / 3 / 40 | 1962 / 1090 | run ends at step 257 with `RuntimeError` from `MetaPlanner._replan_tasks` (no feasible candidate, `min_dist=0.0`) — identical in the unmodified baseline; outside the IR (§Outside) |
| s20_off / on | 200 | 5 | 0 / 3 | 110 / 4 / 86 | 570 / 228 | human finishes at step 123; 76 more IR ticks with nothing moving |
| s30_off / on | 168 | 5 | 0 / 3 | 109 / 4 / 55 | 565 / 226 | robot finishes at step 168 |

Every documented belief figure was reproduced exactly (`g_belief_events.csv`): grasp confidence
0.797 in s00/s20/s30; s20_on θ at step 11 (0.780); s30_on 0.471 on the first chord, 0.640 on
zone_SW entry at step 23, θ at the grasp (39); s10_on θ at step 107 on item_6 (0.853) during the
coffee walk; s10 θ at 257 (0.769).

---

## 1. Domain literals in `shared/`

Everything below is a string that names a kitting-domain object, parameter, predicate, action or
task. Predicate names emitted by the world-state builder (`holding`, `in_zone`) are listed too:
they are not declared by any schema the recognizer reads, so they are a contract by convention.

| # | site | literal | what depends on it | generic mechanism that exists |
|---|---|---|---|---|
| 1.1 | `rec:493-495` `_refuted_by_holding` | `"?item"` | the whole held-item refutation (16 episodes, `d_*.csv`) — being deleted | `TaskSchema.parameter_types` names the enumerable parameters; `ActionSchema.completion` of `pick_up` names which parameter `holding` binds |
| 1.2 | `rec:753` `_get_expected_position` | `"?item"` | phase-1/phase-2 branch; every chord target for `deliver_item` | same |
| 1.3 | `rec:793` `_get_target_zone` | `"?item"` | ZONE_BOOST target for `deliver_item` — being removed | same |
| 1.4 | `rec:761, 778, 804` | `"move_to"` | which step supplies the chord target and the zone; any domain whose movement action is named differently gets NEUTRAL everywhere | `ActionSchema.movement_target_key` / `movement_target_type` / `progress_evaluator` (used by `action_decomposer.py:199-209` and `projection.py:248-257`, never by the recognizer) |
| 1.5 | `rec:720` `_context_weight` | `"ac_activation"` | TEMPERATURE_BOOST — condemned, deferred to the context pass | none in the schema today (no context-relevance field) |
| 1.6 | `rec:726` `_context_weight` | `"coffee_break"` | FATIGUE_BOOST — condemned | none |
| 1.7 | `rec:485, 755` | predicate name `"holding"` | held-item detection and phase-2 detection | `pick_up.completion` is `holding(?agent, ?item)` — the name is available from the schema |
| 1.8 | `rec:715` | predicate name `"in_zone"` | ZONE_BOOST — being removed | none (no schema declares `in_zone`; `world_state_builder.py:110` is the only emitter) |
| 1.9 | `rec:681` `_resolve_term_value` | `"?agent"` | completion-predicate grounding (never reached, §6) | `pl:72, 265-266` use the same literal — a shared convention, not a domain literal; listed for completeness |

`build_hypothesis_space` (`rec:191-211`) and `_build_admissible_keys` (`rec:308-343`) contain no
literals. `likelihood_functions.py` contains none. `planner.py` has `"not_equal"`, `"zone_of"`,
`"home_container_of"` (`pl:172, 241, 243`) — evaluator names, not domain objects; noted under §9.

---

## 2. Structural assumptions

| # | site | assumption | true of kitting today because | what depends on it / where it bites |
|---|---|---|---|---|
| 2.1 | `rec:626` `_get_relevant_action_schemas` | `methods[0]` is the decomposition | `deliver_item.methods[0]` is `deliver_already_held` (`move_to`, `place`) | TODO-46(1). Measured: 0 of 5,579 likelihood calls reached a completion check in any condition (`a_*.csv`, `branch_completion`). `pick_up`'s `GRASP` vocabulary is not in `methods[0]` at all |
| 2.2 | `rec:560-575` `_likelihood` | first schema that answers wins (return inside the loop) | the first schema of every method is `move_to` (STEP*) | even `RELEASE`, which *is* in `place`'s vocabulary in `methods[0]`, never reaches `place` — `move_to` returns first. Measured at every release tick: all hypotheses get exactly 1.0 (`j_*.csv`) |
| 2.3 | `rec:760` | the phase-2 target is the *last* `move_to` of `methods[0]` | `deliver_already_held` has one `move_to` | |
| 2.4 | `rec:777, 803` | a task with no `?item` binding targets its *first* `move_to` | `coffee_break`/`ac_activation` have one | `office_break` (dock_loading) would be scored against `office_door` forever |
| 2.5 | `rec:762-763, 779-780, 805-806` | the first `Const`-bound parameter of that step is the movement target, whatever its name | `move_to` has a single parameter `?target` | `movement_target_key` is ignored; `Var`-bound targets return `None` → NEUTRAL (TODO-46(2),(3)). Measured: 64/43/61/54 phase-2 calls and all 218 coffee_break calls in s10 returned NEUTRAL for this reason (`a_*.csv` `target_none_*`) |
| 2.6 | `rec:753-772` | one holdable parameter per task, named `?item`; "holding it" ⇔ "second phase"; exactly two phases | `deliver_item` | the only phase signal in the recognizer. Deleting the held-item logic deletes it |
| 2.7 | `rec:766-771` | the item's *current* container is where a phase-1 walker heads | true only until the item is delivered | TODO-37(a). Measured `phase1_table_delivered_decoy`: s00_off item_7 104 of 134 calls, item_3 60; s10 item_2 147, item_7 141; s20 item_3 64; s30 item_3 43 (`b_*.csv`). s00_off step 81 and 100: three hypotheses (item_3, item_6, item_7) all target the kitting table while the human walks to shelf_2 |
| 2.8 | `rec:564, 572` | a discrete vocabulary is a `list`; a continuous one is exactly the string `"STEP*"` | kitting/dock_loading declare `["GRASP"]`, `["RELEASE"]`, `["TOUCH"]`, `"STEP*"`, `"STAND*"` | `"STAND*"` is neither, so `wait_at` contributes nothing to dispatch and `stand` is never an event (`_discrete_microactions` = {GRASP, RELEASE} in every condition). `rec:271` also assumes a `list` means discrete |
| 2.9 | `rec:558, 272` | microaction strings compare case-insensitively via `.upper()` | obs_builder lower-cases, schemas upper-case | a convention, not a contract |
| 2.10 | `rec:400-406` | one observed agent: `_history`, `_leg_start_pos`, `_leg_base`, `_evidence` are not keyed by `obs.agent_id` | one human per scenario | a second observed agent would interleave legs (§7) |
| 2.11 | `rec:403-406` | a leg boundary is a displacement `< 1e-6` between consecutive observations, in world units | Mesa agents never drift | ROS positions would never be "stationary" |
| 2.12 | `rec:395-398, 402` | the first observation opens the leg at its own position | | the human's first step (20 cm) is never scored: tick 0 is classified `stationary` in every run (`prev_pos is None`) |
| 2.13 | `rec:729` | `obs.timestamp` is an integer step count and `LONG_SHIFT_THRESHOLD` is in those units | Mesa passes `schedule.steps` | 500 steps = 1000 s at `seconds_per_step: 2.0`; never reached in any run (max 300 steps) |
| 2.14 | `rec:485-487` | `holding` has arity 2, agent first | world_state_builder | |
| 2.15 | `lf:84-94` `direction_consistency_likelihood` | the observed chord of a τ-walker is collinear with the bearing to τ's target from the leg origin — i.e. paths are straight and the origin is where the walker started toward this target | Mesa `steps_toward()` is straight-line | this is the "assumes paths are straight without saying so" case: the correct hypothesis scored exactly 4.000 (cos = 1.000) on every one of its chords in all eight conditions (`h_*.csv`, `L_correct_min = L_correct_max = 4.000`). Neither the docstring nor `design_decisions.md` states the straight-line premise; a detour of any kind costs the true hypothesis credit that no other term restores |
| 2.16 | `rec:204` `build_hypothesis_space` | the hypothesis space is fixed at construction from the objects present in the layout | DESIGN-14 | a foreseeable task whose object type is absent from a layout has no hypothesis at all: s00/s20/s30 have no `coffee_break`/`ac_activation` hypothesis (5 hypotheses each) |
| 2.17 | `rec:246, 139-160`, `types.py:303-319` | hypothesis identity is the `repr` string, mirrored by hand in `task_instance_key` | | every cross-layer lookup (`_by_key`, admissible set, `get_hypothesis`, `[IR-dist]`) goes through the string |

---

## 3. Silent fallbacks

"Occurs" = measured in the eight runs (`a_*.csv`, `b_*.csv`). "Reachable" = code path exists,
never taken here.

| # | site | input that cannot be resolved | becomes | hides | occurs |
|---|---|---|---|---|---|
| 3.1 | `rec:611-613` | `_get_expected_position` → `None` (target is a `Var`) | NEUTRAL for that hypothesis | a hypothesis that *cannot be scored* is indistinguishable from one that *was scored and is uninformative*; the carried item's own hypothesis gets 1.0 for the whole carry | every carry leg, every condition (phase-2: s00 64, s10 43, s20 61, s30 54 calls); every `coffee_break` call in s10 (218) |
| 3.2 | `rec:766-772` | container is an agent id (item carried by the robot) → `object_positions.get("robot_0")` is `None` | falls through to the item's own position, which moves with the robot | "the item is in someone else's hands" becomes "the human is heading for a moving point" | prior-off only (inadmissible when on): s00_off 62 calls, s10_off 83, s20_off 49, s30_off 38 |
| 3.3 | `rec:795-798` | same container-is-agent case in `_get_target_zone` | `None` → no ZONE_BOOST | the correct hypothesis loses ×2 at the grasp (TODO-37(b)) | every grasp: each `item_X zone_SW` episode in `c_*.csv` ends the tick before the grasp |
| 3.4 | `rec:601-602` | `origin is None` | NEUTRAL | none in practice (`origin_none = 0`, all conditions) | never |
| 3.5 | `rec:604-606` | `progress_evaluator` name not in the registry | NEUTRAL, no warning | a typo in a schema silently disables movement evidence for that action | never |
| 3.6 | `rec:575` | no schema answers | NEUTRAL | a task whose first action is discrete and whose vocabulary does not match | never |
| 3.7 | `rec:566-567` | completion predicate unresolvable | NEUTRAL | unbound `Var` (e.g. `?pallet` in dock_loading's `confirm_delivered_pallet`, which has no `parameter_types`) | never reached (2.1) |
| 3.8 | `rec:204` | `known_objects_by_type.get(type, [])` | the task has zero hypotheses | a foreseeable task vanishes from the space when the layout lacks its object | s00, s20, s30 |
| 3.9 | `rec:449` | `prior.get(key, default)` with `default = _initial_prior.get(key, 1/(n+1))` | a fresh uniform weight | a key missing from the evidence state | never (`_evidence` always spans the space) |
| 3.10 | `rec:502` | `sum(unnorm) == 0` | `or 1.0` — normalizes by 1 | an all-zero posterior would pass through the floor and renormalize to uniform | never |
| 3.11 | `rec:466` | `_by_key.get(key)` is `None` | ω = 1.0 | only `unknown` today | every tick (by design) |
| 3.12 | `rec:712-713` | `_get_target_zone` → `None` | no boost, silently | 3.3, and any hypothesis whose target is `Var`-bound (coffee_break never had a zone) | every carry |
| 3.13 | `rec:406` (with `obs_builder.py:94-98`) | executor's action-advance tick has `current_microaction = None` | obs `"stand"`, zero displacement → `stationary` → leg closed | the leg is closed by a *synthetic* observation, not by the grasp/release event. Measured: all 32 legs in `e_*.csv` are closed by `stand`, none by a discrete event; the discrete tick then arrives with the leg already closed and rebased | every leg |
| 3.14 | `rec:426-427` | `most_likely = max(distribution)` | insertion-order tie-break | TODO-42; at t=0 prior-off the winner is the first layout item (s00 item_3, s10 item_1 — boosted by zone at t=0, s20 item_4, s30 item_3) | t=0, every prior-off run |

---

## 4. Duplicated or partial resolution

| # | IR site | re-implements | where the generic version lives | how the IR version is weaker |
|---|---|---|---|---|
| 4.1 | `rec:662-694` `_resolve_term_value` | Var → value grounding | `pl:258-282` `_resolve_step_bindings` + `pl:307-330` `_ground_predicate` | reads `methods[0]` only; resolves a step-call `Const` but not a step-call `Var` chained through task bindings; no derived vars; no `?agent` injection point other than the literal. Never called in any run (`resolve_term_value_calls = 0`) |
| 4.2 | `rec:757-764, 775-781` `_get_expected_position` | movement-target resolution | `projection.py:256-257` (`action.bindings.get(schema.movement_target_key)` → `world.object_positions`) and `action_decomposer.py:190-213`, both over planner-grounded actions | ignores `movement_target_key`; matches action *name*; takes the first `Const`; cannot see a `Var` target. `Projector.build_segments` resolves `kitting_table_0` and `coffee_machine_0` for the same hypotheses every trigger (T1 built 24 human projections from exactly these bindings) |
| 4.3 | `rec:753-772` | "where the item is now" | `world.object_locations` (same map) vs `world.object_home_container` used by `pl:243` `home_container_of` | the IR reads the *current* location (→ table after delivery, agent id while carried); the planner's derived var reads the *home* container. Two different answers to "the item's container" |
| 4.4 | `rec:482-490` `_refuted_by_holding`, `rec:755` | "what is the human holding" | `world.agent_states[agent].holding` (`types.py:78`), and `obs.action_context.target_object` (`obs_builder.py:107`, set to `human.carrying`) | three carriers of the same fact; the IR scans `world.predicates` for a `holding` literal |
| 4.5 | `rec:712-717` | "is the human in zone Z" | `obs.spatial_context.zone` (`obs_builder.py:81-87`) carries the same zone | the IR rebuilds an `in_zone` predicate and tests set membership instead of reading the observation it was given |
| 4.6 | `rec:795-798, 806` `_get_target_zone` | zone of an object | `pl:241-242` `zone_of` derived var, same `world.object_zones` map | no phase-2 branch (TODO-37(b)) |
| 4.7 | `rec:139-160` `HypothesisKey.__repr__` | task-instance identity | `types.py:303-319` `task_instance_key` | two hand-written string builders kept equal by convention (TODO-26) |
| 4.8 | `rec:266-273` `_discrete_microactions` | "which microactions are events" | `DomainModel.get_actions_for_microaction` (`types.py:428-436`), exposed as `DomainKnowledgeBase.get_actions_for_microaction` (`domain_knowledge.py:108-113`) | the knowledge-base reverse lookups `get_tasks_for_action` / `get_actions_for_microaction` are documented as "used by recognizer" (`domain_knowledge.py:25, 98-113`, `io_contracts.md:643-644`) and are called by nothing in the repository |
| 4.9 | `rec:558, 564` | vocabulary membership per schema | `types.py:432` does the same test | duplicated, consistent |

---

## 5. Constants the belief depends on

"P" = a probabilistic quantity (has a likelihood/probability meaning); "K" = a tuning knob.
Condemned constants are listed with where they fire only.

| # | constant | site | meaning | P/K | fires / read at |
|---|---|---|---|---|---|
| 5.1 | `HIGH_LIKELIHOOD = 4.0` | `lf:31`; read `lf:54, 90, 94` | top of the linear kernel; also "completion holds"; also "already at target" | K posing as P (an unnormalised density ratio against NEUTRAL = 1) | condemned. Measured: the correct hypothesis's chord is *exactly* 4.000 on every moving tick of every run (2.15); 186/96/124/124/111/81/97/77 calls hit exactly 4.0 per condition; the `target_norm < 1e-6` "already at target" branch (`lf:89-90`) fired 0 times |
| 5.2 | `LOW_LIKELIHOOD = 0.1` | `lf:32`; read `lf:54, 94` | bottom of the kernel; "completion absent" | K | condemned; the completion branch never fired, so 0.1 was only ever the kernel floor (min observed 0.124 in s30_off, 0.140 in s10) |
| 5.3 | `NEUTRAL_LIKELIHOOD = 1.0` | `lf:33`; read `rec:452, 567, 575, 602, 606, 613`, `lf:85` | `unknown`'s likelihood; every fallback | P by intent (uniform-heading density), but the kernel's mean over a uniform heading is 2.05, so `unknown` is handicapped ~2× against a random walker (design_decisions, TODO-38). Measured mean chord of *wrong* hypotheses: 2.3–3.1 per condition (`h_*.csv`) — every wrong hypothesis outscores `unknown` on average | condemned |
| 5.4 | `ZONE_BOOST = 2.0` | `rec:109`; fires `rec:717` | ω ×2 when the human is in the zone of the hypothesis's phase-1 container / first-move_to target | K | being removed. 52 episodes in `c_*.csv`; 72/36/414/244/64/28/223/158 (tick × hyp) pairs per condition. Fires at t=0 in s10 (human starts in zone_SW with shelves 1, 2, 6: three hypotheses ×2 before any observation, which decides the t=0 `most_likely`); fires for the *wrong* hypothesis in 28 of 52 episodes; the longest episode is s10_off item_6 (steps 107–208, the coffee walk, the wait, and the walk to shelf_4); in s30 (both settings) it fires for item_3 from step 74 to the end of the run (delivered item at the table, human standing at or near the table). The measured s20_on θ crossing at step 11 and s30_on's 0.471 → 0.640 are zone-state events, so both move when it is removed |
| 5.5 | `TEMPERATURE_BOOST = 3.0`, `HIGH_TEMP_THRESHOLD = 26.0` | `rec:110, 118`; `rec:720-723` | | K | condemned. Never fired (context temperature is the 21.0 default, `domain_knowledge.py:134`; no scenario sets it) |
| 5.6 | `FATIGUE_BOOST = 2.5`, `LONG_SHIFT_THRESHOLD = 500` | `rec:111, 119`; `rec:726-730` | | K, and 500 is in simulator steps (2.13) | condemned. Never fired (max 300 steps) |
| 5.7 | `BELIEF_FLOOR = 1e-3` | `rec:125`; read `rec:346, 348, 506` | minimum mass per hypothesis; also the *pinned* value | K. Stays. Two roles: a clamp on live keys (`rec:506`) and the fixed mass of every pinned key (`rec:348`). Applied twice per tick (evidence `_finalize` and output `_finalize`) | live-key clamps: 0 in seven conditions, 54 in s10_off (item_7, output only). Pinned mass: 3–4 × 1e-3 per tick with the prior on, 4–7 more per tick during a refutation. The 0.797 grasp figure is 0.8 − pinned mass |
| 5.8 | `CONFIDENCE_THRESHOLD = 0.75` | `rec:121` | — | dead: read by nothing (`grep`), duplicates `MetaPlanner.theta` (`meta_planner.py:139`) | never |
| 5.9 | uniform prior `1/(n+1)` | `rec:288-290`, admissible `1/|A|` `rec:295-298` | t=0 belief | P | t=0 confidence 0.167 (5+1 keys), 0.111 (9+1), 0.332 (3 admissible incl. unknown in s00/s20/s30 prior-on), 0.249 (s10_on, 6 admissible but zone boost at t=0) |
| 5.10 | `1e-6` | `rec:404`, `lf:84, 89` | "not moving" / "at target", in world units (cm) | K with an implicit unit | leg boundaries; never the target-norm branch |
| 5.11 | kernel shape `LOW + (cos+1)/2 · (HIGH−LOW)` | `lf:94` | linear in cosine | K | being replaced by the excess-path-cost likelihood |
| 5.12 | `PROXIMITY_THRESHOLD = 30.0` | `world_state_builder.py:64` | radius of `at(agent, obj)` | K, embodiment-side | not read by the IR today; it will decide when `move_to`'s completion condition holds for a phase tracker (§8): measured `at(human, item)` becomes true on the last tick of every approach leg and stays true for 4 ticks (`f_*.csv`) |
| 5.13 | `step_size = 20` | `mesa_configs.yaml` | motion per tick | embodiment | sets chord length; irrelevant to the cosine, load-bearing for the excess-path likelihood |
| 5.14 | `ContextKnowledge` defaults 21.0 / 0 | `domain_knowledge.py:133-134` | | K | condemned branches only |
| 5.15 | `theta = 0.75` | `meta_planner.py:139` | consumer-side gate | K | not read by the IR; listed because every "reveal" figure quoted in the docs is measured against it |

---

## 6. Evidence paths actually exercised

Measured from outside on all eight conditions (`a_evidence_paths.csv`; episodes in `c_*`, `d_*`,
`j_*`). "Pairs" = (tick × hypothesis).

| evidence path | reachable? | fired (pairs per condition: s00 off/on, s10 off/on, s20 off/on, s30 off/on) | notes |
|---|---|---|---|
| directional chord, target resolved (`rec:615`) | yes | 588/198, 1679/819, 491/161, 493/166 | the only evidence the recognizer has ever produced. Phase-1 shelf targets and the delivered-item / robot-carried decoys (2.7, 3.2) are all in this count |
| directional, zero-length chord → NEUTRAL (`lf:85`) | yes | 18/6, 22/10, 18/6, 18/6 | every discrete tick: `origin = prev_pos`, displacement 0, so every hypothesis whose target resolves gets exactly 1.0 from the event |
| directional, target unresolvable → NEUTRAL (`rec:613`) | yes | 64/64, 261/261, 61/61, 54/54 | phase-2 carries (all) + `coffee_break` (s10 only). Identical off/on because the affected hypotheses are admissible in both |
| completion predicate — `pick_up` (`holding`) | **no** | 0 in all | unreachable by construction (2.1): `GRASP` is not in `methods[0]`'s vocabulary |
| completion predicate — `place` (`obj_at`) | **no** | 0 in all | in `methods[0]`'s vocabulary, but `move_to` returns first (2.2) |
| completion predicate — `move_to` (`at`) | **no** | 0 in all | `move_to` has no list vocabulary, so `_likelihood` never routes it to the completion check; it can only take the progress branch |
| completion — `wait_at` (ProcessCompletion) | no | 0 | `rec:648` would return `None` → NEUTRAL; never reached |
| `_resolve_term_value` (any term) | no | 0 calls | |
| held-item refutation (`rec:471-496`) | yes | 68/68, 45/45, 65/65, 58/58 ticks; 4 keys (s00/20/30) or 7 keys (s10) per tick | 16 episodes. Each starts at a grasp and ends at the release. Of the 14 episodes with a tick after the release, the post-release `most_likely` is an unrelated item in 5 (all prior-off: s00 ×2, s10 step 75, s20 ×2 — the robot-item or delivered-item decoys of §2.7/§3.2), the item just delivered in 5, and the human's next task in 4; confidence after release 0.28–0.76. Being deleted; §7 lists what depends on it |
| ZONE_BOOST | yes | 72/36, 414/244, 64/28, 223/158 | §5.4. Fires on output only; never in the evidence state |
| TEMPERATURE / FATIGUE | reachable | 0 / 0 | never |
| admissibility mask | yes (prior on) | 3/4/3/3 keys pinned on every tick | mask, stays. Its only measured effect on *evidence* is the smaller normalisation set (t=0 0.332 vs 0.167) and the removal of the robot-item decoys (3.2 vanishes prior-on) |
| floor clamp on a live key | yes | 0/0, 54/0, 0/0, 0/0 | s10_off only, item_7 on output |
| `fallthrough` NEUTRAL (`rec:575`) | reachable | 0 | |
| `at target` HIGH (`lf:90`) | reachable | 0 | |

Two consequences the tables make explicit:

- **Every discrete event contributes exactly 1.0 to every hypothesis** (`j_discrete_ticks.csv`: at
  all 30 event ticks the likelihood multiset is `{1.0: n}`). The event's whole effect is
  `_leg_base ← _evidence` and `_leg_start_pos ← current_pos` (`rec:409-410`) — and by then the leg
  has already been closed one tick earlier by the synthetic `stand` (3.13). The "grasp reveal"
  (0.308 → 0.797 in s00_off at step 41) is the refutation pin applied on output, as
  `design_decisions.md` already says; the audit adds that the event branch itself has never
  changed the evidence state in any run.
- **Prior on vs off changes nothing on the evidence paths** except the set of hypotheses scored:
  the counts for unresolvable targets, discrete ticks and refutation ticks are identical across
  the pair in every scenario.

---

## 7. Per-hypothesis and cross-tick state

Everything the recognizer keeps between `update()` calls, at `89b998d`:

| # | attribute | site | keyed by | reset | note |
|---|---|---|---|---|---|
| 7.1 | `_history: List[Observation]` | `rec:242, 395` | nothing (one observed agent) | never; grows one entry per tick | read only for `_history[-2].position` (`rec:402`) |
| 7.2 | `_evidence: Dict[str, float]` | `rec:280, 305, 409, 412` | hypothesis repr | never | the belief with no ω and no refutation; carries inadmissible keys at `BELIEF_FLOOR` permanently |
| 7.3 | `_leg_base: Dict[str, float]` | `rec:281, 306, 410, 414` | hypothesis repr | at every discrete or stationary tick (`_leg_base ← _evidence`) | one dict for all hypotheses |
| 7.4 | `_leg_start_pos` | `rec:282, 397-398, 410, 414` | nothing — **one global origin** | same ticks as 7.3 | passed as the same `origin` to every `_likelihood` call (`rec:450`) |
| 7.5 | `_admissible`, `_inadmissible`, `_initial_prior` | `rec:284-304` | hypothesis repr | never (construction only) | static |
| 7.6 | `_by_key`, `_hypotheses`, `_discrete_microactions` | `rec:240, 246, 266` | | static | hypothesis space fixed (DESIGN-14) |
| 7.7 | `context: ContextKnowledge` | `rec:239` | | static | |
| 7.8 | `prev_belief` parameter | `rec:367, 383-392` | | accepted, not read | contract compatibility only (io_contracts §2.1) |
| 7.9 | `MetaPlanner._prev_belief` | `meta_planner.py:196, 264` | | per tick | consumer-side; θ crossings are measured against it |
| 7.10 | the implicit phase: `holding(agent, ?item)` in the world | `rec:755`, `rec:471-496` | per hypothesis, but derived from the world each tick, not stored | n/a | the only per-hypothesis "which action are we on" the recognizer has. It is a *world* fact, so it is the same for every hypothesis bound to the held item and absent for every other |
| 7.11 | `RobotAgent.belief / prev_belief` | `sim_agents.py:237-238, 263-268` | | per tick | body-side copies |
| 7.12 | update cadence | `sim_agents.py:250-268` | | | the IR is not called once the robot is `finished` (s00 stops at 169/300, s30 at 168/200) and keeps being called after the human is finished (s20: 76 ticks, s30: 45, s00: 25). No signal in either direction reaches the recognizer |

What would conflict with a per-hypothesis phase index, origin and odometer:

| # | conflict | where |
|---|---|---|
| C1 | **One origin for all hypotheses.** `_weigh` (`rec:450`) hands the same `origin` to every hypothesis; `_progress_likelihood` builds `move_vec` from it (`rec:608-609`); the rebase rule (`rec:409-414`) replaces the *entire* `_evidence` dict with `_leg_base` at once. A per-hypothesis origin means per-hypothesis rebase, i.e. `_leg_base` and `_leg_start_pos` become per-key, and the "replace, do not multiply" rule has to be restated per key | `rec:280-282, 400-414, 431-454, 577-617` |
| C2 | **Leg boundaries are global and come from the body's synthetic `stand`** (3.13), not from any hypothesis's completion condition. In Mesa the two coincide (every leg in `e_legs.csv` spans exactly one human action and is closed on the action-advance tick), so today's data cannot show the difference between "leg closed" and "phase advanced" — the restructure will be the first thing that can |
| C3 | **The held-item logic is the phase.** Deleting `_refuted_by_holding` and the `rec:755` branch removes (a) the choice between shelf and table as target, (b) the ×10 "grasp reveal" that produces every θ crossing at a grasp (10 of 15 `theta_up` events in `g_*.csv` are grasp ticks), and (c) the only mechanism that ever *lowered* a wrong hypothesis to the floor. A phase index takes over (a) by construction; (b) and (c) become whatever the action-level likelihood says at a `GRASP` observation — which today is 1.0 for everyone (§6) |
| C4 | **`_pin` assumes pinned ∩ live = ∅ and that `_evidence` spans the full space** (`rec:345-361, 498-515`). Inadmissible keys are *skipped* in `_weigh` (`rec:447-448`) but still present in `_evidence` at the floor. A completed task pinned at `BELIEF_FLOOR` needs the same treatment or it keeps accumulating evidence (it is not in `_inadmissible`). Decision surfaced: does "completed" join the skip set in `_weigh`, or only the pin set in `_output`? Both readings are consistent with "pinned, never removed"; the evidence that settles it is whether a completed task may become live again (the human re-doing it) |
| C5 | **No completion event exists today.** Nothing tells the recognizer a task ended; `_evidence` for a delivered item decays only through the decoy geometry of 2.7. A phase index that reaches "past the last action" is the first such signal, and the meta-planner's `no_current_task` / `task_committed` triggers (`meta_planner.py:233-256`) are robot-side, not human-side |
| C6 | **`_history` is unbounded and single-agent.** An odometer needs the previous position per hypothesis leg, which `_history[-2]` gives only globally |
| C7 | **The output-only factors are re-derived every tick from the world** (ω, refutation). With ω removed and the refutation deleted, `_output` reduces to `_evidence` plus pins — but `_finalize` still runs twice per tick (evidence and output), each applying the floor; whether the double floor is kept is a decision, not a fact |

---

## 8. Completion conditions declared but never evaluated

Reachability is asked of the *recognizer* (the executor evaluates every ConditionSchema for the
agent executing it — `executor.py:146-162`). Groundability from hypothesis bindings and
tick-level truth were measured externally (`f2_*.csv`, `f_*.csv`).

| domain | action | completion | type | vocabulary | reachable by the IR? | why not | groundable from hyp bindings | measured (human's live plan) |
|---|---|---|---|---|---|---|---|---|
| kitting | `move_to` | `at(?agent, ?target)` | ConditionSchema | `"STEP*"` | no | `_likelihood` routes STEP* to the progress branch only (`rec:572`); the completion check is inside the list-vocabulary branch (`rec:564`) | yes for `deliver_default`, `deliver_already_held`, `coffee_break`; **no** for `deliver_with_return` steps 0–1 (`?other_container` is a derived var) | `at(human, item)` becomes true on the tick the approach ends and holds for 4 ticks (until the grasp suppresses it); `at(human, kitting_table_0)` likewise. Note `at(human, item_X)` also holds whenever the human stands at the table and item_X has been delivered there (s00 step 142: `at(human_0, item_2/3/6/7)` all true) |
| kitting | `pick_up` | `holding(?agent, ?item)` | ConditionSchema | `["GRASP"]` | no | not in `methods[0]` (2.1) | yes | true from the grasp tick until the release (31–44 ticks) |
| kitting | `place` | `obj_at(?item, ?target)` | ConditionSchema | `["RELEASE"]` | no | `move_to` returns first (2.2) | yes | true from the release tick onward for the rest of the run |
| kitting | `wait_at` | — | ProcessCompletion | `"STAND*"` | no | `rec:648` returns `None`; never reached anyway | n/a | `wait_at` (coffee) executes steps 128–158 in s10 with nothing observable except `stand` |
| dock_loading | `scan_it` | `scanned(?item)` | ConditionSchema | `["TOUCH"]` | no | `confirm_delivered_pallet.methods[0]` = [`move_to`, `scan_it`]; `move_to` returns first. Also the task has no `parameter_types`, so its single hypothesis has empty bindings and `?item`/`?pallet` is unbound (TODO-25) | no | not run |
| dock_loading | `move_to`, `pick_up`, `place`, `wait_at` | as kitting | | | no | same as kitting; `deliver_pallet`/`load_return` step 0 is `move_to(Const dock_gate)`, so their chord target is always the gate | mostly yes | not run |

Task-level (`f2_*.csv`, 16 (task, method, step) sites in kitting): 14 groundable from hypothesis
bindings plus `?agent`, 2 not (`deliver_with_return` steps 0 and 1, derived var). Every
groundable predicate was observed true at some tick of the human's actual task; the grounded
predicates of *other* hypotheses were also true at many ticks (e.g. `obj_at(item_7,
kitting_table_0)` holds for 335 tick-hypothesis pairs in s00 because the robot delivered it) —
a phase tracker keyed on world predicates alone will see "completed" for tasks the observed
human never did. Surfaced, not judged.

---

## 9. Method selection sites

| # | site | selects | checks guards? | notes |
|---|---|---|---|---|
| 9.1 | `pl:130-151` `AdaptivePlanner._select_method` | first method whose guards hold | yes, via `_guards_satisfied` | raises if none applies (every kitting task has an unguarded last method; dock_loading `office_break` does not) |
| 9.2 | `pl:153-225` `_guards_satisfied` | — | fully-bound membership test; existential binding of one free `Var` per guard (sorted tie-break); built-in `not_equal` | takes `bindings: Dict[str, str]` including `?agent` and returns the extended bindings |
| 9.3 | `rec:626` `_get_relevant_action_schemas` | `methods[0]` | no | |
| 9.4 | `rec:687-688` `_resolve_term_value` | `methods[0]` | no | |
| 9.5 | `rec:760, 777, 803` `_get_expected_position` / `_get_target_zone` | `methods[0]` | no | |
| 9.6 | `rec:269` `_discrete_microactions` | all methods (union) | no | correct for its purpose (vocabulary), documented as such |
| (9.7) | `types.py:418-426` `get_tasks_for_action` | all methods | no | unused |
| (9.8) | `projection.py:140` and `sim_agents.py:156, 333` | via 9.1 | yes | the same planner selects the *human's* method for the human projection every trigger (`projection.py:196-206`) |

Is `_guards_satisfied` reusable as-is by the recognizer? Mechanically yes: its inputs are a
`MethodSchema`, a `Dict[str, str]` of bindings, and a `WorldState`; a hypothesis supplies
`{"?agent": obs.agent_id, **hyp.bindings}`. Three things to surface, not decide:

- it is a private method of `AdaptivePlanner`; the recognizer would either hold a planner or the
  function would move (the projector already holds its own planner for exactly this reason,
  `projection.py:88`);
- guards are evaluated against the *current* world. For the human holding item_2, `deliver_item(item_4)`
  selects `deliver_with_return` (6 steps, `?other = item_2`) and `deliver_item(item_2)` selects
  `deliver_already_held` (2 steps). Whether a hypothesis's method is chosen once (at phase 0) or
  re-chosen every tick — "the world is the cursor", `design_decisions.md` — changes what "phase k"
  means when the held item changes. Both readings are consistent with the design note;
  `deliver_with_return`'s derived var (`?other_container`, `pl:227-256`) only resolves under the
  per-tick reading;
- `not_equal` is a built-in evaluator by name (`pl:172`), and `zone_of` / `home_container_of` are
  too (`pl:241-243`); a recognizer reusing the function inherits those three names.

---

## 10. Doc/code drift (recognizer-related)

| # | document | says | code |
|---|---|---|---|
| 10.1 | `design_decisions.md:188-190` (typed-parameter entry) | "`shared/` no longer hardcodes `?item` as a string" | `rec:493, 495, 753, 793` read `"?item"` (known instance) |
| 10.2 | `design_decisions.md:147-159` "IR likelihood dispatch" | `completion` "checked for discrete actions like pick_up/place" | never reached in any run (§6) |
| 10.3 | `TODOS_AND_DEFERRED.md:190-206` TODO-19 ✅ | "release/touch microactions now also receive completion-predicate checks (previously always NEUTRAL) — generalized for free" | release ticks return 1.0 for every hypothesis (`j_*.csv`); the check is unreachable (2.2) |
| 10.4 | `TODOS_AND_DEFERRED.md:834-836` TODO-37(c) | "FIXED — `_likelihood()` now returns LOW_LIKELIHOOD for any hypothesis whose `?item` differs from the observed held item, before microaction dispatch" | the refutation is a pin on output (`rec:471-496, 456-469`); `_likelihood` no longer looks at holding (`rec:552-556` says so). The later "One leg is one observation" entry describes the current form; TODO-37(c) was not updated |
| 10.5 | `TODOS_AND_DEFERRED.md:208-220` TODO-20 | the recognizer "re-derives which action schema applies fresh every step by scanning the task tree" | it reads `methods[0]` and returns from the first schema; no tree is scanned |
| 10.6 | `rec:12-13` module docstring | "microaction is 'grasp': if observed agent is now holding τ's target item → HIGH, else → LOW" | never happens; grasp yields 1.0 for all (§6) |
| 10.7 | `rec:14-17` docstring | movement is scored against "the vector from that leg start toward τ's target object" | true only when the target resolves; for phase-2 and `coffee_break` there is no vector and the value is NEUTRAL (§3.1) |
| 10.8 | `design_decisions.md:143-145` | positions are "only consumed by `direction_consistency_likelihood` and target-resolution helpers in recognizer.py — never by planner.py or executor.py" | `projection.py:235, 257` (shared) and `meta_planner` via the projector read `agent_positions` / `object_positions`; the statement predates the projector |
| 10.9 | `io_contracts.md:350-353` §2.1 | "`None` or `[]` switches the persistent assignment **prior** off entirely and `update()` runs its original **unweighted** path" | it is a support mask (TODO-44); the wording was not updated when the weight became a mask |
| 10.10 | `io_contracts.md:732` validation rule 7 | "All intention names in `BeliefState.distribution` are registered in `DomainModel.intentions`" | `unknown` is in every distribution and in no domain's `intentions` |
| 10.11 | `io_contracts.md:643-644`, `domain_knowledge.py:25, 98-113` | `get_tasks_for_action` / `get_actions_for_microaction` are "reverse lookup for IR" / "USED BY shared/recognizer.py" | called by nothing (4.8) |
| 10.12 | `design_decisions.md:711-713` "One leg is one observation" | "A discrete observation … is an EVENT: it multiplies onto the evidence state and closes the current movement leg" | it multiplies 1.0 onto every key (§6) and the leg is already closed by the preceding `stand` (3.13). The sentence is true of the code path and false of its effect |
| 10.13 | `TODOS_AND_DEFERRED.md:998-1021` TODO-46 | "`_get_expected_position()` returns `None` … whenever the target binding it inspects is a `Var`" | correct; the audit adds the measured counts (§3.1) and that `RELEASE` is also blocked by 2.2, which TODO-46 does not list |
| 10.14 | `rec:262-265` comment | "Every method is consulted, not only methods[0] as `_likelihood()`'s dispatch does" | accurate — listed because it is the only place the code itself records the `methods[0]` restriction |

Not drift, but unstated in any doc: the straight-line premise of the chord kernel (2.15), the
synthetic-`stand` leg closure (3.13), and the update cadence tied to the robot's `finished` flag
(7.12).

---

## Findings outside the IR (listed, not analysed)

| # | where | finding |
|---|---|---|
| O1 | `shared/meta_planner.py:542` via `sim_agents.py:309` | s10 (both prior settings) raises `RuntimeError: no feasible candidate` at step 257: every candidate excluded with `min_dist=0.0` after the human's grasp of item_4 at the moment the robot's `theta_crossed` fires. Present in the unmodified baseline; the run stops there. Post-T2 units (`min_safe_distance = 1.0` in cm) may be the reason; not investigated |
| O2 | `mesa_sim/sim_agents.py:250` | the IR stops being called when the robot is `finished` (s00 at 169 of 300 steps, s30 at 168 of 200). In these runs the human had already finished (s00 step 144, s30 step 123), so nothing was lost; a human acting after the robot's last task would be unobserved |
| O3 | `mesa_sim/obs_builder.py:94-98` | `current_microaction = None` → `"stand"`: a synthetic observation the recognizer cannot tell from an actual stand |
| O4 | `mesa_sim/world_state_builder.py:223` | `obj.type == "obstacle"` literal (TODO-24) |
| O5 | `mesa_sim/action_decomposer.py:170, 176, 151` | `"?item"`, `"?duration"` literals in the expansion (TODO-01) |
| O6 | `mesa_sim/sim_model.py:303` | `get_movable_objects` filters on `type == "item"`; unused by the run path |
| O7 | `shared/recognizer.py:93` | stray `from importlib.metadata import distribution`, shadowed by the local `distribution` in `update()`; harmless |
| O8 | `shared/recognizer.py:121` | `CONFIDENCE_THRESHOLD` unused (5.8) |
| O9 | `domains/dock_loading/tasks.py:153-175` | `confirm_delivered_pallet` has no `parameter_types` → one hypothesis with empty bindings (TODO-25); `office_break` guard has no fallback method → `_select_method` would raise for it |
| O10 | `mesa_sim/world_state_builder.py:222-228` | a delivered item keeps producing `at(human, item)` at the table (8, note) — a body-side fact a phase tracker will read |

---

## Most consequential for the phase restructure

1. **There is no event evidence to build on, only movement evidence.** Every discrete tick has
   contributed exactly 1.0 to every hypothesis in every run (§6, `j_*.csv`); `_resolve_term_value`
   has never executed. The action-level likelihood for `GRASP`/`RELEASE` will be the first time
   completion predicates are evaluated inside the recognizer, and the first time the leg/rebase
   rule interacts with a non-trivial event likelihood (C3).
2. **The leg is global and closed by the body, not by any hypothesis** (C1, C2, 3.13). Per-hypothesis
   origin and odometer cannot be bolted onto `_leg_base`/`_leg_start_pos`; the rebase rule has to be
   restated per key. Mesa data cannot distinguish the two designs today because every leg coincides
   with one human action (`e_legs.csv`).
3. **Deleting the held-item logic deletes the phase** (C3, 2.6). Everything that today chooses the
   table over the shelf, and every grasp-tick θ crossing, is that logic.
4. **Completion predicates are groundable from hypothesis bindings for 14 of 16 kitting sites** but
   *not* for `deliver_with_return`'s first two steps (derived var), and the method a hypothesis is on
   depends on the world at selection time (§9). Whether method selection is frozen at phase 0 or
   re-run per tick is an open decision with different phase semantics.
5. **World predicates say "completed" for tasks the human never did** (§8 note, O10):
   `obj_at(item_7, kitting_table_0)` and `at(human_0, item_7)` are both true while the human stands
   at the table after the robot delivered item_7. A phase tracker advancing on world truth alone
   will advance decoy hypotheses; pinning completed tasks at the floor (C4) needs a definition of
   "completed by the observed agent" that the world state does not carry.
6. **The kernel scores the correct hypothesis at exactly HIGH because Mesa walks straight lines**
   (2.15). Every quoted confidence in the docs is conditional on that; the excess-path-cost
   likelihood makes the premise explicit and will change every number.
7. **ZONE_BOOST removal will move**: s20_on's step-11 crossing (→ the grasp at 22, as prior-off),
   s30_on's 0.640 at step 23 (→ 0.471 until the grasp), s10's t=0 `most_likely` (item_1 → layout
   order), and the 0.797 grasp figure only through the floor (unchanged). The 28 wrong-hypothesis
   episodes in `c_*.csv` disappear.

---

## Verification

1. **Baselines regenerated at HEAD `89b998d`** before any analysis code existed, with
   `PYTHONHASHSEED=0`. All eight are byte-identical on `[meta]`, `[IR]`, `[IR-dist]` and the whole
   file to the eight logs already in `logs/run_20260913_0203{46,49,52,56,59}.log` and
   `run_20260913_0204{02,05,08}.log`.
2. **Instrumentation changes nothing.** The eight logs written by `measure.py` are byte-identical
   to those baselines (`cmp`; md5 s00_off 4572841d, s00_on a7e04591, s10_off 28975be5,
   s10_on e8ab22c0, s20_off d19a96c1, s20_on 7acaf0c8, s30_off 1b3c32a4, s30_on 4be200fa). Every
   wrapper calls the original and returns its result unchanged; the external completion
   evaluation reads `world.predicates` only.
3. **Doc figures reproduced** (`g_belief_events.csv`, `i_ticks.csv`): 0.797 at every grasp;
   s20_on step 11 = 0.780; s30_on step 22 = 0.471, step 23 = 0.640; s10_on step 107 = 0.853 on
   item_6; s10 step 257 = 0.769.
4. **s10 crash reproduced** at step 257 in both the baseline (`stderr`) and the instrumented run.

## Not measured

- dock_loading (not run; §8 by reading only).
- Any per-hypothesis phase or odometer (does not exist yet; §7 is a state inventory).
- The sensitivity of any belief figure to the condemned constants (they are being removed, not tuned).
- ROS side.
