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

## T-D R and E Stage 1: the recognizer without `unknown` — the logs from here on

Regenerated at the T-D Stage 1 build (27 September 2026, cycle 1 session 1.3), superseding the T-L stage 3 table.
CAUSE: a behaviour change of the recognizer (`docs/design_decisions.md`, "T-D R and E"): the `unknown` hypothesis,
u and the grade are gone and the belief is normalised over the live hypothesis set H (R1, R6); the `[IR]` line
carries the lifecycle state, the adequacy finding and the members' tail probabilities; the `[run]` header names
the test level and the body's speed; the `[IR-boundary]` line no longer says "+ unknown"; `none(unknown)` refusals
are gone. The `.rec` streams are byte-identical to the stage 3 ones (the human does not react to the robot). The
gate is unchanged; its input is now the leader's share over H, so admissions moved, and in prior-off runs the
robot's own remaining item is admitted once it is the lone live task after the human's last task (world lines
differ from that tick). Measured in session 1.4, not corrected here. Command: `analysis/tb1c_realized_flip/sweep.sh analysis/tb1c_realized_flip/sweep`.

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_08_scenario_s06_01_plain_off | ce35aa74a3e5e1389d30e8d62a142dd6 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_plain_on | 353d3b6e043b131792b4b66095a96c1f | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_realized_off | d1be76378eb7238911194a6b844ee99e | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_realized_on | d0898e09833691bb85152ca1f4fad03a | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_03_plain_off | 8ed88de1916b53875d81006259202a6f | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_plain_on | 2de792c8229ec8bc70ee1e2e7c05372a | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_realized_off | 0e6eae85c312d4da0471ec2960c6f79f | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_realized_on | 358511c6c9c6198045ea644eeec4e0d4 | b9f1a0ec26cfa8c022b9951e9ec1b34b |

## T-D Stage 1, E6 amended: stationary-phase members — the logs from here on

