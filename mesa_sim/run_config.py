"""
mesa_sim/run_config.py

PURPOSE:
    The run configuration and the model built from it (T-viz 0.2): one definition that
    every start uses — the headless start and the solara-ui (mesa_sim/run_mesa.py), and a
    caller with a run configuration that did not come from the command line.

WHAT THIS MODULE DOES:
    - Reads the run configuration: the run file (configs/experiment.yaml, or the yaml --run
      names) with every flag given overriding it, and the run file's overrides block and
      every --override read into config["overrides"] (mesa_sim/overrides.py)
    - Checks a run configuration however it was stated (run_configuration): an unknown key,
      a strategy outside its choices, a switch that is not true/false or a test level outside
      (0, 1) stops the run
    - Resolves the run's triple from the domain registry and builds the SimModel from it

WHAT THIS MODULE DOES NOT DO:
    - No logging set-up and no log line: a sim-run's log pair and its run-level lines are
      mesa_sim/sim_run.py's
    - No Solara: importing it opens no file and imports nothing of the solara-ui
"""

import argparse
import sys
from pathlib import Path

import yaml

# makes mesa_fork importable directly (SimModel imports it under that name)
sys.path.insert(0, str(Path(__file__).parent))

from mesa_sim.sim_model import SimModel
from mesa_sim.overrides import run_overrides

from domains.kitting.registry import domain_config as kitting_config
from domains.dock_loading.registry import domain_config as dock_config


# =============================================================================
# Domain registry
# Maps domain name strings (from experiment.yaml or CLI) to Python objects.
# Add one entry here when adding a new domain.
# =============================================================================


DOMAIN_REGISTRY = {
    "kitting":      kitting_config,
    "dock_loading": dock_config,
}


# =============================================================================
# Experiment config loader
# =============================================================================

EXPERIMENT_CONFIG_PATH = "configs/experiment.yaml"

STRATEGIES = ("single_task", "full_reorder")
GATE_STRATEGIES = ("none", "b2a", "b2b")
COST_STRATEGIES = ("realized", "plain")
BOOL_OPTIONS = ("human_aware", "intention_aware", "assignment_knowledge", "context_knowledge", "separation_stop")
# The run options: the keys a run configuration may state, each with its CLI flag of the
# same name (parse_user_args; tests/test_tviz_sim_run.py holds the two lists equal).
RUN_OPTIONS = ("domain", "layout", "scenario", "steps", "human_aware", "intention_aware", "assignment_knowledge",
               "context_knowledge", "strategy", "gate_strategy", "cost_strategy", "separation_stop", "test_level")
# The run options with a closed list of values, each with its list (checked in run_configuration).
ONE_OF_OPTIONS = {"strategy": STRATEGIES, "gate_strategy": GATE_STRATEGIES, "cost_strategy": COST_STRATEGIES}
# The value a run option takes when the run configuration does not state it (resolve_model_params); `steps` has none,
# a run configuration states it.
OPTION_DEFAULTS = {
    "human_aware": True,            # both on by default (T-F part 1, R3); SimModel applies the override (R5)
    "intention_aware": True,
    "assignment_knowledge": True,   # both on by default (AM3, AM9)
    "context_knowledge": True,
    "strategy": "single_task",
    "gate_strategy": "none",
    "cost_strategy": "realized",
    "separation_stop": False,
    "test_level": 0.05,
}


def run_configuration(config: dict, source: str, flags: dict = None, cli_overrides=()) -> dict:
    """
    The run configuration from `config`, stated as a run file states it (a mapping of run
    options, with "setup" and the "overrides" block optional), and the CLI flags. Flags take
    precedence over stated values. `flags` holds one entry per CLI flag (None when not
    given); the flags are the run options, so a key that is not one of them is an error
    rather than a field nothing reads. Stated values are checked like the flags are: a
    strategy outside its choices, or a switch that is not a boolean (`"false"` is a string,
    and bool("false") is True), stops the run. The overrides block and the --override
    texts are read into the run's overrides (overrides.run_overrides): config["overrides"],
    a tuple, empty when there are none. `source` names where the configuration was stated,
    in the error of an unknown key.
    """
    config = dict(config)
    # "setup" may be named by the run file; there is no --setup flag (T-L,
    # ruling c: one setup per scenario), so it is not a flag. "overrides" is the
    # run file's overrides block (T-L stage 4); --override adds to it.
    allowed = set(RUN_OPTIONS) | {"setup", "overrides"}
    unknown = sorted(set(config) - allowed)
    if unknown:
        raise ValueError(
            f"{source}: unknown keys {unknown}. "
            f"Run options: {sorted(allowed)}"
        )
    config.update({k: v for k, v in (flags or {}).items() if v is not None})
    config["overrides"] = run_overrides(config.get("overrides"), cli_overrides)
    for key, choices in ONE_OF_OPTIONS.items():
        if key in config and config[key] not in choices:
            raise ValueError(f"{key}={config[key]!r}: expected one of {list(choices)}")
    for key in BOOL_OPTIONS:
        if key in config and not isinstance(config[key], bool):
            raise ValueError(f"{key}={config[key]!r}: expected true or false")
    # The adequacy test's level (T-D E5): a probability strictly between 0 and 1.
    if "test_level" in config:
        level = config["test_level"]
        if isinstance(level, bool) or not isinstance(level, (int, float)) or not 0.0 < level < 1.0:
            raise ValueError(f"test_level={level!r}: expected a number strictly between 0 and 1")
    return config


