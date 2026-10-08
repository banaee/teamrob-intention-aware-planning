"""
mesa_sim/run_webui.py

PURPOSE:
    The web-ui's start (T-viz 1a): one command per start (TODO-196, answered for now). It reads the run file and the
    flags as the headless start does (mesa_sim/run_config.py, as strict), builds Mesa's piece for the web-ui
    (mesa_sim/webui_adapter.py) on them and starts the web-ui's server (webui/server.py), which serves the built page.
    The page opens on the run file's sim-run at its start (Hadi, 6 October 2026, P9).

USAGE (from the repository's root; the page built once, webui/page/README.md):
    PYTHONHASHSEED=0 ~/python-envs/ir-nomesa-env/bin/python mesa_sim/run_webui.py [--run <file>] [flags] [--port 8000]
        [--api_only]
    --api_only serves the requests under /api/ alone, without the built page and without its check: the page comes from
    Vite's dev server (npm run dev, which passes /api/ to port 8000). ./web-ui.sh -dev starts both.

WHAT THE START CHECKS:
    - The flags are the headless start's, plus --port. --steps sets the default step limit; the run file's `steps` is
      not used (the web-ui has no step limit unless one is set, P11), and the start says so when the run file states
      one.
    - A run file or flags that state an override, or a layout outside the scenario's reference layouts, stop the start:
      the page's choice cannot show either (T-viz 0.4, Q8; P2). Both stay possible headless.
    - A step limit below one, or a scene appearance naming a state its domain does not declare for the object type,
      stops the start with a message.
    - The built page (webui/page/dist) must exist and be newer than the page's sources; else the start stops, naming
      the command that builds it.

WHAT THIS MODULE DOES NOT DO:
    - No rule of the web-ui (webui/server.py) and no message (mesa_sim/webui_adapter.py)
"""

import argparse
import sys
from pathlib import Path

# Ensure project root is on path when run directly
sys.path.insert(0, str(Path(__file__).parent.parent))

# makes mesa_fork importable directly
sys.path.insert(0, str(Path(__file__).parent))

from mesa_sim.run_config import load_experiment, resolve_triple, user_args_parser  # noqa: E402
from mesa_sim.webui_adapter import MesaSimulator  # noqa: E402
from webui.server import serve  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "webui" / "page"
DIST = PAGE / "dist"
PAGE_SOURCES = ("src", "index.html", "package.json", "package-lock.json", "vite.config.ts", "tsconfig.json")
BUILD_COMMAND = "cd webui/page && npm ci && npm run build"
DEFAULT_PORT = 8000


def read_start(argv: list):
    """The start's command line read and checked: Mesa's piece built on the run configuration, and the port.
    Raises SystemExit with a message for a start the web-ui cannot show."""
    parser = user_args_parser()
    parser.description = "Start the TeamRob web-ui"
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="The server's port on 127.0.0.1")
    args = parser.parse_args(argv)
    flags = {k: v for k, v in vars(args).items() if k not in ("run", "override", "port", "steps")}
    config = load_experiment(args.run, flags, args.override)
    if config["overrides"]:
        raise SystemExit("[run_webui] the run states overrides (%s); the web-ui's choice cannot show them "
                         "(T-viz 0.4, Q8): run it headless" % ", ".join(o.line() for o in config["overrides"]))
    _, layout_id, _, scenario = resolve_triple(config)
    if layout_id not in scenario.reference_layouts:
        raise SystemExit("[run_webui] layout %s is not among the reference layouts of %s (%s); the web-ui offers only "
                         "those: run it headless" % (layout_id, scenario.id, ", ".join(scenario.reference_layouts)))
    if "steps" in config:
        print("[run_webui] the run file's steps (%s) is not used: the web-ui has no step limit unless --steps or the "
              "page sets one" % config["steps"], file=sys.stderr)
    try:
        simulator = MesaSimulator(config, step_limit=args.steps)
    except ValueError as e:      # a step limit below its minimum; a look by a state the domain does not declare
        raise SystemExit("[run_webui] %s" % e)
    return simulator, args.port


def page_ready() -> None:
    """Stops the start when the built page is missing or older than the page's sources."""
    index = DIST / "index.html"
    if not index.is_file():
        raise SystemExit("[run_webui] the page is not built; build it once: " + BUILD_COMMAND)
    sources = [p for name in PAGE_SOURCES for p in ([PAGE / name] if (PAGE / name).is_file()
                                                     else (PAGE / name).rglob("*")) if p.is_file()]
    newest = max(p.stat().st_mtime for p in sources)
    if newest > index.stat().st_mtime:
        raise SystemExit("[run_webui] the built page is older than its sources; build it again: " + BUILD_COMMAND)


def main(argv: list) -> None:
    dev = argparse.ArgumentParser(add_help=False)
    dev.add_argument("--api_only", action="store_true")
    known, rest = dev.parse_known_args(argv)
    simulator, port = read_start(rest)
    if known.api_only:
        serve(simulator, port, None)
        return
    page_ready()
    serve(simulator, port, DIST)


if __name__ == "__main__":
    main(sys.argv[1:])
