# T-K part 1, step 5e: context knowledge on kitting's rooms 02, 05, 06, 07 and the copies of 08 and 09

Written by ccode, 5 October 2026. Step 5e of T-K part 1 (named by Hadi after step 5d; docs/handoffs/T-G_forward_inputs.md, section 5's tree; design_records.md, "T-K", STEP 5E). Results: `REPORT.md` (written after the runs). This file: the set, the settings, the rules the authoring followed, the expectations (committed before any run) and the commands.

**The scenarios are authored.** Each was written to place a case; the counts of the report compare settings on the same scripts and are no rate of occurrence.

## What was ruled (Hadi, 5 October 2026)

- New files only: no existing layout, setup, scenario, test or output changed or deleted; no change to framework code, a strength or a ruled value. A behaviour the human model cannot express is left out and named.
- Rooms 02, 05, 06, 07: about 2 setups and 4 to 6 scenarios per setup; the existing scenarios on them that hold a measured script join as they are.
- Layouts 08 and 09 join as two new layouts, each a copy with one coffee machine added (no A/C switch), placed by a stated reason from the room's arrangement: env_layout_19 (env_layout_08's copy) and env_layout_20 (env_layout_09's). On them 3 or more setups and 10 or more scenarios per setup, each differing from the others in a stated respect.
- Settings: context knowledge off, and on with no timeline fact; a script with a foreseeable task also on with that task's raising fact over the ticks where the human does it (accord); a script with a delivery also on with a raising fact over a delivery (the human works through it). A window is a copy of the scenario with its own timeline.
- Each script once with the idle robot through the recognition test-bed (the IRB instrument and its oracle), once with a working robot through the planning test-bed (the MPB instrument and its oracle), the idle robot first; the oracles' expectations committed before the runs. Declared properties and coverage rows are not required.

## The set

- 105 scripts: 100 new, 5 existing (scenario_s02_01, s02_02, s04_01, s03_06, and the one script of s05_01 and s05_02, which differ in the robot's side only). The existing play scripts of these rooms ("not a measured fixture: nothing is recorded from it") do not join.
  - env_layout_02: 10 new scripts on env_setup_17, env_setup_18, plus 2 existing
  - env_layout_05: 10 new scripts on env_setup_19, env_setup_20, plus 1 existing
  - env_layout_06: 10 new scripts on env_setup_21, env_setup_22, plus 1 existing
  - env_layout_07: 10 new scripts on env_setup_23, env_setup_24, plus 1 existing
  - env_layout_19: 30 new scripts on env_setup_25, env_setup_26, env_setup_27
  - env_layout_20: 30 new scripts on env_setup_28, env_setup_29, env_setup_30
- 555 new scenario literals: per script the idle form (robot empty pool, observing) and the working form, each with no timeline and, where the script holds what it needs, as copies with their own timeline. An existing script's working form with no timeline is the existing scenario itself; its idle form and its copies are new, in the setup that repeats its shift (env_setup_17 = env_setup_02's items, _19 = _04's, _21 = _03's, _23 = _05's).
- Run files (configs/kitting/tk5e/): recognition 279 on + 105 off; planning 282 on + 106 off; 772 runs. Off runs only for the forms with no timeline (with context knowledge off the timeline acts on nothing).

### The two new rooms

- **env_layout_19** at (0, 450). Added in step 5e. Where it stands, and why: the north wall's middle. The shelves line the west, east and south walls and the two tables stand in the south-west and the east of the floor; the north wall between shelf_0 and shelf_3 is the one wall stretch with nothing against it, so a break corner there stays off the storage and the work, and its middle is about equally far from both tables. It stands on x = 0, the edge between zone_NW and zone_NE (the first declared, zone_NW, holds it; no kitting method reads an area). Placed from the room's arrangement, not for a recognizer result. From kitting_table_0: bearing 45.0 deg, 990 cm; from kitting_table_1: bearing 144.5 deg, 860 cm. Delivery walks: kitting_table_0 -> shelf_3: passes 395 cm from it, its heading 23.5 deg off the machine's bearing from kitting_table_0; kitting_table_1 -> shelf_0: passes 298 cm from it, its heading 20.3 deg off the machine's bearing from kitting_table_1; shelf_0 -> kitting_table_1: passes 298 cm from it, its heading 18.3 deg off the machine's bearing from shelf_0; shelf_2 -> kitting_table_1: passes 479 cm from it, its heading 27.1 deg off the machine's bearing from shelf_2; shelf_3 -> kitting_table_0: passes 395 cm from it, its heading 24.5 deg off the machine's bearing from shelf_3; shelf_5 -> kitting_table_0: passes 587 cm from it, its heading 34.0 deg off the machine's bearing from shelf_5; kitting_table_0 -> shelf_0: passes 905 cm from it, its heading 66.0 deg off the machine's bearing from kitting_table_0.
- **env_layout_20** at (125, 450). Added in step 5e. Where it stands, and why: the middle of the free stretch of the north wall, between kitting_table_0 (to x = -400) and shelf_3 (from x = 650). The tables stand against opposite walls and the storage along the side walls; a break corner against a wall beside a workplace, not on the open floor between the tables, and on the north wall rather than the south, where the door stands in the middle of the free stretch. Placed from the room's arrangement, not for a recognizer result. From kitting_table_0: bearing 0.0 deg, 625 cm; from kitting_table_1: bearing 112.6 deg, 975 cm. Delivery walks: kitting_table_0 -> shelf_3: passes 0 cm from it, its heading 0.0 deg off the machine's bearing from kitting_table_0; shelf_3 -> kitting_table_0: passes 0 cm from it, its heading 0.0 deg off the machine's bearing from shelf_3; kitting_table_1 -> shelf_2: passes 587 cm from it, its heading 37.0 deg off the machine's bearing from kitting_table_1; shelf_2 -> kitting_table_1: passes 587 cm from it, its heading 33.0 deg off the machine's bearing from shelf_2; kitting_table_1 -> shelf_3: passes 561 cm from it, its heading 35.1 deg off the machine's bearing from kitting_table_1; kitting_table_0 -> shelf_6: passes 625 cm from it, its heading 96.3 deg off the machine's bearing from kitting_table_0.

### The setups

- env_setup_17 (env_layout_02): env_setup_02's shift (item_k on shelf_k, all to kitting_table_0), so the measured scripts of env_layout_02 have their copies here. Items: item_0 (shelf_0 → T0), item_1 (shelf_1 → T0), item_2 (shelf_2 → T0), item_3 (shelf_3 → T0), item_4 (shelf_4 → T0), item_5 (shelf_5 → T0), item_6 (shelf_6 → T0), item_7 (shelf_7 → T0).
- env_setup_18 (env_layout_02): a second shift: the human's parts on the west and south shelves around the break corner (shelf_1 beside the coffee machine and the A/C switch), the robot's on the east and south-east shelves. Items: item_10 (shelf_1 → T0), item_11 (shelf_2 → T0), item_12 (shelf_6 → T0), item_13 (shelf_0 → T0), item_14 (shelf_3 → T0), item_15 (shelf_5 → T0), item_16 (shelf_4 → T0), item_17 (shelf_7 → T0).
- env_setup_19 (env_layout_05): env_setup_04's shift, so scenario_s04_01's script has its copies here. Items: item_3 (shelf_3 → T0), item_6 (shelf_6 → T0), item_4 (shelf_4 → T0), item_7 (shelf_7 → T0), item_5 (shelf_5 → T0).
- env_setup_20 (env_layout_05): a second shift: two parts on shelf_3 (one the human's, one the robot's), the human's others on the south-east and east shelves. Items: item_31 (shelf_3 → T0), item_32 (shelf_5 → T0), item_33 (shelf_6 → T0), item_34 (shelf_4 → T0), item_35 (shelf_7 → T0), item_36 (shelf_3 → T0).
- env_setup_21 (env_layout_06): env_setup_03's shift, so scenario_s03_06's script has its copies here. Items: item_4 (shelf_4 → T0), item_3 (shelf_3 → T0), item_6 (shelf_6 → T0), item_7 (shelf_7 → T0), item_2 (shelf_2 → T0).
- env_setup_22 (env_layout_06): a second shift: the human's parts on the east shelves (shelf_2, shelf_7) and shelf_6, the robot's on the two middle shelves. Items: item_41 (shelf_2 → T0), item_42 (shelf_7 → T0), item_43 (shelf_6 → T0), item_44 (shelf_4 → T0), item_45 (shelf_3 → T0).
- env_setup_23 (env_layout_07): env_setup_05's shift, so the script of scenario_s05_01 and scenario_s05_02 has its copies here. Items: item_1 (shelf_1 → T0), item_2 (shelf_2 → T0), item_3 (shelf_3 → T0), item_5 (shelf_5 → T0).
- env_setup_24 (env_layout_07): a second shift: the human's parts on shelf_1 (behind the coffee machine), shelf_5 (beside it) and shelf_3 (across the table); the robot's on shelf_2, shelf_3 and shelf_1. Items: item_51 (shelf_1 → T0), item_52 (shelf_5 → T0), item_53 (shelf_3 → T0), item_54 (shelf_2 → T0), item_55 (shelf_3 → T0), item_56 (shelf_1 → T0).
- env_setup_25 (env_layout_19): env_setup_06's shift (item_0, item_1, item_4, item_6 to kitting_table_0; item_3, item_7 to kitting_table_1) with item_2 and item_5 added, both to kitting_table_1. Items: item_0 (shelf_0 → T0), item_1 (shelf_1 → T0), item_2 (shelf_2 → T1), item_3 (shelf_3 → T1), item_4 (shelf_4 → T0), item_5 (shelf_5 → T1), item_6 (shelf_6 → T0), item_7 (shelf_7 → T1).
- env_setup_26 (env_layout_19): the cross shift: every part goes to the far table (the west and south-west shelves to kitting_table_1, the east and south-east shelves to kitting_table_0), so the carries cross the room's middle in front of the coffee machine. Items: item_20 (shelf_0 → T1), item_21 (shelf_1 → T1), item_22 (shelf_2 → T1), item_26 (shelf_6 → T1), item_23 (shelf_3 → T0), item_24 (shelf_4 → T0), item_25 (shelf_5 → T0), item_27 (shelf_7 → T0).
- env_setup_27 (env_layout_19): the near shift: every part goes to the near table (the west side to kitting_table_0, the east side to kitting_table_1); shelf_0 and shelf_3 hold two parts each. Items: item_30 (shelf_0 → T0), item_31 (shelf_1 → T0), item_32 (shelf_2 → T0), item_36 (shelf_6 → T0), item_33 (shelf_3 → T1), item_34 (shelf_4 → T1), item_35 (shelf_5 → T1), item_37 (shelf_7 → T1), item_38 (shelf_0 → T0), item_39 (shelf_3 → T1).
- env_setup_28 (env_layout_20): env_setup_07's shift with item_7 (shelf_3 to kitting_table_0, along the north wall past the coffee machine) and item_8 (shelf_6 to kitting_table_1) added. Items: item_1 (shelf_1 → T1), item_4 (shelf_4 → T1), item_5 (shelf_5 → T1), item_6 (shelf_6 → T0), item_2 (shelf_2 → T0), item_3 (shelf_3 → T1), item_7 (shelf_3 → T0), item_8 (shelf_6 → T1).
- env_setup_29 (env_layout_20): the cross shift: the north-west shelf_2 and the south-west shelf_6 to the south table, the others to the north table (shelf_3's carry along the north wall past the coffee machine). Items: item_61 (shelf_1 → T0), item_62 (shelf_2 → T1), item_63 (shelf_3 → T0), item_64 (shelf_4 → T0), item_65 (shelf_5 → T0), item_66 (shelf_6 → T1).
- env_setup_30 (env_layout_20): the near shift: the west shelves to the north table kitting_table_0, the east shelves to the south table kitting_table_1; shelf_2 and shelf_4 hold two parts each. Items: item_71 (shelf_1 → T0), item_72 (shelf_2 → T0), item_76 (shelf_6 → T0), item_73 (shelf_3 → T1), item_74 (shelf_4 → T1), item_75 (shelf_5 → T1), item_77 (shelf_2 → T0), item_78 (shelf_4 → T1).

### The rules of the authoring (ccode's; confirmed by Hadi, 5 October 2026)

- Every new script ends with the exit walk to a landmark (docs/assumptions.md 1.1); the human is assigned every delivery it performs (at its designated table) and every delivery it never starts. The disjointness rule of the planning sets: no item both in the robot's pool and among the human's assigned tasks (checked by the generator).
- The idle robot stands at one place per room, off the human's main walks: env_layout_02 (−100, −450), _05 (−700, 300), _06 (−550, 100), _07 (−700, 500), _19 (−400, 250), _20 (−900, 25).
- env_layout_08 declares one landmark, corner_SE, and its copy env_layout_19 adds only the coffee machine: there every walk elsewhere and every exit walk goes to corner_SE.
- Kinds of unmodelled behaviour used: a stand (20 to 60 ticks), a walk elsewhere (with or without a stand), a delivery abandoned before the grasp (`.at(move_to, drop, occurrence=0)`) or after it (`.at(pick_up, drop)`, the part kept in hand), a never-started delivery (assigned, not in the script), a delivery to the other table (the table bound to the other one). Every behaviour the prompt names was expressible; none was left out.
- Places of a foreseeable task: at the start, between deliveries, inside a delivery (before the grasp, after the grasp, or at the table before the release: `.at(move_to, X, occurrence=0)`, `.at(pick_up, X)`, `.at(move_to, X, occurrence=1)`), at the end; one or two per script.

### The windows (ccode's rules, confirmed by Hadi, 5 October 2026; placed from the instrument's replay before any run, never moved)

- accord: per foreseeable task, its raising fact (coffee_break: break_time; ac_activation: room_warm) on [the first tick the task is the top of the human's stack, the tick after its last such tick); one window per instance. A second coffee break gets its own window (its recency fact suppresses it regardless: suppression is asked first).
- through: break_time on the ticks of the first delivery the human performs at its designated table with no event inside it. break_time in every room: the coffee machine is the foreseeable task all six rooms share, and its raised strength (2) is the larger cost.
- through_rw: room_warm on the same ticks, for the deliveries-only scripts of the rooms with an A/C switch (02, 05, 07), so that the work-through cost of the A/C's raising fact is also measured.
- A script with no delivery performed at its table and no foreseeable task (scripts 074, 085) runs off and on only.

## The scripts

Per script: the room and setup; the idle form's id; the working form's id; the settings with their windows (half-open, in ticks; `bt` break_time, `rw` room_warm) as idle / working ids; the purpose; the aspects it varies; the expectation in kind (the full line per scenario is in its description).

| # | room, setup | idle | working | copies: setting idle / working (window) | purpose | aspects |
|---|---|---|---|---|---|---|
| 001 | 02, 17 | s17_01 | s02_01 | accord s17_02 / s17_03 (bt 77–155, rw 311–364); through s17_04 / s17_05 (bt 0–77) | scenario_s02_01's script as it is: a coffee break after the first delivery, the A/C activation after the second | foreseeable: between deliveries, two of two kinds; existing |
| 002 | 02, 17 | s17_06 | s02_02 | accord s17_07 / s17_08 (bt 33–77); through s17_09 / s17_10 (bt 126–251) | scenario_s02_02's script as it is: a coffee break inside the first delivery, after the grasp (T-C2c scenario A); no exit walk | foreseeable: inside a delivery; existing |
| 003 | 02, 17 | s17_11 | s17_12 | through s17_13 / s17_14 (bt 0–97); through_rw s17_15 / s17_16 (rw 0–97) | deliveries only: three deliveries from the east, west and east walls | deliveries: three, order east-west-east; start: south-east floor, first walk away from the break corner; robot: south-west start, the south and west shelves, crossing the human at the table |
| 004 | 02, 17 | s17_17 | s17_18 | accord s17_19 / s17_20 (bt 0–75); through s17_21 / s17_22 (bt 75–136) | a coffee break at the start, then two deliveries | foreseeable: at the start; start: floor centre, first walk toward the coffee machine; robot: east start, east shelves, its routes apart from the human's |
| 005 | 02, 17 | s17_23 | s17_24 | accord s17_25 / s17_26 (rw 74–126); through s17_27 / s17_28 (bt 0–74) | the A/C activation alone, between two deliveries | foreseeable: the A/C alone, between deliveries; start: beside the table; robot: south-east start, south and east shelves |
| 006 | 02, 17 | s17_29 | s17_30 | accord s17_31 / s17_32 (bt 38–78); through s17_33 / s17_34 (bt 129–248) | a coffee break inside a delivery whose approach heads toward the coffee machine: item_1 on shelf_1, 3.6 deg off the machine's bearing from the table | foreseeable: inside a delivery, after the grasp; approach toward the machine; robot: east, apart |
| 007 | 02, 17 | s17_35 | s17_36 | through s17_37 / s17_38 (bt 0–85); through_rw s17_39 / s17_40 (rw 0–85) | unmodelled alone: a stand of 20 ticks at the table after the one delivery, a second assigned delivery never started | unmodelled: a stand (20 ticks) and a never-started delivery; no foreseeable task |
| 008 | 02, 18 | s18_01 | s18_02 | through s18_03 / s18_04 (bt 0–113); through_rw s18_05 / s18_06 (rw 0–113) | deliveries only, the first one's approach heading toward the break corner (shelf_1 behind the coffee machine and the A/C switch) | deliveries: three, west and south; approach toward the machine and the switch; robot: east, apart |
| 009 | 02, 18 | s18_07 | s18_08 | accord s18_09 / s18_10 (bt 141–219); through s18_11 / s18_12 (bt 0–53) | a coffee break at the end, after two deliveries | foreseeable: at the end; start: west wall; robot: south-east start, east and south shelves |
| 010 | 02, 18 | s18_13 | s18_14 | accord s18_15 / s18_16 (bt 64–142, bt 211–289); through s18_17 / s18_18 (bt 0–64) | a second coffee break soon after the first (its recency fact holding) | foreseeable: two coffee breaks, between and at the end; robot: north-east start, apart |
| 011 | 02, 18 | s18_19 | s18_20 | accord s18_21 / s18_22 (bt 43–83); through s18_23 / s18_24 (bt 83–153) | unmodelled with a foreseeable task: a delivery abandoned at shelf_1 beside the coffee machine before the grasp, then a coffee break | unmodelled: an abandoned delivery (before the grasp); foreseeable: right after it, at the same corner |
| 012 | 02, 18 | s18_25 | s18_26 | through s18_27 / s18_28 (bt 0–79); through_rw s18_29 / s18_30 (rw 0–79) | unmodelled alone: a walk to the far corner and a stand of 30 ticks there between two deliveries | unmodelled: a walk elsewhere with a stand (30 ticks); robot: south-west start, crossing the human's walk to the corner |
| 013 | 05, 19 | s19_01 | s04_01 | accord s19_02 / s19_03 (bt 117–185, rw 185–207); through s19_04 / s19_05 (bt 0–117) | scenario_s04_01's script as it is: a coffee break, then the A/C activation on the line toward the next shelf | foreseeable: two of two kinds between deliveries; existing |
| 014 | 05, 19 | s19_06 | s19_07 | through s19_08 / s19_09 (bt 0–117); through_rw s19_10 / s19_11 (rw 0–117) | deliveries only: the two deliveries of scenario_s04_01 without its foreseeable tasks | deliveries: two; robot: scenario_s04_01's side |
| 015 | 05, 19 | s19_12 | s19_13 | accord s19_14 / s19_15 (rw 0–33); through s19_16 / s19_17 (bt 33–157) | the A/C activation alone, at the start | foreseeable: the A/C alone, at the start; start: east of the table, first walk south toward the switch |
| 016 | 05, 19 | s19_18 | s19_19 | accord s19_20 / s19_21 (bt 124–192); through s19_22 / s19_23 (bt 0–124) | a coffee break between deliveries | foreseeable: between deliveries; start: west floor; robot: north-east start, east shelves, crossing at the table |
| 017 | 05, 19 | s19_24 | s19_25 | accord s19_26 / s19_27 (rw 55–86); through s19_28 / s19_29 (bt 176–289) | the A/C activation inside a delivery: at shelf_6, before the grasp, the human walks back to the switch | foreseeable: the A/C inside a delivery, before the grasp |
| 018 | 05, 19 | s19_30 | s19_31 | accord s19_32 / s19_33 (bt 34–111) | unmodelled with a foreseeable task: a delivery abandoned after the grasp (the part still in hand), a coffee break, the second delivery never started | unmodelled: an abandoned delivery (after the grasp), a never-started delivery; foreseeable: after them |
| 019 | 05, 20 | s20_01 | s20_02 | through s20_03 / s20_04 (bt 0–109); through_rw s20_05 / s20_06 (rw 0–109) | deliveries only: three, the robot's first part on the human's first shelf | deliveries: three; robot: west start, its first part on the human's shelf_3, crossing |
| 020 | 05, 20 | s20_07 | s20_08 | accord s20_09 / s20_10 (bt 211–279); through s20_11 / s20_12 (bt 0–98) | a coffee break at the end | foreseeable: at the end; start: north-east; robot: south-west start |
| 021 | 05, 20 | s20_13 | s20_14 | accord s20_15 / s20_16 (bt 130–198, rw 198–220); through s20_17 / s20_18 (bt 0–130) | a coffee break and the A/C activation together between deliveries | foreseeable: two of two kinds in a row, between deliveries |
| 022 | 05, 20 | s20_19 | s20_20 | through s20_21 / s20_22 (bt 0–105); through_rw s20_23 / s20_24 (rw 0–105) | unmodelled alone: a stand of 30 ticks at the table between deliveries | unmodelled: a stand (30 ticks), between deliveries; robot: east start, its last part on the human's shelf_3 |
| 023 | 05, 20 | s20_25 | s20_26 | accord s20_27 / s20_28 (bt 190–268); through s20_29 / s20_30 (bt 0–98) | unmodelled with a foreseeable task: a walk to the south-west corner and a stand of 20 ticks, then a coffee break | unmodelled: a walk elsewhere with a stand (20 ticks); foreseeable: right after it |
| 024 | 06, 21 | s21_01 | s03_06 | accord s21_02 / s21_03 (bt 123–178); through s21_04 / s21_05 (bt 0–56) | scenario_s03_06's script as it is: a coffee break at the end, east of the table; no exit walk | foreseeable: at the end; existing |
| 025 | 06, 21 | s21_06 | s21_07 | through s21_08 / s21_09 (bt 0–56) | deliveries only: scenario_s03_06's two deliveries, then the exit walk | deliveries: two; robot: scenario_s03_06's side, crossing at shelf_3 and the table |
| 026 | 06, 21 | s21_10 | s21_11 | accord s21_12 / s21_13 (bt 0–43); through s21_14 / s21_15 (bt 43–121) | a coffee break at the start | foreseeable: at the start; start: east of the table, first walk toward the machine |
| 027 | 06, 21 | s21_16 | s21_17 | accord s21_18 / s21_19 (bt 14–70); through s21_20 / s21_21 (bt 97–162) | a coffee break inside a delivery, after the grasp: the carry diverted to the machine | foreseeable: inside a delivery, after the grasp |
| 028 | 06, 21 | s21_22 | s21_23 | accord s21_24 / s21_25 (bt 59–115); through s21_26 / s21_27 (bt 0–59) | a never-started delivery with a coffee break after the one delivery | unmodelled: a never-started delivery; foreseeable: between (the last delivery never comes) |
| 029 | 06, 21 | s21_28 | s21_29 | through s21_30 / s21_31 (bt 0–47) | unmodelled alone: a walk to corner_NE, 50 cm from the coffee machine, and a stand of 20 ticks there, which looks like a coffee break and is none | unmodelled: a walk elsewhere toward the machine with a stand (20 ticks) |
| 030 | 06, 22 | s22_01 | s22_02 | through s22_03 / s22_04 (bt 0–65) | deliveries only: three | deliveries: three, east, south-east, south-west; robot: south-west start, the middle shelves |
| 031 | 06, 22 | s22_05 | s22_06 | accord s22_07 / s22_08 (bt 97–152, bt 212–267); through s22_09 / s22_10 (bt 0–97) | a second coffee break soon after the first | foreseeable: two coffee breaks, between and at the end |
| 032 | 06, 22 | s22_11 | s22_12 | accord s22_13 / s22_14 (bt 23–113); through s22_15 / s22_16 (bt 113–173) | unmodelled with a foreseeable task: a delivery abandoned at shelf_6 before the grasp, then a coffee break | unmodelled: an abandoned delivery (before the grasp); foreseeable: right after; robot: south-east start |
| 033 | 06, 22 | s22_17 | s22_18 | accord s22_19 / s22_20 (bt 171–228); through s22_21 / s22_22 (bt 0–65) | a stand of 20 ticks at the table, then a coffee break at the end | unmodelled: a stand (20 ticks); foreseeable: at the end, right after it |
| 034 | 06, 22 | s22_23 | s22_24 | through s22_25 / s22_26 (bt 0–50) | deliveries only, the first approach heading toward the coffee machine: from the south-east, shelf_2 lies 7 deg off the machine's bearing | deliveries: two; start: south-east, first walk toward the machine; robot: north-west start |
| 035 | 07, 23 | s23_01 | s05_01, s05_02 | accord s23_02 / s23_03, s23_04 (bt 0–56, rw 96–143); through s23_05 / s23_06, s23_07 (bt 56–96) | the script of scenario_s05_01 and scenario_s05_02 as it is: a coffee break at the start, the delivery from the shelf beside the machine, the A/C activation at the end; no exit walk | foreseeable: at the start and at the end; existing (two robot sides) |
| 036 | 07, 23 | s23_08 | s23_09 | through s23_10 / s23_11 (bt 0–64); through_rw s23_12 / s23_13 (rw 0–64) | deliveries only: the first approach heads straight at the coffee machine (shelf_5 beside it) | deliveries: two; approach toward the machine; robot: scenario_s05_01's side, its first route past the machine |
| 037 | 07, 23 | s23_14 | s23_15 | accord s23_16 / s23_17 (rw 0–49); through s23_18 / s23_19 (bt 49–123) | the A/C activation alone, at the start | foreseeable: the A/C alone, at the start; start: north-east of the table |
| 038 | 07, 23 | s23_20 | s23_21 | accord s23_22 / s23_23 (bt 48–84); through s23_24 / s23_25 (bt 122–214) | a coffee break inside a delivery: at shelf_5 before the grasp, at the machine beside it | foreseeable: inside a delivery, before the grasp; approach toward the machine; robot: item_1 past the machine, crossing |
| 039 | 07, 23 | s23_26 | s23_27 | accord s23_28 / s23_29 (rw 54–138) | unmodelled with a foreseeable task: a delivery abandoned after the grasp, then the A/C activation; the second delivery never started | unmodelled: an abandoned delivery (after the grasp), a never-started delivery; foreseeable: the A/C after them |
| 040 | 07, 23 | s23_30 | s23_31 | through s23_32 / s23_33 (bt 0–95); through_rw s23_34 / s23_35 (rw 0–95) | unmodelled alone: a stand of 30 ticks at the table between deliveries | unmodelled: a stand (30 ticks), between deliveries |
| 041 | 07, 24 | s24_01 | s24_02 | through s24_03 / s24_04 (bt 0–94); through_rw s24_05 / s24_06 (rw 0–94) | deliveries only: the first walk passes the coffee machine to shelf_1 behind it | deliveries: two, south then north; approach toward the machine; robot: south-west start, crossing on the south route |
| 042 | 07, 24 | s24_07 | s24_08 | accord s24_09 / s24_10 (bt 147–207); through s24_11 / s24_12 (bt 0–83) | a coffee break at the end, after a delivery from the shelf beside the machine | foreseeable: at the end; robot: south-west start |
| 043 | 07, 24 | s24_13 | s24_14 | accord s24_15 / s24_16 (bt 0–51, bt 90–150); through s24_17 / s24_18 (bt 51–90) | a second coffee break soon after the first, at the start and after the first delivery | foreseeable: two coffee breaks, at the start and between |
| 044 | 07, 24 | s24_19 | s24_20 | through s24_21 / s24_22 (bt 0–88); through_rw s24_23 / s24_24 (rw 0–88) | unmodelled alone: a walk to the north-west corner and a stand of 20 ticks between deliveries | unmodelled: a walk elsewhere with a stand (20 ticks) |
| 045 | 07, 24 | s24_25 | s24_26 | accord s24_27 / s24_28 (bt 65–125, rw 125–162); through s24_29 / s24_30 (bt 0–65) | a coffee break and the A/C activation after the one delivery; the second delivery never started | unmodelled: a never-started delivery; foreseeable: two of two kinds, at the end |
| 046 | 19, 25 | s25_01 | s25_02 | through s25_03 / s25_04 (bt 0–61) | deliveries only: two, one to each table | deliveries: two, kitting_table_0 then kitting_table_1; start: west floor, first walk away from the machine; robot: south start, south shelves, both tables, crossing at kitting_table_0 |
| 047 | 19, 25 | s25_05 | s25_06 | through s25_07 / s25_08 (bt 0–28) | deliveries only: three, two to the east table, the last across to the west table | deliveries: three, kitting_table_1 twice then kitting_table_0; start: east floor; robot: south-west start, west shelves to kitting_table_0, crossing only at that table |
| 048 | 19, 25 | s25_09 | s25_10 | accord s25_11 / s25_12 (bt 0–60); through s25_13 / s25_14 (bt 60–145) | a coffee break at the start | foreseeable: at the start; start: floor centre, first walk toward the machine; deliveries: both tables; robot: south-east start |
| 049 | 19, 25 | s25_15 | s25_16 | accord s25_17 / s25_18 (bt 95–168); through s25_19 / s25_20 (bt 0–95) | a coffee break between two deliveries, the first a carry across the room | foreseeable: between deliveries; deliveries: kitting_table_1 then kitting_table_0; start: west; robot: north-east start, east shelves to kitting_table_1, crossing at it |
| 050 | 19, 25 | s25_21 | s25_22 | accord s25_23 / s25_24 (bt 32–110); through s25_25 / s25_26 (bt 154–276) | a coffee break inside a delivery after the grasp: from shelf_3 along the north wall to the machine | foreseeable: inside a delivery, after the grasp; start: east floor; robot: south, apart |
| 051 | 19, 25 | s25_27 | s25_28 | accord s25_29 / s25_30 (bt 56–136, bt 274–347); through s25_31 / s25_32 (bt 0–56) | a second coffee break soon after the first | foreseeable: two coffee breaks, between and at the end; deliveries: both tables |
| 052 | 19, 25 | s25_33 | s25_34 | accord s25_35 / s25_36 (bt 194–269); through s25_37 / s25_38 (bt 0–97) | a coffee break at the end | foreseeable: at the end; deliveries: kitting_table_0 (across) then kitting_table_1; robot: north-west start, item_2 across the room, crossing |
| 053 | 19, 25 | s25_39 | s25_40 | through s25_41 / s25_42 (bt 0–57) | unmodelled alone: a stand of 40 ticks at kitting_table_1 between deliveries | unmodelled: a stand (40 ticks), between deliveries; robot: south start, item_7 to kitting_table_1 while the human stands there |
| 054 | 19, 25 | s25_43 | s25_44 | accord s25_45 / s25_46 (bt 32–128); through s25_47 / s25_48 (bt 128–197) | unmodelled with a foreseeable task: a delivery abandoned at shelf_1 before the grasp, then a coffee break | unmodelled: an abandoned delivery (before the grasp); foreseeable: right after; robot: north-east start, to kitting_table_1 |
| 055 | 19, 25 | s25_49 | s25_50 | through s25_51 / s25_52 (bt 78–246) | unmodelled alone: a delivery to the other table (item_6 to kitting_table_1, designated kitting_table_0), and a never-started delivery | unmodelled: a delivery to the other table, a never-started delivery; robot: to kitting_table_1, where the human delivers twice |
| 056 | 19, 26 | s26_01 | s26_02 | through s26_03 / s26_04 (bt 0–114) | deliveries only: one long carry across the room, past the front of the coffee machine | deliveries: one, across; robot: south-centre start, two carries the other way, crossing in the middle |
| 057 | 19, 26 | s26_05 | s26_06 | through s26_07 / s26_08 (bt 0–136) | deliveries only: four, alternating tables | deliveries: four, alternating tables; robot: centre start, crossing |
| 058 | 19, 26 | s26_09 | s26_10 | accord s26_11 / s26_12 (bt 190–264); through s26_13 / s26_14 (bt 0–108) | a coffee break between deliveries, after the second | foreseeable: between, after two deliveries; start: south-east corner, first walk north |
| 059 | 19, 26 | s26_15 | s26_16 | accord s26_17 / s26_18 (bt 94–167); through s26_19 / s26_20 (bt 211–295) | a coffee break inside a delivery at the table, before the release (the part still in hand) | foreseeable: inside a delivery, before the release; robot: north-east start, crossing |
| 060 | 19, 26 | s26_21 | s26_22 | accord s26_23 / s26_24 (bt 0–54); through s26_25 / s26_26 (bt 54–198) | a coffee break at the start, the machine a short walk away | foreseeable: at the start; start: near the machine, a short first walk toward it |
| 061 | 19, 26 | s26_27 | s26_28 | through s26_29 / s26_30 (bt 0–71) | unmodelled alone: a walk to corner_SE and a stand of 20 ticks between deliveries | unmodelled: a walk elsewhere with a stand (20 ticks); start: south floor, first walk away from the machine |
| 062 | 19, 26 | s26_31 | s26_32 | accord s26_33 / s26_34 (bt 94–167); through s26_35 / s26_36 (bt 0–94) | a coffee break after the one delivery; the second delivery never started | unmodelled: a never-started delivery; foreseeable: at the end |
| 063 | 19, 26 | s26_37 | s26_38 | through s26_39 / s26_40 (bt 30–182) | unmodelled alone: a delivery abandoned after the grasp; the next delivery first returns the part to its shelf | unmodelled: an abandoned delivery (after the grasp) followed by a return; start: near the machine, first walk away |
| 064 | 19, 26 | s26_41 | s26_42 | accord s26_43 / s26_44 (bt 36–119); through s26_45 / s26_46 (bt 258–362) | a stand of 20 ticks at the start, then a coffee break inside a delivery before the grasp | unmodelled: a stand (20 ticks) at the start; foreseeable: inside a delivery, before the grasp |
| 065 | 19, 26 | s26_47 | s26_48 | accord s26_49 / s26_50 (bt 0–47, bt 287–367); through s26_51 / s26_52 (bt 47–183) | two coffee breaks, at the start and at the end, far apart | foreseeable: two, at the start and at the end; deliveries: two long carries |
| 066 | 19, 27 | s27_01 | s27_02 | through s27_03 / s27_04 (bt 0–63) | deliveries only: two parts from one shelf | deliveries: two from shelf_0 to kitting_table_0; start: west wall; robot: east, apart |
| 067 | 19, 27 | s27_05 | s27_06 | through s27_07 / s27_08 (bt 0–40) | deliveries only: three to the east table | deliveries: three to kitting_table_1; start: south-east corner; robot: west, apart |
| 068 | 19, 27 | s27_09 | s27_10 | through s27_11 / s27_12 (bt 0–50) | deliveries only: the walk from kitting_table_0 to shelf_3 heads toward the coffee machine | deliveries: three, both tables; approach toward the machine; robot: south start, crossing |
| 069 | 19, 27 | s27_13 | s27_14 | accord s27_15 / s27_16 (bt 44–124); through s27_17 / s27_18 (bt 0–44) | a coffee break between deliveries | foreseeable: between deliveries; start: north-west |
| 070 | 19, 27 | s27_19 | s27_20 | accord s27_21 / s27_22 (bt 38–116); through s27_23 / s27_24 (bt 192–296) | a coffee break inside a delivery, at shelf_3 before the grasp | foreseeable: inside a delivery, before the grasp |
| 071 | 19, 27 | s27_25 | s27_26 | through s27_27 / s27_28 (bt 0–44) | unmodelled alone: a long stand, 60 ticks, at kitting_table_1 | unmodelled: a stand (60 ticks), between deliveries |
| 072 | 19, 27 | s27_29 | s27_30 | accord s27_31 / s27_32 (bt 129–225); through s27_33 / s27_34 (bt 0–45) | unmodelled with a foreseeable task: a walk to corner_SE, then a coffee break | unmodelled: a walk elsewhere (no stand); foreseeable: right after it; robot: two parts from shelf_3 |
| 073 | 19, 27 | s27_35 | s27_36 | accord s27_37 / s27_38 (bt 103–184); through s27_39 / s27_40 (bt 63–103) | unmodelled with a foreseeable task: a delivery to the other table (item_37 to kitting_table_0), a coffee break at the end | unmodelled: a delivery to the other table; foreseeable: at the end; robot: two parts from shelf_0 to kitting_table_0, where the human delivers |
| 074 | 19, 27 | s27_41 | s27_42 | - | unmodelled alone: a delivery abandoned after the grasp, the part carried away to the corner; the second delivery never started | unmodelled: an abandoned delivery, a walk elsewhere, a never-started delivery; no foreseeable task |
| 075 | 19, 27 | s27_43 | s27_44 | accord s27_45 / s27_46 (bt 10–93, bt 192–266); through s27_47 / s27_48 (bt 137–192) | a coffee break inside a delivery after the grasp, and a second soon after at the end | foreseeable: two coffee breaks, inside a delivery and at the end |
| 076 | 20, 28 | s28_01 | s28_02 | through s28_03 / s28_04 (bt 0–35) | deliveries only: scenario_s07_01's two deliveries, then the exit walk | deliveries: two, kitting_table_0 then kitting_table_1; start: west, first walk away from the machine; robot: scenario_s07_01's side without item_6, crossing at kitting_table_1 |
| 077 | 20, 28 | s28_05 | s28_06 | through s28_07 / s28_08 (bt 0–123) | deliveries only: the walk from kitting_table_0 to shelf_3 along the north wall heads straight at the coffee machine | deliveries: two to kitting_table_0; approach toward the machine (the same bearing); robot: south-east, apart |
| 078 | 20, 28 | s28_09 | s28_10 | accord s28_11 / s28_12 (bt 0–54); through s28_13 / s28_14 (bt 54–132) | a coffee break at the start | foreseeable: at the start; start: by kitting_table_0, first walk east toward the machine; deliveries: both tables |
| 079 | 20, 28 | s28_15 | s28_16 | accord s28_17 / s28_18 (bt 58–120); through s28_19 / s28_20 (bt 0–58) | a coffee break between deliveries, the next delivery leaving from the machine | foreseeable: between deliveries; robot: centre start, item_1 across the room, crossing |
| 080 | 20, 28 | s28_21 | s28_22 | accord s28_23 / s28_24 (bt 25–84); through s28_25 / s28_26 (bt 134–243) | a coffee break inside a delivery after the grasp, at the machine along the wall from shelf_3 | foreseeable: inside a delivery, after the grasp |
| 081 | 20, 28 | s28_27 | s28_28 | accord s28_29 / s28_30 (bt 93–172) | a coffee break inside a delivery at the table before the release: from the south table back across the room to the machine | foreseeable: inside a delivery, before the release; deliveries: one; robot: to kitting_table_1, where the human's part waits in hand |
| 082 | 20, 28 | s28_31 | s28_32 | accord s28_33 / s28_34 (bt 35–115, bt 206–268); through s28_35 / s28_36 (bt 0–35) | a second coffee break soon after the first | foreseeable: two coffee breaks, between and at the end; deliveries: kitting_table_1 then kitting_table_0 |
| 083 | 20, 28 | s28_37 | s28_38 | through s28_39 / s28_40 (bt 41–99) | unmodelled alone: a stand of 40 ticks at the start, at kitting_table_1 | unmodelled: a stand (40 ticks) at the start; deliveries: two to kitting_table_1; robot: to kitting_table_0, apart |
| 084 | 20, 28 | s28_41 | s28_42 | accord s28_43 / s28_44 (bt 85–169); through s28_45 / s28_46 (bt 0–42) | unmodelled with a foreseeable task: a walk to corner_NW and a stand of 20 ticks, then a coffee break | unmodelled: a walk elsewhere with a stand (20 ticks); foreseeable: right after it |
| 085 | 20, 28 | s28_47 | s28_48 | - | unmodelled alone: a delivery to the other table (item_6 to kitting_table_1) and a never-started delivery | unmodelled: a delivery to the other table, a never-started delivery |
| 086 | 20, 29 | s29_01 | s29_02 | through s29_03 / s29_04 (bt 0–88) | deliveries only: one carry along the north wall past the coffee machine | deliveries: one; start: near the machine, first walk away from it; robot: west, apart |
| 087 | 20, 29 | s29_05 | s29_06 | through s29_07 / s29_08 (bt 0–108) | deliveries only: three, alternating tables | deliveries: three, alternating; robot: north-east start, to kitting_table_0, crossing |
| 088 | 20, 29 | s29_09 | s29_10 | accord s29_11 / s29_12 (bt 230–291); through s29_13 / s29_14 (bt 0–61) | a coffee break at the end, after two deliveries to the north table | foreseeable: at the end; start: west wall |
| 089 | 20, 29 | s29_15 | s29_16 | accord s29_17 / s29_18 (bt 89–168); through s29_19 / s29_20 (bt 0–89) | a coffee break between two deliveries to the south table | foreseeable: between deliveries; start: by the door, first walk west |
| 090 | 20, 29 | s29_21 | s29_22 | accord s29_23 / s29_24 (bt 18–98); through s29_25 / s29_26 (bt 228–323) | a coffee break inside a delivery, at shelf_4 before the grasp | foreseeable: inside a delivery, before the grasp; robot: west start, crossing |
| 091 | 20, 29 | s29_27 | s29_28 | accord s29_29 / s29_30 (bt 0–77); through s29_31 / s29_32 (bt 77–168) | a coffee break at the start, a long first walk toward the machine from the south table | foreseeable: at the start; start: kitting_table_1, the longest first walk toward the machine; deliveries: one, past the machine again |
| 092 | 20, 29 | s29_33 | s29_34 | accord s29_35 / s29_36 (bt 22–110); through s29_37 / s29_38 (bt 110–201) | unmodelled with a foreseeable task: a delivery abandoned at shelf_5 before the grasp, then a coffee break | unmodelled: an abandoned delivery (before the grasp); foreseeable: right after |
| 093 | 20, 29 | s29_39 | s29_40 | through s29_41 / s29_42 (bt 0–107) | unmodelled alone: a stand of 20 ticks at the south table, then a walk to corner_SE, before the next delivery | unmodelled: two in a row, a stand (20 ticks) and a walk elsewhere |
| 094 | 20, 29 | s29_43 | s29_44 | through s29_45 / s29_46 (bt 0–83) | unmodelled alone: a never-started delivery among two performed | unmodelled: a never-started delivery; deliveries: two, both tables |
| 095 | 20, 29 | s29_47 | s29_48 | accord s29_49 / s29_50 (bt 97–156) | unmodelled with a foreseeable task: a delivery to the other table (item_62 to kitting_table_0), then a coffee break inside the next delivery after the grasp | unmodelled: a delivery to the other table; foreseeable: inside the next delivery, after the grasp |
| 096 | 20, 30 | s30_01 | s30_02 | through s30_03 / s30_04 (bt 0–46) | deliveries only: two parts from one shelf to the north table | deliveries: two from shelf_2; robot: east, two parts from one shelf, apart |
| 097 | 20, 30 | s30_05 | s30_06 | through s30_07 / s30_08 (bt 0–97) | deliveries only: four, alternating tables | deliveries: four, alternating; start: by the door; robot: north-west start, crossing |
| 098 | 20, 30 | s30_09 | s30_10 | accord s30_11 / s30_12 (bt 0–60); through s30_13 / s30_14 (bt 60–140) | a coffee break at the start, the machine along the wall from kitting_table_0 | foreseeable: at the start; start: kitting_table_0, first walk toward the machine; deliveries: two to kitting_table_1 |
| 099 | 20, 30 | s30_15 | s30_16 | accord s30_17 / s30_18 (bt 56–119); through s30_19 / s30_20 (bt 0–56) | a coffee break between deliveries | foreseeable: between deliveries; start: south-west corner |
| 100 | 20, 30 | s30_21 | s30_22 | accord s30_23 / s30_24 (bt 25–113); through s30_25 / s30_26 (bt 146–194) | a coffee break inside a south-west delivery after the grasp | foreseeable: inside a delivery, after the grasp; robot: east, apart |
| 101 | 20, 30 | s30_27 | s30_28 | accord s30_29 / s30_30 (bt 0–45, bt 294–374); through s30_31 / s30_32 (bt 45–123) | two coffee breaks around three deliveries, at the start and at the end | foreseeable: two, at the start and at the end; deliveries: three, both tables |
| 102 | 20, 30 | s30_33 | s30_34 | through s30_35 / s30_36 (bt 0–48) | unmodelled alone: a long stand, 60 ticks, at kitting_table_1 | unmodelled: a stand (60 ticks), between deliveries |
| 103 | 20, 30 | s30_37 | s30_38 | through s30_39 / s30_40 (bt 0–66) | unmodelled alone: a walk to corner_SW and a stand of 40 ticks between deliveries | unmodelled: a walk elsewhere with a stand (40 ticks) |
| 104 | 20, 30 | s30_41 | s30_42 | accord s30_43 / s30_44 (bt 9–88) | unmodelled with a foreseeable task: a delivery abandoned after the grasp, a coffee break with the part in hand; the second delivery never started | unmodelled: an abandoned delivery (after the grasp), a never-started delivery; foreseeable: after them |
| 105 | 20, 30 | s30_45 | s30_46 | accord s30_47 / s30_48 (bt 188–251); through s30_49 / s30_50 (bt 93–188) | unmodelled with a foreseeable task: a delivery to the other table (item_75 to kitting_table_0), a coffee break at the end | unmodelled: a delivery to the other table; foreseeable: at the end; robot: to kitting_table_0, where the human delivers twice |

### The expectations in kind (one line per script and setting; written before the runs)

- 001: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); the A/C activation rarely admitted on or off; its belief at arrival lower on (ordinary 0.02 against the assigned tasks). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; the A/C activation's belief at arrival higher than with no fact (raised by room_warm); admission possible only where the movement evidence allows; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 002: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 003: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior). **through**: the delivery under break_time admitted later than with no fact, near off. **through_rw**: the delivery under room_warm admitted later than with no fact, by less than under break_time (raised 0.5 against 2).
- 004: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off; a delivery whose walk heads toward the machine may lose its admission to the raised coffee break.
- 005: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); the A/C activation rarely admitted on or off; its belief at arrival lower on (ordinary 0.02 against the assigned tasks). **accord**: the A/C activation's belief at arrival higher than with no fact (raised by room_warm); admission possible only where the movement evidence allows; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 006: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off; a delivery whose walk heads toward the machine may lose its admission to the raised coffee break.
- 007: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); the never-started delivery never admitted (no observation warrant); no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **through**: the delivery under break_time admitted later than with no fact, near off; the never-started delivery never admitted (no observation warrant); no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **through_rw**: the delivery under room_warm admitted later than with no fact, by less than under break_time (raised 0.5 against 2).
- 008: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior). **through**: the delivery under break_time admitted later than with no fact, near off; a delivery whose walk heads toward the machine may lose its admission to the raised coffee break. **through_rw**: the delivery under room_warm admitted later than with no fact, by less than under break_time (raised 0.5 against 2).
- 009: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 010: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); the second under its recency fact (suppressed), later still. **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; the second one suppressed by its recency fact, the window gives it nothing; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 011: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); the abandoned delivery admitted while the human walks to it, then retracted as the evidence turns. **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact; the abandoned delivery admitted while the human walks to it, then retracted as the evidence turns. **through**: the delivery under break_time admitted later than with no fact, near off; the abandoned delivery admitted while the human walks to it, then retracted as the evidence turns.
- 012: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **through**: the delivery under break_time admitted later than with no fact, near off; no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **through_rw**: the delivery under room_warm admitted later than with no fact, by less than under break_time (raised 0.5 against 2).
- 013: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); the A/C activation rarely admitted on or off; its belief at arrival lower on (ordinary 0.02 against the assigned tasks). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; the A/C activation's belief at arrival higher than with no fact (raised by room_warm); admission possible only where the movement evidence allows; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 014: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior). **through**: the delivery under break_time admitted later than with no fact, near off. **through_rw**: the delivery under room_warm admitted later than with no fact, by less than under break_time (raised 0.5 against 2).
- 015: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); the A/C activation rarely admitted on or off; its belief at arrival lower on (ordinary 0.02 against the assigned tasks). **accord**: the A/C activation's belief at arrival higher than with no fact (raised by room_warm); admission possible only where the movement evidence allows; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off; a delivery whose walk heads toward the machine may lose its admission to the raised coffee break.
- 016: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 017: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); the A/C activation rarely admitted on or off; its belief at arrival lower on (ordinary 0.02 against the assigned tasks). **accord**: the A/C activation's belief at arrival higher than with no fact (raised by room_warm); admission possible only where the movement evidence allows; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 018: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); the never-started delivery never admitted (no observation warrant); the abandoned delivery admitted while the human walks to it, then retracted as the evidence turns. **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact; the never-started delivery never admitted (no observation warrant); the abandoned delivery admitted while the human walks to it, then retracted as the evidence turns.
- 019: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior). **through**: the delivery under break_time admitted later than with no fact, near off. **through_rw**: the delivery under room_warm admitted later than with no fact, by less than under break_time (raised 0.5 against 2).
- 020: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 021: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); the A/C activation rarely admitted on or off; its belief at arrival lower on (ordinary 0.02 against the assigned tasks). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; the A/C activation's belief at arrival higher than with no fact (raised by room_warm); admission possible only where the movement evidence allows; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 022: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **through**: the delivery under break_time admitted later than with no fact, near off; no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **through_rw**: the delivery under room_warm admitted later than with no fact, by less than under break_time (raised 0.5 against 2).
- 023: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact; no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **through**: the delivery under break_time admitted later than with no fact, near off; no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk.
- 024: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 025: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior). **through**: the delivery under break_time admitted later than with no fact, near off.
- 026: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off; a delivery whose walk heads toward the machine may lose its admission to the raised coffee break.
- 027: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 028: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); the never-started delivery never admitted (no observation warrant). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact; the never-started delivery never admitted (no observation warrant). **through**: the delivery under break_time admitted later than with no fact, near off; the never-started delivery never admitted (no observation warrant).
- 029: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **through**: the delivery under break_time admitted later than with no fact, near off; a delivery whose walk heads toward the machine may lose its admission to the raised coffee break; no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk.
- 030: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior). **through**: the delivery under break_time admitted later than with no fact, near off.
- 031: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); the second under its recency fact (suppressed), later still. **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; the second one suppressed by its recency fact, the window gives it nothing; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 032: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); the abandoned delivery admitted while the human walks to it, then retracted as the evidence turns. **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact; the abandoned delivery admitted while the human walks to it, then retracted as the evidence turns. **through**: the delivery under break_time admitted later than with no fact, near off; the abandoned delivery admitted while the human walks to it, then retracted as the evidence turns.
- 033: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact; no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **through**: the delivery under break_time admitted later than with no fact, near off; no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk.
- 034: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior). **through**: the delivery under break_time admitted later than with no fact, near off; a delivery whose walk heads toward the machine may lose its admission to the raised coffee break.
- 035: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); the A/C activation rarely admitted on or off; its belief at arrival lower on (ordinary 0.02 against the assigned tasks). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; the A/C activation's belief at arrival higher than with no fact (raised by room_warm); admission possible only where the movement evidence allows; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 036: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior). **through**: the delivery under break_time admitted later than with no fact, near off; a delivery whose walk heads toward the machine may lose its admission to the raised coffee break. **through_rw**: the delivery under room_warm admitted later than with no fact, by less than under break_time (raised 0.5 against 2).
- 037: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); the A/C activation rarely admitted on or off; its belief at arrival lower on (ordinary 0.02 against the assigned tasks). **accord**: the A/C activation's belief at arrival higher than with no fact (raised by room_warm); admission possible only where the movement evidence allows; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 038: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off; a delivery whose walk heads toward the machine may lose its admission to the raised coffee break.
- 039: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); the A/C activation rarely admitted on or off; its belief at arrival lower on (ordinary 0.02 against the assigned tasks); the never-started delivery never admitted (no observation warrant); the abandoned delivery admitted while the human walks to it, then retracted as the evidence turns. **accord**: the A/C activation's belief at arrival higher than with no fact (raised by room_warm); admission possible only where the movement evidence allows; a delivery inside a window admitted later than with no fact; the never-started delivery never admitted (no observation warrant); the abandoned delivery admitted while the human walks to it, then retracted as the evidence turns.
- 040: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **through**: the delivery under break_time admitted later than with no fact, near off; no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **through_rw**: the delivery under room_warm admitted later than with no fact, by less than under break_time (raised 0.5 against 2).
- 041: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior). **through**: the delivery under break_time admitted later than with no fact, near off; a delivery whose walk heads toward the machine may lose its admission to the raised coffee break. **through_rw**: the delivery under room_warm admitted later than with no fact, by less than under break_time (raised 0.5 against 2).
- 042: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 043: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); the second under its recency fact (suppressed), later still. **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; the second one suppressed by its recency fact, the window gives it nothing; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 044: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **through**: the delivery under break_time admitted later than with no fact, near off; no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **through_rw**: the delivery under room_warm admitted later than with no fact, by less than under break_time (raised 0.5 against 2).
- 045: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); the A/C activation rarely admitted on or off; its belief at arrival lower on (ordinary 0.02 against the assigned tasks); the never-started delivery never admitted (no observation warrant). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; the A/C activation's belief at arrival higher than with no fact (raised by room_warm); admission possible only where the movement evidence allows; a delivery inside a window admitted later than with no fact; the never-started delivery never admitted (no observation warrant). **through**: the delivery under break_time admitted later than with no fact, near off; the never-started delivery never admitted (no observation warrant).
- 046: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior). **through**: the delivery under break_time admitted later than with no fact, near off.
- 047: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior). **through**: the delivery under break_time admitted later than with no fact, near off.
- 048: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off; a delivery whose walk heads toward the machine may lose its admission to the raised coffee break.
- 049: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 050: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 051: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); the second under its recency fact (suppressed), later still. **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; the second one suppressed by its recency fact, the window gives it nothing; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 052: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 053: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **through**: the delivery under break_time admitted later than with no fact, near off; no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk.
- 054: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); the abandoned delivery admitted while the human walks to it, then retracted as the evidence turns. **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact; the abandoned delivery admitted while the human walks to it, then retracted as the evidence turns. **through**: the delivery under break_time admitted later than with no fact, near off; the abandoned delivery admitted while the human walks to it, then retracted as the evidence turns.
- 055: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); the never-started delivery never admitted (no observation warrant); the delivery to the other table: admitted on the walk to the shelf, then its carry unexplained; no other hypothesis admitted there. **through**: the delivery under break_time admitted later than with no fact, near off; the never-started delivery never admitted (no observation warrant); the delivery to the other table: admitted on the walk to the shelf, then its carry unexplained; no other hypothesis admitted there.
- 056: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior). **through**: the delivery under break_time admitted later than with no fact, near off.
- 057: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior). **through**: the delivery under break_time admitted later than with no fact, near off.
- 058: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 059: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 060: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off; a delivery whose walk heads toward the machine may lose its admission to the raised coffee break.
- 061: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **through**: the delivery under break_time admitted later than with no fact, near off; no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk.
- 062: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); the never-started delivery never admitted (no observation warrant). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact; the never-started delivery never admitted (no observation warrant). **through**: the delivery under break_time admitted later than with no fact, near off; the never-started delivery never admitted (no observation warrant).
- 063: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); the abandoned delivery admitted while the human walks to it, then retracted as the evidence turns. **through**: the delivery under break_time admitted later than with no fact, near off; the abandoned delivery admitted while the human walks to it, then retracted as the evidence turns.
- 064: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact; no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **through**: the delivery under break_time admitted later than with no fact, near off; no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk.
- 065: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); the second under its recency fact (suppressed), later still. **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; the second one suppressed by its recency fact, the window gives it nothing; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 066: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior). **through**: the delivery under break_time admitted later than with no fact, near off.
- 067: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior). **through**: the delivery under break_time admitted later than with no fact, near off.
- 068: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior). **through**: the delivery under break_time admitted later than with no fact, near off; a delivery whose walk heads toward the machine may lose its admission to the raised coffee break.
- 069: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 070: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 071: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **through**: the delivery under break_time admitted later than with no fact, near off; no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk.
- 072: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact; no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **through**: the delivery under break_time admitted later than with no fact, near off; no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk.
- 073: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); the delivery to the other table: admitted on the walk to the shelf, then its carry unexplained; no other hypothesis admitted there. **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact; the delivery to the other table: admitted on the walk to the shelf, then its carry unexplained; no other hypothesis admitted there. **through**: the delivery under break_time admitted later than with no fact, near off; the delivery to the other table: admitted on the walk to the shelf, then its carry unexplained; no other hypothesis admitted there.
- 074: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); the never-started delivery never admitted (no observation warrant); the abandoned delivery admitted while the human walks to it, then retracted as the evidence turns.
- 075: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); the second under its recency fact (suppressed), later still. **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; the second one suppressed by its recency fact, the window gives it nothing; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 076: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior). **through**: the delivery under break_time admitted later than with no fact, near off.
- 077: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior). **through**: the delivery under break_time admitted later than with no fact, near off; a delivery whose walk heads toward the machine may lose its admission to the raised coffee break.
- 078: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off; a delivery whose walk heads toward the machine may lose its admission to the raised coffee break.
- 079: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 080: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 081: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact.
- 082: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); the second under its recency fact (suppressed), later still. **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; the second one suppressed by its recency fact, the window gives it nothing; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 083: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **through**: the delivery under break_time admitted later than with no fact, near off; no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk.
- 084: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact; no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **through**: the delivery under break_time admitted later than with no fact, near off; no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk.
- 085: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); the never-started delivery never admitted (no observation warrant); the delivery to the other table: admitted on the walk to the shelf, then its carry unexplained; no other hypothesis admitted there.
- 086: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior). **through**: the delivery under break_time admitted later than with no fact, near off.
- 087: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior). **through**: the delivery under break_time admitted later than with no fact, near off.
- 088: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 089: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 090: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 091: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off; a delivery whose walk heads toward the machine may lose its admission to the raised coffee break.
- 092: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); the abandoned delivery admitted while the human walks to it, then retracted as the evidence turns. **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact; the abandoned delivery admitted while the human walks to it, then retracted as the evidence turns. **through**: the delivery under break_time admitted later than with no fact, near off; the abandoned delivery admitted while the human walks to it, then retracted as the evidence turns.
- 093: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **through**: the delivery under break_time admitted later than with no fact, near off; no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk.
- 094: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); the never-started delivery never admitted (no observation warrant). **through**: the delivery under break_time admitted later than with no fact, near off; the never-started delivery never admitted (no observation warrant).
- 095: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); the delivery to the other table: admitted on the walk to the shelf, then its carry unexplained; no other hypothesis admitted there. **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact; the delivery to the other table: admitted on the walk to the shelf, then its carry unexplained; no other hypothesis admitted there.
- 096: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior). **through**: the delivery under break_time admitted later than with no fact, near off.
- 097: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior). **through**: the delivery under break_time admitted later than with no fact, near off.
- 098: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off; a delivery whose walk heads toward the machine may lose its admission to the raised coffee break.
- 099: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 100: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength). **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 101: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); the second under its recency fact (suppressed), later still. **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; the second one suppressed by its recency fact, the window gives it nothing; a delivery inside a window admitted later than with no fact. **through**: the delivery under break_time admitted later than with no fact, near off.
- 102: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **through**: the delivery under break_time admitted later than with no fact, near off; no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk.
- 103: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. **through**: the delivery under break_time admitted later than with no fact, near off; no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk.
- 104: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); the never-started delivery never admitted (no observation warrant); the abandoned delivery admitted while the human walks to it, then retracted as the evidence turns. **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact; the never-started delivery never admitted (no observation warrant); the abandoned delivery admitted while the human walks to it, then retracted as the evidence turns.
- 105: **base**: on against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength); the delivery to the other table: admitted on the walk to the shelf, then its carry unexplained; no other hypothesis admitted there. **accord**: the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted later than with no fact; the delivery to the other table: admitted on the walk to the shelf, then its carry unexplained; no other hypothesis admitted there. **through**: the delivery under break_time admitted later than with no fact, near off; the delivery to the other table: admitted on the walk to the shelf, then its carry unexplained; no other hypothesis admitted there.

