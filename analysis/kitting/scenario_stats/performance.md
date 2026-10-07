# Kitting scenarios run: descriptive statistics of what is performed

Every kitting scenario of the registry (722) run once at commit e51b3eb (7 October 2026), in one condition, and
counted from its log pair: the human's ticks per task and per action, the recognizer's leader against the task in
hand, and the robot's ticks per delivery, its decisions, holds and separation. A companion to README.md (what the
scenarios contain). Asked for by Hadi, 7 October 2026. Counts only: nothing here is a measurement of a design question,
and no run is a baseline.

## How it was run

- The condition: intention-aware, assignment knowledge and context knowledge on, `single_task`, gate `none`, cost
  `realized`, separation stop off, test level 0.05; the scenario's first (its only) reference layout; the steps the
  MPB's safety cap (`analysis/kitting/mpb/horizon.py`: the robot's plain chain plus the human's replay plus 30 ticks).
  The cap is a safety cap, not a timeout: a pool not completed within it is counted as such.
- 722 runs, 0 failed. The human's record does not depend on the robot (every script is `independent`; the four
  conditions of one T-F part 1 scenario give the same `.rec`), so the human's tables hold for any condition. The
  robot's tables hold for this condition only.
- Check: the 336 scenarios that T-F part 1's measurement ran in the same condition (`single_task`, context knowledge on)
  give the same completion tick in all 336 (`analysis/kitting/tf1/measurement/results.csv`); scenario_s25_16's log is
  byte-identical to run_288's but for the `[run]` lines.

```bash
analysis/kitting/scenario_stats/run_all.sh <out dir> 10        # about 10 minutes on 10 workers; data stays outside git
~/python-envs/ir-nomesa-env/bin/python analysis/kitting/scenario_stats/perf.py <out dir>/runs perf.json
PYTHONHASHSEED=0 ~/python-envs/ir-nomesa-env/bin/python analysis/kitting/scenario_stats/extract.py rows.json
~/python-envs/ir-nomesa-env/bin/python analysis/kitting/scenario_stats/perf_summary.py perf.json rows.json
```

## What is counted

- A task instance: from its `entered` event in the `.rec` stream; a second instance of the same task in one script is
  its own. Its ticks are the ticks it is on top of the human's stack (time under an interrupting task not included);
  its span is entered to completed (included). One tick is 2 seconds.
- An action occurrence: the consecutive record rows of one action of the task on top, its acknowledgement tick (the
  last progress value repeated) included. A walk resumed after a cut counts as a second occurrence.
