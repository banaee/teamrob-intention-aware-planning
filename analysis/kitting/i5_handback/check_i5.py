#!/usr/bin/env python3
"""
analysis/i5_handback/check_i5.py — the confirmation matrix at HEAD, on I4d's harness (which runs I4c's and I4's).

Runs the eight conditions twice: `base` (HEAD, cmp'd against run_mesa.py's logs in new/) and `nofold` (the I4d
reversion, cmp'd against baseline/ = I4c's logs) — the reversion-control discipline of every stage since I2 —
and then asserts the results carried forward from I4 to I4d, one row each (criteria.md). No variants beyond the
reversion, no sweep, no new metric.

    PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python analysis/i5_handback/check_i5.py
"""
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "i4d_fold_unknown"))
import check_i4d as D                                   # noqa: E402  (imports check_i4c and check_i4)

D.HERE = HERE
D.I4.HERE = HERE
D.REF = {"base": HERE / "new", "nofold": HERE / "baseline"}


def carried_forward(metrics_path):
    m = {(r["condition"], r["variant"]): r for r in csv.DictReader(open(metrics_path))}
    b = lambda c: m[(c, "base")]
    reveal = lambda c, task: next((x for x in b(c)["reveals"].split(" ") if x.startswith(task + ":")), "")
    tick = lambda s: int(s.split(":")[1].split("(")[0]) if s and "never" not in s else None
    checks = [
        ("next-task reveals prior-on: s00 81, s20 57, s30 77, all pre-grasp",
         (tick(reveal("s00_on", "d(item_2)")), tick(reveal("s20_on", "d(item_2)")), tick(reveal("s30_on", "d(item_7)"))) == (81, 57, 77)
         and all("pre-grasp" in reveal(c, t) for c, t in (("s00_on", "d(item_2)"), ("s20_on", "d(item_2)"), ("s30_on", "d(item_7)"))),
         f"{reveal('s00_on', 'd(item_2)')} {reveal('s20_on', 'd(item_2)')} {reveal('s30_on', 'd(item_7)')}"),
        ("coffee crossing at 135 (prior-on) / 143 (prior-off)",
         (tick(reveal("s40_on", "coffee")), tick(reveal("s40_off", "coffee"))) == (135, 143),
         f"{reveal('s40_on', 'coffee')} {reveal('s40_off', 'coffee')}"),
        ("the 63 wrong-task ticks gone: no ac range in s40; only item_6 203–213 (11) prior-on, none prior-off",
         b("s40_on")["wrong_task_ranges"] == "d(item_6):203-213(11)" and b("s40_off")["wrong_task_ranges"] == "",
         f"on: {b('s40_on')['wrong_task_ranges'] or '-'}; off: {b('s40_off')['wrong_task_ranges'] or '-'}"),
        ("segment 3b retraction visible: item_6 0.790 → 0.083 (prior-on)",
         b("s40_on")["item6_3b_start_end"] == "0.790->0.083", b("s40_on")["item6_3b_start_end"]),
        ("s30's first reveal pre-grasp: 28 (off) / 21 (on), grasp 39",
         (tick(reveal("s30_off", "d(item_3)")), tick(reveal("s30_on", "d(item_3)"))) == (28, 21)
         and all("pre-grasp" in reveal(c, "d(item_3)") for c in ("s30_off", "s30_on")),
         f"{reveal('s30_off', 'd(item_3)')} {reveal('s30_on', 'd(item_3)')}"),
        ("TODO-53 closed: ac_activation most_likely on the 3 post-boundary prior ticks only in 184–271; ac 0.001 at 272",
         b("s40_on")["ac_most_likely_ticks_184_271"] == "3" and "ac" not in b("s40_on")["at_272"].split("(")[0],
         f"ac most_likely ticks {b('s40_on')['ac_most_likely_ticks_184_271']}, at 272: {b('s40_on')['at_272']}"),
        ("s20_off's first-task reveal at 20 (pre-grasp, grasp 22)",
         tick(reveal("s20_off", "d(item_3)")) == 20 and "pre-grasp" in reveal("s20_off", "d(item_3)"), reveal("s20_off", "d(item_3)")),
        ("TODO-60 closed: invariant max |Δ log odds| ≤ 1e-9 in every condition",
         all(float(b(c)["invariant_max_err"]) <= 1e-9 for c in D.ORDER),
         "max " + f"{max(float(b(c)['invariant_max_err']) for c in D.ORDER):.1e}"),
        ("no wrong crossing prior-on except item_6's aligned walk (203); none prior-off",
         all(int(b(c)["n_wrong_cross"]) == 0 for c in D.ORDER if c != "s40_on") and int(b("s40_on")["n_wrong_cross"]) == 1,
         " ".join(f"{c}:{b(c)['n_wrong_cross']}" for c in D.ORDER)),
        ("prior-off repeated crossings, recorded not tuned: s00_off 109/113/115, s20_off 20/24/30 and 87/91/95",
         all(x in b("s00_off")["crossings"] for x in ("109:d(item_2)", "113:d(item_2)", "115:d(item_2)"))
         and all(x in b("s20_off")["crossings"] for x in ("20:d(item_3)", "24:d(item_3)", "30:d(item_3)", "87:d(item_2)", "91:d(item_2)", "95:d(item_2)")),
         f"s00_off: {b('s00_off')['crossings']}; s20_off: {b('s20_off')['crossings']}"),
    ]
    lines = ["# I5 — results carried forward, asserted at HEAD (from metrics.csv, variant `base`)\n",
             "| result | holds | measured |", "|---|---|---|"]
    ok = True
    for name, good, detail in checks:
        ok &= bool(good)
        lines.append(f"| {name} | {'yes' if good else 'NO'} | {detail} |")
    lines.append(f"\nALL CARRIED FORWARD: {'yes' if ok else 'NO'}\n")
    (HERE / "criteria.md").write_text("\n".join(lines))
    print("\n".join(lines))
    return ok


if __name__ == "__main__":
    rc = D.final()                      # summary.md: base == new/, nofold == baseline/, invariant, unit checks
    ok = carried_forward(HERE / "metrics.csv")
    sys.exit(0 if rc == 0 and ok else 1)