def load_experiment(run_path: str, flags: dict, cli_overrides=()) -> dict:
    """
    Load the run file (configs/experiment.yaml, or the yaml --run names) and
    apply the CLI flags: the run configuration (run_configuration) of what the
    file states.
    """
    with open(run_path, "r") as f:
        config = yaml.safe_load(f)
    return run_configuration(config, run_path, flags, cli_overrides)


# =============================================================================
# CLI argument parser
# =============================================================================

def _bool_arg(value: str) -> bool:
    """argparse type for the true/false override flags. Needed because bool('false')
    is True — argparse would otherwise accept any string as True."""
    if value.lower() in ("true", "1", "yes"):
        return True
    if value.lower() in ("false", "0", "no"):
        return False
    raise argparse.ArgumentTypeError(f"expected true/false, got '{value}'")


# `solara run mesa_sim/run_mesa.py -- --domain ...`: solara's own arguments come
# first in sys.argv, this script's follow the '--'.
UNDER_SOLARA = "solara" in Path(sys.argv[0]).parts


def script_argv() -> list:
    """The command-line arguments meant for this script: everything after the
    script name headless (a bare '--' dropped), only what follows '--' under
    solara (nothing when there is none)."""
    argv = sys.argv[1:]
    if UNDER_SOLARA:
        return argv[argv.index("--") + 1:] if "--" in argv else []
    return [a for a in argv if a != "--"]


def user_args_parser() -> argparse.ArgumentParser:
    """The parser of the flags (parse_user_args); its help texts are also the run options'
    descriptions in the web-ui's catalogue (mesa_sim/webui_adapter.py)."""
    parser = argparse.ArgumentParser(description="Run TeamRob Mesa simulation")
    parser.add_argument("--run",         type=str,  default=EXPERIMENT_CONFIG_PATH, help="The run file (default: configs/experiment.yaml)")
    parser.add_argument("--override",    type=str,  action="append", default=[], metavar="PATH=VALUE",
                        help="Override one fact of the run's artefacts (repeatable): scenario.<agent>.start_position=x,y | "
                             "layout.<object>.position=x,y | setup.<object>.initial_container=<id>")
    parser.add_argument("--domain",      type=str,  default=None, help="Domain name override (e.g. kitting, dock_loading)")
    parser.add_argument("--layout", type=str, default=None, help="Layout selection (default: the scenario's first reference layout)")
    parser.add_argument("--scenario",    type=str,  default=None, help="Scenario ID override (e.g. scenario_s02_02)")
    parser.add_argument("--steps",       type=int,  default=None, help="Number of steps override for headless run; in the web-ui, a step limit (none by default)")
    parser.add_argument("--human_aware", type=_bool_arg, default=None, help="Human-aware override: true/false (off: the human-unaware robot, no observed human; sets intention_aware, both knowledge options and separation_stop off; T-F part 1)")
    parser.add_argument("--intention_aware", type=_bool_arg, default=None, help="Intention-aware override: true/false (off: the intention-unaware robot, the recognizer computes nothing and the gate admits nothing; sets both knowledge options off; T-F part 1)")
    parser.add_argument("--assignment_knowledge", type=_bool_arg, default=None, help="Assignment knowledge override: true/false (the robot knows the observed human's assigned tasks)")
    parser.add_argument("--context_knowledge", type=_bool_arg, default=None, help="Context knowledge override: true/false (the recognizer's prior from the declared context knowledge, T-K part 1; off: the equal prior)")
    parser.add_argument("--strategy", type=str, default=None, choices=STRATEGIES, help="MetaPlanner B3 strategy override")
    parser.add_argument("--gate_strategy", type=str, default=None, choices=GATE_STRATEGIES, help="MetaPlanner B2 gate strategy override")
    parser.add_argument("--cost_strategy", type=str, default=None, choices=COST_STRATEGIES, help="MetaPlanner B3 cost strategy override")
    parser.add_argument("--separation_stop", type=_bool_arg, default=None, help="Execution-time separation stop override: true/false")
    parser.add_argument("--test_level", type=float, default=None, help="The recognizer's adequacy test level alpha, per derived phase (T-D E5)")
    return parser


def parse_user_args(argv: list = None):
    """Strict: an unknown or misspelled flag exits with an error, so a run never
    falls back silently to the yaml value of the option it meant to set.
    `argv` defaults to the command line's (script_argv)."""
    return user_args_parser().parse_args(script_argv() if argv is None else argv)


