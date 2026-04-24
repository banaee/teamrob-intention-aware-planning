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
    - Returns an AbstractPlan with fully grounded GroundedActions

WHAT THIS MODULE DOES NOT DO:
    - Does NOT parse strings — all structure comes from typed schema objects
    - Does NOT hardcode variable names — derivations declared in MethodSchema
    - Does NOT decide whether to replan (that is replanning.py)
    - Does NOT execute actions (that is mesa_sim/executor.py)
    - Does NOT update beliefs (that is recognizer.py)

GROUNDING:
    Task parameters arrive as Dict[str, str] e.g. {"?item": "item_3"}.
    agent_id is passed explicitly as execution context — not a task parameter.
    The planner resolves each StepCall's bindings:
        Var("?item")       → looked up in task_params
        Const("kitting_table") → used as-is
    All GroundedActions carry a fully instantiated completion_predicate
    (Predicate with Const args only) — executor checks set membership directly.

    TODO Phase 4: method guard evaluation, conflict checking, cost-based selection.
"""

from typing import Dict, List, Optional
import logging

from shared.types import (
    ProcessCompletion, Var, Const, Predicate, ConditionSchema,
    GroundedAction, AbstractPlan, BeliefState, WorldState,
    TaskSchema, MethodSchema, StepCall,
)
from shared.domain_knowledge import DomainKnowledgeBase


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
        Produce an AbstractPlan for the robot to execute.

        SKELETON BEHAVIOUR:
            Selects first method unconditionally (guards not evaluated yet).
            Grounds all StepCalls against task_params, agent_id, and WorldState.
            No conflict checking, no cost-based selection.
        TODO Phase 4: guard evaluation, belief-driven adaptation, conflict checking.
        """
        task_schema = self.knowledge.get_task_schema(my_intention)
        if task_schema is None:
            return AbstractPlan(goal_intention=my_intention, actions=[])

        method = self._select_method(task_schema, world)
        if method is None:
            return AbstractPlan(goal_intention=my_intention, actions=[])

        grounded = self._ground_method(method, task_params, agent_id, world)

        # TODO Phase 4: inspect belief, check conflicts, reorder/reroute

        return AbstractPlan(
            goal_intention=my_intention,
            actions=grounded,
        )

    # =========================================================================
    # Method selection
    # =========================================================================

    def _select_method(
        self,
        task_schema: TaskSchema,
        world: WorldState,
    ) -> Optional[MethodSchema]:
        """
        Select first applicable method.
        Currently returns the first method unconditionally.
        TODO Phase 4: evaluate guards against WorldState.predicates.
        """
        if task_schema.methods:
            return task_schema.methods[0]
        return None

    # =========================================================================
    # Grounding
    # =========================================================================

    def _ground_method(
        self,
        method: MethodSchema,
        task_params: Dict[str, str],
        agent_id: str,
        world: WorldState,
    ) -> List[GroundedAction]:
        """
        Ground each StepCall in the method into a GroundedAction.
        Resolves all Vars to Consts using task_params, agent_id, and WorldState.
        """
        grounded = []
        for step in method.steps:
            operator = self.knowledge.get_action_operator(step.action_name)
            
            if operator is None:
                logging.warning(f"[planner] SKIPPING step '{step.action_name}' — operator not found in domain")
                continue            
            
            bindings = self._resolve_bindings(step, method, task_params, agent_id, world)

            # Ground the completion predicate, unless it's a ProcessCompletion which is monitored differently by the executor. 
            if isinstance(operator.completion, ProcessCompletion):
                completion_predicate = None
            else:
                completion_predicate = self._ground_condition(operator.completion, bindings)

            grounded.append(GroundedAction(
                action_name=step.action_name,
                bindings=bindings,
                completion_predicate=completion_predicate,
                operator=operator,
            ))            
        
        
        
        
        
        return grounded

    def _resolve_bindings(
        self,
        step: StepCall,
        method: MethodSchema,
        task_params: Dict[str, str],
        agent_id: str,
        world: WorldState,
    ) -> Dict[str, str]:
        """
        Resolve a StepCall's bindings to concrete string values.

        Resolution rules (in order):
            ?agent                → agent_id (always injected from execution context)
            Const("x")            → "x" (used as-is)
            Var("?x") in task_params → task_params["?x"]
            Var("?x") not in task_params → derived via method.derived_vars registry

        Returns {var_name: concrete_value} e.g. {"?zone": "zone_SE"}.
        """
        resolved: Dict[str, str] = {"?agent": agent_id}

        for param_var, binding_term in step.bindings.items():
            key = param_var.name
            if isinstance(binding_term, Const):
                resolved[key] = binding_term.value
            elif isinstance(binding_term, Var):
                var_name = binding_term.name
                if var_name in task_params:
                    resolved[key] = task_params[var_name]
                else:
                    derived = self._resolve_derived(var_name, method, task_params, world)
                    if derived is not None:
                        resolved[key] = derived
                    # else: absent — _ground_condition will raise on use
        return resolved

    def _resolve_derived(
        self,
        var_name: str,
        method: MethodSchema,
        task_params: Dict[str, str],
        world: WorldState,
    ) -> Optional[str]:
        """
        Resolve a derived variable using the method's declared derived_vars.
        Dispatches through _lookup — no hardcoded variable names here.

        method.derived_vars declares: {var_name: (lookup_fn, source_var)}
        """
        if var_name not in method.derived_vars:
            return None
        lookup_fn, source_var = method.derived_vars[var_name]
        source_value = task_params.get(source_var)
        if source_value is None:
            return None
        return self._lookup(lookup_fn, source_value, world)

    def _lookup(self, fn: str, obj_id: str, world: WorldState) -> Optional[str]:
        """
        Lookup registry: maps function names to WorldState queries.
        Currently unused in kitting — zone reasoning moved to recognizer context.
        Keep registry for future domains that need derived variable resolution.
        TODO Phase 4: add lookup functions for new domains that need derived variables.
        Currently unused in kitting — zone reasoning moved to recognizer context.
        """
        return None


    # =========================================================================
    # Condition grounding
    # =========================================================================

    def _ground_condition(
        self,
        condition: ConditionSchema,
        bindings: Dict[str, str],
    ) -> Predicate:
        """
        Ground a ConditionSchema into a fully instantiated Predicate.
        All Var args substituted from bindings. Const args passed through.
        Raises ValueError on unresolved variables — fails loudly, not silently.
        """
        resolved_args = []
        for arg in condition.args:
            if isinstance(arg, Var):
                value = bindings.get(arg.name)
                if value is None:
                    raise ValueError(
                        f"Unresolved variable '{arg.name}' in condition "
                        f"'{condition.name}' — check method derived_vars and task_params"
                    )
                resolved_args.append(Const(value))
            else:
                resolved_args.append(arg)  # already a Const
        return Predicate(condition.name, tuple(resolved_args))