Regenerated at cycle 1 session 1.3b (27 September 2026), superseding the T-D R and E Stage 1 table. CAUSE: E6
amended (design_decisions.md, "T-D R and E"): a stationary phase within its priced duration is a member of the
adequacy test with S = 1. Only `[IR]` lines differ from the Stage 1 logs, and in them only the finding and the
tails (members added at S = 1; the belief and every existing member's S unchanged); every other line and the
`.rec` streams are byte-identical. Same commands as the section above.

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_08_scenario_s06_01_plain_off | f1ceaf546f6138df90126d3de0dd0cbb | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_plain_on | 9a2721aa3fc921ff9333768e00ccda02 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_realized_off | be05b6251fcc3c5547999bcb30d0f3a7 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_realized_on | b9f756085305e49091005cbde9dc27ba | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_03_plain_off | f0d15133ca437f4bc11c1da732c73efe | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_plain_on | 0951585744111e81e91f444c2128d76c | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_realized_off | 94a9b707f68c58585001aa0cd16edecb | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_realized_on | d395d91a396a323670b846f0ffbf1c88 | b9f1a0ec26cfa8c022b9951e9ec1b34b |

## T-D cycle 1.5b: E8, E9, E10 and G1 — the logs from here on

Regenerated at cycle 1 session 1.5b (27 September 2026), superseding the "E6 amended" table above. CAUSE: E8 (the
advance tick a member at S = 1), E9 (s_exp by the Projector's attribution), E10 (the belief's evidence per phase
L(v·D)) and G1 (the guard on admission: `_clears_gate` also requires the leader's hypothesis adequacy to be adequate;
new refusals `none(leader_no_observation)`, `none(leader_inadequate)`); design_decisions.md, "T-D R and E", "1.5
rulings". Every `[IR]` line on a live tick differs (the new `leader_adequacy=` field; the tails under E8, E9); `[IR-dist]` differs
where standing now charges the belief (E10); decisions differ at admissions (G1) and wherever the belief moved.
World lines (the agents' per-tick lines) changed in 1 of 8 (s06_03 realized off). The `.rec` streams are byte-identical to the table
above. Per-run diff and the acceptance: `analysis/td_stage1b/` (`baseline_diff.txt`, REPORT.md).

Command (from the repo root; the same as the sections above; restated because 7f4559a had dropped them, restored in 1.5c):
`analysis/tb1c_realized_flip/sweep.sh analysis/tb1c_realized_flip/sweep`

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_08_scenario_s06_01_plain_off | 5441e3e44bb86b2d47007a4792dd1739 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_plain_on | c5c8964185e3cc2d317ed86c935fb7e7 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_realized_off | 98d32dbd4fe4ccdf6f4c5d00f25a2ccc | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_realized_on | 25a26eb6b44f3779dee9f94868554765 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_03_plain_off | 2f418f3ff8dfc851d5a3e3981fc39969 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_plain_on | 965c827855eaa688a3fc51ba64099e79 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_realized_off | 3ade34d4da811f67c654b7a1a2f7ac8c | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_realized_on | dbd8e0e7adab2415edd8d7db9209c7f7 | b9f1a0ec26cfa8c022b9951e9ec1b34b |

## T-D cycle 1.5c: E6 second amendment — the logs from here on

Regenerated at cycle 1 session 1.5c (27 September 2026), superseding the 1.5b table above. CAUSE: E6 amended a second
time (design_decisions.md, "T-D R and E"): a stationary tick with s ≤ s_exp in any phase with s_exp > 0 is an
observation with S = 1 (the latency tick after a grasp and after a boundary), and no hypothesis is a member on a
boundary tick. `[IR]` lines differ in the finding, the leader's adequacy and the tails on those ticks; `[IR-dist]`
is identical on every common tick (L = 1 there before and after; runs that end later add exhausted ticks); admissions that waited for the first walking tick after a boundary now
come on the latency tick (b + 1). World lines changed in 1 of 8 (s06_03 realized off). The `.rec` streams are byte-identical to the
table above. Same command as the 1.5b section. Diff and acceptance: `analysis/td_stage1b/` (`baseline_diff_15c.txt`,
REPORT.md, section 1.5c).

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_08_scenario_s06_01_plain_off | 7bad04298efabe9f433814f1b052a7b3 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_plain_on | 56b9fd35be350824d5a179ed372a920b | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_realized_off | a57beb0042671d6f864617087709388f | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_realized_on | 6665cba47edcc0ffe5c4c33b893b9274 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_03_plain_off | 50933ea7e5eebaa8e3ba1409bbcdfceb | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_plain_on | f43e7991c139e225943de42539b1e024 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_realized_off | 762b472bae87c0f4114403e7f4a884ec | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_realized_on | 5346b3572f22bf62287d6d648aa012d9 | b9f1a0ec26cfa8c022b9951e9ec1b34b |

## TB.2b: the cognitive loop does not end with the task pool — the logs from here on

Regenerated at TB.2b (27 September 2026), superseding the 1.5c table above. CAUSE: the robot observes and recognizes
on every tick; after its terminal return it evaluates no trigger, decides nothing and does not step the executor
(design_decisions.md, "The cognitive loop does not end with the task pool"). Each log gains `[IR]` and `[IR-dist]`
lines from the tick after the declared completion tick to the run's last tick, and within every tick the robot's
`[IR]` and `[IR-dist]` lines now precede its `[meta-trig]` line, so every md5 changed. Criterion, met in all 8: the
log with every `[IR*]` line removed is byte-identical to the 1.5c log, the `[IR*]` lines are byte-identical up to and
including the declared tick, and the `.rec` streams are byte-identical to the table above. Command: `analysis/tb1c_realized_flip/sweep.sh analysis/tb1c_realized_flip/sweep`.
Check and measurements: `analysis/tb2b_exposed_interval/` (`baseline_diff.txt`, REPORT.md).

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_08_scenario_s06_01_plain_off | 547ee8a37348c9cead0b34ffbf2ee1a6 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_plain_on | 60051eb91578846687040f757e308fe7 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_realized_off | 9c72f9afa843ff8a10318457b7ddd560 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_realized_on | 80e4303594ab810034033fb1243f35ee | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_03_plain_off | ec90ea660c72f930248d5bc925601c04 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_plain_on | 653a7bec2ebdd3d10444d1e5c9b38de1 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_realized_off | 726a0c8a87a9b4db210d96a7eb016bd6 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_realized_on | 825dd5add61122d239b199f5b42ce1f5 | b9f1a0ec26cfa8c022b9951e9ec1b34b |

## L-build: T-D L, the belief lifecycle — the logs from here on

Regenerated at L-build (28 September 2026), superseding the TB.2b table above. CAUSE: design_decisions.md, "T-D L: the
belief lifecycle", as amended on the L-records report: the episode boundary is the observed agent's completion of a
terminal action (L1); a hypothesis is retired while its terminal fact holds and re-enters at 1/|H| (L4, `[IR-reentry]`,
new); `recognition_changed` also fires on the belief's episode boundary (L5 B) and on the recorded hypothesis's
inadequacy (retraction, L2 (ii)). Two format changes reach every log: `[meta-trig]` names the condition of a
`recognition_changed` (` cause=entered | replaced | boundary | retraction`), and `[IR-boundary]` names the completed
action (`completed place(item_2,kitting_table_0):` for `completed a task:`); so every md5 changed. No criterion of
identity (L changes behaviour); the `.rec` streams are byte-identical to the table above in all 8. With the two
format changes undone (`analysis/l_build/baseline_diff.py`): identical in 6 of 8 (L08 s06_01_plain_on, L08 s06_01_realized_on, L08 s06_03_plain_off, L08 s06_03_plain_on, L08 s06_03_realized_off, L08 s06_03_realized_on); the
recognizer's lines and the triggers moved, the robot's behaviour not, in none; the robot's behaviour
(`[meta]`, `[hold]`, `[sep]`, its lines) moved in L08 s06_01_plain_off, L08 s06_01_realized_off. Each moved number with its ticks and cause:
`analysis/l_build/REPORT.md`. Command: `analysis/tb1c_realized_flip/sweep.sh analysis/tb1c_realized_flip/sweep`.

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_08_scenario_s06_01_plain_off | 69168a8c4d73bfddac370b723b1ed24b | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_plain_on | d4a82dce9007513a8e5d607495d77f29 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_realized_off | 5b3c13c90958233b456b6e704d65e2f6 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_realized_on | 28eb0514c3371c34114d56cca6e13517 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_03_plain_off | c1f76dbbe5ca1cad3a6a9d11838c47c0 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_plain_on | 5089a5b28d8ae6c95f1be858c798acf7 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_realized_off | 658eae46cb4e4d2f044791fc83a38481 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_realized_on | 526f6fa31a183744edbf616cfb10dfd0 | b9f1a0ec26cfa8c022b9951e9ec1b34b |

## P-build: T-D P, the fallback projection — the logs from here on

Regenerated at P-build (28 September 2026), superseding the L-build table above. CAUSE: design_decisions.md, "T-D P:
the fallback projection": where admission refuses and a human is observed, the decision realizes against the fallback
projection (the human's observed position and last displacement: standing, or a straight continuation to the
workspace boundary or the first fixed object's arrival radius, over each candidate's span); a candidate whose violation
is cleared only by the projection's end is refused (` refused=fallback` on `[meta-cand]`), and with none eligible the
robot waits without a task (`[meta] … wait`, `[meta-b3] … selection=wait`). Format: `[meta-proj]` names a fallback as
`projection=fallback refused=<the refusal's reason>`, so every log whose run refused an admission changed md5. No
criterion of identity (P changes behaviour). The `.rec` streams are byte-identical to the table above in all 8; with
the prior on, the recognizer's lines (`[IR]`, `[IR-…]`) are byte-identical in every run; with P's format additions
undone, the first differing line of every changed run is at tick 0, a decision under the fallback. WAITS: a run whose
robot is still waiting at its last tick has no completion tick; the table records "waits: occupied target (X)" for it
(the human's script ends standing at the robot's delivery table; the six scripts predate T-C2c's authoring convention
and are not edited; design_decisions.md, "T-D P", the deadlock). Completion is the world tick (T6), before (L-build) and
after. Command: `analysis/tb1c_realized_flip/sweep.sh analysis/tb1c_realized_flip/sweep`.

| log | md5 (.log) | md5 (.rec) | completion before | completion after |
|---|---|---|---|---|
| env_layout_08_scenario_s06_01_plain_off | 0a9a0bf95dcc56444178b02e2188748a | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 224 |
| env_layout_08_scenario_s06_01_plain_on | 62bc4b9fe47f3912bf2b48585801efe1 | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 224 |
| env_layout_08_scenario_s06_01_realized_off | 70b0875d92c479be9af11b195ebfe5c2 | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 225 |
| env_layout_08_scenario_s06_01_realized_on | ef34c4c39f7dd5a4e30e35e83dcf3d9a | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 224 |
| env_layout_08_scenario_s06_03_plain_off | e6c4c856657bd3445180a6e0abb495e1 | b9f1a0ec26cfa8c022b9951e9ec1b34b | 340 | 340 |
| env_layout_08_scenario_s06_03_plain_on | dcf509e637bcf411ea1b83c12b8ac73c | b9f1a0ec26cfa8c022b9951e9ec1b34b | 224 | 224 |
| env_layout_08_scenario_s06_03_realized_off | 5b3ee082a1e6cc81102aaabe822a6f87 | b9f1a0ec26cfa8c022b9951e9ec1b34b | 340 | 240 |
| env_layout_08_scenario_s06_03_realized_on | 96cc0b0eff7c5766894e22079ceeae19 | b9f1a0ec26cfa8c022b9951e9ec1b34b | 226 | waits: occupied target (X), from 220 |

## P4-build: T-D P4, persistence, and projection_expired — the logs from here on

Regenerated at P4-build (28 September 2026), superseding the P-build table above. CAUSE: design_decisions.md, "T-D P",
P4 and Q6: the fallback projects the observed persistence only (a straight run of k ticks continued k ticks, cut at the
workspace boundary or the first fixed object with no stand after it; a stand of k ticks held k ticks; no previous
observation, none), realized as any projection (F1), and `projection_expired` re-decides when the fallback a decision
rested on reaches its end (`[meta-trig] … trigger=projection_expired`, new); the refusal and the wait of the P-build
are removed. No criterion of identity (P4 changes behaviour). The `.rec` streams are byte-identical to the table above
in all 8; with the prior on, the recognizer's lines are byte-identical to the L-build table's. A run whose robot has
not delivered its last item at the run's last tick is recorded as "does not complete: occupied target (X), holds
lengthening, from <tick>": the human's script ends standing at the robot's delivery table (the scripts predate T-C2c's
authoring convention and are not edited), and from the first hold on that final stand the robot holds and
reconsiders at each expiry of a longer stand (scenario_s01_06 prior on, 800 steps: expiries at 165, 213, 309, 501,
holds 48, 96, 192, 384, never complete). Completion is the world tick (T6), before (P-build; "waits" there) and after.
Command: `analysis/tb1c_realized_flip/sweep.sh analysis/tb1c_realized_flip/sweep`.

| log | md5 (.log) | md5 (.rec) | completion before (P-build) | completion after (P4) |
|---|---|---|---|---|
| env_layout_08_scenario_s06_01_plain_off | e24c084e2348d583eeeac0e491f02590 | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 224 |
| env_layout_08_scenario_s06_01_plain_on | f64583f1d55c4ba836b23f6a28197779 | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 224 |
| env_layout_08_scenario_s06_01_realized_off | 01738643503d860be585f4b3c1be17f7 | 8cf0930761924a3aab1f1713f3f4bf29 | 225 | 224 |
| env_layout_08_scenario_s06_01_realized_on | bfaeba739db5cb7f578f5f0e7ca84750 | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 224 |
| env_layout_08_scenario_s06_03_plain_off | cdfa4e703859001ab4393d3cb455833c | b9f1a0ec26cfa8c022b9951e9ec1b34b | 340 | 340 |
| env_layout_08_scenario_s06_03_plain_on | 47ceaa56bbc8d1a53d2c43ba0e9d39d5 | b9f1a0ec26cfa8c022b9951e9ec1b34b | 224 | 224 |
| env_layout_08_scenario_s06_03_realized_off | 0dd6d1f4aeab7a8dab96987ee884da8b | b9f1a0ec26cfa8c022b9951e9ec1b34b | 240 | 340 |
| env_layout_08_scenario_s06_03_realized_on | 9bdf7aed2df3252bf2c26a8f08a9b7e5 | b9f1a0ec26cfa8c022b9951e9ec1b34b | waits: occupied target (X) | 226 |

CORRECTION (Track 2.5, 29 September 2026; the table above is left as written): the "340" cells are completions, not the run's end: `env_layout_08_scenario_s06_03_plain_off` completes at 224 (its last release 223) and `env_layout_08_scenario_s06_03_realized_off` at 238 (its last release 237; the log declares `all tasks complete` at 238). The reader counted every `action=place micro=release` line, and after its pool empties the robot's per-tick line keeps its last action and micro (`task=None action=place micro=release`), so the last such line was the run's last tick, 339. `analysis/tb1a_destination/sep_classes.py` (Track 2.5) counts only the releases made while the robot has a task. The "340" cells of the earlier tables of this file are most likely the same reader's artefact; their logs are not kept, so this is not verified.

## 2.5: the exit walk on the six regression scripts (Track 2.5) — the logs from here on

Regenerated at Track 2.5 (29 September 2026), superseding the P4-build table above. CAUSE: `docs/assumptions.md` 1.1:
the human scripts of scenario_s01_01, s01_06, s02_01, s03_01, s04_01 and s06_03 end with the exit walk
`go_to("corner_SE")` (52295f7), and env_layout_02 and env_layout_08 declare the landmark corner_SE. The other
scenarios' scripts are unchanged; their logs and `.rec` streams are byte-identical to the P4-build table (env_layout_08's
new landmark moved nothing). The six scripts' `.rec` streams change from the tick the exit walk begins. Completion is
the world tick (T6), read by `analysis/tb1a_destination/sep_classes.py`: the tick after the robot's last release made
while it has a task; the "before" column is the same reader on the P4-build logs (two cells differ from that table, 224 and 238 for its "340"; the correction above). The `[sep]` minimum is
of the continuous distance; viol / stand / recede are F1's classes (`analysis/f1_robot_responsible/evaluate.py`, its
rule copied into the reader) of the ticks whose continuous minimum lies below min_separation (50 cm): the
near-encounters of `docs/assumptions.md` 4.6.
scenario_s06_03's four logs change, its human from 222 (the exit walk): completion plain 224 / 224 (unchanged),
realized 236 (was 238) / 226 (unchanged), off / on. scenario_s06_01's four are byte-identical.
Commands: `analysis/tb1c_realized_flip/sweep.sh analysis/tb1c_realized_flip/sweep`; `analysis/tb1a_destination/sep_classes.py analysis/tb1c_realized_flip/sweep`.

