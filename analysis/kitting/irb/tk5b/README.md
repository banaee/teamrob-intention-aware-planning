# T-K part 1, step 5b: the recognition set with context knowledge on (kitting, the idle robot)

The records: design_records.md, "T-K", STEP 5B, PLANNED and the step's entries after it. A basic check, not a coverage
set: the context rooms (env_layout_15 to _18) excluded the human's other deviations on purpose; this set holds them.
Results: `analysis/kitting/mpb/tk5b/REPORT.md` (stage 3; one report for both sets).

**The state the set meets.** The setups (env_setup_08, _09) and the scenarios state no timeline, and the rooms
(env_layout_10, _11) hold a coffee machine and no A/C switch. With context knowledge on, only the state with no raising
fact occurs: coffee_break has the ordinary strength 0.02, or the suppressed strength 0.005 for the 90 ticks after an
observed coffee break; the assigned tasks as a whole have 1. So with two deliveries live each has a prior of 0.49 and
the coffee break 0.0196; with one delivery live it has 0.98 (0.995 after an observed break); with none live the coffee
break has 1, as off.

## The set

- The seventeen scenarios of the IRB as they are: scenario_s08_01 to _04 (env_layout_10, env_setup_08) and
  scenario_s09_01 to _13 (env_layout_11, env_setup_09); their scripts: `analysis/kitting/irb/README.md`.
- The reference (context knowledge off): `configs/kitting/irb/scenario_s0*.yaml`, outputs in
  `analysis/kitting/irb/<scenario>/`. Rerun at HEAD into another folder before this step: every log, `.rec` stream
  and instrument output byte-identical to the committed ones (the drift check).
- The runs with context knowledge on: `configs/kitting/irb/tk5b/` (the reference's run files with
  `context_knowledge: true`, nothing else changed), outputs in this folder.
- Assignment knowledge on, θ = 0.75, test level 0.05, the robot idle (an empty pool).

