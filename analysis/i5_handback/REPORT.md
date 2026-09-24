# I5 — confirmation matrix at HEAD, and the hand-back

> Superseding note (24 Sept 2026, the terminology ruling; `docs/glossary.md` §7, `docs/terminology_revision.md`): the harness (`analysis/i4_evidence_model/check_i4.py`, reused by I4c, I4d and I5) labels the human's ground truth `"unknown"` when the human's script is finished and for scenario_40's wander (`S40_TRUTH`: seg3a, seg3b, done). That is a WORLD fact written with the ROBOT's hypothesis name: read it as a finished work order, or unmodelled behaviour (the wander), respectively. So the "`!` = winner ≠ truth" marks and "wrong-θ" counts treat `unknown` leading as the correct reading of those ticks, and "unknown when idle" / `unknown_when_idle` is the `unknown` hypothesis's mass while the work order is finished (high by normalisation, not evidence of unmodelled behaviour). The same holds for this folder's `summary.md`.

No model change. This directory is the validation half of I5; the hand-back itself is `docs/recognizer_handback.md`.

**Matrix (`summary.md`, `criteria.md`).** Eight conditions at HEAD (`a6d7d7a`), `PYTHONHASHSEED=0`, on I4d's
harness with its reversion variant kept: `base` equals `run_mesa.py`'s logs (`new/`) in all eight — and those
logs are byte-identical to I4d's; `nofold` (the I4d reversion) equals I4c's logs (`baseline/`) in all eight;
the accounting invariant holds to |Δ log odds| ≤ 7.1e-15 over 5,069 checks; unit checks U1–U3, U6–U10 and U5''
PASS. Every result carried forward is asserted in `criteria.md`, all `yes`: next-task reveals prior-on 81 /
57 / 77 pre-grasp; coffee 135 / 143; the 63 wrong-task ticks gone (only item_6's aligned walk, 203–213,
remains, prior-on); segment 3b 0.790 → 0.083; s30 pre-grasp 28 / 21; TODO-53 closed; s20_off's first reveal
at 20 pre-grasp; TODO-60 closed; no wrong crossing prior-off, one prior-on (203); the prior-off repeated
crossings present as recorded (s00_off 109 / 113 / 115, s20_off 20 / 24 / 30, 87 / 91 / 95).

No diffs directory: `new/` is byte-identical to I4d's, whose `diffs/` attribute every difference from I4c.

| File | Content |
|---|---|
| `check_i5.py` | runs I4d's `final()` here (base + nofold, invariant, unit checks) and asserts the carried-forward results |
| `criteria.md` | the assertions, one row each |
| `summary.md`, `metrics.csv`, `invariant.csv`, `retention.csv`, `retrigger.md`, `chains.md`, `region.md`, per-tick CSVs | as in I4d |
| `baseline/`, `new/`, `logs_instrumented/` | not in git; `stages.sh` regenerates them |
