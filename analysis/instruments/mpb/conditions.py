#!/usr/bin/env python3
"""
conditions.py — T-F part 1's three conditions as the planning test-bed reads them (design_decisions.md and
design_records.md, "T-F part 1: the conditions human-unaware and intention-unaware"; glossary §9): a run's settings,
the condition they make, and whether the robot's and the human's objects are separate (G).

- `stated(run_file)`: the settings a run file states, its absent keys at the loader's fallback (`mesa_sim/run_mesa.py`,
  `resolve_model_params`: both conditions' options and both knowledge options on, `single_task`).
- `effective(settings)`: R5 as the records state it, the instrument's own reading (not the framework's loader): an
  option that is off sets every option above it to off; `human_aware` off sets `intention_aware` and both knowledge
  options off, `intention_aware` off both knowledge options.
- `from_header(log)`: the effective settings the run itself printed (its `[run]` header).
- `objects_separate(run_file)`: no movable object of the setup is bound both by a task of the robot's pool and by a
  task the human's script names (`Script.tasks()`). G: only then does a human-unaware robot move as the robot alone;
  elsewhere a difference is a recorded finding. A fixed object (a shelf, a table) may be shared: it changes no fact the
  robot's mind reads (B's corner cases are about the robot's own task and object).

    conditions.py <run file> <run.log> <out dir>   writes <out dir>/settings.json (the settings, R5's reading and the
                                                   header's, the condition, whether they agree, objects_separate,
                                                   the human's script dependence)

Standard library and yaml at import; the registry only inside `objects_separate` (the oracle imports `stated`,
`effective` and `Condition` only, within its independence boundary).
"""
import json
import sys
from dataclasses import asdict, dataclass, replace
from enum import Enum
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]


class Condition(Enum):
    """The robot's three conditions (glossary §9)."""
    HUMAN_UNAWARE = "human-unaware"
    INTENTION_UNAWARE = "intention-unaware"
    INTENTION_AWARE = "intention-aware"


@dataclass(frozen=True)
class Settings:
    """A run's settings, the result table's columns (I)."""
    human_aware: bool
    intention_aware: bool
    assignment_knowledge: bool
    context_knowledge: bool
    strategy: str

    @property
    def condition(self) -> Condition:
        if not self.human_aware:
            return Condition.HUMAN_UNAWARE
        if not self.intention_aware:
            return Condition.INTENTION_UNAWARE
        return Condition.INTENTION_AWARE


def stated(run_file) -> Settings:
    cfg = yaml.safe_load(open(run_file))
    return Settings(bool(cfg.get("human_aware", True)), bool(cfg.get("intention_aware", True)),
                    bool(cfg.get("assignment_knowledge", True)), bool(cfg.get("context_knowledge", True)),
                    cfg.get("strategy", "single_task"))


def effective(s: Settings) -> Settings:
    """R5 (design_records.md, "T-F part 1", R5's form)."""
    intention = s.intention_aware and s.human_aware
    return replace(s, intention_aware=intention, assignment_knowledge=s.assignment_knowledge and intention,
                   context_knowledge=s.context_knowledge and intention)


def from_header(log_path) -> Settings:
    header = next(l for l in open(log_path) if l.startswith("[run] "))
    fields = dict(f.split("=", 1) for f in header.split()[2:] if "=" in f)
    on = lambda k: fields[k] == "on"
    return Settings(on("human_aware"), on("intention_aware"), on("assignment_knowledge"), on("context_knowledge"),
                    fields["strategy"])


def scenario_of(run_file):
    import importlib
    cfg = yaml.safe_load(open(run_file))
    domain_config = importlib.import_module(f"domains.{cfg['domain']}.registry").domain_config
    return domain_config, domain_config["scenarios"][cfg["scenario"]]


def objects_separate(run_file) -> bool:
    domain_config, scenario = scenario_of(run_file)
    setup = json.load(open(ROOT / domain_config["setups"][scenario.setup]))
    movable = {o["id"] for o in setup["env_objects"]}
    bound = lambda tasks: {c.value for t in tasks for c in t.bindings.values()} & movable
    robot = bound(t for a in scenario.agents if a.agent_type == "robot" for t in (a.assigned_tasks or []))
    human = bound(t for a in scenario.agents if a.agent_type == "human" for t in a.scheduled_tasks.tasks())
    return not (robot & human)


def dependence(run_file) -> str:
    _, scenario = scenario_of(run_file)
    return next(a for a in scenario.agents if a.agent_type == "human").scheduled_tasks.dependence.value


if __name__ == "__main__":
    sys.path[:0] = [str(ROOT), str(ROOT / "mesa_sim")]
    run_file, log_path, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    reading, printed = effective(stated(run_file)), from_header(log_path)
    cfg = yaml.safe_load(open(run_file))
    json.dump(dict(run_file=str(run_file), domain=cfg["domain"], scenario=cfg["scenario"],
                   layout=cfg.get("layout") or scenario_of(run_file)[1].reference_layouts[0],
                   stated=asdict(stated(run_file)), effective=asdict(reading), header=asdict(printed),
                   agree=reading == printed, condition=reading.condition.value,
                   min_separation=float(next(l for l in open(log_path) if l.startswith("[run] "))
                                        .split("min_separation=")[1].split()[0]),
                   objects_separate=objects_separate(run_file), dependence=dependence(run_file)),
              open(out / "settings.json", "w"), indent=1)
    print(f"{run_file}: {reading.condition.value}; header {'agrees' if reading == printed else 'DISAGREES'} with R5's "
          f"reading; objects separate: {objects_separate(run_file)}")
