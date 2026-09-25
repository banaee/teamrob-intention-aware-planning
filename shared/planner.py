"""
shared/planner.py

PURPOSE:
    The robot's "Adaptive planning" module.
    Produces a sequence of GroundedActions for the robot to execute,
    adapted to the current belief about what the human intends to do.

WHAT THIS MODULE DOES:
    - Fetches TaskSchema from its ProceduralKnowledge (a robot's TaskModel, or the
      Tree for the human's script)
    - Selects applicable method (first method whose guards hold in WorldState);
      decompose() exposes that selection to the recognizer, which must never
      pick a method by position
    - Grounds each ActionStep: resolves Var bindings to Const values
    - Recursively decomposes each TaskStep (a compound sub-task)
    - Returns a flat AbstractPlan (single task, executor-facing)

WHAT THIS MODULE DOES NOT DO:
    - Does NOT parse strings — all structure comes from typed schema objects
    - Does NOT hardcode variable names — derivations declared in MethodSchema
    - Does NOT decide whether to replan (that is replanning.py / meta_planner.py)
    - Does NOT execute actions (that is mesa_sim/executor.py)
    - Does NOT update beliefs (that is recognizer.py)
    - Does NOT schedule across tasks (that is meta_planner.py)

GROUNDING:
    A task arrives as a TaskInstance: its schema object (held by this planner's
    knowledge, by identity) and its bindings, e.g. {Var("?item"): Const("item_3")}.
    agent_id is passed explicitly as execution context — injected as ?agent.
    The planner resolves each step's bindings:
        Var("?item")           → looked up in the task bindings / accumulated bindings
        Const("kitting_table") → used as-is
    All GroundedActions carry a fully instantiated completion_predicate
    (Predicate with Const args only) — executor checks set membership directly.

RECURSION:
    A TaskStep holds a sub-task's TaskSchema; the planner recurses into it with
    the step's bindings. The result is flattened
    into the same action list. Output is always a flat AbstractPlan.
"""

from typing import Dict, List, Optional, Tuple
import logging

from shared.types import (
    ProcessCompletion, Var, Const, Predicate, ConditionSchema,
    GroundedAction, AbstractPlan, BeliefState, WorldState,
    TaskSchema, TaskInstance, ActionSchema, MethodSchema, Step, ActionStep, TaskStep, DESTINATION_LOOKUP,
)
from shared.knowledge import ProceduralKnowledge

logger = logging.getLogger(__name__)


class DecompositionError(ValueError):
    """
    The task cannot be decomposed in THIS world: no method's guards hold, or a
    derived-var lookup has no value here. A fact about the world, not about the
    schema — the same task may decompose a tick later. Callers that plan for
    themselves let it propagate (an unexecutable plan is an error); callers that
    only ask whether a task is possible for someone else (the recognizer, per
    hypothesis) catch it and score the hypothesis neutrally. Schema errors —
    an unknown task or step, an unbound variable, an unknown lookup function —
    stay plain ValueError: they are modelling mistakes and must surface loudly.
    """


