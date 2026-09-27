# The IR test-bed (TB.3b)

The recognizer tested in isolation, on a layout, a setup and scenarios written for it, against expectations derived
from the recognizer records before the run (design_decisions.md, "The IR test-bed"; glossary §8, TB). This file is
the instrument: what it runs, what it derives, from which record, and how it compares. The results are in
`REPORT.md`. Built at the commit that adds this file (27 September 2026).

Standing rule: the records' mechanism stands over runs, baselines and tests. An expectation changes only by
derivation from the records. A disagreement is reported, not fitted.

## The artefacts

Hand-written literals in `domains/kitting/`, registered by discovery; prior ON in every run.

- `layouts/env_layout_10.json`: a square room, 1000 × 1000 cm (env_layout_01's width; 01 is 1000 × 800, not
  square), centred origin, y up. The proportions are from Hadi's sketch (W, H the room's width and height, y from the
  top); sizes are as in env_layout_01, and the coffee machine is 50 × 50 as in env_layout_05 and _07.

  | object | proportion | position (cm) |
  |---|---|---|
  | kitting_table_0 | (0.50 W, 0.08 H) | (0, 420) |
  | shelf_1 (west) | (0.08 W, 0.52 H) | (−420, −20) |
  | shelf_2 (east) | (0.92 W, 0.52 H) | (420, −20) |
  | coffee_machine_0 | (0.33 W, 0.90 H) | (−170, −400) |
  | corner_SE (the one landmark) | 50 cm in from both walls | (450, −450) |

  There is no door, no AC switch and no obstacle. Stated consequences: the two shelves are at equal path cost from
  the table (608.3 cm); the coffee machine's bearing from the table (−101.7°) differs from corner_SE's (−62.7°); no
  `ac_activation` hypothesis exists in this room.
- `setups/env_setup_08.json`: item_1 on shelf_1 and item_2 on shelf_2, both designated to kitting_table_0.
- `scenarios/scenarios_s08.py`: the robot at (−400, 400), i.e. (0.10 W, 0.10 H), with an empty task pool, observing
  human_0. The human starts at the table (0, 420), is assigned `deliver_item(item_1)` and `deliver_item(item_2)`, and
  every script ends with the exit walk `go_to(corner_SE)`. The human is listed first, so within a tick the human acts
  before the robot observes.
  - `scenario_s08_01`: deliver item_1, deliver item_2, exit.
  - `scenario_s08_02`: deliver item_1, `coffee_break(coffee_machine_0)`, deliver item_2, exit.
  - `scenario_s08_03`: `deliver_item(item_1).at(pick_up, coffee_break(...))`, deliver item_2, exit.
  - `scenario_s08_04`: `deliver_item(item_1).at(move_to, coffee_break(...), occurrence=0)`, deliver item_2, exit.

  The coffee break's duration is the schema's (PT60S, 30 ticks).
- `configs/ir_testbed/scenario_s08_0N.yaml`: one run file per scenario. Each sets layout env_layout_10, the prior on,
  single_task, gate none, cost realized, separation_stop off and test_level 0.05. Its steps are the replay's last
  acknowledgement tick + 1 + 30 ticks of the idle human, where 30 covers E5's standing threshold at α = 0.01
  (25 ticks). That gives 204, 281, 271 and 282 steps (last acknowledgements 173, 250, 240, 251). Every run is under
  500 steps, so the `coffee_break` context weight stays inert (handback §2).

To run one scenario by hand:

```bash
PYTHONHASHSEED=0 python mesa_sim/run_mesa.py --run configs/ir_testbed/scenario_s08_01.yaml   # _02, _03, _04 likewise
```

To run the whole instrument (the runs, trajectories, expectations, actual outputs, comparisons and figures) from the
repo root:

```bash
analysis/ir_testbed/run.sh                    # all four; or name scenario ids
for s in scenario_s08_0{1,2,3,4}; do python analysis/ir_testbed/summary.py analysis/ir_testbed/$s > analysis/ir_testbed/$s/summary.md; done
```

## The pipeline, per scenario (`run.sh`)

1. **The run.** The log and its `.rec` go to `runs/env_layout_10_<scenario>_on.{log,rec}` (git-ignored; md5s below).
2. **`trajectory.py` → `trajectory.json`: the body side.**
   - It loads the scenario with the human alone, as `tests/test_th2_executor.py` does, so no recognizer is
     constructed. It then runs the load-time replay `check_script` with the body's conversions (`steps_toward` at
     the body's step size, `_parse_duration_to_steps`).
   - It expands the replay's actions per tick with the body's timing, read from `Executor.step` and
     `HumanAgent._step_stack`:
     - completion is checked at the tick's start, and when it holds the tick is the action's acknowledgement;
     - a walk takes the `steps_toward` positions until `at` holds (30 cm), short of the target point;
     - GRASP, RELEASE and a wait_at's STANDs follow the body's rules, the last STAND recording waited_at;
     - the human spends no per-task completion tick.
   - It derives the world facts the phase rule reads, by `build_world_state`'s rules: `at` for non-held objects
     within 30 cm, `holding`, `obj_at` (the holder while carried) and `waited`.
   - Tick −1 is the observation before the clock starts (`RobotAgent.observe_initial`).
   - **Its own check:** on every tick, the position (rounded to the log's 2 decimals), the action and the micro
     equal the run's human lines. The fallback (reading the run's human lines instead) is to be built only if this
     check fails.
