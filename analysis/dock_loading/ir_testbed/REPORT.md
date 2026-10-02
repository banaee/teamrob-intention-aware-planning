# The IR test-bed on dock_loading: report

The set, its rules and its artefacts: `README.md`. The instrument: `analysis/instruments/ir_testbed/` (rules 1 to 23 in
`analysis/kitting/ir_testbed/README.md`, 24 to 27 in the instrument's README). The expectations were committed before
any run of the set (54edb71): `trajectory.json`, `expected.csv`, `phases.json` per scenario and `predictions.md`.

The report distinguishes "the recognizer currently behaves this way" from "this behaviour is correct by the current
design". Agreement below means the recognizer's public outputs equal the values derived from the records; the
observations at the end describe what both show and rule nothing.

## Controlled (C1 to C14; 42 runs, 1 October 2026)

How it was read: `run.sh dock_loading` on the 42 controlled run files, prior on. Per run:
- the trajectory equals the run's human lines on every tick (position, action, micro);
- the run's own oracle call reproduced the committed `trajectory.json`, `expected.csv` and `phases.json` byte for byte,
  θ read from the run's [run] header (0.75, the value of record used before the runs);
- the in-process `[IR*]` lines are byte-identical to the logged run's;
- `diff.md`: categorical values exactly, numeric values at relative tolerance 1e-9 against `actual.csv` and at half a
  printed unit against `actual_log.csv`.

Result: **42 of 42 agree; 0 disagreements, 0 unmatched rows, in every room.** No disagreement to classify.

Per row and room, from each scenario's `summary.md` (actual; equal to the expected values): each stretch of ticks on
which a hypothesis is the truth, and its first tick with belief ≥ θ (— not reached; scan n is
`confirm_delivered_pallet(pallet_n)`; an unmodelled task has no stretch).

| row | env_layout_02 (s02) | env_layout_03 (s04) | env_layout_04 (s06) |
|---|---|---|---|
| C1 (_02) | scan 0 0–29: 10; scan 2 30–82: 80 | scan 0 0–29: 14; scan 2 30–83: 54 | scan 0 0–18: —; scan 2 19–38: — |
| C2 (_03) | scan 2 0–29: 25; scan 0 30–82: 58 | scan 2 0–27: 8; scan 0 28–81: 62 | scan 2 0–27: 21; scan 0 28–46: — |
| C3 (_04) | scan 0 0–29: —; scan 1 30–32: — | scan 0 0–29: —; scan 1 30–32: — | scan 0 0–18: —; scan 1 19–21: — |
| C4 (_05) | scan 0 0–29: —; scan 2 30–82: —; scan 1 83–135: 111; scan 3 136–188: 186 | scan 0 0–29: —; scan 2 30–83: —; scan 1 84–137: 118; scan 3 138–191: 162 | scan 0 0–18: —; scan 2 19–38: —; scan 1 39–57: —; scan 3 58–76: — |
| C5 (_06) | scan 0 0–29: 10; coffee 30–111: 79; scan 2 112–122: — | scan 0 0–29: 14; coffee 30–82: 43; scan 2 83–131: 102 | scan 0 0–18: —; coffee 19–72: 36; scan 2 73–85: 83 |
| C6 (_07) | scan 0 0–29: 10; office 30–109: 63; scan 2 110–144: — | scan 0 0–29: 14; office 30–109: 60; scan 2 110–147: 124 | scan 0 0–18: —; office 19–85: 25; scan 2 86–125: 123 |
| C7 (_08) | scan 0 0–27: 10; coffee 28–109: 78; scan 0 110–162: 137; scan 2 163–215: 213 | scan 0 0–27: 14; coffee 28–80: 45; scan 0 81–104: 96; scan 2 105–158: 129 | scan 0 0–16: —; coffee 17–70: 38; scan 0 71–94: —; scan 2 95–113: — |
| C8 (_09) | scan 0 0–13: 10; coffee 14–82: 51; scan 0 83–135: 109; scan 2 136–187: 185 | scan 0 0–13: —; coffee 14–62: 25; scan 0 63–87: 78; scan 2 88–141: 112 | scan 0 0–13: —; coffee 14–67: 34; scan 0 68–93: —; scan 2 94–112: — |
| C9 (_10) | scan 0 0–13: 10; scan 2 14–54: 45 | scan 0 0–13: —; scan 2 14–54: 35 | scan 0 0–13: —; scan 2 14–34: 24 |
| C10 (_11) | scan 0 0–13: 10; scan 2 14–54: 45; scan 0 55–106: 83 | scan 0 0–13: —; scan 2 14–54: 35; scan 0 55–108: 89 | scan 0 0–13: —; scan 2 14–34: 24; scan 0 35–54: — |
| C11 (_12) | scan 0 0–29: 10; scan 2 71–123: 117 | scan 0 0–29: 14; scan 2 71–124: 92 | scan 0 0–18: —; scan 2 60–79: 77 |
| C12 (_13) | scan 1 0–29: outside the support; scan 2 30–82: 80 | scan 1 0–29: outside the support; scan 2 30–83: 54 | scan 1 0–18: outside the support; scan 2 19–38: — |
| C13 (_14) | scan 0 0–29: 9 | scan 0 0–29: 14 | scan 0 0–18: 14 |
| C14 (_15) | scan 2 0–29: 25 | scan 2 0–27: 8 | scan 2 0–27: 21 |

The separation counts (`separation.md`): every count is 0 in the 42 runs (the robot stands on the gate's centre point;
the closest approach, 115.85 cm, is above min_separation), as predicted from the trajectories.

### The diagnostic rows C13 and C14 (the standby walk)

The present model's reading of the standby walk, actual (equal to the expectation written in `predictions.md` before
the runs). The scan of pallet_4 never entered the live set (`[IR-inapplicable] ... does not enter the live set`, A4)
and the record states it and the walk to the desk as open at the run's end, in all six runs.