## The commands

```bash
# expectations (before the runs): replay + oracle only
analysis/instruments/irb/run.sh kitting --expect -o analysis/kitting/tk5e/irb/on configs/kitting/tk5e/irb/on/<scenario>.yaml
analysis/instruments/irb/run.sh kitting --expect -o analysis/kitting/tk5e/irb/off configs/kitting/tk5e/irb/off/<scenario>.yaml
analysis/instruments/mpb/run.sh kitting --expect -o analysis/kitting/tk5e/mpb/on configs/kitting/tk5e/mpb/on/<scenario>.yaml
analysis/instruments/mpb/run.sh kitting --expect -o analysis/kitting/tk5e/mpb/off configs/kitting/tk5e/mpb/off/<scenario>.yaml
# the runs: the same without --expect (each run's own oracle call must reproduce the expectations)
```

The runs went through repository copies in parallel (run.sh picks the newest log of logs/, so one copy per worker), the outputs written to this folder (-o, absolute); every copy at the committed state.

## The expectations, committed before the runs (md5)

Per side, the md5 of each oracle table (`expected.csv` for the IRB, `expected_ticks.json` for the MPB), sorted by scenario.


### irb, on (279)

```
acbc59e1ace0a4eadc44fa931a500e00  irb/on/scenario_s17_01/expected.csv
7f3ed664832fae201947406a3e42cb59  irb/on/scenario_s17_02/expected.csv
698d8d754e759014b886614c812fcdb0  irb/on/scenario_s17_04/expected.csv
e2ec499c33c550b80e4ce53651de7fc5  irb/on/scenario_s17_06/expected.csv
dea5100bb84f328b35951d68c13720e8  irb/on/scenario_s17_07/expected.csv
aba07f4e7cef30a37ab4901e1c66eb13  irb/on/scenario_s17_09/expected.csv
aa5077515f9781561bdfab6e582280b6  irb/on/scenario_s17_11/expected.csv
c6ed989360e008ac69c122507000a10d  irb/on/scenario_s17_13/expected.csv
f826bf1ca05386a5b3992f2aabc62507  irb/on/scenario_s17_15/expected.csv
bbd7c70c3e4103ade16b9d32ded2c273  irb/on/scenario_s17_17/expected.csv
fda6080b8c4b62b0fbb8f033229ae26d  irb/on/scenario_s17_19/expected.csv
bbd7c70c3e4103ade16b9d32ded2c273  irb/on/scenario_s17_21/expected.csv
df430f5fd775f870f11c6005484308fb  irb/on/scenario_s17_23/expected.csv
920d2a277459c4d9aee94c3bce2d81c6  irb/on/scenario_s17_25/expected.csv
496cafc8307cb5bf8891957f61bada4c  irb/on/scenario_s17_27/expected.csv
05b027214b1548fa4423c9516af77ecf  irb/on/scenario_s17_29/expected.csv
3feb208793c475ba117ba7949f2e4293  irb/on/scenario_s17_31/expected.csv
940889c7259c7ebba2d7445b188cf530  irb/on/scenario_s17_33/expected.csv
a8cc9fa958e43e60ebf83944f454da49  irb/on/scenario_s17_35/expected.csv
7e385fadde9aeee84c906f662283cc94  irb/on/scenario_s17_37/expected.csv
ae86a1648572db677c7b3ef9f1804e26  irb/on/scenario_s17_39/expected.csv
165814d9793d04630cf8b33ead1cae53  irb/on/scenario_s18_01/expected.csv
f82b7f8121005f7e2048100e5645e493  irb/on/scenario_s18_03/expected.csv
3bd23f1dfec4f31d3567855107412476  irb/on/scenario_s18_05/expected.csv
f5ef01ee6a4b3e2af975adfb43f4bd59  irb/on/scenario_s18_07/expected.csv
c08242732be9fbbce2d79298bd218f2e  irb/on/scenario_s18_09/expected.csv
1042d6677554a0af7632f9a4e090404f  irb/on/scenario_s18_11/expected.csv
aba80a329b74edc67da4d0e926887ca9  irb/on/scenario_s18_13/expected.csv
a4375ba6568a5467541ae636df8ddcf4  irb/on/scenario_s18_15/expected.csv
706be87258ce734e60ae89a206898624  irb/on/scenario_s18_17/expected.csv
0b8cae304cde4937ff5ed8146c3937a3  irb/on/scenario_s18_19/expected.csv
853954cb98f5d03343befb7b9bf3f735  irb/on/scenario_s18_21/expected.csv
0b8cae304cde4937ff5ed8146c3937a3  irb/on/scenario_s18_23/expected.csv
1445710c3e6e868b7bf6dc1dd478797c  irb/on/scenario_s18_25/expected.csv
8b14ec45bf2c434ab25e74fb3d2b256f  irb/on/scenario_s18_27/expected.csv
05acf8f7a289fd53e1d2530402b185d4  irb/on/scenario_s18_29/expected.csv
1074c15082d300ba99feafcd41bfebd8  irb/on/scenario_s19_01/expected.csv
2f08c2a22f2688dbba2a9a132537b96e  irb/on/scenario_s19_02/expected.csv
3a4d84a3d15af7683f09d5560627be6f  irb/on/scenario_s19_04/expected.csv
84245459006505eabb108d46f584addb  irb/on/scenario_s19_06/expected.csv
03357bf4bec45901f79bbe9986e2422b  irb/on/scenario_s19_08/expected.csv
5118dd7629b7527e072bb47529151f55  irb/on/scenario_s19_10/expected.csv
8eb81d58339712f5c95ecf96558c4a49  irb/on/scenario_s19_12/expected.csv
255451ea03ab658e61c21b6b7963f87f  irb/on/scenario_s19_14/expected.csv
c01febb68881280d1a1db4e38c865c37  irb/on/scenario_s19_16/expected.csv
462fee7075cc8c3f3fc786f2fa900a9f  irb/on/scenario_s19_18/expected.csv
6f799ad2e47ff8db752760e27ea0e6e0  irb/on/scenario_s19_20/expected.csv
9064cbc97978dd8ff85d57e423a906a8  irb/on/scenario_s19_22/expected.csv
dfe55b5236fd4f52942672cfbeab533f  irb/on/scenario_s19_24/expected.csv
a320c7266c309762461a8436e34682a4  irb/on/scenario_s19_26/expected.csv
b67d40253861d3e7cc213be352c48830  irb/on/scenario_s19_28/expected.csv
1124c4212cfda31b7d20e11a826d5020  irb/on/scenario_s19_30/expected.csv
2451ad8aed363092d46b140d1c338fd8  irb/on/scenario_s19_32/expected.csv
da2d2126b1ab93f945685f113f6f08ec  irb/on/scenario_s20_01/expected.csv
0de95857cc7afb093d570e53b7a266f5  irb/on/scenario_s20_03/expected.csv
37036ea4957ecc85bbeaef99b17bf70d  irb/on/scenario_s20_05/expected.csv
78121ca0f117b85ed5a9860b044dfdff  irb/on/scenario_s20_07/expected.csv
a57a73fbe3703f505455365a475e0210  irb/on/scenario_s20_09/expected.csv
eef07fddf85dba4662f54f753c9878f3  irb/on/scenario_s20_11/expected.csv
2c6d262be8460f30d9215b3628c4e5fe  irb/on/scenario_s20_13/expected.csv
eae60a222e8dbf4a0cb8779c02e87c28  irb/on/scenario_s20_15/expected.csv
69a1f263113704c82db2e3ab5132c01c  irb/on/scenario_s20_17/expected.csv
527197500d832ce749b058756c67918e  irb/on/scenario_s20_19/expected.csv
0950c66c8b9acf7ce41ce9f768d20eea  irb/on/scenario_s20_21/expected.csv
63ecf1ac3efe2f650a964d5028979f9a  irb/on/scenario_s20_23/expected.csv
e341c4a70ee2934978895aaa0a4527c8  irb/on/scenario_s20_25/expected.csv
6d14cca3e269471752585a553897d8ea  irb/on/scenario_s20_27/expected.csv
7b43a5b31367d584c9249e86e8cc6fa0  irb/on/scenario_s20_29/expected.csv
9808461d62ebbd921314f2310accc24e  irb/on/scenario_s21_01/expected.csv
9e968d27c4f2b946e4f6052fd424cf01  irb/on/scenario_s21_02/expected.csv
836ad0dee99b9e58ab14d36b5217ccb0  irb/on/scenario_s21_04/expected.csv
ccc6c166d8d0af054bf38ea22329398f  irb/on/scenario_s21_06/expected.csv
ed60d2a0337c1c1a48464ec4b44d6bd5  irb/on/scenario_s21_08/expected.csv
27c811371d1c3579bf9a3e60c8a53719  irb/on/scenario_s21_10/expected.csv
cc39460d1d3da328825efdcf978b2aa2  irb/on/scenario_s21_12/expected.csv
27c811371d1c3579bf9a3e60c8a53719  irb/on/scenario_s21_14/expected.csv
8930acdbea74d18fa6ca5277ae102cdd  irb/on/scenario_s21_16/expected.csv
51ef57f4127437e8af934633d387acf3  irb/on/scenario_s21_18/expected.csv
dd9518d4c4b69acdb4a979ee1dee814d  irb/on/scenario_s21_20/expected.csv
7395a16afbdbce7e176ca98461ad3afb  irb/on/scenario_s21_22/expected.csv
5d03fc95b215b2d0a98dd96928704b27  irb/on/scenario_s21_24/expected.csv
3cf28e556d80a77e762257bc7a62d63b  irb/on/scenario_s21_26/expected.csv
392757b3814d1fbf12b22f640ed2ce9e  irb/on/scenario_s21_28/expected.csv
a928e839e6217425c0f16750f4c9d918  irb/on/scenario_s21_30/expected.csv
b2fd98d6700a261586967e582feee31b  irb/on/scenario_s22_01/expected.csv
182ecf3b8baf5ceaebeff9fda396773a  irb/on/scenario_s22_03/expected.csv
cf710196d04b4eb3139ee05f13846e7f  irb/on/scenario_s22_05/expected.csv
33e758b82ce11141abab81e341fe018f  irb/on/scenario_s22_07/expected.csv
c690297eb53cb96651ecf112b85fb4e5  irb/on/scenario_s22_09/expected.csv
b57157549d5f02e2234352d85af6a6a3  irb/on/scenario_s22_11/expected.csv
b54e36e7357ef8b5121b12cce64f98ea  irb/on/scenario_s22_13/expected.csv
b57157549d5f02e2234352d85af6a6a3  irb/on/scenario_s22_15/expected.csv
a0b713cc34234d2bad2ef50610bfabe9  irb/on/scenario_s22_17/expected.csv
8f223b4e7a19d33aaf5269f4f0006eef  irb/on/scenario_s22_19/expected.csv
0ee5ece595adbcac5129fea57f8a6c15  irb/on/scenario_s22_21/expected.csv
6b91948cb34d86abb8312c7613f821e7  irb/on/scenario_s22_23/expected.csv
bffc6472018c749863bdb364adc91388  irb/on/scenario_s22_25/expected.csv
543fbd86286aa647f9397d0c10cffb4b  irb/on/scenario_s23_01/expected.csv
ed8eb47f3ce2f5475dbeb01c5d7f06cb  irb/on/scenario_s23_02/expected.csv
543fbd86286aa647f9397d0c10cffb4b  irb/on/scenario_s23_05/expected.csv
d7d6a77a118946350dff8f35539639f4  irb/on/scenario_s23_08/expected.csv
bcc49921dbd69ca7a8227ff3f0cdc1ce  irb/on/scenario_s23_10/expected.csv
6eefbd9cb5e3e86c9e1fae9a99fa3a2b  irb/on/scenario_s23_12/expected.csv
d4f12cc3602131e0ad645adac9b5f61b  irb/on/scenario_s23_14/expected.csv
3bc357c88ae33529e137967ea7412f6f  irb/on/scenario_s23_16/expected.csv
dc2faef5717e2ba0cb0d00f91e3db497  irb/on/scenario_s23_18/expected.csv
6937d4a6fc35d867621844485d31d4ea  irb/on/scenario_s23_20/expected.csv
e12b556d68a8de268403eb96c18c6bfc  irb/on/scenario_s23_22/expected.csv
c216170bf0a653817542434aba3017c7  irb/on/scenario_s23_24/expected.csv
a3b73cdfbb4c17b6c7948d80ce1c3374  irb/on/scenario_s23_26/expected.csv
8bc102421289c650cd949cabfcf9677e  irb/on/scenario_s23_28/expected.csv
70c83724528abc07fab85ecbb4da1b1c  irb/on/scenario_s23_30/expected.csv
70493be12de5c9e2fe9d0065eac29f6a  irb/on/scenario_s23_32/expected.csv
4a6f6ca22f7799cf1da822508689b920  irb/on/scenario_s23_34/expected.csv
b31e54356097e914c685847533af8522  irb/on/scenario_s24_01/expected.csv
ef58e074a989a19df8253f336984b406  irb/on/scenario_s24_03/expected.csv
427abf00f28c30c1f4b723a03e9a7c4b  irb/on/scenario_s24_05/expected.csv
8636140c62291f080aac1230044d3404  irb/on/scenario_s24_07/expected.csv
264c2d7cd49b6c8242c5c8adfab75f8d  irb/on/scenario_s24_09/expected.csv
74aa71f1e3ecc913f235e50da435f3c1  irb/on/scenario_s24_11/expected.csv
017a350f2c485a25d1e35066dfd03970  irb/on/scenario_s24_13/expected.csv
67555b7f0a75848162a8e7d4b622d81a  irb/on/scenario_s24_15/expected.csv
017a350f2c485a25d1e35066dfd03970  irb/on/scenario_s24_17/expected.csv
0c32e4beb86bedc7edbd1f016f9aa325  irb/on/scenario_s24_19/expected.csv
90e469127c755b7b50b5bad14153de6b  irb/on/scenario_s24_21/expected.csv
25657161bdaa27d98ae6522bfa6a0913  irb/on/scenario_s24_23/expected.csv
ac9d6da109fb915cc7e6eea750d8208b  irb/on/scenario_s24_25/expected.csv
9b9c67d9c9ef318b322106aed97b37d4  irb/on/scenario_s24_27/expected.csv
781a10ccf18cfb61f6311d4883de0348  irb/on/scenario_s24_29/expected.csv
9238e03c0a4eb0ff1bd2db0fed6df7c8  irb/on/scenario_s25_01/expected.csv
48bbe52a23195d6e1dad59594756313a  irb/on/scenario_s25_03/expected.csv
77567d23ecb8284ac8be4753fe641bd6  irb/on/scenario_s25_05/expected.csv
8d721223a0b7f21ef262638fdf50b605  irb/on/scenario_s25_07/expected.csv
2709f3dc3a6047d42e456c0302c27068  irb/on/scenario_s25_09/expected.csv
ff795f0fb6a4f0229f23a690ececf2cf  irb/on/scenario_s25_11/expected.csv
2709f3dc3a6047d42e456c0302c27068  irb/on/scenario_s25_13/expected.csv
99b5dfd64b394a7f8dc58227921fd073  irb/on/scenario_s25_15/expected.csv
4b9e981daf7ebce8a88f2d61c73ed89e  irb/on/scenario_s25_17/expected.csv
6f52ff28a9e1c2f6066dfe44c0fc4032  irb/on/scenario_s25_19/expected.csv
ca35a0f46adf68356c63548e725fd687  irb/on/scenario_s25_21/expected.csv
b3d4c49602ccfecd19fa790afc17c9da  irb/on/scenario_s25_23/expected.csv
dc25f737ca2020c32d50d8b0a79a11c7  irb/on/scenario_s25_25/expected.csv
b09c53734e70950c6b63d521d7a25119  irb/on/scenario_s25_27/expected.csv
9fa3630d7396979bc46bf96a64350eae  irb/on/scenario_s25_29/expected.csv
c103e662b54d8c91bc77e7c7c2664155  irb/on/scenario_s25_31/expected.csv
61dc645950e475cd02a581f3324ba365  irb/on/scenario_s25_33/expected.csv
20d5b1a4cf7ec4cf68ee9d4b6a3d2aed  irb/on/scenario_s25_35/expected.csv
285d64db308686628346501b19917219  irb/on/scenario_s25_37/expected.csv
77af491ccc5367815536669e1ad7978b  irb/on/scenario_s25_39/expected.csv
ca2d24327c8df3ebab9ec3104ae0353e  irb/on/scenario_s25_41/expected.csv
0fe91c17b351583e7cd6dc4f7b038112  irb/on/scenario_s25_43/expected.csv
62042f95f350eb5578442af25faa0d74  irb/on/scenario_s25_45/expected.csv
0fe91c17b351583e7cd6dc4f7b038112  irb/on/scenario_s25_47/expected.csv
8a97e92819d8e43a50d257a9e5db698e  irb/on/scenario_s25_49/expected.csv
552de32db126b0ba1065122e115ea7de  irb/on/scenario_s25_51/expected.csv
ef08b132e27e8b9074598fe75159c8a7  irb/on/scenario_s26_01/expected.csv
d713d00889369aeba9831d32f0357bca  irb/on/scenario_s26_03/expected.csv
a75b136801138b40c24838b0e78262a7  irb/on/scenario_s26_05/expected.csv
457b7356769be721b2f127af82c56b06  irb/on/scenario_s26_07/expected.csv
695ac1e540eb569f7d937b46a7facf78  irb/on/scenario_s26_09/expected.csv
5387fa2200b62400a7be5d2df888d5f6  irb/on/scenario_s26_11/expected.csv
2073e7becd90e36d29051ce9a71c588c  irb/on/scenario_s26_13/expected.csv
06879d0d0c7f7acb2d8216ed34474374  irb/on/scenario_s26_15/expected.csv
bd53e9fba3c9988995e60a9c77d0b3ca  irb/on/scenario_s26_17/expected.csv
5f9486a2cf530552e644c6ae5a27a301  irb/on/scenario_s26_19/expected.csv
3fa8de10ebe39a2f9fa6df471104f2a1  irb/on/scenario_s26_21/expected.csv
98e2de855800b5f52fbbe23a2fa214ed  irb/on/scenario_s26_23/expected.csv
64e94c0716e74fbec556383da2a9d66f  irb/on/scenario_s26_25/expected.csv
49c97b2db656c2d1a982b3a0d418d5a2  irb/on/scenario_s26_27/expected.csv
4f7102414f88e2c73e67c92f98511606  irb/on/scenario_s26_29/expected.csv
6ab1562c80ddf04772469490f4867ea6  irb/on/scenario_s26_31/expected.csv
027a34d3e05368ad34bd1b565ad054ff  irb/on/scenario_s26_33/expected.csv
7b24d44f16177fc1ae4448b0b6964839  irb/on/scenario_s26_35/expected.csv
0a9d52b22b619c0d904de563ed73eaa9  irb/on/scenario_s26_37/expected.csv
81f28fce4cd7089051e8215b84ba832f  irb/on/scenario_s26_39/expected.csv
80906c4341f0105c9a4841a9a9aeaeb0  irb/on/scenario_s26_41/expected.csv
6ded67d160f27f6597dd93242efc14b0  irb/on/scenario_s26_43/expected.csv
93c7fe33d6e8286c4c165c43d0c9ebfc  irb/on/scenario_s26_45/expected.csv
968b3244a64a7471cd69950c05af07a9  irb/on/scenario_s26_47/expected.csv
533173e8d6ed46cd1961b61e09ac6409  irb/on/scenario_s26_49/expected.csv
99e0d4299a7bfe08673cf7f1d553651c  irb/on/scenario_s26_51/expected.csv
5a543df0b5e217ef5bca5ed7550d662b  irb/on/scenario_s27_01/expected.csv
57f199a37462b559fc4a93a212abb3b7  irb/on/scenario_s27_03/expected.csv
3fbfd831e3257d55e7f988b40a115ac2  irb/on/scenario_s27_05/expected.csv
c8a9a772783002f6db9d7f1377765657  irb/on/scenario_s27_07/expected.csv
bf21c9c1a92b17aeca7e2eecbf49794c  irb/on/scenario_s27_09/expected.csv
44d3fca54d52161beb5e1facfddbbb55  irb/on/scenario_s27_11/expected.csv
ff3e77e83fe12fc17454ca03ea10db4b  irb/on/scenario_s27_13/expected.csv
b51d368ccd73eaafdd425084cfa15e73  irb/on/scenario_s27_15/expected.csv
c5c966afd1dde4c09d1ed37264563498  irb/on/scenario_s27_17/expected.csv
7e92a3784c86dbf52c5ba16bd0fdbef6  irb/on/scenario_s27_19/expected.csv
7d9bff6f00d41f6afa4533b52611d2d0  irb/on/scenario_s27_21/expected.csv
057b62e061e189b95a1bc88f3415041a  irb/on/scenario_s27_23/expected.csv
f311f70148a46efc17f050312d2eee41  irb/on/scenario_s27_25/expected.csv
a4035b81877ffe3c8ba41ba76cd15020  irb/on/scenario_s27_27/expected.csv
66bc14d93651bf2e6527d7244e21adef  irb/on/scenario_s27_29/expected.csv
1bb2426f42368dba04ece494179c87e5  irb/on/scenario_s27_31/expected.csv
4680e76b17a00d304fffdbec121eff9a  irb/on/scenario_s27_33/expected.csv
919fe3dfdac6958b2933ac7147c9deed  irb/on/scenario_s27_35/expected.csv
6d75cc0ed890886ceb8434de1ac1c102  irb/on/scenario_s27_37/expected.csv
ef0e86fd0016bca42021173562ecad3e  irb/on/scenario_s27_39/expected.csv
7902d779c8d5cc85c918757050370e41  irb/on/scenario_s27_41/expected.csv
31ca2a1b752159bcf135ee60b7989ef8  irb/on/scenario_s27_43/expected.csv
e42bdc215639d1b222c8c15ea48ac8b0  irb/on/scenario_s27_45/expected.csv
eef745cd8eaa3bc2d3e16c9746f585a5  irb/on/scenario_s27_47/expected.csv
7c9f89acb7a2e084d69f63d2372cd45d  irb/on/scenario_s28_01/expected.csv
ec92ae7825d5ca514c951b94eb2b9177  irb/on/scenario_s28_03/expected.csv
4756f0f199fd9d947febf03d56ad6f66  irb/on/scenario_s28_05/expected.csv
9f48c9ed167ac069fd0c1e01663a30c4  irb/on/scenario_s28_07/expected.csv
2a6e00500467b2a3a3eb7e771e54ccd7  irb/on/scenario_s28_09/expected.csv
6ead80dcacbfeadbb18ecbf8cc49bd96  irb/on/scenario_s28_11/expected.csv
2a6e00500467b2a3a3eb7e771e54ccd7  irb/on/scenario_s28_13/expected.csv
125db3eef51a8ec80b9d9428e2f51452  irb/on/scenario_s28_15/expected.csv
dc52b3e80782a4bfaea793be6d833a60  irb/on/scenario_s28_17/expected.csv
3b27e940148805128024b6d3feec673a  irb/on/scenario_s28_19/expected.csv
325e3ab06bf60f0c0f88f143a25e4b4e  irb/on/scenario_s28_21/expected.csv
721f5ada8defd8e8cfbba06de201b729  irb/on/scenario_s28_23/expected.csv
a3cb8342e4c1e8feca4e43c93a729f21  irb/on/scenario_s28_25/expected.csv
ea369285af9535286742351429265aed  irb/on/scenario_s28_27/expected.csv
dee13ff1c1a21672de38d67061125c17  irb/on/scenario_s28_29/expected.csv
28bbf9030f515a0a8359174dbd463462  irb/on/scenario_s28_31/expected.csv
47062bea53a8578f5e57a64f76ab1552  irb/on/scenario_s28_33/expected.csv
17ba58c59a9e3a3fc344203ee9616c8a  irb/on/scenario_s28_35/expected.csv
2c751a106f8c2d282ebdd272e5a07a39  irb/on/scenario_s28_37/expected.csv
fc0bf97c1df808d907135e3008eae2be  irb/on/scenario_s28_39/expected.csv
32f4d2884cfc39e30e1c6b43de8c2c33  irb/on/scenario_s28_41/expected.csv
90a9b3108a0bf12b21de6bbdd39f5760  irb/on/scenario_s28_43/expected.csv
6ee867340cdc0a23e155ec9f48d4d162  irb/on/scenario_s28_45/expected.csv
0019f9ce75ef2342bb4ffca4ea7e1a90  irb/on/scenario_s28_47/expected.csv
c295ee2e0c71a1d7e31d45e96eaa7220  irb/on/scenario_s29_01/expected.csv
fd24481eb1581cd81df7fea107567366  irb/on/scenario_s29_03/expected.csv
9bd3182464f505aa016f11673adbac2a  irb/on/scenario_s29_05/expected.csv
e864060fe86b684764ed6d7e0f0b4ae9  irb/on/scenario_s29_07/expected.csv
60ce45951753bd95f15d852fcbc755c4  irb/on/scenario_s29_09/expected.csv
38ef5da0ce8a7631e72bff7e9bc43ab8  irb/on/scenario_s29_11/expected.csv
bad332c92291ff4fbfc6ccd58c518e2a  irb/on/scenario_s29_13/expected.csv
f699e0c9e55bc2a02f26c543d5ff8ed4  irb/on/scenario_s29_15/expected.csv
0cf87933ae580df5c45705f989515981  irb/on/scenario_s29_17/expected.csv
75eddd29732b6838a9a13ab887ed6a22  irb/on/scenario_s29_19/expected.csv
8a141ef90e8edb18218c9cf044844b03  irb/on/scenario_s29_21/expected.csv
f5f890f58d1d4b98e4c1220e104b089e  irb/on/scenario_s29_23/expected.csv
19f9b25d514050f2aa21b70cefc453dd  irb/on/scenario_s29_25/expected.csv
96ef3d256487d91384cbd88b8f68fc8d  irb/on/scenario_s29_27/expected.csv
4c73f84449e12d4d774324d300620e4f  irb/on/scenario_s29_29/expected.csv
723fc3f521b5dfe6af324290fc783bee  irb/on/scenario_s29_31/expected.csv
10d8dc918b416b508d7a78cc9c5350dd  irb/on/scenario_s29_33/expected.csv
4b26d9046d5520b82e7cdb1044ce6c7d  irb/on/scenario_s29_35/expected.csv
88b5316229eff1f1280243a83ceab8c9  irb/on/scenario_s29_37/expected.csv
9a5491aa461be2bc69f92df86e3ff5e2  irb/on/scenario_s29_39/expected.csv
7422d70de975af982809834a2a28d40b  irb/on/scenario_s29_41/expected.csv
d0aa6cb69a53070e5a60ac58635749e7  irb/on/scenario_s29_43/expected.csv
1a9c01c4552a9bbff9a5945981d9e66a  irb/on/scenario_s29_45/expected.csv
8ea9153a0bd5d33381ad6806ef12305e  irb/on/scenario_s29_47/expected.csv
43c7f7dbea97f0947d8b9f8a11ce8353  irb/on/scenario_s29_49/expected.csv
8acf7d4d126eaf879fa7e79eedeada07  irb/on/scenario_s30_01/expected.csv
48ba453a0868547f041742525e6838ca  irb/on/scenario_s30_03/expected.csv
4bb24469c2260cd409f6ae4e49056ae3  irb/on/scenario_s30_05/expected.csv
55d115100c1ad8f1cbcc87aa0a897bef  irb/on/scenario_s30_07/expected.csv
c1d15f80e7c62131ac97407eded2c1bc  irb/on/scenario_s30_09/expected.csv
8b6fee002fcf8e947fea108227373b8d  irb/on/scenario_s30_11/expected.csv
c1d15f80e7c62131ac97407eded2c1bc  irb/on/scenario_s30_13/expected.csv
edc919e11c0b7eec7629477518e69973  irb/on/scenario_s30_15/expected.csv
001ddedd0cdf63ca43862fa44e69af83  irb/on/scenario_s30_17/expected.csv
654416c5d4bb1b943a61c2d4b49edb09  irb/on/scenario_s30_19/expected.csv
47903b6d49f24f1eeaeef189c367cd1f  irb/on/scenario_s30_21/expected.csv
7df6f69e3955e591bf2b42ff8be80ff1  irb/on/scenario_s30_23/expected.csv
47903b6d49f24f1eeaeef189c367cd1f  irb/on/scenario_s30_25/expected.csv
ba75dc5f5bbaeef1c41017fa27cba4b3  irb/on/scenario_s30_27/expected.csv
6f829a847bc3785703a3a23be4f3745f  irb/on/scenario_s30_29/expected.csv
ba75dc5f5bbaeef1c41017fa27cba4b3  irb/on/scenario_s30_31/expected.csv
2287685c79103edce387d5b3636d2c68  irb/on/scenario_s30_33/expected.csv
0369aee02601c7888f21413b928019af  irb/on/scenario_s30_35/expected.csv
c88d274ec0491b4521b58c7e8931e898  irb/on/scenario_s30_37/expected.csv
1da847da5891e1afad32732bd209281c  irb/on/scenario_s30_39/expected.csv
7ad3d57244611fc86bbeeb152be6ef5a  irb/on/scenario_s30_41/expected.csv
7d8c0a3c6e6196d95cddd538e03955d8  irb/on/scenario_s30_43/expected.csv
983101ee95b677f0d41a201c512f3f38  irb/on/scenario_s30_45/expected.csv
7082574368eaad58f900e88194997602  irb/on/scenario_s30_47/expected.csv
bfbcf13b67d838f4c73745e9d527d5ec  irb/on/scenario_s30_49/expected.csv
```

