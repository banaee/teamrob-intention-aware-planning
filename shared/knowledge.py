"""
shared/knowledge.py

PURPOSE:
    Knowledge layer for the cognitive layer: procedural knowledge in the two
    forms of T-H, and background context.
    - ProceduralKnowledge: how things are done — task schemas with their
                    methods, action schemas, microactions, costs. The base of
                    the two forms below; the planner reads it and serves both.
    - Tree:         the world's tree of task schemas, one per use case. The
                    human's script (its planner) uses it.
    - TaskModel:    one robot's task model, the subset of the tree the robot is
                    given, by whole schemas. The robot's recognizer, projector,
                    planner and meta-planner use it only.
    - ContextKnowledge: background context facts (shift info, environment
                    state) used by IR for ω_context weighting.

WHAT THIS MODULE DOES:
    - Holds typed schema objects and answers queries with them, not strings
    - Validates the knowledge objects at construction: every method step calls
      a schema of the object, by identity; the landmark rule (Tree); the
      HumanOnlyTask rejection and the every-WorkTask requirement (TaskModel).
      The robot's inference reads no human-only-ness; only this construction-time
      validation does (T-H).

WHAT THIS MODULE DOES NOT DO:
    - Does NOT parse YAML for task or action schema definitions
    - Does NOT resolve variable bindings (that is shared/planner.py)
    - Does NOT know about Mesa, ROS, or any simulator
    - Does NOT hold observable/sensor-based state (that is WorldState)
    - Does NOT handle scenarios or agent assignments (that is sim_model.py)

USED BY:
    - shared/recognizer.py, shared/projection.py, shared/meta_planner.py → TaskModel
    - shared/planner.py      → ProceduralKnowledge (a Tree for the human's
                               script, a TaskModel for the robot)
    - domains/script.py      → Tree
    - mesa_sim/sim_model.py  → builds the Tree and one TaskModel per robot
    - mesa_sim/sim_agents.py → TaskModel, ContextKnowledge.default()
"""

from typing import Dict, List, Optional, Sequence, Tuple

from shared.types import (
    ActionSchema, ActionStep, HumanOnlyTask, LANDMARK_TYPE, TaskSchema, TaskStep, WorkTask,
    destination_derivations,
)


class ProceduralKnowledge:
    """
    How things are done: task schemas (with their methods) and action schemas,
    keyed by name, the domain's microactions, and per-action costs. Every method
    step calls a schema held here, by identity: an ActionStep one of `actions`,
    a TaskStep one of `tasks`. Constructed as a Tree or a TaskModel, never
    directly.
    `costs`: per-action costs the projector reads (Phase 4); empty in Mesa.
    """

    def __init__(self, tasks: Sequence[TaskSchema], actions: Sequence[ActionSchema],
                 microactions: List[str], costs: Optional[Dict[str, float]] = None):
        if type(self) is ProceduralKnowledge:
            raise TypeError("ProceduralKnowledge is not constructed directly: build a Tree or a TaskModel")
        self._costs: Dict[str, float] = dict(costs or {})
        self._tasks: Dict[str, TaskSchema] = {}
        for task in tasks:
            if task.name in self._tasks:
                raise ValueError(f"two task schemas are named '{task.name}'")
            self._tasks[task.name] = task
        self._actions: Dict[str, ActionSchema] = {}
        for action in actions:
            if action.name in self._actions:
                raise ValueError(f"two action schemas are named '{action.name}'")
            self._actions[action.name] = action
        self._microactions = list(microactions)
        for task in self._tasks.values():
            for method in task.methods:
                for step in method.steps:
                    if isinstance(step, ActionStep):
                        if not any(a is step.action for a in self._actions.values()):
                            raise ValueError(
                                f"task '{task.name}', method '{method.name}': step calls action "
                                f"'{step.action.name}', which is not an action schema of this knowledge"
                            )
                    elif isinstance(step, TaskStep):
                        if not self.holds(step.task):
                            raise ValueError(
                                f"task '{task.name}', method '{method.name}': step calls task "
                                f"'{step.task.name}', which is not a task schema of this knowledge"
                            )
                    else:
                        raise TypeError(
                            f"task '{task.name}', method '{method.name}': step {step!r} is "
                            f"neither an ActionStep nor a TaskStep"
                        )

    # ----------------------------------------------------------------------
    # Task queries
    # ----------------------------------------------------------------------

    def holds(self, schema: TaskSchema) -> bool:
        """Whether `schema` is one of the task schemas held here, by identity."""
        return any(t is schema for t in self._tasks.values())

    def task_schemas(self) -> List[TaskSchema]:
        """Every task schema held, in declaration order."""
        return list(self._tasks.values())

    # ----------------------------------------------------------------------
    # Action queries
    # ----------------------------------------------------------------------

    def get_action_schema(self, action_name: str) -> Optional[ActionSchema]:
        """Return ActionSchema for an action type, or None if not found."""
        return self._actions.get(action_name)

    def get_all_actions(self) -> List[ActionSchema]:
        """Every ActionSchema held (schema validation at construction)."""
        return list(self._actions.values())

    def get_microactions(self) -> List[str]:
        """Terminal microactions: ['STEP', 'GRASP', 'RELEASE', 'STAND']."""
        return self._microactions

    # ----------------------------------------------------------------------
    # Cost data (Phase 4)
    # ----------------------------------------------------------------------

    def get_cost(self, key: str) -> Optional[float]:
        """Return cost value by key from costs.yaml, or None if not found."""
        return self._costs.get(key)


