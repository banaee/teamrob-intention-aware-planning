from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    pkg_share = get_package_share_directory("planner")

    # Path to your installed RViz config
    rviz_config = os.path.join(pkg_share, "config", "planner_visualization.rviz")

    return LaunchDescription([

        # ---- RViz ----
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            output="screen",
            arguments=["-d", rviz_config],
        ),

        # ---- Your planner node ----
        Node(
            package="planner",
            executable="planner_2.py",   # MUST include .py
            name="planner_node",
            output="screen",
        ),
    ])

