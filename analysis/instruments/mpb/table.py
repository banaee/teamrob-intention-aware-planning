#!/usr/bin/env python3
"""
table.py <out_root> — the planning test-bed's result table over the runs of run_set.sh (T-F part 1; design_records.md,
"T-F part 1: the conditions human-unaware and intention-unaware", I, R9, R10): one row per run, the run's settings as
columns (I: the effective values the run printed in its `[run]` header), then the measures read from the run's own
outputs, then the oracle's check. Writes <out_root>/results.csv and <out_root>/results.md, rows in run-name order.
The runs are run_set.sh's: <out_root>/<scenario>/<run>/, the log <run>.log in it (K, the measurement of T-F part 1).

Columns:
- run (the run file's name), domain, scenario, layout; human_aware, intention_aware, assignment_knowledge,
  context_knowledge, strategy (the header's; `settings_agree`: R5's reading of the run file gives the same);
  separation_stop (the header's effective value; added for the demo-day round of T-F, 8 October 2026, where it is a
  setting of the set, decision 6; R5 sets it off with human_aware off);
- completion (the world tick after the robot's last release on a task, where the pool completed; `unfinished` when the
  run has no terminal decision within its cap, whatever releases came before; since the comparative report of the
  measurement, 5 October 2026: the column had shown the last release's tick for an unfinished run), terminal (the terminal decision's tick),
  decisions (fired triggers), hold_ticks, stop_ticks (the run's `[stop]` lines: ticks the separation stop refused the
  robot's step), near_encounters (ticks whose continuous [sep] minimum lies below
  min_separation), viol, recede (a moving robot), stand_passing, stand_beside (a standing robot, the human passing or
  standing; analysis/instruments/common/separation.py), sep_min (the continuous minimum);
- oracle: compared | none (no table derivable: a script that depends on the robot, or assignment knowledge off in the
  intention-aware run, MPB-6); disagreements (the count, empty without the oracle); objects_separate; reference
  (human-unaware only: equal | differ, a finding (objects shared) | none; for a script that depends on the robot, from
  reference_check.py, T-K part 1, step 6).
"""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "common"))
import separation

COLUMNS = ["run", "domain", "scenario", "layout", "human_aware", "intention_aware", "assignment_knowledge",
           "context_knowledge", "strategy", "separation_stop", "settings_agree", "completion", "terminal", "decisions",
           "hold_ticks", "stop_ticks", "near_encounters", "viol", "recede", "stand_passing", "stand_beside", "sep_min",
           "oracle", "disagreements", "objects_separate", "reference"]


def row(d: Path, root: Path):
    s = json.load(open(d / "settings.json"))
    m = json.load(open(d / "measures.json"))
    _, by, passing, beside, _, _, cont = separation.counts(d / f"{d.name}.log")
    diff = json.load(open(d / "diff.json")) if (d / "diff.json").exists() else None
    reference = "none"
    if s["condition"] == "human-unaware" and (d / "reference.json").exists() and diff is not None:
        moved = [x for x in diff["disagreements"] if x[1] == "position (the reference run)"]
        reference = "differ, a finding (objects shared)" if diff.get("finding") else ("differ" if moved else "equal")
    elif s["condition"] == "human-unaware" and (d / "reference_check.json").exists():   # a script on the robot (step 6)
        reference = "differ" if json.load(open(d / "reference_check.json"))["disagreements"] else "equal"
    h = s["header"]
    log = d / f"{d.name}.log"
    header = next(l for l in open(log) if l.startswith("[run] "))
    stop = header.split("separation_stop=")[1].split()[0]
    stop_ticks = sum(1 for l in open(log) if l.startswith("[stop] "))
    return dict(run=d.name, domain=s["domain"], scenario=s["scenario"], layout=s["layout"],
                human_aware=h["human_aware"], intention_aware=h["intention_aware"],
                assignment_knowledge=h["assignment_knowledge"], context_knowledge=h["context_knowledge"],
                strategy=h["strategy"], separation_stop=stop, settings_agree=s["agree"], completion=m["completion"] if m["terminal"] is not None else "unfinished", terminal=m["terminal"],
                decisions=len(m["decisions"]), hold_ticks=m["measures"]["hold_ticks"], stop_ticks=stop_ticks,
                near_encounters=m["measures"]["near_encounters"], viol=len(by["viol"]), recede=len(by["recede"]),
                stand_passing=len(passing), stand_beside=len(beside),
                sep_min="" if cont is None else f"{cont[0]:.2f}",
                oracle="compared" if diff is not None else "none",
                disagreements="" if diff is None else len(diff["disagreements"]),
                objects_separate=s["objects_separate"], reference=reference)


if __name__ == "__main__":
    root = Path(sys.argv[1])
    rows = sorted((row(d, root) for d in root.glob("*/*") if (d / "settings.json").exists()), key=lambda r: r["run"])
    with open(root / "results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    lines = ["# The planning test-bed's results (T-F part 1)", "", "| " + " | ".join(COLUMNS) + " |",
             "|" + "---|" * len(COLUMNS)]
    lines += ["| " + " | ".join(str(r[c]) for c in COLUMNS) + " |" for r in rows]
    (root / "results.md").write_text("\n".join(lines) + "\n")
    bad = [r["run"] for r in rows if r["disagreements"] not in ("", 0) or not r["settings_agree"]]
    print(f"table: {len(rows)} runs; with a disagreement or a settings mismatch: {bad or 'none'}")
