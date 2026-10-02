# analysis/

Sorted by domain (the sort, 1 October 2026; design_decisions.md, "T-G: the second domain's rulings", the step added
before the IR test-bed; old paths: `docs/rename_table.md`, "Paths: the sort").

- `instruments/`: the code the domains share. A domain's run set, expectations and reports are never here.
  - `ir_testbed/`: the IR test-bed (trajectory, oracle, actual outputs, comparison, figure, summary);
    `run.sh <domain> [-o root] [run files]`, its run files in `configs/<domain>/ir_testbed/`.
  - `mpb/`: the meta-planner test-bed's shared code; `run.sh <domain> ...`, its run files in `configs/<domain>/mpb/`,
    the domain's own parts (the declared properties, the step cap) in `<domain>/mpb/`.
  - `common/`: the log readers (`tdlib.py`, `logparse.py`) and F1's execution classes (`sep_classes.py`).
- `kitting/`: every earlier analysis (frozen at the commit its README states), the four maintained baseline sets
  (`tb1a_destination`, `tb1b_two_tables`, `tb1c_realized_flip`, `tb3_full_reorder`), and kitting's IR test-bed
  and MPB sets (`ir_testbed/`, `mpb/`).
- `dock_loading/`: dock_loading's sets (the IR test-bed from T-G stage 1).

Data and figures (Hadi, 2 October 2026): analysis/ tracks reports and code only (.md, .py, .sh). The frozen sets' data
is not in git from this commit on; it is restored in any clone with `git checkout 7d00f43 -- analysis/kitting/<set>`. A
full copy of analysis/ as of 2 October 2026 is at /home/hadi/teamrob_analysis_2026-10-02/.
