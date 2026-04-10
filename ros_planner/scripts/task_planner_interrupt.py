#!/usr/bin/env python3
# task_planner.py

import time
import random

class TaskPlanner:
    """
    Two-stage task planner:
        1) Navigate to object
        2) Navigate to target
    """

    def __init__(self, tasks, pick_delay=2.0, place_delay=2.0):
        """
        tasks = [
            {   "id"
                "object": (x_obj, y_obj),
                "target": (x_tgt, y_tgt)
            },
            ...
        ]
        """
        # Attach a unique ID to each task
        self.tasks = []
        for i, t in enumerate(tasks):
            self.tasks.append({
                "id": i,                  # <-- stable task ID
                "object": t["object"],
                "target": t["target"],
            })

        self.task_index = 0
        self.phase = "GOTO_OBJECT"   # or "GOTO_TARGET"

        self.pick_delay = pick_delay
        self.place_delay = place_delay

        self._wait_start_time = None
        self.cancel_active = False


    #________________________________
    #        Helper 
    #___________________________

    def current_task_id(self):
        if self.task_index >= len(self.tasks):
            return None
        return self.tasks[self.task_index]["id"]

    def has_task(self):
        return self.task_index < len(self.tasks)

    def current_goal(self):

        # No more tasks → return None
        if self.task_index >= len(self.tasks):
            return None

        task = self.tasks[self.task_index]
        goal = {"task_id": task["id"]}

        if self.phase == "GOTO_OBJECT":
            return {"x": task["object"][0], "y": task["object"][1]}

        elif self.phase == "GOTO_TARGET":
            return {"x": task["target"][0], "y": task["target"][1]}

        elif self.phase in ["PICK_WAIT", "PLACE_WAIT"]:
            # No navigation goal during wait phases
            return None

        elif self.phase == "CANCEL_GOTO_OBJECT":
            # go back to pickup/object location to return the item
            return {"x": task["object"][0], "y": task["object"][1]}

        elif self.phase == "CANCEL_DROP_WAIT":
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

            

        ######## Cancel
        elif self.phase == "CANCEL_DROP_WAIT":
            if self._wait_start_time is None:
                self._wait_start_time = time.time()

            if time.time() - self._wait_start_time >= self.place_delay:
                print("Cancellation drop finished -> reshuffle and resume")
                self._wait_start_time = None
                self.cancel_active = False

                # reshuffle unfinished tasks like the GOTO_OBJECT interrupt case
                self.reshuffle_unfinished_tasks_randomly()

                # resume normal flow at GOTO_OBJECT
                self.phase = "GOTO_OBJECT"



    def advance(self):
        
        """Called when the robot REACHES its navigation goal"""
        if self.phase == "GOTO_OBJECT":
            self.phase = "PICK_WAIT"

        elif self.phase == "GOTO_TARGET":
            self.phase = "PLACE_WAIT"

        elif self.phase == "PLACE_WAIT":
            self.task_index += 1
            self.phase = "GOTO_OBJECT"

        elif self.phase == "CANCEL_GOTO_OBJECT":
            # reached pickup spot, now "drop back"
            self.phase = "CANCEL_DROP_WAIT"
            self._wait_start_time = None

    #############
    def reshuffle_unfinished_tasks_randomly(self):
        """
        Randomly reshuffle all unfinished tasks.
        Completed tasks remain untouched. WE will use global planner later
        """

        if self.task_index >= len(self.tasks):
            return

        completed = self.tasks[: self.task_index]

        current = self.tasks[self.task_index]

        remaining = self.tasks[self.task_index + 1 :]

        random.shuffle(remaining)

        self.tasks = completed + remaining + [current]

        self.task_index = len(completed)
    #_____________________
    # Insert going back to start point
    #________________________________

    def insert_task_at_current(self, task):
        """
        Insert a new task at the current task index.
        """
        self.tasks.insert(self.task_index, task)

    #_____________________________________________
    # make current task reverse 
    #_____________________________________________
    def make_reverse_task(self):
        """
        Create a task that goes back to the object and places it back.
        """
        current = self.tasks[self.task_index]

        return {
            "id": f"recovery_{current['id']}",
            "object": current["target"],  # go back to where we were going
            "target": current["object"],  # place back where it came from
        }

    #___________________
    #cancellation cost
    #______________________
    def make_cancellation_task(self, interrupted_task):
        return {
            "id": f"cancel_{interrupted_task['id']}",
            "type": "CANCEL",
            "object_pose": interrupted_task["object_pose"],
            "drop_pose": interrupted_task["start_pose"],
        }

    def start_cancellation(self):
        self.cancel_active = True
        self.phase = "CANCEL_GOTO_OBJECT"
        self._wait_start_time = None

        