class Tree(ProceduralKnowledge):
    """
    The world's tree of task schemas for one use case (T-H): every schema a
    WorkTask, a PersonalTask or a HumanOnlyTask, with the action schemas its
    methods call. Built by the domain's registry. The landmark rule is checked
    here: only a HumanOnlyTask may type a parameter as a landmark.
    """

    def __init__(self, tasks: Sequence[TaskSchema], actions: Sequence[ActionSchema],
                 microactions: List[str], costs: Optional[Dict[str, float]] = None):
        super().__init__(tasks, actions, microactions, costs)
        for task in self._tasks.values():
            if isinstance(task, HumanOnlyTask):
                continue
            for var_name, type_name in task.parameter_types.items():
                if type_name == LANDMARK_TYPE:
                    raise ValueError(
                        f"task '{task.name}': parameter {var_name} is typed '{LANDMARK_TYPE}'; "
                        f"only a HumanOnlyTask may type a parameter as a landmark"
                    )

    def get_types_with_destination(self) -> Dict[str, Tuple[str, Optional[str]]]:
        """
        {object type: (task name, destination type)} for every object type
        some task determines a parameter from through the "destination_of"
        lookup — the types whose objects the layout must give a destination,
        and the type that destination must have (the determined parameter's
        parameter_types entry; None if the schema types it not). T-B1a.
        """
        types: Dict[str, Tuple[str, Optional[str]]] = {}
        for task in self._tasks.values():
            for var_name, source_var in destination_derivations(task):
                source_type = task.parameter_types.get(source_var)
                if source_type is not None:
                    types.setdefault(source_type, (task.name, task.parameter_types.get(var_name)))
        return types


class TaskModel(ProceduralKnowledge):
    """
    One robot's task model (T-H): the subset of `tree` the robot is given,
    chosen by WHOLE schemas. Every WorkTask of the tree is in it (the robot plans
    its own tasks with it); a PersonalTask may be omitted; a HumanOnlyTask is
    rejected. Its schemas are the tree's own objects, and so are the action
    schemas, the microactions and the costs: all of the tree's. A TaskStep's
    sub-task must itself be in the model. The hypothesis space is built from it
    and the layout.
    """

    def __init__(self, tree: Tree, schemas: Sequence[TaskSchema]):
        for schema in schemas:
            if not tree.holds(schema):
                raise ValueError(f"task model: '{schema.name}' is not a task schema of the tree")
            if isinstance(schema, HumanOnlyTask):
                raise ValueError(
                    f"task model: '{schema.name}' is a HumanOnlyTask, which is never given to a robot"
                )
        missing = [t.name for t in tree.task_schemas()
                   if isinstance(t, WorkTask) and not any(s is t for s in schemas)]
        if missing:
            raise ValueError(f"task model: every WorkTask of the tree is in it; missing: {missing}")
        super().__init__(schemas, tree.get_all_actions(), tree.get_microactions(), tree._costs)


# ========================================================================
# Context knowledge — e.g. shift duration, room temperature, etc. that may affect human
# behavior and should be considered by the intention recognizer and planner.
# ========================================================================

class ContextKnowledge:
    def __init__(
        self,
        shift_start_step: int = 0,
        room_temperature: float = 21.0,   # default comfortable temperature
        metadata: dict = None,
    ):
        self.shift_start_step = shift_start_step
        self.room_temperature = room_temperature
        self.metadata = metadata or {}

    @classmethod
    def default(cls) -> "ContextKnowledge":
        """Default context — used when no external context source is available."""
        return cls()

    def shift_duration(self, current_step: int) -> int:
        """Steps elapsed since shift start — proxy for fatigue."""
        return current_step - self.shift_start_step
    