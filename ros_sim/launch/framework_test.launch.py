from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


# Maps the user-facing domain name → framework_HRI executable name
DOMAIN_MAP = {
    "kitting":     "planner_2",
    "scania_case": "planner_3",
}


def launch_setup(context, *args, **kwargs):
    domain = LaunchConfiguration("domain").perform(context)

    if domain not in DOMAIN_MAP:
        raise ValueError(
            f"[framework_visualization] Unknown domain '{domain}'. "
            f"Valid options: {list(DOMAIN_MAP.keys())}"
        )

    executable = DOMAIN_MAP[domain]
    print(f"[framework_visualization] Domain='{domain}' → launching '{executable}'")

    pkg_share = get_package_share_directory("planner")
    rviz_config = os.path.join(pkg_share, "config", "planner_visualization.rviz")

    # Add repo to PYTHONPATH so shared/ and domains/ are importable
    env = os.environ.copy()
    env["PYTHONPATH"] = (
        "/home/fatemeh/Github_human_robot_codes/Github/teamrob-intention-aware-planning"
        + ":" + env.get("PYTHONPATH", "")
    )

    return [
        # ---- RViz ----
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            output="screen",
            arguments=["-d", rviz_config],
        ),

        # ---- Planner node (selected by domain argument) ----
        Node(
            package="framework_HRI",
            executable=executable,
            name="continuous_sim",
            output="screen",
            env=env,
        ),
    ]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            "domain",
            default_value="kitting",
            description="Domain to run: 'kitting' (planner_2) or 'scania_case' (planner_3)",
        ),
        OpaqueFunction(function=launch_setup),
    ])