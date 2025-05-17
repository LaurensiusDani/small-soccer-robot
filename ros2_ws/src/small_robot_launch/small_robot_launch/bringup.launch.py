import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='small_robot_control',
            executable='controller',
            name='robot_controller',
            output='screen'
        ),
        Node(
            package='small_robot_vision',
            executable='vision_node',
            name='vision_node',
            output='screen'
        ),
        Node(
            package='small_robot_comm',
            executable='serial_comm',
            name='serial_comm_node',
            output='screen'
        ),
    ])
