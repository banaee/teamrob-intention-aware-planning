# The IRB: report (IRB.3b)

The recognizer in isolation on four scenarios written for it (design_decisions.md, "The intention-recognition test-bed (IRB)"). The
expectations were derived from the recognizer records by an independent generator before the runs. The instrument,
its rules with their sources, and the readings R1 to R4 confirmed at the plan step are in `README.md`. Prior ON in
every run; α = 0.05; θ = 0.75 (the meta-planner's, marked for reference only: with an empty pool the robot decides
nothing after tick 0). 27 September 2026.

**What the comparison validates.** Under B the comparison validates the recognizer's public outputs against the
independent oracle; the recognizer's private expected action and origin are not independently validated, by choice.

## Results

### The replay against the run

Per scenario, the replay expanded per tick against the run's human lines (position to the log's 2 decimals, action,
micro), over every tick of the run:

| scenario | ticks | result |
|---|---|---|
| scenario_s08_01 | 0 to 203 | equal on every tick |
| scenario_s08_02 | 0 to 280 | equal on every tick |
| scenario_s08_03 | 0 to 270 | equal on every tick |
| scenario_s08_04 | 0 to 281 | equal on every tick |

The trajectory's source is the replay throughout. The fallback (reading the run's human lines) was not needed and is
not built. `actual.csv`'s full-precision world facts per tick (`holding`, `waited`, `obj_at`, `at`) also equal the
trajectory's on every tick (diff.md).

### The comparison

`expected.csv` against `actual.csv` (full precision, relative tolerance 1e-9) and against `actual_log.csv` (print
precision). The in-process run's `[IR*]` lines are byte-identical to the logged run's in all four scenarios.

| scenario | ticks compared | (tick, live hypothesis) rows | disagreements vs actual.csv | vs actual_log.csv | rows on one side only |
|---|---|---|---|---|---|
| scenario_s08_01 | 204 | 389 | 0 | 0 | 0 |
| scenario_s08_02 | 281 | 395 | 0 | 0 | 0 |
| scenario_s08_03 | 271 | 402 | 0 | 0 | 0 |
| scenario_s08_04 | 282 | 423 | 0 | 0 | 0 |

The columns compared are:

- **Per tick:** human position, micro, holding, waited, obj_at, at, most_likely, confidence, finding, lifecycle, pins
  and boundary.
- **Per live hypothesis:** belief, S, member and hypothesis adequacy.

Not compared, because the recognizer does not output them: expected action, origin, e, s, s_exp, D, L and evidence.
The generator's own R6 check (the evidence sums to 1 over exactly H) held on every tick.

**Disagreements, classified.** There are none in any scenario, so there is nothing to classify. The per-scenario
`diff.md` files carry the per-column counts.

**The instrument can fail.** The comparison was checked for its power: each mutation below was applied to a scratch
copy of `oracle.py` (never committed) and compared against the unchanged `actual.csv`. The counts are disagreements
per scenario (_01 / _02 / _03 / _04).

| mutation of the generator | disagreements |
|---|---|
| E9: the latency after a completion not priced (entry latency 0) | 273 / 181 / 294 / 137 |
| the boundary-tick rule removed (members on a boundary tick) | 11 / 11 / 11 / 11 |
| E6's second amendment removed (s ≤ s_exp a member only in a stationary phase) | 18 / 18 / 18 / 18 |
| the boundary's entry latency not priced | 354 / 327 / 235 / 215 |
| L not clipped at 1 | 33 / 99 / 142 / 223 |
| reading R1 reversed (STEP / STAND as completion signals) | 231 / 247 / 271 / 363 |
| reading R2 reversed (no floor before the scaling) | 190 / 238 / 249 / 292 |
| **E8's member clause removed** | **0 / 0 / 0 / 0** |

E8 is not exercised independently in these scenarios. Every phase an advance opens is entered from a completion, so
its s_exp ≥ 1 (E9), and its entry tick (s = 0 ≤ s_exp) is already a member under E6's second amendment. The four runs
therefore cannot tell E8's clause apart from its absence. This is a property of the test set, recorded, not a
disagreement.

## Per scenario

Each section has the script's actions per tick, the expected-action table (the oracle's derived phases, which the
comparison does not validate against the recognizer's private state; see above), the derived tick table of events,
and the descriptive trends read from `actual.csv`. The trends describe what the outputs do; they judge nothing. v·D
is recovered from the actual S by inverting E5's tail. Its split into e and the standing charge v·(s − s_exp) is read
from `expected.csv`, whose every compared column equals `actual.csv`.

The truth on a tick is the hypothesis of the task the human's action on that tick belongs to. The acknowledgement tick
counts with its action. The truth is none ("-") for the exit walk and the idle human, which no hypothesis describes.
The finding and each S also appear in `figure.png`.

### scenario_s08_01

**Comparison:** 0 disagreements (204 ticks, 389 hypothesis rows). **Trends (actual):**
- **deliver item_1.** It leads from tick 0 and first reaches θ at 25, on its walk to shelf_1.
- **deliver item_2 while item_1 is the truth.** Its S falls below α at 14 on the first walk (e 357 cm). After the
  grasp at 30 its method becomes `deliver_with_return`: it expects `place(item_1, shelf_1)` (30 to 31), then
  `move_to(shelf_1)` from 32, and its S falls below α again at 41 (e 360 cm).
- **coffee_break.** Its S falls below α at 34: e 285 cm, plus 60 cm for the three standing ticks at the shelf,
  charged against its walk (s_exp 0). It falls below α again at 86, on deliver item_2's walk.
- **The boundaries at 61 and 124.** Each gives unresolved on the boundary tick and adequate on the next.
- **deliver item_2 as the truth.** It first reaches θ at 76.
- **The exit walk.** From 124 coffee_break is the lone live hypothesis, at 0.998. Its S falls below α at 157, 31
  ticks into the walk (v·D 344 cm, all excess), and the finding is unexplained from 157 to the end of the run (203).
  That span covers the rest of the walk (last step 172) and the idle stand. The run holds no unexplained tick while
  a task the robot models is on the human's stack.

![figure](scenario_s08_01/figure.png)

Script actions (replay expanded per tick; the first tick of each action):

| tick | task | action | occurrence |
|---|---|---|---|
| 0 | deliver item_1 | move_to | 0 |
| 30 | deliver item_1 | pick_up | 0 |
| 32 | deliver item_1 | move_to | 1 |
| 61 | deliver item_1 | place | 0 |
| 63 | deliver item_2 | move_to | 0 |
| 93 | deliver item_2 | pick_up | 0 |
| 95 | deliver item_2 | move_to | 1 |
| 124 | deliver item_2 | place | 0 |
| 126 | go_to(?landmark=corner_SE) | move_to | 0 |

Last acknowledgement tick 173; idle from 174 to 203.

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break | move_to(?target=coffee_machine_0) | -1 to 203 |
| deliver item_1 | move_to(?target=item_1) | -1 to 27 |
| deliver item_1 | pick_up(?item=item_1) | 28 to 29 |
| deliver item_1 | move_to(?target=kitting_table_0) | 30 to 58 |
| deliver item_1 | place(?item=item_1,?target=kitting_table_0) | 59 to 60 |
| deliver item_2 | move_to(?target=item_2) | -1 to 29 |
| deliver item_2 | place(?item=item_1,?target=shelf_1) | 30 to 31 |
| deliver item_2 | move_to(?target=shelf_1) | 32 to 60 |
| deliver item_2 | move_to(?target=item_2) | 61 to 90 |
| deliver item_2 | pick_up(?item=item_2) | 91 to 92 |
| deliver item_2 | move_to(?target=kitting_table_0) | 93 to 121 |
| deliver item_2 | place(?item=item_2,?target=kitting_table_0) | 122 to 123 |

Events (actual):

| tick | event |
|---|---|
| 61 | boundary |
| 61 | pin deliver item_1 |
| 124 | boundary |
| 124 | pin deliver item_2 |

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver item_1 | 0 to 62 | 25 | 0.7552 | yes | adequate |
| deliver item_2 | 63 to 125 | 76 | 0.7560 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver item_2 | move_to(?target=item_2) | 0.0315 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver item_1 |
| 34 | coffee_break | move_to(?target=coffee_machine_0) | 0.0579 | 0.0451 | 345.0 | 285.0 | 60.0 | deliver item_1 |
| 41 | deliver item_2 | move_to(?target=shelf_1) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver item_1 |
| 86 | coffee_break | move_to(?target=coffee_machine_0) | 0.0582 | 0.0453 | 344.4 | 344.4 | 0.0 | deliver item_2 |
| 157 | coffee_break | move_to(?target=coffee_machine_0) | 0.9980 | 0.0456 | 343.9 | 343.9 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver item_1 |
| 61 | adequate | unresolved | deliver item_1 |
| 62 | unresolved | adequate | deliver item_1 |
| 124 | adequate | unresolved | deliver item_2 |
| 125 | unresolved | adequate | deliver item_2 |
| 157 | adequate | unexplained | - |

Exit walk (go_to corner_SE): first step 126, last step 172, acknowledgement 173; the idle human from 174. Live at its first tick: coffee_break.

- coffee_break: belief 0.9980 at 126; S < α from 157 (belief 0.9980; v·D 343.9 cm); the finding unexplained from 157.


### scenario_s08_02

**Comparison:** 0 disagreements (281 ticks, 395 hypothesis rows). **Trends (actual):**
- **deliver item_1.** As in _01 up to its boundary at 61: θ first reached at 25; deliver item_2 below α at 14 and 41;
  coffee_break below α at 34.
- **The coffee_break.** After the boundary at 61, coffee_break and deliver item_2 start at 0.4995 each. coffee_break
  first reaches θ at 75, on its walk to the machine, and deliver item_2's S falls below α at 84 (e 350 cm).
- **The coffee pin at 133** (the last STAND of its wait; a boundary). From 133 deliver item_2 is the lone live
  hypothesis at 0.998, the value at its first truth tick (135). Unresolved at 133, adequate from 134.
- **The second delivery's pin at 201** is a boundary, and the lifecycle is exhausted from 201. There is no finding on
  the rest of the delivery's acknowledgement, on the exit walk (203 to 250) or on the idle stand.

![figure](scenario_s08_02/figure.png)

Script actions (replay expanded per tick; the first tick of each action):

| tick | task | action | occurrence |
|---|---|---|---|
| 0 | deliver item_1 | move_to | 0 |
| 30 | deliver item_1 | pick_up | 0 |
| 32 | deliver item_1 | move_to | 1 |
| 61 | deliver item_1 | place | 0 |
| 63 | coffee_break | move_to | 0 |
| 104 | coffee_break | wait_at | 0 |
| 135 | deliver item_2 | move_to | 0 |
| 169 | deliver item_2 | pick_up | 0 |
| 171 | deliver item_2 | move_to | 1 |
| 201 | deliver item_2 | place | 0 |
| 203 | go_to(?landmark=corner_SE) | move_to | 0 |

Last acknowledgement tick 250; idle from 251 to 280.

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break | move_to(?target=coffee_machine_0) | -1 to 101 |
| coffee_break | wait_at(?duration=PT60S,?entity=coffee_machine_0) | 102 to 132 |
| deliver item_1 | move_to(?target=item_1) | -1 to 27 |
| deliver item_1 | pick_up(?item=item_1) | 28 to 29 |
| deliver item_1 | move_to(?target=kitting_table_0) | 30 to 58 |
| deliver item_1 | place(?item=item_1,?target=kitting_table_0) | 59 to 60 |
| deliver item_2 | move_to(?target=item_2) | -1 to 29 |
| deliver item_2 | place(?item=item_1,?target=shelf_1) | 30 to 31 |
| deliver item_2 | move_to(?target=shelf_1) | 32 to 60 |
| deliver item_2 | move_to(?target=item_2) | 61 to 166 |
| deliver item_2 | pick_up(?item=item_2) | 167 to 168 |
| deliver item_2 | move_to(?target=kitting_table_0) | 169 to 198 |
| deliver item_2 | place(?item=item_2,?target=kitting_table_0) | 199 to 200 |

Events (actual):

| tick | event |
|---|---|
| 61 | boundary |
| 61 | pin deliver item_1 |
| 133 | boundary |
| 133 | pin coffee_break |
| 201 | boundary |
| 201 | exhausted (no live hypothesis) from here |
| 201 | pin deliver item_2 |

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver item_1 | 0 to 62 | 25 | 0.7552 | yes | adequate |
| coffee_break | 63 to 134 | 75 | 0.7552 | yes | adequate |
| deliver item_2 | 135 to 202 | 135 | 0.9980 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver item_2 | move_to(?target=item_2) | 0.0315 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver item_1 |
| 34 | coffee_break | move_to(?target=coffee_machine_0) | 0.0579 | 0.0451 | 345.0 | 285.0 | 60.0 | deliver item_1 |
| 41 | deliver item_2 | move_to(?target=shelf_1) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver item_1 |
| 84 | deliver item_2 | move_to(?target=item_2) | 0.0554 | 0.0430 | 349.9 | 349.9 | 0.0 | coffee_break |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver item_1 |
| 61 | adequate | unresolved | deliver item_1 |
| 62 | unresolved | adequate | deliver item_1 |
| 133 | adequate | unresolved | coffee_break |
| 134 | unresolved | adequate | coffee_break |
| 201 | adequate | exhausted | deliver item_2 |

Exit walk (go_to corner_SE): first step 203, last step 249, acknowledgement 250; the idle human from 251. Live at its first tick: none (exhausted).


### scenario_s08_03

**Comparison:** 0 disagreements (271 ticks, 402 hypothesis rows). **Trends (actual):**
- **deliver item_1 before the coffee.** It first reaches θ at 25, and its grasp is at 30. The coffee_break starts at
  32 with item_1 in hand.
- **The walk to the machine** (32 to about 52; arrival advances coffee_break to `wait_at` at 53):
  - deliver item_1 is `deliver_already_held` and expects `move_to(kitting_table_0)` from 30 to 124, one derived
    phase across the break. Its S falls below α at 43 (e 348 cm), at belief 0.312.
  - deliver item_2 is in its return (`move_to(shelf_1)` from 33) and falls below α at 42.
  - coffee_break first reaches θ at 45 (0.804). Its S stays at 0.0988 from 31 to 52: the excess it gathered during
    the walk to the shelf and the standing there, with the straight walk at the machine adding none. It reads 1 from
    53, in `wait_at`.
  - The finding stays adequate throughout.
