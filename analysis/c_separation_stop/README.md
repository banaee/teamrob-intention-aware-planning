# analysis/c_separation_stop — the execution-time separation stop (C)

Scripts that produced the C numbers recorded in design_decisions.md ("Execution-time separation stop")
and TODO-73. Logs are git-ignored; the md5s at the end of `comparison.md` identify the runs.

- `sweep.sh <out_dir> [run_mesa args]`: headless sweep (PYTHONHASHSEED=0); s00 300, s10 450, s20 300,
  s30 200 steps; `CONDS` picks fixtures. Sequential only.
- `evaluate.py`: per condition, stop off against the F1 realized baseline (byte-identical minus the
  `[run]` line), decision sequences off and on, every `[stop]` episode with its window label, the
  acceptance check (every robot step on Mesa's sequential motion against the F1 rule; must be 0 with the
  stop on) and the simultaneous-interpolation figure alongside. Output: `comparison.md`.
- `blocked.py [dir ...]` (R2): blocked time as an outcome from the `[stop]` episodes (total ticks, episodes,
  place and action; completion only when it happens, else "blocked by an occupying human" with the
  duration), human-borne proximity (robot standing, human within min_separation, by what the robot was
  doing) next to the robot violations, and for D2 the stops per blocked place and the walks that contain
  or end in a stop. Default input: `stop_off/` and `stop_on/`. Output: `blocked.md`.

Regenerate from the repo root (~1 min):

    H=analysis/c_separation_stop
    $H/sweep.sh $H/stop_off --cost_strategy realized --gate_strategy none --separation_stop false
    $H/sweep.sh $H/stop_on  --cost_strategy realized --gate_strategy none --separation_stop true
    ~/python-envs/teamrob-sp4-env/bin/python $H/evaluate.py > $H/comparison.md
    ~/python-envs/teamrob-sp4-env/bin/python $H/blocked.py > $H/blocked.md

STOP-ON BASELINES REGENERATED under graded evidence (September 2026): `stop_on/` is the graded HEAD (md5s in
`comparison.md`); `stop_off/` is superseded by `analysis/g1_graded_evidence/sweep/`. Against the post-D2 stop-on
reference (T6's `core/gnone_crealized_son`, byte-identical to D2 on gate none) the grade moves the `[stop]` grep
in two conditions — s20_on (first at 144; 156 → 158 refusals) and s30_on (first at 156; 44 → 46) — and `[sep]`
in s20_on (6), s30_off (27); the decision ticks move as in the stop-off sweep (`g1_graded_evidence/summary.md`);
no run's last release or completion moves. The text below is C's record.

`stop_off/` equals the F1 baselines apart from the header; `stop_on/` is the comparison condition, not a
baseline: with the stop on, s00, s20 and s30 do not complete (the human idles at the table after its
script ends; see the design entry). The stop-off runs contain walk-throughs (the acceptance column of
`comparison.md`) and support decision comparison only, not safety claims. The s10 logs and md5s here
predate TODO-32 (R2): at HEAD s10's `[meta-b3] T_h` at step 123 is 34.00, not 5.00, with no other
difference; the `blocked.md` numbers are unaffected.
