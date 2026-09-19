# analysis/g1_graded_evidence — graded evidence: the checks, the θ data, and the re-baselined sweep

The build: a stretch's evidence against `unknown` is graded by the fraction of the hypothesis's expected path
it covers — its odds are L / u^f instead of L / u (`docs/design_decisions.md`, "A stretch's evidence against
`unknown` is graded by the share of the expected path it covers"; `docs/recognizer_handback.md` §1.4–§1.5).
PYTHONHASHSEED=0; gate none, cost realized, stop off; the regression five (s00 300, s10 450, s20 300, s30 200,
s40 400 steps) and the evaluation fixtures (s50 / s70 / s71, 300), prior off and on.

- `check.py`: `--run` one condition in-process (the plain `run_mesa.run_headless`, the recognizer wrapped) with
  an INDEPENDENT accumulator of the accounting invariant under the grade and a per-tick record of the evidence
  state; `--final <base_dir> <new_dir>` runs the sixteen, checks instrumentation neutrality against the plain
  sweep on the CLAUDE.md greps, and writes `summary.md` and `crossings.md`.
- `summary.md` (committed): invariant per condition (max |Δ log odds| 7.1e-15 over 12,865 checks), reveals
  old → new per human task, crossings old → new, the meta-planner decisions that moved (consequences, not
  judged), completion ticks.
- `crossings.md` (committed): THE θ DATA for the deferred decision (fixed share / ratio of the top two /
  derived from the live set or layout; TODO-64 / 65): at every crossing of θ and ± 2 ticks, the top
  hypothesis's odds against `unknown`, the ratio of the top two, the live-set size.
- `sweep/` (logs, git-ignored): the plain sweep at the graded-evidence HEAD — THE BASELINES from here on,
  replacing `analysis/d2_recognition_trigger/` (`sweep/`, `fixtures/`). `data/`, `logs_instrumented/`:
  git-ignored.

Regenerate from the repo root (~4 min for the sweep, ~4 min for the check):

    H=analysis/g1_graded_evidence
    CONDS="s00 s10 s20 s30 s40" analysis/f1_robot_responsible/sweep.sh $H/sweep \
        --cost_strategy realized --gate_strategy none --separation_stop false
    analysis/f47_fixtures/sweep.sh $H/sweep --cost_strategy realized --gate_strategy none --separation_stop false
    PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python $H/check.py --final <pre-change sweep dir> $H/sweep

`<pre-change sweep dir>` is the same sixteen logs at the HEAD before the change (D2's baselines regenerated at
2d0c89d agree with `analysis/d2_recognition_trigger/` byte-for-byte on `[meta]`, `[IR]` and `[sep]`).

## Headline (details in `summary.md`)

- One-hypothesis reveals now follow the walk: s00_on 81 → 95, s20_on 57 → 72, s30_on 77 → 87, s10_on 314 → 339,
  s70_on / s71_on 98 → 120, s50_on 125 → 136 — each at odds 3.1–3.4 against `unknown`, about half the path
  (a lone task clears θ = 0.75 at f = ln 3 / ln 10 ≈ 0.48).
- Prior-off first-task reveals: s00 39 → 37, s10 29, s20 20, s30 28 → 27, s50 20, s70 / s71 23 unchanged;
  s40 21 → 30 (both priors; grasp at 60).
- No wrong-task crossing in any condition. The prior-off re-crossings within one recognition mostly go
  (s00 113 / 115, s10 33 / 35, s70 / s71 65 / 72 gone; s20 / s50 keep one at 27 and 92).
- Robot motion (`[sep]`) changes in six of sixteen conditions: s20_on, s30_off, s30_on, s50_on, s70_on,
  s71_off. Completion moves in two: s20_on 237 → 235, s71_off 199 → 201 (world ticks).

## md5 (`sweep/`)

| log | md5 |
|---|---|
| s00_off | 9228b8768d08007a9856cffeeaba4a44 |
| s00_on | 77b9f9839f5c5577869fa67430b2f8d8 |
| s10_off | 5c70bdaee75bcc1ed72180c4025cc2d2 |
| s10_on | 85e8f05ab567ed8764218ec0bb837285 |
| s20_off | 0dd16466ba6a049f3f6d2de853df9d3e |
| s20_on | 9a5fe1dee40165693d9972af6a01d471 |
| s30_off | 13b133da863edf80cb03ce15c217b52c |
| s30_on | bb9999477159cfaec703920c1371dfa8 |
| s40_off | ddf9b44b866742131b49633874283941 |
| s40_on | 78ca71086bcbc4629a40756af4d6a3fe |
| s50_off | e99fde7f1136f9a6bb5394d76f5de9fc |
| s50_on | 720903d4c32baf8048c54b098603fa6f |
| s70_off | f87f5497f244871791f4ef13665a1c98 |
| s70_on | 2a77939c1058426d678acb0fa2713259 |
| s71_off | 4afe316e1f4e3d1dd6f16b4035cd3707 |
| s71_on | 46f6df8edbe033a096d51f2b57398e87 |