- **The coffee pin at 84** (a boundary). Both deliveries go to 0.4995. Unresolved at 84, adequate from 85.
- **The resumption at 86** re-expands the carry to the table (the delivery's phase, unchanged): deliver item_1 first
  reaches θ again at 100 (0.778), and deliver item_2 falls below α at 107.
- **deliver item_1's pin at 127** (a boundary) leaves deliver item_2 lone at 0.998.
- **Exhaustion.** deliver item_2's pin at 191 exhausts the lifecycle, and the exit walk (193 to 240) has no finding.

![figure](scenario_s08_03/figure.png)

Script actions (replay expanded per tick; the first tick of each action):

| tick | task | action | occurrence |
|---|---|---|---|
| 0 | deliver item_1 | move_to | 0 |
| 30 | deliver item_1 | pick_up | 0 |
| 32 | coffee_break | move_to | 0 |
| 55 | coffee_break | wait_at | 0 |
| 86 | deliver item_1 | move_to | 0 |
| 127 | deliver item_1 | place | 0 |
| 129 | deliver item_2 | move_to | 0 |
| 159 | deliver item_2 | pick_up | 0 |
| 161 | deliver item_2 | move_to | 1 |
| 191 | deliver item_2 | place | 0 |
| 193 | go_to(?landmark=corner_SE) | move_to | 0 |

Last acknowledgement tick 240; idle from 241 to 270.

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break | move_to(?target=coffee_machine_0) | -1 to 52 |
| coffee_break | wait_at(?duration=PT60S,?entity=coffee_machine_0) | 53 to 83 |
| deliver item_1 | move_to(?target=item_1) | -1 to 27 |
| deliver item_1 | pick_up(?item=item_1) | 28 to 29 |
| deliver item_1 | move_to(?target=kitting_table_0) | 30 to 124 |
| deliver item_1 | place(?item=item_1,?target=kitting_table_0) | 125 to 126 |
| deliver item_2 | move_to(?target=item_2) | -1 to 29 |
| deliver item_2 | place(?item=item_1,?target=shelf_1) | 30 to 32 |
| deliver item_2 | move_to(?target=shelf_1) | 33 to 126 |
| deliver item_2 | move_to(?target=item_2) | 127 to 156 |
| deliver item_2 | pick_up(?item=item_2) | 157 to 158 |
| deliver item_2 | move_to(?target=kitting_table_0) | 159 to 188 |
| deliver item_2 | place(?item=item_2,?target=kitting_table_0) | 189 to 190 |

Events (actual):

| tick | event |
|---|---|
| 84 | boundary |
| 84 | pin coffee_break |
| 127 | boundary |
| 127 | pin deliver item_1 |
| 191 | boundary |
| 191 | exhausted (no live hypothesis) from here |
| 191 | pin deliver item_2 |

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver item_1 | 0 to 31 | 25 | 0.7552 | yes | adequate |
| coffee_break | 32 to 85 | 45 | 0.8044 | yes | adequate |
| deliver item_1 | 86 to 128 | 100 | 0.7779 | yes | adequate |
| deliver item_2 | 129 to 192 | 129 | 0.9980 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver item_2 | move_to(?target=item_2) | 0.0315 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver item_1 |
| 42 | deliver item_2 | move_to(?target=shelf_1) | 0.0010 | 0.0422 | 351.8 | 351.8 | 0.0 | coffee_break |
| 43 | deliver item_1 | move_to(?target=kitting_table_0) | 0.3117 | 0.0440 | 347.5 | 347.5 | 0.0 | coffee_break |
| 107 | deliver item_2 | move_to(?target=shelf_1) | 0.0553 | 0.0429 | 350.0 | 350.0 | 0.0 | deliver item_1 |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver item_1 |
| 84 | adequate | unresolved | coffee_break |
| 85 | unresolved | adequate | coffee_break |
| 127 | adequate | unresolved | deliver item_1 |
| 128 | unresolved | adequate | deliver item_1 |
| 191 | adequate | exhausted | deliver item_2 |

Across the coffee boundary (actual): the coffee_break starts at 32 (its walk), is pinned at 84 (the boundary), and the suspended delivery resumes at 86.

| tick | human action | truth | coffee_break belief / S | deliver item_1 belief / S | deliver item_2 belief / S | finding |
|---|---|---|---|---|---|---|
| 30 | pick_up grasp | deliver item_1 | 0.1374 / 0.1199 | 0.8616 / 1.0000 | 0.0010 / 1.0000 | adequate |
| 31 | pick_up  | deliver item_1 | 0.1169 / 0.0989 | 0.8821 / 1.0000 | 0.0010 / 1.0000 | adequate |
| 32 | move_to step | coffee_break | 0.1319 / 0.0989 | 0.8671 / 0.8248 | 0.0010 / 1.0000 | adequate |
| 33 | move_to step | coffee_break | 0.1511 / 0.0989 | 0.8479 / 0.6702 | 0.0010 / - | adequate |
| 34 | move_to step | coffee_break | 0.1756 / 0.0989 | 0.8234 / 0.5366 | 0.0010 / 0.7594 | adequate |
| 83 | wait_at stand | coffee_break | 0.9980 / 1.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | adequate |
| 84 | wait_at stand | coffee_break | retired | 0.4995 / - | 0.4995 / - | unresolved |
| 85 | wait_at  | coffee_break | retired | 0.4995 / 1.0000 | 0.4995 / 1.0000 | adequate |
| 86 | move_to step | deliver item_1 | retired | 0.5076 / 1.0000 | 0.4914 / 0.9544 | adequate |
| 87 | move_to step | deliver item_1 | retired | 0.5167 / 1.0000 | 0.4823 / 0.9068 | adequate |
| 88 | move_to step | deliver item_1 | retired | 0.5269 / 1.0000 | 0.4721 / 0.8571 | adequate |

Exit walk (go_to corner_SE): first step 193, last step 239, acknowledgement 240; the idle human from 241. Live at its first tick: none (exhausted).


### scenario_s08_04

**Comparison:** 0 disagreements (282 ticks, 423 hypothesis rows). **Trends (actual):**
- **deliver item_1 before the coffee.** It first reaches θ at 25. Its walk to shelf_1 is acknowledged at 29, and the
  coffee_break starts at 30, empty-handed at the shelf.
- **Leaving the shelf.** deliver item_1 had advanced to `pick_up` at 28. As the human leaves the shelf, `at` stops
  holding and the hypothesis regresses to `move_to(item_1)` at 31, a phase that runs 31 to 103 across the break. Its
  entry tick 31 holds no observation (s_exp 0, nothing walked yet). Its S falls below α at 40 (e 352 cm), at belief
  0.231, the tick coffee_break first reaches θ (0.768).
- **The coffee_break.** Its S is 0.1451 from 29 to 50 (the same reading as in _03, with no walk away first), and 1
  from 51, in `wait_at`.
- **The coffee pin at 82** (a boundary). Both deliveries go to 0.4995. Unresolved at 82, adequate from 83.
- **The resumption at 84** walks back to shelf_1: deliver item_1 first reaches θ again at 91 (0.785), and deliver
  item_2 falls below α at 97 (e 345 cm). After the grasp (104 to 105) item_2 is in its return (`move_to(shelf_1)`
  from 109) and falls below α again at 118.
- **deliver item_1's pin at 139** (a boundary) leaves deliver item_2 lone at 0.998.
- **Exhaustion.** deliver item_2's pin at 202 exhausts the lifecycle, and the exit walk (204 to 251) has no finding.

![figure](scenario_s08_04/figure.png)

Script actions (replay expanded per tick; the first tick of each action):

| tick | task | action | occurrence |
|---|---|---|---|
| 0 | deliver item_1 | move_to | 0 |
| 30 | coffee_break | move_to | 0 |
| 53 | coffee_break | wait_at | 0 |
| 84 | deliver item_1 | move_to | 0 |
| 106 | deliver item_1 | pick_up | 0 |
| 108 | deliver item_1 | move_to | 1 |
| 139 | deliver item_1 | place | 0 |
| 141 | deliver item_2 | move_to | 0 |
| 171 | deliver item_2 | pick_up | 0 |
| 173 | deliver item_2 | move_to | 1 |
| 202 | deliver item_2 | place | 0 |
| 204 | go_to(?landmark=corner_SE) | move_to | 0 |

Last acknowledgement tick 251; idle from 252 to 281.

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break | move_to(?target=coffee_machine_0) | -1 to 50 |
| coffee_break | wait_at(?duration=PT60S,?entity=coffee_machine_0) | 51 to 81 |
| deliver item_1 | move_to(?target=item_1) | -1 to 27 |
| deliver item_1 | pick_up(?item=item_1) | 28 to 30 |
| deliver item_1 | move_to(?target=item_1) | 31 to 103 |
| deliver item_1 | pick_up(?item=item_1) | 104 to 105 |
| deliver item_1 | move_to(?target=kitting_table_0) | 106 to 136 |
| deliver item_1 | place(?item=item_1,?target=kitting_table_0) | 137 to 138 |
| deliver item_2 | move_to(?target=item_2) | -1 to 105 |
| deliver item_2 | place(?item=item_1,?target=shelf_1) | 106 to 108 |
| deliver item_2 | move_to(?target=shelf_1) | 109 to 138 |
| deliver item_2 | move_to(?target=item_2) | 139 to 168 |
| deliver item_2 | pick_up(?item=item_2) | 169 to 170 |
| deliver item_2 | move_to(?target=kitting_table_0) | 171 to 199 |
| deliver item_2 | place(?item=item_2,?target=kitting_table_0) | 200 to 201 |

Events (actual):

| tick | event |
|---|---|
| 82 | boundary |
| 82 | pin coffee_break |
| 139 | boundary |
| 139 | pin deliver item_1 |
| 202 | boundary |
| 202 | exhausted (no live hypothesis) from here |
| 202 | pin deliver item_2 |

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver item_1 | 0 to 29 | 25 | 0.7552 | yes | adequate |
| coffee_break | 30 to 83 | 40 | 0.7678 | yes | adequate |
| deliver item_1 | 84 to 140 | 91 | 0.7854 | yes | adequate |
| deliver item_2 | 141 to 203 | 141 | 0.9980 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver item_2 | move_to(?target=item_2) | 0.0315 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver item_1 |
| 40 | deliver item_1 | move_to(?target=item_1) | 0.2312 | 0.0422 | 351.8 | 351.8 | 0.0 | coffee_break |
| 97 | deliver item_2 | move_to(?target=item_2) | 0.0578 | 0.0450 | 345.2 | 345.2 | 0.0 | deliver item_1 |
| 118 | deliver item_2 | move_to(?target=shelf_1) | 0.0010 | 0.0395 | 358.3 | 358.3 | 0.0 | deliver item_1 |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver item_1 |
| 82 | adequate | unresolved | coffee_break |
| 83 | unresolved | adequate | coffee_break |
| 139 | adequate | unresolved | deliver item_1 |
| 140 | unresolved | adequate | deliver item_1 |
| 202 | adequate | exhausted | deliver item_2 |

Across the coffee boundary (actual): the coffee_break starts at 30 (its walk), is pinned at 82 (the boundary), and the suspended delivery resumes at 84.

| tick | human action | truth | coffee_break belief / S | deliver item_1 belief / S | deliver item_2 belief / S | finding |
|---|---|---|---|---|---|---|
| 28 | move_to step | deliver item_1 | 0.1861 / 0.1754 | 0.8129 / 1.0000 | 0.0010 / 0.0005 | adequate |
| 29 | move_to  | deliver item_1 | 0.1605 / 0.1451 | 0.8385 / 1.0000 | 0.0010 / 0.0004 | adequate |
| 30 | move_to step | coffee_break | 0.1605 / 0.1451 | 0.8385 / 1.0000 | 0.0010 / 0.0004 | adequate |
| 31 | move_to step | coffee_break | 0.1605 / 0.1451 | 0.8385 / - | 0.0010 / 0.0004 | adequate |
| 32 | move_to step | coffee_break | 0.1893 / 0.1451 | 0.8097 / 0.7594 | 0.0010 / 0.0003 | adequate |
| 81 | wait_at stand | coffee_break | 0.9980 / 1.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | adequate |
| 82 | wait_at stand | coffee_break | retired | 0.4995 / - | 0.4995 / - | unresolved |
| 83 | wait_at  | coffee_break | retired | 0.4995 / 1.0000 | 0.4995 / 1.0000 | adequate |
| 84 | move_to step | deliver item_1 | retired | 0.5273 / 1.0000 | 0.4717 / 0.8554 | adequate |
| 85 | move_to step | deliver item_1 | retired | 0.5585 / 1.0000 | 0.4405 / 0.7235 | adequate |
| 86 | move_to step | deliver item_1 | retired | 0.5928 / 1.0000 | 0.4062 / 0.6050 | adequate |

Exit walk (go_to corner_SE): first step 204, last step 250, acknowledgement 251; the idle human from 252. Live at its first tick: none (exhausted).


## The recognizer behaves this way, and what that says about the design

- **What the agreement establishes.** Every compared output of the recognizer, on every tick of four runs, equals
  what the records at HEAD specify, as read with R1 to R4. So "the recognizer behaves this way" and "this is what the
  current records prescribe" coincide for every public output compared here.
- **What it does not establish.**
  - It is not evidence that the design is right.
  - It is not evidence for the private state (the expected action and the origin), which is not independently
    validated (option B).
  - It says nothing about E8's clause, which these scenarios do not exercise (see "The instrument can fail").
- **Behaviours that follow from the records, stated as such, not ruled on:**
  1. **The rival delivery after a grasp.** It is measured against a return of the carried item to its home shelf
     (`deliver_with_return`), not against its own item: first `place(item_1, shelf_1)`, with no progress evaluator
     (e = 0), then, once `at(shelf_1)` stops holding, `move_to(shelf_1)` (_01 ticks 30 to 60; the same in every
     scenario).
  2. **Standing charged to a walk.** Standing at a shelf is charged against a rival's open walk phase with s_exp 0
     (coffee_break in _01 and _02 at 34: 60 cm of its 345).
  3. **The sequence at a boundary.** Each boundary gives unresolved (b), then adequate (b + 1), as recorded in 1.5c
     (8 boundaries with a live successor: 61 and 124 in _01; 61 and 133 in _02; 84 and 127 in _03; 82 and 139 in
     _04). The other three boundaries (201, 191, 202) exhaust the lifecycle.
  4. **A lone live hypothesis.** It reads 0.998 at once, by normalisation (R1): deliver item_2 from the coffee pin
     in _02, from deliver item_1's pin in _03 and _04, and coffee_break from 124 in _01.
  5. **The finding is existential.** While a true coffee_break is adequate, a delivery whose S is below α leaves the
     finding adequate (_03 from 43, _04 from 40).

## _03 and _04: mechanical, L not resolved

_03 and _04 test suspended task states, which are L's subject. Their expectations are generated mechanically from
the current records. Among them:

- the delivery's derived phase spans the break (_03: `move_to(kitting_table_0)` from 30 to 124; _04:
  `move_to(item_1)` from 31 to 103);
- the coffee pin is an episode boundary that resets both deliveries to 0.4995;
- in _04, the regress at the proximity threshold as the human leaves the shelf.

The recognizer agrees with each of these. Whether any of them is what L should prescribe is not answered here.

