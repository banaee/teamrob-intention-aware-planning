"""
webui/server.py

PURPOSE:
    The web-ui's server (T-viz 1a): it answers the page's requests over HTTP and holds the web-ui's rules, over any
    simulator that implements webui/simulator.py. It imports no simulator: the start that hands it a simulator's piece
    lives with that simulator (Mesa's: mesa_sim/run_webui.py).

THE RULES:
    - One current sim-run at a time. A choice builds a new one: the current one is ended at the tick reached (its end
      lines written, `choice_changed`) if it was stepped, else discarded (no log pair). A choice that cannot be built
      leaves no current sim-run.
    - A step limit applies only when the choice sets one (the run options' LimitValue in effect): the step that reaches
      it ends the sim-run in the same answer (`steps_reached`); a step of an ended sim-run is refused. Without a limit a
      sim-run ends by a reset, by a change of choice, or at the server's stop.
    - A reset ends the current sim-run at the tick reached (`reset`) if it was stepped, else discards it, and builds
      the same choice again.
    - At the server's stop a stepped current sim-run is ended (`server_stopped`).
    - A step while another step is under way is refused (`busy`). The page requests each step; the server never
      advances by itself.
    - The lock of the choices after the first step is the page's: the server ends a stepped sim-run when a new choice
      arrives, as 0.4 recorded.
    - A view (a layout, or a layout and a setup, with no scenario; T-viz 1a) is the current view until a choice or
      another view replaces it. It is refused while a stepped sim-run is current (the choices are locked); an
      unstepped current sim-run is discarded by it. A view that cannot be produced changes nothing.

ONE THREAD:
    Every call into the simulator's side runs on one worker thread of the server (webui/simulator.py, ONE THREAD),
    in the order the requests arrived. The HTTP side runs on its own thread and never touches a sim-run.

THE REQUESTS (JSON, plain request and response, on 127.0.0.1 only):
    GET  /api/catalogue   the catalogue
    POST /api/choose      SimRunChoice -> SimRunState, or 422 BuildFailure
    POST /api/step        SimRunRef    -> TickUpdate, or 409 StepRefusal
    POST /api/reset       SimRunRef    -> SimRunState, or 409 StepRefusal
    POST /api/view        ViewChoice   -> LayoutView, or 422 BuildFailure, or 409 ViewRefusal
    GET  /api/current     Current (the current sim-run with every tick update it gave, or the current view, or neither)
    The built page is served at /, when the start names its folder.

THE TERMINAL:
    The server's own lines (its address, each sim-run's build and end, the refusals) go to the terminal through the
    logger `webui`, which does not propagate; a sim-run's lines go only to its log pair.
"""

import asyncio
import contextlib
import logging
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Optional, Union

import uvicorn
from pydantic import BaseModel, ValidationError
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from webui import messages as msg
from webui.simulator import BuildFailed, SimRunSide, Simulator

HOST = "127.0.0.1"
GZIP_MINIMUM = 1000      # bytes: answers above it are compressed (the catalogue's 645 KB to about 40 KB)

log = logging.getLogger("webui")


def _terminal() -> None:
    """The server's own lines on the terminal, apart from the root logger a sim-run's log pair is attached to."""
    if not log.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter("[webui] %(message)s"))
        log.addHandler(handler)
    log.setLevel(logging.INFO)
    log.propagate = False


class _Current:
    """The current sim-run: its side, the steps done, whether it has ended, its step limit (None: none), and every tick
    update it gave, the start's first (T-viz 1a (iii): `current` answers with them all)."""

    def __init__(self, side: SimRunSide, limit: Optional[int]):
        self.side = side
        self.steps_done = 0
        self.ended = False
        self.limit = limit
        self.ticks: list = [side.state()]


def _limit(description: msg.RunDescription) -> Optional[int]:
    """The step limit in effect: the value of the run options' limit, None for none."""
    limits = [v.value for v in description.effective if isinstance(v, msg.LimitValue)]
    return limits[0] if limits else None


