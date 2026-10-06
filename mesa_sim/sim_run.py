"""
mesa_sim/sim_run.py

PURPOSE:
    One sim-run (T-viz 0.2): the SimModel built from a run configuration
    (mesa_sim/run_config.py), stepped, with its log pair and the run-level lines. Every start
    uses it: the headless start (mesa_sim/run_mesa.py) steps it N times and ends it; the
    solara-ui (mesa_sim/viz/solara_page.py) steps it on request; so a sim-run writes the same
    logs from any start.

WHAT THIS MODULE DOES:
    - RunLog: the log pair of one sim-run, logs/run_<timestamp>.log (the root logger, also
      echoed to the terminal) and logs/run_<timestamp>.rec (the logger `rec`, the human
      executor's record, T-H2), relative to the working directory. Its lines are held in
      memory until the pair is opened, at the sim-run's first step or its end, so a model
      built and never stepped leaves no file; a name already taken gets a suffix _2, _3, ...
      Logging is process-wide: one pair is attached at a time, and a new one closes the one
      attached before it
    - SimRun: the start line and the override lines, the model, per step the agents' lines
      and [sep], and the run's end (end_run, the end line)
    - start_sim_run: the start whose failure still writes its log pair (an empty pair on a
      flag error, the lines before the error on a failed build), so the newest pair in logs/
      is always the last start's

WHAT THIS MODULE DOES NOT DO:
    - No reading of a run file or of the flags, no building logic: mesa_sim/run_config.py
    - No simulation logic, no Solara
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np

from mesa_sim.run_config import build_model, resolve_triple

LOG_DIR = "logs"
_FORMAT = "%(message)s"


class _HeldFile(logging.Handler):
    """A file handler that holds its lines, formatted, until its file is opened; from then on
    it writes each line as logging.FileHandler does (mode "w", one line per record)."""

    def __init__(self):
        super().__init__()
        self.setFormatter(logging.Formatter(_FORMAT))
        self._held: List[str] = []
        self._file: Optional[logging.FileHandler] = None

    def emit(self, record: logging.LogRecord) -> None:
        if self._file is not None:
            self._file.emit(record)
            return
        try:
            self._held.append(self.format(record))
        except Exception:
            self.handleError(record)

    def open(self, path: str) -> None:
        self.acquire()
        try:
            self._file = logging.FileHandler(path, mode="w")
            self._file.setFormatter(self.formatter)
            for line in self._held:
                self._file.stream.write(line + self._file.terminator)
            self._file.flush()
            self._held = []
        finally:
            self.release()

    def close(self) -> None:
        self.acquire()
        try:
            if self._file is not None:
                self._file.close()
            self._held = []
        finally:
            self.release()
        super().close()


_attached: Optional["RunLog"] = None


class RunLog:
    """
    The log pair of one sim-run. Attached at creation: from then on every line logged in the
    process goes to it, held in memory until open() creates the two files. One pair is
    attached at a time (logging is process-wide): a new pair closes the one attached before
    it, whose files, if opened, end where they stand. A pair never opened leaves no file; a
    closed pair is not opened again.
    """

    def __init__(self):
        global _attached
        if _attached is not None:
            _attached.close()
        self.log_path: Optional[str] = None
        self.rec_path: Optional[str] = None
        self._closed = False
        self._root = logging.getLogger()
        self._rec = logging.getLogger("rec")
        self._root_level = self._root.level
        self._rec_propagate = self._rec.propagate
        self._log_file = _HeldFile()
        self._echo = logging.StreamHandler()   # still prints to terminal
        self._echo.setFormatter(logging.Formatter(_FORMAT))
        self._rec_file = _HeldFile()
        self._root.setLevel(logging.INFO)
        self._root.addHandler(self._log_file)
        self._root.addHandler(self._echo)
        # The human executor's record (T-H2): its own stream, one `[rec]` line per tick,
        # in the file beside the run log, never in the run log.
        self._rec.propagate = False
        self._rec.addHandler(self._rec_file)
        _attached = self

    def open(self) -> None:
        """Creates the two files and writes the lines held so far; nothing once opened."""
        if self._closed:
            raise RuntimeError("a closed log pair is not opened again")
        if self.log_path is not None:
            return
        Path(LOG_DIR).mkdir(exist_ok=True)
        base = f"{LOG_DIR}/run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        stem, n = base, 1
        while Path(f"{stem}.log").exists() or Path(f"{stem}.rec").exists():
            n += 1
            stem = f"{base}_{n}"
        self.log_path, self.rec_path = f"{stem}.log", f"{stem}.rec"
        self._log_file.open(self.log_path)
        self._rec_file.open(self.rec_path)

    def close(self) -> None:
        """Detaches the pair; its files, if opened, are closed as they stand."""
        global _attached
        if self._closed:
            return
        self._closed = True
        self._root.removeHandler(self._log_file)
        self._root.removeHandler(self._echo)
        self._rec.removeHandler(self._rec_file)
        for handler in (self._log_file, self._echo, self._rec_file):
            handler.close()
        self._root.setLevel(self._root_level)
        self._rec.propagate = self._rec_propagate
        if _attached is self:
            _attached = None


def _min_separation_over_tick(r0, r1, h0, h1) -> float:
    """
    The minimum robot–human distance over one tick when the robot moves in a
    straight line from r0 to r1 and the human from h0 to h1, simultaneously.
    The difference D(t) = (r0 − h0) + t ((r1 − h1) − (r0 − h0)) is affine in
    t ∈ [0, 1], so |D| is minimised at the clamped projection of the origin
    onto that segment — closed form, no sampling. A measure (TODO-79), not a
    behaviour: nothing reads it back.
    """
    dx0, dy0 = r0[0] - h0[0], r0[1] - h0[1]
    ex, ey = (r1[0] - h1[0]) - dx0, (r1[1] - h1[1]) - dy0
    ee = ex * ex + ey * ey
    t = 0.0 if ee == 0.0 else min(1.0, max(0.0, -(dx0 * ex + dy0 * ey) / ee))
    return float(np.hypot(dx0 + t * ex, dy0 + t * ey))


class SimRun:
    """
    One sim-run: from the model built from `config` at step 0 to its end, logging into `log`.
    The start line and the override lines are written before the model is built; the pair
    is opened at the first step() or at end().
    """

    def __init__(self, config: dict, log: RunLog):
        self.config = config
        self.log = log
        self.steps_done = 0
        n_steps = config["steps"]
        # The triple is the run's identity (T-L): the start line names the
        # RESOLVED layout, setup and scenario ids.
        _, layout_id, setup_id, scenario = resolve_triple(config)
        logging.info(f"[run_mesa] Starting headless run — "
              f"domain={config['domain']} layout={layout_id} setup={setup_id} scenario={scenario.id} steps={n_steps}")
        # Each override on the start line's block (T-L stage 4, ruling 7), in the
        # --override form, so the world the mind saw is reconstructible from the log.
        for override in config["overrides"]:
            logging.info(f"[run_mesa] override {override.line()}")

        self.model = build_model(config)

        # Positions at the end of the previous tick, for the continuous minimum of
        # the [sep] measure below (TODO-79); the initial positions before step 0.
        self._prev_pos: Dict[Tuple[str, str], tuple] = {
            (rid, hid): (tuple(map(float, robot.pos)), tuple(map(float, human.pos)))
            for rid, robot in self.model.robots.items() for hid, human in self.model.humans.items()
        }

    def step(self) -> None:
        self.log.open()
        model, step = self.model, self.steps_done
        model.step()
        self.steps_done += 1

        for aid, human in model.humans.items():
            logging.info(f"  step: {step}: [{aid}] task={human.current_task} "
                  f"action={human.current_action} "
                  f"micro={human.current_microaction} "
                  f"pos={np.round(human.pos, 2)}")
        for aid, robot in model.robots.items():
            logging.info(f"  step: {step}: [{aid}] task={robot.current_task} "
                  f"action={robot.current_action} "
                  f"micro={robot.current_microaction} "
                  f"pos={np.round(robot.pos, 2)}")
        # Actual robot–human separation (T9): a measure only, so later tasks
        # can report how often and by how much execution falls below
        # min_separation. Nothing here reacts to this number; Mesa's
        # execution-time layer is the executor's separation stop (C, a run
        # option, default off), which reads the human's actual position
        # itself. `dist` samples the end-of-tick
        # positions; `min` (T10, TODO-79) is the continuous minimum over the
        # tick with both agents moving in a straight line from their
        # previous positions to these — the motion model realization
        # assumes — so a close pass between two samples is read at its
        # minimum, not at the nearer sample.
        for rid, robot in model.robots.items():
            for hid, human in model.humans.items():
                r1 = tuple(map(float, robot.pos)); h1 = tuple(map(float, human.pos))
                r0, h0 = self._prev_pos[(rid, hid)]
                sep = float(np.hypot(r1[0] - h1[0], r1[1] - h1[1]))
                logging.info(f"[sep] step={step} {rid}-{hid} dist={sep:.2f} "
                             f"min={_min_separation_over_tick(r0, r1, h0, h1):.2f}")
                self._prev_pos[(rid, hid)] = (r1, h1)

    def end(self) -> None:
        """The run's end (T-G A3): a human whose script depends on the robot states
        the entries still open; an independent script writes nothing. Then the end
        line, and the pair is closed."""
        self.log.open()
        for human in self.model.humans.values():
            human.end_run(int(self.model.schedule.steps))
        logging.info("[run_mesa] Headless run complete.")
        self.log.close()

    def close(self) -> None:
        """Leaves the sim-run without its end: the pair, if opened, ends where it stands."""
        self.log.close()


def start_sim_run(read_config: Callable[[], dict]) -> SimRun:
    """
    A sim-run started from the run configuration `read_config` returns, whose start writes
    its log pair even when it fails (T-viz 0.2): an empty pair on a flag or configuration
    error, the lines before the error on a failed build. The sweep scripts take the newest
    pair in logs/ as the run's and go on after a failed run, so a failed start must not leave
    an earlier run's pair the newest. A start that treats a failure otherwise creates its
    RunLog and SimRun itself and closes the log unopened.
    """
    log = RunLog()
    try:
        return SimRun(read_config(), log)
    except BaseException:
        log.open()
        log.close()
        raise