## The coffee retirement

- **_02, _03, _04.** coffee_break is pinned when `waited` first holds, on the last STAND of its wait: 133 (_02),
  84 (_03), 82 (_04), each a boundary. It stays retired for the run. The second delivery's pin then leaves no
  hypothesis live: the lifecycle is exhausted from 201 (_02), 191 (_03) and 202 (_04), including the exit walk (first
  step 203, 193, 204; acknowledgement 250, 240, 251) and the idle stand. No finding is reported on those ticks
  (80 ticks in each).
- **_01.** coffee_break is never pinned. After deliver item_2's pin at 124 it is the lone live hypothesis, at 0.998.
  Its phase is still the `move_to(coffee_machine_0)` it has expected since tick −1, with its origin moved at each
  boundary. On the exit walk (126 to 172) its excess grows: S falls below α at 157 (v·D 344 cm, all excess), and the
  finding is unexplained from 157 to 203. That span is 47 ticks: the rest of the walk and the 30 ticks of the idle
  human. This is TODO-117's case by construction, as the entry states.

## Runs and tests that disagree with the mechanism

- **The four test-bed runs.** None: 0 disagreements against the records as read.
- **`tests/test_tl2_discovery.py::test_the_registry_is_the_union_of_the_modules`.** It failed on the new artefacts
  because it pins the registry's inventory as a literal (38 scenarios, setups 01 to 07). That is an inventory count,
  not a mechanism. It was updated to 42 scenarios and setups 01 to 08 in the artefacts commit, and the full suite
  passes (135).
- **The maintained baselines.** The tb1a sweep (the five regression fixtures and the three evaluation fixtures, both
  priors: 16 logs and their `.rec`) is byte-identical to its README's IRB.2b section, 32 of 32 md5s. No code on the
  run path changed.

## What the records leave undetermined, and what the instrument decided

- **For the oracle:** the readings R1 to R4 (README), confirmed by Hadi at the plan step. No other choice was needed:
  every value compared follows from the records and the domain's structure.
- **Choices of the instrument, not of the oracle.** None of them feeds a compared value.
  - The oracle's world holds only the observed human's facts. No hypothesis of the human reads the robot's.
  - `AgentState.current_zone` is "unknown", which the decomposition does not read.
  - Tick −1 is not compared (R4).
  - In the trends, the truth on an acknowledgement tick is the acknowledged action's task.
  - In the trends, v·D is recovered from the actual S.

## Flags (outside scope, not fixed)

1. **`analysis/td_stage1b/tdlib.py`.** Its `[coverage]` pattern does not match a `[coverage]` line with a `start:`
   entry (any script with a `Start` event), and `parse` then raises. `actual.py` works around it by handing tdlib the
   log without those lines. tdlib is a frozen record, so it is not edited.
2. **E8 is not exercised independently** by any of the four scenarios (above). Under E9's latency pricing and E6's
   second amendment, E8's clause adds a member only where an advance opens a phase with s_exp = 0. That would need a
   completion latency of 0, which Mesa does not have. A design question for a cycle, if wanted; not a disagreement.
3. **The inventory literal in `test_tl2_discovery.py`** must be edited with every new scenario or setup.

---

# IRB.4b: the enlarged room, twelve scenarios

The section above is IRB.3b's report on env_layout_10, unchanged. This section is IRB.4b's: the enlarged room
`env_layout_11` with `env_setup_09`, and the twelve scenarios of `scenarios_s09.py`, run through the instrument made
independent of the layout (`README.md`, "IRB.4b"). Prior ON in every run; α = 0.05; θ = 0.75 (the meta-planner's,
marked for reference only). 27 September 2026.

**What the comparison validates.** Under B the comparison validates the recognizer's public outputs against the
independent oracle; the recognizer's private expected action and origin are not independently validated, by choice.

## The geometry: shelf_3's position, chosen for observability

- **The criterion, stated before any run.** In _10, on the walk to item_1 (the only place both west deliveries are
  rivals), the rival delivery of item_3 is refuted (S < α, from the oracle) after the first quarter of the walk's
  ticks and before its arrival: separated within the walk, neither at the first steps nor only at the shelves.
- **Tried: (−420, −220)**, on the west wall 200 cm below shelf_1, 10.4° from it (the planned position). Shallow run 1
  (trajectory and oracle only): the walk's arrival is tick 28 and its first quarter ends at 7. The rival's S is 0.976
  at 7, 0.943 at 14, 0.886 at 21 and 0.765 at 28 (excess 35.8 cm); it falls below α only at 41, on the carry after the
  grasp. Not met.
- **Kept: (−420, 300)**, on the west wall 320 cm above shelf_1: bearing −164.1°, 30.4° from shelf_1, 62.3° from
  coffee_machine_0. An analytic screen up the west wall (straight-line excess on the body's walk) found (−420, 240)
  reaching the threshold only at the arrival tick, and (−420, 300) first before it. Shallow run 2: the rival's S is
  0.783 at 7, 0.463 at 14, 0.134 at 21, and falls below α at 25; at the arrival (28) it is 0.017 (excess 443.4 cm).
  Met.
- The position was chosen for the phenomenon's observability, never for a belief or finding value; the expectations
  were derived after it was fixed. The human of the IRB.3b scripts never comes within 221 cm of shelf_3 or 253 cm of
  kitting_table_1. On the twelve new scripts each new object is reached only where a script targets it
  (kitting_table_1 in _08; shelf_3 and item_3 in _09 to _11).

## Coverage labels (the loader's `[coverage]` and `[scenario-coverage]` lines, prior on)

| scenario | entries (coverage) | scenario coverage | decisions / triggers | description |
|---|---|---|---|---|
| s09_01 | deliver 1, deliver 2 covered; exit walk task_absent | modelled_only | - / - | agrees |
| s09_02 | deliver 1, coffee_break, deliver 2 covered | modelled_only | - / - | agrees |
| s09_03 | deliver 1 (start: coffee_break covered), deliver 2 covered | modelled_only | Start / AfterAction | agrees |
| s09_04 | as _03 | modelled_only | Start / AfterAction | agrees |
| s09_05 | deliver 1 (start: go_to(corner_SE) task_absent), deliver 2 covered | task_absent | Start / AfterAction | agrees: states the walk to corner_SE |
| s09_06 | deliver 1 (start: stand(PT80S) task_absent), deliver 2 covered | task_absent | Start / AfterAction | agrees: states the stand |
| s09_07 | deliver 1 (start: deliver 2 covered) | modelled_only | Start / AfterAction | agrees |
| s09_08 | deliver(item_1, kitting_table_1) binding_absent; deliver 2 covered | binding_absent | - / - | agrees: states the wrong-table delivery |
| s09_09 | deliver 1, deliver 3, deliver 2 covered | modelled_only | - / - | agrees: deliver 3 covered, outside the support (Q2) |
| s09_10 | deliver 1, deliver 3 covered | modelled_only | - / - | agrees |
| s09_11 | deliver 1, coffee_break, deliver 3 covered | modelled_only | - / - | agrees |
| s09_12 | deliver 2, deliver 1 covered | modelled_only | - / - | agrees |

Every script's last entry is the exit walk, `go_to(corner_SE)`, task_absent and exempt from scenario coverage. In _05
the same walk mid-script, started by an event, is counted.

## Results

- **The replay against the run:** equal on every tick in all twelve scenarios (position to the log's 2 decimals,
  action, micro). The trajectory's source is the replay throughout.
- **The in-process runs:** their `[IR*]` lines are byte-identical to the logged runs' in all twelve.
- **The independence assertion** held in every oracle process: neither `shared.recognizer` nor
  `shared.likelihood_functions` was loaded.

| scenario | ticks | (tick, live hypothesis) rows | disagreements vs actual.csv (1e-9) | vs actual_log.csv (print precision) | rows on one side only |
|---|---|---|---|---|---|
| s09_01 | 204 | 389 | 0 | 0 | 0 |
| s09_02 | 281 | 395 | 0 | 0 | 0 |
| s09_03 | 271 | 402 | 0 | 0 | 0 |
| s09_04 | 282 | 423 | 0 | 0 | 0 |
| s09_05 | 270 | 588 | 0 | 0 | 0 |
| s09_06 | 246 | 515 | 0 | 0 | 0 |
| s09_07 | 252 | 531 | 0 | 1 | 0 |
| s09_08 | 211 | 553 | 0 | 0 | 0 |
| s09_09 | 252 | 485 | 0 | 0 | 0 |
| s09_10 | 188 | 356 | 0 | 0 | 0 |
| s09_11 | 276 | 389 | 0 | 0 | 0 |
| s09_12 | 205 | 390 | 0 | 0 | 0 |

**Disagreements, classified.** There is one, in s09_07 at tick 35, against the log only: `coffee_break`'s hypothesis
adequacy, expected `inadequate`, read from the log as `adequate`.

- The recognizer's own output (the in-process `BeliefState`) is `inadequate`, with S = 0.0499824, equal to the
  oracle's at 1e-9.
- The log prints that S to four decimals as `0.0500`, and the log reader derives adequacy by comparing the printed
  value with α.
- Classified as a print-precision artefact of the log: the log does not determine a hypothesis adequacy whose S lies
  within 5·10⁻⁵ of α. It is none of the three classes, all of which concern the oracle, the records and the
  recognizer; the recognizer agrees with the records here.
- It is left in `diff.md` as found.

**A reader defect, found and fixed before the recorded outputs.** The first full run showed a row on one side only
at every tick of every scenario: the log reader took every key not yet pinned as live, `deliver_item(item_3)` (or
item_2 in _10 and _11) included. That hypothesis is outside the support: pinned at the floor and never live. The fix
makes the log reader's live set the support, from `[IR-prior]`'s known tasks plus every PersonalTask hypothesis
(handback §1.1). It concerned `actual_log.csv` only; the full-precision comparison showed 0 disagreements before and
after. Rerun, the s08 check below was unchanged.

**The check on the IRB.3b runs.** s08_01 to _04 were rerun through the changed instrument into another folder.

- **Byte-identical to the committed files:** the logs and `.rec` streams, and `trajectory.json`, `expected.csv`,
  `actual.csv`, `actual_log.csv`, `diff.md` and `phases.json`.
- **Differ in presentation only:** `figure.png` and `summary.md` (the generic labels; the added coverage and
  stack-depth columns, support line and event-table lines). Their numbers are unchanged.
- The committed s08 folders are untouched.

**s09_01 to _04 against s08_01 to _04.** The scripts are the same, re-authored on the enlarged room.

- Their `.rec` streams are byte-identical to s08's, and every event tick, finding transition and refutation tick is
  the same.
- The beliefs differ only by the output scaling of one more key at the floor, `deliver_item(item_3)`, outside the
  support: a lone live hypothesis reads 0.9970 instead of 0.9980, and the first-θ beliefs are 0.7544 instead of
  0.7552.

## Per scenario

Each section has a short descriptive paragraph, the figure, then the generated tables:

- the script's actions with their coverage;
- the expected-action table (the oracle's derived phases, not validated against the recognizer's private state);
- the events, including the ticks the finding turns unexplained and back, the admissible hypotheses never pinned, and
  the lifecycle and finding on the last entry;
- the trends from `actual.csv`.

The truth on a tick is the hypothesis of the task on top of the stack, only when the loader judges that task covered.
For each deviation (_05 to _09) the section names the TODO it produces data for and states what the current records
determine and what they leave open. No mechanism is proposed.

### scenario_s09_01

The s08_01 script on the enlarged room. Every tick as in s08_01 (above): deliver_item(item_1) first reaches θ at 25 and
deliver_item(item_2) at 76. The boundaries fall at 61 and 124. From 124 coffee_break is the lone live hypothesis
(0.9970). Its S falls below α at 157 on the exit walk, and the finding is unexplained from 157 to the end (203).

![figure](scenario_s09_01/figure.png)

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 30 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 32 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 61 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 63 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 93 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 95 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 124 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 126 | go_to(corner_SE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 173; idle from 174 to 203. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 203 |
| deliver_item(item_1) | move_to(item_1) | -1 to 27 |
| deliver_item(item_1) | pick_up(item_1) | 28 to 29 |
| deliver_item(item_1) | move_to(kitting_table_0) | 30 to 58 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 59 to 60 |
| deliver_item(item_2) | move_to(item_2) | -1 to 29 |
| deliver_item(item_2) | place(item_1,shelf_1) | 30 to 31 |
| deliver_item(item_2) | move_to(shelf_1) | 32 to 60 |
| deliver_item(item_2) | move_to(item_2) | 61 to 90 |
| deliver_item(item_2) | pick_up(item_2) | 91 to 92 |
| deliver_item(item_2) | move_to(kitting_table_0) | 93 to 121 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 122 to 123 |

Events (actual):

| tick | event |
|---|---|
| 61 | boundary |
| 61 | pin deliver_item(item_1) |
| 124 | boundary |
| 124 | pin deliver_item(item_2) |
| 157 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(corner_SE), ticks 126 to 173): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_1) | 0 to 62 | 25 | 0.7544 | yes | adequate |
| deliver_item(item_2) | 63 to 125 | 76 | 0.7553 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver_item(item_2) | move_to(item_2) | 0.0315 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver_item(item_1) |
| 34 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0579 | 0.0451 | 345.0 | 285.0 | 60.0 | deliver_item(item_1) |
| 41 | deliver_item(item_2) | move_to(shelf_1) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 86 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0581 | 0.0453 | 344.4 | 344.4 | 0.0 | deliver_item(item_2) |
| 157 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9970 | 0.0456 | 343.9 | 343.9 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_1) |
| 61 | adequate | unresolved | deliver_item(item_1) |
| 62 | unresolved | adequate | deliver_item(item_1) |
| 124 | adequate | unresolved | deliver_item(item_2) |
| 125 | unresolved | adequate | deliver_item(item_2) |
| 157 | adequate | unexplained | - |

The last entry (go_to(corner_SE)): first step 126, last step 172, acknowledgement 173; the idle human from 174. Live at its first tick: coffee_break(coffee_machine_0).

- coffee_break(coffee_machine_0): belief 0.9970 at 126; S < α from 157 (belief 0.9970; v·D 343.9 cm); the finding unexplained from 157.


### scenario_s09_02

The s08_02 script on the enlarged room. Every tick as in s08_02: coffee_break first reaches θ at 75. Its pin at 133 is
a boundary, and deliver_item(item_2)'s pin at 201 exhausts the lifecycle. The exit walk (203 to 250) and the idle stand
have no finding.

