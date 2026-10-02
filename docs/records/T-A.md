# Record of planning and building: T-A, the pipeline revision

Moved verbatim from `docs/design_decisions.md` on 2 October 2026 (Hadi's ruling of that day: one record file per task;
the conceptual design stays in design_decisions.md). Each block is headed by the title of the entry it comes from
and its id; in design_decisions.md an index line with the same id stands where the block was.

**The pipeline from T-A: what moved, and why (T-A1)** — RECORD [T-A/1], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
REVISED ORDER (Hadi, 30 September 2026; `docs/roadmap.md`, "The plan from T-A", its order block): T-G no longer
holds 4D or ROS (4D is in the T-D tail, ROS is T-S); T-E is superseded by T-V, track 1. The order stated below is
history; the four decisions stand.

DECIDED (cchat, September 2026, after reading the state in `analysis/big_picture/STATUS.md`). The plan from
here is T-A (records) → T-B (B3.B on two tables) → T-C (the human action script) → T-D (robustness in
kitting) → T-E (demonstration) → T-F (evaluation, Phase 5) → T-G (later: a second domain in Mesa, 4D,
ROS); `docs/roadmap.md` holds it. Four decisions shape that order.
1. B2 (`gate_strategy`) IS AN EVALUATION FACTOR, NOT A DESIGN STEP. STATUS.md named "does the commitment
   gate survive?" as the first question for generated fixtures. It is not a question to answer before
   other work: `none` and `b2a` are both built, nothing downstream depends on which one wins, and B3.B
   leaves `b2a` unchanged (it commits to a task). So it is one factor of T-F's factorial, and no step
   re-reads B2 first. TODO-36 closes on this.
2. THE RANDOMISED HARNESS (TODO-47) MOVES TO T-F. It was "the next step" because three questions (B2, the
   gate's reopening condition, the scale of `min_separation` and β) were said to be answerable only there.
   Of these, B2 is a factor (1), the gate's reopening condition (TODO-47 (g)) is a T-F condition, and the
   scale question is gone: `min_separation` is a distance the body supplies ("`min_separation` is supplied
   by the body", above) and β is a physical tolerance ("β is a physical tolerance", below). What was
   genuinely blocking is the ordering fixture, so TODO-47 (f) stays in T-B as hand-built two-table layouts,
   with programmatic registration built there as the first part of fixture generation.
3. THE DEMONSTRATION COMES AFTER T-B, T-C AND T-D. Built now it could show switch and hold (s70 / s71) only.
   After them it shows what the framework claims: a two-table ordering, a change of mind, `unknown` as an
   outcome, as well as switch and hold, plain against realized cost, the stop on, prior off.
   SUPERSEDED IN PART (T-D R1, 27 September 2026): the `unknown` route no longer exists; its replacement is G. Not closed: the downstream response is G and X. design_decisions.md, "T-D R and E".
4. THE DOCUMENTATION PASS FOR THE PAPER COMES BEFORE THE PAPER, NOT BEFORE THE DEMONSTRATION. The demo is
   an instrument for seeing behaviour, and it needs the viewer, not polished documents; the paper needs
   the record consolidated once the evaluation's content is known.
Reference: T-A1, September 2026; `analysis/big_picture/STATUS.md`; TODO-36; TODO-47

---
