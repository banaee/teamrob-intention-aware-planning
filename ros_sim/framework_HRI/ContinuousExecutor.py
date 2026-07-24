
from __future__ import annotations

import time
import logging
from typing import Optional, Tuple, Dict

from shared.types import AbstractPlan, GroundedAction, WorldState, Predicate, ProcessCompletion

logger = logging.getLogger(__name__)


class ActionExecutor:
    """
    Executes an AbstractPlan produced by AdaptivePlanner against the
    continuous world, using PRIEST for navigation.

    Parameters
    ----------
    layout      : dict — the loaded env_layout dict from load_layout()
                  Used to resolve symbolic targets to (x, y) coordinates.
    pick_delay  : float — seconds to wait during pick_up (simulated grasping)
    place_delay : float — seconds to wait during place (simulated release)
    """

    def __init__(
        self,
        layout:      dict,
        pick_delay:  float = 2.0,
        place_delay: float = 2.0,
    ):
        self.layout      = layout
        self.pick_delay  = pick_delay
        self.place_delay = place_delay

        # Build position lookup: object_id → (x, y)
        # Covers: items (shelf positions), shelves, kitting_table, coffee_machine
        self._position_map: Dict[str, Tuple[float, float]] = self._build_position_map()

        # Current plan state
        self._plan:         Optional[AbstractPlan] = None
        self._action_index: int                    = 0
        self._wait_start:   Optional[float]        = None
        self.status:        str                    = "IDLE"

        # Current navigation goal — read by planner_2._main_loop to feed PRIEST
        self.current_nav_goal: Optional[Dict[str, float]] = None

    # =========================================================================
    # Public API
    # =========================================================================

    def load_plan(self, plan: AbstractPlan) -> None:
        """
        Load a new AbstractPlan and reset execution state.
        Called by planner_2 at the start of each task instance.
        """
        self._plan         = plan
        self._action_index = 0
        self._wait_start   = None
        self.status        = "NAVIGATING" if plan.actions else "TASK_DONE"
        self.current_nav_goal = None

        if plan.actions:
            self._start_action(plan.actions[0])
            logger.info(
                f"[executor] Loaded plan '{plan.goal_intention}' "
                f"with {len(plan.actions)} actions"
            )
        else:
            logger.warning("[executor] Empty plan loaded — TASK_DONE immediately")

    def step(
        self,
        world_state:   WorldState,
        priest_status: str,
    ) -> str:
        """
        Advance execution by one cognitive tick.

        Parameters
        ----------
        world_state   : current WorldState from world_state_builder_continuous
        priest_status : current PRIESTLocalPlanner.status
                        ("RUNNING", "REACHED", "INTERRUPTED", "IDLE")

        Returns
        -------
        status string — one of:
            "NAVIGATING", "WAITING", "ACTION_DONE", "TASK_DONE",
            "NEEDS_REPLAN", "IDLE"
        """
        if self._plan is None or self.status in ("TASK_DONE", "NEEDS_REPLAN", "IDLE"):
            return self.status

        if self._action_index >= len(self._plan.actions):
            self.status = "TASK_DONE"
            logger.info("[executor] All actions completed — TASK_DONE")
            return self.status

        current_action = self._plan.actions[self._action_index]

        # Dispatch by action type
        if current_action.action_name == "move_to":
            return self._step_move_to(current_action, world_state, priest_status)

        elif current_action.action_name == "pick_up":
            return self._step_wait(current_action, world_state, self.pick_delay, "pick_up")

        elif current_action.action_name == "place":
            return self._step_wait(current_action, world_state, self.place_delay, "place")

        elif current_action.action_name == "wait_at":
            # ProcessCompletion — wait until externally signalled (for now, 5 s)
            return self._step_wait(current_action, world_state, 5.0, "wait_at")

        else:
            logger.warning(f"[executor] Unknown action '{current_action.action_name}' — skipping")
            self._advance()
            return self.status

    def current_task_label(self) -> str:
        if self._plan is None:
            return "No plan loaded"
        if self._action_index >= len(self._plan.actions):
            return f"Current Task: {self._plan.goal_intention}\nCurrent Action: completed"
        action = self._plan.actions[self._action_index]
        # Clean up bindings — remove ? prefix and skip ?agent
        bindings_str = ", ".join(
            f"{k.lstrip('?')}={v}"
            for k, v in action.bindings.items()
            if k != "?agent"
        )
        return (
            f"Current Task: {self._plan.goal_intention}({bindings_str})\n"
            f"Current Action: {action.action_name} → {bindings_str}   "
            f"[{self._action_index + 1}/{len(self._plan.actions)}]"
        )
    # =========================================================================
    # Private — action steppers
    # =========================================================================

    def _step_move_to(
        self,
        action:        GroundedAction,
        world_state:   WorldState,
        priest_status: str,
    ) -> str:
        """
        Execute a move_to action.
        Navigation goal is set in self.current_nav_goal — planner_2 feeds it to PRIEST.
        Completion: at(robot_0, target) in world_state.predicates
                    OR PRIEST reports REACHED (belt-and-suspenders).
        """
        # Check completion predicate first
        if self._completion_satisfied(action, world_state):
            logger.info(
                f"[executor] move_to completed via predicate: "
                f"{action.completion_predicate}"
            )
            self._advance()
            return self.status

        # PRIEST reached the goal
        if priest_status == "REACHED":
            logger.info("[executor] move_to completed via PRIEST REACHED")
            self._advance()
            return self.status

        # PRIEST was interrupted
        if priest_status == "INTERRUPTED":
            logger.warning("[executor] PRIEST INTERRUPTED during move_to → NEEDS_REPLAN")
            self.status = "NEEDS_REPLAN"
            return self.status

        # Still navigating — ensure goal is set
        self.status = "NAVIGATING"
        return self.status

    def _step_wait(
        self,
        action:      GroundedAction,
        world_state: WorldState,
        delay:       float,
        label:       str,
    ) -> str:
        """
        Execute a timed wait action (pick_up, place, wait_at).
        Starts a timer on first call, completes after delay seconds.
        Also checks completion predicate in case world_state already satisfies it.
        """
        # Check completion predicate (if not ProcessCompletion)
        if self._completion_satisfied(action, world_state):
            logger.info(f"[executor] {label} completed via predicate")
            self._advance()
            return self.status

        # Start timer on first entry
        if self._wait_start is None:
            self._wait_start = time.time()
            logger.info(f"[executor] {label} wait started ({delay:.1f} s)")
            self.status = "WAITING"
            return self.status

        # Check if delay has elapsed
        elapsed = time.time() - self._wait_start
        if elapsed >= delay:
            logger.info(f"[executor] {label} wait finished after {elapsed:.1f} s")
            self._wait_start = None
            self._advance()
            return self.status

        self.status = "WAITING"
        return self.status

    # =========================================================================
    # Private — helpers
    # =========================================================================

    def _start_action(self, action: GroundedAction) -> None:
        """
        Called when advancing to a new action.
        Sets up navigation goal if action is move_to.
        """
        self._wait_start = None

        if action.action_name == "move_to":
            target_id = action.bindings.get("?target")
            if target_id is None:
                logger.error("[executor] move_to has no ?target binding")
                self.status = "NEEDS_REPLAN"
                return

            pos = self._resolve_position(target_id)
            if pos is None:
                logger.error(f"[executor] Cannot resolve position for '{target_id}'")
                self.status = "NEEDS_REPLAN"
                return

            self.current_nav_goal = {"x": pos[0], "y": pos[1]}
            self.status = "NAVIGATING"
            logger.info(
                f"[executor] move_to '{target_id}' → "
                f"({pos[0]:.2f}, {pos[1]:.2f})"
            )
        else:
            # Non-navigation action — clear nav goal
            self.current_nav_goal = None
            self.status = "WAITING"
            logger.info(f"[executor] Starting {action.action_name}")

    def _advance(self) -> None:
        """Move to the next action in the plan."""
        self._action_index += 1
        self._wait_start    = None

        if self._action_index >= len(self._plan.actions):
            self.status            = "TASK_DONE"
            self.current_nav_goal  = None
        else:
            next_action = self._plan.actions[self._action_index]
            self._start_action(next_action)

    def _completion_satisfied(
        self,
        action:      GroundedAction,
        world_state: WorldState,
    ) -> bool:
        """
        Check if action.completion_predicate is in world_state.predicates.
        Returns False if completion is ProcessCompletion (timed, not predicate-based).
        """
        if action.completion_predicate is None:
            # ProcessCompletion — handled by timer, not predicates
            return False
        return action.completion_predicate in world_state.predicates

    def _resolve_position(self, target_id: str) -> Optional[Tuple[float, float]]:
        """
        Resolve a symbolic target ID to (x, y) in metres.
        Searches: items, shelves, kitting_table, coffee_machine.
        """
        return self._position_map.get(target_id)

    def _build_position_map(self) -> Dict[str, Tuple[float, float]]:
        """
        Build {object_id: (x, y)} from the loaded layout.
        Called once at construction.
        """
        pos_map: Dict[str, Tuple[float, float]] = {}

        # Items — positioned at their shelf
        for item in self.layout.get("items", []):
            pos_map[item["id"]] = (item["x"], item["y"])

        # Shelves
        for shelf in self.layout.get("shelves", []):
            pos_map[shelf["id"]] = (shelf["x"], shelf["y"])

        # Kitting table
        kt = self.layout.get("kitting_table")
        if kt:
            pos_map["kitting_table"] = (kt["x"], kt["y"])

        # Coffee machine
        cm = self.layout.get("coffee_machine")
        if cm:
            pos_map["coffee_machine_0"] = (cm["x"], cm["y"])

        return pos_map

    @staticmethod
    def _format_bindings(bindings: Dict[str, str]) -> str:
        return ", ".join(
            f"{k}={v}" for k, v in bindings.items() if k != "?agent"
        )