![figure](scenario_s09_02/figure.png)

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 30 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 32 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 61 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 63 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 1 |
| 104 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 1 |
| 135 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 169 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 171 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 201 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 203 | go_to(corner_SE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 250; idle from 251 to 280. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 101 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 102 to 132 |
| deliver_item(item_1) | move_to(item_1) | -1 to 27 |
| deliver_item(item_1) | pick_up(item_1) | 28 to 29 |
| deliver_item(item_1) | move_to(kitting_table_0) | 30 to 58 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 59 to 60 |
| deliver_item(item_2) | move_to(item_2) | -1 to 29 |
| deliver_item(item_2) | place(item_1,shelf_1) | 30 to 31 |
| deliver_item(item_2) | move_to(shelf_1) | 32 to 60 |
| deliver_item(item_2) | move_to(item_2) | 61 to 166 |
| deliver_item(item_2) | pick_up(item_2) | 167 to 168 |
| deliver_item(item_2) | move_to(kitting_table_0) | 169 to 198 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 199 to 200 |

Events (actual):

| tick | event |
|---|---|
| 61 | boundary |
| 61 | pin deliver_item(item_1) |
| 133 | boundary |
| 133 | pin coffee_break(coffee_machine_0) |
| 201 | boundary |
| 201 | exhausted (no live hypothesis) from here |
| 201 | pin deliver_item(item_2) |

Never pinned: none. At the last entry (go_to(corner_SE), ticks 203 to 250): lifecycle and finding exhausted; on the idle ticks after it: exhausted.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_1) | 0 to 62 | 25 | 0.7544 | yes | adequate |
| coffee_break(coffee_machine_0) | 63 to 134 | 75 | 0.7544 | yes | adequate |
| deliver_item(item_2) | 135 to 202 | 135 | 0.9970 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver_item(item_2) | move_to(item_2) | 0.0315 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver_item(item_1) |
| 34 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0579 | 0.0451 | 345.0 | 285.0 | 60.0 | deliver_item(item_1) |
| 41 | deliver_item(item_2) | move_to(shelf_1) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 84 | deliver_item(item_2) | move_to(item_2) | 0.0553 | 0.0430 | 349.9 | 349.9 | 0.0 | coffee_break(coffee_machine_0) |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_1) |
| 61 | adequate | unresolved | deliver_item(item_1) |
| 62 | unresolved | adequate | deliver_item(item_1) |
| 133 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 134 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 201 | adequate | exhausted | deliver_item(item_2) |

The last entry (go_to(corner_SE)): first step 203, last step 249, acknowledgement 250; the idle human from 251. Live at its first tick: none (exhausted).


### scenario_s09_03

The s08_03 script on the enlarged room. Every tick as in s08_03: coffee_break first reaches θ at 45 on the walk to the
machine, with item_1 in hand; its pin at 84 is a boundary. deliver_item(item_1) resumes at 86 and first reaches θ again
at 100. The lifecycle is exhausted from 191. L's subject: the expectations are mechanical and L is not resolved.

![figure](scenario_s09_03/figure.png)

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 30 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 32 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 2 |
| 55 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 2 |
| 86 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 127 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 129 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 159 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 161 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 191 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 193 | go_to(corner_SE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 240; idle from 241 to 270. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 52 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 53 to 83 |
| deliver_item(item_1) | move_to(item_1) | -1 to 27 |
| deliver_item(item_1) | pick_up(item_1) | 28 to 29 |
| deliver_item(item_1) | move_to(kitting_table_0) | 30 to 124 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 125 to 126 |
| deliver_item(item_2) | move_to(item_2) | -1 to 29 |
| deliver_item(item_2) | place(item_1,shelf_1) | 30 to 32 |
| deliver_item(item_2) | move_to(shelf_1) | 33 to 126 |
| deliver_item(item_2) | move_to(item_2) | 127 to 156 |
| deliver_item(item_2) | pick_up(item_2) | 157 to 158 |
| deliver_item(item_2) | move_to(kitting_table_0) | 159 to 188 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 189 to 190 |

Events (actual):

| tick | event |
|---|---|
| 84 | boundary |
| 84 | pin coffee_break(coffee_machine_0) |
| 127 | boundary |
| 127 | pin deliver_item(item_1) |
| 191 | boundary |
| 191 | exhausted (no live hypothesis) from here |
| 191 | pin deliver_item(item_2) |

Never pinned: none. At the last entry (go_to(corner_SE), ticks 193 to 240): lifecycle and finding exhausted; on the idle ticks after it: exhausted.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_1) | 0 to 31 | 25 | 0.7544 | yes | adequate |
| coffee_break(coffee_machine_0) | 32 to 85 | 45 | 0.8036 | yes | adequate |
| deliver_item(item_1) | 86 to 128 | 100 | 0.7772 | yes | adequate |
| deliver_item(item_2) | 129 to 192 | 129 | 0.9970 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver_item(item_2) | move_to(item_2) | 0.0315 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver_item(item_1) |
| 42 | deliver_item(item_2) | move_to(shelf_1) | 0.0010 | 0.0422 | 351.8 | 351.8 | 0.0 | coffee_break(coffee_machine_0) |
| 43 | deliver_item(item_1) | move_to(kitting_table_0) | 0.3114 | 0.0440 | 347.5 | 347.5 | 0.0 | coffee_break(coffee_machine_0) |
| 107 | deliver_item(item_2) | move_to(shelf_1) | 0.0553 | 0.0429 | 350.0 | 350.0 | 0.0 | deliver_item(item_1) |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_1) |
| 84 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 85 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 127 | adequate | unresolved | deliver_item(item_1) |
| 128 | unresolved | adequate | deliver_item(item_1) |
| 191 | adequate | exhausted | deliver_item(item_2) |

Across the started task coffee_break(coffee_machine_0) (covered; actual): on top of the stack from 32 to 85, its hypothesis pinned at 84; the suspended task resumes at 86.

| tick | human action | truth | coffee_break(coffee_machine_0) belief / S | deliver_item(item_1) belief / S | deliver_item(item_2) belief / S | finding |
|---|---|---|---|---|---|---|
| 30 | pick_up grasp | deliver_item(item_1) | 0.1373 / 0.1199 | 0.8608 / 1.0000 | 0.0010 / 1.0000 | adequate |
| 31 | pick_up  | deliver_item(item_1) | 0.1167 / 0.0989 | 0.8813 / 1.0000 | 0.0010 / 1.0000 | adequate |
| 32 | move_to step | coffee_break(coffee_machine_0) | 0.1318 / 0.0989 | 0.8662 / 0.8248 | 0.0010 / 1.0000 | adequate |
| 33 | move_to step | coffee_break(coffee_machine_0) | 0.1510 / 0.0989 | 0.8470 / 0.6702 | 0.0010 / - | adequate |
| 34 | move_to step | coffee_break(coffee_machine_0) | 0.1754 / 0.0989 | 0.8226 / 0.5366 | 0.0010 / 0.7594 | adequate |
| 83 | wait_at stand | coffee_break(coffee_machine_0) | 0.9970 / 1.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | adequate |
| 84 | wait_at stand | coffee_break(coffee_machine_0) | retired | 0.4990 / - | 0.4990 / - | unresolved |
| 85 | wait_at  | coffee_break(coffee_machine_0) | retired | 0.4990 / 1.0000 | 0.4990 / 1.0000 | adequate |
| 86 | move_to step | deliver_item(item_1) | retired | 0.5071 / 1.0000 | 0.4909 / 0.9544 | adequate |
| 87 | move_to step | deliver_item(item_1) | retired | 0.5162 / 1.0000 | 0.4818 / 0.9068 | adequate |
| 88 | move_to step | deliver_item(item_1) | retired | 0.5264 / 1.0000 | 0.4716 / 0.8571 | adequate |

The last entry (go_to(corner_SE)): first step 193, last step 239, acknowledgement 240; the idle human from 241. Live at its first tick: none (exhausted).


### scenario_s09_04

The s08_04 script on the enlarged room. Every tick as in s08_04: deliver_item(item_1) regresses to `move_to(item_1)`
at 31 as the human leaves the shelf empty-handed. coffee_break first reaches θ at 40; its pin at 82 is a boundary. The
resumed delivery first reaches θ again at 91, and the lifecycle is exhausted from 202. L's subject: the expectations
are mechanical and L is not resolved.

![figure](scenario_s09_04/figure.png)

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 30 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 2 |
| 53 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 2 |
| 84 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 106 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 108 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 139 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 141 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 171 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 173 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 202 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 204 | go_to(corner_SE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 251; idle from 252 to 281. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 50 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 51 to 81 |
| deliver_item(item_1) | move_to(item_1) | -1 to 27 |
| deliver_item(item_1) | pick_up(item_1) | 28 to 30 |
| deliver_item(item_1) | move_to(item_1) | 31 to 103 |
| deliver_item(item_1) | pick_up(item_1) | 104 to 105 |
| deliver_item(item_1) | move_to(kitting_table_0) | 106 to 136 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 137 to 138 |
| deliver_item(item_2) | move_to(item_2) | -1 to 105 |
| deliver_item(item_2) | place(item_1,shelf_1) | 106 to 108 |
| deliver_item(item_2) | move_to(shelf_1) | 109 to 138 |
| deliver_item(item_2) | move_to(item_2) | 139 to 168 |
| deliver_item(item_2) | pick_up(item_2) | 169 to 170 |
| deliver_item(item_2) | move_to(kitting_table_0) | 171 to 199 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 200 to 201 |

Events (actual):

| tick | event |
|---|---|
| 82 | boundary |
| 82 | pin coffee_break(coffee_machine_0) |
| 139 | boundary |
| 139 | pin deliver_item(item_1) |
| 202 | boundary |
| 202 | exhausted (no live hypothesis) from here |
| 202 | pin deliver_item(item_2) |

Never pinned: none. At the last entry (go_to(corner_SE), ticks 204 to 251): lifecycle and finding exhausted; on the idle ticks after it: exhausted.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_1) | 0 to 29 | 25 | 0.7544 | yes | adequate |
| coffee_break(coffee_machine_0) | 30 to 83 | 40 | 0.7671 | yes | adequate |
| deliver_item(item_1) | 84 to 140 | 91 | 0.7846 | yes | adequate |
| deliver_item(item_2) | 141 to 203 | 141 | 0.9970 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver_item(item_2) | move_to(item_2) | 0.0315 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver_item(item_1) |
| 40 | deliver_item(item_1) | move_to(item_1) | 0.2309 | 0.0422 | 351.8 | 351.8 | 0.0 | coffee_break(coffee_machine_0) |
| 97 | deliver_item(item_2) | move_to(item_2) | 0.0577 | 0.0450 | 345.2 | 345.2 | 0.0 | deliver_item(item_1) |
| 118 | deliver_item(item_2) | move_to(shelf_1) | 0.0010 | 0.0395 | 358.3 | 358.3 | 0.0 | deliver_item(item_1) |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_1) |
| 82 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 83 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 139 | adequate | unresolved | deliver_item(item_1) |
| 140 | unresolved | adequate | deliver_item(item_1) |
| 202 | adequate | exhausted | deliver_item(item_2) |

Across the started task coffee_break(coffee_machine_0) (covered; actual): on top of the stack from 30 to 83, its hypothesis pinned at 82; the suspended task resumes at 84.

| tick | human action | truth | coffee_break(coffee_machine_0) belief / S | deliver_item(item_1) belief / S | deliver_item(item_2) belief / S | finding |
|---|---|---|---|---|---|---|
| 28 | move_to step | deliver_item(item_1) | 0.1859 / 0.1754 | 0.8121 / 1.0000 | 0.0010 / 0.0005 | adequate |
| 29 | move_to  | deliver_item(item_1) | 0.1603 / 0.1451 | 0.8377 / 1.0000 | 0.0010 / 0.0004 | adequate |
| 30 | move_to step | coffee_break(coffee_machine_0) | 0.1603 / 0.1451 | 0.8377 / 1.0000 | 0.0010 / 0.0004 | adequate |
| 31 | move_to step | coffee_break(coffee_machine_0) | 0.1603 / 0.1451 | 0.8377 / - | 0.0010 / 0.0004 | adequate |
| 32 | move_to step | coffee_break(coffee_machine_0) | 0.1891 / 0.1451 | 0.8089 / 0.7594 | 0.0010 / 0.0003 | adequate |
| 81 | wait_at stand | coffee_break(coffee_machine_0) | 0.9970 / 1.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | adequate |
| 82 | wait_at stand | coffee_break(coffee_machine_0) | retired | 0.4990 / - | 0.4990 / - | unresolved |
| 83 | wait_at  | coffee_break(coffee_machine_0) | retired | 0.4990 / 1.0000 | 0.4990 / 1.0000 | adequate |
| 84 | move_to step | deliver_item(item_1) | retired | 0.5268 / 1.0000 | 0.4712 / 0.8554 | adequate |
| 85 | move_to step | deliver_item(item_1) | retired | 0.5579 / 1.0000 | 0.4401 / 0.7235 | adequate |
| 86 | move_to step | deliver_item(item_1) | retired | 0.5923 / 1.0000 | 0.4057 / 0.6050 | adequate |

The last entry (go_to(corner_SE)): first step 204, last step 250, acknowledgement 251; the idle human from 252. Live at its first tick: none (exhausted).


### scenario_s09_05

**The corner walk mid-delivery. Data for TODO-94** (a misleading walk inside an episode), and TODO-122.

After the grasp at 30, `go_to(corner_SE)` is on top from 32 to 79 (task_absent). The delivery resumes at 80 and
carries item_1 to the table.

- **deliver_item(item_1).** Its derived phase `move_to(kitting_table_0)` runs unbroken from 30 to 125, across the walk
  to the corner and the carry back. Its S falls below α at 48, 16 ticks into the corner walk (e 347 cm, belief 0.61).
- **The rivals.** deliver_item(item_2)'s S is already below α (41), and coffee_break's falls below it at 44.
- **The finding.** Unexplained from 48 to 125: through the rest of the corner walk (task_absent) and through the
  resumed carry (80 to 125, covered).
- **The belief during the resumed carry.** deliver_item(item_1) first reaches θ again at 87 (0.767) and rises to 0.997
  while its hypothesis adequacy stays `inadequate`. The finding returns to adequate at 126, when its phase advances to
  `place` (E8).

**What the current records determine.**
- A walk no hypothesis explains leaves the true hypothesis's phase open: no event ends it.
- The excess stays in that one derived phase until its advance (E1, E7), so the resumed task is inadequate until
  `place`.
- The belief is relative: it rises by the rivals' refutation (handback §1.9).

**What they leave open.** Whether the evidence of a misleading walk should be retracted, or a resumption reopen the
phase. That is L (retraction and resumption) and TODO-94's question.

