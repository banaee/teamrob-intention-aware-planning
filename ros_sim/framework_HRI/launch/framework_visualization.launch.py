from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    pkg_share = get_package_share_directory("planner")

    # Path to your installed RViz config
    rviz_config = os.path.join(pkg_share, "config", "planner_visualization.rviz")

    # Add repo to PYTHONPATH so shared/ and domains/ are importable
    env = os.environ.copy()
    env["PYTHONPATH"] = (
        "/home/fatemeh/Github_human_robot_codes/Github/teamrob-intention-aware-planning"
        + ":" + env.get("PYTHONPATH", "")
    )

    return LaunchDescription([

        # ---- RViz ----
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            output="screen",
            arguments=["-d", rviz_config],
        ),

        # ---- Planner node ----
        # Switch executable between planner_2 (kitting) and planner_3 (dock)
        Node(
            package="framework_HRI",
            executable="planner_2",
            # executable="planner_3",
            name="continuous_sim",
            output="screen",
            env=env,
        ),
    ])