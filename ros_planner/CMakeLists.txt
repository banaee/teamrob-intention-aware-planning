cmake_minimum_required(VERSION 3.8)
project(planner)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)
find_package(rclpy REQUIRED)

# Install Python scripts (like ROS1)
install(
    PROGRAMS
        scripts/planner_1.py
        scripts/expert.py
        scripts/local_planner_priest.py
        scripts/task_planner.py
        scripts/bernstein_coeff_order10_arbitinterval.py
        scripts/planner_2.py
        scripts/expert_interrupt.py
        scripts/local_planner_priest_interrupt.py
        scripts/task_planner_interrupt.py
    DESTINATION lib/${PROJECT_NAME}
)

# Install launch files
install(
    DIRECTORY launch/
    DESTINATION share/${PROJECT_NAME}/launch
)

# Install RViz configs
install(
    DIRECTORY config/
    DESTINATION share/${PROJECT_NAME}/config
)


if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