![figure](scenario_s09_05/figure.png)

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 30 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 32 | go_to(corner_SE) | task_absent | move_to | 0 | 2 |
| 80 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 128 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 130 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 159 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 161 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 190 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 192 | go_to(corner_SE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 239; idle from 240 to 269. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 269 |
| deliver_item(item_1) | move_to(item_1) | -1 to 27 |
| deliver_item(item_1) | pick_up(item_1) | 28 to 29 |
| deliver_item(item_1) | move_to(kitting_table_0) | 30 to 125 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 126 to 127 |
| deliver_item(item_2) | move_to(item_2) | -1 to 29 |
| deliver_item(item_2) | place(item_1,shelf_1) | 30 to 31 |
| deliver_item(item_2) | move_to(shelf_1) | 32 to 127 |
| deliver_item(item_2) | move_to(item_2) | 128 to 156 |
| deliver_item(item_2) | pick_up(item_2) | 157 to 158 |
| deliver_item(item_2) | move_to(kitting_table_0) | 159 to 187 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 188 to 189 |

Events (actual):

| tick | event |
|---|---|
| 48 | finding turns unexplained |
| 126 | finding turns adequate (from unexplained) |
| 128 | boundary |
| 128 | pin deliver_item(item_1) |
| 190 | boundary |
| 190 | pin deliver_item(item_2) |
| 223 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(corner_SE), ticks 192 to 239): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_1) | 0 to 31 | 25 | 0.7544 | yes | adequate |
| deliver_item(item_1) | 80 to 129 | 87 | 0.7671 | yes | inadequate |
| deliver_item(item_2) | 130 to 191 | 143 | 0.7580 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver_item(item_2) | move_to(item_2) | 0.0315 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver_item(item_1) |
| 41 | deliver_item(item_2) | move_to(shelf_1) | 0.0010 | 0.0427 | 350.6 | 350.6 | 0.0 | - |
| 44 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.2906 | 0.0467 | 341.3 | 281.3 | 60.0 | - |
| 48 | deliver_item(item_1) | move_to(kitting_table_0) | 0.6104 | 0.0441 | 347.3 | 347.3 | 0.0 | - |
| 153 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0565 | 0.0440 | 347.5 | 347.5 | 0.0 | deliver_item(item_2) |
| 223 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9970 | 0.0457 | 343.6 | 343.6 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_1) |
| 48 | adequate | unexplained | - |
| 126 | unexplained | adequate | deliver_item(item_1) |
| 128 | adequate | unresolved | deliver_item(item_1) |
| 129 | unresolved | adequate | deliver_item(item_1) |
| 190 | adequate | unresolved | deliver_item(item_2) |
| 191 | unresolved | adequate | deliver_item(item_2) |
| 223 | adequate | unexplained | - |

Across the started task go_to(corner_SE) (task_absent; actual): on top of the stack from 32 to 79, no pin; the suspended task resumes at 80.

| tick | human action | truth | coffee_break(coffee_machine_0) belief / S | deliver_item(item_1) belief / S | deliver_item(item_2) belief / S | finding |
|---|---|---|---|---|---|---|
| 30 | pick_up grasp | deliver_item(item_1) | 0.1373 / 0.1199 | 0.8608 / 1.0000 | 0.0010 / 1.0000 | adequate |
| 31 | pick_up  | deliver_item(item_1) | 0.1167 / 0.0989 | 0.8813 / 1.0000 | 0.0010 / 1.0000 | adequate |
| 32 | move_to step | - | 0.1217 / 0.0959 | 0.8763 / 0.8966 | 0.0010 / - | adequate |
| 33 | move_to step | - | 0.1276 / 0.0927 | 0.8704 / 0.7971 | 0.0010 / 0.7631 | adequate |
| 34 | move_to step | - | 0.1345 / 0.0894 | 0.8635 / 0.7024 | 0.0010 / 0.5622 | adequate |
| 78 | move_to step | - | 0.4421 / 0.0000 | 0.5559 / 0.0000 | 0.0010 / 0.0000 | unexplained |
| 79 | move_to  | - | 0.4421 / 0.0000 | 0.5559 / 0.0000 | 0.0010 / 0.0000 | unexplained |
| 80 | move_to step | deliver_item(item_1) | 0.4173 / 0.0000 | 0.5807 / 0.0000 | 0.0010 / 0.0000 | unexplained |
| 81 | move_to step | deliver_item(item_1) | 0.3917 / 0.0000 | 0.6064 / 0.0000 | 0.0010 / 0.0000 | unexplained |
| 82 | move_to step | deliver_item(item_1) | 0.3653 / 0.0000 | 0.6327 / 0.0000 | 0.0010 / 0.0000 | unexplained |

The last entry (go_to(corner_SE)): first step 192, last step 238, acknowledgement 239; the idle human from 240. Live at its first tick: coffee_break(coffee_machine_0).

- coffee_break(coffee_machine_0): belief 0.9970 at 192; S < α from 223 (belief 0.9970; v·D 343.6 cm); the finding unexplained from 223.


### scenario_s09_06

**The long stand. Data for TODO-95** (stationary behaviour), and TODO-122.

`stand(PT80S)` is on top from 30 to 70 (task_absent), at shelf_1, before the pick-up. The delivery resumes at 71: an
acknowledgement tick for the `move_to` that already holds, then the grasp at 72.

- **deliver_item(item_1).** Its phase `pick_up(item_1)` (s_exp 2) runs from 28 to 71. The standing beyond s_exp is
  charged in both outputs (E10): its S falls below α at 47 (v·(s − s_exp) = 340 cm, 17 ticks beyond the priced 2).
- **The belief.** deliver_item(item_1)'s belief holds at 0.92 across the stand (0.860 at 30, 0.918 from 60): coffee_break's
  open walk is charged for the same standing ticks (its S below α at 35, 140 cm of it standing).
- **The finding.** Unexplained from 47 to 71; adequate at 72 (the grasp, E8).

**What the current records determine.**
- A stand at a stationary phase's location is charged against its priced standing, in the belief and in adequacy
  alike (E10, E6).
- A stand at the phase's own location costs the rivals as much as the true hypothesis, so the belief barely moves
  while the finding turns unexplained 17 ticks past the priced standing (E5's threshold at α = 0.05).

**What they leave open.** What the robot infers and does in response: TODO-95's decision level (T-D Q1), G and X.

![figure](scenario_s09_06/figure.png)

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 30 | stand(PT80S) | task_absent | stand | 0 | 2 |
| 71 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 72 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 74 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 103 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 105 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 135 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 137 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 166 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 168 | go_to(corner_SE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 215; idle from 216 to 245. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 245 |
| deliver_item(item_1) | move_to(item_1) | -1 to 27 |
| deliver_item(item_1) | pick_up(item_1) | 28 to 71 |
| deliver_item(item_1) | move_to(kitting_table_0) | 72 to 100 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 101 to 102 |
| deliver_item(item_2) | move_to(item_2) | -1 to 71 |
| deliver_item(item_2) | place(item_1,shelf_1) | 72 to 73 |
| deliver_item(item_2) | move_to(shelf_1) | 74 to 102 |
| deliver_item(item_2) | move_to(item_2) | 103 to 132 |
| deliver_item(item_2) | pick_up(item_2) | 133 to 134 |
| deliver_item(item_2) | move_to(kitting_table_0) | 135 to 163 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 164 to 165 |

Events (actual):

| tick | event |
|---|---|
| 47 | finding turns unexplained |
| 72 | finding turns adequate (from unexplained) |
| 103 | boundary |
| 103 | pin deliver_item(item_1) |
| 166 | boundary |
| 166 | pin deliver_item(item_2) |
| 199 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(corner_SE), ticks 168 to 215): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_1) | 0 to 29 | 25 | 0.7544 | yes | adequate |
| deliver_item(item_1) | 71 to 104 | 71 | 0.9184 | yes | inadequate |
| deliver_item(item_2) | 105 to 167 | 118 | 0.7553 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver_item(item_2) | move_to(item_2) | 0.0315 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver_item(item_1) |
| 35 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.1028 | 0.0453 | 344.6 | 204.6 | 140.0 | - |
| 47 | deliver_item(item_1) | pick_up(item_1) | 0.9162 | 0.0474 | 340.0 | 0.0 | 340.0 | - |
| 83 | deliver_item(item_2) | move_to(shelf_1) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 128 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0581 | 0.0453 | 344.4 | 344.4 | 0.0 | deliver_item(item_2) |
| 199 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9970 | 0.0456 | 343.9 | 343.9 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_1) |
| 47 | adequate | unexplained | - |
| 72 | unexplained | adequate | deliver_item(item_1) |
| 103 | adequate | unresolved | deliver_item(item_1) |
| 104 | unresolved | adequate | deliver_item(item_1) |
| 166 | adequate | unresolved | deliver_item(item_2) |
| 167 | unresolved | adequate | deliver_item(item_2) |
| 199 | adequate | unexplained | - |

Across the started task stand(PT80S) (task_absent; actual): on top of the stack from 30 to 70, no pin; the suspended task resumes at 71.

| tick | human action | truth | coffee_break(coffee_machine_0) belief / S | deliver_item(item_1) belief / S | deliver_item(item_2) belief / S | finding |
|---|---|---|---|---|---|---|
| 28 | move_to step | deliver_item(item_1) | 0.1859 / 0.1754 | 0.8121 / 1.0000 | 0.0010 / 0.0005 | adequate |
| 29 | move_to  | deliver_item(item_1) | 0.1603 / 0.1451 | 0.8377 / 1.0000 | 0.0010 / 0.0004 | adequate |
| 30 | stand stand | - | 0.1373 / 0.1199 | 0.8608 / 1.0000 | 0.0010 / 0.0003 | adequate |
| 31 | stand stand | - | 0.1280 / 0.0989 | 0.8700 / 0.8629 | 0.0010 / 0.0003 | adequate |
| 32 | stand stand | - | 0.1201 / 0.0814 | 0.8779 / 0.7401 | 0.0010 / 0.0002 | adequate |
| 69 | stand stand | - | 0.0796 / 0.0001 | 0.9184 / 0.0006 | 0.0010 / 0.0000 | unexplained |
| 70 | stand  | - | 0.0796 / 0.0000 | 0.9184 / 0.0005 | 0.0010 / 0.0000 | unexplained |
| 71 | move_to  | deliver_item(item_1) | 0.0796 / 0.0000 | 0.9184 / 0.0004 | 0.0010 / 0.0000 | unexplained |
| 72 | pick_up grasp | deliver_item(item_1) | 0.0796 / 0.0000 | 0.9184 / 1.0000 | 0.0010 / 1.0000 | adequate |
| 73 | pick_up  | deliver_item(item_1) | 0.0661 / 0.0000 | 0.9319 / 1.0000 | 0.0010 / 1.0000 | adequate |

The last entry (go_to(corner_SE)): first step 168, last step 214, acknowledgement 215; the idle human from 216. Live at its first tick: coffee_break(coffee_machine_0).

- coffee_break(coffee_machine_0): belief 0.9970 at 168; S < α from 199 (belief 0.9970; v·D 343.9 cm); the finding unexplained from 199.


### scenario_s09_07

**The change of mind. Data for TODO-94** (re-recognition after a switch), and TODO-122.

After item_1's grasp (30), deliver_item(item_2) is started (32) with item_1 in hand, so it expands
`deliver_with_return`: item_1 goes back to shelf_1 (the release at 33), then the walk to item_2. deliver_item(item_1)
resumes at 110 after deliver_item(item_2)'s pin and boundary at 108.

- **deliver_item(item_1) after the return.** Once item_1 is back on its shelf, it regresses to `pick_up(item_1)` and
  then `move_to(item_1)` (35 to 75). Its S falls below α at 44 (belief 0.684).
- **deliver_item(item_2).** It rises from 0.000 at 35 to first reach θ at 64 (0.780), 32 ticks after the switch; it is
  adequate throughout.
- **The finding.** Adequate from 0 to 203. It turns unexplained only on the exit walk (204), when coffee_break is lone.

**What the current records determine.**
- A switch to a modelled task within the support is followed by the belief, at the pace the rivals' refutation allows.
  deliver_item(item_2) enters the switch already refuted: the first walk to shelf_1 put its S below α at 14. There is
  no walk between the grasp and the switch: the started delivery's `move_to(shelf_1)` is acknowledged at 32 and item_1
  is released at 33.
- A resumption is not a boundary: deliver_item(item_1) re-enters from the boundary at 108 like any live hypothesis.

**What they leave open.** TODO-94's question (evidence against the new task, laid before the switch, persists until a
boundary), which is L's.

![figure](scenario_s09_07/figure.png)

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 30 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 32 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 2 |
| 33 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 2 |
| 35 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 2 |
| 76 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 2 |
| 78 | deliver_item(item_2,kitting_table_0) | covered | move_to | 2 | 2 |
| 108 | deliver_item(item_2,kitting_table_0) | covered | place | 1 | 2 |
| 110 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 140 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 142 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 171 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 173 | go_to(corner_SE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 221; idle from 222 to 251. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 251 |
| deliver_item(item_1) | move_to(item_1) | -1 to 27 |
| deliver_item(item_1) | pick_up(item_1) | 28 to 29 |
| deliver_item(item_1) | move_to(kitting_table_0) | 30 to 32 |
| deliver_item(item_1) | pick_up(item_1) | 33 to 34 |
| deliver_item(item_1) | move_to(item_1) | 35 to 75 |
| deliver_item(item_1) | place(item_2,shelf_2) | 76 to 77 |
| deliver_item(item_1) | move_to(shelf_2) | 78 to 107 |
| deliver_item(item_1) | move_to(item_1) | 108 to 137 |
| deliver_item(item_1) | pick_up(item_1) | 138 to 139 |
| deliver_item(item_1) | move_to(kitting_table_0) | 140 to 168 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 169 to 170 |
| deliver_item(item_2) | move_to(item_2) | -1 to 29 |
| deliver_item(item_2) | place(item_1,shelf_1) | 30 to 32 |
| deliver_item(item_2) | move_to(item_2) | 33 to 73 |
| deliver_item(item_2) | pick_up(item_2) | 74 to 75 |
| deliver_item(item_2) | move_to(kitting_table_0) | 76 to 105 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 106 to 107 |

Events (actual):

| tick | event |
|---|---|
| 108 | boundary |
| 108 | pin deliver_item(item_2) |
| 171 | boundary |
| 171 | pin deliver_item(item_1) |
| 204 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(corner_SE), ticks 173 to 221): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_1) | 0 to 31 | 25 | 0.7544 | yes | adequate |
| deliver_item(item_2) | 32 to 109 | 64 | 0.7796 | yes | adequate |
| deliver_item(item_1) | 110 to 172 | 135 | 0.7638 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver_item(item_2) | move_to(item_2) | 0.0315 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver_item(item_1) |
| 35 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0781 | 0.0500 | 334.5 | 214.5 | 120.0 | deliver_item(item_2) |
| 44 | deliver_item(item_1) | move_to(item_1) | 0.6845 | 0.0406 | 355.7 | 355.7 | 0.0 | deliver_item(item_2) |
| 87 | deliver_item(item_1) | move_to(shelf_2) | 0.0010 | 0.0399 | 357.4 | 357.4 | 0.0 | deliver_item(item_2) |
| 144 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0542 | 0.0420 | 352.2 | 292.2 | 60.0 | deliver_item(item_1) |
| 204 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9970 | 0.0468 | 341.2 | 341.2 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_1) |
| 108 | adequate | unresolved | deliver_item(item_2) |
| 109 | unresolved | adequate | deliver_item(item_2) |
| 171 | adequate | unresolved | deliver_item(item_1) |
| 172 | unresolved | adequate | deliver_item(item_1) |
| 204 | adequate | unexplained | - |

