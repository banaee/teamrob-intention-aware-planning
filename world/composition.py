"""
world/composition.py

PURPOSE:
    What a scenario is made of, and its scenario coverage (T-H follow-up):
    computed at load from the human's script and an observing robot, never
    stored on the ScenarioConfig, so no declared tag can drift from the script.
    The author declares only the scenario's purpose, in its description, as
    text (glossary §7, label C).

        scenario_composition(script, robot)    (Composition, ScenarioCoverage)

    The composition is four sets of existing types: the task classes the
    script names, its decisions, its triggers, and the coverage results of its
    tasks (world/queries.coverage). The scenario coverage is one task's
    coverage lifted to the scenario: which non-covered results are present. It
    depends on the robot's task model, so it is a property of the run
    configuration, not of the script alone.

    THE EXIT WALK: the authoring convention's terminal walk out of the
    workspace (design_decisions.md, "SCENARIO-AUTHORING CONVENTION") is not
    counted in the scenario coverage. It is the script's last entry when its
    task is a HumanOnlyTask whose only goal binding is a landmark and that
    decomposes to exactly one movement action to that landmark (every method:
    one action step, whose action declares a movement target bound to the
    landmark), and it carries no events: a rule on type, structure and
    position, never on a schema's name. A terminal go_to_and_stand (a walk and
    a stand) is counted. The composition still holds it.

WHAT THIS MODULE DOES NOT DO:
    - It selects nothing: a batch run's or the viewer's selector calls
      scenario_composition (TODO-110, not built).
    - It does not read the record: the script is what the scenario contains,
      the record what one run did.
"""

from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet, Iterable, List, Optional, Tuple, Type

from shared.types import (
    LANDMARK_TYPE, ActionStep, AfterAction, Decision, Drop, DuringAction, HumanOnlyTask, MethodSchema, PersonalTask,
    Script, ScriptEntry, Start, TaskInstance, TaskSchema, Trigger, Var, WorkTask, goal_bindings,
)
from world.queries import BindingAbsent, Coverage, Covered, ObservingRobot, TaskAbsent, coverage


class ScenarioCoverage(Enum):
    """Coverage lifted from one task to the scenario: which non-covered
    results its tasks have, the exit walk not counted."""
    MODELLED_ONLY = "modelled_only"
    TASK_ABSENT = "task_absent"
    BINDING_ABSENT = "binding_absent"
    BOTH = "both"


# The members of each set, in the order they are printed. The task classes are
# listed most specific first for the lookup (a HumanOnlyTask is a PersonalTask).
_TASK_CLASSES: Tuple[Type[TaskSchema], ...] = (WorkTask, PersonalTask, HumanOnlyTask)
_DECISIONS: Tuple[Type[Decision], ...] = (Start, Drop)
_TRIGGERS: Tuple[Type[Trigger], ...] = (AfterAction, DuringAction)   # Now never appears in a script
_COVERAGE: Tuple[Type[Coverage], ...] = (Covered, TaskAbsent, BindingAbsent)


@dataclass(frozen=True)
class Composition:
    """What a scenario's script is made of, against one observing robot."""
    task_classes: FrozenSet[Type[TaskSchema]]
    decisions: FrozenSet[Type[Decision]]
    triggers: FrozenSet[Type[Trigger]]
    coverage: FrozenSet[Type[Coverage]]

    def __repr__(self):
        return (f"tasks={_names(self.task_classes, _TASK_CLASSES)} decisions={_names(self.decisions, _DECISIONS)} "
                f"triggers={_names(self.triggers, _TRIGGERS)} coverage={_names(self.coverage, _COVERAGE)}")


def scenario_composition(script: Script, robot: ObservingRobot) -> Tuple[Composition, ScenarioCoverage]:
    """
    The script's composition and its scenario coverage against `robot`. Every
    task is Script.tasks() (each entry's, and each Start's). The scenario
    coverage reads the coverage results of the same tasks, less the exit walk.
    """
    tasks = script.tasks()
    events = [ev for entry in script.entries for ev in entry.events]
    composition = Composition(
        task_classes=frozenset(_task_class(t.schema) for t in tasks),
        decisions=frozenset(type(ev.decision) for ev in events),
        triggers=frozenset(type(ev.trigger) for ev in events),
        coverage=frozenset(type(coverage(t, robot)) for t in tasks),
    )
    exit_walk = _exit_walk(script)
    counted = frozenset(type(coverage(t, robot)) for t in tasks if t is not exit_walk)
    return composition, _scenario_coverage(counted)


def _task_class(schema: TaskSchema) -> Type[TaskSchema]:
    return next(c for c in reversed(_TASK_CLASSES) if isinstance(schema, c))


def _exit_walk(script: Script) -> Optional[TaskInstance]:
    """The last entry's task when it is the convention's exit walk: a
    HumanOnlyTask whose only goal binding is a landmark and that decomposes to
    exactly one movement action to that landmark, carrying no events."""
    if not script.entries:
        return None
    last: ScriptEntry = script.entries[-1]
    if last.events or not isinstance(last.task.schema, HumanOnlyTask):
        return None
    goal = goal_bindings(last.task)
    if len(goal) != 1:
        return None
    (var,) = goal
    if last.task.schema.parameter_types.get(var.name) != LANDMARK_TYPE:
        return None
    return last.task if all(_one_walk_to(method, var) for method in last.task.schema.methods) else None


def _one_walk_to(method: MethodSchema, landmark: Var) -> bool:
    """The method's steps are exactly one action step, a movement action
    (it declares a movement target) whose target is bound to `landmark`."""
    if len(method.steps) != 1 or not isinstance(method.steps[0], ActionStep):
        return False
    step = method.steps[0]
    key = step.action.movement_target_key
    return key is not None and step.bindings.get(Var(key)) == landmark


def _scenario_coverage(results: FrozenSet[Type[Coverage]]) -> ScenarioCoverage:
    task_absent, binding_absent = TaskAbsent in results, BindingAbsent in results
    if task_absent and binding_absent:
        return ScenarioCoverage.BOTH
    if task_absent:
        return ScenarioCoverage.TASK_ABSENT
    if binding_absent:
        return ScenarioCoverage.BINDING_ABSENT
    return ScenarioCoverage.MODELLED_ONLY


def _names(present: Iterable[type], order: Tuple[type, ...]) -> str:
    listed: List[str] = [c.__name__ for c in order if c in present]
    return ",".join(listed) if listed else "-"
