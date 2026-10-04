# The IRB (IRB.3b)

The data and figures of this set (.json, .csv, .png) are not in git (Hadi, 2 October 2026). They are regenerated
by the set's run script (`analysis/instruments/irb/run.sh kitting`). A byte comparison uses the local copy or the outside copy,
`/home/hadi/teamrob_analysis_2026-10-02/` (the whole of analysis/ as it was at 38d66ea).

The recognizer tested in isolation, on a layout, a setup and scenarios written for it, against expectations derived
from the recognizer records before the run (design_decisions.md, "The intention-recognition test-bed (IRB)"; glossary §8, IRB). This file is
the instrument: what it runs, what it derives, from which record, and how it compares. The results are in
`REPORT.md`. Built in IRB.3b (27 September 2026) on env_layout_10; made independent of the layout in IRB.4b, which added
the enlarged room and its twelve scenarios (the section "IRB.4b" below).

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
- `configs/irb/scenario_s08_0N.yaml`: one run file per scenario. Each sets layout env_layout_10, the prior on,
  single_task, gate none, cost realized, separation_stop off and test_level 0.05. Its steps are the replay's last
  acknowledgement tick + 1 + 30 ticks of the idle human, where 30 covers E5's standing threshold at α = 0.01
  (25 ticks). That gives 204, 281, 271 and 282 steps (last acknowledgements 173, 250, 240, 251). Every run is under
  500 steps, so the `coffee_break` context weight stays inert (handback §2).

To run one scenario by hand:

```bash
PYTHONHASHSEED=0 python mesa_sim/run_mesa.py --run configs/irb/scenario_s08_01.yaml   # every run file likewise
```

To run the whole instrument (the run lengths, runs, trajectories, expectations, actual outputs, comparisons, figures
and summaries) from the repo root (since IRB.4b; before it, run.sh took scenario ids and summary.py ran separately):

```bash
analysis/irb/run.sh                                            # every run file in configs/irb/
analysis/irb/run.sh configs/irb/scenario_s09_*.yaml     # the enlarged room's twelve
analysis/irb/run.sh -o <dir> configs/irb/scenario_s08_0{1,2,3,4}.yaml   # into another folder
```

Running every run file regenerates the s08 folders' `figure.png` and `summary.md` in the IRB.4b presentation (below);
their committed IRB.3b versions are kept by running the s09 files only.

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

## IRB.4b: independent of the layout; the enlarged room

Built in IRB.4b (27 September 2026). Hadi's constraint: the instrument reads the room, the shift and the scripts from
the artefacts; no coordinate, id or tick appears in the generator, the comparison or the plots; a changed layout means
rerunning, nothing else.

- **What changed in the instrument.**
  - `trajectory.py` takes the run file (its layout, or the scenario's first reference layout, and its scenario); the
    observed human is the scenario's one human; the grasped object is the one the action's schema moves
    (`moved_object_key`); the body's ticks of a duration are computed for every duration bound in the methods of the
    task model's schemas that this room can instantiate. `--length` prints the replay's last acknowledgement tick.
  - `oracle.py` and `actual.py` take the observed human from the scenario; `actual.py` takes the run's steps.
  - `plot.py` and `summary.py` read θ, α, β and v from the run's `[run]` header and label a key without its parameter
    names. `summary.py` reads the truth's coverage from the loader's `[coverage]` lines, generalises the coffee boundary
    to every task started by an event (its start, its pin, the resumption), and calls the script's last entry the exit
    walk by position (the authoring convention). Its event table adds the ticks the finding turns unexplained and back,
    the admissible hypotheses never pinned, and the lifecycle and finding on the last entry and the idle ticks after it.
  - `run.sh` runs every run file (or those named), computes the run length by IRB.3b's rule from the replay and passes
    it as `--steps`, printing a notice when a run file's own `steps` differs (Q3 of the IRB.4b plan).
  - One new body rule in the trajectory: an action with process completion (`stand`) records nothing on its STANDs and
    is complete once they have run (`Executor._is_action_complete`; `action_decomposer._expand_stand`).
  - One reader fix in `actual.py`: the log reader's live set is the support (the `[IR-prior]` known tasks' hypotheses
    and every PersonalTask hypothesis, handback §1.1), not every key not yet pinned. The defect appeared with the first
    room holding a hypothesis outside the support (item_3); the in-process source never had it.
