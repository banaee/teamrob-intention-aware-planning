#!/usr/bin/env python3
"""
analysis/l2_execution_lag/ablate.py  (L2 — attribution of the one decision change)

Runs one condition with L2's two halves switched on separately, by overriding the two
Projector arguments in this process only (shared/ untouched, the T1b/M1 pattern):
  none     both 0            = the T9 baseline
  latency  per-action completion latency only
  offset   human observation offset only
  both     = HEAD
Prints the [meta-cand] lines of one trigger so the mechanism behind a changed decision can
be attributed to one half or the other.

Usage: PYTHONHASHSEED=0 python analysis/l2_execution_lag/ablate.py <layout> <scenario> <prior true|false> <steps> <trigger step>
"""
import os, re, sys, logging
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "mesa_sim"))
if os.environ.get("PYTHONHASHSEED") != "0":
    sys.exit("Run with PYTHONHASHSEED=0 (TODO-42).")
os.chdir(ROOT)

from shared.projection import Projector                      # noqa: E402
from mesa_sim.sim_model import SimModel                      # noqa: E402
from domains.kitting.registry import domain_config           # noqa: E402

layout, scenario, prior, steps, want = sys.argv[1], sys.argv[2], sys.argv[3] == "true", int(sys.argv[4]), int(sys.argv[5])
_orig_init = Projector.__init__
MODE = {"value": (0.0, 0.0)}


def _init(self, *a, **kw):
    kw["action_completion_latency"], kw["observation_offset"] = MODE["value"]
    _orig_init(self, *a, **kw)


Projector.__init__ = _init

for name, mode in [("none (= T9 baseline)", (0.0, 0.0)), ("latency only", (1.0, 0.0)),
                   ("offset only", (0.0, 1.0)), ("both (= HEAD)", (1.0, 1.0))]:
    MODE["value"] = mode
    buf = []
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)
    h = logging.Handler()
    h.emit = lambda rec: buf.append(rec.getMessage())
    root.addHandler(h); root.setLevel(logging.INFO)
    lay = domain_config["layouts"][layout]
    model = SimModel(scenario=lay["scenarios"][scenario], register_fn=domain_config["register_fn"],
                     env_layout_path=lay["path"], assignment_prior=prior)
    for _ in range(steps):
        model.step()
    root.removeHandler(h)
    step, keep = None, []
    for ln in buf:
        m = re.match(r"^\[meta-trig\] step=(\d+)", ln)
        if m:
            step = int(m.group(1))
        elif step == want and (ln.startswith("[meta-cand]") or ln.startswith("[meta] ")):
            keep.append(ln.replace(",?kitting_table=kitting_table_0", "")
                          .replace("deliver_item(?item=", "(").replace("{'?item': '", "(")
                          .replace("', '?kitting_table': 'kitting_table_0'}", ")"))
    print(f"--- {name}: latency={mode[0]}, observation_offset={mode[1]}  (trigger step {want})")
    for ln in keep:
        print("    " + ln[:150])