| row | scenario (room) | walk | leader and gate, per stretch (actual) | finding (actual) | equals expected |
|---|---|---|---|---|---|
| C13 | scenario_s02_14 (env_layout_02) | 30–56 | 30–49 coffee_break(coffee_machine_0) none(below_theta); 50–70 coffee_break(coffee_machine_0) clears; 71–86 coffee_break(coffee_machine_0) none(leader_inadequate) | 30–70 adequate; 71–86 unexplained | yes |
| C13 | scenario_s04_14 (env_layout_03) | 30–56 | 30–45 office_break(office_chair) none(below_theta); 46–56 office_break(office_chair) clears; 57–86 office_break(office_chair) none(leader_inadequate) | 30–56 adequate; 57–86 unexplained | yes |
| C13 | scenario_s06_14 (env_layout_04) | 19–34 | 19–26 office_break(office_chair) none(below_theta); 27–64 coffee_break(coffee_machine_0) none(below_theta) | 19–35 adequate; 36–64 unexplained | yes |
| C14 | scenario_s02_15 (env_layout_02) | 30–56 | 30–37 office_break(office_chair) none(below_theta); 38–56 office_break(office_chair) clears; 57–86 office_break(office_chair) none(leader_inadequate) | 30–56 adequate; 57–86 unexplained | yes |
| C14 | scenario_s04_15 (env_layout_03) | 28–52 | 28–50 coffee_break(coffee_machine_0) none(below_theta); 51–66 coffee_break(coffee_machine_0) clears; 67–82 coffee_break(coffee_machine_0) none(leader_inadequate) | 28–66 adequate; 67–82 unexplained | yes |
| C14 | scenario_s06_15 (env_layout_04) | 28–52 | 28–36 office_break(office_chair) none(below_theta); 37–58 office_break(office_chair) clears; 59–82 office_break(office_chair) none(leader_inadequate) | 28–58 adequate; 59–82 unexplained | yes |

Beside it, the predictions written before the runs (`predictions.md`; not compared): under H1 the walk is led by H1 at
zero excess, cleared within the walk and pinned on arrival; under H2 (no assigned task live) H2 is live from the scan's
pin, since scan 4 is never live, and reads the walk as H1 does. Under the present model the walk is read as
coffee_break or office_break by the room's bearings: cleared on observation warrant in five of the six runs (from 8 to
23 ticks into the walk), never above θ in scenario_s06_14; in every run the finding turns unexplained and the gate
refuses (`none(leader_inadequate)`) once the human stands at the standby place.

### Observations (both sides agree; stated, not ruled)

- C5 of the T-G entry is confirmed on dock_loading: two scans of one bay predict the same motion and divide the
  belief. In C3 (scan 0 then scan 1, both in the dry bay) neither reaches θ in any room, and in C4 the first two walks
  (scan 0 and scan 2, each with a same-bay rival) never reach θ; once one of a pair is retired the other does (C4,
  env_layout_02 and _03). The T-G entry returns this to the design chat as a finding about the mind within V1.
- In env_layout_04 the dry bay lies 16 steps from the standby place: on that first walk scan 0 does not reach θ in any
  row where it is the truth with three or more rivals live (C1, C3 to C11), and does in C13 (two rivals; tick 14). No true
  stretch reaches θ in C1, C3, C4 and C12 there.
