"""
mesa_sim/viz/solara_page.py

PURPOSE:
    The solara-ui's page (T-L stage 4, ruling 7), out of mesa_sim/run_mesa.py since T-viz 0.2
    so that the headless start imports no Solara. Started as before:
        solara run mesa_sim/run_mesa.py [-- <flags>]
    mesa_sim/run_mesa.py imports Page from here under solara only.

WHAT THIS MODULE DOES:
    - Page: the run file the page is started from, read again on every reload, its triple and
      overrides shown and the three override kinds editable (RunFilePanel), and SolaraViz
    - SolaraSimRun: the model SolaraViz builds and steps, one sim-run (mesa_sim/sim_run.py)
      with its log pair, so a stepped sim-run writes the same logs as the headless start

WHAT THIS MODULE DOES NOT DO:
    - No reading or building logic of its own (mesa_sim/run_config.py), no logging set-up
      (mesa_sim/sim_run.py)
"""

import solara

from mesa_sim.run_config import load_user_config, parse_user_args, resolve_model_params, resolve_triple
from mesa_sim.sim_run import start_sim_run
from mesa_sim.viz.space_drawer import space_drawer
from mesa_sim.viz.portrayal import agent_portrayal
from mesa_sim.viz.run_file_panel import RunFilePanel
from mesa_sim.mesa_fork.visualization import SolaraViz


class SolaraSimRun:
    """
    SolaraViz's model: it builds its model by model_class.__new__ and __init__ with the model
    parameters (mesa_sim/mesa_fork/visualization/solara_viz.py, make_model), steps it by
    step() and reads the model's attributes. This class starts a sim-run of the run
    configuration, steps the sim-run, and hands every other attribute to the sim-run's
    SimModel; `running` is SolaraViz's own play flag.
    """

    def __init__(self, run_config: dict):
        self.sim_run = start_sim_run(lambda: run_config)
        self.running = True

    def step(self) -> None:
        self.sim_run.step()

    def __getattr__(self, name):
        # reached only for an attribute this object does not hold: the model's
        sim_run = self.__dict__.get("sim_run")
        if sim_run is None:
            raise AttributeError(name)
        return getattr(sim_run.model, name)


@solara.component
def Page():
    """
    The viewer (T-L stage 4, ruling 7): the run file it is started from, read
    again on every reload, with its triple and overrides shown and the three
    override kinds editable (RunFilePanel), which writes them into that run
    file and reloads. SolaraViz keeps its parameters in its own state, so a
    reload remounts it under a new key: a fresh sim-run on the new run.
    """
    reload_count = solara.use_reactive(0)
    user_args = parse_user_args()
    config = solara.use_memo(load_user_config, dependencies=[reload_count.value])
    model_params = resolve_model_params(config)
    _, layout_id, setup_id, scenario = resolve_triple(config)

    def reload():
        reload_count.value += 1

    with solara.Sidebar():
        RunFilePanel(
            run_path=user_args.run,
            domain=config["domain"],
            layout_id=layout_id,
            setup_id=setup_id,
            scenario=scenario,
            model_params=model_params,
            overrides=config["overrides"],
            cli_overrides=user_args.override,
            on_reload=reload,
        )
    SolaraViz(
        model_class=SolaraSimRun,
        model_params={"run_config": config},
        space_drawer=space_drawer,
        agent_portrayal=agent_portrayal,
        name="TeamRob Simulation",
        play_interval=5,
    ).key(f"run-{reload_count.value}")
