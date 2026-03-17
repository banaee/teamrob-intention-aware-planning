"""
shared/planner.py

PURPOSE:
    The robot's "Adaptive planning" module (see robot agent architecture, HCM paper).
    Produces a sequence of abstract actions for the robot to execute,
    adapted to the current belief about what the human intends to do.
    Answers: "Given what the human is likely doing, what should I do next?"

WHAT THIS MODULE DOES:
    - Takes the robot's assigned intention (e.g. DELIVER_ITEM)
    - Looks up the action sequence from KnowledgeBase
    - Adapts the plan based on the current BeliefState over human intentions
    - Returns an AbstractPlan (sequence of AbstractActions)

WHAT THIS MODULE DOES NOT DO:
    - Does NOT decide whether to replan (that is replanning.py)
    - Does NOT execute actions (that is mesa_sim/executor.py)
    - Does NOT translate to Mesa steps or microactions (that is mesa_sim/microactions.py)
    - Does NOT update beliefs (that is recognizer.py)
    - Does NOT resolve runtime placeholders like {item_zone} fully yet (Phase 4)

INPUTS:
    - my_intention    str — robot's currently assigned task name e.g. "DELIVER_ITEM"
    - belief          BeliefState — current belief over human intentions from recognizer.py
    - world           WorldState — current symbolic world snapshot from simulator
    - current_plan    AbstractPlan | None — existing plan (for plan repair, Phase 4)

OUTPUTS:
    - AbstractPlan    consumed by mesa_sim/executor.py (via mesa_sim/microactions.py)

ADAPTATION LOGIC (to be implemented):
    1. Decompose robot's task into candidate action sequence
    2. Predict human's likely next actions from belief
    3. Check for spatial-temporal conflicts between robot and human paths
    4. Select lowest-cost feasible plan (reorder, wait, or reroute if needed)
    5. Attach execution hints for simulator

ALGORITHM (skeleton):
    Currently returns a flat AbstractPlan from raw task decomposition.
    No parameter resolution. No conflict checking. No adaptation.
    TODO: Implement full cost-based adaptive planning in Phase 4.
"""

from shared.types import AbstractAction, AbstractPlan, ActionType, BeliefState, WorldState, ActionType
from shared.knowledge import KnowledgeBase


class AdaptivePlanner:

    def __init__(self, knowledge: KnowledgeBase):
        """
        knowledge: provides task decompositions and action schemas.
        """
        self.knowledge = knowledge

    def plan(
        self,
        my_intention: str,
        belief: BeliefState,
        world: WorldState,
        current_plan: AbstractPlan | None = None,
    ) -> AbstractPlan:
        """
        Produce an AbstractPlan for the robot to execute.

        INPUT:
            my_intention  - robot's assigned task name e.g. "DELIVER_ITEM"
            belief        - current belief over human intentions
            world         - symbolic world state
            current_plan  - existing plan if any (for repair, not used yet)

        OUTPUT:
            AbstractPlan with a sequence of AbstractActions

        SKELETON BEHAVIOUR:
            - Looks up action sequence for my_intention from KnowledgeBase
            - Wraps each action string in a minimal AbstractAction
            - No placeholder resolution, no conflict checking, no adaptation
            TODO: Full implementation in Phase 4.
        """

        raw_actions = self.knowledge.get_task_actions(my_intention)

        actions = []
        for action_str in raw_actions:
            # parse action name from raw string e.g. "GOTO_ZONE({item_zone})" → "GOTO_ZONE"
            action_name = action_str.split("(")[0].strip()
            actions.append(
                AbstractAction(
                    action_type=ActionType.NAVIGATE,  # TODO Phase 4: map action_name to correct ActionType
                    action_name=action_name,
                    parameters={"raw": action_str, "action_name": action_name},
                )
            )

        # --- Placeholder: adaptation logic ---
        # TODO: inspect belief.most_likely and world state
        # TODO: check for conflicts with predicted human path
        # TODO: reorder or reroute actions if needed
        # TODO: attach execution hints (estimated_path, estimated_duration)

        return AbstractPlan(
            goal_intention=my_intention,
            actions=actions,
        )