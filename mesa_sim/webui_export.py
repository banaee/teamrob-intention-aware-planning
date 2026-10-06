"""
mesa_sim/webui_export.py

PURPOSE:
    Writes the messages of one sim-run at its start as files the web-ui's page reads without a server (T-viz 0.3, the
    style trial): its run description, its start tick update and its domain's scene appearance, in
    webui/page/public/samples/<name>/, with samples/index.json listing the samples. The sim-run is built through Mesa's
    piece (mesa_sim/webui_adapter.py) and discarded: never stepped, it writes no log pair. The samples are data, not
    tracked by git. Since T-viz 1a, increment (i), the page reads the web-ui's server (mesa_sim/run_webui.py) and no
    longer reads the samples; whether this module is removed is Hadi's (flagged at increment (i)).

    PYTHONHASHSEED=0 ~/python-envs/ir-nomesa-env/bin/python -m mesa_sim.webui_export            # the trial's two
    PYTHONHASHSEED=0 ~/python-envs/ir-nomesa-env/bin/python -m mesa_sim.webui_export \\
        --domain kitting --scenario scenario_s01_01 [--layout env_layout_01] [--name my_sample]

THE SCENE APPEARANCE:
    domains/<domain>/appearance.json, validated against webui/appearance.py; a domain without the file gets the
    defaults (Appearance()). It is not a world fact: the simulation never reads it.
"""

import argparse
import json
from pathlib import Path
from typing import Optional

from mesa_sim.webui_adapter import MesaSimulator, appearance
from webui import messages as m

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = ROOT / "webui" / "page" / "public" / "samples"

# The trial's sim-runs (T-viz 0.3, P3): kitting's regression fixture with every kind of kitting object, and
# dock_loading's MPB kind 3, pallets in every container at the start.
TRIAL = (("kitting", "scenario_s02_01", None),
         ("dock_loading", "scenario_s08_01", None))


def export(simulator: MesaSimulator, domain: str, scenario: str, layout: Optional[str], name: str) -> dict:
    catalogue = simulator.catalogue()
    entry = next((s for d in catalogue.domains if d.name == domain for s in d.scenarios if s.id == scenario), None)
    if entry is None:
        raise SystemExit(f"[webui_export] no scenario '{scenario}' in domain '{domain}'")
    choice = m.SimRunChoice(domain=domain, layout=layout or entry.reference_layouts[0], scenario=scenario,
                            options=catalogue.default_choice.options)
    side = simulator.build(choice, name)
    try:
        out = SAMPLES / name
        out.mkdir(parents=True, exist_ok=True)
        (out / "run_description.json").write_text(side.description.model_dump_json(indent=1))
        (out / "tick_update.json").write_text(side.state().model_dump_json(indent=1))
        (out / "appearance.json").write_text(appearance(domain).model_dump_json(indent=1))
    finally:
        side.discard()
    run = side.description.run
    print(f"[webui_export] {name}: {run.domain} {run.layout} {run.setup} {run.scenario} -> {out}")
    return {"name": name, "domain": run.domain, "layout": run.layout, "setup": run.setup, "scenario": run.scenario}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[1], formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--domain")
    parser.add_argument("--scenario")
    parser.add_argument("--layout")
    parser.add_argument("--name", help="the sample's folder name; default: <domain>_<scenario>")
    args = parser.parse_args()
    if (args.domain is None) != (args.scenario is None):
        parser.error("--domain and --scenario go together")
    if args.domain is None and (args.layout or args.name):
        parser.error("--layout and --name need --domain and --scenario")
    runs = TRIAL if args.domain is None else ((args.domain, args.scenario, args.layout),)

    simulator = MesaSimulator()
    index_path = SAMPLES / "index.json"
    index = json.loads(index_path.read_text()) if index_path.is_file() else []
    for domain, scenario, layout in runs:
        name = args.name or f"{domain}_{scenario}" + (f"_{layout}" if layout else "")
        row = export(simulator, domain, scenario, layout, name)
        index = [r for r in index if r["name"] != name] + [row]
    SAMPLES.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(index, indent=1) + "\n")


if __name__ == "__main__":
    main()
