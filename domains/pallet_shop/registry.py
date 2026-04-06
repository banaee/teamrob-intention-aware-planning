# domains/pallet_shop/domain.py
"""
Assembles the pallet_shop DomainModel from tasks and actions.
Entry point: build_pallet_shop_domain()
Called once at startup by KnowledgeBase via sim_model.py.
"""

# TODO: Check Kitting registry for reference on how to structure this DomainModel, then implement actual registry for pallet_shop domain.

from shared.types import DomainModel
# from domains.pallet_shop.actions import ... #TODO: import ActionOperators here when we have them defined 
# from domains.pallet_shop.tasks import ...  #TODO: import TaskSchemas here when we have them defined


def register_pallet_shop_domain() -> DomainModel:
    return DomainModel(
        tasks={
            # TODO: add TaskSchemas here when we have them defined
        },
        actions={
            # TODO: add ActionOperators here when we have them defined
        },
        microactions=["STEP", "GRASP", "RELEASE", "STAND"],
    )