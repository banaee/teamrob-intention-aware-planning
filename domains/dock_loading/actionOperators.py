# domains/dock_loading/actionOperators.py
"""
Action operator definitions for the dock_loading domain.
These are the HTN primitive actions — directly executable, not decomposed further.
Microaction expansion (STEP*, GRASP, TOUCH, etc.) is handled by mesa_sim/action_decomposer.py.

PREDICATE NAMING NOTE:
    Completion predicates use "at(agent, object)" — object-level proximity.
    This matches world_state_builder.py which emits Predicate("at", ...) only
    when agent is within PROXIMITY_THRESHOLD of a named env object or item.
    Zone-level spatial context uses "in_zone(agent, zone)" — a separate predicate.
    Do NOT use "at" for zone-level completion.

ACTIONS:
    move_to       — navigate to a target object or location
    pick_up       — grasp a pallet (agent must be at pallet)
    place         — release a pallet at a target location (agent must be holding it)
    wait_at       — stand at an entity for a process-defined duration
    scan_pallet   — scan a pallet at close range (agent must be at pallet)
"""

from shared.types import Var, Const, ConditionSchema, ProcessCompletion, ActionOperator

_agent  = Var("?agent")
_pallet = Var("?pallet")
_target = Var("?target")
_entity = Var("?entity")


move_to = ActionOperator(
    name="move_to",
    parameters=[_target],
    preconditions=[],
    effects=[
        ConditionSchema("at", (_agent, _target)),
    ],
    completion=ConditionSchema("at", (_agent, _target)),
    microactions="STEP*",
    movement_target_key="?target",
    movement_target_type="object",
)

pick_up = ActionOperator(
    name="pick_up",
    parameters=[_pallet],
    preconditions=[
        ConditionSchema("at", (_agent, _pallet)),
    ],
    effects=[
        ConditionSchema("holding", (_agent, _pallet)),
    ],
    completion=ConditionSchema("holding", (_agent, _pallet)),
    microactions=["GRASP"],
)

place = ActionOperator(
    name="place",
    parameters=[_pallet, _target],
    preconditions=[
        ConditionSchema("holding", (_agent, _pallet)),
    ],
    effects=[
        ConditionSchema("obj_at", (_pallet, _target)),
        ConditionSchema("not_holding", (_agent, _pallet)),
    ],
    completion=ConditionSchema("obj_at", (_pallet, _target)),
    microactions=["RELEASE"],
)

wait_at = ActionOperator(
    name="wait_at",
    parameters=[_entity],
    preconditions=[
        ConditionSchema("at", (_agent, _entity)),
    ],
    effects=[],
    completion=ProcessCompletion(),
    microactions="STAND*",
)

scan_pallet = ActionOperator(
    name="scan_pallet",
    parameters=[_pallet],
    preconditions=[
        ConditionSchema("at", (_agent, _pallet)),
    ],
    effects=[
        ConditionSchema("scanned", (_pallet,)),
    ],
    completion=ConditionSchema("scanned", (_pallet,)),
    microactions=["TOUCH"],
)
