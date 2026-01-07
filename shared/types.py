"""
shared/types.py

Canonical data types for communication between cognitive and embodiment layers.
These types define the contract between simulator-agnostic algorithms and 
simulator-specific implementations.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Set
from enum import Enum


# =============================================================================
# OBSERVATION TYPES
# =============================================================================

@dataclass
class SpatialContext:
    """Spatial information about an observed action."""
    position: Tuple[float, float]
    orientation: float
    zone: Optional[str] = None


@dataclass
class ActionContext:
    """Contextual information about an observed action."""
    target_object: Optional[str] = None
    progress: float = 0.0  # 0.0 to 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Observation:
    """
    Discrete observation of human behavior.
    This is what embodiment layers provide to the cognitive layer.
    """
    timestamp: float
    agent_id: str
    detected_microaction: str  # e.g., "move_to_shelf_3", "pick_item_7"
    spatial_context: SpatialContext
    action_context: ActionContext
    confidence: float = 1.0  # ROS might have < 1.0, Mesa always 1.0


# =============================================================================
# BELIEF STATE TYPES
# =============================================================================

@dataclass
class BeliefState:
    """
    Robot's belief distribution over human intentions.
    Output of intention recognition.
    """
    timestamp: float
    agent_id: str
    distribution: Dict[str, float]  # {intention_id: probability}
    most_likely: str  # intention_id with highest probability
    confidence: float  # overall confidence in belief
    predicted_next_actions: Dict[str, List[str]] = field(default_factory=dict)  # {intention_id: [action_types]}


# =============================================================================
# WORLD STATE TYPES
# =============================================================================

@dataclass
class AgentState:
    """Symbolic state of a single agent."""
    agent_id: str
    current_zone: str
    holding: Optional[str] = None  # item_id or None
    current_task: Optional[str] = None  # task_id or None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorldState:
    """
    Symbolic representation of the environment.
    Built by embodiment layers, consumed by cognitive layer.
    """
    timestamp: float
    agent_states: Dict[str, AgentState]  # {agent_id: AgentState}
    object_locations: Dict[str, str]  # {object_id: location_id}
    predicates: Set[str] = field(default_factory=set)  # e.g., "path_clear", "human_at_table"
    metadata: Dict[str, Any] = field(default_factory=dict)


# =============================================================================
# PLANNING TYPES
# =============================================================================

class ActionType(Enum):
    """High-level action types the robot can perform."""
    NAVIGATE = "navigate"
    PICK = "pick"
    PLACE = "place"
    WAIT = "wait"
    HANDOVER = "handover"


@dataclass
class AbstractAction:
    """
    High-level action with optional execution hints.
    The planner outputs these; embodiment layers interpret them.
    """
    action_type: ActionType
    parameters: Dict[str, Any]  # e.g., {"target": "shelf_3", "item": "item_7"}
    
    # Optional execution hints (Mesa may use directly, ROS may ignore)
    estimated_path: Optional[List[Tuple[float, float]]] = None
    estimated_duration: float = 0.0
    spatial_constraints: Dict[str, Any] = field(default_factory=dict)
    temporal_constraints: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AbstractPlan:
    """
    Complete plan for robot execution.
    Output of adaptive planning.
    """
    goal_intention: str  # What robot is trying to achieve
    actions: List[AbstractAction]
    estimated_total_cost: float = 0.0
    contingencies: Dict[str, Any] = field(default_factory=dict)  # Future: alternative plans
    metadata: Dict[str, Any] = field(default_factory=dict)


# =============================================================================
# TASK KNOWLEDGE TYPES (for configs and knowledge.py)
# =============================================================================

@dataclass
class TaskSchema:
    """
    Schema for a task type (e.g., DELIVER_ITEM, COFFEE_BREAK).
    Instantiated with specific parameters at runtime.
    """
    task_id: str  # e.g., "DELIVER_ITEM", "COFFEE_BREAK"
    parameters: List[str]  # e.g., ["item"], []
    decomposition: List[str]  # Action type IDs that comprise this task
    is_foreseeable: bool = False  # True for human behaviors like COFFEE_BREAK
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskInstance:
    """
    Concrete instantiation of a TaskSchema.
    E.g., DELIVER_ITEM(item_7) is an instance of DELIVER_ITEM schema.
    """
    schema_id: str  # Links to TaskSchema.task_id
    instance_id: str  # Unique identifier for this instance
    parameters: Dict[str, Any]  # e.g., {"item": "item_7"}
    metadata: Dict[str, Any] = field(default_factory=dict)