Across the started task deliver_item(item_2,kitting_table_0) (covered; actual): on top of the stack from 32 to 109, its hypothesis pinned at 108; the suspended task resumes at 110.

| tick | human action | truth | coffee_break(coffee_machine_0) belief / S | deliver_item(item_1) belief / S | deliver_item(item_2) belief / S | finding |
|---|---|---|---|---|---|---|
| 30 | pick_up grasp | deliver_item(item_1) | 0.1373 / 0.1199 | 0.8608 / 1.0000 | 0.0010 / 1.0000 | adequate |
| 31 | pick_up  | deliver_item(item_1) | 0.1167 / 0.0989 | 0.8813 / 1.0000 | 0.0010 / 1.0000 | adequate |
| 32 | move_to  | deliver_item(item_2) | 0.1085 / 0.0814 | 0.8895 / 0.8629 | 0.0010 / 0.8629 | adequate |
| 33 | place release | deliver_item(item_2) | 0.1014 / 0.0670 | 0.8966 / 1.0000 | 0.0010 / 1.0000 | adequate |
| 34 | place  | deliver_item(item_2) | 0.0852 / 0.0551 | 0.9128 / 1.0000 | 0.0010 / 1.0000 | adequate |
| 107 | move_to  | deliver_item(item_2) | 0.0010 / 0.0000 | 0.0010 / 0.0000 | 0.9970 / 1.0000 | adequate |
| 108 | place release | deliver_item(item_2) | 0.4990 / - | 0.4990 / - | retired | unresolved |
| 109 | place  | deliver_item(item_2) | 0.4990 / 1.0000 | 0.4990 / 1.0000 | retired | adequate |
| 110 | move_to step | deliver_item(item_1) | 0.4950 / 0.9771 | 0.5030 / 1.0000 | retired | adequate |
| 111 | move_to step | deliver_item(item_1) | 0.4907 / 0.9535 | 0.5073 / 1.0000 | retired | adequate |
| 112 | move_to step | deliver_item(item_1) | 0.4861 / 0.9293 | 0.5119 / 1.0000 | retired | adequate |

The last entry (go_to(corner_SE)): first step 173, last step 220, acknowledgement 221; the idle human from 222. Live at its first tick: coffee_break(coffee_machine_0).

- coffee_break(coffee_machine_0): belief 0.9970 at 173; S < α from 204 (belief 0.9970; v·D 341.2 cm); the finding unexplained from 204.


### scenario_s09_08

**The misdelivery. Data for TODO-87** (no pin, no boundary, no pool drop), and TODO-122.

item_1 is carried to kitting_table_1 and released there at 75 (binding_absent). Then the human delivers item_2 (77 to
132), then exits.

- **During the carry.** deliver_item(item_1)'s phase `move_to(kitting_table_0)` (30 to 74) refutes it by excess: S < α
  at 66, while its belief is 0.997 (the rivals were refuted earlier). The finding is unexplained from 66 to 74.
- **At the release (75).** `obj_at(item_1, kitting_table_0)` never holds, so there is no pin and no boundary.
  deliver_item(item_1) advances to `pick_up(item_1)` where the item now lies (a member, S = 1), and the finding returns
  to adequate.
- **On the human's next task.** deliver_item(item_1) keeps leading: 0.997 at 86, 0.897 at 120. It is refuted again at
  86 (`move_to(item_1)`) and 110. The true deliver_item(item_2) is adequate but never reaches θ (at most 0.483, at 130).
- **After deliver_item(item_2)'s pin and boundary (131).** deliver_item(item_1) and coffee_break are live at 0.499
  each; on the exit walk both are refuted (149, 164), and the finding is unexplained from 164.
- **Never pinned:** deliver_item(item_1) and coffee_break.

**What the current records determine.**
- Completion is a world fact of the designated table, so a delivery elsewhere retires nothing (handback §1.6).
- The misdelivered item's hypothesis continues with a new derived phase (pick it up where it lies) and keeps its base
  across the next task.

**What they leave open.** Whether a misdelivery should end the episode: L's boundary at a misdelivery, TODO-87 and
T-D Q4.

![figure](scenario_s09_08/figure.png)

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_1,kitting_table_1) | binding_absent | move_to | 0 | 1 |
| 30 | deliver_item(item_1,kitting_table_1) | binding_absent | pick_up | 0 | 1 |
| 32 | deliver_item(item_1,kitting_table_1) | binding_absent | move_to | 1 | 1 |
| 75 | deliver_item(item_1,kitting_table_1) | binding_absent | place | 0 | 1 |
| 77 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 99 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 101 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 131 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 133 | go_to(corner_SE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 180; idle from 181 to 210. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 210 |
| deliver_item(item_1) | move_to(item_1) | -1 to 27 |
| deliver_item(item_1) | pick_up(item_1) | 28 to 29 |
| deliver_item(item_1) | move_to(kitting_table_0) | 30 to 74 |
| deliver_item(item_1) | pick_up(item_1) | 75 to 76 |
| deliver_item(item_1) | move_to(item_1) | 77 to 98 |
| deliver_item(item_1) | place(item_2,shelf_2) | 99 to 100 |
| deliver_item(item_1) | move_to(shelf_2) | 101 to 130 |
| deliver_item(item_1) | move_to(item_1) | 131 to 210 |
| deliver_item(item_2) | move_to(item_2) | -1 to 29 |
| deliver_item(item_2) | place(item_1,shelf_1) | 30 to 31 |
| deliver_item(item_2) | move_to(shelf_1) | 32 to 74 |
| deliver_item(item_2) | move_to(item_2) | 75 to 96 |
| deliver_item(item_2) | pick_up(item_2) | 97 to 98 |
| deliver_item(item_2) | move_to(kitting_table_0) | 99 to 128 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 129 to 130 |

Events (actual):

| tick | event |
|---|---|
| 66 | finding turns unexplained |
| 75 | finding turns adequate (from unexplained) |
| 131 | boundary |
| 131 | pin deliver_item(item_2) |
| 164 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), deliver_item(item_1). At the last entry (go_to(corner_SE), ticks 133 to 180): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_2) | 77 to 132 | not reached | - | - | - |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver_item(item_2) | move_to(item_2) | 0.0315 | 0.0399 | 357.3 | 357.3 | 0.0 | - |
| 35 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0561 | 0.0427 | 350.5 | 290.5 | 60.0 | - |
| 41 | deliver_item(item_2) | move_to(shelf_1) | 0.0010 | 0.0391 | 359.4 | 359.4 | 0.0 | - |
| 66 | deliver_item(item_1) | move_to(kitting_table_0) | 0.9970 | 0.0453 | 344.5 | 344.5 | 0.0 | - |
| 86 | deliver_item(item_1) | move_to(item_1) | 0.9970 | 0.0410 | 354.8 | 354.8 | 0.0 | deliver_item(item_2) |
| 110 | deliver_item(item_1) | move_to(shelf_2) | 0.9788 | 0.0394 | 358.8 | 358.8 | 0.0 | deliver_item(item_2) |
| 149 | deliver_item(item_1) | move_to(item_1) | 0.1001 | 0.0384 | 361.2 | 361.2 | 0.0 | - |
| 164 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9934 | 0.0482 | 338.2 | 338.2 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | - |
| 66 | adequate | unexplained | - |
| 75 | unexplained | adequate | - |
| 131 | adequate | unresolved | deliver_item(item_2) |
| 132 | unresolved | adequate | deliver_item(item_2) |
| 164 | adequate | unexplained | - |

The last entry (go_to(corner_SE)): first step 133, last step 179, acknowledgement 180; the idle human from 181. Live at its first tick: coffee_break(coffee_machine_0), deliver_item(item_1).

- coffee_break(coffee_machine_0): belief 0.5083 at 133; S < α from 164 (belief 0.9934; v·D 338.2 cm); the finding unexplained from 164.

- deliver_item(item_1): belief 0.4897 at 133; S < α from 149 (belief 0.1001; v·D 361.2 cm); the finding unexplained from 164.


### scenario_s09_09

**A delivery outside the support. Data for the switch outside the support** (TODO-101's missing case), and TODO-122.

deliver_item(item_3) (63 to 108) is covered but assigned to nobody, so its hypothesis is outside the support: at the
floor throughout, never scored.

- **The live hypotheses during it.** deliver_item(item_2) and coffee_break. With item_3 in hand, deliver_item(item_2)
  expands `deliver_with_return`: `place(item_3, shelf_3)` at 84 to 85, then `move_to(shelf_3)` while the human carries
  item_3 to the table.
- **The belief.** coffee_break leads (0.968 at 83, 0.993 at 107) without any walk toward the machine: the belief is
  relative over the live set.
- **The finding.** It turns unexplained at 83, adequate at 84 (deliver_item(item_2)'s stationary `place` phase, S = 1),
  unexplained at 86, adequate at 87, and unexplained from 95 to 107. It is adequate again from 108.
- **At the completion (107).** `obj_at(item_3, kitting_table_0)` gives no pin and no boundary; no live hypothesis's
  terminal action completes.
- **Never pinned:** coffee_break.

**What the current records determine.**
- A hypothesis outside the support is skipped before the pin check (handback §1.1, §1.8): no pin, no boundary, no
  score.
- The live set's relative belief then points at whichever live hypothesis is refuted least, and the finding reports
  unexplained whenever every live member is inadequate.

**What they leave open.** What the robot does with a sustained unexplained finding and a confident leader (G, X); the
oracle-IR comparison for this case (TODO-101).

![figure](scenario_s09_09/figure.png)

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 30 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 32 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 61 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 63 | deliver_item(item_3,kitting_table_0) | covered | move_to | 0 | 1 |
| 84 | deliver_item(item_3,kitting_table_0) | covered | pick_up | 0 | 1 |
| 86 | deliver_item(item_3,kitting_table_0) | covered | move_to | 1 | 1 |
| 107 | deliver_item(item_3,kitting_table_0) | covered | place | 0 | 1 |
| 109 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 140 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 142 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 172 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 174 | go_to(corner_SE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 221; idle from 222 to 251. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 251 |
| deliver_item(item_1) | move_to(item_1) | -1 to 27 |
| deliver_item(item_1) | pick_up(item_1) | 28 to 29 |
| deliver_item(item_1) | move_to(kitting_table_0) | 30 to 58 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 59 to 60 |
| deliver_item(item_2) | move_to(item_2) | -1 to 29 |
| deliver_item(item_2) | place(item_1,shelf_1) | 30 to 31 |
| deliver_item(item_2) | move_to(shelf_1) | 32 to 60 |
| deliver_item(item_2) | move_to(item_2) | 61 to 83 |
| deliver_item(item_2) | place(item_3,shelf_3) | 84 to 85 |
| deliver_item(item_2) | move_to(shelf_3) | 86 to 106 |
| deliver_item(item_2) | move_to(item_2) | 107 to 137 |
| deliver_item(item_2) | pick_up(item_2) | 138 to 139 |
| deliver_item(item_2) | move_to(kitting_table_0) | 140 to 169 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 170 to 171 |

Events (actual):

| tick | event |
|---|---|
| 61 | boundary |
| 61 | pin deliver_item(item_1) |
| 83 | finding turns unexplained |
| 84 | finding turns adequate (from unexplained) |
| 86 | finding turns unexplained |
| 87 | finding turns adequate (from unexplained) |
| 95 | finding turns unexplained |
| 108 | finding turns adequate (from unexplained) |
| 172 | boundary |
| 172 | pin deliver_item(item_2) |
| 205 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(corner_SE), ticks 174 to 221): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_1) | 0 to 62 | 25 | 0.7544 | yes | adequate |
| deliver_item(item_3) | 63 to 108 | outside the support (at the floor) | - | - | - |
| deliver_item(item_2) | 109 to 173 | 147 | 0.7521 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver_item(item_2) | move_to(item_2) | 0.0315 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver_item(item_1) |
| 34 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0579 | 0.0451 | 345.0 | 285.0 | 60.0 | deliver_item(item_1) |
| 41 | deliver_item(item_2) | move_to(shelf_1) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 73 | deliver_item(item_2) | move_to(item_2) | 0.1314 | 0.0399 | 357.5 | 357.5 | 0.0 | deliver_item(item_3) |
| 83 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9690 | 0.0468 | 341.3 | 321.3 | 20.0 | deliver_item(item_3) |
| 95 | deliver_item(item_2) | move_to(shelf_3) | 0.0166 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_3) |
| 205 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9970 | 0.0483 | 338.1 | 338.1 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_1) |
| 61 | adequate | unresolved | deliver_item(item_1) |
| 62 | unresolved | adequate | deliver_item(item_1) |
| 83 | adequate | unexplained | deliver_item(item_3) |
| 84 | unexplained | adequate | deliver_item(item_3) |
| 86 | adequate | unexplained | deliver_item(item_3) |
| 87 | unexplained | adequate | deliver_item(item_3) |
| 95 | adequate | unexplained | deliver_item(item_3) |
| 108 | unexplained | adequate | deliver_item(item_3) |
| 172 | adequate | unresolved | deliver_item(item_2) |
| 173 | unresolved | adequate | deliver_item(item_2) |
| 205 | adequate | unexplained | - |

The last entry (go_to(corner_SE)): first step 174, last step 220, acknowledgement 221; the idle human from 222. Live at its first tick: coffee_break(coffee_machine_0).

- coffee_break(coffee_machine_0): belief 0.9970 at 174; S < α from 205 (belief 0.9970; v·D 338.1 cm); the finding unexplained from 205.


### scenario_s09_10

Both deliveries west; deliver_item(item_2) is outside the support.

- **The first walk.** deliver_item(item_3)'s S falls below α at 25, three ticks before the arrival at 28 (the geometry
  criterion), with belief 0.044. deliver_item(item_1) first reaches θ at 27 (0.774), two ticks later than in s09_01
  (25), where the rival is item_2 on the east side.
- **The second delivery.** After the boundary at 61, deliver_item(item_3) first reaches θ at 74 (0.760); its pin at 107
  is a boundary.
- **The exit walk.** coffee_break is lone at 0.9970; its S falls below α at 141, and the finding is unexplained from 141.

