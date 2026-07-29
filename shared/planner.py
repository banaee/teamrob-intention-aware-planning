"""
shared/planner.py

PURPOSE:
    The robot's "Adaptive planning" module.
    Produces a sequence of GroundedActions for the robot to execute,
    adapted to the current belief about what the human intends to do.

WHAT THIS MODULE DOES:
    - Fetches TaskSchema from DomainKnowledgeBase
    - Selects applicable method (first method whose guards hold in WorldState)
    - Grounds each StepCall: resolves Var bindings to Const values
    - Recursively decomposes StepCalls that name a TaskSchema (not a primitive ActionSchema)
    - Returns a flat AbstractPlan (single task, executor-facing)

WHAT THIS MODULE DOES NOT DO:
    - Does NOT parse strings — all structure comes from typed schema objects
    - Does NOT hardcode variable names — derivations declared in MethodSchema
    - Does NOT decide whether to replan (that is replanning.py / meta_planner.py)
    - Does NOT execute actions (that is mesa_sim/executor.py)
    - Does NOT update beliefs (that is recognizer.py)
    - Does NOT schedule across tasks (that is meta_planner.py)

GROUNDING:
    Task parameters arrive as Dict[str, str] e.g. {"?item": "item_3"}.
    agent_id is passed explicitly as execution context — injected as ?agent.
    The planner resolves each StepCall's bindings:
        Var("?item")           → looked up in task_params / accumulated bindings
        Const("kitting_table") → used as-is
    All GroundedActions carry a fully instantiated completion_predicate
    (Predicate with Const args only) — executor checks set membership directly.

RECURSION:
    If a StepCall names a TaskSchema (not a primitive ActionSchema), the planner
    recurses into that sub-task with the current bindings. The result is flattened
    into the same action list. Output is always a flat AbstractPlan.
"""

from typing import Dict, List, Optional, Tuple
import logging

from shared.types import (
    ProcessCompletion, Var, Const, Predicate, ConditionSchema,
    GroundedAction, AbstractPlan, BeliefState, WorldState,
    TaskSchema, ActionSchema, MethodSchema, StepCall,
)
from shared.domain_knowledge import DomainKnowledgeBase

logger = logging.getLogger(__name__)


class AdaptivePlanner:

    def __init__(self, knowledge: DomainKnowledgeBase):
        self.knowledge = knowledge

    def plan(
        self,
        my_intention: str,
        task_params: Dict[str, str],    # {"?item": "item_3"} — task-level bindings only
        agent_id: str,                  # executing agent — injected as ?agent, not in task_params
        belief: BeliefState,
        world: WorldState,
        current_plan: AbstractPlan | None = None,
    ) -> AbstractPlan:
        """
        Produce a flat AbstractPlan for a single task.
        Recursively decomposes sub-tasks until all steps are primitive ActionSchemas.
        Guard evaluation selects the applicable method per task/sub-task.
        """
        # Build initial bindings: task params + agent injection
        bindings: Dict[str, str] = {"?agent": agent_id}
        bindings.update(task_params)

        actions = self._decompose_task(my_intention, bindings, world)

        return AbstractPlan(
            goal_intention=my_intention,
            actions=actions,
        )

    # ------------------------------------------------------------------
    # Internal decomposition
    # ------------------------------------------------------------------

    def _decompose_task(
        self,
        task_name: str,
        bindings: Dict[str, str],
        world: WorldState,
    ) -> List[GroundedAction]:
        """
        Recursively decompose a task into a flat list of GroundedActions.
        Raises if no applicable method is found.
        """
        task_schema = self.knowledge.get_task_schema(task_name)
        if task_schema is None:
            raise ValueError(f"AdaptivePlanner: unknown task '{task_name}'")

        method, bindings = self._select_method(task_schema, bindings, world)  # returns method + updated bindings

        # Resolve derived vars declared on this method before processing steps
        resolved_bindings = self._resolve_derived_vars(method, bindings, world)

        actions: List[GroundedAction] = []
        for step in method.step_calls:
            step_bindings = self._resolve_step_bindings(step, resolved_bindings)
            step_name = step.action_name

            if self.knowledge.get_task_schema(step_name) is not None:
                # StepCall names a TaskSchema — recurse
                sub_actions = self._decompose_task(step_name, step_bindings, world)
                actions.extend(sub_actions)

            elif self.knowledge.get_action_schema(step_name) is not None:
                # StepCall names a primitive ActionSchema — ground and append
                action_schema = self.knowledge.get_action_schema(step_name)
                grounded = self._ground_action(action_schema, step_bindings)
                actions.append(grounded)

            else:
                raise ValueError(
                    f"AdaptivePlanner: step '{step_name}' in method "
                    f"'{method.name}' of task '{task_schema.name}' "
                    f"is neither a known task nor a known action"
                )

        return actions

    def _select_method(
        self,
        task_schema: TaskSchema,
        bindings: Dict[str, str],
        world: WorldState,
        ) -> Tuple[MethodSchema, Dict[str, str]]:
        """
        Return the first method whose guards are all satisfied in world, along
        with bindings updated to include any vars discovered by existential
        guard matching.
        Empty guard list = unconditional (always passes).
        Raises ValueError if no method is applicable.
        """
        for method in task_schema.methods:
            resolved = self._guards_satisfied(method, bindings, world)
            if resolved is not None:
                return method, resolved

        raise ValueError(
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
        resolved = dict(bindings)
        for var_name, (lookup_fn, source_var) in method.derived_vars.items():
            source_val = resolved.get(source_var)
            if source_val is None:
                raise ValueError(
                    f"AdaptivePlanner: derived var '{var_name}' depends on "
                    f"'{source_var}' which is not bound. Method: '{method.name}'"
                )
            if lookup_fn == "zone_of":
                derived_val = world.object_zones.get(source_val)
            elif lookup_fn == "home_container_of":
                derived_val = world.object_home_container.get(source_val)
            else:
                raise ValueError(
                    f"AdaptivePlanner: unknown lookup function '{lookup_fn}' "
                    f"for derived var '{var_name}'"
                )
            if derived_val is None:
                raise ValueError(
                    f"AdaptivePlanner: lookup '{lookup_fn}({source_val})' "
                    f"returned None for derived var '{var_name}'"
                )
            resolved[var_name] = derived_val
        return resolved
    
    def _resolve_step_bindings(
        self,
        step: StepCall,
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
                        f"in step '{step.action_name}'"
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