- In env_layout_02 the walk from the dry bay to the frozen bay passes the coffee machine's direction; scan 2 reaches θ
  only near its arrival (C1 at 80 of 30–82; C12 likewise).
- The office door (C6): the human stops short of the door on the hall side and the hypotheses through the office
  change method with the human's area, with the predicted proximity regress at the door (scenario_s02_07, ticks 117 and
  118); agreement holds there.

## Mixed (M1 to M4; 12 runs, 2 October 2026)

Run after Hadi accepted the controlled section (2 October 2026), as the controlled runs were (same checks).

Result: **12 of 12 agree; 0 disagreements, 0 unmatched rows, in every room**; every trajectory equal to the run's human
lines; the committed expectations reproduced byte for byte. No disagreement to classify. The separation counts are 0.

Each mixed row read against the controlled rows it combines (M1: C7 and C6; M2: C10 and C5; M3: C11 and C8; M4: C12,
C6, C13 and C14): per true stretch its first tick at θ, as ticks from the stretch's start (the baseline table below;
"never": not within the stretch; "out": outside the support).

| row | room | the mixed run: true stretch (start) ticks to θ | the controlled rows it combines |
|---|---|---|---|
| M1 | env_layout_02 | scan 0 (0) 10; coffee (28) 50; scan 0 (110) 27; office (163) 34; scan 2 (242) never | C7: scan 0 (0) 10; coffee (28) 50; scan 0 (110) 27; scan 2 (163) 50 · C6: scan 0 (0) 10; office (30) 33; scan 2 (110) never |
| M1 | env_layout_03 | scan 0 (0) 14; coffee (28) 17; scan 0 (81) 15; office (105) 30; scan 2 (185) 13 | C7: scan 0 (0) 14; coffee (28) 17; scan 0 (81) 15; scan 2 (105) 24 · C6: scan 0 (0) 14; office (30) 30; scan 2 (110) 14 |
| M1 | env_layout_04 | scan 0 (0) never; coffee (17) 21; scan 0 (71) never; office (95) 6; scan 2 (163) 36 | C7: scan 0 (0) never; coffee (17) 21; scan 0 (71) never; scan 2 (95) never · C6: scan 0 (0) never; office (19) 6; scan 2 (86) 37 |
| M2 | env_layout_02 | scan 0 (0) 10; coffee (14) 37; scan 2 (83) never; scan 0 (94) 28 | C10: scan 0 (0) 10; scan 2 (14) 31; scan 0 (55) 28 · C5: scan 0 (0) 10; coffee (30) 49; scan 2 (112) never |
| M2 | env_layout_03 | scan 0 (0) never; coffee (14) 11; scan 2 (63) 19; scan 0 (111) 33 | C10: scan 0 (0) never; scan 2 (14) 21; scan 0 (55) 34 · C5: scan 0 (0) 14; coffee (30) 13; scan 2 (83) 19 |
| M2 | env_layout_04 | scan 0 (0) never; coffee (14) 20; scan 2 (68) never; scan 0 (81) never | C10: scan 0 (0) never; scan 2 (14) 10; scan 0 (35) never · C5: scan 0 (0) never; coffee (19) 17; scan 2 (73) 10 |
| M3 | env_layout_02 | scan 0 (0) 10; scan 2 (71) never; coffee (85) 33; scan 2 (153) never | C11: scan 0 (0) 10; scan 2 (71) 46 · C8: scan 0 (0) 10; coffee (14) 37; scan 0 (83) 26; scan 2 (136) 49 |
| M3 | env_layout_03 | scan 0 (0) 14; scan 2 (71) never; coffee (85) 13; scan 2 (137) 19 | C11: scan 0 (0) 14; scan 2 (71) 21 · C8: scan 0 (0) never; coffee (14) 11; scan 0 (63) 15; scan 2 (88) 24 |
| M3 | env_layout_04 | scan 0 (0) never; scan 2 (60) never; coffee (74) 7; scan 2 (118) 11 | C11: scan 0 (0) never; scan 2 (60) 17 · C8: scan 0 (0) never; coffee (14) 20; scan 0 (68) never; scan 2 (94) never |
| M4 | env_layout_02 | scan 1 (0) out; office (30) 33; scan 2 (110) never | C12: scan 1 (0) out; scan 2 (30) 50 · C6: scan 0 (0) 10; office (30) 33; scan 2 (110) never · C13: scan 0 (0) 9 · C14: scan 2 (0) 25 |
| M4 | env_layout_03 | scan 1 (0) out; office (30) 30; scan 2 (110) 15 | C12: scan 1 (0) out; scan 2 (30) 24 · C6: scan 0 (0) 14; office (30) 30; scan 2 (110) 14 · C13: scan 0 (0) 14 · C14: scan 2 (0) 8 |
| M4 | env_layout_04 | scan 1 (0) out; office (19) 8; scan 2 (86) 37 | C12: scan 1 (0) out; scan 2 (19) never · C6: scan 0 (0) never; office (19) 6; scan 2 (86) 37 · C13: scan 0 (0) 14 · C14: scan 2 (0) 21 |