3. **`oracle.py` → `expected.csv`, `phases.json`: the expectation generator.**
   - It imports nothing from `shared/recognizer.py` or `shared/likelihood_functions.py`, and asserts at exit that
     neither was loaded.
   - It uses `AdaptivePlanner.decompose` on the robot's task model: the planner's decomposition and the domain's
     method guards, which are the domain's structure.
   - Its inputs are the trajectory, the body's parameters it carries (checked against the run's `[run]` header:
     speed 20, β 0.01, test_level 0.05) and α from the run file.
4. **`actual.py` → `actual.csv`, `actual_log.csv`: the recognizer's outputs.** This is option B of the plan step,
   confirmed by Hadi:
   - `actual_log.csv` is read from the run log with `analysis/td_stage1b/tdlib.py`, at print precision: belief 3
     decimals, S 4, position 2. tdlib's `[coverage]` pattern does not match a line with a `start:` entry, so it is
     handed the log without its `[coverage]` lines, which nothing here reads.
   - `actual.csv` comes from the same run re-executed in-process from its run file. After every tick it reads the
     robot's public `BeliefState` at full precision (distribution, tails, hypothesis_adequacy, finding, lifecycle,
     most_likely, confidence) and the world the robot built. Its `[IR*]` lines are asserted byte-identical to the
     logged run's.
   - Nothing of the recognizer is read beyond its output.
5. **`compare.py` → `diff.md`.**
   - Rows are keyed by (tick, live hypothesis), ticks 0 onward; tick −1 has no log line (reading R4).
   - Categorical values are compared exactly.
   - Numeric values are compared against `actual.csv` at relative tolerance 1e-9 (absolute 1e-12 near zero), and
     against `actual_log.csv` at half a unit of the printed digit.
   - Every disagreement is listed with its tick and classified by hand after investigation: the generator misread
     the records; the recognizer disagrees with the records; or the records do not determine the value (used only
     where they genuinely do not).
6. **`plot.py` → `figure.png`.** Belief and S per hypothesis over ticks (expected as lines, actual as dots every fifth
   tick), with θ and α marked, the finding and lifecycle as a band, and the script's action boundaries as thin
   vertical lines.
7. **`summary.py` → `summary.md`.** The tables REPORT.md quotes: the expected-action table, the events, and the trends
   read from `actual.csv`.

### Columns

Per tick per live hypothesis (a tick with none live has one row with the hypothesis fields empty):

