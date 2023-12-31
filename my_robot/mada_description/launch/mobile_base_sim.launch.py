import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import ExecuteProcess, DeclareLaunchArgument, IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node

import xacro

from time import sleep


def generate_launch_description():

    # Specify the name of the package and path to xacro file within the package
    pkg_name = 'mada_description'
    file_subpath = 'urdf/mada.xacro'

    world_subpath = 'config/mada_world.srdf'
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')


    # Use xacro to process the file
    xacro_file = os.path.join(get_package_share_directory(pkg_name),file_subpath)
    robot_description_raw = xacro.process_file(xacro_file).toxml()


    # Configure the node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_description_raw}],)# add other parameters here if required
    
    # Get world for Gazebo
    world_file = os.path.join(get_package_share_directory(pkg_name),world_subpath)
    
    world = LaunchConfiguration('world')

    declare_world_cmd = DeclareLaunchArgument(
        name='world',
        default_value=world_file,
        description='Full path to the world model file to load'
    )   

    jsp = Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            output='screen',
        )

    # Launch gazebo with world parameter
    gazebo = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
            launch_arguments={'world': world}.items()
        )

    sleep(3)

    # Spawn robot in Gazebo, out of robot_description topic
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                    arguments=['-topic', 'robot_description',
                                '-entity', 'mada'],
                    output='screen')


    # Run the node
    return LaunchDescription([    
        declare_world_cmd,  
        gazebo, 
        node_robot_state_publisher,
        jsp,
        spawn_entity
    ])