| log | md5 (.log) | md5 (.rec) | completion before (P4) | completion after (2.5) | [sep] min, continuous (tick) | viol | stand | recede |
|---|---|---|---|---|---|---|---|---|
| env_layout_08_scenario_s06_01_plain_off | e24c084e2348d583eeeac0e491f02590 | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 224 | 412.25 (105) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_plain_on | f64583f1d55c4ba836b23f6a28197779 | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 224 | 412.25 (105) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_realized_off | 01738643503d860be585f4b3c1be17f7 | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 224 | 412.25 (105) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_realized_on | bfaeba739db5cb7f578f5f0e7ca84750 | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 224 | 412.25 (105) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_03_plain_off | fb5e8a43936bfa7ab53553aeac88b94d | c9c444622f25d15abfd849fc495db540 | 224 | 224 | 37.48 (221) | 1 | 2 | 0 |
| env_layout_08_scenario_s06_03_plain_on | 3316cb3f852e8e38a8a11682f7bded1d | c9c444622f25d15abfd849fc495db540 | 224 | 224 | 37.48 (221) | 1 | 2 | 0 |
| env_layout_08_scenario_s06_03_realized_off | d618371426083d9dbb12544fe0384904 | c9c444622f25d15abfd849fc495db540 | 238 | 236 | 90.80 (220) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_03_realized_on | 14f93fee856ed59854e821047ccee258 | c9c444622f25d15abfd849fc495db540 | 226 | 226 | 54.58 (223) | 0 | 0 | 0 |