![figure](scenario_s09_10/figure.png)

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 30 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 32 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 61 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 63 | deliver_item(item_3,kitting_table_0) | covered | move_to | 0 | 1 |
| 84 | deliver_item(item_3,kitting_table_0) | covered | pick_up | 0 | 1 |
| 86 | deliver_item(item_3,kitting_table_0) | covered | move_to | 1 | 1 |
| 107 | deliver_item(item_3,kitting_table_0) | covered | place | 0 | 1 |
| 109 | go_to(corner_SE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 157; idle from 158 to 187. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_3).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 187 |
| deliver_item(item_1) | move_to(item_1) | -1 to 27 |
| deliver_item(item_1) | pick_up(item_1) | 28 to 29 |
| deliver_item(item_1) | move_to(kitting_table_0) | 30 to 58 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 59 to 60 |
| deliver_item(item_3) | move_to(item_3) | -1 to 29 |
| deliver_item(item_3) | place(item_1,shelf_1) | 30 to 31 |
| deliver_item(item_3) | move_to(shelf_1) | 32 to 60 |
| deliver_item(item_3) | move_to(item_3) | 61 to 81 |
| deliver_item(item_3) | pick_up(item_3) | 82 to 83 |
| deliver_item(item_3) | move_to(kitting_table_0) | 84 to 104 |
| deliver_item(item_3) | place(item_3,kitting_table_0) | 105 to 106 |

Events (actual):

| tick | event |
|---|---|
| 61 | boundary |
| 61 | pin deliver_item(item_1) |
| 107 | boundary |
| 107 | pin deliver_item(item_3) |
| 141 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(corner_SE), ticks 109 to 157): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_1) | 0 to 62 | 27 | 0.7736 | yes | adequate |
| deliver_item(item_3) | 63 to 108 | 74 | 0.7602 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 25 | deliver_item(item_3) | move_to(item_3) | 0.0438 | 0.0444 | 346.5 | 346.5 | 0.0 | deliver_item(item_1) |
| 34 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0574 | 0.0451 | 345.0 | 285.0 | 60.0 | deliver_item(item_1) |
| 41 | deliver_item(item_3) | move_to(shelf_1) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 83 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0598 | 0.0468 | 341.3 | 321.3 | 20.0 | deliver_item(item_3) |
| 141 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9970 | 0.0418 | 352.6 | 352.6 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_1) |
| 61 | adequate | unresolved | deliver_item(item_1) |
| 62 | unresolved | adequate | deliver_item(item_1) |
| 107 | adequate | unresolved | deliver_item(item_3) |
| 108 | unresolved | adequate | deliver_item(item_3) |
| 141 | adequate | unexplained | - |

The last entry (go_to(corner_SE)): first step 109, last step 156, acknowledgement 157; the idle human from 158. Live at its first tick: coffee_break(coffee_machine_0).

- coffee_break(coffee_machine_0): belief 0.9970 at 109; S < α from 141 (belief 0.9970; v·D 352.6 cm); the finding unexplained from 141.


### scenario_s09_11

Both deliveries west, coffee between; deliver_item(item_2) is outside the support.

- **The first walk:** as in _10 (deliver_item(item_3) below α at 25; deliver_item(item_1) first at θ at 27).
- **The coffee break.** coffee_break first reaches θ at 73. deliver_item(item_3) falls below α again at 80, on the walk
  to the machine; the pin at 133 is a boundary.
- **The second delivery.** deliver_item(item_3) is lone at 0.9970 from 133; its pin at 195 exhausts the lifecycle. The
  exit walk has no finding.

![figure](scenario_s09_11/figure.png)

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 30 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 32 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 61 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 63 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 1 |
| 104 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 1 |
| 135 | deliver_item(item_3,kitting_table_0) | covered | move_to | 0 | 1 |
| 171 | deliver_item(item_3,kitting_table_0) | covered | pick_up | 0 | 1 |
| 173 | deliver_item(item_3,kitting_table_0) | covered | move_to | 1 | 1 |
| 195 | deliver_item(item_3,kitting_table_0) | covered | place | 0 | 1 |
| 197 | go_to(corner_SE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 245; idle from 246 to 275. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_3).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 101 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 102 to 132 |
| deliver_item(item_1) | move_to(item_1) | -1 to 27 |
| deliver_item(item_1) | pick_up(item_1) | 28 to 29 |
| deliver_item(item_1) | move_to(kitting_table_0) | 30 to 58 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 59 to 60 |
| deliver_item(item_3) | move_to(item_3) | -1 to 29 |
| deliver_item(item_3) | place(item_1,shelf_1) | 30 to 31 |
| deliver_item(item_3) | move_to(shelf_1) | 32 to 60 |
| deliver_item(item_3) | move_to(item_3) | 61 to 168 |
| deliver_item(item_3) | pick_up(item_3) | 169 to 170 |
| deliver_item(item_3) | move_to(kitting_table_0) | 171 to 192 |
| deliver_item(item_3) | place(item_3,kitting_table_0) | 193 to 194 |

Events (actual):

| tick | event |
|---|---|
| 61 | boundary |
| 61 | pin deliver_item(item_1) |
| 133 | boundary |
| 133 | pin coffee_break(coffee_machine_0) |
| 195 | boundary |
| 195 | exhausted (no live hypothesis) from here |
| 195 | pin deliver_item(item_3) |

Never pinned: none. At the last entry (go_to(corner_SE), ticks 197 to 245): lifecycle and finding exhausted; on the idle ticks after it: exhausted.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_1) | 0 to 62 | 27 | 0.7736 | yes | adequate |
| coffee_break(coffee_machine_0) | 63 to 134 | 73 | 0.7789 | yes | adequate |
| deliver_item(item_3) | 135 to 196 | 135 | 0.9970 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 25 | deliver_item(item_3) | move_to(item_3) | 0.0438 | 0.0444 | 346.5 | 346.5 | 0.0 | deliver_item(item_1) |
| 34 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0574 | 0.0451 | 345.0 | 285.0 | 60.0 | deliver_item(item_1) |
| 41 | deliver_item(item_3) | move_to(shelf_1) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 80 | deliver_item(item_3) | move_to(item_3) | 0.0508 | 0.0392 | 359.2 | 359.2 | 0.0 | coffee_break(coffee_machine_0) |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_1) |
| 61 | adequate | unresolved | deliver_item(item_1) |
| 62 | unresolved | adequate | deliver_item(item_1) |
| 133 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 134 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 195 | adequate | exhausted | deliver_item(item_3) |

The last entry (go_to(corner_SE)): first step 197, last step 244, acknowledgement 245; the idle human from 246. Live at its first tick: none (exhausted).


### scenario_s09_12

The deliveries of _01 in the reverse order.

- **The first walk, east.** deliver_item(item_2) first reaches θ at 15 (0.766), against 25 for deliver_item(item_1) in
  _01. On this walk coffee_break is refuted by excess alone: its S falls below α at 24 (e 352 cm). On _01's walk west
  its S fell below α only at 34, with 60 cm of it standing: the coffee machine lies west of centre.
- **The second walk.** deliver_item(item_1) first reaches θ at 88.
- **The exit walk.** coffee_break is lone from 124; the finding is unexplained from 157.

![figure](scenario_s09_12/figure.png)

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 30 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 32 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 61 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 63 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 93 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 95 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 124 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 126 | go_to(corner_SE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 174; idle from 175 to 204. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 204 |
| deliver_item(item_1) | move_to(item_1) | -1 to 29 |
| deliver_item(item_1) | place(item_2,shelf_2) | 30 to 31 |
| deliver_item(item_1) | move_to(shelf_2) | 32 to 60 |
| deliver_item(item_1) | move_to(item_1) | 61 to 90 |
| deliver_item(item_1) | pick_up(item_1) | 91 to 92 |
| deliver_item(item_1) | move_to(kitting_table_0) | 93 to 121 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 122 to 123 |
| deliver_item(item_2) | move_to(item_2) | -1 to 27 |
| deliver_item(item_2) | pick_up(item_2) | 28 to 29 |
| deliver_item(item_2) | move_to(kitting_table_0) | 30 to 58 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 59 to 60 |

Events (actual):

| tick | event |
|---|---|
| 61 | boundary |
| 61 | pin deliver_item(item_2) |
| 124 | boundary |
| 124 | pin deliver_item(item_1) |
| 157 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(corner_SE), ticks 126 to 174): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_2) | 0 to 62 | 15 | 0.7663 | yes | adequate |
| deliver_item(item_1) | 63 to 125 | 88 | 0.7674 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver_item(item_1) | move_to(item_1) | 0.0403 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver_item(item_2) |
| 24 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0541 | 0.0420 | 352.1 | 352.1 | 0.0 | deliver_item(item_2) |
| 41 | deliver_item(item_1) | move_to(shelf_2) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_2) |
| 97 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0527 | 0.0408 | 355.2 | 295.2 | 60.0 | deliver_item(item_1) |
| 157 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9970 | 0.0469 | 341.1 | 341.1 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_2) |
| 61 | adequate | unresolved | deliver_item(item_2) |
| 62 | unresolved | adequate | deliver_item(item_2) |
| 124 | adequate | unresolved | deliver_item(item_1) |
| 125 | unresolved | adequate | deliver_item(item_1) |
| 157 | adequate | unexplained | - |

The last entry (go_to(corner_SE)): first step 126, last step 173, acknowledgement 174; the idle human from 175. Live at its first tick: coffee_break(coffee_machine_0).

- coffee_break(coffee_machine_0): belief 0.9970 at 126; S < α from 157 (belief 0.9970; v·D 341.1 cm); the finding unexplained from 157.


## IRB.4b: the recognizer behaves this way, and what that says about the design

- **What the agreement establishes.** Every compared public output of the recognizer, on every tick of the twelve
  runs, equals what the records at HEAD specify, as read with R1 to R4. That includes the deviations: the corner walk,
  the long stand, the change of mind, the misdelivery and the delivery outside the support.
- **What it does not establish.** The behaviours named in the deviation sections are therefore the current design's,
  not the recognizer's departures from it. Whether they are right is L, P, G and X's question, not answered here.
  The recognizer's private expected action and origin are not independently validated (option B), and E8's clause
  stays unexercised on its own (IRB.3b).

## IRB.4b: runs and tests that disagree with the mechanism

- **The twelve runs:** none against the records (0 disagreements at 1e-9). The one log-side entry (s09_07 at 35) is a
  print-precision artefact, classified above.
- **`tests/test_tl2_discovery.py`.** Its inventory literal moved from 42 to 54 scenarios and from setups 01–08 to
  01–09 with the new artefacts; the full suite passes (135).
- **The maintained baselines.** The tb1a sweep (16 logs and their `.rec`) is byte-identical to its README's IRB.2b
  section, 32 of 32 md5s. No code on the run path changed.

## IRB.4b: flags (outside scope, not fixed)

1. **The log's print precision.** The log prints S to four decimals, so adequacy read from the log is undetermined
   within 5·10⁻⁵ of α (s09_07 at 35). The in-process source is authoritative.
2. **`summary.py`'s refutation table** prints S to four decimals, so a refutation at S = 0.04998 reads `0.0500` (s09_07
   at 35). The tick is right; the printed value rounds.
3. **The s08 folders' `figure.png` and `summary.md`** are the IRB.3b presentation. A rerun of every run file would
   regenerate them in the IRB.4b presentation, with the same numbers.
4. **Flags carried from IRB.3b:**
   - tdlib's `[coverage]` parse fails on `start:` entries; a copy of the log without those lines is handed to it.
   - E8 is not exercised independently.

## L-build: the sixteen recompared under "T-D L" (28 September 2026)

The recognizer was changed under design_decisions.md, "T-D L: the belief lifecycle", as amended on the L-records report;
the generator was changed by derivation from the entry (README, "L-build": rules 5, 5b, 21 and the `reentries` column)
before the recomparison. The sixteen run files were rerun at L-build; the outputs in the scenario folders are
regenerated in place (the IRB.3b and IRB.4b numbers above are the history). The `.rec` streams are byte-identical to
IRB's; the trajectory equals the run's human lines on every tick in all sixteen; the in-process `[IR*]` lines are
byte-identical to the logged runs'.

**Result: 0 disagreements at 1e-9 against the in-process BeliefState and 0 at print precision against the log, in all
sixteen**, after two build defects the comparison found were fixed (below).

### Disagreements, classified (the recomparison's history)