class WebUiServer:
    """The rules over one simulator (the module's docstring). Every method whose name starts with `_on_worker` runs on
    the worker thread only."""

    def __init__(self, simulator: Simulator):
        self._simulator = simulator
        self._worker = ThreadPoolExecutor(max_workers=1, thread_name_prefix="webui-sim")
        self._catalogue: Optional[msg.Catalogue] = None
        self._current: Optional[_Current] = None
        self._view: Optional[msg.LayoutView] = None
        self._serial = 0
        self._stepping = False      # read and written on the HTTP side only

    async def on_worker(self, fn, *args):
        return await asyncio.get_running_loop().run_in_executor(self._worker, fn, *args)

    # ------------------------------------------------------------------
    # On the worker thread
    # ------------------------------------------------------------------

    def _on_worker_start(self) -> None:
        catalogue = self._simulator.catalogue()
        if sum(isinstance(o, msg.LimitOption) for o in catalogue.run_options) > 1:
            raise ValueError("the catalogue declares more than one step limit")
        self._catalogue = catalogue

    def _on_worker_catalogue(self) -> msg.Catalogue:
        return self._catalogue

    def _on_worker_leave(self, reason: msg.EndReason) -> None:
        """The current sim-run left: ended at the tick reached if stepped, discarded if never stepped."""
        current, self._current = self._current, None
        if current is None or current.ended:
            return
        if current.steps_done > 0:
            update = current.side.end(reason)
            log.info("%s ended at tick %s (%s)", current.side.description.sim_run, update.tick, reason.value)
        else:
            current.side.discard()

    def _on_worker_build(self, choice: msg.SimRunChoice) -> msg.SimRunState:
        self._serial += 1
        sim_run = "sim-run-%d" % self._serial
        side = self._simulator.build(choice, sim_run)
        self._current = _Current(side, _limit(side.description))
        run = side.description.run
        log.info("%s built: %s %s %s %s, step limit %s", sim_run, run.domain, run.layout, run.setup, run.scenario,
                 "none" if self._current.limit is None else self._current.limit)
        return msg.SimRunState(description=side.description, tick=side.state())

    def _on_worker_choose(self, choice: msg.SimRunChoice) -> msg.SimRunState:
        self._on_worker_leave(msg.EndReason.CHOICE_CHANGED)
        self._view = None
        return self._on_worker_build(choice)

    def _on_worker_view(self, choice: msg.ViewChoice) -> Union[msg.LayoutView, msg.ViewRefusal]:
        current = self._current
        if current is not None and current.steps_done > 0:
            return msg.ViewRefusal(sim_run=current.side.description.sim_run)
        view = self._simulator.view(choice)      # BuildFailed: nothing changes
        self._on_worker_leave(msg.EndReason.CHOICE_CHANGED)     # unstepped: discarded, no log pair
        self._view = view
        return view

    def _refusal(self, ref: msg.SimRunRef, step: bool) -> Optional[msg.StepRefusal]:
        current = self._current
        if current is None or current.side.description.sim_run != ref.sim_run:
            return msg.StepRefusal(sim_run=ref.sim_run, reason=msg.StepRefusalReason.NOT_CURRENT)
        if step and current.ended:
            return msg.StepRefusal(sim_run=ref.sim_run, reason=msg.StepRefusalReason.ENDED)
        return None

    def _on_worker_step(self, ref: msg.SimRunRef) -> Union[msg.TickUpdate, msg.StepRefusal]:
        refusal = self._refusal(ref, step=True)
        if refusal is not None:
            return refusal
        current = self._current
        update = current.side.step()
        current.steps_done += 1
        if current.limit is not None and current.steps_done >= current.limit:
            update = current.side.end(msg.EndReason.STEPS_REACHED)     # the same tick, with its end
            current.ended = True
            log.info("%s ended at tick %s (steps_reached)", ref.sim_run, update.tick)
        current.ticks.append(update)
        return update

    def _on_worker_reset(self, ref: msg.SimRunRef) -> Union[msg.SimRunState, msg.StepRefusal]:
        refusal = self._refusal(ref, step=False)
        if refusal is not None:
            return refusal
        choice = self._current.side.description.stated
        self._on_worker_leave(msg.EndReason.RESET)
        return self._on_worker_build(choice)

    def _on_worker_current(self) -> msg.Current:
        if self._current is None:
            return msg.Current(state=None, view=self._view)
        current = self._current
        return msg.Current(state=msg.SimRunHistory(description=current.side.description, ticks=tuple(current.ticks)),
                           view=None)

    def _on_worker_stop(self) -> None:
        self._on_worker_leave(msg.EndReason.SERVER_STOPPED)

    # ------------------------------------------------------------------
    # The HTTP side
    # ------------------------------------------------------------------

    async def catalogue(self, request: Request) -> Response:
        return _answer(await self.on_worker(self._on_worker_catalogue))

    async def choose(self, request: Request) -> Response:
        choice = await _body(request, msg.SimRunChoice)
        if isinstance(choice, Response):
            return choice
        try:
            return _answer(await self.on_worker(self._on_worker_choose, choice))
        except BuildFailed as e:
            log.info("a choice was not built: %s", e)
            return _answer(msg.BuildFailure(message=str(e)), 422)

    async def step(self, request: Request) -> Response:
        ref = await _body(request, msg.SimRunRef)
        if isinstance(ref, Response):
            return ref
        if self._stepping:
            return _answer(msg.StepRefusal(sim_run=ref.sim_run, reason=msg.StepRefusalReason.BUSY), 409)
        self._stepping = True
        try:
            answer = await self.on_worker(self._on_worker_step, ref)
        finally:
            self._stepping = False
        return _answer(answer, 409 if isinstance(answer, msg.StepRefusal) else 200)

    async def reset(self, request: Request) -> Response:
        ref = await _body(request, msg.SimRunRef)
        if isinstance(ref, Response):
            return ref
        answer = await self.on_worker(self._on_worker_reset, ref)
        return _answer(answer, 409 if isinstance(answer, msg.StepRefusal) else 200)

    async def view(self, request: Request) -> Response:
        choice = await _body(request, msg.ViewChoice)
        if isinstance(choice, Response):
            return choice
        try:
            answer = await self.on_worker(self._on_worker_view, choice)
        except BuildFailed as e:
            log.info("a view was not produced: %s", e)
            return _answer(msg.BuildFailure(message=str(e)), 422)
        return _answer(answer, 409 if isinstance(answer, msg.ViewRefusal) else 200)

    async def current(self, request: Request) -> Response:
        return _answer(await self.on_worker(self._on_worker_current))

    @contextlib.asynccontextmanager
    async def lifespan(self, app: Starlette):
        await self.on_worker(self._on_worker_start)
        try:
            yield
        finally:
            await self.on_worker(self._on_worker_stop)
            self._worker.shutdown(wait=True)


