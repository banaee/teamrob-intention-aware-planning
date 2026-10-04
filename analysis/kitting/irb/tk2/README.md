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