## G-build: T-D G, admission requires warrant — the logs from here on

Regenerated at G-build (29 September 2026), superseding the 2.5 table above. CAUSE: design_decisions.md, "T-D G:
admission" (AD1 to AD4): the gate also requires the leader to be warranted (commitment: one of the observed human's
assigned tasks, prior on; or the recognizer's observation warrant), and refuses an unwarranted leader as
`none(leader_unwarranted)`; the `[IR]` line ends with `warrant=[<key>=none|observation ...]` over the live
hypotheses, and `[meta-proj] projection=built` names its warrant source (`warrant=commitment`, `observation` or
both). Every log's md5 changes (the `[IR]` field). The diff rule checked on every log against the 2.5 logs: the `.rec`
streams byte-identical in all; prior on, every `[IR*]` line byte-identical once the trailing ` warrant=[...]` is removed,
and every other line identical once `[meta-proj]`'s ` warrant=...` is removed, except in the prior-on runs listed
below, whose first difference is a moved admission of a foreseeable task. Prior on, commitment warrant covers every
assigned task, so only admissions of foreseeable tasks can move. Completion is the world tick (T6),
`analysis/tb1a_destination/sep_classes.py` on both sets; the `[sep]` minimum of the continuous distance and F1's
classes (`docs/assumptions.md` 4.6) as in 2.5. Prior on first.
Prior on: nothing moved beyond the log fields.
Prior off (appendix): scenario_s06_01 (plain and realized) the admission of item_1 at 188 gone; scenario_s06_03 (plain
and realized) the admission of item_1 at 221 gone, refused unwarranted at 223; scenario_s06_03 realized completion 236 →
226, `[sep]` 90.80 → 54.58 cm. `check.py` was not rerun: it reads the registry from before T-L stage 1 (above) and
fails on it.
Commands: `analysis/tb1c_realized_flip/sweep.sh analysis/tb1c_realized_flip/sweep`; `analysis/tb1a_destination/sep_classes.py analysis/tb1c_realized_flip/sweep`.

