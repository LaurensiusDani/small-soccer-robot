cmake_minimum_required(VERSION 3.8)
project(small_robot_launch)
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)

install(
  DIRECTORY small_robot_launch/
  DESTINATION lib/${PROJECT_NAME}
)
ament_python_install_module(
  PACKAGE_NAME small_robot_launch
)
ament_package()
