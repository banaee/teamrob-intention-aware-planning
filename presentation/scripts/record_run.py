"""Records a sim-run for a slide: the run file's sim-run, built and stepped by the same piece of code that feeds the
web-ui (mesa_sim/webui_adapter.py, MesaSimulator), and the tick updates of the ticks a slide replays, so that the deck
needs no server at talk time. Nothing is authored or changed here: the run file is T-F part 1's (under
configs/kitting/tf1/measurement/) or one of the deck's own (configs/kitting/tpres/, Hadi's scenarios for the talk), its
run options passed as the web-ui passes a screen-user's choice.

    PYTHONHASHSEED=0 ~/python-envs/ir-nomesa-env/bin/python presentation/scripts/record_run.py \
        <name> <run file> <first tick> <last tick>

Writes presentation/data/run_<name>.json: the domain's scene appearance, the run's triple and world (the run
description's), and the tick updates of ticks <first> to <last>, each cut to what the slide draws (the world, and per
robot its body, its belief over the live hypotheses, its gate's answer, its last decision and what lies ahead), and the
robots' descriptions (their hypotheses and θ), which the robot's mind beside a replay reads. The deck's build runs it
(scripts/record.mjs) every time, from the original files.
"""

import json
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "mesa_sim"))     # makes mesa_fork importable directly, as the web-ui's start does

from mesa_sim.webui_adapter import MesaSimulator  # noqa: E402
from webui import messages as msg  # noqa: E402

TRIPLE = ("domain", "layout", "scenario")
NOT_OPTIONS = {"setup"}      # the setup is the scenario's; a run file names it for the reader only


def choice_of(simulator: MesaSimulator, run_file: dict) -> msg.SimRunChoice:
    """The run file as a screen-user's choice: its triple, and every declared run option at the run file's value
    (the catalogue's default where the run file names none). A key that is neither is refused."""
    catalogue = simulator.catalogue()
    declared = {d.name for d in catalogue.run_options}
    unknown = set(run_file) - declared - set(TRIPLE) - NOT_OPTIONS
    if unknown:
        raise SystemExit(f"[record_run] run file keys the catalogue does not declare: {sorted(unknown)}")
    options = tuple(v.model_copy(update={"value": run_file[v.name]}) if v.name in run_file else v
                    for v in catalogue.default_choice.options)
    return msg.SimRunChoice(domain=run_file["domain"], layout=run_file["layout"], scenario=run_file["scenario"],
                            options=options)


def cut(update: msg.TickUpdate) -> dict:
    """What a slide draws of a tick update."""
    world = update.world.model_dump(mode="json", exclude={"activity", "separations"})
    robots = []
    for r in update.robots:
        belief = r.belief
        robots.append({
            "robot": r.robot,
            "body": r.body.model_dump(mode="json", include={"task", "hold", "finished"}),
            "belief": None if belief is None else belief.model_dump(mode="json"),
            "gate_answer": r.gate_answer.value,
            "decision": None if r.decision is None else r.decision.model_dump(mode="json"),
            "walks_ahead": [w.model_dump(mode="json") for w in r.walks_ahead],
            "projection_ahead": [p.model_dump(mode="json") for p in r.projection_ahead],
        })
    return {"tick": update.tick, "world": world, "robots": robots}


def main(name: str, run_path: str, first: int, last: int) -> None:
    run_file = yaml.safe_load((REPO / run_path).read_text())
    simulator = MesaSimulator()
    choice = choice_of(simulator, run_file)
    entry = next(d for d in simulator.catalogue().domains if d.name == choice.domain)
    run = simulator.build(choice, f"deck-{name}")
    ticks = []
    try:
        while True:
            update = run.step()
            if update.tick is not None and update.tick >= first:
                ticks.append(cut(update))
            if update.tick is not None and update.tick >= last:
                break
    finally:
        run.discard()
    description = run.description
    recorded = {
        "name": name,
        "run_file": run_path,
        "appearance": entry.appearance.model_dump(mode="json"),
        "run": description.run.model_dump(mode="json"),
        "sim_run": f"deck-{name}",
        "world": description.world.model_dump(mode="json", include={"space", "areas", "fixed_objects",
                                                                     "movable_objects", "scripts"}),
        "robots": [r.model_dump(mode="json", include={"robot", "condition", "assigned", "hypotheses",
                                                       "theta"})
                   for r in description.robots],
        "ticks": ticks,
    }
    out = REPO / "presentation" / "data" / f"run_{name}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(recorded, separators=(",", ":")) + "\n")
    print(f"[record_run] {out.relative_to(REPO)}: ticks {first} to {last} of {run_path}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
