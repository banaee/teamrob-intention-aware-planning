"""
mesa_sim/viz/run_file_panel.py

PURPOSE:
    The viewer's run-file panel (T-L stage 4, ruling 7): the run file the
    viewer is started from, its triple and its overrides, and a form limited to
    the three override kinds, which writes them into that run file and reloads.

WHAT THIS MODULE DOES:
    - Shows the run file's path, the domain, the layout / setup / scenario ids
      and every override in its --override form, those from the command line
      marked (they are not the file's, and are not written or removed here)
    - Adds or replaces one override of the file's block, or removes one (a path
      the command line gives is refused: its value, not the file's, is run):
      the run is first built with the new overrides (the loader's checks, as
      for any run); only a run that loads is written, then the page reloads

WHAT THIS MODULE DOES NOT DO:
    - No selection (layout, setup, scenario) and no other fact: the three kinds only
    - No change during a run
"""

import json
from typing import Callable, Dict, Sequence, Tuple

import solara

from mesa_sim.overrides import (FixedPositionOverride, HomeContainerOverride, Override,
                                StartPositionOverride, file_overrides, read_cli_override,
                                write_overrides)
from mesa_sim.sim_model import SimModel

# The form's three kinds: a label shown in the Select, and the class it makes.
_KINDS = {
    "agent start position": StartPositionOverride,
    "fixed object position": FixedPositionOverride,
    "movable object home container": HomeContainerOverride,
}


def _ids(path: str) -> list:
    with open(path, "r") as f:
        return [obj["id"] for obj in json.load(f).get("env_objects", [])]


@solara.component
def RunFilePanel(run_path: str, domain: str, layout_id: str, setup_id: str, scenario,
                 model_params: Dict, overrides: Sequence[Override], cli_overrides: Sequence[str],
                 on_reload: Callable[[], None]):
    cli_paths = {read_cli_override(text).path() for text in cli_overrides}
    fixed_ids = _ids(model_params["layout_path"])
    movable_ids = _ids(model_params["setup_path"])
    targets = {
        StartPositionOverride: [a.agent_id for a in scenario.agents],
        FixedPositionOverride: fixed_ids,
        HomeContainerOverride: movable_ids,
    }

    kind = solara.use_reactive(next(iter(_KINDS)))
    target = solara.use_reactive(None)
    x = solara.use_reactive(0.0)
    y = solara.use_reactive(0.0)
    container = solara.use_reactive(fixed_ids[0] if fixed_ids else None)
    error = solara.use_reactive("")

    cls = _KINDS[kind.value]
    # The selected id, or the kind's first when the selection is not one of its ids.
    current = target.value if target.value in targets[cls] else (targets[cls][0] if targets[cls] else None)

    def write(file_block: Tuple[Override, ...]):
        """Build the run with the file's new block and the command line's
        overrides (a command-line one replacing the file's for the same path);
        write the block only if the run loads, then reload."""
        by_path = {o.path(): o for o in file_block}
        by_path.update({o.path(): o for o in overrides if o.path() in cli_paths})
        trial = tuple(by_path[p] for p in sorted(by_path))
        try:
            SimModel(**{**model_params, "overrides": trial})
        except (ValueError, TypeError) as e:
            error.value = str(e)
            return
        error.value = ""
        write_overrides(run_path, file_block)
        on_reload()

    def add():
        if current is None:
            return
        if cls is HomeContainerOverride:
            new = HomeContainerOverride(current, container.value)
        else:
            new = cls(current, (float(x.value), float(y.value)))
        if new.path() in cli_paths:
            # The command line's value replaces the file's for this run: an edit
            # here would change nothing in it, and would go to the file untried.
            error.value = f"{new.path()} is given on the command line; not editable here"
            return
        kept = tuple(o for o in file_overrides(run_path) if o.path() != new.path())
        write(kept + (new,))

    def remove(path: str):
        write(tuple(o for o in file_overrides(run_path) if o.path() != path))

    with solara.Card("Run file", margin=1, elevation=2):
        solara.Markdown(f"`{run_path}`  \n"
                        f"domain `{domain}`  \n"
                        f"layout `{layout_id}`  \n"
                        f"setup `{setup_id}`  \n"
                        f"scenario `{scenario.id}`")
        # The rows in a column of their own, so the form below keeps its place in
        # the tree whatever their number; every input takes a plain value and an
        # on_value, so no input's state is matched to another's across a reload.
        with solara.Column():
            if not overrides:
                solara.Markdown("no overrides")
            for override in overrides:
                with solara.Row():
                    solara.Markdown(f"`{override.line()}`")
                    if override.path() in cli_paths:
                        solara.Markdown("(command line)")
                    else:
                        solara.Button("remove", text=True, on_click=lambda p=override.path(): remove(p))

        solara.Select("override", value=kind.value, values=list(_KINDS), on_value=kind.set)
        solara.Select("of", value=current, values=targets[cls], on_value=target.set)
        if cls is HomeContainerOverride:
            solara.Select("home container", value=container.value, values=fixed_ids, on_value=container.set)
        else:
            solara.InputFloat("x", value=x.value, on_value=x.set, continuous_update=True)
            solara.InputFloat("y", value=y.value, on_value=y.set, continuous_update=True)
        solara.Button("Write and reload", color="primary", on_click=add)
        if error.value:
            solara.Error(error.value)
