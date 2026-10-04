# analysis/

Sorted by domain (the sort, 1 October 2026; design_decisions.md, "T-G: the second domain's rulings", the step added
before the IRB; old paths: `docs/rename_table.md`, "Paths: the sort").

- `instruments/`: the code the domains share. A domain's run set, expectations and reports are never here.
  - `irb/`: the IRB (trajectory, oracle, actual outputs, comparison, figure, summary);
    `run.sh <domain> [-o root] [run files]`, its run files in `configs/<domain>/irb/`.
  - `mpb/`: the meta-planner test-bed's shared code; `run.sh <domain> ...`, its run files in `configs/<domain>/mpb/`,
    the domain's own parts (the declared properties, the step cap) in `<domain>/mpb/`.
  - `common/`: the log readers (`tdlib.py`, `logparse.py`) and F1's execution classes (`sep_classes.py`).
- `kitting/`: every earlier analysis (frozen at the commit its README states), the four maintained baseline sets
  (`tb1a_destination`, `tb1b_two_tables`, `tb1c_realized_flip`, `tb3_full_reorder`), and kitting's IRB
  and MPB sets (`irb/`, `mpb/`).
- `dock_loading/`: dock_loading's sets (the IRB from T-G stage 1).

Data and figures (Hadi, 2 October 2026): analysis/ tracks reports and code only (.md, .py, .sh). The frozen sets' data
is not in git from this commit on; it is restored in any clone with `git checkout 7d00f43 -- analysis/kitting/<set>`. A
full copy of analysis/ as of 2 October 2026 is at /home/hadi/teamrob_analysis_2026-10-02/.

Deleted (Hadi, 4 October 2026, T-K part 1, step 1: runs of early tests, no systematic evaluation): the 14 kitting folders
c_separation_stop, d2_recognition_trigger, f1_foreseeable_fixture, f1_robot_responsible, g1_graded_evidence,
i2_ir_foundations, i3_phase_model, i4_evidence_model, i4c_episode, i4d_fold_unknown, i5_handback, t1b_realization,
t6_ablation, t9_arrival_radius. The last commit that holds them is 32029d3 (`git checkout 32029d3 --
analysis/kitting/<folder>`); their untracked data is in the copy named above. Citations of them in the records stay.