- **The check on the IRB.3b runs.** s08_01 to _04 rerun through the changed instrument into another folder: the logs,
  `.rec` streams, `trajectory.json`, `expected.csv`, `actual.csv`, `actual_log.csv`, `diff.md` and `phases.json` are
  byte-identical to the committed ones; `figure.png` and `summary.md` differ in presentation only (the generic labels,
  the added coverage and stack-depth columns, the support line, the event-table additions), their numbers unchanged.
- **The enlarged room.** `env_layout_11` is env_layout_10 plus kitting_table_1 at (350, 420) (the north wall, bearing
  0° from kitting_table_0, 46.3° from its nearest target, shelf_2) and shelf_3 at (−420, 300) (the west wall 320 cm
  above shelf_1, bearing −164.1°, 30.4° from shelf_1 and 62.3° from coffee_machine_0). `env_setup_09`: item_1, item_2
  and item_3 on shelf_1, shelf_2 and shelf_3, all designated to kitting_table_0. `scenarios_s09.py`: _01 to _04 the IRB.3b
  scripts re-authored on this room; _05 the corner walk mid-delivery; _06 the long stand (`stand("PT80S")`, the
  migration of Stay(40)); _07 the change of mind (`deliver_item(item_1).at(pick_up, deliver_item(item_2))`); _08 the
  misdelivery to kitting_table_1; _09 a delivery of item_3, outside the support; _10 and _11 both deliveries west
  (item_1, item_3 assigned; item_2 outside the support), _11 with coffee between; _12 the reverse order of _01.
