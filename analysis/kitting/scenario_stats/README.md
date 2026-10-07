# Kitting scenarios: descriptive statistics

What the kitting scenarios contain, as the registry loads them at commit 10da064 (7 October 2026): the room, the
shift, the two task pools, the human's script, its events and deviations, and the timeline of context facts. Counts
only; nothing is run. Asked for by Hadi, 7 October 2026. What the scenarios perform when run (ticks per task, the
recognizer's leader, the robot's deliveries): `performance.md`, beside this file.

Reproduce from the repository root:

```bash
PYTHONHASHSEED=0 ~/python-envs/ir-nomesa-env/bin/python analysis/kitting/scenario_stats/extract.py rows.json
~/python-envs/ir-nomesa-env/bin/python analysis/kitting/scenario_stats/summarise.py rows.json
```

`extract.py` reads `domains.kitting.registry.domain_config` (scenarios, setups, layouts) and writes one row per
scenario; `summarise.py` prints the distributions and the per-setup table below. Room counts are from the scenario's
first (and in every case only) reference layout.

## Overview

- Scenarios: 722. Setups: 31. Layouts used: 21 (every registered one). Modules: `scenarios_s01` to `scenarios_s31`.
- Every scenario has 1 human and 1 robot, the robot observing the human; 1 reference layout; 4 areas; script
  dependence `independent`; no closing part and no repeatable entry in any script.

## 1. Where the scenarios come from

