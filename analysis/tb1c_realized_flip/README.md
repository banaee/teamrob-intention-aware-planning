# analysis/tb1c_realized_flip — scenario_83: an existence case in which realized cost changes the head under full_reorder (T-B1c)

A record of ONE existence case, not an evaluation and not a baseline: `full_reorder` baselines are recorded in T-B3.
On every fixture measured before this (scenario_80, scenario_81, scenario_00; `analysis/tb2c_per_entry_holds/README.md`,
TODO-47 (f-designations)) no winning ordering under `full_reorder` carried a hold, so realized cost had never changed
the head. scenario_83 is a scenario in which it does, in the way T-B2c was built for: a conflict in an entry AFTER
the head of the plain-cost winning ordering, inside the assessed window, which the head realized alone cannot see.

The scenario literal (`domains/kitting/scenarios.py`, registered in `domains/kitting/registry.py`) is a fixture on
Hadi's ruling (option (i), 8aec522).

**What this case is and is not.** scenario_83 is an EXISTENCE CASE: it shows that realized cost can change the head
under `full_reorder` through a conflict after the head, not that doing so helps. It is fragile on two numbers: the
conflict is decided by 0.78 cm against s = 50 cm (the item_1 carry projected to stop 49.22 cm from the human, the
item_6 carry 58.54 cm; TODO-89), and the timing window is about 3 ticks wide (human start x −410 to −430 flips the
head; −390 and −450 do not). On env_layout8 any case (b) is a TABLE CONVERGENCE: the human's routes touch the robot's
only at the tables, so a conflict after the head can only be a meeting at a table. In execution both orderings meet
the human at kitting_table_0 (37.48 cm under plain cost, inside the assessed window; 42.87 cm under realized, a
quarter tick past T_h), because T_h ends at the human's release and the human, done, stands there. That is the known
horizon limitation — the robot approaching a human still at the table past its projection, scenario_81's finding
(`analysis/tb1b_two_tables/README.md`, the closest approach past the human's projection) — and it is why the
completion ticks below carry no benefit claim.

## The requirements the case is checked against (the T-B1c prompt)

- R1 one variable against scenario_80: the robot's assigned_tasks, its designations and start are scenario_80's;
  only the human's scheduled_tasks, assigned_tasks and start position differ.
- R2 the decision is one B3 call under `--strategy full_reorder`, cost realized, gate none, with a human projection
  admitted; its trigger is `recognition_changed` or `no_current_task`, not `task_committed`.
- R3 the heads of the plain-cost and the realized-cost winning orderings are DIFFERENT tasks at that decision.
- R4 in the plain-cost winner the conflict lies after the head and starts before T_h: `holds[0] = 0`, some
  `holds[k] > 0`, k ≥ 1, within the assessed window.
- R5 the plain-cost gap between the two winners is smaller than the cumulative shift of the plain-cost winner.
- R6 read per decision (same tick, pool, position) from two runs differing in cost_strategy only; completion ticks are
  information, not the comparison.
- R7 plain side: every ordering's plain cost at the decision; realized side: the winner's holds and cumulative
  shifts, the hold sent, validity and minimality of the later hold by F1's sampling.
- R8 both priors.
- R10 nothing else changes: no code under `shared/` or `mesa_sim/`, no constant, no layout, scenario_80 / 81 untouched.

## The scenario

| | scenario_80 | scenario_83 |
|---|---|---|
| human start | (−600, 400) | **(−430, 400)** |
| human scheduled_tasks = assigned_tasks | item_0 → kitting_table_0, item_3 → kitting_table_1 | **item_3 → kitting_table_1, item_0 → kitting_table_0** |
| robot start, assigned_tasks | (−100, −400); item_1, item_6, item_4 → kitting_table_0, item_7 → kitting_table_1 | the same |

Why this script and this timing. The robot's side fixes where a flip can be cheap: under plain cost the course is
7, 4, 6, 1 and the only decision with a small gap between heads is the `no_current_task` after item_4's delivery at
kitting_table_0 (step 159), pool {item_1, item_6}, where (6, 1) costs 64.86 and (1, 6) 66.30 — a gap of 1.44 ticks
(at the first decision the gap between item_7-headed and item_6-headed orderings is 39.9 ticks, after item_7 about
117; no hold of that size exists in this domain, whose stationary segments are one tick each). On env_layout8 the
human's walks (item_0: shelf_0 → kitting_table_0 from the north-west; item_3: shelf_3 → kitting_table_1) and the
robot's short tasks (kitting_table_0 ↔ shelf_1 to the south-west, ↔ shelf_6 to the south-east) meet only at the
table itself, so the conflict is a table convergence: the human must be standing at kitting_table_0 releasing item_0
while the item_1 entry of (6, 1) approaches it, and its projection must end before the item_6 entry of (1, 6)
approaches. That puts the human's item_0 release at about step 221. One delivery cannot occupy the human that long
(the room's diagonal is 112 ticks), so the human does item_3 first, from a start on the north wall whose 68-tick
fetch walk (start → shelf_3) sets the timing: item_3 released at 96, then the 86-tick walk from kitting_table_1 to
shelf_0 (99–184), the grasp at 185, the 34-tick carry, the release at 221, done at 222. Nothing else was tuned:
no constant, no designation, no position of the robot's.

The window is narrow, and that is a property of the robot's side, not of the tuning: the two orderings' second
entries reach kitting_table_0 1.44 ticks apart (the gap), so the human's projection must end inside a span about
three ticks wide. Measured during the design with a scratch scan of the human's start x (the in-process capture of
`check.py`, the start varied; not regenerated by the committed script): start x = −410 gives a hold of 2 before
item_1 (a flip), −430 a hold of 3 (this scenario), −390 a hold of 1 (no flip: 1 < 1.44), −370 and nearer no hold;
at −450 item_0 clears θ on the tick of item_4's completion latency, the decision is taken at 157 by
`recognition_changed` with T_h 66.75 and there is no hold. −430 sits in the middle of the window.

## The decision (`check.py`, `checks.md`; both priors identical at this decision)

Step 159, trigger `no_current_task`, pool {item_1, item_6}, robot at (−680.5, −250.5) (kitting_table_0, just after
item_4's release), projection of item_0 admitted (belief 0.815 off / 0.833 on; T_h 63.75 on the projection clock,
222.75 absolute).

| ordering | plain cost | realized cost | holds per entry | cumulative shifts | share past T_h |
|---|---|---|---|---|---|
| 6 1 (plain-cost winner) | **64.86** | 67.86 | [0, 3] | [0, 3] | 0.06 |
| 1 6 (realized-cost winner) | 66.30 | **66.30** | [0, 0] | [0, 0] | 0.04 |

- R3: head under plain cost item_6, under realized cost item_1. The plain run's B3 call at the same step has the same
  trigger, pool and plain costs (its `[meta-ord]` lines: `head=item_6 cost=64.86`, `head=item_1 cost=66.30`); the
  realized run's read `head=item_6 cost=67.86`, `head=item_1 cost=66.30`, `[meta-win] holds=0,0 shift=0`,
  `[meta-b3] ... winner=item_1 hold=0 T_h=63.75 candidates=2 ordering=item_1 > item_6`.
- R4: (6, 1) holds [0, 3]: the hold is before entry 2 (item_1); item_6 realized alone has hold 0; the hold sent is
  holds[0] of (1, 6) = 0. Entry 2 of (6, 1) starts at 30.10 and its carry reaches the table at 60.86, before
  T_h = 63.75.
- R5: gap 66.30 − 64.86 = **1.44** < cumulative shift of the plain-cost winner **3**.
- R7, validity: (6, 1) at its realized plan sampled at 0.001 tick over the assessed window, rule (a) 0, rule (b) 0,
  minimum distance while moving 51.02 cm; minimality: at cumulative shift 2 the sampling finds 1 rule (a) and 48
  rule (b) samples (49.22 cm). (1, 6) at its realized plan (no hold): rule (a) 0, rule (b) 0, minimum 58.55 cm.
- The plain side: `permutation_costs.py` prices only from the robot's start, over `assigned_tasks`, so it is not used
  here; the plain run's `[meta-ord]` lines (with a pool of two, both orderings) and `check.py`'s `realize()` against
  no human plan give the plain costs, and they agree. Extending the script to price from a decision is scope, not
  done.

The geometry of the conflict. The human's projection stands at (−709.8, −221.6) from 59.75 to T_h = 63.75. The
item_1 entry of (6, 1) approaches from shelf_1 (south-west) and its carry ends at (−723.2, −269.0), **49.22 cm** from
the stand point; the item_6 entry of (1, 6) approaches from shelf_6 (south-east) and ends at (−679.0, −271.5),
**58.54 cm** from it. With min_separation 50 cm the first violates over its last centimetre of approach
(violating shift intervals of entry 2: (−0.11, 0.94), (0.89, 1.94), (1.89, 2.94), from the human's stand segments;
the minimal-shift search from 0 returns 3) and the second is clear. The margin on the conflict is 0.78 cm of projected
arrival geometry: the two approaches end at different points of the table's 30-cm arrival radius, and the human,
standing north of the table, is inside s of one and outside s of the other. Recorded as what the case rests on.

## The executed runs (`sweep/`, `sweep.sh`; completion from the world fact, the robot's last release + 1)

| run | heads | completion | declared | executed holds | human releases | min `[sep]` |
|---|---|---|---|---|---|---|
| s83 realized, prior off / on | 7 4 **1 6** | 226 / 226 | 228 | 0 | 96 (table_1), 221 (table_0) | 42.87 cm at 223 |
| s83 plain, prior off / on | 7 4 **6 1** | 224 / 224 | 226 | 0 | 96, 221 | 37.48 cm at 221 |
| s80 realized, prior off / on | 7 4 6 1 | 224 / 224 | 226 | 0 | 53 (table_0), 172 (table_1) | 408.44 cm at 105 |
| s80 plain, prior off / on | 7 4 6 1 | 224 / 224 | 226 | 0 | 53, 172 | 408.44 cm |

- The one-variable comparison: scenario_80 at the same settings takes 7 4 6 1 under both cost strategies and never
  meets the human; scenario_83's human script moves the head of the last pair under realized cost and nothing else
  in the course (the two cost strategies of scenario_83 take the same course to 159, the same triggers and heads;
  scenario_83's decisions before 159 differ from scenario_80's in the trigger ticks the human's script sets — the
  `recognition_changed` ticks and, with them, which trigger takes the boundary after item_7 — with the same heads).
- The decision sequences differ between the priors before the decision only in the `recognition_changed` ticks
  (51 / 156 off, 33 / 140 on); the decision of interest is at 159 under both, by the same trigger, and the executed
  runs are identical from there.
- Under realized cost the robot spends 2 more ticks than under plain (226 against 224: the 1.44 of the reordering
  plus quantisation) and never holds. Under plain the robot's item_1 carry reaches the table at 221 while the human
  releases item_0 there: 37.48 cm, the meeting the projection saw. Under realized the robot's item_6 carry reaches
  the table at 223, a quarter tick past T_h (222.75), and the human, whose script ended with that release, is still
  standing there: 42.87 cm, past the projection. In execution both orderings come within min_separation of the human
  at kitting_table_0, one inside the assessed window and one past it; the decision is on the projection, which ends at
  the human's release (the known arrival past the projection, as scenario_81's record has it). The projected stop
  points differ from the executed ones by 10–15 cm (step quantisation of the arrival), which is why 49.22 cm projected
  is 37.48 cm executed and 58.54 cm projected is 42.87 cm executed.
