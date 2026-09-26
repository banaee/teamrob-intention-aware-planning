"""
mesa_sim/overrides.py

PURPOSE:
    The overrides of a run file (T-L stage 4; design_decisions.md, "Layouts,
    setups and scenarios", ruling 7; glossary §9, "run file" and "override").
    An override changes one fact of a run's artefacts at load, before
    validation. A closed list of three, one class each: an agent's
    start_position (the scenario), a fixed object's position (the layout), a
    movable object's home container (the setup's "initial_container", a
    reference held as a value).

WHAT THIS MODULE DOES:
    - Reads an override's path, `<artefact>.<id>.<fact>`, once, at the input
      boundary (the run file's overrides block, or --override <path>=<value>),
      into one of the three typed classes; every other path is refused, the
      error naming it. Nothing compares strings after that.
    - Types the value by the fact it overrides: two numbers for a position, an
      id for a container.
    - Applies the overrides to the freshly read artefacts (apply_overrides),
      before the loader validates and loads them as for any run.
    - Prints each override in the one form a reader can apply by hand, which
      is also the --override form (Override.line()).
    - Reads and writes the run file's own overrides block for the viewer
      (file_overrides, write_overrides), round-trip so its comments are kept.

WHAT THIS MODULE DOES NOT DO:
    - No validation beyond the override's own target: bounds, container
      existence and the destination checks are the loader's, as for any run.
    - No change during a run (Phase 7's injection path).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, replace
from numbers import Real
from typing import Dict, List, Sequence, Tuple, Type

import yaml
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq

from shared.types import ScenarioConfig


class Override(ABC):
    """One changed fact of a run's artefacts (glossary §9)."""

    @abstractmethod
    def path(self) -> str:
        """The override's path, `<artefact>.<id>.<fact>`."""

    @abstractmethod
    def value_text(self) -> str:
        """The value in the --override form, read back to the same value."""

    def line(self) -> str:
        """The override as printed in the run log and accepted by --override."""
        return f"{self.path()}={self.value_text()}"


@dataclass(frozen=True)
class StartPositionOverride(Override):
    """An agent's start_position (the scenario)."""
    agent_id: str
    position: Tuple[float, float]

    def path(self) -> str:
        return f"scenario.{self.agent_id}.start_position"

    def value_text(self) -> str:
        return f"{self.position[0]!r},{self.position[1]!r}"


@dataclass(frozen=True)
class FixedPositionOverride(Override):
    """A fixed object's position (the layout)."""
    object_id: str
    position: Tuple[float, float]

    def path(self) -> str:
        return f"layout.{self.object_id}.position"

    def value_text(self) -> str:
        return f"{self.position[0]!r},{self.position[1]!r}"


@dataclass(frozen=True)
class HomeContainerOverride(Override):
    """A movable object's home container (the setup's "initial_container"):
    which container is referenced, not what any object is."""
    object_id: str
    container_id: str

    def path(self) -> str:
        return f"setup.{self.object_id}.initial_container"

    def value_text(self) -> str:
        return self.container_id


# The closed list: (artefact, fact) of a path -> the class it is read into.
_OVERRIDABLE: Dict[Tuple[str, str], Type[Override]] = {
    ("scenario", "start_position"): StartPositionOverride,
    ("layout", "position"): FixedPositionOverride,
    ("setup", "initial_container"): HomeContainerOverride,
}

_FORMS = ("scenario.<agent>.start_position=<x>,<y>, layout.<fixed object>.position=<x>,<y>, "
          "setup.<movable object>.initial_container=<container id>")


def _refuse(path: str, why: str) -> ValueError:
    return ValueError(f"override '{path}': {why}. Overridable: {_FORMS}")


def _position(path: str, value) -> Tuple[float, float]:
    """Two numbers: a yaml list of two, or the text `x,y` of --override."""
    if isinstance(value, str):
        value = value.split(",")
        try:
            value = [float(v) for v in value]
        except ValueError:
            raise _refuse(path, "a position is two numbers") from None
    if (not isinstance(value, (list, tuple)) or len(value) != 2
            or any(isinstance(v, bool) or not isinstance(v, Real) for v in value)):
        raise _refuse(path, "a position is two numbers")
    return (float(value[0]), float(value[1]))


def _container(path: str, value) -> str:
    """An id."""
    if not isinstance(value, str) or not value:
        raise _refuse(path, "a container is an id")
    return value