Read against the controlled rows (both sides agree with the records; stated, not ruled):
- Where a mixed script begins as a controlled one, the stretches are the same tick for tick: M1's first three are
  C7's, M2's first is C10's, M3's first is C11's.
- A component that follows a different prefix behaves as in the controlled row that starts it from the same place:
  office_break in M1 and M4 takes 30 to 34 ticks (env_layout_02 and _03) and 6 to 8 (env_layout_04) to θ, as in C6
  (33, 30, 6); scan 2 out of the office is never at θ in env_layout_02 and at 13 to 15 and 36 to 37 ticks in the other
  rooms, as in C6 (never, 14, 37); the retried scan 0 in M2 (28, 33, never) as in C10 (28, 34,
  never); M2's coffee_break, entered from the dropped walk, as C8's entered from the cut walk (37, 11, 20).
- M3's walk to the frozen bay is cut after 14 ticks: that stretch never reaches θ (as C9's dropped walk in env_layout_03
  and _04); after the break, scan 2 reaches it in env_layout_03 and _04 (19, 11), not in env_layout_02 (the walk from
  the coffee machine, 12 ticks, as C5's 11).
- M4: the extra live hypothesis (scan 0, assigned and never performed) moves office_break's delay by 0 to 2 ticks
  against C6; scan 1 is outside the support as in C12.

### The row M4's standby walk, beside its written predictions

Actual (equal to the expectation written in `predictions.md` before the runs); the scan of pallet_4 never entered the
live set, and the record states it and the walk to the desk as open at the run's end in all three runs.

| scenario (room) | walk | live at its start | leader and gate, per stretch (actual) | finding (actual) | equals expected |
|---|---|---|---|---|---|
| scenario_s02_19 (env_layout_02) | 145–171 | coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), office_break(office_chair) | 145–166 confirm_delivered_pallet(pallet_0) none(below_theta); 167–182 confirm_delivered_pallet(pallet_0) clears; 183–201 confirm_delivered_pallet(pallet_0) none(leader_inadequate) | 145–182 adequate; 183–201 unexplained | yes |
| scenario_s04_19 (env_layout_03) | 148–172 | coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), office_break(office_chair) | 148–202 confirm_delivered_pallet(pallet_0) none(below_theta) | 148–186 adequate; 187–202 unexplained | yes |
| scenario_s06_19 (env_layout_04) | 126–150 | coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), office_break(office_chair) | 126–142 office_break(office_chair) none(below_theta); 143–156 office_break(office_chair) clears; 157–180 office_break(office_chair) none(leader_inadequate) | 126–156 adequate; 157–180 unexplained | yes |

The predictions written before the runs (not compared): under the present model the walk is read as scan 0 (assigned,
never scanned: commitment warrant) in env_layout_02 (cleared from 167) and env_layout_03 (never above θ), as
office_break in env_layout_04 (cleared from 143), unexplained once standing: the run shows exactly this. Under H1, H1
would lead at zero excess against scan 0's walk phase; under H2 (no assigned task live) H2 is never live, scan 0
being live to the run's end, so the prediction under H2 equals the present model's reading, which the run shows. In
env_layout_02 the walk to the standby place is admitted as a scan of pallet_0 the human never makes.

## The baseline: ticks to the threshold per true stretch, all 54 runs (2 October 2026)

A baseline for later design, derived from the existing outputs by `analysis/instruments/ir_testbed/baseline.py` (reporting only): every true stretch of the human's behaviour (a covered task on top of its stack; summary.py's
definition), its length, the live hypotheses at its first tick, and the ticks from its first tick to the first on which
the true hypothesis's belief is at or above θ = 0.75, or "never" within the stretch. Unmodelled behaviour (the walks to
the desk and to the standby place, the stand) has no true hypothesis and no row.

Stretches: 153; in the support 147; at θ within the stretch 98; never 49; outside the support 6. Delay to θ: median 20.0, min 6, max 50.

