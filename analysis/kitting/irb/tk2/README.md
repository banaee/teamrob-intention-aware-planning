# T-K part 1, step 4: the runs with context knowledge on (the IRB on env_layout_15, _16, _17, robot idle)

The data and figures of this set (.json, .csv, .png) are not in git (Hadi, 2 October 2026). The instrument is the shared
IRB (`analysis/instruments/irb/`; rules 1 to 33 in `analysis/kitting/irb/README.md`). The off side of every case is
round 1's run of the same script (`analysis/kitting/irb/tk1/`); a new script has its own off run.

What the step is (Hadi, 4 October 2026; `docs/handoffs/T-G_forward_inputs.md`, 5.4 and 5.7 step 4): context knowledge
off against on, each case labelled by the state the script meets (KT14). Three stages, a pause after each: 1 check and
propose (no runs), 2 author (timelines, scenarios, run files, expectations committed before any run with context
knowledge on; the regression audit), 3 run, compare with the oracle, report.

## Stage 1: the state each script meets (no runs)

Derived from round 1's trajectories (the human's ticks do not depend on the recognizer or on context knowledge; R1) and
the method document, sections 3 and 4: windows half-open in ticks (AM46); the coffee break's recency fact holds for 90
ticks from its completion, the completion tick included (AM47); ac_on holds from the A/C activation's completion. A
level is the foreseeable task's strength level: ord (ordinary, 0.02), raised (coffee break 2, A/C activation 0.5),
supp (suppressed, 0.005). "Arrival": the tick before the wait's first tick, the move's last tick (Hadi's completion
minus the wait); for the A/C activation (a wait of one tick) it is the tick before its completion, on which tick the
hypothesis is retired by its pin. "Live": the deliveries whose terminal fact does not yet hold. Ticks are the IRB's
(the trajectory's), the same ticks the timeline is written in. The cases: "default" the setups' timeline, break_time
178 to 300; 3A to 3F Hadi's point 3; P1 to P6 ccode's proposals on existing scripts (below).

| case | script | timeline | foreseeable task: ticks [levels at that tick]; a level changing during it | deliveries live at its start | a level changing inside a delivery stretch |
|---|---|---|---|---|---|
| default | s13_01 | break_time 178 to 300 | none (control) | - | item_1 (124 to 216) at 178: coffee:raised; item_4 (217 to 308) at 300: coffee:ord |
| default | s13_02 | break_time 178 to 300 | coffee_break: start 67 [coffee:ord]; arrival 109 [coffee:ord]; completion 139 | 3 | item_1 (193 to 285) at 229: coffee:raised; item_4 (286 to 377) at 300: coffee:ord |
| default | s13_03 | break_time 178 to 300 | coffee_break: start 124 [coffee:ord]; arrival 166 [coffee:ord]; completion 196; at 178: coffee:raised | 2 | item_4 (280 to 371) at 286: coffee:raised; item_4 (280 to 371) at 300: coffee:ord |
| default | s13_04 | break_time 178 to 300 | coffee_break: start 217 [coffee:raised]; arrival 258 [coffee:raised]; completion 288 | 1 | item_1 (124 to 216) at 178: coffee:raised |
| default | s13_05 | break_time 178 to 300 | coffee_break (inside a delivery): start 94 [coffee:ord]; arrival 115 [coffee:ord]; completion 145 | 3 | item_1 (199 to 291) at 235: coffee:raised; item_4 (292 to 383) at 300: coffee:ord |
| default | s13_06 | break_time 178 to 300 | coffee_break (inside a delivery): start 96 [coffee:ord]; arrival 117 [coffee:ord]; completion 147 | 3 | item_1 (194 to 286) at 237: coffee:raised; item_4 (287 to 378) at 300: coffee:ord |
| default | s13_07 | break_time 178 to 300 | coffee_break (inside a delivery): start 122 [coffee:ord]; arrival 164 [coffee:ord]; completion 194; at 178: coffee:raised | 3 | item_1 (241 to 334) at 284: coffee:raised; item_1 (241 to 334) at 300: coffee:ord |
| default | s14_01 | break_time 178 to 300 | none (control) | - | item_2 (89 to 180) at 178: coffee:raised A/C:ord |
| default | s14_02 | break_time 178 to 300 | coffee_break: start 89 [coffee:ord A/C:ord]; arrival 135 [coffee:ord A/C:ord]; completion 165 | 2 | item_1 (226 to 325) at 255: coffee:raised A/C:ord; item_1 (226 to 325) at 300: coffee:ord A/C:ord |
| default | s14_03 | break_time 178 to 300 | coffee_break: start 181 [coffee:raised A/C:ord]; arrival 228 [coffee:raised A/C:ord]; completion 258 | 1 | item_2 (89 to 180) at 178: coffee:raised A/C:ord |
| default | s14_04 | break_time 178 to 300 | coffee_break (inside a delivery): start 133 [coffee:ord A/C:ord]; arrival 143 [coffee:ord A/C:ord]; completion 173 | 2 | item_1 (234 to 333) at 263: coffee:raised A/C:ord; item_1 (234 to 333) at 300: coffee:ord A/C:ord |
| default | s14_05 | break_time 178 to 300 | coffee_break (inside a delivery): start 135 [coffee:ord A/C:ord]; arrival 145 [coffee:ord A/C:ord]; completion 175 | 2 | item_1 (227 to 328) at 265: coffee:raised A/C:ord; item_1 (227 to 328) at 300: coffee:ord A/C:ord |
| default | s14_06 | break_time 178 to 300 | coffee_break (inside a delivery): start 179 [coffee:raised A/C:ord]; arrival 226 [coffee:raised A/C:ord]; completion 256 | 2 | item_2 (89 to 178) at 178: coffee:raised A/C:ord; item_1 (308 to 409) at 346: coffee:ord A/C:ord |
| default | s15_01 | break_time 178 to 300 | none (control) | - | item_1 (124 to 216) at 178: coffee:raised A/C:ord; item_4 (217 to 308) at 300: coffee:ord A/C:ord |
| default | s15_02 | break_time 178 to 300 | coffee_break: start 67 [coffee:ord A/C:ord]; arrival 109 [coffee:ord A/C:ord]; completion 139 | 3 | item_1 (193 to 285) at 229: coffee:raised A/C:ord; item_4 (286 to 377) at 300: coffee:ord A/C:ord |
| default | s15_03 | break_time 178 to 300 | coffee_break: start 124 [coffee:ord A/C:ord]; arrival 166 [coffee:ord A/C:ord]; completion 196; at 178: coffee:raised A/C:ord | 2 | item_4 (280 to 371) at 286: coffee:raised A/C:ord; item_4 (280 to 371) at 300: coffee:ord A/C:ord |
| default | s15_04 | break_time 178 to 300 | coffee_break: start 217 [coffee:raised A/C:ord]; arrival 258 [coffee:raised A/C:ord]; completion 288 | 1 | item_1 (124 to 216) at 178: coffee:raised A/C:ord |
| default | s15_05 | break_time 178 to 300 | coffee_break (inside a delivery): start 94 [coffee:ord A/C:ord]; arrival 115 [coffee:ord A/C:ord]; completion 145 | 3 | item_1 (199 to 291) at 235: coffee:raised A/C:ord; item_4 (292 to 383) at 300: coffee:ord A/C:ord |
| default | s15_06 | break_time 178 to 300 | coffee_break (inside a delivery): start 96 [coffee:ord A/C:ord]; arrival 117 [coffee:ord A/C:ord]; completion 147 | 3 | item_1 (194 to 286) at 237: coffee:raised A/C:ord; item_4 (287 to 378) at 300: coffee:ord A/C:ord |
| default | s15_07 | break_time 178 to 300 | coffee_break (inside a delivery): start 122 [coffee:ord A/C:ord]; arrival 164 [coffee:ord A/C:ord]; completion 194; at 178: coffee:raised A/C:ord | 3 | item_1 (241 to 334) at 284: coffee:raised A/C:ord; item_1 (241 to 334) at 300: coffee:ord A/C:ord |
| 3A | s14_07 | room_warm 150 to end | ac_activation: start 89 [coffee:ord A/C:ord]; arrival 135 [coffee:ord A/C:ord]; completion 136 | 2 | - |
| 3A | s14_08 | room_warm 150 to end | ac_activation: start 181 [coffee:ord A/C:raised]; arrival 227 [coffee:ord A/C:raised]; completion 228 | 1 | item_2 (89 to 180) at 150: coffee:ord A/C:raised |
| 3A | s14_09 | room_warm 150 to end | ac_activation (inside a delivery): start 133 [coffee:ord A/C:ord]; arrival 138 [coffee:ord A/C:ord]; completion 139 | 2 | - |
| 3A | s14_10 | room_warm 150 to end | ac_activation (inside a delivery): start 135 [coffee:ord A/C:ord]; arrival 140 [coffee:ord A/C:ord]; completion 141 | 2 | - |
| 3A | s14_11 | room_warm 150 to end | ac_activation (inside a delivery): start 179 [coffee:ord A/C:raised]; arrival 225 [coffee:ord A/C:raised]; completion 226 | 2 | item_2 (89 to 178) at 150: coffee:ord A/C:raised |
| 3A | s15_08 | room_warm 150 to end | ac_activation: start 67 [coffee:ord A/C:ord]; arrival 112 [coffee:ord A/C:ord]; completion 113 | 3 | - |
| 3A | s15_09 | room_warm 150 to end | ac_activation: start 124 [coffee:ord A/C:ord]; arrival 169 [coffee:ord A/C:raised]; completion 170; at 150: coffee:ord A/C:raised | 2 | - |
| 3A | s15_10 | room_warm 150 to end | ac_activation: start 217 [coffee:ord A/C:raised]; arrival 261 [coffee:ord A/C:raised]; completion 262 | 1 | item_1 (124 to 216) at 150: coffee:ord A/C:raised |
| 3A | s15_11 | room_warm 150 to end | ac_activation (inside a delivery): start 94 [coffee:ord A/C:ord]; arrival 132 [coffee:ord A/C:ord]; completion 133 | 3 | - |
| 3A | s15_12 | room_warm 150 to end | ac_activation (inside a delivery): start 96 [coffee:ord A/C:ord]; arrival 134 [coffee:ord A/C:ord]; completion 135 | 3 | - |
| 3A | s15_13 | room_warm 150 to end | ac_activation (inside a delivery): start 122 [coffee:ord A/C:ord]; arrival 167 [coffee:ord A/C:raised]; completion 168; at 150: coffee:ord A/C:raised | 3 | - |
| 3B | s13_02 | break_time 50 to 200 | coffee_break: start 67 [coffee:raised]; arrival 109 [coffee:raised]; completion 139 | 3 | item_3 (0 to 66) at 50: coffee:raised; item_1 (193 to 285) at 229: coffee:ord |
| 3B | s13_02 | break_time 90 to 200 | coffee_break: start 67 [coffee:ord]; arrival 109 [coffee:raised]; completion 139; at 90: coffee:raised | 3 | item_1 (193 to 285) at 229: coffee:ord |
| 3B | s13_02 | break_time 120 to 200 | coffee_break: start 67 [coffee:ord]; arrival 109 [coffee:ord]; completion 139; at 120: coffee:raised | 3 | item_1 (193 to 285) at 229: coffee:ord |
| 3B | s14_02 | break_time 70 to 250 | coffee_break: start 89 [coffee:raised A/C:ord]; arrival 135 [coffee:raised A/C:ord]; completion 165 | 2 | item_0 (0 to 88) at 70: coffee:raised A/C:ord; item_1 (226 to 325) at 255: coffee:ord A/C:ord |
| 3B | s14_02 | break_time 110 to 250 | coffee_break: start 89 [coffee:ord A/C:ord]; arrival 135 [coffee:raised A/C:ord]; completion 165; at 110: coffee:raised A/C:ord | 2 | item_1 (226 to 325) at 255: coffee:ord A/C:ord |
| 3B | s14_02 | break_time 150 to 250 | coffee_break: start 89 [coffee:ord A/C:ord]; arrival 135 [coffee:ord A/C:ord]; completion 165; at 150: coffee:raised A/C:ord | 2 | item_1 (226 to 325) at 255: coffee:ord A/C:ord |
| 3C | s15_08 | room_warm 50 to end | ac_activation: start 67 [coffee:ord A/C:raised]; arrival 112 [coffee:ord A/C:raised]; completion 113 | 3 | item_3 (0 to 66) at 50: coffee:ord A/C:raised |
| 3C | s15_08 | room_warm 90 to end | ac_activation: start 67 [coffee:ord A/C:ord]; arrival 112 [coffee:ord A/C:raised]; completion 113; at 90: coffee:ord A/C:raised | 3 | - |
| 3C | s15_08 | room_warm 0 to 90 | ac_activation: start 67 [coffee:ord A/C:raised]; arrival 112 [coffee:ord A/C:ord]; completion 113; at 90: coffee:ord A/C:ord | 3 | - |
| 3C | s14_07 | room_warm 70 to end | ac_activation: start 89 [coffee:ord A/C:raised]; arrival 135 [coffee:ord A/C:raised]; completion 136 | 2 | item_0 (0 to 88) at 70: coffee:ord A/C:raised |
| 3C | s14_07 | room_warm 110 to end | ac_activation: start 89 [coffee:ord A/C:ord]; arrival 135 [coffee:ord A/C:raised]; completion 136; at 110: coffee:ord A/C:raised | 2 | - |
| 3C | s14_07 | room_warm 0 to 110 | ac_activation: start 89 [coffee:ord A/C:raised]; arrival 135 [coffee:ord A/C:ord]; completion 136; at 110: coffee:ord A/C:ord | 2 | - |
| 3D | s13_03 | break_time 40 to 190 | coffee_break: start 124 [coffee:raised]; arrival 166 [coffee:raised]; completion 196; at 190: coffee:ord | 2 | item_3 (0 to 66) at 40: coffee:raised; item_4 (280 to 371) at 286: coffee:ord |
| 3D | s13_03 | break_time 40 to 150 | coffee_break: start 124 [coffee:raised]; arrival 166 [coffee:ord]; completion 196; at 150: coffee:ord | 2 | item_3 (0 to 66) at 40: coffee:raised; item_4 (280 to 371) at 286: coffee:ord |
| 3D | s14_03 | break_time 60 to 250 | coffee_break: start 181 [coffee:raised A/C:ord]; arrival 228 [coffee:raised A/C:ord]; completion 258; at 250: coffee:ord A/C:ord | 1 | item_0 (0 to 88) at 60: coffee:raised A/C:ord |
| 3E | s13_04 | stated empty | coffee_break: start 217 [coffee:ord]; arrival 258 [coffee:ord]; completion 288 | 1 | - |
| 3E | s14_03 | stated empty | coffee_break: start 181 [coffee:ord A/C:ord]; arrival 228 [coffee:ord A/C:ord]; completion 258 | 1 | - |
| 3F | s15_04 | break_time 178 to 300, room_warm 150 to end | coffee_break: start 217 [coffee:raised A/C:raised]; arrival 258 [coffee:raised A/C:raised]; completion 288 | 1 | item_1 (124 to 216) at 150: coffee:ord A/C:raised; item_1 (124 to 216) at 178: coffee:raised A/C:raised |
| P1 | s13_01 | break_time 0 to end | none (control) | - | - |
| P2 | s15_01 | room_warm 0 to end | none (control) | - | - |
| P3 | s14_01 | break_time 0 to end | none (control) | - | - |
| P4 | s15_10 | stated empty | ac_activation: start 217 [coffee:ord A/C:ord]; arrival 261 [coffee:ord A/C:ord]; completion 262 | 1 | - |
| P5 | s14_08 | break_time 178 to 300 | ac_activation: start 181 [coffee:raised A/C:ord]; arrival 227 [coffee:raised A/C:ord]; completion 228 | 1 | item_2 (89 to 180) at 178: coffee:raised A/C:ord |
| P6 | s15_10 | break_time 178 to 300, room_warm 150 to end | ac_activation: start 217 [coffee:raised A/C:raised]; arrival 261 [coffee:raised A/C:raised]; completion 262 | 1 | item_1 (124 to 216) at 150: coffee:ord A/C:raised; item_1 (124 to 216) at 178: coffee:raised A/C:raised; item_4 (264 to 321) at 300: coffee:ord A/C:supp |

Not in the table (new scripts, ticks approximate until the trajectory is derived in stage 2): P7 (coffee break inside
the last delivery of env_setup_13's script, after the walk to shelf_4, timeline stated empty: start about 261, one
delivery live) and P9 (coffee break after the fourth delivery of env_setup_15's script, break_time 307 to end: start
309, no delivery live).

### Where the states differ from Hadi's points 3 and 4

1. Point 4 holds for every script it names: the break before the window in s13 and s15 _02, _05, _06 and s14 _02, _04,
   _05 (each completes by 175); the break starting inside it in s13 and s15 _04 (217) and s14 _03 (181), _06 (179); the
   window opening during the wait in s13 and s15 _03 (wait 167 to 195) and _07 (wait 165 to 193); deliveries through
   the window in the controls.
2. Under the default, the recency fact of the observed break covers the start of the window in every "before" script:
   the coffee break is suppressed from its completion for 90 ticks and is raised only from 229 (s13, s15 _02), 235
   (_05), 237 (_06), 255 (s14_02), 263 (s14_04), 265 (s14_05), each inside a delivery stretch. In the "wait" scripts
   the recency runs to 285 (_03) and 283 (_07): raised only on 286 to 299 and 284 to 299. So these scripts exercise the
   end of a recency fact inside a delivery more than the window's own edges; the window's own edges inside a delivery
   fall in the controls (178, 300), s13 and s15 _04 (178, inside item_1), s14_03 (178, inside item_2, two ticks before
   its end) and s14_06 (178, the last tick of item_2's stretch).
3. "Starting inside the window" holds by one tick in s14_06 (start 179) and by three in s14_03 (181).
4. 3A (room_warm from 150 to end) reaches the A/C activation in 5 of the 11 scripts: raised from its start in s14_08,
   s14_11, s15_10; the edge during the walk in s15_09 (150, arrival 169) and s15_13 (150, arrival 167). In the other six
   (s14_07, s14_09, s14_10, s15_08, s15_11, s15_12) the A/C is on before 150, so room_warm acts on no level (the A/C
   ordinary while pending, suppressed by ac_on after): these six are the A/C's cases with no raising fact. Stated as a
   fact, not an objection; the windows are Hadi's.
5. 3B: the windows' ends (200, 250) fall inside the recency of the break (139 to 228; 165 to 254) and change no level.
   "From 50" and "from 70" open inside the first delivery after round 1 admitted it (26, 50); the same holds for 3C "from
   50", "from 70" and 3D "40", "60". These cases also test an edge inside an admitted delivery.
6. 3C "0 to 90" and "0 to 110" raise the A/C from tick 0, through the whole first delivery (4 and 3 live).
7. 3D: "40 to 150" closes during the walk to the machine (124 to 165); "40 to 190" and s14_03's "60 to 250" during the
   wait. D therefore also covers the window closing at those two positions.
8. Direction 5, "never on the prior alone": with a delivery live the raised coffee break's prior is 2/3 (2/3.02 with
   the A/C live), below θ. With no delivery live it is 1 (env_layout_15) or 2/2.02 (env_layout_16, _17), above θ on the
   prior alone, and only the warrant (a step toward the machine) delays the admission. No script of points 3 and 4
   takes a coffee break with no delivery live; the exit walk does meet that state (P8), and P9 adds a true break in it.

## Proposals (ccode, stage 1; Hadi may strike any)

Each names the case it adds. The off side of P1 to P6 is round 1's run of the same script; P7 and P9 are new scripts
and need their own off run.

- P1. s13_01's script (control, env_layout_15), break_time 0 to end. Every delivery against the raised coffee break, at
  4, 3, 2 and 1 live, item_2 included, whose shelf lies on the coffee machine's side (both east of the table). The
  recognition side of KT3's second planning case (deliveries through the whole break time); under the default only
  item_1 and item_4 meet the window.
- P2. s15_01's script (control, env_layout_17), room_warm 0 to end. A warm room in which the human never switches the
  A/C on: the deliveries beside the switch (item_1 on shelf_1, item_4 on shelf_4) against the raised A/C activation.
  No ruled script has room_warm through deliveries with the A/C pending at 4 or 3 live.
- P3. s14_01's script (control, env_layout_16), break_time 0 to end. P1 in the dense room, where the movement
  separates nothing before the arrival (round 1), so the prior weighs most.
- P4. s15_10's script (env_layout_17, the A/C after the third delivery, one delivery live), timeline stated empty.
  Hadi's case E with the A/C as the foreseeable task: its switch stands beside the lone delivery's shelf (ac_switch_0
  at (0, -480), shelf_4 at (150, -450)), so the delivery admitted early may stay adequate on most of the walk; when the
  retraction comes. Pairs with s15_10 under 3A, where room_warm (A/C raised, the delivery's prior 1/1.52) prevents the
  early admission.
- P5. s14_08's script (env_layout_16, the A/C after the second delivery), the setup's default (break_time 178 to 300),
  no own timeline. The A/C activation while its cluster neighbour, the coffee break, is raised and the A/C is ordinary:
  the A/C's belief at its arrival under a raised rival.
- P6. s15_10's script, break_time 178 to 300 and room_warm 150 to end. Case F's mirror: the A/C activation the true
  task with both raised (0.5 against 2).
- P7. A new script on env_setup_13: the coffee break inside the last delivery (item_4), after the walk to the shelf;
  timeline stated empty. A lone delivery admitted early and rightly, then cut by the break: the retraction of a right
  admission, and the delivery's admission again when the human resumes it (round 1 places breaks inside the second
  delivery only, with three live).
- P8. No new run: a reading of the exit walk (unmodelled, no delivery live) in every run, off against on (method
  document, section 12, case 3). Round 1 already shows the gate clearing the coffee break during the exit walk where
  the walk shortens the path to the machine (env_layout_15 and _17, for example s13_01 on 309 to 330 and s15_01 on 319
  to 330, then inadequate); the measure lists true stretches only, so these admissions are in no table. With context
  knowledge on, the shares there change (env_layout_17: the coffee break 0.8 when the A/C is on, 0.2 when the break is
  recent). The reading adds one row per run: the ticks on which the gate clears during the exit walk, and for what.
- P9. A new script on env_setup_15: the coffee break after the fourth delivery (no delivery live), then the exit walk;
  break_time from 307 (the tick the last delivery's terminal fact first holds) to end. The true foreseeable task in the
  state with no assigned task live: its belief over θ on the prior alone (2/2.02 against 0.5 off), its admission at its
  first warranted step.

Not proposed: a second coffee break (it waits for Hadi's further layout, 5.8); a second A/C activation (the same kind
of case, and switching on a switch that is on is not a task of the shift).

## Readings to repair before stage 3 (small, ccode's)

- `admission.py` reads the A/C's belief at its arrival on the first tick of its switch_on, where the hypothesis is
  already retired by its pin and has no belief (it would print nan). It reads the tick before (the arrival above).
- `admission.py` prints the A/C's belief at arrival only with context knowledge on; the off side (round 1's
  expected.csv) needs it too.

## Stage 2: the set as authored (Hadi, 4 October 2026: P1 to P9 all in; P8 part of the measure)

- **The default timeline.** env_setup_13, _14, _15 state `"timeline": [{"fact": "break_time", "from": 178, "until":
  300}]`. Every scenario of round 1 without an A/C activation meets it.
- **3A in place.** The 11 scripts with an A/C activation (scenario_s14_07 to _11, s15_08 to _13) state their own
  timeline, room_warm from 150 to the run's end. So round 1's scenarios are the on side's scenarios too; their off side
  is round 1's run.
- **New scenarios** (same module per setup, after round 1's; the description names the script and the case):

  | scenario | case | script | timeline in force |
  |---|---|---|---|
  | s13_08, _09, _10 | 3B | s13_02 | break_time 50, 90, 120 to 200 |
  | s13_11, _12 | 3D | s13_03 | break_time 40 to 190; 40 to 150 |
  | s13_13 | 3E | s13_04 | stated empty |
  | s13_14 | P1 | s13_01 | break_time 0 to end |
  | s13_15 | P7 | new: s13_01's with the coffee break inside item_4's delivery, after the walk to the shelf | stated empty |
  | s14_12, _13, _14 | 3B | s14_02 | break_time 70, 110, 150 to 250 |
  | s14_15, _16, _17 | 3C | s14_07 | room_warm 70 to end; 110 to end; 0 to 110 |
  | s14_18 | 3D | s14_03 | break_time 60 to 250 |
  | s14_19 | 3E | s14_03 | stated empty |
  | s14_20 | P3 | s14_01 | break_time 0 to end |
  | s14_21 | P5 | s14_08 | the setup's (break_time 178 to 300) |
  | s15_14, _15, _16 | 3C | s15_08 | room_warm 50 to end; 90 to end; 0 to 90 |
  | s15_17 | 3F | s15_04 | break_time 178 to 300, room_warm 150 to end |
  | s15_18 | P2 | s15_01 | room_warm 0 to end |
  | s15_19 | P4 | s15_10 | stated empty |
  | s15_20 | P6 | s15_10 | break_time 178 to 300, room_warm 150 to end |
  | s15_21 | P9 | new: s15_01's four deliveries, then the coffee break, then the exit walk | break_time 307 to end |

  The new scripts' ticks (from their trajectories): s13_15, item_4's walk 217 to 260, the coffee break 261 to 309
  (wait from 279, complete 308), item_4 resumed from 310; s15_21, item_4 delivered at 307 (its terminal fact), the
  coffee break 309 to 381 (wait from 351, complete 380).
- **Run files**: `configs/kitting/irb/tk2/scenario_sNN_MM.yaml`, the 57 scenarios with context knowledge on (round 1's
  run files stay off). The off runs of the two new scripts use the same files with `run.sh --context off`, into
  `off/`.
- **The instrument** (small, ccode's):
  - `trajectory.py` rebuilt the scenario without its own timeline, so the setup's always applied in the trajectory
    (the run itself resolves it right). Found by the first expectations (s13_13 showed break_time, s15_09 no room_warm
    at 150); fixed (`timeline=base.timeline`), every expectation recomputed. The MPB's `reference.py` has the same
    omission (flag only: no MPB scenario states a timeline, and its reference run has no human).
  - `admission.py`: the A/C's arrival read on the tick before its switch_on (stage 1's reading), with context
    knowledge off too; a second table, every admission of a hypothesis that is not the true task (P8).
  - `offon.py` (new): off against on per case; the off side found by the same human actions on the same layout, in
    `off/` first, then round 1.
- **Test**: `tests/test_tk_prior.py`'s recency test on scenario_s15_02 states its timeline empty (it reads the level
  after the recency, which the new default break_time raises).

### The regression audit (stage 2)

What the new default and 3A change in existing outputs:
- Round 1 (context knowledge off), rerun under the new artefacts: every log equal except its `[run_mesa] timeline`
  line; every `.rec`, instrument output and figure byte-identical except the trajectories' timeline facts; 0
  disagreements in all 31. Its outputs replaced; md5s in `analysis/kitting/irb/tk1/README.md`, its last section.
- The four maintained sets (tb1a, tb1b, tb1c, tb3: 48 logs and their `.rec`): byte-identical to their baselines.
- Tests: 352 pass. Three tests were updated, none for a change of behaviour: `test_tk_prior.py` (above);
  `test_tl2_discovery.py` counts 128 registered scenarios (102 before); `test_th3_scenarios.py` gives `SimModel` the
  domain's timeline facts, which a setup's timeline needs.

### The expected directions (Hadi's point 5, restated before the runs, with the correction ruled on 4 October 2026)

1. With no raising fact holding: one live delivery is admitted at its first observation, and a retraction follows if
   the human then takes the break; with several live, the deliveries come no later, the break later, the A/C's belief
   at its arrival lower.
2. With break_time: the coffee break reaches the threshold earlier. While a delivery is live it does not reach the
   threshold on the prior alone (its prior is 2/3, or 2/3.02 with the A/C live). With none live it does (2/2.02 or 1),
   and only the observation rule (warrant) delays its admission. A delivery inside the window is admitted later.
3. With room_warm and the A/C off: the A/C's belief at its arrival higher.
4. After an observed break: suppressed for 90 ticks, inside break_time too.
5. At a window's edge inside an episode: the belief changes at that tick, and an admitted delivery can lose the
   threshold there.

The oracle's expectations below are not read against these directions before the runs; stage 3's report does that,
and an expectation that contradicts a direction is a finding.

### How to run (stage 3)

```
analysis/instruments/irb/run.sh kitting -o analysis/kitting/irb/tk2 configs/kitting/irb/tk2/*.yaml
analysis/instruments/irb/run.sh kitting --context off -o analysis/kitting/irb/tk2/off \
    configs/kitting/irb/tk2/scenario_s13_15.yaml configs/kitting/irb/tk2/scenario_s15_21.yaml
analysis/instruments/irb/offon.py analysis/kitting/irb/tk2 actual.csv 0.75 analysis/kitting/irb/tk2/off analysis/kitting/irb/tk1
```

The expectations were written by the same `run.sh` with `--expect` (on: all 57; off: the two new scripts).

### md5s of the expectations (committed before any run with context knowledge on)

```
cb858c0565744aa070b589dd0944412f  scenario_s13_01/expected.csv
3b232fe5c0cd7d1dfdf1daf8533de90e  scenario_s13_02/expected.csv
e3a19902c7a05b5780b548c01ce9d743  scenario_s13_03/expected.csv
dd4633872ef4e6bf4df2bc7444a26c76  scenario_s13_04/expected.csv
f60d8f5a41c70ae0f698e2ee70817e75  scenario_s13_05/expected.csv
7204b177f1f0528ac33f70758083b41e  scenario_s13_06/expected.csv
c8284e4154c87a1cf7d1645731a0fbed  scenario_s13_07/expected.csv
5ef98e7f0f3838289dc2f5a638219eb5  scenario_s13_08/expected.csv
2272a8574e27d1f73052abd187dee222  scenario_s13_09/expected.csv
ac4bbd4d4abc1f8a09eccddf5c72c814  scenario_s13_10/expected.csv
5672f902698a2531e91ec0865d2fe3e3  scenario_s13_11/expected.csv
b807cdb610c7c04baf7debb47e68fe7d  scenario_s13_12/expected.csv
c8b9fea71379fb73c3d2d18171431191  scenario_s13_13/expected.csv
873e051be0a78e27b5819a3665fccf9d  scenario_s13_14/expected.csv
1493f5f16af43ccb5192dff00bf45d46  scenario_s13_15/expected.csv
f4220c343311550b4dde50c98e1dbca1  scenario_s14_01/expected.csv
74a3778671c3682b36173ccd1d92582d  scenario_s14_02/expected.csv
337b8e5d2015d66c554262c43ab10826  scenario_s14_03/expected.csv
04a98332cea3b2a95e4193eb9a7fb874  scenario_s14_04/expected.csv
10993c6f290758376bf1668743aa34b5  scenario_s14_05/expected.csv
a4c71761c1ffcbdd93ad48a0fa003391  scenario_s14_06/expected.csv
6b8d9142f77fda2e27fa611cebe6b253  scenario_s14_07/expected.csv
d25a834428ec43403a8f9600155428e5  scenario_s14_08/expected.csv
74b41aaea902853589e629c92fb38179  scenario_s14_09/expected.csv
a4bf8cf1fffc3a73e11c98232d7c92cc  scenario_s14_10/expected.csv
c652aa766a1d0f157f5a9035e089214a  scenario_s14_11/expected.csv
79ab34b94d0d7f9229f2046e78a76702  scenario_s14_12/expected.csv
e16e95a779d78bd1a67f2a00044e232d  scenario_s14_13/expected.csv
faaf840cb257926bb03a0361aca8f86f  scenario_s14_14/expected.csv
8dd26220afe87fd86a5f12ad25febb94  scenario_s14_15/expected.csv
4456db13ef76805d9a422dbd95c6d39b  scenario_s14_16/expected.csv
c4c69ffcd6a1f4ccda63a2f084b74451  scenario_s14_17/expected.csv
60a93e8eb0029151eef270a398fecd71  scenario_s14_18/expected.csv
e84229019798b36315260f465c178775  scenario_s14_19/expected.csv
65d8ee92240e761014603fdc73a6d35a  scenario_s14_20/expected.csv
67e2d92f00aab789c3d1941813fd69c6  scenario_s14_21/expected.csv
4b40171056b0eabdf1b28ce45c132875  scenario_s15_01/expected.csv
1f44f82222020d20fce081f94564b1ca  scenario_s15_02/expected.csv
c8faf3d733e7d54f097064aa046c9469  scenario_s15_03/expected.csv
9fa5f08ce3e3606cadb8e5d66bb1a445  scenario_s15_04/expected.csv
22189f22f6743cec4645a5c056f09e05  scenario_s15_05/expected.csv
3fa10e8c7b1772d9a3efe11750e60389  scenario_s15_06/expected.csv
6c34c63f9e7f81d02192dd38e317b084  scenario_s15_07/expected.csv
53ac3ad8517a8f35ca59506539a4ce06  scenario_s15_08/expected.csv
aa179fba979de07f56b0950169c2db08  scenario_s15_09/expected.csv
b8848f5514ea567b8a3560d1402c872f  scenario_s15_10/expected.csv
47ffa3f2eac2b634e5f1518eea9f6743  scenario_s15_11/expected.csv
20a3bd3c0522142bb2adb92d86d2a887  scenario_s15_12/expected.csv
c2ca5936849476ac00354e125222f75d  scenario_s15_13/expected.csv
46f92b4dec7d4118363276b8e2932a2e  scenario_s15_14/expected.csv
42f64880398c2e368c1e0956ee64ce58  scenario_s15_15/expected.csv
c829236b0079d9572779f4e0b7d79e05  scenario_s15_16/expected.csv
810dcf3d27ad1456d6c086f6ec06e171  scenario_s15_17/expected.csv
14fe7242f950c3edc5e983821c9bc6b7  scenario_s15_18/expected.csv
428bf40d72c330ba5d62fc31f6d6e6a1  scenario_s15_19/expected.csv
ea27837c1949e59aefb73cc5630ec297  scenario_s15_20/expected.csv
c0b737c206e8dfe82a790589b509968e  scenario_s15_21/expected.csv
d2727d1fed42826c131931a262190d1a  scenario_s13_01/trajectory.json
ccc11a493ac3df2a73ed15769380a60b  scenario_s13_02/trajectory.json
18f19dc20a603a7d6eeb68d36a54c223  scenario_s13_03/trajectory.json
d6ca6c0958ad6dd905bc64dc5839d33f  scenario_s13_04/trajectory.json
aef42d17564d75b5cc9eece92b10dd53  scenario_s13_05/trajectory.json
0df6475630923fe1f6f6333a5b1f1aa0  scenario_s13_06/trajectory.json
4e2206b04f11d969d8438f105295b795  scenario_s13_07/trajectory.json
0474745744f4598e94e4d0daccdb5488  scenario_s13_08/trajectory.json
6659034d66ffa3f4fdd7585035c2ec9f  scenario_s13_09/trajectory.json
0d551053819ca476e966668dfcfd07f2  scenario_s13_10/trajectory.json
cffdfc19ce0e5c23851ee1a7302c9516  scenario_s13_11/trajectory.json
f0ffb22cc1e22b01e8d0acd99ee2532f  scenario_s13_12/trajectory.json
a7ed198098178d35875bb53bb1e9e1dc  scenario_s13_13/trajectory.json
29ba71382a2e88d9ca2cfbe1e9117fce  scenario_s13_14/trajectory.json
544606d27c8f38d3e373c1ee0574fb53  scenario_s13_15/trajectory.json
dbf2a12e9b2bbbf8b5ba7aa87c2e9557  scenario_s14_01/trajectory.json
b125c846aca208bc873ff1c8fb5f0593  scenario_s14_02/trajectory.json
e8e0a4c11e9fdf16bf05d17686082e78  scenario_s14_03/trajectory.json
56af413ec15cc1d67ad14bf4a3c7342b  scenario_s14_04/trajectory.json
d47bbf9db020c2eb3858f2ecceffc8d7  scenario_s14_05/trajectory.json
4293479eb24b4ba84838ee799985b4f3  scenario_s14_06/trajectory.json
9971b3ba01dcc46725eb86040737ada9  scenario_s14_07/trajectory.json
54bc7db8019c08f8e43735e2eadb09e7  scenario_s14_08/trajectory.json
cdad13322ac2e7379d9e6163e42de710  scenario_s14_09/trajectory.json
f7b00a01594bb347fa16478046534f8d  scenario_s14_10/trajectory.json
ae9d8ce0d4569c3cdb54a3e9256e8f96  scenario_s14_11/trajectory.json
586784548a66eefbce8c64357e2eeab7  scenario_s14_12/trajectory.json
01e17aa6006e4d11eeb629e138e6ac21  scenario_s14_13/trajectory.json
f6c524e24a611eaf5715a7adae9cf80d  scenario_s14_14/trajectory.json
22534de601e8a15fee607286d869571f  scenario_s14_15/trajectory.json
43e28def32888092d67a290394dc1917  scenario_s14_16/trajectory.json
0e5d85d4e56091b8d2f30ff6f94142ae  scenario_s14_17/trajectory.json
6dad138989bfba9207ac84b4cd13ca99  scenario_s14_18/trajectory.json
e10b8051bc4700eb0b46b0f17f6a6321  scenario_s14_19/trajectory.json
bda024053ad7fb847804f27553e0a1da  scenario_s14_20/trajectory.json
904a145b12b583bf58e79452ad4c0b83  scenario_s14_21/trajectory.json
4cd0985df9a0fe85253e8645da37e44d  scenario_s15_01/trajectory.json
a3aea3a99d9bcf345f4a5bf408df76b9  scenario_s15_02/trajectory.json
c8f39af65f1d4fd2ef70eba44ceeeacd  scenario_s15_03/trajectory.json
bbbef9274a121942d82586dc9eca597f  scenario_s15_04/trajectory.json
fe8ea422743b1446204c096fd7b21563  scenario_s15_05/trajectory.json
d89f55e11b8a9e9cf420bfaa2028ede8  scenario_s15_06/trajectory.json
dd72b0dbbc9c9cdaaceec874df28c987  scenario_s15_07/trajectory.json
a6c7289c0c87a04d5baa5adcfddf09ac  scenario_s15_08/trajectory.json
177bac682c676e7c58d003fc8bdd33bf  scenario_s15_09/trajectory.json
7e9aa52d029e6b8e947b2867106fdf9e  scenario_s15_10/trajectory.json
80ae2023fdf79836b4a32f54f2d5f8d0  scenario_s15_11/trajectory.json
4ea9ea8cbf0de0aa3b4ab6e25b75acb6  scenario_s15_12/trajectory.json
11cf6fff5d8f2217b9f9c13eabd6c9c1  scenario_s15_13/trajectory.json
cb33406707949d1b4dd08c140f90173a  scenario_s15_14/trajectory.json
b762f70c1000a2dac61e64044dac0ccc  scenario_s15_15/trajectory.json
bbf31ee8bb3e94f84f9defe24cd7ed58  scenario_s15_16/trajectory.json
d081b251dec04d191244dc92f35d2332  scenario_s15_17/trajectory.json
6f4e491f6d1511115db6e363272def8f  scenario_s15_18/trajectory.json
973bff435e35434ddb053fc8b56df230  scenario_s15_19/trajectory.json
53e21ddfc629043ec2aff7d8c97d8e0d  scenario_s15_20/trajectory.json
7cf739e2c8a77dd878de89be857bd94a  scenario_s15_21/trajectory.json
ae4fcd15e6edaa92260f2ef2432a92f2  off/scenario_s13_15/expected.csv
9037ca49234f89e998261bc684f2adf4  off/scenario_s15_21/expected.csv
544606d27c8f38d3e373c1ee0574fb53  off/scenario_s13_15/trajectory.json
7cf739e2c8a77dd878de89be857bd94a  off/scenario_s15_21/trajectory.json
```

### The expectations, off against on (`offon.py analysis/kitting/irb/tk2 expected.csv 0.75 analysis/kitting/irb/tk2/off analysis/kitting/irb/tk1`)

The off side read from round 1's `expected.csv` (its oracle; round 1 agreed with it at 1e-9) and from `off/` for the
two new scripts.

From `expected.csv`, θ = 0.75; off: the same script's run in the off folder named. Ticks inclusive; delay from the stretch's first tick in brackets. "after admission": ticks from the admission to the pin on which the gate no longer clears for the true hypothesis (the retraction reading).

| scenario | timeline in force (on) | off from | true hypothesis | ticks | state at start (on) | first ≥ θ off | on | admitted off | on | after admission off | on | A/C belief at arrival off | on |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| s13_01 | break_time 178 to 300 | tk1/s13_01 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_01 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s13_01 | 〃 | 〃 | deliver_item(item_1) | 124 to 216 | coffee_break ordinary | 161 (37) | 161 (37) | 161 (37) | 161 (37) | - | - | - | - |
| s13_01 | 〃 | 〃 | deliver_item(item_4) | 217 to 308 | coffee_break raised | 248 (31) | 253 (36) | 248 (31) | 253 (36) | - | - | - | - |
| s13_02 | break_time 178 to 300 | tk1/s13_02 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_02 | 〃 | 〃 | coffee_break(coffee_machine_0) | 67 to 140 | ordinary | 101 (34) | 117 (50) | 101 (34) | 117 (50) | - | - | - | - |
| s13_02 | 〃 | 〃 | deliver_item(item_2) | 141 to 192 | coffee_break suppressed | 149 (8) | 149 (8) | 149 (8) | 149 (8) | - | - | - | - |
| s13_02 | 〃 | 〃 | deliver_item(item_1) | 193 to 285 | coffee_break suppressed | 230 (37) | 231 (38) | 230 (37) | 231 (38) | - | - | - | - |
| s13_02 | 〃 | 〃 | deliver_item(item_4) | 286 to 377 | coffee_break raised | 317 (31) | 300 (14) | 317 (31) | 300 (14) | - | - | - | - |
| s13_03 | break_time 178 to 300 | tk1/s13_03 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_03 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s13_03 | 〃 | 〃 | coffee_break(coffee_machine_0) | 124 to 197 | ordinary | 158 (34) | 175 (51) | 158 (34) | 175 (51) | - | - | - | - |
| s13_03 | 〃 | 〃 | deliver_item(item_1) | 198 to 279 | coffee_break suppressed | 219 (21) | 219 (21) | 219 (21) | 219 (21) | - | - | - | - |
| s13_03 | 〃 | 〃 | deliver_item(item_4) | 280 to 371 | coffee_break suppressed | 311 (31) | 280 (0) | 311 (31) | 280 (0) | - | 286 to 299 none(below_theta) (coffee_break(coffee_machine_0)) | - | - |
| s13_04 | break_time 178 to 300 | tk1/s13_04 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_04 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s13_04 | 〃 | 〃 | deliver_item(item_1) | 124 to 216 | coffee_break ordinary | 161 (37) | 161 (37) | 161 (37) | 161 (37) | - | - | - | - |
| s13_04 | 〃 | 〃 | coffee_break(coffee_machine_0) | 217 to 289 | raised | 249 (32) | 238 (21) | 249 (32) | 238 (21) | - | - | - | - |
| s13_04 | 〃 | 〃 | deliver_item(item_4) | 290 to 356 | coffee_break suppressed | 295 (5) | 290 (0) | 295 (5) | 290 (0) | - | - | - | - |
| s13_05 | break_time 178 to 300 | tk1/s13_05 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_05 | 〃 | 〃 | deliver_item(item_2) | 67 to 93 | coffee_break ordinary | never | 87 (20) | never | 87 (20) | - | - | - | - |
| s13_05 | 〃 | 〃 | coffee_break(coffee_machine_0) | 94 to 146 | ordinary | 103 (9) | 120 (26) | 103 (9) | 120 (26) | - | - | - | - |
| s13_05 | 〃 | 〃 | deliver_item(item_2) | 147 to 198 | coffee_break suppressed | 156 (9) | 155 (8) | 156 (9) | 155 (8) | - | - | - | - |
| s13_05 | 〃 | 〃 | deliver_item(item_1) | 199 to 291 | coffee_break suppressed | 236 (37) | 237 (38) | 236 (37) | 237 (38) | - | - | - | - |
| s13_05 | 〃 | 〃 | deliver_item(item_4) | 292 to 383 | coffee_break raised | 323 (31) | 300 (8) | 323 (31) | 300 (8) | - | - | - | - |
| s13_06 | break_time 178 to 300 | tk1/s13_06 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_06 | 〃 | 〃 | deliver_item(item_2) | 67 to 95 | coffee_break ordinary | never | 87 (20) | never | 87 (20) | - | - | - | - |
| s13_06 | 〃 | 〃 | coffee_break(coffee_machine_0) | 96 to 148 | ordinary | 104 (8) | 112 (16) | 104 (8) | 112 (16) | - | - | - | - |
| s13_06 | 〃 | 〃 | deliver_item(item_2) | 149 to 193 | coffee_break suppressed | 170 (21) | 170 (21) | 170 (21) | 170 (21) | - | - | - | - |
| s13_06 | 〃 | 〃 | deliver_item(item_1) | 194 to 286 | coffee_break suppressed | 231 (37) | 231 (37) | 231 (37) | 231 (37) | - | - | - | - |
| s13_06 | 〃 | 〃 | deliver_item(item_4) | 287 to 378 | coffee_break raised | 318 (31) | 300 (13) | 318 (31) | 300 (13) | - | - | - | - |
| s13_07 | break_time 178 to 300 | tk1/s13_07 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_07 | 〃 | 〃 | deliver_item(item_2) | 67 to 121 | coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s13_07 | 〃 | 〃 | coffee_break(coffee_machine_0) | 122 to 195 | ordinary | 153 (31) | 160 (38) | 163 (41) | 163 (41) | - | - | - | - |
| s13_07 | 〃 | 〃 | deliver_item(item_2) | 196 to 240 | coffee_break suppressed | 217 (21) | 217 (21) | 217 (21) | 217 (21) | - | - | - | - |
| s13_07 | 〃 | 〃 | deliver_item(item_1) | 241 to 334 | coffee_break suppressed | 278 (37) | 278 (37) | 278 (37) | 278 (37) | - | - | - | - |
| s13_07 | 〃 | 〃 | deliver_item(item_4) | 335 to 428 | coffee_break ordinary | 367 (32) | 335 (0) | 367 (32) | 335 (0) | - | - | - | - |
| s13_08 | break_time 50 to 200 | tk1/s13_02 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_08 | 〃 | 〃 | coffee_break(coffee_machine_0) | 67 to 140 | raised | 101 (34) | 82 (15) | 101 (34) | 82 (15) | - | - | - | - |
| s13_08 | 〃 | 〃 | deliver_item(item_2) | 141 to 192 | coffee_break suppressed | 149 (8) | 149 (8) | 149 (8) | 149 (8) | - | - | - | - |
| s13_08 | 〃 | 〃 | deliver_item(item_1) | 193 to 285 | coffee_break suppressed | 230 (37) | 230 (37) | 230 (37) | 230 (37) | - | - | - | - |
| s13_08 | 〃 | 〃 | deliver_item(item_4) | 286 to 377 | coffee_break ordinary | 317 (31) | 286 (0) | 317 (31) | 286 (0) | - | - | - | - |
| s13_09 | break_time 90 to 200 | tk1/s13_02 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_09 | 〃 | 〃 | coffee_break(coffee_machine_0) | 67 to 140 | ordinary | 101 (34) | 90 (23) | 101 (34) | 90 (23) | - | - | - | - |
| s13_09 | 〃 | 〃 | deliver_item(item_2) | 141 to 192 | coffee_break suppressed | 149 (8) | 149 (8) | 149 (8) | 149 (8) | - | - | - | - |
| s13_09 | 〃 | 〃 | deliver_item(item_1) | 193 to 285 | coffee_break suppressed | 230 (37) | 230 (37) | 230 (37) | 230 (37) | - | - | - | - |
| s13_09 | 〃 | 〃 | deliver_item(item_4) | 286 to 377 | coffee_break ordinary | 317 (31) | 286 (0) | 317 (31) | 286 (0) | - | - | - | - |
| s13_10 | break_time 120 to 200 | tk1/s13_02 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_10 | 〃 | 〃 | coffee_break(coffee_machine_0) | 67 to 140 | ordinary | 101 (34) | 117 (50) | 101 (34) | 117 (50) | - | - | - | - |
| s13_10 | 〃 | 〃 | deliver_item(item_2) | 141 to 192 | coffee_break suppressed | 149 (8) | 149 (8) | 149 (8) | 149 (8) | - | - | - | - |
| s13_10 | 〃 | 〃 | deliver_item(item_1) | 193 to 285 | coffee_break suppressed | 230 (37) | 230 (37) | 230 (37) | 230 (37) | - | - | - | - |
| s13_10 | 〃 | 〃 | deliver_item(item_4) | 286 to 377 | coffee_break ordinary | 317 (31) | 286 (0) | 317 (31) | 286 (0) | - | - | - | - |
| s13_11 | break_time 40 to 190 | tk1/s13_03 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_11 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | coffee_break raised | 97 (30) | 102 (35) | 97 (30) | 102 (35) | - | - | - | - |
| s13_11 | 〃 | 〃 | coffee_break(coffee_machine_0) | 124 to 197 | raised | 158 (34) | 138 (14) | 158 (34) | 138 (14) | - | - | - | - |
| s13_11 | 〃 | 〃 | deliver_item(item_1) | 198 to 279 | coffee_break suppressed | 219 (21) | 219 (21) | 219 (21) | 219 (21) | - | - | - | - |
| s13_11 | 〃 | 〃 | deliver_item(item_4) | 280 to 371 | coffee_break suppressed | 311 (31) | 280 (0) | 311 (31) | 280 (0) | - | - | - | - |
| s13_12 | break_time 40 to 150 | tk1/s13_03 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_12 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | coffee_break raised | 97 (30) | 102 (35) | 97 (30) | 102 (35) | - | - | - | - |
| s13_12 | 〃 | 〃 | coffee_break(coffee_machine_0) | 124 to 197 | raised | 158 (34) | 138 (14) | 158 (34) | 138 (14) | - | 150 to 161 clears (deliver_item(item_4)); 162 to 169 none(below_theta) (deliver_item(item_4)); 170 to 174 none(below_theta) (coffee_break(coffee_machine_0)) | - | - |
| s13_12 | 〃 | 〃 | deliver_item(item_1) | 198 to 279 | coffee_break suppressed | 219 (21) | 219 (21) | 219 (21) | 219 (21) | - | - | - | - |
| s13_12 | 〃 | 〃 | deliver_item(item_4) | 280 to 371 | coffee_break suppressed | 311 (31) | 280 (0) | 311 (31) | 280 (0) | - | - | - | - |
| s13_13 | none | tk1/s13_04 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_13 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s13_13 | 〃 | 〃 | deliver_item(item_1) | 124 to 216 | coffee_break ordinary | 161 (37) | 161 (37) | 161 (37) | 161 (37) | - | - | - | - |
| s13_13 | 〃 | 〃 | coffee_break(coffee_machine_0) | 217 to 289 | ordinary | 249 (32) | 271 (54) | 249 (32) | 271 (54) | - | - | - | - |
| s13_13 | 〃 | 〃 | deliver_item(item_4) | 290 to 356 | coffee_break suppressed | 295 (5) | 290 (0) | 295 (5) | 290 (0) | - | - | - | - |
| s13_14 | break_time 0 to end | tk1/s13_01 | deliver_item(item_3) | 0 to 66 | coffee_break raised | 26 (26) | 27 (27) | 26 (26) | 27 (27) | - | - | - | - |
| s13_14 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | coffee_break raised | 97 (30) | 102 (35) | 97 (30) | 102 (35) | - | - | - | - |
| s13_14 | 〃 | 〃 | deliver_item(item_1) | 124 to 216 | coffee_break raised | 161 (37) | 162 (38) | 161 (37) | 162 (38) | - | - | - | - |
| s13_14 | 〃 | 〃 | deliver_item(item_4) | 217 to 308 | coffee_break raised | 248 (31) | 253 (36) | 248 (31) | 253 (36) | - | - | - | - |
| s13_15 | none | off/s13_15 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_15 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s13_15 | 〃 | 〃 | deliver_item(item_1) | 124 to 216 | coffee_break ordinary | 161 (37) | 161 (37) | 161 (37) | 161 (37) | - | - | - | - |
| s13_15 | 〃 | 〃 | deliver_item(item_4) | 217 to 260 | coffee_break ordinary | 248 (31) | 217 (0) | 248 (31) | 217 (0) | - | - | - | - |
| s13_15 | 〃 | 〃 | coffee_break(coffee_machine_0) | 261 to 309 | ordinary | 274 (13) | 291 (30) | 277 (16) | 291 (30) | - | - | - | - |
| s13_15 | 〃 | 〃 | deliver_item(item_4) | 310 to 375 | coffee_break suppressed | 315 (5) | 310 (0) | 315 (5) | 310 (0) | - | - | - | - |
| s14_01 | break_time 178 to 300 | tk1/s14_01 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_01 | 〃 | 〃 | deliver_item(item_2) | 89 to 180 | ac_activation ordinary coffee_break ordinary | 138 (49) | 129 (40) | 138 (49) | 129 (40) | - | - | - | - |
| s14_01 | 〃 | 〃 | deliver_item(item_1) | 181 to 282 | ac_activation ordinary coffee_break raised | 232 (51) | 234 (53) | 232 (51) | 234 (53) | - | - | - | - |
| s14_02 | break_time 178 to 300 | tk1/s14_02 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_02 | 〃 | 〃 | coffee_break(coffee_machine_0) | 89 to 166 | ordinary | 143 (54) | 157 (68) | 143 (54) | 157 (68) | - | - | - | - |
| s14_02 | 〃 | 〃 | deliver_item(item_2) | 167 to 225 | ac_activation ordinary coffee_break suppressed | 177 (10) | 171 (4) | 177 (10) | 171 (4) | - | - | - | - |
| s14_02 | 〃 | 〃 | deliver_item(item_1) | 226 to 325 | ac_activation ordinary coffee_break suppressed | 277 (51) | 226 (0) | 277 (51) | 226 (0) | - | 255 to 271 none(below_theta) (coffee_break(coffee_machine_0)); 272 to 277 none(below_theta) (deliver_item(item_1)) | - | - |
| s14_03 | break_time 178 to 300 | tk1/s14_03 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_03 | 〃 | 〃 | deliver_item(item_2) | 89 to 180 | ac_activation ordinary coffee_break ordinary | 138 (49) | 129 (40) | 138 (49) | 129 (40) | - | - | - | - |
| s14_03 | 〃 | 〃 | coffee_break(coffee_machine_0) | 181 to 259 | raised | 235 (54) | 226 (45) | 235 (54) | 226 (45) | - | - | - | - |
| s14_03 | 〃 | 〃 | deliver_item(item_1) | 260 to 318 | ac_activation ordinary coffee_break suppressed | 269 (9) | 260 (0) | 269 (9) | 260 (0) | - | - | - | - |
| s14_04 | break_time 178 to 300 | tk1/s14_04 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_04 | 〃 | 〃 | deliver_item(item_2) | 89 to 132 | ac_activation ordinary coffee_break ordinary | never | 129 (40) | never | 129 (40) | - | - | - | - |
| s14_04 | 〃 | 〃 | coffee_break(coffee_machine_0) | 133 to 174 | ordinary | 149 (16) | 162 (29) | 149 (16) | 162 (29) | - | - | - | - |
| s14_04 | 〃 | 〃 | deliver_item(item_2) | 175 to 233 | ac_activation ordinary coffee_break suppressed | 187 (12) | 179 (4) | 187 (12) | 179 (4) | - | - | - | - |
| s14_04 | 〃 | 〃 | deliver_item(item_1) | 234 to 333 | ac_activation ordinary coffee_break suppressed | 285 (51) | 234 (0) | 285 (51) | 234 (0) | - | 263 to 279 none(below_theta) (coffee_break(coffee_machine_0)); 280 to 285 none(below_theta) (deliver_item(item_1)) | - | - |
| s14_05 | break_time 178 to 300 | tk1/s14_05 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_05 | 〃 | 〃 | deliver_item(item_2) | 89 to 134 | ac_activation ordinary coffee_break ordinary | never | 129 (40) | never | 129 (40) | - | - | - | - |
| s14_05 | 〃 | 〃 | coffee_break(coffee_machine_0) | 135 to 176 | ordinary | 150 (15) | 163 (28) | 150 (15) | 163 (28) | - | - | - | - |
| s14_05 | 〃 | 〃 | deliver_item(item_2) | 177 to 226 | ac_activation ordinary coffee_break suppressed | 187 (10) | 184 (7) | 187 (10) | 184 (7) | - | - | - | - |
| s14_05 | 〃 | 〃 | deliver_item(item_1) | 227 to 328 | ac_activation ordinary coffee_break suppressed | 278 (51) | 227 (0) | 278 (51) | 227 (0) | - | 265 to 272 none(below_theta) (coffee_break(coffee_machine_0)); 273 to 279 none(below_theta) (deliver_item(item_1)) | - | - |
| s14_06 | break_time 178 to 300 | tk1/s14_06 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_06 | 〃 | 〃 | deliver_item(item_2) | 89 to 178 | ac_activation ordinary coffee_break ordinary | 138 (49) | 129 (40) | 138 (49) | 129 (40) | - | - | - | - |
| s14_06 | 〃 | 〃 | coffee_break(coffee_machine_0) | 179 to 257 | raised | 231 (52) | 224 (45) | 231 (52) | 225 (46) | - | - | - | - |
| s14_06 | 〃 | 〃 | deliver_item(item_2) | 258 to 307 | ac_activation ordinary coffee_break suppressed | 267 (9) | 265 (7) | 267 (9) | 265 (7) | - | - | - | - |
| s14_06 | 〃 | 〃 | deliver_item(item_1) | 308 to 409 | ac_activation ordinary coffee_break suppressed | 359 (51) | 308 (0) | 359 (51) | 308 (0) | - | - | - | - |
| s14_07 | room_warm 150 to end | tk1/s14_07 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_07 | 〃 | 〃 | ac_activation(ac_switch_0) | 89 to 137 | ordinary | never | never | never | never | - | - | 0.4626 at 135 | 0.0599 at 135 |
| s14_07 | 〃 | 〃 | deliver_item(item_2) | 138 to 192 | ac_activation suppressed coffee_break ordinary | 148 (10) | 142 (4) | 148 (10) | 142 (4) | - | - | - | - |
| s14_07 | 〃 | 〃 | deliver_item(item_1) | 193 to 294 | ac_activation suppressed coffee_break ordinary | 244 (51) | 193 (0) | 244 (51) | 193 (0) | - | - | - | - |
| s14_08 | room_warm 150 to end | tk1/s14_08 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_08 | 〃 | 〃 | deliver_item(item_2) | 89 to 180 | ac_activation ordinary coffee_break ordinary | 138 (49) | 129 (40) | 138 (49) | 129 (40) | - | - | - | - |
| s14_08 | 〃 | 〃 | ac_activation(ac_switch_0) | 181 to 229 | raised | never | never | never | never | - | - | 0.5475 at 227 | 0.6449 at 227 |
| s14_08 | 〃 | 〃 | deliver_item(item_1) | 230 to 293 | ac_activation suppressed coffee_break ordinary | 242 (12) | 230 (0) | 242 (12) | 230 (0) | - | - | - | - |
| s14_09 | room_warm 150 to end | tk1/s14_09 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_09 | 〃 | 〃 | deliver_item(item_2) | 89 to 132 | ac_activation ordinary coffee_break ordinary | never | 129 (40) | never | 129 (40) | - | - | - | - |
| s14_09 | 〃 | 〃 | ac_activation(ac_switch_0) | 133 to 140 | ordinary | never | never | never | never | - | - | 0.4456 at 138 | 0.0467 at 138 |
| s14_09 | 〃 | 〃 | deliver_item(item_2) | 141 to 194 | ac_activation suppressed coffee_break ordinary | 151 (10) | 149 (8) | 151 (10) | 149 (8) | - | - | - | - |
| s14_09 | 〃 | 〃 | deliver_item(item_1) | 195 to 296 | ac_activation suppressed coffee_break ordinary | 246 (51) | 195 (0) | 246 (51) | 195 (0) | - | - | - | - |
| s14_10 | room_warm 150 to end | tk1/s14_10 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_10 | 〃 | 〃 | deliver_item(item_2) | 89 to 134 | ac_activation ordinary coffee_break ordinary | never | 129 (40) | never | 129 (40) | - | - | - | - |
| s14_10 | 〃 | 〃 | ac_activation(ac_switch_0) | 135 to 142 | ordinary | never | never | never | never | - | - | 0.4814 at 140 | 0.0558 at 140 |
| s14_10 | 〃 | 〃 | deliver_item(item_2) | 143 to 191 | ac_activation suppressed coffee_break ordinary | 151 (8) | 149 (6) | 151 (8) | 149 (6) | - | - | - | - |
| s14_10 | 〃 | 〃 | deliver_item(item_1) | 192 to 293 | ac_activation suppressed coffee_break ordinary | 243 (51) | 192 (0) | 243 (51) | 192 (0) | - | - | - | - |
| s14_11 | room_warm 150 to end | tk1/s14_11 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_11 | 〃 | 〃 | deliver_item(item_2) | 89 to 178 | ac_activation ordinary coffee_break ordinary | 138 (49) | 129 (40) | 138 (49) | 129 (40) | - | - | - | - |
| s14_11 | 〃 | 〃 | ac_activation(ac_switch_0) | 179 to 227 | raised | never | never | never | never | - | - | 0.4351 at 225 | 0.5192 at 225 |
| s14_11 | 〃 | 〃 | deliver_item(item_2) | 228 to 276 | ac_activation suppressed coffee_break ordinary | 236 (8) | 234 (6) | 236 (8) | 234 (6) | - | - | - | - |
| s14_11 | 〃 | 〃 | deliver_item(item_1) | 277 to 378 | ac_activation suppressed coffee_break ordinary | 328 (51) | 277 (0) | 328 (51) | 277 (0) | - | - | - | - |
| s14_12 | break_time 70 to 250 | tk1/s14_02 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_12 | 〃 | 〃 | coffee_break(coffee_machine_0) | 89 to 166 | raised | 143 (54) | 129 (40) | 143 (54) | 129 (40) | - | - | - | - |
| s14_12 | 〃 | 〃 | deliver_item(item_2) | 167 to 225 | ac_activation ordinary coffee_break suppressed | 177 (10) | 171 (4) | 177 (10) | 171 (4) | - | - | - | - |
| s14_12 | 〃 | 〃 | deliver_item(item_1) | 226 to 325 | ac_activation ordinary coffee_break suppressed | 277 (51) | 226 (0) | 277 (51) | 226 (0) | - | - | - | - |
| s14_13 | break_time 110 to 250 | tk1/s14_02 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_13 | 〃 | 〃 | coffee_break(coffee_machine_0) | 89 to 166 | ordinary | 143 (54) | 129 (40) | 143 (54) | 129 (40) | - | - | - | - |
| s14_13 | 〃 | 〃 | deliver_item(item_2) | 167 to 225 | ac_activation ordinary coffee_break suppressed | 177 (10) | 171 (4) | 177 (10) | 171 (4) | - | - | - | - |
| s14_13 | 〃 | 〃 | deliver_item(item_1) | 226 to 325 | ac_activation ordinary coffee_break suppressed | 277 (51) | 226 (0) | 277 (51) | 226 (0) | - | - | - | - |
| s14_14 | break_time 150 to 250 | tk1/s14_02 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_14 | 〃 | 〃 | coffee_break(coffee_machine_0) | 89 to 166 | ordinary | 143 (54) | 150 (61) | 143 (54) | 150 (61) | - | - | - | - |
| s14_14 | 〃 | 〃 | deliver_item(item_2) | 167 to 225 | ac_activation ordinary coffee_break suppressed | 177 (10) | 171 (4) | 177 (10) | 171 (4) | - | - | - | - |
| s14_14 | 〃 | 〃 | deliver_item(item_1) | 226 to 325 | ac_activation ordinary coffee_break suppressed | 277 (51) | 226 (0) | 277 (51) | 226 (0) | - | - | - | - |
| s14_15 | room_warm 70 to end | tk1/s14_07 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_15 | 〃 | 〃 | ac_activation(ac_switch_0) | 89 to 137 | raised | never | never | never | never | - | - | 0.4626 at 135 | 0.6144 at 135 |
| s14_15 | 〃 | 〃 | deliver_item(item_2) | 138 to 192 | ac_activation suppressed coffee_break ordinary | 148 (10) | 142 (4) | 148 (10) | 142 (4) | - | - | - | - |
| s14_15 | 〃 | 〃 | deliver_item(item_1) | 193 to 294 | ac_activation suppressed coffee_break ordinary | 244 (51) | 193 (0) | 244 (51) | 193 (0) | - | - | - | - |
| s14_16 | room_warm 110 to end | tk1/s14_07 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_16 | 〃 | 〃 | ac_activation(ac_switch_0) | 89 to 137 | ordinary | never | never | never | never | - | - | 0.4626 at 135 | 0.6144 at 135 |
| s14_16 | 〃 | 〃 | deliver_item(item_2) | 138 to 192 | ac_activation suppressed coffee_break ordinary | 148 (10) | 142 (4) | 148 (10) | 142 (4) | - | - | - | - |
| s14_16 | 〃 | 〃 | deliver_item(item_1) | 193 to 294 | ac_activation suppressed coffee_break ordinary | 244 (51) | 193 (0) | 244 (51) | 193 (0) | - | - | - | - |
| s14_17 | room_warm 0 to 110 | tk1/s14_07 | deliver_item(item_0) | 0 to 88 | ac_activation raised coffee_break ordinary | 50 (50) | 49 (49) | 50 (50) | 49 (49) | - | - | - | - |
| s14_17 | 〃 | 〃 | ac_activation(ac_switch_0) | 89 to 137 | raised | never | never | never | never | - | - | 0.4626 at 135 | 0.0599 at 135 |
| s14_17 | 〃 | 〃 | deliver_item(item_2) | 138 to 192 | ac_activation suppressed coffee_break ordinary | 148 (10) | 142 (4) | 148 (10) | 142 (4) | - | - | - | - |
| s14_17 | 〃 | 〃 | deliver_item(item_1) | 193 to 294 | ac_activation suppressed coffee_break ordinary | 244 (51) | 193 (0) | 244 (51) | 193 (0) | - | - | - | - |
| s14_18 | break_time 60 to 250 | tk1/s14_03 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_18 | 〃 | 〃 | deliver_item(item_2) | 89 to 180 | ac_activation ordinary coffee_break raised | 138 (49) | 139 (50) | 138 (49) | 139 (50) | - | - | - | - |
| s14_18 | 〃 | 〃 | coffee_break(coffee_machine_0) | 181 to 259 | raised | 235 (54) | 226 (45) | 235 (54) | 226 (45) | - | 250 to 251 none(below_theta) (coffee_break(coffee_machine_0)) | - | - |
| s14_18 | 〃 | 〃 | deliver_item(item_1) | 260 to 318 | ac_activation ordinary coffee_break suppressed | 269 (9) | 260 (0) | 269 (9) | 260 (0) | - | - | - | - |
| s14_19 | none | tk1/s14_03 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_19 | 〃 | 〃 | deliver_item(item_2) | 89 to 180 | ac_activation ordinary coffee_break ordinary | 138 (49) | 129 (40) | 138 (49) | 129 (40) | - | - | - | - |
| s14_19 | 〃 | 〃 | coffee_break(coffee_machine_0) | 181 to 259 | ordinary | 235 (54) | 252 (71) | 235 (54) | 252 (71) | - | - | - | - |
| s14_19 | 〃 | 〃 | deliver_item(item_1) | 260 to 318 | ac_activation ordinary coffee_break suppressed | 269 (9) | 260 (0) | 269 (9) | 260 (0) | - | - | - | - |
| s14_20 | break_time 0 to end | tk1/s14_01 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break raised | 50 (50) | 51 (51) | 50 (50) | 51 (51) | - | - | - | - |
| s14_20 | 〃 | 〃 | deliver_item(item_2) | 89 to 180 | ac_activation ordinary coffee_break raised | 138 (49) | 139 (50) | 138 (49) | 139 (50) | - | - | - | - |
| s14_20 | 〃 | 〃 | deliver_item(item_1) | 181 to 282 | ac_activation ordinary coffee_break raised | 232 (51) | 234 (53) | 232 (51) | 234 (53) | - | - | - | - |
| s14_21 | break_time 178 to 300 | tk1/s14_08 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_21 | 〃 | 〃 | deliver_item(item_2) | 89 to 180 | ac_activation ordinary coffee_break ordinary | 138 (49) | 129 (40) | 138 (49) | 129 (40) | - | - | - | - |
| s14_21 | 〃 | 〃 | ac_activation(ac_switch_0) | 181 to 229 | ordinary | never | never | never | never | - | - | 0.5475 at 227 | 0.0142 at 227 |
| s14_21 | 〃 | 〃 | deliver_item(item_1) | 230 to 293 | ac_activation suppressed coffee_break raised | 242 (12) | 245 (15) | 242 (12) | 245 (15) | - | - | - | - |
| s15_01 | break_time 178 to 300 | tk1/s15_01 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_01 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | ac_activation ordinary coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s15_01 | 〃 | 〃 | deliver_item(item_1) | 124 to 216 | ac_activation ordinary coffee_break ordinary | 171 (47) | 162 (38) | 171 (47) | 162 (38) | - | - | - | - |
| s15_01 | 〃 | 〃 | deliver_item(item_4) | 217 to 308 | ac_activation ordinary coffee_break raised | 262 (45) | 254 (37) | 262 (45) | 254 (37) | - | - | - | - |
| s15_02 | break_time 178 to 300 | tk1/s15_02 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_02 | 〃 | 〃 | coffee_break(coffee_machine_0) | 67 to 140 | ordinary | 103 (36) | 117 (50) | 103 (36) | 117 (50) | - | - | - | - |
| s15_02 | 〃 | 〃 | deliver_item(item_2) | 141 to 192 | ac_activation ordinary coffee_break suppressed | 150 (9) | 149 (8) | 150 (9) | 149 (8) | - | - | - | - |
| s15_02 | 〃 | 〃 | deliver_item(item_1) | 193 to 285 | ac_activation ordinary coffee_break suppressed | 240 (47) | 232 (39) | 240 (47) | 232 (39) | - | - | - | - |
| s15_02 | 〃 | 〃 | deliver_item(item_4) | 286 to 377 | ac_activation ordinary coffee_break raised | 331 (45) | 300 (14) | 331 (45) | 300 (14) | - | - | - | - |
| s15_03 | break_time 178 to 300 | tk1/s15_03 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_03 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | ac_activation ordinary coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s15_03 | 〃 | 〃 | coffee_break(coffee_machine_0) | 124 to 197 | ordinary | 160 (36) | 176 (52) | 160 (36) | 176 (52) | - | - | - | - |
| s15_03 | 〃 | 〃 | deliver_item(item_1) | 198 to 279 | ac_activation ordinary coffee_break suppressed | 227 (29) | 219 (21) | 227 (29) | 219 (21) | - | - | - | - |
| s15_03 | 〃 | 〃 | deliver_item(item_4) | 280 to 371 | ac_activation ordinary coffee_break suppressed | 325 (45) | 280 (0) | 325 (45) | 280 (0) | - | 286 to 299 none(below_theta) (coffee_break(coffee_machine_0)) | - | - |
| s15_04 | break_time 178 to 300 | tk1/s15_04 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_04 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | ac_activation ordinary coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s15_04 | 〃 | 〃 | deliver_item(item_1) | 124 to 216 | ac_activation ordinary coffee_break ordinary | 171 (47) | 162 (38) | 171 (47) | 162 (38) | - | - | - | - |
| s15_04 | 〃 | 〃 | coffee_break(coffee_machine_0) | 217 to 289 | raised | 252 (35) | 238 (21) | 252 (35) | 238 (21) | - | - | - | - |
| s15_04 | 〃 | 〃 | deliver_item(item_4) | 290 to 356 | ac_activation ordinary coffee_break suppressed | 313 (23) | 290 (0) | 313 (23) | 290 (0) | - | - | - | - |
| s15_05 | break_time 178 to 300 | tk1/s15_05 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_05 | 〃 | 〃 | deliver_item(item_2) | 67 to 93 | ac_activation ordinary coffee_break ordinary | never | 87 (20) | never | 87 (20) | - | - | - | - |
| s15_05 | 〃 | 〃 | coffee_break(coffee_machine_0) | 94 to 146 | ordinary | 104 (10) | 120 (26) | 104 (10) | 120 (26) | - | - | - | - |
| s15_05 | 〃 | 〃 | deliver_item(item_2) | 147 to 198 | ac_activation ordinary coffee_break suppressed | 157 (10) | 155 (8) | 157 (10) | 155 (8) | - | - | - | - |
| s15_05 | 〃 | 〃 | deliver_item(item_1) | 199 to 291 | ac_activation ordinary coffee_break suppressed | 246 (47) | 238 (39) | 246 (47) | 238 (39) | - | - | - | - |
| s15_05 | 〃 | 〃 | deliver_item(item_4) | 292 to 383 | ac_activation ordinary coffee_break raised | 337 (45) | 300 (8) | 337 (45) | 300 (8) | - | - | - | - |
| s15_06 | break_time 178 to 300 | tk1/s15_06 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_06 | 〃 | 〃 | deliver_item(item_2) | 67 to 95 | ac_activation ordinary coffee_break ordinary | never | 87 (20) | never | 87 (20) | - | - | - | - |
| s15_06 | 〃 | 〃 | coffee_break(coffee_machine_0) | 96 to 148 | ordinary | 104 (8) | 112 (16) | 104 (8) | 112 (16) | - | - | - | - |
| s15_06 | 〃 | 〃 | deliver_item(item_2) | 149 to 193 | ac_activation ordinary coffee_break suppressed | 170 (21) | 170 (21) | 170 (21) | 170 (21) | - | - | - | - |
| s15_06 | 〃 | 〃 | deliver_item(item_1) | 194 to 286 | ac_activation ordinary coffee_break suppressed | 241 (47) | 232 (38) | 241 (47) | 232 (38) | - | - | - | - |
| s15_06 | 〃 | 〃 | deliver_item(item_4) | 287 to 378 | ac_activation ordinary coffee_break raised | 332 (45) | 300 (13) | 332 (45) | 300 (13) | - | - | - | - |
| s15_07 | break_time 178 to 300 | tk1/s15_07 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_07 | 〃 | 〃 | deliver_item(item_2) | 67 to 121 | ac_activation ordinary coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s15_07 | 〃 | 〃 | coffee_break(coffee_machine_0) | 122 to 195 | ordinary | 153 (31) | 160 (38) | 163 (41) | 163 (41) | - | - | - | - |
| s15_07 | 〃 | 〃 | deliver_item(item_2) | 196 to 240 | ac_activation ordinary coffee_break suppressed | 217 (21) | 217 (21) | 217 (21) | 217 (21) | - | - | - | - |
| s15_07 | 〃 | 〃 | deliver_item(item_1) | 241 to 334 | ac_activation ordinary coffee_break suppressed | 288 (47) | 278 (37) | 288 (47) | 278 (37) | - | - | - | - |
| s15_07 | 〃 | 〃 | deliver_item(item_4) | 335 to 428 | ac_activation ordinary coffee_break ordinary | 381 (46) | 335 (0) | 381 (46) | 335 (0) | - | - | - | - |
| s15_08 | room_warm 150 to end | tk1/s15_08 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_08 | 〃 | 〃 | ac_activation(ac_switch_0) | 67 to 114 | ordinary | never | never | never | never | - | - | 0.6238 at 112 | 0.0914 at 112 |
| s15_08 | 〃 | 〃 | deliver_item(item_2) | 115 to 183 | ac_activation suppressed coffee_break ordinary | 135 (20) | 125 (10) | 135 (20) | 125 (10) | - | - | - | - |
| s15_08 | 〃 | 〃 | deliver_item(item_1) | 184 to 276 | ac_activation suppressed coffee_break ordinary | 231 (47) | 221 (37) | 231 (47) | 221 (37) | - | - | - | - |
| s15_08 | 〃 | 〃 | deliver_item(item_4) | 277 to 368 | ac_activation suppressed coffee_break ordinary | 322 (45) | 277 (0) | 322 (45) | 277 (0) | - | - | - | - |
| s15_09 | room_warm 150 to end | tk1/s15_09 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_09 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | ac_activation ordinary coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s15_09 | 〃 | 〃 | ac_activation(ac_switch_0) | 124 to 171 | ordinary | never | never | never | never | - | - | 0.6130 at 169 | 0.6152 at 169 |
| s15_09 | 〃 | 〃 | deliver_item(item_1) | 172 to 229 | ac_activation suppressed coffee_break ordinary | 180 (8) | 176 (4) | 180 (8) | 176 (4) | - | - | - | - |
| s15_09 | 〃 | 〃 | deliver_item(item_4) | 230 to 323 | ac_activation suppressed coffee_break ordinary | 276 (46) | 230 (0) | 276 (46) | 230 (0) | - | - | - | - |
| s15_10 | room_warm 150 to end | tk1/s15_10 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_10 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | ac_activation ordinary coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s15_10 | 〃 | 〃 | deliver_item(item_1) | 124 to 216 | ac_activation ordinary coffee_break ordinary | 171 (47) | 171 (47) | 171 (47) | 171 (47) | - | - | - | - |
| s15_10 | 〃 | 〃 | ac_activation(ac_switch_0) | 217 to 263 | raised | never | never | never | never | - | - | 0.7487 at 261 | 0.6035 at 261 |
| s15_10 | 〃 | 〃 | deliver_item(item_4) | 264 to 321 | ac_activation suppressed coffee_break ordinary | 279 (15) | 264 (0) | 279 (15) | 264 (0) | - | - | - | - |
| s15_11 | room_warm 150 to end | tk1/s15_11 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_11 | 〃 | 〃 | deliver_item(item_2) | 67 to 93 | ac_activation ordinary coffee_break ordinary | never | 87 (20) | never | 87 (20) | - | - | - | - |
| s15_11 | 〃 | 〃 | ac_activation(ac_switch_0) | 94 to 134 | ordinary | never | never | never | never | - | - | 0.7468 at 132 | 0.1516 at 132 |
| s15_11 | 〃 | 〃 | deliver_item(item_2) | 135 to 203 | ac_activation suppressed coffee_break ordinary | 155 (20) | 145 (10) | 155 (20) | 145 (10) | - | - | - | - |
| s15_11 | 〃 | 〃 | deliver_item(item_1) | 204 to 296 | ac_activation suppressed coffee_break ordinary | 251 (47) | 241 (37) | 251 (47) | 241 (37) | - | - | - | - |
| s15_11 | 〃 | 〃 | deliver_item(item_4) | 297 to 388 | ac_activation suppressed coffee_break ordinary | 342 (45) | 297 (0) | 342 (45) | 297 (0) | - | - | - | - |
| s15_12 | room_warm 150 to end | tk1/s15_12 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_12 | 〃 | 〃 | deliver_item(item_2) | 67 to 95 | ac_activation ordinary coffee_break ordinary | never | 87 (20) | never | 87 (20) | - | - | - | - |
| s15_12 | 〃 | 〃 | ac_activation(ac_switch_0) | 96 to 136 | ordinary | 121 (25) | 125 (29) | 133 (37) | 133 (37) | - | - | 0.9961 at 134 | 0.9875 at 134 |
| s15_12 | 〃 | 〃 | deliver_item(item_2) | 137 to 184 | ac_activation suppressed coffee_break ordinary | 164 (27) | 164 (27) | 164 (27) | 164 (27) | - | - | - | - |
| s15_12 | 〃 | 〃 | deliver_item(item_1) | 185 to 278 | ac_activation suppressed coffee_break ordinary | 231 (46) | 221 (36) | 231 (46) | 221 (36) | - | - | - | - |
| s15_12 | 〃 | 〃 | deliver_item(item_4) | 279 to 372 | ac_activation suppressed coffee_break ordinary | 325 (46) | 279 (0) | 325 (46) | 279 (0) | - | - | - | - |
| s15_13 | room_warm 150 to end | tk1/s15_13 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_13 | 〃 | 〃 | deliver_item(item_2) | 67 to 121 | ac_activation ordinary coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s15_13 | 〃 | 〃 | ac_activation(ac_switch_0) | 122 to 169 | ordinary | 154 (32) | 152 (30) | 166 (44) | 166 (44) | - | - | 0.9952 at 167 | 0.9990 at 167 |
| s15_13 | 〃 | 〃 | deliver_item(item_2) | 170 to 216 | ac_activation suppressed coffee_break ordinary | 197 (27) | 197 (27) | 197 (27) | 197 (27) | - | - | - | - |
| s15_13 | 〃 | 〃 | deliver_item(item_1) | 217 to 308 | ac_activation suppressed coffee_break ordinary | 263 (46) | 253 (36) | 263 (46) | 253 (36) | - | - | - | - |
| s15_13 | 〃 | 〃 | deliver_item(item_4) | 309 to 400 | ac_activation suppressed coffee_break ordinary | 354 (45) | 309 (0) | 354 (45) | 309 (0) | - | - | - | - |
| s15_14 | room_warm 50 to end | tk1/s15_08 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_14 | 〃 | 〃 | ac_activation(ac_switch_0) | 67 to 114 | raised | never | never | never | never | - | - | 0.6238 at 112 | 0.7154 at 112 |
| s15_14 | 〃 | 〃 | deliver_item(item_2) | 115 to 183 | ac_activation suppressed coffee_break ordinary | 135 (20) | 125 (10) | 135 (20) | 125 (10) | - | - | - | - |
| s15_14 | 〃 | 〃 | deliver_item(item_1) | 184 to 276 | ac_activation suppressed coffee_break ordinary | 231 (47) | 221 (37) | 231 (47) | 221 (37) | - | - | - | - |
| s15_14 | 〃 | 〃 | deliver_item(item_4) | 277 to 368 | ac_activation suppressed coffee_break ordinary | 322 (45) | 277 (0) | 322 (45) | 277 (0) | - | - | - | - |
| s15_15 | room_warm 90 to end | tk1/s15_08 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_15 | 〃 | 〃 | ac_activation(ac_switch_0) | 67 to 114 | ordinary | never | never | never | never | - | - | 0.6238 at 112 | 0.7154 at 112 |
| s15_15 | 〃 | 〃 | deliver_item(item_2) | 115 to 183 | ac_activation suppressed coffee_break ordinary | 135 (20) | 125 (10) | 135 (20) | 125 (10) | - | - | - | - |
| s15_15 | 〃 | 〃 | deliver_item(item_1) | 184 to 276 | ac_activation suppressed coffee_break ordinary | 231 (47) | 221 (37) | 231 (47) | 221 (37) | - | - | - | - |
| s15_15 | 〃 | 〃 | deliver_item(item_4) | 277 to 368 | ac_activation suppressed coffee_break ordinary | 322 (45) | 277 (0) | 322 (45) | 277 (0) | - | - | - | - |
| s15_16 | room_warm 0 to 90 | tk1/s15_08 | deliver_item(item_3) | 0 to 66 | ac_activation raised coffee_break ordinary | 28 (28) | 30 (30) | 28 (28) | 30 (30) | - | - | - | - |
| s15_16 | 〃 | 〃 | ac_activation(ac_switch_0) | 67 to 114 | raised | never | never | never | never | - | - | 0.6238 at 112 | 0.0914 at 112 |
| s15_16 | 〃 | 〃 | deliver_item(item_2) | 115 to 183 | ac_activation suppressed coffee_break ordinary | 135 (20) | 125 (10) | 135 (20) | 125 (10) | - | - | - | - |
| s15_16 | 〃 | 〃 | deliver_item(item_1) | 184 to 276 | ac_activation suppressed coffee_break ordinary | 231 (47) | 221 (37) | 231 (47) | 221 (37) | - | - | - | - |
| s15_16 | 〃 | 〃 | deliver_item(item_4) | 277 to 368 | ac_activation suppressed coffee_break ordinary | 322 (45) | 277 (0) | 322 (45) | 277 (0) | - | - | - | - |
| s15_17 | break_time 178 to 300; room_warm 150 to end | tk1/s15_04 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_17 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | ac_activation ordinary coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s15_17 | 〃 | 〃 | deliver_item(item_1) | 124 to 216 | ac_activation ordinary coffee_break ordinary | 171 (47) | 171 (47) | 171 (47) | 171 (47) | - | - | - | - |
| s15_17 | 〃 | 〃 | coffee_break(coffee_machine_0) | 217 to 289 | raised | 252 (35) | 243 (26) | 252 (35) | 243 (26) | - | - | - | - |
| s15_17 | 〃 | 〃 | deliver_item(item_4) | 290 to 356 | ac_activation raised coffee_break suppressed | 313 (23) | 310 (20) | 313 (23) | 310 (20) | - | - | - | - |
| s15_18 | room_warm 0 to end | tk1/s15_01 | deliver_item(item_3) | 0 to 66 | ac_activation raised coffee_break ordinary | 28 (28) | 30 (30) | 28 (28) | 30 (30) | - | - | - | - |
| s15_18 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | ac_activation raised coffee_break ordinary | 97 (30) | 90 (23) | 97 (30) | 90 (23) | - | - | - | - |
| s15_18 | 〃 | 〃 | deliver_item(item_1) | 124 to 216 | ac_activation raised coffee_break ordinary | 171 (47) | 171 (47) | 171 (47) | 171 (47) | - | - | - | - |
| s15_18 | 〃 | 〃 | deliver_item(item_4) | 217 to 308 | ac_activation raised coffee_break ordinary | 262 (45) | 256 (39) | 262 (45) | 256 (39) | - | - | - | - |
| s15_19 | none | tk1/s15_10 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_19 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | ac_activation ordinary coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s15_19 | 〃 | 〃 | deliver_item(item_1) | 124 to 216 | ac_activation ordinary coffee_break ordinary | 171 (47) | 162 (38) | 171 (47) | 162 (38) | - | - | - | - |
| s15_19 | 〃 | 〃 | ac_activation(ac_switch_0) | 217 to 263 | ordinary | never | never | never | never | - | - | 0.7487 at 261 | 0.0574 at 261 |
| s15_19 | 〃 | 〃 | deliver_item(item_4) | 264 to 321 | ac_activation suppressed coffee_break ordinary | 279 (15) | 264 (0) | 279 (15) | 264 (0) | - | - | - | - |
| s15_20 | break_time 178 to 300; room_warm 150 to end | tk1/s15_10 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_20 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | ac_activation ordinary coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s15_20 | 〃 | 〃 | deliver_item(item_1) | 124 to 216 | ac_activation ordinary coffee_break ordinary | 171 (47) | 171 (47) | 171 (47) | 171 (47) | - | - | - | - |
| s15_20 | 〃 | 〃 | ac_activation(ac_switch_0) | 217 to 263 | raised | never | never | never | never | - | - | 0.7487 at 261 | 0.5932 at 261 |
| s15_20 | 〃 | 〃 | deliver_item(item_4) | 264 to 321 | ac_activation suppressed coffee_break raised | 279 (15) | 283 (19) | 279 (15) | 283 (19) | - | - | - | - |
| s15_21 | break_time 307 to end | off/s15_21 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_21 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | ac_activation ordinary coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s15_21 | 〃 | 〃 | deliver_item(item_1) | 124 to 216 | ac_activation ordinary coffee_break ordinary | 171 (47) | 162 (38) | 171 (47) | 162 (38) | - | - | - | - |
| s15_21 | 〃 | 〃 | deliver_item(item_4) | 217 to 308 | ac_activation ordinary coffee_break ordinary | 262 (45) | 217 (0) | 262 (45) | 217 (0) | - | - | - | - |
| s15_21 | 〃 | 〃 | coffee_break(coffee_machine_0) | 309 to 381 | raised | 334 (25) | 309 (0) | 334 (25) | 309 (0) | - | - | - | - |

Admissions of a hypothesis that is not the true task (every tick, the unmodelled ones included), off and on.

| scenario | side | hypothesis admitted | ticks | true task on those ticks | how it ends |
|---|---|---|---|---|---|
| s13_01 | off | coffee_break(coffee_machine_0) | 309 to 330 | unmodelled | retraction at 331 (none(leader_inadequate)) |
| s13_01 | on | coffee_break(coffee_machine_0) | 309 to 330 | unmodelled | retraction at 331 (none(leader_inadequate)) |
| s13_02 | off | coffee_break(coffee_machine_0) | 378 to 399 | unmodelled | retraction at 400 (none(leader_inadequate)) |
| s13_02 | on | coffee_break(coffee_machine_0) | 378 to 399 | unmodelled | retraction at 400 (none(leader_inadequate)) |
| s13_03 | off | coffee_break(coffee_machine_0) | 372 to 393 | unmodelled | retraction at 394 (none(leader_inadequate)) |
| s13_03 | on | deliver_item(item_4) | 150 to 161 | coffee_break(coffee_machine_0) | retraction at 162 (none(below_theta)) |
| s13_03 | on | deliver_item(item_4) | 279 | deliver_item(item_1) (complete: pinned) | the human starts it at 280 |
| s13_03 | on | coffee_break(coffee_machine_0) | 372 to 393 | unmodelled | retraction at 394 (none(leader_inadequate)) |
| s13_04 | off | deliver_item(item_4) | 289 | coffee_break(coffee_machine_0) (complete: pinned) | the human starts it at 290 |
| s13_04 | off | coffee_break(coffee_machine_0) | 357 to 378 | unmodelled | retraction at 379 (none(leader_inadequate)) |
| s13_04 | on | deliver_item(item_4) | 289 | coffee_break(coffee_machine_0) (complete: pinned) | the human starts it at 290 |
| s13_04 | on | coffee_break(coffee_machine_0) | 357 to 378 | unmodelled | retraction at 379 (none(leader_inadequate)) |
| s13_05 | off | coffee_break(coffee_machine_0) | 384 to 405 | unmodelled | retraction at 406 (none(leader_inadequate)) |
| s13_05 | on | deliver_item(item_2) | 94 | coffee_break(coffee_machine_0) | retraction at 95 (none(leader_no_observation)) |
| s13_05 | on | deliver_item(item_2) | 96 to 99 | coffee_break(coffee_machine_0) | retraction at 100 (none(below_theta)) |
| s13_05 | on | coffee_break(coffee_machine_0) | 384 to 405 | unmodelled | retraction at 406 (none(leader_inadequate)) |
| s13_06 | off | coffee_break(coffee_machine_0) | 379 to 400 | unmodelled | retraction at 401 (none(leader_inadequate)) |
| s13_06 | on | deliver_item(item_2) | 96 to 103 | coffee_break(coffee_machine_0) | retraction at 104 (none(below_theta)) |
| s13_06 | on | coffee_break(coffee_machine_0) | 379 to 400 | unmodelled | retraction at 401 (none(leader_inadequate)) |
| s13_07 | off | deliver_item(item_2) | 123 to 130 | coffee_break(coffee_machine_0) | retraction at 131 (none(leader_inadequate)) |
| s13_07 | off | coffee_break(coffee_machine_0) | 429 to 451 | unmodelled | retraction at 452 (none(leader_inadequate)) |
| s13_07 | on | deliver_item(item_2) | 123 to 130 | coffee_break(coffee_machine_0) | retraction at 131 (none(leader_inadequate)) |
| s13_07 | on | deliver_item(item_4) | 334 | deliver_item(item_1) (complete: pinned) | the human starts it at 335 |
| s13_07 | on | coffee_break(coffee_machine_0) | 429 to 451 | unmodelled | retraction at 452 (none(leader_inadequate)) |
| s13_08 | off | coffee_break(coffee_machine_0) | 378 to 399 | unmodelled | retraction at 400 (none(leader_inadequate)) |
| s13_08 | on | deliver_item(item_4) | 285 | deliver_item(item_1) (complete: pinned) | the human starts it at 286 |
| s13_08 | on | coffee_break(coffee_machine_0) | 378 to 399 | unmodelled | retraction at 400 (none(leader_inadequate)) |
| s13_09 | off | coffee_break(coffee_machine_0) | 378 to 399 | unmodelled | retraction at 400 (none(leader_inadequate)) |
| s13_09 | on | deliver_item(item_4) | 285 | deliver_item(item_1) (complete: pinned) | the human starts it at 286 |
| s13_09 | on | coffee_break(coffee_machine_0) | 378 to 399 | unmodelled | retraction at 400 (none(leader_inadequate)) |
| s13_10 | off | coffee_break(coffee_machine_0) | 378 to 399 | unmodelled | retraction at 400 (none(leader_inadequate)) |
| s13_10 | on | deliver_item(item_4) | 285 | deliver_item(item_1) (complete: pinned) | the human starts it at 286 |
| s13_10 | on | coffee_break(coffee_machine_0) | 378 to 399 | unmodelled | retraction at 400 (none(leader_inadequate)) |
| s13_11 | off | coffee_break(coffee_machine_0) | 372 to 393 | unmodelled | retraction at 394 (none(leader_inadequate)) |
| s13_11 | on | coffee_break(coffee_machine_0) | 81 to 91 | deliver_item(item_2) | retraction at 92 (none(below_theta)) |
| s13_11 | on | deliver_item(item_4) | 279 | deliver_item(item_1) (complete: pinned) | the human starts it at 280 |
| s13_11 | on | coffee_break(coffee_machine_0) | 372 to 393 | unmodelled | retraction at 394 (none(leader_inadequate)) |
| s13_12 | off | coffee_break(coffee_machine_0) | 372 to 393 | unmodelled | retraction at 394 (none(leader_inadequate)) |
| s13_12 | on | coffee_break(coffee_machine_0) | 81 to 91 | deliver_item(item_2) | retraction at 92 (none(below_theta)) |
| s13_12 | on | deliver_item(item_4) | 150 to 161 | coffee_break(coffee_machine_0) | retraction at 162 (none(below_theta)) |
| s13_12 | on | deliver_item(item_4) | 279 | deliver_item(item_1) (complete: pinned) | the human starts it at 280 |
| s13_12 | on | coffee_break(coffee_machine_0) | 372 to 393 | unmodelled | retraction at 394 (none(leader_inadequate)) |
| s13_13 | off | deliver_item(item_4) | 289 | coffee_break(coffee_machine_0) (complete: pinned) | the human starts it at 290 |
| s13_13 | off | coffee_break(coffee_machine_0) | 357 to 378 | unmodelled | retraction at 379 (none(leader_inadequate)) |
| s13_13 | on | deliver_item(item_4) | 216 to 258 | deliver_item(item_1) (complete: pinned), coffee_break(coffee_machine_0) | retraction at 259 (none(leader_inadequate)) |
| s13_13 | on | deliver_item(item_4) | 289 | coffee_break(coffee_machine_0) (complete: pinned) | the human starts it at 290 |
| s13_13 | on | coffee_break(coffee_machine_0) | 357 to 378 | unmodelled | retraction at 379 (none(leader_inadequate)) |
| s13_14 | off | coffee_break(coffee_machine_0) | 309 to 330 | unmodelled | retraction at 331 (none(leader_inadequate)) |
| s13_14 | on | coffee_break(coffee_machine_0) | 81 to 91 | deliver_item(item_2) | retraction at 92 (none(below_theta)) |
| s13_14 | on | coffee_break(coffee_machine_0) | 309 to 330 | unmodelled | retraction at 331 (none(leader_inadequate)) |
| s13_15 | off | deliver_item(item_4) | 262 to 268 | coffee_break(coffee_machine_0) | retraction at 269 (none(below_theta)) |
| s13_15 | off | deliver_item(item_4) | 309 | coffee_break(coffee_machine_0) (complete: pinned) | the human starts it at 310 |
| s13_15 | off | coffee_break(coffee_machine_0) | 376 to 397 | unmodelled | retraction at 398 (none(leader_inadequate)) |
| s13_15 | on | deliver_item(item_4) | 216 | deliver_item(item_1) (complete: pinned) | the human starts it at 217 |
| s13_15 | on | deliver_item(item_4) | 262 to 269 | coffee_break(coffee_machine_0) | retraction at 270 (none(leader_inadequate)) |
| s13_15 | on | deliver_item(item_4) | 309 | coffee_break(coffee_machine_0) (complete: pinned) | the human starts it at 310 |
| s13_15 | on | coffee_break(coffee_machine_0) | 376 to 397 | unmodelled | retraction at 398 (none(leader_inadequate)) |
| s14_01 | off | none | - | - | - |
| s14_01 | on | none | - | - | - |
| s14_02 | off | none | - | - | - |
| s14_02 | on | deliver_item(item_1) | 225 | deliver_item(item_2) (complete: pinned) | the human starts it at 226 |
| s14_03 | off | none | - | - | - |
| s14_03 | on | deliver_item(item_1) | 259 | coffee_break(coffee_machine_0) (complete: pinned) | the human starts it at 260 |
| s14_04 | off | none | - | - | - |
| s14_04 | on | deliver_item(item_2) | 133 | coffee_break(coffee_machine_0) | retraction at 134 (none(leader_no_observation)) |
| s14_04 | on | deliver_item(item_2) | 135 to 136 | coffee_break(coffee_machine_0) | retraction at 137 (none(below_theta)) |
| s14_04 | on | deliver_item(item_1) | 233 | deliver_item(item_2) (complete: pinned) | the human starts it at 234 |
| s14_05 | off | none | - | - | - |
| s14_05 | on | deliver_item(item_2) | 135 to 146 | coffee_break(coffee_machine_0) | retraction at 147 (none(leader_inadequate)) |
| s14_05 | on | deliver_item(item_1) | 226 | deliver_item(item_2) (complete: pinned) | the human starts it at 227 |
| s14_06 | off | deliver_item(item_2) | 180 to 187 | coffee_break(coffee_machine_0) | retraction at 188 (none(leader_inadequate)) |
| s14_06 | on | deliver_item(item_2) | 180 to 187 | coffee_break(coffee_machine_0) | retraction at 188 (none(leader_inadequate)) |
| s14_06 | on | deliver_item(item_1) | 307 | deliver_item(item_2) (complete: pinned) | the human starts it at 308 |
| s14_07 | off | none | - | - | - |
| s14_07 | on | deliver_item(item_1) | 192 | deliver_item(item_2) (complete: pinned) | the human starts it at 193 |
| s14_08 | off | none | - | - | - |
| s14_08 | on | deliver_item(item_1) | 229 | ac_activation(ac_switch_0) (complete: pinned) | the human starts it at 230 |
| s14_09 | off | none | - | - | - |
| s14_09 | on | deliver_item(item_2) | 133 | ac_activation(ac_switch_0) | retraction at 134 (none(leader_no_observation)) |
| s14_09 | on | deliver_item(item_2) | 135 to 136 | ac_activation(ac_switch_0) | retraction at 137 (none(below_theta)) |
| s14_09 | on | deliver_item(item_1) | 194 | deliver_item(item_2) (complete: pinned) | the human starts it at 195 |
| s14_10 | off | none | - | - | - |
| s14_10 | on | deliver_item(item_2) | 135 to 140 | ac_activation(ac_switch_0) | retraction at 141 (none(below_theta)) |
| s14_10 | on | deliver_item(item_1) | 191 | deliver_item(item_2) (complete: pinned) | the human starts it at 192 |
| s14_11 | off | deliver_item(item_2) | 180 to 187 | ac_activation(ac_switch_0) | retraction at 188 (none(leader_inadequate)) |
| s14_11 | on | deliver_item(item_2) | 180 to 187 | ac_activation(ac_switch_0) | retraction at 188 (none(leader_inadequate)) |
| s14_11 | on | deliver_item(item_1) | 276 | deliver_item(item_2) (complete: pinned) | the human starts it at 277 |
| s14_12 | off | none | - | - | - |
| s14_12 | on | deliver_item(item_1) | 225 | deliver_item(item_2) (complete: pinned) | the human starts it at 226 |
| s14_13 | off | none | - | - | - |
| s14_13 | on | deliver_item(item_1) | 225 | deliver_item(item_2) (complete: pinned) | the human starts it at 226 |
| s14_14 | off | none | - | - | - |
| s14_14 | on | deliver_item(item_1) | 225 | deliver_item(item_2) (complete: pinned) | the human starts it at 226 |
| s14_15 | off | none | - | - | - |
| s14_15 | on | deliver_item(item_1) | 192 | deliver_item(item_2) (complete: pinned) | the human starts it at 193 |
| s14_16 | off | none | - | - | - |
| s14_16 | on | deliver_item(item_1) | 192 | deliver_item(item_2) (complete: pinned) | the human starts it at 193 |
| s14_17 | off | none | - | - | - |
| s14_17 | on | deliver_item(item_1) | 192 | deliver_item(item_2) (complete: pinned) | the human starts it at 193 |
| s14_18 | off | none | - | - | - |
| s14_18 | on | deliver_item(item_1) | 259 | coffee_break(coffee_machine_0) (complete: pinned) | the human starts it at 260 |
| s14_19 | off | none | - | - | - |
| s14_19 | on | deliver_item(item_1) | 180 to 239 | deliver_item(item_2) (complete: pinned), coffee_break(coffee_machine_0) | retraction at 240 (none(below_theta)) |
| s14_19 | on | deliver_item(item_1) | 259 | coffee_break(coffee_machine_0) (complete: pinned) | the human starts it at 260 |
| s14_20 | off | none | - | - | - |
| s14_20 | on | none | - | - | - |
| s14_21 | off | none | - | - | - |
| s14_21 | on | coffee_break(coffee_machine_0) | 221 to 227 | ac_activation(ac_switch_0) | retraction at 228 (none(below_theta)) |
| s15_01 | off | coffee_break(coffee_machine_0) | 319 to 330 | unmodelled | retraction at 331 (none(leader_inadequate)) |
| s15_01 | on | coffee_break(coffee_machine_0) | 319 to 330 | unmodelled | retraction at 331 (none(leader_inadequate)) |
| s15_02 | off | coffee_break(coffee_machine_0) | 388 to 399 | unmodelled | retraction at 400 (none(leader_inadequate)) |
| s15_02 | on | coffee_break(coffee_machine_0) | 388 to 399 | unmodelled | retraction at 400 (none(leader_inadequate)) |
| s15_03 | off | coffee_break(coffee_machine_0) | 382 to 393 | unmodelled | retraction at 394 (none(leader_inadequate)) |
| s15_03 | on | deliver_item(item_4) | 151 to 161 | coffee_break(coffee_machine_0) | retraction at 162 (none(below_theta)) |
| s15_03 | on | deliver_item(item_4) | 279 | deliver_item(item_1) (complete: pinned) | the human starts it at 280 |
| s15_03 | on | coffee_break(coffee_machine_0) | 382 to 393 | unmodelled | retraction at 394 (none(leader_inadequate)) |
| s15_04 | off | coffee_break(coffee_machine_0) | 367 to 378 | unmodelled | retraction at 379 (none(leader_inadequate)) |
| s15_04 | on | deliver_item(item_4) | 289 | coffee_break(coffee_machine_0) (complete: pinned) | the human starts it at 290 |
| s15_04 | on | coffee_break(coffee_machine_0) | 378 | unmodelled | retraction at 379 (none(leader_inadequate)) |
| s15_05 | off | coffee_break(coffee_machine_0) | 394 to 405 | unmodelled | retraction at 406 (none(leader_inadequate)) |
| s15_05 | on | deliver_item(item_2) | 94 | coffee_break(coffee_machine_0) | retraction at 95 (none(leader_no_observation)) |
| s15_05 | on | deliver_item(item_2) | 96 to 99 | coffee_break(coffee_machine_0) | retraction at 100 (none(below_theta)) |
| s15_05 | on | coffee_break(coffee_machine_0) | 394 to 405 | unmodelled | retraction at 406 (none(leader_inadequate)) |
| s15_06 | off | coffee_break(coffee_machine_0) | 389 to 400 | unmodelled | retraction at 401 (none(leader_inadequate)) |
| s15_06 | on | deliver_item(item_2) | 96 to 103 | coffee_break(coffee_machine_0) | retraction at 104 (none(below_theta)) |
| s15_06 | on | coffee_break(coffee_machine_0) | 389 to 400 | unmodelled | retraction at 401 (none(leader_inadequate)) |
| s15_07 | off | deliver_item(item_2) | 123 to 130 | coffee_break(coffee_machine_0) | retraction at 131 (none(leader_inadequate)) |
| s15_07 | off | coffee_break(coffee_machine_0) | 440 to 451 | unmodelled | retraction at 452 (none(leader_inadequate)) |
| s15_07 | on | deliver_item(item_2) | 123 to 130 | coffee_break(coffee_machine_0) | retraction at 131 (none(leader_inadequate)) |
| s15_07 | on | deliver_item(item_4) | 334 | deliver_item(item_1) (complete: pinned) | the human starts it at 335 |
| s15_07 | on | coffee_break(coffee_machine_0) | 440 to 451 | unmodelled | retraction at 452 (none(leader_inadequate)) |
| s15_08 | off | coffee_break(coffee_machine_0) | 379 to 390 | unmodelled | retraction at 391 (none(leader_inadequate)) |
| s15_08 | on | deliver_item(item_4) | 276 | deliver_item(item_1) (complete: pinned) | the human starts it at 277 |
| s15_08 | on | coffee_break(coffee_machine_0) | 369 to 390 | unmodelled | retraction at 391 (none(leader_inadequate)) |
| s15_09 | off | coffee_break(coffee_machine_0) | 335 to 346 | unmodelled | retraction at 347 (none(leader_inadequate)) |
| s15_09 | on | deliver_item(item_4) | 229 | deliver_item(item_1) (complete: pinned) | the human starts it at 230 |
| s15_09 | on | coffee_break(coffee_machine_0) | 324 to 346 | unmodelled | retraction at 347 (none(leader_inadequate)) |
| s15_10 | off | coffee_break(coffee_machine_0) | 333 to 344 | unmodelled | retraction at 345 (none(leader_inadequate)) |
| s15_10 | on | deliver_item(item_4) | 263 | ac_activation(ac_switch_0) (complete: pinned) | the human starts it at 264 |
| s15_10 | on | coffee_break(coffee_machine_0) | 322 to 344 | unmodelled | retraction at 345 (none(leader_inadequate)) |
| s15_11 | off | coffee_break(coffee_machine_0) | 399 to 410 | unmodelled | retraction at 411 (none(leader_inadequate)) |
| s15_11 | on | deliver_item(item_2) | 94 | ac_activation(ac_switch_0) | retraction at 95 (none(leader_no_observation)) |
| s15_11 | on | deliver_item(item_2) | 96 to 98 | ac_activation(ac_switch_0) | retraction at 99 (none(below_theta)) |
| s15_11 | on | deliver_item(item_4) | 111 to 118 | ac_activation(ac_switch_0) | retraction at 119 (none(leader_inadequate)) |
| s15_11 | on | deliver_item(item_4) | 296 | deliver_item(item_1) (complete: pinned) | the human starts it at 297 |
| s15_11 | on | coffee_break(coffee_machine_0) | 389 to 410 | unmodelled | retraction at 411 (none(leader_inadequate)) |
| s15_12 | off | coffee_break(coffee_machine_0) | 383 to 394 | unmodelled | retraction at 395 (none(leader_inadequate)) |
| s15_12 | on | deliver_item(item_2) | 96 to 108 | ac_activation(ac_switch_0) | retraction at 109 (none(leader_inadequate)) |
| s15_12 | on | deliver_item(item_4) | 278 | deliver_item(item_1) (complete: pinned) | the human starts it at 279 |
| s15_12 | on | coffee_break(coffee_machine_0) | 373 to 394 | unmodelled | retraction at 395 (none(leader_inadequate)) |
| s15_13 | off | deliver_item(item_2) | 123 to 130 | ac_activation(ac_switch_0) | retraction at 131 (none(leader_inadequate)) |
| s15_13 | off | coffee_break(coffee_machine_0) | 411 to 422 | unmodelled | retraction at 423 (none(leader_inadequate)) |
| s15_13 | on | deliver_item(item_2) | 123 to 130 | ac_activation(ac_switch_0) | retraction at 131 (none(leader_inadequate)) |
| s15_13 | on | deliver_item(item_4) | 308 | deliver_item(item_1) (complete: pinned) | the human starts it at 309 |
| s15_13 | on | coffee_break(coffee_machine_0) | 401 to 422 | unmodelled | retraction at 423 (none(leader_inadequate)) |
| s15_14 | off | coffee_break(coffee_machine_0) | 379 to 390 | unmodelled | retraction at 391 (none(leader_inadequate)) |
| s15_14 | on | deliver_item(item_4) | 276 | deliver_item(item_1) (complete: pinned) | the human starts it at 277 |
| s15_14 | on | coffee_break(coffee_machine_0) | 369 to 390 | unmodelled | retraction at 391 (none(leader_inadequate)) |
| s15_15 | off | coffee_break(coffee_machine_0) | 379 to 390 | unmodelled | retraction at 391 (none(leader_inadequate)) |
| s15_15 | on | deliver_item(item_4) | 276 | deliver_item(item_1) (complete: pinned) | the human starts it at 277 |
| s15_15 | on | coffee_break(coffee_machine_0) | 369 to 390 | unmodelled | retraction at 391 (none(leader_inadequate)) |
| s15_16 | off | coffee_break(coffee_machine_0) | 379 to 390 | unmodelled | retraction at 391 (none(leader_inadequate)) |
| s15_16 | on | deliver_item(item_4) | 276 | deliver_item(item_1) (complete: pinned) | the human starts it at 277 |
| s15_16 | on | coffee_break(coffee_machine_0) | 369 to 390 | unmodelled | retraction at 391 (none(leader_inadequate)) |
| s15_17 | off | coffee_break(coffee_machine_0) | 367 to 378 | unmodelled | retraction at 379 (none(leader_inadequate)) |
| s15_17 | on | none | - | - | - |
| s15_18 | off | coffee_break(coffee_machine_0) | 319 to 330 | unmodelled | retraction at 331 (none(leader_inadequate)) |
| s15_18 | on | none | - | - | - |
| s15_19 | off | coffee_break(coffee_machine_0) | 333 to 344 | unmodelled | retraction at 345 (none(leader_inadequate)) |
| s15_19 | on | deliver_item(item_4) | 216 to 261 | deliver_item(item_1) (complete: pinned), ac_activation(ac_switch_0) | retraction at 262 (none(leader_no_observation)) |
| s15_19 | on | deliver_item(item_4) | 263 | ac_activation(ac_switch_0) (complete: pinned) | the human starts it at 264 |
| s15_19 | on | coffee_break(coffee_machine_0) | 322 to 344 | unmodelled | retraction at 345 (none(leader_inadequate)) |
| s15_20 | off | coffee_break(coffee_machine_0) | 333 to 344 | unmodelled | retraction at 345 (none(leader_inadequate)) |
| s15_20 | on | coffee_break(coffee_machine_0) | 322 to 344 | unmodelled | retraction at 345 (none(leader_inadequate)) |
| s15_21 | off | none | - | - | - |
| s15_21 | on | deliver_item(item_4) | 216 | deliver_item(item_1) (complete: pinned) | the human starts it at 217 |

## Stage 3: the runs (4 October 2026)

Results: `REPORT.md`. 0 disagreements at 1e-9 against actual.csv in all 59; the expectations unchanged by the runs. Runs
(git-ignored; md5s at the runs):

```
1332a62912c4549ca97e63403f19a28e  runs/env_layout_15_scenario_s13_01_on.log
2e5f17a2e3ec6b785af34000363452c6  runs/env_layout_15_scenario_s13_02_on.log
2667a3bbe4033a11e03d40578b35d416  runs/env_layout_15_scenario_s13_03_on.log
3c9019d7aa7a49ec24e9b85ea557957d  runs/env_layout_15_scenario_s13_04_on.log
e6dcb4022ba88cc49046dbb0a17013ee  runs/env_layout_15_scenario_s13_05_on.log
51fca3d91c65a3dfb11df472c2aec91c  runs/env_layout_15_scenario_s13_06_on.log
65895cfaf5885650af1d96636fb5f65f  runs/env_layout_15_scenario_s13_07_on.log
908457f2238562b2fb8851bcb04a973c  runs/env_layout_15_scenario_s13_08_on.log
19b4bae7d95a7002fbc3ac8bb37eaed6  runs/env_layout_15_scenario_s13_09_on.log
3b3f0fc3f3b0f6019e2b6cdb0d1be38e  runs/env_layout_15_scenario_s13_10_on.log
2a9c6f95f3ab0985afc6331c9e0adf94  runs/env_layout_15_scenario_s13_11_on.log
a966afc85ff5b4f95e769f76b9bb506b  runs/env_layout_15_scenario_s13_12_on.log
35f42f055212a4330c29ae97b3aa273f  runs/env_layout_15_scenario_s13_13_on.log
e6f4839bba1b6ff9d85354bb470e099a  runs/env_layout_15_scenario_s13_14_on.log
12e1192e0dbb5dc6efb560f66fef5ac0  runs/env_layout_15_scenario_s13_15_on.log
b80ab43af7d0ee20cd5b85d950b47900  runs/env_layout_16_scenario_s14_01_on.log
202d0a5fe84a9c5358b2fa2c5c624f81  runs/env_layout_16_scenario_s14_02_on.log
4c2e0e470e85b47f4b66c1ff047f0459  runs/env_layout_16_scenario_s14_03_on.log
7aad48556dab1f42ad1f15615b91ed86  runs/env_layout_16_scenario_s14_04_on.log
db84f37d50280c32b8f803bae91ffc73  runs/env_layout_16_scenario_s14_05_on.log
2a4f43cf7a8af3edfda1acbdfcaa78d4  runs/env_layout_16_scenario_s14_06_on.log
2ecdb4f137fff80ab6aede25574cb866  runs/env_layout_16_scenario_s14_07_on.log
06afd943e88bdec3e8844c4b32bc6439  runs/env_layout_16_scenario_s14_08_on.log
1d9109491b5ed96a3f170e3545a2979e  runs/env_layout_16_scenario_s14_09_on.log
c11191812910ae487b7d28ef9c3f3a44  runs/env_layout_16_scenario_s14_10_on.log
30bad2a0927350a82b5119378d26ea5a  runs/env_layout_16_scenario_s14_11_on.log
ff418725cc1eb9a0d92ab913cec1596f  runs/env_layout_16_scenario_s14_12_on.log
882138855effbb173162a7f84264f6cc  runs/env_layout_16_scenario_s14_13_on.log
30efb5d86c5d2265f2a2461a6a43b719  runs/env_layout_16_scenario_s14_14_on.log
4b3413d12136c312d1ef8a93263059a7  runs/env_layout_16_scenario_s14_15_on.log
04419fb367cf744d7b49eaa773e9fe9f  runs/env_layout_16_scenario_s14_16_on.log
e4166e697af8c357379c9adec46d1fbd  runs/env_layout_16_scenario_s14_17_on.log
5b28d2022a8d058b55b5891234f0cbcc  runs/env_layout_16_scenario_s14_18_on.log
b6ab160c7ea139f5697800480544cf83  runs/env_layout_16_scenario_s14_19_on.log
2defeb87b957e49ae7948077297ee52e  runs/env_layout_16_scenario_s14_20_on.log
5a32d39f01d83b3cf6900659e7888639  runs/env_layout_16_scenario_s14_21_on.log
b6441532e43a396679a6cd212667d380  runs/env_layout_17_scenario_s15_01_on.log
d911a43695c32b933b792bd8c9e0949b  runs/env_layout_17_scenario_s15_02_on.log
c6610c86fa0279d888688ebb2858e595  runs/env_layout_17_scenario_s15_03_on.log
6c04b4219cf901b2dbfb8ed87bbd5770  runs/env_layout_17_scenario_s15_04_on.log
e93d78641c8fb82120bcb15ccfd546a8  runs/env_layout_17_scenario_s15_05_on.log
da2bf02a0890cb29feb732a0c409d755  runs/env_layout_17_scenario_s15_06_on.log
f7c10bba6e3f0e996ef315f7ac5fa0e1  runs/env_layout_17_scenario_s15_07_on.log
0ea96748ee3872afd296be8a757df7f9  runs/env_layout_17_scenario_s15_08_on.log
613d4843d5573594addf97b3afa628cc  runs/env_layout_17_scenario_s15_09_on.log
6d21ffc36ebc4acf451f52ad551ef0f9  runs/env_layout_17_scenario_s15_10_on.log
78f0bb0234d3b994d7c44bde033429d3  runs/env_layout_17_scenario_s15_11_on.log
33ebd31defe3ea17211df53f6b727995  runs/env_layout_17_scenario_s15_12_on.log
e47e68a1cb26ee71d3be70e69aa165bc  runs/env_layout_17_scenario_s15_13_on.log
dc615567a2e2733116d5554d17bd676a  runs/env_layout_17_scenario_s15_14_on.log
a8faeff6cf7cbc2db458b97d6cfa7b32  runs/env_layout_17_scenario_s15_15_on.log
36928d650500239c989e04962e879f69  runs/env_layout_17_scenario_s15_16_on.log
df3358f0e64e9f7fb5aa45700d3581c5  runs/env_layout_17_scenario_s15_17_on.log
9ff8c692e28279aa1d5bcc97e2d5cca5  runs/env_layout_17_scenario_s15_18_on.log
395558cb1a1c65d81b0717b8e7df61c1  runs/env_layout_17_scenario_s15_19_on.log
c137fb0c5ef3f716674684f28e856467  runs/env_layout_17_scenario_s15_20_on.log
efeec48efa467392f99c62e808513334  runs/env_layout_17_scenario_s15_21_on.log
e478e3955464c5da8e4483fb6a58801a  runs/env_layout_15_scenario_s13_01_on.rec
6756b6ac7ee181c819ce54c78ae73aba  runs/env_layout_15_scenario_s13_02_on.rec
6c2ee6a1b45e58bfd0c76b83d7275cd6  runs/env_layout_15_scenario_s13_03_on.rec
08fbfda9fa0a03fb33c96c9b8c9a63ad  runs/env_layout_15_scenario_s13_04_on.rec
726dd2b9a82635f2139aed1d8b5970c3  runs/env_layout_15_scenario_s13_05_on.rec
c537966a26ce76c9537c0e9e4ba8df11  runs/env_layout_15_scenario_s13_06_on.rec
f759306928400bdc9427ba0569c11433  runs/env_layout_15_scenario_s13_07_on.rec
6756b6ac7ee181c819ce54c78ae73aba  runs/env_layout_15_scenario_s13_08_on.rec
6756b6ac7ee181c819ce54c78ae73aba  runs/env_layout_15_scenario_s13_09_on.rec
6756b6ac7ee181c819ce54c78ae73aba  runs/env_layout_15_scenario_s13_10_on.rec
6c2ee6a1b45e58bfd0c76b83d7275cd6  runs/env_layout_15_scenario_s13_11_on.rec
6c2ee6a1b45e58bfd0c76b83d7275cd6  runs/env_layout_15_scenario_s13_12_on.rec
08fbfda9fa0a03fb33c96c9b8c9a63ad  runs/env_layout_15_scenario_s13_13_on.rec
e478e3955464c5da8e4483fb6a58801a  runs/env_layout_15_scenario_s13_14_on.rec
d845aa4ac311b344cdaed07c5c3ea626  runs/env_layout_15_scenario_s13_15_on.rec
962e436075b7c3f9f555445c944b8bff  runs/env_layout_16_scenario_s14_01_on.rec
c2d2afc42bf1c9e6a69f104ccd364765  runs/env_layout_16_scenario_s14_02_on.rec
1d8302b47da19e51d38441c3e6beb23b  runs/env_layout_16_scenario_s14_03_on.rec
99a4a214e4681eb7483925ca5e9d78b1  runs/env_layout_16_scenario_s14_04_on.rec
c6a4c9bfd459f09856302fc32ce8c301  runs/env_layout_16_scenario_s14_05_on.rec
40ce5a270689411dd5ad07819564fbe1  runs/env_layout_16_scenario_s14_06_on.rec
ac459e141d935406a26e730d5aacf887  runs/env_layout_16_scenario_s14_07_on.rec
4fc04cbdedc31350db303be82bd79e22  runs/env_layout_16_scenario_s14_08_on.rec
0ed61d1b9861e0190690aa25d9284d51  runs/env_layout_16_scenario_s14_09_on.rec
6ce37100f6281b2b4458faef05e0c77c  runs/env_layout_16_scenario_s14_10_on.rec
349ccc75b98e2268d47524c50015acf9  runs/env_layout_16_scenario_s14_11_on.rec
c2d2afc42bf1c9e6a69f104ccd364765  runs/env_layout_16_scenario_s14_12_on.rec
c2d2afc42bf1c9e6a69f104ccd364765  runs/env_layout_16_scenario_s14_13_on.rec
c2d2afc42bf1c9e6a69f104ccd364765  runs/env_layout_16_scenario_s14_14_on.rec
ac459e141d935406a26e730d5aacf887  runs/env_layout_16_scenario_s14_15_on.rec
ac459e141d935406a26e730d5aacf887  runs/env_layout_16_scenario_s14_16_on.rec
ac459e141d935406a26e730d5aacf887  runs/env_layout_16_scenario_s14_17_on.rec
1d8302b47da19e51d38441c3e6beb23b  runs/env_layout_16_scenario_s14_18_on.rec
1d8302b47da19e51d38441c3e6beb23b  runs/env_layout_16_scenario_s14_19_on.rec
962e436075b7c3f9f555445c944b8bff  runs/env_layout_16_scenario_s14_20_on.rec
4fc04cbdedc31350db303be82bd79e22  runs/env_layout_16_scenario_s14_21_on.rec
e478e3955464c5da8e4483fb6a58801a  runs/env_layout_17_scenario_s15_01_on.rec
6756b6ac7ee181c819ce54c78ae73aba  runs/env_layout_17_scenario_s15_02_on.rec
6c2ee6a1b45e58bfd0c76b83d7275cd6  runs/env_layout_17_scenario_s15_03_on.rec
08fbfda9fa0a03fb33c96c9b8c9a63ad  runs/env_layout_17_scenario_s15_04_on.rec
726dd2b9a82635f2139aed1d8b5970c3  runs/env_layout_17_scenario_s15_05_on.rec
c537966a26ce76c9537c0e9e4ba8df11  runs/env_layout_17_scenario_s15_06_on.rec
f759306928400bdc9427ba0569c11433  runs/env_layout_17_scenario_s15_07_on.rec
ffdd1b085c77ac1b2b700883047d44b7  runs/env_layout_17_scenario_s15_08_on.rec
10badc90f3949849526a162004929f47  runs/env_layout_17_scenario_s15_09_on.rec
15542ad2f74ae4201ca81b0365d5ad64  runs/env_layout_17_scenario_s15_10_on.rec
4241f5198f6729e2e13c1b358b3bac80  runs/env_layout_17_scenario_s15_11_on.rec
3839d3ec27e8f1e28ac7a66fedf87b81  runs/env_layout_17_scenario_s15_12_on.rec
36343581ab71fd1cc3b2a5f428df326c  runs/env_layout_17_scenario_s15_13_on.rec
ffdd1b085c77ac1b2b700883047d44b7  runs/env_layout_17_scenario_s15_14_on.rec
ffdd1b085c77ac1b2b700883047d44b7  runs/env_layout_17_scenario_s15_15_on.rec
ffdd1b085c77ac1b2b700883047d44b7  runs/env_layout_17_scenario_s15_16_on.rec
08fbfda9fa0a03fb33c96c9b8c9a63ad  runs/env_layout_17_scenario_s15_17_on.rec
e478e3955464c5da8e4483fb6a58801a  runs/env_layout_17_scenario_s15_18_on.rec
15542ad2f74ae4201ca81b0365d5ad64  runs/env_layout_17_scenario_s15_19_on.rec
15542ad2f74ae4201ca81b0365d5ad64  runs/env_layout_17_scenario_s15_20_on.rec
018c8fdb1002afd33140d34a41cf6976  runs/env_layout_17_scenario_s15_21_on.rec
65ae7d56cd2f05051e1e7c995e41b70c  off/runs/env_layout_15_scenario_s13_15_on.log
1f91828daef19729c15b643925ba59cc  off/runs/env_layout_17_scenario_s15_21_on.log
d845aa4ac311b344cdaed07c5c3ea626  off/runs/env_layout_15_scenario_s13_15_on.rec
018c8fdb1002afd33140d34a41cf6976  off/runs/env_layout_17_scenario_s15_21_on.rec
```

## Step 5d: the expectations after the gate change (5 October 2026, committed before the runs)

The oracle after the gate's build (8357b74: the rank column, D3; observation warrant at admission, AM67;
none(leader_outranked) last, AM68 and D1) recomputes every table; the trajectories are byte-identical to stage 1's
(the human's script is open-loop). Commands as above, with --expect. The runs follow in the next commit; the reading:
analysis/kitting/mpb/tk5b/COMPARISON_5d.md.

    b38f1255fee1d911866cc68242436c49  off/scenario_s13_15/expected.csv
    0510a802c36d152ba1da9b534cd7e172  off/scenario_s15_21/expected.csv
    ec675353cf8d6c058cfd3e443c385f72  scenario_s13_01/expected.csv
    bed98ee107ef5b26f7d4e303b876488c  scenario_s13_02/expected.csv
    3574539b0b250ce1fb93f8dd8c52e455  scenario_s13_03/expected.csv
    1ec6dfc32eb2de72d1e6920d9be96e7b  scenario_s13_04/expected.csv
    7b7d4e8265a4b17e6e07c3531e685db2  scenario_s13_05/expected.csv
    6e380a5416b96a393faacda1d8c96126  scenario_s13_06/expected.csv
    900a1e59e75e1b6cae3453962288dde0  scenario_s13_07/expected.csv
    83709aa5013b26073f63a8692eac2d7e  scenario_s13_08/expected.csv
    c75ff9cb68604032a66d96bc5f93a3ba  scenario_s13_09/expected.csv
    6bc77e038b64206a19ed1cdc3eada044  scenario_s13_10/expected.csv
    bfa30198ce148930d7455c8f332857a0  scenario_s13_11/expected.csv
    ffee99ce2125674ae5d140848ebefdf4  scenario_s13_12/expected.csv
    35eda0cdfacf251bd09d1a0b5a548890  scenario_s13_13/expected.csv
    277f41096d228399c378e3417bc0e544  scenario_s13_14/expected.csv
    6c7993edeedcb980effe6d3c4cb2bc18  scenario_s13_15/expected.csv
    551fb8c4a1d31b4936f052f09d752bce  scenario_s14_01/expected.csv
    4d944d1d67f38c716458e00d6c64e345  scenario_s14_02/expected.csv
    61b54072f121b109707d2d5de39a0849  scenario_s14_03/expected.csv
    90ac72af11d432007b15d3ec5e1c20d4  scenario_s14_04/expected.csv
    299f6c45c518291c428b4ed667a08c79  scenario_s14_05/expected.csv
    107fffe1f43bcf40e0c287b43d4d904a  scenario_s14_06/expected.csv
    d24d25bd08da872d417d62af8147c1d0  scenario_s14_07/expected.csv
    d9fb2b6318627f6dcaded59f3ed7981c  scenario_s14_08/expected.csv
    aeb59f248d4b226998bf8537b3e83c9f  scenario_s14_09/expected.csv
    48ae05f83292b75d1e10de23cab56cfe  scenario_s14_10/expected.csv
    c5b615c778d94fcf1a43e49823b95503  scenario_s14_11/expected.csv
    961dc01b11ad32a0f153992e330988a0  scenario_s14_12/expected.csv
    eed7ce31bca85cef4387535cc199bc5f  scenario_s14_13/expected.csv
    664837eadd23665622ef479a69881f04  scenario_s14_14/expected.csv
    87783651ee07d200d792ad9dcd39ab6a  scenario_s14_15/expected.csv
    0c6d1da8012f50872f1c459843eb5f0b  scenario_s14_16/expected.csv
    0b5afbb340728fbb732663e1943f5ec0  scenario_s14_17/expected.csv
    ab80389fbb08963b51885a388f06d495  scenario_s14_18/expected.csv
    be30a70b602fd41ab0c97eadc8da7ea3  scenario_s14_19/expected.csv
    3ae8a46789e7f4477ac25de5f826c84f  scenario_s14_20/expected.csv
    1f41e0eb969edf7e1324f3c22cc7d63a  scenario_s14_21/expected.csv
    e5468f80ae42179af51b829cb2fadef2  scenario_s15_01/expected.csv
    b2760a333aea432c7fd55168d030c6c9  scenario_s15_02/expected.csv
    e0a89aa41f122b70950b81092cacb667  scenario_s15_03/expected.csv
    0f9de6f9df80967d52344d912ecdd583  scenario_s15_04/expected.csv
    7e7aad0b03cf827c13ecfb120d6bdfa3  scenario_s15_05/expected.csv
    7b4bcad5862310e81ae3d25b02d3b5c5  scenario_s15_06/expected.csv
    3d930c07df815a43562c397862e51bb7  scenario_s15_07/expected.csv
    d2bd699584c1875c72670ad4f3d0b85c  scenario_s15_08/expected.csv
    8b4549220f328144006d725881ffe7fa  scenario_s15_09/expected.csv
    14d5f584fc6af9880a4655b3d2abdf79  scenario_s15_10/expected.csv
    666d0f1f34a0011c1486a44a6f468155  scenario_s15_11/expected.csv
    ff37cd5c07447f0284fd2096d27bbd41  scenario_s15_12/expected.csv
    9a3c9f9fafe72b859526716a32b1e3fd  scenario_s15_13/expected.csv
    4a21d6a987dd81e2fd183d438fe6eec7  scenario_s15_14/expected.csv
    7eada06fe56192b43c6058b43caa9792  scenario_s15_15/expected.csv
    fe9b3e7c78b488e7ec026e94c6e41150  scenario_s15_16/expected.csv
    f034b9f365f2daffb071bb378d389cde  scenario_s15_17/expected.csv
    5c90a98673e95c2b5e80b65fef6e1373  scenario_s15_18/expected.csv
    bbed690df7fb3135285679e63ba6e7df  scenario_s15_19/expected.csv
    625fb17d60727f616a4c165c84ac4995  scenario_s15_20/expected.csv
    d7e95905606fce287acb7dade9de5d54  scenario_s15_21/expected.csv