def _answer(message: BaseModel, status: int = 200) -> Response:
    return Response(content=message.model_dump_json(), status_code=status, media_type="application/json")


async def _body(request: Request, kind):
    """The request's body read as `kind`, or a 400 answer naming why it is not one."""
    try:
        return kind.model_validate_json(await request.body())
    except ValidationError as e:
        return Response(content=str(e), status_code=400, media_type="text/plain")


class _PageFiles(StaticFiles):
    """The built page's files, each answered with `Cache-Control: no-cache`: the browser asks again on every load (a
    304 when nothing changed), so a page rebuilt since the browser last loaded it is never run from its cache. Without
    the header a browser may reuse a cached index.html, and the older bundle it names, for hours after a rebuild and
    across starts on the same address (found 9 October 2026: the old bundle drew the new appearance data)."""

    def file_response(self, *args, **kwargs) -> Response:
        response = super().file_response(*args, **kwargs)
        response.headers["Cache-Control"] = "no-cache"
        return response


def create_app(server: WebUiServer, page: Optional[Path]) -> Starlette:
    """The application: the requests under /api/, and the built page at / when `page` names its folder."""
    routes = [
        Route("/api/catalogue", server.catalogue, methods=["GET"]),
        Route("/api/choose", server.choose, methods=["POST"]),
        Route("/api/step", server.step, methods=["POST"]),
        Route("/api/reset", server.reset, methods=["POST"]),
        Route("/api/view", server.view, methods=["POST"]),
        Route("/api/current", server.current, methods=["GET"]),
    ]
    if page is not None:
        routes.append(Mount("/", app=_PageFiles(directory=str(page), html=True)))
    return Starlette(routes=routes, middleware=[Middleware(GZipMiddleware, minimum_size=GZIP_MINIMUM)],
                     lifespan=server.lifespan)


def serve(simulator: Simulator, port: int, page: Optional[Path]) -> None:
    """Serves the web-ui until it is stopped (Ctrl+C), on 127.0.0.1:`port`."""
    _terminal()
    app = create_app(WebUiServer(simulator), page)
    log.info("the web-ui at http://%s:%d/ (Ctrl+C stops it)", HOST, port)
    uvicorn.run(app, host=HOST, port=port, log_level="warning", access_log=False)