def read_override(path: str, value) -> Override:
    """
    The override a path and its value state: the path read into one of the
    three classes, the value typed by the fact. Any other path (an
    assigned_tasks, a destination, the script, a movable object's position,
    an id, any other fact, a malformed path) is refused, the error naming it.
    """
    segments = path.split(".")
    if len(segments) != 3 or not all(segments):
        raise _refuse(path, "a path is <artefact>.<id>.<fact>")
    artefact, target, fact = segments
    cls = _OVERRIDABLE.get((artefact, fact))
    if cls is None:
        raise _refuse(path, "not overridable")
    if cls is HomeContainerOverride:
        return HomeContainerOverride(target, _container(path, value))
    return cls(target, _position(path, value))


def read_cli_override(text: str) -> Override:
    """--override <path>=<value>: split at the first '='."""
    path, sep, value = text.partition("=")
    if not sep:
        raise _refuse(text, "expected <path>=<value>")
    return read_override(path, value)


def run_overrides(block, cli: Sequence[str]) -> Tuple[Override, ...]:
    """
    The run's overrides: the run file's block (a mapping path -> value, or
    None), then the --override texts, a CLI override replacing the block's for
    the same path as a flag replaces a yaml key; the same path twice on the
    command line is an error. Sorted by path, the order they are printed in.
    """
    if block is None:
        block = {}
    if not isinstance(block, dict):
        raise ValueError(f"overrides: expected a mapping <path>: <value>, got {block!r}")
    by_path = {}
    for path, value in block.items():
        override = read_override(str(path), value)
        by_path[override.path()] = override
    cli_paths = set()
    for text in cli:
        override = read_cli_override(text)
        if override.path() in cli_paths:
            raise _refuse(override.path(), "given twice on the command line")
        cli_paths.add(override.path())
        by_path[override.path()] = override
    return tuple(by_path[p] for p in sorted(by_path))


def apply_overrides(overrides: Sequence[Override], scenario: ScenarioConfig,
                    layout: dict, setup: dict, layout_path: str, setup_path: str) -> ScenarioConfig:
    """
    Applies the overrides to the artefacts as read, before anything is
    validated or built: the layout and setup dicts in place (freshly read by
    the loader, never shared), the scenario as a copy (the registered literal
    is never changed). An override that names an agent or an object the
    artefact does not have is an error naming its path.
    Returns the scenario the run loads.
    """
    if not overrides:
        return scenario
    layout_objects = {obj["id"]: obj for obj in layout.get("env_objects", [])}
    setup_objects = {obj["id"]: obj for obj in setup.get("env_objects", [])}
    agents: List = list(scenario.agents)
    for override in overrides:
        if isinstance(override, FixedPositionOverride):
            if override.object_id in setup_objects:
                raise _refuse(override.path(), f"'{override.object_id}' is a movable object of setup "
                              f"'{setup_path}'; a movable object's position is its container's")
            if override.object_id not in layout_objects:
                raise _refuse(override.path(), f"no object '{override.object_id}' in layout '{layout_path}'")
            layout_objects[override.object_id]["position"] = list(override.position)
        elif isinstance(override, HomeContainerOverride):
            if override.object_id not in setup_objects:
                raise _refuse(override.path(), f"no object '{override.object_id}' in setup '{setup_path}'")
            setup_objects[override.object_id]["initial_container"] = override.container_id
        elif isinstance(override, StartPositionOverride):
            index = next((i for i, a in enumerate(agents) if a.agent_id == override.agent_id), None)
            if index is None:
                raise _refuse(override.path(), f"no agent '{override.agent_id}' in scenario '{scenario.id}'")
            agents[index] = replace(agents[index], start_position=override.position)
        else:
            raise TypeError(f"not an override: {override!r}")
    return replace(scenario, agents=agents)


def file_overrides(run_path: str) -> Tuple[Override, ...]:
    """The overrides the run file's own block states (none from the command line)."""
    with open(run_path, "r") as f:
        return run_overrides((yaml.safe_load(f) or {}).get("overrides"), ())


def write_overrides(run_path: str, overrides: Sequence[Override]) -> None:
    """
    Writes the run file's overrides block (the viewer's edit, ruling 7): the
    block replaced by these overrides, sorted by path, and removed when there
    are none. Round-trip (ruamel.yaml): every other key and every comment of
    the file is kept, since the run file is edited by people.
    """
    rt = YAML()
    rt.preserve_quotes = True
    with open(run_path, "r") as f:
        data = rt.load(f)
    block = CommentedMap()
    for override in sorted(overrides, key=lambda o: o.path()):
        if isinstance(override, HomeContainerOverride):
            block[override.path()] = override.container_id
        else:
            position = CommentedSeq(override.position)
            position.fa.set_flow_style()
            block[override.path()] = position
    if block:
        data["overrides"] = block
    elif "overrides" in data:
        del data["overrides"]
    with open(run_path, "w") as f:
        rt.dump(data, f)