| setups | purpose | scenarios | share |
|---|---|---:|---:|
| s01–s07 | regression and evaluation fixtures | 38 | 5.3% |
| s08–s09 | IRB (the recognizer's test-bed) | 17 | 2.4% |
| s10–s12 | MPB (the meta-planner's test-bed) | 36 | 5.0% |
| s13–s15 | T-K part 1, round 1 and step 4 (IRB, idle robot) | 57 | 7.9% |
| s16, s31 | T-K part 1, step 5, the planning cases | 12 | 1.7% |
| s17–s30 | T-K part 1, step 5e (room copies, idle and working robot) | 562 | 77.8% |

Step 5e dominates the corpus: every pooled figure below mostly describes it.

## 2. The room and the shift (layout and setup)

| measure | min | max | mean | median | distribution (value: scenarios) |
|---|---:|---:|---:|---:|---|
| items in the setup | 2 | 10 | 6.51 | 6 | 2:4, 3:45, 4:77, 5:117, 6:122, 7:25, 8:278, 9:5, 10:49 |
| kitting tables | 1 | 7 | 1.69 | 2 | 1:345, 2:341, 5:31, 7:5 |
| shelves | 2 | 11 | 6.15 | 6 | 2:4, 3:34, 4:106, 5:141, 6:169, 8:232, 9:31, 11:5 |
| coffee machines | 0 | 1 | 0.97 | 1 | 0:25, 1:697 |
| A/C switches | 0 | 1 | 0.37 | 0 | 0:458, 1:264 |
| foreseeable hypotheses (a) | 0 | 2 | 1.33 | 1 | 0:25, 1:433, 2:264 |
| landmarks | 1 | 5 | 3.14 | 5 | 1:318, 3:36, 5:368 |

(a) One `coffee_break` per coffee machine and one `ac_activation` per A/C switch in the room.

Scenarios per layout: env_layout_19 153, _20 152, _02 73, _07 70, _05 67, _06 61, _12 30, _16 21, _17 21, _15 15,
_11 13, _18 11, _08 6, _01 5, _03 5, _09 5, _14 5, _10 4, _04 3, _13 1, _30 1.

## 3. The task pools

| measure | min | max | mean | median | distribution |
|---|---:|---:|---:|---:|---|
| robot's assigned tasks | 0 | 4 | 1.26 | 1 | 0:353, 1:15, 2:205, 3:109, 4:40 |
| robot's assigned tasks, working robot only (369) | 1 | 4 | 2.47 | 2 | |
| human's assigned tasks | 1 | 4 | 2.15 | 2 | 1:58, 2:540, 3:80, 4:44 |
| items in neither pool (b) | 0 | 9 | 3.10 | 3 | 0:139, 1:99, 2:58, 3:96, 4:133, 5:35, 6:131, 7:11, 8:17, 9:3 |

(b) Items in the setup minus the robot's pool minus the human's pool: stock nobody is assigned.

Idle robot (empty pool, observing only): 353 scenarios (48.9%). Working robot: 369 (51.1%).

Robot tasks (rows) against the human's assigned tasks (columns), scenarios per cell:

| | H=1 | H=2 | H=3 | H=4 |
|---|---:|---:|---:|---:|
| R=0 | 15 | 248 | 50 | 40 |
| R=1 | 13 | 2 | – | – |
| R=2 | 27 | 153 | 21 | 4 |
| R=3 | 1 | 99 | 9 | – |
| R=4 | 2 | 38 | – | – |

## 4. The human's script

| measure | min | max | mean | median | distribution |
|---|---:|---:|---:|---:|---|
| script entries | 1 | 6 | 3.78 | 4 | 1:1, 2:53, 3:227, 4:292, 5:121, 6:28 |
| tasks named (entries and started tasks) | 1 | 6 | 3.96 | 4 | 1:1, 2:35, 3:162, 4:357, 5:129, 6:38 |
| `deliver_item` | 0 | 4 | 2.07 | 2 | 0:6, 1:97, 2:502, 3:73, 4:44 |
| `coffee_break` | 0 | 2 | 0.65 | 1 | 0:300, 1:374, 2:48 |
| `ac_activation` | 0 | 1 | 0.12 | 0 | 0:636, 1:86 |
| foreseeable tasks | 0 | 2 | 0.77 | 1 | 0:247, 1:394, 2:81 |
| human-only tasks, all | 0 | 3 | 1.12 | 1 | 0:34, 1:579, 2:100, 3:9 |
| `go_to` (mostly the exit walk) | 0 | 2 | 0.96 | 1 | 0:44, 1:662, 2:16 |
| `stand` | 0 | 1 | 0.10 | 0 | 0:652, 1:70 |
| `go_to_and_stand` | 0 | 1 | 0.06 | 0 | 0:680, 1:42 |

Scripted foreseeable tasks, (`coffee_break`, `ac_activation`): (0,0) 247, (1,0) 341, (0,1) 53, (1,1) 33, (2,0) 48.
No scenario scripts a foreseeable task whose object is missing from its room.

## 5. Events and deviations

| measure | min | max | mean | scenarios with at least one |
|---|---:|---:|---:|---:|
| events per script | 0 | 2 | 0.26 | 182 (25.2%; 0:540, 1:179, 2:3) |
| trigger `at` (after an action) | 0 | 2 | 0.25 | 176 |
| trigger `during` (a mid-action cut) | 0 | 1 | 0.01 | 6 |
| decision start (a switch to another task) | 0 | 1 | 0.18 | 129 |
| decision `drop` (the task in hand abandoned) | 0 | 1 | 0.08 | 56 |
| delivery to a table other than the designated one | 0 | 1 | 0.04 | 30 |
| delivery not in the human's assigned pool | 0 | 1 | 0.04 | 31 |
| assigned task never performed | 0 | 2 | 0.12 | 82 (1:75, 2:7) |

## 6. The timeline of context facts (T-K part 1)

| | scenarios |
|---|---:|
| source: the scenario's own | 425 (58.9%) |
| source: the setup's default | 21 (2.9%) |
| source: none | 276 (38.2%) |
| windows in force: 0 / 1 / 2 | 284 / 409 / 29 (mean 0.65) |
| facts: `break_time` only | 371 |
| facts: `room_warm` only | 54 |
| facts: both | 13 |
| facts: none | 284 |

## 7. Per setup

Ranges over the setup's scenarios. it items, KT kitting tables, cm coffee machines, ac A/C switches, R robot's
tasks, H human's assigned tasks, ent script entries, del / cb / acA scripted deliveries / coffee breaks / A/C
activations, ev scenarios with an event, drp drops, dev deliveries to a non-designated table; timeline: scenarios per
source.

| setup | n | layout | it | KT | cm | ac | R | H | ent | del | cb | acA | ev | drp | dev | timeline |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| s01 | 8 | 01, 04 | 5 | 1 | 0 | 0 | 1-3 | 1-2 | 2-5 | 1-2 | 0 | 0 | 3 | 2 | 0 | none 8 |
| s02 | 3 | 02 | 8 | 1 | 1 | 1 | 4 | 2 | 2-5 | 2 | 1 | 0-1 | 2 | 1 | 0 | none 3 |
| s03 | 9 | 03, 06 | 5 | 1 | 0-1 | 0 | 2-3 | 2-3 | 2-4 | 2-3 | 0-1 | 0 | 4 | 2 | 0 | none 9 |
| s04 | 3 | 05 | 5 | 1 | 1 | 1 | 3 | 2 | 3-5 | 2 | 0-1 | 0-1 | 2 | 2 | 0 | none 3 |
| s05 | 4 | 07 | 4 | 1 | 1 | 1 | 2 | 1-2 | 3-4 | 1-2 | 0-1 | 0-1 | 1 | 1 | 0 | none 4 |
| s06 | 6 | 08 | 6 | 2 | 0 | 0 | 1-4 | 1-2 | 1-3 | 1-2 | 0 | 0 | 1 | 1 | 1 | none 6 |
| s07 | 5 | 09 | 6 | 2 | 0 | 0 | 4 | 2 | 2-4 | 2 | 0 | 0 | 2 | 1 | 1 | none 5 |
| s08 | 4 | 10 | 2 | 1 | 1 | 0 | 0 | 2 | 3-4 | 2 | 0-1 | 0 | 2 | 0 | 0 | none 4 |
| s09 | 13 | 11 | 3 | 2 | 1 | 0 | 0 | 2 | 2-4 | 2-3 | 0-1 | 0 | 6 | 0 | 1 | none 13 |
| s10 | 25 | 12, 13 | 7 | 5 | 0-1 | 0 | 1-4 | 1-2 | 2-5 | 1-2 | 0-1 | 0 | 10 | 0 | 3 | none 11, scenario 14 |
| s11 | 6 | 12 | 5 | 5 | 1 | 0 | 2 | 1 | 2-3 | 0 | 0 | 0 | 0 | 0 | 0 | none 3, scenario 3 |
| s12 | 5 | 14 | 9 | 7 | 1 | 0 | 2 | 2 | 3-4 | 2 | 0-1 | 0 | 0 | 0 | 0 | none 2, scenario 3 |
| s13 | 15 | 15 | 4 | 1 | 1 | 0 | 0 | 4 | 5-6 | 4 | 0-1 | 0 | 4 | 0 | 0 | setup 7, scenario 8 |
| s14 | 21 | 16 | 3 | 1 | 1 | 1 | 0 | 3 | 4-5 | 3 | 0-1 | 0-1 | 6 | 0 | 0 | setup 7, scenario 14 |
| s15 | 21 | 17 | 4 | 1 | 1 | 1 | 0 | 4 | 5-6 | 4 | 0-1 | 0-1 | 6 | 0 | 0 | setup 7, scenario 14 |
| s16 | 11 | 18 | 3 | 2 | 1 | 1 | 1 | 1 | 2-3 | 1 | 0-1 | 0-1 | 0 | 0 | 0 | scenario 11 |
| s17 | 40 | 02 | 8 | 1 | 1 | 1 | 0-4 | 2-3 | 2-5 | 1-3 | 0-1 | 0-1 | 11 | 0 | 0 | none 12, scenario 28 |
| s18 | 30 | 02 | 8 | 1 | 1 | 1 | 0-3 | 2-3 | 4-5 | 2-3 | 0-2 | 0 | 6 | 6 | 0 | none 10, scenario 20 |
| s19 | 34 | 05 | 5 | 1 | 1 | 1 | 0-3 | 2 | 3-5 | 1-2 | 0-1 | 0-1 | 11 | 5 | 0 | none 11, scenario 23 |
| s20 | 30 | 05 | 6 | 1 | 1 | 1 | 0-3 | 2-3 | 4-5 | 2-3 | 0-1 | 0-1 | 0 | 0 | 0 | none 10, scenario 20 |
| s21 | 31 | 06 | 5 | 1 | 1 | 0 | 0-3 | 2 | 3-4 | 1-2 | 0-1 | 0 | 6 | 0 | 0 | none 11, scenario 20 |
| s22 | 26 | 06 | 5 | 1 | 1 | 0 | 0-2 | 2-3 | 3-5 | 2-3 | 0-2 | 0 | 6 | 6 | 0 | none 10, scenario 16 |
| s23 | 36 | 07 | 4 | 1 | 1 | 1 | 0-2 | 1-2 | 3-4 | 1-2 | 0-1 | 0-1 | 11 | 5 | 0 | none 11, scenario 25 |
| s24 | 30 | 07 | 6 | 1 | 1 | 1 | 0-3 | 2 | 3-5 | 1-2 | 0-2 | 0-1 | 0 | 0 | 0 | none 10, scenario 20 |
| s25 | 52 | 19 | 8 | 2 | 1 | 0 | 0-2 | 2-3 | 3-5 | 2-3 | 0-2 | 0 | 12 | 6 | 4 | none 20, scenario 32 |
| s26 | 52 | 19 | 8 | 2 | 1 | 0 | 0-2 | 1-4 | 2-5 | 1-4 | 0-2 | 0 | 16 | 4 | 0 | none 20, scenario 32 |
| s27 | 49 | 19 | 10 | 2 | 1 | 0 | 0-2 | 1-3 | 2-4 | 1-3 | 0-2 | 0 | 15 | 3 | 6 | none 20, scenario 29 |
| s28 | 50 | 20 | 8 | 2 | 1 | 0 | 0-3 | 1-2 | 2-5 | 1-2 | 0-2 | 0 | 11 | 0 | 3 | none 20, scenario 30 |
| s29 | 51 | 20 | 6 | 2 | 1 | 0 | 0-2 | 1-3 | 2-5 | 1-3 | 0-1 | 0 | 17 | 6 | 5 | none 20, scenario 31 |
| s30 | 51 | 20 | 8 | 2 | 1 | 0 | 0-2 | 2-4 | 3-6 | 1-4 | 0-2 | 0 | 11 | 5 | 6 | none 20, scenario 31 |
| s31 | 1 | 30 | 4 | 2 | 1 | 1 | 2 | 1 | 3 | 1 | 1 | 0 | 0 | 0 | 0 | scenario 1 |

## Observations

- One set is most of the corpus: step 5e (s17–s30) holds 562 of 722 scenarios, env_layout_19 and _20 alone 305.
- Half the scenarios have an idle robot (353). A working robot has 2 or 3 tasks in most of them; the human has 2
  assigned tasks in 540 of 722.
- Deviations are sparse: 75% of the scripts have no event, 6 cut into an action, 56 abandon a task. No script uses
  the priority form's repeatable entry or closing part.
- Every scenario has exactly 1 human and 1 robot: kitting does not test several humans or several robots.
- Among the foreseeable tasks the coffee break dominates: a coffee machine is in 97% of the rooms, an A/C switch in
  37%, and an A/C activation is scripted in 86 scenarios.
- In 583 scenarios some stock is in neither pool, up to 9 items.
- The docstring of `scenarios_s31.py` names env_setup_16; its one scenario is on env_setup_31 and env_layout_30.