- Reach θ: 98 of the 147 stretches in the support (env_layout_02 38 of 49, median 28 ticks; env_layout_03 40 of 49,
  median 16; env_layout_04 20 of 49, median 17); every coffee_break and office_break stretch reaches it.
- Never: 49 stretches, every one a scan: the same-motion pairs (C3's and C4's first walks, 9); C3's second scan, which
  has no walk (3); scan 2 leaving the office in env_layout_02 (3; 33 to 35 ticks); and 34 stretches of 26 ticks or
  fewer (env_layout_04's walks from the standby place, the walks cut or dropped after 14 ticks, the walks from the
  coffee machine or the stand to the frozen bay).
- Outside the support: 6 (the scan of pallet_1 in C12 and M4).

### env_layout_02

| scenario | true stretch (start) | length | live at its start | ticks to θ |
|---|---|---|---|---|
| scenario_s02_02 | confirm_delivered_pallet(pallet_0) (0) | 30 | 4 | 10 |
| scenario_s02_02 | confirm_delivered_pallet(pallet_2) (30) | 53 | 3 | 50 |
| scenario_s02_03 | confirm_delivered_pallet(pallet_2) (0) | 30 | 4 | 25 |
| scenario_s02_03 | confirm_delivered_pallet(pallet_0) (30) | 53 | 3 | 28 |
| scenario_s02_04 | confirm_delivered_pallet(pallet_0) (0) | 30 | 4 | never |
| scenario_s02_04 | confirm_delivered_pallet(pallet_1) (30) | 3 | 3 | never |
| scenario_s02_05 | confirm_delivered_pallet(pallet_0) (0) | 30 | 6 | never |
| scenario_s02_05 | confirm_delivered_pallet(pallet_2) (30) | 53 | 5 | never |
| scenario_s02_05 | confirm_delivered_pallet(pallet_1) (83) | 53 | 4 | 28 |
| scenario_s02_05 | confirm_delivered_pallet(pallet_3) (136) | 53 | 3 | 50 |
| scenario_s02_06 | confirm_delivered_pallet(pallet_0) (0) | 30 | 4 | 10 |
| scenario_s02_06 | coffee_break(coffee_machine_0) (30) | 82 | 3 | 49 |
| scenario_s02_06 | confirm_delivered_pallet(pallet_2) (112) | 11 | 3 | never |
| scenario_s02_07 | confirm_delivered_pallet(pallet_0) (0) | 30 | 4 | 10 |
| scenario_s02_07 | office_break(office_chair) (30) | 80 | 3 | 33 |
| scenario_s02_07 | confirm_delivered_pallet(pallet_2) (110) | 35 | 3 | never |
| scenario_s02_08 | confirm_delivered_pallet(pallet_0) (0) | 28 | 4 | 10 |
| scenario_s02_08 | coffee_break(coffee_machine_0) (28) | 82 | 4 | 50 |
| scenario_s02_08 | confirm_delivered_pallet(pallet_0) (110) | 53 | 4 | 27 |
| scenario_s02_08 | confirm_delivered_pallet(pallet_2) (163) | 53 | 3 | 50 |
| scenario_s02_09 | confirm_delivered_pallet(pallet_0) (0) | 14 | 4 | 10 |
| scenario_s02_09 | coffee_break(coffee_machine_0) (14) | 69 | 4 | 37 |
| scenario_s02_09 | confirm_delivered_pallet(pallet_0) (83) | 53 | 4 | 26 |
| scenario_s02_09 | confirm_delivered_pallet(pallet_2) (136) | 52 | 3 | 49 |
| scenario_s02_10 | confirm_delivered_pallet(pallet_0) (0) | 14 | 4 | 10 |
| scenario_s02_10 | confirm_delivered_pallet(pallet_2) (14) | 41 | 4 | 31 |
| scenario_s02_11 | confirm_delivered_pallet(pallet_0) (0) | 14 | 4 | 10 |
| scenario_s02_11 | confirm_delivered_pallet(pallet_2) (14) | 41 | 4 | 31 |
| scenario_s02_11 | confirm_delivered_pallet(pallet_0) (55) | 52 | 3 | 28 |
| scenario_s02_12 | confirm_delivered_pallet(pallet_0) (0) | 30 | 4 | 10 |
| scenario_s02_12 | confirm_delivered_pallet(pallet_2) (71) | 53 | 3 | 46 |
| scenario_s02_13 | confirm_delivered_pallet(pallet_1) (0) | 30 | 4 | outside the support |
| scenario_s02_13 | confirm_delivered_pallet(pallet_2) (30) | 53 | 4 | 50 |
| scenario_s02_14 | confirm_delivered_pallet(pallet_0) (0) | 30 | 3 | 9 |
| scenario_s02_15 | confirm_delivered_pallet(pallet_2) (0) | 30 | 3 | 25 |
| scenario_s02_16 | confirm_delivered_pallet(pallet_0) (0) | 28 | 4 | 10 |
| scenario_s02_16 | coffee_break(coffee_machine_0) (28) | 82 | 4 | 50 |
| scenario_s02_16 | confirm_delivered_pallet(pallet_0) (110) | 53 | 4 | 27 |
| scenario_s02_16 | office_break(office_chair) (163) | 79 | 3 | 34 |
| scenario_s02_16 | confirm_delivered_pallet(pallet_2) (242) | 33 | 3 | never |
| scenario_s02_17 | confirm_delivered_pallet(pallet_0) (0) | 14 | 4 | 10 |
| scenario_s02_17 | coffee_break(coffee_machine_0) (14) | 69 | 4 | 37 |
| scenario_s02_17 | confirm_delivered_pallet(pallet_2) (83) | 11 | 4 | never |
| scenario_s02_17 | confirm_delivered_pallet(pallet_0) (94) | 53 | 3 | 28 |
| scenario_s02_18 | confirm_delivered_pallet(pallet_0) (0) | 30 | 4 | 10 |
| scenario_s02_18 | confirm_delivered_pallet(pallet_2) (71) | 14 | 3 | never |
| scenario_s02_18 | coffee_break(coffee_machine_0) (85) | 68 | 3 | 33 |
| scenario_s02_18 | confirm_delivered_pallet(pallet_2) (153) | 12 | 3 | never |
| scenario_s02_19 | confirm_delivered_pallet(pallet_1) (0) | 30 | 4 | outside the support |
| scenario_s02_19 | office_break(office_chair) (30) | 80 | 4 | 33 |
| scenario_s02_19 | confirm_delivered_pallet(pallet_2) (110) | 35 | 4 | never |