- **shelf_3's position, chosen for observability** (the IRB.4b addendum). The criterion, stated before any run: in _10,
  on the walk to item_1 (the only place both west deliveries are rivals), the rival delivery of item_3 is refuted
  (S < α, from the oracle) after the first quarter of the walk's ticks and before its arrival. Tried first: (−420, −220)
  (10.4° from shelf_1): not met; the rival's excess at the arrival (tick 28) was 35.8 cm (S = 0.765), and S fell below α
  only at 41, on the carry after the grasp. Kept: (−420, 300), the first position up the west wall that meets it (the
  analytic screen: (−420, 240) reaches the threshold only at the arrival tick): S < α at tick 25, the arrival at 28, the
  first quarter ending at 7 (shallow run 2 with the oracle; the rival's excess 443.4 cm at the arrival). Chosen for the
  phenomenon's observability, never for a belief or finding value; the expectations were derived after it was fixed.
  The human of the IRB.3b scripts never comes within 221 cm of shelf_3 or 253 cm of kitting_table_1, and on the new
  scripts each new object is reached only where a script targets it.
- **Run lengths**, by the rule: s09_01 to _12: 204, 281, 271, 282, 270, 246, 252, 211, 252, 188, 276, 205 steps.

### Runs of the enlarged room (git-ignored logs; md5s at IRB.4b)

The s09_01 to _04 `.rec` streams are byte-identical to s08_01 to _04's: the same ground truth.

```
72aa02bcfe5372057f3f293ba53f7e12  runs/env_layout_11_scenario_s09_01_on.log
2b6dafd84a0086185ec971c2bde68d75  runs/env_layout_11_scenario_s09_01_on.rec
009f1a56e9dd44021cf98c6434debaac  runs/env_layout_11_scenario_s09_02_on.log
a9c382958a10484ae1bc2df54e4d3a1c  runs/env_layout_11_scenario_s09_02_on.rec
daa2de0bda0e8b61002e338fb39e0283  runs/env_layout_11_scenario_s09_03_on.log
93551c8fa122df7c3ad6a028f9717845  runs/env_layout_11_scenario_s09_03_on.rec
7734174519c6d6e519b6256de44f029c  runs/env_layout_11_scenario_s09_04_on.log
b2d33459410319657e1f47791c1e180e  runs/env_layout_11_scenario_s09_04_on.rec
d05c73bcf7ba5b558c3797826f897a69  runs/env_layout_11_scenario_s09_05_on.log
c715db44f68926f3bb6b8fa387525f1a  runs/env_layout_11_scenario_s09_05_on.rec
5d8a020b61cf49c5d23db4668053d3c7  runs/env_layout_11_scenario_s09_06_on.log
703b2c62e484b7db940f36166548a88c  runs/env_layout_11_scenario_s09_06_on.rec
d39f1766c59f60131af1e656e8f4a561  runs/env_layout_11_scenario_s09_07_on.log
a2ece1d231a6c071c20efdea470c4c9f  runs/env_layout_11_scenario_s09_07_on.rec
0a552ed661eca67c4e58a05637cf6b55  runs/env_layout_11_scenario_s09_08_on.log
529f6f2019682be19b77f4e1152b1ea5  runs/env_layout_11_scenario_s09_08_on.rec
03e68253f59d1f21ef8f2b69811beff6  runs/env_layout_11_scenario_s09_09_on.log
e252b7b8e703da1492b52df3ae4df3dc  runs/env_layout_11_scenario_s09_09_on.rec
649fd08e6e21fcb668e413ab68759117  runs/env_layout_11_scenario_s09_10_on.log
c3515ed75407562597852c6bf654c806  runs/env_layout_11_scenario_s09_10_on.rec
fe16c489944f62e41dabeb29a16ca44f  runs/env_layout_11_scenario_s09_11_on.log
9a4309d36ae6a47d9f1e36f512b711b2  runs/env_layout_11_scenario_s09_11_on.rec
4338cf7d2c454d27cbe98f18bc63150d  runs/env_layout_11_scenario_s09_12_on.log
606beeb608930d07b519195f915aae90  runs/env_layout_11_scenario_s09_12_on.rec
```

## L-build: the generator derived from "T-D L" (28 September 2026)

The recognizer changed under design_decisions.md, "T-D L: the belief lifecycle", as amended on the L-records report
(DL). The generator was changed by derivation from DL before the recomparison, rule by rule; nothing was fitted to a
run. The recognizer reads L1 generically, through each terminal action schema's preconditions and completion condition
(`AdaptivePlanner.enabled_groundings` / `completed_groundings`); the generator reads it in the entry's own words for the
domain's two terminal actions, and computes re-entry after its normalisation where the recognizer computes it before.

| # | rule (changed or new) | source |
|---|---|---|
| 5 (replaced) | The terminal pin: the terminal action's completion holds → retired, WHILE it holds, read on every tick over every admissible key; a retired key whose fact no longer holds is live again (a retired key the planner cannot decompose stays retired: its fact cannot be read). The boundary is no longer read from the pin | DL L4; HB §1.6 (superseding note) |
| 5b (new) | The boundary (DL L1 as amended): the item the human held on the previous tick is no longer held and is `obj_at` a location that is not an agent (the release leaves the object placed at a container: `place`), or `waited(human, ·)` holds and did not on the previous tick (`wait_at`). The world facts only; no microaction; none on the first observation | DL L1 (amended) |
| 21 (new) | Re-entry, arithmetic C: a returning key enters as a first observation (origin the current position, entry latency 0, its derived action from the world); after the normalisation over the incumbents, with n = \|H\| including the k returning keys, each returning key's evidence and base are 1/n and the incumbents' are scaled by (n − k)/n. A re-entry on a boundary tick is governed by the boundary (rule 14) | DL L4 (amended) |
| column | `reentries`: the keys that re-enter on the tick (`[IR-reentry]`), compared as a per-tick column in both comparisons | DL L4 |

The log reader: `actual.py` reads the log with `analysis/l_build/tdlib.py` (the frozen `analysis/td_stage1b/tdlib.py`
has no `[IR-reentry]`); the live set on a tick is the support minus the keys retired on that tick (the last
`[IR-complete]` later than the last `[IR-reentry]`). `summary.py`'s event table gains the re-entries and marks a boundary
without a pin. Running every run file regenerated the s08 folders' `summary.md` and `figure.png` in the IRB.4b
presentation (see above).

### Runs (git-ignored logs; md5s at L-build)

The `.rec` streams are byte-identical to the IRB.3b and IRB.4b tables above: the same ground truth.

```
9a36fb06f087da46d4a1e56b79ffc591  runs/env_layout_10_scenario_s08_01_on.log
2b6dafd84a0086185ec971c2bde68d75  runs/env_layout_10_scenario_s08_01_on.rec
0049af9dc8db2c66fc9fbb8ec2418abf  runs/env_layout_10_scenario_s08_02_on.log
a9c382958a10484ae1bc2df54e4d3a1c  runs/env_layout_10_scenario_s08_02_on.rec
aacf368e3c327b4a369315c2990ec7e1  runs/env_layout_10_scenario_s08_03_on.log
93551c8fa122df7c3ad6a028f9717845  runs/env_layout_10_scenario_s08_03_on.rec
58ba7c6ae3c13da29ca9cd8755e007e4  runs/env_layout_10_scenario_s08_04_on.log
b2d33459410319657e1f47791c1e180e  runs/env_layout_10_scenario_s08_04_on.rec
aa5da7bb2fc0f675caffc55e98fcd547  runs/env_layout_11_scenario_s09_01_on.log
2b6dafd84a0086185ec971c2bde68d75  runs/env_layout_11_scenario_s09_01_on.rec
5d81043d74972af03f1467171c73a970  runs/env_layout_11_scenario_s09_02_on.log
a9c382958a10484ae1bc2df54e4d3a1c  runs/env_layout_11_scenario_s09_02_on.rec
0656a6d56c183c5e414f9639ee6a28e4  runs/env_layout_11_scenario_s09_03_on.log
93551c8fa122df7c3ad6a028f9717845  runs/env_layout_11_scenario_s09_03_on.rec
ace2ca9fbc23190dfa3b4ab97fc0d941  runs/env_layout_11_scenario_s09_04_on.log
b2d33459410319657e1f47791c1e180e  runs/env_layout_11_scenario_s09_04_on.rec
be0da8567ecf85fe9eafdd58d9407a78  runs/env_layout_11_scenario_s09_05_on.log
c715db44f68926f3bb6b8fa387525f1a  runs/env_layout_11_scenario_s09_05_on.rec
b8c0d2ef82a1676f6ef041f2926f7f3d  runs/env_layout_11_scenario_s09_06_on.log
703b2c62e484b7db940f36166548a88c  runs/env_layout_11_scenario_s09_06_on.rec
90af534c2795eb5a0108b08bd7f822a4  runs/env_layout_11_scenario_s09_07_on.log
a2ece1d231a6c071c20efdea470c4c9f  runs/env_layout_11_scenario_s09_07_on.rec
c72ff48aac72ba69e77f8651f4c2b97f  runs/env_layout_11_scenario_s09_08_on.log
529f6f2019682be19b77f4e1152b1ea5  runs/env_layout_11_scenario_s09_08_on.rec
2c279ff1272f92acc0964182ba92445e  runs/env_layout_11_scenario_s09_09_on.log
e252b7b8e703da1492b52df3ae4df3dc  runs/env_layout_11_scenario_s09_09_on.rec
956be2616c8b13ba0f9694e3d9042a6d  runs/env_layout_11_scenario_s09_10_on.log
c3515ed75407562597852c6bf654c806  runs/env_layout_11_scenario_s09_10_on.rec
bd0bc2848e3cda44cf4deac350566929  runs/env_layout_11_scenario_s09_11_on.log
9a4309d36ae6a47d9f1e36f512b711b2  runs/env_layout_11_scenario_s09_11_on.rec
a13dfaf332631c16610f71df1f578b98  runs/env_layout_11_scenario_s09_12_on.log
606beeb608930d07b519195f915aae90  runs/env_layout_11_scenario_s09_12_on.rec
```

## Track 2.5: the mid-action cut; scenario_s09_13 (29 September 2026)

- **The scenario.** `scenario_s09_13` on env_layout_11 (`scenarios_s09.py`; run file
  `configs/irb/scenario_s09_13.yaml`): `coffee_break(coffee_machine_0)` cut into item_1's carry mid-walk
  (`.during(move_to, "PT28S", ..., occurrence=1)`, 14 of the carry's 28 steps), then deliver item_2, exit. The
  recognition side of a mid-action change (`docs/assumptions.md`, 3.1 rejected); the robot is idle.
- **What changed in the instrument.** `trajectory.py` only: it expanded no mid-action cut before (it raised). The rule,
  by derivation from T-H's executed semantics (design_decisions.md, "T-H", item 6 and the T-H2 TICKS line;
  `HumanAgent._step_stack` step 3, `Executor.suspend` / `resume`): the cut is read from the replay's record (a `Started`
  whose `where` is a `Cut`, on the replay step of the cut action's snapshot); the action runs that many microactions
  and stops where the human stands, with no acknowledgement tick; the resumption (the replay's snapshot of the cut
  action with done > 0) completes the cut action first, a walk as a fresh `steps_toward` from the current position to
  the target's current position, a stand or wait_at with its remaining STANDs; then the replay's next snapshots, as any
  action. `trajectory.json`'s form is unchanged.
- **The check.** The sixteen earlier run files through the extended instrument (`run.sh -o <dir>`): every committed
  output byte-identical, figures and summaries included. scenario_s09_13: the trajectory equals the run's human lines on
  every tick; 0 disagreements. Results: `REPORT.md`, "Track 2.5".
- **Run length**, by the rule: 292 steps (last acknowledgement 261).

```
60d9491efa8d61c7c5679f1a1307719f  runs/env_layout_11_scenario_s09_13_on.log
739ce3199f341516687bfc7701b29143  runs/env_layout_11_scenario_s09_13_on.rec
```

## G-build: observation warrant and the gate (29 September 2026)

The recognizer gained the observation warrant per live hypothesis and the gate its warrant condition (design_decisions.md,
"T-D G: admission" (DG), AD1 to AD4, and the ruling on an unresolved target at the G-build plan step). The generator was
extended by derivation from DG before the recomparison; nothing was fitted. Results: `REPORT.md`, "G-build".

| # | rule (new) | source |
|---|---|---|
| 22 | Observation warrant per live hypothesis: observation if the phase was entered at a fold where the previous expected action's completion holds (the completion E8 reads), since the hypothesis's last boundary, first observation or re-entry (the entry source, any phase); else, for an action with a movement target whose position resolves (rule 10), observation iff dist(o, g) − dist(p, g) > 0 from the phase origin (the movement source, rule 9's straight-line C); none otherwise: no derived phase; a stationary phase (no movement target); a `move_to` whose target has no position (no gain computable); no positive gain. Both sources reset with the origins, at a boundary and at a phase change | DG AD1; the plan-step ruling |
| 23 | The gate's outcome per tick: `none(below_theta)` if the confidence is below θ (exhausted: no leader); else the leader's hypothesis adequacy, `none(leader_inadequate)`, then `none(leader_no_observation)`; else `none(leader_unwarranted)` if the leader is neither an assigned task (commitment: rule 1's known keys) nor observation-warranted; else `clears`. θ from the run's `[run]` header (the one value read from the log: `shared.meta_planner` would load the recognizer) | DG AD1, AD4; DD G1 |
| column | `warrant` per hypothesis, compared exactly against actual.csv (`BeliefState.observation_warrant`) and actual_log.csv (the `[IR]` line's `warrant=[...]`) | DG AD2, AD4 |
| column | `gate` per tick, compared exactly against actual.csv (the robot's meta-planner's `_clears_gate` on that tick's BeliefState: the idle robot asks admission at tick 0 only, so the log carries no per-tick gate) | DG AD1 |

The log reader: `actual.py` removes the `[IR]` line's trailing `warrant=[...]` before the frozen
`analysis/l_build/tdlib.py` reads the line (its `tails` pattern would take it in) and parses it itself. `plot.py` adds a
panel (per hypothesis the ticks it is observation-warranted, and the ticks the gate clears; expected bars, actual
marks); `summary.py` adds the warrant stretches and the gate's answer per stretch. `run.sh` passes the run log to the
oracle.

### Runs (git-ignored logs; md5s at G-build)

The `.rec` streams are byte-identical to the tables above. The logs differ from the L-build and 2.5 runs in the `[IR]`
line's warrant field, and s08_01 to s09_12 also in the step-0 `[meta-proj]` line (T-D P's fallback; those runs were last
made at L-build, before P).

```
bb46aab93594b0630947696e8a48aee1  runs/env_layout_10_scenario_s08_01_on.log
2b6dafd84a0086185ec971c2bde68d75  runs/env_layout_10_scenario_s08_01_on.rec
e036d0f408650738e81b2ec4d9a0b6d4  runs/env_layout_10_scenario_s08_02_on.log
a9c382958a10484ae1bc2df54e4d3a1c  runs/env_layout_10_scenario_s08_02_on.rec
508ac1b4b4a759b6c4147d240fdcf3c7  runs/env_layout_10_scenario_s08_03_on.log
93551c8fa122df7c3ad6a028f9717845  runs/env_layout_10_scenario_s08_03_on.rec
79488c2619753d96af4b0884977eb68a  runs/env_layout_10_scenario_s08_04_on.log
b2d33459410319657e1f47791c1e180e  runs/env_layout_10_scenario_s08_04_on.rec
f06adb1e02734a19be04e77b61ed5b08  runs/env_layout_11_scenario_s09_01_on.log
2b6dafd84a0086185ec971c2bde68d75  runs/env_layout_11_scenario_s09_01_on.rec
8f836baad3f9410151c5c916f0077856  runs/env_layout_11_scenario_s09_02_on.log
a9c382958a10484ae1bc2df54e4d3a1c  runs/env_layout_11_scenario_s09_02_on.rec
a303d0ab64534d6abafe12dd01082795  runs/env_layout_11_scenario_s09_03_on.log
93551c8fa122df7c3ad6a028f9717845  runs/env_layout_11_scenario_s09_03_on.rec
a89938cedb4d00fe2a032109e7c8f013  runs/env_layout_11_scenario_s09_04_on.log
b2d33459410319657e1f47791c1e180e  runs/env_layout_11_scenario_s09_04_on.rec
86edbd8ed36b46aedda1393f823448de  runs/env_layout_11_scenario_s09_05_on.log
c715db44f68926f3bb6b8fa387525f1a  runs/env_layout_11_scenario_s09_05_on.rec
2c92080c3c60764a5d2c011855069c52  runs/env_layout_11_scenario_s09_06_on.log
703b2c62e484b7db940f36166548a88c  runs/env_layout_11_scenario_s09_06_on.rec
31259b7bb1a3d4795fc7e1b5818f9626  runs/env_layout_11_scenario_s09_07_on.log
a2ece1d231a6c071c20efdea470c4c9f  runs/env_layout_11_scenario_s09_07_on.rec
1c949ecc4c40db7364f75ff4f89cb59d  runs/env_layout_11_scenario_s09_08_on.log
529f6f2019682be19b77f4e1152b1ea5  runs/env_layout_11_scenario_s09_08_on.rec
0dcd0fc9abed38283ea69892f9adfc77  runs/env_layout_11_scenario_s09_09_on.log
e252b7b8e703da1492b52df3ae4df3dc  runs/env_layout_11_scenario_s09_09_on.rec
39f97c770277dbc9d08fc5a5ff6f52a9  runs/env_layout_11_scenario_s09_10_on.log
c3515ed75407562597852c6bf654c806  runs/env_layout_11_scenario_s09_10_on.rec
c1598c77bd67c1d327fd60660aa1e027  runs/env_layout_11_scenario_s09_11_on.log
9a4309d36ae6a47d9f1e36f512b711b2  runs/env_layout_11_scenario_s09_11_on.rec
0f41391730ebac6920df37438df30e37  runs/env_layout_11_scenario_s09_12_on.log
606beeb608930d07b519195f915aae90  runs/env_layout_11_scenario_s09_12_on.rec
518acab6d75c24aaecddfb13ddd4f324  runs/env_layout_11_scenario_s09_13_on.log
739ce3199f341516687bfc7701b29143  runs/env_layout_11_scenario_s09_13_on.rec
```

## The sort (1 October 2026): paths only, no change of behaviour

This folder holds kitting's set: the scenarios' outputs, `runs/` (git-ignored), this README and `REPORT.md`
(`docs/rename_table.md`, "Paths: the sort"). The instrument's code moved to `analysis/instruments/irb/` and is
shared by the domains; the run files moved to `configs/kitting/irb/`; the log reader is
`analysis/instruments/common/tdlib.py`, a copy of the frozen `analysis/kitting/l_build/tdlib.py`. Every command above
reads:

```bash
analysis/instruments/irb/run.sh kitting                                       # every configs/kitting/irb/*.yaml
analysis/instruments/irb/run.sh kitting configs/kitting/irb/scenario_s09_*.yaml
analysis/instruments/irb/run.sh kitting -o <dir> configs/kitting/irb/scenario_s08_0{1,2,3,4}.yaml
```

The seventeen runs and every output were regenerated from the sorted tree into another folder: byte-identical to the
committed outputs and to the G-build md5s above.

## T-K part 1, build stage 2: the gate on the belief over the live hypotheses (4 October 2026)

The recognizer's `confidence` is the leader's belief over the live hypotheses (AM42); the generator follows by
derivation, nothing fitted:

| # | rule (new) | source |
|---|---|---|
| 28 | The leader and its confidence: the argmax of the belief over H (the evidence normalised over H, before the floor and the pins of rule 15) and its value there; ties to the first live key in sorted order. Rule 23's θ test reads this value. The `belief` column stays rule 15's reported distribution; the new column `belief_h` is the belief over H per hypothesis, compared against actual.csv (`BeliefState.belief`) at 1e-9 | design_decisions.md, "T-K", R7's AM42 |

The seventeen were rerun and their outputs replaced (AM57). Old data and figures: Kept in one external copy, outside the repository (AM59): `/home/hadi/teamrob_analysis_2026-10-04/` (its README.txt).
The last commit holding the old results' reports: 3b05a8a (the build's stage 2b; the reports there are
93f9083's).
Result: 0 disagreements in all seventeen, every column, `belief_h` included. The gate's per-tick answer moves on four
ticks, each a leader at 0.749 to 0.750 that now clears: scenario_s08_03 and s09_03 at 44 (coffee_break), s09_09 at 122
(deliver_item(item_2)), s09_12 at 87 (deliver_item(item_1)). The `.rec` streams are byte-identical. Runs (git-ignored;
md5s at the rerun):

```
fb58164ca8cf2d7239ae49e183fd32c9  runs/env_layout_10_scenario_s08_01_on.log
2b6dafd84a0086185ec971c2bde68d75  runs/env_layout_10_scenario_s08_01_on.rec
cd9b66b7a91acee7c2af1d82640a2533  runs/env_layout_10_scenario_s08_02_on.log
a9c382958a10484ae1bc2df54e4d3a1c  runs/env_layout_10_scenario_s08_02_on.rec
992a4e4d02ecd252585eeb791664ec3b  runs/env_layout_10_scenario_s08_03_on.log
93551c8fa122df7c3ad6a028f9717845  runs/env_layout_10_scenario_s08_03_on.rec
ec05cac2465ee9f4c06a4c37de31db95  runs/env_layout_10_scenario_s08_04_on.log
b2d33459410319657e1f47791c1e180e  runs/env_layout_10_scenario_s08_04_on.rec
0d4ffad4c19ea70f5d97d9c5372f4fdd  runs/env_layout_11_scenario_s09_01_on.log
2b6dafd84a0086185ec971c2bde68d75  runs/env_layout_11_scenario_s09_01_on.rec
6e262427ad7852bd18182cfcf072e511  runs/env_layout_11_scenario_s09_02_on.log
a9c382958a10484ae1bc2df54e4d3a1c  runs/env_layout_11_scenario_s09_02_on.rec
1cd0219fa6b677990e0f9fd2c76dcc09  runs/env_layout_11_scenario_s09_03_on.log
93551c8fa122df7c3ad6a028f9717845  runs/env_layout_11_scenario_s09_03_on.rec
eb35ca1490cbe50e590be96d0fd1281b  runs/env_layout_11_scenario_s09_04_on.log
b2d33459410319657e1f47791c1e180e  runs/env_layout_11_scenario_s09_04_on.rec
bb9e0b60c696055b341e0a8d7316319c  runs/env_layout_11_scenario_s09_05_on.log
c715db44f68926f3bb6b8fa387525f1a  runs/env_layout_11_scenario_s09_05_on.rec
b975ba1263789d78b5deeea47b1d19ee  runs/env_layout_11_scenario_s09_06_on.log
703b2c62e484b7db940f36166548a88c  runs/env_layout_11_scenario_s09_06_on.rec
61c1e64a15ea7370256f3330035eda19  runs/env_layout_11_scenario_s09_07_on.log
a2ece1d231a6c071c20efdea470c4c9f  runs/env_layout_11_scenario_s09_07_on.rec
2c122d143748842ea4e1582ceb62684e  runs/env_layout_11_scenario_s09_08_on.log
529f6f2019682be19b77f4e1152b1ea5  runs/env_layout_11_scenario_s09_08_on.rec
2c775e87238efe96d9d210848bbc2823  runs/env_layout_11_scenario_s09_09_on.log
e252b7b8e703da1492b52df3ae4df3dc  runs/env_layout_11_scenario_s09_09_on.rec
f1b7385a5089b4e6949993e632c64963  runs/env_layout_11_scenario_s09_10_on.log
c3515ed75407562597852c6bf654c806  runs/env_layout_11_scenario_s09_10_on.rec
52300e27ff0971b0e6a93f630834cf79  runs/env_layout_11_scenario_s09_11_on.log
9a4309d36ae6a47d9f1e36f512b711b2  runs/env_layout_11_scenario_s09_11_on.rec
22a4e7d56ecf26cc1b5cc103174d67f1  runs/env_layout_11_scenario_s09_12_on.log
606beeb608930d07b519195f915aae90  runs/env_layout_11_scenario_s09_12_on.rec
fd3f36430463c7e087a40103e8032899  runs/env_layout_11_scenario_s09_13_on.log
739ce3199f341516687bfc7701b29143  runs/env_layout_11_scenario_s09_13_on.rec
```
