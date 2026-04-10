#!/usr/bin/env python3

# task_planner.py
import time

class TaskPlanner:
    """
    Two-stage task planner:
        1) Navigate to object
        2) Navigate to target
    """

    def __init__(self, tasks, pick_delay=2.0, place_delay=2.0):
        """
        tasks = [
            {
                "object": (x_obj, y_obj),
                "target": (x_tgt, y_tgt)
            },
            ...
        ]
        """
        self.tasks = tasks
        self.task_index = 0
        self.phase = "GOTO_OBJECT"   # or "GOTO_TARGET"

        self.pick_delay = pick_delay
        self.place_delay = place_delay

        self._wait_start_time = None

    def has_task(self):
        return self.task_index < len(self.tasks)

    def current_goal(self):

        # No more tasks → return None
        if self.task_index >= len(self.tasks):
            return None

        task = self.tasks[self.task_index]

        if self.phase == "GOTO_OBJECT":
            return {"x": task["object"][0], "y": task["object"][1]}

        elif self.phase == "GOTO_TARGET":
            return {"x": task["target"][0], "y": task["target"][1]}

        elif self.phase in ["PICK_WAIT", "PLACE_WAIT"]:
            # No navigation goal during wait phases
            return None

        else:
            raise RuntimeError(f"Unknown phase: {self.phase}")


    def update(self):
        """
        Called when navigation REACHED or inside WAIT phases.
        Handles transitions between phases.
        """

        # Phase: picking wait
        if self.phase == "PICK_WAIT":
            if self._wait_start_time is None:
                self._wait_start_time = time.time()

            if time.time() - self._wait_start_time >= self.pick_delay:
                print("Picking delay finished")
                self.phase = "GOTO_TARGET"
                self._wait_start_time = None

        # Phase: placing wait
        elif self.phase == "PLACE_WAIT":
            if self._wait_start_time is None:
                self._wait_start_time = time.time()

            if time.time() - self._wait_start_time >= self.place_delay:
                print("Placing delay finished")
                self.phase = "GOTO_OBJECT"
                self.task_index += 1
                self._wait_start_time = None

    def advance(self):
        
        """Called when the robot REACHES its navigation goal"""
        if self.phase == "GOTO_OBJECT":
            self.phase = "PICK_WAIT"

        elif self.phase == "GOTO_TARGET":
            self.phase = "PLACE_WAIT"

        elif self.phase == "PLACE_WAIT":
            self.task_index += 1
            self.phase = "GOTO_OBJECT"
