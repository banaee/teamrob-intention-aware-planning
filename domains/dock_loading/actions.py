# domains/dock_loading/actions.py
"""
Action schema definitions for the dock_loading domain.
These are the HTN primitive actions — directly executable, not decomposed further.
Microaction expansion (STEP*, GRASP, TOUCH, etc.) is handled by mesa_sim/action_decomposer.py.
The forms are kitting's (domains/kitting/actions.py); scan_it is this domain's own.

PREDICATE NAMING NOTE:
    Completion predicates use "at(agent, object)" — object-level proximity.
    This matches world_state_builder.py which emits Predicate("at", ...) only
    when agent is within PROXIMITY_THRESHOLD of a named env object or item.
    Area-level spatial context uses "in_area(agent, area)" — a separate predicate.
    Do NOT use "at" for area-level completion.

ACTIONS:
    move_to       — navigate to a target object or location
    pick_up       — grasp a pallet (agent must be at pallet)
    place         — release a pallet at a target location (agent must be holding it)
    wait_at       — stand at an entity for a stated duration; completes on waited(agent, entity)
    stand         — stand still for a stated duration, at no entity; process completion only
    scan_it       — touch the pallet's screen at close range (agent must be at pallet);
                    sets the declared state is_scanned (T-G A5)
"""

from shared.types import Var, ConditionSchema, ProcessCompletion, ActionSchema

_agent  = Var("?agent")
_item = Var("?item")      # the portable object an action handles: here a pallet
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
    progress_evaluator="excess_path",   # excess-path (wasted distance) likelihood, I4
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
    moved_object_key="?item",
    moved_to_key="?agent",      # a held pallet is wherever its holder is
)

place = ActionSchema(
    name="place",
    parameters=[_item, _target],
    preconditions=[
        ConditionSchema("holding", (_agent, _item)),
    ],
    effects=[
        ConditionSchema("obj_at", (_item, _target)),
    ],
    # holding is RETRACTED, as in kitting (TODO-07): no not_holding fact.
    retracts=[
        ConditionSchema("holding", (_agent, _item)),
    ],
    completion=ConditionSchema("obj_at", (_item, _target)),
    microactions=["RELEASE"],
    moved_object_key="?item",
    moved_to_key="?target",
)

scan_it = ActionSchema(
    name="scan_it",
    parameters=[_item],
    preconditions=[
        ConditionSchema("at", (_agent, _item)),
    ],
    effects=[
        ConditionSchema("is_scanned", (_item,)),
    ],
    completion=ConditionSchema("is_scanned", (_item,)),
    microactions=["TOUCH"],
)

# wait_at's completion is the world fact the body emits when its timer runs
# out, waited(agent, entity), as in kitting; the body determines the entity by
# proximity.
wait_at = ActionSchema(
    name="wait_at",
    parameters=[_entity],
    preconditions=[
        ConditionSchema("at", (_agent, _entity)),
    ],
    effects=[
        ConditionSchema("waited", (_agent, _entity)),
    ],
    completion=ConditionSchema("waited", (_agent, _entity)),
    microactions="STAND*",
    duration_key="?duration",   # the body reads the stated duration through it (T-H1)
)

# stand (T-H): standing still for a stated time, with no entity. Process
# completion only: it emits no world fact. Used by the HumanOnlyTasks stand
# and go_to_and_stand.
stand = ActionSchema(
    name="stand",
    parameters=[],
    preconditions=[],
    effects=[],
    completion=ProcessCompletion(),
    microactions="STAND*",
    duration_key="?duration",
)
