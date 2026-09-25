"""
world/: the world's side (T-H2). Simulator-agnostic and use-case-agnostic code
about what the human is and does: the human's executor (the stack machine that
runs a Script) and the executor's record, the ground truth. It may import
shared/ only: no body (mesa_sim/, ros_sim/) and no use case (domains/). The
bodies drive it; the robot's mind (shared/) never reads it.
"""
