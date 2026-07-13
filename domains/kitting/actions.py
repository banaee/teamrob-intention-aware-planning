# domains/kitting/actions.py
"""
Action schema definitions for the kitting domain.
These are the HTN primitive actions — directly executable, not decomposed further.
Microaction expansion (STEP*, GRASP, etc.) is handled by mesa_sim/action_decomposer.py.

PREDICATE NAMING NOTE:
    Completion predicates here use "at(agent, object)" — object-level proximity.
    This matches world_state_builder.py which emits Predicate("at", ...) only
    when agent is within PROXIMITY_THRESHOLD of a named env object or item.
    Zone-level spatial context uses "in_zone(agent, zone)" — a separate predicate.
    Do NOT use "at" for zone-level completion — that mismatch was the root cause
    of the stuck-agent bug where move_to never completed.

"""

from shared.types import Var, Const, ConditionSchema, ProcessCompletion, ActionSchema

_agent  = Var("?agent")
_item   = Var("?item")
_target = Var("?target")
_entity = Var("?entity")


# GOTO_ZONE removed entirely:
# - Not a primitive action (HTN) — it decomposed further
# - Not an intermediate task — zone is not a meaningful semantic unit
# - Zone reasoning moved to recognizer context weighting (ωcontext)

# goto_zone = ActionSchema(
#     name="goto_zone",
#     parameters=[_zone],
#     preconditions=[
#         ConditionSchema("zone_exists", (_zone,)),  
#     ],
#     effects=[
#         ConditionSchema("at", (_agent, _zone)),
#     ],
#     completion=ConditionSchema("at", (_agent, _zone)),
#     microactions="STEP*",
#     movement_target_key="?zone",
#     movement_target_type="zone", 
# )

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