class AdaptivePlanner:

    def __init__(self, knowledge: ProceduralKnowledge):
        self.knowledge = knowledge

    def plan(
        self,
        task: TaskInstance,
        agent_id: str,                  # executing agent — injected as ?agent, not a task binding
        belief: BeliefState,
        world: WorldState,
        current_plan: AbstractPlan | None = None,
    ) -> AbstractPlan:
        """
        Produce a flat AbstractPlan for a single task.
        Recursively decomposes sub-tasks until all steps are primitive ActionSchemas.
        Guard evaluation selects the applicable method per task/sub-task.
        """
        actions = self.decompose(task, agent_id, world)

        return AbstractPlan(
            goal_intention=task.schema.name,
            actions=actions,
        )

    def decompose(
        self,
        task: TaskInstance,
        agent_id: str,
        world: WorldState,
        method: Optional[str] = None,
    ) -> List[GroundedAction]:
        """
        The flat GroundedAction list for one task, grounded for `agent_id`
        against `world`: guard-selected method, derived vars, every step Var
        resolved through the task and step bindings. `method` names one of the
        task's methods to use instead of the first applicable one; it must
        apply in `world` (the human action script's expand(task, method=),
        T-C2a). Sub-tasks are selected as always. plan() wraps this for the
        executor; the recognizer calls it directly, once per hypothesis and
        tick, to learn which actions the observed agent would perform if it
        held that intention — the same selection, not a parallel one.
        Raises DecompositionError when no method applies in this world.
        The task's schema must be one this planner's knowledge holds, by
        identity (a robot's planner decomposes only its task model's schemas);
        a schema it does not hold is a ValueError.
        """
        if not self.knowledge.holds(task.schema):
            raise ValueError(
                f"AdaptivePlanner: task '{task.schema.name}' is not a task schema of this planner's knowledge"
            )
        # Build initial bindings: task bindings + agent injection
        bindings: Dict[str, str] = {"?agent": agent_id}
        bindings.update({var.name: const.value for var, const in task.bindings.items()})
        return self._decompose_schema(task.schema, bindings, world, method)

    def is_complete(
        self,
        task: TaskInstance,
        agent_id: str,
        world: WorldState,
    ) -> bool:
        """
        Whether the task is already done in `world`: the completion condition
        of the TERMINAL action of its decomposition for `agent_id` holds. A
        TaskSchema declares no goal of its own — a task's completion is the
        completion of the last action of the method its guards select — so
        the test is derived here from the same decomposition the executor
        and the recognizer use, never from a predicate name. Indifferent to
        who did it: obj_at(item, table) holds whoever delivered the item, and
        that is the fact wanted — the task cannot be done again. A terminal
        ProcessCompletion (no predicate) never reads as complete. Raises
        DecompositionError as decompose() does: a task that cannot be
        decomposed here cannot be planned here either.
        """
        actions = self.decompose(task, agent_id, world)
        predicate = actions[-1].completion_predicate if actions else None
        return predicate is not None and predicate in world.predicates

    # ------------------------------------------------------------------
    # Internal decomposition
    # ------------------------------------------------------------------

    def _decompose_schema(
        self,
        task_schema: TaskSchema,
        bindings: Dict[str, str],
        world: WorldState,
        method_name: Optional[str] = None,
    ) -> List[GroundedAction]:
        """
        The flat GroundedAction list for one task schema: a TaskStep recurses
        into its sub-task's schema, an ActionStep grounds its action schema.
        The step holds the schema object; no name is looked up.
        """
        # Parameters the task declares determined by another parameter (e.g.
        # the item's destination table) are filled before method selection
        bindings = self._resolve_lookups(
            task_schema.determined_parameters, bindings, world, f"Task: '{task_schema.name}'")

        method, bindings = self._select_method(task_schema, bindings, world, method_name)  # returns method + updated bindings

        # Resolve derived vars declared on this method before processing steps
        resolved_bindings = self._resolve_derived_vars(method, bindings, world)

        actions: List[GroundedAction] = []
        for step in method.steps:
            step_bindings = self._resolve_step_bindings(step, resolved_bindings)

            if isinstance(step, TaskStep):
                actions.extend(self._decompose_schema(step.task, step_bindings, world))
            elif isinstance(step, ActionStep):
                actions.append(self._ground_action(step.action, step_bindings))
            else:
                raise TypeError(
                    f"AdaptivePlanner: step {step!r} in method '{method.name}' of task "
                    f"'{task_schema.name}' is neither an ActionStep nor a TaskStep"
                )

        return actions

    def _select_method(
        self,
        task_schema: TaskSchema,
        bindings: Dict[str, str],
        world: WorldState,
        method_name: Optional[str] = None,
        ) -> Tuple[MethodSchema, Dict[str, str]]:
        """
        Return the first method whose guards are all satisfied in world, along
        with bindings updated to include any vars discovered by existential
        guard matching. With `method_name`, only that method is considered.
        Empty guard list = unconditional (always passes).
        Raises DecompositionError if no method is applicable.
        """
        methods = task_schema.methods
        if method_name is not None:
            methods = [m for m in methods if m.name == method_name]
            if not methods:
                raise ValueError(
                    f"AdaptivePlanner: task '{task_schema.name}' has no method '{method_name}'"
                )
        for method in methods:
            resolved = self._guards_satisfied(method, bindings, world)
            if resolved is not None:
                return method, resolved

        raise DecompositionError(
            f"AdaptivePlanner: no applicable method for task '{task_schema.name}' "
            f"in current world state. Bindings: {bindings}"
        )
    
    def _guards_satisfied(
        self,
        method: MethodSchema,
        bindings: Dict[str, str],
        world: WorldState,
    ) -> Optional[Dict[str, str]]:
        """
        Try to satisfy all guards for this method against world state, in order.
        Guards may (a) test an already-bound predicate against world.predicates,
        (b) existentially bind one new Var by searching world.predicates, or
        (c) invoke a built-in evaluator (currently only 'not_equal') rather than
        a world.predicates lookup.
        Returns the bindings dict (original + any newly-discovered vars) if the
        method is applicable, or None if any guard fails.
        Empty guard list → vacuously satisfied, original bindings returned unchanged.
        """
        current = dict(bindings)

        for guard in method.guards:
            if guard.name == "not_equal":
                left, right = guard.args
                left_val = current[left.name] if isinstance(left, Var) else left.value
                right_val = current[right.name] if isinstance(right, Var) else right.value
                if left_val == right_val:
                    return None
                continue

            unbound = [a for a in guard.args if isinstance(a, Var) and a.name not in current]

            if not unbound:
                # fully bound — test membership, same as before
                grounded = self._ground_predicate(guard, current)
                if grounded not in world.predicates:
                    return None
                continue

            if len(unbound) > 1:
                raise ValueError(
                    f"AdaptivePlanner: guard '{guard.name}' in method '{method.name}' "
                    f"has more than one unbound variable "
                    f"({[v.name for v in unbound]}); existential matching supports "
                    f"binding at most one variable per guard."
                )

            # Existential match: find predicates with the same name and matching
            # bound-arg positions; bind the one free position.
            free_var = unbound[0]
            free_index = guard.args.index(free_var)
            matches = []
            for pred in world.predicates:
                if pred.name != guard.name or len(pred.args) != len(guard.args):
                    continue
                ok = True
                for i, arg in enumerate(guard.args):
                    if i == free_index:
                        continue
                    bound_val = current[arg.name] if isinstance(arg, Var) else arg.value
                    if pred.args[i].value != bound_val:
                        ok = False
                        break
                if ok:
                    matches.append(pred.args[free_index].value)

            if not matches:
                return None

            # Deterministic tie-break — world.predicates is a Set, so iteration
            # order isn't a reliable "first match". Not expected to matter today
            # (e.g. 'carrying' is a scalar field, so 'holding' can't have two
            # matches for one agent), but sort rather than rely on set order.
            current[free_var.name] = sorted(matches)[0]

        return current

    def _resolve_derived_vars(
        self,
        method: MethodSchema,
        bindings: Dict[str, str],
        world: WorldState,
    ) -> Dict[str, str]:
        return self._resolve_lookups(method.derived_vars, bindings, world, f"Method: '{method.name}'")

    def _resolve_lookups(
        self,
        lookups: Dict[str, tuple],
        bindings: Dict[str, str],
        world: WorldState,
        where: str,
    ) -> Dict[str, str]:
        """
        Resolve {var_name: (lookup_fn, source_var)} against the world: a
        method's derived_vars or a task's determined_parameters, the same
        lookups for both. `where` names the declaring method or task in errors.
        """
        resolved = dict(bindings)
        for var_name, (lookup_fn, source_var) in lookups.items():
            source_val = resolved.get(source_var)
            if source_val is None:
                raise ValueError(
                    f"AdaptivePlanner: derived var '{var_name}' depends on "
                    f"'{source_var}' which is not bound. {where}"
                )
            if lookup_fn == "zone_of":
                derived_val = world.object_zones.get(source_val)
            elif lookup_fn == "home_container_of":
                derived_val = world.object_home_container.get(source_val)
            elif lookup_fn == DESTINATION_LOOKUP:
                # The station's destination is the default: a task instance
                # that binds the var sends the object where it says (a human's
                # scripted deviation), so the binding is kept (T-B1a). Only this
                # lookup yields to a binding; the others always derive.
                if var_name in resolved:
                    continue
                derived_val = world.object_destination.get(source_val)
            else:
                raise ValueError(
                    f"AdaptivePlanner: unknown lookup function '{lookup_fn}' "
                    f"for derived var '{var_name}'"
                )
            if derived_val is None and lookup_fn == DESTINATION_LOOKUP:
                # A destination is a static fact of the station, required at
                # load for every object of the source type: none here is a
                # modelling error, never a world fact to score around.
                raise ValueError(
                    f"AdaptivePlanner: no destination declared for '{source_val}' "
                    f"(derived var '{var_name}'). {where}"
                )
            if derived_val is None:
                raise DecompositionError(
                    f"AdaptivePlanner: lookup '{lookup_fn}({source_val})' "
                    f"returned None for derived var '{var_name}'"
                )
            resolved[var_name] = derived_val
        return resolved
    
    def _resolve_step_bindings(
        self,
        step: Step,
        bindings: Dict[str, str],
    ) -> Dict[str, str]:
        # Always carry ?agent forward — it's execution context, not a step parameter
        step_bindings: Dict[str, str] = {}
        if "?agent" in bindings:
            step_bindings["?agent"] = bindings["?agent"]        

        for param_var, term in step.bindings.items():   # param_var is Var, term is Var or Const
            key = param_var.name                         # e.g. "?item"
            if isinstance(term, Const):
                step_bindings[key] = term.value
            elif isinstance(term, Var):
                val = bindings.get(term.name)
                if val is None:
                    raise ValueError(
                        f"AdaptivePlanner: unbound variable '{term.name}' "
                        f"in a step of '{_step_schema_name(step)}'"
                    )
                step_bindings[key] = val
            else:
                raise TypeError(f"AdaptivePlanner: unexpected term type {type(term)}")
        return step_bindings


    def _ground_action(
        self,
        schema: ActionSchema,
        bindings: Dict[str, str],
    ) -> GroundedAction:
        """
        Produce a fully grounded GroundedAction from an ActionSchema and bindings.
        Resolves completion predicate to Const args only.
        """
        completion_predicate = None

        if isinstance(schema.completion, ConditionSchema):
            completion_predicate = self._ground_predicate(schema.completion, bindings)
        # ProcessCompletion: no predicate — executor uses duration/process check

        return GroundedAction(
            action_name=schema.name,
            bindings=bindings,
            completion_predicate=completion_predicate,
            schema=schema,
        )

    def _ground_predicate(
        self,
        condition: ConditionSchema,
        bindings: Dict[str, str],
    ) -> Predicate:
        """
        Ground a ConditionSchema into a Predicate with Const args only.
        """
        grounded_args = []
        for term in condition.args:
            if isinstance(term, Const):
                grounded_args.append(term)
            elif isinstance(term, Var):
                val = bindings.get(term.name)
                if val is None:
                    raise ValueError(
                        f"AdaptivePlanner: unbound variable '{term.name}' "
                        f"when grounding predicate '{condition.name}'"
                    )
                grounded_args.append(Const(val))
            else:
                raise TypeError(f"AdaptivePlanner: unexpected term type {type(term)}")

        return Predicate(condition.name, tuple(grounded_args))

def _step_schema_name(step: Step) -> str:
    """The name of the schema a step calls, for error text only."""
    return step.action.name if isinstance(step, ActionStep) else step.task.name