### env_layout_03

| scenario | true stretch (start) | length | live at its start | ticks to θ |
|---|---|---|---|---|
| scenario_s04_02 | confirm_delivered_pallet(pallet_0) (0) | 30 | 4 | 14 |
| scenario_s04_02 | confirm_delivered_pallet(pallet_2) (30) | 54 | 3 | 24 |
| scenario_s04_03 | confirm_delivered_pallet(pallet_2) (0) | 28 | 4 | 8 |
| scenario_s04_03 | confirm_delivered_pallet(pallet_0) (28) | 54 | 3 | 34 |
| scenario_s04_04 | confirm_delivered_pallet(pallet_0) (0) | 30 | 4 | never |
| scenario_s04_04 | confirm_delivered_pallet(pallet_1) (30) | 3 | 3 | never |
| scenario_s04_05 | confirm_delivered_pallet(pallet_0) (0) | 30 | 6 | never |
| scenario_s04_05 | confirm_delivered_pallet(pallet_2) (30) | 54 | 5 | never |
| scenario_s04_05 | confirm_delivered_pallet(pallet_1) (84) | 54 | 4 | 34 |
| scenario_s04_05 | confirm_delivered_pallet(pallet_3) (138) | 54 | 3 | 24 |
| scenario_s04_06 | confirm_delivered_pallet(pallet_0) (0) | 30 | 4 | 14 |
| scenario_s04_06 | coffee_break(coffee_machine_0) (30) | 53 | 3 | 13 |
| scenario_s04_06 | confirm_delivered_pallet(pallet_2) (83) | 49 | 3 | 19 |
| scenario_s04_07 | confirm_delivered_pallet(pallet_0) (0) | 30 | 4 | 14 |
| scenario_s04_07 | office_break(office_chair) (30) | 80 | 3 | 30 |
| scenario_s04_07 | confirm_delivered_pallet(pallet_2) (110) | 38 | 3 | 14 |
| scenario_s04_08 | confirm_delivered_pallet(pallet_0) (0) | 28 | 4 | 14 |
| scenario_s04_08 | coffee_break(coffee_machine_0) (28) | 53 | 4 | 17 |
| scenario_s04_08 | confirm_delivered_pallet(pallet_0) (81) | 24 | 4 | 15 |
| scenario_s04_08 | confirm_delivered_pallet(pallet_2) (105) | 54 | 3 | 24 |
| scenario_s04_09 | confirm_delivered_pallet(pallet_0) (0) | 14 | 4 | never |
| scenario_s04_09 | coffee_break(coffee_machine_0) (14) | 49 | 4 | 11 |
| scenario_s04_09 | confirm_delivered_pallet(pallet_0) (63) | 25 | 4 | 15 |
| scenario_s04_09 | confirm_delivered_pallet(pallet_2) (88) | 54 | 3 | 24 |
| scenario_s04_10 | confirm_delivered_pallet(pallet_0) (0) | 14 | 4 | never |
| scenario_s04_10 | confirm_delivered_pallet(pallet_2) (14) | 41 | 4 | 21 |
| scenario_s04_11 | confirm_delivered_pallet(pallet_0) (0) | 14 | 4 | never |
| scenario_s04_11 | confirm_delivered_pallet(pallet_2) (14) | 41 | 4 | 21 |
| scenario_s04_11 | confirm_delivered_pallet(pallet_0) (55) | 54 | 3 | 34 |
| scenario_s04_12 | confirm_delivered_pallet(pallet_0) (0) | 30 | 4 | 14 |
| scenario_s04_12 | confirm_delivered_pallet(pallet_2) (71) | 54 | 3 | 21 |
| scenario_s04_13 | confirm_delivered_pallet(pallet_1) (0) | 30 | 4 | outside the support |
| scenario_s04_13 | confirm_delivered_pallet(pallet_2) (30) | 54 | 4 | 24 |
| scenario_s04_14 | confirm_delivered_pallet(pallet_0) (0) | 30 | 3 | 14 |
| scenario_s04_15 | confirm_delivered_pallet(pallet_2) (0) | 28 | 3 | 8 |
| scenario_s04_16 | confirm_delivered_pallet(pallet_0) (0) | 28 | 4 | 14 |
| scenario_s04_16 | coffee_break(coffee_machine_0) (28) | 53 | 4 | 17 |
| scenario_s04_16 | confirm_delivered_pallet(pallet_0) (81) | 24 | 4 | 15 |
| scenario_s04_16 | office_break(office_chair) (105) | 80 | 3 | 30 |
| scenario_s04_16 | confirm_delivered_pallet(pallet_2) (185) | 37 | 3 | 13 |
| scenario_s04_17 | confirm_delivered_pallet(pallet_0) (0) | 14 | 4 | never |
| scenario_s04_17 | coffee_break(coffee_machine_0) (14) | 49 | 4 | 11 |
| scenario_s04_17 | confirm_delivered_pallet(pallet_2) (63) | 48 | 4 | 19 |
| scenario_s04_17 | confirm_delivered_pallet(pallet_0) (111) | 53 | 3 | 33 |
| scenario_s04_18 | confirm_delivered_pallet(pallet_0) (0) | 30 | 4 | 14 |
| scenario_s04_18 | confirm_delivered_pallet(pallet_2) (71) | 14 | 3 | never |
| scenario_s04_18 | coffee_break(coffee_machine_0) (85) | 52 | 3 | 13 |
| scenario_s04_18 | confirm_delivered_pallet(pallet_2) (137) | 50 | 3 | 19 |
| scenario_s04_19 | confirm_delivered_pallet(pallet_1) (0) | 30 | 4 | outside the support |
| scenario_s04_19 | office_break(office_chair) (30) | 80 | 4 | 30 |
| scenario_s04_19 | confirm_delivered_pallet(pallet_2) (110) | 38 | 4 | 15 |