### irb, off (105)

```
903077ce83fa839ce2c3cf1f7c6f8c2c  irb/off/scenario_s17_01/expected.csv
8a7334901e8710ed475fe8e2c136038e  irb/off/scenario_s17_06/expected.csv
23dfeb877e7d9959200c64da53a3d466  irb/off/scenario_s17_11/expected.csv
1886715bcfca43375e59f1e3b7f06cda  irb/off/scenario_s17_17/expected.csv
9efbd9fa475e4c6247a453d9aed99ad8  irb/off/scenario_s17_23/expected.csv
00fb7469b41f2772c38b06749291652c  irb/off/scenario_s17_29/expected.csv
e1c2ab6a1a60d1f92b7a52a0dc136667  irb/off/scenario_s17_35/expected.csv
01e14e127024cd9ae04f7616788eea80  irb/off/scenario_s18_01/expected.csv
a3afd0f41b3a82e8eabf01d103dbbcbe  irb/off/scenario_s18_07/expected.csv
63713276c82cd7f6d1e000c4f202876d  irb/off/scenario_s18_13/expected.csv
056a55520fe526cfe2a39514cd7471a5  irb/off/scenario_s18_19/expected.csv
5046fb2b73cf15307b0b79206682aeaf  irb/off/scenario_s18_25/expected.csv
45722505507a2269e7fee11ab4d94825  irb/off/scenario_s19_01/expected.csv
ea3938e196f8a2d654fd2cd962e065f2  irb/off/scenario_s19_06/expected.csv
a4a762b8ee663100cc293dcda6b8ee67  irb/off/scenario_s19_12/expected.csv
0d24d3fea03d93b1b5643322c8a2abff  irb/off/scenario_s19_18/expected.csv
7160a49d7821d51cf305b9bde71b1a0a  irb/off/scenario_s19_24/expected.csv
998595c8067cf77a94b0768b50a89c08  irb/off/scenario_s19_30/expected.csv
931dbe4c05e27c1e8b38bc8db262c8f2  irb/off/scenario_s20_01/expected.csv
8de4574b1fcb3f9636ed66a22768245e  irb/off/scenario_s20_07/expected.csv
c04a7daa7c444d6d3903470f54a5d97f  irb/off/scenario_s20_13/expected.csv
8cedd62e732377a8caf5ed5be5284b81  irb/off/scenario_s20_19/expected.csv
2fb49fefe08c8041c4ef949b45c7ceed  irb/off/scenario_s20_25/expected.csv
5fb3063b21119d28c30f3c586fd14b84  irb/off/scenario_s21_01/expected.csv
f078857e3ce0f152fe2e3e662bf4b956  irb/off/scenario_s21_06/expected.csv
5fe054d1d7609eda9ca27f83e2c7f0ce  irb/off/scenario_s21_10/expected.csv
beffe827edea8bc168ea06ad6e22708c  irb/off/scenario_s21_16/expected.csv
7d3394dfabd15c94d8c23b56b059c027  irb/off/scenario_s21_22/expected.csv
faad3c118bd5e17c7de01034122594ea  irb/off/scenario_s21_28/expected.csv
ea84d1eeaab20e14cce8b4574ecc1ad0  irb/off/scenario_s22_01/expected.csv
066974f2725c396cb16d74f6cf7588f9  irb/off/scenario_s22_05/expected.csv
8749ff157247898c960b47185b8cd82c  irb/off/scenario_s22_11/expected.csv
3102cd1eadc3fa78c6e7d8657a4186c7  irb/off/scenario_s22_17/expected.csv
d75b724ccfc83099e197767500707562  irb/off/scenario_s22_23/expected.csv
857933383cef6d6d49f1020b60c4e5f6  irb/off/scenario_s23_01/expected.csv
86ab1011311df191e2d5b4d394dd923f  irb/off/scenario_s23_08/expected.csv
afaaadfb72887aa2b2fdd7cb48d7b5ef  irb/off/scenario_s23_14/expected.csv
506fdcdc4cb55d70cd7cf216dc6787aa  irb/off/scenario_s23_20/expected.csv
87b6f7d701c426b76b31d377d4ce6a9e  irb/off/scenario_s23_26/expected.csv
fc2f3f6f69c23cf40f12b7bac5081629  irb/off/scenario_s23_30/expected.csv
0c8d43f61156e1d54780949569062120  irb/off/scenario_s24_01/expected.csv
9ac5e7b6e6bbd305245847dc73cc930a  irb/off/scenario_s24_07/expected.csv
90b703b4718c87c353ec910adb774ff8  irb/off/scenario_s24_13/expected.csv
d32e1e5b04a7097addb823d5cdd049a8  irb/off/scenario_s24_19/expected.csv
d4fd752e25e7c0db99abbca9bffc4bb5  irb/off/scenario_s24_25/expected.csv
48029578a3fa95930f1599a16b2c358c  irb/off/scenario_s25_01/expected.csv
cde24edf873c4836f64910d6a7f0206a  irb/off/scenario_s25_05/expected.csv
e67e9b19b6a0a927056273aaa1c5d22e  irb/off/scenario_s25_09/expected.csv
a08e0947936b6bf40530be687fae287a  irb/off/scenario_s25_15/expected.csv
42063681820be04a122eaba3c7a499ed  irb/off/scenario_s25_21/expected.csv
9731490fc6e8edd06112e84ae3e84df0  irb/off/scenario_s25_27/expected.csv
ed0eac3d88b8cda11fc17663589beeee  irb/off/scenario_s25_33/expected.csv
95f802da6f88cccdf396088100c4f3bb  irb/off/scenario_s25_39/expected.csv
1c60aeb35d90bd729a4d1dd4dd8cb5cf  irb/off/scenario_s25_43/expected.csv
20787b317d4898ac0dda39927a9465ed  irb/off/scenario_s25_49/expected.csv
c9543785158c6a8205d2e1aa00b4a5d9  irb/off/scenario_s26_01/expected.csv
91f3ff689429cd811b7f90949fe63565  irb/off/scenario_s26_05/expected.csv
c815adf539d040d84fe927be8510ee20  irb/off/scenario_s26_09/expected.csv
d7e2164db019632a7fbf4c6e031bfed0  irb/off/scenario_s26_15/expected.csv
5112522257b4b8c5b02812353a67a610  irb/off/scenario_s26_21/expected.csv
fe192780657dfd4533a2914a9a0bba08  irb/off/scenario_s26_27/expected.csv
014ca34214acb525f61345f0fc37191e  irb/off/scenario_s26_31/expected.csv
1bb17b6d6355b127fe222e1875c1831a  irb/off/scenario_s26_37/expected.csv
21ca81e59a99fdf3d924642a4f705459  irb/off/scenario_s26_41/expected.csv
b49ebfa133d2ba7d6429b70db7dd71be  irb/off/scenario_s26_47/expected.csv
00ec75b980904be8f6ec4ee597c4898d  irb/off/scenario_s27_01/expected.csv
3fa5bb02bb6be45dfb6441a5f6fb7d3c  irb/off/scenario_s27_05/expected.csv
3691b214c45ec1dab2a78b5ebb001f2c  irb/off/scenario_s27_09/expected.csv
24770edf097edb5a8dbfc83dd5b330d8  irb/off/scenario_s27_13/expected.csv
c0d830efa0e162969707401e4ffbf8d8  irb/off/scenario_s27_19/expected.csv
99967d0a777b150295c25909d69cc3e4  irb/off/scenario_s27_25/expected.csv
e1da666e5c4bddf0cb8da6ea5eb60c37  irb/off/scenario_s27_29/expected.csv
ab2cca472775cb7e08ed2a0846094aef  irb/off/scenario_s27_35/expected.csv
d73199dfe750662540aadd2b33c7bc44  irb/off/scenario_s27_41/expected.csv
030e195ca41d82247f21bafb2f152627  irb/off/scenario_s27_43/expected.csv
688d332e1472958c40ea68049b605531  irb/off/scenario_s28_01/expected.csv
40d8dcef24fb63272923db1f982de3aa  irb/off/scenario_s28_05/expected.csv
4adae2c2915c27032b659966eee94c01  irb/off/scenario_s28_09/expected.csv
b15a8e18d03ca5e2d4815419bdf7ae8d  irb/off/scenario_s28_15/expected.csv
3b5f2948683deb9de4a9ade50697fd2b  irb/off/scenario_s28_21/expected.csv
619875deeced851c42711a8acd1579f9  irb/off/scenario_s28_27/expected.csv
981997f791041b9aa91b11685590697d  irb/off/scenario_s28_31/expected.csv
ff5f49d7525786d39e4db661a98b1c5b  irb/off/scenario_s28_37/expected.csv
48e44e2dadd8b2d8edfdd6783649ecba  irb/off/scenario_s28_41/expected.csv
97cbfe319dc06e3fdd64b3e80a0551fb  irb/off/scenario_s28_47/expected.csv
ce1c5967f3e3cb581efb36b44c90939f  irb/off/scenario_s29_01/expected.csv
74a27b4e8bfa6d1fe77e077947419a16  irb/off/scenario_s29_05/expected.csv
767953f1ad6f842052ee0f1504fcc516  irb/off/scenario_s29_09/expected.csv
f7adcff3ca670fdc1c78a7df0ebe95e2  irb/off/scenario_s29_15/expected.csv
62fb103836aa078607b37c0fe4a42882  irb/off/scenario_s29_21/expected.csv
1f957fb7d77a7f56fbb27de557773265  irb/off/scenario_s29_27/expected.csv
37204533158a6f22dde3363567fb76c3  irb/off/scenario_s29_33/expected.csv
13ba325d824d5f236c7ad4a3efeea2df  irb/off/scenario_s29_39/expected.csv
aea4872095cae362f5d157f8df2f4ad4  irb/off/scenario_s29_43/expected.csv
c1e59e688c68b607c36e834f95a7c737  irb/off/scenario_s29_47/expected.csv
0416116b2f80afbce6b1c7f7070076a4  irb/off/scenario_s30_01/expected.csv
0e01c4345f883b726609614e5942a163  irb/off/scenario_s30_05/expected.csv
a0d834a85e6120fe5d31a81d9d618ffb  irb/off/scenario_s30_09/expected.csv
8ae6d00d5d7a4489b7d2a53eeb435954  irb/off/scenario_s30_15/expected.csv
99f6dc019c05051fdb235681fe93d244  irb/off/scenario_s30_21/expected.csv
0f2e30681ea6bcf29e9b0c614820541d  irb/off/scenario_s30_27/expected.csv
ae9d9ca11133844dd5de8a07a8170bec  irb/off/scenario_s30_33/expected.csv
0b76949448bb4d092be8a473dffd13b4  irb/off/scenario_s30_37/expected.csv
f28a9ebbd8f138ea0cce9debed14cb7e  irb/off/scenario_s30_41/expected.csv
86b0d21d201ee5a706170ee3fde4a253  irb/off/scenario_s30_45/expected.csv
```