Commands (from the repo root):

    analysis/instruments/irb/run.sh kitting --expect -o analysis/kitting/irb/tk5b configs/kitting/irb/tk5b/*.yaml
    analysis/instruments/irb/run.sh kitting -o analysis/kitting/irb/tk5b configs/kitting/irb/tk5b/*.yaml
    analysis/kitting/irb/tk5b/read5b.py expected.csv      # the expectations, off against on (below)
    analysis/kitting/irb/tk5b/read5b.py actual.csv        # the runs, off against on (REPORT.md, Appendix A)
    analysis/kitting/irb/tk5b/read5b.py summary actual.csv   # one row per scenario (REPORT.md)

`read5b.py` reuses admission.py's stretches and wrong admissions and g_reading.py's trigger-rule reading (step 4).

## The expectations (stage 1, committed before any run with context knowledge on)

The oracle's tables with context knowledge on (`expected.csv`, `phases.json`; the IRB's rules 29 to 33), from the
trajectory (`trajectory.json`, byte-identical to the reference's in all seventeen: the timeline acts on the robot's
mind only). Each run must agree with its table at 1e-9, as every IRB run. Expected in words (from the reading below):

1. The chain: 0 disagreements in all seventeen.
2. The true task. Every delivery is admitted at or before off's tick. The first delivery (two live): at 8 against 25
   (19 against 27 in s09_10, _11; 7 against 15 in s09_12). A delivery that is the lone one live: on its stretch's
   first tick (admitted on the previous task's pin tick), against 5 to 25 ticks into it. The coffee break: later, 18 to
   30 ticks into its stretch against 10 to 12 (s08_02 93 against 75; s08_03 55 against 44; s08_04 48 against 40; s09_11
   87 against 73; s09_13 76 against 74, where off clears only at 74 after reaching θ at 67). A delivery resumed after a
   break inside it: the same or one tick earlier (s08_03 100; s08_04 91 against 92; s09_13 120 against 121). The
   corner walk (s09_05) and the long stand (s09_06): the resumed delivery at the same tick on both sides (126; 72). The
   change of mind (s09_07): item_2 at 40 against 46, item_1 again at 110 against 135. The misdelivery (s09_08): item_2 at
   82 against 96. item_3 outside the support (s09_09): never, on both sides. After an admission, the gate stops clearing
   for the true task only in s09_08 (item_1 inadequate 66 to 74 on both sides: the delivery to the wrong table).
3. Admissions of a hypothesis that is not the true task, on (off in brackets); gate length, trigger rule's wrong ticks:
   - the coffee break after the first delivery, the second delivery the lone one live (s08_02, s09_02, s09_11): the
     lone delivery from the first delivery's pin tick while the human walks to the machine, 22, 22 and 18 ticks, the
     gate ending below θ, the trigger rule firing on inadequacy on the same tick (off: none);
   - the coffee break inside a delivery at its grasp (s08_03, s09_03): item_1 kept 11 ticks by the gate and the rule
     (off: 5 and 9); at its first walk (s08_04, s09_04): 1 + 8 ticks by the gate, 10 by the rule (off: 1 + 2 and 7);
     mid-carry (s09_13): 9 and 9 (off: 9 and 9);
   - the corner walk mid-delivery (s09_05): 16 by the gate, 16 by the rule (off: 11 and 16); the long stand (s09_06):
     17 and 17 (off: the same); the change of mind (s09_07): 1 and 1, the rule firing on the boundary (off: 1 and 1, on
     the leader's change);
   - the misdelivery (s09_08): after item_2's completion, item_1 (never placed on its table, so still live and the lone
     delivery) is admitted 17 ticks on the exit walk and retracted on inadequacy; then coffee_break 1 tick (off:
     coffee_break 20 ticks on the exit walk);
   - the delivery outside the support (s09_09): item_2, the lone live delivery, 11 ticks while the human delivers
     item_3, then 1 tick before the human starts it (off: coffee_break 13 ticks);
   - the exit walk: coffee_break 31 or 32 ticks on both sides, identical (no assigned task live: its prior is 1 either
     way), except s09_08.

The reading of the expectations, off against on (`read5b.py expected.csv`):

#### 1. The true task, per stretch

| scenario | true hypothesis | ticks | first ≥ θ off | on | admitted off | on | after admission off | on |
|---|---|---|---|---|---|---|---|---|
| s08_01 | deliver_item(item_1) | 0 to 62 | 25 (25) | 8 (8) | 25 (25) | 8 (8) | - | - |
| s08_01 | deliver_item(item_2) | 63 to 125 | 76 (13) | 63 (0) | 76 (13) | 63 (0) | - | - |
| s08_02 | deliver_item(item_1) | 0 to 62 | 25 (25) | 8 (8) | 25 (25) | 8 (8) | - | - |
| s08_02 | coffee_break(coffee_machine_0) | 63 to 134 | 75 (12) | 93 (30) | 75 (12) | 93 (30) | - | - |
| s08_02 | deliver_item(item_2) | 135 to 202 | 140 (5) | 135 (0) | 140 (5) | 135 (0) | - | - |
| s08_03 | deliver_item(item_1) | 0 to 31 | 25 (25) | 8 (8) | 25 (25) | 8 (8) | - | - |
| s08_03 | coffee_break(coffee_machine_0) | 32 to 85 | 44 (12) | 55 (23) | 44 (12) | 55 (23) | - | - |
| s08_03 | deliver_item(item_1) | 86 to 128 | 100 (14) | 100 (14) | 100 (14) | 100 (14) | - | - |
| s08_03 | deliver_item(item_2) | 129 to 192 | 142 (13) | 129 (0) | 142 (13) | 129 (0) | - | - |
| s08_04 | deliver_item(item_1) | 0 to 29 | 25 (25) | 8 (8) | 25 (25) | 8 (8) | - | - |
| s08_04 | coffee_break(coffee_machine_0) | 30 to 83 | 40 (10) | 48 (18) | 40 (10) | 48 (18) | - | - |
| s08_04 | deliver_item(item_1) | 84 to 140 | 92 (8) | 91 (7) | 92 (8) | 91 (7) | - | - |
| s08_04 | deliver_item(item_2) | 141 to 203 | 154 (13) | 141 (0) | 154 (13) | 141 (0) | - | - |
| s09_01 | deliver_item(item_1) | 0 to 62 | 25 (25) | 8 (8) | 25 (25) | 8 (8) | - | - |
| s09_01 | deliver_item(item_2) | 63 to 125 | 76 (13) | 63 (0) | 76 (13) | 63 (0) | - | - |
| s09_02 | deliver_item(item_1) | 0 to 62 | 25 (25) | 8 (8) | 25 (25) | 8 (8) | - | - |
| s09_02 | coffee_break(coffee_machine_0) | 63 to 134 | 75 (12) | 93 (30) | 75 (12) | 93 (30) | - | - |
| s09_02 | deliver_item(item_2) | 135 to 202 | 140 (5) | 135 (0) | 140 (5) | 135 (0) | - | - |
| s09_03 | deliver_item(item_1) | 0 to 31 | 25 (25) | 8 (8) | 25 (25) | 8 (8) | - | - |
| s09_03 | coffee_break(coffee_machine_0) | 32 to 85 | 44 (12) | 55 (23) | 44 (12) | 55 (23) | - | - |
| s09_03 | deliver_item(item_1) | 86 to 128 | 100 (14) | 100 (14) | 100 (14) | 100 (14) | - | - |
| s09_03 | deliver_item(item_2) | 129 to 192 | 142 (13) | 129 (0) | 142 (13) | 129 (0) | - | - |
| s09_04 | deliver_item(item_1) | 0 to 29 | 25 (25) | 8 (8) | 25 (25) | 8 (8) | - | - |
| s09_04 | coffee_break(coffee_machine_0) | 30 to 83 | 40 (10) | 48 (18) | 40 (10) | 48 (18) | - | - |
| s09_04 | deliver_item(item_1) | 84 to 140 | 92 (8) | 91 (7) | 92 (8) | 91 (7) | - | - |
| s09_04 | deliver_item(item_2) | 141 to 203 | 154 (13) | 141 (0) | 154 (13) | 141 (0) | - | - |
| s09_05 | deliver_item(item_1) | 0 to 31 | 25 (25) | 8 (8) | 25 (25) | 8 (8) | - | - |
| s09_05 | deliver_item(item_1) | 80 to 129 | 87 (7) | 80 (0) | 126 (46) | 126 (46) | - | - |
| s09_05 | deliver_item(item_2) | 130 to 191 | 143 (13) | 130 (0) | 143 (13) | 130 (0) | - | - |
| s09_06 | deliver_item(item_1) | 0 to 29 | 25 (25) | 8 (8) | 25 (25) | 8 (8) | - | - |
| s09_06 | deliver_item(item_1) | 71 to 104 | 71 (0) | 71 (0) | 72 (1) | 72 (1) | - | - |
| s09_06 | deliver_item(item_2) | 105 to 167 | 118 (13) | 105 (0) | 118 (13) | 105 (0) | - | - |
| s09_07 | deliver_item(item_1) | 0 to 31 | 25 (25) | 8 (8) | 25 (25) | 8 (8) | - | - |
| s09_07 | deliver_item(item_2) | 32 to 109 | 46 (14) | 40 (8) | 46 (14) | 40 (8) | - | - |
| s09_07 | deliver_item(item_1) | 110 to 172 | 135 (25) | 110 (0) | 135 (25) | 110 (0) | - | - |
| s09_08 | deliver_item(item_1) | 0 to 76 | 25 (25) | 8 (8) | 25 (25) | 8 (8) | 66 to 74 none(leader_inadequate) (deliver_item(item_1)); 75 to 76 none(below_theta) (coffee_break(coffee_machine_0)) | 66 to 74 none(leader_inadequate) (deliver_item(item_1)); 75 to 76 none(below_theta) (deliver_item(item_1)) |
| s09_08 | deliver_item(item_2) | 77 to 132 | 96 (19) | 82 (5) | 96 (19) | 82 (5) | - | - |
| s09_09 | deliver_item(item_1) | 0 to 62 | 25 (25) | 8 (8) | 25 (25) | 8 (8) | - | - |
| s09_09 | deliver_item(item_3) | 63 to 108 | never | never | never | never | - | - |
| s09_09 | deliver_item(item_2) | 109 to 173 | 122 (13) | 109 (0) | 122 (13) | 109 (0) | - | - |
| s09_10 | deliver_item(item_1) | 0 to 62 | 27 (27) | 19 (19) | 27 (27) | 19 (19) | - | - |
| s09_10 | deliver_item(item_3) | 63 to 108 | 74 (11) | 63 (0) | 74 (11) | 63 (0) | - | - |
| s09_11 | deliver_item(item_1) | 0 to 62 | 27 (27) | 19 (19) | 27 (27) | 19 (19) | - | - |
| s09_11 | coffee_break(coffee_machine_0) | 63 to 134 | 73 (10) | 87 (24) | 73 (10) | 87 (24) | - | - |
| s09_11 | deliver_item(item_3) | 135 to 196 | 140 (5) | 135 (0) | 140 (5) | 135 (0) | - | - |
| s09_12 | deliver_item(item_2) | 0 to 62 | 15 (15) | 7 (7) | 15 (15) | 7 (7) | - | - |
| s09_12 | deliver_item(item_1) | 63 to 125 | 87 (24) | 63 (0) | 87 (24) | 63 (0) | - | - |
| s09_13 | deliver_item(item_1) | 0 to 45 | 25 (25) | 8 (8) | 25 (25) | 8 (8) | - | - |
| s09_13 | coffee_break(coffee_machine_0) | 46 to 106 | 67 (21) | 76 (30) | 74 (28) | 76 (30) | - | - |
| s09_13 | deliver_item(item_1) | 107 to 150 | 121 (14) | 120 (13) | 121 (14) | 120 (13) | - | - |
| s09_13 | deliver_item(item_2) | 151 to 213 | 164 (13) | 151 (0) | 164 (13) | 151 (0) | - | - |

#### 2. Admissions of a hypothesis that is not the true task

The gate: the run of ticks on which it clears with that hypothesis leading (its length in brackets), and how it ends. The trigger rule: the record set on the first tick of the gate's run that clears for it, the ticks it is kept (length in brackets), and the tick and reason the rule fires.

| scenario | side | hypothesis admitted | gate: ticks (n) | true task on those ticks | gate: how it ends | trigger rule: record from; wrong ticks kept (n) | trigger rule: fires |
|---|---|---|---|---|---|---|---|
| s08_01 | off | coffee_break(coffee_machine_0) | 126 to 156 (31) | unmodelled | retraction at 157 (none(leader_inadequate)) | from 126; 126 to 156 (31) | 157 inadequate |
| s08_01 | on | deliver_item(item_2) | 62 (1) | deliver_item(item_1) (complete: pinned) | the human starts it at 63: the next task admitted on the pin tick, not wrong | - | - |
| s08_01 | on | coffee_break(coffee_machine_0) | 126 to 156 (31) | unmodelled | retraction at 157 (none(leader_inadequate)) | from 126; 126 to 156 (31) | 157 inadequate |
| s08_02 | off | deliver_item(item_2) | 134 (1) | coffee_break(coffee_machine_0) (complete: pinned) | the human starts it at 135: the next task admitted on the pin tick, not wrong | - | - |
| s08_02 | off | coffee_break(coffee_machine_0) | 203 to 233 (31) | unmodelled | retraction at 234 (none(leader_inadequate)) | from 203; 203 to 233 (31) | 234 inadequate |
| s08_02 | on | deliver_item(item_2) | 62 to 83 (22) | deliver_item(item_1) (complete: pinned), coffee_break(coffee_machine_0) | retraction at 84 (none(below_theta)) | from 62; 62 to 83 (22) | 84 inadequate |
| s08_02 | on | deliver_item(item_2) | 134 (1) | coffee_break(coffee_machine_0) (complete: pinned) | the human starts it at 135: the next task admitted on the pin tick, not wrong | - | - |
| s08_02 | on | coffee_break(coffee_machine_0) | 203 to 233 (31) | unmodelled | retraction at 234 (none(leader_inadequate)) | from 203; 203 to 233 (31) | 234 inadequate |
| s08_03 | off | deliver_item(item_1) | 32 to 36 (5) | coffee_break(coffee_machine_0) | retraction at 37 (none(below_theta)) | from 25; 32 to 40 (9) | 41 leader coffee_break |
| s08_03 | off | coffee_break(coffee_machine_0) | 193 to 223 (31) | unmodelled | retraction at 224 (none(leader_inadequate)) | from 193; 193 to 223 (31) | 224 inadequate |
| s08_03 | on | deliver_item(item_1) | 32 to 42 (11) | coffee_break(coffee_machine_0) | retraction at 43 (none(leader_inadequate)) | from 8; 32 to 42 (11) | 43 inadequate |
| s08_03 | on | deliver_item(item_2) | 128 (1) | deliver_item(item_1) (complete: pinned) | the human starts it at 129: the next task admitted on the pin tick, not wrong | - | - |
| s08_03 | on | coffee_break(coffee_machine_0) | 193 to 223 (31) | unmodelled | retraction at 224 (none(leader_inadequate)) | from 193; 193 to 223 (31) | 224 inadequate |
| s08_04 | off | deliver_item(item_1) | 30 (1) | coffee_break(coffee_machine_0) | retraction at 31 (none(leader_no_observation)) | from 25; 30 to 36 (7) | 37 leader coffee_break |
| s08_04 | off | deliver_item(item_1) | 32 to 33 (2) | coffee_break(coffee_machine_0) | retraction at 34 (none(below_theta)) | from 25; 32 to 36 (5) | 37 leader coffee_break |
| s08_04 | off | coffee_break(coffee_machine_0) | 204 to 234 (31) | unmodelled | retraction at 235 (none(leader_inadequate)) | from 204; 204 to 234 (31) | 235 inadequate |
| s08_04 | on | deliver_item(item_1) | 30 (1) | coffee_break(coffee_machine_0) | retraction at 31 (none(leader_no_observation)) | from 8; 30 to 39 (10) | 40 inadequate |
| s08_04 | on | deliver_item(item_1) | 32 to 39 (8) | coffee_break(coffee_machine_0) | retraction at 40 (none(leader_inadequate)) | from 8; 32 to 39 (8) | 40 inadequate |
| s08_04 | on | deliver_item(item_2) | 140 (1) | deliver_item(item_1) (complete: pinned) | the human starts it at 141: the next task admitted on the pin tick, not wrong | - | - |
| s08_04 | on | coffee_break(coffee_machine_0) | 204 to 234 (31) | unmodelled | retraction at 235 (none(leader_inadequate)) | from 204; 204 to 234 (31) | 235 inadequate |
| s09_01 | off | coffee_break(coffee_machine_0) | 126 to 156 (31) | unmodelled | retraction at 157 (none(leader_inadequate)) | from 126; 126 to 156 (31) | 157 inadequate |
| s09_01 | on | deliver_item(item_2) | 62 (1) | deliver_item(item_1) (complete: pinned) | the human starts it at 63: the next task admitted on the pin tick, not wrong | - | - |
| s09_01 | on | coffee_break(coffee_machine_0) | 126 to 156 (31) | unmodelled | retraction at 157 (none(leader_inadequate)) | from 126; 126 to 156 (31) | 157 inadequate |
| s09_02 | off | deliver_item(item_2) | 134 (1) | coffee_break(coffee_machine_0) (complete: pinned) | the human starts it at 135: the next task admitted on the pin tick, not wrong | - | - |
| s09_02 | off | coffee_break(coffee_machine_0) | 203 to 233 (31) | unmodelled | retraction at 234 (none(leader_inadequate)) | from 203; 203 to 233 (31) | 234 inadequate |
| s09_02 | on | deliver_item(item_2) | 62 to 83 (22) | deliver_item(item_1) (complete: pinned), coffee_break(coffee_machine_0) | retraction at 84 (none(below_theta)) | from 62; 62 to 83 (22) | 84 inadequate |
| s09_02 | on | deliver_item(item_2) | 134 (1) | coffee_break(coffee_machine_0) (complete: pinned) | the human starts it at 135: the next task admitted on the pin tick, not wrong | - | - |
| s09_02 | on | coffee_break(coffee_machine_0) | 203 to 233 (31) | unmodelled | retraction at 234 (none(leader_inadequate)) | from 203; 203 to 233 (31) | 234 inadequate |
| s09_03 | off | deliver_item(item_1) | 32 to 36 (5) | coffee_break(coffee_machine_0) | retraction at 37 (none(below_theta)) | from 25; 32 to 40 (9) | 41 leader coffee_break |
| s09_03 | off | coffee_break(coffee_machine_0) | 193 to 223 (31) | unmodelled | retraction at 224 (none(leader_inadequate)) | from 193; 193 to 223 (31) | 224 inadequate |
| s09_03 | on | deliver_item(item_1) | 32 to 42 (11) | coffee_break(coffee_machine_0) | retraction at 43 (none(leader_inadequate)) | from 8; 32 to 42 (11) | 43 inadequate |
| s09_03 | on | deliver_item(item_2) | 128 (1) | deliver_item(item_1) (complete: pinned) | the human starts it at 129: the next task admitted on the pin tick, not wrong | - | - |
| s09_03 | on | coffee_break(coffee_machine_0) | 193 to 223 (31) | unmodelled | retraction at 224 (none(leader_inadequate)) | from 193; 193 to 223 (31) | 224 inadequate |
| s09_04 | off | deliver_item(item_1) | 30 (1) | coffee_break(coffee_machine_0) | retraction at 31 (none(leader_no_observation)) | from 25; 30 to 36 (7) | 37 leader coffee_break |
| s09_04 | off | deliver_item(item_1) | 32 to 33 (2) | coffee_break(coffee_machine_0) | retraction at 34 (none(below_theta)) | from 25; 32 to 36 (5) | 37 leader coffee_break |
| s09_04 | off | coffee_break(coffee_machine_0) | 204 to 234 (31) | unmodelled | retraction at 235 (none(leader_inadequate)) | from 204; 204 to 234 (31) | 235 inadequate |
| s09_04 | on | deliver_item(item_1) | 30 (1) | coffee_break(coffee_machine_0) | retraction at 31 (none(leader_no_observation)) | from 8; 30 to 39 (10) | 40 inadequate |
| s09_04 | on | deliver_item(item_1) | 32 to 39 (8) | coffee_break(coffee_machine_0) | retraction at 40 (none(leader_inadequate)) | from 8; 32 to 39 (8) | 40 inadequate |
| s09_04 | on | deliver_item(item_2) | 140 (1) | deliver_item(item_1) (complete: pinned) | the human starts it at 141: the next task admitted on the pin tick, not wrong | - | - |
| s09_04 | on | coffee_break(coffee_machine_0) | 204 to 234 (31) | unmodelled | retraction at 235 (none(leader_inadequate)) | from 204; 204 to 234 (31) | 235 inadequate |
| s09_05 | off | deliver_item(item_1) | 32 to 42 (11) | unmodelled | retraction at 43 (none(below_theta)) | from 25; 32 to 47 (16) | 48 inadequate |
| s09_05 | off | coffee_break(coffee_machine_0) | 192 to 222 (31) | unmodelled | retraction at 223 (none(leader_inadequate)) | from 192; 192 to 222 (31) | 223 inadequate |
| s09_05 | on | deliver_item(item_1) | 32 to 47 (16) | unmodelled | retraction at 48 (none(leader_inadequate)) | from 8; 32 to 47 (16) | 48 inadequate |
| s09_05 | on | deliver_item(item_2) | 129 (1) | deliver_item(item_1) (complete: pinned) | the human starts it at 130: the next task admitted on the pin tick, not wrong | - | - |
| s09_05 | on | coffee_break(coffee_machine_0) | 192 to 222 (31) | unmodelled | retraction at 223 (none(leader_inadequate)) | from 192; 192 to 222 (31) | 223 inadequate |
| s09_06 | off | deliver_item(item_1) | 30 to 46 (17) | unmodelled | retraction at 47 (none(leader_inadequate)) | from 25; 30 to 46 (17) | 47 inadequate |
| s09_06 | off | coffee_break(coffee_machine_0) | 168 to 198 (31) | unmodelled | retraction at 199 (none(leader_inadequate)) | from 168; 168 to 198 (31) | 199 inadequate |
| s09_06 | on | deliver_item(item_1) | 30 to 46 (17) | unmodelled | retraction at 47 (none(leader_inadequate)) | from 8; 30 to 46 (17) | 47 inadequate |
| s09_06 | on | deliver_item(item_2) | 104 (1) | deliver_item(item_1) (complete: pinned) | the human starts it at 105: the next task admitted on the pin tick, not wrong | - | - |
| s09_06 | on | coffee_break(coffee_machine_0) | 168 to 198 (31) | unmodelled | retraction at 199 (none(leader_inadequate)) | from 168; 168 to 198 (31) | 199 inadequate |
| s09_07 | off | deliver_item(item_1) | 32 (1) | deliver_item(item_2) | retraction at 33 (none(below_theta)) | from 25; 32 to 32 (1) | 33 leader coffee_break |
| s09_07 | off | coffee_break(coffee_machine_0) | 173 to 203 (31) | unmodelled | retraction at 204 (none(leader_inadequate)) | from 173; 173 to 203 (31) | 204 inadequate |
| s09_07 | on | deliver_item(item_1) | 32 (1) | deliver_item(item_2) | retraction at 33 (none(below_theta)) | from 8; 32 to 32 (1) | 33 boundary |
| s09_07 | on | deliver_item(item_1) | 109 (1) | deliver_item(item_2) (complete: pinned) | the human starts it at 110: the next task admitted on the pin tick, not wrong | - | - |
| s09_07 | on | coffee_break(coffee_machine_0) | 173 to 203 (31) | unmodelled | retraction at 204 (none(leader_inadequate)) | from 173; 173 to 203 (31) | 204 inadequate |
| s09_08 | off | coffee_break(coffee_machine_0) | 144 to 163 (20) | unmodelled | retraction at 164 (none(leader_inadequate)) | from 144; 144 to 163 (20) | 164 inadequate |
| s09_08 | on | deliver_item(item_1) | 132 to 148 (17) | deliver_item(item_2) (complete: pinned), unmodelled | retraction at 149 (none(leader_inadequate)) | from 132; 132 to 148 (17) | 149 inadequate |
| s09_08 | on | coffee_break(coffee_machine_0) | 163 (1) | unmodelled | retraction at 164 (none(leader_inadequate)) | from 163; 163 to 163 (1) | 164 inadequate |
| s09_09 | off | coffee_break(coffee_machine_0) | 70 to 82 (13) | deliver_item(item_3) | retraction at 83 (none(leader_inadequate)) | from 70; 70 to 82 (13) | 83 inadequate |
| s09_09 | off | coffee_break(coffee_machine_0) | 174 to 204 (31) | unmodelled | retraction at 205 (none(leader_inadequate)) | from 174; 174 to 204 (31) | 205 inadequate |
| s09_09 | on | deliver_item(item_2) | 62 to 72 (11) | deliver_item(item_1) (complete: pinned), deliver_item(item_3) | retraction at 73 (none(leader_inadequate)) | from 62; 62 to 72 (11) | 73 inadequate |
| s09_09 | on | deliver_item(item_2) | 108 (1) | deliver_item(item_3) | the human starts it at 109 | from 108; 108 to 108 (1), right from 109 | 172 leader coffee_break |
| s09_09 | on | coffee_break(coffee_machine_0) | 174 to 204 (31) | unmodelled | retraction at 205 (none(leader_inadequate)) | from 174; 174 to 204 (31) | 205 inadequate |
| s09_10 | off | coffee_break(coffee_machine_0) | 109 to 140 (32) | unmodelled | retraction at 141 (none(leader_inadequate)) | from 109; 109 to 140 (32) | 141 inadequate |
| s09_10 | on | deliver_item(item_3) | 62 (1) | deliver_item(item_1) (complete: pinned) | the human starts it at 63: the next task admitted on the pin tick, not wrong | - | - |
| s09_10 | on | coffee_break(coffee_machine_0) | 109 to 140 (32) | unmodelled | retraction at 141 (none(leader_inadequate)) | from 109; 109 to 140 (32) | 141 inadequate |
| s09_11 | off | deliver_item(item_3) | 134 (1) | coffee_break(coffee_machine_0) (complete: pinned) | the human starts it at 135: the next task admitted on the pin tick, not wrong | - | - |
| s09_11 | off | coffee_break(coffee_machine_0) | 197 to 228 (32) | unmodelled | retraction at 229 (none(leader_inadequate)) | from 197; 197 to 228 (32) | 229 inadequate |
| s09_11 | on | deliver_item(item_3) | 62 to 79 (18) | deliver_item(item_1) (complete: pinned), coffee_break(coffee_machine_0) | retraction at 80 (none(below_theta)) | from 62; 62 to 79 (18) | 80 inadequate |
| s09_11 | on | deliver_item(item_3) | 134 (1) | coffee_break(coffee_machine_0) (complete: pinned) | the human starts it at 135: the next task admitted on the pin tick, not wrong | - | - |
| s09_11 | on | coffee_break(coffee_machine_0) | 197 to 228 (32) | unmodelled | retraction at 229 (none(leader_inadequate)) | from 197; 197 to 228 (32) | 229 inadequate |
| s09_12 | off | coffee_break(coffee_machine_0) | 126 to 156 (31) | unmodelled | retraction at 157 (none(leader_inadequate)) | from 126; 126 to 156 (31) | 157 inadequate |
| s09_12 | on | deliver_item(item_1) | 62 (1) | deliver_item(item_2) (complete: pinned) | the human starts it at 63: the next task admitted on the pin tick, not wrong | - | - |
| s09_12 | on | coffee_break(coffee_machine_0) | 126 to 156 (31) | unmodelled | retraction at 157 (none(leader_inadequate)) | from 126; 126 to 156 (31) | 157 inadequate |
| s09_13 | off | deliver_item(item_1) | 46 to 54 (9) | coffee_break(coffee_machine_0) | retraction at 55 (none(leader_inadequate)) | from 25; 46 to 54 (9) | 55 inadequate |
| s09_13 | off | coffee_break(coffee_machine_0) | 214 to 244 (31) | unmodelled | retraction at 245 (none(leader_inadequate)) | from 214; 214 to 244 (31) | 245 inadequate |
| s09_13 | on | deliver_item(item_1) | 46 to 54 (9) | coffee_break(coffee_machine_0) | retraction at 55 (none(leader_inadequate)) | from 8; 46 to 54 (9) | 55 inadequate |
| s09_13 | on | deliver_item(item_2) | 150 (1) | deliver_item(item_1) (complete: pinned) | the human starts it at 151: the next task admitted on the pin tick, not wrong | - | - |
| s09_13 | on | coffee_break(coffee_machine_0) | 214 to 244 (31) | unmodelled | retraction at 245 (none(leader_inadequate)) | from 214; 214 to 244 (31) | 245 inadequate |

md5s of the expectations (`expected.csv`, `phases.json`, and the `trajectory.json` they are derived from):

    e2ec78f756ab33dc17bfe398780a59cd  scenario_s08_01/expected.csv
    99e0468b9f2d94e2b0cd5a7a334b46e2  scenario_s08_02/expected.csv
    c35ede4d32eecc644f75fe8a5e9d35ea  scenario_s08_03/expected.csv
    0d4ada7713ae687c6ef63163edf199bb  scenario_s08_04/expected.csv
    a0c9ee40926668805f624240b78b7a30  scenario_s09_01/expected.csv
    773087049e0a8eb480daab70f7aa2c4c  scenario_s09_02/expected.csv
    d084f1c3b02ef53f6231b49f1cca24a8  scenario_s09_03/expected.csv
    2b49bd95f687876f2c52f481e549b50f  scenario_s09_04/expected.csv
    73ac04a1a8f24909ab762de12c1b3436  scenario_s09_05/expected.csv
    099cfd953b3337487762bedb8f059cec  scenario_s09_06/expected.csv
    672efebc20c4397ce3511cca0f0447f2  scenario_s09_07/expected.csv
    552eac464a87cef8e3fe97402ec6c752  scenario_s09_08/expected.csv
    608845d83d6783d6bcdf62a10ba7dbda  scenario_s09_09/expected.csv
    3ac020bcfa8c48891bc3a57006a07740  scenario_s09_10/expected.csv
    d2fabd6ba4d892ad352a77499d32ceae  scenario_s09_11/expected.csv
    42b5eb75ff9baa2ffc3392ee96e633dc  scenario_s09_12/expected.csv
    3e7f026ca6e718b45342b1a740093f57  scenario_s09_13/expected.csv
    5a7ede595c5c7088cd62edf88f778b3f  scenario_s08_01/trajectory.json
    e15a3be3164b33a0acef9e5da54db2ca  scenario_s08_02/trajectory.json
    d89c88bcda3de20c8413d15fa404d289  scenario_s08_03/trajectory.json
    e0ee934065c900f4b1a4bf3a2b369212  scenario_s08_04/trajectory.json
    406517d2d5f54c406a03d9ee90cc5670  scenario_s09_01/trajectory.json
    7f2f3866c8a00c077f940a838f2080e2  scenario_s09_02/trajectory.json
    0dabb9bf35309f135cda37156e4e75a7  scenario_s09_03/trajectory.json
    f8681239f6d585d541e8260f27e226c7  scenario_s09_04/trajectory.json
    a92b9343df2dee211038097557ca3d0a  scenario_s09_05/trajectory.json
    bcec7e61acabed82a771bb80278cbdd1  scenario_s09_06/trajectory.json
    044d1764f40aa93a376a9ef1c672dde1  scenario_s09_07/trajectory.json
    7f6d3bb44e21b3266668e83653adaa4a  scenario_s09_08/trajectory.json
    fbdf6da473f20cef934f175f3eec9a79  scenario_s09_09/trajectory.json
    852654dad02d7703f5ad0b3efb90931f  scenario_s09_10/trajectory.json
    602c3671a5988375f0bfa099aaf35c59  scenario_s09_11/trajectory.json
    bf265e0359e5b350eb96724ea92f0c2d  scenario_s09_12/trajectory.json
    88ec0d09f1eae5b6411b56c1619222cc  scenario_s09_13/trajectory.json
    919e26bab122ee95c762036eb2a9f632  scenario_s08_01/phases.json
    ae6ca527cf39fe872769a5201769a83a  scenario_s08_02/phases.json
    4e103298ec3d2caf28b8d50efcef024c  scenario_s08_03/phases.json
    651e72ee2e47a6708cb7f70671a2537e  scenario_s08_04/phases.json
    0c8bc6a4ec601498280dfe7f8f7c0cc0  scenario_s09_01/phases.json
    08dc5d462cf9e37413a5a78e068df053  scenario_s09_02/phases.json
    f2207143f5339956d005a59a687e44c3  scenario_s09_03/phases.json
    25a30e772f9c829c03ac0a7845701293  scenario_s09_04/phases.json
    67517c7e0c7f5f67a101184792bfcbcf  scenario_s09_05/phases.json
    4ae0f44e9f7ead78cbf7d9cd0bf65a34  scenario_s09_06/phases.json
    5dcc6af441bd8aaa3798a0f662f98b40  scenario_s09_07/phases.json
    6b67edab29b18c1b289f7f863e561039  scenario_s09_08/phases.json
    e3df59d6517d5943c263781d4680ad38  scenario_s09_09/phases.json
    195a0abd408edaeb784b2b3ef6d2cf7d  scenario_s09_10/phases.json
    1e4bd993764ff9ef2d5b54d9047d1ecc  scenario_s09_11/phases.json
    db58521960ef067271c2c1cd8b9ce0a4  scenario_s09_12/phases.json
    e25796c49eaf761a868bcda094320767  scenario_s09_13/phases.json

## Runs (stage 2; git-ignored; md5s)

17 runs, context knowledge on; every run agrees with its expectations (0 disagreements against actual.csv and actual_log.csv at 1e-9, 0 unmatched rows); the trajectory equals the run's human lines on every tick; the expectations' md5s unchanged by the runs. Results: `analysis/kitting/mpb/tk5b/REPORT.md`.

    a95cc2eae7b0fcf51bcfc7d813e6ed71  runs/env_layout_10_scenario_s08_01_on.log
    1aeededb6b19047ac26259e86b711a39  runs/env_layout_10_scenario_s08_02_on.log
    c59fecb8d6573defe8c4e2f8b1524114  runs/env_layout_10_scenario_s08_03_on.log
    37aac8c5340ec2328876f8bd644b8b93  runs/env_layout_10_scenario_s08_04_on.log
    cbd9923b09e994b06cf9cefd9e66764e  runs/env_layout_11_scenario_s09_01_on.log
    7c17e389ae0f0b5771cd23b93b2d8623  runs/env_layout_11_scenario_s09_02_on.log
    56099d01ad4ca56a574a5fed7f93f02f  runs/env_layout_11_scenario_s09_03_on.log
    6c1643446f96ce1e75faa52a0565cd09  runs/env_layout_11_scenario_s09_04_on.log
    6a3fa3747facfec19c99e3a56c4b7206  runs/env_layout_11_scenario_s09_05_on.log
    9e2645205162c7383f1a1ecc24f56db2  runs/env_layout_11_scenario_s09_06_on.log
    29e68dfde182ffe644c5d61f787fe923  runs/env_layout_11_scenario_s09_07_on.log
    bb17462229c5e24106c5ee2aa89accfd  runs/env_layout_11_scenario_s09_08_on.log
    5874fb334e9bf715fd71321bfb229deb  runs/env_layout_11_scenario_s09_09_on.log
    01d6b035490d749619c3b7734f90cf44  runs/env_layout_11_scenario_s09_10_on.log
    fe926c06ac704f483eaffb5dd3df734a  runs/env_layout_11_scenario_s09_11_on.log
    0ba34f139de36af3510f8a2c8390236f  runs/env_layout_11_scenario_s09_12_on.log
    3677ff255e79a558c60cd0678bfeb70b  runs/env_layout_11_scenario_s09_13_on.log
    2b6dafd84a0086185ec971c2bde68d75  runs/env_layout_10_scenario_s08_01_on.rec
    a9c382958a10484ae1bc2df54e4d3a1c  runs/env_layout_10_scenario_s08_02_on.rec
    93551c8fa122df7c3ad6a028f9717845  runs/env_layout_10_scenario_s08_03_on.rec
    b2d33459410319657e1f47791c1e180e  runs/env_layout_10_scenario_s08_04_on.rec
    2b6dafd84a0086185ec971c2bde68d75  runs/env_layout_11_scenario_s09_01_on.rec
    a9c382958a10484ae1bc2df54e4d3a1c  runs/env_layout_11_scenario_s09_02_on.rec
    93551c8fa122df7c3ad6a028f9717845  runs/env_layout_11_scenario_s09_03_on.rec
    b2d33459410319657e1f47791c1e180e  runs/env_layout_11_scenario_s09_04_on.rec
    c715db44f68926f3bb6b8fa387525f1a  runs/env_layout_11_scenario_s09_05_on.rec
    703b2c62e484b7db940f36166548a88c  runs/env_layout_11_scenario_s09_06_on.rec
    a2ece1d231a6c071c20efdea470c4c9f  runs/env_layout_11_scenario_s09_07_on.rec
    529f6f2019682be19b77f4e1152b1ea5  runs/env_layout_11_scenario_s09_08_on.rec
    e252b7b8e703da1492b52df3ae4df3dc  runs/env_layout_11_scenario_s09_09_on.rec
    c3515ed75407562597852c6bf654c806  runs/env_layout_11_scenario_s09_10_on.rec
    9a4309d36ae6a47d9f1e36f512b711b2  runs/env_layout_11_scenario_s09_11_on.rec
    606beeb608930d07b519195f915aae90  runs/env_layout_11_scenario_s09_12_on.rec
    739ce3199f341516687bfc7701b29143  runs/env_layout_11_scenario_s09_13_on.rec

## Step 5d: the expectations after the gate change (5 October 2026, committed before the runs)

The oracle after the gate's build (8357b74: the rank column, D3; observation warrant at admission, AM67;
none(leader_outranked) last, AM68 and D1) recomputes every table; the trajectories are byte-identical to stage 1's
(the human's script is open-loop). Commands as above, with --expect. The runs follow in the next commit; the reading:
analysis/kitting/mpb/tk5b/COMPARISON_5d.md.

    c19d18dcfeb119c25b2db3a72177ab0f  scenario_s08_01/expected.csv
    bbc049cef29d1c93f2682b13a581ff59  scenario_s08_02/expected.csv
    f5c1234c7998443a2c65dc784f7b0492  scenario_s08_03/expected.csv
    1a0ca018c7af0d6af58d02ed6ee4e24f  scenario_s08_04/expected.csv
    a0bc3a74418b17970021d4d441422562  scenario_s09_01/expected.csv
    3dda9eb771790659415ffd583093947c  scenario_s09_02/expected.csv
    82cf1d81bca7f162c86fbde192263a73  scenario_s09_03/expected.csv
    f5a742798bb4fe7e87be1188c098d1e7  scenario_s09_04/expected.csv
    7607c3d14deeebd26a0e51ab3a1e433f  scenario_s09_05/expected.csv
    da4d2972b2aff94a15af8ba0a1c379fd  scenario_s09_06/expected.csv
    56fb4eb7368da1376739cf5b38f97510  scenario_s09_07/expected.csv
    059c5bdb5be616296d76d5c53545c37d  scenario_s09_08/expected.csv
    d0f8a83ff0cf070089ac5cdd1937bf7d  scenario_s09_09/expected.csv
    73f6d129e4bbe3ed9873e9d10573e5d0  scenario_s09_10/expected.csv
    54e1d35c579952bb4e9a44dec00a3ac6  scenario_s09_11/expected.csv
    faecab1a642a1393bb086fbada495709  scenario_s09_12/expected.csv
    09e69dd416f8003fb13ff914e8ec40e6  scenario_s09_13/expected.csv