- `recognition_changed` at 156 (off) / 140 (on), pool {item_4, item_1, item_6} with item_4 current: the winning
  ordering is 4 > 1 > 6 (4 6 1 carries a hold of 2 before its item_1 entry) — a flip of the tail only, which changes
  the `ordering=` field and nothing the robot does (R3's point).
- Both agents end at kitting_table_0 and stand: the `[sep]` ticks below 50 cm after completion (113 / 115) are two
  finished agents standing, not motion.

## Drift

With scenario_83 registered (the only change to code), the twenty T-B Q7 baselines (`analysis/tb1a_destination/sweep/`,
the five plus s50 / s70 / s71, and `analysis/tb1b_two_tables/sweep/`, s80 / s81; both priors, `single_task`)
regenerate byte-identical (md5 against the READMEs). The four scenario_80 runs here under `full_reorder` reproduce
tb1b's note (completion 224, both priors, head order 7, 4, 6, 1, no hold).

## Regenerate (repo root)

    analysis/tb1c_realized_flip/sweep.sh analysis/tb1c_realized_flip/sweep
    PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python analysis/tb1c_realized_flip/check.py \
        > analysis/tb1c_realized_flip/checks.md

`check.py` runs the four scenario_83 conditions in process (about 30 s), prices every ordering at every B3 call both
ways, finds the decision, prints the tables above and the sampling, reads the completion ticks from `sweep/` when it
exists, and exits non-zero on a defect. Logs are local (git-ignored); their md5s, at a5f6b8c with the scenario
registered:

| log | md5 |
|---|---|
| s83_realized_off | 7b719acbbf4c63020146a83fbd5f3ff8 |
| s83_realized_on | 36f29241b7f85f0255e14284d98e117e |
| s83_plain_off | 220caec66a24d0f5e208f5aae8e4f701 |
| s83_plain_on | 1a36fb4218cc4916cb1fc327ae904f61 |
| s80_realized_off | 004075a3e44afeef4ed611b2211f1a0b |
| s80_realized_on | ab6e64456ff45a03c4e49d4e9e101aed |
| s80_plain_off | 3cde041d12b07f80d18b521318a511bb |
| s80_plain_on | 5efac49ff330314119ab05e16a25a1fd |

## D3 (dd880be): `task_committed` is not a trigger — the logs from here on

Regenerated at dd880be with the same command, superseding the table above. Only the trigger set changed
(`shared/meta_planner.py`, `evaluate_triggers()`: `task_committed` removed; `docs/design_decisions.md`, "D3:
task_committed is not a trigger"). Against the previous logs, checked per tick: every `[sep]` line, every human
line, every `[IR] step=` and `[IR-dist]` line and the `[run]` header are byte-identical, and so is completion. What
changed: the `[meta*]` lines of the removed `task_committed` decisions (32 in these logs); and the executor's
bookkeeping, positions and ticks identical — no `_load_plan` at the grasp (the removed decision's reload of
`deliver_already_held`), a later `continue_plan` mapping `action_index 2->0` / `3->1` instead of `0->0` / `1->1`,
and `_on_task_complete` on the 4-action plan (`action_index=4 plan_len=4`) instead of the 2-action one.

HOLDS PLACED BY `task_committed` in the previous logs (their `[hold] … trigger=` field): none; no hold changed.

`check.py`'s defect test "the decision's trigger is task_committed" (R2) is vacuous from D3 on: that trigger no
longer exists. The script is not edited.

| log | md5 |
|---|---|
| s80_plain_off | 601f4ef4120ecc390d80966f01c3d698 |
| s80_plain_on | d16efce5728e7698c56cb56b40930863 |
| s80_realized_off | 977403dd962b42a6209f51494afb7483 |
| s80_realized_on | 121f2fe5b1f793019c1203ed1a83b868 |
| s83_plain_off | 02d1d91f37f53dfbb4876030cd860350 |
| s83_plain_on | ebd19106e7a441b77fdc8de5973f91b3 |
| s83_realized_off | 0a5a2bc13ab3c5705c9f767e84f8427a |
| s83_realized_on | 7f3d9a97489fbfa4f2ae5825a771efd5 |

## T-C2b (06093ee): the action-level human executor — the logs from here on

Regenerated at 06093ee with the same command, superseding the table above. CAUSE: the human's per-task completion
tick is dropped (`docs/design_decisions.md`, "The human action script (T-C1, decided)", AS BUILT T-C2b): its
executor is action-level and spends no tick between two tasks, and the human projection no longer carries that tick
(`HUMAN_TASK_COMPLETION_LATENCY` = 0). Against the previous logs every human line is identical once the human is
one tick earlier per task it completed before that tick (`task=` now `None`; the `_on_task_complete: human_0`
line and the human's `[planner]` lines are gone, one `[human] … primitive` line per primitive is new). Where the
human projection's shorter end reaches a hold, the hold is one tick shorter — the ruling in the AS BUILT note, not a
defect. Per log: the human's dropped ticks | first tick a world line (`[sep]`, `[IR] step=`, robot) differs |
completion (world tick) old -> new | holds (start:planned) old -> new.

| log | dropped | first diff | completion | holds old | holds new |
|---|---|---|---|---|---|
| s80_plain_off | 55, 174 | 55 | 224 -> 224 | - | - |
| s80_plain_on | 55, 174 | 55 | 224 -> 224 | - | - |
| s80_realized_off | 55, 174 | 55 | 224 -> 224 | - | - |
| s80_realized_on | 55, 174 | 55 | 224 -> 224 | - | - |
| s83_plain_off | 98, 223 | 98 | 224 -> 224 | - | - |
| s83_plain_on | 98, 223 | 98 | 224 -> 224 | - | - |
| s83_realized_off | 98, 223 | 98 | 226 -> 226 | - | 190:2 |
| s83_realized_on | 98, 223 | 98 | 226 -> 226 | - | 190:2 |

| log | md5 |
|---|---|
| s80_plain_off | f79cdae4584d13ac8124e37eb4bcfc64 |
| s80_plain_on | 3dd3960ca84ac61c99490974d499db30 |
| s80_realized_off | 5b7fb8a80b4bd906c2fffbf472d5f413 |
| s80_realized_on | 452d508e29aac60c33228e20038e1fc8 |
| s83_plain_off | e2493ddc29dae06681486b6714bf1678 |
| s83_plain_on | 8e0d42f4c59676904a925f4516465b15 |
| s83_realized_off | 2fc8cf8de5c4f9863ea28d7d522f6bde |
| s83_realized_on | 730bfd280ce78befb0fed3301692b36a |

## T-H3: the human's script on the stack machine — the logs from here on

Regenerated after T-H3 with the same command, superseding the T-C2b table. CAUSE: every scenario's human script is a
`Script` run by the human's stack machine (`docs/design_decisions.md`, "T-H: the human behaviour model", as built
T-H3); the C1 list form is deleted. Against the T-C2b logs every line outside `[human]` is byte-identical, the human's
step lines included: the robot sees the same body. The `[human] … primitive k: <action>` lines are replaced by the
record's transitions (`entered:<task>`, `completed:<task>`), the step-0 one printed after the executor's `_load_plan`
line. Each log now has its `.rec` stream beside it (the human executor's record, one `[rec]` line per tick; the first
non-empty `.rec` baselines), git-ignored like the logs.

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| s80_plain_off | 341630559a75efc01c31301002c1c970 | 8cf0930761924a3aab1f1713f3f4bf29 |
| s80_plain_on | 0ea6185153e9cf92364cabc22e21c0df | 8cf0930761924a3aab1f1713f3f4bf29 |
| s80_realized_off | 45131c21bdf6a70155eb55d06f7c1995 | 8cf0930761924a3aab1f1713f3f4bf29 |
| s80_realized_on | 61d72d8c85e8f4bdbba12bbae4cdcb7e | 8cf0930761924a3aab1f1713f3f4bf29 |
| s83_plain_off | b14941d5ac19fde74e736840c7b43ce7 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| s83_plain_on | 4a122858982c7c868c81a8dea9d003bd | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| s83_realized_off | 7e5218e4e8640b0688729b857dac47e1 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| s83_realized_on | b3913816203cb94cabc51562e64e4993 | b9f1a0ec26cfa8c022b9951e9ec1b34b |

## T-H4: the record's queries and the coverage line — the logs from here on

Regenerated after T-H4 with the same command, superseding the T-H3 table. CAUSE: the loader prints one `[coverage]`
line per script entry for each robot observing the human, after the `[run]` headers (`docs/design_decisions.md`, "T-H:
the human behaviour model", as built T-H4). Against the T-H3 logs every other line is byte-identical, and every `.rec`
stream is byte-identical (its md5 unchanged).

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| s80_plain_off | 74cc12b7bdc77c65d5ff2a71d0852ce0 | 8cf0930761924a3aab1f1713f3f4bf29 |
| s80_plain_on | eecdf35266a4a4e89cb5a6924b50f487 | 8cf0930761924a3aab1f1713f3f4bf29 |
| s80_realized_off | 0ae7239c50a1efb172a6dd195e546204 | 8cf0930761924a3aab1f1713f3f4bf29 |
| s80_realized_on | 8acd7f0596cfb665e9807fece14c80ff | 8cf0930761924a3aab1f1713f3f4bf29 |
| s83_plain_off | 509216b9e3c7820773a885b6de334707 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| s83_plain_on | b871144601a54d9bb230481d99c11b2d | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| s83_realized_off | 938770a788056decfea88a712c85b965 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| s83_realized_on | d71f1095f56a7256eee1e406acc9f9dc | b9f1a0ec26cfa8c022b9951e9ec1b34b |

## T-H follow-up: the scenario-coverage line — the logs from here on

Regenerated after the T-H follow-up with the same command, superseding the T-H4 table. CAUSE: the loader prints
one `[scenario-coverage]` line per robot observing the human, after its `[coverage]` lines: the script's composition
and scenario coverage (`docs/design_decisions.md`, "T-H: the human behaviour model", as built T-H follow-up). Against
the T-H4 logs every other line is byte-identical, and every `.rec` stream is byte-identical (its md5 unchanged).

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| s80_plain_off | 6e227a559305055f3c41202f80e9941d | 8cf0930761924a3aab1f1713f3f4bf29 |
| s80_plain_on | 942417aae5f2a563e4ddee946ee68aea | 8cf0930761924a3aab1f1713f3f4bf29 |
| s80_realized_off | c479c77be59788c3523827a624949197 | 8cf0930761924a3aab1f1713f3f4bf29 |
| s80_realized_on | 1a66f2d38ef2db57b897ac163fc59edf | 8cf0930761924a3aab1f1713f3f4bf29 |
| s83_plain_off | 702584d73230367f9f77d7b8a478810a | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| s83_plain_on | 47a70872338b3eb232ac47a2ae958ded | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| s83_realized_off | cc6125e8898e55b42f3faa36cee487a8 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| s83_realized_on | 5d93baad6ee5ac87a483bf9ea99787d5 | b9f1a0ec26cfa8c022b9951e9ec1b34b |

## T-L stage 3: the serial ids — the logs from here on

Regenerated after T-L stage 3, superseding the T-H follow-up table. CAUSE: the rename to the serial ids (`docs/design_decisions.md`, "Layouts, setups and scenarios: the three artefacts of
a run", ruling 4 as amended, ruling 6); the runs do not change. Logs are named `<layout id>_<scenario id>_<run
options>.log` (ruling 6), each `.rec` beside its log; `docs/rename_table.md` maps the old tags (its last table).
Against the stage-2 logs (99563cc, run from scratch under the old ids and paired through the rename table) every log
differs in the `[run_mesa]` line alone (`layout=` and `scenario=`), and every `.rec` stream is byte-identical. T-L
stages 1 and 2 had changed the same line alone (the setup id added, then its serial id), with no section here; the
`.rec` md5s equal the T-H follow-up table's.

Regenerate from the repo root with `analysis/tb1c_realized_flip/sweep.sh analysis/tb1c_realized_flip/sweep`.
`check.py` is left as it stands (a record at its commit; it reads the registry shape from before T-L stage 1 and
the old log names).

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_08_scenario_s06_01_plain_off | 81be85f96870cf5dd54af9b35ec62920 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_plain_on | e91542f57a1d053878059fe975d6cfa1 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_realized_off | fda5316eded9f2afdf3dc190c9001350 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_realized_on | 38c80f2e69dc4fd4129a5668ed7d32ec | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_03_plain_off | ef0d7f0388c6178b5a68c7667ec66873 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_plain_on | a3e7fd437eab365a1fdc120d4bbba475 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_realized_off | 1eb4be9d9268bbbe68a472a85fe78b8f | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_realized_on | ebe3d1cda8a8d81b9726503e16643f92 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
