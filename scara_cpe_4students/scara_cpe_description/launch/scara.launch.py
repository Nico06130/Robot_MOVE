import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import ExecuteProcess, DeclareLaunchArgument, IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node


import xacro


def generate_launch_description():

    # Specify the name of the package and path to xacro file within the package
    pkg_name = 'scara_cpe_description'
    file_subpath = 'urdf/scara_cpe.urdf.xacro'
    controller_subpath = 'config/scara_controller.yaml'

    # Use xacro to process the file
    xacro_file = os.path.join(get_package_share_directory(pkg_name), file_subpath)
    robot_description_raw = xacro.process_file(xacro_file).toxml()

    robot_controller= os.path.join(get_package_share_directory(pkg_name), controller_subpath)
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')


    # Configure the node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_raw,
                     'use_sim_time': use_sim_time}]  # add other parameters here if required
    )

    node_rviz = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', '/home/triton-01/Documents/MOVE_ws/src/S1_G10_Lehaut/scara_cpe_4students/scara_cpe_description/config/scara_cpe.rviz'], 
    )

    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[{"robot_description" : robot_description_raw}, robot_controller],
        output="both",
    )

    robot_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["scara_cpe_group_controller", "--controller-manager", "/controller_manager"],
        output="screen",
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
        output="screen",
    )
    # Run the node
    return LaunchDescription([
        control_node,
        joint_state_broadcaster_spawner,
        node_robot_state_publisher,
        robot_controller_spawner,
        
        node_rviz,
        


    ])