### mpb, on (282)

```
535b63557e712856186d2a2310eedf2f  mpb/on/scenario_s02_01/on_single_task/expected_ticks.json
f8e0ad0d2fe9113e9361d934784c46da  mpb/on/scenario_s02_02/on_single_task/expected_ticks.json
5696fca668fdfc88d0e2c2d47c9f9d71  mpb/on/scenario_s03_06/on_single_task/expected_ticks.json
8680e0fe27fd425140ccd7eebd44c124  mpb/on/scenario_s04_01/on_single_task/expected_ticks.json
6dd3cc4a951a699cd91134d7aad2d32d  mpb/on/scenario_s05_01/on_single_task/expected_ticks.json
c3a6615b023fa06e1b04556fb5e9a467  mpb/on/scenario_s05_02/on_single_task/expected_ticks.json
f8fe7c3c6964c78c7324cc407d687a0a  mpb/on/scenario_s17_03/on_single_task/expected_ticks.json
7fd6446559c84c93cd98caf20e0b0f96  mpb/on/scenario_s17_05/on_single_task/expected_ticks.json
e2b21bd726157db41c3d7f3aee25f69f  mpb/on/scenario_s17_08/on_single_task/expected_ticks.json
d01dec04e022004d1de8cfc1b316b5d1  mpb/on/scenario_s17_10/on_single_task/expected_ticks.json
48f787eee6e1fca353e7e16ac90db058  mpb/on/scenario_s17_12/on_single_task/expected_ticks.json
c540b642589ba4eeebb763cbc58d094d  mpb/on/scenario_s17_14/on_single_task/expected_ticks.json
23f5f2cc9a5ca5c5aa7eab76f1796bc8  mpb/on/scenario_s17_16/on_single_task/expected_ticks.json
078438a394ed1a51e8645419d4bb84f3  mpb/on/scenario_s17_18/on_single_task/expected_ticks.json
4a6b0a307d85d07c1917d16bc2e99a37  mpb/on/scenario_s17_20/on_single_task/expected_ticks.json
078438a394ed1a51e8645419d4bb84f3  mpb/on/scenario_s17_22/on_single_task/expected_ticks.json
d09057454c6c64f8bc0bf30a1f77496a  mpb/on/scenario_s17_24/on_single_task/expected_ticks.json
d90fa5bb791d9dbfcd7b7143cb757f2e  mpb/on/scenario_s17_26/on_single_task/expected_ticks.json
e52f2e1534b1c7489f14de237c9c2a94  mpb/on/scenario_s17_28/on_single_task/expected_ticks.json
0b8c4408db2da835eae1dd6a87642d6a  mpb/on/scenario_s17_30/on_single_task/expected_ticks.json
73f5e7be7adab2e6cd66c3382dcab501  mpb/on/scenario_s17_32/on_single_task/expected_ticks.json
03a43ac36a74a0e976b4d8e16b95f45a  mpb/on/scenario_s17_34/on_single_task/expected_ticks.json
c207d97c4e925f55d5d80de444939a5b  mpb/on/scenario_s17_36/on_single_task/expected_ticks.json
33557694c0bbd7699780fa26bfbcd5d5  mpb/on/scenario_s17_38/on_single_task/expected_ticks.json
cd324e40e9ed17ecd0adabca13d5d7e9  mpb/on/scenario_s17_40/on_single_task/expected_ticks.json
9fd247d8ca9db0c3409f8ae1d67892fa  mpb/on/scenario_s18_02/on_single_task/expected_ticks.json
24ce4dec7d723867d416f04c80f5bbe6  mpb/on/scenario_s18_04/on_single_task/expected_ticks.json
a8728a846c4a2ecfb7bea28fdb43f02b  mpb/on/scenario_s18_06/on_single_task/expected_ticks.json
735b132b5e46cd4cc13022eaf0ad60f7  mpb/on/scenario_s18_08/on_single_task/expected_ticks.json
67f20757c2db430e3428eb206062deb9  mpb/on/scenario_s18_10/on_single_task/expected_ticks.json
c36085672bba731ba1975d4257528859  mpb/on/scenario_s18_12/on_single_task/expected_ticks.json
3363b8153b53875f1184b883a5766228  mpb/on/scenario_s18_14/on_single_task/expected_ticks.json
02ebd92e6e340d04af2b2872e1eadf5d  mpb/on/scenario_s18_16/on_single_task/expected_ticks.json
5f021c69081f532f6839145f0d520ee1  mpb/on/scenario_s18_18/on_single_task/expected_ticks.json
c119b1210420cd3f6b95f591e4a8717a  mpb/on/scenario_s18_20/on_single_task/expected_ticks.json
d51e7b3f4867fe1339683ec6a7715cd7  mpb/on/scenario_s18_22/on_single_task/expected_ticks.json
c119b1210420cd3f6b95f591e4a8717a  mpb/on/scenario_s18_24/on_single_task/expected_ticks.json
bf59a910c5dfabe6646122a67372fa30  mpb/on/scenario_s18_26/on_single_task/expected_ticks.json
ebdb48e9281c9c94d956f8a297bc12fe  mpb/on/scenario_s18_28/on_single_task/expected_ticks.json
b0885c6af535d1781ee9fdbb4dcb7290  mpb/on/scenario_s18_30/on_single_task/expected_ticks.json
5f8310382e284f0bb27c8bdfb607c00a  mpb/on/scenario_s19_03/on_single_task/expected_ticks.json
99e30e40ce018f11c6a2e0a8d24078b4  mpb/on/scenario_s19_05/on_single_task/expected_ticks.json
56cedc57fe1fae64e9572e3f1e0c95fb  mpb/on/scenario_s19_07/on_single_task/expected_ticks.json
30f8e3e00fe47dcc58850d901c45cd64  mpb/on/scenario_s19_09/on_single_task/expected_ticks.json
1e57780c35e5ca516827fd29020dfa02  mpb/on/scenario_s19_11/on_single_task/expected_ticks.json
61c64325df0cfc32efe5a773c91ecb05  mpb/on/scenario_s19_13/on_single_task/expected_ticks.json
d4cbc0764908e9e3c8decd7805b4e7af  mpb/on/scenario_s19_15/on_single_task/expected_ticks.json
e0ac6f4615a53e76cd78e59b3dbfbc3e  mpb/on/scenario_s19_17/on_single_task/expected_ticks.json
802460f1110fec6699444c7c5cf9c180  mpb/on/scenario_s19_19/on_single_task/expected_ticks.json
cedc970527d05f2b789539616e1ddd5b  mpb/on/scenario_s19_21/on_single_task/expected_ticks.json
19dc5e7ac8bd19933cf736c7b6e863d1  mpb/on/scenario_s19_23/on_single_task/expected_ticks.json
7d571454de34e5a2e2859224726a2afa  mpb/on/scenario_s19_25/on_single_task/expected_ticks.json
8dbdaa4c214f50db73b8d820674c1fcc  mpb/on/scenario_s19_27/on_single_task/expected_ticks.json
55b06f80511d429e8e14c2090d1efe3d  mpb/on/scenario_s19_29/on_single_task/expected_ticks.json
511937babdfa53b6fd2fa69355dbdf15  mpb/on/scenario_s19_31/on_single_task/expected_ticks.json
bf7ea945d35d832e69cb23e8af9c0e52  mpb/on/scenario_s19_33/on_single_task/expected_ticks.json
efd343cb5dfe9d9d17290876eaf7e4c8  mpb/on/scenario_s20_02/on_single_task/expected_ticks.json
e3efeeb71bfd9e75bdcc2f413ea52851  mpb/on/scenario_s20_04/on_single_task/expected_ticks.json
4cc33e08078ae6a7e629606d23424c1c  mpb/on/scenario_s20_06/on_single_task/expected_ticks.json
264ec151b599715ae67cfc11d7bcba02  mpb/on/scenario_s20_08/on_single_task/expected_ticks.json
cd32cfbee38166dfd1abbc7915ebf140  mpb/on/scenario_s20_10/on_single_task/expected_ticks.json
2f5c6a500296815d4c57eb1c0216b01d  mpb/on/scenario_s20_12/on_single_task/expected_ticks.json
ce67c1f4cf838c5d4fc281a73490e5d7  mpb/on/scenario_s20_14/on_single_task/expected_ticks.json
3cd2d2ffed9e587963b35284d65ad33a  mpb/on/scenario_s20_16/on_single_task/expected_ticks.json
9e1c885369587240d206ecce8e1b1b13  mpb/on/scenario_s20_18/on_single_task/expected_ticks.json
58eb55587f958daec28a34f62464cb71  mpb/on/scenario_s20_20/on_single_task/expected_ticks.json
6e532db33163ee43904cc718963d3d4b  mpb/on/scenario_s20_22/on_single_task/expected_ticks.json
a4597b7e8d99b5cd97c5c93825d38f49  mpb/on/scenario_s20_24/on_single_task/expected_ticks.json
4cc37942d786acfa1ef0fa027f12926b  mpb/on/scenario_s20_26/on_single_task/expected_ticks.json
fe52899fb2085696ab79c9644b37a535  mpb/on/scenario_s20_28/on_single_task/expected_ticks.json
ccb51886dc9f9d07f3a0e4aca435e8e3  mpb/on/scenario_s20_30/on_single_task/expected_ticks.json
5696fca668fdfc88d0e2c2d47c9f9d71  mpb/on/scenario_s21_03/on_single_task/expected_ticks.json
9f5400d3632c20b718f38aecbd7dbe6a  mpb/on/scenario_s21_05/on_single_task/expected_ticks.json
14b9023b8a151d422ed0dfb85ae30b5f  mpb/on/scenario_s21_07/on_single_task/expected_ticks.json
972d31e81ae373abb31c0fad3e9acc4f  mpb/on/scenario_s21_09/on_single_task/expected_ticks.json
b4fd428afa7167e5ff19e0b115ed3bf1  mpb/on/scenario_s21_11/on_single_task/expected_ticks.json
32d92ca5f0e75b66e0ca4d0fc66c7e22  mpb/on/scenario_s21_13/on_single_task/expected_ticks.json
b4fd428afa7167e5ff19e0b115ed3bf1  mpb/on/scenario_s21_15/on_single_task/expected_ticks.json
738a9b72f0082e877aa504e6652ada07  mpb/on/scenario_s21_17/on_single_task/expected_ticks.json
296ad8a5c65bf78ce9754287417d9272  mpb/on/scenario_s21_19/on_single_task/expected_ticks.json
c0e38fd6d4e23ee45138d3602c81abe1  mpb/on/scenario_s21_21/on_single_task/expected_ticks.json
c0236a279f66a1b19f9534ff5070301f  mpb/on/scenario_s21_23/on_single_task/expected_ticks.json
7abe60f4cf83c66e088df8c12e6f55bd  mpb/on/scenario_s21_25/on_single_task/expected_ticks.json
d1ef73943aaabad266b0cb3904c6d05b  mpb/on/scenario_s21_27/on_single_task/expected_ticks.json
5956d5353a347e083b4a4ab329b735da  mpb/on/scenario_s21_29/on_single_task/expected_ticks.json
03a8cdbf9e6bed94d6718ae9a10449c6  mpb/on/scenario_s21_31/on_single_task/expected_ticks.json
792df390b5452dbc7eda9624385f630b  mpb/on/scenario_s22_02/on_single_task/expected_ticks.json
00a1617f1d311465526fe11112c02978  mpb/on/scenario_s22_04/on_single_task/expected_ticks.json
e20cec0ff3d6bba54513d3d02ab83d39  mpb/on/scenario_s22_06/on_single_task/expected_ticks.json
1ac8b887435c163b9a893f3137ee4c10  mpb/on/scenario_s22_08/on_single_task/expected_ticks.json
758125e4d9817151dd99cfef15604f83  mpb/on/scenario_s22_10/on_single_task/expected_ticks.json
bc9e367c37b5597d114d8b7813e80333  mpb/on/scenario_s22_12/on_single_task/expected_ticks.json
7837811d652ae562431442d7c0a9e883  mpb/on/scenario_s22_14/on_single_task/expected_ticks.json
bc9e367c37b5597d114d8b7813e80333  mpb/on/scenario_s22_16/on_single_task/expected_ticks.json
001aa24c02e33d7130878f5056c241e1  mpb/on/scenario_s22_18/on_single_task/expected_ticks.json
001aa24c02e33d7130878f5056c241e1  mpb/on/scenario_s22_20/on_single_task/expected_ticks.json
dd15f5b7f59c065605a6f86230966a72  mpb/on/scenario_s22_22/on_single_task/expected_ticks.json
afeb56c7474841fe61574e3815aef405  mpb/on/scenario_s22_24/on_single_task/expected_ticks.json
7cdb01ac528b7528fc17c2d7e4599ded  mpb/on/scenario_s22_26/on_single_task/expected_ticks.json
fed6bab878710c9b53168430cf42bc8a  mpb/on/scenario_s23_03/on_single_task/expected_ticks.json
c9c0a68d1410a53c7cd4fbf5045488bf  mpb/on/scenario_s23_04/on_single_task/expected_ticks.json
6dd3cc4a951a699cd91134d7aad2d32d  mpb/on/scenario_s23_06/on_single_task/expected_ticks.json
c3a6615b023fa06e1b04556fb5e9a467  mpb/on/scenario_s23_07/on_single_task/expected_ticks.json
07ff218956705671dd312fde12953726  mpb/on/scenario_s23_09/on_single_task/expected_ticks.json
cf652f6cd4a954c38474f51791c29b7b  mpb/on/scenario_s23_11/on_single_task/expected_ticks.json
9e8913919feb3bfee5470cc24e9e73a7  mpb/on/scenario_s23_13/on_single_task/expected_ticks.json
867b20b4f48f2d48d9e13a1a8f2cb356  mpb/on/scenario_s23_15/on_single_task/expected_ticks.json
54d10332a7efe1a7d94521a50e42afae  mpb/on/scenario_s23_17/on_single_task/expected_ticks.json
224167d88367591e8fc4ffee4d107066  mpb/on/scenario_s23_19/on_single_task/expected_ticks.json
81a83de80ac80fcf4bfc42dadeb6082e  mpb/on/scenario_s23_21/on_single_task/expected_ticks.json
c421d34785c57e753a667709bc1e9e3e  mpb/on/scenario_s23_23/on_single_task/expected_ticks.json
daac100742901d5ef79575eaf59fbc6c  mpb/on/scenario_s23_25/on_single_task/expected_ticks.json
bfdc00120ec5a2d76fb4d55af092c4b5  mpb/on/scenario_s23_27/on_single_task/expected_ticks.json
18853423183566015f650c2ec4a45bd8  mpb/on/scenario_s23_29/on_single_task/expected_ticks.json
f63135fbe007102f85f5465d699d1c3f  mpb/on/scenario_s23_31/on_single_task/expected_ticks.json
bacb3ff6ee76972159bbc00b0da852a4  mpb/on/scenario_s23_33/on_single_task/expected_ticks.json
a830873890976f6c75ce9b277998f3d6  mpb/on/scenario_s23_35/on_single_task/expected_ticks.json
1c945bb5d45c0b7467f8c269b93d7701  mpb/on/scenario_s24_02/on_single_task/expected_ticks.json
c8ccfc4ab8c646202d9dbcd2e98b3bc7  mpb/on/scenario_s24_04/on_single_task/expected_ticks.json
a9ebe712c28ba43823fc725479393bf7  mpb/on/scenario_s24_06/on_single_task/expected_ticks.json
ee0dcfb5b36f4584feda1d83c3fd3c59  mpb/on/scenario_s24_08/on_single_task/expected_ticks.json
9327ae3ff596de58b11fee6638405e9f  mpb/on/scenario_s24_10/on_single_task/expected_ticks.json
02cc848f41cc0781e95c3e607fca0c19  mpb/on/scenario_s24_12/on_single_task/expected_ticks.json
660af069bb3e381eb17c1e27fc047ffb  mpb/on/scenario_s24_14/on_single_task/expected_ticks.json
36652441545d423f8bec8d588d22be53  mpb/on/scenario_s24_16/on_single_task/expected_ticks.json
660af069bb3e381eb17c1e27fc047ffb  mpb/on/scenario_s24_18/on_single_task/expected_ticks.json
e1599effcd6b32ef175f2d0418071412  mpb/on/scenario_s24_20/on_single_task/expected_ticks.json
a49ff9bb27a990057cb8e88090330048  mpb/on/scenario_s24_22/on_single_task/expected_ticks.json
6bf5cde6b30f01648e4288aee0de38a7  mpb/on/scenario_s24_24/on_single_task/expected_ticks.json
ccf67b3899e633b007461fbe1b12b6a8  mpb/on/scenario_s24_26/on_single_task/expected_ticks.json
881ab55c41a642233ee0cdf39d9b0f86  mpb/on/scenario_s24_28/on_single_task/expected_ticks.json
5f3c730e54b232af97990c0dadca6821  mpb/on/scenario_s24_30/on_single_task/expected_ticks.json
6e086de4a3b80739269850583e2fd268  mpb/on/scenario_s25_02/on_single_task/expected_ticks.json
6a2f9478b5e695498e9ca1995deb5ab6  mpb/on/scenario_s25_04/on_single_task/expected_ticks.json
bd197fb74695dc0e56e32e479a7a0d4b  mpb/on/scenario_s25_06/on_single_task/expected_ticks.json
5d8db847d5d68a975c916de0c7cc43a6  mpb/on/scenario_s25_08/on_single_task/expected_ticks.json
c9fa5592973fb21e0106d2b6e118d06f  mpb/on/scenario_s25_10/on_single_task/expected_ticks.json
78ae0c5fcdf188149b2fb34e030a5b6b  mpb/on/scenario_s25_12/on_single_task/expected_ticks.json
c9fa5592973fb21e0106d2b6e118d06f  mpb/on/scenario_s25_14/on_single_task/expected_ticks.json
fa3c033d0f0dbbc43bb5d59fe822e12c  mpb/on/scenario_s25_16/on_single_task/expected_ticks.json
c0d8d1940328445a262e05822ea92edc  mpb/on/scenario_s25_18/on_single_task/expected_ticks.json
75bc18d3dd9e629654396f00e6fe52bc  mpb/on/scenario_s25_20/on_single_task/expected_ticks.json
19eab342e525b1d2750ae26df24cbc8c  mpb/on/scenario_s25_22/on_single_task/expected_ticks.json
ab02ff5d4d0b67dfe833e8810e40902a  mpb/on/scenario_s25_24/on_single_task/expected_ticks.json
2062eddc0f5221c2adeb680a153f588c  mpb/on/scenario_s25_26/on_single_task/expected_ticks.json
4a316b9116f9922d2fba92775e940787  mpb/on/scenario_s25_28/on_single_task/expected_ticks.json
261a4216110fb7957bf754047d9c960b  mpb/on/scenario_s25_30/on_single_task/expected_ticks.json
5264c5e17caaa67beebe5c4b58533632  mpb/on/scenario_s25_32/on_single_task/expected_ticks.json
a011b02cf18ee04ced27fdac67946420  mpb/on/scenario_s25_34/on_single_task/expected_ticks.json
a011b02cf18ee04ced27fdac67946420  mpb/on/scenario_s25_36/on_single_task/expected_ticks.json
304dccbe76333a58f8528c389c8379d7  mpb/on/scenario_s25_38/on_single_task/expected_ticks.json
1012e01332f6e7b495d47fe4e7cf0056  mpb/on/scenario_s25_40/on_single_task/expected_ticks.json
744b2fe62e74be09b516a54bda64ec7a  mpb/on/scenario_s25_42/on_single_task/expected_ticks.json
285d5fb499ef4b43819a8e7a52b46227  mpb/on/scenario_s25_44/on_single_task/expected_ticks.json
fe4c50777593570ac98cd93d1805c138  mpb/on/scenario_s25_46/on_single_task/expected_ticks.json
285d5fb499ef4b43819a8e7a52b46227  mpb/on/scenario_s25_48/on_single_task/expected_ticks.json
548ecbbd149dd923e24c900a299ef8f6  mpb/on/scenario_s25_50/on_single_task/expected_ticks.json
190fc0d1de232c44a6cb7c5109ced1dd  mpb/on/scenario_s25_52/on_single_task/expected_ticks.json
37ab2722d4ff57cb92bd211a704a2090  mpb/on/scenario_s26_02/on_single_task/expected_ticks.json
fd462b2392867c812742bd134420cfae  mpb/on/scenario_s26_04/on_single_task/expected_ticks.json
60b553dcb6ee5da475a6e420d050de1f  mpb/on/scenario_s26_06/on_single_task/expected_ticks.json
8c5ae5c81a558df029b64250f8827400  mpb/on/scenario_s26_08/on_single_task/expected_ticks.json
2b48c1b8b1f2a1651bd07ce5dabfc164  mpb/on/scenario_s26_10/on_single_task/expected_ticks.json
a4942d73ee26ed1aa0b0e5c246142477  mpb/on/scenario_s26_12/on_single_task/expected_ticks.json
ec785a226faa0ccdf03364f0090c4530  mpb/on/scenario_s26_14/on_single_task/expected_ticks.json
a78c1362de1d8e5bbd88c9a2599cb276  mpb/on/scenario_s26_16/on_single_task/expected_ticks.json
887432e7addf7c8d83a9d202f1d42897  mpb/on/scenario_s26_18/on_single_task/expected_ticks.json
b4d1cba40c35cee78f3ef35abea152c8  mpb/on/scenario_s26_20/on_single_task/expected_ticks.json
02afc76dd28cc4f623249d6acfe249d6  mpb/on/scenario_s26_22/on_single_task/expected_ticks.json
6a912b6375af6036685c2a5dcc87f41f  mpb/on/scenario_s26_24/on_single_task/expected_ticks.json
30b382b22c6b59cb7bcf10a9f0359af4  mpb/on/scenario_s26_26/on_single_task/expected_ticks.json
21c597feff131361f329339882cf5dac  mpb/on/scenario_s26_28/on_single_task/expected_ticks.json
af81a2de920f006c3b8574f3ecd43fc4  mpb/on/scenario_s26_30/on_single_task/expected_ticks.json
29eb4b1ec77aed5c91a9f9e77748a580  mpb/on/scenario_s26_32/on_single_task/expected_ticks.json
e93a19d56cdc1a34e4323e07c2e7f5aa  mpb/on/scenario_s26_34/on_single_task/expected_ticks.json
2fb4ad9d96afc7ddd4b27de9bf6896fb  mpb/on/scenario_s26_36/on_single_task/expected_ticks.json
4abbb5e5856e0f7da3e405c77fe88a4c  mpb/on/scenario_s26_38/on_single_task/expected_ticks.json
c6d418b7ab38810299d31b9a15823df4  mpb/on/scenario_s26_40/on_single_task/expected_ticks.json
90d4ca3337bdb876c9946ab576b037b5  mpb/on/scenario_s26_42/on_single_task/expected_ticks.json
6088296e418a09a04905e5ff189dcb31  mpb/on/scenario_s26_44/on_single_task/expected_ticks.json
b25d14c8aa8336f52d1c7339a679f888  mpb/on/scenario_s26_46/on_single_task/expected_ticks.json
90a527a0b5aab306478ec475d60118c4  mpb/on/scenario_s26_48/on_single_task/expected_ticks.json
32b6512ef50c5e4d705284f42a0b2a06  mpb/on/scenario_s26_50/on_single_task/expected_ticks.json
abf68414bbd484c4e41311013d441ebf  mpb/on/scenario_s26_52/on_single_task/expected_ticks.json
b07da216396d651e200502a2323c9a08  mpb/on/scenario_s27_02/on_single_task/expected_ticks.json
b6d69b761b3142410dd8c9f9479fb8de  mpb/on/scenario_s27_04/on_single_task/expected_ticks.json
aeccb07d92f79853e0f3f5aab72d3b8c  mpb/on/scenario_s27_06/on_single_task/expected_ticks.json
9c761f8cbeb19be173c7fb3dafcf6b40  mpb/on/scenario_s27_08/on_single_task/expected_ticks.json
73a8af98f10e0cae61e582322f928d81  mpb/on/scenario_s27_10/on_single_task/expected_ticks.json
13eeb460448b0ac4c2b60b170416b2db  mpb/on/scenario_s27_12/on_single_task/expected_ticks.json
34b41d394069f8b81ee466243b78381f  mpb/on/scenario_s27_14/on_single_task/expected_ticks.json
6e7cd7ef24e0ee183795c38d25b49b0b  mpb/on/scenario_s27_16/on_single_task/expected_ticks.json
360342effe13da721862f5e05a19157c  mpb/on/scenario_s27_18/on_single_task/expected_ticks.json
9df290842b5e1dd770f92dc6aed59f99  mpb/on/scenario_s27_20/on_single_task/expected_ticks.json
c19c8ee72d32e5314711a5bd3ea6a1a1  mpb/on/scenario_s27_22/on_single_task/expected_ticks.json
7c868eb85c658256583cfff6ef47aad5  mpb/on/scenario_s27_24/on_single_task/expected_ticks.json
1f229a0ae2f52036145da48df56542c1  mpb/on/scenario_s27_26/on_single_task/expected_ticks.json
6cc18d4088e753255d452a55ef754005  mpb/on/scenario_s27_28/on_single_task/expected_ticks.json
cd3ab90167c14e75603b5b7c1e0a8b4b  mpb/on/scenario_s27_30/on_single_task/expected_ticks.json
cd3ab90167c14e75603b5b7c1e0a8b4b  mpb/on/scenario_s27_32/on_single_task/expected_ticks.json
13220f7510970476c7b623529290a6c9  mpb/on/scenario_s27_34/on_single_task/expected_ticks.json
0f946cb54c06ad3707bfda422c96c7ef  mpb/on/scenario_s27_36/on_single_task/expected_ticks.json
b11e6112785c15b2ba22465a84b00214  mpb/on/scenario_s27_38/on_single_task/expected_ticks.json
a6f36f45de2df177d3478211b41b812e  mpb/on/scenario_s27_40/on_single_task/expected_ticks.json
0563d2572a3b59100f084f453f5e775a  mpb/on/scenario_s27_42/on_single_task/expected_ticks.json
4ff85e6540ad0004aa5a5cc07ebbe1d2  mpb/on/scenario_s27_44/on_single_task/expected_ticks.json
db303f53f99f32973ce609feffa5c5a1  mpb/on/scenario_s27_46/on_single_task/expected_ticks.json
8bdb57a5315b620c939f849551502f3a  mpb/on/scenario_s27_48/on_single_task/expected_ticks.json
e21113df52d1a572441af357f2a50d57  mpb/on/scenario_s28_02/on_single_task/expected_ticks.json
cc1997d0964f230f97b6be065f578647  mpb/on/scenario_s28_04/on_single_task/expected_ticks.json
4d0d6bcc53637a9080d933de5ea56ebf  mpb/on/scenario_s28_06/on_single_task/expected_ticks.json
ebd1617af6529ad3307fc7f677792b72  mpb/on/scenario_s28_08/on_single_task/expected_ticks.json
269c5d18b4386d82628c9a633180f16f  mpb/on/scenario_s28_10/on_single_task/expected_ticks.json
94130baa8cdb06f6bd976049c675c58b  mpb/on/scenario_s28_12/on_single_task/expected_ticks.json
269c5d18b4386d82628c9a633180f16f  mpb/on/scenario_s28_14/on_single_task/expected_ticks.json
e0618172d27ee9fc71b4739bc86c3b65  mpb/on/scenario_s28_16/on_single_task/expected_ticks.json
0b041fee07d99f9328f40ab4cc1d3597  mpb/on/scenario_s28_18/on_single_task/expected_ticks.json
d72b579694308aaaaf985bded47634b2  mpb/on/scenario_s28_20/on_single_task/expected_ticks.json
b70bffadf790fb763e593b0804eda26a  mpb/on/scenario_s28_22/on_single_task/expected_ticks.json
a924791271256629311fde78ac5d6851  mpb/on/scenario_s28_24/on_single_task/expected_ticks.json
c1c717509b5df248733b9759920df370  mpb/on/scenario_s28_26/on_single_task/expected_ticks.json
9e87f06c4fb32a7260d2840ee7d50958  mpb/on/scenario_s28_28/on_single_task/expected_ticks.json
d19344be44fd940c5adbe49ae9c50ff5  mpb/on/scenario_s28_30/on_single_task/expected_ticks.json
e9c53166fba605acd5d80f81a2cd4aa3  mpb/on/scenario_s28_32/on_single_task/expected_ticks.json
939b873550b01059ecc5053fc3a3fad4  mpb/on/scenario_s28_34/on_single_task/expected_ticks.json
faf4ea0e3e04c3ee4ccdea96dc5ce6ab  mpb/on/scenario_s28_36/on_single_task/expected_ticks.json
1f12c0e5b00b1a8648ad51f6a32a88dc  mpb/on/scenario_s28_38/on_single_task/expected_ticks.json
8f684c6aa30bc7fbae90d900508a0caf  mpb/on/scenario_s28_40/on_single_task/expected_ticks.json
307cd9320f7731dcc1009608c2b845cf  mpb/on/scenario_s28_42/on_single_task/expected_ticks.json
c75c6ee3d0fe975ea682b54f55b8fae2  mpb/on/scenario_s28_44/on_single_task/expected_ticks.json
f6335a025e8aea21d3ddda73bae5567f  mpb/on/scenario_s28_46/on_single_task/expected_ticks.json
11080bc1189bc7c01d2b023b239e9851  mpb/on/scenario_s28_48/on_single_task/expected_ticks.json
9564b5432166fc9264518a685d9fad3d  mpb/on/scenario_s29_02/on_single_task/expected_ticks.json
434b64d9b125f5c22e5fb525880dd503  mpb/on/scenario_s29_04/on_single_task/expected_ticks.json
6d4b13202ab91ed92c78aac339673c39  mpb/on/scenario_s29_06/on_single_task/expected_ticks.json
a9734f35f33a4f6896b3f83262e148be  mpb/on/scenario_s29_08/on_single_task/expected_ticks.json
4c96e297ae912d21c60ab13554d189dd  mpb/on/scenario_s29_10/on_single_task/expected_ticks.json
4c96e297ae912d21c60ab13554d189dd  mpb/on/scenario_s29_12/on_single_task/expected_ticks.json
7aa0522f82ecccabc468ba30cdbcfc4c  mpb/on/scenario_s29_14/on_single_task/expected_ticks.json
0334d547895bbab4d4e82bea4f09defc  mpb/on/scenario_s29_16/on_single_task/expected_ticks.json
2b3e84cc34e7dfb303fd822f35bb32ab  mpb/on/scenario_s29_18/on_single_task/expected_ticks.json
d3e06afd4deae3a706237cb3542927b6  mpb/on/scenario_s29_20/on_single_task/expected_ticks.json
543b8c0fcfc3a5d43c4a479112324294  mpb/on/scenario_s29_22/on_single_task/expected_ticks.json
8064b83d80df10dcc79fdab3e7890f84  mpb/on/scenario_s29_24/on_single_task/expected_ticks.json
93bb4555517123903b241b97095c19e5  mpb/on/scenario_s29_26/on_single_task/expected_ticks.json
49d73bdfbb6d1158a4ba59db1c0eb091  mpb/on/scenario_s29_28/on_single_task/expected_ticks.json
52ee5fdc81636d538811abe4e1e9374c  mpb/on/scenario_s29_30/on_single_task/expected_ticks.json
00691e314fe8e1c031b0dad855f5e20d  mpb/on/scenario_s29_32/on_single_task/expected_ticks.json
cab3a9a552ed30e6647b7abb41548757  mpb/on/scenario_s29_34/on_single_task/expected_ticks.json
189b8bdfcab31108f15a8ad52e00ed90  mpb/on/scenario_s29_36/on_single_task/expected_ticks.json
cc493687aabad9ca64d80cbb3a2cf843  mpb/on/scenario_s29_38/on_single_task/expected_ticks.json
68a183453548eab0a04382e657981cf5  mpb/on/scenario_s29_40/on_single_task/expected_ticks.json
fd79a60c2c148ed32a96dc9c09208472  mpb/on/scenario_s29_42/on_single_task/expected_ticks.json
d3b3e99a2049dbee64fd25bc058b7dc9  mpb/on/scenario_s29_44/on_single_task/expected_ticks.json
ddb7e6c606bdb891626c17a3138ad1af  mpb/on/scenario_s29_46/on_single_task/expected_ticks.json
8cf70e112622ec12e1973981d64f9b59  mpb/on/scenario_s29_48/on_single_task/expected_ticks.json
77b1e9801ae60c08e7ea23dce33b5f2d  mpb/on/scenario_s29_50/on_single_task/expected_ticks.json
9f6b9cb5ac862604c24996382abfe736  mpb/on/scenario_s30_02/on_single_task/expected_ticks.json
e9effaf0ccc6a92fe8f60e1ee7b9a165  mpb/on/scenario_s30_04/on_single_task/expected_ticks.json
ca936b0ecd5bdc3d8f668aec7a43f72f  mpb/on/scenario_s30_06/on_single_task/expected_ticks.json
45f2986fdb0eea1accdb701c9a382279  mpb/on/scenario_s30_08/on_single_task/expected_ticks.json
90ba9bbff50dc3bb59ff37fa4dc13cfd  mpb/on/scenario_s30_10/on_single_task/expected_ticks.json
800f636d9710b86fd765b8fca8e5a2ae  mpb/on/scenario_s30_12/on_single_task/expected_ticks.json
90ba9bbff50dc3bb59ff37fa4dc13cfd  mpb/on/scenario_s30_14/on_single_task/expected_ticks.json
e362d8519fe85a371b5541142abd45d1  mpb/on/scenario_s30_16/on_single_task/expected_ticks.json
6dec0707324fc84bc35c3b3587f26085  mpb/on/scenario_s30_18/on_single_task/expected_ticks.json
6ac929603a9aadb097fa6b18a86a7706  mpb/on/scenario_s30_20/on_single_task/expected_ticks.json
c6f214e9847aa0289015c7fb2708a85b  mpb/on/scenario_s30_22/on_single_task/expected_ticks.json
c2e7b314c24f1cff5ad43387f6cfd380  mpb/on/scenario_s30_24/on_single_task/expected_ticks.json
c6f214e9847aa0289015c7fb2708a85b  mpb/on/scenario_s30_26/on_single_task/expected_ticks.json
500f81dfe74f7216692b861eb8171b63  mpb/on/scenario_s30_28/on_single_task/expected_ticks.json
008c0708b0ba2d50a2f8b50c7c4ea0aa  mpb/on/scenario_s30_30/on_single_task/expected_ticks.json
500f81dfe74f7216692b861eb8171b63  mpb/on/scenario_s30_32/on_single_task/expected_ticks.json
ae1e382ff89a11db3a87cad20d5406e9  mpb/on/scenario_s30_34/on_single_task/expected_ticks.json
3e5f3077bbd8e413883aa810a4121796  mpb/on/scenario_s30_36/on_single_task/expected_ticks.json
44288eea35ac21fa514fbafe66046790  mpb/on/scenario_s30_38/on_single_task/expected_ticks.json
0b50823717bf0ac5a7fecf428f2d6e55  mpb/on/scenario_s30_40/on_single_task/expected_ticks.json
67f722567210c568a05d3d661d592742  mpb/on/scenario_s30_42/on_single_task/expected_ticks.json
7951dc92d5518c82e497497d0e4f5c54  mpb/on/scenario_s30_44/on_single_task/expected_ticks.json
5f36fc4b77111f602158b1958dcec04f  mpb/on/scenario_s30_46/on_single_task/expected_ticks.json
7d0356f6c85fb9337da91a9794c1b2d1  mpb/on/scenario_s30_48/on_single_task/expected_ticks.json
149c96ba1baafb29035ac4b96c99727b  mpb/on/scenario_s30_50/on_single_task/expected_ticks.json
```

