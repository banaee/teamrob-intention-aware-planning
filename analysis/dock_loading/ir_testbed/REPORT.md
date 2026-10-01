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

## Mixed (M1 to M4)

Not run: after Hadi's reading of the controlled section.
