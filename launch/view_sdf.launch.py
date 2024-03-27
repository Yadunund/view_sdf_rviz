# Copyright 2024 Yadunund Vijay.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    declared_arguments = []
    declared_arguments.append(
        DeclareLaunchArgument(
                'sdf_file',
                description='The name of the robot sdf model.'
            )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
                'rviz',
                default_value='true',
                description='Open RViz.'
            )
    )
    return LaunchDescription(
        declared_arguments + [OpaqueFunction(function=launch_setup)]
    )

def launch_setup(context, *args, **kwargs):
    sdf_file = LaunchConfiguration('sdf_file')
    rviz_launch_arg = LaunchConfiguration('rviz')

    # Get the parser plugin convert sdf to urdf using robot_description topic
    with open(sdf_file.perform(context), 'r') as infp:
        robot_desc = infp.read()
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[
            {'use_sim_time': True},
            {'robot_description': robot_desc},
        ]
    )

    joint_state_sliders = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
    )

    # Launch rviz
    rviz_config = os.path.join(get_package_share_directory('view_sdf_rviz'), 'rviz', 'test_models.rviz')
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config],
        condition=IfCondition(rviz_launch_arg),
        parameters=[
            {'use_sim_time': True},
        ]
    )

    return [
        joint_state_sliders,
        robot_state_publisher,
        rviz
    ]