### mpb, off (106)

```
85c62c7691b9e56e8fa8ec2171518f82  mpb/off/scenario_s02_01/on_single_task/expected_ticks.json
6604e8b3c1223471ebfe0a153849a30f  mpb/off/scenario_s02_02/on_single_task/expected_ticks.json
97671dfaf2bd3009b0b6d3016f8ed2fa  mpb/off/scenario_s03_06/on_single_task/expected_ticks.json
a060fe3b8169d51730d1daab3a968dfe  mpb/off/scenario_s04_01/on_single_task/expected_ticks.json
dd415c09c8a53b75eb26eda179c73eba  mpb/off/scenario_s05_01/on_single_task/expected_ticks.json
e321e1e048c75e842a43ecab180d928f  mpb/off/scenario_s05_02/on_single_task/expected_ticks.json
6c5ac6b1a50e3db99c555c61fb81b560  mpb/off/scenario_s17_12/on_single_task/expected_ticks.json
aaa0a23776a0dc3a76dc95fc59da1b7f  mpb/off/scenario_s17_18/on_single_task/expected_ticks.json
02cb9bb1c7817ffa919f1507ebccc7e2  mpb/off/scenario_s17_24/on_single_task/expected_ticks.json
f79cef9c9688bf42f1dd61d3f96cd399  mpb/off/scenario_s17_30/on_single_task/expected_ticks.json
7a2cf4e258c184bdc4c4e29717f9b997  mpb/off/scenario_s17_36/on_single_task/expected_ticks.json
7368fc3fa65880d3659fb2153aca5926  mpb/off/scenario_s18_02/on_single_task/expected_ticks.json
f0c773f30f4e3b3e92ababb85a1df583  mpb/off/scenario_s18_08/on_single_task/expected_ticks.json
c5656dbaa6f6e7f461bfc734721ea9f7  mpb/off/scenario_s18_14/on_single_task/expected_ticks.json
9f6f522fe13fe8b1b8639ea3e8bc3e1c  mpb/off/scenario_s18_20/on_single_task/expected_ticks.json
f2f3ecd2ebdafd4381854fa84c6ab408  mpb/off/scenario_s18_26/on_single_task/expected_ticks.json
5fc953b7467c86732ca622ba95ab0419  mpb/off/scenario_s19_07/on_single_task/expected_ticks.json
feac7ea6fb290d25298ea591e8e7545a  mpb/off/scenario_s19_13/on_single_task/expected_ticks.json
175b08f799f117e4a2a8156f87b152de  mpb/off/scenario_s19_19/on_single_task/expected_ticks.json
a9ed620ce1dd1c09aa8f75b12154e2de  mpb/off/scenario_s19_25/on_single_task/expected_ticks.json
65667761de88e370ec8e22af5cc471ee  mpb/off/scenario_s19_31/on_single_task/expected_ticks.json
8f8a0d7b407fcaea3ef28d6a84218855  mpb/off/scenario_s20_02/on_single_task/expected_ticks.json
45ceb21c6ba36e0dc1886466659333c3  mpb/off/scenario_s20_08/on_single_task/expected_ticks.json
19eeea03db0c16a068bfb237e3eab560  mpb/off/scenario_s20_14/on_single_task/expected_ticks.json
ebc3fc10650f8088e4052e9f5311a624  mpb/off/scenario_s20_20/on_single_task/expected_ticks.json
c56a12dd9fe15bfb6ae929d2e6c0e80d  mpb/off/scenario_s20_26/on_single_task/expected_ticks.json
d798d27ba3961d3c405f8d03639ee43e  mpb/off/scenario_s21_07/on_single_task/expected_ticks.json
fa29616972ff09280b7d7cee11ab9f38  mpb/off/scenario_s21_11/on_single_task/expected_ticks.json
33ac15b9a5637f7ccdef1ed9f9af4a88  mpb/off/scenario_s21_17/on_single_task/expected_ticks.json
803135d3db3bd0f8a9777fa91ea5067d  mpb/off/scenario_s21_23/on_single_task/expected_ticks.json
4f40f0bd60cfc4ca5827d3a905bf8343  mpb/off/scenario_s21_29/on_single_task/expected_ticks.json
24762aae27363bfc9f20d4d3d9ed8c01  mpb/off/scenario_s22_02/on_single_task/expected_ticks.json
9e65c122c7dee2d50c91ebb1b0cf7d67  mpb/off/scenario_s22_06/on_single_task/expected_ticks.json
d3330056856bad48aeb536fe3f60a2bd  mpb/off/scenario_s22_12/on_single_task/expected_ticks.json
0deecdddcb37cc76f390eaa3f48b0766  mpb/off/scenario_s22_18/on_single_task/expected_ticks.json
9cf6d1dc1660fef9c4b583a7e9f49613  mpb/off/scenario_s22_24/on_single_task/expected_ticks.json
6df0bfffae902de5d9e28d1447b447c2  mpb/off/scenario_s23_09/on_single_task/expected_ticks.json
f50fd856126df1b06958068e29e1d6a2  mpb/off/scenario_s23_15/on_single_task/expected_ticks.json
7ef0490759c9f404fb2f31e8e8b738a9  mpb/off/scenario_s23_21/on_single_task/expected_ticks.json
6e05eae1a5998a7a2a3d0127a3cf27fe  mpb/off/scenario_s23_27/on_single_task/expected_ticks.json
f7385a2f28a0b2b9272bc8da0702b390  mpb/off/scenario_s23_31/on_single_task/expected_ticks.json
895b6a3142e2ff446df8fee1a01d158a  mpb/off/scenario_s24_02/on_single_task/expected_ticks.json
edeabea8ce156412f76f89cb49831fd6  mpb/off/scenario_s24_08/on_single_task/expected_ticks.json
10a71c713fb16c906a2f7b4468d6e945  mpb/off/scenario_s24_14/on_single_task/expected_ticks.json
f8f1b42328a8e89be3f35cb07d3ed637  mpb/off/scenario_s24_20/on_single_task/expected_ticks.json
5de6dbbd35818d1b23d2283151a319a7  mpb/off/scenario_s24_26/on_single_task/expected_ticks.json
c2ebd5c47b3a9081260455b957bc1aa5  mpb/off/scenario_s25_02/on_single_task/expected_ticks.json
67d1b0fc5f4cdadf58df8d2c43e277ad  mpb/off/scenario_s25_06/on_single_task/expected_ticks.json
ab8144c82ab3df53cab8aa2acbb3556f  mpb/off/scenario_s25_10/on_single_task/expected_ticks.json
5970b99c2f9ce548b861dd0b5679c150  mpb/off/scenario_s25_16/on_single_task/expected_ticks.json
e74e6be079256790a060eb304a75859c  mpb/off/scenario_s25_22/on_single_task/expected_ticks.json
26f70c05bdf9615ac0a79c7160a532c7  mpb/off/scenario_s25_28/on_single_task/expected_ticks.json
ce195a59ace5e7ecf00b79c90aa908c1  mpb/off/scenario_s25_34/on_single_task/expected_ticks.json
44a5116b6145d04feeee7d1f1713ba58  mpb/off/scenario_s25_40/on_single_task/expected_ticks.json
373b173449cdd012147cf1e851423d77  mpb/off/scenario_s25_44/on_single_task/expected_ticks.json
ae336a253972f5114af4726a80682e48  mpb/off/scenario_s25_50/on_single_task/expected_ticks.json
82e76e87a63cf32608f0697f9397ae19  mpb/off/scenario_s26_02/on_single_task/expected_ticks.json
e4eefb609aaacadcab2dee37890b0dfc  mpb/off/scenario_s26_06/on_single_task/expected_ticks.json
a83697a0de6d701d38455151b1b870b1  mpb/off/scenario_s26_10/on_single_task/expected_ticks.json
24d87dbd117e15546e802934e4b054e2  mpb/off/scenario_s26_16/on_single_task/expected_ticks.json
cfe4508bccc14c7abf1a3d3f99cbc993  mpb/off/scenario_s26_22/on_single_task/expected_ticks.json
63a8c01ac9c8cece86a921ccf4495c87  mpb/off/scenario_s26_28/on_single_task/expected_ticks.json
d62cadf7ae325ce02c5314291c38fb01  mpb/off/scenario_s26_32/on_single_task/expected_ticks.json
02003f8035f631f499141f3e4afa0adb  mpb/off/scenario_s26_38/on_single_task/expected_ticks.json
ab3a970c8591dc4ce6bde9110c265603  mpb/off/scenario_s26_42/on_single_task/expected_ticks.json
c4b8e80a23edb85d597ad0bb0108e2f7  mpb/off/scenario_s26_48/on_single_task/expected_ticks.json
2ff6dc0fdc9c51ae824d429cc1e10e69  mpb/off/scenario_s27_02/on_single_task/expected_ticks.json
fe3a1dfd36ffefe68439aea5f18acaf3  mpb/off/scenario_s27_06/on_single_task/expected_ticks.json
c088f5adc1b6534994e6cbb58467868b  mpb/off/scenario_s27_10/on_single_task/expected_ticks.json
98820cddc9d52f97189394bbb26f47df  mpb/off/scenario_s27_14/on_single_task/expected_ticks.json
5c9b790cfc926d93624af38903070b1f  mpb/off/scenario_s27_20/on_single_task/expected_ticks.json
277adeb0f79a95a777f045f3dddbb0c4  mpb/off/scenario_s27_26/on_single_task/expected_ticks.json
a2051f7bb1312134bd54fd4408749db3  mpb/off/scenario_s27_30/on_single_task/expected_ticks.json
7ed9b5dc79f5ec233fb4d85dbc9b1fa7  mpb/off/scenario_s27_36/on_single_task/expected_ticks.json
0e66bfc03d6a72d07fba1010a2c63425  mpb/off/scenario_s27_42/on_single_task/expected_ticks.json
35bbe7c22c3a90114405ba74201d817a  mpb/off/scenario_s27_44/on_single_task/expected_ticks.json
da748769977ead5ad0a163cb95adeac8  mpb/off/scenario_s28_02/on_single_task/expected_ticks.json
f4ff15a6fba41c29fcbd6da58684aa3d  mpb/off/scenario_s28_06/on_single_task/expected_ticks.json
ff980012a964298190e4c1e6152cccd4  mpb/off/scenario_s28_10/on_single_task/expected_ticks.json
64bc0c2bb736db5319c4020b2ebb4e17  mpb/off/scenario_s28_16/on_single_task/expected_ticks.json
bb0b3206d0d85d0cc31f3eda4aa29ad1  mpb/off/scenario_s28_22/on_single_task/expected_ticks.json
c8bcdc15f2cc957fdde68313e116bca1  mpb/off/scenario_s28_28/on_single_task/expected_ticks.json
56e0d4a5fbd40a09823ae5dc853c1d71  mpb/off/scenario_s28_32/on_single_task/expected_ticks.json
6d0a567ca445b6a45da368d5b4234ed6  mpb/off/scenario_s28_38/on_single_task/expected_ticks.json
4c5afa730ebe43a22466e60fea408371  mpb/off/scenario_s28_42/on_single_task/expected_ticks.json
58e2bec07a6b1cf9b33955d7a4140653  mpb/off/scenario_s28_48/on_single_task/expected_ticks.json
268ff0d49054c9add83cca534e768f86  mpb/off/scenario_s29_02/on_single_task/expected_ticks.json
acd38c2c3f5345713312db84637d8599  mpb/off/scenario_s29_06/on_single_task/expected_ticks.json
f7b5d9cd83c83a087c48be1c770205f8  mpb/off/scenario_s29_10/on_single_task/expected_ticks.json
3ce27ee7e6222b6b6e3b4975c5809d42  mpb/off/scenario_s29_16/on_single_task/expected_ticks.json
7db1efb89eb8faaa5715cbe83f5a5df5  mpb/off/scenario_s29_22/on_single_task/expected_ticks.json
d6bf7cb4f52128593eef4a1f4d92ba01  mpb/off/scenario_s29_28/on_single_task/expected_ticks.json
ace6987b65113069ae91ac37ab133c51  mpb/off/scenario_s29_34/on_single_task/expected_ticks.json
01f5289e1b3e0cb998e898c696e59bf9  mpb/off/scenario_s29_40/on_single_task/expected_ticks.json
b776fd6f83b4a0e3657df241c9d22d28  mpb/off/scenario_s29_44/on_single_task/expected_ticks.json
358bc6be91ec6846cfe4b3f78a3153c2  mpb/off/scenario_s29_48/on_single_task/expected_ticks.json
efb0b333fb880b2228644a73f4b3f242  mpb/off/scenario_s30_02/on_single_task/expected_ticks.json
ba8b77ed1c217830a8a18f434da476ba  mpb/off/scenario_s30_06/on_single_task/expected_ticks.json
c4d0b691da8dac61eaab606d41619f48  mpb/off/scenario_s30_10/on_single_task/expected_ticks.json
d41fb9df8abb66d0e4b04686f4fce2b7  mpb/off/scenario_s30_16/on_single_task/expected_ticks.json
c0609c029f0e77799a9f6953bf1a0879  mpb/off/scenario_s30_22/on_single_task/expected_ticks.json
08348bfc7127cbe5a41eb8f2b813eb3a  mpb/off/scenario_s30_28/on_single_task/expected_ticks.json
10401687427b21c198173866fb5edbb7  mpb/off/scenario_s30_34/on_single_task/expected_ticks.json
f94de4cf4f3101003b898cda56dccffc  mpb/off/scenario_s30_38/on_single_task/expected_ticks.json
9aac8d465a4249cadad0caf37ec96ea5  mpb/off/scenario_s30_42/on_single_task/expected_ticks.json
09c91501419c7f1ccba216518c479444  mpb/off/scenario_s30_46/on_single_task/expected_ticks.json
```

