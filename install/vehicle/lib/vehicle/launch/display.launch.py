from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    return LaunchDescription([
        # Declare the model argument
        DeclareLaunchArgument(
            'model',
            default_value=str(FindPackageShare('vehicle') / 'urdf' / 'B4WTYPE3.urdf'),
            description='Path to the URDF file of the robot'
        ),
        
        # Joint State Publisher GUI Node
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen'
        ),
        
        # Robot State Publisher Node with robot description parameter
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': LaunchConfiguration('model')}]
        ),
        
        # RViz Node with configuration file
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz',
            output='screen',
            arguments=['-d', str(FindPackageShare('vehicle') / 'urdf' / 'B4WTYPE3.rviz')]
        ),
    ])

