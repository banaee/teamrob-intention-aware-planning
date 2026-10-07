"""Records what the web-ui's server would send for the view of a layout into a data file of the deck, so that the
deck needs no server at talk time: the domain's scene appearance (the catalogue's) and the view of the layout (no
setup). The same piece of code feeds the web-ui (mesa_sim/webui_adapter.py, MesaSimulator); this script only calls it.

    PYTHONHASHSEED=0 ~/python-envs/ir-nomesa-env/bin/python presentation/scripts/record_view.py kitting env_layout_01

Writes presentation/data/<domain>_<layout>.json. The deck's build runs it (scripts/record.mjs) every time, from the
original files.
"""

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "mesa_sim"))     # makes mesa_fork importable directly, as the web-ui's start does

from mesa_sim.webui_adapter import MesaSimulator  # noqa: E402
from webui.messages import ViewChoice  # noqa: E402


def main(domain: str, layout: str) -> None:
    simulator = MesaSimulator()
    entry = next(d for d in simulator.catalogue().domains if d.name == domain)
    view = simulator.view(ViewChoice(domain=domain, layout=layout, setup=None))
    out = REPO / "presentation" / "data" / f"{domain}_{layout}.json"
    out.parent.mkdir(exist_ok=True)
    recorded = {"appearance": entry.appearance.model_dump(mode="json"), "view": view.model_dump(mode="json")}
    out.write_text(json.dumps(recorded, indent=1) + "\n")
    print(f"[record_view] {out.relative_to(REPO)}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
