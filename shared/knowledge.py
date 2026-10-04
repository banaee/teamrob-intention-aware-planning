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
    - StateDeclaration: one state the domain declares (T-G A5), defined in
                    shared/types.py (a timeline's Window names one) and
                    re-exported here.
    - ContextKnowledge: the declared context knowledge of a domain (T-K part 1,
                    AM26, AM36 to AM38): the suppressed and the ordinary strength,
                    and per foreseeable task its suppressing and raising
                    condition, its raised strength and its recency duration, each
                    with its source. It reaches the recognizer's prior directly, as
                    the task model does; it never drives the human (R1).

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
    - world/human_executor.py → Tree (through the planner)
    - mesa_sim/sim_model.py  → builds the Tree and one TaskModel per robot
    - mesa_sim/sim_agents.py → TaskModel
"""

from dataclasses import dataclass
from typing import Dict, FrozenSet, List, Optional, Sequence, Set, Tuple

from shared.types import (
    ActionSchema, ActionStep, HumanOnlyTask, LANDMARK_TYPE, PersonalTask, Predicate, StateDeclaration, StrengthLevel,
    TaskSchema, TaskStep, WorkTask, destination_derivations,
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

    def get_all_actions(self) -> List[ActionSchema]:
        """Every ActionSchema held (schema validation at construction)."""
        return list(self._actions.values())

    def terminal_actions(self) -> List[ActionSchema]:
        """
        The action schemas that are TERMINAL in this knowledge: the last step
        of some method of a task schema held here, a TaskStep's sub-task
        followed to its own methods' last steps. Once each, by identity, in
        declaration order. Terminal is a property of the schema, whatever its
        binding and wherever else it is called (kitting's robot task model:
        place and wait_at; place is also the second step of
        deliver_with_return). The recognizer's episode boundary is the observed
        agent's completion of one (T-D L1).
        """
        found: List[ActionSchema] = []
        seen: List[TaskSchema] = []

        def visit(task: TaskSchema) -> None:
            if any(t is task for t in seen):
                return
            seen.append(task)
            for method in task.methods:
                if not method.steps:
                    continue
                last = method.steps[-1]
                if isinstance(last, TaskStep):
                    visit(last.task)
                elif not any(a is last.action for a in found):
                    found.append(last.action)

        for task in self._tasks.values():
            visit(task)
        return found

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

    def get_types_with_destination(self) -> Dict[str, FrozenSet[str]]:
        """
        {object type: the destination types declared for it} for every object
        type some task determines a parameter from through the "destination_of"
        lookup — the types whose objects the setup must give a destination, and
        the types that destination may have: the determined parameters'
        parameter_types entries, over every such task (T-B1a; generalised in
        T-G A5: dock_loading's pallet goes to a delivery bay or to the truck).
        A determined parameter the schema types not is an error: its
        destination could not be checked.
        """
        types: Dict[str, set] = {}
        for task in self._tasks.values():
            for var_name, source_var in destination_derivations(task):
                source_type = task.parameter_types.get(source_var)
                if source_type is None:
                    continue
                dest_type = task.parameter_types.get(var_name)
                if dest_type is None:
                    raise ValueError(
                        f"task '{task.name}': determined parameter {var_name} has no type in parameter_types"
                    )
                types.setdefault(source_type, set()).add(dest_type)
        return {source_type: frozenset(dests) for source_type, dests in types.items()}


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
# Context knowledge (T-K part 1): the declared knowledge the recognizer's
# prior reads. Values are modelling assumptions, each with its source.
# ========================================================================

@dataclass(frozen=True)
class Strength:
    """A declared relative weight of a foreseeable task against the assigned tasks as a whole, which contributes 1
    (R3, AM36), with its source. Greater than zero (AM4): checked at construction."""
    value: float
    source: str

    def __post_init__(self):
        if isinstance(self.value, bool) or not isinstance(self.value, (int, float)) or not self.value > 0:
            raise ValueError(f"a strength is a number greater than zero, not {self.value!r} (AM4)")


@dataclass(frozen=True)
class RecencyDuration:
    """The declared duration for which a task's recency fact holds after its observed completion (AM14 to AM16), in
    the physical form a duration binding uses (ISO-8601, PT180S); the body converts it to ticks. With its source."""
    duration: str
    source: str


class ConditionFact:
    """One fact a condition reads (AM11, AM36): a closed family of three, below. `holds` reads the world's predicates
    and the recency facts the mind derives from its memory of observed completions. Not constructed directly."""

    def __init__(self):
        if type(self) is ConditionFact:
            raise TypeError("a ConditionFact is a TimelineFact, an ObjectState or a RecencyFact")

    def holds(self, predicates: Set[Predicate], recent: Sequence[PersonalTask]) -> bool:
        raise NotImplementedError


class TimelineFact(ConditionFact):
    """A timeline fact (a declared state about no object): holds iff its predicate, with no argument, is in the world
    state (the environment emits it on the ticks of its window, AM25, AM40)."""

    def __init__(self, state: StateDeclaration):
        super().__init__()
        if state.object_type is not None:
            raise ValueError(f"'{state.name}' is a state about type '{state.object_type}', not a timeline fact")
        self.state = state

    def holds(self, predicates: Set[Predicate], recent: Sequence[PersonalTask]) -> bool:
        return Predicate(self.state.name, ()) in predicates

    def __repr__(self):
        return f"TimelineFact({self.state.name})"


class ObjectState(ConditionFact):
    """An object state (T-G A5): holds iff the state holds for any object of its declared type in the world state
    (AM44; with at most one A/C switch per layout, that switch's state). Read by the state's name with one argument,
    as the planner reads a ConditionSchema; the environment admits the fact for objects of the declared type only."""

    def __init__(self, state: StateDeclaration):
        super().__init__()
        if state.object_type is None:
            raise ValueError(f"'{state.name}' is a fact about no object, not an object state")
        self.state = state

    def holds(self, predicates: Set[Predicate], recent: Sequence[PersonalTask]) -> bool:
        return any(p.name == self.state.name and len(p.args) == 1 for p in predicates)

    def __repr__(self):
        return f"ObjectState({self.state.name})"


class RecencyFact(ConditionFact):
    """The recency fact of a foreseeable task (AM14, AM27, AM47): holds iff the task is among the recency facts the
    recognizer is given on this run, derived by the mind's memory of observed completions. The task is compared by
    identity."""

    def __init__(self, task: PersonalTask):
        super().__init__()
        self.task = task

    def holds(self, predicates: Set[Predicate], recent: Sequence[PersonalTask]) -> bool:
        return any(t is self.task for t in recent)

    def __repr__(self):
        return f"RecencyFact({self.task.name})"


@dataclass(frozen=True)
class Condition:
    """A conjunction of facts (AM11, AM36): satisfied iff every fact holds. At least one fact; no "not", no "or"
    (T-K part 2's)."""
    facts: Tuple[ConditionFact, ...]

    def __post_init__(self):
        if not self.facts:
            raise ValueError("a condition is one fact or a conjunction of facts; it has none")
        for f in self.facts:
            if not isinstance(f, ConditionFact):
                raise TypeError(f"a condition's fact is a ConditionFact, not {f!r}")

    def satisfied(self, predicates: Set[Predicate], recent: Sequence[PersonalTask]) -> bool:
        return all(f.holds(predicates, recent) for f in self.facts)


@dataclass(frozen=True)
class ForeseeableKnowledge:
    """What the domain declares about one foreseeable task (AM36 to AM38): its suppressing condition, its raising
    condition with its raised strength (present together), and its recency duration (present iff a recency fact of the
    task may be named). The suppressed and the ordinary strength are the domain's, in ContextKnowledge."""
    task: PersonalTask
    suppressing: Optional[Condition] = None
    raising: Optional[Condition] = None
    raised: Optional[Strength] = None
    recency: Optional[RecencyDuration] = None

    def __post_init__(self):
        if not isinstance(self.task, PersonalTask) or isinstance(self.task, HumanOnlyTask):
            raise ValueError(f"'{self.task.name}' is not a foreseeable task (a PersonalTask a robot may be given)")
        if (self.raising is None) != (self.raised is None):
            raise ValueError(f"'{self.task.name}': a raising condition and a raised strength are declared together")


class ContextKnowledge:
    """
    The declared context knowledge of a domain (AM26): the suppressed and the ordinary strength, held for every
    foreseeable task of the domain, and per foreseeable task its ForeseeableKnowledge. One entry per task (checked);
    a RecencyFact names a task of the entries that declares a recency duration (checked). `check_against(task_model)`
    (AM4): every foreseeable task of a robot's task model has an entry and no entry names a task outside it; asked
    when a robot is built with context knowledge on.
    `level(task, predicates, recent)` selects the level (AM36): the suppressing condition first, then the raising,
    else ordinary; `strength` is the level's value. The recognizer only groups and divides (P4).
    """

    def __init__(self, suppressed: Strength, ordinary: Strength, tasks: Sequence[ForeseeableKnowledge]):
        self.suppressed = suppressed
        self.ordinary = ordinary
        self._entries: List[ForeseeableKnowledge] = list(tasks)
        for i, e in enumerate(self._entries):
            if any(o.task is e.task for o in self._entries[:i]):
                raise ValueError(f"context knowledge declares '{e.task.name}' twice")
        for e in self._entries:
            for cond in (e.suppressing, e.raising):
                for f in (cond.facts if cond is not None else ()):
                    if isinstance(f, RecencyFact):
                        named = next((o for o in self._entries if o.task is f.task), None)
                        if named is None or named.recency is None:
                            raise ValueError(f"'{e.task.name}': a condition names the recency fact of "
                                             f"'{f.task.name}', which declares no recency duration here")

    def entries(self) -> List[ForeseeableKnowledge]:
        return list(self._entries)

    def entry(self, task: TaskSchema) -> ForeseeableKnowledge:
        e = next((o for o in self._entries if o.task is task), None)
        if e is None:
            raise ValueError(f"context knowledge declares nothing for '{task.name}'")
        return e

    def check_against(self, task_model: ProceduralKnowledge) -> None:
        """AM4: with context knowledge on, every foreseeable task of the task model declares a strength (has an
        entry), and no entry names a task outside the task model."""
        foreseeable = [t for t in task_model.task_schemas() if isinstance(t, PersonalTask)]
        missing = [t.name for t in foreseeable if not any(e.task is t for e in self._entries)]
        if missing:
            raise ValueError(f"context knowledge declares nothing for the foreseeable tasks {missing} of the task model (AM4)")
        outside = [e.task.name for e in self._entries if not task_model.holds(e.task)]
        if outside:
            raise ValueError(f"context knowledge names {outside}, which are not task schemas of the task model")

    def level(self, task: TaskSchema, predicates: Set[Predicate], recent: Sequence[PersonalTask]) -> StrengthLevel:
        e = self.entry(task)
        if e.suppressing is not None and e.suppressing.satisfied(predicates, recent):
            return StrengthLevel.SUPPRESSED
        if e.raising is not None and e.raising.satisfied(predicates, recent):
            return StrengthLevel.RAISED
        return StrengthLevel.ORDINARY

    def strength_at(self, task: TaskSchema, level: StrengthLevel) -> Strength:
        if level is StrengthLevel.SUPPRESSED:
            return self.suppressed
        if level is StrengthLevel.RAISED:
            return self.entry(task).raised
        return self.ordinary

    def strength(self, task: TaskSchema, predicates: Set[Predicate], recent: Sequence[PersonalTask]) -> Strength:
        return self.strength_at(task, self.level(task, predicates, recent))

    def fact_names(self) -> List[str]:
        """The names of the timeline facts and object states the conditions read, sorted; for the log."""
        names = set()
        for e in self._entries:
            for cond in (e.suppressing, e.raising):
                for f in (cond.facts if cond is not None else ()):
                    if isinstance(f, (TimelineFact, ObjectState)):
                        names.add(f.state.name)
        return sorted(names)

