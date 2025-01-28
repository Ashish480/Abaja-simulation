import os
from pathlib import Path
from launch import LaunchDescription
from launch_ros.parameter_descriptions import ParameterValue
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # Set the package path
    pkg_share = FindPackageShare('vehicle').find('vehicle')

    # Define paths to necessary files
    urdf_model_path = os.path.join(pkg_share, 'urdf', 'B4WTYPE3.urdf')
    sdf_model_path = os.path.join(pkg_share, 'sdf', 'B4WTYPE3.sdf')
    controller_yaml_path = os.path.join(pkg_share, 'config', 'ackermann_controller.yaml')
    world_file_path = os.path.join(pkg_share, 'worlds', 'empty.world')  # Replace with actual world file if needed

    # Launch configuration variables
    use_gui = LaunchConfiguration('gui', default='true')
    use_robot_state_pub = LaunchConfiguration('use_robot_state_pub', default='true')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # Declare launch arguments
    declare_use_gui_cmd = DeclareLaunchArgument(
        name='gui',
        default_value='true',
        description='Flag to enable joint_state_publisher_gui'
    )
    declare_use_robot_state_pub_cmd = DeclareLaunchArgument(
        name='use_robot_state_pub',
        default_value='true',
        description='Whether to start the robot state publisher'
    )
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='true',
        description='Use simulation clock'
    )

    # Start Gazebo with the specified world file
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(FindPackageShare('gazebo_ros').find('gazebo_ros'), 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'world': world_file_path, 'verbose': 'true'}.items()
    )

    # Start robot state publisher
    robot_state_publisher = Node(
        condition=IfCondition(use_robot_state_pub),
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': ParameterValue(Command(['xacro ', urdf_model_path]), value_type=str)
        }],
    )

    # Add controller manager node
    controller_manager = Node(
        package='controller_manager',
        executable='ros2_control_node',
        name='controller_manager',
        parameters=[controller_yaml_path],
        output='screen',
    )

    # Spawn the vehicle model in Gazebo
    spawn_vehicle = TimerAction(
        period=5.0,  # Add a delay to ensure Gazebo is ready
        actions=[
            Node(
                package='gazebo_ros',
                executable='spawn_entity.py',
                name='spawn_model',
                arguments=[
                    '-entity', 'vehicle',
                    '-file', sdf_model_path,
                    '--ros-args', '--log-level', 'debug'
                ],
                output='screen',
            )
        ]
    )

    # Load forward_position_controller
    forward_position_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'forward_position_controller'],
        output='screen'
    )

    # Load forward_velocity_controller
    forward_velocity_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'forward_velocity_controller'],
        output='screen'
    )

    # Load joint_state_broadcaster
    joint_state_broadcaster = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'joint_state_broadcaster'],
        output='screen'
    )

    # Static transform publisher
    static_transform_publisher = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='tf_footprint_base',
        arguments=['0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '1.0', 'base_link', 'base_footprint']
    )

    # Add Ackermann Control Node
    ackermann_control_node = Node(
        package='vehicle',                  # Replace 'vehicle' with your package name
        executable='acker',    # Replace 'ackermann_control' with the actual executable name
        name='ackermann_control',          # Node name
        output='screen',                   # Outputs logs to terminal
        parameters=[{'use_sim_time': use_sim_time}]  # Pass use_sim_time if necessary
    )

    # Create the launch description
    ld = LaunchDescription()

    # Add the actions
    ld.add_action(declare_use_gui_cmd)
    ld.add_action(declare_use_robot_state_pub_cmd)
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(gazebo_launch)
    ld.add_action(robot_state_publisher)
    ld.add_action(controller_manager)  # Added controller_manager
    ld.add_action(spawn_vehicle)
    ld.add_action(static_transform_publisher)
    ld.add_action(forward_position_controller)  # Load forward_position_controller
    ld.add_action(forward_velocity_controller)  # Load forward_velocity_controller
    ld.add_action(joint_state_broadcaster)      # Load joint_state_broadcaster
    ld.add_action(ackermann_control_node)       # Add Ackermann Control Node

    return ld