| log | md5 (.log) | md5 (.rec) | completion before (2.5) | completion after (G-build) | [sep] min, continuous (tick) | viol | stand | recede |
|---|---|---|---|---|---|---|---|---|
| env_layout_08_scenario_s06_01_plain_on | fc03cc9953344aae5a3945346de24eb2 | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 224 | 412.25 (105) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_realized_on | f2b1c2c81d78c7657047699996dd7731 | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 224 | 412.25 (105) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_03_plain_on | 1c4dd4ee4a3c8bd9bfa9ac22e533ba5c | c9c444622f25d15abfd849fc495db540 | 224 | 224 | 37.48 (221) | 1 | 2 | 0 |
| env_layout_08_scenario_s06_03_realized_on | 2c734fb09410644d22f4a8cf8cf97a94 | c9c444622f25d15abfd849fc495db540 | 226 | 226 | 54.58 (223) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_plain_off | 7c086199a3ca526c7ad189ea0e96d835 | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 224 | 412.25 (105) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_01_realized_off | 8b621e3f1f757056ef8a8a3dc5903142 | 8cf0930761924a3aab1f1713f3f4bf29 | 224 | 224 | 412.25 (105) | 0 | 0 | 0 |
| env_layout_08_scenario_s06_03_plain_off | c60a7db0c91a86084328a356985228be | c9c444622f25d15abfd849fc495db540 | 224 | 224 | 37.48 (221) | 1 | 2 | 0 |
| env_layout_08_scenario_s06_03_realized_off | d86b3ef60143f3138296252450878822 | c9c444622f25d15abfd849fc495db540 | 236 | 226 | 54.58 (223) | 0 | 0 | 0 |