- The recognizer's leader: the `[IR]` line's `most_likely` on each tick the instance is on top; a hypothesis matches
  when its schema is the task's and its bindings are the task's (a delivery's hypothesis names the item only). The
  leader is not the gate's outcome: admission also asks θ, adequacy, warrant and rank.
- The robot: a delivery runs from the previous delivery's last acknowledgement to its own `place` acknowledgement,
  ticks without a task left out (a walk the robot abandoned on a switch counts to the next delivery). The completion
  tick is the world tick after the robot's last release, counted where `[meta] ... all tasks complete` is printed.
  Holds from the `[hold] ... end` lines; separation from `[sep]`, every tick of the run (after the robot's completion
  too).

## Runs

runs 722; steps (the safety cap) min 120, median 395.0, max 908
task instances in the records 2858: completed 2802, abandoned 56

## H1. The human's ticks per task (completed instances; ticks with the task on top of the stack)

| task type | n | min | p10 | median | mean | p90 | max | sd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| deliver_item | 1440 | 27 | 54 | 86 | 86.5 | 124 | 169 | 28.4 |
| coffee_break | 470 | 34 | 51 | 73 | 68.0 | 83 | 96 | 13.6 |
| ac_activation | 86 | 8 | 22 | 47 | 43.0 | 53 | 84 | 15.2 |
| go_to | 694 | 18 | 22 | 48 | 49.5 | 82 | 107 | 22.5 |
| stand | 70 | 6 | 21 | 31 | 33.8 | 61 | 61 | 16.0 |
| go_to_and_stand | 42 | 36 | 43 | 88 | 79.1 | 103 | 125 | 24.6 |

Span, entered to completed, of the instances that were suspended (the time under the interrupting task included):

| task type | n | min | p10 | median | mean | p90 | max | sd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| deliver_item | 129 | 97 | 122 | 146 | 157.7 | 221 | 237 | 39.1 |

Abandoned instances (a drop), ticks on top before the drop:

| task type | n | min | p10 | median | mean | p90 | max | sd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| deliver_item | 56 | 9 | 15 | 32 | 33.6 | 54 | 78 | 16.3 |

Instances started by an event (a switch), completed:

| task type | n | min | p10 | median | mean | p90 | max | sd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| deliver_item | 3 | 78 | 78 | 78 | 78.0 | 78 | 78 | 0.0 |
| coffee_break | 106 | 34 | 40 | 61 | 64.4 | 83 | 88 | 16.5 |
| ac_activation | 12 | 8 | 10 | 31 | 31.8 | 47 | 49 | 12.5 |
| go_to | 1 | 48 | 48 | 48 | 48.0 | 48 | 48 | 0.0 |
| stand | 3 | 41 | 45 | 61 | 54.3 | 61 | 61 | 9.4 |
| go_to_and_stand | 4 | 66 | 67 | 74 | 84.8 | 112 | 125 | 23.8 |

Distribution, completed instances, bins of 10 ticks:

- deliver_item: 20–29: 8, 30–39: 27, 40–49: 78, 50–59: 136, 60–69: 266, 70–79: 98, 80–89: 171, 90–99: 242, 100–109: 120, 110–119: 121, 120–129: 51, 130–139: 54, 140–149: 36, 150–159: 22, 160–169: 10
- coffee_break: 30–39: 7, 40–49: 40, 50–59: 86, 60–69: 88, 70–79: 159, 80–89: 72, 90–99: 18
- ac_activation: 0–9: 2, 20–29: 12, 30–39: 18, 40–49: 37, 50–59: 12, 80–89: 5
- go_to: 10–19: 6, 20–29: 231, 30–39: 7, 40–49: 127, 50–59: 49, 60–69: 86, 70–79: 108, 80–89: 61, 90–99: 18, 100–109: 1
- stand: 0–9: 3, 20–29: 28, 30–39: 12, 40–49: 13, 60–69: 14
- go_to_and_stand: 30–39: 2, 40–49: 10, 60–69: 2, 80–89: 7, 90–99: 10, 100–109: 10, 120–129: 1

## H2. The human's ticks per action occurrence (its acknowledgement tick included)

| action | n | min | p10 | median | mean | p90 | max | sd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| move_to | 4310 | 1 | 19 | 42 | 41.3 | 71 | 107 | 19.9 |
| pick_up | 1471 | 2 | 2 | 2 | 2.0 | 2 | 2 | 0.0 |
| place | 1449 | 2 | 2 | 2 | 2.0 | 2 | 2 | 0.0 |
| stand | 112 | 6 | 21 | 21 | 30.8 | 61 | 61 | 13.9 |
| switch_on | 86 | 2 | 2 | 2 | 2.0 | 2 | 2 | 0.0 |
| wait_at | 470 | 31 | 31 | 31 | 31.0 | 31 | 31 | 0.0 |

## H3. The human's script length (ticks until the last task closes)

| measure | n | min | p10 | median | mean | p90 | max | sd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| script length | 722 | 55 | 163 | 274 | 279.9 | 397 | 485 | 89.4 |

Bins of 50: 50–99: 7, 100–149: 44, 150–199: 86, 200–249: 144, 250–299: 146, 300–349: 115, 350–399: 114, 400–449: 44, 450–499: 22

Share of the human's busy ticks per task type (all runs pooled):

- deliver_item: 126431 ticks, 62.6%
- coffee_break: 31938 ticks, 15.8%
- ac_activation: 3699 ticks, 1.8%
- go_to: 34338 ticks, 17.0%
- stand: 2365 ticks, 1.2%
- go_to_and_stand: 3323 ticks, 1.6%

## R1. The recognizer's leader against the task in hand (task-model types; per instance)

Share of the instance's ticks on top of the stack in which the recognizer's most likely hypothesis is the task:

| task type | n | min | p10 | median | mean | p90 | max | sd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| deliver_item | 1496 | 0.00 | 0.84 | 0.97 | 0.9 | 0.99 | 1.00 | 0.1 |
| coffee_break | 470 | 0.00 | 0.20 | 0.68 | 0.6 | 0.97 | 0.98 | 0.3 |
| ac_activation | 86 | 0.00 | 0.00 | 0.34 | 0.4 | 0.96 | 0.96 | 0.4 |

Ticks from the instance's first tick on top until the leader is first the task (instances never led: count):

| task type | n | min | p10 | median | mean | p90 | max | sd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| deliver_item | 1494 | 0 | 0 | 0 | 2.3 | 6 | 77 | 7.7 |
| deliver_item: never the leader | 2 | | | | | | | |
| coffee_break | 460 | 0 | 0 | 18 | 20.7 | 51 | 76 | 20.9 |
| coffee_break: never the leader | 10 | | | | | | | |
| ac_activation | 54 | 0 | 0 | 10 | 15.8 | 42 | 77 | 19.0 |
| ac_activation: never the leader | 32 | | | | | | | |

## P1. The robot (working robot: 369 runs; idle robot: 353 runs)

pool completed within the cap: 356 of 369

| measure | n | min | p10 | median | mean | p90 | max | sd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| completion tick (world) | 356 | 52 | 93 | 174 | 202.2 | 328 | 429 | 89.6 |
| releases done (b) | 369 | 0 | 2 | 2 | 2.4 | 3 | 4 | 0.7 |
| ticks per delivery, total | 890 | 15 | 38 | 81 | 82.1 | 133 | 276 | 36.4 |
| … walking (step) | 890 | 9 | 32 | 73 | 73.7 | 126 | 166 | 34.6 |
| … standing in a task (holds) | 890 | 0 | 0 | 0 | 2.4 | 6 | 132 | 9.5 |
| … grasp and release | 890 | 2 | 2 | 2 | 2.0 | 2 | 2 | 0.0 |
| … acknowledgement ticks | 890 | 4 | 4 | 4 | 4.1 | 4 | 5 | 0.3 |
| ticks without a task before completion | 368 | 0 | 0 | 1 | 1.3 | 2 | 3 | 0.8 |
| holds per run | 369 | 0 | 0 | 0 | 0.8 | 3 | 8 | 1.6 |
| held ticks per run | 369 | 0 | 0 | 0 | 11.8 | 26 | 350 | 40.7 |
| admissions (projection built) | 369 | 0 | 2 | 4 | 3.9 | 6 | 8 | 1.5 |
| fallback projections | 369 | 0 | 5 | 10 | 11.4 | 19 | 27 | 5.2 |
| decisions: no_current_task | 369 | 1 | 1 | 2 | 2.3 | 3 | 4 | 0.8 |
| decisions: recognition_changed | 369 | 0 | 2 | 5 | 4.5 | 7 | 9 | 1.9 |
| decisions: projection_expired | 369 | 0 | 2 | 7 | 7.5 | 14 | 24 | 4.4 |
| decisions: all | 369 | 1 | 7 | 14 | 14.3 | 22 | 30 | 5.4 |
| separation minimum (cm) | 369 | 2 | 11 | 60 | 172.5 | 409 | 1368 | 254.1 |
| ticks below min_separation (50 cm) | 369 | 0 | 0 | 0 | 7.4 | 8 | 285 | 30.9 |

runs with a tick below min_separation: 150 of 369
completion tick, bins of 50: 50–99: 43, 100–149: 63, 150–199: 89, 200–249: 37, 250–299: 75, 300–349: 25, 350–399: 14, 400–449: 10

Idle robot: ticks below min_separation in 19 of 353 runs; separation minimum median 275.7 cm

(b) Releases, not tasks: in scenario_s11_03 and scenario_s11_06 the robot releases 3 times for a pool of 2 (the MPB's
switch while carrying, part (v)).

## Observations

- The human's delivery takes 86 ticks at the median (p10 54, p90 124); a coffee break 73 (its wait is 31 of them); an
  A/C activation 47; the exit walk (`go_to`) 48. Deliveries take 62.6% of the human's busy ticks, coffee breaks
  15.8%, the walks 17.0%.
- A suspended delivery spans 146 ticks at the median from entry to completion, against 86 for one done in one go.
  A dropped delivery is dropped after 32 ticks at the median.
- A script runs 274 ticks at the median (55 to 485).
- The recognizer's leader is the true task on 97% of a delivery's ticks at the median, from its first tick at the
  median. For a coffee break it is 68%, first after 18 ticks, never in 10 of 470. For an A/C activation it is 34%;
  in 32 of 86 instances it never leads.
- The robot completes its pool within the cap in 356 of 369 runs, at tick 174 at the median (52 to 429). The 13 not
  completed: scenario_s01_02, s01_03, s01_05, s02_02, s03_02, s03_03, s03_04, s03_07, s03_08, s07_01, s07_02 (early
  example scripts and fixtures, several with a dropped or unperformed human task) and scenario_s17_08, s17_10. Not
  analysed.
- A robot delivery takes 81 ticks at the median, 73 of them walking; holds are rare (none in the median run, 11.8 held
  ticks per run on average, 350 at most). A run takes 14 decisions at the median, most of them `projection_expired`.
- 150 of the 369 working-robot runs have at least one tick below min_separation (50 cm); 19 of the 353 idle-robot runs
  do (the human passing the standing robot).
- Seen in the logs, not analysed: after the pool ends, the robot's per-tick line in some runs repeats
  `action=place micro=release` with `task=None` on every tick (scenario_s18_02, s18_04, s18_06, s23_09, s23_13,
  s28_02, s28_04); in others it reads `action=None micro=None`. `perf.py` counts only releases inside a task.