- **Per tick:** tick, human_x, human_y, micro, holding, waited, obj_at, at (the human's `at` facts), most_likely,
  confidence, finding, lifecycle, pins, boundary.
- **Per hypothesis:** key, expected_action, origin_x, origin_y, e, s, s_exp, D, L, evidence (the normalised
  evidence before the output floor), belief, S (members only), member, adequacy.

The recognizer does not output `expected_action`, `origin_x`, `origin_y`, `e`, `s`, `s_exp`, `D`, `L` or `evidence`.
They are empty in both actual files and are not compared. `actual_log.csv` also leaves `holding`, `waited`, `obj_at`
and `at` empty (the log does not carry them).

## The rules the generator implements, with their sources

HB is `docs/recognizer_handback.md`; DD is `docs/design_decisions.md`, "T-D R and E", with its "1.5 rulings".

| # | rule | source |
|---|---|---|
| 1 | Hypothesis space: one key per task schema of the robot's task model and typed binding of its enumerated parameters (determined parameters not enumerated), keys sorted; the support under the prior is the assigned tasks ∪ every PersonalTask hypothesis | HB §1.1; glossary §5 |
| 2 | Uniform prior 1/\|H\| at construction and at every boundary; the observation before the clock starts is a scored update | HB §1.2; `RobotAgent.observe_initial` |
| 3 | The clocks: step = \|p − p_last\| (0 on the first observation), odometer += step, standing clock += (step = 0) | HB §1.8 |
| 4 | The phase: the expected action is the first grounded action of the decomposition whose completion does not hold; two actions are the same when their name and grounded bindings are | HB §1.3 |
| 5 | The terminal pin: the terminal action's completion holds → retired; the boundary iff the retiring hypothesis expected its terminal action on the previous tick | HB §1.6, §1.8; DD R6 |
| 6 | The first observation: origin set, entry latency 0, U = base (no factor) | HB §1.8 |
| 7 | The completion signal: pick_up → GRASP, place → RELEASE; HIT 1.0 if the previous expected action's completion holds, else FALSE_ALARM 10⁻³ | HB §1.4, §2; reading R1 |
| 8 | The fold at a phase change (advance or regress): the closing phase's L with this tick included; the origin moves; entry latency 1 iff the previous expected action's completion holds, else 0; E8's advanced set | HB §1.5, §1.8; DD E8, E9 |
| 9 | e = w + C(p,g) − C(o,g), straight-line C; 0 for an action with no progress evaluator (pick_up, place, wait_at), no resolvable target, or w ≤ 0 | HB §1.4, §1.8; DD E2 |
| 10 | Target resolution: the target's current position; a carried object is at its holder's position | HB §1.4 (`target_resolution`) |
| 11 | s = standing ticks since the origin; s_exp = the entry latency + the action's own stationary duration (0 for a walk; the bound duration in ticks for wait_at, PT60S → 30; else the body's default action cost, 1, for pick_up and place) | HB §1.10 table; DD E9, "the source of s_exp" |
| 12 | D = e/v + (s − s_exp); L = 2 / (1 + exp(β·v·D)) for v·D > 0, else 1 (clipped) | DD E2, E10; HB §1.4 |
| 13 | Evidence: U = base × L(open phase); one normalisation over H; bases rescaled by the same total | HB §1.5; DD R1, R6 |
| 14 | The boundary: bases uniform over the live set, evidence = base, every origin moved, entry latency 1 + 0 (the action and observed-task latencies), no E8 member | HB §1.6, §1.8; DD E9 |
| 15 | The output: context weight ω = 1 (inert, HB §2); normalise over H, max with BELIEF_FLOOR = 10⁻³, pinned keys at the floor, live keys scaled to 1 − FLOOR·\|pinned\|; most_likely the argmax, ties to the first key in sorted order; exhausted: most_likely none, confidence 0 | HB §1.7; reading R2 |
| 16 | Membership as amended twice, with the boundary-tick rule: member iff it has a derived phase, the tick is not a boundary tick, and w > 0 ∨ s > s_exp ∨ (s ≤ s_exp ∧ (a stationary action ∨ s_exp > 0)) ∨ it advanced this tick (E8, S = 1) | DD E6 (both amendments), E8; HB §1.10; reading R3 |
| 17 | S(x) = ln(1 + e^(−βx)) / ln 2 for x > 0, else 1 | DD E5; HB §1.10 |
| 18 | The finding: unresolved iff no member; unexplained iff every member has S < α; otherwise adequate. Hypothesis adequacy: adequate / inadequate (members), no_observation | DD E4, G1; HB §1.10 |
| 19 | The lifecycle: exhausted iff H is empty, and no finding then | DD R4; HB §1.7, §1.10 |
| 20 | The proximity regress: `at` flickering at 30 cm is a phase change like any other (rules 4 and 8) | HB §1.3; DD limitation (b) |

The generator also checks R6 at level (1) on every tick: the evidence sums to 1 over exactly H.

### The readings confirmed at the plan step

Where the records are loose, the generator reads them as follows (Hadi, 27 September 2026):

- **R1.** The completion signal covers only a declared microaction list (GRASP, RELEASE). STEP* and STAND* declare no
  completion signal.
- **R2.** The output floor, in this order: normalise over H, max with the floor, pinned keys at the floor, live keys
  scaled.
- **R3.** Membership as in rule 16. The "stationary tick" qualifier changes nothing beyond it.
- **R4.** Tick −1, the observation before the clock starts, is expected but not compared.

## What the comparison validates

The comparison validates the recognizer's public outputs against the independent oracle. The recognizer's private
expected action and origin are not independently validated, by choice (option B; option C, reading them, was not
built).

## Runs (git-ignored logs; md5s at this commit)

```
1231104d1ed3b5fb6fcd8dc7531f3824  runs/env_layout_10_scenario_s08_01_on.log
2b6dafd84a0086185ec971c2bde68d75  runs/env_layout_10_scenario_s08_01_on.rec
2353ceca5abc2e75167a2cb61cc7b8f3  runs/env_layout_10_scenario_s08_02_on.log
a9c382958a10484ae1bc2df54e4d3a1c  runs/env_layout_10_scenario_s08_02_on.rec
d0dbdbd69c01d7989150ae0bd27f039f  runs/env_layout_10_scenario_s08_03_on.log
93551c8fa122df7c3ad6a028f9717845  runs/env_layout_10_scenario_s08_03_on.rec
26e2cc6d9052ee572b7e117be366c9c1  runs/env_layout_10_scenario_s08_04_on.log
b2d33459410319657e1f47791c1e180e  runs/env_layout_10_scenario_s08_04_on.rec
```