- First pass (the recognizer at 493c095): one disagreement in each of the seven coffee scenarios, all in
  `most_likely` on a tick where `coffee_break` and one delivery stand at exactly 1/2 in the evidence: expected
  `coffee_break(coffee_machine_0)`, actual the delivery. s08_02, s09_02, s09_11 at 135, the re-entry tick (one
  incumbent); s08_03, s09_03 at 127 and s08_04, s09_04 at 139, the next boundary (the prior over the two live). The
  records determine the value: handback §1.7, "ties go to the first live key in sorted order". THE RECOGNIZER DISAGREED
  WITH THE RECORDS, twice by one cause: the build set the returning key's evidence and base after the loop, so neither
  the evidence (the argmax's order at the re-entry) nor the bases (the order the boundary's prior is built over) were in
  hypothesis order any more. Fixed in 5129d90 (the returning key's evidence entry made in hypothesis order), with a test.
- Second pass (5129d90): the four boundary cases remained (s08_03, s09_03 at 127; s08_04, s09_04 at 139). Fixed in
  3d65ca6 (the prior at a boundary built in hypothesis order), the test extended to a later boundary.
- Third pass (HEAD): none. No disagreement was classified "the generator misread the entry" or "the entry does not
  determine the value".

### The comparison with IRB (`analysis/l_build/irb_compare.py`: the in-process actual.csv, IRB at ec155f3 against L-build)

Moved ticks are the ticks on which any public output differs (most_likely, confidence, finding, lifecycle, or a live
hypothesis's belief, S or adequacy); the leaders at θ are listed from the first moved tick on.

| scenario | first moved tick | moved ticks | exhausted IRB → L | unexplained IRB → L | leaders at θ, IRB | leaders at θ, L |
|---|---|---|---|---|---|---|
| scenario_s08_01 | - | 0 | 0 → 0 | 47 → 47 | - | - |
| scenario_s08_02 | 135 | 146 | 80 → 0 | 0 → 47 | - | 140 item_2, 201 coffee:coffee_machine_0 |
| scenario_s08_03 | 86 | 185 | 80 → 0 | 0 → 47 | 100 item_1, 127 item_2 | 100 item_1, 142 item_2, 191 coffee:coffee_machine_0 |
| scenario_s08_04 | 84 | 198 | 80 → 0 | 0 → 47 | 91 item_1, 139 item_2 | 92 item_1, 154 item_2, 202 coffee:coffee_machine_0 |
| scenario_s09_01 | - | 0 | 0 → 0 | 47 → 47 | - | - |
| scenario_s09_02 | 135 | 146 | 80 → 0 | 0 → 47 | - | 140 item_2, 201 coffee:coffee_machine_0 |
| scenario_s09_03 | 86 | 185 | 80 → 0 | 0 → 47 | 100 item_1, 127 item_2 | 100 item_1, 142 item_2, 191 coffee:coffee_machine_0 |
| scenario_s09_04 | 84 | 198 | 80 → 0 | 0 → 47 | 91 item_1, 139 item_2 | 92 item_1, 154 item_2, 202 coffee:coffee_machine_0 |
| scenario_s09_05 | - | 0 | 0 → 0 | 125 → 125 | - | - |
| scenario_s09_06 | - | 0 | 0 → 0 | 72 → 72 | - | - |
| scenario_s09_07 | 33 | 75 | 0 → 0 | 48 → 48 | 64 item_2, 135 item_1, 171 coffee:coffee_machine_0 | 46 item_2, 135 item_1, 171 coffee:coffee_machine_0 |
| scenario_s09_08 | 75 | 56 | 0 → 0 | 56 → 56 | 144 coffee:coffee_machine_0 | 96 item_2, 144 coffee:coffee_machine_0 |
| scenario_s09_09 | 107 | 65 | 0 → 0 | 62 → 61 | 147 item_2, 172 coffee:coffee_machine_0 | 123 item_2, 172 coffee:coffee_machine_0 |
| scenario_s09_10 | - | 0 | 0 → 0 | 47 → 47 | - | - |
| scenario_s09_11 | 135 | 141 | 81 → 0 | 0 → 47 | - | 140 item_3, 195 coffee:coffee_machine_0 |
| scenario_s09_12 | - | 0 | 0 → 0 | 48 → 48 | - | - |

Unchanged (0 moved ticks): s08_01, s09_01, s09_05, s09_06, s09_10, s09_12: no terminal action without its fact, no
foreseeable task performed. The robot's pool is empty in every test-bed run, so L2 (ii) and L5 B are not exercised here
(the maintained baselines carry them: `analysis/l_build/REPORT.md`).

By cause:
- L1, a boundary without a pin.
  - scenario_s09_07 (the change of mind): the return of item_1 to shelf_1 at 33 (the first `place` of
    `deliver_with_return`, inside `deliver_item(item_2)`'s execution) is a boundary; IRB had none. All three at 0.3329 on
    33 (unresolved), adequate from 34; `deliver_item(item_2)` reaches θ at 46 (0.7524), 18 ticks earlier than IRB's 64,
    the first walk's refutation of it discarded at the boundary; `deliver_item(item_1)` reaches θ again at 135 as in IRB.
  - scenario_s09_08 (the misdelivery): the release of item_1 on kitting_table_1 at 75 is a boundary without a pin;
    IRB's stale leader (`deliver_item(item_1)` at 0.997 across item_2's delivery) is gone: all three at 0.3329 on 75,
    and `deliver_item(item_2)` reaches θ at 96 (0.7521), where IRB's never exceeded 0.483. `deliver_item(item_1)` stays
    live (its fact `obj_at(item_1, kitting_table_0)` never holds), refuted by the walk to item_2 (0.0009 at 96), and is
    never pinned. The finding: unexplained 66 to 74 as in IRB, unresolved at 75 (IRB: adequate at 75), adequate from 76.
  - scenario_s09_09 (item_3 delivered, outside the support): the release on kitting_table_0 at 107 is a boundary without
    a pin; coffee_break and `deliver_item(item_2)` at 0.499 on 107; item_2 reaches θ at 123 (IRB 147). The unexplained
    stretch 95 to 106 ends at the boundary (unresolved at 107; IRB: 95 to 107, adequate at 108): 62 → 61 unexplained ticks.
- L4, re-entry. In the seven coffee scenarios `coffee_break` is pinned when `waited` holds and re-enters on the tick
  `waited` clears, the human's first step after its latency tick (pin → re-entry: 133 → 135, 84 → 86, 82 → 84), at
  exactly 1/|H|: 0.4995 (s08_02, one incumbent) and 0.3333 (s08_03, _04, two). It re-enters in its walk phase
  (`move_to(coffee_machine_0)`: the human already outside the 30 cm radius), no observation on the re-entry tick, then
  refuted by the walk away (S 0.747 → 0.543 over the next two ticks). Its wait_at phase at re-entry (the case recorded
  for G at the plan step) did not occur. Consequences, each as the entry states them:
  - exhausted: 80 → 0 ticks (81 → 0 in s09_11): after the work order `coffee_break` is the lone live hypothesis, and the
    exit walk and the idle human read unexplained, 47 ticks each (from 234, 224, 235, 234, 224, 235, 229).
  - L3's numbers move (recorded in the entry): after the break at 84 (s09_03) both deliveries stand at 0.4990 on 84 and
    85 as in IRB; coffee returns at 86 as a third rival (the deliveries 0.338 / 0.328); `deliver_item(item_1)` still
    reaches θ at 100. scenario_s09_04: θ again at 92 (IRB 91).
  - the later deliveries: `deliver_item(item_2)` reaches θ at 142 (s09_03; IRB 127, when it was the lone live
    hypothesis at the boundary) and 154 (s09_04; IRB 139); in s08_02, s09_02 and s09_11 at 140 (IRB: lone from 133,
    never re-crossing).
  - after the last delivery `coffee_break` is the lone live hypothesis at 0.997 (leader at θ from 201, 191, 202, 195),
    unexplained from the exit walk on.

## Track 2.5: scenario_s09_13, the mid-action change (29 September 2026)

The scenario (`domains/kitting/scenarios/scenarios_s09.py`; `docs/assumptions.md`, 3.1 rejected): on env_layout_11,
robot idle, prior on, `deliver_item(item_1).during(move_to, "PT28S", coffee_break(coffee_machine_0), occurrence=1)`,
then deliver item_2, then the exit walk. PT28S is 14 ticks, half the carry's 28 steps (measured on scenario_s09_01's
replay: steps 32 to 59, acknowledgement 60). Declared intent (its description, label C): the recognition side of the
general machinery for a mid-action change, not the recognition-to-planning chain (the robot is idle, so no decision is
taken after tick 0 and no retraction or fallback can occur). Coverage, from the loader: entry 0
`deliver_item(item_1)` covered, `start:coffee_break(coffee_machine_0)` covered; entry 1 covered; entry 2 `go_to(corner_SE)`
task_absent (the exit walk); `[scenario-coverage] scenario_coverage=modelled_only tasks=WorkTask,PersonalTask,
HumanOnlyTask decisions=Start triggers=DuringAction`.

The oracle's extension, by derivation from T-H's executed semantics (design_decisions.md, "T-H", item 6 and the T-H2
TICKS line; `HumanAgent._step_stack` step 3, `Executor.suspend` / `resume`), in `trajectory.py` only (`oracle.py` derives
every phase from the world and is unchanged): the walk is cut where the human stands, after the cut's microactions, with
no acknowledgement tick, the break's first step on the next tick; on resumption the cut walk is completed first,
re-expanded from the human's position toward the table's current position (item_1 still in hand), then the task is
re-expanded (`place`, after the re-expansion's `move_to`, already holding, costs its acknowledgement tick at 148). The
cut is read from the replay's typed record (`Started` with `where` a `Cut`), not inferred. The sixteen earlier
scenarios rerun through the extended instrument: every committed output byte-identical.

The run: 292 steps (IRB.3b's rule: last acknowledgement 261 + 1 + 30). The trajectory equals the run's human lines on
every tick. The comparison: 0 disagreements against actual.csv (1e-9) and against actual_log.csv, 0 unmatched rows; no
classification needed.

Script actions (the first tick of each; stack depth 2 while the break is on top):

| tick | task | action | occurrence | stack depth |
|---|---|---|---|---|
| 0 | deliver_item(item_1) | move_to | 0 | 1 |
| 30 | deliver_item(item_1) | pick_up | 0 | 1 |
| 32 | deliver_item(item_1) | move_to | 1 | 1 |
| 46 | coffee_break(coffee_machine_0) | move_to | 0 | 2 |
| 76 | coffee_break(coffee_machine_0) | wait_at | 0 | 2 |
| 107 | deliver_item(item_1) (resumed) | move_to | 1 | 1 |
| 148 | deliver_item(item_1) (re-expanded) | move_to | 0 | 1 |
| 149 | deliver_item(item_1) | place | 0 | 1 |
| 151 | deliver_item(item_2) | move_to | 0 | 1 |
| 181 | deliver_item(item_2) | pick_up | 0 | 1 |
| 183 | deliver_item(item_2) | move_to | 1 | 1 |
| 212 | deliver_item(item_2) | place | 0 | 1 |
| 214 | go_to(corner_SE) | move_to | 0 | 1 |

The expected-action table (the oracle's derived phases; ticks inclusive):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 73 |
| coffee_break(coffee_machine_0) | wait_at(PT60S, coffee_machine_0) | 74 to 104 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 107 to 291 (re-entry at 107) |
| deliver_item(item_1) | move_to(item_1) | -1 to 27 |
| deliver_item(item_1) | pick_up(item_1) | 28 to 29 |
| deliver_item(item_1) | move_to(kitting_table_0) | 30 to 145 |
| deliver_item(item_1) | place(item_1, kitting_table_0) | 146 to 148 |
| deliver_item(item_2) | move_to(item_2) | -1 to 29 |
| deliver_item(item_2) | place(item_1, shelf_1) | 30 to 31 |
| deliver_item(item_2) | move_to(shelf_1) | 32 to 148 |
| deliver_item(item_2) | move_to(item_2) | 149 to 178 |
| deliver_item(item_2) | pick_up(item_2) | 179 to 180 |
| deliver_item(item_2) | move_to(kitting_table_0) | 181 to 209 |
| deliver_item(item_2) | place(item_2, kitting_table_0) | 210 to 211 |

What the recognizer does across the cut (actual; "the recognizer currently behaves this way", and the oracle derived
the same from the records):
- deliver_item(item_1) leads at 0.9955 on the cut tick (46); its carry phase `move_to(kitting_table_0)`, open since 30,
  takes the turn toward the machine as excess: S 0.7759 at 46, below α at 55 (v·D 359.9 cm, belief 0.9604). The
  finding is unexplained from 55.
- coffee_break's phase `move_to(coffee_machine_0)` has been inadequate since 34 (its excess accumulated over the
  delivery's first walks, from its origin at the start); inadequacy attaches to the phase (T-D L2 (i)), so the walk to
  the machine repairs nothing: coffee_break leads at θ from 67 (0.7904) while inadequate, and the finding stays
  unexplained until the advance to `wait_at` at 74 (E8), adequate from 74. In the meta-planner's terms (not exercised
  here): G1 would refuse admission 67 to 73 and admit at 74, "the new task admitted at its next fitting phase".
- The break's `wait_at` completion at 105 is the boundary and pins coffee_break; both deliveries restart at 0.4990
  (unresolved on 105, adequate from 106); coffee_break re-enters at 107 at 1/3 (T-D L4), refuted by the walk away (S < α
  at 116). The resumed delivery of item_1 (carried through the break, re-derived from the held item, L3) reaches θ at
  121 (0.7794), 14 ticks after its resumption, 16 after the boundary.
- deliver_item(item_2): θ at 164 (0.7548), 13 ticks after its first step; the exit walk reads unexplained from 245
  (coffee_break the lone live hypothesis at 0.9970, as in every coffee scenario since L4).

Run (git-ignored; md5s): `runs/env_layout_11_scenario_s09_13_on.log` 60d9491efa8d61c7c5679f1a1307719f,
`runs/env_layout_11_scenario_s09_13_on.rec` 739ce3199f341516687bfc7701b29143.

## G-build: observation warrant and the gate, the seventeen recompared (29 September 2026)

The recognizer gained a third output, the observation warrant per live hypothesis (design_decisions.md, "T-D G:
admission", AD1, AD2), and the gate its warrant condition (AD1, AD4). The instrument was extended by derivation from
the entry before the recomparison (README, "G-build"): `warrant` per hypothesis, compared exactly against actual.csv
and actual_log.csv, and `gate`, the gate's outcome per tick, compared exactly against actual.csv (the idle robot asks
admission at tick 0 only, so the gate's answer is read from its one home on every tick's BeliefState, not from the
log). Nothing was fitted.

Result: 0 disagreements in all seventeen scenarios (scenario_s08_01 to _04, scenario_s09_01 to _13), against
actual.csv and against actual_log.csv, on every column, the belief and the adequacy included (unchanged: every
expected.csv, actual.csv and actual_log.csv equals the committed one once the two new columns are removed). Nothing to
classify. The `.rec` streams are byte-identical; the run logs differ from the committed runs in the `[IR]` line's
`warrant=[...]` field, and s08_01 to s09_12 also in the step-0 `[meta-proj]` line (`projection=fallback
refused=none(below_theta)` for `projection=none(below_theta)`: T-D P's fallback, P-build's recorded difference; those
runs were last made at L-build). An unresolved move_to target (the plan-step ruling: no movement warrant) occurs on no
tick of the seventeen, nor of the 48 maintained logs (counted in process).

The picked cases (actual; the oracle derived the same):
- scenario_s09_01, the tail after 124: coffee_break is the lone live hypothesis at 0.997. The gate answers
  `none(leader_no_observation)` at 124 (the boundary), `none(leader_unwarranted)` at 125 (b + 1: the walk the boundary
  opened, nothing walked, not assigned), clears from 126 to 156 and `none(leader_inadequate)` from 157. A walk toward
  the machine does occur: the exit walk to corner_SE bears about 39° off the machine's bearing from kitting_table_0, so
  its first step gains 15.24 cm toward the machine (295 cm by 155). Before G the gate cleared from 125. The same in
  scenario_s08_01 (clears from 126) and scenario_s09_10 (from 109). The consequence is recorded in the entry's BUILT
  paragraph: a lone foreseeable task is warranted by any walk within 90° of its target's bearing; what AD1 resolves is
  admission on standing.
- scenario_s09_09, 83 to 87: no admission; the gate answers `none(leader_inadequate)` from 83 to 106 (coffee_break
  the leader). Earlier, 70 to 82, coffee_break clears on the walk toward shelf_3 (the delivery of item_3 outside the
  support): the machine lies about 62° off that walk's bearing, warranted by its gain, as before G it was admissible on
  θ and adequacy alone.
- scenario_s09_06, the stand: deliver_item(item_1)'s `pick_up` phase (28 to 71) is entered by the walk's completion at
  28 and holds observation warrant through the stand; the gate clears 25 to 46 (the walk's gain from 25, the entry from
  28; "28 to 46" in cbe3f00, corrected at the records commit) and refuses it as inadequate from 47 to 71; the carry,
  entered by the grasp at 72, is warranted and clears again.

scenario_s05_01 prior on (a maintained fixture, not a test-bed scenario; run through the instrument into a scratch
folder, not committed): the recognizer's outputs, the warrant and the gate agree with the oracle on every tick; 109
disagreements, all in the `obj_at` column (the robot's own items, which the instrument's human-only world does not
move; outside its scope). After the boundary at 141 the lone coffee_break is refused `none(leader_unwarranted)` from
142 to 158 (the human walks away from the machine: no gain) and inadequate from 159; before G it was admitted at 142.
