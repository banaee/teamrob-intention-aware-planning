# domains/dock_loading/actions.py
"""
Action schema definitions for the dock_loading domain.
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
    scan_it       — do touch screen at close range (agent must be at pallet)
"""

from shared.types import Var, Const, ConditionSchema, ProcessCompletion, ActionSchema

_agent  = Var("?agent")
_item = Var("?item")   # # was _pallet = Var("?pallet"), but now universal (item here means any portable object: TODO: in kitting the instances are also item_i)
_target = Var("?target")
_entity = Var("?entity")


move_to = ActionSchema(
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
    progress_evaluator="directional",   # cosine trajectory-consistency scoring
)

pick_up = ActionSchema(
    name="pick_up",
    parameters=[_item],
    preconditions=[
        ConditionSchema("at", (_agent, _item)),
    ],
    effects=[
        ConditionSchema("holding", (_agent, _item)),
    ],
    completion=ConditionSchema("holding", (_agent, _item)),
    microactions=["GRASP"],
)

place = ActionSchema(
    name="place",
    parameters=[_item, _target],
    preconditions=[
        ConditionSchema("holding", (_agent, _item)),
    ],
    effects=[
        ConditionSchema("obj_at", (_item, _target)),
        ConditionSchema("not_holding", (_agent, _item)),
    ],
    completion=ConditionSchema("obj_at", (_item, _target)),
    microactions=["RELEASE"],
)


scan_it = ActionSchema(
    name="scan_it",
    parameters=[_item],
    preconditions=[
        ConditionSchema("at", (_agent, _item)),
    ],
    effects=[
        ConditionSchema("scanned", (_item,)),
    ],
    completion=ConditionSchema("scanned", (_item,)),
    microactions=["TOUCH"],
)


wait_at = ActionSchema(
    name="wait_at",
    parameters=[_entity],
    preconditions=[
        ConditionSchema("at", (_agent, _entity)),
    ],
    effects=[],
    completion=ProcessCompletion(),
    microactions="STAND*",
)