## After the runs (5 October 2026): the oracle's `recent` fix and the 33 changed expectation tables

The recognition oracle's `recent` column was empty on ticks with no live hypothesis, though its memory held the completion (the recognizer reports it there): 9 runs showed it as their only disagreement. Fixed in `analysis/instruments/irb/oracle.py` (REPORT.md, "What was run"). The committed oracle reproduces every table committed above; the fixed one changes only `recent` on those ticks, in these 33 tables (their md5 after the fix; all other 351 recognition and all 388 planning tables are as committed):

```
12424ad652cb06e36edf7b17bc78ec16  irb/on/scenario_s21_01/expected.csv
04bd95c4eb05b38da7da46d217c2938a  irb/on/scenario_s21_02/expected.csv
d0c38a15553e5714ca78c6f8fcc7d39c  irb/on/scenario_s21_04/expected.csv
4be6c6addd5ec16eaa77a86a11bd446c  irb/on/scenario_s22_05/expected.csv
5fd6c55fc621d55f41f35390d160fbe5  irb/on/scenario_s22_07/expected.csv
f42089016a7e0eeec5f7809ef61a35f5  irb/on/scenario_s22_09/expected.csv
571a402302de8a0c95e2d4347a9305df  irb/on/scenario_s22_17/expected.csv
f2fb5ae44666a20003f4afaebc4969f2  irb/on/scenario_s22_19/expected.csv
b9c1dc2dcfb438f58d89481186969c9d  irb/on/scenario_s22_21/expected.csv
76eed4fb8a768fd48240a3d6472e9577  irb/on/scenario_s25_27/expected.csv
0dcf03b0ef8a35638c79e290771ea6db  irb/on/scenario_s25_29/expected.csv
1cee95dba8fa6fcd8743a3a67425c8a8  irb/on/scenario_s25_31/expected.csv
4ca2b326d9035e4fffaec7e7a45b9ad6  irb/on/scenario_s25_33/expected.csv
abb7e1c8302b52cf1c9c8a32ab4dfd46  irb/on/scenario_s25_35/expected.csv
ebc8a19d8a4ba28f03a36dc9dae45947  irb/on/scenario_s25_37/expected.csv
44c769ca66a27751591cb2712196ef16  irb/on/scenario_s26_47/expected.csv
0dcaf20a17ef7b062da489e1d9451521  irb/on/scenario_s26_49/expected.csv
356ea66532fb6b60d9b05c19488304c7  irb/on/scenario_s26_51/expected.csv
8a1296cba65700c3b7adb66095e57bd5  irb/on/scenario_s27_29/expected.csv
7eb0bd35c1a69f855a59cc3a893ef240  irb/on/scenario_s27_31/expected.csv
63473c5ef6f9bf2633ab4c6a7148ffa1  irb/on/scenario_s27_33/expected.csv
801d4f55d4cefa96549744c9efb62e2e  irb/on/scenario_s27_43/expected.csv
9c52bfd4bf0b5c51e7d7131f4155b25f  irb/on/scenario_s27_45/expected.csv
9a90ebdfa19f8368a1baad4da4ef22af  irb/on/scenario_s27_47/expected.csv
823725b11012683753d680ca41fafd2e  irb/on/scenario_s28_31/expected.csv
67221b05579153e6a09a19c2dd0d50c5  irb/on/scenario_s28_33/expected.csv
12d1961902c542340cdc6b9418937340  irb/on/scenario_s28_35/expected.csv
545345958b025bbdb1bfde72a513f0ba  irb/on/scenario_s29_09/expected.csv
b7832669601ff1c20a4164ec19870d5d  irb/on/scenario_s29_11/expected.csv
95f56c01404573368869bae6fe0542aa  irb/on/scenario_s29_13/expected.csv
2d75165cfdfaba781dc89ff5e59e3062  irb/on/scenario_s30_27/expected.csv
1024964a6db6d0189450b68bbf60879b  irb/on/scenario_s30_29/expected.csv
2d75165cfdfaba781dc89ff5e59e3062  irb/on/scenario_s30_31/expected.csv
```

Results: REPORT.md; the comparison: `comp5e.py` (run from the repository root). The per-run outputs stay untracked under `irb/{on,off}/` and `mpb/{on,off}/` (logs and `.rec` in each `runs/`).