### env_layout_04

| scenario | true stretch (start) | length | live at its start | ticks to θ |
|---|---|---|---|---|
| scenario_s06_02 | confirm_delivered_pallet(pallet_0) (0) | 19 | 4 | never |
| scenario_s06_02 | confirm_delivered_pallet(pallet_2) (19) | 20 | 3 | never |
| scenario_s06_03 | confirm_delivered_pallet(pallet_2) (0) | 28 | 4 | 21 |
| scenario_s06_03 | confirm_delivered_pallet(pallet_0) (28) | 19 | 3 | never |
| scenario_s06_04 | confirm_delivered_pallet(pallet_0) (0) | 19 | 4 | never |
| scenario_s06_04 | confirm_delivered_pallet(pallet_1) (19) | 3 | 3 | never |
| scenario_s06_05 | confirm_delivered_pallet(pallet_0) (0) | 19 | 6 | never |
| scenario_s06_05 | confirm_delivered_pallet(pallet_2) (19) | 20 | 5 | never |
| scenario_s06_05 | confirm_delivered_pallet(pallet_1) (39) | 19 | 4 | never |
| scenario_s06_05 | confirm_delivered_pallet(pallet_3) (58) | 19 | 3 | never |
| scenario_s06_06 | confirm_delivered_pallet(pallet_0) (0) | 19 | 4 | never |
| scenario_s06_06 | coffee_break(coffee_machine_0) (19) | 54 | 3 | 17 |
| scenario_s06_06 | confirm_delivered_pallet(pallet_2) (73) | 13 | 3 | 10 |
| scenario_s06_07 | confirm_delivered_pallet(pallet_0) (0) | 19 | 4 | never |
| scenario_s06_07 | office_break(office_chair) (19) | 67 | 3 | 6 |
| scenario_s06_07 | confirm_delivered_pallet(pallet_2) (86) | 40 | 3 | 37 |
| scenario_s06_08 | confirm_delivered_pallet(pallet_0) (0) | 17 | 4 | never |
| scenario_s06_08 | coffee_break(coffee_machine_0) (17) | 54 | 4 | 21 |
| scenario_s06_08 | confirm_delivered_pallet(pallet_0) (71) | 24 | 4 | never |
| scenario_s06_08 | confirm_delivered_pallet(pallet_2) (95) | 19 | 3 | never |
| scenario_s06_09 | confirm_delivered_pallet(pallet_0) (0) | 14 | 4 | never |
| scenario_s06_09 | coffee_break(coffee_machine_0) (14) | 54 | 4 | 20 |
| scenario_s06_09 | confirm_delivered_pallet(pallet_0) (68) | 26 | 4 | never |
| scenario_s06_09 | confirm_delivered_pallet(pallet_2) (94) | 19 | 3 | never |
| scenario_s06_10 | confirm_delivered_pallet(pallet_0) (0) | 14 | 4 | never |
| scenario_s06_10 | confirm_delivered_pallet(pallet_2) (14) | 21 | 4 | 10 |
| scenario_s06_11 | confirm_delivered_pallet(pallet_0) (0) | 14 | 4 | never |
| scenario_s06_11 | confirm_delivered_pallet(pallet_2) (14) | 21 | 4 | 10 |
| scenario_s06_11 | confirm_delivered_pallet(pallet_0) (35) | 20 | 3 | never |
| scenario_s06_12 | confirm_delivered_pallet(pallet_0) (0) | 19 | 4 | never |
| scenario_s06_12 | confirm_delivered_pallet(pallet_2) (60) | 20 | 3 | 17 |
| scenario_s06_13 | confirm_delivered_pallet(pallet_1) (0) | 19 | 4 | outside the support |
| scenario_s06_13 | confirm_delivered_pallet(pallet_2) (19) | 20 | 4 | never |
| scenario_s06_14 | confirm_delivered_pallet(pallet_0) (0) | 19 | 3 | 14 |
| scenario_s06_15 | confirm_delivered_pallet(pallet_2) (0) | 28 | 3 | 21 |
| scenario_s06_16 | confirm_delivered_pallet(pallet_0) (0) | 17 | 4 | never |
| scenario_s06_16 | coffee_break(coffee_machine_0) (17) | 54 | 4 | 21 |
| scenario_s06_16 | confirm_delivered_pallet(pallet_0) (71) | 24 | 4 | never |
| scenario_s06_16 | office_break(office_chair) (95) | 68 | 3 | 6 |
| scenario_s06_16 | confirm_delivered_pallet(pallet_2) (163) | 40 | 3 | 36 |
| scenario_s06_17 | confirm_delivered_pallet(pallet_0) (0) | 14 | 4 | never |
| scenario_s06_17 | coffee_break(coffee_machine_0) (14) | 54 | 4 | 20 |
| scenario_s06_17 | confirm_delivered_pallet(pallet_2) (68) | 13 | 4 | never |
| scenario_s06_17 | confirm_delivered_pallet(pallet_0) (81) | 20 | 3 | never |
| scenario_s06_18 | confirm_delivered_pallet(pallet_0) (0) | 19 | 4 | never |
| scenario_s06_18 | confirm_delivered_pallet(pallet_2) (60) | 14 | 3 | never |
| scenario_s06_18 | coffee_break(coffee_machine_0) (74) | 44 | 3 | 7 |
| scenario_s06_18 | confirm_delivered_pallet(pallet_2) (118) | 14 | 3 | 11 |
| scenario_s06_19 | confirm_delivered_pallet(pallet_1) (0) | 19 | 4 | outside the support |
| scenario_s06_19 | office_break(office_chair) (19) | 67 | 4 | 8 |
| scenario_s06_19 | confirm_delivered_pallet(pallet_2) (86) | 40 | 4 | 37 |