def load_user_config(argv: list = None) -> dict:
    """The run configuration: the run file the CLI names, every flag given overriding it,
    its overrides block and every --override read into config["overrides"].
    `argv` defaults to the command line's (script_argv)."""
    user_args = parse_user_args(argv)
    flags = {k: v for k, v in vars(user_args).items() if k not in ("run", "override")}
    return load_experiment(user_args.run, flags, user_args.override)



# =============================================================================
# Model factory — shared by every start
# =============================================================================
def resolve_triple(user_config: dict):
    '''
    Resolves the run's triple (T-L, glossary §9): the scenario from the
    domain's registry, the setup the scenario declares, and the layout — the
    one the run names, or the scenario's first reference layout when it names
    none. Every reference layout and the scenario's setup must be registered;
    a given layout must be registered but need not be a reference layout; a
    setup named by the run file must equal the scenario's.
    Returns (domain, layout_id, setup_id, scenario).
    '''
    # --------- domain ---------
    domain_name = user_config["domain"]
    if domain_name not in DOMAIN_REGISTRY:
        raise ValueError(
            f"Unknown domain '{domain_name}'. "
            f"Available: {list(DOMAIN_REGISTRY.keys())}"
        )
    domain = DOMAIN_REGISTRY[domain_name]

    # --------- scenario ---------
    scenario_id = user_config["scenario"]
    if scenario_id not in domain["scenarios"]:
        raise ValueError(
            f"Unknown scenario '{scenario_id}' for domain '{domain_name}'. "
            f"Available: {list(domain['scenarios'].keys())}"
        )
    scenario = domain["scenarios"][scenario_id]

    # --------- what the scenario declares is registered ---------
    for ref in scenario.reference_layouts:
        if ref not in domain["layouts"]:
            raise ValueError(
                f"scenario '{scenario_id}': reference layout '{ref}' is not a "
                f"registered layout of domain '{domain_name}'. "
                f"Available: {list(domain['layouts'].keys())}"
            )
    if scenario.setup not in domain["setups"]:
        raise ValueError(
            f"scenario '{scenario_id}': setup '{scenario.setup}' is not a "
            f"registered setup of domain '{domain_name}'. "
            f"Available: {list(domain['setups'].keys())}"
        )

    # --------- setup: the run file may name it; it must be the scenario's ---------
    named_setup = user_config.get("setup")
    if named_setup is not None and named_setup != scenario.setup:
        raise ValueError(
            f"setup '{named_setup}': scenario '{scenario_id}' declares setup "
            f"'{scenario.setup}'; a run file's setup must equal the scenario's "
            f"(one setup per scenario, T-L)"
        )

    # --------- layout: selection, or the first reference layout ---------
    layout_id = user_config.get("layout")
    if layout_id is None:
        layout_id = scenario.reference_layouts[0]
    elif layout_id not in domain["layouts"]:
        raise ValueError(
            f"Unknown layout '{layout_id}' for domain '{domain_name}'. "
            f"Available: {list(domain['layouts'].keys())}"
        )

    return domain, layout_id, scenario.setup, scenario


def resolve_model_params(user_config: dict) -> dict:
    '''
    Resolves user config to the run's triple (resolve_triple) and returns
    SimModel's keyword arguments. Used by every start (build_model), so a name
    the registry does not have fails the same way on all of them.
    '''
    domain, layout_id, setup_id, scenario = resolve_triple(user_config)

    return {
        "scenario":         scenario,
        "register_fn":      domain["register_fn"],
        "task_model_schemas": domain["task_model"],
        "state_declarations": domain["states"],
        "timeline_declarations": domain["timeline_facts"],
        "declared_context":   domain["context_knowledge"],
        "layout_path":      domain["layouts"][layout_id],
        "setup_path":       domain["setups"][setup_id],
        "human_aware":      bool(user_config.get("human_aware", OPTION_DEFAULTS["human_aware"])),
        "intention_aware":  bool(user_config.get("intention_aware", OPTION_DEFAULTS["intention_aware"])),
        "assignment_knowledge": bool(user_config.get("assignment_knowledge", OPTION_DEFAULTS["assignment_knowledge"])),
        "context_knowledge":  bool(user_config.get("context_knowledge", OPTION_DEFAULTS["context_knowledge"])),
        "strategy":         user_config.get("strategy", OPTION_DEFAULTS["strategy"]),
        "gate_strategy":    user_config.get("gate_strategy", OPTION_DEFAULTS["gate_strategy"]),
        "cost_strategy":    user_config.get("cost_strategy", OPTION_DEFAULTS["cost_strategy"]),
        "separation_stop":  bool(user_config.get("separation_stop", OPTION_DEFAULTS["separation_stop"])),
        "test_level":       float(user_config.get("test_level", OPTION_DEFAULTS["test_level"])),
        "overrides":        tuple(user_config.get("overrides", ())),
    }


def build_model(user_config: dict) -> SimModel:
    '''The SimModel of a run configuration (resolve_model_params).'''
    return SimModel(**resolve_model_params(user_config))
