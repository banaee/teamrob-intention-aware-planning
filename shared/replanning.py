"""
shared/replanning.py

PURPOSE:
    The robot's replanning trigger logic (see robot agent architecture, HCM paper).
    Decides WHETHER the robot should replan given a new belief about human intentions.
    Sits between recognizer.py and planner.py in the cognitive loop.

WHAT THIS MODULE DOES:
    - Compares new BeliefState against previous BeliefState
    - Checks if current plan is still feasible given updated belief and world state
    - Returns a decision dict: should we replan, why, and how strongly

WHAT THIS MODULE DOES NOT DO:
    - Does NOT produce a new plan (that is planner.py)
    - Does NOT update beliefs (that is recognizer.py)
    - Does NOT know about Mesa steps or ROS callbacks
    - Simulators decide WHEN to call this — core decides WHAT counts as a trigger

INPUTS:
    - current_plan    AbstractPlan currently being executed (or None if no plan yet)
    - new_belief      latest BeliefState from recognizer.py
    - world           current WorldState from the simulator
    - prev_belief     previous BeliefState to compare against (or None)

OUTPUTS:
    - dict with keys:
        "replan"  : bool    — whether replanning is recommended
        "reason"  : str     — e.g. "belief_divergence", "precondition_broken", "no_plan"
        "score"   : float   — trigger strength 0.0..1.0 (0 = no trigger, 1 = strong trigger)

TRIGGER CONDITIONS (to be implemented):
    1. Belief divergence   — most_likely intention changed, or probability shift exceeds threshold
    2. Precondition broken — current plan's next action is no longer feasible in world state
    3. No plan             — robot has no current plan at all

ALGORITHM (skeleton):
    Currently returns replan=False always.
    TODO: Implement trigger conditions in Phase 4.
"""

from shared.types import AbstractPlan, BeliefState, WorldState


def should_replan(
    current_plan: AbstractPlan | None,
    new_belief: BeliefState,
    world: WorldState,
    prev_belief: BeliefState | None = None,
) -> dict:
    """
    Evaluate whether the robot should replan.

    SKELETON BEHAVIOUR:
        - If no plan exists yet → trigger replan (this is real, not dummy)
        - Otherwise → return False with placeholder trigger checks stubbed out

    TODO in Phase 4:
        - Trigger 1: belief divergence (KL-divergence or max-prob shift > threshold)
        - Trigger 2: precondition check (next action still feasible in world?)
        - Trigger 3: cost delta (is current plan now significantly more expensive?)
    """

    # Real check: if there is no plan at all, we must plan
    if current_plan is None:
        return {
            "replan": True,
            "reason": "no_plan",
            "score": 1.0,
        }

    # --- Placeholder trigger 1: belief divergence ---
    # TODO: compare prev_belief vs new_belief distribution
    # e.g. if most_likely changed or KL-divergence > threshold → replan
    belief_divergence_detected = False  # placeholder

    # --- Placeholder trigger 2: precondition broken ---
    # TODO: check if current_plan.actions[0] preconditions hold in world
    precondition_broken = False  # placeholder

    replan = belief_divergence_detected or precondition_broken

    reason = "none"
    score = 0.0

    if belief_divergence_detected:
        reason = "belief_divergence"
        score = 0.8  # placeholder strength
    elif precondition_broken:
        reason = "precondition_broken"
        score = 1.0  # hard trigger

    return {
        "replan": replan,
        "reason": reason,
        "score": score,
    }