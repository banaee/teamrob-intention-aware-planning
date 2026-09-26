# domains/discovery.py
"""
Registration by discovery (T-L stage 2, ruling 5). Domain-neutral: a domain's
registry.py builds its `domain_config` entries with these two functions, so
the registry cannot omit an artefact or drift from the files.

- Scenarios: every ScenarioConfig bound at module top level in the domain's
  scenarios package, keyed by its id. No side effect beyond adding to the
  returned dict; a duplicate id (two distinct objects claiming one id) is an
  error at import. Identity is object identity — the same object seen twice
  registers once — never a string parsed out of a name.
- Layouts and setups: registered by the files in their folders, keyed by file
  stem (the file owns the id).

Registration runs at import of domains.<domain>.registry, the one entry every
reader uses (recorded with the T-L entry in docs/design_decisions.md).
"""

import importlib
import pkgutil
from pathlib import Path
from types import ModuleType
from typing import Dict

from shared.types import ScenarioConfig

_REPO_ROOT = Path(__file__).resolve().parent.parent


def discover_scenarios(package: ModuleType) -> Dict[str, ScenarioConfig]:
    """
    Import every module of `package` (sorted by name, so the dict order is
    deterministic) and collect its top-level ScenarioConfig bindings, keyed
    by id and in definition order within a module.
    """
    scenarios: Dict[str, ScenarioConfig] = {}
    owner: Dict[str, str] = {}   # id -> module that registered it, for the error
    for module_info in sorted(pkgutil.iter_modules(package.__path__), key=lambda m: m.name):
        module = importlib.import_module(f"{package.__name__}.{module_info.name}")
        for value in vars(module).values():
            if not isinstance(value, ScenarioConfig):
                continue
            registered = scenarios.get(value.id)
            if registered is value:
                continue   # the same object seen again (e.g. re-exported)
            if registered is not None:
                raise ValueError(
                    f"duplicate scenario id '{value.id}': defined in "
                    f"{owner[value.id]} and again in {module.__name__}"
                )
            scenarios[value.id] = value
            owner[value.id] = module.__name__
    return scenarios


def discover_files(folder: Path) -> Dict[str, str]:
    """
    The artefacts registered by the files in `folder`: every *.json, sorted,
    keyed by file stem, valued by its path relative to the repo root (the
    form every reader opens from the repo root).
    """
    return {path.stem: str(path.relative_to(_REPO_ROOT))
            for path in sorted(folder.resolve().glob("*.json"))}
