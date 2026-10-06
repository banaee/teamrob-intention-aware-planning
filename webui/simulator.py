"""
webui/simulator.py

PURPOSE:
    The interface between the web-ui and a simulator (T-viz 0.4): what a simulator's piece implements. Only message
    types cross it. The piece translates its model into messages and holds no rule of the web-ui; the server holds the
    rules (which sim-run is current, the end at the configured steps, the lock after the first step). Mesa's piece is
    mesa_sim/webui_adapter.py; the start that hands it to the server lives with the simulator, so nothing here imports
    one.

ONE THREAD (T-viz 1a):
    The server makes every call into a simulator's side (catalogue, build, and every call on a sim-run) on one thread
    of its own. A piece may rely on it: Mesa's piece writes into a sim-run's log pair only the lines logged on that
    thread, so that lines the server or a library logs on other threads never reach a sim-run's log.
"""

from typing import Protocol

from webui.messages import Catalogue, EndReason, RunDescription, SimRunChoice, SimRunId, TickUpdate


class BuildFailed(Exception):
    """The model could not be built from the choice; no sim-run exists and no log pair is written."""


class SimRunSide(Protocol):
    """One sim-run on the simulator's side."""

    description: RunDescription

    def state(self) -> TickUpdate:
        """The tick update of the tick reached (the start, or the last step)."""

    def step(self) -> TickUpdate:
        """One step; the tick update of the tick executed."""

    def end(self, reason: EndReason) -> TickUpdate:
        """The sim-run's end at the tick reached: its end lines written, its log pair closed; the tick update of that
        tick with its end."""

    def discard(self) -> None:
        """Leaves the sim-run without its end: never stepped, it writes no file."""


class Simulator(Protocol):

    def catalogue(self) -> Catalogue:
        """What can be chosen."""

    def build(self, choice: SimRunChoice, sim_run: SimRunId) -> SimRunSide:
        """The sim-run of the choice, built, at its start. The caller ends or discards the current sim-run first.
        Raises BuildFailed."""
