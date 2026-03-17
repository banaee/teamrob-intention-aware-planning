"""
mesa_sim/obs_builder.py

PURPOSE:
    Translates Mesa human agent state into a canonical Observation object
    for the cognitive layer (shared/recognizer.py).
    This is the "human action detection" boundary in the robot agent architecture.

WHAT THIS MODULE DOES:
    - Reads human agent's current physical state from Mesa (position, microaction, carrying)
    - Derives zone from position via model.get_zone_of_position()
    - Constructs and returns a canonical Observation object

WHAT THIS MODULE DOES NOT DO:
    - Does NOT access the human's script — only observable physical state
    - Does NOT perform any inference or classification
    - Does NOT know about IR, planning, or world state
    - Does NOT handle ROS — ROS has its own obs_builder_ros.py which must
      classify noisy sensor streams into discrete microaction labels

CALLED BY:
    - mesa_sim/agents.py (RobotAgent.step) — once per step, before recognizer.update()

INPUTS:
    - human_agent   HumanAgent — the observed human (read-only)
    - model         FactoryModel — for zone lookup
    - timestamp     float — current simulation step as float

OUTPUTS:
    - shared.types.Observation  consumed by shared/recognizer.py

MESA ADVANTAGE:
    Mesa has perfect ground truth — detected_microaction is read directly
    from human.current_microaction. Confidence is always 1.0.
    ROS must classify from noisy sensors; Mesa never needs to.

MICROACTION LABEL FORMAT:
    Labels are lowercase strings matching the microaction set M from
    actions_library.yaml: "step", "grasp", "release", "stand"
    When current_microaction is None (human idle or not yet started),
    label defaults to "stand".
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from shared.types import Observation, SpatialContext, ActionContext

if TYPE_CHECKING:
    from mesa_sim.model import FactoryModel
    from mesa_sim.agents import HumanAgent


def build_observation(
    human_agent: HumanAgent,
    model: FactoryModel,
    timestamp: float,
) -> Observation:
    """
    Build a canonical Observation from the human agent's current Mesa state.

    INPUT:
        human_agent  — the HumanAgent being observed (read-only)
        model        — FactoryModel for zone lookup (read-only)
        timestamp    — current step as float

    OUTPUT:
        Observation ready for shared/recognizer.py

    SKELETON BEHAVIOUR:
        Reads human.current_microaction directly (perfect Mesa ground truth).
        Returns "stand" when no microaction is active.
        TODO Phase 4: no changes needed here — Mesa obs_builder stays simple.
        The complexity of discretization lives in ros_sim/obs_builder_ros.py.
    """

    # ------------------------------------------------------------------
    # Position and zone
    # ------------------------------------------------------------------
    pos = human_agent.pos  # (x, y) center-origin
    zone = model.get_zone_of_position(pos[0], pos[1])

    spatial_context = SpatialContext(
        position=pos,
        orientation=0.0,  # Mesa agents have no orientation tracking yet
        zone=zone,
    )

    # ------------------------------------------------------------------
    # Detected microaction
    # Mesa ground truth: read directly from agent state
    # Normalize to lowercase to match actions_library.yaml conventions
    # ------------------------------------------------------------------
    raw_microaction = human_agent.current_microaction
    if raw_microaction is not None:
        detected_microaction = str(raw_microaction).lower()
    else:
        detected_microaction = "stand"  # default when idle

    # ------------------------------------------------------------------
    # Action context
    # target_object: what the human is interacting with, if anything
    # In Mesa: carrying tells us what item is held (post-GRASP)
    # target during movement comes from executor (TODO Phase 4)
    # ------------------------------------------------------------------
    action_context = ActionContext(
        target_object=human_agent.carrying,  # item_id or None
        progress=0.0,  # TODO Phase 4: derive from executor progress
    )

    return Observation(
        timestamp=timestamp,
        agent_id=human_agent.unique_id,
        detected_microaction=detected_microaction,
        spatial_context=spatial_context,
        action_context=action_context,
        confidence=1.0,  # Mesa always has perfect observation
    )
